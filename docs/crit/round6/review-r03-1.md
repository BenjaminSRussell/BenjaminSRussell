# Review round 3, reviewer 1: the owner's test

10 Oct 2026. Build looked at: `scratchpad/r6/build/round-02/`: the desk and phone sheets, day and night; `once-p1-lands/`;
the whole page, desk screens 1 and 2 and phone screens 1 to 5. Read: `README.md`, `SPEC.md`, `DECISIONS.md`, `LOG.md`,
and the six reviews from rounds 1 and 2. I don't repeat findings already fixed. Figures were checked against
`assets/stats.json`, the 0.1.3 sdist, the clones and the GitHub API.

Verdict: **it does not meet the goal yet. 6 / 10.** Up from 5. I would not ship it as is.

## The first question: does it meet my goal?

Round 2 fixed real things. Each fact has one home now, so the image and the code block don't say the same thing twice.
The title block is just my name and what I build. W1's cause is right, and its number is read from the constant. The
desk file labels are true for the release. The rule dates come from git. The repository count is 22 and is checked. On
a phone the whole image is about 480 px, so the link line lands on the first screen. Nothing has a size, and no word
names the theme. When I ask "what is it showing?", I get an answer: how my crawler starts, what it does with each page,
how you stop it, and where its output goes. That was the question I asked on 9 Oct. The picture answers it now.

Where it still fails me:

1. **The loudest line in the image gives the wrong reason.** "never ends by itself: no page or depth limit, and the
   parent domain counts as same-site". The colon tells the reader that scope is why it never ends. It isn't. The run
   check proves this itself: a **3-page local site** with `--seeding-strategy none`, no depth and no parent domain, was
   still running at 150 s (`runcheck.rustmapper.steps[ends_by_itself]`). The real cause is in the code. In 0.1.3 the
   "Exit when the frontier is empty" check sits in the `else =>` arm of `tokio::select!` (`sdist:src/bfs_crawler.rs:548-553`).
   That arm runs only when every branch is disabled, and that never happens. Issue #65 says exactly this ("Crawl never
   exits after the frontier drains (completion check unreachable in select! else arm)"). It was fixed on main in
   `d751cf0` on 7 Oct. So H1 commits the same error round 2 removed from W1: both halves are true, and the "because"
   between them is false. "No depth limit" isn't a trap either. Scrapy ships `DEPTH_LIMIT = 0`, which means no limit,
   and still closes the spider when it goes idle. The trap is the missing idle exit.

2. **The band turned my worst release bug into the loudest mark on my profile.** The only filled colour in the image is
   a pink bar across "never ends by itself". On a phone it is the biggest shape under my name. Round 2 was right that a
   stranger must not miss the danger, but it chose the wrong form. A pink highlight comes from a text editor or a diff.
   It reads as "error", and it outranks the project name. A chart doesn't mark a danger that way. US Chart No. 1, K1:
   "A danger line draws attention to a danger which would not stand out clearly enough if represented solely by its
   symbol". It is a dotted line, with no fill. The bigger miss is that the drawing could show the real fault and
   doesn't. The fault is a loop with no exit. Today the track runs straight down through the hazard into "press
   Ctrl-C", so the shape says the run flows on by itself and only the words disagree. Break the track below the loop
   and the shape says it on its own, even in grey: the only way down is Ctrl-C. When a release ends by itself, the gap
   closes. That is the purpose and the theme in one mark, with nothing announced.

3. **Two rows teach kill semantics in two opposite-sounding clauses.** W1 says "after a kill, export-sitemap still
   works" and two rows later C1 says "a second press or a kill skips it". Both are true and both were probed. A stranger
   has to work out that they mean two different files. Three of the seven route rows are now about failing to stop.
   One instruction does the job of both clauses: what to press, and what to run if the process got killed instead. In a
   container that is the usual case: Kubernetes sends TERM, waits 30 s, then KILL. In 0.1.3 the shutdown code listens
   only for `ctrl_c`, the signal Tokio's own shutdown guide shows.

4. **The foot of the page says something false.** "The drawing is rustmapper 0.1.3 from PyPI: every file it names is in
   that release". The desk image names `scripts/import_rust_sitemapper.py`, which is in ideal-url-organizer, not in the
   release, and `data/sitemap.jsonl`, which is output. The audit sentence overclaims, and that is the one sentence
   whose job is not to.

5. **Small things a stranger trips on.** On the phone, S1 breaks after "start URL;" and leaves a two-word line that
   reads like its own item. On the desk, the governor row has no file label, so its words start in the middle of the
   column after a gap, which looks like a rendering bug. "The parent domain counts as same-site" is wrong for anyone
   who knows the term: in the HTML Standard, example.com and sub.example.com *are* same-site. The surprise is narrower
   and plainer: start on a subdomain and it also crawls the domain above it. Siblings are not crawled
   (`url_utils.rs:81-91`).

6. **Still outside this repository, and still the condition for shipping.** The image's only date is "8 NOV 2025". It
   sits beside a hazard that main fixed three days ago (#65 in `d751cf0`, #63 in `aaa38d6`, `--max-urls` at
   `src/cli.rs:82`). Employers check a profile for recent activity first and fastest (Marlow & Dabbish, CSCW 2013). This
   image tells them old and broken. Landing P1 and cutting 0.1.4 rewrites H1, C1 and the date with no edit here. I'm
   not adding it to the must-fix list again, because it was ranked and declined last round as an owner action. It still
   decides whether this ships.

So: the form has a purpose now, the loop, and the content is honest. But its single loudest line explains the bug
wrongly, and it is drawn as an alarm instead of as a shape. Fix 1 to 4 and it becomes an image I'd defend. Ship it only
after 0.1.4.

## Figures checked

| Printed | Key / source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `edition.uploads[0.1.3].time` | 0.1.3, 2025-11-08T19:52:41; PyPI still lists 0.1.3 as latest (checked today) | yes |
| pip install rustmapper | `edition.scripts`, runcheck `install` ok | `["rust_sitemap"]`; 171.4 s median cold | yes |
| start URL; by default also sitemaps, certificate logs, Common Crawl | `sdist:src/cli.rs:58` `default_value = "all"` | release scope | yes |
| fetch a page; same-site links go back on the queue | routes F1, probe `crawl_ctrl_c` | verified both | yes |
| fetches fewer pages at once when saving falls behind | routes G1 (`governor.rs` / sdist `main.rs`) | verified both | yes |
| saved every 50 ms | `BATCH_TIMEOUT_MS` sdist `writer_thread.rs:11`, HEAD `:12` | 50, both | yes |
| after a kill, export-sitemap still works | probe `export_after_kill` | 3 `<loc>` | yes |
| never ends by itself | probe `ends_by_itself` | still running at 150 s on 3 pages | yes |
| : no page or depth limit, and the parent domain counts as same-site | sdist `cli.rs` (no `max_urls`, `max_depth`), `url_utils.rs:88-90` | both true, but given as the cause | **no, as worded** (finding 1) |
| press Ctrl-C once … a second press or a kill skips it | probes `crawl_ctrl_c` ok, `kill_writes_file` false | | yes |
| one line per page: url, depth, status_code, title, … | `SitemapNode`, both trees | | yes |
| read by ideal-url-organizer … with a test | `handoffs[0].state = runs`, 15 reader fields ⊆ writer, both trees | | yes |
| 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust | `test_functions` 176, `ci` success 2026-10-07 (7 jobs), `lines.Rust` 16,390 | | yes |
| 1,920 tests · CI passed 8 Oct 2026 · 69k lines of Python | Scrapy `test_functions`, `ci` (5 jobs), `lines.Python` 69,036 | | yes |
| 3 min from a cold cache on a 4-core Linux x86_64 machine | runcheck install `runs` 168.2/171.4/174.3, `cpus` 4, `cache` cold | 2.9 min | yes |
| ran on 10 Oct 2026; measured 10 Oct 2026; 22 public repositories | `runcheck.date`, `taken`, `repo_count` | | yes |
| every file it names is in that release | sdist file list | `scripts/import_rust_sitemapper.py` is not in it | **no** (finding 4) |
| 3 %; 297 | `coauthored_total.agent_share` 0.031; `agent_authored.total` 297 | | yes |
| 15 more | 22 − 1 − 2 − 4 | 15 | yes |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| Ben Russell | whose page this is | keep | |
| Role line | crawlers and data infrastructure, Python and Rust | keep | the drawing under it proves it |
| Desk left column below the role (empty) | nothing | keep | quiet paper is fine; it keeps the route the only dense block |
| "rustmapper" + "Crawls a site and writes one line for every page it reaches." | which project and what it does | keep | the best line in the image |
| Start bar | where you begin | keep | |
| `pip install rustmapper` | the door | keep | the image's one command, allowlisted |
| 0.1.3 · 8 NOV 2025 | how old the thing you'd install is | keep (changes once 0.1.4 exists) | true and needed; it's also why the hazard below is old news on main (finding 6) |
| Magenta track | read top to bottom, one way through | change | break it below the loop (must-fix 2) so its shape says "no way out but Ctrl-C" |
| seeder.rs, S1 | URLs come from more than links, and by default it calls outside services | keep words, fix phone wrap | the orphaned "start URL;" (must-fix 5) |
| bfs_crawler.rs, F1 | it's a crawler loop | change | takes the scope fact from H1, in plain words (must-fix 1) |
| Governor tick + "fetches fewer pages at once when saving falls behind" | it throttles itself to its store | keep words, change desk placement | the gap in the label column looks like a bug (must-fix 6) |
| writer_thread.rs, W1 | it saves continuously | change | keep "saved every 50 ms" and move the kill consequence into C1 (must-fix 3) |
| Loop line with up arrow | which rows repeat for every page | keep | the one thing only a drawing can show |
| Hazard H1 words | the catch | change | wrong cause (must-fix 1) |
| Hazard band | that this row matters most | cut | an editor's highlight, and the loudest mark on the profile; replaced by the danger line and the gap (must-fix 2) |
| Hazard hatch | a danger | cut | replaced by the danger line; one danger mark, not two |
| C1 "press Ctrl-C once …" | how to get out and get the file | change | one instruction covering both kill clauses (must-fix 3) |
| Rings | a stop | keep | |
| End bar | where you end up | keep | |
| `data/sitemap.jsonl` + field names | what you get, in the struct's own words | keep | |
| Hand-off arrow + "read by ideal-url-organizer …, with a test" | my projects feed each other, and the join is tested | keep | on the phone, "ideal-url-organizer" means nothing until "Also"; acceptable, since the link is one scroll away |
| Night edition | same | keep | the muddy `#312531` band goes with the band |

## Every block of the page

| Block | Verdict | Why |
|---|---|---|
| Image | change | above |
| Alt text | keep | "It loops until one Ctrl-C writes data/sitemap.jsonl" is right, and it will stay right after must-fix 1 to 3 |
| Image link target | change | wrap the `<picture>` in a link to Rust-sitemap, so a tap lands on the project and not the raw SVG (must-fix 7) |
| Link line | keep | |
| Builds / Languages / Stack | keep | |
| rustmapper sentence | keep | |
| Facts line "On main at 32c2651 …" | keep | the only "is it alive" answer on the page today. It is labelled main, so it doesn't contradict the 0.1.3 drawing |
| Install code block | keep | |
| Wheel note | keep | defined, cold, three runs |
| Scrapy sentence, facts, code block, Grafana note | keep | |
| Scrapy bullets | keep | dense, but each one is a design fact a list carries better than a picture |
| Also | keep | |
| 15 more | keep | |
| Working rules | keep | rule 4's "Claude wrote its first version" is honest and the gate requires it |
| Found a mistake? | keep | |
| Data line | change | the "every file it names" overclaim (must-fix 4) |
| License | keep | |

## Must fix, ranked

1. **H1 states its real cause; the scope fact moves to F1** (`chart.toml [route.rustmapper]` H1 and F1; anchors; about
   20 lines). H1 text: "never stops by itself, even after the last page" (47 characters, one line on desk and on
   phone, which saves 34 units on the phone). Release anchors: `src/bfs_crawler.rs` `fn = "start_crawling"` containing
   `else =>` and "Crawl complete: frontier empty". Probe `ends_by_itself` must fail. Once that probe passes, H1 isn't
   drawn at all: a crawl that ends by itself has no trap here. Drop the `--max-urls` and "{secs}" instead wordings,
   because they describe scope, not the fault. F1 text: "fetch a page; links on its domain, above or below it, go back
   on the queue". If `typeset` says that overflows the desk line next to `bfs_crawler.rs`, use "fetch a page; links in
   its domain or the one above go back on the queue". F1 takes H1's `url_utils.rs` parent-branch anchor. Tests: a
   T-ANCHOR fixture where the `else =>` arm is replaced by a timer leaves H1 unverified; the round-2 STRINGS-TWICE and
   FIGURES checks still pass. Why: the loudest line must not give a false "because" (finding 1; issue #65; Scrapy
   `DEPTH_LIMIT` 0 and `spider_idle`).
2. **Draw the fault as a shape and cut the band and hatch** (`scripts/sheets/route.py`: `_band`, `_hatch`, the track
   path; `PURPOSE`, `BREAKS`; about 40 lines). (a) The track stops at the loop's bottom (`y_bot`). It starts again 10
   units (desk) or 12 (phone) above C1's ring, so there is a gap in the line and C1's ring sits at the top of the
   resumed segment. The gap is drawn only while `ends_by_itself` fails, and closes when it passes. Geometry may follow
   a probe but never a count, so T-NOSIZE holds. (b) Remove `_band` and both hatch blocks. Around H1's text block, draw
   a danger line: a rounded rectangle, padding 6, of dots (r 1.4 desk / 1.8 phone, pitch 6 / 8) in `accent`, with no
   fill. It needs ≥ 3:1 as a graphic in both themes (`contrast` plug-in), and the bounds check must find it overlapping
   no text. (c) Update CONTRAST-BAND to CONTRAST-DANGER, and add a test: with all colour stripped (`fill`/`stroke` set
   to ink), the SVG still has the gap in the track. Why: the danger becomes visible through the drawing, not an
   alarm colour, and the name stays the first thing you read (finding 2; Chart No. 1 K1; NN/g on hierarchy).
3. **One instruction for stopping** (`chart.toml` W1 and C1). W1: "saved every 50 ms" (the `const` anchor stays; drop
   `runs = ["export_after_kill"]` here). C1: "press Ctrl-C once to write data/sitemap.jsonl; after a kill, run
   export-sitemap". It needs probes `crawl_ctrl_c` ok, `kill_writes_file` failing and `export_after_kill` ok. Instead
   wording, when a kill does write the file: "press Ctrl-C once to write data/sitemap.jsonl". Why: one row says what to
   do, and the image stops teaching two opposite kill facts (finding 3; Kubernetes pod termination).
4. **Make the data line true** (`scripts/render_readme.py route_clause`; test in `tests/test_pipeline.py`). "every file
   it names is in that release" becomes "every rustmapper source file it names is in that release". When a hand-off
   is drawn, add: "the reader it points to is ideal-url-organizer's, at `<to_sha short>`". Test: a route whose labels
   include a path outside the sdist file list fails ROUTE-LABEL, unless it is the hand-off's `reader` and matches the
   `to` clone at `to_sha`. Why: the audit sentence must not overclaim (finding 4).
5. **Phone wrap** (`route.py wrap`). Choose the separator break only if every line it makes is at least 45 % of
   `max_w`; otherwise break at words. Test: S1 at phone width gives no line under 45 %. Why: "start URL;" on a line by
   itself reads as its own item.
6. **Desk governor row** (`route.py`). A note with no label sets its words at the label column's x (484), in `ink2`, so
   there's no hole in the column. The tick stays. Why: the gap reads as a missing label.
7. **The image links to the project** (`render_readme.py`, `picture:hero` block). Wrap the `<picture>` in
   `<a href="https://github.com/BenjaminSRussell/Rust-sitemap">`. Check on the rendered page that GitHub keeps the
   outer link (this session couldn't fetch github.com to confirm). Why: "how does it help the user see my project?"
   Tapping the drawing should open the project.

Owner action, outside this repository and not re-ranked (declined in round 2): land P1 with its test, give HEAD a
`[project.scripts]` command, publish 0.1.4. After that H1 isn't drawn, the gap closes, and the date reads 2026.

## Sources (fresh this round)

1. NOAA / NGA, *U.S. Chart No. 1*, 13th ed., Section K, "Danger line: A danger line draws attention to a danger which
   would not stand out clearly enough if represented solely by its symbol … or delimits an area containing numerous
   dangers"; and "Colors": magenta for elements "significant to marine navigation", "shades of blue depict potential
   hazards". https://nauticalcharts.noaa.gov/publications/docs/us-chart-1/ChartNo1.pdf (must-fix 2)
2. WHATWG HTML Standard, "same site": example.com and sub.example.com are same-site.
   https://html.spec.whatwg.org/multipage/browsers.html#same-site (finding 5, must-fix 1)
3. Scrapy docs, Settings, `DEPTH_LIMIT`: default 0, "If zero, no limit will be imposed."
   https://docs.scrapy.org/en/latest/topics/settings.html (finding 1: no depth limit is normal; it isn't the trap)
4. Scrapy docs, Signals, `spider_idle`: "If the idle state persists after all handlers of this signal have finished,
   the engine starts closing the spider." https://docs.scrapy.org/en/latest/topics/signals.html (finding 1: the norm is
   to close when idle)
5. Rust-sitemap issue #65, "Crawl never exits after the frontier drains (completion check unreachable in select! else
   arm)", closed by `d751cf0`, 7 Oct 2026; sdist 0.1.3 `src/bfs_crawler.rs:548-553`.
   https://github.com/BenjaminSRussell/Rust-sitemap/issues/65 (finding 1)
6. Kubernetes docs, Pod Lifecycle, termination flow: "send a TERM signal to process 1", default grace "30 seconds",
   then `SIGKILL`. https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ (must-fix 3)
7. Tokio, "Graceful Shutdown": the example detects shutdown with `tokio::signal::ctrl_c` and names no other signal.
   https://tokio.rs/tokio/topics/shutdown (finding 3: why a kill skips the file)
8. J. Marlow, L. Dabbish, "Activity Traces and Signals in Software Developer Recruitment and Hiring", CSCW 2013: "It is
   easy to quickly verify active open source involvement just by seeing … evidence of recent activity in their
   profile's activity feed." https://www.cs.cmu.edu/~xia/resources/Documents/Marlow-cscw13.pdf (finding 6)
9. Nielsen Norman Group, "Visual Hierarchy in UX: Definition": hierarchy comes from contrast in value and saturation, and
   extra backgrounds add clutter, so use them sparingly. https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
   (finding 2)
10. W3C, Understanding SC 1.4.5 Images of Text: "People cannot alter how text looks in images."
    https://www.w3.org/WAI/WCAG22/Understanding/images-of-text.html (why every row has to earn its place in the image)
11. ICA MapCarte 118/365, Ogilby's *Britannia* (1675): strip maps told travellers "the distances, landmarks, obstacles
    and resting points along a given road". https://mapdesign.icaci.org/tag/route-mapping/ (the strip form is earned
    when its obstacles are where they bite; must-fix 2)
12. V&A, Beck's Underground diagram, and the Canterbury editorial: topology over topography, and riders need "where to
    board, where to alight, and where to change". https://api.vam.ac.uk/v2/object/O1361001 (the gap is a "change"
    point: the only way off the loop)
13. GitHub Docs, "Managing your profile README": "to tell other people about yourself".
    https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme
    (must-fix 7)
14. Code and data: Rust-sitemap history clone (`git log --first-parent --since=2025-11-08T19:52:41Z`: 34 first-parent
    commits, most on 7 Oct 2026); `stats.json` `runcheck`, `routes`, `handoffs`; PyPI JSON for rustmapper (latest 0.1.3).
