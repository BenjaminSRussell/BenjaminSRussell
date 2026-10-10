# Review round 4, reviewer 2: the chart historian

10 Oct 2026. Reviewer: a historian of hydrographic charts and sailing directions. For each mark, I ask what the
convention was invented to do, and whether it does that job here. Build looked at: `scratchpad/r6/build/round-03/`.
That covers the desk sheet at 870 and the phone sheet at 390, day and night; `once-p1-lands/` (the same sheet with
S2 drawn); and the page on desk (screens 1–2) and on phone (screens 1–5). Read: `README.md`, `SPEC.md`, `LOG.md`
(rounds 1–3, with what was fixed and what was declined), `DECISIONS.md`, and the nine earlier reviews. I don't repeat
findings that are fixed or already ruled on. Figures were checked against `assets/stats.json`, the 0.1.3 sdist
(`scratchpad/r6/sdist013/rustmapper-0.1.3`), the run check record (`stats.json runcheck`), the clones, and the repo's
own type engine (`scripts/typeset.py text_width`) for every width given below.

Verdict: **does not meet the goal yet. 7 / 10.** I would ship it after one wording fix (must-fix 1), and the other
three are small. The picture is now a real set of directions. Most of its marks do the job their convention was made
for. One row sends a stranger to the wrong file. One mark borrows a convention that says the opposite of what is meant.

## The first question: does it meet the owner's goal?

Taking his tests in order:

- **Every map and every element has a deep purpose.** Nearly every one. The image has one subject: how you get
  rustmapper, what it does with each page, the one thing that goes wrong, how you get out, and what you end up with.
  The forms come from what the project actually does. The crawl is a loop because links go back on the queue
  (`bfs_crawler.rs frontier.add_links`). The loop has no exit because the release's completion check sits in a
  `select!` `else` arm. Tokio runs that arm only when every branch is disabled [S11], and the run check's 3-page crawl
  was still going at 150 s (`runcheck`, `ends_by_itself`). The danger ring sits on the one row that is a danger.
  Nothing has a size. The owner's own question, "is it based on the size of the project or how many commits?", now
  has the answer "nothing has a size". There is one exception, the governor's tick (finding 2).
- **It teaches something true and useful about his projects.** Yes, with one exception, and it is in the row that
  matters most to someone who got stuck: "after a kill, run `export-sitemap`" (finding 1).
- **Nothing chases a reason.** Yes in the image. On the page, one clause in the data line qualifies a figure the page
  no longer prints (finding 4).
- **Nothing announces the theme.** Yes. There are no sea words, and T-WORDS holds. What carries the theme is how the
  marks are used: a line you follow, a ring of dots round a danger, a dated edition at the entrance, terse
  directions, and an invitation to report errors. Each of these does its real job, so none of it reads as costume.
- **Reads on a phone.** Yes. The phone image is about 525 px tall at 390. The link line lands on the first screen.
  Every row fits the 600-unit measure, with G1 the closest at 558.

## How each convention is used, against what it was made for

1. **The track (magenta line).** On a chart, the recommended track is the line you are meant to follow. Chart 1 keeps
   the solid line for the track to be followed (M1, the leading line) and gives recommended tracks their own entries
   (M3, M4) [S3]. In aviation, the magenta line is the course the automation will fly. Vanderburgh's 1997 lecture is
   remembered because crews followed it without understanding it [S9]. Here, the line is the order a run goes in,
   and every stop on it says what happens there. So it is a magenta line you are taught to understand, not just
   follow. **Real purpose.**
2. **The danger ring (dotted line round H1).** IHO S-4 defines the danger line as a line of dots. It "draws attention
   to a danger which would not stand out clearly enough if represented solely by its symbol", or it encloses an area
   too dangerous to cross [S4]. National charts draw it as a black dotted curve [S5]. Here it rings the one fact a
   reader would otherwise skim past, so it is used for exactly its purpose. The accent colour is a change from the
   chart convention, where the dots carry the meaning and the colour doesn't. But it is measured (4.1:1 day,
   6.1:1 night as a graphic), and it is the only accent on the sheet, so it does no harm. **Real purpose.**
3. **The rings at stops.** These are station marks. They are honest, because each one is a file a URL passes
   through, and the desk labels prove it (ROUTE-LABEL). **Real purpose.**
4. **The governor's tick.** This one is borrowed from the Underground diagram, and it is turned upside down. Beck's
   convention, still used on the map today, is that "stations are shown as short ticks, interchanges as circles"
   [S1, S2]. A tick is the plainest mark for a stop on the line. `BREAKS` says the tick was chosen to mean the
   opposite: "it is not a step a URL passes through". Anyone who has read a metro map reads the tick as one more
   stop. The difference only works for readers who never learned the convention. **Used against its purpose**
   (finding 2).
5. **The loop and its arrow.** Flowcharts read top to bottom, and an arrowhead goes where flow runs against that
   direction [S13]. That is exactly where the arrow is drawn, on the way back up. The loop closes at the queue: at
   F1 today and at S2 (`frontier.rs`) in the once-P1 edition. That is true to the code. **Real purpose.**
6. **The gap under the loop.** Charts have no such convention. A dashed or broken track means something else there:
   a track that no fixed marks define [S3]. Here the break has to be read from the drawing alone. Its job is to show
   that the line does not carry you on by itself, and the words next to it say so ("never stops by itself"; "press
   Ctrl-C once"). If a reader misses the gap, they lose nothing. If they see it, it agrees with the words. **Keep**:
   it is cheap and it is true.
7. **Start and end bars.** These are terminus bars, from transit maps rather than charts. On this route the
   entrance and the end are the two fixed points, and you find them in a second. **Real purpose.**
8. **The edition at the entrance ("0.1.3 · 8 NOV 2025").** Charts carry an edition date because a chart older than
   the latest edition is obsolete for navigation. NOAA publishes the dates of latest editions every week for this
   reason [S8]. Putting the release date beside the install line tells a stranger how old the thing they are about
   to install is. A chart also carries a "cleared through" date, the last date it was corrected. Here that is the
   run-check date, and it lives in the data line under the page. That is the right home for it, given the owner's
   rule against fine print in the image. **Real purpose.**
9. **Pictures for the route, text for lookups.** The Coast Pilot exists because some information is "difficult or
   impossible to portray on a nautical chart" [S6]. The Admiralty volumes carry hazards, regulations and port
   facilities next to the chart, not on it [S7]. The page follows this division. The route is drawn. The load
   (20 per host, 256 in all), the 50,000-URL cap [S12], the wheel note and the test counts are text. **Right split.**
10. **"Found a mistake? Open an issue."** This is the chart's oldest courtesy in plain words. Hydrographic offices
    ask users to report discrepancies, and NOAA's ASSIST is the current form of that request [S10]. **Real purpose.**

## Findings

### 1. "After a kill, run `export-sitemap`" sends a stranger to the wrong file

C1 reads "press Ctrl-C once to write `data/sitemap.jsonl`; after a kill, run `export-sitemap`". The next thing on
the route is the end bar and `data/sitemap.jsonl`. So the drawing says that after a kill, `export-sitemap` gets you
back to the same end. It doesn't. In 0.1.3, `run_export_sitemap_command` (`sdist:src/main.rs:387–430`) opens
`CrawlerState` and writes **`sitemap.xml`** (default `--output ./sitemap.xml`, `cli.rs:141`). It writes only the
nodes with status 200. It never writes `sitemap.jsonl`. The run check shows the same thing: after the SIGTERM, "sitemap.jsonl was not
written", while `export-sitemap --data-dir d3 --output k.xml` gave 3 `<loc>`. The other way back is `resume`, which
fails after a kill: "Database already open. Cannot acquire lock." So for anyone whose crawl was killed, the true
direction is "you get `sitemap.xml`, not the JSONL". That is the stranger who most needs the row, and the drawing
gives them the wrong destination.

The same row also leaves a smaller question open. W1 says "saved every 50 ms", and C1 then says Ctrl-C is what
writes the file. A reader asks: saved where, then? The writer thread commits batches to the redb state and the WAL
(`writer_thread.rs:11, :167`; `state.rs:11 use redb`), and `export-sitemap` reads from that same store. If W1 says
"to its database", C1's recovery line makes sense.

### 2. The governor's tick is the transit-map mark for a stop

See convention 4 above. Earlier reviewers kept the tick because "the tick-not-ring difference works". It works only
for a reader who never learned that ticks are stations [S1, S2]. The truthful form is already in the code: the
governor changes how many fetches run at once, so it is a property of the fetch stop, not a separate place.
Sailing directions handle this with a note set under the entry it qualifies. Putting the governor under F1 removes
the inverted mark, saves a row, and keeps the words.

### 3. The desk's rule column is ragged

On the desk, each rule starts at `max(640, label end + 20)` (`route.py:480`), so the three rules start at three
different x positions. `seeder.rs` starts its rule at 640, `bfs_crawler.rs` at 664, and `writer_thread.rs` at 686,
which is 435, 452 and 467 px on screen. A table of stops is read down its columns, and pilot-book tables keep their
columns straight. With a ragged edge it reads as three sentences. Measured with `typeset`: the longest label is
`writer_thread.rs` at 182.4, so one column at 686 fits every rule. The longest, S1 at 515, ends at 1201, under the
1224 limit. In the once-P1 edition, `frontier.rs` (125.4) changes nothing.

### 4. The data line qualifies a figure the page no longer prints

"3 % of Ben's commits carry an AI co-author trailer; 297 more were written by coding agents (Claude, jules) and are
not counted as his." The figures are right (`coauthored_total.agent` 63 of `commits` 2,037 = 3.1 %;
`agent_authored.total` 297). But no figure on the page counts his commits any more. What does depend on authorship
is the dates in the working rules: each is "his first commit adding" the thing (`rules[].first_is_his`), and rule 4
names Claude's. A source note on a chart qualifies something drawn on that chart. This one has no referent, so it
reads as a disclaimer added for its own sake. That is the "chasing a reason" the owner objects to. Round 2 declined
r2-7a (give the share its base), and I am not reopening that. The point here is different: the note should say what
it qualifies.

### Not must-fix

- The license line repeats the data line's provenance ("the build draws only the lines that code and its run check
  prove"). A chart has one source note. I'd cut that second sentence down to "how it's built → DESIGN.md", but it
  does no harm.
- Below the role line, the desk's left column is about 220 px of empty paper. Charts put the title in an unused
  area, and this is that area. Leave it.

## Element audit

### The image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| T1 "Ben Russell" | whose page this is | keep | the title, read first |
| T2 role line | what he builds | keep | the first two words are the subject of the picture |
| R0 "rustmapper" + sentence | which project, and what it does | keep | a pilot entry opens with what the place is |
| R1 start bar | where you begin | keep | a fixed point at the entrance |
| R2 `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the one command, and how old the release is | keep | the edition date beside the entrance does a chart's edition-date job [S8] |
| R5 track | one way through, in run order | keep | a line you follow, and each stop says what happens there [S3, S9] |
| R6 loop + arrow | the rows inside it repeat for every page | keep | the arrowhead is where flow runs against reading order [S13]; it closes at the queue, true to the code |
| S1 seeds | what it contacts by default (sitemaps, CT logs, Common Crawl) | keep | a stranger's real catch: third-party calls by default in 0.1.3 (`cli.rs default_value = "all"`) |
| F1 fetch | each page is fetched and its links queued, parent and subdomains included | keep | the scope fact, plainly stated |
| G1 governor tick + line | it slows down when saving falls behind | change | the words stay; the tick is the transit-map stop mark [S1, S2], so move the line under F1 (must-fix 2) |
| W1 "saved every 50 ms" | progress is kept as it goes | change | add "to its database" so C1's recovery line makes sense (must-fix 1) |
| H1 + dotted ring | the release never stops by itself | keep | the danger line, used for its S-4 purpose [S4, S5]; its cause is right [S11] |
| Gap under the loop | the line doesn't carry you out by itself | keep | there is no chart convention for it, but it is true and agrees with the words |
| C1 Ctrl-C row | the reader's one step, and the recovery after a kill | change | the recovery line points to the wrong file (must-fix 1) |
| R12 end bar | where you end up | keep | the second fixed point |
| R13 `data/sitemap.jsonl` + fields | what is on disk, with the struct's own names | keep | the arrival view |
| R15 arrow + "read by ideal-url-organizer …, with a test" | his projects connect, and the join is tested | keep | the one hand-off proven from both ends |
| Day/night palettes | the same chart in both themes | keep | contrast is measured; the day edition stands alone |
| Empty left column under the role line (desk) | nothing | keep | it is where the title sits, not filler |

### The page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image wrapped in a link to Rust-sitemap | tapping the drawing goes to the project | keep | the picture is the way in |
| Link line | where to go next | keep | it is on the first phone screen |
| "Ben Russell builds…", Languages, Stack | who he is | keep | the lookups belong in text |
| Pick sentence | which of his two crawlers fits your job | keep | a pilot book's choice-of-route note |
| rustmapper sentence | what it is, and what pip gives you today | keep | true to the 0.1.3 wheel (`edition.modules` empty) |
| rustmapper facts line | it is maintained and tested (176 tests, CI 7 Oct, 16k lines of Rust) | keep | checked: `repos[Rust-sitemap]` test_functions 176, Rust 16,390, ci success 2026-10-07 |
| Install code block | the commands to copy | keep | the commands are the ones the wheel installs |
| Wheel note | whether pip will just work | keep | measured cold build, 171 s median |
| Load and 50,000-URL paragraph | how hard it hits a host, and the sitemap cap | keep | the Coast Pilot split [S6]: facts that can't be drawn go in text. 20 and 256 checked in `state.rs:285`, `cli.rs:98`; 50,000 per [S12] |
| Scrapy sentence + facts | the other flagship, alive (1,920 tests, CI 8 Oct, MIT) | keep | checked in `stats.json` |
| Scrapy code block + Grafana line | how to start it | keep | the image half was run in Docker in round 3 |
| Scrapy bullets | what is in it | keep | each one is a design fact |
| Also | four more projects, one line each | keep | |
| "15 more" details | the rest, folded away | keep | 22 − 1 − 2 − 4 = 15, computed |
| Working rules | how he works, each dated by his own first commit | keep | `rules[]` dates checked |
| "Found a mistake?" | where to report an error | keep | the chart's oldest courtesy [S10] |
| Data line | where each claim comes from and when it was checked | change | the AI clause needs a referent (must-fix 4) |
| License line | terms of use | keep (trim optional) | its provenance sentence repeats the data line |

## Must fix, ranked

1. **C1 and W1: the recovery after a kill names the file it actually gives you** (`chart.toml [route.rustmapper]` C1
   and W1; `route.py` desk wrap; `scripts/checks/route.py HEIGHT`; about 15 lines).
   - Set C1 to "press Ctrl-C once to write `data/sitemap.jsonl`; after a kill, `export-sitemap` → `sitemap.xml`".
     Its instead wording, used once a kill writes the file, is unchanged.
   - On the desk the new C1 measures 807 against a measure of 740, so break it at the semicolon into two lines.
   - On the phone it stays two lines. The second line is 538, under the 600 measure. Check that U+2192 is in the
     Plex Mono subset (`scripts/fonts/subset.sh`).
   - Set W1 to "saved to its database every 50 ms" (261 desk, 357 phone). The `const` anchor stays.
   - Add a release anchor for C1: `src/main.rs` `fn = "run_export_sitemap_command"` containing `SitemapWriter::new`.
     C1 stays gated on `export_after_kill` passing.
   - Raise desk ROUTE-HEIGHT from 600 to 620, the SPEC's own 1280 × 620 sheet. With must-fix 2, the desk is about
     571, or about 607 with S2 drawn. Phone is unchanged.
   - Test: C1's drawn text names the export's output file, read from `cli.rs` ExportSitemap `--output`'s default
     basename, so a release that changes it changes the row.
   - Why: after a kill, the drawing currently sends you back to `sitemap.jsonl`. `export-sitemap` writes only
     `sitemap.xml`, and `resume` fails on the lock (`runcheck`; `sdist:src/main.rs:387–430`). The one stranger who
     needs this row gets the wrong destination.
2. **Fold the governor into the fetch stop and drop the tick** (`route.py` G1 drawing; `BREAKS`; tests; about 25
   lines).
   - Draw G1's words as the last line of F1's row, in `ink2` at F1's rule x: at the shared rule column on the desk,
     and under F1's lines at x 88 on the phone.
   - Desk F1 goes from 1 line to 2 (+28 units), and the separate G1 row (36) goes. Net −8 desk. Phone net −9.
   - Remove the tick. Keep `<g id="hero-G1">` and its PURPOSE row, so T-PURPOSE holds.
   - Replace the BREAKS row "The governor has a tick, not a ring" with "The governor is a note under fetch": it
     changes how many fetches run at once (governor `THROTTLE_THRESHOLD_MS`), so it qualifies that stop rather than
     standing as one.
   - Test: no mark is drawn on the track for G1, and G1's text box sits inside F1's row group.
   - Why: on every metro map since Beck, a short tick is a stop [S1, S2]. The mark currently says the opposite of
     what `BREAKS` intends.
3. **One rule column on the desk** (`route.py:476–480`; about 6 lines).
   - Compute `rx = max(G["rule_x"], TX + max(width(label) for drawn labels) + 20)` once per edition, and use it for
     every stop's rule. Today that is 686.4; the longest rule (S1, 515) ends at 1201, under 1224.
   - If a future rule overflows, it wraps; it never shifts the column.
   - Test: every drawn desk rule starts at the same x.
   - Why: a table of stops is read down its columns, and with three starting x positions (435, 452, 467 px on
     screen) it reads as prose.
4. **The data line's AI clause says what it qualifies** (`render_readme.py` `survey` block; one test).
   - Text: "The working rules are dated by Ben's own first commits: 297 commits by coding agents (Claude, jules) are
     not counted as his, and 3 % of his carry an AI co-author trailer."
   - Print it only while at least one `rules[]` row is drawn. The figures come from the same keys as today.
   - Why: a source note qualifies something on the sheet. Today it qualifies a commit count the page doesn't print,
     so it reads as a disclaimer.

## Sources (new this round)

- [S1] "Tube map", Wikipedia: Beck marked ordinary stations with ticks and interchanges with diamonds, later
  circles. https://en.wikipedia.org/wiki/Tube_map
- [S2] K. Field and W. Cartwright, "Another New Design for an Old Map", *Abstracts of the ICA* 1, 81 (2019):
  "Stations are shown as short ticks, interchanges as circles and connectors."
  https://ica-abs.copernicus.org/articles/1/81/2019/
- [S3] Canadian Hydrographic Service, Chart 1, section M (Tracks): M1 "solid line is the track to be followed"; M3/M4
  recommended tracks based or not based on fixed marks.
  https://shc-chs.gc.ca/publications/chart1-carte1/sections/m-tracks/tracks-eng.html. Also the OpenStreetMap INT 1 M
  table, https://wiki.openstreetmap.org/wiki/Template:Table:INT-1:M
- [S4] IHO S-4 B-420.1 wording, as quoted in IHO CL 70/2013 and the CSPCWG letters: a danger line is a line of dots
  that draws attention to a danger which would not stand out clearly enough from its symbol alone.
  https://legacy.iho.int/mtg_docs/circular_letters/english/2013/Cl70e.pdf;
  https://docs.iho.int/mtg_docs/com_wg/CSPCWG/CSPCWG_MISC/CSPCWG_Letters/2010/CSPCWG_L02-10_Foul.pdf
- [S5] Traficom (Finland), chart symbols: a foul area is outlined with a black dotted danger curve, citing B-420.1.
  https://www.traficom.fi/en/chart-symbols
- [S6] NOAA, United States Coast Pilot (InPort record): information "difficult or impossible to portray on a
  nautical chart". https://www.fisheries.noaa.gov/inport/item/39970
- [S7] UKHO, ADMIRALTY Sailing Directions: hazards, pilotage, regulations and port facilities, alongside the chart.
  https://www.admiralty.co.uk/publications/publications-and-reference-guides/admiralty-sailing-directions
- [S8] NOAA, "Dates of Latest Editions", issued weekly: older editions are obsolete; the edition, correction and
  cleared-through dates in the margin. https://www.charts.noaa.gov/MCD/Dole.pdf
- [S9] "Children of the Magenta" (99% Invisible), on Vanderburgh's 1997 American Airlines lecture.
  https://99percentinvisible.org/episode/children-of-the-magenta-automation-paradox-pt-1/; Air Facts,
  https://airfactsjournal.com/2020/09/stepping-down-in-automation-the-real-lesson-for-children-of-the-magenta-line
- [S10] NOAA ASSIST for reporting chart discrepancies (Hydro International, 2018).
  https://www.hydro-international.com/content/news/noaa-simplifies-nautical-chart-error-reporting
- [S11] Tokio `select!` documentation: "If all branches are disabled: go to step 6 … Evaluate the else expression."
  https://docs.rs/tokio/latest/tokio/macro.select.html
- [S12] sitemaps.org protocol: at most 50,000 URLs and 50 MB per file; use a sitemap index beyond that.
  https://www.sitemaps.org/protocol.html
- [S13] ISO 5807:1985, flowchart conventions (flow top to bottom and left to right, arrowheads where it runs
  otherwise; from a secondary guide, since the standard's text is paywalled). https://www.iso.org/standard/11955.html

From the clones and records: `sdist:src/main.rs:387–430` (`run_export_sitemap_command`), `:506–540` (Ctrl-C, the
2 s grace, the JSONL export); `sdist:src/cli.rs:56–61, :98, :130–144`; `sdist:src/writer_thread.rs:11, :167`;
`sdist:src/state.rs:11, :281, :285`; `sdist:src/bfs_crawler.rs:549–556`; `stats.json runcheck.steps` (kill,
export, resume); `stats.json` `repos`, `coauthored_total`, `agent_authored`, `commits`, `rules`, `edition`.
