# Review round 8, reviewer 3: the historian of charts and sailing directions

10 Oct 2026. My lens is the history of hydrographic charts and pilot books. Every convention on a chart or in a
book of sailing directions exists because a navigator needed it for something. For each mark here I ask what the
convention was invented to do, and whether it is doing that job or only borrowing its look.

What I looked at: every PNG in `scratchpad/r6/build/round-07/`. That is the desk sheet at 870 px (day and night), the
phone sheet at 390 and 308 px (day and night), the desk page (two screens) and the phone page at 390 px (six screens)
and 360 px (six screens). I also looked at the four SVGs in `build/assets/` for geometry. I read `README.md`,
`SPEC.md`, `LOG.md` (rounds 1 to 7), the reviews from rounds 1 to 7, and this round's `review-r08-1.md`. I don't repeat
anything already fixed. Where I agree with review 1 of this round, I say so in one line and add only what my lens
adds.

Verdict: **not yet. 8 / 10.** The image is the right kind of drawing. It is a strip chart of one passage: one route,
read in order, showing only what lies along it. A text beside it carries what the drawing can't show. That is how
Ogilby's road strips and every pilot book have worked for three centuries, and here each convention does its old job.
What stops me shipping it is one row. At the reader's only manoeuvre, Ctrl-C, the drawing doesn't give the caution
that a pilot book would print at exactly that point, and the tool itself prompts the wrong action there. The
contradiction review 1 found (21 against 25) also has to go.

## The first question: does it meet the owner's goal?

- **A deep purpose for the map.** Yes. A strip map exists to get a stranger along one route without the rest of the
  country. Ogilby's 1675 *Britannia* drew each road as a strip, top to bottom, with a page of text "giving additional
  advice for the map's use" [S4]. This image does the same for rustmapper: install, seed, the loop of fetch and
  write, the catch, the way out, the file you get, and where that file goes next. The loop bracket and the break in
  the track show something no list can: those rows repeat, and the line doesn't carry you out of them.
- **True and useful about his actual projects.** Yes, line by line (figures below), with one exception on the page
  (review 1, must-fix 1). The image teaches how his crawler behaves, which is more than the README text says at a
  glance.
- **Nothing chases a reason.** In the image, every mark has a job (table below). Nothing has a size, so the owner's
  "is it based on the size of the project?" has the answer "nothing has a size".
- **Nothing announces the theme.** Yes. No word names the sea. The manner carries it: a magenta course line, a dotted
  danger line, an edition date at the entrance, a continuation note at the foot, a source note under the text.
- **Reads on a phone.** Yes at 308 and 278 px, with review 1's heading gap as the one fault.

## Each convention, and whether it does its real job

| Mark | The convention it comes from | What that convention is for | Does it do that here? |
|---|---|---|---|
| The whole strip, top to bottom | the strip road map (Ogilby, 1675) and the route chart | one route, in order, nothing off it; text alongside for what can't be drawn [S4] | **Yes.** It is the right genre for a tool with one way through. |
| Magenta line from the start bar to the end bar | the recommended track: "that portion of a navigation line that a ship should use for navigation" [S5]; magenta is the colour of the active route on chartplotters (cited in earlier rounds) | the line you follow, kept apart from everything you only look at | **Yes.** One line, one way, read downwards. |
| Start bar at `pip install` | the departure point of a passage, and the terminus bar of a line diagram | where you begin | **Yes.** |
| Rings on the track | waypoints, or stations on a line diagram | a place where something happens | **Yes** for S1, F1 and W1. C1 is the reader's action; its words carry that. |
| Loop bracket with an arrow up | no chart convention; it comes from the flow chart | which rows repeat | **Yes.** It is honest about being a diagram and carries the fact the owner asked for. |
| Break in the track under the loop | none on charts | the line does not carry you on | **Yes**, together with the bracket's corner, where the track turns back up and has no way down. |
| Dotted line round H1 | the danger line (INT 1 K1): draws attention to a danger that would not otherwise stand out | mark the one danger on the route | **Yes.** It also gives the clearing mark: "done when it stops printing `Received work item`". A clearing line is "the boundary between a safe and a dangerous area" [S3]. |
| "0.1.3 · 8 NOV 2025" at the entrance | the chart's edition date, read before you trust the chart | how old the thing you use is | **Yes**, and it is placed where it is used. |
| End bar, then `data/sitemap.jsonl` and its fields | arrival | what you end up with, in its own words | **Yes.** |
| Thin line, arrowhead, "sorted 21 ways by ideal-url-organizer" | the continuation note at a chart's edge, and Ogilby's side roads labelled with where they lead | which sheet or road takes you on | **Yes.** It names the next project and what it does with the file. The count must agree with the page (review 1, must-fix 1). |
| Night editions | ECDIS day, dusk and night colour tables: one token, different values per display mode [S6] | the same chart, legible in other light | **Yes.** Same marks, same words; magenta and the danger dots hold on navy. |
| **C1 "press Ctrl-C once to write `data/sitemap.jsonl`"** | the directions for a manoeuvre, with its caution printed on the same line | do this, watch for that, and not the other thing | **Not quite** (must-fix 2). It gives the action. The caution and the mark that says you have arrived are missing, and the file name is repeated in the row below. |

## The row that needs its caution

Read what the tool prints when a stranger does what the image says. This is the run check's own crawl log,
`scratchpad/r6/rc2/work/crawl.log`:

```
Received Ctrl+C, initiating graceful shutdown...
Press Ctrl+C again to force quit
...
Saving state...
Exported 3 nodes to JSONL
Saved to: …/d/sitemap.jsonl
Graceful shutdown complete
```

The tool's first reply to Ctrl-C invites a second one. In 0.1.3 (`sdist main.rs:506-541`) and at HEAD
(`Rust-sitemap:src/orchestration/shutdown.rs:20-50`), that second Ctrl-C calls `std::process::exit(1)` before
`export_to_jsonl` runs, so no `sitemap.jsonl` is written. In 0.1.3 the window is at least the 2 s grace period
(`config.rs:34`, `SHUTDOWN_GRACE_PERIOD_SECS = 2`) plus however long saving and exporting take. On a large crawl that
is long, and the stranger is watching a terminal that tells them to press again.

The image's "once" is right, but it doesn't say why, and it gives no mark for when it is safe. This is exactly the
place where sailing directions print a caution: on the manoeuvre, with the consequence and the mark to watch for.
Bowditch describes sailing directions as carrying what the chart doesn't show, "dangers" and "procedures" among them
[S1]. Safety-writing practice says a warning should state the hazard, what happens if you don't avoid it, and how to
avoid it, and that it can sit inside a single step of a procedure [S8]. The command-line guidelines say the same in
their own terms: "Tell the user what will happen when they hit Ctrl-C again, in case it is a destructive action"
[S9]. rustmapper doesn't, and the drawing is the one place that can, at no cost. Docker Compose prints the same
"press Ctrl+C again to force" on stop [S7], so a developer will press it from habit.

The fix also removes a repetition. `data/sitemap.jsonl` is printed on C1 and again on the end row directly below it,
with the end bar between. "Saved to:" is the arrival mark, and the end row already names the file.

## Figures checked

Against `assets/stats.json`, the 0.1.3 sdist (`scratchpad/r6/sdist013/rustmapper-0.1.3`), the Rust-sitemap clone at
`32c2651`, and the run-check logs.

| Printed | Source | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `edition.date`; all four uploads on 2025-11-08 | yes |
| by default, sitemaps, certificate logs, Common Crawl | sdist `cli.rs:58` `default_value = "all"`; `routes` S1 verified in both trees | yes |
| 500 ms | sdist `main.rs` `THROTTLE_THRESHOLD_MS`; F1 verified | yes |
| logged to disk, then saved to redb, in batches | `routes` W1: the 50 ms wording is unverified and the fallback is drawn | yes |
| never exits by itself; `Received work item` | `runcheck` `ends_by_itself` false at 150 s; `quiet_after_last_page` true; sdist `bfs_crawler.rs:433` | yes |
| Ctrl-C once writes `data/sitemap.jsonl` | `crawl_ctrl_c`: exit 0 2.0 s after one SIGINT, 3 lines | yes |
| fields `url, depth, status_code, title` | `SitemapNode`, both trees | yes |
| sorted 21 ways | `figures` `self.methods` = 21 (handoff row) | yes; 25 on the page (review 1) |
| 176 tests · CI 7 Oct 2026 · 16k lines of Rust · `32c2651` | `repos[Rust-sitemap]`: 176; success 2026-10-07; Rust 16,390; head 32c2651 | yes |
| 1,920 tests (CI selects all but 41) · CI 8 Oct · MIT · 69k · `96e7a1a` | `repos[Scrapy]`: 1,920; `ci_selection.not_selected` 41 (16 + 25); MIT; Python 69,036 | yes |
| 3 min from a cold cache, 4-core Linux | `runcheck` install median 171.4 s, 4 CPUs, cold | yes |
| 20 at a time to one host, 256 in all | sdist `cli.rs:98` "256", `state.rs` `max_inflight: 20` | yes |
| Languages: Python, Rust; Swift, JavaScript, TypeScript, C, Go | `main_language` over 21 repositories: Python 10, Swift 3, JS 2, TS 2, Rust 2, C 1, Go 1 | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | Rust-sitemap 101 + Claude 45; Scrapy 420 + 49 + 22 + 8 = 499, agents 49 + 22 = 71; `coauthored.agent` 1 and 30 | yes |
| 15 more | 22 − profile − 2 − 4 | yes |
| four stages; 5 URLs; 60 s; 50,000 characters | `figures` rows, all `holds` | yes |
| "even after a kill" (code block) | `kill_writes_file` false, `export_after_kill` true (3 `<loc>`) | yes: the block's comment refers to `sitemap.xml` from `export-sitemap`, which is right |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page | keep | the authority's name, read first |
| Role line, two caps lines | crawl and data infrastructure, Python and Rust | keep | the strip under it proves it |
| Empty left column (desk) | nothing, on purpose | keep | old Admiralty charts left the land blank because the navigator didn't need it. Blank space here keeps the route first |
| "rustmapper" + header sentence | which project and what it writes | change (phone) | agree with review 1, must-fix 2: the heading sits one line under the role |
| Start bar | where you begin | keep | departure point |
| `pip install rustmapper` | the way in | keep | |
| "0.1.3 · 8 NOV 2025" | how old the release you install is | keep | edition date at the point of use |
| Magenta track | one way through, read downwards | keep | the recommended track [S5] |
| Rings S1, F1, W1 | steps the tool takes | keep | waypoints |
| S1 seeds | URLs come from more than links, by default | keep | |
| F1 fetch, throttle, scope | the crawl loop, its back-pressure, its reach | keep | |
| W1 write path | it persists as it goes | keep | the reason an export after a kill works |
| Loop bracket and up arrow | which rows repeat | keep | the one fact only a drawing gives |
| Break in the track | no way on but yours | keep | |
| H1 and its dotted line | the catch in 0.1.3 and the mark that says you're done | keep | a danger line with its clearing mark [S3] |
| C1 ring and words | the reader's one manoeuvre | change | add its caution and arrival mark; drop the repeated file name (must-fix 2) |
| End bar, `data/sitemap.jsonl`, fields | what you get | keep | |
| Hand-off line, arrow, "sorted 21 ways by ideal-url-organizer" | his projects feed each other | keep | continuation note. The page must agree on the count (must-fix 1) |
| Night editions | the same in dark mode | keep | [S6] |
| Phone editions | the same on one screen | change | the heading gap (must-fix 3) |
| Alt text | what the drawing does, in 25 words | keep | "It loops until one Ctrl-C writes data/sitemap.jsonl" is right |

## Every block of the page

The page around the image is the sailing directions to the chart. Its job is what Bowditch gives the Enroute
volumes: what the chart can't show, such as dangers, procedures and regulations [S1]. I judge each block by that.

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Link line | where to go | keep | |
| "Ben Russell builds …", Languages, Stack | what he builds, with what | keep | |
| Pick sentence | which tool for which job | keep | |
| rustmapper sentence | the Python API isn't released | keep | |
| rustmapper facts line | alive, tested, size, which commit | keep | "On main at" keeps it apart from the 0.1.3 drawing |
| rustmapper code block | how to run, stop and recover | keep | copyable directions; fits 360 px |
| Wheel note | when pip just works | keep | a condition of the entrance |
| Load and robots note, 50,000 note | what it does to the site you point it at | keep | this is the pilot book's "Caution" paragraph, and the most useful text on the page for a stranger |
| Scrapy sentence and facts | the second tool, measured | keep | |
| Scrapy lead sentence and code block | how to start it | keep | checked against the clone |
| Grafana note and bullets | what Scrapy does that rustmapper doesn't | keep | |
| Also: ideal-url-organizer | the URL sorter | change | agree with review 1, must-fix 1 |
| Also: go_go_go | the Go counterpart | change | agree with review 1, must-fix 3 |
| Also: rust_llm_logger | a mechanism | keep | |
| Also: Ai_code_detector | what it detects | change | agree with review 1, must-fix 6 |
| 15 more | the rest | keep | |
| Working rules 1 and 4 | how he works, with proof | keep | |
| Working rules 2 and 3 | as above | change | agree with review 1, must-fixes 4 and 5 |
| "Found a mistake? Open an issue." | the page can be corrected by its readers | keep | this is the Hydrographic Note. Chart offices ask users to report "errors in any navigational publication" on a set form [S2], because users find errors first. It sits right above the source note, which is where it belongs |
| Data line | which release was drawn, how it was checked, who wrote the code | keep | the chart's source note: what rests on which survey. "With seeding off" says honestly that the S1 row was the one row not exercised |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **One count for ideal-url-organizer** (agree with review 1, must-fix 1, as written there). A continuation note
   and the page it points to must not disagree. On a chart, two depths for one spot is the error a surveyor fears
   most.

2. **C1 gives its caution and its arrival mark** (`chart.toml` C1, :576-583; `scripts/runcheck.py`, one new probe;
   `stats.json` re-run; one fixture test; no height change).
   - Text: "press Ctrl-C once; a second before `Saved to:` quits without writing it". Measured with
     `typeset.text_width`: about 516 units at 19 on the desk (one line, against 740 of measure) and about 706 at 26
     on the phone (two lines, as C1 has today). The sheets keep their heights: desk 571, phone 1,135.
   - Head anchors (`src/orchestration/shutdown.rs`): "Press Ctrl+C again to force quit", "std::process::exit(1)",
     `println!("Saved to: `, with order anchors: the exit handler is spawned before `export_to_jsonl` is called.
     Release anchors: the same strings in `src/main.rs`. These hold today in both trees (`shutdown.rs:22, :34, :47`;
     sdist `main.rs:508, :520, :539`).
   - New run-check probe `second_ctrl_c` (gate false, like `kill_writes_file`): start the same 3-page crawl, send
     SIGINT at 45 s and a second SIGINT 0.3 s later (inside 0.1.3's 2 s grace), wait 10 s. It passes if the exit code
     is 1 and `d/sitemap.jsonl` is absent. C1 gets `runs = ["crawl_ctrl_c", "second_ctrl_c"]`.
   - Fallback (an `instead` entry): today's wording, used when the probe or an anchor fails, for example when a
     release stops discarding the export on a second Ctrl-C.
   - PURPOSE C1: "the reader's one step, the mark that says it's done, and what a second Ctrl-C costs". The alt text
     stays.
   - Why: it is the only row where the stranger acts, and the tool prompts them to press again. Sailing directions
     print the caution on the manoeuvre it belongs to [S1]. A warning names the hazard, its consequence and how to
     avoid it, and it can sit inside one step [S8]. Command-line practice asks a tool to say what a second Ctrl-C
     does when it destroys work [S9]. rustmapper doesn't say it, so the drawing must. It also removes the file name
     printed twice in two rows.

3. **The phone heading gap** (agree with review 1, must-fix 2, as written there). On a chart the title and the area
   it covers are separate lines of the title block. Here "PYTHON AND RUST" and "rustmapper" read as one block.

4. **go_go_go without browser impersonation** (agree with review 1, must-fix 3).

5. **Working rule 3 states the measured fact** (agree with review 1, must-fix 4).

6. **Rule 2's cite in the form of the others; Ai_code_detector says what it does** (agree with review 1, must-fixes 5
   and 6).

**Owner, outside this repository** (rounds 4 to 8, not re-ranked): fix P1 and the idle test, and ship 0.1.4. While
0.1.3 is current, the danger line stays on the drawing, as a pilot book describes the harbour as it is today. In
Rust-sitemap, two lines in `shutdown.rs` would make C1's caution unnecessary: print "Press Ctrl+C again to quit
without writing sitemap.jsonl", or don't exit before the export has finished. When a release does that, the probe
fails and C1 falls back by itself.

**Noted, not ranked.** A chart carries its edition date and its last-correction date on the sheet itself, so a copy
torn from the folio still says how current it is. This image carries the release's date but not the date it was last
checked (10 Oct 2026, in the data line only). Round 2 cut the image's "as of" line, and the text's facts line answers
"alive", so I don't reopen it. If the image is ever posted on its own (a social card, a talk slide), add it back on
that edition.

## Sources (new this round)

1. [S1] Bowditch, *The American Practical Navigator* (NGA Pub. 9, 2017), ch. 6 "Nautical Publications", §604 (Sailing
   Directions Enroute "include additional information about coastal and port approach not depicted on nautical
   charts, including … dangers, navigational aids, procedures") and §605 (Coast Pilots "supplement nautical charts"):
   https://thenauticalalmanac.com/2017_Bowditch-_American_Practical_Navigator/Volume-_1/03-%20Part%201-%20Fundamentals/Chapter%206-%20Nautical%20Publications.pdf
2. [S2] UK Hydrographic Office, "Use of third party data and H-notes": "Please notify us if you discover or suspect
   any of the following by submitting the appropriate Hydrographic note": new dangers, changes in aids, "errors in
   any navigational publication": https://www.gov.uk/guidance/use-of-third-party-data-and-h-notes
3. [S3] S-57 attribute CATNAV, category of navigation line (from the IHO dictionary): a clearing line is "a straight
   line that marks the boundary between a safe and a dangerous area or that passes clear of a navigational danger";
   a leading line is one "along the path of which a vessel can approach safely":
   https://docs.teledynecaris.com/s-57/attribut/def/d-catnav.htm
4. [S4] "Britannia (atlas)", John Ogilby, 1675: 100 strip road maps, each with "a double-sided page of text giving
   additional advice for the map's use"; distances "marked and numbered on each map":
   https://en.wikipedia.org/wiki/Britannia_(atlas)
5. [S5] OpenStreetMap Seamarks, "Leading Lines": the recommended track is "that portion of a navigation line that a
   ship should use for navigation"; clearing lines mark "the boundary between a safe and a dangerous area":
   https://wiki.openstreetmap.org/wiki/Seamarks/Leading_Lines
6. [S6] Teledyne CARIS, "Portrayal Files: Colour Tables" (S-52 and S-101): colours are five-character tokens, and the
   token files are "named according to ECDIS display modes" (`day_bright.xml`, `night_bright.xml`), with one token
   taking different values per mode:
   https://docs.teledynecaris.com/docs/5.1/base%20editor/CARIS%20BASE%20Editor%20Help/CARISFiles_PortrayalFiles.53.6.html
7. [S7] Docker Community Forums, "How to gracefully exit and remove docker-compose services after issuing CTRL-C?":
   Compose prints "Gracefully stopping... (press Ctrl+C again to force)". A developer's habit is to press again:
   https://forums.docker.com/t/how-to-gracefully-exit-and-remove-docker-compose-services-after-issuing-ctrl-c/113470
8. [S8] Holland & Knight, "New ANSI Standard for Product Safety Information in Manuals" (ANSI Z535.6): safety
   messages describe "the nature of a hazard", the consequence of not avoiding it and how to avoid it; "embedded"
   messages sit inside a single step of a procedure:
   https://www.hklaw.com/en/insights/publications/2007/06/new-ansi-standard-for-product-safety-information-i
9. [S9] Command Line Interface Guidelines, "Signals and control characters" (the site was cited in an earlier round;
   this passage was not): "Tell the user what will happen when they hit Ctrl-C again, in case it is a destructive
   action": https://clig.dev/

Clones and data: `assets/stats.json` (`edition`, `routes.rustmapper`, `figures`, `runcheck.rustmapper` including
`kill_writes_file`, `export_after_kill`, `resume_after_kill`, `repos[]`, `coauthored_total`); sdist 0.1.3
`src/main.rs:495-541` (the Ctrl-C handlers, `exit(1)`, the 2 s sleep, `Saved to:`), `src/config.rs:34`,
`src/cli.rs:24-155`, `src/bfs_crawler.rs:433`; Rust-sitemap `32c2651` `src/orchestration/shutdown.rs:1-55`;
`scratchpad/r6/rc2/work/crawl.log`; `scripts/runcheck.py` (probe layout); `build/assets/hero-*.svg` (track, loop and
hand-off geometry and stroke widths); `scripts/typeset.text_width` (C1 widths).
