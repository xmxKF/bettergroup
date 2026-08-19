# 倍特爾科技集團有限公司 — 官方網站

**BETTER SCIENCE TECHNOLOGY GROUP CO., LIMITED**
先進半導體九大主製程設備採購、拆裝機及運送、先進製程技術導入、人才培訓，以及 AI 與先進製造設備的整合應用。

- 語言：**繁體中文（母本）／簡體中文／English／日本語** 四種，各自輸出到 `dist/<lang>/`
- 技術：Python + Jinja2 靜態產生器；輸出為純 HTML／CSS／原生 JS，**無框架、無外部 JS**（僅 Google Fonts 以 `<link>` 載入）
- 地址：香港九龍佐敦佐敦道5號至秀商業大廈10樓　｜　聯絡人：蘇益宏（Kerwin）　｜　kerwin@bettertechgroup.com

---

## 1. 檔案結構

```
bettergroup/
├── build.py                         ★ 靜態產生器（唯一的建置入口）
├── requirements.txt                 相依套件（jinja2；轉檔工具另需 pillow）
│
├── templates/                       Jinja2 模板 —— 只有「結構」，沒有任何文案
│   ├── base.html                    頁面骨架：head／header／main block／footer
│   ├── index.html                   首頁
│   ├── gateway.html                 dist/index.html 語言分流閘道
│   ├── sitemap.xml  robots.txt
│   └── partials/
│       ├── header.html  footer.html         直接 include
│       ├── lang-switcher.html                macro：語言切換器
│       ├── breadcrumb.html                   macro：麵包屑
│       ├── cta-band.html                     macro：共用聯絡條
│       └── media.html                        macro：媒體佔位、section header、各式卡片
│
├── content/                         ★ 所有文案（每個語言一個資料夾）
│   ├── zh-hant/                     繁體中文 —— 結構基準，先改這裡
│   │   ├── common.json              全站共用（header／footer／CTA／表單）
│   │   └── index.json               首頁
│   ├── zh-hans/                     簡體中文（大陸業界術語）
│   ├── en/                          English
│   └── ja/                          日本語
│
├── assets/                          css／img／js／video 四個子目錄複製到 dist/assets/
│   ├── css/style.css                全站唯一樣式表（設計 token ＋ 所有元件）
│   ├── js/main.js                   全站唯一腳本（導覽／捲動淡入／表單／媒體偵測）
│   ├── img/                         logo-96、favicon、交付用圖片
│   ├── video/                       交付用影片
│   └── src/                         轉檔前的原始檔庫（optimize_media.py 自動搬入，不進 dist/）
│
├── tools/
│   ├── optimize_media.py            ★ 把原始媒體檔轉成交付檔（比例／尺寸／壓縮）
│   ├── check_parity.py              產出 HTML 與 docs/content-schema.md／templates/ 規格的結構檢查
│   └── check_links.py               dist/ 內部連結檢查（無相依套件；CI 會跑）
│
├── .github/workflows/deploy.yml     推到 main → 建置 → 發佈到 GitHub Pages（見 §8）
│
├── dist/                            ← 產出目錄（不要手動編輯，也不要進版控）
│   ├── index.html                   語言分流閘道
│   ├── 404.html                     找不到頁面（四語連結 ＋ 回到閘道的連結）
│   ├── zh-hant/ zh-hans/ en/ ja/    每個語言一份完整網站
│   ├── assets/  sitemap.xml  robots.txt
│   ├── .nojekyll                    GitHub Pages 不要跑 Jekyll
│   └── CNAME                        僅在 SITE_URL 是自訂網域時輸出
│
├── DESIGN.md                        ★ 設計系統唯一真實來源（色彩／字體／間距／元件規範）
├── GOAL.md                          客戶原始需求（不得修改）
├── logo.png                         原始 logo（2048px，不得修改；過大，不會複製到 dist）
│
├── docs/
│   ├── content-spec.md              ★ 全站文案唯一真實來源（繁體中文母本）
│   ├── content-schema.md            ★ 多語 JSON 欄位規格（翻譯者與模板作者必讀）
│   ├── components.md                ★ 元件 HTML 片段庫
│   ├── image-prompts.md             圖片生成提示詞（依資產 ID）
│   └── video-prompts.md             影片生成提示詞（依資產 ID）
│
└── templates/                       ★ Jinja2 模板（頁面標記的唯一真實來源，取代第一階段原型）
    ├── base.html                    共用外殼（head／header／footer／語言切換器）
    ├── index.html / about.html / services.html / equipment.html / ai.html
    │   contact.html / equipment-detail.html / gateway.html / 404.html
    │                                各頁模板（equipment-detail.html 供 9 個製程子頁共用）
    └── partials/                    可重用片段（breadcrumb／cta-band／footer／header／lang-switcher／media）
```

★ = 動工前必讀。

---

## 2. 建置與預覽

```bash
pip install -r requirements.txt      # jinja2（tools/optimize_media.py 另需 pillow）
python build.py                      # 產出 dist/
python -m http.server -d dist 8000   # 預覽 → http://localhost:8000/
```

`build.py` 的旗標：

| 旗標 | 作用 |
|---|---|
| （無） | 產出所有語言 |
| `--clean` | 先刪除 `dist/` 再產出 |
| `--lang zh-hant` | 只產出指定語言（可重複，或以逗號分隔） |
| `--validate-only` | 只檢查翻譯結構與資產命名，不寫出任何檔案 |
| `--base-url https://…` | 覆寫 canonical／hreflang／sitemap／CNAME 用的網址 |
| `--quiet` | 不列出「尚未產出的媒體檔」清單 |

網站網址的優先順序：`--base-url` ＞ 環境變數 `SITE_URL` ＞ `build.py` 裡的 `SITE_URL` 常數。
CI 走環境變數（見 §8），本機臨時試某個網址用旗標即可：

```bash
SITE_URL=https://acme.github.io/bettergroup python build.py --clean
```

產出的頁面在 `file://` 下直接開啟也能正常運作（連結全部是相對路徑，沒有任何 `/assets/…`
這種 root-absolute 路徑），因此部署到網站根目錄或 `/<repo>/` 子路徑都一樣能動。
`python tools/check_links.py` 會掃過 `dist/` 把這件事驗證一次
（尚未產出的 `assets/img`／`assets/video` 媒體只列出來，不算錯誤）。
仍建議用 HTTP 伺服器預覽，行為才與正式主機一致。

---

## 3. 四語言是怎麼運作的

### 3.1 網址

```
/                       語言分流閘道（JS 依 navigator.languages 導向；無 JS 不轉頁，改用頁面上的四個語言連結）
/zh-hant/index.html     繁體中文（x-default）
/zh-hans/index.html     簡體中文
/en/index.html          English
/ja/index.html          日本語
```

分流規則：`zh-TW`／`zh-HK`／`zh-MO`／`zh-Hant` → `zh-hant`；其餘 `zh*`（含 `zh`／`zh-CN`／`zh-SG`／`zh-Hans`）→ `zh-hans`；`ja*` → `ja`；`en*` → `en`；有語言偏好但都不符 → `en`；完全讀不到偏好 → `zh-hant`。閘道同時輸出四個純連結，供無 JS 的使用者與爬蟲使用；
閘道與 404 頁都**沒有** `meta refresh`（非零延遲的自動轉頁違反 WCAG 2.2.1，見 `DESIGN.md §11`）。

每頁 `<head>` 都有四個語言的 `hreflang` alternate ＋ `x-default`（指向 zh-hant）＋ `canonical`；
`sitemap.xml` 也帶完整 alternates。

### 3.2 字體與 `lang`

| 語言 | `<html lang>` | Google Fonts |
|---|---|---|
| zh-hant | `zh-Hant-HK` | Inter ＋ Noto Sans TC |
| zh-hans | `zh-Hans-CN` | Inter ＋ Noto Sans SC |
| en | `en` | Inter（不載入 CJK） |
| ja | `ja` | Inter ＋ Noto Sans JP |

`--font-cjk` 由 `style.css` 的 `html[lang^=...]` 選擇器切換；英文版內文行高改為 1.6。
詳見 `DESIGN.md §4`。

### 3.3 語言切換器

Header（桌機）與漢堡選單（行動）各有一組 `繁 / 简 / EN / 日`，連往**其他語言的同一頁**。
視覺規範見 `DESIGN.md §6.1b`，HTML 片段見 `docs/components.md §0`。

---

## 4. 新增一個語言

1. 在 `build.py` 的 `LANGS` 表加一列：`code`、`html_lang`（`<html lang>` 值）、
   `hreflang`、`latin`（以詞為單位、詞間需要空格的語言設 `True`，CJK 設 `False`；
   首頁 H1 的換行處會據此決定要不要補空白）、
   `font_family`（該語言要追加的 Google Fonts family，純拉丁語系留空字串）。
2. 若該語言需要不同的 CJK 字體堆疊，在 `assets/css/style.css` 的
   「語言字體切換」區塊加一條 `html[lang^="…"]{ --font-cjk: … }`。
3. 建立 `content/<code>/`，把 `content/zh-hant/` 的所有 `.json` 複製過去後翻譯
   —— **鍵名與陣列長度不可改**，只改值。語言閘道與 404 頁的文案也在裡面
   （`common.json` 的 `shell` 物件），一併翻譯即可，不必動模板。
4. 在四個語言的 `common.json` 的 `languages` 物件各加一筆
   `{ "label": "…", "name": "…" }`（`label` 是切換器上的短標籤，四語共用；`name` 各語言自譯）。
5. `python build.py --validate-only` 通過後再 `python build.py`。

沒有建立 `content/<code>/` 的語言不會被產出，也不會出現在切換器與 sitemap 裡。

---

## 5. 翻譯是怎麼驗證的

`build.py` 在寫出任何檔案前會做兩層檢查，任何一項不過就中止建置：

1. **結構一致性** —— 每個語言的每個 JSON，其巢狀鍵集合與陣列長度必須與 `zh-hant` 完全相同。
   不符時印出**第一個**不符的完整路徑：

   ```
   建置失敗：[ja] 結構與 zh-hant 不符 → index.stats.entries：list 長度不同（zh-hant=3，ja=2）— 各語言必須逐項對應
   ```

2. **語言不變欄位** —— `id`／`file`／`poster`／`ratio`／`href`／`match`／`brands`／`en`／
   `title_lat`／`num`／`email` 等，以及語言切換器標籤 `common.languages.*.label`
   （`繁`／`简`／`EN`／`日`）必須逐字沿用 `zh-hant`。不符時一次列出全部：

   ```
   建置失敗：[en] 以下欄位為語言不變欄位，必須逐字沿用 zh-hant：
       common.nav.entries[1].href：zh-hant='about.html' 但 en='about-us.html'
   ```

3. **資產命名** —— 每個媒體物件的 `id` 與 `file`／`poster` 必須符合 §6 的對應規則；
   建置摘要會列出該語言用到的所有資產 ID，以及尚未產出的檔案。

欄位名稱與各語言的專屬規則（公司名、地址、標點、簡體術語對照）見 **`docs/content-schema.md`**。

---

## 6. 放入生成的圖片與影片

網站已為 49 個媒體位置預留佔位框。放圖只有三步，**不需要改任何 HTML 或 JSON**：

```bash
# 1. 把檔案放進 assets/img/，檔名用資產 ID 推導出的名字（副檔名、尺寸、比例都不拘）
#    例：assets/img/eqp-03.png、assets/img/litho-01.png
# 2. 轉成交付檔（可先加 --dry-run 看會做什麼）
python tools/optimize_media.py
# 3. 重新建置
python build.py
```

### 命名規則

| 資產 ID | 檔案路徑 |
|---|---|
| `IMG-<PAGE>-<NN>` | `assets/img/<page 小寫>-<nn>.jpg` |
| `VID-<PAGE>-<NN>` | `assets/video/<page 小寫>-<nn>.mp4` |
| 影片海報 | `assets/img/<page 小寫>-<nn>-poster.jpg` |

PAGE 代碼：`HOME, ABOUT, SVC, EQP, LITHO, ETCH, CVD, BAKE, IMP, CMP, CLEAN, INSP, MASK, AI, CONTACT`

範例：

```
IMG-HOME-01   →  assets/img/home-01.jpg
IMG-LITHO-03  →  assets/img/litho-03.jpg
VID-HOME-01   →  assets/video/home-01.mp4  ＋  assets/img/home-01-poster.jpg
VID-AI-01     →  assets/video/ai-01.mp4    ＋  assets/img/ai-01-poster.jpg
```

完整清單見 `docs/content-spec.md` §16（資產索引，含每個版位的比例）。`build.py` 會驗證 JSON 裡的路徑符合本規則。

### `tools/optimize_media.py` — 轉檔工具

| 旗標 | 作用 |
|---|---|
| （無） | 掃描 `assets/img/`（及誤放在 `assets/video/` 的海報圖）與 `assets/video/`，把還不是交付形態的檔案轉檔 |
| `--dry-run` | 只列出會做什麼，不動任何檔案 |
| `--verbose` | 連「已合規／受保護／未對應」的檔案也列進表格 |

轉檔規則（圖片）：

| 項目 | 規則 |
|---|---|
| 比例 | 取自 `content/zh-hant/*.json` 各媒體物件的 `ratio`（**唯一真實來源**）。照片置中裁切；平底技術圖形改以邊緣色延伸畫布，不裁切（沿四邊取樣自動判定） |
| 長邊 | 海報與頁首主視覺（`hero`／`banner_media`）1920，其餘 1600；一律不放大 |
| 編碼 | JPEG、progressive、sRGB，品質 82；超過 400 KB 就逐級降到 70 |
| 檔名 | 一律輸出小寫 `.jpg` |
| 原始檔 | 移到 `assets/src/`（保留原檔名與副檔名），**不會進 `dist/`**，也不會被刪除 |
| 不處理 | `logo*`／`favicon*`；以及已符合上述全部條件的檔案 |

轉檔規則（影片，`content/zh-hant/*.json` 有對應 `VID-` 資產 ID 的 `.mp4` 才會處理）：

| 項目 | 規則 |
|---|---|
| 觸發條件 | 寬度超過 1920px，或檔案超過交付預算 3MB |
| 尺寸 | 等比縮到寬度 ≤ 1920（高度自動取偶數），已符合則不放大 |
| 編碼 | H.264（`libx264`，`-preset slow`）、`yuv420p`、無音軌（`-an`）、`+faststart`；crf 28 起，轉完仍超過 3MB 就用 crf 31 重試一次 |
| 原始檔 | 移到 `assets/src/`（同名已存在時保留較新的一份，較舊的一份加數字後綴） |
| 依賴 | 需要 `ffmpeg`／`ffprobe` 在 PATH 上；找不到時清楚提示並略過所有影片，圖片轉檔不受影響 |

工具是**冪等**的：已轉好的檔案再跑一次會顯示「沒有需要處理的檔案」。

### 生成端建議規格（給生圖／生影片工具）

| 用途 | 比例 | 建議生成尺寸 | 格式 |
|---|---|---|---|
| Hero／寬幅 | 16:9 | 2400×1350 以上 | 任意（轉檔工具會處理） |
| 卡片／段落 | 4:3 | 1600×1200 以上 | 任意 |
| 直式 | 3:4 | 1200×1600 以上 | 任意 |
| 地圖／寬帶 | 21:9 | 2520×1080 以上 | 任意 |
| 影片 | 16:9 | 1920×1080 以上 | MP4、H.264；轉檔工具會處理尺寸、壓縮與移除音軌（交付預算 3MB，見下） |

影片一律靜音自動播放；有音軌也沒關係，`tools/optimize_media.py` 會自動移除。影像風格與禁忌見 `DESIGN.md` §8，逐一資產的提示詞見 `docs/image-prompts.md`／`docs/video-prompts.md`。

**只有 `assets/css`、`assets/img`、`assets/js`、`assets/video` 這四個子目錄會被複製到 `dist/`**，其中 `img`／`video` 裡沒有任何 content JSON 參照、也不在 `build.py` 的 `SHELL_ASSETS` 白名單（favicon 與 `logo-96.png`）內的檔案不會被複製（建置訊息會列出來）；超過大小上限的檔案也會被略過（圖片／`css`／`js` 上限 **1.5MB**，影片上限 **8MB**），並在建置訊息中提示改用 `python tools/optimize_media.py`。`assets/src/` 刻意不在複製清單內。直接放在 `assets/` 底下（不在這些子目錄內）的檔案不會進 `dist/`；建置時會出現警告。根目錄的 `logo.png` 在 `assets/` 之外，本來就不是複製對象。

### 檢查方式

檔案不存在時會看到灰底晶圓網格與資產 ID（例如 `IMG-HOME-01`）；放進正確檔名、跑完轉檔與建置後即顯示實圖。若仍是佔位框，多半是檔名不符對應規則，或該檔案超過大小上限被略過（圖片 1.5MB／影片 8MB，跑 `python tools/optimize_media.py`）。

---

## 7. 新增或修改頁面

1. 在 `templates/` 建立該頁模板（`{% extends "base.html" %}` ＋ `{% block main %}`），
   `<main>` 內容一律從 `docs/components.md` 複製片段，只把文字換成 `{{ ... }}`。
2. 在**每個語言**的 `content/<lang>/` 建立同名 `.json`，欄位依 `docs/content-schema.md`。
3. `build.py` 的 `PAGES` 表已列出全部 15 個頁面；只有「模板存在且該語言有對應 JSON」的頁面才會被產出，
   所以通常不需要改這張表。
4. 對照 `docs/components.md` §21 的上線前自檢逐項確認。

**紅線（不可違反）**

- 不得新增第二個 CSS／JS 檔，不得引用外部 JS 或圖示 CDN（Google Fonts 除外）。
- 不得使用任何第三方品牌 logo；不得出現「授權代理」「official distributor」「原廠指定」。
- 不得捏造成立年份、員工人數、營收、客戶名稱、案例、認證、獎項或其他辦公室。
- AI 架構與量化結果一律標示為第三方公開研究成果，作為倍特爾導入與對標之基準（四種語言皆同）。
- 品牌名稱任何語言都不翻譯；日文版不得自創片假名公司名。
- 不得修改根目錄 `logo.png`、`GOAL.md`。

---

## 8. 部署（GitHub Pages）

正式部署走 **GitHub Actions → GitHub Pages**：推到 `main` 就自動建置並發佈，
`dist/` 不進版控（見 `.gitignore`），流程定義在 `.github/workflows/deploy.yml`。

### 8.1 第一次上線

1. 在 GitHub 建立一個 repository（public 或 private 皆可；private 需要付費方案才能用 Pages）。
2. 把本機 repo 推上去：

   ```bash
   git remote add origin https://github.com/<owner>/<repo>.git
   git push -u origin main
   ```

3. **Settings → Pages → Build and deployment → Source** 選 **GitHub Actions**（不要選 “Deploy from a branch”）。
4. 回到 **Actions** 分頁看 `Deploy to GitHub Pages` 跑完；網址會顯示在該次 run 的 `deploy` 工作上。

之後每次 `git push` 到 `main` 都會自動重新發佈；也可以在 Actions 分頁按
**Run workflow** 手動觸發（`workflow_dispatch`）。

### 8.2 網站網址（`SITE_URL`）

canonical、hreflang、`sitemap.xml`、`robots.txt` 與 `404.html` 的站台根路徑都需要知道正式網址。
workflow 依這個順序決定：

| 情況 | 用到的網址 |
|---|---|
| 有設 repository variable `SITE_URL` | 該值（自訂網域走這條） |
| repo 名稱是 `<owner>.github.io` | `https://<owner>.github.io` |
| 其他 repo | `https://<owner>.github.io/<repo>`（專案頁面，站台掛在子路徑） |

專案頁面的子路徑不需要任何設定 —— 站內連結全部是相對路徑，`404.html` 的站台根路徑
也是由 `SITE_URL` 推導出來的。

### 8.3 自訂網域

1. 在 DNS 加上 GitHub Pages 的紀錄（apex 用 A／AAAA，`www` 用 CNAME 指向 `<owner>.github.io`）。
2. GitHub → **Settings → Secrets and variables → Actions → Variables → New repository variable**，
   名稱 `SITE_URL`，值填完整網址，例如 `https://www.bettertechgroup.com`。
3. 重新跑一次 workflow。`SITE_URL` 的主機不是 `*.github.io` 時，`build.py` 會自動寫出
   `dist/CNAME`，GitHub Pages 據此綁定網域，不需要另外在 Settings → Pages 手動填
   （手動填也可以，兩者一致即可）。
4. 綁定成功後在 Settings → Pages 勾選 **Enforce HTTPS**。

### 8.4 CI 會擋下什麼

workflow 在發佈前依序跑這三關，任何一關失敗就不會發佈：

```bash
python build.py --validate-only   # 四語 JSON 結構、語言不變欄位、資產命名
python tools/check_parity.py      # 產出與原型／模板規格的等價性
python tools/check_links.py       # dist/ 內部連結；root-absolute 路徑一律視為錯誤
```

本機送出前跑同樣三行，就不會被 CI 打回來。

### 8.5 其他平台

| 平台 | 做法 |
|---|---|
| Netlify | build command `python build.py`，publish directory `dist` |
| Vercel | framework 選 “Other”，build command `python build.py`，output directory `dist` |
| Cloudflare Pages | build command `python build.py`，output directory `dist` |
| 一般虛擬主機 | 本機建置後，FTP／SFTP 上傳 **`dist/` 的內容**（不是 repo 根目錄）到網站根目錄 |

### 8.6 上線後自檢

部署後請確認：

- 根網址 `/` 會依瀏覽器語言導向正確的語言版本；關閉 JS 時停在閘道頁，四個語言連結可點（不會自動轉頁）
- 四個語言各自的首頁載入無 console 錯誤，字體正確（TC／SC／JP／Inter）
- 語言切換器能在同一頁面之間互相切換
- 各頁 favicon 顯示正常（`assets/img/favicon.ico`）
- 手機寬 320px 不出現橫向捲動
- `mailto:` 連結與詢問表單能正確開啟郵件軟體
- 隨便打一個不存在的網址（例如 `/nope`、`/en/nope`）會看到 404 頁，四個語言連結可點，
  底部的「回到語言選擇」可回到語言分流閘道（**不會**自動轉頁）

GitHub Pages 已內建 HTTPS 與合理的快取；換到自架主機時建議 `assets/*` 設 1 年
`Cache-Control`，HTML 設 no-cache。

---

## 9. 文件對照

| 想知道什麼 | 看哪裡 |
|---|---|
| 顏色、字體、間距、元件的視覺規範 | `DESIGN.md` |
| 每頁每段要寫什麼字（繁中母本） | `docs/content-spec.md` |
| 多語 JSON 的欄位名稱與規則 | `docs/content-schema.md` |
| 元件的 HTML 怎麼寫 | `docs/components.md` |
| 圖片要生成什麼 | `docs/image-prompts.md` |
| 影片要生成什麼 | `docs/video-prompts.md` |
| 客戶原始需求 | `GOAL.md` |
