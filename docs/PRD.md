# PRD: Ben Russell's profile page

11 Oct 2026. Branch `v12/purpose` at `027f081` plus this document and its review rounds (no PR; `main` is 23 commits
behind `027f081`).

Sources: the owner's 21 messages in this session (the full text is `docs/crit/prd/owner-messages.md`; appendix A
excerpts the 15 that set a rule), `docs/crit/round6/SPEC.md` and `DECISIONS.md`, `docs/crit/round5/DECISIONS.md`,
`docs/crit/round6/LOG.md` (16 review rounds), the 48 reviews under `docs/crit/round6/`, `docs/data/AUDIT.md`,
`chart.toml`, the 28 gate plug-ins under `scripts/checks/`, the 539 tests under `tests/`, `scripts/runcheck.py`,
`.github/workflows/profile.yml`, the round-16 renders, the clone of `Rust-sitemap` at `32c2651`, and the three PRD
reviews under `docs/crit/prd/` (`LOG.md` there records what each round changed).

---

## 0. Status, in six lines

- **What this is.** The final product, every rule the owner set for it, and how each rule is implemented: by a gate
  in `check.py`, by a unit test, by a reviewer's judgement, or not at all. To build and accept the page, read §1, §2,
  §4, §5, §8, §9 and §11. The register is §3's last column, §7, §10 and appendix B. §7.6 and G17–G19 are how the
  session worked, not what the page is.
- **Built.** The image and page described below exist on `v12/purpose`. `python3 -m unittest`: 539 tests, all pass.
  `check.py --tier fast,render` on the round-16 build: 0 fail, 4 warnings (§8.2), exit 2.
- **Reviewed.** 16 product rounds, three reviewers each, research in every round (31 to 59 cited sources per round;
  360 in the seven research files). No round reached a unanimous ship verdict. Best 9/9/8 (round 13); last 8/7/8
  (round 16). PRD review round 1 (11 Oct): 7/6/6, all three "yes, this is what he asked for" (`docs/crit/prd/LOG.md`).
  These scores are as of the date above and go stale the day the next round runs.
- **The blocker is outside this repository.** Every caution on the page is a measured fault of rustmapper 0.1.3. They
  are true and gated. Four of the eight fixes in §5.4 retire their cautions on their own at the next weekly run;
  three need a probe or a fallback wording written here first, and one is a hand switch (§5.4, column "Needs here").
  Until then the top of the profile reads as a fault list for his flagship tool.
- **The owner's decision (§9.1):** release 0.1.4 from a fixed `Rust-sitemap` (1a minimum or 1b full, recommended),
  move the cautions to rustmapper's own README (2), cut the page's list to two items (2b), or ship as is (3). Until he
  decides, the branch stays unmerged and `main` does not change.
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

## 2. Who reads it and what they ask

Research R4 (57 sources on who reads GitHub profiles) gives the readers and the order of their questions. Every
element on the image and every block on the page is tagged with the question it answers; an element that answers
none is cut (test T-PURPOSE, gate ROUTE-PURPOSE).

| Q | The visitor's question | Who asks it first |
|---|---|---|
| Q1 | Who is this and what does he build? | a screener, about 7 s (R4-F1: the six facts screened in about 7 s) |
| Q2 | Which project should I look at? | a hiring engineer, a peer |
| Q3 | Does it work, and is it alive? | anyone about to try it |
| Q4 | How do I start it, and what do I get? | an engineer with a terminal open |
| Q5 | What will trip me up? | the same engineer, one minute later |

Two devices, by his instruction (9 Oct 11:32: *"likely look at it on the web and maybe on your iPhone. If they're
looking at your repos, it's definitely on the web"*): **both must work, each at its own width; the phone (390 px, and
360 px Android) is the stricter constraint, the web the likelier reader.** GitHub's column is 766 to 846 px from a
1,200 px window; 482 to 765 px on an iPad held sideways; the viewport less 82 px on a phone.

## 3. Goals, in the owner's words, made operational

Each row is a thing he said (appendix A has the text), what it means for the product, and where it is held. "Gate"
is a `check.py` finding code (fail unless marked warn); "test" is in `tests/`; "review" means only a reviewer judges
it; "open" means nothing holds it yet.

| # | His words (date) | What it means here | Held by |
|---|---|---|---|
| G1 | "world class one of a kind beautiful profile readme that is stunning and fun and tells a lot about me" (7 Oct) | the standard of finish; a page that says what he builds and shows one of his tools working | review (every round's first question; G1 has no test, the reviewer's yes to §8.3 q.1–4 is its proxy) |
| G1a | "it should say more than it literally says and should have layers of depth and thoughts associated with it" (7 Oct 17:40) | a second reading finds more: the loop bracket up the left (these rows repeat for every page), the gap in the track under the box (the release never exits), the thin line past the end bar (his projects hand each other files) | review (§8.3 q.1 names the three marks) |
| G1b | "is it interesting does it draw in the user what does it say about the person who made it" (7 Oct 17:40) | the page says what kind of engineer made it without saying so: measured figures with their source commits, commands that were run, faults stated with their fix beside them | review (§8.3 q.4) |
| G1c | "stunning and fun" (7 Oct) / "The images are not cool enough" (8 Oct 14:22) / "Wording is weird but it's cool" (8 Oct 14:22) | finish and wit. **The trade, in his words:** on 9 Oct he overrode "fun" for anything that names the theme ("too on the nose", "cringy"); the two winks (§7.1) are what remains of it. A later round does not reopen "fun" without re-reading 9 Oct 11:35 and 11:37 | review (§8.3 q.6) |
| G2 | "Don't tell the user show the user you don't need to tell them it's a ships log or label everything it should be obvious" (8 Oct) | no label names the form; marks carry the manner; no themed headings (the headings are "Also", "Working rules") | ROUTE-WORDS, STRINGS-BANNED, T-WORDS, DESIGN-FRESH; headings pinned by test (§7.1); README prose: review only (gap §10.1) |
| G3 | "It's too dense in certain areas of the image... other parts... open, but you can't read anything" (9 Oct) | one left edge, fixed pitch, nothing placed by hand, nothing overlaps | BOUNDS-*, BOX-PAD, ROUTE-LEFT-EDGE, ROUTE-HEAD-GAP; T-NOSIZE |
| G4 | "I'm looking at iPhone... it has to be kind of accepting of all different formats" (9 Oct) | a phone edition drawn at its own width; type floors on screen; the code block fits 32 columns; the web reader gets the desk edition | ROUTE-PHONE-PX, HERO-COLUMN-PX, HERO-FALLBACK, README-CODE-WIDTH, FLAG-WRAP, DESK-PX; the device check is §8.4 (open) |
| G5 | "Fuck saying ship's log. Just make it a log... If it looks like a shoe... You don't need to tell me it's a shoe" (9 Oct) | the same rule as G2, said again on 9 Oct; nothing further | as G2 |
| G6 | "the images and the text need to... differentiate themselves... It should act like it doesn't know that it is" (9 Oct) | the image keeps what a list cannot show, the text keeps what you copy or look up; no fact said twice | STRINGS-TWICE, STRINGS-COUNT, HERO-SELF-TWICE |
| G7 | "how is the data gathered? The data doesn't look exactly accurate" (9 Oct) | every figure has a key, a definition and a source commit; every claim about code has an anchor in the code | AUDIT-STALE, AUDIT-COVER, FIGURES, ROUTE-UNVERIFIED, ROUTE-HEADER, NOTICE-*, STRINGS-UNMEASURED, ROUTE-STRINGS |
| G8 | "We don't need to show the commits... it feels lazy" (9 Oct) | no commit activity drawn; no commit total printed, of any kind. **Ruled in PRD round 1 by his sentence: off by default** until he turns it on (§9.2) | the image has no count; the provenance-line test bans `commits`, `all_hands`, `calendar_total`; **open on the facts lines**, which still print the agent-authorship counts ("authored 45 of its 146 commits and co-signed 1 of his own 101"); the `[facts] agent_clause` switch is the fix (§10.5) |
| G9 | "Don't show me fucking ships unless it's like artfully well done... it's too on the nose" (9 Oct) | no ship, no boat, no buoy, no rose, no symbols at all; no legend | nothing drawn but bars, rings, a track, a dotted line; held by review (T-PURPOSE checks containment, not shape: §7.1); LEGEND-* idle |
| G10 | "Don't say arg like a fucking pirate... We're in a modern era... little jokes... one-off words... that's funny. Making it all about it... cringy" (9 Oct) | plain modern copy; at most a dry wink or two about the work, none nautical | THEME_WORDS has `ahoy`, `arr`; the winks are counted by review (two today, named in §8.3) |
| G11 | "The map, very helpful. The fucking log, not really... helpful knowledge... in a cool format" (9 Oct) | the image is directions a stranger uses; the log sheet is gone | the route; `log`, `instruments`, `approaches`, `soundings`, `footer` sheets are off the page (their modules and strings are still in the repository: §10.8) |
| G12 | "the ship went off a cliff at the end? No... Unsurveyed?... not smart" (9 Oct) | no end-of-the-world device; no hatched margin; no "unsurveyed" | STRINGS-BANNED, THEME_WORDS (`unsurveyed`) |
| G13 | "It should be telling you about me, but with a layer of a theme of shipping" (9 Oct) | the page is about him and his work, in the third person | T1/T2, "Ben Russell builds", facts lines; `test_no_first_person_on_the_page`; THIS-REPO; the position line and a contact are §8.1 item 6 |
| G14 | "The wording is fucking weird survey the web that is wrong about itself" (9 Oct) | the thesis line is cut, everywhere | `chart.toml [copy]` has no `thesis`; EXPIRY-KEY **warns** on a stale review key (never fails); the phrase is banned nowhere and `docs/BEN-TODO.md` round-4 item 1 still tells him to put it in his bio (§10.10) |
| G15 | "It's trying to be a fucking map for no reason... tiny fucking islands... Is it based on the size of the project or how many commits?" (9 Oct) | no shape has a size that depends on data; the picture exists only where the subject has a route to travel | T-NOSIZE; DECISIONS (four concepts scored on this goal) |
| G16 | "Every single fucking map needs a deep purpose... Everything, single thing inside of this needs a purpose, not a fucking chasing a reason" (9 Oct) | a PURPOSE row per drawn element: what a stranger learns, which Q, from which data | T-PURPOSE, ROUTE-PURPOSE; T-BREAKS (every design departure names a project fact) |
| G17 | "at least 10 reviews of, is it matching what I'm saying? Is it doing what I'm saying? Is it accomplishing my goal?" (9 Oct); "review every single detail I want so much attention to detail" (7 Oct 16:12) | reviews that open with his goal, not with taste; those three questions are §8.3 q.1–4 | 16 rounds; each review's first section is "does it meet the owner's goal" |
| G18 | "Do research on every single round... dozens of sources, hundreds of sources" (9 Oct) | research files per round; each review cites sources | R1–R7 (360); reviews cite 31 to 59 per round |
| G19 | "Use multiple agents and review and check and review and check" (9 Oct); "30 different perspectives from 30 different agents... then 10 teachincal agents" (7 Oct 17:58); "the different ages, different opinions... Where's the fucking opinions there?" (9 Oct 11:35); "Review and ensure this is something I want to see rounds of reviews and research" (11 Oct) | independent reviewers of distinct standpoints who do not see each other's drafts; a fix round between; the PRD itself is reviewed the same way | the Workflow runs; `docs/crit/panel30/`, `tech/`; `review-rNN-{1,2,3}.md`; `docs/crit/prd/review-r01-{1,2,3}.md` |

## 4. Non-goals

- Not a stats card. No stars, followers, streaks, commit totals, activity graphs, language pie.
- Not a themed poster. No ship, rose, buoyage, soundings, tide, light characters, chart number, "corrected through".
- Not a methods section. The provenance line is two facts (which release was drawn and that it was run), under 60
  words. How the build works is in `DESIGN.md`, linked once.
- Not a to-do list. Joins between his projects that do not work are not drawn (concept D's broken joins stay off).
- Not a second image. Scrapy's way in is a code block, not a drawing (judges 1 and 3; it doubled the phone page).
- Not animated. Nothing in the subject moves on a period, so nothing moves; no still editions are needed. This is the
  one home of that rule (FRAMES-*, MOTION-*, FLASH-* idle).

## 5. The product, element by element

### 5.1 The image

Six editions of one drawing, SVG, text as glyph outlines (no web fonts on GitHub). Order on the sheet is the order
of a run. Every element is a `<g id="hero-ID">` and has a row in `scripts/sheets/route.py` `PURPOSE`.

| ID | What is drawn | What a stranger learns | Q | Where the words come from | Drawn only when |
|---|---|---|---|---|---|
| T1 | "Ben Russell", serif | whose page | Q1 | `chart.toml [identity]` | always |
| T2 | "CRAWL AND DATA INFRASTRUCTURE / PYTHON AND RUST" | what he builds | Q1 | `[copy] role_line` (review by 2027-06, EXPIRY warns) | always |
| R0 | "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project, what it does | Q2 | `routes.rustmapper.header` | header anchors hold at HEAD and in the sdist; `crawl_ctrl_c` passed (ROUTE-HEADER) |
| R1 | start bar | where you begin | Q4 | geometry | always |
| R2 | `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the one command; how old the release is | Q4 | `edition.version`, `edition.date` (PyPI) | the run check passed, same version, ≤ 14 days old (ROUTE-ENTRANCE) |
| R5 | the magenta track | one way through, top to bottom; while the release never exits by itself the track breaks under the loop | Q4 | geometry; probe `ends_by_itself` | always; the gap follows the probe |
| R6 | the loop bracket up the left | these rows repeat for every page | Q1 | `bfs_crawler.rs frontier.add_links` | always |
| S1 | "`rust_sitemap crawl` starts from your URL; by default also from sitemaps, certificate logs and Common Crawl" | the command you type; where URLs come from; what it contacts by default | Q5 | `edition.scripts` (the wheel's executables); seeder files and `default_value = "all"` in the sdist; probe `crawl_help` | anchors hold and `crawl_help` passed; "if asked" prints when `default_value = "none"` ships; when `crawl_help` is absent the command is dropped and the row reads "starts from your URL; …" (wordings 3 and 4 in `chart.toml`) |
| S2 | "one queue per host, paced by that host's robots.txt" | polite by construction | Q1 | `frontier.rs`, `robots.rs` | **not drawn**: waits for a release with a Crawl-delay parser and the P1 test (ROUTE-WAITING) |
| F1 | "fetches up to 20 pages at a time from each host; queues their links to your site, its subdomains and its parent domain" | what a site feels; scope | Q1 | `state.rs max_inflight`, `url_utils.rs is_same_domain` | anchors hold in both trees. The printed words are the entry's **second** wording: the first ("fetches pages, fewer at once when saves average over 500 ms…") fails on purpose on `absent = "current_permits > MIN_PERMITS"` and returns by itself on a release whose governor drops that floor; the one row where a release changes the image's words without changing a fault |
| H0 | "on https, pages behind a disallowed link wait" (dotted box) | the first catch on a real site | Q5 | `frontier.rs` blocked branch; probes `robots_stall`, `robots_resume` | probe passed (code-only wording if skipped) |
| H1 | "0.1.3 never exits by itself; quit when `Received work item` lines stop for 60 s" (same box) | when to quit, and the sign | Q5 | `bfs_crawler.rs` select arm; `{quiet}` = timeout 20 + permit wait 30 + backoff, rounded (AUDIT §7) | probe `ends_by_itself` failed and `crawl_ctrl_c`, `quiet_after_last_page`, `quiet_slow_page` passed (`runs`/`fails` in `chart.toml`); retires with a release that exits |
| W1 | "saved as it goes; export works after a kill" | what logging before storing buys | Q5 | `writer_thread.rs` | **not drawn**: `drawn = false`, set by hand in `chart.toml` (round 15: no room on the phone sheet). Its wording holds *because* `kill_writes_file` failed (`fails`); a passing kill flips it to "logged to disk, then saved to redb, in batches" (`tests/test_round13.py:258`), drawn or not |
| C1 | "press Ctrl-C once and wait for `Saved to`; a second press quits without writing the file" | the reader's one step and its cost | Q5 | `main.rs` "Saved to:"; probes `crawl_ctrl_c`, `second_ctrl_c` | probes as stated |
| R12 | end bar | where you end up | Q4 | geometry | always |
| R13 | `data/sitemap.jsonl` "fields: url, depth, status_code, title, …" | what you get, with the real field names | Q4 | `state.rs pub struct SitemapNode` | anchors hold |
| R15 | thin line on, "sorted 21 ways by ideal-url-organizer" | his projects are one body of work | Q2 | `handoffs[]` state `runs` (reader fields ⊆ writer struct in both trees, test exists); `[[figures]]` "21 ways" at its HEAD | state `runs` |

Nothing else is drawn: no border, axis, legend, tint, hatch, symbol or light. Every stroke width comes from
`chartlib.stroke`, every glyph from `typeset`. Trap text is ink inside a dotted accent line with no fill (accent on
day paper is 4.1:1, under the 4.5:1 text needs, over the 3:1 a line needs).

### 5.2 Editions and where each is served

| Edition | Sheet | Served at | Column there | Smallest text on screen (19-unit runs on desk and mid, 26 on the phone, per the build report) |
|---|---|---|---|---|
| phone-day / phone-night | 600 × 1,121 | viewport ≤ 851 px; also the `<img>` fallback | 308 px on a 390 phone, 278 on a 360 | 13.3 px on a 390, 12.0 px on a 360 (floors 13 / 11, ROUTE-PHONE-PX) |
| mid-day / mid-night | 820 × 707 | 852 to 1,199 px | 482 to 765 px | **11.2 px at 852 to 17.7 px at 1,199** (floor 11, HERO-COLUMN-PX; DESK-PX does not run here). Under the phone's 13 px up to a 930 px window; 13.7 px on a 1,024 px iPad held sideways (§9.3, §11) |
| day / night | 1,000 × 707 | ≥ 1,200 px | 766 to 846 px | 14.6 to 16.1 px (DESK-PX, from 1,200) |

Night is redrawn (strokes 20 % heavier, light cuts of the sans and mono), not inverted; every text colour clears
4.5:1 on paper in both (CONTRAST-*). The sheet is **at most 900 px tall from a 768 px viewport up** (HERO-COLUMN-PX,
`TALL_FROM = 768`, `column.py:47`); below 768 the profile is one column and the phone sheet is drawn 1.87 × the
column tall (575 px on a 390 phone; 968 px at a 600 px window; 1,280 at 767). So the loop, the catches, Ctrl-C and
the file are on the first screen of a phone and of an iPad held sideways; an iPad held upright (744 px) scrolls.
The image links to the Rust-sitemap repository (`tests/test_pipeline.py:208`).

### 5.3 The page

In order. Marker blocks (`<!-- x:start -->…<!-- x:end -->`) are written by `scripts/render_readme.py` from
`stats.json` and `chart.toml`; the committed README must equal what the renderer writes (README-STALE).

| # | Block | Q | Rule | Held by |
|---|---|---|---|---|
| 1 | the image, `<picture>` with six sources, alt text | Q1–Q5 | alt ≤ 25 words, not starting "The", built from the drawn route | ALT-*, T-ALT; `test_picture_order` |
| 2 | links: rustmapper · PyPI · Scrapy · Email (+ LinkedIn, resume when `[contact]` is set) | Q2 | PyPI sits beside rustmapper; the position line prints when `[position] text` is set (§8.1 item 6) | `tests/test_round7.py:370`; `tests/test_pipeline.py:495` (block order); POSITION-* |
| 3 | "Ben Russell builds…", Languages, Stack | Q1 | Languages: Python, Rust first, then every other `main_language` by repository count; the Stack line is his | `tests/test_round7.py:91` (the set, and "Python, Rust; " first); the order of the rest by count: no test (§10.9) |
| 4 | the pick: which tool for which job | Q2 | printed only while rustmapper's header, every `pick` figure row and the `no_services` release gate hold; the politeness clause only while Scrapy's stage 2 checks robots.txt (it does not today, so it is off) | `test_pipeline.py:206–210`; FIGURES |
| 5 | rustmapper facts line | Q3 | `head.short`, built-on (from the manifest, in `[facts]` order), `test_functions`, CI conclusion + date + gates, lines; a key that is absent is omitted, never estimated. The agent-authorship commit counts print today against G8 (§9.2) | `test_facts_block_prints_only_present_keys`; CI-GATES |
| 6 | the platform note, "Before you run 0.1.3:" cautions (≤ 7 items, ≤ 25 words each), a `<details>` fold for what the files miss, the code block (≤ 32 columns a line) | Q4, Q5 | each item is a gated wording with anchors and a probe. The three comment lines of the code block ("# 0.1.3 runs until stopped: when / # "Received work item" stops / # for 60 s, then Ctrl-C once") are wrapped at 32 columns for the phone's sake (the commands break at a backslash, which reads the same at any width); Markdown serves one block to every width, so the desk reader sees the comments phone-wrapped (§11) | README-CAUTIONS, README-CD, README-SUBCOMMAND, FLAG-WRAP, README-CODE-WIDTH; `test_no_fenced_line_over_32` |
| 7 | Scrapy sentence, facts line, three bullets, how to run it, its two cautions, code block, where output lands | Q3–Q5 | same gating; every typed number has a `[[figures]]` row that holds at `96e7a1a` | FIGURES |
| 8 | **Also**: ideal-url-organizer, go_go_go, rust_llm_logger, Ai_code_detector | Q2 | one line each; "21 ways" must match the image's count | STRINGS-COUNT |
| 9 | `<details>` "15 more repositories" | Q2 | the count is computed (`repo_count` − profile − 2 − 4); every surveyed repository is linked once | `render_readme.more_count`; REPO-SET |
| 10 | **Working rules** 1–3 | Q1 | each cite's month is computed from his first commit that adds the anchor, the anchor is his, not an agent's, and is live at HEAD; typed numbers in a rule need a `block = "notices"` row | NOTICE-DATE, NOTICE-AUTHOR, NOTICE-LIVE, NOTICE-ANCHORS |
| 11 | "Found a mistake? Open an issue." | | its presence and position only | `test_pipeline.py:506` (block order); nothing else |
| 12 | **the provenance line**, a `<sub>`: which release was drawn, that its commands were run, when, where; tests and lines counted per repository | Q3 | ≤ 60 words; no "generated", "regenerated", "weekly"; no commit total (`commits`, `all_hands`, `calendar_total`); no instrument roll-call | `test_provenance_line_is_from_stats_only` (`tests/test_pipeline.py:307`), called "the provenance-line test" everywhere in this document |
| 13 | license `<sub>` | | present when `LICENSE` and `LICENSE-ASSETS.md` exist | README-LICENSE |

### 5.4 What changes by itself

The page is a function of the state of his tools. Each conditional wording in `chart.toml` carries anchors (file
exists / contains / lacks a literal; a clap argument equals a value) checked at Rust-sitemap's HEAD and in the
released sdist, and the names of run-check probes that must have passed or failed. `scripts/data/route.py` resolves
them at every build; a wording whose conditions fail is replaced by its `instead` wording or dropped, and
ROUTE-UNVERIFIED fails the build if no wording of a drawn entry holds. Nothing conditional is edited by hand, **except
W1's `drawn = false`** (§5.1).

What a 0.1.4 cut from a fixed `main` does to the page. The last two columns were checked in PRD round 1: "At HEAD"
by reading the clone at `32c2651`; "Needs here" by running `scripts/data/route.py resolve()` on today's `stats.json`
with the probe in question flipped.

| Fix in Rust-sitemap | Retires | Needs from the release | At HEAD `32c2651`? | Needs here, first |
|---|---|---|---|---|
| exits when the frontier drains | H1, the gap in the track, the stop-rule comment in the code block | probe `ends_by_itself` passes | yes: `tests/crawl_exits_when_idle.rs` exists (it runs with `--ignore-robots`, so the M1 anchor `absent "--ignore-robots"` fails and M1 is not printed); not in the release | nothing (verified: H1 → `""`, retired) |
| robots.txt 404 → allow; fetched with the URL's own scheme; fail closed until it arrives | L4's https clause, L6/H0 (the https stall) | `tests/robots_4xx_allows_crawl.rs` at HEAD; probes `robots_read` passes, `robots_stall` fails | no: no such test; `src/robots.rs:16` still asks `https://<host>/robots.txt` only | nothing (verified: H0 and L6 → `""`, L4 drops "and reads `robots.txt` only over https") |
| `parse_crawl_delay_secs` in the release | draws S2; rewords L1 and L4 | the release anchor; probe `crawl_delay_obeyed` | yes: `src/robots.rs:53`, used at `src/frontier.rs:911–918`; not in the release | **a probe `crawl_delay_obeyed` in `runcheck.py`** (named at `chart.toml:1080, 1155, 1160`; its comment at 1074 says "not written yet"; the run check has no such step). Without it every L1/L4 wording for a parsing release needs a probe that never ran, both go unverified and ROUTE-UNVERIFIED fails the build |
| default UA with a contact; `From` | L7 | probe `ua_seen` fails on a contact | no: `src/cli.rs:40` default `RustSitemapCrawler/1.0`; no `From` in `src/network.rs` | **an `instead` on L7 with `fails = ["ua_seen"]`, `text = ""`** (verified: with `ua_seen` failed L7 has no wording that holds and goes unverified; the build fails) |
| disallowed and `noindex` pages left out of `export-sitemap` | X1's clauses | probes `sitemap_keeps_disallowed`, `sitemap_keeps_noindex` fail | no: no `noindex` handling in `src/` | nothing for the disallowed clause (verified: X1 drops "and disallowed"); **a wording for a release that also drops `noindex` pages** (verified: with both probes failed X1 goes unverified) |
| `[project.scripts] rustmapper` in the wheel | the image prints `rustmapper crawl` | `edition.scripts` from the wheel's RECORD | no: `pyproject.toml:55 bindings = "pyo3"`, no `[project.scripts]` (§11) | nothing |
| SIGTERM writes the file; `resume` after a kill | W1 drawn; "resume" allowed next to rustmapper | probes `kill_writes_file`, `resume_after_kill` pass | no: no signal handler in `src/` | **lift W1's `drawn = false` by hand and write a wording that holds on a passing kill** (verified: a passing `kill_writes_file` prints the fallback "logged to disk, then saved to redb, in batches" and W1 stays undrawn, as `test_round13.py:258` pins); `resume_after_kill` is named by no entry, only a comment |
| a LICENSE | the LICENSE-FLAGSHIP warning | GitHub detects it | no | nothing |

So four of the eight rows retire by themselves (exit, robots, export's disallowed clause, LICENSE), the packaging row
is pure release work, and three rows (Crawl-delay, User-Agent, SIGTERM) plus the `noindex` half of the export row
need a probe or a wording in this repository before a fixed release helps rather than fails the build (§10.9).

## 6. How the pipeline enforces it

```
build_stats.py  → assets/stats.json   clones (depth 1 + history), GitHub REST, PyPI JSON + wheel RECORD + sdist,
                                       runcheck.json; routes/handoffs resolved against the code
build_assets.py → assets/v9/hero-*.svg six editions; build-report.json with every text run's source and truth
render_readme.py → README.md marker blocks; tokens.py --md → DESIGN.md
check.py --tier fast,render           28 plug-ins; exit 0 pass · 1 fail · 2 warnings · 3 could not check
publish_chart.py                       force-push of the sheets to the orphan `chart` branch, before main is touched
```

- **Weekly job** (`profile.yml`): Sunday 06:20 UTC, on push to `main` (scripts, chart.toml, workflow, `assets/log.json`,
  `requirements.txt`), and on `repository_dispatch: release-published`. Job 1 `runcheck` on macos-14 installs the
  release and runs the probes; job 2 runs tests, builds, gates, publishes sheets, then commits stats + README +
  DESIGN.md to `main`. A failed gate publishes nothing. A failed data fetch (`steps.stats` failed) runs
  `build_assets.py --no-sounding --heartbeat` and the renderer on the last committed `stats.json`: the route sheet
  and the page are rebuilt from last week's figures **with their old dates and no stale mark** (`no_sounding` is read
  only by the off-page `log` and `soundings` sheets; the one test of the path, `tests/test_pipeline.py:47`, builds
  `log`). §6.1 has the rest.
- **Run check** (`scripts/runcheck.py`): 7 gate steps (venv, install, three `--help`s, crawl + one SIGINT, export)
  and 18 probes (`ends_by_itself`, `quiet_after_last_page`, `robots_read`, `ua_seen`, `robots_stall`,
  `blank_rows`, `robots_resume`, `robots_late`, `sitemap_keeps_disallowed`, `workers_cap`, `second_ctrl_c`,
  `non200_status`, `quiet_slow_page`, `redirect_kept`, `sitemap_keeps_noindex`, `kill_writes_file`,
  `export_after_kill`, `resume_after_kill`), each against a local fixture site over http or https. A probe that
  cannot run is `skipped`, never a pass (ROUTE-PROBE-SKIPPED).
- **Tests**: 539, `python3 -m unittest`, 22 s. Fixture trees, never the network. 69 of them (`test_supporting` 24,
  `test_timeline` 26, `test_approaches` 19) test sheets that are off the page; the product's own count is 470.
- **Review**: three independent reviewers per round, each opening with "does it meet the owner's goal", each
  re-measuring every printed figure, each citing sources; a fix round applies or declines each must-fix with a reason
  in `LOG.md`.

### 6.1 Failure and rollback

| Event | What the visitor sees | How it is undone, by whom |
|---|---|---|
| the data fetch fails | the page as last week, same dates, no stale mark (above) | nothing to undo; §10.13 asks whether a mark should exist |
| a gate fails (exit 1 or 3) | nothing new: the page and the `chart` branch as before | nothing to undo; the run's `::error::` lines say what failed |
| a build passes the gates and prints something wrong | the new page | Ben, or a session, `git revert`s the bot commit on `main`; a `workflow_dispatch` with `dry_run: false` rebuilds the sheets from the reverted `stats.json`. Until then the `chart` branch holds the wrong sheets: `publish_chart.py` force-pushes one orphan commit (its docstring, lines 2–14: "no history ... exactly one commit after every run"), so there is no earlier sheet to roll back to, only a rebuild |

## 7. The rules, and how each is implemented

Status: **gate** (`check.py` fails; **gate (warn)** when it only warns), **test** (`unittest`), **review** (a reviewer
judges it each round), **process** (how the session works), **open** (not held by anything yet). The last column is
where it lives.

### 7.1 Don't name the theme

| Rule | Status | Where |
|---|---|---|
| No theme word on the image or in its alt text: chart, sea, ship, harbour/harbor, survey, unsurveyed, buoy, light, berth, approach, pilot, mariner, nautical, sail, anchorage, ahoy, arr | gate, test | ROUTE-WORDS; `test_no_theme_words` (T-WORDS) |
| No theme word in DESIGN.md | gate | DESIGN-FRESH + `design.theme_words` |
| No theme word in the README's visible prose | **review only** | §8.3 q.1 carries the grep; §10.1 proposes the gate |
| No theme word in a `chart.toml` string that any live sheet reads; retired sheet modules and their strings are deleted, not kept | **open** | `[copy] unit_chart` (read by nothing), `unit_hero`, `unit_approaches`, `limit_label`, `footer_line` ("The chart ends here. The web doesn't.") survive at `chart.toml:35–39`, read only by the retired `soundings`, `approaches` and `footer` modules (`build_assets.SHEETS = ["hero"]`); §10.8 |
| Banned phrases anywhere (SVGs, report, README, chart.toml): ILLUSTRATIVE, PENDING, SEEDED, NOT FOR NAVIGATION, Here be dragons, Fair winds, example.com, Oct 2024, "thanks for reading", "that's a mood", "Hi I'm Ben", "Hi, I'm Ben", "drawn not templated", "drawn, not templated", REFRESHED DAILY, "works at night", lorem, TODO, FIXME, `<!-- POSITION` (the 20 entries of `strings.py BANNED`) | gate | STRINGS-BANNED |
| No themed headings; headings are "Also", "Working rules" | test | `test_committed_readme_is_the_one_chart_page`, round tests pin the headings |
| Every design departure from the type and layout rules names a project fact or a measured constraint, never the theme | test | T-BREAKS over `route.py BREAKS` |
| No pirate language | gate (image) | THEME_WORDS `ahoy`, `arr` |
| At most a dry wink or two, about the work, not the sea | review | two today, named in §8.3 q.4: "Boring under load." (working rule 1), "why engines are hard" (game_engine's line) |
| No ships, boats, buoys, roses, lights, hatching, legends | **review**; T-PURPOSE holds containment only | `test_every_element_has_a_purpose` (`tests/test_route.py:812–829`) checks that every group id is a PURPOSE key and that no `path`, `circle`, `rect` or `use` sits outside a group; it never looks at what is inside a group, so a hull drawn inside `hero-R5` would pass. The only shapes today are bars, rings, lines, a dotted box, by the reviewer's eye (§10.11) |

### 7.2 Everything has a purpose; nothing has a size

| Rule | Status | Where |
|---|---|---|
| Every drawn element has a PURPOSE row; no row without an element | gate (drawn → row); test (row → drawn, with S2 and W1 excused by a hand list) | ROUTE-PURPOSE is one-way (`scripts/checks/route.py:43`: a drawn element without a row); `test_every_element_has_a_purpose` subtracts `{"S2", "W1"}` by hand (`tests/test_route.py:819–822`), so a third undrawn row needs a test edit (§10.11) |
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
| Every claim about the code rests on anchors at HEAD and in the released sdist; drawn only when both hold | gate | ROUTE-UNVERIFIED, ROUTE-HEADER, ROUTE-LABEL, ROUTE-WAITING (warn) |
| The install and crawl commands are run, not quoted; the entrance is drawn only within 14 days of a passing run of the same version | gate, CI | ROUTE-ENTRANCE; the `runcheck` job |
| A subcommand named next to "rustmapper" must not be one the run check saw fail | gate | README-SUBCOMMAND |
| A working rule's cite month is computed from his first commit adding the anchor; the anchor is his, not an agent's; the code is live at HEAD | gate | NOTICE-DATE, NOTICE-AUTHOR, NOTICE-LIVE, NOTICE-ANCHORS |
| A skipped probe is never a pass; the code-only wording prints | gate (warn), test | ROUTE-PROBE-SKIPPED; `test_skipped_is_not_a_pass` |
| Sweep days (bulk edits touching most repositories: 9–10 Nov 2025, 1 and 7 Oct 2026) are excluded from any activity figure | code, test | `sweep_dates`; `test_sweep_days_are_named_not_removed`; no activity figure is printed now |
| Test counts are functions (`#[test]`, `def test_`), never files; languages from lines in the clone, never the REST field; generated trees excluded | code, test | `test_test_function_patterns`, `test_main_language_per_repo_from_lines`, `[lines.exclude]` |
| Agent-authored commits are counted apart and never as his | code, test | `agent_authored`, `coauthored_total`; `test_agent_authored_and_agent_share` |
| No commit totals, no "last commit" (sweep-adjusted, contradicted the CI date) | test (the provenance line); **open** (the facts lines) | the provenance-line test bans them; the facts lines print the agent-authorship counts and "his own 101" / "his own 420" (G8; decision §9.2; switch §10.5) |
| CI status is the API's conclusion for the last run on main, with its date and the jobs it gates on | code, gate (warn) | `repos[].ci`; CI-GATES warns when the gate list is empty |
| `scrape_interval` is read from the job, not the global | test | `test_scrape_interval_is_the_jobs_not_the_global` (no longer printed) |
| No placeholder survives: ⟨ ⟩, `<!-- POSITION`, TODO | gate | POSITION-PLACEHOLDER, README-PLACEHOLDER, README-TODO, STRINGS-BANNED |
| Two builds from the same stats are byte-identical | test | `test_two_builds_byte_identical` |
| Figures retire by themselves when the tool changes | code, test; **true of five rows of §5.4, not of three** | `instead` wordings, `waits`, `fails`/`runs`; `test_retires_when_fixed`, `test_a_crawl_that_ends_retires_h1`. True of H1, H0, L6, L4's https clause and X1's disallowed clause; false of L1/L4 under a Crawl-delay parser (no probe), L7 (no fallback) and W1 (hand switch): §5.4 "Needs here" |

### 7.4 Phone first, then desk

| Rule | Status | Where |
|---|---|---|
| A phone edition drawn at its own width (600 units), served to viewports ≤ 851 px and as the `<img>` fallback | test, gate (render) | `test_picture_order`; HERO-FALLBACK |
| No phone text under 13 px on a 390 px phone (image 308 px) or 11 px on a 360 (278 px) | gate | ROUTE-PHONE-PX |
| The sheet is one screen: ≤ 900 px tall **from a 768 px viewport up**; below 768 the height is not bounded (the phone sheet is 1.87 × the column) | gate (render) | HERO-COLUMN-PX, `TALL_FROM = 768`, `TALL_PX = 900` (`column.py:47–48`) |
| Desk words ≥ 14.5 px from a 1,200 px window; a mid edition for 852–1,199, whose only floor is 11 px | gate (render) | DESK-PX from `breakpoint_px + 1` (`column.py:50`, `chart.toml:9`); the mid window is held by `MIN_PX = 11.0` (`column.py:45`): 11.2 px at 852; `test_the_old_breakpoint_fails_on_tablets` |
| Code block lines ≤ 32 columns (what a 360 px phone shows) | gate | README-CODE-WIDTH (`CODE_COLUMNS = 32`); `test_no_fenced_line_over_32` |
| A flag a reader types (`--workers 1`) never wraps mid-flag on a phone | gate (render) | FLAG-WRAP |
| Cautions: one list, ≤ 7 items, ≤ 25 words each; the file faults folded | gate | README-CAUTIONS, README-DETAILS |
| Type floors: desk and mid 19 (serif 25), phone 26 (serif 30); sizes on the scale | gate | TYPE |
| Nothing overlaps; every box inside the sheet less a 6-unit frame; words clear the dotted line by ≥ 8 units | gate | BOUNDS-* (fast), BOX-PAD (render) |
| Rows start at one left edge; the project name sits ≥ 2 role pitches under the role line | gate | ROUTE-LEFT-EDGE, ROUTE-HEAD-GAP |
| Contrast: text ≥ 4.5:1, lines ≥ 3:1, both themes; red/green kept apart for CVD | gate | CONTRAST-* |
| Night redrawn, not inverted | code | `tokens.THEMES`, `W_NIGHT` |
| The six editions are on the `chart` branch before `README.md` names them (8 Oct 11:13: "Merged but all images are unavailable") | test, process | `publish_chart.unshipped` (`scripts/publish_chart.py:81`); `test_publish_before_commit` (`tests/test_round15.py:193`); `test_publish_needs_every_named_edition` (`tests/test_round12.py:124`); `profile.yml` publishes before the commit; §8.1 item 5 |
| Verified on a real iPhone, in Safari and the GitHub app, light and dark | **open** | §8.4, the one home of this check |
| Even density across the image | review | no metric; held by construction (one pitch, one left edge, fixed marks); §8.3 q.3 |

### 7.5 Copy

| Rule | Status | Where |
|---|---|---|
| Third person throughout; no I, my, me | test | `test_no_first_person_on_the_page` |
| Never "this repository" on a profile | gate | THIS-REPO |
| "His Scrapy repository", not the framework; American spelling | review | `[copy] repo_words`; r07; the spelling grep is in §8.3 q.4 |
| Existing wording stays unless cut; every change carries its review round in a `chart.toml` comment | process | the comments in `chart.toml` |
| The role line is re-read by 2027-06 | gate (warn) | EXPIRY-PASSED (`expiry.py:37–42`: all three EXPIRY codes warn, never fail) |
| Alt text ≤ 25 words, not starting "The", says what the image shows in plain words | gate, test | ALT-LONG, ALT-THE; T-ALT |
| Code in the code face; code spaces at the word space; no file names left of the track | gate | TYPE-CODE, ROUTE-CODE-SPACE, ROUTE-LABEL |
| The release label sits right after its command, never at the right edge | gate | ROUTE-RELEASE |
| No "generated by" line a visitor can read; no schedule in the provenance | test | the provenance-line test bans "generated", "regenerated", "weekly" (§10.6 on the two maintainer comments) |
| The thesis line is gone | config; **held by an absence only** | `[copy]` and `[copy.review]` carry no `thesis`; "wrong about itself" is in neither `BANNED` nor the test's `gone` list, and `docs/BEN-TODO.md:39` still carries it (§10.10) |
| Garden paths and reduced relatives read once | review | §8.3 q.4 |

### 7.6 Process

| Rule | Status | Where |
|---|---|---|
| Never push to `main`; the owner merges PRs | process | every change is on a branch; the weekly bot commit to `main` is the workflow's own, by his design |
| Every open PR is mergeable; a branch is opened as a PR before a round ends (8 Oct 09:04: "all PRs need to be ready to merge") | process, **not met today** | PR #17 is open (`gh api`: `state: open`, `mergeable: true`, head `v11.1/no-thesis`); this branch has no PR |
| Commit messages end with the Co-Authored-By and Claude-Session trailers | process | `git log` shows them; the model name in the trailer follows the serving model |
| No "Generated by Claude Code" footer in PR bodies or comments; the server appends its own | process | his instruction of 8 Oct |
| The stop hook: commit and push before stopping | process (session; not verifiable from the repository) | WIP commits when it fires |
| His email is used only to identify him; the page's `mailto:` is the one he set | process | it is not on the page beyond that link |
| At least 10 reviews, each against his words; research every round; multiple agents | process, done | 16 rounds × 3 reviewers; Workflow `wf_eee12105-794` (session; not in the repository); `LOG.md` |
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
6. `[position] text` is set and at least one of `[contact] linkedin` / `resume` is set, so POSITION-EMPTY does not
   fire. Owner: Ben. The page does not merge with the one line a visitor came for left blank (7 Oct: "tells a lot
   about me"; moved here from §8.2 in PRD round 1 on the owner lens).

### 8.2 Warnings allowed today, each with an owner

| Warning | Why it stands | Who clears it |
|---|---|---|
| LICENSE-FLAGSHIP | Rust-sitemap has no LICENSE | Ben, in Rust-sitemap |
| ROUTE-WAITING S2 | 0.1.3 has no Crawl-delay parser; HEAD lacks the P1 test | Ben, 0.1.4 |
| log.shards | `claims.shards` is `num_cpus`, the machine has 8 | harmless; goes with the retired `log` module (§10.8) |

POSITION-EMPTY was the fourth warning on the round-16 build; it is §8.1 item 6 now and blocks the merge.

### 8.3 Judged (each review round, in this order)

Questions 1–4 are his (9 Oct 20:50: *"is it matching what I'm saying? Is it doing what I'm saying? Is it
accomplishing my goal?"*). Each has lines a reviewer ticks; a line that fails is a must-fix.

1. **Does the image meet his goal?** Every `<g id="hero-*">` has a PURPOSE row and the reviewer can state each mark's
   purpose without the table; nothing has a size (T-NOSIZE); no theme word on the image or alt (T-WORDS) and none in
   the README's visible prose (a whole-word grep of THEME_WORDS over the prose outside comments and the `<picture>`;
   round 1 found only "Helm chart", a project fact); the three second-reading marks are there (G1a: the loop bracket,
   the gap under the box, the line past the end bar).
2. **Is every figure true?** Re-measured from `stats.json`, the audit, the sdist and the clones; every typed number
   has a `[[figures]]` row; nothing estimated.
3. **Does the page read on a phone?** At 390 px the image is one screen (575 px) and every word ≥ 13 px (13.3 today);
   nothing cut off; no code line over 32 columns; no two adjacent rows differ in pitch (the density rule, by
   construction).
4. **Does it tell a stranger about him and which project to open?** The first two phone screens show his name, what
   he builds, rustmapper and Scrapy by name and the link line; third person throughout; winks ≤ 2 and they are the
   two named in §7.1; American spelling (grep for colour, behaviour, organise, licence, grey, centre, favour,
   catalogue: none); no sentence a reviewer had to read twice (name it if there is one).
5. **Would the reviewer ship it as is?** Advisory. This is the reviewer's taste; it has no pass condition and it is
   not his bar. Only Ben's own "ship it" closes the product.
6. **Would the reviewer screenshot the image and send it to someone, and what would they say it was?** Advisory;
   the answer is logged. "A flowchart" is the risk in §11 and this is where it is asked, every round (7 Oct 15:30:
   "stunning"; round 4's question to him was which one he would screenshot).

**Done** = §8.1 all hold on the merge commit **and** §8.4 is logged **and** §9.1 is decided by Ben **and** three
reviewers answer yes to questions 1–4 with no must-fix left open. Round 16: no (8/7/8). The must-fixes left were
copy (r16-3) and the meaning of a blank row and of `sitemap.xml` (r16-2), both fixed since; what blocks a yes is
§9.1, not question 5.

### 8.4 On a device (once, before merge)

Open the profile on an iPhone in Safari and in the GitHub app, light and dark. Pass conditions, logged in `LOG.md`:

- Safari at 390 px serves `hero-phone-day` in light mode and `hero-phone-night` in dark (the `<source>` order in
  `README.md` lines 7–12).
- The GitHub app shows `hero-phone-day` in both modes via the `<img>` fallback (`README.md` line 13, HERO-FALLBACK);
  one community report says the apps send the light theme regardless (PRD review r01-2, source 16; unverified).
  Any night edition there is also a pass; a missing image is a fail.
- The image is one screen (≤ 900 CSS px; 575 at 390).
- The first two screens show his name, what he builds, rustmapper and Scrapy by name and the link line.
- Anything else is a fail to log with a screenshot.

### 8.5 After merge

- A failed weekly run is Ben's to notice (the run page; the job's `::error::` lines) and a session's to fix.
- The GitHub constants in the checks (the 82 px mobile inset, the 846 px column, `<picture>` support; measured on
  the live page 10 Oct 2026) are re-measured by whoever opens the next round, and on any GitHub changelog that names
  Markdown images.
- The role line expires 2027-06 (EXPIRY-PASSED warns).
- No success metric is set; "done" is §8.3. One cheap one is available if he wants it: Rust-sitemap's Insights →
  Traffic referrers include the profile within 30 days of merge, read once by Ben.
- `chart.toml` copy is edited after merge by Ben, or by a session only inside a review round (§7.5).

## 9. Open decisions and items

### 9.1 The one decision: what the top of the profile says about rustmapper 0.1.3

Today the image's box and the page's "Before you run 0.1.3" list state six measured faults of the released tool
(L1, L7, L4, L6, L2, L5 on the open list; H0 and H1 in the box). Every one is true, probed and gated. Together they
read as a warning label on his flagship. His test is 9 Oct 20:50, *"is it accomplishing my goal? Not just what I'm
saying"*, so each option below says what the first phone screen reads, not only which probes pass.

| Option | What the first screen says | What the page's list becomes | Cost, and who | What the pipeline does |
|---|---|---|---|---|
| **1a. Minimum 0.1.4** (recommended as the floor) | name; role; rustmapper, one sentence; `pip install rustmapper` 0.1.4; `rustmapper crawl` starts from your URL; fetches up to 20 pages; press Ctrl-C once; `data/sitemap.jsonl`; sorted 21 ways. **No box.** | five items (L1, L7, L4 without its https clause, L2, L5) | §5.4 rows 1, 2 and 6: exit when idle (the test is at HEAD), robots 404/scheme/fail-closed (not at HEAD), `[project.scripts]` (not at HEAD); a release. Ben, or a session with push access to `Rust-sitemap`. Nothing needed here. | H1, the gap, H0, L6 and L4's clause retire at the next weekly run; `release-published` rebuilds at once |
| **1b. Full 0.1.4** (recommended) | as 1a, plus S2 "one queue per host, paced by that host's robots.txt" in the loop and W1 if its switch is lifted | three items (L1 reworded, L2, L5), each a default rather than a fault; the fold keeps the file notes | 1a plus §5.4 rows 3, 4, 5, 7, 8; two of the eight are at HEAD already (exit test, Crawl-delay parser). **Plus, here first:** the `crawl_delay_obeyed` probe, the L7 and `noindex` fallbacks, W1's switch (§10.9); without them the first build after the release fails on L1/L4/L7 | every caution retires on its own only once §10.9 is done |
| 2. Keep the route, move the cautions to rustmapper's README | as today, with the box | one line linking the project's own "Known issues" | the image still draws H0/H1, because they are true of the release the image names; a "Known issues" section in Rust-sitemap; a gate here that the linked section exists | `[route.rustmapper]` items marked off-page |
| 2b. Keep the image and its box; cut the open list to the two first-minute faults | as today, with the box | two items (L1: no pause, 256 workers; L7: no contact in the UA), the other four folded under the existing `<details>`; two is under the "few" the hiring-side sources set (r01-1 §5) | no work in Rust-sitemap; here, README-CAUTIONS' open-list limit and the fold's | retires the same way as 3 |
| 3. Ship as is | as today, with the box, then six items | six items | a visitor's first read of his main tool is its fault list | nothing |

- **Default while undecided:** the branch stays unmerged; `main` and the live page do not change.
- **Decide by:** before the merge. A push to `main` that touches scripts or `chart.toml` triggers a build, so the
  merge is the first weekly run.
- **Size:** 1a is three fixes in Rust-sitemap, one with its test already at HEAD; 1b is eight fixes plus the four
  items here. In days this is Ben's estimate to make; the repository cannot measure it, and this document prints no
  figure it did not measure.
- **A render of the 1a and 1b outcomes** is owed to him before he decides (§9.3): the round-1 `once-p1-lands/` sheet
  is the precedent. The 1b render needs §10.9 first, because the fixture that passes every §5.4 probe fails the
  build today (§5.4, "Needs here").

### 9.2 Owner's calls carried in `docs/BEN-TODO.md`

- `[position] text` and `[contact] linkedin` / `resume` (empty since round 4): now §8.1 item 6, blocking the merge.
- **The agent-authorship counts on the facts lines** ("coding agents (Claude) authored 45 of its 146 commits and
  co-signed 1 of his own 101"; Scrapy's "71 of its 499 … 30 of his own 420"). The rule is his sentence (9 Oct 11:35:
  "We don't need to show the commits… it feels lazy"); the two memos that argued hiding them costs more are the
  agents' judgement, not his. Options: **strike** (his words; the default from PRD round 1), **keep** (an honest
  fact a hiring engineer asks, Q3), **share without totals** ("about a third of its commits were written by coding
  agents", no numbers, in the provenance line which already says who is counted). Implementation either way is the
  `[facts] agent_clause` switch (§10.5), default off, so his answer is one line. Until the switch exists the page
  prints the counts, and G8 is marked open.
- `rustmapper` or `Rust-sitemap` as the printed name (the alias is in `chart.toml`).
- The rustmapper README's worker figure (code 256–1,024, README 32–512, PyPI 256).
- Scrapy: make the near-duplicate filter persist across passes; stage 2's robots check, delay and user agent.

### 9.3 Not yet verified or produced

- The iPhone and GitHub-app check (§8.4).
- The `workflow_dispatch` dry run on the branch (the macOS run check installs the prebuilt wheel, so the install
  note will read differently from the Linux run that produced today's `stats.json`; the https probes depend on
  `sudo -n security add-trusted-cert` on macos-14 and may be skipped, which the gate reports as a warning).
- A real iPad at 852–1,199 px, and his call on the mid window: between 852 and 930 px the route's words are under
  the 13 px floor he gets on a phone (11.2 px at 852). Either lift the mid floor to 13 (a narrower mid sheet, or a
  second breakpoint at 931) or accept the window in writing (§11). 9 Oct 11:32: "accepting of all different
  formats".
- The renders of the §9.1 outcomes: build from a fixture `stats.json` with `ends_by_itself`, `robots_read`,
  `robots_late` passing and `robots_stall`, `ua_seen`, `sitemap_keeps_disallowed`, `kill_writes_file` failing, with
  `edition.scripts` set; put the paths beside round-16's. The 1a fixture builds today; the 1b fixture needs §10.9.

## 10. Gaps this review found

Rules that are held only by a reviewer's eye, or by nothing, with the proposed fix. Items 1–7 are from the PRD's
first draft; 8–16 were added by PRD review round 1 (reviewer and must-fix in brackets). None of 1–8 blocks the
merge; 9 blocks option 1b.

1. **Theme words in README prose** (G2). `theme_words` runs over the image, the alt and DESIGN.md, not over
   `README.md`'s visible prose. Add it to `checks/readme.py` with an allow-list for project facts ("Helm chart",
   "CT logs", "logged"). One function, one test. Until then §8.3 q.1 carries the grep.
2. **"Not too on the nose" has no count** (G10). The reviewers count winks by hand (two today). Record the allowed
   two phrases in `chart.toml [copy] winks` and fail a third unlisted one? Over-engineering; keep it in review. The
   two are named in §7.1 and §8.3 q.4 so no round forgets to count.
3. **Even density** (G3). No metric. The one-pitch, one-edge, fixed-mark rules hold it by construction; a density
   check would be chasing a number. Keep it judged (§8.3 q.3).
4. **The device check** (G4): §8.4, with its pass conditions. It must be done once, by him or on a device the
   session can reach, before the merge.
5. **Commit counts on the facts lines** (G8). Decided in §9.2: off by default, by his sentence. The gap is the
   implementation: `render_readme.agent_clause` is called unconditionally (`render_readme.py:459`) and `chart.toml
   [facts]` has no switch. Add `[facts] agent_clause = false`, read it in the renderer, and a test for both states;
   then mark G8 "gate + switch".
6. **"Generated" survives in two maintainer comments**: the README's first line ("regenerated weekly from
   assets/stats.json") and DESIGN.md's first line ("Generated by `python3 scripts/tokens.py --md`"). Both are HTML
   comments a visitor never sees, and the test guards only the provenance line. Fine as is; noted so the rule's
   scope is explicit: *no generated-by line a visitor can read*.
7. **The worktree's `assets/v9` is stale** (gitignored; it still holds v9 footer stills). `check.py` run without
   `--out-dir` on a stale tree fails on them. Not a product defect; `build_assets.py` first, or point the gate at the
   build. Worth a one-line note in `check.py`'s docstring.
8. **Theme strings and retired modules in the repository** (G2, G11; r01-1 MF7). `chart.toml [copy]` still carries
   `unit_chart = "SOUNDINGS IN COMMIT-DAYS"` (read by nothing), `unit_hero`, `unit_approaches`, `limit_label = "LIMIT
   OF SURVEY 2026"` and `footer_line = "The chart ends here. The web doesn't."`, read only by `scripts/sheets/
   soundings.py`, `approaches.py` and `footer.py`, which `build_assets.py` lists in `ALL_SHEETS` but not in
   `SHEETS = ["hero"]`. The profile repository is public and `chart.toml` is the file he is told to edit; the
   footer line is the thesis voice he cut on 9 Oct 19:39. Fix: delete the five keys and the retired `soundings`,
   `approaches`, `footer`, `log` and `instruments` modules with their tests (69 tests) and the `log.shards` warning;
   extend `theme_words` to `[copy]` values (the §7.1 open row).
9. **Three of §5.4's rows fail the build instead of retiring** (G7; r01-3 MF1), verified by running the resolver:
   write probe `crawl_delay_obeyed` in `runcheck.py` (a fixture robots.txt with `Crawl-delay: 2`, two requests to
   one host at least 2 s apart); add to L7 an `instead` with `fails = ["ua_seen"]`, `text = ""`; add to X1 a wording
   for a release that drops `noindex` pages; replace W1's `drawn = false` with a wording that holds on a passing
   `kill_writes_file` and lift the switch, or leave W1 undrawn and say so in §5.1 for good. Then §5.4's claim is a
   fixture the resolver is run against (item 12).
10. **The thesis line is banned nowhere** (G14; r01-3 MF4). Add "wrong about itself" to `strings.py BANNED` (it scans
    `README.md`, `chart.toml`, the SVGs and the report), and strike `docs/BEN-TODO.md:39` (round-4 item 1 still
    tells him to set his GitHub bio to "The web is wrong about itself; I survey the part that isn't linked"). His
    words, 9 Oct 19:39.
11. **T-PURPOSE and ROUTE-PURPOSE are narrower than their rows** (G9, G16; r01-3 MF5, MF6). Add to
    `test_every_element_has_a_purpose` an assertion on what is inside each non-text group (only `rect`, `circle`,
    `line` and `path` with straight-segment `d`; no `use`, `symbol`, `polygon`, `image`), so "no ships" has a test;
    and derive the excused set from `data.route` (`drawn = false`, `waits`) instead of the hand list `{S2, W1}`.
12. **The PRD has no test** (r01-3 MF8). This repository already fails the build when `README.md`, `DESIGN.md` or
    `AUDIT.md` drift (README-STALE, DESIGN-FRESH, AUDIT-STALE); the PRD is the one generated-by-hand document. Add
    `tests/test_prd.py`: every `[A-Z]+(-[A-Z]+)+` token in §7 and appendix B is emitted by `scripts/checks/*.py` and
    every emitted code is in appendix B; each appendix-B tier equals the plug-in's `TIER`; §6's counts match
    (`ls scripts/checks`, the `unittest` total from the runner, `len(steps)` and the gate/probe split in
    `stats.json`); §8.2's codes equal the gate's warn set on a fresh build; §5.1's IDs and Q's equal `PURPOSE`; each
    §5.4 row is a resolver fixture.
13. **A failed data fetch leaves no mark** (r01-2 MF3). §6 and §6.1 now say what happens (last week's figures, old
    dates, no mark). Decide whether a mark should exist on the route sheet or the page; if yes, define it, have
    `route.py` read `no_sounding`, and test that path with `["hero"]`, not `["log"]`.
14. **The mid window's floor** (G4; r01-3 MF2): §9.3. A product change (narrower mid, or a breakpoint at 931) or an
    accepted trade written in §11.
15. **Languages order** (r01-2 MF9): `tests/test_round7.py:91` pins the set and "Python, Rust; " first; nothing pins
    "then by repository count, then by lines". Add one assertion over a fixture with two counts.
16. **The code block's comment lines on the desk** (r01-1 MF6). README-CODE-WIDTH caps every line at 32 columns for
    the 360 px phone; the three comment lines are the ones that wrap for it, and the desk reader (the likelier one)
    sees them wrapped in an 846 px column. If a wording of the stop rule fits one ≤ 32-column comment, take it ("#
    runs until stopped; Ctrl-C once" is 33). Otherwise the trade stands (§11).

## 11. Risks

- **Reading as a flowchart.** With the manner carried only by the track, the dots and the paper, a visitor may see a
  flowchart. The answer is drawing, never added symbols (DECISIONS, concept A risk 1). From PRD round 1 every review
  is asked §8.3 q.6, so the reading is sought, not merely not raised (rounds 13 and 16 did not raise it unasked).
- **The desk pays for the phone's code width.** In his words the web is the likelier reader (9 Oct 11:32); Markdown
  serves one code block to both, so the desk column (846 px, `page-desk-1.png`) shows the three stop-rule comment
  lines wrapped at the phone's 32 columns with two thirds of the column empty. Accepted for now; §10.16 names the
  one-line fix if a wording exists.
- **The mid window, 852–930 px.** The route's words are 11.2–13.0 px there, under the 13 px a phone gets (§5.2,
  §9.3). No device he named sits in that window (a 1,024 px iPad sideways gets 13.7 px); the trade is written here
  until he rules on it.
- **The weekly run check on macOS differs from the Linux run** that produced today's stats; wordings may shift on
  the first CI build (the install note, probe skips). The gate reports it; nothing false can print.
- **A 0.1.4 cut from HEAD as it stands removes the command line** (`bindings = "pyo3"`, no `[project.scripts]`,
  `pyproject.toml:55` at `32c2651`): `edition.scripts` would be empty and the build would refuse to draw the
  entrance. Fix the packaging before cutting the release (§9.1, 1a).
- **A 0.1.4 that fixes the User-Agent or parses Crawl-delay fails the build here** until §10.9 is done (§5.4,
  "Needs here"). The failure is loud (ROUTE-UNVERIFIED, exit 1, nothing published), not false.
- **GitHub's rendering changes** (the 82 px mobile inset, the 846 px column, the `<picture>` support) were measured
  on the live page on 10 Oct 2026 and are constants in the checks; re-measure when the page looks wrong (§8.5).

---

## Appendix A. The owner's words that bind this product (excerpts; verbatim where quoted, in order)

The full 21 messages are in `docs/crit/prd/owner-messages.md`. Quoted here are the 15 that set a rule; the other
six are "Do another pass and review every single detail…" (7 Oct 16:12, cited in G17), "Start now", "Don't stop",
"Resolve all merge conflicts and all PRs need to be ready to merge" (8 Oct 09:04, §7.6), "Merged but all images are
unavailable" (8 Oct 11:13, §7.4) and "Continue".

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
- 11 Oct (later) — "Review and ensure this is something I want to see rounds of reviews and research"

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
| data | fast | `data.load`, `data.seeded`, `data.provenance`, `data.schema`, `data.invariant`, `data.calendar`, `data.stale`, `data.unsurveyed`, `data.edition`, `data.notices`, `data.claims`, `data.clones`, `data.repo_count` (stats.json invariants); `data.tide`, `data.variation` idle: rules of sheets that are off the page |
| design | fast | DESIGN-FRESH |
| expiry | fast | EXPIRY-PASSED, EXPIRY-KEY, EXPIRY-FORMAT (all warn) |
| figures | fast | FIGURES |
| flash, motion (fast), frames (render), perf (perf) | — | idle: nothing moves (FRAMES-*, MOTION-*, FLASH-*, PERF-*) |
| legend | fast | idle: no symbols (LEGEND-*) |
| log | fast | `log.load`, `log.json`, `log.schema`, `log.version`, `log.rule`, `log.computed`, `log.shards`: idle, the log sheet is off the page (§10.8) |
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
