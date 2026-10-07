# T6 — Chart drawing engine (chartlib v9)

Scope: `scripts/chartlib.py` rewritten as the one drawing library every sheet calls. It owns the field, contours, tints, coastlines, hatching, placement, line weights, symbols, rose, source diagram, paper and the byte budget. It does not own type (T5), SMIL (T4), colour values (T1 tokens, from 15's OKLCH table) or data derivations (T7). Where a critic's number conflicts with a measured constraint, the measured constraint wins and the reason is given.

## 1. Decisions

1. **The soundings generate the field; there is no noise field.** `Field.from_soundings()` solves Gaussian-RBF weights so the field equals each weekly value at its position; the `0.18·sin·cos` wallpaper is deleted (per 08, 14; TECH-BRIEF "never two drawings of one noise field").
2. **Field units are the sheet's depth unit.** Hero: commits/week; land is depth 0; contour levels are chart intervals `[0, 5, 10, 20, 50]`, five lines, figures set in breaks of the line (per 13). Eleven evenly stepped lines were topography.
3. **Every feature is cut at the same level and its drawn area is asserted ±8 %.** Radius is Newton-solved against the polygon area at the 5-contour (the danger-line level, which every island and shoal has); the 0-contour coastline inside is tint-only geometry (per 08 §5). One comparable measure, no asserts in the cron job: failure logs to `build-report.json` and falls back (per 30).
4. **Contours are relative-integer polylines subsampled ×3; cubics survive only on coastlines and the course.** Measured on a hero-like field: 11 cubic levels 55 KB raw / 24 KB gz → polylines 10 / 3 KB → five chart levels without wallpaper 5 / 1 KB (per 14, 12). All sheet-space coordinates are integers; one decimal only inside symbol defs (per 12: −23 % gz, −16 % raster).
5. **Four line weights ≥1.6× apart: HAIR 0.6 · PEN 1.0 · LINE 1.6 · BRUSH 2.6.** PEN is 1.0, not 31's 1.1, so 0.6×1.6 = 0.96 holds; nothing semantic below 0.9 px, HAIR only for texture at opacity ≥ .25 (per 14, 11, 15). The weights are the same at night; night hierarchy is carried by lightness (`ink2` for lines), because a 0.85× width change below one rendered pixel is invisible at 68 % while lightness survives rasterisation (15 over 14).
6. **Tint bands are opaque result colours, deepest first, land last, then a LINE coastline in `ink2`.** Two bands: B (0–5, darker) over A (5–10, lighter); `Theme` gains `shallow_a`, `shallow_b`, `flare`, `light_white` (per 15, 02, 09). Shoals are tinted water inside a danger line, never land (per 02).
7. **No pattern fills for hatching; no filters anywhere.** Hatch is generated lines in a `clipPath` with seeded spacing/angle/end jitter (per 14, 11); plate-mark shadow is three stepped rects, not `feGaussianBlur`; halos are radial-gradient circles (per 12, 11). Varying per line and never along it: jitter records a ruler, wobble fakes a tremor (14).
8. **Hatch has tonal value**: PEN 1.0, opacity .40–.50, spacing 8 ± 12 % (unsurveyed) and 6 ± 12 % (foul), apparent ΔL ≈ .045 from its fill (15's numbers, 14's jitter).
9. **Nothing is in phase.** Every dashed path gets a seeded `stroke-dashoffset` and a gap from 4.0–4.6; day colour fills are misregistered (+0.6, +0.4) from their outlines; all jitter comes from one `Jitter(seed, name)` keyed by sheet and element, never by data, so identical inputs give byte-identical output (per 14, 06, 11).
10. **No interior graticule.** Two labelled meridians and parallels at the margin only (per 13); this also deletes 110 lines and 1.7 ms/frame (12). `graticule()` and `rhumb_lines()` are removed.
11. **One pen for every symbol, one pictorial object (the sloop).** All marks stroke PEN with round caps; lights are a star and a magenta flare, buoys are canted outlines with a position circle; the sloop is the 11-command detail drawing or the 7-command glyph chosen by rendered width (per 31, 15). The wreck is the reference drawing and is kept.
12. **Legend entries are `<use>` of the chart's own symbol ids**, ids prefixed per sheet, and the build diffs legend ids against sheet ids (per 30, 11).
13. **The rose keeps 00 at the top and points a variation arrow at the modal hour**; bars are lines with length ∝ value; no rotation of the dial (08 over spec-hero §4). Data arrives from T7 already in author-offset commit-days.
14. **Paper: square sheet, 14 px unprinted margin, plate mark; day gets seeded dot grain and a 2 % warm radial fall-off, night gets one radial wipe (retroussage) and no grain.** Opaque paper in both editions because the page colour is not ours (per 14, 15, 11).
15. **Size targets per sheet** are set below and gated; the whole page must stay under 11's 100 KB gz per sheet with the hero at ≤ 60 KB gz.

## 2. Design and implementation

### 2.1 Module layout
`chartlib/` becomes a package: `field.py` (Field, contours, compaction), `water.py` (tints, coastline, danger, hatch, vignette, unsurveyed), `place.py` (feature solver, soundings positions), `symbols.py` (library + ids), `furniture.py` (frame, rose, source diagram, paper, scale key), `tokens.py` is T1's and is imported, never duplicated. `chartlib.py` re-exports.

### 2.2 Field and contours

```python
@dataclass
class Field:
    w: int; h: int; gx: int = 160; gy: int = 92
    def value(self, x, y) -> float            # depth in sheet units, land < 0
    def grid(self) -> list[list[float]]       # cached; cleared on mutation
    @classmethod
    def from_soundings(cls, w, h, samples: list[tuple[float,float,float]],   # (x, y, value)
                       base: float, features: list["Feature"], coast: "Coast",
                       sigma: float = 110, ridge: float = 1e-3) -> "Field"
    @classmethod
    def synthetic(cls, w, h, seed, base, features, coast, n=6) -> "Field"   # illustrative sheets (T3)
```
`from_soundings` sets `depth(x,y) = clamp(base − Σ_i feature_i(x,y), …) + Σ_k w_k·G_k(x,y)` and solves the k×k system so `depth(x_k,y_k) = value_k` exactly (zero weeks are solved to 0.5 so no spurious coastline appears; the numeral still prints 0). `Coast(rect, inset=24, unsurveyed_x=(1080,1150))` is the falloff: a smoothstep that drives depth to `base` within 24 px of the drawable rect and across the unsurveyed boundary, so every tint polygon closes and no ring is cut by the neat line (14 §5; replaces the spec's prose). Ridge regularisation keeps the system conditioned when two weekly points fall within 20 px.

```python
def contours(field, levels, clip=None) -> list[Contour]      # Contour(level, pts, closed, length)
def compact_path(pts, closed, every=3) -> str                # "M x y l dx dy … Z", integers, h/v where one delta is 0
def smooth_path(pts, closed, every=2) -> str                 # cubic, integer coords; coast + course only
def contour_labels(cs, role="contour-figure", min_len=160) -> list[tuple[Contour, int, int]]  # (contour, i0, i1) break indices
def draw_contours(cs, index_levels, approx_clip=None) -> str
```
`draw_contours` emits intermediate levels at PEN .55 `ink2` and index levels (10, 50) at LINE .55; a labelled contour becomes two polylines around a gap of `width + 6`, the figure set by T5's `k.label(role="contour-figure", rotate=tangent)` at the lowest-curvature point whose tangent is within 30° of horizontal. Contours inside `approx_clip` (x 1080–1150 on the hero) are redrawn with `DASH["APPROX"]`.

### 2.3 Water

```python
def tint_bands(cs, theme) -> str        # A = closed 10-polys in shallow_a, then B = closed 5-polys in shallow_b, then land (0) in land
def coastline(cs, theme, swell=True) -> str   # LINE ink2 on 0-polys; swell = second PEN pass offset (+0.4,+0.4) at .35 (14 F1)
def danger_lines(cs, level, theme, jit) -> str  # LINE round caps, dash "0.1 g" with g ~ U(4.0,4.6), seeded dashoffset
def hatch(polygon_or_rect, theme, jit, kind="unsurveyed"|"foul", clip_id=...) -> tuple[defs, body]
def coast_vignette(poly, theme, jit, step=6) -> str   # 3 HAIR ticks per sample along the outward normal, 5/3.5/2 px, .5/.35/.25
def unsurveyed_band(x, y, w, h, theme, jit, label_cb) -> tuple[defs, body]   # hatch + fade clip, label via T5 callback
def approximate_fringe(cs, clip_rect) -> str
```
Hatch: lines at −45° ± 1.5°, spacing `s·(1 ± 0.12)`, ends over/undershooting the band ±2 px, opacity `U(.40,.50)`, PEN, inside a `clipPath` of the band polygon; a 130×430 band at spacing 8 is ≈ 70 lines, ≈ 6 KB. Coast vignette goes on named islands only (≤ 6, ≈ 2–3 KB each); islets get the coastline alone. Its faintest tick is .25, not 14's .15, to honour the opacity floor.

### 2.4 Features and placement

```python
@dataclass
class Feature:
    name: str; value: float; kind: str      # island | shoal | islet | harbour | wreck
    x: int = 0; y: int = 0; r: float = 0; amp: float = 0
    area: float = 0; axis: tuple[float,float,int,int] = ()   # (angle°, length, cx, cy) for T5's text-on-path
def place_features(features, drawable, exclusions, course_pts, seed, slots: dict[str,(int,int)], cap=32) -> PlaceReport
def solve_radii(field_builder, features, k_area: float, tol=0.08, iters=4) -> None
def feature_polygons(cs, features) -> dict[str, list[pts]]
def spot_heights(features, cs, clearance=8) -> list[tuple[Feature, int, int, int]]   # (f, x, y, angle) outside its 5-poly
def soundings_along(course_pts, values, spacing=40, lean=2.5) -> list[tuple[int,int,float,float]]   # (x, y, value, lean°)
```
`solve_radii` runs Newton on each feature's `r` (largest first) with `area(r)` = polygon area of its 5-contour and target `k_area·value` (T2 sets `k_area` so the largest feature fits its slot; `area_key` prints 10/100/500 from the same k). Shoals get `amp` for a minimum depth ≈ 2 (tinted, ringed, never land); islands and the harbour drive depth below 0. The field is rebuilt from soundings after the solve so every numeral stays exact. Placement is Halton (seed 2709) with reserve slots; a feature unplaced after 400 candidates joins the "and N islets" count and is reported, never asserted. From 30: `cap=32`, `r ∈ [6, 90]`, names > 18 characters abbreviated by the caller.

### 2.5 Line weights, dashes, ink levels

```python
W = {"HAIR": 0.6, "PEN": 1.0, "LINE": 1.6, "BRUSH": 2.6}
DASH = {"DANGER": "0.1 {g}", "COURSE": "0.1 7", "TRACK": "1 4", "LIMIT": "1.5 4", "APPROX": "3 3", "SECTOR": "2 3"}
def stroke(width_key, color, opacity=None, dash_key=None, jit=None, caps="round") -> str   # the only way to emit stroke attrs
```
Assignments: graticule margin ticks, track and check lines, sector radii, vignette, grain = HAIR (≥ .25); intermediate contours, every symbol stroke, course pecks, waypoint, mast, tiller, hatch = PEN; index contours, coastline, danger dots, neat-line outer rule, tide curve = LINE; serpent head hump, variation arrow, fall lip = BRUSH. The serpent tapers head-first through the weights (BRUSH → LINE → PEN); that is the taper 31 asked for with no extra token. Restricted-area limit is `restricted_line(pts)`: a LIMIT dash with 3 px T-ticks every 12 px on the protected side, generated, not a pattern. The build fails on any `stroke-width` not in `W` (round-trip through `stroke()` only).

### 2.6 Symbol library

```python
def symbol_defs(theme, prefix: str, edition: str) -> str   # <defs> for every symbol below, ids f"{prefix}-sym-{name}"
def use(name, x, y, prefix, scale=1.0, rotate=0, extra="") -> str
# names: sloop, sloop-glyph, can, nun, light, flare, traffic, horn, anchorage, wreck, waypoint, station, fix,
#        ldg, halo (radial gradient circle), correction
def sloop(theme, detail: bool) -> str      # 31's 11-command hull/main/jib/mast/tiller or 7-command glyph; origin waterline centre, bow right
def lateral(kind: "can"|"nun", number, theme, misreg=True) -> str  # outline PEN, IALA fill .85, body rotate(8) about base, position circle r1.2
def light(theme) -> str                    # 5-point star r4 PEN + flare "M0,0 q-3,-9 0,-14 q3,5 0,14" rotated 45° in `flare` .8
def traffic_signal(theme) -> str           # port traffic signal: mast + three stacked lamps; the top lamp carries id -lit
def horn() -> str                          # fog signal: three HAIR arcs radiating from the light
def sector_light(cx, cy, r, from_deg, to_deg, theme, lit=False) -> str   # radii HAIR, arc SECTOR dash; filled only when lit
def wreck(theme) / anchorage(theme) / waypoint() / station() / fix() / ldg_triangles()
def doubt(kind: "ED"|"Rep"|"SD"|"PA", x, y) -> str   # via T5 role "abbr", italic, the chart's doubt marks (per 26)
def correction(x, y, old: str, new: str, theme) -> str  # 1.1 px diagonal strike through old, new in flare italic (14 idea 1; T7 supplies the pair)
def track_lines(x0, y0, x1, y1, n, spacing, theme) -> tuple[str, list[seg]]
def check_lines(track_segs, n, theme) -> str
def course(points, theme, jit, pecked=True) -> str          # COURSE dash, waypoints as <use>, bearings via T5 role "bearing"
def course_samples(points, n=96) -> list[tuple[int,int,float]]   # (x, y, heading°) for T4's animateTransform values
def serpent(theme) -> str                 # three humps growing toward a head facing +x, one eye r1.3, no mouth; weights BRUSH/LINE/PEN
```
Every lit symbol contains one child with `id="{prefix}-{name}-lit"` whose `opacity` T4 animates with `calcMode="discrete"`; the halo is a static radial-gradient circle in `flare`/`accent`/`ok` whose opacity T4 animates the same way (no filter). Day misregistration offsets colour fills by (+0.6, +0.4); night sets `misreg=False`. Symbols are drawn once in `<defs>` and placed with `<use>`; legend cells call the same `use()`.

### 2.7 Furniture

```python
def frame(w, h, theme, kind="minute-bars"|"double"|"none"|"broken", gaps: list[(side, y0, y1)] = ()) -> str
def margin_graticule(rect, meridians: list[(x,label)], parallels: list[(y,label)], theme) -> str
def two_ring_rose(cx, cy, r, theme, hours24: list[float], modal: int, var_label_cb) -> str   # 00 top; numerals 00/06/12/18; bars HAIR..LINE; BRUSH arrow to modal
def source_diagram(x, y, w, h, zones: list[Zone], theme, jit) -> str   # Zone(letter, poly, density) — hatch density encodes coverage (08 idea 3)
def area_key(x, y, k_area, values=(10,100,500), theme) -> str   # replaces the URL scale bar (08)
def paper(w, h, theme, edition, jit) -> tuple[defs, body]   # square, 14 px margin, plate mark (1 px .16 + two stepped inner rects .08/.04), day grain pattern 96×96 ~50 dots r .6–1.2 at .06 + 2 % radial fall-off; night radial wipe #2A3B5A→paper .18→0
def plate_mark(w, h, theme) -> str
```
`frame(kind="broken", gaps=[("right",150,580)])` is how the hero band and the footer water leave the sheet; the log passes `kind="none"` so the system sees the break (30 F5).

### 2.8 Size and element targets (gated by T10)

| Sheet | raw ≤ | gz ≤ | elements ≤ | paths ≤ | notes |
|---|---|---|---|---|---|
| hero 1280×740 | 170 KB | 60 KB | 2 400 | 320 | contours ≈ 10 KB, hatch 6, vignette 15, paper 3, symbols defs 4 |
| approaches 1280×880 | 190 KB | 70 KB | 2 800 | 360 | two hatch regions, 16 tracks, inset |
| soundings 1280×240 | 55 KB | 18 KB | 700 | 60 | |
| log 1280×440 | 95 KB | 30 KB | 1 400 | 40 | glyph uses dominate |
| instruments 1280×230 | 45 KB | 16 KB | 500 | 40 | |
| footer 1280×270 | 40 KB | 12 KB | 450 | 60 | the one ambient loop |
| phone editions | ≤ 60 % of desktop | | | | culled by the caller, same functions |

## Interfaces

**Provided**
- To **T2 / T3** (sheets): everything in §2.2–2.7. The calling order is `paper → Field → solve_radii → contours → tint_bands → coastline → vignette → danger_lines → hatch/unsurveyed → draw_contours → contour_labels → symbols/course → frame → furniture`. Each function returns svg text; `defs` tuples are collected by the caller.
- To **T4** (motion): `course_samples(points, n)` → `(x, y, heading)` lists for `animateTransform` values; `id="{prefix}-{name}-lit"` on every light's lit child and halo; `sloop(detail)` with origin at the waterline so `rotate(-4)` is bow-up; `Contour.length` and `compact_path` output carry `pathLength="1"`-ready geometry for the hero opening (T4 adds the attribute).
- To **T9** (supporting sheets): `sloop`, `serpent`, `hatch`, `frame(kind="broken")`, `frame(kind="none")`, `stroke()`, `DASH["LIMIT"]`, `paper(edition)`, `track_lines` for the instruments glyph, the tide curve's `LINE` weight; `monotone_path(pts)` (monotone cubic, baseline zero; 08) is added to `field.py` for the tide curve.
- To **T10** (QA): `PlaceReport` and `FieldReport` dataclasses (areas, ratios, dropped features, closed-polygon check, bracket test results, element and byte counts) written to `assets/build-report.json`.
- To **T8**: `symbol_defs` is also the source of "Chart No. 1: Symbols" if T8/T9 choose to render it.

**Needed**
- From **T1**: `tokens.Theme` with `paper, land, ink, ink2, muted, shallow_a, shallow_b, accent (nun red), ok (can green), flare, light_white, hair`, day and night values from 15's OKLCH table; the per-sheet `prefix`; the `Jitter(seed, name)` seed registry (I will write `Jitter` if T1 prefers it here).
- From **T5**: `k.label(role, s, x, y, anchor="start", rotate=0, lean=0) -> (svg, width)` for roles `contour-figure`, `sounding`, `spot-height`, `bearing`, `abbr`, `place-water`, `place-land`; a text-on-path call that takes `Feature.axis`.
- From **T7**: `weeks` as `[(start, n)]` with the 34 most recent for the hero, repo `commits` by author filter, `hours24` as commit-days in author offset, `modal_hour`, and for `correction()` the previous build's values where changed.
- From **T4**: the agreed `begin` ids; T6 emits no `<animate>`.
- From **T10**: the gate thresholds above, the CVD/ΔE check on `shallow_a/b` vs `land`, the hatch ΔL ≥ .04 check.

## 4. Build order, effort, risks, omissions

1. `tokens` import, `W`/`DASH`/`stroke()`, `Jitter`, `compact_path`, integer coordinates — 3 h.
2. `Field.from_soundings` + `Coast` + chart-interval `contours` + labels in breaks — 6 h.
3. `tint_bands`, `coastline` with swell, `danger_lines`, `hatch`, `coast_vignette`, `unsurveyed_band`, `approximate_fringe` — 5 h.
4. `place_features`, `solve_radii`, `spot_heights`, `soundings_along`, reports — 5 h.
5. Symbol library with ids and `use()`, sloop ×2, marks, lights, traffic, horn, sector, doubt, correction, serpent, course + samples — 8 h.
6. Furniture: frame kinds, margin graticule, rose, source diagram, area key, paper — 4 h.
7. Golden fixture (today's stats) and stress fixture (40 repos, 9 999 commits, 30-character names) — 4 h.
Total ≈ 35 h.

Risks: the RBF system goes ill-conditioned when weekly points cluster (ridge term, fallback sigma 140, reported); area Newton can oscillate where features overlap (largest first, four iterations, report if outside ±8 %); a contour-break spot can land under a symbol (caller passes exclusions; second-best spot); grain at .06 is sub-JND by design and may read as nothing on some panels (accepted; the radial fall-off carries the surface). Deliberately left out: `feTurbulence`, `feGaussianBlur`, `<pattern>` hatching, `animateMotion`, interior graticule, rhumb lines, the pictorial lighthouse (an inset tower is T3's call), three-band tints, the URL scale bar.

## 5. Acceptance criteria

1. `grep -c 'stroke-width' *.svg` values ∈ {0.6, 1.0, 1.6, 2.6} only; no HAIR stroke with opacity < .25; no semantic stroke under 0.9 px at 1280.
2. Every open-water numeral is bracketed by its two nearest contour levels (`FieldReport.bracket_failures == 0`).
3. For every feature, `|area_5 / (k_area·value) − 1| ≤ 0.08`; all 0/5/10 polygons closed; no feature dropped on the golden fixture; stress fixture builds without error.
4. Hero contour bytes ≤ 15 KB raw; hero ≤ 170 KB raw / 60 KB gz; all sheets within the table; no `<pattern>` except the 96×96 grain; no `filter` attribute anywhere; no `animateMotion`.
5. Every legend `<use href>` resolves to an id present on the sheet, and every symbol id placed on a sheet appears in its legend (set equality, per 30).
6. Two builds from identical `stats.json` are byte-identical; dash offsets, hatch lines and grain differ between any two paths/sheets (no two equal `stroke-dashoffset` values on one sheet).
7. T10's colour run: `shallow_a`, `shallow_b`, `land` pairwise ΔE_ok ≥ .06 under normal, deutan and protan; hatch vs fill ΔL ≥ .04; at night the max L of any `-lit` child exceeds the max L of any text.
8. A 360 px render at DPR 3 shows the coastline, at least one danger line, one light star and the unsurveyed hatch as distinct marks.
