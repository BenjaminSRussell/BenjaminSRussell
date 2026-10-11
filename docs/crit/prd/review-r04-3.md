# PRD review round 4, reviewer 3: An engineer who trusts nothing the PRD says until the code says it too

11 Oct 2026. Document: `docs/PRD.md` at `92b1bef` (832 lines). Product baseline `027f081`; `git diff --stat
027f081..HEAD -- . ':!docs'` is empty, so every line number the PRD cites was meant for the code as it stands. Every
claim below about the code, the data, the renders or the remote was opened or run in `/home/user/wt-v12` on
`v12/purpose`; the command is given so the next round can repeat it (§6 collects them). Findings that
`docs/crit/prd/LOG.md` records as applied or declined in rounds 1–3 are not repeated: the `[facts]` switch, the theme
strings, `tests/test_prd.py` as product work, the §10.9 probe and fallbacks, the 162/169 code count, symbol-over-line
cites. The two other round-4 reviews in the folder were not opened.

**Score: 7 / 10.** The register's positive claims hold again: the 28 plug-ins and their tiers, every code and test
the PRD names, the 25 run-check steps (7 + 18), 539 tests, §5.1 against `PURPOSE` and `chart.toml` row for row, the
§5.4 resolver flips, §8.2 against `gate.txt`, and, new this round, §8.1 item 2 reproduced end to end (build, render
check, `check.py --tier fast,render`: 0 fail, 4 warn, exit 2). What costs the points is one thing the PRD has wrong
about the product and three things it has wrong about itself: a fresh clone's gate fails on a tracked, stale
`assets/build-report.json` that the weekly job never commits, and §10.7 blames gitignored stills that do not exist;
the code-count method the preamble names cannot see two live codes the PRD itself cites; seven live `log.*` codes
and four `STRINGS-*` codes have no row in §7 despite the preamble's promise; and two line numbers were wrong at the
baseline they are dated to.

---

## 1. The owner's question: is the product this PRD defines what he wants?

**Yes.** The sentence that decides it is 9 Oct 20:50: *"My goal is to have a purpose behind each map. Every single
fucking map needs a deep purpose. Every single, not even just maps. Everything, single thing inside of this needs a
purpose, not a fucking chasing a reason."* §5.1 defines one drawing of 17 elements; `scripts/sheets/route.py PURPOSE`
has exactly those 17 keys (printed: T1, T2, R0, R1, R2, R5, R6, S1, S2, F1, H0, W1, H1, C1, R12, R13, R15), each with
what a stranger learns, a Q and a source, and the Q of every row equals §5.1's Q column (checked one by one).
`ROUTE-PURPOSE` (`scripts/checks/route.py:43`) fails a drawn group without a row;
`test_every_element_has_a_purpose` (`tests/test_route.py:812–829`) fails a row without a group. On
`sheet-phone-day-390.png` and `sheet-desk-day-870.png` (opened) nothing is drawn beyond those rows: name, role,
project and sentence, install line with date, three rows of the run, two catches in a dotted box, Ctrl-C, the file
with its fields, the hand-off line. That is 11:37's *"The map, very helpful. The fucking log, not really"* and *"helpful
data that you're looking at [...] in a cool format"*.

For the document rather than the page, the sentence is 11 Oct 01:12: *"review all of the do and donts and
specifically all of the rules that must be followed and review how they are implemented."* §3, §7, §10 and appendix B
are that. "All" and "how they are implemented" are what the must-fixes hold it to.

## 2. Section 7 and appendix B, row by row

| Claim | How checked | Result |
|---|---|---|
| App. B: 28 plug-ins, their tiers | `ls scripts/checks/*.py` less `__init__.py`; `grep -n '^TIER' scripts/checks/*.py`; `check.py:234` defaults a missing `TIER` to `"fast"` (`data.py`, `log.py` have none) | 28; `boxpad`, `column`, `frames`, `wrap` render, `perf` perf, 23 fast. Round-16 `gate.txt` lists 27 runs (perf excluded by `--tier fast,render`) |
| App. B: every code is emitted by the plug-in named | every `"[A-Z]…-…"` and `"data.*"`/`"log.*"` literal per file, plus `fail("FIGURES"…)` (`figures.py:93–104`) and `fail("TYPE"…)` (`type.py:35`) | every code in appendix B is in its plug-in's file; `README-PLACEHOLDER` under `position`; nothing in appendix B is missing from the code. Reverse direction in §3 |
| Every code token in the PRD exists | regex over `PRD.md` (112 tokens), `grep -F` over `scripts/checks/` | all exist; the misses are not codes (`T-*` test tags, `BEN-TODO`, `COMMIT-DAYS`, `FLUID-6626`, `R4-F1`, `CONTACT-EMPTY`, which §10.21 says does not exist yet) |
| Every `test_*` name in the PRD exists | 45 names, `grep -rln "def <name>"` over `tests/` | all 32 test functions exist at the files named; the 13 non-matches are module names (`test_route`, `test_round7`, …), the `stats.json` key `test_functions`, `test_prd` (§10.12, by design absent) and `main`'s v11 `test_alt_is_short_plain_and_agrees_with_chart_toml` (§8.5, rightly absent here) |
| §7.1 THEME_WORDS, pirate words, BANNED | `route.py:60–62` (18 words, `\b…\b`, case-insensitive: `arr` cannot match "array"); `len(strings.BANNED)` = 20; `design.py:18 EXTRA_WORDS` | hold |
| §7.1 T-PURPOSE "containment only" | `tests/test_route.py:812–829`: group ids ⊆ PURPOSE, `want = ids - {"S2", "W1"}`, no `<path|circle|rect|use>` outside a group; nothing about what is inside a group | holds, as the row says |
| §7.2 ROUTE-PURPOSE one-way | `route.py:43` docstring: "a drawn element without a row" | holds |
| §7.3 levels | `route.py:265` warn ROUTE-WAITING, `:275` warn ROUTE-PROBE-SKIPPED, `:281–290` fail ROUTE-ENTRANCE, `:296` info ROUTE-HANDOFF; `data.py:53` fail `data.load`, `:62, 66` warn `data.calendar`, `:69` info `data.calendar`, `:77` fail `data.edition` ("PyPI unreachable and no cache"), `:79` warn (cache), `:90` fail `data.claims`; `expiry.py:37–42` warn ×3; `position.py:31` warn POSITION-EMPTY, `:35` fail CONTACT-PLACEHOLDER; `readme.py:7` LICENSE-FLAGSHIP warns | hold, except the cite `data.py:70` (MF4) |
| §7.3 NOTICE, REPO-SET, README-CD, README-LICENSE, the conditional-wording rule, anchor forms, forks | `repos.py:3–5`; `readme.py:247, 313`; `scripts/data/route.py:59 CONDITIONAL`, `:236 producers()`; `tests/test_round6.py:88`; `test_route.py:93, 107, 375, 386, 417, 485, 517, 558, 576`; `test_proof.py:158` | all at the lines named |
| §7.4 constants | `route.py:70 HEIGHT = {desk 770, phone 1246, mid 964}`, `:57 MAX_AGE = 14`; `column.py:45 MIN_PX 11.0`, `:47 TALL_FROM 768`, `:48 TALL_PX 900`, `:50 DESK_MIN_PX 14.5`, `:231 breakpoint_px`; `readme.py:28 CODE_COLUMNS = 32`, `:121 cautions(max_items=7, max_words=25)`, `:318` reads `_rr.LIST_MAX_ITEMS`; `render_readme.py:670–671` 7 / 25; `tokens.py:73–74 FLOORS` desk/mid 19 (serif 25), phone 26 (serif 30); `tokens.py:131 BUDGETS` 300/100/3000/120/250 | all hold |
| §7.4 publish-before-commit | `publish_chart.py:81 unshipped`; `test_round15.py:193`; `test_round12.py:124`; `profile.yml`: publish at line 142, commit at 153 | holds |
| §7.5 | `test_round7.py:367 test_first_mention`, `:391 test_one_spelling`; `alt.py:32` (25 words), `:39` (last sentence ≤ 10), `:44–50` ALT-POEM; `chart.toml:563 alt_poem` | hold |
| §5.1 against `PURPOSE` and `chart.toml [route.rustmapper]` | both dumped (`tomllib`) | 17 ids, Q for Q. S1: four wordings, 3 and 4 with no `runs` and no `{script}`. F1 wording 1 carries `fn = "governor_task", absent = "current_permits > MIN_PERMITS"` and the printed words are wording 2. H0: `runs = [robots_stall, robots_resume]`, a `skipped = [robots_stall]` twin, `fails = [robots_stall]` → `""`. W1: `drawn = false`, `runs = [export_after_kill]`, `fails = [kill_writes_file]`, fallback "logged to disk, then saved to redb, in batches". H1: `runs = [crawl_ctrl_c, quiet_after_last_page, quiet_slow_page]`, `fails = [ends_by_itself]`; `runs = [ends_by_itself]` → `""`. C1: `runs = [crawl_ctrl_c, second_ctrl_c]` and `runs = [crawl_ctrl_c]`, neither names `ends_by_itself` (`chart.toml:1005–1030`). `header_runs = [crawl_ctrl_c]`. R15: `stats.json handoffs` `sitemap-jsonl→ideal-url-organizer` state `runs`. `edition`: 0.1.3, 2025-11-08, `scripts = ["rust_sitemap"]`, which is what the sheet prints |
| §5.4 "Needs here" | `scripts/data/route.resolve()` on today's `stats.json` with the probe flipped (script in §6) | `ends_by_itself` passed → H1 and M1 `""`, **C1 unchanged** ("press Ctrl-C once and wait for `Saved to`…"); `ua_seen` failed → L7 `verified: False`; both export probes failed → X1 `verified: False`; `kill_writes_file` passed → W1 "logged to disk, then saved to redb, in batches"; `robots_read` passed and `robots_stall` failed → H0 `""`, L6 `""`, L4 "Until a host's `robots.txt` is back, it fetches that host's pages, disallowed ones too. It ignores `Crawl-delay`." (the https clause gone). All six reproduce |
| §5.4 "At HEAD `32c2651`" | the clone at `scratchpad/clones/Rust-sitemap` (`git rev-parse --short HEAD` = `32c2651`) | `src/robots.rs:16` `https://{}/robots.txt`; `:53 pub fn parse_crawl_delay_secs`; `src/frontier.rs:913` calls it; `src/cli.rs:40` `default_value = "RustSitemapCrawler/1.0"`; `pyproject.toml:55 bindings = "pyo3"`, zero `project.scripts`; `tests/` holds `crawl_exits_when_idle.rs` (`:67 "--ignore-robots"`) and no `robots_4xx_allows_crawl.rs`; no `SIGTERM`/`noindex` in `src/` |
| §5.4 probes vs `runcheck.py` | every `runs`/`fails`/`skipped` name in `chart.toml` against the 25 step ids in `stats.json` | 17 probes named; `resume_after_kill` named by nothing but the comment at `chart.toml:900`; `crawl_delay_obeyed` named at `:1080, 1155, 1160` and absent from `runcheck.py` (`PROBES` at `:870–872` and the `_step` calls) |
| §6: counts | `ls`; `python3 -m unittest` ("Ran 539 tests in 20.569s OK"); `stats.json runcheck.rustmapper.steps` | 28; 539; 25 steps: `gate: true` on `venv, install, help, crawl_help, export_help, crawl_ctrl_c, export` (7), 18 probes in §6's order, none `skipped`; `ends_by_itself`, `robots_read`, `kill_writes_file`, `resume_after_kill` failed, the rest passed |
| §6: workflow | `profile.yml:13` cron; `:22–27` push paths (scripts, chart.toml, log.json, requirements.txt, the workflow); `:106` `build_stats.py --runcheck`; `:118–124` the gate step exits on anything but 0 or 2; `:142` publish; `:153` commit; `:160` the `for f in` loop; `:188–199` the pencil-note path (`failure() && steps.stats.outcome == 'failure'`) | hold; the pencil-note path publishes sheets and never reaches the commit step, so on a failed survey the README on `main` is last week's by omission, which is what §6 says |
| §8.1 item 2 | `python3 scripts/build_assets.py` (6 files, 0 problems) → `render_readme.py --check` ("README.md is current") → `check.py --tier fast,render` | **0 fail · 4 warn · 0 error, exit 2**; the four warnings are §8.2's three plus POSITION-EMPTY. First run this round that the sequence has been reproduced rather than read from `gate.txt`. The build modifies the tracked `assets/build-report.json` (MF1); restored with `git checkout` |
| §8.2 against `round-16/gate.txt` | the file | `0 fail · 4 warn · 0 error`: `log.shards`, `POSITION-EMPTY`, `LICENSE-FLAGSHIP`, `ROUTE-WAITING S2`. Exact |
| §8.5, §9.1, app. D | `gh api`: `pulls/17` `{open, mergeable: true, head v11.1/no-thesis}`; `actions/workflows/profile.yml/runs` 12, latest `38140965684` schedule, failure, 2026-10-11T12:52; `branches/main` `d253286`; `branches/chart` `c488907 "chart: soundings 2026-10-09"`; the open PR list is #17 alone (this branch has none) | hold |
| §0 | `ls docs/crit/round6/review-r*-*.md` = 48; `docs/research/round6/R1–R7` exist (307 URL lines across them; appendix D's "360" is uncounted, not checked further) | hold |
| §5.2 pixel figures | 26 × 308 / 600 = 13.35; 26 × 278 / 600 = 12.05; 19 × 482 / 820 = 11.17; 19 × 765 / 820 = 17.7; 19 × 766 / 1000 = 14.55; 19 × 846 / 1000 = 16.07; 1,121 / 600 × 308 = 575 | hold; the sheets are 1000 × 707, 820 × 707, 600 × 1121 (`build-report.json` after a build) |

## 3. The other direction: what the code holds that the register does not say

**Codes with no row in §7.** The preamble (line 272–273) promises "every live code has a row here or an 'idle' mark
in appendix B". A script that reads every code out of `scripts/checks/` and looks for it in §7 (full code, or
prefix plus `-SUFFIX` shorthand) leaves 41 absent. 34 are the FLASH/FRAMES/LEGEND/MOTION/PERF families, idle by
appendix B and §4, fine. The remaining seven and four are not:

- `log.load`, `log.json`, `log.schema`, `log.version`, `log.rule`, `log.computed`, `log.shards`: appendix B now says
  "live on `assets/log.json`" (round 3's correction) and `log.shards` warns on every build (`gate.txt`, and my run),
  but §7 has no row for what `assets/log.json` must satisfy. Live, not idle, and unregistered.
- `STRINGS-ALT`, `STRINGS-MANIFEST`, `STRINGS-README`, `STRINGS-TOML` (`strings.py:164, 165, 180, 183`): the BANNED
  scan per file. §7.1's BANNED row lists the files and names only `STRINGS-BANNED`. Round 3's reviewer listed these in
  §3a; the fix pass added LICENSE-FLAGSHIP, REPO-SET, README-CD and README-LICENSE and left these four.

**Codes the preamble's own count cannot see.** The preamble's grep (`"[A-Z][A-Z0-9]*(-[A-Z0-9]+)+"` plus the dotted
strings) returns 169 strings, and 167 after the two date formats, exactly as stated. But the regex requires a hyphen,
and `FIGURES` (`figures.py:93–104`, fail) and `TYPE` (`type.py:35`, fail) have none. Both are live, both are in
appendix B, both are cited in §7.3 and §7.4. So the method the PRD names undercounts its own register by two, and the
bare `MOTION`, `FRAMES`, `LEGEND`, `PERF` info codes (`motion.py:124` default, `frames.py:47, 93`, `legend.py:62`,
`perf.py:76`) by four more. See MF2.

**Tests that hold a rule the register does not state.** Round 3's list (conditional wordings, anchor forms, forks,
cold-cache install time, `test_never_both`, three working rules, the title block, the gap, the hand-off line) is now
in §7.3 and §5.3, checked. Four that round 3 listed in its §3b are still unstated, and each was opened at its line this
round: `tests/test_round16.py:85 test_pairing` (while H0 is drawn, H1 never says "done"), `tests/test_route.py:871
test_trap_is_ringed_by_a_dotted_line` (the trap box's form), `tests/test_round12.py:208 test_c1_has_no_colon_mid_sentence`,
`tests/test_data.py:83 test_bots`. None is a must-fix on its own; they are listed so the next pass can fold them into
§7.1 (the box), §7.3 (bots) and §7.5 (C1, H1) in one line each. I did not re-read every test docstring this round, so
the list is round 3's, re-verified, not a fresh sweep.

**Sentences of his that state a rule the register does not carry.** Every message in `owner-messages.md` was read
against §3 and §7 again. Round 3's four gaps are closed (8 Oct 14:22 in §7.1; 7 Oct 17:18 and 17:40 in G1d; 16:38 and
23:24 in G17; 11:32's "cool concept" in G13a). One remains, carried only in appendix A (line 723): 9 Oct 11:32, *"But it
doesn't really, it's confusing. Like, you look at it, you're like, oh, I don't know. Like, what's happening?"* That is a
rule about the whole image reading at a glance, distinct from G3 (density) and G16 (a purpose per element): a sheet
can be even and purposeful element by element and still not say what it is. Nothing in §3 traces to it and no §8.3
line asks it (q.1 asks for each mark's purpose; q.6 asks what the reviewer would call it, advisory). MF5.

## 4. Must-fixes, ranked

### MF1. A fresh clone's gate fails, and §10.7 names the wrong cause (product, and PRD text)

**Where.** §10.7 (line 643: "The worktree's `assets/v9` is stale (gitignored v9 footer stills), so `check.py`
without `--out-dir` fails on them | `build_assets.py` first, or `--out-dir`"); §8.1 item 2 (lines 385–388); §6
(line 226, "build-report.json with every text run's source and truth").

**What I found.** `assets/v9/` is gitignored (`.gitignore:6`) and held only the six hero SVGs before I built. The
file that is stale is `assets/build-report.json`, which is **tracked**: `git log -1 -- assets/build-report.json` →
`9e25619`, 8 Oct 2026 07:48, and its `sheets` lists 38 entries (`hero-still-*`, `soundings-*`, `approaches-*`, `log-*`,
`instruments-*`, `footer-*`, the v9/v10 set), not the six editions §5.2 defines. `check.py` reads it by default
(`check.py:202`, `report_path or assets/build-report.json`), so on the committed tree with no build,
`python3 scripts/check.py --tier fast` gives **4599 fail · 8 warn, exit 1** (`XML-SIZE [hero-phone-night]: viewBox
600×1121 but report says 720×900`, then thousands of TYPE fails on sheets that no longer exist). After
`build_assets.py` the report is rewritten (6 files) and the same command passes with 4 warnings. The weekly job never
commits the report: the `for f in` loop at `profile.yml:160` stages `stats.json`, `log.json`, `layout.lock.json`,
`README.md`, `DESIGN.md`, and the comment at `profile.yml:168` says so in as many words ("the build leaves other
tracked files modified (assets/build-report.json)… --autostash parks them"); it is uploaded as a run artefact instead
(`:133`). So the committed report will stay the 8 Oct one on every branch until someone commits it by hand, and
REPORT-SHA/-BYTES/-MISSING/-ORPHAN and XML-SIZE (§7.4's "the report's sha256 matches each SVG") hold only against a
report that is never in the repository. `build_assets.py` has no `--out-dir` flag (argparse: "unrecognized
arguments"); `check.py` has one.

**What to change.** Product: either commit a fresh `assets/build-report.json` on this branch and add it to the
workflow's commit loop (one word at `profile.yml:160`), or gitignore it and have `check.py` fail with one clear
message when it is absent; today's state, a tracked file that every build dirties and no commit refreshes, is the
worst of both. PRD: rewrite §10.7 as "The committed `assets/build-report.json` is the 8 Oct (`9e25619`) report of 38
retired sheets; `check.py` reads it by default (`check.py:202`), so a fresh clone fails the gate (4599 fails) until
`build_assets.py` has rewritten it; the weekly job dirties and never commits it (`profile.yml:160, 168`). Fix: commit
the report and add it to the loop, or ignore it and fail loudly. Owner: a session. Blocks: §8.1 item 2 on a fresh
clone." And in §8.1 item 2 say why the order is build first ("the committed report is stale until `build_assets.py`
rewrites it").

**Why.** §8.1 item 2 is the mechanical acceptance test and it does not pass on the tree as committed; it passes on a
tree after a build. His standard is "review and check and review and check" (9 Oct 20:50); a check that depends on
an uncommitted file is a check nobody else can run. The practice elsewhere is that a generated file is either
committed and verified (Kubernetes `hack/verify-generated-docs.sh` fails CI and says "Please run
hack/update-generated-docs.sh", source 4; Cog `--check` "Check that the files would not change if run again", source
5; embedme `--verify` "Verify that running embedme would result in no changes. Useful for CI", source 3) or not
committed at all. This branch does neither.

### MF2. The code count's method cannot see FIGURES and TYPE (PRD text)

**Where.** §7 preamble, lines 267–270 ("a grep … for code-shaped string literals (`"[A-Z][A-Z0-9]*(-[A-Z0-9]+)+"` and
the dotted `data.*`/`log.*` strings) returns 169 strings, two of which (`YYYY-MM`, `YYYY-MM-DD`) are formats, not
codes: 167").

**What.** The grep reproduces (169, two formats). But it requires a hyphen, so it misses `FIGURES` and `TYPE`, two
live fail codes that appendix B lists and §7.3 and §7.4 cite, and the four bare info codes `MOTION`, `FRAMES`,
`LEGEND`, `PERF`. Replace "167" with: "169 hyphenated or dotted codes less the two formats, plus `FIGURES` and `TYPE`,
which have no hyphen: **169 live codes**; the bare `MOTION`, `FRAMES`, `LEGEND`, `PERF` info codes of the idle
plug-ins are not counted." Or print the regex that counts them: `"[A-Z][A-Z0-9]*(-[A-Z0-9]+)*"` restricted to the first
argument of `fail(`/`warn(`/`info(`, which gives the same 169 plus the four bare codes.

**Why.** Round 3 declined the reviewer's 162 and 169 on the ground that "the PRD prints the one method it names and
the number that method gives" (LOG, round 3, declined). That is the right rule, and this is the case it does not
cover: the one method named is blind to two codes the document itself relies on. §7.3's first rule is "nothing
invented or estimated"; a count that excludes the FIGURES gate, the one that holds every typed number on the page,
is an estimate.

### MF3. Seven live `log.*` codes and four `STRINGS-*` codes have no row in §7 (PRD text)

**Where.** §7 preamble's promise (line 272–273); §7.3 (after the `data.*` row, line 317); §7.1's BANNED row (line
283); appendix B's `log` row (line 786).

**What.** Add to §7.3: "`assets/log.json` is readable JSON of the current schema version, every rule it records is
computed from `stats.json`, and its shard count is the machine's | gate (fail: `log.load`, `log.json`, `log.schema`,
`log.version`, `log.rule`, `log.computed`; warn: `log.shards`) | `checks/log.py`; warns `log.shards` on every build
(§8.2); the file is the retired `log` sheet's and goes with §10.8". Check the fail/warn split against `log.py` before
printing it (I read the codes, not every level). In §7.1's BANNED row, "gate | STRINGS-BANNED" becomes "gate |
STRINGS-BANNED; per file STRINGS-ALT, -MANIFEST, -README, -TOML (`strings.py:164–183`)".

**Why.** The preamble's sentence is a completeness claim and `grep` refutes it in the same way as last round; the
fix pass closed four of the five codes round 3 listed and the `log` family it reclassified as live without giving
it a rule. A register that says "every live code has a row" must be true the way a test is true, or say "most".

### MF4. Two line numbers were wrong at the baseline they are dated to (PRD text)

**Where.** §6 (line 248: "`runcheck.py:7` still says it 'probes four behaviours'") and §10.18 (line 654, the same);
§7.3 (line 317: "`data.calendar` is `info` when no GraphQL window was fetched (`checks/data.py:70`)").

**What.** `scripts/runcheck.py:7` is blank; "Then it probes four behaviours a stranger meets in the first minute" is
line **8**. `scripts/checks/data.py:70` is `for r in stats.get("repos", []):`; the `Finding("info", "data.calendar",
"no GraphQL contribution window in this run…")` is line **69**. Write `:8` and `:69`. §0 says "Line numbers in this
document are as of `027f081`" and the product is unchanged since, so these are not drift; they were off when written
(round 2 and round 3 respectively, and round 3's reviewer 3 repeated the `:70`, which I note against myself as much
as against the fix pass).

**Why.** G7's standard applied to the PRD: "every claim about code has an anchor in the code." Every other line
cite in §5–§7 was opened this round (the full list is in §6 below) and holds; these two are the whole residue, and
they are cheap to fix and cheap to keep wrong, which is the argument for §10.12's "every `file:line` cite points at
the symbol named beside it".

### MF5. "It's confusing… what's happening?" has no row and no judged line (PRD text)

**Where.** §3 (a row beside G3, line 95, or G16, line 109); §8.3 q.1 (lines 423–428); appendix A line 723 (where the
sentence already is).

**What.** Add G3a: "'But it doesn't really, it's confusing. Like, you look at it, you're like, oh, I don't know.
Like, what's happening?' (9 Oct 11:32) | the whole image says what it is at a glance, before any one element is read:
a stranger can say in one sentence what the picture shows | review (§8.3 q.1, new first line)". And in q.1, before
the per-mark lines: "Before reading §1 or the table, the reviewer writes one sentence saying what the image shows;
it must name a tool, an install or a command, and an output. Log the sentence." §1's "one sentence the image must
answer" is the author's; this line is the reader's, and the two are compared.

**Why.** It is his first reaction to the first image and the one sentence of 11:32 that is neither density (G3,
"too dense… can't read anything"), nor theme (G2, G5), nor device (G4). The purpose rule (G16) is per element and
T-PURPOSE holds it per element; nothing holds the whole. Round 3's reviewer 1 and the round-16 product reviews
answer q.6 ("what would they say it was": "install notes drawn as a route", "how you get into my crawler"), which
shows the test is passable; it should be a line he set, not an advisory aside.

## 5. Are the enforcement claims stated at the right level?

Round 3 answered this for the mechanism (make the claims executable; 15 sources in `review-r03-3.md`). This round
read a different set, the tools that keep a *document's* claims matched to *source*, to judge the level the PRD
chooses: codes, tiers, test names, constants, line numbers, counts.

- **Named checks and named locations are the right unit.** Go's example tests are tied to a function name and run
  by `go test`; "Having executable documentation for a package guarantees that the information will not go out of
  date as the API changes" (source 1). Sphinx's `literalinclude` pulls source into a document by `:pyobject:`
  (a class, function or method) or by `:start-after:`/`:end-before:` marker strings, and the docs recommend marker
  comments in the source over line numbers (source 2). The PRD's move in round 3 to symbols beside line numbers is
  that practice; MF4 is the cost of the lines that remain.
- **Counts and lists belong to a command, not a sentence.** Cog keeps generated text inline between markers and
  `--check` fails CI when "the files would not change if run again" is false (source 5); embedme does the same for
  code blocks with `--verify` (source 3); Kubernetes' `verify-generated-docs.sh` is the same shape (source 4). The PRD states its counts as the output of named commands (the grep, `ls`,
  `unittest`), which is the right level; MF2 is a case where the command is wrong, not the level.
- **A traceability register is a thing tools validate.** sphinx-needs gives every requirement an ID
  (`needs_id_required`, `needs_id_regex`) and `needs_warnings` are "checks that all needs must pass during a build";
  with `-W` "the first `needs_warnings` check that does not pass will stop the build" (source 6). Doorstop stores
  each requirement as a YAML file in the repository and `doorstop` with no arguments "runs integrity checks on the
  document tree" (source 7). OpenFastTrace "keeps track of whether you actually implemented everything you planned
  to in your specifications" and "identifies obsolete parts of your product" (source 8). §7 and appendix B are that
  register in Markdown; §10.12 is the integrity check, declined as product three times. The level is right; the
  check is absent, and MF1–MF4 are what absence costs each round.
- **Contract tests read the spec and hit the implementation.** Schemathesis "automatically generates property-based
  tests from your OpenAPI or GraphQL schema" and reports "schema violations" (source 9); nbval re-runs a notebook
  and "a cell that doesn't reproduce the expected output will fail" (source 10). §5.4's "Needs here" column is this:
  each row is a claim the resolver can be run against, and I ran it. The PRD should say the rows are fixtures in
  waiting (it does, §10.9 and §10.12) and keep the flip script where the next reviewer finds it (§6 below).
- **Mismatch between a comment and a signature is a build warning elsewhere.** The kernel's `kernel-doc` emits
  "Excess function parameter 'x' description in 'f'" when a documented parameter no longer exists, `make W=1` runs
  it, and a `-Werror` option lets a caller stop the build (source 11). The PRD's line cites are that kind of
  comment: they describe a signature in another file, and nothing warns when it moves.

Verdict on the level: right. The PRD names the finding code, the plug-in, the tier, the test function, the constant
and the file, which is exactly what the tools above operate on. What it lacks is the operator, and the only PRD-side
answer that does not repeat a declined item is to leave the operator's commands next to the claims, which is what
§6 does for this round.

## 6. The checks, as commands (for `LOG.md` and the next round)

All from `/home/user/wt-v12`. Each prints what §2 cites.

```
ls scripts/checks/*.py | grep -v __init__ | wc -l                       # 28
grep -n '^TIER' scripts/checks/*.py                                    # 26 lines; data.py, log.py default to fast
python3 -m unittest 2>&1 | tail -3                                     # Ran 539 tests … OK
grep -ohE '"[A-Z][A-Z0-9]*(-[A-Z0-9]+)+"|"(data|log)\.[a-z_]+"' scripts/checks/*.py | sort -u | wc -l   # 169 (§7's grep)
grep -nE 'fail\("(FIGURES|TYPE)"' scripts/checks/figures.py scripts/checks/type.py                    # the two it misses
python3 -c "import json;s=json.load(open('assets/stats.json'))['runcheck']['rustmapper']['steps'];print(len(s),sum(x['gate'] for x in s))"   # 25 7
python3 -c "import sys;sys.path.insert(0,'scripts');from sheets import route;print(len(route.PURPOSE),{k:v[1] for k,v in route.PURPOSE.items()})"
python3 - <<'EOF'   # §5.4: flip a probe, resolve, print
import json,sys,copy; sys.path.insert(0,'scripts'); from data import route as R
s=json.load(open('assets/stats.json')); rt=s['routes']['rustmapper']; rc=s['runcheck']['rustmapper']
for flip in ({'ends_by_itself':True},{'ua_seen':False},{'sitemap_keeps_noindex':False,'sitemap_keeps_disallowed':False},
             {'kill_writes_file':True},{'robots_read':True,'robots_stall':False}):
    r2=copy.deepcopy(rc)
    for st in r2['steps']:
        if st['id'] in flip: st['ok']=flip[st['id']]
    out={e['id']:(e.get('verified'),e.get('text','')[:60]) for e in R.resolve(copy.deepcopy(rt),r2)}
    print(flip,{k:out[k] for k in ('C1','H1','M1','L7','X1','W1','H0','L6','L4') if k in out})
EOF
python3 scripts/build_assets.py && python3 scripts/render_readme.py --check && python3 scripts/check.py --tier fast,render; echo rc=$?   # 0 fail 4 warn rc=2
git checkout -- assets/build-report.json                                # the build dirties a tracked file (MF1)
git stash -q; python3 scripts/check.py --tier fast | tail -1; git stash pop -q   # on the committed report: 4599 fail (MF1)
git log -1 --format='%h %cd' -- assets/build-report.json                # 9e25619, 8 Oct
sed -n 160p .github/workflows/profile.yml; sed -n 168p .github/workflows/profile.yml
sed -n 8p scripts/runcheck.py; sed -n 69p scripts/checks/data.py        # MF4
gh api repos/BenjaminSRussell/BenjaminSRussell/pulls/17 --jq '{state,mergeable,head:.head.ref}'
gh api 'repos/BenjaminSRussell/BenjaminSRussell/actions/workflows/profile.yml/runs?per_page=100' --jq '.total_count,(.workflow_runs[0]|{id,event,conclusion,created_at})'
gh api repos/BenjaminSRussell/BenjaminSRussell/branches/main --jq '.commit.sha[0:7]'; gh api repos/BenjaminSRussell/BenjaminSRussell/branches/chart --jq '.commit.sha[0:7]'
```

Line cites opened and found right this round (so the next pass need not): `route.py:43, 57, 60–62, 70, 265, 275,
281–296`; `design.py:18`; `column.py:45, 47, 48, 50, 231`; `readme.py:7, 28, 121, 247, 313, 318`; `position.py:31–35`;
`repos.py:3–5`; `data.py:53, 62, 66, 77, 79, 90`; `expiry.py:37–42`; `tokens.py:73–74, 131`; `publish_chart.py:81`;
`render_readme.py:459, 670–671, 1181`; `scripts/data/route.py:59, 236`; `check.py:202, 234`; `tests/test_route.py:93,
107, 375, 386, 417, 485, 517, 527, 558, 576, 812–829, 894, 1052`; `test_round6.py:88`; `test_proof.py:158, 200`;
`test_pipeline.py:47, 206–210, 296, 307, 495, 506`; `test_round7.py:91, 367, 370, 391`; `test_round13.py:258`;
`test_round15.py:124, 193`; `test_round12.py:124`; `chart.toml:9, 13, 26, 30–31, 35–39, 563, 667, 900, 1005, 1030,
1074, 1080, 1155, 1160, 1257, 1276, 1308, 1357`; `profile.yml:13, 25, 106, 160`; `README.md:1, 7–13, 38, 86`.

## 7. Not must-fixes

- §5.3 row 9's `more_count` is `repo_count − 1 − facts repos − Also names` (`render_readme.py:1181–1187`); the PRD's
  "− profile − 2 − 4" is that formula with today's values, fine.
- §7.4's "Type floors" row cites `TYPE` with no file; the constants are `tokens.py:73–74 FLOORS`, read by `type.py`.
  Worth naming beside the code.
- `gate.txt` shows `-- render frames 1 finding(s)` and `-- fast legend 1 finding(s)`: the idle plug-ins emit one
  `info` each ("no motion: the day edition is its own still"; the legend row count). Appendix B's "idle" is right in
  the sense that matters (fails on nothing).
- The renders: `sheet-phone-day-390.png` and `sheet-desk-day-870.png` carry the same 17 marks; `page-phone-2.png`
  shows the facts line with "coding agents (Claude) authored 45 of its 146 commits and co-signed 1 of his own 101",
  as G8 (open) and §8.1 item 7 say, and "Before you run 0.1.3:" with L1 and L7 first, each with its lever.
- §6's "17 of the 18 probes are named by a wording" counts `skipped` lists as naming (`blank_rows` is in X2's
  `runs`, so it is named either way); holds.

## Sources

Outside sources, read with WebFetch or WebSearch this round:

1. Go blog, "Testing with examples", https://go.dev/blog/examples. Examples "are compiled (and optionally executed)
   as part of a package's test suite"; with an `// Output:` comment "The test passes if the test's output matches its
   output comment"; "Having executable documentation for a package guarantees that the information will not go out
   of date as the API changes."
2. Sphinx, reStructuredText directives, `literalinclude`,
   https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html. `:pyobject:` includes "only the
   specified class, function or method"; `:start-after:`/`:end-before:` select by marker text ("only lines that
   follow the first line containing that string are included"); marker comments in the source are recommended over
   `:lines:`.
3. embedme, https://github.com/zakhenry/embedme. Fills Markdown code blocks from source files; `--verify`: "Verify
   that running embedme would result in no changes. Useful for CI."
4. Kubernetes, `hack/verify-generated-docs.sh`,
   https://github.com/kubernetes/kubernetes/blob/master/hack/verify-generated-docs.sh. Calls
   `kube::verify::generated "Generated docs need to be updated" "Please run 'hack/update-generated-docs.sh'"`.
5. Cog, "Running cog", https://cog.readthedocs.io/en/latest/running.html. "`--check` Check that the files would not
   change if run again"; "You can use the `--check` option to run cog just to check that the files would not change
   if run again"; `--diff` shows the change that made `--check` fail. Index page https://cog.readthedocs.io/en/latest/:
   "All text lines outside of the special markers are passed through unchanged."
6. sphinx-needs, configuration, https://sphinx-needs.readthedocs.io/en/latest/configuration.html. `needs_warnings`
   "defines checks that all needs must pass during a build"; "Use `-W` in your Sphinx build command to stop the whole
   build, if a warning is raised"; `needs_id_required` "Forces the user to set an ID for each need"; `needs_id_regex`
   default `^[A-Z0-9_]{5,}`.
7. Doorstop, https://doorstop.readthedocs.io/en/latest/ and https://github.com/doorstop-dev/doorstop. "facilitates the
   storage of textual requirements alongside source code in version control"; each item is a YAML file, directories
   are documents, documents form a tree; `doorstop` with no arguments "Run[s] integrity checks on the document tree";
   `doorstop link HLTC001 SRD002`.
8. OpenFastTrace, https://github.com/itsallcode/openfasttrace. "a requirement management and tracing suite";
   "Requirement tracing keeps track of whether you actually implemented everything you planned to in your
   specifications"; "identifies obsolete parts of your product"; Gradle and Maven plug-ins for continuous builds (the
   user guide's tag format was not reachable this round).
9. Schemathesis, https://schemathesis.readthedocs.io/en/stable/. "automatically generates property-based tests from
    your OpenAPI or GraphQL schema"; catches "server errors, schema violations, and validation gaps that hand-written
    tests miss"; "Every finding ships with a minimal `curl` reproducer".
10. nbval, https://github.com/computationalmodelling/nbval. A pytest plug-in that "adds functionality to py.test to
    recognise and collect Jupyter notebooks"; each cell is a test; "a cell that doesn't reproduce the expected output
    will fail"; `--nbval-lax` compares only cells marked `#NBVAL_CHECK_OUTPUT`.
11. Linux kernel-doc, https://docs.kernel.org/doc-guide/kernel-doc.html ("The documentation format of `.c` files is
    also verified by the kernel build" with `make W=n`; `tools/docs/kernel-doc -v -none` checks one file) and the
    LKML threads found by search: "Re: [PATCH] doc-guide: kernel-doc: add comment about formatting verification",
    https://lkml.iu.edu/hypermail/linux/kernel/1802.2/02640.html (`make W=1` runs the check; example "Excess function
    parameter 'dest' description in 'tcp_try_coalesce'"), and "[PATCH 22/26] kernel-doc: check for extra kernel-doc
    notations", https://lkml.rescloud.iu.edu/hypermail/linux/kernel/0812.2/02038.html (the "Excess" check's origin).
12. mkdocs, configuration, `validation`, https://www.mkdocs.org/user-guide/configuration/#validation.
    `validation.links.not_found` defaults to `warn`, "intended for use with `mkdocs build --strict` (where it becomes
    an error)"; `strict`: "Set to `true` to halt processing when a warning is raised."
13. docs.kernel.org, "How to help improve kernel documentation", https://docs.kernel.org/doc-guide/contributing.html.
    The docs build emits warnings from malformed kernel-doc comments; "function parameters that lack documentation"
    must be described.

Files opened or run in the worktree (all under `/home/user/wt-v12`):

14. `docs/PRD.md` (832 lines at `92b1bef`); `docs/crit/prd/owner-messages.md` (21 messages, each read against §3 and
    §7); `docs/crit/prd/LOG.md` (rounds 1–3); `docs/crit/prd/review-r03-3.md`.
15. `scripts/checks/*.py`: every `TIER`; every code literal (two greps and a script); `route.py:43, 55–78, 265–296`;
    `design.py:18`; `column.py:45–50, 231`; `readme.py:7, 28, 121, 247, 313, 318`; `position.py:31–35`; `repos.py:3–5`;
    `data.py:53–90`; `expiry.py:37–42`; `figures.py:93–104`; `type.py:35, 73–76`; `strings.py:24, 67, 72, 154,
    164–183`; `motion.py:124–189`; `frames.py:47, 93`; `legend.py:62`; `perf.py:76`; `alt.py:1–50`; `log.py:1–40`.
    `scripts/check.py:2–53, 121–124, 185–205, 234, 272–300`.
16. `scripts/runcheck.py:1–60, 870–872, 1040–1180`; `scripts/data/route.py` (`resolve()` run six times);
    `scripts/sheets/route.py:73–74 PURPOSE` (printed); `scripts/render_readme.py:455–462, 670–671, 1181–1187`;
    `scripts/tokens.py:73–76, 131`; `scripts/publish_chart.py:81`; `scripts/build_assets.py` (run; `--help`);
    `scripts/data/derive.py:16, 54, 64`; `scripts/build_stats.py:518`.
17. `chart.toml` (every `[[route.rustmapper.entry]]` with `instead`, `runs`, `fails`, `skipped`, `drawn`, `fold`,
    `waits`, anchors, dumped with `tomllib`; lines 9, 13, 26, 30–39, 563, 667, 680–733, 811–836, 900, 1005–1030,
    1074–1160, 1257, 1276, 1308, 1357).
18. `assets/stats.json` (`runcheck.rustmapper.steps`, `edition`, `handoffs`, `routes.rustmapper`);
    `assets/build-report.json` (the committed one via `git show HEAD:`, 38 sheets; the rebuilt one, 6);
    `.gitignore:6`; `README.md:1, 7–13, 38, 86`; `.github/workflows/profile.yml:1–70, 116–126, 128–136, 142–172,
    185–199`.
19. `tests/`: `python3 -m unittest` (539, OK, 20.6 s); every `test_*` name the PRD cites (`grep -rln "def …"`);
    `test_route.py:812–830` and the lines in §6; `test_pipeline.py:307–332`, `:505`; `test_round7.py:91`.
20. Renders at `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/`:
    `gate.txt`; `sheet-phone-day-390.png`, `sheet-desk-day-870.png`, `page-phone-2.png` (opened);
    `build/build-report.json` (sheet sizes).
21. The clone `…/scratchpad/clones/Rust-sitemap` at `32c2651`: `src/robots.rs:16, 53`; `src/frontier.rs:913`;
    `src/cli.rs:40`; `pyproject.toml:55`; `tests/crawl_exits_when_idle.rs:67`; `ls tests/`; `grep -rl 'SIGTERM\|noindex'
    src/`.
22. GitHub REST via `gh api`: `pulls/17`; `pulls` (open list); `actions/workflows/profile.yml/runs` (12; run
    `38140965684`); `branches/main` (`d253286`); `branches/chart` (`c488907`). `git`: `diff --stat 027f081..HEAD --
    . ':!docs'` (empty); `log -- assets/build-report.json` (`9e25619`, 8 Oct); `status` before and after the build.
23. `docs/crit/round6/review-r*-*.md` (48, counted); `docs/research/round6/R1–R7` (listed; 307 URL lines).
