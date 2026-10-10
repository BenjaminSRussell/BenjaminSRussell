# Review round 5, reviewer 3: the information designer and cartographer

10 Oct 2026. Build looked at: `scratchpad/r6/build/round-04/`: the four sheets (desk 870 and phone 390, day and night),
`once-p1-lands/` (the same sheet with S2 drawn), the page on desk (screens 1 and 2) and phone (screens 1 to 5), and the
four SVGs in `build/assets/`. Read: `README.md`, `SPEC.md`, `LOG.md` (rounds 1 to 4), every review from rounds 1 to 4,
and this round's `review-r05-1.md` and `review-r05-2.md`. I don't repeat what has been fixed. Where I agree with an
open finding from reviewers 1 or 2, I say so in one line and add only what my trade sees in it.

I read the sheet the way a drawing office checks a chart before it goes out. Does each mark have one meaning? Is it
drawn so that meaning survives at the size people see it? Does the loudest thing on the sheet deserve to be the
loudest? Is every figure traceable to its source?

Verdict: **not yet. 7 / 10.** The form is right, and I would not change the concept. One drawing defect affects every
stop on every edition. It is a two-line fix, and it has to be fixed before this ships.

## The first question: does it meet the owner's goal?

In form, yes. The owner asked what the map is for. This one has a reason that comes from the project itself. A
rustmapper run has an order (install, seeds, fetch, save, stop, output), a loop, one way out, a catch at a known
point, and a hand-off to another of his projects. That is a real route. It fits a strip diagram, the form Ogilby used
for roads and engineers use for process charts. Vertical position carries the order, which is the strongest visual
variable there is. The bracket carries the loop, and a list can't show that. The arrow past the end carries the
hand-off. Nothing on the sheet has a size, so the owner's question "is it the size of the project or the commits?"
has the answer "nothing has a size". No word names the theme. The manner carries it: a magenta line you follow, a
dotted danger line round the hazard, terse rows. It reads at 390 px.

What keeps it from shipping, in order:

1. **Every stop symbol is drawn wrong.** The spec gives each stop a paper-filled ring on the track (SPEC §2.3). In
   all four SVGs, the track (`hero-R5`) and the loop (`hero-R6`) come *after* the stop groups in document order. SVG
   paints later elements on top [1], so the magenta line runs straight through every ring. I measured the rendered
   pixel at each ring's centre on the desk day sheet (S1, F1, W1, C1 at x 310): it is (202, 31, 150), the track's
   magenta, not paper (244, 238, 225). The phone sheet is the same: (195, 0, 137) at all four rings. So what the
   visitor sees is not a stop on a line. It's a circle with a bar through it, Φ, a sign that already means
   something else (null, empty set, and on at least one metro map, island platforms [2]). On a line diagram the
   station mark sits on top of the line and breaks it. That break is what makes it read as "a stop here": "a dot
   for every station. No dot, no station" [2]. It is also the operation circle of the process chart [3]. When the
   line runs through the ring, line and ring merge into one object [4], and the ring stops meaning a stop. This is
   Tufte's 1 + 1 = 3: two marks laid together make a third, unintended one [5].
2. **The loudest mark on the sheet is a fact about an 11-month-old release.** I agree with r05-2 #2 and r05-1 #1. The
   danger line is the only red on the sheet and the only text with a line drawn round it, so it is seen first. Hue
   and enclosure are both selective variables [6, 7]. Salience should follow importance. Name the release in the row,
   and let main's fix be said in text.
3. **Rule 2 cites a write-ahead log as a raw layer "never overwritten".** I agree with r05-2 #1. It's the page's one
   factual error. I confirmed the HEAD tree it cites.

Then smaller drawing points, which are mine (inline code spacing, the loop's arrowhead), and four I agree with
(desk file labels, the release date's place, the kill clause, the data line).

## Figures checked

Every figure on the sheet and the page, against `assets/stats.json`, the sdist `scratchpad/r6/sdist013/rustmapper-0.1.3`,
the clones (Rust-sitemap `32c2651` 2026-10-07, ideal-url-organizer `159968a` 2026-10-07) and the run check's own
output files.

| Printed | Source | Value | Holds |
|---|---|---|---|
| `pip install rustmapper` · 0.1.3 · 8 NOV 2025 | `edition.version`, `.date`, `.uploads` | 0.1.3 at 2025-11-08T19:52:41; 0.1.0–0.1.3 all that day | yes |
| `rust_sitemap` (C1, code block) | `edition.scripts` | `["rust_sitemap"]` | yes |
| your URL, plus by default sitemaps, certificate logs, Common Crawl | sdist `src/cli.rs:61` `seeding_strategy`; `routes.S1` verified both | release default `all`; the "if asked" alternative waits for HEAD's `none` | yes |
| queues links on your URL's domain, above or below it | sdist `src/url_utils.rs:81-91`, both dot-boundary branches | parent and child domains of the start | yes |
| fetches fewer pages at once when saving falls behind | sdist `src/main.rs:90-126` (`THROTTLE_THRESHOLD_MS` 500, `UNTHROTTLE` 100, permits) | | yes |
| saved to its database every 50 ms | sdist `src/writer_thread.rs:11` `BATCH_TIMEOUT_MS: u64 = 50` | | yes (wording: see W1) |
| never stops by itself; done when `Received work item` lines stop | `runcheck.rustmapper` `ends_by_itself` false ("still running at 150 s"), `quiet_after_last_page` ok (3 lines for 3 URLs) | | yes for 0.1.3 |
| press Ctrl-C once to write `data/sitemap.jsonl` | `crawl_ctrl_c` ok: exit 0, 2.0 s after one SIGINT, 3 lines; `rc2/work/d2/sitemap.jsonl` has 3 lines | | yes |
| after a kill, `export-sitemap` → `sitemap.xml` | `kill_writes_file` false; `export_after_kill` "3 `<loc>`" | | yes |
| fields: `url, depth, status_code, title, …` | sdist `src/state.rs:98-114` `SitemapNode`, 15 fields; a real line from the run check has those keys | | yes |
| sorted by ideal-url-organizer: `scripts/import_rust_sitemapper.py`, with a test | clone `159968a`: reader and `tests/test_import_rust_sitemapper.py` exist; reader runs `./run.sh --all` (line 131) | `handoffs[0]` `runs` | yes |
| `32c2651` · 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust | `repos[Rust-sitemap]` | 176; success 2026-10-07, `head_sha` = `head.sha`; Rust 16,390 | yes |
| `96e7a1a` · 1,920 tests · CI passed 8 Oct 2026 · MIT · 69k lines of Python | `repos[Scrapy]` | 1,920; success 2026-10-08; MIT; 69,036 | yes |
| 3 min from a cold cache on a 4-core Linux x86_64 machine | runcheck `install` | median 171.4 s, cold, 4 CPUs | yes (2.86 min, rounded) |
| 22 public repositories; 15 more | `repo_count` 22 (the brief's 21 is from an older build) | 22 − profile − 2 − 4 = 15 | yes |
| 45 of rustmapper's 146; 71 of Scrapy's 499 | `repos[].all_hands` 146 / 499 | | yes (checked by r05-1, r05-2; totals agree) |
| go_go_go: same crawl, resume and export-sitemap commands | clone `go_go_go/README.md:236-309` | `resume --data-dir`, `export-sitemap` | yes |
| 25 ways; stage 3; stage 4; 50,000 characters; localhost:3000 | `figures[]` | all `holds: true` | yes |

No figure is wrong. The one false statement is the rule-2 cite (above), which is a claim, not a figure.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| T1 "Ben Russell" | whose work this is | keep | GitHub prints the name in the header too, but the image travels without it (link previews, screenshots). It ties the drawing to him |
| T2 role line | crawl and data infrastructure, Python and Rust | keep | the drawing underneath backs up both words |
| Desk file labels (`seeder.rs` …) | which file to open | **cut** | I side with r05-1 over r05-2. They are lookups, which the spec itself sends to text. The phone, the common case, has none, so the two editions teach different things. And `seeder.rs` sits one baseline under "PYTHON AND RUST" and reads as part of the title |
| R0 "rustmapper" + sentence | which project, and what it does | keep | the title of the strip, set above where the route starts |
| R1 start bar | begin here | keep | the same shape as the end bar, so the two read as a pair (an associative variable [6]) |
| R2 `pip install rustmapper` | the way in | keep | the image's one command |
| R2 release label | how old what you install is | change | agree with r05-1 #3: set it after the command, not at the far right |
| R5 track | one way through, top to bottom | keep, **repaint** | position is the order; must-fix 1 puts it under the rings |
| Stop rings (S1, F1, W1, C1) | a step the tool takes here | **change** | struck through by the track today (must-fix 1). Once they sit on top, they are the dot of a line diagram [2] and the operation circle of a process chart [3] |
| S1 seeds | URLs come from more than links | keep | |
| F1 fetch and scope | the crawl loop, and how wide it goes | keep | |
| G1 governor note | it slows down when its own store lags | keep | the lighter ink and no ring are right. It qualifies F1, it isn't a step, and layering by value is how a chart keeps a qualifier subordinate [5]. r05-2's "500 ms" would add a checkable measure; I don't object |
| W1 "saved to its database every 50 ms" | it saves as it goes | change | agree with r05-2 #3. "Its database" teaches nothing a stranger can check. Log, then store, is the fact |
| R6 loop bracket | which rows repeat for every page | keep; move the arrowhead | the one shape a list can't give. Its arrowhead sits beside W1's ring today (must-fix 6) |
| Gap under the loop | the line doesn't carry you out by itself | keep | it works because of the corner. The track turns into the bracket at the loop's foot, so the eye follows the loop back up (good continuation [4]). The lower segment then reads as a new start. Settled in round 4 |
| H1 danger line | the catch, where it bites | change | agree with r05-2 #2: name the release. It's the most salient mark on the sheet [6, 7] |
| C1 Ctrl-C | the one thing you do, and that one press saves | change | agree with r05-1 #4: move the kill clause into the code block |
| Inline code runs (`Received work item`, `rust_sitemap export-sitemap`, the field list) | the tool's own words | **change** | a Plex Mono space is 600/1000 em against Plex Sans Condensed's 212, so 2.8 times as wide. "Received work item" reads as three loose words, and a two-word command reads as two (must-fix 5) [8] |
| R12 end bar | you arrive here | keep | |
| R13 `data/sitemap.jsonl` + fields | what you get, with real key names | keep | the keys match a real line from the run check |
| R15 hand-off line, arrow, label | the output feeds another of his projects, and the join is tested | keep | thinner weight than the track, same hue: it continues the route without claiming to be part of the run |
| Night editions | the same | keep | I simulated the two accents for dichromats (Machado 2009 [9]). Magenta becomes a grey-blue (109, 118, 142) and red becomes an olive (144, 128, 29) under deuteranopia, so they still differ in hue. The ring strokes render at 4.9:1 on paper after anti-aliasing (12.5 specified), which clears 3:1 [10] |
| Phone editions | the same, with no file labels | keep | the cleanest edition; the desk should match it |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image, linked to Rust-sitemap | above | change | must-fixes 1, 2, 4–7 |
| Alt text | the route in 25 words | keep | 25 words; names rustmapper, the loop, the one Ctrl-C and the file |
| Link line | where to go | keep | |
| Builds / Languages / Stack | what he builds and with what | keep | |
| Pick sentence | which tool for which job | change | agree with r05-1 #6 / r05-2 #5: names first |
| rustmapper sentence | what it is; the API isn't released | keep | |
| rustmapper facts line | alive, tested, size, which snapshot | keep | |
| Install code block | the commands to paste | change | takes the kill comment (r05-1 #4) |
| Wheel note | whether pip will just work for you | keep | |
| Load and 50,000 note | what it does to someone else's server; the sitemap limit | keep | the one politeness fact a site owner needs, in text where it belongs |
| Scrapy sentence, facts, block | the second tool, measured, and how to start it | keep | |
| Grafana note | where to look once it runs | change | agree with r05-2 #6 (code, not an autolink) |
| Scrapy bullets | how it's built | keep | |
| Also | the next four | keep | |
| 15 more | the rest | keep | |
| Working rules 1, 3, 4 | how he works, each dated by a commit | keep | |
| Working rule 2 | the same | change | r05-2 #1 |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn; agent authorship | change | agree with r05-1 #5. A measurement adds to that: inside `<sub>` the lines on the phone render about 27 px apart for text about 13 px high, roughly double-spaced, against 24 px for 16 px body text. The block runs to ten loose lines. `<sub>` is meant for subscripts, not for fine print [11]. Shortening it is the only fix GitHub's sanitiser leaves |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **Paint the track under the stops** (`scripts/sheets/route.py`, assembly at line 620; about 3 lines and a test).
   - Paint the line groups first: `paint = [g for g in order if g in ("R5", "R6", "R15")] + [g for g in order if g
     not in ("R5", "R6", "R15")]`, and build `body` from `paint`. Keep `rep["route"]["drawn"]` in the reading order
     the spec fixes, so T-PURPOSE and the report don't change.
   - Test (every edition): in document order, every stop group's `<circle>` comes after the `hero-R5` path. A
     render check: at each ring's centre, the pixel is within ΔE 3 of `paper`.
   - Why: today the track runs through every ring, and it shows. The centre pixel is the track's magenta on all eight
     rings I measured, desk and phone. A struck circle reads as one merged symbol, Φ [4, 5], not as a stop on the
     line [2, 3]. SVG paints in document order [1], so the spec's paper fill has never been visible.

2. **The danger line names its release** (agree with r05-2 #2(a); `chart.toml` H1). "`{release}` never stops by
   itself; …". From my side: it is the one mark that is both a unique hue and enclosed, so it pops out first [6, 7].
   Its words have to carry its scope.

3. **Rule 2 loses the WAL cite** (agree with r05-2 #1). It's a false claim in the most closely read paragraph.

4. **Cut the desk file labels** (agree with r05-1 #2; `route.py:528-545`). Against r05-2's "keep": the phone has
   none, and one drawing should teach the same thing at every width.

5. **Set the spaces in inline code at the text's word space** (`route.py`, the span splitter at line 305, or the
   run builder in `scripts/typeset.py`; about 10 lines and a test).
   - Inside a backticked span, set each U+0020 as a `label`-role space (Plex Sans Condensed, 212/1000 em), not a
     Plex Mono space (600/1000 em). The glyphs stay mono.
   - Applies to H1 (`Received work item`), C1 (`rust_sitemap export-sitemap`, while it stays) and R13's field list.
     At 19 units each space goes from 11.4 to 4.0. H1's desk line gets about 15 units shorter, and the field list
     about 30.
   - Test: in any line that has both a `cond` run and a `plex` run, no space advance in the `plex` run is more than
     1.3 times the line's `cond` space.
   - Why: at 2.8 times the word space, a three-word log line reads as three separate words, and a command as two
     [8]. Nobody copies text out of an SVG, so exact mono spacing buys nothing there. The code block below keeps the
     real spacing for pasting.

6. **Move the loop's arrowhead off the ring rows** (`route.py:550-551`; 2 lines and a test).
   - Today `ya` is the bracket's midpoint, (250 + 369) / 2, and that lands beside W1's ring (cy 314). On screen the
     arrowhead and ring are 3 px apart and read as one glyph. Set it halfway between the first two loop rings'
     centres instead (desk 282 today; in the once-P1 edition, between S2 and F1).
   - Test: the arrowhead's vertical extent stays at least `ring_r + 2` from every ring's `cy`, on every edition.
   - Why: the arrow means "back up", and it belongs on bare line. Beside a ring it turns into a mark on that row.

7. **The release date beside its command** (agree with r05-1 #3).

8. **The kill clause into the code block** (agree with r05-1 #4). It also removes the longest mixed-type row, which
   makes must-fix 5 smaller.

9. **The data line, shorter** (agree with r05-1 #5). Inside `<sub>` it is double-spaced on the phone (measured
   above), so every clause it loses saves about 27 px.

## Sources (new this round)

1. W3C, *SVG 2*, §3.4 "Rendering order": "an element that appears later in the markup is painted on top of an
   element that appears earlier". https://www.w3.org/TR/SVG2/render.html
2. Transit Maps (Cameron Booth), "Differentiating local/express services": Vignelli's rule, "A dot for every station.
   No dot, no station". Ticks make it "a little trickier", and a marker's form carries meaning (a line through a
   station circle marks island platforms on one Buenos Aires map). https://transitmap.net/express-routes
3. "Flow process chart" (Gilbreth to ASME, 1921; ASME standard, 1947): the circle is the operation, the arrow is the
   move. https://en.wikipedia.org/wiki/Flow_process_chart
4. Wagemans et al., "A century of Gestalt psychology in visual perception: I. Perceptual grouping and figure-ground
   organization", *Psychological Bulletin* 138(6), 2012: good continuation, closure, element and uniform
   connectedness. https://pmc.ncbi.nlm.nih.gov/articles/PMC3482144/
5. Tufte, *Envisioning Information* (1990), "Layering and separation", 1 + 1 = 3: marks placed together make an
   unintended third effect, and lighter value keeps a layer subordinate. Review in *Cahiers de géographie du Québec*
   37(101), 1993. https://assets.erudit.tech/en/revue/cgq/1993/v37/n101/022358ar.pdf
6. Axis Maps, "Visual variables": hue is selective and associative; same shape reads as a group.
   https://axismaps.com/guide/visual-variables
7. T. White, "Symbolization and the Visual Variables", *GIS&T Body of Knowledge* CV-03-008 (2017).
   https://gistbok-ltb.ucgis.org/30/concept/9292
8. M. Butterick, *Practical Typography*, "Monospaced fonts": every character the same width, more horizontal space,
   "In standard body text, there are no good reasons to use monospaced fonts". Metrics measured from the profile's
   own fonts in `scripts/fonts/`: Plex Mono space 600, Plex Sans Condensed space 212, both x-height 516 per 1000.
   https://practicaltypography.com/monospaced-fonts.html
9. G. M. Machado, M. M. Oliveira, L. A. F. Fernandes, "A physiologically-based model for simulation of color vision
   deficiency", *IEEE TVCG* 15(6), 2009. I used its severity-1.0 deutan and protan matrices.
   https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html
10. W3C, *Understanding SC 1.4.11 Non-text Contrast*: thin lines "may be rendered by user agents with a much fainter
    color", so test the least contrasting part. https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
11. MDN, `<sub>`: "should be used only for typographical reasons", not for appearance.
    https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/sub

From the build and the clones: `build/assets/hero-*.svg` (group order: `hero-S1` … `hero-C1` before `hero-R6`,
`hero-R5`); pixel samples from `sheet-desk-day-870.png` and `sheet-phone-day-390.png`; `scripts/sheets/route.py:280-286,
540-575, 620`; `scripts/typeset.py:75-77`; sdist 0.1.3 `src/cli.rs:59-64`, `src/state.rs:98-114`,
`src/url_utils.rs:81-91`, `src/main.rs:85-131`, `src/writer_thread.rs:11-12`; `scratchpad/r6/rc2/work/d2/sitemap.jsonl`;
ideal-url-organizer `159968a` `scripts/import_rust_sitemapper.py:131`; go_go_go `README.md:236-309`;
`assets/stats.json` (`edition`, `repos`, `routes`, `handoffs`, `runcheck`, `figures`, `repo_count`).
