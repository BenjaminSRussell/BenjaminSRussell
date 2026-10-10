# Review round 11, reviewer 1: Ben, the owner

10 Oct 2026. I looked at every PNG in `scratchpad/r6/build/round-10/`: the desk sheet at 870 (day and night), the
phone sheet at 390 and 308 (day and night), the desk page (two screens), and the phone page at 390 (seven screens)
and 360. I read `README.md`, `SPEC.md`, `LOG.md` round 10 and the round 10 reviews. Nothing already fixed is repeated
here. I checked every figure against `assets/stats.json`, the 0.1.3 sdist (`scratchpad/r6/sdist013`) and the clones,
including the full histories in `clones/*.git` (the working clones are shallow).

Verdict: **not yet. 9 / 10.** Round 10 landed, and it landed right. The Scrapy sentence says what `start.py` does,
with the rows the code actually loads (143,208 and 134,807; I counted them again and got the same). The list says
which release it's about. The stop rule is in the code block where your hands are. No flag breaks in half on a phone.

The image is done. I wouldn't move a mark. It's how you get my crawler, what it does to every page, where it catches
you, how you get out, what file you get and which of my projects reads it. Nothing in it has a size, nothing in it
names a theme, and the two marks that carry the manner (one line to follow, a dotted line round the one danger) are
there because they mean something.

What's left is the bottom of the page, and it comes down to one thing: **three blocks there don't earn their place.**
One working rule makes a claim my own cited repo doesn't keep. One rule repeats a Scrapy bullet word for word in
meaning. One repository line says nothing. All three fixes make the page shorter.

## The first question: does it meet my goal?

- **A deep purpose for the map.** Yes. Only a drawing shows the loop, and where in the loop the trap is.
- **True about my projects.** The image, yes, every row (table below). The page, all but working rule 4
  (must-fix 1).
- **Nothing chases a reason.** Nearly. Rule 4 is a slogan with one import behind it. Rule 1 tells you the circuit
  breaker a second time. "spreadsheet automation" is filler. That's must-fixes 1 to 3.
- **Nothing announces the theme.** Yes. There's no theme word and no wink anywhere.
- **Reads on a phone.** Yes. The image fits one screen at 390 and at 308. The page is about six screens at 390, and
  the fixes take about eight lines off it.

It still doesn't go to `main` until 0.1.4 passes the run check (ROUTE-UNVERIFIED on S2). That's my job, not this
repository's. See the owner notes, because I want to say something new about that this time.

## Figures checked

| Printed | Source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.date` | 0.1.3, 2025-11-08 | yes |
| up to 20 pages at a time from each host | sdist `state.rs` `max_inflight: 20` | 20 | yes |
| sorted 21 ways | ideal-url-organizer `159968a`, 21 record methods + `scripts/import_rust_sitemapper.py` | 21 | yes |
| "for 30 s" (image H1, code comment) | runcheck `quiet_after_last_page`; H1 `quiet` | 30 | yes |
| `--start-url <your-site>` takes a bare domain | sdist `url_utils.rs:178-191` `normalize_url_for_cli` adds `https://` | | yes, so L5's "start at the bare domain" works as typed |
| 176 tests · CI 7 Oct: tests, rustfmt · 16k Rust · `32c2651` | `repos[Rust-sitemap]` `test_functions` 176, `ci.gates`, `lines.Rust` 16,390, `head_sha` | | yes |
| Prebuilt for Apple silicon on CPython 3.13 | `edition.wheels` = `cp313-cp313-macosx_11_0_arm64` | | yes |
| 3 min, cold cache, 4-core | runcheck install median 171.4 s, 4 CPUs | | yes |
| 256 / `--workers 1` / crt.sh by default | sdist `cli.rs`; runcheck `workers_cap` | | yes for 0.1.3, and the lead now says 0.1.3 |
| 1,920 tests (all but 41) · CI 8 Oct · MIT · 69k | `repos[Scrapy]` 1,920; gates; 69,036 | | yes |
| 143,208 bundled URLs, 134,807 on uconn.edu | `Scraping_project/data/raw/uconn_urls.csv` read with Python `csv` (as pandas reads it), hostnames by `urlsplit` | 143,208; 134,807 | yes (counted today) |
| It loads no seeds by default | `start.py:355` `if args.reset_delta:`, `:379` "Skipping Delta Lake reset" | | yes |
| 5 URLs, 60 s | `stage2_worker.py` `DEFAULT_STAGE2_BREAKER_FAILURES = 5`, `_RECOVERY = 60` | 5, 60 | yes |
| Rule 1 "Oct 2026" | `rules[0]` `099dd6c` 2026-10-08, Benjamin Russell, no agent trailer (`Scrapy.git`) | | yes |
| Rule 3: 6 days, then 5 | `67446a4` 25 Sep → `d571e6e` 1 Oct → `e8cbe15` 6 Oct 2025 | | yes |
| Rule 4 "urllib.parse does not [break]" | see must-fix 1 | | **no, not as a fact about this repo** |
| 45 of 146; 71 of 499; co-signed 1 and 30 | `all_hands` − `commits`: 146 − 101; 499 − 420 − 8 dependabot; `coauthored.agent` 1, 30 | | yes |
| 15 more · 21 repositories | 22 in `repos` minus the profile; 2 + 4 + 11 + 4 | | yes |
| excel-and-vba "spreadsheet automation" | `/home/user/excel-and-vba` `eabe846`: one 26-line VBA module, one 55-line Python script | | true, but it says nothing (must-fix 3) |

## Must fix, ranked

1. **Cut working rule 4, "Parse, don't pattern-match."** (`chart.toml` `[[notices]]` n = 4, `:159-170`;
   `tests/test_pipeline.py:296` and `:501`, which name rule 4 as the last row; `docs/data/AUDIT.md` its row. One
   block removed, two test strings changed to rule 3. The `urlparse` anchor test in `tests/test_round6.py:225` can
   stay as a test of the finder.)
   - The body, "A regex for a URL breaks on the first port or login inside it; `urllib.parse` does not.", is a
     general claim, and both halves overreach. RFC 3986 prints a regular expression that splits any well-formed URI
     into its parts [S4]. It keeps the login and port inside the authority instead of breaking on them. Python's own
     docs say `urlsplit()` "does not perform validation" and that components "may contain more than perhaps they
     should" [S5].
   - It isn't true of the repo it cites either. At `159968a` the URL-splitting code (`src/core/url_parser.py`,
     `src/organizers/method_01_by_domain.py`, `src/core/web_crawler.py`) was first committed by Claude on 9 Nov 2025
     (`6e8087f`, `36cc345`). The rule rests on one import of mine four days later (`2be623e`,
     `semantic_analyzer.py`). And the crawler in that repo does the very thing the rule warns about: it sorts links
     into internal and external by comparing raw `netloc` strings (`web_crawler.py:296` and `:309`). `netloc` keeps
     the port, the login and the host's case. So `https://example.com:443/a` counts as *external* from
     `https://example.com/` (I checked: `example.com:443` ≠ `example.com`). Method 24, page authority, one of the
     "4 more from the fetched pages", is built on `internal_links`.
   - The other three rules each carry a fact of mine with a date that teaches something: a breaker, a raw layer,
     metrics in the first week. Rule 4 is a slogan, and its evidence is thinner than its claim. Round 10 called it
     "the thinnest rule" and left it to me. I'm cutting it.
   - Saves about six lines at 390. Three rules are enough. Nothing else in the notices block changes.
   - The bug itself is an owner item (below), not a reason to keep the rule until it's fixed.

2. **Tell the circuit breaker once, in rule 1.** (`README.md:74`, hand-typed Scrapy bullet 3; `chart.toml`
   `[[notices]]` n = 1 `body`, `:119`; the `[[figures]]` rows "5 URLs" and "60 s" at `:378-388` now hold in the
   notices block instead; `tests/test_round6.py:307-308`; AUDIT row. One sentence moved, one test string moved.)
   - Today the page says it twice, 40 lines apart. Bullet 3: "Each host has its own circuit breaker: after 5 URLs on
     it fail every retry, it is left alone for 60 s." Rule 1: "One failing host is set aside for a minute; the rest
     of the crawl goes on." Same fact, said differently. The second reading teaches nothing. GDS put it in one line:
     structure the content "so you won't need another page repeating the same information in a different way" [S8].
     Write the Docs says "Eliminate content overlap" so there's no "parallel maintenance" [S1]. That matters here:
     if the default changes, one copy gets fixed and the other doesn't.
   - Keep it in the rule, because the rule is where it means something. It's evidence of how I build, with a date.
     In bullet 3 it's one more item in a list.
   - Bullet 3 becomes: "Prometheus metrics on Grafana dashboards. Docker Compose and a Helm chart for Kubernetes."
   - Rule 1 body becomes (21 words): "When 5 URLs on one host fail every retry, that host is left alone for 60 s; the
     rest of the crawl goes on." Cite unchanged: "*Scrapy, Oct 2026: a circuit breaker for each host in stage 2.*"
   - Test: STRINGS-TWICE won't catch a paraphrase, so add one assertion: "circuit breaker" or "left alone" appears
     in exactly one block of the visible prose.
   - Saves about two lines at 390.
   - Rule 2 and bullet 1 share three words ("stay raw"), but the rule adds the reason, so they each have a job.
     Leave them.

3. **excel-and-vba goes to the bare "Also:" line.** (`README.md`, hand-typed, inside `<details>`: delete the
   `excel-and-vba — spreadsheet automation.` item and add `[excel-and-vba](…)` to the "Also:" line. Count unchanged
   at 15.)
   - "spreadsheet automation" tells you nothing you couldn't guess from the name. NN/g: a label that's "too obscure
     and vague" has low scent, and people skip it [S2]. Every other line in that list says what the thing does.
   - The repo is 81 lines: a 26-line VBA module (`Enqueue`, `ProcessNext` on a `Queue` sheet) and a 55-line Python
     script that writes audit rows to SQLite. That's honest and small. I'm not going to dress it up with a sentence
     longer than the code. On the bare line next to `Course_crusader` and the widgets, it's listed, and it doesn't
     pretend.
   - Test: none needed beyond the existing count of 15 (11 described + 4 bare becomes 10 + 5).

That's all. The image needs nothing.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page this is | keep | it's the only name in link previews |
| Role, two caps lines | crawl and data infrastructure; Python and Rust | keep | the drawing under it proves it |
| Empty left column (desk) | nothing, on purpose | keep | it makes the route the thing you read |
| "rustmapper" + one-line what it does | which project, what you get | keep | |
| Start bar, `pip install rustmapper`, "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | the date answers "is this current" without a word of excuse |
| Magenta track | one way through, top to bottom | keep | a route line used to mean a route |
| Stop rings | each is one step the tool takes | keep | |
| S1 seeds | URLs come from more than links, by default in 0.1.3 | keep | |
| F1 fetch, per-host cap, scope | the loop's work and how far it reaches | keep | |
| W1 write path | it saves as it goes, to an embedded store | keep | it's why export works after a kill |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Gap in the track under the loop | the only way out of the loop is Ctrl-C | keep | |
| H1, red dotted box | the catch in 0.1.3, and how you know you're done | keep | a danger line round the danger, with the number that clears it. It goes when 0.1.4 lands |
| C1 Ctrl-C | the one thing you do, and the second press not to make | keep | |
| End bar, `data/sitemap.jsonl`, fields | what you get, in the struct's own names | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | my projects feed each other, and that's tested | keep | |
| Night editions | the same | keep | the box and track hold contrast |
| Phone editions (390, 308) | the same, in one screen | keep | |
| Alt text | install, loop, stop, file | keep | 25 words, all true |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image link to the repo | where the drawing's project lives | keep | |
| Link line | where to go | keep | |
| "Ben Russell builds …" | what I build | keep | |
| Languages | what I write in | keep | from the data |
| Stack | what I build on | keep | |
| Pick sentence | which tool for which job | keep | |
| rustmapper facts line | alive, tested, size, which commit, which gates block | keep | |
| rustmapper code block + stop comment | how to run, when to stop, how to recover | keep | the stop rule is now where you act |
| Wheel note | whether pip just works on your machine | keep | |
| "Before you run 0.1.3:" + seven items | what it does to a server, what it can't see, what the file leaves out | keep | every item has its lever or its reason; they retire with 0.1.4 |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy bullet 1 (Delta Lake) | how pages are stored | keep | |
| Scrapy bullet 2 (dedupe, summaries, local model) | what happens to a page | keep | |
| Scrapy bullet 3 (metrics, breaker, deploy) | how it's watched and deployed | change | must-fix 2: the breaker moves to rule 1 |
| Scrapy run sentence | what `start.py` starts, needs and loads, and whose site the seeds are | keep | true both ways now |
| Scrapy code block | how to start it and point it at your site | keep | |
| Grafana note | where to look once it runs | keep | |
| Also (four lines) | four more projects, each by what it does | keep | |
| 15 more (details) | the rest | change | must-fix 3: excel-and-vba to the bare line |
| Working rule 1 | I keep one bad host from stalling a crawl | change | must-fix 2: it carries the numbers |
| Working rule 2 | I keep raw data, and why | keep | the reason is the same one the medallion pattern gives: keep the raw state for "reprocessing and auditing" [S6] |
| Working rule 3 | I measure from the first week | keep | dated, and it's mine |
| Working rule 4 | a slogan about regexes | cut | must-fix 1 |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn, how it was run, who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Owner notes, outside this repository

1. **New: the hold.** Every round since round 4 has ended with "the image doesn't go to `main` until 0.1.4". That
   was my call and it still is. But I should say plainly what it costs. Today `main` still shows the islands map I
   started this whole round by calling pointless. Every week 0.1.4 waits, visitors get the map I rejected, not the
   one I'd ship. So 0.1.4 (P1 and its test, the `LICENSE` that `license-files` names, `[project.scripts]`, the
   release) is now the most valuable work on the whole profile, more than anything left in this repository. If it
   isn't out by the end of October, I'll decide then whether to ship this image with S2 left out. I'm not deciding
   that now, and nobody should loosen the gate for me.
2. **New: ideal-url-organizer compares raw `netloc`.** `src/core/web_crawler.py:296, :309`: compare
   `urlsplit(...).hostname` (lower-cased) and the port with its default filled in, not `netloc`. Otherwise a link
   with `:443`, a login or a capital letter in the host counts as external, and method 24 under-counts internal
   links. Add a test with those three cases.
3. Carried: Scrapy's UConn defaults into a named profile; `restart: unless-stopped` on `scraper` (watch
   `docker-compose ps` on a seeded clone); a "seeding done" line in 0.1.4; `start.py` accepting `docker compose`;
   `resume` after a kill; registrable-domain seeding; statuses and back-off on 429/503; `cargo audit` and
   `clippy -Dwarnings` as blocking.

## Sources (new this round)

1. [S1] Write the Docs, "Documentation principles": under "Unique", "Eliminate content overlap between separate
   sources", so as "to prevent any parallel maintenance". It also says "Accept (some) Repetition", so I only cut a
   repeat that adds nothing (must-fix 2), not rule 2, which adds the reason:
   https://www.writethedocs.org/guide/writing/docs-principles/
2. [S2] Nielsen Norman Group, "Information Scent": "If the link name is too obscure and vague, people might miss a
   good source of information." That's "spreadsheet automation" (must-fix 3):
   https://www.nngroup.com/articles/information-scent/
3. [S3] Nielsen Norman Group, "Accordions on Mobile": collapsing fits "deferring secondary content", and they help
   users "get the big picture before focusing on details". That's why the 15 stay folded and the seven cautions
   stay open: https://www.nngroup.com/articles/mobile-accordions/
4. [S4] RFC 3986, §3.2 and Appendix B: `authority = [ userinfo "@" ] host [ ":" port ]`, and a regular expression
   for "breaking-down a well-formed URI reference into its components". So "a regex for a URL breaks" isn't true
   as a general rule (must-fix 1): https://www.rfc-editor.org/rfc/rfc3986.html
5. [S5] Python documentation, `urllib.parse`: "`urlsplit()` does not perform validation", and components "may contain
   more than perhaps they should". `netloc` is the raw authority, and `hostname` and `port` are the parsed parts.
   That's the bug in owner note 2: https://docs.python.org/3/library/urllib.parse.html
6. [S6] Databricks, "What is the medallion lakehouse architecture?": the bronze layer "contains and maintains the
   raw state of the data source", "is appended incrementally", and "enables reprocessing and auditing". Rule 2
   stands on a practice like this, and it's true of Scrapy's Delta tables:
   https://docs.databricks.com/aws/en/lakehouse/medallion
7. [S7] GitHub Docs, "Organizing information with collapsed sections": `<details>` is collapsed by default and holds
   detail not every reader wants. That's what the 15 more are, and why moving one line inside it costs nothing:
   https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections
8. [S8] Government Digital Service, "FAQs: why we don't have them": structure the content "so you won't need another
   page repeating the same information in a different way". Duplicates leave you "fighting with your own content"
   (must-fix 2): https://gds.blog.gov.uk/2013/07/25/faqs-why-we-dont-have-them/

Clones and data: `assets/stats.json` (`edition`, `repos[]` incl. `coauthored`, `rules[]`, `runcheck.rustmapper`);
sdist 0.1.3 `src/url_utils.rs:178-191`; Scrapy `96e7a1a` `Scraping_project/start.py:355, :379`,
`data/raw/uconn_urls.csv` (143,208 rows, 134,807 on uconn.edu), `src/stage2/stage2_worker.py:219, :923-934`,
`docker-compose.yml:13`; `Scrapy.git` `099dd6c` (author and trailers); ideal-url-organizer `159968a`
`src/core/web_crawler.py:296-311`, `src/core/url_parser.py`, `src/organizers/method_01_by_domain.py`,
`method_24_by_page_authority.py:79`, and `ideal-url-organizer.git` blame (`36cc345`, `6e8087f`, Claude, 9 Nov 2025);
`/home/user/excel-and-vba` `eabe846` (`src/modules/QueueModule.bas` 26 lines, `scripts/queue_sidecar.py` 55 lines);
`chart.toml:116-170, :272-388`; `tests/test_pipeline.py:296, :501`; `tests/test_round6.py:225, :307`.
