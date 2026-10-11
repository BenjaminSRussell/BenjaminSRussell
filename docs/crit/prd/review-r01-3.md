# PRD review round 1, reviewer 3: An engineer who trusts nothing the PRD says until the code says it too

11 Oct 2026. Branch `v12/purpose`, worktree `/home/user/wt-v12`, HEAD `9e3db34` (the PRD's own commit, one past the
`027f081` the PRD names). I read `docs/PRD.md` end to end, then opened every file a row of section 7 or appendix B
names: the 28 plug-ins under `scripts/checks/`, `scripts/check.py`, `scripts/runcheck.py`, `scripts/data/route.py`,
`scripts/sheets/route.py`, `scripts/render_readme.py`, `chart.toml` (the whole `[route.rustmapper]` tree),
`assets/stats.json`, `.github/workflows/profile.yml`, `tests/test_route.py`, `test_pipeline.py`, `test_data.py`,
`test_round6.py` to `test_round16.py`, `test_proof.py`, `docs/crit/round6/SPEC.md` §6–7, `DECISIONS.md`, `LOG.md`
round 16, `docs/BEN-TODO.md`, `docs/crit/prd/owner-messages.md`, and the round-16 renders and `gate.txt`. I ran
`python3 -m unittest` (539 tests, OK, 22.4 s), counted the plug-ins and the run-check steps, and ran the real
resolver (`scripts/data/route.py resolve()`) against four of the release scenarios section 5.4 describes. There is no
`docs/crit/prd/LOG.md` and this is round 1, so nothing below can be a repeat of a fixed finding; where reviewer 1 of
this round found the same thing I say so and do not rank it.

**Verdict on the PRD: 6 / 10.** Its register is better than most: every one of the finding codes it cites (167 distinct codes are emitted under `scripts/checks/`)
exists in `scripts/checks/`, every tier in appendix B is the plug-in's `TIER`, the three counts in section 6 are
right, section 8.2's four warnings are exactly the gate's four, and section 5.1's seventeen IDs and their Q's are
exactly `PURPOSE`'s. What fails is the predicate, not the pointer: in five places the PRD says a gate or test holds
something it does not, and its headline claim, that the cautions "retire by themselves when a release fixes them",
is false for three of the eight rows of section 5.4, which I confirmed by running the resolver rather than by
reading. A PRD whose register is this precise should be tested like code, and it is not.

---

## 1. Is the product this PRD defines what he wants?

**Yes.** The sentence that decides it is from 9 Oct 20:50: *"My goal is to have a purpose behind each map. Every
single fucking map needs a deep purpose. Every single, not even just maps. Everything, single thing inside of this
needs a purpose, not a fucking chasing a reason."* Section 5.1 is that sentence made into a table: seventeen IDs,
each with what a stranger learns, which question it answers, where the words come from and when it may be drawn,
and I confirmed the seventeen are exactly the keys of `scripts/sheets/route.py` `PURPOSE` (lines 74–124), with
the same Q for every one, and that `test_every_element_has_a_purpose` (`tests/test_route.py:812`) and
`ROUTE-PURPOSE` (`scripts/checks/route.py`) hold the drawing to it. The second sentence, 9 Oct 11:37, *"It has to
be helpful knowledge... helpful data that you're looking at... in a cool format"*, is what the rendered sheet is
(`sheet-phone-day-390.png`: install, start, fetch, two catches, Ctrl-C, the file, the hand-off; nothing else).

One condition from his words that the PRD under-reports: 9 Oct 11:32, *"it has to be kind of accepting of all
different formats"*. Section 5.2 says the mid edition gives "≥ 14.5 px"; the code gives 11.2 px at an 852 px window
(MF2). The product as built is what he asked for on a phone and a desk, and under what he asked for in the window
between.

## 2. Must-fixes, ranked

Each: where (section and line of `docs/PRD.md`), what to change, why (his words or a source), and whether it is about
the PRD text or the product it defines.

### MF1. "Retire by themselves" is false for three of the eight rows of §5.4 (PRD text and product; §0 line 22, §5.4 lines 166–185, line 172)

I fed the real resolver (`scripts/data/route.py resolve()`, the function `build_stats` and the `route` gate use)
today's `stats.json` with one step flipped at a time, as the weekly build would see it:

| Scenario §5.4 describes | What the PRD says happens | What the resolver does |
|---|---|---|
| a release that exits by itself (`ends_by_itself` passes) | H1 retires | **true**: H1 → `""`, `retired: True`, no entry unverified |
| a release whose User-Agent carries a contact (`ua_seen` fails) | "L7 retires" (line 181) | **L7 becomes unverified**; `ROUTE-UNVERIFIED` fails the build. L7 (`chart.toml` id `L7`) has no `instead`, so there is no wording that holds when `ua_seen` fails |
| a release with a Crawl-delay parser (`fn parse_crawl_delay` in `src/robots.rs`) | "draws S2; rewords L1 and L4 … release anchor" (line 180) | **L1 and L4 become unverified**; the build fails. Every L1/L4 wording that does not need `absent = "fn parse_crawl_delay"` needs probe `crawl_delay_obeyed` (`chart.toml:1080, 1155, 1160`), and `scripts/runcheck.py` has no such probe (its own comment at `chart.toml:1074` says "not written yet"). The resolver's reason: `run check: no step crawl_delay_obeyed` |
| SIGTERM writes the file (`kill_writes_file` passes) | "W1 drawn" (line 184) | **W1 is not drawn and its words change to the fallback** `"logged to disk, then saved to redb, in batches"`. Two reasons: W1's first wording *requires* `fails = ["kill_writes_file"]`, so a passing kill un-holds it; and W1 carries `drawn = false` set by hand (`chart.toml`, the review-round-15 comment: the phone sheet had no room). `tests/test_round13.py:258 test_kill_that_writes_brings_the_old_words_back` pins exactly this behaviour. `resume_after_kill` is named by no entry at all (grep of `chart.toml`: the only hit is a comment) |

So of the eight rows, "exits when the frontier drains", "robots 404 → allow …" (L4's first clause via `robots_read`
passing, L6/H0 via `robots_stall` failing: both have `""` fallbacks), "disallowed and noindex left out" (X1's
fallback on `sitemap_keeps_disallowed` failing) and "a LICENSE" retire by themselves. The parser row, the UA row
and the SIGTERM row do not, and line 172's "Nothing conditional is edited by hand" is contradicted by W1's
`drawn = false`.

Change: (a) §0 bullet 3 → "Four of the eight cautions retire on their own at the next weekly run; the Crawl-delay
row needs a probe written here first, the User-Agent row needs an empty fallback wording, and W1 needs its hand
switch replaced by a probe." (b) §5.4: add a fourth column, **Needs in this repository**, with: parser row → "probe
`crawl_delay_obeyed` in `runcheck.py`, else the build fails on L1 and L4"; UA row → "an `instead` with
`fails = ["ua_seen"]`, `text = ""`, else the build fails on L7"; SIGTERM row → "replace `drawn = false` with a
wording that holds on `kill_writes_file` passing; today a passing kill prints the fallback". (c) Line 172: "Nothing
conditional is edited by hand, except W1's `drawn = false` (§5.1)". (d) Product: write the probe and the two fallbacks
now; they are small, and the PRD's option 1 (§9.1) cannot be "every caution retires on its own" until they exist.
Why: his words of 9 Oct 11:35, *"how is the data gathered? … it feels lazy"*: the PRD tells him the page tends
itself, and for three faults it would instead go red on the Sunday after he fixes them. The traceability sources
below say it in one line: a link in a matrix "describes the planned relationship; it does not prove the
implementation exists or the test passed" [S9].

### MF2. §5.2 says the mid edition holds 14.5 px; it holds 11 px, and under 13 px for windows 852–930 (PRD text and product; §5.2 line 137)

Line 137: "mid-day / mid-night | 820 × 707 | 852 to 1,199 px | 482 to 765 px | ≥ 14.5 px (DESK-PX)". `DESK-PX`
starts at `breakpoint_px + 1` = 1,200 (`scripts/checks/column.py:50`, `chart.toml:9`); between 852 and 1,199 the
only floor is `HERO-COLUMN-PX`'s `MIN_PX = 11.0` (`column.py:45`), and the comment at `column.py` derives the mid's
820-unit width from exactly that 11 px. I computed the served size from `column.served()`, `column.column_px()` and
the round-16 build report's smallest run (19 units):

| window | column | smallest route text |
|---|---|---|
| 852 | 482 | **11.2 px** |
| 900 | 530 | 12.3 px |
| 930 | 560 | 13.0 px |
| 1,012 | 578 | 13.4 px |
| 1,024 (iPad, iPad mini, sideways) | 590 | 13.7 px |
| 1,199 | 765 | 17.7 px |
| 1,200 | 766 | 14.6 px (DESK-PX from here) |

So in a 852–930 px window the route's words are under the 13 px floor the PRD sets for a phone (§7.4 line 270), and
under 14.5 up to 995 px. Change the cell to "11.2 to 17.7 px (floor 11, HERO-COLUMN-PX)" and add a row to §7.4 or
§9.3: "the mid window's floor is 11 px, under the phone's 13". Product: either lift the mid floor to 13 (the sheet's
own derivation says 820 units cannot hold it at 482 px; a narrower mid or a second breakpoint at 931 would) or state
the trade in §11 in his words. Why: 9 Oct 11:32, *"it has to be kind of accepting of all different formats"* and
*"if you look at it on an iPhone, it's very difficult to see"*: 11.2 px is smaller than anything the phone shows.

### MF3. "At most 900 px tall at any viewport from 360 to 1,920" is not what the gate checks, and is false (PRD text; §5.2 line 141, §7.4 line 271)

`HERO-COLUMN-PX`'s height clause runs from `TALL_FROM = 768` (`column.py:47`), not from 360. Below 768 the column is
the viewport less 82 and the phone sheet (600 × 1,121) is drawn 1.87 × the column tall: 968 px at a 600 px window,
1,237 px at 744 (an iPad mini held upright), 1,280 px at 767. The sheet is under 900 px from 360 to about 563 and
from 768 up. Change both lines to "≤ 900 px tall from 768 px up (HERO-COLUMN-PX, `TALL_FROM`); below 768 the profile
is one column and the sheet is 1.87 × the column". Why: a PRD that states a measured bound should state the bound the
code measures; his instruction was the phone and the web, and the PRD need not promise the window between, but it
must not promise it falsely.

### MF4. EXPIRY never fails, and the thesis line the PRD says is "cut, everywhere" is still in the file that instructs him (PRD text; §3 line 84, §7.5 line 292, §7.3)

G14 says "EXPIRY-KEY (a stale review key fails)". All three EXPIRY codes are `warn` (`scripts/checks/expiry.py:37,
40, 42`; its docstring: "a warning, never a fail"). Write "warns" in G14 and "gate (warn)" at line 292. More to the
point of G14: nothing in the repository bans the thesis line. `BANNED` (`scripts/checks/strings.py:24–29`, 20
phrases) does not carry "wrong about itself"; neither does the `gone` list of `test_committed_readme_is_the_one_chart_page`
(`tests/test_pipeline.py:511–518`). And `docs/BEN-TODO.md`, the file §7.6 and §9.2 name as where his asks live,
still tells him under "Round 4 … 1. Bio and profile fields" to set his GitHub bio to *"The web is wrong about itself;
I survey the part that isn't linked."* Change: add "wrong about itself" to `BANNED` (it scans `README.md`,
`chart.toml`, the SVGs and the report; extend the scan to `docs/BEN-TODO.md` or strike the line there), and say in
G14 "held by: `[copy]` has no `thesis` key; `STRINGS-BANNED` on the phrase; BEN-TODO.md round-4 item 1 struck". Why:
9 Oct 19:39, *"The wording is fucking weird survey the web that is wrong about itself come the fuck on."* The one
file written for him to act on still asks him to publish it.

### MF5. T-PURPOSE does not hold "no ships, boats, buoys, roses" (PRD text; §7.1 line 230)

The row's status is "test" and its evidence is "T-PURPOSE: every mark is inside a PURPOSE group; the only shapes are
bars, rings, lines, a dotted box". The test (`tests/test_route.py:812–829`) asserts three things: every
`<g id="hero-X">` is a PURPOSE key, the drawn set equals the keys less a hand-kept `{S2, W1}`, and no
`path|circle|rect|use` sits outside a group. It never looks at what is inside a group: a hull drawn as a `<path>`
inside `hero-R5` passes. `legend.py` would catch a `<use href="#hero-sym-…">` with no legend, but nothing catches a
drawn shape. Change the status to "review; T-PURPOSE holds containment only", or add the assertion the row claims
(inside every non-text group only `rect`, `circle`, `line`, `path` with a straight-segment `d`, and the dotted `rect`;
no `use`, `symbol`, `polygon`, `image`). Why: 9 Oct 11:35, *"Don't show me fucking ships unless it's like artfully
well done"* is the rule he said most often; the register tells him a test holds it, and a test does not.

### MF6. "No row without an element" is a hand list in one test, not a gate (PRD text; §7.2 line 236)

`ROUTE-PURPOSE` is one-way: "a drawn element without a row" (`scripts/checks/route.py:43`). The other direction lives
only in `test_every_element_has_a_purpose`, which subtracts `{"S2", "W1"}` by hand (`tests/test_route.py:819–822`),
so a third undrawn row would need an edit to the test to pass. Change the status column to "gate (drawn → row);
test (row → drawn, with S2 and W1 excused by name)", or derive the expected set in the test from `data.route.drawn()`
so the exclusion is computed. Why: §7's own standard, "the last column is where it lives", and Willison's point that
documentation coverage tests "at least protect against adding a new option but forgetting to document it" [S1]: a
hand list protects nothing new.

### MF7. Two of his process rules, and the one the renders made him say, are not in the register (PRD text; §7.6 lines 300–311, §7.4)

- 8 Oct 09:04: *"Resolve all merge conflicts and all PRs need to be ready to merge."* No row. The PRD's own status
  is "no PR" with 24 commits past `main`, and PR #17 is open (I confirmed with `gh api
  repos/BenjaminSRussell/BenjaminSRussell/pulls/17`: `state: open`, head `v11.1/no-thesis`). Add to §7.6: "Every open
  PR is mergeable; a branch is opened as a PR before a round ends | process, **not met today** (PR #17 open, this
  branch has none)".
- 8 Oct 11:13: *"Merged but all images are unavailable."* The rule it set (no README names a sheet the `chart` branch
  lacks) is held by `publish_chart.unshipped` (`scripts/publish_chart.py:81`), `test_publish_before_commit`
  (`tests/test_round15.py:193`) and `test_publish_needs_every_named_edition` (`tests/test_round12.py:124`), and the
  workflow's step order. It appears only as §8.1 item 5. Add a §7.4 row: "The six editions are on the `chart` branch
  before `README.md` names them | test, process | `publish_chart.unshipped`; `profile.yml` publishes before the
  commit".
- 7 Oct 16:12 (*"review every single detail… about 2 hours"*), 7 Oct 17:58 (*"30 different perspectives… 10
  technical agents"*; `docs/crit/panel30/` exists) and 11 Oct (later) (*"ensure this is something I want to see
  rounds of reviews and research"*) are process instructions the register's G17–G19 fold in without citing. Cite
  them in G19's "His words" cell; the yardstick should be complete where it is quoted. Reviewer 1 of this round has
  already asked for 7 Oct 17:40 and 8 Oct 14:22 to be added to §3, and for the "26 messages" at line 8 to become 21;
  both are right and I do not rank them again.

### MF8. The PRD's claims about enforcement are not themselves enforced (product and process; §6, §7, appendix B)

I checked every code in §7 and appendix B against `scripts/checks` by grep, every tier against `TIER`, the counts
by counting, and §8.2 against `gate.txt`; all held. That took a reviewer an afternoon and will be stale at the next
plug-in. The projects that keep documentation true do not re-read it; they run it: doctest executes the examples in
a docstring [S2], rustdoc compiles and runs every code block in a doc comment [S3], Go runs `Example` functions and
diffs their `// Output:` [S4], Sphinx and mdBook do the same for a manual [S5, S6], GitLab's CI fails a merge request
whose generated reference page was not regenerated [S7], and Datasette's `test_docs.py` fails when a config option
or a view class has no documentation [S1]. This repository already does that for the page (README-STALE,
DESIGN-FRESH, AUDIT-STALE, AUDIT-COVER): the PRD is the one document it does not. Add `tests/test_prd.py`:

1. every `[A-Z]+(-[A-Z]+)+` token in §7 and appendix B is emitted by some `scripts/checks/*.py` (and every emitted
   code is in appendix B);
2. each appendix-B tier equals the plug-in's `TIER`;
3. §6's counts (28 plug-ins, the `unittest` total, the run check's `len(steps)` and its gate/probe split) match;
4. §8.2's warning codes equal the gate's `warn` set on a fresh build;
5. §5.1's ID column equals `PURPOSE`'s keys, with the same Q per row;
6. each row of §5.4 is a fixture the resolver is run against (the four scenarios in MF1 are the fixture).

And fix the two facts a test would have caught: line 3 (`027f081`, 23 commits) is one behind the commit that holds
the PRD (`9e3db34`, 24; say "at 027f081 plus this document"), and line 8's "26 messages" is 21. Why: his words, 9 Oct
20:50, *"review and check and review and check"*: a check that runs is one he does not have to ask for again.

### MF9. Precision in §5.1 and appendix B (PRD text; lines 117–122, 504, 510)

- F1 (line 119): the printed words are the entry's **second** wording. The first, "fetches pages, fewer at once when
  saves average over 500 ms…", fails on purpose on `absent = "current_permits > MIN_PERMITS"` (`chart.toml`, F1);
  a release whose governor loses that floor flips the text back. "Drawn only when" should say so, since it is the one
  row where the next release changes the image's words without changing a fault.
- H1 (line 121): "probe `ends_by_itself` failed and `quiet_slow_page` passed". The wording also needs `crawl_ctrl_c`
  and `quiet_after_last_page` to have passed (`runs = [...]`, three probes).
- S1 (line 117): also drops the command and prints "starts from your URL; …" when probe `crawl_help` is absent
  (wordings 3 and 4).
- W1 (line 122): "never drawn today: `kill_writes_file` failed" is backwards (MF1): it holds *because* the kill
  failed, and is undrawn because `drawn = false`.
- Appendix B line 504, `data`: "stats.json invariants (calendar, sweeps, keys)" names no code. The codes are
  `data.load`, `data.seeded`, `data.provenance`, `data.schema`, `data.invariant`, `data.calendar`, `data.stale`,
  `data.unsurveyed`, `data.edition`, `data.notices`, `data.tide`, `data.variation`, `data.claims`, `data.clones`,
  `data.repo_count` (`scripts/checks/data.py:53–97`); "sweeps" is not one. `data.tide` and `data.variation`, like
  the `log.*` codes at line 510, check sheets that are off the page; mark them idle as the FLASH/MOTION row does.
- §7.1 line 225: the banned list ends "v7"; `BANNED` (`strings.py:24–29`) has no "v7".

## 3. The register, row by row

What I opened for every row of §7, and whether its status and "where" are right. "Holds" means the named thing
exists, runs in the tier the PRD claims, and checks what the row says.

### 7.1 Don't name the theme

| Row | Holds? | Note |
|---|---|---|
| theme words on image/alt | yes | `ROUTE-WORDS` (`checks/route.py:60–62`, 18 words as listed); `test_no_theme_words` (`test_route.py:842`) |
| theme words in DESIGN.md | yes | `DESIGN-FRESH` + `design.theme_words` (`checks/design.py:28`, adds `EXTRA_WORDS`) |
| README prose | honest "review only" | `checks/readme.py` has no theme scan (grep "theme": none) |
| banned phrases | yes, less "v7" | `strings.py BANNED`; scanned over SVGs, manifest, alt, README, chart.toml (`STRINGS-MANIFEST/-ALT/-README/-TOML`) |
| themed headings | yes | `test_pipeline.py:488–518` pins "**Also**", "**Working rules**", bans "Ship's log", "Notices to mariners", "Survey log"… |
| BREAKS name a fact | yes | `test_breaks_name_a_fact` (`test_route.py:850`): no theme word, no land/sea/water in the reason |
| pirate language | yes | `ahoy`, `arr` in THEME_WORDS |
| winks | review | as stated |
| no ships, boats… | **no** (MF5) | T-PURPOSE holds containment, not shape |

### 7.2 Purpose and size

| Row | Holds? | Note |
|---|---|---|
| PURPOSE row per element, no row without element | half (MF6) | gate one-way; test the other way with a hand list |
| nothing has a size | yes | `test_nothing_has_a_size` (`test_route.py:780`): counts ×3+7, ×2+1, ×5, +9; shape lists equal |
| only where there is a route | decision | `DECISIONS.md` "Concepts and scores": A 8/6/8 = 22 on goal; D 21, C 16, B 12 |
| one home per fact | yes | `STRINGS-TWICE` (`strings.py`, TWICE_WORDS/SHORT_WORDS), `HERO-SELF-TWICE` (`route.py`, `TWICE_SELF = 4`) |
| one count | yes | `STRINGS-COUNT`; README has "21 ways" |

### 7.3 Honest data

| Row | Holds? | Note |
|---|---|---|
| nothing invented | yes | `STRINGS-UNMEASURED`, `ROUTE-STRINGS` (`route_check.SOURCES`); `test_facts_block_prints_only_present_keys` (`test_pipeline.py:405`) |
| register per figure | yes | `AUDIT-STALE` (`audit.py`, regenerated by `scripts/audit_figures.py`, which exists); `AUDIT-COVER` |
| typed numbers rest on `[[figures]]` | yes | `FIGURES` (`figures.py`, via `scripts/data/proof.py`) |
| claims rest on anchors at HEAD and sdist | yes | `ROUTE-UNVERIFIED/-HEADER/-LABEL/-WAITING`; `test_release_holds_head_does_not_fails` (`test_round15.py:167`) |
| commands run, 14 days | yes | `ROUTE-ENTRANCE` (`MAX_AGE`); run check dated 2026-10-10, `taken` 2026-10-10 |
| README-SUBCOMMAND | yes | emitted in `readme.py` |
| NOTICE-DATE/-AUTHOR/-LIVE/-ANCHORS | yes | `notices.py`, `notices_live.py`; `test_month_is_his_first_commit` (`test_proof.py:47`) |
| skipped is never a pass | yes | `runcheck._skip` sets `steps[-1]["skipped"] = True` (`runcheck.py:696–699`); `data/route.py:388–392` reads it; `ROUTE-PROBE-SKIPPED` warns; `test_skipped_is_not_a_pass` (`test_round15.py:277`) |
| sweep days | yes | `stats.json sweep_dates` = 2025-11-09, 2025-11-10, 2026-10-01, 2026-10-07, as the row says |
| tests are functions; languages from lines | yes | `test_data.py` names as given; `[lines.exclude]` at `chart.toml:96` |
| agent commits apart | yes | `test_agent_authored_and_agent_share` |
| no commit totals, no "last commit" | yes for the survey line | `test_provenance_line_is_from_stats_only` (`test_pipeline.py:307–335`): bans `commits`, `all_hands`, `calendar_total` figures and "generated/regenerated/weekly"; ≤ 60 words. The facts lines print agent counts and "his own 101/420", as the PRD admits |
| CI-GATES | yes | `readme.py` (warn) |
| scrape_interval | yes | test exists |
| placeholders | yes | `position.py`, `readme.py`, `strings.py` |
| byte-identical builds | yes | `test_two_builds_byte_identical` (`test_route.py:807`) |
| figures retire | **partly** (MF1) | `test_retires_when_fixed`, `test_a_crawl_that_ends_retires_h1` exist and pass; the rule is true of H1, L4, L6, H0, X1 and false of L1/L4-with-parser, L7, W1 |

### 7.4 Phone first

| Row | Holds? | Note |
|---|---|---|
| phone edition ≤ 851, `<img>` fallback | yes | `test_picture_order`; `HERO-FALLBACK` (`column.py`, render) |
| 13 px / 11 px floors | yes | `route.py:77–78`: `PHONE_SCREEN, MIN_PX = 308, 13.0`; `NARROW_SCREEN, MIN_PX_NARROW = 278, 11.0`. Measured: 13.35 px at 390, **12.05** px at 360 (§5.2 line 136 says "11.0 px"; that is the floor, not the size) |
| one screen ≤ 900 px, 360–1,920 | **no** (MF3) | from 768 only |
| desk ≥ 14.5 from 1,200; mid 852–1,199 | yes as a rule; §5.2's mid cell is wrong (MF2) | `DESK_MIN_PX = 14.5`, `DESK_FULL_PX = 16.0` |
| code ≤ 32 columns | yes | `readme.py CODE_COLUMNS = 32`; `test_no_fenced_line_over_32` (`test_round7.py:71`) |
| FLAG-WRAP | yes, render | `wrap.py TIER = "render"`; `test_lever_line` (`test_round10.py:262`) |
| cautions ≤ 7 items, ≤ 25 words | yes | `readme.py cautions(max_items=7, max_words=25)` |
| type floors 19/25, 26/30 | yes | `tokens.FLOORS` (`tokens.py:73–75`); `TYPE` via `typeset.check_type` |
| bounds, 6-unit frame; box pad ≥ 8 | yes | `bounds.py` (fast), `boxpad.py` (render, `BOX_PAD_MIN = 8` at `sheets/route.py:67`) |
| one left edge; ≥ 2 pitches | yes | `HEAD_GAP_PITCHES = 2` (`route.py:72`) |
| contrast | yes | eight CONTRAST codes in `contrast.py` |
| night redrawn | code | `tokens.THEMES`, not re-checked |
| device check | open | honest |
| even density | review | honest |

### 7.5 Copy, 7.6 Process

Every 7.5 row holds as written except "re-read by 2027-06 | gate" (warn, MF4); "The thesis line is gone | config"
is held by an absence only (MF4). The 7.6 rows are process claims a repository cannot show: I can confirm the
commit trailers on `git log` (present), the weekly bot commit in `profile.yml`, `docs/BEN-TODO.md`'s existence and
"16 rounds × 3 reviewers" (48 files). "The stop hook" and "Workflow `wf_eee12105-794`" are not in the repository
and I did not verify them; the PRD should mark them "session, unverifiable here". The row "Never push to `main`"
sits next to §0's "no PR" and his 8 Oct 09:04 sentence, which the register lacks (MF7).

## 4. The other direction

### 4.1 Finding codes that hold a rule the register does not carry

From the 167 distinct codes emitted under `scripts/checks/` (grep of the string literals, `data.*` and `log.*` included), these hold a rule of the
product and appear nowhere in §7 (some are in appendix B or C as names only):

- `ROUTE-HEIGHT` (desk ≤ 770, phone ≤ 1,246, mid ≤ 964 units; `route.py:70`), `ROUTE-PAINT` (track, loop and the
  line past the end painted before rings and words), `ROUTE-ARROW` (arrowhead clear of a ring's centre row by
  `ring_r + 2`), `ROUTE-RELEASE` is in 7.5 but `ROUTE-CODE-SPACE`'s 1.3× gap limit is not stated.
- `ALT-LAST` (last sentence ≤ 10 words), `ALT-POEM` (info; a `chart.toml alt_poem` that must equal the alt's last
  sentence: a rule from the old page still running).
- `SIZE-RAW/-GZ/-PHONE/-PAGE/-ELEMENTS/-TARGET` and `REPORT-SHA/-BYTES/-MISSING/-ORPHAN/-STATS` (300 KB raw, 100 KB gz,
  120 KB phone, 250 KB per edition set, 3,000 elements; the report's hashes match the SVGs and `stats.json`).
- The twelve `XML-*` codes (no `<text>`, `<script>`, `<style>`, external href; ids unique and sheet-prefixed; every
  reference resolves). Appendix C says these "survive"; §7 does not carry them.
- `README-MISSING/-PICTURE/-PICTURE-FOLDED/-RENDER/-DETAILS`, `POSITION-UNSET/-MISMATCH/-COMMENT/-BLOCK/-STALE`,
  `CONTACT-PLACEHOLDER`.
- `CONTRAST-DANGER` (the dotted line ≥ 3:1 and nothing filled under the trap's words) is in §5.1's prose, not a row.
- `data.*` (fifteen) and `log.*` (six), of which `data.tide`, `data.variation`, `data.claims` and all of `log.*` are
  rules of sheets that are off the page.

### 4.2 Tests that hold a rule the register does not name

Of the 539 tests, these pin a rule with no row (file:line):

- `test_round16.py:77 QuitNotDone`: H1 never says "done" while H0 is drawn (the round-16 fix; the one copy rule a
  stall made necessary, and the register has no row for it).
- `test_round13.py:248 test_one_line_everywhere`: H0 is one phone line in every edition; `test_round15.py:295
  test_phone_height_holds_at_851`.
- `test_round13.py:258 test_kill_that_writes_brings_the_old_words_back` (the W1 behaviour MF1 describes).
- `test_round6.py:88 test_every_committed_conditional_wording_has_a_probe_or_producer` and `:167
  test_any_gated_text_entry_is_skipped_while_its_gate_fails`: every conditional wording rests on a probe or a
  `producer` anchor, never on a setter alone; a gated text entry is skipped while its gate fails.
- `test_round15.py:167 test_release_holds_head_does_not_fails` (a regression on `main` fails even when the release
  holds), `:193 test_publish_before_commit`, `:346 test_unbound_port_is_skipped`.
- `test_round12.py:124 test_publish_needs_every_named_edition`, `:208 test_c1_has_no_colon_mid_sentence`, `:224
  test_fold_label_names_the_largest_group`.
- `test_round9.py:222 test_probe_must_wait_as_long` (the quiet figure the image prints is at most what the probe
  waited), `test_round13.py:214 test_stage_is_checked` (every caution has a stage and the list runs in stage order).
- `test_proof.py:158 test_rest_repos_drops_forks`, `:47 test_month_is_his_first_commit`.
- 69 of the 539 tests (`test_supporting.py` 24, `test_timeline.py` 26, `test_approaches.py` 19) test sheets that
  are off the page; §6's "539" counts them. Say so, or say which count is the product's.

Note also that `grep -c "def test_"` over `tests/` gives 550; `unittest` runs 539. Eleven `def test_` are helpers or
nested; the PRD's 539 is the right number, and a `test_prd.py` should take it from the runner, not the files.

### 4.3 Sentences of his that state a rule the register does not carry

From `owner-messages.md` (21 messages):

| Date | His words | Rule | In the register? |
|---|---|---|---|
| 7 Oct 16:12 | "review every single detail I want so much attention to detail this should take about 2 hours" | effort per pass | no |
| 7 Oct 17:40 | "it should say more than it literally says and should have layers of depth" | a second reading finds more | no (reviewer 1, MF2 of his review) |
| 7 Oct 17:58 | "30 different perspectives from 30 different agents … then 10 technical agents" | the panel | no row; `docs/crit/panel30/` and `tech/` exist |
| 8 Oct 09:04 | "Resolve all merge conflicts and all PRs need to be ready to merge" | PRs mergeable | **no** (MF7) |
| 8 Oct 11:13 | "Merged but all images are unavailable" | sheets published before the README names them | §8.1 only (MF7) |
| 8 Oct 14:22 | "The images are all crushed" / "The images are not cool enough" | the image at the column's width; finish | G3/G4 by implication; "not cool enough" not quoted (reviewer 1) |
| 9 Oct 11:32 | "If they're looking at your repos, it's definitely on the web" | the desk is the likelier reader | §2 reverses it (reviewer 1, MF6 of his) |
| 9 Oct 11:35 | "the different ages, different opinions, yeah, it's cool, but … Where's the fucking opinions there?" | reviewers of distinct standpoints | G19 says "independent"; not "distinct" |
| 11 Oct (later) | "Review and ensure this is something I want to see rounds of reviews and research" | this round's own test | not quoted anywhere in the PRD |

## 5. The checks that held

| Claim | How I checked | Result |
|---|---|---|
| 28 plug-ins (§6, appendix B) | `ls scripts/checks/*.py` less `__init__` | 28 |
| 539 tests (§0, §6) | `python3 -m unittest` | Ran 539, OK, 22.4 s |
| 25 run-check steps: 7 gate + 18 probes (§6 line 202) | `stats.json runcheck.rustmapper.steps`: `gate` flag | 7 gate (venv, install, help, crawl_help, export_help, crawl_ctrl_c, export) + 18 probes, the 18 names as listed |
| §8.2's four warnings | `round-16/gate.txt` | `log.shards`, `POSITION-EMPTY`, `LICENSE-FLAGSHIP`, `ROUTE-WAITING S2`; 0 fail, 0 error, exit 2; render tier ran boxpad, column, frames, wrap |
| appendix B tiers | each plug-in's `TIER` | fast for 23; render: boxpad, column, frames, wrap; perf: perf |
| every code in §7 and appendix B exists | grep of `"CODE"` literals in `scripts/checks/*.py` | all present, including the thin ones (`ROUTE-MISSING` route.py:258, `STRINGS-ALT/-MANIFEST/-README/-TOML` strings.py:164–183, `ALT-NO-README` alt.py:27, `SIZE-PAGE` size.py:59, `POSITION-STALE` position.py:56, `README-RENDER` readme.py:337, `ROUTE-HEIGHT` route.py:305) |
| §5.1's 17 IDs and Q's | `sheets/route.py PURPOSE` | same 17 keys, same Q on every row; `chart.toml` wordings match for S1, S2, H0, H1, C1, R13, L1–L7, X1–X3 |
| §5.1 R15's condition | `stats.json handoffs[0]` | `state: runs`, reader `scripts/import_rust_sitemapper.py`, test `tests/test_import_rust_sitemapper.py` |
| §5.1 S2 "waits" | `chart.toml` S2 `waits = "release"`, head anchor `tests/robots_4xx_allows_crawl.rs` | as stated; `ROUTE-WAITING` warns |
| §5.3 row 9 formula | `render_readme.more_count` | `repo_count − 1 − facts repos − Also names`, computed from the text |
| §5.3 row 12 | `test_provenance_line_is_from_stats_only` | ≤ 60 words; bans generated/weekly/commit figures |
| §5.2 sheet sizes | `viewBox` of the six round-16 SVGs | 1000×707, 820×707, 600×1121 |
| §2 "R4 (57 sources)"; §0 "360 in seven files" | `DECISIONS.md` Research table | R1–R7: 44+44+62+57+52+54+47 = 360 |
| §0 "31 to 59 sources per round" | rounds 13 and 16, Sources sections | 10+11+10 = 31; 11+9+11 = 31 (the low end holds; I did not count the high) |
| §0 "PR #17 open" | `gh api …/pulls/17` | open, head `v11.1/no-thesis` |
| §6 workflow | `profile.yml` | Sunday 06:20 UTC; `runcheck` on macos-14 then `chart` on ubuntu; publish before commit; pencil-note step; `workflow_dispatch` with `dry_run`. Push paths also include `assets/log.json` and `requirements.txt`, which §6 omits |
| line 3's HEAD | `git log` | PRD is at `9e3db34`, 24 past `main`; it names the commit before itself |

## 6. Research: how projects make documentation claims verifiable, and whether the PRD's are stated at the right level

Twelve sources. The question my lens asks is whether "gate / test / review / process / open" plus a code name is the
right level for a claim that a rule is enforced.

1. **Executable examples.** Python's `doctest` "searches for pieces of text that look like interactive Python
   sessions, and then executes those sessions to verify that they work exactly as shown" [S2]. rustdoc "supports
   executing your documentation examples as tests. This makes sure that examples within your documentation are up
   to date and working" [S3]. Go's testable examples compare captured stdout to the `// Output:` comment; "Having
   executable documentation for a package guarantees that the information will not go out of date as the API
   changes" [S4]. Sphinx's `doctest` extension and mdBook's `test` command do the same for a manual and a book [S5,
   S6]. The common move: a claim in a document is a fixture the build runs, so the document cannot drift without
   the build going red. The PRD's §5.4 table is exactly such a set of claims ("a release that does X retires Y"),
   and it is the one place the PRD is wrong three times (MF1). It should be a fixture (MF8 item 6).

2. **Documentation coverage tests.** Willison's `test_docs.py` for Datasette introspects the code (`dir(app)` for
   `*View` classes) and parses the docs (reST labels) and fails when one is undocumented; the tests "at least
   protect against adding a new option but forgetting to document it", and he notes they "can't judge documentation
   quality" [S1]. The PRD's appendix B is a list of 28 modules and their codes; a test that every emitted code is
   listed, and every listed code is emitted, is forty lines and would have caught "sweeps" (MF9).

3. **Generated reference pages that fail CI when stale.** GitLab's docs pipeline has `graphql-verify`, which "fails if
   the GraphQL reference page isn't regenerated through the required process", plus `docs-lint links`, Vale,
   markdownlint and `lint-docs.sh` checks [S7]. This repository already runs the same pattern for `README.md`
   (README-STALE), `DESIGN.md` (DESIGN-FRESH) and `AUDIT.md` (AUDIT-STALE). The PRD's register is a fourth generated
   document that is written by hand.

4. **Prose rules as CI.** Vale is "not a general-purpose writing aid"; it holds style rules, a rule at `level: error`
   "will cause CI builds to fail", and there is an official GitHub Action [S8]. `STRINGS-BANNED` and `ROUTE-WORDS`
   are that, and the PRD classes them right. Its one gap in the class is that the README prose is not scanned
   (§10.1), which the PRD reports honestly.

5. **Docs as code.** Write the Docs defines it as writing documentation "with the same tools as code": version
   control, plain text, code review, automated tests; teams "can block feature merges that lack documentation"
   [S10]. The PRD lives in the repository and is reviewed; it is not tested (MF8).

6. **Living documentation.** Cucumber's BDD page sets the goal as "producing system documentation that is
   automatically checked against the system's behaviour" [S11]; the Manning summary found by search adds that such
   documentation "covers the behaviors that have tests" and no more [S12]. That is the honest reading of the
   register: a row marked "gate" is true to the extent the gate's predicate matches the row's words, which is where
   MF4, MF5 and MF6 fall.

7. **Traceability.** A traceability matrix "links and maps project requirements to their corresponding test cases"
   and checks that "every requirement is covered by at least one test case, and conversely, that every test case is
   linked to a valid requirement" [S9]. The PRD's §7 is a one-way matrix (rule → check); §4 of this review is the
   other direction, and it found 30-odd codes and 18 tests with no requirement row, and three of his sentences with
   no row. The playcode template's line, found in search, that a link "describes the planned relationship; it does
   not prove the implementation exists or the test passed" is MF1 in one sentence [S13].

8. **Requirement words.** RFC 2119 defines MUST as "an absolute requirement", SHOULD as something that "may be
   ignored" for understood reasons, and asks that such imperatives "be used with care and sparingly" [S14]. The PRD's
   status column is its own vocabulary, which is fine, but "gate" conflates fail and warn: EXPIRY, ROUTE-WAITING,
   ROUTE-PROBE-SKIPPED, LICENSE-FLAGSHIP, CI-GATES and POSITION-EMPTY are SHOULDs the page can ship with, while
   ROUTE-UNVERIFIED is a MUST. Split the status into "gate (fail)" and "gate (warn)"; the gate's four exit codes
   already make that distinction (`check.py`: 0 pass · 1 fail · 2 warnings · 3 could not check).

**Judgement.** The PRD states its enforcement claims at the right level of *reference*: a code, a module, a test
name, a tier. That is rarer than it should be and is why I could check every one. It states them at the wrong level
of *proof*: it describes what each check does in its own words, and in five rows the words are wider than the check
(MF2, MF3, MF5, MF6, EXPIRY), and in the one table that predicts behaviour (§5.4) the prediction is wrong three
times. The sources agree on the remedy: a claim about what the code enforces should be a thing the code runs.

## 7. Score

**6 / 10.** Four points off: the three false "retires by itself" rows and the hand switch they hide (MF1); the mid
edition's text size, which is a product fault the PRD's table conceals (MF2); the two gate predicates stated wider
than the code (MF5, MF6) with the EXPIRY level and the thesis line still in BEN-TODO.md (MF4); and the absence of
any test of the PRD itself (MF8), which is why the rest could go wrong unnoticed. What I did not take points for: the
pointers. Every code, tier, count, ID and warning the PRD names is real, and that is the half most PRDs get wrong.

## Sources

1. Simon Willison, "Documentation unit tests" (28 Jul 2018),
   https://simonwillison.net/2018/Jul/28/documentation-unit-tests/ — read in full: tests introspect the code
   (`dir(app)` for `*View` classes) and parse the reST labels; "at least protect against adding a new option but
   forgetting to document it"; "easy to cheat" on quality; `xfail` for adoption.
2. Python documentation, `doctest`, https://docs.python.org/3/library/doctest.html — read the opening and the three
   uses: "searches for pieces of text that look like interactive Python sessions, and then executes those sessions
   to verify that they work exactly as shown"; "literate testing" / "executable documentation".
3. The rustdoc book, "Documentation tests",
   https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html — read: "supports executing your
   documentation examples as tests. This makes sure that examples within your documentation are up to date and
   working"; `ignore`, `no_run`, `compile_fail`, `should_panic`.
4. The Go Blog, "Testable Examples in Go", https://go.dev/blog/examples — read: output "compares the output against
   the example's 'Output:' comment"; "Having executable documentation for a package guarantees that the information
   will not go out of date as the API changes"; examples without an Output comment are compiled but not run.
5. Sphinx, `sphinx.ext.doctest`, https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html — read: snippets
   tested so they "stay up-to-date with the code"; `testsetup`, `testcode`, `testoutput`, `doctest` directives.
6. mdBook, "The test command", https://rust-lang.github.io/mdBook/cli/test.html — read: "will run all available
   tests in a book"; the Rust book's reason, "very important for them to be able to automatically test these code
   examples".
7. GitLab, "Documentation testing", https://docs.gitlab.com/development/documentation/testing/ — read: `docs-lint
   markdown` (Vale, markdownlint, `lint-docs.sh`), `docs-lint links`, `graphql-verify` "fails if the GraphQL reference
   page isn't regenerated through the required process", `docs-lint deprecations-and-removals`.
8. Vale documentation, https://docs.vale.sh/ — read: "not a general-purpose writing aid"; style over grammar; a rule
   at `level: error` "will cause CI builds to fail"; `vale-action`.
9. TestDevLab glossary, "Traceability matrix",
   https://www.testdevlab.com/center-of-excellence/glossary/engineering-terms/traceability-matrix — read: "links and
   maps project requirements to their corresponding test cases"; "every requirement is covered by at least one test
   case, and conversely, that every test case is linked to a valid requirement".
10. Write the Docs, "Docs as Code", https://www.writethedocs.org/guide/docs-as-code/ — read: "writing documentation
    with the same tools as code"; version control, plain text, code review, automated tests; "block feature merges
    that lack documentation".
11. Cucumber, "Behaviour-Driven Development", https://cucumber.io/docs/bdd/ — read: "Producing system documentation
    that is automatically checked against the system's behaviour"; "executable specification".
12. Manning liveBook, "live documentation" concept page (via search summary; page not fetched),
    https://livebook.manning.com/concept/software-development/live-documentation — living documentation "covers the
    behaviors that have tests".
13. playcode.io, "Requirements Traceability Matrix Template With Bidirectional Links" (via search summary; the page
    returned 410 on fetch), https://playcode.io/blog/requirements-traceability-matrix-template — a link "describes
    the planned relationship; it does not prove the implementation exists or the test passed"; orphan and stale-link
    detection.
14. RFC 2119, "Key words for use in RFCs to Indicate Requirement Levels", https://www.rfc-editor.org/rfc/rfc2119 —
    read §1, §3, §5, §6: MUST "an absolute requirement"; SHOULD; MAY "truly optional"; "must be used with care and
    sparingly".
15. Repository files read: `/home/user/wt-v12/docs/PRD.md`; `/home/user/wt-v12/docs/crit/prd/owner-messages.md`;
    `/home/user/wt-v12/docs/crit/prd/review-r01-1.md`; `/home/user/wt-v12/README.md`; `/home/user/wt-v12/chart.toml`;
    `/home/user/wt-v12/assets/stats.json`; `/home/user/wt-v12/.github/workflows/profile.yml`;
    `/home/user/wt-v12/scripts/check.py`; `/home/user/wt-v12/scripts/checks/*.py` (all 28);
    `/home/user/wt-v12/scripts/runcheck.py`; `/home/user/wt-v12/scripts/data/route.py`;
    `/home/user/wt-v12/scripts/sheets/route.py`; `/home/user/wt-v12/scripts/render_readme.py`;
    `/home/user/wt-v12/scripts/publish_chart.py`; `/home/user/wt-v12/scripts/tokens.py`;
    `/home/user/wt-v12/tests/test_route.py`, `test_pipeline.py`, `test_data.py`, `test_proof.py`, `test_round6.py`
    to `test_round16.py`; `/home/user/wt-v12/docs/crit/round6/SPEC.md`, `DECISIONS.md`, `LOG.md`;
    `/home/user/wt-v12/docs/BEN-TODO.md`; renders and gate output under
    `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/` (`gate.txt`,
    `build/build-report.json`, `build/assets/hero-*.svg`, `sheet-phone-day-390.png`, `sheet-mid-day-746.png`,
    `page-desk-1.png`).
