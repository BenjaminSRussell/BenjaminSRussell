# Builder D report — T5 type & lettering engine

Files written (all inside my ownership): `scripts/typeset.py` (965 lines), `scripts/checks/type.py`,
`tests/test_typeset.py` (24 tests, all pass), `scripts/fonts/` (9 subsets, 3 OFL texts, `subset.sh`).
Specimen: `scratchpad/crit/build/D-specimen.svg` + `D-specimen.png` (1280, both editions side by side),
2× crops `D-crop-day.png`, `D-crop-night.png`, `D-crop-sound.png`; generator `specimen.py` beside them.
No git commands were run. `tokens.py` untouched. The full `unittest discover` shows 5 failures, all in
E's `tests/test_timeline.py` (in progress); none in mine.

## 1. Built

### Fonts (`scripts/fonts/`)
```
InstrumentSerif-Regular.ttf 23.4 KB   InstrumentSerif-Italic.ttf 23.2 KB
IBMPlexSansCondensed-Regular.ttf 23.4  -Italic.ttf 25.3  -Light.ttf 23.3        (new, night = Light)
IBMPlexMono-Regular.ttf 14.0  -Medium.ttf 13.8  -Italic.ttf 15.9  -Light.ttf 13.8 (Light new, night)
LICENSE-InstrumentSerif.txt  LICENSE-IBMPlexMono.txt  LICENSE-IBMPlexSansCondensed.txt   subset.sh
```
Deleted: `Inter-*.otf`, `InterDisplay-*.otf`, `DejaVuSansMono*.ttf`, `LICENSE-Inter.txt`, `LICENSE-DejaVu.txt`,
and `IBMPlexMono-SemiBold.ttf` (not in MASTERPLAN §3.1's list; nothing imports it). Sources: google/fonts `main`
(the scratchpad Instrument Serif copies are byte-identical to `main`; the three OFL texts are identical per family).
All nine files are re-subset with one unicode set and `--layout-features='kern,liga,subs,sups' --glyph-names
--no-hinting --desubroutinize`; `subset.sh [SRC_DIR]` reproduces them (no argument = download the originals and the
OFL texts into a temp dir). Unicode set = T5's plus U+2080–2089, U+2009/200A, U+00A0, °, ′ ″, ·, arrows, ✓,
▲ △ ◆ ◇ ● ○. Measured coverage: **no family carries the geometric shapes U+25B2–25CF or thin/hair spaces** (the
engine synthesises the spaces; the shapes stay chartlib symbols), Plex Sans Condensed lacks █ ░ (Mono has them),
Instrument Serif lacks subscript digits, arrows, primes and ✓. `shape()` warns on a cmap miss.

### `scripts/typeset.py`
- `FONTS`: serif, serif-italic, cond, cond-italic, cond-light, plex, plex-light, plex-medium, plex-italic.
- `shape()`: GSUB `liga` greedy longest match from the face's own LigatureSubst (serif: f_i f_l f_f_i f_f_l;
  Condensed: fi); GPOS `kern` format 1 + 2 resolved lookup-ordered (first covering subtable per lookup wins,
  lookups accumulate) instead of the old `setdefault` flattening — cross-checked: identical on all 11,881 serif
  cmap pairs, one italic pair differs where lookup order decides; `KERN_FIX` manual pairs, applied adjacent or
  across one space; synthetic thin .20 em / hair .10 em / nbsp = space; `HAND_KERN`/`HAND_LIFT`; tracking between
  two inked glyphs only.
- `KERN_FIX` values are **measured**, not T5's "+40 for all": serif-italic r +40, f +134, v −10, w −12, y −6,
  t +24; serif r +28, f +52, v/w/y +36. Gaps at the dot: italic "developer · scraping" 123/166 → 163/166;
  with thin spaces 193/196; regular 170/198 → 198/198; "of · x" 28/157 → 162/157.
- Roles from `tokens.ROLES[scale][role]`; night maps `cond→cond-light`, `plex→plex-light` via
  `tokens.NIGHT_LIGHT_CUTS` (so `cond-italic` and `plex-medium` keep their cuts at night — no Light Italic is
  vendored). Grade on the `<g>`: day `stroke=fill stroke-width="0.22" paint-order="stroke" stroke-linejoin="round"`,
  night `stroke=paper stroke-width="0.18"`, only for roles whose tokens grade is `"grade"` (serif ≤ 28).
- `text()` inline paths: size ≥ 36 → integer coordinates, else one decimal. `text_use()` → one `<use href x y>`
  per glyph, ids `{prefix}g-{font}-{size}-{codepoint}` (ligatures use the glyph name, e.g. `g-serif-17-f_i`).
- `_RUNS` registry of `Run(text, role, font, size, x0, x1, y, angle, semantic, within, truth, key, sheet, origin,
  y0, y1, tracking, tracked_spaces)`; rotated runs store the rotated bbox. `FIGURES` list of
  `(sheet, key, value, style)` filled by `text(truth=|key=)` and `sounding()`.
- `sounding()`: Condensed digits via `text_use`, subscript through the encoded U+2080–2089 glyphs (fallback 0.6×
  dropped .15 em if a cut lacks them — only the serif does), `truth="datum"` underline .8 px at baseline+1,
  `illustrative` → italic cut, registers `semantic=False` unless `role="label"`, `origin="sounding"`.
- `text_on_path()`: arc-length placement, per-glyph `<use transform="translate(x y) rotate(a)">`, polyline read
  left-to-right, `spread` distributes the extra into every gap (word spaces too — the first render had
  "UnsurveyedSea"), `start=None` centres, radius guard < 3×size → straight rotated run + entry in `warnings()`.
- `runs()`: figures inside a serif sentence (`("figures", "312")` or an all-figure serif part) set in Condensed
  (italic after an italic serif part) at 0.86× the serif size, registered `origin="runs-figure"` and exempt from
  the scale lint (0.86×17 = 14.6 is off-scale by construction; T5 asked for the ratio).
- `check_type()` → `lint_records()` rules: off-scale size (176 hero-only when the sheet is known); semantic below
  `FLOORS[scale]["semantic"]`; a texture-floor (11 / phone 18) run not from `sounding()` and not role
  `contour-figure`; serif below the serif floor; run leaving `within`; a second `label-caps` run (runs with
  `key="chart-number"` or `"folio"` exempt); tracking on a space. Decision 6: floors in sheet space, no ×0.68.
  `check_budget()`: ≤ 160 glyph defs, ≤ 6 size keys, ≤ 40 KB defs (separate so T10 can treat it as its own check).
- `run_records()` emits the build-report `text[]` schema (s, x0, x1, y, size, font, slant, role, tier, truth,
  key, rot) plus origin, semantic, within, y0, y1, tracked_spaces, tracking — the lint reads these, so
  `scripts/checks/type.py` can run from the sidecar alone.

### `scripts/checks/type.py`
`NAME="type"`, `TIER="fast"`, `check(ctx) -> list[str]`. If `ctx.report` / `ctx["report"]` / `ctx` is a
build-report dict with `sheets{"<sheet>-<edition>": {text[]}}`, lints every sheet (edition and scale parsed from
the key, e.g. `hero-phone-night`), else lints the in-process registry with `ctx.edition/scale/sheet`.
`python3 scripts/checks/type.py assets/build-report.json` runs it standalone (exit 1 on failures).
I did not create `scripts/checks/__init__.py` (A owns the runner); my test imports it as a namespace package.

### Specimen
`D-specimen.svg`: every desk role (display, thesis, figure, figure-2, title, sea-name on a contour, place-water,
place-land, note at −5°, runs, label, label-italic, label-caps, chart number, eight soundings, machine,
machine-strong) plus three phone roles, day on `#F4EEE1` and night on `#0F1A2B`. Looked at 1× and 2×: ligatures
in "fire and flight office", the dot in "developer · scraping" (thin and regular spaces), subscripts, datum
underline, night Light cuts and the serif choke all read as intended. The 176 px name overruns the 640 px
specimen column (the hero is 1280 wide) — not an engine issue.

## 2. Exact exports for the svgkit facade (A)

```python
from typeset import (
    FONTS, KERN_FIX, HAND_KERN, HAND_LIFT, FIGURES, Glyph, Run,
    shape, text, text_use, label, runs, sounding, text_on_path, text_width,
    glyph_defs, glyph_count, begin_asset, exclusions, exclude,
    check_type, check_budget, lint_records, run_records, runs_registry, warnings,
)

def shape(s: str, font: str, size: float | None = None, tracking: float = 0.0,
          hand: dict | None = None, lift: dict | None = None) -> list[Glyph]
    # Glyph(name, adv, dx, kind, dy=0.0, cp=None, ch="", tracked=False); .inked property
def text(s, x, y, role="label", fill=None, anchor="start", within=None, semantic=True, truth=None, key=None,
         edition="day", scale=None, font=None, size=None, tracking=None, opacity=None, rotate=0) -> str
def text_use(...same signature...) -> str
def label(s, x, y, role="label", **kw) -> str            # T6's label_cb: text_use below 36 px, text above
def runs(parts: list[tuple[str, str]], x, y, edition="day", scale=None, fill=None, anchor="start",
         within=None, semantic=True, truth=None, key=None, opacity=None) -> str
def sounding(value, x, y, sub=None, truth="measured", role="texture", anchor="middle",
             edition="day", scale=None, fill=None, key=None, opacity=None) -> str
def text_on_path(s, polyline, role="sea-name", start=0.0, side="above", spread=None, edition="day", scale=None,
                 fill=None, semantic=True, within=None, truth=None, key=None, opacity=None) -> str
def text_width(s, role=None, font=None, size=None, tracking=None, edition="day", scale=None) -> float
def glyph_defs() -> str;  def glyph_count() -> int
def begin_asset(sheet: str = "", prefix: str = "") -> None   # clears glyphs, runs, exclusions, FIGURES, warnings
def exclusions(named: bool = False) -> list[tuple]           # (x, y, w, h); named → (name, x, y, w, h)
def exclude(name, x, y, w, h) -> None
def check_type(edition="day", scale=None, sheet=None) -> list[str]
def check_budget() -> list[str]
def lint_records(records: list[dict], edition="day", scale=None, sheet=None) -> list[str]
def run_records(runs_=None) -> list[dict]                   # build-report text[] entries
def runs_registry() -> list[Run];  def warnings() -> list[str]
FIGURES: list[tuple[sheet, key, value, style]]              # style: upright | italic | datum
```
`edition` accepts `"day" | "night" | "phone-day" | "still-night" | …`, a `tokens.Theme`, or A's `Edition`
(reads `.theme.edition` and `.scale`); `scale=None` infers `phone` from the name, else `desk`.
Role `edition` is also where the fill default comes from (`THEMES[ed].ink`) and the choke colour (`.paper`).

## 3. Needs from others

- **A (T1):** call `typeset.begin_asset(sheet, prefix=...)` per asset, put `glyph_defs()` in `<defs>`, write
  `run_records()` into `build-report.json["sheets"][...]["text"]` and `exclusions(named=True)` into `exclusions`,
  add `glyph_defs: glyph_count()` to the sheet entry; exit 1 on `check_type(ed, scale, sheet)` and report
  `check_budget()`; `scripts/checks/__init__.py` if the runner needs one. If `svg()` prefixes ids by regex, pass
  `prefix=""` here (default) to avoid double prefixes.
- **B (T6):** `label_cb = typeset.label` (signature `label(text, x, y, role, **kw)`; pass `edition=`,
  `rotate=`, `within=`); contour polylines as `list[(x, y)]` for `text_on_path`; exclusion bboxes are `(x, y, w, h)`
  — same shape as `exclude()`. The geometric shapes ▲ △ ◆ ◇ ● ○ must be drawn, no family has them.
- **C (T7):** `truth` and `key` per figure; `sub` meanings per decision 20 (hero `585₁` months, Sheet 3 `4₂` hundreds).
- **E (T4):** `text_use()` keeps one `<use href x y>` per glyph; `appear()`/`fade_in` wrap the whole `<g>` the
  engine returns (grade lives on that group).
- **T2/T3/T9 sheets:** every string through a role; one `label-caps` run per sheet besides the chart number
  (`key="chart-number"`); the log in `machine` 13 (phone 26). Soundings only through `sounding()`; contour
  figures through role `contour-figure` (the only other 11 px allowed).
- **tokens.py proposals (not edited):** a `cond-light-italic` entry is impossible without a fourth Condensed
  cut; if night italic labels should also lighten, add `IBMPlexSansCondensed-LightItalic` to the vendor list and
  `"cond-italic": "cond-light-italic"` to `NIGHT_LIGHT_CUTS`. Consider adding `"figures"` as a documented pseudo-role
  for `runs()`.

## 4. Deviations from T5

1. `KERN_FIX` values are measured per pair (above), not a flat +40; the +40 applies to italic `r` exactly.
2. Glyph names are kept (`--glyph-names`), so "fire" shapes to `f_i`, not `glyph00056` (acceptance 3 reworded).
3. `check_type(edition, scale=None, sheet=None)` takes scale and sheet too (decision 6 floors are per scale;
   176 is hero-only). The glyph budget is `check_budget()`, separate from `check_type()`.
4. `runs()` figures at 0.86× are off-scale by construction; they are registered `origin="runs-figure"` and exempt.
5. Role `contour-figure` (11 px, in tokens) is allowed beside `sounding()` at the texture floor; texture roles
   are forced `semantic=False`.
6. Night keeps `cond-italic` and `plex-medium` at their cuts (tokens maps only `cond` and `plex`).
7. `Glyph` carries extra fields (`dy`, `cp`, `ch`, `tracked`); `dx` is the kern shift before placing, `adv` the
   advance after (with tracking).
8. `text_on_path(start=None)` centres; `spread` widens word spaces too (needed — see the first render).
9. `IBMPlexMono-SemiBold.ttf` removed (MASTERPLAN §3.1 list); legacy `svgkit.FONTS` still names it and the
   Inter/DejaVu keys, loaded lazily — `sheets/_v8_reference.py` only uses serif/plex keys, so it still runs.
10. No `hb-shape` in the container: the kern loader was validated against the old loader (all serif pairs equal)
    rather than HarfBuzz; `uharfbuzz` is not installed and the contract forbids new dependencies.
