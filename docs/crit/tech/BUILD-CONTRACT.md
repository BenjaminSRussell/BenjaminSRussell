# Build contract — Phase 0b (five builders in parallel, one working tree)

Authority: docs/crit/tech/MASTERPLAN.md (wins) > your lead's section (T1/T4/T5/T6/T7) > panel documents.
Shared module already written: `scripts/tokens.py` (Theme, THEMES, W, INK, DASH, SCALE, SCALE_PHONE, FLOORS,
ROLES, GRADE, EASE, LOOP_PERIODS, QUANTUM, PAGE_PERIOD, BUDGETS). Import it; do not edit it (propose changes in
your report instead). Real data: `assets/stats.json` (v1, 21 repos). Fonts: `scripts/fonts/`.

## Facade plan (deviation from MASTERPLAN 3.1, so five people can work without merge conflicts)
`scripts/svgkit.py` becomes a thin FACADE that re-exports from three modules:
- `scripts/edition.py`  — Edition, svg(), id-prefixing, integer-coordinate helpers, `write()`, run registry glue  (owner A/T1)
- `scripts/typeset.py`  — the type engine: shape/text/text_use/runs/sounding/text_on_path/text_width/exclusions/exclude/check_type/glyph_count/FIGURES/begin_asset  (owner D/T5)
- `scripts/timeline.py` — Timeline and samplers (owner E/T4)
Owner A writes the facade LAST, after D and E report their exports. Until then nobody imports svgkit for new code;
import `edition`, `typeset`, `timeline` directly. The OLD svgkit functions stay available (sheets/_v8_reference.py uses them).

## Ownership (write only inside your files; read anything)
A (T1): scripts/edition.py · scripts/build_assets.py (sheet contract ctx, editions, build-report skeleton) ·
   scripts/render_readme.py · scripts/check.py (three-tier runner that discovers scripts/checks/*.py plug-ins) ·
   scripts/checks/{xml,size,strings,expiry,position}.py · chart.toml · .github/workflows/profile.yml + perf.yml ·
   .github/PULL_REQUEST_TEMPLATE.md · LICENSE · LICENSE-ASSETS.md · scripts/publish_chart.py (orphan-branch publisher,
   dry-run capable) · tests/test_edition.py · at the very end: scripts/svgkit.py facade.
B (T6): scripts/chartlib/ (package: __init__.py field.py water.py place.py symbols.py furniture.py) ·
   tests/test_chartlib.py · tests/fixtures/*.json you need. Text: NEVER import typeset; accept callables
   (`label_cb(text, x, y, role, **kw) -> str`) wherever text is drawn, and return bboxes/polylines the sheets need.
   Keep the old scripts/chartlib.py working by renaming it to scripts/chartlib_v8.py (update the import in
   sheets/_v8_reference.py) before creating the package.
C (T7): scripts/data/ (package: __init__ github.py survey.py pypi.py releases.py claims.py model.py logsim.py
   stats_schema.json log_schema.json) · scripts/build_stats.py (rewrite onto the package; `main(mode)`) ·
   scripts/fetch_repodata.py (identity filter, author-local hours, commit-days, weeks) · assets/log.json (v2,
   computed-consistent via logsim) · scripts/checks/{data,log}.py · tests/test_data.py. Run the survey for real
   (git clones work here) and write assets/stats.json v2 (no `seeded` key; `provenance.mode="cache"` is fine).
D (T5): scripts/typeset.py · scripts/fonts/ (vendor IBM Plex Sans Condensed Regular/Italic/Light + IBM Plex Mono
   Light from https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexsanscondensed/ and
   ofl/ibmplexmono/; re-subset Instrument Serif with kern,liga,subs,sups; delete Inter* and DejaVu*; write
   subset.sh; keep OFL texts) · scripts/checks/type.py · tests/test_typeset.py.
E (T4): scripts/timeline.py · scripts/checks/motion.py · scripts/perf_check.js (start from
   /tmp/claude-0/-home-user-BenjaminSRussell/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/perf/harness.js) ·
   scripts/render.mjs (frames via setCurrentTime, silhouette, phone, matrix) · tests/test_timeline.py.

## Rules
- Python 3.13, stdlib + fonttools only (no numpy/scipy). Node 22 + Playwright at /opt/node-tools/node_modules/playwright.
- Deterministic output: seeded `Jitter`, no time-dependent values except from stats.json.
- Do NOT run git add/commit/push. Do not edit files you do not own. Do not edit docs/crit.
- Tests: `python3 -m unittest discover -s tests -v` must pass for your files. Add `tests/__init__.py` if missing.
- When done, write `docs/../scratchpad`? No: write your report to /tmp/claude-0/-home-user-BenjaminSRussell/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/crit/build/<letter>-report.md
  with: what you built, public API (exact signatures), what you need from others, deviations from your lead's spec.
