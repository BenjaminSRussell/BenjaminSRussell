# What only you can do

The chart redraws itself nightly, but some facts are yours to set. Each item says what changes on the
page when you do it. Items marked ✓ were done in the redesign branch.

1. **Bio and profile fields.** Replace the GitHub bio with
   *"Crawl and data infrastructure, Python and Rust. The web is wrong about itself; I survey the part that isn't linked."*
   Set location, website and hireable; pin Rust-sitemap and Scrapy. Reuse the sentence as the repo
   description and the PyPI summary.
2. **Position line and contacts.** In `chart.toml`, set `[position] text = "role · city or timezone · open to / currently"`
   (an empty string omits the line; the build warns) and `[contact] linkedin` / `resume` (empty strings drop the slots).
3. ✓ **Licenses.** `LICENSE` (MIT, scripts) and `LICENSE-ASSETS.md` (CC BY 4.0, sheets and copy) exist; `snake.yml` and the
   Inter/DejaVu fonts are gone. Still yours: delete the old `output` branch on GitHub (the proxy refused the delete).
4. **Rust-sitemap release hygiene.** Add a LICENSE, tag `v0.1.3` at the published commit, write a GitHub Release.
   Until then the Notices fall back to the four PyPI uploads. Later: a maturin release workflow with abi3 wheels for
   Linux, macOS and Windows, cut 0.2.0, and add `repository_dispatch: release-published` to this repo so the edition
   line changes itself. Renaming to `rustmapper` is safe: `chart.toml` carries the alias.
5. **One worker figure.** `governor.rs` says 256–1024, the README 32–512, PyPI 256. Make them agree, then set
   `[claims.workers] measured = true` with the commit sha; the figure goes upright on the approaches sheet.
6. **Scrapy coverage.** Either gate CI at `--cov-fail-under=85` and publish the badge, or leave coverage off the page
   (today it is off everywhere, on purpose). Move the 930 self-filed issues to a Project.
7. **A real log.** Record one rustmapper session on a domain you control and commit it as `assets/log.json` with
   `measured: true`, `source: "session"`, `machine.cores` filled. The ship's log then sets its figures upright.
8. **A Scrapy trial export.** Commit one `exports/run-YYYY-MM-DD.json` (rows per Delta table, wall-clock, host,
   5xx rate, breaker trips); the harbour inset soundings become those counts, upright. Confirm the Prometheus
   `scrape_interval` (15 s global today) is the one you want as Grafana Lt's character.
9. **Archive the shelf.** Archive the four repositories you would not defend (3d-swift-widget, 2d-swift-widgets,
   MLX_convertion, Course_crusader); archived repos become wreck marks.
10. **go_go_go.** Make header rotation opt-in with an identifying default UA, or the page keeps calling it
    "browser-faithful fetching".
11. **Optional Notice 0.** "0.1.0/0.1.1 shipped without the engine; fixed that evening (8 Nov 2025)" turns the
    four releases in 74 minutes into a story.
12. **First live run.** After merging, run the `chart` workflow once by hand and read its summary: confirm the two
    commit totals (calendar vs clone-filtered) and 24 vs 21 repositories; add any fourth author identity string to
    `[identity]`. Upload the social preview PNG from `out/` once per design release.
