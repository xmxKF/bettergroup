#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
倍特爾科技集團 官網 — 靜態網站產生器 / static site generator.

    python build.py                 # 產出全部語言到 dist/
    python build.py --clean         # 先清空 dist/ 再產出
    python build.py --lang zh-hant  # 只產出指定語言（可重複或用逗號分隔）
    python build.py --validate-only # 只跑翻譯結構與資產檢查，不寫檔
    python build.py --allow-missing-media   # 開發用：缺媒體只警告不失敗（CI 永不使用）

依賴：jinja2（見 requirements.txt）。除此之外只用標準函式庫。

輸出結構：
    dist/index.html            語言分流閘道（JS 偵測 + meta refresh + 純連結）
    dist/404.html              找不到頁面（四語連結 + 導回閘道）
    dist/<lang>/<page>.html    每個語言每一頁
    dist/assets/…              由 assets/ 的 css/img/js/video 複製
                                （圖片／css／js 超過 1.5MB、影片超過 8MB 的檔案略過）
    dist/sitemap.xml           含 hreflang alternates
    dist/robots.txt
    dist/.nojekyll             GitHub Pages 不要跑 Jekyll
    dist/CNAME                 僅在網址是自訂網域（非 *.github.io）時輸出
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse, urlsplit

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
except ImportError:  # pragma: no cover
    sys.exit("需要 jinja2：pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
TEMPLATE_DIR = ROOT / "templates"
ASSET_DIR = ROOT / "assets"
DIST_DIR = ROOT / "dist"

# 正式網址。優先順序：--base-url > 環境變數 SITE_URL > 這一行的預設值。
# （GitHub Actions 會把 SITE_URL 設成專案頁面網址或 repository variable 指定的自訂網域。）
SITE_URL = "https://www.bettertechgroup.com"

# 複製 assets/ 時的大小上限，依檔案類型分開設定。交付檔應遠低於此值
# （圖片 ≤ 400KB、影片 ≤ 3MB，見 tools/optimize_media.py），超過上限就代表
# 那是還沒轉檔的原始檔 —— 用 tools/optimize_media.py 轉成交付檔。
MAX_ASSET_BYTES = 1.5 * 1024 * 1024        # 圖片／css／js
MAX_VIDEO_BYTES = 8 * 1024 * 1024          # 影片（.mp4／.webm）
# 只有這四個子目錄會進 dist/。assets/src/ 是 optimize_media.py 保存的原始檔庫，
# 刻意不列在這裡，因此永遠不會被複製到 dist/。
ASSET_SUBDIRS = ("css", "img", "js", "video")

# 外殼資產：由 templates/ 直接引用（favicon、header/footer/閘道的品牌標記），
# 不會出現在任何 content JSON 的 media 物件裡，因此要在白名單裡才不會被當成無人參照。
SHELL_ASSETS = {
    "assets/img/favicon.ico",
    "assets/img/favicon-32.png",
    "assets/img/favicon-180.png",
    "assets/img/logo-264.png",
    "assets/img/xyl-logo-full.png",
}

# ---------------------------------------------------------------------------
# 語言表 — 新增語言只要在這裡加一列，並建立 content/<code>/
# ---------------------------------------------------------------------------
# latin=True 代表該語言以詞為單位、詞間需要空格（首頁 H1 由多行組成，
# 換行處要補一個空白；CJK 不補）。新增拉丁語系語言時務必設為 True。
LANGS = [
    # code       html lang 屬性      hreflang    latin  Google Fonts 追加字體家族
    {"code": "zh-hant", "html_lang": "zh-Hant-HK", "hreflang": "zh-Hant", "latin": False,
     "font_family": "Noto+Sans+TC:wght@400;500;700"},
    {"code": "zh-hans", "html_lang": "zh-Hans-CN", "hreflang": "zh-Hans", "latin": False,
     "font_family": "Noto+Sans+SC:wght@400;500;700"},
    {"code": "en", "html_lang": "en", "hreflang": "en", "latin": True,
     "font_family": ""},
    {"code": "ja", "html_lang": "ja", "hreflang": "ja", "latin": False,
     "font_family": "Noto+Sans+JP:wght@400;500;700"},
]

REFERENCE_LANG = "zh-hant"   # 結構比對基準，也是 x-default
X_DEFAULT = "zh-hant"

BASE_FONT_FAMILY = "Inter:wght@400;500;600;700"

# ---------------------------------------------------------------------------
# 頁面表 — key 對應 content/<lang>/<key>.json
# 只有「模板存在且 content JSON 存在」的頁面才會被產出，因此第二階段先只有 index，
# 第三階段補上模板與 JSON 後不需要再改這張表。
# ---------------------------------------------------------------------------
PAGES = [
    # key,                     template,               output,                       priority
    ("index",                  "index.html",           "index.html",                  "1.0"),
    ("about",                  "about.html",           "about.html",                  "0.8"),
    ("services",               "services.html",        "services.html",               "0.8"),
    ("equipment",              "equipment.html",       "equipment.html",              "0.8"),
    ("ai",                     "ai.html",              "ai.html",                     "0.8"),
    ("contact",                "contact.html",         "contact.html",                "0.8"),
    ("equipment-lithography",  "equipment-detail.html", "equipment-lithography.html", "0.6"),
    ("equipment-etch",         "equipment-detail.html", "equipment-etch.html",        "0.6"),
    ("equipment-cvd",          "equipment-detail.html", "equipment-cvd.html",         "0.6"),
    ("equipment-bake",         "equipment-detail.html", "equipment-bake.html",        "0.6"),
    ("equipment-implant",      "equipment-detail.html", "equipment-implant.html",     "0.6"),
    ("equipment-cmp",          "equipment-detail.html", "equipment-cmp.html",         "0.6"),
    ("equipment-cleaning",     "equipment-detail.html", "equipment-cleaning.html",    "0.6"),
    ("equipment-inspection",   "equipment-detail.html", "equipment-inspection.html",  "0.6"),
    ("equipment-mask",         "equipment-detail.html", "equipment-mask.html",        "0.6"),
]

# ---------------------------------------------------------------------------
# 語言不變欄位：這些 key 在所有語言必須逐字相同（資產 ID、檔名、連結、品牌、數字…）
# ---------------------------------------------------------------------------
INVARIANT_KEYS = {
    "id", "file", "poster", "ratio",          # 媒體物件
    "href", "match",                          # 連結
    "brands", "en", "title_lat", "num",       # 品牌 / 拉丁名 / 編號
    "logo", "email", "mailto", "copyright_year",
    "legal_name_en",
}

# 例外：這些完整路徑的鍵名雖然落在 INVARIANT_KEYS，內容卻是可翻譯的（欄位抬頭／驗證訊息、
# 語言選單中該語言的自稱），不是不變值本身，因此不套用語言不變規則。
INVARIANT_PATH_EXCEPTIONS = {
    "common.footer.labels.email",
    "common.form.messages.email",
    "common.form.mail.email",
    "common.languages.en",          # 語言物件，其 name 可翻譯（日文版寫「英語」等）
}

# 以完整路徑指定的語言不變欄位（鍵名本身太常見、不能列入 INVARIANT_KEYS）。
# 語言切換器的標籤 繁 / 简 / EN / 日 在四種語言必須完全相同。
INVARIANT_PATH_PATTERNS = (
    re.compile(r"^common\.languages\.[A-Za-z-]+\.label$"),
    re.compile(r"^common\.site\.phone(_href)?$"),
)

# 允許「基準語言有字、某個翻譯刻意留空」的完整路徑。
# 這幾張卡在拉丁語系裡只掛拉丁標題（title_lat，例如 Digital Twin），中文／日文才另有標題；
# 除了這裡列出的路徑之外，翻譯把非空字串留成空字串一律視為漏譯（見 compare_structure）。
EMPTY_ALLOWED_PATTERNS = (
    re.compile(r"^ai\.pillars\.entries\[\d+\]\.title$"),
    re.compile(r"^index\.ai\.pillars\[\d+\]\.title$"),
)

ASSET_ID_RE = re.compile(r"^(IMG|VID)-([A-Z0-9]+)-(\d{2})$")
IMG_EXTS = ("jpg", "jpeg", "png", "webp", "avif")

# 網站網址的主機名（每段 1–63 字元、不以 - 開頭或結尾，全長 ≤ 253）。
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$"
)


class BuildError(Exception):
    """翻譯結構或資產對應錯誤 — 一律讓 build 明確失敗。"""


# ===========================================================================
# 內容載入與驗證
# ===========================================================================

def read_json(path: Path):
    with path.open(encoding="utf-8") as fh:
        try:
            return json.load(fh)
        except json.JSONDecodeError as exc:
            raise BuildError(f"{path} JSON 解析失敗：{exc}") from exc


def available_langs() -> list[dict]:
    """LANGS 中實際有 content/<code>/ 目錄的語言。"""
    return [l for l in LANGS if (CONTENT_DIR / l["code"]).is_dir()]


def check_language_dirs() -> None:
    """content/ 底下必須剛好有 LANGS 列出的語言目錄，大小寫完全相符。

    少一個目錄不會讓任何檢查失敗 —— 站台會靜默縮小（入口頁、hreflang、sitemap 都只剩
    剩下的語言），因此這裡把它變成硬性條件。刻意只產出部分語言時請用 --lang。
    """
    if not CONTENT_DIR.is_dir():
        raise BuildError(f"找不到內容目錄：{CONTENT_DIR}")
    actual = {p.name for p in CONTENT_DIR.iterdir() if p.is_dir()}
    expected = {l["code"] for l in LANGS}
    problems = []
    missing = sorted(expected - actual)
    if missing:
        problems.append(
            "缺少語言目錄：" + "、".join(f"content/{m}/" for m in missing)
            + " —— 少一個語言就會從全站、語言閘道與 sitemap 靜默消失"
        )
    extra = sorted(n for n in actual - expected if not n.startswith((".", "_")))
    if extra:
        problems.append(
            "content/ 有 LANGS 未列出的目錄：" + "、".join(extra)
            + " —— 這些內容不會被產出，請加進 build.py 的 LANGS 或移除"
        )
    if problems:
        raise BuildError(
            "\n    ".join(problems)
            + "\n    （確定只要處理部分語言時，請用 --lang 明確指定。）"
        )


def load_content(lang: str) -> dict:
    """讀入 content/<lang>/*.json，回傳 {檔名去副檔名: 內容}。"""
    lang_dir = CONTENT_DIR / lang
    if not lang_dir.is_dir():
        raise BuildError(f"找不到內容目錄：{lang_dir}")
    files = {}
    for path in sorted(lang_dir.glob("*.json")):
        files[path.stem] = read_json(path)
    if "common" not in files:
        raise BuildError(f"{lang_dir} 缺少 common.json")
    return files


def compare_structure(ref, other, path: str, ref_lang: str, lang: str) -> str | None:
    """遞迴比對兩份內容的鍵與長度。回傳第一個差異的描述，相同則回傳 None。"""
    if isinstance(ref, dict):
        if not isinstance(other, dict):
            return f"{path}：{ref_lang} 是 object，{lang} 是 {type(other).__name__}"
        missing = [k for k in ref if k not in other]
        if missing:
            return f"{path}.{missing[0]}：{lang} 缺少此鍵（{ref_lang} 有）"
        extra = [k for k in other if k not in ref]
        if extra:
            return f"{path}.{extra[0]}：{lang} 多出此鍵（{ref_lang} 沒有）"
        for key in ref:
            found = compare_structure(ref[key], other[key], f"{path}.{key}", ref_lang, lang)
            if found:
                return found
        return None

    if isinstance(ref, list):
        if not isinstance(other, list):
            return f"{path}：{ref_lang} 是 list，{lang} 是 {type(other).__name__}"
        if len(ref) != len(other):
            return (f"{path}：list 長度不同（{ref_lang}={len(ref)}，"
                    f"{lang}={len(other)}）— 各語言必須逐項對應")
        for i, item in enumerate(ref):
            found = compare_structure(item, other[i], f"{path}[{i}]", ref_lang, lang)
            if found:
                return found
        return None

    # 型別必須完全相符。以前 None 有逃生門，於是 title=null 這種漏譯可以通過驗證，
    # 再由 Jinja（StrictUndefined 不擋已定義的 None）原樣印出字面 "None"。
    if type(ref) is not type(other):
        return f"{path}：型別不同（{ref_lang}={type(ref).__name__}，{lang}={type(other).__name__}）"
    # 必填非空字串：基準語言有字、翻譯卻是空字串＝漏譯，頁面會靜默變空白。
    # 刻意留空的位置列在 EMPTY_ALLOWED_PATTERNS。
    if isinstance(ref, str) and ref.strip() and not other.strip():
        if not any(p.fullmatch(path) for p in EMPTY_ALLOWED_PATTERNS):
            return (f"{path}：{lang} 是空字串，但 {ref_lang} 有內容"
                    f"（{ref[:24]}…）— 漏譯欄位不得留空")
    return None


def compare_invariants(ref, other, path: str, ref_lang: str, lang: str, out: list) -> None:
    """收集所有「應逐字相同」欄位的差異。"""
    if isinstance(ref, dict) and isinstance(other, dict):
        for key in ref:
            if key not in other:
                continue
            child = f"{path}.{key}"
            keyed = key in INVARIANT_KEYS and child not in INVARIANT_PATH_EXCEPTIONS
            pathed = any(p.fullmatch(child) for p in INVARIANT_PATH_PATTERNS)
            if keyed or pathed:
                if ref[key] != other[key]:
                    out.append(f"{child}：{ref_lang}={ref[key]!r} 但 {lang}={other[key]!r}")
            else:
                compare_invariants(ref[key], other[key], child, ref_lang, lang, out)
    elif isinstance(ref, list) and isinstance(other, list) and len(ref) == len(other):
        for i, item in enumerate(ref):
            compare_invariants(item, other[i], f"{path}[{i}]", ref_lang, lang, out)


def validate_translations(contents: dict[str, dict]) -> None:
    """每個語言的鍵結構與 list 長度必須與 zh-hant 完全一致。"""
    if REFERENCE_LANG not in contents:
        return
    reference = contents[REFERENCE_LANG]
    for lang, files in contents.items():
        if lang == REFERENCE_LANG:
            continue
        # 尚未翻譯的頁面只警告不中止 —— 頁面表本來就允許「某語言還沒有這一頁」，
        # 產出時會自動略過（見 build() 的 `if key not in files`）。
        missing = sorted(set(reference) - set(files))
        if missing:
            print(f"  ! [{lang}] 尚未翻譯的內容檔（這些頁面不會產出）："
                  f"{', '.join(m + '.json' for m in missing)}")
        shared = [name for name in sorted(reference) if name in files]
        for name in shared:
            found = compare_structure(reference[name], files[name], name,
                                      REFERENCE_LANG, lang)
            if found:
                raise BuildError(f"[{lang}] 結構與 {REFERENCE_LANG} 不符 → {found}")
        problems: list[str] = []
        for name in shared:
            compare_invariants(reference[name], files[name], name,
                               REFERENCE_LANG, lang, problems)
        if problems:
            joined = "\n    ".join(problems)
            raise BuildError(
                f"[{lang}] 以下欄位為語言不變欄位，必須逐字沿用 {REFERENCE_LANG}：\n    {joined}"
            )


# ===========================================================================
# 資產檢查
# ===========================================================================

def collect_media(node, path: str, out: list) -> None:
    """找出所有媒體物件（同時具備 id 與 file 的 dict）。"""
    if isinstance(node, dict):
        if isinstance(node.get("id"), str) and isinstance(node.get("file"), str):
            out.append((path, node))
        for key, value in node.items():
            collect_media(value, f"{path}.{key}", out)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            collect_media(item, f"{path}[{i}]", out)


def check_media_object(where: str, m: dict) -> list[str]:
    """檢查資產 ID 與檔案路徑是否符合命名對應規則。"""
    problems = []
    match = ASSET_ID_RE.match(m["id"])
    if not match:
        return [f"{where}：資產 ID「{m['id']}」不符 IMG-<PAGE>-NN / VID-<PAGE>-NN 格式"]
    kind, page, num = match.group(1), match.group(2).lower(), match.group(3)

    if kind == "IMG":
        expect = f"assets/img/{page}-{num}"
        stem, _, ext = m["file"].rpartition(".")
        if stem != expect or ext.lower() not in IMG_EXTS:
            problems.append(f"{where}：{m['id']} 應對應 {expect}.(jpg|png|webp)，實為「{m['file']}」")
        if m.get("poster"):
            problems.append(f"{where}：{m['id']} 是圖片，不應有 poster")
    else:
        expect = f"assets/video/{page}-{num}.mp4"
        if m["file"] != expect:
            problems.append(f"{where}：{m['id']} 應對應 {expect}，實為「{m['file']}」")
        poster = m.get("poster", "")
        pstem, _, pext = poster.rpartition(".")
        if pstem != f"assets/img/{page}-{num}-poster" or pext.lower() not in IMG_EXTS:
            problems.append(
                f"{where}：{m['id']} 的 poster 應為 assets/img/{page}-{num}-poster.jpg，實為「{poster}」"
            )
    if not m.get("ratio"):
        problems.append(f"{where}：{m['id']} 缺少 ratio")
    if not m.get("alt"):
        problems.append(f"{where}：{m['id']} 缺少 alt")
    return problems


def validate_assets(files: dict, lang: str, verbose: bool) -> dict[str, list[str]]:
    """回傳 {page_key: [asset ids]}，並在命名不符規則時丟出 BuildError。"""
    per_page: dict[str, list[str]] = {}
    problems: list[str] = []
    for name in sorted(files):
        found: list = []
        collect_media(files[name], name, found)
        per_page[name] = [m["id"] for _, m in found]
        for where, m in found:
            problems.extend(check_media_object(f"[{lang}] {where}", m))
            target = ROOT / m["file"]
            if verbose and not target.exists():
                print(f"    · 尚未產出：{m['file']}（{m['id']}，頁面會顯示佔位框）")
    if problems:
        raise BuildError("資產命名不符對應規則：\n    " + "\n    ".join(problems))
    return per_page


def asset_cap(rel: str) -> float:
    """該檔案適用的大小上限（bytes）。"""
    return MAX_VIDEO_BYTES if rel.lower().endswith((".mp4", ".webm")) else MAX_ASSET_BYTES


def asset_inventory() -> set[str]:
    """assets/ 的四個子目錄裡實際存在的檔案（相對 repo 根、posix、大小寫如同磁碟）。

    用集合比對而不是 Path.exists()：Windows 的檔案系統不分大小寫，GitHub Pages 分，
    因此 exists() 會放行只有大小寫不符的路徑，上線才 404。
    """
    found: set[str] = set()
    for sub in ASSET_SUBDIRS:
        source = ASSET_DIR / sub
        if not source.is_dir():
            continue
        for path in source.rglob("*"):
            if path.is_file():
                found.add(path.relative_to(ROOT).as_posix())
    return found


def check_assets_present(contents: dict, allow_missing: bool) -> None:
    """被參照的媒體、SHELL_ASSETS 與所有 css／js 必須存在且未超過大小上限。

    預設是硬性條件：缺檔在頁面上只顯示佔位框，在 tools/check_links.py 又被當成
    「尚未產出」放行，於是一次未轉檔的素材投放可以三道 CI 全綠地把破圖推上線。
    開發時要看佔位框請加 --allow-missing-media —— CI 永遠不會傳這個旗標。
    """
    on_disk = asset_inventory()
    by_lower = {rel.lower(): rel for rel in on_disk}
    required = sorted(referenced_media(contents) | SHELL_ASSETS)

    lines: list[str] = []
    missing = 0
    oversize = 0
    for rel in required:
        if rel not in on_disk:
            missing += 1
            actual = by_lower.get(rel.lower())
            if actual:
                lines.append(f"{rel}：磁碟上是「{actual}」— 大小寫不符（GitHub Pages 區分大小寫）")
            else:
                lines.append(f"{rel}：檔案不存在")
    # css／js 不會被 content JSON 參照，但少一個或過大同樣會讓頁面壞掉。
    for rel in sorted(set(required) | {r for r in on_disk if r.startswith(("assets/css/", "assets/js/"))}):
        if rel not in on_disk:
            continue
        size = (ROOT / rel).stat().st_size
        cap = asset_cap(rel)
        if size > cap:
            oversize += 1
            lines.append(f"{rel}：{size:,} bytes（{size / 1024 / 1024:.2f}MB）"
                         f"超過上限 {int(cap):,} bytes（{cap / 1024 / 1024:.1f}MB）"
                         f"— 這是尚未轉檔的原始檔")

    if not lines:
        return
    head = f"資產檢查未通過：缺少 {missing} 個、超過大小上限 {oversize} 個"
    if allow_missing:
        print(f"  ! {head}（--allow-missing-media 已開啟，頁面會顯示佔位框）：")
        for line in lines:
            print(f"      {line}")
        return
    raise BuildError(
        head + "\n    " + "\n    ".join(lines)
        + "\n    請執行 python tools/optimize_media.py 產出交付檔。"
          "開發時要暫時放行，請加 --allow-missing-media（CI 不會、也不該傳入這個旗標）。"
    )


# ===========================================================================
# 產出
# ===========================================================================

def site_root_path(base_url: str) -> str:
    """從 base_url 取出站台根路徑（結尾一定有 /）。

    https://acme.github.io/bettergroup  →  /bettergroup/
    https://www.bettertechgroup.com     →  /
    給 dist/404.html 用：GitHub Pages 的 404 會被套用到任何深度的網址，
    相對連結會跟著錯，所以要有一個可靠的站台根路徑。
    """
    path = urlparse(base_url).path.strip("/")
    return f"/{path}/" if path else "/"


def custom_domain(base_url: str) -> str:
    """base_url 指向自訂網域時回傳主機名，指向 *.github.io 時回傳空字串。"""
    host = (urlparse(base_url).hostname or "").lower()
    if not host or host.endswith(".github.io") or host in ("localhost", "127.0.0.1"):
        return ""
    return host


def validate_base_url(raw: str, source: str) -> str:
    """驗證並正規化網站網址；不合格就丟 BuildError，訊息一定指名來源（SITE_URL／--base-url）。

    只接受 http(s) + 合法主機名，拒絕 query／fragment／使用者資訊／空白／結尾雜訊，
    並把結尾多餘的 "/" 正規化掉。要寫出 CNAME（自訂網域）時路徑必須為空、不可帶 port ——
    否則 dist/CNAME 會把 GitHub Pages 的自訂網域綁到別人家的主機上。
    """
    def bad(why: str) -> BuildError:
        return BuildError(f"{source} 不是合法的網站網址（{raw!r}）：{why}")

    if not raw:
        raise bad("值是空的")
    if any(ch.isspace() for ch in raw):
        raise bad("含有空白字元")

    split = urlsplit(raw)
    scheme = split.scheme.lower()
    if scheme not in ("http", "https"):
        raise bad("scheme 必須是 http 或 https（要連 https:// 一起寫）")
    if split.query:
        raise bad(f"不可帶 query 字串（?{split.query}）")
    if split.fragment:
        raise bad(f"不可帶 fragment（#{split.fragment}）")
    if "@" in split.netloc:
        raise bad("不可帶使用者資訊（user:pass@host）")
    try:
        port = split.port
    except ValueError:
        raise bad("port 不是合法的數字") from None
    host = (split.hostname or "")
    if not host or not HOSTNAME_RE.match(host):
        raise bad(f"主機名不合法（{host!r}）")

    path = split.path.rstrip("/")
    if path:
        if not path.startswith("/"):
            raise bad(f"路徑必須以 / 開頭（{split.path!r}）")
        if "//" in path or any(ch in path for ch in "\\;"):
            raise bad(f"路徑含有多餘的字元（{split.path!r}）")

    netloc = f"{host}:{port}" if port else host
    normalised = f"{scheme}://{netloc}{path}"
    if custom_domain(normalised):
        # 自訂網域 → build() 會寫 dist/CNAME，而 CNAME 只能是主機名。
        if path:
            raise bad(f"自訂網域會寫出 dist/CNAME，網址不可帶路徑（{path}）")
        if port:
            raise bad("自訂網域會寫出 dist/CNAME，網址不可帶 port")
    return normalised


def font_families(lang: dict) -> str:
    if lang["font_family"]:
        return f"{BASE_FONT_FAMILY}&family={lang['font_family']}"
    return BASE_FONT_FAMILY


def page_plan(contents: dict[str, dict]) -> list[tuple]:
    """回傳實際可產出的 (key, template, output, priority)。"""
    plan = []
    for key, template, output, priority in PAGES:
        if not (TEMPLATE_DIR / template).is_file():
            continue
        if not any(key in files for files in contents.values()):
            continue
        plan.append((key, template, output, priority))
    return plan


def referenced_media(contents: dict) -> set[str]:
    """所有語言的 content JSON 參照到的媒體路徑（file 與 poster），相對 repo 根目錄。"""
    used: set[str] = set()
    for files in contents.values():
        for name in files:
            found: list = []
            collect_media(files[name], name, found)
            for _, m in found:
                used.add(m["file"])
                if m.get("poster"):
                    used.add(m["poster"])
    return used


def copy_assets(contents: dict) -> tuple[int, int, int]:
    """複製 assets/ 到 dist/assets/。

    略過三種檔案：超過大小上限的（影片超過 MAX_VIDEO_BYTES，其餘超過 MAX_ASSET_BYTES；
    ＝尚未轉檔的原始檔）、以及 img/ 與 video/ 裡沒有任何 content JSON 參照、也不在
    SHELL_ASSETS 白名單裡的檔案（沒有任何頁面指得到它們，複製過去只是死重量）。
    """
    target_root = DIST_DIR / "assets"
    used = referenced_media(contents)
    copied = skipped = unused = 0
    for stray in sorted(ASSET_DIR.glob("*")):
        if stray.is_file():
            print(f"  ! assets/ 底下的散檔不會進 dist/（請放進 {'/'.join(ASSET_SUBDIRS)}）："
                  f"{stray.relative_to(ROOT)}")
    for sub in ASSET_SUBDIRS:
        source = ASSET_DIR / sub
        if not source.is_dir():
            continue
        for path in sorted(source.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT).as_posix()
            if sub in ("img", "video") and rel not in used and rel not in SHELL_ASSETS:
                print(f"  ! 沒有任何頁面參照，不複製到 dist/：{rel}")
                unused += 1
                continue
            cap = MAX_VIDEO_BYTES if path.suffix.lower() in (".mp4", ".webm") else MAX_ASSET_BYTES
            if path.stat().st_size > cap:
                print(f"  ! 略過過大的檔案（{path.stat().st_size / 1024 / 1024:.1f}MB > "
                      f"{cap / 1024 / 1024:.1f}MB）：{path.relative_to(ROOT)}")
                print(f"    這是尚未轉檔的原始檔，頁面上會顯示佔位框。請執行："
                      f"python tools/optimize_media.py")
                skipped += 1
                continue
            target = target_root / path.relative_to(ASSET_DIR)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            copied += 1
    return copied, skipped, unused


# 模板裡的中文段落註解只給維護者看，不必出現在交付的 HTML（英文版尤其不該露出中文
# 建置備註）。<script>／<style>／IE 條件註解不動。
_SKIP_BLOCK_RE = re.compile(r"(?is)<(script|style)\b[^>]*>.*?</\1\s*>")
_HTML_COMMENT_RE = re.compile(r"[ \t]*<!--(?!\[if)[\s\S]*?-->[ \t]*\n?")


def strip_html_comments(html: str) -> str:
    out: list[str] = []
    pos = 0
    for m in _SKIP_BLOCK_RE.finditer(html):
        out.append(_HTML_COMMENT_RE.sub("", html[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(_HTML_COMMENT_RE.sub("", html[pos:]))
    return "".join(out)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def build(langs: list[dict], base_url: str, verbose: bool, allow_missing: bool) -> None:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=True,
        undefined=StrictUndefined,
        trim_blocks=False,
        lstrip_blocks=False,
        keep_trailing_newline=True,
    )

    all_langs = available_langs()
    contents = {l["code"]: load_content(l["code"]) for l in all_langs}
    validate_translations(contents)
    print(f"翻譯結構檢查通過（基準：{REFERENCE_LANG}；語言：{', '.join(contents)}）")

    asset_report = {}
    for l in all_langs:
        asset_report[l["code"]] = validate_assets(contents[l["code"]], l["code"], verbose)
    check_assets_present(contents, allow_missing)
    print("資產 ID 與路徑對應檢查通過")

    plan = page_plan(contents)
    skipped_pages = [k for k, *_ in PAGES if k not in {p[0] for p in plan}]

    # 供 hreflang / 語言切換器使用的完整語言清單（不受 --lang 影響）
    lang_list = [{"code": l["code"], "hreflang": l["hreflang"],
                  "html_lang": l["html_lang"]} for l in all_langs]

    rendered = 0
    for l in langs:
        code = l["code"]
        files = contents[code]
        for key, template_name, output, _ in plan:
            if key not in files:
                continue
            template = env.get_template(template_name)
            html = template.render(
                lang=code,
                lang_latin=l["latin"],
                html_lang=l["html_lang"],
                hreflang=l["hreflang"],
                langs=lang_list,
                x_default=X_DEFAULT,
                base_url=base_url.rstrip("/") + "/",
                font_families=font_families(l),
                asset_prefix="../",
                page_key=key,
                page_output=output,
                page=files[key],
                common=files["common"],
            )
            write(DIST_DIR / code / output, strip_html_comments(html))
            rendered += 1

    # 語言分流閘道、sitemap、robots — 一律以「全部語言」為準
    gateway = env.get_template("gateway.html").render(
        langs=[{**l, "name": contents[l["code"]]["common"]["languages"][l["code"]]["name"],
                "label": contents[l["code"]]["common"]["languages"][l["code"]]["label"],
                "shell": contents[l["code"]]["common"]["shell"],
                "title": contents[l["code"]]["common"]["site"]["legal_name"]}
               for l in all_langs],
        x_default=X_DEFAULT,
        x_default_html_lang=next(l["html_lang"] for l in all_langs
                                 if l["code"] == X_DEFAULT),
        base_url=base_url.rstrip("/") + "/",
        site_name=contents[REFERENCE_LANG]["common"]["site"]["legal_name"],
        site_name_en=contents[REFERENCE_LANG]["common"]["site"]["legal_name_en"],
    )
    write(DIST_DIR / "index.html", strip_html_comments(gateway))

    sitemap = env.get_template("sitemap.xml").render(
        langs=lang_list, pages=plan, x_default=X_DEFAULT,
        base_url=base_url.rstrip("/") + "/",
        contents=contents,
    )
    write(DIST_DIR / "sitemap.xml", sitemap)

    robots = env.get_template("robots.txt").render(
        base_url=base_url.rstrip("/") + "/",
    )
    write(DIST_DIR / "robots.txt", robots)

    not_found = env.get_template("404.html").render(
        langs=[{**l, "name": contents[l["code"]]["common"]["languages"][l["code"]]["name"],
                "shell": contents[l["code"]]["common"]["shell"]}
               for l in all_langs],
        shell_ref=contents[REFERENCE_LANG]["common"]["shell"],
        x_default=X_DEFAULT,
        x_default_html_lang=next(l["html_lang"] for l in all_langs
                                 if l["code"] == X_DEFAULT),
        base_path=site_root_path(base_url),
        site_name=contents[REFERENCE_LANG]["common"]["site"]["legal_name"],
        site_name_en=contents[REFERENCE_LANG]["common"]["site"]["legal_name_en"],
    )
    write(DIST_DIR / "404.html", strip_html_comments(not_found))

    # GitHub Pages 預設會用 Jekyll 處理輸出，會吃掉底線開頭的檔案與目錄。
    # .nojekyll 讓它原樣發佈；寫在這裡才能在 --clean 之後存活。
    write(DIST_DIR / ".nojekyll", "")

    # 自訂網域時輸出 CNAME，GitHub Pages 會據此設定網域。
    domain = custom_domain(base_url)
    if domain:
        write(DIST_DIR / "CNAME", f"{domain}\n")

    copied, skipped_assets, unused_assets = copy_assets(contents)
    if skipped_assets and not allow_missing:
        raise BuildError(
            f"有 {skipped_assets} 個資產超過大小上限被略過（見上方清單）——"
            "略過即代表頁面上是佔位框，不得發佈。"
            "請執行 python tools/optimize_media.py，或加 --allow-missing-media 暫時放行。"
        )

    print()
    print("─" * 62)
    print(f"  輸出目錄     dist/")
    print(f"  語言         {', '.join(l['code'] for l in langs)}"
          f"{'' if len(langs) == len(all_langs) else '（已用 --lang 過濾）'}")
    print(f"  頁面／語言   {len(plan)}（{', '.join(p[0] for p in plan)}）")
    if skipped_pages:
        print(f"  尚未實作     {', '.join(skipped_pages)}")
    print(f"  HTML 檔      {rendered}")
    print(f"  資產         複製 {copied} 個檔案"
          f"{f'，略過 {skipped_assets} 個過大檔案' if skipped_assets else ''}"
          f"{f'，略過 {unused_assets} 個無人參照的檔案' if unused_assets else ''}")
    print(f"  其他         index.html（語言閘道）、404.html、sitemap.xml、robots.txt、.nojekyll"
          f"{('、CNAME（' + domain + '）') if domain else ''}")
    print(f"  網站網址     {base_url.rstrip('/')}（站台根路徑 {site_root_path(base_url)}）")
    print("─" * 62)
    ids = sorted({i for pages in asset_report[REFERENCE_LANG].values() for i in pages})
    if ids:
        print(f"  使用中的資產 ID（{len(ids)}）：{', '.join(ids)}")
    print(f"  預覽：python -m http.server -d dist 8000")


def main() -> int:
    # Windows 主控台預設為 cp950，直接輸出繁中會出現亂碼。
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="倍特爾官網靜態產生器")
    parser.add_argument("--clean", action="store_true", help="產出前先刪除 dist/")
    parser.add_argument("--lang", action="append", default=None,
                        help="只產出指定語言（可重複，或以逗號分隔）")
    env_site_url = (os.environ.get("SITE_URL") or "").strip()
    parser.add_argument("--base-url", default=None,
                        help="canonical / hreflang / sitemap / CNAME 用的網站網址"
                             f"（未指定時取環境變數 SITE_URL，再無則用預設 {SITE_URL}）")
    parser.add_argument("--validate-only", action="store_true",
                        help="只檢查內容結構與資產命名，不寫出任何檔案")
    parser.add_argument("--allow-missing-media", action="store_true",
                        help="開發用：被參照的媒體缺檔或超過大小上限時只警告不失敗"
                             "（頁面顯示佔位框）。CI 永遠不傳這個旗標。")
    parser.add_argument("--quiet", action="store_true", help="不列出尚未產出的媒體檔")
    args = parser.parse_args()

    if args.base_url is not None:
        raw_url, url_source = args.base_url, "--base-url"
    elif env_site_url:
        raw_url, url_source = env_site_url, "環境變數 SITE_URL"
    else:
        raw_url, url_source = SITE_URL, "build.py 的 SITE_URL 常數"

    try:
        base_url = validate_base_url(raw_url, url_source)
        # 沒帶 --lang 就代表要產出全站，四個語言目錄一個都不能少。
        if not args.lang:
            check_language_dirs()
    except BuildError as exc:
        print(f"\n建置失敗：{exc}", file=sys.stderr)
        return 1

    all_langs = available_langs()
    if not all_langs:
        print("content/ 下找不到任何語言目錄。", file=sys.stderr)
        return 1

    selected = all_langs
    if args.lang:
        wanted = {c.strip() for item in args.lang for c in item.split(",") if c.strip()}
        unknown = wanted - {l["code"] for l in all_langs}
        if unknown:
            print(f"未知或尚未建立的語言：{', '.join(sorted(unknown))}", file=sys.stderr)
            return 1
        selected = [l for l in all_langs if l["code"] in wanted]

    try:
        if args.validate_only:
            contents = {l["code"]: load_content(l["code"]) for l in all_langs}
            validate_translations(contents)
            for l in all_langs:
                validate_assets(contents[l["code"]], l["code"], not args.quiet)
            check_assets_present(contents, args.allow_missing_media)
            print("檢查通過。")
            return 0

        if args.clean and DIST_DIR.exists():
            shutil.rmtree(DIST_DIR)
            print("已清除 dist/")
        build(selected, base_url, not args.quiet, args.allow_missing_media)
    except BuildError as exc:
        print(f"\n建置失敗：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
