# SPEC — Hero sheet, "Chart No. N" (overture)

Canvas **1280 × 740**. Neat line inset M=18 (outer rule) / 24 (inner rule); drawable water = (24, 24, 1232, 692). Fonts: Instrument Serif (`serif`, `serif-italic`), IBM Plex Mono (`plex`) plus **vendor IBM Plex Mono Italic as `plex-italic`** (OFL). Themes: `CHART_LIGHT` / `CHART_DARK` unchanged except where §6 says. All numbers below are 1280-space px; the phone edition (§9) scales from the same code via a `scale` parameter on `hero()`.

Data inputs (all from `assets/stats.json`): `repos[]` (name, commits, first, last, authors), `hours[24]`, `weeks[52]` (weekly contributions; absent until the workflow runs), `followers`, `repo_count` (fallback `len(repos)`), `pypi.version` (fallback "0.1.3"), `pypi.released` (optional). **N = repo_count.** `SHELVED = {3d-swift-widget, 2d-swift-widgets, MLX_convertion, Course_crusader}` is a constant in `build_assets.py`.

## 1. Layout

| Element | Position | Spec |
|---|---|---|
| Name | x 64, baseline 222 | "Ben Russell", `serif` 176, tracking −3, `ink`. No eyebrow above it. |
| Thesis | x 72, baseline 300 | "I survey a web that is wrong about itself." `serif-italic` 40, tracking −0.2, `ink2`. |
| name_box (calm zone) | (40, 40, 800, 280) | no blob centres, no soundings; halo ellipse (440,190, rx 460, ry 170). |
| Cartouche | (48, 486, 592, 224) | double rule as today; `paper` fill .94. Left column x 70–470, right column x 488–616. |
| Compass | centre (1000, 168), r 80 | §4. Exclusion box (906, 70, 190, 240). |
| Unsurveyed band | x 1150 → sheet edge | §3. Exclusion for all features. |
| Chart No. outside neat line | top-right: "N" right-aligned at (1262, 14), `plex` 13; bottom-left: "CHART NO. N · SHEET 1" at (24, 735), `plex` 13 | muted; the only text outside the neat line. |

**Cartouche contents** (mono lines are `plex` 13, tracking 1.2, caps, `muted` unless noted):

| Baseline y | Left column (x 70) |
|---|---|
| 516 | BENJAMIN S. RUSSELL — `plex` 13, tracking 1.8, `ink` |
| 546 | *Full-stack developer · mostly crawlers, lately in Rust* — `serif-italic` 22, `ink2` |
| 560 | rule x 70–616, 0.6px, ink .6 |
| 584 | CHART NO. {N}  ·  EDITION {pypi.version}{" · " + released[:7] if present} |
| 604 | SOUNDINGS IN COMMITS  ·  DATUM: MAIN |
| 624 | IALA REGION B  ·  CORRECTED THROUGH NOTICE 5 |
| 644 | scale labels *0*, *20k*, *40k URLS* in `plex-italic` 13 (illustrative → italic), at x 70 / 170 / 270 |
| 652–657 | scale bar 200 × 5, alternating fills every 50px |
| 678 | SCALE OF DISCOVERED URLS  ·  NOT FOR NAVIGATION (the one occurrence on the page) |

Right column: **source diagram** inset at (488, 578) 120 × 68 (a miniature of the sheet, 1px `ink` rule): area **A** (x 0–84, full height) tint `cool` .14 = sitemaps, full coverage; area **B** (x 84–120) hatch 45° spacing 3 = CT logs, partial; area **C** strip (y 50–68, x 0–84) dotted fill = Common Crawl, lead line only. Letters A/B/C `plex` 13 at the area centres. Key below, `plex` 13 muted: y 664 "A  SITEMAPS", 682 "B  CT LOGS", 700 "C  COMMON CRAWL". The same three letters recur on the chart itself in `plex` 13 at .5 opacity: A at (430, 392), B at (1134, 96), C at (820, 702).

## 2. The archipelago

**Radius.** `r = 3.2 · sqrt(commits)`, clamped to [6, 90]. Area is therefore ∝ commits. Today: game_engine 77, Scrapy 58, Data_science_dev 55, BenjaminSRussell 42, Rust-sitemap 36, FashionDB 26, Data-visualizer 23, … cozy-game 8.5. A change of one commit count in stats.json changes a blob radius and therefore the contours (Standard 2).

**Kind** (first rule that matches): `wreck` if name ∈ SHELVED → `harbour` if name == "Scrapy" → `islet` if r < 16 → `island` if `last` is > 90 days before `updated` (dormant: surfaced, finished) → else `shoal` (active: still being sounded). Scrapy is the stated exception to "active = shoal": the harbour is the platform you return to, drawn as land with an anchorage.

**Field.** Keep `make_field`; feed one blob per non-wreck feature: `(x, y, 0.9·r, amp)` with amp 2.3 (island, islet, harbour) or 1.3 (shoal: crosses the 0.8 and 1.1 levels, never LAND). Scrapy adds two negative blobs (790, 540, 16, −1.5) and (810, 520, 16, −1.5) that carve a basin opening NE; assert `field(760,575) > LAND` and `field(790,540) < 0.8`. Random filler blobs: n = 6, amplitude ≤ 0.7, so nothing anonymous reaches a tint level. Multiply `Field.value` by an edge falloff (smoothstep to 0 over the 24 px inside the drawable rect and over x 1080→1150) so every tint contour closes; the build asserts all 0.8 and 1.1 polygons are closed. LAND = 1.5; levels 0.5…1.4 step 0.1, index every 5.

**Tint bands** (both editions): fill the closed 0.8 polygons with band A, the closed 1.1 polygons with band B on top, then land. Day: A = `cool` #2E6FB0 at .10, B at .18, land `#E6DCC6`. Night: A = `cool` #7CB8FF at .07, B at .13, land `#172740` with a 0.8px `ink` .5 coastline. **Danger line**: each shoal's 0.8 polygon re-stroked with `stroke-dasharray="0 4.5" stroke-linecap="round"` 1.4px `ink` .8. Hatch appears nowhere on features.

**Placement.** Named six (by commits, today) take slots keyed by name, else by rank:

| Repo | Chart name | Kind | Centre |
|---|---|---|---|
| Scrapy | Scrapy Harbor (upright) | harbour | (760, 560) |
| Rust-sitemap | *Rustmapper Shoal* | shoal | (1040, 470) |
| game_engine | Game Engine I. (upright) | island | (870, 360) |
| Data_science_dev | *Data Science Bank* | shoal | (990, 610) |
| BenjaminSRussell | *Profile Shoal* | shoal + △ station glyph at centre | (330, 405) |
| FashionDB | *FashionDB Bank* | shoal | (640, 420) |

Rank slots 1–6 in that order for an unmapped repo; name = repo name (underscores → spaces) + " Shoal" / " I.". Names: islands upright `serif` 15, shoals `serif-italic` 15, `ink` .9, centred, +4 below centre. Remaining features sort by r descending and go through a greedy Halton-sequence search (seed 2709) accepting the first point that is inside the drawable rect minus exclusions (name_box, cartouche + 16, compass box, band x ≥ 1150) by ≥ r+28, ≥ `ri + rj + 44` from every placed feature, ≥ r+30 from the course polyline, and, for islets, biased to x > 600. go_go_go is force-placed at (930, 490) because the course sights it. Wrecks: fixed (1100, 300), (905, 470), (1110, 660), (676, 668): dotted danger circle r 11, a 14px hull line with a 6px mast stub, label `Wk 'YY` (year of last commit) `plex-italic` 13 to the right.

**Course** (seaward → harbour; the direction of returning). Waypoints: WP1 (1140, 300) on the unsurveyed boundary · WP2 (1100, 410) off Rustmapper Shoal (discovery) · WP3 (975, 525) off go_go_go islet and Data Science Bank (crawl) · WP4 (812, 508) harbour entrance (crawl platform) · WP5 (776, 556) anchorage ⚓ "Delta Lake" (storage), anchor glyph + `plex` 13 upright label. Dashed 2 6 as today; waypoints as today; bearings per leg in `plex` 13 (not 9.5), 12px off the leg on the side away from the nearest feature. Game Engine I., Profile Shoal and FashionDB Bank are sighted, not visited (a game engine and a database are not on a crawl's track).

## 3. Soundings

Size **11px**, `plex`, `ink` .75; spacing 40. Three classes:

1. **Feature soundings, upright** — each non-wreck repo's `commits`, placed 8px outside its danger line / coastline at the one of 12 compass angles with the most clearance (21 today: 585, 331, 295, 169, 126, 67 …). Wrecks carry theirs inside the circle label.
2. **Open-water soundings** — n = 34. If `weeks` exists: the most recent 34 weekly totals, upright, laid out along the course from seaward (oldest) to harbour (newest); 0 is drawn as 0. Otherwise the current field-depth algorithm, in **`plex-italic`** (illustrative by convention, no caption).
3. **Heights above datum, underlined** (the drying-height convention: these stand above the data, they are not commit counts): **512** 10px NE of Rustmapper Shoal, **256** beside go_go_go, **{followers}** (46) beside Profile Shoal. Underline 0.8px, 1px below the baseline. Repo count is the chart number; 0.1.3 is the edition.

**Unsurveyed margin.** Spacing grows `40 + 60·clamp((x−900)/250)`; opacity falls .75 → .40 over x 1000→1150; none at x ≥ 1150. Contours in x 1080–1150 are drawn through a second clipPath with `stroke-dasharray="3 3"` (approximate contours). Band x 1150→1280, y 150→580: hatch pattern (spacing 6, 45°, `ink` .28) that **runs to the sheet edge**, no neat line, no minute bars in that span (border function takes `gap=(150, 580)` for the right side); above and below the gap the band stops at the inner rule. "UNSURVEYED" `plex` 13, tracking 3, rotated −90°, centred (1206, 365); "LIMIT OF SURVEY 2026" `plex` 13 rotated −90° at (1160, 365) just inside the boundary.

## 4. Compass rose

Centre (1000, 168). **Outer true ring** r 80: 1px circle; ticks every 10° (6px) and 30° (11px, 1px stroke); numerals every 30° except 000 in `plex` 13 at r 94 (030 … 330), "N" `plex` 13 at 000; no E/S/W, no star, no rhumb lines. A 10px accent arrowhead at 000 on the ring is the rose's only colour. **Inner ring** r 58 (0.6px circle): the 24-hour commit clock — 24 bars radiating inward, width 2.6, length `4 + 26·hours[h]/max(hours)`, `ink` .7, hour 0 at the top before rotation, then the whole group rotated by `−15°·argmax(hours)` so the busiest hour (21 today) sits at north. "21h" `plex` 13 inside the ring under north. Below the rose, centred x 1000: y 286 "VAR 21h00 (2026)", y 304 "ANNUAL CHANGE SEE COLOPHON", both `plex` 13 muted. (Colophon resolves it: he works at night, and the rose points at the only fixed thing on the chart, the accent.)

## 5. Lateral marks (IALA Region B)

At the harbour entrance only; none at the seaward end (the sea has no marks). Course heading at WP4 is ~276°, so returning starboard is north. **R "2"** red nun (cone, `accent`) at (812, 484), light `Fl R 4s`; **G "1"** green can (flat-topped rect, `ok`) at (812, 532), light `Fl G 4s`, offset 2 s so they alternate. Labels `plex` 13: `R "2" Fl R 4s` above the nun, `G "1" Fl G 4s` below the can. Light = 3px dot atop the body; flash = opacity `0;1;1;0;0` keyTimes `0;.02;.1;.14;1` dur 4 s, the two marks `begin="sail.begin"` and `begin="sail.begin+2s"`. Swap `buoy()` kinds: `nun` is the cone, `can` the rect.

## 6. Night edition beyond palette

Contour opacity .42 → .30; soundings .75 → .55; graticule .10 → .06; feature names `ink2`; tint per §2; buoy bodies .65. Lights become the brightest objects: each gets a halo `<circle r="14">` filled `accent`/`ok` with `filter: feGaussianBlur stdDeviation 4`, animated with the same flash values, peak opacity .95; the anchorage symbol gets a faint fixed halo (.25). The name stays full `ink`; the rose's accent arrow gets a 2px halo. Day: no halos, light dots flash at .9, structures (buoy shapes, coastlines) carry the sheet.

## 7. Second-look layers (none captioned)

1. Pencil note in `serif-italic` 16, `muted`, rotated −7°: "sitemap.xml lies again — see Notice 3" at (990, 402) with a 30px leader to Rustmapper's danger line.
2. Pencil note rotated +5°: "raw layer first — Notice 2" at (690, 646), leader to the Delta Lake anchor.
3. Underlined heights 512 / 256 / 46 among the soundings (§3).
4. "VAR 21h00 (2026) · ANNUAL CHANGE SEE COLOPHON", resolved only in the README colophon.
5. Profile Shoal carries the △ station glyph: the sheet marks where it was surveyed from.
6. Open-water soundings are the last 34 weeks in course order; the one nearest the anchor is this week's.
7. A, B, C on the chart match the source-diagram areas; the wrecks' `'YY` years.

## 8. Motion (05 P1 + P7; easings settle `0.16 0.84 0.44 1`, draw `0.4 0 0.2 1`, sea `0.37 0 0.63 1`)

t=0 frame is a finished blank form: paper, neat line + minute bars, graticule, band hatch, cartouche rules, compass rings, "N". Then, all `fill="freeze"`:

| t (s) | Element | Animation |
|---|---|---|
| 0.2 + 0.12·i | contour level i (deep first) | `pathLength="1"` dashoffset 1→0, dur 1.6, draw |
| 1.0 / 1.3 | tint A / tint B | opacity 0→target, dur 1.0, settle |
| 1.6 | land fills, danger lines, wrecks, anchorage | opacity dur 0.65 settle |
| 1.4 + 0.04·k | sounding k (sorted by projection onto the course, seaward first; off-course ones by x desc) | opacity 0→1 + translate 0,3→0,0, dur 0.25, settle |
| 2.0 | compass inner ring | rotate `rot+12 → rot−4 → rot`, keyTimes 0;.45;1, dur 1.6, sea |
| 2.2 + 0.1·rank | feature names | opacity dur 0.4 settle |
| 2.6 / 2.85 | "Ben" / "Russell" | `calcMode="discrete"` opacity 0→1 per word (two clip groups), 1 step each |
| 3.1 | thesis line | opacity + 4px rise, dur 0.4 settle |
| 3.3 | cartouche rules + inset | `pathLength="1"` draw, dur 0.65 |
| 3.6 | cartouche text, bearings, light labels | opacity dur 0.4 settle |
| 4.0 | boat (`id="sail"`) | begins |

Boat: `<animateMotion id="sail" dur="96s" repeatCount="indefinite" rotate="auto" path="{smooth_path(WP1..WP5)}" keyPoints="0;1;1;0;0" keyTimes="0;0.44;0.5;0.94;1" calcMode="spline" keySplines="0.37 0 0.63 1;0 0 1 1;0.37 0 0.63 1;0 0 1 1" begin="4s"/>` — sails in 42.2 s, holds at anchor 5.8 s, sails out, holds at sea. Tack and righting on the return leg: `<set attributeName="transform" to="scale(1,-1)" begin="sail.begin+45.1s; sail.repeatEvent+45.1s" dur="48s"/>` on the hull group (mirrors across the tangent so the glyph is upright with the sail on the other side). Heel: `animateTransform rotate −3;3;−3` dur 4 s, sea, inside the boat group. Lights per §5. **Indefinite loops after the opening: 2** (boat with its children; the lateral-light pair). Compass does not loop. Reduced-motion edition = end state with all `<animate>` removed.

## 9. Phone edition (720 × 560, `media="(max-width: 600px)"`, two more `<source>`s)

Culled: graticule; open-water soundings to 14 nearest the course; names to the four largest; compass to r 52 with 30° ticks and N + 090/180/270 only; source-diagram inset and key, line 624 and the bottom-left outside number; one pencil note (Notice 3); band width 64. Grows: name 132, thesis 28 (two lines if width > 600), cartouche mono 15, soundings 13, bearings/light labels 15, boat scale 1.15, buoys ×1.3. Same timeline; sounding stagger 60 ms.

## 10. Alt text (built from stats, ≤60 words)

"Chart No. 21, the open web. Ben Russell: I survey a web that is wrong about itself. Twenty-one repositories as shoals and islets, area by commits; a course from the unsurveyed margin past Rustmapper Shoal into Scrapy Harbor; a compass whose inner ring is the 24-hour commit clock. Soundings in commits, datum main. Not for navigation."

**Build checks.** grep SVG for ILLUSTRATIVE|PENDING|SEEDED → 0; semantic text ≥ 13px (soundings 11 only); all tint polygons closed; bounds clean except the band's deliberate bleed; < 300 KB; filmstrip at 0/25/50/75/99 % of 96 s shows a finished sheet.

## Summary

1. 1280×740 sheet; name 176 / thesis 40 italic / cartouche with chart no., edition, datum, Notice 5, source diagram, scale bar; chart number repeated outside the neat line.
2. Archipelago from stats.json: r = 3.2√commits, kind by shelved/harbour/size/dormancy, shoals as tinted water inside dotted danger lines, two tint bands, course seaward → Rustmapper → go_go_go → Scrapy Harbor anchorage with Region B marks at the harbour only.
3. Soundings 11px: repo counts upright, last 34 weeks upright in course order (italic fallback), underlined 512/256/46; right margin thins into a hatched UNSURVEYED band that breaks the neat line.
4. Two-ring rose with the 24-hour commit clock rotated to the busiest hour, VAR note resolved in the colophon; night edition dims ink and makes the lights the brightest things.
5. One-shot 4 s opening (contours by depth → tints → soundings → name → cartouche), then only the 96 s out-and-back boat and the 4 s light pair loop; phone edition at 720 culls texture and grows type.
