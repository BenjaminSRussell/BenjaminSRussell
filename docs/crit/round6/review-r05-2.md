# Review round 5, reviewer 2: the staff engineer screening for data infrastructure

10 Oct 2026. Build looked at: `scratchpad/r6/build/round-04/`, which has the sheet on desk (870) and phone (390), day
and night, and the whole page on desk (screens 1 and 2) and phone (screens 1 to 5). Read: `README.md`, `SPEC.md`,
`LOG.md` (rounds 1 to 4) and the twelve earlier reviews. Nothing that has already been fixed is repeated here. I checked
every figure against `assets/stats.json`, the 0.1.3 sdist (`scratchpad/r6/sdist013`), the Rust-sitemap clone at
`32c2651`, the Scrapy clone at `96e7a1a` and the run-check logs.

How I read it: I screen GitHub profiles for data-infrastructure hires. I look on my phone between meetings first. If
the phone gets me interested, I look again on a laptop. I give the first screen about ten seconds. On the laptop I
open one thing to check that the claims hold up.

Verdict: **not yet. 7 / 10.** I would not ship it as it is.

## The first question: does it meet the owner's goal?

Mostly, yes. On the phone, in ten seconds, I get the name and "crawl and data infrastructure". I get a project with a
one-line job ("Crawls a site and writes one line for every page it reaches"). Then I get a top-to-bottom run of that
project: how you get it, where URLs come from, what repeats for every page, the catch, how you stop it, the file you
end up with, and which of his other projects reads that file. Nothing has a size. No word names the theme. A list
couldn't show the loop bracket, and a list wouldn't make me look at the catch at the step where it happens. The
picture teaches me something true about his work faster than the text does. That is the goal, and it is met in form.

Three things stop me, and two of them are specific to the people this profile is for.

1. **What a screener takes away is "his flagship never stops".** The only colour on the page that isn't the track is
   the red dotted line around "never stops by itself". Colour that differs from everything around it is seen
   before anything else, whatever else is on the screen (Healey and Enns [1]). Nothing on the page says this is a
   bug in an 11-month-old release that main has already fixed, with a regression test. The evidence for that is
   measured, not claimed. `tests/crawl_exits_when_idle.rs` exists at `32c2651`, and its doc comment says it is the
   "Regression test for #65: a crawl must exit on its own once the site is exhausted". CI's
   `Test (ubuntu-latest, stable)` job runs `cargo test --all-features` (`.github/workflows/ci.yml:76`), and on that
   sha it passed on 7 Oct 2026 (`repos[Rust-sitemap].ci`, `head_sha` = `head.sha`). Round 3 declined the "main has
   fixed it" sentence because "without a measured run the sentence would be a claim". A passing CI test on the
   drawn sha is a measured run, by the project's own CI, and the facts line already trusts that same CI for "CI
   passed 7 Oct 2026". To someone hiring, "found the bug, wrote the regression test, release pending" is one of the
   best things a profile can show. Right now the page shows only the first half. The owner has asked for a 0.1.4
   twice. Until it ships, the page can still say what main does. The usual way to do that is an "Unreleased" note
   [9].

2. **The data-infrastructure part is the quietest thing in the image, and one cite about it is wrong.** For my
   hire, the two signals in rustmapper are the write path and the backpressure. The writer appends each batch to a
   write-ahead log and fsyncs it before committing to redb (`sdist:src/writer_thread.rs:122-167`, the same order at
   HEAD `:136-181`). That is the WAL rule as PostgreSQL states it: changes are written "only after those changes
   have been logged" [3]. The governor reduces fetch permits when the average redb commit time goes over 500 ms
   (`sdist:src/main.rs:90-123`). That is backpressure in its textbook form: the slow consumer tells the producer to
   slow down [5]. The image renders the first as "saved to its database every 50 ms", which describes any program,
   and the second in `ink2`, the lightest text on the sheet. Meanwhile working rule 2 cites "rustmapper, Nov 2025,
   the write-ahead log" as a raw layer that "is appended to and never overwritten". At `32c2651` that is false.
   `WalWriter::checkpoint()` is "Truncate the whole log", and `on_commit` runs it by default every 64 commits or at
   64 MiB (`src/wal.rs:165-166, 249-270`). A WAL is a durability buffer, not a raw layer. Anyone who has run a
   database will catch this in the one paragraph they read closely.

3. **The page doesn't pass its own gate.** `check.py --tier fast` still fails ROUTE-UNVERIFIED on S2 (P1 isn't at
   HEAD; `routes.rustmapper.entries[S2].missing`). I don't add it as a must-fix again, because it is an owner action
   and was ranked and declined twice. But under the build's own rules, this doesn't go to `main` until that gate is
   green.

Smaller problems: the pick sentence holds back both project names until the end of its clauses, and the Grafana
note's bare `http://localhost:3000` becomes a link that goes nowhere for every visitor.

## Figures checked

| Printed | Source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `edition.date` | 0.1.3, 2025-11-08 | yes |
| `pip install rustmapper` → `rust_sitemap` | `edition.scripts` | `["rust_sitemap"]` | yes |
| `seeder.rs`, `bfs_crawler.rs`, `writer_thread.rs` | sdist `src/` listing | all three present | yes |
| your URL, plus by default sitemaps, certificate logs, Common Crawl | `routes` S1, release scope; sdist `cli.rs` `default_value = "all"` | verified | yes |
| fetches a page; queues links on your URL's domain, above or below it | sdist `url_utils.rs:81-91`, `frontier.rs` `start_url_domain` | parent and child domains of the start, at a dot boundary | yes |
| fetches fewer pages at once when saving falls behind | sdist `main.rs:90-123` (500 ms EWMA up, 100 ms down, 32 to 512 permits) | verified | yes; the measure is left out (must-fix 4) |
| saved to its database every 50 ms | sdist `writer_thread.rs:11` `BATCH_TIMEOUT_MS = 50`, `MAX_BATCH_SIZE = 5000` | at most 50 ms per batch | yes, but it leaves out the WAL (must-fix 3) |
| never stops by itself; done when `Received work item` lines stop | sdist `bfs_crawler.rs:433` (`eprintln!`, so printed at every log level); runcheck `quiet_after_last_page`; `rc2/work/crawl.log` | three lines for three URLs, then silence | yes for 0.1.3; fixed at HEAD by test (must-fix 2) |
| press Ctrl-C once to write `data/sitemap.jsonl`; after a kill, `export-sitemap` → `sitemap.xml` | `crawl.log` ("Press Ctrl+C again to force quit", "Saved to: …/sitemap.jsonl"); `export_after_kill` 3 `<loc>` | | yes |
| fields: `url, depth, status_code, title, …` | `SitemapNode`, both trees | | yes |
| sorted by ideal-url-organizer, with a test | `handoffs[0]`, `to_sha` `159968a` | runs | yes |
| 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust · `32c2651` | `repos[Rust-sitemap]` | 176; success, 2026-10-07, 7 jobs; 16,390; head `32c2651` | yes |
| 1,920 tests · CI passed 8 Oct 2026 · MIT license · 69k lines of Python · `96e7a1a` | `repos[Scrapy]` | 1,920; success, 2026-10-08; MIT; 69,036 | yes |
| 20 per host, 256 in all, no pause unless `Crawl-delay` | `routes` L1 | verified | yes |
| 22 public repositories; 15 more | `repo_count` | 22; 22 − 1 − 2 − 4 = 15 | yes |
| 45 of rustmapper's 146; 71 of Scrapy's 499 | `repos[].others` (bot), `all_hands` | Claude 45 / 146; jules 49 + Claude 22 = 71 / 499 | yes |
| Rule 2: "rustmapper, Nov 2025, the write-ahead log" for "appended to and never overwritten" | `rules[wal]` 4334458, 2025-11-03; HEAD `src/wal.rs:249` `checkpoint()` = `truncate(0)`, default every 64 commits | the month holds; the claim does not | **no** (must-fix 1) |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page this is | keep | |
| Role line, two caps lines | crawl and data infrastructure, Python and Rust | keep | the drawing under it backs up "crawl". Must-fixes 3 and 4 make it back up "data infrastructure" too |
| Desk file labels in the left column | which file to open to check each step | keep | true (sdist listing) and right for an engineer. `seeder.rs` sits about 9 px under "PYTHON AND RUST" and reads for a moment as part of the title block. That's acceptable, no change |
| "rustmapper" + "Crawls a site and writes one line for every page it reaches." | which project and what it does | keep | the best ten words on the page |
| Start bar | where you begin | keep | |
| `pip install rustmapper` | the way in | keep | |
| "0.1.3 · 8 NOV 2025" | the age of what pip gives you | keep | |
| Magenta track | one way through, read top to bottom | keep | |
| Stop rings | a step the tool takes | keep | |
| S1 seeds | URLs come from more than links, and by default it calls outside sources | keep | CT logs as a seed source is a clever choice, and a screener notices it |
| F1 fetch and scope | the crawler loop and how wide it reaches | keep | "above or below it" was settled in round 4 |
| G1 governor note | the crawl slows when saving lags | change | the one design idea that is his and unusual, set in the lightest ink with no measure. Full ink, with its 500 ms (must-fix 4) |
| W1 "saved to its database every 50 ms" | it saves as it goes | change | "its database" says nothing. The write path is a WAL with fsync, then redb (must-fix 3) |
| Loop bracket and up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Gap in the track under the loop | the loop has no exit but Ctrl-C | keep | it closes by itself when a release ends on its own |
| H1 in the dotted danger line | the catch, at the step where it bites | change | true, but it reads as the project's flaw and not the release's. Name the release in the row (must-fix 2) |
| C1 Ctrl-C and the kill recovery | the one thing you do, and the way back | keep | it matches the tool's own "Press Ctrl+C again to force quit" |
| End bar | where you end up | keep | |
| `data/sitemap.jsonl` + fields | what you get, in the struct's own words | keep | |
| Hand-off arrow + "sorted by ideal-url-organizer, with a test" | his projects feed each other, and the join is tested | keep | |
| Night editions | the same | keep | contrast holds. The red reads less loud at night, which is fine |
| Phone edition | the same, without file labels | keep | reads at 390 with no squinting. G1's line is the longest and still fits |
| Link round the image to Rust-sitemap | a tap lands on the project | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image | above | change | must-fixes 2, 3, 4 |
| Alt text | the same in 25 words | keep | |
| Link line | where to go | keep | |
| Builds / Languages / Stack | what he builds and with what | keep | |
| Pick sentence | which tool for which job | change | the names come last in both clauses (must-fix 5) |
| rustmapper sentence | what it is; the API isn't released | keep | |
| rustmapper facts line | alive, tested, size, which snapshot | keep | |
| Install code block | how to run and stop it | keep | the round-4 Ctrl-C comment is right |
| Wheel note | when pip just works | keep | |
| Load and 50,000 note | what it does to someone else's server; the sitemap limit | keep | then add the "main exits by itself" sentence after it (must-fix 2) |
| Scrapy sentence and facts line | the second tool, measured | keep | |
| Scrapy code block | how to start it | keep | long, but every comment prevents a real failure |
| Grafana note | where to look once it runs | change | the bare URL is autolinked [7] to the visitor's own localhost (must-fix 6) |
| Scrapy bullets | how it's built: Delta Lake, MinHash, local summaries, Prometheus, breakers | keep | the strongest data-infrastructure evidence on the page |
| Also | the next four | keep | |
| 15 more | the rest | keep | |
| Rule 1 Boring under load | his stance, dated by his own commit | keep | |
| Rule 2 Raw before clean | his stance | change | the rustmapper half of the cite is false at HEAD (must-fix 1) |
| Rule 3 Dashboards before speed | his stance | keep | rustmapper main has a Prometheus `/metrics` too (`582e8d7`), so the flagship is consistent with it |
| Rule 4 Parse, don't pattern-match | his stance | keep | "Claude's commit used it first" is honest. It weakens the rule as his own, but cutting it is the owner's call |
| Found a mistake? | the page can be corrected | keep | |
| Data line | what was checked and run | keep | about 85 words in `<sub>`, nine lines on a phone. Nobody screening reads it, and that's fine: it's there for the one who checks |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **Take the WAL out of rule 2's cite** (`chart.toml [[notices]]` rule 2 anchors, `data/proof.py`; 2 lines and a
   test).
   - Drop "rustmapper, Nov 2025, the write-ahead log" from the cite. It reads "*Scrapy, Oct 2025, the Delta Lake
     tables.*"
   - Add a NOTICE-ANCHORS case so that no rule 2 anchor can point at `wal.rs`.
   - Why: at `32c2651` the WAL is truncated to zero by default every 64 commits (`src/wal.rs:165, 249-270`). A WAL
     is the opposite of a raw layer that is "never overwritten". It is the page's one factual error, and it sits in
     the paragraph a data engineer reads most closely. The WAL is still worth showing, in the image, where it is
     true (must-fix 3).

2. **Say what main fixed, and tie the trap to its release** (`chart.toml [route.rustmapper]`, new text entry M1 and
   H1's wording; `render_readme.py` `install:Rust-sitemap`; about 25 lines and three tests).
   - (a) H1 becomes "`{release}` never stops by itself; done when `Received work item` lines stop". On the desk
     that is one line, about 735 of 870 px. On the phone it stays two lines: "0.1.3 never stops by itself; done
     when" and "`Received work item` lines stop". The fallback wordings take the same prefix.
   - (b) Add a new text entry M1, printed after the load and 50,000 sentence: "On main, a crawl stops by itself
     once the site runs out of pages: `tests/crawl_exits_when_idle.rs` passes in CI at `32c2651`. That fix is not
     on PyPI yet."
     - Head anchor: `tests/crawl_exits_when_idle.rs` contains `fn crawl_exits_after_frontier_drains`.
     - Gate: `repos[Rust-sitemap].ci.conclusion == "success"` and `ci.head_sha == head.sha`, and the job list
       contains a job whose name starts with `Test`.
     - Probe: `ends_by_itself` failed for the release, so M1 retires together with H1.
   - (c) Print no idle timing. The test runs with `--idle-plateau-secs 1 --idle-grace-secs 1`, and the defaults are
     30 and 60 (`src/cli.rs:130, 137`).
   - STRINGS-TWICE passes: the only run shared with the image is "stops by itself", 3 words with no code token.
   - Tests: M1 is not printed when CI's `head_sha` differs from `head.sha`, or when the test file is missing; H1
     names `edition.version`.
   - Why: the red line is the first thing anyone sees [1], and recruiters use the signals that are cheapest to
     check. This turns the loudest line from "broken" into "found, tested, release pending", using only facts the
     build already trusts. A release note keeps its "Unreleased" section for exactly this [9].

3. **W1 names the write path** (`chart.toml` W1; about 6 lines).
   - Text: "logged to disk, then saved to redb, every 50 ms" (47 characters; one line on desk and phone, shorter
     than G1).
   - Anchors, in both trees: in `writer_thread.rs`, `wal.append(&record)` / `wal_writer.append(&record)` and
     `fsync()` come before `state.apply_event_batch(&batch)`. Keep `const BATCH_TIMEOUT_MS = 50` and `use redb::`
     in `state.rs`.
   - Test: an order anchor fails if `apply_event_batch` comes before `fsync` in the function body.
   - Why: "its database" teaches nothing. A WAL with fsync before the commit is the most standard data-infrastructure
     idea there is [3, 4]. It is in the code, and it explains why "after a kill, export-sitemap" works. The Stack
     line already names redb, so the image confirms the Stack line instead of repeating it.

4. **G1 at full weight, with its measure** (`route.py` G1 colour; `chart.toml` G1; about 8 lines and a test).
   - Text: "fetches fewer pages at once when saves average over 500 ms".
   - Scope: release, with a value anchor `{const:THROTTLE_THRESHOLD_MS}` in sdist `src/main.rs` (500.0, printed
     without the decimal). HEAD uses 2,000 ms, set through `GOVERNOR_THROTTLE_THRESHOLD_MS`, so like L1 this is a
     fact of the release.
   - Set it in `ink`, not `ink2`, still as F1's last line with no mark. On the phone it is about 596 units wide,
     inside the 600 measure. If typeset says it overflows, use "when a save averages over 500 ms".
   - Test: the printed number follows the constant, and G1's fill equals F1's.
   - Why: this is backpressure from the store to the fetchers [5]. It is the one design choice on the sheet that
     tells a screener he thinks about the storage side. A design fact without a number is a claim. With the
     threshold it becomes a mechanism you can check.

5. **The pick sentence starts with the names** (`chart.toml [copy] pick`; 1 line).
   - Text: "**rustmapper** lists a site's URLs from one binary with no services to run. **Scrapy** keeps the pages
     themselves, deduplicated and summarised, in a pipeline that needs Docker."
   - The same gates apply (`no_services`, the three `use = "pick"` figures).
   - Why: readers fix on the first words of a line [F-pattern, cited in r01-2]. Today the first words are "For the
     list of", and both names come last.

6. **Grafana's address as code, not a link** (`chart.toml` / the Scrapy note; 1 line).
   - Text: "Grafana opens on `localhost:3000`."
   - Check that the FIGURES row still matches inside a code span.
   - Why: GitHub turns a bare URL into a link [7], so this one sends every visitor to their own machine's port
     3000.

Owner note (not in this repository and not ranked): the project has three names. The image says rustmapper, the
command is `rust_sitemap`, and a tap lands on `Rust-sitemap`. Renaming the repository to `rustmapper` costs a minute,
and GitHub redirects the old URLs. Pinning it first makes the profile's Pinned card match the image [8].

## Sources (new this round)

1. C. G. Healey and J. T. Enns, "Attention and Visual Memory in Visualization and Computer Graphics", *IEEE TVCG*
   18(7), 2012: a target with a unique hue "pops out", and finding it doesn't depend on how many distractors there
   are. https://www.csc2.ncsu.edu/faculty/healey/download/tvcg.12a.pdf
2. A. Trockman, S. Zhou, C. Kästner, B. Vasilescu, "Adding Sparkle to Social Coding: An Empirical Study of
   Repository Badges in the npm Ecosystem", ICSE 2018: build and test signals on a repository are mostly reliable
   and correlate with more tests. https://www.cs.cmu.edu/~ckaestne/pdf/srcicse18.pdf (supports trusting a CI-passed
   test as evidence, must-fix 2)
3. PostgreSQL documentation, "Write-Ahead Logging (WAL)": data changes are written "only after those changes have
   been logged". https://www.postgresql.org/docs/current/wal-intro.html
4. redb documentation, `Durability`: an `Immediate` commit is "guaranteed to be persistent as soon as
   `WriteTransaction::commit` returns". https://docs.rs/redb/latest/redb/enum.Durability.html
5. Conduktor, "Backpressure handling in streaming systems", and Dagster, "Data backpressure": the slow consumer
   signals the fast producer upstream to slow down. https://conduktor.io/glossary/backpressure-handling-in-streaming-systems ;
   https://dagster.io/glossary/data-backpressure
6. F. L. Schmidt and J. E. Hunter, "The Validity and Utility of Selection Methods in Personnel Psychology",
   *Psychological Bulletin* 124(2), 1998: work samples are among the strongest predictors. A runnable route with real
   file names works as a work sample, which is why the image's form suits a hiring reader.
   https://stafforini.com/works/schmidt-1998-validity-and-utility/
7. GitHub Docs, "Autolinked references and URLs": GitHub "automatically creates links from standard URLs".
   https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls
8. GitHub Docs, "Pinning items to your profile": pins exist "so other people can quickly see your best work".
   https://docs.github.com/en/enterprise-server@3.18/account-and-profile/how-tos/profile-customization/pinning-items-to-your-profile
9. Keep a Changelog 1.1.0: "Keep an `Unreleased` section at the top to track upcoming changes", so people can see
   what's coming. https://keepachangelog.com/en/1.1.0/
10. F. Calefato, L. Quaranta, F. Lanubile, "A Lot of Talk and a Badge", 2023. Its summary of Marlow and Dabbish
    (CSCW 2013) says employers looked only at "activity traces that are easy to verify quickly".
    https://arxiv.org/abs/2303.14702

From the clones and records:
- Rust-sitemap `32c2651`: `tests/crawl_exits_when_idle.rs` (doc comment, `--ignore-robots`, idle flags 1 s);
  `.github/workflows/ci.yml:76`; `src/wal.rs:165-166, 176-187, 249-270`; `src/writer_thread.rs:136-196`;
  `src/orchestration/governor.rs:16-34`; `src/cli.rs:130, 137`.
- Sdist 0.1.3: `src/writer_thread.rs:11-12, 122-180`; `src/main.rs:84-151`; `src/bfs_crawler.rs:433`;
  `src/url_utils.rs:81-91`.
- `scratchpad/r6/rc2/work/crawl.log`. `assets/stats.json`: `edition`, `repos`, `routes`, `handoffs`, `rules`, `ci`.
