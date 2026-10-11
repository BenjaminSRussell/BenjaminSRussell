# PRD review round 2, reviewer 3: An engineer who trusts nothing the PRD says until the code says it too

11 Oct 2026. Document: `docs/PRD.md` at `e17cc80` (691 lines). Everything below that is a claim about the code, the
data or the renders was opened and run in the worktree `/home/user/wt-v12` (branch `v12/purpose`); the commands are
named inline so the next reviewer can repeat them. Earlier rounds' fixes (`docs/crit/prd/LOG.md`) are not repeated.

## 1. The owner's question: is the product this PRD defines what he wants?

**Yes.** The sentence that decides it is 9 Oct 20:50: *"Is it accomplishing my goal? Not just what I'm saying. My
goal is to have a purpose behind each map. Every single fucking map needs a deep purpose. Every single, not even just
maps. Everything, single thing inside of this needs a purpose."* The product in §5.1 is one drawing whose every
`<g id="hero-*">` has a row in `scripts/sheets/route.py PURPOSE` (17 rows; I printed the dict and it matches the 17
IDs of §5.1's table one for one, Q for Q), and the gate `ROUTE-PURPOSE` (`scripts/checks/route.py:335–342`) fails a
drawn element without a row and a group set that differs from the report. The second sentence that confirms it is
9 Oct 11:37: *"what I'd want are very helpful information... The map, very helpful. The fucking log, not really"*; the
round-16 sheet (`sheet-phone-day-390.png`, `sheet-desk-day-870.png`, opened) is directions for running rustmapper
and nothing else: install line, the command, what each page gets, the two catches in a dotted box, Ctrl-C, the file,
the hand-off. His 11 Oct 01:12 ask, *"review all of the do and donts and specifically all of the rules that must be
followed and review how they are implemented"*, is what §3, §7 and appendix B are. The condition the round-1
reviewers attached stands: under option 3 the first phone screen is his flagship's fault list, which §9.1 is honest
about.

## 2. What I checked and what held

The brief was to trust nothing until the code says it. These are the claims I tested; all of them held.

| Claim in the PRD | How I checked | Result |
|---|---|---|
| §6, §0: 28 gate plug-ins | `ls scripts/checks/*.py` = 29 files, one is `__init__.py` | 28 |
| §6: 539 tests, 22 s | `python3 -m unittest` in the worktree: "Ran 539 tests in 20.663s, OK"; per-module count by a loader walk: `test_supporting` 24, `test_timeline` 26, `test_approaches` 19 (= 69) | holds, but see MF3 |
| §6: 25 run-check steps, 7 gates + 18 probes | `stats.json runcheck.rustmapper.steps`: 25; `gate: true` = `venv, install, help, crawl_help, export_help, crawl_ctrl_c, export` (7); 18 probes with the ids §6 lists, in that order | holds |
| §8.2 against `round-16/gate.txt` | the file: `0 fail · 4 warn · 0 error`, exit 2; the four are `log.shards`, `POSITION-EMPTY`, `LICENSE-FLAGSHIP`, `ROUTE-WAITING S2` | §8.2's three plus the one it says moved to §8.1 item 6: exact |
| Appendix B, every tier | each plug-in's `TIER` constant (`data.py`, `log.py` have none: default fast per `check.py`'s contract) | all 28 tiers right |
| Appendix B, every code | every `fail(`/`warn(`/`error(`/`info(` literal in `scripts/checks/*.py`, plus the `scan(..., code)` calls in `strings.py` and the dotted `data.*`/`log.*` strings | every code in appendix B is emitted; the 15 `data.*` and 7 `log.*` are there; `ALT-GLOSS`/`ALT-TWIN` are retired (`alt.py:43`) and rightly absent |
| Every code cited anywhere in `PRD.md` | regex `[A-Z]+(-[A-Z*]+)+` over the PRD, grepped against `scripts/checks` | all exist; the only misses are not codes (`BEN-TODO`, `COMMIT-DAYS`) |
| Every `test_*` named in the PRD | `def test_…` grep over `tests/` | all 22 exist, at the files named; `test_route.py` comments tag `test_nothing_has_a_size` T-NOSIZE, `test_no_theme_words` T-WORDS, `test_breaks_name_a_fact` T-BREAKS, `test_alt_from_the_route` T-ALT (lines 780–850) |
| Line citations: `route.py:43`, `test_route.py:812–829` and `819–822`, `test_round13.py:258`, `publish_chart.py:81` and docstring lines 2–14, `test_round15.py:193`, `test_round12.py:124`, `test_pipeline.py:47/206–210/208/307/495/506`, `test_round7.py:91/370`, `render_readme.py:459`, `BEN-TODO.md:39`, `column.py:45/47–48/50`, `expiry.py:37–42`, `chart.toml:9/35–39/1074/1080/1155/1160`, `README.md` lines 7–13 | `sed -n` on each | every one lands on the thing claimed |
| §7.1 THEME_WORDS list (18 words) | `checks/route.py:60–61` | identical, `ahoy` and `arr` included |
| §7.1 the 20 BANNED entries | `from checks.strings import BANNED; len()` = 20 | identical list |
| §7.2 STRINGS-TWICE: a run of 5 words, 3 naming code or a date; exceptions | `TWICE_WORDS = 4` with `n = TWICE_WORDS + 1`, `SHORT_WORDS = 3`, `TWICE_ALLOW = ("pip install rustmapper", "received work item")` | holds |
| §7.4 floors 13 / 11 px; type floors 19/25 and 26/30; 7 items × 25 words; alt ≤ 25 words; `CODE_COLUMNS = 32`; `BOX_PAD_MIN` 8; `HEAD_GAP_PITCHES` 2; `TALL_FROM` 768, `TALL_PX` 900, `MIN_PX` 11, `DESK_MIN_PX` 14.5 | `route.py:77–78`, `tokens.py:73–75`, `readme.py:121`, `render_readme.py:670–671`, `alt.py:32`, `readme.py:28`, `sheets/route.py`, `column.py:45–50` | all hold |
| §5.1, every row against `PURPOSE` and `chart.toml [route.rustmapper]` | printed both; S1 has four wordings and 3–4 drop the command; F1's first wording carries `absent = "current_permits > MIN_PERMITS"` and the printed words are wording 2; H1 `runs = [crawl_ctrl_c, quiet_after_last_page, quiet_slow_page]`, `fails = [ends_by_itself]`; W1 `drawn = false`, fallback "logged to disk, then saved to redb, in batches"; R13 anchors `pub struct SitemapNode`; `header_runs = [crawl_ctrl_c]`; ROUTE-ENTRANCE "14 days" at `route.py:14` | every cell holds |
| §5.4 "Needs here" column | re-ran `scripts/data/route.resolve()` on today's `stats.json` with probes flipped: `ua_seen` failed → L7 `verified: False`, no wording holds; both export probes failed → X1 unverified; `ends_by_itself` passed → H1 and M1 `""`; `kill_writes_file` passed → W1 "logged to disk, then saved to redb, in batches", still undrawn | the four verified cells reproduce |
| §5.4 "At HEAD `32c2651`" column | the clone at `scratchpad/clones/Rust-sitemap` is at `32c2651`: `src/robots.rs:16` asks `https://{}/robots.txt`; `parse_crawl_delay_secs` at `robots.rs:53`, used at `frontier.rs:911–913`; `cli.rs:40` default `RustSitemapCrawler/1.0`; `pyproject.toml:55 bindings = "pyo3"`, no `[project.scripts]`; no `noindex` in `src/`; only `ctrl_c()` in `shutdown.rs`, no SIGTERM; `crawl_exits_when_idle.rs:67` passes `--ignore-robots`; no `tests/robots_4xx_allows_crawl.rs` | every cell holds |
| §5.4 row 3: `crawl_delay_obeyed` is named and never runs | the set of `runs`/`fails` names in `chart.toml` minus the run-check step ids = `{crawl_delay_obeyed}`; `runcheck.py` has no such function | holds |
| §7.6: PR #17 open and mergeable | `gh api repos/…/pulls/17`: `state: open, mergeable: true, head: v11.1/no-thesis` | holds |
| §0: `main` 23 commits behind | `git rev-list --count main..027f081` = 23 | holds |
| §8.3 q.1: the README grep finds only "Helm chart" | whole-word THEME_WORDS over `README.md` prose outside comments, `<picture>` and code spans | one hit: "a Helm chart for Kubernetes" |
| §8.3 q.4: spelling, winks, first person | the eight-word grep: none; "Boring under load." and "why engines are hard" present; no `I/my/me` | holds |
| §5.3 row 9: 15 more repositories = 22 − 1 − 2 − 4 | `repo_count` 22 | holds |
| §5.3 row 5 / G8: "45 of its 146 … 1 of his own 101" | `README.md` facts line; `stats.json` Rust-sitemap `all_hands` 146, `commits` 101, `coauthored.agent` 1 | holds |
| §6.1: a failed gate publishes nothing | `profile.yml` gate step exits on rc ∉ {0, 2}; publish and commit steps have no `always()`, so they are skipped; the failure path (`failure() && steps.stats.outcome == 'failure'`) rebuilds from the committed stats and publishes sheets only, no commit to `main` | holds |

So the PRD's claims about the code are, today, right. What follows is about what the register leaves out and one
place where it reads his words selectively.

## 3. Must-fixes, ranked

### MF1. §7 is one-way: the plug-ins hold about a hundred rules the register never states (PRD)

**Where.** §7 preamble (line 248–252) and the six tables under it; appendix B (line 654).

**What.** §7 cites 50 finding-code tokens (my regex over §7 alone). The 28 plug-ins emit about 150 distinct codes.
Appendix B lists the codes, but a code in a list is not a rule with a status and a home. These live rules run on
every build and have no row in §7:

- `SIZE-RAW, -GZ, -PHONE, -PAGE, -ELEMENTS, -TARGET` and `REPORT-SHA, -BYTES, -MISSING, -ORPHAN, -STATS`
  (`size.py`: raw ≤ 300 KB, gz ≤ 100 KB, phone raw ≤ 120 KB, ≤ 3000 elements; the report's sha256 matches each SVG
  and `stats.json`). Appendix C mentions "the budgets (SIZE-*)" as surviving; §7 does not.
- `XML-PARSE, -FORBIDDEN, -EXTERNAL-HREF, -ID-DUP, -ID-PREFIX, -REF, -VIEWBOX, -ROOT, -SIZE` (`xml.py`: no live
  `<text>`, `<script>`, `<style>` or external href on a sheet; ids unique and sheet-prefixed; every `#ref` resolves).
  This is the rule behind §5.1's "text as glyph outlines (no web fonts on GitHub)", and it is a gate, not prose.
- `ROUTE-HEIGHT` (desk ≤ 770 units, phone ≤ 1246, mid ≤ 964, `route.py:70`), `ROUTE-PAINT` (rings, bars and words
  painted after the track), `ROUTE-ARROW` (the loop's arrowhead clear of a ring), `ROUTE-MISSING`, `ROUTE-HANDOFF`.
- `ALT-POEM`, `ALT-LAST`, `ALT-NO-README` (`alt.py`: the alt's last sentence ≤ 10 words and equal to `chart.toml
  alt_poem`'s line). §7.5's alt row says only "≤ 25 words, not starting The".
- `NOTICE-CITE` (a cite is `"<repo>, <Mon YYYY>: <what>."`), beside the four NOTICE codes §7.3 does list.
- `POSITION-UNSET, -MISMATCH, -COMMENT, -BLOCK, -STALE`, `CONTACT-PLACEHOLDER` (the printed position line must equal
  `[position] text`; `[contact]` placeholders fail).
- `README-MISSING, -PICTURE, -PICTURE-FOLDED, -RENDER` (one picture block, not inside `<details>`, markers paired).
- The 13 live `data.*` codes: `data.seeded` (no seeded stats may ship outside `--dev`), `data.schema`,
  `data.provenance`, `data.stale`, `data.edition`, `data.calendar`, `data.invariant`, `data.repo_count`, `data.claims`,
  `data.clones`, `data.notices`, `data.unsurveyed`, `data.load`. "Nothing invented" (§7.3 row 1) names
  STRINGS-UNMEASURED and ROUTE-STRINGS but not the gate that refuses seeded data.
- `BOUNDS-TEXTURE, -MORE, -NO-MANIFEST`, `CONTRAST-TINT, -LIGHT, -LIGHTS, -LINE, -RG, -CVD` (named by wildcard
  only).
- `EXPIRY-KEY`, `EXPIRY-FORMAT` (named in G14 and appendix B, not in §7.5's expiry row).

**Change.** Either (a) add rows: to §7.3 "The stats file is unseeded, schema-valid, dated and internally consistent
| gate | `data.seeded`, `data.schema`, `data.provenance`, `data.stale`, `data.invariant`, …" and "The printed
position line equals `[position] text`; no contact placeholder | gate | POSITION-MISMATCH, -STALE, …"; to §7.4
"Each edition within budget: raw ≤ 300 KB, gz ≤ 100 KB, phone ≤ 120 KB, ≤ 3000 elements; the report's hashes match
the files | gate | SIZE-*, REPORT-*", "Every sheet parses; no live text, script or external href; ids unique and
prefixed; every reference resolves | gate | XML-*", "Sheet height ≤ 770 / 1246 / 964 units; marks painted after the
track; the arrowhead clears the rings | gate | ROUTE-HEIGHT, ROUTE-PAINT, ROUTE-ARROW"; to §7.5 "The alt's last
sentence ≤ 10 words and equal to `[alt] alt_poem` | gate | ALT-LAST, ALT-POEM" and NOTICE-CITE on the cite row. Or
(b) say in §7's preamble that §7 holds the rules that trace to his words and appendix B the engineering rules, and
add a fourth column to appendix B, "Rule", one line per code group, so that the register is complete in one place.
(a) is better: the brief's test, "every finding code … that holds a rule the register does not mention", fails on
about two thirds of the codes today.

**Why.** His 11 Oct 01:12 words: *"specifically all of the rules that must be followed and review how they are
implemented"*. "All" is the word. A requirements register that lists holders without the rule they hold is the thing
the traceability sources warn about: a link records a planned relationship, not what is enforced (sources 4, 5, 12).

### MF2. G8 quotes half a sentence and leaves out the one that points the other way (PRD; it shapes §9.2)

**Where.** §3 row G8 (line 90); §9.2 bullet 2 (line 461–468); appendix A (9 Oct 11:35 and 11:37 excerpts).

**What.** G8's cell reads *"We don't need to show the commits... it feels lazy"*. The verbatim text
(`owner-messages.md`, 9 Oct 11:35) is: *"We don't need to show the commits are kind of cool. The data is kind of cool
that we're pulling, but at the same time, it feels lazy, and I don't really like that."* The ellipsis joins two
fragments across a clause that reads at least two ways ("we don't need to show the commits; [they] are kind of cool"
or "we don't need to show [that] the commits are kind of cool"). Two minutes later (11:37) he says: *"with a second
layer of everything, talking about my fucking profile. Talking about my commits. Talking about my work. That is what
this should all be about."* That sentence is in no row of §3, not in G8, not in §9.2, and appendix A's 11:37 excerpt
cuts it with "[...]" (`grep -n 'Talking about my commits' docs/PRD.md` returns nothing). §9.2 then calls "strike"
*"his words; the default from PRD round 1"*.

**Change.** G8's "His words" cell: print the 11:35 sentence whole, then add *"Talking about my commits. Talking about
my work. That is what this should all be about." (9 Oct 11:37)*. §9.2 bullet 2: replace *"The rule is his sentence
(9 Oct 11:35 …); the two memos that argued hiding them costs more are the agents' judgement, not his"* with *"He said
both: 11:35 reads against showing commit figures, 11:37 says the page should talk about his commits and his work.
The default stays off until he picks one; the switch is one line."* Keep the three options. This is not reopening
round 1's "off by default" ruling (the switch, `[facts] agent_clause`, is still the right mechanism); it is the
register carrying both of his sentences instead of one.

**Why.** His standard for reviews is *"is it matching what I'm saying?"* (9 Oct 20:50). A register that quotes him
selectively cannot answer that. The round-1 LOG says reviewer 1's lens wins conflicts; this is a fact about the
transcript, not a lens.

### MF3. §6's "the product's own count is 470" counts 48 tests of engines no page sheet uses (PRD)

**Where.** §6, "Tests" bullet (line 234–235); §10.8.

**What.** The 69 excluded are `test_supporting`, `test_timeline`, `test_approaches`. But `test_chartlib` (22) tests
`island_breaks_surface_with_shelf`, `single_bump_contour_closed_and_area`, `soundings_along_and_spot_heights`,
`symbol_defs_ids_prefixed_and_sloop_commands`, `tints_coast_danger_hatch`, `coast_closes_everything` — islands,
contours, soundings, a sloop, hatching, none of which the route draws (§4, §7.1 "no ships… hatching"); and
`test_timeline` is already counted but `test_edition` (11) holds motion rules too (`test_numeric_begin_untouched`,
`test_no_timestamps`). At minimum the 22 of `test_chartlib` belong with the 69 (names from `grep 'def test_'`). The
honest sentence is "91 of them test sheets and engines that are off the page (`test_supporting` 24, `test_timeline`
26, `test_approaches` 19, `test_chartlib` 22); the product's own count is 448", or compute it the way §10.12
proposes and print nothing until then.

**Change.** Reword the bullet as above; add `test_chartlib` and the `chartlib` functions the route does not call to
§10.8's deletion list.

**Why.** §7.3's first rule, nothing estimated. 470 was computed from three files chosen by name; the fourth is in
plain sight.

### MF4. G4 and §7.4 do not carry the sentence that created the phone rules (PRD)

**Where.** §3 row G4 (line 86); §7.4 preamble.

**What.** 8 Oct 14:22, *"The images are all crushed and survey is weird"*, is the message that produced
HERO-COLUMN-PX, ROUTE-PHONE-PX, DESK-PX and the three editions; appendix A quotes it, §3 does not cite it anywhere
(G4 cites 9 Oct only; §7.4's `chart` branch row cites 8 Oct 11:13). The register's rule "no phone text under 13 px"
has a holder but no owner sentence.

**Change.** G4's "His words" cell: add *"The images are all crushed" (8 Oct 14:22)* before the 9 Oct quote, so the
row reads as the two messages it came from.

**Why.** §3's own contract: *"Each row is a thing he said."*

### MF5. A probe the weekly job runs is named by nothing, and the PRD does not say so where it lists the probes (PRD)

**Where.** §6, "Run check" bullet (line 228–233); §5.4 row 7.

**What.** `resume_after_kill` runs every week (it is one of the 18, `ok: false` today) and is named by no entry's
`runs` or `fails` in `chart.toml` (only a comment at `chart.toml:900`). §5.4 row 7 says so in passing ("named by no
entry, only a comment"); §6's list presents 18 probes as if each fed a wording. The run-check docstring
(`runcheck.py:7`) still says "probes four behaviours".

**Change.** §6: after the probe list add *"17 of the 18 are named by a wording's `runs`/`fails`; `resume_after_kill`
is run and read by nothing (§5.4 row 7)"*. Add to §10 a one-line item: either name it from W1's future wording or
drop the probe; and fix the docstring's "four".

**Why.** G16: *"Everything, single thing inside of this needs a purpose."* A probe that runs for nothing is the
pipeline's version of a mark with no PURPOSE row.

### MF6. The enforcement claims are stated one level above what holds them: the PRD is the only document in the repository that nothing checks (PRD and product; §10.12 already records the product half)

**Where.** §0 bullet 1; §10.12; §7 preamble.

**What.** Every claim I checked in §2 held today, by hand, in about two hours of `sed`, `grep` and resolver runs.
Nothing will hold them tomorrow. The repository already treats its other prose as code: README-STALE, DESIGN-FRESH
and AUDIT-STALE fail the build when `README.md`, `DESIGN.md` or `AUDIT.md` drift from what the scripts write. The
outside practice is the same: Rust's rustdoc runs the examples in the docs as tests so they cannot rot (source 1);
Python's doctest exists "to check that a module's docstrings are up-to-date" (source 2); Sphinx's doctest builder
and `mdbook test` do it for whole manuals (sources 3, 8); Doorstop and Sphinx-Needs keep requirements as text in
the repository with IDs that a build validates (sources 4, 5); codocia binds each page to the files it covers by
hash and exits non-zero when they move (source 11). §10.12 lists the test to write and round 1 declined it as
product work. I am not repeating that must-fix. What the PRD text itself should change: §0's first bullet should
say in one sentence that the register is checked by hand as of the date above and by nothing after it, so a reader
does not take "Held by: gate" as a claim that is itself gated. Until `tests/test_prd.py` exists, the right level for
the PRD's enforcement claims is "names a holder that existed on 11 Oct 2026", not "is held".

**Change.** §0 bullet 1, append: *"The register's own claims (that each code and test it names exists and runs in
the tier stated) were checked by hand on 11 Oct 2026 and are checked by nothing since; §10.12 is the test that would
hold them."* And in §7's preamble: *"Status is what the holder did on the round-16 build, not a promise."*

**Why.** His 9 Oct 20:50: *"Is it doing what I'm saying?"* The PRD answers for the page and the pipeline; it cannot
yet answer for itself.

## 4. The other direction: what the repository holds that the register does not say

Beyond MF1's codes, tests in `tests/` that hold a product rule no §7 row states (names from `grep 'def test_'`):

- `test_pipeline.test_default_build_is_the_hero` (D1: the default build is the hero alone), `test_missing_module_is_a_failure`, `test_refuses_half_built_sets`, `test_unknown_edition_rejected`: the build is all six editions or nothing.
- `test_pipeline.test_nothing_to_check_is_exit_3`: the gate's "could not check" exit; §6 names the exit code, §7 has no row.
- `test_round6.test_every_committed_conditional_wording_has_a_probe_or_producer` and `test_setter_alone_does_not_verify_a_condition`: a wording's condition must be verified by a probe or a producer, never by the code that sets the value. This is a stronger rule than §7.3's "anchors at HEAD and in the released sdist" and it has no row.
- `test_round6.test_a_720_sheet_fails_at_308`, `test_1199_passes_from_360`: the breakpoint is derived, not chosen.
- `test_round12.test_c1_has_no_colon_mid_sentence`, `test_once_is_c1s_alone`, `test_fold_label_names_the_largest_group`, `test_rule_three_title`: copy rules pinned by test, absent from §7.5.
- `test_round13.test_no_folded_item_in_the_open_list`, `test_no_label_no_fold`: the fold's contents are disjoint from the open list; §5.3 row 6 and §7.4's cautions row say "folded" without the disjointness.
- `test_round15.test_never_both` (S2 and its code-only fallback never both print), `test_release_holds_head_does_not_fails` (a regression on main fails even when the release holds): §7.3 row 4 mentions ROUTE-WAITING but not the regression half.
- `test_round16.test_height_does_not_move`, `test_every_edition_clears`: the phone height is pinned at 1,121 units across rounds.
- `test_proof.test_rest_repos_drops_forks`, `test_list_unites_cache_rest_and_confirmed_links`: forks are not surveyed; the repository set is the union of three sources. §5.3 row 9 (REPO-SET) does not say forks are out.

Sentences in `owner-messages.md` that state a rule the register does not carry (beyond MF2 and MF4):

- 7 Oct 17:40, *"this should appear like it took a team months of work and years of workshopping"*: in appendix A, in no G row. It is a finish standard, arguably G1's, and G1 should cite it.
- 8 Oct 09:04, *"Resolve all merge conflicts"*: §7.6 carries "ready to merge" but not "no conflicts"; PR #17's `mergeable: true` covers it today, so the row should say both.

Everything else he typed is carried (I read all 21 messages against §3 and §7.6).

## 5. Section 8.3 and the renders

`sheet-phone-day-390.png`: the three second-reading marks (loop bracket, the gap under the box, the line past the end
bar) are visible; nothing is drawn but bars, rings, the track, the dotted box and type. `page-desk-1.png`: the three
comment lines of the code block wrap at the phone's 32 columns inside an 846 px column, as §11 says; the facts line
prints the agent counts. Advisory answers: I would ship the pipeline today and the page under option 1a; I would
screenshot the phone sheet and call it "install notes drawn as a route", which is the flowchart risk in §11 put
kindly.

## 6. Score

**7 / 10.** Every claim the PRD makes about code, data, tiers, counts, line numbers and resolver behaviour held when
I checked it, which is rarer than it should be. It loses a point for the register's one-way completeness (MF1), one
for quoting the owner by halves on the one decision he has to make (MF2), and one for a count it did not compute
(MF3). None of the must-fixes changes the product.

## Sources

1. https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html — rustdoc extracts code examples from doc comments and runs them; `no_run`, `compile_fail`, hidden `#` lines; the examples stay correct because they are tests.
2. https://docs.python.org/3/library/doctest.html — the three uses: checking docstrings are up to date, regression tests, executable tutorials; the warning that nondeterministic output makes doctests fragile.
3. https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html — `testsetup`/`testcode`/`testoutput` directives; snippets in the manual are collected and run by the doctest builder.
4. https://sphinx-needs.readthedocs.io/en/latest/ — requirements, specifications and test cases as linked objects with IDs inside the docs; traceability; schema validation and filters.
5. https://doorstop.readthedocs.io/en/latest/ — requirements as YAML items with IDs in version control, documents linked parent to child, the `doorstop` command checks the tree's integrity.
6. https://www.writethedocs.org/guide/docs-as-code/ — docs in the same tools as code: version control, review, automated tests; teams block merges that lack documentation.
7. https://cucumber.io/docs/bdd/ — examples in Gherkin that run as automated tests become documentation checked against behaviour (Discovery, Formulation, Automation).
8. https://rust-lang.github.io/mdBook/cli/test.html — `mdbook test` runs the book's Rust blocks so examples do not go out of date; blocks marked `ignore` are skipped.
9. https://docs.vale.sh/ — a prose linter with rules as YAML styles, severities that fail CI.
10. https://understandingdata.com/posts/doc-drift-detection-ci/ — doc drift caught at the merge gate "the same way you catch broken tests"; a mapping table of code paths to doc pages.
11. https://docs.rs/crate/codocia/latest — each Markdown page declares the files it covers; `codocia check` compares content hashes to a snapshot and exits non-zero on stale pages or missing covered files.
12. https://www.stell-engineering.com/blog/requirements-traceability-matrix — (via search summary) an RTM row carries the requirement ID, verification method, evidence location and owner; a link records a planned relationship, not proof that the test passed.
13. `/home/user/wt-v12/docs/PRD.md` at `e17cc80`.
14. `/home/user/wt-v12/docs/crit/prd/owner-messages.md`, all 21 messages.
15. `/home/user/wt-v12/docs/crit/prd/LOG.md`, round 1's applied and declined items.
16. `/home/user/wt-v12/scripts/check.py`, `scripts/checks/*.py` (28 plug-ins, docstrings, `TIER`, emitted codes).
17. `/home/user/wt-v12/tests/*.py` (539 tests, run; `test_route.py:780–850`, `test_round13.py:258–262`, `test_round15.py:193`, `test_round12.py:124`, `test_pipeline.py:47–508`, `test_round7.py:91, 370`).
18. `/home/user/wt-v12/chart.toml` (`[route.rustmapper]` entries and wordings; lines 9, 35–39, 900, 1074–1080, 1153–1160), `/home/user/wt-v12/assets/stats.json` (run-check steps, repos, edition, `repo_count`, `sweep_dates`).
19. `/home/user/wt-v12/scripts/runcheck.py` (docstring, `PROBES`), `scripts/data/route.py resolve()` (run with probes flipped), `scripts/sheets/route.py PURPOSE`, `scripts/tokens.py FLOORS`, `scripts/render_readme.py:459, 670–671`, `scripts/publish_chart.py`, `scripts/build_assets.py:59–60`.
20. `/home/user/wt-v12/.github/workflows/profile.yml`, `/home/user/wt-v12/README.md`, `/home/user/wt-v12/DESIGN.md:26`, `/home/user/wt-v12/docs/BEN-TODO.md:39`.
21. `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/` — `gate.txt`, `sheet-phone-day-390.png`, `sheet-desk-day-870.png`, `page-desk-1.png`.
22. `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/clones/Rust-sitemap` at `32c2651` — `src/robots.rs`, `src/frontier.rs`, `src/cli.rs`, `src/orchestration/shutdown.rs`, `pyproject.toml`, `tests/crawl_exits_when_idle.rs`.
23. `gh api repos/BenjaminSRussell/BenjaminSRussell/pulls/17` (state, mergeable, head).
