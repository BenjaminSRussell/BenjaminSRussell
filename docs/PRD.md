# PRD: Ben Russell's profile page

11 Oct 2026. Branch `v12/purpose` at `027f081` (23 commits past `main`, no PR). This document defines the final
product, lists every rule the owner set for it, and reviews how each rule is implemented: by a gate in `check.py`,
by a unit test, by a reviewer's judgement, or not at all. Section 7 is the register. Section 10 is what this review
found missing.

Sources: the owner's 26 messages in this session (appendix A, verbatim), `docs/crit/round6/SPEC.md` and
`DECISIONS.md`, `docs/crit/round5/DECISIONS.md`, `docs/crit/round6/LOG.md` (16 review rounds), the 48 reviews under
`docs/crit/round6/`, `docs/data/AUDIT.md`, `chart.toml`, the 28 gate plug-ins under `scripts/checks/`, the 539 tests
under `tests/`, `scripts/runcheck.py`, `.github/workflows/profile.yml`, and the round-16 renders.

---

## 0. Status, in five lines

- **Built.** The image and page described below exist on `v12/purpose`. `python3 -m unittest`: 539 tests, all pass.
  `check.py --tier fast,render` on the round-16 build: 0 fail, 4 warnings (§8.2), exit 2.
- **Reviewed.** 16 rounds, three reviewers each, research in every round (31 to 59 cited sources per round; 360 in the
  seven research files). No round reached a unanimous ship verdict. Best 9/9/8 (round 13); last 8/7/8 (round 16).
- **The blocker is outside this repository.** Every caution on the page is a measured fault of rustmapper 0.1.3. They
  are true, gated, and retire by themselves when a release fixes them (§5.4). Until then the top of the profile reads
  as a fault list for his flagship tool.
- **The owner's decision (§9.1):** release 0.1.4 from a fixed `Rust-sitemap` (recommended), move the cautions to
  rustmapper's own README, or ship as is.
- **Not pushed to `main`; no PR.** PR #17 (the thesis line cut) is still open and separate.

---

## 1. What the product is

A GitHub profile README, `BenjaminSRussell/BenjaminSRussell`, regenerated weekly from his repositories. One image at
the top, then text. The image is **the way into rustmapper**: how you install it, what it does with each page in
order, where it goes wrong, how you stop it, what file you get, and which other project of his reads that file. The
page under it is the lookup material: who he is, which project to open, the facts of each, how to run them, and the
rest of his work.

The product has a manner, not a theme. A navigator would recognise a route strip, a magenta track, a dotted danger
line and a cream sheet. Nobody is told. No word on the page names the sea.

**One sentence the image must answer** (SPEC §0): *how you start rustmapper, what happens to a URL inside it in order,
where a stranger goes wrong, and where the output goes next.* Every mark on the image either belongs to that sentence
or is cut.

**What it is not** (§4).

## 2. Who reads it and what they ask

Research R4 (57 sources on who reads GitHub profiles) gives the readers and the order of their questions. Every
element on the image and every block on the page is tagged with the question it answers; an element that answers
none is cut (test T-PURPOSE, gate ROUTE-PURPOSE).

| Q | The visitor's question | Who asks it first |
|---|---|---|
| Q1 | Who is this and what does he build? | a screener, about 7 s |
| Q2 | Which project should I look at? | a hiring engineer, a peer |
| Q3 | Does it work, and is it alive? | anyone about to try it |
| Q4 | How do I start it, and what do I get? | an engineer with a terminal open |
| Q5 | What will trip me up? | the same engineer, one minute later |

Two devices, by his instruction: **an iPhone (390 px, and 360 px Android) first, then a laptop** (GitHub's column is
766 to 846 px from a 1,200 px window; 482 to 765 px on an iPad held sideways).

## 3. Goals, in the owner's words, made operational

Each row is a thing he said (appendix A has the full text), what it means for the product, and where it is held.
"Gate" is a `check.py` finding code; "test" is in `tests/`; "review" means only a reviewer judges it.

| # | His words (date) | What it means here | Held by |
|---|---|---|---|
| G1 | "world class one of a kind beautiful profile readme that is stunning and fun and tells a lot about me" (7 Oct) | the standard of finish; a page that says what he builds and shows one of his tools working | review (every round's first question) |
| G2 | "Don't tell the user show the user you don't need to tell them it's a ships log or label everything it should be obvious" (8 Oct) | no label names the form; marks carry the manner | ROUTE-WORDS, STRINGS-BANNED, T-WORDS, DESIGN-FRESH; README prose: review only (§10.1) |
| G3 | "It's too dense in certain areas of the image... other parts... open, but you can't read anything" (9 Oct) | one left edge, fixed pitch, nothing placed by hand, nothing overlaps | BOUNDS-*, BOX-PAD, ROUTE-LEFT-EDGE, ROUTE-HEAD-GAP; T-NOSIZE |
| G4 | "I'm looking at iPhone... it has to be kind of accepting of all different formats" (9 Oct) | a phone edition drawn at its own width, served first; type floors on screen; the code block fits 32 columns | ROUTE-PHONE-PX, HERO-COLUMN-PX, HERO-FALLBACK, README-CODE-WIDTH, FLAG-WRAP, DESK-PX; device check still open (§9.3) |
| G5 | "Fuck saying ship's log. Just make it a log... If it looks like a shoe... You don't need to tell me it's a shoe" (9 Oct) | same as G2; also no themed headings | as G2; headings are plain ("Also", "Working rules") |
| G6 | "the images and the text need to... differentiate themselves... It should act like it doesn't know that it is" (9 Oct) | the image keeps what a list cannot show, the text keeps what you copy or look up; no fact said twice | STRINGS-TWICE, STRINGS-COUNT, HERO-SELF-TWICE |
| G7 | "how is the data gathered? The data doesn't look exactly accurate" (9 Oct) | every figure has a key, a definition and a source commit; every claim about code has an anchor in the code | AUDIT-STALE, AUDIT-COVER, FIGURES, ROUTE-UNVERIFIED, ROUTE-HEADER, NOTICE-*, STRINGS-UNMEASURED, ROUTE-STRINGS |
| G8 | "We don't need to show the commits... it feels lazy" (9 Oct) | no commit activity drawn; no commit totals printed | the image has no count; survey-line test bans `commits`, `all_hands`, `calendar_total`; the facts lines still print agent-authorship commit counts (owner's call, §9.2) |
| G9 | "Don't show me fucking ships unless it's like artfully well done... it's too on the nose" (9 Oct) | no ship, no boat, no buoy, no rose, no symbols at all; no legend | nothing drawn but bars, rings, a track, a dotted line; LEGEND-* idle |
| G10 | "Don't say arg like a fucking pirate... We're in a modern era... little jokes... one-off words... that's funny. Making it all about it... cringy" (9 Oct) | plain modern copy; at most a dry wink or two about the work, none nautical | THEME_WORDS has `ahoy`, `arr`; the winks are counted by review (two today, r16-3) |
| G11 | "The map, very helpful. The fucking log, not really... helpful knowledge... in a cool format" (9 Oct) | the image is directions a stranger uses; the log sheet is gone | the route; `log`, `instruments`, `approaches`, `soundings`, `footer` sheets are off the page |
| G12 | "the ship went off a cliff at the end? No... Unsurveyed?... not smart" (9 Oct) | no end-of-the-world device; no hatched margin; no "unsurveyed" | STRINGS-BANNED, THEME_WORDS (`unsurveyed`) |
| G13 | "It should be telling you about me, but with a layer of a theme of shipping" (9 Oct) | the page is about him and his work, in the third person | T1/T2, "Ben Russell builds", facts lines; `test_no_first_person_on_the_page`; THIS-REPO |
| G14 | "The wording is fucking weird survey the web that is wrong about itself" (9 Oct) | the thesis line is cut, everywhere | `chart.toml [copy]` has no `thesis`; EXPIRY-KEY (a stale review key fails) |
| G15 | "It's trying to be a fucking map for no reason... tiny fucking islands... Is it based on the size of the project or how many commits?" (9 Oct) | no shape has a size that depends on data; the picture exists only where the subject has a route to travel | T-NOSIZE; DECISIONS (four concepts scored on this goal) |
| G16 | "Every single fucking map needs a deep purpose... Everything, single thing inside of this needs a purpose, not a fucking chasing a reason" (9 Oct) | a PURPOSE row per drawn element: what a stranger learns, which Q, from which data | T-PURPOSE, ROUTE-PURPOSE; T-BREAKS (every design departure names a project fact) |
| G17 | "at least 10 reviews of, is it matching what I'm saying? Is it doing what I'm saying? Is it accomplishing my goal?" (9 Oct) | reviews that open with his goal, not with taste | 16 rounds; each review's first section is "does it meet the owner's goal" |
| G18 | "Do research on every single round... dozens of sources, hundreds of sources" (9 Oct) | research files per round; each review cites sources | R1–R7 (360); reviews cite 31 to 59 per round |
| G19 | "Use multiple agents and review and check and review and check" (9 Oct) | independent reviewers who do not see each other's drafts; a fix round between | the Workflow runs; `review-rNN-{1,2,3}.md` |

## 4. Non-goals

- Not a stats card. No stars, followers, streaks, commit totals, activity graphs, language pie.
- Not a themed poster. No ship, rose, buoyage, soundings, tide, light characters, chart number, "corrected through".
- Not a methods section. The provenance line is two facts (which release was drawn and that it was run), under 60
  words. How the build works is in `DESIGN.md`, linked once.
- Not a to-do list. Joins between his projects that do not work are not drawn (concept D's broken joins stay off).
- Not a second image. Scrapy's way in is a code block, not a drawing (judges 1 and 3; it doubled the phone page).
- Not animated. Nothing in the subject moves on a period, so nothing moves.

## 5. The product, element by element

### 5.1 The image

Six editions of one drawing, SVG, text as glyph outlines (no web fonts on GitHub). Order on the sheet is the order
of a run. Every element is a `<g id="hero-ID">` and has a row in `scripts/sheets/route.py` `PURPOSE`.

| ID | What is drawn | What a stranger learns | Q | Where the words come from | Drawn only when |
|---|---|---|---|---|---|
| T1 | "Ben Russell", serif | whose page | Q1 | `chart.toml [identity]` | always |
| T2 | "CRAWL AND DATA INFRASTRUCTURE / PYTHON AND RUST" | what he builds | Q1 | `[copy] role_line` (review by 2027-06, EXPIRY) | always |
| R0 | "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project, what it does | Q2 | `routes.rustmapper.header` | header anchors hold at HEAD and in the sdist; `crawl_ctrl_c` passed (ROUTE-HEADER) |
| R1 | start bar | where you begin | Q4 | geometry | always |
| R2 | `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the one command; how old the release is | Q4 | `edition.version`, `edition.date` (PyPI) | the run check passed, same version, ≤ 14 days old (ROUTE-ENTRANCE) |
| R5 | the magenta track | one way through, top to bottom; while the release never exits by itself the track breaks under the loop | Q4 | geometry; probe `ends_by_itself` | always; the gap follows the probe |
| R6 | the loop bracket up the left | these rows repeat for every page | Q1 | `bfs_crawler.rs frontier.add_links` | always |
| S1 | "`rust_sitemap crawl` starts from your URL; by default also from sitemaps, certificate logs and Common Crawl" | the command you type; where URLs come from; what it contacts by default | Q5 | `edition.scripts` (the wheel's executables); seeder files and `default_value = "all"` in the sdist; probe `crawl_help` | anchors hold; a fallback wording prints if `default_value = "none"` ships |
| S2 | "one queue per host, paced by that host's robots.txt" | polite by construction | Q1 | `frontier.rs`, `robots.rs` | **not drawn**: waits for a release with a Crawl-delay parser and the P1 test (ROUTE-WAITING) |
| F1 | "fetches up to 20 pages at a time from each host; queues their links to your site, its subdomains and its parent domain" | what a site feels; scope | Q1 | `state.rs max_inflight`, `url_utils.rs is_same_domain` | anchors hold in both trees |
| H0 | "on https, pages behind a disallowed link wait" (dotted box) | the first catch on a real site | Q5 | `frontier.rs` blocked branch; probes `robots_stall`, `robots_resume` | probe passed (code-only wording if skipped) |
| H1 | "0.1.3 never exits by itself; quit when `Received work item` lines stop for 60 s" (same box) | when to quit, and the sign | Q5 | `bfs_crawler.rs` select arm; `{quiet}` = timeout 20 + permit wait 30 + backoff, rounded (AUDIT §7) | probe `ends_by_itself` failed and `quiet_slow_page` passed; retires with a release that exits |
| W1 | "after a kill, export-sitemap still has the pages" | what logging before storing buys | Q5 | `writer_thread.rs` | **never drawn today**: `kill_writes_file` failed |
| C1 | "press Ctrl-C once and wait for `Saved to`; a second press quits without writing the file" | the reader's one step and its cost | Q5 | `main.rs` "Saved to:"; probes `crawl_ctrl_c`, `second_ctrl_c` | probes as stated |
| R12 | end bar | where you end up | Q4 | geometry | always |
| R13 | `data/sitemap.jsonl` "fields: url, depth, status_code, title, …" | what you get, with the real field names | Q4 | `state.rs pub struct SitemapNode` | anchors hold |
| R15 | thin line on, "sorted 21 ways by ideal-url-organizer" | his projects are one body of work | Q2 | `handoffs[]` state `runs` (reader fields ⊆ writer struct in both trees, test exists); `[[figures]]` "21 ways" at its HEAD | state `runs` |

Nothing else is drawn: no border, axis, legend, tint, hatch, symbol, light or motion. Every stroke width comes from
`chartlib.stroke`, every glyph from `typeset`. Trap text is ink inside a dotted accent line with no fill (accent on
day paper is 4.1:1, under the 4.5:1 text needs, over the 3:1 a line needs).

### 5.2 Editions and where each is served

| Edition | Sheet | Served at | Column there | Smallest text on screen |
|---|---|---|---|---|
| phone-day / phone-night | 600 × 1,121 | viewport ≤ 851 px; also the `<img>` fallback | 308 px on a 390 phone, 278 on a 360 | 13.3 px / 11.0 px (floor 13 / 11, ROUTE-PHONE-PX) |
| mid-day / mid-night | 820 × 707 | 852 to 1,199 px | 482 to 765 px | ≥ 14.5 px (DESK-PX) |
| day / night | 1,000 × 707 | ≥ 1,200 px | 766 to 846 px | 14.6 to 16.1 px (DESK-PX) |

Night is redrawn (strokes 20 % heavier, light cuts of the sans and mono), not inverted; every text colour clears
4.5:1 on paper in both (CONTRAST-*). The sheet is at most 900 px tall at any viewport from 360 to 1,920
(HERO-COLUMN-PX), so the loop, the catches, Ctrl-C and the file are on the first screen of a phone and of an iPad.
No still editions: nothing moves. The image links to the Rust-sitemap repository.

### 5.3 The page

In order. Marker blocks (`<!-- x:start -->…<!-- x:end -->`) are written by `scripts/render_readme.py` from
`stats.json` and `chart.toml`; the committed README must equal what the renderer writes (README-STALE).

| # | Block | Q | Rule |
|---|---|---|---|
| 1 | the image, `<picture>` with six sources, alt text | Q1–Q5 | alt ≤ 25 words, not starting "The", built from the drawn route (ALT-*, T-ALT) |
| 2 | links: rustmapper · PyPI · Scrapy · Email (+ LinkedIn, resume when `[contact]` is set) | Q2 | the position line prints when `[position] text` is set; "" omits it and warns (POSITION-EMPTY) |
| 3 | "Ben Russell builds…", Languages, Stack | Q1 | Languages: Python, Rust first, then every other `main_language` by repository count; the Stack line is his |
| 4 | the pick: which tool for which job | Q2 | printed only while rustmapper's header, every `pick` figure row and the `no_services` release gate hold; the politeness clause only while Scrapy's stage 2 checks robots.txt (it does not today, so it is off) |
| 5 | rustmapper facts line | Q3 | `head.short`, built-on (from the manifest, in `[facts]` order), `test_functions`, CI conclusion + date + gates, lines, agent-authored counts; a key that is absent is omitted, never estimated |
| 6 | the platform note, "Before you run 0.1.3:" cautions (≤ 7 items, ≤ 25 words each), a `<details>` fold for what the files miss, the code block (≤ 32 columns a line) | Q4, Q5 | each item is a gated wording with anchors and a probe; README-CAUTIONS, README-CD, README-SUBCOMMAND, FLAG-WRAP, README-CODE-WIDTH |
| 7 | Scrapy sentence, facts line, three bullets, how to run it, its two cautions, code block, where output lands | Q3–Q5 | same gating; every typed number has a `[[figures]]` row that holds at `96e7a1a` (FIGURES) |
| 8 | **Also**: ideal-url-organizer, go_go_go, rust_llm_logger, Ai_code_detector | Q2 | one line each; "21 ways" must match the image's count (STRINGS-COUNT) |
| 9 | `<details>` "15 more repositories" | Q2 | the count is computed (`repo_count` − profile − 2 − 4); every surveyed repository is linked once (REPO-SET) |
| 10 | **Working rules** 1–3 | Q1 | each cite's month is computed from his first commit that adds the anchor (NOTICE-DATE), the anchor is his, not an agent's (NOTICE-AUTHOR), and is live at HEAD (NOTICE-LIVE); typed numbers in a rule need a `block = "notices"` row |
| 11 | "Found a mistake? Open an issue." | | |
| 12 | provenance `<sub>`: which release was drawn, that its commands were run, when, where; tests and lines counted per repository | Q3 | ≤ 60 words; no "generated", no schedule, no commit totals, no instrument roll-call (test) |
| 13 | license `<sub>` | | present when `LICENSE` and `LICENSE-ASSETS.md` exist (README-LICENSE) |

### 5.4 What changes by itself

The page is a function of the state of his tools. Each conditional wording in `chart.toml` carries anchors (file
exists / contains / lacks a literal; a clap argument equals a value) checked at Rust-sitemap's HEAD and in the
released sdist, and the names of run-check probes that must have passed or failed. `scripts/data/route.py` resolves
them at every build; a wording whose conditions fail is replaced by its `instead` wording or dropped, and
ROUTE-UNVERIFIED fails the build if no wording of a drawn entry holds. Nothing conditional is edited by hand.

What a 0.1.4 cut from a fixed `main` does to the page, with no edit here:

| Fix in Rust-sitemap | Retires | Needs |
|---|---|---|
| exits when the frontier drains | H1, the gap in the track, the stop-rule comment in the code block | probe `ends_by_itself` passes |
| robots.txt 404 → allow; fetched with the URL's own scheme; fail closed until it arrives | L4's first clause, L6/H0 (the https stall) | `tests/robots_4xx_allows_crawl.rs` at HEAD; probes `robots_read`, `robots_stall` |
| `parse_crawl_delay_secs` in the release | draws S2; rewords L1 and L4 | release anchor |
| default UA with a contact; `From` | L7 | probe `ua_seen` (fails on a contact) |
| disallowed and `noindex` pages left out of `export-sitemap` | X1's clause | probe `sitemap_keeps_disallowed` fails |
| `[project.scripts] rustmapper` in the wheel | the image prints `rustmapper crawl` | `edition.scripts` from the wheel's RECORD |
| SIGTERM writes the file; `resume` after a kill | W1 drawn; "resume" allowed next to rustmapper | probes `kill_writes_file`, `resume_after_kill` |
| a LICENSE | the LICENSE-FLAGSHIP warning | GitHub detects it |

## 6. How the pipeline enforces it

```
build_stats.py  → assets/stats.json   clones (depth 1 + history), GitHub REST, PyPI JSON + wheel RECORD + sdist,
                                       runcheck.json; routes/handoffs resolved against the code
build_assets.py → assets/v9/hero-*.svg six editions; build-report.json with every text run's source and truth
render_readme.py → README.md marker blocks; tokens.py --md → DESIGN.md
check.py --tier fast,render           28 plug-ins; exit 0 pass · 1 fail · 2 warnings · 3 could not check
publish_chart.py                       force-push of the sheets to the orphan `chart` branch, before main is touched
```

- **Weekly job** (`profile.yml`): Sunday 06:20 UTC, on push to `main` (scripts, chart.toml, workflow), and on
  `repository_dispatch: release-published`. Job 1 `runcheck` on macos-14 installs the release and runs the probes;
  job 2 runs tests, builds, gates, publishes sheets, then commits stats + README + DESIGN.md to `main`. A failed gate
  publishes nothing; a failed sounding publishes last week's figures with a dated note.
- **Run check** (`scripts/runcheck.py`): 7 gate steps (venv, install, three `--help`s, crawl + one SIGINT, export)
  and 18 probes (`ends_by_itself`, `quiet_after_last_page`, `robots_read`, `ua_seen`, `robots_stall`,
  `blank_rows`, `robots_resume`, `robots_late`, `sitemap_keeps_disallowed`, `workers_cap`, `second_ctrl_c`,
  `non200_status`, `quiet_slow_page`, `redirect_kept`, `sitemap_keeps_noindex`, `kill_writes_file`,
  `export_after_kill`, `resume_after_kill`), each against a local fixture site over http or https. A probe that
  cannot run is `skipped`, never a pass (ROUTE-PROBE-SKIPPED).
- **Tests**: 539, `python3 -m unittest`, 22 s. Fixture trees, never the network.
- **Review**: three independent reviewers per round, each opening with "does it meet the owner's goal", each
  re-measuring every printed figure, each citing sources; a fix round applies or declines each must-fix with a reason
  in `LOG.md`.

## 7. The rules, and how each is implemented

Status: **gate** (`check.py` fails or warns), **test** (`unittest`), **review** (a reviewer judges it each round),
**process** (how the session works), **open** (not held by anything yet). The last column is where it lives.

### 7.1 Don't name the theme

| Rule | Status | Where |
|---|---|---|
| No theme word on the image or in its alt text: chart, sea, ship, harbour/harbor, survey, unsurveyed, buoy, light, berth, approach, pilot, mariner, nautical, sail, anchorage, ahoy, arr | gate, test | ROUTE-WORDS; `test_no_theme_words` (T-WORDS) |
| No theme word in DESIGN.md | gate | DESIGN-FRESH + `design.theme_words` |
| No theme word in the README's visible prose | **review only** | r16-3 grepped by hand; §10.1 proposes the gate |
| Banned phrases anywhere (SVGs, report, README, chart.toml): ILLUSTRATIVE, PENDING, SEEDED, NOT FOR NAVIGATION, Here be dragons, Fair winds, example.com, Oct 2024, "thanks for reading", "Hi I'm Ben", "drawn not templated", REFRESHED DAILY, lorem, TODO, FIXME, v7 | gate | STRINGS-BANNED |
| No themed headings; headings are "Also", "Working rules" | test | `test_committed_readme_is_the_one_chart_page`, round tests pin the headings |
| Every design departure from the type and layout rules names a project fact or a measured constraint, never the theme | test | T-BREAKS over `route.py BREAKS` |
| No pirate language | gate (image) | THEME_WORDS `ahoy`, `arr` |
| At most a dry wink or two, about the work, not the sea | review | r16-3 counted two: "Boring under load.", "why engines are hard" |
| No ships, boats, buoys, roses, lights, hatching, legends | test | T-PURPOSE: every mark is inside a PURPOSE group; the only shapes are bars, rings, lines, a dotted box |

### 7.2 Everything has a purpose; nothing has a size

| Rule | Status | Where |
|---|---|---|
| Every drawn element has a PURPOSE row (what is learned, Q1–Q5, source); no row without an element | gate, test | ROUTE-PURPOSE; `test_every_element_has_a_purpose` |
| No shape's size or position depends on any count (tests, lines, commits, repositories) | test | `test_nothing_has_a_size` (two stats fixtures differing in every count give identical geometry) |
| The image exists only where the subject has a route a visitor travels | decision | DECISIONS: four concepts scored on the goal; A chosen 22/30 on goal |
| Lookups (counts, languages, the other repositories) go in text, never in the picture | design | SPEC §0; the facts lines |
| One home per fact: no run of 5 words, or 3 words naming code or a date, both on the image and in the README's prose (exceptions: `pip install rustmapper`, `Received work item`) | gate | STRINGS-TWICE, HERO-SELF-TWICE |
| One count for one thing: the image's "21 ways" must appear in that repository's README line | gate | STRINGS-COUNT |

### 7.3 Honest data only

| Rule | Status | Where |
|---|---|---|
| Nothing invented or estimated; an absent key is omitted, never filled | gate, code | STRINGS-UNMEASURED (every hero text run's `truth` is `measured`); ROUTE-STRINGS (every run's key is an allowed source); `facts_block` prints only present keys (test) |
| Every figure printed has a register row with a definition, a key and a source commit | gate | AUDIT-STALE (the register is regenerated by `audit_figures.py`); AUDIT-COVER (every digit run on the image and page is covered) |
| Every number typed into README prose rests on a `[[figures]]` row that holds at that repository's HEAD | gate | FIGURES (`proof.py` re-reads the anchor) |
| Every claim about the code rests on anchors at HEAD and in the released sdist; drawn only when both hold | gate | ROUTE-UNVERIFIED, ROUTE-HEADER, ROUTE-LABEL, ROUTE-WAITING |
| The install and crawl commands are run, not quoted; the entrance is drawn only within 14 days of a passing run of the same version | gate, CI | ROUTE-ENTRANCE; the `runcheck` job |
| A subcommand named next to "rustmapper" must not be one the run check saw fail | gate | README-SUBCOMMAND |
| A working rule's cite month is computed from his first commit adding the anchor; the anchor is his, not an agent's; the code is live at HEAD | gate | NOTICE-DATE, NOTICE-AUTHOR, NOTICE-LIVE, NOTICE-ANCHORS |
| A skipped probe is never a pass; the code-only wording prints | gate | ROUTE-PROBE-SKIPPED; `test_skipped_is_not_a_pass` |
| Sweep days (bulk edits touching most repositories: 9–10 Nov 2025, 1 and 7 Oct 2026) are excluded from any activity figure | code, test | `sweep_dates`; `test_sweep_days_are_named_not_removed`; no activity figure is printed now |
| Test counts are functions (`#[test]`, `def test_`), never files; languages from lines in the clone, never the REST field; generated trees excluded | code, test | `test_test_function_patterns`, `test_main_language_per_repo_from_lines`, `[lines.exclude]` |
| Agent-authored commits are counted apart and never as his | code, test | `agent_authored`, `coauthored_total`; `test_agent_authored_and_agent_share` |
| No commit totals, no "last commit" (sweep-adjusted, contradicted the CI date) | test | the survey-line test bans them; the facts lines print no total of his own, only the agent-authorship counts (§9.2) |
| CI status is the API's conclusion for the last run on main, with its date and the jobs it gates on | code, gate | `repos[].ci`; CI-GATES warns when the gate list is empty |
| `scrape_interval` is read from the job, not the global | test | `test_scrape_interval_is_the_jobs_not_the_global` (no longer printed) |
| No placeholder survives: ⟨ ⟩, `<!-- POSITION`, TODO | gate | POSITION-PLACEHOLDER, README-PLACEHOLDER, README-TODO, STRINGS-BANNED |
| Two builds from the same stats are byte-identical | test | `test_two_builds_byte_identical` |
| Figures retire by themselves when the tool changes | code, test | `instead` wordings, `waits`, `fails`/`runs`; `test_retires_when_fixed`, `test_a_crawl_that_ends_retires_h1` |

### 7.4 Phone first, then desk

| Rule | Status | Where |
|---|---|---|
| A phone edition drawn at its own width (600 units), served to viewports ≤ 851 px and as the `<img>` fallback | test | `test_picture_order`; HERO-FALLBACK |
| No phone text under 13 px on a 390 px phone (image 308 px) or 11 px on a 360 (278 px) | gate | ROUTE-PHONE-PX |
| The sheet is one screen: ≤ 900 px tall at every viewport 360–1,920 | gate | HERO-COLUMN-PX |
| Desk words ≥ 14.5 px from a 1,200 px window; a mid edition for 852–1,199 | gate | DESK-PX; `test_the_old_breakpoint_fails_on_tablets` |
| Code block lines ≤ 32 columns (what a 360 px phone shows) | gate | README-CODE-WIDTH |
| A flag a reader types (`--workers 1`) never wraps mid-flag on a phone | gate (render) | FLAG-WRAP |
| Cautions: one list, ≤ 7 items, ≤ 25 words each; the file faults folded | gate | README-CAUTIONS, README-DETAILS |
| Type floors: desk and mid 19 (serif 25), phone 26 (serif 30); sizes on the scale | gate | TYPE |
| Nothing overlaps; every box inside the sheet less a 6-unit frame; words clear the dotted line by ≥ 8 units | gate | BOUNDS-* (fast), BOX-PAD (render) |
| Rows start at one left edge; the project name sits ≥ 2 role pitches under the role line | gate | ROUTE-LEFT-EDGE, ROUTE-HEAD-GAP |
| Contrast: text ≥ 4.5:1, lines ≥ 3:1, both themes; red/green kept apart for CVD | gate | CONTRAST-* |
| Night redrawn, not inverted | code | `tokens.THEMES`, `W_NIGHT` |
| Verified on a real iPhone, in Safari and the GitHub app, light and dark | **open** | LOG rounds 15–16 "still open" (§9.3) |
| Even density across the image | review | no metric; held indirectly by one pitch, one left edge, fixed marks |

### 7.5 Copy

| Rule | Status | Where |
|---|---|---|
| Third person throughout; no I, my, me | test | `test_no_first_person_on_the_page` |
| Never "this repository" on a profile | gate | THIS-REPO |
| "His Scrapy repository", not the framework; American spelling | review | `[copy] repo_words`; r07 |
| Existing wording stays unless cut; every change carries its review round in a `chart.toml` comment | process | the comments in `chart.toml` |
| The role line is re-read by 2027-06 | gate | EXPIRY-PASSED |
| Alt text ≤ 25 words, not starting "The", says what the image shows in plain words | gate, test | ALT-LONG, ALT-THE; T-ALT |
| Code in the code face; code spaces at the word space; no file names left of the track | gate | TYPE-CODE, ROUTE-CODE-SPACE, ROUTE-LABEL |
| The release label sits right after its command, never at the right edge | gate | ROUTE-RELEASE |
| No "generated by" line on the page; no schedule in the provenance | test | the survey-line test bans "generated", "regenerated", "weekly" |
| The thesis line is gone | config | `[copy]` and `[copy.review]` carry no `thesis` |
| Garden paths and reduced relatives read once | review | r16-3 |

### 7.6 Process

| Rule | Status | Where |
|---|---|---|
| Never push to `main`; the owner merges PRs | process | every change is on a branch; the weekly bot commit to `main` is the workflow's own, by his design |
| Commit messages end with the Co-Authored-By and Claude-Session trailers | process | the model name in the trailer follows the serving model |
| No "Generated by Claude Code" footer in PR bodies or comments; the server appends its own | process | his instruction of 8 Oct |
| The stop hook: commit and push before stopping | process | WIP commits when it fires |
| His email is used only to identify him | process | it is not on the page (the page's `mailto:` is the one he set) |
| At least 10 reviews, each against his words; research every round; multiple agents | process, done | 16 rounds × 3 reviewers; Workflow `wf_eee12105-794`; `LOG.md` |
| Report failures as they are | process | the ship verdict was never reached, and is reported so |
| Asks that only he can do go in `docs/BEN-TODO.md` | process | position, contact, LICENSE, the worker figure, the name |

## 8. Acceptance criteria for the final product

### 8.1 Mechanical (must all hold on the commit that merges)

1. `python3 -m unittest`: all pass.
2. `python3 scripts/check.py --tier fast,render` on a fresh build: 0 fail, 0 error; warnings only from §8.2.
3. `render_readme.py --check` clean; `DESIGN.md` and `docs/data/AUDIT.md` regenerated (README-STALE, DESIGN-FRESH,
   AUDIT-STALE).
4. A `workflow_dispatch` dry run of `profile.yml` on the branch: the macOS run check uploads, the build gates, the
   publish dry-runs.
5. The six editions exist on the `chart` branch before `README.md` names them (`publish_chart.unshipped`).

### 8.2 Warnings allowed today, each with an owner

| Warning | Why it stands | Who clears it |
|---|---|---|
| POSITION-EMPTY | `[position] text` is "" | Ben: one line, "role · city or timezone · open to / currently" |
| LICENSE-FLAGSHIP | Rust-sitemap has no LICENSE | Ben, in Rust-sitemap |
| ROUTE-WAITING S2 | 0.1.3 has no Crawl-delay parser; HEAD lacks the P1 test | Ben, 0.1.4 |
| log.shards | `claims.shards` is `num_cpus`, the machine has 8 | harmless; retire the claim with the log sheet |

### 8.3 Judged (each review round, in this order)

1. Does the image meet his goal: a purpose a stranger can state, nothing with a size, nothing that names the theme?
2. Is every figure true: re-measured from `stats.json`, the audit, the sdist and the clones?
3. Does the page read on a phone: one screen for the image, every word ≥ 13 px, nothing cut off?
4. Does it tell a stranger about him and which project to open?
5. Would the reviewer ship it as is?

The bar for "done" that he set: the reviewers answer yes to all five. Round 16: no (8/7/8). The must-fixes left were
copy (r16-3) and the meaning of a blank row and of `sitemap.xml` (r16-2), both now fixed; what remains is §9.1.

### 8.4 On a device (once, before merge)

Open the profile on an iPhone in Safari and in the GitHub app, light and dark; note which edition each serves, that
the image is one screen, and that the first two screens show his name, what he builds, rustmapper and Scrapy by name
and the link line. Log it in `LOG.md`.

## 9. Open decisions and items

### 9.1 The one decision: what the top of the profile says about rustmapper 0.1.3

Today the image's box and the page's "Before you run 0.1.3" list state six measured faults of the released tool.
Every one is true, probed and gated. Together they read as a warning label on his flagship.

| Option | What ships | Cost | What the pipeline does |
|---|---|---|---|
| **1. Fix Rust-sitemap and release 0.1.4** (recommended) | the same image with the box gone, S2 drawn, `rustmapper crawl` as the command; the cautions list shrinks to the platform note | work in Rust-sitemap: exits when idle, robots 404/scheme/fail-closed, Crawl-delay, UA with contact, export filters, `[project.scripts]`, SIGTERM write, `resume`, LICENSE, tests for each; a release | every caution retires on its own at the next weekly run (§5.4); `repository_dispatch: release-published` rebuilds at once |
| 2. Keep the route, move the cautions to rustmapper's README | the image as today; the page's list becomes one line linking the project's own "Known issues" | the image still draws H0/H1, because they are true of the release the image names | `[route.rustmapper]` items marked off-page; a new gate that the linked section exists |
| 3. Ship as is | today's branch | a visitor's first read of his main tool is its fault list | nothing |

This needs his call. Option 1 needs push access to `BenjaminSRussell/Rust-sitemap` in a session that has it.

### 9.2 Owner's calls carried in `docs/BEN-TODO.md`

- `[position] text` and `[contact] linkedin` / `resume` (empty since round 4).
- Keep or strike the agent-authorship counts on the facts lines ("coding agents (Claude) authored 45 of its 146
  commits…"): two memos said hiding them costs more than stating them; he said "we don't need to show the commits".
- `rustmapper` or `Rust-sitemap` as the printed name (the alias is in `chart.toml`).
- The rustmapper README's worker figure (code 256–1,024, README 32–512, PyPI 256).
- Scrapy: make the near-duplicate filter persist across passes; stage 2's robots check, delay and user agent.

### 9.3 Not yet verified

- The iPhone and GitHub-app check (§8.4).
- The `workflow_dispatch` dry run on the branch (the macOS run check installs the prebuilt wheel, so the install
  note will read differently from the Linux run that produced today's `stats.json`; the https probes depend on
  `sudo -n security add-trusted-cert` on macos-14 and may be skipped, which the gate reports as a warning).
- A real iPad at 852–1,199 px.

## 10. Gaps this review found

Rules that are held only by a reviewer's eye, or by nothing, with the proposed fix. None blocks the merge; each is a
small change in this repository.

1. **Theme words in README prose** (G2, G5). `theme_words` runs over the image, the alt and DESIGN.md, not over
   `README.md`'s visible prose. Add it to `checks/readme.py` with an allow-list for project facts ("Helm chart",
   "CT logs", "logged"). One function, one test.
2. **"Not too on the nose" has no count** (G10). The reviewers count winks by hand (two today). Record the allowed
   two phrases in `chart.toml [copy] winks` and fail a third unlisted one? Over-engineering; keep it in review, but
   write the current two into the review checklist (§8.3) so no round forgets to count.
3. **Even density** (G3). No metric. The one-pitch, one-edge, fixed-mark rules hold it by construction; a density
   check would be chasing a number. Keep it judged.
4. **The device check** (G4) is the one rule with nothing behind it. It must be done once, by him or on a device the
   session can reach, before the merge.
5. **Commit counts on the facts lines** (G8). The survey line bans them; the facts lines print agent-authorship as
   commit counts. The rule as he said it was about the chart; the page's counts are his decision (§9.2). Whichever
   way, write it into `chart.toml` so the renderer's `agent_clause` is a switch, not a code edit.
6. **"Generated" survives in two maintainer comments**: the README's first line ("regenerated weekly from
   assets/stats.json") and DESIGN.md's first line ("Generated by `python3 scripts/tokens.py --md`"). Both are HTML
   comments a visitor never sees, and the test guards only the provenance line. Fine as is; noted so the rule's
   scope is explicit: *no generated-by line a visitor can read*.
7. **The worktree's `assets/v9` is stale** (gitignored; it still holds v9 footer stills). `check.py` run without
   `--out-dir` on a stale tree fails on them. Not a product defect; `build_assets.py` first, or point the gate at the
   build. Worth a one-line note in `check.py`'s docstring.

## 11. Risks

- **Reading as a flowchart.** With the manner carried only by the track, the dots and the paper, a visitor may see a
  flowchart. The answer is drawing, never added symbols (DECISIONS, concept A risk 1). The round-13 and round-16
  reviewers did not raise it.
- **The weekly run check on macOS differs from the Linux run** that produced today's stats; wordings may shift on
  the first CI build (the install note, probe skips). The gate reports it; nothing false can print.
- **A 0.1.4 cut from HEAD as it stands removes the command line** (`bindings = "pyo3"`, no `[project.scripts]`):
  `edition.scripts` would be empty and the build would refuse to draw the entrance. Fix the packaging before
  cutting the release.
- **GitHub's rendering changes** (the 82 px mobile inset, the 846 px column, the `<picture>` support) were measured
  on the live page on 10 Oct 2026 and are constants in the checks; re-measure when the page looks wrong.

---

## Appendix A. The owner's words that bind this product (verbatim, in order)

- 7 Oct 15:30 — "This readme does not show an expert or high level smart person who has a massive interest in
  design i want to make this world class one of a kind beautiful profile readme that is stunning and fun and tells a
  lot about me"
- 7 Oct 17:18 — "It's mediocre and not exciting or well designed and intercut this feels basic"
- 7 Oct 17:40 — "Be intentional and research this need multiple waves of agents with opinions going over this and
  setting up expectations problems complaints issues with astetic what could Improve it is it interesting does it
  draw in the user what does it say about the person who made it refine and parallelize making expectations and
  standard that aren't so fucking boring and basic and low effort this should appear like it took a team months of
  work and years of workshopping to create and design and manufacture it should say more than it literally says and
  should have layers of depth and thoughts associated with it"
- 7 Oct 17:58 — "I want 30 different perspectives from 30 different agents all making a document of what needs to be
  done what's good and bad and why and ideas for fixes and improvements and high level ideas then 10 teachincal
  agents working together on ideas of how to implement all of the ideas into one cohesive masterpiece"
- 8 Oct 14:22 — "The images are all crushed and survey is weird / Wording is weird but it's cool / The images are
  not cool enough"
- 8 Oct 14:52 — "Don't tell the user show the user you don't need to tell them it's a ships log or label everything
  it should be obvious"
- 8 Oct 16:38 — "Merged check and this needs higher reviews"
- 8 Oct 23:24 — "I still don't like the design and methodology run all agent judgment for a second round and review
  and implementation"
- 9 Oct 11:32 — "The first image doesn't say anything about me or anything. It's a sailing thing, which I do fuck
  with. I think that's a cool concept, given that our picture is a sailboat going off a cliff. But it doesn't really,
  it's confusing. [...] It's too dense in certain areas of the image. You look at one area of the image, it's
  incredibly dense. The other parts, it's like kind of like open, but you can't read anything. If you're going to
  make an image, I'm looking at iPhone. I think the iPhone experience is going to be a very common one. [...] it has
  to be kind of accepting of all different formats, especially if you want to be able to know what the fuck it's
  trying to say about me. Yeah, it's a sailing theme, but it's a lot of the image, and it tells you ship's log. Fuck
  saying ship's log. Just make it a log. Like, it doesn't need to be something that says, I'm a ship. It can just be
  a ship. [...] If it looks like a shoe, it smells like a shoe, it's probably a fucking shoe. You don't need to tell
  me it's a shoe."
- 9 Oct 11:35 — "the images and the text need to kind of like either differentiate themselves a little bit, or
  don't go too far into the ship theme. [...] It should act like it doesn't know that it is. [...] we really need to
  be focused on, how is the data gathered? The data doesn't look exactly accurate. It looks like it's kind of like
  all over the place. We don't need to show the commits are kind of cool. The data is kind of cool that we're
  pulling, but at the same time, it feels lazy, and I don't really like that. [...] Don't show me fucking ships
  unless it's like artfully well done. And if you have the people reviewing it, the different ages, different
  opinions, yeah, it's cool, but it's fucking, it's too on the nose. Where's the fucking opinions there?"
- 9 Oct 11:37 — "we need many different agents [...] going through this entire fucking thought process with where
  I'm trying to get, which is a theme without telling me it's a fucking theme. [...] Don't say arg like a fucking
  pirate. Don't use pirate language. We're in a modern era. But if it's shipping themed, it should just feel
  shipping. And if there's little things, little jokes you can throw in, like one word, one-off words that are
  referenced being a pirate or some shit, like that's funny. Making it all about it too fucking much. No one wants
  that. It's just cringy. [...] the data we're showing should be helpful. [...] The map, very helpful. The fucking
  log, not really. And the ship went off a cliff at the end? No, it's fucking dumb. Unsurveyed? [...] that's not
  smart. It's not intelligent. [...] It should be telling you about me, but with a layer of a theme of shipping.
  [...] It has to be helpful knowledge. [...] you'd want it to be helpful data that you're looking at [...] and it's
  in a cool format."
- 9 Oct 19:39 — "The wording is fucking weird survey the web that is wrong about itself come the fuck on"
- 9 Oct 20:50 — "Review the mapping again, the first map. I just feel like there's something that doesn't speak to
  the actual projects. It's trying to be a fucking map for no reason. Like, what is that going to help? How does it
  help the user see my project? What is it showing? It feels like this is like chasing a purpose instead of having a
  purpose. [...] they're tiny fucking islands. That part makes no fucking sense to me at all. [...] Is it based on
  the size of the project or how many commits? There's nothing about that teaches you anything. So that's my main
  issue. Use multiple agents and review and check and review and check. Based on everything I've said, keep that as
  the highest like breakdown of, is that meeting my expectations or not? It should not be done until it goes over at
  least 10 reviews of, is it matching what I'm saying? Is it doing what I'm saying? Is it accomplishing my goal? Not
  just what I'm saying. My goal is to have a purpose behind each map. Every single fucking map needs a deep purpose.
  Every single, not even just maps. Everything, single thing inside of this needs a purpose, not a fucking chasing a
  reason. Do research. Do a lot of research. Do research on every single round of reviews and checks. Research. Get
  dozens of sources, hundreds of sources. Get reasons to make this worthwhile."
- 11 Oct 01:12 — "Review in incredible depth making an entire PRD for the final product and review all of the do and
  donts and specifically all of the rules that must be followed and review how they are implemented"

Standing instructions from earlier in the session: never push to `main` (he merges); the commit trailers; no
"Generated by Claude Code" in PR comments ("that's dumb and a waste of tokens"); honest data, nothing invented; the
stop hook's commit-and-push.

## Appendix B. Gate plug-ins and their codes

| Plug-in | Tier | Codes |
|---|---|---|
| alt | fast | ALT-LONG, ALT-THE, ALT-LAST, ALT-POEM, ALT-NO-README |
| audit | fast | AUDIT-STALE |
| audit_cover | fast | AUDIT-COVER |
| bounds | fast | BOUNDS-COLLIDE, BOUNDS-EDGE, BOUNDS-EXCLUSION, BOUNDS-MORE, BOUNDS-NO-MANIFEST, BOUNDS-TEXTURE |
| boxpad | render | BOX-PAD |
| column | render | HERO-COLUMN-PX, HERO-FALLBACK, DESK-PX |
| contrast | fast | CONTRAST-TEXT, -LINE, -DANGER, -TINT, -LIGHT, -LIGHTS, -RG, -CVD |
| data | fast | stats.json invariants (calendar, sweeps, keys) |
| design | fast | DESIGN-FRESH |
| expiry | fast | EXPIRY-PASSED, EXPIRY-KEY, EXPIRY-FORMAT |
| figures | fast | FIGURES |
| flash, motion (fast), frames (render), perf (perf) | — | idle: nothing moves (FRAMES-*, MOTION-*, FLASH-*, PERF-*) |
| legend | fast | idle: no symbols (LEGEND-*) |
| log | fast | log.shards and the log sheet's rules (off the page) |
| notices | fast | NOTICE-DATE, NOTICE-AUTHOR, NOTICE-CITE, NOTICE-ANCHORS |
| notices_live | fast | NOTICE-LIVE |
| position | fast | POSITION-EMPTY, -UNSET, -MISMATCH, -PLACEHOLDER, -COMMENT, -BLOCK, -STALE, CONTACT-PLACEHOLDER, README-PLACEHOLDER |
| readme | fast | README-MISSING, -PICTURE, -PICTURE-FOLDED, -DETAILS, -LICENSE, -STALE, -RENDER, -CODE-WIDTH, -CAUTIONS, -CD, -TODO, -SUBCOMMAND, LICENSE-FLAGSHIP, CI-GATES, THIS-REPO |
| repos | fast | REPO-SET |
| route | fast | ROUTE-UNVERIFIED, -WAITING, -PROBE-SKIPPED, -HEADER, -ENTRANCE, -LABEL, -HANDOFF, -STRINGS, -WORDS, -HEIGHT, -PAINT, -RELEASE, -ARROW, -CODE-SPACE, -LEFT-EDGE, -PHONE-PX, -PURPOSE, -HEAD-GAP, -MISSING, TYPE-CODE, HERO-SELF-TWICE |
| size | fast | SIZE-RAW, -GZ, -PHONE, -PAGE, -ELEMENTS, -TARGET, REPORT-* |
| strings | fast | STRINGS-BANNED, -UNMEASURED, -TWICE, -COUNT, -ALT, -MANIFEST, -README, -TOML |
| type | fast | TYPE (floors, scale, one label-caps run) |
| wrap | render | FLAG-WRAP |
| xml | fast | XML-PARSE, -FORBIDDEN, -EXTERNAL-HREF, -ID-DUP, -ID-PREFIX, -REF, -KEYTIMES, -FADE-BASE, -SET-LOOP, -SIZE, -VIEWBOX, -ROOT |

## Appendix C. Where the earlier standards stand

`docs/crit/STANDARDS.md` (8 Oct, v8) and `docs/crit/tech/MASTERPLAN.md` set the thesis line, islands sized by
commits, IALA buoyage, light characters, a chart number and "corrected through Notice N". Every one of those was
overturned by his messages of 9 Oct and by round 5 and round 6 decisions; they are kept as the record of what was
tried. What survives from them: the honesty convention (nothing illustrative is printed at all now, so upright vs
italic numerals is moot), the type engine and its floors, the budgets (SIZE-*), the XML rules, and the gate's four
exit codes.
