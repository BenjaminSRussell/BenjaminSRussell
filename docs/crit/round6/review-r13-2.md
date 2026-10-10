# Review round 13, reviewer 2: the historian of charts and sailing directions

10 Oct 2026. My question for every mark and every block: is this convention used for the job it was invented for, or
is it there because charts have one? I looked at every PNG in `scratchpad/r6/build/round-12/`: the desk sheet at 870
(day and night), the mid sheet at 746 (day and night), the phone sheet at 390 and 308 (day and night), the desk page
(two screens), the README at 1,180 and 900, the phone page at 390 (seven screens) and at 360 (seven). I read
`README.md`, `SPEC.md`, `LOG.md` through round 12, `DESIGN.md`, and every earlier review, including the two earlier
historians (`review-r04-2.md`, `review-r08-3.md`). I don't repeat anything already fixed or declined. I checked the
figures against `assets/stats.json`, the 0.1.3 sdist (`scratchpad/r6/sdist013`) and the clones.

**Verdict: 9 / 10. Not yet. I would ship the image as it is. The page needs two small fixes first.**

## The first question: does it meet the owner's goal?

- **Every map has a deep purpose.** Yes. The picture is a strip map of one route, and a strip map is the right form
  for a crawler you run once from start to finish. Ogilby's 1675 road strips showed "a part of the road and the
  surrounding environment", with what you meet on the way: rivers, bridges, side roads [S6]. They were "the start of
  all strip maps" and were copied for two centuries [S7]. A strip map leaves out what isn't on the way, and so does
  this one. It has no grid, no coast, no sizes and no compass. It shows install, the loop each page goes round, the
  one danger, the one thing you do, the file you get and who reads it next. The owner asked "what is it showing?"
  This answers him in one look.
- **It teaches something true and useful about his projects.** Yes. Every row holds against the sdist and the run
  check (table below). A screener learns that he builds crawlers that are polite per host, seed beyond links, and
  write to disk before the database. A user learns how to get it, how to stop it and what they end up with.
- **Nothing chases a reason.** In the image, yes. Every mark does a job a navigator would recognise, and none is
  there for looks (audit below). On the page, one sentence one click away claims more checking than was done
  (must-fix 1).
- **Nothing announces the theme.** True. The magenta line, the dotted danger line, the edition date at the entrance
  and the continuation arrow are all real chart habits, and none is named. Someone who has never seen a chart reads
  them as "follow this", "watch out", "how old", "goes on to".
- **Reads on a phone.** Yes. At 390 and 308 the image fits one screen, day and night. The mid sheet fixed the iPad.
  At 1,180 the whole route is on the first screen. At 900 the mid sheet's smallest text is about 12 px, which is
  small but holds the floor.

## What each convention is for, and whether it's used for that

| Mark | Where it comes from | Its real job | Used for that here? |
|---|---|---|---|
| Vertical strip, read top to bottom | road strips (Ogilby) and the pilot book's coastal sequence | show only what you meet, in the order you meet it | **Yes.** The order is the tool's order. |
| Magenta line | the track to follow (NOAA, and later aviation) | the line you are meant to take | **Yes.** One line, one way through. Cleared by r04-2. |
| Start and end bars | transit diagrams | where the line begins and ends | **Yes.** `pip install` and `data/sitemap.jsonl`. |
| Rings | station marks | a place the line stops | **Yes.** Each ring is one step the tool takes. |
| Loop bracket with up arrow | flowcharts | which steps repeat | **Yes.** It's the one thing a list can't show. |
| Red dotted line round H1 | the danger line (IHO S-4) | draws the eye to a danger you would otherwise miss | **Yes.** r04-2 and r08-3 cleared it; it stays while 0.1.3 is current. |
| "0.1.3 · 8 NOV 2025" at the entrance | the edition date in a chart's margin | how old the thing you rely on is | **Yes.** It's where you decide to install. |
| Thin line, arrowhead, "sorted 21 ways by ideal-url-organizer" | the continuation note at a chart's edge | where the route goes on, on another sheet | **Yes.** The next sheet is the first project in "Also". |
| Data line under the page | the source note (source diagram) | how the chart was made, and how far to trust it | **Mostly.** The page's own note is honest. The method page it links to overclaims (must-fix 1). |
| "Before you run 0.1.3:" list | the pilot book's text beside the chart | what the chart can't show, keyed to where it bites | **Mostly.** It's the right content, but not in the order of the drawing it sits under (must-fix 2). |

What I checked and dropped:
- **A "checked on" date in the image.** Charts carry a "corrected to" date beside the edition date, because "the
  date of a published chart edition can be misleading" [S8]. Here the edition date is the release, which is the
  date a user needs, and the date it was checked (10 Oct 2026) is in the data line. Adding it to the image puts back
  the title-block clutter that round 6 cut. Leave it.
- **W1 has no consequence.** "logged to disk, then saved to redb, in batches" tells a screener how he builds, and
  its consequence (export-sitemap works after a kill) was moved to the code block on purpose (LOG rounds 7 to 9).
  It stays.
- **Three names for one tool** (rustmapper, Rust-sitemap, `rust_sitemap`). That's P4, the owner's.

## Figures checked

| Printed | Source | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version` 0.1.3; `edition.uploads[3]` 2025-11-08T19:52:41 | yes |
| `rust_sitemap crawl` | `edition.scripts` `["rust_sitemap"]` | yes |
| by default also from sitemaps, certificate logs and Common Crawl | sdist `cli.rs` `seeding_strategy` default `"all"` | yes |
| up to 20 pages at a time from each host | sdist `src/state.rs:285` `max_inflight: 20` | yes |
| `Received work item` | sdist `src/bfs_crawler.rs:433` | yes |
| 60 s | `routes.rustmapper` H1 `quiet` 60; probes `quiet_after_last_page`, `quiet_slow_page` ok | yes |
| `Saved to` line | sdist `src/main.rs:539`, `:704` `println!("Saved to: …")`; probe `second_ctrl_c` exit 1, no file | yes |
| fields `url, depth, status_code, title, …` | sdist `src/state.rs:98-114` `pub struct SitemapNode` | yes |
| sorted 21 ways | ideal-url-organizer `159968a`: `method_01` to `method_21` are the URL-record methods; `scripts/import_rust_sitemapper.py:4` "methods-1-21 pathway"; its 15 `URL_RECORD_FIELDS` are all in `SitemapNode`. Methods 22 to 25 need page content, so 21 is the right count for this file | yes |
| 176 test functions · CI passed 7 Oct 2026: tests, rustfmt · 16k lines of Rust · `32c2651` | `repos[Rust-sitemap]` 176, `ci` success 2026-10-07, gates, `lines.Rust` 16,390, `head.short` | yes |
| 3 min, cold cache, 4-core | runcheck `install`: median 171.4 s of 168.2 to 174.3, 4 CPUs, empty `CARGO_HOME` | yes |
| up to 256 at a time | sdist `src/cli.rs:32` `default_value = "256"` | yes |
| 50,000 URLs per file | sitemaps.org limit (X1 `audit`) | yes |
| 1,920 test functions (all but 41) · CI 8 Oct 2026 · MIT · 69k | `repos[Scrapy]` 1,920; `ci_selection.not_selected` 41 (16 outside, 25 deselected); `license` MIT; `lines.Python` 69,036 | yes |
| 143,208 bundled URLs, 134,807 on uconn.edu | `uconn_urls.csv` has no header row: 143,207 + 1 = 143,208 rows; hosts `uconn.edu` or `*.uconn.edu` 134,806 + 1 = 134,807 | yes |
| Rule 1: 5 URLs, 60 s, Oct 2026 | Scrapy `stage2_worker.py:218-219`; `099dd6c` 2026-10-08, his | yes |
| Rule 3: 6 days, then 5 | first commit `67446a4` 2025-09-25; `d571e6e` 2025-10-01 adds `prometheus_exporter.py`; `e8cbe15` 2025-10-06 "gafka dashboard" | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | `Rust-sitemap.git` 146 (97 + 4 his, 45 Claude); `Scrapy.git` 499 (jules 49 + Claude 22); `coauthored.agent` 1, 30 | yes |
| Languages line | `repos[].main_language`: Python 11, Swift 3, JavaScript 2, Rust 2, TypeScript 2, C 1, Go 1, Python and Rust led by `languages_lead` | yes |
| 15 more · 21 repositories | `repo_count` 22 less the profile; 2 + 4 + 15 | yes |
| DESIGN.md: "its probes check each caution the README prints" | `chart.toml` items: L1 `runs` workers_cap, L4 `fails` robots_read, X1, X2, X3 have probes; **L2, L5, L3 have none** | **no** (must-fix 1) |

## Must fix, ranked

1. **Make the method page say which cautions were run and which were only read in the code**
   (`scripts/tokens.py:216`, the hard-coded sentence in `DESIGN_HEAD`; `chart.toml`, a `short` label on each caution
   entry; DESIGN.md regenerated; one test. About 25 lines.)
   - **What's wrong.** The data line's "drawing" link opens DESIGN.md, the page's source note. It says the run
     check's "probes check each caution the README prints". Five of the eight do have a probe (L1 `workers_cap`, L4
     `robots_read`, X1 `sitemap_keeps_noindex`, X2 `non200_status` and `redirect_kept`, X3 `redirect_kept`). Three
     don't: L2 (crt.sh and Common Crawl), L5 (`www.` skips `blog.`) and L3 (no JavaScript). Those three are checked
     against the 0.1.3 source by anchors, which is honest and enough, but they were never run. The run check also
     crawls with `--seeding-strategy none`, so L2 can't be probed by it as it stands.
   - **Why it matters.** It is a false sentence about how the page was checked, on the page whose only job is to
     say that. A source note must say how good the data is, not only that it exists. The IHO's guide to chart
     accuracy faults the old source diagrams because "most simply said how old a survey was, rather than how good"
     [S2]. NOAA puts it the same way: "Mariners need to know if data is old", and a chart is a patchwork of surveys
     made by different methods [S5][S9]. Here the two methods are "run against a server" and "read in the code", and
     the page should say which caution rests on which.
   - **What to build.** Write the sentence from `chart.toml`, not by hand. Give each `item = true` entry a
     `short = "…"` (L1 "load", L4 "robots.txt", L2 "seeding", L5 "the www scope", L3 "JavaScript", X1 "sitemap.xml",
     X2 "status codes", X3 "redirects"). In `tokens.py`, count the drawn items with `runs` or `fails` and those without,
     and print: "its probes test 5 of the 8 cautions the README prints; the other 3 (seeding, the www scope,
     JavaScript) are checked against the 0.1.3 source only." With no unprobed item, it prints "its probes test every
     caution the README prints."
   - **Test.** In `tests/test_round13.py`, the DESIGN.md sentence's two counts equal the computed counts. Removing
     `runs` from X3 in a fixture changes the sentence to "4 of the 8 … (…, redirects)". DESIGN-FRESH catches the rest.
   - The visible README needs no change. Its data line claims only "its commands were run, with seeding off, against
     a local 3-page site", and that's true.

2. **Put the cautions in the order of the drawing they sit under** (`chart.toml`: move the X3 entry, lines 986 to
   1003, above X2, and X1, lines 923 to 956, below X3, so the order is L1, L4, L2, L5, L3, X3, X2, X1; add a `stage`
   key to each caution; one test. No change to height or wording.)
   - **What's wrong.** The image is in the order the tool works. The list under it isn't, at the end. Today it runs
     L1, L4, L2, L5, L3, **X1, X2, X3**. X3 (after a redirect it reads links from the old address) is about which
     links it follows, the same subject as L3 just above it, and it happens inside the loop. X2 is about what the
     file records. X1 is about `sitemap.xml`, which only exists after `export-sitemap`, the last command of the code
     block directly under the list. So the list ends where the drawing starts, and the caution about the export sits
     three items away from the export command.
   - **Why it matters.** Pilot books are written in the order you meet things: "as much as possible, the coastal
     description is in geographic sequence", with each feature keyed to the chart that shows it [S1]. NGA's Sailing
     Directions are "numbered sections along a coast" [S3]. Waghenaer's 1584 *Spieghel*, the first book to pair the
     two, put "a description of sailing instructions for the coastal strip in question" on the page facing the chart
     of that strip [S4]. The same holds for a how-to: "the fundamental structure of a how-to guide is a sequence",
     and the order should mean something [S10]. A reader who has just followed the drawing top to bottom should meet
     its cautions in the same order, and the last one should sit right above the command it's about.
   - **Why L1 and L4 stay first.** They are about how it treats any server all along the route. They're the general
     cautions, like a Coast Pilot's general chapters before the coastal sequence [S1], and L1 is the one that harms
     other people's servers. Then the route: start (L2 seeding, L5 the start URL's scope), links (L3, X3), the file
     (X2), the export (X1).
   - **Build.** Give each caution `stage = "server" | "start" | "links" | "file" | "export"`. The test in
     `tests/test_round13.py` asserts that the rendered `install:Rust-sitemap` items run in non-decreasing stage
     order, so a ninth caution can't land in the wrong place. README-CAUTIONS, STRINGS-TWICE and FLAG-WRAP are
     unaffected: the words don't change.

That's all. The image itself needs nothing.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose work this is | keep | the sheet's title; it travels without GitHub's header |
| Role, two caps lines | crawl and data infrastructure, in Python and Rust | keep | the route under it proves it |
| Empty paper under the role (desk) | nothing, on purpose | keep | a strip map leaves out what isn't on the way |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which tool and what you get | keep | a pilot entry opens by saying what the place is |
| Start bar | where you begin | keep | the entrance as a fixed point |
| `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | the edition date, where you decide to rely on it |
| Magenta track | one way through, top to bottom | keep | the track to follow, for its real job |
| Stop rings | each one is a step the tool takes | keep | station marks |
| S1 `rust_sitemap crawl` … sitemaps, certificate logs, Common Crawl | the command, and that it finds URLs beyond links, by default | keep | the first thing the tool does |
| F1 20 per host; links to your site, subdomains, parent domain | how hard it hits one host and how far it reaches | keep | |
| W1 logged to disk, then saved to redb, in batches | it writes before it commits | keep | the screener's line; its consequence lives in the code block, by decision |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Gap in the track under the loop | the loop doesn't end by itself | keep | cleared by r04-2; the words beside it say the same |
| H1, red dotted line | the 0.1.3 catch and how to know you're done | keep | a danger line used as one; it goes when 0.1.4 ships |
| C1 Ctrl-C once | your one step, and the press not to make | keep | |
| End bar + `data/sitemap.jsonl` + fields | the file, in the struct's own field names | keep | |
| Continuation arrow + "sorted 21 ways by ideal-url-organizer" | his projects feed each other, and where to go next | keep | a continuation note; 21 holds for this file (methods 1 to 21) |
| Whole image links to Rust-sitemap | one tap to the code | keep | |
| Night editions | the same | keep | redrawn, not inverted |
| Mid editions (852 to 1,199 px) | the same, in one screen on an iPad | keep | new in round 12; the route fits the first screen at 1,180 |
| Phone editions (390, 308) | the same, in one screen | keep | |
| Alt text | install, loop, stop, file | keep | 25 words |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| `<picture>` sources | the right sheet for the width | keep | phone, mid, desk, each day and night |
| Link line | where the code, the package and the second tool are | keep | |
| "Ben Russell builds …" | what he builds | keep | |
| Languages | what he writes in, from the data | keep | |
| Stack | what he builds on | keep | |
| Pick sentence | which tool for which job | keep | the most useful sentence for a chooser |
| rustmapper facts line | which commit, deps, tests, CI, size | keep | |
| Wheel note | whether pip just works on your machine | keep | |
| "Before you run 0.1.3:" + 8 items | what it does to servers, what it can't see, what the files hold | **change** | must-fix 2: the order |
| rustmapper code block | how to run, when to stop, how to recover | keep | the 360 overflow is r12-1's unranked note |
| Scrapy sentence + facts line | the second tool, measured | keep | |
| Scrapy bullets 1 to 3 | storage, what happens to a page, how it's watched and shipped | keep | |
| Scrapy run sentence | what `start.py` starts, needs and loads | keep | |
| Scrapy code block | how to start it on your site | keep | |
| Grafana + `data/delta/` + DATA_USAGE.md | where to look, and where the pages land | keep | Scrapy now has an arrival, like rustmapper |
| Also (four lines) | four more tools, each by what it does | keep | ideal-url-organizer first, the continuation's target |
| 15 more (fold) | the rest, by group | keep | |
| Working rules 1 to 3 | how he works, each with a dated commit | keep | |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn, how it was run, who wrote the code | keep | an honest source note |
| Licence line | the profile's terms | keep | |
| DESIGN.md, linked as "drawing" | how the picture is checked | **change** | must-fix 1 |

## Owner, outside this repository

Carried, not re-ranked: P1 and its test (S2 is still unverified at HEAD, so ROUTE-UNVERIFIED blocks `main`), 0.1.4
with `[project.scripts]` and a LICENSE, `resume` after a kill, redirects (`response.url()`), and opening the profile
once on an iPad held sideways. New and small: if a probe for L2 is wanted, it needs a run with seeding on and a
local stand-in for crt.sh and Common Crawl, which the run check doesn't have. That isn't needed for must-fix 1. The
fix is to say it isn't probed.

## Sources (new this round)

1. [S1] NOAA, *United States Coast Pilot 4*, chapter 1, "General Information": "as much as possible, the coastal
   description is in geographic sequence, north to south on the east coast …"; "Features are described as they
   appear on the largest scale chart, with that chart number prominently shown in blue"; the Coast Pilot is "a
   supplement to NOAA nautical charts. Much of the content cannot be shown graphically on the charts". The general
   chapters come first, then the coast in order (must-fix 2).
   https://nauticalcharts.noaa.gov/publications/coast-pilot/files/cp4/CPB4_C01_WEB.pdf
2. [S2] IHO, *S-67 Mariners' Guide to Accuracy of Electronic Navigational Charts* (v0.5): source diagrams "most
   simply said how old a survey was, rather than how good"; seafloor coverage, whether anything was missed, "is far
   more important than the accuracy of the survey" (must-fix 1).
   https://iho.int/uploads/user/Services%20and%20Standards/DQWG/Letters/S-67%20Mariners%20guide%20to%20accuracy%20of%20ENC%20v0.5.pdf
3. [S3] Bowditch, *The American Practical Navigator*, ch. 4 (Wikisource): "Each volume of the Sailing Directions
   (Enroute) contains numbered sections along a coast or through a strait" (must-fix 2).
   https://en.wikisource.org/wiki/The_American_Practical_Navigator/Chapter_4
4. [S4] Utrecht University Special Collections, "*Spieghel der Zeevaerdt* by Waghenaer": "On the first page we each
   time find a description of sailing instructions for the coastal strip in question, which is depicted on the second
   and third page"; the charts run "from the southern tip of the island of Texel to Spanish Cádiz". Text beside the
   strip it describes, in the same order (must-fix 2).
   https://www.uu.nl/en/special-collections/the-treasury/maps-and-atlases/spieghel-der-zeevaerdt-by-waghenaer
5. [S5] NOAA Office of Coast Survey, "How accurate are nautical charts?": "Most nautical charts are made up of survey
   data collected by various sources over a long time"; "Mariners need to know if data is old"; they must
   "understand the capabilities and the limitations of the chart" (must-fix 1).
   https://nauticalcharts.noaa.gov/updates/how-accurate-are-nautical-charts/
6. [S6] Brock University Map, Data & GIS Library, *Road Maps of England and Wales from the atlas Britannia, 1675,
   1698*: "Each strip represents a part of the road and the surrounding environment, with the top of one strip
   continued at the bottom of the strip next to it"; the maps note "hills, rivers, bridges, … notable side roads".
   Why a strip is the right form for this image (first question).
   https://brocku.scholaris.ca/items/925b97cd-3481-4579-be3e-d2ca2c30b83b
7. [S7] Old Essex Maps, "Road maps": Ogilby's *Britannia* is "the start of all strip maps and of British Road Books",
   copied by Senex, Gardner and Bowen. https://www.oldessexmaps.co.uk/roadmaps.html
8. [S8] IHO CSPCWG working papers (via search; not re-quoted from the PDF): a survey date shows "the adequacy of the
   equipment used", and "the date of a published chart edition can be misleading (as the source data may be much
   older)". Why the edition date and the checked date are different facts (checked and dropped).
   https://docs.iho.int/mtg_docs/com_wg/CSPCWG/CSPCWG_MISC/CSPCWG_Letters/2011/CSPCWG_L07-11_CSPCWG7_Actions_Gp2.pdf
9. [S9] WorkBoat, "Entering the navigation 'Twilight Zone'": "Each NOAA chart has a source diagram that shows the
   vintage of hydrographic surveys on which the chart is based"; "Depths on some parts of the chart may be based on
   pre-1900 hydrographic surveys conducted with sextants and leadlines". One chart, two methods, and the reader
   told which is which (must-fix 1). https://www.workboat.com/viewpoints/entering-navigation-twilight-zone
10. [S10] Diátaxis, "How-to guides": "The fundamental structure of a how-to guide is a *sequence*. It implies logical
    ordering in time, that there is a sense and meaning to this particular order" (must-fix 2).
    https://diataxis.fr/how-to-guides/
11. [S11] Wikipedia, "Strip map": "a road map laid out similarly to a straight-line diagram", with the ordinary
    road-map details "rather than technical details". The form, and why the image carries no technical clutter.
    https://en.wikipedia.org/wiki/Strip_map

Clones and data: `assets/stats.json` (`edition`, `repos[]` including `ci_selection`, `routes.rustmapper`, `rules[]`,
`runcheck.rustmapper.steps`: `install`, `crawl_ctrl_c`, `second_ctrl_c`, `kill_writes_file`, `export_after_kill`,
`resume_after_kill`); `chart.toml:681-1003` (W1, H1, L1 to L5, X1 to X3, with their `runs` and `fails`);
`scripts/tokens.py:205-218` (`DESIGN_HEAD`); `scripts/render_readme.py:610-684`; `DESIGN.md`; sdist 0.1.3
`src/state.rs:98-114, :285`, `src/bfs_crawler.rs:433`, `src/main.rs:539, :704`, `src/cli.rs:32, :98`; ideal-url-organizer
`159968a` `src/organizers/method_01` to `method_25`, `scripts/import_rust_sitemapper.py:4, :32-48`, `README.md`
"Methods 1-21" and "Methods 22-25"; `Scrapy.git` (499 commits, `67446a4`, `d571e6e`, `e8cbe15`, `099dd6c`), Scrapy
`96e7a1a` `Scraping_project/src/stage2/stage2_worker.py:218-219`, `data/raw/uconn_urls.csv`; `Rust-sitemap.git`
(146 commits by author).
