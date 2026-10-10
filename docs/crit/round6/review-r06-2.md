# Review round 6, reviewer 2: the systems engineer who checks every claim against the clones

10 Oct 2026. Build looked at: `scratchpad/r6/build/round-05/`. That is the sheet on desk (870) and phone (390), day and
night, and the whole page on desk (screens 1 and 2) and phone (screens 1 to 5). Read: `README.md`, `SPEC.md`,
`DECISIONS.md`, `LOG.md` (rounds 1 to 5) and the fifteen earlier reviews. Nothing already fixed is repeated here.

How I read it: I have shipped crawlers and storage engines. I don't stop at a string in a file. I run the binary
against a server I control and read its request log, and I build main and do the same. Every result below comes from
the 0.1.3 binary the run check installed (`scratchpad/r6/rc2/work/v/bin/rust_sitemap`), from a release build of
Rust-sitemap `32c2651` that I made for this review (`scratchpad/r6/r06-2/rs`, 4 min 56 s cold), or from the clones at
the shas `stats.json` names. Scripts, site and logs are in `scratchpad/r6/r06-2/`.

Verdict: **not yet. 6 / 10.** The image is close. I found nothing false in it, and its form is right. The page under
it is a different matter. It has four statements a crawler or data engineer will catch, and three of them sit in the
rustmapper and Scrapy blocks directly under the image. That is a step back from round 5's "no figure is wrong", and
the earlier rounds missed them for one reason: the anchor engine checks that a string exists, not that the code path
runs.

## The first question: does it meet the owner's goal?

**The image: yes, in form and almost in content.** It answers "what is it showing?" in one look. It shows how you get
rustmapper, where its URLs come from, the loop it runs for every page, how it throttles itself to its own store,
the catch in this release and how to tell when you're done, the one key you press, the file you get, and which of his
other projects reads that file. Nothing has a size. No word names the theme. A list can't show the loop bracket or
put the catch at the step where it bites. It reads at 390 px in day and night. I checked every row against the
release and found no false row. One wording is loose (the header, must-fix 6).

**The page: no.** The owner's standing rule is "honest data only, nothing invented". Four statements fail it:

1. **"no pause between them unless the site's `robots.txt` sets a `Crawl-delay`" is false for 0.1.3, the release the
   sentence is about.** 0.1.3 never reads `Crawl-delay`. The only code that writes a host's robots facts is
   `frontier.rs:784-790`, and it always sends `crawl_delay_secs: None`. `robots.rs` has no parser for it (the word
   appears only in its doc comment). The L1 anchor `host_state.crawl_delay_secs = delay` proves a setter exists, not
   that anything calls it with a value. It also misses something worse. 0.1.3 asks for robots.txt at
   `format!("https://{}/robots.txt", domain)` (`robots.rs`), so on a plain-http site it never sees the file and obeys
   nothing in it. I measured this. A local http site had a robots.txt with `Disallow: /secret.html` and
   `Crawl-delay: 5`. 0.1.3 made 13 requests in 109 ms, fetched `/secret.html` 9 ms after `/`, and never once asked
   for `/robots.txt` (`r06-2/server.log`). Its own stderr says "missing robots.txt, fetching in background (allowing
   crawl)". This is the one paragraph a site owner reads, and r05-3 called it "the one politeness fact a site owner
   needs" [1, 2, 3].
2. **"On main, a crawl stops by itself once the site runs out of pages" holds only with a flag the sentence leaves
   out.** `tests/crawl_exits_when_idle.rs:67` passes `--ignore-robots`. Without that flag, main is the P1 bug in the
   spec: it defers every URL until robots.txt arrives (#47), and it still asks for it over https. I ran my build of
   `32c2651` on the same http site with no flags. It made **zero** requests and printed "Crawl complete: 0 URLs
   discovered, 0 crawled". It did stop by itself, after 90 s, with one unfetched line. Then I ran it with the test's
   flags (`--ignore-robots`, 1 s idle). It got 12 pages and exited in 2.3 s. So the sentence is true, and it points a
   reader at `cargo install` of a build that crawls nothing on any http site. That is the M1 gate checking a test's
   name and not its conditions.
3. **"Circuit breakers wrap the HTTP, Delta Lake and Redis services" is false at `96e7a1a`.** `HTTP_CIRCUIT_BREAKER`,
   `DELTA_CIRCUIT_BREAKER` and `REDIS_CIRCUIT_BREAKER` are defined in `src/utils/retry.py:249-275`, and nothing in the
   repository uses them or `get_circuit_breaker`. I grepped every `.py`. The stage-1 `CircuitBreakerMiddleware`
   (`retry_middleware.py:180`) is in no `DOWNLOADER_MIDDLEWARES`, neither `settings.py:125-157` nor
   `spider_config.py:92`. The breakers that actually run are per host, in stage 2: `_breaker(domain)`,
   `stage2_worker.py:923-934`. After `STAGE2_BREAKER_FAILURES` (5) URLs on one host fail every retry, that host is
   deferred for 60 s (Scrapy `README.md:385-400`). That is a better fact than the false one, and it is true [4].
4. **"its commands were run against a local 3-page site" leaves out that the command run is not the command printed.**
   The run check passed `--seeding-strategy none` (`runcheck.rustmapper.steps[crawl_ctrl_c].cmd`). The block a
   visitor pastes doesn't, so on 0.1.3 they get the default `all`. The image says so: "plus by default sitemaps,
   certificate logs, Common Crawl". That means crt.sh and the Common Crawl index are queried before the first fetch
   (`main.rs:551-552`, `crawler.initialize(&seeding_strategy).await`). I timed those two services today. crt.sh took
   28.3 s to answer a query for a small domain. `index.commoncrawl.org` returned 503 to one fetch and dropped the
   connection on another [5]. The data line was cut to two facts last round. It now overstates one of them.

Smaller: rust_llm_logger's "so logging costs the caller nothing" overstates the code (must-fix 5). The header "one
line for every page it reaches" undercounts what the file holds (must-fix 6).

None of this argues for a new concept. The image is the strongest thing on the page. Fix the four sentences and the
two gates that let them through, and the page meets the goal. The owner's own blockers (0.1.4, About text, README
line 25) are unchanged since round 5 and are not repeated here. PyPI still says 0.1.3, and the About text still
reads "goes until it reaches end points". Both were checked today.

## Figures and claims checked

| Printed | Source | Measured | Holds |
|---|---|---|---|
| `pip install rustmapper` · 0.1.3 · 8 NOV 2025 | `edition`; PyPI JSON today | latest 0.1.3; releases 0.1.0–0.1.3, all 8 Nov 2025 | yes |
| your URL, plus by default sitemaps, certificate logs, Common Crawl | sdist `cli.rs` default `all`; `main.rs:552` seeds before crawling | crt.sh 28.3 s; CC index 503 today | yes (and see claim 4) |
| fetches a page; queues links on your URL's domain, above or below it | sdist `url_utils.rs:81-91` | both dot-boundary branches | yes |
| fetches fewer pages at once when saves average over 500 ms | sdist `main.rs:90-140` | 1 permit per 250 ms while EWMA > 500 and > 32 permits idle; adds permits back under 100 ms | yes (mechanism; see notes) |
| logged to disk, then saved to redb, every 50 ms | sdist `writer_thread.rs:11` and its append → fsync → apply order | | yes |
| 0.1.3 never stops by itself; done when `Received work item` lines stop | `bfs_crawler.rs:433`; my run: 12 lines for 12 URLs | | yes (see notes on timing) |
| press Ctrl-C once to write `data/sitemap.jsonl` | runcheck `crawl_ctrl_c`; my run: 12 lines after one SIGINT | | yes |
| fields: `url, depth, status_code, title, …` | `SitemapNode` | a 404 URL has `status_code: null`, `crawled_at: null` | names yes; header, must-fix 6 |
| sorted by ideal-url-organizer: `scripts/import_rust_sitemapper.py`, with a test | `handoffs[0]` | I ran the 6 tests at `159968a`: pass. I fed my real 0.1.3 output, null-status line included, through `convert_file`: 12 written, 0 skipped, every row builds a `URLRecord`. CI `ci-cpu.yml:38` runs the test | yes, end to end |
| 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust · `32c2651` | `repos[Rust-sitemap]` | 161 Rust attributes + 15 Python = 176; Rust 16,390 | yes |
| 1,920 tests · CI passed 8 Oct · MIT · 69k lines of Python · `96e7a1a` | `repos[Scrapy]` | Python + Rust tests under `tree.py`'s rule; 69,036 | yes |
| Prebuilt for Apple silicon on CPython 3.13; 3 min cold build | `edition.wheels`; runcheck `install` | one `cp313 macosx_11_0_arm64` wheel; median 171.4 s | yes |
| up to 20 requests at a time to one host, 256 in all | sdist `state.rs:285` `max_inflight: 20`; `bfs_crawler.rs:283` `max_concurrent = max_workers` (256) caps in-flight tasks even when the governor grows the semaphore | | yes |
| … with no pause unless `robots.txt` sets a `Crawl-delay` | sdist `frontier.rs:787` `crawl_delay_secs: None`; `robots.rs:19` https only | 13 requests in 109 ms; Disallowed page fetched; `/robots.txt` never asked for | **no** (claim 1) |
| 0.1.3 writes one `sitemap.xml`; 50,000 URLs per file | X1 anchors; sitemaps.org | the protocol also caps a file at 50 MB [6] | yes |
| On main, a crawl stops by itself … `crawl_exits_when_idle.rs` passes in CI | test file line 67 `--ignore-robots` | my HEAD build, no flags: 0 requests, "0 crawled"; with the test's flags: 12 pages, 2.3 s | **misleading** (claim 2) |
| docker-compose `scraper` service; `-a allowed_domains` / `-a start_urls` | `docker-compose.yml:8`; `base_spider.py:45-52, 76, 134` (`_as_list`) | | yes |
| Grafana on `localhost:3000` | `docker-compose.yml:249` | | yes |
| Delta Lake raw, schema merge, partitions by domain, OPTIMIZE and VACUUM | `lakehouse_manager.py:364-368, 1001, 626-632` | partitioned tables: `stage1_discovery`, `stage2_page_analysis` | yes |
| Circuit breakers wrap the HTTP, Delta Lake and Redis services | `retry.py:249-275`; no caller anywhere | per-host breakers in stage 2 only | **no** (claim 3) |
| 25 ways (ideal-url-organizer) | `src/organizers/method_*.py` | 25 files | yes |
| rust_llm_logger: forwards while parsing, logging costs the caller nothing | `proxy.rs:148-190` | `parser.feed_chunk(&data).await` runs before `client_tx.send`; the record is written after `drop(client_tx)` | half (must-fix 5) |
| 45 of rustmapper's 146; 71 of Scrapy's 499 | `repos[].others`, `all_hands` | Claude 45 / 146; jules 49 + Claude 22 / 499 | yes |
| 15 more | `repo_count` 22 | 22 − 1 − 2 − 4 | yes (the brief's 21 is older) |
| its commands were run against a local 3-page site on 10 Oct 2026 (Linux x86_64) | `runcheck.rustmapper` | with `--seeding-strategy none`, not in the printed block | **overstated** (claim 4) |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose work this is | keep | the image travels without GitHub's header |
| Role line, two caps lines | crawl and data infrastructure, Python and Rust | keep | the drawing proves "crawl"; W1 and G1 prove "data infrastructure" |
| "rustmapper" + header sentence | which project, what it does | change | "every page it reaches" → "every URL it finds" (must-fix 6) |
| Start bar | begin here | keep | |
| `pip install rustmapper` | the way in | keep | the one command, and it works (run check, my run) |
| "0.1.3 · 8 NOV 2025" beside it | how old what you install is | keep | round 5 fixed its place; it reads as the release's date now |
| Magenta track | one way through, top to bottom | keep | |
| Stop rings, paper-filled over the track | a step the tool takes | keep | fixed last round; checked at 390 and 870 |
| S1 seeds | URLs come from more than links, and by default from outside services | keep | true for 0.1.3. It is also why the pasted command waits on crt.sh (claim 4). That belongs in text, not here |
| F1 fetch / queue scope | the loop, and how wide it reaches | keep | |
| G1 governor line | the crawl slows when its own store lags | keep | the one design idea of his that a storage engineer stops on. See notes on its limits |
| W1 log, then redb, every 50 ms | it is durable as it goes | keep | append → fsync → commit, both trees |
| Loop bracket and up arrow | which rows repeat per page | keep | the shape a list can't give |
| Gap under the loop | no exit but Ctrl-C | keep | closes when a release ends by itself |
| H1 in the dotted danger line | the catch in this release and when to act | keep | true for 0.1.3. Notes give the timing caveat, not a must-fix |
| C1 "press Ctrl-C once to write `data/sitemap.jsonl`" | the one key you press | keep | my run: one SIGINT, 12 lines |
| End bar | you arrive here | keep | |
| `data/sitemap.jsonl` + field names | what you get, in the struct's words | keep | |
| Hand-off line, arrow, "sorted by ideal-url-organizer …, with a test" | his projects feed each other, and the join holds | keep | verified end to end with real 0.1.3 output today, the strongest claim on the sheet |
| Night editions | the same | keep | |
| Phone editions | the same | keep | the cleanest edition |
| Link round the image | a tap lands on the project | keep | the About text it lands on is still the owner's to fix (r05-1) |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image | above | change | must-fix 6 only |
| Alt text | the route in 25 words | keep | |
| Link line | where to go | keep | |
| Builds / Languages / Stack | what he builds and with what | keep | |
| Pick sentence | which tool for which job | keep | names first now; `no_services` holds (Redis flag is a bool, false by default) |
| rustmapper sentence | what it is; API unreleased | keep | |
| rustmapper facts line | alive, tested, size, which snapshot | keep | |
| Install code block | the commands to paste | keep | runs as printed. The seeding wait is said in the data line (must-fix 4) |
| Wheel note | will pip just work | keep | |
| L1 load sentence | what it does to someone's server | **change** | false on Crawl-delay; silent on https-only robots (must-fix 1) |
| X1 one sitemap.xml / 50,000 | the sitemap limit | keep | could add "or 50 MB" [6], optional |
| M1 "On main, a crawl stops by itself" | what main fixed | **change** | true only under `--ignore-robots`; gate it (must-fix 2) |
| Scrapy sentence, facts line | the second tool, measured | keep | |
| Scrapy code block | how to start it | keep | `scraper` service and `-a` parsing checked |
| Grafana note | where to look | keep | |
| Scrapy bullet 1 (stages) | the shape of the pipeline | keep | |
| Scrapy bullet 2 (Delta Lake) | raw-first storage | keep | checked in `lakehouse_manager.py` |
| Scrapy bullet 3 (MinHash, stage 3/4, local BART) | dedupe and summaries without an API | keep | |
| Scrapy bullet 4 (Prometheus, breakers, Helm) | how it is run and watched | **change** | the breaker clause is false (must-fix 3) |
| Also: ideal-url-organizer, go_go_go, Ai_code_detector | the next projects | keep | 25 methods; git-history loader exists |
| Also: rust_llm_logger | the next project | **change** | "costs the caller nothing" (must-fix 5) |
| 15 more | the rest | keep | |
| Working rules 1–4 | how he works, each dated | keep | rule 1's cite is a commit date. Its circuit breaker is real in history even though the service breakers are unused now |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn; agent authorship | **change** | "commands were run" without "seeding off" (must-fix 4) |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **L1 says what 0.1.3 actually does with robots.txt** (`chart.toml [route.rustmapper]` L1, about line 524;
   `data/route.py` anchors; `scripts/runcheck.py`; about 30 lines and three tests).
   - Text while the release lacks a parser: "It sends up to {field:max_inflight} requests at a time to one host,
     {arg:workers} in all, with no pause between them. {release} ignores `Crawl-delay`, and asks for `robots.txt` only
     over https, so a plain-http site's rules are not read." On desk that is about two lines. The `instead` text,
     once a release parses it: today's sentence.
   - Release anchors: replace `text = "host_state.crawl_delay_secs = delay"` with `{path = "src/robots.rs", absent =
     "fn parse_crawl_delay"}` for the 0.1.3 wording, and `{path = "src/robots.rs", text = "format!(\"https://{}/robots.txt\""}`
     for the https clause. Main has `parse_crawl_delay_secs` (`robots.rs:53`), so a 0.1.4 cut from main flips the
     first clause by itself. The https clause stays until `fetch_robots_txt` uses `url_utils::robots_url`.
   - Run-check probe `robots_read` (gate false, like `ends_by_itself`): add to the route-site fixture a `robots.txt`
     with `Disallow: /secret.html` and a page that links to it. Pass if the server log has a `GET /robots.txt` and no
     `GET /secret.html`. Today it fails (my run). The https clause is printed only while the probe fails.
   - Engine rule, so this class of error can't recur: a `text` anchor on an assignment or setter doesn't count as
     evidence of behaviour. For any entry whose words say "unless", "when" or "only", require either a probe or an
     anchor on the producer. Add a test fixture where the setter exists and the producer passes `None`. The entry
     must come out unverified.
   - Why: it is false in the paragraph a site owner reads, and the truth (20 at a time, no delay, rules unread on
     http) is exactly what they need [1, 2, 3, 7].

2. **M1 is printed only when main crawls a site without the flag its test uses** (`chart.toml` M1, about line 552;
   about 3 lines and a test).
   - Add head anchors `{path = "tests/crawl_exits_when_idle.rs", absent = "--ignore-robots"}`, or require that S2 is
     verified at HEAD (P1's `tests/robots_4xx_allows_crawl.rs`). Either one means M1 is not printed today.
   - H1 still says "0.1.3 never stops by itself", which is true. The page loses "release pending", and it should,
     until main can crawl an http site.
   - Test: with the test file holding `--ignore-robots` and S2 unverified, M1 is absent from the README.
   - Why: my build of `32c2651` made zero requests to a plain-http site and reported "0 crawled". The sentence sends
     a reader to that build.

3. **Scrapy bullet 4 names the breakers that run** (`README.md` Scrapy bullets, from `chart.toml` or the template that
   writes them; 1 line plus a FIGURES row).
   - Text: "Prometheus metrics on Grafana dashboards. Each host has its own circuit breaker: after 5 URLs on it fail
     every retry, it is left alone for 60 s. Docker Compose and a Helm chart for Kubernetes."
   - FIGURES rows: "5 URLs" from `DEFAULT_STAGE2_BREAKER_FAILURES` and "60 s" from `DEFAULT_STAGE2_BREAKER_RECOVERY`
     in `stage2_worker.py`, read as constants, not literals.
   - Owner note, not this repository: delete or wire the three unused service breakers in `retry.py`, or register
     `CircuitBreakerMiddleware`.
   - Why: false as printed. The true version is also more useful, because it is what happens to a stranger's site
     [4].

4. **The data line says the crawl was run with seeding off** (`render_readme.py`, `survey` marker; a few words and a
   test).
   - Text: "… its commands were run, with seeding off, against a local 3-page site on 10 Oct 2026 (Linux x86_64). …".
     The words come from the run check's recorded `cmd`: printed when it contains `--seeding-strategy none`.
   - Test: if the run check's crawl command differs from the README block by any flag, the data line names that
     flag.
   - Why: the pasted block, run as printed, waits on crt.sh (28 s today) and the Common Crawl index (503 today)
     before its first fetch. "The commands were run" should mean the command shown, or say how it differed [5].

5. **rust_llm_logger says what the tee does** (`chart.toml` / the Also list; 1 line).
   - Text: "a non-buffering reverse proxy for LLM servers, in Rust. Each chunk is parsed for token counts and passed
     straight on, and the call is logged only after the client has its last byte."
   - Why: `proxy.rs:170-173` parses each chunk before sending it, so the cost is small but not nothing, and nothing
     runs "while" the chunk is forwarded. The true fact, logging after the response closes (`proxy.rs:191-192`), is
     the design point worth printing.

6. **The header counts URLs, not pages** (`chart.toml [route.rustmapper] header`; the alt text if it reuses it; 1
   line).
   - Text: "Crawls a site and writes one line for every URL it finds." Desk one line. Phone: "Crawls a site and writes
     one / line for every URL it finds."
   - Why: in my run, a link to a missing page got a line with `status_code: null` and `crawled_at: null`, and in 0.1.3
     non-200 responses are not recorded as a status (`bfs_crawler.rs:786`). A reader filtering for 200s needs to know
     the file holds every URL, not every page fetched.

## Notes (true, not ranked)

- **H1's "done when the lines stop".** A `Received work item` line is printed when a task starts, before its fetch
  (`bfs_crawler.rs:433`). A fetch can then run up to the 20 s `--timeout` (`cli.rs:48`), and in my run `/p10.html`
  was requested twice with only one line. On a large site the precise rule is "done 20 s after the lines stop". Not
  ranked: on the phone it would cost a third line, and the tool's own fix is on main.
- **G1's limits.** The governor can only shrink the cap while more than 32 permits are idle (`main.rs:114`). It grows
  the semaphore by one per 250 ms while saves are under 100 ms, with no total bound, because it compares
  `available_permits()` with 512 and not the total [8]. In-flight work stays capped at 256 (`bfs_crawler.rs:283`).
  "Fetches fewer pages at once when saves average over 500 ms" is the mechanism as designed, and I'd keep it. A
  storage reviewer who reads `main.rs` will see both edges.
- **After a kill**, the run check's `resume_after_kill` failed with "Database already open. Cannot acquire lock", and
  main's normal exit printed "Failed to export XML sitemap: Database creation error: Database already open" (my HEAD
  run). Neither is on the page, and neither should be until it's fixed. It's an issue for the owner's tracker.

## Sources (new this round)

1. IETF RFC 9309, *Robots Exclusion Protocol* (2022): §2.3 "scheme:[//authority]/robots.txt"; §2.3.1.3 a crawler "MAY
   access any resources" after a 4xx. It defines no crawl-delay directive.
   https://www.rfc-editor.org/rfc/rfc9309.html
2. Google Search Central, "How Google interprets the robots.txt specification": rules apply "only to the host,
   protocol, and port number where the robots.txt file is hosted"; `crawl-delay` is not supported.
   https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt
3. Bing Webmaster Blog, "To crawl or not to crawl, that is BingBot's question" (2012): "BingBot honors the
   Crawl-delay directive", read as one page per window of 1–30 s. It is honoured by some crawlers and not others,
   which is why a page that names it must be exact. https://blogs.bing.com/webmaster/2012/05/03/to-crawl-or-not-to-crawl-that-is-bingbots-question
4. M. Fowler, "CircuitBreaker" (bliki): "You wrap a protected function call in a circuit breaker object, which
   monitors for failures." A breaker defined and never wrapped around a call is not one.
   https://martinfowler.com/bliki/CircuitBreaker.html
5. Measured today through this session's proxy: `https://crt.sh/?q=%.toscrape.com&output=json&exclude=expired`, 200
   in 28.3 s; `https://index.commoncrawl.org/collinfo.json` and `https://index.commoncrawl.org/`, a dropped
   connection and a 503. These are the two services 0.1.3's default seeding waits on.
6. sitemaps.org, *Sitemaps XML format*: no more than 50,000 URLs "and must be no larger than 50MB (52,428,800
   bytes)" per file. https://www.sitemaps.org/protocol.html
7. H.-T. Lee, D. Leonard, X. Wang, D. Loguinov, "IRLbot: Scaling to 6 Billion Pages and Beyond", *ACM TWEB* 3(3),
   2009: webmasters "become easily annoyed when Web crawlers slow down their servers … This leads to … blocking of the
   crawler". Per-host limits are what a site owner checks first.
   https://s1.irl.cse.tamu.edu/people/hsin-tsang/papers/tweb2009.pdf
8. tokio docs, `Semaphore`: `available_permits` "Returns the current number of available permits"; `add_permits`
   panics only above `MAX_PERMITS` (`usize::MAX >> 3`). The governor's 512 is a cap on idle permits, not on the
   total. https://docs.rs/tokio/latest/tokio/sync/struct.Semaphore.html
9. Scrapy docs, *AutoThrottle*: designed to "be nicer to sites instead of using default download delay of zero". It
   is the comparison a reader makes: his Scrapy project obeys robots.txt and caps Crawl-delay at 60 s
   (`settings.py:121-124`), and his Rust crawler's release reads neither.
   https://docs.scrapy.org/en/latest/topics/autothrottle.html
10. C. Olston, M. Najork, *Web Crawling*, Foundations and Trends in IR 4(3), 2010 (politeness as a core crawler
    duty), via the UFMG course slides that summarise it:
    https://homepages.dcc.ufmg.br/~nivio/cursos/ri15/transp/crawling.pdf

From the clones, the binaries and my runs:
- 0.1.3 sdist: `src/robots.rs` (whole file), `src/frontier.rs:640-830`, `src/state.rs:270-290, 525-570`,
  `src/main.rs:84-160, 262, 551-552`, `src/bfs_crawler.rs:283, 300-330, 425-470, 740-790`, `src/cli.rs:40-70, 105-112`.
- Rust-sitemap `32c2651`: `src/robots.rs:15-60`, `src/frontier.rs:746-845, 911-961`,
  `tests/crawl_exits_when_idle.rs:59-70`; my release build in `scratchpad/r6/r06-2/rs`.
- Runs in `scratchpad/r6/r06-2/`: `site/` (11 pages, `robots.txt` with Disallow and Crawl-delay 5), `serve.py`
  (timestamped request log), `server.log` (0.1.3: 13 requests in 109 ms, `/secret.html` fetched, no `/robots.txt`),
  `server2.log` (HEAD, no flags: 0 requests; `run2/c.err` "0 URLs discovered, 0 crawled"), `server3.log` (HEAD with
  the test's flags: 13 requests, 12 lines, 2.3 s), `converted.jsonl` (the hand-off on real output).
- Scrapy `96e7a1a`: `src/utils/retry.py:240-275`, `src/stage1/middlewares/retry_middleware.py:180-235`,
  `src/settings.py:120-160`, `src/stage1/middlewares/spider_config.py:85-100`, `src/stage2/stage2_worker.py:23,
  331, 915-934`, `src/stage1/experimental/base_spider.py:45-137`, `src/lakehouse/lakehouse_manager.py:364-368,
  975-1005, 626-632`, `docker-compose.yml:1-37, 244-262`, `README.md:385-400`.
- ideal-url-organizer `159968a`: `tests/test_import_rust_sitemapper.py` (6 pass), `scripts/import_rust_sitemapper.py:
  56-145`, `.github/workflows/ci-cpu.yml:32-38`, `src/organizers/method_*.py` (25).
- rust_llm_logger `aadba12`: `src/proxy.rs:140-200`, `src/parsers/*.rs` `feed_chunk`.
- `assets/stats.json`: `edition`, `repos`, `routes`, `handoffs`, `runcheck`, `figures`, `repo_count`; `chart.toml`
  L1 (524-530), M1 (552-566).
