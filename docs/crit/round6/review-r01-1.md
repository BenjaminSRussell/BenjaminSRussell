# Review round 1, reviewer 1: the owner's test

9 Oct 2026. Build looked at: `scratchpad/r6/build/round-00/` (desk and phone, day and night, the page on desk and
phone), `README.md`, `SPEC.md`. This is the first review of round 6, so no earlier finding is repeated.

Verdict: **does not meet the goal yet. 5 / 10.** I would not ship it as is.

## The first question: does it meet the goal?

What it gets right, and it's a lot:

- The islands are gone. Nothing has a size, so nobody has to ask "is that the size of the project or how many
  commits?". That was my main complaint, and it's fixed.
- Every figure checks out (table below). Every stop and trap is something the code really does, in both the release
  and HEAD. The frontier stop is held back because of the robots.txt 404 bug, and that's right.
- Nothing names the theme. No pirate talk, no "survey", no ship.
- It answers "what is it showing?" in one sentence: how to start rustmapper and what comes out.

Where it fails my goal:

1. **It's a picture of text, and the same text sits right under it.** Count it. The two commands, the platform
   note, the release and its date, the seeders, the governor, the hand-off to ideal-url-organizer and
   export-sitemap all appear again within one screen below, as text you can actually copy. That's eight of the
   image's fifteen items. All the image adds is the two traps, the WAL line and the field names. A visitor reads the
   same facts twice, and the copy in the picture is the one they can't copy, search or zoom. WCAG 1.4.5 says it
   plainly: people can't change how text in an image looks, and machines can't read it. NN/g's eye-tracking work
   says text in images and coloured blocks at the top of a page are what readers learn to skip. That's the opposite
   of "every element has a purpose": half the image has no purpose the text below doesn't already serve better.

2. **The drawn marks carry almost nothing, and the spec admits it.** SPEC §7 test 4 says to strip the colour, the
   hatch and the bars and check that it still reads. It does, and that's the problem. If removing the line loses
   nothing, the line is decoration. The rings are all the same, so they say nothing a bullet doesn't. The red "//"
   only means "warning", and the words already say that. A strip map earns its form by putting a measure along the
   road: Ogilby's *Britannia* (1675) measured every road with a wheel, at one inch to the mile, and marked the hills,
   bridges and ferries you meet on the way. Beck's Tube map kept the one thing passengers navigate, which lines
   connect and where you change, and dropped the rest. This track has no measure and no junction. It's a bullet
   list with a pink line beside it. That's what "chasing a purpose" looks like.

3. **The "route a URL goes through" isn't a route any more.** The order drawn is seeders, a scope trap, governor,
   WAL, a Ctrl-C trap, output. The governor is a control loop that changes concurrency, not a step a URL passes
   through. The WAL records state events. Ctrl-C is something you do. With the frontier held back, not one per-URL
   stage is left between the seeds and the output. The track promises a pipeline, and the content is a list of
   properties. Either the picture has a real sequence or it shouldn't pretend to.

4. **It's about one install, not about me.** "How does it help the user see *my project*?" It shows one repository
   out of 21, as a how-to. Diátaxis is right that a how-to is "action and only action" for someone who already
   knows they want the tool. Someone landing on my profile doesn't know that yet. The only thing about me is the
   left column, and half of that is metadata: a commit sha you can't click, three dates in four lines, "as of".
   On the phone those three muted lines come before the project's name.

5. **The traps don't say what to do.** A pilot book names the danger *and how to keep clear of it*. The Coast
   Pilot exists for exactly the advice a chart can't carry. "Subdomains are in scope and there is no depth limit"
   leaves a stranger with no move to make. The code gives one: in 0.1.3, which is what pip installs, there's no
   `--max-urls` and no `--duration` (`sdist:src/cli.rs` has neither), so the only way to end a big crawl is Ctrl-C,
   which is exactly the second trap. They're one hazard and should read as one. The scope line also understates:
   `is_same_domain` (`src/url_utils.rs:81-91`) puts the start host's parent domain in scope too, not only its
   subdomains. Start at `blog.x.com` and `x.com` gets crawled.

So: honest and finally about the project, but half of it repeats the README in a form you can't use, and the
graphic part teaches nothing the words don't. That isn't a deep purpose yet.

## Figures checked

| Figure | Key | Value | Holds |
|---|---|---|---|
| 21 repositories | `repo_count` | 21 | yes |
| 32c2651 · 7 Oct 2026 | `repos.Rust-sitemap.head` | `32c2651…`, 2026-10-07; clone `git log -1` the same | yes |
| CI passed 7 Oct 2026 | `repos.Rust-sitemap.ci` | success, 2026-10-07 | yes |
| As of 9 Oct 2026 | `taken` | 2026-10-09 | yes |
| 0.1.3 · 8 Nov 2025 | `edition.version/date` | 0.1.3, 2025-11-08 | yes |
| macOS arm64 + Python 3.13 | `edition.wheels` | `cp313-cp313-macosx_11_0_arm64` | yes. Not run: `runcheck` ran on Linux x86_64 from source, and the survey line says so |
| `rust_sitemap` | `edition.scripts` | `["rust_sitemap"]` | yes |
| seeders, governor, WAL, Ctrl-C, struct fields | `routes.rustmapper.entries` | all verified head and release; S2 unverified (test file missing), not drawn | yes |
| ideal-url-organizer hand-off | `handoffs[0].state` | `runs`; 15 reader fields ⊆ writer; `tests/test_import_rust_sitemapper.py` has 6 tests | yes |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| T1 Ben Russell | whose page | keep | |
| T2 role line | what he builds | keep | |
| T3 "1 OF 21 PUBLIC REPOSITORIES" | this is one picked project | change | true, but desk says "PUBLIC" and phone doesn't. Pick one wording |
| T4 "CODE 32c2651 · 7 OCT 2026" | which code was checked | change | the sha can't be clicked and is already in the data line. Keep the date only, merged with T5 |
| T5 "CI ON MAIN PASSED 7 OCT 2026" | it works and is alive | keep | merge with T4's date into one line |
| T6 "AS OF 9 OCT 2026" | when it was read | change | a third date in four lines. Fold into the merged line or leave it to the data line |
| R0 rustmapper + one-line description | which project, what it does | keep | the best line in the image |
| R1/R12 start and end bars | where it starts and ends | change | only useful if the track carries a measure (must-fix 2). Otherwise cut |
| R2 `pip install rustmapper` + 0.1.3 · 8 Nov 2025 | how to get it; the release is old | change | the command is duplicated by the copyable block. Keep one entry line in the image and drop the code-block duplicate of the facts, or the reverse (must-fix 1) |
| R3 `rust_sitemap crawl --start-url <site>` | the real command name | change | same duplication. It earns its place only as the leg's start, with its measure |
| R4 platform note | whether pip just works for you | change | duplicated word for word below. One home: the text |
| R5 magenta track | nothing beyond "in order" | change | give it a measure or cut it |
| S1 seeders | where URLs come from | keep | not in the bullet too: cut the README's seeds bullet or this |
| H1 scope trap | big sites get crawled whole | change | add the move ("only Ctrl-C ends it in 0.1.3") and the parent domain; merge with H2 |
| S3 governor | it slows when it can't save | change | it's a control loop, not a stop. Say "fewer requests in flight" (it holds semaphore permits, `governor.rs`); duplicated by the first bullet |
| S4 WAL | a crash doesn't lose the crawl | keep | not said in the text; real (`wal.rs`, `Resume`) |
| H2 Ctrl-C trap | output only exists after one Ctrl-C | change | merge with H1 into one hazard with its move. The tool itself prints "Press Ctrl+C again to force quit", so the trap is the timing, not the key |
| `//` hatch | "warning" | change | says what the words say. Keep only if it marks the one merged hazard |
| rings | "a stop" | cut on phone | identical marks with no file names on phone teach nothing |
| R13 `data/sitemap.jsonl` + fields | what you get, real field names | keep | the most useful line for an engineer |
| R14 export-sitemap | second output | cut | in the code block, copyable |
| R15 read by ideal-url-organizer | his projects connect, and it's tested | keep | but cut the README's repeat or this |

## Every block of the page

| Block | Verdict | Why |
|---|---|---|
| Image | change | see above |
| Alt text | keep | states the message |
| Link line | keep | |
| Builds / Languages / Stack | keep | |
| rustmapper sentence "0.1.3 on PyPI, 8 Nov 2025" | change | the third copy of the release and its date (image, sentence, facts) |
| Facts line | keep | |
| Install code block + wheel note | keep | the copyable home of the commands. The wheel note is the one to keep; cut R4 from the image |
| Governor and seeds bullets | change | both are in the image. Keep each fact once |
| Hand-off sentence | change | the first half repeats R15. The second half ("not read by Scrapy yet") is my to-do list on the front page, which the decisions said to keep off. Cut it |
| Scrapy sentence, facts, code block, note | change | the comment "# from the clone root, start.py fails" reads as an instruction to run it there. Say "# start.py must run from here" |
| Scrapy bullets | keep | |
| Also / 15 more | keep | |
| Working rules | keep | rule 4 has no reason, only a citation. Give it one line or cut it |
| "Found a mistake?" | keep | |
| Data line | change | about 70 words of fine print. Says what was checked, which is good. Cut the sha (it's in the image) or shorten |
| License | keep | |

## Must fix, ranked

1. **One home per fact.** Today 8 of the image's 15 items repeat the text within one screen. Pick:
   the image keeps what a list can't show (order, where it bites, where it goes); the text keeps what you copy or
   look up (commands, platform note, release date). Cut R4 and R14 from the image, and cut the README's governor and
   seeds bullets, the first half of the hand-off sentence and the rustmapper sentence's release clause, or the
   reverse. Test: no string over 4 words appears in both the image and README.md (extend `strings`).
2. **Give the track a measure or remove it.** The weekly `runcheck` already runs the route. Record each step's wall
   time (`time.monotonic()` around each step in `scripts/runcheck.py`, into `steps[].secs`) and print the real legs on
   the track: "install: N min, compiles Rust on Linux; seconds with the Apple-silicon wheel", "first line in
   data/sitemap.jsonl after N s", "one Ctrl-C → file written in N s". The crawl leg comes from a fixture site, so
   print only install and shutdown, which aren't set by the harness. That's Ogilby's mile marks: what a stranger
   pays at each leg. If the measure can't be made honest, drop the bars and the track and set the route as plain
   numbered steps. Either way §7 test 4 must start to *fail*: removing the line has to lose something.
3. **One hazard with its move, made accurate.** Replace H1 and H2 with: "a big site never ends on its own: no depth
   or page limit in 0.1.3, and the domain above the start is in scope too. Press Ctrl-C once: it saves and writes
   the file. A second press quits without it." Anchors: `sdist:src/cli.rs` absent `max_urls` and `duration`;
   `url_utils.rs` `is_same_domain` parent branch; `shutdown.rs` strings. At HEAD, `--max-urls` exists: once a
   release carries it, the line becomes "stop it with --max-urls N". Gate it on `edition`.
4. **Stop calling it a URL's route unless it is one.** Either restore a real per-URL sequence (seed → frontier →
   fetch → parse → stored), drawn only as P1 lands, or relabel the order as the run's (install, start, while it
   runs, stop, output) and move governor and WAL off the track into a "while it runs" pair beside it. Test:
   every item on the track is a step a user does or a URL passes through.
5. **Tighten the title block to what's about him.** Desk and phone: name, role, then one muted line, "rustmapper ·
   1 of 21 · CI passed 7 Oct 2026". Cut the sha line and "AS OF" from the image (both stay in the data line).
   That saves 2 lines on desk and 2 on phone (about 68 px on the phone sheet). Same wording on both.
6. **Governor wording:** "fewer requests in flight when redb commits slow down" (semaphore permits,
   `governor.rs:56-71`), on the image and in the bullet if it stays.
7. **Small text fixes:** Scrapy comment "# start.py must run from here"; cut "not read by Scrapy yet" from the
   front page; give rule 4 one line of reason.

## Sources (fresh this round)

1. W3C, *Understanding SC 1.4.5: Images of Text*: https://www.w3.org/WAI/WCAG22/Understanding/images-of-text.html
2. Wikipedia, *John Ogilby*: *Britannia* (1675), 100 strip maps, measured by wheel at 1 in to the mile, hills,
   bridges and ferries shown, with a page of advice per road: https://en.wikipedia.org/wiki/John_Ogilby
3. Wikipedia, *Strip map*: https://en.wikipedia.org/wiki/Strip_map
4. Diátaxis, *How-to guides*: "action and only action": https://diataxis.fr/how-to-guides/
5. Wikipedia, *Chartjunk* (Tufte 1983; Bateman et al. 2010; Kosara on helpful annotation; Parsons & Shukla 2020):
   https://en.wikipedia.org/wiki/Chartjunk
6. NN/g, *Banner Blindness Revisited* (text in images, coloured blocks and top banners get skipped):
   https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/
7. GitHub Docs, *Managing your profile README* ("tell other people about yourself"):
   https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
8. RFC 9309 §2.3.1.3–2.3.1.4 (4xx may crawl all; 5xx assume disallow): https://www.rfc-editor.org/rfc/rfc9309.html
9. Wikipedia, *Harry Beck* (kept lines and interchanges, dropped distance): https://en.wikipedia.org/wiki/Harry_Beck
10. NOAA, *U.S. Coast Pilot* ("supplemental information that is difficult to portray on a nautical chart"):
    https://nauticalcharts.noaa.gov/publications/coast-pilot/index.html
11. Clones: `Rust-sitemap` 32c2651 `src/cli.rs` (flags `max_urls`, `duration`, idle plateau, no depth),
    `src/url_utils.rs:81-91`, `src/orchestration/governor.rs`, `src/orchestration/shutdown.rs`; sdist 0.1.3
    `src/cli.rs` (no `max_urls`, no `duration`); `ideal-url-organizer` 159968a `scripts/import_rust_sitemapper.py`,
    `tests/test_import_rust_sitemapper.py`.

The web-search budget for this run was used up by earlier agents, so the sources above were fetched directly by
URL.
