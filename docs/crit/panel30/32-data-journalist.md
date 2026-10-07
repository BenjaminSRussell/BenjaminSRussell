# 32 — Data journalist (visual investigations, honest charts, annotation)

I make charts that must survive an editor, a fact-checker and a hostile reader. I recomputed every headline from `assets/stats.json`, read `build_stats.py` / `fetch_repodata.py`, spec-hero §2–4 and spec-supporting §A, looked at soundings-night-2x and hero-day-2x, and spot-checked three repositories against live GitHub (bare clones of go_go_go, rust_llm_logger, game_engine).

## What is good

- **The data is real and consistent.** Every repo's `hours` and `weekdays` sum to its `commits` (21/21); the clones confirm dates and counts exactly. A profile that can be fact-checked is rare.
- **Upright/italic as the certainty convention** is how a newsroom marks estimate vs. measurement. The page's best idea.
- **Soundings D1–D3 has the right skeleton:** one hero number, *dated* HW/LW, a slack-water bracket. A peak without a date is a boast; with a date it is a fact.
- **Chart number = repo count, edition = PyPI version**: metadata that is data.

## What the data actually says

- **One fortnight is a third of the year.** game_engine: 585 commits, 4–14 Jan 2026, 53 a day, 62% in two UTC hours (21–22h), 53% on one weekday; its second "author" is `google-labs-jules[bot]` (105 commits across branches). This agent-assisted sprint sets the largest island (r=77 vs. Scrapy 58), compass north (256 of the 317 commits at 21h), the Tuesday peak (310 of 441) and the tide's HW.
- **Without it the picture inverts and improves:** busiest hour 16h UTC, then 19h; weekdays flatten to Sunday 212, Friday 187; weekend share 24%. The honest headline is *a year of steady evening-and-weekend work on crawl infrastructure, plus one sprint*.
- **The time zone is in the data and discarded.** Author offsets are `-0500/-0400`; `fetch_repodata.py` counts UTC. 21h UTC is 4–5 pm local. The planned colophon line "he works at night" (spec-hero §4) is false, and fixable without claiming a location: count in the author's own offset, label it "author's local time".
- **Duration is the flattering measure, and nothing encodes it.** Scrapy: 331 commits over 378 days, committing today (PR #1113). Rust-sitemap 353 days, FashionDB 344, Data-visualizer 378.
- **9 Nov 2025: nine repositories surfaced in one day.** "First commit" is first push, not project start. Unflattering, and charming if told.
- **7 Oct 2026: 17 of 21 repos touched today** (verified on three). A sweep day that defeats the dormancy rule (`last` within 90 days → "active").
- **Authors ≠ collaborators.** go_go_go's three are *Benjamin Russell*, *BenjaminSRussell* and *Claude*; rust_llm_logger's four include a bot. Two totals (1,828 GitHub-credited vs. 1,868 all hands) need matching captions.
- **"Since Oct 2024"** implies two years; first surveyed commit is 25 Sep 2025. **PyPI:** four releases, all 8 Nov 2025: a packaging afternoon, so "Edition 0.1.3 · Nov 2025", never "four editions". **Followers 46 / stars 0:** one vanity metric hidden, the other printed twice.

## What is bad, ranked

1. **The three loudest claims (biggest island, compass north, HW) are one agent-assisted sprint read in the wrong time zone.** A reader with `git log` finds it in five minutes; then the italic convention buys nothing.
2. **Area ∝ commits is read as effort.** 53/day and 0.88/day on one scale, unannotated, says the voxel engine is the biggest thing he built.
3. **The even-spread tide fallback is a chart of a formula**, labelling plateaus HW/LW with dates that never happened. The clone pass has every timestamp; the fallback should not exist.
4. **"REFRESHED DAILY BY ACTIONS" is a promise printed on a static file.** If the workflow dies, the SVG keeps promising. A dateline states a date, not a cadence.
5. **No methodology.** Nothing defines commit, author, hour, week or active. No source line anywhere.
6. **Followers as an underlined height** sits among measured depths beside 512 and 256, which measure code, not him.
7. **Soundings copy decorates instead of annotating:** "slack water" without a month, HW without a cause, "lifetime commits" without a population.

## What needs to be done

- **F1 Local-time clock.** `git log --format=%ai`, keep the offset, bucket hours and weekdays in author time, normalised per commit-day so no sprint sets north. Label `VAR 16h00 · AUTHOR'S LOCAL TIME`. Delete the night line.
- **F2 One population, named.** Filter to Ben's two identities for `commits`; keep `all_hands` separately. Caption: `commits · 21 public repos · Sep 2025–`. Agents and bots appear nowhere unlabelled.
- **F3 Annotate the cause.** `HW 290 · wk of 5 Jan · game_engine, ten days`; a dotted `typical week {median}` rule; slack water names its month. Full y-scale, no broken axis: the spike is the story, told.
- **F4 Delete the fallback.** `fetch_repodata.py` writes `repos[].weeks` from real timestamps; the tide is their sum, italic until the calendar confirms it.
- **F5 Dateline, not slogan.** `SOUNDINGS TAKEN 7 OCT 2026 · 21 REPOSITORIES · ALL HANDS`. "Daily" lives only in the README colophon.
- **F6 Features carry their survey span**, 11px upright under the name: `Jan 2026` for Game Engine I., `Sep 2025–` for Scrapy Harbor. The one mark that makes area ∝ commits honest.
- **F7 Narrative metrics replace followers:** `378 days surveyed` · `6 languages` · `{n} repos active 9+ of 12 months` · `since 25 Sep 2025`. Drop the underlined 46.
- **F8 Define active** as commits in ≥3 of the last 12 weeks.
- **F9 Source line on every data sheet**, mono 11px: `Source: git history of 21 public repos (HEAD), GitHub contribution calendar, PyPI. Hours in author's local time.`

## Improvements and ideas

1. **(Bold) The year, annotated: a dateline strip (1280×200) under the tide.** Every commit a 1px hairline on one axis, Sep 2025 → today, with four serif-italic callouts: *9 Nov 2025 — nine repositories surfaced in one day* · *8 Nov — rustmapper 0.1.0→0.1.3 in an afternoon* · *4–14 Jan 2026 — 585 commits, a game engine, with help* · *7 Oct 2026 — 17 repositories touched*. Raw data plus annotation is the most honest chart there is, and it turns every gotcha into a told story.
2. **Corrections column.** "Corrected through Notice N" becomes real: `NOTICES.md` logs each methodology change (UTC→local, all hands→author) with a date; N is the count. Journalism's credibility device in chart grammar.
3. **"How we counted"** as a `<details>` in the colophon: six lines defining commit, author, hour, week, active, edition, and exclusions (forks, private, bots).
4. **Encode duration on the coastline.** Area stays ∝ author-commits; the danger line gets one dot per surveyed month (Scrapy 13, game_engine 1). Two variables, two marks, both real.

## What the page says about its maker

Now: a developer who gathered real data, then let one two-week sprint, counted in the wrong time zone, write his headlines, and printed a cadence promise on a file that cannot keep it. The data says something plainer and better: twelve months of steady late-afternoon-and-weekend work on crawl infrastructure in six languages, one shipped package, one burst of agent-assisted play, 17 repositories still tended this morning. The page should say that, dated and sourced, with the sprint a told anecdote rather than a discovered one.

## Five most important lines

1. game_engine (585 commits, 4–14 Jan 2026, bot co-author) sets the biggest island, compass north (256 of 317 commits at 21h) and the tide's HW; without it the busiest hour is 16h and the story is a year of steady work plus one sprint. Annotate it as that.
2. Git author offsets (-0500/-0400) are discarded: count hours and weekdays in the author's local time (no location claimed), per commit-day, and drop the "he works at night" line (21h UTC is 4–5 pm local).
3. Delete the even-spread tide fallback; build `weeks` from clone timestamps now; label HW with its cause (`game_engine, ten days`) and add a `typical week` median rule.
4. Replace "REFRESHED DAILY BY ACTIONS" with a dateline (`SOUNDINGS TAKEN 7 OCT 2026 · 21 REPOSITORIES · ALL HANDS`) plus a source line on every data sheet; "daily" lives only in the README.
5. Filter counts to Ben's two git identities (agents and `google-labs-jules[bot]` named separately), date every named feature with its survey span, define "active" as ≥3 of the last 12 weeks, and swap followers for `378 days surveyed`.
