# T5 — Type & lettering engine

Re-measured with fontTools on the vendored subsets and on google/fonts @ `5e8a3ba`; where a critic's figure was wrong I say so.

## 1. Decisions

1. **Three faces, three voices** (per 07, 13, 33): Instrument Serif = the chart-maker (name, thesis, place names, notes); **IBM Plex Sans Condensed** = the chart (soundings, bearings, labels, title block, legend); IBM Plex Mono = the machine (log, WAL tape, `$` commands).
2. **Adopt Plex Sans Condensed, with a correction.** 07 claimed "35% narrower": measured, `SURVEYED 2024 – 2026 · RUSTMAPPER ON PYPI` at 13 px is 261 px condensed vs 320 px mono, **18% narrower**. Still adopted for what mono lacks: a plain zero (mono's dot is 118×124 units and closes the counter at ×0.68), kerning (mono has 0 pairs), a true italic (−11°), and encoded subscript digits U+2080–2089 with `subs` for the historian's sub-unit soundings.
3. **Vendor Plex Mono Light for night** (stems 57–64 units vs Regular 80–87, ×0.73). Night differs by weight, not inversion (per 07, 33); Condensed Light likewise. Delete Inter and DejaVu (per 35).
4. **One scale, enforced**: `11 · 13 · 17 · 22 · 28 · 36 · 46 · 60 · 96`, plus 176 on the hero only. Phone scale in 720-space: `18 · 26 · 30 · 40 · 132` (per 10). The build fails on any other size; the scale is the allowed set, roles need not use it all (per 30).
5. **Serif floor 17 px** (per 07: hairline 25/1000 em Regular, measured; 37 Italic). Amends spec-hero (names 15, notes 14–16) and 30's roles: 15 px × 0.68 puts a 25-unit hairline at 0.26 px.
6. **Soundings are upright or italic, never "4° slanted"** (13 vs 07). One rule, upright = measured, sloping = illustrative; a decorative lean would corrupt it. The subscript stays: `58₃` = 58 commits, 3 contributors, defined once in the legend (T7 owns the meaning).
7. **Scan tier** (per 29): anything a persona needs in 60 s is ≥ 22 px serif in the F-path or lives in Markdown. `label-caps` is budgeted to one run per sheet plus the chart number.
8. **Grade per edition** (per 07, 14): day serif ≤ 28 gets a 0.22 px ink spread; night serif ≤ 28 a 0.18 px paper-coloured choke; night small sans/mono use the Light cuts instead of a choke.
9. **Names along contours are placed glyph by glyph**, not with `<textPath>`. `<textPath>` renders on GitHub (07) but needs a font, and we ship outlines; `text_on_path()` emulates it (14) and the lint can see it.
10. **Phone edition serves at `(max-width: 767px)`** (per 10). Between 600 and 767 px a 1280 sheet shows at 0.45–0.58, where 13 px is 6–7.5 px: see the ×0.5 column.
11. **The lettering sentence** (per 06, 07, 09), once in the legend: "Upright: measured, fixed, dry. Sloping: illustrative, floating, submerged. Underlined: height above datum." T8 repeats it in the colophon.

## 2. Design and implementation

### 2.1 Type roles (desktop, 1280-space)

| Role | Face | Size | Tracking | Case | Usage | ×0.68 | ×0.5 |
|---|---|---|---|---|---|---|---|
| display | Serif Regular | 176 | −3, hand-kerned | mixed | hero name only | 120 | 88 |
| figure | Serif Regular | 96 | −2 | figures | one hero number per sheet (commits) | 65 | 48 |
| figure-2 | Serif Regular | 46 | −1 | figures | secondary big figures (Soundings row) | 31 | 23 |
| thesis | Serif Italic | 36 | −0.2 | mixed | the one italic line under the name | 24.5 | 18 |
| title | Serif Regular | 28 | −1 | mixed | title-block names, open title block | 19 | 14 |
| sea-name | Serif Italic | 28 | +2 (spread) | mixed | sea areas, on a contour via text_on_path | 19 | 14 |
| place-water | Serif Italic | 17 | 0 | mixed | shoals, banks, harbours, anchorages, wrecks | 11.6 | 8.5 |
| place-land | Serif Regular | 17 | 0 | mixed | islands, named structures | 11.6 | 8.5 |
| note | Serif Italic | 17 | 0 | mixed | one pencil note per sheet, rotated −4…−7° | 11.6 | 8.5 |
| label | Sans Cond Regular | 13 | 0 | mixed | mark labels, light characters, bearings, legend, numbered notes, title-block lines | 8.8 | 6.5 |
| label-caps | Sans Cond Regular | 13 | +0.6 (0.046 em) | caps | one stamp per sheet + chart number | 8.8 | 6.5 |
| texture | Sans Cond Regular / Italic | 11 | 0 | figures | soundings only; never semantic | 7.5 | 5.5 |
| machine | Plex Mono Regular (Medium for `$`) | 13 | 0 | as typed | log body, WAL caption, `pip install` | 8.8 | 6.5 |

Night: the four sans/mono roles use the Light cuts; serif ≤ 28 takes the choke; `display` stays full ink. Floor **9 px rendered**: every role but `texture` passes at ×0.68, none at ×0.5 (decision 10). Phone roles (720-space, ×0.5 at 360): display 132 → 66, thesis 40 → 20, place 30 → 15, label 26 → 13, texture 18 → 9; nothing else (per 10).

### 2.2 Lettering by feature class

`chartlib.LETTERING: dict[class, (role, slant)]`, consulted by every feature drawer:

| Class | Examples | Lettering |
|---|---|---|
| dry, fixed | islands, lights, leading marks, installations, title block, bearings | upright (`place-land`, `label`) |
| water, submerged | sea areas, shoals, banks, harbours, anchorages, wrecks | italic (`sea-name`, `place-water`) |
| floating | buoys and their characters: `R "2" Fl R 4s` | italic `label`; the light character stays with its mark (per 33) |
| figure, measured | repo commits, 512, 16, 0.1.3, chart number | upright |
| figure, illustrative | field depths, log wind | italic |
| figure, above datum | 512 / 256 / followers in spec-hero §3 | upright + underline 0.8 px, 1 px below baseline |

### 2.3 svgkit changes

**Shaping.** New `shape(s, font) -> list[Glyph(name, adv, dx, kind)]`, shared by `text`, `text_use`, `text_width`, `text_on_path`: (a) `liga` from the font's own GSUB LigatureSubst (greedy longest match; the subset already holds fi/fl/ffi/ffl as glyph00054–57, never used today); (b) GPOS kern as now; (c) `KERN_FIX[font]` manual pairs for what the font lacks: `serif-italic ('r','periodcentered') +40`, and the same for `f v w y` before the dot (italic `r` overhangs its advance +36, the dot's sidebearings are 0/−11: "developer · scraping" sets 123 units left of the dot, 181 right); (d) synthetic spaces: U+2009 thin = 0.20 em, U+200A hair = 0.10 em, U+00A0 = space advance, none of them present in any of the three families; (e) **tracking is added between two inked glyphs only**, never after a space or a synthetic space. `cap()`'s 1.8 px on a 600-unit space made "BENJAMIN S.  RUSSELL" three words.

**Roles.** `text(s, x, y, role="label", fill=None, anchor, within=None, semantic=True, edition=None)`; `font`/`size` remain as keyword overrides for texture, and any override off `SCALE` fails the lint. `ROLES[edition][role] -> (font, size, tracking, case, grade)`; `edition` comes from the Theme (T1). `grade` emits on the enclosing `<g>`: day `stroke=fill stroke-width=.22 paint-order=stroke stroke-linejoin=round`, night `stroke=paper stroke-width=.18`. On the `<g>` it inherits to every `<use>`, so defs stay shared; grade never animates.

**Mixed runs.** `runs([(role, text), ...], x, y)` sets figures inside a serif sentence in Condensed at 0.86× the serif size (no `onum` in Instrument Serif, verified on the full font; lining figures sit at 730 over 720 caps).

**Hand-kern.** `HAND_KERN["display"] = {("R","u"): -20, ("s","s"): +2}` units, plus `dy` −1.5 px on the second `l` of Russell; role `display` only (per 07, 28).

**Soundings.** `sounding(value, x, y, sub=None, truth="measured"|"illustrative"|"datum", role="texture", anchor="middle")`: digits via `text_use` in Condensed Regular or Italic; `sub` rendered with the encoded subscript glyphs U+2080–2089 (real `subs` forms; fallback: 0.6× digits shifted −0.15 em if a cut lacks them); `datum` draws the underline across `text_width`. Registers the run `semantic=False` unless `role="label"`.

**Text on path.** `text_on_path(s, polyline, role, start=0.0, side="above", spread=None)`: cumulative arc length over the polyline (T6's contour polylines, same data as the drawn contour), each glyph placed at its advance midpoint with `<use transform="translate(x y) rotate(a)">`; `spread` letterspaces to a fraction of a feature's long axis (`sea-name` 70%). Guard: local radius ≥ 3× size, else a straight run and a warning. First uses: one `sea-name`, `UNSURVEYED`.

**Run registry and lint.** `_EXTENTS` becomes `_RUNS: list[Run(text, role, font, size, x0, x1, y, angle, semantic, within)]`, rotated runs recording their rotated bbox. `check_type(edition) -> list[str]` fails on: size off the edition's scale; semantic run with `size × 0.68 < 9` (desktop) or `size × 0.5 < 9` (phone); an 11 px run not made by `sounding()` (per 33); serif below 17; a run leaving its `within` box (the caption over sounding 19, per 01, 33); a second `label-caps` run; tracking on a space. `build_assets.py` exits 1 on these; `check_bounds` reads `_RUNS`.

**Glyph budget and `<use>`.** Glyph ids stay `(font, size, codepoint)`; grade lives on the group so ids never multiply. Every role ≤ 28 goes through `text_use` (24 place names ≈ 290 placements, ≈ 60 unique glyphs); roles ≥ 36 are inline paths with integer coordinates (`_ntos0`, threshold moved from 40 to 36). Budget per sheet: ≤ 160 glyph defs, ≤ 40 KB, ≤ 6 size keys. Today: hero 94 / 24 KB / 5 keys, all off-scale (9, 9.5, 10, 11, 11.5); approaches 128 / 39 KB / 6.

**Fonts to vendor** (OFL, from google/fonts @ `5e8a3ba`):

```
ofl/ibmplexsanscondensed/IBMPlexSansCondensed-Regular.ttf  -> scripts/fonts/  key "cond"
ofl/ibmplexsanscondensed/IBMPlexSansCondensed-Italic.ttf   ->                 key "cond-italic"
ofl/ibmplexsanscondensed/IBMPlexSansCondensed-Light.ttf    ->                 key "cond-light"   (night)
ofl/ibmplexmono/IBMPlexMono-Light.ttf                      ->                 key "plex-light"   (night)
```

`scripts/fonts/subset.sh`, run once, committed:

```
pyftsubset SRC --unicodes='U+0020-007E,U+00A0,U+00B0,U+00B7,U+00D7,U+00E9,U+2009-200A,U+2013-2014,
  U+2018-2019,U+201C-201D,U+2022,U+2026,U+2032-2033,U+2080-2089,U+2190-2193,U+2197,U+2212,U+2588,U+2591,U+2713'
  --layout-features='kern,liga,subs,sups' --glyph-names --no-hinting --desubroutinize --output-file=DST
```

Trial: Condensed Regular 23.4 KB / 140 glyphs with `liga, subs, sups` and all ten subscript digits; Mono Light 13.8 KB. Re-subset Instrument Serif with the same flags so `kern`/`liga` survive by design, not luck. Add `LICENSE-IBMPlexSansCondensed.txt`.

### 2.4 Measured collision fixes

| Symptom | Cause (units/1000 em) | Fix |
|---|---|---|
| "developer· scraping" | see shaping (c) | `KERN_FIX` + thin spaces round `·` |
| "fire", "flight" f over the i-dot | italic `f` overhangs +131; no `liga` | shaping (a) |
| soundings "1●, 2●" | mono dotted zero, 118×124 units | Condensed zero (open counter, measured) |
| night italic names "dashed grey" | 37-unit hairline at 0.26 px | serif floor 17, night choke, `ink2` |
| caption leaves the cartouche | no container check | `within=` + lint |
| soundings pile at the fan origin; ring cuts a name | cullers have no text bbox | `exclusions()` from `_RUNS`; cull at ≥ 28 px (per 33) |

## 3. Interfaces

**Provide.** `svgkit.text(s, x, y, role=…, within=…, semantic=…)`, `text_use` (same signature, defs path), `runs([...])`, `sounding(value, x, y, sub, truth, role)`, `text_on_path(s, polyline, role, start, side, spread)`, `text_width(s, role=…)`, `exclusions() -> list[bbox]`, `check_type(edition) -> list[str]`, `glyph_count()`; tables `SCALE`, `SCALE_PHONE`, `ROLES`, `HAND_KERN`, `KERN_FIX`, `chartlib.LETTERING`. Font keys: `serif`, `serif-italic`, `cond`, `cond-italic`, `cond-light`, `plex`, `plex-light`, `plex-medium`.

**Need.** T1: `Theme.edition ∈ {day, night, phone-day, phone-night, reduced}` from `tokens.py`; `build_assets` fails on `check_type`. T6: contour polylines `list[(x, y)]` with named index levels, for `text_on_path` and figures in line breaks (I return the run bbox, T6 breaks the line). T7: per value, `truth`, the subscript meaning, the `stats.json` keys feeding `sounding()`. T2/T3/T9: all text through roles; one `label-caps` run chosen per sheet; the log in `machine` 13 (14.5 is off-scale: amend spec-supporting), phone log 26. T4: `appear()` wraps the graded `<g>`. T8: the legend sentence and a colophon line naming three faces. T10: `check_type` in CI, OCR of semantic runs at 360 px, a throwaway-repo check that `paint-order` survives camo.

## 4. Build order, effort, risks, omissions

1. Vendor, subset script, licences (1 h). 2. `shape()`: liga, kern, `KERN_FIX`, synthetic spaces, tracking rule, tests on the three collision strings (3 h). 3. `ROLES`/`SCALE`, `text(role=)`, grade (3 h). 4. `_RUNS`, `within`, `check_type`, exit code (2 h). 5. `sounding()` (1.5 h). 6. `text_on_path` (3 h). 7. `HAND_KERN` (0.5 h). 8. Migrate chartlib/common, delete `cap()` tracking, Inter, DejaVu (3 h). **≈ 17 h.**

Risks: the class-kerning loader is greedy (`setdefault`) and may mis-pair the condensed cut; validate ten pairs against `hb-shape`. `paint-order` is SVG2, fine in Chromium/Firefox/WebKit, unverified through camo; fallback is a second `<use>` group stroked behind the fill. Tight contours bend glyphs badly; the radius guard covers it.

Left out: small caps (no `smcp`; scaled caps lose weight), old-style figures (no `onum`), optical sizes (none exist; grade is the substitute), hinting, variable fonts, mono kerning (none, correctly), the 4° slant (decision 6).

## 5. Acceptance criteria

1. `build_assets.py` exits 1 on: a size off `SCALE`/`SCALE_PHONE`; a semantic run under 9 px at ×0.68 (desktop) or ×0.5 (phone); an 11 px run bypassing `sounding()`; serif under 17; a run leaving its `within` box.
2. `grep -c 'g-plex-' assets/hero-light.svg` returns 0; soundings are `g-cond-11-*`; the hero has ≤ 160 glyph defs and ≤ 6 size keys.
3. "fire" in a serif run shapes to `glyph00056` (fi); `text_width("A B") == text_width("A") + space + text_width("B")` (no tracking on spaces).
4. "developer · scraping" sets with left and right gaps within 10 units of each other at the dot.
5. Every sheet has exactly one `label-caps` run besides the chart number.
6. Day: every serif group ≤ 28 px carries `paint-order="stroke" stroke-width=".22"`; night: `.18` in paper; night `label`/`machine` ids are `g-cond-light-*` / `g-plex-light-*`.
7. The legend carries the lettering sentence of decision 11 verbatim; the colophon names three faces.
8. OCR recovers every `semantic=True` run at 360 px (phone editions) and at 870 px day (desktop).
9. `scripts/fonts/`: Instrument Serif ×2, Plex Sans Condensed ×3, Plex Mono Regular/Medium/Light/Italic, OFL files, `subset.sh`; no Inter, no DejaVu.
