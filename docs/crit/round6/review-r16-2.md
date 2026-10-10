# Review round 16, reviewer 2: the data engineer who wants a definition for every number

10 Oct 2026. I looked at every PNG in `scratchpad/r6/build/round-15/`: the desk sheet at 870 and 846 (day and night),
the mid sheet at 746 (day and night), the phone sheet at 390 and 308 (day and night), and the README at 1,280 (two
screens), 390 (seven) and 360 (seven). I read `README.md`, `SPEC.md`, `LOG.md` round 15, the three round 15 reviews and
the earlier data reviews (r02-3, r07-2, r11-3, r12-2). I checked every figure against `assets/stats.json`,
`docs/data/AUDIT.md` §7, the 0.1.3 sdist (`scratchpad/r6/sdist013/rustmapper-0.1.3`) and the history clones. I also
re-ran 0.1.3's `export-sitemap` on the data directories round 15's https probes left behind, and ran Scrapy's own
`Stage3Worker.run()` twice on two near-identical pages (`scratchpad/r16-2/`). Nothing below repeats a fixed finding.

Verdict: **not yet. 7 / 10.**

Every figure on the page has a key and a row, and every one I checked holds (table below). The image is right in what
it does: it is the way through his main tool, in order, with the catches where they bite, and nothing in it has a size
to misread. What stops me shipping is not a wrong number. It is the meaning of the data the page hands people:

1. **A blank row in `sitemap.jsonl` means four things, and the page defines two.** In round 15's own stall run, 6 of
   the 12 rows are links 0.1.3 never asked for (`p6` to `p10`, and the disallowed `secret.html`). They have
   `status_code` and `crawled_at` null, the same blank the fold says means "errors, timeouts and non-HTML 200s". The
   image's done rule ("done when `Received work item` lines stop for 60 s") is met by that stalled crawl, and the log
   says "Exported 12 nodes". Nothing on the page tells you half the file was never fetched, or how to find out.
2. **0.1.3's `sitemap.xml` lists pages `robots.txt` disallows.** On round 15's `robots_late` data, `export-sitemap`
   wrote 21 URLs, and 10 of them are the `secret*.html` pages the site disallowed. Google's Sitemaps report names that
   as an error ("Sitemap contains urls which are blocked by robots.txt") [1]. The fold's sitemap item doesn't say so.
3. **Scrapy's "near-duplicate pages by MinHash" does not hold in the worker `start.py` runs.** The MinHash index is
   built fresh for each batch, and a page it skips is not marked done, so the continuous loop summarizes it on the next
   pass. I ran the real `Stage3Worker.run()` twice: pass 1 summarized `a` and skipped `b`; pass 2 summarized `b`. The
   gate that prints "deduplicated" in the `pick` sentence checks only that the string `MinHashLSH` is in the file.

## Does it meet the owner's goal?

- **Every element has a purpose.** Yes for the image: each row answers how in, what happens, what goes wrong, how out,
  where it goes. On the page, yes, with the three meanings above to fix.
- **It teaches something true and useful about his actual projects.** Mostly. It teaches how to run rustmapper 0.1.3
  and what it does to a site. But the most useful thing a stranger can learn about the output, which rows are real
  pages, is missing, and one Scrapy claim is false in the running pipeline.
- **Nothing chases a reason.** Yes. The gap under the loop says "it doesn't end by itself" and is backed by the
  150 s probe. The dotted line is the only mark with a meaning to learn, and the words inside it say what it means.
- **Nothing announces the theme.** Yes. No theme word anywhere.
- **Reads on a phone.** Yes. At 390 and 308 the sheet is one screen, and the smallest words are 13 px or more.

## Every figure, checked

| Where | Printed | Key / source | Re-measured | Holds |
|---|---|---|---|---|
| image | 0.1.3 · 8 NOV 2025 | `edition.version`, `edition.date` | PyPI upload 2025-11-08T19:52:41 | yes |
| image | up to 20 pages at a time from each host | F1 `{field:max_inflight}` | `sdist:src/state.rs:285` `max_inflight: 20`, checked at `frontier.rs:655` | yes |
| image | 60 s | H1 `{quiet}` = 30 + 20 + 4 + 1, rounded up | AUDIT §7 H1; probe `quiet_slow_page` | yes |
| image | sorted 21 ways | `self.methods` 21 keys | AUDIT §7 R15 | yes |
| facts | `32c2651`, 176 test functions, CI passed 7 Oct 2026: tests, rustfmt, 16k lines | `repos[Rust-sitemap]` head, `test_functions`, `ci`, `lines` 16,390 | | yes |
| facts | 45 of its 146; 1 of his own 101 | `others` Claude 45, `all_hands` 146, `coauthored.agent` 1, `commits` 101 | `git log` on the history clone: 97 + 4 + 45 = 146, 31 merges, one `Co-Authored-By: Claude Sonnet 5` | yes |
| install | CPython 3.13, Apple silicon; 3 min, cold, 4-core | `edition.wheels`; `runcheck` install | 168.2 to 174.3 s, empty `CARGO_HOME`, 4 CPUs | yes |
| L1 | 256 at a time; `--workers 1` | `{arg:workers}`; probe `workers_cap` | `main.rs:262` `Semaphore::new(config.max_workers)`; the log's own "256 concurrent requests" | yes |
| L7 | `RustSitemapCrawler/1.0` | probe `ua_seen` | `cli.rs` default | yes |
| fold X1 | 50,000 URLs per file | sitemaps.org; main's `DEFAULT_MAX_URLS_PER_SITEMAP` | Google's Sitemaps report also fails a file over 50,000 [1] | yes, but see must-fix 2 |
| Scrapy facts | `96e7a1a`, 1,920 (all but 41), CI 8 Oct 2026, gates, MIT, 69k | `repos[Scrapy]`; `ci_selection` 16 + 25 | 69,036 lines | yes |
| Scrapy facts | 71 of its 499; 30 of his own 420 | jules 49 + Claude 22; dependabot 8 in the 499; `coauthored.agent` 30 | | yes |
| Scrapy | five sentences, 50,000 characters, 5 s, 4 per host, `Python/3.11 aiohttp/3.13.1`, `localhost:3000` | `[[figures]]` rows | | yes |
| Scrapy | near-duplicate pages by MinHash | `[[figures]]` `MinHashLSH` | see must-fix 3 | **no, in the running worker** |
| Also | 21 ways; 15 more | `self.methods`; 22 − profile − 2 − 4 | | yes |
| Languages | Python, Rust; Swift, JavaScript, TypeScript, C, Go | `main_language` counts 3, 2 (110,917 lines), 2 (37,021), 1 (151,872), 1 | | yes |
| rule 1 | 5 URLs, 60 s, Oct 2026 | `099dd6c` 2026-10-08, his | `git log -S_host_breakers` | yes |
| rule 2 | Oct 2025 | `52dcbd8` 2025-10-04 | | yes |
| rule 3 | 6 days, 5 days | `67446a4` 25 Sep, `d571e6e` 1 Oct, `e8cbe15` 6 Oct 2025 | | yes; "was up" measures a commit (r11-3, still open, the owner's call) |
| data line | 0.1.3, 10 Oct 2026, Linux x86_64 | `runcheck.rustmapper` | | yes |

## What I measured this round

**The blank rows (must-fix 1).** `rc15/work/d-robots_stall/sitemap.jsonl`, written by 0.1.3 after one Ctrl-C:

```
https://localhost/            200   crawled_at 1791625494
https://localhost/p1.html … p5.html   200
https://localhost/p6.html … p10.html  null  crawled_at null
https://localhost/secret.html         null  crawled_at null
```

12 rows, 6 fetched. The log printed six `Received work item` lines, one `blocked by robots.txt`, then nothing until
the SIGINT, and then "Exported 12 nodes to JSONL". So the crawl met the image's done rule while half its rows had never
been asked for. Each row is written as one line of `serde_json::to_string`, so the blank is the literal
`"crawled_at":null` with no space (`grep -c` gives 6 on this file). Codd asked for two kinds of null in 1990, "missing
but applicable" and "missing but inapplicable", because one null that means several things can't be read [7]. Data
specs make you list what a missing value means [8]. Here one null means: error, timeout, non-HTML 200, disallowed, or
never reached. The first three are in the fold; the last two are not.

This is the common case, not an edge case. About 96 % of hosts and 95.6 % of mobile home pages are served over https
[5], and about 84 % of sites answer `robots.txt` with a 200, three quarters of them with a `*` group [4]. Any such site
that links one disallowed URL can stall its host in 0.1.3.

**The disallowed pages in `sitemap.xml` (must-fix 2).** I copied round 15's data directories and ran the installed
0.1.3 binary (`r6/runcheck/work/v/bin/rust_sitemap`, `--version` 0.1.3):

- `export-sitemap --data-dir late`: "Exported 21 URLs". 10 of them are `secret1.html` to `secret10.html`, which that
  site's `robots.txt` disallows. They were fetched before `robots.txt` arrived (L4) and kept their 200.
- `export-sitemap --data-dir stall`: 6 URLs of the site's 11 allowed pages, with no warning.

`run_export_sitemap_command` keeps `node.status_code == Some(200)` and nothing else; there is no robots check in it
(`sdist:src/main.rs`). Google's Sitemaps report lists "Sitemap contains urls which are blocked by robots.txt" as an
error [1], and its Page indexing help names a sitemap of blocked URLs as a cause of error spikes [2]. Google also says
`robots.txt` is mainly there to keep a crawler off a site's load, not to hide pages [3], which is why a stranger
pointing rustmapper at his own site will care that the file he submits lists the pages he fenced off.

**Scrapy's near-duplicates (must-fix 3).** `src/stage3/stage3_worker.py`: `_run_traced` calls
`self._deduplicate_documents(batch)` for each batch, and that method builds `MinHashLSH(threshold=…, num_perm=128)`
fresh every call. A skipped page is not written to `stage3_summaries`, so `_processed_hashes()` doesn't hold it, and
it is pending again on the next `run()`. `run_stage3_worker` runs `run()` in `run_drain_loop`, idle 30 s, until
shutdown, and that is the `stage3-worker` command in `docker-compose.yml`. datasketch's docs say an index without a
shared `basename` and storage starts empty [6]. I ran the clone's real worker (only Delta, Postgres, tracing and config
stubbed; `scratchpad/r16-2/dedup_sim.py`) on two pages that differ in their last two words:

```
pass 1: wrote 1; summaries for ['a']
pass 2: wrote 1; summaries for ['a', 'b']
pass 3: wrote 0; summaries for ['a', 'b']
```

So inside one batch of one pass, MinHash skips a near-duplicate; across passes, both get summarized. A crawler's
near-duplicate filter is worth naming exactly because it is global over the crawl, as in Google's (Manku, Jain and Das
Sarma, WWW 2007 [9]). One that forgets between passes is not that, and a screener who opens the file will see it. (I
also checked the 0.3 threshold the page doesn't print: across 2,534 pairs of different documents in the clones, the
word-set Jaccard of the first 1,000 words never reached 0.3; the median was 0.04. So the threshold is not the
problem.)

## Every element of the image

| Element | What a visitor learns | Verdict | Why |
|---|---|---|---|
| Name, serif | whose page this is | keep | |
| Role line, two caps lines | he builds crawl and data infrastructure in Python and Rust | keep | the route below proves it |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | what the tool is and what file it makes | keep | true: a node is written when a link is found (`state.rs` "A new node was discovered…"), fetched or not. Must-fix 1 makes "every URL it finds" readable |
| Start bar, `pip install rustmapper`, "0.1.3 · 8 NOV 2025" | the line that gets it, and that the release is 11 months old | keep | `edition` holds |
| Ring: `rust_sitemap crawl` starts from your URL; by default also sitemaps, certificate logs, Common Crawl | where URLs come from, and that by default it asks third parties | keep | 0.1.3 `cli.rs` `default_value = "all"` |
| Ring: up to 20 pages at a time from each host; queues links to your site, subdomains, parent domain | what a site feels, and the scope | keep | `max_inflight: 20`; `is_same_domain` takes subdomains and every parent (from `a.b.site` it takes `b.site` and `site`), so "parent domain" is fair for the usual `www.` start |
| Loop line with the up arrow | these rows repeat for every page | keep | a crawler is a loop, and only the drawing shows where it closes |
| Dotted line, H0 "on https, a disallowed link stalls its host" | the stall | **change** | "stalls its host" can read as "slows the server down", which is the opposite of the fact. "stalls its queue" is the same length and names the thing that stops (must-fix 4) |
| Dotted line, H1 "0.1.3 never exits by itself; done when `Received work item` lines stop for 60 s" | when to stop it | keep | 60 s defined and probed. After a stall it reads a part crawl as done; must-fix 1 puts the check where the reader types, because the phone sheet has no room for another row (1,121 of 1,122 units) |
| Gap in the track under the loop | the run doesn't end on its own | keep | `ends_by_itself` false at 150 s; `select!` `else` never fires while `work_rx` is open |
| Ring: Ctrl-C once; a second press before `Saved to` quits without the file | how to stop without losing the file | keep | probes `crawl_ctrl_c`, `second_ctrl_c` |
| End bar, `data/sitemap.jsonl`, fields `url, depth, status_code, title, …` | the file and its real field names | keep | `SitemapNode`; the names are right, what a blank means is must-fix 1 |
| Arrow, "sorted 21 ways by ideal-url-organizer" | his projects feed each other | keep | 21 keys; reader fields ⊆ writer fields |
| Night editions | the same at night | keep | |
| Phone editions (390, 308) | the same in one column | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Picture and alt | the route, in 25 words for a screen reader | keep | no figures in the alt |
| Link line | where to go | keep | |
| Builds / Languages / Stack | who he is, his languages, his tools | keep | the languages order recomputed above |
| `pick` sentence | which tool for which job | **change** | "deduplicated" is gated on the string `MinHashLSH`, which proves the word is there, not that it works (must-fix 3) |
| rustmapper facts line | it's tested, alive, how big, who wrote it | keep | every number holds |
| Wheel note | will pip just work, and the cost if not | keep | measured cold, three runs |
| "Before you run 0.1.3:" (L1, L7, L4, L6, seeds, `www.`) | what it does to a site | keep | all hold, all probed |
| Fold: JavaScript, redirects | what the file can't see | keep | |
| Fold: X2, the blank `status_code` | what a blank row means | **change** | it leaves out links never fetched (must-fix 1) |
| Fold: X1, `sitemap.xml` | what the export keeps | **change** | it leaves out disallowed pages it fetched (must-fix 2) |
| Code block | the commands, and when to stop | **change** | add the one line that says how much of the file was never fetched (must-fix 1) |
| Scrapy sentence and facts | what it is, tested, alive | keep | |
| Scrapy bullet 1 (Delta Lake) | how raw data is kept | keep | |
| Scrapy bullet 2 (dedup, summaries) | what happens to a page | **change** | the MinHash clause is false across passes (must-fix 3); the summary and stage 4 parts hold |
| Scrapy bullet 3 (alerts, kill switch) | how it is watched and stopped | keep | |
| Scrapy run paragraph, cautions, code block, Grafana | how to start it and what it does to a site | keep | |
| Also | four more tools | keep | all `[[figures]]` hold |
| 15 more | the rest | keep | the count is computed |
| Working rules | how he works, each with dated proof | keep | dates recomputed above; "was up" left to the owner as r11-3 did |
| Found a mistake? | the page can be corrected | keep | |
| Data line | how and when the drawing was checked | keep | |
| License line | terms | keep | Noted, not ranked: rustmapper's PyPI metadata says `License-Expression: MIT` and `license-files = ["LICENSE"]`, but neither the sdist nor the repository has a LICENSE file. The page prints no license for the tool it tells you to install. It's on the owner's list (LICENSE-FLAGSHIP) |

## Must fix, ranked

1. **Say what a blank row is, and give the check** (`chart.toml` X2 `text` and anchors; `render_readme.stop_lines`
   for the code block; `scripts/runcheck.py` `robots_stall`; AUDIT §7 X2 row; one test; about 30 lines).
   - X2 (25 words, the README-CAUTIONS cap): "Only HTML pages that answer 200, redirected or not, get a `status_code`.
     Errors, timeouts, non-HTML 200s and links never fetched are left blank, `crawled_at` too."
   - Code block, after the Ctrl-C comment and before the export: `# rows never fetched or failed` and
     `grep -c '"crawled_at":null' \` / `  data/sitemap.jsonl` (both lines under 32 columns). Print it only while the
     anchors hold: `pub crawled_at: Option<` in `src/state.rs` in both trees, and `serde_json::to_string(&node)` in
     `export_to_jsonl`.
   - `robots_stall` also asserts that the rows for `p6`…`p10` and `secret.html` have `crawled_at` null (6 of 12 today)
     and records the `grep -c` count, so the line is checked the way the others are.
   - Why: the image's done rule is met by a stalled crawl, and on https, which is where nearly every site is [5], the
     stall is the normal risk. This is the one number a user needs after Ctrl-C, and the file already holds it.

2. **Say that 0.1.3's `sitemap.xml` keeps disallowed pages** (`chart.toml` X1 `text` and anchors; a new probe step;
   AUDIT §7 X1; one test; about 20 lines).
   - X1 (23 words): "Its `sitemap.xml` is every row with `status_code` 200, in one file (the format allows 50,000):
     `noindex`, canonicalized and disallowed pages it fetched included."
   - Anchor: in `run_export_sitemap_command`, `node.status_code == Some(200)` (as now) and `absent = "robots"`.
   - Probe `sitemap_keeps_disallowed`: `export-sitemap` on the `robots_late` data directory; pass if the 10
     `secret*.html` are in `<loc>` (21 today). An empty wording with `fails = [...]` retires it when a release filters
     them.
   - Why: Google's own report fails a sitemap like that [1, 2], and the reader most likely to run rustmapper is mapping
     his own site.

3. **Make Scrapy's dedup claim match the running worker** (README Scrapy bullet 2, hand-typed; `chart.toml` the
   `pick` row "deduplicated" and its `[[figures]]` anchor; one test; about 10 lines).
   - Bullet 2: "Repeat URLs are dropped by their hash. In stage 3 a page's summary is its first five sentences;
     documents over 50,000 characters go to stage 4, …" (the rest unchanged). The MinHash clause goes.
   - The `pick` row "deduplicated" moves off the `MinHashLSH` literal to the URL dedup it really rests on:
     `src/core/constants.py` `REDIS_KEY_SEEN_URLS = "seen:urls"` and `src/pipelines.py` `def _canonical_queue_row`.
   - Owner, in Scrapy: persist the index (datasketch `storage_config` on the Redis it already runs, with a fixed
     `basename` [6]), or write a skipped page's hash to `stage3_summaries` as a duplicate. Then add a test that runs
     `run()` twice and expects one summary, and the clause can come back with that test as its anchor.
   - Why: I ran his own worker; pass 2 summarized the page pass 1 skipped. A presence anchor passed while the
     behaviour failed. That is the gap every other claim on this page closes with a probe or a test.

4. **H0: "stalls its queue", not "stalls its host"** (`chart.toml` H0 `text`; the PURPOSE row; alt unchanged; one
   test pins the string; about 5 lines).
   - "on https, a disallowed link stalls its queue" is 44 characters, one more than today, and still one phone line at
     308 (HERO-COLUMN-PX decides; if it fails, "on https, a disallowed link stalls the queue").
   - Why: "host" is the server in plain speech, and "stalls its host" reads as harm to the site. The queue is the thing
     F1 just said it fills, and L6 says the same in the README ("stalls that host's crawl").

5. **Bring `BREAKS` up to date** (`scripts/sheets/route.py:126-131`; one line).
   - "Order is position; the loop is a line" still lists "and the log" among the rows that repeat. W1 isn't drawn
     since round 15. Change it to "(fetch, at most 20 at once from one host, the robots.txt stall, and the crawl that
     never exits)".
   - Why: BREAKS is the page's record of why each mark is there; a reason for a mark that isn't drawn is the kind of
     thing T-BREAKS exists to stop.

## Sources

The web search budget for this turn ran out on my first query, so every source below was fetched directly by its
URL. None of them is in `scratchpad/r6/cited-urls.txt`.

1. Google Search Console Help, "Sitemaps report": "Sitemap contains urls which are blocked by robots.txt"; more than
   50,000 URLs is a parsing error. https://support.google.com/webmasters/answer/7451001
2. Google Search Console Help, "Page indexing report": a submitted sitemap that includes robots.txt-blocked URLs as a
   cause of error spikes; "URL blocked by robots.txt". https://support.google.com/webmasters/answer/7440203
3. Google Search Central, "Introduction to robots.txt": "used mainly to avoid overloading your site with requests";
   "not a mechanism for keeping a web page out of Google".
   https://developers.google.com/search/docs/crawling-indexing/robots/intro
4. HTTP Archive, Web Almanac 2024, SEO chapter: robots.txt answered 200 on 83.5 % (desktop) and 83.9 % (mobile), 404 on
   about 14 %, 5xx on 0.1 %; `*` user agent in 76.6 % and 76.9 % of files. https://almanac.httparchive.org/en/2024/seo
5. HTTP Archive, Web Almanac 2024, Security chapter: about 98 % of mobile requests over https; 95.6 % of mobile home
   pages; about 96 % of hosts. https://almanac.httparchive.org/en/2024/security
6. datasketch documentation, "MinHash LSH": the threshold is fixed when the index is made; without a shared `basename`
   and storage a new index doesn't reach the old data. https://ekzhu.com/datasketch/lsh.html
7. E. F. Codd, *The Relational Model for Database Management, Version 2* (1990), A-marks ("missing but applicable")
   and I-marks ("missing but inapplicable"), as summarized in "Null (SQL)". https://en.wikipedia.org/wiki/Null_(SQL)
8. Frictionless Data, Table Schema, `missingValues`: a schema lists what counts as missing.
   https://specs.frictionlessdata.io/table-schema/
9. G. S. Manku, A. Jain, A. Das Sarma, "Detecting near-duplicates for web crawling", WWW 2007, pp. 141-150 (citation
   only; the page holds no abstract text). https://research.google/pubs/detecting-near-duplicates-for-web-crawling/

Clones and runs: `sdist:src/state.rs:285`, `src/frontier.rs:655-690`, `src/url_utils.rs:81-91`,
`src/bfs_crawler.rs:420-555, 1001-1040`, `src/main.rs` `run_export_sitemap_command`, `PKG-INFO`; Rust-sitemap.git
`git log` (146 commits, 31 merges); Scrapy.git `git log -S` for the four rule anchors; Scrapy
`src/stage3/stage3_worker.py:45-200, 258-270`, `src/utils/graceful_shutdown.py:219-250`, `config.yml:220-227`,
`docker-compose.yml` `stage3-worker`; `scratchpad/r6/rc15/work/d-robots_{stall,late}`; my runs in
`scratchpad/r16-2/` (`late.xml` 21 URLs, `stall.xml` 6, `dedup_sim.py`).
