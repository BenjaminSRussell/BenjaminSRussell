# Review round 10, reviewer 2: information design and cartography

10 Oct 2026. Lens: Tufte, Bertin and the Admiralty drawing offices. I looked at every PNG in
`scratchpad/r6/build/round-09/`: the sheet on desk (870) and phone (390 and 308), day and night, and the whole page
on desk, at 390 and at 360. I read `README.md`, `SPEC.md`, `LOG.md` through round 9 and the round 1 to 9 reviews. I
don't repeat anything already fixed or already declined, unless I have a new reason.

Score: **8 / 10**. Meets the goal: **no**, by two small page faults, both buildable today. The image doesn't need
to change.

## The owner's goal, first

- **Every map and every element has a deep purpose.** The image does. It's a strip map of one route: install, the
  rows that repeat for every page, the one danger, the one thing you do, and what you end up with. That is the
  oldest honest use of a route map: show only what you meet along the way, in the order you meet it. Order is the
  strongest channel on the sheet, and it carries the one thing text can't: which rows repeat, and where the repeat
  never ends. Nothing has a size, so nobody has to ask what a size means.
- **It teaches something true and useful about his actual projects.** Yes. Every row is a property of rustmapper
  0.1.3 that I could check in the sdist or in the run check (table below). A stranger learns how it fetches, how far
  it reaches, that it saves as it goes, that it never stops by itself, how to tell it's done, and which key not to
  press twice.
- **Nothing chases a reason.** Yes, in the image. On the page, one important fact now has no text home at all:
  when to stop the crawl. The image is the only place it lives, and an image of text is the one place a screen
  reader, a search and a copy can't reach (must-fix 1).
- **Nothing announces the theme.** True. You have to know charts to see the magenta track, the danger line or the
  continuation arrow. No word says any of it.
- **Reads on a phone.** The image reads at 390 and at 308. The page around it breaks one of its two levers in half
  on common phone widths: `--workers 1` wraps as `--` / `workers 1` (must-fix 2).

## Figures checked this round

| Printed | Where I checked | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `stats.json edition` 0.1.3, 2025-11-08 | yes |
| up to 20 pages at a time from each host | sdist `state.rs:285` `max_inflight: 20` (the comment at `:240` says "default: 2", which is stale; the value is 20), checked at `frontier.rs:655` | yes |
| its subdomains and its parent domain | sdist `url_utils.rs:81-91` `is_same_domain`: equal, a subdomain of the base, or a suffix of the base | yes |
| `Received work item` | sdist `bfs_crawler.rs:433`, `eprintln!`: always printed to stderr, no log level needed | yes |
| quiet for 30 s | `routes.rustmapper` H1 `quiet` 30; probe `quiet_slow_page` ok (15.0 s gap, SIGINT 30 s after the last line, 3 of 3 pages) | yes |
| second press before `Saved to:` | probe `second_ctrl_c`: exit 1, no file | yes |
| fields `url, depth, status_code, title` | `SitemapNode`, both trees | yes |
| sorted 21 ways | `handoffs` state `runs`; `figures` 21 | yes |
| 176 tests | Rust-sitemap clone at `32c2651`: 161 `#[test]`/`#[tokio::test]` + 15 `def test_` = 176 | yes |
| CI passed 7 Oct 2026: tests, rustfmt · 16k lines | `repos[]` success 2026-10-07, gates `[tests, rustfmt]`, Rust 16,390 | yes |
| 1,920 tests · 8 Oct 2026: tests, ruff, mypy, bandit · 69k | `repos[]` 1,920, gates four, Python 69,036 | yes |
| 0.1.3 ignores `Crawl-delay` | sdist `frontier.rs:787` writes `crawl_delay_secs: None` for every host; no parser | yes |
| robots.txt only over https | sdist `robots.rs:19` `format!("https://{}/robots.txt")`; probe `robots_read` failed (never asked over http) | yes |
| 3 min, cold cache, 4-core Linux | run check install median 171.4 s, 4 CPUs | yes |
| coding agents authored 45 / 71, co-signed 1 / 30 | `agent_authored` total 297, per-repo rows as r09-2 checked | yes |

Every figure on the page holds.

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif display | whose work this is | keep | the title of the sheet; the image travels without GitHub's header (link previews, screenshots) |
| Role line, two caps lines | crawl and data infrastructure, in Python and Rust | keep | the route under it proves the first half |
| Empty paper under the role (desk) | nothing, on purpose | keep | quiet land makes the route read first |
| "rustmapper" + one-line header | which tool, what it gives you | keep | a pilot entry opens with what the place is |
| Start bar | where you begin | keep | the fixed point at the entrance |
| `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old that release is | keep | the edition date where you use it |
| Magenta track | one way through, top to bottom | keep | the line you follow, in the one colour kept for it |
| S1 ring: starts from your URL; by default also sitemaps, certificate logs, Common Crawl | where URLs come from, and who gets asked about your domain | keep | |
| F1 ring: up to 20 pages at a time per host; scope | the load one site feels, and how far it reaches | keep | the politeness fact, in the clause it belongs to |
| W1 ring: logged to disk, then saved to redb, in batches | it saves as it goes | keep | note 2: "logged" sits one row above a log line on the terminal; it's still plain and true |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one fact only a drawing gives |
| Break in the track under the loop | the loop has no exit but yours | keep | subtle, but it costs nothing and is never wrong |
| H1, dotted danger line: never exits; done once `Received work item` is quiet for 30 s | the catch in 0.1.3, and the mark that says you're done | keep the mark | a clearing mark with its number. Its fact needs a home in text too (must-fix 1) |
| C1 ring: press Ctrl-C once; second press loses the file | your one move, and what not to do there | keep | the point of commitment |
| End bar + `data/sitemap.jsonl` + fields | what you get, in the struct's own names | keep | |
| Thin continuation + arrowhead + "sorted 21 ways by ideal-url-organizer" | this output feeds another of his projects | keep | the only tested join, and the number agrees with the page |
| Night editions | the same in dark mode | keep | magenta and the danger dots hold on navy |
| Phone editions (600 wide; 390 and 308 on screen) | the same, in one screen | keep | 26-unit text is about 13.3 px at 308 |
| Alt text | what the image does, in 25 words | keep | it says "loops until one Ctrl-C", but not when (must-fix 1 fixes that in the block, not the alt) |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Link line | where to go | keep | |
| "Ben Russell builds …", Languages, Stack | what he builds, in what, on what | keep | |
| Pick sentence | which of the two tools for which job | keep | |
| rustmapper facts line | which commit, tests, what CI blocks on, size | keep | |
| rustmapper code block | how to install, run, stop and recover | change | its one stop line, "stop it with one Ctrl-C", doesn't say when. The image does, and only the image (must-fix 1) |
| Wheel note | will pip just work on your machine | keep | |
| "Before you run it:" + six items | what it does to a server, the two levers, what it can't see, what the file leaves out | change | right items. The levers split mid-flag on phones (must-fix 2) |
| Scrapy sentence, facts, three bullets | the second tool and the data-infrastructure evidence | keep | |
| Scrapy run sentence, block, Grafana note | how to start it | keep | |
| Also (four lines) | four more tools, each by what it does | keep | |
| 15 more | the rest | keep | |
| Working rules 1–4 | how he works, each with a dated cite | keep | note 3: rule 1 and rule 2 restate Scrapy bullets 3 and 1 |
| Found a mistake? | the page can be corrected | keep | |
| Data line | what was run, on what, and who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **The stop rule gets a text home, in the code block, where the reader acts.** (`scripts/render_readme.py`,
   `install:Rust-sitemap` block; about 15 lines and two tests.)
   - Today the block reads `# stop it with one Ctrl-C`. Nowhere in the page's text does it say that 0.1.3 never
     stops by itself, or how to tell when it's done. That fact is in the image only. Since round 9 it is also the
     image's only number a user acts on.
   - Replace that one comment line with three, all within the 32-character code width:

     ```sh
     # 0.1.3 runs until stopped: once
     # "Received work item" is quiet
     # for 30 s, press Ctrl-C once
     ```

     (32, 31 and 29 characters.) Build them from the H1 entry: `{release}` and `{quiet}` exactly as the image
     fills them, printed only while H1 is drawn with its quiet value. Otherwise fall back to today's line, and when
     H1 retires (0.1.4 stops by itself), print nothing. The `30` is covered by H1's existing AUDIT row.
   - STRINGS-TWICE: "Received work item" has no `_`, `--`, `.rs`, `.jsonl` or date, so the gate passes it. Still,
     add it to the allowlist next to `pip install rustmapper`, with this reason, so the next person doesn't "fix" it
     back.
   - Tests: (a) with H1 drawn and quiet 30, the block has those three lines and no line over 32; (b) with H1
     retired, the block has no "Ctrl-C" line about quiet and no "30".
   - Phone cost: two lines in the code block, about 48 px at 390.
   - Why: round 2 decided "the README text is the long description" of the image, which WCAG asks for when a short
     alt can't carry a complex image's information [S1]. One home per fact has since moved this fact out of the
     text, so that's no longer true for it. The code block is what people copy and come back to, and a warning
     belongs at the step where the hazard is, inside the procedure [S2]. Pilot books and charts work the same way.
     The pilot book carries in words what a navigator needs at the moment of action [S3], and a clearing line is
     useful only as a number you can check from where you stand [S4]. This doesn't repeat the image's other rows.
     It repeats the one instruction someone needs with their hand on the keyboard.

2. **Each lever starts its own line, so a flag never breaks in half on a phone.** (`render_readme.text_blocks`;
   about 10 lines, one fast test and one render test.)
   - Measured in Chromium (`scratchpad/r10-2/wrap.mjs`, the README item text, GitHub's 16 px body and 85 % mono
     code, side padding 16 and 41 px). `--workers 1` splits as `--` | `workers 1` at 320, 360, 412 and 430 px.
     The round-9 page render shows it at 360 as "hosts. -" / "-workers 1". `--seeding-strategy none` splits as
     `--seeding-` | `strategy none` at 320 to 430 at one padding or the other.
   - Change: where an item's second sentence opens with a code span (today L1's `--workers 1` and L2's
     `--seeding-strategy none`), join the two sentences with `<br>` instead of a space:

     > - It sends requests with no pause between them, up to 256 at a time across all hosts.<br>`--workers 1`
     >   sends one at a time.

     With the flag at the start of a line it never splits at any width from 320 to 430 (same harness: zero splits).
     At 390 each item keeps its four lines, or gains one at most.
   - Tests: fast tier, an item whose second sentence opens with a code span is joined with `<br>`. Render tier, a
     new check in the phone harness: at 320, 360, 375, 390, 412 and 430, no inline `code` that begins with `-`
     wraps before its first space (`Range.getBoundingClientRect` per character, as in `wrap.mjs`).
   - Why: a hyphen-minus is a soft wrap opportunity in CSS, and nothing in GitHub's sanitised Markdown can turn
     that off [S5]. U+2011 or a word joiner would break the flag when copied, which is why round 7 left
     `Crawl-delay` alone. A line break before the lever is a different fix: no hack, and the copied text is
     unchanged. The levers are the two lines a stranger types, so they are the two that must read cleanly. Google's
     style guide puts optional flags in the prose around a command, as this list does, and keeps them runnable [S6].
     A side effect is good too: both remedies now line up at the left edge, under their problems, where an eye
     scanning down finds them.

## Notes (true, not ranked)

1. **Desk type.** The route is set in a condensed face at 19 units, about 12.9 px in the 870 column. That's a little
   under GitHub's 13.6 px code text and well under the 16 px body text right below it. Narrower letters are harder
   to recognise, because neighbouring letters crowd them [S7]. It reads, and the floors hold. But if the desk
   layout is ever reopened, there is room: a 22-unit route with the track at x 420 fits every row today, and the
   empty left column pays for it. The cost is height (about 600, and over the 620 gate with S2 drawn). Not now.
2. **"logged to disk"** in W1 sits right above H1's `Received work item`, which is a log line on the terminal. A
   reader could look in the data folder for that line. It's plain and true, so keep it. Change it only if a test
   reader trips on it.
3. **Rules 1 and 2 restate Scrapy's bullets 3 and 1** (one host set aside for a minute, after 5 failures for 60 s;
   the raw layer that stays raw). The rules frame the facts as how he works, which is a different question, so both
   are kept. If the page ever needs phone lines back, rule 1's body is the first place to look.
4. **The strip map is the right form.** A schematic route that gives up geography for order and clarity is faster
   to use than a "true" one [S8], and the image keeps words and drawing together rather than putting the words in a
   legend [S9]. Nothing on this sheet would read better as a list.
5. **Owner, outside this repository (carried):** fix P1 so S2 can be drawn, ship 0.1.4, and the other items in
   LOG.md round 9. ROUTE-UNVERIFIED still fails on S2, and the image doesn't go to `main` until 0.1.4. That keeps it
   from shipping, whatever this review says.

## Sources (new this round)

1. [S1] W3C, *Understanding SC 1.1.1: Non-text Content*. For a complex image, use a short alternative plus a
   long description (G92) when "a short description can not serve the same purpose and present the same
   information". https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html
2. [S2] Clarion Safety Systems, *Understanding ANSI Z535.6*: embedded safety messages "apply to a particular step or
   instruction within a section or procedure".
   https://www.clarionsafety.com/safety-resources/machinery/understanding-ansi-z535-6-a-guide-to-safety-information-in-product-manuals-and-materials/
3. [S3] NOAA Office of Coast Survey, *United States Coast Pilot*: the volumes "contain supplemental information
   that is difficult to portray on a nautical chart." https://nauticalcharts.noaa.gov/publications/coast-pilot/index.html
4. [S4] OpenStreetMap Wiki, *Seamarks/Leading Lines*: a clearing line is "a straight line that marks the boundary
   between a safe and a dangerous area"; a line that doesn't project to marks you can see "isn't navigationally
   useful". https://wiki.openstreetmap.org/wiki/Seamarks/Leading_Lines
5. [S5] W3C, *CSS Text Module Level 3*, line breaking and `hyphens`: hyphen-minus is an "always visible" character
   that brings its own soft wrap opportunity, and `hyphens: none` "does not suppress" it.
   https://www.w3.org/TR/css-text-3/
6. [S6] Google developer documentation style guide, *Code syntax*: keep click-to-copy blocks runnable, and mention
   optional flags in the surrounding prose. https://developers.google.com/style/code-syntax
7. [S7] Readability Matters, on Oderkerk and Beier (VSS 2020), *Fonts of wider letter shapes improve recognition*:
   "extending fonts horizontally (increasing character width) increased letter recognition", by reducing "crowding
   interference from surrounding letters".
   https://readabilitymatters.org/articles/widened-letter-shapes-have-implications-for-improved-readability
8. [S8] Maxwell J. Roberts, in *The Psychologist* (BPS), "Going underground": schematic designs that break the
   conventions on principle "can result in designs up to 50 per cent faster for journey planning than official
   maps". https://www.bps.org.uk/psychologist/big-picture-going-underground
9. [S9] *Eye* magazine, review of Tufte's *Beautiful Evidence*: "evidence is evidence", whether words, images or
   numbers, and "too often these components of information become segregated".
   https://www.eyemagazine.com/review/article/information-overlord

Code and data: sdist 0.1.3 (`state.rs:228-300`, `frontier.rs:655`, `:775-795`, `robots.rs:19`, `url_utils.rs:81-110`,
`bfs_crawler.rs:433`), the Rust-sitemap clone at `32c2651` (test count), `assets/stats.json` (`edition`,
`routes.rustmapper` H1 `quiet`, `runcheck.rustmapper` steps, `repos[]`, `handoffs`, `figures`, `agent_authored`).
Measurement: `scratchpad/r10-2/wrap.mjs` (Chromium, widths 320 to 430, two paddings).
