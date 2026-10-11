# PRD: Ben Russell's profile page

**Status:** draft. **Approved when** Ben answers §9.0 (c); from then on the text changes only when the product
changes. **Next, in order (the stop rule, §0):** the fix round opens the PR (§10.17) and does §10.19 and §10.23; one
product review round on the PR's build (§8.3, Done); his yes. No PRD round runs before the merge.
**Owner of the decisions:** Ben. **Owner of the text:** the session; edited only in a PRD review round or when the
product changes. **Baseline:** the product code at `027f081` on `v12/purpose`, on `origin` at `9e3db34` with no PR;
`origin/main` (`d253286`) was 23 commits behind it on 11 Oct 2026 (`git rev-list --count origin/main..027f081`). The
figures and the 90 `file:line` cites were last re-read at `b6cca2c` (PRD round 6, reviewer 3), and no product file
has changed since `027f081` (`git diff --stat 027f081..HEAD -- . ':!docs'` is empty). **Last updated:** 11 Oct 2026,
PRD review round 6.

Sources: the owner's 21 messages in this session (the full text is `docs/crit/prd/owner-messages.md`; appendix A
excerpts the 15 that set a rule), `docs/crit/round6/SPEC.md` and `DECISIONS.md`, `docs/crit/round5/DECISIONS.md`,
`docs/crit/round6/LOG.md` (16 review rounds), the 48 reviews under `docs/crit/round6/`, `docs/data/AUDIT.md`,
`chart.toml`, the 28 gate plug-ins under `scripts/checks/`, the 539 tests under `tests/`, `scripts/runcheck.py`,
`.github/workflows/profile.yml`, the renders under `docs/crit/prd/renders/` (`round-16`, `once-1a`, `once-2b`,
`once-2b-r3`; §9.1), a clone of `Rust-sitemap` at `32c2651` (the session's
`scratchpad/clones/Rust-sitemap`; `build_stats.py` makes the clones, so any clone at that commit serves), and the PRD
reviews under `docs/crit/prd/` (three a round; `LOG.md` there records what each round changed).

---

## 0. Status

- **What this is.** The final product, every rule the owner set for it, and how each rule is implemented: by a gate in
  `check.py`, by a unit test, by a reviewer's judgement, or not at all. To build and accept the page, read §1, §2, §4,
  §5, §8, §9 and §11 (505 lines, 9,520 words, of the document's 921 lines and 20,568 words, by `wc -l`
  and `wc -w` over the lines of those sections, split at `## ` headings; the rest is the register and the
  appendices). The register is §3's last column, §7, §10 and appendix B; how the work was done, by his instruction,
  is appendix D. Line numbers in this document are as of `027f081`; where a symbol exists it is named beside the
  line. The register is hand-checked each round until §10.12 exists (the commands are in `docs/crit/prd/LOG.md`,
  rounds 4 to 6).
- **Built and reviewed.** The image and page exist on `v12/purpose`: 539 tests pass; `check.py --tier fast,render`
  on the round-16 build gives 0 fail and the four warnings of §8.2 (on the tree as committed, with no build first, it
  fails on the stale `assets/build-report.json`, §10.7). Scores: `docs/crit/round6/LOG.md` (16 product rounds),
  `docs/crit/prd/LOG.md` (six PRD rounds). What waits on Ben is §9.0; what waits on a session is §8.1 and §10.
- **Stop rule.** The next session is the fix round: it opens the PR first (§10.17; the branch is on `origin`, so no
  push is needed), then does §10.19 and §10.23 (two product changes); one product review round judges the PR's
  build (§8.3, Done); then Ben's yes. No PRD round runs before the merge; the first after it reads the document
  once against the live page. Round 5's rule said the same with §8.1 items 7 and 8 in front, and round 6 ran
  against it (appendix D's last table records it): six PRD rounds have changed no product file (`git diff --stat
  027f081..HEAD -- . ':!docs'` is empty) while `main` serves the page he rejected on 9 Oct (§9.1, row 0). Items 7
  and 8 are no longer in front, on the owner lens: the switch's default reproduces today's page, and nothing a
  visitor sees reads the five `[copy]` keys (§8.5, §10.8). His 9 Oct 20:50 floor ("at least 10 reviews") is met by
  the 16 product rounds; his 11 Oct sentence's object is "something I want", the page, and the page is not live.

---

## 1. What the product is

A GitHub profile README, `BenjaminSRussell/BenjaminSRussell`, regenerated weekly from his repositories. One image at
the top, then text. The image is **the way into rustmapper**: how you install it, what it does with each page in
order, where it goes wrong, how you stop it, what file you get, and which other project of his reads that file. The
page under it is the lookup material: who he is, which project to open, the facts of each, how to run them, and the
rest of his work. Words: **the image** is what the page shows at the top, in any of its six **editions** (one SVG
each, named `hero-*` in the code and the gates); a **sheet** is one edition's drawn area, measured in units; **the
route** is the drawn order of a run, and **the track** its magenta line (R5). The page itself calls the image "the
drawing" (`README.md:151`).

The product has a manner, not a theme. A navigator would recognise a route strip, a magenta routeing line (this
document calls it the track, R5), a dotted danger line and a cream sheet. Nobody is told. No word on the page names
the sea. The forms are the chart's own: INT 1 prints routeing measures "usually magenta" while a recommended track
itself is a black dashed line with arrowheads, and a dotted or pecked line encloses a danger (sources in
`docs/crit/prd/LOG.md`, round 2). The double reading is intended, not only a risk (§11): a reader who knows the forms sees where the colours
come from; one who does not sees a clean route (G13a; asked every round at §8.3 q.6).

**One sentence the image must answer** (SPEC §0): *how you start rustmapper, what happens to a URL inside it in order,
where a stranger goes wrong, and where the output goes next.* Every mark on the image either belongs to that sentence
or is cut.

## 2. Who reads it and what they ask

Research R4 (57 sources on who reads GitHub profiles) gives the readers and the order of their questions. Every
element on the image and every block on the page is tagged by its author with the question it answers. T-PURPOSE and
ROUTE-PURPOSE hold that every drawn element has a row and a tag Q1–Q5 (`tests/test_route.py:829` asserts `^Q[1-5]$`),
not that the tag is right; the reviewer judges the tags at §8.3 q.1.

| Q | The visitor's question | Who asks it first |
|---|---|---|
| Q1 | Who is this and what does he build? | a screener. R4-F1 estimates about 7 s for the six facts; the practitioner guides say 30 s to a minute (sources in `docs/crit/prd/LOG.md`, round 2); none is measured. The first-screen rule (§8.3 q.4) rests on "first screen", not on a number |
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
it; "open" means nothing holds it yet. G17–G19, his instructions for how the work is done, keep their ids in
appendix D.

| # | His words (date) | What it means here | Held by |
|---|---|---|---|
| G1 | "world class one of a kind beautiful profile readme that is stunning and fun and tells a lot about me" (7 Oct 15:30, the second half of the sentence; the first half is G1e) | the standard of finish; a page that says what he builds and shows one of his tools working | review (every round's first question; G1 has no test: the bar is the reviewer's yes to §8.3 q.1–4 and to q.6's first line, the screenshot question) |
| G1a | "it should say more than it literally says and should have layers of depth and thoughts associated with it" (7 Oct 17:40) | a second reading finds more: the loop bracket up the left (these rows repeat for every page), the gap in the track under the box (the release never exits), the thin line past the end bar (his projects hand each other files) | test (the gap: `test_the_gap_shows_without_colour`, `tests/test_route.py:894`, the track breaks once under the loop by ≥ 14 units with every colour set to black; the hand-off line: `test_handoff_line_drawn_only_when_it_runs`, `:527`); gate, test (ROUTE-ARROW, the bracket's arrowhead; `test_loop_arrow_is_on_bare_line`, `tests/test_route.py:1002`); review for whether a reader finds them (§8.3 q.1 names the three marks) |
| G1b | "is it interesting does it draw in the user what does it say about the person who made it" (7 Oct 17:40) | the page says what kind of engineer made it without saying so: measured figures with their source commits, commands that were run, faults stated with their fix beside them; and screen one makes a stranger scroll to the second (the first half of the sentence, "is it interesting does it draw in the user") | review (§8.3 q.4; the scroll, q.6's fourth line). No gate, no test |
| G1c | "stunning and fun" (7 Oct) / "The images are not cool enough" (8 Oct 14:22) / "Wording is weird but it's cool" (8 Oct 14:22) | finish and wit. **The trade, in his words:** on 9 Oct he overrode naming the theme and running bits ("too on the nose"; "Making it all about it too fucking much... It's just cringy"). "Stunning" and "fun" still stand as goals, judged at §8.3 q.6; "not on the nose" is a constraint on how they are met, not a withdrawal of them. A later round that touches either re-reads 9 Oct 11:35 and 11:37 first | review (§8.3 q.6's first line, part of Done) |
| G1d | "this should appear like it took a team months of work and years of workshopping to create and design and manufacture" (7 Oct 17:40); "It's mediocre and not exciting or well designed and intercut this feels basic" (7 Oct 17:18) | the care shows without being announced: one pitch and one left edge (G3), the real field names and the release's own date, every figure with its source commit, the second-reading marks (G1a), and the one `DESIGN.md` link for a reader who wants to see how it was made. Decoration is not the answer to "months of work"; the sources agree (clarity is noticed before complexity; "not a wall of badges or animations"; stronger READMEs explain decisions: `docs/crit/prd/LOG.md`, round 3) | review (§8.3 q.6, third line: does it look made with care, and where did the reviewer see it). No gate, no test |
| G1e | "This readme does not show an expert or high level smart person who has a massive interest in design" (7 Oct 15:30, the first half; the first thing he said, and what the old page failed at) | two claims, proved two ways: "expert" is G1b (measured figures, commands that were run, faults with their fix). "A massive interest in design" shows in how the page is made, not in ornament: three faces with a reason each (`tokens.py ROLES`: the name and the project's name in the serif, `display` and `project`; the rows in the condensed sans, `label`; commands in the mono, `machine`, set at the word space), night redrawn with heavier strokes and the Light cuts rather than inverted (§5.2; `NIGHT_LIGHT_CUTS`, `tokens.py:117`), one pitch and one left edge (G3), the column measured on the live page and written down (`DESIGN.md:21`), and `DESIGN.md` one click from the page (`README.md:151`). A stranger would say the person who made this cares about design | review (§8.3 q.6, third line: whether someone who designs for a living would see a designer's hand, and where). No gate, no test |
| G2 | "Don't tell the user show the user you don't need to tell them it's a ships log or label everything it should be obvious" (8 Oct) | no label names the form; marks carry the manner; no themed headings (the headings are "Also", "Working rules") | ROUTE-WORDS, STRINGS-BANNED, T-WORDS, DESIGN-FRESH; headings pinned by test (§7.1); README prose: review only (gap §10.1) |
| G3 | "It's too dense in certain areas of the image... other parts... open, but you can't read anything" (9 Oct) | one left edge, fixed pitch, nothing placed by hand, nothing overlaps | BOUNDS-*, BOX-PAD, ROUTE-LEFT-EDGE, ROUTE-HEAD-GAP; T-NOSIZE |
| G3a | "But it doesn't really, it's confusing. Like, you look at it, you're like, oh, I don't know. Like, what's happening?" (9 Oct 11:32) | the whole image says what it is at a glance, before any one element is read: a stranger can say in one sentence what the picture shows (a tool, how you start it, what you get) | review (§8.3 q.1, first line: the reviewer's one sentence, written before reading §1 or §5.1, logged in `docs/crit/prd/LOG.md`). No gate, no test: T-PURPOSE holds a purpose per element, nothing holds the whole |
| G4 | "The images are all crushed" (8 Oct 14:22); "I'm looking at iPhone... it has to be kind of accepting of all different formats" (9 Oct) | a phone edition drawn at its own width; type floors on screen; the code block fits 32 columns; the web reader gets the desk edition | ROUTE-PHONE-PX, HERO-COLUMN-PX, HERO-FALLBACK, README-CODE-WIDTH, FLAG-WRAP, DESK-PX; the device check is §8.4 (open) |
| G5 | "Fuck saying ship's log. Just make it a log... If it looks like a shoe... You don't need to tell me it's a shoe" (9 Oct) | the same rule as G2, said again on 9 Oct; nothing further | as G2 |
| G6 | "the images and the text need to... differentiate themselves... It should act like it doesn't know that it is" (9 Oct) | the image keeps what a list cannot show, the text keeps what you copy or look up; no fact said twice | STRINGS-TWICE, STRINGS-COUNT, HERO-SELF-TWICE |
| G7 | "how is the data gathered? The data doesn't look exactly accurate" (9 Oct) | every figure has a key, a definition and a source commit; every claim about code has an anchor in the code | AUDIT-STALE, AUDIT-COVER, FIGURES, ROUTE-UNVERIFIED, ROUTE-HEADER, NOTICE-*, STRINGS-UNMEASURED, ROUTE-STRINGS |
| G8 | "We don't need to show the commits are kind of cool. The data is kind of cool that we're pulling, but at the same time, it feels lazy, and I don't really like that" (9 Oct 11:35); "Talking about my commits. Talking about my work. That is what this should all be about" (9 Oct 11:37) | no commit activity drawn; no commit total on the image or in the provenance line; the facts lines' agent-authorship clause, which names each repository's commit count ("authored 45 of its 146 commits"), prints by default and his word reverses it (§9.2, the one home of that decision; §9.0 (b)). He said both: 11:35 is about the v8 picture of commits ("show the commits"), 11:37 says the page should talk about his commits and his work | the image has no count (T-NOSIZE); the provenance-line test bans `commits`, `all_hands`, `calendar_total`; the facts lines: §9.2, and the switch §8.5 adds after the merge |
| G9 | "Don't show me fucking ships unless it's like artfully well done... it's too on the nose" (9 Oct) | no ship, no boat, no buoy, no rose, no symbols at all; no legend | nothing drawn but bars, rings, a track, a dotted line; held by review (T-PURPOSE checks containment, not shape: §7.1); LEGEND-* idle |
| G10 | "Don't say arg like a fucking pirate. Don't use pirate language. We're in a modern era. [...] if there's little things, little jokes you can throw in, like one word, one-off words that are referenced being a pirate or some shit, like that's funny. Making it all about it too fucking much. No one wants that. It's just cringy" (9 Oct 11:37) | two rules, not one: no pirate talk and no running bit; a one-off word as a joke is allowed ("that's funny"); more than a couple is "cringy". Plain modern copy otherwise. Winks today: two, named in §7.1 and §8.3 q.4; whether a wink uses the one-off allowance is the writer's call | THEME_WORDS has `ahoy`, `arr` (the pirate-talk half); the count is review (§8.3 q.4; §10.2) |
| G11 | "The map, very helpful. The fucking log, not really... helpful knowledge... in a cool format" (9 Oct) | the image is directions a stranger uses; the log sheet is gone | the route; `log`, `instruments`, `approaches`, `soundings`, `footer` sheets are off the page (their modules and strings are still in the repository: §10.8) |
| G12 | "the ship went off a cliff at the end? No... Unsurveyed?... not smart" (9 Oct) | no end-of-the-world device; no hatched margin; no "unsurveyed" | STRINGS-BANNED, THEME_WORDS (`unsurveyed`) |
| G13 | "It should be telling you about me" (9 Oct 11:37, the first half of the sentence) | the page is about him and his work, in the third person | T1/T2, "Ben Russell builds", facts lines; `test_no_first_person_on_the_page`; THIS-REPO; the position line and a contact are §8.1 item 6 |
| G13a | "but with a layer of a theme of shipping" (9 Oct 11:37, the second half); "It's a sailing thing, which I do fuck with. I think that's a cool concept" (9 Oct 11:32, his permission beside the prohibitions of G2, G5, G9, G10 and G12) | the manner is in the marks, never in a word (§1): a reader who knows the forms recognises a routeing line, a danger line and a sheet; one who does not sees a clean route | review: §8.3 q.6, its answers logged every round in `docs/crit/prd/LOG.md`. No gate, no test |
| G14 | "The wording is fucking weird survey the web that is wrong about itself" (9 Oct) | the thesis line is cut, everywhere | `chart.toml [copy]` has no `thesis`; EXPIRY-KEY **warns** on a stale review key (never fails); the phrase is banned nowhere and `docs/BEN-TODO.md` round-4 item 1 still tells him to put it in his bio (§10.10) |
| G15 | "It's trying to be a fucking map for no reason... tiny fucking islands... Is it based on the size of the project or how many commits?" (9 Oct) | no shape has a size that depends on data; the picture exists only where the subject has a route to travel | T-NOSIZE; DECISIONS (four concepts scored on this goal) |
| G16 | "Every single fucking map needs a deep purpose... Everything, single thing inside of this needs a purpose, not a fucking chasing a reason" (9 Oct) | a PURPOSE row per drawn element: what a stranger learns, which Q, from which data | T-PURPOSE, ROUTE-PURPOSE; T-BREAKS (every design departure names a project fact) |

## 4. Non-goals

- Not a stats card. No stars, followers, streaks, activity graphs, language pie; no commit total except inside the
  agent-authorship clause of the facts lines (G8; the provenance line's own ban is §5.3 row 12).
- Not a bio. No photo, no greeting, no narrative paragraph, no timeline; the one line of status is `[position]
  text` (8 Oct 14:52: "Don't tell the user show the user"). "Ben Russell builds…" is one sentence of what he builds.
- Not a badge wall. No shields, icon grid or visitor counter; the Languages and Stack lines are words (G1d:
  decoration is not care).
- Not a card deck. No pinned-repository or stats cards; "Also" and the "15 more repositories" fold are the only
  lists of his work. (These three are the conventions of a generated profile README and its curated examples;
  sources in `docs/crit/prd/LOG.md`, round 4.)
- Not a themed poster. No ship, rose, buoyage, soundings, tide, light characters, chart number (the title block
  carries no count, no CI and no "1 OF": `test_title_block_is_name_and_role`, `tests/test_route.py:1052`), "corrected
  through".
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
| F1 | "fetches up to 20 pages at a time from each host; queues their links to your site, its subdomains and its parent domain" | what a site feels; scope | Q1 | `state.rs max_inflight`, `url_utils.rs is_same_domain` | anchors hold in both trees; the governor is a clause of this row, never a row of its own (`test_governor_is_a_clause_of_fetch`, `tests/test_route.py:935`). The printed words are the entry's **second** wording: the first ("fetches pages, fewer at once when saves average over 500 ms…") fails on purpose on `absent = "current_permits > MIN_PERMITS"` and returns by itself on a release whose governor drops that floor; the one row where a release changes the image's words without changing a fault |
| H0 | "on https, pages behind a disallowed link wait" (dotted box) | the first catch on a real site | Q5 | `frontier.rs` blocked branch; probes `robots_stall`, `robots_resume` | probe passed (code-only wording if skipped) |
| H1 | "0.1.3 never exits by itself; quit when `Received work item` lines stop for 60 s" (same box) | when to quit, and the sign | Q5 | `bfs_crawler.rs` select arm; `{quiet}` = timeout 20 + permit wait 30 + backoff, rounded (AUDIT §7) | probe `ends_by_itself` failed and `crawl_ctrl_c`, `quiet_after_last_page`, `quiet_slow_page` passed (`runs`/`fails` in `chart.toml`); the "60 s" comes from the probe alone (`test_h1_takes_the_quiet_words_only_on_the_probe`, `tests/test_route.py:267`); while H0 is drawn H1 never says "done" (`test_pairing`, `tests/test_round16.py:85`); begins with `edition.version` (`test_h1_names_the_release`, `tests/test_route.py:726`); retires with a release that exits |
| W1 | "saved as it goes; export works after a kill" | what logging before storing buys | Q5 | `writer_thread.rs` | **not drawn**: `drawn = false`, set by hand in `chart.toml` (round 15: no room on the phone sheet). Its wording holds *because* `kill_writes_file` failed (`fails`); a passing kill flips it to "logged to disk, then saved to redb, in batches" (`tests/test_round13.py:258`), drawn or not; no timed-flush wording, "every N ms" (`test_no_period_wording`, `tests/test_round7.py:196`) |
| C1 | "press Ctrl-C once and wait for `Saved to`; a second press quits without writing the file" | the reader's one step and its cost | Q5 | `main.rs` "Saved to:"; probes `crawl_ctrl_c`, `second_ctrl_c` | probes as stated; a release that exits leaves this row wrong (§5.4 row 1) |
| R12 | end bar | where you end up | Q4 | geometry | always |
| R13 | `data/sitemap.jsonl` "fields: url, depth, status_code, title, …" | what you get, with the real field names | Q4 | `state.rs pub struct SitemapNode` | anchors hold and `crawl_ctrl_c` passed (`runs`, `chart.toml:1041`) |
| R15 | thin line on, "sorted 21 ways by ideal-url-organizer" | his projects are one body of work | Q2 | `[[handoffs]]` (`chart.toml:1443`) state `runs` (reader fields ⊆ writer struct in both trees, test exists); `[[figures]]` "21 ways" at its HEAD | state `runs` |

Nothing else is drawn: no border, axis, legend, tint, hatch, symbol or light. Every stroke width comes from
`chartlib.stroke`, every glyph from `typeset`. Trap text is ink inside a dotted accent line with no fill (accent on
day paper is 4.1:1, under the 4.5:1 text needs, over the 3:1 a line needs; `test_trap_is_ringed_by_a_dotted_line`,
`tests/test_route.py:871`, holds the ring and its contrast on both themes).

### 5.2 Editions and where each is served

| Edition | Sheet, units | Served at | Column there | Smallest text on screen (19-unit runs on desk and mid, 26 on the phone, per the build report) |
|---|---|---|---|---|
| phone-day / phone-night | 600 × 1,121 | viewport ≤ 851 px; also the `<img>` fallback | 308 px on a 390 phone, 278 on a 360 | 13.3 px on a 390, 12.0 px on a 360 (floors 13 / 11, ROUTE-PHONE-PX) |
| mid-day / mid-night | 820 × 707 | 852 to 1,199 px | 482 to 765 px | 11.2 px at 852 to 17.7 px at 1,199 (floor 11, HERO-COLUMN-PX; DESK-PX does not run here); the 852–930 px window is §9.1b |
| day / night | 1,000 × 707 | ≥ 1,200 px | 766 to 846 px | 14.6 to 16.1 px (DESK-PX, from 1,200) |

Night is redrawn (strokes 20 % heavier, light cuts of the sans and mono), not inverted; every text colour clears
4.5:1 on paper in both (CONTRAST-*). The sheet is **at most 900 px tall from a 768 px viewport up** (HERO-COLUMN-PX,
`column.TALL_FROM = 768`, `column.py:47`); below 768 the profile is one column and the phone sheet is drawn 1.87 × the
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
| 3 | "Ben Russell builds…", Languages, Stack | Q1 | Languages: Python, Rust first (`[copy] languages_lead`, `chart.toml:58`, each only while some repository's `main_language`), then every other `main_language` by repository count, then by lines, then by name (`languages_line`, `render_readme.py:162`); the Stack line is his | `tests/test_round7.py:91` (the set, and "Python, Rust; " first); `test_order` (`:105`: the rest by repository count, Go with two repositories before C with one, and a lead language no repository has is dropped); the lines and name tie-breaks: no test (§10.15) |
| 4 | the pick: which tool for which job | Q2 | printed only while rustmapper's header, every `pick` figure row and the `no_services` release gate hold; the politeness clause only while Scrapy's stage 2 checks robots.txt (it does not today, so it is off) | `test_pipeline.py:211–223` (the pick's own assertions: `use == "pick"`, `header_verified`, `no_services`); FIGURES |
| 5 | rustmapper facts line | Q3 | `head.short`, built-on (from the manifest, in `[facts]` order), `test_functions`, CI conclusion + date + gates, lines; a key that is absent is omitted, never estimated. The agent-authorship clause prints (§9.2, the one home; the switch, §8.5) | `test_facts_block_prints_only_present_keys`; CI-GATES |
| 6 | the platform note, "Before you run 0.1.3:" cautions (≤ 7 items, ≤ 25 words each: `render_readme.LIST_MAX_ITEMS = 7`, `LIST_MAX_WORDS = 25`, `render_readme.py:670–671`, read by `checks/readme.py:318`; the fold has the same cap and takes the entries marked `fold = true` in `chart.toml`), a `<details>` fold for what the files miss, the code block (≤ 32 columns a line) | Q4, Q5 | each item is a gated wording with anchors and a probe. The three comment lines of the code block are wrapped at 32 columns for the phone's sake (the commands break at a backslash, which reads the same at any width); what that costs the desk is §11. M1 (`kind = "ci"`, `chart.toml:1419`, the `main`-has-fixed-it line) prints after the cautions only while its `cargo` gate holds (`render_readme.py:697, 740`); not printed today (its `absent "--ignore-robots"` anchor fails, §5.4 row 1) | README-CAUTIONS, README-CD, README-SUBCOMMAND, FLAG-WRAP, README-CODE-WIDTH; `test_no_fenced_line_over_32`; `test_time_only_when_cold` (`tests/test_proof.py:200`: the install time prints only from a cold-cache source build, and the wheel note names its platform); a `fold = true` entry never prints in the open list and no `fold_lead` means no `<details>` (`test_no_folded_item_in_the_open_list`, `tests/test_round13.py:156`; `test_no_label_no_fold`, `:178`); the code block's lines, the three stop-rule comments and the blank-rows grep among them, are pinned by `test_install_block_says_how_it_ends` (`tests/test_route.py:443`); M1 prints only on its `cargo` gate and names no idle timing (`test_m1_says_what_main_fixed_only_on_its_evidence`, `:673`) |
| 7 | Scrapy sentence, facts line, three bullets, how to run it, its two cautions, code block, where output lands | Q3–Q5 | same gating; every typed number has a `[[figures]]` row that holds at `96e7a1a` | FIGURES |
| 8 | **Also**: ideal-url-organizer, go_go_go, rust_llm_logger, Ai_code_detector | Q2 | one line each; "21 ways" must match the image's count | STRINGS-COUNT |
| 9 | `<details>` "15 more repositories" | Q2 | the count is computed (`repo_count` − profile − 2 − 4); the `<summary>` leads with the largest group and names every group, and every folded repository is in a group; every surveyed repository is linked once; forks are not surveyed | `render_readme.more_count` (`test_more_count_is_computed`, `tests/test_proof.py:179`); `test_fold_label_names_the_largest_group` (`tests/test_round12.py:224`); REPO-SET; `test_rest_repos_drops_forks` (`tests/test_proof.py:158`) |
| 10 | **Working rules** 1–3 | Q1 | exactly three; each cite's month is computed from his first commit that adds the anchor, the anchor is his, not an agent's, and is live at HEAD; typed numbers in a rule need a `block = "notices"` row | NOTICE-DATE, NOTICE-AUTHOR, NOTICE-LIVE, NOTICE-ANCHORS; `test_notices_first_four_and_no_release_line` (`tests/test_pipeline.py:296`: three rows, rule 4 cut) |
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

What a 0.1.4 cut from a fixed `main` does to the page. The last two columns were checked: "At HEAD" by reading the
clone at `32c2651`; "Needs here" by running `scripts/data/route.py resolve()` on today's `stats.json` with the probe
in question flipped, and by the 1a render (§9.1); the runs are in `docs/crit/prd/LOG.md`, round 1. The rule that
makes the column necessary is §7.3's row on conditional wordings.

| Fix in Rust-sitemap | Retires | Needs from the release | At HEAD `32c2651`? | Needs here, first |
|---|---|---|---|---|
| exits when the frontier drains | H1, the gap in the track, the stop-rule comment in the code block | probe `ends_by_itself` passes | yes: `tests/crawl_exits_when_idle.rs` exists (it runs with `--ignore-robots`, so the M1 anchor `absent "--ignore-robots"` fails and M1 is not printed); not in the release | **a C1 wording for a release that exits** (§10.9): H1 retires and the code block's stop-rule comments go, but C1's two wordings hold on `crawl_ctrl_c` / `second_ctrl_c` alone (`chart.toml:1005–1030`), neither names `ends_by_itself`, so the sheet still reads "press Ctrl-C once and wait for `Saved to`" under a release that stops by itself (the 1a render, §9.1) |
| robots.txt 404 → allow; fetched with the URL's own scheme; fail closed until it arrives | L4's https clause, L6/H0 (the https stall) | `tests/robots_4xx_allows_crawl.rs` at HEAD; probes `robots_read` passes, `robots_stall` fails | no: no such test; `src/robots.rs:16` still asks `https://<host>/robots.txt` only | nothing: H0 and L6 → `""`, L4 drops "and reads `robots.txt` only over https" |
| `parse_crawl_delay_secs` in the release | draws S2; rewords L1 and L4 | the release anchor; probe `crawl_delay_obeyed` | yes: `src/robots.rs:53`, called at `src/frontier.rs:913`; not in the release | **a probe `crawl_delay_obeyed` in `runcheck.py`** (named at `chart.toml:1080, 1155, 1160`; its comment at 1074 says "not written yet"; the run check has no such step). Without it every L1/L4 wording for a parsing release needs a probe that never ran, both go unverified and ROUTE-UNVERIFIED fails the build. `test_never_both` (`tests/test_round15.py:124`) already forbids S2 beside L4's "ignores `Crawl-delay`" |
| default UA with a contact; `From` | L7 | probe `ua_seen` fails on a contact | no: `src/cli.rs:40` default `RustSitemapCrawler/1.0`; no `From` in `src/network.rs` | **an `instead` on L7 with `fails = ["ua_seen"]`, `text = ""`**: with `ua_seen` failed L7 has no wording that holds, goes unverified, and the build fails |
| disallowed and `noindex` pages left out of `export-sitemap` | X1's clauses | probes `sitemap_keeps_disallowed`, `sitemap_keeps_noindex` fail | no: no `noindex` handling in `src/` | nothing for the disallowed clause (X1 drops "and disallowed"); **a wording for a release that also drops `noindex` pages**: with both probes failed X1 goes unverified |
| `[project.scripts] rustmapper` in the wheel | the image prints `rustmapper crawl` | `edition.scripts` from the wheel's RECORD | no: `pyproject.toml:55 bindings = "pyo3"`, no `[project.scripts]` (§11) | nothing |
| SIGTERM writes the file; `resume` after a kill | W1 drawn; "resume" allowed next to rustmapper | probes `kill_writes_file`, `resume_after_kill` pass | no: no signal handler in `src/` | **lift W1's `drawn = false` by hand and write a wording that holds on a passing kill**: with `kill_writes_file` passing the fallback "logged to disk, then saved to redb, in batches" prints and W1 stays undrawn (`test_round13.py:258`); `resume_after_kill` is named by no entry, only a comment (§10.18) |
| a LICENSE | the LICENSE-FLAGSHIP warning | GitHub detects it | no | nothing |

So three of the eight rows retire by themselves (robots, export's disallowed clause, LICENSE), the packaging row is
pure release work, the exit row retires its box (row 1), and four rows (exit's C1 wording,
Crawl-delay, User-Agent, SIGTERM) plus the `noindex` half of the export row need a probe or a wording in this
repository before a fixed release helps rather than fails the build (§10.9).

## 6. How the pipeline enforces it

```
build_stats.py  → assets/stats.json   clones (depth 1 + history), GitHub REST, PyPI JSON + wheel RECORD + sdist,
                                       runcheck.json; routes/handoffs resolved against the code
build_assets.py → assets/v9/hero-*.svg six editions; build-report.json with every text run's source and truth
                                       (tracked, and stale as committed: §10.7)
render_readme.py → README.md marker blocks; tokens.py --md → DESIGN.md
check.py --tier fast,render           28 plug-ins; exit 0 pass · 1 fail · 2 warnings · 3 could not check
publish_chart.py                       force-push of the sheets to the orphan `chart` branch, before main is touched
```

- **Weekly job** (`profile.yml`): scheduled for Sunday 06:20 UTC (cron `20 6 * * 0`, `profile.yml:13`; "The `schedule` event can be delayed during periods of high loads", GitHub docs, and run 12 ran at 12:52 UTC), on push to `main` (scripts, chart.toml, workflow, `assets/log.json`,
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
  cannot run is `skipped`, never a pass (ROUTE-PROBE-SKIPPED). 17 of the 18 are named by a wording's `runs`/`fails`
  in `chart.toml`; `resume_after_kill` is run every week and read by nothing (`chart.toml:900` is a comment; §5.4
  row 7; §10.18). `runcheck.py:8` still says it "probes four behaviours".
- **Tests**: 539, `python3 -m unittest`, 22 s. Fixture trees, never the network. 91 of them belong to sheets that
  are off the page (§10.8 names the modules); the product's own count is 448.
- **Review**: how the rounds are run is appendix D (G17–G19 and its last table).

### 6.1 Failure and rollback

| Event | What the visitor sees | How it is undone, by whom |
|---|---|---|
| the data fetch fails | the page as last week, same dates (above) | nothing to undo. The mark is the provenance line's date: it prints `runcheck.rustmapper.date` from `stats.json` (`render_readme.py:1017`; "on 10 Oct 2026" today, `README.md:151`), so a rebuild from last week's file prints last week's date; no second mark (G6; §10.13 closed) |
| a gate fails (exit 1: a `fail`; exit 3: an `error`, which is one of the runner's five codes, appendix B's first row, or a plug-in that could not check: FRAMES-TOOL, -RENDER, -SILHOUETTE, PERF-TOOL, -RUN, REPORT-STATS, FLAG-WRAP, MOTION-XML, MOTION-READ, the nine `error` emits in `scripts/checks/`) | nothing new: the page and the `chart` branch as before | nothing to undo; the run's `::error::` lines say what failed |
| a build passes the gates and prints something wrong | the new page | **No CI path rebuilds from an older `stats.json`**: every trigger re-surveys (`build_stats.py --runcheck …`, `profile.yml:106`, live with `GITHUB_TOKEN`), so a `workflow_dispatch` brings the figure back if it came from the data; and reverting the bot commit is itself a push that re-surveys, because `assets/log.json` is in the commit (the `for f in` loop, `profile.yml:160`) and in `push: paths` (`:25`). Rollback is local: a session checks out the last good `assets/stats.json`, runs `build_assets.py`, `render_readme.py`, `check.py --tier fast,render`, `publish_chart.py`, and opens a PR with `stats.json`, `README.md` and `DESIGN.md`; Ben merges it (appendix D: never push to `main`). Those three paths are not in `push: paths` (`profile.yml:22–27`), so that merge does not re-survey; if the fault is in code or `chart.toml`, the revert is a second PR, whose merge re-surveys, and it goes first or the next run reprints the fault. The `chart` branch has no history (`publish_chart.py` docstring, lines 2–14: one orphan commit, force-pushed), so there is no older sheet to point at, only a rebuild |

## 7. The rules, and how each is implemented

Status: **gate** (`check.py` fails; **gate (warn)** when it only warns), **test** (`unittest`), **review** (a reviewer
judges it each round), **process** (how the session works), **open** (not held by anything yet). The last column is
where it lives. Status is what the holder did on the round-16 build, not a promise (§0, first bullet). The 28
plug-ins emit 168 live codes, counted by the grep in `docs/crit/prd/LOG.md`, round 4 (169 code-shaped strings less
three that are not codes, plus `FIGURES` and `TYPE`, which have no hyphen; the four bare codes of the idle plug-ins
are not counted). The grep covers `scripts/checks/` only; the runner's own five codes are appendix B's first row.
The number is a grep, not a register, and §10.12 is what would pin the set. The engineering rules that trace to no sentence of his (budgets, XML hygiene, the stats
invariants, paint order, the alt poem, the position line) sit in the table nearest their subject, so that every live
code has a row here or an "idle" mark in appendix B.

### 7.1 Don't name the theme

| Rule | Status | Where |
|---|---|---|
| No theme word on the image or in its alt text: chart, sea, ship, harbour/harbor, survey, unsurveyed, buoy, light, berth, approach, pilot, mariner, nautical, sail, anchorage, ahoy, arr (8 Oct 14:22, "survey is weird", is the one word he banned by name: `survey` is in `THEME_WORDS`, `checks/route.py:60`, and in `design.py:18 EXTRA_WORDS`) | gate, test | ROUTE-WORDS; `test_no_theme_words` (T-WORDS) |
| No theme word in DESIGN.md | gate | DESIGN-FRESH + `design.theme_words` |
| No theme word in the README's visible prose | **review only** | §8.3 q.1 carries the grep; §10.1 proposes the gate |
| No theme word in a `chart.toml` string that any live sheet reads; retired sheet modules and their strings are deleted, not kept | **open** | `[copy] unit_chart` (read by nothing), `unit_hero`, `unit_approaches`, `limit_label`, `footer_line` ("The chart ends here. The web doesn't.") survive at `chart.toml:35–39`, read only by the retired `soundings`, `approaches` and `footer` modules (`build_assets.SHEETS = ["hero"]`); §10.8 |
| Banned phrases anywhere (SVGs, report, README, chart.toml): ILLUSTRATIVE, PENDING, SEEDED, NOT FOR NAVIGATION, Here be dragons, Fair winds, example.com, Oct 2024, "thanks for reading", "that's a mood", "Hi I'm Ben", "Hi, I'm Ben", "drawn not templated", "drawn, not templated", REFRESHED DAILY, "works at night", lorem, TODO, FIXME, `<!-- POSITION` (the 20 entries of `strings.py BANNED`) | gate | STRINGS-BANNED (the SVGs); the same scan per file as STRINGS-MANIFEST and STRINGS-ALT (the report's text runs and alts), STRINGS-README, STRINGS-TOML (`strings.py:147 scan()`, called at `:164–183`) |
| No themed headings; headings are "Also", "Working rules" | test | `test_committed_readme_is_the_one_chart_page`, round tests pin the headings |
| Every design departure from the type and layout rules names a project fact or a measured constraint, never the theme | test | T-BREAKS over `route.py BREAKS` |
| No pirate language | gate (image) | THEME_WORDS `ahoy`, `arr` |
| No pirate talk, no running bit; a one-off word as a joke is allowed, more than a couple is "cringy" (G10, his two rules) | review | two winks today, named in §8.3 q.4: "Boring under load." (working rule 1), "why engines are hard" (game_engine's line); neither uses the one-off allowance, and nothing bars a later one |
| No ships, boats, buoys, roses, lights, hatching, legends | **review**; T-PURPOSE holds containment only | `test_every_element_has_a_purpose` (`tests/test_route.py:812–829`) checks that every group id is a PURPOSE key and that no `path`, `circle`, `rect` or `use` sits outside a group; it never looks at what is inside a group, so a hull drawn inside `hero-R5` would pass. The only shapes today are bars, rings, lines, a dotted box, by the reviewer's eye (§10.11) |

### 7.2 Everything has a purpose; nothing has a size

| Rule | Status | Where |
|---|---|---|
| Every drawn element has a PURPOSE row; no row without an element | gate (drawn → row); test (row → drawn, with S2 and W1 excused by a hand list) | ROUTE-PURPOSE is one-way (`scripts/checks/route.py:43`: a drawn element without a row); `test_every_element_has_a_purpose` subtracts `{"S2", "W1"}` by hand (`tests/test_route.py:819–822`), so a third undrawn row needs a test edit (§10.11) |
| No shape's size or position depends on any count (tests, lines, commits, repositories) | test | `test_nothing_has_a_size` (two stats fixtures differing in every count give identical geometry) |
| The image exists only where the subject has a route a visitor travels | decision | DECISIONS: four concepts scored on the goal; A chosen 22/30 on goal |
| Lookups (counts, languages, the other repositories) go in text, never in the picture | design | SPEC §0; the facts lines |
| One home per fact: no run of 5 words, or 3 words naming code or a date, both on the image and in the README's prose (exceptions: `pip install rustmapper`, `Received work item`) | gate, test | STRINGS-TWICE, HERO-SELF-TWICE; `test_code_face_and_self_twice` (`tests/test_route.py:620`: HERO-SELF-TWICE and TYPE-CODE on the build) |
| One count for one thing: the image's "21 ways" must appear in that repository's README line | gate | STRINGS-COUNT |

### 7.3 Honest data only

| Rule | Status | Where |
|---|---|---|
| Nothing invented or estimated; an absent key is omitted, never filled | gate, code | STRINGS-UNMEASURED (every hero text run's `truth` is `measured`); ROUTE-STRINGS (every run's key is an allowed source); `facts_block` prints only present keys (test) |
| Every figure printed has a register row with a definition, a key and a source commit | gate | AUDIT-STALE (the register is regenerated by `audit_figures.py`); AUDIT-COVER (every digit run on the image and page is covered) |
| Every number typed into README prose rests on a `[[figures]]` row that holds at that repository's HEAD | gate, test | FIGURES (`proof.py` re-reads the anchor); `test_committed_readme_has_no_bare_figure` (`tests/test_proof.py:137`: the committed README through `figures_check` in the suite) |
| Every claim about the code rests on anchors at HEAD and in the released sdist; drawn only when both hold | gate, test | ROUTE-UNVERIFIED, ROUTE-HEADER, ROUTE-LABEL, ROUTE-WAITING (warn; `test_today_warns_once`, `tests/test_round15.py:155`: it fires once, at `warn`, naming S2); T-BOTH (`tests/test_route.py:107`: true in both trees or not drawn); ROUTE-LABEL's tests, `test_label_only_when_the_file_is_anchored_in_both` (`:394`) and `test_handoff_reader_label` (`:609`) |
| Anchor forms: a file exists, contains `text`, lacks `absent`; `const` prints the code's value and must agree between trees; `fn` narrows to a body; `field` and `arg` read a struct field or a clap default; `edition.scripts` comes from the wheel's RECORD; a hand-off's state from the reader's and writer's structs | test | T-ANCHOR (`tests/test_route.py:93, 375, 386, 558, 576`), T-SCRIPTS (`:417`), T-WHEELS (`:485`), T-HANDOFF (`:517`) |
| A wording that states a condition (`unless`, `when`, `only`, `if`: `scripts/data/route.py:59 CONDITIONAL`) names a probe in `runs`/`fails` or carries a `producer` anchor; a setter anchor alone verifies nothing. This is the rule behind §5.4's "Needs here" column: a Crawl-delay wording needs `crawl_delay_obeyed` (§10.9) | test | `test_every_committed_conditional_wording_has_a_probe_or_producer` (`tests/test_round6.py:88`); `producers()` (`route.py:236`) |
| Forks are not surveyed | test | `test_rest_repos_drops_forks` (`tests/test_proof.py:158`) |
| Every README link to one of his repositories is to a surveyed one, every surveyed repository is linked once, none twice inside `<details>`, and the "N more" count is the number linked there | gate | REPO-SET (`checks/repos.py:3–5`) |
| The flagship has a LICENSE GitHub detects | gate (warn) | LICENSE-FLAGSHIP (`checks/readme.py:7`); stands today (§8.2) |
| The install and crawl commands are run, not quoted; the entrance is drawn only within 14 days of a passing run of the same version | gate, test, CI | ROUTE-ENTRANCE; `test_failed_runcheck_hides_the_entrance` (`tests/test_route.py:1069`: a failed run check or another version hides R2) and `test_runcheck_gate_ignores_probes` (`:225`: a probe step is recorded with `gate: false`); the `runcheck` job |
| A subcommand named next to "rustmapper" must not be one the run check saw fail | gate | README-SUBCOMMAND |
| A working rule's cite month is computed from his first commit adding the anchor; the anchor is his, not an agent's; the code is live at HEAD; the cite reads `<repo>, <Mon YYYY>: <what>.` | gate | NOTICE-DATE, NOTICE-AUTHOR, NOTICE-LIVE, NOTICE-ANCHORS; NOTICE-CITE (the form, `notices.py CITE_FORM`) |
| The stats file is readable, unseeded, schema-valid, with provenance, and internally consistent; a claim is measured only with a source and a sha; PyPI unreachable with no cache stops the build. Warnings: an edition from cache, a repository not re-surveyed, a run with no live clone, a repo-count drift, no notices, the calendar disagreeing with the clones by over 10 % | gate | `data.load`, `data.seeded`, `data.schema`, `data.provenance`, `data.invariant`, `data.claims`, `data.edition` (fail, `checks/data.py:53–90`); `data.edition` (cache), `data.stale`, `data.clones`, `data.repo_count`, `data.notices`, `data.calendar`, `data.unsurveyed` (warn); `data.calendar` is `info` when no GraphQL window was fetched (`checks/data.py:69`); `data.tide`, `data.variation` idle |
| `assets/log.json` (the retired `log` sheet's record, still committed by the workflow, `profile.yml:160`) is readable, schema-valid and rule-consistent; its version matches the edition's and its shard count the machine's | gate | `log.load`, `log.schema`, `log.rule` (fail); `log.version`, `log.shards` (warn); `log.computed` (info) (`checks/log.py:47–69`); `log.shards` warns on every build (§8.2); the file, the plug-in and its codes go with §10.8 |
| The printed position line equals `[position] text`; an unset key fails, `""` warns and omits the slot, a README still showing an old line warns; no ⟨ ⟩ placeholder in `[contact]`; no `<!-- POSITION` comment in place of a line | gate | POSITION-UNSET, -PLACEHOLDER, -MISMATCH, -BLOCK, -COMMENT (fail); POSITION-EMPTY, -STALE (warn); CONTACT-PLACEHOLDER (`checks/position.py`) |
| The README has exactly one hero picture block, with paired markers and one `<picture>` that names `hero-day.svg`, not inside `<details>`; the staleness check itself must be able to run | gate | README-PICTURE, README-PICTURE-FOLDED (fail); README-MISSING, README-RENDER (warn) |
| A skipped probe is never a pass; the code-only wording prints | gate (warn), test | ROUTE-PROBE-SKIPPED; `test_skipped_is_not_a_pass` |
| Sweep days (bulk edits touching most repositories: 9–10 Nov 2025, 1 and 7 Oct 2026) are excluded from any activity figure | code, test | `sweep_dates`; `test_sweep_days_are_named_not_removed`; no activity figure is printed now |
| Test counts are functions (`#[test]`, `def test_`), never files; languages from lines in the clone, never the REST field; generated trees excluded | code, test | `test_test_function_patterns`, `test_main_language_per_repo_from_lines`, `[lines.exclude]` |
| Agent-authored commits are counted apart and never as his | code, test | `agent_authored`, `coauthored_total`; `test_agent_authored_and_agent_share`; `test_bots` (`tests/test_data.py:83`: `is_bot` on "Claude" and "dependabot[bot]", not on him) |
| No commit totals, no "last commit" (sweep-adjusted, contradicted the CI date) | test (the provenance line); the facts lines' clause prints by decision | the provenance-line test bans them; the agent-authorship clause: §9.2 (the one home), §8.5 (the switch) |
| CI status is the API's conclusion for the last run on main, with its date and the jobs it gates on | code, gate (warn) | `repos[].ci`; CI-GATES warns when the gate list is empty |
| `scrape_interval` is read from the job, not the global | test | `test_scrape_interval_is_the_jobs_not_the_global` (no longer printed) |
| No placeholder survives: ⟨ ⟩, `<!-- POSITION`, TODO | gate | POSITION-PLACEHOLDER, README-PLACEHOLDER, README-TODO, STRINGS-BANNED |
| Two builds from the same stats are byte-identical | test | `test_two_builds_byte_identical` |
| Figures retire by themselves when the tool changes | code, test; **true of some §5.4 rows, not all** | `instead` wordings, `waits`, `fails`/`runs`; `test_retires_when_fixed`, `test_a_crawl_that_ends_retires_h1`. Which rows: §5.4, column "Needs here" |

### 7.4 Phone first, then desk

| Rule | Status | Where |
|---|---|---|
| A phone edition drawn at its own width (600 units), served to viewports ≤ 851 px and as the `<img>` fallback | test, gate (render) | `test_picture_order`; HERO-FALLBACK |
| No phone text under 13 px on a 390 px phone (image 308 px) or 11 px on a 360 (278 px) | gate | ROUTE-PHONE-PX |
| The sheet is one screen: ≤ 900 px tall **from a 768 px viewport up**; below 768 the height is not bounded (the phone sheet is 1.87 × the column) | gate (render), test | HERO-COLUMN-PX, `column.TALL_FROM = 768`, `column.TALL_PX = 900` (`column.py:47–48`); `test_phone_height_holds_at_851` (`tests/test_round15.py:295`: the phone sheet's drawn height at 851 px ≤ `TALL_PX`, W1 undrawn, H0 one line) |
| Desk words ≥ 14.5 px from a 1,200 px window; a mid edition for 852–1,199, whose only floor is 11 px | gate (render) | DESK-PX from `breakpoint_px + 1` (read at `column.py:231`; `column.DESK_MIN_PX = 14.5`, `:50`; `chart.toml:9`); the mid window is held by `column.MIN_PX = 11.0` (`:45`); the 852–930 window is §9.1b; `test_the_old_breakpoint_fails_on_tablets` |
| Code block lines ≤ 32 columns (what a 360 px phone shows) | gate | README-CODE-WIDTH (`CODE_COLUMNS = 32`); `test_no_fenced_line_over_32` |
| A flag a reader types (`--workers 1`) never wraps mid-flag on a phone | gate (render) | FLAG-WRAP |
| Cautions: one list, ≤ 7 items, ≤ 25 words each; the file faults folded | gate | README-CAUTIONS, README-DETAILS |
| Type floors: desk and mid 19 (serif 25), phone 26 (serif 30); sizes on the scale | gate | TYPE (`tokens.py:73–74 FLOORS`, read by `type.py`) |
| Nothing overlaps; every box inside the sheet less a 6-unit frame; words clear the dotted line by ≥ 8 units | gate; gate (warn) for two | BOUNDS-COLLIDE, -EDGE, -EXCLUSION, -MORE (fail), -TEXTURE (warn, `bounds.py:85`), -NO-MANIFEST (warn, `bounds.py:56`: a sheet with no text manifest in the report is skipped, so every BOUNDS fail rests on the manifest being written) (fast); BOX-PAD (render) |
| Each edition within budget: raw ≤ 300 KB, gzip ≤ 100 KB, phone raw ≤ 120 KB, ≤ 3,000 elements, one desk set ≤ 250 KB gzip; the report's sha256 matches each SVG and `stats.json`; the per-sheet target (hero 170 KB raw / 60 KB gzip) warns | gate | SIZE-RAW, -GZ, -PHONE, -PAGE, -ELEMENTS; SIZE-TARGET (warn); REPORT-SHA, -MISSING, -ORPHAN (fail), -BYTES (warn, `size.py:56`), -STATS (error, `size.py:70`) (`tokens.BUDGETS`, `tokens.py:131`) |
| Every sheet parses; no live `<text>`, `<script>`, `<style>`, `<image>` or external href (the rule behind §5.1's glyph outlines); ids unique and sheet-prefixed; every `#ref` resolves; the root is `<svg>` with a viewBox that matches the report | gate | XML-PARSE, -FORBIDDEN, -EXTERNAL-HREF, -ID-DUP, -ID-PREFIX, -REF, -ROOT, -VIEWBOX, -SIZE; idle (animation): -KEYTIMES, -FADE-BASE (fail), -SET-LOOP (warn, `xml.py:82`) |
| Sheet height ≤ 770 (desk), 1,246 (phone), 964 (mid) units; rings, bars and words painted after the track, the loop and the hand-off line; the loop's arrowhead keeps ring_r + 2 from every ring's centre row; `stats.json` carries the route | gate, test | ROUTE-HEIGHT (`checks.route.HEIGHT`, `checks/route.py:70`), ROUTE-PAINT (`test_lines_are_painted_under_the_marks`, `tests/test_route.py:971`), ROUTE-ARROW (`test_loop_arrow_is_on_bare_line`, `:1002`), ROUTE-MISSING; ROUTE-HANDOFF (info: each hand-off's state) |
| Rows start at one left edge; the project name sits ≥ 2 role pitches under the role line | gate, test | ROUTE-LEFT-EDGE, ROUTE-HEAD-GAP; `test_one_left_edge_and_desk_files_left_of_the_track` (`tests/test_route.py:953`: `left_edge()` clean on every edition) |
| Contrast: text ≥ 4.5:1, lines ≥ 3:1, both themes; red/green kept apart for CVD | gate | CONTRAST-TEXT, -LINE, -DANGER, -TINT, -LIGHT, -LIGHTS, -RG, -CVD |
| Night redrawn, not inverted | code | `tokens.THEMES`, `W_NIGHT` |
| The six editions are on the `chart` branch before `README.md` names them (8 Oct 11:13: "Merged but all images are unavailable"); held on the live page, not only on the merge commit, once §10.23's `--keep-current` exists (§8.6) | test, process | `publish_chart.unshipped` (`scripts/publish_chart.py:81`); `test_publish_before_commit` (`tests/test_round15.py:193`); `test_publish_needs_every_named_edition` (`tests/test_round12.py:124`); `profile.yml` publishes before the commit; §8.1 item 5; §8.6 |
| Verified on a real iPhone, in Safari and the GitHub app, light and dark | **open** | §8.4, the one home of this check |
| Even density across the image | review | no metric; held by construction (one pitch, one left edge, fixed marks); §8.3 q.3 |

### 7.5 Copy

| Rule | Status | Where |
|---|---|---|
| Third person throughout; no I, my, me | test | `test_no_first_person_on_the_page` |
| Never "this repository" on a profile | gate | THIS-REPO |
| "His Scrapy repository", not the framework; American spelling | test (the first mention and seven words) + review (the rest) | `test_first_mention` (`tests/test_round7.py:367`: "His" before the first "Scrapy" in the prose; PyPI before Scrapy on the link line); `test_one_spelling` (`:391`: summarise, summarised, organise, optimise, recognise, normalise, summarisation absent; "summarized" present); `[copy] repo_words`; §8.3 q.4's grep extends the test's seven |
| A code block whose first line is `cd <path>` never follows a sentence that puts the reader in that folder already | gate | README-CD (`checks/readme.py:247`) |
| The License bullet renders when `LICENSE` and `LICENSE-ASSETS.md` exist | gate | README-LICENSE (`checks/readme.py:313`) |
| Existing wording stays unless cut; every change carries its review round in a `chart.toml` comment | process | the comments in `chart.toml` |
| The role line is re-read by 2027-06; a `[copy.review]` key names a `[copy]` key and reads `YYYY-MM` or `YYYY-MM-DD` | gate (warn) | EXPIRY-PASSED, EXPIRY-KEY, EXPIRY-FORMAT (`expiry.py:37–42`: all three warn, never fail) |
| Alt text ≤ 25 words, not starting "The", says what the image shows in plain words; its last sentence ≤ 10 words | gate, test | ALT-LONG, ALT-THE, ALT-LAST; ALT-NO-README (warn); T-ALT (`tests/test_route.py:832`: length, first word, the three names, the "How to install" prefix) |
| The alt's last sentence equals `[alt] alt_poem`'s hero line ("It loops until one Ctrl-C writes data/sitemap.jsonl.", `chart.toml:563`) | **gate (warn); no test** | ALT-POEM (`alt.py:50` emits `warn`); `test_pipeline.py:553` checks the poem's length only; the fix is §10.24 |
| C1 says `Saved to` without the tool's colon mid-sentence (the anchor still tests `println!("Saved to: `); "once" is C1's word alone on the route; H1 never says "done" while H0 is drawn | test | `test_c1_has_no_colon_mid_sentence` (`tests/test_round12.py:208`), `test_once_is_c1s_alone` (`:216`), `test_pairing` (`tests/test_round16.py:85`) |
| Code in the code face; code spaces at the word space; no file names left of the track | gate, test | TYPE-CODE (`test_code_is_in_the_code_face`, `tests/test_route.py:1036`), ROUTE-CODE-SPACE (`test_code_spaces_are_word_spaces`, `:1013`), ROUTE-LABEL (`test_label_only_when_the_file_is_anchored_in_both`, `:394`; `test_handoff_reader_label`, `:609`); `test_no_edition_draws_file_labels` (`:1030`: `file_right` is `None` on every scale) |
| The release label sits right after its command, never at the right edge | gate, test | ROUTE-RELEASE; `test_release_label_follows_its_command` (`tests/test_route.py:984`) |
| No "generated by" line a visitor can read; no schedule in the provenance | test | the provenance-line test bans "generated", "regenerated", "weekly" (§10.6 on the two maintainer comments) |
| The thesis line is gone | config; **held by an absence only** | `[copy]` and `[copy.review]` carry no `thesis`; "wrong about itself" is in neither `BANNED` nor the test's `gone` list, and `docs/BEN-TODO.md:39` still carries it (§10.10) |
| Garden paths and reduced relatives read once | review | §8.3 q.4 |

### 7.6 Process

The process rules (never push to `main`; every PR mergeable; the trailers; no generated-by footer; the stop hook; his
email; the review count; failures reported as they are; `BEN-TODO.md`) are appendix D, with their rows unchanged:
they are how the session works, not what the page is. Two are not met today: the PR for this branch (§10.17) and round 5's stop rule, which round 6 ran against (appendix D's last table).

## 8. Acceptance criteria for the final product

### 8.1 Mechanical (must all hold on the commit that merges)

A §10 item that blocks the merge is also a line here. Items 1–5 are run by a session on the branch; 6–8 are not merge
blockers and say where each lives; the first merge, a procedure rather than a state, is §8.6.

1. `python3 -m unittest`: all pass.
2. From the committed `assets/stats.json`, no network: `python3 scripts/build_assets.py && python3
   scripts/render_readme.py --check && python3 scripts/check.py --tier fast,render`: 0 fail, 0 error; warnings only
   from §8.2. The build comes first (§10.7). A fresh *survey* (`build_stats.py` live: `GITHUB_TOKEN`, the clones,
   PyPI, a macOS `runcheck.json`) is item 4's job, not this item's; the two can give different wordings (§11).
3. `render_readme.py --check` clean; `DESIGN.md` and `docs/data/AUDIT.md` regenerated (README-STALE, DESIGN-FRESH,
   AUDIT-STALE).
4. A `workflow_dispatch` dry run of `profile.yml` on the branch: the macOS run check uploads, the build gates, the
   publish dry-runs. Only the dry run is permitted on a branch: a dispatch with `dry_run` false builds whatever ref
   it ran on (`actions/checkout@v4` with no `ref`, `profile.yml:72–74`) and its commit step runs `git pull --rebase
   --autostash origin main && git push origin HEAD:main` (`:174`), which pushes that branch's commits to `main`: the
   merge, done by the bot (§10.22).
5. The six editions exist on the `chart` branch before `README.md` names them (`publish_chart.unshipped`); which
   publish, and when, is §8.6.
6. `[position] text` and a contact: §9.0 (a); not a merge blocker (6b, the contact, is §10.21).
7. The agent-authorship clause on the facts lines prints on the merge commit as it does today (`README.md:38, 86`)
   unless Ben has said "strike" or "share" (§9.2, the one home of the decision; his word is §9.0 (b)). The switch,
   `[facts] agent_clause`, is added after the merge (§8.5, §10.5), not before: its default reproduces this page.
8. The five retired `[copy]` keys at `chart.toml:35–39` and the retired sheet modules go in the first fix PR after the
   merge (§10.8), not before: no live sheet reads them (`build_assets.SHEETS = ["hero"]`, §7.1) and 8 Oct 14:52 is
   about what the user is shown.
9. The first merge: §8.6, with the PR open first (§10.17). Owner: a session; the order is not Ben's to pick.
10. Under 2b, L4 and L5 carry `fold = true` in `chart.toml` (§10.19); his yes to 2b covers it (§9.0 (c)).

### 8.2 Warnings allowed today, each with an owner

| Warning | Why it stands | Who clears it |
|---|---|---|
| LICENSE-FLAGSHIP | Rust-sitemap has no LICENSE | Ben, in Rust-sitemap |
| ROUTE-WAITING S2 | 0.1.3 has no Crawl-delay parser; HEAD lacks the P1 test | Ben, 0.1.4 |
| log.shards | `claims.shards` is `num_cpus`, the machine has 8 | harmless; goes with the retired `log` module (§10.8), in the first fix PR after the merge |
| POSITION-EMPTY | `[position] text` is `""` (§9.0 (a)); the slot is omitted | Ben, in `chart.toml`, before or after the merge (§8.1 item 6) |

These are the four warnings of the round-16 build (§0; `renders/round-16/gate.txt`) and the allowed set on the merge
commit; three once (a) is set, and two once §10.8 is done after the merge.

### 8.3 Judged (each review round, in this order)

Questions 1–4 are his (9 Oct 20:50: *"is it matching what I'm saying? Is it doing what I'm saying? Is it
accomplishing my goal?"*). Each has lines a reviewer ticks; a line that fails is a must-fix.

1. **Does the image meet his goal?** First, before reading §1 or §5.1, the reviewer writes one sentence saying what
   the image shows; it must name a tool, how you start it (an install or a command) and an output, and it is logged
   against G3a in `docs/crit/prd/LOG.md` beside §1's own sentence (9 Oct 11:32: "what's happening?"). The line is
   a product reviewer's, given the image before any document; a PRD reviewer has read §1 first, and the answers
   logged from PRD rounds say so. Then: every
   `<g id="hero-*">` has a PURPOSE row and the reviewer can state each mark's
   purpose without the table; nothing has a size (T-NOSIZE); no theme word on the image or alt (T-WORDS) and none in
   the README's visible prose (a whole-word grep of THEME_WORDS over the prose outside comments and the `<picture>`;
   round 1 found only "Helm chart", a project fact); the three second-reading marks are there (G1a: the loop bracket,
   the gap under the box, the line past the end bar); each element's Q (§5.1) is the question a stranger would ask of
   it (name any you would retag; T-PURPOSE checks only that a tag exists, §2).
2. **Is every figure true?** Re-measured from `stats.json`, the audit, the sdist and the clones; every typed number
   has a `[[figures]]` row; nothing estimated.
3. **Does the page read on a phone?** At 390 px the image is one screen (575 px) and every word ≥ 13 px (13.3 today);
   nothing cut off; no code line over 32 columns; ROUTE-LEFT-EDGE and ROUTE-HEAD-GAP pass, and the reviewer names any
   area of the image that reads denser than another (G3); none is the pass.
4. **Does it tell a stranger about him and which project to open?** The first two phone screens show his name, what he
   builds, rustmapper and Scrapy by name and the link line (whether it carries a contact beyond Email is noted, §8.1
   item 6b; its absence is not a must-fix); third person throughout; winks ≤ 2 and they are the two named in §7.1;
   American spelling (`test_one_spelling` holds seven words; the grep extends it: colour, behaviour, organise,
   licence, grey, centre, favour, catalogue: none); no sentence a reviewer had to read twice (name it if there is
   one).
5. **Would the reviewer ship it as is?** Advisory. This is the reviewer's taste; it has no pass condition and it is
   not his bar. Only Ben's own merge closes the product (§7.6).
6. **Would the reviewer screenshot the image and send it to someone?** A no is a must-fix, and the reviewer says
   what would make it a yes (7 Oct 15:30: "stunning and fun", his first sentence; G1, G1c). Second line, advisory:
   what would they say it was; the answer is logged against G13a in `docs/crit/prd/LOG.md`. "A flowchart" is the
   risk in §11 and this is where it is asked, every round. Third line, for G1d and G1e: does it look made with care,
   where did the reviewer see it, and would someone who designs for a living see a designer's hand, and where.
   Fourth line, advisory, for G1b ("is it interesting does it draw in the user"): what on the first screen made the
   reviewer scroll to the second; if nothing, say so. No gate, no test.

**Done** = §8.1 all hold on the merge commit **and** §9.0 (c) is a yes **and** one product review round on that
commit's build (three reviewers answer yes to questions 1–4 and to q.6's first line, no must-fix left open). The
third clause has not yet been true of any build: round 16's reviewers said "None meets the goal yet"
(`docs/crit/round6/LOG.md`, round 16), its fixes are `027f081`, and no product round has judged that build, so the
round runs on the PR's build (§0). §8.4 follows the merge (it needs the live page) and is logged in the first week
after it. Done means ready for Ben to merge; his merge is the acceptance (§7.6: he merges PRs). "Must-fix" here means
a product-review must-fix (`docs/crit/round6/review-rNN-*.md`); PRD-review must-fixes live in §10 and
`docs/crit/prd/LOG.md`. The product rounds' scores are in `docs/crit/round6/LOG.md`.

### 8.4 On a device (once, on the live page in the first week after the merge)

Owner: Ben (the session has no device; §9.0 (d)). After the merge, open the profile on an iPhone in Safari and in
the GitHub app, light and dark, and send the screenshots in a session; the session writes the entry in
`docs/crit/round6/LOG.md` under the round that merged, with the screenshots' paths (two `LOG.md` files exist,
`docs/crit/round6/` and `docs/crit/prd/`; neither has a device entry today). It cannot run before the merge: the
profile shows `main`'s README, and this branch's image is on GitHub only after a publish (§8.6). If it
fails, §6.1 is the back-out. Pass conditions:

- Safari at 390 px serves `hero-phone-day` in light mode and `hero-phone-night` in dark (the `<source>` order in
  `README.md` lines 7–12).
- The GitHub app shows `hero-phone-day` in both modes via the `<img>` fallback (`README.md` line 13, HERO-FALLBACK);
  one community report says the apps send the light theme regardless (cited in `docs/crit/prd/review-r01-2.md`,
  source 16; unverified).
  Any night edition there is also a pass; a missing image is a fail.
- The image is one screen (≤ 900 CSS px; 575 at 390).
- The first two screens show his name, what he builds, rustmapper and Scrapy by name and the link line.
- Anything else is a fail to log with a screenshot.

### 8.5 After merge

- **A failed weekly run.** GitHub sends a scheduled workflow's notifications "to the user who initially created the
  workflow", and to whoever last edits the cron syntax instead (GitHub docs, "Notifications for workflow runs"); the
  cron line was last changed in `eeea9d1` by Benjamin Russell, 9 Oct (`git log -S'20 6 * * 0' --
  .github/workflows/profile.yml`), so a failed run reaches his inbox if Actions notifications are on in his settings
  (he can choose "only when a workflow run has failed"). A session must not edit that line, or the notifications
  follow a commit author who is no GitHub user. What Ben does with the email: open a session and paste the run's
  link; the session fixes it and opens a PR. Until this branch merges every scheduled run fails on `main`'s v11
  tests (state on 11 Oct 2026, run 12: `docs/crit/prd/LOG.md`, round 2). "In a public repository, scheduled
  workflows are automatically disabled when no repository activity has occurred in 60 days" (GitHub docs, "Events
  that trigger workflows"); a gate-failing run commits nothing (§6.1), so nine red Sundays with no other push stop
  the schedule silently, and whoever changes the cron to re-enable it "will become the `actor` associated with any
  workflow runs".
- **The agent-authorship switch.** `[facts] agent_clause` in `chart.toml`, read where `render_readme.py:459` calls
  `agent_clause(r)` unconditionally today, default `true`, with a test for both states: a session adds it the week
  Ben answers §9.0 (b), and his answer is then one line in `chart.toml`. Not a merge blocker (§8.1 item 7, §10.5).
- **The retired strings and modules** (§10.8): the first fix PR after the merge.
- After each run the sheet can lag the text for minutes to hours (§11). A sheet stale past a day is Ben's to purge:
  `curl -X PURGE` on the Camo URL in the page source, sparingly (GitHub docs, "About anonymized URLs": "Purging the
  cache forces every GitHub user to re-request the image").
- The GitHub constants in the checks (the 82 px mobile inset, the 846 px column, `<picture>` support; measured on
  the live page 10 Oct 2026) are re-measured by whoever opens the next round, and on any GitHub changelog that names
  Markdown images.
- The role line expires 2027-06 (EXPIRY-PASSED warns).
- No success metric is set; "done" is §8.3. One cheap one is available if he wants it: Rust-sitemap's Insights →
  Traffic referrers include the profile within 30 days of merge, read once by Ben and recorded, with its date, in
  `docs/crit/round6/LOG.md` under the round that merged.
- `chart.toml` copy is edited after merge by Ben, or by a session only inside a review round (§7.5).

### 8.6 The first merge

Owner: a session. The order is a fact about `publish_chart.py` and `profile.yml`, not about what the page says, so it
is not one of Ben's inputs (§9.0). The live `main` (`d253286`) names eight sheets on the `chart` branch: `hero-day`,
`hero-night`, `hero-phone-day`, `hero-phone-night` and four `hero-*-still-*` editions, the `still` ones under
`prefers-reduced-motion: reduce` at any width (`git show d253286:README.md`, lines 6–13; all eight are on `chart` at
`c488907`). This branch's README names the first four plus `hero-mid-day` and `hero-mid-night` and no `still`
(`README.md:7–13`; the renderer keeps the `still` rows only as comments, `render_readme.py:43–52`).
`publish_chart.py` force-pushes one orphan commit holding only what the build report names (its docstring, lines
2–14) and has no option to keep anything (`--dry-run`, `--branch`, `--remote`, `--report`, `--social`, `-m`; lines
155–160). A browser picks one `<source>` and does not move on when its file is missing: the HTML standard chooses
"one image source from sourceSet" and an image whose fetch yields no data is broken; MDN's `<img>` fallback is for
"no matches", not a failed load (sources in `docs/crit/prd/LOG.md`, round 5). So every order but C has a window in
which some readers of the live page get no image, which is 8 Oct 11:13 ("Merged but all images are unavailable")
planned in advance.

- **(C) Publish keeping the live sheets, then merge at any pace** (recommended; needs §10.23): the first publish
  stages the current `chart` tip's files first and the report's over them (`--keep-current` in `publish_chart.py`,
  one test that every path `main`'s README names is in the staged tree, `unshipped()` run against both READMEs), so
  no `<source>` on either README points at a missing file; Ben merges when he likes; the next weekly run republishes
  without the option and the four `still` and two old sheets go when nothing names them. The only window is §11's
  cache lag. Item 5 and §7.4's publish row then hold on the live page, not only on the merge commit.
- **(A) Publish, then merge within the hour** (only if §10.23 is skipped): for that hour every reader whose browser
  reports `prefers-reduced-motion: reduce` sees a broken image, because the `still` sources are gone.
- **(B) Merge, then let the job publish** (only if Ben says so): the merge touches `scripts/` (`git diff --stat
  origin/main..HEAD -- scripts`: 36 files; 38 with `chart.toml` and `.github`), so the push runs the job, which
  publishes before it commits (`profile.yml:142–153`); until then (minutes; longer under load, §6) every reader
  between 852 and 1,199 px sees a broken image, because the two `mid` sources do not exist yet.

Every order needs §8.1 item 2 green on the branch first, and under every order the sheet can lag the text for the
window §11 costs.

## 9. Open decisions and items

### 9.0 What only Ben does, in order

(a) `[position] text` and one of `[contact] linkedin` / `resume` in `chart.toml` (§8.1 item 6; all three are `""`
today, `chart.toml:26, 30–31`; the shape is in `docs/BEN-TODO.md`: "role · city or timezone · open to / currently").
Not needed for the merge: the slot prints on the first build after he sets them. (b) One word against §9.2's
first decision, strike, keep or share, said in a session (the session records it verbatim in `owner-messages.md`
and as one line in `docs/crit/prd/LOG.md`); until he says one, the clause prints as it does today (§9.2; the switch
that makes his answer one line in `chart.toml` is §8.5). (c) One word, yes or no, to merging 2b (§9.1): the list
under the image goes from six open items to four and the rest fold; the image does not change (only a release
changes it, rows 1a and 1b). Compare `renders/round-16/page-phone-2.png` with `renders/once-2b/page-phone-2.png`
(the phone), and `renders/round-16/page-desk-1.png` with `renders/once-2b/page-desk-1.png` (the web, the reader his
words make likelier, §2). A yes means a session opens the PR (§10.17), sets the two `fold = true` lines (§10.19),
publishes (§8.6, order C once §10.23 exists), the product round judges the PR's build (§8.3, Done), and he merges;
the order is the session's, not his. This is the one input the merge waits on, and his yes approves this document
(header). (d) The device check (§8.4): on the live page in the first week after the merge, the screenshots sent in a
session. (e) The printed name, `rustmapper` or `Rust-sitemap` (§9.2, second bullet): not needed for the merge;
`rustmapper` stands until he says otherwise. Everything else is a session's, and a session acts only while Ben has
one open: every owner in §8 and §10 that reads "a session" or "next session" is work he starts; until he does, those
rows do not move and §8.5's failed run has no one. The 1a-against-1b choice comes after a release and is not needed
for the merge; §9.1b's default stands until he says otherwise.

### 9.1 The decisions: what the page says about rustmapper 0.1.3, now and after a release

A merge reaches rows 0, 2b and 3 (the list under the image); a release reaches rows 1a and 1b (the image and the
box). Only row 2b is decided now (§9.0 (c)); 1a against 1b is what a release does later. Today the image's box and
the page's "Before you run 0.1.3" list state six measured faults of the released tool (L1, L7, L4, L6, L2, L5 on the
open list; H0 and H1 in the box). Every one is true, probed and gated. Together they read as a warning label on his
flagship. His test is 9 Oct 20:50, *"is it accomplishing my goal? Not just what I'm saying"*, so each option below
says what the first phone screen and the first desk render read, not only which probes pass: the phone is the
stricter constraint, the web the likelier reader (§2), and on the web the whole list sits beside the image's column.
The 1a and 2b outcomes are rendered (below); the 1b render waits on §10.9.

**What is live while this is undecided** (checked 11 Oct 2026 by REST and on the `chart` branch): `main` at `d253286`
serves the v11 sheet from `chart` `c488907` (groups `hero-row0`, `hero-row1`, …), alt *"Ben Russell's 22 repositories
by week, Sep 2025 to Oct 2026: Scrapy and rustmapper busiest, quiet Feb to Apr 2026. The rest share one row."*; facts
lines with *"last commit 8 Aug 2026"*; a first-person footer (*"my commits … regenerated weekly"*); and the thesis
line he cut on 9 Oct 19:39, pending PR #17. That is the map he rejected on 9 Oct 20:50 (*"tiny fucking islands … Is
it based on the size of the project or how many commits?"*), and its weekly job failed on 11 Oct (§8.5).

| Option | First phone screen (390 px) | First desk render (1,280 × 1,700 px, `page-desk-1.png`) | What the page's list becomes | Cost, and who | What the pipeline does |
|---|---|---|---|---|---|
| **0. Leave `main` as it is** (what happens while nothing is decided) | the v11 sheet: "22 repositories by week … busiest, quiet Feb to Apr 2026"; "last commit 8 Aug 2026"; "my commits"; "regenerated weekly"; the thesis line | not rendered; `git show d253286:README.md` puts the same sheet, the link line, the sentence and four rustmapper bullets with "last commit 8 Aug 2026" under it | the v11 page: an activity sheet with repositories as rows, first person, a schedule line | no work; every week undecided keeps up a page that breaks G8, G13, G14, G15, §7.3 and §7.5. The costliest row in what strangers see | nothing; the next scheduled run fails on the v11 tests again |
| **1a. Minimum 0.1.4** (the floor; the step after 2b) | name; role; rustmapper, one sentence; `pip install rustmapper` 0.1.4 · its date; `rustmapper crawl` (one name) starts from your URL; fetches up to 20 pages; **Ctrl-C once stops early**, once §10.9's C1 wording exists (§5.4 row 1); `data/sitemap.jsonl`; sorted 21 ways. **No box.** | `renders/once-1a/page-desk-1.png`: the sheet without the box, the link line, the sentence, the pick, the facts line, the platform note, five cautions, the fold line and a code block with no stop-rule comments; Scrapy's first line follows | five items (L1, L7, L4 without its https clause, L2, L5) | §5.4 rows 1, 2 and 6: exit when idle (the test is at HEAD), robots 404/scheme/fail-closed (not at HEAD), `[project.scripts]` (not at HEAD); a release. Ben, or a session with push access to `Rust-sitemap`. Here first: the C1 wording (§10.9). | H1, the gap, H0, L6 and L4's clause retire at the next weekly run; `release-published` rebuilds at once |
| **1b. Full 0.1.4** (the end state) | as 1a, plus S2 "one queue per host, paced by that host's robots.txt" in the loop and W1 if its switch is lifted | not rendered (§10.9 first) | three items (L1 reworded, L2, L5), each a default rather than a fault; the fold keeps the file notes | 1a plus §5.4 rows 3, 4, 5, 7, 8; two of the eight are at HEAD already (exit test, Crawl-delay parser). **Plus, here first:** the `crawl_delay_obeyed` probe, the L7 and `noindex` fallbacks, W1's switch (§10.9); without them the first build after the release fails on L1/L4/L7 | every caution retires on its own only once §10.9 is done |
| 2. Keep the route, move the cautions to rustmapper's README | as today, with the box | not rendered | one line linking the project's own "Known issues" | the image still draws H0/H1, because they are true of the release the image names; a "Known issues" section in Rust-sitemap; a gate here that the linked section exists | `[route.rustmapper]` items marked off-page |
| **2b. Keep the image and its box; cut the open list to what explains the first screen** (recommended now; rendered, below) | as today, with the box, and `0.1.3 · 8 NOV 2025` (eleven months old at the merge, older each week) over `rust_sitemap crawl` (the wheel's command; the image says `rustmapper` two lines up). Only a release changes either (§5.4 row 6; §11) | `renders/once-2b/page-desk-1.png`: the sheet, the link line, the sentence, the pick, the facts line, the platform note, **four** cautions (each a mark's text or its lever), the fold line and the code block | four items, by rule: open every item that is the text of a mark on the first screen or carries its lever; fold the rest. Today that is L1 (no pause, 256 workers; `--workers 1`), L7 (no contact in the UA; `--user-agent`), L6 (the sign of H0's stall, `blocked by robots.txt`) and L2 (S1's lever, `--seeding-strategy none`); L4 and L5 fold under the existing `<details>`. Four is under the "few" the hiring-side sources set, and the two-sided-message meta-analyses say an admitted fault persuades only with its refutation beside it, and a fold is not beside (sources in `docs/crit/prd/LOG.md`, rounds 1–4). The first cut of 2b, L1 and L7 open, folded the text of two marks drawn on screen one (S1's lever, H0's sign) against G6; its render is kept as `once-2b-r3` | no work in Rust-sitemap; here, one change (§10.19): L4 and L5 get `fold = true` in `chart.toml` (two lines). The fold then holds six (L4, L5, L3, X3, X2, X1), under `render_readme.LIST_MAX_ITEMS = 7`, which `cautions()` (`checks/readme.py:121`) applies to the open list and the fold alike; `cautions()` on the 2b page: nothing. No cap moves and round 13's "7 for each" ruling stands. A session, before the merge; his yes to 2b covers it (§9.0 (c)) | retires the same way as 3: H1, the gap, H0, L6 and L4's clause go on the next weekly run after a release |
| 3. Ship as is | as 2b: the box, the date and the two names; the six items begin on the second screen (`renders/round-16/page-phone-2.png`: three of them) | `renders/round-16/page-desk-1.png`: as 2b with **six** cautions, two of them (L4, L5) explaining nothing on the image, the whole list under the facts line beside the image's column | six items | a visitor's first read of his main tool is its fault list, whole on the first desk render | nothing |

**The rows are not alternatives.** 1a/1b and 2b/3 are steps, not a menu: merging now (2b or 3) and releasing 0.1.4
later gives 1a or 1b by itself, because some of §5.4's rows retire on `release-published` or at the next weekly run
with no edit here, and the rest need §10.9, which is work in this repository, not in Rust-sitemap. Merging first
costs nothing a release would not undo on its own, and 0 → 2b is reversible (`git revert` of the merge commit on
`main`; §6.1). Two first-screen facts make the release worth cutting soon whatever the cautions do: the date beside
the install line and the two names for one tool; a merge changes neither, a release changes both. So the decision is
sequenced:

- **Recommended:** **merge 2b now**, then decide 1a against 1b with the renders in hand. **If nothing is decided:**
  row 0, every week. 3 is not the better immediate merge: the hiring-side sources want a fault list short, after
  the positive, and each item with its fix, and 2b is the only row that gets there without Rust work; 3 puts six
  items, two unfixed, on the second phone screen and all six on the first desk render beside the image.
- **Decide by:** 2b before the merge (one change here, §10.19; §10.23 first, §8.6). 1a against 1b before the
  release is cut. A push to `main` that touches scripts or `chart.toml` triggers a build, so the merge is the first
  weekly run.
- **Size:** 1a is three fixes in Rust-sitemap, one with its test already at HEAD; 1b is eight fixes plus the four
  items here. In days this is Ben's estimate to make; the repository cannot measure it, and this document prints no
  figure it did not measure.
- **The 1a render**, `docs/crit/prd/renders/once-1a/` (sheet, first two phone screens, first desk screen, fixture,
  page text). Beside round-16's: **no box and no gap in the track** (H0, H1, L6 and M1 resolve to `""`; G1a's second
  mark goes with the fault it marked), the loop closing on the fetch row, `rustmapper crawl` on the first line of
  the route, L4 without its https clause, the open list five items (L1, L7, L4, L2, L5); the phone sheet 982 units
  tall against 1,121. The version line still reads "0.1.3 · 8 NOV 2025" and the Ctrl-C row is unchanged (§5.4 row
  1). Fixture and gate notes: `docs/crit/prd/LOG.md`, round 2. The 1b render needs §10.9 first.
- **The 2b render**, `docs/crit/prd/renders/once-2b/` (`stats-once-2b.json`, `README-2b.md`, three phone screens,
  the first desk screen; the image is round-16's, unchanged). Beside round-16's: the second phone screen
  (`page-phone-2.png`) ends "Before you run 0.1.3:" with L1 (`--workers 1`), L7 (`--user-agent`) and L6 ending in its
  sign, `blocked by robots.txt`; the third opens with L2 (`--seeding-strategy none`), the closed fold and the code
  block; the 390 px page is 5,429 CSS px against 5,645. The first cut (L1 and L7 open; the fold at eight) is kept at
  `renders/once-2b-r3/`. Fixture, gate and tool notes: `docs/crit/prd/LOG.md`, round 4.

### 9.1b The second decision: the mid window, 852–930 px

Between 852 and 930 px the mid sheet's 19-unit text is 11.2 to 13.0 px, under the 13 px floor a phone gets
(`column.py`: `MIN_PX = 11.0`, line 45; `column_px(852)` = 482 px, lines 56–63; the mid sheet starts at `mid_from_px
= 852`, `chart.toml:13`). No device he named sits in that window; a 1,024 px iPad held sideways gets 13.7 px. This is
the one home of the trade; §5.2, §7.4, §10.14 and §11 point here.

| Option | What the 852–930 px reader sees | Cost, and who | Default |
|---|---|---|---|
| **a. Accept 11.2–13 px in writing** (recommended) | the mid sheet as today, 11.2 px at 852 | none; written here and in §11 | yes |
| b. Serve the phone sheet to 930 (`mid_from_px = 931`) | the phone sheet in a 482–560 px column, its 26-unit text about 21–24 px | one number and six `<source>` lines regenerate; **but HERO-COLUMN-PX fails at 852 as the gate stands**: the phone sheet is 1.868 × its column (1,121 / 600 units), 900.5 px at 482 px, over `TALL_PX = 900` by half a pixel, so b also needs the sheet 1 unit shorter or the gate moved; a session | no |
| c. A narrower mid sheet | smaller type on every mid reader, 852–1,199 | a redesign of one edition, a build and a review round; a session | no |

Decides: Ben (9 Oct 11:32: *"accepting of all different formats"*). Until he does, a stands.

### 9.2 Owner's calls carried in `docs/BEN-TODO.md`

- **The agent-authorship clause on the facts lines** ("coding agents (Claude) authored 45 of its 146 commits and
  co-signed 1 of his own 101", `README.md:38`; Scrapy's "71 of its 499 … 30 of his own 420", `:86`). This bullet is
  the one home of the decision; G8, §5.3 row 5, §7.3, §8.1 item 7, §8.5, §9.0 (b) and §10.5 point here. He said
  both: 9 Oct 11:35 (*"We don't need to show the commits are kind of cool. The data is kind of cool that we're
  pulling, but at the same time, it feels lazy, and I don't really like that"*) reads against showing commit
  figures; 9 Oct 11:37 (*"Talking about my commits. Talking about my work. That is what this should all be about"*)
  says the page should talk about his commits and his work. Read as he said it, 11:35 is about the v8 picture that
  *showed* the commits and called that picture lazy; the line in question is a disclosure of who wrote the code,
  which he has never named in any message (`docs/BEN-TODO.md:16` has asked him, "Strike it if you'd rather not",
  unanswered). Options: **strike**, **keep** (11:37; an honest fact a hiring engineer asks, Q3), **share without
  totals** ("about a third of its commits were written by coding agents", no numbers, in the provenance line which
  already says who is counted). **Recommended: keep, as printed** (the tool named, the counts measured, his own
  commits counted apart, §7.3; the 2026 hiring-side evidence for it, and its cost, the reader's distrust of AI
  output, are quoted in `docs/crit/prd/LOG.md`, round 5). **Decides:** Ben, one word in a session (§9.0 (b)).
  **Until he does:** the clause prints as today, with no switch. **Implementation either way:** the `[facts]
  agent_clause` switch, default on, added after the merge (§8.5, §10.5), so his answer is one line in `chart.toml`.
  Rounds 1 and 2 ruled strike and round 5 keep, all on the owner lens; the reversal is the sign that the text has
  settled what it can, and the rest is his word.
- **The printed name.** Options: `rustmapper` (the PyPI name and what a reader types; printed today through the
  alias in `chart.toml`; recommended, since the first screen is the install line) or `Rust-sitemap` (the repository,
  linked from the image and the link line either way). **Decides:** Ben; one line in `chart.toml` (§9.0 (e)).
  **Until he does:** `rustmapper` stands (it is what prints). **Decide by:** before a release that adds
  `[project.scripts]`, when the two names on the first screen become one (§11).
- **Work in his other repositories that would change a clause here**, not decisions about this page: the rustmapper
  README's worker figure (code 256–1,024, README 32–512, PyPI 256; the page prints the code's 256 on L1 either way)
  is `docs/BEN-TODO.md`'s first round-5 ask; Scrapy's stage-2 robots check, delay and user agent (the pick's
  politeness clause then prints by itself, §5.3 row 4) and its near-duplicate filter across passes are not yet in
  `BEN-TODO.md`, and the next fix round adds that line, in the same edit that strikes the overtaken round-4 third ask
  (`docs/BEN-TODO.md:34–36`, the three concept stills; §10.10 carries the companion line).

### 9.3 Not yet verified or produced

- The iPhone and GitHub-app check (§8.4; after the merge).
- The `workflow_dispatch` dry run on the branch (the macOS run check installs the prebuilt wheel, so the install
  note will read differently from the Linux run that produced today's `stats.json`; the https probes depend on
  `sudo -n security add-trusted-cert` on macos-14 and may be skipped, which the gate reports as a warning).
- A real iPad at 852–1,199 px. His call on the mid window is §9.1b (default a: accept in writing).
- The 1b render: a fixture `stats.json` with `ends_by_itself`, `robots_read`, `robots_late` passing and
  `robots_stall`, `ua_seen`, `sitemap_keeps_disallowed`, `kill_writes_file` failing, with `edition.scripts` set; it
  needs §10.9 first. The 1a and 2b renders exist (§9.1).

## 10. Gaps this review found

Rules held only by a reviewer's eye, or by nothing, with the proposed fix. One row each, ids stable (other sections
cite them); which round added or closed each is in `docs/crit/prd/LOG.md`. **Rule:** a row that blocks the merge is
also a line in §8.1; a row that closes keeps its id in the line under the table and its reasoning moves to the log.
**Rank:** *must* (before the merge, or where the cell says), *should* (before the next rustmapper release), *nice*
(when a session has nothing ranked above it). Owner: Ben, or the next session (§9.0: a session acts only while Ben
has one open).

| # | Gap | Fix (file) | Rank | Owner | Status |
|---|---|---|---|---|---|
| 1 | Theme words in README prose (G2): `theme_words` runs over the image, the alt and DESIGN.md, not `README.md`'s visible prose | add it to `checks/readme.py` with an allow-list for project facts ("Helm chart", "CT logs", "logged"); one function, one test. Until then §8.3 q.1 carries the grep | nice | next session | open |
| 4 | The device check (G4) has not been done | §8.4, once, on the live page; Ben sends the screenshots, a session writes the entry with their paths | must: the first week after the merge, not the merge | Ben (the look); next session (the entry) | open |
| 5 | Commit counts on the facts lines (G8): the agent-authorship clause prints with no switch (`render_readme.py:459`; `[facts]`, `chart.toml:667`, has no key); the decision's one home is §9.2 | `[facts] agent_clause = true` in `chart.toml`, read at `render_readme.py:459`, a test for both states (§8.5) | nice: after the merge, the week he answers §9.0 (b); its default reproduces today's page | next session | open |
| 7 | A fresh clone's gate fails: the committed `assets/build-report.json` is the 8 Oct report (`9e25619`) of 38 retired sheets; `check.py` reads it by default (`check.py:202`), so on the tree as committed `check.py --tier fast` gives 4,599 fails (XML-SIZE "viewBox 600×1121 but report says 720×900", then TYPE on sheets that no longer exist) and passes only after `build_assets.py` rewrites it; the weekly job dirties the file and never commits it (`profile.yml:160` adds five files; the comment at `:168` says so) and uploads it as a run artefact instead (`:133`). `assets/v9` is gitignored and was never the cause | commit a fresh report on this branch and add `assets/build-report.json` to the loop at `profile.yml:160`, or gitignore it and have `check.py` fail with one clear message when it is absent; until then §8.1 item 2 builds first | should: until then a fresh clone's gate fails | next session | open |
| 8 | Theme strings and retired modules in the public repository (G2, G11): `chart.toml:35–39` (`unit_chart = "SOUNDINGS IN COMMIT-DAYS"`, `unit_hero`, `unit_approaches`, `limit_label`, `footer_line = "The chart ends here. The web doesn't."`), read only by `scripts/sheets/soundings.py`, `approaches.py`, `footer.py` (`build_assets.ALL_SHEETS`, not `SHEETS = ["hero"]`) | delete the five keys; the `soundings`, `approaches`, `footer`, `log`, `instruments` modules with their tests; `tests/test_chartlib.py` (22) and the `chartlib` functions the route does not call (it calls `stroke` only: `grep chartlib. scripts/sheets/route.py`); the `log.shards` warning; extend `theme_words` to `[copy]` values (§7.1 open row). 91 tests go (§6) | nice: the first fix PR after the merge; no live sheet reads them and 8 Oct 14:52 is about what the user is shown | next session | open |
| 9 | Three of §5.4's rows fail the build instead of retiring, and one retires its box and leaves a wrong step (G7; verified by running the resolver and by the 1a render) | probe `crawl_delay_obeyed` in `runcheck.py` (a fixture robots.txt with `Crawl-delay: 2`, two requests to one host ≥ 2 s apart); an `instead` on L7 with `fails = ["ua_seen"]`, `text = ""`; a wording on X1 for a release that drops `noindex`; W1: a wording that holds on a passing `kill_writes_file` and the switch lifted, or leave W1 undrawn and say so in §5.1 for good; **C1**: give the first wording `fails = ["ends_by_itself"]` beside its `runs`, and add a wording held by `runs = ["ends_by_itself", "crawl_ctrl_c", "second_ctrl_c"]`, "stops when the queue drains and writes the file; Ctrl-C once stops early and still writes it; a second press quits without" (the `second_ctrl_c` anchors as today; 9 Oct 11:37, "It has to be helpful knowledge"). Then each §5.4 row is a resolver fixture (item 12) | should: a fixed release fails the build until then; the C1 wording before 1a, the rest before 1b | next session | open |
| 10 | The thesis line is banned nowhere (G14; 9 Oct 19:39) | "wrong about itself" into `strings.py BANNED` (it scans `README.md`, `chart.toml`, the SVGs, the report); strike `docs/BEN-TODO.md:39` (round-4 item 1 still tells him to put it in his bio) and, in the same edit, `BEN-TODO.md:34–36` and the Scrapy line §9.2 names | nice | next session (BANNED, the `BEN-TODO.md` edit); Ben (what the file asks) | open |
| 11 | T-PURPOSE and ROUTE-PURPOSE are narrower than their rows (G9, G16) | in `test_every_element_has_a_purpose`, assert what is inside each non-text group (only `rect`, `circle`, `line`, `path` with straight segments; no `use`, `symbol`, `polygon`, `image`), so "no ships" has a test; derive the excused set from `data.route` (`drawn = false`, `waits`) instead of `{S2, W1}` | nice | next session | open |
| 12 | The PRD has no test; its register is checked by hand (§0) | `tests/test_prd.py`: every `[A-Z]+(-[A-Z]+)+` token in §7 and appendix B is emitted by `scripts/checks/*.py` and every emitted code is in appendix B; each tier equals the plug-in's `TIER`; §6's counts match (`ls scripts/checks`, the runner's total, `len(steps)` and the gate/probe split); §8.2's codes equal the warn set on a fresh build; §5.1's IDs and Q's equal `PURPOSE`; each §5.4 row is a resolver fixture; every `file:line` cite points at the symbol named beside it; each code's level (`fail` / `warn` / `info` / `error`) as emitted equals the status its §7 row states; **the reverse direction:** every `tests/*.py` function whose trailing comment names a code or a T-id is cited in that code's row (round 6 found eight that were not, and a §10 gap a test had closed); appendix B is written by the test from `scripts/checks/*.py`, `check.py` and the test loader, and the test fails when the committed appendix differs (the AUDIT-STALE / `cargo rdme --check` pattern) | nice: it blocked "the next PRD round" once and round 4 ran without it; the register stays hand-checked each round until it exists (the commands: `docs/crit/prd/LOG.md`, rounds 4 to 6) | next session | open |
| 15 | Languages order: `test_order` (`tests/test_round7.py:105`) pins the rest by repository count and drops a lead language no repository has; nothing pins the tie-breaks in `languages_line` (`render_readme.py:162`, key `(-count, -lines, name)`: equal counts by lines, then by name) | one assertion over a fixture with two equal counts | nice | next session | open |
| 16 | The code block's comment lines wrap at the phone's 32 columns on the desk (`page-desk-1.png`) | a ≤ 32-column wording of the stop rule if one exists ("# runs until stopped; Ctrl-C once" is 33), edited in `chart.toml` and in `test_install_block_says_how_it_ends` (`tests/test_route.py:443`), which pins the block's lines; otherwise the trade stands (§11) | nice | next session | open |
| 17 | This branch has no PR (§7.6 "not met today"; 8 Oct 09:04) | the branch is on `origin` at `9e3db34` with every product file (`git ls-remote --heads origin v12/purpose`; the five commits after it are docs only); `gh pr create --head v12/purpose` needs no push (`gh api …/pulls?state=all&head=BenjaminSRussell:v12/purpose`: 0 on 11 Oct 2026); the fix round opens it first, before any code change, so the PR is where §10.19 and §10.23 land | must: the merge (§8.1 item 9) | next session | open |
| 18 | `resume_after_kill` runs every week and is read by nothing (§6; `chart.toml:900` is a comment); `runcheck.py:8` says "probes four behaviours" of 18 | name the probe from W1's future wording (item 9) or drop it; fix the docstring | nice | next session | open |
| 19 | Option 2b needs one change here: the entries that fold are marked `fold = true` in `chart.toml` (read by `render_readme.text_blocks` from `stats.json`'s routes), and `render_readme.LIST_MAX_ITEMS = 7` caps the open list and the fold alike (`checks/readme.py:121` `cautions()`) | mark L4 and L5 `fold = true` (two lines, after `short` as L3's at `chart.toml:1257`); the fold then holds six (L3, X3, X2, X1 today plus the two), under the cap of 7; verified on the 2b render (`cautions()`: nothing). No cap moves; round 13's "7 for each" ruling (`render_readme.py:670`) stands. The first cut of 2b (L4, L6, L2, L5 folded) needed the fold's cap at 8 and is withdrawn (§9.1) | must: the merge under 2b (§8.1 item 10) | next session; his yes to 2b (§9.0 (c)) | open |
| 21 | §8.1 item 6b (one contact beyond Email) is held by no gate: `checks/position.py:32–35` reads `[contact]` only for ⟨ ⟩ placeholders, so POSITION-EMPTY silent does not mean a contact is set | CONTACT-EMPTY (warn) when both `[contact] linkedin` and `resume` are `""`: one `elif` in `position.py`, one test; until then §8.3 q.4's link-line tick | nice | next session | open |
| 22 | `profile.yml`'s commit step pushes `HEAD:main` from whatever ref a `workflow_dispatch` ran on (`actions/checkout@v4` with no `ref`, `:72–74`; `git push origin HEAD:main`, `:174`), so a dispatch with `dry_run` false on a branch merges that branch by the bot's hand, against appendix D's first rule | guard the publish and commit steps with `github.ref == 'refs/heads/main'` (two `if:` lines) and say so in the `dry_run` description; until then §8.1 item 4 permits only the dry run on a branch | should: a hazard, not a note; item 4 carries the rule until then | next session | open |
| 23 | The first publish removes the four `still` sheets the live `main` names and, under order B, the v12 README names two `mid` sheets before they exist, so every order but C has a window in which some readers get a broken image (§8.6; 8 Oct 11:13). `publish_chart.py` ships only what the report names and has no keep option (docstring 2–14; argparse 155–160) | `--keep-current` in `publish_chart.py`: stage the current `chart` tip's files first, then the report's over them, the commit still parentless; one test that every path `main:README.md` names is in the staged tree; `unshipped()` (`:81`) run against both READMEs. The next weekly run republishes without it | must: the merge (§8.6, order C; §8.1 item 9) | next session | open |
| 24 | The alt-poem clause of §7.5 is held by a warning only: `alt.py:50` emits `warn("ALT-POEM", …)` and no product test reads `[alt] alt_poem` (`test_pipeline.py:553` checks its length) | `warn` → `fail` at `alt.py:50` and one assertion in T-ALT (`tests/test_route.py:832`) that the alt's last sentence equals the poem's hero line | nice | next session | open |

Closed (the reasoning is in `docs/crit/prd/LOG.md`): **2**, "not too on the nose" has no count, kept in review (§7.1,
§8.3 q.4); **3**, even density has no metric, kept in review (§8.3 q.3); **6**, "Generated" survives in two
maintainer comments a visitor never sees; **13**, a failed fetch's mark is the provenance line's date (§6.1 row 1);
**14**, the mid window's floor is a decision (§9.1b); **20**, the sheet's lag after a run is accepted (§11).

## 11. Risks

- **Reading as a flowchart.** With the manner carried only by the track, the dots and the paper, a visitor may see a
  flowchart. The answer is drawing, never added symbols (DECISIONS, concept A risk 1). Every review is asked §8.3
  q.6, so the reading is sought, not merely not raised (rounds 13 and 16 did not raise it unasked).
- **The desk pays for the phone's code width.** In his words the web is the likelier reader (9 Oct 11:32); Markdown
  serves one code block to both, so the desk column (846 px, `renders/round-16/page-desk-1.png`) shows the three stop-rule comment
  lines wrapped at the phone's 32 columns with two thirds of the column empty. Accepted for now; §10.16 names the
  one-line fix if a wording exists.
- **The mid window, 852–930 px.** §9.1b; option a stands.
- **The sheet can lag the text after each run.** The `<picture>` sources are
  `raw.githubusercontent.com/…/chart/assets/v9/hero-*.svg` (`README.md` lines 7–13) and `publish_chart.py`
  force-pushes new sheets to the same paths. raw.githubusercontent.com caches for 300 s (GitHub staff in community
  discussion #46691: "The cache is set for 5 minutes"; `max-age=86400` seen on some files, hours reported in some
  regions; FLUID-6626: "a varnish cache that does not allow updates more frequently than every 300 seconds"), and
  GitHub serves Markdown images through Camo, which caches on top (GitHub docs, "About anonymized URLs"). So for
  minutes, sometimes longer, a visitor can see the new README with last week's sheet: the week H1 retires, the list
  drops the stop-rule while the image still shows the box. Accepted: both states are true of the release, and round
  15's publish-before-commit rule covers a missing sheet, not a stale one (8 Oct 11:13 was the same class of
  surprise). If it must be shorter: name the sheets by run (`hero-day-<date>.svg`) so the README's new URLs miss the
  cache; one line in `publish_chart.py`, one in `render_readme.py`, and HERO-FALLBACK's path check (§10.20). A sheet
  stale past a day is purged by Ben (§8.5). The first merge's own window is costed in §8.6.
- **The weekly run check on macOS differs from the Linux run** that produced today's stats; wordings may shift on
  the first CI build (the install note, probe skips). The gate reports it; nothing false can print.
- **A 0.1.4 cut from HEAD as it stands removes the command line** (`bindings = "pyo3"`, no `[project.scripts]`,
  `pyproject.toml:55` at `32c2651`): `edition.scripts` would be empty and the build would refuse to draw the
  entrance. Fix the packaging before cutting the release (§9.1, 1a). Until then the first screen names the tool
  twice (`rustmapper` on the install line, `rust_sitemap crawl` on the next row) and dates it 8 Nov 2025.
- **A 0.1.4 that fixes the User-Agent or parses Crawl-delay fails the build here** until §10.9 is done. The failure
  is loud (ROUTE-UNVERIFIED, exit 1, nothing published), not false.
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
| `check.py` (the runner, outside `scripts/checks/` and the §7 grep) | — | PLUGIN-RESULT (`check.py:115`), PLUGIN-IMPORT (`:246`), PLUGIN-CRASH (`:254`), NO-SHEETS (`:286`), NO-REPORT (`:288`): all `error`, exit 3 (§6.1) |
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
| log | fast | `log.load`, `log.schema`, `log.rule` (fail), `log.version`, `log.shards` (warn), `log.computed` (info): live on `assets/log.json` (the workflow commits it, `profile.yml:160`); warns `log.shards` on every build (§8.2; round-16 `gate.txt`: "fast log 2 finding(s)"); rule in §7.3; goes with the retired `log` sheet (§10.8). `"log.json"` at `log.py:36` is a file name, not a code |
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

## Appendix D. How the work was done, by his instruction

These rows bind the process, not the page: none has a gate, a test or a line in §8. Their ids (G17–G19) and the
§7.6 row texts are unchanged so every cite resolves here.

| # | His words (date) | What it means here | Held by |
|---|---|---|---|
| G17 | "at least 10 reviews of, is it matching what I'm saying? Is it doing what I'm saying? Is it accomplishing my goal?" (9 Oct); "review every single detail I want so much attention to detail" (7 Oct 16:12); "Merged check and this needs higher reviews" (8 Oct 16:38); "run all agent judgment for a second round and review and implementation" (8 Oct 23:24) | reviews that open with his goal, not with taste; those three questions are §8.3 q.1–4 | 16 rounds; each review's first section is "does it meet the owner's goal" |
| G18 | "Do research on every single round... dozens of sources, hundreds of sources" (9 Oct) | research files per round; each review cites sources | R1–R7 (360); reviews cite 31 to 59 per round |
| G19 | "Use multiple agents and review and check and review and check" (9 Oct); "30 different perspectives from 30 different agents... then 10 teachincal agents" (7 Oct 17:58); "the different ages, different opinions... Where's the fucking opinions there?" (9 Oct 11:35); "Review and ensure this is something I want to see rounds of reviews and research" (11 Oct) | independent reviewers of distinct standpoints who do not see each other's drafts; a fix round between; the PRD itself is reviewed the same way. The 11 Oct sentence is cited for "ensure this is something I want": its object is the page, and the rounds are the means. The count comes from 9 Oct 20:50 ("at least 10 reviews"), met by the 16 product rounds; the PRD rounds stop at the merge (§0's stop rule), and round 6 ran against round 5's version of it (the last row of the table below) | the Workflow runs; `docs/crit/panel30/`, `tech/`; `docs/crit/round6/review-rNN-{1,2,3}.md`; `docs/crit/prd/review-rNN-{1,2,3}.md` |

The process rules of §7.6:

| Rule | Status | Where |
|---|---|---|
| Never push to `main`; the owner merges PRs | process | every change is on a branch; the weekly bot commit to `main` is the workflow's own, by his design; §6.1's rollback is a PR for the same reason, and a non-dry `workflow_dispatch` on a branch would break the rule by the bot's hand (§8.1 item 4, §10.22) |
| Every open PR is mergeable and without conflicts; a branch is opened as a PR before a round ends (8 Oct 09:04: "Resolve all merge conflicts and all PRs need to be ready to merge") | process, **not met today** | PR #17 is open (`gh api`: `state: open`, `mergeable: true`, head `v11.1/no-thesis`); this branch has none, though it has been on `origin` since before PRD round 1 (§10.17: `gh pr create` needs no push) |
| Commit messages end with the Co-Authored-By and Claude-Session trailers | process | `git log` shows them; the model name in the trailer follows the serving model |
| No "Generated by Claude Code" footer in PR bodies or comments; the server appends its own | process | his instruction of 8 Oct |
| The stop hook: commit and push before stopping | process (session; not verifiable from the repository) | WIP commits when it fires |
| His email is used only to identify him; the page's `mailto:` is the one he set | process | it is not on the page beyond that link |
| At least 10 reviews, each against his words; research every round; multiple agents | process, done | 16 rounds × 3 reviewers; Workflow `wf_eee12105-794` (session; not in the repository); `LOG.md` |
| Report failures as they are | process | the ship verdict was never reached, and is reported so |
| Asks that only he can do go in `docs/BEN-TODO.md` | process | position, contact, LICENSE, the worker figure, the name |
| Three independent reviewers per round, each opening with "does it meet the owner's goal", each re-measuring every printed figure, each citing sources; a fix round applies or declines each must-fix with a reason in `LOG.md` | process | `docs/crit/round6/LOG.md`, `docs/crit/prd/LOG.md` |
| No PRD round before the fix round (§0; round 5's rule, with §8.1 items 7 and 8, §10.19, §10.23 and the PR in front) | process, **not met**: round 6 ran on 11 Oct 2026 with `git diff --stat 027f081..HEAD -- . ':!docs'` empty and no PR; the fix round is overdue by one round | §0's stop rule as round 6 rewrote it; `docs/crit/prd/LOG.md`, round 6 |
