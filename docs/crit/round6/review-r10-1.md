# Review round 10, reviewer 1: Ben, the owner

10 Oct 2026. I looked at every PNG in `scratchpad/r6/build/round-09/`: the desk sheet at 870 (day and night), the
phone sheet at 390 and 308 (day and night), the desk page (two screens) and the phone page at 390 (six screens) and
360 (seven). I read `README.md`, `SPEC.md`, `LOG.md` (round 9's fixes) and every review from rounds 1 to 9. Nothing
already fixed is repeated here. I checked every figure against `assets/stats.json`, the 0.1.3 sdist
(`scratchpad/r6/sdist013`) and the clones (Rust-sitemap `32c2651`, Scrapy `96e7a1a`, ideal-url-organizer `159968a`).

Verdict: **not yet. 8 / 10.** Round 9 landed. The cautions are now one list, the to-do line is gone, the Scrapy
sentence agrees with its `cd`, S1 has its verb, H1 has its number, and the facts lines say which CI gates block.

The image is done. I'd ship it the day 0.1.4 passes the run check, and I wouldn't move a mark. Top to bottom it's
how you get my crawler, where its URLs come from, the loop it runs for every page, where it catches you, how you get
out, what file you get and which of my projects reads that file. Nothing in it has a size, nothing names a theme,
and nothing is there to look nautical. The two marks that carry the manner are real chart practice used for what
they mean: one line you follow, and a dotted line drawn round the one danger.

What I won't ship is two sentences of text, and both have the same problem: **they say something my code doesn't
do.** The Scrapy run sentence says `python start.py` "crawls a university's sample site". On a fresh clone it loads
no seeds at all. The bundled "sample" behind `--reset-delta` is 143,218 URLs of a live university's site. The
rustmapper list sits right under "on main at `32c2651`" and states two defaults, 256 workers and seeding on, that
main no longer has. That's the complaint I started with: "the data doesn't look exactly accurate". It's the last
kind of mistake I want on this page.

## The first question: does it meet my goal?

- **A deep purpose for the map.** Yes. Only a drawing shows the loop, and only a drawing shows where in the loop
  the trap sits. Take away the colour and it still reads as directions.
- **True about my projects.** The image, yes, line by line (table below). The page, not quite: must-fix 1 and 2.
- **Nothing chases a reason.** Yes. Every row of the image answers "what do I do, what happens, what goes wrong".
  Every block of the page names a project fact. The weakest block is working rule 4. It's still true, it's mine and
  it's dated, so it stays (see the audit).
- **Nothing announces the theme.** Yes. There's no theme word anywhere, and no wink.
- **Reads on a phone.** Yes. The image fits one screen at 390 and at 308. The page is six screens at 390, and
  must-fix 1 doesn't lengthen it.

## Figures checked

| Printed | Source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.date`; four uploads all 8 Nov 2025 | 0.1.3, 2025-11-08 | yes |
| by default also from sitemaps, certificate logs and Common Crawl | sdist `cli.rs` `default_value = "all"` | | yes for 0.1.3. At HEAD the default is `"none"` (`src/cli.rs:53`) |
| up to 20 pages at a time from each host | sdist `state.rs` `max_inflight: 20` | 20 | yes |
| logged to disk, then saved to redb, in batches | sdist `writer_thread.rs:11` `BATCH_TIMEOUT_MS: 50`; `wal.rs:152` "fsync batching" | | yes |
| never exits by itself; `Received work item` | runcheck `ends_by_itself` false at 150 s; sdist `bfs_crawler.rs:433` `eprintln!("Crawler: Received work item: …")` | | yes. It's an `eprintln!`, so it shows at any log level |
| quiet for 30 s | runcheck `quiet_slow_page` ok; timeout 20 + backoff 4 + 1, rounded up | 30 | yes |
| a second press before `Saved to:` quits without writing | runcheck `second_ctrl_c`: exit 1, no file | | yes |
| fields url, depth, status_code, title | sdist `state.rs` `SitemapNode` | | yes |
| sorted 21 ways by ideal-url-organizer | `self.methods` 21 keys; `scripts/import_rust_sitemapper.py` reads `sitemap.jsonl` at `159968a`, with its test | 21 | yes |
| up to 256 at a time across all hosts; `--workers 1` | sdist `cli.rs` 256; runcheck `workers_cap` | 256 | yes for 0.1.3. At HEAD the default is `512` (`src/cli.rs:34`) |
| crt.sh and Common Crawl by default | sdist `ct_log_seeder.rs`, `cli.rs` `"all"` | | yes for 0.1.3; no at HEAD |
| robots.txt only over https; ignores Crawl-delay | sdist `robots.rs` `format!("https://{}/robots.txt"…)`; runcheck `robots_read` | | yes |
| 50,000 URLs per file | `DEFAULT_MAX_URLS_PER_SITEMAP`; sitemaps.org | 50,000 | yes |
| no `status_code` for 404, 429, 503 | runcheck `non200_status` | | yes |
| 3 min, cold cache, 4-core | runcheck install median 171.4 s, 4 CPUs | | yes |
| `32c2651` · 176 tests · CI 7 Oct: tests, rustfmt · 16k Rust | `repos[Rust-sitemap]`: head, 176, success 2026-10-07, gates `["tests","rustfmt"]`, 16,390 | | yes |
| `96e7a1a` · 1,920 (all but 41) · CI 8 Oct: tests, ruff, mypy, bandit · MIT · 69k | `repos[Scrapy]`; `ci_selection.not_selected` 41; gates; 69,036 | | yes |
| "`python start.py` … crawls a university's sample site" | none: no `[[figures]]` row; see must-fix 1 | | **no** |
| 5 URLs, 60 s breaker | `stage2_worker.py` | 5, 60 | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | Rust-sitemap 101 + Claude 45; Scrapy 420 + jules 49 + Claude 22 + dependabot 8; `coauthored.agent` 1, 30 | | yes |
| Rule 3: 6 days, then 5 | `67446a4` 25 Sep → `d571e6e` 1 Oct → `e8cbe15` 6 Oct 2025 | | yes |
| 15 more | 11 listed + 4 on the "Also:" line | 15 | yes |

## Must fix, ranked

1. **The Scrapy run sentence says what `start.py` does** (`README.md:73`, hand-typed; `chart.toml` new
   `[[figures]]` rows near `:312-343`; `tests/test_pipeline.py:495-498` and `tests/test_round9.py:133-138`. One
   sentence rewritten, three figures rows, two test strings.)
   - What the code does at `96e7a1a`:
     - `start.py:345` runs `docker-compose up -d`. The `scraper` service runs `python -m src.main`, which runs the
       orchestrator's `run_full_pipeline(stage1_url_limit=50, …)` (`pipeline_orchestrator.py:398-410`).
     - The scout spider's start URLs are `-a start_urls` or else the Delta table `seed_urls`
       (`src/stage1/experimental/base_spider.py:134`). If that table can't be read, `_load_seed_urls` logs an error
       and returns `[]` (`:153-161`).
     - Nothing loads `seed_urls` on a fresh clone. The only writers are `cli.py reset` (`:353-368`), `reseed.py`
       and `scripts/reset_lake.py`, and `start.py` calls `cli.py reset` only `if args.reset_delta:` (`:355`). By
       default it prints "Skipping Delta Lake reset."
     - `--reset-delta` loads `data/raw/uconn_urls.csv`. pandas reads it with `header=None` and skips blank lines,
       which gives 143,218 rows, 134,745 of them on `uconn.edu` or a subdomain, across 2,221 hosts (counted today).
       Scrapy's own README tells a reader to run exactly that ("# Reset everything / python start.py
       --reset-delta", `README.md:288-289`).
   - So the page is wrong both ways. Without the flag nothing is crawled, so "crawls … sample site" is false. With
     the flag the "sample" is a live third party's site at 143,218 URLs, and the word "sample" hides that. A stranger
     needs that warning more than anything else in the Scrapy block.
   - New sentence, the same length as today's (about 65 words; the `cd` already shows where to stand, so "start.py
     runs only inside `Scraping_project`" goes):

     > Run these from the folder you cloned [Scrapy](…) into. `python start.py` starts PostgreSQL, Redis, Grafana and
     > a worker for each of the four stages. It needs Docker and the `docker-compose` command (Docker Desktop has it;
     > on Linux, install Compose standalone). It loads no seeds unless you add `--reset-delta`, which loads 143,218
     > bundled URLs, 134,745 of them on uconn.edu. The last command crawls your site.

   - Anchors, as `[[figures]]` rows so that FIGURES fails if the code moves:
     - "loads no seeds": `start.py` contains `if args.reset_delta:` and `LOCAL_SEED_FILE = Path("data/raw/uconn_urls.csv")`;
       `base_spider.py` contains `or self._load_seed_urls()` and `return []`.
     - "143,218": a new kind `csv_rows` (non-blank lines of `Scraping_project/data/raw/uconn_urls.csv`).
     - "134,745 of them on uconn.edu": the same rows whose `urlsplit().hostname` is `uconn.edu` or ends in `.uconn.edu`.
     - "a worker for each of the four stages": `docker-compose.yml` has `stage1-worker` to `stage4-worker`.
   - Test: the strings check fails any visible "sample site" with no figures row, and the order tests read the new
     opening "Run these from the folder you cloned [Scrapy](…) into."
   - Why: honest data, the rule I've held since round 1. This claim has no figures row, so nothing has ever checked
     it. NOAA had to pull its own magenta line from the Intracoastal charts because, left unchecked against the
     water, it came to pass "on the wrong side of aids to navigation" and to cross "shoals, obstructions" [S2]. A
     drawn route nobody re-surveys becomes a hazard, and so does a run sentence. Scrapy's own guide asks a crawler to
     go no faster than a person browsing, "2 seconds apart or more" [S4]. A stranger should know before pressing
     Enter whose site the bundled seeds point at. uconn.edu's live robots.txt (read today) sets no Crawl-delay and
     allows nearly everything, so nothing on their side will slow a stranger down [S5].

2. **The rustmapper list says which release it's about** (`chart.toml:486` `list_lead`; the `text` of L4 `:765`,
   X1 `:818`, X2 `:839` and their `instead` strings; `render_readme.py:598`, where the lead is filled; tests in
   `tests/test_round9.py:69, :93, :103-104`. Four strings, one format call, four test lines.)
   - Lead: `list_lead = "Before you run {release}:"`, which prints "Before you run 0.1.3:". Fill it with the same
     `{release}` as the text entries.
   - Drop the leading "{release} " from L4, X1 and X2, so they read "It ignores `Crawl-delay`, …", "It writes one
     `sitemap.xml` …", "It gives no `status_code` …". The image's H1 keeps its own "0.1.3", because the image has no
     lead-in.
   - Why: all six items are `scope = "release"`, and two of them are false on main. Main's `src/cli.rs` defaults
     `--workers` to `512` (`:34`) and `--seeding-strategy` to `"none"` (`:53`). The facts line right above the
     list says "on main at `32c2651`". As printed today, a reader who clones main is told 256 and "by default it asks
     crt.sh" about a build that does neither. The Kubernetes docs style guide gives the rule in one line: write "In
     version 1.4, …", not "In the current version, …" [S6]. One lead-in that names the release scopes all six items
     and removes three repeats of "0.1.3", so the flagship reads less like a list of confessions. When a release
     retires every item, the lead goes with them, as it does now.
   - Test (README-CAUTIONS): if any list entry has `scope = "release"`, the lead contains the release number, and
     no list item starts with it.

That's all. The image needs nothing. The other blocks keep their purpose (audit below).

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page | keep | the first thing on the profile, and the only name in link previews |
| Role line, two caps lines | crawl and data infrastructure; Python and Rust | keep | the drawing under it proves the first line |
| Empty left column under the role (desk) | nothing, on purpose | keep | the space makes the route the thing you read |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project, what it gives you | keep | |
| Start bar + `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | the date is the honest answer to "is this current" |
| Magenta track | one way through, top to bottom | keep | one line you follow, in the colour a chart keeps for a route [S2] |
| Stop rings | one step the tool takes | keep | |
| S1 seeds | URLs come from more than links, by default | keep | the image is scoped by its install row; it's true for 0.1.3 |
| F1 fetch, per-host cap, scope | the loop's work and how far it reaches | keep | |
| W1 write path | it saves as it goes, to an embedded store | keep | it's why `export-sitemap` works after a kill (runcheck `export_after_kill`: 3 `<loc>`), and it names the design |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Gap in the track under the loop | there's no exit from the loop but Ctrl-C | keep | |
| H1, red dotted box | the catch in 0.1.3, and how you know you're done | keep | a danger line drawn round the danger, with a clearing mark. That's what a navigator wants marked. It retires when 0.1.4 lands |
| C1 Ctrl-C | the one thing you do, and the second press to avoid | keep | |
| End bar + `data/sitemap.jsonl` + fields | what you get, in the struct's own field names | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | my projects feed each other, and that's tested | keep | the reader script and its test exist at `159968a` |
| Night editions | the same | keep | the box and track hold contrast |
| Phone editions (390, 308) | the same, in one screen | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image + alt text | above | keep | |
| Link line | where to go | keep | |
| "Ben Russell builds …" | what I build | keep | |
| Languages | what I write in | keep | from the data |
| Stack | what I build on | keep | |
| Pick sentence | which tool for which job | keep | |
| rustmapper facts line | alive, tested, size, which commit, which gates | keep | it's also why must-fix 2 is needed: it dates main, and the list is about 0.1.3 |
| rustmapper code block | how to run, stop and recover | keep | |
| Wheel note | whether pip just works on your machine | keep | |
| "Before you run it:" + six items | what it does to a server, what it can't see, what the file leaves out | change | must-fix 2: scope the list to 0.1.3 |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy bullets | what Scrapy does that rustmapper doesn't | keep | |
| Scrapy run sentence | what `start.py` starts, what it needs, whose site the seeds hit | change | must-fix 1: the claim is false both ways |
| Scrapy code block | how to start it, and how to point it at your site | keep | |
| Grafana note | where to look once it runs | keep | |
| Also (four lines) | four more projects, each by what it does | keep | |
| 15 more | the rest | keep | spot-checked: ISRC matching in `Spotify_to_apple_music` tests, Three.js in `Wheel/src`, Expo in `cozy-game/package.json`, Reddit in `FashionDB/reddit_db`, zero-shot in `Elusive_trades_data` |
| Working rules 1–3 | how I build crawlers, each with a dated cite | keep | |
| Working rule 4 | how I parse URLs | keep | it's the thinnest rule, but it's mine, dated, and checked (no regex URL parsing in `src`). Three rules would also be fine, and that's my call, not a must |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn, how it was run, who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Owner, outside this repository (not ranked here)

1. **New: Scrapy's defaults point at a third party.** `config.yml` `stage1.allowed_domains: [uconn.edu]` and the
   143,218-row seed file make a stranger's first `--reset-delta` a crawl of UConn. Move them to a named profile
   (`config/profiles/uconn.yml`), and have `--reset-delta` with no seed file refuse to load any seeds. Then the
   page's sentence gets shorter by itself.
2. **New, check before acting:** the `scraper` service has `restart: unless-stopped` (`docker-compose.yml:13`), and
   `src.main` returns once the pipeline is done. Docker restarts a container like that whenever it stops [S3], so
   with seeds loaded the 50-item pipeline may run again and again until `docker-compose down`. Each run can send up
   to `CONCURRENT_REQUESTS` (1,024 for scout) before the item cap closes the spider. Watch `docker-compose ps` for
   an hour on a seeded clone. If it loops, use `restart: "no"` or `on-failure`.
3. Carried from rounds 4 to 9: fix P1 and ship 0.1.4 (the red box and four list items retire by themselves); commit
   Rust-sitemap's LICENSE; `start.py` accepting `docker compose`; `resume` after a kill; the registrable-domain
   seeders; status codes and back-off on 429/503 (RFC 6585 lets a server send `Retry-After` "indicating how long to
   wait" [S1], and 0.1.3 reads none); `cargo audit`, `clippy -Dwarnings`.

## Sources (new this round)

1. [S1] RFC 6585, §4 "429 Too Many Requests": a 429 "MAY include a Retry-After header indicating how long to wait
   before making a new request". That's what X2's 429 row throws away: https://www.rfc-editor.org/rfc/rfc6585.html
2. [S2] NOAA, "Intracoastal Waterway Route 'Magenta Line' on NOAA Nautical Charts", Federal Register 2013-23440:
   the line "passes on the wrong side of aids to navigation; crosses shoals, obstructions, shoreline; and falls
   outside of dredged channels", so Coast Survey is "systematically removing" it. A route that isn't re-checked
   becomes a hazard, and that's must-fix 1:
   https://www.govinfo.gov/content/pkg/FR-2013-09-26/pdf/2013-23440.pdf
3. [S3] Docker Docs, "Start containers automatically": `always` means "Always restart the container if it stops";
   `unless-stopped` is "similar to `always`" except after a manual stop. That's owner item 2:
   https://docs.docker.com/engine/containers/start-containers-automatically/
4. [S4] Scrapy documentation, "Common Practices: Avoiding getting banned": space requests "2 seconds apart or more"
   with `DOWNLOAD_DELAY`, "to keep your pace closer to that of a person browsing":
   https://docs.scrapy.org/en/latest/topics/practices.html
5. [S5] uconn.edu `robots.txt`, read 10 Oct 2026: `User-agent: *` with WordPress admin and search paths disallowed,
   no `Crawl-delay`, and a `Sitemap:` line. Nothing on the site's side paces a stranger's crawl:
   https://uconn.edu/robots.txt
6. [S6] Kubernetes documentation style guide, "Avoid statements that will soon be out of date": do write "In version
   1.4, …", don't write "In the current version, …". That's must-fix 2:
   https://kubernetes.io/docs/contribute/style/style-guide/
7. [S7] The Good Docs Project, README template: "specify any project limitations or when a user would not want to
   use the project", and "List any prerequisites". That's why the six cautions and the Docker sentence stay:
   https://www.thegooddocsproject.dev/template/readme
8. [S8] Salerno, Treude and Thongtanunam, "Open Source Software Development Tool Installation: Challenges and Strategies For Novice
   Developers" (arXiv 2404.14637, 24 observed installation sessions): "unclear documentation, such as installation
   instructions, and inadequate feedback" are the common blockers. A run sentence that says a command crawls when it
   loads nothing is that failure: https://arxiv.org/abs/2404.14637
9. [S9] RFC 9309, re-read for this round: it defines only allow and disallow rules, so Crawl-delay is a convention,
   not the standard. A 4xx robots.txt "MAY access any resources", and a 5xx "MUST assume complete disallow". L4
   rightly says "ignores `Crawl-delay`" and doesn't call it a violation of the standard:
   https://www.rfc-editor.org/rfc/rfc9309.html (cited before; not counted as new)

Clones and data: `assets/stats.json` (`edition`, `runcheck.rustmapper.steps` incl. `kill_writes_file`,
`export_after_kill`, `resume_after_kill`; `repos[]`; `routes.rustmapper.entries`); sdist 0.1.3 `bfs_crawler.rs:433`,
`writer_thread.rs:11-12`, `wal.rs:152-201`; Rust-sitemap `32c2651` `src/cli.rs:34, :53`; Scrapy `96e7a1a`
`Scraping_project/start.py:33, :142-221, :334-376`, `cli.py:331-368`, `src/main.py`,
`src/orchestrator/pipeline_orchestrator.py:80-118, :398-410`, `src/stage1/base_spider.py`,
`src/stage1/experimental/base_spider.py:74-77, :134, :153-170`, `src/lakehouse/seed_manager.py:240-270`,
`config.yml:28-40, :137-154`, `docker-compose.yml:1-35`, `data/raw/uconn_urls.csv` (143,218 rows read; 134,745 on
uconn.edu; 2,221 hosts), `README.md:86-95, :288-289`; ideal-url-organizer `159968a`
`scripts/import_rust_sitemapper.py`, `tests/test_import_rust_sitemapper.py`; `chart.toml:486, :734-839`, its
`[[figures]]` rows (no row for "sample site").
