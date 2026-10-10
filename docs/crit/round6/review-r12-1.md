# Review round 12, reviewer 1: Ben, the owner

10 Oct 2026. I looked at every PNG in `scratchpad/r6/build/round-11/`: the desk sheet at 870 (day and night), the
phone sheet at 390 and 308 (day and night), the desk page (two screens), the phone page at 390 (six screens) and at
360 (seven). I read `README.md`, `SPEC.md`, `LOG.md` round 11 and all the earlier reviews. Nothing already fixed is
repeated here. I also rendered the four published SVGs myself at 3x
(`scratchpad/r12rev/`), and the README at a 1,180 px viewport, an iPad Air held sideways, because nobody has looked
at that width since round 6. Every figure was checked against `assets/stats.json`, the 0.1.3 sdist and the clones.

Verdict: **not yet. 9 / 10.** Round 11 landed. Rule 4 is gone, the breaker is told once, the command is in the
picture, the warnings come before the commands, and the blank rows say what they mean. The image is still right.
It shows my crawler as a route you actually take: install, the loop it runs on every page, the one catch and how
you know you're done, the one key to press, the file you get, and which of my projects reads it. Nothing has a size,
no word names a theme, and nothing in it is there for decoration.

What's left is three things. One is big and nobody has measured it in six rounds. Two are small, and both are
sentences that point somewhere they shouldn't.

1. **On an iPad held sideways, or a laptop window under 1,200 px, the picture is a two-screen poster.** The page
   serves the phone sheet up to a 1,199 px viewport. The phone sheet has grown from about 1,000 units to 1,121 since
   that breakpoint was set, and at those widths GitHub's column is 578 to 765 px. So the picture is drawn 1,080 to
   1,429 px tall. At 1,200 px it drops to 342 px. On the first screen of an iPad you see my name, the role line and
   two rows of the route. The loop, the trap, Ctrl-C and the output file are all below the fold. Must-fix 1.
2. The go_go_go line says it has "the same crawl, resume and export-sitemap commands" as rustmapper. My own run
   check shows rustmapper 0.1.3's `resume` failing at exactly the moment you'd use it. Must-fix 2.
3. "Spiders run by name (`scout`), not by file name" warns about a mistake that no command on the page lets you
   make. Must-fix 3.

## The first question: does it meet my goal?

- **A deep purpose for the map.** Yes. Only a drawing shows the loop and where in the loop the catch is. Take away
  the colour, the dotted box and the bars and it still reads as directions for a stranger: how in, what happens,
  what goes wrong, where you end up.
- **True about my projects.** The image, yes, every row (table below). The page, all but the word "resume" in the
  go_go_go line (must-fix 2).
- **Nothing chases a reason.** All but one sentence under the Scrapy code block (must-fix 3).
- **Nothing announces the theme.** Yes. No theme word, no wink, not in the alt text either.
- **Reads on a phone.** Yes at 390, 360 and 308. **No on a tablet held sideways** (must-fix 1). I said it has to
  accept every format. An iPad is a format, and Safari on iPad asks for the desktop site by default [S3], so it gets
  GitHub's two-column profile with a 700 to 765 px README column [S4][S5].

It still doesn't go to `main` until S2 verifies (ROUTE-UNVERIFIED, P1 at Rust-sitemap's HEAD). That's my job, and
the end-of-October decision from round 11 stands.

## Figures checked

| Printed | Source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.date`; `uploads[3]` 2025-11-08T19:52:41 | | yes |
| `rust_sitemap crawl` | `edition.scripts` = `["rust_sitemap"]`; runcheck `crawl_help` ok | | yes |
| up to 20 pages at a time from each host | sdist `src/state.rs:285` `max_inflight: 20` | 20 | yes |
| 60 s | H1 `quiet`; runcheck `quiet_slow_page` ok (slow page held 15 s, SIGINT 60 s after the last line, 3 of 3 written) | 60 | yes |
| sorted 21 ways | ideal-url-organizer `159968a`: `method_01` to `method_21`, `scripts/import_rust_sitemapper.py` "methods-1-21 pathway" | 21 | yes |
| 176 test functions | 161 Rust test attributes + 15 `def test_` in `python/tests` at `32c2651` (counted today) | 176 | yes |
| 16k lines of Rust | `lines.Rust` 16,390; `cat **/*.rs \| wc -l` at `32c2651` = 16,390 | | yes |
| CI passed 7 Oct 2026: tests, rustfmt | `ci.conclusion` success, `ci.date`, `ci.gates` | | yes |
| Prebuilt for Apple silicon on CPython 3.13 | `edition.wheels` = `cp313-cp313-macosx_11_0_arm64` | | yes |
| 3 min, cold cache, 4-core Linux x86_64 | runcheck `install` median 171.4 s, 4 CPUs, empty `CARGO_HOME` | | yes |
| up to 256 at a time; `--workers 1` | sdist `cli.rs:191` `assert_eq!(workers, 256)`; runcheck `workers_cap` | | yes |
| 50,000 URLs per file | sitemap protocol limit (cited in round 7) | | yes |
| 1,920 test functions (all but 41) · CI 8 Oct · MIT · 69k | `repos[Scrapy]` 1,920; gates; `lines.Python` 69,036 | | yes |
| 143,208 bundled URLs, 134,807 on uconn.edu | `uconn_urls.csv` read with Python `csv` (as pandas does), `urlsplit().hostname` on the raw field | 143,208; 134,807 | yes. If you strip whitespace first you get 134,808 (`'https://healthcareinnovation.online.uconn.edu '`), but `cli.py` doesn't strip, so 134,807 is the number the code loads |
| 5 URLs, 60 s (rule 1) | `stage2_worker.py:218-219` | 5, 60 | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | `git rev-list --count HEAD` in `Rust-sitemap.git` 146, `Scrapy.git` 499; `commits` 101 and 420; `coauthored.agent` 1 and 30 | | yes |
| 15 more · 21 repositories | `repo_count` 22 minus the profile; 4 + 2 shown + 15 | | yes |
| go_go_go "same crawl, resume and export-sitemap commands" | go_go_go `internal/cli/resume.go`; sdist `cli.rs:89` `Resume {`; runcheck `resume_after_kill` **ok: false**, "Database already open. Cannot acquire lock." | | **the command exists in both; in 0.1.3 it fails after a kill** (must-fix 2) |
| "a local 3-page site" (data line) | runcheck `crawl_ctrl_c` "3 lines", `export` "3 `<loc>`" | | yes, for the drawing's commands |

One thing I checked and dropped. In the desk render, `rust_sitemap` looks lighter than `crawl`, and `Received`
lighter than `work item`. They are the same glyph `<use>`s (`hero-g-plex-19-114` for both r's), with the same fill,
and the measured ink per glyph is the same (41.5 against 42.5 for the two r's, 45.8 against 45.8 for the two a's).
It's the letter shapes. Nothing to fix.

## Must fix, ranked

1. **A middle edition of the image for 852 to 1,199 px viewports.** (`scripts/sheets/route.py` `SIZES` and
   `EDITIONS`; `scripts/tokens.py` a `_MID` role table; `chart.toml [hero]` a second breakpoint; `render_readme.py`
   the `<picture>` sources; `scripts/checks/column.py` HERO-COLUMN-PX; `scripts/publish_chart.py`; DESIGN.md's
   column paragraph. About 150 lines and a test file.)
   - **What's wrong, measured.** I took GitHub's column table from `checks/column.py` (vw − 370 from 768 to 1,011,
     vw − 434 from 1,012 to 1,279, 846 from 1,280) and today's sheets (desk 1,280 × 571, phone 600 × 1,121). This is
     how tall the picture is drawn:

     | Viewport | Device | Column | Sheet served | Drawn height |
     |---|---|---|---|---|
     | 1,280 | laptop, full width | 846 | desk | 377 px |
     | 1,200 | | 766 | desk | 342 px |
     | 1,199 | laptop window | 765 | phone | **1,429 px** |
     | 1,194 | iPad Pro 11 sideways [S5] | 760 | phone | **1,420 px** |
     | 1,180 | iPad Air 11 sideways [S4] | 746 | phone | **1,394 px** |
     | 1,100 | laptop window | 666 | phone | **1,244 px** |
     | 1,024 | | 590 | phone | **1,102 px** |
     | 820 | iPad Air portrait | 450 | phone | 841 px (on a 1,180 px tall screen: fine) |

     At 1,180 (`scratchpad/r12rev/mid-screen1.png`) the first 820 px show my name 170 px tall, the role, the
     project name and two route rows. "Ben Russell" is set bigger than any heading on GitHub, and the half of the
     route that matters (the loop, the dotted box, Ctrl-C, the file) is a scroll away. People spend about 57 % of
     their viewing time above the fold [S1]. The drawing's whole point is that you see the route in one look, and
     at these widths you can't.
   - **Why it went unseen.** Round 6 set `breakpoint_px = 1199` so the desk sheet's 19-unit text never falls under
     11 px. That was right. But the gate checks only the smallest text, never the height. And every render since
     round 6 has been at 1,280, 390, 360 or 308.
   - **The fix is the one `<picture>` exists for:** a different composition for a different layout, not the same
     one scaled up [S2]. Add a **mid** edition (`hero-mid-day.svg`, `hero-mid-night.svg`). Use the phone's stacked
     composition (name and role on top, route below, same elements, same order, same words as the phone) at about
     **820 units wide**, with the **desk** type sizes (19 semantic, 25 serif, the desk `display` and `project`
     roles). At 820 units the route's measure is about 690 units, close to the desk's 740, so most rows stay on the
     same number of lines as on the desk. Expected height is about 780 units: **458 px at 852, 728 px at 1,199**,
     down from 1,429.
   - **Serving.** `<source media="(min-width: 852px) and (max-width: 1199px) and (prefers-color-scheme: dark)">`
     → mid-night, then the same without the colour scheme → mid-day, ahead of the phone sources. The phone sources
     become `(max-width: 851px)`. 852 is where the phone sheet reaches 900 px tall (column 482). At that column the
     mid sheet's 19-unit text is 19 × 482 / 820 = 11.2 px, which is just over the floor. Let the build derive both
     numbers from the column table and `SIZES`, not hard-code them.
   - **Gate.** HERO-COLUMN-PX also fails any viewport from 768 to 1,919 where the served hero is drawn taller than
     900 px, alongside the 11 px text floor it already holds. Today's build fails it from 852 to 1,199. With the mid
     edition it passes. T-NOSIZE, T-SAME, T-PURPOSE, T-WORDS and the contrast and bounds checks run on the mid
     editions too.
   - **Review renders** from now on include the README at 1,180 and at 900.

2. **Take "resume" out of the go_go_go line.** (`README.md:94`, hand-typed; `chart.toml:182` claim row text; one
   assertion.)
   - The line reads: "rustmapper's counterpart in Go, with the same crawl, resume and export-sitemap commands". A
     reader takes that to mean rustmapper resumes. 0.1.3 has the subcommand (`cli.rs:89`, "Resume from persisted
     state so interrupted jobs continue"). But my run check killed a crawl and ran `rust_sitemap resume --data-dir
     d3`, and it quit with "Database creation error: Database already open. Cannot acquire lock." (`resume_after_kill`,
     ok false). That's redb's `DatabaseAlreadyOpen` [S8]: the killed process's lock is still there. After a kill is
     the only time you'd reach for `resume`. Round 6 cut the WAL stop's "resume picks up after a kill" from the image
     for this reason. The word got back in through a line about a different repository.
   - New text: "rustmapper's counterpart in Go, with the same crawl and export-sitemap commands, plus optional
     headless-Chrome rendering and SQLite storage with full-text search." The `chart.toml` claim row keeps checking
     go_go_go's `export-sitemap`; the `resume.go` literal goes.
   - Test: in the visible prose, a rustmapper subcommand named next to "rustmapper" may not be one whose runcheck
     probe failed (`resume` ↔ `resume_after_kill`). When 0.1.4 fixes it and the probe passes, the word may come
     back.
   - Saves about one line at 390.

3. **Cut "Spiders run by name (`scout`), not by file name."** (`README.md:88`, hand-typed. The sentence becomes
   "Grafana opens on `localhost:3000`.")
   - The only spider command on the page is `scrapy crawl scout`, and it's already right. You can't copy the mistake
     the sentence warns about. It's standard Scrapy anyway: `scrapy crawl quotes` "runs the spider named `quotes`" [S7].
     The repo's own README says it at the point where you'd go wrong (`Scrapy/README.md:241`, "`scrapy crawl scout`
     # not `scrapy crawl scout_spider`"). On my profile it's a catch somebody once found, kept because it was found,
     not because a visitor needs it. Grafana's port stays: it's where you look next.
   - Saves about two lines at 390 and 360.

That's all. The image itself needs nothing.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page this is | keep (mid edition: desk size, not phone size scaled up) | |
| Role, two caps lines | crawl and data infrastructure; Python and Rust | keep | the drawing under it proves it |
| Empty left column (desk) | nothing, on purpose | keep | the route is the thing you read |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project and what you get | keep | true with the blank rows too: every URL gets a line |
| Start bar, `pip install rustmapper`, "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | |
| Magenta track | one way through, top to bottom | keep | |
| Stop rings | each is one step the tool takes | keep | |
| S1 `rust_sitemap crawl` + seeds | the command, and where URLs come from by default | keep | the command is now in the picture; `--start-url` stays in the code block |
| F1 fetch, per-host cap, scope | the loop's work and how far it reaches | keep | consistent with L5 (siblings like `blog.` are out) |
| W1 write path | it saves as it goes | keep | it's why `export-sitemap` works after a kill (runcheck `export_after_kill` ok) |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Gap in the track under the loop | the only way out of the loop is you | keep | |
| H1, red dotted box | the catch in 0.1.3, and the number that tells you you're done | keep | it goes when 0.1.4 lands |
| C1 Ctrl-C | the one key, and the second press not to make | keep | runcheck `second_ctrl_c` |
| End bar, `data/sitemap.jsonl`, fields | the file, in the struct's own names | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | my projects feed each other | keep | |
| Night editions | the same | keep | |
| Phone editions (390, 308) | the same, in one screen | keep | |
| **Tablet and narrow-laptop widths** | the same, but over two screens | **change** | must-fix 1 |
| Alt text | install, loop, stop, file | keep | 25 words |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image link to the repo | where the project lives | keep | |
| `<picture>` sources | the right sheet for the width | change | must-fix 1 |
| Link line | where to go | keep | |
| "Ben Russell builds …" | what I build | keep | |
| Languages | what I write in | keep | from the data |
| Stack | what I build on | keep | |
| Pick sentence | which tool for which job | keep | |
| rustmapper facts line | alive, tested, size, which commit | keep | |
| Wheel note | whether pip just works on your machine | keep | before the command now |
| "Before you run 0.1.3:" + seven items | what it does to a server, what it can't see, what the file leaves out | keep | every item has its lever or its reason. Strangers point this at other people's servers, so it stays open, not folded |
| rustmapper code block + stop comment | how to run, when to stop, how to recover | keep | see the note on 360 below |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy bullets 1–3 | storage, what happens to a page, how it's watched and deployed | keep | |
| Scrapy run sentence | what `start.py` starts, needs and loads | keep | it's the only place a visitor learns that `--reset-delta`, which Scrapy's README calls "Reset everything", loads a university's 143,208 URLs |
| Scrapy code block | how to start it and point it at your site | keep | |
| Grafana note | where to look once it runs | change | must-fix 3: keep the port, cut the spider-name half |
| Also: ideal-url-organizer | the reader of rustmapper's file | keep | |
| Also: go_go_go | the Go sibling | change | must-fix 2 |
| Also: rust_llm_logger, Ai_code_detector | two more tools, each by what it does | keep | |
| 15 more (details) | the rest | keep | |
| Working rules 1–3 | how I build, each with a dated fact | keep | |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn, how it was run, who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Noted, not ranked

- **The code block at 360.** Two comment lines are 32 columns (`# 0.1.3 runs until stopped: when`, `# sitemap.xml,
  even after a kill`). At 360 GitHub's `pre` has 278 − 2 × 16 = 246 px for content, at 85 % of 16 px [S6], so 30
  monospace columns fit (0.6 em × 13.6 px = 8.2 px each) and 32 take 261 px. In the 360 render the words run into
  the block's right padding and touch its edge. They're still legible, so I'm not ranking it. If the comment is ever
  reworded, keep every line to 30 columns.
- The data line's "a local 3-page site" is true of the drawing's commands. The X2 probe ran on a bigger fixture,
  but the data line doesn't claim to cover that.

## Owner notes, outside this repository

1. **New: Scrapy's README says "Sample URLs loaded" after `python start.py`** (`Scrapy/README.md:96-100`). At
   `96e7a1a` that isn't true. `start.py` loads seeds only with `--reset-delta`, and the same README lists that flag
   as "Reset everything" (`:289`), which loads the 143,208 UConn URLs. My profile now tells the truth and the repo it
   links to doesn't. Fix the quick start: "No seeds are loaded. Point discovery at your site with `scrapy crawl
   scout -a allowed_domains=… -a start_urls=…`."
2. **New, follows from must-fix 2:** `resume` after a kill fails on the stale redb lock. In 0.1.4, open the
   database with a retry, or tell the user to remove the lock, so `resume` does what its help text says.
3. Carried: P1 and its test, 0.1.4 with `[project.scripts]` and the LICENSE, statuses and back-off on 429/503,
   Scrapy's UConn defaults into a named profile, `start.py` accepting `docker compose`, registrable-domain seeding,
   `cargo audit` and `clippy -Dwarnings` as blocking, ideal-url-organizer's raw-`netloc` comparison, the GitHub bio,
   and opening the profile once in the GitHub iOS and Android apps. Add: open it once on an iPad held sideways after
   must-fix 1 ships.

## Sources (new this round)

1. [S1] Nielsen Norman Group, "Scrolling and Attention": "users spent about 57% of their page-viewing time above
   the fold." Why a hero that needs two screens loses the half below (must-fix 1):
   https://www.nngroup.com/articles/scrolling-and-attention/
2. [S2] MDN, "Responsive images": serving "different cropped images ... for various layouts" is "the art direction
   problem", and `<picture>` with `<source media>` is the tool for it. The first `<source>` whose media condition
   is true is the one shown. That's the mid edition and its media order (must-fix 1):
   https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images
3. [S3] Safari on iPadOS asks for the desktop version of sites by default, so an iPad gets GitHub's two-column
   profile, not the mobile one (must-fix 1): https://www.guidingtech.com/how-to-request-desktop-site-on-safari-on-iphone-and-ipad
   and https://discussions.apple.com/thread/251135276
4. [S4] Yesviz, iPad Air 11" (M2): viewport 1,180 × 820 CSS px held sideways:
   https://yesviz.com/devices/ipad-air-11-2024/
5. [S5] Kiosk Group, "Determining screen dimensions for content": iPad Pro 11" 834 × 1,194 CSS px, iPad Air 10.9"
   820 × 1,180. Both sideways widths fall between 1,012 and 1,199:
   https://support.kioskgroup.com/article/660-determining-screen-dimensions-for-content
6. [S6] `github-markdown-css` (sindresorhus), the published copy of GitHub's Markdown styles: `.markdown-body pre`
   `padding: 16px; font-size: 85%`, base `font-size: 16px`, `img { max-width: 100% }`. The 360 note, and why the
   picture fills the column at any width:
   https://raw.githubusercontent.com/sindresorhus/github-markdown-css/main/github-markdown.css
7. [S7] Scrapy tutorial: `scrapy crawl quotes` "runs the spider named `quotes`", and a spider's `name` "must be
   unique within a project". Running by name is the framework's own convention (must-fix 3):
   https://docs.scrapy.org/en/latest/intro/tutorial.html
8. [S8] redb `DatabaseError::DatabaseAlreadyOpen`: "The Database is already open. Cannot acquire lock." That's the
   error 0.1.3's `resume` hit after a kill (must-fix 2): https://docs.rs/redb/latest/redb/enum.DatabaseError.html
9. [S9] GitHub Docs, "Managing your profile README": a profile README is "to tell other people about yourself".
   The test for must-fixes 2 and 3: a line about a sibling repo shouldn't imply something false about mine, and a
   line about Scrapy's internals has to earn its room:
   https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme

Clones and data: `assets/stats.json` (`edition`, `repos[]`, `routes.rustmapper`, `runcheck.rustmapper` steps
`crawl_ctrl_c`, `workers_cap`, `second_ctrl_c`, `quiet_slow_page`, `kill_writes_file`, `export_after_kill`,
`resume_after_kill`); `assets/v9/hero-*.svg` (glyph `<use>` ids, viewBoxes 1280 × 571 and 600 × 1121); sdist 0.1.3
`src/state.rs:285`, `src/cli.rs:89, :191`; Rust-sitemap `32c2651` (161 test attributes, 15 Python tests, 16,390 Rust
lines); `Rust-sitemap.git` and `Scrapy.git` commit counts 146 and 499; Scrapy `96e7a1a` `README.md:86-100, :241,
:289`, `Scraping_project/data/raw/uconn_urls.csv` (143,208 rows, 134,807 on uconn.edu), `src/stage2/stage2_worker.py:218-219`,
`src/stage1/scout_spider.py:47`; ideal-url-organizer `159968a` `src/organizers/`, `scripts/import_rust_sitemapper.py`;
go_go_go `internal/cli/resume.go`; `scripts/checks/column.py` (column table); `chart.toml:9, :180-196`; my renders in
`scratchpad/r12rev/` (`desk-day-2x.png`, `phone-day-3x.png`, `mid-screen1.png`, `p360a.png`, `p360b.png`).
