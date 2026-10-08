# SPEC — Sheet 3 "Approaches" (merged rustmapper survey + Scrapy Harbor), 1280×880

Replaces `approach_scrapy()` and `survey_rustmapper()` with one `approaches(t)`. Map-first: the chart fills the neat line; every panel is a cartouche on it. Day = CHART_LIGHT, night = CHART_DARK. Chart number (`stats.repos`, upright 13px Plex) outside the neat line at (1252,12) anchor=end and (28,874). Neat line: `frame()` rules at 14/19, broken (24px gaps) on the west edge at y 300–324 and 560–584. Vendor IBM Plex Mono Italic (OFL) as `"plex-italic"` for illustrative numerals.

## 1. Geography and what it means

West→east is the pipeline: rustmapper discovers, the channel is Scrapy's four stages, the anchorage is Delta Lake. One field (`make_field(1280, 880, seed=27, n=12, r=(50,130), a=(0.4,0.9), avoid=[(0,0,640,880)], extra=COAST)`), land level 1.5.

| Zone | Rect (x,y,w,h) | Meaning |
|---|---|---|
| W · Unsurveyed | 20,20,164,680 | Hatch `hatch_defs("hu", ink, 6, 45, .18)`; "UNSURVEYED" Plex 14px tracked +2, rotated −90°, centred (96, 420). No soundings. |
| Limit of survey | polyline x≈184, y 20→700, ±6px waver every 48px | Dotted 1.2px, dash "1.5 4". Label along it, rotated −90°: "LIMIT OF SURVEY 2026" 13px at (176, 560). |
| S · Survey ground | 200,110,400,576 | 4×4 blocks (100×144) lettered A–P row-major from NW; letter 13px upright Plex at block (x+6, y+15) with a 24px hairline under it; "A" has "· shards 0–15" after it once. 16 track lines, horizontal, y = 128 + i·36 (i = 0…15), x 210→590, 0.7px dash "1 5" opacity .55. Cross-lines (checks): vertical dash "1 5" at x = 300, 400, 500, opacity .35. Caption on line 1's east end: "16 lines ×32 = 512 workers" 13px upright. |
| C · Approach water | 600,20,460,680 | Channel, tints, shoal, wreck, inset. |
| L · Land | x ≥ ~1060 | COAST blobs: headland (1120,200,70,2.6), (1250,60,110,3), (1250,760,120,3), basin carve (1150,430,58,−1.8). Fill `t.land`, never hatched. |
| B · Bottom strip | 20,700,1240,160 | Title blocks and legend, §2–3. |

**Soundings.** Survey ground: 8 per line at x = 230 + j·50, 11px, italic (illustrative; depth = `int((1.5−field)·38)` clamped 4–60). Approach water: `soundings(field, (600,20,460,680), n=30, size=11)` italic, avoid channel (clearance 40), inset rect, legend. Four **upright** soundings are real and placed by hand: `512` at (578,668) end of line 16; `16` at (218,668) start of line 16; `256` at (640,80) (go_go_go worker pools, open water, no caption); `90` inside the inset at the basin mouth (test coverage). Depth deepens toward the anchorage: depth is trust.

**Channel** (centre line dash "2 6", 1px): waypoints W0 (612,640) → W1 (730,596) → W2 (850,548) → W3 (960,500) → W4 (1056,452) → ANCH (1140,436). Bearings per leg in 11px upright beside each leg midpoint (`course()` with `bearings=True`, no boat). Leading line: solid 0.9px from front mark (1176,423) seaward to W3, dashed beyond to W1; marks are two small triangles on land, rear at (1230,404); label "Health Ldg Lts 070° · Iso 2s" 13px upright at (1060,392) anchor=end. On the line = health check passing.

| Mark | Position | Shape / colour | Label (13px upright Plex) | Character |
|---|---|---|---|---|
| G"1" URLS | (662,594) | can, `t.ok` | G"1" URLS above-left | Fl G 4s, phase 0 |
| R"2" SCOUT | (799,596) | nun, `t.accent` | R"2" SCOUT below-right | Fl R 4s, phase 2s |
| G"3" ANALYZE | (896,500) | can | G"3" ANALYZE | Fl G 4s, phase 0 |
| R"4" SUMMARIZE | (1017,500) | nun | R"4" SUMMARIZE | Fl R 4s, phase 2s |
| Grafana Lt | (1092,212) headland | lighthouse (`lighthouse(beam=False)`) | "Grafana Lt" upright 14 + "Fl(3) 10s" 13 at (1104,236) | Fl(3) 10s |
| Breaker Lt | (1068,532) south point | sector light: 3px dot + sector arcs r=72, bearings 040°–100° from seaward | "Breaker Lt · Fl(2) R 6s · sector unlit" 13px at (1000,560) anchor=end | lit only when open |
| Health Ldg Lts | (1176,423) / (1230,404) | triangles | see above | Iso 2s |

`buoy()` gains `kind="nun"`: red trapezoid (base 10, top 6, height 11); cans stay flat. Region B: red nuns to starboard returning. Each lit mark gets a 3px light dot at its top and a halo circle r=9 (`t.ok`/`t.accent`, opacity 0) animated per §5.

**Breaker sector.** Red fill appears only in the legend. On the chart: two hairline radii and an arc, dash "1 3", no fill. The breaker is closed, so the sector is dark; no caption says so.

**Shoal.** "Rate Limit Shoal" (adaptive rate limits): extra blob (880,650,56,1.3) so the 5-contour closes; danger line = dotted ring on the 5-contour; name serif-italic 17px at (880,676). **Foul ground**: patch SW of the headland, polygon around (1040,262) r≈22, `hatch_defs("hf", ink, 4, −45, .3)`, "Foul" 13px upright. **Wreck**: "Wk" 13px upright at (716,418) with the S-4 wreck glyph (hull hairline with three verticals), danger ring r=16; name below in serif-italic 14px from `stats.wrecks[0]` = oldest unmerged, >1 yr stale branch in Scrapy's clone (B1 fetches it); fallback: oldest archived repo.

**Anchorage.** `anchor_glyph(1140,436, s=1.3)`, "Delta Lake" serif-italic 19px at (1140,470) anchor=middle, "Anchorage" 13px upright under it. Installations on the main chart are 6×6 structure squares (PostgreSQL (1182,398), Redis (1154,494), Prometheus mast (1140,252)), named only in the inset.

**Inset** (chart-within-chart): frame 656,118,288,196 (`cartouche`), plus a second frame at +6,+6 behind it (paper fill), and a hairline from its SE corner to the basin mouth (1068,430). Header "SCRAPY HARBOR · inset · ×3" 13px tracked. Contents at ×3 about the basin centre: basin outline and tint; anchorage at (800,222) with "Delta Lake" italic 17; quays and labels upright 13: "PostgreSQL · metrics" tank (two stacked rounded rects) at (872,164); "Redis · queues" twin tanks at (784,290); "Prometheus · scrapes" mast at (704,150) on the hill behind "Grafana Lt" (676,190, lighthouse s=0.7, flashing in sync with the main light); leading triangles at (902,210)/(934,198); Breaker Lt dot at (690,276) with unlit sector; sounding `90` upright at (730,236).

**Source diagram** at (36,36,112,72): mini-sheet outline with the survey ground split into three horizontal bands lettered A/B/C (boxed letters, to differ from block letters), each tinted `cool` at 30/20/10%; table right of it, 11px: "A sitemaps · B CT logs · C Common Crawl". Header "SOURCES" 13px. On the chart, three brace-ticks on the limit-of-survey line at y 128/320/512 carry the boxed letters: the seeds push the edge west.

## 2. Typography (all outlines via svgkit)

| Role | Font / size | Examples |
|---|---|---|
| Water place names | Instrument Serif Italic 17–19 | Delta Lake, Rate Limit Shoal, wreck name (14) |
| Land / structures | Instrument Serif Regular 14; Plex 13 upright | Grafana Lt, Scrapy Harbor (inset header is Plex) |
| Mark labels, notes, legend, bearings | IBM Plex Mono 13 upright, tracking +0.6 (notes), +1.8 (headers) | G"1" URLS, NOTES |
| Soundings texture | Plex 11 italic / Plex 11–13 upright for real values | 54 / 512 |
| Title-block titles | Instrument Serif 28, tracking −1 | rustmapper, Scrapy Harbor |
| Marginal pencil note | Instrument Serif Italic 14, `t.muted`, rotated −6° | §6 |

Two title blocks, `cartouche()`, bottom strip y 706–852 (146 tall). **rustmapper** at (36,706,330,146): title 28px at (52,738); line "Survey vessel · Rust · PyPI {version}" 13px at (52,758) (version from `stats.pypi.version`, upright because measured); "NOTES" 13px tracked at (52,782); numbered notes 13px, pitch 16, from y 800: `1 16 track lines × 32 = 512 workers` · `2 Blocks A–P: frontier in 16 shards` · `3 Write-ahead log: resumes at the last sounding` · `4 Redis, optional, for distributed runs`. **Scrapy Harbor** at (930,706,316,146): title at (946,738); line "Platform · Python · Docker · Kubernetes"; NOTES: `1 Marks numbered from seaward, Region B` · `2 Soundings reduced to raw layer (Delta Lake)` · `3 PostgreSQL metrics · Redis queues` · `4 Prometheus feeds Grafana Lt and the Ldg Lts` · `5 Tests cover 90%+ of the harbour`. No chips; links live in the README under each note number.

## 3. Legend panel

Cartouche at (382,706,532,146), header "SYMBOLS USED ON THIS CHART AND ON CHART {n}" 13px tracked at (396,726). Two columns (x 396 and 660), symbol cell 32px wide, text 13px upright at cell +40, row pitch 14.5 from y 744, 8 rows:

| Col 1 | Col 2 |
|---|---|
| green can — `G can · port hand returning` | dashed line — `Survey track · one line ×32 workers` |
| red nun — `R nun · starboard hand` | boxed/unboxed `A` — `Block letter · one frontier shard` |
| light dot + "Fl(3) 10s" — `Light · flashes its character` | crosshair — `Waypoint · pipeline stage` |
| red-filled arc — `Red sector · breaker open` | `070°` — `Bearing · true, from seaward` |
| dotted ring — `Danger line · submerged shoal` | `54` upright — `Upright figure · measured` |
| cool swatch (2 tones) — `Shallow water · ≤5 and ≤10` | *54* italic — `Italic figure · illustrative` |
| `Wk` glyph — `Wreck · abandoned branch` | hatch swatch — `Hatch · unsurveyed or foul` |
| anchor — `Anchorage · raw storage` | two triangles + line — `Leading line · health check` |

Each symbol is the same `<use>`/primitive as on the chart; test by diffing symbol ids.

## 4. Water, hazards, day and night

Contour levels 0.5…1.5 step 0.1 (11), index every 5. Tints: polygon between coast (1.5) and the 1.3 contour filled `t.cool` at .14; between 1.3 and 1.1 at .07 (fill closed contours, mask land). Danger lines on every closed 1.3 contour not touching land. Foul: hatch "hf" over the patch, no tint. Unsurveyed: hatch "hu", no contours or soundings, neat line broken.

Night (CHART_DARK): ink → `t.ink2` for contours at 0.6× opacity; soundings `t.ink2` .55; land `#172740` without stroke; tints .20/.10; hatch .12. Lights brightest: halo `feGaussianBlur stdDeviation=3` on the light dots (filter id "glow"), halo radius 12, Grafana Lt gets a 220px, 10°-wide ruled sector pair at .08 (ruled, not a wedge) toward the channel. Day: no halos, no glow, structures full ink.

## 5. Motion (SMIL only, inside `<img>`)

Easings: `settle` 0.16 0.84 0.44 1 · `draw` 0.4 0 0.2 1 · `sea` 0.37 0 0.63 1. Scale: 150/400/650/1600/2600 ms; loops 10/24/48/96 s.

**Survey (one-shot, 24 s).** Lines 1–8 (blocks A–H) are already sounded at t=0; their contours show through `clipPath` y 110–398. Vessel (`boat(s=0.8)`) starts at (590,416), east end of line 9. Legs `leg9…leg16`, each `animateMotion` 2.6 s `settle`, `fill="freeze"`, along the line alternating E→W, W→E; `begin="leg{n-1}.end+0.4s"`; turns are 400 ms `animateTransform` rotate ±180°, `sea`. Lead-line drop: a 1px vertical 14px long under the hull, `animate y2` 0→14 over 300 ms `draw` at `begin="legN.begin+{(j+0.5)/8·2.6}s"`, 8 per leg; sounding `sNN` (opacity 0→1, 250 ms `settle`, 3px rise) at `begin="dropNN.end"`. **WAL tape** at (52,834) inside the rustmapper block: 56 cells 8×6 in two rows, cell k `<set opacity to=1 begin="sNN.begin" fill=freeze>`; the 64 cells for lines 1–8 are drawn lit. Caption "write-ahead log · one cell per sounding" 11px. **Contours** of the south half (clip y 398–686) `pathLength=1` dash trace 1.6 s `draw` at `begin="leg16.end+0.6s"`, stagger 90 ms by level, then tints fade 650 ms; all `fill="freeze"`. The vessel freezes at (590,668) beside `512`.

**Lights (loop).** Grafana Lt and inset twin: opacity `calcMode=discrete` values `1;0;1;0;1;0` keyTimes `0;.03;.1;.13;.2;.23` dur 10 s. Buoys Fl 4s: values `1;0` keyTimes `0;.1` dur 4 s, reds `begin="2s"` so the fairway alternates. Ldg Lts Iso 2s: values `1;0` keyTimes `0;.5` dur 2 s. All begin at 0 s; every dur divides 24 s, so this is one phase-locked loop.

**Packet boat (loop, 48 s).** `boat(s=0.55)` on `smooth_path` W0→ANCH: `animateMotion` dur 48 s `keyPoints="0;1;1;1" keyTimes="0;.5;.83;1"` `calcMode=spline` keySplines `settle;0 0 1 1;0 0 1 1`, rotate auto; opacity values `0;1;1;0;0;0` keyTimes `0;.008;.83;.838;.99;1`: 400 ms fade-in at W0, 24 s run, 16 s hold at anchor, 400 ms fade, reappears.

Loops remaining: lights and packet boat (2 of the page's 3). The survey vessel does not bob; it is finished.

## 6. Second-look layers (uncaptioned)

1. Pencil note at (690,452), serif-italic 14, rotated −6°, `t.muted`: "sitemap.xml wrong about itself again — see Notice 3", its tail touching the wreck ring.
2. The wreck's italic name is a real dead branch (`stats.wrecks[0]`), year beneath it in 11px.
3. Upright soundings `512`, `16`, `256`, `90` among italic ones; the legend explains why without naming them.
4. The Breaker Lt sector is drawn unlit; the legend shows it red. Connecting them tells you the breaker is closed.
5. Health Ldg Lts bearing 070° re-appears in the README's Notices as the heading number for health checks.

## 7. Still-frame rule

t=0: full geography, tints, land, inset, legend, title blocks; north-half soundings and contours; all 16 tracks and letters; vessel on line 9; every light in its lit phase; packet boat half faded-in at W0; 64 WAL cells lit. t=∞: all that plus south-half soundings and contours, vessel frozen beside `512`, tape full, lights flashing, packet boat somewhere on its 48 s cycle (the 16% it is absent, marks, vessel and lights still hold the water). Filmstrip at 0/6/12/18/23.9 s and 0/12/24/36/47.5 s: every frame a finished sheet.

## 8. Alt text

"Approaches to Scrapy Harbor. West of the limit of survey the water is unsurveyed; rustmapper runs sixteen parallel track lines, each worth thirty-two workers, and the soundings fill in behind the vessel. A buoyed channel, marks numbered from seaward, leads past Grafana Light into the Delta Lake anchorage. Inset: the harbour works. Upright figures are measured; italic ones are not." (63 words)

## Summary
- One 1280×880 map-first sheet: unsurveyed west, rustmapper's 16-line survey ground with lettered shard blocks, buoyed Region B channel into Scrapy Harbor, inset basin.
- Every number is italic unless measured (512, 16, 256, 90, PyPI version, chart number); the legend defines the convention and all 16 symbols used on the page.
- Chart grammar is exact: can/nun, Fl G 4s / Fl R 4s / Fl(3) 10s / Iso 2s, sector light unlit = breaker closed, leading line = health check, danger lines, tints, foul hatch.
- Motion: 24 s one-shot survey with lead-line drops, soundings and WAL cells per sounding, contours freezing; two loops remain (lights, 48 s packet boat); every frame composed.
- Two cartouche title blocks with numbered mono notes replace chips; three-plus second-look layers tie the wreck, pencil note and bearings to the Notices.
