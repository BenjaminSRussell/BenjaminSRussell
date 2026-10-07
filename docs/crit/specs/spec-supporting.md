# Spec — the four supporting sheets (Soundings · Ship's log · Instruments · Limit of survey)

Conventions. Tokens: `scripts/design-tokens.json`. Easings: `settle` = `0.16 0.84 0.44 1`, `draw` =
`0.4 0 0.2 1`, `sea` = `0.37 0 0.63 1`. One-shots carry `fill="freeze"`. Semantic type ≥13px at 1280;
9–11px only as texture. Italic numerals = illustrative, upright = measured, defined once on the
Approaches legend; no caption repeats it. Every build passes the still-frame test (0/25/50/75/99%).

---

## A. SOUNDINGS — tide table strip, 1280×240

**Job.** One real graph on the page, read like the tide table printed in the margin of a harbour chart.

**Chrome (differs from hero: no neat-line, no minute bars).** Tide-table rules only: a 1.4px head rule
at y=24 and a 0.5px rule at y=28, both x=32..1248; a 0.8px foot rule at y=216. Nothing at the sides.
Head line, mono 13px tracking +1.2, upper: left at (48,48) `TIDE TABLE · COMMITS · LAST 52 WEEKS ·
DATUM: MAIN`; right-aligned at (1232,48) `REFRESHED {updated}`. Sheet number outside the rules,
bottom-right (1232,234) mono 13px muted: `No. {repos} · 2`.

**Hero figure.** `{commits}` Instrument Serif 96px, tracking −2, baseline (46,150). Caption
`lifetime commits` mono 13px muted at (48,176). It is the only serif on the sheet.

**Small figures**, mono 13px, two rows at x=330, baselines y=112 and y=138, value upright in ink then
label in muted: `24  public repos` / `46  followers` · `6  languages` / `since Oct 2024`. A 0.6px
vertical hair at x=306, y=88..146.

**Language depth-scale.** Bar x=48..520, y=196, h=6, stroked 0.6px, segments by `languages[].share`
in the ramp accent → ink → ink2 → muted → soft → hair. Labels under it at y=214, mono 13px:
`Python 46%  Rust 22%  Swift 13%  C 9%  TypeScript 6%  Other 4%` (swatch 7×7 before each name).

**Tide curve.** Plot x=572..1232, y=56..176 (h=120). Horizontal datum rules at 0, HW/2, HW (0.5px,
dash `1 4`), labelled in the right gutter at x=1236 mono 11px (texture): `0`, `{HW/2}`, `{HW}`.
Month ticks on the foot of the plot every 4–5 weeks from the week dates, labels mono 13px muted
(`O N D J F M A M J J A S`, one letter each, so they survive 68%). Curve: `chartlib.smooth_path` of
the 52 weekly points, stroke ink 1.4px; area fill ink at .08.
- **HW**: accent dot r=3.5 at the max week; label mono 13px accent `HW {n} · wk of {d Mon}`, placed
  left or right of the dot so it never leaves the plot.
- **LW**: hollow dot r=3 at the min *non-trailing* week; label mono 13px muted `LW {n} · wk of {d Mon}`.
- **Slack water**: the quietest 4-week window (lowest rolling sum): a 0.6px bracket under the plot
  base at y=180 spanning those weeks, labelled mono 13px muted `slack water`. Slack is relative; the
  bracket is drawn even when no week is zero.
- Caption under the plot (572,208) mono 13px muted: `{sum} contributions · 52 weeks · one week per step`.

**Data.** `build_stats.fetch` must store `weeks` as `[{"start":"2025-10-06","n":31}, …]` (first
`contributionDays[0].date` per week) instead of bare ints; the labels need dates. Repos/followers/
since/languages from stats.json as now.

**Fallback when `weeks` is absent (no placeholder).** `fetch_repodata.py` already clones each repo
bare (B1); have it write `repos[].weeks` = 52 weekly counts from `git log --date=short`. The tide is
then the per-week sum over repos: real commits, real dates, drawn exactly as above, with HW/LW/sum
numerals set **italic** (from clones, not GitHub's calendar). If even that is missing (first build),
spread each repo's `commits` evenly across `first..last`, every tide numeral italic. No caption either way.

**Motion (one-shot, 3.0 s, then frozen forever).**
| element | begin | dur | easing | how |
|---|---|---|---|---|
| datum rules + month ticks | present at t=0 | — | — | static chrome |
| curve | 0.3 s | 1.6 s | draw | `pathLength="1"`, dasharray 1, dashoffset 1→0 |
| area fill | 1.5 s | 0.65 s | settle | opacity 0→.08 |
| HW/LW dots + labels | 1.9 s / 2.05 s | 0.4 s | settle | opacity 0→1, translate y +3→0 |
| slack bracket | 2.2 s | 0.4 s | draw | pathLength draw |
| hero figure | 0.2 s | 0.4 s | settle | clip-rect rises; **opacity starts at .35 at t=0**, not 0 |
| small figures (4) | 0.5 s + i·0.12 | 0.4 s | settle | same rise |
| language segments (6) | 1.0 s + i·0.12 | 0.25 s | settle | width 0→w, left to right |
No loops. **Still-frame rule:** at t=0 the sheet shows head rule, head line, datum rules, month
ticks, captions and a ghosted hero figure; from 3.0 s it is the complete table.

**Alt.** "Tide table of commits, one week a step: high water {n} the week of {date}, low water
{n} the week of {date}, slack water in {month}. {commits} lifetime commits; {repos} public repos;
{followers} followers; since {since}. Depth scale by language: Python, Rust, Swift, C, TypeScript."

---

## B. SHIP'S LOG — 1280×440, ruled paper, no neat-line

**Paper.** A warmer stock: day `#F8EEDB`, night `#121C30` (one step warmer than the chart paper), full
bleed to the rounded sheet edge, **no frame rects at all**. Ruled lines 0.8px `hair` every 30px from
y=118 to y=418 (eleven rules). A red margin at x=120, 1px accent at .55 opacity, y=0..440 (bleeds).

**Header (static, present at t=0).** `Log of the rustmapper` Instrument Serif italic 30px at (136,64).
Right-aligned mono 13px muted at (1236,60): `SHIP'S LOG · {target} · {version}` → `SHIP'S LOG ·
EXAMPLE.COM · 0.1.3`. Column heads mono 13px tracking +1.2 upper, baseline y=100: `TIME` (44),
`POSITION · URLS` (136), `WIND · REQ/S` (330), `REMARKS` (460). Head rule under them is the first
ruled line (y=118), drawn 1px ink at .6 instead of hair.

**Columns.** TIME x=44, mono 13px muted. POSITION x=136 (w 170), mono 14.5px, numerals *italic*
(Plex Mono Italic vendored; it is the honesty convention). WIND x=330 (w 110), same, italic.
REMARKS x=460..1236, mono 14.5px ink; commands prefixed `$ ` in accent plex-medium. Rows at
y=132+30·i.

**Entries, verbatim** (`—` is an em dash in muted; `[bar]` is the crawl bar; `*…*` is italic):

| i | time | position | wind | remarks |
|---|---|---|---|---|
| 0 | 14:02 | — | — | `$ pip install rustmapper` |
| 1 | 14:02 | — | — | `Successfully installed rustmapper-0.1.3` |
| 2 | 14:03 | *1* | — | `$ rustmapper crawl --start-url example.com --workers 512 --seeding-strategy all` |
| 3 | 14:03 | *1* | — | `seeded · sitemap  ct  commoncrawl · frontier 16 shards · wal on · redis off` |
| 4 | 14:04 | *12,044* → *31,870* → *48,213* | *188* → *412* → *203* | `crawl under way  [bar]  512 in flight` |
| 5 | 14:05 | *48,213* | *203* | `remarks · nothing to report` |
| 6 | 14:06 | *48,213* | *41* | **Nothing on fire.** (Instrument Serif italic 17px, ink — the only serif in the body) |
| 7 | 14:08 | *48,213* | — | `$ rustmapper export-sitemap --data-dir ./data --output sitemap.xml` |
| 8 | 14:08 | *48,213* | — | `wrote sitemap.xml · 48,213 urls · 4m 12s` |
| 9 | 14:12 | | | `$ ▮` (cursor; the open line) |

Sign-off on the last rule, right-aligned at (1236,404), Instrument Serif italic 18px ink2:
`Entered by B.S.R. · watch ended 14:12`. The bar: x=460+17·cw, y=row−12, w=26·cw, h=10, track hair,
fill accent, square corners (it is a ruled paper, not a UI).

**Data — `assets/log.json`** (Ben pastes a real session; `measured:true` flips every numeral upright):
```json
{ "vessel":"rustmapper","version":"0.1.3","target":"example.com","date":"2026-10-07",
  "measured":false,"signoff":{"initials":"B.S.R.","time":"14:12"},
  "entries":[
   {"time":"14:02","position":null,"wind":null,"kind":"cmd","text":"pip install rustmapper"},
   {"time":"14:04","position":12044,"wind":188,"kind":"crawl","text":"crawl under way","inflight":512,
    "swaps":[{"at":1.0,"position":12044,"wind":188,"bar":0.28},{"at":3.8,"position":48213,"wind":203,"bar":1.0}]},
   {"time":"14:06","position":48213,"wind":41,"kind":"beat","text":"Nothing on fire."} ] }
```
`kind` ∈ `cmd` (typed, `$` prefix) · `out` · `crawl` (bar + swaps) · `remark` · `beat` (serif italic).
`build_assets.log()` lays out rows at 30px pitch and refuses >10 entries.

**Motion — one-shot, 14.4 s, `fill="freeze"` everywhere, only the cursor loops.**
- **t=0 already on paper:** stock, rules, red margin, header, column heads, and entry 0 complete
  (stamped and typed, static). The sheet is never a blank ledger.
- Stamps and `out` rows: opacity 0→1 + translate y 3→0, 250 ms, `settle`.
- **Typing (`cmd` rows):** per-character `<animate attributeName="opacity" values="0;1" calcMode="discrete">`
  on each glyph `<use>`, keyTimes jittered 50–90 ms per glyph (deterministic LCG seeded on row index),
  +160 ms after a space, +220 ms before each `--`. The cursor rect rides the same keyTimes with
  `attributeName="x" calcMode="discrete"`. Never a clip wipe.
- **Crawl bar:** width in three bursts, `0 0 .2 1`-style via `draw` then plateaus: 5.9→6.9 s to 28%,
  hold, 7.4→8.3 s to 62%, hold, 8.9→9.7 s to 100% (`settle`). POSITION and WIND numerals swap with
  discrete opacity at 6.9 / 8.3 / 9.7 s (three stacked `<g>`s, one visible).
- Schedule: e1 0.4 · e2 typed 1.0–5.0 · e3 5.3 · e4 5.9 (bursts to 9.7) · e5 10.1 · e6 10.9 (400 ms,
  `settle`) · e7 typed 11.2–13.4 (faster: 36–60 ms, the operator has done this before) · e8 13.6 ·
  e9 prompt + sign-off 14.0 (650 ms, `settle`).
- **Cursor:** `values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"`, begins at
  14.0 s. The one loop.
- **Still-frame rule:** every frame before 14.4 s is a log in progress (header + ≥1 full entry);
  every frame after is the complete log with a blinking prompt. No wipe, no reset.

**Alt.** "Ship's log, rustmapper 0.1.3, example.com. 14:02 installed. 14:03 crawl with 512 workers,
seeded from sitemaps, CT logs and Common Crawl, 16 shards, WAL on. 14:04 crawl under way.
14:05 remarks: nothing to report. 14:06 Nothing on fire. 14:08 sitemap.xml exported. Entered by B.S.R."

---

## C. INSTRUMENTS — equipment list strip, 1280×230

**Job.** The stack as a chart's instrument inventory: one line per fitting, bold = underway daily,
`fitted` = the first commit of the repo it is fitted in. Replaces the four-column legend entirely.

**Chrome (differs again).** No neat-line, no head rule. Three columns separated by two 0.6px
vertical rules at x=440 and x=856, y=40..200. Each column's group label is a **rotated marginal
note**: mono 13px tracking +2, upper, `rotate(-90)`, baseline at x=40 / 456 / 872, reading upward
from y=200: `LANGUAGES`, `STORES & QUEUES`, `DECK`. Foot line mono 13px muted at (60,222):
`bold · underway daily      fitted · first commit of the repo it serves`. Sheet number outside
everything, right-aligned (1236,222): `No. {repos} · 6`.

**Rows.** 6 per column, pitch 24px, baselines y=72..192. Row anatomy, left to right: name mono 14px
(`plex-medium` ink for the daily set, `plex` ink2 otherwise) at column x+20; dot leader (hair, 0.8px,
dasharray `1 4`, round caps) from name end +8 to the fitted column −8; fitted mono 13px muted
right-aligned at column x+372: `{YYYY-MM} · {repo}`.

| LANGUAGES | fitted | STORES & QUEUES | fitted | DECK | fitted |
|---|---|---|---|---|---|
| **Python** | 2025-09 · Scrapy | **Scrapy** | 2025-09 · Scrapy | **Docker · Kubernetes** | 2025-09 · Scrapy |
| **Rust** ⫽ | 2025-10 · Rust-sitemap | Delta Lake ⚓ | 2025-09 · Scrapy | Prometheus · Grafana ☆ | 2025-09 · Scrapy |
| Swift | 2026-01 · 3d-swift-widget | **PostgreSQL** | 2025-09 · Scrapy | GitHub Actions | 2025-11 · BenjaminSRussell |
| C | 2026-01 · game_engine | Redis | 2025-09 · Scrapy | tokio | 2025-10 · Rust-sitemap |
| TypeScript | 2025-12 · Data_science_dev | SQLite · GRDB | 2025-11 · Spotify_to_apple_music | SwiftUI · MapKit | 2026-01 · 3d-swift-widget |
| Go | 2025-11 · go_go_go | Parquet | 2025-09 · Scrapy | MLX · Qwen | 2025-11 · MLX_convertion |

Symbols: exactly three, and only the ones the Approaches legend defines — **track line** (`⫽`, three
short parallel hairlines) after Rust, **anchorage** (`⚓` outline) after Delta Lake, **light** (star
with flare, `☆` here) after Grafana. Drawn with the same chartlib glyphs as the Approaches sheet at
0.55 scale, ink2, 6px after the name. Nothing else gets a mark.

**Data.** A `FITTINGS` table in `build_assets.py` maps each name → repo; `fitted` = `stats.repos[name].first`
formatted `%Y-%m`. Missing repo → the fitted cell is left empty and the leader runs to the margin
(honest absence, no dash). Dates are measured, so upright.

**Motion (one-shot, 1.3 s).** Names, group labels and rules are present at t=0. Dot leaders draw
left→right with `pathLength="1"`, 400 ms `draw`, staggered 40 ms by row then column; fitted cells
`settle` in 250 ms on each leader's end. Frozen after 1.3 s; no loops.
**Still-frame rule:** t=0 is a finished inventory without leaders; t≥1.3 s is the sheet.

**Alt.** "Instruments carried. Languages: Python and Rust daily, Swift, C, TypeScript, Go. Stores
and queues: Scrapy and PostgreSQL daily, Delta Lake, Redis, SQLite, Parquet. Deck: Docker daily,
Prometheus and Grafana, GitHub Actions, tokio, SwiftUI, MLX. Fitted dates are each repo's first commit."

---

## D. FOOTER — "LIMIT OF SURVEY", 1280×270

**Geometry.** Single neat-line (1px ink .8) at x=14..1266, y=14..240, **broken on the right between
y=112 and y=226** where the water leaves the sheet. Water surface `hy=150`, 1.2px ink, from x=40 to
`edge=1040`; the drop `M1040,150 q14,2 18,16 v60`; three fall lines x=1046/1053/1060 dasharray `3 7`.
Swell: the existing repeated `q24,-5 48,0` wave at hy+9, 0.8px at .45.

**Limit of survey.** Vertical dotted line x=1000, y=30..226, 1px ink, dasharray `1 5`, round caps.
Rotated marginal label `rotate(-90)` mono 13px tracking +2 upper at x=992, reading upward from y=226:
`LIMIT OF SURVEY`. Beyond it, x=1000..1266 above the water (y=30..150) and the strip x=1120..1266 below
it: `hatch_defs(45°, spacing 6)` ink at .28 (day) / .22 (night) over `land`; label `UNSURVEYED`
upright mono 13px tracking +2 at (1130,72). Soundings-as-texture: six 11px mono numerals thinning
toward the limit (x=700..980, y=180..220, italic), none beyond it.

**Copy.** `The chart ends here. The web doesn't.` Instrument Serif italic 28px ink at (48,78). Micro-
caption mono 13px muted right-aligned against the limit line at (984,238): `surveyed to this line ·
beyond it, no data`. Chart number **outside the neat line**, mono 13px muted at (1264,258) anchor end:
`No. {repos}`; left of it at (16,258): `corrected through Notice 5`. Nothing else is written.

**Boat.** `chartlib.boat` at scale 1.0, hull on hy−1. Starts at x=90 at t=0 (never off-sheet).
- Approach: `animateTransform translate 90→980` (60px short of the edge), `dur=24s`, `settle`, freeze.
- Bob (loops, sea only, one 10 s period): rotate `-2.5;2.5;-2.5` and translate-y `0;-2;0` both
  `keySplines="sea;sea"`, `dur=10s`. Swell translates `0→-48` in 10 s with `sea` (water surges).
  Fall-line dashoffset and spray share the 10 s period so the footer counts as **one** ambient loop.
- Spray: seven droplets r=1.4 at `cx=1050+9i`, `cy` base 230 → apex 212 → base, keyTimes `0;.5;1`,
  `keySplines="0 0 0.58 1; 0.42 0 1 1"` (decelerate up, accelerate down: a parabola), `cx` drifts
  +8px linearly over the arc (ballistic horizontal is linear; this is the one allowed linear),
  durations 1.0–1.6 s staggered, restarted on the 10 s grid with `begin="0; sea10.end"` chains.

**Sea serpent (uncaptioned, silent).** One path, three cubic Béziers:
`M-130,0 c20,-26 40,-26 60,0 c20,-26 40,-26 60,0 c20,-26 40,-26 60,0`, stroke ink 2.2px round caps,
no fill, plus two eye dots r=1.6 at (−118,−14) and (−112,−14), in a `<g>` positioned at
`translate(880,150)` — 100px behind the boat's held position, between swell and hull in z-order.
Clipped by a rect y<150 so it emerges from the water. Motion per cycle (2.4 s): translate-y
`+30→0` 0.9 s `settle`, hold 0.6 s, `0→+30` 0.9 s `draw`; opacity .7.
`begin="arrive.end+72s; serpent.end+93.6s"` → first rise at 96 s, then every 96 s, phase-aligned with
the hero. Night: eyes in accent at .8; day: eyes ink.

**Day/night.** Day: paper `#F4EEE1`, hatch over `#E6DCC6`, spray ink .35, sail red. Night: paper
`#0F1A2B`, hatch over `#172740`, limit line ink .85 (the brightest hairline on the sheet), spray .5,
fall lines .6, sail orange. The neat-line break is identical.

**Still-frame rule.** t=0: boat at x=90, every line and word present. 0–24 s: boat under way.
≥24 s: boat held 60px short, bobbing, water over the edge, serpent only for 2.4 s in 96. There is
no frame without a boat, no seam, no reset.

**Alt.** "Limit of survey. A sailboat holds sixty pixels short of where the water leaves the sheet;
beyond the dotted line the paper is hatched unsurveyed. The chart ends here. The web doesn't.
Surveyed to this line; beyond it, no data. Something rises behind the boat now and then. Chart
No. {repos}, corrected through Notice 5."

---

## Summary
1. Soundings becomes a 1280×240 tide table: real 52-week curve with dated HW/LW and slack water, one 96px commits figure, mono ≥13px figures, depth-scale; a repo-clone fallback in italic replaces the placeholder; draws once, freezes at 3 s.
2. Ship's log is warmer ruled paper with a red margin and no frame; TIME/POSITION/WIND/REMARKS from `assets/log.json`; nine real-CLI entries with "nothing to report" then "Nothing on fire."; discrete typing, bursty bar, one-shot freeze, cursor the only loop, entry 0 present at t=0.
3. Instruments is a three-column equipment list with rotated group labels, dot leaders, bold daily drivers and a `fitted` column from real first-commit dates; only the three chart symbols the Approaches legend defines.
4. Footer is "Limit of survey": dotted limit line, hatched UNSURVEYED, water over a broken neat-line, parabolic spray, 24 s settle to 60px short with a sea bob, a silent serpent every 96 s, chart number outside the frame.
5. All four honour the conventions: italic = illustrative with no disclaimers, semantic type ≥13px, named easings only, distinct chrome per sheet, and no frame that is ever blank.
