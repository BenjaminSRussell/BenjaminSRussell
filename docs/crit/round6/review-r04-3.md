# Review round 4, reviewer 3: the working navigator

10 Oct 2026. I'm a deck officer and yacht navigator, and I plan passages from real charts and pilot books. For every
mark I ask what the convention is for: what a navigator does differently because the mark is there.

What I looked at: `scratchpad/r6/build/round-03/`. That is the desk sheet at 870 and the phone sheet at 390, day and
night; `once-p1-lands/`; the whole page on desk (screens 1–2) and on phone (screens 1–5). What I read: `README.md`,
`SPEC.md`, `LOG.md` (rounds 1–3, fixed and declined), `chart.toml [route.rustmapper]`, the twelve earlier reviews,
and this round's `review-r04-1.md` and `review-r04-2.md`. I don't repeat their findings. Where I agree with one, I say
so in a line.

How I checked the figures: against `assets/stats.json`, the 0.1.3 sdist (`scratchpad/r6/sdist013`), the clones, and
the run check's own crawl logs (`scratchpad/r6/rc2/work/crawl.log`, `ends.log`). Widths come from the repo's
`typeset.text_width` in the day cut.

Verdict: **does not meet the goal yet. 7 / 10.** The form is right, and I would keep it. What it lacks is the thing a
pilot book never leaves out. It shows the danger, but it doesn't give the mark that tells you when you are past it.

## The first question: does it meet the owner's goal?

Mostly, yes. The test I use is whether a stranger can do the passage from the drawing alone. A passage plan runs from
berth to berth. It marks the dangers on the route and says how progress is watched [1]. This drawing does the first
two. It starts at `pip install`, ends at a named file, and goes on to the next project that reads it. The one danger
sits on the loop where it bites. Nothing has a size, nothing announces the theme, and it reads at 390 px. The owner's
"what is it showing?" now has a one-line answer: how you run his crawler and what you get. A list can't say "this part
repeats and has no exit", and the drawing can.

It fails on the third part: how you know where you are. I ran the passage in my head with only the phone image:

1. `pip install rustmapper`. Fine.
2. Then what do I type? The image never names the program. Its only other command is `export-sitemap`, written as
   if it were a command. A stranger types `rustmapper crawl` or `export-sitemap` and gets "command not found". The
   command that works, `rust_sitemap`, is in the code block a screen and a half lower on the phone.
3. "never stops by itself, even after the last page", then "press Ctrl-C once". **When?** How do I know the last
   page has gone by? The image warns me that there is no exit and tells me to make one, but it gives me no mark to
   act on. Every pilotage instruction pairs the action with the thing you watch for: a leading line you hold until
   the marks open, a clearing line you don't cross [2, 3]. A user who gets no feedback assumes the program has hung
   and acts again [4]. Here, acting again is the second Ctrl-C that throws the file away.

The tool does give a mark, and the run check already records it. In 0.1.3, `bfs_crawler.rs:433` prints
`Crawler: Received work item: <url> (depth n)` for every URL it starts, with no verbosity switch. In the run check's
3-page crawl (`rc2/work/ends.log`), those lines are three, one per page, and then nothing for the rest of the 150 s,
until the SIGINT. "When the `Received work item` lines stop, press Ctrl-C once" is true, can be checked, and is the
one thing the stranger needs at that point.

So the drawing is a correct chart with the dangers marked, but no clearing marks yet. Must-fixes 1 and 2 add them.
They need no new rows, only words on rows that are already drawn.

One more condition, which isn't mine to waive. As built, `check.py --tier fast` fails ROUTE-UNVERIFIED on S2
(LOG.md, round 3). A sheet that fails its own gate isn't shipped, whatever I think of it.

**On r04-1's must-fix 1 (ship 0.1.4 first).** I agree it's the best fix, but I wouldn't hold the image for it. A pilot
book describes the harbour as it is today, not as the harbour board says it will be. 0.1.3 is what `pip` gives a
stranger, and the drawing says so at the entrance ("0.1.3 · 8 NOV 2025"). While 0.1.3 is current, the hazard belongs
on the drawing, with the mark that clears it.

**Agreed with this round, not repeated below.** One rule column on the desk (r04-1 #3, r04-2 #3). C1 names the file
the export writes (r04-2 #1); my must-fix 2 builds on it. The stop in the pasted block (r04-1 #2). The governor tick
reads as a stop (r04-2 #2).

## Figures checked

| Printed | Source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `edition.date` | 0.1.3, 2025-11-08 | yes |
| by default sitemaps, certificate logs, Common Crawl | `sdist:src/cli.rs:58` | `default_value = "all"` | yes |
| queues links on its domain, above or below it | `sdist:src/url_utils.rs:81-91`; `frontier.rs:492` | scope is relative to the **start** URL's host, not the page's | the fact holds; the word "its" points at the wrong thing (must-fix 3) |
| fetches fewer pages at once when saving falls behind | `sdist:src/main.rs:90-93, 113-145` | 500 ms commit EWMA, permits 32–512; in-flight capped separately at `--workers` (`bfs_crawler.rs:283, 430`) | yes |
| saved every 50 ms | `sdist:src/writer_thread.rs:11` | `BATCH_TIMEOUT_MS: u64 = 50` | yes |
| never stops by itself | `runcheck.rustmapper` `ends_by_itself` | still running at 150 s | yes (0.1.3) |
| press Ctrl-C once to write `data/sitemap.jsonl` | `crawl_ctrl_c` | exit 0 2.0 s after one SIGINT, 3 lines | yes |
| after a kill, run `export-sitemap` | `export_after_kill` | 3 `<loc>`, written to `sitemap.xml` (not the JSONL) | the action holds; the program name is missing (must-fix 2) |
| fields: url, depth, status_code, title | `SitemapNode`, both trees | | yes |
| read by ideal-url-organizer … with a test | `handoffs[0]` `runs`, `to_sha 159968a` | 15 fields ⊆ writer | yes |
| 176 tests · CI passed 7 Oct 2026 · 16k lines · `32c2651` | `repos[Rust-sitemap]` | 176; success 2026-10-07; 16,390; head 32c2651 | yes |
| 1,920 tests · CI 8 Oct 2026 · MIT · 69k · `96e7a1a` | `repos[Scrapy]` | 1,920; success; MIT; 69,036 | yes |
| 3 min, cold, 4-core Linux | `runcheck` `install` | median 171.4 s (168.2–174.3) | yes |
| 20 per host, 256 in all, no pause | `sdist:state.rs:281, 285`; `cli.rs:32`; `bfs_crawler.rs:283` | 20; 0; 256 (a hard cap on in-flight tasks, whatever the governor adds) | yes |
| 50,000 URLs per file | main `sitemap_writer.rs:134` | `50_000` | yes |
| 50,000 characters (Scrapy) | `Scrapy:src/core/config.py:389` | `massive_doc_threshold=50000` | yes |
| 22 public repositories; 15 more | `repo_count` 22; 22 − profile − 2 − 4 | 15 | yes |
| 3 %; 297 | `coauthored_total.agent_share` 0.031; `agent_authored.total` 297 | | yes (r04-1 #4 covers what it qualifies) |

## How each mark works for someone using it

| Mark | Convention it borrows | Does it do that job here? |
|---|---|---|
| Start bar at `pip install` | the departure point of a passage plan | Yes. You find it at once. |
| Magenta line | the route you follow | Yes. One line, read top to bottom. |
| Rings | positions on the route where something happens | Yes, for the tool's steps. C1 is the one ring where **you** act, and only its wording shows that. Good enough. |
| Loop bracket with the arrow up | the part of the route that repeats | Yes. Only a drawing can show it, and it's the best thing in the image. |
| Gap under the loop | the line doesn't carry you out | Yes, and it agrees with the words. |
| Dotted line round H1 | a danger line: draw attention to a danger | It marks the danger but gives no clearing mark (must-fix 1). |
| End bar and `data/sitemap.jsonl` | arrival | Yes. The file you open, with its real field names. |
| Thin arrow to ideal-url-organizer | the onward passage | It names the destination but not what happens there (must-fix 4). |
| "0.1.3 · 8 NOV 2025" at the entrance | the edition date, read before you trust the chart | Yes, and placed where it's used. |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell" | whose page | keep | |
| Role line | crawl and data infrastructure, Python and Rust | keep | the drawing proves it |
| Header "rustmapper" + sentence | which project, what it does | keep | |
| Start bar | where to begin | keep | |
| `pip install rustmapper` | the way in | keep | |
| "0.1.3 · 8 NOV 2025" | how old the thing you install is | keep | the edition date at the point of use |
| Track | one way through | keep | |
| S1 "your URL, plus by default sitemaps, certificate logs, Common Crawl" | URLs come from more than links, and by default outside services are asked | keep | see the note on S1 with F1 below |
| F1 "fetches a page; queues links on its domain, above or below it" | it's a crawler loop, and its scope | change | "its" reads as the page's domain; the code checks the start URL's (must-fix 3) |
| G1 tick + "fetches fewer pages at once when saving falls behind" | it throttles itself to its store | keep the words | the tick is r04-2 #2 |
| W1 "saved every 50 ms" | it saves as it goes, which is why the export after a kill works | keep | |
| Desk file labels | which file to open | keep | the column is r04-1 #3, r04-2 #3 |
| Loop bracket and arrow | which rows repeat | keep | |
| H1 + dotted line | the crawl has no exit | change | add the mark that tells you when to act (must-fix 1) |
| Gap | the line doesn't carry you out | keep | |
| C1 | the one thing you do, and the way back after a kill | change | name the program (must-fix 2) |
| End bar, `data/sitemap.jsonl`, fields | what you get | keep | |
| Hand-off arrow + label | his projects feed each other | change | say what the next project does with it (must-fix 4) |
| Night editions | the same | keep | the danger dots and magenta hold on navy; no text below 4.5:1 |
| Phone editions | the same, no file labels | keep | the cleanest edition; each fix below costs at most one phone line |
| Link round the image | a tap goes to the project | keep | |

**A note on S1 with F1 (not a must-fix).** The two rows together hide the largest load surprise in 0.1.3. With the
default `all`, the certificate-log seeder asks crt.sh for every name under the start's registrable domain
(`ct_log_seeder.rs:40`, `?q=%.{domain}`; `bfs_crawler.rs:177, 222-226`). Certificate logs are public by design [8], so
that includes forgotten staging and admin hosts. Start at `example.com` and every one that resolves passes the scope
check (`frontier.rs:492`) and is fetched at 20 at a time with no pause. Common defaults are much gentler: Heritrix
opens one connection per server [5], Scrapy's AutoThrottle aims at one request per site [7], and wget advises a wait
between requests [6]. I'd normally ask for a trap here. I don't, for two reasons. The fact is already in text (L1).
And main's default is `none` (DECISIONS.md), so the hazard goes when the default changes in a release, and S1's
`instead` wording already handles that. If 0.1.4 slips by months, raise it again.

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image | above | change | must-fixes 1–4 |
| Alt text | what it shows, in 25 words | keep | "loops until one Ctrl-C writes data/sitemap.jsonl" is right |
| Link line | where to go | keep | |
| Builds / Languages / Stack | what he builds, with what | keep | |
| Pick sentence | which tool for which job | change | r04-1 #6 |
| rustmapper sentence | what it is; the API is unreleased | keep | |
| rustmapper facts line | alive, tested, size, at which commit | keep | "On main at" keeps it apart from the 0.1.3 drawing |
| Install block | how to run it | change | r04-1 #2 |
| Wheel note | when pip just works | keep | |
| L1 + X1 | what it does to the site you point it at; the 50,000 limit | keep | L1 is what anyone crawling someone else's site must know. The norms above say 20 at a time per host is far from gentle [5, 6, 7], and Google tells site owners to fight overload with 429s and 503s [10] |
| Scrapy sentence, facts line | the second tool, measured | keep | |
| Scrapy block | how to start it | change | it starts with `cd Scraping_project`, from nowhere (must-fix 5) |
| Grafana note | where to look once it runs | keep | |
| Scrapy bullets | how it's built | keep | |
| Also | the next four | keep | |
| 15 more | the rest | keep | |
| Working rules | how he works, each tied to a dated commit | keep | |
| Found a mistake? | the page can be corrected | keep | |
| Data line | what was checked and run, and when | change | r04-1 #4 (the AI clause) |
| Licence line | terms | change | r04-1 #5 |

## Must fix, ranked

1. **Give H1 the mark that tells you when to act.**
   - Where: `chart.toml` H1, `scripts/runcheck.py`, `scripts/checks/route.py`. About 30 lines and a test.
   - Text: H1 becomes "never stops by itself; done when `Received work item` lines stop". `Received work item` is set
     in `machine`, as TYPE-CODE needs.
   - Size: desk 536 units, one line inside the 728 the dotted line allows. Phone 733 against a 600 measure, so two
     lines, +34 units.
   - Release anchor: `src/bfs_crawler.rs`, `fn = "start_crawling"`, text `Crawler: Received work item:`.
   - New probe `quiet_after_last_page`, recorded from the existing `ends_by_itself` run's stderr (`ends.log`). It
     passes when two things hold. The count of distinct URLs on `Received work item` lines equals the count of
     `sitemap.jsonl` lines written after the SIGINT. And the last such line comes at least 100 s before the SIGINT.
     H1 takes the new wording only while that probe passes. Otherwise it keeps today's wording. Its empty `instead`
     still retires the row once a release ends by itself.
   - Height: phone ROUTE-HEIGHT goes from 1040 to 1100 (594 px on screen, still under one iPhone screen). That covers
     this +34, must-fix 2's +34, and S2. r04-2 #2 gives 9 back.
   - Why: the image says there is no exit and tells you to make one, but not when. Every pilotage instruction comes
     with the mark you watch for [2, 3]. Progress has to be watched, not guessed [1]. Without feedback, users act
     again [4], and here a second Ctrl-C throws the file away. The tool already prints the mark, and the run check
     already captures it.

2. **C1 names the program it runs.**
   - Where: `chart.toml` C1 and `route.py` text interpolation. About 10 lines.
   - Text: on top of r04-2 #1, the kill clause reads "after a kill, `{script} export-sitemap` → `sitemap.xml`".
     `{script}` comes from `edition.scripts`, using the same rule as the code block (T-SCRIPTS), so it prints
     `rust_sitemap` today and `rustmapper` once a wheel ships that.
   - Size: desk "after a kill, `rust_sitemap export-sitemap` writes `sitemap.xml`" is 574 units, its own line after
     r04-2's break at the semicolon. Phone 786, so two lines; C1 goes from 2 lines to 3 (+34).
   - Test: C1's drawn text contains the first entry of `edition.scripts`.
   - STRINGS-TWICE: exempt runs that are exactly `<script> <subcommand>` from the 3-word code rule. A command has to be
     spelled the same everywhere it appears.
   - Why: the image's only commands are `pip install rustmapper` and a bare subcommand. A stranger reading only the
     image types `export-sitemap` or `rustmapper …` and gets "command not found". SPEC §2.2 R3 called wrong commands
     the most common documentation failure. Since R3 was cut, this one row is where the image names a command.

3. **F1 says whose domain.**
   - Where: `chart.toml` F1 text. One line.
   - Text: "fetches a page; queues links on your URL's domain, above or below it". "your URL" picks up S1's words.
   - Size: desk 527 units, one line in the 561 left today and in the 538 left at r04-2's single column (686). Phone
     721, two lines, the same as today.
   - Why: the scope check is against the start URL's host (`frontier.rs:492`, `start_url_domain`), not the page's.
     "its domain" on a row that begins "fetches a page" reads as the page's own domain. That is a different and wider
     rule. A stranger can't use "above or below" without knowing what it's measured from.

4. **The onward arrow says what the next project does.**
   - Where: `chart.toml [[handoffs]]` label and `route.py` R15. About 8 lines and one anchor.
   - Text: "read by" becomes "sorted by". Desk: "sorted by ideal-url-organizer: `scripts/import_rust_sitemapper.py`,
     with a test", 694 units, one line. Phone: "sorted by ideal-url-organizer, with a test", 420 units, one line.
   - Anchor in the reader at `to_sha`: `scripts/import_rust_sitemapper.py` contains `run.sh` and `--all`. Its
     docstring says it "then run[s] the full analysis pipeline against it". If the anchor goes, fall back to "read by".
   - Why: the arrow is there to show that his projects are one body of work. "Read by X" only says X exists. "Sorted
     by X" says what the output is for, and the Also line confirms it ("25 ways to sort a pile of URLs").

5. **The Scrapy block starts where a stranger is.**
   - Where: the Scrapy code block in `chart.toml` / `render_readme.py`. One line changed, one added.
   - Text: replace "# run start.py from inside this dir" with "# in a clone of this repository;" (32 columns) and
     "# start.py runs only from here" (30). Both are under README-CODE-WIDTH's 38.
   - Why: the block's first command is `cd Scraping_project`, and "this dir" has no referent on a profile page. A
     getting-started section starts from what the user has [9], and the rustmapper block does (`pip install`). Scrapy's
     own README records the failure the old comment guarded against (`Scrapy:README.md:88-89`, #334). The new lines
     keep that guard and add where you begin.

## Sources (new this round)

1. IMO Resolution A.893(21), *Guidelines for Voyage Planning* (1999). §3.1: the plan covers the whole voyage "from
   berth to berth". §3.2.1: the route is laid down on the charts "with all areas of danger". §5.2: progress against
   the plan "should be closely and continuously monitored". I read the official French text in this copy:
   https://ppa.gc.ca/standard/pilotage/2018-07/IMO%20A.893.pdf
2. IHO S-57 attribute CATNAV, as published by Teledyne CARIS. A clearing line "marks the boundary between a safe and a
   dangerous area or … passes clear of a navigational danger". A leading line is one "along the path of which a vessel
   can approach safely". https://docs.teledynecaris.com/s-57/attribut/def/d-catnav.htm
3. Practical Boat Owner, "Nav in a nutshell: using transits": transits hold you on a line and tell you you are clear
   of a danger ("keep the next bay open"). https://www.pbo.co.uk/seamanship/nav-in-a-nutshell-using-transits-23183
4. Nielsen Norman Group, "Progress Indicators Make a Slow System Less Insufferable". Without feedback, users are
   unsure "whether it may have crashed", and "most users will assume the action was not registered and they will try
   again". https://www.nngroup.com/articles/progress-indicators/
5. Internet Archive, Heritrix 3 wiki, "Politeness parameters": "The most basic aspect of robot politeness is to only
   open a single connection to a server at a time." https://github.com/internetarchive/heritrix3/wiki/Politeness-parameters
6. GNU Wget manual, `--wait`: "recommended, as it lightens the server load". Also `-l`: recursion is limited to a
   depth of 5 by default. https://www.gnu.org/software/wget/manual/wget.html
7. Scrapy documentation, AutoThrottle extension: made to "be nicer to sites instead of using default download delay
   of zero"; `AUTOTHROTTLE_TARGET_CONCURRENCY` defaults to 1.0. https://docs.scrapy.org/en/latest/topics/autothrottle.html
8. RFC 6962, *Certificate Transparency*: certificates are logged publicly "in a manner that allows anyone to audit".
   https://www.rfc-editor.org/rfc/rfc6962
9. GitHub Docs, "About READMEs": a README says "how users can get started with the project".
   https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
10. Google Search Central, "Reduce the Googlebot crawl rate": crawling can "cause a critical load on your
    infrastructure"; owners should answer 500, 503 or 429.
    https://developers.google.com/search/docs/crawling-indexing/reduce-crawl-rate

From the clones and records:
- `sdist:src/bfs_crawler.rs:433` (`Crawler: Received work item`), `:174-229` (registrable domain for the CT and Common
  Crawl seeders), `:283, :430` (in-flight cap = `--workers`).
- `sdist:src/frontier.rs:492` (scope against `start_url_domain`); `sdist:src/url_utils.rs:81-91`;
  `sdist:src/ct_log_seeder.rs:40`.
- `sdist:src/main.rs:90-145` (governor); `sdist:src/cli.rs:18-99`.
- `scratchpad/r6/rc2/work/crawl.log` and `ends.log` (the run check's stderr).
- `ideal-url-organizer:scripts/import_rust_sitemapper.py` (docstring, `run.sh --all`); `Scrapy:README.md:88-89`.
- `assets/stats.json`: `edition`, `repos`, `runcheck`, `routes`, `handoffs`, `figures`, `coauthored_total`,
  `agent_authored`.
