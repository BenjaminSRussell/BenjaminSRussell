<!-- A chart of the open web, kept as a profile. Sheets are redrawn nightly from the day's data by scripts/build_assets.py; corrections are welcome and will be entered as notices. -->

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/hero-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/hero-light.svg" width="100%" alt="The open web. Ben Russell: I survey a web that is wrong about itself. Chart number is the public repo count; edition is the rustmapper release. Soundings in commits, datum main. One feature per repository, area by commits, the six largest named; shoals tinted inside danger lines; wrecks marked Wk. Region B marks, lights flashing their characters. Two-ring rose. Right margin hatched UNSURVEYED. A boat sails out and back."></picture>

<p align="center">
  <a href="https://github.com/BenjaminSRussell/Rust-sitemap"><b>rustmapper</b></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/BenjaminSRussell/Scrapy"><b>Scrapy</b></a>
  &nbsp;·&nbsp;
  <a href="https://pypi.org/project/rustmapper/">PyPI</a>
  &nbsp;·&nbsp;
  <a href="mailto:benjamin.sheldon.russell@gmail.com">Email</a>
  &nbsp;·&nbsp;
  <a href="#colophon-how-the-chart-was-drawn">Colophon</a>
</p>

<!-- POSITION: Ben, add one line here: role · city or timezone · what you want next. The chart has a slot for it. -->

<br>

Most of what I build is survey work on a web that is wrong about itself: the sitemap and the site disagree, and the subdomains nobody links to appear in neither. The crawlers take the soundings. The storage keeps the raw log, so any depth can be checked again, and a dashboard says where the boat is while that still matters. I care how the work looks for the same reason I care that it holds.

<br>

## Soundings <sub>the figures, taken daily</sub>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/soundings-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/soundings-light.svg" width="100%" alt="Tide table. Fifty-two weeks of commits as a tide curve, high water and low water dated, slack water noted where the water was slack. One large figure for commits, the rest small, with a depth scale of languages. Upright numerals are measured. The curve draws in once and holds."></picture>

<br>

## Approaches <sub>the two systems</sub>

One chart, read left to right. rustmapper goes out first and finds the coastline; Scrapy is the harbor the survey feeds, where the fleet is run.

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/approaches-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/approaches-light.svg" width="100%" alt="Approaches to Scrapy Harbor. Left, unsurveyed water where a survey vessel runs parallel track lines, sixteen drawn, marked times thirty-two, lettered blocks for the shards, each sounding written to the WAL tape. Right, a buoyed channel, G 1 URLS to R 4 SUMMARIZE, past Grafana Lt Fl(3) 10s and a red sector for the breaker, into the anchorage at Delta Lake. Legend panel and source diagram in the corners."></picture>

**[rustmapper](https://github.com/BenjaminSRussell/Rust-sitemap) is the survey vessel:** a concurrent sitemap crawler written in Rust and shipped to [PyPI](https://pypi.org/project/rustmapper/) as a Python package.

- Up to 512 workers, adaptively throttled, over a sharded frontier
- A write-ahead log, so a stopped crawl resumes where it stopped
- Seeds from sitemaps, Certificate Transparency logs and the Common Crawl index; the last two are how you find the subdomains nobody links to
- Optional Redis for distributed runs; the Python package is built with maturin, so the fast path is one `pip install rustmapper` away

**[Scrapy](https://github.com/BenjaminSRussell/Scrapy) is the harbor:** a multi-stage crawler platform built on the Scrapy framework, not the framework itself. It is where a run is operated.

- A scout spider goes first; analysis and summarization stages follow, each its own mark in the channel
- Raw pages land in Delta Lake and stay raw. Metrics go to PostgreSQL and queues to Redis, behind one storage interface
- Prometheus metrics on Grafana dashboards, with circuit breakers on the hosts that misbehave
- Docker and Kubernetes manifests, and tests covering 90%+ of it

<br>

## Ship's log <sub>one session</sub>

A rustmapper run, entered the way a watch is kept: time, position, wind, remarks.

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/log-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/log-light.svg" width="100%" alt="Watch log on ruled paper, no neat line. Columns: time, position in URLs, wind in requests per second set italic, remarks. The remarks are the lines of a rustmapper session, seeding from sitemaps, CT logs and Common Crawl, sixteen shards, WAL on, sitemap exported. 14:05, remarks, nothing to report. The next entry: Nothing on fire. Signed off. Types once; only the cursor keeps time."></picture>

<br>

## Notices to mariners <sub>five corrections</sub>

Five corrections to this chart, written down so I stop making them. The title block reads "Corrected through Notice 5" because of this list.

1. **Boring under load.** The system worth having is the one still running after you have stopped watching it. Clever is for prototypes. *Entered from Scrapy, whose circuit breakers exist for this reason.*
2. **Keep the log. Raw before clean.** The question you will want to answer next month is one you cannot ask today, so the raw layer is never overwritten. *Entered from the Delta Lake anchorage in Scrapy, and from the write-ahead log in rustmapper.*
3. **Lights before speed.** A crawler you cannot watch is a crawler you cannot trust; dashboards and breakers go in version one. *Entered from Grafana Lt, the first thing built on the Scrapy approach.*
4. **Parse, don't pattern-match.** Never regex what a parser already understands. *Entered from ideal-url-organizer, where the rule was first written down.*
5. **The surface is part of the system.** A chart nobody can read is not a chart, and a tool that confuses its operator is already failing. *Entered from this page, whose earlier editions looked fine and read as a template.*

<br>

## Instruments <sub>the stack</sub>

Python and Rust most days; Swift, C, TypeScript and Go when the work asks for them. Built on Apple silicon.

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/instruments-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/instruments-light.svg" width="100%" alt="Instruments, a short strip. Mono columns, no boxes, the daily driver in bold. Languages: Python, Rust, Swift, C, TypeScript, Go. Data: Delta Lake, PostgreSQL, Redis, Parquet. Ops: Docker, Kubernetes, Prometheus, Grafana, GitHub Actions. Surfaces and models: SwiftUI, MapKit, React Native, MLX with Qwen. Chart number repeated outside the rule."></picture>

<br>

## Other waters <sub>smaller work</sub>

Shorter crossings.

- [**Elusive_trades_data**](https://github.com/BenjaminSRussell/Elusive_trades_data) — HVAC parts search across several supplier APIs, part numbers matched by zero-shot classification. File-based: no database, no Docker, no passwords.
- [**ideal-url-organizer**](https://github.com/BenjaminSRussell/ideal-url-organizer) — 25+ ways to sort a pile of URLs: by domain, crawl depth, subdomain, actual page content. Home of the "no regex" rule.
- [**go_go_go**](https://github.com/BenjaminSRussell/go_go_go) — the Go sibling of rustmapper: 256-worker pools, per-host politeness, Bloom-filter dedup sized for 100M+ URLs, the same seed sources.
- [**rust_llm_logger**](https://github.com/BenjaminSRussell/rust_llm_logger) — a non-buffering reverse proxy for LLM servers, in Rust. A stream-tee forwards tokens to the client while parsing them for metrics, so logging costs the caller nothing.
- [**mlx_Qwen_data_entry**](https://github.com/BenjaminSRussell/mlx_Qwen_data_entry) — Qwen-DBA: profiles database workloads and has Qwen, on Apple MLX, recommend optimizations, with a human in the loop.
- [**Ai_code_detector**](https://github.com/BenjaminSRussell/Ai_code_detector) — probabilistic forensics for AI-generated code across seven languages, from stylometry down to git-history patterns.

<details>
<summary><b>Below the waterline</b></summary>
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

## Colophon <sub>how the chart was drawn</sub>

- **Type.** Instrument Serif for titles and the italic asides; IBM Plex Mono for labels, soundings and the log. Set as outlines in every SVG, so the sheets look the same on every machine.
- **Editions.** Navy ink on cream paper by day; after dark, a night chart on which the lights are the brightest things on the sheet. Your system setting picks the edition through `<picture>`.
- **Motion.** SMIL only, and slow. The boat takes 96 seconds to cross the hero and come back; you are not meant to wait for it.
- **Variation.** The compass rose's inner ring is a 24-hour clock of my commits, turned so the busiest hour sits at north. The variation note names the hour.
- **Build.** [`scripts/build_assets.py`](scripts/build_assets.py) draws every sheet from the day's figures, which [`scripts/build_stats.py`](scripts/build_stats.py) fetches each morning. Conventions and the motion spec are in [DESIGN.md](DESIGN.md).

If you like it, borrow it.

<picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/footer-dark.svg"><img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/main/assets/footer-light.svg" width="100%" alt="Limit of survey. A dotted limit line, hatched ground beyond it, and a sailboat that approaches the edge, holds sixty pixels short and rides the swell. Past the line the water goes over. Surveyed to this line; beyond it, no data. The chart ends here. The web doesn't."></picture>
