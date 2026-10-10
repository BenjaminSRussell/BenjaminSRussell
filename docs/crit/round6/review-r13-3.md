# Review round 13, reviewer 3: the deck officer and yacht navigator

10 Oct 2026. I use real charts and pilot books. For each mark and each paragraph I ask the question I ask of a chart
or a pilot book: what does the person using it do differently because it is there?

**What I looked at.** Every PNG in `scratchpad/r6/build/round-12/`:
- the desk sheet at 870, day and night;
- the mid sheet at 746, day and night;
- the phone sheet at 390 and 308, day and night;
- the page at 1,280 (two screens), at 1,180 and 900 (first screen), at 390 (seven screens) and at 360 (seven).

**What I read.** `README.md`, `SPEC.md`, `LOG.md` through round 12, both earlier navigator reviews (`review-r04-3.md`,
`review-r09-2.md`), the round 10 to 12 reviews, and this round's `review-r13-1.md` and `review-r13-2.md`. I don't
repeat anything already fixed. Where I agree with this round's other reviewers, I say so in one line.

**How I checked.** Every figure was checked against `assets/stats.json`, the 0.1.3 sdist
(`scratchpad/r6/sdist013/rustmapper-0.1.3`) and the clones (Scrapy `96e7a1a`, ideal-url-organizer `159968a`). I also
ran one new probe of my own: the run check's installed 0.1.3 binary against a local **https** site with no
robots.txt (`scratchpad/r13-3/probe/`).

**Verdict: not yet. 8 / 10.** I would ship the image as it is. The page has two faults, and both are about Scrapy, the
second project:

1. If a stranger runs the page's Scrapy command against their own site, every request introduces itself as
   `UConn-Discovery-Crawler/1.0`. The command sends a false identity, and the page doesn't say so.
2. The page tells a chooser, in eight items, everything rustmapper 0.1.3 doesn't do for the site it crawls. It never
   says that Scrapy does those things: it obeys `robots.txt` and its `Crawl-delay`, and it waits out a `Retry-After`.
   For someone pointing a crawler at a server they don't own, that is the deciding difference between his two tools.
   It is also the best engineering fact on the page, and it is missing.

## The first question: does it meet the owner's goal?

- **Every map has a deep purpose.** The image does. It is the one route a URL takes through rustmapper:
  - the way in;
  - the steps the tool takes, in the order it takes them;
  - which of them repeat;
  - the one danger, with the number that tells you you're past it;
  - the one action, and the mistake to avoid while you do it;
  - the berth;
  - where the cargo goes next.

  A list can't show the loop and the missing exit, and a drawing can. Nothing in it has a size, so "is it the size of
  the project or the commits?" has no question left to answer.
- **It teaches something true and useful about his actual projects.** The image, yes: every row holds (table below).
  The page, almost. It is true, but it is lopsided. It is a full pilot-book entry for one harbour, dangers and all.
  The second harbour gets its facilities and its approach, but no word on how it treats the people whose servers it
  visits. The one thing the second harbour gets wrong, its false identity, isn't printed either.
- **Nothing chases a reason.** In the image, yes. One reason in this round's other reviews runs ahead of the code:
  r13-1's proposed W1 wording "a kill keeps the crawl". After a kill, 0.1.3 writes no `sitemap.jsonl` and `resume`
  fails. Only `export-sitemap` gets anything back. See must-fix 3.
- **Nothing announces the theme.** True. You only see the chart habits if you know them: the magenta track, the
  dotted danger line with its clearing number, the edition date at the entrance and the continuation arrow. No word
  names them.
- **Reads on a phone.** Yes. At 390 and 308 the image fits on one screen. The 308 render's smallest text is about
  13 px.

## What a navigator does with each mark

| Mark | What it is for at sea | What the stranger does because of it here | Works? |
|---|---|---|---|
| Start bar at `pip install rustmapper` | the departure point of a passage plan | starts here, nowhere else | yes |
| "0.1.3 · 8 NOV 2025" at the entrance | the edition date, read before trusting a chart | knows every row below is about an 11-month-old release | yes. The rows are pinned to the edition ("0.1.3 never exits"), so a screenshot stays true without a correction date. That is why the image needs no "checked on" date, and the data line carries one for the page. |
| Magenta track | the line you are meant to follow | reads down, one way | yes |
| Rings | positions where something happens | sees each step the tool takes | yes |
| Loop bracket, arrow up | (no chart equivalent; it is route-map grammar) | sees which rows repeat for every page | yes, the best mark in the image |
| Break under the loop | no charted way out | understands that the exit is theirs to make | yes |
| Dotted box round H1 | a danger line round a hazard, with a clearing number | waits for 60 s of no `Received work item` lines before acting | yes. The 60 holds in the probe (`quiet_slow_page`: a 15 s gap is not the end; 60 s after the last line, one SIGINT writes 3 of 3) |
| C1 ring, outside the loop | the commitment point | presses once, then waits for `Saved to` | yes |
| End bar, `data/sitemap.jsonl` | the berth | knows the file and its real field names | yes |
| Thin arrow, "sorted 21 ways by ideal-url-organizer" | "continued on chart …" | knows the cargo goes somewhere else of his | yes. See note 2 on the next leg |

## Figures checked

| Printed | Source | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `edition.date`; all four uploads on 2025-11-08 | yes |
| `rust_sitemap crawl` | `edition.scripts` `["rust_sitemap"]`; probe `crawl_help` | yes |
| by default also sitemaps, certificate logs, Common Crawl | sdist `cli.rs` `default_value = "all"`; the seeders run before the first work item (`bfs_crawler.rs:215-262`), so seeding's quiet comes before the clearing rule applies | yes |
| up to 20 pages at a time from each host | `routes` F1 fallback, `state.rs` `max_inflight` | yes |
| logged to disk, then saved to redb, in batches | W1 fallback, `drain_batch` anchors | yes |
| never exits by itself; 60 s | `ends_by_itself` false; `quiet` 60; probes `quiet_after_last_page`, `quiet_slow_page` ok | yes |
| Ctrl-C once; a second press before `Saved to` | `second_ctrl_c` ok (exit 1, no file) | yes |
| fields `url, depth, status_code, title` | `SitemapNode`, both trees | yes |
| sorted 21 ways | `figures` "21 ways", `self.methods` 21; importer `scripts/import_rust_sitemapper.py` ("methods-1-21 pathway") | yes |
| 176 test functions · CI passed 7 Oct 2026 · 16k lines · `32c2651` | `repos[Rust-sitemap]`: 176; success 2026-10-07; Rust 16,390; head `32c2651` | yes |
| 1,920 test functions (all but 41) · CI 8 Oct 2026 · MIT · 69k · `96e7a1a` | `repos[Scrapy]`: 1,920; `ci_selection.not_selected` 41; success 2026-10-08; MIT; Python 69,036 | yes |
| 3 min, cold cache, 4-core Linux | `runcheck` install median 171.4 s, 4 CPUs | yes |
| 256 at a time; `--workers 1` | `cli.rs` "256"; probe `workers_cap` | yes |
| 143,208 bundled URLs, 134,807 on uconn.edu | recounted from `data/raw/uconn_urls.csv`: 143,208 rows, 134,807 with host `uconn.edu` or a subdomain | yes |
| 5 URLs, 60 s (rule 1) | `figures` rows `DEFAULT_STAGE2_BREAKER_FAILURES = 5`, `_RECOVERY = 60` | yes; "in a row" is r13-1 #1 |
| 50,000 characters; first five sentences; `localhost:3000`; four stages | `figures` rows, all `holds` | yes |
| 6 days, then 5 days; Oct 2026, Oct 2025, Oct 2025 | `rules[]` | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | `others` Claude 45, `all_hands` 146; jules 49 + Claude 22, `all_hands` 499; `coauthored.agent` 1 and 30 | yes |
| 15 more | `repo_count` 22 − profile − 2 − 4 | yes |
| 10 Oct 2026, Linux x86_64, seeding off, 3-page site | `runcheck` | yes |

## The two Scrapy facts, measured

**The identity.** In `Scraping_project/src/settings.py:115` the user agent is
`USER_AGENT = _scrapy_config.get("user_agent", "UConn-Discovery-Crawler/1.0")`. `_scrapy_config` comes from the
`scrapy:` section of `config.yml` (`settings.py:24-74`), and `config.yml` has no `scrapy:` section. Its top-level keys
are redis, postgres, stage1 to stage4, kafka, delta_lake, message_queues, logging, monitoring and export. Nothing
overrides the header per request on the scout path. `PoliteRobotsTxtMiddleware` also reads it to pick the robots.txt
group (`robots_middleware.py:77`).

So the page's last Scrapy command, `docker-compose run --rm scraper scrapy crawl scout -a allowed_domains=<domain> -a
start_urls=<url>`, crawls the reader's site as "UConn-Discovery-Crawler/1.0". Three things follow:
- the site's operator sees a university that never visited;
- robots.txt rules written for that name are applied to the reader;
- if the reader points it at a site they don't own, any complaint goes to UConn.

RFC 9110 says the field exists to "identify the user agent software", and that implementations shouldn't use
"the product tokens of other implementations" [S1]. Scrapy's own project template says "Crawl responsibly by
identifying yourself (and your website) on the user-agent" [S2]. Cloudflare's verified-bot policy requires a bot that
"declares who it is deterministically" and "represents itself honestly" [S3]. Site owners verify crawlers because
others claim to be them: Google offers verification for crawlers "claiming to be from Google" [S4], and Common Crawl
warns that some crawlers falsely identify as CCBot [S5]. In my trade this is a vessel transmitting another ship's
identity. The watch is expected to check its own static data, because "inaccurate and/or missing AIS information is a
safety concern" [S6][S7]. The fix is cheap. Scrapy's `-s` settings "have the highest precedence" [R1], and `USER_AGENT` is
not in the scout's `custom_settings`, so `-s USER_AGENT=…` wins.

**The politeness.** `get_spider_settings("scout")` (`src/stage1/middlewares/spider_config.py`) sets the following:
- `ROBOTSTXT_OBEY` is on by default;
- Scrapy's robots middleware is replaced by `PoliteRobotsTxtMiddleware`, which honours `Crawl-delay` up to 60 s;
- `RetryAfterMiddleware` waits out a `Retry-After` on a 429 or 503, up to 120 s, and backs off exponentially when
  there is none;
- AutoThrottle is on.

The tests behind it are in CI's selection, with no `slow`, `kafka` or `performance` marker:
- `tests/unit/stage1/test_robots_policy.py`: 6 tests, including
  `test_disallowed_path_is_never_requested_and_crawl_delay_is_capped`;
- `test_retry_after.py`: 16 tests;
- `test_robots_fixtures_526.py`: 6 tests.

rustmapper 0.1.3 does none of this. The page says so in L1, L4 and X2, and the run check measured it. A `Retry-After`
tells the client "how long to wait before making a new request" [S8], and 0.1.3 ignores it. Sailing directions exist
to set "navigational hazards, buoyage, pilotage, regulations" next to "port facilities" [S9], so a master can choose a
port. Here the page gives rustmapper's hazards in full and leaves out Scrapy's pilot service. Round 6 noted the
contrast in its sources (`review-r06-2.md` source 9), and round 8 noted it in a paragraph about go_go_go. Neither put
it on the page.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page | keep | read first, as a chart's title is |
| Role, two caps lines | crawl and data infrastructure; Python and Rust | keep | the route under it proves it |
| Empty left column (desk) | nothing, on purpose | keep | open water keeps the eye on the track |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project and what it gives you | keep | true with blank rows too |
| Start bar | where you begin | keep | |
| `pip install rustmapper` | the way in | keep | |
| "0.1.3 · 8 NOV 2025" | how old the release is | keep | it dates every caution under it |
| Magenta track | one way through | keep | |
| S1 ring, `rust_sitemap crawl`, seeds | the command, and who else hears about your domain | keep | seeding ends before the first work item, so the clearing rule below is not fooled by it |
| F1 ring, 20 per host, scope | the load a site feels, and how far it reaches | keep | |
| W1 ring, "logged to disk, then saved to redb, in batches" | it saves as it goes | keep, or change only with wording that holds | see must-fix 3 on r13-1's proposal |
| Loop bracket, arrow up | which rows repeat | keep | the one fact only a drawing gives |
| Break under the loop | no way out but yours | keep | |
| H1 red dotted box | the 0.1.3 catch and its clearing number | keep | a danger mark with a number you can check, as a clearing line should be |
| C1 ring outside the loop | the one action and its mistake | keep | |
| End bar, `data/sitemap.jsonl`, fields | the berth, in the struct's names | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | his projects feed each other | keep | |
| Night editions | the same | keep | magenta and the danger dots hold on navy |
| Mid editions | the same, on one tablet screen | keep | 457 px at 900; the whole route above the fold at 1,180 |
| Phone editions (390, 308) | the same, on one screen | keep | |
| Alt text | install, loop, stop, file | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image link to the repository | where the project lives | keep | |
| Link line | where to go | keep | |
| "Ben Russell builds …", Languages, Stack | what he builds, and with what | keep | |
| Pick sentence | which tool for which job | **change** | must-fix 2: add the difference that matters on someone else's server |
| rustmapper facts line | alive, tested, size, which commit | keep | |
| Wheel note | whether `pip` just works | keep | |
| "Before you run 0.1.3:" | the dangers, each with its lever | keep | the split is r13-1 #2 and the order is r13-2 #2; I agree with both and don't repeat them |
| rustmapper code block | how to run, when to stop, what to do after a kill | keep | |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy bullets 1–3 | storage, what happens to a page, how it's watched and deployed | keep | |
| Scrapy run sentence | what `start.py` starts, needs and loads | **change** | must-fix 1: one clause on the identity |
| Scrapy code block | how to point it at your site | **change** | must-fix 1: one line, `-s USER_AGENT=<your-bot>` |
| Grafana and `data/delta/` | where to look once it runs | keep | |
| Also: four tools | the reader of the file, the Go sibling, two more | keep | |
| 15 more (fold) | the rest | keep | |
| Working rules | how he works, each with a dated commit | keep | rule 1's "in a row" is r13-1 #1 |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release was drawn, how it was run, who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **Say who Scrapy's crawl claims to be, and give the lever.** (`README.md:80-90`, the hand-typed Scrapy run sentence
   and code block; one `[[figures]]` row; one test. About 8 lines.)
   - Code block: add one line before the `-a` lines, at 28 characters, inside the 32-column phone width:

     ```sh
     docker-compose run --rm \
       scraper scrapy crawl scout \
       -s USER_AGENT=<your-bot> \
       -a allowed_domains=<domain> \
       -a start_urls=<url>
     ```

   - Run sentence: replace "The last command crawls your site." with "The last command crawls your site; without
     `-s USER_AGENT`, its requests say `UConn-Discovery-Crawler/1.0`." That's 9 more words, about one line at 390. The
     flag starts its own line in the code block, so FLAG-WRAP isn't touched. Check the sentence with FLAG-WRAP at 320
     to 430 anyway.
   - `[[figures]]` row: text "`UConn-Discovery-Crawler/1.0`", repo Scrapy, path `Scraping_project/src/settings.py`,
     literal `USER_AGENT = _scrapy_config.get("user_agent", "UConn-Discovery-Crawler/1.0")`. Add an `absent` check
     that `Scraping_project/config.yml` has no top-level `scrapy:` key, so the clause fails FIGURES the day either
     the default or the config changes. Then the builder drops the clause, and keeps the `-s` line, which is good
     practice either way.
   - Test: README-STALE or FIGURES fails on a fixture where `config.yml` gains `scrapy: {user_agent: x}`.
   - Owner, in Scrapy: change the default to a name and contact for the project, for example
     `Scrapy-discovery/1.0 (+https://github.com/BenjaminSRussell/Scrapy)`. Do the same for the hard-coded
     `"MyScraper/1.0 (Educational Research Bot)"` in `src/stage4/large_doc_processor.py:86` and
     `"SitemapParser/1.0 (compatible; web crawler)"` in `src/stage1/sitemap_parser.py:299`. Add this to the carried
     "UConn defaults into a named profile" item.
   - Why: it is the one command on the page that makes a stranger misidentify themselves to a server, and the page
     is otherwise careful about exactly that relationship [S1–S7, R1].

2. **Put Scrapy's politeness in the pick sentence.** (`chart.toml:46` `pick`; three `[[figures]]` rows with
   `use = "pick"`; one test. About 15 lines.)
   - New text: "**rustmapper** gives you a site's list of URLs from one binary, with no services to run. His **Scrapy**
     repository keeps the pages themselves, deduplicated and summarized, and needs Docker. It obeys `robots.txt` and
     its `Crawl-delay`, and waits out a `Retry-After`." That's 13 more words, about two lines at 390, and less than a
     third of what r13-1's fold saves.
   - Rows, all in Scrapy at `96e7a1a`:
     - "obeys `robots.txt`": `src/stage1/middlewares/spider_config.py` literal
       `"ROBOTSTXT_OBEY": bool(spider_config.get("robotstxt_obey", True))`, plus an `absent` check that
       `config.yml`'s `stage1.spiders.scout` has no `robotstxt_obey: false`.
     - "its `Crawl-delay`": `spider_config.py` literal `PoliteRobotsTxtMiddleware": 100`, plus the test
       file `tests/unit/stage1/test_robots_policy.py` with `test_disallowed_path_is_never_requested_and_crawl_delay_is_capped`.
     - "waits out a `Retry-After`": `spider_config.py` literal `RetryAfterMiddleware": 560`, plus the test file
       `tests/unit/stage1/test_retry_after.py`.
   - Leave the caps (60 s, 120 s) out of the sentence. They would add two figures and two AUDIT rows to a sentence
     whose job is the choice. Scrapy's README states them for anyone who follows the link.
   - STRINGS-TWICE: "robots.txt" and "Crawl-delay" also appear in L4, but no five-word run is shared. Run the check
     anyway.
   - Test: the pick sentence's new clause is printed only while all three rows hold, and a fixture with
     `robotstxt_obey: false` under the scout drops it.
   - Why: the page's eight cautions tell a chooser what rustmapper doesn't do for the site it crawls. The one sentence
     written for choosing has to say that the other tool does it, or the comparison is only half made [S9]. It is
     also the strongest true thing the page can say about how he builds crawlers, and it is measured and tested in
     his own CI, not claimed.

3. **If W1 is reworded this round (r13-1 #3), the words must hold after a kill.** (`chart.toml:682` W1 `text`; the
   anchors and `runs` r13-1 gives. No change if r13-1 #3 isn't taken.)
   - r13-1 proposes "saved to disk as it goes, so a kill keeps the crawl". The run check says otherwise:
     `kill_writes_file` failed (SIGTERM, "sitemap.jsonl was not written") and `resume_after_kill` failed
     ("Database already open. Cannot acquire lock"). Only `export_after_kill` passed (3 `<loc>`). After a kill you
     keep the 200 pages as `sitemap.xml`, not the crawl, not the JSONL and not a resumable run. Round 12 took
     "resume" out of the go_go_go line for the same reason.
   - Wording that holds, at 51 characters, the same length as r13-1's: "saved as it goes; export-sitemap works after a
     kill". Five-word runs against the code block's "# sitemap.xml, even after a kill": none shared.
   - Keep r13-1's limit: one line on the phone sheet in every edition, with `runs = ["export_after_kill"]` and
     `fails = ["kill_writes_file"]`, so the row is reworded the day 0.1.4 writes the file on SIGTERM.

## Notes (true, not ranked)

1. **0.1.3 asks for robots.txt on the wrong port.** I served 12 pages over https on 127.0.0.1:8743 with no robots.txt
   and a trusted self-signed certificate (`scratchpad/r13-3/probe/`). 0.1.3 printed "missing robots.txt, fetching in
   background (allowing crawl)" once. The server never got a `GET /robots.txt`. It got 12 page requests, the first
   seven 11 to 14 ms apart. `fetch_robots_txt` builds `format!("https://{}/robots.txt", domain)` from the host
   without its port, so a site on a non-default port has its rules read from port 443, or not at all. Few strangers
   crawl a non-default port, and L4 already says the release reads robots.txt only over https. This is for the owner's
   0.1.4 list, next to P1: build the robots URL from the queued URL's scheme, host and port (`url_utils::robots_url`
   already does).
2. **The next leg has no entry on the page.** The arrow says the file is "sorted 21 ways by ideal-url-organizer", and
   the Also line says "21 ways to sort a pile of URLs from their crawl records". Neither says the one command that
   continues the passage (`python3 scripts/import_rust_sitemapper.py <path-to-sitemap.jsonl>`, after copying the
   config and installing its requirements). Round 6 cut the script path from the image, and that was right. If the
   Also line ever has room, "— reads rustmapper's `sitemap.jsonl` and sorts the URLs 21 ways …" would make the
   continuation note match the chart it points to.
3. **Three names for one thing.** The image says rustmapper, the command is `rust_sitemap`, and the link goes to
   `Rust-sitemap`. P4 fixes the command. Renaming the repository to `rustmapper` would fix the third. GitHub redirects
   the old name for web traffic, clones, fetches and pushes. Its one exception is Actions that call the repository by
   name [S10], and nothing here does.
4. **Agreed with this round, not repeated.** r13-1 #1 (rule 1 "in a row"), #2 (the fold); r13-2 #1 (DESIGN.md says
   which cautions were probed), #2 (the caution order follows the drawing).

## Sources (new this round; none cited in earlier rounds)

1. [S1] RFC 9110, *HTTP Semantics*, §10.1.5 User-Agent: the field identifies "the user agent software"; "implementations
   are encouraged not to use the product tokens of other implementations … as this circumvents the purpose of the
   field": https://www.rfc-editor.org/rfc/rfc9110#section-10.1.5
2. [S2] Scrapy's `startproject` template, `settings.py.tmpl`: "# Crawl responsibly by identifying yourself (and your
   website) on the user-agent", and `ROBOTSTXT_OBEY = True`:
   https://github.com/scrapy/scrapy/blob/master/scrapy/templates/project/module/settings.py.tmpl
3. [S3] Cloudflare, "Verified bots policy": a verified bot "declares who it is deterministically", "represents itself
   honestly" and "obeys robots.txt and crawl directives"; one example breach is not respecting crawl-delay:
   https://developers.cloudflare.com/bots/concepts/bot/verified-bots/policy/
4. [S4] Google Search Central, "Verifying Googlebot and other Google crawlers": verification for when "troublemakers
   are accessing your site while claiming to be from Google":
   https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot
5. [S5] Common Crawl, "CCBot": identifies as `CCBot/2.0 (https://commoncrawl.org/faq/)`; notes that some crawlers
   falsely identify as CCBot, and gives reverse DNS for checking: https://commoncrawl.org/ccbot
6. [S6] Transport Canada, Ship Safety Bulletin 10/2016, on IMO Resolution A.1106(29): the OOW checks "own ship's
   static information"; "Inaccurate and/or missing AIS information is a safety concern"; "users remain responsible for
   all information entered":
   https://tc.canada.ca/en/marine-transportation/marine-safety/ship-safety-bulletins/automatic-identification-system-ais-ssb-no-10-2016
7. [S7] IMO, Resolution A.1106(29), *Revised guidelines for the onboard operational use of shipborne AIS*, the source
   of S6's duties (identity is static data, set at installation and checked by the watch):
   https://wwwcdn.imo.org/localresources/en/OurWork/Safety/Documents/AIS/Resolution%20A.1106(29).pdf
8. [S8] MDN, `Retry-After`: in a 429 it "indicates how long to wait before making a new request"; in a 503, how long
   the service is expected to be unavailable:
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Retry-After
9. [S9] UKHO, *Admiralty Sailing Directions*: each volume gives "navigational hazards, buoyage, pilotage,
   regulations" and "port facilities", "to support port entry": the hazards and the services side by side, so a
   master can choose:
   https://www.admiralty.co.uk/publications/publications-and-reference-guides/admiralty-sailing-directions
10. [S10] GitHub Docs, "Renaming a repository": "all existing information, with the exception of project site URLs,
    is automatically redirected"; clone, fetch and push keep working; Actions are not redirected:
    https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository

[R1] Cited again, not counted as new: Scrapy, "Settings": command-line settings "have the highest precedence"; `USER_AGENT`
defaults to `Scrapy/VERSION (+https://scrapy.org)`: https://docs.scrapy.org/en/latest/topics/settings.html (the `-s` lever in must-fix 1).

Code and data:
- Scrapy `96e7a1a`:
  - `Scraping_project/src/settings.py:24-74, :115, :121`;
  - `src/stage1/middlewares/spider_config.py` (`get_spider_settings`);
  - `robots_middleware.py:1-15, :77`;
  - `retry_after_middleware.py:1-35`;
  - `config.yml` (no `scrapy:` key; `stage1.spiders.scout`);
  - `docker-compose.yml` (`scraper`, no entrypoint);
  - `tests/unit/stage1/test_robots_policy.py`, `test_retry_after.py`, `test_robots_fixtures_526.py`;
  - `src/stage4/large_doc_processor.py:86`, `src/stage1/sitemap_parser.py:299`;
  - `data/raw/uconn_urls.csv`.
- Sdist 0.1.3: `src/bfs_crawler.rs:168-265, :428-440`; `src/frontier.rs:675-810`; `src/robots.rs:18-24`;
  `src/network.rs:22-70`; `src/cli.rs:16-130`.
- ideal-url-organizer `159968a`: `scripts/import_rust_sitemapper.py:1-20`.
- `assets/stats.json`: `edition`, `routes.rustmapper`, `runcheck.rustmapper.steps`, `figures`, `repos[]`,
  `coauthored_total`, `agent_authored`.
- My probe: `scratchpad/r13-3/probe/` (`srv.py`, `req.log`, `crawl.log`, `d/sitemap.jsonl`).
