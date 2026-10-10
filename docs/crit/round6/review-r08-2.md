# Review round 8, reviewer 2: the developer choosing a crawler

10 Oct 2026. Reviewer: a developer who found this profile while looking for a sitemap crawler or a crawl platform,
and who has to decide whether to try rustmapper, Ben's Scrapy, or neither. Build looked at:
`scratchpad/r6/build/round-07/`. That is the desk sheet at 870 (day and night), the phone sheet at 390 and 308 (day
and night), the desk page (two screens), and the phone page at 390 (six screens) and 360 (six screens). Read:
`BRIEF.md`, `README.md`, `SPEC.md`, `LOG.md` (rounds 1 to 7) and the 21 earlier reviews. Round 3's review 3 had the
same lens as mine, and every one of its five must-fixes is now on the page (the license line says "This profile",
the pick sentence exists, the load and 50,000 clauses are under the install block, the Scrapy block runs in the
container). I don't repeat anything already fixed or already declined with a reason.

Every figure was checked against `assets/stats.json`, the 0.1.3 sdist (`scratchpad/r6/sdist013/rustmapper-0.1.3`),
the clones at the shas `stats.json` names (Rust-sitemap `32c2651`, Scrapy `96e7a1a`, ideal-url-organizer `159968a`)
and the full-history clones (`clones/*.git`).

**Verdict: 7 / 10. It does not meet the goal yet. I would not ship it as is.**

## The first question: does it meet the owner's goal?

Nearly. Taking the goal one test at a time, from where I sit:

- **Deep purpose for the map.** Yes. It is the only picture on the page, and it is the thing a shopper needs most:
  how the tool runs from install to output, in order, with the loop it repeats and the one place it bites. The loop
  bracket and the break in the track tell me "this runs until you stop it", and a list can't show that as fast.
- **It teaches something true and useful about his projects.** Useful, yes. True, all but one clause. The loop step
  says the crawler "fetches pages, fewer at once when saves average over 500 ms". The code has a governor with that
  threshold, but it can't do what the line says. It only takes back *idle* fetch slots, and it stops while 32 are
  still idle. On a crawl of one site, where one host never holds more than 20 slots, the number of fetches running
  never drops (finding 1). That is the one line in the image a shopper reads as "this tool is careful under load",
  and the code says it isn't. It fails the owner's standing rule: "honest data only".
- **Nothing chases a reason.** In the image, yes. Every mark answers a question I'd ask before running it.
- **Nothing announces the theme.** Yes. To me it reads as a clean strip diagram of a CLI. The magenta line, the end
  bars and the dotted line round the one danger do the work without a word about it.
- **Reads on a phone.** Yes. At 308 px the 26-unit text is about 13 px, the whole route fits in one screen, both
  code blocks fit at 360 px without scrolling sideways, and the link line is on screen 1.

So the form is done. Two things stop me shipping: one false clause in the image (finding 1), and one figure that
reads as an error two screens below it (finding 2). The other findings are what I need to *act* on the page's
honest warnings. They're short text, not more picture.

## What I'd conclude today, as the developer

Reading the image and the two rustmapper paragraphs, I'd take this away: pip installs it at once on an Apple-silicon
Mac and takes three minutes with a Rust toolchain anywhere else. By default it also asks certificate logs and Common
Crawl about my domain. It sends 20 requests at a time to one host with no pause, and 0.1.3 doesn't read robots.txt
on a plain-http site. It never exits by itself, so I watch for `Received work item` to stop, then press Ctrl-C once.
The output is a JSONL with real field names, and one sitemap.xml with no 50,000 split.

My verdict as a user: **fine for a one-off map of a site I own, while I watch it. Not for someone else's site, and
not unattended or in CI.** That's honest, and it's the answer to "should I try rustmapper". The image did its job.

For Scrapy: a four-stage Docker pipeline that keeps the pages, deduplicates and summarizes them, with Grafana. I'd
try it if I wanted the pages themselves, and I'd hit the `docker-compose` problem in finding 4 within a minute on
Linux.

Then I go looking for the next answers, and these are missing: how do I make rustmapper gentle (finding 3), and
will it see the links on a JavaScript site (finding 5).

## Findings

1. **The governor clause in the image claims an effect the code can't have.** In 0.1.3 the governor
   (`sdist:src/main.rs:84-150`) reads `permits.available_permits()` (`:108`). While the commit EWMA is over 500 ms
   it takes one permit with `try_acquire_owned()`, but only `if current_permits > MIN_PERMITS` (`:114-115`), with
   `MIN_PERMITS = 32` (`:92`). `available_permits` counts idle permits only. `try_acquire_owned` returns `NoPermits`
   when none are idle, and tokio has no way to take back a permit a task already holds [5]. So the governor removes
   idle capacity and stops while 32 slots are still idle. A running fetch keeps its permit (`bfs_crawler.rs:757`).
   That gives one invariant: the slots in use are never cut below what is running, and 32 more stay free. Each host
   is capped at `max_inflight: 20` (`state.rs:285`, checked at `frontier.rs:655`). So on a crawl of one site served
   from one host, the 20 fetches go on at full rate however slow redb gets. What the governor can do is stop
   *growth*: on a crawl that spreads to many subdomains while saves lag, concurrency can rise only about 32 above
   where it was. That is not "fetches pages, fewer at once". Main is the same shape, with a floor of 256 idle permits
   (`src/orchestration/governor.rs:29, :54`).
   The anchor engine passed this because F1's release anchors check that the comparison
   `if commit_ewma_ms > THROTTLE_THRESHOLD_MS` exists (`chart.toml:499`, marked `producer`). They don't check the
   guard that makes it a no-op for the job the header describes ("Crawls a site"). For me this is the line I'd have
   trusted most. "Slows itself when its store lags" is what I'd want to hear before pointing a 20-wide crawler at a
   site. Earlier rounds kept it as "the one design idea that's his and unusual" (r05-1, r06-1). Round 6's review 2
   noted the 32-idle guard in its unranked notes, but nobody set it against the 20-per-host cap. With that cap the
   guard means the clause is false for a single-host crawl, not just loose.

2. **The image says "sorted 21 ways by ideal-url-organizer"; the Also list says "25 ways to sort a pile of URLs".**
   Both are true. `self.methods` in `src/main.py` has 21 keys (that's what the importer's `--all` runs). There are 25
   `method_*.py` files, and the 4 extra ones (22 to 25) take `PageContent` from the organizer's own crawler. But the
   page never says so. On the desk page the two numbers are one screen apart. Two different counts for one small
   tool is exactly what makes a reader think "the data doesn't look exactly accurate" (owner) and stop trusting the
   other figures. Stanford's web credibility guidelines put it plainly: "Avoid errors of all types, no matter how
   small they seem" [10]. Round 7 fixed the image's number and left the text's on purpose (LOG round 7, r2-2). The
   fix is to make the text explain the gap, not to change either count.

3. **The page tells me rustmapper is hard on a site, and doesn't tell me the two flags that make it gentle.** L1
   says "up to 20 requests at a time to one host, 256 in all, with no pause". S1 says it consults certificate logs
   and Common Crawl by default. Both are fair warnings, and both have a lever in 0.1.3. `--workers N`
   (`sdist:src/cli.rs:29-35`) becomes `max_workers` (`main.rs:73`), and the crawl loop never runs more than that many
   tasks (`bfs_crawler.rs:283, :430`). So `--workers 2` means at most two requests at a time, whatever the host cap.
   `--seeding-strategy none` (`cli.rs:56-61`) turns off every seeder (`bfs_crawler.rs:188-196`), so the crawl
   starts from my URL and its links alone, and my domain goes to no outside service. The data line even says the
   run check used "seeding off", but the flag itself isn't printed anywhere on the page. Other crawlers put
   politeness on the command line where you can see it: katana's usage lists `-rate-limit` (default 150 per second),
   `-concurrency` (default 10), `-delay` and `-depth` (default 3) [6]. Google's own crawlers slow down on 429 and
   5xx [8]. A shopper who has just read "no pause" needs the next sentence to be "here is how to turn it down".
   Without it the honest warning reads as "don't use this".

4. **On Linux with Docker's own packages, the Scrapy quickstart fails before it starts.** `start.py` checks for the
   hyphenated command: `REQUIRED_TOOLS = {"local": ("docker", "docker-compose")}` (`Scraping_project/start.py:24-25`,
   `shutil.which` at `:242`), and it runs `docker-compose up -d` (`:345`). The block on the page then runs
   `docker-compose run --rm scraper …`. Compose V2, the current one, is a Docker CLI plugin called as
   `docker compose`, with a space. Docker Desktop aliases `docker-compose` to it by default [2]. Docker's Linux
   install leaves you with `docker compose` and verifies it that way [3]. GitHub's hosted runners removed the
   V1 `docker-compose` binary in July 2024 [4]. So on a fresh Ubuntu machine set up the way Docker documents,
   `python start.py` stops at preflight and the block's last command is "command not found". The page says "it needs
   docker and docker-compose", which is literally true, but a Linux user reads that as "Compose", which they have.
   Round 7's own Docker check ran `docker compose build` and `docker compose run` (LOG round 7, "The Scrapy block, in
   Docker"), so this was missed only because the check didn't use the page's spelling. The real fix is in Scrapy,
   one line. Until then the page has to say which command it means.

5. **Nothing says rustmapper reads only the HTML a server sends.** 0.1.3 parses with `scraper` and `html5ever`
   (`sdist:Cargo.toml:35-36`). There is no browser or JavaScript engine among its dependencies. Google describes its
   own crawl as fetch and parse HTML first, then render in headless Chromium later, and it finds links injected by
   JavaScript only after rendering [11]. A sitemap shopper with a single-page app gets a near-empty `sitemap.jsonl`
   from rustmapper and doesn't learn why from the page. The answer is already there, two screens down: go_go_go
   "adds headless-Chrome rendering … off by default". One clause in rustmapper's block joins the two. Lower rank:
   it's a scope fact, not a wrong one.

Smaller, no must-fix:

- Rust-sitemap still has no LICENSE file (`stats.json` `repos[Rust-sitemap].license` is null, LICENSE-FLAGSHIP
  warns). The Scrapy facts line ends "MIT license" and rustmapper's says nothing. A careful shopper notices the
  silence and reads it, correctly, as "not licensed". In the FSE 2020 study of how practitioners pick libraries,
  license came up among the most often in interviews, and 44 % of survey respondents rated active maintenance highly
  influential [1]. The fix is Ben's, and it's already on his list (round 3, review 3). I'd put it first among his
  outside actions: it is the one thing on this page that stops a company user cold.
- Scrapy framework users have `SitemapSpider`, which reads sitemaps, sitemap indexes and the sitemaps listed in
  robots.txt [7]. rustmapper's edge over that is the link crawl plus certificate-log and Common Crawl seeds. The
  pick sentence ("gives you a site's list of URLs from one binary, with no services to run") is still the right
  sentence. I'd keep it.
- "0.1.3 writes one `sitemap.xml` however many pages it found; the sitemap format allows 50,000 URLs per file" is
  right, and Google gives the same limit along with 50 MB uncompressed [9].

## Figures checked

| Printed | Key / source | Value | Holds |
|---|---|---|---|
| `pip install rustmapper` · 0.1.3 · 8 NOV 2025 | `edition.version`, `.date`, `.scripts`; runcheck `install` ok | 0.1.3, 2025-11-08, `["rust_sitemap"]` | yes |
| by default … sitemaps, subdomains in certificate logs, Common Crawl | `sdist:src/cli.rs:56-61` `default_value = "all"`; `bfs_crawler.rs:188-196` | | yes |
| fetches pages, fewer at once when saves average over 500 ms | `main.rs:90` `THROTTLE_THRESHOLD_MS: f64 = 500.0`; guard `:114` | the threshold exists; the effect doesn't on one host | **no** (finding 1) |
| queues their links to your site, its subdomains and its parent domain | `url_utils.rs:81-91` `is_same_domain` | both directions, dot boundary | yes |
| logged to disk, then saved to redb, in batches | `routes` W1 fallback; `writer_thread.rs` `drain_batch` | | yes |
| 0.1.3 never exits by itself; done when it stops printing `Received work item` | runcheck `ends_by_itself` false at 150 s; `quiet_after_last_page` ok; `bfs_crawler.rs:433` | | yes |
| press Ctrl-C once to write `data/sitemap.jsonl` | runcheck `crawl_ctrl_c` ok, exit 2.0 s after one SIGINT, 3 lines | | yes |
| fields: `url, depth, status_code, title, …` | `SitemapNode`, both trees; `handoffs[0].writer_fields_release` (15) | | yes |
| sorted 21 ways by ideal-url-organizer | `figures` row `self.methods` = 21 (ast, checked by me); `handoffs[0].state` `runs` | 21 | yes, but see finding 2 |
| Also: 25 ways to sort a pile of URLs | 25 `src/organizers/method_*.py`; 4 of them take `PageContent` | 25 | yes, conflicts with 21 unexplained (finding 2) |
| 32c2651 · 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust | `repos[Rust-sitemap]` `.head.short`, `.test_functions`, `.ci`, `.lines.Rust` | 32c2651, 176, success 2026-10-07, 16,390 | yes |
| 96e7a1a · 1,920 tests (CI selects all but 41) · CI passed 8 Oct 2026 · MIT · 69k lines | `repos[Scrapy]` | 96e7a1a, 1,920, `ci_selection.not_selected` 41, 2026-10-08, MIT, 69,036 | yes |
| Prebuilt for Apple silicon on CPython 3.13 | `edition.wheels` | `cp313-cp313-macosx_11_0_arm64` only | yes |
| 3 min, 4-core Linux x86_64, cold | runcheck `install` | median 171.4 s, 4 CPUs, cold | yes |
| 20 requests at a time to one host, 256 in all, no pause | `state.rs:281, :285`; `cli.rs:32`; `bfs_crawler.rs:283, :430`; probe `robots_read` (fetches 1 ms apart) | | yes |
| robots.txt only over https | `robots.rs:19` `format!("https://{}/robots.txt"…)`; probe `robots_read` false | | yes |
| 50,000 URLs per file | sitemaps.org; Google [9] | | yes |
| four stages | 4 `stage[0-9]/__init__.py` | | yes |
| 5 URLs fail, 60 s | `stage2_worker.py` `DEFAULT_STAGE2_BREAKER_FAILURES = 5`, `_RECOVERY = 60` | | yes |
| 50,000 characters, stage 4 | `config.py` `massive_doc_threshold=50000` | | yes |
| localhost:3000 | `docker-compose.yml` grafana `"3000:3000"`; `start.py:29` | | yes |
| 15 more repositories | `repo_count` 22 − profile − 2 − 4 | 15 | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | `repos[].all_hands` 146 / 499; `git log` in `Rust-sitemap.git` and `Scrapy.git`: 45 and 71 agent-authored; `repos[].coauthored.agent` 1 and 30 | | yes |
| Languages Python, Rust; Swift, JavaScript, TypeScript, C, Go | `repos[].main_language` (LOG round 7 count) | | yes |
| 10 Oct 2026, Linux x86_64, seeding off | `runcheck.rustmapper.date`, `.runner`, `crawl_ctrl_c.cmd` | | yes |

## Every element of the image

| Element | What I learn | Verdict | Why |
|---|---|---|---|
| "Ben Russell" | whose page | keep | the first fact, largest type |
| Role line "CRAWL AND DATA INFRASTRUCTURE / PYTHON AND RUST" | what he builds | keep | the drawing below proves it |
| Empty desk column under the role | nothing | keep | quiet paper keeps the route the one dense block |
| "rustmapper" serif header | which tool | keep | |
| "Crawls a site and writes one line for every URL it finds." | it gives me a URL list, not page content | keep | the line that tells me it isn't a scraper, and the pick sentence leans on it |
| Start bar | where to begin | keep | |
| `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | how to get it, and that the only release is 11 months old | keep | the age I judge maintenance by, set against main's CI date in the text |
| Track, magenta | one way through, top to bottom | keep | |
| S1 "your URL and, by default, URLs looked up rather than followed: …" | by default it asks crt.sh and Common Crawl about my domain | keep | the row I most need before running it on a private host. Finding 3 gives it its off switch in the text |
| F1 "fetches pages, fewer at once when saves average over 500 ms; queues their links …" | that it fetches in a loop, how far its scope reaches, and (wrongly) that it slows under load | **change** | the scope clause is true and useful. The governor clause is false for a one-host crawl (finding 1). Say the per-host 20 instead, which is the figure that governs a site crawl (must-fix 1) |
| W1 "logged to disk, then saved to redb, in batches" | a write-ahead log sits under the store, so a kill doesn't lose the crawl | keep | "in batches" is weak for me, but it is the true wording left after round 7, and the step itself earns its row |
| Loop bracket + up arrow | which steps repeat for every page | keep | the mark a list can't replace |
| H1 dotted box "0.1.3 never exits by itself; done when it stops printing `Received work item`" | the catch, and how to tell when I'm done | keep | the most decision-relevant line in the image: it's why I won't run this in CI |
| Break in the track below the loop | the loop doesn't end by itself; I end it | keep | shows the H1 fact without another word |
| C1 "press Ctrl-C once to write `data/sitemap.jsonl`" | the one thing I do | keep | |
| End bar | where I end up | keep | |
| `data/sitemap.jsonl` + fields | what I get, with the struct's field names | keep | lets me judge whether it feeds my pipeline before installing. The repeated file name is the action, then the result (r07-2 kept it, and I agree) |
| Thin line, arrowhead, "sorted 21 ways by ideal-url-organizer" | his tools connect, and the format is stable enough that another tool depends on it | keep | the number must agree with the text (must-fix 2) |
| Night editions | the same | keep | contrast holds in both |
| Phone editions (390, 308) | the same, stacked | keep | the route is one screen at 308 px |

Nothing to cut, nothing to add to the picture. Findings 3 to 5 are lookups, and lookups go in text (SPEC §0).

## Every block of the page

| Block | What I learn | Verdict | Why |
|---|---|---|---|
| Image | how rustmapper runs and where it bites | change | F1's governor clause (must-fix 1) |
| Alt text | the same in 25 words | keep | "It loops until one Ctrl-C writes data/sitemap.jsonl" is the whole verdict in one sentence |
| Link line | where to go | keep | |
| Builds / Languages / Stack | who he is | keep | |
| Pick sentence | which tool for which job | keep | the sentence I asked for in round 3, and it's right |
| rustmapper about line | pip gives a CLI; the Python API is unreleased | keep | saves me looking for an `import rustmapper` that 0.1.3 doesn't have |
| rustmapper facts line | alive, tested, size | keep | the license gap is Ben's to fix (smaller items) |
| rustmapper install block | the commands, and Ctrl-C once | keep | 32 columns, fits at 360 |
| Wheel note | when pip just works | keep | the 3-minute figure is measured |
| L1 + X1 load and sitemap paragraph | how hard it hits a site; the 50,000 limit | change | add the two flags that answer it (must-fix 3); drop the per-host clause if F1 now carries it (must-fix 1); add the HTML-only clause (must-fix 5) |
| Scrapy lead | his system, not the framework, four stages | keep | |
| Scrapy facts line | alive, tested, licensed | keep | |
| Scrapy run sentence | where to run it, what it needs, what it crawls | change | name the hyphenated command and where it exists (must-fix 4) |
| Scrapy block | the commands | keep | runs in the container. The spelling is fixed in the sentence above it and by Ben in `start.py` |
| Grafana / spiders by name | where to look, and a trap | keep | |
| Scrapy bullets | how it's built | keep | the breaker and summaries are what tell me it's the stateful, careful one |
| Also | the next four | change | ideal-url-organizer line explains 25 vs 21 (must-fix 2). go_go_go's headless Chrome is the answer to finding 5 |
| 15 more | the rest | keep | |
| Working rules | how he works | keep | each one cites a file I can open; rule 1 matches the Scrapy bullet |
| Found a mistake? | the page can be corrected | keep | |
| Data line | what was run and who wrote the code | keep | |
| License line | the profile's terms | keep | "This profile" fixed round 3's confusion |

## Must fix, ranked

1. **F1 says the per-host cap, not the governor** (`chart.toml [route.rustmapper]` F1 at `:484-501`, L1 at `:604`;
   `sheets/route.py` PURPOSE and BREAKS rows for F1; `docs/data/AUDIT.md` routes row; `DESIGN.md`; one fixture test;
   about 30 lines, no height change).
   - F1 text: "fetches up to {field:max_inflight} pages at a time from each host; queues their links to your site,
     its subdomains and its parent domain". Release anchors: the four scope anchors kept, plus
     `{path = "src/state.rs", field = "max_inflight"}` (L1 already reads it) and
     `{path = "src/frontier.rs", text = "current_inflight >= host_state.max_inflight"}`. Drop the three
     `main.rs` governor anchors from this wording. Desk stays two lines; phone stays four.
   - Keep the governor wording as a first alternative, gated on a new `absent` anchor:
     `{path = "src/main.rs", fn = "governor_task", absent = "current_permits > MIN_PERMITS"}`. That way the
     governor comes back by itself on a release whose throttle can cut running fetches, for example one that
     tracks total permits and uses `forget_permits`. Today the alternative fails, so the per-host wording draws.
   - L1 then starts "It sends them with no pause, {arg:workers} at most in all." so the image and the text don't
     both say 20. The rest of L1 is unchanged.
   - Test: a fixture `main.rs` with the guard present gives the per-host wording. With the guard removed it gives
     the governor wording.
   - Why: "honest data only". It is the image's only clause about the tool's behaviour under load, and for a one-site
     crawl it says the opposite of what happens (finding 1). The per-host 20 is the figure that does govern the
     crawl the header describes, at the step where it applies.
   - Owner note, in Rust-sitemap: the governor removes idle permits only (`main.rs:114`; main `governor.rs:54`
     with a 256 floor), so it can't slow a crawl. That's an issue for his tracker, not for this page.

2. **The Also line explains 25 against the image's 21** (`README.md` Also list, hand-typed; `chart.toml [[figures]]`
   one new row; about 10 lines with the FIGURES test).
   - Text: "**ideal-url-organizer** — 25 ways to sort a pile of URLs: 21 from the URLs and crawl data alone (by
     domain, crawl depth, subdomain, …), 4 more from pages it fetches itself." That's 3 lines on a 390 phone, one
     more than today.
   - New `[[figures]]` row `text = "4 more"`, `repo = "ideal-url-organizer"`, `glob = "src/organizers/method_*.py"`,
     counting files that contain `List[PageContent]` (= 4). The "21" in the line reads the existing `handoff = true`
     row.
   - New fast check HANDOFF-AGREES: every count printed beside "ideal-url-organizer" on the page or the image comes
     from one of those rows.
   - Why: two unexplained counts for one tool on one screen read as an error, and they cost the trust every other
     verified figure on the page has earned (finding 2, [10]).

3. **One sentence after L1 with the two flags that turn it down** (`chart.toml` a new text entry `T1`, scope
   `release`, rendered after L1 by `render_readme.text_entries`; a run-check probe; about 40 lines).
   - Text: "`--workers 2` holds it to two requests at a time; `--seeding-strategy none` starts from your URL and its
     links alone and asks no outside service about your domain."
   - Release anchors: `cli.rs` `workers: usize` with `default_value = "256"`; `main.rs`
     `max_workers: u32::try_from(workers)`; `bfs_crawler.rs` `let max_concurrent = self.config.max_workers` and
     `in_flight_tasks.len() < max_concurrent`; `bfs_crawler.rs` `strategies.contains(&"all")` and the three
     `enable_*` lines.
   - New probe `workers_cap` in `scripts/runcheck.py`. Crawl the fixture with `--workers 1 --seeding-strategy none`,
     and pass if the fixture server's log never shows two requests open at once. The `robots_read` probe already
     logs request times. If the probe fails, the sentence is not printed. The "2" in the sentence is the flag's
     argument, so AUDIT-COVER needs one row saying so.
   - Phone: about 4 lines.
   - Why: the page warns me that the tool is hard on a site and talks to third parties by default. Without the
     levers, the honest warning reads as "don't use this", and both levers are in the release (finding 3).

4. **Say which Compose the Scrapy quickstart needs** (`README.md` Scrapy run sentence, or its `chart.toml` source;
   one `[[figures]]`-style anchor; about 10 lines).
   - Change "it needs docker and docker-compose" to "it needs Docker and the `docker-compose` command, which Docker
     Desktop provides; on Linux, where Docker's Compose plugin answers only to `docker compose`, add a
     `docker-compose` alias first." That's 2 more lines on a phone.
   - Anchor: `Scraping_project/start.py` contains `"docker-compose")` in `REQUIRED_TOOLS`. When the anchor stops
     holding, the sentence drops to "it needs Docker and Docker Compose".
   - Owner action, in Scrapy: have `start.py` accept `docker compose` (try the plugin, then the hyphenated name),
     and print `docker compose` in the block once it does.
   - Why: on a fresh Linux machine set up the way Docker documents, the quickstart stops at preflight and the last
     command is "not found" (finding 4, [2], [3], [4]).

5. **One clause on what rustmapper can't see** (rustmapper `about` block or after L1; release anchor `Cargo.toml`
   absent `chromiumoxide`, `headless_chrome`, `fantoccini`, with `scraper` present; about 10 lines).
   - Text: "It reads links from the HTML a server sends; no JavaScript runs. go_go_go can render pages in headless
     Chrome." That's 2 lines on a phone.
   - Why: on a JavaScript-built site, a sitemap shopper otherwise gets a near-empty file with no explanation, and
     the page already has the alternative two screens down (finding 5, [11]).

## Owner actions outside this repository (not must-fixes here)

Ranked for a shopper. (1) Commit the MIT `LICENSE` that `pyproject.toml` already names, so 0.1.4's sdist ships it.
(2) `start.py`: accept `docker compose`. (3) Make the governor able to cut running fetches, or say in Rust-sitemap's
README what it does. (4) The ones already on his list: P1, the idle test without `--ignore-robots`, 0.1.4, wheels
beyond macOS arm64, the About text.

## Sources (new this round)

1. Larios Vargas, Aniche, Treude, Bruntink, Gousios, "Selecting Third-Party Libraries: The Practitioners'
   Perspective", ESEC/FSE 2020, pp. 245-256 (16 interviews, 115 survey answers). License among the most raised
   factors, and 44 % rate active maintenance highly influential; "If a project is not active for one year, I would
   think that is a dead project". https://ar5iv.labs.arxiv.org/html/2005.12574 (smaller items: license and release
   age are what a shopper checks)
2. Docker blog, "Announcing Compose V2 General Availability": V2 is called by "replacing the hyphen with a space";
   "On Docker Desktop version 4.4.2+, we enable aliasing of `docker-compose` syntax to `docker compose` by default".
   https://www.docker.com/blog/announcing-compose-v2-general-availability/ (finding 4, must-fix 4)
3. Docker Docs, "Install the Docker Compose plugin" (Linux): both install routes verify with `docker compose
   version`. https://docs.docker.com/compose/install/linux/ (finding 4)
4. actions/runner-images issue #9692: Compose v1 deprecated since July 2023, its binary removed from the hosted
   Ubuntu and Windows images on 29 July 2024; a maintainer confirmed in Feb 2026 it was not put back.
   https://github.com/actions/runner-images/issues/9692 (finding 4: `docker-compose` is absent on a stock Linux CI
   runner too)
5. tokio docs, `Semaphore::try_acquire_owned`: returns "TryAcquireError::NoPermits if there are no permits left".
   Permits return only when a holder drops them; `forget_permits` shrinks the pool but not held permits.
   https://docs.rs/tokio/latest/tokio/sync/struct.Semaphore.html (finding 1: the governor can't take a running
   fetch's permit)
6. ProjectDiscovery katana, README usage: `-concurrency` default 10, `-rate-limit` default 150 per second,
   `-delay`, `-depth` default 3, `-crawl-duration`. https://github.com/projectdiscovery/katana (finding 3: what a
   shopper expects to find on the command line)
7. Scrapy docs, Spiders, `SitemapSpider`: reads `sitemap_urls`, "supports nested sitemaps and discovering sitemap
   urls from robots.txt". https://docs.scrapy.org/en/latest/topics/spiders.html (smaller items: the pick sentence
   against the framework's own sitemap tool)
8. Google Search Central, "How HTTP status codes, and network and DNS errors affect Google Search": "`5xx` and `429`
   server errors prompt Google's crawlers to temporarily slow down".
   https://developers.google.com/search/docs/crawling-indexing/http-network-errors (finding 3: the yardstick for
   "no pause")
9. Google Search Central, "Build and submit a sitemap": "50MB (uncompressed) or 50,000 URLs" per file, then split and
   optionally index. https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap (X1 holds)
10. Stanford Web Credibility Project, guidelines 1 and 10: "Make it easy to verify the accuracy of the information
    on your site"; "Avoid errors of all types, no matter how small they seem".
    https://credibility.stanford.edu/guidelines/index.html (finding 2)
11. Google Search Central, "Understand JavaScript SEO basics": crawl parses the HTML response for links; later "a
    headless Chromium renders the page and executes the JavaScript", and "Googlebot parses the rendered HTML for
    links again". https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
    (finding 5)
12. Code, read for this review: sdist 0.1.3 `src/main.rs:73, 84-150` (governor; `:92` `MIN_PERMITS = 32`, `:108`,
    `:114-115`), `src/bfs_crawler.rs:188-196, 283, 430, 433, 757`, `src/state.rs:281, 285`, `src/frontier.rs:655`,
    `src/cli.rs:1-160`, `src/robots.rs:18-25`, `src/url_utils.rs:81-91`, `Cargo.toml:27-60`; Rust-sitemap `32c2651`
    `src/orchestration/governor.rs:16-34, 48-60`, `src/state.rs:442`; ideal-url-organizer `159968a` `src/main.py`
    (`self.methods`, 21 keys by ast), `src/organizers/method_22`-`25` (`List[PageContent]`); Scrapy `96e7a1a`
    `Scraping_project/start.py:24-29, 242, 312, 345`, `docker-compose.yml` (`scraper` service); `clones/Rust-sitemap.git`
    and `clones/Scrapy.git` (146 / 45 and 499 / 71).
