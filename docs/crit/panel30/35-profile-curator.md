# Crit 35 — the profile-README curator

I maintain an awesome-list of GitHub profiles and have triaged thousands: stats cards, snakes, typing SVGs, WakaTime, Spotify, 3D contribution graphs, lowlighter/metrics, Figma headers with outlined type, Actions-generated art. I read README.md, README.draft.md, STANDARDS, CHANGELIST, the specs, 23-oss-maintainer, the workflows and `scripts/`, and looked at page-day-full.png and hero-day-2x.png.

## What is good

- **The hero is the rare screenshot that explains itself.** Name, thesis, named features, a boat. One of perhaps five profiles I could identify from a 400px thumbnail, and nothing on it is a widget someone else drew.
- **Type as outlines via `svgkit.py` is the most copyable thing here.** The number-one failure of "designed" SVG READMEs is fonts: a 2 MB Figma export, or a `font-family` that falls back to Times. A subsetting pipeline that emits glyph defs and keeps a sheet of numerals under 300 KB solves a complaint the community has had since 2020. Extract it; it will travel further than the profile.
- **Honest-by-convention.** Upright measured, italic illustrative, defined once. The category runs on numbers nobody can check (visitor counters, "1000+ hours coded"); a notation for uncertainty is a real contribution.
- **The data-driven archipelago (C2) is, to my knowledge, without precedent on a profile.** Prior art I know: simonw's self-updating README (2020), Platane/snk, readme-typing-svg, anuraghazra's cards, lowlighter/metrics (habits, isometric calendar), yoshi389111's 3D graph, GitHub Skyline and GitHub City, novatorem's Spotify card. Contour maps from scalar fields are common in plotter art. Nobody I have seen has put a repository portfolio on a bathymetric chart with correct chart grammar. I have not seen everything; I would still submit it under "Elaborate" and "Dynamic Realtime" as a first.

## What is bad, ranked

1. **Three sheets are known tricks in costume, and curators see through costume instantly.** Soundings (1,828 · 24 · 46 · 6 · Oct 2024, a language bar, an activity curve) is the stats card plus top-langs plus the activity graph, in serif. The log that "types itself" is readme-typing-svg, the most recognised cliché after badge rows. The legend was a skills table. The page gets filed as *stats card + typing SVG, nice palette*, the shelf it is trying to leave.
2. **"If you like it, borrow it" is unforkable and unlicensed.** Panel 23 found the missing LICENSE; the deeper problem is that nothing is borrowable mechanically: `LOGIN` is a constant in `build_stats.py`, "Ben Russell" is a literal set at 176px for ten characters, the edition line assumes a PyPI package. Profiles go viral through their *mechanism*, never their beauty: the snake, the typing SVG and the 3D graph spread because each was two lines of YAML. A one-of-a-kind chart with no fork path has a ceiling of one tweet.
3. **No shareable raster.** Link cards on X, Slack and Discord do not render SVG, and the repo has no custom social preview. The one screenshot that explains itself is never the screenshot anyone sees.
4. **"How it's built" is buried.** Viral profiles put "built with → repo" one line under the hero. Here the build line is inside the last section and the contribution invite is an HTML comment. Fix: the nav's last link becomes *Source* and points at `scripts/`.
5. **The profile is more interesting than the repos, and the chart points at them.** Click rustmapper from the gallery and you reach `Rust-sitemap`: no license, no release. Gallery visitors click through more than recruiters; that drop is the worst moment of the experience.
6. **Animation budget.** 55 `<animate>` in the survey, 24 in the log, 13 in the footer, all starting at load whether visible or not. Heavy SMIL profiles are the ones screenshotted with a fan-noise joke. SMIL also starts on image load, not on scroll, so one-shot openings below the fold play to nobody (16 flagged it; I can confirm it).

## What needs to be done

- **Delete sheet 2 as a sheet.** Keep the tide curve as a tidal-information strip in the hero's bottom margin (real charts carry tidal panels); put the five figures in Markdown where recruiters and screen readers can read them.
- **The log is a record, not a performance.** Render the session already written; only the last entry is being entered when the sheet loads, then the cursor holds. One line being entered is a watch being kept; a full page typing is the trick everyone owns.
- **Separate grammar from geography.** `chart.toml`: login, display name, thesis, named-feature overrides, palette, optional PyPI package. The engine (chartlib, svgkit, stats→features, hero, footer) is the template; the Approaches sheet, the log session and the copy are Ben's and stay un-templated. Because the archipelago is drawn from the forker's own repos, every fork is one-of-a-kind by construction, which resolves the template-vs-unique tension. Fit the name to the cartouche (measure the outlined run, scale to a 120px floor); fall back to "FIRST EDITION" without a package. Target: fork → enable Actions → six lines → run workflow, under ten minutes.
- **License before "borrow."** MIT for `scripts/`, CC BY 4.0 for sheets and copy, OFL fonts as vendored (OFL permits outlining; keep the license texts). Delete Inter and DejaVu. Replace the line with the path: "The engine is MIT; `chart.toml` makes it yours." Template repository only after this lands.
- **Render a PNG nightly and set it as the social preview.** resvg in `profile.yml`, `assets/hero-light.png` at 1.91:1, committed; upload once as the repo's Social preview. Test both editions at 600px wide: name, thesis and one island name must survive the card crop.
- **Put "one feature per repository · area by commits" on the sheet,** one cartouche line in chart register. Today the hero looks like a drawing; the screenshot must explain its own data.
- **Reduced motion inside the SVG.** `@media (prefers-reduced-motion: reduce)` in SVG CSS is honoured inside `<img>` in current browsers in my experience, like in-SVG `prefers-color-scheme`; add it, test on GitHub, cap the page at two sheets looping indefinitely.

## Improvements and ideas

- **The chart is on the chart.** The `BenjaminSRussell` repo already draws as a feature (r=42, fourth largest). Name it in the chart's italic, unmentioned in the copy, the way a chart marks its own position: the best available second-look layer, and it makes the generator a visible project rather than scaffolding.
- **Promote the generator to a named repository with a release.** "Chart" is ungoogleable. A named engine whose README opens with a *different* user's chart proves the fork path, gives awesome-lists a mechanism to list, and fixes problem 5.
- **Bold: a fleet.** Each fork carries a small "charted by" credit outside the neat line and, by opt-in in `chart.toml`, is listed in `FLEET.md` in the engine repo. The first stranger's chart is when the profile stops being a portfolio and becomes a tool; it is also the only honest growth metric this page can have.
- **Fix the destinations before submission.** No awesome-list submission until Rust-sitemap has a LICENSE and a release (23-F1). The gallery audience clicks; the click must survive.

## What the page says about its maker

Now: a designer-engineer who built one image nobody else could have built, surrounded it with the standard README stack in the same ink, and wrote "borrow it" on a repository nobody can legally or practically borrow. It should say: someone who invented a mechanism, named it, licensed it, made it forkable in ten minutes, and kept his own chart as its first and best edition. The community does not remember beautiful profiles; it remembers the people whose trick it is still using.

## Five most important lines

1. Three sheets are known tricks in costume (stats card, top-langs bar, typing SVG): fold the figures into Markdown and a hero tidal strip, and render the log as a record with only the last line being entered.
2. Separate grammar from geography: `chart.toml` plus a data-driven archipelago makes every fork unique by construction; remove the hardcoded login and name, fit the name to the cartouche, fall back when there is no PyPI package.
3. License before "borrow" (MIT scripts, CC BY 4.0 sheets, OFL fonts kept), delete Inter/DejaVu, replace "If you like it, borrow it" with the actual fork path; Template repository only after.
4. Build a hero PNG nightly and set it as the repo's social preview; test both editions at 600px wide, because no link card renders SVG and that screenshot is the whole marketing.
5. Name the generator, give it a release, let the chart mark itself as a feature, and submit to no awesome-list until Rust-sitemap has a LICENSE and a tag.
