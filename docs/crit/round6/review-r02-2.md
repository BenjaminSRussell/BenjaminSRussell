# Review round 2, reviewer 2: the phone-first student

10 Oct 2026. Reviewer: a 19-year-old CS student who reads GitHub on a phone and screenshots what's worth sending.
Build looked at: `scratchpad/r6/build/round-01/` (desk and phone, day and night; the page on desk and phone, five
phone screens; `once-p1-lands/`; `gate.txt`), `README.md`, `SPEC.md`, `LOG.md`, the three round-1 reviews. Figures
checked against `assets/stats.json`, the Rust-sitemap clone at `32c2651`, the 0.1.3 sdist in `scratchpad/r6/sdist013`,
`chart.toml` and live PyPI. Findings fixed in round 1 aren't repeated here.

Verdict: **close, but not shippable as is. 7 / 10.** `meets_goal`: no.

## The first question: does it meet the owner's goal?

Mostly yes. I'll start with what a stranger on a phone gets, because that's the test he set.

- **It speaks to the project.** I scroll once and I know the name, what he builds, the one tool he wants me to look
  at, how to install it, what it does with each page, the one way it goes wrong, how to get out, and what file I end
  up with. The islands are gone and nothing has a size, so "is it the size of the project or how many commits?"
  can't come up.
- **The one drawn mark that earns its place is the loop.** The line back up the left side wraps fetch → log, and the
  hazard sitting at the bottom of it says "never ends by itself". Shape and words say the same thing: this loop has
  no exit except the next row, Ctrl-C. A list can't show that. Diagram practice says a loop needs a visible exit
  condition (Visual Paradigm's activity-diagram guide), and here the only exit is a keypress. That's the most useful
  thing on the image, and it's drawn, not just written.
- **Nothing announces the theme.** No sea words, no ship, no pirate talk. The magenta line and the hatch are the only
  hint, and they do a job.
- **It reads on a phone.** At 390 px the label text is about 14 px on screen, near Apple's commonly cited 11 pt floor
  and above it. NN/g found comprehension on phones is the same as on desktop, only a bit slower for hard text. So a
  dense but short card is fine, as long as each line is unambiguous. That's where it slips.

Where it falls short, in the order a phone reader hits them:

1. **One label on the image is false by the page's own rule.** The data line says "The drawing describes rustmapper
   0.1.3 … every line on it names code found there". The desk image labels the governor row `governor.rs`. 0.1.3 has
   no `governor.rs`: the governor is `governor_task` in `sdist:src/main.rs:84`, and `chart.toml` G1 anchors the
   release to `src/main.rs`. Someone who checks the first label they can check finds it's wrong. That is the "data
   doesn't look exactly accurate" complaint, coming back through the audit sentence itself.
2. **The crawl that was run isn't the crawl that's drawn.** The image and the README tell a stranger to run
   `rust_sitemap crawl --start-url <site>`, and S1 says that by default it "also seeds from sitemaps, CT logs, Common
   Crawl". The run check ran `--seeding-strategy none` against a local three-page site (`runcheck.steps[crawl_ctrl_c]`).
   The data line still says "its … crawl … lines were run against 0.1.3". The part a stranger never sees is the
   default: their first crawl sends their domain to crt.sh and to Common Crawl's index. crt.sh's operators state a
   limit of 5 requests per minute per IP. Common Crawl says its CDX endpoint is "heavily rate limited" and blocks IPs
   for 24 hours. The 0.1.3 seeder does back off on 429 and 5xx (`ct_log_seeder.rs:185-215`), so this isn't a hazard to
   draw. But the run claim has to say what was actually run.
3. **"The file" and "a kill" read as a contradiction.** Two rows apart: "after a kill, export-sitemap still writes
   sitemap.xml", then "a second press, or a kill, quits without it", where "it" is "the file". There are two files on
   the image, and "a kill" leads to two outcomes that sound opposite. I had to read it three times to work out that the
   kill skips `sitemap.jsonl` but the log can still be exported to `sitemap.xml`. On a phone that's the line people
   will screenshot, so it has to be exact. clig.dev's rule for a second Ctrl-C is to "tell the user what will happen",
   and the tool's own message does that. The image should be just as plain.
4. **"RUSTMAPPER · 1 OF 21" is a riddle.** 1 of 21 what? Rank, episode, stars? And on the phone it sits directly
   above the serif "rustmapper" header, so the name appears twice within about 60 px. The round-1 fix took the noun
   out. Put "public repositories" back and drop the name.
5. **"3 min on Linux x86_64: pip builds it from source" hides the condition.** It was measured on a runner with a
   Rust toolchain installed. A student on Linux without `rustc` gets a build failure, not a 3-minute wait. The README
   says "needs a Rust toolchain", but the image is what people see, and the image makes it sound like a plain wait.

None of these is a design problem. The concept now has a purpose: how to run it, how it behaves, where it ends. Each
fix is a word or a gate, and every one bears on "it should teach a visitor something true".

Would I screenshot it? Not yet. Once the kill line is fixed, the loop plus "press Ctrl-C once: that writes
data/sitemap.jsonl" is the bit I'd send a friend who's writing their own crawler. It's a real design detail (graceful
first press, hard second press, write-ahead log underneath), stated the way the tool behaves. YouGov's report on
Snapchat's study found Gen Z far more likely to talk in images than in text. A card like this gets passed around when
every line holds up when someone checks it.

## Figures checked

| Figure on the page | Key / source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 Nov 2025 | `edition.version/date`; live PyPI JSON today | 0.1.3, 2025-11-08 19:52; still the latest release, one cp313 macOS arm64 wheel plus the sdist | yes |
| 3 min on Linux x86_64, from source | `runcheck.rustmapper.steps[install].secs`, `.runner` | 179.8 s, Linux x86_64, "sdist (built with Rust)" | yes; the Rust requirement isn't said (finding 5) |
| `rust_sitemap` | `edition.scripts` | `["rust_sitemap"]` | yes |
| 1 of 21 | `repo_count` | 21 | yes; wording unclear (finding 4) |
| CI on main passed 7 Oct 2026 | `repos[Rust-sitemap].ci` | success, 2026-10-07, last 5 all success | yes |
| `seeder.rs`, `bfs_crawler.rs`, `wal.rs` | sdist `src/` listing and clone `src/` | present in both | yes |
| `governor.rs` | sdist `src/` | **absent**; governor is in `src/main.rs:84` | **no** (finding 1) |
| "by default also seeds from …" | `sdist:src/cli.rs:58` `default_value = "all"` | all | yes; not what the run check ran (finding 2) |
| "parent domain counts as same-site" | `sdist:src/url_utils.rs:88-90` | `base_domain.ends_with(url_domain)` | yes |
| "never ends by itself" | `runcheck` `ends_by_itself` | still running at 150 s | yes (3-page fixture) |
| Ctrl-C once writes the file; second press quits | `sdist:src/main.rs:507-535` | "Press Ctrl+C again to force quit", `join("sitemap.jsonl")` | yes |
| kill writes no file / export after kill works | `kill_writes_file` false, `export_after_kill` 3 `<loc>` | as stated | yes |
| url, depth, status_code, title | `sdist:src/state.rs:98-114` `SitemapNode` | all four present | yes |
| read by ideal-url-organizer, with a test | `handoffs[0].state` | `runs`, 15 reader fields ⊆ release writer | yes |
| 176 tests · 16k lines of Rust | `test_functions` 176, `lines.Rust` 16,390 | | yes |
| 1,920 tests · 69k lines of Python · CI 8 Oct | 1920, 69,036, success 2026-10-08 | | yes |
| 3 % AI co-author; 297 by agents | `coauthored_total.agent` 63 / `commits` 2,033 = 3.1 %; `agent_authored.total` 297 | | yes; nothing on the page counts commits (block 14 below) |
| measured 10 Oct 2026 | `taken` 2026-10-10 | | yes |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| Name, serif | whose page | keep | first and biggest; right |
| Role line, two caps lines | crawlers and data, in Python and Rust | keep | the image then shows exactly that |
| "RUSTMAPPER · 1 OF 21" | nothing clear | change | "1 of 21" has no noun; the name repeats the header right next to it. Say "1 OF 21 PUBLIC REPOSITORIES" |
| "CI ON MAIN PASSED 7 OCT 2026" | the code is tested and alive | keep | measured, dated |
| "rustmapper" header + sentence | which tool, what it does | keep | the best line on the card |
| Start bar | where to begin | keep | with the loop below, the track now has a shape to start |
| `pip install rustmapper` | how to get it | keep | the entrance belongs on the route, even with a copyable block below |
| "0.1.3 · 8 NOV 2025" | the release is eleven months old | keep | in context with "CI on main" it's the honest gap |
| "3 min on Linux x86_64: pip builds it from source" | what installing costs | change | add the condition: it needs Rust (finding 5) |
| `rust_sitemap crawl --start-url <site>` | the real command | keep | |
| Seeder ring + line | URLs come from more than links, and by default from third parties | keep | true for 0.1.3; the run claim must match (finding 2) |
| `seeder.rs` label (desk) | a file I can open | keep | exists in both trees |
| Fetch ring + line, `bfs_crawler.rs` | it's a crawl loop that stays on one site | keep | the start of the loop |
| Governor tick + muted line | it slows when storage can't keep up | keep | the tick-not-ring difference works: it acts on the loop, it isn't a step |
| `governor.rs` label (desk) | a file to open in the release | change | false for 0.1.3 (finding 1) |
| WAL ring + line, `wal.rs` | a kill doesn't lose the crawl's record | keep | measured by `export_after_kill` |
| Loop line + up arrow | the middle repeats for every page | keep | the one shape that teaches what a list can't |
| Hatch `//` + hazard line | it never stops by itself; scope is wider than you think | keep | sits at the loop's bottom, where it bites |
| Ctrl-C ring + line | the only exit, and what each kind of exit leaves behind | change | name the file; make it read cleanly against the WAL line (finding 3) |
| End bar | where you end up | keep | |
| `data/sitemap.jsonl` + field names | the output and its real fields | keep | JSON Lines' own rule (one JSON value per line, `.jsonl`) matches "one line per page" |
| Thin line + arrow, "read by ideal-url-organizer, with a test" | his projects connect, and the join is tested | keep | the only cross-project fact, and it's proven |
| Night edition | the same, in dark mode | keep | GitHub's mobile apps reportedly always serve the light image, so the day edition has to stand alone. It does |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image | how to run his main tool and how it behaves | change | findings 1 to 5 |
| Alt text | the same in 25 words | keep | |
| Link line | where to go | keep | |
| Builds / Languages / Stack | who he is, what he uses | keep | |
| rustmapper sentence | what it is | keep | |
| Facts line | tested, alive, how big | keep | every figure holds |
| Install code block | copyable commands | keep | |
| Wheel note | when pip just works | keep | the copyable home of the condition the image shortens |
| Scrapy sentence, facts | the second project | keep | |
| Scrapy code block | how to start it | change | "# start.py must run from here" now sits *above* `cd Scraping_project`, so "here" points to the folder you're in *before* the cd, which is the wrong one. Say "# run start.py from inside this dir" (35 columns) |
| Scrapy note (Grafana, by name, sample URLs) | three real catches | keep | |
| Scrapy bullets | how it's built | keep | |
| Also (4) | the next projects worth a look | keep | |
| 15 more `<details>` | the rest, folded | keep | |
| Working rules | how he thinks, each with a dated project | keep | each rule cites its proof |
| Found a mistake? | the page can be corrected | keep | |
| Data line | what was checked and run | change | its first sentence is false for `governor.rs` and overstates the crawl (findings 1, 2). The AI clause "and are not counted as mine" qualifies a count the page no longer prints; give it its base. On the phone "Ctrl-C" breaks as "Ctrl-/C" |
| License | terms, how to fork | keep | |

## Must fix, ranked

1. **Make every desk file label true for the release.** In `scripts/data/route.py`, draw an entry's `file` label
   only when a path ending in that name is among both its `head` and its `release` anchors. Otherwise print no label
   (the row keeps its text, as on the phone). Today that drops `governor.rs` (release: `src/main.rs`). Add a test in
   `tests/test_route.py`: an entry whose release anchor is a different file gets `label = None`. Add a ROUTE-LABEL
   fail to `scripts/checks/route.py` for any drawn label missing from either tree. Why: the data line promises that
   every line names code in 0.1.3, and this is the one place it doesn't.
2. **Say what the run check actually ran.** In `render_readme.py route_clause`, take the crawl wording from the step's
   `cmd`. The data line reads "… its install, crawl (on a local three-page site, `--seeding-strategy none`), Ctrl-C,
   kill and export lines were run …". Or run the probe with the drawn defaults, but on 127.0.0.1 that means queries to
   crt.sh and Common Crawl from CI every week, which their limits argue against. So change the words, not the probe.
   Add a test: a `crawl_ctrl_c` cmd containing `--seeding-strategy none` must put that flag in the clause. Why: an
   audit sentence that overstates is worse than none.
3. **Rewrite C1 so the two "kill" rows can't be misread.** `chart.toml` C1 `text` = "press Ctrl-C once: that writes
   data/sitemap.jsonl; a second press or a kill skips it" (76 characters, down from 84, so no new wrap on desk or
   phone). W1 stays. Anchors and probes unchanged. Why: two files and two kinds of exit; the reader must know which
   file each line means.
4. **Give "1 of 21" its noun and drop the repeated name.** Fine-print line 1 = "1 OF 21 PUBLIC REPOSITORIES" on
   desk and phone. On desk it must fit x 56–410 at `label` 19, tracking 1.6. If `typeset` says it doesn't, use
   "1 OF 21 PUBLIC REPOS". Update T-PURPOSE and the phone height check (no change expected: same line count). Why: a
   number without a unit teaches nothing, and the name is already 60 px away.
5. **Put the condition into the install measure.** R4 text = "3 min on Linux x86_64, compiled; needs Rust" (43
   characters, shorter than today's 48, so the phone stays on one line and the P1 edition stays under 1,200). Record
   `rustc --version` in `runcheck.py`'s install step `detail` so "needs Rust" rests on the run as well as on maturin.
   Why: for a stranger without Rust the current line isn't true.
6. **Scrapy comment:** in `render_readme.py`'s Scrapy block (and `tests/test_pipeline.py:400`), "# start.py must run
   from here" → "# run start.py from inside this dir". Why: the comment sits above `cd`, so "here" means the wrong
   place.
7. **Data-line tidy-ups:** (a) give the AI clause its base: "63 of my 2,033 commits (3 %) carry an AI co-author
   trailer; 297 more were written by coding agents (Claude, jules) and are not in the 2,033" (from
   `coauthored_total.agent`, `commits`, `agent_authored.total`). (b) Write "Ctrl‑C" with U+2011 (non-breaking hyphen)
   in `route_clause`, so it never splits across lines on the phone.

## Sources (fresh this round)

1. clig.dev, *Command Line Interface Guidelines*, "Signals and control characters" and "Robustness": "Tell the user
   what will happen when they hit Ctrl-C again"; crash-only, recoverable. https://clig.dev/ (must-fix 3)
2. Common Crawl, *FAQ*: the CDX endpoint is "heavily rate limited"; 503 means slow down; blocked IPs wait 24 h.
   https://commoncrawl.org/faq (must-fix 2)
3. crt.sh Google Group, Sectigo staff on rate limits (5 requests per minute per IP, 2023; no published fair-use policy,
   2024). https://groups.google.com/g/crtsh/c/NZJntKrBdmg and https://groups.google.com/g/crtsh/c/niabC5EYW2g
   (must-fix 2)
4. W3C, *Understanding SC 1.4.10: Reflow*: maps and diagrams are excepted only where two-dimensional layout carries
   the meaning, as the loop does here; the text around them must still reflow.
   https://www.w3.org/WAI/WCAG22/Understanding/reflow.html (why the loop earns the image form; the lookups stay text)
5. NN/g, *Reading Content on Mobile Devices*: "no practical differences in the comprehension scores"; hard text
   slightly slower on phones. https://www.nngroup.com/articles/mobile-content/ (a dense card is fine if each line is
   unambiguous)
6. Apple, *Human Interface Guidelines: Typography*, minimum legible size (11 pt per secondary summaries).
   https://developer.apple.com/design/human-interface-guidelines/typography (phone type check)
7. RodrigoTomeES, *prefers-color-scheme hack*, and dev.to, *GitHub README images based on prefers-color-scheme*:
   GitHub's Android and iOS apps return the light theme. https://github.com/RodrigoTomeES/prefers-color-scheme-hack ;
   https://dev.to/keracudmore/github-readme-images-based-on-prefers-color-scheme-5cp8 (the day edition must stand
   alone; it does)
8. Visual Paradigm, *Handling Decisions and Loops in Activities*: a loop needs a clear exit condition.
   https://skills.visual-paradigm.com/?p=1697 (the loop and its Ctrl-C exit)
9. JSON Lines: each line is a valid JSON value; extension `.jsonl`. https://jsonlines.org/ (R13 "one line per page")
10. PyPI JSON for rustmapper, fetched 10 Oct 2026: 0.1.3 is still the latest, one cp313 macOS arm64 wheel plus the
    sdist. https://pypi.org/pypi/rustmapper/json (release figures; must-fix 5)
11. HR Dive on Ladders' 2018 eye-tracking study: a 7.4 s first screen; simple layouts with clear headings did best;
    clutter and long sentences hurt. https://www.hrdive.com/news/eye-tracking-study-shows-recruiters-look-at-resumes-for-7-seconds/541582/
    (why the title block's fine print must be unambiguous at a glance; must-fix 4)
12. YouGov, *Gen Z prefer visuals* (Snapchat study of 27,000 users): Gen Z are much more likely to communicate in
    images. https://yougov.com/articles/34256-gen-z-prefer-visuals-snapchat (the image is what gets screenshotted
    and passed on, so it has to be exact)
13. Clones and release: `sdist rustmapper-0.1.3` `src/` listing (no `governor.rs`), `src/main.rs:84-126, 507-535`,
    `src/cli.rs:58`, `src/url_utils.rs:81-91`, `src/state.rs:98-114`, `src/ct_log_seeder.rs:179-215`;
    Rust-sitemap `32c2651` `src/orchestration/governor.rs`; `chart.toml` G1, C1; `assets/stats.json` `runcheck`.
