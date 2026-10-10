# Review round 12, reviewer 3: a developer choosing between rustmapper and Scrapy

10 Oct 2026. I came to this profile because I need either a sitemap for a site or a crawl platform, and I want to
know which of his two tools to try. I looked at every PNG in `scratchpad/r6/build/round-11/`: the desk sheet at 870
(day and night), the phone sheet at 390 and 308 (day and night), the desk page (two screens) and the phone page at
390 (six screens). I read `README.md`, `SPEC.md`, `LOG.md` through round 11, all the round 11 reviews and
`review-r12-2.md`. I don't repeat anything already fixed, or anything review r12-2 already raises (DESIGN.md, the C1
colon, "once"/"when", Scrapy bullet 2, the fold label, rule 3's title).

I checked the figures against `assets/stats.json`, the 0.1.3 sdist (`scratchpad/r6/sdist013`) and the clones. I also
ran three new things: the installed 0.1.3 binary against a local site that redirects, the same site through
go_go_go (built from its clone today), and the export path Scrapy writes to.

Verdict: **not yet. 8 / 10.** The image is right, and I would not move a mark. The "pick" sentence under it is the
most useful sentence on the page for someone like me. But what I came for is a correct list of URLs, and **the page
says nothing about redirects, which is where 0.1.3 gets that list wrong.** One sentence on the page is false because of
it. The Scrapy half also never says where the pages end up.

## The first question: does it meet the owner's goal?

- **A deep purpose for the map.** Yes. It shows the one thing a list can't: the loop a URL goes round, and where in
  that loop the 0.1.3 trap is. Install, start, loop, trap, stop, file, the next tool. Nothing in it has a size.
- **Teaches something true and useful about his projects.** The image, yes: every row holds against the code and the
  probes. The page, nearly. X2 says "Only HTML pages that answer 200 get a `status_code`". I ran 0.1.3: a link that
  answers **301** is written as `status_code: 200`, under the old address, with the target's title, and it goes into
  `sitemap.xml` (must-fix 1). For someone who wants a sitemap, how a crawler handles redirects is the first thing to
  know. The list covers concurrency, robots, seeds, scope, JavaScript, file size and status codes, and says nothing
  about redirects.
- **Nothing chases a reason.** True. Every block answers a question I had. The one gap is the reverse: the Scrapy
  half has no arrival, so I can start it but I don't know what it produced or where (must-fix 2).
- **Nothing announces the theme.** True. A magenta line, a dotted box, a start bar and an end bar. I read them as
  "follow this" and "watch out" before I thought of charts.
- **Reads on a phone.** Yes. At 390 and at 308 the image fits one screen, day and night. The labels are 13.3 px or
  larger, and no flag splits in the prose.

**Would I try it?** For a quick list of URLs from a site I own: yes, rustmapper, with `--workers 1` and seeding off,
because the list told me to. For pages kept and summarized: Scrapy, if I have Docker. The page got me to that choice
in about a minute. That is the goal. The two fixes below are about whether the result I take home is the one the page
describes.

## What I ran

**0.1.3 against redirects.** The binary is `scratchpad/r6/runcheck/work/v/bin/rust_sitemap` (`--version`: 0.1.3).
I ran it on a local site (`scratchpad/r12-3/srv.py`) with `--seeding-strategy none --timeout 3`, sent one SIGINT
after 25 s, then ran `export-sitemap`. The site:

- `/` links to `/old`, `/new.html`, `/dir` and `/canon.html`
- `/old` answers 301 to `/new.html`
- `/dir` answers 301 to `/dir/`, the way Apache's `DirectorySlash On` (the default) does [S5]. `/dir/` links to
  `child.html`
- `/canon.html` has `<link rel="canonical" href="/new.html">` and `<meta name="robots" content="noindex">`

What the server logged and what the files hold:

| URL | Server | `sitemap.jsonl` | `sitemap.xml` |
|---|---|---|---|
| `/old` | 301 → `/new.html` | `url: /old`, `status_code: 200`, `title: "New"` | listed |
| `/new.html` | 200 | `status_code: 200`, `title: "New"` | listed (the same page twice) |
| `/dir` | 301 → `/dir/` | `url: /dir`, `status_code: 200`, `title: "Dir"` | listed under `/dir` |
| `/dir/child.html` | never asked for | no row | missing |
| `/child.html` | 404 (asked for: `child.html` resolved against `/dir`, not `/dir/`) | `status_code: null` | not listed |
| `/canon.html` | 200, noindex, canonical elsewhere | `status_code: 200` | listed |

So in 0.1.3:

1. A URL that redirects is kept under the address it asked for, with the target's status and title. RFC 3986 says
   the base after a redirect is "the last URI used" [S1]. reqwest follows up to 10 redirects by default [S2], and
   gives the final address as `Response::url()` [S3]. Neither tree calls it (`grep '\.url()'`: no hits in `src/` at
   0.1.3 or at `32c2651`).
2. Relative links on the target are resolved against the old address: `effective_base = base_href … unwrap_or(&job.url)`
   (`bfs_crawler.rs:593` at HEAD; the same `effective_base` at 0.1.3, `:343`). Browsers use the document's own URL,
   which is the final one [S8, S9]. On any site that redirects `/docs` to `/docs/` and uses relative links (Sphinx
   output does), every page under that folder is fetched at the wrong address, gets a 404, and is lost.
3. `sitemap.xml` keeps redirecting and `noindex` URLs. Google's own report has a status for this, "Page with
   redirect: … this URL will not be indexed" [S10]. It asks for "the URLs … that you want to see in Google's search
   results" [S4]. Screaming Frog's generator leaves out 3xx, noindex and canonicalised pages by default [S7]. HEAD's
   `orchestration/export.rs` now skips canonicalised pages (#46), but not redirects or noindex.

Points 1 and 2 hold in both trees by the code, and I ran 0.1.3. They are true of main too, so they don't retire
when 0.1.4 ships unless the owner fixes them.

**go_go_go on the same site** (`go build ./cmd/gogogoscraper` at `4078b55`, `crawl --seeding-strategy none
--timeout 3`): it **exited by itself in 1 s** (exit 0, "Crawl completed!"), asked for `/robots.txt` over plain http,
and wrote `status_code: 404` for `/child.html`. It has the same two redirect faults (`/old` written as 200, and
`child.html` resolved against `/dir`). That goes in the notes, not the must-fixes, but it matters for my choice:
three of the seven 0.1.3 cautions don't apply to his Go crawler.

**Where Scrapy's pages go.** `docker-compose.yml` sets `DELTA_LAKE_PATH=/data/delta` on `scraper` and every stage
worker, and mounts `./data:/data`. `src/utils/delta.py` reads `DELTA_LAKE_PATH` first, and `get_table_path` is
`base_path / table_name`. So the pages land in `Scraping_project/data/delta/<table>/` on the host.
`docs/guides/DATA_USAGE.md` (in the repo, current) lists the tables and shows how to read them, and `cli.py export`
writes CSV, JSON or Parquet (`--format`, default csv).

## Figures checked

| Printed | Source | Holds |
|---|---|---|
| `pip install rustmapper` · 0.1.3 · 8 Nov 2025 | `edition.version`, `.date` 2025-11-08, `.scripts` `["rust_sitemap"]` | yes |
| `rust_sitemap crawl` | `edition.scripts[0]`; sdist `cli.rs` `#[command(name = "rust_sitemap")]` | yes |
| by default also from sitemaps, certificate logs and Common Crawl | sdist `cli.rs` `seeding_strategy` `default_value = "all"` | yes |
| up to 20 pages at a time from each host | sdist `state.rs:285` `max_inflight: 20` | yes |
| up to 256 at a time across all hosts | sdist `cli.rs:32` `default_value = "256"`, `bfs_crawler.rs:63` | yes |
| lines stop for 60 s | 30 permit + 20 timeout + 4 + 1, rounded up (LOG r11) | yes as defined |
| `Saved to:` | sdist `main.rs:539` | yes |
| fields `url, depth, status_code, title` | my run's rows | yes |
| "Only HTML pages that answer 200 get a `status_code`" | my run: `/old` and `/dir` answered 301, rows say 200 | **no** (must-fix 1) |
| "one `sitemap.xml` however many pages"; 50,000 | sdist `run_export_sitemap_command` `SitemapWriter::new`; [S4] "50MB … or 50,000 URLs" | yes |
| 176 test functions · CI passed 7 Oct 2026 · 16k lines of Rust · `32c2651` | `repos[Rust-sitemap]` 176, `ci` success 2026-10-07, `lines.Rust` 16,390, `head_sha` | yes |
| 1,920 test functions · CI 8 Oct 2026 · MIT · 69k · `96e7a1a` | `repos[Scrapy]` 1,920, success 2026-10-08, `license` MIT, 69,036 | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | `others` Claude 45, `all_hands` 146; jules 49 + Claude 22, 499; `coauthored.agent` 1, 30 | yes |
| 15 more | 21 − 2 − 4 | yes |
| Prebuilt for Apple silicon on CPython 3.13 | `edition.wheels` `cp313-cp313-macosx_11_0_arm64` | yes |

## Every element of the image

| Element | What I learn as someone choosing | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose tools these are | keep | |
| Role line, two caps lines | he builds crawlers, in Python and Rust | keep | the route under it is the proof |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | what it does, before any detail | keep | true in my run: 6 URLs, 6 rows |
| Start bar | where to begin | keep | |
| `pip install rustmapper` · 0.1.3 · 8 NOV 2025 | it's on PyPI, and the release is 11 months old | keep | the date tells me before the list does that this is an early release |
| S1 `rust_sitemap crawl` … sitemaps, certificate logs, Common Crawl | the command, and that it asks third parties by default | keep | |
| F1 20 per host; links to your site, subdomains, parent domain | how hard it hits one host, and how far it reaches | keep | |
| W1 logged, then saved to redb, in batches | a kill doesn't lose the crawl | keep | |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| H1 dotted box | 0.1.3 won't stop, and how I know it's done | keep | wording is r12-2's must-fix 3 |
| C1 Ctrl-C once | how to stop without losing the file | keep | wording is r12-2's must-fix 2 |
| End bar + `data/sitemap.jsonl` + fields | what I get and where | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | the output is used by another of his tools | keep | |
| Whole image links to Rust-sitemap | one tap to the code | keep | |
| Alt text | the same route in words | keep | |
| Night and phone editions | the same | keep | contrast holds by eye at 308 |

Nothing in the image needs to change for redirects. The image draws the route, and the redirect faults belong in the
list, where the image's own rows send you for limits.

## Every block of the page

| Block | What I learn | Verdict | Why |
|---|---|---|---|
| Link line | where the code and the package are | keep | |
| "Ben Russell builds …", Languages, Stack | who he is, in three lines | keep | |
| Pick sentence (rustmapper vs Scrapy) | which one to try | keep | it decides the visit; one binary vs Docker is the right split |
| rustmapper facts line | alive, tested, size | keep | no licence where Scrapy's says MIT (note 3) |
| Wheel note | whether `pip` will just work | keep | |
| "Before you run 0.1.3:" L1–L5 | what it does to a server, and the flag for each | keep | the most useful list on the page for me |
| X1 one `sitemap.xml` | what the sitemap file is | **change** | say what goes into it (must-fix 1) |
| X2 status codes | what a blank row means | **change** | false for redirects (must-fix 1) |
| (missing) redirects | | **add** | must-fix 1 |
| rustmapper code block | how to run, stop, export | keep | |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy bullets | the design | keep (bullet 2 per r12-2) | |
| Scrapy run sentence + code block | what `start.py` starts, needs and loads | keep | |
| Grafana / spider-name note | where to look while it runs | **change** | add where the pages land (must-fix 2) |
| Also: ideal-url-organizer, go_go_go, rust_llm_logger, Ai_code_detector | his other tools | keep | go_go_go: see note 1 |
| 15 more (fold) | the rest | keep (label per r12-2) | |
| Working rules 1–3 | how he works, with the commit | keep | |
| Found a mistake? | the page can be corrected | keep | I'd use it for exactly this review's finding |
| Data line | which release was run, and how; who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **Say what 0.1.3 does with redirects, and make X2 true** (`chart.toml` X1 and X2 `text`, a new entry X3 after X2;
   `scripts/runcheck.py` a probe `redirect_kept`; a fixture `tests/fixtures/redirect-site/`; `render_readme.py`
   `LIST_MAX_ITEMS` 7 → 8; AUDIT §7 rows. About 80 lines and three tests. Phone cost about 4 lines, roughly 190 CSS px
   at 390.)
   - Why: X2 says a page gets a `status_code` only if it answers 200. A 301 is written as 200, so the sentence is
     false on sites with redirects, which is most sites. For someone who came for a sitemap, this is the fact that
     decides whether the file can go to a search engine as it is.
   - X2, new text (24 words): "Only an HTML 200, even after a redirect, gets a `status_code`. An error, a timeout
     or a non-HTML 200 is left blank, `crawled_at` too." If FIGURES or the word cap asks for "never retried" back,
     keep it and let X3 carry the redirect alone, with X2 unchanged except "pages that answer 200" → "pages that end
     in a 200".
   - X3, new item (24 words): "After a redirect it keeps the old address and reads the page's links from it: if
     `/docs` redirects to `/docs/`, `a.html` is fetched as `/a.html`."
     - Anchors, scope "both": release `src/bfs_crawler.rs` `effective_base` `unwrap_or(&job.url)` (or the 0.1.3
       spelling at `:343`), and `absent = ".url()"` in `src/bfs_crawler.rs` and `src/network.rs`. HEAD the same
       (`bfs_crawler.rs:593`). Retire it (`instead = ""`) when either tree calls `response.url()` or records a final
       URL.
     - Probe `redirect_kept`: serve the table above (`/old` 301 → `/new.html`; `/dir` 301 → `/dir/` linking
       `child.html`). It passes when the `/old` row has `status_code` 200 and `title` "New", `/child.html` was asked
       for, and `/dir/child.html` never was. `scratchpad/r12-3/srv.py` is a working start (40 lines). It ran in 25 s.
   - X1, new text (23 words): "Its `sitemap.xml` is every page with `status_code` 200, in one file; the format allows
     50,000 per file. It keeps `noindex` and canonicalised pages." Release anchors: `run_export_sitemap_command`
     contains `node.status_code == Some(200)` and has no `canonical` and no `noindex`. HEAD skips canonicalised pages,
     so this one is scope "release" (it is under "Before you run 0.1.3:", which stays true).
   - The eighth item: Microsoft's 2-to-7 is a guideline for lists people scan, and this is the list a chooser reads
     line by line. If the cap must stay at 7, fold X1's new last sentence into X3's place and keep X1 as it is.
     Don't drop the redirect item.
   - Test: STRINGS-TWICE against H1 and the comments (no five-word run is shared, but run it); README-CAUTIONS with
     8 items; FLAG-WRAP at 320 to 430 (no flag in X1 or X3 starts with "-").

2. **Give Scrapy an arrival: where the pages land** (`README.md`, the hand-typed sentence after the Scrapy code
   block; one `[[figures]]`-style anchor row, or a strings check, on `docker-compose.yml`
   `DELTA_LAKE_PATH=/data/delta` and `./data:/data`. About 3 lines, plus a test.)
   - Why: rustmapper's image ends in a file you can open. Scrapy's block ends on "Grafana opens on `localhost:3000`",
     a dashboard. Someone deciding whether to build on it needs to know what it leaves behind and how to read it. The
     repo answers that in `DATA_USAGE.md`. The profile doesn't link to it.
   - New text, replacing the current line: "Grafana opens on `localhost:3000`. The pages land in `data/delta/`, one
     Delta table per stage; [DATA_USAGE.md](https://github.com/BenjaminSRussell/Scrapy/blob/main/Scraping_project/docs/guides/DATA_USAGE.md)
     shows how to read or export them. Spiders run by name (`scout`), not by file name." That's +22 words, about two
     lines at 390.
   - Check: the link resolves at `96e7a1a` (README-STALE already checks links in the visible prose; if it doesn't
     cover repo-relative blob URLs, add the path to its list).

## Notes (true, not ranked)

1. **go_go_go does three things 0.1.3 doesn't.** On my fixture it exited by itself, asked for robots.txt over http,
   and recorded the 404. Its flags show `--max-depth` (default 5), `--max-pages`, `--per-host-concurrency`
   (default 2) and `--max-retries` (default 3). The Also line calls it a "counterpart". For a chooser, "it stops
   when the crawl is done and records every status" would be the reason to open it. Printing that needs a go_go_go
   run check in the pipeline (a Go toolchain in CI). I'd leave it to the owner. It is also a fair hint for 0.1.4.
2. **L5 and redirects meet.** L5 says "Start at the bare domain to take them all." On a site where the bare domain
   redirects to `www.`, the code means relative links are then resolved against the bare domain, and each of those
   URLs redirects again. I didn't probe this (it needs two host names), so it stays a note. If X3 ships and a probe
   with two hosts confirms it, L5 could add "the one your site redirects to".
3. **Licence.** Scrapy's facts line says MIT, and rustmapper's says nothing. The 0.1.3 package declares
   `License :: OSI Approved :: MIT License`, and the repository has no LICENSE file (`stats.json` `license: null`,
   the LICENSE-FLAGSHIP warning). Someone who has to clear a licence will see the gap. It's the owner's commit, and
   already on his list.
4. **The release calls itself alpha.** PKG-INFO has `Development Status :: 3 - Alpha` (`edition.status`). The page
   doesn't need the word: the date, the version and the list say it more usefully.
5. For the owner, outside this repository: record `response.url()` as the node's URL (or as a `final_url` field) and
   resolve links against it, in both crawlers; leave 3xx and `noindex` out of `export-sitemap`. That retires X3 and
   half of X1 by itself.

## Sources (new this round)

1. [S1] RFC 3986 §5.1.3, "Base URI from the Retrieval URI": "if the retrieval was the result of a redirected request,
   the last URI used (i.e., the URI that resulted in the actual retrieval of the representation) is the base URI."
   https://www.rfc-editor.org/rfc/rfc3986.html#section-5.1.3
2. [S2] reqwest docs, `redirect::Policy`: the default policy "has a maximum of 10 redirects it will follow in a chain
   before returning an error". Neither tree sets a policy (`network.rs` `Client::builder()`), so 0.1.3 follows them.
   https://docs.rs/reqwest/latest/reqwest/redirect/struct.Policy.html
3. [S3] reqwest docs, `Response::url`: "Get the final `Url` of this `Response`." The value the crawler needs, and never
   reads. https://docs.rs/reqwest/latest/reqwest/struct.Response.html
4. [S4] Google Search Central, "Build and submit a sitemap": "Include the URLs in your sitemap that you want to see in
   Google's search results"; "Use fully-qualified, absolute URLs"; "Google ignores `<priority>` and `<changefreq>`
   values"; "All formats limit a single sitemap to 50MB (uncompressed) or 50,000 URLs."
   https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
5. [S5] Apache httpd, `mod_dir`, `DirectorySlash` (default `On`): a request for `/foo/dirname` is redirected to
   `/foo/dirname/` so that "Relative URL references inside html pages will work correctly." The redirect in my
   fixture is the web server's default. https://httpd.apache.org/docs/2.4/mod/mod_dir.html
6. [S6] Scrapy docs, `Response.urljoin`: "merely an alias" for `urllib.parse.urljoin(response.url, url)`. The framework
   under his Scrapy repo resolves links against the response it got, which is what rustmapper doesn't do.
   https://docs.scrapy.org/en/latest/topics/request-response.html
7. [S7] Screaming Frog SEO Spider user guide, XML sitemap: "only HTML pages with a '200' response from a crawl will be
   included in the sitemap, so no 3XX, 4XX or 5XX responses", and pages "which are 'noindex', 'canonicalised'" are
   left out by default. This is the bar a sitemap user compares against.
   https://www.screamingfrog.co.uk/seo-spider/user-guide/general/
8. [S8] WHATWG HTML, "fallback base URL": with no `<base>`, "Return document's URL."
   https://html.spec.whatwg.org/multipage/urls-and-fetching.html
9. [S9] WHATWG Fetch: a response's URL is "a pointer to the last URL in response's URL list". With S8, a browser
   resolves `child.html` on `/dir` → `/dir/` as `/dir/child.html`. https://fetch.spec.whatwg.org/
10. [S10] Google Search Console Help, Page indexing report: "Page with redirect: This is a non-canonical URL that
    redirects to another page. As such, this URL will not be indexed", and "A URL is considered to [be] submitted by
    a sitemap even if it was also discovered through some other mechanism." https://support.google.com/webmasters/answer/7440203
11. [S11] Scrapy docs, `RedirectMiddleware`: "The urls which the request goes through (while being redirected) can be
    found in the `redirect_urls` `Request.meta` key". The framework keeps both addresses, the old one and the one it
    landed on. https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
12. [S12] Secondary, for the practice only: practitioners' sitemap audits remove "everything that isn't a 200" and
    list only final destination URLs (Moz Q&A; quickseo.ai sitemap checks guide).
    https://mozprod.nodebb.com/community/q/topic/60298/301-redirects-sitemaps-and-indexing-how-to-hide-redirected-urls-from-search-engines/4

Code and runs: sdist 0.1.3 `src/main.rs:387-445` (`run_export_sitemap_command`), `:539`; `src/bfs_crawler.rs:343`,
`:372`, `:784-825`; `src/state.rs:285`; `src/cli.rs:32, :58, :146-157`; `PKG-INFO:4, :6`. Rust-sitemap `32c2651`
`src/bfs_crawler.rs:593, :700`, `src/network.rs:25-46`, `src/orchestration/export.rs:8-60`,
`tests/crawl_exits_when_idle.rs`. go_go_go `4078b55` (`go build`, `crawl --help`, one run). Scrapy `96e7a1a`
`Scraping_project/docker-compose.yml:18-23`, `src/utils/delta.py:55-61, :338`,
`src/lakehouse/lakehouse_manager.py:2391-2394`, `cli.py:279-303, :644-648`, `docs/guides/DATA_USAGE.md`. Probe
server and outputs: `scratchpad/r12-3/srv.py`, `scratchpad/r12-3/probe/` (0.1.3), `scratchpad/r12-3/gprobe/`
(go_go_go).
