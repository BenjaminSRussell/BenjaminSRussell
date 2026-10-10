# Review round 11, reviewer 3: the data engineer

10 Oct 2026. My lens: a number gets onto the page only if it has a definition, the audit holds that definition, and
the code or a measurement agrees with it. I looked at every PNG in `scratchpad/r6/build/round-10/`: the desk sheet at
870 (day and night), the phone sheet at 390 and 308 (day and night), the desk page (two screens), and the phone page
at 390 and 360. I read `README.md`, `SPEC.md`, `LOG.md` through round 10, `docs/data/AUDIT.md` §2 and §7, and every
round 1 to 10 review plus `review-r11-1.md` and `review-r11-2.md`. Nothing here repeats a finding already fixed or
already raised this round. (Rule 4, the duplicated breaker and excel-and-vba are r11-1's; the command in the image
and the order of the install blocks are r11-2's.)

I didn't stop at reading. I checked figures against `assets/stats.json`, the 0.1.3 sdist
(`scratchpad/r6/sdist013/rustmapper-0.1.3`), the clones and their full histories (`clones/*.git`), and the CI logs
of the runs the facts lines cite (`gh run view --log`). I also ran two things myself:

- **The hand-off, end to end.** I fed two real 0.1.3 `sitemap.jsonl` files (`r6/runcheck/work/d`, `r6/rc9/work/d6`,
  8 rows) to ideal-url-organizer's `scripts/import_rust_sitemapper.py` at `159968a`, in a scratch copy with its light
  dependencies. **21 of 21 methods completed.** The "sorted 21 ways" mark is true as behaviour, not only as field
  names (`scratchpad/r11-3/run.log`).
- **Three new probes on the 0.1.3 binary** the run check installed: a page that answers 500, a page that answers 200
  with `application/json`, and a page held 8 s with `--timeout 3` (`scratchpad/r11-3/probe/`).

**Verdict: 8 / 10. It does not meet the goal yet, and I would not ship it as is.** The image is the right picture,
and almost every figure on it holds. Two of the figures that hold their definition still tell a reader something the
tool doesn't do, and the page prints two other numbers that disagree with the source a reader would check them
against.

## The first question: does it meet the owner's goal?

- **A deep purpose for each map and element.** Yes. Only a drawing shows the loop and where the trap sits in it.
  Nothing has a size, so "is it based on the size of the project or how many commits?" gets the answer "nothing
  has a size".
- **True and useful about his actual projects.** Mostly. One thing a visitor would act on is incomplete: what the
  output file says about pages that went wrong (must-fix 1). One printed wait, the 30 s, leaves out a delay that is
  in the code (must-fix 2).
- **Nothing chases a reason.** Yes, for the image. The page's two "ways" counts disagree for no reason the visitor
  can see (must-fix 4).
- **Nothing announces the theme.** Yes. There is no theme word anywhere.
- **Reads on a phone.** Yes. At 390 and 308 the image fits one screen, with text at 13.3 px or larger.

"The data doesn't look exactly accurate" is the owner's oldest complaint. What's left is in that category: the figures
match their definitions, but some definitions don't match what a reader checks them against.

## Figures checked

| Where | Printed | Source | Measured | Holds |
|---|---|---|---|---|
| image | 0.1.3 · 8 NOV 2025 | `edition.version`, `.date` | 0.1.3, first upload 2025-11-08 | yes |
| image | up to 20 pages at a time from each host | sdist `state.rs:285` `max_inflight: 20`; checked at `frontier.rs:655` before each dispatch | 20 | yes |
| image | by default also from sitemaps, certificate logs and Common Crawl | sdist `cli.rs` `default_value = "all"` | | yes (never run: the run check seeds `none`, and the data line says so) |
| image + code block | lines stop for 30 s | AUDIT §7 H1: 20 s `--timeout` + 4 s backoff + 1, rounded up | leaves out the permit wait in `bfs_crawler.rs:757` (up to 30 s) | **definition incomplete** (must-fix 2) |
| image | fields: url, depth, status_code, title | `SitemapNode`, both trees | in 0.1.3, `status_code` is 200 or null and nothing else | names yes; meaning see must-fix 1 |
| image | sorted 21 ways by ideal-url-organizer | `self.methods` 21 keys; `run.sh --all` | **21/21 ran on a real 0.1.3 file** | yes |
| facts | 176 tests | 161 Rust test attributes + 15 `def test_` in `python/tests` | CI run 37704909539: cargo reports 135 (lib) + 160 (bin) + 1 + 2 doctests per pass, pytest "15 passed" | yes as functions; see must-fix 3 |
| facts | 1,920 tests (CI selects all but 41) | 1,910 Python + 10 Rust (`kafka-delta-ingest/src/main.rs`); 41 = 16 outside + 25 deselected | CI run 37779293103, test (3.12): **"3075 passed, 9 skipped, 25 deselected, 1 xfailed"** | as defined, yes; **not the number CI shows** (must-fix 3) |
| facts | CI passed 7 / 8 Oct 2026, gates | `repos[].ci`, `ci.gates` | both runs success at `head_sha` | yes |
| facts | 16k lines of Rust, 69k of Python | `lines` 16,390 / 69,036 | | yes |
| wheel note | CPython 3.13, Apple silicon; 3 min cold, 4-core | `edition.wheels`; runcheck 168.2 / 171.4 / 174.3 s, rustc 1.97.0 | | yes (built with one rustc only) |
| L1 | up to 256 at a time across all hosts | `cli.rs` workers 256; JoinSet cap `bfs_crawler.rs:430` | page fetches only: robots.txt fetches run beside them, 6 per shard (`frontier.rs:20`) | yes for pages (note below) |
| X1 | 50,000 URLs per file | sitemaps.org | | yes |
| X2 | no `status_code` for 404, 429 or 503 | probe `non200_status` | **true, but also for a 500, a timeout and a non-HTML 200**, and `crawled_at` is null too | incomplete (must-fix 1) |
| Scrapy | 143,208; 134,807 on uconn.edu | `csv` rows, `urlsplit().hostname` | 143,208; 134,807 (recounted today) | yes |
| Scrapy | 5 URLs, 60 s, 50,000 characters | `stage2_worker.py:218-219`, `config.py:389` | | yes |
| Also | 25 ways … 21 … 4 more | glob of 25 `method_*.py` files | the 4 have no command: no entry point imports methods 22 to 25 | as a file count, yes; see must-fix 4 |
| rule 3 | 6 days, then 5 | `67446a4` 25 Sep → `d571e6e` 1 Oct → `e8cbe15` 6 Oct 2025 (`Scrapy.git`) | | yes |
| data line | 45 of 146; 71 of 499; 1 and 30 | `others`, `all_hands`, `coauthored.agent`; Scrapy's other 165 trailers are his own address | | yes |
| §7 register | rows F1, W1 | `audit_figures.route_rows` | list `{const:THROTTLE_THRESHOLD_MS}` and `{const:BATCH_TIMEOUT_MS}` as "printed"; neither is drawn | **register wrong** (must-fix 5) |

## What the probes showed

The 0.1.3 binary wrote these rows (seeding `none`, `--timeout 3`, one SIGINT):

| Page | What the server did | Requests | `status_code` | `crawled_at` |
|---|---|---|---|---|
| `/`, `/ok.html` | 200, `text/html` | 1 each | 200 | set |
| `/err` | 500 | 1 | null | null |
| `/feed` | 200, `application/json` | 1 | null | null |
| `/hang.html` | answered after 8 s (timeout 3 s) | 1 | null | null |
| `/busy.html`, `/gone.html` (round 9 probe) | 429, 404 | 1 each | null | null |

The code agrees. `CrawlAttemptFact`, the only event that sets `status_code`, `crawled_at`, `content_type` and
`title`, is sent only from the parser (`bfs_crawler.rs:389-399`). The parser is reached only from
`Ok(response) if … == 200` with an HTML content type (`:786-797`). A non-HTML 200 returns `Ok(Vec::new())` early
(`:798-804`). Every other answer takes `Ok(_) =>` (`:810`). A timeout, refused connection, DNS or TLS error takes
`Err(e)` (`:817`), which `handle_crawl_error` counts as transient: no failure recorded, no requeue (`:640-670`). No
code path retries a URL. In this file, "null" means "anything but an HTML 200". A row for a page that answered 500
looks exactly like a row for a page that was never asked for.

That is a data problem a visitor meets on the first big crawl. ideal-url-organizer's method 15 shows it: in my run it
reported "Crawled: 6 URLs (75.0%) / Not crawled: 2 URLs". Those two were the 429 and the 404. Both were fetched.

## Must fix, ranked

1. **X2 says what a blank row means** (`chart.toml` X2 `text`; `tests/fixtures/status-site/` gets three pages; the
   `non200_status` probe in `scripts/runcheck.py`; AUDIT §7 X2 row; about 25 lines and one test).
   - Text (25 words, the README-CAUTIONS cap): "Only HTML pages that answer 200 get a `status_code`. An error, a
     timeout or a non-HTML 200 is left blank, `crawled_at` too, and never retried."
   - Fixture: add `/err` (500), `/feed` (200, `application/json`) and `/hang.html` (held 8 s). The probe crawls with
     `--timeout 3`. It passes when each of the five non-200-HTML rows has `status_code` and `crawled_at` null and
     was requested once.
   - Anchors (release): keep the round 9 anchors, and add `fn = "handle_crawl_error"`
     `text = "false // Don't block host for transient errors"` and `fn = "process_url_streaming"`
     `text = "is_html_content_type(ct)"`. Keep `instead = ""` on `fails = ["non200_status"]`, so the item retires
     when 0.1.4 records every status.
   - Why: the end bar promises a file with a `status_code` field. A reader who sees a null treats it as "not
     fetched", and his own organizer does the same. Codd split nulls into "missing but applicable" and "missing but
     inapplicable" for this reason [S9]. A list item is the only place the page can say which null this is. The
     guide that crawlers follow says the opposite of what 0.1.3 does: Scrapy retries 429 and 503, and timeouts and
     lost connections, twice by default [S3]. Google slows down on 429 and 5xx instead of dropping the URL [S5].
   - Owner note (Rust-sitemap, already carried as "record every response's status"): send `CrawlAttemptFact` from
     the `Ok(_)` and `Err` branches too, with the status or an error kind. Then method 15 counts correctly with no
     edit in ideal-url-organizer.

2. **H1's quiet time includes the permit wait** (`scripts/data/route.py` `quiet_secs`; `chart.toml` H1 value
   anchors; the `quiet_slow_page` probe waits the new value; AUDIT §7 H1; about 15 lines and one test).
   - In 0.1.3, a work item is logged ("Received work item", `bfs_crawler.rs:433`) before its task waits for a network
     permit, for up to 30 s (`tokio::time::timeout(Duration::from_secs(30), network_permits.acquire_owned())`, `:757`).
     Then it fetches, for up to 20 s. Only after parsing are its links queued, and only then does a new line appear.
     The permits are the governor's semaphore (`main.rs:262, :375`). The governor holds idle permits back while saves
     lag (`main.rs:114-115`, the same mechanism review r08-2 traced). So the wait is real, and it happens when the
     last level of a big site is in flight. tokio's semaphore is first in, first out [S2], so a late item waits
     behind every earlier one. reqwest's timeout runs "until the response body has finished" [S1]. A wait that
     reaches 30 s drops the URL ("an error is returned and the future is canceled" [S8]), which must-fix 1's
     "timeout" covers.
   - The bound becomes 30 (permit) + 20 (`--timeout`) + 4 (backoff) + 1, so 55, rounded up to **60 s**. Add a value
     anchor `{path = "src/bfs_crawler.rs", fn = "process_url_streaming", text = "timeout(Duration::from_secs(30),
     network_permits.acquire_owned())"}`. Have `quiet_secs` read the 30 from it, the way it reads `arg:timeout`, and
     fail the build if the anchor goes. The image prints "…lines stop for 60 s", and the code block prints
     "# for 60 s, then Ctrl-C once". Both are still one desk line and two phone lines.
   - The probe `quiet_slow_page` must wait 60 s after the last line before its SIGINT (`run_missing` already makes the
     number fall back to "…, even after the last page" when the probe waited less).
   - Why: the 30 s is the one figure on the image a reader acts on blind. If it's too short, they stop the crawl
     while the last page's links are still on their way, and they never learn that they did. Waiting 30 s longer
     costs them half a minute, once.

3. **Name the unit: "test functions"** (`scripts/render_readme.py` facts; `tests/test_pipeline.py` facts strings;
   AUDIT §7 "N tests" row; about 6 lines).
   - Print "176 test functions" and "1,920 test functions (CI selects all but 41)".
   - Why: the facts line puts the count beside "CI passed 8 Oct 2026", and the link goes to a run whose log says
     "3075 passed, 9 skipped, 25 deselected, 1 xfailed". pytest runs each parametrized case as its own test [S4]. Two
     honest numbers 60 % apart, with nothing on the page to say why, are what "the data doesn't look exactly
     accurate" means. Printing the CI totals instead doesn't work across repositories. Cargo runs the lib and the bin
     as separate test executables [S6], so Rust-sitemap's log reports 135 + 160 for 161 functions. The function count
     is the consistent unit. It only needs its name. Add one AUDIT sentence: "CI logs count parametrized cases (Scrapy
     3,075 on 8 Oct 2026) and the lib and bin targets separately (Rust-sitemap 135 + 160); the page counts functions."

4. **One count of the organizer's sorts on the page: 21** (README `Also`, hand-typed, the ideal-url-organizer line;
   `chart.toml [[figures]]` rows `25 ways` and `4 more` removed and `21 from` reworded; AUDIT §7 regenerated; about
   8 lines).
   - Line: "**ideal-url-organizer** — 21 ways to sort a pile of URLs from their crawl records (domain, crawl depth,
     subdomain, …)."
   - Why: the image says "sorted 21 ways" and the text two screens down says "25 ways". A visitor can't tell that
     both are true, and NN/g's consistency heuristic is the rule here: people "should not have to wonder whether
     different words … mean the same thing" [S10]. The 4 extra are files that no command runs. `main.py`'s
     `self.methods` lists 21, `--method` accepts only those, and no entry point imports methods 22 to 25 (grep over
     the tree finds only `tests/test_stub_embedder.py`). A sort you can't run is not a way to sort. When a command
     runs them, the row comes back by itself with the count of reachable methods.

5. **The §7 register lists what is drawn, not every wording** (`scripts/audit_figures.py` `route_rows`, about 15
   lines; one test).
   - Today `route_rows` takes the placeholders of the entry *and* all its alternatives (`cands = [e] + instead`). So
     the F1 row says it prints `{const:THROTTLE_THRESHOLD_MS}` (500 ms, not drawn), and the W1 row says it prints
     `{const:BATCH_TIMEOUT_MS}` (50 ms, not drawn). What is drawn is "20" in F1 and no figure in W1.
   - Build the "printed" column from the wording `routes` resolved and drew. Put the other wordings' placeholders
     under "drawn instead when …" in the definition. A drawn entry with no placeholder gets no row.
   - Test: with the round 10 `stats.json`, the F1 row prints `{field:max_inflight}` only, and W1 has no row.
   - Why: §7 is the register a reviewer opens to check a figure. A register that lists a figure that isn't on the
     page sends them looking for something that isn't there, and it hides which definition belongs to the "20".

## Not ranked, noted

- L1's "up to 256 at a time" counts page fetches. robots.txt fetches run beside them under their own limit, 6 per
  shard with one shard per CPU (`frontier.rs:20`, `main.rs` `num_cpus::get()`). On one site that adds at most one
  request per host, so the sentence is fair for the reader it's written for. If it is ever reworded, "up to 256
  pages at a time" is exact.
- Rule 3, "a dashboard was up 5 days after that": the anchor is the commit that added `"panels"` (`e8cbe15`, "gafka
  dashboard"). "Was committed" is what the anchor measures. It's a small word, and r11-1 owns the rules block.
- The wheel note's "needs a Rust toolchain" was measured with rustc 1.97.0 only. Cargo.toml says edition 2021 and
  no `rust-version`. If a reader with an older toolchain reports a failure, record the oldest rustc that builds the
  sdist and print it.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page this is | keep | |
| Role, two caps lines | crawl and data infrastructure, in Python and Rust | keep | the drawing proves it |
| Empty left column (desk) | nothing | keep | no figure there needs a definition |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project, what you get | keep | true: every discovered URL gets a row, fetched or not |
| Start bar, `pip install rustmapper`, "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | both from PyPI |
| Magenta track | one path, read top to bottom | keep | |
| Stop rings | one step each | keep | no size, no data |
| S1 seeds | URLs come from more than links, by default | keep | `default_value = "all"` |
| F1 "up to 20 pages at a time from each host; queues their links to …" | how hard it hits one host, and how far it reaches | keep | `max_inflight` checked per dispatch |
| W1 "logged to disk, then saved to redb, in batches" | it saves as it goes | keep | no figure, correctly |
| Loop bracket and arrow | which steps repeat | keep | |
| H1 dotted box | the catch in 0.1.3 and when you're done | **change** | 30 s → 60 s (must-fix 2) |
| C1 Ctrl-C | how to stop without losing the file | keep | probes `crawl_ctrl_c`, `second_ctrl_c` |
| End bar, `data/sitemap.jsonl`, fields | the file and its field names | keep | the names are the struct's; their meaning is the list's job (must-fix 1) |
| Hand-off arrow, "sorted 21 ways by ideal-url-organizer" | his projects feed each other | keep | I ran it: 21/21 |
| Night editions | the same | keep | |
| Phone editions (390, 308) | the same in one screen | keep | |
| Alt text | install, loop, stop, file | keep | 25 words, true |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Link line | where to go | keep | |
| "Ben Russell builds …" | what he builds | keep | |
| Languages | what he writes in | keep | `main_language` by repository count, then lines; defined in §7 |
| Stack | what he builds on | keep | no figures |
| Pick sentence | which tool for which job | keep | |
| rustmapper facts line | alive, tested, size | **change** | "test functions" (must-fix 3) |
| rustmapper code block | how to run and stop | **change** | 60 s (must-fix 2) |
| Wheel note | whether pip just works | keep | measured three times, cold |
| "Before you run 0.1.3:" items L1–L5, X1 | what it does to a server and what it can't see | keep | all anchored; L1 note above |
| X2 | what a blank row means | **change** | must-fix 1 |
| Scrapy sentence | what it is | keep | |
| Scrapy facts line | alive, tested, size | **change** | "test functions" (must-fix 3) |
| Scrapy bullets | the design | keep (bullet 3 per r11-1) | figures hold |
| Scrapy run sentence and code block | what `start.py` starts and loads | keep | 143,208 / 134,807 recounted |
| Grafana note | where to look | keep | `"3000:3000"` |
| Also: ideal-url-organizer | another of his tools | **change** | 21, not 25 (must-fix 4) |
| Also: go_go_go, rust_llm_logger, Ai_code_detector | his other work | keep | `[[figures]]` hold |
| 15 more (details) | the rest | keep (excel-and-vba per r11-1) | count holds |
| Working rules 1–3 | how he works, dated | keep | dates recounted in `Scrapy.git` |
| Working rule 4 | | cut (r11-1) | |
| Found a mistake? | the page can be corrected | keep | |
| Data line | how the drawing was checked; who wrote the code | keep | every count holds |
| Licence line | terms | keep | |

## Sources (new this round)

1. [S1] reqwest docs, `ClientBuilder::timeout`: "The timeout is applied from when the request starts connecting
   until the response body has finished." This is why the 20 s term covers the body.
   https://docs.rs/reqwest/latest/reqwest/struct.ClientBuilder.html
2. [S2] tokio docs, `Semaphore`: "This Semaphore is fair, which means that permits are given out in the order they
   were requested." So a late work item waits behind every earlier one (must-fix 2).
   https://docs.rs/tokio/latest/tokio/sync/struct.Semaphore.html
3. [S3] Scrapy docs, `RetryMiddleware`: `RETRY_HTTP_CODES` defaults to `[500, 502, 503, 504, 522, 524, 408, 429]`,
   `RETRY_TIMES` to 2, and timeouts and lost connections are retried. This is the behaviour 0.1.3 lacks (must-fix 1).
   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
4. [S4] pytest docs, "How to parametrize": the decorated function "will run three times", once per parameter set.
   That is why CI's 3,075 is bigger than 1,920 functions (must-fix 3).
   https://docs.pytest.org/en/stable/how-to/parametrize.html
5. [S5] Google Search Central, "HTTP status codes, network and DNS errors": "5xx and 429 server errors prompt Google's
   crawlers to temporarily slow down", and the rate goes back up after 2xx. A 429 is a signal to wait, not a
   page to forget. https://developers.google.com/search/docs/crawling-indexing/http-network-errors
6. [S6] The Cargo Book, `cargo test`: it builds "lib as a unit test" and "bins as unit tests", and "each target
   compiles to a special executable … and then is run serially". That is why Rust-sitemap's log shows 135 + 160
   (must-fix 3). https://doc.rust-lang.org/cargo/commands/cargo-test.html
7. [S7] RFC 6585 §4, 429 Too Many Requests: the response "MAY include a Retry-After header indicating how long to
   wait before making a new request". The probe's `Retry-After: 2` was ignored.
   https://www.rfc-editor.org/rfc/rfc6585.html
8. [S8] tokio docs, `time::timeout`: if the duration elapses first, "an error is returned and the future is
   canceled". The URL is dropped, not requeued (must-fixes 1 and 2).
   https://docs.rs/tokio/latest/tokio/time/fn.timeout.html
9. [S9] "Null (SQL)", Wikipedia: Codd proposed two null markers, "Missing But Applicable" and "Missing But
   Inapplicable", because one null can't say why data is missing. In 0.1.3 one null covers "failed", "not HTML" and
   "never asked" (must-fix 1). https://en.wikipedia.org/wiki/Null_(SQL)
10. [S10] Nielsen Norman Group, "10 Usability Heuristics", no. 4: "Users should not have to wonder whether
    different words, situations, or actions mean the same thing." That is the 21 against the 25 (must-fix 4).
    https://www.nngroup.com/articles/ten-usability-heuristics/

Measured, not cited: GitHub Actions logs for Scrapy run 37779293103 (job `test (3.12)`, pytest summary line) and
Rust-sitemap run 37704909539 (Test and Python wrapper jobs), read with `gh run view --log`. My probes are in
`scratchpad/r11-3/probe/` (`server.py`, `server2.py`, `d/`, `d2/`) and the hand-off run is in `scratchpad/r11-3/run.log`.
Code: sdist 0.1.3 `src/bfs_crawler.rs:389-399, :430-433, :640-670, :757-777, :786-817`, `src/main.rs:84-151, :262,
:375`, `src/frontier.rs:20, :595-660`, `src/state.rs:285`; ideal-url-organizer `159968a` `src/main.py:56-78`,
`scripts/import_rust_sitemapper.py`, `src/organizers/registry.py`; Scrapy `96e7a1a` `Scraping_project/tests`
(1,910 functions by AST), `kafka-delta-ingest/src/main.rs` (10), `data/raw/uconn_urls.csv`; `Scrapy.git` `67446a4`,
`d571e6e`, `e8cbe15`; this repository `scripts/audit_figures.py:115-160`, `scripts/data/tree.py:1-30`.
