# Review round 14, reviewer 2: the staff engineer screening for data infrastructure

10 Oct 2026. I screen GitHub profiles for data-infrastructure hires: first on a phone between other things, then on
a laptop for the ones that make the cut. I looked at every PNG in `scratchpad/r6/build/round-13/`: the sheet on desk
at 870 (day, night), mid at 746 (day, night), phone at 390 and 308 (day, night), the desk page (two screens), the
phone page at 390 (six screens) and at 360 (seven), and the 900 and 1,180 pages. I read `README.md`, `SPEC.md`, the
round 13 log and the reviews from rounds 1 to 13, including the two earlier screener reviews (r05-2, r09-3). I don't
repeat anything already fixed. Every figure was checked against `assets/stats.json`, the clones, the 0.1.3 sdist and,
for two commits, the GitHub API.

Verdict: **not yet. 8 / 10.** I would ship the image as it is, once 0.1.4 passes the run check. The page is not ready.
Last round added a sentence that says his Scrapy repository "obeys `robots.txt` and its `Crawl-delay`". The code
says that holds for stage 1 only: stage 2 then fetches every link stage 1 found, disallowed ones included, under
aiohttp's default user agent. That's a false politeness claim, on a profile whose whole case is that he builds
careful crawlers. It has to go first. Two smaller changes would help a screener a lot. The agent-authorship figures
should sit next to the test and line counts they qualify. And the best operations evidence in Scrapy (its alerts, a
kill switch, a runbook) should replace a bullet that only says "dashboards".

## The first question: does it meet the owner's goal?

- **A deep purpose for the map.** Yes. The image is directions through one tool: what you install, where its URLs
  come from, the loop each page goes through, the one fault, how you stop it, the file you get, and who reads that
  file next. The bracket and the gap in the track show the loop and the missing exit, and a list can't. Nothing has a
  size, so the owner's question "is it based on the size of the project or how many commits?" has nothing to bite on.
- **True and useful about his projects.** In the image, yes: every row holds against the sdist and the run check
  (table below). On the page, one sentence is false (must-fix 1).
- **Nothing chases a reason.** In the image, nothing does. On the page, Scrapy's third bullet ("Prometheus metrics on
  Grafana dashboards") fills a slot with the weakest true thing it could say. The repository has much stronger
  evidence (must-fix 3).
- **Nothing announces the theme.** True. The magenta line, the dotted danger box and the terse rows carry it, and no
  word names it.
- **Reads on a phone.** The image fits on one 390 screen and at 308. On the page, the Scrapy evidence a screener
  wants begins at the bottom of phone screen 3, a screen sooner than in round 9. The agent-authorship figures are on
  screen 6, five screens from the counts they qualify (must-fix 2).

## Figures checked (independently this round)

| Printed | Source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.date` | 0.1.3, 2025-11-08 | yes |
| `rust_sitemap crawl` | `edition.scripts` | `["rust_sitemap"]` | yes |
| up to 20 pages at a time from each host | sdist `state.rs:285` `max_inflight: 20`; `frontier.rs:655` | 20 | yes. The field's comment at `:240` says "default: 2", which is stale; the value used is 20 |
| your site, its subdomains and its parent domain | sdist `url_utils.rs:81-91`, both branches | | yes |
| saved as it goes; export works after a kill | runcheck `export_after_kill` 3 `<loc>`; `kill_writes_file` false | | yes, and it claims no more than that |
| never exits by itself; `Received work item` for 60 s | runcheck `ends_by_itself` false at 150 s; `quiet_slow_page` ok; sdist `bfs_crawler.rs:433` | | yes |
| second press before the `Saved to` line | runcheck `second_ctrl_c`: exit 1, no file; sdist `main.rs:519, :539` | | yes |
| fields `url, depth, status_code, title` | `handoffs[0].writer_fields_*` | | yes |
| sorted 21 ways | `figures` "21 ways", measured 21 | | yes |
| 176 test functions · 16k lines of Rust | clone at `32c2651`: 161 Rust attributes + 15 Python; 16,390 lines | 176; 16,390 | yes |
| CI passed 7 Oct 2026: tests, rustfmt | `repos[Rust-sitemap].ci`, `gates` | success, 2026-10-07 | yes |
| 1,920 (CI selects all but 41) · 8 Oct · MIT · 69k | `repos[Scrapy]` | 1,920; 41; MIT; 69,036 | yes |
| 256 at a time; `--workers 1` | sdist `cli.rs:191`; runcheck `workers_cap` | | yes |
| 143,208 / 134,807 on uconn.edu | `figures` CSV rows | | yes |
| 5 URLs in a row; 60 s (rule 1) | `figures`; commit `099dd6c`, his, 8 Oct 2026 | | yes. The breaker landed two days before this build |
| 6 days, then 5 (rule 3) | `rules`: repo first 2025-09-25, prometheus 10-01, grafana 10-06 | | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | `repos[].commits` 101 and 420, `others` (Claude 45; jules 49, Claude 22, dependabot 8), `coauthored.agent` 1 and 30 | | yes |
| 15 more | 22 − profile − 2 flagships − 4 Also | 15 | yes |
| **It obeys `robots.txt` and its `Crawl-delay`** (pick) | Scrapy `96e7a1a`, see must-fix 1 | | **stage 1 only** |
| **crawls your site as `<your-bot>`** (Scrapy run sentence) | same | | **stage 1 only** |

## Every element of the image

| Element | What a screener learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell" | whose work this is | keep | the first thing read, at every width |
| Role line, two caps lines | crawl and data infrastructure; Python and Rust | keep | the image proves "crawl". The text has to prove "data infrastructure", and must-fix 3 helps it do that |
| Empty left column under the role (desk) | nothing, on purpose | keep | the route reads first |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which tool, what it gives you | keep | |
| Start bar + `pip install rustmapper` + 0.1.3 · 8 NOV 2025 | the way in; the release is 11 months old | keep | an honest age. The fix is a release |
| Magenta track | one way through, top to bottom | keep | |
| Stop rings | one step each | keep | |
| S1 `rust_sitemap crawl` … sitemaps, certificate logs and Common Crawl | the command that really runs, and that URLs come from more than links by default | keep | the seeding sources are a design choice a crawl engineer recognises |
| F1 20 per host; scope | concurrency is capped per host; what's in scope | keep | the per-host cap is the first politeness fact I check |
| Loop bracket + arrow | which rows repeat for each page | keep | only a drawing shows it |
| W1 "saved as it goes; export works after a kill" | a kill doesn't lose the pages for the export | keep | it's weaker data-infra signal than the old WAL wording. But the facts line names redb and rkyv, and the row now claims only what the run check proves |
| Gap under the loop | no exit but Ctrl-C | keep | |
| H1 red dotted box | the known fault in 0.1.3, and how to tell you're done | keep while 0.1.3 is current | it's the loudest mark, and it's a defect. A defect stated with its workaround is a maturity signal. It retires itself with 0.1.4 |
| C1 Ctrl-C once | the one action, and what a second press costs | keep | |
| End bar + `data/sitemap.jsonl` + fields | the output contract, in the struct's names | keep | a data engineer reads this row first |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | his tools fit together, and the join is tested | keep | |
| Night editions | the same | keep | |
| Mid edition (746) | the same, stacked, at laptop widths under 1,200 | keep | |
| Phone editions (390, 308) | the same on one screen | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Picture + alt | above | keep | |
| Link line | where to go | keep | no LinkedIn or résumé (see owner note 2) |
| Builds / Languages / Stack | what he builds with | keep | the Stack line is my keyword pass |
| Pick sentence | which tool for which job | **change** | the politeness clause is true of stage 1 only (must-fix 1) |
| rustmapper facts line | which commit, tests, CI gates, size | **change** | the agent share belongs here (must-fix 2) |
| Wheel note | will pip just work | keep | |
| "Before you run 0.1.3:" (4 open items) | what it does to someone else's server, and the lever for each | keep | |
| Fold "What 0.1.3's files miss or get wrong" | what's in the file afterwards | keep | |
| rustmapper code block | how to run, stop and export | keep | |
| Scrapy sentence | the second tool, and what it is | keep | |
| Scrapy facts line | which commit, tests, CI gates, licence, size | **change** | must-fix 2 |
| Scrapy bullet 1 (Delta raw layer) | storage design | keep | the strongest data-infra line on the page |
| Scrapy bullet 2 (dedup, summaries) | processing design | keep | |
| Scrapy bullet 3 (Prometheus on Grafana; Compose, Helm) | that it's observable and deployable | **change** | the alerts, kill switch and runbook are stronger, and true (must-fix 3) |
| Scrapy run sentence | where to run it, what it needs, who it says it is | **change** | the user-agent sentence covers stage 1 only (must-fix 1) |
| Scrapy code block | how to start it | keep | |
| Arrival sentence (Grafana, `data/delta/`) | where the output lands | keep | |
| Also (4 lines) | four more tools, by what they do | keep | |
| 15 more | the rest | keep | |
| Working rules 1–3 | how he works, each with a dated cite | keep | rule 3 is the one I'd quote in a debrief |
| Found a mistake? | the page can be corrected | keep | |
| Data line | what was run; who wrote the code | **change** | it keeps the definitions; the counts move up (must-fix 2) |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **Say what Scrapy's politeness covers: stage 1, not the pipeline.** (`chart.toml [copy] pick_polite`; the
   hand-typed Scrapy run sentence in `README.md`, about line 83; three new `[[figures]]` rows; one test. About 15 lines.
   It adds about 2 phone lines at 390.)
   - **What's wrong.** The scout yields two things for every in-scope link it finds
     (`Scraping_project/src/stage1/scout_spider.py:162`, `:179`). One is a `scrapy.Request`, which
     `PoliteRobotsTxtMiddleware` (`spider_config.py:100`) filters. The other is a plain dict with `target_stage =
     "stage2"`. `QueueItemPipeline.process_item` (`src/pipelines.py:748-771`) writes that dict to `stage2_queue`, and
     the only thing it checks is SSRF. The stage 2 worker, which `python start.py` starts (`docker-compose.yml:117`),
     then GETs each URL with aiohttp (`stage2_worker.py:668`, `:817`).
     - There is no robots.txt check anywhere in `src/stage2/`, `src/workers/` or `src/utils/`, and no `Crawl-delay`.
     - Non-HTML links (PDFs, documents) go to stage 2 without ever passing through a `Request` (`:179`).
     - Stage 2's `ClientSession` sets no headers (`_new_session`, `:394-403`), so its requests carry aiohttp's default
       user agent, not `<your-bot>`. Stage 4 hard-codes `MyScraper/1.0 (Educational Research Bot)`
       (`stage4/large_doc_processor.py:86`).
     - So on a site whose robots.txt disallows `/private/`, a page linking to `/private/a.html` gets that URL fetched
       by stage 2, under a name the site owner never saw.
     - Stage 2 does wait out `Retry-After` (`:827`, `:914-920`) and caps each host at 4 in flight (`:116-140`). Those
       parts of the claim hold.
   - **Why it ranks first.** It's a false sentence on the profile, about the one property a crawler's reputation rests
     on. It also sits right after a list that faults rustmapper for ignoring `Crawl-delay`. A site owner who sees
     disallowed paths fetched by a "Python aiohttp" agent can't block it by name. Google's own guidance assumes a site
     can identify a crawler and slow it with 429 or 503 [S7]. A screener who opens `stage2_worker.py` (the file rule
     1 cites) finds this in a few minutes, and from then on doubts every other sentence.
   - **Build:**
     - `pick_polite`: "Its discovery spider obeys `robots.txt` and its `Crawl-delay`, and waits out a
       `Retry-After`." Its three rows stay as they are, since all three are stage 1 facts.
     - Scrapy run sentence: after "…its requests say `UConn-Discovery-Crawler/1.0`." add "Stage 2 then fetches every
       link the crawl found, ones `robots.txt` disallows included, without that name." (21 words; FLAG-WRAP has no
       flag to break.)
     - New `[[figures]]` rows for that sentence:
       - `scout_spider.py`, literal `yield self._queue_for_stage2(url, response.url, content_hint)`, count 2;
       - `stage2_worker.py`, `absent` regex `(?i)robots`;
       - `stage2_worker.py`, `absent` regex `User-Agent`;
       - `pipelines.py`, literal `elif target_stage == "stage2":`.
     - When the owner adds a robots check or a user agent to stage 2, a row fails, FIGURES goes red, and the sentence
       is reworded, which is the same rule as every other typed figure.
   - **Test** (`tests/test_round14.py`): with the stage 2 fixture containing `RobotFileParser` or `robots`, the row
     fails. `pick_polite` doesn't start with "It obeys" while the stage 2 `absent` rows hold.
   - Owner, in Scrapy: have stage 2 consult the same robots cache (Protego, as Scrapy uses), honour `Crawl-delay`, and
     send `USER_AGENT` from config in stage 2 and stage 4. Then the original clause is true and can come back.

2. **Put the agent counts next to the counts they qualify.** (`scripts/render_readme.py` `facts_block`; the
   `survey` block; AUDIT §5 row for `others`; `README-STALE`; one test. About 25 lines. +1 phone line per facts line,
   −2 lines from the data line.)
   - **What's wrong.** "176 test functions … 16k lines of Rust" is on screen 2. "Tests and lines are counted per
     repository, whoever wrote them: coding agents … authored 45 of rustmapper's 146 commits" is in `<sub>` at the
     foot of screen 6. The disclosure is honest, but it's five screens from the figure it qualifies. Most screeners
     never reach it, and the ones who do will have formed a view of the 176 tests without it.
   - **Why it matters now.** 76 % of 1,000 US hiring managers say AI makes it harder to judge whether a candidate's
     work is their own, and 35 % have already met AI-made portfolio projects [S3]. Developers' distrust of AI output
     rose to 46 % in 2025 [S4]. Every profile I screen this year raises the question. The best-supported finding on
     disclosure is that saying you used AI costs some trust, and having someone else find it costs more [S1]. Ben
     already pays the first cost. Placed where it is, he still risks the second, because a screener who reads the
     commit log before the foot of the page "finds" what he disclosed. Things placed near each other are read as one
     group [S8], and this caveat belongs with the counts.
   - **Build:**
     - Facts lines gain one clause, from `repos[].others` with `bot: true` less `AUTOMATION`, over all commits on the
       default branch: rustmapper "· coding agents authored 45 of its 146 commits"; Scrapy "· coding agents authored
       71 of its 499 commits".
     - The data line becomes: "The drawing shows rustmapper 0.1.3 … (Linux x86_64). Tests and lines are counted per
       repository, whoever wrote them; agents also co-signed 1 and 30 of his own commits." The rule in AUDIT §5
       (print `coauthored.agent` only beside `agent_authored`) still holds: the two now sit in the same section of
       the page, each linked to `#data`.
   - **Test:** the two clauses equal the computed counts. A fixture with no agent commits prints no clause, not
     "0 of".

3. **Scrapy's third bullet: say how it is run in production, not only that it has dashboards.** (Hand-typed bullet
   in `README.md`, about line 79; six `[[figures]]` rows; about 12 lines. It grows by about 2 phone lines at 390.)
   - **What's there.**
     - `monitoring/alerting_rules.yml` holds 42 alert rules, loaded by `monitoring/prometheus.yml:26-28` and mounted in
       `docker-compose.yml:235-236`. They are on metrics the code really emits: `DeltaWriteFailuresSustained` on
       `delta_write_failures_total` (`lakehouse_manager.py:73`), and `Stage2StarvedWhileStage1Active` on
       `stage2_queue_empty` (`stage2_worker.py:67`). Each fires on a symptom and says what is broken.
     - A global kill switch (`src/utils/crawl_guard.py`, his commit `88340c0`, 8 Oct 2026) "stops new downloads
       within" `kill_switch_check_secs`, default 5 s (`:271`), with daily request and byte budgets, an audit log, a
       CLI (`cli.py:569` `cmd_killswitch`), 15 tests (`tests/…/test_crawl_guard_kill_switch.py`) and a SEV1 runbook
       (`docs/runbooks/sev1_abuse_kill_switch.md`).
   - **Why.** For a data-infrastructure hire this is the strongest evidence in the repository. Google's SRE guidance
     is that "every page should be actionable" and that monitoring should catch symptoms, "what's broken", ahead of
     causes [S6]. Recording the response ahead of time "produces roughly a 3x improvement in MTTR" [S5]. "Prometheus
     metrics on Grafana dashboards" says none of that. The kill switch also answers what a site owner needs most from
     a crawler: a way to stop it fast [S7].
   - **New bullet:** "Prometheus alerts on its own metrics, such as Delta writes spilling to disk, and Grafana
     dashboards. A kill switch stops new downloads within 5 s, with a runbook. Docker Compose and a Helm chart for
     Kubernetes."
   - **Rows:**
     - `alerting_rules.yml` literal `alert: DeltaWriteFailuresSustained`, with `lakehouse_manager.py` literal
       `"delta_write_failures_total"` in `also`;
     - `prometheus.yml` literal `/etc/prometheus/alerting_rules.yml`;
     - `crawl_guard.py` literal `opt("kill_switch_check_secs", 5.0)`;
     - `cli.py` literal `def cmd_killswitch`;
     - the runbook path exists;
     - the test file exists.
   - **No count of alerts is printed.** Verifying all 42 against emitted metrics is more than one row can hold, and
     the comment at `alerting_rules.yml:650` records an earlier set that "used names nothing emitted".

## Owner, outside this repository (new this round; not ranked; the carried items stand)

1. **Scrapy stage 2 and stage 4: robots.txt, `Crawl-delay` and one user agent** (must-fix 1). This is the most
   important code change on either flagship. It costs less than the rustmapper P1 fix, and it would make the original
   pick clause true.
2. **Fill `[position]` and `[contact]` in `chart.toml`.** Both are empty (POSITION-EMPTY warns every build). After "is
   this person good?", the first thing I need is "are they looking, for what, and where?", then a résumé or LinkedIn
   to forward. GitHub describes the profile README as the place to "tell other people about yourself" [S9]. The build
   already prints both slots. Only Ben can supply the words, so nothing here can invent them.
3. **One measured crawl at scale.** Scrapy's README says its throughput figures "are design targets … not measured
   benchmarks" (`README.md:653-654`), and rustmapper's 1,060 URLs/min is a code comment (`state.rs:285`). A dated,
   permitted crawl of a site he controls, with pages, bytes, elapsed time and error share committed as a file, would
   let the page print one figure a data-infrastructure screener asks about first. SPEC §4 block 7 already reserves
   the slot.
4. **Fix the stale comment** `state.rs:240` "(default: 2)": the value is 20.
5. Carried: P1 and 0.1.4 (the red box and the gap retire), `response.url()` as the link base, `resume` after a kill,
   a LICENSE, pin Rust-sitemap and Scrapy, the GitHub bio, a real-device check.

## Sources (new this round)

Web searches ran out partway through this round (the session's search budget was spent). The rest were fetched
directly.

1. [S1] University of Arizona News on Schilke and Reimann, "The transparency dilemma: How AI disclosure erodes trust",
   *OBHDP* 188 (2025): "13 experiments involving more than 5,000 participants". Disclosure lowers trust, and quiet use
   "can trigger the steepest decline in trust if others uncover it later":
   https://news.arizona.edu/employee-news/being-honest-about-using-ai-work-makes-people-trust-you-less-research-finds
   (paper listing: https://ideas.repec.org/a/eee/jobhdp/v188y2025ics0749597825000172.html)
2. [S2] GitHub, Octoverse 2025: 518.7M pull requests merged (+29 %), and 80 % of new developers use Copilot in their
   first week. It's the base rate that makes agent authorship a routine screening question:
   https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
3. [S3] Resume Genius, survey of 1,000 US hiring managers (Jan–Feb 2025): "35% of hiring managers have come across
   AI-created portfolio projects", "76% believe AI makes it harder to assess whether candidates are authentic":
   https://resumegenius.com/blog/job-hunting/ai-impact-on-hiring
4. [S4] Stack Overflow Developer Survey 2025, as reported by TechRepublic: 46 % of developers distrust the accuracy of
   AI output (31 % in 2024), and 84 % use or plan to use AI tools:
   https://www.techrepublic.com/article/news-developer-trust-in-ai-declines/
5. [S5] O'Reilly, "Tenets of SRE" (from Google's SRE book): recording best practices ahead of time in a playbook
   "produces roughly a 3x improvement in MTTR"; "humans should be notified only when they need to take action":
   https://oreilly.com/ideas/tenets-of-sre
6. [S6] Google SRE book, "Monitoring Distributed Systems": "Every page should be actionable"; monitoring answers
   "what's broken, and why?", and "it's better to spend much more effort on catching symptoms than causes":
   https://sre.google/sre-book/monitoring-distributed-systems/
7. [S7] Google Search Central, "Reduce the Google crawl rate": in an emergency, "return a 500, 503, or 429 HTTP
   response status code", optionally with `Retry-After`. The guidance assumes a site can see who is crawling it and
   slow that crawler: https://developers.google.com/search/docs/crawling-indexing/reduce-crawl-rate
8. [S8] Nielsen Norman Group, "Proximity Principle in Visual Design": "Items close together are likely to be
   perceived as part of the same group": https://www.nngroup.com/articles/gestalt-proximity/
9. [S9] GitHub Docs, "Managing your profile README": the README is there to "tell other people about yourself":
   https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme

Clones and data:
- Scrapy `96e7a1a`, `Scraping_project/`: `src/stage1/scout_spider.py:133-180, :291-301`;
  `src/stage1/middlewares/spider_config.py:90, :100`; `src/pipelines.py:717-798`;
  `src/stage2/stage2_worker.py:67, :116-140, :394-403, :658-672, :813-827, :914-920`;
  `src/workers/stage2_worker.py:9`; `src/stage4/large_doc_processor.py:86`; `src/utils/crawl_guard.py:7, :47-49, :271`;
  `cli.py:569`; `docs/runbooks/sev1_abuse_kill_switch.md`; `monitoring/alerting_rules.yml` (42 `alert:`, `:338`,
  `:400`, `:650`); `monitoring/prometheus.yml:26-28`; `docker-compose.yml:117-123, :235-236`; `README.md:653-654`.
  There's no `robots` in `src/stage2`, `src/workers` or `src/utils`.
- GitHub API: commits `099dd6c` (breaker, 8 Oct 2026) and `88340c0` (kill switch, 8 Oct 2026), both his; PR #1228
  opened by him.
- sdist 0.1.3: `state.rs:240, :285`; `frontier.rs:655`; `url_utils.rs:81-91`; `bfs_crawler.rs:433`;
  `main.rs:519, :539`; `cli.rs:191`.
- Rust-sitemap `32c2651`: 161 Rust test attributes, 15 Python tests, 16,390 lines of Rust.
- `assets/stats.json`: `edition`, `routes.rustmapper`, `runcheck.rustmapper.steps`, `repos[]` (`commits`, `others`,
  `coauthored`, `ci`, `lines`, `test_functions`), `figures`, `rules`, `handoffs`, `repo_count`.
