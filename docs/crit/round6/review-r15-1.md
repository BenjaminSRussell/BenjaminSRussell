# Review round 15, reviewer 1: Ben, the owner

10 Oct 2026. I looked at every PNG in `scratchpad/r6/build/round-14/`: the desk sheet at 870 and 846 (day and night),
the mid sheet at 746 (day and night), the phone sheet at 390 and 308 (day and night), the README's first screen at
1,180, 900, 1,366, 1,280 and 1,920, the README at 1,280 (two screens), 390 (six) and 360 (seven). I read `README.md`,
`SPEC.md`, `LOG.md` round 14 and the round 13 and 14 reviews. Round 14's fixes are not repeated here. Every figure was
checked again against `assets/stats.json`, the 0.1.3 sdist and the clones (table below). I also read the publish path,
`chart.toml`'s route entries and the `chart` branch as it stands now.

Verdict: **not yet. 8 / 10.** Nothing printed today is false, and the image is done. Round 14 landed: the desk sheet
is the stacked one (words at 16 px in the 846 column), Scrapy's two stages are told apart, the reset sentence is gone,
and each agent count sits next to the commit count it qualifies.

What stops me shipping is not the page. It's what happens the day I merge it, and what happens the day I do the job
round 14 left me.

1. **The job round 14 gave me would put a false stop on the image.** S2, "one queue per host, paced by that host's
   robots.txt", is waiting only for P1's test file at Rust-sitemap's HEAD. Its release anchors (`struct ReadyHost`,
   `fn fetch_robots_txt`) already pass in 0.1.3. But 0.1.3 isn't paced by robots.txt at all. Its `robots.rs` has no
   `parse_crawl_delay`, `HostState::new` sets `crawl_delay_secs: 0`, and the only producer passes
   `crawl_delay_secs: None` (`sdist:src/frontier.rs:787`). The page says so itself: "It sends requests with no pause
   between them … It ignores `Crawl-delay`." So the day I merge P1 into Rust-sitemap, the weekly build draws, on a
   picture of 0.1.3, a politeness 0.1.3 doesn't have, ten lines above the bullet that says it doesn't. Must-fix 1.
2. **Merging this branch today puts the islands back on my profile.** The gate is red on purpose (ROUTE-UNVERIFIED,
   S2, the one entry `route.unverified` returns from today's `stats.json`). In `profile.yml` a red gate skips the
   commit and the publish. The `chart` branch (`c488907`, 9 Oct) still serves the old 1,280 x 624 island sheet as
   `hero-day.svg`, and it has no `hero-mid-*.svg` at all. My README's first `<source>` names those mid files for 852 to
   1,199 px. So after the merge, a laptop window or an iPad held sideways gets a broken image. A browser takes the
   first `<source>` whose media matches [S2], and a failed load is "broken", not a fall-back [S3]. Every other width
   gets the map I said "makes no fucking sense", under alt text that describes a crawler route. That stays true until
   0.1.4 ships. Must-fix 2.

The third must-fix is small and new: round 14's Scrapy run sentence is now the densest block on the phone.

## The first question: does it meet my goal?

- **A deep purpose for the map.** Yes. One map, the route a URL takes through rustmapper 0.1.3: in, seeded, fetched,
  saved, the loop, the catch inside the loop, the one key, the file, and the project of mine that reads it. A list
  can't show the loop or where the catch bites in it. Nothing in it has a size. Nothing is an island.
- **True about my projects.** Today, yes, on the image and the page (table below). Tomorrow, no: S2 is armed to draw a
  false stop (must-fix 1).
- **Nothing chases a reason.** Yes. Every element below has a job a stranger needs done. The one block that works
  harder than it reads is the Scrapy run sentence (must-fix 3). It's there for a good reason, but its form hides it.
- **Nothing announces the theme.** Yes: the image, the page, the alt text and DESIGN.md. The manner is a strip map's.
  Nobody is told so.
- **Reads on a phone.** The image fits one screen at 390, 360 and 308. The page is 5,109 CSS px at 390. The Scrapy run
  sentence is 16 lines at 390 and about 17 at 360. Four of its code spans break across lines (`<your-` / `bot>`,
  `UConn-` / `Discovery-Crawler/1.0`, `Crawl-` / `delay`, `Python/3.11` / `aiohttp/3.13.1`).
- **Would I ship it as is?** No: must-fix 2. The content is ready. The pipeline won't put it on my profile.

## What I checked this round

**S2 against 0.1.3** (`scratchpad/r6/sdist013/rustmapper-0.1.3`):

```
src/robots.rs     fn fetch_robots_txt (18), fn fetch_robots_txt_from_url (33), fn is_stale (46); no crawl_delay
src/state.rs:280  crawl_delay_secs: 0          (HostState::new)
src/state.rs:560  host_state.crawl_delay_secs = delay   (the only setter)
src/frontier.rs:787  crawl_delay_secs: None    (its only producer)
src/frontier.rs:79   struct ReadyHost          (S2's release anchor: passes)
```

At HEAD (`32c2651`) `frontier.rs:911-913` reads `robots::parse_crawl_delay_secs(body)`, so "paced by that host's
robots.txt" is true of main and false of the release. `stats.json` says the same: S2 `verified_release: true`,
`verified_head: false`, missing only `tests/robots_4xx_allows_crawl.rs`. Rustmapper's own caution row (LOG round 2,
r2-1) already uses the right anchor: `robots.rs` *without* `fn parse_crawl_delay`. S2 needs the mirror of it.

**The publish path.** `profile.yml` runs on every push to `main` that touches `scripts/**` or `chart.toml`, and this
branch touches both. The gate step exits 1 on a fail. The commit and publish steps have no status function, so they
run only if every earlier step succeeded [S1]. `git ls-tree origin/chart` lists 11 files. The hero files there are
`hero-day`, `hero-night`, `hero-phone-day`, `hero-phone-night` and four stills; there is no `hero-mid-day.svg` or
`hero-mid-night.svg`. `hero-day.svg` on that branch opens `viewBox="0 0 1280 624"`, which is the island sheet.
`main`'s README names only those eight files, so `main` is consistent today. This branch's README is not, until a
publish runs. GitHub serves README images through Camo's cache [S4], so even after a good publish the old sheet can
linger for a while. That's one more reason not to merge the README ahead of the sheets.

**Rule 2 against bullet 1.** "Appended to and never overwritten" sits under a bullet that runs "OPTIMIZE and VACUUM". I
checked that they don't contradict each other. VACUUM deletes only files "no longer referenced by a Delta table and
… older than the retention threshold", and the cost is time travel to older versions [S5]. An append-only table loses
no rows that way. `lakehouse_manager.py` writes the raw layer with `mode="append"`. Its two `delete(` calls are the
queue GC (terminal queue rows, archived first) and `repair_unknown_domain`, which appends each row with its domain
before deleting the `unknown` partition. Both are operator maintenance, like the guarded wipe round 14 accepted. Rule
2 holds.

## Figures checked

| Printed | Source | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version` 0.1.3, `uploads` 0.1.3 at 2025-11-08T19:52:41 | yes |
| `pip install rustmapper` / `rust_sitemap crawl` | `edition.scripts` `["rust_sitemap"]` | yes |
| by default also from sitemaps, certificate logs and Common Crawl | sdist `cli.rs:58` `default_value = "all"` | yes |
| up to 20 pages at a time from each host | sdist `state.rs:285` `max_inflight: 20`; `frontier.rs:655` the check | yes |
| your site, its subdomains and its parent domain | S1/F1 anchors, `url_utils.rs is_same_domain` both `ends_with` | yes |
| saved as it goes; export works after a kill | runcheck `export_after_kill` ok, `kill_writes_file` in `fails` | yes |
| never exits by itself; `Received work item` … 60 s | sdist `bfs_crawler.rs:433` `eprintln!("Crawler: Received work item…`; H1 `quiet` 60; runcheck `ends_by_itself` in `fails` | yes |
| a second press before the `Saved to` line quits without writing the file | sdist `main.rs:517-520` second handler `std::process::exit(1)` before `:535-539` export and `println!("Saved to: …")` | yes |
| `data/sitemap.jsonl`; `url, depth, status_code, title` | `main.rs:535` `join("sitemap.jsonl")`; runcheck keys | yes |
| sorted 21 ways by ideal-url-organizer | `159968a`: 25 `method_*.py` files, 21 in `main.py self.methods` (the `[[figures]]` row, round 11); README's own "Methods 1-21" | yes, by the row's definition |
| 176 test functions | 161 `#[…test` attributes + 15 Python `def test_` in the clone at `32c2651` | yes |
| CI passed 7 Oct 2026: tests, rustfmt | `repos[Rust-sitemap].ci` success 2026-10-07, gates `tests`, `rustfmt` | yes |
| 16k lines of Rust | `lines.Rust` 16,390 | yes |
| Claude authored 45 of its 146 commits; co-signed 1 of his own 101 | `Rust-sitemap.git`: 97 + 4 his, 45 Claude; one `Co-authored-by: Claude` trailer | yes |
| Prebuilt for Apple silicon on CPython 3.13 | `edition.wheels` `["cp313-cp313-macosx_11_0_arm64"]` | yes |
| 3 min, cold cache, 4-core Linux x86_64 | runcheck `runner` Linux x86_64, `install` sdist; round 14's median stands | yes |
| 256 at a time; `--workers 1` | sdist `cli.rs:32` `default_value = "256"` | yes |
| Scrapy 1,920 test functions (CI selects all but 41) | `repos[Scrapy].test_functions` 1,920 (AUDIT's definition: collected files only; a raw grep of every `.py` gives 1,918 plus 10 Rust) | yes |
| CI passed 8 Oct 2026: tests, ruff, mypy, bandit · MIT · 69k | CI success 2026-10-08; Python 69,036 | yes |
| jules and Claude authored 71 of 499; co-signed 30 of his own 420 | `Scrapy.git`: 420 his, 49 jules, 22 Claude, 8 dependabot | yes |
| first five sentences; over 50,000 characters; bart-large-cnn | `constants.py:83` `extractive_max_sentences: 5`; `stage2_worker.py:954-960` `len(text) > MASSIVE_DOC_THRESHOLD` (50000); `stage4` `facebook/bart-large-cnn` | yes |
| near-duplicate pages by MinHash | `stage3_worker.py:7,151` `MinHashLSH` | yes |
| spider obeys robots.txt and Crawl-delay; stage 2: disallowed too, 4 per host, `Python/3.11 aiohttp/3.13.1` | round 14's rows; re-read at `96e7a1a` | yes |
| Rule 2: appended, never overwritten | see "Rule 2 against bullet 1" | yes |
| go_go_go: crawl and export-sitemap; headless Chrome; SQLite full-text search | `4078b55`: `crawl.go:44`, `export.go`, `renderer/chromedp.go`; FTS5 under `-tags sqlite_fts5`, which its CI and README build with | yes |
| rust_llm_logger: logged after the client's last byte | `aadba12` `proxy.rs:192` "Close the client stream before recording", `:251` `record` | yes |
| Ai_code_detector: `aicd scan` | `aicd.py:29,38`; `setup.py:48` `aicd=` | yes |
| 15 more | `repo_count` 22 = profile + 2 + 4 + 15 | yes |
| Languages line | `languages_line`: lead Python, Rust, then main languages by repo count, then lines | yes |

## Must fix, ranked

1. **S2 must not be drawable on a 0.1.3 image.** (`chart.toml:769-771`, S2's `release` anchors; one test. About 10
   lines.)
   - **What's wrong.** See point 1 above. The release anchors prove the struct and the fetch function exist, not that
     anything paces. S2's only gate is a test file at Rust-sitemap's HEAD, which says nothing about the release.
   - **Change.** Add `{path = "src/robots.rs", text = "fn parse_crawl_delay"}` to S2's `release` list. It is the
     mirror of the caution row's `absent` anchor, so the bullet "It ignores `Crawl-delay`" and the stop "paced by that
     host's robots.txt" flip on the same release, never one without the other. Add the comment: "0.1.3 has no
     Crawl-delay parser; this stop is drawn from the first release that has one."
   - **Test.** The 0.1.3 sdist plus a HEAD fixture that has `tests/robots_4xx_allows_crawl.rs` gives S2 unverified
     (release missing `fn parse_crawl_delay`). A release fixture with `fn parse_crawl_delay_secs` plus that HEAD gives
     S2 verified. STRINGS-TWICE or a new pairing test: S2 drawn and the "ignores `Crawl-delay`" bullet printed is a
     fail.

2. **Let the true image publish while S2 waits for a release.** (`chart.toml` S2 gains `waits = "release"`;
   `scripts/checks/route.py:253-256`; `profile.yml` step order; tests. About 30 lines.)
   - **What's wrong.** See point 2 above. The gate guards against drawing a stop that isn't true. It does that, but it
     also blocks publishing the six editions that are true. Merging now shows a broken image at 852 to 1,199 px and the
     island sheet at every other width, under a README about a crawler route. That lasts until 0.1.4, a release I
     haven't cut.
   - **Change, check.** An entry with `waits = "release"` whose *release* anchors fail is reported as `ROUTE-WAITING`,
     a warning (exit 2, which the workflow already allows), naming the missing anchor. The entry stays undrawn, as
     today. Every other unverified entry still fails, and so does a `waits` entry that holds in the release but not at
     HEAD (that's a real regression on main). After must-fix 1, today's S2 is exactly the warning case.
   - **Change, workflow.** Move "Publish sheets to the orphan chart branch" above "Commit stats, log, lock and README to
     main". `publish_chart.unshipped` already refuses a README that names an unshipped edition, so publishing first
     means `main` can never name a file the branch lacks, even if the publish fails.
   - **Before merging.** Run the workflow once on this branch with `dry_run: true` and read `out/check/`. The fast tier
     should be 0 fail, and the render tier should run, not be skipped as it was in every round-14 gate run. DESK-PX and
     the column checks have only passed "run alone" so far.
   - **Test.** Today's `stats.json` gives exit 2 with one ROUTE-WAITING and no ROUTE-UNVERIFIED. A fixture with S2's
     release anchors passing and HEAD missing gives ROUTE-UNVERIFIED (fail). An entry without `waits` that fails gives
     a fail, as now.

3. **Give Scrapy's effect on a site the same form as rustmapper's.** (`README.md:86`, hand-typed; the four `[[figures]]`
   rows keep their text. About 6 lines.)
   - **What's wrong.** The pick sentence asks a visitor to choose between my two tools. Rustmapper's effect on other
     people's servers is a lead line and a list ("Before you run 0.1.3:"). Scrapy's is the last two sentences of a
     105-word paragraph with seven code spans: 16 lines at 390, with four spans broken across lines. The two facts a
     site owner needs (who obeys robots.txt, and who doesn't) are in there, but nobody finds them. Use the same pattern
     for ideas of the same weight [S6], and give a list a lead-in line, with each bullet following from it [S7].
   - **Change.** Keep "Run these from the folder you cloned Scrapy into. `python start.py` starts PostgreSQL, Redis,
     Grafana and a worker for each of the four stages. It needs Docker and the `docker-compose` command (Docker
     Desktop has it; on Linux, install Compose standalone). It loads no seeds: the last command gives the spider your
     site." Then:

     > Before you run it:
     >
     > - The spider obeys `robots.txt` and its `Crawl-delay`, and names itself `<your-bot>` (without that line,
     >   `UConn-Discovery-Crawler/1.0`).
     > - The stage 2 worker then fetches every link the spider queued, disallowed ones too, 4 at a time per host, as
     >   `Python/3.11 aiohttp/3.13.1`.

   - **Why "Before you run it:".** The same lead as rustmapper's tells the visitor these are the same kind of fact for
     the other tool. The difference between the two lists *is* the comparison. STRINGS-TWICE: none of the figure
     strings is printed twice; the lead is not a figure.
   - **Size.** About +1 line at 390 (a lead line and two bullet indents, against two sentence joins saved). The
     breaks no longer hide the point.
   - **Test.** README-CAUTIONS, or a new check: the Scrapy block has a list under "Before you run it:" whose two items
     contain `Crawl-delay` and `Python/3.11 aiohttp/3.13.1`.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page this is | keep | first thing read on every edition |
| Role, two caps lines | crawl and data infrastructure; Python and Rust | keep | the route under it proves the first line |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project, and what you get from it | keep | true on the run check |
| Start bar + `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | the date is what makes every 0.1.3 caution honest |
| Magenta track | one way through, top to bottom | keep | order is the strongest channel the subject has |
| Stop rings | each is one step the tool takes | keep | |
| S1 `rust_sitemap crawl` + seeds | the real command, and where URLs come from by default | keep | the default asks third parties; the page gives the flag |
| F1 fetch, 20 per host, scope | the loop's work, and how far it reaches | keep | |
| W1 "saved as it goes; export works after a kill" | a kill doesn't throw the crawl away | keep | |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| H1, red dotted box, inside the loop | 0.1.3 never exits, and how you know it's done | keep | goes when 0.1.4 ships |
| Gap in the track under the loop | the only way out is you | keep | |
| C1 Ctrl-C once | the one key, and the second press not to make | keep | the tool itself prints "Press Ctrl+C again to force quit" |
| End bar + `data/sitemap.jsonl` + fields | the file, in the struct's own names | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | my projects feed each other | keep | 21 is what `main.py` runs |
| S2 (not drawn) | (would claim) 0.1.3 is paced by robots.txt | **change** | must-fix 1: false for the release it would be drawn on |
| Night editions | the same | keep | contrast holds; the red box reads on navy |
| Desk (stacked, 1,000) and mid editions | the same, the whole route on the first screen | keep | 16 px words at 846; whole route above the fold at 1,366 x 650 |
| Phone editions (390, 308) | the same, on one phone screen | keep | |
| Alt text | install, loop, stop, file | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image link to the repository | where the project lives | keep | |
| `<picture>` sources | the right sheet for the width | keep, gated | must-fix 2: the mid sources point at files the branch doesn't have until a publish |
| Link line | where to go | keep | |
| "Ben Russell builds …" | what I build | keep | |
| Languages | what I write in | keep | from the data |
| Stack | what I build on | keep | |
| Pick sentence | which tool for which job | keep | |
| rustmapper facts line | alive, tested, size, which commit, who wrote it | keep | each count beside its qualifier |
| Wheel note | whether `pip` just works on your machine | keep | |
| "Before you run 0.1.3:" | what it does to someone else's server, with the lever for each | keep | the model for must-fix 3 |
| Fold "What 0.1.3's files miss or get wrong" | the file caveats, one step away | keep | |
| rustmapper code block | how to run it, when to stop, how to recover | keep | the comment travels with the commands when copied |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy bullets 1–3 | storage; what happens to a page; how it's watched, stopped and deployed | keep | |
| Scrapy run sentence | what `start.py` starts and needs; what the crawl does to a site | **change** | must-fix 3: same form as rustmapper's list |
| Scrapy code block | how to point it at your site and name your bot | keep | |
| Grafana and `data/delta/` | where to look once it runs | keep | |
| Also: four tools | the file's reader, the Go sibling, two more tools by what they do | keep | |
| 15 more (fold) | the rest | keep | |
| Working rules 1–3 | how I build, each with its evidence | keep | rule 2 checked against VACUUM this round |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn, how it was run, who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Noted, not ranked

- "co-signed 1 of his own 101" asks the reader to know what a `Co-authored-by` trailer is. "and is co-author on 1 of
  his own 101" says it in plain words. That's my taste, not a fault.
- At 1,920 the stacked desk sheet leaves about a quarter of its width empty on the right. Round 14's reviewer 3 judged
  that margin a good measure. I agree.
- `check.py --tier fast` run in this worktree, against the `assets/` left on disk, reports thousands of TYPE and
  XML-SIZE fails from retired sheets (`footer-still-*`) and a stale `build-report.json`. The round's own gate run
  (LOG) was clean apart from S2. Whoever runs the gate by hand should rebuild first. A clean-tree note in the
  README's maintainer comment would save the next person the scare.

## Owner notes, outside this repository

1. **Corrected from round 14.** Landing P1 in Rust-sitemap is still right, because HEAD never crawls a site whose
   robots.txt is a 404. But it is not what puts S2 on the image. After must-fix 1, S2 waits for a *release* with the
   Crawl-delay parser: 0.1.4 cut from main, with P1 in it.
2. **Carried:** 0.1.4 (exits when idle, P1, `response.url()` as the link base, `noindex` and canonicalized pages left
   out of `export-sitemap`, `resume` after a kill, the robots.txt port, a LICENSE, `[project.scripts]` so the command
   is `rustmapper`). PyPI won't let me replace 0.1.3's files, so the fix has to be a new version number [S8]. Also
   carried: Scrapy stage 2's robots check, delay and name; `start.py --reset-delta`; `[position]` and `[contact]`; one
   measured crawl at scale; the GitHub bio; the iOS and Android apps; a real iPad.

## Sources (new this round; none cited in earlier rounds)

The shared web-search budget ran out partway through this round. Every source below was opened and read directly.

1. [S1] GitHub Docs, "Evaluate expressions in workflows and actions", status check functions: "A default status check
   of `success()` is applied unless you include one of these functions", and `success()` "returns `true` when all
   previous steps have succeeded". The commit and publish steps have none, so a red gate stops both (must-fix 2):
   https://docs.github.com/en/actions/reference/workflows-and-actions/expressions
2. [S2] WHATWG HTML Standard, "The picture element": "The user agent will skip to the next source element if the value
   does not match the environment." The mid `<source>` matches first at 852 to 1,199 px (must-fix 2):
   https://html.spec.whatwg.org/multipage/embedded-content.html
3. [S3] WHATWG HTML Standard, "Images": the user agent "will choose the first source element for which the media query
   in the media attribute matches". An image whose data can't be had is in the "broken" state, and nothing in the
   algorithm retries the next source. A missing `hero-mid-day.svg` is a broken image, not the desk sheet (must-fix 2):
   https://html.spec.whatwg.org/multipage/images.html
4. [S4] GitHub Docs, "About anonymized URLs": "To host your images, GitHub uses the open-source project Camo". If an
   updated image doesn't show, its cache has to be reset or purged. The old sheet can outlive a good publish, so the
   README must not go out ahead of the sheets (must-fix 2):
   https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-anonymized-urls
5. [S5] Delta Lake, "Table utility commands", VACUUM: it removes "files no longer referenced by a Delta table and are
   older than the retention threshold" (default 7 days), and "the ability to time travel back to a version older than
   the retention period is lost". Compaction plus VACUUM loses no appended rows, so rule 2 and bullet 1 agree:
   https://docs.delta.io/latest/delta-utility.html
6. [S6] Purdue OWL, "Parallel Structure": "using the same pattern of words to show that two or more ideas have the same
   level of importance", and "keep all the elements in a list in the same form". Rustmapper's and Scrapy's effects on
   a site are ideas of the same weight (must-fix 3):
   https://owl.purdue.edu/owl/general_writing/mechanics/parallel_structure.html
7. [S7] GOV.UK, A to Z style guide, "Bullet points and steps": "You can use bullets to make text easier to read",
   "always use a lead-in line", and bullets "should normally form a complete sentence following from the lead text".
   Hence the two Scrapy bullets (must-fix 3):
   https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/
8. [S8] PyPI, Help, file name reuse: PyPI "does not allow for a filename to be reused, even once a project has been
   deleted and recreated", and "deleted files cannot be re-uploaded". A release's code is fixed, so a stop drawn on
   "0.1.3" has to be proved in 0.1.3's files, not at HEAD (must-fix 1, owner note 2): https://pypi.org/help/
9. [S9] The clones and the sdist, read for this round: `rustmapper-0.1.3` `src/robots.rs`, `src/state.rs:280,560`,
   `src/frontier.rs:79,655,787`, `src/main.rs:505-541`; Rust-sitemap `32c2651` `src/frontier.rs:911-913`; Scrapy
   `96e7a1a` `src/lakehouse/lakehouse_manager.py:918,1387`, `src/stage2/stage2_worker.py:954-960`,
   `src/core/constants.py:83`; ideal-url-organizer `159968a` `src/organizers/`, `README.md:14-43`; go_go_go `4078b55`
   `internal/storage/sqlite.go:16-18`, `.github/workflows/ci.yml:21`; rust_llm_logger `aadba12` `src/proxy.rs:192,251`;
   the `chart` branch at `c488907`.
