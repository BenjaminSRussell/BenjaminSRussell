<!-- The hero is regenerated weekly from assets/stats.json by scripts/build_assets.py and published to the `chart` branch. Text between x:start and x:end marker comments is written by scripts/render_readme.py; edit chart.toml, not this file, for those lines. -->

<a name="top"></a>
<!-- picture:hero:start -->
<a href="https://github.com/BenjaminSRussell/Rust-sitemap">
<picture>
<source media="(min-width: 852px) and (max-width: 1199px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-mid-night.svg">
<source media="(min-width: 852px) and (max-width: 1199px)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-mid-day.svg">
<source media="(max-width: 851px) and (prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-phone-night.svg">
<source media="(max-width: 851px)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-phone-day.svg">
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-night.svg">
<img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-day.svg" width="100%" alt="How to install Ben Russell's crawler rustmapper, what it does with each page, and how to stop it. It loops until one Ctrl-C writes data/sitemap.jsonl.">
</picture>
</a>
<!-- picture:hero:end -->

<p align="center">
  <!-- position:start — chart.toml [position] text; "" omits the slot -->
<!-- position:end -->
  <a href="https://github.com/BenjaminSRussell/Rust-sitemap"><b>rustmapper</b></a>&nbsp;· <a href="https://pypi.org/project/rustmapper/">PyPI</a>&nbsp;· <a href="https://github.com/BenjaminSRussell/Scrapy"><b>Scrapy</b></a>&nbsp;· <a href="mailto:benjamin.sheldon.russell@gmail.com">Email</a>
  <!-- contact:start — set linkedin / resume in chart.toml [contact]; "" drops the slot -->
<!-- contact:end -->
</p>

**Ben Russell builds** web crawlers, discovery pipelines, raw-first storage, and the dashboards that watch them.<br>
**Languages** <!-- n:languages -->Python, Rust; Swift, JavaScript, TypeScript, C, Go<!-- /n -->.<br>
**Stack** Delta Lake, PostgreSQL, Redis, Parquet · Docker, Kubernetes, Prometheus, Grafana, GitHub Actions · tokio, redb, maturin.

<!-- pick:start -->
**rustmapper** gives you a site's list of URLs from one binary, with no services to run. His **Scrapy** repository keeps the pages themselves, deduplicated and summarized, and needs Docker.
<!-- pick:end -->

<!-- about:Rust-sitemap:start -->
<!-- about:Rust-sitemap:end -->

<!-- facts:Rust-sitemap:start -->
**[rustmapper](https://github.com/BenjaminSRussell/Rust-sitemap)** · *on main at `32c2651`: built on tokio, redb, rkyv, reqwest, clap · 176 test functions · CI passed 7 Oct 2026: tests, rustfmt · 16k lines of Rust · coding agents (Claude) authored 45 of its 146 commits and co-signed 1 of his own 101*
<!-- facts:Rust-sitemap:end -->

<!-- install:Rust-sitemap:start -->
Prebuilt for Apple silicon on CPython 3.13; elsewhere `pip` builds it from source, which needs a Rust toolchain (3 min from a cold cache on a 4-core Linux x86_64 machine).

Before you run 0.1.3:

- It sends requests with no pause between them, up to 256 at a time across all hosts.<br>`--workers 1` sends one at a time.
- It ignores `Crawl-delay`, and asks for `robots.txt` only over https, so a plain-http site's rules are not read.
- By default it asks crt.sh and Common Crawl about your domain.<br>`--seeding-strategy none` asks no one.
- From `www.<site>` it skips sibling hosts such as `blog.`, even ones crt.sh lists. Start at the bare domain to take them all.

<details>
<summary>What 0.1.3's files miss or get wrong</summary>

- It reads links from the HTML a server sends, and no JavaScript runs. go_go_go can render pages in headless Chrome.
- After a redirect it keeps the old address and reads the page's links from it: if `/docs` redirects to `/docs/`, `a.html` is fetched as `/a.html`.
- Only HTML pages that answer 200, redirected or not, get a `status_code`. Errors, timeouts and non-HTML 200s are left blank, `crawled_at` too, never retried.
- Its `sitemap.xml` is every page with `status_code` 200, in one file; the format allows 50,000 URLs per file. It keeps `noindex` and canonicalized pages.

</details>

```sh
pip install rustmapper
rust_sitemap crawl \
    --start-url <your-site>
# 0.1.3 runs until stopped: when
# "Received work item" stops
# for 60 s, then Ctrl-C once

# sitemap.xml, even after a kill
rust_sitemap export-sitemap
```
<!-- install:Rust-sitemap:end -->

<!-- handoffs:start -->
<!-- handoffs:end -->

**[Scrapy](https://github.com/BenjaminSRussell/Scrapy)** is his crawl system on top of the Scrapy framework, in four stages: discovery, analysis, summaries, large documents.

<!-- facts:Scrapy:start -->
*On main at `96e7a1a`: built on deltalake, redis, psycopg2, prometheus-client, datasketch · 1,920 test functions (CI selects all but 41) · CI passed 8 Oct 2026: tests, ruff, mypy, bandit · MIT license · 69k lines of Python · coding agents (jules, Claude) authored 71 of its 499 commits and co-signed 30 of his own 420*
<!-- facts:Scrapy:end -->

- Raw pages land in Delta Lake and stay raw: typed Arrow schemas per table, schema evolution by merge, partitions by domain, OPTIMIZE and VACUUM from a maintenance queue. Metrics in PostgreSQL, queues in Redis.
- Repeat URLs are dropped by their hash, near-duplicate pages by MinHash. In stage 3 a page's summary is its first five sentences; documents over 50,000 characters go to stage 4, where bart-large-cnn runs on the worker itself, so nothing is sent to an external API.
- Prometheus alerts on its own metrics, such as Delta writes spilling to disk, and Grafana dashboards. A kill switch stops new downloads within 5 s, with a runbook. Docker Compose and a Helm chart for Kubernetes.

Run these from the folder you cloned [Scrapy](https://github.com/BenjaminSRussell/Scrapy) into. `python start.py` starts PostgreSQL, Redis, Grafana and a worker for each of the four stages. It needs Docker and the `docker-compose` command (Docker Desktop has it; on Linux, install Compose standalone). It loads no seeds: the last command gives the spider your site and names it `<your-bot>` (without that line, `UConn-Discovery-Crawler/1.0`). The spider obeys `robots.txt` and its `Crawl-delay`. The stage 2 worker then fetches every link the spider queued, disallowed ones too, 4 at a time per host, as `Python/3.11 aiohttp/3.13.1`.

```sh
cd Scrapy/Scraping_project
python start.py
docker-compose run --rm \
  scraper scrapy crawl scout \
  -s USER_AGENT=<your-bot> \
  -a allowed_domains=<domain> \
  -a start_urls=<url>
```

Grafana opens on `localhost:3000`. What it writes lands in Delta tables under `data/delta/`; [DATA_USAGE.md](https://github.com/BenjaminSRussell/Scrapy/blob/main/Scraping_project/docs/guides/DATA_USAGE.md) lists them and shows how to read or export them.

<a name="also"></a>
**Also**

- [**ideal-url-organizer**](https://github.com/BenjaminSRussell/ideal-url-organizer) — 21 ways to sort a pile of URLs from their crawl records (domain, crawl depth, subdomain, …).
- [**go_go_go**](https://github.com/BenjaminSRussell/go_go_go) — rustmapper's counterpart in Go, with the same crawl and export-sitemap commands, plus optional headless-Chrome rendering and SQLite storage with full-text search.
- [**rust_llm_logger**](https://github.com/BenjaminSRussell/rust_llm_logger) — a non-buffering reverse proxy for LLM servers, in Rust. Each chunk is parsed for token counts and passed straight on, and the call is logged only after the client has its last byte.
- [**Ai_code_detector**](https://github.com/BenjaminSRussell/Ai_code_detector) — `aicd scan` scores each file of a repository for signs of AI authorship, from its comments, naming, structure and git history, and says why it flagged it.

<details>
<summary><!-- n:more_count -->15<!-- /n --> more repositories: scrapers and data tools, Swift apps, games, a C game engine</summary>
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
- Also: [3d-swift-widget](https://github.com/BenjaminSRussell/3d-swift-widget) · [2d-swift-widgets](https://github.com/BenjaminSRussell/2d-swift-widgets) · [MLX_convertion](https://github.com/BenjaminSRussell/MLX_convertion) · [Course_crusader](https://github.com/BenjaminSRussell/Course_crusader) · [excel-and-vba](https://github.com/BenjaminSRussell/excel-and-vba)

</details>

<a name="rules"></a>
**Working rules**

<!-- notices:start -->
1. **Boring under load.** When 5 URLs in a row on one host fail every retry, that host is left alone for 60 s; the rest of the crawl goes on. *Scrapy, Oct 2026: a circuit breaker for each host in stage 2.*
2. **Raw before clean.** Next month's question can't be known today, so the raw layer is appended to and never overwritten. *Scrapy, Oct 2025: raw pages written to Delta Lake with `write_deltalake`.*
3. **Measure in week one.** Metrics were exported 6 days after the first commit, and a dashboard was up 5 days after that. *Scrapy, Oct 2025: Prometheus metrics, then Grafana dashboards.*
<!-- notices:end -->

Found a mistake? [Open an issue](https://github.com/BenjaminSRussell/BenjaminSRussell/issues/new).

<a name="data"></a>
<!-- survey:start -->
<sub>The [drawing](DESIGN.md) shows rustmapper 0.1.3, the release pip installs; its commands were run, with seeding off, against a local 3-page site on 10 Oct 2026 (Linux x86_64). Tests and lines are counted per repository, whoever wrote them.</sub>
<!-- survey:end -->

<!-- license:start -->
<sub>**This profile** Code MIT; images and text CC BY 4.0; fonts under their own licenses in [`scripts/fonts/`](scripts/fonts/).</sub>
<!-- license:end -->
