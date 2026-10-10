# Review round 14, reviewer 1: Ben, the owner

10 Oct 2026. I looked at every PNG in `scratchpad/r6/build/round-13/`: the desk sheet at 870 (day and night), the mid
sheet at 746 (day and night), the phone sheet at 390 and 308 (day and night), the README at 1,280 (two screens), 1,180
and 900 (first screen), 390 (six screens) and 360 (seven). I read `README.md`, `SPEC.md`, `LOG.md` round 13 and the
round 12 and 13 reviews. Nothing already fixed is repeated. Every figure was checked against `assets/stats.json`, the
0.1.3 sdist and the clones, and this round I ran Scrapy's own code for the one claim I couldn't settle by reading.

Verdict: **not yet. 8 / 10.** The image is done. I would ship it as it is, on every edition. It shows my crawler as the
route a stranger takes: install, seed, fetch, save, the loop, the catch inside the loop, the one key to press, the file,
and the project of mine that reads it. Nothing in it has a size and no word in it names a theme. Round 13's three fixes
landed: rule 1 says "in a row", the four file caveats sit in a labelled fold, and W1 says what saving buys you.

What drops the score is the Scrapy half of the page, where two sentences say things my code doesn't do. One of them was
added last round. "The data doesn't look exactly accurate" was my complaint from the start, and a false sentence about
my own tool is worse than an ugly picture.

1. **"It obeys `robots.txt` and its `Crawl-delay`" is true of Scrapy's spider and false of the system the README
   starts.** The scout obeys both. But the scout puts every link into `stage2_queue` *before* it requests it, and puts
   non-HTML links there without requesting them at all. The stage 2 worker, which `python start.py` starts, then
   fetches every queued URL with aiohttp: no `robots.txt` check, no `Crawl-delay`, 4 at a time per host, and no
   User-Agent of its own. So a disallowed link on your site gets fetched, as `Python/3.11 aiohttp/3.13.1`, not as
   `<your-bot>`. It also makes the pick sentence's "It" read as rustmapper, whose list says "It ignores `Crawl-delay`"
   ten lines below. Must-fix 1.
2. **"`--reset-delta` loads 143,208 bundled URLs" is false at `96e7a1a`.** Since `b787e65` (8 Oct 2026) the reset goes
   through a guard. `start.py` passes `--force`, which now means `--confirm --yes`, and `--yes` is refused unless
   `ALLOW_LAKE_RESET=1` is set inside the container. `docker-compose.yml` doesn't set it, so the flag loads nothing and
   `start.py` exits 3. I ran the guard with those exact flags (below). Must-fix 2.

## The first question: does it meet my goal?

- **A deep purpose for the map.** Yes. There is one map. It shows the order a URL goes through rustmapper, which only
  a drawing can show (the loop and where the catch sits in it). It is directions, not decoration.
- **True about my projects.** The image, yes, every row (table below). The page, no: two Scrapy sentences
  (must-fixes 1 and 2).
- **Nothing chases a reason.** Yes. Every block has a job a stranger needs done. The `--reset-delta` sentence had one
  (don't crawl a university by accident), but it loses that job once the flag does nothing.
- **Nothing announces the theme.** Yes, on the image, the page, the alt text and DESIGN.md.
- **Reads on a phone.** Yes. The image fits one screen at 390, 360 and 308. The page is about 4,965 CSS px at 390,
  down from 5,213. Both fixes below come out about even on length.

It still doesn't go to `main` until S2 verifies (ROUTE-UNVERIFIED, P1 at Rust-sitemap's HEAD). That one is my job.

## What I ran

**The reset guard.** I loaded `Scraping_project/src/utils/destructive_guard.py` at `96e7a1a` by path (`python3 -I`,
with the audit log sent to the scratchpad), built `start.py`'s arguments (`--force`) with `guard_flags`, and called
`authorize` the way `cmd_reset` does, with no terminal:

```
env without ALLOW_LAKE_RESET -> proceed False, refused, exit 3
  "REFUSED: --yes needs ALLOW_LAKE_RESET=1 in the environment (or drop --yes and type the confirmation)"
env with ALLOW_LAKE_RESET=1  -> proceed True, authorized
```

`start.py` runs the reset as `docker-compose run --rm --no-deps -T scraper python cli.py reset --force`. The `scraper`
service's `environment:` is `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `DELTA_LAKE_PATH`, `LOG_LEVEL` and `WORKERS`.
There is no `env_file`, and `run` gets the service's configuration [S3]. Compose doesn't pass host variables in unless
they're listed [S4]. `-T` means no terminal, so the typed confirmation can't happen either. `run_command` uses
`check=True` and calls `sys.exit(exc.returncode)`. The Dockerfile sets `ENVIRONMENT=production`, but the guard reads
`ENV` / `APP_ENV`, so it treats the container as development and refuses through the `--yes` branch.

**Stage 2, read in the tree.**
- `src/stage1/scout_spider.py:160-179`. For an HTML link, `_queue_for_stage2(url, …)` is yielded before
  `scrapy.Request(url, …)`. For any other link, only `_queue_for_stage2` is yielded. In Scrapy, items go to the item
  pipelines and requests go through the scheduler to the downloader middlewares [S2]. So the robots middleware can drop
  the request, but the queue row is already written by `pipelines.py:771`.
- `src/stage2/stage2_worker.py`. `aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=30))`
  (`:403`) and `session.get(current, allow_redirects=False)` (`:668`) pass no headers. aiohttp then generates the
  User-Agent itself [S1], as `"Python/{major}.{minor} aiohttp/{version}"` [S5]. The image is `python:3.11-slim` and
  `requirements.txt` pins `aiohttp==3.13.1`. `limit_per_host` is `DEFAULT_STAGE2_PER_HOST_CONCURRENCY = 4`
  (`config.yml:195` the same). A numeric `Retry-After` is honoured (`_retry_delay`).
- `grep -rli robots src` gives `settings.py`, `common/url_value_assessor.py` (a regex that skips `/robots.txt` as a
  URL), and three files under `stage1/`. Nothing in stage 2, the pipelines or the orchestrator checks robots.txt.
- `docker-compose.yml` has `stage2-worker: command: python -m src.workers.stage2_worker`, which runs
  `run_drain_loop(…, idle_seconds=30)`, a continuous worker. `python start.py` brings it up (`docker-compose up -d`).

Google draws the same line I need the page to draw. Its crawlers "always respect robots.txt rules for automatic crawls"
[S6]. Fetchers that act on a user's request "generally ignore robots.txt rules" [S7], and Google says so where it lists
them. Stage 2 is a fetcher started by a crawl, not by a user, so it has no such excuse. The page can't call the whole
system polite.

## Figures checked

| Printed | Source | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.date`; `uploads` 0.1.3 at 2025-11-08T19:52 | yes |
| `rust_sitemap crawl` … sitemaps, certificate logs and Common Crawl | `edition.scripts` `["rust_sitemap"]`; sdist `cli.rs` seeding default `all` | yes |
| up to 20 pages at a time from each host | sdist `state.rs:285` `max_inflight: 20` | yes |
| saved as it goes; export works after a kill | runcheck `export_after_kill` ok (3 `<loc>`), `kill_writes_file` false | yes |
| `Received work item`, 60 s | sdist `bfs_crawler.rs:433`; H1 `audit` sum 30 + 20 + 4 + 1 → 60; runcheck `quiet_slow_page` ok | yes |
| a second press before `Saved to` … without writing the file | sdist `main.rs:539`; runcheck `second_ctrl_c` exit 1, no file | yes |
| `data/sitemap.jsonl`; `url, depth, status_code, title` | runcheck `crawl_ctrl_c` keys present | yes |
| sorted 21 ways by ideal-url-organizer | round 13 check stands (`method_01` … `method_21`) | yes |
| 176 test functions; CI 7 Oct 2026: tests, rustfmt; 16k lines | `repos[Rust-sitemap]`: 176; CI success 2026-10-07; gates `tests`, `rustfmt` (clippy is `\|\| true`, audit `continue-on-error`, so leaving them out is right); Rust 16,390 | yes |
| 256 at a time; `--workers 1` | sdist `cli.rs` test `assert_eq!(workers, 256)`; runcheck `workers_cap` | yes |
| `robots.txt` only over https | runcheck `robots_read` false | yes |
| 3 min, cold cache, 4-core | runcheck `install` median 171.4 s, 4 CPUs | yes |
| Scrapy 1,920 tests; CI selects all but 41; 8 Oct; tests, ruff, mypy, bandit; 69k | `repos[Scrapy]` 1,920; CI success 2026-10-08; Python 69,036 | yes |
| **"It obeys `robots.txt` and its `Crawl-delay`, and waits out a `Retry-After`"** | stage 1: `spider_config.py`, `PoliteRobotsTxtMiddleware` (cap 60 s); stage 2: none of the three for robots, `Crawl-delay` not at all | **stage 1 only** (must-fix 1) |
| **"The last command crawls your site as `<your-bot>`"** | `-s USER_AGENT` reaches the scout; stage 2 sends aiohttp's default | **the scout only** (must-fix 1) |
| **"`--reset-delta` loads 143,208 bundled URLs, 134,807 of them on uconn.edu"** | 143,208 rows: yes. Loads: refused by the guard (above). 134,807: one row is `https://healthcareinnovation.online.uconn.edu ` with a trailing space, which `urlsplit` keeps [S8], so it is 134,808 by hand | **no** (must-fix 2) |
| `UConn-Discovery-Crawler/1.0` | `settings.py:115` fallback, no `scrapy:` in `config.yml` | yes, for the scout |
| `localhost:3000`; `data/delta/` | `docker-compose.yml` `"3000:3000"`; `DELTA_LAKE_PATH=/data/delta`, `./data:/data` | yes |
| Rule 1: 5 in a row, 60 s | round 13 anchors (`record_success` `else:` reset, `:791`) | yes |
| Rule 2: appended, never overwritten | `lakehouse_manager.py` `mode="append"` | yes (the guarded wipe is an operator command, not the raw layer's write path) |
| Rule 3: 6 days, then 5 | `repo_first` 2025-09-25; Prometheus 10-01; panels 10-06 | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | bare clones, `git log HEAD`: Claude 45 of 146; jules 49 + Claude 22 = 71 of 499 (plus 420 mine, 8 dependabot); agent `Co-authored-by` trailers 1 and 30 | yes |
| 15 more | `repo_count` 22 = this profile + 2 + 4 + 15 | yes |

## Must fix, ranked

1. **Say what Scrapy does to a site in both stages, and drop the pick sentence's politeness clause until stage 2
   earns it.** (`chart.toml:50` `pick_polite`; its three `use = "pick_polite"` rows at `:325-347`; the Scrapy run
   sentence in `chart.toml`; the user-agent row at `:352`; `scripts/data/proof.py` gains a `present` check; tests.
   About 40 lines.)
   - **What's wrong.** See "What I ran". The clause was added last round on evidence from stage 1 only: the scout's
     settings, its middleware, and a test of the scout. It reads as a claim about "His Scrapy repository", the subject
     of the sentence before it. A site owner who checks their logs after running my README will see disallowed paths
     fetched by `Python/3.11 aiohttp/3.13.1`. That is the "Perplexity" story in miniature, told about my own profile.
     The pick sentence's "It" also sits ten lines above rustmapper's "It ignores `Crawl-delay`", so even the true half
     reads like a contradiction.
   - **Pick sentence.** Drop the clause. `render_readme.pick_block` already drops it when any `pick_polite` row fails.
     Add a fourth row that fails today:
     `{text = "It obeys robots.txt (stage 2)", use = "pick_polite", repo = "Scrapy", path =
     "Scraping_project/src/stage2/stage2_worker.py", present = [{pattern = '(?i)robots'}], absent = [{path =
     "Scraping_project/src/stage2/stage2_worker.py", pattern = 'ClientSession\((?![^)]*headers=)'}]}`. The clause then
     comes back by itself the day stage 2 checks robots.txt and sends its own name. `proof.py`: `present` is the mirror
     of `absent` (a regex that must match), about 8 lines. Also change the clause's first word to "Scrapy" for that
     day, so it can't be read as rustmapper.
   - **Run sentence**, replacing everything after "install Compose standalone)." (the reset sentence goes too, see 2):
     "It loads no seeds: the last command gives the spider your site and names it `<your-bot>` (without that line,
     `UConn-Discovery-Crawler/1.0`). The spider obeys `robots.txt` and its `Crawl-delay`. The stage 2 worker then
     fetches every link it queued, disallowed ones too, 4 at a time per host, as `Python/3.11 aiohttp/3.13.1`."
   - **Anchors for the new sentence** (`[[figures]]`, typed prose, so FIGURES goes red when the code changes):
     - "disallowed ones too": `scout_spider.py` contains `yield self._queue_for_stage2(url, response.url,
       content_hint)` followed by `yield scrapy.Request(` (an order anchor, as H1 uses). `stage2_worker.py` is
       `absent` `(?i)robots`.
     - "4 at a time per host": `DEFAULT_STAGE2_PER_HOST_CONCURRENCY = 4`, and `config.yml` `per_host_concurrency: 4`.
     - "`Python/3.11 aiohttp/3.13.1`": `Dockerfile` `FROM python:3.11-slim as base`; `requirements.txt`
       `aiohttp==3.13.1`; `stage2_worker.py` `absent` `headers=` on the `ClientSession(` line and on
       `session.get(current`.
     - The scout half keeps the three existing rows, moved from `use = "pick_polite"` to this sentence.
   - **Size.** The pick sentence loses about 2 lines at 390. The run sentence nets about +1 after the reset sentence
     is cut. About −1 line in all. STRINGS-TWICE: "`robots.txt` and its `Crawl-delay`" is printed once, here.
   - **Test.** Today's tree gives no clause in the pick sentence. A fixture `stage2_worker.py` with a robots check and
     `headers={"User-Agent": …}` gives the clause back, starting with "Scrapy".

2. **Cut the `--reset-delta` sentence.** (The run sentence in `chart.toml`; the `[[figures]]` rows "143,208" and
   "134,807 of them on uconn.edu" at `:404-418`; "It loads no seeds by default." becomes "It loads no seeds:" as in
   must-fix 1. About 15 lines.)
   - **What's wrong.** The flag does nothing but exit 3 (above). The sentence's only purpose was the warning that the
     bundled seeds are a university's live site. With the flag refused, a stranger can't load them by accident, and
     the sentence is just false. Its row checked the CSV and never the path that loads it. That is a figure with a
     definition the code no longer stands behind.
   - **Don't replace it with "`--reset-delta` is refused".** That is my to-do list, not the visitor's (the spec's own
     rule for broken joins, section 3).
   - **Guard against it coming back wrong.** The "It loads no seeds" row gains `also = [{path =
     "Scraping_project/cli.py", literal = "guarded_lake_wipe(DELTA_LAKE, args"}]`, and a note in `chart.toml`: if
     `start.py` ever passes `ALLOW_LAKE_RESET=1` (or `-e`) to that `run`, the sentence can come back with the word
     "wipes". `cmd_reset` deletes the whole lake first (`shutil.rmtree(base)`), and the old sentence never said so.
   - **Size.** About 2.5 lines off at 390.

That's all. The image needs nothing.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page this is | keep | first thing read on every edition |
| Role, two caps lines | crawl and data infrastructure; Python and Rust | keep | the route under it proves the first line |
| Empty left column (desk, below the role) | nothing, on purpose | keep | the eye goes to the route; filling it would be decoration |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project and what you get | keep | true with blank rows too |
| Start bar + `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | the date makes every 0.1.3 caution honest |
| Magenta track | one way through, top to bottom | keep | |
| Stop rings | each is one step the tool takes | keep | |
| S1 `rust_sitemap crawl` + seeds | the real command, and where URLs come from by default | keep | the default asks third parties; the open caution gives the flag |
| F1 fetch, 20 per host, scope | the loop's work and how far it reaches | keep | |
| W1 "saved as it goes; export works after a kill" | a kill doesn't throw away the crawl's sitemap | keep | round 13's wording holds by the run check. "export" is named in the code block right under it |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| H1, red dotted box, inside the loop | 0.1.3 never exits, and how you know it's done | keep | goes when 0.1.4 ships |
| Gap in the track under the loop | the only way out is you | keep | |
| C1 Ctrl-C once | the one key, and the second press not to make | keep | |
| End bar + `data/sitemap.jsonl` + fields | the file, in the struct's own names | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | my projects feed each other | keep | tested reader |
| Night editions | the same | keep | contrast holds; the red box reads on navy |
| Mid editions (852 to 1,199) | the same, on one tablet screen | keep | the whole route is above the fold at 1,180 and 900 |
| Phone editions (390, 308) | the same, on one phone screen | keep | the smallest text at 308 is still legible |
| Alt text | install, loop, stop, file | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image link to the repository | where the project lives | keep | |
| `<picture>` sources | the right sheet for the width | keep | |
| Link line | where to go | keep | |
| "Ben Russell builds …" | what I build | keep | |
| Languages | what I write in | keep | |
| Stack | what I build on | keep | |
| Pick sentence, first two sentences | which tool for which job | keep | |
| Pick sentence, politeness clause | (claims) Scrapy is polite | **cut, gated** | must-fix 1: stage 1 only |
| rustmapper facts line | alive, tested, size, which commit | keep | |
| Wheel note | whether `pip` just works on your machine | keep | |
| "Before you run 0.1.3:" (four open items) | what it does to someone else's server, and the lever for each | keep | |
| Fold "What 0.1.3's files miss or get wrong" | the file caveats, one step away | keep | round 13's split works: one line at 390, two at 360 |
| rustmapper code block | how to run it, when to stop, how to recover | keep | |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy bullets 1–3 | storage, what happens to a page, how it's watched and deployed | keep | |
| Scrapy run sentence, up to "standalone)" | what `start.py` starts and needs | keep | |
| `--reset-delta` sentence | (claims) the flag loads UConn's URLs | **cut** | must-fix 2 |
| User-agent sentence | who the crawl says it is | **change** | must-fix 1: both stages |
| Scrapy code block | how to point it at your site and name your bot | keep | the `-s USER_AGENT` line is right for the scout |
| Grafana and `data/delta/` | where to look once it runs | keep | |
| Also: four tools | the file's reader, the Go sibling, two more tools by what they do | keep | |
| 15 more (fold) | the rest | keep | |
| Working rules 1–3 | how I build, each with its evidence | keep | |
| Found a mistake? | the page can be corrected | keep | this round shows why it's there |
| Data line | which release is drawn, how it was run, who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Noted, not ranked

- The 360 code block's two 32-column comment lines still touch the padding (rounds 12 and 13). Unchanged and still
  legible.
- `proof.csv_rows` with `host` misses one row with a trailing space (134,807 against 134,808 by hand). It goes away
  with must-fix 2. If a host count is printed again, strip the field the way the reader does, or say "rows whose host
  is".

## Owner notes, outside this repository

1. **New: Scrapy stage 2.** Check `robots.txt` before fetching. The cheapest fix is to stop the scout queueing a URL
   for stage 2 until the request for it comes back. That covers HTML links. Non-HTML links need a robots check in
   stage 2 itself. Also set a `User-Agent` on stage 2's `ClientSession` from the same setting as the scout, and give
   it a per-host delay from `Crawl-delay`. RFC 9309's product token is meant to be "a substring of the identification
   string that the crawler sends", which stage 2 can't be today. The pick clause comes back by itself after that.
2. **New: `start.py --reset-delta`.** It passes `--force` into a container that lacks `ALLOW_LAKE_RESET=1`, so it is
   always refused. Pass `-e ALLOW_LAKE_RESET=1` on that `docker-compose run`, or drop `-T` and `--force` so the typed
   confirmation can happen. Then fix its help text ("Reset Delta Lake tables and reload seed URLs") to say it wipes
   them first. `start.py` itself prints "Use '--reset-delta' to wipe and reseed" every time it starts.
3. **Carried:** 0.1.4 (exits when idle, P1, `response.url()` as the base, `noindex` and canonicalized pages left out
   of `export-sitemap`, `resume` after a kill, the robots.txt port, a LICENSE, `[project.scripts]`); Scrapy's default
   user agent; the GitHub bio; the iOS and Android apps; one look on a real iPad.

## Sources (new this round; none cited in earlier rounds)

The web search budget for this run was used up before I started. Every source below was opened directly and read.

1. [S1] aiohttp, "Client Reference": aiohttp "autogenerates headers like User-Agent or Content-Type if these headers
   are not explicitly passed", and `ClientSession(headers=…)` is how a session sends its own on every request. Stage
   2 passes none (must-fix 1): https://docs.aiohttp.org/en/stable/client_reference.html
2. [S2] Scrapy, "Architecture overview", data flow step 8: the engine "sends processed items to Item Pipelines" and
   "sends processed Requests to the Scheduler". Requests reach the downloader middlewares only later. That's why a
   queue row written as an item gets past the robots middleware (must-fix 1):
   https://docs.scrapy.org/en/latest/topics/architecture.html
3. [S3] Docker, `docker compose run`: one-off commands "start in new containers with configuration defined by that of
   the service". `-e` is the only way to add a variable for one run (must-fix 2):
   https://docs.docker.com/reference/cli/docker/compose/run/
4. [S4] Docker, "Set environment variables within a container": variables are set with `environment` or `env_file`.
   Host values pass through only when you list the name without a value. The `scraper` service lists no
   `ALLOW_LAKE_RESET` (must-fix 2):
   https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/
5. [S5] aiohttp source at the pinned 3.13.1, `aiohttp/http.py`:
   `SERVER_SOFTWARE = "Python/{0[0]}.{0[1]} aiohttp/{1}".format(sys.version_info, __version__)`. That gives the exact
   string printed in must-fix 1: https://raw.githubusercontent.com/aio-libs/aiohttp/v3.13.1/aiohttp/http.py
6. [S6] Google Search Central, "Overview of Google crawlers and fetchers": common crawlers "always respect robots.txt
   rules for automatic crawls". That is the standard "obeys robots.txt" sets for a crawl system, all of it:
   https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers
7. [S7] Google Search Central, "Google's user-triggered fetchers": "Because the fetch was requested by a user, these
   fetchers generally ignore robots.txt rules". The one accepted exception is a user's own request, and Google states
   it openly. Stage 2 is neither (must-fix 1):
   https://developers.google.com/search/docs/crawling-indexing/google-user-triggered-fetchers
8. [S8] Python, `urllib.parse`: `urlsplit` strips "leading C0 control and space characters" and removes `\n`, `\r`
   and `\t` anywhere. Trailing spaces are kept, which explains the off-by-one in the uconn.edu count (noted):
   https://docs.python.org/3/library/urllib.parse.html
9. [S9] MDN, "User-Agent": the header "lets servers and network peers identify the application … of the requesting
   user agent", and crawler strings carry a name and a URL (`+http://www.google.com/bot.html`). A site owner reading
   their logs can't tell `Python/3.11 aiohttp/3.13.1` belongs to my crawl (must-fix 1, owner note 1):
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent
