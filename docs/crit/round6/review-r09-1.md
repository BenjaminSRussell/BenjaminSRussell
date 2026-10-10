# Review round 9, reviewer 1: Ben, the owner

10 Oct 2026. What I looked at: every PNG in `scratchpad/r6/build/round-08/`. That covers the desk sheet at 870 (day
and night), the phone sheet at 390 and 308 (day and night), the desk page (two screens), and the phone page at 390
(six screens) and at 360 (seven). I read `README.md`, `SPEC.md`, `LOG.md` (round 8's fixes) and the reviews from
rounds 1 to 8. Nothing already fixed is repeated here. I checked every figure against `assets/stats.json`, the 0.1.3
sdist (`scratchpad/r6/sdist013`) and the clones.

Verdict: **not yet. 8 / 10.** All of round 8's fixes landed. There is one count for ideal-url-organizer (21 and 25,
explained). The phone heading now stands clear of my role line. go_go_go has lost the impersonation clause. Rule 3
gives its days, the cites share one form, Ai_code_detector says what it does, F1 states the per-host cap, and the
two levers and the no-JavaScript line are on the page.

The image does what I asked for. Read top to bottom, it's directions through my crawler: what you install, where
URLs come from, what repeats for every page, where it bites, how you stop it, what file you get, and which of my
other projects reads that file. That's the oldest kind of route map there is. Ogilby's strip maps of 1675 put one
road on a strip, in order, with what you meet along it, continued from one strip to the next [S8]. I would ship the
image as drawn the day 0.1.4 passes the run check.

What I won't ship is the text around it, for three reasons. Under the picture my flagship reads as a run of warnings
in long paragraphs. One line tells the visitor about my to-do list instead of the tool. And the Scrapy instructions
contradict their own code block.

## The first question: does it meet my goal?

- **A deep purpose for the map.** Yes. It shows the order of things, the loop, and where the trap sits in that
  order, and a list can't show those. Strip the colour out and it still reads as directions.
- **True about my projects.** Yes, line by line (table below). There's one new fact I found in the code. It belongs
  in Rust-sitemap, not here (owner actions, item 1).
- **Nothing chases a reason.** In the image, yes. On the page, the rustmapper opener doesn't hold up: "the Python
  API, built with maturin, is on main and not yet released". It tells a stranger about something they can't use and
  gives them nothing to do about it. That's my to-do list, and the spec already rules to-do lists off the front
  page (SPEC §3, the hand-off joins: "they are Ben's to-do list, not a visitor's").
- **Nothing announces the theme.** Yes. No word names it, and nothing winks.
- **Reads on a phone.** The image does, in one screen. The rustmapper text under it doesn't read well. After the
  code block come three paragraphs of prose holding seven separate cautions (no pause, 256 at once, `Crawl-delay`,
  https-only robots, the two flags, no JavaScript, one `sitemap.xml`). On a 390 phone that's about 21 lines of
  continuous text, with code spans breaking mid-word ("`Crawl-`/`delay`"). 79 % of readers scan a new page and only
  16 % read word by word. Bulleted lists and scannable layout measured 47 % better [S2]. Google's own style guide
  says too many notices "begin to lose their visual distinctiveness", and it advises against two in a row [S1]. Each
  caution is true, and a stranger about to run my crawler needs each one. So none of them is cut. They get
  stacked so a phone reader sees them as one checklist, with the fix next to each problem.

## Figures checked

| Printed | Source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.date`; all four uploads 8 Nov 2025 | 0.1.3, 2025-11-08 | yes |
| by default: sitemaps, certificate logs, Common Crawl | sdist `cli.rs` `default_value = "all"`; `bfs_crawler.rs:188-192` | | yes |
| up to 20 pages at a time from each host | sdist `state.rs:285` `max_inflight: 20`, `frontier.rs:655` | 20 | yes |
| your site, its subdomains and its parent domain | sdist `url_utils.rs:81-91` (both suffix branches); applied to seeds too, `frontier.rs:492` | | yes |
| logged to disk, then saved to redb, in batches | `routes` W1 anchors | | yes |
| never exits by itself; `Received work item` | runcheck `ends_by_itself` false at 150 s; `quiet_after_last_page` ok | | yes |
| a second press before `Saved to:` quits without writing | runcheck `second_ctrl_c`: exit 1, no file | | yes |
| fields url, depth, status_code, title | sdist `state.rs:98-114` `SitemapNode` | | yes |
| sorted 21 ways; Also: 25 = 21 + 4 | `src/main.py` `self.methods` 21 keys (ast, at `159968a`); 25 `method_*.py` | 21, 25 | yes, and they agree now |
| no pause; 256 at a time across all hosts | runcheck `robots_read`: closest fetches 1 ms apart; sdist `cli.rs` workers 256; `crawl_delay_secs: 0` | | yes |
| ignores `Crawl-delay`; robots.txt only over https | sdist `robots.rs:19` `format!("https://{}/robots.txt"…)`; runcheck `robots_read` false | | yes |
| `--workers 1` one at a time | runcheck `workers_cap`: at most 1 open | | yes |
| 3 min from a cold cache, 4-core | runcheck install median 171.4 s, 4 CPUs | | yes |
| On main at `32c2651` · 176 tests · CI 7 Oct · 16k lines of Rust | `repos[Rust-sitemap]`: head `32c2651`, 176, success 2026-10-07, 16,390 | | yes |
| `96e7a1a` · 1,920 tests (all but 41) · CI 8 Oct · MIT · 69k | `repos[Scrapy]`; `ci_selection.not_selected` 41; 69,036 | | yes |
| circuit breaker: 5 URLs, 60 s | `stage2_worker.py:218-219` | 5, 60 | yes |
| Languages Python, Rust; Swift, JavaScript, TypeScript, C, Go | `main_language` over the 21 (profile excluded): Python 10, Swift 3, JS 2, TS 2, Rust 2, C 1, Go 1 | | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | `commits` 101 + Claude 45; 420 + jules 49 + Claude 22 + dependabot 8; `coauthored.agent` 1, 30 (Scrapy's other 165 trailers name Ben himself, from squash merges, checked in `Scrapy.git`) | | yes |
| Rule 3: 6 days, then 5 | `67446a4` 25 Sep 2025 → `d571e6e` 1 Oct → `e8cbe15` 6 Oct (`Scrapy.git`) | 6, 5 | yes |
| Rule 1 Oct 2026; rule 2 Oct 2025; rule 4 Nov 2025 | `099dd6c` 8 Oct 2026, `52dcbd8` 4 Oct 2025, `2be623e` 13 Nov 2025, all his | | yes |
| 15 more | 11 listed + 4 on the "Also:" line | 15 | yes |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page | keep | GitHub puts the profile README at the top of the profile [S6], so the image is the first thing read. On the repository page and in link previews there's no other name |
| Role line, two caps lines | crawl and data infrastructure; Python and Rust | keep | the drawing under it proves the first line |
| Empty left column under the role (desk) | nothing | keep | the room is what makes the route read first |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project, and what it gives you | keep | the phone gap is fixed |
| Start bar + `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | the date sits on the thing it dates |
| Magenta track | one way through, top to bottom | keep | a strip map's road [S8] |
| Stop rings | one step the tool takes | keep | |
| S1 seeds | URLs come from more than links, by default | change | true, but the wording is a noun phrase built around "looked up rather than followed", and every other row has a verb. Three lines on the phone (must-fix 4) |
| F1 fetch, per-host cap, scope | the loop's work and its reach | keep | right now that it says the cap |
| W1 write path | it saves as it goes | keep | it's why export works after a kill (runcheck `export_after_kill` ok) |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Gap in the track under the loop | the loop has no exit but Ctrl-C | keep | |
| H1, red dotted box | the catch in 0.1.3, and how to tell you're done | keep the mark | true. It's still the loudest thing on my profile, and the fix is mine (owner actions) |
| C1 Ctrl-C | the one thing you do, and the second press to avoid | keep | |
| End bar + `data/sitemap.jsonl` + fields | what you get, in the struct's own words | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | my projects feed each other | keep | the number now agrees with the page |
| Night editions | the same | keep | contrast holds in both |
| Phone editions (390 and 308) | the same, in one screen | keep | S1 is the one row that wraps to three lines for no gain |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image + alt text | above | keep | |
| Link line | where to go | keep | |
| "Ben Russell builds …" | what I build | keep | |
| Languages | what I write in | keep | from the data |
| Stack | what I build on | keep | |
| Pick sentence | which tool for which job | keep | this is rustmapper's real opener |
| rustmapper about line | pip gives a command line; an API I haven't released | cut | to-do list, not the tool. The code block already shows what pip gives (must-fix 2) |
| rustmapper facts line | alive, tested, size, which commit | change | it needs the project link at its head once the about line goes (must-fix 2) |
| rustmapper code block | how to run, stop and recover | keep | fits 360 |
| Wheel note | whether pip just works on your machine | keep | it belongs to the install, right under the block |
| L1 + L2 (load, levers) | what it does to a server, and how to turn it down | change | right content, wrong form: cautions in prose (must-fix 1) |
| L3 + X1 (no JavaScript, one sitemap.xml) | what it can't see; the file limit | change | same (must-fix 1) |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy run sentence | where to run it, what it needs | change | it says run "in `Scraping_project`", then the block's first line is `cd Scrapy/Scraping_project`. Follow the sentence and the first command fails (must-fix 3) |
| Scrapy code block | how to start it | keep | |
| Grafana note + three bullets | what Scrapy does that rustmapper doesn't | keep | |
| Also (four lines) | four more projects, each by what it does | keep | |
| 15 more | the rest | keep | |
| Working rules 1–4 | how I work, each with a dated cite | keep | |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn, how it was run, who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **The rustmapper cautions become one short list** (`render_readme.py`, which renders the text entries L1, L2, L3
   and X1 from `chart.toml [route.rustmapper]` at `:707-790`; the anchors, scopes and runs stay as they are. About 30
   lines and two tests.)
   - The wheel note stays as the one sentence under the code block. After it, one lead-in and five items, each a
     problem with its lever beside it:

     > Before you point it at a site you don't run:
     > - It sends requests with no pause between them, up to 256 at a time across all hosts. `--workers 1` sends one
     >   at a time.
     > - 0.1.3 ignores `Crawl-delay`, and asks for `robots.txt` only over https, so a plain-http site's rules are not
     >   read.
     > - By default it asks crt.sh and Common Crawl about your domain. `--seeding-strategy none` asks no one.
     > - It reads links from the HTML a server sends, and no JavaScript runs. go_go_go can render pages in headless
     >   Chrome.
     > - It writes one `sitemap.xml` however many pages it found. The format allows 50,000 URLs per file.

   - Each item is one existing text entry (L1 split at its lever; L2's seeding half joins the third item). The words
     come from the existing anchors. "crt.sh" is backed by the release anchor `ct_log_seeder.rs`
     `"https://crt.sh/?q=%.{}"`, which needs a new anchor row. An item whose entry retires (for example, X1 once a
     release has `SitemapIndexWriter`) drops out of the list. When none is left, the lead-in goes too.
   - Tests (fast tier): the rustmapper block has at most one prose paragraph after the code block. The list holds
     ≤ 5 items, each ≤ 25 words. STRINGS-TWICE still passes (the 20-per-host cap stays in the image only).
   - Why: the cautions are the most useful text on the page for a stranger, and in prose they're the hardest to
     scan. Readers scan [S2]. Notices in a row lose their force [S1]. A list should be 2 to 7 short items of the
     same structure, introduced by a sentence or a fragment ending in a colon [S3]. On the 390 phone this turns about
     21 lines of paragraphs into five short items you take in at a glance. It's the same facts in less space, and it
     reads as care rather than confession.

2. **Cut the Python-API line. The project link heads the facts line** (`render_readme.py`, `about:Rust-sitemap`
   block and the `python_api` gate at `chart.toml:489-490`; about 10 lines and one test.)
   - Remove "**[rustmapper](…)**: `pip install` gives you its command line; the Python API, built with maturin, is
     on main and not yet released." The facts line becomes: "**[rustmapper](…)** · *on main at `32c2651`: built on
     tokio, redb, rkyv, reqwest, clap · 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust*".
   - Once a wheel ships the `rustmapper` module (`edition.modules`), the gate can print one fact instead: "`import
     rustmapper` works after `pip install`". That's a fact a visitor can act on.
   - Test: no visible sentence on the page contains "not yet released" or "not released" unless it also names a
     command or a flag the reader can use.
   - Why: every element needs a purpose for the visitor. This line exists to explain my packaging state. The code
     block right under it already shows what pip gives you. "Maturin" stays in the Stack line, where it's true of the
     0.1.3 wheel too.

3. **The Scrapy run sentence agrees with its block** (`README.md` Scrapy run sentence, or its `chart.toml` source,
   and `tests/test_pipeline.py:495`; one sentence and the test string.)
   - "Run these from the folder you cloned [Scrapy](…) into; `start.py` runs only inside `Scraping_project`.
     `python start.py` runs all four stages and crawls a university's sample site. It needs Docker and the
     `docker-compose` command (Docker Desktop has it; on Linux, install Compose standalone). The last command runs
     only discovery, on your site."
   - That also cuts the 26-word clause about the Compose plugin to 9 words, with the same instruction.
   - Test: the sentence before the block may not say "in `Scraping_project`" when the block's first line `cd`s into
     it.
   - Why: a reader who does what the sentence says types `cd Scrapy/Scraping_project` from inside
     `Scraping_project`, and it fails. The first command a stranger types has to work.

4. **S1 says what it does, with a verb** (`chart.toml [route.rustmapper]` S1 at `:525` and its `instead` at `:531`;
   two strings, no anchor changes.)
   - "starts from your URL; by default also from sitemaps, subdomains in certificate logs and Common Crawl". The
     `instead`: "starts from your URL; if asked, also from sitemaps, subdomains in certificate logs and Common
     Crawl".
   - F1, the next row, says links are followed, so S1 doesn't need "rather than followed" to make the contrast.
   - Expected phone height: S1 goes from three lines to two (−34 units). Desk stays two lines. ROUTE-HEIGHT and the
     render tier are unchanged otherwise.
   - Why: "your URL and, by default, URLs looked up rather than followed" is the only row with no verb, and the hardest
     row to read cold. Plain-language guidance: the most direct form of the verb, shorter words [S4]. List items of
     one structure, each starting with a verb [S3]. I've complained about weird wording before. This is the last
     row that has it.

**Owner, outside this repository (not ranked here; carried from rounds 4 to 8, plus one new item).**

1. **New: the seeders ask about the wrong domain.** In 0.1.3 and on main (`32c2651`), `bfs_crawler.rs` seeds
   crt.sh and Common Crawl with `url_utils::get_root_domain`, which is the last two labels of the host. For a site
   on `github.io`, `co.uk` or `com.au`, that's the public suffix, not the site. Common Crawl gets asked for
   `*.github.io` (capped at 100,000 URLs, `MAX_COMMON_CRAWL_RESULTS`), and the frontier then throws nearly all of it
   away (`frontier.rs:492`). crt.sh answered `%.co.uk` with a 502 today. The Public Suffix List exists because
   "there was and remains no algorithmic method" for this, and the last-two-labels rule fails for `co.uk` [S5].
   Common Crawl asks people "not [to] overload the URL index server" [S6]. The right function,
   `get_registrable_domain` (PSL-backed), is already in `url_utils.rs:24`. Use it for the seeders, add a test with
   `blog.example.co.uk`, and the image's S1 stays true with no edit here.
2. Still open: fix P1, ship 0.1.4 with a command and a crawl that exits by itself (the red box retires itself),
   commit Rust-sitemap's LICENSE, fix the About text and `README.md:25`, let `start.py` accept `docker compose`, and
   `resume` after a kill ("Database already open"). The image doesn't go to `main` until 0.1.4 passes the run check.

## Sources (new this round)

1. [S1] Google developer documentation style guide, "Notes, cautions, warnings, and other notices": "Don't use too
   many notices"; with several on a page "they begin to lose their visual distinctiveness"; avoid "two (or more)
   notices in a row": https://developers.google.com/style/notices
2. [S2] Nielsen Norman Group, "How Users Read on the Web": "79 percent of our test users always scanned any new page";
   16 % read word by word; scannable layout 47 % better, concise text 58 % better:
   https://www.nngroup.com/articles/how-users-read-on-the-web/
3. [S3] Microsoft Writing Style Guide, "Lists": 2 to 7 items, each "fairly short", "consistent in structure … a phrase
   that starts with a verb", introduced by "a complete sentence, or a fragment that ends with a colon":
   https://learn.microsoft.com/en-us/style-guide/scannable-content/lists
4. [S4] digital.gov plain-language guide, "Writing": use "the strongest, most direct form of the verb possible";
   shorter words: https://digital.gov/guides/plain-language/writing
5. [S5] Public Suffix List, "Learn more": the two-label rule "did not work for top-level domains where only
   third-level registrations are allowed (e.g. co.uk)"; "there was and remains no algorithmic method":
   https://publicsuffix.org/learn/
6. [S6] Common Crawl Index Server: "Please do not overload the URL index server"; bulk work belongs on the columnar
   index: https://index.commoncrawl.org/
7. [S7] GitHub Docs, "About your profile": "GitHub shows your profile README at the top of your profile page":
   https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/about-your-profile
8. [S8] Brock University Map, Data & GIS Library, "Road Maps of England and Wales from the atlas Britannia, 1675":
   "Each strip represents a part of the road and the surrounding environment, with the top of one strip continued at
   the bottom of the strip next to it"; the strips record "hills, rivers, bridges … notable side roads". That's the
   form the image takes, one route in order, with what you meet on it:
   https://brocku.scholaris.ca/items/925b97cd-3481-4579-be3e-d2ca2c30b83b
9. [S9] GitHub Docs, "Basic writing and formatting syntax": unordered lists with `-`, `*` or `+`, which is the
   Markdown the list in must-fix 1 renders from, with no HTML the sanitiser could strip:
   https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
10. [S10] GOV.UK Design System, "Warning text": warn "when you need to warn users about something important", such as
    the consequences "of an action … that they might take". That's the test each list item in must-fix 1 passes,
    and why none is cut: https://design-system.service.gov.uk/components/warning-text/

Measured today: `crt.sh/?q=%.co.uk&output=json&exclude=expired` returned 502 in 0.7 s; `%.github.io` returned 200 in
1.1 s.

Clones and data: `assets/stats.json` (`edition`, `runcheck.rustmapper.steps`, `repos[]`, `coauthored_total`,
`agent_authored`); sdist 0.1.3 `bfs_crawler.rs:170-262`, `url_utils.rs:14-21, :24-29, :81-91`,
`frontier.rs:492, :655, :670, :814`, `common_crawl_seeder.rs:9, :185, :236`, `ct_log_seeder.rs:11, :179`,
`state.rs:98-114, :285`, `robots.rs:19`, `config.rs:35`; Rust-sitemap `32c2651` (`get_root_domain` at
`bfs_crawler.rs:245`, `MAX_COMMON_CRAWL_RESULTS`); ideal-url-organizer `159968a` (`self.methods` 21 by ast, 25
`method_*.py`); `Scrapy.git` (first commit `67446a4`; `d571e6e`, `e8cbe15`, `52dcbd8`, `099dd6c`; co-author
trailers: Ben 168, Claude Sonnet 5 28, Claude 2); Scrapy `stage2_worker.py:218-219`; `chart.toml:489-490, :515-535,
:707-790`; `tests/test_pipeline.py:495`.
