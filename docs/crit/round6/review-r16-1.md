# Review round 16, reviewer 1: Ben, the owner

10 Oct 2026. I looked at every PNG in `scratchpad/r6/build/round-15/`: the sheet on desk at 870 and 846 (day and
night), mid at 746 (day and night), phone at 390 and 308 (day and night), the README at 1,280 (two screens), at 390
(seven) and 360 (seven), and the first screen at 900, 1,180, 1,280, 1,366 and 1,920. I read `README.md`, `SPEC.md`,
`LOG.md` round 15, the three round 15 reviews, and `chart.toml`'s H0, H1, L6 and blank-rows entries. I don't repeat
anything round 15 fixed. Every figure was checked again (table below).

Verdict: **not yet. 8 / 10.** Round 15 landed. S2 can't be drawn on 0.1.3 any more, the true sheets publish before
`main` names them, Scrapy's effect on a site has the same form as rustmapper's, rustmapper's own name is on the page,
and the install note says only what was tried. The map is still the right map. It's the route a URL takes through my
tool. Nothing in it has a size, and nothing in it is an island.

What stops me is the box round 15 added. It put the stall right above the line that says how you know you're done,
inside one dotted line. So the picture now says two things that can't both be true: "a disallowed link stalls its
host", then "done when `Received work item` lines stop for 60 s". After a stall the lines stop too, and the picture
calls it done. `chart.toml` says so itself, above H0: "A stalled host also stops the `Received work item` lines, so
H1's rule reads a stall as done; the dotted line marks it as a catch." Putting a rock on the chart doesn't fix the
line that says the channel is clear. That's the one finding that blocks, and it's one word.

## The first question: does it meet my goal?

- **A deep purpose for the map.** Yes. How you get rustmapper 0.1.3, where its URLs come from, the loop each page
  goes through, the catches inside the loop, the one key, the file, and the project of mine that reads it next. A list
  can't show which rows repeat, or that the catches sit inside the loop.
- **True about my projects.** Every figure holds (table below). One word on the image does not: "done" (must-fix 1).
- **Nothing chases a reason.** The box's first line half-chases one. It names a fault, but it doesn't say what the
  fault does to *you*, and "stalls its host" reads, to someone who runs a site, like it hangs their server. A warning
  has to say what happened in words the reader uses, and what to do about it [S2]. Must-fixes 2 and 3.
- **Nothing announces the theme.** Yes. No sea words in the image, the alt text, the headings or DESIGN.md. The dotted
  line round a danger is a chart's manner, and nobody is told that.
- **Reads on a phone.** The image is one screen at 390, 360 and 308, day and night. But inside the box the words sit
  on the dots: on the 390 phone sheet there's about 3 px from the text to the dots, and "60 s" touches the right edge
  (must-fix 4). The page is 5,525 CSS px at 390. That's long, but every screen opens on something you can tell apart.
- **Would I ship it as is?** No. Must-fix 1 is a false word on the first thing anyone sees.

## What I checked this round

**What happens after a stall, in 0.1.3** (`scratchpad/r6/sdist013/rustmapper-0.1.3`, and r15-2's logs in
`scratchpad/r15-2/probe/`):

```
src/frontier.rs:684-690   eprintln!("Shard {}: URL {} blocked by robots.txt", …); continue;   (no push_ready_host)
crawl_shop.log:5          Shard 3: URL https://localhost/search blocked by robots.txt
crawl_shop.log:6-7        two more `Received work item` lines, then nothing until the SIGINT
d_shop/sitemap.jsonl      18 rows; products/p1..p12: crawled_at null, status_code null
```

So three things are true after a stall. The `Received work item` lines stop. The terminal shows one line that says
why: `blocked by robots.txt`. And the pages that never came are in the file as blank rows, so `export-sitemap` leaves
them out. Once the lines have stopped for 60 s nothing more will come either way. H1's 60 is the longest a started
item can take to finish, and a stalled host is pushed back only when a page brings a new link to it. So *quit then*
is right in both cases. *Done* is right in one.

**The blank rows.** The fold's third item says "Errors, timeouts and non-HTML 200s are left blank". A stranger whose
https crawl stalled sees a column of blanks and reads them as errors. Pages it never fetched are blank too: the
probe's own `beyond.html` (`non200_status`), the stalled products above, anything still queued at Ctrl-C. The first
sentence ("Only HTML pages that answer 200 … get a `status_code`") covers them, but nobody reads it as a list of what's
blank. The second sentence is the one they read.

**A note on r15-2's shop run, not on the page.** `/collections/all` and `/pages/about` were fetched (server log: 200),
yet their rows are blank. That's the fixture, not the stall. Python's `http.server` serves a file with no extension as
`application/octet-stream` [S8, S9], and 0.1.3 writes a status only for HTML. So "1 row of 18 with a status" overstates
the stall. "None of the 12 products fetched" is still right, and that's all L6's comment claims. Nothing printed
changes.

**The box.** `scripts/sheets/route.py:59` `DANGER_PAD = 6` on every side. The phone dots are a 3.4-unit round-capped
stroke (`hero-phone-day.svg`: `<rect x="82" … width="465.2" height="113.6" … stroke-width="3.4"`), so the clear space
inside is about 4.3 units, 2.8 px at 390 and 2.2 px at 308. The phone sheet has 1 unit of height left (1,121 of 1,122),
so the padding can grow only sideways. There's room for that: the loop bracket's right side is at about x 58, and the
sheet runs to 600.

## Figures checked

| Printed | Source | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version` 0.1.3, `uploads[3].time` 2025-11-08T19:52:41 | yes |
| `pip install rustmapper` / `rust_sitemap crawl` | `edition.scripts` `["rust_sitemap"]` | yes |
| up to 20 pages at a time from each host | sdist `state.rs` `max_inflight: 20` | yes |
| 256 at a time; `--workers 1` | sdist `cli.rs` `default_value = "256"` | yes |
| `RustSitemapCrawler/1.0`; `--user-agent` | sdist `cli.rs` default; `steps.json` `ua_seen` ok, no From | yes |
| on https, a disallowed link stalls its host / L6 | `frontier.rs:684-690`; `robots_stall` ok (5 before, 0 after), `robots_resume` ok | yes (wording: must-fix 3) |
| Until a host's `robots.txt` is back … disallowed ones too | `robots_late` ok: 10 of 10 disallowed fetched | yes |
| never exits by itself; 60 s | H1 audit 30 + 20 + 4 + 1 → 60; `quiet_slow_page` | yes; "done": **no** (must-fix 1) |
| a second press before the `Saved to` line quits without writing | sdist `main.rs:508` "Press Ctrl+C again to force quit", `:535-539` | yes |
| `data/sitemap.jsonl`; `url, depth, status_code, title` | `main.rs:535`; the file's keys | yes |
| sorted 21 ways by ideal-url-organizer | `159968a` `src/main.py:56-78`: 21 entries in `self.methods`, `method_01` to `method_21` | yes |
| 176 test functions · CI passed 7 Oct 2026: tests, rustfmt · 16k lines | `test_functions` 176; `ci` success 2026-10-07, `gates` `["tests","rustfmt"]` (Clippy `\|\| true`, audit `continue-on-error`, `ci.yml:109,154`); `lines.Rust` 16,390 | yes |
| Claude authored 45 of its 146 commits; co-signed 1 of his own 101 | `all_hands` 146, `others` Claude 45, `commits` 101, `coauthored.agent` 1 | yes |
| Scrapy 1,920 (CI selects all but 41) · 8 Oct · tests, ruff, mypy, bandit · MIT · 69k | `test_functions` 1,920, `ci_selection.not_selected` 41; `gates`; `license` MIT; `lines.Python` 69,036 | yes |
| jules, Claude authored 71 of its 499; co-signed 30 of his own 420 | `others` 49 + 22; `all_hands` 499; `coauthored.agent` 30; `commits` 420 | yes |
| 15 more | `repo_count` 22 = profile + rustmapper + Scrapy + 4 + 15 | yes |
| tested over http and https on 10 Oct 2026 (Linux x86_64) | `rc15/steps.json` `date` 2026-10-10; `robots_stall`, `robots_late` ran | yes |

## Must fix, ranked

1. **H1 says "done" where it means "quit".** (`chart.toml:948`, one word; the six editions; DESIGN.md has only "0.1.3
   never exits by itself", so it doesn't change; the tests that pin H1's text: `test_round7.py:388`,
   `test_round9.py:223`, `test_round10.py:196`, `test_round12.py:222`, `test_route.py:156,282`.)
   - **What's wrong.** "done when `Received work item` lines stop for 60 s" is false after a stall, and the line right
     above it says stalls happen. The visitor follows the picture, gets a short file, and the picture told them it
     was complete.
   - **Change.** `text = "{release} never exits by itself; quit when `Received work item` lines stop for {quiet} s"`.
     "quit when" is the same 9 characters as "done when", so every edition keeps its line breaks and its height. It's
     true either way: after 60 s of quiet nothing more will come, stalled or finished. It's an instruction, like the
     code block's "# for 60 s, then Ctrl-C once", and the next ring says how to quit. Update the H0 comment in
     `chart.toml` ("so H1's rule reads a stall as done") to say why the word changed.
   - **Why it matters.** Feedback at the end of a run is what tells you that you got what you came for [S1]. A word
     that says "finished" when the run was cut short is the worst status a tool can give [S3].
   - **Test.** H1's text contains "quit when" and not "done when". A new pairing test: if H0 is drawn, H1 doesn't
     contain "done".

2. **Give the stall its sign and its cost, where the visitor acts.** (`chart.toml` L6, line 1145, and its `instead`
   copy; the fold row at `chart.toml:1282`; one anchor; about 8 lines.)
   - **What's wrong.** L6 says what 0.1.3 does, but not how you'd know it happened or what it costs you. The fold
     explains blank rows as "errors, timeouts and non-HTML 200s", so a stalled crawl's blanks get blamed on the site.
   - **Change, L6.** Append one sentence: "A `blocked by robots.txt` line in its output is the sign." (Anchor: the
     message literal H0 already uses. It's an `eprintln!`, so it's on the terminal the visitor is watching. No probe
     is needed: `robots_stall` already runs the branch that prints it.)
   - **Change, fold.** "… Errors, timeouts, non-HTML 200s and pages it never reached are left blank, `crawled_at` too,
     never retried." (Anchor: probe `non200_status`, whose `beyond.html` was never asked for and has a null row.)
   - **Why.** Say what went wrong, and put the warning next to where it bites [S2, S3]. The visitor bites at the
     terminal and at the file.
   - **Size.** +1 line at 390 for L6. The fold is closed by default.
   - **Test.** L6's text contains `blocked by robots.txt`. The fold row contains "never reached". AUDIT-COVER and
     STRINGS-TWICE stay clean.

3. **H0: say what waits, in the visitor's words.** (`chart.toml:846` and its `instead`, line 857; DESIGN.md line 6;
   `test_round13.py:270`, `test_round15.py:253`.)
   - **What's wrong.** "on https, a disallowed link stalls its host". To anyone who runs a site, "stalls its host"
     reads as "hangs the server". The thing that stops is the crawler's queue for that host, and the thing the
     visitor loses is pages.
   - **Change.** `text = "on https, pages behind a disallowed link wait"` (45 characters; today's is 43). It names
     what the visitor loses (pages), says where (behind the link), and uses L6's verb ("wait"), which round 15 already
     chose over "ends" because a new link can wake the host. That claims no more than L6 does. If it measures over
     one phone line at 308 (the test round 15 already has), use "on https, links after a disallowed one wait" (43).
   - **Why.** A warning names the problem in the reader's words [S2]. A host queue that is never scheduled again is
     starved, not "stalled" [S10], and the reader doesn't need either word.
   - **Test.** H0 stays one line in all six editions (round 15's test). DESIGN.md quotes the new text.

4. **Give the words inside the dotted line room to breathe, sideways only.** (`scripts/sheets/route.py:59-61`,
   `_danger` at `:516`; about 6 lines.)
   - **What's wrong.** The text runs into the dots: about 2.8 px of clear space at 390, 2.2 px at 308, and "60 s"
     touches the right edge on both phone sheets. A border is meant to set the words apart, and here it crowds them
     [S4]. A design system's alert pads its text 20 px across and 16 px down [S5, S6]. I'm not asking for that much,
     but 3 px isn't padding.
   - **Change.** Split the padding: `DANGER_PAD_X = {"phone": 12, "mid": 10, "desk": 10}`, `DANGER_PAD_Y = 6`
     (unchanged, because the phone sheet has 1 unit of height to spare). On phone the box goes from x 82–547 to x 76–553,
     which is clear of the loop bracket (about x 58) and of the 600 edge.
   - **Test.** A new BOX-PAD check in the render tier: in every edition, the clear space from the text's ink box to
     the inner edge of the dots (pad minus half the stroke) is at least 8 units sideways. ROUTE-HEIGHT and
     HERO-COLUMN-PX don't move.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page it is; survives a screenshot | keep | |
| Role, two caps lines | crawl and data infrastructure; Python and Rust | keep | the route under it proves line one |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project, and what you get | keep | |
| Start bar + `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | the date is what makes every 0.1.3 caution fair |
| Magenta track | one way through, top to bottom | keep | order is the subject's strongest channel |
| Stop rings | each is one step the tool takes | keep | |
| S1 `rust_sitemap crawl` + seeds | the real command; three outside sources by default | keep | |
| F1 fetch, 20 per host, scope | the loop's work and how far it reaches | keep | |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Dotted line round the catches | where in the loop it goes wrong | keep, pad it | must-fix 4 |
| H0 the stall | on https, pages can stop coming | **change** | must-fix 3: "stalls its host" reads as harm to the server |
| H1 never exits; 60 s | when to stop it | **change** | must-fix 1: "done" is false after H0 |
| Gap in the track under the loop | the only way out is you | keep | |
| C1 Ctrl-C once | the one key, and the press not to make | keep | |
| End bar + `data/sitemap.jsonl` + fields | the file, in the struct's own names | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | my projects feed each other | keep | 21 is `self.methods` |
| W1 (not drawn) | (would say) a kill keeps the pages | keep undrawn | the code block says it where you type |
| S2 (not drawn) | (would say) paced by robots.txt | keep undrawn | waits for a release with the parser |
| Night editions | the same | keep | the red dots read on navy |
| Desk (1,000), mid (820), phone (600) editions | the same, sized to the column | keep | |
| Alt text | install, loop, stop, file | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image link to the repository | where the project lives | keep | |
| `<picture>` sources, phone `<img>` | the right sheet for the width, and a readable fallback | keep | |
| Link line | where to go | keep | |
| "Ben Russell builds …" | what I build | keep | |
| Languages | what I write in | keep | |
| Stack | what I build on | keep | |
| Pick sentence | which tool for which job | keep | |
| rustmapper facts line | alive, tested, size, which commit, who wrote it | keep | |
| Wheel note | whether `pip` just works on your machine | keep | says only what was tried |
| "Before you run 0.1.3:" L1, L7, L4, L2, L5 | what it does to someone else's server, with the lever for each | keep | |
| L6 the stall | what 0.1.3 does on https | **change** | must-fix 2: add the sign |
| Fold "What 0.1.3's files miss or get wrong" | the file's caveats, one tap away | **change** (item 3) | must-fix 2: blanks include pages never reached |
| rustmapper code block | how to run it, when to stop, how to recover | keep | "then Ctrl-C once" already says quit, not done |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy bullets 1–3 | storage; what happens to a page; how it's watched, stopped and deployed | keep | |
| Scrapy run paragraph + "Before you run it:" | what `start.py` starts and needs; what the crawl does to a site | keep | same form as rustmapper's now |
| Scrapy code block | how to point it at your site and name your bot | keep | |
| Grafana and `data/delta/` | where to look once it runs | keep | |
| Also: four tools | the file's reader, the Go sibling, two more tools by what they do | keep | |
| 15 more (fold) | the rest | keep | |
| Working rules 1–3 | how I build, each with its evidence | keep | |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn and how it was run | keep | names http and https now |
| Licence line | the profile's terms | keep | |

## Noted, not ranked

- Six cautions and four more in the fold, against one sentence of what rustmapper is for. All of them are true, and
  the levers make them useful. But the page now reads like 0.1.3's issue list, and that says more about the release
  than about me. The cure isn't on this page: it's 0.1.4 (below), which retires H0, L6 and half of L4 by itself.
- L4 and L6 sit next to each other and are both about `robots.txt` on https. Once must-fix 2 lands they may read
  better as one item, but their anchors and probes differ, so I'm leaving that to taste.
- "co-signed 1 of his own 101" is still my taste note from round 15.

## Owner notes, outside this repository

1. **Cut 0.1.4 from main, after one check.** Main re-pushes the host after a blocked URL (`6bcb6cd`) and fails closed
   until `robots.txt` is in. A release cut from it retires H0, L6 and L4's first clause, and with
   `parse_crawl_delay_secs` it draws S2. First rule out r15-2's finding that main at `32c2651` deferred the start URL
   over https and then reported an empty frontier. If that's real, 0.1.4 would crawl nothing on https.
2. **Carried:** exits when idle, P1, `response.url()` as the link base, `noindex` and canonical pages out of
   `export-sitemap`, `resume` after a kill, the robots.txt port, a LICENSE, `[project.scripts]`, a default user agent
   with a contact; the `workflow_dispatch` dry run on `v12/purpose`; the GitHub iOS app, light and dark; Scrapy stage
   2's robots check, delay and name; `[position]` and `[contact]`; a real iPad.

## Sources (new this round; none cited in earlier rounds)

1. [S1] Ben Shneiderman, "The Eight Golden Rules of Interface Design", rules 3 and 4: "Offer informative feedback";
   "Design dialogs to yield closure … Informative feedback at the completion of a group of actions gives users the
   satisfaction of accomplishment". A completion signal that fires on a cut-short run is wrong feedback (must-fix 1):
   https://www.cs.umd.edu/users/ben/goldenrules.html
2. [S2] Nielsen Norman Group, "Error-Message Guidelines": "Provide descriptions of the exact problems"; "Merely
   stating the problem is also not enough; offer some potential remedies"; "Display the error message close to the
   error's source". Hence the sign in L6 and the plain words in H0 (must-fixes 2, 3):
   https://www.nngroup.com/articles/error-message-guidelines/
3. [S3] Nielsen Norman Group, "Indicators, Validations, and Notifications": indicators "should be shown in close
   proximity to that element", and users who miss a status message repeat the action. The visitor reads status at the
   terminal and the file, so that's where the sign goes (must-fixes 1, 2):
   https://www.nngroup.com/articles/indicators-validations-notifications/
4. [S4] Matthew Butterick, Practical Typography, "Rules and borders": "Thicker borders are counterproductive—they
   create noise that upstages the information inside". A dotted line pressed against its words does that (must-fix 4):
   https://practicaltypography.com/rules-and-borders.html
5. [S5] U.S. Web Design System, "Alert": the heading "shouldn't include more than one line of text", in "concise,
   human-readable language"; when a user must act, "let them know what they need to do". It pads its alert on both
   axes (`$theme-alert-padding-x`, `-y`) (must-fixes 3, 4): https://designsystem.digital.gov/components/alert/
6. [S6] U.S. Web Design System, "Settings": `$theme-alert-padding-x` 2.5 units and `-y` 2 units (USWDS units are
   8 px: 20 px and 16 px). That's the scale of padding a warning box is given (must-fix 4):
   https://designsystem.digital.gov/documentation/settings/
7. [S7] GOV.UK Design System, "Inset text": "Use inset text very sparingly - it's less effective if it's overused",
   and it can be missed, so critical content belongs in a warning. That's one reason to keep the dotted line for the
   two catches and not add a third box for the sign (must-fix 2 puts it in L6 instead):
   https://design-system.service.gov.uk/components/inset-text/
8. [S8] Python docs, `http.server`: `guess_type` looks up the extension, then `mimetypes`, then
   `default_content_type`, which is `'application/octet-stream'` by default. That's why the shop fixture's
   extensionless pages came back blank (note on r15-2): https://docs.python.org/3/library/http.server.html
9. [S9] Python docs, `mimetypes`: the type "is `None` if the type can't be guessed (missing or unknown suffix)". Same
   note: https://docs.python.org/3/library/mimetypes.html
10. [S10] Wikipedia, "Starvation (computer science)": "a process is perpetually denied necessary resources to process
    its work". That's what a never-re-pushed host queue is, and why the image should name the pages that wait, not
    the host (must-fix 3): https://en.wikipedia.org/wiki/Starvation_(computer_science)
11. [S11] The sdist and clones, read for this round: `rustmapper-0.1.3` `src/frontier.rs:670-700`, `src/cli.rs:18-60`,
    `src/state.rs:280-290`, `src/main.rs:505-541`, `src/bfs_crawler.rs:433`; `scratchpad/r15-2/probe/crawl_shop.log`,
    `req_shop.log`, `d_shop/sitemap.jsonl`; `scratchpad/r6/rc15/steps.json`; ideal-url-organizer `159968a`
    `src/main.py:56-78`; Rust-sitemap `32c2651` `.github/workflows/ci.yml:94-166`; `assets/stats.json`;
    `scripts/sheets/route.py:59-61,516-540`; `build/round-15/build/assets/hero-phone-day.svg`.
