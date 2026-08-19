# 倍特爾科技集團官網 — 影片生成提示詞（Video Prompts）

> 對應檔案：`docs/content-spec.md` §16 資產索引、`DESIGN.md` §8 影像方向、§6.8 媒體佔位規範。
> 本檔涵蓋 **2 個 `VID-*` 站內資產**（`VID-HOME-01`、`VID-AI-01`），另附 **2 支選用彩蛋短片**（未被網站引用）。
> 說明文字為繁體中文；**生成提示詞一律使用英文**（影片模型對英文提示的理解與可控性最佳）。
> 檔名規則：`VID-<PAGE>-<NN>` → `assets/video/<page小寫>-<nn>.mp4`；海報 → `assets/img/<page小寫>-<nn>-poster.jpg`。

---

## 0. 全站影片規格與一致性（Global Spec）

### 0.1 交付規格（兩支站內影片皆同）

| 項目 | 規格 |
|---|---|
| 容器／編碼 | MP4 ／ H.264 High Profile（相容性優先；如另備 WebM/VP9 為選配） |
| 音軌 | **無音軌**（完全移除 audio track，不是靜音軌） |
| 幀率 | 24 fps（生成端若為 30 fps 亦可，但同一支片內不得變速） |
| 位元率 | 4–6 Mbps（1080p）／ 2–3 Mbps（720p 備援） |
| 解析度 | 主檔 1920×1080；行動備援可另存 1280×720 |
| 檔案大小 | **單支 ≤ 6 MB**（首頁 hero 影片建議 ≤ 4 MB），必要時縮短或降位元率 |
| 長度 | 6–12 秒 |
| 迴圈 | **必須 loop-safe**：末幀與首幀在構圖、亮度、物件位置上可無縫銜接，播放時不得出現跳接 |
| 播放屬性 | 站內以 `autoplay muted loop playsinline preload="metadata"` 播放，並提供 `poster`；`prefers-reduced-motion` 時不自動播放 |
| 色彩 | Rec.709、無 HDR；與圖片同一調性（冷中性、降飽和 10–15%） |
| 畫面內文字 | **零文字**（不得有任何字幕、標籤、浮水印、品牌銘牌） |

### 0.2 共用視覺語彙

- 影片必須與 `docs/image-prompts.md` 的兩個視覺家族一致：`VID-HOME-01` 屬 **A 家族紀實攝影**，`VID-AI-01` 屬 **B 家族極簡技術圖形**。
- 運鏡只允許三種：**極慢橫移（dolly / truck）**、**極慢推進（push-in）**、**靜止機位＋畫面內部運動**。不得使用旋轉、環繞、手持晃動、無人機爬升、變焦拉扯、鏡頭甩動。
- 全片速度感恆定，不得有加速／減速的戲劇化節奏；無轉場特效、無閃白、無鏡頭光斑。
- 光譜色僅以極細線或極小點出現，任何時刻的彩色面積不得超過畫面約 3%。

### 0.3 共用負面提示詞（VNEG-BASE）

```
text, letters, words, subtitles, captions, numbers, labels, watermark, timecode, logo,
brand nameplate, manufacturer marking, UI overlay, HUD, holographic projection, sci-fi interface,
camera shake, handheld wobble, whip pan, crash zoom, orbit shot, drone ascent, dutch angle,
fast cuts, scene change, transition wipe, flash frame, strobing, flicker, exposure pumping,
lens flare, bloom, light leaks, purple neon, cyberpunk grade, teal-and-orange grade, oversaturation,
morphing objects, warping geometry, objects appearing or disappearing, duplicated limbs,
distorted hands, extra fingers, recognisable faces, people looking at camera, handshake,
smoke, sparks, fire, water splash chaos, dust particles floating, motion blur smear,
cartoon, anime, 3d clay render, plastic look, low resolution, jpeg artifacts, upscaling artifacts
```

### 0.4 海報影格（Poster）的選取原則

| 原則 | 說明 |
|---|---|
| 取首格或近首格 | 海報應等於影片的第 0 幀（或第 1–12 幀內），使影片開始播放時無視覺跳動。 |
| 構圖完整 | 該幀必須自身即為一張合格的靜態圖（構圖成立、留白足夠給 HTML 文案）。 |
| 無運動殘影 | 避開任何有動態模糊或元素半途移動的幀。 |
| 尺寸與命名 | 1920×1080（16:9）JPEG，品質 82–88，sRGB，去 EXIF，檔名嚴格為 `assets/img/<page>-<nn>-poster.jpg`；抽格後放進 `assets/img/` 並執行 `python tools/optimize_media.py`，即自動轉成交付規格。 |
| 備援 | 若影片未產出或載入失敗，海報即為該版位的靜態視覺；提示詞另見 `docs/image-prompts.md` 對應段落。 |

---

## 1. VID-HOME-01 — 首頁 hero 無塵室長鏡頭

| 項目 | 內容 |
|---|---|
| 資產 ID | `VID-HOME-01` |
| 頁面 | `index.html`（§1.1 hero） |
| 影片檔 | `assets/video/home-01.mp4`（H.264，無音軌，loop-safe） |
| 海報檔 | `assets/img/home-01-poster.jpg` |
| 長度 | 10 秒（可接受 8–12 秒） |
| 比例／解析度 | 16:9 ／ 1920×1080 |
| 家族 | A（紀實攝影） |
| 一句話（zh） | 無塵室設備列的極慢橫移長鏡頭，機械手臂與艙門在畫面內安靜運作。 |

### 分鏡（Shot list）

單鏡到底，不切。
`0–2s` 設備列靜置，機械手臂處於待命位置 → `2–6s` 攝影機以恆定速度向右橫移約半個機台寬度，同時左側機台的傳輸手臂完成一次緩慢的取放動作 → `6–9s` 一扇載入埠艙門緩緩闔上 → `9–10s` 攝影機停穩、手臂回到與第 0 幀完全相同的待命位置，構圖回到起點。

### Positive prompt

```
A single continuous 10-second locked-composition shot inside a semiconductor cleanroom equipment
aisle. Two rows of tall white process tools recede toward a distant vanishing point down a polished
light-grey epoxy floor; a perforated ceiling filter grid runs overhead; all machine panels are
smooth, blank and unmarked. The camera performs one extremely slow, perfectly smooth lateral dolly
to the right on a rail, travelling only a short distance at constant speed, verticals staying
absolutely straight. Inside a clean glass access panel on the nearest tool, a robotic wafer transfer
arm executes one slow deliberate pick-and-place motion and returns to its rest position. A load-port
door on a second tool closes gently. Lighting is even cool-white ceiling illumination with soft
floor reflections; a single small amber indicator lamp is the only warm accent. No people anywhere.
Cool neutral grade, saturation reduced, deep navy-graphite shadows with full detail, soft
unclipped highlights, calm and precise documentary cinematography, shallow-to-medium depth of field
on a 35mm lens at f/4, cinematic 24fps, no text of any kind in frame.
```

### Negative prompt

```
VNEG-BASE, plus: people, engineers walking, hands entering frame, fast robot motion, spinning
machinery, blinking warning lights, alarm strobe, open maintenance panels, exposed cables,
yellow lithography lighting over the whole scene, warm interior grade, doors opening and closing
repeatedly, camera pushing forward, zoom, rotation, ceiling collapse, reflections of a film crew
```

### 模型注記（Runway Gen-4 / Kling / Veo 3 / Sora）

| 模型 | 建議做法 |
|---|---|
| **Runway Gen-4** | 用 `assets/img/home-01-poster.jpg`（或依 `image-prompts.md` 生成的同構圖靜圖）作為 **first frame**，並在 Motion 設定選 minimal camera motion；Gen-4 的 first/last frame 功能可將**同一張圖同時設為首尾幀**，是取得無縫迴圈最穩的做法。 |
| **Kling 1.6 / 2.x** | 使用「首尾幀」模式並上傳同一張圖；Motion Strength 設低（約 0.3），Camera Movement 選「Horizontal / Right」且幅度最小；Kling 對機械運動的物理一致性較佳。 |
| **Veo 3** | 以純文字提示即可，務必在提示中明確寫 `no audio`（Veo 預設會生成音訊，交付前必須移除音軌）；`camera: slow lateral dolly right, locked horizon`。 |
| **Sora** | 對「單鏡不切」遵循度好，但易自行加入人物；在提示尾端重複一次 `absolutely no people in the frame`。 |
| 迴圈製作 | 若模型無首尾幀功能：生成 12 秒 → 取用中段 10 秒 → 以 0.4 秒交叉溶接（cross-dissolve）首尾，或採 boomerang（正播＋倒播）方式；本鏡的橫移＋回位設計即為 boomerang 友善。 |
| 常見失敗 | 手臂動作過快、機台面板長出字樣、地板出現人影。出現任一項即重跑，不做後製補救。 |

### 海報影格

取第 0 幀（攝影機尚未移動、手臂在待命位）。該幀構圖須在下三分之一保留空白供 hero 文案；輸出為 `assets/img/home-01-poster.jpg`。

---

## 2. VID-AI-01 — AI 頁抽象資料動畫

| 項目 | 內容 |
|---|---|
| 資產 ID | `VID-AI-01` |
| 頁面 | `ai.html`（§14.1 hero） |
| 影片檔 | `assets/video/ai-01.mp4`（H.264，無音軌，loop-safe） |
| 海報檔 | `assets/img/ai-01-poster.jpg` |
| 長度 | 8 秒（可接受 6–10 秒） |
| 比例／解析度 | 16:9 ／ 1920×1080 |
| 家族 | B（極簡技術圖形） |
| 一句話（zh） | 晶圓上流動的熱場與散落的缺陷點雲，逐步收斂成兩個清晰的分類群集，再回到起始狀態。 |

### 分鏡（Shot list）

固定機位、無攝影機運動，全部動態發生在畫面內部。
`0–2s` 深藍底上出現晶圓細線圓形與淡淡的晶粒網格；熱場等高線緩慢流動，缺陷點雲均勻散落且輕微漂移 → `2–5s` 點雲開始收斂，逐步聚成兩個群集，被歸類的點依序轉為單一青藍與單一琥珀 → `5–7s` 兩個群集邊緣浮現 1px 細線圈選；晶圓邊緣一小段光譜弧線由左向右掃過一次 → `7–8s` 群集重新鬆開、顏色褪回灰白、點雲回到第 0 幀的分布，準備無縫循環。

### Positive prompt

```
An 8-second abstract data-visualisation animation, static camera, flat two-dimensional graphic
design language on a deep navy graphite background (#101A2B). A single large hairline circle
representing a silicon wafer sits slightly left of centre, its interior carrying a very faint
orthogonal die grid. Smooth nested thermal contour hairlines drift slowly across the wafer like a
gently evolving field. A scattered cloud of small dots covers the wafer surface, drifting almost
imperceptibly, then gradually and organically converging into two tight clusters; as each dot joins
a cluster it changes from pale grey to either a single teal-blue (#5CC8E8) or a single amber
(#E9B23C). Thin 1px outlines fade in around the two clusters. A short spectral gradient arc sweeps
once along part of the wafer's circumference from left to right. Finally the clusters relax, colours
fade back to pale grey and the dots return to their original scattered positions, so the last frame
matches the first exactly. Everything is flat with hairline strokes, wide empty margins, generous
negative space on the right, no glow, no bloom, no depth of field, no 3D, no perspective, no text,
no labels, no numbers, no axes. Calm, clinical, premium engineering aesthetic, constant pacing,
24fps.
```

### Negative prompt

```
VNEG-BASE, plus: glowing particles, bloom, lens dirt, volumetric light, 3d rendering, camera moves,
parallax, rotating wafer, neural brain imagery, human silhouette, circuit board traces, starfield,
rainbow jet colormap, dashboard panels, chart axes, tooltips, cursor, numbers counting up,
typing animation, data streams of characters, matrix code rain, ripple distortion, glitch effect
```

### 模型注記（Runway Gen-4 / Kling / Veo 3 / Sora）

| 模型 | 建議做法 |
|---|---|
| **Runway Gen-4** | 以 `assets/img/ai-01-poster.jpg` 或 `assets/img/ai-01.jpg` 作為 first frame，**並將同一張圖設為 last frame**，即可天然無縫迴圈；Motion Strength 設低，避免點雲抖動過大。 |
| **Kling 2.x** | 首尾同圖模式；此類平面圖形動畫 Kling 容易加入立體感與光暈，提示中須反覆強調 `flat 2d vector graphic, no glow, no depth`。 |
| **Veo 3** | 文字提示表現佳，但同樣預設生成音訊，交付前務必移除；可加 `style: flat motion graphics, After Effects look`。 |
| **Sora** | 對「抽象非寫實圖形」較易自行加入寫實質感；若結果偏 3D，改用首尾幀導向的模型。 |
| **最穩做法** | 本片本質是 motion graphics，**以 After Effects／SVG＋CSS 動畫手工製作可 100% 控制迴圈與色彩**，AI 生成僅建議作為動態節奏的參考稿。若手工製作，直接以 `IMG-AI-01` 的圖形為基底做點雲收斂與弧線掃過。 |
| 常見失敗 | 收斂動作過快（應慢到近乎察覺不到）、群集顏色超過兩種、光譜弧線變成大面積彩帶、末幀與首幀不一致。 |

### 海報影格

取第 0 幀（點雲尚未收斂、顏色仍為灰白），對應 `docs/image-prompts.md` 之「IMG-AI-01（海報）」提示詞；輸出為 `assets/img/ai-01-poster.jpg`，右側須保留空白供 hero 文案。

---

## 3. 選用彩蛋片（Optional — 網站目前不引用）

> 以下兩支 **不在 `docs/content-spec.md` 的資產索引中**，網站頁面不得引用、佔位框不得指向它們。
> 僅供簡報、展會循環播放、社群或未來版本使用。若日後要上站，須先在 content-spec 增列資產 ID。

### OPT-VID-01（選用）— 品牌片頭短片（Brand Sting）

| 項目 | 內容 |
|---|---|
| 建議檔名 | `assets/video/optional-brand-sting.mp4`（**不放入 `assets/video/<page>-<nn>.mp4` 命名空間**） |
| 長度 | 6 秒 |
| 比例／解析度 | 16:9 ／ 1920×1080（另可輸出 1:1 與 9:16 社群版） |
| 迴圈 | 非迴圈用途（片頭），末幀停在靜態標誌狀態 |

**Positive prompt**

```
A 6-second minimal brand sting on a deep navy graphite background (#101A2B), static camera, flat
motion-graphics language. A single hairline circle draws itself clockwise over two seconds, forming
a wafer outline; inside it, a faint orthogonal die grid fades up cell by cell in a soft radial
order. A thin spectral gradient highlight then sweeps once across the circle from left to right,
like light diffracting off a polished wafer, illuminating the grid only where it passes. The sweep
exits the frame and the circle settles into a calm static state with a single 1px teal-blue arc on
its upper right edge, leaving clear empty space beside it for a wordmark to be added later in
post-production. Pure flat 2D vector aesthetic, hairline strokes, no glow, no bloom, no 3D, no
depth of field, no text, no logo rendered by the model. Elegant, restrained, precise, 24fps.
```

**Negative prompt**

```
VNEG-BASE, plus: rendered wordmark, any letterforms, glowing edges, particle burst, shockwave,
lens flare sweep, 3d rotating disc, chrome material, metallic reflection, confetti, sparkles,
fast easing, bouncy overshoot, rainbow filling the whole circle
```

**模型注記**：Runway/Kling 以「空白深藍圖」為 first frame，`IMG-AI-01` 為 last frame，即可得到「畫出圓形」的過程；但此類精確幾何動畫**強烈建議以 SVG stroke-dasharray 動畫或 After Effects 製作**，AI 生成難以保證圓形不變形。真正的公司 logo（`logo.png`）一律以疊加圖層方式在後製加入，**不得交由模型生成**。

---

### OPT-VID-02（選用）— AI 頁背景循環（Ambient Loop）

| 項目 | 內容 |
|---|---|
| 建議檔名 | `assets/video/optional-ai-ambient-loop.mp4` |
| 長度 | 12 秒 |
| 比例／解析度 | 16:9 ／ 1920×1080（背景用途，可降至 1600×900 以縮小檔案） |
| 迴圈 | 必須完全無縫；末幀＝首幀 |
| 位元率 | ≤ 2 Mbps（背景影片必須極輕量，目標 ≤ 3 MB） |

**Positive prompt**

```
A 12-second seamless ambient background loop on a deep navy graphite field (#101A2B), static camera,
flat 2D motion-graphics language, extremely low visual energy so that overlaid typography stays
fully readable. A sparse field of hairline horizontal rules drifts upward at a nearly imperceptible
constant speed, unevenly spaced, most of them very low contrast grey. Three of the rules carry a
faint spectral gradient at low opacity. Occasionally two thin lines cross a small solid dot, and the
dot brightens softly to teal-blue (#5CC8E8) and fades again over about two seconds. Contrast stays
very low throughout, the centre of the frame remains the quietest area, and the final frame is
pixel-identical to the first so the clip loops invisibly. No glow, no bloom, no gradients filling
the background, no depth, no camera movement, no text, no numbers.
```

**Negative prompt**

```
VNEG-BASE, plus: high contrast movement, busy animation, particles swarming, matrix code rain,
data stream characters, flowing waves, gradient background wash, neon lines, glowing grid,
parallax starfield, pulsing brightness, anything that competes with foreground text
```

**模型注記**：以 Kling/Runway 首尾同圖模式生成後，仍須以剪輯軟體驗證 loop 接點；背景片一律搭配 `--dark-900` 半透明遮罩使用，確保文字對比 ≥ 4.5:1。同樣建議可用 CSS/SVG 動畫替代以節省頻寬。**此片不得在 `prefers-reduced-motion` 下播放。**

---

## 4. 涵蓋確認（Coverage Check）

| 資產 ID | 頁面 | 影片檔 | 海報檔 | 狀態 |
|---|---|---|---|---|
| `VID-HOME-01` | index.html | `assets/video/home-01.mp4` | `assets/img/home-01-poster.jpg` | 已涵蓋 |
| `VID-AI-01` | ai.html | `assets/video/ai-01.mp4` | `assets/img/ai-01-poster.jpg` | 已涵蓋 |
| `OPT-VID-01`（選用） | — | `assets/video/optional-brand-sting.mp4` | — | 選用，網站不引用 |
| `OPT-VID-02`（選用） | — | `assets/video/optional-ai-ambient-loop.mp4` | — | 選用，網站不引用 |

**站內 `VID-*` 資產合計 2 個，與 `docs/content-spec.md` §16 完全一致，無遺漏。**
兩張海報圖的完整提示詞另見 `docs/image-prompts.md`（「IMG-HOME-01（海報）」與「IMG-AI-01（海報）」）。
