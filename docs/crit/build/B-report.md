# Builder B report — T6 chart drawing engine (`scripts/chartlib/`)

## What I built

- Renamed `scripts/chartlib.py` → `scripts/chartlib_v8.py`; `scripts/sheets/_v8_reference.py` now imports `chartlib_v8 as c` (still imports clean).
- New package `scripts/chartlib/` — `__init__.py` (re-exports + `LETTERING`), `field.py`, `water.py`, `place.py`, `symbols.py`, `furniture.py`. Stdlib only; imports `tokens` (never edits it); never imports `typeset`/`svgkit`; emits no `<animate*>`, no `<pattern>`, no `filter`.
- `tests/test_chartlib.py` — 22 tests; whole suite `python3 -m unittest discover -s tests -v` = 127 OK (includes A/D/E's tests).
- Visual self-check: `scratchpad/crit/build/B-selfcheck.{svg,png}` (+ `-night`), produced by `B-selfcheck.py` (uses plain `<text>` for lettering; not build code). Hero-like sheet: 4 features solved to area, 52 soundings on the course, tints, coastline + swell, vignette, danger line, unsurveyed band with ramp, contours with figures in breaks and APPROX fringe, course + bearings, sloop at 1×/2× and glyph, light + horn, can/nun with lit cores (halos at night), wreck, Rep/ED, serpent, rose with the real `hours[24]` (v2 stats, modal 14h), source diagram, area key, restricted line, track/check lines, traffic/ldg/fix/waypoint, correction, broken frame, margin graticule. **52 KB raw / 11 KB gz, 247 elements, stroke widths ∈ {0.6, 1.0, 1.6, 2.6} only, every coordinate integer or one decimal.** Contours alone ≈ 8 KB.

## Model (reconciling T6's spec with MASTERPLAN 15/16)

Depth = count. `depth(x,y) = base + f(x,y)·(water − land_lift − clamp(shoal_lift) − base)` where
`water = max(base + Σₖ aₖ·W(|p−pₖ|/h_snd), 0.5)` (soundings; zero weeks solve to 0.5, no spurious coastline),
feature lift `A·W(d/h)` with `h = ratio·r` and **A solved so depth = 5 exactly at distance r** (so `solve_radii`'s target is the drawn 5-polygon), `clamp` keeps a shoal alone at depth ≥ 2 (a flat bank; shoals never break the surface), islands/harbour go below 0, `f` is the `Coast` smoothstep falloff (24 px inside the drawable rect, 1→0 across `unsurveyed_x`), so every polygon closes.
Sounding amplitudes: dense `(W + ridge·I)` LU with partial pivoting, then iterative refinement against `W` itself — well-conditioned systems reproduce samples to ~1e-9, clustered points stay damped (`FieldReport.refine_steps`, `ridge_used`).
Grid: `cell=8` px (161×93 on the hero), evaluated kernel-wise over bounding boxes (0.01–0.05 s). `contours(field, levels, clip=rect)` reuses the global grid's nodes inside `clip`, so what `solve_radii` measures is what is drawn.
Marching squares segments are **oriented** (shallow on the left), so every closed `Contour` carries `shallow_inside`; tint fills are one `<path fill-rule="evenodd">` per level with nested deep holes (lagoons, the harbour basin) handled.

## Public API (exact signatures)

```python
# field.py
class Coast(rect, inset=24.0, unsurveyed_x=(1080, 1150)); .factor(x, y) -> float
class Kernel(x, y, h, amp, kind)                      # kind: "water" | "land" | "shoal"
class FieldReport(n_samples, residual_max, faded[], on_feature[], clamped[], ridge_used, refine_steps, bracket_failures[], unclosed[], grid)
class Field(w, h, base=20.0, cell=8.0, coast=None, kernels=[], floor=0.5, shoal_floor=2.0, report)
    @classmethod from_soundings(w, h, samples, base, features=(), coast=None, kernel="bump", h_snd=30.0, ridge=1e-3,
                                extra=(), level=5.0, cell=8.0, refine=4) -> Field     # extra: [(x, y, h, amp)] land kernels, amp<0 deepens
    @classmethod synthetic(w, h, seed, base, features=(), coast=None, n=6, spread=0.5, cell=8.0) -> Field
    value(x, y) -> float; grid() -> list[list[float]]; invalidate(); axes() -> (xs, ys); local_grid(rect) -> (xs, ys, rows)
def feature_kernel(ft, base, level=5.0) -> Kernel | None        # sets ft.h, ft.amp
KERNEL_RATIO = {"island": 1.82, "harbour": 1.82, "islet": 1.82, "shoal": 1.82, "wreck": 0.0}; DEFAULT_LEVELS = (0, 5, 10, 20, 50)
def bump(q); def fmt(v) -> str; def smoothstep(t)
def lu_solve(A, b) -> list; def solve_ridge(M, d, ridge=1e-3, refine=3) -> (a, steps)
class Contour(level, pts, closed, length, shallow_inside=None); .area(); .centroid(); .contains(x, y)
def contours(field, levels, clip=None) -> list[Contour]
def closed_check(cs, levels=None, min_len=30.0) -> [(level, length)]
def band_of(cs, x, y, levels, base=None) -> float | None
def bracket_test(cs, samples, levels=DEFAULT_LEVELS, base=None, tie=0.02, skip=(), field=None) -> [(i, x, y, v, expected, found, cause)]
def compact_path(pts, closed, every=3) -> str;  def parse_path(d) -> [(x, y)]
def smooth_path(pts, closed, every=2) -> str;   def monotone_path(pts, baseline=None) -> str
def clip_polyline(pts, rect, closed=False) -> (inside_parts, outside_parts)
def contour_labels(cs, role="contour-figure", min_len=160.0, gap=20.0, exclusions=(), max_tilt=30.0, levels=None, skip_levels=(0.0,)) -> [(Contour, i0, i1)]
def break_anchor(c, i0, i1) -> (x, y, angle°);  def broken_polylines(c, i0, i1) -> [pts]
def draw_contours(cs, index_levels, theme, approx_clip=None, breaks=(), opacity=0.55, every=3, skip_levels=(0.0,), min_len=0.0) -> str
def polygon_area(pts) (signed); polygon_centroid(pts); point_in_polygon(x, y, pts); polyline_length(pts, closed=False)

# water.py
def tint_bands(cs, theme, levels=(10.0, 5.0), land_level=0.0, every=3) -> str
def level_polygons(cs, level) -> [pts]
def coastline(cs, theme, swell=True, level=0.0, every=2) -> str
def danger_lines(cs, level, theme, jit, inside=None, every=3, opacity=0.9) -> str       # inside=[(x,y)] → only polygons containing a point
def hatch(poly_or_rect, theme, jit, kind="unsurveyed"|"foul", clip_id="hatch", ramp=None, spacing=None, angle=None, color=None) -> (defs, body)
def coast_vignette(poly, theme, jit, step=6.0, lengths=(5, 3.5, 2), opacities=(.5, .35, .25), gaps=(1.5, 2, 2)) -> str
def unsurveyed_band(x, y, w, h, theme, jit, label_cb=None, ramp_w=40.0, label="UNSURVEYED", limit_label=None, clip_id="unsurv", label_at=None, limit_at=None) -> (defs, body)
def approximate_fringe(cs, clip_rect, theme, every=3, opacity=0.55, skip_levels=(0.0,)) -> str

# place.py
@dataclass Feature(name, value, kind, x=0, y=0, r=0.0, amp=0.0, area=0.0, axis=(), alias="", sub=None, ratio=None, h=0.0, placed=False, slot=None, target=0.0)
@dataclass PlaceReport(placed[], dropped[], beyond_cap[], slot_conflicts[], candidates_tried, min_pair_clearance, min_course_clearance); .islets_more
@dataclass RadiusReport(name, value, target, area, r, ratio, ok, iters, clamped)
def kind_of(r, active, alias="", archived=False) -> str
def place_features(features, drawable, exclusions, course_pts, seed, slots, cap=32, clear_edge=28, clear_pair=44, clear_course=30, islet_min_x=600, tries=400) -> PlaceReport
def solve_radii(field_builder, features, k_area, tol=0.08, iters=4, level=5.0, r_bounds=(6.0, 90.0)) -> list[RadiusReport]
def feature_polygons(cs, features, level=5.0) -> {name: pts}
def spot_heights(features, cs, clearance=8, level=5.0) -> [(Feature, x, y, angle)]
def soundings_along(course_pts, values, rows=(-48, -24, 24, 48)) -> [(x, y, value)]      # ints
def soundings_lean(course_pts, pts, max_lean=2.5) -> [lean°]
def halton(i, base); def dist_to_polyline(x, y, pts)

# symbols.py  (ids f"{prefix}-sym-{name}"; lit children f"{prefix}-{name}-lit")
SYMBOL_NAMES = ("sloop","sloop-glyph","can","nun","light","flare","traffic","horn","anchorage","wreck","waypoint","station","fix","ldg","halo","correction","rep","ed")
def symbol_defs(theme, prefix, edition) -> str        # the CONTENT for the caller's <defs>; includes the halo radialGradient f"{prefix}-halo-g"
def symbol_ids(prefix) -> [str]
def use(name, x, y, prefix, scale=1.0, rotate=0, extra="") -> str      # SVG2 `href`
def sloop(theme, detail=True, rig=True) -> str;  SLOOP_DETAIL, SLOOP_GLYPH (31's exact paths)
def lateral(kind: "can"|"nun", number=None, theme=None, misreg=True) -> str
def light(theme, prefix="sym", core_r=1.5) -> str;  def flare(theme, opacity=0.8) -> str
def halo(theme, prefix="sym", r=14, color=None) -> (gradient_def, circle)
def lit_core(x, y, theme, lit_id, r=1.5, halo_r=None, prefix="sym", color=None) -> str   # per-instance lit id (+ "-halo")
def traffic_signal(theme, prefix="sym"); def horn(theme); def anchorage(theme); def wreck(theme); def waypoint(theme)
def station(theme); def fix(theme); def ldg_triangle(theme); def rep_ring(theme); def ed_islet(theme); def correction_mark(theme)
def correction(x, y, old, new, theme, label_cb, old_w=None, size=11) -> str
def doubt(kind: "ED"|"Rep"|"SD"|"PA", x, y, label_cb=None, prefix=None, theme=None) -> str
def serpent(theme) -> str          # <g class="serpent"> with .hump-1 (PEN) .hump-2 (LINE) .head (BRUSH) .eye

# furniture.py
class Jitter(seed, name); .uniform(a,b) .gauss(mu,s) .choice(seq) .offset(limit) .phase(period) .sub(name) -> Jitter
def stroke(width_key, color, opacity=None, dash_key=None, jit=None, caps="round", gap=None) -> str   # the only stroke emitter; KeyError off W/DASH
def op(v) -> str                   # ".55"
def frame(w, h, theme, kind="minute-bars"|"double"|"none"|"broken", gaps=(), rules=(18, 24), bar=20) -> str
def margin_graticule(rect, meridians, parallels, theme, label_cb=None, tick=6) -> str
def two_ring_rose(cx, cy, r, theme, hours24, modal, var_label_cb=None, label_cb=None) -> str   # var_label_cb(x, y) -> str
@dataclass Zone(letter, poly[fractions], density=0.5)
def source_diagram(x, y, w, h, zones, theme, jit, label_cb=None) -> str
def area_key(x, y, k_area, values=(10, 100, 500), theme=None, label_cb=None, gap=14) -> str
def paper(w, h, theme, edition, jit, prefix="paper", margin=14, grain=None) -> (defs, body);  def plate_mark(w, h, theme, margin=14) -> str
def course(points, theme, jit, pecked=True, label_cb=None, prefix=None, bearings=True, sides=None, offset=12.0) -> str
def course_samples(points, n=96, per_seg=24) -> [(x, y, heading°)]      # one decimal; heading = true bearing of travel
def compass_bearing(p, q) -> float;  def catmull_rom(points, per_seg=16, closed=False);  def polyline_at(pts, s) -> ((x,y),(tx,ty))
def lateral_offset(leg, s, side: "starboard"|"port"|"right"|"left", d) -> (x, y)
def track_lines(x0, y0, x1, y1, n, spacing, theme, opacity=0.55) -> (svg, segs);  def check_lines(segs, n, theme, opacity=0.35) -> str
def restricted_line(pts, theme, closed=True, inside=True, tick=3.0, every=12.0) -> str
def hatch_lines(poly, spacing, angle, jit, overshoot=2.0, angle_jitter=1.5, spacing_jitter=0.12); def hatch_paths(lines, attrs_for, buckets)

# __init__.py
LETTERING: {class: (T5 role, "upright"|"italic")}  — island-name, shoal-name, sea-name, harbour-name, spot-height, sounding,
  sounding-illustrative, contour-figure, bearing, mark-label, light-label, doubt, wreck-label, fix-label, note, caption,
  unit-line, var-label, rose-numeral, zone-letter, legend, correction-old, correction-new, area-key  (all roles exist in tokens.ROLES["desk"])
```

`label_cb` contract everywhere: `label_cb(text, x, y, role, anchor="start"|"middle"|"end", rotate=0, fill=None) -> str`; coordinates I hand over are already rounded to one decimal.

## What I need from others

- **D (T5 / typeset):** a `label_cb` with the kwargs above (anchor, rotate, fill); a width measure (`text_width(s, role)`) so sheets can pass `gap=width+6` to `contour_labels` and `old_w` to `correction`; text-on-path taking `Feature.axis = (angle°, length, cx, cy)`.
- **A (T1 / edition):** the per-sheet `prefix`; `svg(ed, w, h, body, defs, sheet)` must take my `defs` content (I return gradient/clipPath/symbol content, no `<defs>` wrapper) and must not re-prefix ids that already start with the sheet prefix. No change to `tokens.py` is needed; one proposal: nothing. (I use `DASH["DANGER"]` with explicit `gap` 2.6–3.4 for the three dotted *symbol* rings — wreck, Rep, ED — inside defs; everything on the sheet proper uses g ∈ U(4.0, 4.6).)
- **E (T4 / timeline):** a `<use>` of `{prefix}-sym-light` shares one `-lit` child across all instances, so G and R lights cannot have different `begin`s through the def. Use **`lit_core(x, y, theme, lit_id, halo_r=14 at night)`** per mark for the flashing core (+ `lit_id-halo`) and keep the star/flare as the `<use>`. `course_samples(points, 64)` gives `(x, y, heading)`; for the hero the boat is `scale(-1,1) rotate(-4)` (bow-left, bow-up) and heading is informational. `serpent()` parts carry classes `hump-1/hump-2/head/eye` for the +0.25/+0.5 s stagger.
- **T2 (hero):** build order `paper → Field.from_soundings(..., extra=basin kernels) → solve_radii(builder, feats, k_area) → F = builder(feats) → contours(F, DEFAULT_LEVELS) → tint_bands → coastline → coast_vignette(level_polygons(cs, 0)) → danger_lines(cs, 5, theme, jit, inside=shoal centres) → unsurveyed_band → draw_contours(cs, (10, 50), theme, approx_clip=(1040,24,110,692), breaks, min_len≈40) → break_anchor + label_cb → spot_heights → course`. Pass `base` to `bracket_test` and `skip` the x ≥ 1080 soundings; a `cause == "unresolved"` failure is a lone sounding far from base whose 5-ring is smaller than the 8 px grid — nudge it 4 px (your rule) or accept (its band is correct in the field). **Avoid `base` exactly on a contour level** (median clamped to [10, 50] can land on 10/20/50 — nudge by 0.5). Harbour basin kernels go in `extra` as `(x, y, 24, −amp)` in depth units (amp ≈ 1.5·base). Weeks `n` of 0 print 0 and solve to 0.5.
- **T3 (approaches):** land mass = `Feature(kind="island", ratio=…)`/`extra` kernels or an open coast via `extra`; `Zone.poly` in panel fractions, convex; `restricted_line` uses `DASH["RESTRICT"]` + teeth (your `DASH_RESTRICT`); concave `hatch` regions fall back to a `clipPath` named `clip_id`.
- **C (T7):** nothing more — v2 `hours[24]`, `variation.hour` and `weeks[].n` are what the rose and soundings read (self-check already uses the v2 file).
- **T10:** `FieldReport`, `PlaceReport`, `RadiusReport` are plain dataclasses (`dataclasses.asdict`) for `build-report.json`.

## Deviations from T6 / MASTERPLAN §3.2 (and why)

1. **Island kernel ratio default 1.82 r (not 1.33)** — within Decision 16's range. In the depth frame the amplitude is solved from the 5-ring, so the ratio only sets shelf width; at 1.33 the 0/5/10 contours of an island fall within 4 % of r and read as a cliff (seen in the first self-check). `Feature.ratio` overrides per feature.
2. **Shoal plateau clamp**: a shoal alone never goes shallower than 2 (T6 "minimum depth ≈ 2") — implemented as a clamp on the shoal lift, so a sounding < 2 inside a shoal's support is held at 2 and reported in `FieldReport.clamped` rather than reproduced (prints its numeral, same < 5 band).
3. **Ridge**: `(W + ridge·I)` factorisation plus refinement against `W` — exact for well-conditioned systems (the "reproduces samples" test holds at 1e-6 with ridge 1e-3), damped for clusters.
4. `draw_contours` and `approximate_fringe` take `theme` (colour is needed); `draw_contours` groups all paths of a weight class into one `<path>` (few elements) and gains `min_len`.
5. `contour_labels` skips level 0 by default and takes `levels=`; returns 3-tuples as specified, with `break_anchor()` for the figure's `(x, y, angle)`.
6. `hatch`: convex regions are clipped **geometrically** (so the ±2 px end jitter is visible) and need no `clipPath`; only concave polygons use the `clipPath`. Lines are bucketed into four opacity groups → ≤ 4 `<path>` elements per region. The band's fade is one `userSpaceOnUse` linearGradient stroke (`ramp=`), not a mask.
7. `danger_lines(..., inside=)` extension so the hero rings shoals but not islands.
8. `solve_radii` returns `list[RadiusReport]` (spec: None) — compatible with callers that ignore it; converges in 1–4 iterations on the self-check (ratios 0.93–1.03).
9. `soundings_along` returns `(x, y, value)` (MASTERPLAN) — the lean is `soundings_lean()`.
10. `spot_heights`: inside the feature above its name when r ≥ 16 (T2), else outside its 5-polygon to the east (T6).
11. `symbol_defs` returns defs **content**; symbols are `<g id>` not `<symbol>`; `use()` emits SVG2 `href`. Added symbols `rep`, `ed` (T3's doubt marks); `sector_light` not written (MASTERPLAN §6 out of scope). `lateral()`'s `number` is accepted but not drawn (lettering is the callback's).
12. The sloop glyph as given by 31 is 10 drawing commands (+3 Z), not 7; I kept his exact paths and the test bounds both drawings at ≤ 12 commands excluding Z (detail = 11 exactly).
13. `paper()` grain is one `<path>` of ~225 sub-pixel squares at .06 (no `<pattern>`, no extra stroke widths); day fall-off and night wipe are radialGradients; plate mark is three stepped PEN rects.
14. `two_ring_rose` numerals sit between the rings (ri = r − 24, numerals at ri + 10; 30° ticks 9 px) so they clear the ticks; bars are LINE strokes, the variation arrow BRUSH.
15. `Jitter` seeds `random.Random(f"{seed}:{name}")` (sha512 string seeding; byte-identical across processes — tested).
16. `frame()` takes `rules=(18, 24)` (hero) / `(14, 19)` (T3) and emits two rule paths + one bar path.

## Known limits / notes

- Grid cell 8 px: features r ≥ 6 solve within ±8 % (islet r 9.8 → 0.93 after 4 iterations); rings of lone soundings far from base (< ~5 px) are not resolved — reported, not drawn (`min_len`).
- `Field.synthetic` uses `halton` + `Jitter` for T3's illustrative water.
- Not implemented: `plate_mark` inner blur (by design), `sector_light`, T2's `hand_hatch`/`border(gap=)` names (use `hatch`/`frame(kind="broken", gaps=)`).
