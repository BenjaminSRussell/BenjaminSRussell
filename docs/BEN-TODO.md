# What only you can do

The chart redraws itself weekly and on every push to `main`, but some facts are yours to set. Each item
says what changes on the page when you do it. Items marked ✓ were done in the redesign branch.

## Round 5 (9 Oct 2026, decisions D3 and D7): four asks

- **Fix the rustmapper README's worker figure.** The repository disagrees with itself: `governor.rs` says the pool
  runs 256–1,024 workers, the README says 32–512, the PyPI page says 256. Until the three agree, the page's
  first rustmapper bullet says only that the governor grows or shrinks the pool on redb commit latency, with no
  number. Make them agree (the code is the one to trust), then the figure returns to the bullet with the README's
  throughput figure beside it. (Item 5 below is the same ask for the sheet.)
- **The co-author line.** The page says what share of your commits carry an AI co-author trailer (63 on 9 Oct
  2026, about 3 %: default branches, trailers naming a model; GitHub's squash trailers that name you are not
  counted), and how many more commits coding agents wrote outright (Claude, jules), which are not counted as yours.
  Strike it if you'd rather not: delete the `agent_clause` item in `scripts/render_readme.py` `survey_block`.
- **Fill the position and contact slots.** `chart.toml [position] text` ("role · city or timezone · open to /
  currently") prints after the role line under the image; `[contact] linkedin` / `resume` add two links to the row
  under it. Both are empty and the page omits them (same ask as round 4, still open).
- **Which name to print: `rustmapper` or `Rust-sitemap`.** The page and the image letter the project `rustmapper`
  (the PyPI package name) and link to the `Rust-sitemap` repository. Say which you want printed; if you rename the
  repository to `rustmapper`, the two agree and `chart.toml` carries the old name as an alias.

## Round 4 (8 Oct 2026, decision D10): three asks

- **Fill the position and contact slots.** `chart.toml [position] text` is the one line a hiring manager
  came for ("role · city or timezone · open to / currently"); it prints after "Crawl and data
  infrastructure · Python and Rust" under the chart. `[contact] linkedin` / `resume` add the two links to
  the row under it. Both are empty today and the page simply omits them (item 2 below).
- **Record one real rustmapper run** on a host you may crawl, and commit it as `assets/log.json` with
  `measured: true`, `source: "session"` and `machine.cores` filled (item 7 below). Since round 4 nothing
  unmeasured is printed, so the page shows no crawl figures at all until there is a measured run; with one,
  it can show real URLs/s, hosts and WAL size.
- **Look at the three concept stills** on branch `concepts/round4` (the vessel in section, the waterfall,
  the survey lines), built from different premises than the archipelago, and say which one you would
  screenshot. That answer, not another review round, sets the direction.

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
