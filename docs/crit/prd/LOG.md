# PRD review log

## Round 1

11 Oct 2026. Reviews: `review-r01-1.md` (the owner's lens) **7 / 10**, `review-r01-2.md` (a product manager who
rejects vague PRDs) **6 / 10**, `review-r01-3.md` (an engineer who trusts nothing until the code says it) **6 / 10**.
All three answer **yes** to "is the product this PRD defines what he wants": reviewer 1 on 9 Oct 11:37 ("what I'd
want are very helpful information... The map, very helpful... It should be telling you about me"), reviewer 2 on
"It has to be helpful knowledge... in a cool format" and "Everything, single thing inside of this needs a purpose",
reviewer 3 on the same 9 Oct 20:50 sentence, confirmed against `PURPOSE`. Reviewer 1 adds the condition the PRD
already names: the page as it ships under option 3 is not the page he wants, because its first screen says his
flagship ships with a stop-rule. Where two reviewers conflict, reviewer 1 wins; the one conflict was §8.3 (reviewer 1
wanted a sixth judged question, reviewer 2 wanted question 5 made advisory): both applied, with q.5 and q.6 advisory
and q.1–4 the bar.

Every fact added to `PRD.md` in this round was checked here: the resolver (`scripts/data/route.py resolve()`) was run
on today's `stats.json` with each §5.4 probe flipped; the clone of `Rust-sitemap` at `32c2651` was read for each
§5.4 fix; `column.py`, `expiry.py`, `strings.py`, `test_route.py`, `publish_chart.py`, `profile.yml`, the build
report and `page-desk-1.png` were opened for the rest; PR #17 via `gh api`.

### Applied

| Id | What changed in `PRD.md` |
|---|---|
| r1 MF1, r2 MF4 | §9.1 rewritten: options 1a (minimum: exit, robots, packaging) and 1b (full), 2, 2b (keep the box, cut the open list to L1 and L7), 3; a column for what the first phone screen says and what the list becomes under each; cost and who (Ben or a session with push access); default while undecided (unmerged); decide-by (before the merge, which triggers a build); size stated as what is at HEAD, no invented day count; the owed renders in §9.3 with the fixture that produces them. Also §0 bullet 5. |
| r1 MF2 | §3: rows G1a (layers of depth: the loop bracket, the gap, the hand-off line), G1b (what it says about the person who made it), G1c (stunning and fun / not cool enough, with the 9 Oct trade written down). |
| r1 MF3 | POSITION-EMPTY moved from §8.2 to §8.1 item 6 (position line and one contact set before merge; owner Ben); §9.2 and G13 point there. The owner lens; no code changed. |
| r1 MF4, r2 MF5 | G8 ruled by his sentence: off by default; G8 marked open on the facts lines (not "test"); §9.2 is now a decision row (strike / keep / share without totals, strike recommended); §10.5 names the exact gap (`render_readme.py:459` calls `agent_clause` unconditionally; no `[facts]` switch). The page itself is unchanged (product). |
| r1 MF5, r2 MF2, r3 MF8 (part) | Line 8: 21 messages, appendix A excerpts the 15 that set a rule and lists the six it leaves out; appendix A retitled "excerpts; verbatim where quoted"; the 11 Oct (later) message added. Line 3: "at `027f081` plus this document and its review rounds". |
| r1 MF6 | §2 reworded in his order: both devices, the phone the stricter constraint, the web the likelier reader; §5.3 row 6 says the comment lines wrap for the phone; §11 records the desk cost (`page-desk-1.png`); §10.16 the one-line fix if a ≤ 32-column wording exists. |
| r1 MF7 | §7.1 new row (no theme word in a `chart.toml` string a live sheet reads; retired modules deleted), status open; §10.8 lists the five keys (`chart.toml:35–39`), their only readers (retired `soundings`, `approaches`, `footer`), `SHEETS = ["hero"]`, and the fix. Product unchanged. |
| r1 MF8 | §8.3 q.6: would the reviewer screenshot the image and what would they say it was; §11's flowchart risk now says it is asked every round. |
| r2 MF1 | §8.3: q.1–4 are his bar with tickable lines; q.5 advisory, not his; "Done =" defined (§8.1, §8.4 logged, §9.1 decided by Ben, three yeses on q.1–4, no open must-fix); round 16's block named as §9.1. |
| r2 MF3 | §6 line on the failure path corrected (last week's figures, old dates, no stale mark; `no_sounding` read only by off-page sheets; the one test builds `log`); §6.1 Failure and rollback added (fetch fails / gate fails / bad build passes: `git revert` on `main` plus a `workflow_dispatch` rebuild; the orphan `chart` branch has no history to roll back). The stale-mark decision is §10.13. |
| r2 MF6 | One home each: G5 is a pointer to G2 (no themed headings folded into G2); the device check lives in §8.4 (G4, §7.4, §9.3, §10.4 point there); the README theme-word gap in §10.1 (G2, §7.1, §8.3 point); the retirement list in §5.4 (§9.1 cites rows); "nothing moves" in §4 only (§5.1 and §5.2 mentions removed). |
| r2 MF7 (part) | §0 opens with what the document is and a reading order (build/accept: §1, 2, 4, 5, 8, 9, 11; register: §3 last column, §7, §10, app. B; process: §7.6, G17–G19); the scores are dated as going stale; lines 3–6 folded into §0. The two-part split and moving appendix C are declined below. |
| r2 MF8 | §8.3 lines per review-held rule (winks ≤ 2, named; the README grep; the spelling grep list; garden paths; density by construction); §8.4 pass conditions (Safari serves phone-day/night by mode; the app shows phone-day via the `<img>` fallback, the light-theme report cited as unverified; ≤ 900 CSS px; first two screens). |
| r2 MF9 | §5.3 gained a "Held by" column: row 2 `test_round7.py:370` and `test_pipeline.py:495`; row 3 `test_round7.py:91` (set and "Python, Rust; " first; the rest's order untested, §10.15); row 11 block order only; row 12 named "the provenance line" with `test_provenance_line_is_from_stats_only` (`test_pipeline.py:307`); the image link `test_pipeline.py:208`. "Survey-line test" and "sounding" are gone from the prose. |
| r2 MF10 | §8.5 After merge: owner of a failed run, re-measuring the GitHub constants, the 2027-06 expiry, "no success metric is set; done is §8.3" with the one cheap referrer check offered, who edits `chart.toml` copy. |
| r2 MF11 | Line 45 deleted; lines 3–6 folded into §0; §2's 7 s cites R4-F1. |
| r3 MF1 | §0 bullet 3: four of eight retire on their own, three need a probe or wording here, one is a hand switch; §5.4 gained columns "At HEAD `32c2651`?" and "Needs here, first", each cell from the clone or a resolver run (and a fifth gap found the same way: X1 goes unverified when both export probes fail); line 172 names W1's `drawn = false`; §10.9 is the product work; §11 carries the risk. The probe and fallbacks are not written (product). |
| r3 MF2 | §5.2 mid row: 11.2 px at 852 to 17.7 px at 1,199, floor 11, under the phone's 13 up to 930; §7.4 row says the mid window's only floor is 11; the phone-at-360 cell corrected to 12.0 px (the floor is 11); §9.3 and §11 carry the trade for his call; §10.14. Product unchanged. |
| r3 MF3 | §5.2 and §7.4: ≤ 900 px from a 768 px viewport up (`TALL_FROM`); below 768 the phone sheet is 1.87 × the column (575 at 390, 968 at 600, 1,280 at 767). |
| r3 MF4 | G14 and §7.5: EXPIRY warns, never fails; the thesis line held by an absence only; `BEN-TODO.md:39` named; §10.10 is the fix (BANNED entry, strike the line). Product and BEN-TODO unchanged. |
| r3 MF5 | §7.1 "no ships" row: review; T-PURPOSE holds containment only, with what the test does and does not check; G9 says so; §10.11. |
| r3 MF6 | §7.2 first row: gate one-way (drawn → row), test the other way with the hand list `{S2, W1}` at `test_route.py:819–822`; §10.11. |
| r3 MF7 | §7.6 new row: every open PR mergeable, not met today (PR #17 open and mergeable, this branch has no PR); §7.4 new row: editions on the `chart` branch before the README names them, with its three holders; G17 cites 7 Oct 16:12, G19 cites 7 Oct 17:58, 9 Oct 11:35 ("Where's the fucking opinions") and 11 Oct (later). |
| r3 MF9 | §5.1: F1 says the printed words are the second wording and why; H1 names all four probes; S1 says the command is dropped without `crawl_help`; W1 corrected (holds because the kill failed; undrawn by the switch). Appendix B: the fifteen `data.*` codes with `tide`/`variation` idle, the seven `log.*` codes idle; "v7" removed from the banned list and the 20 real entries listed. |

### Declined, or applied only in part

| Id | Why |
|---|---|
| r2 MF7 (the two-part split; appendix C to LOG.md) | The fix pass keeps section numbering stable (every review and `LOG.md` cite §-numbers), and his 11 Oct 01:12 instruction asks for the rules and how they are implemented in one document. Applied instead: the reading order in §0, the dated scores, lines 3–6 folded. A later round may split it once the numbering has fewer readers. |
| r1 MF1 (the render of the option-1 outcome) | Not produced in this pass: the 1b fixture fails the build today (L1/L4/L7 unverified, verified by running the resolver), and producing renders is a build step, not a PRD edit. Recorded in §9.3 with the exact fixture; the 1a render can be built now. |
| r3 MF1 (write the probe and the fallbacks), r3 MF4 (BANNED entry, strike BEN-TODO), r3 MF5/MF6 (test assertions), r3 MF8 (`tests/test_prd.py`), r1 MF7 (delete keys and modules), r1 MF4 / r2 MF5 (the `[facts]` switch), r2 MF3 (the stale mark) | Product changes; this pass edits only the PRD. Each is in §10 (items 5, 8–13) with the reviewer's reason and the exact file and line. |
| r2 MF4 (a size in days) | Declined for the number only: the PRD prints no figure it did not measure (§7.3's first rule), and a day count for Rust work would be invented. §9.1 states the size as fixes, what is at HEAD, and what is needed here; the days are his to estimate. |
| r2 MF10 (one success metric) | Applied as "none is set; done is §8.3", with the referrer check offered rather than set: nothing in his words asks for a metric, and setting one on his behalf would be a rule he did not make. |

### Next round

Look at §5.4 and §9.1 together: build the 1a fixture render, check every "Needs here" cell against the code once §10.9
exists, and judge whether the decision table now lets him choose from the first-screen sentences alone.

## Round 2

11 Oct 2026. Reviews: `review-r02-1.md` (the owner's lens) **7 / 10**, `review-r02-2.md` (a product manager who
rejects vague PRDs) **7 / 10**, `review-r02-3.md` (an engineer who trusts nothing until the code says it) **7 / 10**.
All three answer **yes** to "is the product this PRD defines what he wants": reviewer 1 on 9 Oct 11:37 ("It should be
telling you about me, but with a layer of a theme of shipping... It has to be helpful knowledge") with the 20:50
purpose test; reviewer 2 on 11:37 ("helpful data that you're looking at... in a cool format") and 20:50; reviewer 3
on 20:50 ("Everything, single thing inside of this needs a purpose") and 11:37 ("The map, very helpful. The fucking
log, not really"), confirmed against `PURPOSE` and ROUTE-PURPOSE. What all three found: the one decision in §9.1 was
framed as if waiting were free while the live page is the v11 map he rejected (r1, r2); two of his sentences were
carried narrower than he said them (r1: G10, G13; r3: G8, G4); the round-1 rulings (the `[facts]` switch, the theme
strings) were required by nothing (r1, r2); §6.1's rollback path did not exist and the weekly job's one scheduled
run had failed (r2); §7 cited 50 of 160 live codes (r3).

Conflicts, resolved on the owner lens (reviewer 1 wins): (1) §9.2's G8 default: reviewer 3 asked that the default
"stay off until he picks one" with both sentences printed; reviewers 1 and 2 asked that "strike" stay the default and
block the merge. Applied: both sentences printed whole in G8 and §9.2 (r3), default strike, not yet implemented,
blocking (r1, r2). (2) §10.8's owner: reviewer 2 set Ben (he is told to edit `chart.toml`); reviewer 1 asked for the
deletion before merge. Applied: a session, blocking the merge (§8.1 item 8). (3) §10's blocking column: reviewer 2
set "blocks merge: none"; reviewer 1's MF5 makes 5 and 8 blockers and reviewer 2's own MF6 makes 5 one. Applied: 5
and 8 block the merge, 4 blocks it through §8.3's "Done", 9 blocks 1b, 19 blocks the 2b merge.

Every fact added to `PRD.md` in this round was checked here: the live `main` README, the `chart` branch's head and
group ids, PR #17 and the 12 workflow runs with run 12's job log (REST, `gh api`); `profile.yml` lines 13–28, 106,
157; `build_stats.py` modes; `render_readme.py:459, 670–671`; `column.py:44–63`; `chart.toml:9, 13, 24–39, 563, 667,
900, 1074–1160`; `runcheck.py:7`; `checks/data.py`, `position.py`, `readme.py`, `size.py`, `xml.py`, `alt.py`,
`notices.py`, `expiry.py`, `route.py:60–80` and `tokens.py:131` for the §7 rows; the 160 distinct codes counted over
every `fail`/`warn`/`error`/`info` literal in `scripts/checks/*.py`; the 539 tests counted per module by a loader
walk (`test_chartlib` 22, `test_edition` 11); `grep chartlib. scripts/sheets/route.py` (one call, `stroke`); the
phone sheet's height ratio (1,121 / 600 = 1.868; 900.5 px at a 482 px column). Outside sources re-read for the
sentences the PRD now carries: INT 1 (Nippon Foundation mirror, routeing symbols "usually magenta", recommended
tracks "dashed lines with arrowheads (colour black)"); AM Nautical on dotted or pecked danger lines; GitHub docs
"About anonymized URLs" (Camo, `curl -X PURGE`); GitHub community discussion #46691 ("The cache is set for 5
minutes"); FLUID-6626 (varnish, 300 s); Underdog ("the 30-Second Scan"), TechInterview ("Total time: 30–90 seconds"),
GreatFrontEnd ("In the first minute"); Stanford GSB on the blemishing effect (positive first, minor, "does not hold
if the negative information is very strong").

The 1a render was produced this round (reviewer 1's MF4; round 1 said it could be built): the session's
`scratchpad/prd-r02/once-1a/` (`stats-once-1a.json` from today's `stats.json` with `ends_by_itself` and `robots_read`
passing, `robots_stall` failing, `edition.scripts = ["rustmapper"]`, routes re-verified against the clone at `32c2651`
and the local 0.1.3 sdist by `refresh_routes_1a.py`; the sheets, `README-1a.md`, `sheet-phone-day-390.png`,
`sheet-desk-day-870.png`, `page-phone-1..7.png`, `page-desk-1..2.png`). The gate on that build: the round-16
warnings and one REPORT-STATS fail that hashes `assets/stats.json`, not the fixture. No product file changed.

### Applied

| Id | What changed in `PRD.md` |
|---|---|
| r1 MF1, r2 MF2 | §9.1: a "What is live while this is undecided" paragraph (the v11 sheet at `chart` `c488907`, the alt text quoted, "last commit 8 Aug 2026", the first-person footer, the thesis line pending PR #17, the red run 12); row 0 "Leave `main` as it is" with its cost (G8, G13, G14, G15, §7.3, §7.5); "the rows are not alternatives" (four §5.4 rows retire on `release-published` with no edit here; 0 → 2b reversible); default changed from "unmerged, `main` does not change" to **merge 2b now, then decide 1a against 1b with the renders**, with why 3 is not the better immediate merge; decide-by split (2b before the merge; 1a/1b before the release); 2b's one change here named (`LIST_MAX_ITEMS`, `fold = true`; §10.19). §0 bullets 5 and 6 rewritten to match. The PR: §10.17 (the fix pass does not push). |
| r1 MF2 | G10's meaning is his two rules (no pirate talk, no running bit; a one-off word as a joke allowed, "that's funny"; more than a couple "cringy"), quoted at length; G1c's trade: he overrode naming the theme and running bits, "stunning" and "fun" still stand and are judged at §8.3 q.6; §7.1's wink row aligned (neither wink uses the allowance; nothing bars a later one). |
| r1 MF3 | G13 split: G13 keeps "telling you about me" (third person); new G13a "with a layer of a theme of shipping" (the manner in the marks, held by review at §8.3 q.6, the round-2 answers logged in the row). §1 cites INT 1 and the danger-line convention, calls the magenta line a routeing line ("this document calls it the track, R5"), and says the double reading is intended. §8.3 q.6 logs against G13a. |
| r1 MF4 | The 1a render built and its paths, fixture and what it shows (no box, no gap, five items, 982 units against 1,121) put in §9.1 beside round-16's; §9.3's render bullet is now the 1b render only; §9.1's intro says which render exists. |
| r1 MF5, r2 MF6 | §8.1 item 7 (`[facts] agent_clause` exists, defaults to `false`, no counts on the merge commit unless he writes keep/share in LOG.md; fails today, with the lines) and item 8 (the five `[copy]` keys and retired modules deleted; fails today); the rule "a §10 item that blocks the merge is also a line here"; §10.5 and §10.8 marked blocking; §9.2 says "default: strike; not yet implemented; blocks the merge"; G8's and §5.3 row 5's holders point at item 7. Product unchanged. |
| r1 MF6 | §2's Q1 cell: 7 s is R4-F1's estimate; the guides read this round say 30 s to a minute (three quoted); none is measured; the first-screen rule rests on "first screen". |
| r2 MF1 | §6.1's third row replaced: no CI path rebuilds from an older `stats.json` (`profile.yml:106` re-surveys on every trigger; the revert is a push because `assets/log.json` is in the commit, line 157, and in `push: paths`, line 24); the local rollback steps; code or `chart.toml` reverted first; the `chart` branch has no history. §0 "Built" and §8.5's first bullet carry the 12 runs, the one commit (`d253286`) and run 12's failure at `Unit tests` with the two test names and the run id. Product unchanged (the failing tests are `main`'s v11 code). |
| r2 MF3 | Lines 3–4 replaced by a header: Status (draft, blocked on §9.1), Owner of the decision (Ben), Owner of the text (the session; edited only in a PRD round or when the product changes), Baseline (`027f081` code; figures read at `e17cc80`, re-checked in round 2), Last updated. §8.1 item 2 is the no-network build from the committed `stats.json` with the three commands; a fresh survey is item 4's. |
| r2 MF4 | §10 is a table: id, gap, fix (file), blocks, owner, status; ids 1–16 stable, 17–20 added; closed items (2, 3, 6, 14) kept as one line each with their reasoning here; the rule at the top. |
| r2 MF5 | §9.1b: the mid-window trade as a decision table (a: accept in writing, recommended and default; b: serve the phone sheet to 930, which fails HERO-COLUMN-PX at 852 by half a pixel, computed; c: a narrower mid sheet); decides Ben. §5.2, §7.4, §9.3, §10.14 and §11 are pointers. |
| r2 MF7 | §8.4: owner Ben (the session has no device), the log named (`docs/crit/round6/LOG.md`, under the merging round, with screenshot paths; neither LOG has an entry today). §8.3: Done means ready for Ben to merge, his merge is the acceptance (§7.6); "must-fix" means a product-review must-fix; q.5 says his merge, not "ship it". |
| r2 MF8 | §11: the stale-sheet window after each run (raw 300 s, Camo on top, same paths force-pushed; accepted; the run-named-sheet option costed, §10.20); §8.5: Ben purges a sheet stale past a day (`curl -X PURGE` on the Camo URL, sparingly). |
| r2 MF9 | §0's per-round scores reduced to one line pointing here; "scheduled for" 06:20 with run 12's 12:52; `LIST_MAX_ITEMS`/`LIST_MAX_WORDS` named in §5.3 row 6 and §9.1; §9.2 bullets 3–5 each given options, a recommendation and who decides; line 10 says "a clone at that commit" and where the session's is. |
| r3 MF1 | §7 preamble: 160 codes from 28 plug-ins, 50 cited in round 1, the engineering rules added to the table nearest their subject. New rows: §7.3 (the `data.*` invariants with fail/warn levels from `checks/data.py`; the position line and contact placeholders; the README picture block), NOTICE-CITE on the cite row; §7.4 (SIZE-*/REPORT-* with the budgets from `tokens.py:131`; XML-* with the forbidden elements; ROUTE-HEIGHT/-PAINT/-ARROW/-MISSING/-HANDOFF with the heights from `checks/route.py:70`), BOUNDS and CONTRAST wildcards expanded; §7.5 (ALT-LAST/ALT-POEM with the poem line from `chart.toml:563`; EXPIRY-KEY/-FORMAT). Appendix B unchanged. |
| r3 MF2 | G8 prints the 11:35 sentence whole and adds the 11:37 sentence; §9.2 says "He said both"; the default stays strike on the owner lens (above). Appendix A untouched (verbatim by rule). |
| r3 MF3 | §6: 91 off-page tests (`test_chartlib` 22 added, with what it tests and that the route calls `stroke` only); the product's count 448; `test_edition` noted; §10.8 lists `test_chartlib` and the unused `chartlib` functions. |
| r3 MF4 | G4 cites "The images are all crushed" (8 Oct 14:22) before the 9 Oct quote. |
| r3 MF5 | §6: 17 of 18 probes are named by a wording; `resume_after_kill` is read by nothing; `runcheck.py:7` says "four"; §10.18 and §5.4 row 7 point at it. The docstring itself is product (not changed). |
| r3 MF6 | §0 bullet 1: the register's claims were checked by hand on 11 Oct 2026 and are checked by nothing since; §7's preamble: status is what the holder did on the round-16 build, not a promise. |
| r3 §4 (not a must-fix) | §7.6's PR row carries "Resolve all merge conflicts" (no conflicts) beside "ready to merge". |

### Declined, or applied only in part

| Id | Why |
|---|---|
| r1 MF1 (open the PR) | The fix pass is told not to push, and a PR needs the branch on the remote. Recorded as §10.17 with an owner (a session with push, or Ben); §7.6's row says so. |
| r1 MF5, r2 MF6 (the `[facts]` switch), r1 MF5 (delete the keys and modules), r2 MF1 (the red run on `main`), r3 MF5 (the docstring), r2 MF8's run-named sheets, r1 MF1's 2b change | Product changes; this pass edits only the PRD and this log. Each is in §10 (items 5, 8, 17–20) with the reviewer's reason, the file and line, an owner and a blocking state, and the two he ruled on (5, 8) are now §8.1 items 7 and 8, so the merge cannot pass without them. |
| r2 MF4 (closed items moved out of §10) | Applied in part: items 2, 3, 6 and 14 stay as one-line rows so their ids stay citable (§3, §7, §8 cite §10.1–§10.16 by number); their reasoning is this log's. |
| r2 MF5 (§9.1b's option b as costed by the reviewer) | Applied with a correction: the second breakpoint is `mid_from_px` (`chart.toml:13`), not `breakpoint_px` (`chart.toml:9`, the desk breakpoint), and b fails HERO-COLUMN-PX at 852 (900.5 px > 900) as the gate stands, so it is not the one-number change the review described. |
| r2 MF9 (§9.2 bullets 3–5 to `BEN-TODO.md`) | Given options in §9.2 instead; `BEN-TODO.md` is outside this pass's files. |
| r3 MF2 (appendix A's 11:37 excerpt) | Appendix A is kept verbatim by the fix pass's rule; the sentence is in G8 and §9.2, and the full message is in `owner-messages.md`. |

### Next round

Read §9.1 as he would: does row 0, the 1a render and the sequenced default let him decide in one sitting, and is
§8.1 (items 7 and 8 now blocking) something a session can clear in one fix round before the 2b merge.
