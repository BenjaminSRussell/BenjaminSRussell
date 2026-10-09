# Concept D: what his repositories hand each other, and which hand-offs run today

Round 6, 9 Oct 2026. One concept for the first image and the page around it. The image answers "what is it showing?" in
one sentence:

> **Which of his repositories feed which, through what file, and whether the receiving side actually reads it today.**

This is the honest version of the half of the current image the owner said he could see: "it shows you where the
repos are". Here a repository's place on the drawing means something you can check. It sits on the sending or the
receiving side of a file that crosses between two of his projects. Each line between two projects says three things:
what crosses, who reads it, and whether that reading works on today's code.

Citations: `R6-F5` means round-6 research file R6, finding F5. `N1`–`N4` are sources added in this memo (section 10).
Code is cited as `repo:path:line` in the clones under `scratchpad/clones/` (default branch HEADs, 9 Oct 2026). Git
history is cited by short sha from the bare mirrors (`<repo>.git`).

---

## 1. Why this angle, and what the other concepts miss

**The finding the other angles pass over.** Every research file looks for the geography inside one project: the route a
URL takes through rustmapper (R1-I3, R3 impl. 2, R6 impl. 1, concept A) or a crawl of one site (R7-I2). R6-F5 points
at a different geography and then leaves it: "This is the one geography no single repository draws: a URL found by
rustmapper can be organised by url-organizer and was meant to feed Scrapy's stages." I followed that thread through
the code. The repositories are joined by **six declared hand-offs** (files one project writes for another). I checked
each one from both ends, writer and reader, and they come out in three states:

- **1 runs.** rustmapper's `sitemap.jsonl` is read by ideal-url-organizer's importer, and a test feeds the importer a
  record.
- **2 are written for a reader whose code expects other fields.** Data-visualizer was built on 27 Oct 2025 around the
  record rustmapper wrote that week. Three days later rustmapper replaced `links` with `link_count`, and
  Data-visualizer's validator still requires `links`. Separately, rustmapper exports a Delta table named
  `stage1_discovery` "for Scrapy". Scrapy's table of that name has 9 columns, and 5 of them are missing from the
  export.
- **3 exist only on the sending side.** ideal-url-organizer's `seeds.jsonl` is meant for rustmapper and for Scrapy, and
  Course_crusader's `courses.parquet` is meant for Data-visualizer. No code in any of the receivers reads them.

None of this is written anywhere a visitor would see it. Each sending README describes its own export as if the
hand-off were done (`Rust-sitemap:README.md:141` "Handoff to Scrapy"; `ideal-url-organizer:README.md:525`;
`Course_crusader:README.md:58`). Only reading both sides shows the state.

**Why this is a picture's job.** The sea-chart tradition has a distinction for exactly this, and it is the strongest
reason I found for drawing anything. The Coast Pilot separates a channel's **project depth**, "the planned dredging
depth of a channel [that] may not reflect surveyed conditions", from its **controlling depth**, "the least known depth
of a channel as determined by hydrographic surveys". It warns that "project depth must not be confused with
controlling depth", that depths "may vary considerably between maintenance dredging", and that depths "reported by
owners ... have not been verified" (N1, ch. 1, ¶25.001–27, page dated 04 Oct 2026). A sending README is the owner's
report: the planned depth. The receiving code plus a test is the survey: the controlling depth. The image prints only
the surveyed state, re-checked every week, the way Coast Pilot files are "posted weekly" (N1; R2-F11). The image never
names any of this. It just keeps the two apart (R1-I13, the owner's "if it looks like a shoe").

**Why this beats the obvious options.**

| Option | What it teaches | Why D is stronger for the owner's goal |
|---|---|---|
| Current week-islands | when he committed | Fails every test in R5 (relation, true inferences, only facts, channel). D's positions come from real joins in code, not the calendar (R3-F1, R5-F7). |
| A: route through rustmapper | how one crawler works inside | True, but it is one project's internals, which is the project README's job (R6-F13: Scrapy already draws its own route twice). It answers "how does it work?" A profile visitor first asks "what is all this, and what goes together?" (R6-F12, Shneiderman's overview first). D is the overview, and A's route stays in the rustmapper text block, where it already reads well (R4 impl. 10). |
| C: one card per project | is each project ready, how do I start it | Cards are lookups, and the text can carry them (R3-F4, R5-F10). They show each project alone, which is the "21 separate islands" impression the owner rejected. D shows the projects are one body of work, which is the main thing a visitor should learn (R6-F1). |
| Map of a real crawl (R7-I2) | what his crawler finds on one site | Needs a crawl with a permitted target that no repository holds yet (R6 impl. 11, R7-I5). D needs no new data collection, only reading code that already exists. |
| A C4 container diagram of everything | what the boxes are | C4 draws intended relations (R3-F10). D draws only relations that are verified, and marks the planned ones as planned. That difference is the whole point (N1). |

**Precedent for the form.** Beck's 1931 Underground diagram dropped the physical layout because "only the topology of
the route mattered" to a traveller. Connections were emphasised and interchanges marked, and it "immediately became
popular" (N2). Distance on D means nothing. What matters is who connects to whom. This is the C4 rule that "every line
should be labelled" (R3-F10), applied to the joins between projects, not the boxes inside one.

**What a visitor gets from D that the text does not give faster.** (1) rustmapper is the hub. Three of his other
projects take its output. That is a degree you see at a glance, and it tells the visitor which repository to open
first (R4-F5). (2) The work forms a loop: crawl, then organise, then choose the next crawl's seeds. A list of 21 names
hides this. (3) The state of every join, by line style, without reading a sentence. The working line is the most
prominent mark, because prominence should follow importance (R1-F1, S-52; R3 impl. 4). (4) The file formats he works
in (JSONL, Delta, Parquet), with each one shown where it crosses.

---

## 2. The hand-offs as found (the data the image draws)

Every row was checked in both clones. "Reader" means code in the receiving repository that opens this file or table.

| # | From → To | What crosses | Writer (evidence) | Reader (evidence) | State on 9 Oct 2026 |
|---|---|---|---|---|---|
| H1 | rustmapper → ideal-url-organizer | `data/sitemap.jsonl` | `Rust-sitemap:src/lib.rs:292` | `ideal-url-organizer:scripts/import_rust_sitemapper.py:1-48` keeps 15 fields, all present in `Rust-sitemap:src/state.rs:131-147`; test `tests/test_import_rust_sitemapper.py` (added `80dba9e`, 8 Aug 2026) | **runs**: reader exists, fields match, a test feeds it a record |
| H2 | rustmapper → Data-visualizer | `data/sitemap.jsonl` | same | `Data-visualizer:analysis/data_validator.py:59` requires `url, depth, status_code, content_type, links`; `run.sh:296-297` runs it before every `analyze` unless validation is skipped | **fields differ**: `links` was dropped from rustmapper in `f77b002` (30 Oct 2025, "-    pub links: Vec<String>"). The validator dates from `a46b9e0` (27 Oct 2025). Its committed `data/input/sample.jsonl` has the 14 fields of rustmapper's `SitemapNode` at `c1f32ee` (27 Oct 2025, `src/node_map.rs:32-47`), in the same order, and was crawled 27 Oct 2025 06:43–06:47 UTC (`discovered_at` 1761547389). No other clone uses that record (`grep url_normalized` finds only these two) |
| H3 | rustmapper → Scrapy | Delta table `stage1_discovery` | `Rust-sitemap:python/rustmapper/export_parquet.py:30-52` (21 columns; added `32c2651`, 7 Oct 2026) | Scrapy has a table of that name, `Scrapy:Scraping_project/src/core/schemas.py:12-22`, 9 columns. No Scrapy file names rustmapper or Rust-sitemap (grep, `.py` and `.md`) | **fields differ**: the export lacks `url_hash, is_heavy, is_dynamic, status, queued_at`, 5 of Scrapy's 9. `url_hash` is also Scrapy's z-order key (`lakehouse_manager.py:401`) |
| H4 | ideal-url-organizer → rustmapper | `seeds.jsonl` | `ideal-url-organizer:src/export/seeds.py:1-13`; test `tests/test_export_seeds.py` (added `94fe6b6`, 7 Oct 2026) | none. `Rust-sitemap:src/cli.rs:17-18` takes a single `start_url: String`, and no code reads a seed file | **no reader** |
| H5 | ideal-url-organizer → Scrapy | `seeds.jsonl` | same | none. `Scrapy:.../src/lakehouse/seed_manager.py` has `add_urls_to_seeds` and `bulk_seed_from_list` (lines 166, 328), which take lists. Nothing reads `seeds.jsonl` | **no reader** |
| H6 | Course_crusader → Data-visualizer | `courses.parquet` | `Course_crusader:coursecrusader/cli.py:330`, `database.py:926` (added `f70c743`, 7 Oct 2026) | none. `grep -i parquet` over Data-visualizer finds nothing | **no reader** |

Repositories with no hand-off in either direction are not drawn. go_go_go is one of them, even though it is
rustmapper's Go twin: its `data/sitemap.jsonl` has a different schema (`go_go_go:internal/types/types.go:63-78`, no
`links`, no `content_type`), and nothing reads it. It goes in the text with what differs (section 6).

---

## 3. How the image encodes things (the same on every edition)

| Visual variable | What it means | Why this channel | Evidence |
|---|---|---|---|
| Left or right column (desk); block order (phone) | sends or receives. The left column holds repositories whose outgoing lines are drawn there. ideal-url-organizer receives on the right and sends back left, so the loop shows | Position carries the one relation that is real: direction of hand-off. Nothing else is placed by position, so closeness implies nothing false (R3-F2, R5-F4) | R3-F1, R5-test 2 |
| A line with an arrow | a file one project writes for another, pointing at the reader | A line is a path, and here it is one (R5-F4: readers take a line as a way through) | R3-F10 (C4: every line labelled) |
| **Solid magenta line, 2.5 px, filled arrowhead** | runs: a reader exists and the fields match | On a chart, magenta marks what you act on (R1-F6, I9). This is the one join a visitor can use today, so it is the most prominent mark (R1-F1, S-52) | R1-F6; R3 impl. 4 |
| **Solid ink line, 2 px, with a 2 × 12 px red bar across it 12 px before the arrowhead** | fields differ: both sides have code, but they disagree on the record | The bar sits where the join fails, at the reader, the way a danger mark sits on the hazard (R1-F9, F10). Red is used only here | R1-F9, F10 |
| **Dashed grey line, 1.5 px (4 on, 3 off), open arrowhead** | no reader: only the sending side exists | The least prominent mark is the planned-only state. The planned depth is kept visibly apart from the surveyed one (N1) | N1; R2-F11 |
| Label above a line, monospace | the file or table that crosses | The repository's own file name, so a visitor who opens the repository finds the same words (R3 impl. 12) | R3 impl. 12 |
| Label below a line, sans | the state in plain words, naming the field that fails | One rule per line, readable without a key (R1-F10, R4-F12). There is no legend, because every line carries its own meaning | R4 impl. 13, R3 impl. 13 |
| Node: repository name + main language + four-word role | what the project is | Name and role first. The first two words of each line carry the meaning (R4-F3, impl. 5) | R4-F8 |

There is no area, no size-coded mark, no axis, no border graduation, no tint and no motion. Every node is the same
size, because nothing about a repository's size is being shown (R1-F16, R5-F6).

---

## 4. The image, exactly

### 4.1 Desk edition: 870 × 410 viewBox, drawn 1:1 in GitHub's 870 px column

Type: serif for the name (the face in use now), sans for everything else, mono for file names. **Nothing smaller than
13 px.** Margins 32 px. Ink, grey, magenta and red come from the existing token set in day and night.

**Title band (y 0–100)**

| Element | Position, size | Text |
|---|---|---|
| Name | x 32, baseline y 56, serif 40 px | Ben Russell |
| Role line | x 32, y 82, sans 13 px caps, tracking 0.08 em | CRAWL AND DATA INFRASTRUCTURE · PYTHON AND RUST |
| Fine print, line 1 | right-aligned x 838, y 56, sans 13 px caps, grey | WHAT 5 OF 21 REPOSITORIES HAND EACH OTHER |
| Fine print, line 2 | right-aligned x 838, y 76, same | CHECKED ON EACH DEFAULT BRANCH · 9 OCT 2026 |
| Rule | y 100, x 32–838, 0.75 px grey | (none) |

**Nodes** (name 16 px semibold; second line 13 px, language in caps, then the role)

| Node | Name baseline | Second line | Text of second line |
|---|---|---|---|
| rustmapper | x 32, y 146 | y 164 | RUST · crawls one site |
| Course_crusader | x 32, y 372 | y 390 | PYTHON · course catalogs |
| ideal-url-organizer | x 620, y 146 | y 164 | PYTHON · sorts a crawl 25 ways |
| Scrapy | x 620, y 252 | y 270 | PYTHON · four-stage crawl |
| Data-visualizer | x 620, y 322 | y 340 | PYTHON · PostgreSQL dashboards |

**Lines.** The corridor runs x 232–608. All lines are horizontal, vertical or 45°, as in the precedent (N2). There is
one junction dot, 4 px ink, at J (300, 150), where rustmapper's output splits.

| Line | Path | Style | Label above (mono 13 px) | Label below (sans 13 px) |
|---|---|---|---|---|
| H4 | (608,126) → (232,126), arrow at the left | dashed grey | `seeds.jsonl` · rustmapper takes one --start-url (one line, centred, y 119) | (none; the label above carries it, to keep 24 px clear of H1) |
| H1 | (232,150) → (608,150) | solid magenta | (none) | y 168 `data/sitemap.jsonl`; y 184 "read by import_rust_sitemapper.py, with a test" |
| H5 | (614,170) down to (614,240), arrow into Scrapy at y 246 | dashed grey | right-aligned x 606, y 204: `seeds.jsonl` | right-aligned x 606, y 220: "no reader in Scrapy" |
| H3 | J → 45° to (402,252) → (608,252) | ink + red bar at x 596 | right-aligned x 600, y 245: `Delta table stage1_discovery` | right-aligned x 600, y 270: "lacks url_hash and 4 more of Scrapy's columns" (red) |
| H2 | J → down to (300,318) → (608,318) | ink + red bar at x 596 | right-aligned x 600, y 311: `data/sitemap.jsonl` | right-aligned x 600, y 334: "needs links; rustmapper dropped it 30 Oct 2025" (red) |
| H6 | (232,368) → (600,368) → up to (600,338) → (612,338) | dashed grey | (none) | x 240, y 386: `courses.parquet` · no Parquet reader in Data-visualizer |

The builder may move any label by up to 8 px to clear a collision. The gate in section 7 rejects any overlap of text
with text or with a line.

### 4.2 Phone edition: 390 × about 770 viewBox, drawn 1:1 at 390 px

The graph unfolds into a tree: one block per sending repository, and under it one branch per line it sends. A
repository that both receives and sends (ideal-url-organizer) appears as a branch target under rustmapper and again as
a block with its own branches. That is the same graph, read top to bottom (R6 impl. 10, R7-I8). Side gutters are
16 px. **Nothing smaller than 13 px** (R1-I10).

| Band | y | Content |
|---|---|---|
| Title | name serif 40 px at y 52; role 14 px caps on two lines at y 80 and 98; fine print 13 px caps grey at y 122 and 140 | "Ben Russell" / "CRAWL AND DATA INFRASTRUCTURE" / "PYTHON AND RUST" / "WHAT 5 OF 21 REPOSITORIES HAND EACH OTHER" / "CHECKED ON EACH DEFAULT BRANCH · 9 OCT 2026" |
| Rule | y 156 | 0.75 px grey, x 16–374 |
| Block rustmapper | name 17 px at y 188; second line 13 px at y 206 | "rustmapper" / "RUST · crawls one site" |
| Trunk | x 26, y 216–414, 1.5 px ink | (none) |
| Branch H1 | segment x 26→58 at y 236 in H1's style; target 15 px at x 64, y 240; file mono 13 px at y 258; state at y 275 | "ideal-url-organizer" / `data/sitemap.jsonl` / "read by import_rust_sitemapper.py, with a test" |
| Branch H3 | segment at y 306; target y 310; file y 328; state y 345 (red) | "Scrapy" / `Delta table stage1_discovery` / "lacks url_hash and 4 more of its columns" |
| Branch H2 | segment at y 376; target y 380; file y 398; state y 415 (red) | "Data-visualizer" / `data/sitemap.jsonl` / "needs links, dropped 30 Oct 2025" |
| Block ideal-url-organizer | y 458 and 476 | "ideal-url-organizer" / "PYTHON · sorts a crawl 25 ways" |
| Branch H4 | segment at y 506; target y 510; file y 528; state y 545 | "rustmapper" / `seeds.jsonl` / "no reader: it takes one --start-url" |
| Branch H5 | segment at y 576; target y 580; file y 598; state y 615 | "Scrapy" / `seeds.jsonl` / "no reader in Scrapy" |
| Block Course_crusader | y 660 and 678 | "Course_crusader" / "PYTHON · course catalogs" |
| Branch H6 | segment at y 708; target y 712; file y 730; state y 747 | "Data-visualizer" / `courses.parquet` / "no Parquet reader in it" |

The name, the role line and both main projects (rustmapper at y 188, Scrapy at y 310) fall in the top 420 px, which is
the first phone screen (R4 impl. 6). The link line under the image starts the second screen.

### 4.3 Editions

The editions are day and night, at desk and phone size: four SVGs. With no motion, the four reduced-motion `<source>`
lines in `README.md:5-13` have nothing left to do and are deleted. The `<img>` fallback is the day desk edition, and it
must be legible on its own in the GitHub iOS app (R4 impl. 7).

### 4.4 Element table

Every element states (1) what a visitor learns, (2) why this form, (3) evidence, (4) the data it needs and whether
`build_stats` gathers it today.

| Element | (1) Visitor learns | (2) Why this form | (3) Evidence | (4) Data; gathered? |
|---|---|---|---|---|
| Name | whose page this is | the first of the six facts a screener reads; the largest type is read first | R4-F1, F4 | `chart.toml [identity]`; yes |
| Role line | what he builds, in the first two words | it states what the picture shows: crawl and data tools passing data on | R4 impl. 5; R5 impl. 10 | `chart.toml [copy]`; yes |
| Fine print 1, "WHAT 5 OF 21 REPOSITORIES HAND EACH OTHER" | what the drawing is, and that 16 repositories are left out of it | a chart states its subject and what was selected (R1-F2 title block). Naming the omission honestly (R1-I7) keeps a visitor from thinking these five are everything | R1-F2, I7; R5-F2 (titles carry recall) | 5 = node count from `handoffs`, **new**; 21 = `repo_count`, yes |
| Fine print 2, "CHECKED ON EACH DEFAULT BRANCH · 9 OCT 2026" | the states are measured, from the code, as of a date | the datum and the date are what a reader must settle before trusting the marks (R1-F2). A dated survey is what separates controlling depth from project depth (N1) | R1-F2, I8; R2-F11, I9; N1 | `taken`, yes; per-repository HEAD sha, **new** (`handoffs[].from_sha`, `to_sha`) |
| Node: name | which repository; the same spelling as the link line under the image | the repository's own name is a door into the code (R3 impl. 12). "rustmapper" is the PyPI and profile name, mapped from `Rust-sitemap` | R3 impl. 12; R4 impl. 11 | `chart.toml [hero.aliases]`; yes |
| Node: language | Rust feeds Python, so "Python and Rust" is concrete | a plain lookup fact, kept because it costs one word and makes the role line true on the drawing | stats `repos[].main_language` | yes |
| Node: four-word role | what each project does, enough to read the lines | a pilot entry opens with what the place is (R2-F2). Each role is a cut of the repository's own first line: `Rust-sitemap:README.md:3` "Concurrent web crawler"; `Course_crusader:README.md:3` "course-catalog scraper"; `Data-visualizer:README.md:3` "exploring and displaying data from PostgreSQL"; ideal-url-organizer `src/organizers/method_01`…`method_25`; Scrapy `src/stage1`…`stage4` | R2-F2; R4-F8 | `chart.toml [handoffs.roles]`, **new key**; each with a `source` line |
| H1 line + labels | the one chain that runs today: crawl with rustmapper, then hand the file to ideal-url-organizer | the most prominent mark, because it is the most useful fact, and it is the only line a visitor can act on (R1-F1, F6; R3 impl. 4) | section 2, H1 | **new**: `handoffs[H1]` state from a reader-path check, a test-path check, and fields ⊆ fields |
| H2 line, red bar, labels | Data-visualizer was built on rustmapper's October 2025 output, and today's output breaks its validator on one field | a hazard marked where it bites, with one rule (the field name), like a clearing line (R1-F10). It tells a visitor not to chain these two without changing one side, and it tells Ben the one-line fix | section 2, H2; R2-F3 | **new**: required fields parsed from `data_validator.py`, sender fields from `state.rs`, drop date from `git log -S` |
| H3 line, red bar, labels | rustmapper's "for Scrapy" export does not yet match Scrapy's table | same form as H2; the first missing column (`url_hash`) is named because it is Scrapy's key | section 2, H3 | **new**: columns from `schemas.py:12-22` and `export_parquet.py:30-52` |
| H4, H5 lines | ideal-url-organizer is meant to choose the next crawl, and the crawlers don't read its file yet | dashed and grey: the planned state, kept visibly apart from the surveyed one (N1). It shows the loop, which no list shows | section 2, H4–H5; R6-F5 | **new**: writer-path check plus reader search (no match = no reader) |
| H6 line | Course_crusader is built to hand course data on, and the receiver can't open Parquet yet | same as H4 | section 2, H6 | **new** |
| Junction dot J | rustmapper's one output goes three ways | marks the split on a single file, so three lines don't read as three different outputs | `Rust-sitemap:src/lib.rs:292` (one `sitemap.jsonl`) | geometry |
| Rule under the title | separates who he is from what is drawn | the only furniture; it carries no data and claims none | R1-F12 (furniture has a job: here, reading order) | none |

**Alt text** (the full content in words, because the image can't be read by a screen reader or clicked, R4-F16, impl.
12): "Ben Russell, crawl and data infrastructure in Python and Rust. What 5 of his 21 repositories hand each other,
checked on 9 Oct 2026: rustmapper's sitemap.jsonl is read by ideal-url-organizer, with a test. Data-visualizer needs a
links field rustmapper dropped on 30 Oct 2025. rustmapper's Delta export lacks 5 of the 9 columns of Scrapy's
stage1_discovery table. ideal-url-organizer's seeds.jsonl and Course_crusader's courses.parquet have no reader yet."
`chart.toml [alt]` builds this from `handoffs`.

---

## 5. What leaves the image, and why

| Removed | Reason |
|---|---|
| Week-islands, the "15 more" blobs | a week of commits is not a place; area is the weakest channel; and the owner's own question has no answer (R1-I2, R3 impl. 1, R5 table) |
| Blue shallows | blue means shallow and dangerous on a chart, but here it was "the exact 2-D buffer of the land" (R1-F6, R5-F5, F13) |
| Month axis and commit-day rows | time is not the subject; position must not be set by a date (R3 impl. 6, 11) |
| "Fl 30s" | a pun in a notation visitors can't decode, picking one of three configured values (R1-I6, R5 impl. 7) |
| "0.1.3 · PyPI" mark | true, but it belongs at the install line in the text with its date (R5-F13, R6 impl. 8) |
| Graduated dashed border | border graduations are scales for latitude and longitude. There are no coordinates here, so the border implies a measure that does not exist (R5-F5, Mackinlay) |
| Motion editions | nothing moves in the subject |

---

## 6. The page around the image

| Block | What it says | (1) Visitor learns | (2) Why here, in this form | (3) Evidence |
|---|---|---|---|---|
| Link line under the image | rustmapper · ideal-url-organizer · Scrapy · Data-visualizer · Course_crusader · PyPI · Email | the image can't be clicked, so its names are links straight under it, in the image's reading order | R4 impl. 8; R4-F13 |
| "Ben Russell builds …" + Languages + Stack | kept as is | the planning-guide facts, one line each | R2 I8 |
| rustmapper block | the "why" bullets as now. **The command block corrected** to `pip install rustmapper`, then `rust_sitemap crawl --start-url <your-site>` and `rust_sitemap export-sitemap …`, with the one-line platform note | the commands that work. Today's `rustmapper crawl` fails with "command not found" on the released wheel | R4-F17, impl. 9; R6-F6; wheel listing `scratchpad/r6/pypi-wheel/` |
| rustmapper block, new last bullet | "Its `sitemap.jsonl` feeds ideal-url-organizer (`scripts/import_rust_sitemapper.py`); the Delta export for Scrapy lacks `url_hash, is_heavy, is_dynamic, status, queued_at`." | the full list of missing columns, which the image shortens to "url_hash and 4 more" | section 2, H3; R6 impl. 2 |
| Scrapy block | as now, with two corrections: "summaries from BART-large-CNN" becomes "extractive summaries in Stage 3; BART-large-CNN for documents over 50,000 characters in Stage 4"; add the way in, `cd Scraping_project && python start.py` | what the project does, accurately, and how to start it | R6-F7, impl. 7; R2 I3; `stage3_worker.py:194-196`, `stage4/summarization.py:78-79` |
| Also | ideal-url-organizer, Data-visualizer, Course_crusader (one line each, all on the image); go_go_go rewritten: "rustmapper's crawler in Go, plus headless Chrome, SQLite search and browser TLS-fingerprint impersonation; its `sitemap.jsonl` uses a different schema"; rust_llm_logger; Ai_code_detector | each project's one shape in words. go_go_go's real differences are stated, not hidden behind "sibling" | R6-F9, F11, impl. 7, 9 |
| 15 more (details) | kept | side projects read as interest; a list, not a picture | R4-F5; R3 impl. 10 |
| Working rules | kept, each with the project and date it comes from. Rule 3 reworded plainly: "Dashboards in version one." | how he works, each rule tied to a file; the rarest README content is the "why" | R4-F8 (why = 2.7 %) |
| Measurement note | rewritten: "Hand-offs: a line is solid when the receiving repository has code that reads the file and its fields match the sender's current output; dashed when only the sender's code exists. Checked weekly on each default branch. Figures in the project lines are from clones of 21 public repositories, 9 Oct 2026." The co-author disclosure stays | it says what the image measures and how, so every mark has a definition | R1-I8; R2 I9; BRIEF standing rule |
| "Found a mistake? Open an issue" | kept | the correction channel, which keeps the guide true | R2-F11 (Hydrographic Notes) |
| License line | kept | legal | (none needed) |

---

## 7. What build_stats must gather (none of it exists today)

A new `handoffs` section in `chart.toml` declares each join once. `build_stats` verifies every declaration against the
clones at HEAD, through the same `read(repo, sha, path)` hook `claims.verify_scrape_interval` already uses
(`scripts/data/claims.py:97`, `scripts/build_stats.py:300`).

```toml
[[handoffs]]
id = "H2"
from = "Rust-sitemap"          # drawn as rustmapper via [hero.aliases]
to = "Data-visualizer"
file = "data/sitemap.jsonl"
writer = { path = "src/lib.rs", pattern = 'join\("sitemap.jsonl"\)' }
reader = { path = "analysis/data_validator.py", pattern = '"required": \[' }
fields = { to = { path = "analysis/data_validator.py", list = '"required": \[([^\]]*)\]' },
           from = { path = "src/state.rs", struct = "SitemapNode" } }
test = ""                      # optional; H1 sets tests/test_import_rust_sitemapper.py
```

State rules, computed at every build. A declaration cannot change a state; the code decides it.
- writer pattern not found → the line is **not drawn** and the build warns.
- reader path or pattern not found anywhere in the `to` clone → **no reader**.
- `fields.to` minus `fields.from` is not empty → **fields differ**, and the label names the missing fields in schema
  order. If one field is missing, its drop date comes from `git log -S'pub <field>'` on the sender, the date of the
  commit that removed it.
- otherwise → **runs**. The "with a test" label is printed only if `test` exists in the `to` clone.

`stats.json` gains `handoffs[]: {id, from, to, file, from_sha, to_sha, state, missing[], dropped_on, test}`.
`docs/data/AUDIT.md` gains one row per state rule and the definition "reader = code in the receiving repository that
opens this file, found by pattern at `to_sha`". "No reader" therefore means "none found by this search", and the
measurement note says so.

Gates for `scripts/check.py --tier render`:
- every label string on the SVG either comes from `handoffs[]` or from `chart.toml` with a `source`;
- no text box overlaps another text box or a line;
- no font size below 13 px on either edition;
- the H1 style is used only when `state == "runs"`.

---

## 8. Tests against the owner's goal (run at every review round)

1. **"What is it showing?"** Show the image alone for 10 s to someone who doesn't know Ben. Ask: which project feeds
   the others, and which join works? It passes when they say rustmapper, and rustmapper to ideal-url-organizer.
2. **"Is it based on the size of the project or how many commits?"** Ask what any mark's size means. The right answer
   is "nothing has a size", and no shape varies.
3. **Every mark traces.** For each line, a reviewer opens the writer and reader files at the shas in `stats.json`
   and finds what the label says.
4. **It changes when the code changes, and only then.** Add `links` back to `SitemapNode` in a scratch clone and
   rebuild: H2 turns magenta. A rebuild a week later with no code change gives a byte-identical SVG (R3 impl. 11).
5. **No theme words on the image** (grep the SVG text against the banned list in BRIEF).
6. **Phone.** At 390 px the name, the role line, rustmapper and Scrapy are within the first 420 px, and every label is
   at least 13 px.

---

## 9. Risks

- **It shows more open joins than working ones** (1 runs, 2 differ, 3 have no reader). That is the honest state. It
  also hands Ben a short, exact work list, and the image improves on its own as he closes each one. If he would rather
  not show planned joins, H4–H6 can be dropped as a group. H2 and H3 should stay, because the sending READMEs already
  claim them.
- **Four of the six writers date from 7 Oct 2026**, the bulk-merge day (`32c2651`, `94fe6b6`, `f70c743`; R3-F9). The
  code is real, but the drawing rests on recent work. The dates are in the audit rows.
- **H2 attributes Data-visualizer's input to rustmapper** from an exact 14-field match and the same day. No file in
  Data-visualizer names rustmapper. The label avoids claiming authorship, saying only "needs links; rustmapper dropped
  it", and both facts are in the code.
- **"No reader" is a search result.** A reader under an unexpected name would be missed. The patterns are declared and
  the audit says so.
- **Only five of 21 repositories appear.** The fine print says so, and the rest are in the text.
- **Web search budget**: the shared search limit for this turn was used up after one search. N1–N4 were fetched
  directly and read. A follow-up round could add sources on how readers interpret dashed and solid lines in node-link
  diagrams.

---

## 10. Sources added in this memo

- N1. NOAA Office of Coast Survey, *U.S. Coast Pilot 1*, Chapter 1 "General Information", page dated 04 Oct 2026,
  ¶25–27 "Depths" (controlling depth, project depth, "must not be confused", depths reported by owners not verified)
  and the opening section on weekly updates. https://nauticalcharts.noaa.gov/publications/coast-pilot/files/cp1/CPB1_C01_WEB.pdf
  (read; text extracted locally to `scratchpad/dl-cp1/cp1.txt`, lines 170–218).
- N2. "Tube map", Wikipedia, read 9 Oct 2026 (Beck 1931: "only the topology of the route mattered"; interchanges marked
  "to emphasise connections"; "immediately became popular"). https://en.wikipedia.org/wiki/Tube_map (read)
- N3. I. Robinson, "Consumer-Driven Contracts: A Service Evolution Pattern", martinfowler.com, 12 Jun 2006 (removing a
  field consumers rely on "will break existing consumers"). https://martinfowler.com/articles/consumerDrivenContracts.html (read)
- N4. Pact Foundation, "Introduction" (contract testing "checks each application in isolation" at an integration
  point). https://docs.pact.io/ (read)

N3 and N4 are why the state is decided at the reader (consumer) side, with field sets compared, rather than by the
sender's README.

Project evidence used beyond the round-6 files: the git history in section 2 (`c1f32ee`, `f77b002`, `a46b9e0`,
`80dba9e`, `94fe6b6`, `f70c743`, `32c2651`); `Data-visualizer:data/input/sample.jsonl` (40 records, www.hartford.edu,
depths 1–11); `Scrapy:Scraping_project/src/core/schemas.py:12-22`; `Rust-sitemap:python/rustmapper/export_parquet.py:30-52`;
`go_go_go:internal/types/types.go:63-78`.
