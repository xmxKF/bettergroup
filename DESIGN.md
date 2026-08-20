# DESIGN.md — 倍特爾科技集團 官方網站設計系統

> 本檔為唯一的視覺決策來源。所有頁面（index / about / services / equipment / ai / contact / equipment-*）
> 與 `assets/css/style.css` 必須完全遵守此處的 token 與規則。未經明確核准不得偏離。
> 語言：繁體中文（zh-Hant-HK）；英文僅用於公司英文名、品牌名、小型 section 標籤 / eyebrow。

---

## 1. 品牌本質與美學方向

**本質。** 倍特爾是連接日系前沿半導體設備與客戶產線的技術夥伴：設備採購、拆裝機與運送、先進製程技術導入、人材培訓，並在九大主製程中導入最前沿的 AI 架構。品牌氣質是「乾淨的無塵室」而非「熱鬧的展場」——精密、克制、可被工程師信任。網站的說服力來自資訊密度與版面秩序，不是視覺特效。

**方向：簡約又專業（Light-first B2B）。** 米白紙面、石墨字色、大量留白、12 欄網格、單一主色。深藍石墨色僅用於 hero 與 footer 兩條「暗帶」，形成頁面的節奏骨架。Logo 的虹彩光譜是全站唯一的強彩度元素，只以髮絲級的線、角標、hover 高光出現——它應該像晶圓在燈下的繞射，一閃即逝，而不是背景大色塊。任何一頁只要移除 logo，畫面就應該回到近乎黑白灰的專業狀態。

---

## 2. Logo 使用規範

檔案：`assets/img/logo.png`（原始）＋後續衍生 `logo-mark.png` / `logo-on-dark.png`（若產生）。**根目錄 `logo.png` 不得修改。**

| 場景 | 高度 | 備註 |
|---|---|---|
| Header（≥960px） | 36px | 垂直置中，右側接公司中文名 |
| Header（<960px） | 30px | 公司名可縮為單行或隱藏英文名 |
| Footer | 44px | 置於暗帶上 |
| Hero 內浮水印（可選，僅首頁） | 320–480px | opacity 0.06–0.10，不可蓋住文字 |
| favicon | 32 / 180px | 直接使用圓形晶圓標 |

規則：
- **淨空區**：四周至少留 logo 高度 **0.5×** 的空白，任何文字、線、邊框不得侵入。
- **深色底**：logo 本身在深藍石墨（`--dark-900`）上可直接使用，不加白色方塊底、不加外框、不加陰影。
- **禁止**：改色、去彩、加漸層濾鏡、拉伸變形（等比縮放 only）、旋轉、加陰影／描邊、放在雜亂照片上、與品牌名（NIKON/CANON/TEL…）並排成「合作夥伴牆」。
- **最小尺寸**：24px 高以下不得使用（圓內網格會糊掉）。
- Logo 是唯一可出現完整虹彩的資產；其他地方只能出現「光譜線」而非「光譜面」。

**光譜漸層（`--grad-spectral`）允許出現於：** 區塊上／下的 2–3px 分隔線、hero 底部的 1px 髮絲線、卡片 hover 時的頂部 2px 線、媒體佔位框的角標、目前頁籤（active nav）下的 2px 底線、表格 thead 下方 2px 線、CTA 帶上緣 3px 線。
**禁止出現於：** 大面積背景、按鈕填色、文字漸層（`background-clip:text`）、圖示填色、卡片整體邊框、footer 大塊、任何面積超過 **視窗寬 × 3px** 的填色區。同一畫面（一屏）內最多出現 **2 種** 光譜元素 —— 計「種類」而非「個數」，並且**不計入**兩個全站常駐的細節：目前頁籤（active nav）下的 2px 底線與 §6.3 eyebrow 前的 24px 短線。
> **例外（§6.4 AI 能力卡）：** AI 能力卡左側的 3px 直立光譜條屬同一元件的重複樣式，整組卡片格線合計以 **1 種** 計。此為唯一例外，其他任何重複元件不得比照。

---

## 3. 色彩 Tokens

```css
:root{
  /* ── 中性（Light-first） ───────────────────────────── */
  --bg:            #F6F7F8;  /* 頁面底：冷調米白 */
  --surface:       #FFFFFF;  /* 卡片 / 表面 */
  --surface-alt:   #EFF1F3;  /* 次表面：placeholder、表格斑馬、code */
  --surface-sunk:  #E7EAED;  /* 內凹 / 分隔區塊 */
  --border:        #E2E5E9;  /* 標準 1px 邊框 */
  --border-strong: #CBD1D8;  /* 表格線、輸入框 */
  --text:          #16202C;  /* 主文字（石墨）   15.3:1 on --bg */
  --text-2:        #4A5765;  /* 次文字            6.9:1 on --bg */
  --text-muted:    #626C79;  /* 弱文字／說明      5.0:1 on --bg（AA 下限，勿再淡） */

  /* ── 暗帶（hero / footer / CTA） ───────────────────── */
  --dark-900:      #101A2B;  /* 主暗帶：深藍石墨 */
  --dark-800:      #16202F;  /* 暗帶內卡片 */
  --dark-700:      #1E2A3B;  /* 暗帶內邊框 / hover */
  --on-dark:       #F2F5F8;  /* 暗帶主文字      15.9:1 */
  --on-dark-2:     #A9B6C6;  /* 暗帶次文字       8.5:1 */
  --on-dark-muted: #8F9DAE;  /* 暗帶弱文字       6.3:1（勿再淡） */

  /* ── 主色（單一 accent：晶圓深青藍） ───────────────── */
  --accent:        #0C6B8F;  /* 連結 / CTA 底色   5.97:1 on #FFF */
  --accent-hover:  #08536F;  /* hover / active    8.48:1 on #FFF */
  --accent-soft:   #EAF4F8;  /* 淡底：tag、選中列、icon 底 */
  --accent-border: #BBD9E5;  /* 淡底對應邊框 */
  --accent-on-dark:#5CC8E8;  /* 暗帶內的連結     9.03:1 on --dark-900 */

  /* ── 語意色（僅狀態提示，不做裝飾） ────────────────── */
  --success:       #1E7A4C;  /* 5.33:1 on #FFF */
  --success-soft:  #E8F3ED;
  --warn:          #8A5A0F;  /* 5.92:1 on #FFF（文字用此，不用亮橘） */
  --warn-soft:     #FBF2E3;

  /* ── 光譜漸層（自 logo 取樣） ──────────────────────── */
  --grad-spectral: linear-gradient(90deg,
      #C42B3A 0%,  #E2662B 16%, #E9B23C 30%, #C9CE55 44%,
      #56C08A 58%, #2FA9B8 72%, #4A80C8 86%, #7B4CC0 100%);
  --grad-spectral-soft: linear-gradient(90deg,
      rgba(196,43,58,.55), rgba(233,178,60,.55), rgba(86,192,138,.55),
      rgba(47,169,184,.55), rgba(123,76,192,.55));  /* 用於淡髮絲線 */

  /* ── 晶圓網格紋理（placeholder / hero 底紋） ───────── */
  --grid-line:      rgba(22,32,44,.045);    /* 亮底上 */
  --grid-line-dark: rgba(242,245,248,.055); /* 暗帶上 */
}
```

**對比度備註（WCAG）**
- 內文（`--text` / `--text-2` / `--text-muted`）在 `--bg`、`--surface`、`--surface-alt` 上皆 ≥ 4.5:1（AA）。`--text-muted` 已是下限，**不可再調淡，字級不可低於 13px**。
- 主要按鈕：白字 on `--accent` = 5.97:1（AA）；hover 態 8.48:1。
- 暗帶：`--on-dark-muted` 在 `--dark-900` 上 6.3:1；暗帶內連結一律用 `--accent-on-dark`（9.0:1），**不可**在暗底直接用 `--accent`（僅 2.9:1，禁止）。
- 光譜漸層永遠是裝飾、不承載資訊，因此不受對比度規範；但其上不得放置文字。

---

## 4. 字體 Typography

```css
--font-cjk: "Noto Sans TC","PingFang TC","Microsoft JhengHei","Heiti TC",sans-serif;
--font-lat: "Inter","Helvetica Neue",Arial;   /* 結尾不得有 sans-serif 等通用字族 */
--font-ui:  var(--font-lat), var(--font-cjk);   /* 一般文字：拉丁優先，中文 fallback */
--font-mono:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace;
```

> **`--font-lat` 結尾絕不可放 `sans-serif`／`system-ui` 等通用字族。**
> 通用字族一旦出現，瀏覽器會就地解析所有字符（含 CJK），永遠走不到後面的
> `--font-cjk`，`html[lang]` 的分語言字體切換會整組失效（Noto Sans TC/SC/JP
> 一個 subset 都不會被載入，日文與簡中頁面會用系統的繁中字形顯示）。
> 通用字族只放在 `--font-cjk` 的最後一項。
>
> 同理，單獨使用 `--font-lat` 的規則（`.lat`、`.num`、`.eyebrow`、`.brand__en`、
> `.card__meta`、`.card--process .card__en`、`.card__arch`、`.brand-chip`、
> `.brand-bar`、`.stat-row__num`、`.data-table .model`、`.footer__en`）一律寫成
> `font-family:var(--font-lat),var(--font-cjk);` — 這些元素在英／日版會裝載中文
> 法定名稱、架構名或機型名，缺了 CJK 尾巴同樣會掉回系統字體。
### 依語言切換 CJK 字體（四語版）
`--font-cjk` 由 `html[lang]` 覆寫，其餘 token 完全不變：

```css
:root                  { --font-cjk: "Noto Sans TC","PingFang TC","Microsoft JhengHei","Heiti TC",sans-serif; }
html[lang^="zh-Hans"]  { --font-cjk: "Noto Sans SC","PingFang SC","Microsoft YaHei","Heiti SC",sans-serif; }
html[lang^="ja"]       { --font-cjk: "Noto Sans JP","Hiragino Sans","Yu Gothic","Meiryo",sans-serif; }
html[lang^="en"]       { --lh-body: 1.6; }   /* 純拉丁內文不需要 CJK 的 1.8 */
```

`html lang` 值：zh-Hant → `zh-Hant-HK`、zh-Hans → `zh-Hans-CN`、en → `en`、ja → `ja`。

Google Fonts **每個語言只載入該語言需要的一種 CJK 字體**（由 `build.py` 依語言寫入）：

| 語言 | Google Fonts `family` 參數 |
|---|---|
| zh-Hant | `Inter:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;700` |
| zh-Hans | `Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700` |
| ja | `Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700` |
| en | `Inter:wght@400;500;600;700`（不載入任何 CJK 字體） |

一律 `display=swap` ＋ `preconnect`。**任何語言都不得再新增第三種字體**（Inter ＋ 該語言的 Noto Sans 為上限）。日文不另外指定襯線或明朝體。

### 型階（Desktop ≥960px｜Mobile <640px）

| Token | 用途 | Desktop　px / line-height / weight / letter-spacing | Mobile |
|---|---|---|---|
| `--fs-display` | 首頁 hero 大標 | 56 / 1.14 / 700 / -0.02em | 34 / 1.24 |
| `--fs-h1` | 內頁頁首標題 | 40 / 1.20 / 700 / -0.015em | 28 / 1.30 |
| `--fs-h2` | 區塊標題 | 30 / 1.30 / 700 / -0.01em | 23 / 1.38 |
| `--fs-h3` | 卡片標題 | 22 / 1.45 / 600 / -0.005em | 19 / 1.50 |
| `--fs-h4` | 小標 / 表格標題 | 18 / 1.55 / 600 / 0 | 17 / 1.55 |
| `--fs-lead` | 導言段 | 19 / 1.80 / 400 / 0 | 17 / 1.80 |
| `--fs-body` | 內文 | 16 / 1.80 / 400 / 0 | 16 / 1.80 |
| `--fs-small` | 註解 / 圖說 / footer | 14 / 1.75 / 400 / 0.01em | 13 / 1.75 |
| `--fs-eyebrow` | 區塊上方英文標籤 | 12 / 1.20 / 600 / 0.16em（uppercase） | 11 / 1.20 |
| `--fs-mono` | 資產 ID / 型號 | 12 / 1.20 / 500 / 0.08em | 11 / 1.20 |

### 中文（CJK）專用規則
- 中文內文行高 **1.8**（允許 1.7–1.85）；中文標題行高不得低於 **1.14**（display）／**1.30**（h2 以下）。
- **中文一律不用斜體**（`font-style:italic` 禁用於任何含中文的元素）；強調改用 `font-weight:500/700` 或 `--accent` 色。
- 中文不用 `text-transform`；字距（letter-spacing）不得超過 `0.05em`。`--fs-eyebrow` 的 0.16em 僅作用於純英文標籤。
- 中英混排：段落設 `word-break:normal; overflow-wrap:anywhere; line-break:strict;`。**不手動插入半形空格**；有支援時加 `text-spacing-trim: normal`。
- 標點使用全形「，。、：；「」（）」；括號內為英文品牌時採半形，如 `KOKUSAI ELECTRIC (KE)`。
- 數字、型號、品牌名以 `--font-lat` 呈現；表格與統計數字加 `font-variant-numeric: tabular-nums`。
- 行寬上限：標題約 **20 個中文字**；內文段落約 **38 個中文字 / 72 英文字元**（中文段落 `max-width:38em`，英文為主者 `68ch`）。
  - 例外：`--fs-small` 的單句註解／圖說（`.note`／`.table-note`／`.brand-note`／`.form__hint`）行寬上限為 **760px**（`--container-prose`），使合規註記能在桌機排成單行，不在詞中折斷；註解內的短連結加 `white-space:nowrap`。
- `text-wrap: balance` 用於 h1/h2/h3；`text-wrap: pretty` 用於 lead 與內文。

---

## 5. 間距與版面

### 間距尺標（4 / 8 基準）
```
--space-1:4   --space-2:8   --space-3:12  --space-4:16  --space-5:20
--space-6:24  --space-8:32  --space-10:40 --space-12:48 --space-16:64
--space-20:80 --space-24:96 --space-32:128        （單位 px）
```
只准使用上述值；不得出現 `13px`、`27px` 這類自由值（1px 髮絲線除外）。

### 垂直節奏
| 區塊型別 | Desktop 上下 padding | Mobile |
|---|---|---|
| 一般 section | 80px | 64px |
| 重點 section（首段、CTA） | 96px | 80px |
| 緊湊 section（麵包屑列、統計列） | 40px | 32px |
| Hero（暗帶） | 上 120 / 下 112 | 上 72 / 下 64 |
| Footer | 上 72 / 下 40 | 上 56 / 下 32 |

區塊內部間距：eyebrow→h2 = 12px；h2→lead = 16px；lead→內容 = 40px（**桌機與行動一致**）；卡片格線 gap = 24px（mobile 16px）。

### 容器與網格
```
--container:       1200px;  /* 標準 */
--container-wide:  1360px;  /* 僅 hero 底圖 / 全幅媒體 */
--container-prose:  760px;  /* 長文：about、ai 說明 */
gutter: 20px (<640) / 32px (≥640) / 40px (≥960)
grid:   12 欄, column-gap 24px, row-gap 32px
```
常用配置：卡片 3 欄（各 span 4）、圖文 2 欄（6/6）、偏心圖文（7/5）、設備列表 4 欄（span 3，僅 ≥1200）。

### 斷點
```
sm 640px    md 960px    lg 1200px
```
Mobile-first：base 單欄；≥640 兩欄；≥960 三欄＋桌面型階；≥1200 啟用 4 欄與最大容器。

### 圓角
```
--r-xs:2px  --r-sm:4px  --r-md:8px  --r-lg:12px  --r-pill:999px
```
卡片 8px、按鈕 4px、tag/pill 999px、媒體與 placeholder 4px、輸入框 4px。**不用 >12px 的大圓角**（會失去精密感）。

### 陰影（極克制）
```
--sh-sm: 0 1px 2px rgba(16,26,43,.06);
--sh-md: 0 2px 10px rgba(16,26,43,.07);
--sh-lg: 0 14px 36px rgba(16,26,43,.10);
```
卡片預設 **無陰影、只有 1px 邊框**；hover 才升到 `--sh-md`。`--sh-lg` 僅供捲動後的 sticky header 與行動選單面板。**禁止彩色陰影、禁止 inset 立體效果。**

### 邊框規則
- 一律 `1px solid var(--border)`；表格內線用 `--border-strong`。
- 分隔用 `border-top`，不用帶陰影的 `<hr>`。
- 光譜線以獨立的 2–3px 元素承載 `--grad-spectral`，不使用 `border-image`。

---

## 6. 元件視覺規範

### 6.1 Header / Nav
- Sticky `top:0`，高度 72px（<960px 為 60px）。底 `rgba(246,247,248,.86)` ＋ `backdrop-filter: blur(12px) saturate(1.2)`；不支援時 fallback 為不透明 `--bg`。
- 捲動 >8px 時加下邊框 `1px var(--border)` ＋ `--sh-sm`，同時底色提高到 `rgba(246,247,248,.94)`
  （以 class 切換，180ms）—— 頁面捲動時暗色媒體會從 header 底下通過，.86 的底在該瞬間讓導覽字浮動不定。
- 導覽順序固定：首頁 / 關於我們 / 服務項目 / 設備與製程 / AI 智慧製造 / 聯絡我們。15px / 500 / `--text-2`；hover → `--text`；current → `--text` ＋ 文字寬度的 2px `--grad-spectral` 底線。
- 右側單一 CTA 按鈕「洽詢設備」（secondary 樣式）。文案刻意與導覽第六項「聯絡我們」不同，避免同一列出現兩個相同標籤。
- <960px：漢堡選單展開為全幅面板（`--surface`，項目 18px、上下 padding 16px、逐項 1px 分隔線）。

### 6.1b 語言切換器（Language switcher）
四語版新增的唯一 header 元件。**標籤永遠是 `繁 / 简 / EN / 日`，不隨語言翻譯**；可及名稱（`.visually-hidden`）才用各語言的語言名。

- **位置**：桌機在 `.nav` 內、導覽清單與右側 CTA 按鈕之間；<960px 收進漢堡面板，放在導覽項目與底部 CTA 按鈕之間，並以 1px `--border` 上分隔線與導覽項目分開。
- **樣式**：四顆並排的方形膠囊，`min-width:30px`、`height:28px`、`padding-inline:7px`、`gap:--space-1`、圓角 `--r-sm`、12px / 600 / `--text-muted`。
  - hover：文字 `--text`、底 `--surface-alt`。
  - 目前語言：文字 `--text`、底 `--surface-sunk`、字重 700，並加 `aria-current="true"`。**不使用底線或光譜線** —— 那是導覽項目的專屬記號，避免與「目前頁面」混淆。
  - 行動版放大為 `min-width:48px`、`height:40px`、15px，並加 1px `--border` 外框（目前語言為 `--border-strong`）以符合 44px 觸控目標。
- **連結**：一律指向「其他語言的同一頁」（`../<lang>/<同檔名>`），不回首頁。
- **960–1179px**：導覽列加上切換器後會超出容器，此區間整體收緊 —— 品牌英文副標暫隱、導覽字級 14px、`.nav` 與 `.nav__list` 間距降為 `--space-4`、切換器改窄版（`min-width:26px`、`padding-inline:4px`、`gap:0`）。**≥1180px 與 <960px 的版面與核准原型完全一致。**
- 切換器**不得**做成下拉選單、不得顯示國旗、不得只顯示目前語言。

### 6.2 Hero
**暗帶版（僅 index.html）**：底 `--dark-900`；晶圓網格底紋 `repeating-linear-gradient` 32px、`--grid-line-dark`；再疊 `radial-gradient(60% 80% at 20% 0%, rgba(92,200,232,.10), transparent)`。內容左對齊、最大 720px：eyebrow（`--accent-on-dark`）→ display 標題（`--on-dark`）→ lead（`--on-dark-2`）→ 兩顆按鈕。區塊最底加 1px `--grad-spectral` 髮絲線橫貫全幅。右側可放 `IMG-HOME-01`（16:9）。
**亮帶版（所有內頁）**：底 `--surface`、下緣 1px `--grad-spectral-soft` 髮絲線（取代原本的 1px `--border`，與首頁暗帶 hero 底部的髮絲線同一語彙，見 §2 允許清單）；麵包屑 → eyebrow → h1 → lead（最大 640px）。高度較矮（上 72 / 下 56）、無網格底紋。

### 6.3 Section header
垂直堆疊：`eyebrow`（英文、`--accent`、uppercase，前可加 24px 光譜短線）→ `h2` → `lead`（`--text-2`，最大 640px）。預設左對齊；置中僅用於 CTA 帶。

### 6.4 卡片
共同：`--surface` 底、1px `--border`、`--r-md`、padding 28px（mobile 20px）、無陰影。hover：`border-color:var(--border-strong)`、`--sh-md`、`translateY(-2px)`、頂部 2px `--grad-spectral` 由左展開（`transform:scaleX(0→1)`，180ms）。整卡可點時整張為連結，標題 hover → `--accent`。
- **服務卡（services.html）**：頂部 28px 線稿圖示（`stroke:currentColor`、1.5px、色 `--accent`）→ h3 → 說明 3–4 行 → 「了解更多 →」文字連結。
- **製程卡（equipment.html ×9）**：左上 2 位數編號（`--font-mono` 12px `--text-muted`，`01`–`09`）→ h3 製程中文名 → 英文小標（`--fs-small` `--text-muted`）→ 品牌文字 chips → 底部「查看設備 →」。可於頂部加 4:3 媒體框（`IMG-EQP-0n`）。**英文版（`lang == 'en'`）不輸出英文小標**——該行與 h3 標題同語言、內容重複；其餘三語照常輸出。
- **AI 能力卡（ai.html）**：`--surface` 底、左側 3px 直立 `--grad-spectral` 條（**唯一允許的直式光譜**）；架構名稱（`--font-lat` 600）＋年份（`--text-muted`）→ 對標製程 → 一行說明。**卡上必須標示「對標／導入之前沿架構」**，不得寫成倍特爾自有成果或自有數據。

### 6.5 品牌列（純文字，無 logo）
- Chips 形式：`--surface-alt` 底、1px `--border`、`--r-pill`、padding 6px 14px、`--font-lat` 14px/500、`--text-2`、字距 0.02em。
- 或於製程頁用「品牌條」：品牌名以 `--fs-h4` 排成一列，以 `·` 分隔。
- **嚴禁使用任何品牌 logo 圖檔**（第三方商標）。品牌寫法固定：NIKON、CANON、TEL、DNS、SAMCO、TAZMO、ULVAC、NISSIN、EBARA、ACCRETECH、ADVANTEST、NUFLARE、JEOL、MATSUSHITA、**KOKUSAI ELECTRIC (KE)**、**LASERTEC**。
- 品牌列鄰近須有一行 `--fs-small` `--text-muted` 說明：所列品牌為倍特爾之銷售及維護／採購與服務範圍。**不得以任何形式暗示為原廠授權代理商。**

### 6.6 統計 / 數據列
- 3–4 格等寬，格間以 1px `--border` 直線分隔；數字 44px（mobile 30px）/700/`--font-lat`/`tabular-nums`；下方 label `--fs-small` `--text-muted`。
- **只能使用 GOAL.md 可驗證的事實**，例如「9 大主製程」「16 個日系設備品牌」「5 項核心服務」。
- **禁止捏造**：成立年份、員工人數、營收、出貨台數、客戶數、良率提升幅度、認證、獎項、案例。若無真實數字，改用「文字三欄」而不是數據列。
- AI 架構表的量化結果（如 Acc 98.39%）**只能出現在標明來源的架構表或 AI 卡片內**，並標為第三方研究之對標指標；不得放入本列。

### 6.7 CTA 帶
- 底 `--dark-900`、上緣 3px `--grad-spectral`；內容置中、最大 720px：h2（`--on-dark`）→ 一行 lead（`--on-dark-2`）→ primary 按鈕「聯絡我們」＋ on-dark ghost 連結 `better_stg@163.com`（mailto）。
- 上下 padding 96 / 64px。每頁最多一個 CTA 帶，置於 footer 之前。

### 6.8 媒體佔位（IMG-* / VID-*）— 必須全站一致
資產 ID 格式 `IMG-<PAGE>-<NN>` / `VID-<PAGE>-<NN>`；PAGE ∈ HOME, ABOUT, SVC, EQP, LITHO, ETCH, CVD, BAKE, IMP, CMP, CLEAN, INSP, MASK, AI, CONTACT。
檔案對應：`assets/img/<page小寫>-<nn>.jpg`；影片 `assets/video/<page小寫>-<nn>.mp4` ＋ poster `assets/img/<page小寫>-<nn>-poster.jpg`。

視覺：
- 容器：`--surface-alt` 底、`--r-sm`、1px `--border`、`position:relative`、固定比例（hero 16:9、卡片 4:3、直式 3:4、聯絡／地圖 21:9）。
- 底紋：雙向晶圓網格 `repeating-linear-gradient(0deg | 90deg, var(--grid-line) 0 1px, transparent 1px 24px)`。
- 角標：左上角 28×3px 的 `--grad-spectral` 短線，距邊 12px（全站統一採左上短線，不混用其他角標）。
- 標籤：置中，`--font-mono` `--fs-mono` `--text-muted`，內容為資產 ID（例 `IMG-HOME-01`）；其下一行 `--fs-small` 灰字簡述畫面（例「無塵室設備列」）。
- 行為：真實檔案存在時自動顯示——`<img>` 以 `onerror` 隱藏自身並露出 placeholder 層；`<video>` 同理（`onerror` 掛在 `<video>` 上）。placeholder 為容器內的絕對定位層，預設可見，媒體載入成功時以 class 隱藏。
- 影片檔尚未產出、但 poster 已存在時：保留 `<video>` 並顯示 poster（`main.js` 加上 `.is-poster-only`），同時隱藏播放／暫停控制；poster 亦不存在才回到 placeholder。
- **不得**在 placeholder 上加假 UI、假圖表、假數據、emoji 或裝飾插畫。

### 6.9 Footer
- 底 `--dark-900`、上緣 1px `--grad-spectral-soft` 髮絲線。四欄（≥960）／單欄堆疊（<640）：
  1. logo（44px）＋中文全名（`--on-dark` 16px）＋英文全名（`--on-dark-muted` `--fs-small` `--font-lat`）
  2. 導覽六項（`--on-dark-2`，hover `--accent-on-dark`）
  3. 聯絡：`香港九龍佐敦佐敦道5號至秀商業大廈10樓`、`better_stg@163.com`（mailto）、`+86-135-3007-1950`（tel）—— 兩個連結皆 `--accent-on-dark`。**不列聯絡人姓名**（客戶 2026-08 指示）。
  - <960px 以觸控為主：導覽／製程連結補 `padding-block:12px`，可點高度 ≥44px（§10）。
  4. 九大製程快速連結（`--fs-small`）
- 底列：上邊框 `1px solid var(--dark-700)`，內容 `© 2026 倍特爾科技集團有限公司　BETTER SCIENCE TECHNOLOGY GROUP CO., LIMITED`，`--fs-small` `--on-dark-muted`；末行為網站設計 credit（`common.footer.credit`），同一 `--fs-small` `--on-dark-muted`，`href` 有值時渲染為 `--accent-on-dark` 連結、無值（目前）則為純文字。

### 6.10 麵包屑
`--fs-small`、`--text-muted`；分隔符 `/`（`--border-strong` 色，左右 8px）；最後一項為 `--text-2` 且非連結；位於內頁 hero 上緣，與 h1 間距 16px。

### 6.11 表格（AI 架構表）
- 全寬、`--surface` 底、外框 1px `--border`、`--r-md` ＋ `overflow:hidden`；外層 `overflow-x:auto` 供窄螢幕橫捲，右緣加 24px 漸隱遮罩提示可捲動；遮罩僅在實際溢出時出現（`main.js` 比對 `scrollWidth`／`clientWidth` 後加上 `.is-scrollable`），表格未溢出時不得留下白色漸層。
- `thead`：`--surface-alt` 底、`--fs-small`/600/`--text`、下方 2px `--grad-spectral`。
- `td`：padding 14px 16px、`--fs-small`、行高 1.7、`vertical-align:top`、上邊框 1px `--border`；偶數列 `--surface-alt`。
- 數字欄 `tabular-nums`；模型名 `--font-lat` 500。
- 表格必須附 caption／說明句：此表為第三方學術與業界公開架構，係倍特爾導入與對標之依據；**名稱與年份須與 GOAL.md 完全一致**。

### 6.12 按鈕
| 型別 | 樣式 |
|---|---|
| Primary | 底 `--accent`、白字、`--r-sm`、padding 13px 26px、15px/600；hover 底 `--accent-hover` ＋ `translateY(-1px)`；active 回 `translateY(0)` |
| Secondary | 透明底、1px `--border-strong`、字 `--text`；hover 邊框 `--accent`、字 `--accent`、底 `--accent-soft` |
| Ghost | 無邊框、字 `--accent`、padding 8px 4px；hover 底 `--accent-soft` |
| On-dark primary | 底 `--accent-on-dark`、字 `--dark-900`；hover 底 `#8ADCF2` |
| On-dark secondary | 1px `rgba(242,245,248,.28)`、字 `--on-dark`；hover 邊框 `--on-dark`、底 `rgba(255,255,255,.06)` |

共同：`--r-sm`；行內圖示 16px 置於文字右側 8px；`:focus-visible` 為 2px `--accent` outline ＋ 2px offset。**不用漸層按鈕、不用陰影按鈕、中文不用全大寫或疏排。**

### 6.13 連結
內文連結：`--accent`、`text-decoration:underline`、`text-underline-offset:3px`、`text-decoration-thickness:1px`；hover → `--accent-hover` ＋ thickness 2px。導覽與卡片內連結可無底線（靠色與位置區分），但必須有明確 hover 態。箭頭連結「了解更多 →」hover 時箭頭右移 3px。

### 6.14 Tag / Pill
`--accent-soft` 底、1px `--accent-border`、`--accent` 字、12px/500、padding 4px 10px、`--r-pill`。中性版用 `--surface-alt` / `--border` / `--text-2`。**不可作為按鈕使用**（無 hover 抬升、無點擊態）。

### 6.15 手風琴（Accordion）　*（目前無頁面使用；原聯絡頁 FAQ 已於 2026-08 移除，規格保留備用）*
- 每列上邊框 1px `--border`；標題列 padding 20px 0、`--fs-h4`、右側 `+`／`−` 線稿圖示（1.5px，展開時旋轉 45°，180ms）。
- 展開內容 `--fs-body` `--text-2`，上 padding 4px、下 32px、最大 720px。
- 展開列標題色為 `--accent`，列左側加 2px `--grad-spectral` 直條（僅展開態）。
- 以 `<details>/<summary>` 或按鈕＋`aria-expanded` 實作；必須可鍵盤操作。

### 6.16 製程頁翻頁（Pager）

- 僅用於九個 `equipment-*.html`，位置固定在「適用場景」之後、CTA 帶之前。
- 兩張等寬卡片（<640px 上下堆疊）：上邊框 1px `--border`、卡片同 §6.4 規格（`--surface`、1px `--border`、`--r-md`）。
- 內容：`--fs-small` `--text-muted` 的「上一段製程／下一段製程」＋ `--fs-h4` 製程名；箭頭以 CSS `::before`／`::after` 產生，左卡靠左、右卡靠右。
- hover 與卡片一致（邊框轉 `--border-strong`、`--sh-md`、`translateY(-2px)`），製程名轉 `--accent`。
- 順序同頁尾九大製程並首尾相接（掩模版製程 → 黃光段）。

### 6.17 聯絡資訊列（Info strip）與聯絡行（Contact lines）

- **`.info-strip`（僅 contact.html §15.2）**：三筆聯絡方式（信箱／電話／地址）收成單一帶框物件 ——
  `--surface` 底、1px `--border`、`--r-md`、`overflow:hidden`，格間 1px `--border` 分隔線。
  骨架與 §6.6 統計列相同：≥960px 三等欄（分隔線為 `border-left`、padding 32px），
  以下垂直堆疊（分隔線改為 `border-top`、padding 24px 20px）。
  欄位名 `--fs-small`/600/`--text-muted`/字距 0.04em；值 `--fs-body`/500/`--text`。
  信箱與電話值套 `.contact-card__value--nowrap`（不斷行），地址套 `--keep`。
  **不用三張獨立卡片**：地址比信箱／電話長，等高卡片會在另兩張下方留下不等量空白。
- **`.contact-lines`（about 總部區塊、contact 側欄卡）**：`<ul>` 每列「標籤＋值」，
  標籤取自 `common.footer.labels`（`電郵：`／`電話：`），`--fs-small` `--text-muted`；
  列距 `--space-2`，值為 `.link`。與 footer 聯絡欄同一組視覺。

---

## 7. 動態 Motion

```css
--dur-fast: 120ms;  --dur: 180ms;  --dur-slow: 240ms;  --dur-reveal: 420ms;
--ease:    cubic-bezier(.22,.61,.36,1);   /* 標準出場 */
--ease-in: cubic-bezier(.55,.06,.68,.19); /* 收合 */
```
- **唯一的捲動動畫：fade-up。** `opacity:0; transform:translateY(16px)` → `opacity:1; translateY(0)`，`--dur-reveal` ＋ `--ease`。IntersectionObserver：`threshold:0.15`、`rootMargin:"0px 0px -10% 0px"`、**只播一次**（觸發後 unobserve）。群組項目 stagger 60ms，最多疊到第 6 項（360ms 封頂）。
- Hover 只允許：`color`、`background-color`、`border-color`、`box-shadow`、`transform:translateY(-1~-2px)`、光譜線 `scaleX`。時長 `--dur`。
- 禁止：視差捲動、自動輪播、彈跳／回彈曲線、旋轉入場、打字機效果、數字滾動計數、骨架載入動畫、滑鼠跟隨光暈、任何 >500ms 的動畫。
- Focus 環永不動畫、永不移除。
```css
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{
    animation-duration:.01ms!important; animation-iteration-count:1!important;
    transition-duration:.01ms!important; scroll-behavior:auto!important;
  }
  .reveal{opacity:1!important; transform:none!important;}
}
```
JS 亦須偵測 `matchMedia('(prefers-reduced-motion: reduce)')`，命中時直接把元素設為可見、不註冊 observer。

**無 JS 保底（必要）**：動畫預設「關」—— CSS 的 `.reveal{opacity:1; transform:none;}` 是基準狀態，
隱藏起始狀態寫在 `.js-anim .reveal{…}`。`<head>` 內的 inline script 加上 `html.js-anim` 開啟動畫，
同時設一道 1200ms 保險：`main.js` 沒有加上 `html.js-ready` 就自行撤除 `js-anim`。
`main.js` 的初始化全段包在 `try/catch`，catch 內也會撤除 `js-anim`。
因此 JS 被封鎖、載入失敗或初始化拋錯時，全站內容仍完整可見（絕不可反過來由 head 直接開啟隱藏狀態）。
影片同理：標記只寫 `data-autoplay`，由 `main.js` 在暫停鈕可用之後才補上 `autoplay` 並播放。
沒有 JS 就只顯示 poster —— 絕不能出現「會自動播放但按不停」的影片（WCAG 2.2.2）。

---

## 8. 影像方向（供後續 prompt 撰寫者）

**題材**：無塵室內部與設備列（equipment bay）、黃光區的琥珀色照明環境、機台操作面板與晶圓傳送匣（FOUP）、12 吋晶圓在燈下的繞射彩虹、防塵衣（bunny suit）工程師進行維護與拆裝機、設備包裝與吊裝運送、貨櫃與空運物流、香港辦公室與維港天際線、教育訓練場景（工程師圍著白板或機台講解）、AI 主題以「乾淨的資料視覺化投影在無塵室玻璃上」表現。

**風格**：紀實攝影感（documentary），非 3D 渲染、非插畫。35mm / 50mm 視角，f/2.8–f/5.6，淺至中景深；垂直線保持正交（建築攝影式修正）。構圖冷靜，偏對稱或強線性透視。

**色調**：冷中性基調（偏冷白平衡），呼應 `--dark-900` 與 `--bg`；整體彩度降低約 10–15%，只在晶圓繞射、指示燈與黃光區保留彩度峰值——讓照片中的「彩虹」與 logo 的光譜互相呼應。高光柔和不過曝，陰影保留細節（不要死黑）。

**光線**：以無塵室頂部均勻漫射光為主，加一道側向柔光造型；黃光區採真實琥珀色（約 #E9B23C）而非濾鏡感的橘。夜間物流可用低色溫燈光對比冷藍天空。

**畫幅**：hero 16:9、卡片 4:3、直式人像 3:4、寬帶 21:9。人物一律配戴完整無塵服與護目鏡，臉部不需清晰可辨（避免肖像權問題）。

**避免**：握手／西裝合照等 stock 味構圖、假造的 UI／HUD／全息投影疊加、任何可辨識的真實品牌 logo 或機台銘牌字樣、地球儀＋電路板的陳腔濫調、紫色霓虹 AI 風、過度銳化與 HDR 光暈、可辨識的真實客戶或廠房、任何暗示倍特爾擁有自有晶圓廠的畫面（本公司為設備採購與服務商）、畫面內文字（AI 生成文字易變形；所有文案由 HTML 呈現）。

---

## 9. Do / Don't

**Do**
- 每個視覺值都引用本檔 token（`var(--…)`），不寫死色碼。
- 一屏內只有一個主要行動（primary button）。
- 用留白與 1px 線分區，而不是用底色塊分區。
- 中文標題短、直述、可掃描；英文只用於 eyebrow 與品牌名。
- 所有數字先問：GOAL.md 有嗎？沒有就不要寫。
- 媒體佔位一律套用 §6.8 的統一樣式與資產 ID。

**Don't**
- 不加第三種字體、第二個 accent 色、彩色陰影、>12px 圓角。
- 不用光譜漸層做背景、按鈕、文字色或圖示色。
- 不放任何第三方品牌 logo；不寫「授權代理」「official distributor」「原廠指定」。
- 不把 AI 架構表的量化結果寫成倍特爾的成果或客戶成效。
- 不捏造成立年份、人數、案例、認證、客戶、獎項、辦公室據點。
- 不用 emoji 當圖示、不用外部 JS／圖示 CDN（Google Fonts 除外）。
- 不做輪播、視差、數字計數、自動播放有聲影片。

---

## 10. 無障礙檢查表（每頁上線前逐項確認）

- [ ] `<html lang="zh-Hant-HK">`；`<title>` 含頁名與公司名；`meta description` 為繁中。
- [ ] 標題階層連續（每頁唯一 h1，不跳級）。
- [ ] 所有文字對比 ≥ 4.5:1（大型標題 ≥ 3:1）；暗帶連結使用 `--accent-on-dark`。
- [ ] `:focus-visible` 全站可見：2px `--accent` outline ＋ 2px offset（暗帶改用 `--accent-on-dark`）。
- [ ] Skip link（跳至主要內容）為頁面第一個可聚焦元素。
- [ ] `<nav aria-label="主要導覽">`；當前頁加 `aria-current="page"`。
- [ ] 所有 `<img>` 有 `alt`（裝飾性用 `alt=""`）；媒體佔位層 `aria-hidden="true"`，資產 ID 不被朗讀。
- [ ] 影片不自動播放；若自動播放必須靜音＋`playsinline`＋可暫停，並提供 poster。
- [ ] 表格有 `<caption>` 與 `<th scope>`；橫捲容器可鍵盤聚焦（`tabindex="0"` ＋ `role="region"` ＋ `aria-label`）。
- [ ] 手風琴與行動選單可鍵盤操作，狀態以 `aria-expanded` 表示。
- [ ] 觸控目標 ≥ 44×44px；漢堡按鈕有 `aria-label`。
- [ ] `prefers-reduced-motion` 下所有內容仍完整可見。
- [ ] 320px 寬不橫向捲動；200% 縮放不破版。
- [ ] mailto 連結文字即為信箱本身，方便朗讀與複製。

---

## 11. 修訂與偏離紀錄（Amendments）

本節記錄第三、四階段實作時相對本文件與 `docs/content-spec.md` 的偏離，以及事後補上的規則。
之後每次偏離都必須追加一列，否則規格與實作會再度失聯。

| 項目 | 說明 |
|---|---|
| 站台外殼頁（`dist/index.html` 語言閘道、`dist/404.html`） | 本文件 §1–§10 只規範內容頁。兩張外殼頁不套用 `assets/css/style.css`，樣式內嵌在 `templates/gateway.html`／`templates/404.html`；文案取自 `common.json` 的 `shell` 物件（見 `docs/content-schema.md §4`），因此仍受四語結構驗證。 |
| 404 不自動轉頁 | 原先 4 秒自動導回閘道，違反 WCAG 2.2.1（Timing Adjustable）。已移除計時器，改為四語語言連結 ＋「回到語言選擇」連結。閘道頁的立即轉向不受影響（純路由、沒有可讀內容）。 |
| 混語片段標記 | 外殼頁的四語並列文字每段各自包在 `<span lang="…">`（WCAG 3.1.2）。 |
| 動畫預設關閉 | `.reveal` 的隱藏起始狀態改由 `html.js-anim` 開啟（見 §7）；原本的 `.no-js` 反向作法在 `main.js` 載入失敗時會讓整頁空白。 |
| 媒體 `caption` 規則 | `caption` 收成簡短主體標籤，美術指導用語只留在 `alt`（見 `docs/content-schema.md §2`）。四語一致。 |
| `title_lat` 的斜線 | 語言不變欄位一律用 ASCII `LithoDreamer / ILT`；CJK 譯文（`arch` 等非不變欄位）仍用全形／。 |
| 閘道頁不自動轉頁 | 原先 `templates/gateway.html` 帶 `<meta http-equiv="refresh" content="1;url=…">` 當無 JS 的退路，任何非零延遲的自動轉頁都是 WCAG 2.2.1 的失敗案例（技術 F40）。已整條移除：有 JS 時由頁尾的路由腳本立即轉向，無 JS 時就停在閘道頁點四個語言連結。`common.json` 的 `shell.gateway_note` 四語同步改成祈使句（「請選擇語言版本」／`Choose your language`），無 JS 時文案才不會與行為矛盾。 |
| 內容圖不做 `srcset` | 經評估後**維持現狀**：`media_img` 只出一張 1600px 長邊的 JPEG（`tools/optimize_media.py` 已壓到 400 KB 以下，實測最大 273 KB）。在 1440 版面下卡片圖約 355 CSS px，1x 螢幕確實多下載了像素，但這是頻寬取捨、不影響正確性（`.media` 有 `aspect-ratio`，CLS 為 0），而加 `srcset` 需要轉檔工具多產一組 800px 檔、資產數量翻倍。日後若要做，作法是 `optimize_media.py` 同時輸出 800／1600 兩個版本，並在 `media_img` 加 `srcset`／`sizes`。 |
| `logo-256.png`／`logo-512.png` | 全站（HTML／CSS／模板／manifest）沒有任何地方參照，建置時本來就不複製到 `dist/`，已從版控移除以免誤以為是交付檔。實際使用中的衍生檔只有 `logo-96.png`（閘道頁與 header 標記）與 `favicon-*`；需要更大尺寸時從根目錄的 `logo.png`（2048px）重新產生。 |
| `tools/check_links.py` | 第三階段新增：檢查 `dist/` 內部連結，root-absolute 路徑視為錯誤。CI 三關之一（README §8.4）。 |
| `SITE_URL` 優先序 | `--base-url` ＞ 環境變數 `SITE_URL` ＞ `build.py` 常數（README §2、§8.2）。 |
| 2026-08 精修（聯絡資訊／FAQ／版面） | 逐項改動與理由見 **§12 精修紀錄**；§5 垂直節奏表、§6.1、§6.2、§6.9、§6.15、§6.17 已同步更新。 |
| 未被參照的資產不進 `dist/` | `assets/img`／`assets/video` 裡沒有任何 content JSON 指到、也不在 `build.py` 的 `SHELL_ASSETS` 白名單內的檔案，建置時只列出警告、不複製（避免交付檔悄悄變成死重量）。 |

---

## 12. 精修紀錄（Refinement log）

### 2026-08-19 — 聯絡資訊調整、移除 FAQ、版面精修

客戶指示（原文）：「不用寫聯繫人名，只要留郵箱跟手機號碼就可以，+86-135-3007-1950,
better_stg@163.com，移除常見問題FAQ，優化微調版面設計。」

本次是**設計系統內的精修**，不是改版：token、字體、色彩、元件語彙、頁面結構一律不動；
只調整既有數值與兩個聯絡資訊元件。以下逐項記錄改動與理由。

#### A. 內容（Tasks 1–2）

| 改動 | 理由 |
|---|---|
| 全站移除聯絡人姓名（footer、contact 資訊列與側欄卡、about 負責人卡的信箱行、meta description、四語 JSON） | 客戶指示：聯絡方式只留信箱與電話 |
| 信箱改為 `better_stg@163.com`（含 `main.js` 的 fallback 與四語 `cta_band`／`form.mailto`） | 同上 |
| 新增電話 `+86-135-3007-1950`（顯示四語一致）／`tel:+8613530071950`；footer 標籤 `聯絡人：` → `電話：`（电话：／Phone: ／電話：） | 同上 |
| about 頁「公司負責人」卡**保留姓名與職稱**，只拿掉卡片底部的 mailto 行 | 該卡是公司治理資訊，不是聯絡方式；拿掉信箱後就不再把個人呈現為聯絡窗口 |
| 移除聯絡頁 FAQ 區塊（模板、四語 JSON、規格文件、`#faq-*` 錨點） | 客戶指示 |
| 側欄「填寫前可先看」三個 FAQ 錨點 → 服務項目／設備與製程／AI 智慧製造三頁 | FAQ 移除後錨點會斷；改指實際頁面，卡片仍有存在意義 |

#### B. 版面精修（Task 3）

| # | 改動 | 之前 → 之後 | 理由 |
|---|---|---|---|
| 1 | 桌機區塊垂直節奏收緊一級 | `--sec-pad` 96→80、`--sec-pad-major` 128→96、`--sec-pad-tight` 48→40 | 相鄰兩個 section 各 96px，內容之間出現 192px 空白 —— 在 1440×900 上超過視窗高度的五分之一是純空白，讀起來像「沒排完」而不是留白。收到 80 後仍寬裕，但每頁少掉一到兩屏的空轉，也更貼近 §1 所寫「說服力來自資訊密度與版面秩序」。所有值仍在 4／8 尺標上；行動版不變（64/80/32） |
| 2 | `.section-header` 下距離統一 40px | 桌機 48 → 40 | 原本桌機 48／行動 40 與 §5「lead→內容 = 40px」不符，且與收緊後的區塊 padding 疊加後標題與內容之間過鬆。改回規格值，順帶讓四個斷點的節奏一致 |
| 3 | 內頁亮帶 hero 下緣改為 1px 光譜髮絲線 | `border-bottom:1px var(--border)` → `::after` 1px `--grad-spectral-soft` | 內頁頁首原本以一條灰線收尾，與首頁暗帶 hero 底部的光譜髮絲線斷了關係，13 個內頁的頁首因此像「還沒做完的白框」。改為髮絲線後同一語彙貫穿全站，且仍只有 1px、不承載資訊。每屏光譜元素種類仍為 1（eyebrow 短線不計，見 §2） |
| 4 | 聯絡資訊改為 `.info-strip` 資訊列 | 三張獨立 `.card` → 一件帶框、格間 1px 分隔線的三格資訊列 | 地址比信箱／電話長一至兩行，等高卡片會在另外兩張下方各留 80–90px 空白，三張卡片看起來像沒填滿。收成「一件」後空白藏在格內、三筆資訊讀作同一組事實；骨架直接沿用 §6.6 統計列，不引入新視覺語彙 |
| 5 | 資訊列欄位名降級、值升級 | 欄位名 `--fs-h3`(22px)/600/`--text` → `--fs-small`/600/`--text-muted`；值 `--fs-body`/400/`--text-2` → `--fs-body`/500/`--text` | 「電子郵件」「電話」是欄位名不是標題，原本比信箱本身還顯眼。倒過來之後，一眼看到的是可用的值 |
| 6 | 側欄卡與 about 總部改用 `.contact-lines` | 單行 mailto ＋ 一行小字姓名 → 「電郵：／電話：」兩行標籤＋連結 | 電話加入後需要標籤才分得清；標籤直接沿用 `common.footer.labels`，與 footer 聯絡欄同一組視覺，不另造字串 |
| 7 | 側欄「填寫前可先看」改用箭頭連結 | `.feature-list`（前綴短破折號） → `.link-list` ＋ `.arrow-link` | 內容已從「問題」變成「頁面」，勾點列表的破折號讀起來像條列事實；箭頭連結是全站既有的「往下一頁」記號 |
| 8 | 聯絡頁分隔視覺併入「辦公室位置」段末 | 獨立的 `#contact-divider` section → 位置段末 `mt-12` | 移除 FAQ 後，這張裝飾條成了兩個 section 之間的孤兒圖，且與其後的暗色 CTA 帶連成兩塊深色。併進上一段後少一道區塊界線、頁面收尾更順，資產 `IMG-CONTACT-03` 仍在使用 |
| 9 | Sticky header 捲動後底色加不透明度 | `.is-stuck` 底 `rgba(246,247,248,.86)` → `.94` | 暗色媒體（首頁 AI 視覺、製程頁主視覺）從 header 底下通過時，.86 的底讓導覽字浮動不定。.94 仍看得出玻璃感，但字始終貼在固定底色上 |
| 10 | <960px footer 導覽連結補觸控高度 | 連結 gap 12px、可點高 ~22px → `padding-block:12px`、gap 0，可點高 ≥44px | §10 無障礙檢查表要求觸控目標 ≥44×44px，footer 兩欄連結原本不合格。只在 <960px 生效，桌機版面完全不變 |

**未動**：字體家族、型階、色彩 token（未新增任何色）、圓角、陰影、動態時長與曲線、
`prefers-reduced-motion`／無 JS／列印的行為、九大製程與各內頁的結構與文案。

**已知遺留**：`.accordion`（CSS §18）與 `main.js` 第 8 段「錨點展開手風琴」在 FAQ 移除後
不再有頁面使用。兩者都是既有元件與既有程式，本次刻意**不刪**（見 §6.15 標註）；
若確定不再需要手風琴，再另案移除。

