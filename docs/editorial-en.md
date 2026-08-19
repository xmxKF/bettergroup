# editorial-en.md — English copy edit log (Phase 4)

Scope: `content/en/*.json`, all 16 files. Editorial pass only — meaning, facts, numbers,
brand names, architecture names and years unchanged; no key, list length or
language-invariant field touched. US spelling, sentence case in body copy, no exclamation
marks, headings kept to 6–8 words or fewer.

Terminology follows `docs/glossary-en.md`. Two conventions were standardised across the
language and are now recorded in the glossary (§0 and §11).

**Totals — 56 strings changed across 15 files.**

| File | Strings changed |
|---|---|
| `common.json` | 0 |
| `index.json` | 7 |
| `about.json` | 6 |
| `services.json` | 5 |
| `equipment.json` | 4 |
| `ai.json` | 8 |
| `contact.json` | 4 |
| `equipment-lithography.json` | 3 |
| `equipment-etch.json` | 3 |
| `equipment-cvd.json` | 3 |
| `equipment-bake.json` | 3 |
| `equipment-implant.json` | 3 |
| `equipment-cmp.json` | 2 |
| `equipment-cleaning.json` | 1 |
| `equipment-inspection.json` | 1 |
| `equipment-mask.json` | 3 |

---

## Cross-file standardisations

### 1. Meta title suffix → `| BETTER`
Twelve of fifteen pages already ended `| BETTER`; `about`, `services` and `contact` used
the full legal name, which also pushed those titles past the SERP truncation point.
`BETTER` is the defined short name for running text (glossary §1), so the short form wins.
The full legal name still appears in the footer and in `about.intro`.

### 2. `banner_label` → `<subject> photo`
The glossary already specifies this aria-label pattern (§11). Four pages used
`Photo of a/the <subject>` instead. Not visible text; screen-reader only.

### 3. Media `caption` trimmed to a label
`caption` renders inside the placeholder box (`media__ph > media__desc`), and 22 of them
were verbatim copies of the art-direction `alt` string — including the prompt tail
("cool tones", "symmetrical composition", "scientific photography style"). Every one is
now a short subject label; the full description stays in `alt`, so nothing is lost for
screen readers. These are noted per file below as "caption trimmed".

---

## `common.json` — no changes

Reviewed in full. Nav labels, CTA labels, form strings, footer column titles and the
trademark note are all glossary-defined verbatim and are width-measured; nothing to gain.

---

## `index.json` — 7

*Rationale: idiom repairs on three sentences that read as literal renderings, plus one card-text and one table-cell consistency fix.*

| Before | After |
|---|---|
| Full coverage from equipment to process, **and** from people to artificial intelligence. | Full coverage from equipment to process and from people to artificial intelligence. |
| **We help establish** process conditions, tune tools and convert to volume production **against your line targets**, shortening the transfer cycle. | **Against your line targets, we help set** process conditions, tune tools and convert to volume production, shortening the transfer cycle. |
| **Benchmarking** digital twin, physics-based simulation and generative lithography architectures **into** every process area. | Digital twin, physics-based simulation and generative lithography architectures, **benchmarked and deployed in** every process area. |
| Metrology, defect inspection and electrical test **equipment**. | Metrology, defect inspection and electrical test **tools**. |
| Procurement, acceptance, de-installation, packing, shipping, move-in, installation and tuning **are coordinated by one team**. | **One team coordinates** procurement, acceptance, de-installation, packing, shipping, move-in, installation and tuning. |
| Digital twin, physics-based simulation and defect models **are benchmarked in** to strengthen yield and tool utilization management. | **We benchmark and deploy** digital twin, physics-based simulation and defect models to strengthen yield and tool utilization management. |
| TSMC smart manufacturing: **time-series RNN FDC** + federated learning | TSMC smart manufacturing: **RNN time-series FDC** + federated learning |

Notes: "benchmarking X into Y" and "benchmarked in" are not English; both rewrites keep the
two separate ideas (對標 benchmark + 導入 deploy) that the source carries. The trailing
participle in the process-transfer card was attaching to the wrong clause, fixed by moving
the qualifier to the front, as in the master. The eighth process card was the only one of
nine that said "equipment" rather than "tools". The FDC model name now matches the wording
used in `ai.json` and on the etch / CMP / cleaning pages.

## `about.json` — 6

*Rationale: one over-translated hero lead, one stacked preposition, meta title, and three captions.*

| Before | After |
|---|---|
| `"About Us \| BETTER SCIENCE TECHNOLOGY GROUP"` | `"About \| BETTER"` |
| Serving advanced manufacturing across four **disciplines**: equipment, process, people and AI. | Serving advanced manufacturing along four **lines**: equipment, process, people and AI. |
| …deploy it in real use cases **in** every process area. | …deploy it in real use cases **across** every process area. |
| Hong Kong skyline and a modern commercial building facade**, cool tones with open space** | Hong Kong skyline and a modern commercial building facade *(caption trimmed)* |
| Wafer and data nodes joined by hairlines**, spectral gradient detail on deep blue** | Wafer and data nodes joined by hairlines *(caption trimmed)* |
| Top-down meeting room table: equipment specifications and a notebook**, cool tones, no faces** | Top-down meeting room table: equipment specifications and a notebook *(caption trimmed)* |

Note: "disciplines" overstated 主線 (main lines / tracks) and clashed with the site's own
"five core business lines"; "lines" restores both the sense and the internal echo.

## `services.json` — 5

*Rationale: one cross-reference sentence that read as an instruction chain, one punctuation collision, meta title, one caption.*

| Before | After |
|---|---|
| `"Services \| BETTER SCIENCE TECHNOLOGY GROUP"` | `"Services \| BETTER"` |
| **Depending on the process areas in your project, go to the** [nine process pages] **for the equipment scope.** | **For the equipment scope of the areas in your project, see the** [nine process pages]**.** |
| Move-in positioning, reinstallation, utility hook-up**, and functional and** process tuning. | Move-in positioning, reinstallation, utility hook-up**, then functional and** process tuning. |
| Engineer tuning at the tool with a handheld instrument**, cool tones** | Engineer tuning at the tool with a handheld instrument *(caption trimmed)* |

(The note rewrite is two strings: `note.before` and `note.after`.)

Note: the flow step was the only sentence on the site with an Oxford comma, and it landed
immediately before "and … and". Reordering to "then" removes both problems and matches the
sequential sense of the step.

## `equipment.json` — 4

*Rationale: one padded closing sentence, three captions.*

| Before | After |
|---|---|
| The nine areas feed one another, and variation in any one **of them** is amplified through the stack, so **a consistent equipment and data strategy is required**. | The nine areas feed one another, and variation in any one is amplified through the stack, so **equipment and data strategy has to be consistent**. |
| Perspective photo of a row of process tools in a cleanroom at the boundary of the yellow and white light bays, warm and cool contrast, symmetrical composition | Row of process tools at the boundary of the yellow and white light bays *(caption trimmed)* |
| Cyclic flow diagram of the nine process areas: thin-line icons arranged in a ring, with photomask as the starting point and inspection as the feedback loop | Cyclic flow diagram of the nine process areas, photomask through inspection *(caption trimmed)* |
| Top-down wafer close-up: the surface refracts a rainbow spectrum against a dark background, echoing the brand spectrum colors | Top-down wafer close-up: the surface refracts a rainbow spectrum *(caption trimmed)* |

## `ai.json` — 8

*Rationale: two leads with word repetition, four table-typography fixes, two captions.*

| Before | After |
|---|---|
| The architectures and quantitative **results** listed below **are third-party research results**, used as technical reference benchmarks and not measurements of our own. | The architectures and quantitative results listed below **come from third-party research**, used as technical reference benchmarks and not measurements of our own. |
| **All of the following are** third-party published research, used as deployment benchmarks. | **Everything below is** third-party published research, used as deployment benchmarks. |
| `die/wafer pass-fail, precision/recall` | `Die/wafer pass-fail, precision/recall` |
| `Patterns -20~25% (over 50% in some cases)` | `Patterns -20–25% (over 50% in some cases)` |
| `MAE<15×10⁻⁵V, 10–30× faster than NGSPICE` | `MAE < 15×10⁻⁵V, 10–30× faster than NGSPICE` |
| BETTER uses them as the benchmark for the work it deploys, **not as** measurements of our own. | BETTER uses them as the benchmark for the work it deploys, **not** measurements of our own. |
| Wafer overlaid with neural network nodes**, deep blue ground with fine spectral lines** | Wafer overlaid with neural network nodes **on deep blue** *(caption trimmed)* |
| AI deployment dashboard **style**: five stage cards with metric figures**, dark UI** | AI deployment dashboard: five stage cards with metric figures *(caption trimmed)* |

Notes: the AI framing is untouched — every architecture, model name, year and number in the
21-row benchmark table and the 9-row matrix is byte-identical, and both `note` strings still
attribute the results to third-party publication. The `die/wafer` cell was the only one in
its column that started lowercase. Ranges elsewhere in the same table use en dashes
(`28–3nm`, `5–12×`, `10–30×`), so `-20~25%` was brought into line. The closing `note` now
uses the same fixed phrase as the home page ("not measurements of our own", glossary §8).

## `contact.json` — 4

*Rationale: one wordy opener, one address sentence whose tail was lost in the commas, meta title, one caption.*

| Before | After |
|---|---|
| `"Contact \| BETTER SCIENCE TECHNOLOGY GROUP"` | `"Contact \| BETTER"` |
| **You do not have to use the form.** Write to us directly and one point of contact will reply. | **The form is optional.** Write to us directly and one point of contact will reply. |
| …Jordan, Kowloon, Hong Kong**, next to the Jordan business district.** | …Jordan, Kowloon, Hong Kong**. The office sits next to the Jordan business district.** |
| Meeting in a modern office**, cool tones, no identifiable faces** | Meeting in a modern office**, equipment specifications on the table** *(caption trimmed)* |

Note: the address contains six commas, so a seventh comma clause read as another address
component rather than as a remark about the location.

## Nine `equipment-<area>.json` — 19

*Rationale: aria-label pattern, caption trimming, one unclear pronoun. No `scope`, `services`, `fit`, `ai.text` or `metric` copy was altered — those strings are shared verbatim across the nine pages and are already glossary-fixed.*

**`banner_label` → `<subject> photo`**

| File | Before | After |
|---|---|---|
| `equipment-cmp.json` | Photo of a CMP tool | CMP tool photo |
| `equipment-cleaning.json` | Photo of the wafer cleaning area | Wafer cleaning bay photo |
| `equipment-inspection.json` | Photo of the wafer inspection area | Inspection bay photo |
| `equipment-mask.json` | Photo of a photomask | Photomask photo |

**Captions trimmed** (full description retained in `alt`)

| File | After |
|---|---|
| `equipment-lithography.json` | Lithography bay aisle: a row of exposure tools under yellow filtered lighting · Inside a coat and develop track: color bands on the photoresist film · Mask pattern overlaid with hotspot predictions and graph attention edges |
| `equipment-etch.json` | Etch tool exterior with plasma glow through the chamber viewport · Inside a plasma etch chamber: the wafer chuck under an even glow · Plasma simulation isosurfaces beside sensor time-series curves |
| `equipment-cvd.json` | Vertical furnace exterior, piping and heating zones clearly layered · Wafer boat loading into the furnace, wafers evenly spaced · Wafer thermal field contours and a thickness uniformity color map |
| `equipment-bake.json` | Hot plate and chill plate modules in a row, seen from above · Wafer on a hot plate, with surface heat shimmer · Wafer temperature contour heat map beside ramp-up and ramp-down curves |
| `equipment-implant.json` | Long beamline of an ion implanter, piping and magnet sections · Beamline and wafer end station with the ion beam path visualized · Simulated wafer dopant concentration profiles with uncertainty bands |
| `equipment-cmp.json` | CMP platen and polishing head in operation, slurry across a wet surface |
| `equipment-mask.json` | Reticle pod and quartz photomask under dark-field lighting |

**Other**

| File | Before | After |
|---|---|---|
| `equipment-mask.json` | Benchmark metric: 10–30× faster than NGSPICE (metric from **its** original domain) | Benchmark metric: 10–30× faster than NGSPICE (metric from **the** original domain) |

`its` had no antecedent in the sentence — the reader had to guess whether it referred to
MaxViT / U-Net or to NGSPICE. The caveat itself is kept: this figure comes from the IR-drop
domain, not from photomask writing.

---

## Deliberately not changed

- **`ai.pillars[2].title_lat`** — `LithoDreamer／ILT` in `ai.json` uses a full-width solidus
  while `index.json` uses `LithoDreamer / ILT`. `title_lat` is a language-invariant field;
  fixing it means changing `content/zh-hant/ai.json` too, which is out of scope for an
  English pass. Flagged for the master-copy owner.
- **`equipment-mask.json` `ai.entries[2]`** — carries `(ASP-DAC'26)` inside `arch` while
  `equipment-lithography.json` puts the same conference in the dedicated `year` field, which
  renders in `.card__year`. Moving it is a data change across four languages, not copy.
  Flagged.
- **`equipment.json` nine card texts** — "Procurement, sales and maintenance of X equipment"
  nine times is repetitive in English, but it mirrors the master exactly and each card is a
  fixed-height grid cell. Left as is.
- **Nav, CTA, button, hero-title-line and step-title strings** — all width-measured and all
  glossary-fixed. No edit would have shortened them without breaking the glossary.
- **`about.mission.entries[0].term`** — "easier to obtain, to run well and to keep running"
  is already three parallel infinitives and matches 被取得／被用好／被用久 exactly.

---

## Addendum (phase-4 acceptance)

| Item | Change |
|---|---|
| `services.json` `IMG-SVC-02` caption | "…sensor time-series curves**, dark UI**" → "…sensor time-series curves". The §3 caption rule was applied to English first; this was the one leftover, and the same rule has now been applied to zh-hant, zh-hans and ja so all four languages match. |
| `ai.json` `title_lat` | `LithoDreamer／ILT` → `LithoDreamer / ILT`. A language-invariant field cannot differ per language, and a fullwidth CJK solidus inside Latin text set in Inter reads badly; `index.json` already used the ASCII form. |
| `common.json` new `shell` object | `not_found` / `language_nav` / `gateway_note` / `back_to_gateway` — the gateway and 404 copy, previously hardcoded in the templates and therefore outside the four-language validation. |
