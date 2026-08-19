# components.md — 倍特爾官網元件庫（複製貼上用）

> **給頁面建置者：** 本檔是唯一的 HTML 片段來源。
> 建置任一頁面時：以 `templates/base.html` 為共用外殼，新頁面模板照既有 `templates/*.html`（如 `equipment-detail.html`）的結構建立，
> `<main>` 內容只能由本檔片段組裝。**不要自創 class、不要寫 inline 色碼、不要新增 CSS 檔或 JS 檔。**
> 文案一律取自 `docs/content-spec.md`；欄位結構見 `docs/content-schema.md`；視覺規則見 `DESIGN.md`。
>
> **四語版（zh-Hant／zh-Hans／en／ja）**：頁面已改由 `build.py` ＋ `templates/` ＋ `content/<lang>/*.json` 產生。
> 本檔片段仍是唯一的 class 與結構來源 —— 把片段搬進 `templates/` 時**只可以把文字換成 `{{ ... }}`，不可改動標籤、class 或屬性順序**。
> 欄位名稱見 `docs/content-schema.md`。
>
> 共通約定
> - 每個要「捲動淡入」的區塊或卡片加 `class="reveal"`；同組第 2–6 項再加 `reveal--d1` … `reveal--d5`（每階 60ms，最多疊到第 6 項）。
> - 每頁 **只有一個 `<h1>`**（在 hero）；區塊標題用 `<h2>`，卡片標題用 `<h3>`。
> - 每頁最多 **一個 CTA 帶**，放在 `</main>` 之前。
> - 每頁最多 **一個暗帶 hero**（僅 index.html 用暗帶，其餘一律亮帶）。
> - 同一屏內光譜元素最多 2 處（eyebrow 短線、卡片 hover 線、媒體角標各算 1 處）。

---

## 目錄

| 元件 | class | 何時使用 |
|---|---|---|
| [語言切換器](#0-語言切換器與各語言字體連結) | `.lang-switch` | header 與行動選單，四語版必備 |
| [暗帶 Hero](#1-暗帶-hero僅-indexhtml) | `.hero-dark` | 只有首頁 |
| [亮帶 Hero](#2-亮帶-hero所有內頁) | `.hero-light` | 所有內頁的頁首 |
| [麵包屑](#3-麵包屑) | `.breadcrumb` | 內頁 hero 內、h1 之上 |
| [Section header](#4-section-header) | `.section-header` | 每個區塊的開頭 |
| [卡片格線 3／4 欄](#5-卡片格線-34-欄) | `.grid--3` `.grid--4` | 平行並列的 3–9 個項目 |
| [製程卡](#6-製程卡九大製程用) | `.card--process` | 連往九大製程頁 |
| [AI 能力卡](#7-ai-能力卡) | `.card--ai` | 標示「對標／導入之前沿架構」 |
| [功能列表](#8-功能列表feature-list) | `.feature-list` | 設備範圍、服務內容、適用場景 |
| [品牌 chips](#9-品牌-chips) | `.brand-chips` | 列出日系設備品牌（純文字） |
| [統計列](#10-統計列) | `.stat-row` | 只放 GOAL.md 可驗證的數字 |
| [媒體佔位（圖）](#11-媒體佔位img-) | `.media` | 所有 `IMG-*` 資產 |
| [媒體佔位（影片）](#12-媒體佔位vid-) | `.media` + `<video>` | 所有 `VID-*` 資產 |
| [表格](#13-表格ai-架構表) | `.table-wrap` | AI 架構對標表、對應矩陣 |
| [步驟／時間軸](#14-步驟時間軸) | `.steps` | 服務流程、導入步驟 |
| [手風琴](#15-手風琴details) | `.accordion` | FAQ |
| [兩欄圖文](#16-兩欄圖文) | `.split` | 文字＋媒體並置 |
| [按鈕與連結](#17-按鈕與連結) | `.btn` `.arrow-link` `.link` | 行動點 |
| [Tag](#18-tag) | `.tag` | 狀態／分類標示（不可當按鈕） |
| [製程頁翻頁](#19b-製程頁翻頁) | `.pager` | 九個 `equipment-*.html`，CTA 帶之前 |
| [CTA 帶](#19-cta-帶共用聯絡條) | `.cta-band` | 每頁 footer 之前 |
| [表單](#20-表單僅-contacthtml) | `.form` | 只有 contact.html |

---

## 0. 語言切換器與各語言字體連結

### 0.1 `<head>` 內的字體連結（每個語言只載入自己的 CJK 字體）

```html
<!-- zh-Hant -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;700&display=swap">
<!-- zh-Hans -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap">
<!-- ja -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap">
<!-- en（不載入 CJK 字體） -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
```

前面固定接兩行 `preconnect`（`fonts.googleapis.com` 與 `fonts.gstatic.com`，後者加 `crossorigin`）。
`<html lang>` 依語言為 `zh-Hant-HK`／`zh-Hans-CN`／`en`／`ja`；`--font-cjk` 由 `style.css` 的
`html[lang^=...]` 選擇器自動切換，不需要在頁面裡寫任何 style。

### 0.2 桌機切換器（放在 `.nav` 內，導覽清單與 CTA 按鈕之間）

```html
<nav class="lang-switch" aria-label="語言選擇">
  <a class="lang-switch__item" href="../zh-hant/index.html" hreflang="zh-Hant" lang="zh-Hant" aria-current="true" title="繁體中文"><span aria-hidden="true">繁</span><span class="visually-hidden">繁體中文</span></a>
  <a class="lang-switch__item" href="../zh-hans/index.html" hreflang="zh-Hans" lang="zh-Hans" title="簡體中文"><span aria-hidden="true">简</span><span class="visually-hidden">簡體中文</span></a>
  <a class="lang-switch__item" href="../en/index.html" hreflang="en" lang="en" title="English"><span aria-hidden="true">EN</span><span class="visually-hidden">English</span></a>
  <a class="lang-switch__item" href="../ja/index.html" hreflang="ja" lang="ja" title="日本語"><span aria-hidden="true">日</span><span class="visually-hidden">日本語</span></a>
</nav>
```

### 0.3 行動版切換器（放在 `.mobile-nav` 的清單與 `.mobile-nav__cta` 之間）

```html
<nav class="lang-switch lang-switch--mobile" aria-label="語言選擇">
  … 同上四個 <a class="lang-switch__item"> …
</nav>
```

規則
- `href` 一律指向**其他語言的同一頁**（同檔名），不是回首頁。
- 標籤 `繁 / 简 / EN / 日` 四語共用，**不翻譯**；`.visually-hidden` 內才放翻譯後的語言名。
- 目前語言加 `aria-current="true"`，不加底線或光譜線（那是導覽項目的記號）。
- 不做下拉選單、不放國旗、不隱藏未選語言。視覺規範見 `DESIGN.md §6.1b`。

---

## 1. 暗帶 Hero（僅 index.html）

深藍暗帶＋晶圓網格底紋＋底部光譜髮絲線。**只有首頁可用。**

```html
<section class="hero-dark" id="hero">
  <div class="container">
    <div class="hero__grid">
      <div class="hero__content">
        <p class="eyebrow">Semiconductor Equipment &amp; AI</p>
        <h1 class="hero__title"><span class="nb">先進半導體製程的</span><span class="nb">整合夥伴</span></h1>
        <p class="hero__lead">九大主製程設備採購、拆裝運送、技術導入與 AI 整合。</p>
        <p class="hero__sub">以香港為據點，串接日系主力設備品牌與前沿人工智能架構。</p>
        <div class="hero__actions btn-row">
          <a class="btn btn--on-dark-primary" href="contact.html">洽詢設備與服務</a>
          <a class="btn btn--on-dark-secondary" href="equipment.html">瀏覽九大製程</a>
        </div>
      </div>
      <div class="hero__media reveal">
        <!-- 影片或圖片佔位，見 §11 / §12 -->
      </div>
    </div>
  </div>
  <span class="hero__rule" aria-hidden="true"></span>
</section>
```

> `.nb` = 不可斷詞單位。中文長標題請以語意切段包起來，避免在詞中折行。

---

## 2. 亮帶 Hero（所有內頁）

白底、下 1px 邊框、含麵包屑。**每頁只有一個 `<h1>`。**

```html
<section class="hero-light" id="about-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="麵包屑">
      <ol>
        <li><a href="index.html">首頁</a></li>
        <li><span aria-current="page">關於我們</span></li>
      </ol>
    </nav>
    <p class="eyebrow">About Better</p>
    <h1>立足香港的半導體設備集團</h1>
    <p class="lead">以設備、製程、人才與 AI 四條主線服務先進製造。</p>
  </div>
</section>
```

製程頁另可在 h1 下加英文名：

```html
<h1>黃光段設備</h1>
<p class="lat muted small">Lithography</p>
```

---

## 3. 麵包屑

三層（製程頁）版本；放在亮帶 hero 的 `.container` 最上方。

```html
<nav class="breadcrumb" aria-label="麵包屑">
  <ol>
    <li><a href="index.html">首頁</a></li>
    <li><a href="equipment.html">設備與製程</a></li>
    <li><span aria-current="page">黃光段</span></li>
  </ol>
</nav>
```

---

## 4. Section header

每個 `<section>` 的開頭。eyebrow 為英文、自帶 24px 光譜短線。

```html
<section class="section" id="pillars">
  <div class="container">
    <div class="section-header reveal">
      <p class="eyebrow">What We Do</p>
      <h2>五大核心業務</h2>
      <p class="lead">從設備到製程、從人才到人工智能的完整覆蓋。</p>
    </div>
    <!-- 區塊內容 -->
  </div>
</section>
```

區塊外殼可選：

| class | 效果 |
|---|---|
| `.section` | 標準上下留白（桌機 96px） |
| `.section--major` | 重點區塊（桌機 128px） |
| `.section--tight` | 緊湊列（桌機 48px） |
| `.section--alt` | 淺灰底（一頁最多用 2 次，用來分節奏） |
| `.section--line` | 上緣 1px 分隔線 |
| `.section-header--center` | 置中（僅 CTA 帶用） |

---

## 5. 卡片格線 3／4 欄

3 欄用 `.grid--3`（≥960px 三欄）；設備列表 4 欄用 `.grid--4`（≥1200px 四欄）。
整卡可點時用 `<a class="card card--link">`；純陳述用 `<article class="card">`。

```html
<div class="grid grid--3">

  <a class="card card--link reveal" href="services.html#service-relocation">
    <p class="card__num">02</p>
    <h3 class="card__title">拆裝機及運送服務</h3>
    <p class="card__text">提供設備拆機、包裝、跨境運送、進場定位與重新安裝的全流程執行與協調。</p>
    <p class="card__foot"><span class="arrow-link">服務內容</span></p>
  </a>

  <article class="card reveal reveal--d1">
    <h3 class="card__title">一站式採購到裝機</h3>
    <p class="card__text">採購、驗機、拆機、包裝、運送、進場、安裝與調試由同一團隊統籌。</p>
  </article>

</div>
```

服務卡（services.html）於標題上方加 28px 線稿圖示，`stroke` 用 `currentColor`：

```html
<article class="card reveal">
  <svg class="card__icon" viewBox="0 0 24 24" aria-hidden="true">
    <path d="M3 7h18M3 12h18M3 17h18"/>
  </svg>
  <h3 class="card__title">設備採購與銷售</h3>
  <p class="card__text">九大主製程設備的選型、採購與維護支援。</p>
  <p class="card__foot"><a class="arrow-link" href="#service-equipment">了解更多</a></p>
</article>
```

> 卡片格線最後一格可放媒體佔位補滿（用 `.media--fill`），見 §11。

---

## 6. 製程卡（九大製程用）

編號 → 中文名 → 英文名 → 一行說明 → 品牌 chips → 查看設備。

```html
<a class="card card--link card--process reveal" href="equipment-lithography.html">
  <p class="card__num">01</p>
  <h3 class="card__title">黃光段</h3>
  <p class="card__en">Lithography</p>
  <p class="card__text">曝光、旋塗與顯影設備，決定線寬與圖形精度。</p>
  <ul class="brand-chips">
    <li class="brand-chip">NIKON</li>
    <li class="brand-chip">CANON</li>
    <li class="brand-chip">TEL</li>
    <li class="brand-chip">DNS</li>
  </ul>
  <p class="card__foot"><span class="arrow-link">查看設備</span></p>
</a>
```

> 九張製程卡下方**必須**接一句合規說明（見 §9）。
> 英文版（`lang == 'en'`）省略 `.card__en` 一行——標題本身已是英文，兩行會重複；繁中／簡中／日文照常輸出。

---

## 7. AI 能力卡

左側 3px 直立光譜條（全站唯一允許的直式光譜）。**必須標示為對標／導入之前沿架構。**

```html
<article class="card card--ai reveal">
  <h3 class="card__title">數字孿生 <span class="lat">Digital Twin</span></h3>
  <p class="card__text">為機台與製程建立虛擬對照體，於模型中先行驗證條件變更與維護排程。</p>
</article>
```

帶架構名與年份時（**九個製程頁一律用這個欄位順序**：架構名 → 對本製程的作用 → `對標指標：` → tag）：

```html
<article class="card card--ai reveal">
  <p class="card__arch">DeepOHeat-v1 <span class="card__year">（2025）</span></p>
  <p class="card__text">以 DeepONet＋KAN 建立熱場代理模型，快速推算腔體與晶圓熱分布。</p>
  <p class="card__meta">對標指標：MAPE 0.035%、訓練 -62×、記憶體 -31×</p>
  <p class="card__foot"><span class="tag">對標／導入之前沿架構</span></p>
</article>
```

> tag 一律是「對標／導入之前沿架構」，**不可**把量化指標放進 tag；指標一律寫在 `card__meta`
> 並以「對標指標：」起頭。製程頁的「AI 整合」區塊版型也固定為：
> `section-header`（全幅）＋ `grid grid--3`（四張卡時用 `grid--4`）＋全幅 `media--16-9` 收尾媒體。

> 量化結果（如 MAPE 0.035%）只能出現在架構表或 AI 卡內，且必須標明為第三方研究成果。

---

## 8. 功能列表（feature list）

設備範圍、服務內容、涵蓋範圍、交付項目、適用場景一律用這個。

```html
<ul class="feature-list feature-list--3">
  <li>設備採購與機種評估選型</li>
  <li>設備狀態查驗與驗機協助</li>
  <li>拆機、包裝與跨境運送</li>
  <li>進場安裝、對準與調試</li>
</ul>
```

> 全幅區塊（服務內容、交付項目、適用場景、業務範圍）用 `feature-list--3`
> （≥960px 三欄、≥640px 兩欄、行動版單欄；恰好 4 項時 ≥960px 自動改排 2×2，
> 避免第二列只剩一個孤兒）；兩欄圖文的窄欄內用 `feature-list--2` 或不加修飾子。
> 單欄時去掉修飾子。定義式內容（使命／願景）改用 `.def-list`：
> `<dl class="def-list"><dt>使命</dt><dd>…</dd></dl>`

---

## 9. 品牌 chips

**純文字，嚴禁品牌 logo 圖檔。** 寫法固定：NIKON、CANON、TEL、DNS、SAMCO、TAZMO、ULVAC、NISSIN、EBARA、ACCRETECH、ADVANTEST、NUFLARE、JEOL、MATSUSHITA、**KOKUSAI ELECTRIC (KE)**、**LASERTEC**。

```html
<ul class="brand-chips">
  <li class="brand-chip">KOKUSAI ELECTRIC (KE)</li>
  <li class="brand-chip">MATSUSHITA</li>
</ul>
<p class="brand-note">上列品牌設備由倍特爾提供採購、銷售及維護服務；品牌名稱為其各自所有權人之商標，僅供設備說明之用。</p>
```

製程頁也可用「品牌條」：

```html
<p class="brand-bar">NIKON · CANON · TEL · DNS</p>
```

> **不得**寫「授權代理」「official distributor」「原廠指定」。

---

## 10. 統計列

**只能放 GOAL.md 可驗證的事實**：9 大主製程、16 個日系設備品牌、5 項核心業務。
禁止成立年份、人數、營收、客戶數、良率提升幅度。

```html
<section class="section section--tight" aria-label="服務範圍概要">
  <div class="container">
    <div class="stat-row reveal">
      <div class="stat-row__item">
        <p class="stat-row__num">9</p>
        <p class="stat-row__label">大主製程設備涵蓋範圍</p>
      </div>
      <div class="stat-row__item">
        <p class="stat-row__num">16</p>
        <p class="stat-row__label">個日系主力設備品牌</p>
      </div>
      <div class="stat-row__item">
        <p class="stat-row__num">5</p>
        <p class="stat-row__label">項核心業務服務</p>
      </div>
    </div>
  </div>
</section>
```

> 四格版加 `.stat-row--4`。沒有真實數字時，改用三欄文字卡，不要硬湊數據列。

---

## 11. 媒體佔位（IMG-*）

**這是唯一允許的圖片寫法。** 檔案不存在時顯示設計化佔位框；把 `assets/img/<page>-<nn>.jpg` 放進去即自動顯示。

```html
<div class="media media--4-3" data-asset="IMG-HOME-03">
  <img src="assets/img/home-03.jpg"
       alt="抽象資料視覺化：晶圓熱場等高線與感測時序曲線疊合"
       loading="lazy" decoding="async"
       onerror="this.hidden=true">
  <div class="media__ph" aria-hidden="true">
    <span class="media__id">IMG-HOME-03</span>
    <span class="media__desc">晶圓熱場等高線與感測時序曲線疊合</span>
  </div>
</div>
```

必守事項：
- `data-asset` 與 `.media__id` 內容 = 資產 ID，**兩處必須一致**。
- `src` 由 ID 推導：`IMG-HOME-03` → `assets/img/home-03.jpg`（PAGE 轉小寫）。
- 放圖時檔名照上式命名即可，**副檔名與尺寸不拘**；執行 `python tools/optimize_media.py` 會依 `content/zh-hant/*.json` 的 `ratio` 轉成交付檔（`.jpg`、正確比例、長邊 1920／1600、≤ 400 KB），原始檔移入 `assets/src/`（不進 `dist/`）。
- `onerror="this.hidden=true"` **不可省略**（`assets/js/main.js` 另有備援偵測）。
- `.media__ph` 必須 `aria-hidden="true"`；`<img>` 一定要有中文 `alt`。
- 比例：`media--16-9`（hero／寬幅）、`media--4-3`（卡片／段落）、`media--3-4`（直式）、`media--21-9`（地圖／寬帶）。
- 放進卡片格線當一格時加 `media--fill`（改為填滿該格）。
- 佔位框內**不得**加假 UI、假圖表、假數據、emoji 或插畫。

---

## 12. 媒體佔位（VID-*）

自動播放一律 **靜音 ＋ loop ＋ playsinline ＋ poster ＋ 可暫停按鈕**。
標記裡寫的是 `data-autoplay` 而不是 `autoplay`：暫停鈕要靠 `main.js` 才會動，
沒有 JS 就不該有停不下來的自動播放（WCAG 2.2.2）。`main.js` 偵測到控制項可用後才補上
`autoplay` 並呼叫 `play()`；`prefers-reduced-motion` 時不補，只顯示 poster。

```html
<div class="media media--16-9" data-asset="VID-HOME-01">
  <video muted loop playsinline data-autoplay preload="metadata"
         poster="assets/img/home-01-poster.jpg"
         onerror="this.hidden=true"
         aria-label="無塵室環境橫移鏡頭，晶圓傳輸機械手臂與設備艙門運作">
    <source src="assets/video/home-01.mp4" type="video/mp4">
  </video>
  <div class="media__ph" aria-hidden="true">
    <span class="media__id">VID-HOME-01</span>
    <span class="media__desc">無塵室橫移長鏡頭：晶圓傳輸機械手臂與設備艙門運作</span>
  </div>
  <button class="media__ctrl" type="button" data-media-ctrl>暫停影片</button>
</div>
```

> `VID-HOME-01` → 影片 `assets/video/home-01.mp4`、海報 `assets/img/home-01-poster.jpg`。
> `[data-media-ctrl]` 由 `main.js` 接管文字與播放狀態；影片未載入時該按鈕自動隱藏。

---

## 13. 表格（AI 架構表）

外層 `.table-wrap` 提供圓角與右緣漸隱；內層 `.table-scroll` 提供橫捲並可鍵盤聚焦。

```html
<div class="table-wrap reveal">
  <div class="table-scroll" tabindex="0" role="region" aria-label="AI 架構對標表，可左右捲動">
    <table class="data-table">
      <caption class="visually-hidden">AI 架構對標表：領域、代表模型、核心架構與量化結果</caption>
      <thead>
        <tr>
          <th scope="col">領域</th>
          <th scope="col">代表模型（年份）</th>
          <th scope="col">核心架構</th>
          <th scope="col">關鍵量化結果</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">熱模擬代理</th>
          <td class="model">DeepOHeat-v1（2025）</td>
          <td>DeepONet＋KAN＋GMRES 細化</td>
          <td class="num">MAPE 0.035%、訓練-62×、記憶體-31×</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
<p class="table-note">資料來源為第三方公開發表之研究與產業資訊，倍特爾以其作為導入對標基準。</p>
```

必守事項：
- `<caption>` 用 `visually-hidden`（可見說明句一律放表格下方的 `.table-note`，否則窄螢幕會被橫捲切掉）。
- 每個欄標題都要 `scope="col"`，列標題 `scope="row"`。
- 模型名加 `class="model"`、量化數字加 `class="num"`。
- **架構名稱與年份必須與 GOAL.md／content-spec 完全一致，不得改寫或補值。**

---

## 14. 步驟／時間軸

服務流程、AI 導入步驟。

```html
<ol class="steps">
  <li class="steps__item reveal">
    <span class="steps__dot" aria-hidden="true"></span>
    <p class="steps__num">01</p>
    <p class="steps__title">諮詢</p>
    <p class="steps__text">釐清製程節點、產能目標、場地與廠務限制，界定專案範圍。</p>
  </li>
  <li class="steps__item reveal reveal--d1">
    <span class="steps__dot" aria-hidden="true"></span>
    <p class="steps__num">02</p>
    <p class="steps__title">評估選型</p>
    <p class="steps__text">跨品牌機種比較，提出規格、交期與成本的可行方案。</p>
  </li>
</ol>
```

---

## 15. 手風琴（`<details>`）

FAQ 專用；原生可鍵盤操作，不需額外 JS。

```html
<div class="accordion">
  <details class="accordion__item">
    <summary class="accordion__summary">
      倍特爾是這些品牌的授權代理嗎？
      <span class="accordion__icon" aria-hidden="true"></span>
    </summary>
    <div class="accordion__body">
      <p>我們提供上述日系品牌設備的採購、銷售及維護服務。網站所列品牌名稱為其所有權人商標，僅供設備說明之用。</p>
    </div>
  </details>
</div>
```

---

## 16. 兩欄圖文

```html
<div class="split split--7-5 split--top">
  <div class="reveal">
    <div class="section-header">
      <p class="eyebrow">Positioning</p>
      <h2>我們如何看待 AI</h2>
    </div>
    <p>AI 對半導體製造的價值，來自把感測、量測與檢測資料轉換為可行動的判斷。</p>
  </div>
  <div class="reveal reveal--d1">
    <!-- 媒體佔位 §11 -->
  </div>
</div>
```

| class | 欄寬 |
|---|---|
| `.split` | 6 / 6（預設，垂直置中） |
| `.split--7-5` | 7 / 5 偏文字 |
| `.split--5-7` | 5 / 7 偏內容 |
| `.split--top` | 改為頂端對齊 |
| `.split__media--first` | 讓媒體欄在行動版排最前 |

長文段落請包 `.prose`（最大 760px），段落自動限制在 38 個中文字寬。

---

## 17. 按鈕與連結

```html
<div class="btn-row">
  <a class="btn btn--primary" href="contact.html">洽詢設備與服務</a>
  <a class="btn btn--secondary" href="equipment.html">瀏覽九大製程</a>
</div>

<!-- 暗帶（hero-dark / cta-band）內改用： -->
<div class="btn-row">
  <a class="btn btn--on-dark-primary" href="contact.html">洽詢設備與服務</a>
  <a class="btn btn--on-dark-secondary" href="mailto:kerwin@bettertechgroup.com">kerwin@bettertechgroup.com</a>
</div>

<a class="arrow-link" href="equipment.html">查看設備與製程總覽</a>
<p>詳見<a class="link" href="ai.html">AI 智慧製造</a>頁面。</p>
```

規則：一屏只有一個 primary 按鈕；`.btn--sm` 用於導覽列；`.btn-row--center` 用於 CTA 帶。

---

## 18. Tag

```html
<span class="tag">對標／導入之前沿架構</span>
<span class="tag tag--neutral">Lithography</span>
```

> Tag **不可**當按鈕或連結使用。

---

## 19b. 製程頁翻頁

九個 `equipment-*.html` 專用，置於 CTA 帶之前。順序固定為
黃光段 → 蝕刻段 → 化學氣相沉積 → 烘烤製程 → 離子植入 → CMP 研磨 → 晶圓水洗 → 晶圓檢測 → 掩模版製程，
且**首尾相接**（掩模版製程的下一段是黃光段）。

```html
<nav class="pager" aria-label="製程頁導覽">
  <div class="container">
    <div class="pager__row reveal">
      <a class="pager__link pager__link--prev" href="equipment-mask.html">
        <span class="pager__label">上一段製程</span>
        <span class="pager__title">掩模版製程</span>
      </a>
      <a class="pager__link pager__link--next" href="equipment-etch.html">
        <span class="pager__label">下一段製程</span>
        <span class="pager__title">蝕刻段</span>
      </a>
    </div>
  </div>
</nav>
```

> 箭頭以 CSS `::before` / `::after` 產生，不寫在 HTML 內；只有這個元件可以出現在 `equipment-*.html`。

---

## 19. CTA 帶（共用聯絡條）

每頁 `</main>` 之前放一個，內容取自 content-spec §0.5（ai.html 主 CTA 改為「討論 AI 導入場景」）。

```html
<section class="cta-band" id="contact-band">
  <div class="container">
    <div class="cta-band__inner reveal">
      <p class="eyebrow eyebrow--center">Get in Touch</p>
      <h2>與我們談談您的產線需求</h2>
      <p class="lead">從設備選型到裝機與 AI 導入，提供單一窗口。</p>
      <div class="btn-row btn-row--center">
        <a class="btn btn--on-dark-primary" href="contact.html">洽詢設備與服務</a>
        <a class="btn btn--on-dark-secondary" href="mailto:kerwin@bettertechgroup.com">kerwin@bettertechgroup.com</a>
      </div>
    </div>
  </div>
</section>
```

製程頁的 CTA 文字改為「索取設備與服務說明」。

---

## 20. 表單（僅 contact.html）

`data-mailto-form` 會被 `main.js` 接管：驗證 → 組 mailto → 開啟郵件軟體。**不需要後端。**

```html
<form class="form form--2col" data-mailto-form data-mailto="kerwin@bettertechgroup.com" novalidate>
  <div class="field">
    <label for="f-name">姓名<span class="req" aria-hidden="true">*</span></label>
    <input id="f-name" name="name" type="text" required placeholder="請輸入您的姓名">
    <p class="error" role="alert"></p>
  </div>
  <div class="field">
    <label for="f-company">公司<span class="req" aria-hidden="true">*</span></label>
    <input id="f-company" name="company" type="text" required placeholder="公司或機構名稱">
    <p class="error" role="alert"></p>
  </div>
  <div class="field">
    <label for="f-email">Email<span class="req" aria-hidden="true">*</span></label>
    <input id="f-email" name="email" type="email" required placeholder="your@company.com">
    <p class="error" role="alert"></p>
  </div>
  <div class="field">
    <label for="f-phone">電話</label>
    <input id="f-phone" name="phone" type="tel" placeholder="含國碼，例如 +852">
    <p class="error" role="alert"></p>
  </div>
  <div class="field field--full">
    <label for="f-category">需求類別<span class="req" aria-hidden="true">*</span></label>
    <select id="f-category" name="category" required>
      <option value="">請選擇需求類別</option>
      <option>設備採購</option>
      <option>拆裝運送</option>
      <option>製程技術導入</option>
      <option>人才培訓</option>
      <option>AI 整合</option>
      <option>其他</option>
    </select>
    <p class="error" role="alert"></p>
  </div>
  <div class="field field--full">
    <label for="f-message">訊息<span class="req" aria-hidden="true">*</span></label>
    <textarea id="f-message" name="message" required placeholder="請簡述製程段、設備需求與時程"></textarea>
    <p class="error" role="alert"></p>
  </div>
  <div class="form__foot">
    <button class="btn btn--primary" type="submit">送出詢問</button>
    <p class="form__hint">送出後將開啟您的郵件軟體，內容已預先填入，請確認後寄出。</p>
  </div>
</form>
```

> 欄位 `name` 必須是 `name / company / email / phone / category / message`，主旨與內文格式已寫死在 `main.js`。

---

## 21. 上線前自檢（每頁）

- [ ] `<html lang="zh-Hant-HK">`、`<title>`、`meta description` 皆取自 content-spec。
- [ ] 只有一個 `<h1>`；標題階層不跳級。
- [ ] 每個 `IMG-*` / `VID-*` 都用 §11／§12 的完整寫法，`data-asset` 與 `.media__id` 一致。
- [ ] 品牌只有文字、沒有 logo；附上合規說明句；沒有「代理／授權」字樣。
- [ ] AI 數字都標示為第三方研究成果；沒有寫成倍特爾自有數據。
- [ ] 沒有捏造年份／人數／客戶／案例／認證。
- [ ] 每頁一個 CTA 帶，放在 footer 之前。
- [ ] 320px 寬不橫向捲動；表格用 `.table-wrap` 包起來。
