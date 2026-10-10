# Round 6 spec: the way into rustmapper

9 Oct 2026. This is the build spec for the first image and the page around it. It takes concept A (the way into his
work) and adds the judges' grafts. DECISIONS.md says why. Everything below is written so one engineer can build it in
this pipeline (`build_stats.py` → `stats.json` → `sheets/*.py` → `render_readme.py` → `check.py`).

Citations: `R4 impl. 9` is round-6 research file R4, implication 9. `R2-F3` is R2, finding F3. Code is cited as
`repo:path` in the clones at Rust-sitemap `32c2651` (7 Oct 2026), Scrapy `96e7a1a` (8 Oct 2026), ideal-url-organizer
`159968a` (7 Oct 2026), and the PyPI sdist `rustmapper-0.1.3` (`sdist:path`). Every code fact in this file was checked
in those trees for this spec.

---

## 0. What the image says, in one sentence

> **How you start rustmapper, what happens to a URL inside it in order, where a stranger goes wrong, and where the
> output goes next.**

The owner asked "what is it showing?" and "how does it help the user see my project?". The answer is that sentence,
and every mark in the image either belongs to it or is cut.

Why a picture and not a list (R5 test, questions 1 to 6): the project has a real route. A URL is seeded, queued per
host, fetched by a worker pool the governor resizes, logged, and written out as `data/sitemap.jsonl`. Vertical
position is the order a URL goes through, which is the strongest channel there is (R1-F16, R5-F6). A trap is drawn at
the stop where it happens, so you see where in the run it bites. A bullet list can't show that (R1-F10, R3 impl. 9).
The entrance and the end are fixed points you find in a second (R4-F3). Lookups (test counts, languages, the other 20
repositories) stay in text, because text beats a picture for lookups (R3-F4, R5-F10).

The visitor questions every element must answer (from concept C, R4-F1/F5/F7/F8, R2-F3):

| Q | Question |
|---|---|
| Q1 | Who is this and what does he build? |
| Q2 | Which project should I look at? |
| Q3 | Does it work, and is it alive? |
| Q4 | How do I start it, and what do I get? |
| Q5 | What will trip me up? |

An element that answers none of these is cut. That rule is enforced by a test (section 7, T-PURPOSE).

---

## 1. Blocking work in Rust-sitemap (before the new image ships)

These changes are in Ben's Rust-sitemap repository, not in this one. The image is drawn only from what the tool
actually does, so the build refuses to draw the affected marks until they land (section 5 anchors, section 6 run
check).

| # | Change | Why | Evidence | How this pipeline enforces it |
|---|---|---|---|---|
| P1 | A robots.txt answered 4xx means "allow all". A 5xx or an unreachable server means "disallow all", retried later. The frontier fetches robots.txt with the queued URL's own scheme (use `url_utils::robots_url`), not a hard-coded `https://`. Add `tests/robots_4xx_allows_crawl.rs`, which crawls a local server that has no robots.txt and expects pages to be fetched. | At HEAD a site whose robots.txt is a 404 is never crawled. `robots.rs` returns `None` for any status but 200, and `frontier.rs` defers the URL every 250 ms for as long as there is no robots body. RFC 9309 §2.3.1.3 says a crawler may access everything after a 4xx, and §2.3.1.4 covers 5xx. Concept B's trial saw it happen (books.toscrape.com, nothing fetched in 400 s). The frontier's `fetch_robots_txt(domain)` builds `https://{domain}/robots.txt`, so plain-http sites hit the same path. That was found during this synthesis and needs confirming on Ben's machine. | `Rust-sitemap:src/robots.rs` (the `status_code == 200` match), `src/frontier.rs` ("fail closed until robots.txt arrives (#47)", the deferral branch). 0.1.3 (`sdist:src/frontier.rs`) predates #47. | Stop S2's HEAD anchors require the test file (section 5). The weekly run check crawls a site with no robots.txt (section 6). |
| P2 | `--duration` stops a crawl that has stalled. Add a test. | B's trial: `--duration 300` did not stop the stalled crawl, and `timeout` killed it at 400 s. | concept B, "What the research trial found" | Not drawn, so it doesn't block the image. Listed so the README's cargo line (section 4, block 5) is honest. |
| P3 | README fixes. Line 86: the `--seeding-strategy` default is `none` at HEAD (`src/cli.rs`). Line 25: on macOS arm64, `pip install rustmapper` 0.1.3 installs the `rust_sitemap` binary, not just a library (the 0.1.3 wheel contains only `rustmapper-0.1.3.data/scripts/rust_sitemap`). | The README contradicts the code and the release. | `Rust-sitemap:README.md:25, :86`; `src/cli.rs` (`default_value = "none"`); `sdist:src/cli.rs` (`default_value = "all"`); wheel listing in `scratchpad/r6/pypi-wheel/w.whl` | Not checked here. It is the source of hazard H2 in concept A, which is removed (section 3). |
| P4 | Release 0.1.4 so that `pip install rustmapper` provides a command named `rustmapper` (and keeps `rust_sitemap`). Note: HEAD's `pyproject.toml` builds with `bindings = "pyo3"`, which ships no executable, so a 0.1.4 cut from HEAD as it is would remove the command line from pip altogether. The `main()` wrapper in `python/rustmapper/__init__.py` needs a `[project.scripts]` entry and a binary (or the native crawler) to call. | Concept A printed "the command is rust_sitemap, not rustmapper" as a hazard. All three judges said to fix that at the source and not advertise a packaging bug on the profile (R4 impl. 9, R6 impl. 4). | `Rust-sitemap:pyproject.toml` (`bindings = "pyo3"`), `sdist:pyproject.toml` (`bindings = "bin"`), `python/rustmapper/__init__.py` (`def main`) | Not blocking. The command in the image and in the code block comes from `edition.scripts`, the executables in the released wheel. Today that prints `rust_sitemap crawl`. After a 0.1.4 that ships `rustmapper`, it prints `rustmapper crawl` with no edit here. |

Only P1 blocks the image.

---

## 2. The image, element by element

### 2.1 What it looks like (desk; the phone stacks the same content)

```
Ben Russell                       rustmapper  RUST
CRAWL AND DATA INFRASTRUCTURE     Crawls a site and writes one line for every page it reaches.
PYTHON AND RUST                 ━━  pip install rustmapper                          0.1.3 · 8 NOV 2025
                                 ┃  rust_sitemap crawl --start-url <site>
1 OF 21 PUBLIC REPOSITORIES      ┃  prebuilt for macOS arm64 + Python 3.13; elsewhere pip needs Rust
CODE 32c2651 · 7 OCT 2026        ○  *_seeder.rs    start URL, plus seeds from sitemaps, CT logs, Common Crawl
CI ON MAIN PASSED 7 OCT 2026     ○  frontier.rs    one queue per host, paced by that host's robots.txt
AS OF 9 OCT 2026               ▨ ┃  subdomains are in scope and there is no depth limit
                                 ○  governor.rs    fewer fetch workers when redb commits lag
                                 ○  wal.rs         logged before stored; resume picks up after a kill
                               ▨ ┃  written when the crawl stops: press Ctrl-C once, not twice
                                ━━  data/sitemap.jsonl  one line per page: url, depth, status_code, title, …
                                 │  rust_sitemap export-sitemap → sitemap.xml
                                 ▼  read by ideal-url-organizer: scripts/import_rust_sitemapper.py, with a test
```

`━━` start and end bars, `┃` the track, `○` a stop, `▨` a trap (hatched block on the left of the track), `│▼` the
thinner line that carries the output on to another of his projects. Nothing else is drawn: no border, no sheet edge,
no axis, no islands, no tint, no light, no motion, no legend.

### 2.2 Element table

Every row says what a visitor learns, which question it answers, why this form, the evidence, and the data. "New"
means `build_stats` must gather it (section 5).

| ID | Element | Visitor learns | Q | Why this form | Evidence | Data |
|---|---|---|---|---|---|---|
| T1 | Name "Ben Russell", serif | whose page this is | Q1 | the first fact a screener reads; largest type, read first | R4-F1, F4 | `chart.toml [identity]`, shown name as today |
| T2 | Role line "CRAWL AND DATA INFRASTRUCTURE / PYTHON AND RUST" | what he builds, in the first two words | Q1 | the role line names what the picture shows: a crawler | R4 impl. 5, R5-F2 | `chart.toml [copy] role_line`, split at " · " |
| T3 | "1 OF 21 PUBLIC REPOSITORIES" | this is one chosen project; there are others, listed below | Q2 | a title block says what was selected and from what (from concept C and judge 3) | R1-F2, I7, I8 | `repo_count` (exists) |
| T4 | "CODE 32c2651 · 7 OCT 2026" | which version of the code the drawing was checked against, and how recent that code is | Q3 | the title block dates the source. The sha is a link-able fact for engineers; the date is the "alive" answer for everyone else | R1-F2, R2-F11, R4-F7 | **new** `repos[Rust-sitemap].head.short`, `.head.date` |
| T5 | "CI ON MAIN PASSED 7 OCT 2026" | the project's own tests pass on main, and when that was measured | Q3 | a measured status, computed, not a claim. It becomes "FAILED" by itself (from concept C). Words only, with no tick glyph, so it doesn't read as a stats badge (R4 impl. 14) | R4-F7, impl. 3 | `repos[Rust-sitemap].ci` (exists): `conclusion` success → PASSED, failure → FAILED, any other value → "LAST RUN <VALUE>"; `date` |
| T6 | "AS OF 9 OCT 2026" | when the build read all of this, so a stale "passed" can't pass as current | Q3 | the title block's "as of" | R1-F2 | `taken` (exists) |
| R0 | Header "rustmapper" serif + "RUST" + "Crawls a site and writes one line for every page it reaches." | which project, and what it does, before any detail | Q1, Q2 | a pilot-book entry opens with what the place is | R2-F2 item 1, R4-F8 | name `[hero.aliases]`, language `repos[].main_language` (exist); sentence `chart.toml [route.rustmapper] header` with anchors, **new** |
| R1 | Start bar | where you begin | Q4 | the entrance is a fixed point you find at once | R1-I5 | none (geometry) |
| R2 | `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the line that gets it, and that the release is older than the code drawn below | Q4, Q3 | the shortest correct start, first on the route. The version belongs at the install end, not on a timeline | R1-F10, I5; R4-F9; R5-F13; R6 impl. 8 | `edition.project`, `edition.version`, `edition.date` (exist). Drawn only if the run check passed (section 6) |
| R3 | `rust_sitemap crawl --start-url <site>` | the command that actually runs after pip | Q4 | wrong commands are the most common documentation failure | R4-F9, impl. 9; R6-F6 | **new** `edition.scripts`. Prints `rustmapper` if it is among them, else the first script. Empty list → build fails. Drawn only if the run check passed |
| R4 | Platform note "prebuilt for macOS arm64 + Python 3.13; elsewhere pip needs Rust" | whether pip will just work on their machine | Q5 | the condition for strangers, stated next to the entrance | R2-F3 | `edition.wheels` (exists), turned into words by `wheel_words()`. Omitted when wheels cover Linux x86_64, macOS arm64 and Windows x86_64 |
| R5 | Track, one magenta line from start bar to end bar | there is one way through, read top to bottom | Q4 | the line you follow, in the colour charts keep for what you act on; one line, one path | R1-F3, F6, I9; R3 impl. 8 | none |
| S1 | stop `*_seeder.rs` "start URL, plus seeds from sitemaps, CT logs, Common Crawl" | where URLs come from, and that he doesn't rely on links alone | Q1 | links alone miss pages (a directed path between two pages exists about 24 % of the time); seeders are the answer. Worded "plus seeds from" because the default differs (HEAD `none`, 0.1.3 `all`) and both can do it | R6-F3; R7-F3, F9 | anchors, **new** |
| S2 | stop `frontier.rs` "one queue per host, paced by that host's robots.txt" | it is polite by construction | Q1 | the Mercator frontier design, the core of a crawler, recognisable in one line | R6-F2 step 5; R7-F11 | anchors **new**; the HEAD anchors include P1's test file, so this stop can't be drawn over the 404 bug |
| H1 | trap "subdomains are in scope and there is no depth limit" | pointed at a big site, it crawls every subdomain to the bottom | Q5 | a known limit, stated as a fact at the stop where scope is decided | R2-F3; R1-F10 | anchors **new**: `is_same_domain` present, `max_depth` absent from `src/cli.rs`, in both trees |
| S3 | stop `governor.rs` "fewer fetch workers when redb commits lag" | the crawl slows when it can't save what it found, not when the network is slow | Q1 | his most unusual design choice. It states the mechanism, which is true in both versions; the worker counts are not (32–512 vs 256–1,024) | R4 impl. 10; R6-F7 | anchors **new** |
| S4 | stop `wal.rs` "logged before stored; resume picks up after a kill" | a crash doesn't lose the crawl, and there is a `resume` command | Q1, Q5 | the reason it is a durable tool | R6-F2 step 8 | anchors **new** |
| H2 | trap "written when the crawl stops: press Ctrl-C once, not twice" | the output file doesn't exist until the crawl ends. A first Ctrl-C saves and writes it; a second exits without writing it | Q5 | a real property of the tool, true in both versions, placed at the end where it bites | `Rust-sitemap:src/orchestration/shutdown.rs` ("Second Ctrl+C exits immediately", export after the first); `sdist:src/main.rs` (same strings) | anchors **new**; also exercised by the run check (one SIGINT, then the file must exist) |
| R12 | End bar | where you end up | Q4 | the berth: the file you open when the run is done | R2-F2 item 7, F9 | none |
| R13 | `data/sitemap.jsonl` "one line per page: url, depth, status_code, title, …" | what you get and where it is on disk, with the real field names | Q4 | the arrival view. Field names are the struct's, so a visitor who opens the file sees the same words | `Rust-sitemap:src/state.rs` and `sdist:src/state.rs` (`pub struct SitemapNode`) | anchors **new** |
| R14 | `rust_sitemap export-sitemap → sitemap.xml` (desk only) | the second output, and the command for it | Q4 | a sitemap is the product's name | `src/cli.rs` (`ExportSitemap`) in both | anchors **new**; command name from `edition.scripts` |
| R15 | Thin magenta line past the end bar, arrowhead, "read by ideal-url-organizer: scripts/import_rust_sitemapper.py, with a test" | his projects are one body of work: this output feeds another of them, and that join is tested | Q2 | the one hand-off proven by reader code and a test (from concept D). It is drawn only when the check passes, never as dashed or broken. Other joins stay off the image | concept D table, H1; `ideal-url-organizer:scripts/import_rust_sitemapper.py` (`URL_RECORD_FIELDS`, 15 fields, all in `SitemapNode` at HEAD and 0.1.3), `tests/test_import_rust_sitemapper.py` | **new** `handoffs[]` |

Order is fixed: T1–T6 in the left column; R0, R1, R2, R3, R4, S1, S2, H1, S3, S4, H2, R12, R13, R14, R15 down the route.

### 2.3 Placement and sizes

All values are sheet units. GitHub shows the desk sheet at ×0.68 (870 px column) and the phone sheet at ×0.54
(390 px). Type floors are the existing ones (`scripts/tokens.py` FLOORS): desk 19 semantic and 25 serif, phone 26 and
30. Roles are existing `tokens.ROLES` names except `project`, which is new (serif, desk 41, phone 40, tracking −1.0
and −0.5, grade none). Caps lines use role `label` with explicit tracking (desk 1.6, phone 1.0), as the current hero
does, because `check_type` allows only one `label-caps` run per sheet.

Widths of text are measured by `typeset` (ctx.k), never estimated. Where a line doesn't fit, it wraps at a word
boundary and every item below moves down by one line height. The baselines given are the targets for today's
strings; the gates in section 7 are the limits.

**Desk: 1280 × 620 (870 × 422 on screen; today's hero is 870 × 424).**

> Review round 14: superseded. The desk sheet is now the mid edition's stacked layout on a 1000-unit sheet
> (`scripts/sheets/route.py`: `SIZES["desk"] = (1000, 900)`, `L["desk"] = dict(L["mid"])`; 1000 × 707 today, gate 770).
> Side by side at 1280 its 19-unit words were 12.6 px in GitHub's 846 px column; stacked they are 16.1 px there and
> 14.6 px at a 1,200 px window (`checks/column.py` DESK-PX). The left-column and route-column coordinates below are
> kept as the record of the first build.

Left column, x 56 to 410:
- T1: role `display` set at 88 (the current hero's documented break), ink, baseline 128.
- T2: role `label`, 19, tracking 1.6, caps, ink, baselines 182 and 210.
- T3–T6: role `label`, 19, tracking 1.6, caps, `muted`, baselines 262, 290, 318, 346. In T4 the sha is a `machine`
  (Plex Mono 19) run in lowercase, `muted`, on the same baseline.

Route column: track at x 456; text starts at x 484; right limit x 1224; stop rules start at x 640.
- R0: "rustmapper" role `project` 41, ink, x 484, baseline 84. "RUST" role `label` 19 caps, `muted`, 16 after the
  name, same baseline. Sentence: role `label` 19, ink, baseline 118.
- R1: rect x 444, y 148, 24 × 4, fill `flare`.
- R2: `machine` 19, ink, baseline 178. Release label: `label` 19 caps tracking 1.6, `muted`, right-aligned at x 1224,
  same baseline.
- R3: `machine` 19, ink, baseline 206.
- R4: `label` 19, `muted`, baseline 234.
- R5: line x 456 from y 152 to y 486, stroke `flare`, weight BRUSH (3.4; night 4.08), butt caps.
- Rows at a 36 pitch: S1 276, S2 312, H1 348, S3 384, S4 420, H2 456.
  - Stop: ring centred (456, baseline − 6), r 6, stroke ink at PEN, fill `paper`. File name: `machine` 19, `ink2`,
    x 484. Rule: `label` 19, ink, x 640.
  - Trap: hatch block x 432 to 450, y baseline − 13 to baseline + 1. Three parallel 45° strokes at LINE weight
    (2.1; night 2.52) in `accent`, clipped to the block. Text: `label` 19, ink, x 484. Trap text is never red: `accent`
    on day paper is 4.09:1, under 4.5:1 for text. The hatch is a graphic and needs 3:1.
- R12: rect x 444, y 486, 24 × 4, fill `flare`.
- R13: `machine` 19, ink, x 484, baseline 516. Rule `label` 19, ink, 20 after the file name.
- R14: `machine` 19, `ink2`, x 484, baseline 544. The arrow is U+2192; add it to the Plex Mono subset
  (`scripts/fonts/subset.sh`) if it is missing.
- R15: line x 456 from y 490 to y 570, stroke `flare`, weight LINE. A filled triangle (`flare`) 10 wide and 8 tall,
  tip down at y 578. Label baseline 584 at x 484: "read by ideal-url-organizer:" in `label` 19 `ink2`, the path in
  `machine` 19 `ink2`, ", with a test" in `label` 19 `ink2`.

**Phone: 720 × about 1170 (390 × about 634 on screen; today's phone hero is 390 × 610).**

Same elements, same order, same words, except: no file names on stops (rules only), no R14 (the code block under the
image carries it), and the release label joins the platform note. Track at x 56, text at x 88, right limit x 688.
- T1: role `display` 132, baseline 140, x 40.
- T2: `label` 26 caps tracking 1.0, ink, baselines 196 and 230.
- Fine print, `label` 26 caps tracking 1.0, `muted`: 276 "CODE 32c2651 · 7 OCT 2026" (sha in `machine` 26),
  310 "CI ON MAIN PASSED 7 OCT 2026", 344 "1 OF 21 REPOSITORIES · AS OF 9 OCT 2026". These are T4, T5, then T3 and T6
  on one line.
- R0: "rustmapper" `project` 40 + "RUST" `label` 26 caps `muted`, baseline 412. Sentence `label` 26 ink, baselines
  452 and 486 (it wraps).
- R1: rect x 44, y 514, 24 × 4.
- R2: `machine` 26, baseline 552. R3: `machine` 26, baseline 586.
- R4: `label` 26 `muted`, baselines 620 and 654: "0.1.3 · 8 Nov 2025 · prebuilt for macOS arm64 + Python 3.13;"
  / "elsewhere pip needs Rust".
- Items at line height 34 and gap 12 (pitch 46 for one-line items): S1 700 and 734 (wraps), S2 780, H1 826, S3 872,
  S4 918, H2 964 and 998 (wraps). Stop ring r 8, PEN; hatch block x 26 to 48, 22 × 18, LINE strokes.
- R12: rect x 44, y 1022, 24 × 4. Track from y 518 to 1022.
- R13: `machine` 26, baseline 1060; rule `label` 26 on its own line, baseline 1094.
- R15: line x 56 from y 1026 to 1118, arrowhead tip at 1126; label `label` 26 `ink2`, baseline 1140:
  "read by ideal-url-organizer, with a test".
- Sheet height = last baseline + 30.

**Day and night.** Day uses `tokens.THEMES["day"]`, night uses `THEMES["night"]` with `W_NIGHT` weights and the
Light cuts for sans and mono, which the type engine already applies. Contrast on paper, computed for this spec:
day ink 12.5, ink2 8.3, muted 5.1, flare 4.6, accent 4.1 (graphic only); night ink 10.0, ink2 7.2, muted 5.7, flare
6.3, accent 6.1. Every text colour clears 4.5:1 in both. The day edition must stand alone, because the GitHub mobile
app may always serve it (R4 impl. 7).

**Editions.** Four files: `hero-day.svg`, `hero-night.svg`, `hero-phone-day.svg`, `hero-phone-night.svg`. Nothing
moves, so the still and motion editions would be the same file; the still files and the phone stills are no longer
built. `publish_chart.py` deletes `hero-still-*.svg` and `hero-phone-still-*.svg` from the chart branch.

---

## 3. What is removed, and why

| Removed | Why (project fact, not theme) | Evidence |
|---|---|---|
| Week islands, their sizes, shallows, the month axis | They encoded when he committed, as areas. A visitor doesn't travel a calendar, and the owner couldn't tell whether size meant project size or commits. "There's nothing about that teaches you anything." | owner, 9 Oct; R1-I2; R4 impl. 2; R5 test (fails 1–6) |
| One row per repository, its day count, the "15 more" row | lookups and activity counts; a list does it better, and the list is in the text | R3-F4; R4 impl. 3, 13; R5 test |
| "Fl 30s" light on Scrapy | a code only a sailor reads, one of three configured intervals, nothing a visitor acts on | R1-I6; R5-F13; R6-F7 |
| "0.1.3 · PyPI" mark on the timeline | kept as a fact, moved to the install line, where it is used | R5 test; R6 impl. 8 |
| Graduated border and the hairline sheet edge | graduations are latitude and longitude, and there are none. The paper colour already shows the sheet's extent | R1-F12 |
| Fine print "Datum main", Eastern time | facts no visitor needs, in the scarce top-left | R4 impl. 5 |
| Motion and the still editions | nothing in the subject moves on a period | concept A §2.3 |
| Concept A's hazard "the command is rust_sitemap, not rustmapper" | a packaging bug, fixed at the source (P4). The command printed is the one the wheel installs | all three judges; R4 impl. 9 |
| Concept A's hazard "crt.sh may stall it: --seeding-strategy sitemap" | false at HEAD, where the default is `none`; fails A's own "true in both" rule | `Rust-sitemap:src/cli.rs` vs `sdist:src/cli.rs`; judges 1–3 |
| Concept A's second image (Scrapy's route) | it doubled the phone page, put a third party's domain on the profile, and Scrapy's README already draws its stages twice. Its entrance and two traps move into a code block (section 4) | judges 1 and 3 |
| Concept D's broken and unbuilt joins (Data-visualizer `links`, Scrapy `stage1_discovery` columns, `seeds.jsonl`, `courses.parquet`) | true, but on the front page they read as "his projects don't fit together", and they are Ben's to-do list, not a visitor's. One sentence in text at most; the rest go to issues | judges 1 and 3; concept D §2 |
| `[hero] named_min`, `[claims.scrape_interval]`, `[claims.workers]` in `chart.toml` | nothing prints them now. `claims.workers` also cites a stale sha (`00a877d`) | `chart.toml` |

`weeks`, `week_days`, `months`, `tide`, `variation`, `hours` and `sweeps` stay in `stats.json` for the audit.
Nothing on the page prints them.

---

## 4. The page around the image

Order: the image, the links, who he is, rustmapper (verdict, how to run, why, where its output goes), Scrapy (the
same, as text), the rest. A heading block names the visitor question it answers.

| # | Block | Learns (Q) | Content and rule | Evidence |
|---|---|---|---|---|
| 1 | Image | Q1–Q5 | section 2. `<picture>` with three `<source>` (phone night, phone day, desk night) and `<img>` desk day; the reduced-motion sources go | R4-F4 |
| 1a | Alt text | Q1, Q4 | Built from the verified route, two sentences, ≤ 25 words (the `alt` check): "How to start Ben Russell's crawler rustmapper and what happens to a URL inside it. It ends at data/sitemap.jsonl; two traps are marked." The trap count and end file come from `routes`. | R4 impl. 12, F16 |
| 2 | Link line `rustmapper · Scrapy · PyPI · Email` | Q2 | unchanged. ideal-url-organizer is linked in block 8, because putting it ahead of Scrapy would demote Scrapy | R4 impl. 8 |
| 3 | "Ben Russell builds…", Languages, Stack | Q1 | unchanged | R4-F1 |
| 4 | rustmapper sentence + facts line | Q3 | sentence unchanged. Facts line: `Built on tokio, redb, rkyv, reqwest, clap · 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust`. "last commit 8 Aug 2026" is dropped: it is sweep-adjusted, and next to a 7 Oct CI pass and 7 Oct commits it "doesn't look exactly accurate". The image's code date answers "alive". Same rule for Scrapy's facts line. | judge 2; owner, earlier |
| 5 | Install code block, copyable (new marker `install:Rust-sitemap`, written from `edition.scripts`) | Q4 | `pip install rustmapper` / `rust_sitemap crawl --start-url <your-site>` / `rust_sitemap export-sitemap --data-dir ./data --output sitemap.xml`. Under it, the existing wheel note. Once P1 and P2 are at HEAD (their test files found), also: "Newer than the release: `cargo install --git https://github.com/BenjaminSRussell/Rust-sitemap`". Before that, the cargo line is not printed. Today's block prints `rustmapper crawl`, which fails with "command not found". | R4 impl. 9; R6-F6 |
| 6 | Two "why" bullets | Q1 | governor bullet unchanged. Seeds bullet reworded: "Can seed from sitemaps, Certificate Transparency logs and the Common Crawl index (`--seeding-strategy`): …" (the rest unchanged). The WAL and frontier bullets are cut, because the image says them. | R4-F8, impl. 10; R5 impl. 9 |
| 7 | (none) | | concept A's "one line of real output" is not added: its example uses `example.com`, which the `strings` check bans, and it is a format sample, not a crawl. Once rustmapper completes a permitted, dated crawl, one committed line may be added here. | judge 3, from B |
| 8 | Hand-off sentence (new marker `handoffs`, written from `handoffs[]`) | Q2 | "Its `data/sitemap.jsonl` is read by [ideal-url-organizer](…) (`scripts/import_rust_sitemapper.py`, with a test). Its Delta export for Scrapy's `stage1_discovery` table is not read by Scrapy yet." The second sentence follows the computed state of that join and changes when the code changes. | concept D; R6 impl. 2 |
| 9 | Scrapy sentence + facts line (no last commit) + new code block | Q3, Q4, Q5 | `cd Scraping_project     # from the clone root, start.py fails` / `python start.py         # the whole pipeline; needs docker and docker-compose` / `scrapy crawl scout -a allowed_domains=<domain> -a start_urls=<url>`. Under it: "Grafana opens on http://localhost:3000. Spiders run by name (`scout`), not by file name. The bundled config's sample URLs are a university's site; the last line points discovery at yours." | `Scrapy:README.md:86-96, 228-256`; `Scraping_project/start.py` (`REQUIRED_TOOLS`); `src/stage1/scout_spider.py` (`name = "scout"`) |
| 10 | Scrapy bullets | Q1 | 1, 2 and 4 unchanged. Bullet 3 corrected: "Near-duplicates are dropped by URL hash and MinHash. Most pages get an extractive summary in stage 3; documents over 50,000 characters go to stage 4, where bart-large-cnn runs on the worker itself, so nothing is sent to an external API." | `src/stage3/stage3_worker.py` (MinHash, "extractive summary"); `src/core/config.py` (`massive_doc_threshold=50000`); `src/stage4/summarization.py` (`facebook/bart-large-cnn`) |
| 11 | "Also" | Q2 | go_go_go rewritten: "rustmapper's counterpart in Go, with the same crawl, resume and export-sitemap commands. It adds headless-Chrome rendering, SQLite storage with full-text search, and browser TLS-fingerprint impersonation, all off by default." "100M+" and "same three seed sources" are dropped. The other three lines are unchanged. | `go_go_go:README.md` (flags table, defaults false); R6-F7, F9 |
| 12 | "15 more" `<details>` | Q2 | unchanged | R4 impl. 13 |
| 13 | Working rules | Q1 | rule 3 renamed "Dashboards before speed" (it was a pun on the theme; its own text says dashboards). The others are unchanged. | judge 2 |
| 14 | Data line (marker `survey`) | Q3 | "The drawing is checked against rustmapper's code at `<short>` and its `<version>` release on PyPI; every stop and trap names a file you can open, and the install lines are run weekly on macOS arm64. Test counts and CI results measured `<taken>` from clones of `<n>` public repositories · `<share>` % of my commits carry an AI co-author trailer; `<agent total>` more were written by coding agents (Claude, jules) and are not counted as mine · regenerated weekly." The bulk-edit clause goes, because no figure on the page uses commit-days now. | R2-F11; AUDIT.md |
| 15 | License line | | unchanged | |

Owner actions outside this repository: pin Rust-sitemap and Scrapy first, and make each pin's description match the
first sentence of its block (R4 impl. 11).

---

## 5. Data: what `build_stats` must gather

**Already in `stats.json` and used:** `repo_count`, `taken`, `edition.{project, version, date, wheels}`,
`repos[].{main_language, test_functions, ci, lines}`, `coauthored_total`, `agent_authored`.

**New keys (bump `stats_schema.json`; add one AUDIT.md row each):**

1. **`repos[name].head = {sha, short, date}`** for Rust-sitemap, Scrapy and ideal-url-organizer. `sha` is
   `git rev-parse HEAD` in the history clone `survey_all` already makes (`git_dirs[name]`). `short` is its first 7
   characters. `date` is `git log -1 --format=%cs HEAD`, the committer date of HEAD, with no sweep exclusion: it dates
   the code that was read, not his activity. Today: `32c2651`, 2026-10-07; `96e7a1a`, 2026-10-08; `159968a`,
   2026-10-07.

2. **`edition.scripts`**: the executables in the latest release's wheel, from its `RECORD`, entries matching
   `<name>-<version>.data/scripts/<exe>`, plus `[project.scripts]` / `console_scripts` names from
   `entry_points.txt` if present. If there is more than one wheel, take the union. Fetch the wheel URL from the PyPI
   JSON `pypi.py` already reads. Carry from the cache when `edition.version` is unchanged. Today `["rust_sitemap"]`.
   **`edition.sdist = {filename, sha256}`**: the latest release's sdist, downloaded per build (it is small) into the
   work directory for the release anchors below; not committed.

3. **`routes.rustmapper`**, written by the new `scripts/data/route.py` (about the size of `claims.py`) from
   `chart.toml [route.rustmapper]`:

   ```toml
   [route.rustmapper]
   repo = "Rust-sitemap"
   header = "Crawls a site and writes one line for every page it reaches."
   header_anchors = [{path = "src/url_utils.rs", text = "pub fn is_same_domain"}]

   [[route.rustmapper.entry]]
   id = "S1"
   kind = "stop"                         # stop | trap | end | export
   file = "*_seeder.rs"
   text = "start URL, plus seeds from sitemaps, CT logs, Common Crawl"
   head = [{path = "src/sitemap_seeder.rs"}, {path = "src/ct_log_seeder.rs"},
           {path = "src/common_crawl_seeder.rs"}, {path = "src/cli.rs", text = "seeding_strategy"}]
   release = [{path = "src/sitemap_seeder.rs"}, {path = "src/ct_log_seeder.rs"},
              {path = "src/common_crawl_seeder.rs"}, {path = "src/cli.rs", text = "seeding_strategy"}]
   ```

   An anchor is `{path}` (the file must exist), `{path, text}` (the file must contain the literal), or
   `{path, absent}` (the file must not contain it). `head` is checked in the Rust-sitemap clone at
   `repos[].head.sha`, through the existing `survey.file_at(git_dir, sha, path)` hook. `release` is checked in the
   unpacked sdist. **An entry is drawn only if every `head` and every `release` anchor holds** (concept A's "true in
   both" rule, now applied mechanically to HEAD as well). The anchors for today:

   | ID | head (Rust-sitemap 32c2651) | release (sdist 0.1.3) |
   |---|---|---|
   | S1 | as above | as above |
   | S2 | `src/frontier.rs` "struct ReadyHost"; `src/robots.rs` "fn fetch_robots_txt"; `tests/robots_4xx_allows_crawl.rs` (exists; **fails today until P1**) | `src/frontier.rs` "struct ReadyHost"; `src/robots.rs` "fn fetch_robots_txt" |
   | H1 | `src/url_utils.rs` "pub fn is_same_domain"; `src/cli.rs` absent "max_depth" | same |
   | S3 | `src/orchestration/governor.rs` "THROTTLE_THRESHOLD_MS" | `src/main.rs` "THROTTLE_THRESHOLD_MS" |
   | S4 | `src/wal.rs` "[u32 len][u32 crc32c][u128 seqno][payload]"; `src/cli.rs` "Resume {" | same |
   | H2 | `src/orchestration/shutdown.rs` "Force quit requested, exiting immediately" and `join("sitemap.jsonl")` | `src/main.rs`, same two strings |
   | R13 | `src/state.rs` "pub struct SitemapNode", "pub depth: u32", "pub status_code: Option<u16>", "pub title: Option<String>" | `src/state.rs`, same |
   | R14 | `src/cli.rs` "ExportSitemap" | `src/cli.rs` "ExportSitemap" |

   Output: `routes.rustmapper = {repo, head_sha, release, header, entries: [{id, kind, file, text, verified_head,
   verified_release, missing: [...]}]}`. The sheet draws from this key only. It never draws an entry that isn't
   verified and never drops one silently: an unverified entry fails `check.py --tier fast` (section 7), naming the
   entry and the missing string.

4. **`handoffs[]`**, written by `route.py` from `chart.toml [[handoffs]]`. Two joins are declared:

   - `sitemap-jsonl→ideal-url-organizer` (drawn as R15, and the first sentence of block 8). Writer fields: the `pub
     <name>:` lines inside `pub struct SitemapNode { … }` in `src/state.rs`, at HEAD and in the sdist. Reader fields:
     `URL_RECORD_FIELDS` in `ideal-url-organizer:scripts/import_rust_sitemapper.py` at its HEAD, read with
     `ast.literal_eval` on that assignment (not a regex). Test: `tests/test_import_rust_sitemapper.py` exists. State
     `runs` iff reader ⊆ writer at HEAD, reader ⊆ writer in the release, and the test exists; otherwise `fields
     differ` or `no reader`. R15 is drawn only when the state is `runs`.
   - `delta-export→Scrapy stage1_discovery` (text only, the second sentence of block 8). Writer:
     `Rust-sitemap:python/rustmapper/export_parquet.py` exists. Reader: any file in the Scrapy clone containing
     "rustmapper" or "Rust-sitemap". None today → `no reader` → "is not read by Scrapy yet".

   A parse that finds no struct or no list fails the build. It never yields an empty field set.
   Output per join: `{id, from, to, file, from_sha, to_sha, release, reader_fields, writer_fields_head,
   writer_fields_release, test, state}`.

5. **`runcheck.rustmapper`**: written by the weekly run check (section 6), merged by `build_stats` from the
   workflow artifact `runcheck.json`: `{date, runner, python, version, scripts, steps: [{cmd, ok, detail}], ok}`.

---

## 6. The run check: the image claims only what the tool does

A new job `runcheck` in `.github/workflows/profile.yml`, on `macos-14` (Apple silicon, the only platform with a
prebuilt wheel), with Python 3.13. The build job `needs` it and downloads its artifact. Driver:
`scripts/runcheck.py`, standard library only.

1. `python3.13 -m venv v && v/bin/pip install rustmapper==<edition.version>`.
2. For each name in `edition.scripts`: `<exe> --help` exits 0; `<exe> crawl --help` mentions `--start-url`;
   `<exe> export-sitemap --help` exits 0.
3. Serve `tests/fixtures/route-site/` (three HTML pages linking each other, **no robots.txt**) with
   `python3 -m http.server` on 127.0.0.1. Run `<exe> crawl --start-url http://127.0.0.1:<port>/ --seeding-strategy
   none --data-dir d`. After 45 s send **one** SIGINT and wait up to 60 s for exit. Pass if `d/sitemap.jsonl` has a line
   for each of the three pages with `status_code` 200 and the keys `url`, `depth`, `status_code` and `title`.
4. `<exe> export-sitemap --data-dir d --output s.xml`; pass if `s.xml` has three `<loc>`.

Step 3 tests R2, R3, S2 (a crawl actually starts on a site with no robots.txt), H2 (one Ctrl-C writes the file) and
R13 (the field names). If step 3 fails for the released 0.1.3, the image doesn't ship until a release passes. That
is the point: the entrance is drawn only when it works.

---

## 7. Tests that must hold

**Unit tests** (`tests/test_route.py`, new; `tests/test_hero.py` is replaced):

| Test | Holds when |
|---|---|
| T-ANCHOR | `route.py` marks an entry unverified when a `head` or `release` anchor is missing, a `text` is absent, or an `absent` string is present, and lists the failing anchor. Fixture trees, not the network. |
| T-BOTH | An entry true at HEAD and false in the release (fixture: `cli.rs` default `"all"` vs `"none"` for a seeding hazard) is unverified. This is the H2 case from concept A. |
| T-SCRIPTS | `edition.scripts` `["rust_sitemap"]` → R3 prints `rust_sitemap crawl`; `["rust_sitemap", "rustmapper"]` → `rustmapper crawl`; `[]` → the build raises. |
| T-WHEELS | `["cp313-cp313-macosx_11_0_arm64"]` → "prebuilt for macOS arm64 + Python 3.13; elsewhere pip needs Rust"; wheels for linux x86_64, macOS arm64 and win amd64 → no note. |
| T-CI | `ci.conclusion` success → "PASSED", failure → "FAILED", cancelled → "LAST RUN CANCELLED", with the run's date; `ci` absent → T5 omitted and `check.py` warns. |
| T-HANDOFF | Reader ⊆ writer at both trees with a test → `runs` and R15 drawn. Remove a field from the fixture struct → `fields differ`, R15 not drawn, no dashed or red line anywhere. A file with no `URL_RECORD_FIELDS` → build fails. |
| T-NOSIZE | Two stats fixtures differing in every count (`test_functions`, `lines`, `commits`, `repo_count`) give identical non-text geometry (every `rect`, `circle`, `path`, `line`, `polygon`). No shape's size depends on data. |
| T-SAME | Two builds from the same `stats.json` are byte-identical (R3 impl. 11). |
| T-PURPOSE | Each drawn element is a `<g id="…">` with an ID from section 2.2. The sheet's `PURPOSE` table (id → visitor learns → Q1–Q5 → source) has exactly those IDs: no drawn element without a row, no row without an element, and every row names a Q and a file, `stats.json` key or research finding. |
| T-ALT | The alt text is built from `routes`, is ≤ 25 words, doesn't start with "The", and names rustmapper and the end file. |
| T-WORDS | No text run in any edition, and not the alt text, matches whole-word, case-insensitive: chart, sea, ship, harbour, harbor, survey, unsurveyed, buoy, light, berth, approach, pilot, mariner, nautical, sail, anchorage, ahoy, arr. ("logged" and "CT logs" are project facts and allowed.) |
| T-BREAKS | Every reason in the sheet's `BREAKS` table names a project fact or a measured constraint; none says land, sea, water or chart without one. |

**`check.py --tier fast`** (new plug-in `scripts/checks/route.py`):
- ROUTE-UNVERIFIED (fail): any entry in `routes.rustmapper` with `verified_head` or `verified_release` false.
- ROUTE-ENTRANCE (fail): `runcheck.rustmapper` missing, `ok` false, `version` ≠ `edition.version`, or `date` more
  than 14 days before `taken`.
- ROUTE-STRINGS (fail): every text run on the hero comes from `routes`, `handoffs`, `edition`, `repos[].ci`,
  `repos[].head`, `repo_count`, `taken` or `chart.toml [copy]`/`[identity]`, and its report `truth` is `measured`
  (this extends the existing `strings` plug-in).
- The existing `strings` banned list still runs over README and SVGs.

**`check.py --tier render`:**
- Type floors as today: desk ≥ 19 semantic and ≥ 25 serif; phone ≥ 26 and ≥ 30. On a 390 px viewport, no text is
  under 14 px on screen.
- No text box overlaps another text box, a stop ring, a hatch block or the track (the `bounds` plug-in, extended to
  rings and hatches).
- Desk sheet height ≤ 640; phone ≤ 1200 (650 px on screen).
- Contrast: every text colour ≥ 4.5:1 on paper and every graphic ≥ 3:1, in both themes (the `contrast` plug-in).

**Owner's-goal tests, run by reviewers at every review round, with fresh research each round:**

1. **"What is it showing?"** Show the phone image alone for 10 s to five people who don't know Ben. Ask: what does he
   build; how would you start his main project; where does its output go; what is one catch? Pass if at least four
   say a crawler, name `pip install rustmapper` or the crawl command, name `sitemap.jsonl`, and name one trap
   (R4 impl. 1).
2. **"Is it based on the size of the project or how many commits?"** Ask what any shape's size means. Pass if the
   answer is "nothing has a size" (T-NOSIZE backs it).
3. **"Everything needs a purpose."** For each element, say in one sentence what a stranger learns from it without
   the theme being explained. Any empty sentence cuts the element (R4 impl. 13).
4. **"Chasing a purpose instead of having one."** Remove all colour, the hatch and the bars. The page must still read
   as directions for a stranger: how in, what happens, what goes wrong, where you end up (R2-I11).
5. **"It should be obvious; don't tell me it's a shoe."** No word names the theme (T-WORDS). The manner carries it:
   a course-up strip, the magenta line you follow, the danger side hatched, terse judgements, a dated title block.
6. **"The data doesn't look exactly accurate."** For every figure in the image (0.1.3, 8 Nov 2025, 3.13, 32c2651,
   7 Oct 2026, 21, 9 Oct 2026), a reviewer finds its key in `stats.json` and its AUDIT row, and for every stop and
   trap opens the file at the sha and finds the anchor.
7. **"I'm looking at iPhone."** On a real iPhone, in Safari and in the GitHub app (light and dark), the first two
   screens show his name, what he builds, rustmapper and Scrapy by name, and the link line (R4 impl. 6, 7). The
   profile header's height is measured on the device, not estimated.
8. **Run the commands.** Paste the README's rustmapper block into a clean Python 3.13 venv on macOS arm64. It runs.

---

## 8. Files to change in this repository

- `scripts/sheets/route.py` (new; `NAME = "hero"` so file names and README markers stay; `KIND = "chart"`;
  `SIZES = {"desk": (1280, 620), "phone": (720, 1170)}`; `EDITIONS = ("day", "night", "phone-day", "phone-night")`;
  `PURPOSE` and `BREAKS` tables). `scripts/sheets/hero.py` is retired, and `build_assets.py` loads `route` for the
  hero.
- `scripts/data/route.py` (new); `scripts/data/pypi.py` (`scripts`, `sdist`); `scripts/build_stats.py` (head, routes,
  handoffs, runcheck merge); `scripts/data/stats_schema.json`.
- `scripts/runcheck.py` (new); `tests/fixtures/route-site/` (new: `index.html`, `a.html`, `b.html`);
  `.github/workflows/profile.yml` (`runcheck` job).
- `scripts/render_readme.py`: `install:<repo>` and `handoffs` markers, facts line without the last commit, the new
  survey line, the picture element with four editions, `alt_for` from `routes`.
- `scripts/checks/route.py` (new); `strings`, `bounds` and `type` plug-ins extended as section 7 says.
- `scripts/tokens.py`: the new role `project` in `_DESK` and `_PHONE`.
- `chart.toml`: `[route.rustmapper]` and its entries, `[[handoffs]]`; notice 3 renamed; `[hero] named_min`, `[claims.scrape_interval]` and `[claims.workers]` removed, with the tests that pin
  them updated.
- `README.md` regenerated; `docs/data/AUDIT.md` rows for every new key; `DESIGN.md` hero section rewritten to this
  spec.
- `scripts/publish_chart.py`: prune the still editions from the chart branch.
