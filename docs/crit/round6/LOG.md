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
