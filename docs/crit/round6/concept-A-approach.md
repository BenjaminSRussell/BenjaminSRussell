# Concept A: the way into his work

Round 6, 9 Oct 2026. One concept for the first image and the page around it. It answers the owner's question, "what is
it showing?", in one sentence:

> **How you start rustmapper, what happens to a URL inside it, in order, and the three places where a stranger goes
> wrong.** The same drawing is repeated once for Scrapy, next to Scrapy's text.

Research is cited as `R2-F4` (round-6 file R2, finding F4) or `R5-test 3` (R5's six-question test). Code is cited as
`repo:path:line` in the clones at Rust-sitemap `32c2651` (7 Oct 2026), Scrapy `96e7a1a` (8 Oct 2026) and the PyPI
sdist `rustmapper-0.1.3.tar.gz` (`sdist:path:line`), all read for this memo.

---

## 1. Why this subject, and why a picture

**The subject comes first, then the form** (R5-F7, Munzner's "wrong abstraction"). The facts a visitor comes for are
known: what he builds, which project to open, how to run it, whether it works, what goes wrong (R4-F5, F7, F8; R3-F11
lists the 44 kinds of questions programmers ask, which are "where is it, what calls what, how does data get from A to
B"; R2-F14). The current image answers none of them. It shows when he committed (R2 "a log drawn to look like a
chart"; R3-F5; R5-F3: a "mere appearance match").

**His projects have a real route.** In rustmapper a URL is seeded, queued per host, paced by robots.txt, fetched by a
worker pool the governor resizes, written to a checksummed log and then redb, and comes out as `data/sitemap.jsonl`
(R6-F2, every stop a file). Scrapy has the same shape in four stages over Delta tables (R6-F4). A route with an order of
stops, hazards at known places and an end where you get something is the one relation a pilot book and these projects
share (R5-test 1; R5-F14; R1-I3).

**The form is the pilot book's, not the chart's.** A stranger entering a harbour reads, in this order: what the place
is; the way in; what you will see; the hazards; where to berth (R2-F2, Coast Pilot 1 ch. 6). The deck version keeps
only the route, the marks in order and the hazards, and is drawn "aligned with the waterway ... course-up" (R2-F10,
R1-F3). That is what this image is: a straightened strip, top to bottom, from the command that starts the program to
the file it hands you.

**What the picture does that text does not.** Vertical position is the order a URL passes through (position on a common
scale, the strongest channel: R1-F16, R5-F6). A hazard sits at the stop where it bites, so a reader sees *where* in
the run each trap is, which a bullet list cannot show (R1-F10 clearing lines; R3 implication 9). The entrance and the
end are fixed points a reader can find in a second (R4-F3: first words carry the gist). Everything else that is a
lookup (test counts, CI dates, languages, the other 19 repositories) stays in text, because a table or list beats a
map for lookups (R3-F4, R5-F10, R1-I11).

**How this differs from the "Approaches to Scrapy Harbor" sheet cut in round 4.** That sheet turned stages into buoys,
Grafana into a lighthouse and Delta Lake into an anchorage, coined names ("429 Shoal"), drew soundings that were
illustrative, and needed a symbol key that took 40 % of its height (docs/crit/round4/crit-stranger.md:21, :56;
crit-type.md:35). This concept has no symbols to decode, no place names, no soundings and no key. Every mark is a
command, a file or a fact that a build step finds in the code (section 5).

---

## 2. The first image: rustmapper's way in, with the title block

### 2.1 What is drawn (the same on desk and phone; only the layout changes)

From top to bottom, on one magenta line:

```
Ben Russell                              rustmapper  RUST
CRAWL AND DATA INFRASTRUCTURE            Crawls one site and lists every page it can reach.
PYTHON AND RUST                          ━━ pip install rustmapper            0.1.3 · 8 NOV 2025
                                         ┃  rust_sitemap crawl --start-url <site>
READ FROM THE CODE AT 32C2651            ┃  prebuilt for macOS arm64 + Python 3.13; elsewhere pip needs Rust
AND PYPI 0.1.3 · 9 OCT 2026            ▨ ┃  the command is rust_sitemap, not rustmapper
                                         ○  src/*_seeder.rs   start URL, plus sitemaps, CT logs, Common Crawl
                                       ▨ ┃  crt.sh may stall it: --seeding-strategy sitemap
                                         ○  frontier.rs       a queue per host, paced by its robots.txt
                                       ▨ ┃  subdomains are in scope; there is no depth limit
                                         ○  governor.rs       fewer fetch workers when redb commits lag
                                         ○  wal.rs            logged before stored; resume after a kill
                                         ━━ data/sitemap.jsonl  one line per page: url, depth, status, title
                                            rust_sitemap export-sitemap → sitemap.xml
```

`━━` is the start bar and the end bar, `┃` the track (magenta), `○` a stop (ink ring), `▨` a hazard (red hatch on the
left of the track, the danger side). Nothing else is on the sheet: no border graduations, no axis, no islands, no
water tint, no light, no motion.

### 2.2 The rule that keeps every mark true for the person who installs it

`pip install rustmapper` gives 0.1.3 from 8 Nov 2025; the drawing is read from the code of 7 Oct 2026. They differ: the
governor's range is 32–512 with 500/100 ms thresholds in 0.1.3 (`sdist:src/main.rs:89-93`) and 256–1,024 with
2,000/200 ms at HEAD (`Rust-sitemap:src/orchestration/governor.rs:14-34`); `--max-urls`, idle exit and the 50,000-URL
sitemap split exist only at HEAD (`Rust-sitemap:src/cli.rs:82`, `src/completion_detector.rs`,
`src/sitemap_writer.rs:134`; absent in the sdist). So: **a stop or hazard is drawn only if it is true in both the
released package and the current code, and it prints the mechanism, never a count that differs between them.** That
is why the governor line says "fewer workers when commits lag" and not "256–1,024 workers"; it also settles the five
conflicting worker figures (R6-F7) by printing none. File names are HEAD's, because the repository link opens HEAD
(R3 implication 12).

### 2.3 Element by element

Each row: what a visitor learns; why this form; evidence; the data it needs and whether `build_stats` has it today.

| Element | Visitor learns | Why this form | Evidence | Data, gathered? |
|---|---|---|---|---|
| **Name** "Ben Russell", serif | whose page this is | the first of the six facts a screener reads (R4-F1); largest type = the first thing to read | R4-F1, F4 | `chart.toml [chart] login` / identity; yes |
| **Role line** "CRAWL AND DATA INFRASTRUCTURE / PYTHON AND RUST" | what he builds, in the first two words | the role line must name what the picture shows (R5 impl. 10); the picture is a crawler, so they agree | R4 impl. 5, R5-F2 (titles carry recall) | `chart.toml [copy] role_line`; yes |
| **Datum line** "READ FROM THE CODE AT 32C2651 AND PYPI 0.1.3 · 9 OCT 2026" | the drawing comes from the code at a named version, and how old it is | a chart's title block is read first and says what was measured and when (R1-F2); pilot-book pages carry their date (R2-F11) | R1-F2, I8; R2-F11, I9 | `repos[Rust-sitemap].head.sha`: **new**; `edition.version`: yes; `taken`: yes |
| **Project header** "rustmapper RUST" + "Crawls one site and lists every page it can reach." | which project this is and what it does, before any detail | a pilot entry opens with what the place is (R2-F2 item 1); the "what" is 16.7 % of README content and the visitor's first need (R4-F8) | R2-F2; R4-F8; `Rust-sitemap:README.md:3` | name from `chart.toml [hero.aliases]`, language `repos[].main_language`: yes; the sentence: `chart.toml` copy, **new key** |
| **Start bar + `pip install rustmapper`** | the one line that gets it | the entrance is the first mark on the route and the shortest correct start (R1-I5 leading line); wrong install lines are the most common documentation failure (R4-F9) | R1-F10, I5; R4-F9, F17 | the package name `edition.project`: yes |
| **"0.1.3 · 8 NOV 2025"** beside it | the release is eleven months older than the code drawn below | a version belongs at the install end of the route, not on a timeline (R6 impl. 8, R5-F13) | `edition.version`, `edition.date` | yes |
| **`rust_sitemap crawl --start-url <site>`** | the command that actually runs after pip | the 0.1.3 wheel holds one file, `rustmapper-0.1.3.data/scripts/rust_sitemap`, and no `rustmapper` command | R6-F6; R4-F17; wheel listing (scratchpad/r6/pypi-wheel/w.whl); `sdist:src/cli.rs:6` | binary name from the wheel: **new** `edition.scripts` |
| **Platform note** "prebuilt for macOS arm64 + Python 3.13; elsewhere pip needs Rust" | whether pip will just work on their machine | a pilot book states the condition for strangers ("drafts greater than 4 or 5 feet") next to the entrance (R2-F3) | `edition.wheels = ["cp313-cp313-macosx_11_0_arm64"]`; R6-F6 | yes (`edition.wheels`) |
| **Hazard H1** "the command is rust_sitemap, not rustmapper" | why the command differs from the package, and that other docs which say `rustmapper crawl` need an alias | the trap a stranger hits first, placed at the entrance; red hatch on the danger side (Bowditch danger bearing, R2-F4) | `Rust-sitemap:README.md:25`; R6-F6; R4 impl. 9 | quote verified in README: **new** (route check) |
| **Track** (one magenta line, start bar to end bar) | there is one way through, and you follow it top to bottom | the line you follow is drawn in the colour charts reserve for what you act on (R1-F6, I9); one line = one graph (R3 impl. 8) | R1-F3, F6; R3-F10 | none (geometry) |
| **Stop S1** `src/*_seeder.rs` "start URL, plus sitemaps, CT logs, Common Crawl" | where URLs come from, and that he does not rely on links alone | a directed path between two pages exists 24 % of the time, so a crawler that only follows links misses pages; seeders are his answer (R6-F3, R7-F3, F9) | `Rust-sitemap:src/sitemap_seeder.rs:1`, `ct_log_seeder.rs:81-82`, `common_crawl_seeder.rs:105`; same three files in the sdist | anchors verified: **new** |
| **Hazard H2** "crt.sh may stall it: --seeding-strategy sitemap" | the default seeding waits on outside services, and the one flag that avoids it | a clearing line: one hazard, one rule (R1-F10); it sits at the seeding stop because that is where the stall happens | `Rust-sitemap:README.md:86` (default `all`), `:222-223`; `sdist:src/cli.rs:58` (default `all` in 0.1.3) | quote verified: **new** |
| **Stop S2** `frontier.rs` "a queue per host, paced by its robots.txt" | the crawler is polite by construction: one queue per host, gaps set by the host's own robots.txt | this is the Mercator frontier design (R6-F2 step 5, R7-F11), the core of a crawler; a visitor who knows crawlers recognises it in one line | `Rust-sitemap:src/frontier.rs:78` (`ReadyHost`), `:103-107` (rendezvous shard), `src/config.rs:21`; `sdist:src/frontier.rs:77-100, 814` | anchors: **new** |
| **Hazard H3** "subdomains are in scope; there is no depth limit" | pointing it at a large site crawls every subdomain to the bottom | a known limit is stated as a fact for strangers, like "uncovers 9 feet" (R2-F3); it sits at the frontier, where scope is decided | `Rust-sitemap:src/url_utils.rs:81-91` (identical in the sdist), `bfs_crawler.rs:697` (depth recorded, never cut); R6-F2 step 4 | anchors: **new** |
| **Stop S3** `governor.rs` "fewer fetch workers when redb commits lag" | the crawl slows when it cannot save what it found, not when the network is slow | this is his most unusual design choice and the one "why" his README carries (R4 impl. 10); the line states the mechanism true in both versions (2.2) | `Rust-sitemap:src/orchestration/governor.rs:14-67`; `sdist:src/main.rs:84-130` | anchors: **new** |
| **Stop S4** `wal.rs` "logged before stored; resume after a kill" | a crash does not lose the crawl; there is a `resume` command | the reason the project exists as a durable tool; R6-F2 step 8 | `Rust-sitemap:src/wal.rs:68` (`[len][crc32c][seqno][payload]`), `README.md:251-262`; `sdist:src/wal.rs:68`; `resume` in both CLIs | anchors: **new** |
| **End bar + `data/sitemap.jsonl`** "one line per page: url, depth, status, title" | what you get and where it is on disk | the berth is "where you lie": the file you open when the run is done (R2-F2 item 7; R2-F9 the arrival view) | `Rust-sitemap:README.md:131-133`; `sdist:src/main.rs:535` (writes `sitemap.jsonl`), `sdist:src/state.rs:98-112` (fields) | anchors: **new** |
| **`rust_sitemap export-sitemap → sitemap.xml`** | the second output, and the command for it | a sitemap is literally a map of a site (R6-F3); this is the product's name | `sdist:src/cli.rs:129-141`; `Rust-sitemap:README.md:38` | anchors: **new** |

**Left out of this image, and why.** Week islands, shallows, axis, commit rows, "15 more": they encode the calendar,
which a visitor does not navigate (R1-I2, R3 impl. 1, R5 impl. 1, R2-I1, R7-I1). `Fl 30s`: a code only a sailor reads,
one of three configured intervals, and nothing a visitor acts on (R1-I6, R5-F13). The dashed graduated border:
graduations are degrees of latitude and longitude, and there are none (R1-F12: furniture has a mechanical job or goes);
a hairline edge stays so the sheet's extent is clear on GitHub's page. Bloom sizes, shard counts, worker counts,
throughput: either they differ between versions or they are unmeasured (R6-F7, F8). The hand-off to
ideal-url-organizer: true, but off the route, so it goes in the text (R5-test 5). Motion: nothing in this subject moves
on a period; the still and animated editions become one file.

### 2.4 Sizes and places

Sheet units; GitHub shows the desk sheet at ×0.68 (870 px column) and the phone sheet at ×0.54 (390 px). Floors from
`scripts/tokens.py:71-74`: desk 19 semantic / 25 serif, phone 26 semantic / 30 serif.

**Desk, 1280 × 600 sheet (870 × 408 on screen; the current hero is 870 × 424).**

- Left column x 56–400: name serif 88, baseline y 128 (60 px on screen). Role line caps 19, tracking 1.6, baselines
  182 and 210. Datum line caps 19 in `muted`, baselines 262 and 290. The rest of the column is paper.
- Route column: track at x 456, text at x 484, 740 px of text width (about 70 characters at 19 px).
  - Header: "rustmapper" serif 30 + "RUST" caps 19 `muted`, baseline 72; the sentence in sans 19, baseline 100.
  - Start bar: magenta, 24 × 4, at y 128, x 444–468. Entrance lines at baselines 140, 167 (mono 19, ink) and 194
    (sans 19, `muted`); the version label caps 19 `muted` on line 140 at x ≥ 760.
  - Track: magenta, weight BRUSH (3.4), x 456, y 128 to 490.
  - Rows at a 36 px pitch from baseline 232: H1 232, S1 268, H2 304, S2 340, H3 376, S3 412, S4 448.
  - End bar at y 490 (magenta, 24 × 4); end lines at baselines 496 and 523.
  - Stop ring: radius 6, PEN (1.3) ink, paper fill, centred on the track at the row's x-height. File name in mono 19
    `ink2`, the rule in sans 19 `ink`, 16 px apart.
  - Hazard: a 14 × 10 block of three 45° hatch strokes (HAIR, `accent`) at x 438–452, left of the track; the text in
    sans 19 `ink`. Red text was tested and fails: `accent` #D73626 on paper #F4EEE1 is 4.09:1, under 4.5:1; the hatch
    is a graphic and needs only 3:1. Night: `accent` #FF6853 on #0F1A2B is 6.1:1.
- Hairline edge (HAIR, `hair`) 12 px inside the sheet.

**Phone, 720 × 1250 sheet (390 × 677 on screen; the current phone hero is 390 × 610).**

- Name serif 132, baseline 150. Role line caps 26, baselines 210 and 244. Datum line caps 26 `muted`, baselines 290
  and 324.
- Header baseline 390 ("rustmapper" serif 40 + "RUST" caps 26); sentence sans 26, baseline 428.
- Track at x 40, text at x 72, 628 px wide (about 46 sans or 40 mono characters at 26 px).
- Entrance: start bar y 460; lines at 482 and 516 (mono 26), 550 and 584 (sans 26 `muted`: the version and the
  platform note, split over two lines).
- Stops take two lines on the phone (file name, then rule), pitch 82; hazards one line, pitch 48, except H2 which
  wraps after "stall it:" (two lines). Order and content are the desk's.
- End bar and the two end lines finish near y 1210; sheet bottom 1250.
- First-two-screens check (R4 impl. 6): with GitHub's mobile profile header (about 450 px; measure on the device) the
  image ends near 1,130 px and the link line under it near 1,150 px, inside two iPhone screens.

---

## 3. The second image: Scrapy's way in, placed above Scrapy's text

Same form, same rules, its own sheet, so the phone hero stays one screen. Scrapy's own README draws its main stages
twice in Mermaid (`Scrapy:README.md:22-34, 124-161`); this drawing adds what those diagrams do not have: the entrance,
three traps, the stage-4 branch condition and the place you land (R6-F4: "a picture that only repeats that adds
nothing").

```
Scrapy  PYTHON                  ━━ cd Scraping_project && python start.py
Discovers pages, then           ┃  needs docker and docker-compose
analyses and summarises       ▨ ┃  from the clone root, start.py fails
them in four stages.            ○  stage1/scout_spider.py  same site, depth 10, obeys robots.txt
                              ▨ ┃  run it as scrapy crawl scout, not scout_spider
READ FROM THE CODE AT         ▨ ┃  the bundled config crawls uconn.edu: -a allowed_domains=…
96E7A1A · 9 OCT 2026            ○  lakehouse/      raw rows in Delta tables, partitioned by domain
                                ○  stage2/         parsed; pages over 50,000 characters go to stage 4
                                ○  stage3/         MinHash drops near-duplicates; extractive summary
                                 ╲○ stage4/        large documents: bart-large-cnn, on the worker
                                ━━ localhost:3000  Grafana: Scraping Pipeline Health
                                   data/delta_lake/  the tables themselves
```

| Element | Visitor learns | Why this form | Evidence | Data, gathered? |
|---|---|---|---|---|
| Title block (name, language, sentence, datum) | which project, what it does, read from which commit | as 2.3; the sentence corrects the profile's "BART summaries" overstatement by naming stages | `Scrapy:README.md:20`; R6 impl. 7 | language `repos[].main_language`: yes; sha: **new** |
| Entrance `cd Scraping_project && python start.py` | the one command that starts the whole pipeline | the shortest correct start (R1-I5) | `Scrapy:README.md:91-96` | anchor: **new** |
| "needs docker and docker-compose" | what must be installed first | the stranger's condition beside the entrance (R2-F3) | `Scrapy:Scraping_project/start.py:24-27` (`REQUIRED_TOOLS`) | anchor: **new** |
| H1 "from the clone root, start.py fails" | the first trap, at the first step | the project's own README calls it out (#334) | `Scrapy:README.md:86-89` | quote: **new** |
| S1 `stage1/scout_spider.py` "same site, depth 10, obeys robots.txt" | where pages are found and how far it goes | the first stop of the URL's path | `src/stage1/scout_spider.py:47` (`name = "scout"`), `src/settings.py:121, 228-229` | anchors: **new** |
| H2 "run it as scrapy crawl scout, not scout_spider" | the spider's name is not its file's name | trap at the stop it belongs to (#489) | `Scrapy:README.md:228-241` | quote: **new** |
| H3 "the bundled config crawls uconn.edu: -a allowed_domains=…" | by default it crawls someone else's site, and how to point it at yours | a stranger must know whose site they are hitting (R7-F12: a crawl shows its own conduct) | `Scraping_project/config.yml:29-30`; `Scrapy:README.md:256` | anchors: **new** |
| S2 `lakehouse/` "raw rows in Delta tables, partitioned by domain" | everything lands raw first; the stages talk through tables | his "raw before clean" rule, shown where it happens | `src/lakehouse/lakehouse_manager.py:364-368, 538-553` | anchors: **new** |
| S3 `stage2/` "parsed; pages over 50,000 characters go to stage 4" | analysis happens here, and the condition for the branch | the branch point is a decision on the route, so it is a stop (R1-F9) | `src/core/config.py:389` (`massive_doc_threshold=50000`), `src/stage2/stage2_worker.py:960` | anchors: **new** |
| S4 `stage3/` "MinHash drops near-duplicates; extractive summary" | how duplicates are caught and what kind of summary most pages get | corrects the page's claim that all summaries come from BART (R6-F7) | `src/stage3/stage3_worker.py:7, 22` | anchors: **new** |
| S4b `stage4/` on a short spur from S3 | large documents take a separate path, summarised on the worker by bart-large-cnn | a spur is the only honest drawing of "some pages go elsewhere" (R6-F4: main channel plus branches) | `src/stage4/summarization.py:79` | anchors: **new** |
| End `localhost:3000` "Grafana: Scraping Pipeline Health" and `data/delta_lake/` | where you look when it runs, and where the data is on disk | the berth: what you see on arrival (R2-F9) | `start.py:29`, `monitoring/dashboards/scraping_pipeline_health.json:2-3`, `config.yml:301-302` | anchors: **new** |

Sizes: desk 1280 × 520 sheet (870 × 354), left column holds "Scrapy" serif 53, "PYTHON" caps 19, the sentence in sans 19
over three lines and the datum line; route column, pitch, marks and colours exactly as 2.4. Phone 720 × 1110 (390 ×
600), stops on two lines as 2.4. Left out: the 30 s scrape interval, the 42 alert rules, Kafka, Redis, Postgres, Helm
(true, but nothing a newcomer acts on to get in: R1-I7 select by importance; R2-F10 drop what you will not act on).

---

## 4. The page around the images

Order is the pilot book's: what he is (planning guide, one line), then each project's entry: picture, verdict, how to
run, why (R2-F12, I8; R4-F8 cognitive funnel).

| Block | Visitor learns | Why it is here and in this form | Evidence |
|---|---|---|---|
| 1. First image (section 2) | who, what he builds, how to start rustmapper and what it does | first and largest thing he controls on the profile (R4-F4) | as 2.3 |
| 2. Link line `rustmapper · Scrapy · PyPI · Email` (unchanged) | where to click; nothing inside an `<img>` is clickable | names the projects in the image's order (R4 impl. 8) | R4-F13 |
| 3. "Ben Russell builds …", Languages, Stack (unchanged) | the keywords a screener scans for | planning-guide facts, one line each (R2-I8); recruiters scan for keywords (R4-F1) | R4-F1 |
| 4. rustmapper: one sentence, then the measured facts line (176 test functions, CI passed 7 Oct 2026, 16k lines of Rust, last commit 8 Aug 2026) | whether it works and is alive | the plain verdict for a stranger (R2-F3); recency answers "alive?" (R4-F7) | `repos[Rust-sitemap].test_functions, ci, lines, last_ns`: gathered |
| 5. rustmapper code block, copyable: `pip install rustmapper` / `rust_sitemap crawl --start-url <your-site>` / `rust_sitemap export-sitemap --data-dir ./data --output sitemap.xml` / `# current code: cargo install --git https://github.com/BenjaminSRussell/Rust-sitemap` | the same commands as the image, in a form you can paste, plus the way to get the newer code | an image cannot be copied; the current block prints `rustmapper crawl`, which fails with "command not found" | R6-F6; R4-F17, impl. 9; `Rust-sitemap:README.md:25` |
| 6. One line of real output under the block: `{"url":"https://example.com/","depth":0,"status_code":200,"content_length":1024,"title":"Example","link_count":5}` | exactly what the berth file looks like | the arrival view (R2-F9), as text so it can be read and searched | `Rust-sitemap:README.md:133` (format, not a crawl result; labelled "format") |
| 7. Two "why" bullets: the governor (kept as written) and the three seed sources (kept); the WAL and frontier bullets are cut because the image now says them | the reasons behind the two least obvious stops | "why" is the 2.7 % most READMEs skip (R4-F8, impl. 10); what the image shows is not repeated (R5 impl. 9) | current README |
| 8. One sentence on hand-offs: "`sitemap.jsonl` feeds ideal-url-organizer (`scripts/import_rust_sitemapper.py`); a Delta export named `stage1_discovery` is written for Scrapy, which does not read it yet." | the projects are one body of work, and which link is built | true and off the route, so text; the unbuilt link is stated as unbuilt (R6-F5, impl. 2) | `ideal-url-organizer:scripts/import_rust_sitemapper.py`, `tests/test_import_rust_sitemapper.py`; `Rust-sitemap:README.md:141-169`; grep of Scrapy finds no reader |
| 9. Second image (section 3) | how to start Scrapy and what a page goes through | its own entrance and traps differ from rustmapper's | as section 3 |
| 10. Scrapy facts line (1,920 test functions, CI passed 8 Oct 2026, 69k lines, last commit 8 Oct 2026) and code block `cd Scraping_project` / `python start.py` / `# Grafana: http://localhost:3000` | verdict and copyable commands | as 4 and 5 | `repos[Scrapy]`: gathered; `Scrapy:README.md:93-105` |
| 11. Two Scrapy "why" bullets: raw-first Delta (kept), breakers and per-host throttles (kept); the BART bullet corrected to "stage 4, large documents" | reasons, and no overstatement | R6-F7, impl. 7 | `stage3_worker.py:22`, `stage4/summarization.py:79` |
| 12. "Also": four lines, each saying the project's shape; go_go_go's line names what differs (headless Chrome, SQLite search, TLS-fingerprint impersonation) and drops "100M+" (three different values in its own repo) | what else he built, honestly | lookups belong in a list (R3-F4); R6-F9, F11 | `go_go_go:README.md`; R6-F7 |
| 13. "15 more" in `<details>` (unchanged) | the rest exist, one line each | hiring readers read side projects as interest (R4-F5), but they are not the way in | R4 impl. 13 |
| 14. Working rules (unchanged) | how he thinks, each rule tied to code | the "why" at profile level | current README |
| 15. Data line, rewritten: "The drawings are read from the code: rustmapper at 32c2651 and the 0.1.3 package on PyPI, Scrapy at 96e7a1a. Every stop and trap names a file you can open. Test counts, CI results and dates measured 9 Oct 2026 from clones of 21 public repositories · 3 % of my commits carry an AI co-author trailer; 297 more were written by coding agents and are not counted as mine · regenerated weekly." | how sure each figure is and where it comes from | a guide says how sure it is and dates itself (R2-F11); the old line described a chart that is gone | `AUDIT.md`; `coauthored_total`, `agent_authored`: gathered |
| 16. Alt text for image 1: "How to start Ben Russell's crawler rustmapper and what happens to a URL inside it: pip install rustmapper, then run rust_sitemap crawl. URLs come from the start URL, sitemaps, CT logs and Common Crawl; wait in a queue per host paced by robots.txt; are fetched by workers the governor cuts when database commits lag; are logged before they are stored; and end as data/sitemap.jsonl and sitemap.xml. Three traps are marked: the command name, seeding that can stall on crt.sh, and no depth limit." Image 2 the same for Scrapy. | the message, for a screen reader or a broken image | alt states the message, not the drawing (R4 impl. 12; W3C complex images, R4-[51]) | R4-F16 |
| 17. License line (unchanged) | terms | required | — |

---

## 5. Data: what each mark needs, and what to build

**Already gathered by `scripts/build_stats.py`:** `edition.project`, `edition.version`, `edition.date`,
`edition.wheels`; per repository `main_language`, `test_functions`, `ci`, `lines`, `last_ns`; `taken`;
`coauthored_total`; `agent_authored`.

**New, all from clones and PyPI the build already reads:**

1. `repos[].head = {sha, date}` for the two flagships: `git rev-parse HEAD` and `git log -1 --format=%cs` in the clone
   build_stats already makes. (The sha in `claims.workers`, 00a877d, is a hand-set value in `chart.toml` and is already
   out of date against the clone's 32c2651.)
2. `edition.scripts`: the executables in the released wheel, read from its `RECORD` (`*.data/scripts/*`). Today that
   is `["rust_sitemap"]`. Cached per version so the wheel is fetched once per release.
3. `[route.rustmapper]` and `[route.Scrapy]` in `chart.toml`: an ordered list of entries, each `{kind = "stop" |
   "hazard" | "entrance" | "end", file, text, anchors = [...], quote?}`. `anchors` are literal strings the file must
   contain (for example `"ADJUSTMENT_INTERVAL_MS: u64 = 250"`, `"DEPTH_LIMIT = 10"`, `"massive_doc_threshold=50000"`,
   `"name = \"scout\""`); a hazard carries a `quote` from the repository's README.
4. `scripts/data/route.py` (new, about the size of `claims.py`): at build time it opens each `file` at the recorded
   HEAD sha and checks every anchor and quote; for rustmapper entries it repeats the anchor check against the 0.1.3
   sdist (`anchors_release`), which enforces rule 2.2. It writes `stats.json` key `routes` with each entry, its
   `verified` flag and the sha. A failed entry fails `check.py --tier fast` with the file and the missing string; the
   sheet never draws an unverified mark and never drops one silently.
5. Optional, weekly on a macOS arm64 runner: `pip install rustmapper && rust_sitemap --help` and, for Scrapy,
   `python start.py --dry-run` (`start.py:4-9`), so the entrance lines are checked by running them (R1-I5, R4 impl. 9).

**No longer needed by the hero:** `weeks`, `week_days`, `months`, `tide`, `variation`, `hours`, `claims.scrape_interval`,
`sweeps` for drawing. They stay in `stats.json` for the audit; nothing on the page prints them.

The hero module becomes `scripts/sheets/approach.py` drawing one route from `stats.routes[name]`; the BREAKS table's
reasons are rewritten so each names a project fact (R5 impl. 5).

---

## 6. Checks that this meets the owner's goal

| His words | How this concept answers | Test a reviewer runs |
|---|---|---|
| "what is that going to help? How does it help the user see my project? What is it showing?" | It shows how to start his main project and what it does to a URL, in order. | Show image 1 for 10 s to someone new; ask "what does he build, how do you start it, where does the output go?" Pass if they say crawler, `pip install rustmapper` / `rust_sitemap crawl`, `sitemap.jsonl` (R4 impl. 1, R3 impl. 14). |
| "tiny islands ... Is it based on the size of the project or how many commits?" | No shape has a size. Every mark is a ring, a bar, a hatch or a line; position means order. | List every shape in the SVG; none has a size that varies with data (R4 impl. 2, R5 impl. 8). |
| "chasing a purpose instead of having a purpose" | The form follows the subject: the projects have a route, so the drawing is a route; the reason for every element names a project fact. | Grep the new BREAKS table for reasons that mention land, chart, sea or water without a project fact: none (R5 impl. 5). |
| "Everything, single thing inside of this needs a purpose" | Sections 2.3, 3 and 4 give each element what it teaches, why the form, and its source. | An element without a row in those tables, or a row without a file, line or `stats.json` key, fails. |
| "If I was a sailor, if I was a pilot ... very helpful information" | It is a pilot book's entry: way in, marks in order, hazards with their remedy, where you land. | Remove every colour and the hatch: the page still reads as directions for a stranger (R2-I11). |
| "Don't tell the user ... it should be obvious"; no theme words; no pirate talk | No word names the theme. The manner (course-up strip, magenta track, hatched dangers, terse judgements, dated datum) carries it. | Grep image text for chart, sea, harbour, survey, buoy, light, berth, approach: zero hits. |
| "The data doesn't look exactly accurate"; honest data only | Every mark is verified against the code at a sha, and true in the release too (2.2). No count that differs between versions is printed. | `route.py` passes; every number in the SVG (0.1.3, 8 Nov 2025, 50,000, depth 10, Python 3.13, the two shas, 9 Oct 2026) has a source row. |
| "I'm looking at iPhone ... accepting of all formats" | Phone layout is designed first: 14 px type on screen, one column, 677 px tall. | At 390 px every label is ≥ 13 px on screen and the link line is inside the first two screens on a real iPhone, in Safari and the GitHub app (R4 impl. 6, 7). |

---

## 7. Risks

1. **It may read as a flowchart, not as something with a "cool format".** The theme is now only in the manner. If the
   owner wants the shipping layer visible, this concept gives him less of it than any earlier round. The answer to that
   is better drawing of the same marks (line quality, type, the hatch), never added symbols.
2. **Text inside an image.** Commands in the picture cannot be copied, searched or translated; they are repeated in
   the code blocks below, which is deliberate duplication.
3. **Two images instead of one.** The page gains a second picture; it replaces four README bullets and the hero's
   islands, but the page is still one image longer than today.
4. **Maintenance.** Renaming a file or changing a default breaks the build until `chart.toml [route.*]` is edited. That
   is the cost of every mark being checked; the error names the entry.
5. **Selection is still editorial.** Which three traps and which five stops are drawn is a choice. The limit is that
   each comes from the project's own README or code, never invented.
6. **The release and the code diverge further** with every commit to Rust-sitemap. If 0.1.4 is not released, the
   "true in both" rule removes more stops over time. Releasing from HEAD (with a `rustmapper` entry point) would also
   let the image show `rustmapper crawl` again (R4 impl. 9).
7. **Engineers' detail, recruiters' glance.** File names and shas mean little to a non-engineer; the role line, header
   sentence and berth have to carry the message for them. The 10-second test in section 6 checks this.
8. **GitHub's mobile app may always serve the day edition** (R4-F13, anecdotal); the day edition must stand alone.
9. **Phone height** depends on GitHub's mobile profile header, which was estimated, not measured.
10. **Scrapy's default target is a third party's site (uconn.edu).** Printing it is honest and useful as a warning; it
    also puts another organisation's name on the profile.
