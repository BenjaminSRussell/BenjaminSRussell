# PRD review round 3, reviewer 3: An engineer who trusts nothing the PRD says until the code says it too

11 Oct 2026. Document: `docs/PRD.md` at `107a988` (776 lines). The product code is unchanged since the baseline
`027f081` (`git diff --stat 027f081..HEAD`: nine files, all under `docs/`), so every line number the PRD cites still
points where it pointed in rounds 1 and 2. Everything below that is a claim about the code, the data, the renders or
the remote was opened or run in the worktree `/home/user/wt-v12` on branch `v12/purpose`; the command is named so the
next reviewer can repeat it. Findings that `docs/crit/prd/LOG.md` marks applied or declined are not repeated (the
`[facts]` switch, the theme strings, `tests/test_prd.py` as a product ask, the probe and fallbacks of §10.9).

**Score: 7 / 10.** The register's claims about the code are right where they are checkable and most of them are:
every finding code the PRD cites is emitted by the plug-in appendix B names, every tier is the plug-in's `TIER`,
every test it names exists at the file named, the counts (28, 539, 25, 7 + 18, 48, 12) reproduce, §8.2 is `gate.txt`
exactly, §5.1 is `PURPOSE` row for row, and the five §5.4 resolver flips reproduce to the word. What costs the three
points is the same thing as last round, now with evidence: the register is a hand-maintained matrix, and it has
already drifted with no code change between rounds (a code count that reproduces by no method, three status cells
that say "review" where a test exists, line numbers off by one and three, a plug-in marked idle that warns on every
build).

---

## 1. The owner's question: is the product this PRD defines what he wants?

**Yes.** The sentence that decides it is 9 Oct 20:50: *"My goal is to have a purpose behind each map. Every single
fucking map needs a deep purpose. Every single, not even just maps. Everything, single thing inside of this needs a
purpose, not a fucking chasing a reason."* The product of §5.1 is one drawing whose 17 `<g id="hero-*">` groups are
the 17 keys of `scripts/sheets/route.py PURPOSE` (printed: T1, T2, R0, R1, R2, R5, R6, S1, S2, F1, H0, W1, H1, C1,
R12, R13, R15; the Q of every row matches §5.1's Q column), and `ROUTE-PURPOSE` (`scripts/checks/route.py:43`) fails
a drawn group without a row. On `sheet-phone-day-390.png` and `sheet-desk-day-870.png` (opened) nothing is drawn
that is not in that table: name, role, project and its sentence, the install line with its date, four rows of what
the run does, two catches in a dotted box, Ctrl-C, the file and its fields, the hand-off line. That is 11:37's *"The
map, very helpful. The fucking log, not really"* and *"helpful data that you're looking at [...] in a cool format"*.

The sentence that decides this document, as opposed to the page, is 11 Oct 01:12: *"review all of the do and donts
and specifically all of the rules that must be followed and review how they are implemented"*. §3, §7, §10 and
appendix B are that review. "All" is the word the must-fixes below hold the document to.

## 2. Section 7 and appendix B, row by row: what I opened and what held

| Claim | How checked | Result |
|---|---|---|
| Appendix B: 28 plug-ins | `ls scripts/checks/*.py` minus `__init__.py` | 28 |
| Appendix B: every tier | each file's `TIER` constant; `data.py` and `log.py` have none, and `check.py:234` defaults to `"fast"` | all 28 right (`boxpad`, `column`, `frames`, `wrap` render; `perf` perf; the rest fast) |
| Appendix B: every code | every `fail(`/`warn(`/`error(`/`info(`/`Finding(` literal, the `scan(…, code)` calls in `strings.py:161–183`, the `err(…, "MOTION-…")` calls in `motion.py`, the dotted `data.*`/`log.*` strings | every code appendix B lists is emitted by the plug-in it names; `README-PLACEHOLDER` is rightly under `position`; `FIGURES` and `TYPE` are single codes (`figures.py:93–104`, `type.py:35`) |
| Every code token in `PRD.md` | regex `[A-Z][A-Z0-9]*(-[A-Z0-9*]+)+` over the PRD (105 distinct), `grep -F` over `scripts/checks/` | all exist; the eight misses are not codes (`BEN-TODO`, `COMMIT-DAYS`, `FLUID-6626`, `R4-F1`, `T-ALT`, `T-BREAKS`, `T-NOSIZE`, `T-PURPOSE`) |
| Every `test_*` name in the PRD | `grep -rn "def <name>"` over `tests/` | all 25 exist at the files named; `test_functions` is a `stats.json` key (§5.3 row 5), `test_alt_is_short_plain_and_agrees_with_chart_toml` is `main`'s v11 test (§0), both rightly absent |
| The warn/info levels §7 asserts | the call sites | ROUTE-WAITING, ROUTE-PROBE-SKIPPED warn (`route.py:265, 275`); ROUTE-HANDOFF info (`:296`); CI-GATES, README-MISSING, README-RENDER warn (`readme.py:104, 279, 337`); POSITION-EMPTY, -STALE warn (`position.py:31, 56`); SIZE-TARGET warn (`size.py:46`); ALT-NO-README warn (`alt.py:27`); the three EXPIRY codes warn (`expiry.py:37–42`); `data.*` fail/warn split as §7.3 states (`data.py:53–98`) |
| §7.1 THEME_WORDS (18 words), BANNED (20) | `route.py:60–61`; `from checks.strings import BANNED` | identical; `design.py:18 EXTRA_WORDS` adds eight for DESIGN.md |
| §7.1 DESIGN.md theme words are a gate | `design.py:53–55` | `fail("DESIGN-FRESH", "theme words in DESIGN.md's prose…")` |
| §7.2 ROUTE-PURPOSE one-way; the hand list `{S2, W1}` | `route.py:43`; `tests/test_route.py:812–829` (`want = ids - {"S2", "W1"}` at 822) | holds |
| §7.3 the stats invariants and levels | `data.py:53–98` | holds; one level the row omits: `data.calendar` is also emitted as `info` when no GraphQL window was fetched (`data.py:70`) |
| §7.3 NOTICE-CITE form | `notices.py:23 CITE_FORM` | `<repo>, <Mon YYYY>: <what>.` |
| §7.4 floors and constants | `route.py:70, 77–78`; `column.py:45–50`; `readme.py:28, 121`; `render_readme.py:670–671`; `tokens.py:131–133` | 770/1246/964; 308/13 and 278/11; `MIN_PX 11`, `TALL_FROM 768`, `TALL_PX 900`, `DESK_MIN_PX 14.5`; `CODE_COLUMNS 32`; 7/25; the budgets 300/100/3000/120/250 and hero 170/60: all hold |
| §7.4 publish-before-commit | `publish_chart.py:81 unshipped`; `test_round15.py:193`; `test_round12.py:124`; `profile.yml` commit step after the publish step, `if: ${{ !inputs.dry_run }}` | holds |
| §7.6 PR #17 | `gh api repos/BenjaminSRussell/BenjaminSRussell/pulls/17` | `state: open, mergeable: true, head: v11.1/no-thesis` |
| §5.1 against `PURPOSE` and `chart.toml [route.rustmapper]` | both printed | 17 ids, Q for Q. S1: four wordings, 3 and 4 without `{script}` (the command dropped without `crawl_help`). F1: wording 1 carries `fn = "governor_task", absent = "current_permits > MIN_PERMITS"` (`chart.toml:829`); the printed words are wording 2. H0 `runs = [robots_stall, robots_resume]`, a `skipped` wording, and `fails = [robots_stall]` → `""`. W1 `drawn = false`, `runs = [export_after_kill]`, `fails = [kill_writes_file]`, fallback "logged to disk, then saved to redb, in batches". H1 `runs = [crawl_ctrl_c, quiet_after_last_page, quiet_slow_page]`, `fails = [ends_by_itself]`, and `runs = [ends_by_itself]` → `""`. C1 `runs = [crawl_ctrl_c, second_ctrl_c]`. R13 anchors `pub struct SitemapNode`, `pub depth: u32`, `pub status_code: Option<u16>`, `pub title: Option<String>` in both trees. `header_runs = [crawl_ctrl_c]`. ROUTE-ENTRANCE's 14 days at `route.py:14`. `edition.version 0.1.3`, `date 2025-11-08`, `scripts = ["rust_sitemap"]`: the sheet prints `rust_sitemap crawl` and `0.1.3 · 8 NOV 2025` |
| §5.4 probe names | the set of every `runs`/`fails` name in `chart.toml` minus the 25 step ids in `stats.json` | `{crawl_delay_obeyed}`; named at `chart.toml:1080, 1155, 1160`; the comment at `1074–1075` says "not written yet"; no such function in `runcheck.py`. Steps named by no wording: the six gates and `resume_after_kill` (named only in the comment at `chart.toml:900`) |
| §5.4 "Needs here" | `scripts/data/route.resolve()` on today's `stats.json` with each probe flipped | `ua_seen` failed → L7 `verified: False`; `ends_by_itself` passed → H1 and M1 `""`; both export probes failed → X1 `verified: False`; `kill_writes_file` passed → W1 "logged to disk, then saved to redb, in batches". All four reproduce |
| §5.4 "At HEAD `32c2651`" | the clone at `scratchpad/clones/Rust-sitemap` (`git rev-parse`: `32c2651`) | `src/robots.rs:16` asks `https://{}/robots.txt`; `parse_crawl_delay_secs` at `robots.rs:53`, called at `frontier.rs:913`; `cli.rs:40` default `RustSitemapCrawler/1.0`; `pyproject.toml:55 bindings = "pyo3"`, no `[project.scripts]`; no `SIGTERM`/`signal::unix` in `src/`; no `noindex` in `src/`; `tests/crawl_exits_when_idle.rs:67` passes `--ignore-robots`; no `tests/robots_4xx_allows_crawl.rs` |
| §5.4 `[route.rustmapper.gates]` / `release_gates` | `chart.toml:700–733` | `cargo` waits on the P1 and P2 tests; `export_defaults`, `no_services`, `export_after_kill`, `blank_rows` are the release gates §5.3 rows 4 and 6 lean on |
| §6: 28 plug-ins, 539 tests, 22 s, 25 steps, 7 + 18 | `ls`; `python3 -m unittest` ("Ran 539 tests in 21.343s, OK"); a loader walk per module; `stats.json runcheck.rustmapper.steps` | 539 (`test_supporting` 24, `test_timeline` 26, `test_approaches` 19, `test_chartlib` 22 = 91; product 448; `test_edition` 11); 25 steps, `gate: true` on `venv, install, help, crawl_help, export_help, crawl_ctrl_c, export`, the 18 probes in §6's order; `runcheck.py:7` says "probes four behaviours" |
| §8.2 against `round-16/gate.txt` | the file | `0 fail · 4 warn · 0 error`, exit 2: `log.shards`, `POSITION-EMPTY`, `LICENSE-FLAGSHIP`, `ROUTE-WAITING S2`. §8.2's three plus the one it moved to §8.1 item 6: exact |
| §0: `main` 23 behind; 12 runs; 48 reviews; seven research files | `git rev-list --count main..027f081` = 23 (26 to HEAD, the three PRD commits); `gh api …/workflows/profile.yml/runs` = 12; `ls docs/crit/round6/review-r*-*.md` = 48; `docs/research/round6/R1…R7` exist | hold |
| §8.3 q.4 first person, winks | `page-desk-1.png`, `page-phone-2.png` opened; `README.md` | third person; "Boring under load." present; the facts line prints "authored 45 of its 146 commits and co-signed 1 of his own 101" (G8 open, as the PRD says) |

So the register's **positive** claims hold. What follows is where its statuses, its counts and its line numbers do
not, and what it leaves out.

## 3. The other direction: what the code holds that the register does not say

### 3a. Finding codes with no row in §7 and no idle mark

§7's preamble (line 279) promises "every live code has a row here or an 'idle' mark in appendix B". Taking §7
(lines 271–384) and reading the shorthand (`-LINE` after `CONTRAST-TEXT`) and wildcards (`FRAMES-*`) generously,
these codes have neither:

| Code | What it holds (from the plug-in) | Where the rule could live |
|---|---|---|
| `LICENSE-FLAGSHIP` (warn, `readme.py:7`) | a flagship GitHub detects no license for | §8.2 names it as a warning; §7 has no rule "the flagship has a LICENSE" |
| `README-CD` (fail, `readme.py:247`) | a code block whose first line is `cd <path>` may not follow a sentence that says to run it "in" that folder | §5.3 row 6 names it as a holder; no rule states it |
| `README-LICENSE` (fail, `readme.py:313`) | when `LICENSE` and `LICENSE-ASSETS.md` exist the License bullet must render | §5.3 row 13 only |
| `REPO-SET` (fail, `repos.py:3–5`) | every README repository link is surveyed; every surveyed repository is linked; none twice inside `<details>`; the "N more" matches | §5.3 row 9 only |
| `log.load, .json, .schema, .version, .rule, .computed, .shards` | `assets/log.json` v2 schema and consistency with `stats.json` (`log.py:1`) | appendix B says **idle**; `gate.txt` shows `-- fast log 2 finding(s)` and the `log.shards` warning on the round-16 build, and §8.2 lists it. A plug-in that runs on every build and warns is not idle; it is a live gate on a file (`assets/log.json`) the workflow commits (`profile.yml:160`) |
| `STRINGS-ALT, -MANIFEST, -README, -TOML` | the BANNED scan per file (`strings.py:161–183`) | covered by §7.1's BANNED row in substance; the row names only `STRINGS-BANNED` |
| `data.calendar` at `info` | no GraphQL window this run (`data.py:70`) | §7.3's row lists it as warn only |

### 3b. Tests that hold a rule the register does not state

`tests/test_route.py` tags its tests with T-codes. The PRD names five (T-PURPOSE, T-NOSIZE, T-WORDS, T-BREAKS,
T-ALT). The file also carries **T-ANCHOR** (`:93, 375, 386, 558, 576`: a missing file, text or `absent` anchor fails;
`const` prints the code's value; `fn` narrows to the body; `field`/`arg` anchors), **T-BOTH** (`:107`: true in both
trees or not drawn, "the crt.sh hazard of concept A"), **T-SCRIPTS** (`:417`: `edition.scripts` from the wheel),
**T-WHEELS** (`:485`) and **T-HANDOFF** (`:517`). T-BOTH is the test behind §7.3's fourth row, which cites only the
gate. The others are the anchor grammar that every §5.1 and §5.4 claim rests on, and the register never says what an
anchor is or that a test holds its forms.

Rules held by a test and stated nowhere in §3–§7 (each opened):

| Rule (as the test asserts it) | Test |
|---|---|
| A conditional wording ("unless", "when", "only", "if": `scripts/data/route.py:59 CONDITIONAL`) must name a probe in `runs`/`fails` or carry a `producer` anchor; a setter anchor alone verifies nothing | `tests/test_round6.py:88 test_every_committed_conditional_wording_has_a_probe_or_producer`, with `:70–86` (setter alone fails, producer or probe passes). This is the rule behind §5.4 row 3 and §10.9: it is *why* L1's Crawl-delay wording needs `crawl_delay_obeyed`, and the PRD never states it |
| Forks are dropped from the surveyed set | `tests/test_proof.py:158 test_rest_repos_drops_forks`. §5.3 row 9 says "every surveyed repository" without saying what is surveyed |
| The install time prints only from a cold-cache source build, never from a wheel or a warm cache; the wheel note names the platform it was built on | `tests/test_proof.py:200 test_time_only_when_cold`. §5.3 row 6's "platform note" has no holder |
| S2 and L4's "ignores `Crawl-delay`" are never both printed | `tests/test_round15.py:124 test_never_both` |
| While H0 is drawn, H1 never says "done" | `tests/test_round16.py:85 test_pairing` (the round-16 "quit, not done" ruling) |
| Exactly three working rules, rule 4 cut; no "editions", no `pypi.org` in them | `tests/test_pipeline.py:296 test_notices_first_four_and_no_release_line`. §5.3 row 10 says "1–3" with NOTICE-* as holders, which check cites, not the count |
| The title block carries no `repo_count`, no CI, no "1 OF" (no chart number) | `tests/test_route.py:1052 test_title_block_is_name_and_role`. §4's "no chart number" has a test and §4 names no holders at all |
| The gap under the box is ≥ 14 units and shows with every colour set to black | `tests/test_route.py:894 test_the_gap_shows_without_colour`. G1a says "review" |
| The hand-off line is drawn only while the join's state is `runs` | `tests/test_route.py` `test_handoff_line_drawn_only_when_it_runs`. G1a's third mark; §5.1 R15 says "test exists" without naming it |
| The trap box is a rounded `rect`, `fill="none"`, accent stroke, round caps, dasharray `0.1 n` | `tests/test_route.py:871 test_trap_is_ringed_by_a_dotted_line`. §5.1's prose says it; no row |
| C1 has no colon mid-sentence; `Saved to:` is tested in the anchor, not printed | `tests/test_round12.py:208` |
| Seven British spellings absent, "summarized" present | `tests/test_round7.py:391 test_one_spelling` (see MF2) |
| The first "Scrapy" in the prose is preceded by "His"; PyPI precedes Scrapy on the link line | `tests/test_round7.py:367 test_first_mention` (see MF2) |
| `is_bot("Claude")`, `is_bot("dependabot[bot]")` true; a human name false | `tests/test_data.py:83 test_bots`; §7.3's agent row cites only `test_agent_authored_and_agent_share` |

### 3c. Sentences of his that state a rule the register does not carry

Every message was read against §3, §7 and appendix A. Appendix A says 15 messages "set a rule" and quotes them.
Four of the 15 are cited by no row of §3 or §7 (`grep -n` over the PRD finds them only in appendix A):

- 8 Oct 14:22, *"survey is weird"*: the only time he objected to a word before 9 Oct. The rule is held (`survey` is in
  `THEME_WORDS`, `route.py:60`, and in `design.py:18 EXTRA_WORDS`), but §7.1's first row traces to G2 and G5, not to
  the sentence that banned the word. G1c quotes the other two thirds of that message.
- 7 Oct 17:18, *"It's mediocre and not exciting or well designed and intercut this feels basic"*: G1's standard;
  uncited.
- 8 Oct 16:38, *"Merged check and this needs higher reviews"* and 8 Oct 23:24, *"run all agent judgment for a second
  round and review and implementation"*: G17/G19 process rules; uncited.

Two more sentences are rules by his own framing and are carried only by implication:

- 9 Oct 11:32, *"It's a sailing thing, which I do fuck with. I think that's a cool concept"*: the positive half of the
  theme ruling. G13a carries 11:37's "with a layer of a theme of shipping"; the 11:32 sentence that says keep it is
  cited nowhere, so a later reader of §3 sees only the prohibitions (G2, G5, G9, G10, G12) and one permission.
- 7 Oct 17:40, *"this should appear like it took a team months of work and years of workshopping"*: the finish
  standard in his words; G1 paraphrases "the standard of finish" and cites 7 Oct 15:30 only.

## 4. Must-fixes, ranked

### MF1. The register's own figure and its completeness claim do not hold (PRD text)

**Where.** §7 preamble, lines 275–279 ("The 28 plug-ins emit 160 distinct codes … so that every live code has a row
here or an 'idle' mark in appendix B"); appendix B, line 755 (`log` "idle"); §8.2, line 421.

**What.** 160 reproduces by no method I tried. By the method the preamble names (every `fail`/`warn`/`error`/`info`
literal plus the dotted strings) the count is **162**, because `frames.py:47, 93`, `legend.py:62` and `perf.py:76`
emit bare `FRAMES`, `LEGEND`, `PERF` info codes the preamble does not count. By every code literal in the files
(adding the `scan(…, code)` codes of `strings.py` and the `err(msg, code)` codes of `motion.py`, which the
`fail(`-regex misses) it is **169**. Replace the sentence with one that names the method and the number it gives, or
print no number: "The 28 plug-ins emit about 160 codes; the exact set is the output of `grep` over
`scripts/checks/` and will be pinned by §10.12." Then make the completeness claim true: add to §7.3 "The flagship has
a LICENSE GitHub detects | gate (warn) | LICENSE-FLAGSHIP"; "Every README repository link is surveyed, every surveyed
repository is linked once, the 'N more' count matches | gate | REPO-SET"; to §7.5 "A `cd` in a code block never
follows a sentence that puts the reader in that folder already; the License bullet renders when the files exist |
gate | README-CD, README-LICENSE". Change appendix B's `log` row from "idle" to "live on `assets/log.json`; warns
`log.shards` on every build (§8.2); goes with §10.8", and add `info` to `data.calendar`'s levels in §7.3.

**Why.** §7.3's first rule is "nothing invented or estimated", and the PRD applies it to itself ("this document prints
no figure it did not measure", §9.1). His instruction is "all of the rules" (11 Oct 01:12). A count that cannot be
reproduced and a completeness claim that a `grep` refutes are the two things an engineer checks first, and both fail.
Round 2's reviewer 3 asked for exactly this coverage (r02-3 MF1, applied); the fix pass added the rows but printed a
count it did not derive.

### MF2. Three status cells say "review" where a test holds the rule (PRD text)

**Where.** §7.5 line 361 ("His Scrapy repository", not the framework; American spelling | **review**); §3 G1a, line
97 (Held by: **review**); §8.3 q.4, line 441–443.

**What.** `tests/test_round7.py:391 test_one_spelling` asserts seven British spellings are absent from the visible
README (`summarise`, `summarised`, `organise`, `optimise`, `recognise`, `normalise`, `summarisation`) and that
"summarized" is present. `tests/test_round7.py:367 test_first_mention` asserts the first "Scrapy" in the prose is
preceded by "His" and that "is his crawl system on top of the Scrapy framework" is on the page. So the §7.5 row is
"test (seven words; the first mention) + review (the rest)", and §8.3 q.4's grep list (colour, behaviour, organise,
licence, grey, centre, favour, catalogue) should say it extends the test's seven, not stands alone. G1a: the gap is
pinned by `test_the_gap_shows_without_colour` (≥ 14 units, legible in black), the hand-off line by
`test_handoff_line_drawn_only_when_it_runs`, and the loop bracket's arrowhead by ROUTE-ARROW; the cell should read
"test (the gap, the line) and gate (the bracket); review for whether a reader finds them".

**Why.** The register's one job is to say how each rule is implemented ("review how they are implemented", 11 Oct
01:12). A cell that says "review" when a test exists understates the product and tells the next session the wrong
place to look. The doctest sources below are built on the opposite principle: the document's claim is only as good
as the check that reads it (Python doctest's first stated purpose is "to check that a module's docstrings are
up-to-date", source 2).

### MF3. Rules the tests hold and the register never states (PRD text; one is the rule behind §5.4)

**Where.** §7.3 (after the "Every claim about the code rests on anchors" row, line 314); §5.3 rows 6, 9, 10; §4.

**What.** Add these rows, from §3b:

- §7.3: "A wording that states a condition (`unless`, `when`, `only`, `if`) names a probe in `runs`/`fails` or a
  `producer` anchor; a setter anchor alone verifies nothing | test | `test_every_committed_conditional_wording_has_a_probe_or_producer`
  (`tests/test_round6.py:88`); `CONDITIONAL`, `SETTER`, `producers()` in `scripts/data/route.py:59–60, 236`". This is
  the rule that makes §5.4 row 3 and §10.9 necessary, and the PRD explains the consequence (L1/L4 go unverified)
  without the rule.
- §7.3: "Anchors have five forms (file exists / `text` / `absent` / `const` / `fn`-scoped, plus `field` and `arg`),
  each held by a test | test | T-ANCHOR (`test_route.py:93, 375, 386, 558, 576`); T-BOTH (`:107`); T-SCRIPTS
  (`:417`); T-WHEELS (`:485`); T-HANDOFF (`:517`)".
- §7.3: "Forks are not surveyed | test | `test_rest_repos_drops_forks` (`test_proof.py:158`)"; §5.3 row 9 says so.
- §5.3 row 6, Held by: add "`test_time_only_when_cold` (`test_proof.py:200`): the install time prints only from a
  cold-cache source build; the wheel note names its platform".
- §5.3 row 10, Held by: add "`test_notices_first_four_and_no_release_line` (`test_pipeline.py:296`): exactly three".
- §5.4 row 3, "Needs here": add "`test_never_both` (`test_round15.py:124`) already forbids S2 beside L4's 'ignores
  Crawl-delay'".
- §4: give the non-goals their holders where one exists: "No chart number" is `test_title_block_is_name_and_role`
  (`test_route.py:1052`, no "1 OF", no count or CI on the title block); "no commit totals" the provenance-line test.

**Why.** "Specifically all of the rules that must be followed" (11 Oct 01:12). The tests are the rules the sessions
actually wrote down; a register that omits them is smaller than the product.

### MF4. Line numbers and a file reference that point one or three lines off (PRD text)

**Where.** §6.1, line 269 ("`assets/log.json` is in the commit (line 157) and in `push: paths` (line 24)"); §7.4,
line 339 ("DESK-PX from `breakpoint_px + 1` (`column.py:50`, …)").

**What.** `profile.yml:24` is `"chart.toml"`; `assets/log.json` is line **25**. Line 157 is `git config user.email`;
the `for f in assets/stats.json assets/log.json …` that stages it is line **160**. `column.py:50` is `DESK_MIN_PX =
14.5`; `breakpoint_px` is read at `column.py:231` (`bp = … .get("breakpoint_px", 1199)`). Write "`profile.yml:25`",
"`:160`", and "`column.py:231` (`DESK_MIN_PX` at `:50`)". While there: §5.4 row 3's "`frontier.rs:911–918`" is
`:913` for the call in the clone (the range is fine; the call is one line).

**Why.** Small, but this is the document's own standard ("every claim about code has an anchor in the code", G7),
and these three were added in round 2 and are already wrong with no code change, which is the point of MF6.

### MF5. Appendix A's "15 that set a rule" includes four that no rule cites (PRD text)

**Where.** Appendix A, lines 665–668 and the excerpts at 673, 683, 687, 688; §3 G1, G1c, G17; §7.1 first row.

**What.** Either cite them or move them to the "other six". Concretely: §7.1's first row gains "(8 Oct 14:22: 'survey
is weird'; `survey` is in THEME_WORDS and `design.py EXTRA_WORDS`)"; G1 cites 7 Oct 17:18 beside 15:30 and quotes
17:40's "appear like it took a team months of work and years of workshopping" as the finish standard in his words;
G17 cites 8 Oct 16:38 ("higher reviews") and 23:24 ("second round"). And G13a gains 9 Oct 11:32, *"It's a sailing
thing, which I do fuck with. I think that's a cool concept"*, so the table carries his permission as well as his
prohibitions.

**Why.** "Is it matching what I'm saying?" (9 Oct 20:50) is answered by a register that traces each rule to the
sentence that set it. Round 2 fixed this for G8, G10 and G13; these four are the remainder.

### MF6. The enforcement claims are at the right level; the document's own enforcement is not (PRD text, and one §10 column)

**Where.** §0 first bullet (lines 23–25); §10.12 (line 618, Blocks: "nothing"); every line-number citation in §5–§7.

**What.** This round found four kinds of drift in a document whose code did not change between rounds: a count (MF1),
statuses (MF2), line numbers (MF4) and an idle mark (MF1). None was caught, because the register is a traceability
matrix kept by hand, and §0 says so. The outside practice for keeping a document's claims true against code is to
make the claims executable: Rust's doctests fail when an example stops compiling (source 1), Python's doctest exists
"to check that a module's docstrings are up-to-date" (2), Sphinx and pytest run documentation snippets in the build
(3, 10), mdBook runs a book's code blocks as tests (4), ExUnit extracts test cases from the docs (5), Dredd "reads
your API description and step by step validates whether your API implementation replies" (9), specification by
example calls the validated set "living documentation" precisely because unvalidated documentation goes stale (14),
and GitLab fails CI "when either the source code files or the documentation files are updated" without the other (15).
The traceability literature says the opposite about hand-kept matrices: they are "cumbersome and error-prone" at
scale and go inconsistent through "outdated copies" (8).

The PRD states its claims at the right level for that: codes, tiers, test names, constants, line numbers. What it
lacks is the check, and `tests/test_prd.py` is declined as product work (LOG rounds 1 and 2; §10.12). Three changes
the PRD can make itself:

1. **Cite symbols, not lines, wherever a symbol exists.** `render_readme.LIST_MAX_ITEMS`, `column.TALL_FROM`,
   `checks.route.HEIGHT`, `publish_chart.unshipped`, `tests.test_route.test_every_element_has_a_purpose` are stable
   under edits; `:670`, `:47`, `:70`, `:81`, `:812–829` are not. Keep a line number only where there is no name
   (`chart.toml:1074` comments, `README.md:38`), and date it. A test can resolve a symbol with `grep -n "^NAME ="` or
   `inspect`; it cannot know whether a line number was meant for this commit or the last.
2. **Stamp the register.** §0's "checked by hand on 11 Oct 2026" should be "checked by hand against `027f081` on 11 Oct
   2026 (PRD round 3: four drifts found, MF1–MF4)", so the next reader knows the register is a claim with a date,
   not a fact.
3. **Give §10.12 a blocking state.** "Blocks: nothing" is why it is still open after three rounds that each found
   drift. "Blocks: the next PRD round" (the round cannot score the register above 7 while it is unchecked) is a PRD
   decision, not product work, and it is the one lever this document has.

**Why.** His 9 Oct 20:50 standard is "review and check and review and check"; a document that describes 160-odd
automatic checks and is itself checked by nobody fails that standard on its own page. The sources below are the
practice; §10.12 already names the test; the PRD can at least stop making the test harder with every line number
it adds.

## 5. Not must-fixes

- §5.1 R2's "`≤ 14 days old`" and ROUTE-ENTRANCE: `route.py:14` says "dated more than 14 days before `taken`";
  the PRD's wording is right.
- §6's "`resume_after_kill` is run every week and read by nothing": confirmed (named only in the comment at
  `chart.toml:899–900`); §10.18 carries it.
- §9.1's "the fold holds four today: L3, X3, X2, X1": the four `fold = true` lines at `chart.toml:1257, 1276, 1308,
  1357`.
- Appendix B's `legend` row says "idle: no symbols (LEGEND-*)"; `legend.py:62` still emits an info `LEGEND` row count
  on every build. Harmless; "idle" means "fails on nothing", which is true.
- The renders: `sheet-phone-day-390.png` and `sheet-desk-day-870.png` show the same seventeen marks; `page-desk-1.png`
  shows the three stop-rule comment lines wrapped at the phone's width in an 846 px column, as §11 says it costs.

## 6. The next round

Run the §7 and appendix B checks of §2 again after the fix pass, from a script, and put the script's output in
`LOG.md`; if the fix pass will not write `tests/test_prd.py`, the review round should at least leave the commands.

## Sources

Outside sources (read for MF6):

1. Rust, "Documentation tests", https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html.
   Doc examples are extracted and run; "regular doctests are considered to 'pass' if they compile and run without
   panicking", so an example that stops compiling fails the build.
2. Python, `doctest`, https://docs.python.org/3/library/doctest.html. First stated purpose: "check that a module's
   docstrings are up-to-date by verifying that all interactive examples still work as documented"; also regression
   testing and "executable documentation".
3. Sphinx, `sphinx.ext.doctest`, https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html. "This extension
   allows you to test such code snippets in the documentation in a natural way"; `testcode`/`testoutput` run in the
   docs build.
4. mdBook, `mdbook test`, https://rust-lang.github.io/mdBook/cli/test.html. A book's code blocks run as rustdoc tests;
   "At the moment, only Rust tests are supported."
5. Elixir, `ExUnit.DocTest`, https://ex-unit.hexdocs.pm/ExUnit.DocTest.html. "Extract test cases from the
   documentation": `iex>` examples in `@doc` become test cases.
6. Write the Docs, "Docs as Code", https://www.writethedocs.org/guide/docs-as-code/. Docs in version control, reviewed
   like code, "following the same workflows as development teams"; teams may refuse to merge features without docs.
7. Cucumber, "Behaviour-Driven Development", https://cucumber.io/docs/bdd/. Examples written so both people and
   machines read them, "automatically checked against the system's behaviour", so the documentation is living.
8. Wikipedia, "Requirements traceability", https://en.wikipedia.org/wiki/Requirements_traceability. A traceability
   matrix maps requirements to code and tests; manual matrices are "cumbersome and error-prone", and "Repository or
   tool stack integration can present a significant challenge to maintaining traceability in a dynamic system."
9. Dredd, https://dredd.org/en/latest/. "Dredd reads your API description and step by step validates whether your API
   implementation replies with responses" as documented.
10. pytest, "How to run doctests", https://docs.pytest.org/en/stable/how-to/doctest.html. `--doctest-modules` and
    `--doctest-glob` run documentation examples as part of the test run.
11. Vale, https://docs.vale.sh/. "Vale is a command-line tool that brings code-like linting to prose"; rule-based,
    errors can fail a CI build.
12. Rust, "The `#[doc]` attribute", https://doc.rust-lang.org/rustdoc/write-documentation/the-doc-attribute.html.
    `#[doc = include_str!("../../README.md")]` pulls a README into the crate docs (where its examples become doctests);
    the page itself only says "including external files as documentation".
13. Knuth, "Literate Programming", https://www-cs-faculty.stanford.edu/~knuth/lp.html. "The main idea is to treat a
    program as a piece of literature, addressed to human beings rather than to a computer."
14. Wikipedia, "Specification by example", https://en.wikipedia.org/wiki/Specification_by_example. "a complete set of
    specifications with examples is called Living Documentation"; validated automatically so it does not go stale.
15. GitLab, "Documentation testing", https://docs.gitlab.com/development/documentation/testing/. Vale, markdownlint,
    link and redirect checks in CI; "A CI/CD job fails when either the source code files or the documentation files
    are updated" without the other.

Files opened in the worktree (all under `/home/user/wt-v12` unless absolute):

16. `docs/PRD.md` (776 lines at `107a988`); `docs/crit/prd/owner-messages.md` (21 messages); `docs/crit/prd/LOG.md`;
    `docs/crit/prd/review-r02-3.md`; `docs/crit/prd/review-r03-1.md` (first 60 lines).
17. `scripts/checks/*.py` (28 plug-ins: every `TIER`, every code literal; `route.py:6–22, 43, 60–62, 70, 77–78,
    265–296`; `readme.py:7–11, 28, 97–104, 121–125, 246–250, 279, 312–337`; `repos.py:3–38`; `position.py:31, 56`;
    `data.py:53–98`; `design.py:1–60`; `expiry.py:37–42`; `column.py:11–13, 44–63, 231`; `size.py:46`; `alt.py:27`;
    `strings.py:147–183`; `motion.py:129–185`; `frames.py:47, 93`; `legend.py:62`; `perf.py:76`; `figures.py:93–104`;
    `type.py:35`; `notices.py:23`; `log.py:1–25`); `scripts/check.py:2–53, 234`.
18. `scripts/runcheck.py:1–60` and its `def` list; `scripts/data/route.py:59–60, 236, 294, 420, 498` and `resolve()`
    run five times with probes flipped; `scripts/data/derive.py:16–54`; `scripts/sheets/route.py PURPOSE` (printed);
    `scripts/render_readme.py:459, 670–671`; `scripts/tokens.py:128–140`; `scripts/publish_chart.py:1–14, 79–83`.
19. `chart.toml:9, 13, 35–39, 563, 667, 680–735, 811–863, 898–902, 1032–1057, 1072–1082` and every `[[route.rustmapper.entry]]`
    with its `instead` wordings, `runs`, `fails`, `drawn`, `fold`, `waits` (dumped with `tomllib`).
20. `assets/stats.json` (`runcheck.rustmapper.steps`, `edition`, `routes.rustmapper`); `README.md:7–13, 38, 86`;
    `.github/workflows/profile.yml:13–30, 100–110, 148–165`; `docs/BEN-TODO.md:39`.
21. `tests/`: `python3 -m unittest` (539, OK, 21.3 s); a loader walk per module; every `def test_` with its docstring;
    `test_route.py:93–107, 375–386, 417, 485, 517, 558, 576, 780–830, 871, 894, 1052`; `test_round6.py:70–95`;
    `test_round7.py:91, 367–395`; `test_round12.py:124, 208`; `test_round13.py:248–260`; `test_round15.py:124, 193`;
    `test_round16.py:85`; `test_pipeline.py:47, 206–210, 296, 307–330, 495, 506`; `test_proof.py:158, 200`;
    `test_data.py:83`; `test_edition.py`.
22. `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/gate.txt`,
    `sheet-phone-day-390.png`, `sheet-desk-day-870.png`, `page-phone-2.png`, `page-desk-1.png`.
23. The clone `scratchpad/clones/Rust-sitemap` at `32c2651`: `src/robots.rs:16, 53`; `src/frontier.rs:913`;
    `src/cli.rs:40`; `pyproject.toml:55`; `tests/crawl_exits_when_idle.rs:67`; `grep` for `SIGTERM`, `noindex`,
    `project.scripts`, `robots_4xx_allows_crawl.rs`.
24. GitHub REST via `gh api`: `pulls/17` (open, mergeable, `v11.1/no-thesis`); `actions/workflows/profile.yml/runs`
    (12). `git`: `rev-list --count main..027f081` (23), `main..HEAD` (26), `diff --stat 027f081..HEAD` (docs only).
25. `docs/crit/round6/review-r*-*.md` (48 files, counted); `docs/research/round6/R1…R7` (seven files, listed).
