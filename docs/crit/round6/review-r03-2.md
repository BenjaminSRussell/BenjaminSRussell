# Review round 3, reviewer 2: the copy editor

10 Oct 2026. Reviewer: a deadpan copy editor who knows where a theme stops being charming and starts being cringe.
Build looked at: `scratchpad/r6/build/round-02/`. That covers the desk sheet at 870 and the phone sheet at 390, day
and night; the page on desk (screens 1–2) and on phone (screens 1–5); and `once-p1-lands/`. Read: `README.md`,
`SPEC.md`, `LOG.md`, `DECISIONS.md` and the six earlier reviews. Figures checked against `assets/stats.json`, the
0.1.3 sdist (`scratchpad/r6/sdist013`), the 0.1.3 wheel (`scratchpad/r6/pypi-wheel/w.whl`) and the clones. I don't
repeat findings that are already fixed or already ruled on in `LOG.md`.

Verdict: **does not meet the goal yet. 6 / 10.** It is close. What's left is mostly copy, and one line of that copy
is false.

## The first question: does it meet the owner's goal?

Mostly. Taking his tests in order:

- **Every element has a purpose.** Nearly. The image is now one route: install, seed, a loop of fetch and save, one
  hazard, one way out, one file, one hand-off. Nothing has a size. Nothing is there to fill space. The loop is the
  one mark a list can't replace.
- **It teaches something true.** Not quite. The hazard is the row the band tells you to read first, and its colon
  gives the wrong cause (finding 1). The data line under the page also claims something the drawing doesn't do
  (finding 6).
- **Nothing chases a reason.** Yes, in the image. On the page, two cross-references and one rule heading are there
  for effect rather than for the visitor (findings 7, 8).
- **Nothing announces the theme.** Yes. No sea words anywhere, and T-WORDS holds. The theme is down to the magenta
  line, the start and end bars, and the hatch. It doesn't tip into cringe anywhere. If anything it now sits on the
  other side of the line, where the one themed mark that's left gets read as something else: the hatch reads as a
  Rust comment (finding 2). The page has exactly one wink left, the heading "Keep the log." That is the one word the
  owner has already turned down ("The log, not really").
- **Reads on a phone.** Yes. The phone sheet is 527 px at 390, short enough. One wrap leaves a two-word stub line
  ("start URL;"), and the image repeats itself in two places a phone reader pays for (findings 3, 4).

So the structure passes the owner's test and the words don't yet. That's my department.

## Findings

1. **The hazard gives the wrong cause.** "never ends by itself: no page or depth limit, and the parent domain counts
   as same-site." The colon says the crawl runs forever because its scope is unbounded. The run check proves
   otherwise. The `ends_by_itself` probe crawled a **3-page** site, which had all three pages written by the 45 s
   mark (`crawl_ctrl_c`: "3 lines"), and it was "still running at 150 s". Scope has nothing to fetch on a 3-page
   site. The real cause is in Ben's own issue #65: the completion check "sits in the `else =>` arm of
   `tokio::select!`", which "only runs when every branch is disabled". It is in 0.1.3 at
   `sdist:src/bfs_crawler.rs:550` (`else => { if self.frontier.is_empty() && in_flight_tasks.is_empty() { …
   "Crawl complete" … break`). tokio's docs say the same: "If all branches are disabled … Evaluate the `else`
   expression." Both halves are true and the colon between them is false. Round 2 fixed this exact fault in W1, and
   round 1 brought it back here when it merged H1. A stranger who reads the line limits the scope and still waits
   forever.

2. **The danger mark reads as a Rust comment.** At 870 and at 390, the hatch draws as a red `//` immediately to the
   left of the hazard line. The image is full of `.rs` file names. In Rust, `//` is "an ordinary comment …
   interpreted as a form of whitespace" (Rust Reference), so a programmer reads the row as "this line is switched
   off". That is the opposite of "don't miss this". Round 1 said the hatch only says "warning". This is a different
   point: for this audience the hatch says something wrong. Charts already have the right mark. The danger line
   (INT 1 / Chart 1, K1) "draws attention to a danger which would not stand out clearly enough if represented
   solely by its symbol", and it is drawn as a dotted line around the danger. A dotted border on the band is a
   chart's own habit and needs no explaining. Slashes are a coder's habit.

3. **The image says two things twice in ten lines.**
   - "Crawls a site and writes **one line for every page** it reaches." (header), then "**one line per page**: url,
     depth, status_code, title, …" (end row).
   - "press Ctrl-C once: that writes **data/sitemap.jsonl**; …", then **`data/sitemap.jsonl`** on the next row,
     under the end bar.

   STRINGS-TWICE checks the hero against the README, not the hero against itself. On the phone, each repeat costs a
   line of 14 px text.

4. **Who does what isn't clear.** "fetch a page" (the tool) and "press Ctrl-C once" (you) are both imperatives. So
   the one thing the visitor must do looks no different from what the crawler does. The other rows switch to third
   person or passive ("fetches fewer pages", "saved every 50 ms", "never ends"). Google's style guide asks for "the
   imperative for instructions" and "the third person for what the software … does". Microsoft's asks for the
   imperative for customer actions. S1 is a fragment followed by a semicolon ("start URL; by default also …"). On
   the phone it breaks right after the semicolon and leaves "start URL;" alone on its line.

5. **Code is set in two faces.** `data/sitemap.jsonl` is in mono on the end row and in sans on the Ctrl-C row.
   `export-sitemap` (a subcommand) and `url, depth, status_code, title` (struct fields) are in sans. File names and
   the import path are in mono. Google's "Code in text" list puts filenames and paths, command-line utility names,
   method names and "database elements (such as row and column names)" in code font. On the desk the image already
   mixes faces in one line (R15: label, then a `machine` path), so the sheet can do it.

6. **The data line claims more than the drawing does.** "The drawing is rustmapper 0.1.3 from PyPI: every file it
   names is in that release". The drawing names `data/sitemap.jsonl`, an output file. On desk it also names
   `scripts/import_rust_sitemapper.py`, which is in ideal-url-organizer, not in rustmapper. The claim is true only of
   the three `.rs` labels. Also "its install, crawl …, Ctrl‑C, kill and export lines ran": lines don't run.

7. **Pronouns with no clear antecedent, and a cross-reference that teaches nothing.**
   - Rule 4's cite: "ideal-url-organizer, Nov 2025; Claude wrote its first version." "Its" could be the
     repository, the rule or the parser. `stats.json rules[4]` says something narrower. The first `urllib.parse` in
     the repo is Claude's (`6e8087f`). His own first is `2be623e`, 13 Nov 2025. Google's pronoun rule is to
     "repeat the noun".
   - The Also line "Home of the "no regex" rule." points at a rule two screens down. It tells the visitor nothing
     the rule doesn't, and the rule now credits Claude first.

8. **"Keep the log." is the last theme wink, and the one the owner has already turned down.** Rule 2 is headed by
   two slogans, "Keep the log. Raw before clean." The second says what the rule says. The first is a double
   meaning: the write-ahead log, and the log a ship keeps. He said "The log, not really", and round 2 renamed rule 3
   for the same fault. "Raw before clean." can stand alone.

9. **The page switches person.** It opens in the third person ("**Ben Russell builds** …") and ends in the first
   ("3 % of **my** commits …; … not counted as **mine**"). Google's style guide: identify who the reader is "and be
   consistent about that". The owner's profile is about him, in his name, so the third person is the one to keep.

10. **The license line promises what forking no longer gives.** "To make your own, fork the repository, fill in
    `chart.toml` and run the workflow; the images are regenerated from your repositories." The hero is now a
    hand-written route with anchors into one project. `scripts/sheets/route.py` has `PROJECT = "rustmapper"`, and
    `route.repo` falls back to `"Rust-sitemap"`. A fork that fills in `[identity]` gets rustmapper's route, or a
    ROUTE-UNVERIFIED failure. It doesn't get a picture of its own repositories.

11. **The rustmapper sentence describes a package the reader can't install.** "a concurrent sitemap crawler written
    in Rust, with a CLI and a Python package built with maturin." The wheel `pip install rustmapper` fetches
    contains four entries: `METADATA`, `WHEEL`, `RECORD` and `rustmapper-0.1.3.data/scripts/rust_sitemap`. There is
    no importable module. The Python API (`python/rustmapper/__init__.py`, pyo3) exists only on main. The facts line
    under the sentence is labelled "On main"; the sentence isn't, and the code block under both installs 0.1.3.

12. **The Scrapy block's warning comes after the line it warns about.** The note "The bundled config's sample URLs
    are a university's site; the last line points discovery at yours" sits under the block. In the block,
    `python start.py` runs first, and it calls `docker-compose up -d`. That starts the `scraper` service (container
    name `uconn-scraper`, `CMD python -m src.main`, the pipeline orchestrator) on the bundled config, with seed file
    `data/raw/uconn_urls.csv`. Someone who pastes the block from the top has started the sample crawl before they
    reach the line that points it at their own site.

Smaller items, no must-fix: "Raw pages land in Delta Lake and stay raw" says "raw" twice. Rules 1 and 3 both turn
on "watching" ("still running after you have stopped watching it" / "a crawler you cannot watch"), and read one
after the other they almost argue. The desk sheet's left column is empty under the role line. That's not a copy
matter, and no fact needs the space.

## Figures checked

| Printed | Key / source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.date`, `.uploads[3].time` | 0.1.3, 2025-11-08T19:52:41 | yes |
| `pip install rustmapper` → `rust_sitemap` (README block) | `edition.scripts`; wheel listing | `["rust_sitemap"]`; only `…/scripts/rust_sitemap` | yes |
| seeder.rs, bfs_crawler.rs, writer_thread.rs | `routes` S1, F1, W1 `paths.release` | all three in `sdist/src/` | yes |
| "by default also sitemaps, certificate logs, Common Crawl" | `sdist:src/cli.rs:58` | `default_value = "all"` | yes (release) |
| "saved every 50 ms" | `sdist:src/writer_thread.rs:11` | `BATCH_TIMEOUT_MS: u64 = 50` ("Drain batches every 50 ms") | yes |
| "after a kill, export-sitemap still works" | `runcheck` `export_after_kill` | 3 `<loc>` | yes |
| "never ends by itself" | `runcheck` `ends_by_itself` | still running at 150 s, 3-page site | yes |
| "…: no page or depth limit, and the parent domain counts as same-site" (as the cause) | `sdist:src/bfs_crawler.rs:550`; issue #65 | the cause is the unreachable `else =>` completion check | **no** (finding 1) |
| "parent domain counts as same-site" (as a fact) | `sdist:src/url_utils.rs:81-91` | `base_domain.ends_with(url_domain)` branch | yes |
| "a second press or a kill skips it" | `kill_writes_file` | SIGTERM, file not written | yes |
| url, depth, status_code, title | `routes` R13; `sdist:src/state.rs` | in `SitemapNode` | yes |
| "read by ideal-url-organizer … with a test" | `handoffs[0]` | 15 reader fields ⊆ writer, test present | yes |
| 176 tests · 16k lines of Rust · CI passed 7 Oct 2026 · `32c2651` | `repos[Rust-sitemap]` | 176; 16,390; success 2026-10-07; head `32c2651` | yes |
| 1,920 tests · 69k lines of Python · CI passed 8 Oct 2026 · `96e7a1a` | `repos[Scrapy]` | 1,920; 69,036; success 2026-10-08 | yes |
| 3 min from a cold cache on a 4-core Linux x86_64 machine | `runcheck.steps[install]` | cold, 4 CPUs, 168.2 / 171.4 / 174.3 s | yes |
| 22 public repositories; 15 more | `repo_count`; 22 − 1 − 2 − 4 | 22; 15 | yes |
| ran on 10 Oct 2026 (Linux x86_64) | `runcheck.date`, `.runner` | 2026-10-10, Linux x86_64 | yes |
| 3 %; 297 | `coauthored_total.agent_share`; `agent_authored.total` | 0.031; 297 | yes |
| 25 ways; 50,000 characters; stage 3; stage 4; localhost:3000 | `figures[]` | all `holds: true` | yes |
| Sep 2025; Oct 2025; Nov 2025 (rules) | `rules[]` | fd33c11 29 Sep; 52dcbd8 4 Oct; 4334458 3 Nov; d571e6e 1 Oct; e8cbe15 6 Oct; 2be623e 13 Nov | yes |
| "every file it names is in that release" | drawing vs sdist | `data/sitemap.jsonl`, `scripts/import_rust_sitemapper.py` aren't | **no** (finding 6) |
| "a Python package built with maturin" | 0.1.3 wheel | binary only, no module | **not for what pip installs** (finding 11) |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page | keep | |
| Role line, two caps lines | crawlers and data, Python and Rust | keep | the drawing proves it; see the README's "builds" line below |
| "rustmapper" serif | which project | keep | |
| "Crawls a site and writes one line for every page it reaches." | what it does | keep | the best line in the image; the end row should stop repeating it |
| Start bar | where you begin | keep | |
| `pip install rustmapper` | the door | keep | the image's one command |
| "0.1.3 · 8 NOV 2025" | the release, and its age | keep | |
| Track (magenta) | read top to bottom, one way through | keep | the theme's one quiet mark that works |
| S1 ring + `seeder.rs` + "start URL; by default also …" | where URLs come from; what it contacts by default | change | the fragment and the phone stub (finding 4) |
| F1 ring + `bfs_crawler.rs` + "fetch a page; …" | it's a crawl loop | change | third person, so it doesn't read as your step (finding 4) |
| G1 tick + "fetches fewer pages at once when saving falls behind" | it slows itself down to the store | keep | the tick-not-ring difference holds |
| W1 ring + `writer_thread.rs` + "saved every 50 ms: after a kill, export-sitemap still works" | a kill doesn't lose the crawl | change | `export-sitemap` in mono; third person "saves" (findings 4, 5) |
| Loop line + up arrow | which rows repeat | keep | the one thing only a drawing shows |
| H1 band | the row to read first | keep | does its job; ink on it is 10.3:1 by day |
| H1 hatch `//` | "danger", or to a programmer "commented out" | change | replace with a dotted danger line on the band's edge (finding 2) |
| H1 text | the catch | change | false cause (finding 1) |
| C1 ring + "press Ctrl-C once: that writes data/sitemap.jsonl; …" | your only action, and what each exit leaves | change | drop the repeated file name (finding 3) |
| End bar | where you end up | keep | |
| `data/sitemap.jsonl` + "one line per page: url, depth, status_code, title, …" | the output and its real fields | change | drop "one line per page", set the fields in mono (findings 3, 5) |
| Hand-off line + arrow + "read by ideal-url-organizer: …, with a test" | his projects connect, and the join is tested | keep | the only line about the body of work |
| Night editions | the same in dark | keep | band 8.4:1, hatch 5.1:1 by night |
| Phone edition | the same, stacked | keep | one stub wrap (finding 4) |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image | how to run his main tool, how it behaves | change | findings 1–5 |
| Alt text | the image in 25 words | keep | true, and unaffected by finding 1 |
| Link line | where to go | keep | |
| "Ben Russell builds crawl and data infrastructure: …" | who he is | change | "crawl and data infrastructure" is word for word the role line 60 px above it. Start at the list: "Ben Russell builds web crawlers, discovery pipelines, raw-first storage, and the dashboards that watch them." |
| Languages, Stack | what he uses | keep | |
| rustmapper sentence | what it is | change | finding 11 |
| rustmapper facts line | tested, alive, how big, which snapshot | keep | |
| Install block + wheel note | how to start it, when pip just works | keep | |
| Scrapy sentence, facts | the second project | keep | |
| Scrapy code block + note | how to start it, three catches | change | finding 12 |
| Scrapy bullets | how it's built | keep | "stay raw" is minor |
| Also | the next four | change | cut "Home of the "no regex" rule." (finding 7) |
| 15 more | the rest, folded | keep | |
| Working rules | how he works, each with dated proof | change | rule 2 heading (finding 8), rule 4 cite (finding 7) |
| Found a mistake? | the page can be corrected | keep | |
| Data line | what was checked and run | change | findings 6, 9 |
| License line | terms, how to fork | change | finding 10 |

## Must fix, ranked

1. **H1: state the cause the run check measured.** In `chart.toml [route.rustmapper]`, set H1 to "never ends by
   itself, even after its last page: a 3-page site ran past {secs:ends_by_itself} s". Print 150 from
   the probe, the way the existing `instead` already does. Add a release anchor `{path = "src/bfs_crawler.rs", text
   = "Crawl complete: frontier empty"}` and keep `fails = ["ends_by_itself"]`. Drop the scope clause from this row.
   If it stays anywhere, it goes in the README text as a separate fact, not as the reason. The new text is 76
   characters, under today's 87, so the desk stays on one line and the phone stays at two. Keep the `--max-urls`
   instead for 0.1.4. Add a T-ANCHOR case: a trap whose probe fails on a fixture smaller than any limit it names
   can't print that limit as its cause. Why: the row the band tells you to read first has to be true.
2. **Replace the `//` hatch with a dotted danger line** (`scripts/sheets/route.py`, trap drawing). Remove the three
   45° strokes. Draw the H1 band's outline as a dotted line in `accent`: round dots of 2.1 units (LINE weight),
   spaced 5 units centre to centre, on all four edges (desk and phone). Keep the 14 % fill. Contrast as a graphic
   is 4.1:1 by day and 6.1:1 by night (over 3:1). T-NOSIZE holds, because the size still follows the text lines.
   Update CONTRAST-BAND and the `bounds` check (dots inside the band's box). Why: in a picture of Rust files, red
   `//` means "ignored". A dotted line around a danger is the chart's own sign for "unsafe; don't miss it".
3. **One home per fact inside the image, too.** R13 text becomes "fields: `url, depth, status_code, title, …`".
   C1 becomes "press Ctrl-C once to write the file below; a second press or a kill skips it", and its `instead`
   becomes "… a second press skips it". New fast check HERO-SELF-TWICE: no code token (`_`, `--`, `.rs`, `.jsonl`,
   a `/` path) and no run of 4 or more words appears twice in one edition's text. The alt text is exempt.
4. **Separate your step from the tool's** (`chart.toml`). The tool's rows go in the third person; the user's in the
   imperative. S1 becomes "your URL, plus by default sitemaps, certificate logs, Common Crawl" (66 characters,
   with no semicolon to make a stub line). F1 becomes "fetches a page; same-site links go back on the queue". W1
   becomes "saves every 50 ms, so after a kill `export-sitemap` still works". C1 stays imperative (must-fix 3). The
   anchors don't change. Why: on a route, the one action that's yours should be the one that reads like an order.
5. **One face for code** (`scripts/sheets/route.py` label runs). Inside label text, set backticked spans in
   `machine` at the same size, as R15 already does. Apply it to `export-sitemap` and the R13 fields. New render
   check TYPE-CODE: a label run containing `_`, `--`, `.rs`, `.jsonl` or a known subcommand outside a `machine`
   span fails.
6. **Make the data line say what's true** (`render_readme.py`, `survey` marker). Change "every file it names is in
   that release" to "every source file it names is in that release". Change "its install, crawl (…), Ctrl‑C, kill
   and export lines ran on" to "its install, crawl (…), Ctrl‑C, kill and export lines were run on". Use the third
   person: "3 % of Ben's commits carry an AI co-author trailer; 297 more were written by coding agents (Claude,
   jules) and are not counted as his." Add a test: no first-person pronoun (`I`, `my`, `mine`, `me`) in the
   README's visible text outside quoted code.
7. **Rule 2 and rule 4, and the Also line** (`chart.toml [[notices]]`, README "Also"). Rule 2's heading becomes
   "**Raw before clean.**" Rule 4's cite becomes "ideal-url-organizer, Nov 2025; Claude's commit used it first."
   The `names_agent` gate still passes. Cut "Home of the "no regex" rule." from the ideal-url-organizer line. Why:
   the last double meaning on the page goes, and so do a pronoun with three possible antecedents and a pointer that
   teaches nothing.
8. **License line** (`render_readme.py` license block). Change it to: "To make your own, fork the repository and
   write your project's route in `chart.toml` (`[route.<name>]`, each line with the code it rests on); the build
   draws only the lines your code and its run check prove." If `route.py` keeps `PROJECT = "rustmapper"` fixed,
   either read the name from `chart.toml` or say plainly that the hero is rustmapper's. Why: a promise on the page
   that the code doesn't keep is the "doesn't look exactly accurate" complaint again.
9. **The rustmapper sentence** (`chart.toml [copy]` or `render_readme.py`). Change it to: "**rustmapper** is a
   concurrent sitemap crawler written in Rust. `pip install` gives you its command line; the Python API built with
   maturin is on main, not yet released." Gate the second clause on `edition.scripts` being non-empty and the
   wheel having no `rustmapper/__init__.py`. Once a release ships the module, it reads "…, with a CLI and a Python
   API built with maturin."
10. **Scrapy block: warn before the line, not after** (`render_readme.py` Scrapy block). Put
    `# crawls a university's sample site` (35 columns) above `python start.py`, and
    `# or only discovery, on your own site:` above `scrapy crawl scout`. The note under the block keeps Grafana and
    the spider name, and drops "The bundled config's sample URLs are a university's site; the last line points
    discovery at yours." README-CODE-WIDTH still holds.
11. **The "builds" line** (`chart.toml [copy]`). Change it to "**Ben Russell builds** web crawlers, discovery
    pipelines, raw-first storage, and the dashboards that watch them." Why: the role line in the image already says
    "crawl and data infrastructure", 60 px higher.

## Sources (fresh this round)

1. tokio, `select!` macro documentation: "If all branches are disabled: go to step 6 … Evaluate the `else`
   expression." https://docs.rs/tokio/latest/tokio/macro.select.html (finding 1, must-fix 1)
2. BenjaminSRussell/Rust-sitemap issue #65, "Crawl never exits after the frontier drains (completion check
   unreachable in select! else arm)", closed 2026-10-07: "all 21 URLs were fetched in about 1 s, but the process was
   still running at 120 s". https://github.com/BenjaminSRussell/Rust-sitemap/issues/65 (finding 1)
3. Rust-sitemap commit `d751cf0`, "Exit crawl when idle: run completion check on a timer, not select! else (closes
   #65)", 7 Oct 2026, and `sdist rustmapper-0.1.3:src/bfs_crawler.rs:550` (the `else =>` arm).
   (finding 1)
4. The Rust Reference, "Comments": line comments are `//`; "Non-doc comments are interpreted as a form of
   whitespace." https://doc.rust-lang.org/reference/comments.html (finding 2, must-fix 2)
5. Canadian Hydrographic Service, Chart 1, section K, "Rocks, wrecks, obstructions": "A danger line draws attention
   to a danger which would not stand out clearly enough if represented solely by its symbol … or delimits an area
   containing numerous dangers, through which it is unsafe to navigate."
   https://cartes.gc.ca/publications/chart1-carte1/sections/k-rocks/general-eng.html (must-fix 2)
6. IHO CSPCWG, "Sections K–L of INT 1" (CSPCWG7-11.3A), on the K1 danger line as the generic symbol drawing "the
   navigator's attention to a danger". https://legacy.iho.int/mtg_docs/com_wg/CSPCWG/CSPCWG7/CSPCWG7-11.3A_sections_K-L_of_INT1.pdf
   (must-fix 2)
7. web.dev, "Understanding same-site and same-origin": same-site is "the same scheme and the same eTLD+1";
   "different subdomains don't matter". https://web.dev/articles/same-site-same-origin (finding 1: to a web
   engineer "the parent domain counts as same-site" says nothing surprising, which is another reason to take it out
   of the hazard)
8. Google developer documentation style guide, "Code in text": code font for "filenames, filename extensions … and
   paths", "command-line utility names", "database elements (such as row and column names)".
   https://developers.google.com/style/code-in-text (finding 5, must-fix 5)
9. Google developer documentation style guide, "Second person": "Use the imperative for instructions"; "use the third
   person for what the software … does"; identify the reader and "be consistent about that".
   https://developers.google.com/style/person (findings 4, 9; must-fix 4, 6)
10. Google developer documentation style guide, "Pronouns": a pronoun must point clearly to its noun; otherwise
    repeat the noun. https://developers.google.com/style/pronouns (finding 7, must-fix 7)
11. Microsoft Writing Style Guide, "Verbs" and "Writing step-by-step instructions": the imperative is for customer
    actions and procedures. https://learn.microsoft.com/en-us/style-guide/grammar/verbs ;
    https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions
    (finding 4)
12. rustmapper 0.1.3 wheel, `cp313-cp313-macosx_11_0_arm64`: four entries, no Python module
    (`scratchpad/r6/pypi-wheel/w.whl`); Rust-sitemap `pyproject.toml` (`bindings = "pyo3"` on main). (finding 11)
13. Scrapy `Scraping_project/start.py:33, 345, 353` (`LOCAL_SEED_FILE = data/raw/uconn_urls.csv`,
    `docker-compose up -d`), `docker-compose.yml:8-12` (`scraper`, `container_name: uconn-scraper`), `Dockerfile`
    (`CMD ["python", "-m", "src.main"]`), `src/main.py` (runs the pipeline orchestrator). (finding 12)
14. This repository: `scripts/sheets/route.py` (`PROJECT = "rustmapper"`), `render_readme.py:246` (the license
    text). (finding 10)
