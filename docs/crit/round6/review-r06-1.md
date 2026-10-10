# Review round 6, reviewer 1: Ben, the owner

10 Oct 2026. What I looked at: `scratchpad/r6/build/round-05/`, meaning the desk sheet (870) and the phone sheet (390) in
day and night, the page on desk (screens 1 and 2) and the page on phone (screens 1 to 5). I read `README.md`,
`SPEC.md`, `LOG.md` (the round-5 fixes) and the fifteen reviews from rounds 1 to 5. I don't repeat anything that was
fixed. Every figure was checked against `assets/stats.json`, the 0.1.3 sdist (`scratchpad/r6/sdist013`), the
Rust-sitemap clone at `32c2651`, the ideal-url-organizer and go_go_go clones, and the PyPI JSON and GitHub API today.

Verdict: **not yet. 8 / 10.** It's the best this has been. The image finally has a purpose: it shows how my crawler
works and where its output goes, and every row answers a question a stranger has. Last round's fixes all landed.
The desk now teaches the same thing as the phone, the date sits on its command, the Ctrl-C row is one line, the data
line is two facts, and the rings are drawn over the track. I'm not shipping it yet for two reasons. One sentence on
the page vouches for code that I know is broken. And the thing I keep saying is mine to do still isn't done.

## The first question: does it meet my goal?

Close. Element by element it does what I asked for. Each mark is a step my tool actually takes, from the release pip
installs, and you read them in order. Nothing has a size. Nothing is drawn for decoration. No word names the theme.
The manner is there for anyone who knows it: one magenta line to follow, which is the colour a chartplotter uses for
the route [S1], a bar at each end, and a single red warning on the one stretch that goes wrong [S1]. Nobody has to
be told it's a chart. It reads on the phone in one screen.

What stops me shipping it:

1. **The page vouches for main, and main is broken in a way the page doesn't mention.** The sentence after the load
   note reads: "On main, a crawl stops by itself once the site runs out of pages:
   `tests/crawl_exits_when_idle.rs` passes in CI at `32c2651`. That fix is not on PyPI yet." I opened that test. It
   runs the crawler with `--ignore-robots` (`tests/crawl_exits_when_idle.rs:67`). Its fixture server answers 404 for
   `/robots.txt`, and on main a 404 robots.txt means the URL is deferred every 250 ms and never fetched
   (`src/robots.rs:19,32` match only status 200; `src/frontier.rs`, "fail closed until robots.txt arrives (#47)").
   Round 1 ran it: on a site with no robots.txt, main "fetches nothing … exits at 90 s with `processed 0`"
   (review-r01-3). RFC 9309 §2.3.1.3 says a crawler "MAY access any resources" after a 4xx. Google treats every 4xx
   except 429 "as if a valid robots.txt file didn't exist" [S5]. So the test proves main stops only when robots
   checks are turned off. "That fix is not on PyPI yet" tells a visitor main is the better build. Rust-sitemap's own
   README, which is one tap away, tells them to `cargo install --git` it. A visitor who does that and points it at a
   site with no robots.txt gets an empty file. This page already has a rule for that case: the cargo line isn't printed
   until P1 and P2 are at HEAD (`routes.rustmapper.gates.cargo`, which fails today). M1 is the same recommendation
   with the gate left off. Honest data only.

2. **The release is still the loudest thing on my profile, and its fix is still mine to make.** This is the third
   round I've said it. The red dotted box reads "0.1.3 never stops by itself". It's true, and naming the release was
   the right fix in this repository. But a warning every visitor sees on every visit stops being read [S2, S3], and
   this one is about an 11-month-old build. PyPI still says 0.1.3, 8 Nov 2025 (checked today). Rust-sitemap's About
   text still says "goes until it reaches end points", and `README.md:25` still says pip "installs the **Python
   library**" (both checked today). That's a click-through that contradicts the image. One new point makes the
   release smaller than I thought. If P1 is fixed and `--ignore-robots` comes out of `crawl_exits_when_idle.rs`, that
   one test proves both fixes, because its fixture already serves a 404 robots.txt. When 0.1.4 passes the run check,
   the red box, the gap, M1, the kill comment and X1 all retire, with no edit here.

3. **The hand-off label doesn't say what you get.** The desk reads "sorted by ideal-url-organizer:
   `scripts/import_rust_sitemapper.py`, with a test". The phone reads "sorted by ideal-url-organizer, with a test".
   "With a test" attaches to "sorted", so it reads as if the sorting needs a test. That's the ambiguous-modifier problem
   style guides warn about [S4]. The path is a lookup that nobody reading a profile needs. What a stranger wants to
   know is what the next project does with the file, and that's in the code: the reader runs the organizer's whole
   pipeline (`import_rust_sitemapper.py:131-143`, `run.sh --all`), and there are 25 sorts (`figures[]` "25 ways", 25
   `method_*.py` files, `holds: true`). The test stays as the gate, so the line is still drawn only when the join is
   proven. It just doesn't need to be printed.

4. **Small wording, the kind I called "fucking weird" before.**
   - F1 "queues links on your URL's domain, above or below it". "Above or below" is the code's view of a domain
     (`is_same_domain`, both branches). Say what it means.
   - Rule 4's cite, "ideal-url-organizer, Nov 2025; Claude's commit used it first." It's honest, but a working rule
     backed by someone else's commit isn't evidence of how I work. `chart.toml:146` records my own first
     `urllib.parse` commit on 13 Nov 2025. I couldn't re-check that, because the clone is shallow and the API isn't
     enabled for this repository. Cite my commit, or cut the rule.
   - rustmapper is described three times in one phone screen: the image's header, the pick sentence, and "is a
     concurrent sitemap crawler written in Rust". The third says nothing the facts line ("16k lines of Rust") and the
     image don't already say.

## Figures checked

| Printed | Source | Value | Holds |
|---|---|---|---|
| pip install rustmapper · 0.1.3 · 8 NOV 2025 | `edition`; PyPI JSON today | 0.1.3; four uploads, all 8 Nov 2025; latest still 0.1.3 | yes |
| your URL, plus by default sitemaps, certificate logs, Common Crawl | sdist `cli.rs:58` `default_value = "all"`; `ct_log_seeder.rs:179` crt.sh; `common_crawl_seeder.rs:185` | | yes |
| fetches a page; queues links on your URL's domain, above or below it | sdist `url_utils.rs:81-91` | parent and subdomains, not siblings | yes (wording, finding 4) |
| fetches fewer pages at once when saves average over 500 ms | sdist `main.rs:90,113` `THROTTLE_THRESHOLD_MS = 500.0` vs commit EWMA | | yes |
| logged to disk, then saved to redb, every 50 ms | sdist `writer_thread.rs:11` `BATCH_TIMEOUT_MS = 50`; order checked in round 5 | | yes |
| 0.1.3 never stops by itself; done when `Received work item` lines stop | sdist `bfs_crawler.rs:433`; runcheck `ends_by_itself` false (150 s), `quiet_after_last_page` ok | | yes |
| press Ctrl-C once to write `data/sitemap.jsonl` | sdist `main.rs:519,535`; runcheck `crawl_ctrl_c` ok, 2.0 s, 3 lines | | yes |
| fields: url, depth, status_code, title, … | `SitemapNode`, both trees; `handoffs[0].writer_fields_*` | | yes |
| sorted by ideal-url-organizer … with a test | `handoffs[0]` `state: runs`, `does: sorted by`, 15 reader fields within both writer sets | | yes (wording, finding 3) |
| On main at `32c2651` · 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust | `repos[Rust-sitemap]` | 176; success at `head_sha` = `head.sha`; 16,390 | yes |
| On main at `96e7a1a` · 1,920 tests · CI passed 8 Oct 2026 · MIT · 69k lines of Python | `repos[Scrapy]` | 1,920; success; MIT; 69,036 | yes |
| Prebuilt for Apple silicon on CPython 3.13; 3 min cold on 4-core Linux | `edition.wheels`; runcheck `install` | `cp313-cp313-macosx_11_0_arm64` only; median 171.4 s | yes |
| 20 per host, 256 in all, no pause unless `Crawl-delay` | sdist `state.rs:285` `max_inflight: 20`; `cli.rs:31` `"256"` | | yes |
| 0.1.3 writes one `sitemap.xml`; the format allows 50,000 URLs per file | no index writer in the sdist; sitemaps.org "no more than 50,000 URLs" | | yes |
| On main, a crawl stops by itself … `crawl_exits_when_idle.rs` passes in CI | test file `:54`, `:67` | **passes only with `--ignore-robots`**; main fetches nothing from a 404-robots site | **misleading** (finding 1) |
| 45 of rustmapper's 146; 71 of Scrapy's 499 | `repos[].others`, `all_hands` | Claude 45 / 146; jules 49 + Claude 22 = 71 / 499 | yes |
| 15 more | `repo_count` 22 − profile − 2 flagships − 4 Also | 15 | yes |
| go_go_go "same crawl, resume and export-sitemap commands" | go_go_go `internal/cli/resume.go:14`, `export.go:21` | true of the command names. 0.1.3's own `resume` fails ("Database already open", runcheck `resume_after_kill`), but the line doesn't claim it works | yes |
| (click-through) Rust-sitemap About text; `README.md:25` | GitHub API today; clone | "goes until it reaches end points"; "installs the Python library" | **no** (finding 2, owner) |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page | keep | the first thing read |
| Role line, two caps lines | crawl and data infrastructure, Python and Rust | keep | the drawing under it proves both |
| Empty left column under the role line (desk) | nothing | keep | white space. I asked for less density. Filling it would be chasing a reason |
| "rustmapper" + "Crawls a site and writes one line for every page it reaches." | which project, and what it does | keep | the best sentence on the page |
| Start bar | where you begin | keep | the route's fixed entrance |
| `pip install rustmapper` | the way in | keep | the image's one command |
| "0.1.3 · 8 NOV 2025" beside it | how old the build you'd install is | keep | fixed last round. It reads as the release's date now |
| Magenta track | one way through, read top to bottom | keep | the colour a chartplotter uses for the route [S1]. A straight line keeps "visual tracking" unbroken [S8] |
| Stop rings, painted over the track | one step the tool takes | keep | fixed last round |
| S1 seeds | URLs come from more than links, and by default it calls outside services | keep | a fact a stranger should know before running it on their own site |
| F1 fetch / queue | it's a crawler loop, and its scope | change | "above or below it" is code-speak (finding 4) |
| G1 governor | it slows down when saving falls behind, at a measured 500 ms | keep | the one design idea that's mine and unusual |
| W1 write path | it logs, then saves, every 50 ms | keep | the data-infrastructure signal |
| Loop bracket and up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Gap in the track under the loop | the loop has no exit but Ctrl-C | keep | most people won't notice it. A closed line would claim an exit that 0.1.3 doesn't have. It closes by itself when a release ends on its own |
| H1, red dotted box | the catch in this release, and how to tell when you're done | keep the mark, retire the bug | true of 0.1.3, so it stays until 0.1.4 (finding 2, owner) |
| C1 "press Ctrl-C once to write `data/sitemap.jsonl`" | the one thing you do | keep | one line now. Naming the file again right above the end row is fine: it says what the press produces |
| End bar | where you end up | keep | |
| `data/sitemap.jsonl` + fields | what you get, in the struct's own words | keep | |
| Hand-off line and arrow | my projects feed each other | keep | the only cross-project fact, and it's proven |
| Hand-off label | (today) which script reads it, and that the join "has a test" | change | say what you get: "sorted 25 ways by ideal-url-organizer" (finding 3) |
| Night editions | the same | keep | contrast holds. The red box is readable as salmon on navy |
| Phone editions | the same, in one screen | keep | the cleanest edition, and the desk matches it now |
| Link around the image | a tap lands on the project | keep | fix what it lands on (owner, finding 2) |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image | above | change | must-fix 3 and 4 |
| Alt text | the route in 25 words | keep | |
| Link line | where to go | keep | |
| Builds / Languages / Stack | what I build, and with what | keep | |
| Pick sentence | which tool for which job | keep | fixed last round |
| rustmapper sentence | the API isn't released | change | drop the third description (must-fix 5) |
| rustmapper facts line | alive, tested, size, snapshot | keep | |
| Install block | how to run and stop it, and how to recover after a kill | keep | |
| Wheel note | when pip just works | keep | a README should state status [S7] |
| Load note + 50,000 sentence | what it does to someone's server, and the sitemap limit | keep | both true and both useful to a stranger |
| M1 "On main, a crawl stops by itself …" | (claims) main is fixed | cut while the cargo gate fails | it recommends a build that fetches nothing from a site with no robots.txt (must-fix 1) |
| Scrapy sentence, facts, block, Grafana note, bullets | the second tool, measured, and how to start it | keep | |
| Also | the next four | keep | |
| 15 more | the rest | keep | |
| Working rules 1–3 | how I work, each tied to a dated commit | keep | |
| Working rule 4 | as above, but the cite says Claude did it first | change | cite my own commit or cut the rule (must-fix 6) |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn, and agent authorship | keep | fixed last round |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **Don't print M1 while the cargo gate fails** (`chart.toml:553-567`, the M1 entry; `scripts/render_readme.py`
   `text_entries`, around line 497-518; about 6 lines and two tests).
   - Give M1 the key `gate = "cargo"`. In `text_entries`, skip any entry whose `gate` names a
     `routes.rustmapper.gates[...]` record with `ok` false. Today `gates.cargo` is false (P1's and P2's test files are
     missing at HEAD), so M1 isn't printed.
   - Also add a head anchor `{path = "tests/crawl_exits_when_idle.rs", absent = "--ignore-robots"}` under M1's
     `instead` alternative (empty text), so that even once the gate opens, M1 only claims "stops by itself" when the
     test runs with robots checks on. If that anchor fails while the gate holds, the empty alternative is used and
     nothing is dropped silently.
   - Tests: M1 isn't printed with `gates.cargo.ok` false. With the gate true and the fixture test file containing
     `--ignore-robots`, the empty alternative is taken. With both holding, M1 prints as today.
   - The page loses "On main, a crawl stops by itself … That fix is not on PyPI yet." That's about 5 phone lines.
   - Why: the test it cites passes only with `--ignore-robots`. On main, a site whose robots.txt is a 404 is never
     fetched, against RFC 9309 §2.3.1.3 and against how Google reads it [S5]. The page already won't print the cargo
     line for that reason, and M1 shouldn't sneak the same advice back in.

2. **Owner, in Rust-sitemap (mine, not this repository): fix P1, take `--ignore-robots` out of
   `crawl_exits_when_idle.rs`, and ship 0.1.4.** Until then this image doesn't go to `main`.
   - P1 as SPEC §1 states it (4xx means allow, 5xx means disallow and retry, the queued URL's own scheme). Then delete
     line 67 (`"--ignore-robots",`) from the test. Its fixture already serves 404 for `/robots.txt`, so one test then
     proves both #65 and P1.
   - Today, with no release: About text "Crawls a site and writes one line for every page it reaches." and
     `README.md:25` as review r05-1 wrote it. Both are unchanged as of today.
   - Why: a warning every visitor sees on every visit gets tuned out [S2, S3], and this one is about a build that's 11
     months old. Maintenance is judged by recent activity [S6], and pip users only see the release.

3. **The hand-off label says what you get** (`scripts/sheets/route.py:650-662`; `chart.toml:584` `does`; about 10
   lines and a test).
   - Both editions: "sorted 25 ways by ideal-url-organizer", in `label`, `ink2`, one line, with no path and no ", with
     a test". "25 ways" is filled from the `figures[]` row (`text = "25 ways"`, `holds`). If that row doesn't hold, the
     label is "sorted by ideal-url-organizer".
   - The gate doesn't change: R15 is drawn only when `handoffs[0].state` is `runs`, and that still requires the test.
   - Check: STRINGS-TWICE against Also's "25 ways to sort a pile of URLs". The three-word runs differ ("25 ways by"
     and "25 ways to"). PURPOSE row R15: "his projects are one body of work: this output is sorted 25 ways by
     another".
   - Why: "with a test" attaches to "sorted" [S4], and the script path is a lookup. The desk loses about 330 units of
     line.

4. **F1 in plain words** (`chart.toml` F1 text; 1 line).
   - "fetches a page; queues links to your site, its subdomains and its parent domain". Same anchors
     (`is_same_domain`, both branches). On the phone: two lines, as today.
   - Why: "above or below it" is how the code sees a domain, not how a visitor does.

5. **One description of rustmapper per screen** (`render_readme.py`, the `about:Rust-sitemap` block; 1 line).
   - "**[rustmapper](…)**: `pip install` gives you its command line; the Python API, built with maturin, is on main and
     not yet released." Cut "is a concurrent sitemap crawler written in Rust."
   - Why: the image's header, the pick sentence and this sentence all introduce the same tool within one phone
     screen. The facts line already says Rust.

6. **Rule 4 cites my own commit, or goes** (`chart.toml:144-148`; `checks/notices.py`; about 8 lines and a test).
   - Add an `author = "self"` key to the `urlparse` anchor, so `{month:urlparse}` comes from my first commit that
     contains `urllib.parse` (`chart.toml:146` says 13 Nov 2025). Drop "Claude's commit used it first", and set
     NOTICE-AUTHOR to check the author-scoped anchor.
   - If no commit of mine holds it, cut rule 4. Three rules are enough.
   - Why: the cite exists to prove the rule is how I work. Saying the first use was someone else's argues the
     opposite. The agent share is already disclosed honestly in the data line.

## Sources (new this round)

1. [S1] Garmin, GPSMAP 8400/8600 manual, "Route Color Coding": magenta is the "default route/course line"; red
   striped is "Warning! This segment of the route might be unsafe". This is the convention the track and the one red
   mark follow:
   https://www8.garmin.com/manuals/webhelp/gpsmap8400-8600/EN-US/GUID-EC4B1BB4-3F3B-4D52-AC7F-1C71A9E079F1.html
2. [S2] Vance, Jenkins, Anderson, Bjornn, Kirwan, "Tuning Out Security Warnings: A Longitudinal Examination of
   Habituation Through fMRI, Eye Tracking, and Field Experiments", MIS Quarterly 42(2), 2018: attention to repeated
   warnings fell sharply over a week, and warnings that changed resisted it:
   https://misq.org/tuning-out-security-warnings-a-longitudinal-examination-of-habituation-through-fmri-eye-tracking-and-field-experiments.html
3. [S3] Anderson, Vance, Kirwan, Jenkins, Eargle, "From Warning to Wallpaper: Why the Brain Habituates to Security
   Warnings and What Can Be Done About It", JMIS 33(3), 2016: https://jmis-web.org/articles/1304
4. [S4] Google developer documentation style guide, "Write for a global audience": put a modifier right before what it
   modifies, and "if the meaning is still ambiguous, try rephrasing": https://developers.google.com/style/translation
5. [S5] Google Search Central, "How Google interprets the robots.txt specification": "Google's crawlers treat all 4xx
   errors, except 429, as if a valid robots.txt file didn't exist":
   https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt
6. [S6] OpenSSF Scorecard, checks.md, "Maintained": the highest score needs "at least one commit per week during the
   previous 90 days". Activity is measured on the repository, and a pip user sees only the release:
   https://github.com/ossf/scorecard/blob/main/docs/checks.md
7. [S7] Prana, Treude, Thung, Atapattu, Lo, "Categorizing the Content of GitHub README Files", Empirical Software
   Engineering 24(3), 2019: "many README files lack information regarding the purpose and status of a repository":
   https://arxiv.org/abs/1802.06997
8. [S8] Wu, Niedermann, Takahashi, Roberts, Nöllenburg, "A Survey on Transit Map Layout – from Design, Machine, and
   Human Perspectives", Computer Graphics Forum 39(3), 2020: schematic maps exist "to facilitate passengers'
   orientation and navigation", with straight lines so that "visual tracking of users is not disrupted":
   https://pmc.ncbi.nlm.nih.gov/articles/PMC7539984/

Re-checked today (cited before): RFC 9309 §2.3.1.3–4 (https://www.rfc-editor.org/rfc/rfc9309.txt, "the crawler MAY
access any resources"); sitemaps.org protocol ("no more than 50,000 URLs and must be no larger than 50MB").

Clones and APIs: Rust-sitemap `32c2651` `tests/crawl_exits_when_idle.rs:1-110`, `src/robots.rs:19,32`,
`src/frontier.rs:729-795`, `src/cli.rs` (idle defaults 30 s / 60 s), `README.md:25`; sdist 0.1.3 `src/cli.rs:28-62`,
`src/state.rs:275-285`, `src/main.rs:90,113,519,535`, `src/writer_thread.rs:11`, `src/url_utils.rs:81-91`,
`src/bfs_crawler.rs:433`, `src/ct_log_seeder.rs:179`, `src/common_crawl_seeder.rs:111,185`; ideal-url-organizer
`159968a` `scripts/import_rust_sitemapper.py:1-60,131-143`, `README.md` (25+ methods); go_go_go `4078b55`
`internal/cli/resume.go:14`, `export.go:21`; `assets/stats.json` (`edition`, `repos`, `routes.rustmapper` with
`gates`, `handoffs`, `runcheck.rustmapper`, `figures`, `agent_authored`); GitHub API `repos/BenjaminSRussell/Rust-sitemap`
(description, pushed 7 Oct) and `/commits` (`32c2651` newest); PyPI JSON `rustmapper` (0.1.3 latest).
