# Review round 1, reviewer 3: does the route actually work?

9 Oct 2026. Reviewer: systems engineer, checking every claim against the code and against the running binary.
Looked at: `scratchpad/r6/build/round-00/` (desk and phone, day and night; whole page on desk and phone),
`README.md`, `SPEC.md`, `review-r01-1.md`. I agree with most of reviewer 1's findings and don't repeat them. This
review adds the one test nobody had run yet: **I followed the image's directions and ran the tool.**

Verdict: **does not meet the goal. 4 / 10.** I would not ship it as is.

## The first question: does it meet the owner's goal?

The form is finally pointed at the right target. The image says what rustmapper is, how to start it, what goes
wrong, and where the output goes. Nothing has a size, nothing names the theme, and it reads on a phone. That's real
progress since the islands.

But a set of directions has one job: when a stranger follows it, they get where it says they will. I followed it,
with the version it tells you to install (0.1.3, the same binary the `runcheck` built), and two of its five route
lines aren't true for that version:

1. **"resume picks up after a kill" is false for 0.1.3.** `rust_sitemap resume` fails every time, after a clean
   Ctrl-C, after `kill -9` and after SIGTERM, with
   `Error: Crawler("Database creation error: Database already open. Cannot acquire lock.")`. The cause is in
   `sdist:src/main.rs:642`: the resume handler opens `CrawlerState` (redb, which takes an exclusive file lock) and
   then calls `build_crawler`, which opens it again at `:180` without dropping the first handle. It was fixed at HEAD
   in #30 ("drop(state)" with the comment "otherwise resume always failed", `src/main.rs` near the Resume handler),
   closed 7 Oct 2026. It isn't released. I built HEAD (32c2651) and checked: after `kill -9`, `resume` works and
   rewrites `sitemap.jsonl` with all 3 pages.
2. **The crawl never finishes on its own in 0.1.3, and the image hides that.** On the three-page fixture site
   (`tests/fixtures/route-site/`), all three pages are fetched in under a second. The process was still running at
   150 s and had written no `sitemap.jsonl`. Issue #65 (closed 7 Oct 2026, not released) names the cause: the
   completion check sits in the `else =>` arm of `tokio::select!`, which only runs when *every* branch is disabled,
   and the `work_rx.recv()` branch never is (`sdist:src/bfs_crawler.rs:427-556`). The tokio docs confirm `else` runs
   only when all branches are disabled. The `runcheck` passes only because it sends SIGINT at 45 s. So H2, "written
   when the crawl stops: press Ctrl-C once, not twice", reads as if the crawl stops. For pip users it never does. The
   real directions are "it never finishes by itself: when pages stop coming, press Ctrl-C once."
3. **A kill sends SIGTERM, and SIGTERM writes nothing.** `timeout`, `docker stop` and systemd all send SIGTERM. With
   SIGTERM the 0.1.3 process dies with no `sitemap.jsonl` (I checked with `timeout 150`). What survives in both
   versions is the database: `export-sitemap --data-dir d` after a `kill -9` wrote all 3 URLs with 0.1.3 and with
   HEAD. That's the true durability line, and it's useful.

**Why the checks missed it.** Each route entry is "verified" by finding strings in files (SPEC §5.3). S4's anchors
are `"[u32 len][u32 crc32c][u128 seqno][payload]"` in `wal.rs` and `"Resume {"` in `cli.rs`. Both are there, and the
feature is broken. The header "Crawls a site and writes one line for every page it reaches" is anchored to
`pub fn is_same_domain`, a scope check that doesn't back the sentence. A string in a file shows the code exists, not
that it works. The data line under the page then promises more than that: "a stop or a trap is drawn only while the
code it describes is found in both." That is the owner's old complaint, "the data doesn't look exactly accurate", in
a new form. It looks verified and isn't.

**What this means for the goal.** The owner asked, "How does it help the user see my project?" Today it helps a
stranger install a release that hangs, with a promise of crash recovery that fails. A route that strands the person
who follows it is worse than islands, because islands at least didn't promise anything. And the most useful true
thing about this project isn't on the page anywhere: **the released 0.1.3 is eleven months old, and the code on
`main` behaves differently in four ways a user hits in the first minute** (table below). That gap between the
edition and the corrections is the thing a real chart prints in its margin. Every chart carries its edition date and
its last correction, and "old or uncorrected charts should never be used for navigation." The image prints
"0.1.3 · 8 NOV 2025" and "CODE 32c2651 · 7 OCT 2026" a few centimetres apart and never says that they differ, or how.

| Behaviour a stranger meets in the first minute | 0.1.3 (what `pip install` gives) | `main` at 32c2651 | How I checked |
|---|---|---|---|
| Crawl ends when the pages run out | **never**; waits until Ctrl-C (#65) | yes, 90 s after the last new URL (30 s plateau + 60 s grace, `--idle-plateau-secs`, `--idle-grace-secs`) | ran both on the 3-page fixture |
| `resume` after a kill | **always fails**, "Database already open" (#30) | works, 3/3 pages | ran both, after `kill -9` |
| Site whose robots.txt is a 404 | crawls ("missing robots.txt … allowing crawl") | **fetches nothing**: "deferring … until robots.txt is fetched", exits at 90 s with `processed 0` (P1) | ran both, no `--ignore-robots` |
| Default seeding | `all` (contacts crt.sh and the Common Crawl index on your behalf) | `none` | `sdist:src/cli.rs:57`, `src/cli.rs:53` |
| `sitemap.xml` at the end of a crawl | not written (separate command) | tries and warns "Failed to export XML sitemap: Database already open"; `export-sitemap` afterwards works | ran HEAD |
| `export-sitemap` after `kill -9` | works, 3 `<loc>` | works, 3 `<loc>` | ran both |

The fourth row matters too. The image's S1 says "plus seeds from sitemaps, CT logs, Common Crawl" as if that's
optional. For a pip user it's the default: their first crawl of their own site queries crt.sh and Common Crawl
without being asked.

Neither version gives a stranger a clean route today. 0.1.3 hangs. HEAD won't crawl a site without a robots.txt,
which is most small sites. That's why the owner action ranked first below (land P1, release 0.1.4 from HEAD) does more
for the image than any drawing change. Until then, the image must draw only what the release really does, gated on
running it.

## Figures checked against `assets/stats.json` and the clones

| Figure on the image or page | Key / source | Value | Holds |
|---|---|---|---|
| 21 repositories | `repo_count` | 21 | yes |
| 32c2651 · 7 Oct 2026 | `repos[Rust-sitemap].head` | `32c26519…`, 2026-10-07; clone `git log -1 --format='%H %cs'` matches | yes |
| CI on main passed 7 Oct 2026 | `repos[Rust-sitemap].ci` | success, 2026-10-07, last 5 all success | yes |
| As of 9 Oct 2026 | `taken` | 2026-10-09 | yes |
| 0.1.3 · 8 Nov 2025 | `edition.version`, `.date`; PyPI JSON | 0.1.3 uploaded 2025-11-08 19:52:41, the fourth release within 74 minutes | yes |
| prebuilt for macOS arm64 + Python 3.13 | `edition.wheels`; PyPI JSON | one wheel, `cp313-cp313-macosx_11_0_arm64`, plus sdist | yes |
| `rust_sitemap crawl --start-url` | `edition.scripts`; `rust_sitemap --help` from the built 0.1.3 | `crawl`, `resume`, `export-sitemap` | yes |
| fields url, depth, status_code, title | `SitemapNode`; real output | 0.1.3 writes `schema_version` 1, HEAD writes 5, and both carry those four | yes |
| fewer fetch workers when redb commits lag | `sdist:src/main.rs:84-140` | semaphore permits 32–512, one taken per 250 ms while the commit EWMA is over 500 ms | mechanism yes (see r1 on "requests in flight") |
| logged before stored | `sdist:src/writer_thread.rs:110-160` | WAL append + fsync before the redb commit, truncated after | yes |
| resume picks up after a kill | run | **fails in 0.1.3** | **no** |
| written when the crawl stops | run | 0.1.3 never stops by itself | **misleading** |
| 176 tests | `repos[].test_functions` | 161 Rust attributes + 15 Python `def test_` at HEAD | yes, counted at HEAD, not in the release |
| 16k lines of Rust | `repos[].lines.Rust` | 16,390 | yes |
| 1,920 tests, 69k Python (Scrapy) | `repos[Scrapy]` | 1,920; 69,036 | yes |
| hand-off to ideal-url-organizer, with a test | `handoffs[0]` | `runs`; 15 reader fields, a subset of both writer sets | yes |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| T1 Ben Russell | whose page | keep | |
| T2 role line | what he builds | keep | |
| T3 "1 of 21 (public) repositories" | this is one chosen project | keep | one wording on both editions (r1) |
| T4 "CODE 32c2651 · 7 OCT 2026" | when the code was last changed | change | its only real job is to set the code against the release, and it doesn't. Turn it into the correction line (must-fix 4) |
| T5 "CI on main passed 7 Oct 2026" | main's tests pass | change | true, but it describes `main`, while the route installs 0.1.3. Put it on the same line as the code date so it's clearly about `main` |
| T6 "AS OF 9 OCT 2026" | when the build read it | change | fold it into the data line (r1) |
| R0 rustmapper + sentence | what it is | change | keep the sentence, but anchor it to the export code (`fn export_jsonl` / `sitemap.jsonl` join), not `is_same_domain` |
| R1, R12 bars | start and end | keep, conditionally | they earn a place only once the end is reached by the route as drawn. Today, for 0.1.3, it isn't without Ctrl-C |
| R2 `pip install rustmapper` + 0.1.3 date | how to get it | change | the date is the edition. Pair it with what's corrected since (must-fix 4) |
| R3 `rust_sitemap crawl …` | the real command | keep | it runs |
| R4 platform note | whether pip just works | keep in text only | r1 must-fix 1 |
| R5 track | read in order | change | r1 is right that it's a list. It gets a real job if a measured figure sits on it (must-fix 2 gives one: "ends 90 s after the last page" or "never ends") |
| S1 seeders | where URLs come from | change | say the default: "seeds from sitemaps, CT logs and Common Crawl by default (0.1.3)" / "if asked (main)", from `cli.rs` `default_value`, gated per version |
| H1 scope trap | big sites are crawled whole | change | merge with the stop trap (r1 must-fix 3) |
| S3 governor | it slows when it can't save | keep | true in both; wording per r1 |
| S4 WAL + resume | a crash doesn't lose the crawl | **cut the resume clause now** | false for the release. Replace with "a kill keeps the pages: export-sitemap still writes sitemap.xml", tested in both (must-fix 1, 3) |
| H2 Ctrl-C trap | the file appears only after Ctrl-C | change | the true trap is that 0.1.3 never stops, and that SIGTERM writes nothing (must-fix 2) |
| hatch marks | "danger here" | keep | only while each stands for a measured failure |
| rings | "a stop" | change | r1: they carry nothing on the phone |
| R13 `data/sitemap.jsonl` + fields | what you get, real field names | keep | verified in output from both versions |
| R14 export-sitemap | second output | change | merge into the new S4 line, where it's the recovery move, and drop it as a separate row |
| R15 read by ideal-url-organizer | his projects connect, tested | keep | holds. Drop the README repeat (r1) |

## Every block of the page

| Block | Verdict | Why |
|---|---|---|
| Image | change | above |
| Alt text | change | "two traps are marked" stays true only while the trap count comes from verified entries. Keep it built from `routes` |
| Link line | keep | |
| Builds / Languages / Stack | keep | |
| rustmapper sentence | change | add what decides which one to run: "0.1.3 on PyPI, 8 Nov 2025; `main` has since fixed resume and the crawl's exit (both unreleased)". Generated from `routes` (must-fix 4) |
| Facts line (176 tests, CI passed) | change | both describe `main`, not the release you're told to install. Say "on main" |
| rustmapper code block | change | on the phone, line 3 is cut at `--data-dir ./d` (`page-phone-2.png`). Rewrap so no line is over 38 characters. Add the Ctrl-C step as a comment, because that's the step 0.1.3 needs |
| Wheel note | keep | |
| Governor / seeds bullets | change | per r1. The seeds bullet should say it's the default in 0.1.3 |
| Hand-off sentence | change | per r1 |
| Scrapy block | change | on the phone both comments are cut off ("# from the clone r", "# the whole pipeli"), so the one warning in the block is invisible where most visitors read. Put each comment on its own line above its command |
| Scrapy bullets, Also, 15 more | keep | |
| Working rules | keep | rule 2 cites "rustmapper, Oct 2025, the write-ahead log". The WAL is real, but the recovery it exists for didn't work in the release. The rule is still true as a rule, so leave it |
| Data line | change | "a stop or a trap is drawn only while the code it describes is found in both" overclaims. After must-fix 1, say "every line on the route was run against 0.1.3 on <date>, <runner>" |
| License | keep | |

## Must fix, ranked

1. **Gate every route line on running it, not on finding strings.** Extend `scripts/runcheck.py` (about 60 lines)
   with three steps on the fixture site, each recorded in `steps[]` with `secs` (from `time.monotonic()`):
   - `ends_by_itself`: `crawl` with no signal, up to 150 s. Record `ok` and the exit time.
   - `resume_after_kill`: `crawl`, `kill -9` at 4 s, then `resume` with SIGINT at 30 s. Pass if `sitemap.jsonl`
     has 3 lines.
   - `export_after_kill`: `crawl`, `kill -9` at 4 s, then `export-sitemap`. Pass if there are 3 `<loc>`.

   In `chart.toml`, give each `[[route.rustmapper.entry]]` a `runs = ["<step id>"]` list. `scripts/data/route.py`
   marks an entry unverified when any of its steps failed, and ROUTE-UNVERIFIED already fails the build. String
   anchors stay as a second check. Today's result for 0.1.3: `ends_by_itself` false, `resume_after_kill` false,
   `export_after_kill` true. Test: a `tests/test_route.py` fixture where the step fails must yield an undrawn entry.
   *Why:* the owner's "the data doesn't look exactly accurate", and S4 being false right now.
2. **Replace H2 with the stop behaviour as measured.** When `ends_by_itself` fails: "never finishes by itself: when
   new pages stop, press Ctrl-C once; that writes the file. A kill writes nothing." When it passes: "stops <secs> s
   after the last new page; Ctrl-C once ends it sooner." Both strings come from runcheck, so the figure is measured
   (that's the measure on the track r1 asked for). Merge in r1's scope clause so there's one hazard, not two.
   *Why:* it's the first thing a pip user hits, and the current line implies the opposite.
3. **Replace S4 with what holds in both:** "`wal.rs` — logged before stored; after a kill, export-sitemap still
   writes sitemap.xml". Gate on `export_after_kill`. Drop R14 as a separate row. Bring "resume" back only when
   `resume_after_kill` passes for the released version.
4. **Say how the edition differs from the code on `main`.** Desk title block, one muted line in place of T4 and T6:
   "0.1.3 ON PYPI · MAIN 32c2651 · 7 OCT 2026 · CI PASSED". Under the rustmapper sentence in the README, one sentence
   generated from the runcheck run against both builds (add a HEAD leg to runcheck: `cargo install --git … --rev
   <head.sha>`, about 5 min on the runner): "`main` has since fixed `resume` and the crawl's exit; neither is
   released." It prints nothing once the release passes the same steps. *Why:* it's the most useful true fact about
   the project, and it's what a chart's margin is for.
5. **Owner actions, the highest value of anything here (outside this repository):** land P1 (I confirmed it by
   running HEAD: no robots.txt → "deferring … until robots.txt is fetched", `processed 0`, exits at 90 s). Fix the
   end-of-crawl XML export at HEAD ("Failed to export XML sitemap: Database already open": the same double-open
   pattern as #30, in `finish_crawl`). Then release 0.1.4 from HEAD. After that, items 2 to 4 shrink to one working
   route with a measured stop time, which is the image the spec meant to draw.
6. **Phone code blocks:** no line over 38 characters in either block, and the Scrapy comments on their own lines.
   Add a render check: on a 390 px viewport, every `pre` has `scrollWidth <= clientWidth`.
7. **Anchor the header to what it says:** replace `header_anchors` (`is_same_domain`) with the JSONL export function
   at both trees, plus the runcheck's 3-line output.
8. **S1 says the default:** wording per version from `cli.rs` `default_value` ("by default" for `all`, "if asked"
   for `none`). The stranger's first crawl contacts two third-party services, and they should know that.

## Sources (fresh this round)

The shared web-search budget for this run was already used up, so these were fetched directly by URL or read from
the clones and from runs I made in `scratchpad/r01-3/`.

1. tokio, `select!` macro docs: `else` "evaluates if none of the other branches match", and runs only once all
   branches are disabled: https://docs.rs/tokio/latest/tokio/macro.select.html
2. Rust-sitemap issue #65, "Crawl never exits after the frontier drains (completion check unreachable in select! else
   arm)", closed 2026-10-07 (GitHub REST `repos/BenjaminSRussell/Rust-sitemap/issues/65`).
3. Rust-sitemap issue #30, "Persist frontier state for crash recovery between crawls", closed 2026-10-07 (REST).
4. Rust-sitemap issue #47, "frontier.rs handle_robots_check: crawls a host before its robots.txt arrives…", closed
   2026-10-07 (REST). This is the fix that introduced the fail-closed path behind P1.
5. redb `DatabaseError::DatabaseAlreadyOpen`: "The Database is already open. Cannot acquire lock.":
   https://docs.rs/redb/latest/redb/enum.DatabaseError.html
6. PyPI JSON for rustmapper: four releases on 8 Nov 2025 within 74 minutes, one wheel (cp313 macOS arm64) plus sdist,
   no later release: https://pypi.org/pypi/rustmapper/json
7. Keep a Changelog 1.1.0, the "Unreleased" section, so "people can see what changes they might expect":
   https://keepachangelog.com/en/1.1.0/
8. maturin, *Distribution*: Linux wheels need manylinux or zig, and `maturin generate-ci` writes the CI. This is the
   route to wheels beyond macOS arm64: https://www.maturin.rs/distribution.html
9. Wikipedia, *Nautical chart*: "old or uncorrected charts should never be used for navigation". Every chart producer
   provides a correction system: https://en.wikipedia.org/wiki/Nautical_chart
10. Wikipedia, *Range lights*: two marks kept in line tell the navigator "the vessel is on the correct bearing",
    a route defined by something you can check, not by a drawing: https://en.wikipedia.org/wiki/Range_lights
11. Google Testing Blog, "Test Behavior, Not Implementation" (2013):
    https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html
12. Clones and runs: `sdist rustmapper-0.1.3` `src/main.rs:84-140, :180, :642`, `src/bfs_crawler.rs:420-556`,
    `src/cli.rs:57`, `src/writer_thread.rs:110-185`, `src/url_utils.rs:81-91`; Rust-sitemap 32c2651 `src/main.rs`
    (Resume handler, `drop(state)`, #30), `src/cli.rs:53, :82-140`, `src/completion_detector.rs`; the built 0.1.3
    binary from `r6/runcheck/work/v/bin/rust_sitemap` and a HEAD release build (`cargo build --release`, 4 min 43 s),
    both run on `tests/fixtures/route-site/`. Logs: `scratchpad/r01-3/*.out`.
