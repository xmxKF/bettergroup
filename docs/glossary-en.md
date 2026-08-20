# glossary-en.md — 中英對照術語表（English）

> 供 `content/en/*.json` 的翻譯者使用。第三階段補其餘 14 頁時，**一律沿用本表用語**，
> 不得自創同義詞。母本為 `docs/content-spec.md`；結構規範見 `docs/content-schema.md`。
> 已完成並可作範例的檔案：`content/en/common.json`、`content/en/index.json`。

## 0. 通用書寫規則（English）

| 項目 | 規則 |
|---|---|
| 拼寫 | **美式英文**（planarization, vapor, utilization, program, behavior, optimization）。業界術語以美式為準。 |
| 詢問／洽詢 | 一律 **inquiry / inquire**（不用 enquiry）。 |
| 標題大小寫 | H1／H2／H3 用 **sentence case**；導覽列、按鈕、footer 欄標題用 **Title Case**。 |
| 標點 | 半形 `, . : ( ) " "`；不使用驚嘆號。 |
| 品牌名 | **永不翻譯**，大寫原樣：NIKON, CANON, TEL, DNS, SAMCO, KOKUSAI ELECTRIC (KE), MATSUSHITA, TAZMO, ULVAC, NISSIN, EBARA, ACCRETECH, ADVANTEST, LASERTEC, NUFLARE, JEOL。 |
| 公司自稱 | 內文短名一律 **BETTER**（不用 "Better"、"the Company"、"we at BETTER"）。 |
| AI 成果 | 一律寫成 *benchmark / reference architecture*，永遠不可寫成 BETTER 自有量測結果。 |
| eyebrow 標籤 | 原始 JSON 已是英文且**一律大寫**（`WHAT WE DO`、`NINE PROCESS AREAS`…，見 `docs/content-spec.md`），**原樣保留**；四語言相同，唯一例外是 `ENQUIRY` 在英文版寫 `INQUIRY`。 |
| 標題長度 | hero／section 標題 ≤ 6–8 字；hero `title_lines` 每行 ≤ 19 字元（含空格），否則會溢出。 |

---

## 1. 公司、地址與聯絡（common.json → site / brand / footer）

| zh-Hant | English |
|---|---|
| 倍特爾科技集團有限公司 | BETTER SCIENCE TECHNOLOGY GROUP CO., LIMITED |
| 倍特爾科技集團（header 短名） | BETTER（header 品牌鎖定字；full name 只出現在 footer） |
| 倍特爾（內文簡稱） | BETTER |
| 副行（header brand__en） | 倍特爾科技集團有限公司（英文版副行放中文法定名） |
| 香港九龍佐敦佐敦道5號至秀商業大廈10樓 | 10/F, Chi Sau Commercial Building, 5 Jordan Road, Jordan, Kowloon, Hong Kong |
| （已移除：原「公司負責人」姓名對照列，about 頁該卡已移除） | — |
| +86-135-3007-1950 | （不譯，逐字沿用；連結 `tel:+8613530071950`） |
| 地址： | `"Address: "`（字串結尾保留一個半形空白） |
| 電郵： | `"Email: "` |
| 電話： | `"Phone: "` |
| 網站導覽（footer 欄標題） | Site Map |
| 九大製程（footer 欄標題） | Nine Process Areas |
| 聯絡方式（footer 欄標題） | Contact |
| © 2026 …版權所有。 | © 2026 BETTER SCIENCE TECHNOLOGY GROUP CO., LIMITED 倍特爾科技集團有限公司. All rights reserved. |
| 本網站所列品牌名稱均為其各自所有權人之商標，僅供設備說明用途。 | All brand names shown on this site are trademarks of their respective owners and are used for equipment identification only. |
| 網站設計：顯藝科技（footer.credit，`href` 留空） | Website by 顯藝科技（footer.credit；company name not translated, no invented English name） |
| 先進半導體製程設備採購、拆裝運送、技術導入與 AI 整合。 | Procurement, de-installation and shipping, process technology transfer and AI integration for advanced semiconductor equipment. |

## 2. 導覽與介面字串（common.json → nav / a11y / media_ctrl / pager）

| zh-Hant | English |
|---|---|
| 首頁 | Home |
| 關於我們 | About |
| 服務項目 | Services |
| 設備與製程 | Equipment & Processes |
| AI 智慧製造 | AI Manufacturing |
| 聯絡我們 | Contact |
| 跳至主要內容 | Skip to main content |
| 主要導覽 | Main navigation |
| 麵包屑 | Breadcrumb |
| 開啟主選單／關閉主選單 | Open main menu / Close main menu |
| 語言選擇 | Language |
| 繁體中文／簡體中文／English／日本語 | Traditional Chinese / Simplified Chinese / English / Japanese |
| 暫停影片／播放影片 | Pause / Play |
| 暫停背景影片／播放背景影片 | Pause background video / Play background video |
| 上一段製程／下一段製程 | Previous process / Next process |
| 製程頁導覽 | Process navigation |
| 可左右捲動 | scrollable horizontally |

## 3. CTA 與按鈕（common.json → nav.cta / cta_band / shared_cta）

| zh-Hant | English |
|---|---|
| 洽詢設備（header 按鈕） | Inquire |
| 洽詢設備與服務 | Send an Inquiry |
| 瀏覽九大製程 | Explore Nine Process Areas |
| 了解 AI 智慧製造 | Discover AI Manufacturing |
| 查看服務項目 | View Our Services |
| 索取設備與服務說明 | Request Equipment Details |
| 查看設備與製程總覽 | View equipment and process overview |
| 查看設備（製程卡） | View equipment |
| 設備與製程（卡片連結） | Equipment & Processes |
| 服務內容（卡片連結） | Service details |
| 與我們談談您的產線需求 | Let's talk about your line |
| 從設備選型到裝機與 AI 導入，提供單一窗口。 | One point of contact from equipment selection through installation and AI integration. |

## 4. 五大核心業務（index / services）

| zh-Hant | English |
|---|---|
| 五大核心業務 | Five core business lines |
| 九大主製程設備採購 | Equipment for nine process areas |
| 設備採購與銷售 | Equipment procurement and sales |
| 拆裝機及運送服務 | De-installation, shipping and installation |
| 先進製程技術導入 | Advanced process technology transfer |
| 先進半導體人才培訓 | Semiconductor talent training |
| AI 與先進製造整合 | AI and advanced manufacturing |
| 五大服務，一個窗口 | Five services, one point of contact |

## 5. 九大製程（index.processes / equipment / footer）

`en` 欄位是**語言不變**的拉丁副標，不可更動；`title` 欄位（卡片 h3）必須與它**不同字**，
否則卡片會出現同字重複。以下為定案配對，footer 連結沿用 `title` 欄。

| # | zh-Hant | `title`（h3／footer） | `en`（語言不變副標） |
|---|---|---|---|
| 01 | 黃光段 | Photolithography | Lithography |
| 02 | 蝕刻段 | Dry & Plasma Etch | Etch |
| 03 | 化學氣相沉積 | CVD | Chemical Vapor Deposition |
| 04 | 烘烤製程 | Bake & Thermal | Thermal / Bake |
| 05 | 離子植入 | Ion Implant | Ion Implantation |
| 06 | CMP 研磨 | CMP | Chemical Mechanical Polishing |
| 07 | 晶圓水洗 | Wafer Clean & Dry | Wafer Cleaning |
| 08 | 晶圓檢測 | Inspection & Test | Wafer Inspection & Test |
| 09 | 掩模版製程 | Photomask | Mask / Reticle |

製程頁 h1（`equipment-<area>.html`）用 `<title> equipment`：Photolithography equipment、
Dry & plasma etch equipment、CVD equipment、Bake & thermal equipment、Ion implant equipment、
CMP equipment、Wafer clean & dry equipment、Inspection & test equipment、Photomask equipment。

## 6. 製程與設備術語

| zh-Hant | English |
|---|---|
| 製程／製程段 | process / process area |
| 主製程 | main process area |
| 機台 | tool（複數 tools；避免 machine） |
| 設備 | equipment |
| 曝光機 | exposure tool（steppers and scanners） |
| 奈米壓印 | nanoimprint |
| 旋塗與顯影設備／塗佈顯影機 | coat and develop tracks |
| 乾式蝕刻／電漿蝕刻 | dry etch / plasma etch |
| 薄膜沉積 | thin-film deposition |
| 爐管／熱盤 | furnace / hot plate |
| 熱預算 | thermal budget |
| 摻雜 | dopant / doping |
| 平坦化／減薄 | planarization / thinning |
| 清洗與乾燥 | cleaning and drying |
| 量測 | metrology |
| 缺陷檢測 | defect inspection |
| 電性測試 | electrical test |
| 電子束寫入機 | e-beam writer |
| 掩模版／光罩 | photomask / reticle |
| 線寬 | linewidth |
| 關鍵尺寸 | critical dimension (CD) |
| 側壁形貌 | sidewall profile |
| 膜厚均勻度 | thickness uniformity |
| 階梯覆蓋 | step coverage |
| 圖形精度／圖形保真度 | pattern fidelity |
| 良率 | yield |
| 稼動／稼動率 | tool utilization |
| 潔淨室／無塵室 | cleanroom |
| 晶圓傳輸機械手臂 | wafer transfer robot |
| 設備艙門 | load port |
| 試片／試跑 | test wafer / trial run |
| 爬坡期 | ramp（shorten the ramp） |
| 量產轉換 | conversion to volume production |

## 7. 服務流程與交付（services.json）

| zh-Hant | English |
|---|---|
| 涵蓋範圍 | Scope of work |
| 服務方式（步驟） | How we work |
| 交付項目 | Deliverables |
| 標準服務流程 | Our standard service flow |
| 諮詢 | Consultation |
| 評估選型 | Evaluation and selection |
| 採購／驗機 | Procurement and acceptance |
| 拆機／包裝／運送 | De-installation, packing and shipping |
| 安裝／調試 | Installation and tuning |
| 培訓／維護 | Training and maintenance |
| 需求釐清 | Requirement definition |
| 機種提案 | Tool proposal |
| 商務執行 | Commercial execution |
| 驗機交付 | Acceptance and handover |
| 現場勘查 | Site survey |
| 移機計畫 | Relocation plan |
| 防震防潮包裝 | Shock- and moisture-protected packing |
| 跨境運送 | Cross-border shipping |
| 進場定位 | Move-in and positioning |
| 復裝 | Reinstallation |
| 調試 | Tuning and commissioning |
| 到場驗收 | On-site acceptance |
| 製程條件建立 | Process condition setup |
| 參數視窗 | Parameter window |
| 重現性驗證 | Repeatability verification |
| 跨機台一致性 | Tool-to-tool consistency |
| 標準作業程序 | Standard operating procedure (SOP) |
| 維護保養 | Maintenance and servicing |
| 故障排除 | Troubleshooting |
| 教材 | Training materials |
| 能力盤點 | Skills assessment |

## 8. AI 詞彙（index.ai / ai.json / 製程頁 AI 區塊）

| zh-Hant | English |
|---|---|
| AI 智慧製造 | AI Manufacturing |
| 前沿架構 | frontier architecture |
| 對標／對標架構 | benchmark / benchmark architecture |
| 對標指標 | benchmark metric |
| 導入 | deployment（動詞 deploy；技術轉移用 transfer） |
| 數字孿生 | Digital Twin |
| 物理仿真 | Physics Simulation（內文 physics-based simulation） |
| 生成式微影 | generative lithography |
| 反演式微影修正 | inverse lithography correction (ILT) |
| 光學鄰近效應優化 | optical proximity optimization |
| 缺陷分類 | defect classification |
| 良率預測 | yield prediction |
| 時序 FDC | time-series FDC |
| 聯邦學習 | federated learning |
| 逃逸率 | escape rate |
| 佈局熱點 | layout hotspot |
| 架構（年份） | Architecture (year) |
| 應用製程 | Process area |
| 第三方公開發表 | published by third-party academic and industry research |
| 非倍特爾自有量測數據 | not measurements of our own |

## 9. 表單字串（common.form，contact.html 使用）

| zh-Hant | English |
|---|---|
| 姓名／請輸入您的姓名 | Name / Your name |
| 公司／公司或機構名稱 | Company / Company or organization |
| 電話／含國碼，例如 +852 | Phone / With country code, e.g. +852 |
| 需求類別／請選擇需求類別 | Inquiry type / Select an inquiry type |
| 訊息／請簡述製程段、設備需求與時程 | Message / Briefly describe the process area, equipment and timeline |
| 設備採購 | Equipment procurement |
| 拆裝運送 | De-installation & shipping |
| 製程技術導入 | Process technology transfer |
| 人才培訓 | Talent training |
| AI 整合 | AI integration |
| 其他 | Other |
| 送出詢問 | Send inquiry |
| 必填 | required |
| 此欄位為必填。 | This field is required. |
| 請選擇需求類別。 | Please select an inquiry type. |
| 請輸入正確的電子郵件格式。 | Please enter a valid email address. |
| 網站詢問（信件主旨前綴） | Website inquiry |
| `mail.subject_sep`（主旨分隔符，母本為全形「｜」） | 半形 `" \| "`（空格＋直線＋空格） |
| `mail.sep`（內文抬頭分隔符，母本為全形「：」） | 半形 `": "`（冒號＋空格） |
| 送出後將開啟您的郵件軟體… | Submitting opens your email client with the message pre-filled. Please review it and send. |

## 10. 首頁既有譯文（可直接引用的定案句）

| zh-Hant | English |
|---|---|
| 先進半導體製程的整合夥伴 | Advanced process integration partner |
| 九大主製程設備採購、拆裝運送、技術導入與 AI 整合。 | Equipment procurement, relocation, process transfer and AI integration across nine process areas. |
| 以香港為據點，串接日系主力設備品牌與前沿人工智能架構。 | Based in Hong Kong, connecting leading Japanese equipment brands with frontier AI architectures. |
| 大主製程設備段／個日系主力設備品牌／項核心業務 | main process areas / leading Japanese brands / core business lines |
| 九大主製程設備 | Nine main process areas |
| 每一段製程都對應日系主力品牌與專屬 AI 對標架構。 | Every area maps to leading Japanese brands and its own AI benchmark architectures. |
| 每一段製程都導入前沿 AI | Frontier AI in every process area |
| 選擇倍特爾的理由 | Why work with BETTER |
| 上列品牌設備由倍特爾提供採購、銷售及維護服務… | BETTER provides procurement, sales and maintenance services for the equipment brands listed above. Brand names are trademarks of their respective owners and are used for equipment identification only. |

## 11. 設備總覽頁與九個製程頁的重複字串（第三階段追加，append-only）

九個 `equipment-<area>.json` 共用同一模板，下列字串**每頁都會出現**，必須逐字沿用，
不得改寫成同義詞；`content/en/equipment-cmp.json`／`equipment-cleaning.json` 已先落地為準。

| zh-Hant | English |
|---|---|
| 設備範圍（h2） | Equipment scope |
| 服務內容（h2） | Services provided |
| AI 整合（h2） | AI integration |
| 適用場景（h2） | Where it fits |
| 以下為倍特爾對標導入的第三方前沿架構。 | The third-party frontier architectures BETTER benchmarks and deploys. |
| 對標／導入之前沿架構（tag） | Benchmark architecture |
| 對標指標：… | `Benchmark metric: …`（半形冒號＋空白，句首大寫） |
| 以日系主力品牌為主，涵蓋… | Focused on leading Japanese brands, covering … |
| 設備採購與機種評估選型 | Equipment procurement, evaluation and tool selection |
| 設備狀態查驗與驗機協助 | Tool condition inspection and acceptance support |
| 拆機、包裝與跨境運送 | De-installation, packing and cross-border shipping |
| 進場安裝（＋調試） | Move-in installation (and tuning) |
| 維護保養與備品規劃 | Maintenance and spare parts planning |
| 操作與維護人員培訓 | Operator and maintenance staff training |
| 研究機構建立…實驗能力 | Research institutes building … capability |
| `banner_label`（各頁橫幅 aria-label） | `<主體> photo`（例：Lithography bay photo、Etch tool photo、Ion implanter photo） |

### 本批新增的設備／AI 名詞

| zh-Hant | English |
|---|---|
| 塗佈顯影軌道／旋塗顯影軌道 | coat and develop track |
| 光阻 | photoresist |
| 對準（黃光） | alignment |
| 腔體 | chamber |
| 耗材 | consumables |
| 備品 | spare parts |
| 晶舟 | wafer boat |
| 熱盤／冷卻盤 | hot plate / chill plate |
| 加熱模組 | heater module |
| 升降溫曲線 | ramp profile |
| 束線 | beamline |
| 端站 | end station |
| 離子源 | ion source |
| 通道效應 | channeling effect |
| 摻雜剖面 | dopant profile |
| 重新驗證／重新校正 | requalification / recalibration |
| 終點偵測 | endpoint detection |
| 過蝕／欠蝕 | over-etch / under-etch |
| 代理模型 | surrogate model |
| 不確定性量化 | uncertainty quantification |
| 離群偵測 | outlier detection |
| 熱不均 | thermal non-uniformity |

## 11. 製程頁與 AI 頁補充（第三階段新增，append-only）

以下為 `equipment-<area>.json` 與 `ai.json` 在第三階段定案、且反覆出現的用語。

| zh-Hant | English | 出現處 |
|---|---|---|
| 設備範圍 | Equipment scope | `scope.title`（h2） |
| 服務內容 | Services provided | `services.title`（h2） |
| 適用場景 | Where it fits | `fit.title`（h2） |
| 以下為倍特爾對標導入的第三方前沿架構。 | The third-party frontier architectures BETTER benchmarks and deploys. | `ai.lead` |
| 對標指標： | `"Benchmark metric: "` | `ai.entries[].metric` 前綴 |
| 對標／導入之前沿架構 | Benchmark architecture | `ai.entries[].tag` |
| 設備採購與機種評估選型 | Equipment procurement, evaluation and tool selection | `services.features` |
| 設備狀態查驗與驗機協助 | Tool condition inspection and acceptance support | `services.features` |
| 拆機、包裝與跨境運送 | De-installation, packing and cross-border shipping | `services.features` |
| 操作與維護人員培訓 | Operator and maintenance staff training | `services.features` |
| 以日系主力品牌為主，涵蓋… | Focused on leading Japanese brands, covering … | `scope.paragraphs` |
| 研究機構建立…能力 | Research institutes building … capability | `fit.features` |
| 逃逸率 -15% | escape rate down 15%（內文）／`escape rate -15%`（表格數值欄） | AI 卡片與對標表 |
| 約 92%（28–3nm） | about 92% (28–3nm)；數字與 en dash 原樣沿用 | AI 卡片 |
| 研磨物理仿真 | Polish physics simulation | CMP |
| 平坦化製程條件導入 | Planarization process condition setup | CMP |
| 藥液系統／藥液供應 | chemical delivery system / chemical supply | Wafer Cleaning |
| 顆粒缺陷根因分析 | Particle defect root cause analysis | Wafer Cleaning |
| 單片式／批次式清洗 | single-wafer / batch cleaning | Wafer Cleaning |
| 已知良品（KGD） | known good die (KGD) | Inspection & Test |
| 離群偵測 | outlier detection | Inspection & Test |
| 共形預測 | conformal prediction | Inspection & Test |
| 複審（e-beam） | review（e-beam defect review） | Inspection & Test |
| 封測廠 | test house | Inspection & Test |
| 掩模版廠 | mask shop | Photomask |
| 電子束寫入數字孿生 | E-beam writing digital twin | Photomask |
| 寫入劑量／鄰近效應 | write dose / proximity effects | Photomask |
| 防震環境確認 | vibration environment check | Photomask |
| 我們如何看待 AI | How we approach AI | ai.json |
| 三大貫穿主軸 | Three pillars across all areas | ai.json |
| 典型應用： | `"Typical uses: "` | ai.json pillars |
| AI 架構對標表 | AI benchmark architectures | ai.json |
| 領域／代表模型（年份）／核心架構／輸入數據特徵／輸出／評估指標／關鍵量化結果 | Domain / Model (year) / Core architecture / Input features / Output / metrics / Key quantitative results | 對標表欄位 |
| 製程與 AI 對應 | Process and AI mapping | ai.json |
| 主要對標架構／導入重點 | Main benchmark architectures / Deployment focus | 矩陣表欄位 |
| AI 導入五步驟 | Five steps to deployment | ai.json |
| 資料接入／模型導入／驗證 | Data integration / Model deployment / Validation | ai.json 步驟 |
| 討論 AI 導入場景 | Discuss an AI use case | ai.json CTA |

> `ai.json` 的 `pillars.entries[].title` 在英文版一律為空字串，`title_lat` 已是英文，
> 若兩者都填會在卡片標題出現同字重複（與 `content/en/index.json` 的處理一致）。

## 11. about／services／contact 三頁新增用語（第三階段補充）

> 本節為 `content/en/{about,services,contact}.json` 翻譯時新增的常用詞，後續頁面一律沿用。

| zh-Hant | English |
|---|---|
| ~~公司負責人~~（已移除：`about.leadership` 已移除） | — |
| 服務對象 | Who we serve |
| 使命／願景 | Mission / Vision |
| 業務範圍 | Business scope |
| 我們的價值主張 | What we stand for |
| 總部據點 | Our Hong Kong base |
| 晶圓製造廠 | wafer fab |
| 先進封裝測試廠 | advanced packaging and test plant |
| 二手與翻新設備 | used and refurbished equipment |
| 型錄規格 | catalog specification |
| 備品／耗材 | spares / consumables |
| 設備履歷 | service history |
| 現況盤點 | current state |
| 條件建立 | condition setup |
| 實驗設計 | design of experiments |
| 資料接入 | data onboarding |
| 模型導入 | model deployment |
| 場景／應用場景 | use case |
| 水電氣接續 | utility hook-up |
| 可驗證 | verifiable |
| 聯絡資訊 | Contact information |
| 聯絡人（卡片標題） | Contact person |
| 公司地址（卡片標題） | Address |
| 需求諮詢（表單區 h2） | Tell us what you need |
| 其他聯絡方式 | Other ways to reach us |
| 直接來信 | Email us directly |
| 填寫前可先看 | Before you write |
| 辦公室位置 | Office location |
| 常見問題 | Frequently asked questions |
| 授權代理／指定經銷商 | authorized agent / appointed distributor（一律用於否定句） |

## 12. 第四階段（英文文案潤稿）新增的統一規則

> 本節為 `content/en/*.json` 英文潤稿時定案的寫法，append-only。逐項變更紀錄見
> `docs/editorial-en.md`。

| 項目 | 規則 | 範例 |
|---|---|---|
| `meta.title` 品牌後綴 | 一律 `… \| BETTER`（不寫全稱，全稱只出現在 footer 與 `about.intro`） | `About \| BETTER`、`Services \| BETTER`、`Contact \| BETTER` |
| `banner_label`（aria-label） | 一律 `<subject> photo`，不寫 `Photo of a/the <subject>` | `CMP tool photo`、`Wafer cleaning bay photo`、`Inspection bay photo`、`Photomask photo` |
| 媒體 `caption` | 佔位框上的可見標籤，寫成**短主體描述**（約 ≤ 12 字）；`alt` 才寫完整的美術指示（光線、色調、構圖） | alt: `Exterior of an etch tool with plasma glow through the chamber viewport, dark surroundings and a magenta halo` → caption: `Etch tool exterior with plasma glow through the chamber viewport` |
| 對標／導入的動詞搭配 | 用 `benchmark and deploy`；**不可**寫 `benchmark X into Y`、`benchmarked in` | `Digital twin, physics-based simulation and generative lithography architectures, benchmarked and deployed in every process area.` |
| 表格數值範圍 | 一律半形數字 + en dash `–`，不用 `~` | `-20–25%`、`28–3nm`、`5–12×`、`10–30×` |
| 表格儲存格首字 | 一律大寫起首 | `Die/wafer pass-fail, precision/recall` |
| 比較運算子 | 前後各一個半形空白 | `MAE < 15×10⁻⁵V` |
| 時序 FDC 模型名 | 一律 `RNN time-series FDC`（不寫 `time-series RNN FDC`） | `TSMC smart manufacturing: RNN time-series FDC + federated learning` |
| 製程卡 `text` 的設備字 | 九張卡一律用 `tools` | `Metrology, defect inspection and electrical test tools.` |
| 牛津逗號 | 不使用；若列舉尾端出現 `and … and`，改用 `then` 或重排 | `Move-in positioning, reinstallation, utility hook-up, then functional and process tuning.` |
| 四條主線（about hero） | `four lines`（不寫 `four disciplines`，與 five core business lines 呼應） | `Serving advanced manufacturing along four lines: equipment, process, people and AI.` |

## `title_lat` slash (phase-4 addendum)

`title_lat` is a language-invariant field: always the ASCII form with spaces —
**`LithoDreamer / ILT`**. The fullwidth `／` stays only in the translated `arch` prose of the
CJK languages, which is not invariant.
