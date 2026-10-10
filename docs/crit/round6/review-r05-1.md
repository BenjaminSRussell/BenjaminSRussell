# Review round 5, reviewer 1: Ben, the owner

10 Oct 2026. Build looked at: `scratchpad/r6/build/round-04/`: the desk sheet (870) and phone sheet (390), day and
night; `once-p1-lands/` (the same sheet with S2 drawn); the whole page on desk (screens 1 and 2, light, plus the dark
full page) and on phone (screens 1 to 5). Read: `README.md`, `SPEC.md`, `LOG.md` (round-4 fixes) and the twelve reviews
from rounds 1 to 4. I don't repeat anything that was fixed. Every figure was checked against `assets/stats.json`, the
0.1.3 sdist, the Rust-sitemap clone at `32c2651`, the PyPI JSON and the GitHub API today.

Verdict: **not yet. 7 / 10.** The page around the image got better this round. The image itself got one new defect,
and the thing that kept it off `main` last round is still there. I would not ship it as it is.

## The first question: does it meet my goal?

Mostly, and closer than last round. Last round's fixes landed: one left edge, the stop comment in the block people
paste, an AI clause tied to the counts it qualifies, a licence line with no build footer, a pick sentence that's true.
I'm not asking for a new concept. The picture teaches something a list can't: a URL goes in, gets fetched, its links
queued, it's saved, and that repeats; there's one way out; the file lands here; another of my projects reads it.
Nothing has a size and no word names the theme. It reads on the phone.

What stops me shipping it:

1. **The release is still the loudest thing on my profile, and the click-through contradicts the profile.** The red
   ring still reads "never stops by itself". Main fixed that in `d751cf0` on 7 Oct, and PyPI still says 0.1.3, 8 Nov
   2025 (checked today). `check.py --tier fast` still fails ROUTE-UNVERIFIED on S2. That's my job, and I said so last
   round. What's new: I followed the image's own link. It goes to Rust-sitemap, whose About text says the tool "goes
   until it reaches end points". That's the opposite of the red ring. Its README (line 25) says
   "`pip install rustmapper` installs the **Python library**. The command-line tool is the Rust binary `rust_sitemap`.
   Install it with `cargo install`" and then calls the command `rustmapper` through an alias. My profile, right above,
   says `pip install` gives you the command line, and prints `rust_sitemap crawl`. For 0.1.3 the profile is right and
   the README is wrong. So a visitor who does exactly what the image invites, a tap, lands on three statements that
   disagree with it. Dabbish et al. found that people on GitHub draw a "surprisingly rich set of social inferences"
   from what's visible [S2]. The inference here is "his flagship's docs don't agree with each other." Fixing the About
   text and README line 25 doesn't need a release. It's ten minutes.

2. **On the desk, the file labels read as part of my title.** Last round I asked for the labels to move into the
   empty left column. They did, and now `seeder.rs` sits with its baseline about 10 px under "PYTHON AND RUST" on screen, in the same
   block. Read top to bottom, the left column says "CRAWL AND DATA INFRASTRUCTURE / PYTHON AND RUST / seeder.rs /
   bfs_crawler.rs / writer_thread.rs". The code check passes because the boxes don't overlap, but proximity is what a
   reader goes by: "items close together are likely to be perceived as part of the same group" [S5], and a column
   under a heading reads as one region [S6]. The phone, the common case, has no labels and loses nothing. An
   engineer finds the files in one click. Cut them from the desk too.

3. **The image's only date reads as the date of the whole drawing.** On the desk, "0.1.3 · 8 NOV 2025" is
   right-aligned at x 1224, about 250 px on screen from the end of `pip install rustmapper`. That far from the command
   it reads as the sheet's date stamp in the top corner, so it looks like the profile is a year old. The phone gets it
   right: the date follows the command closely and reads as "this release is from Nov 2025". The desk should do the
   same. It's proximity again [S5], and it's my old complaint that "the data doesn't look exactly accurate".

4. **The image prints the recovery command and not the main command.** By my own rule from round 2, commands live in
   the code block and the image keeps exactly one, `pip install rustmapper`. That's why R3 (`rust_sitemap crawl`) was
   cut. But C1 still prints `rust_sitemap export-sitemap writes the pages to sitemap.xml` after a kill. So the drawing
   names the rare path's command and leaves out the main path's. That clause makes C1 the longest row: two desk lines,
   three phone lines. And it's an instruction for the moment you've killed a crawl, when you're at the terminal with
   the code block, not reading my profile. "A well-designed warning will be of little use if the user does not
   encounter it in the task environment" [S3], and a how-to step belongs where the action is [S8]. Move it into the
   block as a comment above the export line. C1 becomes "press Ctrl-C once to write `data/sitemap.jsonl`".

5. **The data line is still a methods section in fine print.** On the phone it runs to ten lines of small type at the
   foot of the page. Most of it is process: "every rustmapper source file it names is in that release; the reader it
   points to is ideal-url-organizer's, at `159968a`", "(a local 3-page site, `--seeding-strategy none`)", "Tests and
   CI measured 10 Oct 2026 from 22 public repositories · regenerated weekly". "Regenerated weekly" is the
   generated-by footer I ruled out. What a visitor needs is two facts: which release the drawing shows and that it was
   run, and the honest note about agent-written commits. Keep those. The proof stays in `DESIGN.md`, which the word
   "drawing" already links to.

6. **The pick sentence is true now, but nobody talks like that.** "For the list of a site's URLs, from one binary with
   no services to run, **rustmapper**; to keep the pages themselves, deduplicated and summarised, in a pipeline that
   needs Docker, **Scrapy**." Each project name comes after a pile of clauses. Readers fixate on the start of lines and
   on words that stand out [S7], so put the bold names first.

## Figures checked

| Printed | Source | Value | Holds |
|---|---|---|---|
| pip install rustmapper / 0.1.3 · 8 NOV 2025 | `edition.version`, `.date`; PyPI JSON today | 0.1.3, 2025-11-08 19:52 UTC; 0.1.0–0.1.3 all that day; latest is still 0.1.3 | yes |
| your URL, plus by default sitemaps, certificate logs, Common Crawl | `sdist:src/cli.rs` `seeding_strategy` `default_value = "all"`; three `*_seeder.rs` | | yes (release scope) |
| `seeder.rs`, `bfs_crawler.rs`, `writer_thread.rs` | sdist `src/` and clone `src/` | all three exist in both | yes (but finding 2) |
| fetches a page; queues links on your URL's domain, above or below it | `sdist:src/url_utils.rs:81-91` `is_same_domain`, both branches | | yes |
| fetches fewer pages at once when saving falls behind | `sdist:src/main.rs:90-140` governor: commit EWMA > 500 ms shrinks permits | | yes |
| saved to its database every 50 ms | `sdist:src/writer_thread.rs:11` `BATCH_TIMEOUT_MS: u64 = 50` | | yes |
| never stops by itself; done when `Received work item` lines stop | `sdist:src/bfs_crawler.rs:433` (`eprintln!`, stderr), `:548-553` (`else =>` arm); runcheck `ends_by_itself` false, `quiet_after_last_page` ok | still running at 150 s; 3 work-item lines for 3 URLs | yes for 0.1.3; fixed on main `d751cf0` |
| press Ctrl-C once … after a kill, `rust_sitemap export-sitemap` writes … `sitemap.xml` | runcheck `crawl_ctrl_c` ok (2.0 s), `kill_writes_file` false, `export_after_kill` 3 `<loc>` | | yes (but finding 4) |
| data/sitemap.jsonl fields: url, depth, status_code, title, … | `SitemapNode`, both trees | | yes |
| sorted by ideal-url-organizer: `scripts/import_rust_sitemapper.py`, with a test | `handoffs[0]` `state: runs`, `does: sorted by`; 15 reader fields ⊆ writer in both trees | | yes |
| On main at `32c2651` · 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust | `repos[Rust-sitemap]` | 176; success 2026-10-07; 16,390 | yes |
| On main at `96e7a1a` · 1,920 tests · CI passed 8 Oct 2026 · MIT license · 69k lines of Python | `repos[Scrapy]` | 1,920; success 2026-10-08; MIT; 69,036 | yes |
| Prebuilt for Apple silicon on CPython 3.13; 3 min from a cold cache on a 4-core Linux x86_64 machine | `edition.wheels`; runcheck `install` | `cp313-cp313-macosx_11_0_arm64` only; median 171.4 s, cold, 4 CPUs | yes |
| up to 20 requests at a time to one host, 256 in all, no pause unless `Crawl-delay` | `sdist:src/state.rs:281, 285`; `cli.rs` `workers` `default_value = "256"` | | yes |
| 0.1.3 writes one `sitemap.xml`; 50,000 URLs per file | no `SitemapIndexWriter` in the sdist; main `sitemap_writer.rs:134` `DEFAULT_MAX_URLS_PER_SITEMAP = 50_000` | | yes |
| 45 of rustmapper's 146; 71 of Scrapy's 499 | `repos[].others` (bot), `all_hands` | Claude 45 / 146; jules 49 + Claude 22 = 71 / 499 (dependabot 8 left out) | yes |
| 22 public repositories; 15 more | `repo_count`; 22 − profile − 2 flagships − 4 Also | 22; 11 listed + 4 on the "Also:" line = 15 | yes |
| 25 ways; stage 3; stage 4; 50,000 characters; localhost:3000 | `figures[]` | all `holds: true` | yes |
| (the click-through) Rust-sitemap About text and README line 25 | GitHub API `repos/BenjaminSRussell/Rust-sitemap` description; clone `README.md:25` | "goes until it reaches end points"; "installs the Python library" | **no**: both contradict the profile (finding 1) |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page | keep | |
| Role line, two caps lines | crawl and data infrastructure, Python and Rust | keep | the drawing under it proves both |
| "rustmapper" + "Crawls a site and writes one line for every page it reaches." | which project and what it does | keep | the best sentence on the page |
| Start bar | where you begin | keep | |
| `pip install rustmapper` | the way in | keep | the image's one command, as I ruled |
| "0.1.3 · 8 NOV 2025" | how old the thing you'd install is | change | on the desk it's 250 px away and reads as the drawing's date (finding 3) |
| Magenta track | one way through, read top to bottom | keep | the strip-map form: a route read start to finish, with only what's along it [S9] |
| Stop rings | a step the tool takes | keep | |
| S1 seeds | URLs come from more than links; by default it calls outside services | keep | |
| F1 fetch / queue | it's a crawler loop, and its scope | keep | |
| G1 governor note | it throttles itself to its own store | keep | the one design idea that's mine and unusual |
| W1 "saved to its database every 50 ms" | it saves as it goes | keep | |
| Desk file labels | which file to open | cut | they read as part of the title block, and the phone does without them (finding 2) |
| Loop bracket with up arrow | which rows repeat | keep | once 0.1.4 ends by itself, this stays true: the crawl loop until the queue empties |
| Gap in the track under the loop | the loop has no exit but Ctrl-C | keep | closes by itself when a release ends on its own |
| H1 in the dotted danger line | the catch, and how to tell when you're done | keep the mark, retire the bug | true of 0.1.3 only (must-fix 1) |
| C1 "press Ctrl-C once to write … after a kill, …" | the one thing you do | change | cut the kill clause into the code block (finding 4) |
| End bar | where you end up | keep | |
| `data/sitemap.jsonl` + fields | what you get, in the struct's own words | keep | |
| Hand-off arrow + "sorted by ideal-url-organizer …, with a test" | my projects feed each other, and the join is tested | keep | |
| Night editions | the same | keep | contrast holds |
| Phone editions | the same, without file labels | keep | still the cleanest edition; the desk should match it |
| Link round the image | a tap lands on the project | keep, and fix what it lands on | must-fix 1(b) |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image | above | change | must-fix 2, 3, 4 |
| Alt text | the route in 25 words | keep | true today; it's rebuilt from `routes` |
| Link line | where to go | keep | |
| Builds / Languages / Stack | what I build and with what | keep | |
| Pick sentence | which tool for which job | change | names first (finding 6) |
| rustmapper sentence | what it is; the API isn't released | keep | |
| rustmapper facts line | alive, tested, size, which snapshot | keep | |
| Install code block | how to run and stop it | change | takes the kill recovery comment (must-fix 4) |
| Wheel note | when pip just works | keep | |
| Load and 50,000 note | what it does to someone's server; the sitemap limit | keep | |
| Scrapy sentence, facts line, code block, Grafana note, bullets | the second tool, measured, and how to start it | keep | |
| Also | the next four | keep | |
| 15 more | the rest | keep | |
| Working rules | how I work, each with a dated commit | keep | |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn; agent authorship | change | cut it to the two facts (finding 5) |
| Licence line | the profile's terms | keep | fixed last round |

## Must fix, ranked

1. **The flagship's own pages stop contradicting the profile** (in Rust-sitemap; owner, me).
   - (a) Ship 0.1.4 as I listed last round (P1 robots 4xx, the MIT `LICENSE` that `license-files` names,
     `[project.scripts]`, wheels, release). Until it passes the run check, this image doesn't go to `main`. Nothing
     changes in this repository for that.
   - (b) **Today, with no release:** set Rust-sitemap's About text to the image's header sentence, "Crawls a site and
     writes one line for every page it reaches." (GitHub repo settings, one field; `gh repo edit
     BenjaminSRussell/Rust-sitemap --description "…"`). Rewrite `README.md:25` to: "`pip install rustmapper` (0.1.3,
     macOS arm64 wheel or a source build) installs the `rust_sitemap` command. The Python library is on main and
     ships in the next release." In the examples below it, change the alias `rustmapper` to `rust_sitemap` while
     0.1.3 is current.
   - Why: the image links there. A visitor who taps it should land on the same facts, not three statements that
     disagree with it [S2]. A pinned card and search results show that About text too [S10].

2. **Cut the desk file labels** (`scripts/sheets/route.py:528-545`; about 10 lines and a test).
   - Add a proximity rule to the all-or-none test. A label may be drawn only if its cap height starts at least one
     line (`G["line"]`, 28) below the title block's last baseline. Today `seeder.rs` fails that, so none are drawn and
     the desk matches the phone.
   - Change the data line's "every rustmapper source file it names" in the same commit (it goes anyway in must-fix 5).
   - Test: on today's stats, `report.file_labels` is false on the desk.
   - Why: `seeder.rs` one baseline (about 10 px) under "PYTHON AND RUST" reads as a fourth line of my title [S5, S6].

3. **Put the release date next to the install command on the desk** (`route.py:469-470`; about 4 lines).
   - Set the release label at `TX + width(install, "machine") + 32`, anchor start, same baseline, `muted`, caps, as
     on the phone. Today that's about x 724 to 884 in sheet units, well inside 1224.
   - If it doesn't fit the measure, it drops under the command, never right-aligned.
   - Test: on every edition, the gap between the end of the command and the start of the release label is at most 40
     units.
   - Why: at the far right it reads as the drawing's date, a year old [S5].

4. **Move the kill recovery from C1 into the code block** (`chart.toml [route.rustmapper]` C1;
   `render_readme.py install:Rust-sitemap`; about 15 lines and tests).
   - C1 becomes "press Ctrl-C once to write `data/sitemap.jsonl`". Its probes stay the same (`crawl_ctrl_c` passed).
   - The block, still within 38 columns:
     ```
     pip install rustmapper
     rust_sitemap crawl \
         --start-url <your-site>
     # stop it with one Ctrl-C
     # sitemap.xml, even after a kill:
     rust_sitemap export-sitemap
     ```
   - The new comment is printed only while `kill_writes_file` fails and `export_after_kill` passes. Once a kill writes
     the file, the line goes.
   - STRINGS-TWICE stays clean, because the image no longer has the clause. HERO-SELF-TWICE likewise.
   - Height: desk −28, phone −68. Rebaseline ROUTE-HEIGHT.
   - Why: one home for commands (my round-2 rule). The recovery step belongs where you are when you need it
     [S3, S8]. This also removes the image's longest row.

5. **Cut the data line to what a visitor needs** (`render_readme.py`, `survey` marker; about 10 lines and a test).
   - Text: "The [drawing](DESIGN.md) is rustmapper 0.1.3, the release pip installs; its commands were run against a
     local 3-page site on 10 Oct 2026 (Linux x86_64). Tests and lines are counted per repository, whoever wrote them:
     coding agents (Claude, jules) authored 45 of rustmapper's 146 commits and 71 of Scrapy's 499."
   - Gone: the source-file and reader-sha clause, the `--seeding-strategy` aside, "Tests and CI measured … from 22
     public repositories", and "regenerated weekly". The facts lines already date and pin every count. The 15 in the
     `<details>` row still comes from `repo_count`, so REPO-SET still holds.
   - Test: no "regenerated" or "generated" in visible README text.
   - Why: it's ten phone lines of methods. Two of its clauses are build process, and one is a generated-by footer.

6. **Names first in the pick sentence** (`chart.toml [copy] pick`; one line, same gates).
   - Text: "**rustmapper** gives you a site's list of URLs from one binary, with no services to run. **Scrapy** keeps
     the pages themselves, deduplicated and summarised, in a pipeline that needs Docker."
   - The `no_services` gate and the three `use = "pick"` figures stay.
   - Why: a reader scanning the start of the line should hit the tool's name first, not a stack of clauses [S7].

## Sources (new this round)

1. [S1] Trockman, Zhou, Kästner, Vasilescu, "Adding Sparkle to Social Coding: An Empirical Study of Repository Badges
   in the npm Ecosystem", ICSE 2018. Visible status signals are read as quality signals:
   https://par.nsf.gov/servlets/purl/10063054
2. [S2] Dabbish, Stuart, Tsay, Herbsleb, "Social coding in GitHub: transparency and collaboration in an open software
   repository", CSCW 2012. People draw "a surprisingly rich set of social inferences" from what's visible:
   https://www.lri.fr/~mbl/ENS/CSCW/2012/papers/Dabbish2012.pdf
3. [S3] Wogalter, Conzola, Smith-Jackson, "Research-based guidelines for warning design and evaluation", Applied
   Ergonomics 33 (2002) §2.3: "A well-designed warning will be of little use if the user does not encounter it in the
   task environment": https://about.fb.com/wp-content/uploads/2018/04/ArtElevenWogalterNine.pdf
4. [S4] Keep a Changelog 1.1.0, "Unreleased" section: what's on main and not yet released is something to show
   users, not hide (it backs must-fix 1(b)'s "on main, ships in the next release"):
   https://keepachangelog.com/en/1.1.0/
5. [S5] Nielsen Norman Group, "Proximity Principle in Visual Design": "Items close together are likely to be perceived
   as part of the same group": https://www.nngroup.com/articles/gestalt-proximity/
6. [S6] Nielsen Norman Group, "The Principle of Common Region": items within a boundary are perceived as a group:
   https://www.nngroup.com/articles/common-region/
7. [S7] Nielsen Norman Group, "Text Scanning Patterns: Eyetracking Evidence" (F, spotted, layer-cake): readers fixate
   on line starts and on words that stand out: https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/
8. [S8] Diátaxis, "How-to guides": "action and only action", from the user's side, where the work is done:
   https://diataxis.fr/how-to-guides/
9. [S9] *Britannia* (Ogilby, 1675): roads drawn as continuous strips, start to destination, with only what lies along
   the way. That's the form this route follows: https://en.wikipedia.org/wiki/Britannia_(atlas)
10. [S10] GitHub Help, "Pinning repositories to your profile": pinned cards show a summary of the work, stars and
    language: https://help.github.com/articles/pinning-repositories-to-your-profile/

Clones and APIs: PyPI JSON `rustmapper` (latest 0.1.3; 0.1.0–0.1.3 all on 8 Nov 2025; files: one macOS arm64 wheel and
the sdist); GitHub REST `repos/BenjaminSRussell/Rust-sitemap` (description "This program runs a rust webscraper to
create a sitemap that goes until it reaches end points", pushed 7 Oct) and `/commits` (`32c2651` newest; `d751cf0`,
`aaa38d6` on 7 Oct); Rust-sitemap clone `README.md:1-60`, `src/sitemap_writer.rs:134`; sdist 0.1.3 `src/cli.rs:25-70`,
`src/main.rs:84-140`, `src/bfs_crawler.rs:433, 520-560`, `src/url_utils.rs:81-91`, `src/writer_thread.rs:11`,
`src/state.rs:281-285`; `assets/stats.json` (`repos`, `routes`, `handoffs`, `runcheck`, `figures`,
`agent_authored`); `scripts/sheets/route.py:469-470, 528-545`.
