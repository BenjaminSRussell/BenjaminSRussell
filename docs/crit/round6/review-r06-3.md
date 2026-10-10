# Review round 6, reviewer 3: the student on a phone

10 Oct 2026. I'm 19 and study CS. I look at GitHub on my phone, and I screenshot things to send to friends when
they're worth it. What I looked at: every PNG in `scratchpad/r6/build/round-05/` (the sheet on desk and phone, day and
night, and the page on desk, screens 1 and 2, and phone, screens 1 to 5). I read `README.md`, `SPEC.md`, `LOG.md`
(round 5) and all earlier reviews, including `review-r06-1.md` from this round. Anything already fixed, or already
raised this round, isn't repeated.

I also did what nobody had done yet. I opened the **live** `github.com/BenjaminSRussell` in a headless browser with an
iPhone user agent, at eight widths, and measured where GitHub actually puts the image and how wide it is
(`scratchpad/r6/r06-3/ghw.mjs`, `ghw2.mjs`, `gh390.mjs`, screenshot `gh390.png`). Those numbers drive my top two
findings.

Verdict: **not yet. 7 / 10.** The image has a purpose now. It's a cheat sheet for a real tool: how to get it, what it
does to each page, the one catch, how to stop it, and what file you get. I'd send that to a friend who asked how to
get every URL on a site, and the `pip install rustmapper` line means the screenshot carries its own way back to the
project. That's the best test a picture can pass with me. But "reads on a phone" is part of the owner's goal, and on
a real phone the image is smaller than the build thinks. On an iPad it's unreadable.

## The first question: does it meet the goal?

Mostly, for the image's content. Every row is a step the tool really takes, in order, from the release pip installs.
Nothing has a size. No word names the theme. To me it doesn't look nautical at all. It looks like a clean flowchart,
or a metro line, in a strong magenta. I think that's right: the owner said it should "act like it doesn't know that it
is". A sailor will catch the manner, and nobody else has to.

Where it fails the goal is the phone, which the owner called "a very common one":

1. **On a real iPhone the image is 308 px wide, not 390.** GitHub's mobile profile puts the README inside a bordered
   box with padding. Measured on the live page, the image is always the viewport minus 82 px: 278 px at 360, 293 at
   375, 308 at 390, 332 at 414, 348 at 430. It starts 674 px down the page, under GitHub's own header, bio,
   achievements and tabs. The build's phone check (`scripts/checks/route.py:56`, `PHONE_SCREEN = 390`) and the
   preview harness (`.md{padding:16px}`, a 358 px image) both assume a wider image. So the phone sheet's 26-unit text
   is **11.1 px at 390 and 10.0 px at 360**, not the 14 px the spec promised (SPEC §7, render tier). The page's own
   text right under it is 14 px (measured `font-size` of `.markdown-body`). Apple's floor for any text is 11 pt and
   its body default is 17 pt [S5]. At 360, Android's most common width after 414 [S3], the image's text is under that
   floor. Every review so far has judged a 358 px picture that no phone shows.

2. **On a tablet the desk sheet is served at 398 to 641 px, and its text is 6 to 9.5 px.** The `<picture>` switches on
   `max-width: 767px` (`chart.toml:9`). But GitHub switches to its two-column profile at 768 (Primer's `md`
   breakpoint [S2]), and the README column there is the viewport minus 370: 398 px at 768, 450 at 820, 641 at 1011.
   From 1012 to 1279 it's the viewport minus 434 (578 to 845), and from 1280 it's capped at 846. The desk sheet is
   1280 units wide with 19-unit text. So an iPad in portrait (768×1024 is the most common tablet size, 820×1180 is
   third [S4]) gets **5.9 to 6.7 px text**, and a 1024-wide window gets 8.8 px. I rendered the desk frame at 398 px
   (`scratchpad/r6/r06-3/desk-at-398-2x.png`). The route rows are a grey smear. The phone sheet at the same 398 px
   would be 14.4 px.

3. **The row that would make me screenshot it doesn't say why it matters.** S1 reads "your URL, plus by default
   sitemaps, certificate logs, Common Crawl". I didn't know what certificate logs give you, and most people won't. In
   the code, the CT seeder yields `https://{subdomain}/` for every subdomain it finds on crt.sh (sdist
   `src/ct_log_seeder.rs:327`, HEAD `:352, :393`). Common Crawl gives every URL it has indexed under `*.domain`
   (`common_crawl_seeder.rs:185`). A sitemap lists pages that internal links may never reach [S9]. So the point is
   that **it finds pages without following links**. Most crawlers can't, and that's the one thing on the image I'd
   tell a friend. Right now it's a list of nouns.

What is good and should stay exactly as it is:

- **The name in the image.** On the phone it repeats GitHub's "Benjamin Russell" header 100 px above. That repeat
  is fine, because a screenshot loses GitHub's header and keeps the image. Screenshots are mostly social and taken on
  the go, to bookmark or pass on a compact piece of something [S6]. The name and role line are what make a cropped
  screenshot say whose work it is.
- **`pip install rustmapper` as the first line of the route.** In a screenshot it's the search term and the link
  back.
- **One image, one project.** I can read it in one phone screen. The old islands picture didn't tell me anything.
  This one does.

## Figures checked

Against `assets/stats.json` (taken 2026-10-10), the 0.1.3 sdist (`scratchpad/r6/sdist013/rustmapper-0.1.3`) and the
Rust-sitemap clone at `32c2651`.

| Printed | Source | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `edition.date`; four uploads 0.1.0–0.1.3, all 8 Nov 2025 | yes |
| your URL, plus by default sitemaps, certificate logs, Common Crawl | sdist `cli.rs:58` `default_value = "all"`; seeders as above | yes (wording, finding 3) |
| fetches fewer pages at once when saves average over 500 ms | sdist `main.rs:90` `THROTTLE_THRESHOLD_MS: f64 = 500.0`, `:113` vs `commit_ewma_ms` | yes |
| logged to disk, then saved to redb, every 50 ms | sdist `writer_thread.rs:11` `BATCH_TIMEOUT_MS: u64 = 50` | yes |
| 0.1.3 never stops by itself; done when `Received work item` lines stop | sdist `bfs_crawler.rs:433`; runcheck `ends_by_itself` false at 150 s, `quiet_after_last_page` ok | yes |
| press Ctrl-C once to write `data/sitemap.jsonl` | sdist `main.rs:519` force-quit string; runcheck `crawl_ctrl_c` ok, 3 lines, 2.0 s | yes |
| fields: url, depth, status_code, title, … | `handoffs[0].writer_fields_release` (15 fields) | yes |
| sorted by ideal-url-organizer, with a test | `handoffs[0]` `state: runs`, `does: sorted by`, `missing_fields: []` | yes (wording raised by r06-1 #3) |
| 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust | `repos[Rust-sitemap]`: 176; success at `head_sha` = `head.sha`; Rust 16,390 | yes |
| 1,920 tests · CI passed 8 Oct 2026 · MIT · 69k lines of Python | `repos[Scrapy]`: 1,920; success; MIT; Python 69,036 | yes |
| 3 min from a cold cache on a 4-core Linux x86_64 machine | runcheck `install`: median 171.4 s of 3 runs (168.2–174.3), 4 CPUs, cold | yes |
| up to 20 requests at a time to one host, 256 in all | sdist `state.rs:285` `max_inflight: 20`; `cli.rs:32` `"256"` | yes |
| 45 of rustmapper's 146 commits; 71 of Scrapy's 499 | `repos[].others`: Claude 45 / `all_hands` 146; jules 49 + Claude 22 = 71 / 499, dependabot's 8 left out | yes |
| 25 ways to sort | `figures[]` `25 ways`, glob `method_*.py`, measured 25, holds | yes |
| 15 more repositories | `repo_count` 22 − profile − 2 flagships − 4 Also | yes. GitHub's tab says 24, which is 22 plus two forks (Boxalarm-monorepo, ggml-viz), checked on the live page. Consistent |
| On main, a crawl stops by itself … | | misleading, raised by r06-1 #1; I agree |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose work this is, and it stays with a screenshot | keep | the only name that survives a crop [S6] |
| Role line, two caps lines | crawl and data infrastructure, Python and Rust | keep | the drawing proves both |
| Empty left column (desk) | nothing | keep | white space, not filler |
| "rustmapper" + "Crawls a site and writes one line for every page it reaches." | what the tool does, in one line | keep | the clearest sentence on the page |
| Start bar | where you begin | keep | it reads as "start" without a label |
| `pip install rustmapper` | how to get it; the search term in a screenshot | keep | |
| "0.1.3 · 8 NOV 2025" | the build you'd get is 11 months old | keep | honest, and next to its command |
| Magenta track | one path, read top to bottom | keep | reads as a metro line or flowchart to a non-sailor. That's fine |
| Stop rings | one step each | keep | |
| S1 seeds | today: a list of sources I can't place | change | say what they buy (must-fix 3) |
| F1 fetch and queue | the crawl loop and its scope | change | r06-1 #4 ("above or below it"); not repeated |
| G1 governor | it slows down when saving falls behind, at 500 ms | keep | the unusual design idea, with a number I can check |
| W1 write path | logged, then saved, every 50 ms | keep | |
| Loop bracket and up arrow | these rows repeat for every page | keep | a loop is the one thing the picture shows better than text |
| Gap in the track under the loop | no exit but Ctrl-C | keep | subtle, but closing it would be false for 0.1.3 |
| H1, red dotted box | the catch, and how to tell you're done | keep for now | true. It is also the most screenshot-able line, and it's a bug notice with his name on top. Its fix is r06-1 #2 (ship 0.1.4) |
| C1 "press Ctrl-C once to write `data/sitemap.jsonl`" | the one thing you do | keep | |
| End bar | where you end up | keep | |
| `data/sitemap.jsonl` + fields | what you get, in the struct's words | keep | |
| Hand-off arrow and label | his projects feed each other | keep the mark | label wording is r06-1 #3 |
| Night editions | the same, in dark mode | keep | GitHub's apps reportedly always ask for the light one [S7], and the `<img>` fallback is the day desk sheet [S8]. The day edition stands alone, so that's covered |
| Phone editions | the same in one screen | change | sized for a 390 px image, shown at 308 (must-fix 2) |
| Desk editions below 1200 px | — | change | served at 398–765 px on tablets and small windows (must-fix 1) |
| Link around the image | a tap opens the project | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image | above | change | must-fix 1–3 |
| Alt text | the route in 25 words | keep | |
| Link line | where to go next | keep | |
| Builds / Languages / Stack | what he builds, and with what | keep | a long tag list on the phone, but it's what a screener scans for |
| Pick sentence | which tool for which job | keep | the most useful two sentences under the image |
| rustmapper sentence | the Python API isn't released | change | r06-1 #5 (one description per screen); not repeated |
| rustmapper facts line | alive, tested, size, which commit | keep | |
| Install block | copyable commands, how to stop, the kill recovery | keep | |
| Wheel note | whether pip will just work, and the cost if not | keep | "3 min" is measured and it's the thing a student hits first |
| Load and 50,000 sentence | what it does to someone's server; the sitemap limit | keep | |
| M1 "On main …" | (claims) main is fixed | cut while the cargo gate fails | r06-1 #1; agreed |
| Scrapy sentence, facts, block, Grafana note, bullets | the second tool, measured, and how to run it | keep | |
| Also | the next four, each in one line | keep | go_go_go's line is the most interesting on the page for me |
| 15 more `<details>` | the rest, folded | keep | |
| Working rules 1–3 | how he works, each tied to a dated commit | keep | |
| Working rule 4 | as above, cited to Claude's commit | change | r06-1 #6; not repeated |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release is drawn; agent authorship per repository | keep | |
| Licence line | the profile's terms | keep | |
| (outside this repo) GitHub bio | "Scraping enthusiast and full stack developer" | change, owner | on a phone it's the first sentence above the image (measured), and it says something different from the role line (must-fix 4) |

## Must fix, ranked

1. **Serve the phone sheet to every column under 766 px** (`chart.toml:9` `breakpoint_px`, 1 line; a new check of
   about 30 lines in `scripts/checks/route.py`; tests).
   - Set `breakpoint_px = 1199`. Measured on the live page, a 1200 px viewport gives a 766 px column, where the desk
     sheet's 19-unit text is 11.4 px. Below that, the phone sheet is served: at 398 px (768 viewport) its text is
     14.4 px and its height about 560 px; at 765 px (1199) 27.6 px and about 1,080 px.
   - New HERO-COLUMN-PX (render tier). Store GitHub's measured column as a table in the check: viewport ≤ 767 → vw − 82;
     768–1011 → vw − 370; 1012–1279 → vw − 434; ≥ 1280 → 846. For every viewport from 320 to 1920 in steps of 1,
     take the sheet the `<source>` list serves and the smallest text run in that sheet, and fail if it's under 11 px.
     Today it fails at 768 (5.9 px) and 1024 (8.8 px). With the change it passes everywhere (lowest 10.0 at 360 today,
     12.0 after must-fix 2).
   - Note in DESIGN.md that the table was measured on 10 Oct 2026 and should be re-measured if GitHub changes the
     profile layout.
   - Why: 768×1024 is the most common tablet size and 820×1180 is third [S4]. Every iPad in portrait gets 6 px text
     today. "It has to be kind of accepting of all different formats."

2. **Size the phone sheet for the image GitHub actually shows** (`scripts/checks/route.py:56`; the phone sheet width
   in `scripts/sheets/route.py` / `tokens.py`; the preview harness; heights rebaselined).
   - Set `PHONE_SCREEN = 308` (the column at a 390 viewport, measured) and keep `MIN_PX = 13` at 308. Add a second
     floor of 11 px at 278 (the 360 viewport).
   - Narrow the phone sheet from 720 to 600 units, keeping every type token. The right limit moves from x 688 to
     x 568. Then 26 units is 13.3 px at 390, 14.4 px at 414 (the most common phone size [S3]), and 12.0 px at 360.
     Raising the phone roles from 26 to 31 at 720 wide gives the same result, if that's easier in `tokens.py`.
   - Expect about three more wrapped lines (S1, G1, the field list). Typeset it and rebaseline ROUTE-HEIGHT phone.
     The limit should be the height that keeps the image inside one screen at 308 px: at most 640 px on screen, so
     1,246 units at 600 wide.
   - Fix the preview harness to match the device: in `preview_phone.mjs`, `.md{padding:16px 41px}`, so the image is
     308 px at 390. Put a 360 px render in the standard set (`renderset2.py`) next to the 390 one.
   - Why: today the image's text is 11.1 px on the commonest iPhone width and 10 px on the commonest Android width
     [S3], under the page's own 14 px and at or under Apple's 11 pt floor [S5]. The gate passes only because it
     measures a 390 px image that doesn't exist.

3. **S1 says what the seeds buy** (`chart.toml [route.rustmapper]` S1 text and anchors; about 4 lines and a test).
   - Text: "your URL, plus by default URLs found without links: sitemaps, subdomains in certificate logs, Common Crawl".
     The fallback, when the release default isn't `all`, keeps the same words with "if asked" at the end, as today.
   - New anchors in both trees: `src/ct_log_seeder.rs` contains `format!("https://{}/", subdomain)` (sdist `:327`,
     HEAD `:352`, `:393`). Keep `cli.rs` `default_value = "all"` (release) and the three seeder files.
   - Size: two lines on the desk (+28 units: 543 → 571, under the 592 gate; with S2 drawn 607, so rebaseline to 620),
     and three on the phone at the new measure. Count it in must-fix 2's typesetting.
   - STRINGS-TWICE: the README today has no seeding sentence (no "certificate" or "Common Crawl" in it), so nothing
     repeats. Run the check anyway.
   - Why: "certificate logs" is a word most visitors can't place. What it means, a subdomain list from public CT logs
     [S10], and what sitemaps give, pages links may miss [S9], is the thing that sets this crawler apart. It's what a
     student would forward. Same facts, with the reason left in.

4. **Owner, outside this repository: change the GitHub bio** (profile settings, one field).
   - Today it reads "Scraping enthusiast and full stack developer". On a phone it's the first sentence on the page,
     about 400 px above the image (measured). Set it to the role line: "Crawl and data infrastructure, in Python and
     Rust."
   - Why: the image says one thing and the sentence right above it says another. Round 4's MASTERPLAN asked for this,
     and it still hasn't been done.

I agree with r06-1's must-fix 1 (cut M1 while the cargo gate fails) and 2 (ship 0.1.4). From my side, 2 also matters
because the red box is the line most likely to end up in someone's screenshot.

## Sources (new this round)

1. [S1] Live measurement, this review: `https://github.com/BenjaminSRussell`, rendered by Playwright Chromium with an
   iOS Safari user agent at 360, 375, 390, 414 and 430 (mobile), and 768, 820, 1011, 1012, 1024, 1100, 1199, 1200,
   1280, 1366 and 1440 (desktop). It records the image's `currentSrc`, x, y and width, and `.markdown-body`
   `font-size` (14 px on mobile). Scripts and screenshot are in `scratchpad/r6/r06-3/`.
2. [S2] Primer, "Size": breakpoints xsmall 320, small 544, **medium 768**, **large 1012**, **xlarge 1280**, xxlarge
   1400. These match the steps measured in S1. https://primer.style/foundations/primitives/size
3. [S3] StatCounter, mobile screen resolution, worldwide, August 2026: 414×896 13.63 %, 360×800 9.25 %, 390×844
   6.81 %. https://gs.statcounter.com/screen-resolution-stats/mobile/worldwide
4. [S4] StatCounter, tablet screen resolution, worldwide, July 2026: 768×1024 9.03 %, 820×1180 5.7 %.
   https://gs.statcounter.com/screen-resolution-stats/tablet/worldwide
5. [S5] Apple Human Interface Guidelines, Typography: iOS and iPadOS default 17 pt, minimum 11 pt. The live page's
   body didn't load for me; the figures are from a copy of Apple's table
   (https://glama.ai/mcp/servers/@tmaasen/apple-dev-mcp/blob/b82f0efe2115dc4539c83a2374a714a84aeb350a/content/universal/typography.md).
   https://developer.apple.com/design/human-interface-guidelines/typography
6. [S6] Cramer, Sang, Park, "Uses and Gratifications of the Screenshot in Human Communication: An Exploratory Study",
   *Electronic Journal of Communication* 29(1–2), 2019: a mostly college-age sample. Screenshots are social, frequent
   and taken on the go, and are used to bookmark information and to compact the useful part.
   https://researchprofiles.canberra.edu.au/en/publications/uses-and-gratifications-of-the-screenshot-in-human-communication-/
7. [S7] RodrigoTomeES, prefers-color-scheme-hack README: in GitHub's Android and iOS apps, `prefers-color-scheme`
   "always return[s] the light theme". https://github.com/RodrigoTomeES/prefers-color-scheme-hack
8. [S8] GitHub Blog, "How to make your images in Markdown on GitHub adjust for dark mode and light mode": the `<img>`
   fallback is used when no `<source>` media query matches.
   https://github.blog/developer-skills/github/how-to-make-your-images-in-markdown-on-github-adjust-for-dark-mode-and-light-mode/
9. [S9] Google Search Central, "What is a sitemap": on larger sites it's "more difficult to make sure that every page
   is linked by at least one other page", and "a sitemap helps search engines discover URLs on your site".
   https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
10. [S10] RFC 6962, Certificate Transparency (obsoleted by RFC 9162): "publicly logging the existence of Transport
    Layer Security (TLS) certificates as they are issued or observed", which is why a log search lists a domain's
    hostnames. https://www.rfc-editor.org/rfc/rfc6962
11. [S11] Venigalla, Chimalakonda, "An Empirical Study On Correlation between Readme Content and Project Popularity",
    arXiv 2206.10772, 2022: READMEs of popular projects are "well organised using lists and images". It's an
    association only, but it backs one image plus lists, which is what this page is. https://arxiv.org/abs/2206.10772

Clones: sdist 0.1.3 `src/cli.rs:24-68`, `src/main.rs:90,113,519`, `src/writer_thread.rs:11`, `src/state.rs:285`,
`src/ct_log_seeder.rs:67,158,327`, `src/common_crawl_seeder.rs:111,185`, `src/sitemap_seeder.rs:356,360`,
`src/bfs_crawler.rs:433`; Rust-sitemap `32c2651` `src/ct_log_seeder.rs:352,393`; `assets/stats.json` (`edition`,
`repos`, `handoffs`, `figures`, `runcheck.rustmapper`); `scripts/checks/route.py:56,262`; `scripts/render_readme.py:131-152`;
`chart.toml:9`; the live repositories tab (24 = 22 own + 2 forks).
