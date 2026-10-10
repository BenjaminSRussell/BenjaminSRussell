# Review round 11, reviewer 2: the phone-first student

10 Oct 2026. Reviewer: a 19-year-old CS student who reads GitHub on a phone and screenshots what's worth sending.
I looked at every PNG in `scratchpad/r6/build/round-10/`: the sheet on desk at 870 (day and night), the phone sheet
at 390 and 308 (day and night), the desk page (two screens), the phone page at 390 (seven screens) and at 360 (seven).
I read `README.md`, `SPEC.md`, `LOG.md` through round 10, and the reviews from rounds 1 to 10, including round 2's
student review. Nothing already fixed is repeated. Where I bring back something an earlier round declined, I say so
and say what's new.

Verdict: **not yet. 8 / 10.** `meets_goal`: no. It's close. I would screenshot the image, and that's exactly the
test it fails: the screenshot tells my friend how to install the tool but not how to run it.

## The first question: does it meet the owner's goal?

- **Every map and every element has a deep purpose.** Yes. The image is one run of rustmapper 0.1.3 from top to
  bottom: install, where URLs come from, the loop it runs for every page, the one catch, the one key you press, the
  file you get, and the project of his that reads that file. Nothing has a size, so nobody can ask "is it the size
  of the project or how many commits?" The loop bracket and the dotted box are the only marks that aren't text, and
  each one carries a fact: which rows repeat, and where the catch is.
- **It teaches something true and useful about his actual projects.** Yes. Every figure I checked holds (table
  below). The gap is a missing fact, not a wrong one. The image never names the command you type, and the command
  (`rust_sitemap`) isn't the package name (`rustmapper`). That's the first place a stranger goes wrong, and the
  image's own sentence (SPEC §0) promises "how you start rustmapper … where a stranger goes wrong" (must-fix 1).
- **Nothing chases a reason.** Yes, in the image. On the page, one block is in the wrong place rather than without a
  reason: the list headed "Before you run 0.1.3:" comes after the commands it warns about (must-fix 2).
- **Nothing announces the theme.** True. There are no sea words and no ship. The magenta line and the dotted box
  would read as "a route" and "watch out" to someone who has never seen a chart.
- **Reads on a phone.** The image fits one screen at 308 px (what an iPhone at 390 actually shows), day and night.
  The page is about six screens at 390. One code comment runs into the next on a phone (must-fix 3).

**Would I send it?** The image, yes, to a friend writing their own crawler. "0.1.3 never exits by itself; done once
`Received work item` lines stop for 30 s" plus the Ctrl-C row is a real thing to know, and it's stated the way the
tool behaves. On an iPhone, Live Text lets whoever gets the screenshot press and hold `pip install rustmapper` and
copy it [S1, S2]. So the image's commands are usable even as a picture. That makes the missing run command matter
more, not less. PyPI's page for rustmapper links back to the repository (`PKG-INFO` `Project-URL: Homepage`), so
someone with only the screenshot can find him.

## Figures checked (against `assets/stats.json`, the 0.1.3 sdist and the clones)

| Printed | Checked in | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `edition.uploads` | 0.1.3 at 2025-11-08T19:52:41 | yes |
| by default also from sitemaps, certificate logs and Common Crawl | sdist `src/cli.rs:58` `default_value = "all"` | all | yes |
| up to 20 pages at a time from each host | sdist `src/state.rs:285` `max_inflight: 20` | 20 | yes |
| `Received work item` | sdist `src/bfs_crawler.rs:433` `eprintln!` | on stderr | yes |
| a second press before `Saved to:` | sdist `src/main.rs:539` | `println!("Saved to: …")` | yes |
| sorted 21 ways by ideal-url-organizer | `figures` (`self.methods`), handoff `159968a` | 21 | yes |
| 25 ways … 21 … 4 more (Also) | `figures` glob `src/organizers/method_*.py`; clone | 25 files | yes |
| 176 tests · 16k lines of Rust · `32c2651` | `repos[Rust-sitemap].test_functions`, `lines.Rust`, `head` | 176; 16,390; 32c2651 | yes |
| CI passed 7 Oct 2026: tests, rustfmt | `repos[Rust-sitemap].ci` | success, 2026-10-07, gates tests and rustfmt | yes |
| 1,920 tests (CI selects all but 41) · 69k lines of Python · MIT | `repos[Scrapy].test_functions`, `ci_selection.not_selected`, `lines`, `license` | 1,920; 41; 69,036; MIT | yes |
| CI passed 8 Oct 2026: tests, ruff, mypy, bandit | `repos[Scrapy].ci` | success, 2026-10-08 | yes |
| up to 256 at a time across all hosts | sdist `src/cli.rs:32` | 256 | yes |
| 3 min from a cold cache on a 4-core Linux x86_64 machine | `runcheck.rustmapper` install | median 171.4 s, 4 CPUs | yes |
| Prebuilt for Apple silicon on CPython 3.13 | `edition.wheels` | `cp313-cp313-macosx_11_0_arm64` only | yes |
| 143,208 bundled URLs, 134,807 on uconn.edu | `figures` `csv_rows` | 143,208; 134,807 | yes |
| Languages: Python, Rust; Swift, JavaScript, TypeScript, C, Go | `repos[].main_language` | Python 11, Swift 3, JavaScript 2, Rust 2, TypeScript 2, C 1, Go 1 | yes (lead pair first, then by count) |
| 15 more | `repo_count` 22 minus the profile, 2 flagships, 4 in Also | 15 | yes |
| Rule 3: metrics 6 days after the first commit, dashboard 5 days after that | Scrapy `first` 2025-09-25; `rules` prometheus `d571e6e` 2025-10-01, grafana `e8cbe15` 2025-10-06 | 6 and 5 | yes |
| 45 of rustmapper's 146; 71 of Scrapy's 499; co-signed 1 and 30 | `repos[].others`, `all_hands`, `coauthored.agent` | 101 + 45 = 146; 420 + 49 + 22 + 8 = 499, agents 71; 1; 30 | yes |

## Every element of the image

| Element | What a visitor learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose work this is | keep | the screenshot carries his name when it leaves GitHub |
| Role line, "CRAWL AND DATA INFRASTRUCTURE / PYTHON AND RUST" | what he does and in what | keep | the drawing under it proves it |
| Empty left column under the role (desk) | nothing, on purpose | keep | it makes the route the thing you read |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project and what you get | keep | |
| Start bar + `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | how to get it and how old the release is | keep | Live Text can copy it out of a screenshot [S1, S2] |
| S1 "starts from your URL; by default also from sitemaps, certificate logs and Common Crawl" | where URLs come from | change | it says "starts" but never says what you type. Name the command here (must-fix 1) |
| F1 "fetches up to 20 pages at a time from each host; queues their links to …" | the loop's work and its reach | keep | |
| W1 "logged to disk, then saved to redb, in batches" | it saves as it goes | keep | it's why `export-sitemap` works after a kill |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Gap in the track under the loop | the loop has no way out but you | keep | |
| H1, red dotted box | the catch in 0.1.3 and how you know you're done | keep | it's the line I'd screenshot. It goes when 0.1.4 lands |
| C1 "press Ctrl-C once; a second press before `Saved to:` quits without writing the file" | what you do, and what not to do | keep | |
| End bar + `data/sitemap.jsonl` + fields | the file and its real field names | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | his projects feed each other | keep | |
| Night editions | the same | keep | box and track keep their contrast |
| Phone editions (shown at 308 and 278) | the same, in one screen | keep | 26-unit text is about 13.3 px at 308 |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image link + alt text | the route; the alt says install, loop, Ctrl-C, file | keep | |
| Link line (rustmapper · PyPI · Scrapy · Email) | where to go | keep | |
| "Ben Russell builds …" | what he builds | keep | |
| Languages | what he writes in, from the data | keep | |
| Stack | what he builds on | keep | a lookup line, and lookups belong in text |
| Pick sentence | which tool for which job | keep | |
| rustmapper facts line | alive, tested, size, commit, which gates block | keep | |
| rustmapper code block | how to run, stop and recover | change | the two comment groups run together on a phone (must-fix 3) |
| Wheel note | whether `pip` just works on your machine | change (move) | a precondition, printed after the command (must-fix 2) |
| "Before you run 0.1.3:" + seven items | what it does to a server, what it can't see, what the file leaves out, with the flag for each | change (move) | "before you run", printed after the run command (must-fix 2) |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy bullets | what Scrapy does that rustmapper doesn't | keep | |
| Scrapy run paragraph | what `start.py` starts, what it needs, whose URLs `--reset-delta` loads | keep | it states the conditions before its code block, which is the order the rustmapper block should copy |
| Scrapy code block | how to start it and point it at your site | keep | |
| Grafana note | where to look once it runs | keep | |
| Also (four lines) | four more projects, each by what it does | keep | |
| 15 more (folded) | the rest | keep | |
| Working rules 1–4 | how he builds, each with a dated cite | keep | rule 3's 6 and 5 days hold |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn, how it was run, who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **Name the command in the image** (`chart.toml:581` and `:587`, S1's `text` and its `instead`;
   `scripts/data/route.py`, a `{cmd}` placeholder resolved like `{quiet}` at `:183`; one test. About 15 lines.)
   - New S1 text: "`{cmd} crawl` starts from your URL; by default also from sitemaps, certificate logs and Common
     Crawl". The `instead` text gets the same prefix. `{cmd}` is filled by `route_mod.command_name(edition.scripts,
     edition.project)`, the same function the code block uses, so it prints `rust_sitemap` today and `rustmapper`
     by itself once P4 ships a `rustmapper` script. Draw it in the mono face, as H1 draws `Received work item`.
   - Anchor: release `src/cli.rs` contains `Crawl {` (sdist `cli.rs:17`), plus the run check's `crawl_help` step
     ("`rust_sitemap crawl --help` mentions `--start-url`"), which passed today. No script in `edition.scripts`:
     the row keeps today's words, never a guessed command.
   - Size: on the phone S1 goes from two lines to three (about +34 units, 1,087 to about 1,121; the gate is 1,246).
     On the desk it wraps to two lines (543 to about 576; the gate is 620). STRINGS-TWICE stays clean, because the
     only run shared with the code block is two words, "rust_sitemap crawl".
   - Why: the image is what people screenshot and send, and Live Text makes every command in it copyable [S1, S2].
     Today that screenshot gives `pip install rustmapper` and then "starts from your URL" with no command. The
     receiver types `rustmapper` and gets "command not found". Round 2 cut `rust_sitemap crawl --start-url <site>`
     from the image because the code block one screen down has it, and round 9 left that alone because P4 would fix
     it at the source. A screenshot doesn't include the code block, and P4 has been open since round 4. Two mono
     words fix the first mistake a stranger makes, and they fix themselves once P4 lands.

2. **Put the wheel note and "Before you run 0.1.3:" before the code block** (`scripts/render_readme.py:539-545`,
   `install_block`: return `blocks` first, then the fence; tests `tests/test_pipeline.py:495`,
   `tests/test_round9.py:69, :93`, `tests/test_round10.py:110, :236`. About 5 lines of code and 6 test lines. The page
   gets no longer.)
   - New order inside the `install:Rust-sitemap` markers: wheel note, then "Before you run 0.1.3:" and its seven
     items, then the code block. The facts line above and the Scrapy block below don't move.
   - Why: the lead says "Before you run", and it sits after the command, under a copy button. Two of the items carry
     flags you'd add to that command (`--workers 1`, `--seeding-strategy none`), and the wheel note says what you
     need before `pip install` works at all (a Rust toolchain anywhere but Apple silicon on CPython 3.13). Read in
     today's order, you copy, run, then find out what you should have added. Google's procedure rule is to "ensure
     that the reader has the information that they need in order to prepare for the task ahead of time" [S3], and
     Make a README files requirements as a subsection of Installation, not after Usage [S4]. The page already does this for
     Scrapy: its paragraph says what `start.py` starts, that it needs Docker and what `--reset-delta` loads, and only
     then shows the commands. rustmapper should match.
   - The cost, said plainly: on a 390 px phone the rustmapper code block moves about one screen further down. The
     people who reach it are the ones who scrolled to run it. On a phone 80 % of readers don't get past the first
     quarter of a page [S5], and the image already covers that quarter.
   - Test: the install block's first paragraph starts "Prebuilt for", its second is "Before you run 0.1.3:", and its
     last block is the fence. The README-CAUTIONS scope rule doesn't change.

3. **A blank line between the two comment groups in the rustmapper code block** (`scripts/render_readme.py:586`,
   `stop_lines`: add `""` before the kill comment when `out` already holds the stop lines; one test. 3 lines.)
   - Today, at 390 and at 360, the block reads as one four-line comment: "0.1.3 runs until stopped: when / "Received
     work item" stops / for 30 s, then Ctrl-C once / sitemap.xml, even after a kill". The last line belongs to the
     `export-sitemap` command under it, but nothing separates it from the Ctrl-C sentence, so on a phone it reads as
     "Ctrl-C once … sitemap.xml". With a blank line it becomes a caption for the command below it.
   - Google's shell style guide: "Use blank lines between blocks to improve readability" [S6]. The block already
     uses a blank line before "# newer than the release:" when the cargo gate holds, so this follows its own rule.
     Cost: one code line, about 24 px on the phone. No words change and no line gets longer. `tests/test_route.py:421`
     still passes, because the kill comment still sits right above the command.

## Owner, outside this repository (not ranked here)

1. **New evidence: the GitHub bio still reads "Scraping enthusiast and full stack developer"** (live profile, read
   today). On a phone the bio sits above the README, so it's the first line a visitor reads, right before an image
   that says "Crawl and data infrastructure · Python and Rust". The technical plan proposed rewriting it in round 4
   (`docs/crit/tech/MASTERPLAN.md:257`), but its wording had a theme line that was cut since. Use the image's role
   line as it is: "Crawl and data infrastructure. Python and Rust." It takes about 30 seconds in Settings, and it's
   the cheapest fix left on the first screen.
2. **Check on a device:** the GitHub iOS and Android apps. One README author reports that the apps "always return
   the `light` theme" for `prefers-color-scheme` [S7], and GitHub's own docs say only that the `<img>` is used when
   no source matches [S8]. If an app also ignores the `max-width` source, it shows the desk day image (1,280 wide)
   in a phone column, at about 7 px text. GitHub's Mobile docs don't say how READMEs render [S9]. Open the profile
   in the app once. If it shows the desk edition, make the phone day edition the `<img>` fallback.
3. Carried: ship 0.1.4 with a `rustmapper` script (P4), which also makes must-fix 1's word `rustmapper`; commit
   Rust-sitemap's LICENSE (PyPI says MIT and `stats.json` says `license: None`); the rest of round 10's list stands.

## Sources (new this round)

1. [S1] Apple Support, *Copy and translate text from photos on your iPhone or iPad*: "Touch and hold a word and move
   the grab points to adjust the selection", then copy; needs iPhone XS or later with iOS 15.
   https://support.apple.com/120004
2. [S2] Apple, *iPhone User Guide: Interact with text in a photo (Live Text)*: copy or share text in a photo, open a
   website, place a call. https://support.apple.com/guide/iphone/interact-photos-live-text-visual-iph37fdd714b/15.0/ios
3. [S3] Google developer documentation style guide, *Procedures*: "Ensure that the reader has the information that
   they need in order to prepare for the task ahead of time." https://developers.google.com/style/procedures
   (cited in round 10 for another point; quoted here for this rule.)
4. [S4] Make a README: if a project "only runs in a specific context" or has "dependencies that have to be installed
   manually", "add a Requirements subsection" to Installation. https://www.makeareadme.com/
5. [S5] Office for National Statistics service manual, *How people read online*: "80% of users on a phone or tablet
   do not scroll past the first quarter of a release." https://service-manual.ons.gov.uk/content/writing-for-users/how-people-read-online
6. [S6] Google Shell Style Guide: "Use blank lines between blocks to improve readability."
   https://google.github.io/styleguide/shellguide.html
7. [S7] RodrigoTomeES, *prefers-color-scheme-hack*, Limitations: "doesn't work as expected in Github apps (android /
   ios)", which "always return the `light` theme". https://github.com/RodrigoTomeES/prefers-color-scheme-hack
   (cited in rounds 2 and 6 for the colour scheme; used here for the width source.)
8. [S8] GitHub Docs, *Quickstart for writing on GitHub*: the `<img>` is "an image to display in case neither of the
   other images can be matched". https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github
9. [S9] GitHub Docs, *GitHub Mobile*: "Search for, browse, and interact with users, repositories, and
   organizations". It says nothing about how READMEs render. https://docs.github.com/en/get-started/using-github/github-mobile
10. [S10] Pew Research Center, *Teens, Social Media and Technology 2024*: 95 % of US teens have or have access to a
    smartphone. This is why the screenshot is the unit of sharing for my age group.
    https://www.pewresearch.org/internet/2024/12/12/teens-social-media-and-technology-2024/
11. [S11] Nielsen Norman Group, *Scrolling and Attention*: 57 % of viewing time above the fold and 74 % in the first
    two screenfuls (desktop eye tracking; cited in round 1, read again for this round's ordering trade-off).
    https://www.nngroup.com/articles/scrolling-and-attention/
12. [S12] Microsoft Writing Style Guide, *Writing step-by-step instructions*: "Try to fit all the steps on the same
    screen". That's why must-fix 2 moves the prose and keeps the code block whole. (cited in round 3.)
    https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions

Code and data: sdist 0.1.3 (`PKG-INFO` Project-URL; `src/cli.rs:17, :32, :58`; `src/state.rs:285`;
`src/bfs_crawler.rs:433`; `src/main.rs:539`), `assets/stats.json` (`edition`, `repos[]`, `rules`, `figures`,
`runcheck`, `repo_count`), the ideal-url-organizer clone (25 `method_*.py`), `scripts/render_readme.py:506-590`,
`chart.toml:536, :581-591`, the live profile page (bio), and the round-10 renders at 390 and 360.
