# Concept B: the picture is one of his crawls

Round 6, 9 Oct 2026. Angle: the image shows the thing his tools actually map, which is a website as his crawler
walks it. It is drawn from the record his crawler writes, so the picture is the output of his work, not a picture
about it.

## The one sentence

**rustmapper walked a whole website, and here is what it found: how many pages sit at each distance from the front
page, what failed, and when it finished.**

That is the owner's test applied to the image. "What is it showing?" One real crawl. "How does it help the user see
my project?" It is what the project produces, so a visitor sees the output before reading any claim about it.
"Is it based on the size of the project or how many commits?" Neither. Every mark is a count of pages from a file
the crawler wrote, and the axis says what it counts.

## Why this subject has a real geography

- Distance on the web is counted in links from a start page. A breadth-first crawler's own order follows that
  distance (R7 F4; Najork and Wiener via R7 [40]). Crawl tools draw exactly this: Screaming Frog defines crawl depth
  as "number of 'clicks' away from the start page" (Screaming Frog SEO Spider user guide, Tabs, read 9 Oct 2026), and
  Scrapy has a setting whose only job is to count requests at each depth (`DEPTH_STATS_VERBOSE`, R7 [43]).
- rustmapper records it for every page: `depth`, `parent_url`, `status_code`, `crawled_at`, `response_time_ms`
  (`Rust-sitemap/src/state.rs:131-150`; a found link gets `job.depth + 1`, R7 F5, `bfs_crawler.rs:590`).
- Reaching a page is a real problem with a real cost. In Broder's crawls a path between two random pages existed 24 %
  of the time (R7 F3). Google tells sites to link each paginated page to the next "to help Googlebot ... find
  subsequent pages", because its crawler follows `<a href>` links and does not click (Google Search Central,
  "Pagination, incremental page loading, and their impact on Google Search", updated 10 Dec 2025).

So the horizontal space of the picture means one thing: links travelled from the front door. Position means
something real, as F1 of R3 and F15 of R1 demand. Nothing is laid out by a date.

## The target: books.toscrape.com

- **Permission.** toscrape.com describes it as "A fictional bookstore that desperately wants to be scraped. It's a
  safe place for beginners learning web scraping and for developers validating their scraping technologies"
  (toscrape.com, read 9 Oct 2026). The site's own banner says it is "a demo website for web scraping purposes". That
  meets R7 I5 (a target with permission) without inventing a site to be mapped.
- **It has a shape worth seeing.** I crawled it on 9 Oct 2026 to find out (trial below). The result has a peak close
  to the door and a long thin tail: the paginated listing is reached one "next" link at a time, so its last page is
  50 links from the front, while every one of the 1,000 book pages is within 9. A visitor sees in one look what a
  crawler is up against: most of a site is near, and some of it is a long way down a single path.
- **Ruled out.** crawler-test.com (built by a crawler vendor to break crawlers) is a catalogue of SEO test cases,
  mostly at depth 1. In the trial, go_go_go stalled on it after 119 pages. Putting that on the profile would show
  his crawler failing a stress test, which may be true and useful to Ben, but it is not what a stranger needs first.
  Sites he does not have permission to crawl (the eleven in ideal-url-organizer's viewer spec, R6 F5) are ruled out.
  He owns no domain: `benjaminsrussell.github.io` returns 404, and no clone has a CNAME file.
- **Certificate Transparency is not drawn.** crt.sh lists 2 certificates and 2 names under crawler-test.com, and
  books.toscrape.com is a single host. On a single-host site CT adds nothing, and R7 I5 forbids printing someone
  else's host list. rustmapper's CT seeder stays a sentence in the text.

## What the research trial found (evidence, not for print)

Both runs were made from this session's sandbox on 9 Oct 2026, links only, with robots.txt obeyed and small caps.

**rustmapper at HEAD `00a877d` (7 Oct 2026), built from `/home/user/rust-sitemap` (`cargo build --release`, 5 min).**
`rust_sitemap crawl --start-url https://books.toscrape.com/ --workers 8 --seeding-strategy none --max-urls 1500
--duration 300` printed `Added 1 start URL(s) to frontier`, then `Shard 1: deferring https://books.toscrape.com/
until robots.txt for books.toscrape.com is fetched`, and nothing more. No page was fetched. `--duration 300` did not
stop it; `timeout` killed it at 400 s. The same happened on crawler-test.com, whose robots.txt returns 200: killed at
330 s with `--duration 240`. The debug log shows the robots.txt request was answered (a pooled connection was
logged), so the request itself got out. The code explains the books case. `robots.rs:18-24` returns `None` for any
status other than 200, and `frontier.rs:750-764` (the fail-closed change of #50, 7 Oct 2026) defers the URL for as
long as there is no robots body. RFC 9309 §2.3.1.3 says the opposite for a 4xx: the crawler "MAY access any
resources on the server". books.toscrape.com's robots.txt is a 404. I did not isolate the crawler-test.com case. The
sandbox goes through an HTTPS proxy, so this must be reproduced on Ben's machine before anyone reads it as a verdict.
The released 0.1.3 predates #50; a build of it was not allowed in this session.

**go_go_go at clone HEAD `4078b55` (7 Oct 2026), his Go crawler** (`go build`, then `crawl --start-url
https://books.toscrape.com/ --seeding-strategy none --max-pages 1300 --max-depth 80 --per-host-concurrency 2
--workers 4 --use-header-rotation=false --user-agent GoGoGoBot`). It finished on its own: "Crawl completed!
Discovered: 1194, Processed: 1195, Errors: 0". `sitemap.jsonl` holds 1,195 rows, all status 200. The first
`crawled_at` is 21:57:31Z and the last is 21:59:32Z (2 min 01 s). Pages at each depth:

| depth | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 to 49 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pages | 1 | 73 | 512 | 214 | 129 | 71 | 44 | 33 | 23 | 14 | 2 each | 1 |

The 1,000 book pages all sit at depths 1 to 9. Depths 10 to 50 hold only listing pages: `catalogue/page-N.html` and
`catalogue/category/books_1/page-N.html`. The deepest row is `catalogue/category/books_1/page-50.html` at 50. One
pair of URLs is byte-identical (`/` and `/index.html`, same `content_hash`). This proves the data exists, the
target's shape is legible, and his own code can produce it today. The printed sheet must come from a rustmapper
record (below), not from this table.

## The image, element by element

Every element states what a visitor learns, why this form is right, and the evidence. Anything that cannot be
stated that way is listed under "Removed".

| # | Element | What a visitor learns | Why this form | Evidence |
|---|---|---|---|---|
| 1 | Name, serif display | Whose page this is | The name is the first of six data points a screener reads (R4 F1) | R4 [32]; current hero |
| 2 | Role line, "Crawl and data infrastructure · Python and Rust" | What he builds | The title and text carry the message people take away (R5 F2 [8]); the role line must name what the picture shows (R5 I10) | R5 I10; R6 F1 (seven of 21 repositories acquire web data) |
| 3 | Crawl terms, five or six short lines: target; "a site built to be scraped"; tool and version; "links only · robots.txt obeyed"; pages, errors, time; stop reason and date | Which crawl this is, done by what, under what rules, and whether it finished. Without these the drawing cannot be trusted | This is a chart's title block: read first, it says what was measured and when (R1 F2). For a crawl, the seed, limits and date are the legend, and a crawl map that omits them misleads (R7 F3, I4). A crawl shown in public must show its own good conduct (R7 F12) | `stats.crawl.*` (new, below); RFC 9309 [R7 24]; toscrape.com statement |
| 4 | Lollipop columns, one per depth 0 to max: a stem whose length is the number of pages at that depth, and a fixed-size head on every depth that has pages | How the site spreads out from the front page: most pages are close, and the reach is long | Length on a common baseline is the most accurately read channel (R1 F16, R3 F6, R5 F6). A fixed head marks "pages exist here" even where the count is 1 or 2. A stem that short is under a screen pixel, and blank would read as "nothing there" (R1 F13: blank is a warning, not empty water) | `crawl.by_depth[]`; trial table above |
| 5 | Depth axis, ticks every 10, caption "links from the front page" | What position means, in plain words | Every serious map states what position means (R7 F1, F2; R3 F1). The caption names the data, never the theme (R3 I7) | Screaming Frog depth definition; `depth` field, `state.rs` |
| 6 | Peak label, the count above the tallest column (trial: 512 at depth 2) | The scale, read once, without a y-axis | Direct labelling of the one value that sets the scale; no gridlines needed (R3 F15: no legend to learn) | `crawl.peak {depth, n}` |
| 7 | Tail bracket over the run of short columns: "2 pages at each depth" (text built from the data) | That the deep end is a single narrow path, not a mass of pages | The shape is the lesson. The bracket states the count the eye cannot read at that height | `crawl.by_depth[]`, run-length of equal counts |
| 8 | Deepest-page label, path tail with a hairline leader (trial: "…/books_1/page-50.html") | The concrete thing at the far end: the last page of a list, 50 links in | The one most important point on the route gets its name (S-52 prominence by importance, R1 F1) | `crawl.deepest {depth, url}`; `parent_url` chain in rustmapper's record |
| 9 | Outcome colour on the heads: ink for fetched OK; the caution colour for failed (4xx, 5xx, timeout); an open head for found but not fetched (robots-disallowed, or left in the frontier at a cap) | What broke and what was not entered, where in the site | Colour is a code with fixed meanings: caution for hazards, never decoration (R1 F6, I9). Only classes that occur are drawn, so the trial run would be all ink | `status_code`, `crawled_at` null; `crawl.by_status` |
| 10 | One hairline frame | Separates the image from the README text | The owner asked that images and text "differentiate themselves" (BRIEF). It replaces the graduated border, which on a real chart is a scale and here measured nothing (R1 F12) | BRIEF, earlier quotes |

Removed, because none passes the test: the week islands and shallows (R1 I2, R3 I1, R5 table); one row per
repository with language and day count (a lookup, which the text does faster, R3 F4 and I10); "15 more · 33"; the
month axis; "Fl 30s" (a word match on "scrape", and one of three configured intervals, R5 F13); the light's
animation, and with it the still editions (nothing in a finished crawl moves, so motion would encode nothing); the
fine print "21 repositories · datum: main · Eastern time" (it describes commit counting, which is gone); the footer
URL and date (the visitor is already on the profile, and the date sits in element 3). "0.1.3 · PyPI" survives as
part of element 3: it becomes "the version that drew this", which is the fact a visitor acts on (R5 F13, R6 I8).

## Exact layout

Sheet sizes stay as in `scripts/sheets/hero.py:38`: desk 1280 × 624 shown at about 870 (× 0.68), phone 720 × 1126
shown at 390 (× 0.54). The type floors are unchanged (`hero.py:73`): desk 19 sheet px (13 on screen), phone 26
(14 on screen). Sizes below are sheet px.

**Desk, 1280 × 624**

- Frame: one 1.5 px hairline, inset 16.
- Left column, x 56 to 430:
  - Name at today's display size, baseline about y 120.
  - Role line in two lines of 21 px small caps, y 190 and 218.
  - Crawl terms: six lines of 19 px small caps at 26 px pitch, y 290 to 420, each line at most 32 characters
    (about 375 px). From the trial, as they would read: `BOOKS.TOSCRAPE.COM` / `A SITE BUILT TO BE SCRAPED` /
    `RUSTMAPPER 0.1.4 · LINKS ONLY` / `ROBOTS.TXT OBEYED` / `1,195 PAGES · 0 ERRORS · 2 MIN` /
    `COMPLETE · 9 OCT 2026`. The figures in this example are the go_go_go trial's; the sheet prints the record's.
- Right panel, chart area x 500 to 1200, baseline y 520, top y 110:
  - 51 columns (depth 0 to 50) at a 13.7 px pitch. Stem 3 px wide; head a 7 px circle. Scale: the peak column
    takes 400 px, so 0.78 px per page in the trial. A 1-page stem is under a pixel, which is why the head is always
    drawn.
  - Axis: hairline at y 520, ticks at depths 0, 10, 20, 30, 40, 50 with 19 px figures at y 548. Caption
    `LINKS FROM THE FRONT PAGE` right-aligned at x 1200, y 576.
  - Peak label: 21 px figures, centred 14 px above the peak head.
  - Tail bracket: hairline at y 492 spanning the first to last column of the equal-count run, text centred above it
    at y 480 (`2 PAGES AT EACH DEPTH`).
  - Deepest label: right-aligned at x 1200, y 450, 19 px, path tail only, with a hairline leader down to the head.
    It must not cross the bracket. If the deepest depth sits inside the bracket, the label goes above the bracket
    text.

**Phone, 720 × 1126**

- Frame: one hairline, inset 12.
- Name at today's phone size, y 40 to 150.
- Role line in two lines of 30 px small caps, y 200 and 236.
- Crawl terms: the same six lines at 26 px, 34 px pitch, y 300 to 470.
- Chart turned so that depth runs down the sheet, which is the phone's long side (R6 I10):
  - Caption `LINKS FROM THE FRONT PAGE` at 26 px, x 40, y 520.
  - Rows for depth 0 to 50 from y 560 to y 1060, a 10 px pitch. Head a 7 px circle (3.8 px on screen); stems run
    right from x 110, with the peak taking 520 px (to x 630).
  - Depth labels at 26 px, right-aligned at x 90, on rows 0, 10, 20, 30, 40, 50 (100 px apart).
  - Peak label at 26 px, at x 640, on the peak row.
  - Tail note at 26 px, x 160, centred on the tail rows (trial: y about 860): `10 TO 50: 2 PAGES EACH`.
  - Deepest label at 26 px, x 160, on the last row: `…/PAGE-50.HTML`.
- Total drawn height is about 1,080, inside 1126.

On both layouts nothing is placed by hand. Every position comes from depth and count, and every label comes from a
key in `stats.crawl`. Two builds from the same record are byte-identical (R3 I11).

**Alt text** (it states the message, R4 I12): "A crawl by rustmapper of books.toscrape.com, a site built to be
scraped: 1,195 pages, most within three links of the front page, the paged list of books running 50 links deep."
The long description, with the full per-depth counts, goes in the caption under the image (R4 F16).

## The page around it, block by block

| Block | Keep, change, cut | What a visitor learns, and why it is text | Evidence |
|---|---|---|---|
| The image | New, as above | What his crawler produces, in one look | above |
| Caption, new, one `<sub>` line under the image | New | How to read the image and where it comes from: "Pages at each distance in links from the front page of books.toscrape.com, as rustmapper 0.1.4 found them on [date]; links only, robots.txt obeyed. The record and the command are in `assets/crawl/`." A complex image needs a short alt text plus a description in the page (R4 F16). It also gives the source note a chart carries (R1 I8) | `stats.crawl` |
| Link line (rustmapper · Scrapy · PyPI · Email) | Keep | The image cannot be clicked, so the first text line under it names the same projects in the same order (R4 I8) | R4 F13 |
| "Ben Russell builds…", Languages, Stack | Keep | Lookups, which text does faster than any drawing (R3 F4) | `stats.json` `repos[].lines`; AUDIT §2 |
| rustmapper heading and facts line | Keep the facts (tests, CI, lines, last commit) | Is it alive, tested, released: the cues hiring readers check (R4 F5, F7) | `repos[].test_functions`, `ci`, `lines`, `last_ns` |
| rustmapper install block | **Change**: print the command that works, which is also the command that made the image | The route in. Today it fails: `pip install rustmapper` installs `rust_sitemap`, not `rustmapper` (R6 F6, R4 F17). Wrong install steps are the most common documentation failure (R4 F9). Either release 0.1.4 with a `rustmapper` entry point (R4 I9) or print `rust_sitemap`. Pass `--seeding-strategy none` explicitly, because the README says the default is `all` (README line 96) while `cli.rs` says `none` | R6 F6; `cli.rs` default `"none"` |
| rustmapper bullets | Keep three; rewrite the seeds bullet with the measured case | The "why", which only 2.7 % of READMEs give (R4 F8). The seeds bullet becomes concrete: on this target the sitemap seeder found nothing (no robots.txt, no sitemap), and Common Crawl's index holds N of its URLs, printed only if the `commoncrawl` seeder line was recorded (R7 F10) | `crawl.seeders`; stderr line `Seeder '…' streamed N URLs` (`bfs_crawler.rs:262`) |
| Scrapy block | Keep; fix "summaries from BART-large-CNN" to Stage 4 only (Stage 3 is extractive) | What the platform does; the claim must match the code (R6 F7, I7) | `stage3_worker.py:194-196`, `stage4/summarization.py:78-79` |
| Also (4 projects) | Keep; correct go_go_go to say what differs (Chrome rendering, SQLite search, TLS-fingerprint impersonation) | Side projects are read as a sign of interest (R4 F5); the Go line hides the main difference today (R6 F9) | go_go_go README |
| 15 more (collapsed) | Keep | The rest of the work, out of the way | R4 I13 |
| Working rules (4 notices) | **Cut** | Each one repeats a bullet above it: breakers (Scrapy bullet 4), raw-first and WAL (Scrapy bullet 2, rustmapper bullet 2), Prometheus (Scrapy bullet 4), "no regex" (the ideal-url-organizer line). If the text above already says it, it goes (R5 I9). Move the one clause the bullets lack, "the question you will want next month is one you cannot ask today", into Scrapy bullet 2 | README notices block vs bullets |
| "Found a mistake? Open an issue" | Keep | The channel for corrections, which keeps a guide true (R2 F11) | R2 [12, 13] |
| Data line (`survey:` block) | **Change** | Drop the sweep-day sentence, since there is no commit chart left for it to qualify. Keep the AI co-author disclosure, because it tells a visitor how much of the code is his (R4 F5). Add "the crawl record: `assets/crawl/`" | `coauthored_total`, `agent_authored` |
| License line | Change one clause | "the images are regenerated from your repositories" becomes "from your own crawl record". It must stay true | — |

## Data: what each mark needs, and whether `build_stats` gathers it

`build_stats.py` gathers none of it today. It reads clones, GitHub, PyPI and releases. Its only crawl-shaped keys
are `sources` (three names from `chart.toml`, `first: null`) and `trial` (Scrapy `exports/run-*.json`, null), and
`assets/log.json` is `"measured": false`, `"source": "computed"`. Nothing in it can be printed as crawl data.

New, in this order:

1. **A committed crawl record**, made by hand on each rustmapper release, never by the weekly CI (R7 I5: a frozen,
   dated record, no repeated load on a third party). `scripts/crawl_record.py` runs, on Ben's machine:
   `rustmapper crawl --start-url https://books.toscrape.com/ --seeding-strategy none --workers 4 --data-dir <tmp>`.
   Then it makes two seed-count runs, `--seeding-strategy sitemap --max-urls 1` and `commoncrawl --max-urls 1`, to
   capture each `Seeder '…' streamed N URLs` line. It writes `assets/crawl/books.toscrape.com/<date>/`:
   - `run.json`: the command verbatim, the tool name, `--version` output, its source (PyPI file name or git sha),
     the start and end times, the stop line verbatim (`GRACEFUL SHUTDOWN: Crawl Complete` from `bfs_crawler.rs:1060`,
     or `Reached max_urls limit…, stopping crawl` from `:977`), and the seeder lines verbatim;
   - `pages.jsonl.gz`: a column projection of `sitemap.jsonl` (`url`, `depth`, `parent_url`, `status_code`,
     `crawled_at`, `response_time_ms`, `content_type`). These are rows the crawler wrote, with columns dropped;
   - `stderr.txt`, untouched.
2. **`scripts/data/crawl.py`**, called from `build_stats.main`, reads the newest record and writes
   `stats.crawl`. Every key is a count or a copy, nothing estimated:
   - `host`, `date`, `tool`, `version`, `source`, `command`, `flags`;
   - `fetched` (rows with `crawled_at` set), `not_fetched` (rows without it), `failed` (status ≥ 400 or none
     after a fetch);
   - `by_depth[]` (fetched rows per `depth`), `by_status{}` (2xx, 3xx, 4xx, 5xx, none);
   - `peak {depth, n}`, `deepest {depth, url}`, `duration_s` (last minus first `crawled_at`);
   - `stop` (`complete`, `max_urls` or `duration`, parsed from the stop line), `seeders {sitemap, commoncrawl}`
     (an integer, or null when no line was recorded).
3. **Validation** (in `data/model.py` and `check.py`): the record exists, has a depth-0 row, `sum(by_depth) ==
   fetched`, and `stop` is one of the three values. If `source` is PyPI, `version` must equal `edition.version`, so
   the image never claims a version other than the one that ran. Every figure on the sheet maps to a `stats.crawl`
   key (R6 I5).
4. **AUDIT.md rows** for each key, before anything prints (R7 I4). Depth is defined as "links from the start URL on
   the path rustmapper first found". It is not guaranteed to be the shortest path, because several workers fetch at
   once and the first discovery wins (`frontier.rs` dedup). The printed figures are the run's, never adjusted.

## Prerequisites (nothing ships before these)

1. **rustmapper must complete this crawl.** At `00a877d` it did not, in this sandbox (above). Reproduce it on Ben's
   machine. If it reproduces, fix `robots.rs` so a 4xx robots.txt means allow all and a 5xx means disallow all
   (RFC 9309 §2.3.1.3 and §2.3.1.4). Make `--duration` stop a crawl that has stalled. Add a test that crawls a local
   site with no robots.txt. This is the angle working as intended: when the picture is the tool's output, it can only
   be drawn when the tool works.
2. **One command name.** Release 0.1.4 from HEAD with a `rustmapper` entry point, or print `rust_sitemap` everywhere
   (R6 F6, R4 I9).
3. **Crawl with the released version**, so that "rustmapper 0.1.4" on the image is exactly what `pip install` gives.
4. **Record the crawler's stop reason in its own words** (step 1 of the data list). Optionally, add a
   `skip_reason` field to `SitemapNode` in rustmapper. Then a "found, not fetched" head can say why (robots or cap)
   from the crawler's own record. A second robots parser in the build would be a different matcher's opinion, so it
   is not used.

If 1 cannot be fixed in time, there is one honest fallback: draw the sheet from go_go_go's record and name go_go_go
in element 3. That changes which project the profile leads with, and Ben has to choose it. It is not a silent swap.

## Checks for the next review round

- Five-second look, at 870 px and at 390 px: a stranger says "a crawl of a site: most pages are near the front,
  some are very deep", and names rustmapper (R3 I4, R4 I1).
- Every number on the sheet has a `stats.crawl` key and an AUDIT row. Grep the SVG for digits and map each one.
- No word on the sheet names the theme. Every label names the data.
- At 390 px every text is at least 14 px on screen, and the depth-10 to depth-50 heads read as a line of separate
  marks, not a smear. Render on a real phone, including the GitHub iOS app with the light edition (R4 I7).
- The command in the install block, pasted into a clean Python 3.13 environment, produces a record whose `by_depth`
  matches the sheet's.

## Risks

1. **The flagship cannot produce the record today**, as far as this sandbox shows: two capped runs at `00a877d`
   fetched nothing beyond robots.txt, and `--duration` did not stop them. Until this is reproduced and fixed, the
   concept cannot ship with rustmapper's name on it.
2. **The shape belongs to the site, not to Ben.** A visitor might take away "a bookstore has deep pagination" and not
   "his crawler is good". The title block (tool, rules, complete) and the caption carry the credit. No book titles,
   prices or other site content appear. If reviewers still read it as being about the bookstore, the concept fails
   the owner's test.
3. **The target is a third party.** It invites scraping in its own words, but it can change or disappear. The record
   is frozen and dated, so the image stays true to its date. A new record is made only on a release.
4. **The picture rarely changes.** The site is static, so each release redraws the same shape unless the crawler's
   behaviour changes. That is the point (it doubles as a regression check), but the owner may want something that
   visibly moves. Nothing here should be animated to fake that.
5. **Depth can differ between runs** by a page or two at the boundary between depths, because of concurrent
   discovery. The sheet prints the record as it is. Smoothing it or "correcting" it to a shortest path is ruled out.
6. **Thin marks at the tail.** On the phone the 41 tail heads sit at 5.4 px on screen. They may merge into a line on
   some displays. That still reads as the narrow path, but it needs the device check.
7. **Not everyone knows why depth matters.** A non-technical visitor may not know that pages many links deep are the
   ones crawlers find late or miss. The caption says what the axis is. The text, not the image, says why it matters.
8. **Two of rustmapper's distinctive features are absent from the image**: the CT and Common Crawl seeders, and the
   governor. On this target they would add nothing true to the drawing (a single host, no sitemap), so they stay in
   the bullets, with the Common Crawl count printed only if it is measured.
9. **A docs disagreement the record exposes**: the README says the default seeding is `all` (line 96), while
   `cli.rs` says `none`. The command must pass the flag explicitly, and one of the two documents should be fixed.

## Sources used in this memo, beyond R1 to R7

- toscrape.com home page and books.toscrape.com banner (purpose statements), read 9 Oct 2026.
- crawler-test.com `robots.txt` (29 `Sitemap:` lines, disallow rules including `/infinite`) and home page (428
  links; sections status_codes, canonical_tags, urls, robots_protocol, redirects, ...), read 9 Oct 2026.
- crt.sh, `%.crawler-test.com`, excluding expired certificates: 2 certificates, 2 names, read 9 Oct 2026. The Common
  Crawl index (`index.commoncrawl.org`) did not answer from this sandbox; the proxy recorded the tunnel closing.
- RFC 9309 §2.3.1.3 and §2.3.1.4, read 9 Oct 2026.
- Google Search Central, "Pagination, incremental page loading, and their impact on Google Search", updated
  10 Dec 2025.
- Screaming Frog, SEO Spider user guide, "Tabs" (Crawl Depth definition), read 9 Oct 2026.
- Rust-sitemap at `00a877d`: `src/state.rs:131-150`, `src/robots.rs:18-24`, `src/frontier.rs:699-828` and
  `830-900`, `src/bfs_crawler.rs:195-280, 977, 1060, 1186-1210, 1513-1600`, `src/cli.rs:14-90`, `README.md:96`;
  git log for #50 and #52 (7 Oct 2026).
- go_go_go at `4078b55`: `crawl --help`; the trial record.
- This repository: `scripts/build_stats.py` (keys `trial`, `sources`), `scripts/sheets/hero.py:38, 73`,
  `assets/stats.json`, `assets/log.json`, `README.md`, `docs/crit/round5/DECISIONS.md`.
