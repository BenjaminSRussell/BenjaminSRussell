# Review round 8, reviewer 1: Ben, the owner

10 Oct 2026. What I looked at: every PNG in `scratchpad/r6/build/round-07/`. That is the desk sheet at 870 (day and
night), the phone sheet at 390 and 308 (day and night), the desk page (two screens), the phone page at 390 (six
screens) and at 360. I read `README.md`, `SPEC.md`, `LOG.md` (round 7's fixes) and the reviews from rounds 1 to 7, and
I don't repeat anything already fixed. Every figure was checked against `assets/stats.json`, the 0.1.3 sdist
(`scratchpad/r6/sdist013`) and the clones.

Verdict: **not yet. 8 / 10.** All of round 7's fixes landed. W1 says "in batches", the hand-off counts what actually
runs, the Languages line comes from the data, rule 1 cites the breaker that runs, the code blocks fit 360 px, and
"his Scrapy" is no longer confused with the framework. The image does the job I asked for. It shows how my crawler
runs, in order, where it bites, how you stop it, what file you get, and which of my other projects reads that file.
Nothing has a size, nothing names a theme, and it fits one phone screen.

Here's what still stops me shipping it. The page now contradicts itself on a number, and that's exactly my complaint
that "the data doesn't look exactly accurate". On the phone the image's top still runs two headings together. And two
lines on the page either teach nothing or teach the wrong thing about me.

## The first question: does it meet my goal?

- **Deep purpose for the map.** Yes. It's the route a URL takes through rustmapper, and the loop bracket and the gap
  in the track show something a list can't: those rows repeat until you stop it. Strip out the colour and it still
  reads as directions.
- **True about my projects.** The image is, line by line (table below). The page isn't, in one place: the image says
  "sorted **21** ways by ideal-url-organizer", and two screens down the Also line says "**25** ways to sort a pile of
  URLs". Each one is right on its own. `self.methods` in `src/main.py` has 21 keys, the importer's `--all` runs those,
  and there are 25 `method_*.py` files, of which 22 to 25 need the page content. Nobody reading the page knows that.
  They see two numbers for the same thing. Numerals are what the eye stops on, even inside text people skip [S1]. And
  "avoid errors of all types, no matter how small" is a credibility rule because readers treat small errors as a sign
  about the whole site [S2].
- **Nothing chases a reason.** In the image, yes. On the page, working rule 3 does. "**Dashboards before speed.**
  Dashboards go in version one." The body says the title again, and nothing in the history backs "before speed": the
  "performance" redesign commit (`52dcbd8`, 4 Oct 2025) came *before* the first Grafana dashboard (`e8cbe15`, 6 Oct).
  A principle needs a rationale and an answer to "how does this affect me?" [S3]. This one has neither, and the real
  fact underneath is better than the slogan.
- **Nothing announces the theme.** Yes. T-WORDS holds, and nothing on the page winks.
- **Teaches the right thing about me.** One line works against me. The go_go_go entry advertises "browser
  TLS-fingerprint impersonation". In that repository's own README the feature is there "to bypass JA3 fingerprint
  detection", built on uTLS, a library for "parroting" browsers' ClientHello [S4]. Cloudflare's published norms for
  well-behaved crawlers say: no "stealth tactics to try and dodge detection", respect robots.txt, stay within rate
  limits [S5]. The same page already tells a stranger, correctly, that rustmapper 0.1.3 sends 20 requests at a time
  with no pause and ignores `Crawl-delay`. That warning has to stay, because I'm handing them the install command. Put
  the two together and a site operator, or a data-infrastructure lead hiring, reads a pattern: crawlers built to get
  past the people running the sites. My Scrapy project is the opposite. It obeys robots.txt and runs AutoThrottle by
  default (`src/settings.py:121, :179`), the way Scrapy's own template does [S6]. Leaving a feature out of a one-line
  summary isn't dishonest. Leading with the evasion is a choice, and it's the wrong one.
- **Reads on a phone.** Mostly. One fault: "PYTHON AND RUST" then "rustmapper" sit about one line apart (50 units, the
  role line's own pitch is 34), so the project name reads as a third line of my role, not as the heading of the
  drawing. Round 7's reviewer noted it and didn't rank it, and it wasn't touched. A heading needs more space above it
  than the lines around it, or it doesn't read as a heading [S7].

## Figures checked

| Printed | Source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.date` (all four uploads 8 Nov 2025) | 0.1.3, 2025-11-08 | yes |
| by default, sitemaps, certificate logs, Common Crawl | sdist `cli.rs:58` `default_value = "all"`; `routes` S1 verified both | | yes |
| fewer at once when saves average over 500 ms | sdist `main.rs:90` `THROTTLE_THRESHOLD_MS: f64 = 500.0`, `:113` EWMA compare | 500 | yes |
| logged to disk, then saved to redb, in batches | `routes` W1 fallback wording (`drain_batch` anchors) | | yes |
| never exits by itself; `Received work item` | sdist `bfs_crawler.rs:433`; runcheck `ends_by_itself` false at 150 s | | yes |
| press Ctrl-C once to write `data/sitemap.jsonl` | runcheck `crawl_ctrl_c` ok, 3 lines | | yes |
| fields url, depth, status_code, title | `handoffs[0].writer_fields_release` | | yes |
| sorted 21 ways by ideal-url-organizer | `figures[]` `self.methods` = 21 (ast, re-counted in the clone at `159968a`) | 21 | yes, but see Also |
| Also: 25 ways to sort | `figures[]` glob `method_*.py` = 25 | 25 | true, **contradicts the image** (must-fix 1) |
| 176 tests · CI 7 Oct 2026 · 16k lines of Rust · `32c2651` | `repos[Rust-sitemap]` | 176; success; 16,390 | yes |
| 1,920 tests (CI selects all but 41) · CI 8 Oct · MIT · 69k · `96e7a1a` | `repos[Scrapy]`, `ci_selection.not_selected` 41 | | yes |
| 3 min from a cold cache, 4-core Linux | runcheck install median 171.4 s, 4 CPUs | | yes |
| 20 at a time to one host, 256 in all | sdist `state.rs:285` `max_inflight: 20`; `cli.rs:98` `"256"` | | yes |
| Languages Python, Rust; Swift, JavaScript, TypeScript, C, Go | `main_language` over 21 repos: Python 10, Swift 3, JS 2, TS 2, Rust 2, C 1, Go 1 | | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | `repos[].commits`, `others`, `coauthored.agent` | 101+45; 420+49+22+8 | yes |
| 15 more | 22 − profile − 2 − 4 | 15 | yes |
| Rule 1 Oct 2026; rule 2 Oct 2025; rule 3 Oct 2025; rule 4 Nov 2025 | `rules[]` `099dd6c`, `52dcbd8`, `d571e6e`/`e8cbe15`, `2be623e`, all his | | yes |
| Scrapy block: `scraper` service, `scout`, `-a` args, `localhost:3000` | `docker-compose.yml:8, :249`; `scout_spider.py:47`; `base_spider.py:52` splits `-a` lists | | yes |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page | keep | read first |
| Role line, two caps lines | crawl and data infrastructure, Python and Rust | keep | the drawing under it proves both |
| Empty left column under the role (desk) | nothing | keep | the room is what makes the route read first |
| "rustmapper" + header sentence | which project, what it writes | change (phone) | the words are right; the gap above it is too small on the phone (must-fix 2) |
| Start bar | where you begin | keep | |
| `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | the date sits on the command it dates |
| Magenta track | one way through, top to bottom | keep | |
| Stop rings | one step the tool takes | keep | |
| S1 seeds | URLs come from more than links, by default | keep | worth knowing before you point it at your own site |
| F1 fetch, throttle and scope | the crawl loop, its back-pressure, its reach | keep | one clause each now; reads right on the phone |
| W1 write path | it persists as it goes | keep | the data-infrastructure signal; it is why export works after a kill |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Gap in the track under the loop | the loop has no exit but Ctrl-C | keep | |
| H1, red dotted box | the catch in 0.1.3 and how to tell you're done | keep the mark | true. The cause is mine to fix in Rust-sitemap (not re-ranked) |
| C1 Ctrl-C | the one thing you do | keep | |
| End bar + `data/sitemap.jsonl` + fields | what you get, in the struct's words | keep | |
| Hand-off line, arrow, "sorted 21 ways by ideal-url-organizer" | my projects feed each other | keep | right number; the page below must agree (must-fix 1) |
| Night editions | the same | keep | contrast holds |
| Phone editions (600 wide, shown at 308) | the same, one screen | change | the heading gap (must-fix 2) |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image + alt text | above | change | must-fix 2 |
| Link line | where to go | keep | |
| "Ben Russell builds …" | what I build | keep | |
| Languages | what I write in | keep | from the data now |
| Stack | what I build on | keep | |
| Pick sentence | which tool for which job | keep | |
| rustmapper sentence | the Python API isn't released | keep | |
| rustmapper facts line | alive, tested, size, which commit | keep | |
| rustmapper code block | how to run, stop and recover | keep | fits 360 px |
| Wheel note, load note, 50,000 note | when pip just works; what it does to a server; the sitemap limit | keep | a stranger about to run it needs all three |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy lead sentence + code block | how to start it | keep | verified against the clone |
| Grafana note + bullets | what Scrapy does that rustmapper doesn't | keep | |
| Also: ideal-url-organizer | the URL sorter | change | 25 against the image's 21 (must-fix 1) |
| Also: go_go_go | the Go counterpart | change | leads with browser impersonation (must-fix 3) |
| Also: rust_llm_logger | a mechanism | keep | |
| Also: Ai_code_detector | what it detects | change | the repository's tagline, not what it does (must-fix 6) |
| 15 more | the rest | keep | |
| Working rule 1 | how I work, with proof | keep | |
| Working rule 2 | as above | change | its cite breaks the "repo, month: what" form the other three use (must-fix 5) |
| Working rule 3 | as above | change | body says the title again; "before speed" isn't backed (must-fix 4) |
| Working rule 4 | as above | keep | |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn, agent authorship | keep | |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **One count for ideal-url-organizer across the page** (`chart.toml`, the Also entry for ideal-url-organizer near
   :181, and one `[[figures]]` row; `render_readme.py` reads both rows; about 10 lines and two tests).
   - Also line: "**ideal-url-organizer** — 25 ways to sort a pile of URLs: 21 from the URLs alone (domain, crawl
     depth, subdomain, …), 4 more from the page content." The 21 is the existing `self.methods` row, the same one the
     image reads. The 4 is the glob row minus the keys row. A new `[[figures]]` row backs "page content": each of
     `method_22` to `method_25` contains `PageContent` (true at `159968a`: `method_22_by_http_status.py`,
     `_23_by_schema_org_type.py`, `_24_by_page_authority.py`, `_25_by_semantic_similarity.py`).
   - The image stays "sorted 21 ways by ideal-url-organizer".
   - New STRINGS-COUNT check (fast tier): for each repository, any "<n> ways" in the hero's text manifest must also
     appear in that repository's README line. Test: a fixture where the hero says 21 and the README only 25 fails.
   - Why: two numerals for one thing, two screens apart, is the "doesn't look exactly accurate" I've been complaining
     about since round 4. Numerals are what readers look at [S1], and small errors cost the whole page [S2].

2. **The phone sheet separates my role from the project heading** (`scripts/sheets/route.py`, the phone gap from T2's
   last baseline to R0's baseline; one constant and a test).
   - Phone gap 50 → 70 units (+20). The phone sheet goes from 1,135 to 1,155, under the 1,246 gate. Desk is
     unchanged, because the role and the route are separate columns there.
   - Test (render tier): on every phone edition, the gap from the last role-line baseline to the project name's
     baseline is at least 2 × the role line's own pitch (34 → ≥ 68).
   - Why: phone first. Today "PYTHON AND RUST / rustmapper" reads as one block of three lines. A heading needs more
     space above it than the text around it [S7].

3. **go_go_go without browser impersonation** (`chart.toml`, the Also text for go_go_go; one line).
   - "**go_go_go** — rustmapper's counterpart in Go, with the same crawl, resume and export-sitemap commands, plus
     optional headless-Chrome rendering and SQLite storage with full-text search."
   - Keep the README-claims anchors for the two features that stay (`--enable-js-rendering`, `--enable-sqlite`,
     defaults false). Drop the `--enable-tls-fingerprint` one.
   - Why: on a page that already says, truthfully, that my main crawler doesn't pause and ignores `Crawl-delay`,
     advertising a feature its own README sells as a way "to bypass JA3 fingerprint detection" [S4] tells a site owner
     I build crawlers to get past them. That's the opposite of the norms the people who run sites publish [S5], and
     of what my Scrapy project does by default [S6]. Picking what goes in one line is my call, and this one doesn't
     teach anyone how I work.

4. **Working rule 3 states the measured fact, not the title again** (`chart.toml [[notices]]` 3, :142-146; `proof.py`
   gets a `days_after_first` value; about 15 lines, an AUDIT row, a test).
   - Title: "**Measure from the start.**" Body: "Scrapy exported Prometheus metrics {days:prometheus} days after its
     first commit, and had Grafana dashboards {days:grafana−prometheus} days later." Today that prints 6 (25 Sep → 1
     Oct 2025, `67446a4` → `d571e6e`) and 5 (→ `e8cbe15`, 6 Oct). Cite unchanged: "*Scrapy, Oct 2025: Prometheus
     metrics, then Grafana dashboards.*"
   - The day counts come from `rules[].date` and the repository's first commit date (both already gathered), with
     AUDIT-COVER rows. A test: the fixture dates give the printed numbers, and a rule body that repeats its title's
     key noun with no figure fails.
   - Why: "Dashboards go in version one" teaches nothing the title doesn't, and "before speed" isn't what the history
     shows: the performance redesign landed two days before the first dashboard. A principle should answer "how does
     this affect me?" [S3]. "Six days" does.

5. **Rule 2's cite in the same form as the others** (`chart.toml:136`; one line and a test).
   - "*Scrapy, Oct 2025: raw pages written to Delta Lake with `write_deltalake`.*" (the anchor text that holds at
     `52dcbd8` and at HEAD).
   - Test: every printed cite matches `<repo>, <Mon YYYY>: <what>.`
   - Why: three cites use a colon and one uses a comma. On a list that small the odd one out reads as a typo [S2].

6. **Ai_code_detector says what it does** (`chart.toml`, its Also text; one line plus a claims anchor).
   - "**Ai_code_detector** — `aicd scan` scores each file of a repository for signs of AI authorship, from its
     comments, naming, structure and git history, and says why it flagged it." Anchors in the clone at `aa7368b`:
     `README.md` "aicd scan", `detector_enhanced.py` "StylometryAnalyzer" and "Analyzing git history", and the Phase 3
     per-file explanations.
   - Why: "probabilistic forensics … from stylometry down to git-history patterns" is the repository's tagline. The
     other three Also lines each say what the thing does. This one doesn't.

**Owner, not in this repository, and not re-ranked** (rounds 4 to 7): fix P1, take `--ignore-robots` out of the idle
test, ship 0.1.4, and set Rust-sitemap's About text and `README.md:25`. The red box stays the loudest mark on my
profile until a release exits by itself. One more thing for that list: in this round's run check, `resume` after a
kill failed in 0.1.3 ("Database already open. Cannot acquire lock."). Nothing on the page promises it works, but the
go_go_go line names the command.

## Sources (new this round)

1. [S1] Nielsen Norman Group, "Show Numbers as Numerals When Writing for Online Readers": "numerals often stop the
   wandering eye", "even when they're embedded within a mass of words that users otherwise ignore":
   https://www.nngroup.com/articles/web-writing-show-numbers-as-numerals/
2. [S2] Stanford Persuasive Technology Lab, Stanford Guidelines for Web Credibility: guideline 1 "Make it easy to verify
   the accuracy of the information on your site"; guideline 10 "Avoid errors of all types, no matter how small they
   seem": https://credibility.stanford.edu/guidelines/index.html
3. [S3] UK Home Office Engineering, SEGAS-00002 "Writing a principle": a principle must have a rationale, "the reader
   should readily discern the answer to the question: 'How does this affect me?'", and titles should avoid vague words:
   https://engineering.homeoffice.gov.uk/standards/writing-a-principle
4. [S4] refraction-networking/uTLS README: "ClientHello fingerprinting resistance" and "can be used to parrot
   ClientHello of popular browsers". go_go_go's own README, `README.md:22`, uses it to "bypass JA3 fingerprint
   detection": https://github.com/refraction-networking/utls
5. [S5] Cloudflare, "Perplexity is using stealth, undeclared crawlers to evade website no-crawl directives", 4 Aug
   2025: norms for well-behaved crawlers, including "Don't flood sites with excessive traffic … or use stealth tactics
   to try and dodge detection" and "respecting website signals like robots.txt, staying within rate limits":
   https://blog.cloudflare.com/perplexity-is-using-stealth-undeclared-crawlers-to-evade-website-no-crawl-directives/
6. [S6] Scrapy documentation, Settings: `ROBOTSTXT_OBEY` is enabled "in settings.py file generated by `scrapy
   startproject`", and the template sets `CONCURRENT_REQUESTS_PER_DOMAIN` 1 and `DOWNLOAD_DELAY` 1:
   https://docs.scrapy.org/en/latest/topics/settings.html
7. [S7] Butterick, Practical Typography, "Space above and below": the space below a heading should be smaller than the
   space above, and where paragraphs are already spaced, "the space you add around a heading should be larger, to
   create a distinction": https://practicaltypography.com/space-above-and-below.html
8. [S8] RFC 9309, Robots Exclusion Protocol, §1 and §2.4: "It may be inconvenient for service owners if crawlers visit
   the entirety of their URI space", and crawlers "SHOULD NOT use the cached version for more than 24 hours". This is
   the standard the load note's robots.txt clause is measured against: https://www.rfc-editor.org/rfc/rfc9309.html
9. [S9] Google Search Central, "Reduce the Googlebot crawl rate": on 500, 503 and 429 Googlebot "reduces your site's
   crawl rate across the whole hostname" and raises it again when the errors drop. It's the yardstick a site owner
   brings to the load note, and the reason the note stays:
   https://developers.google.com/search/docs/crawling-indexing/reduce-crawl-rate
10. [S10] Zyte, "How to crawl the web politely with Scrapy": per-domain concurrency, not global concurrency, is what a
    target site feels, which is why the load note gives "20 at a time to one host" first:
    https://www.zyte.com/blog/how-to-crawl-the-web-politely-with-scrapy

Clones and data: `assets/stats.json` (`edition`, `routes.rustmapper`, `handoffs`, `figures`, `rules`, `runcheck`,
`repos[]`); sdist 0.1.3 `state.rs:285`, `cli.rs:58, :98`, `main.rs:90, :113`, `bfs_crawler.rs:433`;
ideal-url-organizer `159968a` (`src/main.py` `self.methods`, 21 keys by ast; 25 `method_*.py`; `PageContent` in 22 to
25); Scrapy.git (`67446a4` first commit 25 Sep 2025, `d571e6e` 1 Oct, `52dcbd8` 4 Oct, `e8cbe15` 6 Oct;
`Scraping_project/src/settings.py:121, :140, :147, :179`; `docker-compose.yml:8, :249`; `scout_spider.py:47`;
`experimental/base_spider.py:52`); go_go_go `4078b55` `README.md:22, :109-111`; Ai_code_detector `aa7368b`
`README.md`, `detector_enhanced.py:77, :195`.
