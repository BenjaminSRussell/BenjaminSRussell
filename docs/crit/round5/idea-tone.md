# Round 5 — tone: a page that acts like it does not know it is themed

Copy editor and comedy writer, 35. House styles I have edited are dry on purpose: the Economist caption that
under-describes the photo, the Field Notes back cover that lists paper stock and staple gauge and nothing else, the
Wes Anderson prop whose label says only what a real label would say. The joke in all three is the same joke: the
format is grave, the subject is small, and the object never once looks at the camera.

v10 looks at the camera in every section. The rule it breaks is simple, so I will state it once and then apply it
line by line:

**A nautical word is allowed when it is the plain word for the thing. It is banned when it renames a thing that
already has a name.** "Log", "chart", "edition", "correction", "datum", "survey", "sweep" survive if you delete the
theme, because software and publishing use them too. "Harbor", "survey vessel", "other waters", "below the
waterline", "notices to mariners", "wrong depth", "I." after an island survive only inside the costume. One costume
word is a one-off; one per section is a bit being milked; one per bullet is a sketch that will not end.

Second rule: **the picture does the theme; the words do Ben.** If the drawing is a chart, every caption can be
flat and literal and the whole thing still reads as a chart. The moment a caption helps the drawing be a chart, the
drawing looks like it needed help.

## 1. What a visitor needs to know about Ben

1. What he builds, in one plain sentence. Crawl and data infrastructure, Python and Rust. **Answered** (the role
   line), but on the sheet it sits under "THE OPEN WEB · FROM SURVEYS", so the first legible sentence is boilerplate.
2. The two things to look at. rustmapper (pip-installable, on PyPI) and the Scrapy platform. **Answered**, but both
   are introduced in costume ("is the survey vessel", "is where a run is operated"), so a recruiter reads the joke
   before the noun.
3. How he thinks: the throttle watches the database, raw before clean, dashboards in version one. **Answered**, but
   split between bullets and "Notices to mariners", where the heading makes them sound like a bit.
4. Whether he is working now and on what. **Not answered** in plain words anywhere. The data says: last commits 7
   Oct 2026 across 18 repositories; Data_science_dev carried the biggest week of the year (w/c 5 Oct). The sheet
   prints this as "HW · SWEEP 7 OCT 358", which is unreadable at 390 px and unexplained at 870.
5. How to try it in thirty seconds. **Answered**: the pip block. Best thing on the page; leave it alone.
6. What he does when nobody is paying him: a voxel engine in C, Swift widgets, a prize wheel. **Answered**, hidden
   behind "Below the waterline", which is the wrong title for a list of things he did for fun.
7. When he works. Modal hour 14:00, mostly weekdays. **Half answered**: "VAR 14h" is a private joke.
8. How to reach him. **Answered**: Email.

## 2. What a real reference object in my field carries

A back cover, a colophon, a caption, a plate label. They carry: specs in units (paper, ink, dimensions); provenance
(printed where, when, from what); an edition and a correction history; one line of practical use; and at most one
dry line, placed where boilerplate would be. Nothing on them names its own genre. That is the entire craft.

Honest mappings onto his facts:

- **Edition and date** = the PyPI release (0.1.3, 8 Nov 2025). "Edition" is a chart word and a publishing word.
  Honest; keep.
- **Small corrections 2026 — 5–173** = the numbered commits to this README this year. This is the real chart
  convention used for its real purpose, and it is true (169 corrections to the page in one year is a fact about
  Ben). Honest and the best detail on the sheet. Keep, make it legible, do not caption it.
- **Datum: main** = measured from the main branch. The plain word in both trades. Honest; keep.
- **Limit of survey** = the data stops at the run date. Honest. The label on the line is enough; the hatching
  labelled "UNSURVEYED" is the shoe telling you it is a shoe.
- **Redrawn weekly** = the correction cycle. Honest, and it is already in plain English. Keep.
- **The pencil note** = a surveyor's margin grumble that is also literally true of crawling. Honest. Keep, once.
- **Hours rose** = modal commit hour as the rose. Honest if the caption is literal ("MOST COMMITS 14:00").
  "VAR 14h" is a pun that only a navigator gets, and he would then ask what 14 hours of variation means.

Forced:

- **Light characters** ('R "2" Fl R 4s'). A light's character identifies a mark at night. There is nothing here it
  identifies. Set dressing.
- **IALA Region B.** Cites a buoyage standard the chart does not use. Set dressing.
- **"I." after every island, "Bank", "Shoal" after every water name.** The first is a joke; nine is a glossary.
- **"Notices to mariners" = principles.** Real notices are corrections to the chart; the data already has those
  (the README commits). Using the heading for his engineering rules is renaming.
- **Harbour = Scrapy.** chart.toml lists "Scrapy Harbor" as an alias of a repo called Scrapy. If that is his own
  name for the project, keep it; if it was coined for the chart, it is a costume on the biggest word on the sheet.
  Ben decides; I would print the repo name.

## 3. The proposal

I am the words person; the cartographer owns the geometry. My proposal is a lettering pass on the archipelago as
drawn, and a page under it that reads like a colophon.

**The image, desk (870 px).** Same islands, same harbour, same rocks. Lettering reduced to: name; thesis; role
line; one provenance line ("FROM 21 REPOSITORIES · SEP 2025 – OCT 2026"); one unit line ("FIGURES ARE DAYS WITH
COMMITS · DATUM: MAIN"); one edition line ("rustmapper 0.1.3 · PyPI · NOV 2025"); one count line ("21 REPOSITORIES
· 9 NAMED · 12 UNDER SEVEN DAYS"). Each feature labelled with its repository name, as typed on GitHub, caps on land,
italic on water, with the first-commit month in brackets under the two main ones only. Figures inside the features
stay. The hours rose stays with the caption "MOST COMMITS 14:00 (2026)". The pencil note stays. The limit-of-survey
line stays, rotated; the "UNSURVEYED" label goes. No lights, no boat, no course line. Bottom margin: "SMALL
CORRECTIONS 2026 — 5–173" left, "GITHUB.COM/BENJAMINSRUSSELL · 7 OCT 2026 · REDRAWN WEEKLY" right, exactly as now.

**The image, phone (390 px).** Name, thesis, role line, the count line. Features labelled with the repo name only
for the five largest; the rest carry only their figure. Rose and pencil note drop. Limit line stays without its
label. Nothing moves at either width: a page that does not know it is themed does not animate its boat.

**The page under it**, in order, about 700 words total:
1. Role line and the four links (as now).
2. Three bold lines: builds / languages / stack (as now).
3. **rustmapper** — lead sentence in plain words, five bullets as now, the pip block.
4. **Scrapy** (or Scrapy Harbor if that is its name) — lead sentence plain, four bullets with the two costume
   clauses cut.
5. **Also** — four one-line entries (as now, retitled).
6. A collapsed list titled **15 more** — contents as now.
7. **Working rules** — the four numbered lines, cites in italic, as now.
8. Survey line, one sentence, and the license line.

## 4. Details and one-off words

**Five that land** (each once, uncaptioned, set as the real thing would be set):

1. *sitemap.xml lies again* — pencil, lower case, no notice number, tucked by the limit line. A field note that is
   also the thesis of his whole trade. The best line on the sheet; it must be the only pencil line.
2. *SMALL CORRECTIONS 2026 — 5–173* in the bottom margin, as a real chart prints it, meaning exactly what it means
   here: this page was corrected 169 times this year. Nobody explains it; the curious can count.
3. *DATUM: MAIN*. Two trades, one word, zero wink.
4. The hours rose with 00 / 06 / 12 / 18 at the cardinal points and the caption *MOST COMMITS 14:00 (2026)*. The
   joke is in the drawing; the caption is a fact.
5. *Edition 0.1.3, 8 Nov 2025, provisional.* "Provisional" is how a chart describes an unverified sounding and how
   an engineer describes an 0.x release. Nobody has to be told.

**Five that would be cringe** (the line the builders must not cross):

1. **"is the survey vessel" / "is where a run is operated."** Renaming the two nouns a visitor came for. Also
   both are the kind of sentence someone reads aloud in a bad voice.
2. **Section heads in costume:** "Other waters", "Below the waterline", "Notices to mariners", and the sign-off
   "Found a wrong depth?" A reader who skims to the issues link lands on the bit with no setup.
3. **The island suffix on everything:** "Wheel I.", "Data-visualizer I.", "Game Engine I.", "FashionDB Bank",
   "Profile Shoal". Nine gags, one premise. Islands look like islands.
4. **Bits leaking into the technical bullets:** "each its own mark in the channel", "nothing leaves the harbor for
   an API". Technical sentences are where the straight man lives. Once the bullets wink, nothing on the page is
   trustworthy.
5. **The chart proving it is a chart:** the anchored sailboat, the two lights with Fl 4s characters, "IALA REGION
   B", the course line, "UNSURVEYED" on the hatching. This is the shoe telling you it is a shoe.

## 5. Kill list

Image:
- Boat, anchor, course line, both lights and their characters: "You don't need to show me a boat per se."
- "UNSURVEYED": the hatching says it. "You don't need to tell me it's a shoe."
- "IALA REGION B": a standard with nothing to apply it to. "It's not smart."
- "SOUNDINGS IN COMMIT-DAYS" printed twice (top margin and data block): dense where it should be open.
- "HW · SWEEP 7 OCT / 358": unreadable on an iPhone, unexplained on a desk. "What the fuck is it trying to say?"
- "VAR 14h": a pun; replace with the fact.
- Every "I.", "Bank", "Shoal" suffix: "Making it all about it is too much."
- "9 CHARTED · 12 AS ROCKS": the rocks are drawn; say what the twelve are (under seven commit-days).

Text:
- "is the survey vessel", "is where a run is operated", "Other waters", "Below the waterline", "Notices to
  mariners", "Found a wrong depth?", "mark in the channel", "leaves the harbor": all telling. "It should act like
  it doesn't know that it is."
- The survey log's three commit totals (1,665 / 1,966 / 1,828): "The data doesn't look exactly accurate." Print
  none until the audit picks one; "We don't need to show the commits."
- The alt text's boat ("A boat sails in and anchors"): same shoe, read aloud.

## 6. The two-second test

**Two seconds, iPhone:** a name in a big serif, an old-looking chart, the words "crawl and data infrastructure ·
Python and Rust". That is the right two seconds. Today the two seconds also include "THE OPEN WEB · FROM SURVEYS",
which is noise, and a red boat, which is the tell.

**Thirty seconds:** the big island is Scrapy, started Sep 2025; the next is rustmapper, Oct 2025, on PyPI; the
figures are days he actually committed; he mostly works at two in the afternoon; the page has been corrected 169
times this year, which tells you something about him that no bullet could. Then the first bullet: a throttle that
watches the database, not the network. If the reader says "huh, why is his README a chart?" and then keeps reading
the bullets, the theme has done its job and nobody mentioned it.

---

## Appendix: line by line, v10 README and chart lettering

Format: **keep** / **cut** / **rewrite →** new text. Where a line is both chart and README (chart.toml [copy]), I
list it once.

### Chart lettering (hero, desk)

| Line | Verdict |
|---|---|
| SOUNDINGS IN COMMIT-DAYS (top margin) | **cut**; one unit line is enough and it belongs in the data block |
| 21 (top right folio) | **keep** |
| Ben Russell | **keep** |
| I survey a web that is wrong about itself. | **keep**; "survey" is the plain verb for a crawler and the one place the theme and the trade share a word |
| THE OPEN WEB · FROM SURVEYS 2025–2026 | **rewrite →** FROM 21 REPOSITORIES · SEP 2025 – OCT 2026 |
| CRAWL AND DATA INFRASTRUCTURE · PYTHON AND RUST | **keep**; move it to directly under the thesis |
| SOUNDINGS IN COMMIT-DAYS · DATUM: MAIN | **rewrite →** FIGURES ARE DAYS WITH COMMITS · DATUM: MAIN |
| CHART NO. 21 · EDITION 0.1.3 · NOV 2025 · IALA REGION B | **rewrite →** rustmapper 0.1.3 · PyPI · NOV 2025 |
| 21 REPOSITORIES · 9 CHARTED · 12 AS ROCKS | **rewrite →** 21 REPOSITORIES · 9 NAMED · 12 UNDER SEVEN DAYS |
| 00 / 06 / 12 / 18 on the rose | **keep** |
| VAR 14h (2026) | **rewrite →** MOST COMMITS 14:00 (2026) |
| sitemap.xml lies again | **keep**, pencil, once |
| Data Science Bank / 11 | **rewrite →** Data_science_dev / 11 |
| GAME ENGINE I. / 8 | **rewrite →** GAME_ENGINE / 8 |
| HW · SWEEP 7 OCT / 358 | **cut** from the sheet; if the figure survives the audit it goes in the survey line as "biggest week: w/c 5 Oct 2026, 358 commits" |
| R "2" Fl R 4s · G "1" Fl G 4s | **cut** |
| SCRAPY HARBOR (SEP 2025) / 26 | **keep** the date and figure; name per Ben: SCRAPY or SCRAPY HARBOR, whichever the repo calls itself |
| Profile Shoal / 9 | **rewrite →** this README / 9 (italic; it is the one honest in-joke, the chart charting itself, and it needs no suffix) |
| URL ORGANIZER I. / 7 | **rewrite →** IDEAL-URL-ORGANIZER / 7 |
| FashionDB Bank / 7 | **rewrite →** FashionDB / 7 |
| WHEEL I. / 8 | **rewrite →** WHEEL / 8 |
| DATA-VISUALIZER I. / 8 | **rewrite →** DATA-VISUALIZER / 8 |
| rustmapper (OCT 2025) / 22 | **keep** |
| LIMIT OF SURVEY 2026 | **keep** |
| UNSURVEYED | **cut** |
| CHART NO. 21 · SHEET 1 · SMALL CORRECTIONS 2026 — 5–173 | **rewrite →** SHEET 1 · SMALL CORRECTIONS 2026 — 5–173 (one chart number per sheet is enough; it is already the folio) |
| GITHUB.COM/BENJAMINSRUSSELL · 7 OCT 2026 · REDRAWN WEEKLY | **keep** |
| the boat and the course line | **cut** |

### chart.toml [copy] strings not printed on the hero

| String | Verdict |
|---|---|
| unit_hero = SOUNDINGS IN COMMITS | **cut** with its sheet |
| unit_approaches = SOUNDINGS IN URLS · THOUSANDS | **cut** with its sheet |
| footer_line = The chart ends here. The web doesn't. | **cut**; it is the rejected concept's caption and it is the chart explaining itself |
| log_footnote = Heights observed, not predicted. | **keep** if the line it footnotes survives; it is flat and true |
| alt.hero "...A boat sails in and anchors." | **rewrite →** Chart of Ben Russell's 21 repositories as islands; figures are days with commits; Scrapy and rustmapper largest. |
| alt_poem (six lines) | **cut**; alt text is for screen readers, not for a poem |
| notices[5] "The surface is part of the system." | **keep** the title and body; cite **rewrite →** This page, Nov 2025. |

### README, top to bottom

| Line | Verdict |
|---|---|
| alt="Chart of Ben Russell's 21 repositories ... A boat sails in and anchors." | **rewrite** as above |
| Crawl and data infrastructure · Python and Rust | **keep** |
| rustmapper · Scrapy Harbor · PyPI · Email | **keep** |
| **Ben Russell builds** crawl and data infrastructure: web crawlers, discovery pipelines, raw-first storage, the dashboards that watch them. | **keep** |
| **Languages** Python, Rust; Swift, C, TypeScript, Go. | **keep** |
| **Stack** Delta Lake, PostgreSQL, Redis, Parquet · Docker, Kubernetes, Prometheus, Grafana, GitHub Actions · tokio, redb, maturin. | **keep** |
| **rustmapper is the survey vessel:** a concurrent sitemap crawler written in Rust and shipped to PyPI as a Python package. | **rewrite →** **rustmapper** is a concurrent sitemap crawler written in Rust and shipped to PyPI as a Python package. |
| Edition 0.1.3, 8 Nov 2025, provisional. | **keep** |
| The throttle watches the database, not the network: ... | **keep**; best bullet on the page |
| Every frontier event is written to a CRC32-framed write-ahead log ... | **keep** |
| The frontier is rendezvous-hashed by registrable domain ... | **keep** |
| Seeds from sitemaps, Certificate Transparency logs and the Common Crawl index: ... | **keep** |
| Rust CLI and a Python package built with maturin. ... | **keep** |
| pip block | **keep** |
| **Scrapy Harbor is where a run is operated:** a multi-stage crawl platform built on the Scrapy framework. | **rewrite →** **Scrapy Harbor** is a multi-stage crawl platform built on the Scrapy framework. |
| A scout spider goes first; analysis and summarization workers follow, each its own mark in the channel. | **rewrite →** A scout spider goes first; analysis and summarization workers follow. |
| Raw pages land in Delta Lake and stay raw: ... | **keep** |
| Duplicates caught by URL hash and MinHash; summaries from BART-large-CNN on the worker itself, so nothing leaves the harbor for an API. | **rewrite →** ... on the worker itself, so nothing goes out to an API. |
| Prometheus metrics on Grafana dashboards. Circuit breakers ... | **keep** |
| **Other waters** | **rewrite →** **Also** |
| ideal-url-organizer — 25+ ways to sort a pile of URLs ... Home of the "no regex" rule. | **keep** |
| go_go_go — the Go sibling of rustmapper ... | **keep** |
| rust_llm_logger — ... so logging costs the caller nothing. | **keep** |
| Ai_code_detector — probabilistic forensics ... | **keep** |
| **Below the waterline** · 15 more repositories: Swift widgets, a C game engine, games, tooling | **rewrite →** **15 more** · Swift widgets, a C game engine, games, tooling |
| the eleven collapsed entries and the "Also:" line | **keep** all; "The kind of thing you build to learn why engines are hard" is the right register for the whole page |
| **Notices to mariners** | **rewrite →** **Working rules** |
| 1. Boring under load. ... | **keep** |
| 2. Keep the log. Raw before clean. ... | **keep**; "log" is the plain word here |
| 3. Lights before speed. ... | **keep**; it is a one-off and it is the plain idiom for observability-first |
| 4. Parse, don't pattern-match. | **keep** |
| Found a wrong depth? Open an issue. | **rewrite →** Wrong figure? Open an issue. |
| **Survey log** · taken 7 Oct 2026, 19:47 UTC · 21 public repositories cloned, author's commits only · 1,665 commits · 1,966 all hands · 1,828 by GitHub's calendar · instruments: clones live, GraphQL cached, REST partial, PyPI live, releases live · surveyed on 1 of the last 150 days · rustmapper 0.1.3, 8 Nov 2025. | **rewrite →** **Survey** · taken 7 Oct 2026, 19:47 UTC · 21 public repositories cloned, author's commits only · rustmapper 0.1.3, 8 Nov 2025. (Commit totals wait for the audit; "all hands" and the instrument roll-call are diagnostics, not copy.) |
| Redrawn from my repositories by scripts/build_assets.py · how it's drawn → DESIGN.md | **keep** |
| **License** Code MIT; sheets and copy CC BY 4.0; ... the sheets redraw from your repositories. | **keep** |

Count after the pass: nautical words left on the whole page that are not the plain word for the thing: zero, or
one if Ben keeps "Harbor" as the project's name. That is the number.
