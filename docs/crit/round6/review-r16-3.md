# Review round 16, reviewer 3: the copy editor

10 Oct 2026. I looked at every PNG in `scratchpad/r6/build/round-15/`: the sheet on desk at 870 and 846, mid at 746,
phone at 390 and 308, each day and night; the README at 1,280 (two screens), at 390 (seven) and 360 (seven). I read
`README.md`, `SPEC.md`, `LOG.md` round 15, the round 15 reviews and `review-r16-1.md`. I don't repeat anything round 15
fixed. Where I touch the same line as r16-1, I say so and say where I differ.

Verdict: **not yet. 8 / 10.** The picture has a job and does it: how you get rustmapper, what it does to each page,
where it goes wrong, the one key, the file, and who reads the file next. Nothing in it has a size. Nothing names the
sea. The theme is a magenta line, a dotted line round the catches and cream paper, and nobody is told what they are.
That's the right side of the line. A sailor would see the danger line and the course line. Everyone else sees a route
and a warning box. Nobody has to get the joke.

What's left is copy. The image has two sentences a reader has to read twice. The page has three in the Scrapy block,
and two of those were made by round 15's own insertions. None of it is false. All of it makes a stranger slower.

## The first question: does it meet the owner's goal?

- **Every element has a purpose.** Yes. I tried to cut each mark (table below), and each one teaches a step, a catch
  or an output that the text would take longer to show. The loop bracket is the best thing on the page: it shows which
  rows repeat, and that the catches sit inside the loop.
- **True and useful about his projects.** True, figure by figure (table below). One word is false after a stall
  (r16-1 must-fix 1, "done"). I agree, and I'd fix it with a different word (must-fix 1).
- **Nothing chases a reason.** Yes. No element is there for the theme alone.
- **Nothing announces the theme.** Yes. I grepped the README, the alt text and the visible text in every edition for
  the T-WORDS list. Nothing. The only "chart" on the page is Scrapy's Helm chart, which is a project fact.
- **Little jokes, not too much.** "Boring under load." and "The kind of thing you build to learn why engines are hard."
  are the only two winks on the page. Both are dry, both are about the work, and neither is nautical. Leave them. A
  third would be one too many.
- **Reads on a phone.** The image is one screen at 390 and 308. The garden paths below cost more on a phone, where
  each clause breaks over a line.
- **Would I ship it as is?** No, but it's close. Must-fixes 1 to 3 are each one sentence.

## Figures checked

| Printed | Source | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version` 0.1.3, `edition.date` 2025-11-08 | yes |
| `pip install rustmapper`, `rust_sitemap crawl` | `edition.scripts` `["rust_sitemap"]` | yes |
| up to 20 pages at a time from each host | sdist `src/state.rs:285` `max_inflight: 20` | yes |
| your site, its subdomains and its parent domain | sdist `src/url_utils.rs:81-91` `is_same_domain`: equal, `ends_with` either way on a dot | yes |
| `Received work item`; 60 s | sdist `src/bfs_crawler.rs:433` `eprintln!("Crawler: Received work item: …")`; H1's audit | yes; "done": no (must-fix 1) |
| on https, a disallowed link stalls its host | sdist `src/frontier.rs:687` "blocked by robots.txt", then `continue;` | yes |
| `Saved to` line | sdist `src/main.rs:539`, `:704` `println!("Saved to: {}", …)` | yes |
| fields `url, depth, status_code, title` | sdist `state.rs` `SitemapNode` | yes |
| sorted 21 ways by ideal-url-organizer | `159968a` `src/main.py` `self.methods`: `method_01_by_domain` to `method_21_domain_and_depth_matrix`; `scripts/import_rust_sitemapper.py` and its test exist | yes |
| 256 at a time; `RustSitemapCrawler/1.0` | sdist `src/cli.rs:32`, `:40` | yes |
| rustmapper: 176 tests, CI passed 7 Oct 2026 (tests, rustfmt), 16k lines, `32c2651` | `test_functions` 176; `ci` success 2026-10-07, `gates`; `lines.Rust` 16,390; `head.short` | yes |
| Claude authored 45 of its 146; co-signed 1 of his own 101 | `others` Claude 45; `all_hands` 146; `coauthored.agent` 1; `commits` 101 | yes |
| Scrapy: 1,920 (all but 41), 8 Oct 2026, tests ruff mypy bandit, MIT, 69k, `96e7a1a` | `test_functions`, `ci_selection.not_selected` 41, `ci.gates`, `license`, `lines.Python` 69,036, `head.short` | yes |
| jules, Claude authored 71 of 499; co-signed 30 of his own 420 | `others` 49 + 22; `all_hands` 499; `coauthored.agent` 30; `commits` 420 | yes |
| `UConn-Discovery-Crawler/1.0` | Scrapy `src/settings.py:115` | yes |
| over 50,000 characters | `src/core/config.py:389` `massive_doc_threshold=50000` | yes |
| starts PostgreSQL, Redis, Grafana and a worker for each stage | `start.py:345` `docker-compose up -d`; `docker-compose.yml` services include `prometheus` too | true, but not the whole list (must-fix 4e) |
| Measure in week one: 6 days, then 5 | `rules` prometheus 2025-10-01, `repo_first` 2025-09-25; grafana 2025-10-06 | yes |
| 15 more | `repo_count` 22 = profile + 2 + 4 + 15 | yes |

## Must fix, ranked

1. **H1: not "done", and not "quit" either. Use "end it when".** (`chart.toml:948`; the tests r16-1 lists.)
   - **What's wrong.** I agree with r16-1 that "done" is false after the stall drawn one line above. But r16-1's
     replacement, "quit when", puts the same verb on the right move and the wrong one two rows apart. C1 says "a second
     press … quits without writing the file". Read top to bottom, the image says "quit when the lines stop" and then
     "quitting loses the file". A reader who skims gets the verb and not the key count. Microsoft's style guide doesn't
     use "quit" or "exit" for ending a program at all [S5, S6].
   - **Change.** `text = "{release} never exits by itself; end it when `Received work item` lines stop for {quiet} s"`.
     That's 2 characters longer than "done when". The phone's first line becomes "0.1.3 never exits by itself; end it
     when" (40 characters). H0, at 43, already fits one line inside the same box, so the break holds. "End it" is the
     user's act, and C1 says how. "Quits" stays in C1 only, for what the program does on a second press.
   - **Test.** H1 contains "end it when" and neither "done" nor "quit". No two drawn rows share the verb stem "quit".

2. **C1 reads as "the `Saved to` line quits". Reorder it.** (`chart.toml:984`; `route.py` PURPOSE C1 wording if it
   quotes the row; the tests that pin C1's text.)
   - **What's wrong.** "press Ctrl-C once; a second press before the `Saved to` line quits without writing the file".
     The reader parses "the `Saved to` line quits" first, then has to back up to find that "a second press" is the
     subject. That's a garden path [S1]. On the phone the break falls after "before the", so the misreading gets a
     whole line to settle in.
   - **Change.** `text = "press Ctrl-C once and wait for `Saved to`; a second press quits without writing the file"`
     (86 characters; today's is 89). Now the instruction comes first and the warning second, each with its own
     subject. The anchors don't move: they test the `Saved to:` literal and the order of the export and the print.
     Two phone lines, as now; one desk line, as now.
   - **Test.** C1's text contains "wait for `Saved to`"; it still fits the existing line budget in all six editions.

3. **L6: "each link `robots.txt` disallows stalls" is a reduced relative. Put the "that" back.** (`chart.toml:1144`
   and its `instead`, `:1155`; README line 49.)
   - **What's wrong.** Without "that", the reader takes "each link `robots.txt`" as the start of the main clause, and
     "disallows stalls" as its verb and object. A reduced relative clause is the classic way to make a garden path
     [S1, S2]. The sentence also says "link" three times in 24 words.
   - **Change.** "On an https site, a link that `robots.txt` disallows stalls that host's crawl: pages queued behind it
     wait for a new link to that host." It says the same thing, it's 2 words shorter, and "pages" is what the visitor
     loses. This works with r16-1's must-fix 2: their sign sentence ("A `blocked by robots.txt` line in its output is
     the sign.") goes after it unchanged.
   - **Test.** L6 contains "a link that `robots.txt` disallows"; AUDIT-COVER and README-CAUTIONS stay clean.

4. **Scrapy block: five small repairs, all in hand-typed lines.** (`README.md:87, 89, 93, 106`; the tests that pin
   them: `test_round9.py:136-142`, `test_pipeline.py:503`, `test_round7.py:86`, `test_round10.py:63`,
   `test_round12.py:157`; the `[[figures]]` substrings stay as they are.)
   - a. **Bullet 3, line 87.** "Prometheus alerts on its own metrics, such as Delta writes spilling to disk, and
     Grafana dashboards." One verb is doing two jobs, so it reads as if Prometheus alerts on Grafana dashboards [S3].
     Change it to: "… such as Delta writes spilling to disk, and Grafana dashboards show them." The figure rows for
     "Prometheus alerts on its own metrics" and "Delta writes spilling to disk" still match. Grafana's datasource is
     Prometheus (`monitoring/grafana_datasource.yml:6-10`).
   - b. **Line 106.** "Grafana opens on `localhost:3000`. What it writes lands in Delta tables …". The nearest noun
     for "it" is Grafana, and Grafana writes nothing there [S4]. Change it to: "The crawl's output lands in Delta tables
     under `data/delta/`; …". The figure row "Delta tables under `data/delta/`" still matches.
   - c. **Line 89.** "Run these from the folder you cloned Scrapy into." Round 15 put a lead and a two-item list
     between "these" and the commands. On a 390 phone the code block is now about a screen and a half below the word
     that points at it. Change it to "Run the commands below from the folder you cloned Scrapy into." That's +2 words,
     and the sentence order the tests pin is kept.
   - d. **Line 93.** "(without that line, `UConn-Discovery-Crawler/1.0`)". No line has been mentioned yet. The line
     it means is in the code block below. Change it to "(without the `USER_AGENT` line, …)".
   - e. **Line 89.** "`python start.py` starts PostgreSQL, Redis, Grafana and a worker for each of the four stages."
     A list of four reads as complete. It also starts Prometheus (`start.py:345` `docker-compose up -d`; the
     `prometheus` service in `docker-compose.yml`), and bullet 3 and the Grafana line depend on it. Change it to
     "PostgreSQL, Redis, Prometheus, Grafana and a worker …", and add `{literal = "\n  prometheus:"}` to that figure
     row's `also`.
   - **Size.** About +1 line at 390. **Test.** The pinned strings above are updated to the new wording, and a check
     that the Scrapy block has no "What it writes" and no "that line,".

5. **One serial comma in a page that otherwise uses none.** (`README.md:26`, `[identity]` or wherever it's typed;
   `render_readme.alt_for`.)
   - Line 26 has "raw-first storage, and the dashboards" and the alt text has "what it does with each page, and how to
     stop it". Every other list on the page has no comma before the "and": "PostgreSQL, Redis, Grafana and …",
     "comments, naming, structure and git history", "sitemaps, certificate logs and Common Crawl". Pick one style and
     keep it [S7]. Drop the two commas; neither list is ambiguous without it. Zero lines.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page it is | keep | largest type, read first |
| Role, two caps lines | crawl and data infrastructure; Python and Rust | keep | the route under it proves line one. Tracking is 8 % of the size, inside the 5–12 % that caps want [S8] |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project, and what you get | keep | a plain sentence, capitalised, with a full stop. The rows under it are lowercase fragments, which is how chart notes read |
| Start bar + `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | the date is what makes every "0.1.3" caution fair |
| Magenta track | one way through, top to bottom | keep | the theme's one colour, and it carries the order |
| Stop rings | each ring is one step | keep | |
| S1 `rust_sitemap crawl` + seeds | the real command, and three outside sources by default | keep | "certificate logs" is the plain name for what the page calls crt.sh. Fine as it is |
| F1 fetch, 20 per host, scope | the loop's work and how far it reaches | keep | "its parent domain" is true (`is_same_domain`) and matches L5 |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Dotted line round the catches | where in the loop it goes wrong | keep (r16-1 pads it) | a chart's danger line. To anyone else it reads as a warning box, which is also right |
| H0 the stall | on https, pages can stop coming | keep, reworded by r16-1 must-fix 3 | |
| H1 never exits; 60 s | when to stop it yourself | **change** | must-fix 1: "end it when" |
| C1 Ctrl-C once | the one key, and the press not to make | **change** | must-fix 2: garden path |
| End bar + `data/sitemap.jsonl` + fields | the file, in the struct's names | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | his projects feed each other | keep | the same "21 ways" as the Also line, so the two points agree |
| Night editions | the same | keep | |
| Desk, mid and phone editions | the same, sized to the column | keep | |
| Alt text | install, loop, stop, file | keep | drop the serial comma (must-fix 5) |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image link to the repository | where the project lives | keep | |
| Link line | where to go | keep | |
| "Ben Russell builds …" | what he builds | change | must-fix 5, one comma |
| Languages | what he writes in; the semicolon puts Python and Rust first | keep | |
| Stack | what he builds on | keep | |
| Pick sentence | which tool for which job | keep | the best sentence on the page |
| rustmapper facts line | alive, tested, size, commit, who wrote it | keep | see the italics note |
| Wheel note | whether `pip` just works for you | keep | see the note on "Apple silicon" |
| "Before you run 0.1.3:" L1, L7, L4, L2, L5 | what it does to someone else's server, with the lever for each | keep | "line, then `<br>` lever" is a good pattern; keep it for every item |
| L6 the stall | what 0.1.3 does on https | **change** | must-fix 3, and r16-1's sign |
| Fold "What 0.1.3's files miss or get wrong" | the file's caveats | keep (r16-1 item 3) | |
| rustmapper code block | how to run it, when to stop, how to recover | keep | its "then Ctrl-C once" is already an instruction, which H1 should match |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy bullets 1–2 | storage; what happens to a page | keep | |
| Scrapy bullet 3 | how it's watched, stopped and deployed | **change** | must-fix 4a |
| Scrapy run paragraph | what `start.py` starts and needs | **change** | must-fix 4c, 4e |
| Scrapy "Before you run it:" | what the crawl does to a site | **change** | must-fix 4d |
| Scrapy code block | how to point it at your site | keep | |
| Grafana and `data/delta/` | where to look once it runs | **change** | must-fix 4b |
| Also: four tools | the file's reader, the Go sibling, two more | keep | |
| 15 more (fold) | the rest | keep | the game_engine aside is the right amount of joke |
| Working rules 1–3 | how he builds, with evidence | keep | "Measure in week one" holds: metrics on day 6 |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn and how it was run | keep | |
| Licence line | the profile's terms | keep | |

## Noted, not ranked

- **The facts lines are whole paragraphs in italic**, six lines each at 390. Butterick: italic is "fine for short bits
  of text, but not for long stretches", and in a sans the slant "doesn't stand out" anyway [S9]. Round 5 chose italic
  over `<sub>` on purpose, so I'm not ranking it. If it's revisited, roman text with the link in bold reads faster.
- **Word spaces in the caps role line** measure 4 to 5 px at 870, against letter gaps of 2 to 4 px. "PYTHON AND RUST"
  holds together at a glance, but only just. If `typeset` doesn't add the tracking to the space, add it.
- **"Prebuilt for Apple silicon … On Linux x86_64"** puts a marketing name and a platform tag in one sentence.
  "macOS arm64" would match the other half.
- **"Start at the bare domain to take them all."** "To include them" is plainer. It's taste.
- **"A kill switch stops new downloads within 5 s, with a runbook."** "With a runbook" hangs off "5 s" [S10]. "A kill
  switch, with a runbook, stops …" fixes it, but the figure row pins "with a runbook", so it's cosmetic.
- **"rustmapper · on main at …"** starts lowercase after the link; Scrapy's starts "On main at" as its own paragraph.
  Both are right where they are. Mentioned only so nobody "fixes" one to match the other.
- **At 1,280, `UConn-Discovery-Crawler/1.0` breaks after "Discovery-"**, so a reader who copies the first line gets
  half a user agent. GitHub decides where to wrap, so there's nothing to build here.

## Sources (new this round; none cited in earlier rounds)

1. [S1] Wikipedia, "Garden-path sentence": "a grammatically correct sentence that starts in such a way that a reader's
   most likely interpretation will be incorrect". That's C1 and L6 (must-fixes 2, 3):
   https://en.wikipedia.org/wiki/Garden-path_sentence
2. [S2] Wikipedia, "Reduced relative clause": "a relative clause that is not marked by an explicit relative pronoun or
   relativizer", "given to ambiguity or garden path effects". That's L6's missing "that" (must-fix 3):
   https://en.wikipedia.org/wiki/Reduced_relative_clause
3. [S3] Wikipedia, "Zeugma and syllepsis": "the use of a word to modify or govern two or more words or phrases". That's
   Scrapy bullet 3, where "alerts on" governs both the metrics and the Grafana dashboards (must-fix 4a):
   https://en.wikipedia.org/wiki/Zeugma_and_syllepsis
4. [S4] Wikipedia, "Antecedent (grammar)", uncertain antecedents: when "two or more prior nouns or phrases could
   match", "repeat the words of the antecedent rather than use only a pronoun". That's "What it writes" after Grafana
   (must-fix 4b), and the same advice covers "these" and "that line" (4c, 4d):
   https://en.wikipedia.org/wiki/Antecedent_(grammar)
5. [S5] Microsoft Style Guide, "quit": "Don't use *quit* to refer to … Closing an app or a program." That's one reason
   not to take r16-1's "quit when" (must-fix 1):
   https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/q/quit
6. [S6] Microsoft Style Guide, "exit": "Don't use to describe closing an app or program." The image's own "never exits
   by itself" describes the program, which is fine. The instruction to the user should use a different verb (must-fix
   1): https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/e/exit
7. [S7] Wikipedia, "Serial comma": "It is important that the serial comma's usage within a document be consistent."
   The Economist omits it "unless one of the items includes another and". So does this page, except twice (must-fix
   5): https://en.wikipedia.org/wiki/Serial_comma
8. [S8] Matthew Butterick, Practical Typography, "Letterspacing": "always add 5–12% extra letterspacing to text in all
   caps". The role line's 1.6 on 19 is 8 %, so the tracking is right; only the word space is in question (noted):
   https://practicaltypography.com/letterspacing.html
9. [S9] Matthew Butterick, Practical Typography, "Bold or italic": "fine for short bits of text, but not for long
   stretches"; sans italics "just have a gentle slant that doesn't stand out" (noted, the facts lines):
   https://practicaltypography.com/bold-or-italic.html
10. [S10] Wikipedia, "Dangling modifier": a modifier that "could be misinterpreted as being associated with a word
    other than the one intended" ("with a runbook", noted): https://en.wikipedia.org/wiki/Dangling_modifier
11. [S11] The sdist and clones, read for this round: `rustmapper-0.1.3` `src/state.rs:285`, `src/url_utils.rs:81-91`,
    `src/bfs_crawler.rs:433`, `src/frontier.rs:687`, `src/main.rs:539, 704`, `src/cli.rs:32, 40`;
    ideal-url-organizer `159968a` `src/main.py` (`self.methods`); Scrapy `96e7a1a` `Scraping_project/start.py:345`,
    `docker-compose.yml` (services), `monitoring/grafana_datasource.yml`, `src/settings.py:115`,
    `src/core/config.py:389`; `assets/stats.json` (`edition`, `repos[]`, `rules`); `chart.toml` (`[[figures]]`, H0,
    H1, C1, L6); a pixel measurement of the role line in `sheet-desk-day-870.png`.

I couldn't run more web searches this round because the session's search budget was spent. Every source above was
read directly with WebFetch.
