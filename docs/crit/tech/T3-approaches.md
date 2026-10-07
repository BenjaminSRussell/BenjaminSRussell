# T3 — Approaches sheet (Sheet 3, the climax room)

Base: spec-approaches.md, amended where the verified facts or the panel require. `approaches(t, ed)` replaces `approach_scrapy()` and `survey_rustmapper()`. Canvas **1280 × 960** (amends E1's 880: the full legend needs a 224px strip; 27 wants the climax tall).

## 1. Decisions

1. **Orientation agrees with the hero: harbour west, survey ground and unsurveyed water east, channel runs ~290° into the anchorage.** Per 26 and 16/27 (one harbour mouth; the survey edge on the right on every sheet). The pipeline reads right-to-left, the direction of returning and of mark numbering; T8 rewrites "read left to right" as "read from seaward".
2. **rustmapper → Scrapy is a proposed channel**: pecked centre line from the survey ground to the first lit mark, two hollow unlit marks, legend row "Proposed channel · unlit". Per 20 (zero references in the Scrapy repo). URLS → SCOUT → ANALYZE → SUMMARIZE is Scrapy's real stage order and stays lit.
3. **Survey geometry is the real frontier**: one track line per shard (`log.json.shards`, cores of the machine that ran the logged session, T9); check lines = dedup; permits 256–1024 in the notes. "16 × 32 = 512" is deleted; **no upright 512, 16, 256 or 90 on this sheet.** Per 19, 20.
4. **The breaker is a port traffic signal in the harbour inset, beside the stores it wraps.** Legend shows its three states as proceed / stop / one at a time; no sector light anywhere. Per 21 (an unlit charted light is a defect), 26, 20 (breakers wrap http/delta/redis, not hosts). 25's red-sector line goes with the mapping.
5. **Light characters are derived or absent.** Grafana Lt = `Fl {scrape_interval}s` from the Scrapy repo's `monitoring/prometheus.yml` (T7), else drawn fixed. Ldg Lts fixed unless T7 supplies a readiness-probe period. Horn beside Grafana Lt = Alertmanager. Per 21. Buoy characters (Fl G 4s / Fl R 4s) are the chart's own buoyage and claim nothing about code.
6. **Anchorage = three real Delta tables as basins** (`stage1_discovery`, `stage2_page_analysis`, `stage4_summaries`), soundings = row counts, upright only when `stats.scrapy.run` exists. Per 20. Sheet unit **SOUNDINGS IN URLS · THOUSANDS**, declared once outside the neat line (13, 34); depth is a count, so the raw basin is deepest and "depth is trust" is dropped.
7. **Source diagram becomes a Zones-of-Confidence panel**, with `Rep` / `ED` / `SD` doubt marks in zones A / B / C on the chart. Per 22, 26. 25's "A: as declared by the site. B, C: as found." sits under it.
8. **robots.txt is a T-dashed restricted area the track lines stop at**, no invented path inside it. Per 22.
9. **Honesty per figure**: upright measured, italic illustrative, defined in the legend with ED/Rep/SD. Water names italic, land and structures upright (07, 13).
10. **Finished work at t = 0 plus one delayed, short, discrete one-shot** (the vessel plots the last track line as eight fixes from 24 s); lights discrete opacity; packet boat eight fixes per 96 s by `animateTransform` values. No `animateMotion`, geometry attributes or filters. Per 12.
11. **Phone edition 720 × 1240: the geography rotated 90° anticlockwise** so the channel runs down the screen, re-lettered through a point mapper; fallback two stacked halves. Per 10.
12. **One label per object (27)**: blocks carry drawable facts, bullets carry purpose, alt text opens with a tombstone.
13. **Subtraction (33)**: foul ground, second pencil note, WAL dedup cells, speed-limit mark and governor gauge go; "Rate Limit Shoal" becomes *429 Shoal* (22).

## 2. Geography (1280-space integers; neat-line rules at 14/19)

| Zone | Rect / position | Content |
|---|---|---|
| Land | x ≤ 220; headlands (160,200,70,2.6), (30,60,110,3), (30,760,120,3); basin carve (150,440,36,−1.8) | `t.land`, never hatched. "SCRAPY HARBOR" upright serif 28 at (60,300), the one display name on the chart. |
| Anchorage | (150,440) | `anchorage()` s 1.3; "Delta Lake" serif-italic 19 at (150,478). Basins drawn only in the inset. |
| Proposed channel | pecked 1px "4 4" from (684,616) to W0 | Two hollow outline marks ±18px off the line; no light, no number. |
| Channel | W0 (560,600) → W1 (470,560) → W2 (390,528) → W3 (320,500) → W4 (236,462) → ANCH (150,440); dash "2 6" | Bearings per leg 13 upright from `course(bearings=True)`; waypoints ⊙. |
| Survey ground | 680,120,400,570 | n = `log.shards` horizontal track lines, y = 120 + (i+1)·570/(n+1), x 690→1070, 0.7px dash "1 5" .55; check lines vertical at x 790/890/990, .35. Caption at line 1's east end: "one shard per core · {n} here" (n italic unless `log.measured`). |
| Restricted area | polygon (900,300)–(1060,300)–(1060,420)–(900,420) | T-dashed boundary, teeth inward; "robots.txt · Disallow" 13 upright; track lines stop 6px short. |
| Zone letters | boxed A/B/C 13 at (1086, 215/405/595) on the limit line | ZOC bands |
| Doubt marks | `Rep` dotted ring r 7 at (760,210); `ED` islet r 4 at (980,480); `SD` beside the sounding at (840,640) | 13 upright, pinned 8px right of the mark (33). |
| Limit of survey | polyline x ≈ 1096, y 20→700, ±6 waver per 48px, dash "1.5 4" | "LIMIT OF SURVEY 2026" 13 rotated −90° at (1104,560). |
| Unsurveyed | 1100,20,160,680 | `hatch_defs("hu", ink, 6, 45, .18)`; "UNSURVEYED" 14 tracked +2 rotated −90° at (1180,420); east neat line broken 24px at y 300–324 and 560–584, hatch runs to the sheet edge there. |
| ZOC panel | cartouche 680,26,400,86 | §3 |
| Inset | cartouche 316,112,300,210 + paper shadow +6,+6; hairline from (316,322) to the basin mouth (232,452) | §2b |
| Bottom strip | 20,700,1240,240 | rustmapper block (36,706,336,224) · legend (388,706,504,224) · Scrapy Harbor block (908,706,336,224) |
| Outside the neat line | "N" 13 at (1262,14) end; "CHART NO. N · SHEET 3 · APPROACHES TO SCRAPY HARBOR" 13 at (24,955); "SOUNDINGS IN URLS · THOUSANDS" 13 in `t.accent` centred at (640,12) | Series lock-up in the same position on every sheet (28). |

**Marks** (Region B, returning heading ~290°, so starboard = north), placed by `lateral_offset(leg, s, side, 24)`:

| Mark | ≈ Position | Shape | Label 13 upright | Character |
|---|---|---|---|---|
| G"1" URLS | (518,604) S of W0–W1 | can `t.ok` | G"1" URLS | Fl G 4s, begin 0 |
| R"2" SCOUT | (430,520) N of W1–W2 | nun `t.accent` | R"2" SCOUT | Fl R 4s, begin 2s |
| G"3" ANALYZE | (356,540) S of W2–W3 | can | G"3" ANALYZE | Fl G 4s, begin 0 |
| R"4" SUMMARIZE | (280,456) N of W3–W4 | nun | R"4" SUMMARIZE | Fl R 4s, begin 2s |
| Grafana Lt | headland (160,200) | star r 4 + 45° flare (26, 31); tower only in the inset | "Grafana Lt · Fl {s}s" 14/13 at (178,196); "Horn" 13 beneath | Fl {scrape_interval}s, else fixed |
| Health Ldg Lts | front (100,434), rear (60,428) on land; line solid to W3, pecked to W1 | two triangles | "Health Ldg Lts {brg}°" 13 at (250,414) | F |
| Proposed marks | (640,596), (604,626) | hollow can / nun outlines | none | unlit |

Hazards: *429 Shoal*, blob (470,660,56,1.3) closing the 5-contour, danger-line ring, name serif-italic 17 at (470,688). Wreck "Wk" at (560,400) from `stats.scrapy.stale_branches[0]` (name serif-italic 14, year 13), omitted if the key is absent. "Local knowledge advised · see Notices 1–5" 13 upright at (330,610) (26). One pencil note, serif-italic 14 `t.muted` −6°, at (700,232), leader to the Rep ring: "sitemap says yes; the lead says no".

**Soundings.** Survey ground: 6 per line at x = 720 + j·60, 11px italic, `int((1.5−field)·38)` clamped 4–60, none on the last line at t = 0; culled under 28px apart (33). Approach water: `soundings(field, (220,20,460,680), n=24, size=11)` italic, clearance 40. Contours (T6) at {2, 5, 10, 20}, figures in line breaks; tints to 5 and 10.

**2b. Inset "SCRAPY HARBOR · inset · ×3".** Three basins at ×3 about (150,440): outer `stage1_discovery` widest and deepest, sill, inner `stage2_page_analysis`, sill, dock `stage4_summaries`; table names upright 13; one sounding per basin (rows ÷ 1000, subscript hundreds per T5's glyph), upright if `stats.scrapy.run` else italic. Quays: "PostgreSQL · metrics", "Redis · queues", "Prometheus" mast, Grafana Lt tower (5:1, lantern on the main light's `begin`), "Horn", **"Traffic Sig"** three-lamp mast beside Redis (label only; no current state claimed), "Summarization Wks · BART" shed (20), Ldg triangles, anchor, "Delta Lake" italic 17.

## 3. Panels (strings pre-sized to fit Plex Mono 13)

**ZOC panel**: header "ZONES OF CONFIDENCE" 13 tracked at (692,42); mini-sheet 96×54 at (692,48) with bands A/B/C; table at x 800, rows y 60/76/92: `A sitemaps · existence doubtful` · `B CT logs · exists, may not answer` · `C Common Crawl · as reported`; under it, 13px: **"A: as declared by the site. B, C: as found."**

**rustmapper block**: title "rustmapper" serif 28 at (52,740); "PyPI {version} · provisional · {released}" 13 upright from `stats.edition` (19); "NOTES" 13 tracked at (52,786); notes 13, pitch 16 from y 804, verbatim:
`1 Frontier hashed by registrable domain` · `2 One shard per core · permits 256–1024` · `3 Sized by redb commit latency · 250 ms` · `4 WAL crc32 · rkyv · checkpoints to redb` · `5 Seeds A·B·C · robots crawl-delay kept`.
WAL tape at (52,896): 56 cells 8×6, the last line's 8 cells `<set>` on each fix; caption "write-ahead log · one cell per sounding" 13 at (52,922).

**Scrapy Harbor block**: title "Scrapy Harbor" serif 28; "Python · edition main · {commits} commits" (`stats.repos[Scrapy].commits`, upright); NOTES:
`1 Typed Arrow schema per table` · `2 schema_mode=merge, partition by domain` · `3 Dedup by URL hash and MinHash` · `4 OPTIMIZE/VACUUM queued as maintenance` · `5 Breakers wrap http · delta · redis` · `6 BART-large-CNN summaries on the worker`.
No coverage figure anywhere (20 F1: gate CI at 85 with a badge or say nothing).

**Legend**: header "SYMBOLS ON THIS CHART AND ON CHART {N}" 13 tracked at (402,728); columns at x 402 and 650, symbol cell 28, text at +36, 13 upright, pitch 15 from y 748, thirteen rows each. Every symbol is a `<use>` of the chart's own id (`sym-can`, `sym-nun`, `sym-light`, `sym-ldg`, `sym-trafsig`, `sym-horn`, `sym-anchor`, `sym-wk`, `sym-wp`, `sym-rep`, `sym-ed`, `sym-sd`, `sym-zone`; dashes by name).

| Col 1 | Col 2 |
|---|---|
| green can — `G can · port, returning` | dotted ring — `Danger line · shoal` |
| red nun — `R nun · starboard` | two swatches — `Tint · under 5 · under 10` |
| star + flare — `Light · its character` | T-dashed — `Restricted · robots.txt` |
| triangles + line — `Ldg line · health check` | dash "1 5" — `Track line · one shard` |
| one stack — `Traffic Sig · breaker` | vertical dash — `Check line · dedup` |
| stacks GGG / RRR / GWG — `go · stop · one at a time` | pecked + hollow mark — `Proposed channel · unlit` |
| horn arc — `Horn · Alertmanager` | hatch — `Hatch · unsurveyed` |
| anchor — `Anchorage · Delta tables` | dotted waver — `Limit of survey` |
| Wk — `Wk · dead branch, year` | boxed A — `Zone letter · seed source` |
| ⊙ — `Waypoint · pipeline stage` | `4₂` — `Sounding · thousands` |
| `290°` — `Bearing · true` | `54` — `Upright · measured` |
| Rep ring — `Rep · reported, not found` | *54* — `Sloping · illustrative` |
| ED islet — `ED · existence doubtful` | `SD` — `SD · sounding doubtful` |

## 4. Night rules

Contours `t.ink2` at 0.6× day opacity; soundings .55; land `#172740` (T6 may lift paper per 27); tints .20/.10; hatch .12; semantic text ≥ .85 (10). Lights brightest: gradient-circle halos r 12, no `feGaussianBlur` (12); Grafana Lt a static ruled flare pair at .08. Day: no halos, dots flash at .9. Colour never alone: nun/can shape plus odd/even numbers (09).

## 5. Motion (discrete only; everything else `fill="freeze"`)

| id | element | animation | repaints |
|---|---|---|---|
| `ap.lights.g` | G"1", G"3" dots + halos | opacity `discrete` values `1;0` keyTimes `0;.1` dur 4s | 0.5/s |
| `ap.lights.r` | R"2", R"4" | same, begin 2s | 0.5/s |
| `ap.lt.grafana` | main star + inset lantern | `1;0` keyTimes `0;.03` dur {scrape_interval}s | 0.13/s at 15s |
| `ap.packet` | `boat(s=.55)` on the lit channel | `animateTransform translate` + `rotate`, `discrete`, 8 values from `smooth_path(W0..ANCH)` at keyTimes 0–.25, hold at ANCH, opacity `1;0;1` at .99/1, dur 96s indefinite | 0.08/s |
| `ap.survey.fix1..8` | `boat(s=.8)` on the last track line | discrete translate, begin 24s + 2(k−1) | 8 total |
| `ap.snd.k`, `ap.wal.k` | sounding k, WAL cell k | `<set opacity to=1 begin="ap.survey.fix{k}.begin">` | same instants |

Steady state ≈ 1.2 repaints/s (gate ≤ 2). t = 0: everything drawn except the last line's soundings; vessel at its east end, lights lit, packet boat at W0, 48 WAL cells lit. t = ∞: plus that line and 8 cells, vessel frozen at the west end. Reduced-motion edition = end state, `<animate>`/`<set>` stripped (T4).

## 6. Phone edition (720 × 1240, `(max-width: 767px)`; sources phone+dark, phone, dark, img; reduced-motion above)

`ed.P(x,y)` rotates the chart 90° anticlockwise, scales 720/700, crops land to x ≥ 60 and the band to 64px; symbols placed through `P`, drawn upright; north arrow top-left pointing left ("oriented to the channel", 26). Type in 720-space: names 30, semantic 26, texture 18, nothing else (10). Kept: "SCRAPY HARBOR", "Delta Lake", four lit marks, Grafana Lt, anchor, limit line, "UNSURVEYED", 14 soundings, three doubt marks. Cut: inset, ZOC, blocks, legend, pencil note, bearings, check lines. Motion: lights only. Fallback: two stacked 720 × 600 halves (east above west), the second `<picture>` served a 1280 × 1 transparent SVG on desktop.

## 7. Alt text (22 words)

"Sheet 3, Approaches. Survey ground east, where rustmapper sounds; buoyed channel west into Scrapy Harbor; legend defines every symbol; upright figures measured."

## 8. Interfaces

**Provide:** `approaches(t, ed) -> str`; symbol ids `sym-*`; dashes `DASH_TRACK "1 5"`, `DASH_PECK "4 4"`, `DASH_RESTRICT "6 3" + teeth`, `DASH_LIMIT "1.5 4"`, `DASH_DANGER "0 4.5" round`; the legend wording as the page's single definition (T8 repeats the upright/italic sentence in the Colophon, 09); timeline ids `ap.*`.
**Need.** **T7:** `stats.repos` count; `stats.edition {version, released}`; `stats.repos[Scrapy].commits`; `stats.scrapy.scrape_interval_s` (from `monitoring/prometheus.yml`); optional `readiness_period_s`, `stale_branches[] {name, last}`, `run {date, tables{name:{rows, version}}}` from `exports/run-*.json`; the rule that a value quoted from a pinned source file counts as measured (256–1024, 250 ms). **T9:** `log.json.shards`, `log.json.measured`. **T5:** 13px floor; upright vs italic for mark labels; the `4₂` subscript glyph; whether Plex Sans Condensed is vendored (notes ≤ 40 and legend rows ≤ 25 characters, so Plex Mono fits regardless). **T6:** contours {2,5,10,20} with figures in breaks, two tint bands, HAIR/PEN/BRUSH weights, hatch generator, integer rounding, star-and-flare `light()`, new `boat()`, `lateral_offset()`. **T4:** discrete `animateTransform` sampler for `smooth_path`, `set`/`flash` helpers, reduced-motion strip, filmstrip times 0/24/48/72/95.9 s. **T2:** "SEE SHEET 3" coverage box on the hero around the harbour and its eastern approaches; hero drops upright 512. **T8:** "read from seaward"; politeness sentence for rustmapper and Scrapy only; bullets without 90%+ or "breakers on hosts"; "meant to feed" for the proposed channel. **T10:** warm-up ≥ 42 s before counting repaints; legend `<use>` diff test; 360px OCR. **T1:** `<picture>` source order; the Actions step that reads the two Scrapy files.

## 9. Build order, effort, risks, left out

Geography, coast, basins (4 h) → symbol library on T6's weights (3 h) → survey ground, restricted area, doubt marks, soundings (3 h) → inset (3 h) → blocks, ZOC, legend + diff test (3 h) → motion (2 h) → night (1 h) → phone mapper (4 h): **≈ 23 h**. Risks: inset lettering at 68% (13px floor holds); `log.shards` missing (n = 8, caption italic); Plex Mono widths (build fails on overflow); the rotation mapper (fallback halves). Left out: foul ground, sector light, governor gauge, speed-limit mark, WAL dedup cells, every upright 512/256/16/90, second pencil note.

## 10. Acceptance criteria

1. `grep -E "512|ILLUSTRATIVE|PENDING|SEEDED|90%"` on both editions → 0; upright figures are only chart number, PyPI version/date, Scrapy commits, `Fl {s}s` and run-backed basin rows.
2. Every legend `<use>` resolves to an id on the sheet and vice versa; no string overflows its cartouche (bounds check).
3. Odd greens south, even reds north of a channel heading 270–310°; Ldg bearing equals the final leg; chart-number position matches Sheets 1 and 2 to the pixel.
4. T10 harness after 42 s warm-up: ≤ 2 repaints/s, 0 with lights and packet boat stripped; no `animateMotion`, animated geometry or filter; raw < 300 KB.
5. Filmstrip at 0/24/48/72/95.9 s: every frame finished; reduced-motion edition equals the end state.
6. Phone at 360 CSS px: OCR recovers "SCRAPY HARBOR", "Delta Lake", "UNSURVEYED", four mark numbers, "Grafana Lt"; nothing under 18px in 720-space.
7. Changing `scrape_interval_s`, `log.shards` or `stats.scrapy.run` changes the light character, track-line count or basin soundings.
