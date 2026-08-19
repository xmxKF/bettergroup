# content-schema.md — 多語內容 JSON 規格

本檔定義 `content/<lang>/*.json` 的**最終欄位名稱**。第三階段的模板作者與翻譯者
一律依此檔產出 JSON；欄位名稱不得自創、不得改名。

- 文案的唯一真實來源仍是 **`docs/content-spec.md`**（繁體中文母本）。本檔只規範「結構」。
- 版面與元件的唯一真實來源是 **`DESIGN.md`** 與 **`docs/components.md`**。
- 產生器：`build.py`（見 `README.md`）。

---

## 0. 語言與檔案

```
content/
  zh-hant/     ← 母本（繁體中文，香港／台灣用語）。結構基準。
  zh-hans/     ← 簡體中文，使用中國大陸半導體業界慣用術語（非逐字轉換）
  en/          ← English
  ja/          ← 日本語
```

每個語言目錄下的檔案完全相同：

| 檔名 | 對應頁面 | 模板 |
|---|---|---|
| `common.json` | 全站共用（header／footer／CTA 帶／表單） | `partials/*.html` |
| `index.json` | `index.html` | `templates/index.html` |
| `about.json` | `about.html` | `templates/about.html` |
| `services.json` | `services.html` | `templates/services.html` |
| `equipment.json` | `equipment.html` | `templates/equipment.html` |
| `ai.json` | `ai.html` | `templates/ai.html` |
| `contact.json` | `contact.html` | `templates/contact.html` |
| `equipment-lithography.json` … `equipment-mask.json`（9 檔） | `equipment-<area>.html` | `templates/equipment-detail.html` |

---

## 1. 全域不變式（build.py 會強制檢查）

1. **UTF-8、縮排 2 空白、`ensure_ascii: false`**（中文／日文以原字元存檔，不用 `\uXXXX`）。
2. **鍵結構完全一致**：每個語言的每個檔案，其巢狀鍵集合必須與 `zh-hant` 逐一相同。
   多一個鍵、少一個鍵都會讓建置失敗，並印出第一個不符的路徑。
3. **陣列長度完全一致**：`entries`、`features`、`steps`、`rows`… 的元素數量必須與
   `zh-hant` 相同。不可以因為某語言「講得比較短」就刪掉一項。
4. **語言不變欄位**：下列鍵在所有語言必須**逐字相同**，翻譯時原樣複製：

   | 鍵 | 內容 |
   |---|---|
   | `id` | 資產 ID（`IMG-HOME-01`）與區塊錨點（`service-relocation`、`faq-agency`） |
   | `file`／`poster` | 資產路徑 |
   | `ratio` | 媒體比例（`16-9`／`4-3`／`3-4`／`21-9`） |
   | `href`／`match` | 所有連結與 `data-nav-match` |
   | `brands` | 品牌名稱陣列（品牌名永不翻譯） |
   | `en` | 製程的英文名（`Lithography`、`Chemical Vapor Deposition`…） |
   | `title_lat` | 卡片中的拉丁文術語（`Digital Twin`、`LithoDreamer / ILT`） |
   | `num` | 統計數字與卡片編號（`9`／`16`／`01`） |
   | `logo`、`email`、`mailto`、`copyright_year`、`legal_name_en` | 全站固定值 |

   > 例外：`common.footer.labels.email`（欄位抬頭「電郵：」）、`common.form.messages.email`
   > （驗證訊息）、`common.form.mail.email`（信件抬頭）雖然鍵名是 `email`，內容卻是
   > 介面文字，**必須翻譯**；`common.languages.en` 雖然鍵名是 `en`，卻是語言物件、其
   > `name` 可翻譯。這四個路徑已列入 `build.py` 的 `INVARIANT_PATH_EXCEPTIONS`。

   另有以**完整路徑**指定的語言不變欄位（鍵名太常見，不能靠鍵名判斷），
   列在 `build.py` 的 `INVARIANT_PATH_PATTERNS`：

   | 路徑 | 內容 |
   |---|---|
   | `common.languages.*.label` | 語言切換器標籤 `繁`／`简`／`EN`／`日`，四語必須完全相同 |
   | `common.site.phone`／`common.site.phone_href` | 電話號碼與 `tel:` 連結，四語必須完全相同 |

5. **保留字**：JSON 的鍵**不可**使用 `items`、`keys`、`values`、`get`、`pop`、`update`
   等 Python dict 方法名 —— Jinja 的 `a.b` 會取到方法而不是資料。
   清單一律用 **`entries`**（本檔所有 schema 皆已遵守）。
6. **文案內的品牌與架構名不翻譯**：`KOKUSAI ELECTRIC (KE)`、`LASERTEC`、`NUFLARE`、
   `DeepOHeat-v1`、`LithoDreamer`、`G2LGAN` 等一律保留原文，只翻譯其周圍的說明文字。
7. **AI 表格的量化結果是「對標架構」**：任何語言都不得改寫成倍特爾自有的量測數據。
   `note` 一定要譯出「第三方公開發表、作為導入與對標基準」的語意。

---

## 2. 媒體物件（media object）

出現在任何 `media` 欄位。**只有 `alt` 與 `caption` 需要翻譯。**

```jsonc
{
  "id": "IMG-HOME-01",                  // 語言不變
  "file": "assets/img/home-01.jpg",     // 語言不變
  "ratio": "4-3",                       // 語言不變：16-9 | 4-3 | 3-4 | 21-9
  "alt": "五大業務示意：半導體廠務剖面等距構圖",   // 翻譯（螢幕閱讀器用）
  "caption": "五大業務示意：半導體廠務剖面等距構圖" // 翻譯（佔位框上的說明）
}
```

**`caption` 是簡短的「主體標籤」，不是 `alt` 的複本。** `caption` 會在媒體尚未產出時
出現在佔位框裡，是訪客真的會讀到的字；美術指導用語（冷／暖色調、構圖留白、對稱構圖、
科學攝影風格、深色 UI、無可辨識人臉、燈光方向…）一律只留在 `alt`，不進 `caption`。
四種語言一致套用（`caption` 不是語言不變欄位，各語言各自翻譯）。
表格的 `caption`（`<caption class="visually-hidden">`）是另一回事，本來就該完整描述，不受此規則限制。

影片再加一個 `poster`（語言不變）：

```jsonc
{
  "id": "VID-HOME-01",
  "file": "assets/video/home-01.mp4",
  "poster": "assets/img/home-01-poster.jpg",
  "ratio": "16-9",
  "alt": "無塵室環境橫移鏡頭，晶圓傳輸機械手臂與設備艙門運作",
  "caption": "無塵室橫移長鏡頭：晶圓傳輸機械手臂與設備艙門運作"
}
```

純裝飾用的圖（例如 `contact.json` 的 `divider_media`）再加一個 `decorative`（語言不變、四語皆為 `true`）：

```jsonc
{
  "id": "IMG-CONTACT-03",
  "file": "assets/img/contact-03.jpg",
  "ratio": "21-9",
  "decorative": true,                   // 語言不變：輸出 alt=""（螢幕閱讀器略過）
  "alt": "深藍底上的細線光譜漸層橫紋",     // 仍須填寫（build.py 會檢查，也是佔位框說明的備援）
  "caption": "深藍底上的細線光譜漸層橫紋"
}
```

`decorative` 是**選填**欄位，只有需要輸出 `alt=""` 的圖才寫；沒有這個欄位的媒體物件行為不變。

### 命名對應規則（build.py 會驗證）

| 資產 ID | `file` | `poster` |
|---|---|---|
| `IMG-<PAGE>-NN` | `assets/img/<page>-<nn>.jpg`（亦接受 `.png`／`.webp`／`.avif`） | 不可有 |
| `VID-<PAGE>-NN` | `assets/video/<page>-<nn>.mp4` | `assets/img/<page>-<nn>-poster.jpg` |

`<page>` 為 ID 中間段的小寫：`HOME`→`home`、`SVC`→`svc`、`EQP`→`eqp`、`LITHO`→`litho`、
`ETCH`→`etch`、`CVD`→`cvd`、`BAKE`→`bake`、`IMP`→`imp`、`CMP`→`cmp`、`CLEAN`→`clean`、
`INSP`→`insp`、`MASK`→`mask`、`ABOUT`→`about`、`AI`→`ai`、`CONTACT`→`contact`。
檔案還沒產出也沒關係 —— 頁面會顯示 `docs/components.md §11–§12` 的佔位框。

---

## 3. 連結（href）慣例

- **同語言頁面**：只寫檔名，`"equipment-etch.html"`、`"services.html#service-relocation"`。
  產生器把頁面寫到 `dist/<lang>/`，因此相對連結會停在同一個語言資料夾內。
- **資產**：一律寫成 `"assets/img/…"`（不含 `../`）。模板會自己補上 `../` 前綴。
- **信件**：`"mailto:Masuhiro@bettertechgroup.com"`。
- **切換語言**：不需要寫在 JSON 裡，語言切換器由 `build.py` 自動產生。
- **電話**：`"tel:+8613632665441"`（顯示字串另存於 `common.site.phone`）。
- 錨點 `#service-relocation` 等**語言不變**，四個語言的頁面錨點相同。

---

## 4. `common.json`

```jsonc
{
  "site": {
    "name":          "倍特爾科技集團",                              // 短名（header 用）
    "legal_name":    "倍特爾科技集團有限公司",                       // 完整法定名稱（footer）
    "legal_name_en": "BETTER SCIENCE TECHNOLOGY GROUP CO., LIMITED", // 語言不變
    "address":       "香港九龍佐敦佐敦道5號至秀商業大廈10樓",
    "email":         "Masuhiro@bettertechgroup.com",                  // 語言不變
    "phone":         "+86-136-3266-5441",                           // 語言不變（顯示字串）
    "phone_href":    "tel:+8613632665441",                           // 語言不變（連結）
    "copyright_year":"2026"                                         // 語言不變
  },

  "brand": {                       // header 左上角
    "logo": "assets/img/logo-96.png",   // 語言不變
    "logo_alt": "倍特爾科技集團有限公司",
    "name_primary":   "倍特爾科技集團",              // 主行
    "name_secondary": "Better Science Technology Group" // 副行（小字、大寫）
  },

  "languages": {                   // label 語言不變（繁/简/EN/日）；name 各語言自譯
    "zh-hant": { "label": "繁",  "name": "繁體中文" },
    "zh-hans": { "label": "简",  "name": "簡體中文" },
    "en":      { "label": "EN",  "name": "English"  },
    "ja":      { "label": "日",  "name": "日本語"   }
  },
  "shell": {                       // 站台外殼頁（dist/index.html 語言閘道、dist/404.html）
    "not_found":       "找不到此頁面",          // 404 的 <h1>，四語並列
    "language_nav":    "語言版本",              // 404 語言清單的 <nav aria-label>（取 zh-hant 那份）
    "gateway_note":    "請選擇語言版本",        // 閘道底部說明，四語並列（無 JS 時不轉頁，須是祈使句）
    "back_to_gateway": "回到語言選擇"           // 404 底部回到閘道的連結，四語並列
  },

  "lang_switcher": { "aria_label": "語言選擇" },

  "a11y": {
    "skip_link": "跳至主要內容",
    "nav_label": "主要導覽",
    "breadcrumb_label": "麵包屑",
    "nav_open": "開啟主選單",
    "nav_close": "關閉主選單"
  },

  "media_ctrl": {                  // 影片暫停／播放鈕
    "pause": "暫停影片", "play": "播放影片",
    "pause_aria": "暫停背景影片", "play_aria": "播放背景影片"
  },

  "nav": {
    "entries": [                   // 順序固定，六項，href 語言不變
      { "label": "首頁",      "href": "index.html",     "match": "" },
      { "label": "關於我們",  "href": "about.html",     "match": "" },
      { "label": "服務項目",  "href": "services.html",  "match": "" },
      { "label": "設備與製程","href": "equipment.html",
        "match": "equipment.html equipment-lithography.html equipment-etch.html equipment-cvd.html equipment-bake.html equipment-implant.html equipment-cmp.html equipment-cleaning.html equipment-inspection.html equipment-mask.html" },
      { "label": "AI 智慧製造","href": "ai.html",       "match": "" },
      { "label": "聯絡我們",  "href": "contact.html",   "match": "" }
    ],
    "cta":        { "label": "洽詢設備",      "href": "contact.html" }, // header 右側按鈕
    "mobile_cta": { "label": "洽詢設備與服務","href": "contact.html" }  // 行動選單底部按鈕
  },

  "footer": {
    "brand_primary":   "倍特爾科技集團有限公司",
    "brand_secondary": "BETTER SCIENCE TECHNOLOGY GROUP CO., LIMITED",
    "desc":  "先進半導體製程設備採購、拆裝運送、技術導入與 AI 整合。",
    "nav_title": "網站導覽", "process_title": "九大製程", "contact_title": "聯絡方式",
    "labels": { "address": "地址：", "email": "電郵：", "phone": "電話：" },
    // labels 三個抬頭同時供 footer 聯絡欄、about 總部區塊與 contact 側欄卡使用
    "process_links": [ { "label": "黃光段", "href": "equipment-lithography.html" }, … 共 9 項 ],
    "copyright": "© 2026 倍特爾科技集團有限公司 BETTER SCIENCE TECHNOLOGY GROUP CO., LIMITED. 版權所有。",
    "trademark_note": "本網站所列品牌名稱均為其各自所有權人之商標，僅供設備說明用途。"
  },

  "cta_band": {                    // 每頁最底的共用聯絡條
    "eyebrow": "GET IN TOUCH",
    "title":   "與我們談談您的產線需求",
    "lead":    "從設備選型到裝機與 AI 導入，提供單一窗口。",
    "primary":   { "label": "洽詢設備與服務", "href": "contact.html" },
    "secondary": { "label": "Masuhiro@bettertechgroup.com", "href": "mailto:Masuhiro@bettertechgroup.com" }
  },

  "shared_cta": {                  // 內頁重複出現的按鈕文案
    "primary":  { "label": "洽詢設備與服務", "href": "contact.html" },
    "secondary":{ "label": "瀏覽九大製程",   "href": "equipment.html" },
    "ai":       { "label": "了解 AI 智慧製造","href": "ai.html" },
    "services": { "label": "查看服務項目",   "href": "services.html" },
    "process_page": { "label": "索取設備與服務說明", "href": "contact.html" }
  },

  "pager": {                       // 製程頁上一段／下一段的固定標籤
    "prev_label": "上一段製程", "next_label": "下一段製程", "aria_label": "製程頁導覽"
  },

  "form": {                        // 只有 contact.html 用；字串由 main.js 讀 data-* 取得
    "mailto": "Masuhiro@bettertechgroup.com",             // 語言不變
    "required_mark_aria": "必填",
    "fields": {                    // 六個欄位，鍵名固定（= <input name>）
      "name":     { "label": "姓名",    "placeholder": "請輸入您的姓名" },
      "company":  { "label": "公司",    "placeholder": "公司或機構名稱" },
      "email":    { "label": "Email",   "placeholder": "your@company.com" },
      "phone":    { "label": "電話",    "placeholder": "含國碼，例如 +852" },
      "category": { "label": "需求類別","placeholder": "請選擇需求類別" },
      "message":  { "label": "訊息",    "placeholder": "請簡述製程段、設備需求與時程" }
    },
    "categories": ["設備採購","拆裝運送","製程技術導入","人才培訓","AI 整合","其他"], // 6 項
    "submit": "送出詢問",
    "hint": "送出後將開啟您的郵件軟體，內容已預先填入，請確認後寄出。",
    "messages": { "required": "此欄位為必填。", "select": "請選擇需求類別。",
                  "email": "請輸入正確的電子郵件格式。" },
    "mail": {                      // 組進 mailto 內文的欄位抬頭
      "subject_prefix": "網站詢問",
      "subject_sep": "｜",           // 主旨欄位之間的分隔符（en 為 " | "）
      "sep": "：",                   // 內文「抬頭 + 值」之間的分隔符（en 為 ": "）
      "name": "姓名", "company": "公司", "email": "Email",
      "phone": "電話", "category": "需求類別", "message": "訊息"
    }
  }
}
```

---

## 5. 每頁共通的前兩個欄位

所有頁面 JSON 都以這兩個欄位開頭：

```jsonc
"meta": {
  "title":       "先進半導體設備採購與 AI 整合｜倍特爾科技集團",  // <title>
  "description": "倍特爾科技集團為香港半導體設備服務商，…"        // <meta name=description>
},
"breadcrumb": [                       // index.json 為空陣列 []
  { "label": "首頁",       "href": "index.html" },
  { "label": "設備與製程", "href": "equipment.html" },
  { "label": "黃光段" }               // 最後一項不可有 href
]
```

`hero` 區塊（首頁以外一律是亮帶 hero）：

```jsonc
"hero": { "eyebrow": "ABOUT US", "title": "關於倍特爾", "lead": "一句導言。" }
```

---

## 6. `index.json`（已完成，可作為範例）

實檔見 `content/zh-hant/index.json`。區塊順序與欄位：

| 欄位 | 內容 |
|---|---|
| `meta` / `breadcrumb`（空陣列） | 見 §5 |
| `hero` | `eyebrow`、`title_lines[2]`（每行一個 `<span class="nb">`，避免不當斷行）、`lead`、`sub`、`primary{label,href}`、`secondary{label,href}`、`media`（VID-HOME-01） |
| `stats` | `aria_label`、`entries[3]{num,label}`（`num` 語言不變） |
| `pillars` | `eyebrow`、`title`、`lead`、`entries[5]{num,title,text,link_label,href}`、`media`（IMG-HOME-01） |
| `processes` | `eyebrow`、`title`、`lead`、`overview_link{label,href}`、`media`（IMG-HOME-02）、`entries[9]{num,title,en,text,brands[],link_label,href}`、`brand_note` |
| `ai` | `eyebrow`、`title`、`lead`、`paragraphs[2]`、`cta{label,href}`、`media`（IMG-HOME-03）、`pillars[3]{title,title_lat,text}`、`table{scroll_label,caption,columns[3],rows[3]{model,metric,process},note}` |
| `why` | `eyebrow`、`title`、`lead`、`media`（IMG-HOME-04）、`entries[4]{title,text}` |

> `ai.pillars[2].title` 是空字串 `""`（該卡只有拉丁標題 `LithoDreamer / ILT`）。
> 四個語言都必須保留這個空字串，不可補字。

---

## 7. `about.json`

```jsonc
{
  "meta": { … }, "breadcrumb": [ … ],
  "hero": { "eyebrow": "ABOUT BETTER", "title": "…", "lead": "…" },

  "intro": {                                   // #company-intro（media 為 null 時單欄；有 media 時 split 7-5，圖在右）
    "eyebrow": "…", "title": "…", "lead": "",  // 本頁各區塊皆無 lead，四語一律空字串
    "paragraphs": ["…", "…", "…", "…"],        // <div class="prose"> 內的段落
    "features_label": "服務對象",               // 清單上方的 <p class="small muted">
    "features": ["…", "…", "…", "…"],          // <ul class="feature-list">
    "media": null                              // 選填，沒有時寫 null（四語一致，見 §2 media object）
  },

  "mission": {                                 // #mission-vision（split 5-7，圖在左）
    "eyebrow": "…", "title": "…", "lead": "",
    "entries": [                               // <dl class="def-list">，2 項
      { "term": "使命：…", "desc": "…" },       // term → <dt>，desc → <dd>
      { "term": "願景：…", "desc": "…" }
    ],
    "media": { … }                             // IMG-ABOUT-02，ratio 4-3
  },

  "leadership": {                              // #leadership
    "eyebrow": "…", "title": "…", "lead": "",
    "paragraphs": ["…"],
    "card": { "title": "蘇益宏（Kerwin）",      // 姓名
              "role": "公司負責人",             // <p class="small muted">
              "text": "…" }                    // 職責描述
    // 本卡是「公司治理」資訊，不是聯絡方式：卡片內不放 email／電話
  },

  "scope": {                                   // #business-scope
    "eyebrow": "…", "title": "…", "lead": "",
    "features": ["…"]                          // feature-list--3，6 項
    // 下方的 arrow-link 取自 common.shared_cta.services
  },

  "our_values": {                              // #values（核心價值）
    "eyebrow": "…", "title": "…", "lead": "",
    "entries": [ { "title": "…", "text": "…" } ],   // 卡片格線，3 張
    "media": { … }                             // IMG-ABOUT-04，ratio 16-9
  },

  "headquarters": {                            // #headquarters
    "eyebrow": "…", "title": "…", "lead": "",
    "media": { … }                             // IMG-ABOUT-03，ratio 21-9
    // 名稱／英文名／地址／電郵四行直接取自 common.site，不重複寫在本檔
  }
}
```

> 鍵名為什麼是 `our_values` 而不是 `values`：`values` 是 Python dict 的方法名，
> Jinja 的 `page.values` 會取到方法而不是資料（見 §1 保留字）。

## 8. `services.json`

```jsonc
{
  "meta": { … }, "breadcrumb": [ … ],
  "hero": { "eyebrow": "SERVICES", "title": "…", "lead": "…" },

  "banner_label": "服務項目主視覺",              // 主視覺 section 的 aria-label
  "banner_media": { … },                       // IMG-SVC-01，ratio 21-9

  "labels": {                                  // 五個服務區塊共用的三個 <h3>
    "features": "涵蓋範圍", "steps": "服務方式", "outcomes": "交付項目"
  },

  "services": [                                // 恰好 5 項，順序固定
    {
      "id": "service-equipment",               // 語言不變（= section id / 錨點）
      "eyebrow": "01 / PROCUREMENT",           // 編號 + 英文，各語言沿用
      "title": "…", "lead": "…",
      "features": ["…"],                       // 左欄：涵蓋範圍
      "steps": [                               // 右欄：服務方式（4 步）
        { "num": "01", "title": "…", "text": "…" }
      ],
      "outcomes": ["…"],                       // feature-list--3：交付項目

      "note": {                                // 選填，沒有時寫 null（四語一致）
        "before": "…相關製程請見",               // 連結前的文字
        "link": { "label": "設備與製程總覽", "href": "equipment.html" },
        "after": "。"                           // 連結後的文字
      },
      "media": null,                           // 選填，只有 service-ai 有（IMG-SVC-02，16-9）
      "cta": null                              // 選填，只有 service-ai 有（arrow-link → ai.html）
    }
    // service-relocation / service-process / service-training / service-ai
  ],

  "flow": {                                    // #service-flow
    "eyebrow": "…", "title": "…", "lead": "…",
    "steps": [ { "num": "01", "title": "…", "text": "…" } ],   // 6 步
    "media": { … }                             // IMG-SVC-04，ratio 3-4
  },

  "closing_media": { … }                       // IMG-SVC-03，ratio 21-9
}
```

> 區塊底色由順序決定（第 1／3／5 個 `section--line`、第 2／4 個 `section--alt`），
> 由模板計算，不寫在 JSON 裡。`note`／`media`／`cta` 為 `null` 的項目，
> 其他語言也必須是 `null`。

## 9. `equipment.json`（總覽頁）

```jsonc
{
  "meta": { … }, "breadcrumb": [ … ],
  "hero": { "eyebrow": "EQUIPMENT & PROCESS", "title": "…", "lead": "…" },
  "banner_label": "設備列照片",                 // 橫幅媒體區塊的 <section aria-label>
  "banner_media": { … },                       // ratio 16-9

  "flow": {                                    // #process-flow
    "eyebrow": "…", "title": "…", "lead": "",  // 本頁 lead 為空字串（原型無 lead）
    "paragraphs": ["…"],
    "media": { … }                             // ratio 4-3
  },

  "processes": {                               // #process-cards
    "eyebrow": "…", "title": "…", "lead": "…",
    "entries": [                               // 9 項，與 index.json 的製程卡同結構
      { "num": "01", "title": "黃光段", "en": "Lithography", "text": "…",
        "brands": ["NIKON","CANON","TEL","DNS"],
        "link_label": "查看設備", "href": "equipment-lithography.html" }
    ],
    "brand_note": "…"
  },

  "gallery_media": { … },                      // ratio 21-9

  "services": {                                // #equipment-services
    "eyebrow": "…", "title": "…", "lead": "",  // 本頁 lead 為空字串
    "features": ["…"]                          // feature-list--3
  }
}
```

> `lead` 為空字串 `""` 時，`section_header` 巨集不會輸出 `<p class="lead">`。
> 四個語言都必須保留這個空字串（結構一致性檢查會比對鍵，不可刪鍵）。
> 清單下方的 `查看服務項目 →` 取自 `common.shared_cta.services`，不寫在本檔。

---

## 10. `equipment-<area>.json`（九個製程頁共用 `equipment-detail.html`）

`<area>` ∈ `lithography, etch, cvd, bake, implant, cmp, cleaning, inspection, mask`。

```jsonc
{
  "meta": { … },
  "breadcrumb": [
    { "label": "首頁", "href": "index.html" },
    { "label": "設備與製程", "href": "equipment.html" },
    { "label": "黃光段" }
  ],

  "hero": {
    "id": "litho-hero",                        // 區塊錨點，語言不變（黃光段是 litho-，其餘同 <area>）
    "eyebrow": "LITHOGRAPHY",                  // 大寫英文，語言不變
    "title": "黃光段設備",
    "title_lat": "Lithography",                // 語言不變（<p class="lat muted small">）
    "lead": "曝光與旋塗顯影，決定線寬、對準與圖形保真度。"
  },
  "banner_label": "黃光區照片",                 // 橫幅媒體區塊的 <section aria-label>
  "banner_media": { … },                       // IMG-LITHO-01，ratio 16-9

  "scope": {
    "id": "litho-scope",                       // 語言不變
    "eyebrow": "…", "title": "設備範圍", "lead": "",
    "features": [                              // 品牌／機種清單；品牌名不翻譯
      "NIKON 全系列曝光機產品",
      "CANON 全系列曝光機產品，包含奈米壓印設備"
    ],
    "paragraphs": ["以日系主力品牌為主，涵蓋…"],  // 清單下方的 <p class="mt-6">
    "media": { … }                             // IMG-LITHO-02，ratio 4-3
  },

  "services": {
    "id": "litho-services",                    // 語言不變
    "eyebrow": "…", "title": "…", "lead": "",
    "features": ["…"]                          // feature-list--3
  },

  "ai": {
    "id": "litho-ai",                          // 語言不變
    "eyebrow": "AI INTEGRATION", "title": "AI 整合",
    "lead": "以下為倍特爾對標導入的第三方前沿架構。",
    "entries": [                               // card--ai：多數頁 3 張；mask 4 張、inspection 6 張
      {
        "arch": "LithoDreamer 生成式微影／ILT", // 架構名保留原文，說明可譯
        "year": "",                            // 有年份／會議時填「（ASP-DAC'26）」，含括號
        "arch_note": "",                       // 年份之後的補充（如「ViT（DINOv2）＋半監督」），無則空字串
        "text": "…",
        "metric": "對標指標：以生成式方法縮短微影修正迭代",
        "tag": "對標／導入之前沿架構"
      }
    ],
    "media": { … }                             // IMG-LITHO-03，ratio 16-9
  },

  "fit": {
    "id": "litho-fit",                         // 語言不變
    "eyebrow": "…", "title": "…", "lead": "",
    "features": ["…"]                          // feature-list--3
  },

  "pager": {                                   // 標籤取自 common.pager
    "prev": { "href": "equipment-mask.html", "title": "掩模版製程" },
    "next": { "href": "equipment-etch.html", "title": "蝕刻段" }
  }
}
```

九頁的 `pager` 首尾相接（mask → lithography → etch → cvd → bake → implant → cmp →
cleaning → inspection → mask），`href` 語言不變。

補充規則：

- 九頁共用一個模板，因此**區塊錨點必須寫在 JSON 裡**：`hero`／`scope`／`services`／
  `ai`／`fit` 各有一個 `id`。鍵名是 `id`，已列入 `build.py` 的 `INVARIANT_KEYS`，
  四種語言必須逐字相同。黃光段的前綴是 `litho-`，其餘八頁等於 `<area>-`。
- `scope`／`services`／`fit` 的 `lead` 為空字串 `""`（原型這三段只有 eyebrow ＋ h2）。
  各語言一律保留空字串，不可刪鍵、也不可補字。
- `ai.entries[].arch_note` 對應原型 `<p class="card__arch">架構名 <span class="card__year">（年份）</span> 補充</p>`
  最後那段補充文字（例：`ViT（DINOv2）＋半監督`、`XGBoost＋PCA`、`貝氏 PINN 思路`）。
  `year` 為空字串時 `arch_note` 也必須是空字串。
- `ai.entries` 的長度**逐頁不同**（多數 3 張、`mask` 4 張、`inspection` 6 張），
  但同一頁的四個語言必須相同。版型固定 `grid grid--3`，第 4／7 張自動換行。
- 頁面最底的 CTA 帶主按鈕取自 `common.shared_cta.process_page`（「索取設備與服務說明」），
  其餘文字取自 `common.cta_band`，不寫在本檔。
- `ai.eyebrow` 九頁一律為 `AI INTEGRATION`（依 `docs/content-spec.md` §5.4）。
  第一階段原型有四頁誤植為 `AI Integration`；`.eyebrow` 由 CSS `text-transform:uppercase`
  呈現，畫面完全相同，JSON 一律採母本的大寫寫法。

---

## 11. `ai.json`

```jsonc
{
  "meta": { … }, "breadcrumb": [ … ],

  "hero": {                                    // 亮帶 hero + 右側影片（無 paragraphs）
    "eyebrow": "AI × ADVANCED MANUFACTURING", "title": "…", "lead": "…",
    "media": { … }                             // VID-AI-01，ratio 16-9
  },

  "positioning": {                             // #ai-positioning
    "eyebrow": "…", "title": "…", "lead": "",  // 本段 lead 為空字串
    "paragraphs": ["…", "…", "…"],             // 包在 <div class="stack-4"> 內，共 3 段
    "media": { … }                             // ratio 4-3
  },

  "pillars": {                                 // #ai-pillars：三大主軸
    "eyebrow": "…", "title": "…", "lead": "…",
    "entries": [
      { "title": "數字孿生", "title_lat": "Digital Twin",   // title_lat 語言不變
        "text": "…", "meta": "典型應用：條件變更預演、維護排程、移機後復機驗證" }
    ],
    "media": { … }                             // ratio 21-9
  },

  "benchmarks": {                              // #ai-benchmark-table
    "eyebrow": "…", "title": "…", "lead": "…",
    "table": {
      "scroll_label": "…可左右捲動",           // .table-scroll 的 aria-label
      "caption": "…",                          // <caption class="visually-hidden">
      "columns": ["領域", "代表模型（年份）", "核心架構",   // 6 欄，順序固定
                  "輸入數據特徵", "輸出／評估指標", "關鍵量化結果"],
      "rows": [ { "domain": "熱模擬代理",                  // <th scope="row">
                  "model":  "DeepOHeat-v1（2025）",        // <td class="model">
                  "arch":   "DeepONet＋KAN＋GMRES 細化",
                  "inputs": "功耗圖／floorplan（物理資訊訓練，無需模擬資料）",
                  "metrics": "MAPE、訓練時間、記憶體",
                  "result": "MAPE 0.035%、訓練-62×、記憶體-31×" } ],  // <td class="num">，21 列
      "note": "資料來源為第三方公開發表之研究與產業資訊，倍特爾以其作為導入對標基準。"
    }
  },

  "matrix": {                                  // #ai-process-matrix：製程 × AI
    "eyebrow": "…", "title": "…", "lead": "…",
    "table": {
      "scroll_label": "…", "caption": "…",
      "columns": ["製程", "主要對標架構", "導入重點"],
      "rows": [ { "process_label": "黃光段",
                  "process_href": "equipment-lithography.html",  // 語言不變
                  "arch": "LithoDreamer／ILT、可解釋 GAT（ASP-DAC'26）",
                  "focus": "光罩圖形生成修正、佈局熱點預測、軌道數字孿生" } ]  // 9 列
    }
  },

  "delivery": {                                // #ai-delivery：導入流程
    "eyebrow": "…", "title": "…", "lead": "…",
    "steps": [ { "num": "01", "title": "…", "text": "…" } ],   // 5 步
    "media": { … }                             // ratio 4-3
  },

  "cta": {                                     // 只覆寫 CTA 帶的主按鈕，其餘取自 common.cta_band
    "primary": { "label": "討論 AI 導入場景", "href": "contact.html" }
  }
}
```

> `benchmarks.table.rows` 共 **21 列**、`matrix.table.rows` 共 **9 列**，
> 順序與 `docs/content-spec.md` §14.4／§14.5 完全一致，不可增刪或重排。
> 架構名、模型名、年份與量化數字一律沿用原文，只翻譯周圍的中文說明；
> `note` 必須譯出「第三方公開發表、作為導入與對標基準」的語意。

---

## 12. `contact.json`

```jsonc
{
  "meta": { … }, "breadcrumb": [ … ],
  "hero": { "eyebrow": "CONTACT", "title": "…", "lead": "…" },

  "info": {                                    // #contact-info：聯絡資訊列（.info-strip，三格）
    "eyebrow": "…", "title": "…", "lead": "",  // 本區無 lead，四語一律空字串
    "entries": [
      { "title": "電子郵件", "text": "Masuhiro@bettertechgroup.com", "variant": "mailto" },
      { "title": "電話",     "text": "+86-136-3266-5441",           "variant": "tel" },
      { "title": "公司地址", "text": "香港九龍…",                    "variant": "keep" }
    ],
    // variant 語言不變：
    //   "keep"   → <p class="info-strip__value contact-card__value--keep">（CJK 不亂斷行）
    //   "mailto" → <a class="link contact-card__value--nowrap" href="mailto:{text}">
    //   "tel"    → <a class="link contact-card__value--nowrap" href="{common.site.phone_href}">
    //   （mailto 的 text 即信箱本身；tel 的 text 是顯示號碼，連結另取 common.site.phone_href）
    "media": { … }                             // IMG-CONTACT-02，ratio 21-9
  },

  "enquiry": {                                 // #enquiry-form；表單字串一律取自 common.form
    "eyebrow": "…", "title": "…", "lead": "…",
    "aside_label": "其他聯絡方式",               // <aside> 的 aria-label
    "side_card":  { "title": "…", "text": "…" },
                    // 卡片最下方的「電郵／電話」兩行取自 common.site.email／phone
                    // 與 common.footer.labels，不重複寫在本檔
    "side_notes": { "title": "…",
                    "entries": [ { "label": "…", "href": "services.html" } ] }  // href 語言不變
  },

  "location": {                                // #contact-location
    "eyebrow": "…", "title": "…", "lead": "",
    "paragraphs": ["…"],
    "media": { … }                             // IMG-CONTACT-01，ratio 21-9
  },

  "divider_media": { … }                       // IMG-CONTACT-03，ratio 21-9，decorative: true
                                               // 接在 location 段末，不另開區塊
}
```

> 表單本身（欄位、選項、驗證訊息、mailto 內文抬頭與分隔符）完全來自 `common.form`；
> 模板會把這些字串輸出成 `<form>` 上的 `data-*` 屬性供 `main.js` 讀取。
> `<input>` 的 `name` 固定為 `name / company / email / phone / category / message`
> （`main.js` 以 `form.elements[name]` 取值）；`id` 一律加 `f-` 前綴
> （`f-name`、`f-company`…），避免 `id` 與 `name` 在 `form.elements` 上互相覆蓋。

## 13. 各語言的專屬規則

| | zh-hant（母本） | zh-hans | en | ja |
|---|---|---|---|---|
| `html lang` | `zh-Hant-HK` | `zh-Hans-CN` | `en` | `ja` |
| 公司主名稱 | 倍特爾科技集團 | 倍特尔科技集团 | BETTER SCIENCE TECHNOLOGY GROUP CO., LIMITED | BETTER SCIENCE TECHNOLOGY GROUP CO., LIMITED |
| 副行 | Better Science Technology Group | Better Science Technology Group | 倍特爾科技集團有限公司 | 倍特爾科技集團有限公司 |
| footer 法定名稱 | 倍特爾科技集團有限公司 + 英文名 | 倍特尔科技集团有限公司 + 英文名 | 英文名 + 倍特爾科技集團有限公司 | 英文名 + 倍特爾科技集團有限公司 |
| 地址 | 香港九龍佐敦佐敦道5號至秀商業大廈10樓 | 香港九龙佐敦佐敦道5号至秀商业大厦10楼 | 10/F, Chi Sau Commercial Building, 5 Jordan Road, Jordan, Kowloon, Hong Kong | （同 en 的英文地址） |
| 電話抬頭 | 電話： | 电话： | Phone: | 電話： |
| 標點 | 全形，。、：「」（） | 全形，。、：“”（） | 半形 , . : " " ( ) | 全形 、。「」（） |

- **日文不得自創片假名公司名**；一律使用英文法定名稱。
- **簡體版必須用大陸業界術語**，不是繁簡字元轉換。對照範例：
  黃光段→光刻，蝕刻→刻蝕，掩模版→掩膜版／光罩，晶圓水洗→晶圓清洗，
  離子植入→離子注入，物理仿真→物理仿真（同），數字孿生→數字孿生（同），
  稼動→稼動率／設備綜合效率，良率→良率（同），機台→設備。
- **英文版**內文行高為 1.6（`html[lang^="en"]` 已在 `style.css` 設定），不需要在 JSON 處理。

---

## 14. 交付前自檢

```bash
python build.py --validate-only     # 只檢查結構與資產命名，不寫檔
python build.py --lang ja           # 只重建單一語言
python build.py --clean             # 全部重建
```

- 結構不符會印出**第一個**不符的完整路徑，例如
  `[ja] 結構與 zh-hant 不符 → services.services[2].steps：list 長度不同（zh-hant=4，ja=3）`
- 語言不變欄位被改動會一次列出全部，例如
  `[en] common.nav.entries[1].href：zh-hant='about.html' 但 en='about-us.html'`
- 通過後以 `python -m http.server -d dist 8000` 逐頁目視檢查，並對照
  `docs/components.md §21`（上線前自檢）與 `DESIGN.md §10`（無障礙檢查表）。
