# Review round 7, reviewer 3: the copy editor

10 Oct 2026. My lens: the words, line by line, and the point where a theme stops being charming and starts being
embarrassing. What I looked at: every PNG in `scratchpad/r6/build/round-06/`. That is the desk sheet at 870 (day and
night), the phone sheet at 390 and 308 (day and night), the desk page (two screens), and the phone page at 390 and 360
(six screens each). I read `README.md`, `SPEC.md`, `DECISIONS.md`, `LOG.md`, the 18 reviews from rounds 1 to 6, and
the two other round-7 reviews. I don't repeat anything already fixed. Where I agree with review 1 or review 2 of this
round, I say so in one line and don't argue it again. Figures were checked against `assets/stats.json`, the 0.1.3
sdist (`scratchpad/r6/sdist013`) and the clones.

**Verdict: 7 / 10. It does not meet the goal yet. I would not ship it as is.**

## The first question: does it meet the owner's goal?

Mostly, and the image comes closer than the page around it.

- **A deep purpose for the map.** Yes. The image is a route a stranger follows: install it, what goes in, the loop
  it runs, where it bites, how to stop it, what file you get, and what reads that file next. Nothing has a size.
  Nothing is drawn to look nautical. The loop bracket and the break in the track show something a list can't.
- **Nothing announces the theme.** Yes, and I looked hard. No visible word names it. The manner is right and not
  overdone: one magenta line to follow, a bar at each end, and a dotted line around the one danger. On a real chart,
  a danger line "draws attention to a danger which would not stand out clearly enough if represented solely by its
  symbol" [12], and that is what the red dots do for H1. Nobody has to know that to read it. That is the charming
  side of the line, and the image stays on it.
- **Where it tips into cringe.** Not in the image, and not in anything nautical. It tips in the **Working rules**.
  Three of the four bodies use one poster template: "The system worth having is the one still running…", "The
  question you will want next month is one you cannot ask today…", "A crawler you cannot watch is a crawler you cannot
  trust". Rule 3 is a snowclone of "you can't manage what you can't measure" [10], a line that is usually pinned on
  Drucker, who never said it [11]. Read three in a row, they sound like a LinkedIn post. That is the same "too on the
  nose" problem the owner had with the ship theme, now coming from management slogans. Rules 1 and 3 also pull
  against each other: one says the good system runs after you stop watching it, and the next says you can't trust
  what you can't watch.
- **True and useful about his projects.** The image's facts all hold (table below). The page has one confusion that
  nobody has raised in seven rounds. The **Scrapy** in bold on his profile is his repository, but "Scrapy" is also a
  well-known framework, with 64.7k stars and the name `Scrapy` on PyPI [1, 2]. The link line reads "rustmapper ·
  Scrapy · PyPI", and the pick sentence says "**Scrapy** keeps the pages themselves … in a pipeline that needs Docker".
  A screener who knows the framework reads that as a claim about the framework, or as Ben claiming it. The block's
  first sentence doesn't fix it ("Scrapy is a multi-stage crawl platform built on the Scrapy framework"), and
  "pipeline" is the framework's own term for something else [3].
- **Reads on a phone.** The image does. The page breaks lines in the wrong places: "CI passed 8 / Oct 2026" and "16k
  lines of / Rust" (390), "(3 / min" nearly, and "`Crawl-` / `delay`" inside a code span at both 390 and 360. Code
  blocks clip at 360 (review 1's must-fix 1 and review 2's must-fix 3; I agree and don't repeat them).

## Figures checked

| Printed | Source | Holds |
|---|---|---|
| `pip install rustmapper` · 0.1.3 · 8 NOV 2025 | `edition.version` 0.1.3, `edition.date` 2025-11-08 | yes |
| "by default" seeds | sdist `src/cli.rs` `default_value = "all"` | yes (wording: must-fix 6) |
| 500 ms | sdist `src/main.rs` `THROTTLE_THRESHOLD_MS: f64 = 500.0` | yes |
| every 50 ms | `BATCH_TIMEOUT_MS = 50`, but it is the idle wait | no (review 2's must-fix 1; I agree) |
| 0.1.3 never stops by itself | runcheck `ends_by_itself`: "still running at 150 s" | the fact holds; the verb is wrong (must-fix 2) |
| `Received work item` | sdist `src/bfs_crawler.rs:433`, an `eprintln!`, so it always prints to the terminal | yes |
| Ctrl-C once writes `data/sitemap.jsonl` | runcheck `crawl_ctrl_c`: exit 0 2.0 s after one SIGINT, 3 lines | yes |
| fields url, depth, status_code, title | `SitemapNode` in both trees | yes |
| sorted 25 ways | 25 `method_*.py` files; the import runs 21 | no (review 2's must-fix 2; I agree) |
| 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust · `32c2651` | `repos[Rust-sitemap]`: 176, success 2026-10-07, 16,390, head `32c2651` | yes |
| 1,920 tests · CI passed 8 Oct 2026 · MIT · 69k lines · `96e7a1a` | `repos[Scrapy]`: 1,920, success 2026-10-08, MIT, 69,036, head `96e7a1a` | yes (review 2's CI caveat stands) |
| 3 min, cold cache, 4 cores | runcheck install: median 171.4 s, cold, 4 CPUs | yes |
| 20 per host, 256 in all, no pause | sdist `state.rs` `max_inflight: 20`; `cli.rs` 256; probe `robots_read`: closest fetches 1 ms apart | yes |
| 50,000 URLs per file | sitemaps.org; Google: "you must break your sitemap into multiple sitemaps" [4] | yes (note 2) |
| four stages (proposed, must-fix 1) | `Scraping_project/src/stage1` to `stage4`; Scrapy README: Discovery, analysis, summaries, large docs | yes |
| 22 repositories, 15 more | `repo_count` 22; 22 − profile − 2 − 4 = 15 | yes |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page this is | keep | read first, at the right size |
| Role line, two caps lines | crawl and data infrastructure, in Python and Rust | keep | the route below proves both halves |
| Empty left column under the role (desk) | nothing | keep | an empty column is better than filler. It is the only quiet place on the sheet |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project, and what it makes | keep | the best sentence on the page: plain, true for a 404 line too |
| Start bar | where you begin | keep | a fixed entrance, unlabelled, which is right |
| `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | the date sits on its command |
| Magenta track | one way through, top to bottom | keep | the route colour, never named |
| Stop rings | one step the tool takes | keep | |
| S1 "your URL, plus by default URLs found without links: …" | it finds URLs it never followed a link to | change | the fact is good. The comma that should come after "plus" is missing, so it reads "plus by default URLs", and "found without links" can mean two things (must-fix 6) |
| F1 "fetches a page; queues links to …" | the loop and its scope | keep | (review 1's must-fix 3 on how it joins G1; I agree) |
| G1 "fetches fewer pages at once when saves average over 500 ms" | it slows down when saving falls behind | keep | the one unusual design idea, given as a number you can check |
| W1 "logged to disk, then saved to redb, every 50 ms" | log, then store | change | review 2's must-fix 1. Also: it has no subject. When it's rewritten, give it one: "each result logged to disk, then saved to redb, in batches" |
| Loop bracket + up arrow | which rows repeat | keep | the one thing only a drawing shows |
| Break in the track under the loop | the loop has no way out but Ctrl-C | keep | true of 0.1.3 |
| H1 red dotted box | the catch in this release, and how to tell you're done | change the words, keep the mark | "never stops … lines stop" uses one verb for two different things in one line (must-fix 2) |
| C1 "press Ctrl-C once to write `data/sitemap.jsonl`" | the one thing you do | keep | the only imperative on the route, so the reader's own action stands out. A list of mixed grammar is usually a fault [7]; here the mix carries meaning: the tool does things, you do one thing |
| End bar + `data/sitemap.jsonl` + fields | what you get, in the struct's own words | keep | |
| Hand-off line, arrow, "sorted 25 ways by ideal-url-organizer" | his projects feed each other | keep the line, fix the count | review 2's must-fix 2 |
| Night editions | the same | keep | contrast holds by eye |
| Phone editions | the same, in one screen | keep | |
| Alt text | how to start it, the loop, the stop | keep | it states the message in 25 words |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Link line "rustmapper · Scrapy · PyPI · Email" | where to go | change | "Scrapy · PyPI" reads as the framework's PyPI page. Put PyPI next to the project it belongs to (must-fix 1) |
| "Ben Russell builds …" | what he builds | keep | |
| Languages | what he writes in | change | review 1's must-fix 2 (JavaScript); I agree |
| Stack | what he builds on | keep | |
| Pick sentence | which tool for which job | change | "**Scrapy** keeps the pages…" can be read as the framework (must-fix 1); "summarised" is the page's one British spelling (must-fix 5) |
| rustmapper sentence | the API isn't released | keep | |
| rustmapper facts line | alive, tested, size | change | "CI passed 8 / Oct 2026", "16k lines of / Rust": the dates and units break across lines on a phone (must-fix 4) |
| rustmapper code block | how to run, stop and recover | change | reviews 1 and 2 (360 px); I agree |
| Wheel note | when pip just works | change | "(3 min" can wrap away from its unit; same fix (must-fix 4) |
| Load note (L1) | what it does to a server | keep | true, useful, plain. `Crawl-` / `delay` breaks at the hyphen (note 1) |
| Sitemap note (X1) | the one-file limit | keep | (note 2: say what the limit means for you) |
| Scrapy sentence | what Scrapy is | change | "a multi-stage crawl platform built on the Scrapy framework" names the collision without resolving it, and "platform" is the only puffed-up noun on the page (must-fix 1) |
| Scrapy facts line | alive and tested | keep | (review 2's must-fix 5 stands) |
| Scrapy code block | how to start it | change | reviews 1 and 2 |
| Grafana / spider-name note | two things that trip a stranger | keep | |
| Scrapy bullet 1 "A scout spider goes first; …" | the stages | cut, if must-fix 1 lands | the new lead sentence says it, with the stage names |
| Scrapy bullets 2–4 | the design, in checkable terms | keep | |
| Also: ideal-url-organizer, go_go_go, rust_llm_logger | the next three | keep | each line is a mechanism |
| Also: Ai_code_detector "probabilistic forensics for AI-generated code" | what it does | keep, just | "probabilistic forensics" is lifted from its own README, and "from stylometry down to git-history patterns" redeems it. If anything on the page gets trimmed next, it's this |
| 15 more | the rest | keep | "The kind of thing you build to learn why engines are hard" is the page's one joke, and it lands. It is the kind of one-off line the owner asked for. Leave it alone |
| Working rules 1–3 | how he works | change | one template three times, one snowclone, and rules 1 and 3 contradict each other (must-fix 3) |
| Working rule 4 | how he parses URLs | keep | "Parse, don't pattern-match" echoes a known essay title. One borrowed form is a nod; three would be a habit |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn; agent authorship | change | "The drawing is rustmapper 0.1.3": a drawing isn't a release, it shows one. "Scrapy's 499" has the same name problem (must-fix 7) |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **Tell his Scrapy from the Scrapy framework at first mention** (`render_readme.py`, the link line, the pick
   gate's text in `chart.toml [copy]`, the Scrapy block's lead; one `[[figures]]` row; about 15 lines and a test).
   - Link line: "rustmapper · PyPI · Scrapy · Email". PyPI moves next to the project it belongs to. Same links.
   - Pick sentence: "**rustmapper** gives you a site's list of URLs from one binary, with no services to run. His
     **Scrapy** repository keeps the pages themselves, deduplicated and summarized, and needs Docker." That's 2 words
     longer than today, and on the phone it stays six lines. "Pipeline" goes, because in Scrapy it names item
     pipelines [3], and the repository has its own `pipelines.py`.
   - Block lead, replacing "is a multi-stage crawl platform built on the Scrapy framework.": "**[Scrapy](…)** is his
     crawl system on top of the Scrapy framework, in four stages: discovery, analysis, summaries, large documents."
     New `[[figures]]` row: `text = "four stages"`, `repo = "Scrapy"`, `glob = "Scraping_project/src/stage[0-9]"`,
     `count = 4`.
   - Cut bullet 1 ("A scout spider goes first; analysis and summarization workers follow, each its own stage."): the
     lead now says it. That saves three phone lines.
   - Test: in the visible README text, the first "Scrapy" after the image that is not a link is preceded by "His",
     and the block's lead holds "Scrapy framework".
   - Owner, not here: the repository's own README is titled "Web Scraping Pipeline". A rename (e.g. `crawl-pipeline`)
     would remove the problem at the source. Recorded for him, not ranked.
   - Why: the link line and the pick sentence are the second and fourth things a visitor reads. "Is it his or is it
     the famous one?" is the first question a crawler engineer will ask, and the page answers it only in the
     eleventh paragraph.

2. **H1: "exits", not "stops"** (`chart.toml` H1, line 501, and its fallback at 508; `routes` re-verified; one test).
   - Text: "`{release}` never exits by itself; done when it stops printing `Received work item`". Fallback:
     "`{release}` never exits by itself, even after the last page".
   - Today the line says it "never stops" and then that you're done when the lines "stop". The crawl does stop. The
     process doesn't exit. The probe already uses the right verb ("exits by itself within 150 s"), and so does
     `crawl_ctrl_c` ("exit 0 2.0 s after one SIGINT"). "It stops printing" also says where the lines are, which today
     the reader has to guess: `bfs_crawler.rs:433` is an `eprintln!`, so it's the terminal.
   - Desk: about 7 characters longer, so still one line (it ends near 765 px, and the measure is 832). Phone: the
     second line may wrap to a third (+34 units, 1,169 → about 1,203, inside the 1,246 gate). The dotted box grows
     with it.
   - Test: the drawn H1 text holds "exits", and it doesn't use "stop" with two different subjects.

3. **Working rules in plain claims, one template at most** (`chart.toml [[notices]]` 1–3 bodies; rule 1's anchor
   and cite per review 1's must-fix 4; about 6 lines and a test).
   - 1 **Boring under load.** "One failing host is set aside for a minute; the rest of the crawl goes on." Cite, as
     review 1 gives it: "*Scrapy, Oct 2026: a circuit breaker for each host in stage 2.*" The body now says what the
     proof shows: after 5 URLs fail every retry, that host is left alone for 60 s (`stage2_worker.py:218-219`).
   - 2 **Raw before clean.** "Next month's question can't be known today, so the raw layer is appended to and never
     overwritten."
   - 3 **Dashboards before speed.** "Dashboards go in version one." The cite carries the proof. The snowclone goes.
   - Test: no two rule bodies match `^(The|A) \w+ .* is (the one|one|a \w+) ` (the "X that … is Y that …" frame), and
     no body holds "you cannot … you cannot".
   - Why: this is where the page tips from voice into slogan. The owner's word for the ship version was "cringy", and
     it applies here just as well. Rules 1 and 3 read as a contradiction: stop watching it, but don't trust it unless
     you watch it.

4. **Keep dates and number-unit pairs on one line** (`render_readme.py` `fmt_date` line 81 and `facts_block` line
   375; the wheel note's "3 min"; about 8 lines and a test).
   - `fmt_date` returns `f"{day} {Mon} {year}"` (and `Mon YYYY` for month-only). Facts: `16k lines`
     is not enough, because "lines of / Rust" breaks too, so join "of" and the language: `16k lines of Rust`.
     Units: `3 min`, `60 s`, `500 ms`, and `50,000 characters` in text the renderer writes.
   - A no-break space "prohibits breaks on either side" [5], and style guides keep a number with its unit [6].
     GitHub strips inline styles [9], so `white-space: nowrap` isn't available. The character is the only tool.
   - Test: every date and every `<digits> <unit>` in the visible README text is joined by U+00A0. The FIGURES and
     STRINGS checks normalize U+00A0 to a space before matching.
   - Why: "CI passed 8" at the end of a line, with "Oct 2026" on the next, is exactly where the owner's "the data
     doesn't look exactly accurate" begins on a phone.

5. **One spelling system** (`chart.toml` `[copy]` pick text and the `[[figures]]` row `text = "summarised"` at
   line 201; one test).
   - "summarised" → "summarized". It is the only British spelling in the visible README. The same page says
     "summarization", "license" and "color". The Google developer style guide follows Merriam-Webster's first form
     [8], which is "summarize".
   - Test: no visible README word matches `\w+is(e|ed|ing|ation)\b` from a short list (summarise, organise, optimise,
     recognise, normalise).

6. **S1 punctuated, and "without links" said once, clearly** (`chart.toml` S1, line 409, and the fallback at 415).
   - "your URL and, by default, URLs looked up rather than followed: sitemaps, subdomains in certificate logs,
     Common Crawl". Fallback: "your URL and, if asked, URLs looked up rather than followed: …".
   - The anchors are unchanged. Each seeder looks URLs up (a sitemap file, a crt.sh query, the Common Crawl index)
     and doesn't follow links. Desk: still two lines (+11 characters on the first, which stays inside the measure).
     Phone: still three.
   - Why: "plus by default URLs" runs a parenthetical into its noun, and "found without links" could mean URLs that
     have no links.

7. **The data line says "shows"** (`render_readme.py` `survey` block; one test).
   - "The [drawing](DESIGN.md) shows rustmapper 0.1.3, the release pip installs; …" and "… 71 of the Scrapy
     repository's 499." (The framework has thousands of commits, and "Scrapy's 499" invites the same misreading as
     must-fix 1.)

## Notes (true, not ranked)

1. `Crawl-delay` breaks at its hyphen inside the code span on a phone, at 390 and at 360, because a hyphen is a break
   opportunity [5]. U+2011 would fix the look but break copy-and-search for a robots.txt directive. Leave it, unless
   a rewrite happens to move the word. Not worth a hack.
2. X1 ends on the limit and leaves the reader to work out what it means for them. Google's wording is "you must break
   your sitemap into multiple sitemaps" [4]. A clause would finish the thought: "…; the sitemap format allows 50,000
   URLs per file, so a bigger site's file has to be split before you submit it." This is advice, not a fact about
   0.1.3, so I haven't ranked it.
3. Three names for one project are still on the first screen: `rustmapper` (PyPI, header), `rust_sitemap` (the
   command) and `Rust-sitemap` (the repository the image links to). That's the owner's fix (0.1.4 and a rename), and
   it was recorded in rounds 4 to 6. Not re-ranked.
4. On the theme, for the record: the hidden marker names (`survey`, `notices`) and the `chart` branch in the image
   URLs are never seen in the rendered page. They are fine.

## Sources (new this round)

1. scrapy/scrapy on GitHub: 64.7k stars, "Scrapy, a fast high-level web crawling & scraping framework for Python".
   https://github.com/scrapy/scrapy
2. PyPI JSON for `scrapy`, fetched today: name "Scrapy", 2.19.0, "A high-level Web Crawling and Web Scraping
   framework". https://pypi.org/pypi/scrapy/json
3. Scrapy docs, *Item Pipeline*: "After an item has been scraped by a spider, it is sent to the Item Pipeline". In
   Scrapy, "pipeline" is a framework term. https://docs.scrapy.org/en/latest/topics/item-pipeline.html
4. Google Search Central, *Build and submit a sitemap*: "All formats limit a single sitemap to 50MB (uncompressed) or
   50,000 URLs … you must break your sitemap into multiple sitemaps."
   https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
5. Unicode UAX #14, *Line Breaking Algorithm*: a hyphen gives "a line break opportunity after the character"; NO-BREAK
   SPACE (GL) prohibits breaks on either side; U+2011 for a hyphen that must not break.
   https://www.unicode.org/reports/tr14/
6. Wikipedia, *Non-breaking space*: "Many style guides recommend that numbers and the associated units not be split
   across lines." https://en.wikipedia.org/wiki/Non-breaking_space
7. Google developer documentation style guide, *Lists*: "Use the same syntax/structure for all list items in a given
   list, if possible." https://developers.google.com/style/lists
8. Google developer documentation style guide, *Spelling*: follow Merriam-Webster and "use the first form listed".
   https://developers.google.com/style/spelling
9. github/markup README: rendered HTML "is sanitized, aggressively removing things that could harm you", including
   inline styles. https://github.com/github/markup
10. Wikipedia, *Snowclone*: a cliché phrasal template, recognisable in many variants (Pullum, 2003).
    https://en.wikipedia.org/wiki/Snowclone
11. Ness Labs, *The fallacy of "what gets measured gets managed"*: Drucker didn't coin it and didn't believe it; the
    phrase probably descends from Ridgway (1956). https://nesslabs.com/what-gets-measured-gets-managed
12. NOAA/IHO Chart No. 1, section K, "danger line", as quoted (secondhand) in a chart-symbols thread: "draws
    attention to a danger which would not stand out clearly enough if represented solely by its symbol".
    https://bassresource.com/bass-fishing-forums/topic/184695-navionics-web-app-symbol-help

Clones and data: `assets/stats.json` (`edition`, `repos[]`, `runcheck.rustmapper.steps` including `ends_by_itself`,
`quiet_after_last_page`, `crawl_ctrl_c`, `robots_read`); sdist 0.1.3 `src/bfs_crawler.rs:433` (`eprintln!`),
`src/cli.rs`, `src/main.rs:90`; Scrapy `Scraping_project/src/stage1` to `stage4`, `src/pipelines.py`, `README.md:1-4`
("Web Scraping Pipeline"), `:130-139` (stage names); `chart.toml` lines 109-145 (notices), 201 (summarised), 409-415
(S1), 501-508 (H1); `scripts/render_readme.py:66-81` (`fmt_date`), `:375` (lines of). Renders:
`page-phone-2.png`/`-3.png` (390: "CI passed 8 / Oct 2026", "16k lines of / Rust", "`Crawl-` / `delay`"),
`page-phone-360-2.png` ("`Crawl-` / `delay`").
