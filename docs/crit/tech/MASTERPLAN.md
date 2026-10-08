# MASTERPLAN — the "Chart" profile README, v9

Integrator's merge of T1–T10. Where a section and this plan disagree, this plan wins; where this plan is silent, the section stands. Every number here is either from a lead's section, from TECH-BRIEF's verified facts, or marked as a decision.

---

## 1. Executive summary

**Thesis.** *The web is wrong about itself. Ben surveys the parts that are off the chart.* The hero says it in one italic line; every sheet argues it with the edge of the survey (soundings thin, hatching at the margin), and the footer is where the water goes over the edge.

**What the finished page is.** Six SVG sheets, 38 files, redrawn nightly from `assets/stats.json` by `scripts/build_assets.py`, served from the orphan `chart` branch, wrapped in a README whose plain text alone tells a hiring manager what Ben builds.

| # | Sheet | Size (1280-space) | One line |
|---|---|---|---|
| 1 | **Hero · Chart No. {N}** | 1280×740 | The archipelago: one feature per public repo, area ∝ Ben's commits; 52 weekly soundings generate the contours; two-ring rose as a 24-hour clock in author-local time; a course from the unsurveyed margin into Scrapy Harbor; the boat sails in once (4–28 s) and anchors. |
| 2 | **Soundings · Sheet 2** | 1280×400 | Tide table of the same 52 weeks (HW with its cause, LW, typical week, slack water) above a fleet register of 21 per-repo sparklines on one shared scale. No motion. |
| 3 | **Approaches to Scrapy Harbor · Sheet 3** | 1280×960 | The climax: rustmapper's survey ground east (one track line per shard), a buoyed Region B channel heading 290° into the harbour west, the rustmapper→Scrapy link charted as a *proposed, unlit* channel, Zones of Confidence, harbour inset with real Delta tables, and the page's single legend that defines every symbol and the upright/italic convention. |
| 4 | **Ship's log · Sheet 4** | 1280×490 | One rustmapper session on ruled paper, computed-consistent and italic until Ben records a real run; the nightly heartbeat line is typed in once (44 s) and the cursor blinks. |
| 5 | **Instruments · Sheet 5** | 1280×290 | Equipment list in three columns (LEAD · LOG · LOOKOUT) hung on the right two-thirds of the sheet, bold where the fitting's repo is active this quarter; mirrored in Markdown. No motion. |
| 6 | **Limit of survey · Sheet 6** | 1280×270 | The water leaves the sheet; the boat arrives (40–64 s) and anchors at the limit line; the only ambient loop (swell, mist); a serpent rises once every 96 s where "Obstn rep. 2026 (PA)" is charted. |

**What makes it one of a kind.** Every figure on every sheet is real or italic, by a convention a hydrographer would recognise; the islands *are* the portfolio and change when the data does; the chart counts itself (the profile repo is a feature, the chart number is the repo count); the motion is the chart surveying itself and every still frame is a finished sheet; night is designed (lights are the brightest things), not inverted; and four uncaptioned second-look layers reward a second visit.

**How we know it is done.** `check.py --ci` exits 0 (or 2 with only position/expiry warnings), the regression suite is green and GitHub post-merge steps 1–4 are clean; then the judged rubric scores ≥ 30/36 with no zero and J1/J2/J7/J10 each ≥ 2, **and** the five-second test on the shadow profile passes (≥ 80 % name the field, ≥ 60 % recall the name, ≤ 10 % call him a Scrapy maintainer, ≥ 80 % read name and thesis at 360 px). Verbatim in §7.

---

## 2. Decisions log

Each: the conflict → the decision → why. Tie-break order: thesis, honesty, the 360 px reader.

1. **Harbour orientation (T2 enter 217°, entrance NE vs T3 harbour west, channel ~290°).** → **Both sheets use a final approach leg of 290° true.** Hero course: WP1 (1136,296) → WP2 (1046,360) → WP3 (900,470) → **WP4 (842,580)** → WP5 (776,556) anchorage; bearings **235° · 233° · 208° · 290°**. Hero marks swap sides for a 290° heading in Region B: **R "2" nun at (827,551) north of the leg, G "1" can at (813,593) south.** Harbour basin kernels move to (800,566) and (824,572) so the entrance opens ESE. Coverage box **(680,470,210,160)**, "SEE SHEET 3" at (894,476). Sheet 3: W4 becomes (236,471) so W4→ANCH is exactly 290°; Ldg Lts 290°. *Why:* Sheet 3 is a larger-scale chart of the hero's harbour and must be north-up with the same channel bearing; moving one hero waypoint and two buoys is cheaper and safer than rotating T3's 1280-wide geography, and a westward course needs no tack (T4's `tack()` stays in the kit, unused on the hero).
2. **Instruments width (T9 800×290 at 62 % right-aligned vs T8 declined for the type floor).** → **Full-width 1280×290 sheet; the three columns occupy x 480→1280, the left 480 px carries only the rotated group labels, the footnote and the folio.** No `align`, no `width="62%"`. *Why:* the silhouette 27 wanted survives, the scale is the same 0.68 every sheet gets (13 px → 8.8 px), the phone edition is a proper 720-wide file instead of a 223 px sliver, and we drop a sanitizer dependency.
3. **README markers (T1 `<!-- chart:<sheet> -->` vs T8 `x:start/end`; T7 `stat:key` vs T10 `n:key`).** → **Blocks: `<!-- name:start -->…<!-- name:end -->` with names `picture:<sheet>`, `position`, `contact`, `figures`, `notices`, `instruments`, `license`. Inline numbers: `<!-- n:key -->…<!-- /n -->`.** *Why:* T8's README already uses the block form; T10's inline form is shorter and T10 writes the checker.
4. **Soundings sheet height (T9 400 vs 240).** → **400, with the fleet register folded in (confirmed).** *Why:* 21 sparklines on one scale are the honest answer to "which repos are alive" and still shorter than every other chart sheet, so the arc (overture → short → tall climax) holds.
5. **Approaches canvas (T3 960 vs 880).** → **1280×960; phone 720×1240.** T4/T6 tables updated. *Why:* the climax is the tall sheet and the full legend needs its 224 px strip.
6. **Type floors (T5 roles vs T10 phone 26/18).** → **Floors are in sheet space: desktop 13 semantic / 11 texture / 17 serif; phone 26 / 18 / 30 serif. The "×0.68 ≥ 9 px" arithmetic is dropped** (13 × 0.68 = 8.8 would fail its own rule). Scale is T5's: `11 · 13 · 17 · 22 · 28 · 36 · 46 · 60 · 96` (+176 hero only); phone `18 · 26 · 30 · 40 · 132`. Off-scale sizes in T3/T9 are remapped: 14 and 14.5 → 13, 18 and 19 → 17, 30 → 28, serif-italic 14 notes → 17. *Why:* T5 measured the hairlines; T10's phone floors are T5's own phone scale; one rule the lint can read from `tokens.py`. **Revised, v9.1 (8 Oct 2026):** the dropped arithmetic was right and the decision wrong: the live profile printed 13 px at 8.8 px and read as crushed. Desk scale is now `16 · 19 · 25 · 32 · 41 · 53 · 68 · 88 · 141 · 176`, floors 19 / 16 / 25, line weights ×1.3; sheets grew where their furniture needed it (soundings 520, approaches per its module, log 590, instruments 360).
7. **Hero thesis line (metaphor vs plain; UX wanted an A/B).** → **Launch default: "I survey a web that is wrong about itself." under the name; the plain register already sits in the hero title block ("Crawl and data infrastructure · Python and Rust") and in the at-a-glance table. The A/B runs on the shadow profile in the acceptance session (variant B: the role line under the name, the metaphor moved to the title block); swap only if A fails the ≥ 80 % field-naming threshold and B passes.** *Why:* the thesis is the page; the hero already carries both registers, so the test only decides their order.
8. **Where SVGs live.** → **Orphan branch `chart`, folder `assets/v9/`, one force-pushed commit per run (T1 confirmed). README URLs: `https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/<sheet>-<edition>.svg`.** T8's `main/assets/…` URLs are replaced. *Why:* ~3 MB of path data per changed day does not belong in `main`'s history; stats/log/lock JSON stay on `main` as the chart's own log.
9. **Edition list and `<picture>` order (T1 vs T2/T4).** → **Six editions per sheet, named `day · night · still-day · still-night · phone-day · phone-night`, plus `hero-phone-still-day/night` (38 files). Source order, most specific first: phone+dark, phone, reduce+dark, reduce, dark, `<img>` day; the hero prepends phone+reduce+dark and phone+reduce.** No `height`, no `<a>` wrapper. *Why:* a phone edition is already motion-safe except the hero, which keeps a 4 s opening and lights, so a reduced-motion phone reader is owed a still.
10. **Motion timeline (T4 24 s vs T2 42 s; survey 28 vs 24; typing 48 vs 30; serpent 44 vs arrive+20).** → **One page-wide timeline (§2.1): hero boat 4–28 s; Approaches survey fixes 28–42 s; log heartbeat typed 44–48 s, cursor from 48.5 s; footer arrival 40–64 s; serpent first at 84 s then every 96 s.** Soundings and Instruments carry no motion (T9/12 over T4's tide draw-in). *Why:* "one continuous thing at a time" (12 binding): hero 4–28, then only the footer, whose arrival is the one post-hero continuous window; the survey is discrete and sits in the gap; typing follows the survey; the serpent needs an anchored witness.
11. **Fleet register.** → **Confirmed: lives on the Soundings sheet; no seventh sheet.**
12. **Profile repo on the chart (T1/T2/T7 keep vs 36 out).** → **Keep as *Profile Shoal* with the △ station; author filter removes `github-actions[bot]` so it grows only when Ben edits it.** *Why:* "the chart counts itself" is the better sentence once the bot problem is gone; `repo_count` honestly includes it.
13. **Fonts.** → **Confirmed: vendor IBM Plex Sans Condensed (Regular, Italic, Light) and IBM Plex Mono Light; delete Inter and DejaVu; re-subset Instrument Serif with `kern,liga,subs,sups`.** T8's colophon names three faces.
14. **Worker count, shards, coverage.** → **"512" is never upright; it appears only in the log (what Ben typed) in italic. The notes line "permits 256–1024" sets its figures italic (quoted code defaults, not a run). Shards = `log.json.profile.shards` = `machine.cores` of the logged machine, italic until `measured`. No coverage percentage anywhere (sheet, bullet or badge) until Ben gates CI.** *Why:* four sources disagree on workers; T3's "no upright 512/16/256/90" is the honest floor.
15. **Field convention (T2 intensity: contours enclose ≥ n; T3/T6 depth: contours enclose ≤ n).** → **Depth = count on every sheet.** Hero: weekly commits are depths; contours 5 · 10 · 20 · 50 are depth contours; tint B under 5 (darker), tint A under 10; features lift the field: islands break the surface (coastline at 0), shoals stop between 0 and 5 (tinted, danger line at the 5-contour); **area is asserted at the 5-contour for every feature (±8 %)**; spot heights = repo commits, upright. Open-water base = median of `weeks[].n` clamped to [10, 50]; T2 re-solves amplitudes in this frame. *Why:* STANDARDS 4 and J4: soundings must read as depths, small near land, or a hydrographer fails the sheet; T3's "the raw basin is deepest" already assumes it.
16. **Kernel (T2 compact bump vs T6 Gaussian RBF).** → **Compact bump `W(q)=(1−q²)³`, h = 30 for soundings, h = 1.33–1.82 r for features; `Field.from_soundings(kernel="bump")`.** *Why:* features and soundings never leak into each other, so the bracket test and the area assertion stay local.
17. **Hero water soundings: 52 weeks (T2) vs 34 (T6/T7).** → **52, four rows, oldest seaward; fallback three rows.** *Why:* the tide table shows 52; "same data" means the same 52.
18. **Weeks unit (T7 commit-days vs T2/T9 commits).** → **`weeks[].n` = commits (author-filtered); `weeks[].days` = commit-days, stored for the colophon. Hours and weekdays stay commit-days in author-local time.** *Why:* the unit line says "SOUNDINGS IN COMMITS", area is commits, and the sprint must read as a sprint (HW 312 · game_engine, 13 days).
19. **Tide upright source (T9 GraphQL upright vs T7 clones upright).** → **Clone-derived, author-filtered weeks are the measurement and print upright; the GraphQL calendar is the second instrument, named in the source line and used by `check.py` (warn at >10 % disagreement).**
20. **Subscript meaning (T2 months active; T5 contributors; T3 hundreds).** → **Two rows in the legend: hero spot height `585₁` = commits, months with a commit; Sheet 3 sounding `4₂` = thousands, hundreds. Contributor counts are not drawn.** *Why:* the sprint reading is the honesty layer 08/32 asked for; thousands-with-hundreds is real chart grammar.
21. **Light colours.** → **Static flare and halo in `flare` (chart magenta) on every sheet; the flashing core is `light_core`; buoy bodies red/green by shape and number; day has no halos. Unit lines ("SOUNDINGS IN COMMITS", "SOUNDINGS IN URLS · THOUSANDS") in ink, not accent, on both sheets.**
22. **Sheet module contract (four variants).** → `build(ctx) -> str` and `alt(data, cfg) -> str` per module, with `ctx.ed` (Edition), `ctx.data`, `ctx.cfg`, `ctx.tl` (Timeline), `ctx.k` (type/run registry); phone and still are branches of `ctx.ed`, not separate functions.
23. **Indefinite-animation emitter (T1 `svgkit.loop()` vs T4 `Timeline`).** → **`Timeline.every()` and `Timeline.flash()` are the only emitters of `repeatCount="indefinite"`; `loop()` is deleted.**
24. **`check.py` ownership (T1, T4, T5, T7, T10 each wrote a checker).** → **T10's three-tier runner; T4's `check_motion`, T5's `check_type`, T7's ten data checks become plug-ins under `scripts/checks/`; T10's exit codes 0/1/2/3.**
25. **stats.json schema (T1 containers vs T7 keys).** → **T7's keys (§3.3), plus T1's `repos[].aliases/slot`, `tz_offsets`, T2's `repos[].months_active`, `[[sources]]` dates from `chart.toml`, and `repos[].stale_branches[]` for Scrapy.**
26. **log.json schema (T7 vs T9).** → **T9's schema (`profile`, `start`, `heartbeat.template`), plus T7's `source ∈ computed|session|cc-index` and `machine{cores, host}`; T7's `check_log` rules apply.**
27. **Folio position.** → `CHART NO. {N} · SHEET k` bottom-left outside the neat line at (24, h−5) on every sheet, including Soundings and Log; the notices count `N` top-right at (1262,14) on chart sheets.
28. **Wrecks.** → Only `archived == true` repos are wrecks, at T2's four fixed positions; until Ben archives, the four shelf repos are islets.
29. **Copy fixes forced by the above (→ T8):** alt "A boat sails in and anchors."; colophon Motion ("The boat sails in once in the first half-minute and anchors; after that only the lights keep time."), Variation ("counted in my own timezone; the arrow points at the busiest hour"), Type (three faces); "read from seaward"; URLs to the `chart` branch; soundings alt loses "draws in once".

### 2.1 Page-wide timeline (absolute seconds from each image's load; all `fill="freeze"` unless loop)

| t (s) | Sheet | Event | Class |
|---|---|---|---|
| 0 | all | every sheet finished except the hero's opening; all lights lit; footer swell running | — |
| 0–4.0 | hero | contours deep-first 0.2+0.12·i (1.6 s draw) · tints 1.0/1.3 · land, danger lines, wrecks, anchorage 1.6 · soundings 1.4+0.04·k in course order · rose settle 2.0 · names 2.2+0.1·rank · "Ben"/"Russell" 2.6/2.85 · thesis 3.1 · rules 3.3 · imprint, bearings, light labels, pencil note 3.6 | one-shot |
| 0 → ∞ | hero | G "1" Fl G 4s (begin 0) · R "2" Fl R 4s (begin 2) | discrete loop, ≤1 repaint/s |
| 0 → ∞ | approaches | G "1"/G "3" Fl G 4s (0) · R "2"/R "4" Fl R 4s (2) · Grafana Lt Fl {scrape_interval}s · packet boat 7 fixes at 0,4,…,24 then hold to 96, 0.4 s fade at 95.5 | discrete loops, ≈1.2 repaints/s |
| 4.0–28.0 | hero | boat sails WP1→WP5, 64 sampled `animateTransform` values, `settle` at both ends, `scale(-1,1) rotate(-4)`; anchored forever at 28 | **continuous** (the page's only one besides the footer) |
| 28, 30 … 42 | approaches | survey vessel plots 8 fixes on the last track line; sounding k and WAL cell k `<set>` at fix k | discrete one-shot |
| 40–64 | footer | `arrive` 90→980 settle; at 64: rotate −4→0 (0.65), main luffs once (0.8), rode + anchor + "14 · good holding" fade 0.65 | continuous on the ambient sheet |
| 44–≈48 | log | heartbeat line typed per glyph (36–60 ms, +160 after space); cursor rides | discrete one-shot |
| 48.5 → ∞ | log | cursor blink, 1 s period | discrete loop, 2 repaints/s |
| 0 → ∞ | footer | swell 10 s `sea`, hull −2 px, three mist arcs on the 10 s grid, fall lines | ambient, ≤4 ms/frame |
| 84, 180, 276 … | footer | serpent rises 0.9 / holds 0.6 / sinks 0.9 (humps +0.25/+0.5 s); three ripples over 20 s | one 96 s-period loop |

Grid: every discrete instant on 0.5 s; loop periods ∈ {1, 4, 10, 15, 96} (1 s cursor, 15 s Grafana from real config; 2 s Iso deleted with the sector light). Longest loop L = 96 s. Perf warm-ups: hero 30 s, approaches 44 s, log 50 s, footer 66 s. Filmstrip instants: T10's set {0, 0.5, opening_end+0.1, 24, 48, 72, 95, 600} plus the event instants {4.1, 28.1, 42.1, 48, 64.1, 84.5}.

---

## 3. Interface contract

### 3.1 Modules

```
chart.toml · LICENSE (MIT) · LICENSE-ASSETS.md (CC BY 4.0)
scripts/tokens.py            Theme(edition), INK, WIDTH(W), DASH, ROLE/SCALE/SCALE_PHONE, floors; --md → DESIGN.md
scripts/svgkit.py            Edition, Timeline, svg(), text engine (shape/text/text_use/runs/sounding/text_on_path), run registry
scripts/chartlib/            __init__ (re-exports) field.py water.py place.py symbols.py furniture.py
scripts/data/                github.py survey.py pypi.py releases.py claims.py model.py stats_schema.json log_schema.json
scripts/build_stats.py       fetch → model → validate → one write of assets/stats.json
scripts/build_assets.py      sheet × edition → bounds → assets/v9/*.svg + build-report.json
scripts/render_readme.py     fills README markers from chart.toml, stats.json, FITTINGS
scripts/check.py             three tiers; plug-ins in scripts/checks/{xml,size,motion,type,bounds,strings,contrast,legend,alt,position,data,log,flash,expiry}.py
scripts/render.mjs           frames | silhouette | phone | matrix | shadow   (Playwright)
scripts/perf_check.js        12's harness + --warm --trace --width --dpr --json
scripts/preview.py           resvg stills, social PNG
scripts/sheets/              hero.py soundings.py approaches.py log.py instruments.py footer.py
scripts/fonts/               InstrumentSerif ×2 · IBMPlexSansCondensed ×3 · IBMPlexMono Regular/Medium/Light/Italic · OFL texts · subset.sh
tests/                       fixtures stats-{golden,stress,rename,noweeks}.json · golden/*.png · unit tests
.github/workflows/profile.yml (daily 06:20 UTC, dispatch, push on scripts/**, repository_dispatch) · perf.yml (scripts/** pushes, Sundays)
.github/PULL_REQUEST_TEMPLATE.md
main:   assets/stats.json assets/log.json assets/layout.lock.json README.md DESIGN.md
chart:  assets/v9/*.svg social/hero-{day,night}.png build-report.json   (orphan, one commit per run)
```

### 3.2 Public signatures (reconciled)

**tokens.py (T1 container, T5/T6 values)**
```python
@dataclass(frozen=True) class Theme: edition: str; paper, paper_log, land, ink, ink2, muted, shallow_a, shallow_b, accent, ok, flare, light_core, hair: str
THEMES: dict[str, Theme]           # day, night (phone-* and still-* reuse them)
W = {"HAIR":0.6,"PEN":1.0,"LINE":1.6,"BRUSH":2.6}
DASH = {"DANGER":"0.1 {g}","COURSE":"0.1 7","TRACK":"1 5","PECK":"4 4","LIMIT":"1.5 4","APPROX":"3 3","RESTRICT":"6 3"}
SCALE = (11,13,17,22,28,36,46,60,96,176); SCALE_PHONE = (18,26,30,40,132)
ROLES[edition][role] -> (font, size, tracking, case, grade)   # roles per T5 §2.1
FLOORS = {"desk":{"semantic":13,"texture":11,"serif":17}, "phone":{"semantic":26,"texture":18,"serif":30}}
```

**svgkit.py**
```python
@dataclass class Edition: name: str; theme: Theme; motion: bool; scale: Literal["desk","phone"]; width: int
def svg(ed, w, h, body, defs, sheet) -> str          # id prefix f"{sheet}-", honest header, opaque paper
class Timeline:                                     # T4 §2.1 verbatim; motion=False → end states
    def __init__(self, sheet, motion=True, period=96.0, quantum=0.5, ambient=False)
    def cue(name, begin, dur) -> float;  def t(name) -> (begin, end)
    def anim(attr, values, dur, begin, ease=None, freeze=True, repeat=None, key_times=None, discrete=False, still=None) -> str
    def xform(kind, values, dur, begin, ...) -> str
    def fade_in(inner, begin, dur=0.25, rise=3, ease="settle") -> str;  def draw_in(path_attrs, dur=1.6, begin=0.0, ease="draw") -> str
    def reveal(inner, begin) -> str;  def typed(s, x, y, role, begin, seed, pace=(0.036,0.06), space=0.16) -> (svg, end, times)
    def flash(character, period, begin=0.0, still="lit") -> str       # the one light-character parser
    def sail(path_d, begin, dur, n=64, ease="settle", mast_x=3.0) -> Sail(anim, end, tacks, facing)
    def fixes(points, begin, every=4.0, labels=None, hold=None) -> str
    def every(kind_or_attr, segments, begin, period=96) -> str          # the only other indefinite emitter
    def report() -> dict   # {class, indefinite, repaints_per_s, opening_end_s, longest_loop_s, loops[], continuous_windows, violations}
# type engine (T5)
def shape(s, font) -> list[Glyph]
def text(s, x, y, role="label", fill=None, anchor="start", within=None, semantic=True, truth=None, key=None) -> str
def text_use(...)  # same signature, <use> per glyph with x/y (typed() depends on it)
def runs(parts: list[(role, text)], x, y) -> str
def sounding(value, x, y, sub=None, truth="measured"|"illustrative"|"datum", role="texture", anchor="middle") -> str
def text_on_path(s, polyline, role, start=0.0, side="above", spread=None) -> str
def text_width(s, role=...) -> float;  def exclusions() -> list[bbox];  def exclude(name, x, y, w, h)
def check_type(edition) -> list[str];  def glyph_count() -> int
FIGURES: list[(sheet, key, value, style)]          # filled by text(truth=, key=) and sounding(); T7's registry
```

**chartlib (T6; `k` = svgkit)**
```python
class Field: from_soundings(w, h, samples, base, features, coast, kernel="bump", h_snd=30, ridge=1e-3); value(x,y); grid()
def contours(field, levels, clip=None) -> list[Contour(level, pts, closed, length)]
def compact_path(pts, closed, every=3) -> str;  def smooth_path(pts, closed, every=2) -> str;  def monotone_path(pts) -> str
def contour_labels(cs, role="contour-figure", min_len=160) -> list[(Contour, i0, i1)];  def draw_contours(cs, index_levels, approx_clip=None) -> str
def tint_bands(cs, theme) -> str;  def coastline(cs, theme, swell=True) -> str;  def danger_lines(cs, level, theme, jit) -> str
def hatch(poly, theme, jit, kind, clip_id) -> (defs, body);  def coast_vignette(poly, theme, jit) -> str;  def unsurveyed_band(x,y,w,h,theme,jit,label_cb) -> (defs, body)
@dataclass class Feature: name, value, kind, x, y, r, amp, area, axis
def place_features(features, drawable, exclusions, course_pts, seed, slots, cap=32) -> PlaceReport
def solve_radii(field_builder, features, k_area, tol=0.08, iters=4);  def spot_heights(features, cs, clearance=8)
def soundings_along(course_pts, values, rows=(-48,-24,24,48)) -> list[(x, y, value)]
def stroke(width_key, color, opacity=None, dash_key=None, jit=None, caps="round") -> str      # the only stroke emitter
def symbol_defs(theme, prefix, edition) -> str;  def use(name, x, y, prefix, scale=1.0, rotate=0, extra="") -> str
# symbols: sloop, sloop-glyph, can, nun, light, flare, traffic, horn, anchorage, wreck, waypoint, station, fix, ldg, halo, correction
def sloop(theme, detail: bool) -> str;  def lateral(kind, number, theme, misreg=True) -> str;  def light(theme) -> str
def traffic_signal(theme); def horn(); def doubt(kind: "ED"|"Rep"|"SD"|"PA", x, y); def serpent(theme)
def course(points, theme, jit, pecked=True) -> str;  def course_samples(points, n=96) -> list[(x, y, heading)]
def lateral_offset(leg, s, side, d) -> (x, y);  def track_lines(x0,y0,x1,y1,n,spacing,theme) -> (str, segs);  def check_lines(segs, n, theme)
def restricted_line(pts) -> str
def frame(w, h, theme, kind="minute-bars"|"double"|"none"|"broken", gaps=()) -> str;  def margin_graticule(rect, meridians, parallels, theme)
def two_ring_rose(cx, cy, r, theme, hours24, modal, var_label_cb) -> str;  def source_diagram(x, y, w, h, zones, theme, jit)
def area_key(x, y, k_area, values=(10,100,500), theme);  def paper(w, h, theme, edition, jit) -> (defs, body)
class Jitter(seed, name)   # the one randomness source; keyed by sheet and element, never by data
```

**sheets/<name>.py (all six)**
```python
NAME: str; KIND: "chart"|"strip"|"paper"|"edge"; SIZES = {"desk": (w, h), "phone": (w, h)}; BREAKS: list[(what, how, why)]
def build(ctx) -> str          # ctx.ed, ctx.data, ctx.cfg, ctx.tl, ctx.k
def alt(data, cfg) -> str      # ≤ 25 words, plain, from data
```
Sizes: hero (1280,740)/(720,900) · soundings (1280,400)/(720,360) · approaches (1280,960)/(720,1240) · log (1280,490)/(720,220) · instruments (1280,290)/(720,48) · footer (1280,270)/(720,320).

**data / build / check**
```python
fetch_repodata.survey(repo, workdir, identity) -> dict | None
build_stats.main(mode: "live"|"cache"|"cache-failed") -> Stats;  build_stats.derive(repos, calendar, pypi, releases) -> dict
build_assets.main(editions=ALL, no_sounding=False, heartbeat=True);  sheets.log.simulate(profile, entries) -> list[Row]
render_readme.main(readme, cfg, stats, fittings) -> str
check.main(ci=False, release=False, dev=False, only=None) -> int   # 0 pass · 1 fail · 2 warnings · 3 could not check
```

### 3.3 `assets/stats.json` v2 (T7 owns; keys each sheet reads)

Top level: `schema:2, updated_at, taken, run_id, provenance{mode, failed_at, soundings_taken{taken, of}}, login, account_since, repo_count, followers, stars, commits, all_hands, calendar_total, first_commit, days_surveyed, languages[], repos[], unsurveyed[], hours[24], weekdays[7], hours_basis:"author-local commit-days", tz_offsets{}, variation{hour, year, prior_hour, annual_change|null, basis_days}, weeks[52]{start, n, days, repos{}}, tide{hw{start,n,cause,cause_days}, lw, median, slack{start,end,month}}, sweeps[], edition{project, version, date, releases, status, wheels[]}, notices[]{repo, tag, date, title, url, source}, corrections{year:[…]}, claims{id:{value, unit, source, sha, measured}}, trial|null, sources[]{letter, name, first|null}`.
`repos[]`: `name, aliases[], slot, commits, all_hands, others[]{name, commits, bot}, first, last, commit_days, months_active, hours[24], weekdays[7], weeks[52], active, dormant, archived, stale, stale_since, language, stars, span, stale_branches[]?`.

| Sheet | Reads |
|---|---|
| hero | `repos[]` (alias, slot, commits, months_active, first, active, archived, stale), `weeks[].n`, `hours[]`, `variation`, `repo_count`, `edition`, `notices` (N), `corrections`, `sources[]`, `unsurveyed[]`, `taken` |
| soundings | `weeks[]`, `tide`, `repos[].weeks/commits/name`, `repo_count`, `commits`, `calendar_total`, `updated_at`, `provenance` |
| approaches | `repo_count`, `edition`, `repos[Scrapy].commits/stale_branches`, `claims.scrape_interval/workers/shards`, `trial`, `log.json.profile.shards/measured` |
| log | `log.json`, `updated_at`, `commits`, `repo_count`, `provenance` (heartbeat and stale note) |
| instruments | `repos[].first/active`, `cfg.fittings`, `updated_at` |
| footer | `repo_count`, `notices` (N), `taken` |

Invariants `check.py` enforces: `repos` is a list; `sum(hours)==sum(weekdays)==commit_days` per repo; `commits+Σothers==all_hands`; no `seeded` key; `provenance.mode ∈ {live, cache}` with `taken` ≤ 8 days.

### 3.4 `chart.toml`

```toml
[chart]      login="BenjaminSRussell" release="v9" seed=27 breakpoint_px=767 base_url="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/"
[identity]   names=[...] emails=[...] bots=["github-actions[bot]","google-labs-jules[bot]","Claude"]
[position]   text=""                       # "" omits the slot (warning); ⟨ ⟩ fails the build
[contact]    linkedin="" resume=""         # "" drops the link
[copy]       thesis="I survey a web that is wrong about itself." role_line="Crawl and data infrastructure · Python and Rust"
[copy.review] role_line="2027-06"
[[notices]]  n=1 date="2025-11-08" repo="Rust-sitemap" title="…" url="…" source="pypi"   # hand-entered; releases appended by data/releases.py
[[features]] repo="Rust-sitemap" aliases=["rustmapper"] slot="named-5" kind="vessel"
[[sources]]  letter="A" name="SITEMAPS" first="2025-03"   # first optional
[claims.workers] source="Rust-sitemap:src/governor.rs" sha="…" value="256–1024" unit="permits" measured=false
[fittings]   # T9 table C: name → repo, group
[motion]     enabled=true
[budgets]    svg_kb=300 gz_kb=100 elements=3000 phone_svg_kb=120 page_gz_kb=250
[alt]        hero="…" soundings="…" …     # templates; alt_poem=[six lines]
[log]        path="assets/log.json"
[social]     hero_png_sha=""
```

### 3.5 `build-report.json` (T10 owns; T4/T6 contribute)

`{built, stats_sha, poem[], sheets{ "<sheet>-<edition>": {svg, sha256, w, h, form, bytes, gz, elements, paths, text[]{s, x0, x1, y, size, font, slant, role, tier, truth, key, rot}, exclusions[], breaks[], symbols_used[], legend[], lights[]{id, character, color, bbox}, motion{class, opening_end_s, longest_loop_s, loops[], repaints_per_s, continuous_windows, violations[]}, features[]{name, commits, area_px, cx, cy, ratio}, bracket_failures, lock_drift[], area_law:"area∝commits"} } }`. The report's sha256 of each SVG must match the file (check 1).

### 3.6 README markers and files

Blocks `<!-- picture:<sheet>:start/end -->` (the whole `<picture>`), `position`, `contact`, `figures`, `notices`, `instruments`, `license`; inline `<!-- n:key -->…<!-- /n -->`. Files per sheet: `<sheet>-day.svg`, `-night`, `-still-day`, `-still-night`, `-phone-day`, `-phone-night`; hero adds `hero-phone-still-day/night`. All under `chart/assets/v9/`; social PNGs under `chart/social/`.

---

## 4. Build plan

| Phase | Work (owner) | Depends on | Hours | Exit criteria |
|---|---|---|---|---|
| **0a Stop the bleeding** | delete `snake.yml` and `output` branch; `check=True`; non-zero exits; pinned requirements; concurrency; rebase (T1) | — | 2 | Nightly job is red on any failure; nothing half-published |
| **0b Foundation** (parallel) | `tokens.py` + `--md`, `Edition`, `svg()`, id prefix, integer coords, orphan publish stub (T1, 16) · type engine, fonts, `check_type` (T5, 17) · chartlib package: field, water, place, symbols, furniture, fixtures (T6, 35) · data package, schema, derivations, notices, claims, `log.json` v2 + `simulate`, honesty checks (T7, 20) · `Timeline` core, still mode, samplers, `flash`, `every`, `typed`, `check_motion` (T4, 19) | 0a | 107 | `build_assets.py` renders a blank sheet in all six editions from the committed cache; `tokens --md` regenerates DESIGN.md byte-identically; golden and stress fixtures load; `check.py --only fast` runs on the stub |
| **1 Hero** | kernels in the depth frame, area assertion, 52-week solve; slots/Halton/lockfile; title block and outside furniture; rose; double shoal, notes, marks at 290°; band; opening + sampled boat; night; phone + phone-still; checks (T2, 36 + T4 4) | 0b | 40 | T2 §5 criteria 1–8 pass; `check.py` fast+render exit 0 on the hero |
| **2 Approaches** (parallel with 1) | geography at 960, coast, basins; symbol library use; survey ground, restricted area, doubt marks; inset; blocks, ZOC, legend + `<use>` diff; discrete motion; night; phone mapper (T3, 23 + T4 4) | 0b | 27 | T3 §10 criteria pass; legend ids == sheet ids across hero/approaches/footer |
| **3 Supporting** (parallel with 1–2) | log sheet; soundings + fleet register; instruments 1280×290; footer with sloop/serpent; phone editions; tests (T9, 41 + T4 4) | 0b | 45 | T9 §5 criteria pass; footer ≤ 4 ms/frame; soundings and instruments 0 repaints |
| **4 README, docs, workflow** | README from T8 with §2 fixes, markers, alts, poem; `render_readme.py`; `profile.yml` + `perf.yml`, orphan publish, heartbeat path, social PNG; LICENSE files; DESIGN.md generated; PR template (T1 10, T8 6, T4 6) | 1–3 | 22 | `gh api /markdown` keeps six/eight sources, `<sub>`, `<details>`, anchors; a dry run publishes to the `chart` branch; a forced stats failure publishes the pencil-note edition |
| **5 QA, scratch repo, ship** | `check.py` three tiers, fixtures, goldens, `render.mjs`, `perf_check.js`, source matrix, shadow profile, OCR, engine matrix; heartbeat verification; judged rubric + five-second test + thesis A/B; acceptance.md (T10 30, T1 4, T7 2, all 8) | 4 | 44 | §7 gate met and recorded in `tech/acceptance.md`; social preview uploaded; Ben's list items 1, 5, 7 done |

**Total ≈ 287 h** of lead time; budget **310 h** with contingency. Critical path: 0a → 0b (T6 chartlib, 35 h, is the long pole; T2 can start on kernels against the `Field` interface in week 1) → Phase 1 → Phase 4 → Phase 5. With five leads in Phase 0 and three sheet leads in Phases 1–3, calendar time is about four working weeks.

---

## 5. Ben must do (not pipeline work)

1. **Bio.** Replace "Scraping enthusiast and full stack developer" with: **"Crawl and data infrastructure, Python and Rust. The web is wrong about itself; I survey the part that isn't linked."** (alternate: "Crawl and data infrastructure in Python and Rust. rustmapper on PyPI; Scrapy Harbor on GitHub."). Set location, website, hireable; pin both repos; reuse the sentence as repo description and PyPI summary.
2. **Position line.** Fill `[position] text = "⟨role⟩ · ⟨city or timezone⟩ · ⟨open to / currently⟩"` in `chart.toml`, or set it to `""` explicitly. The build fails while `⟨ ⟩` remains. Supply LinkedIn and résumé URLs or set them to `""`.
3. **Profile repo LICENSE.** "Add `LICENSE` (MIT for `scripts/`; sheets and copy CC BY 4.0). Delete `snake.yml`, the `output` branch, and `scripts/fonts/Inter*`, `DejaVu*`." The README's License bullet does not ship until both files exist.
4. **Rust-sitemap release hygiene.** "Add `LICENSE` (MIT, matching pyproject), tag `v0.1.3` at the published commit, create a GitHub Release with notes. Until then the Notices fall back to PyPI uploads and print 'four notices, one day'." Then: "Add a maturin-action release workflow (abi3 wheels: linux x86_64/aarch64, macOS x86_64/arm64, Windows), drop `target-cpu=native`, cut 0.2.0, and add a `repository_dispatch: release-published` to this repo. The edition line changes itself." Rename to `rustmapper` only after the `chart.toml` alias lands (byte-identical sheets are the test).
5. **Worker count.** "Pick one worker figure from `governor.rs` (min 256 / max 1024, 250 ms EWMA) and make README (32–512), PyPI summary (256) and `cli.rs` agree. '512' stays italic until all four match; then `claims.workers` sets it upright."
6. **Scrapy coverage.** "Gate CI at `--cov-fail-under=85` and publish the badge, or the coverage number leaves every sheet and bullet. No third option." Also: move the 930 self-filed issues to a Project; populate `bug` and `good first issue`; decide whether to rename the repo (copy works either way; "Scrapy Harbor" is the name on the page).
7. **A real log.** "Record one real rustmapper session on a domain you control (`rustmapper crawl … | tee assets/log.raw`), or run a Common Crawl index query; commit it as `assets/log.json` with `measured: true`, `source: "session"|"cc-index"`, `machine.cores` filled. Expect ~2 req/s on one host; the restraint is the demonstration." Until then the log is computed-consistent and italic.
8. **Scrapy trial export.** "Commit one `exports/run-YYYY-MM-DD.json` (rows per Delta table, `_delta_log` versions, wall-clock, host, 5xx rate, breaker trips); the anchorage soundings become those counts, upright." Also verify `monitoring/prometheus.yml` `scrape_interval` is the one you want on the chart (it becomes Grafana Lt's character).
9. **Archive the shelf.** "Archive `3d-swift-widget`, `2d-swift-widgets`, `MLX_convertion`, `Course_crusader` (or whichever four you would not defend); archived repos become `Wk` marks."
10. **go_go_go.** "Make header rotation opt-in with an identifying default UA, or the profile calls it 'browser-faithful fetching', not 'per-host politeness'."
11. **Optional Notice 0.** Decide whether to add a dated notice: "0.1.0/0.1.1 shipped without the engine; fixed that evening (8 Nov 2025)". Honest, and it makes the PyPI "four releases in 74 minutes" a story rather than a smell.
12. **Admin.** Create the scratch repo for T10's sanitizer/shadow tests; upload the social preview PNG once per design release; confirm the two commit totals (1,828 calendar vs clone-filtered) and 24 vs 21 repos on the first live run before `ED` marks are trusted; tell us of any fourth author identity string.

---

## 6. Risks and mitigations (top 10), and out of scope

| # | Risk | Mitigation |
|---|---|---|
| 1 | GitHub's sanitizer drops `(max-width)` or `(prefers-reduced-motion)` media | Order keeps the `dark`/`img` pair working alone; proven on the scratch repo before launch; if the app ignores `<picture>`, the hero `<img>` fallback becomes the phone edition (T10 decides) |
| 2 | Depth-frame re-solve (decision 15) shifts T2's amplitudes and the 52-sounding solve goes ill-conditioned near WP4–WP5 | Compact kernels, ridge term, three-row fallback; bracket test and ±8 % area assertion are the gates; stress fixture in Phase 0 |
| 3 | Author filtering shrinks features and flips kinds on the first live run | `layout.lock.json` shows every move; drift > 40 px is a warning not a rearranged sea; aliases fixed in `chart.toml` |
| 4 | Hero repaint cost during 4–28 s (18+3 ms/frame) on low-end phones | Phone hero uses 7 discrete fixes, not a continuous sail; 360 px DPR 3 gate ≤ 0.25 repaints/s after 6 s |
| 5 | A computed log reads as a demo | The "2 of 512 permits · one host" line and italic numerals say so; only Ben's real run cures it (list item 7) |
| 6 | Plex Sans Condensed changes caption widths; T3's pre-sized panels overflow | Every panel asserts `within=`; notes ≤ 40 and legend rows ≤ 25 characters; condensed is 18 % narrower than mono, so fits regardless |
| 7 | Trace timings vary ±20 % on shared runners | 2× headroom; perf fails only on two consecutive runs; perf on `scripts/**` pushes and Sundays, not the daily cron |
| 8 | A cancelled run between the `main` commit and the `chart` push | Publish is one force-push; the next run republishes; data and sheets are both derived from the same `stats.json` sha recorded in the report |
| 9 | `repo_count` 24 vs 21 surveyed: `ED` marks could libel live repos | `unsurveyed[]` is checked by hand on the first live run; `ED` only for repos returning no history |
| 10 | Chromium-only measurements; Firefox starts the SMIL clock at load | Frames compared in webkit/firefox on `--release`; all frames are composed so a shifted clock is harmless; recorded in DESIGN.md |

**Deliberately out of scope for v9:** weekly survey cadence; repo-header PNGs; a "Chart No. 1: Symbols" sheet (v9.1); PRs instead of direct commits; hatch density by source coverage and author rings; the A2 poster; paper dot grain beyond the 2 % fall-off; the 96 s compass swing; out-and-back sailing; heel or bob on anything but the footer hull; `textPath`, filters, `animateMotion`, `pattern` hatching; followers and stars on any sheet; per-repo sparkline *sheet*; a public SLI endpoint; pixel-perfect goldens; anything needing a logged-in GitHub session in CI; the sector light, governor gauge, speed-limit mark and WAL dedup cells; the contribution snake.

---

## 7. Acceptance

### 7.1 The acceptance test for "masterpiece" (T10 §4, verbatim)

**Floor (automated):** `check.py --ci` exit 0, or 2 with only position/expiry warnings; regression suite green; post-merge steps 1–4 clean.

**Judged** (two reviewers new to the page plus Ben; median; 0–3 each):

| # | Criterion | From |
|---|---|---|
| J1 | Thesis read in one line, said once | 24, STD |
| J2 | Cover the name: the hero picture alone argues the survey edge | 28 |
| J3 | Cover the titles: a stranger names every sheet by silhouette | 33, STD 6 |
| J4 | A hydrographer names region, unit and datum from the sheet | STD 4, 13, 26 |
| J5 | Point at any mark: one sentence says its job, and it reads on a phone | 33 |
| J6 | Change a number in stats.json → the chart visibly changes | 06, STD 2 |
| J7 | Honesty: both commit instruments, unit per sheet, no invented geometry or unsupported claim | 34, 19, 20 |
| J8 | Motion reads as the chart surveying itself; every still is finished | 05, 12 |
| J9 | Copy says each thing once; no borrowed jokes; glossed headings | 04, 24, 25, 29 |
| J10 | Recruiter finds field, systems, languages, contact in plain text within 60 s | 03, 18, 29 |
| J11 | Night is designed, not inverted: lights are the brightest things | 15, 27 |
| J12 | ≥ 4 uncaptioned second-look layers, each making the first reading truer | STD 13, 33 |

**Pass:** ≥ 30/36, no zero, J1/J2/J7/J10 each ≥ 2, **and** 29's five-second test on the shadow profile (3 cohorts × 10; 870 px day, repeated at 360 and night): ≥ 80 % name the field, ≥ 60 % recall the name, ≤ 10 % call him a Scrapy maintainer, ≥ 80 % read name and thesis at 360, glossed headings ≥ 1.5/2. The thesis A/B (plain vs "wrong about itself") runs in the same session and decides the hero line.

### 7.2 Still-frame gate

A sheet at any instant is a finished sheet. For each sheet, with still edition S and frames F(t) at the instants in §2.1: ink coverage `ink(F(t))/ink(S) ≥ 0.95` at every sampled time (hero only: ≥ 0.6 at t = 0, rising, ≥ 0.95 from 4.1 s); for t ≥ opening_end, changed-pixel fraction `|F(t) − S| ≤ 1.5 %`; no sampled frame has a text-free rectangle larger than 25 % of the sheet where S has text; a boat in every footer frame; header plus ≥ 10 entries in every log frame; every `*-still.svg` contains zero `<animate*>`/`<set>` and pixel-matches the animated edition at t = 95 s within 1.5 %. Silhouettes: frozen states at 128 px, pairwise L1 ≥ 0.25 on a 16×8 mass grid.

### 7.3 Perf gate (12's numbers, binding)

Frozen sheets (soundings, instruments, every still, every phone file but the hero) 0 repaints after warm-up; hero ≤ 1 repaint/s after 30 s; approaches ≤ 2/s after 44 s; log ≤ 2/s after 50 s; footer the only ambient loop at ≤ 4 ms/frame (raster + paint); nothing over 8 ms/frame while moving after its opening; hero-phone at 360 px DPR 3 ≤ 0.25 repaints/s after 6 s; no `animateMotion`, no animated geometry attribute outside a ≤ 4 s one-shot, no filter under an animated ancestor; every discrete instant on the 0.5 s grid; `check_motion` zero violations. Size: ≤ 300 KB raw / 100 KB gz per SVG (hero target 170/60, approaches 200/75, soundings 80/25, log 95/30, instruments 50/18, footer 40/12); phone ≤ 120 KB raw; one desktop edition set ≤ 250 KB gz; ≤ 3000 elements; two builds from one `stats.json` byte-identical.
