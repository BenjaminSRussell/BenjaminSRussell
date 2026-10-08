# T4 — Motion engine

Owner: motion. Inputs: 05, 12 (binding measurements), 31, 26, 16, 25, 09, 10, 11, 30, 36; spec-hero §8–9, spec-approaches §5, spec-supporting motion blocks; `scripts/svgkit.py` (`anim`, `set_at`, `draw_in`, `appear`, `flash`, `EASE`, `LOOP`), `chartlib.course/out_and_back`, `scratchpad/perf/harness.js`.

## 1. Decisions

1. **05's three principles plus one from 12:** motion is survey work; nothing loops that could freeze; rhythm is nautical; *one continuous thing at a time on the page* (hero 0–28 s, then approaches 28–52 s; per 12 fact 1).
2. **`animateMotion` is deleted from the codebase.** `chartlib.course()` and `out_and_back()` are replaced by `Timeline.sail()`: `animateTransform type="translate"` with `values` sampled from the path by arc length and `keyTimes` warped by the easing. Identical on screen at 68 %, change-only invalidation while holding (per 12 facts 3–4, 11).
3. **No `rotate="auto"`, no heel/rock loops anywhere.** A profile boat on a plan chart does not rotate; direction is a mirror (`scale(-1,1)`) applied once per reversal inside a 1.2 s tack with luffing sails (per 31, 26). Under way: fixed `rotate(-4)` bow-up; held: `rotate(0)`.
4. **Desktop hero: the boat sails in once and anchors.** 4 s opening, then one 24 s passage from the unsurveyed margin to the anchorage, `fill="freeze"` forever. No out-and-back: it would put 58 repaints/s on a 20 ms/frame sheet (12 rule: no continuous animation on a sheet over 8 ms/frame after its opening). After 28 s the hero carries only the lateral-light pair (≤1 repaint/s). The alt line "A boat sails out and back" must become "A boat sails in and anchors" (→ T8).
5. **Only the hero and tide strip open at load; Approaches and the log open on deliberate delays** (survey 28 s, typing 48 s), because the SMIL clock runs offscreen (12 fact 5, 11, 16, 35). Every frame before and after is composed. Rejected: 11's "resurvey every 96 s" (≈23 % of a core on one sheet).
6. **Packet boat is plotted, not sailed.** Dead-reckoning fixes every 4 s (12 idea 1, 10 idea 1, 26 "date the fixes"): discrete translate, 0.25 repaints/s, a ⊙ fix mark left at each position; 24 s run, 72 s hold at anchor, 96 s period, 400 ms opacity fade at the wrap. Phone hero uses the same mechanism (10 F6).
7. **All discrete transitions snap to a 0.5 s grid.** Lights, fixes, cursor and label swaps share change instants, so four light characters on Approaches cost ≈1.7 repaints/s instead of 3+. A flash is 0.5 s long (chart-plausible; ≤1 flash/s per light, far under 09's 3/s).
8. **Footer is the one ambient loop** (3 ms/frame measured): 24 s `settle` arrival, then a 10 s `sea` loop. The boat anchors on arrival (rode + anchor glyph settle in; main luffs once) because a sailboat cannot hold station above a fall (26); "Obstn rep. 2026 (PA)" sits where the serpent rises (25). Serpent first rises at `arrive.end+20s` and leaves three decaying ripples (16 F3); it is one 96 s-period animation, not an `.end` chain (11).
9. **Geometry attributes are never animated** (`x, y, cx, cy, width, height, r, x1…y2, d, stroke-dashoffset`) except `stroke-dashoffset` inside the ≤4 s hero/tide openings (contour tracing). Cursor = discrete translate; crawl bar = `scale`; spray = translate; fall lines = translated dashed line in a clip (12, 11).
10. **No syncbase in emitted SVG.** The scheduler resolves every chain (`name.end+0.4s`) to absolute seconds at build time; no `repeatEvent`, no `.end` chains, no `keyPoints` (11 §8). Every freeze-in element carries base `opacity="0"`.
11. **`motion=False` emits the frozen end state** from the same code path; still editions serve `prefers-reduced-motion` (09, 36). Phone editions are still by construction except the hero (10 F6); hero gets a phone-still file too.
12. **Filters never touch anything animated**; night halos are static radial-gradient circles sharing the light's opacity animation (11, 12).
13. **Light characters keep real rhythm**: `Fl(3) 10s`, `Fl R 4s`/`Fl G 4s` alternating, `Iso 2s`; 10, 4 and 2 all divide 96 so the page phase-locks (05, 30).

## 2. Design and implementation

### 2.1 The scheduler (`svgkit.py`)

```python
class Timeline:
    """One per sheet build. Resolves cues to absolute seconds, prefixes ids, enforces budgets,
    and in still mode emits end states instead of SMIL."""
    def __init__(self, sheet: str, motion: bool = True, period: float = 96.0,
                 quantum: float = 0.5, ambient: bool = False): ...
    def cue(self, name: str, begin: float, dur: float) -> float      # registers; returns end time
    def t(self, name: str) -> tuple[float, float]                   # (begin, end) of a cue
    def anim(self, attr, values, dur, begin, ease=None, freeze=True, repeat=None,
             key_times=None, discrete=False, still=None) -> str    # <animate>, '' when still
    def xform(self, kind, values, dur, begin, ease=None, freeze=True, repeat=None,
              key_times=None, discrete=False, still=None) -> str   # <animateTransform>
    def fade_in(self, inner, begin, dur=0.25, rise=3, ease="settle") -> str
    def draw_in(self, path_attrs, dur=1.6, begin=0.0, ease="draw") -> str
    def reveal(self, inner, begin) -> str                           # base opacity=0 + <set>
    def typed(self, s, x, y, font, size, fill, begin, seed, pace=(0.06, 0.11),
              space=0.16, dash=0.22) -> tuple[str, float, list[float]]  # svg, end, glyph times
    def flash(self, character, period, begin=0.0, still="lit") -> str
    def sail(self, path_d, begin, dur, n=48, ease="settle", mast_x=3.0) -> Sail
    def fixes(self, points, begin, every=4.0, labels=None, hold=None) -> str
    def tack(self, begin, mast_x) -> str
    def every(self, kind_or_attr, segments, begin, period=None) -> str  # one long-period loop
    def report(self) -> dict   # counts, repaints/s estimate, opening_end, violations
```

Enforced at build (raise): `repeat="indefinite"` only on `opacity`/`transform`, continuous values only when `ambient=True`; discrete instants `begin + keyTime·dur` divisible by `quantum`; loop `dur` ∈ `LOOP`; geometry attributes only in finite one-shots ending ≤4 s after their group starts; ids `f"{sheet}-{name}"`. `still=None` means last value for one-shots; loops must pass `still` explicitly (lights `"lit"`, boats the anchored point, cursor `1`, serpent hidden). In still mode `fade_in` returns `inner` unwrapped, `draw_in` a plain path, `reveal` the bare element, `sail` a static `translate(x_end y_end)`.

`report()` is written to `assets/build-report.json["motion"][sheet]` (T1's report file): `{indefinite, repaints_per_s, opening_end, continuous_windows:[[a,b],…], geometry_anims, violations:[]}`.

### 2.2 Path sampling → `animateTransform`

`sail()` flattens each cubic of `smooth_path()` into 64 chords, takes `n` points equally spaced by arc length, rounds to integers, and warps `keyTimes` through the easing's cubic Bézier (solve x→y by bisection), so `calcMode="linear"` between samples reproduces the ease. It detects x-direction reversals and returns `Sail(anim, end, tacks=[t…], facing0)`.

```xml
<g id="hero-boat" transform="translate(1180 410)">            <!-- still edition: translate(640 468) -->
  <animateTransform attributeName="transform" type="translate" begin="4s" dur="24s" fill="freeze"
    calcMode="linear"
    values="1180 410;1163 404;1146 399;…;646 468;640 468"
    keyTimes="0;0.0316;0.0627;…;0.9871;1"/>
  <g id="hero-hull" transform="scale(-1,1)">…11-command sloop…</g>
</g>
```

Spec-hero's course turns from 077°/106° to 276°, so `sail()` emits one tack about 14 s into the passage:

```xml
<!-- sails: luff flat, refill on the other side; hull mirrors at the flat moment -->
<g transform="translate(3 0)"><g>
  <animateTransform attributeName="transform" type="scale" begin="17.6s" dur="1.2s" fill="freeze"
    values="1 1;0.06 1;-1 1" keyTimes="0;0.5;1" calcMode="spline"
    keySplines="0.4 0 0.2 1;0.16 0.84 0.44 1"/>
  <g transform="translate(-3 0)">…main, jib…</g></g></g>
<animateTransform xlink:href="#hero-hull" attributeName="transform" type="scale" begin="18.2s"
  dur="0.1s" fill="freeze" calcMode="discrete" values="-1 1;1 1"/>
```

### 2.3 Discrete steppers

Fixes (Approaches packet boat, phone hero), labels optional (T2/T3 supply times or dates):

```xml
<animateTransform attributeName="transform" type="translate" begin="0s" dur="96s"
  repeatCount="indefinite" calcMode="discrete"
  values="300 560;380 548;…;1068 430;1068 430" keyTimes="0;0.0417;…;0.25;1"/>
<g opacity="0"><circle r="3" .../><use href="#g-plex-13-48" .../>   <!-- ⊙ 0412 -->
  <animate attributeName="opacity" values="1;1;0" keyTimes="0;0.99;1" dur="96s" begin="8s" repeatCount="indefinite" calcMode="discrete"/></g>
```

Lights, quantised (Fl(3) 10s → flashes at 0, 1.5, 3 s, each 0.5 s):

```xml
<circle ... fill="url(#hero-halo-r)" opacity="1">
  <animate attributeName="opacity" values="1;0;1;0;1;0" keyTimes="0;0.05;0.15;0.2;0.3;0.35"
    dur="10s" begin="0s" repeatCount="indefinite" calcMode="discrete"/></circle>
```

Typing (log): `typed()` wraps each glyph `<use>` from `text_use()`; times come from an LCG seeded on the row index.

```xml
<g fill="#1B2A41">
  <use href="#g-plex-15-112" x="128" y="201" opacity="0"><set attributeName="opacity" to="1" begin="49.06s"/></use>
  <use href="#g-plex-15-105" x="137" y="201" opacity="0"><set attributeName="opacity" to="1" begin="49.15s"/></use>…
</g>
<rect id="log-cursor" x="0" y="190" width="8" height="15" transform="translate(128 0)">
  <animateTransform attributeName="transform" type="translate" calcMode="discrete" begin="49s" dur="4.1s"
    fill="freeze" values="128 0;137 0;146 0;…"/>
  <animate attributeName="opacity" values="1;0" keyTimes="0;0.5" dur="1s" begin="62.5s"
    repeatCount="indefinite" calcMode="discrete"/></rect>
```

Crawl bar: `xform("scale", ["0 1","0.28 1","0.28 1","0.62 1","0.62 1","1 1"], 3.8, begin, key_times=[0,.26,.39,.63,.79,1], ease=["draw","linear","draw","linear","settle"])` on a rect whose origin is the bar's left edge; POSITION/WIND numerals are three stacked groups toggled by discrete opacity on the same instants.

### 2.4 Long-period loops (`every`)

One element, one period, a hold padded to 96 s; no chains:

```xml
<g id="footer-serpent" clip-path="url(#footer-water)" transform="translate(880 150)">
  <animateTransform attributeName="transform" type="translate" additive="sum" begin="44s" dur="96s"
    repeatCount="indefinite" values="0 30;0 0;0 0;0 30;0 30" keyTimes="0;0.0094;0.0156;0.025;1"
    calcMode="spline" keySplines="0.16 0.84 0.44 1;0 0 1 1;0.4 0 0.2 1;0 0 1 1"/>
  …head path, then humps 2 and 3 with the same animation offset +0.25 s / +0.5 s…</g>
<g transform="translate(880 150)"><circle r="6" fill="none" stroke-width="0.6" opacity="0">
  <animate attributeName="opacity" values="0;0.5;0;0" keyTimes="0;0.025;0.233;1" dur="96s" begin="44s" repeatCount="indefinite"/>
  <animateTransform attributeName="transform" type="scale" values="1;1;2.6;2.6" keyTimes="0;0.025;0.233;1" dur="96s" begin="44s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.16 0.84 0.44 1;0 0 1 1"/></circle> ×3</g>
```

### 2.5 Choreography tables (all `fill="freeze"` unless marked loop; times absolute)

**Hero (desktop 1280×740).** t=0: paper, neat line, minute bars, graticule pattern, UNSURVEYED hatch, open title-block rules, compass rings, N, buoy bodies, boat at the seaward end (never off-sheet).

| t (s) | element | how |
|---|---|---|
| 0.2+0.12·i | contour level i, deep first | `draw_in` 1.6 s draw |
| 1.0 / 1.3 | tint A / B | opacity → target, 1.0 s settle |
| 1.6 | land fills, danger lines, wrecks, anchorage | `fade_in` 0.65 settle |
| 1.4+0.04·k | sounding k (course order) | `fade_in` 0.25, rise 3 |
| 2.0 | compass inner ring | `xform rotate` `rot+12;rot−4;rot` keyTimes 0;.45;1, 1.6 s sea |
| 2.2+0.1·rank | feature names | `fade_in` 0.4 |
| 2.6 / 2.85 | "Ben" / "Russell" | `reveal` (one discrete step each) |
| 3.1 | thesis | `fade_in` 0.4, rise 4 |
| 3.3 / 3.6 | title-block rules / imprint, bearings, light labels | `draw_in` 0.65 / `fade_in` 0.4 |
| 4.0–28.0 | boat `sail()` 24 s settle, one tack ≈17.6 s | continuous; then anchored forever |
| 0 → ∞ loop | R"2" Fl R 4s, G"1" Fl G 4s (green begin 2 s) | discrete opacity, 1 repaint/s total |

Repaint rate after 28 s: 1/s. Nothing else loops on the hero.

**Tide strip (soundings).** t=0: rules, ticks, captions, ghosted hero figure. Curve `draw_in` 1.0–2.6 s draw; HW/LW marks `fade_in` at 2.6/2.75; figures `fade_in` 2.6+0.12·j, 0.4 s. Frozen at 3.5 s; 0 loops.

**Approaches (1280×880).** t=0: full geography, lines 1–8 sounded, vessel at east end of line 9, every light in its lit phase, 64 WAL cells lit, packet boat at W0. Delayed opening at 28 s: legs 9–16 as `xform translate` 2.6 s settle each, +0.4 s gaps (28.0–51.6 s); turn = `tack()`; lead-line drop = `xform scale(1,0→1)` 0.3 s draw, 8 per leg; sounding sNN `fade_in` at drop end; WAL cell `reveal` at sNN; south contours `draw_in` from 52.2 s, stagger 90 ms; tints 0.65 s; vessel frozen beside `512` at ~54.5 s. Loops: Grafana Lt + inset twin Fl(3) 10s, four buoys Fl 4s (reds +2 s), Ldg Lts Iso 2s, packet-boat fixes every 4 s (6 fixes, 24 s run, 72 s hold, fade 0.4 s at 95.5 s). Estimated repaints/s after 55 s: ≈1.7 lights + 0.25 fixes ≈ 2.0.

**Log (1280×440).** t=0: paper, rules, red margin, header, entry 0 and 1 complete. Typing from 48.0 s on spec-supporting's relative schedule (+48): cmd rows typed 60–110 ms/glyph (+160 after space, +220 before `--`), out rows `fade_in` 0.25, crawl bar bursts 53.9–57.7 s with swaps at 54.9/56.3/57.7, "Nothing on fire." `fade_in` 0.4 at 58.9 in body mono (25), second command 36–60 ms/glyph, sign-off 62.0 s. Cursor blink from 62.5 s, 1 s period, discrete: 2 repaints/s, the log's only loop.

**Instruments.** No motion. Still file = main file.

**Footer (1280×260, ambient).** t=0: everything drawn, boat at x=90 under way (`rotate(-4)`). `arrive`: `xform translate 90→980` 0–24 s settle; at 24.0 s `rotate −4→0` 0.65 s settle, main luffs once (`scale 1;0.6;1` 0.8 s), rode + anchor + `14 · good holding` `fade_in` 0.65. Loop (10 s, sea): hull `translate-y 0;−2;0`; swell `translate-x 0→−48`; three mist arcs translate-y 0→−8 + opacity .5→0, 1.6 s each on the 10 s grid; fall lines: dashed line translate-y 0→10 inside the water clip. Serpent + ripples per §2.4 at 44 s, every 96 s. Budget ≤4 ms/frame (measured 2.8).

**Phone editions (720-wide, `motion=False`)** for every sheet except the hero. Phone hero: same 4 s opening, sounding stagger 60 ms; boat as `fixes()` every 4 s from 4 s to 28 s (6 fixes) with a 26px time label swapping per fix (labels from T2), then anchored; light pair as desktop. `hero-phone-*-still.svg` additionally built for reduced motion.

### 2.6 Still-frame guarantee

Rule: **a sheet at any instant is a finished sheet.** Formally, for each sheet with still edition S and frames F(t) at t ∈ {0, 0.5·opening_end, opening_end+1, 24, 48, 72, 95} s: (a) ink coverage `ink(F(t))/ink(S) ≥ 0.6`, where ink = pixels not within ΔE 3 of paper; (b) for t ≥ opening_end, changed-pixel fraction `|F(t) − S| ≤ 1.5 %` (lights, cursor, fixes, serpent); (c) no sampled frame has a text-free rectangle larger than 25 % of the sheet where S has text (the log/tide "blank ledger" test). Checked by `scripts/filmstrip.js`: inline the SVG in Playwright, `svg.pauseAnimations(); svg.setCurrentTime(t)`, screenshot, compare to S. The static side (`scripts/check_motion.py`) parses the SVG and asserts: no `animateMotion`; no geometry-attribute animation outside a finite ≤4 s one-shot; base `opacity="0"` on every element with an opacity freeze-in; no `begin` containing `.`; every indefinite animation on opacity/transform; discrete instants on the 0.5 s grid; per-sheet indefinite count and estimated repaints/s ≤ the budget table; `*-still.svg` contains zero `<animate*>`/`<set>`.

### 2.7 Repaint budget and CI

| sheet | continuous window | indefinite anims | repaints/s after opening | ms/frame cap |
|---|---|---|---|---|
| hero | 0–28 s | 2 | ≤1 | 20 (opening only) |
| soundings | 1–3.5 s | 0 | 0 | — |
| approaches | 28–55 s | ≤10 | ≤2 | 15 (opening only) |
| log | 48–62.5 s (discrete) | 1 | 2 | — |
| instruments | none | 0 | 0 | — |
| footer | always | ≤12 | continuous | 4 |

Page after 64 s, from 12's per-repaint costs: footer ≈17 % + ~5 repaints/s × ~10 ms ≈ 5 % → ≈22 % of a core, versus 150–200 % today. Phone hero ≤0.25 repaints/s after 4 s.

CI (`scripts/perf_check.js`, derived from `scratchpad/perf/harness.js`; adds `--warm=`): for each `assets/*-dark.svg`, `node scripts/perf_check.js <svg> --width=870 --warm=<opening_end+2> --seconds=10`, then `--width=360 --dpr=3` on the phone files with `--warm=6`. Fail if: a frozen sheet (soundings, instruments, any `-still`, phone non-hero) shows >0 `ProxyMain::BeginMainFrame` after warm; hero/approaches/log exceed their repaints/s; footer `rasterPerFrame + paintPerFrame > 4`. Warm totals ≈170 s; run nightly and on PRs touching `scripts/`, not on the stats commit. Chromium only until `playwright install` is permitted; recorded as such in DESIGN.md.

## 3. Interfaces

**Provide.** `svgkit.Timeline` (§2.1) and `EASE`, `LOOP`, `QUANTUM=0.5`; `chartlib.sample_path(d, n) -> list[(x,y)]`; `Sail` dataclass `(anim: str, end: float, tacks: list[float], facing: int)`. File suffixes: `{sheet}-{light,dark}.svg`, `{sheet}-{light,dark}-still.svg`, `{sheet}-phone-{light,dark}.svg`, `hero-phone-{light,dark}-still.svg`. `build-report.json["motion"]` schema above. `scripts/check_motion.py`, `scripts/filmstrip.js`, `scripts/perf_check.js`.

**T1**: `build_assets.py` loops editions `(theme, motion, phone)`; passes `Timeline(sheet, motion=…, ambient=(sheet=="footer"))`; runs `check_motion.py` before `git add`; `<picture>` order per sheet: phone+dark, phone, reduce+dark, reduce, dark, img (hero adds phone+reduce pairs at the top). **T2**: course waypoints and `smooth_path` d; mast_x of the 11-command sloop; phone fix labels (6 strings); hero sounding course order; keep lights at Fl R/G 4s. **T3**: positions of W0…ANCH and the six fix points; light characters as strings (`"Fl(3) 10s"`, `"Fl R 4s"`, `"Iso 2s"`); survey leg endpoints; `512` sounding id. **T5**: `text_use` must keep one `<use>` per glyph with `x`/`y` attributes (typed() depends on it). **T6**: contour paths with `pathLength="1"` acceptable; graticule as pattern (never animated); halos as gradient circles with `id` so flash can target them. **T7/T9**: `log.json` entries with `kind`; `typed()` seeds from row index; the `measured` flag does not affect motion. **T8**: alt lines "A boat sails in and anchors." and footer alt describing the still state only (25). **T10**: consumes `build-report.json["motion"]`, the filmstrip PNGs and perf JSON; verifies on a scratch repo that GitHub keeps `media="(prefers-reduced-motion: reduce)"` (undocumented, 11/09).

**Need.** From 12's owner: harness unchanged except `--warm`; from T1: an env/TOML `motion = "on"|"off"` kill switch (36 F6) that forces `motion=False` for all editions.

## 4. Build order, effort, risks, omissions

Order: (1) `Timeline` core + still mode + `check_motion.py` (8 h); (2) `sample_path`/`sail`/`tack`/`fixes`, delete `course`/`out_and_back`/`animateMotion` (6 h); (3) `flash` quantised + `every` (2 h); (4) `typed` + cursor + bar (3 h); (5) hero and footer choreography with T2/T9 (8 h); (6) Approaches delayed survey + lights + fixes with T3 (4 h); (7) `filmstrip.js`, `perf_check.js`, workflow wiring (6 h); (8) scratch-repo media-query test (1 h). ≈38 h.

Risks: GitHub may strip `prefers-reduced-motion` (fallback: animated edition); Chromium-only measurements; Chrome starts the clock at first paint, Firefox at load (delays shift, all frames composed, harmless); per-glyph `<set>` adds ~20 KB raw / 3 KB gz to the log; 30's type-role lint must accept 26px phone labels.

Left out deliberately: heel/bob on anything but the footer hull, survey-vessel idling, repeat-on-scroll, `repeatEvent`, `keyPoints`, `feGaussianBlur`, `patternTransform`, cross-sheet synchronisation (impossible in `<img>`), hero out-and-back.

## 5. Acceptance criteria

1. `grep -c animateMotion assets/*.svg` = 0; `check_motion.py` passes on every file with zero violations.
2. Every `*-still.svg` has no `<animate`, `<animateTransform`, `<set`, and pixel-matches the animated edition at t = 95 s within 1.5 % (lights lit, boat anchored).
3. Filmstrip (§2.6) passes for all sheets at the seven sampled times; no frame of log or tide shows blank paper.
4. `perf_check.js`: soundings, instruments and every still/phone-non-hero file 0 repaints after warm; hero ≤1/s, approaches ≤2/s, log ≤2/s; footer ≤4 ms/frame; 360 px DPR3 hero ≤0.25 repaints/s after 6 s.
5. Every discrete key instant on the page is a multiple of 0.5 s; every loop dur ∈ {2, 4, 10, 24, 96} (2 s for Iso only).
6. The emitted SVG contains no `begin` with a syncbase (`.begin`, `.end`, `repeatEvent`); every freeze-in has base `opacity="0"`.
7. Hero opening ends at 4.0 s, boat anchored by 28.0 s; Approaches survey begins at 28.0 s; log typing at 48.0 s; footer serpent at 44 s then every 96 s with three ripples; these appear in `build-report.json["motion"]`.
8. Light characters match their labels (Fl(3) 10s: three 0.5 s flashes at 0/1.5/3 s), under 09's 3 flashes/s.
