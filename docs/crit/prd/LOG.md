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
