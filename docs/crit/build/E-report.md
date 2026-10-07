# E — T4 motion engine: build report

Files written (all mine per BUILD-CONTRACT; nothing else touched, no git):

- `scripts/timeline.py` — Timeline, NullTimeline, Sail, Tack, samplers, light-character parser
- `scripts/checks/motion.py` — static motion lint plug-in (`NAME="motion"`, `TIER="fast"`)
- `scripts/perf_check.js` — 12's harness + `--warm --seconds --width --dpr --json --class --static --offscreen --no-fail` + MASTERPLAN 7.3 budget evaluator
- `scripts/render.mjs` — `frames | silhouette | phone | matrix` (Playwright, no image library: pixels are read in-page through a canvas)
- `tests/test_timeline.py` — 26 tests, all green (`python3 -m unittest tests.test_timeline`)
- demo: `scratchpad/crit/build/make_demo.py` → `E-demo.svg` (22.8 KB / 2 KB gz), `E-demo-still.svg` (9.2 KB, zero `<animate*>`/`<set>`), `E-demo-report.json`, `E-frames/` (frame-*.png, still.png, strip.png, frames.json, phone.png, 128 px silhouettes), `E-perf-{opening,after,still}.json`

## 1. Public API (exact signatures; `__all__` is what `svgkit` re-exports via `from timeline import *`)

```python
EASE: dict[str, str]; LOOP_PERIODS: tuple; QUANTUM: float; PAGE_PERIOD: float   # straight from tokens
GEOMETRY_ATTRS: frozenset; LOOP_ATTRS = {"opacity", "transform"}; SYNCBASE: re.Pattern; GRID_TOL = 0.0025

class Timeline:
    def __init__(self, sheet: str, motion: bool = True, period: float = 96.0, quantum: float = 0.5, ambient: bool = False)
    def cue(self, name, begin, dur) -> float                 # a cue named "opening" fixes report()["opening_end_s"]
    def t(self, name) -> tuple[float, float]
    def id(self, name) -> str                                # f"{sheet}-{name}" (edition.prefix_ids is idempotent)
    def on_grid(self, t) -> bool;  def snap(self, t) -> float
    def anim(self, attr, values, dur, begin, ease=None, freeze=True, repeat=None, key_times=None, discrete=False,
             still=None, name=None, additive=False, kind=None, cls="one-shot") -> str      # <animate>, '' when still
    def xform(self, kind, values, dur, begin, ease=None, freeze=True, repeat=None, key_times=None, discrete=False,
              still=None, name=None, additive=False, cls="one-shot") -> str                  # <animateTransform>
    def set(self, attr, to, begin, name=None, exempt=False) -> str                            # <set>, grid-snapped
    def prop(self, attr, values, dur, begin, still=None, **kw) -> tuple[str, str]  # ('opacity="0"', <animate>) / ('opacity="1"', '') still
    @staticmethod still_value(values, still=None) -> str
    def fade_in(self, inner, begin, dur=0.25, rise=3, ease="settle", name=None) -> str       # <g opacity="0">…; still: inner
    def draw_in(self, path_attrs, dur=1.6, begin=0.0, ease="draw", name=None) -> str         # pathLength=1; still: <path …/>
    def reveal(self, inner, begin, name=None) -> str                                          # opacity="0" injected on the element + <set>
    def typed(self, s, x, y, role, begin, seed, pace=(0.036, 0.06), space=0.16, glyphs=None, dash=0.22) -> (svg, end, times)
        # glyphs: callable glyph_cb(s, x, y, role) -> list[(svg_fragment, x_advance)] (one per character, '' for space)
        # or that list prebuilt. Never imports typeset. Output is wrapped in <g class="typed">.
    def cursor(self, times, xs, y, w=8, h=15, blink_begin=None, fill="currentColor", end_x=None, name=None) -> str
    def flash(self, character, period=None, begin=0.0, still="lit", lit=1, dark=0, name=None) -> str
        # the one light-character parser: F, Fl, Fl(n), LFl, Oc, Oc(n), Iso, Q (+ colour letter, + "10s" period)
    def sail(self, path_d, begin, dur, n=64, ease="settle", mast_x=3.0, pitch=-4.0, pitch_settle=0.0, name=None) -> Sail
    def tack(self, begin, mast_x, sails, facing=1, dur=1.2, name=None) -> Tack
    def fixes(self, points, begin, every=4.0, labels=None, hold=None, boat=None, ink="currentColor", mark=None,
              fade=None, name=None) -> str
    def every(self, kind_or_attr, segments, begin, period=96.0, discrete=False, additive=False, still=None, name=None) -> str
        # segments = [(t_rel, value[, ease_to_next]), …]; last value holds to period
    def opening_end(self) -> float;  def continuous_windows(self) -> list[list[float]];  def repaints_per_s(self) -> float | "continuous"
    def report(self) -> dict  # {sheet, class, motion, ambient, indefinite, repaints_per_s, opening_end_s, longest_loop_s,
                              #  loops[{attr,kind,period,begin,changes,discrete,still,name}], continuous_windows, geometry_anims,
                              #  snapped[{what,from,to}], cues, anims, violations[]}

class NullTimeline(Timeline)   # Timeline(sheet, motion=False, …)

@dataclass Sail:  anim, end, tacks: list[float], facing: int, start, stop, transform, pitch, headings, begin, dur, still
    def wrap(self, inner, pitch=-4.0, mirror=True, gid=None, facing_anim="") -> str
        # <g transform=translate(x0 y0)>{anim}<g transform="scale(facing 1)">{facing_anim}<g transform="rotate(pitch)">{pitch}{inner}</g></g></g>
@dataclass Tack:  sails (wrapped, luffing), hull (discrete scale flip for the facing group), begin, end, flip_at, facing

def sample_path(d, n) -> list[(x, y, heading_deg)]     # M/L/H/V/C/S/Q/T/Z abs+rel, curves flattened to <= 1 px chords; arcs raise
def path_length(d) -> float
def parse_character(character, period=None) -> (kind, n, period)
def flash_schedule(character, period=None) -> list[(t0, t1)]   # lit intervals on the 0.5 s grid
def ease_curve(ease) -> (x1, y1, x2, y2);  def ease_at(ease, x) -> y;  def ease_inverse(ease, progress) -> x
```

Rules enforced (raise = ValueError at emit time; record = `report()["violations"]`):
indefinite only on opacity/transform (raise); continuous indefinite only when `ambient=True` (raise, in still mode too);
loop period ∈ `tokens.LOOP_PERIODS` (raise); loops need `still=` (raise); discrete begins snapped to the grid and recorded
in `report()["snapped"]`, internal key instants off-grid raise; geometry attrs never loop (raise), one-shot > 4 s or
unfrozen recorded; string `begin` (any syncbase) raises, and every emitted string is re-checked against `SYNCBASE`;
`animateMotion` is never emitted. `repeatCount="indefinite"` appears once in the source (inside `anim`), reached only
through `flash()`, `every()`, the looping `fixes()` and `cursor(blink_begin=…)`.

`checks/motion.py`: `check(ctx) -> list[Finding]` using `check.Finding/fail/warn` when the runner provides them
(fallback namedtuple with the same `(level, code, msg, where)` shape); reads `ctx.svgs` (dict or list), `ctx.report`
(either `report["motion"][sheet]` or `report["sheets"][name]["motion"]`), else `assets/v9/*.svg`, `assets/*.svg`,
`assets/build-report.json`. Codes: MOTION, MOTION-ANIMATEMOTION, MOTION-GEOMETRY, MOTION-FILTER, MOTION-LOOP-ATTR,
MOTION-SYNCBASE, MOTION-STILL, MOTION-BUDGET, MOTION-REPORT, MOTION-XML/READ. Also `scan(svg_text, name)` and a CLI.
On the legacy `assets/` it fails as it should (animateMotion, `cy`/`width`/`x`/dashoffset loops, 14 s periods).

`perf_check.js`: repaints = `ProxyMain::BeginMainFrame` in the trace window (12's measure); ms/frame = raster+paint per
repaint. Budget class inferred from the filename (`frozen | hero | approaches | log | footer | hero-phone | none`) or
`--class=`. Exit 1 on a budget failure unless `--no-fail`. `--json=path` writes rows.

`render.mjs frames <svg> <outdir> t1,t2 [--still S] [--width] [--strip png] [--json]`: inline, `pauseAnimations();
setCurrentTime(t)`, per frame `inkFrac`, and against S: `coverage = ink(F)/ink(S)`, `changedFrac`, `emptiedCellFrac`
(8×8 cells inked in S but < 10 % of that in F; > 0.25 flags `blankLedger`). `silhouette <svg…> [--out]`: 128 px,
16×8 mass grid, pairwise L1 (≥ 0.25 pass, exit 1 otherwise), `heaviestTopLeft` per sheet. `phone <svg> <out> [--width 360]
[--dpr 3]`. `matrix`: placeholder (needs render_readme's preview page).

## 2. Measured (demo sheet 1280×740, Chromium 141 headless, `<img width=870>`, DPR 1)

| run | warm | trace | repaints | repaints/s | ms/frame (raster+paint) | cpu | verdict |
|---|---|---|---|---|---|---|---|
| E-demo.svg during the sail (`--class=hero`) | 6 s | 10 s | 554 | 55.4 | 3.52 | 21 % | FAIL as expected: continuous window 4–28 s (the hero's own budget applies only after 30 s) |
| E-demo.svg after the opening (`--warm=30`) | 30 s | 10 s | 10 | **1.0** | 3.78 | 0.5 % | PASS: two Fl 4s lights sharing instants = 1 repaint/s, exactly `report()`'s estimate for the lights |
| E-demo-still.svg (`frozen`) | 4 s | 6 s | 0 | **0** | – | 0 % | PASS |

`Timeline.report()` for the demo: class `lights`, indefinite 5 (2 lights + fixes translate + fixes fade + cursor blink),
repaints_per_s 2.0 over the 96 s period (lights 1.0 + the 1 s cursor blink from 48.5 s; the 30–40 s trace saw only
the lights, hence 1.0), opening_end_s 4.0, longest_loop 96, continuous_windows [[0.2, 28.0]], violations [].

Frames vs still (`render.mjs frames … 0.5,2,4,10,30 --still`): t=0.5 coverage 0.088 (contours tracing in), t=2 0.673,
t=4 0.986, t=10 0.988 / changed 0.37 %, t=30 0.994 / changed 0.07 %; no frame flags blank-ledger after 2 s. Looked at
`E-frames/strip.png`: contours draw deep-first, tint settles, soundings lift in, name blocks step in, boat faces west with
bow-up trim, tacks (sails luff, hull mirrors) where the course doubles back, anchors level at 28 s; ⊙ fixes accumulate
along the packet boat's track with the glyph boat stepping; both lights lit in every frame sampled on the grid.
Silhouette: demo vs legacy footer L1 0.99, vs log 0.76 (pass).

## 3. Deviations from T4 / MASTERPLAN (all deliberate, each reversible)

1. **Fix marks do not loop.** T4 §2.3 gave every ⊙ its own 96 s indefinite opacity loop (9 indefinite animations for
   7 fixes, over Approaches' budget of 10 with its lights). The marks are now finite `reveal()`s that stay; only the
   boat loops (translate + a 0.5 s dark gap before the wrap): 2 indefinite animations, ≈0.08 repaints/s. A navigator
   does not erase the fixes; on the wrap the boat re-runs over its plotted track.
2. **The wrap fade is a 0.5 s discrete gap, not a 400 ms opacity fade**: a continuous loop segment is forbidden off
   the ambient sheet, and 0.4 is off-grid.
3. **Tack flip at begin+0.5 s** (grid) instead of +0.6; the luff keyTimes put the flat moment at 0.5/1.2 so the hull
   mirrors exactly when the sails are flat. Tack begins are snapped.
4. **`typed()` takes `glyphs=`** (callable or prebuilt per-character list) instead of `font, size, fill`, so timeline
   never imports typeset (BUILD-CONTRACT). Its `<set>`s and the cursor ride are off-grid by nature (36–60 ms
   cadence); they are emitted inside `<g class="typed">` / `<rect class="typed">`, recorded as class `typed-burst`,
   and the static lint exempts them only inside 40–52 s. The blink loop is on the grid.
5. **Grid tolerance 2.5 ms** (`GRID_TOL`): keyTimes carry 6 decimals on discrete/loop animations so begin+kt·dur hits
   the grid within microseconds; the lint uses the same tolerance.
6. **Pitch levels in one discrete step at `sail.end`** by default (`pitch_settle=0`), so the hero carries nothing
   continuous after 28 s; the footer passes `pitch_settle=0.65` for its settle.
7. **`continuous_windows` merges touching one-shots**, so the hero reports [0.2, 28] (T4 §2.7's "0–28 s"), not just the
   sail; `opening_end_s` is the chain of non-sail one-shots from t=0 (4.0 on the hero) or the `opening` cue.
8. **`Iso 2s` cannot be emitted**: 2 ∉ `tokens.LOOP_PERIODS` (MASTERPLAN deleted it with the sector light). `VQ` raises
   (2 Hz cannot sit on a 0.5 s grid). `Q` = one 0.5 s flash per second.
9. **Geometry one-shots > 4 s are recorded, not raised** (T4 said raise); the lint fails them, so CI still blocks.
10. **`sample_path` returns (x, y, heading)**, a superset of T4 §3's `(x, y)`.
11. Light characters with a period inside the string (`"Fl(3) 10s"`, `"Fl {scrape_interval}s"`) work with `period=None`.
12. `render.mjs` text-free-rectangle test is a coarse 8×8 "emptied cells" fraction, not a maximal-rectangle search.

## 4. Needs from others

- **A (T1)**: `build_assets.py` passes `Timeline(sheet, motion=ed.motion, ambient=(sheet == "footer"))` and writes
  `tl.report()` to `build-report.json["sheets"][name]["motion"]` (or `["motion"][sheet]`; the plug-in reads both);
  the `motion = "on"|"off"` kill switch forcing `motion=False`; `scripts/checks/__init__.py` is empty while
  `checks/xml.py` does `from checks import Finding` (A's own; mine imports from `check`). Perf warm-ups per
  MASTERPLAN 2.1: hero 30, approaches 44, log 50, footer 66; phone hero `--width=360 --dpr=3 --warm=6`.
- **D (T5)**: `glyph_cb(s, x, y, role) -> [(fragment, advance)]` per character ('' for spaces) so `typed()` can wrap
  one `<use>` per glyph; fragments must be single elements (opacity is injected on the leaf).
- **B (T6)**: `smooth_path` d-strings (M/C only) are what `sail()` samples; halos as gradient circles whose opacity
  takes `flash()`; contour `path_attrs` without `pathLength` (draw_in adds it); the 11-command sloop split into
  hull and sails strings so `tack()` can wrap the sails and `Sail.wrap(…, facing_anim=tack.hull)` can flip the hull.
- **T2/T3 sheet authors**: fix points, labels as positioned fragments relative to each fix, light strings; pass
  `still=` on every loop; register `tl.cue("opening", 0, 4.0)` on the hero.
- **tokens.py (propose, not edited)**: nothing needed; `GRID_TOL` could move there if other modules want it.

## 5. Not done / caveats

- Full suite: `python3 -m unittest discover -s tests` = 105 tests, 1 failure in `tests/test_data.py` (C's `steady`
  fixture), none in mine.
- Chromium only (no `playwright install`); `matrix` is a placeholder; perf numbers are for the 23 KB demo, not the
  real 170 KB hero (whose ms/frame will be ~5× higher; repaint counts are what the gate reads).
