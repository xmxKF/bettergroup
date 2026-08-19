#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/check_parity.py — 原型 HTML 與產生器輸出的等價性檢查。

第一階段的單語原型（曾放在 repo 根目錄的 *.html）是「已核准的標記與文案」，
第三階段驗收後已刪除；現在的標記唯一真實來源是 templates/，文案唯一真實
來源是 docs/content-spec.md（欄位結構見 docs/content-schema.md）。

本工具留著給還保有一份原型目錄（例如簽核歸檔、另一個分支）的人做比對用：

    python tools/check_parity.py --proto path/to/prototypes about services contact
    python tools/check_parity.py --proto path/to/prototypes   # 檢查該目錄下所有有對應原型的頁面
    python tools/check_parity.py                               # 預設看 repo 根目錄；原型已刪除時不算失敗

第三階段的模板必須產出同樣的 DOM 與同樣的可見文字，只允許第二階段已確立的差異。

比對方式：把兩份 HTML 的 <body> 攤平成同一串 token
（開始標籤 + class 集合 + href/src；以及正規化後的可見文字），再做逐行 diff。

已正規化（= 允許）的差異：
  · 整個 <head>（canonical／hreflang／favicon 與樣式表的 ../ 前綴）
  · 資產路徑的 ../ 前綴：../assets/… → assets/…
  · 語言切換器（<nav class="lang-switch">）整個子樹 —— 原型沒有
  · 所有 data-* 屬性（main.js 的多語字串來源）
  · 空白、換行、縮排、HTML 註解

其餘任何差異都會列出來，且必須為空。
"""

from __future__ import annotations

import difflib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST_LANG = "zh-hant"

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}

# 只比對這些屬性；其餘（data-*、aria-*、style、loading…）不參與比對。
KEEP_ATTRS = ("href", "src", "id", "name", "type")

# 這些子樹只存在於產生器輸出（第二階段確立），比對時整段略過。
SKIP_CLASSES = ("lang-switch",)

# .eyebrow 由 CSS 的 text-transform:uppercase 呈現，畫面完全相同，
# 因此英文大小寫不參與比對（原型中 AI INTEGRATION／AI Integration 混用，
# 母本 docs/content-spec.md 一律為大寫，JSON 已依母本統一）。
UPPERCASE_CLASSES = ("eyebrow",)


def norm_path(value: str) -> str:
    """把頁面到資產的相對前綴正規化掉。"""
    return re.sub(r"^\.\./(assets/)", r"\1", value)


class Flatten(HTMLParser):
    """把 <body> 攤平成 token 串。"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tokens: list[str] = []
        self.stack: list[str] = []
        self.in_body = False
        self.skip_depth: int | None = None
        self.upper_depth: int | None = None

    # -- helpers ----------------------------------------------------------
    def _signature(self, tag: str, attrs: list[tuple[str, str | None]]) -> str:
        a = {k: (v or "") for k, v in attrs}
        classes = sorted(a.get("class", "").split())
        parts = [tag]
        if classes:
            parts.append("." + ".".join(classes))
        for key in KEEP_ATTRS:
            if key in a:
                parts.append(f" {key}={norm_path(a[key])}")
        return "<" + "".join(parts) + ">"

    # -- parser hooks -----------------------------------------------------
    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True
            return
        if not self.in_body:
            return
        classes = dict((k, v or "") for k, v in attrs).get("class", "").split()
        if self.skip_depth is None and any(c in SKIP_CLASSES for c in classes):
            self.skip_depth = len(self.stack)
            if tag not in VOID:
                self.stack.append(tag)
            else:
                self.skip_depth = None      # 自閉合的略過標籤：只跳過自己
            return
        if tag not in VOID:
            self.stack.append(tag)
            if self.upper_depth is None and any(c in UPPERCASE_CLASSES for c in classes):
                self.upper_depth = len(self.stack) - 1
        if self.skip_depth is None:
            self.tokens.append(self._signature(tag, attrs))

    def handle_startendtag(self, tag, attrs):
        if self.in_body and self.skip_depth is None:
            self.tokens.append(self._signature(tag, attrs))

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False
            return
        if not self.in_body or tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        if self.skip_depth is not None and len(self.stack) <= self.skip_depth:
            self.skip_depth = None
        if self.upper_depth is not None and len(self.stack) <= self.upper_depth:
            self.upper_depth = None

    def handle_data(self, data):
        if not self.in_body or self.skip_depth is not None:
            return
        if self.stack and self.stack[-1] in ("script", "style"):
            return
        text = " ".join(data.split())
        if text:
            self.tokens.append(text.upper() if self.upper_depth is not None else text)


def flatten(path: Path) -> list[str]:
    parser = Flatten()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser.tokens


def check(page: str, proto_dir: Path) -> tuple[bool, str]:
    proto = proto_dir / f"{page}.html"
    built = ROOT / "dist" / DIST_LANG / f"{page}.html"
    if not proto.is_file():
        return False, f"找不到原型：{proto}"
    if not built.is_file():
        return False, f"找不到產出：{built}（先跑 python build.py）"
    a, b = flatten(proto), flatten(built)
    diff = list(difflib.unified_diff(a, b, fromfile=f"{page}.html（原型）",
                                     tofile=f"dist/{DIST_LANG}/{page}.html（產出）",
                                     lineterm="", n=2))
    return (not diff), "\n".join(diff)


def main(argv: list[str]) -> int:
    proto_dir = ROOT
    if argv and argv[0] == "--proto":
        if len(argv) < 2:
            print("--proto 需要接一個目錄路徑")
            return 1
        proto_dir = Path(argv[1])
        argv = argv[2:]

    explicit_pages = bool(argv)
    pages = argv or sorted(
        p.stem for p in proto_dir.glob("*.html")
        if not p.stem.startswith("_") and (ROOT / "dist" / DIST_LANG / p.name).is_file()
    )

    if not pages and not explicit_pages:
        print(f"（{proto_dir} 沒有原型 HTML 可比對——已刪除或從未提供，視為通過。"
              f"標記來源見 templates/，文案來源見 docs/content-spec.md。）")
        return 0

    failed = 0
    for page in pages:
        ok, detail = check(page, proto_dir)
        print(f"{'PASS' if ok else 'FAIL'}  {page}")
        if not ok:
            failed += 1
            print(detail)
            print()
    print(f"\n{len(pages) - failed}/{len(pages)} 頁與原型等價。")
    return 1 if failed else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    sys.exit(main(sys.argv[1:]))
