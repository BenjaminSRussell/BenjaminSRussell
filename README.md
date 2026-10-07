<!--
  Hi. This page is generated art plus hand-written words.
  Every image is an SVG with its type set as outlines, in a dark and a light
  version, built by scripts/build_assets.py. Design notes live in DESIGN.md.
-->

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/hero-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/hero-light.svg" width="100%" alt="Ben Russell. I build crawlers that survive the open web, and the systems that make sense of what they bring back."></picture>

<p align="center">
  <a href="https://github.com/BenjaminSRussell/Rust-sitemap"><b>rustmapper</b></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/BenjaminSRussell/Scrapy"><b>Scrapy</b></a>
  &nbsp;·&nbsp;
  <a href="https://pypi.org/project/rustmapper/">PyPI</a>
  &nbsp;·&nbsp;
  <a href="mailto:benjamin.sheldon.russell@gmail.com">Email</a>
  &nbsp;·&nbsp;
  <a href="#colophon">How this page is made</a>
</p>

<br>

**Hi, I'm Ben.** I'm a full-stack developer with a soft spot for the unglamorous middle of the stack: the part where a page that lies becomes a row you can trust. Almost everything I build points the same way. Crawlers that stay standing when the site changes. Storage that keeps the trail so you can re-derive anything. Surfaces that let you see what the machine is doing *before* it breaks.

I care about design the way I care about data contracts. If a tool is hard to look at, it is hard to operate, and I'd rather fix the surface than apologize for it. This page is my small proof of that: every image on it is generated from a design system, in a dark and a light version, with real typography set as outlines.

<br>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/stats-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/stats-light.svg" width="100%" alt="By the numbers: lifetime commits, public repos, followers, languages in play, and the month I joined GitHub. Refreshed daily by GitHub Actions."></picture>

<br>

## Featured work

Two projects I keep coming back to. One is the platform, the other is the engine.

<a href="https://github.com/BenjaminSRussell/Scrapy"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/card-scrapy-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/card-scrapy-light.svg" width="100%" alt="Scrapy: a multi-stage crawler platform. URLs flow through scout, analyze and summarize stages into Delta Lake, with Prometheus and Grafana watching."></picture></a>

**[Scrapy](https://github.com/BenjaminSRussell/Scrapy)** is the platform. A multi-stage crawler that discovers, analyzes and summarizes web content at scale, built to be operated rather than demoed.

- Scout spider with URL prioritization, JS-heavy page detection and adaptive, domain-aware rate limits
- Raw data lands in Delta Lake, metrics in PostgreSQL, queues in Redis, one storage interface over all three
- Circuit breakers, health checks, live Grafana dashboards on Prometheus metrics
- Typed configuration, 90%+ test coverage, Docker and Kubernetes manifests, one-command start

<br>

<a href="https://github.com/BenjaminSRussell/Rust-sitemap"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/card-rustmapper-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/card-rustmapper-light.svg" width="100%" alt="rustmapper: a concurrent sitemap crawler in Rust. A root URL fans out through frontier shards to discovered pages, driven by up to 512 adaptive workers with a write-ahead log."></picture></a>

**[rustmapper](https://github.com/BenjaminSRussell/Rust-sitemap)** is the engine. A concurrent sitemap crawler and URL discovery tool written in Rust and shipped as a Python package, so the fast path is one `pip install` away.

- Up to 512 workers with adaptive concurrency control and a sharded frontier
- Persistent state with a write-ahead log, so a crawl can be stopped and resumed
- Seeds from sitemaps, Certificate Transparency logs and the Common Crawl index, which is how you find the subdomains nobody links to
- Optional Redis for distributed runs, native Rust CLI, Python API via maturin, published on [PyPI](https://pypi.org/project/rustmapper/)

<br>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/terminal-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/terminal-light.svg" width="100%" alt="An animated terminal: pip install rustmapper, then rustmapper crawl --start-url example.com --workers 512, seeding from sitemaps, CT logs and Common Crawl, crawling, and exporting sitemap.xml."></picture>

<br>

## How I think about it

Five rules I keep relearning, written down so I stop relearning them.

1. **Boring under load.** The interesting version of a system is the one that is still running on day forty. Clever is for prototypes.
2. **Keep the trail.** Raw before clean, always. The question you will want to answer next month is one you cannot imagine today.
3. **Observable before fast.** A crawler you cannot watch is a crawler you cannot trust. Dashboards and breakers are part of version one, not the polish.
4. **Contracts over heroics.** Clear data shapes beat clever parsing. I keep a personal golden rule for URLs: never regex what a parser already understands.
5. **The surface is part of the system.** Design is not the last step. If the tool is ugly it is probably also confusing, and confusion is an operational cost.

<br>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/stack-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/stack-light.svg" width="100%" alt="Stack. Languages: Python, Rust, Swift, C, TypeScript, SQL. Data: Scrapy, Delta Lake, PostgreSQL, Redis, SQLite with GRDB, Parquet. Ops: Docker, Kubernetes, Prometheus, Grafana, GitHub Actions, tokio. Surfaces and ML: SwiftUI, MapKit, React Native, MLX, Qwen, Ollama."></picture>

<br>

## The shelf

The rest of the field. Some of it sharp, some of it exploratory, all of it real code.

<details open>
<summary><b>Scrape, search and data</b></summary>
<br>

- [**Elusive_trades_data**](https://github.com/BenjaminSRussell/Elusive_trades_data) — a deterministic, file-based HVAC parts search that pulls from several supplier APIs and matches part numbers with zero-shot classification. No database, no Docker, no passwords.
- [**ideal-url-organizer**](https://github.com/BenjaminSRussell/ideal-url-organizer) — 25+ ways to organize a pile of URLs, by domain, crawl depth, subdomain and actual page content. Home of the "no regex" rule.
- [**FashionDB**](https://github.com/BenjaminSRussell/FashionDB) — scrapes Reddit and the web for fashion rules, then runs them through an NLP pipeline.
- [**Data-visualizer**](https://github.com/BenjaminSRussell/Data-visualizer) — a lightweight, Superset-inspired exploration UI over PostgreSQL. Display only, by design.
- [**go_go_go**](https://github.com/BenjaminSRussell/go_go_go) — the Go sibling of rustmapper: 256-worker pools, per-host politeness, Bloom-filter dedup sized for 100M+ URLs, and the same seeding trio of sitemaps, CT logs and Common Crawl.

</details>

<details open>
<summary><b>Local models and tooling</b></summary>
<br>

- [**rust_llm_logger**](https://github.com/BenjaminSRussell/rust_llm_logger) — a non-buffering reverse proxy for LLM servers in Rust, Axum and Tower. A stream-tee forwards tokens to the client while parsing them for metrics, so logging costs the caller nothing.
- [**mlx_Qwen_data_entry**](https://github.com/BenjaminSRussell/mlx_Qwen_data_entry) — Qwen-DBA: profiles database workloads and uses Qwen on Apple MLX to recommend optimizations, with a human in the loop.
- [**Ai_code_detector**](https://github.com/BenjaminSRussell/Ai_code_detector) — probabilistic forensics for AI-generated code across seven languages, from stylometry and structure to git history patterns.

</details>

<details open>
<summary><b>Surfaces and play</b></summary>
<br>

- [**3d-swift-globe-widget**](https://github.com/BenjaminSRussell/3d-swift-globe-widget) — Titan: a native macOS 3D globe in MapKit and SwiftUI with permanent night mode, glowing data centers and packets arcing NYC to LA.
- [**Spotify_to_apple_music**](https://github.com/BenjaminSRussell/Spotify_to_apple_music) — bidirectional library migration with ISRC, fuzzy text and duration matching, a SwiftUI face and a CLI.
- [**game_engine**](https://github.com/BenjaminSRussell/game_engine) — a voxel game engine in C with its own physics. The kind of thing you build to understand why engines are hard.
- [**cozy-game**](https://github.com/BenjaminSRussell/cozy-game) — Cozy Haven, a peaceful farming game in React Native and Expo.
- [**Data_science_dev**](https://github.com/BenjaminSRussell/Data_science_dev) — Data Science Tycoon, a browser game where you climb from data entry clerk to Chief Data Officer by making charts your boss rates out of five.
- [**Wheel**](https://github.com/BenjaminSRussell/Wheel) — a Three.js prize wheel with a physics-based spin controller, an LED rim and confetti. Lands on a programming language.
- Also on the shelf: [3d-swift-widget](https://github.com/BenjaminSRussell/3d-swift-widget) · [2d-swift-widgets](https://github.com/BenjaminSRussell/2d-swift-widgets) · [MLX_convertion](https://github.com/BenjaminSRussell/MLX_convertion) · [Course_crusader](https://github.com/BenjaminSRussell/Course_crusader)

</details>

<br>

<div align="center">
<a href="https://github.com/BenjaminSRussell"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/output/github-contribution-grid-snake-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/output/github-contribution-grid-snake.svg" width="100%" alt="Contribution graph, eaten daily by a snake."></picture></a>
<sub>a year of commits, eaten nightly</sub>
</div>

<br>

## Colophon

This page is designed, not templated, and it is built the same way I build everything else.

- **Type.** Inter Display for headlines, Inter for copy, DejaVu Sans Mono for captions. Set as outlines inside every SVG, so it looks the same on every machine.
- **Color.** One warm signal orange on GitHub's own background. Mint only ever means *done*. Blue only ever means *the web*. Nothing else is colored.
- **Themes.** Every image ships in a dark and a light version and follows your system setting through `<picture>`.
- **Motion.** SMIL only, slow and purposeful. Packets travel pipelines, rows resolve in order, the terminal types, a small boat crosses the footer.
- **Build.** `scripts/build_assets.py` generates the artwork; `scripts/build_stats.py` fetches live numbers and a GitHub Action refreshes them daily. Tokens and rules are in [DESIGN.md](DESIGN.md).

If you like it, borrow it. Change the name, the copy and the palette, and it is yours.

<br>

**Off the clock.** The avatar is a sailboat about to go over a waterfall at golden hour. I'm told that's a mood. Mostly it's a reminder that the view is best right before the drop, and that it pays to have checked the chart.

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/footer-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/footer-light.svg" width="100%" alt="A small sailboat crossing a horizon line. Fair winds."></picture>
