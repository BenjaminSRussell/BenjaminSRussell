# Review round 1, reviewer 2: information design and cartography

9 Oct 2026. Build looked at: `scratchpad/r6/build/round-00/` (desk and phone sheets, day and night; page on desk and
phone, screens 1 to 3) and `once-p1-lands/` (the same sheet with the frontier stop drawn). Read: README.md, SPEC.md,
DECISIONS.md, AUDIT.md rows 92 to 96. No earlier round-6 review exists, so nothing here repeats one.

## Verdict against the owner's goal

**Not ready to ship. Score 6 of 10.**

The islands are gone and nothing in the image has a size. That answers the owner's main complaint ("is it based on
the size of the project or how many commits?"): nothing is. The new picture says one thing you can put in a sentence:
how to start rustmapper, what it does with a URL, where it goes wrong, and what file you end up with. That's a real
purpose that comes from the project, and a big step up from round 5.

It falls short of "every element has a deep purpose" in four ways:

1. **The drawing gets the shape of a crawler wrong.** It draws one straight line: seeds, then governor, then WAL,
   then the file. A crawler is a loop. It fetches a page, takes the links it finds, and puts them back on the queue
   until the queue runs dry. Every reference model says so (Mercator: "repeatedly executes the following steps"; the
   Stanford IR book's five-module loop; Wikipedia's "recursively visited"). The image has no fetch stop at all. The
   governor isn't a step a URL passes through either: it's a separate task that resizes the worker pool from the
   side. The loop is the one fact a picture can show better than a list, and it's the fact the picture leaves out.
   Right now, once colour is removed, the image is a bulleted list with a line beside it (SPEC test 4 passes, and that
   passing is the problem). The line encodes only order, and a numbered list does that too.
2. **The image and the text under it say the same things.** On the phone, inside two screens, the visitor reads
   twice: the install commands (R2, R3, R14 against the code block), the platform note (R4 against the wheel note),
   the release and its date (R2 against "0.1.3 on PyPI, 8 Nov 2025"), the CI date (T5 against the facts line), the
   hand-off (R15 against the hand-off sentence), and the seeds and governor stops (S1, S3 against the two bullets).
   The owner asked earlier for images and text to "differentiate themselves". Visitors read about 20 % of a page's
   words (NN/g), so every repeat crowds out something new.
3. **The left column has three dates and a sha that teach a visitor nothing they can use.** "CODE 32c2651 · 7 OCT
   2026", "CI ON MAIN PASSED 7 OCT 2026" and "AS OF 9 OCT 2026" are provenance. Only the CI line answers a visitor's
   question ("does it work?"). The sha can't be clicked in an image, and it's already in the data line at the
   bottom. "1 OF 21 PUBLIC REPOSITORIES" doesn't say what the 21 are or where the other 20 went.
4. **The build fails as it stands.** `check.py --tier fast` fails ROUTE-UNVERIFIED on S2 (the frontier), so the
   round-00 image goes from seeds straight to the governor. It leaves out the place where URLs are queued, which is
   the heart of the crawler. The `once-p1-lands` render is the real candidate, and it needs P1 in Rust-sitemap.

On a phone, the image reads at 390 px with no text under 14 px. But the code blocks below it hide their warnings off
the right edge (see must-fix 5).

## Figures checked

Each one was checked against `assets/stats.json` and the clones. All are correct.

| Printed | Source | Checked |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `edition.date` | yes, 0.1.3 uploaded 2025-11-08 19:52 |
| prebuilt for macOS arm64 + Python 3.13 | `edition.wheels` = `cp313-cp313-macosx_11_0_arm64` | yes |
| `rust_sitemap crawl` | `edition.scripts` = `["rust_sitemap"]` | yes |
| CODE 32c2651 · 7 OCT 2026 | `repos[Rust-sitemap].head` | yes; clone HEAD `32c26519…`, committer date 2026-10-07 |
| CI ON MAIN PASSED 7 OCT 2026 | `repos[Rust-sitemap].ci` success 2026-10-07 | yes |
| 21 / AS OF 9 OCT 2026 | `repo_count`, `taken` | yes |
| 176 tests · 16k lines of Rust | `test_functions` 176, `lines.Rust` 16,390 | yes |
| Scrapy 1,920 tests · CI 8 Oct · 69k lines | `test_functions`, `ci`, `lines.Python` 69,036 | yes |
| "read by ideal-url-organizer, with a test" | `handoffs[0].state` = `runs`, 15 reader fields all in the writer struct at both trees | yes |
| 3 % AI co-author trailer; 297 agent-authored | `coauthored_total.agent_share` 0.031; `agent_authored.total` 297 | yes |
| install lines ran 9 Oct 2026 on Linux x86_64 | `runcheck.rustmapper` date, runner, ok | yes |

Code facts checked in the clone (32c2651) and the 0.1.3 sdist:

- **H1 is true but incomplete.** `url_utils::is_same_domain` also admits the *parent* domain. The test asserts that
  `test.local` matches `www.test.local`. So a crawl started at `www.` also crawls the apex. That check runs where
  links are extracted (`bfs_crawler.rs:701` at HEAD, `:374` in 0.1.3), which is on the loop, not at the seeds.
- **No depth limit holds in both trees.** HEAD has `--max-urls` and `--duration`. 0.1.3 has neither, and 0.1.3 is
  what `pip install` gets. So for the route the image draws, Ctrl-C is the only way to stop a crawl that won't end.
  That ties H1 to H2, and the image doesn't show the tie.
- **The crawl does end by itself** when the frontier is empty and idle (`completion_detector.rs`). H2 is still
  right: the file is written on the way out, after the first Ctrl-C.
- **The loop exists in both trees.** Discovered links go back via `frontier.add_links(discovered_links)`
  (`bfs_crawler.rs:818` HEAD, `:403` 0.1.3).
- **The governor works from the side.** `governor_task` adds and removes semaphore permits (`governor.rs:48-66`).
  It isn't in the URL's path.
- **The WAL is written before the redb commit** (`writer_thread.rs:125`, "WAL write must succeed before DB commit").
  S4 is correct.
- **`*_seeder.rs` is a glob, not a file.** `src/seeder.rs` exists in both trees and holds the trait every seeder
  implements.
- **The release crawls a site with no robots.txt.** The runcheck passed on 0.1.3. The P1 bug is at HEAD only, which
  `pip` doesn't install. That's why the "true in both" gate on S2 is strict but correct: it keeps the frontier off
  the image until HEAD is fixed too.

## Element audit: the image

| Element | What a visitor learns | Verdict | Why |
|---|---|---|---|
| T1 Ben Russell | whose page it is | keep | first read, largest type |
| T2 role line | he builds crawlers and data infrastructure, in Python and Rust | keep | the picture below is that claim made concrete |
| T3 "1 OF 21 PUBLIC REPOSITORIES" | that something was picked out of 21 | cut | the reader can't tell what "1 of 21" refers to. The link line and "Also" show the rest. The count can go in the data line |
| T4 "CODE 32c2651 · 7 OCT 2026" | the code date | cut | a sha in an image can't be clicked and means nothing to a non-engineer. The CI line answers "alive" with the same date. The sha is already in the data line |
| T5 "CI ON MAIN PASSED 7 OCT 2026" | its tests pass, and when | keep | the one title-block line that answers a visitor's question (does it work?). Computed, so it flips by itself |
| T6 "AS OF 9 OCT 2026" | when the build read the facts | cut | a third date beside two others. "Measured 9 Oct 2026" is in the data line already |
| R0 rustmapper + RUST + sentence | which project, and what it does | keep; cut "RUST" | the sentence is the best line in the image. "RUST" repeats T2 and the text |
| R1 start bar | where you begin | keep | the entrance as a fixed point |
| R2 `pip install rustmapper` + 0.1.3 · 8 Nov 2025 | how to get it, and how old the release is | keep in the image, remove the repeat from the text | the release age matters next to the 7 Oct CI date |
| R3 `rust_sitemap crawl --start-url <site>` | the real command name | keep | wrong commands are the commonest failure. This one comes from the wheel |
| R4 platform note | whether pip will just work for you | keep in the image, cut the wheel note under the code block | a condition at the entrance belongs on the route |
| R5 the magenta track | one way through, top to bottom | change | right now it carries only order. Give it the loop (must-fix 1) so it carries the crawler's structure |
| S1 seeds stop | where URLs come from, beyond links | keep; change file to `seeder.rs` | true in both; the glob is not a file |
| S2 frontier stop (missing today) | polite, one queue per host | keep, blocked on P1 | without it the route skips the queue, the heart of a crawler |
| (new) fetch stop on the loop | it fetches, parses, and sends same-site links back to the queue | add | the step that makes it a crawler. Absent today |
| H1 subdomain/depth trap | it may crawl far more than you meant | move onto the loop; add "and the parent domain" | the scope check happens where links are extracted, so that's where the trap bites. The parent-domain fact is the bigger surprise |
| S3 governor stop | it slows when it can't save, not when the network is slow | change: draw it off the track, as a side note with a short tick to the fetch stop | it acts on the workers from outside the URL's path. Inline, it says something false about order |
| S4 WAL stop | a crash doesn't lose the crawl; `resume` exists | keep | the reason it's durable. Correct order |
| H2 Ctrl-C trap | the file appears only when it stops; one Ctrl-C, not two | change wording to lead with the action | it's the remedy for H1 in the release, so it should read as an instruction |
| R12 end bar | where you end up | keep | |
| R13 `data/sitemap.jsonl` + fields | what you get, with the real field names | keep | |
| R14 export-sitemap (desk only) | the second output | cut from the image | it's in the copyable code block right below, and the phone already drops it |
| R15 hand-off arrow to ideal-url-organizer | his projects connect, and that join is tested | keep in the image; cut the repeat sentence from the text | the only line that shows a body of work rather than one repo |
| stop rings, hatch blocks | stop vs trap | keep | they're the only marks that tell the two apart. The hatch reads as a warning without a legend |
| desk file-name column | the stop is real code you can open | keep on desk | costs nothing on desk; the phone rightly drops it |

## Element audit: the page

| Block | What a visitor learns | Verdict | Why |
|---|---|---|---|
| picture element and alt text | the route, for screen readers too | keep; update the alt to say "a loop" once must-fix 1 lands | alt states the message |
| link line | where to click | keep | |
| "Ben Russell builds…", Languages, Stack | who he is, what he uses | keep | the lookups belong in text |
| rustmapper sentence "…0.1.3 on PyPI, 8 Nov 2025." | release and date | change: cut the version-and-date clause | the image says it one inch above |
| rustmapper facts line | deps, tests, CI, size | keep | the only place with tests and size |
| install code block | copyable commands | keep; fix phone width | text is right for copying |
| wheel note under the code block | platform condition | cut | the image says it (R4) |
| governor bullet, seeds bullet | why the design is unusual | keep | they give the reason; the image gives only the fact. The wording isn't a copy |
| hand-off sentence 1 | output feeds ideal-url-organizer | cut | the image says it (R15) |
| hand-off sentence 2 "not read by Scrapy yet" | an unfinished join | cut | DECISIONS itself calls this Ben's to-do list, and it reads as "his projects don't fit together" |
| Scrapy sentence, facts, code block, note, bullets | the second project, as text | keep; fix phone width of the code block | text suits a project that has no image |
| Also, 15 more | the other repositories | keep | |
| Working rules | how he works, tied to dated code | keep | |
| data line | how every figure is checked | keep; take T3, T4 and T6 in here (count, sha, date) | the right home for provenance |
| license line | | keep | |

## Must fix, ranked

1. **Draw the loop and the fetch stop, and take the governor off the line.** Change `sheets/route.py` and
   `chart.toml [route.rustmapper]`.
   - Add a stop `F1`, kind `stop`, file `bfs_crawler.rs`, text "fetch the page; same-site links go back to the
     queue". Anchors in both trees: `src/bfs_crawler.rs` contains "frontier.add_links(discovered_links)" and
     "BfsCrawler::is_same_domain(".
   - Draw one return path in the left gutter, between the track and the hatch column: from the F1 ring, out to the
     left by 14 units (phone 18), up to the S2 ring, then back into the track. Stroke `flare` at LINE weight, with a
     filled arrowhead (8 × 6, phone 10 × 8) pointing up at the top.
   - Move H1 onto that return path. Put its hatch block on the up-stroke, and its text on the row after F1: "links
     to subdomains and the parent domain count as same-site; there is no depth limit".
   - Move S3 out of the stop sequence. Put it as a right-side note on F1's row, or the row under it. Mark it with a
     short horizontal tick, not a ring, so it reads as acting on the fetch, not as a step.
   - Keep S4 after F1, and the end bar after S4.
   - Why: a crawler is a loop (Mercator, IR book). The scope trap bites at link extraction. The governor is a side
     controller. A list can't draw a loop; a chart can. This is what makes the image a map of the project and not a
     list with a line.
   - Size: rows go from 6 to 7 on desk, so the sheet grows about 36 units, within the 640 gate. On phone it grows
     about 46 units, within the 1,200 gate.
2. **Land P1 in Rust-sitemap, or don't ship the hero.** The fast tier fails today, and the round-00 image has no
   queue. The `once-p1-lands` build is the image to ship once `tests/robots_4xx_allows_crawl.rs` is at HEAD. Don't
   loosen the gate.
3. **Cut T3, T4 and T6 from the image.** Leave the name, the role and one line: "CI PASSED ON MAIN 7 OCT 2026". Move
   "1 of 21 public repositories" into the data line, where the sha and the measured date already are. On phone this
   frees two lines (about 68 units) at the top of the first screen. Also cut "RUST" from R0. Update T-PURPOSE rows.
4. **Remove the repeats from the text.** Cut "0.1.3 on PyPI, 8 Nov 2025" from the rustmapper sentence. Cut the
   wheel note under the install block. Cut both hand-off sentences, so the `handoffs` marker writes nothing while R15
   is drawn. Cut R14 from the desk image. Each fact then appears once: the image owns the route, the release, the
   platform condition and the hand-off; the text owns copyable commands, test counts and the why.
5. **Fit both code blocks to a 375 px phone (38 characters a line).** Today the Scrapy comments "# from the clone
   root, start.py fails" and "# needs docker and docker-compose" sit off-screen on phone. Those are its traps. Put
   each comment on its own line above its command, and break `rust_sitemap export-sitemap --data-dir ./data` after
   `export-sitemap`. Add a render check that measures the longest line of each fenced block in README against 38.
6. **Reword H2 so it reads as the remedy:** "to stop it: one Ctrl-C writes the file; a second exits without it".
   In 0.1.3 there's no `--max-urls` or `--duration`, so this is how a pip user stops the crawl H1 warned about. The
   anchors stay the same.
7. **Show the stop's real file:** change S1's file from `*_seeder.rs` to `seeder.rs`. It exists in both trees, and
   the stop column is meant to name a file you can open.

## Sources (new this round)

The web-search budget for this run was used up by earlier agents in the same turn, so these came from direct
fetches of primary pages and from the clones. Each one bears on a finding above.

1. Najork and Heydon, *High-Performance Web Crawling*, SRC Research Report 173 (2001), §3, "Mercator's
   Architecture": "takes a list of seed URLs … and repeatedly executes the following steps"; the worker "goes back
   to step 1"; one FIFO queue per host in the back end. https://www.cs.cornell.edu/courses/cs685/2002fa/mercator.pdf
   (must-fix 1; S2 wording)
2. Manning, Raghavan and Schütze, *Introduction to Information Retrieval*, §20.2.1 "Crawler architecture": the
   five-module loop, links pass the URL filter and duplicate check and return to the frontier, with robots filtering
   right before the fetch. https://nlp.stanford.edu/IR-book/html/htmledition/crawler-architecture-1.html
   (must-fix 1)
3. Wikipedia, "Web crawler", overview: seeds, frontier, "recursively visited according to a set of policies";
   politeness. https://en.wikipedia.org/wiki/Web_crawler (must-fix 1)
4. Wikipedia, "Harry Beck": the Tube diagram shows connections, not distances, because riders need to know how to
   get between stations. https://en.wikipedia.org/wiki/Harry_Beck (a route picture earns its form by showing how
   the parts connect, here the loop; nothing needs a size)
5. Wikipedia, "Strip map": a straight-line road map that keeps only what the traveller needs, after Ogilby's
   *Britannia* (1675). https://en.wikipedia.org/wiki/Strip_map (supports the strip form; a strip still has to show
   junctions and returns)
6. Wikipedia, "Visual variable" (Bertin): position is the imposition variable; hue and shape are associative.
   https://en.wikipedia.org/wiki/Visual_variable (the track uses position only for order, so a list matches it;
   ring against hatch is a correct use of shape)
7. Wikipedia, "Chartjunk" (Tufte, 1983): "non-data-ink or redundant data-ink".
   https://en.wikipedia.org/wiki/Chartjunk (must-fix 3, 4)
8. Tufte, "Sparkline theory and practice", on the NYT Knicks graphic: labels the reader already knows "are not
   needed", and a repeated tint is "an unnecessary congruence".
   https://www.edwardtufte.com/notebook/sparkline-theory-and-practice-edward-tufte/ (must-fix 4: say each fact once)
9. Nielsen Norman Group, "How Little Do Users Read?": "at most 28 % of the words … 20 % is more likely".
   https://www.nngroup.com/articles/how-little-do-users-read/ (must-fix 4)
10. Nielsen Norman Group, "F-shaped pattern": first lines and the left side get the most fixations.
    https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/ (must-fix 3: the top-left lines are the
    most-read spot and shouldn't hold a sha)
11. Nielsen Norman Group, "Scrolling and attention": 57 % of viewing time is above the fold, 17 % on the second
    screen. https://www.nngroup.com/articles/scrolling-and-attention/ (must-fix 3, 4: the first two phone screens
    are the budget)
12. RFC 9309 §2.3.1.3 and §2.3.1.4: a 4xx robots.txt means the crawler may access everything; a 5xx means assume
    complete disallow. https://www.rfc-editor.org/rfc/rfc9309.html (must-fix 2)
13. Wikipedia, "Sailing Directions": they give "navigational hazards" and "details of routes", the local knowledge a
    pilot would give. https://en.wikipedia.org/wiki/Sailing_Directions (a hazard comes with the way to clear it:
    must-fix 6)
14. The clones: Rust-sitemap 32c2651 `src/bfs_crawler.rs:690-706, 818`, `src/url_utils.rs:81-91, 273-290`,
    `src/orchestration/governor.rs:7-70`, `src/writer_thread.rs:125-176`, `src/completion_detector.rs:1-8`,
    `src/cli.rs:81-85`, `src/seeder.rs:1`; sdist 0.1.3 `src/bfs_crawler.rs:374, 403`, `src/main.rs:84-91`,
    `src/cli.rs` (no `max_urls` or `duration`).
