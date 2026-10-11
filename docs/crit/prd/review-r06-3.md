# PRD review round 6, reviewer 3: An engineer who trusts nothing the PRD says until the code says it too

11 Oct 2026. Document: `docs/PRD.md` at `b6cca2c` (baseline `027f081`; `git diff --stat 027f081..HEAD -- . ':!docs'`
is empty, so every line the PRD cites was read on the tree it names). Renders:
`scratchpad/r6/build/round-16/` (`sheet-phone-day-390.png`, `page-desk-1.png`, `page-phone-1.png`,
`page-phone-2.png`, `gate.txt`, `build/build-report.json` opened). Everything below that says "ran" or "opened" is a
command I ran or a line I read; the commands are in §6. I did not read the other two round-6 reviews.

## 1. Is the product this PRD defines something he wants, by his own words?

**Yes.** The sentence that decides it is 9 Oct 20:50: *"Everything, single thing inside of this needs a purpose,
not a fucking chasing a reason"*, read with 11:37 as its test: *"The map, very helpful. The fucking log, not
really... It has to be helpful knowledge."* The code says what the PRD says: `scripts/sheets/route.py PURPOSE` has
17 rows and §5.1 has 17 rows, id for id and Q for Q (T1 Q1, T2 Q1, R0 Q2, R1 Q4, R2 Q4, R5 Q4, R6 Q1, S1 Q5, S2 Q1,
F1 Q1, H0 Q5, W1 Q5, H1 Q5, C1 Q5, R12 Q4, R13 Q4, R15 Q2); ROUTE-PURPOSE (`checks/route.py:337`) fails a drawn group
with no row; and the phone sheet draws nothing outside that table: a name, a role, a project line, an install line
with its date, a track, a loop, four steps, a dotted box with two catches, a stop, a file and a hand-off. The log
sheet he called "not really" helpful is off the page (`build_assets.SHEETS = ["hero"]`, line 59).

His 11 Oct sentence, the one this round runs under, is *"Review and ensure this is something I want to see rounds
of reviews and research."* Its object is the page, and the page the PRD defines is the one above. But the round
itself is not what the PRD says should happen: §0's stop rule reads *"no PRD round 6 until a fix round has done
§8.1 items 7 and 8, §10.19 and §10.23 and the branch has a PR"*, no product file has changed since `027f081`, and
`gh api` finds no PR for `v12/purpose`. A document whose process rows say "process" in the status column has to
record when the process did not follow them (MF4).

**§8.3 q.1, first line (G3a), written before re-reading §1 or §5.1** (I had read §1 in earlier rounds, so this is a
PRD reviewer's line, as §8.3 now says): the image shows a crawler called rustmapper, installed with `pip install
rustmapper`, started with `rust_sitemap crawl`, looping over pages until you press Ctrl-C once, and writing
`data/sitemap.jsonl`. A tool, a way to start it, an output.
**§8.3 q.6:** yes, I would screenshot it; I would call it "install notes drawn as a route" (my round-2 and round-5
answer). Third line (G1d, G1e): the care is in one left edge for every row, the release date small beside the
install line, the real field names on the file row, and the gap in the track under the box; there is no decoration
to see it in. Someone who designs for a living would see a designer's hand in the three faces doing three jobs
(serif for the names, condensed sans for the rows, mono for what you type) and in nothing being placed by hand.

## 2. Section 7 and appendix B, row by row, against the plug-ins

Method: an `ast` walk of every `scripts/checks/*.py` printed its docstring, `TIER` and code literals; a grep printed
the level each code is emitted at; a second script resolved every `file:line` cite in the PRD to the line's text; a
third listed every `test_` function in `tests/` with its trailing comment and whether the PRD names it.

**Appendix B: every row holds.** 28 plug-ins (`ls scripts/checks/*.py | grep -v __init__ | wc -l` = 28). Tiers:
`boxpad`, `column`, `wrap`, `frames` carry `TIER = "render"`, `perf` carries `"perf"`, `data.py` and `log.py` have no
`TIER` and `check.py:234` defaults them to fast, the other 21 say `"fast"`. Every code listed under a plug-in is a
literal in that file and no plug-in emits a code its row omits (alt 5, bounds 6, column 3, contrast 8, data 15,
expiry 3, log 6 + the `log.json` path, notices 4, position 9, readme 15, route 21, size 11, strings 8, xml 12; flash
4, frames 9, legend 6, motion 10, perf 4 idle). 169 strings less `YYYY-MM`, `YYYY-MM-DD`, `log.json`, plus `FIGURES`
(`figures.py:93–104`) and `TYPE` (`type.py:35`) = **168**, the preamble's number. Every one of the 168 is in the PRD
by full name or by its row's prefix and suffix (script in §6, result: none missing). The runner's five `error` codes
are at `check.py:115, 246, 254, 286, 288` as appendix B's first row says.

**Levels against §7's status cells.** Every level the PRD states matches the emit: ALT-POEM warn (`alt.py:50`) and
info (`:52`); BOUNDS-TEXTURE and -NO-MANIFEST warn (`bounds.py:85, 56`); REPORT-BYTES warn, REPORT-STATS error
(`size.py:56, 70`); XML-SET-LOOP warn (`xml.py:82`); ROUTE-WAITING warn (`route.py:265`), -PROBE-SKIPPED warn
(`:275`), -HANDOFF info (`:296`); LICENSE-FLAGSHIP and CI-GATES warn (`readme.py:89, 104`); README-MISSING and
-RENDER warn (`:279, 337`); POSITION-EMPTY and -STALE warn (`position.py:31, 56`); EXPIRY-* warn (`expiry.py:37, 40,
42`); SIZE-TARGET warn (`size.py:46`); `data.calendar` warn at `data.py:62, 66` and info at `:69`; `data.tide` and
`.variation` fail (`:84, 87`); `log.computed` info, `log.version` and `.shards` warn (`log.py:53, 65, 69`). The nine
`error` emits §6.1 lists are the nine the grep finds (FRAMES-TOOL `:34`, -RENDER `:65`, -SILHOUETTE `:103`, PERF-TOOL
`:35`, -RUN `:57`, REPORT-STATS `size.py:70`, FLAG-WRAP `wrap.py:105`, MOTION-XML `:129`, MOTION-READ `:278`).

**§7.1.** `THEME_WORDS` (`checks/route.py:60–61`) is the 18 words the first row lists; `design.py:18 EXTRA_WORDS`
has `survey`, `unsurveyed`, `ship's`. ROUTE-WORDS covers the alt (`route.py:319`: `texts + e["alt"]`), and
`test_no_theme_words` (`test_route.py:842`) joins `e["alt"]` too, so "on the image or in its alt text | gate, test"
is exact. The README-prose row is right that nothing holds it: `test_readme_words` (`test_round6.py:318`), which a
reader of the test list would take for that gate, pins the circuit-breaker sentences, not theme words. The five
`[copy]` keys are at `chart.toml:35–39`. `BANNED` (`strings.py:24–29`) is the 20 entries listed. The headings row's
test (`test_pipeline.py:488–510`) does pin `**Also**` and `**Working rules**` in order and bans `## Soundings`,
`## Ship's log` and the rest. T-PURPOSE's hand list `{"S2", "W1"}` is at `test_route.py:821`.

**§7.2.** ROUTE-PURPOSE one-way (`route.py:337`); `test_nothing_has_a_size` (`:780`) varies `test_functions`,
`commits`, `lines` and `repo_count` and compares every non-text shape; STRINGS-TWICE/-COUNT fail (`strings.py:173,
176`, `SHORT_WORDS = 3` at `:68`).

**§7.3.** Every test named exists at the line named (37 test names resolved, §6). The conditional-wording rule:
`CONDITIONAL` at `scripts/data/route.py:59`, `producers()` at `:236`, the test at `test_round6.py:88`. ROUTE-ENTRANCE
`MAX_AGE = 14` (`route.py:58, 289`). `[facts]` (`chart.toml:667`) has one key, `built_on`; `render_readme.py:459` calls
`agent_clause(r)` with no switch; `README.md:38, 86` print the counts. `[position] text`, `[contact] linkedin`,
`resume` are `""`. `[lines.exclude]` at `chart.toml:96`; `sweep_dates` at `render_readme.py:860`; `coauthored_total`
and `agent_authored` are the stats keys `build_stats.py:510–511` read.

**§7.4.** `column.py`: `MIN_PX = 11.0` (:45), `TALL_FROM = 768` (:47), `TALL_PX = 900.0` (:48), `DESK_MIN_PX = 14.5`
(:50), the `breakpoint_px` read (:231); `column_px(852)` = 482, `(390)` = 308, `(360)` = 278, `(1200)` = 766, `(1280)`
= 846, so every pixel figure in §5.2 and §9.1b recomputes (26 × 308/600 = 13.3; 19 × 482/820 = 11.2; 1,121/600 × 482
= 900.5). `checks/route.py:77–78`: `PHONE_SCREEN, MIN_PX = 308, 13.0`, `NARROW_SCREEN, MIN_PX_NARROW = 278, 11.0`.
`CODE_COLUMNS = 32` (`readme.py:28`). `BOX_PAD_MIN = 8` (`sheets/route.py:67`). `arrow_clear` tests `d < r + 2`
(`route.py:211`). `tokens.BUDGETS` (`:131`): 300/100/3000/120/250 and `targets_kb["hero"] = (170, 60)`.
`FLOORS` (`tokens.py:73–74`): desk 19/16/25, phone 26/18/30. `HEIGHT` (`route.py:70`): 770/1246/964. The round-16
report's sheets are 1000 × 707, 820 × 707, 600 × 1121, as §5.2 says. `publish_chart.unshipped` at `:81`; the docstring
is lines 2–14 and the argparse options are `--dry-run`, `--branch`, `--remote`, `--report`, `--social`, `-m`, no keep.
`README.md:7–13` has six sources and the `<img>` fallback is `hero-phone-day`; `grep -c prefers-reduced-motion
README.md` = 0; `git show d253286:README.md` lines 6–13 name the four `still` sheets under `prefers-reduced-motion`.

**§7.5.** `alt.py:33, 35, 40`: 25 words, "the", 10 words. `test_first_mention` `test_round7.py:367`, `test_one_spelling`
`:391`, `alt_poem` `chart.toml:563`, README-CD `readme.py:247/326`, README-LICENSE `:313`, THIS-REPO `:307`.

**§7.6 and appendix D.** PR #17: `gh api repos/…/pulls/17` → `open`, `mergeable: true`, head `v11.1/no-thesis`.
This branch: `gh api "repos/…/pulls?state=all&head=BenjaminSRussell:v12/purpose"` → 0. The "not met today" is
right; the reason the PRD gives for it is not (MF3).

## 3. §5.1, §5.4, §6 and §8.2 against the code

**§5.1 against `chart.toml [route.rustmapper]`** (19 `entry` tables: S1, S2, F1, H0, W1, H1, C1, R13, L1, L7, L4, L6,
L2, L5, L3, X3, X2, X1, M1; the T/R rows are geometry and PURPOSE). S1: four wordings, the first two with
`{script} crawl` and `runs = ["crawl_help"]`, the last two without the command and with no probe, as the row says.
S2: `waits = "release"`. F1: first wording carries `{const:THROTTLE_THRESHOLD_MS}`, the second `{field:max_inflight}`,
both `runs = ["crawl_ctrl_c"]`. H0: `runs = ["robots_stall", "robots_resume"]`, then the code-only twin, then `""`
on `fails = ["robots_stall"]`. W1: `drawn = false`, `runs = ["export_after_kill"]`, `fails = ["kill_writes_file"]`,
fallback "logged to disk, then saved to redb, in batches". H1: `runs = ["crawl_ctrl_c", "quiet_after_last_page",
"quiet_slow_page"]`, `fails = ["ends_by_itself"]`, then a one-probe twin, then `""` on `runs = ["ends_by_itself"]`.
C1: `runs = ["crawl_ctrl_c", "second_ctrl_c"]` and a one-probe fallback; neither names `ends_by_itself`. R13: `runs =
["crawl_ctrl_c"]` (`chart.toml:1041`). R0: `header_runs = ["crawl_ctrl_c"]`. M1: `gate = "cargo"`, `fails =
["ends_by_itself"]`. `[[handoffs]]` at `:1443` and `:1463`. `crawl_delay_obeyed` is named at `:1080, 1155, 1160` and
its comment at `:1074` says "not written yet"; `resume_after_kill` appears only in the comment at `:900`.

**§5.4 against the resolver.** I re-ran every flip through `tests/test_round13.resolved` (`scripts/data/route.py
resolve()` on today's `stats.json`): `ends_by_itself` passing → H1 `""` retired, M1 `""`, **C1 unchanged** ("press
Ctrl-C once and wait for `Saved to`…"); `ua_seen` failing → L7 `verified = False`; both export probes failing → X1
`verified = False`; `sitemap_keeps_disallowed` alone failing → X1's wording 2 ("every page", the "and disallowed"
clause gone); `kill_writes_file` passing → W1 "logged to disk, then saved to redb, in batches"; `robots_read` passing
and `robots_stall` failing → H0 `""`, L6 `""`, L4 "Until a host's `robots.txt` is back, it fetches that host's pages,
disallowed ones too. It ignores `Crawl-delay`." (the https clause dropped). Every "Needs here" cell reproduces.

**§6's counts.** `stats.json` `runcheck.rustmapper.steps`: 25, 7 with `gate: true` (venv, install, help,
crawl_help, export_help, crawl_ctrl_c, export) and 18 probes in the order §6 lists them; `runcheck.py:696–699` sets
`steps[-1]["skipped"] = True` on a probe that cannot run; `runcheck.py:8` still says "four behaviours". 17 of 18
probes are named by some `runs`/`fails` in the entry walk above; `resume_after_kill` by none. `python3 -m unittest`
→ "Ran 539 tests in 20.1s OK"; a loader walk gives `test_approaches` 19 + `test_chartlib` 22 + `test_supporting` 24
+ `test_timeline` 26 = 91 off-page, 448 product. The gate: `check.py --tier fast` on the tree as committed → "FAIL
(exit 1) · 4599 fail · 8 warn" (§10.7); `build_assets.py && render_readme.py --check && check.py --tier fast,render`
→ "pass with warnings (exit 2) · 0 fail · 4 warn · 0 error"; the build dirtied `assets/build-report.json` and I
restored it with `git checkout --`. The weekly job: `gh api …/actions/workflows/profile.yml/runs` → 12 runs, all on
`main`, the latest `schedule`, `failure`, `2026-10-11T12:52:59Z`; `origin/main` is `d253286` by `github-actions[bot]`;
`git rev-list --count origin/main..027f081` = 23. All as §0, §6 and §8.5 say.

**§8.2 against `gate.txt`.** The four WARN lines are `log.shards`, `POSITION-EMPTY`, `LICENSE-FLAGSHIP`,
`ROUTE-WAITING … S2`; "fast log 2 finding(s)"; `frames` emits one info in the render tier. My own run printed the
same four and nothing else. §8.2 is exact.

**Line cites.** 90 `file:line` cites resolved by script; every one lands on the line or symbol the PRD names beside
it. Two land on docstring prose rather than code (`render_readme.py:697` and `:740`, the M1 sentences inside the
`text_blocks` and install docstrings); they state the rule, so they serve, but the symbol to name is `text_blocks`
(`:694`).

## 4. The other direction: what the code holds that the register does not say

**Tests whose trailing comment names a gate code, and the code's row says "gate" alone** (the list is mechanical:
every `test_` function whose comment carries a `T-…` id or a `WORD-WORD` code; 25 such tests, 8 of them cited by
neither name nor line):

| Test | Comment | §7 row that says "gate" only |
|---|---|---|
| `test_lines_are_painted_under_the_marks` (`test_route.py:971`) | ROUTE-PAINT | §7.4 height/paint row (line 370) |
| `test_loop_arrow_is_on_bare_line` (`:1002`) | ROUTE-ARROW | the same row; G1a's holder cell (line 104) says "gate (ROUTE-ARROW…)" |
| `test_release_label_follows_its_command` (`:984`) | ROUTE-RELEASE | §7.5 release-label row (line 393) |
| `test_code_spaces_are_word_spaces` (`:1013`) | ROUTE-CODE-SPACE | §7.5 code row (line 392) names a different test |
| `test_code_is_in_the_code_face` (`:1036`) | TYPE-CODE on the build | the same row |
| `test_code_face_and_self_twice` (`:620`) | TYPE-CODE, HERO-SELF-TWICE | §7.2 one-home row (line 321): "gate" |
| `test_label_only_when_the_file_is_anchored_in_both` (`:394`), `test_handoff_reader_label` (`:609`) | ROUTE-LABEL | §7.3 both-trees row (line 331) and §7.5 code row name ROUTE-LABEL with one other test |

These eight run on the committed build and on fixtures every `unittest` run, so the rule is held twice and the
register says once. MF2.

**Tests that hold a rule the register states nowhere, or states with a weaker holder:**

| Test | What it pins | Where it belongs |
|---|---|---|
| `test_order` (`test_round7.py:105`) | the Languages line's rest is ordered by repository count (Go, two repositories and 15 lines, before C, one repository and 99 lines) and a lead language no repository has is dropped | §5.3 row 3 and §10.15 say "no test" for the order by count. **Wrong.** MF1 |
| `test_fold_label_names_the_largest_group` (`test_round12.py:224`) | the "15 more repositories" `<summary>` leads with the largest group and names every group; every repository in the fold is in a group | §5.3 row 9 states only "the count is computed" |
| `test_no_folded_item_in_the_open_list` (`test_round13.py:156`), `test_no_label_no_fold` (`:178`) | a `fold = true` entry never prints in the open list; without `fold_lead` there is no `<details>` | §5.3 row 6's fold clause |
| `test_install_block_says_how_it_ends` (`test_route.py:443`) | the code block's exact lines, including the three stop-rule comments and the blank-rows grep | §5.3 row 6 and §10.16: the ≤ 32-column rewording §10.16 proposes must edit this test |
| `test_m1_says_what_main_fixed_only_on_its_evidence` (`:673`) | M1 prints only on the `cargo` gate and never names an idle timing | §5.3 row 6's M1 clause names `render_readme.py:697, 740` and no test |
| `test_h1_names_the_release` (`:726`) | H1 begins with `edition.version` | §5.1 H1 |
| `test_no_period_wording` (`test_round7.py:196`) | W1 never says "every N ms" | §5.1 W1 |
| `test_more_count_is_computed` (`test_proof.py:179`) | `more_count` = `repo_count` − profile − facts − Also | §5.3 row 9 cites the function, not its test |
| `test_committed_readme_has_no_bare_figure` (`test_proof.py:137`) | the committed README runs through `figures_check` in the suite | §7.3 FIGURES row: "gate" → "gate, test" |
| `test_failed_runcheck_hides_the_entrance` (`test_route.py:1069`), `test_runcheck_gate_ignores_probes` (`:225`) | a failed gate step hides R2; a failed probe does not | §7.3 entrance row: "gate, CI" |
| `test_phone_height_holds_at_851` (`test_round15.py:295`) | `drawn_h(phone, 851) ≤ TALL_PX`; W1 undrawn; H0 one line; the danger marks are H0 and H1 | §7.4 one-screen row: "gate (render)" |
| `test_today_warns_once` (`test_round15.py:155`) | ROUTE-WAITING fires exactly once, at `warn`, naming S2 | §8.2's ROUTE-WAITING row |

MF5 folds these in. None was raised by rounds 4 or 5 (their lists are applied; I checked `LOG.md`).

**Owner sentences against the register.** I read all 21 messages against §3 and appendix D. Every rule-shaped
sentence has a row. The two that round 5 named as carried by implication (9 Oct 11:32 *"you can spend some time
looking at it"*, G1a; 7 Oct 16:12 *"about 2 hours"*, process, overtaken) still are, and can stay so. One sentence
of 9 Oct 11:35 is carried in halves: *"the images and the text need to kind of like either differentiate themselves
a little bit, or don't go too far into the ship theme"*; G6 quotes the first alternative and G2/G13a hold the second,
which is the right split. Nothing to add.

**Status cells for process rows.** Appendix D's "Every open PR is mergeable… process, not met today" is right.
"At least 10 reviews… process, done" is right (16 product rounds in `docs/crit/round6/`). But §0's stop rule and the
header's "Next step, in order" describe a sequence this round broke, and no process row records it. MF4.

## 5. Research: how projects make documentation claims verifiable, and whether the PRD states enforcement at the right level

Twelve outside sources read this round (list at the end), chosen to be different from rounds 4 and 5's (Go examples,
Sphinx `literalinclude`, Cog, embedme, Kubernetes verify scripts, sphinx-needs, Doorstop, OpenFastTrace, kernel-doc;
rustdoc, `doctest`, Sphinx doctest, ExUnit, mdBook, cargo-rdme, MkDocs strict, Write the Docs, Specification by
Example, Cucumber, Concordion, ArchUnit). They fall into the same three patterns, and add a fourth that matters here.

1. **Examples in prose are executed.** pytest collects `test*.txt` for doctests by default and `--doctest-glob`
   extends that to other files [1]; byexample runs the snippets in Markdown "as regression tests" and "will compare
   the output of the examples with the expected ones and it will show any difference" [2]; pytest-examples collects
   examples "in docstrings and markdown files", runs them, and "check[s] print statements are inlined correctly" [5].
2. **Generated text is regenerated in CI and the diff fails the build.** terraform-docs has `--output-check`, "check
   if content of output file is up to date" [3]; templ's CI runs `templ generate` then `git diff --exit-code`, "If any
   files have changed, then the pipeline should fail" [9]; gRPC's `vet.sh` runs `go mod tidy` and then `git status
   --porcelain … || (git status; git --no-pager diff; exit 1)` [10]; Go's protobuf repository fails its integration
   test on "stale generated files" [12]. oclif's `readme` command writes the commands section of a README from the
   CLI itself [8].
3. **The specification drives the test.** Schemathesis generates tests from the OpenAPI or GraphQL schema and
   "catches server errors, schema violations, and validation gaps that hand-written tests miss" [4]; Hilton's
   reading of living documentation: "reliable documentation, thanks to automated checks and manual reconciliation
   with its implementation", which "reconciles any differences between test scenarios and automated tests - two
   redundant knowledge representations" [11].
4. **Snapshots, reviewed by a person.** insta stores the expected output beside the test, writes a `.snap.new` on a
   mismatch, and `cargo insta review` lets a person accept or reject the change [6]; Sphinx's `linkcheck` builder
   "scans all documents for external links" and reports the broken ones [7].

**Judgement.** The PRD's enforcement claims are at the right *granularity*: a code, a level, a tier, a test, a file
and a line, the same things a doctest, a `--output-check` or a snapshot names. They are at the wrong *direction*:
every claim is a copy of the code made by hand and re-read by hand once a round. This round the copy is almost
exact in the forward direction (168 codes, every level, every tier, every test name, every §5.4 cell, every §8.2
warning, 90 line cites), and wrong in the reverse direction (eight tests with a code's name in their comment that no
row cites; a §10 gap that a test closed; ten more pinned rules the register calls "gate" or "code" or does not
name). That is exactly what the sources predict for a mirror nobody executes: the half that a hand check greps
for is right, the half it does not grep for drifts. §10.12 is the fix, and its spec already has pattern 2 (appendix
B written by the test, failing when the committed appendix differs). What it lacks is the reverse rule, which is
mechanical: every `tests/*.py` function whose trailing comment names a code is cited in that code's row (the 25
such tests are the list in §4). Pattern 4 is the right shape for §7's status column: a snapshot of (code, level,
tier, tests-that-name-it) that a person reviews when it changes, not a prose table. Until the test exists, the hand
check in `LOG.md` needs the two scripts in §6 added to it, because rounds 4 and 5's commands check the forward
direction only.

## 6. The hand check, as commands (run from `/home/user/wt-v12`)

```
ls scripts/checks/*.py | grep -v __init__ | wc -l                                              # 28
python3 -m unittest 2>&1 | tail -3                                                             # Ran 539 tests … OK
grep -ohE '"[A-Z][A-Z0-9]*(-[A-Z0-9]+)+"|"(data|log)\.[a-z_]+"' scripts/checks/*.py | sort -u | wc -l   # 169
grep -nE '\b(fail|warn|info|error)\(\s*f?"[A-Za-z]' scripts/checks/*.py                        # the level per code
grep -nE 'Finding\("(fail|warn|info|error)"' scripts/checks/data.py scripts/checks/log.py scripts/checks/motion.py
grep -nE 'error\("(PLUGIN|NO-)' scripts/check.py                                               # the runner's five
python3 -c "import json;s=json.load(open('assets/stats.json'))['runcheck']['rustmapper']['steps'];print(len(s),sum(x['gate'] for x in s))"   # 25 7
python3 -c "import sys;sys.path.insert(0,'scripts');from sheets import route;print(len(route.PURPOSE))"   # 17
python3 -c "import sys;sys.path.insert(0,'scripts');from checks import column;print(column.column_px(852))"   # 482
python3 scripts/check.py --tier fast | tail -1                                                 # committed report: 4599 fail
python3 scripts/build_assets.py && python3 scripts/render_readme.py --check && python3 scripts/check.py --tier fast,render | tail -5   # 0 fail 4 warn
git checkout -- assets/build-report.json
git ls-remote --heads origin v12/purpose                                                       # 9e3db34
gh api "repos/BenjaminSRussell/BenjaminSRussell/pulls?state=all&head=BenjaminSRussell:v12/purpose" --jq length   # 0
git diff --stat origin/main..HEAD -- scripts | tail -1                                         # 36 files
git diff --stat origin/main..HEAD -- scripts chart.toml .github | tail -1                      # 38 files
```
The reverse-direction scripts (new): (a) for every `test_` function in `tests/*.py`, print `file:line name` and the
trailing `# …` comment, and flag the ones whose comment carries `T-[A-Z]+` or `[A-Z]+-[A-Z-]+` and whose name is not
in `docs/PRD.md` (8 today); (b) for every `` `path:line` `` in `docs/PRD.md`, print the line's text and the nearest
`def`/assignment above it (90 cites; all resolve). The probe-flip script is round 5's: load `tests/test_round13`,
deep-copy `stats["runcheck"]["rustmapper"]`, set a step's `ok`, call `resolved(stats, rc)` and read `text` /
`verified` / `retired` / `wording` per entry.

## 7. Must-fixes, ranked

**MF1 (PRD).** §5.3 row 3 (line 204) and §10.15 (line 746). The row says "the order of the rest by count: no test
(§10.15)" and §10.15 says "nothing pins 'then by repository count, then by lines'". `test_order`
(`tests/test_round7.py:105`) pins the count order: a fixture with Go on two repositories (15 lines) and C on one (99
lines) must print "Swift; Go, C", and a lead language no repository has ("Rust is no repository's: left out") is
dropped. What nothing pins is the two tie-breaks in `languages_line` (`render_readme.py:162`, key `(-count, -lines,
name)`): equal counts by lines, then by name. Change row 3's holder to "`tests/test_round7.py:91` (the set, and
"Python, Rust; " first); `test_order` (`:105`: the rest by repository count; a lead language with no repository
dropped); the lines and name tie-breaks: no test (§10.15)" and §10.15's gap to "the tie-breaks (equal counts by
lines, then by name) are untested: one assertion over a fixture with two equal counts". Why: §7.3's own rule, every
claim about the code rests on the code; this one rests on a reading that stopped at line 91.

**MF2 (PRD).** Seven codes whose rows say "gate" are also held by tests on the committed build, named in the tests'
own comments (§4's first table): add "test" and the test to §7.4's height/paint row (line 370: `test_lines_are_painted_under_the_marks`,
`tests/test_route.py:971`; `test_loop_arrow_is_on_bare_line`, `:1002`), §7.5's release-label row (line 393:
`test_release_label_follows_its_command`, `:984`), §7.5's code row (line 392: `test_code_spaces_are_word_spaces`,
`:1013`; `test_code_is_in_the_code_face`, `:1036`; `test_label_only_when_the_file_is_anchored_in_both`, `:394`;
`test_handoff_reader_label`, `:609`), §7.2's one-home row (line 321: `test_code_face_and_self_twice`, `:620`, for
HERO-SELF-TWICE), and G1a's holder cell (line 104: ROUTE-ARROW is "gate, test"). Then §10.12's Fix cell gains the
mechanical rule that would have caught all eight: "every `tests/*.py` function whose trailing comment names a code
or a T-id is cited in that code's row". Why: §7's preamble promises that the status column is "what the holder did
on the round-16 build"; a rule held by a gate and a test is held twice, and the document says once. Sources [9],
[10], [11]: the register is reliable only in the direction something checks it, and nothing checks this one.

**MF3 (PRD; and a process item).** §10.17 (line 748), appendix D's PR row (line 925) and §0 (line 43). The reason
given for the missing PR, "the fix passes do not push, so a session with push does it, or Ben", is not true of the
product: `git ls-remote --heads origin v12/purpose` → `9e3db34`, which is `027f081` plus the PRD's first commit, so
every product file has been on `origin` since before round 1; `git rev-list --count origin/main..HEAD` = 29, of
which the five PRD-round commits (`e17cc80`…`b6cca2c`) are docs only and local. A PR needs the head on the remote,
not the reviewer's commits, so `gh pr create --head v12/purpose` has needed no push for five rounds. Change §10.17's
Fix cell to "the branch is on `origin` at `9e3db34` with every product file; `gh pr create --head v12/purpose` needs
no push; open it before the fix round so the four items land in it" and drop "the fix passes do not push" from
appendix D's row and from `LOG.md`'s round-2 decline. Why: 8 Oct 09:04, *"all PRs need to be ready to merge"*; a
rule stated as unmet for a reason that does not hold is a status cell that is wrong.

**MF4 (PRD).** Header (lines 3–7) and §0's last bullet (lines 42–48). The stop rule reads "no PRD round 6 until a
fix round has done §8.1 items 7 and 8, §10.19 and §10.23 and the branch has a PR"; this is PRD round 6, `git diff
--stat 027f081..HEAD -- . ':!docs'` is empty, and the PR count is 0. Either the rule binds and the document records
that it was broken (a process row in appendix D: "no PRD round before the fix round | process, **not met**: round 6
ran on 11 Oct with no product change"), or it does not bind and the sentence goes. Keep the rule, add the row, and
change the header's "Next step, in order" to say the fix round is now overdue by one round. Why: his 11 Oct
sentence, *"ensure this is something I want to see rounds of reviews and research"*: a document whose process
claims are not what happened cannot ensure anything; appendix D's own row "Report failures as they are".

**MF5 (PRD).** Fold the unregistered rules of §4's second table into the register, one cell each: §5.3 row 9 gains
"the `<summary>` leads with the largest group and names every group; every folded repository is in a group
(`test_fold_label_names_the_largest_group`, `tests/test_round12.py:224`); `test_more_count_is_computed`
(`tests/test_proof.py:179`)"; §5.3 row 6 gains "a `fold = true` entry never prints in the open list and no `fold_lead`
means no fold (`test_no_folded_item_in_the_open_list`, `tests/test_round13.py:156`; `test_no_label_no_fold`, `:178`);
the code block's lines are pinned by `test_install_block_says_how_it_ends` (`tests/test_route.py:443`); M1 by
`test_m1_says_what_main_fixed_only_on_its_evidence` (`:673`)"; §10.16's Fix cell names `test_route.py:443` as the
test the rewording edits; §5.1 H1 gains `test_h1_names_the_release` (`:726`) and W1 `test_no_period_wording`
(`tests/test_round7.py:196`); §7.3's FIGURES row becomes "gate, test" with `test_committed_readme_has_no_bare_figure`
(`tests/test_proof.py:137`); §7.3's entrance row becomes "gate, test, CI" with `test_failed_runcheck_hides_the_entrance`
(`tests/test_route.py:1069`) and `test_runcheck_gate_ignores_probes` (`:225`); §7.4's one-screen row gains
`test_phone_height_holds_at_851` (`tests/test_round15.py:295`); §8.2's ROUTE-WAITING row gains `test_today_warns_once`
(`tests/test_round15.py:155`). Why: round 5's MF4 did the same for ten tests and was applied; these twelve are the
rest of what a walk of the 462 test functions finds, and a reviewer asked at §8.3 q.3 and q.4 to judge the fold, the
code block and the phone height is not told a test already pins each.

**MF6 (PRD).** Two printed numbers do not reproduce by the command printed beside them. §8.6 order B (line 572):
"`git diff --stat main..HEAD -- scripts`: 38 files" gives 36 against `origin/main` (`d253286`, the `main` the PRD
names everywhere else); 38 is `-- scripts chart.toml .github`, the command `LOG.md` round 4 ran. The worktree's local
`main` is stale (`LOG.md` round 5 says so), so every `main..` command in the PRD should read `origin/main..`. §0's
first bullet (line 28): "515 lines, 9335 words" for §1, 2, 4, 5, 8, 9 and 11 by `wc` split at `## ` headings gives
515 lines and 9,372 words when run (the split script is in §6); print the number the method gives or name the
method that gives 9,335. Why: §7.3's first rule, nothing printed that was not measured, applies to the document's
figures about itself.

Not a must-fix: `render_readme.py:697, 740` point at docstring sentences (name `text_blocks`, `:694`, beside them);
`runcheck.py:8`'s "four behaviours" (§10.18, product); `test_readme_words` (`test_round6.py:318`) is not a theme-word
test, so §10.1 stands as written; the `frames` info line in `gate.txt` (appendix B's "idle" is accurate enough).

## 8. Score

**7 / 10.** The forward direction reproduces: 28 plug-ins, 539 tests, 25 steps, 17 PURPOSE rows, 168 codes, every
level, every tier, every test name at its line, every §5.4 cell under the resolver, every §8.2 warning, 90 line
cites, 12 workflow runs, PR #17's state. What is wrong is the reverse direction, which no hand check so far has run:
eight tests that name a code in their own comment and are cited nowhere, a §10 gap that a test at line 105 of the
file the PRD cites at line 91 had closed, twelve pinned rules the register calls "gate" or does not name, a PR
withheld for five rounds on a reason that was false from round 1, and a stop rule the round itself broke. The
answer to his 11 Oct sentence is still reviewer 2's from round 4: six PRD rounds have changed no product file; the
one product change that ends this class of finding is §10.12, and MF2 says the rule it must add.

## Sources

Outside, read with WebFetch or WebSearch this round:

1. pytest, "How to run doctests" — https://docs.pytest.org/en/stable/how-to/doctest.html — "By default, pytest will collect `test*.txt` files looking for doctest directives"; `--doctest-glob` "can be given multiple times"; `--doctest-modules` runs docstring examples.
2. byexample — https://byexamples.github.io/byexample/ — "write snippets of code in your documentation and execute them as regression tests"; "will compare the output of the examples with the expected ones and it will show any difference"; Python, Ruby, Shell, Go, Rust and others in one file.
3. terraform-docs CLI reference — https://terraform-docs.io/reference/terraform-docs/ — `--output-check`: "check if content of output file is up to date (default false)".
4. Schemathesis — https://schemathesis.readthedocs.io/en/stable/ — "automatically generates property-based tests from your OpenAPI or GraphQL schema"; "Catches server errors, schema violations, and validation gaps that hand-written tests miss"; each finding with a reproducing curl.
5. pytest-examples — https://github.com/pydantic/pytest-examples — "Pytest plugin for testing Python code examples in docstrings and markdown files"; lints with ruff and black; "check print statements are inlined correctly"; `--update-examples` rewrites them in place.
6. insta, quickstart — https://insta.rs/docs/quickstart/ — new snapshots "stored next to the old ones with the extra `.new` extension"; `cargo insta review` "will let you interactively review them"; inline snapshots updated on review.
7. Sphinx, builders — https://www.sphinx-doc.org/en/master/usage/builders/index.html — `linkcheck` "scans all documents for external links" and writes the broken and redirected ones to `output.txt`; the `doctest` builder runs the documentation's doctests when the extension is on.
8. oclif — https://github.com/oclif/oclif — `oclif readme`: "Adds commands to README.md in current directory".
9. templ, "CI/CD" — https://templ.guide/developer-tools/cicd — `templ generate` then `git diff --exit-code`; "If any files have changed, then the pipeline should fail".
10. grpc-go, `scripts/vet.sh` — https://raw.githubusercontent.com/grpc/grpc-go/master/scripts/vet.sh — `go mod tidy -compat=1.26` then `git status --porcelain 2>&1 | fail_on_output || (git status; git --no-pager diff; exit 1)`.
11. Peter Hilton, "Living documentation principles" — https://hilton.org.uk/blog/living-documentation-principles — "reliable documentation, thanks to automated checks and manual reconciliation with its implementation"; "it reconciles any differences between test scenarios and automated tests - two redundant knowledge representations".
12. Go protobuf, `integration_test.go` — https://go.googlesource.com/protobuf/+/refs/tags/v1.29.1/integration_test.go — read as a search result (WebSearch, query "CI git diff --exit-code verify generated files"): the integration test runs the generators and fails on "stale generated files". The StrictDoc pages (https://strictdoc.readthedocs.io/en/stable/, https://github.com/strictdoc-project/strictdoc) were fetched and said only "Software for technical documentation and requirements management"; not used for a claim.

Repository files opened (paths from `/home/user/wt-v12`): `docs/PRD.md` (whole); `docs/crit/prd/owner-messages.md`
(whole); `docs/crit/prd/LOG.md` (whole); `docs/crit/prd/review-r05-3.md` (whole, for what not to repeat);
`scripts/check.py:1–60, 82–83, 115, 202, 234–238, 246, 254, 272–300, 331–344`; every `scripts/checks/*.py`
(docstring, `TIER`, code literals, emit levels by grep; `alt.py:20–55`, `bounds.py:56, 85`, `boxpad.py:3–7, 48–50`,
`column.py:45–50, 231`, `data.py:53–96`, `design.py:7–31`, `expiry.py:37–42`, `log.py:36, 47–69`, `motion.py:129,
278`, `readme.py:10, 28, 32, 89, 104, 121, 247, 304–337`, `route.py:41, 58, 60–62, 70, 77–78, 200–214, 265–342`,
`size.py:5, 46, 56, 70`, `strings.py:24–48, 68, 99, 147`, `xml.py:82`); `scripts/runcheck.py:1–55, 589, 696–705,
866–876, 964–980, 1181–1197`; `scripts/sheets/route.py:67, 73–74, 126, 799` and `PURPOSE` printed; `scripts/data/route.py:59,
230–240`; `scripts/render_readme.py:43–52, 146–165, 398, 459, 670–671, 694–699, 738–742, 860, 925, 1017, 1181`;
`scripts/tokens.py:59, 73–74, 117, 131–133`; `scripts/build_assets.py:59–60`; `scripts/build_stats.py:510–518`;
`scripts/publish_chart.py:1–16, 81, 150–162`; `.github/workflows/profile.yml:13, 22–27, 72–74, 106, 133, 142, 153,
160, 168, 174, 189–191`; `chart.toml` (`[route.rustmapper]` walked whole with `tomllib`; lines 9, 13, 24–39, 96, 563,
667, 900, 1041, 1074–1160, 1257, 1419, 1443, 1463; `[copy]`, `[facts]`, `[alt]`, `[position]`, `[contact]`);
`assets/stats.json` (`runcheck.rustmapper.steps`); `README.md:7–13, 38, 86, 151`; `DESIGN.md:21`;
`docs/BEN-TODO.md:16, 34–36, 39`; `tests/` (all 462 test functions by `ast`; `test_route.py:93, 107, 225, 267, 375,
386, 394, 417, 443–460, 485, 517, 527, 558, 569, 576, 609, 620, 673–690, 726–740, 780–811, 812–829, 832, 842–870,
871, 894, 935, 953, 971, 984, 1002, 1013, 1030, 1036, 1052, 1069`; `test_round6.py:88, 281–335`;
`test_round7.py:71–125, 191–203, 367, 391`; `test_round8.py:212–230, 354–368`; `test_round12.py:124, 208, 216,
224–250, 270`; `test_round13.py:36–66, 156–190, 258`; `test_round15.py:124, 155–166, 193, 277–292, 295–312`;
`test_round16.py:85, 131–146, 283–300`; `test_pipeline.py:47, 208, 211–223, 246–253, 254, 274, 296, 307–330, 405–420,
488–512, 553`; `test_proof.py:137–148, 158, 179–186, 200, 235–250`; `test_data.py:83, 199, 212, 225, 359, 498`);
`git show d253286:README.md` lines 6–13; the renders `round-16/sheet-phone-day-390.png`, `page-desk-1.png`,
`page-phone-1.png`, `page-phone-2.png`, `gate.txt`, `build/build-report.json`.
