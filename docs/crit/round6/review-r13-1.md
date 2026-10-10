# Review round 13, reviewer 1: Ben, the owner

10 Oct 2026. I looked at every PNG in `scratchpad/r6/build/round-12/`: the desk sheet at 870 (day and night), the new
mid sheet at 746 (day and night), the phone sheet at 390 and 308 (day and night), the README at 1,280 (two screens),
1,180 and 900 (first screen), 390 (seven screens) and 360 (seven). I read `README.md`, `SPEC.md`, `LOG.md` round 12 and
the round 7 to 12 reviews. Nothing already fixed is repeated. Every figure was checked against `assets/stats.json`, the
0.1.3 sdist (`scratchpad/r6/sdist013/rustmapper-0.1.3`) and the clones.

Verdict: **not yet. 9 / 10.** Round 12 landed. On an iPad held sideways the whole route, the file and the hand-off are
now on the first screen (`page-1180-1.png`), and at 900 the picture is 457 px tall, not a poster. "resume" is gone
from the go_go_go line, the spider sentence is gone, and the redirect caution is true. The image is still right, and I
am not asking for a new picture. It shows my crawler as a route a stranger actually takes, nothing in it has a size,
and no word names a theme.

Three things are left. One is a sentence that says more than the code does. One is a list that grew past its own limit
and is now the densest part of the page on a phone. One is a row in the picture whose reason exists only in our
reviews, not on the picture.

1. **Working rule 1 overstates the breaker.** "When 5 URLs on one host fail every retry" reads as five in total. The
   code counts five in a row: one success puts the count back to zero. Must-fix 1.
2. **"Before you run 0.1.3:" is eight items, and four of them are not about before you run.** The list cap was raised
   from 7 to 8 last round to fit X3, against the style guide the cap itself cites. At 390 the list is about 825 CSS px,
   a full screen of one tool's caveats before the reader reaches Scrapy. Must-fix 2.
3. **W1 says what the tool does inside, not what it does for you.** Seven reviews kept "logged to disk, then saved to
   redb, in batches" because "it's why `export-sitemap` works after a kill". A visitor never reads that reason. It is
   in our review files, not on the image. That is having a reason somewhere else, not having a purpose on the page.
   Must-fix 3.

## The first question: does it meet my goal?

- **A deep purpose for the map.** Yes. The route has a real order (install, seed, fetch, save, loop, stop, file,
  hand-off), the loop and where the catch sits in it can only be shown by drawing it, and the end points at the
  project of mine that reads the file. It is directions, not decoration.
- **True about my projects.** The image, yes, every row (table below). The page, all but working rule 1 (must-fix 1).
- **Nothing chases a reason.** All but W1 (must-fix 3) and the list cap that was moved to fit an eighth item
  (must-fix 2).
- **Nothing announces the theme.** Yes, on the image, the page, the alt text and DESIGN.md.
- **Reads on a phone.** The image, yes at 390, 360 and 308, and now on a tablet too. The page reads, but it is 5,213 CSS
  px at 390 and has grown three rounds running (4,997 → 5,213). The cautions are the densest stretch (must-fix 2).

It still doesn't go to `main` until S2 verifies (ROUTE-UNVERIFIED, P1 at Rust-sitemap's HEAD). That's my job.

## Figures checked

| Printed | Source | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.date`; `uploads` 2025-11-08 | yes |
| `rust_sitemap crawl` … sitemaps, certificate logs and Common Crawl | sdist `cli.rs:58` `default_value = "all"` (seeding strategy); runcheck `crawl_help` | yes |
| up to 20 pages at a time from each host | sdist `state.rs` `max_inflight: 20` | yes |
| its subdomains and its parent domain | sdist `url_utils.rs:81-90` `is_same_domain`: equal, a `.`-bounded suffix either way | yes (any parent, not just one; fine for a stranger) |
| logged to disk, then saved to redb, in batches | `chart.toml:682-699` W1, `drain_batch` anchors | yes (but see must-fix 3) |
| `Received work item` lines, 60 s | sdist `bfs_crawler.rs:433` `eprintln!("Crawler: Received work item: …")`; runcheck `quiet_slow_page` ok | yes |
| a second press before the `Saved to` line quits without writing the file | sdist `main.rs:535-539` `println!("Saved to: …")`; runcheck `second_ctrl_c`: exit 1, no file | yes |
| `data/sitemap.jsonl`; fields `url, depth, status_code, title` | sdist `cli.rs:24` `default_value = "./data"`, `main.rs:535` `join("sitemap.jsonl")`, `state.rs:98-113` `SitemapNode` | yes |
| sorted 21 ways by ideal-url-organizer | `159968a`: `method_01` … `method_21` are the URLRecord pathway; `scripts/import_rust_sitemapper.py` reads `sitemap.jsonl`. Methods 22-25 need page content, so 21 is the right number for this file | yes |
| 176 test functions; 16k lines of Rust; CI 7 Oct 2026 | `repos[Rust-sitemap]`; round 12 recount | yes |
| 3 min from a cold cache, 4-core | runcheck `install` median 171.4 s, 4 CPUs | yes |
| 256 at a time; `--workers 1` | sdist `cli.rs:32` `default_value = "256"`; runcheck `workers_cap` | yes |
| `robots.txt` only over https | runcheck `robots_read` false on the http fixture: `/robots.txt` never asked for | yes |
| X1, X2, X3 | runcheck `sitemap_keeps_noindex` (5 `<loc>`), `non200_status`, `redirect_kept` | yes |
| 1,920 test functions (Scrapy) | counted today: 1,910 `def test_` in `test_*.py`/`*_test.py` + 10 Rust attributes in `kafka-delta-ingest` = 1,920 | yes |
| 69k lines of Python | all `.py` at `96e7a1a`: 69,036 | yes |
| `localhost:3000` | `docker-compose.yml:249` `"3000:3000"` | yes |
| `docker-compose` (Docker Desktop has it) | `start.py:25` `("docker", "docker-compose")`; Docker's own migration page says Desktop keeps a `docker-compose` alias [S4] | yes |
| bart-large-cnn on the worker | `stage4/summarization.py:79`, `large_doc_processor.py:76` | yes |
| **Rule 1: "When 5 URLs on one host fail every retry … left alone for 60 s"** | `stage2_worker.py:218-219` (5, 60); `utils/retry.py` `CircuitBreaker.record_success` sets `failure_count = 0` in the closed state; `_fetch_with_retries` calls it on every success (`:791`) | **5 and 60 hold; "5 URLs" without "in a row" does not** (must-fix 1) |
| Rule 2: append, never overwrite | `lakehouse_manager.py` writes with `mode="append"`, `schema_mode="merge"` (`:1378`, `:2080`, `:2298`, `:2379`) | yes |
| Rule 3: 6 days, then 5 | `repo_first` 2025-09-25; `prometheus_client` 2025-10-01; `"panels"` 2025-10-06 | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | `git log --format=%an` in the bare clones: Claude 45 of 146; jules 49 + Claude 22 = 71 of 499; agent co-author trailers on his own commits 1 and 30 | yes |

## Must fix, ranked

1. **Rule 1: "5 URLs in a row".** (`chart.toml:128` the `body`; `chart.toml:376` the `[[figures]]` row text; one
   anchor; one test. About 6 lines.)
   - **What's wrong.** `CircuitBreaker` in `Scraping_project/src/utils/retry.py` resets `failure_count` to 0 on any
     success while closed, and stage 2 calls `record_success()` on every page that comes back. So a host where 5 URLs
     fail but a good page lands between them never trips. That is the standard closed-state design: Microsoft's
     pattern page describes a counter of recent failures that resets [S2], and resilience4j counts a failure rate over
     the last N calls, not a running total [S3]. Mine is the plain consecutive kind. A stranger who reads "5 URLs"
     thinks a total. A Scrapy user who sees a flaky host never pause will think the page lied.
   - **New body:** "When 5 URLs in a row on one host fail every retry, that host is left alone for 60 s; the rest of
     the crawl goes on." (Three words more, about half a line at 390.)
   - **Anchor:** the figures row text becomes "5 URLs in a row on one host", and its `also` list gains
     `{path = "Scraping_project/src/utils/retry.py", literal = "self.failure_count = 0"}`, so the claim fails the
     day a success stops resetting the count.

2. **Split "Before you run 0.1.3:" in two: what it does to other people's servers stays open, what its files hold goes
   in a fold.** (`chart.toml` the L3, X1, X2, X3 entries at `:912`, `:924`, `:958`, `:987` gain `fold = true`;
   `scripts/render_readme.py` the install block renders folded entries after the open list as `<details>`;
   `LIST_MAX_ITEMS` back to 7, applied to each list; `checks/readme.py` README-CAUTIONS reads both lists. About 40
   lines and a test.)
   - **What's wrong, measured.** Eight items. At 390 they run from the middle of screen 2 to the middle of screen 3,
     about 825 CSS px, and at 360 nearly two and a half screens (`page-phone-360-2.png`, `-3.png`). That is the
     densest part of the page, on the format I said is the common one. And the cap was raised to 8 in round 12 "to fit
     X3", while the comment on that same constant cites a style guide's 2 to 7. Moving the rule to fit the content is
     the thing I keep saying not to do.
   - **The split is already in the list.** Round 11 kept these open because "strangers point this at other people's
     servers". That is true of four items: L1 (no pause, 256 at once, `--workers 1`), L4 (`Crawl-delay`, `robots.txt`
     only over https), L2 (crt.sh and Common Crawl, `--seeding-strategy none`) and L5 (start at the bare domain).
     Each is something you do or decide before you press enter. The other four, L3 (no JavaScript), X1 (`sitemap.xml`
     keeps `noindex` and canonicalized pages), X2 (blank `status_code`) and X3 (redirect base), are about what is in
     the file afterwards. Nobody hurts anyone by not reading them first. They matter, X1 especially, since Google
     tells you to list only the canonical URL of each page in a sitemap [S5], but they are second-level detail.
     Progressive disclosure is exactly this: what most people need first, the rest one clearly labelled step away,
     never deeper than two levels [S1]. A `<details>` is closed by default and its `<summary>` is the label [S8][S6].
   - **Build:**
     - Open, unchanged: "Before you run 0.1.3:" then L1, L4, L2, L5.
     - Then, before the code block, `<details><summary>What 0.1.3's files miss or get wrong</summary>` holding L3,
       X1, X2, X3 as the same bullets, in that order. Four words of label that say what is inside.
     - `LIST_MAX_ITEMS = 7` per list (the cited 2 to 7). The README-CAUTIONS check keeps requiring every route
       `text` entry to be printed, and now also that each folded one sits inside the `<details>`.
     - Test: no item with `fold = true` appears in the open list; every item in the open list has a lever (a flag or
       an action) or is L4.
   - **Size.** About 360 CSS px off the page at 390 (5,213 → about 4,850), 400 at 360, 150 at 1,280. The
     rustmapper block ends a screen sooner on a phone, and Scrapy, the second project, moves up the page.

3. **W1: say what saving as it goes does for you, in one phone line.** (`chart.toml:699` W1 `text`; the W1 anchors;
   `tokens.idea` regenerates DESIGN.md's opening; one test. About 10 lines.)
   - **What's wrong.** "logged to disk, then saved to redb, in batches" tells a stranger two internal words (a log,
     redb) and nothing to act on. Every keep since round 7 gave the same reason: it's why `export-sitemap` works after
     a kill (runcheck `export_after_kill`: 3 `<loc>`, while `kill_writes_file` shows `sitemap.jsonl` is not written).
     That reason is what a visitor needs, and it is the reason a write-ahead log exists at all: committed work is on
     disk before the store is updated, so a crash doesn't take it [S7]; redb's own pitch is "crash-safe by default"
     [S9]. Put the reason on the row.
   - **New text:** "saved to disk as it goes, so a kill keeps the crawl". The code block's
     "# sitemap.xml, even after a kill" then reads as the how-to for a promise the picture made. The two share no
     phrase, so STRINGS-TWICE stays clean.
   - **Hard limit: one line on the phone sheet.** W1 is one line at 390 today. A second line adds about 35 units to the
     1,121-unit phone sheet, and at an 851 px viewport (column 482) it would be drawn about 928 px tall, over
     HERO-COLUMN-PX's 900 px, which moves the mid breakpoint down to where the mid sheet's text drops under 11 px. If
     the text above wraps at 600 units, use "saved as it goes, so a kill keeps the crawl". Test: W1 is one line in
     every edition.
   - **Anchors:** keep the `drain_batch` anchors, and add the runcheck probe `export_after_kill` (ok) to W1's `runs`,
     so the row is retired the day an export after a kill stops working.

That's all. The image needs nothing else.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page this is | keep | desk, mid and phone each at their own size now |
| Role, two caps lines | crawl and data infrastructure; Python and Rust | keep | the route under it proves it |
| Empty left column (desk) | nothing, on purpose | keep | the eye goes to the route |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project and what you get | keep | true with the blank rows too |
| Start bar, `pip install rustmapper`, "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | the date makes every caution below it honest |
| Magenta track | one way through, top to bottom | keep | |
| Stop rings | one step the tool takes, each | keep | |
| S1 `rust_sitemap crawl` + seeds | the command, and where URLs come from by default | keep | |
| F1 fetch, per-host cap, scope | the loop's work and how far it reaches | keep | |
| W1 write path | (today) two internal words | **change** | must-fix 3: say that a kill keeps the crawl |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Gap in the track under the loop | the only way out of the loop is you | keep | |
| H1, red dotted box | the catch in 0.1.3, and how you know you're done | keep | goes when 0.1.4 ships |
| C1 Ctrl-C | the one key, and the second press not to make | keep | |
| End bar, `data/sitemap.jsonl`, fields | the file, in the struct's own names | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | my projects feed each other | keep | |
| Night editions | the same | keep | contrast holds |
| Mid editions (852 to 1,199) | the same, in one screen on a tablet | keep | round 12's fix works: 457 px at 900, the whole route above the fold at 1,180 |
| Phone editions (390, 308) | the same, in one screen | keep | |
| Alt text | install, loop, stop, file | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image link to the repo | where the project lives | keep | |
| `<picture>` sources | the right sheet for the width | keep | |
| Link line | where to go | keep | |
| "Ben Russell builds …" | what I build | keep | |
| Languages | what I write in | keep | |
| Stack | what I build on | keep | |
| Pick sentence | which tool for which job | keep | |
| rustmapper facts line | alive, tested, size, which commit | keep | |
| Wheel note | whether `pip` just works on your machine | keep | |
| "Before you run 0.1.3:" L1, L4, L2, L5 | what it does to someone else's server and what to set first | keep, open | each has its lever |
| L3, X1, X2, X3 | what the files miss or get wrong | **change** | must-fix 2: into one labelled fold |
| rustmapper code block + stop comment | how to run, when to stop, how to recover | keep | |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy bullets 1–3 | storage, what happens to a page, how it's watched and deployed | keep | |
| Scrapy run sentence | what `start.py` starts, needs and loads | keep | the `docker-compose` aside is true [S4] |
| Scrapy code block | how to start it and point it at your site | keep | |
| Grafana and `data/delta/` | where to look once it runs | keep | |
| Also: four tools | the reader of the file, the Go sibling, two more tools by what they do | keep | |
| 15 more (fold) | the rest | keep | |
| Working rule 1 | how I build: a failing host doesn't stop the crawl | **change** | must-fix 1: "in a row" |
| Working rules 2, 3 | raw first; measure from week one | keep | |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn, how it was run, who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Noted, not ranked

- Rule 1's evidence is two days old (`099dd6c`, 8 Oct 2026). The `CircuitBreaker` class has existed since 29 Sep 2025,
  but nothing called it until that commit, and the stage-1 middleware is not wired in. The page says "Oct 2026", so it
  is honest. If it reads thin to someone, the fix is a longer record, not a better sentence.
- The 360 code block still has two 32-column comment lines touching the padding (round 12's note). Unchanged; still
  legible.

## Owner notes, outside this repository

1. Carried and now the biggest lever on the page: ship 0.1.4 with P1 (exits when idle), `response.url()` as the base,
   `noindex` and canonicalized pages left out of `export-sitemap`, and `resume` after a kill. That retires H1, X1's
   second half, X3, and the whole question of how long the caution list is.
2. Carried: the Scrapy quick start's "Sample URLs loaded", the GitHub bio, the iOS and Android apps, the iPad check
   (now done in render; still open it once on a real one).

## Sources (new this round, none cited in earlier rounds)

1. [S1] Nielsen Norman Group, "Progressive Disclosure": show "everything that users frequently need up front", defer
   the rest behind a clearly labelled control, and "designs that go beyond 2 disclosure levels typically have low
   usability". The split in must-fix 2: https://www.nngroup.com/articles/progressive-disclosure/
2. [S2] Microsoft Azure Architecture Center, "Circuit Breaker pattern": in the closed state "the proxy maintains a count
   of the number of recent failures" and the counter resets. What the word "5" has to mean on a page (must-fix 1):
   https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
3. [S3] resilience4j, "CircuitBreaker": the count-based window "aggregates the outcome of the last N calls" and trips
   on a failure rate. Breakers count differently, so the page must say which kind mine is (must-fix 1):
   https://resilience4j.readme.io/docs/circuitbreaker
4. [S4] Docker Docs, "Migrate to Compose V2": Docker Desktop keeps a `docker-compose` alias that redirects to
   `docker compose`. Confirms the Scrapy run sentence: https://docs.docker.com/compose/migrate
5. [S5] Google Search Central, "Consolidate duplicate URLs": "Pick a canonical URL for each of your pages and submit
   them in a sitemap", and noindex is not the way to pick one. Why X1 stays on the page, in the fold:
   https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
6. [S6] W3C WAI-ARIA Authoring Practices, "Disclosure (Show/Hide) pattern": a widget whose content is collapsed or
   expanded. The fold is a standard control, not a trick: https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/
7. [S7] SQLite, "Write-Ahead Logging": a commit is appended to the WAL, and after a crash "the first new connection to
   open the database will start a recovery process". What W1's log is for (must-fix 3):
   https://www.sqlite.org/wal.html
8. [S8] MDN, `<details>`: closed by default, showing only the triangle and the `<summary>` label. The label in
   must-fix 2 is all a reader sees until they ask:
   https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details
9. [S9] redb README: "Crash-safe by default", "Fully ACID-compliant transactions". The property W1 should state in
   plain words: https://github.com/cberner/redb
10. [S10] Nielsen Norman Group, "Inverted Pyramid": the most important information first, because readers "stop
    reading at any point". Server-facing cautions before file details (must-fix 2):
    https://www.nngroup.com/articles/inverted-pyramid/
