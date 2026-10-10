# Review round 4, reviewer 1: Ben, the owner

10 Oct 2026. Build looked at: `scratchpad/r6/build/round-03/`: the desk sheet (870) and the phone sheet (390), day and
night; the whole page on desk (screens 1 and 2) and on phone (screens 1 to 5). Read: `README.md`, `SPEC.md`, `LOG.md`
(round-3 fixes), and the nine reviews from rounds 1 to 3. I don't repeat anything that was fixed. Every figure was
checked against `assets/stats.json`, the 0.1.3 sdist, the Rust-sitemap clone at `32c2651`, and the GitHub and PyPI APIs
today.

Verdict: **not yet. 7 / 10.** Up from 6. I would not ship it as it is.

## The first question: does it meet my goal?

On form, yes. I asked "what is it showing, and how does it help someone see my project?" Now the answer is plain. It
shows how you start my crawler, what it does with each page, the one loop it never leaves, how you stop it, what file
you get, and which of my other projects reads that file. Nothing has a size. No word names the theme. The magenta line
you follow and the dotted danger line are things a chart does without saying so. It reads on the phone. This is the
first picture on this profile that teaches something true about my work that you couldn't get faster from the text:
the order of things and where the trap sits in that order. I'm not going back to islands, and I'm not asking for a new
concept.

What still stops me shipping it:

1. **The loudest thing on my profile is a bug I fixed three days ago.** The only red on the page is "never stops by
   itself, even after the last page". It's true of 0.1.3, the only thing `pip` gives you. It's no longer true of the
   project: main fixed it in `d751cf0` (closes #65, 7 Oct), and resume after a kill in `aaa38d6` (#63). Count the 0.1.3
   caveats a visitor reads before they reach Scrapy. The trap, the kill clause, the wheel note, and "0.1.3 writes one
   `sitemap.xml` however many pages it found". Four warnings about an 11-month-old alpha. What a visitor actually
   learns is "his flagship's release is old and broken and he hasn't shipped the fix." The drawing is honest, so the
   drawing isn't what's wrong. My release is. The build also says so: `check.py --tier fast` fails ROUTE-UNVERIFIED on
   S2, because P1 (robots.txt 4xx means "allow all") isn't on main. So this doesn't pass its own gate today. Earlier
   rounds put this down as "owner action, declined". I'm the owner and I'm taking it. It's must-fix 1, with what it
   actually takes. While checking, I found that a 0.1.4 cut from main as it stands would **fail to build**. Main's
   `pyproject.toml` names `license-files = ["LICENSE"]`, there is no LICENSE file in the tree (GitHub API 404 at
   `32c2651`), and PEP 639 says a build tool "MUST raise an error if any individual user-specified pattern does not
   match at least one file". Even if it built, `bindings = "pyo3"` with no `[project.scripts]` would ship no command at
   all.

2. **The code block people copy never tells them how to stop it.** The image says "press Ctrl-C once". The block under
   it, the thing a visitor actually pastes, is `pip install` / `crawl` / `export-sitemap`, with no word about stopping.
   Paste it and `crawl` runs forever. When they press Ctrl-C, the terminal flushes the rest of what they pasted (with
   NOFLSH unset, INTR flushes the input queue: termios(3)), so the `export-sitemap` line never runs. The CLI
   guidelines are blunt about it: "Tell the user what will happen when they hit Ctrl-C again" and "If your program
   displays no output for a while, it will look broken". Round 1 (r01-3) asked for this comment and it never landed.
   The block also spells out two flags that are the defaults (`export-sitemap` defaults to `./data` and
   `./sitemap.xml`: `sdist:src/cli.rs:131-143`), which costs two phone lines for nothing.

3. **The desk rows don't line up.** "your URL…", "fetches a page…" and "saved every 50 ms" each start at a different x
   (≈549, 567 and 585 px on screen), and "fields:" starts at a fourth. The cause is `route.py:480`:
   `rx = max(rule_x, TX + width(file) + 20)` is worked out per row. On a list a stranger reads top to bottom, a ragged
   left edge reads as sloppy. Penzo's form study (as usability.gov summarises it) found that a hard left edge lets
   readers predict where the next label is, and a jagged edge makes the form harder to scan. The phone has no file
   labels and is clean. The desk's empty left column, under the role line, is the place for them.

4. **The AI sentence qualifies a count the page no longer shows.** "297 more were written by coding agents … and are
   not counted as his". Not counted in what? Since the islands went, no figure on the page counts my commits. The
   figures it does show are tests and lines per repository, and those include agent-written code. The honest version
   attaches the disclosure to the numbers it qualifies. 45 of Rust-sitemap's 146 commits are authored by Claude
   (`repos[Rust-sitemap].others`, `all_hands` 146). 71 of Scrapy's 499 are by agents (jules 49, Claude 22), plus
   dependabot's 8.

5. **The licence line is a "how this was built" footer.** "The image is rustmapper's route in `chart.toml`
   (`[route.rustmapper]`, each line with the code it rests on); the build draws only the lines that code and its run
   check prove · how it's built → DESIGN.md". That is a generated-by footer, which I ruled out, and it repeats what the
   data line already says. On the phone it's six lines of small print at the bottom of my profile, and it says
   "chart".

6. **"From one command" isn't true.** The pick sentence says "For the list of a site's URLs from one command,
   **rustmapper**". It takes `crawl`, a Ctrl-C, and `export-sitemap` if you want XML. The real difference from Scrapy
   is that rustmapper needs no services. Scrapy needs Docker, Redis and PostgreSQL.

## Figures checked

| Printed | Source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.uploads[3].time`; PyPI JSON today | 0.1.3, 2025-11-08T19:52:41; latest still 0.1.3 | yes |
| pip install rustmapper → `rust_sitemap` | `edition.scripts`; runcheck `help`, `crawl_help` ok | `["rust_sitemap"]` | yes |
| your URL, plus by default sitemaps, certificate logs, Common Crawl | `sdist:src/cli.rs:58` | `default_value = "all"` | yes |
| fetches a page; queues links on its domain, above or below it | `routes` F1 both trees | verified | yes |
| fetches fewer pages at once when saving falls behind | `routes` G1 (`governor.rs` / sdist `main.rs`) | verified | yes |
| saved every 50 ms | `sdist:src/writer_thread.rs:11` | `BATCH_TIMEOUT_MS: u64 = 50` | yes |
| never stops by itself, even after the last page | runcheck `ends_by_itself`; `sdist:src/bfs_crawler.rs:548-553` (`else =>` arm) | still running at 150 s on 3 pages | yes for 0.1.3; fixed on main `d751cf0` |
| press Ctrl-C once to write `data/sitemap.jsonl`; after a kill, run `export-sitemap` | `crawl_ctrl_c` ok (2.0 s), `kill_writes_file` false, `export_after_kill` 3 `<loc>`; `sdist:src/main.rs:519, 535` | | yes |
| fields: url, depth, status_code, title, … | `SitemapNode`, both trees | | yes |
| read by ideal-url-organizer … with a test | `handoffs[0]` | 15 reader fields ⊆ writer, both trees; test at `159968a` | yes |
| 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust · `32c2651` | `repos[Rust-sitemap]` | 176; success 2026-10-07 (7 jobs); 16,390; head `32c2651` | yes |
| 1,920 tests · CI passed 8 Oct 2026 · MIT license · 69k lines of Python · `96e7a1a` | `repos[Scrapy]` | 1,920; success 2026-10-08; MIT; 69,036 | yes |
| Prebuilt for Apple silicon on CPython 3.13 | `edition.wheels` | `cp313-cp313-macosx_11_0_arm64` only | yes |
| 3 min from a cold cache on a 4-core Linux x86_64 machine | runcheck `install` | 168.2 / 171.4 / 174.3 s, cold, 4 CPUs | yes |
| up to 20 requests at a time to one host, 256 in all, no pause unless `Crawl-delay` | `sdist:src/state.rs:281, 285`; `cli.rs:32` | `crawl_delay_secs: 0`, `max_inflight: 20`, `256` | yes |
| 50,000 URLs per file | `routes` X1 (main's `DEFAULT_MAX_URLS_PER_SITEMAP`) | verified | yes |
| 25 ways; stage 3; stage 4; 50,000 characters; localhost:3000 | `figures[]` | all `holds: true` | yes |
| 22 public repositories; 15 more | `repo_count`; 22 − 1 − 2 − 4 | 22; 15 | yes |
| 3 % AI co-author trailer; 297 by agents | `coauthored_total.agent_share`; `agent_authored.total` | 0.031 (63 / 2,032); 297 (Claude 172, jules 125) | yes, but it qualifies nothing shown (finding 4) |
| (implied by the install block) the commands complete as pasted | runcheck `ends_by_itself` false | crawl never returns | **no** (finding 2) |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page | keep | |
| Role line, two caps lines | crawl and data infrastructure, Python and Rust | keep | the drawing under it proves both words |
| Empty desk left column under the role | nothing | change | it's where the file labels go (must-fix 3) |
| "rustmapper" + "Crawls a site and writes one line for every page it reaches." | which project, what it does | keep | the best line on the page |
| Start bar | where you begin | keep | |
| `pip install rustmapper` | the way in | keep | |
| "0.1.3 · 8 NOV 2025" | how old the thing you'd install is | keep | true and needed; it reads 2026 once 0.1.4 ships (must-fix 1) |
| Magenta track | one way through, read top to bottom | keep | |
| Stop rings | a step the tool takes | keep | |
| S1 "your URL, plus by default sitemaps, certificate logs, Common Crawl" | URLs come from more than links, and by default it calls outside services | keep | |
| F1 "fetches a page; queues links on its domain, above or below it" | it's a crawler loop, and its scope | keep | |
| Governor tick + "fetches fewer pages at once when saving falls behind" | it throttles itself to its store | keep | the one design idea that is mine and unusual |
| W1 "saved every 50 ms" | it saves as it goes | keep | it's why "after a kill, run export-sitemap" works |
| Desk file labels (`seeder.rs`, `bfs_crawler.rs`, `writer_thread.rs`) | which file to open to check each step | change | true and useful to an engineer, but they push each rule to a different x (must-fix 3) |
| Loop bracket with up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Gap in the track below the loop | the loop has no exit but Ctrl-C | keep | it closes by itself when a release ends on its own |
| H1 in the dotted danger line | the catch | keep the mark, retire the bug | true of 0.1.3; must-fix 1 takes it off the page the right way |
| C1 "press Ctrl-C once to write `data/sitemap.jsonl`; after a kill, run `export-sitemap`" | the one thing you do, and the way back from a kill | keep | |
| End bar | where you end up | keep | |
| `data/sitemap.jsonl` + fields | what you get, in the struct's own words | keep | |
| Hand-off arrow + "read by ideal-url-organizer …, with a test" | my projects feed each other, and the join is tested | keep | |
| Night editions | the same | keep | contrast holds; nothing muddy |
| Phone edition | the same, without file labels | keep | the cleanest edition; the desk should match its left edge |
| Link round the image to Rust-sitemap | a tap lands on the project | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image | above | change | must-fix 3 |
| Alt text | the same in 25 words | keep | right now; rebuilt from `routes` after 0.1.4 |
| Link line `rustmapper · Scrapy · PyPI · Email` | where to go | keep | |
| Builds / Languages / Stack | what I build and with what | keep | |
| Pick sentence | which tool for which job | change | "from one command" is false (must-fix 6) |
| rustmapper sentence | what it is; the API isn't released | keep | |
| rustmapper facts line | alive, tested, size, which snapshot | keep | |
| Install code block | how to run it | change | no stop instruction; default flags (must-fix 2) |
| Wheel note | when pip just works | keep | |
| Load and 50,000 note | what it does to someone's server; the sitemap limit | keep | the load sentence is what a polite user needs; the 50,000 clause retires with a release that splits |
| Scrapy sentence, facts line | the second tool, measured | keep | |
| Scrapy code block | how to start it | keep | five comment lines is a lot, but each one prevents a real failure |
| Grafana note | where to look once it runs | keep | |
| Scrapy bullets | how it's built | keep | dense, but each one is a design fact |
| Also | the next four | keep | |
| 15 more | the rest | keep | |
| Working rules | how I work, each with a dated commit | keep | |
| Found a mistake? | the page can be corrected | keep | |
| Data line | what was checked and run | change | the AI clause (must-fix 4) |
| Licence line | the profile's terms | change | cut the build sentence (must-fix 5) |

## Must fix, ranked

1. **Ship rustmapper 0.1.4 from main, so the profile stops advertising fixed bugs** (in Rust-sitemap; owner, me;
   about a day). (a) P1: in `src/robots.rs`, `fetch_robots_txt` and `fetch_robots_txt_from_url` return "allow all"
   for any 4xx except 429. This follows RFC 9309 §2.3.1.3 and Google's crawlers, which "treat all 4xx errors, except
   429, as if a valid robots.txt file didn't exist". A 5xx or an unreachable server stays fail-closed with a retry.
   The 4xx answer has to be a value that `frontier.rs:830`'s "fresh timestamp but empty body" branch doesn't treat as
   first contact. Build the URL with `url_utils::robots_url`, so http sites aren't asked over https. Add
   `tests/robots_4xx_allows_crawl.rs`, the HEAD anchor S2 already waits for. (b) Commit the MIT `LICENSE` that
   `pyproject.toml`'s `license-files` names. Without it, maturin refuses to build under PEP 639. (c) Give pip a
   command again: add a `[project.scripts]` entry, `rustmapper = "rustmapper:main"`, whose `main` calls the native
   crawler. That's what maturin's guide recommends for pyo3 projects ("Shipping both a binary and library would
   double the size of your wheel"). (d) Build wheels for Linux x86_64 and aarch64, macOS arm64 and Windows x86_64 in a
   tag-triggered release workflow (`maturin-action`), then publish 0.1.4. Nothing changes in this repository: H1
   retires once `ends_by_itself` passes, the gap closes, C1 drops its kill clause once `kill_writes_file` passes, X1
   retires once the sdist has `SitemapIndexWriter`, the wheel note shrinks, the date reads 2026, S2 is drawn, and
   ROUTE-UNVERIFIED goes green. Why: the image's one red mark and three README caveats describe a release, not the
   project. Main fixed them, and a visitor can't tell. Until 0.1.4 passes the run check, this image doesn't go to
   `main`.

2. **Put the stop in the code block people paste** (`render_readme.py`, `install:Rust-sitemap`; about 15 lines and a
   test). The new block:
   ```
   pip install rustmapper
   rust_sitemap crawl \
       --start-url <your-site>
   # stop it with one Ctrl-C
   rust_sitemap export-sitemap
   ```
   The comment line is printed only while `ends_by_itself` fails and `crawl_ctrl_c` passes. Once a release ends by
   itself, it becomes nothing. The `--data-dir ./data` and `--output sitemap.xml` flags go, because they're the
   defaults (`sdist:src/cli.rs:131-143`, value-anchored like L1 so they come back if a release changes them). One
   comment line, "# writes ./sitemap.xml", may follow the export command if README-CODE-WIDTH allows (≤ 38
   columns). The block goes from 6 lines to 5 on the phone. STRINGS-TWICE / HERO-SELF-TWICE allow it: the image says
   "press Ctrl-C once to write …", a different run of words. Why: the thing people copy should say how it ends. A
   pasted block can't recover from a Ctrl-C, because the terminal discards the rest of the paste.

3. **One left edge for the desk rules; file labels in the empty left column** (`scripts/sheets/route.py:476-480`,
   desk only; about 20 lines and a test). Set every stop and note rule at `TX` (x 484), as the phone does. Draw each
   file label in `machine` 19 `muted`, right-aligned to x 424, on the rule's baseline, clear of the loop bracket
   (which starts at about x 441). Add a bounds rule: no file label may cross the role line's box or the bracket. New
   render check ROUTE-LEFT-EDGE: every drawn rule in an edition starts at the same x. If a label can't fit
   (measured with `typeset`, as everything else is), drop all desk file labels rather than some, and change the data
   line's "every rustmapper source file it names" to "every step it shows" in the same commit. Why: a list read top to
   bottom needs one left edge. Today it has four, and they look like a rendering bug. The left column is empty paper
   that can hold the labels.

4. **Attach the AI disclosure to the numbers it qualifies** (`render_readme.py`, `survey` marker; about 15 lines,
   one AUDIT row, a test). Replace "3 % of Ben's commits carry an AI co-author trailer; 297 more were written by coding
   agents (Claude, jules) and are not counted as his." with: "Tests and lines are counted per repository, whoever
   wrote them: coding agents (Claude, jules) authored 45 of rustmapper's 146 commits and 71 of Scrapy's 499." Compute
   it from `repos[].others`, where `name` is in `[identity] bots` / `agent_authored.names` (automation like
   dependabot excluded), over `repos[].all_hands`. The sentence prints for the repositories that have a facts line.
   Why: the old sentence answers a commit count that left with the islands. The new one is the honest footnote to the
   test and line counts that are actually printed.

5. **Cut the build-description sentence from the licence line** (`chart.toml` / `render_readme.py`, `license`
   marker; 2 lines). Leave: "**This profile** Code MIT; images and text CC BY 4.0; fonts under their own licenses in
   `scripts/fonts/`." Remove "The image is rustmapper's route in `chart.toml` … run check prove · how it's built →
   DESIGN.md". If DESIGN.md must stay reachable, link it from the word "drawing" in the data line. Why: it's a "how
   this was generated" footer, which the standing rules ban. It repeats the data line, and it puts "chart" in front of
   the visitor.

6. **Make the pick sentence true** (`chart.toml [copy] pick`; one line). "For the list of a site's URLs, from one
   binary with no services to run, **rustmapper**; to keep the pages themselves, deduplicated and summarised, in a
   pipeline that needs Docker, **Scrapy**." Anchor "no services" on the release's `enable_redis` being an opt-in flag
   (`sdist:src/cli.rs:63-64`, `#[arg(long …)] enable_redis: bool`). Why: it takes three steps, not one command, and
   the image says so two inches above.

## Sources (new this round)

1. Command Line Interface Guidelines, "Signals and control characters" and "Robustness": https://clig.dev/
2. Semantic Versioning 2.0.0, item 4 and the 1.0.0 FAQ ("Major version zero (0.y.z) is for initial development"):
   https://semver.org/
3. maturin user guide, "Bindings" (`bin` vs `pyo3`; a console-script entry point instead of shipping a binary):
   https://www.maturin.rs/bindings.html
4. Python Packaging User Guide, "Writing your pyproject.toml", `[project.scripts]`:
   https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
5. PEP 639, `license-files`: tools "MUST raise an error if any individual user-specified pattern does not match at
   least one file": https://peps.python.org/pep-0639/
6. Google Search Central, "How Google interprets the robots.txt specification" (4xx except 429 = no robots.txt; 5xx
   handling): https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt
7. termios(3), NOFLSH (INTR flushes the input queue unless it is set): https://man7.org/linux/man-pages/man3/termios.3.html
8. The Twelve-Factor App, IX "Disposability" (shut down gracefully on SIGTERM; be robust against sudden death):
   https://12factor.net/disposability
9. GitHub Open Source Survey 2017: "Incomplete or outdated documentation is a pervasive problem, observed by 93% of
   respondents": https://opensourcesurvey.org/2017/
10. Google developer documentation style guide, "Code samples" (comments in the sample's own syntax; wrap for narrow
    windows): https://developers.google.com/style/code-samples
11. Prana, Treude, Thung, Atapattu, Lo, "Categorizing the Content of GitHub README Files", Empirical Software
    Engineering 24(3), 2019: "What" and "How" are common, and purpose and *status* are often missing:
    https://arxiv.org/abs/1802.06997
12. usability.gov newsletter (Apr 2008), summarising Penzo's eye-tracking study of form label alignment: a hard left
    edge lets users predict where the next label is: https://cybercemetery.unt.edu/oilspill/20120928045207mp_/http://www.usability.gov/newsletter/pubs/042008news.html
13. Ladders 2018 eye-tracking study as reported by HR Dive (7.4 s initial screen; clear sections did better, clutter
    worse): https://www.hrdive.com/news/eye-tracking-study-shows-recruiters-look-at-resumes-for-7-seconds/541582/

Clones and APIs: Rust-sitemap `32c2651` (`pyproject.toml`, `src/robots.rs:15-34`, `src/frontier.rs:746, 781, 830`,
no `LICENSE` in the tree); GitHub REST `repos/BenjaminSRussell/Rust-sitemap/commits` (`d751cf0`, `aaa38d6`, 7 Oct
2026) and `/contents/LICENSE` (404); PyPI JSON `rustmapper` (latest 0.1.3); sdist 0.1.3 `src/cli.rs`, `src/main.rs`,
`src/state.rs`, `src/writer_thread.rs`, `src/bfs_crawler.rs`; `scripts/sheets/route.py:476-480`.
