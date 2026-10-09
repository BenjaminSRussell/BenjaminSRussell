# Round 5 · data memo

Lens: data engineer, 29, metrics pipelines. A number without a definition is a lie in a nice font. I re-measured all 21 repositories today (shallow clones, `ls-remote`, API) before writing.

## 1. What a visitor needs to know about Ben

1. **What he builds, in what.** Crawl and data infrastructure, Python and Rust. *Answered* in text; the chart never says it.
2. **The two real projects and what they stand on.** Scrapy Harbor: 69k lines Python, 257 test files, 5 workflows. rustmapper: 16k lines Rust, on PyPI. *Answered in prose*, measured nowhere.
3. **Is it alive?** Both have commit-days in 5–6 distinct months since Sep 2025. *Not answered*: the chart prints "(SEP 2025)" with no end.
4. **Does it hold together?** 19 of 21 repos have CI config, 18 a tests directory, all 21 a manifest. *Absent.*
5. **How to reach him, how to run it.** Email, `pip install`. *Answered.*
6. **How he works.** Branch-per-fix, agents under direction (1,322 `fix/*` branches on one repo). *Absent.*
7. **Else.** Swift, C, Go. *Answered*, folded away.

## 2. What can be measured honestly, at what cost, and whether a sailor wants it

| fact | definition | cost | verdict |
|---|---|---|---|
| first / latest commit | min/max author-local date of Ben's commits, **sweep days removed** | free | helpful. Raw `last` is poisoned: 17 of 21 repos read 2026-10-07 because 358 commits hit 18 repos that day |
| activity window | distinct months with a non-sweep commit-day | free | helpful; the honest "still maintained" |
| languages by lines | `wc -l` by extension, vendored/generated dirs excluded | free, needs an exclusion list | helpful per flagship, vanity as a pie. game_engine: 5,212 C files over 8 commit-days, generated, not typed; byte shares would call that his C |
| release tags | `git ls-remote --tags` | free | **zero tags, zero releases in 21 repos.** rustmapper's "4 releases" are 4 PyPI uploads in 74 minutes on 8 Nov 2025. One edition; say so |
| dependency manifests | names in Cargo.toml / pyproject / package.json / go.mod / Package.swift, depth ≤2 | free | helpful: "built on" is the first question |
| test presence | count of `test_*.py`, `*_test.go`, `*.test.ts`, `*Tests.swift`, `tests/*.rs` | free | helpful as a count, vanity as a tick. Scrapy 257, rustmapper 3, cozy-game 0 |
| CI config | files in `.github/workflows`; last conclusion needs one API call | free / 1 call | helpful only with the conclusion. rustmapper passed 7 Oct; Scrapy one failure in five, 8 Oct |
| README length | words in root README | free | vanity. 167–2,940 words; nothing to act on |
| hours histogram | commit-days by modal author-local hour, zone −04:00/−05:00 | free | marginal. "Afternoons, US Eastern" is true and dull |

Conventions, mapped honestly:

- **Depth** = a quantity you can be wrong about at one spot: commit-days per project per month, sweeps out. Works. Commits do not: Data_science_dev put 48% of its 308 in one day.
- **Channel** = the maintained route: months Sep 2025 → Oct 2026 with soundings along it. Works.
- **Light character** = a periodic signal, lit when due: CI that runs on every push and last passed, conclusion printed. Works. v10's `Fl R 4s` is a string constant (`hero.py:960`). Forced.
- **Tidal diamond** = a table of values at a place: per-project panel, built on / tests / checks / lines / corrected. Works exactly.
- **Edition, small corrections** = when last corrected: page redrawn weekly; per project, last non-sweep commit. Works.
- **Hazard** = a known gotcha: "pip builds from source without a wheel"; worker count disagrees between README, PyPI and code (`claims.workers.measured=false`). Works.
- **Rocks**: a danger to you; twelve small repos are not. **Limit of survey**: he ruled on it. **Variation**: corrects a bearing; the modal hour corrects nothing. Forced, all three.

**Lazy data, by name.** *Commit totals*: three on one page (1,665 / 1,966 / 1,828) from three definitions (author-filtered clone, all hands, GitHub's calendar), and game_engine's 246 commits on 13 Jan 2026 weigh a month of Scrapy. *The contribution calendar*: the same counts as squares; 7 Oct 2026 would be the brightest day of the year, and it was housekeeping. *Stars* (0, 1, 1), *followers*, *branch heads* (1,645 on Data_science_dev, agent-made), *issue counts* (98 of Scrapy's last 100 opened by himself), *workflow runs* (3,804). Machinery, not work.

## 3. The proposal

One still image, "Approach sheet". 870 wide at desk, 390 on the phone.

**Desk.** Left 60%: title block top-left, name 56px, "Crawl and data infrastructure · Python and Rust", small caps "Soundings in commit-days · Datum: main · Edition 7 Oct 2026". Below, a horizontal channel with 13 month ticks Sep 2025 → Oct 2026. Seven tracks, one per project with ≥7 commit-days (Scrapy Harbor, rustmapper, Data_science_dev, Data-visualizer, Wheel, FashionDB, ideal-url-organizer; game_engine and the profile repo excluded, see kill list): a thin line from first to last non-sweep month, the month's commit-days printed as a depth figure, blank where zero. Right 40%: two diamond panels, Scrapy Harbor and rustmapper, five rows each: *Built on* (top five manifest names), *Tests* (file count), *Checks* (workflow count, last result, date), *Lines* (non-vendored, by language), *Corrected* (last non-sweep commit). Bottom rule, 9px: "Sweeps 9–10 Nov 2025, 1 and 7 Oct 2026 excluded."

**Phone.** Title block, the two panels stacked full width, then the channel with four tracks and month initials. Nothing moves. No boat, no lights, no hatch.

**Page under it:** links line; "Ben Russell builds" paragraph; rustmapper and Scrapy Harbor blocks (keep); "Other work", four items; details retitled "Fifteen more"; the four notices retitled "Working rules"; one provenance line: "Measured 7 Oct 2026 from clones of 21 repositories, author's commits only, sweep days excluded; redrawn weekly." About 650 words.

## 4. Details and one-off words

1. "Datum: main" stays. The reference everything is measured from; so is the branch.
2. "Edition 7 Oct 2026", under it "Small corrections weekly". True, and how a chart says it.
3. The sweep footnote names its dates. A sailor knows a sweep is a survey pass, not weather.
4. "Checks · 5 · one failed 8 Oct" on Scrapy's panel. Print the failure. Honesty is the detail.
5. The hours dial, if kept, labelled "Local −04:00". Zone time.

## 5. Kill list

- "HW · SWEEP 358": the biggest number on the chart is a housekeeping day. This is the "all over the place".
- `R "2" Fl R 4s`, `G "1" Fl G 4s`: constants. Fake instruments.
- "12 AS ROCKS", the fringe: small repos are not hazards.
- "LIMIT OF SURVEY", "UNSURVEYED", the hatch: "not smart".
- "VAR 14h": wrong convention for the fact.
- The boat and anchor: not artfully done.
- "Game Engine I.": 8 commit-days on a generated engine is not coastline.
- Survey log with three commit counts and "instruments: clones live": pipeline status belongs in the pipeline.
- "Survey vessel", "Below the waterline", "Notices to mariners", "Found a wrong depth?", "Other waters", "IALA REGION B", "CHART NO. 21": each names the metaphor.

## 6. The two-second test

Two seconds on an iPhone: a name, "crawl and data infrastructure, Python and Rust", a dated edition, two tables of numbers that look checked. Odd that it is drawn like a chart.

Thirty seconds: two real systems, what each stands on, both tested and checked, the months each was worked, a page re-measured weekly that says what it leaves out, then the install line. The word "ship" never appears.
