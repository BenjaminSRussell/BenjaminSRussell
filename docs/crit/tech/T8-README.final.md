<!-- Sheets are redrawn nightly from assets/stats.json by scripts/build_assets.py. Text between x:start and x:end marker comments is written by the build; edit chart.toml, not this file, for those lines. -->

<a name="top"></a>
<picture>
<!-- T1: phone and reduced-motion <source> lines go here, most specific first, in T1 §2.4 order: phone+dark, phone, reduce+dark, reduce, then the dark source below. -->
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/hero-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/hero-light.svg" width="100%" alt="Chart of Ben Russell's repositories, titled: I survey a web that is wrong about itself. Right margin unsurveyed. A boat sails out and back."></picture>
<sub>One feature per public repository, area by commits. The chart number is the public repository count; the edition is the rustmapper release.</sub>

<p align="center">
  <a href="https://github.com/BenjaminSRussell/Rust-sitemap"><b>rustmapper</b></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/BenjaminSRussell/Scrapy"><b>Scrapy Harbor</b></a>
  &nbsp;·&nbsp;
  <a href="https://pypi.org/project/rustmapper/">PyPI</a>
  &nbsp;·&nbsp;
  <a href="mailto:benjamin.sheldon.russell@gmail.com">Email</a>
  &nbsp;·&nbsp;
  <!-- contact:start — Ben: real URLs or set linkedin/resume = "" in chart.toml to drop the slot; the gate refuses ⟨ ⟩ -->
  <a href="⟨linkedin url⟩">LinkedIn</a>
  &nbsp;·&nbsp;
  <a href="⟨résumé url⟩">Résumé</a>
  <!-- contact:end -->
  &nbsp;·&nbsp;
  <a href="scripts/">How it's built</a>
</p>

<!-- position:start — Ben fills this line; scripts/check.py fails the build while ⟨ ⟩ remains -->
<p align="center"><b>⟨role⟩</b> · ⟨city or timezone⟩ · ⟨open to / currently⟩</p>
<!-- position:end -->

| | |
|---|---|
| **Ben Russell builds** | crawl and data infrastructure: web crawlers, discovery pipelines, raw-first storage, the dashboards that watch them |
| **Languages** | Python, Rust; Swift, C, TypeScript, Go |
| **Stack** | Delta Lake, PostgreSQL, Redis, Parquet · Docker, Kubernetes, Prometheus, Grafana, GitHub Actions · tokio, redb, maturin |

Most of what I build is survey work. The sitemap and the site disagree, and the subdomains nobody links to appear in neither, so the crawlers go and take soundings, one measured depth at a time, instead of trusting what the site declares. The storage keeps the raw log, so any depth can be checked again, and a dashboard says where the boat is while that still matters. I care how the work looks for the same reason I care that it holds.

<br>

<a name="soundings"></a>
## Soundings <sub><i>stats</i></sub>

<picture>
<!-- T1: phone and reduced-motion <source> lines go here, most specific first. -->
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/soundings-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/soundings-light.svg" width="100%" alt="Tide table: fifty-two weeks of commits as a curve, high and low water dated, one large commit figure. The curve draws in once and holds."></picture>
<!-- figures:start -->
<sub>1,828 commits · 21 repositories surveyed · since Oct 2024 · soundings taken 7 Oct 2026</sub>
<!-- figures:end -->

<br>

<a name="approaches"></a>
## Approaches <sub><i>main projects</i></sub>

One sheet, read left to right. rustmapper goes out first and finds the coastline. Scrapy Harbor is where a crawl is run and kept. The channel between them is charted as proposed; nothing runs it yet.

<picture>
<!-- T1: phone and reduced-motion <source> lines go here, most specific first. -->
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/approaches-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/approaches-light.svg" width="100%" alt="Chart of two systems: rustmapper's survey lines left, a buoyed channel into Scrapy Harbor right, legend below. The soundings fill in behind the vessel."></picture>
<sub>Soundings in URLs. The legend on this sheet defines every symbol used on the page and says which figures are measured.</sub>

**[rustmapper](https://github.com/BenjaminSRussell/Rust-sitemap) is the survey vessel:** a concurrent sitemap crawler written in Rust and shipped to [PyPI](https://pypi.org/project/rustmapper/) as a Python package. Edition 0.1.3, 8 Nov 2025, provisional.

- The throttle watches the database, not the network: a governor reads redb commit latency every 250 ms and grows or shrinks the worker pool between 256 and 1,024 permits, so the crawl slows when it cannot persist what it found.
- Every frontier event is written to a CRC32-framed write-ahead log (rkyv, zero-copy replay) before it reaches redb; a killed crawl resumes at the last record.
- The frontier is rendezvous-hashed by registrable domain, one shard per core, so a host's queue lives in one place; robots.txt is read first and its crawl-delay honoured. Optional Redis for distributed runs.
- Seeds from sitemaps, Certificate Transparency logs and the Common Crawl index: what a site says about itself, every host that ever held a certificate, and every URL someone once linked.
- Rust CLI and a Python package built with maturin. Prebuilt wheel for Apple silicon on CPython 3.13; elsewhere `pip` builds from source and needs a Rust toolchain.

```sh
pip install rustmapper
rustmapper crawl --start-url example.com
rustmapper export-sitemap --data-dir ./data --output sitemap.xml
```

**[Scrapy Harbor](https://github.com/BenjaminSRussell/Scrapy) is where a run is operated:** a multi-stage crawl platform built on the Scrapy framework.

- A scout spider goes first; analysis and summarization workers follow, each its own mark in the channel.
- Raw pages land in Delta Lake and stay raw: typed Arrow schemas per table, schema evolution by merge, partitions by domain, OPTIMIZE and VACUUM from a maintenance queue. Metrics in PostgreSQL, queues in Redis.
- Duplicates caught by URL hash and MinHash; summaries from BART-large-CNN on the worker itself, so nothing leaves the harbor for an API.
- Prometheus metrics on Grafana dashboards. Circuit breakers wrap the HTTP, Delta Lake and Redis services; per-host throttles are separate. Docker Compose and a Helm chart for Kubernetes.

<br>

<a name="log"></a>
## Ship's log <sub><i>one run</i></sub>

One rustmapper run, entered the way a log is kept.

<picture>
<!-- T1: phone and reduced-motion <source> lines go here, most specific first. -->
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/log-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/log-light.svg" width="100%" alt="Ship's log on ruled paper: one rustmapper run, entry by entry, from install to exported sitemap. Types once; only the cursor keeps time."></picture>
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
<summary><b>Below the waterline</b> · 12 more repositories: Swift widgets, a C game engine, games, tooling</summary>
<br>

- [**3d-swift-globe-widget**](https://github.com/BenjaminSRussell/3d-swift-globe-widget) — Titan: a native macOS 3D globe in MapKit and SwiftUI, permanent night mode, packets arcing from NYC to LA.
- [**Spotify_to_apple_music**](https://github.com/BenjaminSRussell/Spotify_to_apple_music) — library migration in both directions, matching on ISRC first and on fuzzy text and duration after. A SwiftUI face and a CLI.
- [**game_engine**](https://github.com/BenjaminSRussell/game_engine) — a voxel engine in C with its own physics. The kind of thing you build to learn why engines are hard.
- [**cozy-game**](https://github.com/BenjaminSRussell/cozy-game) — Cozy Haven, a farming game in React Native and Expo.
- [**Data_science_dev**](https://github.com/BenjaminSRussell/Data_science_dev) — Data Science Tycoon, a browser game: climb from data-entry clerk to Chief Data Officer by making charts your boss rates out of five.
- [**Wheel**](https://github.com/BenjaminSRussell/Wheel) — a Three.js prize wheel with a physics-based spin and an LED rim. Lands on a programming language.
- [**FashionDB**](https://github.com/BenjaminSRussell/FashionDB) — scrapes Reddit and the web for fashion rules and runs them through an NLP pipeline.
- [**Data-visualizer**](https://github.com/BenjaminSRussell/Data-visualizer) — a lightweight, Superset-inspired exploration UI over PostgreSQL. Display only, by design.
- Also: [3d-swift-widget](https://github.com/BenjaminSRussell/3d-swift-widget) · [2d-swift-widgets](https://github.com/BenjaminSRussell/2d-swift-widgets) · [MLX_convertion](https://github.com/BenjaminSRussell/MLX_convertion) · [Course_crusader](https://github.com/BenjaminSRussell/Course_crusader)

</details>

<br>

<a name="instruments"></a>
## Instruments <sub><i>languages and stack</i></sub>

Python and Rust most days; Swift, C, TypeScript and Go when the work asks for them. Built on Apple silicon.

<picture>
<!-- T1: phone and reduced-motion <source> lines go here, most specific first. -->
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/instruments-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/instruments-light.svg" width="100%" alt="Equipment list in three columns: languages, stores and queues, deck; the date each was first fitted. The daily driver in bold; the rest when asked."></picture>
<!-- instruments:start (generated from the same FITTINGS table as the sheet) -->
<sub><b>Languages</b> Python · Rust · Swift · C · TypeScript · Go &nbsp;&nbsp; <b>Stores and queues</b> Delta Lake · PostgreSQL · Redis · SQLite and GRDB · Parquet &nbsp;&nbsp; <b>Deck</b> Scrapy (framework) · Docker and Kubernetes · Prometheus and Grafana · GitHub Actions · tokio · SwiftUI and MapKit · MLX and Qwen</sub>
<!-- instruments:end -->

<br>

<a name="colophon"></a>
<details>
<summary><b>Colophon</b> · how the sheets are drawn: type, editions, motion, variation, license</summary>
<br>

- **Type.** Instrument Serif for titles and the italic asides; IBM Plex Mono for labels, soundings and the log. Set as outlines in every sheet, so they look the same on every machine.
- **Editions.** Navy ink on cream paper by day; after dark, a night sheet on which the lights are the brightest things. Your system picks the edition through `<picture>`; a phone gets a narrower edition, and a request for reduced motion gets every sheet finished and still.
- **Motion.** SMIL only, and slow. The boat takes 96 seconds to cross the hero and come back; you are not meant to wait for it.
- **Variation.** The compass rose's inner ring is a 24-hour clock of my commits, counted in my own timezone, turned so the busiest hour sits at north. That is the variation.
- **Figures.** Upright numerals are measured; italic numerals are not. The chart number includes this repository; the chart is one of the things it charts.
- **Build.** [`scripts/build_assets.py`](scripts/build_assets.py) draws every sheet from the day's figures, which [`scripts/build_stats.py`](scripts/build_stats.py) fetches each morning. Conventions and the motion spec are in [DESIGN.md](DESIGN.md).
<!-- license:start — ships only once LICENSE and chart.toml exist (T1); the gate checks both files -->
- **License.** Code MIT; sheets and copy CC BY 4.0; fonts under their own licenses in [`scripts/fonts/`](scripts/fonts/). To draw your own, fork the repository, fill in `chart.toml` and run the workflow; the sheets redraw from your repositories.
<!-- license:end -->

</details>

<br>

<picture>
<!-- T1: phone and reduced-motion <source> lines go here, most specific first. -->
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/footer-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/footer-light.svg" width="100%" alt="Limit of survey: a dotted line, hatched ground beyond, a sailboat holding short of the edge. The chart ends here; the web doesn't."></picture>
