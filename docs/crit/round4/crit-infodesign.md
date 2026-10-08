# Information-design review — what is measured, how it is encoded, whether it tells the truth

Read: readme-light.png in five slices, the six 870 px day sheets, 2× crops of the hero's island clusters and the Soundings curve; `assets/stats.json` tabulated per repo (commits, all-hands, bot share, commit_days, months_active, first/last, biggest day); DESIGN.md; recrit3/crit-owner.md (not repeated here: neatline strike-through, duplicated prose, notice inflation, Other-waters blurbs are all already on the list).

## 1. What the page measures, and whether it is the right measure

The page measures one thing, commits, and prints it four times in three disguises: as island area and sounding figure on the hero, as weekly totals along the hero's course, as the 52-week curve and figure rows on Sheet 2, and as the 21-cell register. Everything a stranger is invited to read as "size of work" is a commit count.

Commits are the wrong marginal of this table. The data itself says so:

- 1,665 commits fell on **77 distinct days** out of 377 surveyed (20 % of days). 32 of the last 52 weeks are zero.
- `game_engine`, the largest island, has 512 commits on 8 days; **447 of them (87 %) on two days** (201 on 11 Jan, 246 on 13 Jan), 73 of the 585 all-hands by a bot, and 148 stale branches. It is dormant.
- The "HW 358" that headlines Sheet 2 and the hero course is **one calendar day (7 Oct 2026) touching 18 repositories**; `stats.json` already classifies it as a `sweep`. Course_crusader got 29 commits that day, 88 % of its lifetime total. The chart's highest-profile number is a housekeeping event wearing the name of a project.
- Meanwhile the two projects the prose says he is: Scrapy 26 commit-days over 5 active months, rustmapper 22 commit-days over 6 active months. By commit-days they are first and second by a wide margin; by commits they are third and fifth, and rustmapper (87₆) is drawn smaller than the profile repo (173₄).

Commits reward squash-style bursts, generated code and mass edits; commit-days reward showing up, and are immune to all three. `commit_days` is in the file for every repo. So are `months_active`, `first`/`last` (span), `others[].commits` with `bot: true`, `days[]` (date, hour, n) per repo, `languages[].share`, `edition.releases`, and three source-cited `claims` with SHAs. The truer story is sitting in the JSON and the chart does not draw it:

| what | where in stats.json | currently shown? |
|---|---|---|
| days he actually worked on each repo | `repos[].commit_days` | subscript-size on Sheet 3 legend only; not on hero |
| how long each repo has been alive | `first`, `last`, `months_active` | months as an 8 px subscript (265₅) |
| how much was him vs a bot | `others[]` with `bot` | aggregate only (1,665 / 1,966); per repo it is 100 % to 44 % (rustmapper 45 of 132 by "Claude", FashionDB 30 of 69, Spotify 10 of 18). DESIGN.md promises "two instruments wherever one is" and the hero shows one. |
| when in the day he works | `hours[]` (24 bins, 150 commit-days) | collapsed to one integer, "VAR 14h" |
| language mix | `languages[].share` (Python .46, Rust .22, Swift .13, C .09, TS .06) | never drawn as a quantity; Instruments prints names and first dates |
| releases | `edition` (4 uploads, 8 Nov 2025, 74 minutes) | as "Notices 6–9" |
| sweeps | `sweeps[]` | drawn as high water |
| checkable engineering facts | `claims` (256–1,024 permits, num_cpus shards, 15 s scrape, each with a SHA) | in prose only |

Missing from the data that a stranger wants and the survey could take: per-repo language (`language` is null for 17 of 21), a one-line description per repo from GitHub, PyPI downloads (the PyPI instrument is live), whether CI passes, any contribution outside his own repos (the survey clones only his own; a stranger wants to know if he has ever had a PR merged elsewhere), repo size or line count as a second axis so a 4-commit repo and a 300-commit repo can be told apart by substance.

## 2. Do the encodings carry information or decorate it

**Island area ∝ commits.** Honest by assertion (within 8 %) but mis-targeted and redundant. The proportional boundary is the 5-contour, i.e. the outer edge of the pale tint; what the eye segments as "the island" is the tan land, and that is not proportional (Game Engine's land is about the size of Data Science Bank's, its halo is what makes it the largest). Area is also the weakest quantitative channel after colour (perceived ratios compress; 512 vs 87 should read 6×, it reads about 3×), and the figure is printed inside anyway, so the area adds nothing the numeral has not said. Area here is decoration that happens to be calibrated.

**Depth as commits.** This is the lie by implication. The sheet is titled SOUNDINGS IN COMMITS; a sounding is a depth; a chart reader expects bigger numbers in deeper, safer water. Here bigger numbers are higher land (512 sits on an island), and the same unit is printed in the water along the course for a different quantity (weekly totals, 296, 240). Two marginals of one table (per-repo sums and per-week sums) share a single surface and a single unit, and the contours are interpolated across x–y positions that are pure layout. A contour on this chart means "near something with a big count" and nothing else. At 870 px the 10/20/50 contour figures are illegible; the rings read as halos. Contours: noise that implies a continuous field where there is none.

**The course.** Time with no axis. The pecked track from Scrapy Harbor to rustmapper carries the 52 weekly totals, but the reader cannot recover order, dates or spacing, and it visually asserts a route between repositories that is only metaphor. Sheet 2 shows the same 52 numbers with an axis. The hero course is a worse copy of Sheet 2 placed above it.

**The rose as a 24 h clock.** Twenty-four measured values reduced to one hand pointing at 14, with "14h" printed under it. The hand carries zero bits beyond the caption. The hours histogram is actually interesting: 115 of 150 commit-days fall 10:00–18:59 (77 %), which says "daytime worker, not a 2 a.m. hacker"; it is not drawn.

**Subscripts.** The one glyph that carries the more honest measure (months active, 265₅) is set at footnote size and footnote position, and the same glyph means "thousands/hundreds" on Sheet 3 and "days" on Sheet 2. One sign, three meanings: a Bertin failure on its own.

**Sheet 2's curve.** A spline through 52 weekly bins with 32 zeros. Smoothing invents shape: the one-day 358 becomes a hill with a leading slope; 240 and 296 in consecutive weeks become a plateau; a fill under the curve implies a continuous quantity. The two staggered rows of figures below detach the numbers from their bins. The 21 cells' sparklines are invisible at 870 px (a flat rule with, at most, one bump). Honest data, dishonest line.

**Sheet 3's URL field.** Every sounding is sloping, i.e. invented. That is a sheet of fabricated numbers with a legend that says so. The honest content on the sheet (stage names, Delta Lake / Redis / Postgres, zones A/B/C, the robots.txt box) is a *mechanism*, which a diagram can show without any numbers.

**Sheet 4.** Every figure in the log except the last line is italic, i.e. the entire artefact is a simulated run. Italic in a typewriter face at 19 px is barely distinguishable from upright; the convention is doing legal work, not visual work.

**Unsurveyed margin.** Pure metaphor (`unsurveyed: []`) costing 12 % of the width on four sheets. It would become true if it meant *time after the survey date*.

Legible and honest at 870 px: the island figures, the register figures, Sheet 2's figure rows (if aligned), the Instruments dates, the contact row. Noise: contours, course, rose hand, sparklines, Sheet 3's field, the log's numbers.

## 3. The upright/sloping convention; the ship's log

The convention does not survive without the legend, and even with the legend it is a disclaimer, not an encoding. Italic is already the voice of water names, notes, the thesis, and sea names, so a sloping figure next to *Delta Lake* reads as "place", not "unmeasured". The rule a data graphic should follow is simpler: **a figure that was not measured is not printed as a figure.** Once that rule is kept, the convention has nothing left to mark and can be retired, or kept as a build check that *forbids* sloping figures rather than licensing them.

The ship's log, as computed fiction, is not worth a sheet. It is a product demo dressed as evidence, on the sheet that looks most like evidence. It is worth a sheet only if the run is real (a fixture site crawled in the nightly workflow, times and req/s recorded, signed). The real log that already exists is the survey itself: "1947 UTC · 21 repositories cloned · live/cache/partial instruments"; if a log sheet is wanted before the real crawl exists, that is the honest one.

## 4. The strongest data-graphic version of this page

**Lead with one chart: the survey lines.** Twenty-one rows, one per repository, sorted by commit-days; x is 13 months from Sep 2025 to today; one dot per commit-day, dot area ∝ commits that day (or three size classes: 1–9, 10–49, 50+); repo name at left with `commit_days · months · commits` upright at full size; author vs all-hands as a short two-tone bar at the row end. Sweep days drawn as a vertical pecked line through every affected row, labelled "sweep · 18 repos · 7 Oct 2026". The hatched margin to the right of today is the unsurveyed, and now means something. The rose becomes a 24-bin radial histogram of commit-days by hour (hours are cyclic, so radial is justified here). The chart furniture (neatline, title block, lights, boat, night edition) all survives; hydrographic fair sheets are literally parallel lines of soundings, so the metaphor gets truer, not weaker.

Five seconds: two long, dense rows at the top (Scrapy, rustmapper), a cluster of short rows in Nov 2025 and Jan 2026, a vertical column of dots on 7 Oct. Name and thesis. One minute: every date, every count, who did the committing, the hour of day. Nothing to decode, nothing invented.

**Then, in order:**

1. Hero = survey lines + rose + title block (replaces hero islands and Sheet 2's curve, which is just the column sum of the strip).
2. Register as a real table, not a grid of cells: repo · commit-days · months · span · commits (author / all hands) · language · release · stars. Sorted by commit-days. Twenty-one rows by seven columns is a table's job and no graphic does it better.
3. Sheet 3 as a mechanism diagram: sources A/B/C → rustmapper (frontier, governor, WAL) → Scrapy stages → Delta Lake / Postgres / Redis → Prometheus / Grafana. The only numbers are the three SHA-cited claims. The prose bullets live once, under it.
4. Ship's log only when the run is real.
5. Instruments: five language-share bars (basis stated: bytes) with first-use date as a secondary column; or fold into the table and cut the sheet.
6. Footer at half height.

Six sheets become three (hero, register, mechanism), four if the log is earned.

## 5. Ranked changes

| # | change | why | effort |
|---|---|---|---|
| 1 | **Make commit-days the primary measure**, with span and months at full size; commits become the secondary figure. | Sweep-proof and burst-proof; flagships float to the top on the data alone; every figure stays measured. | M |
| 2 | **Replace the hero island field with the survey-lines strip plot** (rows = repos, x = time, dot = commit-day, area = commits that day; sweeps marked; margin right of today = unsurveyed). | One chart that gives the field in five seconds and the evidence in a minute, from `repos[].days` which is already in the file. | L |
| 3 | **Delete every unmeasured numeral from artwork** (Sheet 3 URL field, Sheet 4 figures). Retire the sloping convention or invert it into a check that forbids sloping figures. | A disclaimer typeface is not an encoding; fiction printed in figures is read as figures. | S |
| 4 | **Turn Sheet 3 into a mechanism diagram** carrying only the three SHA-cited claims. | The honest content of that sheet is structure, not quantity; the diagram also absorbs the duplicated prose. | M |
| 5 | **Cut the ship's log** until a real fixture crawl runs in CI and signs it. | Computed evidence on the most evidence-looking sheet. | S cut / L real |
| 6 | **Show author vs all-hands per repository** (two-tone bar or paired figure). | DESIGN.md promises two instruments wherever one is; per repo the bot share runs 0–56 % and is invisible. | S |
| 7 | **Sheet 2: no spline.** Bars or dots per week, one figure row aligned to bins, sweep day labelled as a sweep, not high water. Drop the sheet entirely once the strip plot exists. | Smoothing invents slopes; staggered figures detach from their bins. | S |
| 8 | **Rose → 24-bin radial histogram of commit-days by hour.** | Twenty-four measured values instead of one hand; cyclic data is the one case where radial is right. | S |
| 9 | **Register → a proper table** with commit-days, months, span, author/all-hands, language, release, stars; fix the survey so `language` is not null for 17 of 21 repos. | Twenty-one rows by seven columns is a lookup task; the cell grid and dead sparklines do it badly. | M |
| 10 | **One glyph, one meaning.** Subscript means one thing or nothing; print months active at full size next to commit-days; language share drawn as five bars with the basis stated. | Three meanings for one sign is the cheapest thing on the page to get wrong and the easiest to fix. | S |
