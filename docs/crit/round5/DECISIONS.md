# Round 5 decisions: a chart that is helpful knowledge about Ben, themed without saying so

Seven memos (navigator, hiring, infodesign, tone, skeptic, student, data) written from the owner's three messages of
9 Oct 2026, without seeing each other. Where they agree, that is the decision. Where they differ, the choice and the
reason are given. The owner's test, in his words: a theme without telling me it's a theme; the map is helpful, the
log is not; it should be telling you about me with a layer of shipping; helpful knowledge, in a cool format.

## What all seven said

1. **The v10 image says nothing about him.** The role line is in 9 px caps inside a picture whose own headline is a
   slogan; the islands encode one doubling of radius; the top-right corner stacks eight label families; the bottom
   left gives 57 % of the repositories zero information. Kill the composition, not just the labels.
2. **Every mark that names the theme goes**: the boat and anchor, the two buoys with invented light characters
   (`Fl R 4s` is a string constant at hero.py:960), the course line, the compass rose and VAR 14h, the rock fringe,
   LIMIT OF SURVEY and UNSURVEYED, CHART NO. / IALA REGION B / SMALL CORRECTIONS, SOUNDINGS IN COMMIT-DAYS,
   the island suffixes and chart names (Profile Shoal, Data Science Bank, Game Engine I.), the pencil note.
3. **Real repository names.** "Scrapy Harbor" was coined in the v8 chart commit; the project is `Scrapy`. Print `Scrapy`.
4. **The high-water figure is housekeeping.** 7 Oct 2026: 358 commits across 18 repositories in one day, most with
   agent co-author trailers; 9–10 Nov 2025 and 1 Oct 2026 are sweeps too. Drawn as the deepest water, the chart lied
   with its own number. Sweep days are excluded from every shape and figure; the exclusion is stated once in fine print.
5. **Three commit totals is no total.** 1,665 / 1,966 / 1,828 come from three definitions. None is printed.
6. **Time is the honest geography.** Five of seven proposed a sheet whose axis is Sep 2025 to Oct 2026 with one row
   per repository; a sixth (navigator) draws the same thing as a coastline. A chart convention is kept only when it
   means the same kind of thing as the fact: a datum and date, a periodic light for a periodic thing, a hazard mark
   for a known gotcha, a sloping figure for a figure the sources disagree on.
7. **Text written straight.** No themed headings, no bits in the technical bullets, no "survey vessel". The theme
   lives in the drawing. A stranger should think "why is his readme a chart? odd" and never be told.

## D1. The image: the coast of the year

One sheet, chart-styled, on v10's paper, type and border (the border reads as a chart in a second and says nothing).
Geography is time. Nothing on it is placed by hand; nothing on it is a constant.

**Axis.** Sep 2025 to the survey date, drawn as a chart's latitude scale along the foot: month ticks, S O N D J F M
A M J J A S O, years at Sep 2025 and Jan 2026. The sheet ends at the survey date. No hatching, no word beyond it.

**Rows.** One per repository with seven or more commit-days (sweep days excluded: today nine, with six-and-under
repositories merged), ordered by commit-days, the real name at the left in the sheet's small caps, the language tag
in lighter ink where known. Each row is a bank: a land shape whose vertical thickness by month is that month's
commit-days (sweeps out), with the coastline drawn as chartlib draws coast, two derived tints (the 5-day and 10-day
contours of the monthly figure), no figure printed inside. Empty months are water. A tenth row, "12 more", carries
their days merged in the lightest ink, no name. A repository with no non-sweep day is not drawn as land anywhere.

**Marks, all derived.** `Scrapy` carries the one light, `Fl 15s`, because Prometheus scrapes every 15 s
(claims.scrape_interval, measured, sha-cited); it is the only thing that moves, a beat every 15 s, still under
reduced motion. `Rust-sitemap` is lettered `rustmapper` (its package name, which is how the repository is known) and
carries one mark at 8 Nov 2025: `0.1.3 · PyPI`. No other symbols.

**Title block**, top-left, four lines: the name at display size; the thesis line (his); the role line
`CRAWL AND DATA INFRASTRUCTURE · PYTHON AND RUST`; one fine-print line of datum and date:
`21 REPOSITORIES · AUTHOR'S COMMITS ON MAIN · SWEEP DAYS EXCLUDED · 7 OCT 2026 · EASTERN TIME` (every item measured;
"Eastern time" because every commit carries -0400/-0500). `DATUM: MAIN` is the one joke on the sheet and it is true.
Nothing else is lettered. No imprint line on the phone; on the desk the foot carries only the GitHub URL and the date.

**Phone first.** 720 wide portrait: title block stacked, then the rows at full width, the axis compressed to 13
months (about 22 px a month at 390 px on screen); nothing under 26 px sheet type (13 px on screen); rows 34–40 px
apart; nothing overlaps because nothing is placed by data except along one axis. Desk 1280 × ~620: title block left
third, rows right two thirds. Same drawing, two layouts.

**Why not the others.** The track-with-dots (student) and the dot rows (infodesign, hiring) are honest and legible
but read as a Gantt chart in a costume; the banks keep the drawing a chart. The spatial harbour (skeptic) keeps the
hand slots that collided on live data. The diamond panels (data) are helpful knowledge and go on the page as text
(D4), where the phone can read them.

## D2. The data: measured, defined, sweeps out

- `build_stats.py` adds per repository: `months` (commit-days per month, sweep days excluded), `first_ns`/`last_ns`
  (first and last non-sweep day), `coauthored` (commits carrying a Co-authored-by trailer, count and share), `tests`
  (test files by the data memo's patterns), `workflows` (files under .github/workflows), `manifest` (top dependency
  names, depth ≤ 2, from Cargo.toml / pyproject / package.json / go.mod / Package.swift), `lines` by language from
  the clone with vendored and generated directories excluded. All from the clones it already makes; one API call per
  flagship for the last workflow conclusion where the token allows, else absent.
- The calendar comparison (`data.calendar`) is removed or re-scoped: GitHub's contribution calendar counts private and
  organisation activity and is not comparable to clones of 21 public repositories.
- `commits`, `all_hands`, `calendar_total` stay in stats.json for the audit's record and are printed nowhere.
- The audit (docs/data/AUDIT.md) is the definition of record for every key; the page's data line is written from it.

## D3. The page text

The v11/page rewrite stands (every themed heading and bit cut; foot line without totals) with these on top:
- `Scrapy Harbor` becomes `Scrapy` everywhere on the page and in chart.toml copy; rustmapper stays rustmapper.
- The rules list is headed **Working rules**; the four other repositories under **Also**; the fold reads
  `15 more repositories: …`; the sign-off `Found a mistake? Open an issue.`
- The worker-pool figure is not printed until the repository agrees with itself (code 256–1,024, README 32–512,
  PyPI 256): the bullet says the governor grows and shrinks the pool on redb commit latency, no number. Ask of the
  owner in BEN-TODO: fix the rustmapper README; then the figure returns, with the README's throughput beside it.
- "provisional" is cut; `0.1.3 · PyPI · 8 Nov 2025` is how the edition is stated.
- The install block's toolchain sentence becomes the first bullet under it (the known gotcha, stated plainly).

## D4. Helpful knowledge under each project

Under rustmapper and Scrapy, one generated line each from D2's keys, plain words, nothing vanity:
`Built on tokio, redb, rkyv, reqwest · 3 test files · 2 workflows, last run passed 7 Oct 2026 · 16k lines of Rust ·
last worked 8 Aug 2026`. If a value is absent it is omitted, never estimated. This is the data memo's tidal diamond
as text, the hiring memo's badge row without badges.

## D5. The provenance line

One `<sub>` line at the foot, from stats only:
`Measured 7 Oct 2026 from clones of 21 public repositories, author's commits on main, sweep days (9–10 Nov 2025,
1 and 7 Oct 2026) excluded · N commits carry agent co-author trailers · regenerated weekly.`
The co-author fact is printed because two memos (hiring, skeptic) say hiding it costs him more than stating it; the
owner can strike it. No instrument roll-call.

## D6. Tone, the line

Allowed: a nautical word that is the plain word for the thing (log, chart, datum, edition). Banned: a nautical word
that renames something that has a name. One-off words that stay: `DATUM: MAIN`; `Fl 15s`; `Eastern time`. Cut from
the memos' lists: "Not to be used for navigation", "Laid up", "Wk" on game_engine (a joke at a repository's expense),
the pencil note (needs explaining), "small corrections 5–173" (fabricated provenance).

## D7. Method

- The build is gated on the cached stats and on a live-like stats file; nothing data-placed can collide, by
  construction (one axis).
- Review before the PR by the same seven lenses, reading the built sheet at 390 and 870 px and the page; their
  verdicts are committed under docs/crit/round5/review-*.md and the sharpest lines go to the owner unedited.
- Asks of the owner (docs/BEN-TODO.md): fix the rustmapper README's worker figure; fill the position and contact
  slots; strike the co-author line if he wants; say whether `rustmapper` or `Rust-sitemap` is the name to print.
