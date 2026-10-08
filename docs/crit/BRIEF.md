# Crit brief — Ben Russell's GitHub profile README ("Chart", v8)

## The person
Benjamin S. Russell. GitHub: BenjaminSRussell. Bio: "Scraping enthusiast and full stack developer".
On GitHub since Oct 2024; 24 public repos; ~1,800 commits; 46 followers. Avatar: a sailboat on a river
about to go over a waterfall at golden hour. Email handle contains "sail". Projects (real):
- Scrapy: multi-stage crawler platform (scout spider, analysis, summarization, Delta Lake raw storage,
  PostgreSQL metrics, Redis queues, Prometheus/Grafana, circuit breakers, Docker/K8s, 90%+ tests).
- Rust-sitemap / rustmapper: concurrent sitemap crawler in Rust, up to 512 adaptive workers, sharded
  frontier, write-ahead log, optional Redis, seeds from sitemaps + Certificate Transparency logs +
  Common Crawl; shipped on PyPI as `rustmapper` (v0.1.3) via maturin.
- go_go_go: Go crawler, 256-worker pools, Bloom-filter dedup for 100M+ URLs.
- Elusive_trades_data (HVAC parts search across supplier APIs, zero-shot matching), ideal-url-organizer
  (25+ ways to organize URLs; "no regex" rule), FashionDB, Data-visualizer (Superset-inspired),
  rust_llm_logger (zero-copy stream-tee proxy for LLM servers), mlx_Qwen_data_entry (Qwen-DBA on MLX),
  Ai_code_detector, 3d-swift-globe-widget (MapKit night globe), Spotify_to_apple_music (SwiftUI),
  game_engine (voxel engine in C), cozy-game (RN farming game), Data_science_dev (browser game), Wheel.
Languages: Python, Rust, Swift, C, TypeScript, Go. Builds for macOS/Apple silicon.
He cares intensely about design and wants the profile to read as the work of an expert with a massive
interest in design: "world class, one of a kind, beautiful, stunning, fun, tells a lot about me".

## His verdict on the previous two versions
v7 (minimal, Inter, orange accent, clean cards): "mediocre, not exciting, not well designed, feels basic".
He wants something that "appears like it took a team months of work and years of workshopping",
that "says more than it literally says", with "layers of depth and thought".

## What exists now (v8 "Chart")
Concept: the README is a nautical chart of the open web. Each image is a "sheet" from the same chart.
Type: Instrument Serif (titles, italic asides) + IBM Plex Mono (captions, soundings, log).
Palette: navy ink on cream paper (day), navy night chart (dark). Red cans / green cones as the only
other colours. Sheets: hero (Chart No. 27), soundings (live stats + tide curve), approach-scrapy
(harbour approach), survey-rustmapper (survey fan), log (ship's log terminal), legend (stack), footer
(edge of the chart, waterfall). README copy in a "chart voice" (Approaches, Notes to mariners, Other
waters, Colophon, Off the clock).

Renders (PNG) in this folder: page-day-full.png, page-night-full.png, page-day-top.png,
page-night-top.png, hero-day-2x.png, hero-night-2x.png, approach-scrapy-day-2x.png,
survey-rustmapper-night-2x.png, log-day-2x.png, legend-night-2x.png, soundings-night-2x.png,
footer-night-2x.png. Stills only: on GitHub the boat sails the course (48s), a packet boat runs the
channel (16s), the lighthouse beam sweeps (9s), soundings fill in (14s), the log types itself (14s).

Source: /home/user/BenjaminSRussell/README.md, DESIGN.md, scripts/build_assets.py (sheets),
scripts/chartlib.py (chart engine), scripts/svgkit.py (type as outlines), scripts/build_stats.py.

## Hard constraints (do not propose around them)
- GitHub README: Markdown + a sanitized HTML subset. Images are SVG served through GitHub's proxy
  in <img>: SMIL animation works; JavaScript, external fonts, external CSS, hover and click interactivity
  do NOT. <picture> with prefers-color-scheme works (dark/light editions). <details> works.
- The README column on the profile page is ~870px wide; our sheets are 1280 wide and scale to ~68%.
  On phones it's ~360px. Fine detail must survive that.
- Type must be converted to outlines (no web fonts). Any OFL font from the Google Fonts repo is
  available to vendor.
- Keep each SVG under ~300KB.
- Everything must be honest: no fabricated stats, hobbies, locations, employers, or testimonials.
  Illustrative numbers must be labelled as such.

## What we want from you
Be specific, opinionated and demanding. World-class standard: would a top design studio ship this?
Write to the file named in your instructions. Structure:
1. First impression (3 sentences, honest).
2. What works (brief).
3. Problems and complaints, ranked by impact. Reference specific sheets/areas.
4. Expectations and standards: what would "months of team work" look like here? Concrete, testable.
5. Proposals: ranked, concrete, buildable within constraints. Include at least 3 ideas that add
   layers of meaning (things that say more than they literally say) and at least 2 that increase
   delight/curiosity on a second look.
6. What it currently says about the person who made it, vs what it should say.
