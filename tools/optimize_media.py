#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
倍特爾官網 — 媒體交付轉檔工具 / media delivery optimiser.

把「客戶或生成工具丟進 assets/img/ 的原始檔」轉成網站真正要用的交付檔：
正確檔名（小寫 .jpg）、正確比例（取自 content/zh-hant/*.json 的 ratio 欄位）、
合理的長邊與檔案大小。也處理 assets/video/ 裡客戶交付的影片：內容 JSON 有對應
VID 資產 ID、但寬度超過 1920 或檔案超過交付預算的，會轉成 H.264／無音軌的交付檔。
原始檔（圖片與影片皆同）移到 assets/src/ 保存，不刪除。

    python tools/optimize_media.py --dry-run     # 只列出會做什麼，不動檔案
    python tools/optimize_media.py               # 實際轉檔
    python tools/optimize_media.py --verbose     # 連「已合規／未對應」的檔案也列出

規則（見下方常數）：

    圖片比例    以 content/zh-hant/*.json 的媒體物件 ratio 為唯一真實來源
    圖片長邊    海報／頁首主視覺（hero、banner_media）1920，其餘 1600；一律不放大
    圖片編碼    JPEG，quality 82，progressive，sRGB；超過 400 KB 就往下降到 70
    圖片裁切    照片置中裁切；平底技術圖形改用「以邊緣色延伸畫布」而非裁切
                （平底判定：沿四邊取樣，若所有取樣點與中位色差 ≤ 8 即視為平底）
    影片        寬度上限 1920（等比縮小，尺寸取偶數）；H.264（libx264，-preset slow）、
                無音軌、+faststart；交付預算 3MB，crf 28 起，超過預算就用 crf 31 重試一次
    保護        logo*／favicon* 一律不碰；已符合上述全部條件的檔案也不碰

依賴：Pillow（PIL）。影片轉檔另需 ffmpeg／ffprobe（須在 PATH 上）；
找不到時會清楚提示並略過所有影片，圖片轉檔不受影響。
"""

from __future__ import annotations

import argparse
import io
import json
import shutil
import statistics
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    sys.exit("需要 Pillow：pip install pillow")

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content" / "zh-hant"
IMG_DIR = ROOT / "assets" / "img"
VIDEO_DIR = ROOT / "assets" / "video"
SRC_DIR = ROOT / "assets" / "src"

# 長邊上限：海報與頁首主視覺會滿版呈現，其餘為段落／卡片配圖。
LONG_EDGE_HERO = 1920
LONG_EDGE_OTHER = 1600
# 這些 JSON 路徑片段代表「頁首主視覺」版位。
HERO_PATH_PARTS = ("hero", "banner_media")

QUALITY_START = 82
QUALITY_FLOOR = 70
QUALITY_STEP = 4
TARGET_BYTES = 400 * 1024

# 比例容差：與版位比例相差超過這個比率就要裁切／延伸畫布。
RATIO_TOLERANCE = 0.01
# 平底判定：邊框取樣點與中位色的最大差值。
FLAT_BORDER_MAX_DEV = 8

PROTECTED_PREFIXES = ("logo", "favicon")
SOURCE_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp", ".avif")

# 影片：寬度上限、交付預算（超過就轉檔）、編碼參數。
VIDEO_MAX_WIDTH = 1920
VIDEO_TARGET_BYTES = 3 * 1024 * 1024
VIDEO_CRF_START = 28
VIDEO_CRF_RETRY = 31
VIDEO_PRESET = "slow"


# ---------------------------------------------------------------------------
# 版位表 —— 從 content/zh-hant/*.json 讀出每個資產的比例與用途
# ---------------------------------------------------------------------------

def collect_slots() -> dict[str, dict]:
    """回傳 {檔名 stem: {id, ratio, long_edge}}，涵蓋圖片與影片海報。"""
    slots: dict[str, dict] = {}

    def add(file_path: str, asset_id: str, ratio: str, json_path: str) -> None:
        stem = Path(file_path).stem
        hero = any(part in json_path.split(".") for part in HERO_PATH_PARTS)
        slots[stem] = {
            "id": asset_id,
            "ratio": ratio,
            "long_edge": LONG_EDGE_HERO if hero else LONG_EDGE_OTHER,
        }

    def walk(node, json_path: str) -> None:
        if isinstance(node, dict):
            if isinstance(node.get("id"), str) and isinstance(node.get("file"), str):
                ratio = node.get("ratio") or "16-9"
                if node.get("poster"):
                    # 影片本身不是本工具的處理對象，只處理它的海報圖。
                    add(node["poster"], node["id"] + "（海報）", ratio, json_path + ".hero")
                else:
                    add(node["file"], node["id"], ratio, json_path)
            for key, value in node.items():
                walk(value, f"{json_path}.{key}")
        elif isinstance(node, list):
            for item in node:
                walk(item, json_path)

    for path in sorted(CONTENT_DIR.glob("*.json")):
        walk(json.loads(path.read_text(encoding="utf-8")), path.stem)
    return slots


def collect_video_slots() -> dict[str, dict]:
    """回傳 {檔名 stem: {id, file}}，只涵蓋 VID 開頭的影片本身（不含海報圖）。"""
    slots: dict[str, dict] = {}

    def walk(node) -> None:
        if isinstance(node, dict):
            if (isinstance(node.get("id"), str) and isinstance(node.get("file"), str)
                    and node["id"].startswith("VID-") and node.get("poster")):
                slots[Path(node["file"]).stem] = {"id": node["id"], "file": node["file"]}
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    for path in sorted(CONTENT_DIR.glob("*.json")):
        walk(json.loads(path.read_text(encoding="utf-8")))
    return slots


def ratio_value(ratio: str) -> float | None:
    """'16-9' → 1.777…；'fill' 等非固定比例回傳 None（不做幾何調整）。"""
    parts = ratio.split("-")
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        return None
    return int(parts[0]) / int(parts[1])


# ---------------------------------------------------------------------------
# 影像處理
# ---------------------------------------------------------------------------

def load_rgb(path: Path) -> Image.Image:
    im = Image.open(path)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        flat = Image.new("RGB", im.size, (255, 255, 255))
        flat.paste(im, mask=im.split()[-1])
        return flat
    return im.convert("RGB")


def border_colour(im: Image.Image) -> tuple[tuple[int, int, int], int]:
    """沿四邊取樣，回傳（中位色, 最大色差）。色差小 = 平底。"""
    w, h = im.size
    inset = max(2, min(w, h) // 200)
    step_x = max(1, w // 200)
    step_y = max(1, h // 200)
    samples = []
    for x in range(0, w, step_x):
        samples.append(im.getpixel((x, inset)))
        samples.append(im.getpixel((x, h - 1 - inset)))
    for y in range(0, h, step_y):
        samples.append(im.getpixel((inset, y)))
        samples.append(im.getpixel((w - 1 - inset, y)))
    median = tuple(int(statistics.median(s[i] for s in samples)) for i in range(3))
    deviation = max(max(abs(s[i] - median[i]) for i in range(3)) for s in samples)
    return median, deviation


def fit_ratio(im: Image.Image, want: float) -> tuple[Image.Image, str]:
    """把畫面調整到目標比例。平底圖形延伸畫布，其餘置中裁切。"""
    w, h = im.size
    current = w / h
    if abs(current - want) / want <= RATIO_TOLERANCE:
        return im, "比例相符"

    colour, deviation = border_colour(im)
    if deviation <= FLAT_BORDER_MAX_DEV:
        if current < want:                       # 太窄 → 左右補邊
            new_w, new_h = round(h * want), h
        else:                                    # 太寬 → 上下補邊
            new_w, new_h = w, round(w / want)
        canvas = Image.new("RGB", (new_w, new_h), colour)
        canvas.paste(im, ((new_w - w) // 2, (new_h - h) // 2))
        return canvas, f"延伸畫布 rgb{colour}"

    if current > want:                           # 太寬 → 裁掉左右
        new_w, new_h = round(h * want), h
    else:                                        # 太高 → 裁掉上下
        new_w, new_h = w, round(w / want)
    left, top = (w - new_w) // 2, (h - new_h) // 2
    return im.crop((left, top, left + new_w, top + new_h)), "置中裁切"


def downscale(im: Image.Image, long_edge: int) -> tuple[Image.Image, bool]:
    w, h = im.size
    if max(w, h) <= long_edge:
        return im, False
    scale = long_edge / max(w, h)
    return im.resize((round(w * scale), round(h * scale)), Image.LANCZOS), True


def encode(im: Image.Image) -> tuple[bytes, int]:
    """逐步降品質直到 ≤ TARGET_BYTES，最低到 QUALITY_FLOOR。"""
    data = b""
    quality = QUALITY_START
    while True:
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=quality, progressive=True, optimize=True)
        data = buf.getvalue()
        if len(data) <= TARGET_BYTES or quality <= QUALITY_FLOOR:
            return data, quality
        quality = max(QUALITY_FLOOR, quality - QUALITY_STEP)


def is_compliant(path: Path, slot: dict) -> bool:
    """已是交付形態的檔案完全不碰。"""
    if path.suffix != ".jpg" or path.name != path.name.lower():
        return False
    if path.stat().st_size > TARGET_BYTES:
        return False
    with Image.open(path) as im:
        if not im.info.get("progressive"):
            return False
        w, h = im.size
        if max(w, h) > slot["long_edge"]:
            return False
        want = ratio_value(slot["ratio"])
        if want is not None and abs(w / h - want) / want > RATIO_TOLERANCE:
            return False
    return True


# ---------------------------------------------------------------------------
# 影片處理
# ---------------------------------------------------------------------------

def has_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def probe_video(path: Path) -> tuple[int, int, int]:
    """回傳（寬, 高, 檔案大小 bytes）。"""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    stream = json.loads(out.stdout)["streams"][0]
    return int(stream["width"]), int(stream["height"]), path.stat().st_size


def is_video_compliant(width: int, height: int, size_bytes: int) -> bool:
    """已是交付形態的影片完全不碰。"""
    return width <= VIDEO_MAX_WIDTH and size_bytes <= VIDEO_TARGET_BYTES


def transcode_video(path: Path, crf: int) -> Path:
    """跑 ffmpeg，回傳轉檔結果的暫存檔路徑（呼叫者負責之後刪除或搬移）。

    暫存檔開在 VIDEO_DIR 底下，跟交付路徑同一個磁碟機，之後才能用
    Path.replace() 原子搬移（系統預設暫存目錄可能在不同磁碟機，搬移會失敗）。
    """
    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False, dir=VIDEO_DIR)
    tmp.close()
    tmp_path = Path(tmp.name)
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(path),
         "-vf", f"scale=w='min({VIDEO_MAX_WIDTH}\\,iw)':h=-2",
         "-c:v", "libx264", "-preset", VIDEO_PRESET, "-crf", str(crf),
         "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart",
         str(tmp_path)],
        capture_output=True, text=True, check=True,
    )
    return tmp_path


def archive_with_dedupe(path: Path, dry_run: bool) -> Path:
    """把原始檔搬到 assets/src/；同名檔案已存在時，保留較新的一份，
    較舊的一份改用數字後綴（archive-1.mp4、archive-2.mp4…）。"""
    archive = SRC_DIR / path.name
    if dry_run:
        return archive
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        newer, older = ((path, archive) if path.stat().st_mtime >= archive.stat().st_mtime
                         else (archive, path))
        n = 1
        bumped = archive.with_name(f"{archive.stem}-{n}{archive.suffix}")
        while bumped.exists():
            n += 1
            bumped = archive.with_name(f"{archive.stem}-{n}{archive.suffix}")
        if older is archive:
            archive.replace(bumped)
            path.replace(archive)
        else:
            path.replace(bumped)
    else:
        path.replace(archive)
    return archive


def process_video(path: Path, slot: dict, dry_run: bool) -> dict:
    """回傳這個影片的處理結果（dry-run 時仍會實際轉檔到暫存檔以回報大小，但不寫入交付路徑）。"""
    before_w, before_h, before_bytes = probe_video(path)

    crf = VIDEO_CRF_START
    tmp_path = transcode_video(path, crf)
    note = ""
    if tmp_path.stat().st_size > VIDEO_TARGET_BYTES:
        tmp_path.unlink(missing_ok=True)
        crf = VIDEO_CRF_RETRY
        tmp_path = transcode_video(path, crf)
        note = f"仍逾 {VIDEO_TARGET_BYTES // (1024 * 1024)}MB，已用 crf {crf} 重試"

    after_w, after_h, after_bytes = probe_video(tmp_path)

    target = VIDEO_DIR / f"{path.stem.lower()}.mp4"
    archive = SRC_DIR / path.name
    if not dry_run:
        archive = archive_with_dedupe(path, dry_run=False)
        tmp_path.replace(target)
    else:
        tmp_path.unlink(missing_ok=True)

    return {
        "action": "轉檔",
        "asset": slot["id"],
        "before": f"{before_w}×{before_h} mp4 {before_bytes / 1024 / 1024:.1f}MB",
        "after": f"{after_w}×{after_h} mp4 crf{crf} {after_bytes / 1024 / 1024:.1f}MB",
        "note": note or "縮寬／轉碼",
        "target": target,
        "archive": archive,
    }


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def candidates() -> list[Path]:
    """assets/img/ 的所有影像，加上誤放在 assets/video/ 的海報圖。"""
    found = [p for p in sorted(IMG_DIR.glob("*")) if p.is_file()]
    if VIDEO_DIR.is_dir():
        found += [p for p in sorted(VIDEO_DIR.glob("*"))
                  if p.is_file() and p.suffix.lower() in SOURCE_EXTS]
    return found


def process(path: Path, slot: dict, dry_run: bool) -> dict:
    """回傳這個檔案的處理結果（dry-run 時不寫任何檔案）。"""
    im = load_rgb(path)
    before = im.size
    before_bytes = path.stat().st_size
    want = ratio_value(slot["ratio"])
    geometry = "比例未定義"
    if want is not None:
        im, geometry = fit_ratio(im, want)
    im, resized = downscale(im, slot["long_edge"])
    data, quality = encode(im)

    target = IMG_DIR / f"{path.stem.lower()}.jpg"
    archive = SRC_DIR / path.name
    if not dry_run:
        SRC_DIR.mkdir(parents=True, exist_ok=True)
        if archive.exists():
            archive.unlink()
        path.replace(archive)
        target.write_bytes(data)
    return {
        "action": "轉檔",
        "asset": slot["id"],
        "before": (f"{before[0]}×{before[1]} {path.suffix.lstrip('.').lower()} "
                   f"{before_bytes / 1024:.0f}KB"),
        "after": f"{im.size[0]}×{im.size[1]} jpg q{quality} {len(data) / 1024:.0f}KB",
        "note": geometry + ("／縮圖" if resized else ""),
        "target": target,
        "archive": archive,
    }


def display_width(text: str) -> int:
    """CJK 全形字在終端機佔兩欄，直接用 len() 會讓表格歪掉。"""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)


def pad(text: str, width: int) -> str:
    return text + " " * max(0, width - display_width(text))


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(description="把原始媒體檔轉成網站交付檔")
    parser.add_argument("--dry-run", action="store_true", help="只列出會做什麼，不動檔案")
    parser.add_argument("--verbose", action="store_true",
                        help="連已合規、受保護、未對應的檔案也一併列出")
    args = parser.parse_args()

    if not CONTENT_DIR.is_dir():
        print(f"找不到內容目錄：{CONTENT_DIR}", file=sys.stderr)
        return 1
    slots = collect_slots()

    rows: list[tuple[str, str, str, str, str]] = []
    converted = 0
    for path in candidates():
        rel = path.relative_to(ROOT).as_posix()
        stem = path.stem.lower()
        if stem.startswith(PROTECTED_PREFIXES):
            if args.verbose:
                rows.append((rel, "保護", "—", "—", "logo／favicon 不處理"))
            continue
        if path.suffix.lower() not in SOURCE_EXTS:
            if args.verbose:
                rows.append((rel, "略過", "—", "—", "非影像檔"))
            continue
        slot = slots.get(stem)
        if slot is None:
            if args.verbose:
                rows.append((rel, "未對應", "—", "—", "檔名不在任何版位的資產對應表中"))
            continue
        if path.parent == IMG_DIR and is_compliant(path, slot):
            if args.verbose:
                rows.append((rel, "已合規", slot["id"], "—", "不動"))
            continue
        result = process(path, slot, args.dry_run)
        converted += 1
        rows.append((rel, result["action"], result["asset"],
                     f'{result["before"]} → {result["after"]}', result["note"]))

    video_slots = collect_video_slots()
    ffmpeg_ok = has_ffmpeg()
    if not ffmpeg_ok and video_slots:
        print("找不到 ffmpeg／ffprobe（須在 PATH 上），略過所有影片轉檔；圖片轉檔不受影響。",
              file=sys.stderr)
    if VIDEO_DIR.is_dir():
        for path in sorted(VIDEO_DIR.glob("*.mp4")):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT).as_posix()
            stem = path.stem.lower()
            slot = video_slots.get(stem)
            if slot is None:
                if args.verbose:
                    rows.append((rel, "未對應", "—", "—", "檔名不在任何版位的資產對應表中"))
                continue
            if not ffmpeg_ok:
                rows.append((rel, "略過", slot["id"], "—", "找不到 ffmpeg，無法轉檔"))
                continue
            width, height, size_bytes = probe_video(path)
            if is_video_compliant(width, height, size_bytes):
                if args.verbose:
                    rows.append((rel, "已合規", slot["id"], "—", "不動"))
                continue
            result = process_video(path, slot, args.dry_run)
            converted += 1
            rows.append((rel, result["action"], result["asset"],
                         f'{result["before"]} → {result["after"]}', result["note"]))

    if not rows:
        print("沒有需要處理的檔案。")
        return 0

    headers = ("檔案", "動作", "資產 ID", "before → after", "說明")
    widths = [max(display_width(str(r[i])) for r in (*rows, headers)) for i in range(5)]
    line = "  ".join("─" * w for w in widths)
    print("  ".join(pad(h, w) for h, w in zip(headers, widths)))
    print(line)
    for row in rows:
        print("  ".join(pad(str(c), w) for c, w in zip(row, widths)))
    print(line)
    if args.dry_run:
        print(f"（--dry-run）會轉檔 {converted} 個檔案，原始檔會移到 "
              f"{SRC_DIR.relative_to(ROOT).as_posix()}/。實際執行請去掉 --dry-run。")
    else:
        print(f"已轉檔 {converted} 個檔案；原始檔已移到 "
              f"{SRC_DIR.relative_to(ROOT).as_posix()}/（不會進 dist/）。")
        print("接著執行：python build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
