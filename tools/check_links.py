#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/check_links.py — dist/ 內部連結檢查（無相依套件，只用標準函式庫）。

    python build.py --clean
    python tools/check_links.py            # 檢查 dist/
    python tools/check_links.py --dist out # 檢查別的目錄

掃描 dist/ 裡所有 .html 的 href／src／srcset 與所有 .css 的 url(…)，
把相對路徑對照實際檔案解析：

  · 指不到檔案的「頁面」連結（.html、.xml、.txt、.css、.js…）→ 壞連結，結束碼 1
  · 指不到檔案的 assets/img／assets/video 媒體 → 預期中的佔位框（尚未產出的圖片／影片），
    只列出來當提醒，不算失敗（見 README §6）
  · 站外連結（http(s)://、//、mailto:、tel:、data:、javascript:）與純錨點一律略過

這是為 GitHub Pages 準備的：專案頁面會把站台掛在 /<repo>/ 子路徑底下，
任何 root-absolute 路徑（/assets/…）在那裡都會壞掉，因此本工具也會直接
把 "/" 開頭的內部連結報成錯誤。
"""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent

# 這些屬性會指向另一個檔案。
URL_ATTRS = {"href", "src", "poster", "data-rel"}
SKIP_SCHEMES = ("http://", "https://", "//", "mailto:", "tel:", "data:", "javascript:", "#")
# 尚未產出的媒體會顯示佔位框，是設計上允許的狀態。
PLACEHOLDER_DIRS = ("assets/img/", "assets/video/")
CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.found: list[tuple[str, str]] = []   # (attr, value)

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if not value:
                continue
            if name in URL_ATTRS:
                self.found.append((name, value))
            elif name == "srcset":
                for part in value.split(","):
                    candidate = part.strip().split(" ")[0]
                    if candidate:
                        self.found.append((name, candidate))


def references(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".css":
        return [("url()", m) for m in CSS_URL_RE.findall(text)]
    parser = Links()
    parser.feed(text)
    return parser.found


def is_placeholder(target: Path, dist: Path) -> bool:
    rel = target.relative_to(dist).as_posix() if target.is_relative_to(dist) else ""
    return rel.startswith(PLACEHOLDER_DIRS)


def check(dist: Path) -> int:
    files = sorted(p for p in dist.rglob("*") if p.suffix.lower() in (".html", ".css"))
    if not files:
        print(f"{dist} 裡沒有 .html／.css —— 請先執行 python build.py", file=sys.stderr)
        return 1

    broken: list[str] = []
    placeholders: set[str] = set()
    checked = 0

    for path in files:
        here = path.relative_to(dist).as_posix()
        for attr, raw in references(path):
            value = raw.strip()
            if not value or value.lower().startswith(SKIP_SCHEMES):
                continue
            split = urlsplit(value)
            if split.scheme or split.netloc:
                continue
            if not split.path:
                continue          # 純 ?query 或 #fragment
            if split.path.startswith("/"):
                broken.append(f"{here} → {value}（{attr}）：root-absolute 路徑在子路徑部署下會壞掉")
                continue
            target = (path.parent / unquote(split.path)).resolve()
            if target.is_dir():
                target = target / "index.html"
            checked += 1
            if target.exists():
                continue
            if is_placeholder(target, dist):
                placeholders.add(target.relative_to(dist).as_posix())
            else:
                broken.append(f"{here} → {value}（{attr}）：找不到檔案")

    print(f"檢查 {len(files)} 個檔案裡的 {checked} 個內部連結（根目錄 {dist}）")
    if placeholders:
        print(f"  · 尚未產出的媒體 {len(placeholders)} 個（頁面顯示佔位框，不算錯誤）：")
        for rel in sorted(placeholders):
            print(f"      {rel}")
    if broken:
        print(f"\n壞掉的連結 {len(broken)} 條：", file=sys.stderr)
        for line in broken:
            print(f"    {line}", file=sys.stderr)
        return 1
    print("內部連結全部可解析。")
    return 0


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="dist/ 內部連結檢查")
    parser.add_argument("--dist", default=str(ROOT / "dist"), help="要檢查的目錄（預設 dist/）")
    args = parser.parse_args(argv)
    dist = Path(args.dist).resolve()
    if not dist.is_dir():
        print(f"找不到目錄：{dist}", file=sys.stderr)
        return 1
    return check(dist)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
