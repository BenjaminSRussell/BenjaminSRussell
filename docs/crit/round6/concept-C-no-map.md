# Concept C: no map. One card per project, in the order a stranger needs the facts

Round 6, 9 Oct 2026. This concept starts from what a visitor needs to learn and then picks the form. It does not start
from the theme. The answer is not a map. The first image becomes a printed card holding the five facts a stranger needs
before trying each of his two main projects: what it does, whether it is in working order, how to start it, and what
will trip them up. Fields are fixed and come in a fixed order. There is one card for rustmapper and one for Scrapy. On
the desk they sit side by side so the fields line up for comparison. On the phone they are stacked.

The nautical document this follows exists and does the same job: the **pilot card** of IMO Resolution A.601(15). A
pilot boards a ship they have never handled and has minutes to learn its current condition, how it handles and what is
not working. The card gives them that in a uniform format. A visitor opening an unfamiliar project is in the same
position. Nothing on the image names the form. It just works the way that form works.

Citations: `R2-F4` means round-6 research file R2, finding F4. `N1`–`N6` are the sources added in this memo (section 8).
Code is cited as `repo:path:line` in the clones (Rust-sitemap `32c2651`, 7 Oct 2026; Scrapy `96e7a1a`, 8 Oct 2026) and
in the PyPI sdist `rustmapper-0.1.3.tar.gz` (`sdist:path:line`, at `scratchpad/r6/sdist013/`). Data keys are
`assets/stats.json` keys.

---

## 1. What a visitor needs to learn, in order

The research agrees on the questions and on their order.

| # | The visitor's question | Source |
|---|---|---|
| Q1 | Who is this and what does he build? | R4-F1 (the six facts screened in about 7 s), R4-F4, R2-I10 (a) |
| Q2 | Which project should I open first? | R4-F5 (employers open the project with the most work, then read the code), R2-I10 (b) |
| Q3 | Is it in working order: tested, passing, alive, released? | R4-F7 (recency answers "is it alive?"), R2-I4, R4 impl. 3 |
| Q4 | How do I start it, with a command that works? | R4-F8, F9 (wrong install steps are the most common documentation failure), R6-F6 |
| Q5 | What will go wrong for me? | R2-F3 (the most frequent sentence in a pilot book is a plain judgement for strangers), R2-I10 (d), R6-F10 |
| Q6 | Why is it built this way? | R4-F8 ("why" is 2.7 % of README content and the rarest part), R4 impl. 10 |
| Q7 | What else has he made? | R4-F5 (side projects read as interest), R3 impl. 10 |

Q1 to Q5 are answered by a few short facts per project. They are the same five fields for every project, read in a
fixed order, and compared across two projects. Q6 takes sentences. Q7 is a list.

## 2. Choosing the form: every candidate, and why it wins or loses

| Form | What it would teach | Verdict, with evidence |
|---|---|---|
| Current week-islands | when commits happened | Out. It answers none of Q1–Q7 (R2: "a log drawn to look like a chart"; R3-F5; R5-F3, F4, F6; R7-F2). |
| No image at all, text only | Q1–Q7 as Markdown | Close second, rejected. GitHub's stylesheet sets `.markdown-body table {display: block; width: max-content; max-width: 100%; overflow: auto}` (N4), so a table with more than two text columns scrolls sideways at 390 px. NN/g finds about two wordy columns fit on a phone and sideways scrolling is only "somewhat acceptable" (N5). GFM has no columns and no fixed field layout. The image is the only part of the page whose layout can be designed separately for phone and desk (`<picture>` with `max-width: 767px`, `README.md:5-13`). |
| A Markdown table | Q2–Q5 compared | Rejected for the same reason: it scrolls on the phone, which the owner names as the common case (BRIEF). |
| Route diagram of one project (concept A) | how a URL moves through rustmapper | True and well sourced, but it answers "how does it work inside", which is not a first question (Q1–Q5 come first: R2-F2 order, R4-F8). Scrapy's README already draws its stages twice in Mermaid (R6-F4, F13). It belongs on the project's own page, not the profile's first screen. |
| Sectional drawing (a cross-section of the stack) | layers | Rejected. Software has no physical section (R3-F1, Brooks), so any layering would be invented. It fails R5's test 1 (relation) and test 2 (true inferences). |
| Map of a real crawl (R7-I2) | depth and failures of one site | Rejected for now. No public repository holds crawl results (R6 impl. 11), and a new crawl needs a permitted target (R7-I5). It would teach the crawler's output, not whether a visitor can use it. |
| Bar chart of lines per repository | where the most work is | Rejected. It answers part of Q2, but it is the stats-card genre hiring readers discount (R4-F15, F6), and the owner already called activity counts lazy (BRIEF). |
| Light List table (one row per repository) | identify each repository | Rejected as the main form. A Light List exists to give the "detailed description" of an aid the navigator has already found on the chart (N3, §607). A visitor isn't trying to identify a repository. They're deciding whether to try one. One thing is kept: its order. Entries are "listed from seaward" (N3, §609), in the order a stranger meets them, and the card fields follow that rule. |
| **A card per project, fixed fields, fixed order** | **Q1–Q5 for the two main projects, comparable** | **Chosen.** The pilot card exists "to provide information to the pilot on boarding the ship" and to "describe the current condition of the ship". IMO adopted it because of "the need to achieve a uniform format and content" (N1, §3.1 and preamble). Its "CHECKED IF ABOARD AND READY" box is a set of ticks for equipment that works now (N1, appendix 1). The pilots' guidance says the card supplements the spoken exchange and does not replace it (N2, A.960 §5.3). On this page the README text plays that spoken part. |

**What the image does that the text below it cannot.** (1) It puts Q1–Q5 for both projects in the first screen, where
57 % of viewing time is spent (R4-F3) and where a picture would otherwise take attention without carrying facts (R4-F2,
19 % of fixation on a photo). (2) Its fields line up across the two projects on the desk, so "which is ready, which
needs Docker" is a glance along one row (R3-F4: tables beat maps for "which" questions). (3) It has a separate layout
for 390 px, which Markdown can't provide (N4, N5). (4) Its ticks are computed at every build and turn to a cross when a
check fails, which no hand-written sentence does.

**What the image costs.** You can't copy, click or search text inside an `<img>` (R4-F13), and screen readers need the
alt text. So every command on the card is repeated once as a copyable code block below, and the alt text carries the
card's full content (section 5). That duplication is deliberate and limited to the commands.

---

## 3. The image, element by element

### 3.1 What is drawn

Desk: a top band with the title block, then a three-column table. A field-label column sits on the left with
rustmapper and Scrapy beside it. Each field is one row, so the same field sits at the same height for both projects.

```
Ben Russell              CRAWL AND DATA INFRASTRUCTURE · PYTHON AND RUST
                         TWO OF 21 PUBLIC REPOSITORIES · AS OF 9 OCT 2026
─────────────────────────────────────────────────────────────────────────────────────
              rustmapper  RUST    last commit 8 Aug 2026 │ Scrapy  PYTHON    last commit 8 Oct 2026
WHAT IT DOES  Crawls one site; writes each page it       │ Finds pages, keeps them raw in Delta Lake,
              reaches as a line of data/sitemap.jsonl.   │ then analyses and summarises them in stages.
CHECKED       ✓ CI on main passed 7 Oct 2026 · 176 tests │ ✓ CI on main passed 8 Oct 2026 · 1,920 tests
TO RUN        pip install rustmapper                     │ cd Scraping_project
              rust_sitemap crawl --start-url URL         │ python start.py
              0.1.3 from 8 Nov 2025, prebuilt for        │ No release. Needs docker and docker-compose;
              macOS arm64 + Python 3.13; else needs Rust │ dashboard at localhost:3000.
WATCH FOR   ▍ The command is rust_sitemap, not rustmapper│▍ Spiders run by name: scrapy crawl scout.
            ▍ No depth limit; subdomains are in scope.   │▍ The bundled config targets a university's
                                                         │  domain; pass -a allowed_domains=yours.
```

Phone: the same content top to bottom. Title block, then the rustmapper card, then the Scrapy card. Each field label
sits on its own line above its text.

Removed: the islands, the shallows, the month axis, the commit-day rows, "15 more", the "Fl 30s" light, the graduated
dashed border, the motion editions. Section 7 says why for each.

### 3.2 Element table

Columns: what a visitor learns; why this form is right for it; evidence; data needed and whether `build_stats`
gathers it today.

| Element | Visitor learns | Why this form | Evidence | Data, gathered? |
|---|---|---|---|---|
| **Name** "Ben Russell", serif | whose page it is | the first of the six facts screened (R4-F1); largest type is read first | R4-F1, F4 | `chart.toml [identity]`: yes |
| **Role line** "CRAWL AND DATA INFRASTRUCTURE · PYTHON AND RUST" | what he builds (Q1), in the first three words | titles and text carry what people remember (R5-F2, R4-F11); the first two words must carry the gist (R4-F3, impl. 5); the role names what the cards show, two crawl projects in Python and Rust (R5 impl. 10) | R6-F1 (his work is crawling and its data, in several languages) | `chart.toml [copy] role_line`: yes |
| **Selection line** "TWO OF 21 PUBLIC REPOSITORIES" | the cards are a choice, and there is more | a chart states its coverage. A guide gives detail where visitors go and a line elsewhere (R2-F12). Saying what was left out is honest selection (R1-I7) | R2-F12; R1-I7 | `repo_count` = 21: yes; "two" = number of cards: yes |
| **Date** "AS OF 9 OCT 2026" | how current the ticks and dates are | every Coast Pilot page carries its update date (R2-F11). The pilot card has a "Date" field at its head because it describes current condition (N1, appendix 1) | R2-F11, I9; N1 | `taken`: yes |
| **Card header**: project name (serif) + main language (caps, muted) | which project and in what language (Q2) | the name the visitor will search for. The language is one of the screen keywords (R4-F1). The package name, not the repository name, because that is what `pip` takes (`chart.toml [hero.aliases]`) | R4-F1; R6-F6 | `repos[].main_language`, `[hero.aliases]`: yes |
| **"last commit 8 Aug 2026" / "8 Oct 2026"** in the header | whether it is alive (Q3) | recency is the one activity fact that answers a visitor's question (R4-F7). A date, not a count, so there is no volume genre (R4-F6). Bulk-edit days are excluded so the date is real work | R4-F7; AUDIT.md row `last_ns` (line 75) | `repos[].last_ns`: yes |
| **WHAT IT DOES**: one sentence each | what the project is (Q1, Q2), and what you get out of it | a pilot entry opens with what the place is (R2-F2 item 1). README "what" comes first in the cognitive funnel (R4-F8). The rustmapper sentence names the output file so the visitor knows what success looks like (R2-F9, the arrival view) | rustmapper: `Rust-sitemap:README.md:131-134`, `src/state.rs:131-145`; Scrapy: `README.md:20-22`, `src/lakehouse/lakehouse_manager.py:364-368, 538-553` | text: **new** `chart.toml [card.<repo>] what` with source anchors |
| **CHECKED**: tick + "CI on main passed <date> · <n> tests" | it is in working order today (Q3), and how much is tested | the pilot card's "CHECKED IF ABOARD AND READY" is a column of ticks for what works now (N1). A tick is computed, so it is a measurement, not a claim. The test count uses the audit's wording "176 tests" | `repos[].ci` (AUDIT.md:83), `repos[].test_functions` (AUDIT.md:77, verdict line 182) | `ci.conclusion`, `ci.date`, `test_functions`: yes |
| Tick rule | a cross and "CI on main failed <date>" when the latest run is not `success`; the line is left out when `ci` is absent | a guide says how sure it is (R2-F11). A mark that can only ever be a tick is decoration | AUDIT.md:83 (`stale: true` carried) | yes |
| **TO RUN**: two commands (mono) | the shortest start that works (Q4) | the leading line: one way in, each step checkable (R1-I5). The current page prints `rustmapper crawl`, which fails because the 0.1.3 wheel installs only `rust_sitemap` | R6-F6; R4-F17, impl. 9; `sdist:Cargo.toml:8` (`name = "rust_sitemap"`), `sdist:pyproject.toml:52` (`bindings = "bin"`); Scrapy `README.md:91-96` | binary name: **new** `edition.scripts` from the wheel's `RECORD`; commands: **new** `[card.<repo>] run` |
| **TO RUN** note: release and platform (rustmapper) / requirements and where to look (Scrapy) | whether `pip` will work on my machine; that the release is older than the code; what to install first; where the result shows up | a pilot book states the stranger's condition beside the entrance ("drafts greater than 4 or 5 feet", R2-F3). The pilot card's guidance warns that particulars on the card may not match current conditions (N2), which here is release versus code | `edition.version`, `edition.date`, `edition.wheels`; `Scrapy:Scraping_project/start.py:24-29` (`REQUIRED_TOOLS`, `LOCAL_GRAFANA_URL`); no git tags in any repository (R6-F8) | edition: yes; Scrapy note: **new** `[card.Scrapy] note` with anchors |
| **WATCH FOR**: two lines each, with a short accent bar | the traps a stranger hits first (Q5), each with its fix | the most common sentence in a pilot book is a fact plus what it means for a stranger (R2-F3). A clearing line is one hazard, one rule (R1-F10). The bar is the only accent on the card, so the eye finds the traps. Text stays ink because accent text is 4.09:1 on paper and fails 4.5:1 (concept A §2.4) | rustmapper: `Rust-sitemap:README.md:25`; `src/url_utils.rs:81-91` and `bfs_crawler.rs:697`, identical scope rule in `sdist:src/url_utils.rs:81-91`, no depth flag in `sdist:src/cli.rs`. Scrapy: `README.md:228-241` (#489); `Scraping_project/config.yml:29-30`; `README.md:256` (`-a allowed_domains=`) | **new** `[card.<repo>] watch` with quote or anchor per line |
| **Column rule** between the two cards (desk), PEN rule between cards (phone) | these are two separate projects | the one structural mark. The pilot card form is ruled into boxes for the same reason (N1, appendix 1) | N1 | none |
| **Row rules** (desk, HAIR) | which line belongs to which field | rows aligned across both cards make the comparison a straight line for the eye (position on a common scale, R1-F16; R3-F4) | R1-F16; N5 (keep row labels visible) | none |
| **Field labels** in spaced caps, muted | what each line is, without a legend | self-evident labels (R4-F12). Fixed labels in a fixed order are what make the card a form and not a paragraph (N1: "uniform format and content") | N1; R4-F12 | none |
| **Hairline frame** on the paper fill | where the card ends on GitHub's white or dark page | a printed form has an edge. The old graduated border implied latitude and longitude that do not exist (R1-F12) | R1-F12 | none |

**The rule that keeps each line true.** A line about rustmapper is printed only if it is true for the code a visitor
installs with `pip` (0.1.3) **and** for the code at HEAD that the repository link opens. That is why the card prints no
worker counts, which differ five ways (R6-F7), no `--max-urls` (HEAD only) and no Python API (unreleased, R6-F6).
Concept A uses the same rule (§2.2). The check runs against `scratchpad/r6/sdist013/` in development and against the
cached sdist in the build (section 6).

### 3.3 Sizes and places

Sheet units. GitHub shows the desk sheet at ×0.68 (870 px column) and the phone sheet at ×0.54 (390 px). Type sizes come
from the existing scale (`scripts/tokens.py`: `SCALE`, `SCALE_PHONE`, `FLOORS`: desk 19 semantic, phone 26 semantic).
Fonts: serif for names, `cond` for prose, `plex` for commands, `label-caps` for field labels.

**Desk: 1280 × 600 sheet → 870 × 408 px on screen** (today's hero is 870 × 424).

- Frame: HAIR, 12 inside the sheet edge. Paper fill as today, day and night editions.
- Title band. "Ben Russell" serif 88 at x 48, baseline 108 (60 px on screen). Role line `label-caps` 19 at x 560,
  baseline 72. Selection and date line `label-caps` 19 muted at x 560, baseline 104. A PEN rule at y 140 runs from x 48
  to 1232.
- Columns: labels x 48–188, rustmapper x 208–700, Scrapy x 740–1232. A HAIR vertical rule at x 720 runs from y 160 to 576.
- Header row, baseline 196: project name serif 41, language `label-caps` 19 muted 16 after it, "last commit …" `label`
  19 muted, right-aligned to the column edge. HAIR row rule at 214.
- WHAT IT DOES: label baseline 246; text `label` 19, baselines 246 and 272 (about 57 characters a line at 492 wide).
  Rule at 290.
- CHECKED: baseline 322. Tick glyph 19 at the column's left edge, text starting 26 units to its right. Rule at 340.
- TO RUN: commands `machine` 19, baselines 372 and 398 (43 characters fit; the longest is 35). Note `label` 19 muted,
  baselines 424 and 450. Rule at 468.
- WATCH FOR: baselines 500 and 526, plus 552 for Scrapy's wrap. Accent bar 3 × 16, `accent`, 10 left of each line's
  text.
- Bottom margin to 600. Smallest text on screen is 12.9 px (19 × 0.68), the desk floor already in use.

**Phone: 720 × 1580 sheet → 390 × 856 px on screen** (today's phone hero is 390 × 610).

- Frame HAIR at 12. Text from x 40 to 680 (640 wide: about 54 `cond` characters or 41 `plex` characters at 26).
- Name serif 132, baseline 150. Role line `label-caps` 26, baselines 206 and 240. Selection line baseline 284, date
  line baseline 318, both muted.
- rustmapper card. PEN rule at 344. Header baseline 392: name serif 40, language caps 26 muted, "last commit 8 Aug
  2026" `label` 26 muted on the next line, 426. Each field has its label line (`label-caps` 26 muted) and then its text
  lines at a 34 pitch, with 42 between fields. WHAT IT DOES: 2 lines. CHECKED: 1. TO RUN: 2 mono and 2 note. WATCH FOR:
  2. The card ends near 930.
- Scrapy card. PEN rule at 960, same pattern. WHAT IT DOES: 2 lines. CHECKED: 1. TO RUN: 2 mono and 2 note. WATCH FOR:
  3. The card ends near 1550.
- Smallest text on screen is 14 px (26 × 0.54).
- First two screens (R4 impl. 6): both project names are within the image's first 540 px. Assuming GitHub's mobile
  header is about 450 px (not measured; measure on a device), the link line under the image falls near 1,320 px, inside
  two iPhone screens. The image is 246 px taller than today's, and every added line answers Q1–Q5.

---

## 4. The page around the image

| Block | Visitor learns | Why it is here, in this form | Evidence | Change |
|---|---|---|---|---|
| 1. The card image (section 3) | Q1–Q5 for both main projects | the first and largest thing he controls (R4-F4), so it carries the facts (R4-F2) | as 3.2 | replaces the hero |
| 2. Link line `rustmapper · Scrapy · PyPI · Email` | where to click, in the image's order | nothing inside an `<img>` links (R4-F13). Scent (R4 impl. 8) | `README.md:17-22` | keep |
| 3. "Ben Russell builds …", Languages, Stack | the screen keywords | recruiters scan for keywords (R4-F1). This is planning-guide material, one line each (R2-I8) | `README.md:24-26` | keep. Add "Every commit authored on US Eastern time." from `tz_offsets` (AUDIT.md verdict line 199) as the one place the time zone appears |
| 4. rustmapper paragraph: one sentence + link | which repository to open | the card carries the facts, so this carries only the name and the link | `README.md:28` | keep the sentence. **Cut** the italic facts line (`facts:Rust-sitemap`), because the card now holds it |
| 5. rustmapper code block | commands you can copy | an image can't be copied (R4-F13). The current block prints `rustmapper crawl`, which fails (R6-F6) | R4-F17, impl. 9 | **fix**: `pip install rustmapper` / `rust_sitemap crawl --start-url <your-site>` / `rust_sitemap export-sitemap --data-dir ./data --output sitemap.xml` / `# current code: cargo install --git https://github.com/BenjaminSRussell/Rust-sitemap` |
| 6. rustmapper "why" bullets (governor, WAL, frontier, seeds) | why it is built this way (Q6) | the rarest and strongest part of a README (R4-F8, impl. 10); sentences, not fields | `README.md:34-37`; R6-F2 | keep. Seed bullet unchanged; governor bullet unchanged |
| 7. Platform note bullet | — | now on the card | — | **cut** |
| 8. Scrapy paragraph + code block (`cd Scraping_project`, `python start.py`) | Scrapy's link and copyable commands | as 4 and 5 | `Scrapy:README.md:91-96` | keep the sentence, **cut** the facts line, **add** the code block |
| 9. Scrapy "why" bullets | Q6 for Scrapy | as 6 | `README.md:55-58` | **correct** "summaries from BART-large-CNN" to "large documents summarised by bart-large-cnn in stage 4; others get an extractive summary" (R6-F7, `stage3_worker.py:22`, `stage4/summarization.py:79`) |
| 10. One hand-off sentence | the projects are one body of work, and which link is built | true but not a Q1–Q5 fact, so it is text. An unbuilt link is said to be unbuilt (R6-F5) | `ideal-url-organizer:scripts/import_rust_sitemapper.py`; `Rust-sitemap:README.md:141-169`; no reader in Scrapy | **add**: "`sitemap.jsonl` feeds ideal-url-organizer (`scripts/import_rust_sitemapper.py`). A Delta export for Scrapy is written but not yet read." |
| 11. "Also": four lines | what else he built (Q7) | a lookup, so a list (R3-F4, R5-F10) | `README.md:62-67` | **correct** go_go_go: say what differs (headless Chrome, SQLite search, TLS-fingerprint impersonation) and drop "100M+", which has three values in its own repo (R6-F7, F9) |
| 12. "15 more" in `<details>` | the rest exist | hiring readers read side projects as interest (R4-F5), but they are not a first question | `README.md:69-87` | keep |
| 13. Working rules | how he thinks, each rule tied to code | profile-level "why" (Q6) | `README.md:91-97` | keep. **Rename** rule 3 "Lights before speed" to "Dashboards before speed": the theme word is a pun, and the rule's own text already says dashboards (BRIEF: nothing names the theme) |
| 14. "Found a mistake? Open an issue." | how to report an error | the correction loop a guide keeps with its readers (R2-F11) | `README.md:99` | keep |
| 15. Data line | how each figure on the card is measured | a guide says how sure it is (R2-F11). The old line describes a chart that is gone | AUDIT.md | **rewrite**: "Measured 9 Oct 2026. Ticks are the latest CI run on each default branch. Test counts are test functions at HEAD. Last commit leaves out bulk-edit days. Commands and traps are checked against rustmapper 0.1.3 on PyPI and the code at 32c2651, and Scrapy at 96e7a1a. 3 % of my commits carry an AI co-author trailer; 297 more were written by coding agents and are not counted as mine. Regenerated weekly." |
| 16. Alt text | the card's message, for screen readers and broken images | alt states the message, not the drawing (R4 impl. 12, F16) | W3C complex images (R4-[51]) | **rewrite**: "Ben Russell, crawl and data infrastructure in Python and Rust. rustmapper (Rust): crawls one site and writes each page to data/sitemap.jsonl; CI passed 7 Oct 2026, 176 tests; install with pip install rustmapper, run rust_sitemap crawl --start-url URL; watch for: the command is rust_sitemap, and there is no depth limit. Scrapy (Python): finds pages, keeps them raw in Delta Lake and analyses them in stages; CI passed 8 Oct 2026, 1,920 tests; run cd Scraping_project then python start.py, needs Docker; watch for: run spiders as scrapy crawl scout, and set allowed_domains to your own." Generated from the same `stats.cards` data so it can't drift |
| 17. License line | terms | required | — | keep |

---

## 5. Data: what each mark needs

**Already gathered by `scripts/build_stats.py`:** `[identity]`, `[copy] role_line`, `repo_count`, `taken`,
`repos[].main_language`, `repos[].ci` (flagships), `repos[].test_functions`, `repos[].last_ns`, `edition.version`,
`edition.date`, `edition.wheels`, `tz_offsets`, `coauthored_total`, `agent_authored`.

**New:**

1. `edition.scripts`: the executables in the released wheel, read from `RECORD` (`*.data/scripts/*`). Today that is
   `["rust_sitemap"]`. Fetched once per version and cached. The card's command is built from this, so a 0.1.4 that adds
   a `rustmapper` entry point changes the card by itself.
2. `chart.toml [card.<repo>]` for the two flagships: `what`, `run = [...]`, `note`, `watch = [...]`. Every line carries
   `source = "repo:path"` and `anchors = [...]` (literal strings the file must contain, for example `"bindings = \"bin\""`,
   `"name = \"scout\""`, `"allowed_domains:"`, `"REQUIRED_TOOLS"`), or a `quote` from the repository's README.
   rustmapper lines also carry `anchors_release`, checked against the 0.1.3 sdist.
3. `scripts/data/cards.py`, new and about the size of `claims.py`. It opens each source at the clone's HEAD (and the
   sdist for `anchors_release`), checks every anchor and quote, and writes `stats.cards` with a `verified` flag and the
   sha per line. Any unverified line fails `check.py --tier fast` and names the line and the missing string. The sheet
   never draws an unverified line and never drops one silently.
4. `repos[].head.sha` for the two flagships (`git rev-parse HEAD` in the clone the build already makes), for the data
   line.
5. Optional, weekly on a macOS arm64 runner: `pip install rustmapper && rust_sitemap --help`, so the TO RUN line is
   checked by running it (R1-I5, R4 impl. 9).

**No longer drawn:** `weeks`, `week_days`, `months`, `tide`, `variation`, `hours`, `claims.scrape_interval`, `sweeps`.
They stay in `stats.json` for the audit. `scripts/sheets/hero.py` is replaced by `scripts/sheets/card.py`, whose
reasons table names a visitor question (Q1–Q5) for every element.

---

## 6. Checks against the owner's goal

| His words | How this concept answers | Test a reviewer runs |
|---|---|---|
| "what is that going to help? How does it help the user see my project? What is it showing?" | It shows, for his two main projects, what each does, whether it works today, how to start it, and what goes wrong. | Show the image for 10 s to someone new. Ask: what does he build; which project would you try first and how; what is one catch? Pass if they say crawlers, name a project and its command, and name one trap (R4 impl. 1; R2-I10). |
| "tiny islands … Is it based on the size of the project or how many commits?" | Nothing on the image has a size that carries data. Every number is printed as a number, with a definition. | List every shape in the SVG. None varies in size with data (R4 impl. 2, R5 impl. 8). |
| "chasing a purpose instead of having a purpose" | The questions were written down first (section 1) and the form was picked against them, with the other forms rejected on evidence (section 2). | Every element in 3.2 names a Q1–Q5 question. An element that can't name one is cut. |
| "Everything, single thing inside of this needs a purpose" | Tables 3.2 and 4 give each element and each page block what it teaches, why the form, and a source. | A row without a file and line, a `stats.json` key or a research finding fails. |
| "If I was a sailor, if I was a pilot … very helpful information" | It is what a pilot is handed on boarding a ship they don't know: current condition, how to handle it, what is not working (N1, N2). | Remove every rule and the accent. The text still reads as instructions for a stranger, field by field (R2-I11). |
| "Don't tell the user … it should be obvious"; no theme words; no pirate talk | No word on the image names the theme. The labels are plain English (WHAT IT DOES, CHECKED, TO RUN, WATCH FOR). | Grep the image text and alt text for chart, sea, ship, harbour, survey, light, buoy, pilot, log: zero hits. |
| "The data doesn't look exactly accurate"; honest data only | Every line is checked against the code and, for rustmapper, the release. Ticks are computed. No estimates. | `cards.py` passes, and every number on the card (7 Oct, 176, 8 Aug, 0.1.3, 8 Nov 2025, 3.13, 8 Oct, 1,920, 21, 9 Oct) maps to a key in 3.2. |
| "I'm looking at iPhone" | A separate phone layout with 14 px minimum text. Both projects are named in the first screen. | At 390 px nothing is under 13 px on screen. Check in Safari and the GitHub iOS app, in light mode too (R4 impl. 7). |

---

## 7. What is left out, and why

- **Islands, shallows, month axis, commit-day rows**: they encode the calendar, which no visitor question needs (R1-I2,
  R3 impl. 1, R5 impl. 1, R2-I1, R7-I1).
- **"15 more" row**: a lookup, already in `<details>` (R3 impl. 10).
- **"Fl 30s"**: a code only a sailor reads, one of three configured intervals, nothing a visitor acts on (R1-I6, R5-F13).
- **"0.1.3 · PyPI" mark**: the fact stays and moves to TO RUN, where it answers Q4 (R5-F13, R6 impl. 8).
- **Graduated dashed border**: graduations mean degrees that don't exist (R1-F12). It becomes a hairline frame.
- **"DATUM: MAIN"**: true, but no visitor question needs it in the image. It moves to the data line ("each default
  branch").
- **"EASTERN TIME"**: a planning fact (R2-I8) that moves to the text (block 3), measured from `tz_offsets`.
- **Motion and still editions**: nothing on the card changes over time, so there are two editions (day, night) at each
  width, not four.
- **Internal stages, worker counts, Bloom sizes, throughput**: either they differ between versions (R6-F7), or they are
  unmeasured (R6-F8), or they answer Q6, which belongs in the bullets.

---

## 8. Sources added this round

The shared web-search budget was used up before this memo's first search. These sources were fetched directly by URL
and their text was extracted and read. PDFs were converted with `pdftotext` into `scratchpad/r6c/`.

- **N1.** IMO, Resolution A.601(15), *Provision and Display of Manoeuvring Information on Board Ships*, adopted 19 Nov
  1987, §3.1–3.3 and appendix 1 (pilot card form: "Date", particulars, engine, steering, "CHECKED IF ABOARD AND READY",
  "OTHER INFORMATION"). https://wwwcdn.imo.org/localresources/en/KnowledgeCentre/IndexofIMOResolutions/AssemblyDocuments/A.601(15).pdf (read)
- **N2.** IMPA, *Guidance on the Master-Pilot Exchange (MPX)*, reproducing IMO A.960(23) §5.3–5.4: the card should
  "supplement and assist, not substitute for, the verbal information exchange". Card data rests on "new vessel"
  conditions and "may not be accurate" in local conditions.
  https://www.impahq.org/sites/default/files/2021-04/IMPA%20Guidance%20on%20the%20Master%20-%20Pilot%20Exchange%20%28MPX%29.pdf (read)
- **N3.** NGA, *The American Practical Navigator* (Bowditch), 2017, ch. 6, §604 (Sailing Directions), §607 (light lists
  "supplementing the charts … consult the light lists to determine their detailed description"), §609 ("lists seacoast
  aids first, followed by entrance and harbor aids listed from seaward"). Same URL as R2-[4]. (read)
- **N4.** sindresorhus, `github-markdown-css` (GitHub's Markdown stylesheet), `.markdown-body table { display: block;
  width: max-content; max-width: 100%; overflow: auto }`.
  https://raw.githubusercontent.com/sindresorhus/github-markdown-css/main/github-markdown.css (read)
- **N5.** A. Schade, "Mobile Tables: Comparisons and Other Data Tables". Nielsen Norman Group, 17 Sep 2017. About two
  wordy columns fit a phone. Sideways scrolling is "somewhat acceptable" only if signalled. Keep row labels visible.
  https://www.nngroup.com/articles/mobile-tables/ (read)
- **N6.** "List of lights". Wikipedia, read 9 Oct 2026 (secondary; confirms the light list's purpose as a reference
  that describes aids). https://en.wikipedia.org/wiki/List_of_lights

With R1–R7 (44 + 44 + 62 + 57 + 52 + 54 + 47 sources), the research behind this concept lists about 360 citations
(many repeated across files), plus the six above.

---

## 9. Risks

1. **The owner may find it too plain.** He asked for "a cool format" with a shipping layer. This concept puts the whole
   theme into the manner of a printed form: ruled boxes, spaced caps, ticks, a date at the head. If that reads as a
   spreadsheet, the fix is better typography and rules. More symbols would bring back the problem he named.
2. **It can look like a stats card.** The profile-kit cards that hiring readers discount are activity counts (R4-F15).
   This card has no activity count. The test count and dates answer "does it work, is it alive". A reviewer should
   still check that it doesn't read as a badge wall.
3. **Text in an image.** It can't be copied or searched. Commands are repeated as code blocks, and the alt text carries
   everything (blocks 5, 8, 16).
4. **Phone height.** 856 px against today's 610. The GitHub mobile header height is estimated, not measured.
5. **Editorial choice of traps.** Which two traps each card shows is a judgement. The limit is that every one is
   quoted from the project's own README or anchored in its code, and checked at every build.
6. **Release drift.** Each new commit to Rust-sitemap widens the gap with 0.1.3, and the "true in both" rule removes
   lines over time. Releasing 0.1.4 with a `rustmapper` entry point fixes this and the command-name trap together
   (R4 impl. 9).
7. **A third party in the defaults.** Scrapy's bundled config targets a university's domain. The card warns without
   naming it. The repository names it.
8. **Overlap with concept A.** A spends the image on rustmapper's internals. C spends it on the stranger's first five
   questions for both projects. A's route drawing could sit inside the Rust-sitemap repository's own README, where "how
   does it work inside" is the visitor's question.
9. **The GitHub mobile app may always serve the day edition** (R4-F13, anecdotal). The day edition must stand on its
   own.
