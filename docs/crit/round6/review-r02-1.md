# Review round 2, reviewer 1: the owner's test

10 Oct 2026. Build looked at: `scratchpad/r6/build/round-01/` (desk and phone sheets, day and night; the whole page,
desk screens 1 and 2 and phone screens 1 to 5; `once-p1-lands/`). Read: `README.md`, `SPEC.md`, `DECISIONS.md`,
`LOG.md` and the three round-1 reviews. Findings already fixed in round 1 are not repeated.

Verdict: **does not meet the goal. 5 / 10.** I would not ship it as is.

## The first question: does it meet my goal?

What round 1 fixed, and fixed well:

- The crawler is drawn as a loop now. Fetch, the links go back, round again. A list can't show that, so for the first
  time the drawing carries something the words don't. Strip the line and you lose which rows repeat.
- The traps are one hazard with its way out ("never ends by itself" → "press Ctrl-C once").
- "Resume" is gone because it fails in 0.1.3. The run check proves what the drawing says, not just that a string
  exists in a file. That's the honest data rule actually being enforced.
- The left column lost the sha and the "as of". Nothing names the theme. Nothing has a size.

Where it still fails me:

1. **The picture's loudest news is that my main project is broken, and I fixed it last week.** Read the image the
   way a stranger does: "never ends by itself", "a second press, or a kill, quits without it", plus a 3-minute
   compile. That describes 0.1.3, eleven months old. On `main` I closed #65 (never exits) and #63 (resume lock) on
   7 Oct, and there are 22 merged pull requests and 55 commits since the release (GitHub API). The image is true
   and it's the worst true thing it could say. A profile is where a recruiter or engineer decides in about ten
   seconds whether to look further (NN/g). Recruiters read a profile for signs the work is good, and this one
   advertises a hang. The judges already said not to put a packaging bug on the profile but to fix it at the
   source (SPEC P4). The same goes for this bug, and it's fixed already; it just isn't released. The highest-value
   change to this image isn't in this repository. It's landing P1 and cutting 0.1.4.

2. **It's still a README drawn as a picture, and the README repeats it.** Round 1 asked for one home per fact. The
   new STRINGS-TWICE gate only catches runs of five words, so the short repeats got through. `pip install rustmapper`
   and `rust_sitemap crawl --start-url` sit in the image and again in the code block one phone screen down. "CI on
   main passed 7 Oct 2026" is in the image and again in the facts line. The gate passes and I still read the same
   things twice. That's passing the check without meeting what it was for. Of the image's 13 lines on phone, the
   loop is the only thing a picture has to do. The rest is small grey text that can't be copied, zoomed or
   searched.

3. **One line says something false about why it works.** "logged before stored: after a kill, export-sitemap still
   writes sitemap.xml". The colon says the log is why export survives a kill. It isn't. `export-sitemap` never reads
   the log. It opens the redb store ("Export only needs the stored state", `sdist:src/main.rs:396`). The log is only
   replayed when you start the crawler (`build_crawler`, `:197-250`). Export survives a kill because the writer
   commits to redb every 50 ms (`writer_thread.rs:11`, `BATCH_TIMEOUT_MS = 50`, same at HEAD). Both halves are true
   and the "because" between them is wrong. That's "the data doesn't look exactly accurate" again, in one colon.

4. **It's too dense and too long on the phone.** The phone sheet is 1155 × 720, so 624 px tall at 390, about a full
   iPhone screen of 14 px grey text before the link line. On the desk it's 13 lines at about 13 px, smaller than
   the 16 px README text under it. "It's too dense in certain areas" was my first complaint, and this is the
   densest image yet. Every line has the same weight, so nothing reads first. The one thing a stranger must not
   miss, the hazard, gets a hatch 18 units wide in the far-left gutter, the least-read spot on the sheet.

5. **The theme has gone entirely.** "Telling you about me, with a layer of a theme of shipping, in a cool format."
   The only trace left is the magenta line, and no visitor reads that as anything. It looks like a man page with a
   pink rail. I don't want ships back. I want the one real chart habit that also does the job: a danger is the
   thing on a chart you can't miss. Draw the hazard like that (must-fix 5) and the theme and the purpose are the
   same mark.

So the form now has one real reason (the loop) and the content is honest. But it puts my worst release first,
repeats the text, makes one false causal claim, and on the phone it's a screen of fine print. Not a deep purpose
yet. It's a correct how-to for the wrong version.

## Figures checked (stats.json, the clones, the 0.1.3 sdist, the GitHub API)

| Printed | Key / source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.date`, `.uploads` | 0.1.3, 2025-11-08T19:52:41 | yes |
| 3 min on Linux x86_64: pip builds it from source | `runcheck.rustmapper.steps[install].secs`, `.runner` | 179.8 s, Linux x86_64, "sdist (built with Rust)" | yes, but the runner already has Rust installed; the line leaves out that you need it (must-fix 6) |
| `rust_sitemap crawl --start-url` | `edition.scripts` | `["rust_sitemap"]` | yes |
| RUSTMAPPER · 1 OF 21 | `repo_count` | 21 | yes |
| CI ON MAIN PASSED 7 OCT 2026 | `repos[Rust-sitemap].ci` | success, 2026-10-07, last 5 success | yes |
| by default also seeds from sitemaps, CT logs, Common Crawl | `sdist:src/cli.rs:58` | `default_value = "all"` | yes (release scope) |
| fetch a page; same-site links go back | routes F1, probe `crawl_ctrl_c` | verified both | yes |
| fewer requests in flight when redb commits slow down | routes G1 | verified both | yes |
| logged before stored: after a kill, export-sitemap still writes sitemap.xml | routes W1, probe `export_after_kill` 3 `<loc>` | both halves true; the causal link is false (`sdist:src/main.rs:387-397` reads redb only) | **no, as worded** |
| never ends by itself: no page or depth limit, parent domain same-site | routes H1, probe `ends_by_itself` false at 150 s; `url_utils.rs:81-91` | yes for 0.1.3. At HEAD `--max-urls` exists (`src/cli.rs:82`) and #65 is fixed | yes (release) |
| Ctrl-C once writes; a second press or a kill quits without it | probes `crawl_ctrl_c` ok, `kill_writes_file` false | yes for 0.1.3. At HEAD the kill half is checked by strings only (`shutdown.rs` handles only `ctrl_c`, so it holds) | yes |
| one line per page: url, depth, status_code, title | routes R13 | verified both | yes |
| read by ideal-url-organizer, with a test | `handoffs[0].state` `runs`; `tests/test_import_rust_sitemapper.py` | 6 tests | yes |
| 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust | `test_functions` 176, `lines.Rust` 16,390 | | yes, at HEAD |
| 1,920 tests · CI passed 8 Oct 2026 · 69k lines | Scrapy `test_functions`, `ci`, `lines.Python` 69,036 | | yes |
| measured 10 Oct 2026; run 9 Oct 2026 | `taken`; `runcheck.date` | 2026-10-10; 2026-10-09 | yes |
| 3 %; 297 | `coauthored_total.agent_share` 0.031; `agent_authored.total` 297 | | yes |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| Ben Russell | whose page | keep | |
| Role line | crawlers and data infrastructure, Python and Rust | keep | the drawing proves it |
| "RUSTMAPPER · 1 OF 21" | that one project of 21 was picked | cut | "rustmapper" is set in serif three lines below it on phone and beside it on desk. "21" of what isn't said, and the link line and "15 more" already show there are others |
| "CI ON MAIN PASSED 7 OCT 2026" | main's tests pass | cut from the image | it's in the facts line under the code. It's also about `main`, while everything drawn is 0.1.3. Side by side, "passed" sits next to "never ends by itself" and they seem to contradict each other |
| rustmapper + "Crawls a site and writes one line for every page it reaches." | what it is | keep | the best line in the image |
| Start bar / end bar | where it starts and where it ends | keep | they bracket the loop; with the loop, they mean something |
| `pip install rustmapper` + 0.1.3 · 8 Nov 2025 | how you get it, and how old the release is | keep, as the image's only command | it's the door. Its age is the context for the hazard below |
| "3 min on Linux x86_64: pip builds it from source" | install cost | cut from the image, move to the wheel note | it leaves out that you need a Rust toolchain, which the text says. Half a fact in each home |
| `rust_sitemap crawl --start-url <site>` | the real command | cut from the image | it's in the copyable code block right below, with `<your-site>` |
| Magenta track | read in order | keep | |
| Loop line with up arrow | which steps repeat for every page | keep | the one thing only a drawing can show |
| seeder.rs "start URL; by default also seeds from sitemaps, CT logs, Common Crawl" | where URLs come from; it calls outside services by default | change wording | "CT logs" is jargon. Say "certificate logs" |
| bfs_crawler.rs "fetch a page; same-site links go back on the queue" | it's a crawler loop | keep | |
| governor.rs "fewer requests in flight when redb commits slow down" | it throttles itself to the store | change wording | "redb commits" means nothing to a visitor; the file name already serves the engineer. "fetches fewer pages at once when saving falls behind" |
| wal.rs "logged before stored: after a kill, export-sitemap still writes sitemap.xml" | a kill doesn't lose the crawl | change | false causality (above). Point it at the real cause, with its number |
| Hazard "never ends by itself: …" + hatch | the catch | change | right content, wrong weight. It's the one row a stranger must see, and it's drawn the lightest. Once 0.1.4 ships it changes to the `--max-urls` wording, which the gate already has |
| "press Ctrl-C once: …" | how to get out and get the file | keep | the way out, placed right |
| Ring marks | a stop | keep | they tell stops from the hazard and the governor's tick |
| Governor tick | a side control, not a step | keep | |
| desk file-name column | each line is a file you can open | keep on desk | |
| `data/sitemap.jsonl` + fields | what you get, with the real field names | keep | |
| Hand-off arrow + "read by ideal-url-organizer, with a test" | his projects fit together, and the join is tested | keep | the only line about the body of work |

## Every block of the page

| Block | Verdict | Why |
|---|---|---|
| Image | change | above |
| Alt text | keep | states the message in 25 words. Rebuild it if the hazard wording changes |
| Link line | keep | |
| Builds / Languages / Stack | keep | |
| rustmapper sentence | keep | |
| rustmapper facts line | keep | the one home for tests and CI once the image drops its CI line |
| Install code block | keep | the one home for commands |
| Wheel note | change | take the measured install time: "elsewhere pip builds it from source, which needs a Rust toolchain (3 min on a Linux x86_64 runner)" |
| Scrapy sentence, facts, code block, Grafana note | keep | fits 38 columns now; comments sit on their own lines |
| Scrapy bullets | keep | |
| Also, 15 more | keep | |
| Working rules | keep | |
| Found a mistake? | keep | |
| Data line | change | 82 words. "every line on it names code found there, and each line about the design also at 32c2651 on main" can't be parsed by anyone but its author. Cut it to two plain sentences |
| License | keep | |

## Must fix, ranked

1. **Release before you draw (owner action, Rust-sitemap; blocks shipping).** Land P1 with
   `tests/robots_4xx_allows_crawl.rs`, add a `[project.scripts]` entry so the wheel installs a command, and run
   `maturin generate-ci github` for Linux x86_64/aarch64, Windows and macOS wheels. Then publish 0.1.4 from HEAD.
   The pipeline already switches wordings when it does: H1 becomes "no depth limit…: stop it with --max-urls N",
   the `ends_by_itself` probe prints its measured seconds, and `resume` comes back once `resume_after_kill` passes.
   Why: today the image's main message about my flagship is a hang that's already fixed on main. Until then, don't
   publish this hero. Keep the round-5 one live. Nothing gets loosened.
2. **One home per fact, enforced on short runs too** (`scripts/sheets/route.py`, `scripts/checks/strings.py`).
   Cut R3 (the crawl command), the install-time line and the CI line from both editions. The image keeps exactly
   one command, `pip install rustmapper`, as the entrance. Extend STRINGS-TWICE so that any run of 3 or more words
   containing a code token (`_`, `--`, `.rs`, `.jsonl`), and any date, fails if it appears in both the hero and the
   README's visible text, with a one-entry allowlist: `pip install rustmapper`. This saves 3 lines on desk (about
   84 units) and 3 on phone (about 100 units).
3. **Fix W1's cause** (`chart.toml [route.rustmapper]`). The file becomes `writer_thread.rs`, the text "saved every
   50 ms: after a kill, export-sitemap still writes sitemap.xml". Anchors in both trees: `writer_thread.rs`
   contains `BATCH_TIMEOUT_MS: u64 = 50`, and `main.rs` (sdist) / the export module (HEAD) opens `CrawlerState`
   without `WalReader`. Probe `export_after_kill`. Print the 50 from the constant, not a literal. Add a T-ANCHOR case:
   change the constant in the fixture and the printed number changes.
4. **Cut the "RUSTMAPPER · 1 OF 21" line.** The title block becomes the name and the role, and nothing else. On
   phone that's 2 lines less (about 60 units) at the top of the first screen. Together with item 2, the phone sheet
   goes from 1155 to about 1000 (540 px), and the desk from 592 to about 480. Set the render gate to phone ≤ 1020,
   desk ≤ 500.
5. **Make the hazard the first thing you see** (`sheets/route.py`, trap drawing). Behind the hazard row, a band
   from the hatch's left edge (x 432 desk / 26 phone) to the right limit, as tall as the row's text block plus 6
   units, filled `accent` at 14 % over paper (day `#F0D4C7`, night `#312531`). Ink on it measures about 10:1 in both
   themes, so the text stays `ink`. Keep the hatch. No border, no legend. Why: a stranger's one catch has to land in
   the ten seconds they give the page (owner test 1), and on a chart the danger is the mark you can't miss. That's
   the theme carried by doing the job, not by a symbol. Test: the `contrast` plug-in checks text on the band, and
   T-NOSIZE still holds (the band's size depends on text, not on data).
6. **Plain words** (`chart.toml`): G1 "fetches fewer pages at once when saving falls behind". S1 "CT logs" →
   "certificate logs". Wheel note: "Prebuilt for Apple silicon on CPython 3.13; elsewhere pip builds it from
   source, which needs a Rust toolchain ({install secs} on a {runner} runner)." The figures come from `runcheck`.
7. **Data line to two sentences, under 45 words** (`render_readme.py`, `survey` marker): "The drawing is rustmapper
   <version> as pip installs it: each line names a file in that release, and its install, crawl, Ctrl-C, kill and
   export lines were run on <date> (<runner>). Tests and CI measured <taken> from <n> public repositories ·
   regenerated weekly." Keep the AI-trailer sentence after it, as is.

## Sources (fresh this round)

1. Nielsen Norman Group, "How Long Do Users Stay on Web Pages?": "the first 10 seconds of the page visit are
   critical"; "communicate your value proposition within 10 seconds".
   https://www.nngroup.com/articles/how-long-do-users-stay-on-web-pages/ (finding 1, must-fix 1, 5)
2. Nielsen Norman Group, "The Layer-Cake Pattern of Scanning Content on the Web": readers jump between elements
   that stand out; headings must look distinct from body text.
   https://www.nngroup.com/articles/layer-cake-pattern-scanning/ (finding 4: thirteen lines at equal weight;
   must-fix 5)
3. Nielsen Norman Group, "Reading Content on Mobile Devices": comprehension holds, but "the need for brevity and
   prioritization is still critical". https://www.nngroup.com/articles/mobile-content/ (must-fix 2, 4)
4. W3C, Understanding SC 1.4.10 Reflow: graphics are excepted because they are two-dimensional, but they should
   stay within the viewport. https://www.w3.org/WAI/WCAG22/Understanding/reflow.html (finding 4: an image of text
   doesn't reflow, so keep it short)
5. W3C WAI, Complex Images tutorial: a diagram needs a short alt plus a long description "as part of the main
   content". https://www.w3.org/WAI/tutorials/images/complex/ (the README text is the long description, so the
   image shouldn't duplicate it; must-fix 2)
6. Docker docs, `docker container stop`: SIGTERM, then SIGKILL after 10 s on Linux.
   https://docs.docker.com/reference/cli/docker/container/stop/ (the "a kill quits without it" clause is real: the
   usual way a crawl gets stopped writes nothing in 0.1.3)
7. PyPA, Entry points specification: for each `console_scripts` entry, the installer "will create a command-line
   wrapper". https://packaging.python.org/en/latest/specifications/entry-points/ (must-fix 1: HEAD's pyo3 build
   needs one, or 0.1.4 loses the command)
8. Semantic Versioning 2.0.0, item 4 and FAQ: 0.y.z "anything MAY change", and "if your software is being used in
   production, it should probably already be 1.0.0". https://semver.org/ (must-fix 1: cutting 0.1.4 is cheap and
   expected)
9. Nordic APIs, "Why Time to First Call Is a Vital API Metric": the benefit is lost when users meet "errors on their
   first attempt(s)". https://nordicapis.com/why-time-to-first-call-is-a-vital-api-metric/ (finding 1: the drawn
   route's first run never ends)
10. Stack Overflow Developer Survey 2025, operating systems (read through the table quoted at aboutchromebooks.com;
    the survey page itself didn't load): Windows about 57 % personal and 50 % professional, macOS about 33 %.
    https://survey.stackoverflow.co/2025/technology (must-fix 6: most visitors don't get the Apple-silicon wheel,
    so "needs a Rust toolchain" is the line they need)
11. GitHub REST API, `repos/BenjaminSRussell/Rust-sitemap/issues` and `/pulls` and `/commits?since=2025-11-09`:
    #65 and #63 closed 7 Oct 2026; 22 merged PRs and 55 commits since 0.1.3. (finding 1)
12. Code: sdist 0.1.3 `src/main.rs:197-250` (WAL replay only in `build_crawler`), `:387-397` (export opens
    `CrawlerState` only), `src/writer_thread.rs:11, :110-178` (50 ms batches; WAL fsync, then redb commit, then
    truncate), `src/cli.rs:58` (`"all"`), `src/url_utils.rs:81-91`; Rust-sitemap 32c2651 `src/writer_thread.rs:12`,
    `src/cli.rs:82` (`max_urls`), `src/orchestration/shutdown.rs:20-32` (only `ctrl_c` handled),
    `pyproject.toml:55` (`bindings = "pyo3"`); ideal-url-organizer `tests/test_import_rust_sitemapper.py` (6 tests).
