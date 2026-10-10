# Round 6 log

## Round 1

Reviews: `review-r01-1.md` (the owner's test) **5 / 10**, `review-r01-2.md` (information design) **6 / 10**,
`review-r01-3.md` (does the route work?) **4 / 10**. None meets the goal. Where they conflict, review 1 (the owner's
lens) wins.

Renders: `scratchpad/r6/build/round-01/` (the standard set, plus `once-p1-lands/`, the same sheet with the frontier
stop drawn, from `stats-once-p1-lands.json`).

### What the run check found first

`scripts/runcheck.py` now times every step and runs four probes on 0.1.3, the release pip installs (Linux x86_64,
9 Oct 2026). Review 3's findings hold:

| Probe | 0.1.3 |
|---|---|
| install (pip builds from the sdist) | passed, 179.8 s |
| crawl, one SIGINT at 45 s, three pages written | passed; exit 2.0 s after the SIGINT |
| `ends_by_itself`: a crawl with no signal exits within 150 s | **no**: still running at 150 s |
| `kill_writes_file`: SIGTERM after 5 s, sitemap.jsonl written | **no** |
| `export_after_kill`: export-sitemap on what the kill left | yes, 3 `<loc>` |
| `resume_after_kill` | **no**: "Database already open. Cannot acquire lock." |

So "resume picks up after a kill" was false for the release and is gone, and the hazard now says the crawl never
ends by itself.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1, r2-4: one home per fact | Cut from the image: the platform note (R4) and the export line (R14). Cut from the README: the release clause of the rustmapper sentence, the governor and seeds bullets, both hand-off sentences (the `handoffs` marker writes nothing while R15 is drawn; the Delta-export to-do is gone). New gate STRINGS-TWICE: no run of 5 words appears in both the hero's text and the README's visible text (the alt is exempt). |
| r1-2: a measure on the track | Every run-check step carries `secs` from `time.monotonic()`. The image prints one leg: the install, "3 min on Linux x86_64: pip builds it from source" (R4). The crawl and Ctrl-C times are recorded, not printed. With the loop (below), stripping colour and marks now loses information, so SPEC §7 test 4 fails as asked. |
| r1-3, r2-6, r3-2: one hazard with its move | H1 and H2 are merged. H1 on the loop: "never ends by itself: no page or depth limit, and the parent domain counts as same-site" (anchors: `url_utils.rs` parent branch, sdist `cli.rs` without `max_urls` or `max_depth`, probe `ends_by_itself` failed). Its way out, C1, on the next row: "press Ctrl-C once: that writes the file; a second press, or a kill, quits without it" (shutdown strings, probes `crawl_ctrl_c` passed and `kill_writes_file` failed). Gated on the edition: once a release carries `--max-urls`, H1 reads "stop it with --max-urls N"; once a crawl ends by itself, it prints the measured seconds. |
| r1-4, r2-1: a real order, the loop | The route is the run's order: install, start, seeds, then the rows that repeat for every page, closed by one line back up the left side (R6, flare at LINE weight, an up arrowhead 8 × 10, phone 10 × 12), then the way out and the output. New stop F1 `bfs_crawler.rs` "fetch a page; same-site links go back on the queue" (anchors `frontier.add_links(discovered_links)` and `BfsCrawler::is_same_domain(` in both trees). The governor (G1) is off the line: a short tick and secondary ink, "fewer requests in flight when redb commits slow down" (r1-6). Once P1 lands, S2 (the queue) joins the loop and the way back ends at its ring (see `once-p1-lands/`). |
| r1-5, r2-3: the title block | Name, role, then one muted line, the same words on desk and phone: "RUSTMAPPER · 1 OF 21 · CI ON MAIN PASSED 7 OCT 2026" (it wraps after "1 OF 21"). The sha and AS OF are cut from the image; the data line carries the sha and the date. "RUST" is cut from R0. Phone: 3 fine-print lines become 2. |
| r1-7 | Scrapy comment "# start.py must run from here". Rule 4 gets its reason: "A regex for a URL breaks on the first port or login inside it; `urllib.parse` does not." |
| r2-5, r3-6: phone code blocks | Both blocks fit 38 columns; Scrapy's comments sit on their own lines above their commands. New gate README-CODE-WIDTH (a bare URL is the only exception). |
| r2-7 | S1's file is `seeder.rs`. |
| r3-1: gate on running | Route entries name the probes they rest on (`runs`, `fails` in chart.toml); `data/route.py resolve()` draws an entry only when its anchors hold and its probes came out as stated, and ROUTE-UNVERIFIED fails otherwise. Entries may carry `instead` wordings and `scope = "release"` (a fact of the release only, like its seeding default). |
| r3-3 | S4 is replaced by W1 `wal.rs` "logged before stored: after a kill, export-sitemap still writes sitemap.xml" (probe `export_after_kill`). `resume` returns only when `resume_after_kill` passes. |
| r3-7 | The header rests on the code that writes sitemap.jsonl (both trees) and the run check's crawl. The data line now says what the drawing describes and which lines were run: "The drawing describes rustmapper 0.1.3, the release pip installs: every line on it names code found there, and each line about the design also at `32c2651` on main; its install, crawl, Ctrl-C, kill and export lines were run against 0.1.3 on 9 Oct 2026 on Linux x86_64." |
| r3-8 | S1 states the release's default: "start URL; by default also seeds from sitemaps, CT logs, Common Crawl" (sdist `cli.rs` `default_value = "all"`); a release defaulting to `none` reads "… if asked". |

Also: the alt text is "How to start Ben Russell's crawler rustmapper, what it does with each page, and how to stop it.
It loops until one Ctrl-C writes data/sitemap.jsonl." (25 words); `stats_schema.json` carries the new keys; AUDIT.md
has a row for the timed steps and probes.

### Fixes declined, and why

| Must-fix | Why not |
|---|---|
| r2-4 (keep the platform note in the image, cut the wheel note) | Conflicts with r1-1; the owner's lens wins. The note is a lookup, so it stays in text. |
| r2-4, r2 element table (keep the governor and seeds bullets) | Conflicts with r1-1. The image carries both now, with the release's default. |
| r1-2, the "Ctrl-C to file written" leg | Measured (2.0 s) and recorded, but not printed: on a three-page fixture the figure says nothing about a real crawl, which writes every page on the way out. That makes it as harness-made as the crawl leg r1 already ruled out. |
| r1-2, "seconds with the Apple-silicon wheel" | Not measured: the run check has only run on Linux. The install line prints the runner it measured; it will print the wheel's time once the macos-14 job runs. |
| r3-4: a HEAD leg in the run check and the sentence "main has since fixed resume and the crawl's exit" | Not done this round. HEAD fetches nothing from a site with no robots.txt (P1), so a HEAD leg on this fixture can't measure the exit or resume like for like; it needs a second fixture with a robots.txt and a ~5 min cargo build each week. Without a measured run the sentence would be a claim. Next round, or once P1 lands. |
| r3-4: "0.1.3 ON PYPI · MAIN 32c2651 · …" title line | Conflicts with r1-5 (no sha in the image). The release and its date stay on the install line; the CI line says "on main". |
| r3-6: a 390 px `scrollWidth` render check | The 38-column check on the source covers the same failure without a browser in the fast tier. |
| r2-2, r3-5: land P1 / release 0.1.4 in Rust-sitemap | Owner actions outside this repository. The gate still fails ROUTE-UNVERIFIED on S2, as it should; it isn't loosened. |

### Measured state of this build

- Desk sheet 592 high (628 once P1 lands, gate 640); phone 1178 (1198 once P1 lands, gate 1200). The phone's item
  pitch went from 46 to 43, and the gap under the title block from 68 to 60, to keep the P1 edition inside 1200.
- `python3 -m unittest`: 232 tests, all pass.
- `check.py --tier fast,render`: 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 2 warnings (log.shards,
  POSITION-EMPTY), 0 errors. STRINGS-TWICE, README-CODE-WIDTH and README-STALE are clean.

## Round 2

Reviews: `review-r02-1.md` (the owner's test) **5 / 10**, `review-r02-2.md` (the phone-first student) **7 / 10**,
`review-r02-3.md` (every number needs a definition) **5 / 10**. None meets the goal. Where they conflict, review 1
(the owner's lens) wins.

Renders: `scratchpad/r6/build/round-02/` (the standard set, plus `once-p1-lands/`, the same sheet with S2 drawn, from
`stats-once-p1-lands.json`).

### What was measured again first

- **The install, cold.** `runcheck.py` now times the install three times, each in a fresh venv with an empty
  `CARGO_HOME`, and records `cache: "cold"`, `rustc`, `cpus` and `runs`. 10 Oct 2026, Linux x86_64, 4 CPUs,
  rustc 1.97.0: 168.2, 171.4, 174.3 s. The 9 Oct figure (179.8 s, one run, 489 crates already cached) is withdrawn.
  The probes came out as on 9 Oct (`ends_by_itself` no, `kill_writes_file` no, `export_after_kill` yes,
  `resume_after_kill` no).
- **The repository count.** 22, not 21: `excel-and-vba` is public, not a fork, 4 commits. Cache mode could never find
  it (it listed the cached names only). It is now cloned and counted; `commits` is 2,037.
- **The rules' months, from git.** Rule 1's named breakers are Claude's (e6fe879, 9 Nov 2025); his own is one
  `CircuitBreaker` class (fd33c11, 29 Sep 2025). Delta Lake 4 Oct 2025, the WAL 3 Nov 2025, Prometheus 1 Oct 2025,
  Grafana 6 Oct 2025. Rule 4: the first `urllib.parse` in ideal-url-organizer is Claude's (6e8087f, 9 Nov); his own
  first is 2be623e, 13 Nov 2025. Review 3 had this one as holding; it does not, as written.
- **CI's jobs.** Rust-sitemap's run on 32c2651: 7 jobs, all `success`, all on `ubuntu-latest` (Security Audit reports
  `success` under its step-level `continue-on-error`). Scrapy's on 96e7a1a: 5 jobs, all `success`.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-2: one home per fact | Cut from the image: the crawl command (R3), the install time (R4) and the CI line. The image's one command is `pip install rustmapper`. STRINGS-TWICE now also fails any run of 3 words that names code (`_`, `--`, `.rs`, `.jsonl`) or a date (a month with a year) found in both the hero and the README's visible text, with one allowlisted phrase, `pip install rustmapper`. |
| r1-3: W1's cause | W1 is `writer_thread.rs` "saved every 50 ms: after a kill, export-sitemap still works". The 50 is printed from `const BATCH_TIMEOUT_MS` through a new `const` anchor, read in both trees, and the trees must agree. New `fn` anchors: `run_export_sitemap_command` opens `CrawlerState` and has no `WalReader`, in `main.rs` (sdist) and `orchestration/export.rs` (HEAD). Probe `export_after_kill`. T-ANCHOR fixture cases: changing the constant changes the printed number; differing constants fail; `fn` narrows to the body. "writes sitemap.xml" became "still works" to keep the row on one desk line under the longer file label. |
| r1-4: the title block | Name and role only. "RUSTMAPPER · 1 OF 21" is gone (PURPOSE T3 with it). |
| r1-5: the hazard band | Behind H1, a band from the hatch's left edge to the text's right limit, the text block's height plus 6, accent at 14 % over paper (day `#F0D4C7`, night `#312531`), first in the row's group so the track, the loop line and the words sit on it. Ink on it measures 10.3:1 by day and 8.4:1 by night; the hatch 3.4:1 and 5.1:1. New CONTRAST-BAND check. T-NOSIZE holds: the band's size follows the number of text lines only. The hatch on the loop sits at x 414 desk / 8 phone (the review's 432 / 26 is the off-loop hatch), so the band starts there. |
| r1-6: plain words | G1 "fetches fewer pages at once when saving falls behind". S1 "start URL; by default also sitemaps, certificate logs, Common Crawl" ("seeds from" dropped to keep one desk line). Wheel note "Prebuilt for Apple silicon on CPython 3.13; elsewhere `pip` builds it from source, which needs a Rust toolchain (3 min from a cold cache on a 4-core Linux x86_64 machine)". |
| r1-7, r2-2: the data line | "The drawing is rustmapper 0.1.3 from PyPI: every file it names is in that release, and its install, crawl (a local 3-page site, `--seeding-strategy none`), Ctrl‑C, kill and export lines ran on 10 Oct 2026 (Linux x86_64). Tests and CI measured 10 Oct 2026 from 22 public repositories · regenerated weekly." The crawl's words come from the step's own command and detail (`crawl_words`); a test checks the flag appears when the cmd carries it. The AI sentence follows as it was. |
| r2-1: true file labels | `label_for`: a desk label is drawn only when a path ending in that name is among the entry's release anchors and, unless the entry is release-scope, its head anchors. G1 loses `governor.rs` (0.1.3 keeps it in `main.rs`). ROUTE-LABEL fails any drawn label not among its entry's anchors; candidates store their anchor `paths`. |
| r2-3: C1 | "press Ctrl-C once: that writes data/sitemap.jsonl; a second press or a kill skips it" (and the `instead`: "… a second press skips it"). |
| r2-5 (part) | `rustc --version` is recorded in the install step (`rustc`, and in `detail`). |
| r2-6 | Scrapy comment "# run start.py from inside this dir". |
| r2-7b | "Ctrl‑C" in the data line uses U+2011. |
| r3-1: every public repository | Cache mode lists the cached names, REST `users/{login}/repos?type=owner` when it answers (it does not from this session; it does in the workflow), and README links that REST `repos/{login}/{name}` confirms are his, public and not forks (`list_repositories`; `provenance.repo_list`). The "N more repositories" figure is computed (`more_count`: 22 − profile − 2 flagships − 4 Also = 15). New REPO-SET check. The image prints no count now (r1-4), so the "1 OF 22" line is not drawn. |
| r3-2: the rules' dates | `[[notices]]` carry `anchors {key, repo, text}`; `data/proof.py` finds his first commit adding each (author date) and the first by anyone; cites print `{month:key}`. NOTICE-DATE, NOTICE-AUTHOR, NOTICE-ANCHORS. Cites now: "Scrapy, Sep 2025: a circuit breaker in the error handler." "Scrapy, Oct 2025, the Delta Lake tables; rustmapper, Nov 2025, the write-ahead log." "Scrapy, Oct 2025: Prometheus metrics, then Grafana dashboards." "ideal-url-organizer, Nov 2025; Claude wrote its first version." (`names_agent = true`). |
| r3-3: cold install | Above. The time prints only when `cache == "cold"` (test), and only in the wheel note. |
| r3-4: snapshot labels | "On main at `32c2651`: built on …" and "On main at `96e7a1a`: …". |
| r3-5: CI from the jobs | `rest_jobs()` stores each job's name, conclusion and runs-on labels, with the run's `head_sha`; a failed job under a passing run prints "CI passed, <job> failed (not blocking)". The AUDIT `ci` row says what "passed" covers and leaves out. |
| r3-6: typed figures | "25+ ways" → "25 ways"; "across seven languages" → no number (9 languages is a derived count no file states); "Most pages get" → "Pages get"; "rates out of five" → "for your boss" (nothing in the repository says five). New `[[figures]]` rows (25 ways, stage 3, stage 4, 50,000 characters, localhost:3000), checked at HEAD by `proof.figure_records`; new FIGURES check fails any number in the README's own prose that no holding row covers. |
| r3-7: AUDIT.md | Stale rows fixed (hero prints, scrape_interval verdict, 2,037, github-actions 1 / 306 in all, the route entries, the install record). New rows for `rules`, `figures`, the cache-mode repository list and the CI jobs. §7 "Printed figures" is generated by `scripts/audit_figures.py` from PURPOSE, the README blocks, `[[figures]]` and the notices' anchors, with no weekly values in it; AUDIT-STALE fails when it drifts. |

### Fixes declined, and why

| Must-fix | Why not |
|---|---|
| r1-1: land P1, add `[project.scripts]`, wheels for every platform, publish 0.1.4 | Owner actions in Rust-sitemap, outside this repository and this branch. The pipeline already switches H1 to the `--max-urls` wording and prints the measured exit once a release carries them. ROUTE-UNVERIFIED still fails on S2, as it should; no gate is loosened. Nothing here touches `main`, so the round-5 hero stays live. |
| r1-4: gates desk ≤ 500, phone ≤ 1020 | Phone ≤ 1020 is set: 973 today, 1016 with S2 drawn. Desk is set to ≤ 580, not 500: on the desk the title block is a separate column, so cutting its line saved no height, and only R3 and R4 (56 units) came out of the route column. With every row on one line the desk is 536 (572 with S2); 500 would need line spacing tighter than 13 px text can take. Was 640. |
| r2-4, r3-1 (image): "1 OF 21/22 PUBLIC REPOSITORIES" | Conflicts with r1-4 (owner lens): the title block is name and role. The count is in the data line, and REPO-SET holds the README to it. |
| r2-5: keep R4 with "compiled; needs Rust" | Conflicts with r1-2 (owner lens): the install time and its condition live in the wheel note, once. |
| r2-7a: give the AI clause its base ("63 of my 2,037 commits") | Conflicts with r1-7 ("keep the AI-trailer sentence after it, as is"), and the owner has said the page need not show commit totals. The share stays a share; its definition is in AUDIT §7. |
| r1-7: under 45 words | The two sentences are 51 words: r2-2's clause (what the crawl ran on, 7 words) is the reason, and an audit line that overstates is worse than a long one. |
| r3-3: "the image's install line gets no number until the macos-14 job supplies one" | The image has no install-time line at all now (r1-2). |

### Measured state of this build

- Desk sheet 536 high (572 with S2 drawn; gate 580); phone 973 (1016; gate 1020).
- `python3 -m unittest`: 252 tests, all pass.
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 2 warnings (log.shards,
  POSITION-EMPTY), 0 errors; the render tier is skipped while fast fails, and run alone it passes (0 fail). STRINGS-TWICE,
  FIGURES, REPO-SET, NOTICE-*, ROUTE-LABEL, CONTRAST-BAND, AUDIT-STALE and README-STALE are clean.

## Round 3

Reviews: `review-r03-1.md` (the owner's test) **6 / 10**, `review-r03-2.md` (the copy editor) **6 / 10**,
`review-r03-3.md` (the developer choosing a crawler) **6 / 10**. None meets the goal. Where they conflict, review 1
(the owner's lens) wins.

Renders: `scratchpad/r6/build/round-03/` (the standard set, plus `once-p1-lands/` from `stats-once-p1-lands.json`).

### What was measured again first

- **The stats, rebuilt.** `build_stats.py --mode cache` (clones live, PyPI live, REST partial), so the new keys come
  from the instruments, not from a hand edit: `repos[].license` (Scrapy `MIT`, Rust-sitemap `null`: REST
  `repos/BenjaminSRussell/Rust-sitemap` answers `"license": null`), `edition.modules` (`[]`: the 0.1.3 wheel holds
  `METADATA`, `WHEEL`, `RECORD` and `rustmapper-0.1.3.data/scripts/rust_sitemap`), the `pick` rows, the
  `python_api` gate (holds at 32c2651) and the two README sentences. Everything else came out as on 10 Oct (22
  repositories, 2,037 commits, the rules' months, CI).
- **H1's cause, in the code.** The release's `start_crawling` (`src/bfs_crawler.rs:550`) keeps its "Crawl complete:
  frontier empty and no tasks in flight" check in the `else =>` arm of `tokio::select!`, which runs only when every
  branch is disabled. Rust-sitemap #65, fixed on main in `d751cf0`. The run check's three-page crawl wrote all three
  pages and was still running at 150 s.
- **The scope fact.** `url_utils.rs` `is_same_domain` (both trees) takes the start's subdomains and every domain the
  start ends with, at a dot boundary; siblings are not taken.
- **The load.** In the release `HostState::new` sets `max_inflight: 20` and `crawl_delay_secs: 0`; `--workers`
  defaults to 256 (main has since raised it to 512); a robots.txt `Crawl-delay` is applied at `state.rs:560`.
- **The Scrapy block, in Docker.** `docker compose build scraper` on Scrapy `96e7a1a` (the `base` stage; the
  `production` stage is base plus copies of the same files and ran this disk out of space) builds, and
  `docker compose run --rm --no-deps scraper scrapy list` prints `base`, `deep_dive`, `depth`, `javascript`, `scout`:
  inside the image `scrapy` is on the path and `scrapy.cfg` is found in `/app`. A crawl in the image without Redis
  stops at "Failed to connect to Redis", as it should: the compose service gets Redis from `depends_on` and
  `REDIS_HOST=redis`. The full `docker-compose run --rm scraper scrapy crawl scout …` with Redis was **not** run:
  Docker Hub answered 429 to the `redis:7-alpine` pull. The one sandbox change was the session's CA file for pip.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1, r2-1: H1's cause | H1 "never stops by itself, even after the last page", release anchors `fn start_crawling` containing `else =>` and "Crawl complete: frontier empty", probe `ends_by_itself` failing. The `--max-urls` and `{secs}` wordings are gone; an alternative with empty text retires H1 once the probe passes (`resolve`: `retired`, neither drawn nor unverified). T-ANCHOR fixtures: the else arm replaced by a timer leaves H1 unverified; a crawl that ends retires it; H1's words carry no scope term. |
| r1-1: the scope fact | F1 "fetches a page; queues links on its domain, above or below it", with the two `is_same_domain` branches as anchors in both trees. r1's own wording (76 characters) and its fallback (74) both broke onto a second desk line next to `bfs_crawler.rs`, which would take the S2 edition past the gate; this is the same fact in 61. |
| r1-2, r2-2: the fault as a shape | The band and both hatch blocks are cut. While a drawn trap on the loop names a failed probe, the track stops at the loop's foot and starts again 10 (desk) / 12 (phone) above C1's ring. With the old pitch those numbers left a 1-unit gap on the desk and none on the phone, so the next row moves down until the gap is 16 / 18 units (the only probe-driven geometry; T-NOSIZE holds). H1's words are ringed by a dotted danger line: a rounded rectangle, padding 6, `rx` 6, BRUSH dots (r 1.7, the nearest token weight to r 1.4 / 1.8) evened round the perimeter at about 6 / 8, accent, no fill; its four edges are exclusions, so the bounds check fails any text crossing it. CONTRAST-BAND became CONTRAST-DANGER (accent ≥ 3:1 on paper, 4.1 day and 6.1 night; nothing filled under the trap). New test: with every fill and stroke set to black, the track still breaks once, at the loop's foot, by ≥ 14 units. |
| r1-3: one instruction for stopping | W1 "saved every 50 ms" (const anchor kept, no probe). C1 "press Ctrl-C once to write `data/sitemap.jsonl`; after a kill, run `export-sitemap`", on `crawl_ctrl_c` and `export_after_kill` passing and `kill_writes_file` failing, with the export anchors (opens `CrawlerState`, never `WalReader`) moved from W1. Its alternative, once a kill writes the file: "press Ctrl-C once to write `data/sitemap.jsonl`". |
| r1-4, r2-6: the data line | "The drawing is rustmapper 0.1.3 from PyPI: every rustmapper source file it names is in that release; the reader it points to is ideal-url-organizer's, at `159968a`. Its install, crawl (…), Ctrl‑C, kill and export lines were run on 10 Oct 2026 (Linux x86_64)." ROUTE-LABEL now covers every drawn source file (`.rs`, `.py`, `.toml`): one keyed to a route entry must be among its anchors; one keyed to a hand-off must be that hand-off's `reader`, with state `runs` and a `to_sha`. |
| r1-5: phone wrap | A separator break is taken only when every line is ≥ 45 % of the measure; word breaks are balanced (the narrowest measure that keeps the line count). Test on every edition for S1, F1, C1, H1. S1 also takes r2's wording (below), which has no semicolon. |
| r1-6: the governor row | A note with no file label sets its words at the label column (x 484) in `ink2`; the tick stays. Test. |
| r1-7: the image links to the project | The hero's `<picture>` is wrapped in `<a href="https://github.com/BenjaminSRussell/Rust-sitemap">` (`hero_link` from chart.toml). Checked after the push: GitHub's rendered README for `v12/purpose` (REST `repos/…/readme`, HTML) keeps the outer `<a href>` round its `<themed-picture>`, and adds no link of its own to the raw SVG. |
| r2-3 (part): one home per fact in the image | R13 "fields: `url, depth, status_code, title, …`". New HERO-SELF-TWICE: no run of 4 words drawn twice in one edition (alt left out). |
| r2-4: the user's step and the tool's | S1 "your URL, plus by default sitemaps, certificate logs, Common Crawl" (its alternative "… Common Crawl if asked"), F1 in the third person, C1 the one imperative. |
| r2-5: one face for code | Backticked spans in a row's words are set in `machine` at the label size, measured in that face when lines are broken, and re-opened across a line break. New TYPE-CODE (fast): a hero run outside `machine` holding `_`, `--`, `.rs`, `.jsonl` or `export-sitemap` fails. |
| r2-6: third person | "3 % of Ben's commits … are not counted as his." New test: no I, my, mine or me in the README's visible prose. |
| r2-7: rules and Also | Rule 2 "Raw before clean."; rule 4's cite "ideal-url-organizer, Nov 2025; Claude's commit used it first." (`names_agent` still holds); "Home of the "no regex" rule." cut. |
| r2-8 (part), r3-1 (part): the license line | "**This profile** Code MIT; …. The image is rustmapper's route in `chart.toml` (`[route.rustmapper]`, each line with the code it rests on); the build draws only the lines that code and its run check prove". README-LICENSE looks for "Code MIT". |
| r2-9: the rustmapper sentence | New `about:Rust-sitemap` block: "… written in Rust. `pip install` gives you its command line; the Python API, built with maturin, is on main and not yet released." while `edition.modules` lacks `rustmapper` and the `python_api` gate holds; "… with a command line and a Python API built with maturin." once a wheel ships the module; a bare sentence when never measured. |
| r2-10, r3-4: the Scrapy block | "# the whole pipeline (needs docker / # and docker-compose); it crawls a / # university's sample site" above `python start.py`; "# or only discovery, on your own site:" above `docker-compose run --rm scraper \ scrapy crawl scout …`; the sample-URLs sentence under the block is cut. All lines ≤ 38 columns. |
| r2-11: the builds line | "Ben Russell builds web crawlers, discovery pipelines, raw-first storage, and the dashboards that watch them." |
| r3-1: licenses, measured | `repos[].license` from REST `license.spdx_id` (GraphQL `licenseInfo.spdxId` in live mode), `null` when GitHub detects none or says `NOASSERTION`, absent when the API did not answer (the cache's value is carried). Schema and AUDIT rows. The facts line prints "· MIT license" after the CI clause only when set (Scrapy today). LICENSE-FLAGSHIP warns for Rust-sitemap. |
| r3-2: which tool for which job | New `pick` block: "For the list of a site's URLs from one command, **rustmapper**; to keep the pages themselves, deduplicated and summarised, in a pipeline that needs Docker, **Scrapy**." Printed only while the route header holds and the three `[[figures]]` rows tagged `use = "pick"` hold at Scrapy's HEAD (`MinHashLSH` and "extractive summary" in `stage3_worker.py`, `"local": ("docker", "docker-compose")` in `start.py`). |
| r3-3: load and the 50,000 cap | Two route entries of the new kind `text` (checked by the route engine, never drawn), printed as their own paragraph under the wheel note: L1 "It sends up to 20 requests at a time to one host, 256 in all, with no pause between them unless the site's `robots.txt` sets a `Crawl-delay`." (release scope; new value anchors `{field:max_inflight}`, `{arg:workers}`, and `equals` to pin `crawl_delay_secs: 0`); X1 "0.1.3 writes one `sitemap.xml` however many pages it found; the sitemap format allows 50,000 URLs per file." while the sdist has no `SitemapIndexWriter`, the 50,000 read from main's `DEFAULT_MAX_URLS_PER_SITEMAP` (`from_head`); it retires once a release splits. Tests for both. |
| — | ROUTE-HEIGHT is desk ≤ 600, phone ≤ 1040: the gap adds 15 / 19 units, and the S2 edition (once P1 lands, with the gap) is 587 / 1035. DESIGN.md's paragraph (generated from `tokens.py`) describes the route as drawn now. |

### Fixes declined, and why

| Must-fix | Why not |
|---|---|
| r2-1: H1 "never ends by itself, even after its last page: a 3-page site ran past {secs} s", and keep the `--max-urls` alternative | Conflicts with r1-1 (owner lens): the short cause, no figure, and no scope wording when a release has `--max-urls`; a release that ends by itself retires the row. r2's T-ANCHOR case is kept in spirit: the test asserts H1's words name no limit, depth or domain. |
| r2-2: keep the 14 % fill under the dotted outline | Conflicts with r1-2 (owner lens): no fill. |
| r2-3 (part): C1 "write the file below", and HERO-SELF-TWICE on code tokens | Conflicts with r1-3 (owner lens), whose C1 names the file the press writes. HERO-SELF-TWICE checks runs of 4 words only; with a code-token rule it would fail the owner's wording on `data/sitemap.jsonl`. |
| r2-4 (part): W1 "saves every 50 ms, so after a kill export-sitemap still works" | Conflicts with r1-3: the kill clause lives on C1, once. |
| r2-8 (part): "fork the repository and write your project's route …" | Not true of the build: the PyPI project, the run check and the sheet's project are rustmapper's, so a fork would get rustmapper's route or a failing gate. The line says the image is rustmapper's route instead (r2's own second option). |
| r3-3: "both go through FIGURES" | FIGURES covers numbers typed by hand outside the build-written blocks. These are build-written and stronger than a literal row: 20, 256 and 50,000 are read from the code by the value anchors, and the sentence is not printed when they do not hold. |
| r3-4: `docker-compose exec scraper …` | `exec` needs the running stack, which `python start.py` brings up with the sample pipeline; `run --rm` starts Redis (`depends_on`) and runs only the given command, so "or only discovery" is true. The full run with Redis is not confirmed (Docker Hub 429, above); the image half is. |
| r3-5: Rust-sitemap's About text, pins, DESC-DRIFT | Owner actions in Rust-sitemap and on the profile. DESC-DRIFT is not added: `stats.json` does not carry the API description, and a check on a figure the pipeline does not gather would be the first one of its kind. |
| r1 owner action, r3-1 owner action: land P1, a `[project.scripts]` command, 0.1.4; commit Rust-sitemap's MIT `LICENSE` | Outside this repository. ROUTE-UNVERIFIED still fails on S2 and LICENSE-FLAGSHIP warns, as they should. Once 0.1.4 ends by itself, H1 is retired and the gap closes with no edit here. |

### Measured state of this build

- Desk sheet 551 high (587 with S2 drawn; gate 600); phone 992 (1035; gate 1040).
- `python3 -m unittest`: 263 tests, all pass.
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 3 warnings (log.shards,
  POSITION-EMPTY, LICENSE-FLAGSHIP Rust-sitemap), 0 errors; the render tier is skipped while fast fails, and run alone
  it passes (0 fail). TYPE-CODE, HERO-SELF-TWICE, ROUTE-LABEL, CONTRAST-DANGER, STRINGS-TWICE, FIGURES, README-STALE,
  README-CODE-WIDTH and AUDIT-STALE are clean.

## Round 4

Reviews: `review-r04-1.md` (the owner's test) **7 / 10**, `review-r04-2.md` (the chart historian) **7 / 10**,
`review-r04-3.md` (the working navigator) **7 / 10**. None meets the goal. Where they conflict, review 1 (the owner's
lens) wins.

Renders: `scratchpad/r6/build/round-04/` (the standard set, plus `once-p1-lands/`, the same sheet with S2 drawn,
from `stats-r4-all.json`).

### What was measured first

- **When the crawl is done, from its own output.** `scripts/runcheck.py` has a new probe, `quiet_after_last_page`,
  taken from the `ends_by_itself` run: the crawl's output is read through a pipe, and each `Received work item` line
  is stamped as it arrives. The probe passes when those lines name as many URLs as `sitemap.jsonl` has lines after
  the SIGINT, and the last came at least 100 s before it. The two probes were run again on 10 Oct 2026 (Linux x86_64)
  on the 0.1.3 binary that day's run check installed (`scratchpad/r6/rc4/probe.py`): `ends_by_itself` no
  (still running at 150 s), `quiet_after_last_page` yes ("3 work-item lines for 3 URLs, the last 150 s before the
  SIGINT; 3 lines in sitemap.jsonl after it"). Both steps replace or join the record in `runcheck.rustmapper`; the
  install and the other steps are the morning's.
- **The routes and the hand-off, re-checked.** `routes.rustmapper` and the fields hand-off were verified again from
  the Rust-sitemap clone at `32c2651`, the 0.1.3 sdist and ideal-url-organizer at `159968a`
  (`scratchpad/r6/reroute4.py`, which refuses a tree at another commit than `stats.json` names).
- **What the export writes.** `run_export_sitemap_command` (sdist `src/main.rs`) opens `CrawlerState` and builds a
  `SitemapWriter` on `--output`, whose default in `cli.rs` `ExportSitemap` is `./sitemap.xml` in both trees. It never
  writes `sitemap.jsonl`. `--data-dir` defaults to `./data` for both `crawl` and `export-sitemap`.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-2: the stop in the pasted block | The install block reads `pip install rustmapper` / `rust_sitemap crawl \` / `    --start-url <your-site>` / `# stop it with one Ctrl-C` / `rust_sitemap export-sitemap`. The comment is printed only while `ends_by_itself` failed and `crawl_ctrl_c` passed. The export's two flags are gone while the new release gate `export_defaults` holds: `ExportSitemap`'s `data_dir` is `./data` and its `output` `./sitemap.xml`, and `Crawl`'s `data_dir` is `./data` (value anchors, narrowed to the subcommand by the new anchor key `block`). If a release changes them, the flags come back. 7 lines to 5. The optional `# writes ./sitemap.xml` line is not printed: the image's Ctrl-C row and X1's sentence under the block already say where it writes, and STRINGS-TWICE caught the repeat. |
| r1-3 (wins over r2-3): one left edge | Every row's words start at x 484 on the desk, as on the phone. The desk's file labels are set in `machine` 19, muted, right-aligned to x 424 on the row's first baseline, in the empty column under the role line. They are drawn all or none: if one would come within 4 units of the name or the role line, or the column met the loop's line, none is drawn (test). Today all three fit (`seeder.rs` 321–424, `bfs_crawler.rs` 264–424, `writer_thread.rs` 242–424; the role line's second line ends at 224). New ROUTE-LEFT-EDGE (fast tier, from the build report): every drawn row's leftmost run right of the track starts at one x. |
| r1-4 (wins over r2-4): the AI clause | "Tests and lines are counted per repository, whoever wrote them: coding agents (Claude, jules) authored 45 of rustmapper's 146 commits and 71 of Scrapy's 499." Computed per repository with a facts line from `repos[].others` with `bot: true`, less `survey.AUTOMATION` (dependabot's 8 Scrapy commits are left out), over `repos[].all_hands`. No agent commits, no clause. The trailer share and the 297 are gone from the page. AUDIT §7 row replaced; tests. |
| r1-5: the licence line | "**This profile** Code MIT; images and text CC BY 4.0; fonts under their own licenses in `scripts/fonts/`." The build sentence is cut. DESIGN.md is linked from the word "drawing" in the data line. |
| r1-6: the pick sentence | "For the list of a site's URLs, from one binary with no services to run, **rustmapper**; …". Printed only while the release gate `no_services` holds: `Crawl`'s Redis flag is a clap `bool` (`enable_redis: bool,` under "Enable distributed crawling with Redis"), false unless given. |
| r2-1 + r3-2: C1 and W1 | C1 "press Ctrl-C once to write `data/sitemap.jsonl`; after a kill, `rust_sitemap export-sitemap` writes the pages to `sitemap.xml`". `sitemap.xml` is `{arg:output}`, read from `ExportSitemap --output`'s default in both trees (a string default prints without its `./`); new release anchor `fn run_export_sitemap_command` contains `SitemapWriter::new`. `rust_sitemap` is `{script}`, filled by the sheet from `edition.scripts` by the T-SCRIPTS rule (test: C1 names `edition.scripts[0]`). On the desk it breaks at the semicolon into two lines. Not r2's "→": on the phone the arrow and the file fell to a line of their own; "writes the pages to" keeps three balanced phone lines and is plainer. W1 "saved to its database every 50 ms", with anchors `state.apply_event_batch(&batch)` in `writer_thread.rs` and `use redb::` in `state.rs`, both trees. |
| r2-2: the governor under fetch | The tick is gone. G1's words are the last line of F1's row, in `ink2`, at F1's x; `hero-G1` and its PURPOSE row stay. BREAKS: "The governor is a note under fetch". Test: no mark for G1, its line is F1's next line and above W1. |
| r3-1: when to act | H1 "never stops by itself; done when `Received work item` lines stop", with the release anchor `fn start_crawling` containing `Crawler: Received work item:` and the probe `quiet_after_last_page` (above). Without that probe it falls back to "never stops by itself, even after the last page"; once a release ends by itself, the empty alternative still retires the row. Tests for all three. Desk one line; phone two. |
| r3-3: whose domain | F1 "fetches a page; queues links on your URL's domain, above or below it". |
| r3-4: what the next project does | The hand-off record gains `does`: "sorted by" when ideal-url-organizer's reader at `to_sha` contains `run.sh` and `--all` (it imports the file and runs the organizer's whole pipeline), else "read by". Desk "sorted by ideal-url-organizer: `scripts/import_rust_sitemapper.py`, with a test"; phone "sorted by ideal-url-organizer, with a test". |
| r3-5: the Scrapy block | "# in a clone of this repository;" / "# start.py runs only from here" above `cd Scraping_project` (32 and 30 columns). |
| — | ROUTE-HEIGHT desk ≤ 620, phone ≤ 1100. Today 571 / 1051; with S2 drawn 607 / 1094. DESIGN.md's paragraph (from `tokens.py`) describes the route as drawn now. |

### Fixes declined, and why

| Must-fix | Why not |
|---|---|
| r1-1: ship rustmapper 0.1.4 from main (P1 robots 4xx, the MIT `LICENSE`, `[project.scripts]`, a wheel workflow, the release) | All of it is work in Rust-sitemap and a PyPI release under the owner's account, outside this repository and this session's credentials. The findings are recorded for him: a 0.1.4 cut from `32c2651` would fail to build (PEP 639: `license-files = ["LICENSE"]` matches no file) and would ship no command (`bindings = "pyo3"` without `[project.scripts]`). Review 3 asks not to hold the image for it, and the image says what pip installs today. ROUTE-UNVERIFIED still fails on S2 and LICENSE-FLAGSHIP still warns, as they should; once 0.1.4 passes the run check, H1, the gap, C1's kill clause and X1 retire, S2 is drawn, and the gate goes green with no edit here. |
| r1-2 (part): "# writes ./sitemap.xml" | Optional in the review, and a repeat: STRINGS-TWICE fails "rust_sitemap export-sitemap writes" against the image's C1. The file's name is on C1 and in X1's sentence under the block. |
| r3-2 (part): exempt `<script> <subcommand>` runs from STRINGS-TWICE's 3-word rule | No run collides now. The only collision the build met was a real repeat of a fact (above), which the exemption would have hidden. |
| r2-4: "The working rules are dated by Ben's own first commits: 297 …" | Conflicts with r1-4 (owner lens), applied above. |
| r2-3: one rule column at x 686 | Conflicts with r1-3 (owner lens), applied above: the column is x 484 and the files move left of the track. |

### Measured state of this build

- Desk sheet 571 high (607 with S2 drawn; gate 620); phone 1051 (1094; gate 1100).
- `python3 -m unittest`: 274 tests, all pass.
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 3 warnings (log.shards,
  POSITION-EMPTY, LICENSE-FLAGSHIP Rust-sitemap), 0 errors; the render tier is skipped while fast fails, and run alone
  it passes (0 fail, 0 warn). ROUTE-LEFT-EDGE, ROUTE-HEIGHT, ROUTE-LABEL, TYPE-CODE, HERO-SELF-TWICE, STRINGS-TWICE,
  FIGURES, README-STALE, README-CODE-WIDTH and AUDIT-STALE are clean.

## Round 5

Reviews: `review-r05-1.md` (the owner's test) **7 / 10**, `review-r05-2.md` (the staff engineer screening for data
infrastructure) **7 / 10**, `review-r05-3.md` (the information designer) **7 / 10**. None meets the goal. Where they
conflict, review 1 (the owner's lens) wins.

Renders: `scratchpad/r6/build/round-05/` (the standard set, plus `once-p1-lands/`, the same sheet with S2 drawn, from
`stats-r5-all.json`). Routes re-verified from the local trees with `scratchpad/r6/reroute5.py` (Rust-sitemap clone at
`32c2651`, the 0.1.3 sdist, ideal-url-organizer at `159968a`; it refuses a tree at another commit than `stats.json`
names). It also drops rule 2's `wal` record from `rules` and takes the notices' cites from chart.toml, as
`build_stats.py` would.

### What was measured first

- **The track over the rings.** In round 4's SVGs every stop group came before `hero-R5` and `hero-R6`, so the track
  was painted over each ring. After the fix, the rendered pixel at each ring's centre equals paper on all eight rings,
  desk and phone, day and night (ΔE 0.0; `scratchpad/r6/ringpx.py build/round-05`).
- **The write path, in order.** In `writer_loop`, in both trees, the WAL append comes before its `fsync()`, and the
  fsync before `state.apply_event_batch(&batch)` (sdist `src/writer_thread.rs:122, 136, 167`; HEAD `:136, 150, 181`).
  `WalWriter::fsync` calls `sync_all()` (sdist `src/wal.rs:198-200`, HEAD `:287-289`).
- **The governor's threshold.** 0.1.3 `src/main.rs:90` `const THROTTLE_THRESHOLD_MS: f64 = 500.0`, compared with the
  commit EWMA at `:113`. HEAD reads `GOVERNOR_THROTTLE_THRESHOLD_MS` (`src/orchestration/governor.rs:16`), so the
  figure is the release's.
- **What main fixed.** `tests/crawl_exits_when_idle.rs` at `32c2651` holds `fn crawl_exits_after_frontier_drains`
  under `#[test]`, with no `#[ignore]`; `ci.yml:76` runs `cargo test --all-features`; `repos[Rust-sitemap].ci` is a
  success at `head_sha` = `head.sha`, with the job `Test (ubuntu-latest, stable)`. The test runs with 1 s idle flags,
  so no timing is printed.
- **Widths.** G1 with its measure is 647 units on the phone (measure 600) and 473 on the desk; review 2's fallback
  ("when a save averages") is 665, longer still. The phone sets G1 on two lines.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-2 + r3-4: cut the desk file labels | The all-or-none test gains a proximity rule: a label is drawn only if its cap top (baseline less the code face's ascent) is at least `G["line"]` (28) under the title block's last baseline. `seeder.rs` fails it, so none is drawn and the desk teaches what the phone does. Tests: no file names on any edition today, `file_labels` false; with the rows moved 80 lower, they are drawn. |
| r1-3 + r3-7: the release date next to its command | The release label starts at `TX + width(install) + 32`, anchored start, on the command's baseline, muted caps, desk and phone (desk x 767–929; phone 463–674). If it would pass the measure it drops under the command at the left edge, never to the right edge. New ROUTE-RELEASE (fast tier): the gap is at most 40, or the label sits under the command at the rows' left edge. |
| r1-4 + r3-8: the kill recovery into the code block | C1 is "press Ctrl-C once to write `data/sitemap.jsonl`" (one line on both sheets), resting on its two shutdown anchors and `crawl_ctrl_c`. The block gains `# sitemap.xml, even after a kill:` above `rust_sitemap export-sitemap` (33 columns), printed only while `kill_writes_file` failed, `export_after_kill` passed and the new release gate `export_after_kill` holds (the release's export opens `CrawlerState`, never `WalReader`, and builds a `SitemapWriter`; the file name is `ExportSitemap --output`'s default). Tests for each condition. |
| r1-5 + r3-9: the data line | "The [drawing](DESIGN.md) is rustmapper 0.1.3, the release pip installs; its commands were run against a local 3-page site on 10 Oct 2026 (Linux x86_64). Tests and lines are counted per repository, whoever wrote them: coding agents (Claude, jules) authored 45 of rustmapper's 146 commits and 71 of Scrapy's 499." The source-file and reader-sha clause, the `--seeding-strategy` aside, "Tests and CI measured … from 22 public repositories" and "regenerated weekly" are gone; DESIGN.md's paragraph now carries how the drawing is checked (its files in the release, the reader's commit, the crawl's flags). A cache-failed build still says so. Phone: 6 lines, was 10. Test: no "generated" or "regenerated" in visible README text ("AI-generated code", a project's subject, is allowed by the hyphen). |
| r1-6 + r2-5: names first in the pick sentence | Review 1's words: "**rustmapper** gives you a site's list of URLs from one binary, with no services to run. **Scrapy** keeps the pages themselves, deduplicated and summarised, in a pipeline that needs Docker." Same gates. |
| r2-1 + r3-3: rule 2 loses the WAL | Cite "*Scrapy, Oct 2025, the Delta Lake tables.*"; the `wal` anchor and its `rules` record are gone. NOTICE-ANCHORS test: no rule 2 anchor is in Rust-sitemap, ends in `wal.rs` or names the WAL's record framing, and `rules` holds only `delta` for rule 2. |
| r2-2 + r3-2: the trap names its release, and what main fixed | (a) H1 "`{release}` never stops by itself; done when `Received work item` lines stop", filled from `edition.version` by the sheet; the fallback takes the same prefix. Desk one line, phone two. (b) New text entry M1, printed after the load and 50,000 sentence: "On main, a crawl stops by itself once the site runs out of pages: `tests/crawl_exits_when_idle.rs` passes in CI at `32c2651`. That fix is not on PyPI yet." Head anchors (the test function, no `#[ignore]`, `cargo test` in `ci.yml`), release anchors (the `else =>` arm and its message), probe `ends_by_itself` failed, and the new `ci` key: printed only while `route.ci_ok` holds (success, `ci.head_sha` = `head.sha` = the route's sha, a passing job named `Test*`). An empty alternative on `ends_by_itself` passing retires it with H1. No idle timing. Tests: not printed when CI ran at another sha; unverified without the test file; retired by a release that ends. |
| r2-3: W1 names the write path | "logged to disk, then saved to redb, every 50 ms". New order anchor (`before`) in `data/route.py`: in `writer_loop`, append before fsync, fsync before `apply_event_batch`, both trees; `WalWriter::fsync` holds `sync_all()`; `BATCH_TIMEOUT_MS` and `use redb::` kept. Tests: the order anchor fails when the commit comes first. |
| r2-4: G1 at full weight with its measure | "fetches fewer pages at once when saves average over 500 ms", release scope, `{const:THROTTLE_THRESHOLD_MS}` from the sdist's `src/main.rs` (`500.0` prints as 500; test), in ink like F1, still F1's last line with no mark. Tests: G1's fill is `ink` and equals F1's; the number follows the constant. Two lines on the phone (above). |
| r2-6: Grafana's address | "Grafana opens on `localhost:3000`." The FIGURES row still matches inside the code span. Test: no `http://localhost` in visible README text. |
| r3-1: the track under the rings | The SVG body paints R5, R6 and R15 first, then the rest; `rep.route.drawn` keeps the reading order. New ROUTE-PAINT (fast tier): no group other than a line comes before the last line group. Test: every `<circle>` follows `hero-R5` on every edition; measured ΔE 0 at every ring (above). |
| r3-5: code spaces at the word space | Inside a row's backticked span, each word is set in the code face and each space in the label face (212/1000 em, not 600). `Received work item` is three code runs 4.0 apart at 19 units, not 11.4; H1's desk line is about 15 shorter, the field list about 30. New ROUTE-CODE-SPACE (fast tier): no code run of a row holds a space, and two code runs on one line are at most 1.3 label spaces apart. The README's code block keeps real spacing. |
| r3-6: the loop's arrowhead | The arrowhead sits halfway between the first two rings of the loop (desk 277–287, between F1 at 250 and W1 at 314; with S2 drawn, 263–273 between S2 and F1), not at the bracket's midpoint beside W1's ring. New ROUTE-ARROW (fast tier): the arrowhead keeps `ring_r + 2` from every ring's centre row. |
| — | ROUTE-HEIGHT rebaselined: desk ≤ 592 (620 − 28), phone ≤ 1066. Today 543 / 1017; with S2 drawn 579 / 1060. Not phone −68: G1 with its measure takes a second phone line (+34). PURPOSE, BREAKS, the route docstrings, DESIGN.md's paragraph (`tokens.py`) and AUDIT.md (routes row, §7 register) describe the sheet as drawn now. |

### Fixes declined, and why

| Must-fix | Why not |
|---|---|
| r1-1(a): ship 0.1.4 (P1 robots 4xx, the MIT `LICENSE` that `license-files` names, `[project.scripts]`, wheels) | Work in Rust-sitemap and a PyPI release under the owner's account, outside this repository and this session's credentials. Unchanged from round 4: ROUTE-UNVERIFIED still fails on S2 and LICENSE-FLAGSHIP warns, as they should. When 0.1.4 ends by itself, H1, M1, the gap and the kill comment retire, and the gate goes green with no edit here. The image does not go to `main` before then. |
| r1-1(b): Rust-sitemap's About text and `README.md:25` | Also the owner's: another repository, edited under his account (`gh repo edit` and a commit to its default branch), and this session commits only to `v12/purpose` here. The text for him, as review 1 gives it: About "Crawls a site and writes one line for every page it reaches."; `README.md:25` "`pip install rustmapper` (0.1.3, macOS arm64 wheel or a source build) installs the `rust_sitemap` command. The Python library is on main and ships in the next release."; and the examples' alias `rustmapper` → `rust_sitemap` while 0.1.3 is current. |
| r2-4 against r3 (G1 "the lighter ink is right") | The owner's lens does not speak to the ink; review 1 calls the governor "the one design idea that's mine and unusual". With its 500 ms it is a measured fact a screener can check, not a qualifier, so it takes F1's ink. It keeps review 3's point that it is no stop: no ring, F1's row. |
| r2 owner note: rename Rust-sitemap to rustmapper, pin it first | Not ranked, and the owner's: a rename in another repository. Recorded for him. |
| r2 table "Desk file labels: keep" | Conflicts with r1-2 (owner lens) and r3-4: cut. |

### Measured state of this build

- Desk sheet 543 high (579 with S2 drawn; gate 592); phone 1017 (1060; gate 1066).
- `python3 -m unittest`: 286 tests, all pass.
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 3 warnings (log.shards,
  POSITION-EMPTY, LICENSE-FLAGSHIP Rust-sitemap), 0 errors; the render tier is skipped while fast fails, and run alone
  it passes (0 fail, 0 warn). ROUTE-PAINT, ROUTE-RELEASE, ROUTE-ARROW, ROUTE-CODE-SPACE, ROUTE-LEFT-EDGE, ROUTE-HEIGHT,
  ROUTE-LABEL, TYPE-CODE, HERO-SELF-TWICE, STRINGS-TWICE, FIGURES, README-STALE, README-CODE-WIDTH, NOTICE-DATE and
  AUDIT-STALE are clean.

## Round 6

Reviews: `review-r06-1.md` (the owner's test) **8 / 10**, `review-r06-2.md` (the systems engineer who runs every
claim) **6 / 10**, `review-r06-3.md` (the student on a phone) **7 / 10**. None meets the goal. Where they conflict,
review 1 (the owner's lens) wins.

Renders: `scratchpad/r6/build/round-06/` (the standard set; the phone sheets also at 308 px, the width GitHub shows
them on a 390 px phone; the phone page at 390 and at 360, `page-phone-360-*.png`, with GitHub's 41 px box padding;
the desk page at a 1280 px viewport, since a 1100 px window now gets the phone sheet; and `once-p1-lands/`, the sheet
with S2 drawn, from `stats-r6-all.json`). Routes re-read from the local trees with `scratchpad/r6/reroute6.py`
(Rust-sitemap clone at `32c2651`, the 0.1.3 sdist, ideal-url-organizer at `159968a`, Scrapy at `96e7a1a`; it refuses
a tree at another commit than `stats.json` names), which also merges the new probe, recomputes the rules on the
history clones and re-checks every `[[figures]]` row. Render set: `scratchpad/r6/renderset3.py`.

### What was measured first

- **0.1.3 and robots.txt.** The new probe `robots_read` (`scripts/runcheck.py --probe robots_read`, fixture
  `tests/fixtures/robots-site/`: `Disallow: /secret.html`, `Crawl-delay: 5`) against the 0.1.3 binary, plain http,
  one SIGINT at 15 s: 4 requests, no `GET /robots.txt`, `/secret.html` fetched, the two closest fetches 1 ms apart.
  The server's own request log decides. Review 2's finding holds: `robots.rs` builds only
  `https://{}/robots.txt`, has no Crawl-delay parser, and `frontier.rs:787` always stores `crawl_delay_secs: None`.
- **Main's idle test.** `tests/crawl_exits_when_idle.rs:67` at `32c2651` passes `--ignore-robots`. Review 2's build of
  main without it fetched nothing from an http site. M1 rested on that test.
- **Rule 4.** On the full history clone (`ideal-url-organizer.git`, 47 commits, not shallow), his first commit with
  `urllib.parse` is `2be623e`, 13 Nov 2025, adding `from urllib.parse import urlparse` to
  `src/analyzers/semantic_analyzer.py`. The repository's first ones are Claude's, 9 Nov.
- **Scrapy's breakers.** `stage2_worker.py:218-219` `DEFAULT_STAGE2_BREAKER_FAILURES = 5`,
  `DEFAULT_STAGE2_BREAKER_RECOVERY = 60`, used per host by `_breaker(domain)` (`:923-934`); Scrapy's README
  (`:397-400`) says the same. The three service breakers in `utils/retry.py` have no caller.
- **rust_llm_logger.** `proxy.rs:170-173` calls `parser.feed_chunk(&data).await` and then `client_tx.send`; the record
  is written after `drop(client_tx)` (`:191-192`).
- **Widths.** At 600 units the phone sheet is 1,169 tall (600 px at 308), 1,246 with S2 drawn (640 px). The desk sheet
  is 571 (607 with S2). Smallest text: phone 26 units, 13.3 px at 308 and 12.0 px at 278; desk 19 units, 11.4 px in
  the 766 px column of a 1200 px window.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1 + r2-2: M1 not printed while the cargo gate fails | M1 carries `gate = "cargo"`; `data/route.py` keeps the key on the record, and `render_readme.text_entries` skips any text entry whose gate record is not `ok` (a gate never computed does not hold). M1's own wording gains the head anchor `absent = "--ignore-robots"` on `tests/crawl_exits_when_idle.rs`, and a last empty alternative holds while the test has that flag, so today M1 is retired (verified, not printed, not a failure). "On main, a crawl stops by itself … not on PyPI yet." is gone from the page. Tests: not printed with `cargo` false; with the gate true and the fixture test holding `--ignore-robots`, the empty alternative is taken; with both holding, it prints; CI at another sha still drops it. |
| r1-3: the hand-off label | "sorted 25 ways by ideal-url-organizer", `label`, `ink2`, one line, desk and phone; no script path, no ", with a test". `sheets/route.py` `handoff_words()` reads "25 ways" from the `[[figures]]` row of the receiving repository that holds (25 `method_*.py` files at `159968a`); without it, "sorted by ideal-url-organizer". The gate is unchanged: R15 is drawn only while the hand-off's state is `runs`, which needs the test. PURPOSE R15 updated. Tests for the words and the fallbacks. |
| r1-4: F1 in plain words | "fetches a page; queues links to your site, its subdomains and its parent domain", same `is_same_domain` anchors (both branches, both trees). |
| r1-5: one description of rustmapper per screen | `about_block`: "**[rustmapper](…)**: `pip install` gives you its command line; the Python API, built with maturin, is on main and not yet released." No "concurrent sitemap crawler written in Rust" on any path. |
| r1-6: rule 4 cites his own commit | The `urlparse` anchor carries `author = "self"`; `proof.rule_records` writes `scope: "self"` on its record; NOTICE-AUTHOR checks that his first commit adding the text exists (and that the record was computed with the scope) instead of asking whether the repository's first one was his. Cite: "*ideal-url-organizer, Nov 2025: URLs split with `urllib.parse`.*" `names_agent` is gone. The month is his commit's (2be623e, above). Tests: committed record; fails without his commit or without the scope; an unscoped anchor still fails on an agent-first record. |
| r2-1: L1 says what 0.1.3 does with robots.txt | "It sends up to 20 requests at a time to one host, 256 in all, with no pause between them. 0.1.3 ignores `Crawl-delay`, and asks for `robots.txt` only over https, so a plain-http site's rules are not read." Release anchors: `robots.rs` without `fn parse_crawl_delay` (main's `parse_crawl_delay_secs` flips it), `fetch_robots_txt` holding `format!("https://{}/robots.txt"`, `crawl_delay_secs: 0`, `max_inflight`, `--workers`; `fails = ["robots_read"]`. Alternatives: without the https clause once the probe passes; the old "unless … `Crawl-delay`" only once a probe `crawl_delay_obeyed` (not written) has seen the pause. Engine rule (`route.CONDITIONAL`, `producers`): a wording with `unless`, `when`, `only` or `if` is verified only with a run-check probe or an anchor marked `producer = true` that is not a field assignment; G1's comparison and S1's fallback default are marked. Fixture test: the setter exists and the producer passes None, so the entry is unverified; a setter marked producer still is. |
| r2-3: Scrapy bullet 4 | "Each host has its own circuit breaker: after 5 URLs on it fail every retry, it is left alone for 60 s." Two `[[figures]]` rows read the literals `DEFAULT_STAGE2_BREAKER_FAILURES = 5` and `DEFAULT_STAGE2_BREAKER_RECOVERY = 60` in `stage2_worker.py` at HEAD; both hold. |
| r2-4: the data line names the seeding flag | "… its commands were run, with seeding off, against a local 3-page site on 10 Oct 2026 (Linux x86_64)." `crawl_words` names every flag of the run check's crawl command that the printed block lacks: in words from `FLAG_WORDS`, otherwise as itself; `--data-dir` is declared immaterial (where a run writes). The printed block's flags come from one constant, `BLOCK_CRAWL_FLAGS`. Test: every flag that differs is named or declared immaterial. |
| r2-5: rust_llm_logger | "a non-buffering reverse proxy for LLM servers, in Rust. Each chunk is parsed for token counts and passed straight on, and the call is logged only after the client has its last byte." |
| r2-6: the header counts URLs | "Crawls a site and writes one line for every URL it finds." Review 1 kept the old sentence as "the best on the page" but made no case against the change; the new one is the same sentence, made true for a file that holds a line for a 404 link (`status_code` null). Desk one line, phone two. |
| r3-1: the phone sheet below a 1200 px viewport | `chart.toml` `breakpoint_px = 1199`. New HERO-COLUMN-PX (`scripts/checks/column.py`, render tier; a module has one tier, so it is not in `checks/route.py`, which is fast): GitHub's measured column table (vw − 82 under 768, vw − 370 to 1011, vw − 434 to 1279, 846 from 1280); for every viewport from 360 to 1920 it takes the sheet the README's `<source>` list serves and fails a smallest text run under 11 px. With 767 it fails 768–1175 (5.9 px at 768); with 1199 it passes. The measurement date and the table are in DESIGN.md (from `tokens.py`). |
| r3-2: the phone sheet for a 308 px image | The hero's phone sheet is 600 units wide (it was 720; `title_w` 520, right edge 568), every type token kept: 26 units are 13.3 px at 308, 14.4 at 332 (414 phone), 12.0 at 278 (360 phone). `checks/route.py`: `PHONE_SCREEN = 308`, `MIN_PX = 13`, a second floor of 11 px at 278, the sheet's width read from the report. The extra wraps (S1 three lines, the header two, the release label under its command) took the phone sheet to 1,187, 1,264 with S2 drawn; the gap from the role line to the project's name (60 → 50) and the foot (30 → 22) give back 18, so it is 1,169 today and 1,246 with S2, inside the 1,246 the reviewer set (640 px at 308). ROUTE-HEIGHT desk 620, phone 1,246. Preview: `scratchpad/r6/tools/preview_phone.mjs` sets `.md{padding:16px 41px}`; the render set adds 360 px. BREAKS row added. |
| r3-3: S1 says what the seeds buy | "your URL, plus by default URLs found without links: sitemaps, subdomains in certificate logs, Common Crawl"; the fallback "your URL, plus, if asked, URLs found without links: …". New anchor in both trees: `src/ct_log_seeder.rs` contains `format!("https://{}/", subdomain)` (sdist :327, HEAD :352, :393); `default_value = "all"` kept. Desk two lines (+28), phone three. |
| — | `stats_schema.json` admits `gate` on a route entry and `scope` on a rule record. AUDIT.md's routes and rules rows describe the new L1, M1, S1, F1, header and rule 4; §7 regenerated. DESIGN.md's paragraph on how the drawing is checked names the robots probe and the condition rule. |

### Fixes declined, and why

| Must-fix | Why not |
|---|---|
| r1-2: fix P1, take `--ignore-robots` out of the idle test, ship 0.1.4; set Rust-sitemap's About text and `README.md:25` | Work in Rust-sitemap and on PyPI under the owner's account, outside this repository and this session's credentials. The image does not go to `main` until then. Text for him, updated by review 2's header fix: About "Crawls a site and writes one line for every URL it finds."; `README.md:25` as round 5 wrote it. When 0.1.4 passes the run check, H1, the gap, the kill comment and X1 retire, and M1 prints once the idle test runs without `--ignore-robots` and the cargo gate holds, with no edit here. |
| r3-4: the GitHub bio | The owner's profile setting. The text for him: "Crawl and data infrastructure, in Python and Rust." |
| r3-1, the range 320–359 | HERO-COLUMN-PX starts at 360, the narrowest phone in the reviewer's measurements and in ROUTE-PHONE-PX's second floor. At 320–335 px (first-generation iPhone SE) the 600-unit sheet's 26-unit text is 10.3–10.9 px; holding 11 px there needs a sheet of 562 units or less, which no longer fits one screen. Recorded in `checks/column.py`. |
| r2 note: H1's "done 20 s after the lines stop"; G1's limits; resume after a kill | Not ranked by review 2, and the image already says when you are done in the tool's own words. |
| r2 table "hand-off label: keep" | Conflicts with r1-3 (owner lens), applied above. |

### Measured state of this build

- Desk sheet 571 high (607 with S2 drawn; gate 620); phone 600 × 1,169 (1,246 with S2; gate 1,246).
- `python3 -m unittest`: 310 tests, all pass (24 new in `tests/test_round6.py`).
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 3 warnings (log.shards,
  POSITION-EMPTY, LICENSE-FLAGSHIP Rust-sitemap), 0 errors; the render tier is skipped while fast fails, and run alone
  it passes (0 fail, 0 warn), HERO-COLUMN-PX included. ROUTE-PHONE-PX, ROUTE-HEIGHT, ROUTE-RELEASE, ROUTE-PAINT,
  ROUTE-ARROW, ROUTE-CODE-SPACE, ROUTE-LEFT-EDGE, ROUTE-LABEL, TYPE-CODE, HERO-SELF-TWICE, STRINGS-TWICE, FIGURES,
  NOTICE-DATE, NOTICE-AUTHOR, README-STALE and AUDIT-STALE are clean.

## Round 7

Reviews: `review-r07-1.md` (the owner's test) **8 / 10**, `review-r07-2.md` (the data engineer) **7 / 10**,
`review-r07-3.md` (the copy editor) **7 / 10**. None meets the goal. Where they conflict, review 1 (the owner's lens)
wins.

Renders: `scratchpad/r6/build/round-07/` (the standard set; the phone sheets also at 308 px; the phone page at 390 and
at 360, `page-phone-360-*.png`). `stats.json` re-read from the local trees with `scratchpad/r6/reroute7.py` (as
reroute6, plus every rule's liveness at HEAD and `repos[].ci_selection` for the two flagships; it refuses a tree at
another commit than `stats.json` names).

### What was measured first

- **The writer.** `drain_batch` (sdist `writer_thread.rs:246-276`, HEAD `:258-289`) blocks in `recv_deadline` only
  until the first event, at most `BATCH_TIMEOUT_MS` (50), then drains with `try_recv` up to `MAX_BATCH_SIZE` and
  returns. `writer_loop` never sleeps on the constant. Review 2 is right: 50 ms is the idle wait.
- **The hand-off.** `ideal-url-organizer` at `159968a`: `self.methods` in `src/main.py` has 21 keys (ast);
  `scripts/import_rust_sitemapper.py:143` runs `[str(run_sh), "--all"]`; `run.sh:42-43` maps `--all` to
  `src/main.py --full`. The 25 `method_*.py` files include four that take `PageContent`.
- **Rule 1.** `git log --reverse -S_host_breakers` on `Scrapy.git`: first commit `099dd6c`, 8 Oct 2026, his. Plain
  `git grep "class CircuitBreaker" HEAD` still finds the old anchor at HEAD (Claude's uncalled class in
  `utils/retry.py`, and `CircuitBreakerOpen`), so a liveness check on the old text would have passed; the first
  files of rules 2 and 3 (`tools/export_to_datalake.py`, `src/common/prometheus_exporter.py`) were deleted in his
  own rebuild, `1b0f502`, 5 Oct 2025, while the practice continued in other files.
- **Scrapy's CI.** `main.yml` runs `python -m pytest tests/ -m "not slow and not kafka and not performance"` in
  `Scraping_project`, and `tests/unit/test_docker_entrypoints.py` in a smoke job. Of the 1,920 test functions counted:
  16 are in collected files outside `Scraping_project/tests` (`temp_scripts/`, …), 25 are deselected by the markers
  (ast, function, class and module level). 21 `skipif`, 21 `pytest.skip()` and 18 `importorskip` are decided at run
  time. Rust-sitemap: `cargo test --all-features` and `pytest -q python/tests`, nothing left out.
- **Languages.** `main_language` over the 21 public repositories without the profile: Python 10, Swift 3,
  JavaScript 2, TypeScript 2, Rust 2, C 1, Go 1. REST's `language` was read for 4 of 22 this run, and agrees.
- **Widths.** In round 6's renders 32 code columns fit at 360 px and 36 at 390. After the fixes the desk sheet is
  571 high (unchanged), the phone sheet 600 × 1,135 (was 1,169: G1's line is gone and W1 is one line).

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1 + r2-3: code blocks fit 360 px | `checks/readme.py` `CODE_COLUMNS = 32`, the measurement (viewport, GitHub's `pre` CSS, the cut column) in the docstring. rustmapper: "# sitemap.xml, even after a kill" (32, no colon; `render_readme.stop_lines`). Scrapy: the comments move into one sentence before the block, "Run these from a clone of [Scrapy](…), in `Scraping_project` (`start.py` runs only there). `python start.py` runs all four stages; it needs docker and docker-compose and crawls a university's sample site. The last command runs only discovery, on your site." The block is six lines, longest 31. New THIS-REPO fail: no visible "this repository". |
| r1-2: Languages from the data | Inline marker `<!-- n:languages -->` filled by `render_readme.languages_line`: `[copy] languages_lead = ["Python", "Rust"]`, then every other `main_language` (profile out) by repository count, then lines: "Python, Rust; Swift, JavaScript, TypeScript, C, Go". §7 row. |
| r1-3: F1 and G1 one clause each | G1 retired; F1 is "fetches pages, fewer at once when saves average over 500 ms; queues their links to your site, its subdomains and its parent domain", scope `release`, its release anchors the union with G1's three `main.rs` anchors (the comparison marked `producer`), the 500 still `{const:THROTTLE_THRESHOLD_MS}`. PURPOSE, BREAKS and DESIGN.md say "a clause of fetch". Desk two lines, phone four, as before. Test: no step renders under another. |
| r1-4 + r3-3: rule 1, liveness, plain rules | Rule 1 anchor `{key = "breaker", repo = "Scrapy", text = "_host_breakers", author = "self"}`, cite "*Scrapy, Oct 2026: a circuit breaker for each host in stage 2.*" (`[[figures]]` row "stage 2"). New NOTICE-LIVE (`checks/notices_live.py`): each printed rule's anchor text must be in a non-documentation file at HEAD (`rules[].at_head`, `head_paths`, `proof.live_paths`). Bodies: 1 "One failing host is set aside for a minute; the rest of the crawl goes on."; 2 "Next month's question can't be known today, so the raw layer is appended to and never overwritten."; 3 "Dashboards go in version one." Test: at most one "The/A X … is …" frame, no "you cannot … you cannot". |
| r2-1: W1 without 50 ms | First wording "… every {const:BATCH_TIMEOUT_MS} ms", holding only with `writer_loop` sleeping on the constant (it does not); then "logged to disk, then saved to redb, in batches" on `fn = "drain_batch"` anchors `recv_deadline(deadline)` and `try_recv()` in both trees, order anchors kept. PURPOSE, AUDIT routes row and §7 say batches. Fixture tests for both wordings. |
| r2-2: R15 "sorted 21 ways" | New `[[figures]]` kind: `keys = "self.methods"`, `count = 21` (ast, `proof.dict_keys`), `also` literals for the importer's `--all` call and `run.sh`'s `--all)` → `main.py --full`, `handoff = true`. `handoff_words` reads only that row; the Also line keeps "25 ways" from the glob row. Tests: 2-key fixture prints "2 ways"; no `--all` call, "sorted by". |
| r2-4: the register | `audit_figures.records`: a row for every route entry whose wording reads a figure (F1, W1, H1, L1, X1, M1; definition from the anchor and the entry's `audit` note: L1's "no pause" from probe `robots_read`, X1's 50,000 from the sitemaps.org protocol), R15 from the handoff row, and rows for `ci_selection`, `license`, Languages, co-signed, "CC BY 4.0". New AUDIT-COVER (`checks/audit_cover.py`, fast): any digit in the hero's text manifest or the README's visible text without a row fails. Today none. |
| r2-5: Scrapy's test count | `tree.ci_selection` (line-level workflow read, no YAML dependency; ast markers) writes `repos[].ci_selection`, wired into `build_stats.py`; the facts line prints "1,920 tests (CI selects all but 41)". See declined for 63. |
| r2-6 + r3-7: the data line | "The [drawing](DESIGN.md) shows rustmapper 0.1.3, …", "71 of the Scrapy repository's 499" (`[copy] repo_words`), "and co-signed 1 and 30 of his own" from `repos[].coauthored.agent`, printed only when every listed repository has the count. |
| r3-1: his Scrapy, not the framework | Link line "rustmapper · PyPI · Scrapy · Email". Pick: "His **Scrapy** repository keeps the pages themselves, deduplicated and summarized, and needs Docker." Lead: "**[Scrapy](…)** is his crawl system on top of the Scrapy framework, in four stages: discovery, analysis, summaries, large documents." (`[[figures]]` "four stages", 4 `stage[0-9]/__init__.py`). Bullet 1 cut. Test: the first unlinked "Scrapy" follows "His". |
| r3-2: H1 "exits" | "{release} never exits by itself; done when it stops printing `Received work item`"; fallback "… never exits by itself, even after the last page". Desk one line, phone two (no height added). |
| r3-4: dates and units on one line | `fmt_date` joins with U+00A0; `keep_together` joins dates, "3 min", "60 s", "50,000 characters" and "16k lines of Rust" in the facts, install, rules and data blocks (code spans untouched); the two hand-typed ones in the Scrapy bullets typed with U+00A0. FIGURES and STRINGS normalize U+00A0. Test over the visible text. |
| r3-5: one spelling | "summarized" in the pick text and its `[[figures]]` row; test against -ise forms. |
| r3-6: S1 | "your URL and, by default, URLs looked up rather than followed: sitemaps, subdomains in certificate logs, Common Crawl"; fallback "… and, if asked, …". Anchors unchanged; desk two lines, phone three. |

### Fixes declined, or changed, and why

| Must-fix | Why |
|---|---|
| r2-5: "CI runs all but 63" | Printed "CI selects all but 41". The 38 skip marks are all `skipif` (ast count, on tests the markers do not deselect); a `skipif` (and `pytest.skip()`, `importorskip`) is decided on the CI machine, so counting it as not run would state a figure nobody measured. The 41 is what the workflow's own commands leave out: 25 deselected by `-m`, plus 16 tests in collected files outside `tests/`, which the reviewer's count (1,904) did not include. "Selects" is pytest's own word. |
| r1-2: an AUDIT row saying Linguist bytes | `main_language` is not Linguist's figure; it is the language with most newlines at HEAD (`tree.py`). The row says so and that REST's `language`, where read (4 of 22), agrees. |
| r1-4: "today NOTICE-LIVE fails rule 1" | A plain liveness check would pass the old anchor (the text is still at HEAD in an uncalled class); a "same file" check fails rules 2 and 3, whose first files he rebuilt on 5 Oct 2025. NOTICE-LIVE asks that the code is still there, docs excluded; the re-anchoring to `_host_breakers` is what fixes rule 1. |
| r1-1: the Scrapy sentence's wording | "runs the whole pipeline" became "runs all four stages" (review 3: "pipeline" names the framework's item pipelines), and "From a clone of …" became "Run these from a clone of …", a sentence rather than a fragment. |
| r2-6: "co-signed … of mine" | "of his own": the page speaks of him in the third person. |
| r3 note 1: `Crawl-` / `delay` | Left, as the reviewer advised: U+2011 would break copy and search for a robots.txt directive. |
| Owner, outside this repository (rounds 4 to 7) | Fix P1, take `--ignore-robots` out of the idle test, ship 0.1.4; Rust-sitemap's About text and `README.md:25`; the GitHub bio; review 3's rename of the Scrapy repository. The image does not go to `main` until 0.1.4. |

### Measured state of this build

- Desk sheet 571 high (gate 620); phone 600 × 1,135 (gate 1,246).
- `python3 -m unittest`: 337 tests, all pass (27 new in `tests/test_round7.py`).
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 3 warnings (log.shards,
  POSITION-EMPTY, LICENSE-FLAGSHIP Rust-sitemap), 0 errors; the render tier is skipped while fast fails, and run alone
  it passes (0 fail, 0 warn). AUDIT-COVER, NOTICE-LIVE, THIS-REPO, README-CODE-WIDTH (32), FIGURES, STRINGS-TWICE,
  NOTICE-DATE, NOTICE-AUTHOR, README-STALE and AUDIT-STALE are clean.

## Round 8

Reviews: `review-r08-1.md` (the owner's test) **8 / 10**, `review-r08-2.md` (the developer choosing a crawler)
**7 / 10**, `review-r08-3.md` (the historian of charts and sailing directions) **8 / 10**. None meets the goal. Where
they conflict, review 1 (the owner's lens) wins; review 3 agrees with review 1 on every shared item.

Renders: `scratchpad/r6/build/round-08/` (the standard set; the phone sheets also at 308 px; the phone page at 390 and
at 360, `page-phone-360-*.png`). `stats.json` re-read from the local trees with `scratchpad/r6/reroute8.py` (as
reroute7, plus `go_go_go` and `Ai_code_detector` for the new [[figures]] rows, `repo_first` for rule 3, and the two
new probes merged from `scratchpad/r6/rc8/steps.json`).

### What was measured first

- **The governor (review 2's finding 1 holds).** 0.1.3 `main.rs:84-150`: `current_permits = permits.available_permits()`
  (idle permits only), and a permit is taken with `try_acquire_owned()` only `if current_permits > MIN_PERMITS`
  (32). A running fetch keeps its permit; one host is capped at `max_inflight: 20` (`state.rs:285`, checked at
  `frontier.rs:655`). From 256 permits the governor can shrink the pool to about 52, never under the 20 a one-site
  crawl uses, so "fewer at once when saves average over 500 ms" is false for the crawl the header describes.
- **Two new probes, on the 0.1.3 binary the run check installed** (`rc2/work/v`). `workers_cap`: the fixture site,
  each answer held 1 s: default workers, 3 requests, at most 2 open at once; `--workers 1`, 3 requests, at most 1.
  `second_ctrl_c`: SIGINT after 15 s, a second 0.3 s later: exit 1, no `sitemap.jsonl`, no `Saved to:`; the log ends
  "Force quit requested, exiting immediately...".
- **ideal-url-organizer at `159968a`.** `self.methods` has 21 keys (methods 1-21); `List[PageContent]` is in exactly
  `method_22` to `method_25` (HTTP status, schema.org type, page authority, semantic similarity). Methods 12, 14 and
  15 read the crawl record (`content_type`, `discovered_at`, `is_crawled()`), so "from the URLs alone" is not exact.
- **Rule 3.** Scrapy's first commit `67446a4`, 25 Sep 2025 (his); `d571e6e`, 1 Oct, adds
  `src/common/prometheus_exporter.py` with `start_http_server`; `e8cbe15`, 6 Oct, adds
  `monitoring/grafana_dashboard.json` (one dashboard). 6 days, then 5.
- **Scrapy's Compose.** `start.py:25` `"local": ("docker", "docker-compose")`, checked with `shutil.which` (`:242`),
  which a shell alias does not satisfy.
- **What rustmapper sees.** 0.1.3 `Cargo.toml` has `scraper` and `html5ever` and no browser or JavaScript engine.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1 + r2-2 + r3-1: one count for ideal-url-organizer | Also line: "25 ways to sort a pile of URLs: 21 from the URLs and their crawl records (domain, crawl depth, subdomain, …), 4 more from the fetched pages." New [[figures]] rows "21 from" (`self.methods`, 21 keys, the count the image's hand-off reads) and "4 more" (new kind: `glob` + `contains = "List[PageContent]"`, 4); the "25 ways" row carries `parts = ["21 from", "4 more"]` and holds only while they add up (`proof.figure_records`). New STRINGS-COUNT (fast): a hero run "<n> ways … <repo>" needs n in that repository's README list line. The image keeps "sorted 21 ways". |
| r1-2 + r3-3: phone heading gap | `sheets/route.py` phone `head_after_title` 50 → 70. New ROUTE-HEAD-GAP (route check, read from the build report): on a phone edition the project's name must sit at least 2 × the role line's pitch (34) under its last baseline. Desk unchanged. Phone sheet 1,121 (F1 lost a line, below). |
| r1-3 + r3-4: go_go_go | "rustmapper's counterpart in Go, with the same crawl, resume and export-sitemap commands, plus optional headless-Chrome rendering and SQLite storage with full-text search." No impersonation clause. Rows at go_go_go HEAD: `Use:   "resume"` and `"export-sitemap"`, `"enable-js-rendering", false, …headless Chrome`, `"enable-sqlite", false` with `USING fts5(`. |
| r1-4 + r3-5: rule 3 | "**Measure from the start.** Metrics were exported 6 days after the first commit, and a dashboard was up 5 days after that." Cite unchanged. `{days:key}` (from `rules[].repo_first`, the earliest commit on HEAD by anyone, git) and `{days:a..b}` (between two anchors) in `proof.fill_days`; a count not computed prints "?" and fails NOTICE-DATE; two AUDIT §7 rows; AUDIT-COVER covers the filled body. |
| r1-5 + r3-6: rule 2's cite | "*Scrapy, Oct 2025: raw pages written to Delta Lake with `write_deltalake`.*" New NOTICE-CITE (fast): every printed cite is "<repo>, <Mon YYYY>: <what>."; a comma form fails. |
| r1-6 + r3-6: Ai_code_detector | "`aicd scan` scores each file of a repository for signs of AI authorship, from its comments, naming, structure and git history, and says why it flagged it." Rows at `aa7368b`: `setup.py` `aicd=ai_code_detector.aicd:main` with `aicd.py` `name="scan"`; `detector_enhanced.py` `StylometryAnalyzer(` and "Analyzing git history"; `use_explanations: bool = True`. |
| r2-1: F1 says the per-host cap | The governor wording stays first, now also on `{path = "src/main.rs", fn = "governor_task", absent = "current_permits > MIN_PERMITS"}`; the alternative that draws is "fetches up to {field:max_inflight} pages at a time from each host; queues their links to your site, its subdomains and its parent domain" (`state.rs` field, `frontier.rs` `current_inflight >= host_state.max_inflight`, the four scope anchors). Desk two lines, phone three (was four). L1 keeps the total: "It sends its requests with no pause between them, at most 256 at a time across all hosts. …" PURPOSE, BREAKS ("The per-host cap is a clause of fetch"), DESIGN.md and the AUDIT routes row say so. Fixture tests both ways. |
| r2-3: the two levers | New text entry L2, release scope, after L1: "`--workers 1` holds it to one request at a time; `--seeding-strategy none` starts from your URL and its links alone and asks no outside service about your domain." Anchors: `cli.rs` workers default 256 and seeding default all, `main.rs` `max_workers: u32::try_from(workers)`, `bfs_crawler.rs` `let max_concurrent = self.config.max_workers`, `in_flight_tasks.len() < max_concurrent` and the four `strategies.contains` lines; `runs = ["workers_cap"]`. AUDIT §7 row for the "1" (`route_rows` now takes a text entry with an `audit` note and no `{…}` figure). |
| r2-4: which Compose | Scrapy run sentence: "`python start.py` runs all four stages and crawls a university's sample site. It needs Docker and the `docker-compose` command: Docker Desktop has it; on Linux, where Docker's Compose plugin answers only to `docker compose`, install Compose standalone as well." [[figures]] row "the `docker-compose` command" on `start.py`'s `REQUIRED_TOOLS` and `shutil.which(`. |
| r2-5: what it cannot see | New text entry L3, release scope, starting its own paragraph (`para = true`, new in `data/route.py` and `render_readme.text_paragraphs`): "It reads links from the HTML a server sends; no JavaScript runs. go_go_go can render pages in headless Chrome." Anchors: `Cargo.toml` has `scraper = "` and none of chromiumoxide, headless_chrome, fantoccini, deno_core, rusty_v8. X1 follows in the same paragraph. |
| r3-2: C1's caution | "press Ctrl-C once; a second press before `Saved to:` quits without writing the file" (desk one line, phone two, as before). Head anchors in `shutdown.rs` `setup_shutdown_handler`, release anchors in the sdist's `main`: "Press Ctrl+C again to force quit", order anchors `std::process::exit(1)` before `export_to_jsonl(&path)` and that before `println!("Saved to: `; `runs = ["crawl_ctrl_c", "second_ctrl_c"]`; the old wording is the `instead`. New gate-false probe `second_ctrl_c` and `workers_cap` in `scripts/runcheck.py` (also `--probe workers_cap,second_ctrl_c`). PURPOSE C1 updated. The file is named once, by the end row. |

### Fixes declined, or changed, and why

| Must-fix | Why |
|---|---|
| r1-1: "21 from the URLs alone", "4 more from the page content" | Methods 12, 14 and 15 read the crawl record (content type, discovery time, crawl status), not the URL, and method 22 sorts by HTTP status, which is not page content. Printed "from the URLs and their crawl records" and "from the fetched pages". |
| r2-2: a separate HANDOFF-AGREES check | Folded into review 1's STRINGS-COUNT, which tests the same thing (one count across the image and the page). The 21 in the Also line reads its own [[figures]] row with the same `self.methods` count; a test asserts the two rows agree. |
| r1-4: "Scrapy exported Prometheus metrics … had Grafana dashboards" | The body would repeat the cite word for word ("Prometheus metrics, then Grafana dashboards"), and e8cbe15 adds one dashboard. Printed "Metrics were exported 6 days after the first commit, and a dashboard was up 5 days after that." Review 1's test "a body that repeats its title's key noun with no figure fails" would fail rule 2 ("Raw before clean." / "the raw layer"), which no reviewer flagged; the test asks instead that no body opens on its title's first word unless it carries a figure. |
| r2-1: L1 "It sends them with no pause, 256 at most in all." | "Them" has no antecedent in the README, where L1 follows the wheel note. Printed "It sends its requests with no pause between them, at most 256 at a time across all hosts." |
| r2-3: "`--workers 2` holds it to two requests at a time" | Printed `--workers 1` and "one request": the probe ran with 1 and saw at most one open request, so the printed figure is the one measured (Scrapy's own template is also one per domain). |
| r2-3: the probe "pass if no two requests overlap" | The probe also crawls with the default workers and passes only if the server saw two requests open at once there: a site that never overlaps cannot show a cap. |
| r2-4: "add a `docker-compose` alias first" | `start.py` finds the tool with `shutil.which` and runs `docker-compose up -d` as a subprocess; a shell alias satisfies neither. "Install Compose standalone" is Docker's documented way to get the hyphenated binary on Linux. The sentence is hand-typed prose, so its fallback is the FIGURES gate (the row fails once `start.py` stops naming `docker-compose`), not an automatic rewording. |
| r3-2: "a second before `Saved to:` …" | "A second" reads as one second. Printed "a second press before `Saved to:` …". The probe sends the first SIGINT after 15 s, not 45 s: the three pages take under a second, and the entrance crawl already covers the 45 s case. |
| tests: `all_verified` | The fixture that draws "what the sheet draws once P1 lands" now verifies the HEAD side only and keeps the release's anchors as read: P1 lands on main, and F1's governor wording waits on a new release. With every first wording forced true the phone would be 1,266 (20 over the gate); if a release ever restores the governor wording while S2 is drawn, ROUTE-HEIGHT will say so then. |
| Owner, outside this repository (rounds 4 to 8) | Fix P1, take `--ignore-robots` out of the idle test, ship 0.1.4; Rust-sitemap's LICENSE file, About text and `README.md:25`; let `start.py` accept `docker compose`; make the governor able to cut fetches in flight, or say what it does; have the first Ctrl-C say "again to quit without writing sitemap.jsonl" (C1 then falls back by itself); `resume` after a kill fails in 0.1.3 ("Database already open"). The image does not go to `main` until 0.1.4. |

### Measured state of this build

- Desk sheet 571 high (gate 620); phone 600 × 1,121 (gate 1,246). With S2 drawn: desk 607, phone 1,198.
- `python3 -m unittest`: 364 tests, all pass (27 new in `tests/test_round8.py`).
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 3 warnings (log.shards,
  POSITION-EMPTY, LICENSE-FLAGSHIP Rust-sitemap), 0 errors; the render tier is skipped while fast fails, and run alone
  it passes (0 fail, 0 warn). STRINGS-COUNT, ROUTE-HEAD-GAP, NOTICE-CITE, NOTICE-DATE (with the day counts),
  AUDIT-COVER, FIGURES (22 rows, all hold), STRINGS-TWICE, README-STALE and AUDIT-STALE are clean.

## Round 9

Reviews: `review-r09-1.md` (the owner's test) **8 / 10**, `review-r09-2.md` (the deck officer and yacht navigator)
**8 / 10**, `review-r09-3.md` (the staff engineer screening for data infrastructure) **8 / 10**. None meets the goal.
All three say the image does what the owner asked; what holds the page back is the text around it. Where the
reviews conflict, review 1 (the owner's lens) wins. Review 3 backs review 1 on every shared item.

Renders: `scratchpad/r6/build/round-09/` (the standard set, plus the phone sheets at 308 px and the phone page at
360, `page-phone-360-*.png`). The page renders now use GitHub's `sub` rule (`line-height: 0`, `bottom: -.25em`),
so the data and licence lines sit at the body's 24 px pitch, as on GitHub, not at the 27 px the old harness drew.
`stats.json` was re-read from the local trees with `scratchpad/r6/reroute9.py` (as reroute8, plus `repos[].ci.gates`
and the two new probes, merged from `scratchpad/r6/rc9/steps.json`).

### What was measured first

- **A 429 in 0.1.3 (review 2's finding 1 holds).** `--probe non200_status`, run on the 0.1.3 binary the run check
  installed: `busy.html` answers 429 with `Retry-After: 2` and links to `beyond.html`, and `gone.html` is a 404. In
  12 s: 5 requests, `busy.html` asked for once, `beyond.html` never, and both rows have `status_code` null. The code
  says why (sdist `bfs_crawler.rs` `process_url_streaming`): only `Ok(response) if … == 200` goes on to parsing;
  `Ok(_) =>` returns `Ok(Vec::new())`. The field is set only from the parse job, and neither file reads `Retry-After`.
- **How long the quiet runs.** A fetch can take up to `--timeout`, which defaults to 20 s (`cli.rs`; set on the
  reqwest client in `network.rs`). After a failure the host waits 2^failures s and is dropped at
  `MAX_FAILURES_THRESHOLD` = 3, so the longest wait is 4 s, counted in whole seconds. A host's first robots.txt
  fetch runs in the background and does not hold its URLs ("Proceed with crawling - don't block on robots.txt",
  `frontier.rs`), so it adds nothing. 20 + 4 + 1 = 25, rounded up to 30. `--probe quiet_slow_page`: `slow.html` is
  held 15 s. Two `Received work item` lines came 15.0 s apart, and 30 s after the last one, one SIGINT wrote all
  three pages with status 200.
- **What CI blocks on.** At `96e7a1a`, Scrapy's `main.yml` runs ruff, mypy, bandit and pytest as plain steps in
  `test`, and pytest again in `entrypoint-smoke`. At `32c2651`, Rust-sitemap's `ci.yml` makes only `cargo test`
  (Test), `pytest` (Python wrapper) and `cargo fmt --all -- --check` (Format) able to fail the run. Clippy ends in
  `|| true`. Security Audit is `continue-on-error` at both the job and the step. Benchmark ends in `|| echo`.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1 + r3-3: the cautions as one short list | Under the wheel note: "Before you run it:" (`[route.rustmapper] list_lead`) and the text entries marked `item = true`, one Markdown item each (`render_readme.text_blocks`). L1 now carries its lever: "It sends requests with no pause between them, up to 256 at a time across all hosts. `--workers 1` sends one at a time." (`runs = ["workers_cap"]`, L2's workers anchors). The robots clause is its own entry, L4, on `robots_read` (failed), with the same alternatives as before. L2: "By default it asks crt.sh and Common Crawl about your domain. `--seeding-strategy none` asks no one." It has new anchors on `ct_log_seeder.rs` `"https://crt.sh/?q=%.{}` and the Common Crawl index URL. L3: "It reads links from the HTML a server sends, and no JavaScript runs. go_go_go can render pages in headless Chrome." X1 as before. A retired entry drops its item, and with no item left the lead-in goes too. New README-CAUTIONS (fast): at most one prose paragraph after the code block, one list, at most 6 items, each at most 25 words. On the 390 phone the three paragraphs (about 21 lines) become six short items. |
| r1-2 + r3-5: no to-do line; the link heads the facts line | The about line ("the Python API, built with maturin, is on main and not yet released") is gone, and so is its gate `python_api`. The facts line reads "**[rustmapper](…)** · *on main at `32c2651`: built on … · CI passed 7 Oct 2026: tests, rustfmt · 16k lines of Rust*" (`FACTS_LINK`). Once a wheel ships the module, the about block prints "`import rustmapper` works after `pip install`." New README-TODO (fast): no visible sentence says "not (yet) released" without a code span the reader can use. |
| r1-3 + r3-1: the Scrapy run sentence agrees with its `cd` | "Run these from the folder you cloned [Scrapy](…) into; `start.py` runs only inside `Scraping_project`. `python start.py` runs all four stages and crawls a university's sample site. It needs Docker and the `docker-compose` command (Docker Desktop has it; on Linux, install Compose standalone). The last command runs only discovery, on your site." New README-CD (fast): a block whose first line is `cd <path>` may not follow a sentence that says to run it "in" that folder. |
| r3-2: what Scrapy does before how to run it | Scrapy now reads: sentence, facts line, the three bullets (Delta Lake raw layer; MinHash and stage 4; Prometheus, breakers, Compose and Helm), then the run sentence, the code block and the Grafana note. The order test has "- Raw pages land in Delta Lake" between the facts block and "Run these from". No words were added. |
| r1-4 + r3-6: S1 with a verb | "starts from your URL; by default also from sitemaps, certificate logs and Common Crawl"; the `instead` reads "if asked, also from …". It is two lines on the phone (was three) and one on the desk (was two). Heights: desk 571 → 543, phone 1,121 → 1,087. |
| r2-1: what `sitemap.jsonl` cannot tell you | New text entry X2, release scope, the last item: "0.1.3 gives no `status_code` to a page that answers 404, 429 or 503, never asks for it again, and follows none of its links." (24 words). Anchors: `process_url_streaming` `Ok(response) if response.status().as_u16() == 200` before `Ok(_) =>`, and `result: Ok(Vec::new())`; `status_code: job.status_code`; no `Retry-After` in `bfs_crawler.rs` or `frontier.rs`; no `429` in `bfs_crawler.rs`. `runs = ["non200_status"]`, and an empty `instead` on `fails = ["non200_status"]` retires it. New gate-false probe `non200_status` (`tests/fixtures/status-site/`). AUDIT §7 row and §2 text-entry note. |
| r2-2: H1's clearing mark has its number | "{release} never exits by itself; done once `Received work item` is quiet for {quiet} s". `{quiet}` comes from `data/route.py` `quiet_secs` on the release's value anchors `arg:timeout` (`cli.rs` block Crawl) and `const:MAX_FAILURES_THRESHOLD`. Order and meaning anchors: `network.rs` `.timeout(Duration::from_secs(timeout_secs))`, `record_failure` `2_u32.pow(self.failures.min(8))` and `is_permanently_failed`. Today the value is 30. A probe that records `quiet_secs` must have waited at least that long (`run_missing`), or H1 falls back to "…, even after the last page". New probe `quiet_slow_page`, added to H1's `runs`. Desk one line, phone two. PURPOSE H1 updated. AUDIT §7 defines `{quiet}`. |
| r2-3: the alt text | "How to install Ben Russell's crawler rustmapper, what it does with each page, and how to stop it. It loops until one Ctrl-C writes data/sitemap.jsonl." (25 words). T-ALT asserts "How to install". |
| r3-4: the facts lines name the CI gates | New `repos[].ci.gates` (`data/tree.py` `ci_gates_at`, called by `build_stats.py`; schema; AUDIT §2 row and §7 row). It reads the workflow named `ci.workflow` at `ci.head_sha` with a line reader. A step counts only when its job passed in that run, neither it nor its job has `continue-on-error: true`, it does not end in `\|\| true`, `\|\| :` or `\|\| echo`, and it does not follow a `set +e`. Prints "CI passed 8 Oct 2026: tests, ruff, mypy, bandit" (Scrapy) and "CI passed 7 Oct 2026: tests, rustfmt" (rustmapper). With no workflow read, the old wording stays and CI-GATES warns. Fixture tests: a `ci.yml` with clippy `\|\| true`, bench `\|\| echo` and a continue-on-error audit gives `["tests", "rustfmt"]`, and a Scrapy-like file gives four gates. |
| r3-7: the review renders use GitHub's `sub` rule | `scratchpad/r6/tools/preview*.mjs` and `scratchpad/tools/preview*.mjs`: `sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}sub{bottom:-.25em}`. Measured on `page-phone-6.png`: the data line's pitch is now 48 px at 2x, the same as the body text. |

### Fixes declined, or changed, and why

| Must-fix | Why |
|---|---|
| r1-1: the lead-in "Before you point it at a site you don't run:" | The list also holds what it cannot see (L3), the single sitemap file (X1) and what the file leaves out (X2). None of those is about someone else's site, and a lead-in should introduce every item. The page prints "Before you run it:". |
| r1-1: "list ≤ 5 items" | The list has six items, because X2 (review 2) is the sixth. The cap is 6, inside the 2 to 7 of the Microsoft guide that review 1 cites. Every item stays under 25 words. Merging X2 into X1 would have broken that limit, and dropping X1 would cut a true caution, which review 1 said none should be. |
| r1-4: S1 "…, subdomains in certificate logs and Common Crawl" | At that length the phone row stays three lines (balanced wrap, measured 1,121), not the two review 1 expected. "subdomains in" is cut: "…, certificate logs and Common Crawl". That gives two phone lines and one desk line. The L2 item names crt.sh for anyone who wants the source. |
| r2-1: X2's words ("records a status only for a page that answers 200: …") | That wording is 32 words. As a list item it is "gives no `status_code` to a page that answers 404, 429 or 503, never asks for it again, and follows none of its links" (24 words). It names the field the image shows. |
| r2-2: "widen the quiet_after_last_page probe" | It is a separate probe, `quiet_slow_page`, with its own fixture (`tests/fixtures/slow-site/`). `quiet_after_last_page` reads the `ends_by_itself` run, whose three-page fixture the entrance steps and `check_jsonl` share, and a held page there would slow every entrance check. H1 needs both probes. |
| r2-2: "change H1 and its first instead" | Only H1's own wording changes. The first `instead` is the fallback for a run check without the slow-page probe. If it carried a quiet mark with no number, it would bring back exactly what review 2 asked to remove, so it keeps the cause alone. |
| Owner, outside this repository (rounds 4 to 9) | Carried: fix P1, ship 0.1.4, commit Rust-sitemap's LICENSE, let `start.py` accept `docker compose`, fix `resume` after a kill. New this round: seed crt.sh and Common Crawl with `get_registrable_domain`, not `get_root_domain` (review 1); record every response's status and back off on 429/503 the way the seeders do (review 2); `cargo update` for the 24 advisories OSV lists, a blocking `cargo audit`, `clippy -Dwarnings`, and deleting the Benchmark job (review 3). With those done, the facts line prints "tests, rustfmt, clippy, cargo audit" by itself. Also new: `check_archived_root` in WAL replay, and the `crc32c` comment in `wal.rs` (review 3). |

### Measured state of this build

- Desk sheet 543 high (gate 620); phone 600 × 1,087 (gate 1,246). With S2 drawn: desk 579, phone 1,164.
- `python3 -m unittest`: 385 tests, all pass (21 new in `tests/test_round9.py`).
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 3 warnings (log.shards,
  POSITION-EMPTY, LICENSE-FLAGSHIP Rust-sitemap), 0 errors. The render tier is skipped while fast fails; run alone
  it passes (0 fail, 0 warn). README-CAUTIONS, README-CD, README-TODO, CI-GATES, STRINGS-TWICE, STRINGS-COUNT,
  FIGURES, AUDIT-COVER, README-STALE and AUDIT-STALE are clean.

## Round 10

Reviews: `review-r10-1.md` (the owner's test) **8 / 10**, `review-r10-2.md` (information design and cartography)
**8 / 10**, `review-r10-3.md` (the systems engineer) **8 / 10**. None meets the goal. All three say the image is the
right picture. What holds the page back is text that says something the code does not do (review 1), a stop rule
that lives only in an image of text (review 2), and a stop rule whose clock starts too early (review 3). The reviews
do not conflict. Review 3 sets the words for review 2's code-block fix, and the owner's review is followed where it
gives wording.

Renders: `scratchpad/r6/build/round-10/` (the standard set, plus the phone sheets at 308 px and the phone page at
360, `page-phone-360-*.png`). `stats.json` was re-read from the local trees with `scratchpad/r6/reroute10.py`
(as reroute9, no new probes).

### What was measured first

- **What `python start.py` loads (review 1).** At `96e7a1a`, `start.py` runs `docker-compose up -d` and calls
  `cli.py reset` only `if args.reset_delta:`. The scout spider takes `-a start_urls` or the Delta table
  `seed_urls`, and `_load_seed_urls` returns `[]` when the table is missing. `cli.py reset` reads
  `data/raw/uconn_urls.csv` with `pd.read_csv(header=None)`. The file has 143,218 non-blank lines, but 10 quoted
  fields never close on their own line and each swallows the next one, so pandas (and Python's csv module, which
  gives the same rows) loads **143,208** rows. Of those, **134,807** have a `urlsplit().hostname` of `uconn.edu`
  or a subdomain of it. The review's 143,218 and 134,745 counted lines, not the rows the code loads. The page
  prints the loaded rows.
- **Where flags split on a phone (review 2).** The new `render.mjs wrap` measures each inline code span character
  by character in Chromium at 320, 360, 375, 390, 412 and 430 px, with 16 px and 41 px side padding. With the round 9
  joins, `--workers 1` splits as `--` | `workers 1` (at 360 and 412), and `--seeding-strategy none` splits as
  `--seeding-` | `strategy none` (at 320 to 430). The new Scrapy sentence's `--reset-delta` split as `--reset-` |
  `delta` at 320, 360, 390 and 430. With each flag starting its own line, nothing splits at any of those widths.
- **H1's new words on the phone.** "…done once `Received work item` lines stop for 30 s" stays two lines at 600
  units (the dotted box holds it at 390 and at 308). Heights are unchanged: desk 543, phone 1,087.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1: the Scrapy run sentence says what `start.py` does | "Run these from the folder you cloned [Scrapy](…) into. `python start.py` starts PostgreSQL, Redis, Grafana and a worker for each of the four stages. It needs Docker and the `docker-compose` command (Docker Desktop has it; on Linux, install Compose standalone). It loads no seeds by default.<br>`--reset-delta` loads 143,208 bundled URLs, 134,807 of them on uconn.edu. The last command crawls your site." New `[[figures]]` rows: "a worker for each of the four stages" (`docker-compose.yml` has `stage1-worker:` to `stage4-worker:`, `postgres:`, `redis:`, `grafana:`; `start.py` runs `("docker-compose", "up", "-d")`); "It loads no seeds by default." (`start.py` `if args.reset_delta:`, `LOCAL_SEED_FILE`, the `cli.py` `reset` call; `base_spider.py` `or self._load_seed_urls()` and `return []`; `cli.py` `pd.read_csv(csv_path, header=None, names=["url"])`); "143,208" and "134,807 of them on uconn.edu" (new kind `csv_rows`, with `host`, in `data/proof.py`). FIGURES now also fails a CLAIMS phrase ("sample site") that no holding row's text contains. AUDIT §2 and §7 rows. |
| r1-2: the list names the release it describes | `list_lead = "Before you run {release}:"`, filled in `render_readme.text_blocks`, prints "Before you run 0.1.3:". L4, X1 and X2 (and L4's alternative) start "It …". The image's H1 keeps its own "0.1.3". README-CAUTIONS: if any drawn list entry has `scope = "release"`, the lead must name the release and no item may start with it (`checks/readme.py` `cautions_scope`). AUDIT §7 row for the lead. |
| r2-1 + r3-1: the stop rule in the code block | `render_readme.stop_lines` prints `# 0.1.3 runs until stopped: when` / `# "Received work item" stops` / `# for 30 s, then Ctrl-C once` (32, 28 and 28 columns), filled with `edition.version` and H1's `quiet` (now carried by `route.resolve`), only while H1 is drawn with its number. H1 drawn without the number: the old line. H1 retired: no stop line. "received work item" is in STRINGS-TWICE's allowlist, with the reason. Phone cost: two code lines, about 48 px at 390. AUDIT §7 row. |
| r3-1: H1's clock starts once the lines stop | "{release} never exits by itself; done once `Received work item` lines stop for {quiet} s". New release anchor: `src/main.rs` has `crawler.initialize(&seeding_strategy).await?` before `process_incoming_urls(`. A fixture with the order reversed falls back to "…, even after the last page". PURPOSE H1 updated. |
| r3-2: the scope lever, the 7th item | L5, after L2: "From `www.<site>` it skips sibling hosts such as `blog.`, even ones crt.sh lists. Start at the bare domain to take them all." (22 words). Its anchors are the same in both trees: `is_same_domain`'s two branches, `add_url_to_local_queue_unchecked`'s `if !Self::is_same_domain(&url_domain, start_url_domain)`, `get_root_domain(&start_url_domain)`, and the crt.sh query. An empty alternative retires it when any anchor goes. `LIST_MAX_ITEMS` and the README-CAUTIONS cap go from 6 to 7. |
| r2-2: each lever starts its own line | `render_readme.lever_line`: where an item's second sentence opens with a code span, the two are joined by `<br>`. New render-tier check FLAG-WRAP (`checks/wrap.py`, `render.mjs wrap`): no inline code that begins with "-" may wrap before its first space, at 320 to 430 px with 16 and 41 px padding, in any paragraph or list item of the visible prose. Measured clean today, and it fails the round 9 joins. |

### Fixes declined, or changed, and why

| Must-fix | Why |
|---|---|
| r1-1: "143,218 bundled URLs, 134,745 of them on uconn.edu" | Those count the file's lines. `cli.py reset` loads 143,208 rows, because 10 quoted fields span two lines, and 134,807 of the rows it loads are on uconn.edu. The figure the reader acts on is what the command loads, and the `csv_rows` row checks that. |
| r1-1: "It loads no seeds unless you add `--reset-delta`, which loads …" | In that position `--reset-delta` splits as `--reset-` / `delta` at four phone widths (the same fault as review 2's must-fix 2). So the sentence ends before the flag: "It loads no seeds by default.<br>`--reset-delta` loads …". It has the same facts and one more line break, and the flag starts a line. FLAG-WRAP checks the whole prose, not only the list, so a flag can't split anywhere on the page. |
| r1-1: "a strings check" for "sample site" | It is in FIGURES (`CLAIMS`), next to the rule for numbers, because the check is the same: visible prose needs a holding `[[figures]]` row. |
| r2-1 / r3-1: `# 0.1.3 runs until stopped: once` … `# for 30 s, press Ctrl-C once` | STRINGS-TWICE fails "for 30 s press ctrl-c once": that is the image's H1 and C1 rows read in order, a five-word run. The comment says the rule, and the image keeps the caution about a second press. The lines read "…: when" / "… stops" / "# for 30 s, then Ctrl-C once", which also avoids "once … once". |
| r3-2: "release and HEAD scope" | L5 is scope "both", with the same anchors on both sides, because it holds on main too (with seeding asked for). It is printed under "Before you run 0.1.3:", which stays true. It retires instead of failing when an anchor goes, as review 3 asked ("Retire the item if any of them goes"). |
| r2-2: "a render-tier check in the phone harness" | The scratch harness is not part of the repository. The check runs through `scripts/render.mjs wrap` in the render tier, with the CSS and paddings of review 2's `wrap.mjs`. |
| Owner, outside this repository | Carried: fix P1 and ship 0.1.4 (H1, four list items and M1 retire by themselves), commit Rust-sitemap's LICENSE, let `start.py` accept `docker compose`, fix `resume` after a kill, seed with `get_registrable_domain`, record statuses and back off on 429/503, `cargo audit` and `clippy -Dwarnings` as blocking. New this round: move Scrapy's UConn defaults (`config.yml` `allowed_domains`, the seed file) to a named profile, and have `--reset-delta` without a seed file load nothing (review 1). Watch `docker-compose ps` on a seeded clone for an hour, because `restart: unless-stopped` on `scraper` may rerun the 50-item pipeline (review 1). Have 0.1.4 print a line when seeding ends and crawling starts (review 3). |

### Measured state of this build

- Desk sheet 543 high (gate 620); phone 600 × 1,087 (gate 1,246). Neither changed this round.
- Page: desk 2,737 px at 1,280 (was 2,617); phone 5,172 CSS px at 390 (was 5,004), with two stop lines, the 7th
  item and the two `<br>` levers.
- `python3 -m unittest`: 406 tests, all pass (21 new in `tests/test_round10.py`, one of them a Chromium render).
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 3 warnings (log.shards,
  POSITION-EMPTY, LICENSE-FLAGSHIP Rust-sitemap), 0 errors. The render tier is skipped while fast fails. Run alone,
  it passes (0 fail, 0 warn), FLAG-WRAP included. README-CAUTIONS, FIGURES, STRINGS-TWICE, AUDIT-COVER,
  README-STALE and AUDIT-STALE are clean.

## Round 11

Reviews: `review-r11-1.md` (the owner) **9 / 10**, `review-r11-2.md` (the phone-first student) **8 / 10**,
`review-r11-3.md` (the data engineer) **8 / 10**. None meets the goal yet. All three say the image is the right
picture. What is left: three blocks at the bottom of the page that do not earn their place (review 1), a screenshot
that gives the install but not the command, and cautions printed after the command they qualify (review 2), and
figures that hold their definition but not what a reader checks them against (review 3). The reviews do not
conflict. Review 3 builds on review 1's cuts, and every must-fix is applied.

Renders: `scratchpad/r6/build/round-11/` (the standard set, plus the phone sheets at 308 px and the phone page at
360, `page-phone-360-*.png`). `stats.json` was re-read from the local trees with `scratchpad/r6/reroute11.py`, and
the two changed probes were re-run on the installed 0.1.3 binary (`scratchpad/r6/rc11/steps.json`) and merged.

### What was measured first

- **The blank rows (review 3).** `runcheck.py --probe non200_status` on the extended fixture, `--timeout 3`: 8
  requests; busy.html (429), gone.html (404), err (500), feed (200, `application/json`) and hang.html (held 8 s)
  were each asked for once, beyond.html never, and all five rows have `status_code` and `crawled_at` null. The
  sdist agrees: `process_url_streaming` returns early for a non-HTML 200 (`is_html_content_type(ct)`), and
  `handle_crawl_error` treats a timeout as transient (`false // Don't block host for transient errors`).
- **The permit wait (review 3).** `bfs_crawler.rs:757` wraps `network_permits.acquire_owned()` in
  `tokio::time::timeout(Duration::from_secs(30), …)`, after the `Received work item` line. 30 + 20 + 4 + 1 = 55,
  rounded up to 60. `--probe quiet_slow_page` with `QUIET_BOUND = 60`: slow.html held 15 s, SIGINT 60 s after the
  last work-item line, 3 of 3 pages written, exit 0.
- **The command in the image (review 2).** S1 grows as review 2 said: desk 543 to 571 (gate 620), phone 1,087 to
  1,121 (gate 1,246). `rust_sitemap crawl` is drawn in the mono face (role `machine`), as `Received work item` is.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1: cut rule 4 | `[[notices]]` n = 4 removed; `NOTICES_ON_PAGE`, `checks/notices.py` and `checks/notices_live.py` print and check rules 1 to 3; `rules[]` has no `urlparse` record; AUDIT §2 says why. The `RuleFour` tests now test the `author = "self"` scope on rule 1 (`_host_breakers`). |
| r1-2: the breaker once, in rule 1 | Rule 1: "When 5 URLs on one host fail every retry, that host is left alone for 60 s; the rest of the crawl goes on." Scrapy bullet 3: "Prometheus metrics on Grafana dashboards. Docker Compose and a Helm chart for Kubernetes." The `[[figures]]` rows are "5 URLs on one host" (adds `_host_breakers`) and "60 s", both `block = "notices"`. FIGURES now reads the printed rules' bodies: a number there needs a holding row, and a notices row must be in a printed rule. Test: "circuit breaker" or "left alone" is in one block of the visible prose. |
| r1-3: excel-and-vba bare | Moved to the "Also:" line in `<details>`, after Course_crusader. 10 described + 5 bare = 15. |
| r2-1: the command in the image | S1: "`{script} crawl` starts from your URL; by default also from sitemaps, certificate logs and Common Crawl". `{script}` is the sheet's existing placeholder, filled by `route.command_name(edition.scripts, project)`, the same call as the code block, so it prints `rust_sitemap` now and `rustmapper` once a release ships that script. New release anchor `src/cli.rs` block `Commands` has `Crawl {`, and `runs = ["crawl_help"]`. Without the probe, the two old wordings (no command) are the 3rd and 4th alternatives. |
| r2-2: conditions before the commands | `install_block` returns the wheel note and "Before you run 0.1.3:" with its seven items, then the fence. README-CAUTIONS reads the block's prose around the code, not after it. |
| r2-3: the two comments apart | `stop_lines` puts a blank line before `# sitemap.xml, even after a kill` when stop lines are above it. |
| r3-1: what a blank row means | X2: "Only HTML pages that answer 200 get a `status_code`. An error, a timeout or a non-HTML 200 is left blank, `crawled_at` too, and never retried." (25 words). New release anchors `handle_crawl_error` "false // Don't block host for transient errors" and `process_url_streaming` "is_html_content_type(ct)"; `instead = ""` on `fails = ["non200_status"]` kept. Fixture: `hang.html` and links to `err`, `feed`, `hang.html`; the server answers `/err` 500 and `/feed` JSON 200 and holds `hang.html` 8 s, and logs each request as it arrives. `status_verdict` checks all five rows (`status_code` and `crawled_at` null, asked for once). AUDIT §7 X2 row. |
| r3-2: the permit wait in the quiet | New value kind `wait` (`route.wait_value`: the seconds of a tokio timeout around a future). H1 anchor `{fn = "process_url_streaming", wait = "network_permits.acquire_owned()"}`; `QUIET_FROM` and `quiet_secs(timeout, threshold, permit)`: 60. Without the anchor, H1 falls back to "…, even after the last page". Image: "…lines stop for 60 s"; code block: "# for 60 s, then Ctrl-C once". `QUIET_BOUND = 60`, `QUIET_LIMIT = 180`. H1's audit note and PURPOSE updated. |
| r3-3: the unit | "176 test functions" and "1,920 test functions (CI selects all but 41)". AUDIT §7's facts row says the CI logs count parametrized cases (Scrapy 3,075 on 8 Oct 2026) and the lib and bin targets apart (Rust-sitemap 135 + 160), and that the page counts functions. |
| r3-4: one count of the sorts | Also line: "**ideal-url-organizer** — 21 ways to sort a pile of URLs from their crawl records (domain, crawl depth, subdomain, …)." `[[figures]]` "25 ways", "21 from" and "4 more" removed; the hand-off row "21 ways" covers the Also line too, and AUDIT §7 says so. |
| r3-5: the register lists what is drawn | `route.resolve` records which wording it drew (`wording`). `audit_figures.route_rows(cfg, stats)` prints the drawn wording's figures and lists the others as "drawn instead when their anchors and probes hold"; a drawn wording with no figure, or a retired one, gets no row. AUDIT-STALE and AUDIT-COVER pass `ctx.stats`; `audit_figures.py` reads `assets/stats.json` (`--stats`). Today F1 prints `{field:max_inflight}` only, and W1 and M1 have no row. |

### Fixes declined, or changed, and why

| Must-fix | Why |
|---|---|
| r2-1: a new `{cmd}` placeholder in `scripts/data/route.py` | The sheet already fills `{script}` with `command_name(edition.scripts, project)` after the route is resolved (`sheets/route.py` `plan`). A second name for the same value would be two copies that can drift. Same behaviour, same function. With no scripts the sheet raises before anything is drawn, as it did. |
| r1-2: the row "5 URLs" | FIGURES also counts number words, and "on one host" carries "one". The row is "5 URLs on one host", with `_host_breakers` added as a literal, so "one host" rests on the per-host breakers in the code too. |
| r3-5: "drawn instead when …" per wording | The other wordings' figures are listed together after the drawn one; the conditions are their anchors and probes, which the entry's own chart.toml block states. |
| Owner, outside this repository | Carried: ship 0.1.4 (P1 and its test, the LICENSE `license-files` names, `[project.scripts]` with `rustmapper`, which also turns S1's command into `rustmapper`); record every response's status in 0.1.4 (send `CrawlAttemptFact` from the `Ok(_)` and `Err` branches) so X2 retires and ideal-url-organizer's method 15 counts right; Scrapy's UConn defaults into a named profile; `start.py` accepting `docker compose`; `resume` after a kill; registrable-domain seeding; back-off on 429/503; `cargo audit` and `clippy -Dwarnings` as blocking. New this round: decide at the end of October whether to ship the image with S2 left out if 0.1.4 is not out (review 1); compare `urlsplit(...).hostname` and the port, not raw `netloc`, in ideal-url-organizer's `web_crawler.py:296, :309`, with a test for `:443`, a login and a capital letter (review 1); set the GitHub bio to "Crawl and data infrastructure. Python and Rust." and open the profile once in the GitHub iOS and Android apps to see which edition they show (review 2). |

### Measured state of this build

- Desk sheet 571 high (gate 620); phone 600 × 1,121 (gate 1,246).
- Page: desk 2,710 px at 1,280 (was 2,737); phone 4,997 CSS px at 390 (was 5,172).
- `python3 -m unittest`: 424 tests, all pass (18 new in `tests/test_round11.py`).
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 3 warnings (log.shards,
  POSITION-EMPTY, LICENSE-FLAGSHIP Rust-sitemap), 0 errors. The render tier is skipped while fast fails. Run alone,
  it passes (0 fail, 0 warn). README-CAUTIONS, FIGURES, STRINGS-TWICE, AUDIT-COVER, README-STALE and AUDIT-STALE
  are clean.

## Round 12

Reviews: `review-r12-1.md` (the owner) **9 / 10**, `review-r12-2.md` (the copy editor) **8 / 10**,
`review-r12-3.md` (a developer choosing between rustmapper and Scrapy) **8 / 10**. None meets the goal yet. All three
say the image is the right picture and should not change. What is left: on an iPad held sideways or a laptop window
under 1,200 px the picture was a two-screen poster (review 1); the one page that explains the drawing still talked in
the theme's words and described marks that are not drawn (review 2); and the page said nothing about redirects, where
0.1.3 gets its list wrong and one caution was false (review 3). One conflict: review 3 kept the spider-name sentence
that review 1 cut. The owner's review wins; review 3's arrival sentence is added without it.

Renders: `scratchpad/r6/build/round-12/` (the standard set, plus `sheet-mid-day-746.png` and
`sheet-mid-night-746.png`, the mid sheets as an iPad Air shows them, and `page-1180-1.png` and `page-900-1.png`, the
first screen of the README at a 1,180 px and a 900 px viewport: `scratchpad/r6/tools/preview_mid.mjs`, the column
from `checks/column.py`). `stats.json` was re-read from the local trees with `scratchpad/r6/reroute12.py`, and the new
probe was run on the installed 0.1.3 binary (`scratchpad/r6/rc12/steps.json`) and merged.

### What was measured first

- **The drawn height (review 1).** From `checks/column.py`'s table and the built sheets: the phone sheet (600 x
  1,121) is drawn 900 px tall at a 482 px column, so 851 is the last viewport it may serve; at 852 an 820-unit sheet's
  19-unit text is 11.2 px (the widest that holds 11 px there is 832 units). The old serving fails HERO-COLUMN-PX's new
  height rule at 852 to 1,199 (348 viewports, up to 1,429 px).
- **Redirects (review 3).** `runcheck.py --probe redirect_kept` on the new fixture `tests/fixtures/redirect-site/`
  (`/old` 301 to `/new.html`; `/dir` 301 to `/dir/`, which links `child.html`; `canon.html` noindex with a canonical
  link): 8 requests; `/old` written as url `/old`, `status_code` 200, title "New"; `/child.html` asked for once,
  `/dir/child.html` never. `export-sitemap` then wrote one file of 5 `<loc>`, `/old` and `canon.html` among them.
  The sdist agrees: `effective_base = base_href.as_deref().unwrap_or(&job_url_clone)`, no `.url()` in
  `bfs_crawler.rs` or `network.rs`, no redirect policy, and the export keeps `node.status_code == Some(200)` with no
  canonical or noindex test. HEAD has the same base (`&job.url`) and skips canonicalized pages.
- **Where Scrapy's output lands (review 3).** `docker-compose.yml` sets `DELTA_LAKE_PATH=/data/delta` and mounts
  `./data:/data`; `docs/guides/DATA_USAGE.md` lists the tables. There are several tables per stage, not one, so the
  sentence says "Delta tables under `data/delta/`".

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1: a mid edition | `edition.py` editions `mid-day`, `mid-night` (scale `mid`, 820 wide); `tokens.py` `_MID` (the desk roles at desk sizes) and `FLOORS["mid"]`; `sheets/route.py` `SIZES["mid"]`, `EDITIONS`, `L["mid"]` (the phone's stacked order at the desk's spacing, name at 68), and a BREAKS row. The sheet is 820 x 707: 416 px tall at 852, 643 px at an iPad Air's 1,180, 660 px at 1,199 (was 1,394 and 1,429). `render_readme.py` serves `(min-width: 852px) and (max-width: 1199px)` with and without `prefers-color-scheme: dark` ahead of the phone sources, now `(max-width: 851px)`; `chart.toml` `mid_from_px = 852`. HERO-COLUMN-PX reads which sheet each viewport is served from the sources' own min and max widths, and also fails any viewport from 768 to 1,919 where that sheet is drawn over 900 px; `column.derive()` gives 851 and 832 from the table and the built sheets, and the tests hold `mid_from_px` and 820 to them. ROUTE-HEIGHT has a mid limit (964 units, 900 px at 1,199), and ROUTE-HEAD-GAP runs on the mid sheets. `publish_chart.py` refuses a set that lacks a file the README's `<picture>` names. Every sheet test (T-NOSIZE, T-SAME, T-PURPOSE, words, bounds, contrast) runs on the mid editions. |
| r1-2: no "resume" | go_go_go line: "with the same crawl and export-sitemap commands"; the `[[figures]]` row checks `crawl.go` `Use: "crawl"` and `export.go`. New README-SUBCOMMAND: a sentence that names rustmapper and a subcommand whose run-check probe failed (`resume` and `resume_after_kill`) fails. |
| r1-3: the spider-name sentence | Cut. |
| r2-1: DESIGN.md | Regenerated from `tokens.py --md` and rewritten there: the maintainer note in an HTML comment, "# How the picture is drawn", a 118-word opening written from the drawn route (`tokens.idea`: the rows' own first clauses through `sheets/route.py` `plan`, so a reworded row rewrites it; the old generator put back the retired 500 ms governor), the run check in one sentence, Editions with the mid sheet and the serving numbers read from `chart.toml` and the checks, the Actions playbook with "data step" and "the edition drawn from them". "Honesty conventions" and "Motion" are gone. The tables list only what the hero draws with (paper, ink, ink2, muted, flare, accent; PEN, LINE, BRUSH; DANGER; display, label, project, machine at desk, mid and phone sizes), each with its use. New fast check DESIGN-FRESH (`checks/design.py`): DESIGN.md must equal `tokens.py --md`, and its prose outside code and comments may hold no T-WORDS word and none of ship's, islands, lateral, soundings, unsurveyed, pecked, datum, survey. The old file fails it on ten words. The weekly workflow regenerates DESIGN.md after the README and commits it. |
| r2-2: C1's colon | "press Ctrl-C once; a second press before the `Saved to` line quits without writing the file". The anchors still test `println!("Saved to: `. Desk one line; phone still two (1,121 units). |
| r2-3: "when", not "once" | H1: "… done when `Received work item` lines stop for 60 s". Test: "once" is C1's alone among the drawn rows. STRINGS-TWICE clean. |
| r2-4: Scrapy bullet 2 | "Repeat URLs are dropped by their hash, near-duplicate pages by MinHash. In stage 3 a page's summary is its first five sentences; …". `[[figures]]` row "first five sentences" on `constants.py` `"extractive_max_sentences": 5` and the two `stage3_worker.py` lines that use it. |
| r2-5: the fold label | "15 more repositories: scrapers and data tools, Swift apps, games, a C game engine". Test: the fold's 15 links match a group table, and the label leads with the largest group (6). |
| r2-6: rule 3's title | "Measure in week one."; body unchanged. |
| r3-1: redirects | X1: "Its `sitemap.xml` is every page with `status_code` 200, in one file; the format allows 50,000 URLs per file. It keeps `noindex` and canonicalized pages." (release scope; anchors `node.status_code == Some(200)`, no `canonical`, no `noindex` in `run_export_sitemap_command`; probe `sitemap_keeps_noindex`). X2: "Only HTML pages that answer 200, redirected or not, get a `status_code`. Errors, timeouts and non-HTML 200s are left blank, `crawled_at` too, never retried." (adds probe `redirect_kept`). New X3 (both trees): "After a redirect it keeps the old address and reads the page's links from it: if `/docs` redirects to `/docs/`, `a.html` is fetched as `/a.html`." (anchors the `effective_base` line in each tree, no `.url()` in `bfs_crawler.rs` and `network.rs`, no `redirect::Policy`; retires when the probe fails). `runcheck.py` probe `redirect_kept` (two steps), fixture, verdict functions and tests; `LIST_MAX_ITEMS` 8; AUDIT §2 and §7 rows. |
| r3-2: Scrapy's arrival | "Grafana opens on `localhost:3000`. What it writes lands in Delta tables under `data/delta/`; [DATA_USAGE.md](…/Scraping_project/docs/guides/DATA_USAGE.md) lists them and shows how to read or export them." `[[figures]]` row on `DELTA_LAKE_PATH=/data/delta`, `./data:/data`, `delta.py` and the guide's `python cli.py export`. |

### Fixes declined, or changed, and why

| Must-fix | Why |
|---|---|
| r3-2: keep "Spiders run by name (`scout`), not by file name" | Conflicts with r1-3; the owner's review wins. The only spider command on the page is already right, and Scrapy's README warns where you would go wrong. |
| r3-2: "one Delta table per stage" | Not true: DATA_USAGE.md lists several tables per stage (stage 1 alone writes five). The sentence says "Delta tables under `data/delta/`". |
| r1-1: the build derives 852 and 820 | `checks/column.py` derives them from the column table and the built sheets, and the tests fail if `chart.toml` `mid_from_px` or the mid width disagree; the README is still rendered from `chart.toml`, so its `<picture>` does not depend on a build report being present. The name is set at 68, not the desk's 88: at a 765 px column 88 units would be 82 px, larger than review 1 wanted, and 68 is on the desk scale. |
| r3-1: X2 without "never retried" | Kept, by review 3's own fallback: "Errors, timeouts and non-HTML 200s" in place of "An error, a timeout or a non-HTML 200" keeps it within 25 words (24). |
| r3-1: X1 "50,000 per file", "canonicalised" | "50,000 URLs per file" (the unit stays), and the page's American spelling. |
| r2-1: `hair` in the token table | The hero draws no hairline; the table lists what it draws with. |
| Owner, outside this repository | Carried from round 11 (0.1.4 with P1, the LICENSE and `[project.scripts]`; statuses and back-off on 429/503; Scrapy's UConn defaults into a profile; `start.py` accepting `docker compose`; registrable-domain seeding; `cargo audit` and `clippy -Dwarnings` blocking; the organizer's raw-`netloc` comparison; the GitHub bio; the iOS and Android apps). New: fix Scrapy's quick start, which says "Sample URLs loaded" after `python start.py` (review 1); make `resume` after a kill open the redb file despite the stale lock (review 1); record `response.url()` as the node's URL and resolve links against it, and leave 3xx and `noindex` out of `export-sitemap`, which retires X3 and half of X1 (review 3); open the profile once on an iPad held sideways (review 1). |

### Measured state of this build

- Desk sheet 1,280 x 571 (gate 620); mid 820 x 707 (gate 964); phone 600 x 1,121 (gate 1,246).
- Page: desk 2,830 px at 1,280 (was 2,710); phone 5,213 CSS px at 390 (was 4,997: X3 and the two longer cautions,
  the arrival sentence, less the spider sentence and the go_go_go word). At 1,180 the whole route, the file and the
  hand-off are on the first 820 px screen.
- `python3 -m unittest`: 445 tests, all pass (16 new in `tests/test_round12.py`).
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 3 warnings (log.shards,
  POSITION-EMPTY, LICENSE-FLAGSHIP Rust-sitemap), 0 errors. The render tier is skipped while fast fails. Run alone,
  it passes (0 fail, 0 warn); HERO-COLUMN-PX: every viewport 360 to 1,920 px gets 11 px text, and from 768 a picture
  at most 900 px tall. DESIGN-FRESH, README-SUBCOMMAND, README-CAUTIONS, FIGURES, STRINGS-TWICE, AUDIT-COVER,
  README-STALE and AUDIT-STALE are clean.

## Round 13

Reviews: `review-r13-1.md` (the owner) **9 / 10**, `review-r13-2.md` (the historian of charts and sailing
directions) **9 / 10**, `review-r13-3.md` (the deck officer and yacht navigator) **8 / 10**. None meets the goal yet.
All three would ship the image as it is. What was left: a working rule that said more than the code does, a caution
list that had grown past its own cap and was the densest stretch of the phone page, a row in the picture whose reason
was only in our reviews (review 1); a method page that claimed every caution was probed, and cautions in an order
that did not follow the drawing (review 2); and a Scrapy command that crawls as UConn's bot, with a pick sentence that
never says Scrapy is polite where rustmapper 0.1.3 is not (review 3). One conflict: review 1's W1 wording ("so a kill
keeps the crawl") is false by the run check; review 3's correction is taken, shortened to fit review 1's one-line
limit.

Renders: `scratchpad/r6/build/round-13/` (the standard set, plus the mid sheets at 746, the phone sheets at 308, the
phone page at 360, and `page-1180-1.png`, `page-900-1.png`). `stats.json` was re-read from the local trees with
`scratchpad/r6/reroute13.py` (no new probe run; the round 12 run check stands).

### What was measured first

- **The breaker (review 1).** Scrapy `96e7a1a`, `src/utils/retry.py`: `record_success` sets `failure_count = 0` in its
  `else:` branch (the closed state); `stage2_worker.py:791` calls `breaker.record_success()` after every page that
  comes back. Five failures with a success between them never trip it: the count is five in a row.
- **W1 on one phone line (reviews 1 and 3).** Built each wording into the six editions (`scratchpad/r6/r13/try_w1.py`):
  "saved as it goes; export-sitemap works after a kill" (review 3's, 51 characters) and its comma and colon variants
  take two lines on the phone sheet, which grows from 1,121 to 1,155 units. "saved as it goes; export works after a
  kill" is one line on every edition and the phone sheet stays 1,121.
- **The user agent (review 3).** `settings.py:115` falls back to `UConn-Discovery-Crawler/1.0`; `config.yml` has no
  top-level `scrapy:` section; the scout's settings (`get_spider_settings("scout")`, its `custom_settings`) set no
  `USER_AGENT`. Scrapy's `-s` settings rank above a spider's `custom_settings`, so `-s USER_AGENT=…` wins.
- **The politeness (review 3).** `spider_config.py`: `"ROBOTSTXT_OBEY": bool(spider_config.get("robotstxt_obey",
  True))`, Scrapy's `RobotsTxtMiddleware` set to `None` and `PoliteRobotsTxtMiddleware` at 100, `RetryAfterMiddleware`
  at 560; `config.yml` sets no `robotstxt_obey`; the tests `test_robots_policy.py`
  (`test_disallowed_path_is_never_requested_and_crawl_delay_is_capped`) and `test_retry_after.py` are at HEAD.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1: "in a row" | Rule 1: "When 5 URLs in a row on one host fail every retry, that host is left alone for 60 s; the rest of the crawl goes on." The `[[figures]]` row is "5 URLs in a row on one host"; its `also` gains stage 2's `breaker.record_success()` and the reset in `record_success`'s `else:` branch (the same assignment in `__init__` proves nothing, so the anchor is that branch, to `def record_failure`). Test: a `retry.py` without the reset, or a stage 2 that never reports a success, fails the row. |
| r1-2: the fold | `chart.toml`: L3, X3, X2, X1 have `fold = true`; route `fold_lead = "What {release}'s files miss or get wrong"`. `render_readme.text_blocks` prints the open list (L1, L4, L2, L5) and then, before the code block, `<details><summary>What 0.1.3's files miss or get wrong</summary>` with the four folded items; with no label, the items join the open list. `LIST_MAX_ITEMS` is 7 again, for each list. README-CAUTIONS reads the fold (one fold, one list in it, a label, at most 7 items, each at most 25 words; the label is the folded list's lead-in and names the release) and, new, `cautions_placed`: every drawn caution is printed, a folded one inside the `<details>` and the others in the open list. Tests: no folded item in the open list; every open item has its lever (a flag or "Start at") or is L4; an X1 moved to the open list or dropped fails; an eighth item in a list fails. AUDIT §7 has a row for the label. |
| r1-3, r3-3: W1 | The drawn wording is "saved as it goes; export works after a kill", on the old order anchors plus `run_export_sitemap_command` opening `CrawlerState`, with `runs = ["export_after_kill"]` and `fails = ["kill_writes_file"]`. The day a kill writes the file (or the export after a kill stops working) the row falls back to "logged to disk, then saved to redb, in batches". The "every 50 ms" wording, which no tree ever held, is gone. `PURPOSE["W1"]` says what the row buys and what it does not claim. DESIGN.md's opening now quotes "saved as it goes". Test: W1 is one line on all six editions and the phone sheet is 1,121 units. |
| r2-1: DESIGN.md's probe sentence | Each caution has a `short` (load, robots.txt, seeding, the www scope, JavaScript, redirects, status codes, sitemap.xml). `tokens.probed` counts the printed cautions whose drawn wording names a probe: "Its probes test 5 of the 8 cautions the README prints; the other 3 (seeding, the www scope, JavaScript) are checked in the code only." With every caution probed it says so. Tests: the counts match the route, and taking `runs` off X3 gives "4 of the 8 … (seeding, the www scope, JavaScript, redirects)". |
| r2-2: the order | `chart.toml`: L1, L4, L2, L5, L3, X3, X2, X1, each with `stage` (server, start, links, file, export; `data/route.STAGES`, checked by `verify_route` and the schema). With the fold, X1 is the last item, right above the export command. `cautions_placed` fails when the printed items, open list first, then the fold, are out of stage order; a test swaps X3 and X1 and sees it fail. |
| r3-1: the user agent | README: "The last command crawls your site as `<your-bot>`; without that line, its requests say `UConn-Discovery-Crawler/1.0`." The code block gains `  -s USER_AGENT=<your-bot> \` (28 columns) before the `-a` lines. `[[figures]]` row on the `settings.py` literal, with a new `absent` check (`data/proof.py`: a regular expression that must not match) on `config.yml` (`^scrapy\s*:`) and on `spider_config.py` (`USER_AGENT`). Tests: a `scrapy:` section, a new default or a scout-level `USER_AGENT` each fail the row. |
| r3-2: Scrapy's politeness | `[copy] pick_polite`, "It obeys robots.txt and its Crawl-delay, and waits out a Retry-After.", appended to the pick sentence while its three `use = "pick_polite"` rows hold (`render_readme.pick_block`): `ROBOTSTXT_OBEY` with the scout's `custom_settings` and no `robotstxt_obey: false` in `config.yml`; `PoliteRobotsTxtMiddleware": 100` with Scrapy's own middleware off and the robots-policy test; `RetryAfterMiddleware": 560` with `test_retry_after.py`. Tests: a failed or missing row drops the clause and keeps the rest of the sentence; `robotstxt_obey: false` fails its row. |

### Fixes declined, or changed, and why

| Must-fix | Why |
|---|---|
| r1-3: "so a kill keeps the crawl" | False by the run check (review 3): `kill_writes_file` and `resume_after_kill` failed; only `export_after_kill` passed. |
| r3-3: "export-sitemap works after a kill" | Two lines on the phone sheet (1,155 units, measured), against review 1's hard limit; "export works after a kill" is one line. The code block right under the cautions names the command and its comment reads "# sitemap.xml, even after a kill". |
| r1-2: the fold's order "L3, X1, X2, X3" | The split is review 1's; the order inside the fold is review 2's (L3, X3, X2, X1), so the whole list follows the drawing and X1 sits above the export command. The two reviews do not conflict on what is open and what is folded. |
| r1-1: the anchor `self.failure_count = 0` | That assignment is also in `__init__`, so it would hold without the reset. The anchor is the `else:` branch of `record_success`, plus stage 2's call. |
| r2-1: "checked against the 0.1.3 source only" | L5 is checked in both trees (the 0.1.3 sdist and HEAD), so the sentence says "checked in the code only". |
| r3-1: "without `-s USER_AGENT`, its requests say …" | FLAG-WRAP failed: at 360 px `-s USER_AGENT` breaks after its hyphen. The sentence names the placeholder instead and points at "that line". It is hand-typed prose like the rest of the run sentence, so when the default or the config changes FIGURES fails and the weekly run goes red, as for every typed figure; the builder does not drop it by itself. |
| r3-2: `use = "pick"` | `use = "pick"` rows gate the whole pick sentence; the clause has its own (`pick_polite`), so a failed row drops only the clause, as the review's test asks. The `robotstxt_obey` check covers all of `config.yml`, not only the scout: stricter, simpler to read. |
| Notes, not ranked (review 3) | The robots.txt port (0.1.3 builds `https://{host}/robots.txt` without the port) goes on the owner's 0.1.4 list. The next leg's command (`import_rust_sitemapper.py`) and renaming the repository to `rustmapper` are not must-fixes and are not taken. |
| Owner, outside this repository | Carried from round 12 (0.1.4 with P1, `response.url()` as the base, `noindex` and canonicalized pages out of `export-sitemap`, `resume` after a kill, a LICENSE and `[project.scripts]`; the Scrapy quick start's "Sample URLs loaded"; the GitHub bio; the iOS and Android apps; an iPad check on a real device). New: change Scrapy's default user agent to a name and contact for the project, and the hard-coded ones in `stage4/large_doc_processor.py:86` and `stage1/sitemap_parser.py:299` (the user-agent clause and the `-s` line's sentence then need rewording, which FIGURES will flag); build 0.1.4's robots.txt URL from the queued URL's scheme, host and port. |

### Measured state of this build

- Desk sheet 1,280 x 571 (gate 620); mid 820 x 707 (gate 964); phone 600 x 1,121 (gate 1,246). W1 is one line on
  all six editions.
- Page: desk 2,774 px at 1,280 (was 2,830); phone 4,965 CSS px at 390 (was 5,213) and 5,365 at 360 (was 5,685). The
  fold saves more than the pick clause and the user-agent sentence add.
- `python3 -m unittest`: 466 tests, all pass (21 new in `tests/test_round13.py`; older tests that pinned the 8-item
  list, the item order, W1's old wording and rule 1's old body now hold the new ones).
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 3 warnings (log.shards,
  POSITION-EMPTY, LICENSE-FLAGSHIP Rust-sitemap), 0 errors. The render tier is skipped while fast fails. Run alone,
  it passes (0 fail, 0 warn). README-CAUTIONS, FIGURES, FLAG-WRAP, STRINGS-TWICE, DESIGN-FRESH, AUDIT-COVER,
  README-STALE and AUDIT-STALE are clean.

## Round 14

Reviews: `review-r14-1.md` (the owner) **8 / 10**, `review-r14-2.md` (the staff engineer screening for data
infrastructure) **8 / 10**, `review-r14-3.md` (information design and cartography) **8 / 10**. None meets the goal
yet. All three found the same false sentence: round 13's "It obeys `robots.txt` and its `Crawl-delay`" is true of
Scrapy's spider and false of the system the README starts, because the scout queues every link for stage 2 before
(or instead of) requesting it, and stage 2 fetches them all with aiohttp, with no robots.txt check, no Crawl-delay and
no name of its own. Reviews 1 and 3 found a second: `--reset-delta` loads nothing since Scrapy `b787e65`, because the
reset `start.py` runs is refused by the lake guard. Review 2 asked for the agent counts beside the counts they
qualify, and for the third Scrapy bullet to say how the system is run. Review 3 measured the desk sheet's words at
12.6 px in GitHub's 846 px column, under the page's own 16 px body text, for every desktop window from 1,200 px up.
Where the reviews differ on wording, the owner's review wins.

Renders: `scratchpad/r6/build/round-14/` (the standard set; the desk sheets also at 846, the column GitHub gives
them; the mid sheets at 746; the phone sheets at 308; the phone page at 360; the README's first screen at 1,180,
900, 1,366 x 650, 1,280 x 600 and 1,920 x 960). `stats.json` figure rows were re-read at the same HEADs with
`scratchpad/r6/reroute14.py` (no new probe run; the round 12 run check stands).

### What was measured first

- **Stage 2 (reviews 1, 2, 3).** Scrapy `96e7a1a`: `scout_spider.py` yields `_queue_for_stage2(url, …)` before
  `scrapy.Request(url, …)` for an HTML link and alone for any other link; `pipelines.py` writes it on
  `elif target_stage == "stage2":` with only an SSRF check. `stage2_worker.py` has no `robots` and no Crawl-delay
  (`grep -ic robots` 0), opens `aiohttp.ClientSession(connector=connector, timeout=…)` and calls
  `session.get(current, allow_redirects=False)` with no headers, so aiohttp sends `Python/3.11 aiohttp/3.13.1`
  (`python:3.11-slim`, `aiohttp==3.13.1`). Per host: `DEFAULT_STAGE2_PER_HOST_CONCURRENCY = 4`, `config.yml`
  `per_host_concurrency: 4`, no compose override.
- **The reset (reviews 1, 3).** `start.py` runs `docker-compose run --rm --no-deps -T scraper python cli.py reset
  --force`; `cmd_reset` calls `guarded_lake_wipe(DELTA_LAKE, args, …)`, and `--yes` needs `ALLOW_LAKE_RESET=1`, which
  no compose service sets. Review 1's run of the guard with those flags (refused, exit 3) stands.
- **Bullet 3 (review 2).** `alerting_rules.yml` `alert: DeltaWriteFailuresSustained` on
  `delta_write_failures_total{outcome="spilled"}`, which `lakehouse_manager.py` increments with that label;
  `prometheus.yml` loads `/etc/prometheus/alerting_rules.yml`, mounted in compose. `crawl_guard.py`
  `opt("kill_switch_check_secs", 5.0)`, no override in `config.yml`; both stages consult the guard
  (`CrawlGuardMiddleware`, `_crawl_guard_reason()`); `cmd_killswitch`, 15 tests, `docs/runbooks/sev1_abuse_kill_switch.md`.
- **The desk sheet (review 3).** Rebuilt with `SIZES["desk"] = (1000, 900)` and `L["desk"] = L["mid"]`: 1,000 x 707,
  0 problems; 19-unit words are 14.6 px at a 1,200 px window (column 766) and 16.1 px from 1,280 (column 846); the
  image is 598 px tall at 846. In the 1,366 x 650 preview the whole route, the hand-off line included, is on the
  first screen.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1, r2-1, r3-2: Scrapy's politeness | The pick sentence's clause is off the page. `[copy] pick_polite` now starts "Scrapy obeys …", so the day it returns it cannot be read as rustmapper; a fourth `use = "pick_polite"` row on `stage2_worker.py` (`present` `(?i)robots`, `absent` a `ClientSession(` without `headers=`) fails today and brings the clause back by itself once stage 2 checks robots.txt and sends its own name. `proof.py` gains `present` (a regex that must match). `checks/figures.py` fails a `pick_polite` row only while the clause is printed, so the gate does not turn the build red. The run sentence now reads, after "install Compose standalone).": "It loads no seeds: the last command gives the spider your site and names it `<your-bot>` (without that line, `UConn-Discovery-Crawler/1.0`). The spider obeys `robots.txt` and its `Crawl-delay`. The stage 2 worker then fetches every link the spider queued, disallowed ones too, 4 at a time per host, as `Python/3.11 aiohttp/3.13.1`." Four new `[[figures]]` rows: the spider's settings, middleware and robots test; "disallowed ones too" (the scout's order anchor, its non-HTML branch, the pipeline's stage 2 branch; `absent` robots and Crawl-delay in both stage 2 files and robots in the pipeline); "4 at a time per host" (default, config, no compose override); "`Python/3.11 aiohttp/3.13.1`" (Dockerfile, requirements, the session and the GET as they are; `absent` any user agent or `headers=`). Tests: each change in stage 2 (a robots check, a delay, a header, another aiohttp, 8 per host, a compose override, the scout queueing after its request) fails its row. |
| r1-2, r3-2: `--reset-delta` | The sentence and its two CSV rows are cut; "It loads no seeds by default." is "It loads no seeds:", its row also reads `guarded_lake_wipe(DELTA_LAKE, args` in `cli.py`, and `chart.toml` says when the sentence may come back (start.py passes `ALLOW_LAKE_RESET=1`, and the word "wipes", since `cmd_reset` deletes the lake first). No "is refused" on the page. |
| r2-2: agent counts | Each flagship's facts line ends with its own count: "coding agents (Claude) authored 45 of its 146 commits and co-signed 1 of his own 101"; Scrapy "coding agents (jules, Claude) authored 71 of its 499 commits and co-signed 30 of his own 420" (`render_readme.agent_counts`, `agent_clause`). The data line keeps the definition: "Tests and lines are counted per repository, whoever wrote them." AUDIT §7 has a row for each clause; AUDIT's `agent_authored` row says where it is printed. Tests: the clauses equal the computed counts; no agent commit prints no clause, not "0 of". |
| r2-3: bullet 3 | "Prometheus alerts on its own metrics, such as Delta writes spilling to disk, and Grafana dashboards. A kill switch stops new downloads within 5 s, with a runbook. Docker Compose and a Helm chart for Kubernetes." Four rows (the alert with its metric, Prometheus loading the rules and compose mounting them; the `spilled` label in the rule and the code; the 5 s default, both stages' guard, the CLI command and the tests, `absent` a `config.yml` override; the runbook file). No alert count is printed. |
| r3-1: the desk sheet | `scripts/sheets/route.py`: `SIZES["desk"] = (1000, 900)`, `L["desk"] = dict(L["mid"])`; the side-by-side geometry (title column 354, track at 456, file labels at 424) is retired. `hero-day.svg` and `hero-night.svg` are the stacked sheets, 1,000 x 707. `checks/column.py` gains DESK-PX (from `breakpoint_px` + 1 to 1,920: at least 14.5 px, and 16 where the column is 846); the desk height gate is 770. DESIGN.md (from `tokens.py`), the BREAKS table, SPEC §2.3 (a superseded note) say so. Tests: the geometry equals the mid's; the built desk sheet is 1,000 wide with the mid's height, drawn elements and PURPOSE IDs; DESK-PX fails the 1,280 sheet and passes the 1,000 one. The review renders draw the desk at 846 as well as 870. |

### Fixes declined, or changed, and why

| Must-fix | Why |
|---|---|
| r2-1: "Its discovery spider obeys …" as the pick clause | The owner's review drops the clause until stage 2 earns it, and the run sentence says what each stage does. Two sentences saying the spider obeys robots.txt would also fail STRINGS-TWICE. |
| r2-1: "… without that name." | The owner's wording names the string a site owner will see in the log (`Python/3.11 aiohttp/3.13.1`), which says more than "without that name". |
| r2-1: the scout literal "count 2"; `absent` `User-Agent` | Rows cannot count a literal; the two branches are anchored separately (the HTML branch as an order anchor, the else branch). The user-agent check is `(?i)user.?agent` plus `headers=` on the session and on the GET, which covers more ways to send a name. |
| r1-1: the gate's text "It obeys robots.txt (stage 2)" | It is "Scrapy obeys robots.txt in stage 2 too", so the row reads as what it gates. |
| r2-2: "agents also co-signed 1 and 30 of his own commits" on the data line | AUDIT §5 prints the co-signed count only beside the authored one; on the data line "1 and 30" would name no repository. Each facts line carries both, with his own commit count as the denominator ("1 of his own 101"). |
| r3-1: desk height gate 760 | 707 today; S2's two lines add about 56, which is 763. The gate is 770 (651 px at 846). |
| r3-1: `edition.DESK_W` | Left at 1,280: other sheets (built only on request) use it; the hero's width comes from `route.SIZES`. |
| r2-1 evidence: stage 4's `MyScraper/1.0 (Educational Research Bot)` | Not printed: stage 4 fetches only documents over 50,000 characters, and a third agent string would add two phone lines to a sentence the owner sized. On the owner's list below. |
| Live-like stats build | `v92/live-stats.json` (8 Oct) carries no `routes.rustmapper`, so the hero cannot build from it; that was so before this round. |
| Owner, outside this repository | New: Scrapy stage 2 should consult robots.txt (Protego, as Scrapy does), wait each host's Crawl-delay and send `USER_AGENT` from config, and stage 4 should too (`large_doc_processor.py:86`); or the scout should queue a link for stage 2 only once its request comes back. Then the pick clause returns by itself. `start.py --reset-delta` should pass `-e ALLOW_LAKE_RESET=1` (or drop `-T` and `--force`), and its help should say it wipes the lake. Carried: 0.1.4 (exits when idle, P1, `response.url()` as the base, `noindex` and canonicalized pages out of `export-sitemap`, `resume` after a kill, the robots.txt port, a LICENSE, `[project.scripts]`); `[position]` and `[contact]`; one measured crawl at scale; `state.rs:240`'s stale "(default: 2)"; the GitHub bio; the iOS and Android apps; a real iPad. |

### Measured state of this build

- Desk sheet 1,000 x 707 (gate 770); mid 820 x 707 (gate 964); phone 600 x 1,121 (gate 1,246). From 1,200 px the
  route's words are 14.6 to 16.1 px (were 11.4 to 12.6).
- Page: desk 3,021 px at 1,280 (was 2,774; the image is 221 px taller); phone 5,109 CSS px at 390 (was 4,965) and
  5,533 at 360 (was 5,365): the agent clauses and bullet 3 add more than the reset and pick cuts save.
- `python3 -m unittest`: 480 tests, all pass (15 new in `tests/test_round14.py`; older tests that pinned the reset
  sentence, the old bullet, the old data line, the 1,280 desk and its file labels now hold the new ones).
- `check.py --tier fast,render`: fast 1 fail (ROUTE-UNVERIFIED S2, P1 not at HEAD), 3 warnings (log.shards,
  POSITION-EMPTY, LICENSE-FLAGSHIP Rust-sitemap), 0 errors. The render tier is skipped while fast fails. Run alone,
  it passes (0 fail, 0 warn); DESK-PX: from 1,200 px the route's words are 14.5 px or more, and 16 px or more at the
  846 px column. FIGURES, AUDIT-COVER, AUDIT-STALE, DESIGN-FRESH, README-STALE and STRINGS-TWICE are clean.

## Round 15

Reviews: `review-r15-1.md` (the owner) **8 / 10**, `review-r15-2.md` (the systems engineer who runs the code)
**7 / 10**, `review-r15-3.md` (the student on a phone) **8 / 10**. None meets the goal yet. Nothing printed in round 14
was false, but three things were wrong with what would happen next. S2 ("paced by that host's robots.txt") was armed
to be drawn on a 0.1.3 image the day P1 lands at HEAD, though 0.1.3 has no Crawl-delay parser. Merging would have
put the old island sheet and a broken mid image on the profile, because S2's red gate skipped the publish. And the
release has a fault the page never named: on https, the first link `robots.txt` disallows stalls that host's queue,
and a slow `robots.txt` lets disallowed pages through. Every probe served plain http, where 0.1.3 never reads
`robots.txt`, so 14 rounds missed it. Review 3 found that the `<img>` a client falls back to was the desk sheet (5.9 px
words in a 308 px column), that rustmapper's own user agent was not on the page, and that the install note said
"elsewhere" when only Linux had been tried.

Renders: `scratchpad/r6/build/round-15/` (the standard set; desk also at 846, mid at 746, phone at 308, the phone page
at 360, first screens at 900, 1,180, 1,280, 1,366 and 1,920). `stats.json` was re-read with `scratchpad/r6/reroute15.py`
(the route at the same HEADs and in the 0.1.3 sdist; the figure rows), and the run check gained five steps from
today's probe run against the same installed 0.1.3 (`scratchpad/r6/rc15/steps.json`).

### What was measured first

- **The stall (review 2).** `runcheck.py --probe robots_stall` (new): https on 127.0.0.1:443 with a certificate made
  for the run, `robots.txt` `Disallow: /secret` answered at once, the home page held 1 s and linking p1 to p5,
  `secret.html`, p6 to p10. Result: 7 requests; p1 to p5 fetched, `secret.html` not, p6 to p10 never in 30 s. Code:
  `sdist:src/frontier.rs` `get_next_url`, "blocked by robots.txt" then `continue;` with no `push_ready_host`.
- **It does resume (new, against review 2's wording).** `add_url_to_local_queue_unchecked` pushes the host back
  whenever a new URL is queued. A first run with p1.html held 3 s and linking one new page fetched p6 to p10 right after
  it. Probe `robots_resume` (new) now measures this: p6 to p10 are fetched only after the late page with the new link
  is answered (13 requests). So "ends that host's crawl" and "never asked for" are false. "Stalls … wait for a new
  link" is true.
- **The late `robots.txt` (review 2).** Probe `robots_late` (new): `robots.txt` answered 0.5 s late; 22 requests, 10 of
  the 10 disallowed pages fetched. Code: "missing robots.txt, fetching in background (allowing crawl)" and "// Proceed
  with crawling - don't block on robots.txt" in `get_next_url`. The cap there is `max_inflight` (20) at a time, and a
  `robots.txt` fetch may take 30 s and is then retried, so the total is not bounded by 20.
- **The name (review 3).** Probe `ua_seen` (new, in the `robots_read` run): 4 requests, every one with User-Agent
  `RustSitemapCrawler/1.0`, and no From header. Code: `cli.rs` `Crawl` `user_agent` default, `network.rs`
  `.user_agent(&user_agent)`.
- **The height budget.** The phone sheet is served up to an 851 px window, where GitHub's column is 481 px and
  HERO-COLUMN-PX holds the picture to 900 px tall. That caps it at 1,122 units, not the 1,246 of ROUTE-HEIGHT that
  review 2 sized against. Today it is 1,121, so H0 can be drawn only if one row gives up its line, and H0 itself must
  fit one phone line (about 45 characters).

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1: S2 on a 0.1.3 image | S2 gains `{path = "src/robots.rs", text = "fn parse_crawl_delay"}` in `release` (and `head`), with a comment: it mirrors the `absent` anchor of L1 and L4, so "paced by that host's robots.txt" and "It ignores `Crawl-delay`" flip on the same release. Tests: the 0.1.3-shaped release plus a HEAD with P1's test file leaves S2 unverified ("release src/robots.rs: no 'fn parse_crawl_delay'"). A release with `parse_crawl_delay_secs` verifies it. For both releases and both probe states, S2 is never drawn beside an L4 that says "ignores `Crawl-delay`". Built from stats where S2 holds, its group is drawn with its PURPOSE row. |
| r1-2: publish while S2 waits | S2 has `waits = "release"` (`data/route.py` accepts only "release"). `R.waiting(e)` is true for an unverified entry with `waits` whose own release anchors fail. `checks/route.py` reports it as ROUTE-WAITING (warn) and still leaves it undrawn. Every other unverified entry is still ROUTE-UNVERIFIED (fail), and so is a `waits` entry that holds in the release but not at HEAD. `profile.yml`: "Social preview", "Publish sheets to the orphan chart branch" and "Publish, dry run" now come before "Commit stats, log, lock and README to main", so main never names a file the branch lacks. Tests: today's stats give one ROUTE-WAITING and no fail; release-pass/head-fail gives a fail; S2 without `waits` fails; the workflow's step order. Local gate on today's stats: fast 0 fail, and the render tier ran (0 fail). |
| r1-3: Scrapy's effect on a site | `README.md` (hand-typed): the paragraph ends at "It loads no seeds: the last command gives the spider your site." Then "Before you run it:" and two items: "The spider obeys `robots.txt` and its `Crawl-delay`, and names itself `<your-bot>` (without that line, `UConn-Discovery-Crawler/1.0`)." and "The stage 2 worker then fetches every link the spider queued, disallowed ones too, 4 at a time per host, as `Python/3.11 aiohttp/3.13.1`." The spider's `[[figures]]` row loses its full stop, so it still matches. Test: the list sits under the lead, and its items carry `Crawl-delay` and `Python/3.11 aiohttp/3.13.1`. |
| r2-1: L6, the stall, in the open list | New `L6` (stage server, after L4): "On an https site, each link `robots.txt` disallows stalls that host's crawl: the links queued behind it wait for a new link to that host." (24 words.) Release anchors: the blocked branch as one literal, from the message to `continue;`, in `get_next_url`; the re-push in `add_url_to_local_queue_unchecked`; the https robots URL. `runs = ["robots_stall", "robots_resume"]`. A code-only wording holds only while the probes were `skipped`. An empty wording with `fails = ["robots_stall"]` retires it. |
| r2-2: draw the stall | New trap `H0` (loop, release scope) right under F1: "on https, a disallowed link stalls its host", one line in every edition, same anchors and probes as L6. W1 gets `drawn = false`: it is still checked, its row stays in `chart.toml` and AUDIT, and `R.drawn` leaves it out. Two traps on consecutive rows share one dotted line, drawn in the last one's group. CONTRAST-DANGER accepts a trap inside a shared line, by the report's danger box. PURPOSE has H0; BREAKS and the module docstring say there are two catches; DESIGN.md's opening names both ("The dotted line marks the catches: …"). Heights: desk and mid 707, phone 1,121, all unchanged; the phone sheet is 899 px tall at 851. |
| r2-3: L4, before the rules are in | L4: "Until a host's `robots.txt` is back, it fetches that host's pages, disallowed ones too. It ignores `Crawl-delay`, and reads `robots.txt` only over https." (22 words.) New anchors: the two `get_next_url` strings. `runs = ["robots_late"]`, `fails = ["robots_read"]`. Alternatives: the round 6 wording while `robots_late` is skipped, or once it fails; one for each later fix (http read, Crawl-delay parsed); and an empty one. |
| r2-4: https probes | `scripts/runcheck.py`: `make_cert` (openssl, SAN localhost and 127.0.0.1, an absolute path), `serve_https` (http.server in TLS on 127.0.0.1:443), `tls_env` (SSL_CERT_FILE, NO_PROXY), `trust_cert` (macOS in CI only: `sudo -n security add-trusted-cert`, removed after), and `_skip`. Probes `robots_stall`, `robots_resume` and `robots_late`, with fixtures `tests/fixtures/robots-{stall,resume,late}-site/`. A probe that cannot bind 443, make a certificate, or get one request through, or whose `robots.txt` came too late to say anything, is `skipped`. `run_missing` treats a skipped step as neither passed nor failed. A wording with `skipped = [...]` holds only then, and ROUTE-PROBE-SKIPPED warns. Tests: each verdict; a busy port is skipped; a skipped probe never retires L6. |
| r2-5: the data line | `render_readme.route_clause`: "…its commands were run, with seeding off, against local test sites over http and https on 10 Oct 2026 (Linux x86_64)." It prints this only while `robots_stall` and `robots_late` both ran (`https_ran`); otherwise it prints the round 14 words. The data line is built in `render_readme.py`, not `[copy] survey`. |
| r3-1: the `<img>` fallback | `HERO_ROUTE_SOURCES`: the desk has its own `(min-width: 1200px) and (prefers-color-scheme: dark)` → night and `(min-width: 1200px)` → day; `<img src>` is `hero-phone-day.svg`. `checks/column.py`: `img_edition`, `falls_back`, and HERO-FALLBACK (fail): some width from 360 to 1,920 matches no `<source>`, or the `<img>` is not a phone edition, or its smallest text is under 11 px in the 278 px column. `served()` falls back to the `<img>`'s edition. Tests: six sources and a phone `<img>`; `served` at 360, 390, 851, 852, 1,199, 1,200 and 1,920 gives phone, phone, phone, mid, mid, desk, desk; a desk `<img>` (5.3 px at 278) and a missing desk source both fail. |
| r3-2: rustmapper's name | New `L7` (stage server, right after L1): "It names itself `RustSitemapCrawler/1.0`, with no way to reach you.<br>`--user-agent <your-bot>` sends your name instead." Anchors: `cli.rs` `Crawl` `user_agent` `equals` the default (stricter than the absent http/@ check: any contact changes the literal); `network.rs` `.user_agent(&user_agent)`; no `header::FROM` and no `"From"`. `runs = ["ua_seen"]`. AUDIT-COVER now strips `<…>` placeholders from a literal as `visible()` strips them from the page. Tests: a contact-bearing default, a From header, or a failed probe fails the row; L7 prints second. |
| r3-3: "elsewhere" | `_wheel_sentence`: "Prebuilt for Apple silicon on CPython 3.13. On Linux x86_64, `pip` builds it from source, which needs a Rust toolchain (3 min from a cold cache on a 4-core machine); other platforms were not tried." It builds the list from `source_runners`, the run checks whose install was an sdist build and passed. It takes one record or a list, and the tail goes once the three common platforms are covered. No source build: "… `pip` builds it from source elsewhere, which needs a Rust toolchain; this was not tried." Tests: one runner, two runners, none, and a wheel-only (macOS) run. |

### Fixes declined, or changed, and why

| Must-fix | Why |
|---|---|
| r2-1, r2-2: "ends that host's crawl", "the links queued after it are never asked for" | False in general: a new link to the host puts it back on the queue (`add_url_to_local_queue_unchecked`), measured by `robots_resume`. L6 says "stalls … wait for a new link to that host", and H0 says "stalls its host". |
| r2-2: H0's text "the first link `robots.txt` disallows ends that host's crawl" | Besides "ends", it takes two phone lines, and the phone sheet has room for one (1,122 units at most, see the height budget). "on https, a disallowed link stalls its host" fits one line. It keeps "https", without which it is false on http sites, and "host" is the unit F1 just named. |
| r2-2 against r1 (W1 "keep") | The owner's review keeps W1. Here it conflicts with drawing the stall, which the owner's review did not weigh, and the phone budget allows one or the other. W1 is the row that reassures rather than directs, and the README's block already says it where the reader types ("# sitemap.xml, even after a kill"). H0 marks the one place where H1's quiet-minute rule reads a stalled crawl as finished. W1 is not drawn but stays checked. To undo: drop `drawn = false` and H0. |
| r2-3: "up to 20 pages per host before …" and the `state.rs:285` anchor | 20 is a cap at any one moment, not a total. A `robots.txt` fetch can take 30 s and is retried, so more than 20 can get through. L4 says what happens without a number. |
| r2-4: the steps "pass by default" guard | Implemented as `skipped`. Additionally, `robots_stall` and `robots_resume` are skipped, not failed, when the disallowed page was fetched (the rules were not in yet): such a run says nothing about the stall and must not retire L6. |
| r2-5: `[copy] survey` | The data line is built in `render_readme.route_clause`, so the change is there. |
| r3-2: the id L6 | L6 is the stall (review 2), so the name is `L7`. The "absent http or @" anchor became `equals`, which catches any change to the default. |
| r1-2: "do one dry_run workflow run" | See "The workflow" below. |
| Noted, not ranked (r1): "co-author on 1 of his own 101"; a clean-tree note in the maintainer comment | Not changed this round. Taste, and a dev note; on the owner's list. |

### The workflow

The local gate on the committed `stats.json` gives fast 0 fail, 4 warnings (log.shards, POSITION-EMPTY,
LICENSE-FLAGSHIP, ROUTE-WAITING S2), and then runs the render tier: 0 fail, and HERO-COLUMN-PX, HERO-FALLBACK,
DESK-PX and FLAG-WRAP all hold. A run on GitHub cannot be judged from here, for two reasons. Its run check is on
macos-14, which installs the prebuilt wheel (so the install note prints "this was not tried"). And whether the https
probes run there depends on `sudo -n security add-trusted-cert`; if they cannot, they are skipped, the code-only
wordings stand, and ROUTE-PROBE-SKIPPED warns. One `workflow_dispatch` with `dry_run: true` on `v12/purpose` before
merging is on the owner's list.

### Owner, outside this repository

- **0.1.4 (Rust-sitemap).** Main already re-pushes the host after a blocked URL (`6bcb6cd`) and fails closed until
  `robots.txt` is in (#47), so a release cut from main retires H0, L6 and L4's first clause by itself. With
  `parse_crawl_delay_secs` in the release, S2 is drawn and L1 and L4 reword themselves. Before cutting it, rule out
  review 2's finding: main at `32c2651`, over https with a 200 `robots.txt`, deferred the start URL and then reported
  an empty frontier without fetching it. Also: the default user agent with a contact
  (`rustmapper/<version> (+https://github.com/BenjaminSRussell/Rust-sitemap)`) and `From` when a contact is given; a
  test for `status_code` null on pages fetched after a block (review 2's shop run). The rest is carried (exits when
  idle, P1, `response.url()` as the base, `noindex` and canonical pages out of `export-sitemap`, `resume` after a
  kill, the robots.txt port, a LICENSE, `[project.scripts]`).
- **When S2 is drawn**, the phone sheet gains about 77 units. That fits only if H0 and H1 retire with it, which a
  0.1.4 from main does. Otherwise HERO-COLUMN-PX fails, which is the right result.
- **Still open:** open the profile once in the GitHub iOS app, light and dark, and log which edition it shows; the
  dry run above; Scrapy stage 2's robots check, delay and name; `start.py --reset-delta`; `[position]` and
  `[contact]`; one measured crawl at scale; the GitHub bio; a real iPad.

### Measured state of this build

- Desk sheet 1,000 x 707 (gate 770); mid 820 x 707 (gate 964); phone 600 x 1,121 (ROUTE-HEIGHT 1,246; 899 px tall at
  the 851 px window, under HERO-COLUMN-PX's 900). The loop holds F1, then H0 and H1 in one dotted line.
- Page: desk 3,245 px at 1,280 (was 3,021); phone 5,525 CSS px at 390 (was 5,109) and 5,949 at 360 (was 5,533). L7,
  L6, L4's longer item and the Scrapy list add more than anything this round removed.
- `python3 -m unittest`: 513 tests, all pass (33 new in `tests/test_round15.py`; older tests that pinned W1 drawn, the
  old L4, the four-item list, the old run sentence, the "elsewhere" note, the 3-page data line, the five-source
  picture and one danger mark now pin the new state).
- `check.py --tier fast,render`: fast 0 fail, 4 warnings (log.shards, POSITION-EMPTY, LICENSE-FLAGSHIP, ROUTE-WAITING
  S2), 0 errors, exit 2. The render tier ran: 0 fail. README-STALE, DESIGN-FRESH, AUDIT-STALE, AUDIT-COVER, FIGURES,
  STRINGS-TWICE, README-CAUTIONS, FLAG-WRAP, CONTRAST-DANGER and HERO-FALLBACK are clean.

## Round 16

Reviews: `review-r16-1.md` (the owner) **8 / 10**, `review-r16-2.md` (the data engineer) **7 / 10**,
`review-r16-3.md` (the copy editor) **8 / 10**. None meets the goal yet. Every figure held. What was wrong was what
the words led a reader to believe. The image drew the robots.txt stall, then said "done when `Received work item`
lines stop for 60 s" one row below it, and a stalled crawl stops those lines too. "Stalls its host" read, to a site
owner, as harm to the server. A blank row in `sitemap.jsonl` could also be a page never fetched, and the page did not
say so. 0.1.3's `sitemap.xml` lists the disallowed pages it fetched. Scrapy's "near-duplicate pages by MinHash" does
not hold across the worker's passes. Some sentences had to be read twice.

Renders: `scratchpad/r6/build/round-16/` (the standard set; desk also at 846, mid at 746, phone at 308, the phone page
at 360, first screens at 900, 1,180, 1,280, 1,366 and 1,920). `stats.json` was re-read with `scratchpad/r6/reroute16.py`
(the route at the same HEADs and in the 0.1.3 sdist; the figure rows). The run check's `robots_stall` and
`robots_late` were run again today against the same installed 0.1.3 (`scratchpad/r6/rc16/steps.json`), and each now
has a follow-on step.

### What was measured first

- **Blank rows (review 2).** `runcheck.py --probe robots_stall` with the new `blank_rows` step: 12 rows; the 6 pages
  the server never saw (p6 to p10 and the disallowed `secret.html`) are rows with `status_code` and `crawled_at` null;
  `grep -c '"crawled_at":null'` on the file gives 6, the number of rows with `crawled_at` null. The crawl's output has
  `Shard 3: URL https://localhost/secret.html blocked by robots.txt` (line 5 of the log).
- **The sitemap (review 2).** `sitemap_keeps_disallowed`: `export-sitemap` on the `robots_late` run's data wrote 21
  `<loc>`, all 10 disallowed pages that run fetched among them. `run_export_sitemap_command` reads no robots rules.
- **Scrapy's dedup (review 2).** At `96e7a1a` the URL dedup that runs is the spider's `RFPDupeFilter` (settings.py; no
  `scrapy:` section in config.yml to change it), `_canonical_queue_row` on every queue row, and stage 2's upsert by
  `url_hash`. `REDIS_KEY_SEEN_URLS` is defined in constants.py but not read anywhere, so it is not an anchor.

### Fixes applied

| Must-fix | What changed |
|---|---|
| r1-1: H1's "done" | H1: "0.1.3 never exits by itself; quit when `Received work item` lines stop for 60 s". Same 9 characters, so no edition's line breaks moved. The H0 comment in `chart.toml` says why. Tests that pinned the text are updated; `test_round16.QuitNotDone` checks that H1 never says "done" while H0 is drawn. |
| r1-2: the stall's sign and cost | L6 ends "The sign: `blocked by robots.txt`." (the literal the anchors hold; the branch's `eprintln!`). X2 (the fold): "Errors, timeouts, non-HTML 200s and pages never reached are left blank, `crawled_at` too." It rests on new anchors (`AddNodeFact(SitemapNode)`, `crawled_at: None,` in state.rs) and the new probe `blank_rows`, with a code-only wording while that probe is skipped. AUDIT-COVER and STRINGS-TWICE are clean (tests too). |
| r1-3 + r2-4: H0's words | H0: "on https, pages behind a disallowed link wait" (45 characters), both wordings. One phone line in all six editions (round 15's test passes). PURPOSE and DESIGN.md follow. |
| r1-4: padding inside the dotted line | `DANGER_PAD_X = {desk: 11, phone: 12, mid: 11}`, `DANGER_PAD_Y = 6`. The phone box is now x 76 to 570 (the loop bracket ends at x 56). New render-tier check BOX-PAD (`scripts/checks/boxpad.py`): the words' box (advance widths) to the inner edge of the dots, at least `BOX_PAD_MIN` = 8 units sideways, in every edition. Measured: phone 10.3 day, 10.0 night; desk and mid 9.3 day, 9.0 night. Heights unchanged: desk and mid 707, phone 1,121. |
| r2-1: the blank rows and their count | X2 as above. The code block gains, after the stop rule: `# count the blank rows`, `grep -c '"crawled_at":null' \`, `  data/sitemap.jsonl` (each under 32 columns). `render_readme.blank_lines` prints it while the new release gate `blank_rows` holds (`pub crawled_at: Option<`, `serde_json::to_string(&node)` in `export_to_jsonl`, `join("sitemap.jsonl")`, the crawl's `--data-dir` default `./data`) and the `blank_rows` probe did not fail. |
| r2-2: disallowed pages in sitemap.xml | X1: "Its `sitemap.xml` is every row with `status_code` 200, in one file; the format allows 50,000 URLs per file. It keeps `noindex`, canonicalized and disallowed pages." (25 words.) New anchor `absent = "robots"` in `run_export_sitemap_command`; new probe `sitemap_keeps_disallowed`. Two fallbacks print the round 12 wording: while the probe is skipped, and once it fails. Both needed `from_head = true` for the 50,000, which a test caught. |
| r2-3: Scrapy's dedup | Bullet 2: "Repeat URLs are dropped by their hash. In stage 3 …". The `deduplicated` pick row now rests on settings.py's `DUPEFILTER_CLASS … RFPDupeFilter`, `def _canonical_queue_row` and its use on the stage 2 queue, and stage 2's `# #311: upsert by url_hash`, with no `scrapy:` section in config.yml. |
| r2-5: BREAKS | "(fetch, at most 20 at once from one host, the robots.txt stall, and the crawl that never exits)". The module docstring no longer says "under the log". |
| r3-2: C1's garden path | C1: "press Ctrl-C once and wait for `Saved to`; a second press quits without writing the file". Same anchors, same line counts. |
| r3-3: L6's reduced relative | L6: "On https, pages queued behind a link that `robots.txt` disallows wait for a new link to that host. The sign: `blocked by robots.txt`." (23 words.) |
| r3-4: the Scrapy block | (a) "… and Grafana dashboards show them." (b) "The crawl's output lands in Delta tables under `data/delta/`". (c) "Run the commands below from …". (d) "(without the `USER_AGENT` line, …)". (e) "PostgreSQL, Redis, Prometheus, Grafana and a worker …", with `"\n  prometheus:"` in that figure row's `also`. Every `[[figures]]` substring still matches. |
| r3-5: serial comma | "raw-first storage and the dashboards"; the alt text "what it does with each page and how to stop it". |

### Fixes declined, or changed, and why

| Must-fix | Why |
|---|---|
| r3-1: "end it when" for H1 | The reviews conflict and the owner's review wins: "quit when". It is the same length, so no line moves, and it is an instruction like the code block's "then Ctrl-C once". Review 3's point that C1 says "quits" two rows down holds: the right move and the wrong one share a verb. C1's new order puts the instruction ("press Ctrl-C once and wait for `Saved to`") before the warning, which separates them. |
| r2-4: "stalls its queue" | The owner's review wins: "pages behind a disallowed link wait" names what the visitor loses and uses L6's verb. |
| r1-2 + r3-3: L6 as "… stalls that host's crawl: pages queued behind it wait …" plus the sign sentence | That is 35 words, and the list's cap is 25 (README-CAUTIONS). The kept wording puts "pages" first, as H0 does, and is 23 words. "stalls that host's crawl" is the clause that went. |
| r1-2 + r2-1: X2's "never retried" | Both reviews' wordings together come to 29 words. "Pages never reached" (review 1's test) went in, and "never retried" came out to meet the cap. The count in the code block is where the reader acts on a blank row. |
| r2-1: the comment "# rows never fetched or failed" | A non-HTML 200 is fetched and did not fail, but it is still a blank row, so the comment would be false for it. The comment is "# count the blank rows", and the fold defines a blank row just above the block. AUDIT-COVER also failed "# blank rows (no HTML 200)": a 200 with no register row. |
| r2-1: the grep line gated on HEAD's state.rs too | The code block runs the release pip installs. A HEAD anchor would drop the line when main changes, while 0.1.3 behaves the same. The gate reads the release only. |
| r2-1: the check on `robots_stall` itself | It is a separate step, `blank_rows`, in the same run. Tying X2 to `robots_stall` passing would make X2 unverified the day a release fixes the stall. Instead, `blank_rows` checks that every page the server never saw is a blank row, and that the grep counts exactly the blank rows. It is skipped when the https run cannot go or when every page was reached. |
| r2-3: the anchor `REDIS_KEY_SEEN_URLS = "seen:urls"` | That constant is defined and never read at `96e7a1a`, so it would be the same kind of presence anchor the review faulted. The row uses the dupe filter, the canonical queue row and the stage 2 upsert, which run. |
| r1-4: desk and mid at 10 | At 10, the night editions' 4.08-unit stroke left 7.96 units, under BOX-PAD's 8. Desk and mid take 11. |
| r3-4e: "about +1 line at 390" | Measured: the phone page is 5,645 CSS px at 390 (was 5,525). The grep lines, L6's sign and the Scrapy repairs account for it. |

### Owner, outside this repository

- **Scrapy:** make the near-duplicate filter global, either by persisting the MinHash index (datasketch
  `storage_config` on the Redis the stack already runs, with a fixed `basename`) or by recording a skipped page's hash
  in `stage3_summaries`. Add a test that runs `Stage3Worker.run()` twice and expects one summary. The clause can come
  back once it is anchored on that test.
- **0.1.4 (Rust-sitemap):** carried from round 15. A release cut from main retires H0, L6 and L4's first clause. Also:
  leave robots-disallowed and `noindex` pages out of `export-sitemap`, which retires X1's new clause through the
  fallbacks.
- **Still open:** the iOS app check, the `workflow_dispatch` dry run, Scrapy stage 2's robots check, delay and name,
  `[position]` and `[contact]`, a real iPad.

### Measured state of this build

- Desk sheet 1,000 x 707; mid 820 x 707; phone 600 x 1,121 (899 px tall at the 851 px window, under HERO-COLUMN-PX's
  900). H0 is one line in every edition. The danger box on the phone runs from x 76 to 570.
- Page: desk 3,317 px at 1,280 (was 3,245); phone 5,645 CSS px at 390 (was 5,525) and 6,045 at 360 (was 5,949).
- `python3 -m unittest`: 539 tests, all pass (26 new in `tests/test_round16.py`; older tests that pinned H1's "done",
  the old C1, H0, L6, X2 and X1, the Scrapy sentences and the code block now pin the new state).
- `check.py --tier fast,render`: 0 fail, 4 warnings (log.shards, POSITION-EMPTY, LICENSE-FLAGSHIP, ROUTE-WAITING S2),
  0 errors, exit 2. The render tier ran with BOX-PAD (new), HERO-COLUMN-PX, HERO-FALLBACK, DESK-PX and FLAG-WRAP, and
  none failed. README-STALE, DESIGN-FRESH, AUDIT-STALE, AUDIT-COVER, FIGURES, STRINGS-TWICE, README-CAUTIONS and
  CONTRAST-DANGER are clean.
