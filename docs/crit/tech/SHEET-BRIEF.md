# Sheet brief — Phases 1–3 (three builders in parallel, one working tree)

Authority: docs/crit/tech/MASTERPLAN.md (wins; §2 decisions 1–29, §2.1 timeline, §3 contract, §7 gates) >
your lead's section (T2 hero · T3 approaches · T9 supporting) + the matching spec in docs/crit/specs/ >
panel documents (docs/crit/panel30, STANDARDS.md). T8-README.final.md is the copy source; T8-copy-notes.md
explains what was verified. Nothing in artwork may contradict the "verified facts" list in T8-copy-notes.md.

## The foundation you build on (read the reports first, then the source)
| Module | Report | What it gives you |
|---|---|---|
| scripts/tokens.py | — | Theme/THEMES, W, INK, DASH, SCALE, SCALE_PHONE, FLOORS, ROLES, GRADE, EASE, LOOP_PERIODS, QUANTUM, PAGE_PERIOD, BUDGETS. Never edit. |
| scripts/edition.py · build_assets.py · check.py | docs/crit/build/A-report.md | Edition, svg(), Ctx, sheet contract, build-report, check tiers, chart.toml |
| scripts/chartlib/ | docs/crit/build/B-report.md | Field, contours, water, place, symbols, furniture, Jitter. Text only via label callbacks. |
| scripts/data/ · assets/stats.json v2 · assets/log.json v2 | docs/crit/build/C-report.md | real survey numbers; the schema; what is measured vs computed |
| scripts/typeset.py | docs/crit/build/D-report.md | text/text_use/runs/sounding/text_on_path/text_width/exclude/begin_asset/run_records; truth marks |
| scripts/timeline.py | docs/crit/build/E-report.md | Timeline/NullTimeline, cue, fade_in, draw_in, reveal, typed, flash, sail, tack, fixes, every, report() |

`scripts/svgkit.py` is a facade re-exporting edition + typeset + timeline; `import svgkit as k` is fine, or import the
three modules directly. chartlib is imported as `import chartlib` (package).

## Sheet contract (build_assets.py — do not change it)
```python
NAME: str; KIND: "chart"|"strip"|"paper"|"edge"
SIZES = {"desk": (w, h), "phone": (w, h)}
BREAKS: list[tuple[str, str, str]]            # (what, how, why) — the deliberate rule-breaks you document
EDITIONS: list[str] | None                     # optional; default the six; hero adds HERO_EXTRA (phone-still-*)
def build(ctx) -> str                          # body SVG (no outer <svg>); ctx.ed ctx.data ctx.cfg ctx.tl ctx.k ctx.sheet ctx.log
                                               # ctx.no_sounding ctx.heartbeat ctx.stats_sha ctx.extra (dict you may fill for build-report)
def alt(data, cfg) -> str                      # ≤ 25 words, plain, from data
```
Sizes (MASTERPLAN §3.2): hero (1280,740)/(720,900) · soundings (1280,400)/(720,360) · approaches (1280,960)/(720,1240)
· log (1280,490)/(720,220) · instruments (1280,290)/(720,48) · footer (1280,270)/(720,320).
`ctx.tl` is a Timeline for the motion editions and a NullTimeline for still editions: one code path, `motion` decides.
Call `ctx.tl.cue("opening", 0, 4.0)` where the plan defines an opening; pass `still=` on every loop.
Everything you draw goes through the engines: chartlib for geometry, typeset for every glyph, timeline for every
`<animate*>`/`<set>`. No raw `<text>`, no hand-written SMIL, no `<pattern>`, no filters, no `animateMotion`.

## Non-negotiables (from MASTERPLAN §2, STANDARDS.md, T8-copy-notes)
- Honest: upright numerals = measured from stats.json; italic = illustrative; underline = above datum. No invented
  geometry presented as data. "512" is never upright (worker count disputed). No coverage figure anywhere.
  rustmapper does not feed Scrapy: the link is a proposed, unlit channel. Nothing from the banned-string list
  (scripts/checks/strings.py).
- Depth = count convention: contours 5/10/20/50 enclose ≤ n commits; tints B under 5, A under 10; features lift the
  field; feature area ∝ commits (±8 % at the 5-contour). One unit per sheet, stated on the sheet.
- Type: ROLES only, floors in sheet space (desk semantic 13 / texture 11 / serif 17; phone 26/18/30), exclusions
  registered for everything placed over the field, no collisions (typeset.check_type must be clean).
- Motion: §2.1 timeline is binding; only opacity and transform animate; 0.5 s grid; loop periods {1,4,10,15,96};
  only the footer is ambient; still edition = the t=95 s frame; every still is a finished sheet (§7.2).
- Night is designed, not inverted: lights are the brightest things; use THEMES["night"] values, NIGHT_LIGHT_CUTS.
- Phone editions are redrawn at SCALE_PHONE, not scaled: fewer soundings, bigger type, same story.
- Size budgets (§7.3): hero 170/60 KB, approaches 200/75, soundings 80/25, log 95/30, instruments 50/18, footer 40/12
  (raw/gz); ≤ 3000 elements; deterministic (two builds byte-identical).
- The legend lives on approaches: every symbol id used on hero/approaches/footer must come from chartlib.symbol_defs
  so the legend ↔ sheet `<use>` diff is empty.

## Ownership (write only inside your files; read anything; propose engine changes in your report)
- H (T2): scripts/sheets/hero.py · tests/test_hero.py
- P (T3): scripts/sheets/approaches.py · tests/test_approaches.py
- S (T9): scripts/sheets/soundings.py · log.py · instruments.py · footer.py · tests/test_supporting.py
Shared, read-only: every engine module, chart.toml (needs a key? say so in your report; the orchestrator adds it).
Do NOT run git add/commit/push. Do not edit docs/crit except nothing. Delete nothing.

## How to work
1. Read MASTERPLAN §2, §2.1, §3, §7; your T-doc and spec; the five build reports; then the engine source you call.
2. Build with `python3 scripts/build_assets.py --sheets <name> --out <scratch>/<name> --report <scratch>/<name>/build-report.json`
   (scratch = /tmp/claude-0/-home-user-BenjaminSRussell/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/crit/build/<letter>/).
   Only when it is right, build into assets/v9 (the default) so the orchestrator can run check.py on everything.
3. Look at it. Render with `node scripts/render.mjs frames|silhouette|phone` and
   `/tmp/claude-0/-home-user-BenjaminSRussell/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/tools/shot.mjs`; read the PNGs; iterate
   until it would survive the panel in docs/crit/panel30 (pick five critics and answer them in your head).
4. Gate yourself: `python3 scripts/checks/motion.py <svg>`, `python3 scripts/check.py --dev --tier fast`,
   `node scripts/perf_check.js --warm <s> <svg>` (budgets §7.3), `python3 -m unittest discover -s tests`.
5. Report to /tmp/claude-0/-home-user-BenjaminSRussell/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/crit/build/<letter>-report.md:
   what you built, the T-doc criteria table with pass/fail evidence, sizes and perf numbers per edition, deviations,
   what you need (chart.toml keys, engine fixes), and the PNG paths you inspected.
