<!-- The hero is regenerated weekly from assets/stats.json by scripts/build_assets.py and published to the `chart` branch. Text between x:start and x:end marker comments is written by scripts/render_readme.py; edit chart.toml, not this file, for those lines. -->

<a name="top"></a>
<!-- picture:hero:start -->
<a href="https://github.com/BenjaminSRussell/Rust-sitemap">
<picture>
<source media="(max-width: 1199px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-phone-night.svg">
<source media="(max-width: 1199px)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-phone-day.svg">
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-night.svg">
<img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-day.svg" width="100%" alt="How to start Ben Russell's crawler rustmapper, what it does with each page, and how to stop it. It loops until one Ctrl-C writes data/sitemap.jsonl.">
</picture>
</a>
<!-- picture:hero:end -->

<p align="center">
  <!-- position:start — chart.toml [position] text; "" omits the slot -->
<!-- position:end -->
  <a href="https://github.com/BenjaminSRussell/Rust-sitemap"><b>rustmapper</b></a>&nbsp;· <a href="https://github.com/BenjaminSRussell/Scrapy"><b>Scrapy</b></a>&nbsp;· <a href="https://pypi.org/project/rustmapper/">PyPI</a>&nbsp;· <a href="mailto:benjamin.sheldon.russell@gmail.com">Email</a>
  <!-- contact:start — set linkedin / resume in chart.toml [contact]; "" drops the slot -->
<!-- contact:end -->
</p>

**Ben Russell builds** web crawlers, discovery pipelines, raw-first storage, and the dashboards that watch them.<br>
**Languages** Python, Rust; Swift, C, TypeScript, Go.<br>
**Stack** Delta Lake, PostgreSQL, Redis, Parquet · Docker, Kubernetes, Prometheus, Grafana, GitHub Actions · tokio, redb, maturin.

<!-- pick:start -->
**rustmapper** gives you a site's list of URLs from one binary, with no services to run. **Scrapy** keeps the pages themselves, deduplicated and summarised, in a pipeline that needs Docker.
<!-- pick:end -->

<!-- about:Rust-sitemap:start -->
**[rustmapper](https://github.com/BenjaminSRussell/Rust-sitemap)**: `pip install` gives you its command line; the Python API, built with maturin, is on main and not yet released.
<!-- about:Rust-sitemap:end -->

<!-- facts:Rust-sitemap:start -->
*On main at `32c2651`: built on tokio, redb, rkyv, reqwest, clap · 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust*
<!-- facts:Rust-sitemap:end -->

<!-- install:Rust-sitemap:start -->
```sh
pip install rustmapper
rust_sitemap crawl \
    --start-url <your-site>
# stop it with one Ctrl-C
# sitemap.xml, even after a kill:
rust_sitemap export-sitemap
```

Prebuilt for Apple silicon on CPython 3.13; elsewhere `pip` builds it from source, which needs a Rust toolchain (3 min from a cold cache on a 4-core Linux x86_64 machine).

It sends up to 20 requests at a time to one host, 256 in all, with no pause between them. 0.1.3 ignores `Crawl-delay`, and asks for `robots.txt` only over https, so a plain-http site's rules are not read. 0.1.3 writes one `sitemap.xml` however many pages it found; the sitemap format allows 50,000 URLs per file.
<!-- install:Rust-sitemap:end -->

<!-- handoffs:start -->
<!-- handoffs:end -->

**[Scrapy](https://github.com/BenjaminSRussell/Scrapy)** is a multi-stage crawl platform built on the Scrapy framework.

<!-- facts:Scrapy:start -->
*On main at `96e7a1a`: built on deltalake, redis, psycopg2, prometheus-client, datasketch · 1,920 tests · CI passed 8 Oct 2026 · MIT license · 69k lines of Python*
<!-- facts:Scrapy:end -->

```sh
# in a clone of this repository;
# start.py runs only from here
cd Scraping_project
# the whole pipeline (needs docker
# and docker-compose); it crawls a
# university's sample site
python start.py
# or only discovery, on your own site:
docker-compose run --rm scraper \
    scrapy crawl scout \
    -a allowed_domains=<domain> \
    -a start_urls=<url>
```

Grafana opens on `localhost:3000`. Spiders run by name (`scout`), not by file name.

- A scout spider goes first; analysis and summarization workers follow, each its own stage.
- Raw pages land in Delta Lake and stay raw: typed Arrow schemas per table, schema evolution by merge, partitions by domain, OPTIMIZE and VACUUM from a maintenance queue. Metrics in PostgreSQL, queues in Redis.
- Near-duplicates are dropped by URL hash and MinHash. Pages get an extractive summary in stage 3; documents over 50,000 characters go to stage 4, where bart-large-cnn runs on the worker itself, so nothing is sent to an external API.
- Prometheus metrics on Grafana dashboards. Each host has its own circuit breaker: after 5 URLs on it fail every retry, it is left alone for 60 s. Docker Compose and a Helm chart for Kubernetes.

<a name="also"></a>
**Also**

- [**ideal-url-organizer**](https://github.com/BenjaminSRussell/ideal-url-organizer) — 25 ways to sort a pile of URLs: by domain, crawl depth, subdomain, actual page content.
- [**go_go_go**](https://github.com/BenjaminSRussell/go_go_go) — rustmapper's counterpart in Go, with the same crawl, resume and export-sitemap commands. It adds headless-Chrome rendering, SQLite storage with full-text search, and browser TLS-fingerprint impersonation, all off by default.
- [**rust_llm_logger**](https://github.com/BenjaminSRussell/rust_llm_logger) — a non-buffering reverse proxy for LLM servers, in Rust. Each chunk is parsed for token counts and passed straight on, and the call is logged only after the client has its last byte.
- [**Ai_code_detector**](https://github.com/BenjaminSRussell/Ai_code_detector) — probabilistic forensics for AI-generated code, from stylometry down to git-history patterns.

<details>
<summary><!-- n:more_count -->15<!-- /n --> more repositories: Swift widgets, a C game engine, games, tooling</summary>
<br>

- [**3d-swift-globe-widget**](https://github.com/BenjaminSRussell/3d-swift-globe-widget) — Titan: a native macOS 3D globe in MapKit and SwiftUI, permanent night mode, packets arcing from NYC to LA.
- [**Spotify_to_apple_music**](https://github.com/BenjaminSRussell/Spotify_to_apple_music) — library migration in both directions, matching on ISRC first and on fuzzy text and duration after. A SwiftUI face and a CLI.
- [**game_engine**](https://github.com/BenjaminSRussell/game_engine) — a voxel engine in C with its own physics. The kind of thing you build to learn why engines are hard.
- [**cozy-game**](https://github.com/BenjaminSRussell/cozy-game) — Cozy Haven, a farming game in React Native and Expo.
- [**Data_science_dev**](https://github.com/BenjaminSRussell/Data_science_dev) — Data Science Tycoon, a browser game: climb from data-entry clerk to Chief Data Officer by making charts for your boss.
- [**Wheel**](https://github.com/BenjaminSRussell/Wheel) — a Three.js prize wheel with a physics-based spin and an LED rim. Lands on a programming language.
- [**FashionDB**](https://github.com/BenjaminSRussell/FashionDB) — scrapes Reddit and the web for fashion rules and runs them through an NLP pipeline.
- [**Data-visualizer**](https://github.com/BenjaminSRussell/Data-visualizer) — a lightweight, Superset-inspired exploration UI over PostgreSQL. Display only, by design.
- [**Elusive_trades_data**](https://github.com/BenjaminSRussell/Elusive_trades_data) — HVAC parts search across several supplier APIs, part numbers matched by zero-shot classification. File-based: no database, no Docker, no passwords.
- [**mlx_Qwen_data_entry**](https://github.com/BenjaminSRussell/mlx_Qwen_data_entry) — Qwen-DBA: profiles database workloads and has Qwen, on Apple MLX, recommend optimizations, with a human in the loop.
- [**excel-and-vba**](https://github.com/BenjaminSRussell/excel-and-vba) — spreadsheet automation.
- Also: [3d-swift-widget](https://github.com/BenjaminSRussell/3d-swift-widget) · [2d-swift-widgets](https://github.com/BenjaminSRussell/2d-swift-widgets) · [MLX_convertion](https://github.com/BenjaminSRussell/MLX_convertion) · [Course_crusader](https://github.com/BenjaminSRussell/Course_crusader)

</details>

<a name="rules"></a>
**Working rules**

<!-- notices:start -->
1. **Boring under load.** The system worth having is the one still running after you have stopped watching it. *Scrapy, Sep 2025: a circuit breaker in the error handler.*
2. **Raw before clean.** The question you will want next month is one you cannot ask today, so the raw layer is appended to and never overwritten. *Scrapy, Oct 2025, the Delta Lake tables.*
3. **Dashboards before speed.** A crawler you cannot watch is a crawler you cannot trust; dashboards go in version one. *Scrapy, Oct 2025: Prometheus metrics, then Grafana dashboards.*
4. **Parse, don't pattern-match.** A regex for a URL breaks on the first port or login inside it; `urllib.parse` does not. *ideal-url-organizer, Nov 2025: URLs split with `urllib.parse`.*
<!-- notices:end -->

Found a mistake? [Open an issue](https://github.com/BenjaminSRussell/BenjaminSRussell/issues/new).

<a name="data"></a>
<!-- survey:start -->
<sub>The [drawing](DESIGN.md) is rustmapper 0.1.3, the release pip installs; its commands were run, with seeding off, against a local 3-page site on 10 Oct 2026 (Linux x86_64). Tests and lines are counted per repository, whoever wrote them: coding agents (Claude, jules) authored 45 of rustmapper's 146 commits and 71 of Scrapy's 499.</sub>
<!-- survey:end -->

<!-- license:start -->
<sub>**This profile** Code MIT; images and text CC BY 4.0; fonts under their own licenses in [`scripts/fonts/`](scripts/fonts/).</sub>
<!-- license:end -->
