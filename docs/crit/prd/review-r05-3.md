# PRD review round 5, reviewer 3: An engineer who trusts nothing the PRD says until the code says it too

11 Oct 2026. Document: `docs/PRD.md` at `0a557ff` (baseline `027f081`; `git diff --stat 027f081..HEAD -- . ':!docs'`
is empty, so every line number the PRD cites was checked against the tree as it stands). Renders:
`scratchpad/r6/build/round-16/` (`sheet-phone-day-390.png`, `page-desk-1.png`, `page-phone-2.png`, `gate.txt`
opened). Everything below that says "verified" is a command I ran or a line I opened; the commands are in §6.

## 1. Is the product this PRD defines something he wants, by his own words?

**Yes.** The sentence that decides it is 9 Oct 20:50: *"Everything, single thing inside of this needs a purpose, not
a fucking chasing a reason"*, with 11:37 as its test, *"The map, very helpful. The fucking log, not really... It has
to be helpful knowledge."* The code says the same thing the PRD says: `scripts/sheets/route.py PURPOSE` has 17
rows, §5.1 has 17 rows, the ids and the Q tags agree one for one (T1 Q1, T2 Q1, R0 Q2, R1 Q4, R2 Q4, R5 Q4, R6 Q1,
S1 Q5, S2 Q1, F1 Q1, H0 Q5, W1 Q5, H1 Q5, C1 Q5, R12 Q4, R13 Q4, R15 Q2), ROUTE-PURPOSE (`checks/route.py:337`)
refuses a drawn group with no row, and the phone sheet (`sheet-phone-day-390.png`) draws nothing that is not in that
table: a name, a role, a project line, an install line with its date, a track, a loop, four steps, a dotted box with
two catches, a stop, a file and a hand-off. For the document itself, 11 Oct 01:12 (*"review all of the do and donts
and specifically all of the rules that must be followed and review how they are implemented"*) is met in form: every
rule has a holder column, and this round I could check 168 of the holders against the code. Where the column is
wrong is §4.

**§8.3 q.1, first line (G3a), written before re-reading §1 or §5.1:** the image shows a crawler called rustmapper,
installed with `pip install rustmapper`, started with `rust_sitemap crawl`, looping over pages until you press Ctrl-C
once, and writing `data/sitemap.jsonl`. It names a tool, a way to start it and an output.
**§8.3 q.6:** yes, I would screenshot it; I would call it "install notes drawn as a route" (the same words as my
round-2 answer). Third line (G1d): the care shows in one left edge for every row, the release's own date beside the
install line, the real field names on the file row, and the gap in the track under the box; I did not see it in
decoration, because there is none.

## 2. Section 7 and appendix B, row by row, against the plug-ins

Method: `grep -ohE '"[A-Z][A-Z0-9]*(-[A-Z0-9]+)+"|"(data|log)\.[a-z_]+"' scripts/checks/*.py | sort -u | wc -l` →
169 (the PRD's number); per plug-in, an `ast` walk printed each file's docstring, `TIER` and code literals; a second
grep printed the level (`fail` / `warn` / `info` / `error`) each code is emitted at.

**Appendix B: every row holds.** 28 plug-ins (`ls scripts/checks/*.py | grep -v __init__ | wc -l` = 28). Tiers: `boxpad`,
`column`, `wrap`, `frames` carry `TIER = "render"`; `perf` carries `"perf"`; `data.py` and `log.py` have no `TIER`
and `check.py:234` defaults them to fast; the other 21 say `"fast"`. Every code listed under a plug-in is a literal in
that file, and no plug-in emits a hyphenated code the row omits (alt 5, bounds 6, column 3, contrast 8, data 15, expiry
3, notices 4, position 9, readme 15, route 21, size 11, strings 8, xml 12, flash 4, frames 9, legend 6, motion 10,
perf 4). The three non-codes the preamble names (`YYYY-MM`, `YYYY-MM-DD`, `log.json`) are at `expiry.py:37`,
and `log.py:36`; `FIGURES` and `TYPE` are at `figures.py:93–104` and `type.py:35`; the bare `MOTION`, `FRAMES`,
`LEGEND`, `PERF` at `motion.py:124`, `frames.py:47`, `legend.py:62`, `perf.py:76`. So 169 − 3 + 2 = 168 reproduces.

**What the grep cannot see, and the register does not carry (new):** `check.py` itself emits four codes, all at
level `error` (exit 3): `PLUGIN-RESULT` (`check.py:115`, a plug-in returned something that is not a Finding),
`PLUGIN-IMPORT` (`:246`), `PLUGIN-CRASH` (`:254`) and `NO-SHEETS` (`:286`, "run build_assets.py first"). They are
outside `scripts/checks/`, so outside the preamble's method, and in no row of §7 or appendix B. §6.1's second row
("a gate fails (exit 1 or 3)") is the place a reader would look for what exit 3 means, and it does not say. MF3.

**§7 statuses, checked against the level each code is emitted at.** 168 codes; four rows state a level the code
does not have:

| Row (line) | Says | Code says |
|---|---|---|
| §7.5 alt row (385) | ALT-LONG, ALT-THE, ALT-LAST, ALT-POEM are gate; only ALT-NO-README is marked warn | `alt.py:50`: `warn("ALT-POEM", "alt poem differs from chart.toml alt_poem…")`. The "last sentence equal to `[alt] alt_poem`'s hero line" half of the rule is a warning, never a fail. The test half: T-ALT (`test_route.py:832–840`) asserts ≤ 25 words, not "The", three substrings and the prefix "How to install"; it never reads `alt_poem`. `test_pipeline.py:553` asserts the poem's length only. So that clause is held by nothing that fails. MF1 |
| §7.4 overlap row (363) | BOUNDS-COLLIDE, -EDGE, -EXCLUSION, -MORE, -TEXTURE, -NO-MANIFEST: gate | `bounds.py:56` `warn("BOUNDS-NO-MANIFEST", "no text manifest in the report; bounds not checked")` and `continue`; `bounds.py:85` `warn("BOUNDS-TEXTURE", …)`. NO-MANIFEST is the one that matters: a sheet whose report entry has no `text[]` is skipped with a warning, so every BOUNDS fail depends on the manifest being there. MF2 |
| §7.4 budget row (364) | REPORT-SHA, -BYTES, -MISSING, -ORPHAN, -STATS: gate; SIZE-TARGET (warn) | `size.py:56` `warn("REPORT-BYTES", …)`. MF2 |
| §7.4 XML row (365) | XML-SET-LOOP listed with the fails (marked idle) | `xml.py:82` `warn`. Idle today; the mark is still wrong |

Every other level the PRD states is right, including the ones a reader would doubt: ROUTE-WAITING warn (`route.py:265`),
ROUTE-PROBE-SKIPPED warn (`:275`), ROUTE-HANDOFF info (`:296`), LICENSE-FLAGSHIP warn (`readme.py:89`), CI-GATES warn
(`:104`), README-MISSING and README-RENDER warn (`:279`, `:337`), POSITION-EMPTY and POSITION-STALE warn
(`position.py:31`, `:56`), EXPIRY-* all warn (`expiry.py:37–42`), SIZE-TARGET warn (`size.py:46`), `data.calendar`
warn at `data.py:62` and info at `:69`, `data.tide`/`data.variation` fail (`:84`, `:87`), `log.computed` info (`log.py:53`),
`log.version`/`log.shards` warn (`:65`, `:69`), FLAG-WRAP info/error/fail (`wrap.py:98–105`). The `data.seeded`,
`.provenance`, `.schema`, `.invariant` split is computed from the error text at `data.py:56–58`, all fail, as §7.3 says.

**§7.1.** THEME_WORDS (`checks/route.py:60–61`) is exactly the 18 words the first row lists, `survey` among them;
`design.py:18 EXTRA_WORDS` holds `survey`, `unsurveyed`, `ship's`. The README-prose row is right to say "review
only": no plug-in greps README prose for THEME_WORDS (`strings.py` scans BANNED phrases, not theme words). The
`[copy]` row's five keys are at `chart.toml:35–39`. The "no ships" row's description of T-PURPOSE matches
`test_route.py:812–829` (ids set, `want = ids - {"S2", "W1"}` at `:821`, the `^Q[1-5]$` regex at `:829`).

**§7.2.** ROUTE-PURPOSE one-way: `route.py:337` fails "element … is drawn but has no PURPOSE row" and nothing in the
plug-in walks the table the other way. T-NOSIZE `test_route.py:780`, T-SAME `:807` (named by test name in §7.3, its
id T-SAME is the one T-id in the tests the PRD never prints; harmless). STRINGS-TWICE/-COUNT fail (`strings.py:173, 176`).

**§7.3.** Every test named exists (32 of the 45 `test_*` tokens in the PRD are test names; the other 13 are module
names, `test_functions` the stats key, `test_prd` the proposed file, and the two `main`-branch v11 tests of §8.5).
`test_every_committed_conditional_wording_has_a_probe_or_producer` at `test_round6.py:88`, `CONDITIONAL` at
`scripts/data/route.py:59`, `producers()` at `:236`, REPO-SET docstring at `repos.py:3–5`, README-SUBCOMMAND fail
(`readme.py:324`), NOTICE-* all fail (`notices.py:36–61`, `notices_live.py:27`), the position codes as listed. The
"Figures retire by themselves" row's caveat is right (§3 below re-ran the flips).

**§7.4.** `column.py:45, 47, 48, 50, 231` hold `MIN_PX = 11.0`, `TALL_FROM = 768`, `TALL_PX = 900.0`,
`DESK_MIN_PX = 14.5`, the `breakpoint_px` read; `tokens.py:73–74 FLOORS` (desk 19/16/25, phone 26/18/30);
`tokens.py:131 BUDGETS` (300/100/3000/120/250); `checks/route.py:70 HEIGHT` (770/1246/964); `publish_chart.py:81
unshipped`; `test_round15.py:193`, `test_round12.py:124`. The left-edge row says "gate" only; a test holds it too
(`test_one_left_edge_and_desk_files_left_of_the_track`, `test_route.py:953`). See §4.

**§7.5.** README-CD at `readme.py:247` (docstring) and fail at `:326`; README-LICENSE `:313`; `test_first_mention`
`test_round7.py:367`, `test_one_spelling` `:391`; `chart.toml:563 alt_poem`. The thesis-line row is right that nothing
bans the phrase: `strings.py BANNED` has no "wrong about itself" and `docs/BEN-TODO.md:39` still carries it.

**Appendix D** is process; the one checkable claim, `git log` trailers, holds on the last three commits.

## 3. §5.1, §5.4, §6 and §8.2 against the code

**§5.1 against `route.py PURPOSE` and `chart.toml [route.rustmapper]`** (19 entries: S1, S2, F1, H0, W1, H1, C1,
R13, L1, L7, L4, L6, L2, L5, L3, X3, X2, X1, M1; the T/R rows are geometry and PURPOSE only). Walking each entry and
its `instead` list: S1's four wordings are as the row says (two with the command and `runs = ["crawl_help"]`, two
without and no probe). F1's first wording carries `{const:THROTTLE_THRESHOLD_MS}` and the `absent = "current_permits >
MIN_PERMITS"` anchor (`chart.toml:829`); the second is what prints. H0: `runs = ["robots_stall", "robots_resume"]`,
then a code-only twin, then `""` on `fails = ["robots_stall"]`. H1: `runs = ["crawl_ctrl_c", "quiet_after_last_page",
"quiet_slow_page"]`, `fails = ["ends_by_itself"]`, as the row says. W1: `drawn = false`; `runs = ["export_after_kill"]`,
`fails = ["kill_writes_file"]`; its fallback is the round-13 line. C1: `runs = ["crawl_ctrl_c", "second_ctrl_c"]` and a
one-probe fallback; neither names `ends_by_itself`. R13: `runs = ["crawl_ctrl_c"]`, which the row's "Drawn only when"
cell omits (it says "anchors hold"; one probe too). R0's `header_runs = ["crawl_ctrl_c"]` as the row says. R15's
hand-off is `[[handoffs]]` at `chart.toml:1443`, not under `[route.rustmapper]`; the row's "handoffs[] state runs"
is right. M1 (`kind = "ci"`) is an entry §5.1 cannot hold (not drawn) and §5.3 does not place; `render_readme.py:697,
740` put it after the cautions when its `cargo` gate holds. One line in §5.3 row 6 would close that (MF7).

**§5.4 against `runcheck.py` and the resolver.** `stats.json` carries 25 steps, 7 with `gate: true` (venv, install,
help, crawl_help, export_help, crawl_ctrl_c, export) and 18 probes, in the order §6 lists them. The probe dispatch
(`runcheck.py:870 PROBES` plus the inline calls at `:1117–1136` and the kill block at `:1140–1160`) produces exactly
those 18; `runcheck.py:8` still says "probes four behaviours". Which probes a wording names, from the walk: 17 of
18 are named by some `runs`/`fails`; `resume_after_kill` by none (its only mention is the comment at `chart.toml:900`);
`crawl_delay_obeyed` is named by L1's second wording (`:1080`) and L4's sixth and seventh (`:1155`, `:1160`) and is
no step. Both as §6 and §5.4 row 3 say. Re-running the resolver (`scripts/data/route.py resolve()`, through
`tests/test_round13.resolved`) with the probes flipped: `ends_by_itself` passing → H1 `""` retired, M1 `""`, **C1
unchanged** ("press Ctrl-C once and wait for `Saved to`…"); `ua_seen` failing → L7 `UNVERIFIED`; both export probes
failing → X1 `UNVERIFIED`; `sitemap_keeps_disallowed` alone failing → X1 drops "and disallowed"; `kill_writes_file`
passing → W1 "logged to disk, then saved to redb, in batches"; `robots_read` passing and `robots_stall` failing →
H0 and L6 `""`, L4 keeps its first wording. Every "Needs here" cell of §5.4 reproduces.

**§6's counts.** 28 plug-ins; `python3 -m unittest` → "Ran 539 tests in 22.2s OK"; a loader walk gives
`test_approaches` 19 + `test_chartlib` 22 + `test_supporting` 24 + `test_timeline` 26 = 91 off-page, 448 product;
25 run-check steps, 7 + 18. The gate: `check.py --tier fast` on the tree as committed → "FAIL (exit 1) · 4599 fail ·
8 warn" (§10.7); `build_assets.py && render_readme.py --check && check.py --tier fast,render` → "pass with warnings
(exit 2) · 0 fail · 4 warn · 0 error", the same four warnings as `gate.txt`; the build dirtied
`assets/build-report.json` and I restored it with `git checkout --`.

**§8.2 against `gate.txt`.** The four WARN lines are `log.shards`, `POSITION-EMPTY`, `LICENSE-FLAGSHIP`,
`ROUTE-WAITING [stats.json routes]: S2 …`; "fast log 2 finding(s)" is there (one warn, one info). §8.2 is exact.
`gate.txt` also shows `frames` emitting one finding in the render tier (the info at `frames.py:47`, "no motion: the
day edition is its own still"), so "idle" in appendix B means "fires nothing above info", which is fine.

## 4. The other direction: rules in the code that the register does not carry

**Tests holding a rule with no row** (471 distinct test names; the PRD names 32; the ones below assert a copy or
layout rule a reviewer would want to know is pinned):

| Test | What it pins | Where it belongs |
|---|---|---|
| `test_c1_has_no_colon_mid_sentence` (`test_round12.py:208`) | C1 prints "`Saved to`" without the tool's colon mid-sentence, while the anchor still tests `println!("Saved to: ` | §7.5, a copy row |
| `test_once_is_c1s_alone` (`:216`) | the word "once" appears in C1 and in no other route text | §7.5 |
| `test_pairing` (`test_round16.py:85`) | while H0 is drawn, H1 never says "done" (a stall one row up would make it false); no H1 wording says "done when" | §7.5 or §5.1 H1 |
| `test_trap_is_ringed_by_a_dotted_line` (`test_route.py:871`) | the trap group is a dotted accent line with no fill, with WCAG contrast on each theme | §5.1's "Trap text is ink inside a dotted accent line" sentence (held by nothing named) and §7.4's contrast row |
| `test_one_left_edge_and_desk_files_left_of_the_track` (`:953`) | the gate's `left_edge()` is clean on every edition and no file label sits left of the track | §7.4 left-edge row (add "test") |
| `test_no_edition_draws_file_labels` (`:1030`) | round 14: the side-by-side desk is retired | §7.5 ROUTE-LABEL row |
| `test_governor_is_a_clause_of_fetch` (`:935`) | F1's governor is a clause of the fetch row, never a row of its own | §5.1 F1 |
| `test_bots` (`test_data.py:83`), `test_charted_branches_drop_a_bots` (`:317`) | `is_bot` on "Claude" and "dependabot[bot]", bots dropped from branch counts | §7.3 agent-authorship row |
| `test_h1_takes_the_quiet_words_only_on_the_probe` (`test_route.py:267`), `test_probe_must_wait_as_long` (`test_round9.py:222`) | H1's "60 s" prints only from the probe, and the probe waits at least that long | §5.1 H1 |
| `test_twice_allowed` (`test_round10.py:166`) | the two STRINGS-TWICE exceptions | §7.2 one-home row |

Round 4 left the first four of these "for round 5 to fold into §7.1, §7.3 and §7.5 after reading each"; read, they
are MF4.

**Owner sentences that state a rule the register does not carry.** Appendix A quotes 7 Oct 15:30 whole, but G1's
cell starts at "world class": the first clause, *"This readme does not show an expert or high level smart person who
has a massive interest in design"*, is the premise of the brief and appears in no goal row; a grep of `PRD.md` for
"interest in design" and "expert" finds only appendix A. G1b ("what it says about the person who made it") and G1d
("months of work") are near it but neither asks whether a stranger would say the maker cares about design. MF6.
Two more sentences are carried only by implication and can stay so: 9 Oct 11:32 *"That misses a point of, like,
yeah, you can spend some time looking at it"* (G1a's second reading is the answer, but the sentence is not quoted
there) and 7 Oct 16:12 *"this should take about 2 hours"* (process, overtaken by his own 7 Oct 17:58). Every other
rule-shaped sentence in `owner-messages.md` has a row: I read all 21 messages against §3 and appendix D.

**Cites that drifted or point beside their subject.** Of 60 `file:line` cites resolved, 59 point at the line
named. §5.3 row 4 cites `test_pipeline.py:206–210` for the pick; 206–208 are the docstring and the picture link,
and the pick assertions (`use == "pick"`, `header_verified`, `no_services`) are at `:211–223`. MF7.

## 5. Research: how projects make documentation claims verifiable, and whether this PRD states enforcement at the right level

Twelve sources read (list at the end). They sort into three ways of keeping a document honest about code:

1. **The document is executed.** Python's `doctest` "searches for pieces of text that look like interactive Python
   sessions, and then executes those sessions to verify that they work exactly as shown" [2]; rustdoc's doctests
   exist so that "examples within your documentation are up to date and working", and an example that no longer
   compiles fails `cargo test` [1]; Sphinx's `doctest` builder "will collect them and run them as doctest tests"
   [3]; ExUnit "generate[s] tests from code examples found in `@moduledoc` and `@doc`" [4]; `mdbook test` runs a
   book's Rust blocks through rustdoc [5]. The common rule: a claim in prose that can be run is run, and a stale
   claim fails the build rather than waiting for a reader.
2. **The document is generated from the code, or checked against it, in CI.** `cargo rdme --check` exits 3 when the
   README no longer matches the crate docs, so "a stale README blocks the build" [6]; MkDocs `strict: true` turns a
   broken-link warning into a halt [7]; Write the Docs lists "automated tests" and blocking merges as the docs-as-code
   practices [8].
3. **The specification is the test.** Specification by Example holds that "when they are validated frequently, such
   documents are a reliable source of information" and calls the set "Living Documentation" [9]; Cucumber's aim is
   "system documentation that is automatically checked against the system's behaviour" [10]; Concordion regenerates
   the spec on every run and highlights each failing assertion, so "the specifications become trusted as an accurate
   source of reference" [11]; ArchUnit's "main focus is to automatically test architecture and coding rules, using any
   plain Java unit testing framework" [12], which is rules-in-a-document turned into rules-in-a-test.

**Judgement on the PRD's level.** The granularity is right: §7 names the code, its level, its tier, the test, the
file and the line, which is what a doctest or a Concordion spec names. The direction is wrong: every one of those
claims is a hand copy of the code, checked by a reader once a round (§0 says so), and the sources agree that a mirror
nobody executes is stale on the day it is written. The evidence is the PRD's own: four rounds, no code change, drift
found in every one, and this round four level cells and four runner codes that the round-4 hand check (which greps for
tokens and tiers, not levels) could not have caught. The right level for this register is pattern 2: appendix B and
§7's "Where" tokens generated from `scripts/checks/*.py` (code, level, tier) and from the test loader, with a
`--check` that fails when the committed document differs, exactly as `cargo rdme --check` and AUDIT-STALE already do
here for AUDIT.md. §10.12 is that item; its spec needs the level column added (MF5). Until it exists, the honest
status line is the one §0 has, and the 56-cite hand check should add the level grep from §6 below.

## 6. The hand check, as commands (run from `/home/user/wt-v12`)

```
ls scripts/checks/*.py | grep -v __init__ | wc -l                                            # 28
python3 -m unittest 2>&1 | tail -3                                                           # Ran 539 tests … OK
grep -ohE '"[A-Z][A-Z0-9]*(-[A-Z0-9]+)+"|"(data|log)\.[a-z_]+"' scripts/checks/*.py | sort -u | wc -l   # 169
grep -nE '\b(fail|warn|info|error)\(\s*f?"[A-Z]' scripts/checks/*.py | sort -k3 -u          # the level per code (new)
grep -nE 'error\("(PLUGIN|NO-SHEETS)' scripts/check.py                                       # the runner's four codes (new)
python3 -c "import json;s=json.load(open('assets/stats.json'))['runcheck']['rustmapper']['steps'];print(len(s),sum(x['gate'] for x in s))"   # 25 7
python3 -c "import sys;sys.path.insert(0,'scripts');from sheets import route;print(len(route.PURPOSE))"   # 17
python3 scripts/check.py --tier fast | tail -1                                               # committed report: 4599 fail
python3 scripts/build_assets.py && python3 scripts/render_readme.py --check && python3 scripts/check.py --tier fast,render | tail -5   # 0 fail 4 warn
git checkout -- assets/build-report.json
```
The probe-flip script is §3's: load `tests/test_round13.py`, deep-copy `stats["runcheck"]["rustmapper"]`, set a step's
`ok`, call `resolved(stats, rc)` and read `text` / `verified` / `retired` per entry.

## 7. Must-fixes, ranked

**MF1 (PRD; and a product option).** §7.5, alt row (line 385). Status "gate, test" overstates the poem clause.
Change the row to: "Alt text ≤ 25 words, not starting "The", last sentence ≤ 10 words | gate, test | ALT-LONG, ALT-THE,
ALT-LAST; T-ALT (`test_route.py:832`: length, first word, the three names, the "How to install" prefix)" and a second
line: "its last sentence equals `[alt] alt_poem`'s hero line (`chart.toml:563`) | **gate (warn)**; no test | ALT-POEM
(`alt.py:50`); `test_pipeline.py:553` checks the poem's length only". Why: `alt.py:50` is `warn`, and no product test
reads `alt_poem`. If the clause is meant to hold, the product fix is one word at `alt.py:50` (`warn` → `fail`) plus
an assertion in T-ALT; add it to §10 as a row owned by a session.

**MF2 (PRD).** §7.4 lines 363 and 364. Mark BOUNDS-TEXTURE and BOUNDS-NO-MANIFEST "(warn)" and add "a sheet with no
text manifest in the report is skipped with BOUNDS-NO-MANIFEST, so the BOUNDS fails rest on the manifest being
written"; mark REPORT-BYTES "(warn)" beside SIZE-TARGET; in line 365 move XML-SET-LOOP to the warn side of the idle
mark. Why: `bounds.py:56, 85`, `size.py:56`, `xml.py:82`.

**MF3 (PRD).** §7 preamble (lines 283–292) and appendix B. Add a row "check.py (the runner) | — | PLUGIN-IMPORT,
PLUGIN-CRASH, PLUGIN-RESULT, NO-SHEETS (all `error`, exit 3; `check.py:246, 254, 115, 286`)", and in the preamble say
the grep covers the plug-ins only. In §6.1's second row (line 276) replace "(exit 1 or 3)" with "(exit 1: a `fail`;
exit 3: an `error`, which is one of the runner's four codes or a plug-in that could not check: FRAMES-TOOL,
PERF-TOOL, REPORT-STATS, FLAG-WRAP, MOTION-XML, MOTION-READ)". Why: §7's own rule, "every live code has a row here
or an idle mark in appendix B", and these are the codes a maintainer meets when the job goes red for a reason that is
not the page.

**MF4 (PRD).** Fold the unregistered tests of §4 into the register, one row or one cell each: §7.5 a new row "C1 says
`Saved to` without the colon; "once" is C1's word alone; H1 never says "done" while H0 is drawn | test |
`test_c1_has_no_colon_mid_sentence` (`test_round12.py:208`), `test_once_is_c1s_alone` (`:216`), `test_pairing`
(`test_round16.py:85`)"; §5.1's trap sentence (line 168) gains "(`test_trap_is_ringed_by_a_dotted_line`,
`test_route.py:871`)"; §7.4's left-edge row (367) becomes "gate, test" with `test_route.py:953`; §7.5's ROUTE-LABEL
row (386) gains `test_no_edition_draws_file_labels` (`:1030`); §5.1 F1 gains `test_governor_is_a_clause_of_fetch`
(`:935`); §7.3's agent row (343) gains `test_bots` (`test_data.py:83`); §5.1 H1 gains
`test_h1_takes_the_quiet_words_only_on_the_probe` (`test_route.py:267`). Why: round 4 deferred four of these to this
round by name; the others hold rules a reviewer is asked to judge at §8.3 q.4 ("no sentence read twice") without being
told a test already pins the wording.

**MF5 (PRD; the product work is §10.12).** §10.12 (line 712), the Fix cell: add "each code's level (fail / warn /
info / error) as emitted equals the status its §7 row states" and "appendix B is written by the test from
`scripts/checks/*.py` and the loader, and the test fails when the committed appendix differs (the AUDIT-STALE /
`cargo rdme --check` pattern)". Why: the existing spec (tokens exist, tiers match, counts match) would have passed
this round's register while MF1–MF3 were wrong in it; sources [6], [9], [11] above say a register nobody executes
is not a reference.

**MF6 (PRD).** §3 G1 (line 96). Quote the clause that opens the brief: *"This readme does not show an expert or high
level smart person who has a massive interest in design"* (7 Oct 15:30), and add to its meaning "a stranger would say
the person who made this cares about design"; add that line to §8.3 q.6's third line (G1d), which already asks where
the reviewer saw care. Why: it is the first sentence he typed, the one every later sentence refines, and the
register carries it only in appendix A.

**MF7 (PRD).** Cites beside their subject: §5.3 row 4 (line 196) `test_pipeline.py:206–210` → `:211–223`; §5.1 R13's
"Drawn only when" → "anchors hold and `crawl_ctrl_c` passed (`runs`)"; §5.1 R15's source → "`[[handoffs]]`,
`chart.toml:1443`"; §5.3 row 6 gains one clause: "M1 (`kind = "ci"`, the `main`-has-fixed-it line) prints after the
cautions only while its `cargo` gate holds (`render_readme.py:697, 740`); not printed today (its `absent
"--ignore-robots"` anchor fails, §5.4 row 1)". Why: §0 promises line numbers checked by hand; 59 of 60 held, and the
reader of row 4 lands on the picture test.

Not a must-fix: the 11:32 and 16:12 sentences of §4, which can stay as they are; `runcheck.py:8`'s "four behaviours"
(§10.18, product); the `frames` info in `gate.txt` (appendix B's "idle" is accurate enough).

## 8. Score

**7 / 10.** The register now reproduces: 28 plug-ins, 539 tests, 25 steps, 17 PURPOSE rows, 168 codes, every tier,
every §5.4 cell, every §8.2 warning, 59 of 60 line cites. What is still wrong is the kind of thing a hand check
misses by construction: four levels, four codes outside the grep's reach, a warn-only clause presented as a gate, and
ten tests that hold rules the register does not say are held. The answer to the owner's 11 Oct sentence is the one
reviewer 2 gave in round 4 and it still stands: five rounds have changed no product file; the one product change
that would end this class of finding is §10.12, and this round's MF5 says what it must check.

## Sources

Outside, read with WebFetch this round:

1. rustdoc, "Documentation tests" — https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html — "`rustdoc` supports executing your documentation examples as tests. This makes sure that examples within your documentation are up to date and working"; `ignore`, `no_run`, `compile_fail`, `should_panic`.
2. Python docs, `doctest` — https://docs.python.org/3/library/doctest.html — "searches for pieces of text that look like interactive Python sessions, and then executes those sessions to verify that they work exactly as shown"; use case 1, "check that a module's docstrings are up-to-date".
3. Sphinx, `sphinx.ext.doctest` — https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html — "the `doctest` builder will collect them and run them as doctest tests"; `doctest_fail_fast`.
4. ExUnit.DocTest — https://ex-unit.hexdocs.pm/ExUnit.DocTest.html — "Doctests allow us to generate tests from code examples found in `@moduledoc` and `@doc` attributes."
5. mdBook, `mdbook test` — https://rust-lang.github.io/mdBook/cli/test.html — runs a book's Rust blocks through rustdoc; `ignore` and non-Rust blocks skipped.
6. cargo-rdme — https://github.com/orium/cargo-rdme — "To verify that your README is up to date with your crate's documentation you can run `cargo rdme --check`"; exit 0 / 3 / 4.
7. MkDocs configuration, `strict` and `validation` — https://www.mkdocs.org/user-guide/configuration/#strict — "Set to `true` to halt processing when a warning is raised"; `links.not_found` is "intended for use with `mkdocs build --strict` (where it becomes an error)".
8. Write the Docs, "Docs as Code" — https://www.writethedocs.org/guide/docs-as-code/ — version control, code review, automated tests on docs; "You can block merging of new features if they don't include documentation".
9. Wikipedia, "Specification by example" — https://en.wikipedia.org/wiki/Specification_by_example — "when they are validated frequently, such documents are a reliable source of information on business functionality"; Living Documentation.
10. Cucumber, "Behaviour-Driven Development" — https://cucumber.io/docs/bdd/ — "system documentation that is automatically checked against the system's behaviour".
11. Concordion — https://concordion.org/ — specifications instrumented and run; failing assertions highlighted with expected and actual; "The specifications become trusted as an accurate source of reference."
12. ArchUnit user guide — https://www.archunit.org/userguide/html/000_Index.html — "ArchUnit's main focus is to automatically test architecture and coding rules, using any plain Java unit testing framework."

Repository files opened (paths from `/home/user/wt-v12`): `docs/PRD.md`; `docs/crit/prd/owner-messages.md`;
`docs/crit/prd/LOG.md`; `docs/crit/round6/SPEC.md` (§0); `scripts/check.py:1–80, 108–115, 202, 234–238, 246, 254,
286`; every `scripts/checks/*.py` (docstring, `TIER`, code literals, emit levels; `alt.py:25–55`, `bounds.py:50–92`,
`size.py:44–70`, `strings.py:55–70, 140–185`, `xml.py:78–86`, `motion.py:124–292`, `data.py:53–96`, `log.py:36–69`,
`route.py:43, 58–62, 70, 265–337`, `wrap.py:85–105`, `position.py:27–56`, `readme.py:7, 89, 104, 121, 247, 279–337`,
`expiry.py:37–42`, `figures.py:93–104`, `type.py:35`, `frames.py:47`, `legend.py:62`, `perf.py:76`, `design.py:18`,
`repos.py:3–5, 30`, `column.py:45–50, 229–237`); `scripts/runcheck.py:1–30, 866–875, 1100–1168`;
`scripts/sheets/route.py PURPOSE`; `scripts/data/route.py:59, 236`; `scripts/render_readme.py:459, 670–671, 697,
740`; `scripts/tokens.py:73–74, 131`; `scripts/publish_chart.py:2–14, 81`; `.github/workflows/profile.yml:13, 22–27,
72–74, 106, 133, 142–153, 160, 168, 174`; `chart.toml` (`[route.rustmapper]` walked whole; lines 9, 13, 26, 30–31,
35–39, 563, 667, 829, 900, 1005–1030, 1074–1160, 1257, 1443); `assets/stats.json` (`runcheck.rustmapper.steps`);
`README.md:7–13, 38, 49, 50, 86`; `docs/BEN-TODO.md:34–36, 39`; `tests/` (all 471 test names by `ast`;
`test_route.py:93, 107, 124, 267, 375, 386, 417, 485, 517, 527, 558, 576, 780, 807, 812–841, 850, 871, 894, 935, 953,
1030, 1052`; `test_round6.py:88`; `test_round7.py:91, 367, 370, 391`; `test_round12.py:124, 205–222`;
`test_round13.py:41–64, 258–275`; `test_round15.py:124, 193`; `test_round16.py:80–100, 336`; `test_pipeline.py:47,
196–223, 296, 307, 495, 506, 553`; `test_proof.py:158, 200`; `test_data.py:80–97, 317`); the round-16 renders
`sheet-phone-day-390.png`, `page-desk-1.png`, `page-phone-2.png` and `gate.txt`.
