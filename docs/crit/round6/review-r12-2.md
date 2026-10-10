# Review round 12, reviewer 2: the copy editor

10 Oct 2026. My lens: the words, line by line, and the point where a theme stops being charming and starts being
embarrassing. I looked at every PNG in `scratchpad/r6/build/round-11/`: the desk sheet at 870 (day and night), the
phone sheet at 390 and 308 (day and night), the desk page (two screens) and the phone page at 390 (six screens) and
360. I read `README.md`, `SPEC.md`, `LOG.md` through round 11, the round 7 copy review (`review-r07-3.md`) and the
round 11 reviews, and I followed the one link on the page that explains the drawing. Nothing already fixed is
repeated here. I checked figures against `assets/stats.json`, the 0.1.3 sdist (`scratchpad/r6/sdist013`) and the
clones.

**Verdict: 8 / 10. It does not meet the goal yet, and I would not ship it as is.**

## The first question: does it meet the owner's goal?

- **A deep purpose for the map.** Yes. The image is directions for a stranger: how to get it, what it does to every
  page, where the 0.1.3 catch is, how to get out, what file you get and which of his projects reads it next. Nothing
  has a size, and the loop bracket shows something a list can't.
- **True and useful about his projects.** The image's facts hold (table below). One Scrapy bullet credits the wrong
  tool with a job (must-fix 4). One fold label hides the six repositories that best back up his role line
  (must-fix 5).
- **Nothing chases a reason.** It nearly holds. Rule 3's title promises more than its body proves (must-fix 6).
- **Nothing announces the theme.** On the page, yes. No visible word names it, and the manner is down to one magenta
  line and one dotted line, each of which means something. **One click away, no.** The data line's link
  "[drawing](DESIGN.md)" is the only place a visitor is told how the picture is made. It opens a page titled "DESIGN —
  how the chart is drawn" that talks about "the ship's log paper", "islands, coast", "red lateral marks", "the flashing
  core of a light", the "unsurveyed band", "chart practice", "soundings" and a channel "pecked and unlit". None of that
  is on the profile any more, and "unsurveyed" is a word the owner banned by name. That is must-fix 1.
- **Reads on a phone.** Yes. The image fits one screen at 390 and at 308. No flag splits.

On where the theme sits on the charm-to-cringe line: the profile is on the right side of it, and the risk now is
adding something back. The magenta route is a real convention. NOAA kept a magenta route line on its waterway charts
for a century, and it became "an advisory directional guide" after boaters followed a stale copy of it into shoals
[S9]. The dotted red line round the one catch is a danger line. Neither is explained, and neither needs to be. The
deadpan lines carry the voice: "`--seeding-strategy none` asks no one", "The kind of thing you build to learn why
engines are hard". Dry humour should be "straight-faced" and should never be forced; "if you're unsure, keep a
straight face" [S5]. Two dry lines are enough. Don't add a third, and don't add a single mark of theme to the image.

## Figures checked

| Printed | Source | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version` 0.1.3, `edition.date` 2025-11-08 | yes |
| `rust_sitemap crawl` | `edition.scripts` `["rust_sitemap"]` | yes |
| up to 20 pages at a time from each host | sdist `state.rs:285` `max_inflight: 20` | yes |
| "its subdomains and its parent domain" | sdist `url_utils.rs:81-91` `is_same_domain`: equal, or one ends with the other at a `.` boundary | yes (it checks for the dot, so `notexample.com` is out) |
| `Received work item` lines | sdist `bfs_crawler.rs:433` `eprintln!("Crawler: Received work item: …")` | yes |
| 60 s | H1 `quiet` 30 + 20 + 4 + 1, rounded up; probe `quiet_slow_page` ok | yes |
| `Saved to:` | sdist `main.rs:539`, `:704` `println!("Saved to: {}", …)` | yes (the wording is must-fix 2) |
| sorted 21 ways | `handoffs[0]` state `runs`, 15 reader fields; 21 methods | yes |
| 176 test functions · CI 7 Oct 2026: tests, rustfmt · 16k lines of Rust · `32c2651` | `repos[Rust-sitemap]` 176, success 2026-10-07, gates, 16,390, head | yes |
| 1,920 test functions · CI 8 Oct 2026: tests, ruff, mypy, bandit · MIT · 69k · `96e7a1a` | `repos[Scrapy]` 1,920, success 2026-10-08, gates, MIT, 69,036, head | yes |
| 3 min, cold cache, 4-core | runcheck install median 171.4 s, 4 CPUs | yes |
| 143,208 / 134,807 on uconn.edu | counted in round 11 and checked again by review r11-1 | yes |
| "Near-duplicates are dropped by URL hash and MinHash" | Scrapy `stage3_worker.py:148-185`: a repeated `url_hash` is skipped; MinHash LSH (Jaccard 0.3, first 1,000 words) drops near-duplicate text | **half**: the hash drops repeats, not near-duplicates (must-fix 4) |
| "an extractive summary" | `stage3_worker.py:193-198`: the first 5 sentences (`SUMMARY_LIMITS["extractive_max_sentences"] = 5`), cut at 1,000 characters | true, but vague (must-fix 4) |
| 50,000 characters → stage 4 | `core/config.py:389` `massive_doc_threshold=50000` | yes |
| Rule 1: 5 URLs, 60 s, Oct 2026 | `rules[0]` `099dd6c` 2026-10-08, his | yes |
| Rule 3: 6 days, then 5 | `rules[]` prometheus `d571e6e` 2025-10-01 (repo's first commit 2025-09-25), grafana `e8cbe15` 2025-10-06 | yes (the title is must-fix 6) |
| 45 of 146; 71 of 499; co-signed 1 and 30 | `all_hands` − `commits` 146 − 101; 499 − 420 − 8 dependabot; `coauthored.agent` 1, 30 | yes |
| "a local 3-page site" | runcheck entrance step: 3 lines, status 200 | yes |
| 15 more | 22 − profile − 2 − 4 | yes |

## Must fix, ranked

1. **Make the page the "drawing" link opens describe this drawing, in plain words** (`scripts/tokens.py`
   `DESIGN_HEAD`, `uses = {…}` at `:135` and `design_md()` at `:242`; `DESIGN.md` regenerated; one check. About 60
   lines changed, most of them deleted.)
   - Today DESIGN.md says at the top "Generated by `python3 scripts/tokens.py --md > DESIGN.md`; edit
     `scripts/tokens.py`, not this file", but it was edited by hand. I regenerated it into the scratchpad. The output
     differs from the committed file in two places, and the generator puts back "the governor … with its 500 ms
     threshold", which is the wording the image retired in round 8. So the next regeneration would make the method
     page contradict the image.
   - Its title, its "Honesty conventions" and its token and role tables describe retired sheets in the theme's own
     words: "how the chart is drawn", "the ship's log paper", "islands, coast", "water under 10", "red lateral marks",
     "light flares and halos (chart magenta)", "the flashing core of a light", "hatch ink for the unsurveyed band",
     the `sea-name` role, "Doubt marks follow chart practice", "the rustmapper → Scrapy channel is pecked and unlit",
     "the pencil-note edition", "the survey clones every public repository". A visitor who checks the method gets
     exactly the "too on the nose" vocabulary the owner cut, plus conventions for marks that aren't drawn.
   - Google's documentation guide calls this dead documentation: "Dead docs are bad. They misinform", and "First
     delete what you're certain is wrong" [S3]. NOAA's magenta line is the same failure: a route line nobody updated
     for 70 years that led boats into shoals [S9].
   - What to build:
     - Title "# How the picture is drawn". Move the "Generated by" line into an HTML comment (`<!-- … -->`), so it
       still tells a maintainer and isn't a "generated by" line a visitor reads.
     - Open with what the data line's link promises, at most 120 words, in short sentences: what each row is, that
       a row is drawn only when its anchors hold at HEAD and in the 0.1.3 sdist, and that the install and stop rows
       are drawn only when the run check passed. Split today's one 300-word "The idea" sentence into short ones.
     - Write that paragraph from the drawn route, not as fixed prose: the fetch row's wording comes from
       `routes.rustmapper` (the `wording` that `route.resolve` records), so it can't go stale again.
     - Delete "Honesty conventions" and "Motion". They describe sheets that aren't on the page.
     - The token and role tables list only what the hero draws with (paper, ink, ink2, muted, flare, accent, hair;
       display, label, project, machine), with plain uses: flare "the track to follow", accent "the dotted line round
       the 0.1.3 catch". The supporting sheets' tokens stay in `tokens.py` and get one line: "Other tokens serve sheets
       not on the profile."
     - In the Actions playbook, "survey" becomes "data step" and "the pencil-note edition" becomes "the edition
       drawn from cached figures".
   - Check: a new fast-tier rule, DESIGN-FRESH. It fails when `DESIGN.md` differs from `tokens.py --md` output, or
     when DESIGN.md matches the T-WORDS list plus "ship's", "islands", "lateral", "soundings", "unsurveyed",
     "pecked", "datum" or "survey" outside code spans.

2. **C1: take the colon out of the sentence** (`chart.toml` C1 `text`, `:751`; PURPOSE C1 in `sheets/route.py:90`;
   the C1 text in any test that pins it. The anchors stay as they are, since they test the code, not the drawn
   words.)
   - Today it reads "a second press before `Saved to:` quits without writing the file". The colon is the tool's own,
     but in mid-sentence it reads as a label with a value: "Saved to: quits without writing the file". That's the
     one line where a stranger is told what not to do, and it parses wrong at a glance on the phone, where it starts
     the second line.
   - Google's style guide quotes UI text without its ending punctuation, as with an ellipsis: "leave out the
     ellipsis" [S6]. Do the same with the colon.
   - New text: "press Ctrl-C once; a second press before the `Saved to` line quits without writing the file". It's 8
     characters longer. Desk: it stays one line, ending near 792 px of 832. Phone: it may go to three lines (+34
     units, 1,121 → 1,155, inside the 1,246 gate).

3. **H1: "when", not "once", next to "Ctrl-C once"** (`chart.toml` H1 `text`, `:715`; PURPOSE H1; one test.)
   - The two adjacent rows read "…done once `Received work item` lines stop for 60 s" and "press Ctrl-C once". That's
     the same word in two senses, one line apart: "as soon as" and "one time". Round 10 kept "once … once" out of the
     code comment for this reason (LOG round 10, declined r2-1). The image still has it.
   - Microsoft: "once: Don't use as a synonym for *after*" [S1]. Google: "If you mean *after*, then use *after*
     instead of *once*" [S2].
   - New text: "{release} never exits by itself; done when `Received work item` lines stop for {quiet} s". Same
     length, same lines on both sheets. STRINGS-TWICE: the five-word runs against the comment ("…: when" /
     `"Received work item" stops` / "for 60 s, then Ctrl-C once") don't match ("when received work item lines" vs
     "… stops"). Run the check anyway.
   - Test: across the drawn rows, "once" appears only in C1.

4. **Scrapy bullet 2: credit each job to the right tool, and say what the summary is** (`README.md`, hand-typed
   Scrapy bullet 2; one `[[figures]]` row for "five", `repo = "Scrapy"`, the literal
   `"extractive_max_sentences": 5` in `src/core/constants.py`.)
   - "Near-duplicates are dropped by URL hash and MinHash" gives a URL hash a job it can't do. In
     `_deduplicate_documents` a repeated `url_hash` is skipped (an exact repeat), and MinHash LSH drops pages whose
     text is close. The IR textbook makes the same split: a fingerprint catches exact duplicates, and it "fails to
     capture … near duplication", which needs shingling [S4]. A data engineer reading the bullet will spot it.
   - "an extractive summary" is true but sounds like more than it is. The code keeps the first five sentences, split
     on ".", cut at 1,000 characters. Saying so is more honest and costs four words.
   - New text: "Repeat URLs are dropped by their hash, near-duplicate pages by MinHash. In stage 3 a page's summary is
     its first five sentences; documents over 50,000 characters go to stage 4, where bart-large-cnn runs on the worker
     itself, so nothing is sent to an external API." That's +3 words, and about one more line at 390.

5. **Name the data tools in the fold's label** (`README.md:99`, the hand-typed `<summary>`; one test.)
   - "15 more repositories: Swift widgets, a C game engine, games, tooling" leaves out the largest group in the fold,
     the scrapers and data tools: FashionDB (scrapes Reddit and the web), Data-visualizer, Elusive_trades_data,
     mlx_Qwen_data_entry, MLX_convertion and Course_crusader (a university course-catalog scraper, `README.md:3`).
     That's 6 of 15, against 4 Swift, 3 games and 1 engine. Those six back up "CRAWL AND DATA INFRASTRUCTURE", and the
     label tells a screener the fold is games. A summary is the scent a reader uses to decide whether to open it.
   - New text: "15 more repositories: scrapers and data tools, Swift apps, games, a C game engine". At 390 it is still
     two lines.
   - Test: the summary names the group with the most members (a small table in `chart.toml` or the test itself).

6. **Rule 3's title says what its body proves** (`chart.toml [[notices]]` n = 3 `title`; one test string.)
   - "Measure from the start." Then: "Metrics were exported 6 days after the first commit". A careful reader sees the
     title and the evidence disagree by six days. That's the owner's "doesn't look exactly accurate", in a heading.
   - New title: "Measure in week one." Day 6 is in week one, and the dashboard on day 11 is "5 days after that".
     It's the same length, and the body is unchanged.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page this is | keep | |
| Role, two caps lines | crawl and data infrastructure; Python and Rust | keep | the route under it proves both halves |
| Empty left column (desk) | nothing, on purpose | keep | the route is what you read |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project, what it makes | keep | still the best sentence on the page |
| Start bar | where you begin | keep | |
| `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old the release is | keep | |
| Magenta track | one way through, top to bottom | keep | a real route convention, never named [S9] |
| Stop rings | each is a step the tool takes | keep | |
| S1 "`rust_sitemap crawl` starts from your URL; by default also from sitemaps, certificate logs and Common Crawl" | the command, and that it finds URLs without links | keep | |
| F1 "fetches up to 20 pages at a time from each host; queues their links to your site, its subdomains and its parent domain" | the loop's work and its reach | keep | "queues their links to your site" can read as sending links to your site; the reach is checked at a dot boundary, so it's true. Note 1 |
| W1 "logged to disk, then saved to redb, in batches" | it saves as it goes | keep | it still has no subject (round 7 noted it); note 2 |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| Gap in the track under the loop | Ctrl-C is the only way out | keep | |
| H1, red dotted box | the 0.1.3 catch and the number that clears it | change | must-fix 3 |
| C1 "press Ctrl-C once; …" | your one step, and the press not to make | change | must-fix 2 |
| End bar + `data/sitemap.jsonl` + fields | what you get, in the struct's names | keep | |
| Hand-off arrow + "sorted 21 ways by ideal-url-organizer" | his projects feed each other | keep | |
| Night editions | the same | keep | contrast holds by eye |
| Phone editions (390, 308) | the same, in one screen | keep | |
| Alt text | install, loop, stop, file | keep | |
| Link on the image to the repo | where the project lives | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Link line | where to go | keep | |
| "Ben Russell builds …" | what he builds | keep | |
| Languages | what he writes in | keep | |
| Stack | what he builds on | keep | |
| Pick sentence | which tool for which job | keep | |
| rustmapper facts line | which commit, deps, tests, CI gates, size | keep | note 3 on its shape |
| Wheel note | whether pip just works on your machine | keep | |
| "Before you run 0.1.3:" + 7 items | what it does to a server, what it can't see, what the file leaves out | keep | "asks no one" is the right kind of dry |
| rustmapper code block + stop comment | how to run and stop it | keep | |
| Scrapy sentence | his crawl system, not the framework | keep | |
| Scrapy facts line | alive, tested, measured | keep | |
| Scrapy bullet 1 (Delta Lake) | how pages are stored | keep | a noun pile, but every noun is checkable |
| Scrapy bullet 2 (dedupe, summaries) | what happens to a page | change | must-fix 4 |
| Scrapy bullet 3 (metrics, deploy) | how it's watched and shipped | keep | |
| Scrapy run sentence | what `start.py` starts, needs and loads | keep | |
| Scrapy code block | how to start it on your site | keep | |
| Grafana note | where to look | keep | |
| Also (four lines) | four more projects, each by what it does | keep | |
| 15 more (summary label) | what's in the fold | change | must-fix 5 |
| 15 more (contents) | the rest | keep | the game_engine line stays the page's one joke |
| Working rule 1 | he keeps one bad host from stalling a crawl | keep | |
| Working rule 2 | he keeps raw data, and why | keep | |
| Working rule 3 | he measures in the first week | change | must-fix 6 |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn, how it was run, who wrote the code | keep | its link is must-fix 1 |
| Licence line | the profile's terms | keep | |
| DESIGN.md (one click away, linked as "drawing") | how the picture is checked | change | must-fix 1 |

## Notes (true, not ranked)

1. F1, if it is ever rewritten for another reason: "queues the links that stay on your site, its subdomains or its
   parent domain" says where the links point. Not worth a phone line on its own.
2. W1 has no subject, so on the desk the row reads as if the crawler is what's logged. Purdue's fix for a dangling
   modifier is to "name the appropriate or logical doer" [S7]: "each result logged to disk, then saved to redb, in
   batches". It costs a second phone line (+34 units). Do it if the phone has room after must-fix 2.
3. The two facts lines don't match in shape: "**rustmapper** · *on main at …*" against "*On main at …*". Each has a
   reason (rustmapper has no lead sentence), so leave it.
4. Serial commas: the page leaves them out about a dozen times and uses one twice ("raw-first storage, and the
   dashboards"; the alt text's "with each page, and how to stop it"). Google uses the serial comma [S8]. Either way
   is fine, but the page should pick one. Dropping those two commas is the smaller change.
5. "Ctrl-C" against the tool's own "Press Ctrl+C again to force quit". Both style guides write a plus sign, and
   Google says "Don't use *Ctl-S*" [S2]. Terminal users write "Ctrl-C", and the page is consistent with itself.
   Leave it.
6. On the theme: leave it exactly where it is. Testing and restraint both point the same way. NN/g warns that for
   users already frustrated "a humorous tone might be irritating" [S10]. The cautions list is where a stranger is
   most likely to be annoyed, and it rightly has no jokes.

## Sources (new this round)

1. [S1] Microsoft Writing Style Guide, "once": "Don't use as a synonym for *after*."
   https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/o/once
2. [S2] Google developer documentation style guide, word list: "once": "If you mean *after*, then use *after* instead
   of *once*"; keyboard commands: "Don't use *Ctl-S*, *Cmd-S* …". https://developers.google.com/style/word-list
3. [S3] Google documentation guide, "Documentation best practices": "Dead docs are bad. They misinform …"; "First
   delete what you're certain is wrong"; "Cut out everything unnecessary, including out-of-date, incorrect, or
   redundant information." https://google.github.io/styleguide/docguide/best_practices.html
4. [S4] Manning, Raghavan and Schütze, *Introduction to Information Retrieval*, §19.6 "Near-duplicates and shingling":
   a fingerprint finds exact duplicates and "fails to capture … near duplication"; shingling does that.
   https://nlp.stanford.edu/IR-book/html/htmledition/near-duplicates-and-shingling-1.html
5. [S5] Mailchimp Content Style Guide, "Voice and tone": "Our humor is dry … straight-faced, subtle"; "don't go out of
   your way to make a joke—forced humor can be worse than none at all"; "If you're unsure, keep a straight face."
   https://styleguide.mailchimp.com/voice-and-tone/
6. [S6] Google developer documentation style guide, "UI elements and interaction": "If a UI element name ends with an
   ellipsis (...), leave out the ellipsis"; text the user types goes in code font.
   https://developers.google.com/style/ui-elements
7. [S7] Purdue OWL, "Dangling Modifiers and How to Correct Them": "a word or phrase that modifies a word not clearly
   stated"; fix it by naming "the appropriate or logical doer of the action".
   https://owl.purdue.edu/owl/general_writing/mechanics/dangling_modifiers_and_how_to_correct_them.html
8. [S8] Google developer documentation style guide, "Commas": "use a comma before the final *and* or *or*".
   https://developers.google.com/style/commas
9. [S9] NOAA Office of Coast Survey, "Coast Survey to improve 'magenta line' on Intracoastal Waterway nautical
   charts" (Jan 2014): removal began "after receiving reports of groundings by boaters who followed the line into
   shoals"; "Charts rarely recorded updates of the magenta line in the ensuing 70 years"; it becomes "an advisory
   directional guide". https://nauticalcharts.noaa.gov/updates/?p=1343
10. [S10] Nielsen Norman Group, "The Four Dimensions of Tone of Voice": serious vs. funny; for frustrated users "a
    humorous tone might be irritating"; "test". https://www.nngroup.com/articles/tone-of-voice-dimensions/
11. [S11] Federal Register, 26 Sep 2013, NOAA request for comments on the Intracoastal Waterway magenta line (the
    notice behind S9). https://www.govinfo.gov/content/pkg/FR-2013-09-26/pdf/2013-23515.pdf
12. [S12] GitHub Docs, "Managing your profile README": GitHub will "display your profile README on your profile page";
    nothing else in the repository is shown, so DESIGN.md is reached only through the link.
    https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme

Clones and data: `assets/stats.json` (`edition`, `repos[]`, `rules[]`, `handoffs[]`, `runcheck.rustmapper.steps`);
sdist 0.1.3 `src/state.rs:285`, `src/url_utils.rs:81-91`, `src/bfs_crawler.rs:433`, `src/main.rs:539, :704`; Scrapy
`96e7a1a` `Scraping_project/src/stage3/stage3_worker.py:22, :148-198`, `src/core/constants.py:83`,
`src/core/config.py:389`, `config.yml:227`; Course_crusader `d1266cf` `README.md:3`, `docs/SCRAPER_STATUS.md`;
`scripts/tokens.py:135, :153-200, :242`; `DESIGN.md` against `python3 scripts/tokens.py --md` (diff at lines 13-18);
`chart.toml:715, :751`; `scripts/checks/strings.py:67-72` (TWICE_WORDS 4). Also measured: word-set Jaccard between
the 20 longest READMEs in the clones (first 1,000 words, as stage 3 reads them) is at most 0.13, with a median of
0.06, so the 0.3 threshold does mean near-duplicate and the bullet's "near-duplicate pages" holds.
