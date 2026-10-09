<!-- The hero is regenerated weekly from assets/stats.json by scripts/build_assets.py and published to the `chart` branch. Text between x:start and x:end marker comments is written by scripts/render_readme.py; edit chart.toml, not this file, for those lines. -->

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
<img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-day.svg" width="100%" alt="Ben Russell's 22 repositories by week, Sep 2025 to Oct 2026: Scrapy and rustmapper busiest, quiet Feb to Apr 2026. The rest share one row.">
</picture>
<!-- picture:hero:end -->

<p align="center">
  <!-- position:start — chart.toml [position] text; "" omits the slot -->
<!-- position:end -->
  <a href="https://github.com/BenjaminSRussell/Rust-sitemap"><b>rustmapper</b></a>&nbsp;· <a href="https://github.com/BenjaminSRussell/Scrapy"><b>Scrapy</b></a>&nbsp;· <a href="https://pypi.org/project/rustmapper/">PyPI</a>&nbsp;· <a href="mailto:benjamin.sheldon.russell@gmail.com">Email</a>
  <!-- contact:start — set linkedin / resume in chart.toml [contact]; "" drops the slot -->
<!-- contact:end -->
</p>

**Ben Russell builds** crawl and data infrastructure: web crawlers, discovery pipelines, raw-first storage, the dashboards that watch them.<br>
**Languages** Python, Rust; Swift, C, TypeScript, Go.<br>
**Stack** Delta Lake, PostgreSQL, Redis, Parquet · Docker, Kubernetes, Prometheus, Grafana, GitHub Actions · tokio, redb, maturin.

**[rustmapper](https://github.com/BenjaminSRussell/Rust-sitemap)** is a concurrent sitemap crawler written in Rust, with a CLI and a Python package built with maturin. <!-- n:edition_version -->0.1.3<!-- /n --> on [PyPI](https://pypi.org/project/rustmapper/), <!-- n:edition_date -->8 Nov 2025<!-- /n -->.

<!-- facts:Rust-sitemap:start -->
*Built on tokio, redb, rkyv, reqwest, clap · 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust · last commit 8 Aug 2026*
<!-- facts:Rust-sitemap:end -->

- The throttle watches the database, not the network: a governor reads redb commit latency every 250 ms and grows or shrinks the worker pool, so the crawl slows when it cannot persist what it found.
- Every frontier event is written to a CRC32-framed write-ahead log (rkyv, zero-copy replay) before it reaches redb; a killed crawl resumes at the last record.
- The frontier is rendezvous-hashed by registrable domain, one shard per core, so a host's queue lives in one place; robots.txt is read first and its crawl-delay honoured. Optional Redis for distributed runs.
- Seeds from sitemaps, Certificate Transparency logs and the Common Crawl index: what a site says about itself, every host that ever held a certificate, and every URL someone once linked.

```sh
pip install rustmapper
rustmapper crawl --start-url <your-site>
rustmapper export-sitemap --data-dir ./data \
    --output sitemap.xml
```

- Prebuilt wheel for Apple silicon on CPython 3.13; elsewhere `pip` builds from source and needs a Rust toolchain.

**[Scrapy](https://github.com/BenjaminSRussell/Scrapy)** is a multi-stage crawl platform built on the Scrapy framework.

<!-- facts:Scrapy:start -->
*Built on deltalake, redis, psycopg2, prometheus-client, datasketch · 1,920 tests · CI passed 8 Oct 2026 · 69k lines of Python · last commit 8 Oct 2026*
<!-- facts:Scrapy:end -->

- A scout spider goes first; analysis and summarization workers follow, each its own stage.
- Raw pages land in Delta Lake and stay raw: typed Arrow schemas per table, schema evolution by merge, partitions by domain, OPTIMIZE and VACUUM from a maintenance queue. Metrics in PostgreSQL, queues in Redis.
- Duplicates caught by URL hash and MinHash; summaries from BART-large-CNN on the worker itself, so nothing is sent to an external API.
- Prometheus metrics on Grafana dashboards. Circuit breakers wrap the HTTP, Delta Lake and Redis services; per-host throttles are separate. Docker Compose and a Helm chart for Kubernetes.

<a name="also"></a>
**Also**

- [**ideal-url-organizer**](https://github.com/BenjaminSRussell/ideal-url-organizer) — 25+ ways to sort a pile of URLs: by domain, crawl depth, subdomain, actual page content. Home of the "no regex" rule.
- [**go_go_go**](https://github.com/BenjaminSRussell/go_go_go) — the Go sibling of rustmapper: 256-worker pools, a Bloom filter sized for 100M+ URLs, the same three seed sources.
- [**rust_llm_logger**](https://github.com/BenjaminSRussell/rust_llm_logger) — a non-buffering reverse proxy for LLM servers, in Rust. A stream-tee forwards tokens to the client while parsing them for metrics, so logging costs the caller nothing.
- [**Ai_code_detector**](https://github.com/BenjaminSRussell/Ai_code_detector) — probabilistic forensics for AI-generated code across seven languages, from stylometry down to git-history patterns.

<details>
<summary>15 more repositories: Swift widgets, a C game engine, games, tooling</summary>
<br>

- [**3d-swift-globe-widget**](https://github.com/BenjaminSRussell/3d-swift-globe-widget) — Titan: a native macOS 3D globe in MapKit and SwiftUI, permanent night mode, packets arcing from NYC to LA.
- [**Spotify_to_apple_music**](https://github.com/BenjaminSRussell/Spotify_to_apple_music) — library migration in both directions, matching on ISRC first and on fuzzy text and duration after. A SwiftUI face and a CLI.
- [**game_engine**](https://github.com/BenjaminSRussell/game_engine) — a voxel engine in C with its own physics. The kind of thing you build to learn why engines are hard.
- [**cozy-game**](https://github.com/BenjaminSRussell/cozy-game) — Cozy Haven, a farming game in React Native and Expo.
- [**Data_science_dev**](https://github.com/BenjaminSRussell/Data_science_dev) — Data Science Tycoon, a browser game: climb from data-entry clerk to Chief Data Officer by making charts your boss rates out of five.
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
1. **Boring under load.** The system worth having is the one still running after you have stopped watching it. *Scrapy, Sep 2025: breakers on the Delta Lake, Redis and HTTP services.*
2. **Keep the log. Raw before clean.** The question you will want next month is one you cannot ask today, so the raw layer is appended to and never overwritten. *Scrapy, Sep 2025, the Delta Lake tables; rustmapper, Oct 2025, the write-ahead log.*
3. **Lights before speed.** A crawler you cannot watch is a crawler you cannot trust; dashboards go in version one. *Scrapy, Sep 2025: Prometheus and Grafana.*
4. **Parse, don't pattern-match.** *ideal-url-organizer, Nov 2025.*
<!-- notices:end -->

Found a mistake? [Open an issue](https://github.com/BenjaminSRussell/BenjaminSRussell/issues/new).

<a name="data"></a>
<!-- survey:start -->
<sub>Measured 9 Oct 2026 from clones of 22 public repositories, my commits on their default branches; bulk-edit days (9–10 Nov 2025, 1 and 7 Oct 2026, when one change touched most repositories) are left out of the chart · 3 % of my commits carry an AI co-author trailer; 297 more were written by coding agents (Claude, jules) and are not counted as mine · regenerated weekly.</sub>
<!-- survey:end -->

<!-- license:start -->
<sub>**License** Code MIT; images and text CC BY 4.0; fonts under their own licenses in [`scripts/fonts/`](scripts/fonts/). To make your own, fork the repository, fill in `chart.toml` and run the workflow; the images are regenerated from your repositories · how it's built → [DESIGN.md](DESIGN.md)</sub>
<!-- license:end -->
