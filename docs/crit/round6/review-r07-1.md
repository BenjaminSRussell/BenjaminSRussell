# Review round 7, reviewer 1: Ben, the owner

10 Oct 2026. What I looked at: every PNG in `scratchpad/r6/build/round-06/`. That is the desk sheet at 870 (day and
night), the phone sheet at 390 and 308 (day and night), the desk page (two screens), the phone page at 390 (six
screens) and at 360 (six screens). I read `README.md`, `SPEC.md`, `LOG.md` (the round-6 fixes) and the 18 reviews from
rounds 1 to 6. I don't repeat anything that was fixed. Every figure was checked against `assets/stats.json`, the 0.1.3
sdist (`scratchpad/r6/sdist013`) and the clones, including the full-history bare clones (`clones/*.git`).

Verdict: **not yet. 8 / 10.** Every round-6 fix landed. M1 is gone. The hand-off reads "sorted 25 ways by
ideal-url-organizer". F1 is in plain words. The phone sheet is sized for the 308 px image GitHub actually shows. Rule 4
cites my own commit. The image does what I asked for: it shows how my crawler runs, in order, with the one place it
goes wrong, where the output lands, and which of my other projects picks it up. Nothing has a size, nothing announces
a theme, and it reads in one phone screen.

I still wouldn't ship it as is. There are four problems in this repository, all small, and the release that is mine
to cut (not repeated here). Two of the four break my own rules, "phone first" and "the data doesn't look exactly
accurate", in places nobody has looked yet.

## The first question: does it meet my goal?

Mostly. Taking the goal line by line:

- **Deep purpose for the map.** Yes. A stranger learns how to start rustmapper, what happens to each URL, where it
  bites, how to stop it, what file they get, and what reads that file next. The loop bracket and the break in the
  track show "this repeats until you stop it", and a list can't show that. The magenta line is the route colour a
  chartplotter uses, and nobody has to be told that.
- **Every element has a purpose.** Every mark answers one of the spec's five questions. One line fails as *reading*,
  though its fact is right. On the phone, F1's last line runs straight into G1: "…its subdomains and its parent
  domain / fetches fewer pages at once when saves / average over 500 ms." Read top to bottom, the parent domain is
  what fetches fewer pages. That's a garden-path sentence, and readers keep the wrong first reading even after they
  correct it [S6]. The same join is on the desk.
- **True about my projects.** The image is. The page has two errors nobody caught.
  - "**Languages** Python, Rust; Swift, C, TypeScript, Go." leaves out JavaScript. Data_science_dev is JavaScript
    (108,779 lines, 467 of my commits, more than Scrapy's 420) and so is Wheel. Employers read the languages in your
    projects as the skills you have [S8].
  - Working rule 1's cite, "*Scrapy, Sep 2025: a circuit breaker in the error handler*", points to a class
    (`src/common/error_handling.py`, `fd33c11`) that nothing called. It was deleted six days later (`1b0f502`, 5 Oct
    2025). The breaker that runs today, per host, is my commit `099dd6c` from 8 Oct 2026, and the Scrapy bullet above
    already describes it.
- **Nothing chases a reason.** Yes, in the image. In the Scrapy code block, six of its thirteen lines are comments.
  GitHub's own docs say to put explanatory text before a code block, not inside it, and to keep code lines to about
  60 characters so nobody has to scroll [S1].
- **Nothing announces the theme.** Yes. No word names it. T-WORDS holds.
- **Reads on a phone.** The image does. The code blocks don't. At 360 px the rustmapper block cuts the colon off
  "# sitemap.xml, even after a kill:". The Scrapy block cuts five lines, including two trailing `\` continuation
  marks, so the command looks broken. At 390 px it still cuts "# or only discovery, on your own sit". The 38-column
  check passes because it doesn't measure the phone. In the renders, 32 columns fit at 360 and 36 at 390. GitHub sets
  code at 85 % with `overflow: auto`, so a long line is cut and scrolls; it doesn't wrap [S2]. 360 px Android widths
  are still on the commonest list, behind the iPhones [S3].

## Figures checked

| Printed | Source | Value | Holds |
|---|---|---|---|
| pip install rustmapper · 0.1.3 · 8 NOV 2025 | `edition` | 0.1.3, 2025-11-08, latest | yes |
| your URL, plus by default … sitemaps, certificate logs, Common Crawl | `routes` S1, verified both trees; sdist `cli.rs` `default_value = "all"` | | yes |
| fetches a page; queues links to your site, its subdomains and its parent domain | `routes` F1, verified both; runs `crawl_ctrl_c` | | yes (reading: must-fix 3) |
| fetches fewer pages at once when saves average over 500 ms | sdist `main.rs:90` `THROTTLE_THRESHOLD_MS: f64 = 500.0`, `:113` | | yes (reading: must-fix 3) |
| logged to disk, then saved to redb, every 50 ms | sdist `writer_thread.rs:11` `BATCH_TIMEOUT_MS: u64 = 50` | | yes |
| 0.1.3 never stops by itself; done when `Received work item` lines stop | sdist `bfs_crawler.rs:433`; runcheck `ends_by_itself` false at 150 s, `quiet_after_last_page` ok | | yes |
| press Ctrl-C once to write `data/sitemap.jsonl` | sdist `main.rs:519` force-quit string; runcheck crawl step ok, exit 2.0 s after one SIGINT, 3 lines | | yes |
| fields: url, depth, status_code, title, … | `handoffs[0].writer_fields_*` | | yes |
| sorted 25 ways by ideal-url-organizer | `handoffs[0]` state `runs`; 25 `method_*.py` in the clone | 25 | yes |
| 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust · `32c2651` | `repos[Rust-sitemap]` | 176; success 2026-10-07 at `head_sha`; 16,390 | yes |
| 1,920 tests · CI passed 8 Oct 2026 · MIT · 69k lines of Python · `96e7a1a` | `repos[Scrapy]` | 1,920; success; MIT; 69,036 | yes |
| 3 min from a cold cache on a 4-core Linux machine | runcheck install | median 171.4 s, 4 CPUs | yes |
| 20 at a time to one host, 256 in all, no pause; robots only over https | sdist `state.rs:285` `max_inflight: 20`; runcheck `robots_read` false (no `GET /robots.txt`, `/secret.html` fetched, 1 ms apart) | | yes |
| 5 URLs fail every retry → left alone 60 s | `stage2_worker.py:218-219` (round 6) | | yes |
| 45 of rustmapper's 146; 71 of Scrapy's 499 | `repos[].commits` + `others` | 101 + 45 = 146; 420 + 49 + 22 + 8 = 499, agents 71 | yes |
| 15 more | 22 − profile − 2 − 4 | 15 | yes |
| **Languages** Python, Rust; Swift, C, TypeScript, Go | `repos[].main_language`: Python 11, Swift 3, JavaScript 2, TypeScript 2, Rust 2, C 1, Go 1 | JavaScript missing | **no** (must-fix 2) |
| Rule 1 "Scrapy, Sep 2025: a circuit breaker in the error handler" | `rules[0]` `fd33c11`; `git grep CircuitBreaker fd33c11 -- src` finds only the class; file deleted `1b0f502` | a class with no caller that lasted six days | **misleading** (must-fix 4) |
| Rules 2 to 4 | `rules[1..4]`, all `first_is_his` or `scope: self` | | yes |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page | keep | read first |
| Role line, two caps lines | crawl and data infrastructure, in Python and Rust | keep | the drawing under it proves both words |
| Empty left column (desk) | nothing | keep | it's breathing room I asked for, not filler |
| "rustmapper" + header sentence | which project, and what it writes | keep | one sentence that's true for a 404 link too |
| Start bar | where you begin | keep | the fixed entrance |
| `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old that build is | keep | the date sits on the command |
| Magenta track | one way through, top to bottom | keep | the route colour, unannounced |
| Stop rings over the track | one step the tool takes | keep | |
| S1 seeds | URLs come from more than links, by default from outside services | keep | worth knowing before you point it at your own site |
| F1 fetch and queue | the crawl loop and its scope | change | its last line runs into G1 (must-fix 3) |
| G1 governor line | it slows when saving falls behind, at 500 ms | change | the fact stays, but it has to read as its own clause (must-fix 3) |
| W1 write path | log, then store, every 50 ms | keep | the data-infrastructure signal |
| Loop bracket and up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Break in the track under the loop | the loop has no exit but Ctrl-C | keep | true of 0.1.3, and it closes by itself when a release ends on its own |
| H1, red dotted box | the catch in this release, and how to tell you're done | keep the mark | true. Its cause is mine to fix in Rust-sitemap (owner note below) |
| C1 Ctrl-C | the one thing you do, and what it writes | keep | |
| End bar + `data/sitemap.jsonl` + fields | what you get, in the struct's own words | keep | |
| Hand-off line, arrow, "sorted 25 ways by ideal-url-organizer" | my projects feed each other, and what the next one does | keep | fixed last round, and it reads right |
| Night editions | the same | keep | contrast holds |
| Phone editions (600 wide) | the same, in one screen | keep | 13.3 px at 308 |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image + alt text | above | change | must-fix 3 |
| Link line | where to go | keep | |
| "Ben Russell builds …" | what I build | keep | |
| Languages | what I write in | change | JavaScript is missing (must-fix 2) |
| Stack | what I build on | keep | every item is in a facts line or a bullet |
| Pick sentence | which tool for which job | keep | |
| rustmapper sentence | the API isn't released | keep | fixed last round |
| rustmapper facts line | alive, tested, size, snapshot | keep | |
| rustmapper code block | how to run, stop and recover | change | one line cut at 360 (must-fix 1) |
| Wheel note, load note, 50,000 note | when pip just works; what it does to a server; the sitemap limit | keep | all true, all useful to a stranger |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy code block | how to start it | change | five lines cut at 360. "In a clone of this repository" on my profile means the profile repository. Explanations belong before the block (must-fix 1) |
| Grafana note + bullets | what Scrapy does that rustmapper doesn't | keep | |
| Also | the next four | keep | each line is a mechanism, not an adjective |
| 15 more | the rest | keep | |
| Working rule 1 | how I work, with proof | change | the proof is a class nothing called (must-fix 4) |
| Working rules 2 to 4 | as above | keep | each cites my own commit |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn, and agent authorship | keep | |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **The code blocks fit a 360 px phone** (`scripts/checks/readme.py:20` `CODE_COLUMNS`; `render_readme.py`, the
   `install:Rust-sitemap` block and the Scrapy block; about 20 lines and tests).
   - Set `CODE_COLUMNS = 32`. Measured in this round's renders, 32 columns fit at 360 and 33 are cut. Record that in
     the check's docstring with the date, the way HERO-COLUMN-PX records its table.
   - rustmapper block: "# sitemap.xml, even after a kill" (32, no colon). The other lines are already ≤ 27.
   - Scrapy block. Move the explanations into one sentence before the block, as GitHub's docs say [S1]: "From a clone
     of [Scrapy](…), in `Scraping_project` (`start.py` runs only there). `python start.py` runs the whole pipeline; it
     needs docker and docker-compose and crawls a university's sample site. The last command runs only discovery, on
     your site." Then:
     ```sh
     cd Scrapy/Scraping_project
     python start.py
     docker-compose run --rm \
       scraper scrapy crawl scout \
       -a allowed_domains=<domain> \
       -a start_urls=<url>
     ```
     The longest line is 31. That's 6 lines where today's block has 13, about 7 phone lines shorter. It also gets rid
     of "this repository", which on my profile names the wrong repository.
   - Keep the FIGURES rows that read "Scraping_project", "start.py" and "scout". Keep the `docker-compose` /
     `REQUIRED_TOOLS` anchor.
   - Tests: no line in any fenced block is longer than 32 columns. No visible README text holds "this repository".
   - Why: phone first. Today a stranger on Android sees commands with their `\` cut off.

2. **Languages comes from the data and includes JavaScript** (`README.md:24` is hand-typed outside every marker; add a
   `languages` marker in `render_readme.py` and `chart.toml [copy] languages_lead = ["Python", "Rust"]`; about 15
   lines and a test).
   - The text is the lead pair, then every other `main_language` of the public repositories (profile excluded),
     ordered by repository count and then by lines. Today that gives: "**Languages** Python, Rust; Swift, JavaScript,
     TypeScript, C, Go."
   - Add a FIGURES-style test: every `main_language` in `stats.json` appears in the line, and the line names nothing
     that isn't one.
   - Add an AUDIT.md row: `main_language` is Linguist's byte count per repository, vendored and generated files
     excluded [S10].
   - Why: the line drops the language of my second-busiest repository, 467 commits. People read your languages as your
     skills [S8], and JavaScript and TypeScript are the most-used languages on GitHub [S9].

3. **F1 and G1 read as one clause each** (`chart.toml` F1 at :437 and G1 at :458; `sheets/route.py` where a `note`
   is set under its stop; about 10 lines and a test).
   - Merge G1's words into F1, so the qualifier sits next to the verb it qualifies: "fetches pages, fewer at once when
     saves average over 500 ms; queues their links to your site, its subdomains and its parent domain".
   - Take F1's release anchors as the union of both entries' anchors, including G1's three on `main.rs` with the
     `producer = true` comparison. F1's scope becomes `release`, which is what the drawing is. Retire G1 as its own
     line, and fold its PURPOSE row into F1's.
   - The 500 stays `{const:THROTTLE_THRESHOLD_MS}`. Desk: two lines, as today. Phone: four lines, as today. Height
     doesn't change.
   - Test: no line of a row ends with a noun and is followed by a line in the same row that starts with a finite verb
     and no punctuation between them. Simpler still: no `note` entry renders as its own line under a stop.
   - Why: on the phone the parent domain is what "fetches fewer pages", and a wrong first parse lingers [S6]. Nothing
     between the lines marks a new clause. Text that sits close together reads as one group [S7].

4. **Working rule 1 cites the breaker that runs** (`chart.toml:113-114`; `data/proof.py` already supports
   `author = "self"`; about 4 lines and a test).
   - Anchor `{key = "breaker", repo = "Scrapy", text = "_host_breakers", author = "self"}`, which is my commit
     `099dd6c`, 8 Oct 2026. Cite: "*Scrapy, {month:breaker}: a circuit breaker for each host in stage 2.*" That prints
     "Oct 2026".
   - NOTICE-AUTHOR checks the scope, as it does for rule 4. Add a NOTICE-LIVE check that each rule's anchor text is
     still in the repository at `head.sha`. Today rule 1 fails it (`class CircuitBreaker` in `error_handling.py` is
     gone) and rules 2 to 4 pass.
   - Why: the rule says the system worth having is the one still running, and its proof is a class nothing ever called
     that I deleted six days later. Honest data only.

**Owner, not in this repository, and not re-ranked** (rounds 4 to 6 asked for it): fix P1, take `--ignore-robots`
out of `crawl_exits_when_idle.rs`, and ship 0.1.4. Set Rust-sitemap's About text and `README.md:25`. Until then the
red box is the loudest line on my profile, and this image doesn't go to `main`.

## Notes (true, not ranked)

- On the phone, the gap from "PYTHON AND RUST" to "rustmapper" (about 26 px at 308) is barely larger than the gaps
  inside the route header, so the project's name reads close to a third title line [S7]. Another 10 to 14 units there
  would fit under the 1,246 gate (1,169 today). I'm not ranking it, because round 6 took that space out on purpose.
- An ANSI Z535-style warning names the hazard, the consequence and how to avoid it [S4, S5]. H1 has the hazard and
  how to tell you're done, and C1 right under it has the action. Split across two adjacent rows like that, it works,
  and the break in the track between them is the drawing's point. Keep it.

## Sources (new this round)

1. [S1] GitHub Docs, content style guide, "Code blocks": "Keep lines in code samples to about 60 characters, to avoid
   requiring readers to scroll horizontally in the code block", and "Locate explanatory text before the code block,
   rather than using comments inside the code block":
   https://github.com/github/docs/blob/main/content/contributing/style-guide-and-content-model/style-guide.md
2. [S2] github-markdown-css (GitHub's rendered Markdown styles): `.markdown-body pre` has `overflow: auto`, and code is
   set at `font-size: 85%`, so long lines are cut and scroll; they don't wrap:
   https://github.com/sindresorhus/github-markdown-css/blob/main/github-markdown.css
3. [S3] StatCounter, mobile screen resolution stats, United States, 2026: 414×896 and 390×844 lead, with 360-wide
   Android sizes still on the list: https://gs.statcounter.com/screen-resolution-stats/mobile/united-states-of-america
4. [S4] ANSI blog, "ANSI Z535.4-2023: Product Safety Signs and Labeling": a message panel carries the hazard, the
   consequence and how to avoid it: https://blog.ansi.org/ansi-z535-4-2023-product-safety-sign-or-label/
5. [S5] In Compliance, "Designing Effective Product Safety Labels: Your Guide to Content": all three items give the
   reader what they need to decide:
   https://incompliancemag.com/designing-effective-product-safety-labels-your-guide-to-content/
6. [S6] Christianson, Hollingworth, Halliwell, Ferreira, "Thematic Roles Assigned along the Garden Path Linger",
   Cognitive Psychology 42, 2001: readers keep the misparse even after reanalysis:
   https://ferreiralab.faculty.ucdavis.edu/wp-content/uploads/sites/222/2015/05/Christianson-et-al.-2001_LingeringInterpretationsGP_Cog-Psych.pdf
7. [S7] Nielsen Norman Group, "Proximity: Gestalt Principle for User Interface Design": elements close together are
   seen as one group: https://www.nngroup.com/videos/proximity-gestalt/
8. [S8] Marlow and Dabbish, "Activity Traces and Signals in Software Developer Recruitment and Hiring", CSCW 2013:
   employers look at "the content of someone's code and the languages they had used", and "the languages they used in
   their projects would signal proficiency in those languages":
   https://www.cs.cmu.edu/~xia/resources/Documents/Marlow-cscw13.pdf
9. [S9] GitHub, Octoverse 2025: TypeScript passed Python and JavaScript in August 2025 as the most used language on
   GitHub: https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
10. [S10] GitHub Linguist, "How Linguist works": it excludes vendored, generated and documentation files, and the
    percentages are bytes of code per language:
    https://github.com/github-linguist/linguist/blob/main/docs/how-linguist-works.md

Clones and data: `assets/stats.json` (`repos[].main_language`, `lines`, `commits`, `others`, `ci`, `head`; `edition`;
`routes.rustmapper`; `handoffs`; `rules`; `runcheck`); sdist 0.1.3 `state.rs:285`, `bfs_crawler.rs:433`,
`main.rs:90,113,519`, `writer_thread.rs:11`; Scrapy.git `fd33c11` (`git grep CircuitBreaker -- src`: the class only),
`1b0f502` (deletes `src/common/error_handling.py`), `e6fe879` (Claude adds `utils/retry.py`, 9 Nov 2025),
`099dd6c` (mine, per-host breaker, 8 Oct 2026), `stage2_worker.py:23,331,923-934`; Data_science_dev.git (1,790
commits by me in the history, `src/js/` 148k lines with 39.5k of task data); ideal-url-organizer (25 `method_*.py`).
README code blocks measured by column: the longest are 38 and 34 (Scrapy) and 33 (rustmapper). In
`page-phone-360-2/3.png` the cut falls after column 32. In `page-phone-3.png` (390) it falls after column 36.
