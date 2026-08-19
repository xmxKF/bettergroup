# 倍特爾科技集團官網 — 圖片生成提示詞（Image Prompts）

> 對應檔案：`docs/content-spec.md` §16 資產索引、`DESIGN.md` §8 影像方向。
> 本檔涵蓋 **48 個 `IMG-*` 資產 ＋ 2 張影片海報**（共 50 張靜態圖），逐一對應到固定檔名。
> 說明文字為繁體中文；**生成提示詞一律使用英文**（影像模型對英文提示的理解與可控性最佳）。
> 檔名規則：`IMG-<PAGE>-<NN>` → `assets/img/<page小寫>-<nn>.jpg`；影片海報屬影片資產，ID 為 `VID-<PAGE>-<NN>（海報）` → `assets/img/<page小寫>-<nn>-poster.jpg`。
> 產出後請以原始檔名放入 `assets/img/`，頁面上的佔位框會自動被實圖取代。

---

## 0. 全站視覺一致性（Global Consistency）

整套圖必須看起來像「同一位攝影師、同一天、同一組器材」拍出來的，加上「同一位設計師」畫的圖形。
因此全站只有 **兩個視覺家族**，任何資產必屬其一，不得混血（IMP-02 為唯一明示的例外）。

### 0.1 家族 A — 紀實攝影（Documentary Photography）

用於真實場景：無塵室、設備、物流、辦公室、人物（一律穿完整無塵服、臉部不可辨識）。

**STYLE-A 共用尾綴（附加到每一個 A 家族提示詞末端）**

```
BETTER house style: documentary editorial photography, shot on full-frame with a 35mm or 50mm prime,
f/2.8-f/5.6, medium depth of field, verticals kept perfectly orthogonal (architectural perspective
correction), calm composition, either near-symmetrical or driven by one strong linear perspective,
generous negative space on one side for typography; cool neutral white balance, global saturation
reduced 10-15%, colour peaks allowed ONLY in wafer diffraction rainbows, machine indicator LEDs and
yellow-lithography amber (#E9B23C); shadows fall toward deep navy graphite (#101A2B) and retain full
detail (never crushed black), highlights soft and never clipped; lighting is even diffuse cleanroom
ceiling light plus a single soft directional side key; restrained, precise, trustworthy engineering
mood; no text, no signage, no nameplates anywhere in frame; natural film-like grain, no HDR.
```

### 0.2 家族 B — 極簡技術圖形（Minimal Technical Graphic）

用於流程圖、資料視覺化、抽象品牌視覺、地圖、介面示意。**不是 3D 渲染、不是插畫風炫技**，而是像工程文件裡的乾淨向量圖被精緻化。

**STYLE-B 共用尾綴（附加到每一個 B 家族提示詞末端）**

```
BETTER graphic style: minimal technical infographic, flat vector-like clarity with subtle depth,
drawn on either deep navy graphite ground #101A2B or cool off-white ground #F6F7F8; hairline strokes
(1-2px equivalent), wide margins, strict grid alignment, engineering-drawing precision; single accent
colour teal-blue #0C6B8F on light grounds / #5CC8E8 on dark grounds; the spectral gradient
(#C42B3A, #E2662B, #E9B23C, #C9CE55, #56C08A, #2FA9B8, #4A80C8, #7B4CC0) appears ONLY as thin lines,
small nodes or short accent segments, never as a large fill or background wash; no glossy bevels,
no glow bloom, no drop shadows, no neon; no text, no labels, no numbers, no legends; calm, clinical,
premium B2B feel; flat lighting, even exposure.
```

### 0.3 共用負面提示詞（NEG-BASE）

每個資產的負面提示詞皆以此為基底，再加上該資產的專屬追加項。

```
text, letters, words, captions, numbers, labels, legends, watermark, signature, date stamp,
any logo, any brand nameplate, any manufacturer marking, company name, model number,
fake UI overlay, HUD, holographic projection, sci-fi interface, floating windows, glowing circuit board,
globe with circuits, purple neon, magenta cyberpunk lighting, teal-and-orange grade, lens flare,
bokeh balls, HDR halo, over-sharpening, oversaturated colours, heavy vignette, tilted horizon,
distorted hands, extra fingers, six fingers, deformed anatomy, recognisable faces, portrait close-up,
handshake, business suit, stock-photo posing, pointing at screen, group smiling at camera,
messy cables, dust, clutter, rust, dirty floor, crowded frame,
cartoon, anime, clay render, plastic toy look, low-poly, illustration texture on photo assets,
blurry, out of focus, motion blur, low resolution, jpeg artifacts, duplicated objects, warped geometry
```

### 0.4 全站規則（必須遵守）

| 規則 | 說明 |
|---|---|
| 畫面內零文字 | 所有文案由 HTML 呈現；AI 生成文字必然變形。若模型仍生出文字，重跑或後製移除。 |
| 零品牌識別 | 不得出現任何真實或虛構的廠牌 logo、銘牌、型號字樣、貼紙。 |
| 人物處理 | 一律完整無塵服＋護目鏡＋口罩；背面、側面或遠景，臉部不可辨識；不得出現握手、西裝、對鏡頭微笑。 |
| 不得暗示自有晶圓廠 | 倍特爾為設備採購與服務商；畫面可為無塵室與設備，但不得出現「這是本公司量產線」的敘事線索（如廠房招牌、車間全景加人員編制）。 |
| 介面類資產 | `IMG-SVC-02`、`IMG-CMP-03`、`IMG-CLEAN-03`、`IMG-INSP-03`、`IMG-AI-03` 一律以 **B 家族無文字抽象資料圖形** 呈現，**不可**做成疊在照片上的假 HUD。 |
| 色彩紀律 | 全站彩度峰值只保留三處：晶圓繞射彩虹、指示燈、黃光區琥珀。其餘接近冷調黑白灰。 |
| 光譜色用量 | 任一張圖中，光譜漸層佔畫面面積不得超過約 3%，且必須是線／點而非面。 |
| 輸出格式 | JPEG，品質 82–88，sRGB，去除 EXIF；長邊不得低於下列各資產標示的最小解析度。生成完成後把檔案放進 `assets/img/`（副檔名不限），執行 `python tools/optimize_media.py` 即自動轉成交付檔（正確比例、長邊 1920／1600、≤ 400 KB），原始檔移入 `assets/src/`。 |
| 命名 | 直接使用各資產標示的檔案路徑與檔名，不加後綴。 |

### 0.5 比例與最小解析度對照

比例欄與 `content/zh-hant/*.json` 各媒體物件的 `ratio` 欄位一致（`ratio` 為唯一真實來源）；解析度是**生成端的下限**，不是交付尺寸——交付尺寸由 `tools/optimize_media.py` 決定。

| 用途 | 比例 | 最小解析度 | MJ 參數 |
|---|---|---|---|
| Hero／全幅媒體 | 16:9 | 2400×1350 | `--ar 16:9` |
| 卡片／段落配圖 | 4:3 | 1600×1200 | `--ar 4:3` |
| 直式人像／窄欄 | 3:4 | 1200×1600 | `--ar 3:4` |
| 寬帶／地圖／分隔視覺 | 21:9 | 2520×1080 | `--ar 21:9` |

### 0.6 各模型通用設定建議

| 模型 | 建議 |
|---|---|
| **Midjourney v7** | 加 `--style raw`；A 家族 `--stylize 100–150`，B 家族 `--stylize 50–100`；負面詞以 `--no` 串接（取 NEG-BASE 前 20 項即可，過長會稀釋）。同批次固定 `--seed` 以維持一致性。 |
| **Flux.1 / Flux Pro** | guidance 3.0–3.5（A 家族偏 3.0，B 家族偏 3.5）；prompt 以完整散文輸入，不需 `--` 參數；Flux 無原生負面詞，改把禁止項改寫為肯定敘述（如 "clean uncluttered floor, no signage" → "bare polished epoxy floor, blank panels"）。 |
| **Imagen 3 / 4** | 設 `aspectRatio`；A 家族開頭加 `A photograph of`，B 家族開頭加 `A minimal flat vector infographic of`；`personGeneration` 設為 allow_adult 且仍需保持臉部不可辨識。 |
| **DALL·E 3 / GPT Image** | 以散文輸入，並在句尾明確寫 `Do not render any text, letters, numbers or logos anywhere in the image.`（該模型最容易自動加字）。 |
| 一致性技巧 | 先產出 `IMG-EQP-01`（A 家族基準）與 `IMG-AI-01`（B 家族基準），確認調性後，其餘資產以其為 style reference（MJ `--sref` / Flux redux / Imagen style image）批次生成。 |

---

## 1. index.html（首頁）— HOME

### VID-HOME-01（海報）｜`assets/img/home-01-poster.jpg`

- **一句話（zh）**：`VID-HOME-01` 的海報影格——無塵室設備列橫移鏡頭的首格靜幀。
- 頁面 index.html｜家族 A｜16:9｜最小 2400×1350｜用途：影片載入前的靜態畫面，須與影片首格同構圖。

**Positive**

```
A wide cleanroom equipment aisle seen straight down its centre line, two rows of tall white
semiconductor process tools receding to a vanishing point, a robotic wafer transfer arm frozen
mid-motion behind a clean glass access panel on the left tool, closed load-port doors, polished
epoxy floor reflecting the ceiling light panels, perforated ceiling filter grid, cool white
illumination, one small amber indicator lamp as the only warm accent, wide empty floor space in
the lower third for typography, 35mm lens, f/4, deep focus, cool neutral grade, near-monochrome
palette of white, pale grey and deep navy graphite.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: people in frame, open maintenance panels, exposed wiring, warning stickers,
yellow lithography lighting, warm interior grade, fisheye distortion
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 120`；Flux guidance 3.0；Imagen 前綴 `A photograph of`；此圖必須與 `VID-HOME-01` 的首格構圖一致（同機位、同焦段），建議由影片抽格後再調色，或以本提示詞生成後作為影片的 first-frame 條件圖。

---

### IMG-HOME-01｜`assets/img/home-01.jpg`

- **一句話（zh）**：等距剖面示意圖，象徵設備、遷移、製程、人才、AI 五條業務主線。
- 頁面 index.html｜家族 B｜4:3｜最小 1600×1200｜用途：五大業務支柱區塊配圖。

**Positive**

```
A minimal isometric cutaway diagram of a semiconductor fab facility, drawn as a clean engineering
schematic on a deep navy graphite ground #101A2B: a raised cleanroom floor slab with five distinct
tool bays arranged left to right at equal spacing, each bay reduced to a simple geometric volume,
connected underneath by thin routing lines that converge into one horizontal spine; hairline white
and pale grey strokes, one teal-blue #5CC8E8 highlight line tracing the spine, five tiny nodes on the
spine each carrying a different single hue sampled from the spectral gradient, the diagram centred in
a slightly squarer 4:3 frame with generous empty margins on all four sides (it is displayed inside a
card cell and may be cropped on the long edge), strict isometric projection at 30 degrees, no
perspective distortion, no floor texture.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: photorealism, people, machinery detail, pipes and cable clutter, blueprint grid
background, glowing edges, gradient background wash, drop shadows
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 60`；Flux guidance 3.5；DALL·E 3 表現最佳（等距圖形理解好），務必加 `no text`。

---

### IMG-HOME-02｜`assets/img/home-02.jpg`

- **一句話（zh）**：九宮格製程流程示意，象徵晶圓自掩模版到成品的流轉。
- 頁面 index.html｜家族 B｜4:3｜最小 1600×1200｜用途：九大製程總覽區塊配圖。

**Positive**

```
A minimal flat infographic on a cool off-white ground #F6F7F8: a three-by-three grid of nine equal
square cells with hairline #CBD1D8 borders and generous internal padding, each cell containing one
different simple line-drawn geometric pictogram at 1.5px stroke weight in teal-blue #0C6B8F
(a lens ring, a chamber, a stacked film cross-section, a heat coil, a beam line, a rotating disc,
a droplet spray, a measuring reticle, a rectangular plate), a single continuous thin path threading
through the nine cells in reading order to suggest sequence, the path rendered as a hairline
spectral gradient line, the nine-cell grid centred in a four-by-three frame and nearly filling it,
with equal generous white margins on all four sides, perfectly aligned grid, clinical and calm.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: icon labels, numbering, colourful filled icons, emoji, skeuomorphic icons,
3d isometric boxes, photographic elements, drop shadows, rounded cartoon shapes
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 50`；圖示辨識度若不足，可改以向量工具重繪——本資產本質上是可手工製作的圖形，AI 生成僅作為初稿。

---

### IMG-HOME-03｜`assets/img/home-03.jpg`

- **一句話（zh）**：晶圓熱場等高線與感測時序曲線疊合的抽象資料視覺化。
- 頁面 index.html｜家族 B｜4:3｜最小 1600×1200｜用途：AI 整合亮點條配圖。

**Positive**

```
An abstract data visualisation on a deep navy graphite ground #101A2B: a large circle representing a
wafer occupies the left half, filled with smooth concentric thermal contour lines of varying spacing
that pool into two off-centre hot regions, contours drawn as hairlines shifting subtly from cool
teal #2FA9B8 to warm amber #E9B23C only at the peaks; on the right half, four thin horizontal
time-series traces stacked with equal vertical rhythm, each a different single hue from the spectral
gradient, quiet and low-amplitude with one synchronised excursion; a hairline vertical rule connects
the wafer to the traces; vast negative space, no axes, no ticks, no frames.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: chart axes, gridlines, tick marks, tooltips, dashboard panels, window chrome,
neon glow, particle effects, lens bloom, dark blue gradient vignette
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 70`；Flux guidance 3.5；此圖與 `IMG-CVD-03`、`IMG-BAKE-03` 屬同一語彙，建議同批同 seed 生成。

---

### IMG-HOME-04｜`assets/img/home-04.jpg`

- **一句話（zh）**：工程團隊於機台前檢視資料看板的側面剪影。
- 頁面 index.html｜家族 A｜4:3｜最小 1600×1200｜用途：選擇倍特爾區塊配圖。

**Positive**

```
Two engineers in full white cleanroom bunny suits with hoods, goggles and masks, seen from behind
and slightly to the side as dark-rimmed silhouettes against a bright process tool, standing at a
comfortable distance from a large wall-mounted display whose surface is rendered as a soft
out-of-focus field of pale blue-grey luminance with no legible content, one engineer's gloved hand
resting at their side, the other holding a slim clipboard-sized tablet angled away from camera;
cleanroom aisle continues behind them, cool white overhead light rim-lighting the suits, faces
completely unreadable, composition weighted right with empty aisle on the left, 50mm lens, f/2.8,
subject sharp, background gently soft.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: readable screen content, charts on the display, pointing gestures, thumbs up,
uncovered faces, hair visible, street clothes, lab coats instead of bunny suits, three or more people
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 130`；Imagen 需明確寫 `faces not visible, seen from behind`；若螢幕內容出現線條或文字，改以 `--no screen content` 重跑。

---

## 2. about.html（關於我們）— ABOUT

### IMG-ABOUT-01｜`assets/img/about-01.jpg`

- **一句話（zh）**：香港天際線與現代商業大廈立面的冷調照片，象徵港島樞紐位置。
- 頁面 about.html｜家族 A｜3:4｜最小 1200×1600｜用途：頁首／公司定位配圖。

**Positive**

```
A cool, restrained vertical architectural photograph of a modern Hong Kong commercial tower at blue
hour, upright portrait framing, camera slightly below eye level looking up the full height of a
glass-and-anodised-aluminium facade whose window grid is rendered crisply and repeats to the top of
the frame, two neighbouring towers receding into soft atmospheric haze at the left edge, the lower
sixth showing a calm strip of harbour water, overcast even sky filling the upper third as clean
negative space, verticals perfectly corrected with no keystoning, cool blue-grey palette with only a
few warm window lights as minimal accent, 35mm tilt-shift look, f/5.6, high micro-contrast but no HDR.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: billboards, neon signage, illuminated advertising, junk boats, tourists, flags,
sunset orange sky, laser show, crowded night scene, identifiable named buildings signage
```

- **Model notes**：MJ `--ar 3:4 --style raw --stylize 140`；避免生成可辨識的招牌字樣；若模型加上霓虹廣告，加 `--no signage, advertising`。

---

### IMG-ABOUT-02｜`assets/img/about-02.jpg`

- **一句話（zh）**：晶圓與資料節點以細線連結的極簡抽象視覺。
- 頁面 about.html｜家族 B｜4:3｜最小 1600×1200｜用途：使命與願景區塊配圖。

**Positive**

```
A minimal abstract composition on a deep navy graphite ground #101A2B: a single large hairline
circle representing a wafer, centred slightly low, its interior divided by a faint orthogonal die
grid at very low contrast; from the wafer edge, eight thin straight lines radiate outward at uneven
angles to small solid dots of decreasing size, forming a sparse node network in the upper area; two
of the connecting lines carry a subtle spectral gradient, the rest are pale grey hairlines; enormous
negative space, asymmetric balance, absolute geometric precision, no glow.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: dense network mesh, brain or neuron imagery, glowing nodes, particle field,
starfield background, circuit traces, gradient blur, 3d spheres
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 50`；Flux guidance 3.5；與 `IMG-AI-01` 同語彙，宜同批生成。

---

### IMG-ABOUT-03｜`assets/img/about-03.jpg`

- **一句話（zh）**：九龍佐敦一帶街廓抽象化的簡化線稿地圖，單一標記點。
- 頁面 about.html｜家族 B｜21:9｜最小 2520×1080｜用途：總部位置區塊配圖。

**Positive**

```
A stylised minimal map illustration on a cool off-white ground #F6F7F8: an abstracted dense urban
street grid of an Asian harbour-side district, blocks rendered as flat pale grey #EFF1F3 shapes with
hairline #CBD1D8 outlines, main avenues as slightly wider white channels running diagonally, a
waterfront edge sweeping across one corner as a single soft grey plane; one small solid teal-blue
#0C6B8F circular marker with a thin concentric ring sits just off centre as the only saturated
element; ultra-wide letterbox band composition with the street grid spread horizontally and large
clean margins left and right, flat top-down orthographic view, no terrain, no shadows.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: street names, place labels, map pins with icons, compass rose, scale bar,
satellite imagery, 3d buildings, google-maps colour scheme, roads in yellow, parks in green
```

- **Model notes**：MJ `--ar 21:9 --style raw --stylize 50`；**此圖為風格化示意，非導航地圖**，不得標示真實街名；正式上線前建議以向量工具重繪以確保零文字。

---

### IMG-ABOUT-04｜`assets/img/about-04.jpg`

- **一句話（zh）**：會議室桌面俯視，攤開的設備規格文件與筆記本。
- 頁面 about.html｜家族 A｜16:9｜最小 2400×1350｜用途：核心價值區塊配圖。

**Positive**

```
A top-down flat-lay photograph of a light grey conference table: several loosely fanned technical
document sheets showing abstract line drawings and tables whose content is too small and too soft to
read, a closed dark notebook with a thin metal pen laid parallel to its edge, a slim aluminium laptop
closed at the top edge of the frame, a plain white ceramic cup with black coffee, and one anti-static
glove folded neatly; arrangement is orderly with clear alignment to an invisible grid, wide empty
table surface on the right for typography, soft even overhead daylight from a large window creating
gentle directional shadows, cool neutral grade, 50mm lens, f/5.6, shot perfectly perpendicular.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: hands, arms, people, legible document text, printed logos on stationery,
colourful sticky notes, phone screen content, plants, decorative props, warm wood tabletop
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 110`；文件上的「文字」須維持不可讀的細微紋理，若模型生出清晰假字，重跑或後製模糊。

---

## 3. services.html（服務項目）— SVC

### IMG-SVC-01｜`assets/img/svc-01.jpg`

- **一句話（zh）**：包裝完整的機台模組吊裝進入無塵室通道的廣角照。
- 頁面 services.html｜家族 A｜21:9｜最小 2520×1080｜用途：頁首／服務總覽配圖。

**Positive**

```
An ultra-wide letterbox (cinemascope) industrial photograph of a large crated semiconductor tool module wrapped in plain matte
protective film and strapped to a heavy steel skid, suspended just above the floor by four clean
lifting slings from an overhead gantry, being moved through a tall white equipment entry corridor
toward an open airlock door; two figures in full white cleanroom suits stand well back at the frame
edges guiding it, seen from behind; strong one-point perspective down the corridor, cool white
lighting from continuous ceiling panels, polished floor with soft reflections, empty clean band of
corridor wall along the top of the frame,
35mm lens, f/5.6, everything crisp and orderly.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: shipping labels, barcodes, fragile stickers, crane brand markings, forklift,
cardboard boxes, warehouse racking, outdoor loading dock, hard hats and hi-vis vests,
people facing camera
```

- **Model notes**：MJ `--ar 21:9 --style raw --stylize 130`；若出現貼標籤／條碼，加 `--no labels, barcode, stickers`。

---

### IMG-SVC-02｜`assets/img/svc-02.jpg`

- **一句話（zh）**：機台數字孿生介面示意——3D 機台輪廓與感測時序曲線並置的深色資料圖形。
- 頁面 services.html｜家族 B｜16:9｜最小 2400×1350｜用途：AI 與先進製造整合服務配圖。

**Positive**

```
A dark abstract interface-style data graphic on ground #101A2B, composed as a flat layout with no
window chrome: on the left, a semiconductor process tool represented as a precise wireframe volume
in pale grey hairlines with one internal chamber highlighted by a thin teal-blue #5CC8E8 outline; on
the right, three stacked cards of subtly lighter navy #16202F, each containing one smooth sensor
time-series trace at hairline weight, the traces in three different single hues drawn from the
spectral gradient, plus one card holding a small radial gauge arc; a single hairline spectral rule
separates the two halves; strict alignment, wide gutters, absolutely no text, no numerals, no icons.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: readable numbers, KPI figures, buttons, tabs, sidebars, window title bar, cursor,
browser frame, neon glow, glassmorphism blur, realistic monitor bezel, desk photograph
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 60`；**這是圖形不是照片**，不可做成拍攝螢幕的照片；DALL·E 3 對「無文字介面」需明確禁止指令。

---

### IMG-SVC-03｜`assets/img/svc-03.jpg`

- **一句話（zh）**：六節點串成一線的服務流程等距插畫。
- 頁面 services.html｜家族 B｜21:9｜最小 2520×1080｜用途：服務流程時間軸區塊配圖。

**Positive**

```
An ultra-wide minimal process diagram on cool off-white #F6F7F8: one perfectly horizontal hairline
axis spanning the full width, with six evenly spaced circular nodes sitting on it; each node is an
open ring of 2px stroke, five in graphite grey and one filled solid teal-blue #0C6B8F; above
alternating nodes, small abstract line pictograms float at consistent size (a magnifier ring, a
crate outline, a chamber, a wrench-free abstract tool shape, a wafer circle, a speech-free
rectangle), all in 1.5px teal strokes; a thin spectral gradient segment underlines the axis between
the first and last node; enormous white space above and below, exacting alignment.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: step numbers, stage labels, arrows with text, timeline dates, gantt bars,
colourful filled icons, drop shadows, 3d perspective, decorative flourishes
```

- **Model notes**：MJ `--ar 21:9 --style raw --stylize 50`；21:9 對多數模型較不穩定，可先產 16:9 再裁切，但須保留左右完整節點。

---

### IMG-SVC-04｜`assets/img/svc-04.jpg`

- **一句話（zh）**：工程師於機台前手持量測工具執行調試作業（直式）。
- 頁面 services.html｜家族 A｜3:4｜最小 1200×1600｜用途：安裝調試／技術服務配圖。

**Positive**

```
A vertical documentary photograph of a single engineer in a full white cleanroom bunny suit with
hood, goggles and mask, seen in three-quarter profile from behind, standing close to an opened
service side of a process tool, holding a small handheld metrology instrument up toward a mounting
fixture with both gloved hands; the tool's internal structure shows precise machined brackets and
clean anodised panels with no markings; a soft blue-grey instrument indicator glow at chest height
is the only colour accent; face fully unreadable, cool diffuse cleanroom light with one soft key
from the left, shallow depth of field with the instrument sharp, 50mm lens, f/2.8, vertical framing
with headroom for typography.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: visible face, mask pulled down, bare hands, screwdriver cliché, sparks,
warning labels, tangled cables, second person, industrial dirt, warm workshop lighting
```

- **Model notes**：MJ `--ar 3:4 --style raw --stylize 130`；手部易變形，優先選手部被工具遮擋或背向鏡頭的結果。

---

## 4. equipment.html（設備與製程總覽）— EQP

### IMG-EQP-01｜`assets/img/eqp-01.jpg`

- **一句話（zh）**：無塵室製程設備列透視照，黃光區與白光區的交界。
- 頁面 equipment.html｜家族 A｜16:9｜最小 2400×1350｜用途：頁首主視覺。**本圖為 A 家族的風格基準圖，請最先生成。**

**Positive**

```
A symmetrical wide photograph looking down a long cleanroom equipment bay: identical white process
tools line both sides in strict repetition, converging to a distant doorway; the near half of the
corridor is lit by cool white ceiling panels, while the far half beyond a glass partition glows in
authentic amber lithography light (#E9B23C), creating a clean cool-to-warm transition exactly at
the frame's midpoint; polished light-grey epoxy floor mirrors both zones, perforated ceiling filter
grid recedes overhead, blank machine panels with no markings, no people, 35mm lens, f/5.6, verticals
perfectly straight, calm and monumental, cool neutral grade with the amber as the only saturated area.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: people, open panels, cable trays on floor, warning tape, monitors showing content,
orange filter look, uneven yellow cast over the whole frame, wide-angle barrel distortion
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 120`，建議 `--seed` 固定並以此圖作為全站 A 家族的 `--sref`；Flux guidance 3.0；黃光必須是局部區域，不可整張染黃。

---

### IMG-EQP-02｜`assets/img/eqp-02.jpg`

- **一句話（zh）**：九大製程環形循環流程圖，檢測為回饋迴路。
- 頁面 equipment.html｜家族 B｜4:3｜最小 1600×1200｜用途：九大製程流說明配圖。

**Positive**

```
A minimal circular process diagram on cool off-white #F6F7F8: nine small open ring nodes evenly
distributed around one large hairline circle, connected head-to-tail by thin arc segments with tiny
directional chevrons, forming a closed clockwise loop; one node sits at the top as the entry point,
drawn slightly larger with a solid teal-blue #0C6B8F fill; from a node at the lower right, a thinner
inner arc cuts back across the circle toward the top node to indicate a feedback path, this single
inner arc rendered as a hairline spectral gradient; everything else in graphite grey hairlines,
generous margins, flat orthographic, exact radial symmetry.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: node labels, step numbers, arrowheads with text, gear icons, infinity symbol,
pie chart look, colourful segments, 3d ring, glow, gradient background
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 50`；環形對稱建議以向量工具最終定稿。

---

### IMG-EQP-03｜`assets/img/eqp-03.jpg`

- **一句話（zh）**：晶圓俯視特寫，表面折射出彩虹光譜，呼應品牌色。
- 頁面 equipment.html｜家族 A｜21:9｜最小 2520×1080｜用途：製程卡片區收尾視覺。

**Positive**

```
An ultra-wide letterbox macro photograph of a 300mm silicon wafer lying flat on a matte dark graphite
surface, the wafer placed right of centre in a wide horizontal band, shot from directly above with a slight offset so the wafer edge and its single flat notch enter the frame from
the right; the mirror surface diffracts a broad soft rainbow across the die grid, the spectral sweep
reading red through amber, green, teal and violet exactly like the brand gradient, while the
unlit areas stay near-black with retained detail; the fine orthogonal die grid is just visible under
the diffraction; one soft elongated highlight streak crosses the surface; deep clean negative space
on the left, 50mm macro, f/5.6, no dust, no fingerprints, cool ambient with a single controlled
soft-box reflection.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: fingerprints, dust particles, scratches, tweezers, gloved hand, oil-slick
psychedelic colours, cyan-magenta only rainbow, plastic disc look, chrome car-paint reflection
```

- **Model notes**：MJ `--ar 21:9 --style raw --stylize 140`；此圖是全站彩度最高的一張，其他資產須明顯低於它。

---

## 5. equipment-lithography.html（黃光段）— LITHO

### IMG-LITHO-01｜`assets/img/litho-01.jpg`

- **一句話（zh）**：黃光區走道全景，黃色濾光照明下的曝光機列。
- 頁面 equipment-lithography.html｜家族 A｜16:9｜最小 2400×1350｜用途：頁首主視覺。

**Positive**

```
A clean symmetrical photograph of a lithography bay bathed in authentic amber safe-light (#E9B23C):
two rows of large exposure tools with smooth blank enclosures recede down a polished floor, their
white panels rendered warm cream by the filtered light, the ceiling filter grid glowing softly
amber, a distant cool-white doorway at the vanishing point providing a small cool counterpoint;
no people, no markings, one small green status lamp on the nearest tool; 35mm lens, f/5.6, verticals
straight, the amber cast is genuine environmental light with neutral highlights, not an orange
filter; calm, hushed, precise.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: uniform orange colour grade, sepia tone, sodium-vapour look, people, open covers,
red darkroom lighting, smoke, haze machine effect
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 120`；Flux 對「琥珀環境光但白平衡不崩」表現最佳，guidance 3.0。

---

### IMG-LITHO-02｜`assets/img/litho-02.jpg`

- **一句話（zh）**：旋塗顯影軌道內部特寫，晶圓於旋塗腔中、光阻膜面反射色帶。
- 頁面 equipment-lithography.html｜家族 A｜4:3｜最小 1600×1200｜用途：設備範圍區塊配圖。

**Positive**

```
A close-up interior view of a coater-developer track module: a single wafer held on a spin chuck
inside a clean circular cup, a slim dispense nozzle arm poised just above its centre, the resist
film on the wafer surface showing smooth concentric interference colour bands in soft amber, green
and violet; the module's stainless interior is spotless with precise machined edges, amber safe-light
spills in from the upper left while a cool internal lamp lights the chuck; shot through the open
module face at a slight downward angle, 50mm macro, f/4, wafer surface sharp, module edges falling
gently out of focus.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: liquid splashes, drips, residue, scratches on wafer, human hands, plastic look,
rainbow oil slick, exaggerated saturation, visible machine branding
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 130`；干涉色帶須柔和，若過度飽和加 `--no oversaturated colours`。

---

### IMG-LITHO-03｜`assets/img/litho-03.jpg`

- **一句話（zh）**：AI 視覺化——光罩圖形與熱點預測疊圖，圖注意力連線標示。
- 頁面 equipment-lithography.html｜家族 B｜16:9｜最小 2400×1350｜用途：AI 對標架構區塊配圖。

**Positive**

```
An abstract technical graphic on deep navy #101A2B: the left two-thirds show a dense orthogonal
layout pattern of thin rectangles and channels resembling a mask layout, drawn entirely in pale grey
hairlines at varying line widths; three small regions of that layout are softly highlighted with
low-opacity warm amber #E9B23C fills marking predicted hotspots, each ringed by a 1px teal-blue
outline; overlaid across the layout, a sparse graph of small round nodes connected by very thin
straight edges of varying opacity suggests attention weights, two edges carrying a subtle spectral
gradient; the right third is empty navy space; flat, precise, no glow, no depth.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: heatmap rainbow blobs, jet colormap, legible layout text, circuit board
photograph, PCB traces, glowing neon lines, 3d extrusion, particle sparks
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 60`；與 `IMG-MASK-03` 同語彙但構圖須明顯不同（此圖偏左、Mask 圖為左右對照）。

---

## 6. equipment-etch.html（蝕刻段）— ETCH

### IMG-ETCH-01｜`assets/img/etch-01.jpg`

- **一句話（zh）**：蝕刻機台外觀與腔體觀察窗透出的電漿輝光。
- 頁面 equipment-etch.html｜家族 A｜16:9｜最小 2400×1350｜用途：頁首主視覺。

**Positive**

```
A photograph of a plasma etch tool in a dim cleanroom bay: the tool's smooth blank enclosure fills
the right half, and a small round quartz viewport near its centre emits a controlled violet-pink
plasma glow that spills a soft gradient onto the surrounding panel and floor; the rest of the scene
is lit only by low cool ambient light, deep navy shadows retaining detail, one row of tiny status
lamps along the panel edge; the left half is quiet empty aisle for typography; 35mm lens, f/2.8,
viewport sharp, restrained exposure so the glow never blooms, cool grade with the plasma as the only
saturated element.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: heavy bloom, lens flare, purple neon everywhere, cyberpunk grade, sparks,
lightning arcs, smoke, people, open chamber, gauges with readable dials
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 130`；輝光面積控制在畫面 10% 以內，避免落入「紫色霓虹 AI 風」。

---

### IMG-ETCH-02｜`assets/img/etch-02.jpg`

- **一句話（zh）**：電漿蝕刻腔體內部視角，晶圓承載盤與均勻輝光。
- 頁面 equipment-etch.html｜家族 A｜4:3｜最小 1600×1200｜用途：設備範圍區塊配圖。

**Positive**

```
A scientific close-up looking down into an open plasma etch chamber: a circular electrostatic chuck
at the centre carrying one bare silicon wafer, surrounded by a precisely machined focus ring and a
symmetrical ring of small gas holes in the ceramic showerhead above; a faint even violet-pink glow
fills the chamber volume without hot spots, the metal interior showing fine radial machining marks
and a clean matte finish; perfectly perpendicular top-down framing, radial symmetry, 50mm macro,
f/5.6, even illumination, cool neutral base with a single restrained colour accent.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: fire, sparks, glowing filaments, molten metal, dirty chamber, deposits, corrosion,
lightning, science-fiction reactor, extreme bloom, off-centre chaotic composition
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 110`；強調 `radial symmetry, top-down` 可大幅提升成功率。

---

### IMG-ETCH-03｜`assets/img/etch-03.jpg`

- **一句話（zh）**：AI 視覺化——電漿模擬等值面與感測時序曲線並置。
- 頁面 equipment-etch.html｜家族 B｜16:9｜最小 2400×1350｜用途：AI 對標架構區塊配圖。

**Positive**

```
A two-part abstract simulation graphic on deep navy #101A2B: on the left, a cross-sectional field of
smooth nested iso-contour lines fills a rounded chamber outline, the contours drawn as hairlines
that shift gradually from teal #2FA9B8 at the periphery to soft violet #7B4CC0 at the core, spacing
tightening toward the centre; on the right, two long horizontal sensor traces run in parallel with a
clear rhythmic pattern and one sharp transition point marked by a thin vertical hairline that
extends across both traces; a single 1px spectral rule divides left and right; flat, exact, huge
negative space, no frames, no axes.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: jet or rainbow heatmap fill, volumetric smoke render, particle simulation,
glowing plasma photo, chart axes, tooltips, dashboards, 3d perspective
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 60`；與 `IMG-CVD-03` 共用「等值線＋曲線」骨架，可同 seed 微調。

---

## 7. equipment-cvd.html（化學氣相沉積）— CVD

### IMG-CVD-01｜`assets/img/cvd-01.jpg`

- **一句話（zh）**：直立式爐管設備外觀，管路與加熱段層次分明。
- 頁面 equipment-cvd.html｜家族 A｜16:9｜最小 2400×1350｜用途：頁首主視覺。

**Positive**

```
A photograph of a tall vertical furnace deposition tool standing in a bright cleanroom: the
cylindrical furnace body rises through the frame slightly right of centre, its stacked heating
zones readable as clean horizontal bands, with neatly bundled polished stainless gas lines running
vertically alongside in perfect parallel and turning through precise right angles; blank white
enclosure panels, no markings, one small green lamp; cool white diffuse ceiling light plus a soft
side key modelling the cylinder, deep navy-grey shadow side retaining detail; empty floor and wall
on the left, 35mm lens, f/5.6, verticals absolutely straight, minimal and monumental.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: steam, vapour clouds, rust, insulation wrap, chaotic piping, valves with tags,
industrial refinery look, warm sodium lighting, people, ladders
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 120`；強調 `parallel pipe runs, right angles` 讓構圖保持秩序感。

---

### IMG-CVD-02｜`assets/img/cvd-02.jpg`

- **一句話（zh）**：晶舟載入爐管瞬間特寫，多片晶圓整齊排列。
- 頁面 equipment-cvd.html｜家族 A｜4:3｜最小 1600×1200｜用途：設備範圍區塊配圖。

**Positive**

```
A close-up of a quartz wafer boat loaded with dozens of evenly spaced silicon wafers, captured at
the moment it rises into the mouth of a vertical furnace tube: the wafers read as a precise stack of
thin parallel discs, their edges catching a warm backlight from inside the tube while their faces
stay cool grey, the transparent quartz rods showing clean specular highlights; the furnace opening
frames the boat with a soft dark ring; shallow depth of field keeps the front wafer edges razor
sharp and lets the stack recede into softness; 50mm macro, f/2.8, warm-cool contrast held tight,
no glare.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: broken wafers, uneven spacing, glowing orange furnace like a kiln, flames,
dust, fingerprints, hands, plastic cassette, rainbow wafers
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 120`；晶圓間距須均勻，若出現不規則堆疊則重跑。

---

### IMG-CVD-03｜`assets/img/cvd-03.jpg`

- **一句話（zh）**：AI 視覺化——晶圓熱場等高線與膜厚均勻度色階圖。
- 頁面 equipment-cvd.html｜家族 B｜16:9｜最小 2400×1350｜用途：AI 對標架構區塊配圖。

**Positive**

```
An abstract analysis graphic on deep navy #101A2B, split into two aligned panels: the left panel
holds a large circle with smooth concentric thermal contour hairlines, slightly eccentric so the
rings bunch toward the lower right; the right panel holds an identical circle divided into a fine
polar sector grid, each sector filled with a very low-saturation step of a restrained teal-to-amber
scale to suggest film-thickness uniformity, sector borders as hairlines; both circles sit on the
same baseline with equal size and a wide gutter between; one thin spectral tick strip runs beneath
the right circle as an unlabelled scale; flat, clinical, generous margins.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: rainbow jet colormap, saturated heatmap, numeric scale, legend text, axis labels,
3d surface plot, glow, gradient background, dashboard panels
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 60`；色階務必低飽和，避免與 `IMG-EQP-03` 的彩虹搶眼。

---

## 8. equipment-bake.html（烘烤製程）— BAKE

### IMG-BAKE-01｜`assets/img/bake-01.jpg`

- **一句話（zh）**：熱盤與冷卻盤模組排列的設備上視圖，金屬表面與熱輻射感。
- 頁面 equipment-bake.html｜家族 A｜16:9｜最小 2400×1350｜用途：頁首主視覺。

**Positive**

```
An elevated three-quarter photograph looking down onto a bank of thermal process modules in a
coater-developer track: a row of circular hotplate and chill-plate stations set flush into a clean
brushed-aluminium deck, each station a precisely machined disc with a fine concentric turning
pattern and a narrow surrounding gap, lids raised in unison above them on slim posts; the metal
reflects the cool ceiling light in long soft streaks, one plate showing a faint warm thermal tint
at its centre; strict repetition and parallel alignment, empty deck area on the right, 35mm lens,
f/5.6, cool neutral grade, quiet industrial elegance.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: glowing red hot metal, visible heating elements, kitchen hotplate look, burnt
marks, scratches, steam, condensation, people, tangled wiring, warning symbols
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 120`；「熱」以極輕微色溫變化表現，不可畫成發紅金屬。

---

### IMG-BAKE-02｜`assets/img/bake-02.jpg`

- **一句話（zh）**：晶圓置於熱盤上的近距離特寫，表面熱擾動與細微光暈。
- 頁面 equipment-bake.html｜家族 A｜4:3｜最小 1600×1200｜用途：設備範圍區塊配圖。

**Positive**

```
A macro photograph of a single silicon wafer resting on proximity pins just above a polished
circular hotplate: the wafer's mirror surface reflects the module's clean interior, and a very
subtle heat shimmer distorts the reflection near the wafer edge; the hotplate beneath shows a fine
concentric machining pattern and three small pin shadows; framing is tight and slightly oblique so
the wafer edge cuts a clean arc across the frame, a soft cool highlight grazing that edge; 100mm
macro, f/4, extremely shallow focus falling off behind the wafer edge, cool neutral palette with a
whisper of warmth at the plate.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: strong mirage distortion, fire, glowing orange plate, water droplets, dust specks,
scratched wafer, tweezers, gloved hand, heavy rainbow reflection
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 120`；熱擾動要「幾乎看不見」，過強即失去精密感。

---

### IMG-BAKE-03｜`assets/img/bake-03.jpg`

- **一句話（zh）**：AI 視覺化——晶圓溫度輪廓熱圖與升降溫曲線並置。
- 頁面 equipment-bake.html｜家族 B｜16:9｜最小 2400×1350｜用途：AI 對標架構區塊配圖。

**Positive**

```
An abstract thermal analysis graphic on deep navy #101A2B: on the left, a circle filled with a
gentle two-tone temperature field rendered as fine stepped bands from cool teal #2FA9B8 through
neutral grey to warm amber #E9B23C, the warm zone offset toward the upper left, all band edges as
hairlines with no blur; on the right, three stacked ramp curves rise, hold a flat plateau, then fall,
each drawn as a single hairline in a different restrained hue, with faint dotted guide lines marking
the plateau level; a thin spectral rule runs along the bottom edge of the right panel; flat,
precise, spacious.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: rainbow jet colormap, fiery gradient, glow, blurred gaussian heatmap, temperature
numbers, degree symbols, axis labels, dashboard chrome, 3d surface
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 60`；與 `IMG-CVD-03` 須可辨差異：此圖用「階梯色帶＋升降溫曲線」，CVD 用「等高線＋極座標扇區」。

---

## 9. equipment-implant.html（離子植入）— IMP

### IMG-IMP-01｜`assets/img/imp-01.jpg`

- **一句話（zh）**：離子植入機長束線設備外觀，管線與磁鐵段的工業幾何感。
- 頁面 equipment-implant.html｜家族 A｜16:9｜最小 2400×1350｜用途：頁首主視覺。

**Positive**

```
A long lateral photograph of an ion implanter's beamline: a horizontal run of large cylindrical
vacuum sections, heavy analyser magnet housings and precisely flanged joints extends across the
full width of the frame at chest height, supported on a clean machine frame, all surfaces smooth
matte grey and white with no markings; behind it a plain cleanroom wall; the repetition of flanges
and bolt rings creates a strong rhythmic geometry, foreshortened slightly by a near-parallel camera
angle; cool white overhead light with one soft side key raking along the cylinders; empty space
above the beamline, 35mm lens, f/5.6, industrial, ordered, monumental.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: particle accelerator sci-fi look, glowing beams outside the machine, cables in
disarray, hazard radiation symbols, rust, people, laboratory clutter, warm tungsten light
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 120`；避免模型把它畫成粒子加速器科幻場景，必要時加 `--no sci-fi, glowing beam`。

---

### IMG-IMP-02｜`assets/img/imp-02.jpg`

- **一句話（zh）**：束線與晶圓端站特寫，藍色離子束軌跡以視覺化方式呈現。
- 頁面 equipment-implant.html｜家族 A＋B 混合（全站唯一）｜4:3｜最小 1600×1200｜用途：設備範圍區塊配圖。

**Positive**

```
A clean technical image of an ion implanter end station interior: a wafer held vertically on a
precise tilting platen faces the open mouth of the beamline tube on the left; a stylised ion beam is
represented not as photographic glow but as a bundle of perfectly straight thin cyan-blue #5CC8E8
hairlines travelling from the tube to the wafer surface, converging slightly, drawn with graphic
precision over the photographic hardware; the hardware itself is matte grey machined metal, cool
lit, blank of markings; composition strictly horizontal, wafer on the right third, generous dark
space above; 50mm lens, f/5.6, restrained.
+ STYLE-A suffix, with the beam element in STYLE-B graphic language
```

**Negative**

```
NEG-BASE, plus: laser beam glow, volumetric god rays, sparks, particle explosion, star wars energy
blast, lens bloom, purple beam, thick opaque beam, animated speed lines
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 90`；混合風格對模型較難，建議先生成無束線的硬體照，再以向量疊加細線束（後製最穩）。

---

### IMG-IMP-03｜`assets/img/imp-03.jpg`

- **一句話（zh）**：AI 視覺化——摻雜濃度剖面模擬圖與不確定性區間帶。
- 頁面 equipment-implant.html｜家族 B｜16:9｜最小 2400×1350｜用途：AI 對標架構區塊配圖。

**Positive**

```
An abstract simulation graphic on deep navy #101A2B: a single smooth asymmetric bell-shaped depth
profile curve sweeps across the centre as a 2px teal-blue #5CC8E8 hairline, its peak offset left;
around it, a soft translucent band of the same hue at very low opacity widens toward the tail to
represent an uncertainty interval, its edges drawn as fine dotted hairlines; below the curve, a thin
horizontal baseline with sparse unlabelled tick marks; at the left edge, a narrow vertical strip
shows a stack of five faint stepped bands sampled from the spectral gradient; nothing else, huge
negative space, flat and exact.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: axis numbers, legend, chart title, gridlines, excel look, glowing curve, neon,
particle trails, 3d plot, multiple overlapping charts, dashboard frame
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 55`；單曲線類圖形建議向量重繪，AI 生成常自動添加座標數字。

---

## 10. equipment-cmp.html（CMP 研磨）— CMP

### IMG-CMP-01｜`assets/img/cmp-01.jpg`

- **一句話（zh）**：CMP 研磨盤與研磨頭運轉特寫，研磨液流動、濕潤金屬表面反光。
- 頁面 equipment-cmp.html｜家族 A｜16:9｜最小 2400×1350｜用途：頁首主視覺。

**Positive**

```
A close documentary photograph of a chemical mechanical polishing platen in operation: a large
circular polishing pad with a fine radial groove pattern fills most of the frame, a cylindrical
carrier head pressing down at the upper right, and a slim dispense arm delivering a thin stream of
pale milky slurry that spreads into smooth wet sheets across the pad; the wet surface throws long
soft specular reflections of the cool ceiling light; motion is implied by the slurry's flow, not by
blur; stainless surrounding basin, spotless, no markings; slightly elevated angle, 35mm lens, f/5.6,
cool neutral grade, clean and wet and controlled.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: splashing mess, foam, dirty slurry residue, scratched pad, rust, motion blur
streaks, sparks, grinding sparks, workshop grinder look, people, hands
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 130`；避免模型聯想到「打磨機噴火花」，必要時加 `--no sparks, grinder`。

---

### IMG-CMP-02｜`assets/img/cmp-02.jpg`

- **一句話（zh）**：研磨後晶圓鏡面表面特寫，反射環境線條，展現平坦度。
- 頁面 equipment-cmp.html｜家族 A｜4:3｜最小 1600×1200｜用途：設備範圍區塊配圖。

**Positive**

```
A macro photograph of a freshly polished silicon wafer held at a shallow angle so its mirror surface
reflects the straight lines of a cleanroom ceiling as perfectly undistorted parallel bands, proving
its flatness; the wafer edge cuts a clean arc across the upper frame, a faint spectral diffraction
sheen appears only along that edge, the rest reading as pure cool silver-grey; the background is a
soft dark graphite gradient with no detail; extremely fine surface texture visible on close
inspection, no defects; 100mm macro, f/8, edge-to-edge sharpness on the reflection lines, cool
neutral grade.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: scratches, swirl marks, water spots, fingerprints, dust, wavy distorted reflection,
oil-slick colours, chrome ball look, gloved hand, tweezers, background clutter
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 120`；反射線條必須筆直——扭曲即代表「不平坦」，語意錯誤，須重跑。

---

### IMG-CMP-03｜`assets/img/cmp-03.jpg`

- **一句話（zh）**：AI 視覺化——晶圓移除率分布圖與良率預測指標卡並置。
- 頁面 equipment-cmp.html｜家族 B｜16:9｜最小 2400×1350｜用途：AI 對標架構區塊配圖。

**Positive**

```
An abstract analytics graphic on deep navy #101A2B: on the left, a circle divided into a fine
concentric-ring and radial-sector mesh, each cell filled with a very low-saturation step from a
narrow teal-to-grey scale so a smooth centre-to-edge gradient emerges, cell borders as hairlines;
on the right, three stacked rectangular cards in slightly lighter navy #16202F, each holding one
abstract element only — a short horizontal bar, a small ring gauge, a tiny sparkline — all in
hairline strokes with a single teal accent, and absolutely no numerals or text; a hairline spectral
rule sits above the card stack; wide gutters, strict grid, flat and quiet.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: numbers, percentages, KPI values, chart titles, legends, buttons, window chrome,
browser frame, glassmorphism, neon glow, rainbow heatmap, photorealistic monitor
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 55`；此圖與 `IMG-INSP-03`、`IMG-AI-03` 同屬「無文字儀表語彙」，需彼此構圖有別。

---

## 11. equipment-cleaning.html（晶圓水洗）— CLEAN

### IMG-CLEAN-01｜`assets/img/clean-01.jpg`

- **一句話（zh）**：單片式清洗腔體內晶圓高速旋轉、藥液呈環狀噴灑。
- 頁面 equipment-cleaning.html｜家族 A｜16:9｜最小 2400×1350｜用途：頁首主視覺。

**Positive**

```
A photograph looking down into a single-wafer spin-clean chamber: a wafer spins on a chuck at the
centre while a swing arm dispenses clear chemistry onto its surface, the liquid flinging outward
into a perfectly even circular sheet and a fine ring of droplets caught crisply at the wafer edge;
a thin water film on the wafer produces soft concentric highlights; the chamber's white polymer
bowl is spotless with smooth radial contours; overhead cool white light, everything clean and
controlled; top-down framing with slight offset, 35mm lens, f/5.6, fast shutter freezing the
droplet ring, cool neutral grade with pure white highlights.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: foam, bubbles, soap suds, dirty water, stains, chaotic splashing, motion blur
smear, steam clouds, hands, kitchen sink look, yellow tinted liquid
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 130`；`fast shutter, frozen droplets` 是關鍵詞，否則易出現糊掉的水花。

---

### IMG-CLEAN-02｜`assets/img/clean-02.jpg`

- **一句話（zh）**：清洗後晶圓乾燥出料的瞬間，表面無水痕、冷白潔淨環境。
- 頁面 equipment-cleaning.html｜家族 A｜4:3｜最小 1600×1200｜用途：設備範圍區塊配圖。

**Positive**

```
A clean photograph of a wafer transfer robot end-effector withdrawing a perfectly dry silicon wafer
from a cleaning module's open port: the wafer is horizontal, its mirror surface uniform and free of
any water marks, catching one smooth soft highlight from the module's interior light; the slim
ceramic blade of the end-effector supports it from below with precise clearance; the module's white
interior recedes into soft focus behind; framing is horizontal and calm with the wafer occupying the
lower two-thirds and clean empty space above; 50mm lens, f/4, cool white balance, pristine.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: water droplets, drying stains, streaks, condensation, steam, gloved human hand
carrying wafer, cassette clutter, dark background, warm light, dust motes in the air
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 120`；「無水痕」是本圖的敘事重點，任何水珠都必須排除。

---

### IMG-CLEAN-03｜`assets/img/clean-03.jpg`

- **一句話（zh）**：AI 視覺化——SEM 缺陷影像網格與分類信心度標註。
- 頁面 equipment-cleaning.html｜家族 B｜16:9｜最小 2400×1350｜用途：AI 對標架構區塊配圖。

**Positive**

```
An abstract classification graphic on deep navy #101A2B: a strict grid of twelve equal square tiles
with wide gutters, each tile containing a different abstract greyscale micro-texture suggestive of
electron-microscope imagery — fine granular noise, a curved ridge, a small cluster of dots, a linear
scratch-like feature — all monochrome and low contrast; three tiles are marked with a 1px teal-blue
#5CC8E8 selection frame and one tile with a thin amber #E9B23C frame; beneath each marked tile sits
a very short unlabelled progress bar segment in a single spectral hue; everything flat, aligned,
text-free, generous margins.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: percentages, confidence numbers, class names, bounding box labels, cursor,
UI panels, real SEM photographs with scale bars, colourised electron micrographs, neon glow
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 60`；SEM 質感必須抽象、不可看起來像真實檢測資料，以免被誤讀為客戶資料。

---

## 12. equipment-inspection.html（晶圓檢測）— INSP

### IMG-INSP-01｜`assets/img/insp-01.jpg`

- **一句話（zh）**：檢測機台與晶圓載入端特寫，螢幕上顯示晶圓圖，冷藍色調。
- 頁面 equipment-inspection.html｜家族 A｜16:9｜最小 2400×1350｜用途：頁首主視覺。

**Positive**

```
A photograph of a wafer inspection tool's load port area: a smooth white FOUP carrier seated on the
port at the left, the tool's blank enclosure rising behind it, and a wall-mounted operator display
on the right whose screen shows only a soft out-of-focus circular pattern of cool blue-grey dots
with no legible content; the room is lit cool and low, the screen providing a gentle blue key that
grades the nearby panels; strong horizontal composition, empty panel space in the upper third,
35mm lens, f/2.8, load port sharp and screen softly defocused, cool blue-leaning neutral grade.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: readable screen UI, menus, toolbars, numbers on display, keyboard and mouse,
office desk, people, warm lighting, monitor brand bezel markings, reflection of a photographer
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 130`；螢幕務必失焦，避免任何可讀介面（DESIGN.md 禁止假 UI）。

---

### IMG-INSP-02｜`assets/img/insp-02.jpg`

- **一句話（zh）**：晶圓圖缺陷分布視覺化貼近螢幕拍攝，色點群聚形成特徵圖樣。
- 頁面 equipment-inspection.html｜家族 A｜4:3｜最小 1600×1200｜用途：設備範圍區塊配圖。

**Positive**

```
An extreme close-up photograph of a high-quality display panel showing an abstract wafer map: a
large circle composed of a fine orthogonal grid of tiny square cells, most cells dark navy, a
scattered minority glowing in restrained teal and a small arc-shaped cluster in soft amber near the
edge; the camera sits close and slightly oblique so the panel's subpixel structure is faintly
visible at the nearest edge, giving a tactile screen texture; no interface elements of any kind
surround the circle, only dark screen; 50mm macro, f/2.8, focus on the cluster, gentle falloff, cool
grade, dark and quiet.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: menus, toolbars, window borders, cursor, tooltips, legends, colour scale, numbers,
moiré artefacts, screen glare, dust on screen, rainbow jet colormap, reflections of a room
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 110`；若出現嚴重摩爾紋，改以 B 家族純圖形方式重製。

---

### IMG-INSP-03｜`assets/img/insp-03.jpg`

- **一句話（zh）**：AI 視覺化——晶圓圖缺陷分類結果與信心度長條圖並置。
- 頁面 equipment-inspection.html｜家族 B｜16:9｜最小 2400×1350｜用途：AI 對標架構區塊配圖。

**Positive**

```
An abstract classification result graphic on deep navy #101A2B: on the left, a wafer circle built
from a fine square-cell grid, most cells near-invisible dark, with one clear ring-shaped defect
signature picked out in teal cells and a small edge cluster in amber cells; on the right, five
horizontal bars of decreasing length stacked with equal rhythm, each a plain hairline-outlined bar
with a partial fill, the top bar filled in teal-blue #5CC8E8 and the rest in muted grey; no labels,
no numbers, no axis; a 1px spectral rule sits beneath the bar group; wide gutter between the two
halves, strict alignment, flat and calm.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: class names, percentage values, legends, tooltips, dashboard chrome, gridlines,
3d bars, gradients inside bars, glow, neon, rainbow palette
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 55`；長條圖易被模型加上數字，DALL·E 3 必須明確禁止文字。

---

## 13. equipment-mask.html（掩模版製程）— MASK

### IMG-MASK-01｜`assets/img/mask-01.jpg`

- **一句話（zh）**：光罩盒與石英掩模版特寫，表面反射細密圖形，暗場照明。
- 頁面 equipment-mask.html｜家族 A｜16:9｜最小 2400×1350｜用途：頁首主視覺。

**Positive**

```
A dark-field studio photograph of a square quartz photomask resting inside an opened protective
pod: the mask's chrome pattern reads as an extremely fine dense micro-structure that catches a
single raking light and returns a soft directional shimmer with faint spectral edges, while the
surrounding pod surfaces stay deep matte graphite; the composition is nearly top-down with the mask
rotated a few degrees off axis, its clean bevelled edges catching thin bright lines; background
falls to near-black with retained detail, generous empty space at the left; 100mm macro, f/8, tack
sharp on the pattern, cool grade, jewel-like restraint.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: readable circuit patterns, alignment mark text, barcodes on pod, fingerprints,
dust, scratches, rainbow oil slick, glass paperweight look, colourful backlighting, hands
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 140`；暗場照明是本圖辨識度來源，`dark-field, single raking light` 為必要關鍵詞。

---

### IMG-MASK-02｜`assets/img/mask-02.jpg`

- **一句話（zh）**：電子束寫入機台外觀與真空腔體，冷白光、精密機構細節。
- 頁面 equipment-mask.html｜家族 A｜4:3｜最小 1600×1200｜用途：設備範圍區塊配圖。

**Positive**

```
A photograph of an electron-beam writer tool: a tall cylindrical column rises from a massive
vibration-isolated base, the vacuum chamber below it ringed with precisely bolted flanges and
polished stainless ports, all surfaces matte grey and blank of markings; the column's stacked
segments create a clear vertical rhythm; shot from a low three-quarter angle to emphasise mass and
precision, cool white cleanroom light with one soft side key defining the cylinder, deep navy
shadows with detail; plain wall behind, empty space at the top; 35mm lens, f/5.6, verticals
perfectly straight.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: laboratory clutter, gas cylinders, cables on floor, warning labels, control
monitors with content, people, warm lighting, sci-fi glow, rust, tape and handwritten notes
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 120`；與 `IMG-CVD-01` 同為「直立柱體設備」，須以角度與光位明顯區隔（此圖低角度、CVD 為平視）。

---

### IMG-MASK-03｜`assets/img/mask-03.jpg`

- **一句話（zh）**：AI 視覺化——光罩圖形 ILT 修正前後對照，疊加熱點預測色塊。
- 頁面 equipment-mask.html｜家族 B｜16:9｜最小 2400×1350｜用途：AI 對標架構區塊配圖。

**Positive**

```
A side-by-side comparison graphic on deep navy #101A2B: two equal square panels separated by a
hairline vertical rule; the left panel shows a simple orthogonal layout figure of clean rectangles
in pale grey hairlines; the right panel shows the same figure transformed into a curvilinear
inverse-lithography style shape with rounded corners, added serifs and small assist features, drawn
in the same hairline weight but outlined in teal-blue #5CC8E8; two small regions in the left panel
carry low-opacity amber #E9B23C hotspot patches that are absent on the right; a short spectral
segment marks the top edge of the right panel; flat, exact, wide margins, no annotations.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: before and after labels, arrows with text, captions, legends, chip photograph,
PCB traces, glow, 3d extrusion, rainbow heatmap, cluttered pattern density
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 60`；左右兩圖必須明顯同源但形態不同（直角 vs 曲線化），這是 ILT 的視覺重點。

---

## 14. ai.html（AI 智慧製造）— AI

### VID-AI-01（海報）｜`assets/img/ai-01-poster.jpg`

- **一句話（zh）**：`VID-AI-01` 的海報影格——熱場與缺陷點雲尚未收斂的中段靜幀。
- 頁面 ai.html｜家族 B｜16:9｜最小 2400×1350｜用途：影片載入前的靜態畫面，須與影片同一視覺系統。

**Positive**

```
A frame from an abstract data animation, rendered as a still on deep navy #101A2B: a large wafer
circle centred slightly left, overlaid by flowing thermal contour hairlines that curve like a field
in motion, and a scattered point cloud of small dots across the wafer, roughly half of them already
gathered into two tight clusters while the rest remain dispersed; clustered dots take a single
teal-blue #5CC8E8 and a single amber #E9B23C, unclustered dots stay pale grey; a hairline spectral
arc traces part of the wafer edge; wide empty navy space on the right, flat, no glow, no motion blur.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: motion blur, streaks, particle glow, bloom, depth of field, 3d render, neon,
chart axes, labels, dashboard, brain network cliché
```

- **Model notes**：MJ `--ar 16:9 --style raw --stylize 60`；最佳做法是直接自 `VID-AI-01` 第 3–4 秒抽格輸出；若以本提示詞生成，也可作為影片的 first-frame 條件圖。

---

### IMG-AI-01｜`assets/img/ai-01.jpg`

- **一句話（zh）**：晶圓與神經網路節點疊合的抽象靜態主視覺。
- 頁面 ai.html｜家族 B｜4:3｜最小 1600×1200｜用途：AI 頁主視覺。**本圖為 B 家族的風格基準圖，請最先生成。**

**Positive**

```
A minimal abstract hero graphic on deep navy #101A2B: a single large hairline wafer circle sits
right of centre, its interior carrying a very faint orthogonal die grid; across and beyond it, a
sparse three-layer node network is drawn with small solid dots and ultra-thin straight edges, the
layers reading left to right with uneven, deliberately non-symmetrical connections; only three
edges carry the spectral gradient, everything else pale grey; one 1px teal-blue #5CC8E8 arc follows
part of the wafer circumference; the left third is completely empty for typography; flat, exact,
spacious, no glow, no depth cues.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: dense neural net mesh, glowing synapses, brain imagery, human silhouette with
network head, circuit board, starfield, particle system, blue gradient wash, 3d spheres, bokeh
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 50`，固定 `--seed` 並作為全站 B 家族的 `--sref`；Flux guidance 3.5。

---

### IMG-AI-02｜`assets/img/ai-02.jpg`

- **一句話（zh）**：數字孿生、物理仿真、生成式微影三種視覺語彙並置的三欄式抽象插畫。
- 頁面 ai.html｜家族 B｜21:9｜最小 2520×1080｜用途：三大技術主軸區塊配圖。

**Positive**

```
An ultra-wide triptych graphic on cool off-white #F6F7F8, three equal panels separated by hairline
vertical rules: the left panel shows two identical simplified tool outlines side by side, one solid
grey and one dashed teal, linked by short horizontal tie lines to suggest a twin; the middle panel
shows a rounded chamber outline filled with smooth nested iso-contour hairlines; the right panel
shows one orthogonal rectangle transforming into a curvilinear outline with small assist shapes
beside it; all drawing in 1.5px strokes, single accent teal-blue #0C6B8F, one short spectral
segment under each panel; enormous white space, strict alignment, no labels.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: panel titles, captions, icon labels, numbers, dividing coloured backgrounds,
drop shadows, 3d perspective, gradients, glow, decorative illustration style
```

- **Model notes**：MJ `--ar 21:9 --style raw --stylize 50`；三欄比例須嚴格相等，若模型失衡可改生成三張 1:1 再拼接。

---

### IMG-AI-03｜`assets/img/ai-03.jpg`

- **一句話（zh）**：AI 導入流程看板風格——五階段卡片與抽象指標，深色 UI。
- 頁面 ai.html｜家族 B｜4:3｜最小 1600×1200｜用途：AI 導入流程區塊配圖。

**Positive**

```
An abstract dark board-style layout on deep navy #101A2B, with no window chrome and no text: five
equal vertical cards in slightly lighter navy #16202F arranged in a single row with even gutters,
each card containing only a small hairline pictogram at the top (a magnifier ring, a chamber, a
node graph, a wafer circle, an open book shape) and two short grey placeholder rules beneath it,
plus a thin horizontal progress bar at the card's foot; the first three progress bars are filled in
teal-blue #5CC8E8 to different extents, the rest empty; one continuous hairline spectral rule runs
across the top of all five cards; flat, aligned to a strict grid, spacious.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: lorem ipsum, readable text, numbers, percentages, buttons, avatars, browser window,
tabs, glassmorphism, drop shadows, neon glow, kanban card clutter, screenshot bezel
```

- **Model notes**：MJ `--ar 4:3 --style raw --stylize 55`；「placeholder rules」是關鍵——以灰色細線代替文字，可有效避免模型生成亂碼字。

---

## 15. contact.html（聯絡我們）— CONTACT

### IMG-CONTACT-01｜`assets/img/contact-01.jpg`

- **一句話（zh）**：九龍佐敦街廓的極簡線稿地圖，單一標記點指向辦公大樓。
- 頁面 contact.html｜家族 B｜21:9｜最小 2520×1080｜用途：辦公室位置區塊寬帶配圖。

**Positive**

```
An ultra-wide stylised map graphic on cool off-white #F6F7F8: an abstracted dense urban block
pattern of a harbour-side Asian district spans the full width, blocks as flat pale grey #EFF1F3
shapes with hairline outlines, three main avenues cutting through as wider white channels, a
waterfront band sweeping across the upper left corner as a single soft grey plane with a hairline
edge; one solid teal-blue #0C6B8F dot with two thin concentric rings marks a location just right of
centre; a single hairline spectral rule runs along the very bottom edge of the frame; flat
orthographic top-down, huge margins, no terrain, no shadows, no labels.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: street names, district labels, map service styling, compass, scale bar, pin icons
with shadows, satellite photo, 3d buildings, green parks, blue water fill, traffic lines
```

- **Model notes**：MJ `--ar 21:9 --style raw --stylize 50`；**僅為風格化示意，不作導航用途**；為確保零文字，建議最終以向量工具重繪。

---

### IMG-CONTACT-02｜`assets/img/contact-02.jpg`

- **一句話（zh）**：現代辦公空間會議情境的冷調照片，桌上攤開設備規格文件。
- 頁面 contact.html｜家族 A｜21:9｜最小 2520×1080｜用途：頁首／聯絡情境配圖。

**Positive**

```
A calm ultra-wide letterbox interior photograph of a modern meeting room, the composition spread
horizontally across the frame: a light grey table runs diagonally from the lower left, carrying loosely arranged technical document sheets with unreadable fine line drawings,
a closed notebook and a slim pen; two empty upholstered chairs sit at the far side; behind them a
floor-to-ceiling window with vertical mullions lets in soft overcast daylight and shows a
low-contrast blur of city towers; walls plain, no decoration, no artwork; no people in frame;
35mm lens, f/4, focus on the documents, background gently soft, cool neutral grade, quiet and
professional.
+ STYLE-A suffix
```

**Negative**

```
NEG-BASE, plus: people, hands, faces, legible documents, printed logos, whiteboard writing,
plants, coffee cups clutter, warm cosy lighting, wooden furniture, motivational posters,
video conference screen with a call in progress
```

- **Model notes**：MJ `--ar 21:9 --style raw --stylize 120`；若模型放入人物，加 `--no people, person`。

---

### IMG-CONTACT-03｜`assets/img/contact-03.jpg`

- **一句話（zh）**：深藍底上的細線光譜漸層橫紋，作為頁尾前的抽象視覺分隔。
- 頁面 contact.html｜家族 B｜21:9｜最小 2520×1080｜用途：頁尾前品牌視覺分隔帶。

**Positive**

```
An ultra-wide minimal brand graphic on deep navy graphite #101A2B: a set of about twenty perfectly
horizontal hairlines spanning the full width, unevenly spaced with large gaps in the upper area and
tighter clustering toward the lower third; most lines are very low-contrast grey, while five of
them carry the spectral gradient at low opacity, each line's colour sweeping smoothly from red
through amber, green, teal to violet across the frame width; the lines never touch and never form a
block of colour; the overall impression is a whisper of diffraction, not a rainbow band; absolutely
flat, no glow, no texture, no noise.
+ STYLE-B suffix
```

**Negative**

```
NEG-BASE, plus: solid rainbow band, thick colourful stripes, gradient background fill, neon glow,
lens flare, prism illustration, light streaks, blur, grain, vaporwave aesthetic
```

- **Model notes**：MJ `--ar 21:9 --style raw --stylize 40`；此圖是全站「光譜線」規則的極致示範，彩色面積必須極小；亦可完全以 CSS/SVG 重繪。

---

## 16. 涵蓋確認（Coverage Check）

| 頁面 | 資產 |
|---|---|
| index.html | IMG-HOME-01、IMG-HOME-02、IMG-HOME-03、IMG-HOME-04、VID-HOME-01（海報）`home-01-poster.jpg` |
| about.html | IMG-ABOUT-01～04 |
| services.html | IMG-SVC-01～04 |
| equipment.html | IMG-EQP-01～03 |
| equipment-lithography.html | IMG-LITHO-01～03 |
| equipment-etch.html | IMG-ETCH-01～03 |
| equipment-cvd.html | IMG-CVD-01～03 |
| equipment-bake.html | IMG-BAKE-01～03 |
| equipment-implant.html | IMG-IMP-01～03 |
| equipment-cmp.html | IMG-CMP-01～03 |
| equipment-cleaning.html | IMG-CLEAN-01～03 |
| equipment-inspection.html | IMG-INSP-01～03 |
| equipment-mask.html | IMG-MASK-01～03 |
| ai.html | IMG-AI-01～03、VID-AI-01（海報）`ai-01-poster.jpg` |
| contact.html | IMG-CONTACT-01～03 |

**合計：48 個 `IMG-*` 資產 ＋ 2 張影片海報 ＝ 50 張靜態圖，與 `docs/content-spec.md` §16 完全一致，無遺漏。**
