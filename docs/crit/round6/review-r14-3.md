# Review round 14, reviewer 3: information design and cartography

10 Oct 2026. My lens is Tufte, Bertin and the Admiralty drawing offices. I looked at every PNG in
`scratchpad/r6/build/round-13/`: the sheet on desk at 870 (day, night), mid at 746 (day, night) and phone at 390 and
308 (day, night), and the page at 1,280 (two screens), 1,180, 900, 390 (six screens) and 360. I read `README.md`,
`SPEC.md`, `LOG.md` through round 13, and the earlier reviews, including round 14's reviews 1 and 2. I don't repeat
anything already fixed. Where I agree with a finding another round-14 reviewer has already specified, I say so in one
line and don't specify it again.

This round I also built the hero myself, in a copy of the tree (`scratchpad/r14-3/tree`, nothing changed in
`wt-v12`), to test the one change I'm asking for. Renders: `scratchpad/r14-3/current-desk-at-846.png`,
`trial2-day-at-846.png`, `trial2-night-at-846.png`, `trial2-day-at-766.png`.

Score: **8 / 10**. Meets the goal: **no**.

- **The image's content is right.** I'd keep every mark and every word.
- **On desk it is drawn too small.** Every desktop window from 1,200 px up gets the desk sheet. In those windows the
  route's words are 12.6 px, against the page's 16 px body text right under them. One pixel narrower, at 1,199, the
  same words are 17.7 px. Most desktop screens in use are 1,280 px wide or wider (StatCounter, below), so most desk
  visitors get the smallest version. Must-fix 1.
- **The page has the two false Scrapy sentences** that reviewers 1 and 2 found. I checked them in the code and agree.
  Must-fix 2.

## The first question: does it meet the owner's goal?

- **Every map has a deep purpose.** Yes. There is one map. It is a strip map of one route: the install, the rows that
  repeat for every page, the catch inside the loop, the one key you press, the file you get, and the project of his
  that reads it. Order down the page is the strongest channel the sheet has, and it carries the one fact text can't
  show: which steps repeat, and that only you end the repeat. No shape has a size, so nobody has to ask what a size
  means. That answers the owner's islands question for good.
- **Every element has a purpose.** On the image, yes (audit below). On the page, every block has a job, but two
  sentences say things the code doesn't do (must-fix 2).
- **It teaches something true and useful about his projects.** The image does: every row is a property of
  rustmapper 0.1.3 that I found in the sdist or in the run check (table below). The page fails on Scrapy's stage 2.
- **Nothing chases a reason, and nothing announces the theme.** True. You only see the chart conventions (the magenta
  track, the dotted danger line, the line carried on to the next project) if you already know charts. No word names
  them.
- **Reads on a phone.** Yes. At 390 the route is 13.3 px and the whole image fits one screen. The phone is in better
  shape than the desk. People hold a phone closer than a laptop, so 13.3 px on a phone appears larger to the eye than
  12.6 px on a laptop.

The owner asked for a picture that is "accepting of all different formats". His complaint "It's too dense in certain
areas of the image" fits the desk sheet best. The left 28 % of that sheet is empty below the role line, while the
route is packed into the right 60 % at the smallest type size on the page.

## Figures checked

| Printed | Where I checked | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `stats.json` `edition` 0.1.3, 2025-11-08 | yes |
| `rust_sitemap crawl`; by default sitemaps, certificate logs, Common Crawl | `edition.scripts` `["rust_sitemap"]`; sdist `cli.rs:58` `default_value = "all"` | yes |
| up to 20 pages at a time from each host | sdist `state.rs:285` `max_inflight: 20` | yes |
| saved as it goes; export works after a kill | `runcheck.rustmapper` `export_after_kill` ok | yes |
| `Received work item`, 60 s | sdist `bfs_crawler.rs:433`; route H1 `quiet` 60 | yes |
| second Ctrl-C before `Saved to` | sdist `main.rs:519` "Force quit requested", `:539` "Saved to:" | yes |
| fields `url, depth, status_code, title` | runcheck `crawl_ctrl_c`: keys present | yes |
| sorted 21 ways | `handoffs` state `runs`, `figures` | yes |
| 176 tests · CI 7 Oct 2026: tests, rustfmt · 16k lines | `repos[Rust-sitemap]` 176; success 2026-10-07; gates `[tests, rustfmt]`; Rust 16,390 | yes |
| 256 at a time | sdist `cli.rs:191` `assert_eq!(workers, 256)` | yes |
| ignores `Crawl-delay`; robots.txt only over https | sdist `frontier.rs:787` `crawl_delay_secs: None`; `robots.rs:19` `format!("https://{}/robots.txt")` | yes |
| 3 min, cold cache, 4-core | runcheck `install` median 171.4 s, 4 CPUs | yes |
| 1,920 tests · 8 Oct 2026: tests, ruff, mypy, bandit · 69k | `repos[Scrapy]` 1,920; success 2026-10-08; four gates; Python 69,036 | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | full clones `scratchpad/r5/rv/*.git` at `32c2651` and `96e7a1a`: Claude 45 of 146; jules 49 + Claude 22 of 499; his commits with an agent `Co-authored-by` trailer: 1 and 30 | yes |
| Rule 3: 6 days, then 5 | first commit 2025-09-25; `prometheus_client` first in `d571e6e` 2025-10-01; "gafka dashboard" `e8cbe15` 2025-10-06 | yes |
| 15 more | `repo_count` 22 = profile + 2 flagships + 4 Also + 15 | yes |
| "It obeys `robots.txt` and its `Crawl-delay` …" | `scout_spider.py:162-179`: the stage 2 queue row is yielded before the `scrapy.Request` (and alone for non-HTML links); `stage2_worker.py:403`, `:668`: aiohttp, no headers; no robots code anywhere in stage 2 | **stage 1 only** |
| "`--reset-delta` loads 143,208 bundled URLs" | `start.py:364-376` runs `cli.py reset --force` with `-T`; `destructive_guard.guard_flags` makes `--force` mean `--confirm --yes`; `authorize` refuses `--yes` without `ALLOW_LAKE_RESET=1`; `docker-compose.yml` never sets it | **no** |

## What the desk visitor sees, measured

GitHub's README column, as `scripts/checks/column.py` measured it on 10 Oct, is 846 px from a 1,280 px window up,
and the README serves the 1,280-unit desk sheet from 1,200 px. The route is set at 19 units.

| Window (px) | Edition | Column | Route text | Image height |
|---|---|---|---|---|
| 390 | phone 600 | 308 | 13.3 px | 575 |
| 1,180 | mid 820 | 746 | 17.3 px | 643 |
| 1,199 | mid 820 | 765 | **17.7 px** | 660 |
| 1,200 | desk 1,280 | 766 | **11.4 px** | 342 |
| 1,280 to 1,920+ | desk 1,280 | 846 | **12.6 px** | 377 |
| page body text, every width | | | 16 px | |

- **Most desk visitors.** StatCounter's desktop resolutions for September 2026 are 1,920 x 1,080 (28.07 %),
  1,536 x 864 (10 %), 1,366 x 768 (7.95 %), 1,280 x 720 (4.71 %), 2,560 x 1,440 (3.95 %) and 1,280 x 1,200 (3.64 %)
  [S3]. Every one of them is 1,280 px wide or wider, so every one gets 12.6 px. Together that is 58 % of desktop
  screens.
- **What 12.6 px means to the eye.** IBM Plex Sans Condensed and Plex Mono both have an x-height of 516/1000
  (`scripts/fonts/*.ttf`, OS/2 `sxHeight`), so 12.6 px type has an x-height of 6.5 px. A CSS pixel is defined as
  about 0.0213° of visual angle at arm's length, 71 cm [S2], so 6.5 px is 0.14°. OSHA puts a monitor 50 to 100 cm
  from the eyes [S4]. Even at its nearest 50 cm, the route's x-height is only 0.196°. Legge and Bigelow's consensus
  critical print size, below which reading slows, is 0.2° of x-height. Newspapers sit at 0.20° to 0.26° [S1]. So on a
  laptop the route is at or under the size where reading slows, and the body text right under it is not.
- **The other rules of thumb agree.** Butterick puts web body text at 15 to 25 px [S6]. Lighthouse calls text under
  12 px too small [S5]. The desk sheet is under 12 px from 1,200 to 1,222 px, and the mid sheet is under 12 px from
  852 to 862.
- **Why the build didn't catch it.** HERO-COLUMN-PX's floor is 11 px (`column.py` `MIN_PX`). That floor is right for
  a 360 px phone and too low for a laptop. The review renders also show the desk sheet at 870 px, so they make it look
  3 % larger than the 846 px GitHub actually gives it.
- **Why this is not round 10's note again.** Round 10's reviewer 2 noted "about 12.9 px in the 870 column" and said
  "not now", because the only fix then was a larger desk font that would push the sheet past its 620 gate. Since round
  12 the pipeline has had the stacked mid layout, and the column table is measured. Together they show both the
  1,199/1,200 jump and a fix that needs no new layout.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose work this is | keep | the image travels without GitHub's header (link previews, screenshots) |
| Role line, two caps lines | crawl and data infrastructure, in Python and Rust | keep | the route below proves the first half |
| Empty left column, desk only | nothing | **change** | 28 % of the sheet's width holds nothing below y 220, while the route is set at the page's smallest size. Must-fix 1 stacks the desk like the mid and phone editions |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which tool, and what you get | keep | a sailing-directions entry opens with what the place is |
| Start bar + `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old that release is | keep | the date makes every 0.1.3 caution honest |
| Magenta track | one way through, top to bottom | keep | the one colour kept for the line you follow |
| Stop rings | each is a step, in order | keep | the C1 ring is a step you take, the others are steps the tool takes. The words say which, so one symbol is enough |
| S1: `rust_sitemap crawl` starts from your URL; by default also sitemaps, certificate logs, Common Crawl | the real command, and who is asked about your domain by default | keep | |
| F1: up to 20 pages at a time per host; links to the site, its subdomains and parent | the load on one site, and how far it reaches | keep | |
| W1: saved as it goes; export works after a kill | a kill doesn't throw away the sitemap | keep | "export" is named in the code block right under the image |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one fact only a drawing gives |
| H1, dotted danger line: never exits; done when `Received work item` stops for 60 s | the catch, and the check that tells you you're done | keep | a danger line with the number you check it by |
| Gap in the track under the loop | the loop has no exit but you | keep | it costs nothing and is never wrong |
| C1: Ctrl-C once; a second press before `Saved to` loses the file | the one move, and the mistake to avoid | keep | 89 characters on one line: inside Butterick's 45 to 90 [S7], just over WCAG's 80 [S9]. Leave it |
| End bar + `data/sitemap.jsonl` + fields | what you get, in the struct's own names | keep | |
| Thin line on + arrowhead + "sorted 21 ways by ideal-url-organizer" | his projects feed each other, and the join is tested | keep | |
| Night editions | the same, in dark mode | keep | the Light cuts hold at 16 px in the trial too |
| Mid editions (852 to 1,199) | the same, stacked | keep | 11.2 to 12.9 px from 852 to about 950, but few devices have windows that width (note 1) |
| Phone editions (390 and 308) | the same, on one screen | keep | |
| Alt text | install, loop, stop, file | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image link to the repository | where the project lives | keep | |
| Link line | where to go | keep | |
| "Ben Russell builds …", Languages, Stack | what he builds, in what, on what | keep | the Stack line repeats names from both facts lines, but it is the keyword scan screeners do. Keep it |
| Pick sentence, first two sentences | which tool for which job | keep | |
| Pick sentence, politeness clause | (claims) Scrapy is polite | **cut** | must-fix 2 |
| rustmapper facts line | which commit, tests, CI gates, size | keep | reviewer 2's must-fix 2 (agent counts next to the counts) is a fair placement point, and I don't oppose it |
| Wheel note | will pip just work | keep | |
| "Before you run 0.1.3:" (four open items) | what it does to someone else's server, and the lever for each | keep | warnings before the procedure, each lever starting its own line |
| Fold "What 0.1.3's files miss or get wrong" | the file caveats, one tap away | keep | |
| rustmapper code block | install, run, when to stop, recover | keep | |
| Scrapy sentence, facts line, three bullets | the second system, measured | keep | |
| Scrapy run sentence up to "standalone)." | what `start.py` starts and needs | keep | |
| `--reset-delta` sentence | (claims) the flag loads UConn's URLs | **cut** | must-fix 2 |
| User-agent sentence | who the crawl says it is | **change** | must-fix 2: it is true of the scout only |
| Scrapy code block | how to point it at your site and name your bot | keep | |
| Grafana and `data/delta/` line | where to look once it runs | keep | |
| Also, four tools | the file's reader, the Go sibling, two more by what they do | keep | |
| 15 more (fold) | the rest | keep | |
| Working rules 1 to 3 | how he works, each with dated evidence | keep | |
| Found a mistake? | the page can be corrected | keep | |
| Data line | what was run, on what, and who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **From a 1,200 px window up, serve a stacked 1,000-unit sheet (the mid layout) instead of the side-by-side
   1,280-unit one.** On every desktop the route's words are then the same size as the page's text.
   (`scripts/sheets/route.py` `SIZES` and `L`; the README `<picture>` sources in `render_readme.py`; `column.py`;
   SPEC §2.3; the desk gates in the tests. About 40 lines of code and 6 tests.)
   - **What.** Add a `desk` geometry that is `L["mid"]` exactly: `title_x` 40, name 68, `text_x` 80, `right` 780, the
     same pitch and gaps, on a 1,000-unit-wide sheet (`SIZES["desk"] = (1000, 900)`, height from the content). The
     extra 220 units stay as paper on the right. The measure stays the mid's, so the lines break exactly as they do
     at 1,180 today, and no row runs past 89 characters. Retire the side-by-side geometry (`title_w` 354, `track_x`
     456, `file_right`). The `<picture>` keeps its four sources. `hero-day.svg` and `hero-night.svg` become the
     1,000-unit stacked sheets, so the `<img>` fallback and the GitHub app also get the larger type.
   - **Built and measured** (`scratchpad/r14-3/tree`, `SIZES["mid"]` set to `(1000, 900)`, nothing else changed;
     renders `trial2-*.png`). The sheet comes out 1,000 x 707, with 0 build problems, in day and night.

     | Window | Column | Route text | Height | x-height at 71 cm |
     |---|---|---|---|---|
     | 1,200 | 766 | 14.6 px (was 11.4) | 541 px (was 342) | 0.16° |
     | 1,280 and up | 846 | 16.1 px (was 12.6) | 598 px (was 377) | 0.18°, the same as the body text |

     The jump at 1,199/1,200 shrinks from 17.7 → 11.4 px to 17.7 → 14.6 px. The name stays the size it is now (68
     units, 57.5 px at 846, against 58 px today).
   - **The cost, stated.** The image is 221 px taller at 846. With GitHub's header and padding (about 120 px), it
     still fits a 1,920 x 1,080 window and a 1,536 x 864 one with the link line showing. On a 1,366 x 768 laptop (a
     window about 650 px tall) the last row, the hand-off line, falls below the first screen, and at 1,280 x 720 the
     Ctrl-C row and the file do too. That is the same trade round 12 accepted for the mid sheet at 1,180 (643 px tall),
     and it stays well under TALL_PX's 900. If the owner wants the whole route on a 768 px laptop screen, build the
     same layout 1,100 units wide instead: 14.6 px text, 544 px tall. Don't go wider than 1,100. Past that the route is
     back under 14 px, and keeping the height was the only reason for the old desk.
   - **Why a stacked layout and not a bigger font in the old one.** In the side-by-side layout the route's longest
     row already ends at x 1,152 of 1,224 at 19 units. Any larger type needs the name column to give way, which is
     what stacking does. The stacked order (name, role, then the route at one left edge) is also what the phone and
     mid editions already use. Every visitor, on any device, then reads the same picture in the same order. The
     side-by-side sheet is the one edition that doesn't. Reading falls off down the left edge of a page [S8], and a
     stacked route puts every row's first words on one left edge under the name.
   - **Gates and tests.**
     - `column.py`: a second floor, DESK-PX, from `breakpoint_px + 1` to 1,920: route text at least 14.5 px, and at
       least 16 px where the column is 846. Run against today's README it fails, and on the stacked sheet it passes.
     - The desk height gate goes from 620 to 760 units.
     - Tests that pin 1,280 x 571 change to the new size. Fixtures for the side-by-side `file_right` rule are dropped.
     - T-PURPOSE: the desk sheet has the same element IDs as the mid sheet.
     - The review render set draws the desk sheet at 846, the measured column, not 870.
   - **Why it must change.** The image is the one thing every visitor looks at, and the desk is where screeners and
     hiring engineers read it. Today it is printed below the critical print size for laptop distances [S1, S2, S4],
     under the page's own body text and under Butterick's web minimum [S6], for every common desktop screen [S3]. One
     pixel narrower, the build already gives the same words at 17.7 px. The owner's test is "how does it help the user
     see my project?". At 12.6 px in a condensed face, most desk visitors see it as smaller and harder to read than the
     text below it.

2. **Fix the two Scrapy sentences that the code doesn't support. I agree with reviewer 1's must-fixes 1 and 2 and
   reviewer 2's must-fix 1, and I checked them myself.** (`chart.toml [copy] pick_polite` and its rows; the Scrapy
   run sentence; the `[[figures]]` rows for "143,208" and "134,807". Reviewer 1 gives the sizes and the anchors.)
   - **What I checked.** `scout_spider.py:162` yields `_queue_for_stage2` before the `scrapy.Request` at `:167`, and
     `:179` yields it alone for non-HTML links. `stage2_worker.py:403` and `:668` fetch with aiohttp and no headers.
     No file under `src/stage2` mentions robots. `start.py:364-376` passes `--force` with `-T`, and
     `destructive_guard.authorize` refuses `--yes` without `ALLOW_LAKE_RESET=1`, which `docker-compose.yml` never
     sets.
   - **What the page should do.** Cut the politeness clause (gated, as reviewer 1 specifies, so it comes back by
     itself the day stage 2 checks robots.txt and sends its own name). Cut the `--reset-delta` sentence. Say in the run
     sentence that the stage 2 worker fetches every queued link, 4 at a time per host, as `Python/3.11 aiohttp/3.13.1`.
   - **My one addition, from the reader's side.** Write the run sentence in the order a reader acts: what it starts,
     what it needs, what it does to a site, then the command. Don't open with the bot name. Reviewer 1's wording
     already follows that order. Keep it that way through the edit.

That's all. The rest of the page doesn't need to change.

## Notes (true, not ranked)

1. **The mid sheet's narrow end.** From 852 to about 950 px the mid sheet is 11.2 to 12.9 px. No phone or tablet
   uses those widths: iPads in portrait (768 to 834) get the phone sheet at 17 px and more, and in landscape (1,024 to
   1,194) the mid sheet at 13.7 to 17.6 px. Only a narrowed desktop window lands there. Leave it.
2. **The empty right margin of the stacked desk sheet** (220 units) is a ragged-right text block at a good measure,
   not dead paper. Don't fill it.
3. **The phone is fine as it is.** 13.3 px at 390 and 12.0 px at 360, on a screen held much closer than a laptop.
   Nothing to change.
4. **Owner, outside this repository:** reviewer 1's notes on Scrapy stage 2 (a robots check, one user agent, a
   per-host delay) and `start.py --reset-delta`, plus the carried 0.1.4 list. ROUTE-UNVERIFIED still fails on S2, so
   the image doesn't go to `main` until P1 is at HEAD, whatever this review says.

## Sources (new this round; none cited in earlier rounds)

The session's web-search budget was spent before this review started, so every source below was fetched directly by
its URL and read.

1. [S1] Gordon E. Legge and Charles A. Bigelow, "Does print size matter for reading? A review of findings from vision
   science and typography", *Journal of Vision* 11(5), 2011: "a consensus value for the critical print size for
   normally sighted readers is 0.2° x-height"; the fluent range runs "from approximately 0.2° to 2°"; newspapers have
   "a mean visual angle of 0.23° in a range from 0.20° to 0.26°". https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264/
2. [S2] W3C, *CSS Values and Units Level 4*, the reference pixel: "the visual angle of one pixel on a device with a
   device pixel density of 96dpi and a distance from the reader of an arm's length", nominally 28 in, "about 0.0213
   degrees". https://www.w3.org/TR/css-values-4/#reference-pixel
3. [S3] StatCounter, *Desktop Screen Resolution Stats Worldwide*, September 2026: 1,920 x 1,080 28.07 %, 1,536 x
   864 10 %, 1,366 x 768 7.95 %, 1,280 x 720 4.71 %, 2,560 x 1,440 3.95 %, 1,280 x 1,200 3.64 %.
   https://gs.statcounter.com/screen-resolution-stats/desktop/worldwide
4. [S4] OSHA, *eTools: Computer Workstations, Monitors*: "the preferred viewing distance is between 20 and 40 inches
   (50 and 100 cm)". https://www.osha.gov/etools/computer-workstations/components/monitors
5. [S5] Chrome for Developers, *Lighthouse: Document doesn't use legible font sizes*: text "smaller than 12 px" is
   flagged when it is 40 % or more of the page. https://developer.chrome.com/docs/lighthouse/seo/font-size
6. [S6] Matthew Butterick, *Practical Typography*, "Point size": on the web, body text of "15–25 pixels".
   https://practicaltypography.com/point-size.html
7. [S7] Matthew Butterick, *Practical Typography*, "Line length": "an average line length of 45–90 characters,
   including spaces". https://practicaltypography.com/line-length.html
8. [S8] Baymard Institute, "Readability: the optimal line length": 50 to 75 characters for body text; with long lines
   readers find it "hard to … find where each line starts". https://baymard.com/blog/line-length-readability
9. [S9] W3C, *Understanding SC 1.4.8: Visual Presentation*: "Width is no more than 80 characters or glyphs", because
   "long lines of text can become a significant barrier" for some readers.
   https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html

Code and data: `assets/stats.json` (`edition`, `repos[]`, `routes.rustmapper`, `runcheck.rustmapper`, `handoffs`,
`agent_authored`), sdist 0.1.3 (`state.rs:285`, `cli.rs:58`, `:191`, `bfs_crawler.rs:433`, `main.rs:519`, `:539`,
`robots.rs:19`, `frontier.rs:787`), full-history clones `scratchpad/r5/rv/Rust-sitemap.git` (146 commits) and
`Scrapy.git` (499), Scrapy clone at `96e7a1a` (`scout_spider.py`, `stage2_worker.py`, `start.py`,
`destructive_guard.py`, `docker-compose.yml`), `scripts/checks/column.py` (`column_px`, `MIN_PX`),
`scripts/fonts/*.ttf` (x-heights). Trial build: `scratchpad/r14-3/tree` (`SIZES["mid"] = (1000, 900)`), renders in
`scratchpad/r14-3/`.
