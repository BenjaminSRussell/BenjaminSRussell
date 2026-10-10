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
