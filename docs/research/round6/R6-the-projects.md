# R6. The projects themselves: what they are, how a URL moves through them, and what is really a map

Round 6 research, 9 Oct 2026. The question this file answers: if every map and every mark on the page must have a
purpose that comes from the projects, what do the projects actually contain that a visitor needs to see, and which of
it has a real geography (a route, a boundary, a structure you move through)?

Method. I read the clones in `scratchpad/clones/` (default branch, depth-1 checkouts; the bare `.git` mirrors for
history), downloaded and opened the rustmapper wheel and sdist that PyPI serves today, and read the standards, papers
and official guides below. Line numbers are for the clone HEADs: Rust-sitemap `32c2651` (7 Oct 2026), Scrapy `96e7a1a`.
Web searching hit the shared per-turn limit early in this round, so every web source below was fetched directly from a
known primary URL and read; where only part of a document could be read, the entry says so. Nothing here is from memory
alone.

## Sources

### A. The projects (clones, read-only) and this repository's measured facts

1. Rust-sitemap (rustmapper), `README.md` (install lines 7-25, options 78-95, output 126-139, Parquet/Delta hand-off
   141-195, architecture 209-215, troubleshooting 217-226, crash recovery 249-264, metrics 290-329, host budget 331-342).
2. Rust-sitemap source: `src/cli.rs` (subcommands 14-280), `src/main.rs` (169-527), `src/lib.rs` (410-426),
   `src/orchestration/governor.rs` (1-72), `src/frontier.rs` (103-200, 203-249, 328-440, 900-961, 1021-1121),
   `src/url_utils.rs` (81-91), `src/bfs_crawler.rs` (78, 679-705, 1041-1070), `src/wal.rs` (68, 191-279),
   `src/completion_detector.rs` (1-40), `src/sitemap_writer.rs` (134), `src/config.rs` (4-22), seeders
   `src/sitemap_seeder.rs` (1, 238-242), `src/ct_log_seeder.rs` (81-82), `src/common_crawl_seeder.rs` (105).
3. Rust-sitemap `Cargo.toml` (1-80), `pyproject.toml` (1-80), `python/rustmapper/__init__.py` (25-65, 170).
4. Rust-sitemap `docs/superpowers/specs/2026-08-08-rust-sitemapper-url-organizer-bridge-design.md` (the hand-off
   design, lines 1-89).
5. Rust-sitemap history, `Rust-sitemap.git`: `git log` (first commit 20 Oct 2025; 39 commits after 8 Nov 2025).
6. rustmapper on PyPI, JSON API `https://pypi.org/pypi/rustmapper/json` (read 9 Oct 2026), and the two files of 0.1.3
   opened locally: `rustmapper-0.1.3-cp313-cp313-macosx_11_0_arm64.whl` (contents: `rustmapper-0.1.3.data/scripts/
   rust_sitemap`, 6.2 MB, plus metadata; no Python module, no `entry_points.txt`) and `rustmapper-0.1.3.tar.gz`
   (`pyproject.toml` line 52: `bindings = "bin"`; `src/cli.rs` defaults: workers 256).
7. Scrapy (Ben's crawl platform), `README.md` (diagrams 20-33 and 117-160, quick start 84-100, spider names 230-256,
   monitoring 260-272, storage, testing, troubleshooting).
8. Scrapy source: `Scraping_project/src/stage1/scout_spider.py` (18, 73-83, 86-192),
   `src/lakehouse/lakehouse_manager.py` (40-43, 117, 364-368, 401, 525-560), `src/stage2/stage2_worker.py` (1-30,
   960-962), `src/stage3/stage3_worker.py` (1-30, 194-196), `src/stage4/stage4_worker.py` (1-25),
   `src/stage4/summarization.py` (78-79), `src/settings.py` (120-229), `src/core/config.py` (351-389),
   `src/stage1/sitemap_parser.py` (1), `docker-compose.yml` (services at 8-244), `monitoring/prometheus.yml` (30-45),
   `monitoring/alerting_rules.yml` (42 `- alert:` rules), `kafka-delta-ingest/` (`Cargo.toml`, `src/main.rs`, 1,003
   lines), `CHANGELOG.md` (27).
9. ideal-url-organizer: `README.md`, `run.sh` (39-60), `src/core/data_loader.py` (13-41), `src/organizers/`
   (`method_01` ... `method_25`, `registry.py`), `src/analyzers/link_graph_analyzer.py` (41-112, 272-287),
   `src/core/web_crawler.py` (412 lines), `scripts/import_rust_sitemapper.py` (1-30), `data/README.md`,
   `docs/superpowers/specs/2026-08-08-cross-site-insight-and-viewer-app-design.md` (1-90).
10. go_go_go: `README.md`, `internal/crawler/frontier.go` (12-78), `internal/crawler/politeness.go` (20-66),
    `internal/cli/*.go` (crawl, resume, export-sitemap, export-parquet, search), `internal/storage/storage.go` (17-29),
    `internal/navigation/weighted.go` (39-121).
11. rust_llm_logger: `README.md`, `src/app.rs` (34-48, 87), `src/proxy.rs` (115, 149), `src/store.rs` (14, 30),
    `src/parsers/*.rs`.
12. Ai_code_detector: `README.md` (install, quick start, "How it works", parsing backends), `src/ai_code_detector/`
    (`ingest/`, `analysis/`, `model/`, `report/`, `gate.py`, `aicd.py`).
13. The other fifteen repositories' READMEs (first lines read for each): Data_science_dev, game_engine, Wheel,
    Data-visualizer, Course_crusader, Elusive_trades_data, FashionDB, MLX_convertion, Spotify_to_apple_music,
    2d-swift-widgets, 3d-swift-widget, 3d-swift-globe-widget, cozy-game, mlx_Qwen_data_entry, BenjaminSRussell.
14. This repository: `assets/stats.json` (taken 2026-10-09: `repos[]`, `edition`, `claims`), and `docs/data/AUDIT.md`
    (definitions, section 2; per-repository table, section 3; verdicts, section 4).
15. This repository's current page: `README.md` (rustmapper and Scrapy sections, "Also" list) and the current render
    `scratchpad/r6/current-sheet-desk-870.png`.

### B. Standards

16. sitemaps.org. "Sitemaps XML format." Protocol 0.9, sitemaps.org (Google, Yahoo, Microsoft), 2006, page current
    2026. https://www.sitemaps.org/protocol.html
17. Koster, M., Illyes, G., Zeller, H., Sassman, L. "RFC 9309: Robots Exclusion Protocol." IETF, September 2022.
    https://www.rfc-editor.org/rfc/rfc9309.html
18. Laurie, B., Langley, A., Kasper, E. "RFC 6962: Certificate Transparency." IETF (Experimental), June 2013.
    https://www.rfc-editor.org/rfc/rfc6962.html
19. Berners-Lee, T., Fielding, R., Masinter, L. "RFC 3986: Uniform Resource Identifier (URI): Generic Syntax." IETF,
    January 2005 (section 6, normalization and comparison; read to 6.1). https://www.rfc-editor.org/rfc/rfc3986.html
20. Python Packaging Authority. "Entry points specification." packaging.python.org, current 2026.
    https://packaging.python.org/en/latest/specifications/entry-points/

### C. Web crawling and the web graph

21. Najork, M., Heydon, A. "High-Performance Web Crawling." Compaq SRC Research Report 173, 26 Sep 2001 (read in
    full, frontier section pp. 8-9). https://www.cs.cornell.edu/courses/cs685/2002fa/mercator.pdf
22. Manning, C. D., Raghavan, P., Schütze, H. *Introduction to Information Retrieval*, ch. 20.2.3 "The URL frontier."
    Cambridge University Press, 2008. https://nlp.stanford.edu/IR-book/html/htmledition/the-url-frontier-1.html
23. Broder, A., Kumar, R., Maghoul, F., Raghavan, P., Rajagopalan, S., Stata, R., Tomkins, A., Wiener, J. "Graph
    structure in the Web." WWW9 / Computer Networks 33, 2000 (read in full).
    https://www.cis.upenn.edu/~mkearns/teaching/NetworkedLife/broder.pdf
24. Brin, S., Page, L. "The Anatomy of a Large-Scale Hypertextual Web Search Engine." Computer Networks 30,
    pp. 107-117, 1998 (publication page and abstract).
    https://research.google/pubs/the-anatomy-of-a-large-scale-hypertextual-web-search-engine/
25. Kleinberg, J. M. "Authoritative Sources in a Hyperlinked Environment." Journal of the ACM 46(5), 1999 (abstract
    and introduction read). https://www.cs.cornell.edu/home/kleinber/auth.pdf
26. Broder, A. Z. "On the resemblance and containment of documents." Compression and Complexity of Sequences, 1997
    (abstract and introduction read).
    https://www.cs.princeton.edu/courses/archive/spring13/cos598C/broder97resemblance.pdf
27. Google Search Central. "Robots.txt specification: how Google interprets the robots.txt specification." Google,
    current 2026. https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt
28. Google Search Central. "Learn about sitemaps." Google, current 2026.
    https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
29. Google Search Central. "Crawl budget management for large sites." Google, current 2026.
    https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget
30. Common Crawl. "Common Crawl Index Server" (CDX API, `collinfo.json`). Common Crawl Foundation, current 2026.
    https://index.commoncrawl.org/
31. "Rendezvous hashing" (secondary; cites Thaler, D., Ravishankar, C., University of Michigan, 1996). Wikipedia,
    read 9 Oct 2026. https://en.wikipedia.org/wiki/Rendezvous_hashing
32. "Bloom filter" (secondary; cites Bloom, B. H., "Space/time trade-offs in hash coding with allowable errors,"
    CACM 13(7), 1970, whose ACM page refused the fetch). Wikipedia, read 9 Oct 2026.
    https://en.wikipedia.org/wiki/Bloom_filter
33. Salesforce (Althouse, J., Atkinson, J., Atkins, J.). "JA3: a method for profiling SSL/TLS clients." GitHub,
    2017; archived 1 May 2025. https://github.com/salesforce/ja3

### D. The tools the projects are built on (official documentation)

34. Scrapy developers. "Architecture overview." Scrapy 2.x documentation, current 2026.
    https://docs.scrapy.org/en/latest/topics/architecture.html
35. Scrapy developers. "Settings" (DEPTH_LIMIT, DEPTH_PRIORITY, scheduler queues, ROBOTSTXT_OBEY).
    https://docs.scrapy.org/en/latest/topics/settings.html
36. Scrapy developers. "Frequently Asked Questions" ("DFO by default"). https://docs.scrapy.org/en/latest/faq.html
37. Scrapy developers. "AutoThrottle extension." https://docs.scrapy.org/en/latest/topics/autothrottle.html
38. Scrapy developers. "Spiders" (SitemapSpider, allowed_domains). https://docs.scrapy.org/en/latest/topics/spiders.html
39. Armbrust, M., et al. "Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores." PVLDB 13(12),
    pp. 3411-3424, 2020 (abstract and introduction read). https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf
40. Databricks. "Medallion architecture" (bronze, silver, gold). Glossary, current 2026.
    https://www.databricks.com/glossary/medallion-architecture
41. delta-io. "kafka-delta-ingest." GitHub, current 2026. https://github.com/delta-io/kafka-delta-ingest
42. Prometheus authors. "Configuration" (global and per-job `scrape_interval`). prometheus.io, current 2026.
    https://prometheus.io/docs/prometheus/latest/configuration/configuration/
43. redb authors. "redb" crate documentation. docs.rs, current 2026. https://docs.rs/redb/latest/redb/
44. rkyv authors. "rkyv: zero-copy deserialization framework for Rust." https://rkyv.org/
45. Tokio authors. "tokio::sync::Semaphore." docs.rs, current 2026.
    https://docs.rs/tokio/latest/tokio/sync/struct.Semaphore.html
46. maturin authors. "Bindings" (pyo3 vs bin). maturin user guide, current 2026. https://www.maturin.rs/bindings.html
47. ekzhu. "MinHash LSH." datasketch documentation, current 2026. https://ekzhu.com/datasketch/lsh.html
48. Meta AI. "facebook/bart-large-cnn" model card, Hugging Face; and Lewis, M., et al. "BART: Denoising
    Sequence-to-Sequence Pre-training...", arXiv:1910.13461, 2019. https://huggingface.co/facebook/bart-large-cnn
49. Ollama. "API" (`/api/generate`, `prompt_eval_count`, `eval_count`). GitHub, current 2026.
    https://github.com/ollama/ollama/blob/main/docs/api.md

### E. What a stranger needs from a page about software

50. Brown, S. "The C4 model for visualising software architecture" and "Abstractions." c4model.com, current 2026.
    https://c4model.com/ and https://c4model.com/abstractions
51. Diátaxis. "Start here" (tutorials, how-to guides, reference, explanation). diataxis.fr, current 2026.
    https://diataxis.fr/start-here/
52. Shneiderman, B. "The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations." IEEE Symposium on
    Visual Languages, 1996 (read in full). https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf
53. GitHub Docs. "Managing your profile README." docs.github.com, current 2026.
    https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
54. GitHub Docs. "Creating diagrams" (Mermaid, GeoJSON, TopoJSON, ASCII STL). docs.github.com, current 2026.
    https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams

54 sources: 15 from the projects and this repository, 39 from outside.

## Findings

### F1. Ben's work is one subject, crawling and the data it produces, written four times in three languages [1, 7, 9, 10, 13, 14]

Of the 21 public repositories, seven acquire data from the web: Scrapy (Python, 69,036 lines), rustmapper (Rust,
16,390), ideal-url-organizer (Python, 12,242, with its own 412-line `src/core/web_crawler.py`), Course_crusader
(Python, 10,132; "unified university course-catalog scraper"), go_go_go (Go, 7,138), Elusive_trades_data (Python, 6,303;
supplier APIs) and FashionDB (Python, 5,193; Reddit via `praw`). Line counts are `repos[].lines` for the main language
[14]. These seven hold about 126k of the lines in programming languages that are not a game, a widget or a model tool.
rustmapper and go_go_go are the same crawler in two languages: the same `crawl / resume / export-sitemap` commands, the
same three seeders (sitemap, Certificate Transparency, Common Crawl), the same `--seeding-strategy
none/sitemap/ct/commoncrawl/all` flag [1, 10]. The rest (games, Swift widgets, a C engine, MLX tools) do not touch the
web. A visitor who should learn one thing learns this: he builds the machinery that finds pages, fetches them, and keeps
what it found.

### F2. rustmapper has a real route: a URL enters, waits, is fetched, and leaves as a line of JSONL and a sitemap [1, 2, 21, 22]

Traced in the code, one URL's path is:

1. **Seeded.** `crawl --start-url` plus seeders: robots.txt `Sitemap:` lines and sitemap indexes
   (`sitemap_seeder.rs:1`, filtered by robots rules at 238-242), crt.sh (`ct_log_seeder.rs:81-82`), the Common Crawl
   CDX index (`common_crawl_seeder.rs:105`). Each seeder has a time limit, default 120 s (README 87).
2. **Dispatched to a shard.** `FrontierDispatcher::add_links` normalises the URL, takes its host, and sends it to the
   shard chosen by rendezvous hashing of the registrable domain, so every subdomain of a site lands on one shard
   (`frontier.rs:103-108, 155-197`). The number of shards is `num_cpus::get()` (`lib.rs:426`).
3. **Checked for "seen".** The shard batches 500 incoming URLs (`config.rs:18`), tests each against a Bloom filter sized
   for 10 million URLs at 1 % false positives (`config.rs:13-14`, `frontier.rs:249`), and confirms likely duplicates
   against redb (`frontier.rs:349-362`).
4. **Kept in scope.** Only URLs whose host equals the start domain, or is a subdomain or parent of it, are queued
   (`url_utils.rs:81-91`, `frontier.rs:466`, `bfs_crawler.rs:699-704`). There is no depth limit: depth is recorded
   (`next_depth = job.depth + 1`, `bfs_crawler.rs:697`) but never cut.
5. **Waits for its host.** Each host has a ready time in a min-heap (`frontier.rs:97-100`); robots.txt is fetched with a
   3 s timeout and its `Crawl-delay` sets the gap (`frontier.rs:900-961`, `config.rs:21`). This is the Mercator
   front-queue / back-queue design: one queue per host, a heap of the times each host may next be contacted [21, 22].
6. **Gets a worker.** A Tokio semaphore holds the worker permits (`lib.rs:410`); a governor wakes every 250 ms, reads the
   writer's commit latency (EWMA), takes a permit away above 2,000 ms and gives one back below 200 ms, between 256 and
   1,024 permits by default (`governor.rs:14-67`) [45].
7. **Fetched and parsed.** reqwest with hickory DNS; links extracted with `scraper`/`html5ever`; optional Next.js and
   Shopify parsers (README 276-283).
8. **Recorded.** Every frontier change is appended to a write-ahead log framed `[len][crc32c][seqno][payload]`
   (`wal.rs:68`), fsynced every 100 ms (README 251), then committed to redb [43, 44]; the node lands in
   `data/sitemap.jsonl` (README 131-134).
9. **Leaves.** `export-sitemap` writes `sitemap.xml`, splitting at 50,000 URLs into a `sitemapindex`
   (`sitemap_writer.rs:134`, README 128), which is the protocol's own cap [16]; `classify` tags tech stacks;
   `python -m rustmapper.export_parquet` writes Parquet or a Delta table with a versioned 21-column schema
   (README 141-195).
10. **Ends.** The crawl stops on its own when the frontier is empty, nothing is in flight, no new URL has appeared for
    30 s, and that has held for 60 s (`completion_detector.rs:1-40`, README 94, 226).

Every stop names a file that exists. This is a route in the plain sense the brief asks for: a sequence of places a
thing passes through, each with a rule that decides whether it goes on.

### F3. What is genuinely spatial in rustmapper is the site it maps, not the repository [1, 16, 23, 28, 30]

Four things in this project have a real geography, and each has a source:

- **The web is a directed graph, and you cannot reach all of a site by following links.** Broder et al. found a core of
  56 million mutually reachable pages, with three other regions of about 44 million each (IN, OUT, tendrils), and a
  directed path between two random pages only 24 % of the time [23]. That is why rustmapper has seeders: a sitemap is
  what the site says about itself, Certificate Transparency logs list every host that ever held a public certificate
  [18], and the Common Crawl index lists URLs other crawls have seen [30]. Google gives the same reason for sitemaps:
  pages that nothing links to may not be found [28].
- **A sitemap is literally a map of a site**: a list of URLs, each with optional `lastmod`, `changefreq` and `priority`,
  at most 50,000 per file [16]. rustmapper's main output is one.
- **The frontier is a boundary between known and unknown**: discovered-but-not-fetched URLs, persisted so that after a
  crash "the uncrawled nodes ... are the frontier checkpoint" (README 251-256).
- **Hosts are places with a state.** The live report and the `rustmapper_hosts{status}` gauge sort every host into
  ready, delayed, saturated, backoff or blocked, and list the 25 most constrained with in-flight slots, crawl-delay,
  seconds until next eligible and consecutive failures (README 312, 331-342). Depth from the start URL is a real
  distance (the `depth` column, README 180).

None of these is the calendar. A week of commits has none of these properties: nothing travels between weeks, and
nothing is reachable or unreachable.

### F4. Scrapy is a staged pipeline with branches and side channels, and its tables are the stops [7, 8, 34, 39, 40]

The scout spider (`scout_spider.py:86-192`) classifies each response, extracts links, and for every new URL makes one
of four moves: off-site URLs become `stage1_offsite_candidates` items; static assets are discarded and counted; HTML
pages are queued for the JavaScript spider, queued for Stage 2, and followed at `depth + 1`; other content goes to
Stage 2 only. Discovery is written to `stage1_discovery`, partitioned by domain (`lakehouse_manager.py:364-368`).
The lakehouse defines 14 Delta tables (`lakehouse_manager.py:538-553`): `seed_urls`, `uconn_urls`,
`stage1_discovery`, `stage1_errors`, `stage1_offsite_candidates`, `js_spider_queue`, `stage2_queue`,
`stage2_page_analysis`, `stage2_errors`, `stage3_analytics`, `stage3_summaries`, `stage4_large_docs`,
`stage4_large_doc_summaries`, `stage4_summaries`, plus two quarantine tables (40-43). Stage 2 fetches with aiohttp,
parses with BeautifulSoup, guards against SSRF and soft bans (`stage2_worker.py:1-30`) and flags a page as a massive
document above 50,000 characters (`config.py:389`, `stage2_worker.py:960`). Stage 3 deduplicates with MinHash LSH at a
Jaccard threshold of 0.3 and writes an extractive summary, the first sentences of the text
(`stage3_worker.py:7, 22, 194-196`) [26, 47]. Stage 4 summarises the massive documents with `facebook/bart-large-cnn`
(`stage4/summarization.py:78-79`) [48]. A 1,003-line Rust service, also named `kafka-delta-ingest` but Ben's own code,
not the delta-io project [41], moves Kafka messages into Delta. Raw-first storage in Delta is the bronze layer of the
medallion pattern [39, 40]. Compose runs `scraper`, `stage1-worker` to `stage4-worker`, Redis, Postgres, two exporters,
Prometheus and Grafana (`docker-compose.yml:8-244`). Prometheus scrapes the crawler job every 30 s, which overrides the
global default [42] (`prometheus.yml:38-39`).

So Scrapy's geography is a route with a main channel (seed, discover, analyse, summarise) and branches (JS rendering,
large documents, off-site, errors and quarantine). Its README already draws the main channel twice in Mermaid
(README 20-33, 117-160), so a picture that only repeats that adds nothing.

### F5. The projects connect to each other, partly in working code and partly on paper [1, 4, 8, 9]

- **rustmapper → ideal-url-organizer: built.** `scripts/import_rust_sitemapper.py` takes a `sitemap.jsonl`, keeps the
  15 fields url-organizer's `URLRecord` accepts (any other key raises `TypeError`, `data_loader.py:39-41`), writes
  `data/raw/urls.jsonl` and runs `./run.sh --all` (methods 1-21, data quality, charts, report). It has a test
  (`tests/test_import_rust_sitemapper.py`). Methods 22-25 (HTTP status, schema.org type, PageRank authority, semantic
  similarity) read a different input and are not bridged [4, 9].
- **url-organizer → a viewer: designed, half built.** The 8 Aug 2026 spec describes a FastAPI sidecar on
  `127.0.0.1:8731` over `data/results_by_site/*` and a SwiftUI app that launches `rust_sitemap crawl` and the bridge;
  the `server/` package (`app.py`, `aggregator.py`, `jobs.py`) and its tests exist; the viewer app is a separate
  repository that is not among the 21 public ones. The spec lists eleven crawled sites (wikipedia, hackernews, nike,
  target, allbirds, reactdev, walmart, stubhub, zillow, two target-massive runs), but `data/` is gitignored, so none of
  those results is in any public repository [9].
- **rustmapper → Scrapy: one side only.** rustmapper exports a Delta table named `stage1_discovery` "for Scrapy"
  (README 141-169), and Scrapy has a `stage1_discovery` table, but no file in the Scrapy clone mentions rustmapper,
  Rust-sitemap or the export (grep over `.py` and `.md`). The README itself says "the issue describes" the entry
  point. It is a planned hand-off, not a working one.

This is the one geography no single repository draws: a URL found by rustmapper can be organised by url-organizer and
was meant to feed Scrapy's stages.

### F6. The route in is broken on the page today: `pip install rustmapper` does not give a `rustmapper` command [1, 3, 5, 6, 15, 20, 46]

The profile README tells a visitor to run `pip install rustmapper` then `rustmapper crawl --start-url <your-site>`.
What PyPI actually serves:

- Version 0.1.3, uploaded 8 Nov 2025, four uploads in 74 minutes, one wheel only:
  `cp313-cp313-macosx_11_0_arm64`, plus an sdist [6, 14].
- The wheel contains a single executable, `rustmapper-0.1.3.data/scripts/rust_sitemap`, and no Python package and no
  entry points. The sdist's `pyproject.toml` says `bindings = "bin"` [6]. maturin packages a `bin` binding's binary as
  a script on `PATH` [46]; a command called `rustmapper` would need an entry point, and there is none [20].
- So on an Apple-silicon Mac with Python 3.13, `pip install rustmapper` installs `rust_sitemap`, and `rustmapper crawl`
  fails with "command not found". On every other platform pip builds the sdist and needs a Rust toolchain, with the
  same result. `from rustmapper import Crawler`, which the repository README shows, fails on the released version
  everywhere: the Python wrapper (`python/rustmapper/`, pyo3 mixed layout, `pyproject.toml:54-60`) was added on
  7 Oct 2026 (#41) and has not been released [3, 5].
- The repository README knows this and says to `alias rustmapper=rust_sitemap` (README 25); the profile page does not.
- 39 commits have landed since the release, among them the Python API, `classify`, Parquet/Delta export, the metrics
  server, idle exit and the WAL limits. None of that is in what `pip` installs [5]. The released CLI also differs:
  its `--workers` default is 256, HEAD's is 512 [6, 2].

For a stranger, the most useful single fact about rustmapper is which command works after install. The page currently
states one that does not.

### F7. The same quantity has five different values across the docs, so every printed figure must name its source [1, 2, 3, 6, 14]

Workers: README "Governor: adaptive concurrency control (32-512 workers)" (README 213); CLI default 512
(`cli.rs:34`); governor floor and ceiling 256 and 1,024, overridable by `GOVERNOR_MIN_PERMITS` / `GOVERNOR_MAX_PERMITS`
(`governor.rs:26-34`); library default 256 (`bfs_crawler.rs:78`); `pyproject.toml` description "256 workers"; the
released 0.1.3 CLI 256 [6]. The governor never shrinks the pool below `min_permits` (`governor.rs:54`), so with the CLI
default of 512 it moves between 256 and 512 unless the environment changes it. `stats.json` `claims.workers` records
"256-1024" from the governor with `measured: false` [14]. Round-6 R3 implication 5 quotes "32-512 workers, adaptive";
that is the stale README figure. Alert rules: Scrapy's README says 41 (README 272); the file has 42 [8]. go_go_go's
Bloom filter: the README says "handles 100M+ URLs", the code comment says "~10M URLs", the constant is 100,000,000 at
1 % [10]. Scrapy "summaries from BART-large-CNN" on the profile page is true of Stage 4 only; Stage 3's summaries are
the first sentences of the text [8, 15].

### F8. Some numbers are measurements and some are design targets, and the projects say which [1, 7]

Measured once and dated in the README: resume after `kill -9` on a 400-page site, debug build, restore scan 3 ms, 354
URLs re-queued, 2 pages fetched again (README 258-262). Stated without a method: "50-200 URLs/minute" and the per-URL
timing breakdown (README 107-112). Scrapy says outright that its spider figures "are design targets ... not measured
benchmarks" (Scrapy README, Performance). Measured by this repository and defined in the audit: test functions
(rustmapper 176, Scrapy 1,920), CI on the default branch (rustmapper success 7 Oct, Scrapy success 8 Oct), main
language and lines, last non-sweep commit (rustmapper 8 Aug 2026), no git tags in any repository [14].

### F9. Politeness is where the crawlers differ, and the differences matter to anyone who runs them [2, 8, 10, 17, 27, 29, 33, 35, 37]

- rustmapper honours robots.txt by default (`--ignore-robots` turns it off) and also its `Crawl-delay`
  (`frontier.rs:911-961`). `Crawl-delay` is not in RFC 9309 [17] and Google ignores it [27]; rustmapper treating it as
  a floor is stricter than the standard. Per-host error backoff and the "starved hosts" alert are visible in the report.
- Scrapy obeys robots.txt by default (`settings.py:120-121`), runs AutoThrottle, which sets each host's delay toward
  latency divided by the target concurrency [37] (`settings.py:179-185`), caps at 64 concurrent requests and 32 per
  domain (`settings.py:139-141`), and limits depth to 10 with `DEPTH_PRIORITY = 1` (`settings.py:228-229`), so deeper
  pages wait behind shallower ones [35]; Scrapy's own default is depth-first [36].
- go_go_go defaults to two requests per host (`--per-host-concurrency 2`) and respects robots.txt, and it also ships
  browser TLS-fingerprint impersonation with `utls` and header rotation "to bypass JA3 fingerprint detection"
  (go_go_go README). JA3 is the client fingerprint servers use to recognise bots [33]. That is a different stance from
  rustmapper's, and a page that calls go_go_go "the Go sibling" without saying so hides the main difference.
- Google's own crawler slows when a site's response time rises [29]; rustmapper's governor slows when its own database
  slows, not the site (F2.6). Both are real, and they are different signals.

### F10. What a stranger trips on, project by project [1, 7, 9, 10, 11, 12]

- **rustmapper:** the binary is `rust_sitemap` (F6); `--seeding-strategy all` (the default) queries crt.sh and Common
  Crawl and can stall or find internal hosts that time out (README 222-223); a small site takes about 90 s to exit
  after its last page (README 226); `--enable-redis` with a bad URL is fatal by design (README 231); no depth limit,
  and subdomains are in scope (F2.4).
- **Scrapy:** every command must be run from `Scraping_project/` (README 86-89, #334); the spider is `scout`, not
  `scout_spider` (README 241); the Helm chart deploys Stages 1-3 only, Stage 4 needs Compose; Grafana's local password
  defaults to `admin`; the bundled config targets `uconn.edu` (`config.yml:29-30`); first `cargo build` of the Rust
  ingestor compiles librdkafka and needs CMake, OpenSSL and SASL headers.
- **ideal-url-organizer:** the strict `URLRecord(**data)` loader rejects any extra key (`data_loader.py:39-41`); full
  install pulls spaCy, Tesseract and optionally Ollama; the clone has a single commit.
- **go_go_go:** build to `bin/` yourself (`go build -o bin/gogogoscraper ./cmd/gogogoscraper`); `search` needs a crawl
  run with `--enable-sqlite`.
- **rust_llm_logger:** clients call `http://127.0.0.1:3000/proxy/<backend_port>/<endpoint>` (`app.rs:41`), only ports
  in `--allowed-backend-ports` (default 11434, 8080, 8000, 5000); OpenAI-compatible servers report streamed token
  usage only when the request asks for it, hence `--inject-stream-usage` [49 for Ollama's fields]; calls persist only
  with `--metrics-db` (`store.rs:14`).
- **Ai_code_detector:** one command `aicd`; `aicd scan` exits 0, 1 or 2 for low, moderate and high probability, so it
  can gate CI; it is "probabilistic forensics", and the README's own list of AI tells (single author, commit bursts,
  generic messages) matches how many people work, so its output is an estimate, not a verdict.

### F11. The four "Also" projects each have one shape a stranger needs [9, 10, 11, 12, 24, 25]

- **ideal-url-organizer** is a fan-out: one pile of URLs in, 25 groupings out (methods 1-21 on URL structure, 22-25
  on content), including a parent-child tree (`method_13_hierarchical_tree`), a link graph (`method_19`), PageRank
  [24] and HITS hubs and authorities [25] (`link_graph_analyzer.py:72-112`). Its "no regex for URL parsing" rule
  follows RFC 3986's point that URI equivalence is a matter of defined normalisation steps, not string matching
  [19].
- **go_go_go** is rustmapper's route in Go with three additions: headless-Chrome rendering (`chromedp`), SQLite with
  full-text search, Parquet export; and the evasion features in F9.
- **rust_llm_logger** is a tee on a pipe: one request in, the response stream split to the client and to a parser
  task (`proxy.rs:115, 149`), metrics to SQLite, Prometheus at `/metrics` and a dashboard at `/` (`app.rs:45-48`).
- **Ai_code_detector** is a four-stage pipeline: `ingest/` (git loader, file filter, suppressions), `analysis/`
  (AST and tree-sitter, stylometry, structure, duplication, history), `model/` (embedder, classifier, explainer),
  `report/` (JSON, Markdown, HTML, SARIF).

### F12. What the current image draws is not in any project [14, 15, 21, 23, 52]

The current hero places each repository on a row and each week with commits as an island sized by the days in that
week. Its datum is `weeks[]` and `repos[].days`: when Ben committed. Nothing in F2-F11 depends on when a commit was
made. A visitor who reads the islands correctly learns that Scrapy had commits in September 2025 and October 2026 and
that rustmapper was busy in October and November 2025, which the text says faster ("last commit 8 Aug 2026"). The
island shape has no meaning in any project: rustmapper's real "islands" would be hosts (F3), Scrapy's would be tables
(F4). Shneiderman's rule for a visual overview is that it shows the whole collection so the reader can choose where to
zoom [52]; a timeline of commit weeks gives an overview of activity, which is not what a visitor came to choose among.

### F13. What a stranger needs from a page about software has a known order [50, 51, 52, 53, 54]

GitHub's stated purpose for a profile README is to "tell other people about yourself" [53]. Diátaxis separates four
needs: learning (a tutorial), a goal (a how-to: "practical directions to help the user who is in that situation"),
facts (reference) and understanding (explanation, "put things in a bigger picture") [51]. C4 describes a system at the
level of its containers, "applications and data stores", and the relations between them, before any code [50].
For these projects that order is: what the system is and how its parts connect (C4 context and containers: F2, F4,
F5), the command that works (how-to: F6), the facts with sources (reference: F7, F8), the traps (F10). GitHub renders
Mermaid in Markdown files [54], and Scrapy already uses it, so a diagram drawn only to restate one repository's
pipeline would duplicate what its own README shows.

## What this means for the owner's image and page

Each implication is something a reviewer can check against the image or the page, and each answers his test: does this
element teach a visitor something true about the projects, with a reason it has to be a picture?

1. **Base the main picture on the route a URL takes through his crawl work, not on time.** The stops are the ones in F2
   (seed, shard, seen-test, scope, host wait, worker, fetch, WAL and redb, JSONL, sitemap or Parquet, done) and, if
   Scrapy is drawn, the tables in F4. Purpose: it is the only geography the projects really have (F3, F4). Test: every
   stop and every line on the image names a file or table that `grep` finds in the clones, and no element's position
   is set by a date.

2. **Draw the cross-project hand-offs, and draw them as they really are.** rustmapper → url-organizer is built (solid);
   rustmapper → Scrapy's `stage1_discovery` is designed but has no reader in Scrapy (shown as not yet connected, or left
   out); url-organizer → viewer is a spec plus a server. Purpose: no repository README shows this system, and it is the
   strongest evidence that the projects are one body of work (F1, F5). Test: for each line between two projects, a
   reviewer can open the file that implements it; a line without such a file is not drawn as working.

3. **If a shape stands for a place, it must be a place in the system.** Candidates with a real meaning: hosts (with the
   five states rustmapper itself reports), tables, stores (redb, Delta, Redis, Postgres), outputs (`sitemap.jsonl`,
   `sitemap.xml`). Islands for weeks, and island size for commit-days, go. Purpose: answers his "why the hell would you
   have tiny islands to represent projects" with the only defensible reading (F3, F12). Test: for every filled shape,
   the reviewer can say what real thing it is and what its size or position measures, in one sentence with a source.

4. **Fix the install line before drawing anything.** Either change the page to `pip install rustmapper` then
   `rust_sitemap crawl --start-url <site>` with the platform note (prebuilt for macOS arm64 on Python 3.13, otherwise
   a Rust toolchain), or release 0.1.4 from HEAD with the Python wrapper and a `rustmapper` entry point and then keep
   the current lines. Purpose: the route in is the most helpful fact a stranger can get, and today it fails (F6).
   Test: in a clean Python 3.13 environment, every command printed on the page runs and prints help or output.

5. **Print one value per figure, from the file it comes from.** Workers 256-1,024 (governor) or "512 by default,
   adaptive" (CLI), never "32-512"; 50,000 URLs per sitemap file; WAL fsync every 100 ms; crawler scraped every 30 s; 14
   Delta tables; 42 alert rules; 176 and 1,920 test functions. Purpose: the standing rule "never print a figure without
   a definition the audit stands behind", and F7 shows the docs disagree with each other. Test: every number in the SVG
   and the README has a row in a source table (file and line, or `stats.json` key) in the build script or `AUDIT.md`.

6. **Say which numbers are measured.** The resume figures (3 ms, 354 re-queued, 2 refetched) are one dated local run;
   "50-200 URLs/minute" is unmeasured; Scrapy's throughput figures are design targets by its own statement. Purpose:
   honest data only (F8). Test: no unmeasured throughput figure appears on the image; any measured one carries its
   conditions.

7. **Correct the two text claims that overstate.** "Summaries from BART-large-CNN" becomes Stage 4 (large documents)
   only, with Stage 3 extractive; "the Go sibling of rustmapper" says what differs (Chrome rendering, SQLite search,
   TLS-fingerprint impersonation). Purpose: what the projects actually do (F4, F9, F11). Test: each sentence on the
   page about a project can be matched to a file and line in that project.

8. **Put each kept detail where it belongs on the route.** The "30 s" light means Prometheus scrapes the Scrapy
   crawler every 30 s: if it stays, it sits at the monitoring stop of the Scrapy route, not on a commit row. "0.1.3 ·
   PyPI" sits at the install end of rustmapper with its date (8 Nov 2025), because a visitor needs to know the release
   is eleven months older than the code. Purpose: every mark answers "what does a visitor learn here" (F6, F12).
   Test: remove any one mark; if nothing a visitor could act on is lost, the mark should not have been there.

9. **Give each "Also" project its one shape in words, not in the picture.** url-organizer is a fan-out, rust_llm_logger
   a tee, Ai_code_detector a four-stage pipeline (F11). These belong in one plain line each under the image; they do not
   need a chart, because nothing in them is navigated by the reader. Test: the image shows only what has a route, a
   boundary or a hand-off with the crawl system; the fifteen unrelated repositories appear in the text list only.

10. **Keep it legible at 390 px by keeping the route linear.** rustmapper's route has about ten stops and Scrapy's main
    channel four plus two branches; drawn top-to-bottom on the phone and left-to-right on the desk, each fits.
    Purpose: phone first, and a stranger must be able to follow one URL from entry to output. Test: at 390 px every
    stop label is readable without zooming, and a reviewer can trace one URL from seed to `sitemap.xml` in under ten
    seconds.

11. **Do not draw a crawl that was never run.** No public repository holds crawl results (`data/` is gitignored in all
    of them). If the picture shows real hosts, depths or states, they must come from a crawl Ben runs and commits with
    its date and command, of a site he is allowed to crawl; otherwise the route is drawn without fabricated volumes.
    Purpose: honest data, nothing invented (F5, F8). Test: any count drawn on the route reproduces from a committed
    file with the stated command.
