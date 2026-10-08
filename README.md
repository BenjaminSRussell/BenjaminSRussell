<!-- Sheets are redrawn nightly from assets/stats.json by scripts/build_assets.py and published to the `chart` branch. Text between x:start and x:end marker comments is written by scripts/render_readme.py; edit chart.toml, not this file, for those lines. -->

<a name="top"></a>
<!-- picture:hero:start -->
<picture>
<source media="(max-width: 767px) and (prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-phone-still-night.svg">
<source media="(max-width: 767px) and (prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-phone-still-day.svg">
<source media="(max-width: 767px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-phone-night.svg">
<source media="(max-width: 767px)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-phone-day.svg">
<source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-still-night.svg">
<source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-still-day.svg">
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-night.svg">
<img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-day.svg" width="100%" alt="Chart of Ben Russell's 21 repositories, titled: I survey a web that is wrong about itself. Right margin unsurveyed. A boat sails in and anchors.">
</picture>
<!-- picture:hero:end -->
<sub>One feature per public repository, area by commits. The chart number is the public repository count; the edition is the rustmapper release.</sub>

<p align="center">
  <a href="https://github.com/BenjaminSRussell/Rust-sitemap"><b>rustmapper</b></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/BenjaminSRussell/Scrapy"><b>Scrapy Harbor</b></a>
  &nbsp;·&nbsp;
  <a href="https://pypi.org/project/rustmapper/">PyPI</a>
  &nbsp;·&nbsp;
  <a href="mailto:benjamin.sheldon.russell@gmail.com">Email</a>
  <!-- contact:start — set linkedin / resume in chart.toml [contact]; "" drops the slot -->
<!-- contact:end -->
  &nbsp;·&nbsp;
  <a href="DESIGN.md">How it's built</a>
</p>

<!-- position:start — chart.toml [position] text; "" omits the line -->
<!-- position:end -->

| At a glance | |
|---|---|
| **Ben Russell builds** | crawl and data infrastructure: web crawlers, discovery pipelines, raw-first storage, the dashboards that watch them |
| **Languages** | Python, Rust; Swift, C, TypeScript, Go |
| **Stack** | Delta Lake, PostgreSQL, Redis, Parquet · Docker, Kubernetes, Prometheus, Grafana, GitHub Actions · tokio, redb, maturin |

Most of what I build is survey work. The sitemap and the site disagree, and the subdomains nobody links to appear in neither, so the crawlers go and take soundings, one measured depth at a time, instead of trusting what the site declares. The storage keeps the raw log, so any depth can be checked again, and a dashboard says where the boat is while that still matters. I care how the work looks for the same reason I care that it holds.

<br>

<a name="soundings"></a>
## Soundings <sub><i>stats</i></sub>

<!-- picture:soundings:start -->
<picture>
<source media="(max-width: 767px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/soundings-phone-night.svg">
<source media="(max-width: 767px)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/soundings-phone-day.svg">
<source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/soundings-still-night.svg">
<source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/soundings-still-day.svg">
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/soundings-night.svg">
<img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/soundings-day.svg" width="100%" alt="Tide table of commits: high water 358, week of 5 Oct, Data Science Bank; low water 0; typical week 0. Below, one line per repository.">
</picture>
<!-- picture:soundings:end -->
<!-- figures:start -->
<sub><!-- n:commits -->1,665<!-- /n --> commits of mine · <!-- n:all_hands -->1,966<!-- /n --> all hands · <!-- n:repo_count -->21<!-- /n --> repositories surveyed · since <!-- n:account_since -->Oct 2024<!-- /n --> · soundings taken <!-- n:taken -->7 Oct 2026<!-- /n --></sub>
<!-- figures:end -->

<br>

<a name="approaches"></a>
## Approaches <sub><i>main projects</i></sub>

One sheet, read from seaward. rustmapper goes out first and finds the coastline. Scrapy Harbor, to the west, is where a crawl is run and kept. The channel between them is charted as proposed; nothing runs it yet.

<!-- picture:approaches:start -->
<picture>
<source media="(max-width: 767px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/approaches-phone-night.svg">
<source media="(max-width: 767px)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/approaches-phone-day.svg">
<source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/approaches-still-night.svg">
<source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/approaches-still-day.svg">
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/approaches-night.svg">
<img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/approaches-day.svg" width="100%" alt="Sheet 3, Approaches: rustmapper's survey ground east, buoyed channel west into Scrapy Harbor, every symbol in the legend. The soundings fill in behind the vessel.">
</picture>
<!-- picture:approaches:end -->
<sub>Soundings in URLs. The legend on this sheet defines every symbol used on the page and says which figures are measured.</sub>

**[rustmapper](https://github.com/BenjaminSRussell/Rust-sitemap) is the survey vessel:** a concurrent sitemap crawler written in Rust and shipped to [PyPI](https://pypi.org/project/rustmapper/) as a Python package. Edition <!-- n:edition_version -->0.1.3<!-- /n -->, <!-- n:edition_date -->8 Nov 2025<!-- /n -->, provisional.

- The throttle watches the database, not the network: a governor reads redb commit latency every 250 ms and grows or shrinks the worker pool between 256 and 1,024 permits, so the crawl slows when it cannot persist what it found.
- Every frontier event is written to a CRC32-framed write-ahead log (rkyv, zero-copy replay) before it reaches redb; a killed crawl resumes at the last record.
- The frontier is rendezvous-hashed by registrable domain, one shard per core, so a host's queue lives in one place; robots.txt is read first and its crawl-delay honoured. Optional Redis for distributed runs.
- Seeds from sitemaps, Certificate Transparency logs and the Common Crawl index: what a site says about itself, every host that ever held a certificate, and every URL someone once linked.
- Rust CLI and a Python package built with maturin. Prebuilt wheel for Apple silicon on CPython 3.13; elsewhere `pip` builds from source and needs a Rust toolchain.

```sh
pip install rustmapper
rustmapper crawl --start-url <your-site>
rustmapper export-sitemap --data-dir ./data --output sitemap.xml
```

**[Scrapy Harbor](https://github.com/BenjaminSRussell/Scrapy) is where a run is operated:** a multi-stage crawl platform built on the Scrapy framework.

- A scout spider goes first; analysis and summarization workers follow, each its own mark in the channel.
- Raw pages land in Delta Lake and stay raw: typed Arrow schemas per table, schema evolution by merge, partitions by domain, OPTIMIZE and VACUUM from a maintenance queue. Metrics in PostgreSQL, queues in Redis.
- Duplicates caught by URL hash and MinHash; summaries from BART-large-CNN on the worker itself, so nothing leaves the harbor for an API.
- Prometheus metrics on Grafana dashboards. Circuit breakers wrap the HTTP, Delta Lake and Redis services; per-host throttles are separate. Docker Compose and a Helm chart for Kubernetes.

<br>

<a name="log"></a>
## Ship's log <sub><i>how a run is kept</i></sub>

<!-- log_lede:start -->
A rustmapper run as the log would record it, entered the way a log is kept. The figures are computed from the crawler's own settings, not yet measured; the day I record a real session this page sets them upright by itself.
<!-- log_lede:end -->

<!-- picture:log:start -->
<picture>
<source media="(max-width: 767px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/log-phone-night.svg">
<source media="(max-width: 767px)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/log-phone-day.svg">
<source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/log-still-night.svg">
<source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/log-still-day.svg">
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/log-night.svg">
<img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/log-day.svg" width="100%" alt="Ship's log, rustmapper 0.1.3: 10 entries, 1402 to 1550, 12,440 URLs on 1 host, computed from settings, unsigned. Types once; only the cursor keeps time.">
</picture>
<!-- picture:log:end -->
<sub>Entered from <a href="assets/log.json">assets/log.json</a>.</sub>

<br>

<a name="notices"></a>
## Notices to mariners <sub><i>five principles</i></sub>

Figures correct themselves nightly. These five I had to be told.

<!-- notices:start -->
1. **Boring under load.** The system worth having is the one still running after you have stopped watching it. *Scrapy Harbor, Sep 2025: breakers on the Delta Lake, Redis and HTTP services.*
2. **Keep the log. Raw before clean.** The question you will want next month is one you cannot ask today, so the raw layer is appended to and never overwritten. *Scrapy Harbor, Sep 2025, the Delta Lake tables; rustmapper, Oct 2025, the write-ahead log.*
3. **Lights before speed.** A crawler you cannot watch is a crawler you cannot trust; dashboards go in version one. *Scrapy Harbor, Sep 2025: Prometheus and Grafana.*
4. **Parse, don't pattern-match.** *ideal-url-organizer, Nov 2025.*
5. **The surface is part of the system.** A tool that confuses its operator is already failing. *This page, Nov 2025: its earlier editions read as a template.*

<sub>Notices 6–9, editions: [rustmapper 0.1.0](https://pypi.org/project/rustmapper/0.1.0/) · [rustmapper 0.1.1](https://pypi.org/project/rustmapper/0.1.1/) · [rustmapper 0.1.2](https://pypi.org/project/rustmapper/0.1.2/) · [rustmapper 0.1.3](https://pypi.org/project/rustmapper/0.1.3/) · *8 Nov 2025*.</sub>
<!-- notices:end -->

Found a wrong depth? [Open an issue](https://github.com/BenjaminSRussell/BenjaminSRussell/issues/new); corrections are entered as notices.

<br>

<a name="other-waters"></a>
## Other waters <sub><i>smaller projects</i></sub>

- [**Elusive_trades_data**](https://github.com/BenjaminSRussell/Elusive_trades_data) — HVAC parts search across several supplier APIs, part numbers matched by zero-shot classification. File-based: no database, no Docker, no passwords.
- [**ideal-url-organizer**](https://github.com/BenjaminSRussell/ideal-url-organizer) — 25+ ways to sort a pile of URLs: by domain, crawl depth, subdomain, actual page content. Home of the "no regex" rule.
- [**go_go_go**](https://github.com/BenjaminSRussell/go_go_go) — the Go sibling of rustmapper: 256-worker pools, a Bloom filter sized for 100M+ URLs, the same three seed sources.
- [**rust_llm_logger**](https://github.com/BenjaminSRussell/rust_llm_logger) — a non-buffering reverse proxy for LLM servers, in Rust. A stream-tee forwards tokens to the client while parsing them for metrics, so logging costs the caller nothing.
- [**mlx_Qwen_data_entry**](https://github.com/BenjaminSRussell/mlx_Qwen_data_entry) — Qwen-DBA: profiles database workloads and has Qwen, on Apple MLX, recommend optimizations, with a human in the loop.
- [**Ai_code_detector**](https://github.com/BenjaminSRussell/Ai_code_detector) — probabilistic forensics for AI-generated code across seven languages, from stylometry down to git-history patterns.

<details>
<summary><b>Below the waterline</b> · 15 more repositories: Swift widgets, a C game engine, games, tooling</summary>
<br>

- [**3d-swift-globe-widget**](https://github.com/BenjaminSRussell/3d-swift-globe-widget) — Titan: a native macOS 3D globe in MapKit and SwiftUI, permanent night mode, packets arcing from NYC to LA.
- [**Spotify_to_apple_music**](https://github.com/BenjaminSRussell/Spotify_to_apple_music) — library migration in both directions, matching on ISRC first and on fuzzy text and duration after. A SwiftUI face and a CLI.
- [**game_engine**](https://github.com/BenjaminSRussell/game_engine) — a voxel engine in C with its own physics. The kind of thing you build to learn why engines are hard.
- [**cozy-game**](https://github.com/BenjaminSRussell/cozy-game) — Cozy Haven, a farming game in React Native and Expo.
- [**Data_science_dev**](https://github.com/BenjaminSRussell/Data_science_dev) — Data Science Tycoon, a browser game: climb from data-entry clerk to Chief Data Officer by making charts your boss rates out of five.
- [**Wheel**](https://github.com/BenjaminSRussell/Wheel) — a Three.js prize wheel with a physics-based spin and an LED rim. Lands on a programming language.
- [**FashionDB**](https://github.com/BenjaminSRussell/FashionDB) — scrapes Reddit and the web for fashion rules and runs them through an NLP pipeline.
- [**Data-visualizer**](https://github.com/BenjaminSRussell/Data-visualizer) — a lightweight, Superset-inspired exploration UI over PostgreSQL. Display only, by design.
- [**ggml-viz**](https://github.com/BenjaminSRussell/ggml-viz) — ggml graph and tensor visualization.
- [**Boxalarm-monorepo**](https://github.com/BenjaminSRussell/Boxalarm-monorepo) — infrastructure, UI and backend in one repository.
- [**excel-and-vba**](https://github.com/BenjaminSRussell/excel-and-vba) — spreadsheet automation.
- Also: [3d-swift-widget](https://github.com/BenjaminSRussell/3d-swift-widget) · [2d-swift-widgets](https://github.com/BenjaminSRussell/2d-swift-widgets) · [MLX_convertion](https://github.com/BenjaminSRussell/MLX_convertion) · [Course_crusader](https://github.com/BenjaminSRussell/Course_crusader)

</details>

<br>

<a name="instruments"></a>
## Instruments <sub><i>languages and stack</i></sub>

Python and Rust most days; Swift, C, TypeScript and Go when the work asks for them. Built on Apple silicon.

<!-- picture:instruments:start -->
<picture>
<source media="(max-width: 767px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/instruments-phone-night.svg">
<source media="(max-width: 767px)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/instruments-phone-day.svg">
<source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/instruments-still-night.svg">
<source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/instruments-still-day.svg">
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/instruments-night.svg">
<img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/instruments-day.svg" width="100%" alt="Instruments carried, 18 fittings in three columns: languages, stores and queues, deck; dated by first commit. Bold: underway this quarter; the rest when asked.">
</picture>
<!-- picture:instruments:end -->
<!-- instruments:start -->
<sub><b>Languages</b> Python · Rust · Swift · C · TypeScript · Go &nbsp;&nbsp; <b>Stores and queues</b> Delta Lake · PostgreSQL · Redis · Parquet and Arrow · redb and WAL · fastbloom &nbsp;&nbsp; <b>Deck</b> Prometheus and Grafana · Docker and Kubernetes · GitHub Actions · tokio · maturin and PyPI · MLX and Qwen</sub>
<!-- instruments:end -->

<br>

<a name="colophon"></a>
<details>
<summary><b>Colophon</b> · how the sheets are drawn: type, editions, motion, variation, license</summary>
<br>

- **Type.** Instrument Serif for titles and the italic asides; IBM Plex Sans Condensed for names and notes; IBM Plex Mono for soundings, labels and the log. Set as outlines in every sheet, so they look the same on every machine.
- **Editions.** Navy ink on cream paper by day; after dark, a night sheet on which the lights are the brightest things. Your system picks the edition through `<picture>`; a phone gets a sheet redrawn for its width, and a request for reduced motion gets every sheet finished and still.
- **Motion.** SMIL only, and slow. The boat sails in once in the first half-minute and anchors; after that only the lights keep time.
- **Variation.** The compass rose's inner ring is a 24-hour clock of my commits, counted in my own timezone; the arrow points at the busiest hour. That is the variation.
- **Figures.** Upright numerals are measured; italic numerals are not; an underlined figure is above datum. The chart number includes this repository; the chart is one of the things it charts.
- **Build.** [`scripts/build_assets.py`](scripts/build_assets.py) draws every sheet from the day's figures, which [`scripts/build_stats.py`](scripts/build_stats.py) surveys each morning, and [`scripts/check.py`](scripts/check.py) refuses to publish a sheet that breaks a rule. Conventions, tokens and the motion spec are in [DESIGN.md](DESIGN.md).
<!-- license:start -->
- **License.** Code MIT; sheets and copy CC BY 4.0; fonts under their own licenses in [`scripts/fonts/`](scripts/fonts/). To draw your own, fork the repository, fill in `chart.toml` and run the workflow; the sheets redraw from your repositories.
<!-- license:end -->

</details>

<br>

<!-- picture:footer:start -->
<picture>
<source media="(max-width: 767px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/footer-phone-night.svg">
<source media="(max-width: 767px)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/footer-phone-day.svg">
<source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/footer-still-night.svg">
<source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/footer-still-day.svg">
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/footer-night.svg">
<img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/footer-day.svg" width="100%" alt="Limit of survey: hatched ground beyond a dotted line, a sailboat anchored at it, 21 repositories charted. The chart ends here; the web doesn't.">
</picture>
<!-- picture:footer:end -->
