# Review round 15, reviewer 2: the systems engineer who checks every claim against the clones

10 Oct 2026. I have shipped crawlers and storage engines. I read every claim against the code, then run the code. I
looked at every PNG in `scratchpad/r6/build/round-14/`: the sheet on desk at 870 and 846 (day, night), mid at 746
(day, night), phone at 390 and 308 (day, night), the desk page (two screens), the phone page at 390 (six screens) and
at 360 (seven), and the first screen at 900, 1,180, 1,280, 1,366 and 1,920. I read `README.md`, `SPEC.md`, `LOG.md`
through round 14 and the round 14 reviews. I don't repeat anything already fixed.

Verdict: **not yet. 7 / 10.** The drawing is the right form, and every row on it holds against the 0.1.3 sdist and
the run check. But I ran 0.1.3 against a site served over https with an ordinary `robots.txt`, and it fails there in
a way the page never mentions. **The first link a host's `robots.txt` disallows ends the crawl of that host.** On a
shop-shaped fixture (header links to `/search` and `/cart`, both disallowed the way Shopify disallows them), 0.1.3
fetched 4 pages in 70 s and never asked for any of the 12 product pages. Then the drawn trap ("done when `Received
work item` lines stop for 60 s") told me the crawl was done. The run check missed this because every probe serves
plain http, and 0.1.3 never reads `robots.txt` over http. The second fault: when `robots.txt` takes 50 ms or more to
come back, 0.1.3 fetches the host's first 20 pages without it, disallowed ones included. Both faults are in the
release the image tells a stranger to install, and neither is on the page.

## The first question: does it meet the owner's goal?

- **A deep purpose for the map.** Yes. The image is directions through one tool: how you get it, where its URLs
  come from, the loop each page goes through, how you know it's done, how you stop it, the file you get, and who
  reads that file next. Nothing has a size. Nothing is drawn for decoration.
- **True and useful about his actual projects.** Every row is true. The set of rows is not: the one trap it draws is
  less dangerous than one it leaves out. A stranger who follows the image on a typical shop or docs site gets a file
  that is mostly blank `status_code` rows, and the image's own "done" rule tells them nothing went wrong. A map that
  marks the shallow you can see and leaves out the reef you can't is the wrong way round (must-fixes 1 and 2).
- **Nothing chases a reason.** In the image, one row is weak. W1, "saved as it goes; export works after a kill",
  reassures more than it directs, and the code block under the cautions already says it ("# sitemap.xml, even after a
  kill"). It is the row to give up when must-fix 2 needs the space.
- **Nothing announces the theme.** True. No word names it.
- **Reads on a phone.** The image fits one 390 screen and still reads at 308. The page is long (5,109 CSS px at 390),
  but every block below earns its place except where noted.

## What I ran

All runs used the 0.1.3 binary the run check installed from PyPI
(`scratchpad/r6/runcheck/work/v/bin/rust_sitemap`), `--seeding-strategy none`, against Python's `http.server` over
TLS on 127.0.0.1:443. Port 443 matters because 0.1.3 builds the robots URL without the port
(`format!("https://{}/robots.txt")`, round 13 note). The certificate was trusted with `SSL_CERT_FILE`, and
`NO_PROXY=localhost` kept the session proxy out. Fixtures and logs are in `scratchpad/r15-2/probe/`.

| Run | Site | `robots.txt` | What the server saw | File |
|---|---|---|---|---|
| control | home links `/p1`…`/p10` | `Disallow: /nothing-here`, instant | `/`, `/robots.txt`, all 10 pages | 11 rows, 11 with 200 |
| stall | home links `/p1`…`/p5`, `/secret1.html`, `/p6`…`/p10` | `Disallow: /secret`, instant | `/robots.txt`, `/`, `/p1`…`/p5`; then `blocked by robots.txt` once and nothing more in 25 s. Run twice, same both times | 12 rows, 6 with 200; `/p6`…`/p10` never asked for |
| shop | header `/collections/all`, `/pages/about`, `/search`, `/account/login`, `/cart`; 12 product links | allbirds.com's lines for `/cart`, `/account`, `/checkout`, `/search` [S6, S7], instant | `/`, `/robots.txt`, `/collections/all`, `/pages/about`; `/search` blocked; 70 s of nothing; one SIGINT | 18 rows, **1** with a `status_code`; 0 of 12 products fetched |
| late, 50 ms | home links `/secret1`…`/secret10` and `/p1`…`/p10` | `Disallow: /secret`, answered after 50 ms | all 10 disallowed pages, 0 `blocked` lines | 21 rows |
| late, 150 ms and 500 ms | same | same, 150 ms and 500 ms | all 10 disallowed pages both times; at 500 ms, 6 of them were requested after `robots.txt` had been served | 21 rows |

The code says the same thing. In `sdist:src/frontier.rs`:

- `:684-690`: a URL that `robots.txt` disallows logs "blocked by robots.txt" and then `continue`s. The ready host it
  was popped with is not pushed back, unlike the backoff branch (`:644`) and the at-capacity branch (`:667`), so the
  rest of that host's queue is never scheduled again.
- `:728` and `:808`: with no `robots.txt` cached yet, it starts a background fetch, prints "missing robots.txt,
  fetching in background (allowing crawl)", and goes on dispatching. Only the per-host cap stops it (`state.rs:285`,
  `max_inflight: 20`).

Main re-pushes the host after a blocked URL (`frontier.rs:808-816` at `32c2651`; the re-push was in place by
`6bcb6cd`, 13 Nov 2025, five days after 0.1.3), and it fails closed until `robots.txt` arrives (#47). So both faults
are 0.1.3's, which is what the page is about.

I also built main at `32c2651` (`cargo build --release`, 4 min 57 s on this 4-core box) and ran the control and shop
sites. It asked for `/robots.txt`, got a 200, printed "deferring https://localhost/ until robots.txt for localhost
is fetched" once, and never asked for `/`. After 30 s it reported "frontier empty, 0 in-flight". I haven't found the
cause, and it may be specific to loopback. It goes on the owner's list, not the page. If it is real, a 0.1.4 cut from
main as it stands would crawl nothing on https sites.

## Figures checked

| Printed | Source | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.date`; PyPI uploads | yes |
| `rust_sitemap crawl` | `edition.scripts` `["rust_sitemap"]` | yes |
| by default also from sitemaps, certificate logs and Common Crawl | `sdist:src/cli.rs:58` `default_value = "all"`; `bfs_crawler.rs:190-212` | yes. Note: the seeders run to the end *before* the start URL is queued (`bfs_crawler.rs:215-266`), so a default run can show no work-item line for as long as crt.sh and Common Crawl take. Not a must-fix: "stop for 60 s" can't fire before the lines start |
| up to 20 pages at a time from each host | `state.rs:285`; `frontier.rs:655` | yes |
| your site, its subdomains and its parent domain | `url_utils.rs` `is_same_domain`, both branches | yes |
| saved as it goes; export works after a kill | runcheck `export_after_kill` 3 `<loc>`; `kill_writes_file` false | yes, and it claims no more |
| never exits by itself; 60 s | runcheck `ends_by_itself` false, `quiet_slow_page` ok | yes. After a stall the lines also stop, and the rule then reads "done" (must-fix 2) |
| second press before `Saved to` | runcheck `second_ctrl_c` | yes |
| fields `url, depth, status_code, title` | `state.rs` `SitemapNode`; my files | yes |
| sorted 21 ways | `figures` "21 ways"; `import_rust_sitemapper.py` `URL_RECORD_FIELDS`, 15 fields | yes |
| 176 test functions · 16k lines of Rust · CI passed 7 Oct | `repos[Rust-sitemap]` 176, 16,390, success 2026-10-07 | yes |
| 45 of its 146 commits; co-signed 1 of his own 101 | `others` Claude 45; `commits` 101; `coauthored.agent` 1 | yes |
| 1,920 (all but 41) · 8 Oct · MIT · 69k | `repos[Scrapy]` 1,920, success 2026-10-08, MIT, 69,036 | yes |
| 71 of its 499; co-signed 30 of his own 420 | jules 49 + Claude 22; 420 + 49 + 22 + dependabot 8 = 499; `agent` 30 | yes |
| 3 min from a cold cache, 4 cores | runcheck `install`: median 171.4 s, 3 runs, 4 CPUs | yes |
| 256 at a time; `--workers 1` | `cli.rs:32`; runcheck `workers_cap` | yes |
| 15 more | 22 repositories − profile − 2 − 4 | yes |
| rule 1: 5 in a row, 60 s | Scrapy `099dd6c`, his, 8 Oct 2026 | yes |
| rule 3: 6 days, then 5 | `rules`: first commit 2025-09-25, Prometheus 10-01, Grafana 10-06 | yes |
| "its commands were run … against a local 3-page site" | runcheck: all fixtures over `http://127.0.0.1` | true, and it's the gap: no probe has ever crawled over https, the only scheme on which 0.1.3 reads `robots.txt` |

## Every element of the image

| Element | What a visitor learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell" | whose page this is | keep | read first at every width |
| Role, two caps lines | crawl and data infrastructure; Python and Rust | keep | the image proves "crawl"; the text below proves the rest |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which tool, and what you get | keep | true even after a stall: the blank rows are still lines. Must-fix 2 is what stops it misleading |
| Start bar + `pip install rustmapper` + 0.1.3 · 8 NOV 2025 | the way in, and that the release is 11 months old | keep | an honest age; the fix is a release |
| Magenta track | one way through, top to bottom | keep | |
| S1 ring: `rust_sitemap crawl` starts from your URL; seeds by default | the command that runs, and where URLs come from | keep | |
| F1 ring: up to 20 per host; scope | the per-host cap and what's in scope | keep | this is where the stall happens; the new trap goes right under it |
| Loop bracket + arrow | which rows repeat for each page | keep | only a drawing shows it |
| W1 ring: saved as it goes; export works after a kill | a kill doesn't lose the export | **cut** (for must-fix 2's space) | true, but it's the one row that reassures rather than directs, and the code block already carries it: "# sitemap.xml, even after a kill" |
| H1 dotted box: never exits by itself; done when lines stop for 60 s | how you know it's finished | keep | true and needed. With the stall trap above it, a stranger knows a quiet minute can mean blocked as well as finished |
| Gap in the track under the loop | no exit except Ctrl-C | keep | |
| C1 ring: Ctrl-C once; second press loses the file | the one action, and what a second press costs | keep | |
| End bar + `data/sitemap.jsonl` + fields | the output contract, in the struct's own names | keep | a data engineer reads this row first |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | his projects fit together, and the join is tested | keep | |
| **Missing: the robots.txt stall** | that on a site with linked disallowed pages, the crawl of that host ends early | **add** (must-fix 2) | the trap a stranger is most likely to hit on a real site, at the stop where it happens |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Link line | where the two projects and the release live | keep | |
| "Ben Russell builds …", Languages, Stack | who, and with what | keep | |
| Pick sentence | which project fits which job | keep | "a site's list of URLs" holds once the stall is in the open list |
| rustmapper facts line | main is tested, current and his, with the agent share next to the counts | keep | every figure holds |
| Install note (wheel, 3 min) | whether pip will just work | keep | measured |
| "Before you run 0.1.3:" open list (L1, L4, L2, L5) | load, robots.txt, seeding, scope, each with its lever | **change** | L4 leaves out both robots faults (must-fixes 1 and 3) |
| Fold: what 0.1.3's files miss or get wrong | JS, redirects, status codes, sitemap.xml | keep | correct split; these are file-content faults |
| Code block | the three lines, and when to stop | keep | |
| Scrapy lead + facts line | what Scrapy is, and that it's tested and alive | keep | |
| Scrapy bullets 1 to 3 | raw-first storage, dedup and summaries, operations | keep | true (re-read at `96e7a1a`); bullet 3 is the strongest operations evidence on the page |
| Scrapy run paragraph | what `start.py` starts, what it needs, what each stage does to a site | keep | long on a phone (17 lines at 390), but every clause is something an operator needs, and "disallowed ones too" is honest |
| Scrapy code block + Grafana line | how to run it and where output lands | keep | |
| Also (4) | the four next-best projects, one line each | keep | |
| 15 more | the rest, folded | keep | |
| Working rules (3) | how he builds, each with a dated commit | keep | |
| Found a mistake? | where corrections go | keep | |
| Data line | what was run, and how counts are counted | **change** | true, but after must-fix 4 it must say the probes ran over https as well (must-fix 5) |
| License line | | keep | |

## Must fix, ranked

1. **Add the stall to the open list of cautions.** `chart.toml`, a new `[[route.rustmapper.entry]]` `L6`,
   `stage = "server"`, `short = "robots.txt stall"`, `scope = "release"`, `item = true`, placed right after L4 so the
   open list reads L1, L4, L6, L2, L5 (5 of 7 items). Text, 21 words: "On an https site, the first link `robots.txt`
   disallows ends that host's crawl: the links queued after it are never asked for." `release` anchors:
   `src/frontier.rs` contains `"Shard {}: URL {} blocked by robots.txt",` followed by `continue;` before any
   `push_ready_host` in the same branch. Add `fn`-scoped matching if `proof.py` needs it, or use `before =` as X2
   does. `runs = ["robots_stall"]` (must-fix 4). The `instead` is empty text, retired by `fails = ["robots_stall"]`,
   so the item goes the day a release re-queues the host. Why: on any site whose `robots.txt` disallows a page it
   links to, which is every Shopify store's `/cart` (5.4 % of all websites run Shopify [S8]), 0.1.3 crawls a few pages
   and stops, and nothing on the page says so. Size: one list item, 2 phone lines at 390.

2. **Draw the stall in the loop, and cut W1 to keep the height.** `chart.toml` route: a new `kind = "trap"` entry
   `H0`, `loop = true`, `scope = "release"`, directly after F1, in the same dotted danger box as H1. Text: "the first
   link `robots.txt` disallows ends that host's crawl" (desk one line; phone two lines at 600 units). Use L6's
   anchors and `runs = ["robots_stall"]`. Remove W1 from the drawn entries, but keep its row in `chart.toml` and give
   it `drawn = false` so the AUDIT trail stays. Update `PURPOSE`, `BREAKS` and T-PURPOSE. The phone sheet goes from
   1,121 to about 1,155 units (two trap lines, about 80, minus W1's one line and gap, about 46), under the 1,246 gate.
   The desk sheet goes from 707 to about 707 (one line each way). Why: the image's job is "where a stranger goes
   wrong". This is the place, it sits at the F1 stop where it happens, and without it H1's "done" rule calls a stalled
   crawl finished. Alt text: "two traps are marked" if the alt text counts them.

3. **Say in L4 that 0.1.3 fetches before it has the rules.** L4's text becomes, 22 words: "It fetches up to 20
   pages per host before that host's `robots.txt` is back, ignores `Crawl-delay`, and reads `robots.txt` only over
   https." Add the release anchors `src/frontier.rs` text `"missing robots.txt, fetching in background (allowing
   crawl)..."` and `"// Proceed with crawling - don't block on robots.txt"`, plus `state.rs` `max_inflight: 20`, and
   `runs = ["robots_late"]`. Keep the two existing `instead` rows, each with the same first clause while
   `robots_late` holds. Why: with a 50 ms `robots.txt`, all 10 disallowed pages in my fixture were fetched. "Asks for
   robots.txt only over https" reads as if https sites were safe, and they aren't.

4. **Probe over https.** `scripts/runcheck.py`, two new steps, each 30 to 70 s:
   - Fixture: `tests/fixtures/route-site-https/`, the stall and late sites above. Use a throwaway certificate made per
     run with `openssl req -x509 -newkey rsa:2048 -nodes -subj /CN=localhost -addext
     subjectAltName=DNS:localhost,IP:127.0.0.1`. Serve it with `http.server` wrapped in `ssl` on 127.0.0.1:443. Port
     443 is needed because 0.1.3 drops the port from the robots URL. On the Linux runner, bind it with `sudo sysctl -w
     net.ipv4.ip_unprivileged_port_start=443` [S10], or run the server under sudo. Run the crawler with
     `SSL_CERT_FILE=<cert>` and `NO_PROXY=localhost,127.0.0.1`, and crawl `https://localhost/`.
   - `robots_stall`: `robots.txt` answered at once with `Disallow: /secret`; the home page links five allowed pages,
     one disallowed, then five more. Passes (the fault is present) if, after 30 s and one SIGINT, none of the five
     pages after the disallowed link was requested.
   - `robots_late`: `robots.txt` answered after 0.5 s; the home page links ten disallowed and ten allowed pages.
     Passes if any disallowed page was requested.
   - Tests: a fixture release that re-pushes the host fails `robots_stall` and retires L6 and H0. A probe that can't
     bind 443 marks both steps `skipped`, and ROUTE-ENTRANCE warns. It must not pass them by default.

   Why: the run check's fixtures are all `http://`, and 0.1.3 doesn't read `robots.txt` over http, so nothing in the
   pipeline has ever exercised the release's robots path. That is how a fault this size got through 14 rounds.

5. **Data line: name both schemes.** `chart.toml [copy]` survey text: "its commands were run, with seeding off,
   against local test sites over http and https on 10 Oct 2026 (Linux x86_64)." Print it only when both new steps
   ran. Why: "a local 3-page site" was true of the first probe and understates the rest. After must-fix 4 the reader
   should know the robots claims were run, not only read in the code.

## Notes, not ranked

1. **Owner, outside this repository.** (a) Cut 0.1.4. Main already re-queues the host after a blocked URL and fails
   closed until `robots.txt` arrives, and it stops when idle. Those three fixes retire H1, H0 and L6 by themselves.
   (b) Before cutting it, run main against an https site with a 200 `robots.txt`. My build of `32c2651` deferred the
   start URL once and then reported an empty frontier without fetching it, on both the control and shop fixtures
   (`scratchpad/r15-2/probe/crawl_main_*.log`). It may be loopback-specific, but it has to be ruled out, along with
   P1. (c) In 0.1.3's shop run, `/collections/all` and `/pages/about` were fetched with 200 and still written with
   `status_code` null, so the file under-reports even the pages it did fetch after a block. The control run doesn't
   show this, so it is tied to the block. That is worth a test on main.
2. **Seeders run before the start URL.** `initialize` drains every seeder, then adds the start URL
   (`bfs_crawler.rs:215-266`). A default run on a big domain can sit for minutes on "Running 3 seeder(s)..." with no
   work-item line. The page's L2 lever (`--seeding-strategy none`) already covers what a stranger should do, so this
   is a note.
3. **How others do it.** Scrapy's `RobotsTxtMiddleware` parks every request for a host on a Deferred until that
   host's `robots.txt` is parsed [S1]. Python's `urllib.robotparser` is read-then-`can_fetch` [S2]. Heritrix runs DNS
   and robots.txt as preconditions before a URI is fetched [S9]. 0.1.3 is the outlier, and main has moved to the
   standard behaviour. That is the story 0.1.4 should tell.

## Sources (new this round; none cited in earlier rounds)

- [S1] Scrapy, `scrapy/downloadermiddlewares/robotstxt.py` (a Deferred per netloc; requests await it):
  https://raw.githubusercontent.com/scrapy/scrapy/master/scrapy/downloadermiddlewares/robotstxt.py
- [S2] Python docs, `urllib.robotparser` (`read`, `can_fetch`, `crawl_delay`):
  https://docs.python.org/3/library/urllib.robotparser.html
- [S3] HTTP Archive, Web Almanac 2024, SEO chapter (83.9 % of mobile `robots.txt` requests return 200; `*` group in
  76.9 % of files): https://almanac.httparchive.org/en/2024/seo
- [S4] Google, robotstxt C++ library (the matcher 0.1.3's `robotstxt` crate ports): https://github.com/google/robotstxt
- [S5] docs.rs, `robotstxt` crate (native Rust port of Google's matcher; `DefaultMatcher`):
  https://docs.rs/robotstxt/latest/robotstxt/
- [S6] Shopify Help Center, "Editing robots.txt" (default rules disallow `/cart`, `/checkout`, `/account`, filtered
  and sorted collections): https://help.shopify.com/en/manual/promoting-marketing/seo/editing-robots-txt
- [S7] allbirds.com `robots.txt`, a live Shopify store (`Disallow: /cart`, `/account`, `/checkout`, `/search`):
  https://www.allbirds.com/robots.txt
- [S8] W3Techs, content management systems overview, 10 Oct 2026 (WordPress 40.1 %, Shopify 5.4 % of all websites):
  https://w3techs.com/technologies/overview/content_management
- [S9] Heritrix 3 documentation, "Configuring Jobs" (`robotsPolicyName`; DNS and robots.txt preconditions):
  https://heritrix.readthedocs.io/en/latest/configuring-jobs.html
- [S10] Linux kernel documentation, `ip-sysctl`, `ip_unprivileged_port_start`:
  https://docs.kernel.org/networking/ip-sysctl.html
- Clones and runs: `sdist rustmapper-0.1.3` `src/frontier.rs:644, :667, :684-690, :728, :808`, `src/state.rs:285`,
  `src/bfs_crawler.rs:170-266`, `src/cli.rs:24, :32, :58`; Rust-sitemap history `6bcb6cd` (13 Nov 2025), `0539faf`,
  `44b9779`, HEAD `32c2651` `src/frontier.rs:780-847`; ideal-url-organizer `159968a`
  `scripts/import_rust_sitemapper.py`; Scrapy `099dd6c`; probe fixtures and logs in `scratchpad/r15-2/probe/`.

The web search budget for this turn ran out before I started. Every source above was read directly, by URL.
