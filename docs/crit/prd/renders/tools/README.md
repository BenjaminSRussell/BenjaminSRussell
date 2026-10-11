# How the page screenshots under `docs/crit/prd/renders/` are made

Three scripts, copied from the session's `r6/tools/` (they are review tooling, not the product; `scripts/render.mjs`
renders single SVGs and its `matrix` mode is a placeholder).

- `preview_phone.mjs <README.md> <outDir> <repoRoot> [width=390]`: the README at a phone width, device scale 2, to
  `<outDir>/readme-<width>.png` (full page).
- `preview.mjs <README.md> <outDir> <repoRoot>`: a 1,280 px viewport, dark and light, to `readme-dark.png` and
  `readme-light.png`.
- `preview_mid.mjs <README.md> <outDir> <repoRoot> [width=1180] [height=820]`: a two-column viewport.

Each imports `marked` and `playwright` by absolute path in its first two lines; edit those to a local install
(`npm install marked playwright@1.49.1 && npx playwright install chromium`). `<repoRoot>` must hold a built
`assets/v9/hero-*.svg` (`python3 scripts/build_assets.py`), because the scripts rewrite the README's
`raw.githubusercontent.com/…/chart/` URLs to `file://<repoRoot>/`. A fixture page is rendered with
`python3 scripts/render_readme.py --readme <copy of README.md> --cfg <chart.toml> --stats <fixture stats.json>` first
(`once-1a`, `once-2b`, `once-2b-r3`).

The `page-phone-N.png` and `page-desk-N.png` files are the full-page PNGs cut every 1,700 px (850 CSS px at 2× on the
phone; 1,700 CSS px on the desk) with Pillow: `im.crop((0, y, w, y + 1700))` for `y` in steps of 1,700. The
`sheet-*.png` files are the SVG editions rendered at the column widths named in their file names (round-16's build).
