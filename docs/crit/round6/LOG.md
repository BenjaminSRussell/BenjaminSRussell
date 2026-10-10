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
