#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/test_build_guards.py — build.py 建置護欄的回歸測試（只用標準函式庫 + build.py 本身）。

    python tools/test_build_guards.py          # 全部跑一次，任何一項失敗就回傳 1
    python tools/test_build_guards.py -v       # 連通過的案例也印細節

每一條護欄都用「真的跑一次 build.py」來驗證，斷言結束碼與錯誤訊息，涵蓋：

  · SITE_URL／--base-url 驗證 —— scheme、主機名、query／fragment／空白／port，
    以及自訂網域（會寫出 dist/CNAME）時路徑必須為空
  · 被參照的媒體或 SHELL_ASSETS 缺檔、大小寫不符、超過大小上限 → 建置失敗；
    只有 --allow-missing-media 能放行
  · content/<lang>/ 少一個目錄（或多出 LANGS 沒有的目錄）→ 建置失敗；帶 --lang 才略過
  · 翻譯把欄位寫成 null 或空字串 → 結構驗證失敗

媒體、語言目錄與結構的案例都跑在暫存沙盒裡（build.py + content/ 的副本 + 0 byte 的
假素材），**不會動到 repo 內的任何檔案**。網址案例直接跑 repo 內的 build.py --validate-only。
"""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build as B  # noqa: E402  （需要 jinja2，見 requirements.txt）

VERBOSE = False


# ---------------------------------------------------------------------------
# 執行輔助
# ---------------------------------------------------------------------------

def run_build(root: Path, args: list[str]) -> tuple[int, str]:
    """在 root 底下跑一次 build.py，回傳 (結束碼, stdout+stderr)。"""
    env = dict(os.environ)
    env.pop("SITE_URL", None)          # 測試不受呼叫端環境影響
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, str(root / "build.py"), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
    )
    return proc.returncode, proc.stdout + proc.stderr


def sandbox_assets() -> list[str]:
    """repo 內容實際參照到的媒體 + 外殼資產。"""
    contents = {l["code"]: B.load_content(l["code"]) for l in B.available_langs()}
    return sorted(B.referenced_media(contents) | B.SHELL_ASSETS)


@contextlib.contextmanager
def sandbox():
    """建一個可安全破壞的沙盒：build.py + content/ + 0 byte 的假素材。"""
    with tempfile.TemporaryDirectory(prefix="bg-guards-") as tmp:
        root = Path(tmp)
        shutil.copy2(ROOT / "build.py", root / "build.py")
        shutil.copytree(ROOT / "content", root / "content")
        for rel in sandbox_assets():
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"")
        yield root


def patch_json(path: Path, mutate) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    mutate(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8", newline="\n")


def expect_fail(root: Path, args: list[str], needles: list[str], what: str) -> None:
    code, out = run_build(root, args)
    assert code != 0, f"{what}：預期非零結束碼，實際 0\n{out}"
    for needle in needles:
        assert needle in out, f"{what}：錯誤訊息少了「{needle}」\n{out}"
    if VERBOSE:
        print(f"      exit={code} · {out.strip().splitlines()[-1][:110]}")


def expect_pass(root: Path, args: list[str], what: str) -> None:
    code, out = run_build(root, args)
    assert code == 0, f"{what}：預期結束碼 0，實際 {code}\n{out}"


# ---------------------------------------------------------------------------
# 1. SITE_URL / --base-url 驗證（發現 4）
# ---------------------------------------------------------------------------

BAD_URLS = [
    ("",                                                  "值是空的"),
    ("www.bettertechgroup.com",                           "少了 scheme"),
    ("ftp://www.bettertechgroup.com",                     "scheme 不是 http(s)"),
    ("https://",                                          "沒有主機名"),
    ("https://www.bettertechgroup.com ",                  "結尾有空白"),
    ("https://www.better techgroup.com",                  "主機名含空白"),
    ("https://user:pw@www.bettertechgroup.com",           "帶使用者資訊"),
    ("https://-bad-.example.com",                         "主機名以 - 開頭"),
    ("https://www.bettertechgroup.com:notaport",          "port 不是數字"),
    ("https://example.com/bettergroup?preview=1",         "帶 query"),
    ("https://example.com/bettergroup#top",               "帶 fragment"),
    ("https://www.bettertechgroup.com/sub",               "自訂網域帶路徑（CNAME 會綁錯）"),
    ("https://www.bettertechgroup.com:8443",              "自訂網域帶 port"),
]

GOOD_URLS = [
    ("https://www.bettertechgroup.com",             "https://www.bettertechgroup.com"),
    ("https://www.bettertechgroup.com/",            "https://www.bettertechgroup.com"),
    ("HTTPS://WWW.BetterTechGroup.COM/",            "https://www.bettertechgroup.com"),
    ("https://robertoshiu.github.io/bettergroup",   "https://robertoshiu.github.io/bettergroup"),
    ("https://robertoshiu.github.io/bettergroup/",  "https://robertoshiu.github.io/bettergroup"),
    ("http://localhost:8000",                       "http://localhost:8000"),
]


def test_bad_base_url_fails_the_build():
    """每個壞網址都要讓 build.py 以非零結束碼失敗，訊息指名來源。"""
    for url, why in BAD_URLS:
        if VERBOSE:
            print(f"    · {why}：{url!r}")
        expect_fail(ROOT, ["--base-url", url, "--validate-only", "--quiet"],
                    ["建置失敗", "--base-url"], f"壞網址（{why}）")


def test_bad_site_url_env_fails_the_build():
    """同樣的驗證要套用在環境變數 SITE_URL 上，且訊息要指名 SITE_URL。"""
    env = dict(os.environ)
    env["SITE_URL"] = "https://example.com/bettergroup?preview=1"
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "--validate-only", "--quiet"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode != 0, f"壞 SITE_URL：預期非零結束碼\n{out}"
    assert "SITE_URL" in out, f"壞 SITE_URL：訊息沒有指名 SITE_URL\n{out}"
    if VERBOSE:
        print(f"      exit={proc.returncode} · {out.strip().splitlines()[-1][:110]}")


def test_good_base_url_is_normalised():
    """合法網址要通過，且結尾斜線與大小寫被正規化。"""
    for url, expected in GOOD_URLS:
        got = B.validate_base_url(url, "測試")
        assert got == expected, f"{url!r} 正規化成 {got!r}，預期 {expected!r}"
    expect_pass(ROOT, ["--base-url", GOOD_URLS[0][0], "--validate-only", "--quiet"],
                "合法網址")


def test_custom_domain_cname_is_host_only():
    """要寫 CNAME 的網址必須是純主機名（路徑與 port 已在上面被擋掉）。"""
    assert B.custom_domain(B.validate_base_url("https://www.bettertechgroup.com", "測試")) \
        == "www.bettertechgroup.com"
    assert B.custom_domain(
        B.validate_base_url("https://robertoshiu.github.io/bettergroup", "測試")) == ""


# ---------------------------------------------------------------------------
# 2. 媒體必須存在且未超標（發現 3）
# ---------------------------------------------------------------------------

def test_sandbox_baseline_passes():
    """沙盒本身要是綠燈，否則下面的紅燈證明不了任何事。"""
    with sandbox() as root:
        expect_pass(root, ["--validate-only", "--quiet"], "沙盒基準")


def test_missing_referenced_media_fails():
    with sandbox() as root:
        (root / "assets/img/home-01.jpg").unlink()
        expect_fail(root, ["--validate-only", "--quiet"],
                    ["assets/img/home-01.jpg", "檔案不存在"], "缺少被參照的圖片")


def test_missing_shell_asset_fails():
    with sandbox() as root:
        (root / "assets/img/xyl-logo-full.png").unlink()
        expect_fail(root, ["--validate-only", "--quiet"],
                    ["assets/img/xyl-logo-full.png", "檔案不存在"], "缺少外殼資產")


def test_case_mismatch_fails():
    """GitHub Pages 區分大小寫，Windows 不分 —— 只有大小寫不同也要擋下來。"""
    with sandbox() as root:
        victim = root / "assets/img/home-01.jpg"
        victim.rename(victim.with_name("Home-01.JPG"))
        expect_fail(root, ["--validate-only", "--quiet"],
                    ["assets/img/home-01.jpg", "大小寫不符"], "大小寫不符的素材")


def test_oversize_media_fails():
    with sandbox() as root:
        (root / "assets/img/home-01.jpg").write_bytes(b"\0" * int(B.MAX_ASSET_BYTES + 1))
        expect_fail(root, ["--validate-only", "--quiet"],
                    ["assets/img/home-01.jpg", "超過上限"], "超過大小上限的素材")


def test_allow_missing_media_flag_restores_tolerance():
    """--allow-missing-media 要讓缺檔與超標退回警告（開發用；CI 不傳）。"""
    with sandbox() as root:
        (root / "assets/img/home-01.jpg").unlink()
        (root / "assets/img/home-02.jpg").write_bytes(b"\0" * int(B.MAX_ASSET_BYTES + 1))
        code, out = run_build(root, ["--validate-only", "--quiet", "--allow-missing-media"])
        assert code == 0, f"--allow-missing-media：預期結束碼 0，實際 {code}\n{out}"
        for needle in ("assets/img/home-01.jpg", "assets/img/home-02.jpg"):
            assert needle in out, f"--allow-missing-media：清單少了 {needle}\n{out}"


# ---------------------------------------------------------------------------
# 3. 語言目錄不可靜默消失（發現 13）
# ---------------------------------------------------------------------------

def test_missing_language_dir_fails():
    with sandbox() as root:
        shutil.rmtree(root / "content/ja")
        expect_fail(root, ["--validate-only", "--quiet"],
                    ["content/ja/", "缺少語言目錄"], "少一個語言目錄")


def test_missing_language_dir_is_skippable_with_lang():
    with sandbox() as root:
        shutil.rmtree(root / "content/ja")
        expect_pass(root, ["--validate-only", "--quiet", "--lang", "zh-hant,zh-hans,en"],
                    "--lang 明確略過語言")


def test_unlisted_language_dir_fails():
    with sandbox() as root:
        (root / "content/ko").mkdir()
        expect_fail(root, ["--validate-only", "--quiet"],
                    ["ko", "LANGS"], "多出 LANGS 沒列的語言目錄")


# ---------------------------------------------------------------------------
# 4. null 與空字串不得繞過結構驗證（發現 14）
# ---------------------------------------------------------------------------

def test_null_value_fails_structure_check():
    with sandbox() as root:
        patch_json(root / "content/ja/about.json",
                   lambda d: d["meta"].__setitem__("title", None))
        expect_fail(root, ["--validate-only", "--quiet"],
                    ["about.meta.title", "型別不同"], "翻譯把欄位寫成 null")


def test_empty_string_fails_structure_check():
    with sandbox() as root:
        patch_json(root / "content/en/about.json",
                   lambda d: d["meta"].__setitem__("title", ""))
        expect_fail(root, ["--validate-only", "--quiet"],
                    ["about.meta.title", "空字串"], "翻譯把欄位留成空字串")


def test_allowlisted_empty_string_still_passes():
    """EMPTY_ALLOWED_PATTERNS 名下刻意留空的欄位不能被誤判（en 的 ai.pillars 標題）。"""
    assert any(p.fullmatch("ai.pillars.entries[0].title") for p in B.EMPTY_ALLOWED_PATTERNS)
    assert B.compare_structure("數位孿生", "", "ai.pillars.entries[0].title",
                               "zh-hant", "en") is None
    assert B.compare_structure("數位孿生", "", "about.meta.title",
                               "zh-hant", "en") is not None


# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    global VERBOSE
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    VERBOSE = "-v" in argv or "--verbose" in argv

    tests = [(name, fn) for name, fn in sorted(globals().items())
             if name.startswith("test_") and callable(fn)]
    failed: list[str] = []
    for name, fn in tests:
        print(f"  · {name}")
        try:
            fn()
        except AssertionError as exc:
            failed.append(name)
            print(f"    FAIL {name}\n{exc}", file=sys.stderr)
        except Exception as exc:                      # noqa: BLE001
            failed.append(name)
            print(f"    ERROR {name}：{type(exc).__name__}: {exc}", file=sys.stderr)

    print("─" * 62)
    if failed:
        print(f"護欄測試失敗 {len(failed)}／{len(tests)}：{', '.join(failed)}", file=sys.stderr)
        return 1
    print(f"護欄測試全部通過（{len(tests)} 項）。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
