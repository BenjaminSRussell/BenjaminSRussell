# Round 5 — the hiring screen

Staff engineer, data infrastructure, 44. I screen GitHub profiles for a living: thousands by now. Phone between meetings (eight seconds), laptop when the phone pass earned it (ninety seconds before I open a repo).

## 1. What a visitor needs to know about Ben

Ranked in the order I look, with the v10 verdict.

1. **What he builds, in one line.** v10 has it: "Crawl and data infrastructure · Python and Rust" is the right line, but on a phone it sits under a chart whose own headline is a slogan. Half-answered.
2. **One thing that shipped and that I can run.** Answered well: rustmapper on PyPI, `pip install rustmapper`, three commands. Best block on the page; 600 px below the fold on a phone.
3. **Is he active now, and what shape was the last year?** Not answered. The chart's numbers (11, 8, 26, 22) are "commit-days" with no key. The honest shape, from stats.json in a minute: a dense Sep–Nov 2025, a near-empty Dec–Aug, a September 2026 return, and a 358-commit week ending 7 Oct touching 19 of 21 repos, bot co-authors on most. Hidden, that sweep costs him the interview when I find it. Shown, it is a story I can ask about.
4. **Does he understand the hard part of what he built?** Answered, better than most senior profiles: the governor on redb commit latency, the CRC32-framed WAL, rendezvous hashing by domain, raw-first Delta Lake. Those bullets are the interview.
5. **Is Rust real or a weekend?** Partly: 22 % by bytes, 87 commits over 22 days, a release. Real enough; print the dates.
6. **Tests, CI, releases.** Not answered: no badge row, no tests, no CI. Four PyPI uploads in 75 minutes on 8 Nov 2025 is a publish-fix afternoon; fine for 0.1.3, but "provisional" belongs on no release.
7. **Location, availability, years.** Not answered. `[position]` empty, no LinkedIn or resume; the data knows his timezone (UTC-4/-5) and the page does not.
8. **Stars and followers.** I check, I discount. Neither print nor hide.

Net: the text answers 1, 2 and 4; the chart answers nothing I rank and costs the first phone screen.

## 2. The reference object, and which conventions carry it honestly

What I judge with: the top of a good README (one line, one install, a dated green badge row), a CHANGELOG, and the year's contribution strip. All three are dated and keyed.

Honest mappings:

- **Title block** (name, edition, datum, survey date) = README header. "Datum: main" is a true pun that costs nothing.
- **Source diagram** (the inset showing which survey covered which area, in what year) = which repos were worked, when. The only convention that carries item 3.
- **Tide curve, one year, high and low water dated** = the contribution graph drawn properly. "HW 7 Oct, 358" is honest only if labelled as a sweep.
- **Zone of confidence** = `measured = true/false` in chart.toml. A figure cited by file and sha is A1; the worker pool, where README, PyPI and code disagree, is C. Upright versus sloping figures already do this without a word.
- **Hazard mark** = a known gotcha. "sitemap.xml lies again" is v10's one honest hazard; the pool-size disagreement and 148 stale branches on game_engine are two more.
- **Limit of survey** = data cut-off date, and nothing else.

Forced, and they make me roll my eyes: light characters ("R '2' Fl R 4s": no fact about his work is a flash period); soundings as islands (a repo is not an island; the blob encodes nothing); the compass clock (nobody hires on commit hour); "IALA Region B", the hatching, the boat, the course line.

## 3. The proposal

One sheet, no ship, no water: a **source diagram with a title block**, on v10's paper, in v10's type, inside v10's border.

**Desk, 870 × ~420 px.** Left third, the title block: "Ben Russell" at v10 size; the role line; two project lines: `rustmapper · Rust · 0.1.3 on PyPI · Nov 2025` and `Scrapy Harbor · Python · Sep 2025 –`. At the foot: `Python 46 · Rust 22 · Swift 13 · C 9` and `Datum: main · surveyed 7 Oct 2026`.

Right two thirds: a time axis Sep 2025 → Oct 2026 with month ticks. One row per repository with seven or more commit-days (nine rows) and a last row "12 more" as faint ticks. Each row is a thin rule with a dot on every commit-day (the `days` arrays, which the audit calls sound). Real repo names. rustmapper and Scrapy in dark ink, the rest grey. One italic line over the 7 Oct column: `7 Oct 2026: 19 repositories retouched in one day`. No numbers on the rows.

**Phone, 390 px.** Title block full width, then five rows (Scrapy, rustmapper, Data_science_dev, ideal-url-organizer, game_engine) plus a "16 more" tick row, quarter ticks, nothing under 13 px. The sheet ends above the fold; the install block is first under it.

**Motion.** None.

**The page under it.** (1) Role line and links, `[position]` filled, a LinkedIn or resume link. (2) rustmapper as written, minus "is the survey vessel" and "provisional". (3) Scrapy Harbor as written, minus "is where a run is operated" and "each its own mark in the channel". (4) The four smaller repos under "Also". (5) The collapsed rest. (6) The four principles under "How I build", citations kept. (7) One footer: `21 repositories, author's commits only, surveyed 7 Oct 2026.`

## 4. Details and one-off words

1. `Datum: main`. True, small, funny once.
2. Commit-day marks drawn as the sounding dot, not a square: a stranger sees a dot plot, a sailor sees the lead going down.
3. The retouch day annotated in italic as a hazard, no symbol. Candour I hire for.
4. `0.1.3` upright; "256–1,024 permits" sloping in the text, because README and code disagree. Keep the convention, drop the explanation.
5. v10's border, kept: it smells like the thing without saying so.

## 5. Kill list

- Archipelago, buoys, course, boat, compass clock, "VAR 14h", "IALA Region B", "12 as rocks", "Unsurveyed", "Limit of survey": each names the theme; none carries a fact I rank. His words: it tells you ship's log.
- "Soundings in commit-days": a unit nobody shares, a number nobody reads.
- The three commit totals (1,665 / 1,966 / 1,828): three answers is no answer, and the audit calls them suspect. His words: all over the place.
- "survey vessel", "where a run is operated", "Other waters", "Below the waterline", "Notices to mariners", "Found a wrong depth?", "Survey log", "Small corrections 2026—5—173": every heading says it is a ship. Headings should say what is under them.
- "provisional", "surveyed on 1 of the last 150 days", "instruments: clones live…": a log of the script, not of him. That is the lazy feeling.
- Island aliases ("Game Engine I.", "Profile Shoal"): I look every repo up twice.

## 6. The two-second test

**Two seconds, iPhone:** a name, "Crawl and data infrastructure · Python and Rust", two projects with a year each, and a strip of dated dots that reads as a year of work, busy last autumn and this one. Pass.

**Thirty seconds:** rustmapper installs in one line; Scrapy Harbor is the bigger system; the dots show a quiet spring and a 7 Oct retouch he labelled himself; five bullets say he has thought about backpressure and durability. I open the repo. That is the whole job.
