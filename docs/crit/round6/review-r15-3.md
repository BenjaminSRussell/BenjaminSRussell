# Review round 15, reviewer 3: a 19-year-old CS student who lives on a phone

10 Oct 2026. I looked at every PNG in `scratchpad/r6/build/round-14/`: the phone sheet at 390 and 308 (day and night),
the desk sheet at 870 and 846 (day and night), the mid sheet at 746 (day and night), the README at 390 (six screens)
and 360 (seven), at 1,280 (two), and the first screen at 900, 1,180, 1,280, 1,366 and 1,920. I read `README.md`,
`SPEC.md`, `LOG.md` rounds 13 and 14, the round 13 and 14 reviews and `review-r15-1.md`, so nothing below repeats a
finding that is fixed or already raised this round. r15-1's three must-fixes (S2 on a 0.1.3 image, the publish
order, the Scrapy run sentence) are not repeated here, and I agree with all three.

How I read a profile: someone drops a `github.com/<user>` link in a Discord or a group chat, I tap it on my iPhone,
and if something is worth it I screenshot it and send it on. So I asked two questions. What does the first screen
teach me? And what does the screenshot still say once it has left GitHub, with no code block, no links and no
README under it?

Verdict: **not yet. 8 / 10.** The image is the best thing on the page and I would send it. It's one screen, it's
about his actual tool, and it shows the one thing a list can't: the crawl loops, and the catch sits inside the loop.
Nothing in it has a size, nothing is an island, and nothing names the theme. Every figure I checked is true (table
below). Three things stop me shipping it:

1. **The way I'd actually open this link may get the desk image at about 6 px.** On an iPhone with the GitHub app
   installed, a tapped `github.com/<user>` link opens in the app, not Safari. GitHub's own app-site-association file
   claims every remaining route for the app with a catch-all `*`, and a bare profile path matches nothing it
   excludes [S1]. Nobody has checked how the app picks from a `<picture>` (it has been on the owner's list since
   round 11). If it ignores the `<source>` lines, it shows the `<img>` [S2]. Since round 14 that `<img>` is the
   1,000-unit desk sheet, whose 19-unit words come out at 5.9 px in a 308 px column. The fix doesn't depend on the
   answer, and it costs about 20 lines. Must-fix 1.
2. **Rustmapper's name on the wire isn't on the page. Scrapy's is.** Round 14 told a visitor exactly what a site
   owner will see in their logs when they run Scrapy (`UConn-Discovery-Crawler/1.0`, then
   `Python/3.11 aiohttp/3.13.1`) and how to change it. Rustmapper, the tool the page tells you to run first, sends
   `RustSitemapCrawler/1.0` with no contact, and the flag that changes it is never mentioned. Must-fix 2.
3. **"elsewhere `pip` builds it from source" claims more than anything measured it.** The only source build that
   has ever run was on Linux x86_64. Many students run Windows, where "a Rust toolchain" also means Visual Studio's
   C++ build tools [S9]. Must-fix 3.

## The first question: does it meet the owner's goal?

- **A deep purpose for the one map.** Yes. It's the route a URL takes through rustmapper 0.1.3, in the order a run
  goes: install, start, the fetch loop, the catch inside the loop, the one key you press, the file, and the project
  of his that reads it. The loop bracket and the dotted box *inside* it are the two things a bullet list can't show:
  "this repeats" and "this is where it never ends". I got both in under ten seconds on the 390 render, before I'd
  read a word of the README.
- **True and useful about his actual projects.** Yes. Every line is a fact about 0.1.3 that changes what I'd do: the
  command is `rust_sitemap`, not the package name; it also asks certificate logs and Common Crawl unless told not to;
  it takes 20 pages at a time from one host; it follows links into subdomains *and the parent domain*; it never exits;
  pressing Ctrl-C twice loses the file. A friend I sent the screenshot to could run it right, apart from must-fix 2's
  courtesy and the `--start-url` flag (audit, S1 row).
- **Nothing chases a reason.** Yes, on the image. The start and end bars, the ring at each step, the arrow back up and
  the break in the line under the loop all carry a step or a state. On the page, every block either says what a
  project does, how to run it, or what it does to someone else's server.
- **Nothing announces the theme.** Yes. I looked for it on purpose: no sea words in the image, the alt text, the
  headings or the data line. The theme is only in the manner (one coloured line you follow, a dotted danger line
  round the catch, a dated note at the foot). If nobody told me, I'd call it "a really clean diagram".
- **Reads on a phone.** The image, yes: 575 px tall at 390 and 519 px at 360, one screen either way, day and night,
  13.3 px words at 390 (settled in rounds 6 and 14; I don't reopen it). Not in the app until must-fix 1 is done,
  because nobody knows what the app serves. The README is 5,109 CSS px at 390, about eight screens. That's long, but
  each screen starts with something I can tell apart (a bold name, a list, a code block), and the 15 other
  repositories are folded.
- **Would I ship it as is?** No: must-fix 1, plus r15-1's publish order.

## The screenshot test

I cropped the 390 day render to the image alone, the way a screenshot leaves GitHub, and read it as the friend I
send it to would.

| What the friend learns from the screenshot alone | Carried? |
|---|---|
| Whose it is | yes: "Ben Russell", the largest thing on it. That's why the name stays even though GitHub's header shows it too: the header doesn't go into the screenshot |
| What it is | yes: "rustmapper / Crawls a site and writes one line for every URL it finds." |
| How to get it | yes: `pip install rustmapper`, 0.1.3, and its date |
| How to run it | almost: `rust_sitemap crawl starts from your URL`. Typed as `rust_sitemap crawl https://…` it fails once. clap makes `start_url: String` a required option, and it can't be passed positionally [S8]. The error prints the usage, so it costs one retry (audit, S1 row) |
| What it will do to a site | partly: 20 at a time per host, subdomains and parent domain, three outside services by default. Not who it says it is (must-fix 2) |
| How it ends | yes: the dotted box, Ctrl-C once, and the file |
| What happens next | yes: "sorted 21 ways by ideal-url-organizer" |

That's a screenshot worth sending. I'd send it with "this guy's README tells you how his crawler breaks before it
tells you how it works", and from me that's a compliment.

## Figures checked this round

| Figure | Where printed | Checked against | OK |
|---|---|---|---|
| 0.1.3 · 8 Nov 2025 | image R2 | `stats.json edition.version`, `.date`; `uploads[3].time` 2025-11-08T19:52:41 | yes |
| `rust_sitemap` | image S1, code block | `edition.scripts`; sdist `src/cli.rs` `#[command(name = "rust_sitemap")]` | yes |
| sitemaps, certificate logs, Common Crawl by default | image S1 | sdist `src/cli.rs` `seeding_strategy` `default_value = "all"` | yes |
| up to 20 pages at a time from each host | image F1 (the `instead` wording) | sdist `src/state.rs:285` `max_inflight: 20`; `routes` F1 governor wording unverified in the release, so the cap is drawn | yes |
| 60 s | image H1 | `chart.toml` H1 `audit`: 30 + 20 + 4 + 1 rounded up; probe `quiet_slow_page` | yes |
| `Received work item`, `Saved to` | image H1, C1 | sdist `src/bfs_crawler.rs:433`, `src/main.rs:539`, `:704` | yes |
| 21 ways | image R15, Also | `ideal-url-organizer` README "Methods 1-21"; `handoffs` state `runs` | yes |
| 176 test functions | rustmapper facts | `git grep` at 32c2651: 161 Rust test attributes + 15 Python `def test_` = 176 (AUDIT row's definition) | yes |
| 16k lines of Rust | rustmapper facts | `repos[Rust-sitemap].lines.Rust` 16,390 | yes |
| CI passed 7 Oct 2026 | rustmapper facts | `repos[].ci` success, 2026-10-07, `head_sha` = 32c2651 | yes |
| 45 of its 146; 1 of his own 101 | rustmapper facts | full-history clone: 146 commits; shortlog Benjamin Russell 97 + BenjaminSRussell 4 = 101, Claude 45; 1 of his own with an agent trailer | yes |
| 71 of its 499; 30 of his own 420 | Scrapy facts | clone: 499; 420 his, jules 49 + Claude 22 = 71, dependabot 8 left out; 30 with an agent trailer | yes |
| 1,920 test functions; 69k lines | Scrapy facts | `repos[Scrapy].test_functions`, `.lines.Python` 69,036 | yes |
| 256 at a time | Before you run | sdist `src/cli.rs:32` `default_value = "256"` | yes |
| 3 min from a cold cache, 4-core Linux x86_64 | install note | `runcheck` install: median 171.4 s, 4 CPUs, empty `CARGO_HOME` | yes |
| 10 Oct 2026 (Linux x86_64) | data line | `runcheck.rustmapper.date`, `.runner` | yes |
| 15 more | details summary | 22 repositories (the profile repository included) less the 7 named | yes |

New facts behind the must-fixes, read in the 0.1.3 sdist and at Rust-sitemap 32c2651:

```
sdist src/cli.rs:37-41      #[arg(short, long, default_value = "RustSitemapCrawler/1.0", help = "User agent string for requests")]
                            user_agent: String,                       (Crawl; HEAD src/cli.rs:40, same default)
sdist src/network.rs:33     .user_agent(&user_agent)                  (the reqwest client sends it on every request)
sdist src/frontier.rs:680   matcher.one_agent_allowed_by_robots(robots_txt, &self.user_agent, &queued.url)
sdist src/network.rs        no From header anywhere; no URL or address in the default
sdist src/cli.rs:18-19      #[arg(short, long, …)] start_url: String  (required; -s or --start-url, never positional)
runcheck install            "sdist (built with Rust)", runner Linux x86_64; no Windows or Intel-Mac run exists
README <img>                hero-day.svg = the 1,000-unit desk sheet since round 14; 19 units × 308/1000 = 5.9 px
```

## Element audit: the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose work this is | keep | it's the one thing that makes a screenshot attributable once it leaves GitHub |
| Role line, two caps lines | he does crawl and data infrastructure in Python and Rust | keep | the first five words say what the picture under them is about |
| "rustmapper" + one-line header | which tool, and what it gives you | keep | read before any detail; the header's "every URL it finds" is checked by the run |
| Start bar | where you begin | keep | the entrance is found at once; costs nothing |
| `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the line that gets it, and that the release is 11 months old | keep | the age is the honest context for every catch below it |
| Ring + S1 "`rust_sitemap crawl` starts from your URL; by default also from sitemaps, certificate logs and Common Crawl" | the command, and the three outside services it asks by default | change (optional, not a must-fix) | the command is the screenshot's only runnable line and lacks its required flag [S8]. On the phone, `rust_sitemap crawl -s <URL>` fits one line, 28 mono characters ≈ 437 of the 480 units between `text_x` 88 and `right` 568. Then "starts there; by default also from sitemaps, certificate logs and Common Crawl". `-s` is clap's derived short for `start_url` [S8], unique in 0.1.3's `Crawl` |
| Ring + F1 "fetches up to 20 pages at a time from each host; queues their links to your site, its subdomains and its parent domain" | how hard it hits one host, and how far its scope reaches | keep | "parent domain" is the surprise in the whole image, and it's true (`base_domain.ends_with(url_domain)`) |
| Loop bracket with the arrow back up | the rows inside repeat for every page | keep | the one shape a list can't draw; at 308 px the arrowhead is small but it's on the side your eye starts from |
| Ring + W1 "saved as it goes; export works after a kill" | a crash doesn't lose the list | keep | probe `export_after_kill` passes; the wording claims no more than that |
| Dotted box + H1 "0.1.3 never exits by itself; done when `Received work item` lines stop for 60 s" | it hangs, and how you know it's done | keep | the most useful row on the page; the only red, inside the loop where it bites |
| Break in the line under the loop | you only get out by your own hand | keep | subtle, but it's true, it's never labelled, and it needs no legend |
| Ring + C1 "press Ctrl-C once; a second press …" | the one key, and how to lose the file | keep | probe `second_ctrl_c`: exit 1, no file |
| End bar + `data/sitemap.jsonl` + fields | what you get, by its real field names | keep | the names match the struct |
| Thin line, arrow, "sorted 21 ways by ideal-url-organizer" | his projects connect, and here's how | keep | the one join backed by reader code and a test |
| Paper colour, no frame | where the sheet ends | keep | nothing else is spent on it |
| `<a href>` round the picture | a tap opens Rust-sitemap | keep | on a phone the image is what a thumb hits first |
| `<img>` fallback (`hero-day.svg`, the desk sheet) | whatever a renderer shows when it ignores the sources | change | must-fix 1 |
| Alt text | the route in two sentences | keep | names the tool, the loop, Ctrl-C and the file |

## Element audit: the page

| Block | What a stranger learns | Verdict | Why |
|---|---|---|---|
| Link line `rustmapper · PyPI · Scrapy · Email` | where to go next | keep | four thumb-sized targets right under the image |
| "Ben Russell builds …", Languages, Stack | what he works in | keep | three lines; the Stack line is a lookup, and text is the right form for it |
| Pick sentence | which of his two crawlers to use | keep | one binary versus Docker is the real choice |
| rustmapper facts line | tested, alive, how big, how much is his | keep | every count checked above; the agent clause next to its own denominator is something I'd screenshot by itself |
| Install note | will pip just work on my machine | change | must-fix 3 |
| "Before you run 0.1.3:" (four open items) | what it does to someone else's server, each with its lever | change | must-fix 2 adds the fifth thing a site owner sees: the name |
| Fold "What 0.1.3's files miss or get wrong" | the data's limits | keep | folded on a phone, one line, opens when you care |
| Code block | the copyable commands | keep | the comments say the catch where you paste. `<your-site>` pasted as is is a shell redirect and errors out. Google's style guide prefers `YOUR_SITE` with a "Replace the following" list [S7], but the angle form is used across the whole page and the error is harmless, so I wouldn't change it this round |
| Scrapy sentence + facts line | his bigger system, measured the same way | keep | same form as rustmapper's, so they compare |
| Scrapy bullets (three) | what's inside: storage, dedup and summaries, operations | keep | each is a design choice a screener asks about |
| Scrapy run sentence + code block | how to start it and what it does to a site | change | r15-1 must-fix 3 (a "Before you run it:" list); not repeated here |
| Grafana / Delta line | where the output is | keep | the arrival, as the image's end bar is for rustmapper |
| Also (four) | his other work that touches the crawlers | keep | one line each, and each says what it does |
| "15 more repositories" fold | the rest exist | keep | folded; the summary names the kinds |
| Working rules (three) | how he works, each with the code that shows it | keep | each rule has a dated fact under it, so none of them is a slogan |
| "Found a mistake? Open an issue." | he wants to be corrected | keep | one line; fits a page this careful about truth |
| Data line | what the drawing was checked against | keep | the date and runner match `runcheck` |
| License line | reuse terms | keep | |

## Must fix, ranked

1. **Make the `<img>` fallback the phone edition, and give the desk its own `<source>`.**
   (`scripts/render_readme.py` `HERO_ROUTE_SOURCES` and the `<img>` line in `picture()`; `scripts/checks/column.py`
   `served()`; tests. About 20 lines.)
   - **What's wrong.** See point 1 above. A tapped profile link on an iPhone with the app installed opens in the app
     [S1]. The spec's rule is that a browser takes the first `<source>` whose media matches and otherwise uses the
     `<img>` [S2]. A renderer that ignores `<source>` therefore shows `hero-day.svg`, which since round 14 is the
     1,000-unit desk sheet: 5.9 px words and a 21 px name in a 308 px column. Before round 14 it was 1,280 units, 4.6 px.
     The app's behaviour has been an owner check since round 11 and is still unknown. The risk is lopsided: the phone
     sheet in a desk column is big but readable, while the desk sheet in a phone column can't be read at all.
   - **Change.** Sources, in order: mid night, mid day, phone night, phone day (as now), then
     `(min-width: {bp+1}px) and (prefers-color-scheme: dark)` → `night` and `(min-width: {bp+1}px)` → `day`, replacing
     today's bare `(prefers-color-scheme: dark)` → `night`. `<img src>` becomes `hero-phone-day.svg`. Every browser
     width from 0 to ∞ is still served by a `<source>`, so no browser render changes. Only a client that ignores
     `<source>` sees a difference, and it gets the edition made for the narrowest column.
   - **Gate.** `column.served()` must return the matching source at every width from 360 to 1,920 and never fall back
     to the `<img>`. Add a check, HERO-FALLBACK (fail): the `<img>`'s edition must be a phone edition, and its smallest
     text must be at least `MIN_PX` at `column_px(360)`. `publish_chart.unshipped` already makes sure every named file
     is on the `chart` branch.
   - **Test.** The rendered `<picture>` has six `<source>` lines and an `<img>` naming `hero-phone-day.svg`.
     `served(readme, vw)` equals today's edition at 360, 390, 851, 852, 1,199, 1,200 and 1,920. A README whose `<img>`
     is `hero-day.svg` fails HERO-FALLBACK.
   - **Owner, still:** open the profile once in the GitHub iOS app, light and dark, and note in LOG.md which edition
     it shows. If it honours the sources, nothing changes for anyone. If it doesn't, this fix is what keeps the image
     readable there.

2. **Say what rustmapper calls itself, and the flag that changes it.** (`chart.toml`, a new route entry `L6` after
   `L1`, `stage = "server"`, `short = "name"`; anchors; one test. About 15 lines. +2 lines at 390.)
   - **What's wrong.** See point 2 above. A crawler is supposed to say who it is: RFC 9309 asks that its product token
     appear in the User-Agent and that the identification string "describe the purpose of the crawler" [S3]. RFC 9110
     says a robot "SHOULD send a valid From header field so that the person responsible for running the robot can be
     contacted" [S4]. The crawlers people know put a contact URL in the string, as `CCBot/2.0
     (https://commoncrawl.org/faq/)` does, and site owners block them by that token [S5, S6]. 0.1.3 sends
     `RustSitemapCrawler/1.0`, sends no From header, and uses the same string to match robots.txt groups
     (`frontier.rs:680`). So a student running the README's command crawls under a name nobody can reach, and any
     `User-agent: RustSitemapCrawler` rules a site has written apply to them. Round 14 printed this fact for Scrapy.
     Leaving it out for rustmapper makes the safer-looking tool look safer than it is.
   - **Text** (open list, right after L1, the same `<br>` form L1 uses so the flag starts its own line and FLAG-WRAP
     holds at 360):
     "It names itself `RustSitemapCrawler/1.0`, with no way to reach you.<br>`--user-agent <your-bot>` sends your name
     instead."
   - **Anchors** (`release` and `head`): `src/cli.rs` block `Crawl` arg `user_agent` `equals = "RustSitemapCrawler/1.0"`;
     `src/network.rs` text `.user_agent(&user_agent)`; `src/network.rs` `absent = "header::FROM"`; and `absent` of
     `http` or `@` inside the default literal, so the words "no way to reach you" go red the day a contact is added.
     `audit`: "the default in `cli.rs`, set on the reqwest client in `network.rs`; no From header". No probe is needed
     to draw it, but `runcheck.py` can log the `User-Agent` its fixture server receives (one line in the handler), and
     `runs = ["ua_seen"]` then ties the text to a measured request.
   - **Size.** The open list goes from 4 items to 5 (`LIST_MAX_ITEMS` is 7), and the page about 60 CSS px longer at
     390. `<your-bot>` is already the page's placeholder for the same idea, so a reader recognises it.
   - **Test.** A fixture `cli.rs` whose default is `RustSitemapCrawler/1.0 (+https://…)` fails the row. The printed
     list has L6 right after L1, in stage order (`cautions_placed`).
   - **Owner, in Rust-sitemap (0.1.4 list):** default to `rustmapper/<version> (+https://github.com/BenjaminSRussell/Rust-sitemap)`
     and send a `From` when `--contact` is given. The row then rewords itself.

3. **Don't say "elsewhere" when only Linux was tried.** (`scripts/render_readme.py` `_wheel_sentence`, about 10
   lines; one test.)
   - **What's wrong.** See point 3 above. The sentence covers every platform without a wheel, and the run check has
     built from source only on `Linux x86_64` (`runcheck.rustmapper.runner`). On Windows, rustup's MSVC toolchain
     needs Visual Studio's "MSVC … C++ x64/x86 build tools" and a Windows SDK as well [S9]. "Needs a Rust toolchain"
     undersells that. And whether 0.1.3 builds there at all (pyo3 with `auto-initialize`, in a `bin` build) has never
     been tried. The standing rule is "never print a figure without a definition the audit stands behind". A
     platform claim is that kind of figure.
   - **Text, from the data:** "Prebuilt for Apple silicon on CPython 3.13. On Linux x86_64, `pip` builds it from
     source, which needs a Rust toolchain (3 min from a cold cache on a 4-core machine); other platforms were not
     tried." Build it from `edition.wheels` and `runcheck.rustmapper.runner`. When a run check passes on another
     runner, that runner joins the list and the tail goes once all three common platforms are covered.
   - **Test.** A `runcheck` with runner `Linux x86_64` gives the sentence above. Two runners (Linux, Windows) name
     both. No run check gives "`pip` builds it from source elsewhere; this was not tried."

## Sources (new this round)

The web-search budget for this turn was used up by the time I started, so these were fetched directly from primary
pages I knew of, or read in the clones. No search engine was queried another way.

1. [S1] GitHub, `https://github.com/apple-app-site-association` (fetched 10 Oct 2026; saved as
   `scratchpad/r15-3-aasa.json`): app IDs `VEKTX9H2N7.com.github.stormbreaker.prod` and `.dev`. 18 components. Profile
   paths are excluded only when they carry a `tab` query that isn't on the included list, and the last component is
   `{"/": "*", "comment": "Matches all remaining routes"}`. So a bare `/BenjaminSRussell` opens in the app.
2. [S2] WHATWG HTML Living Standard, *Images: selecting an image source*: "The user agent will choose the first
   `source` element for which the media query in the `media` attribute matches"; a non-matching source means
   "continue to the next child", and the `img` itself is the last candidate.
   https://html.spec.whatwg.org/multipage/images.html#selecting-an-image-source
3. [S3] RFC 9309, *Robots Exclusion Protocol*, §2.2.1: crawlers "set their own name, which is called a product token,
   to find relevant groups"; "the product token SHOULD be a substring in the User-Agent header"; "The identification
   string SHOULD describe the purpose of the crawler." https://www.rfc-editor.org/rfc/rfc9309.html
4. [S4] RFC 9110, *HTTP Semantics*, §10.1.2: "A robotic user agent SHOULD send a valid From header field so that the
   person responsible for running the robot can be contacted if problems occur on servers, such as if the robot is
   sending excessive, unwanted, or invalid requests." §10.1.5: "A user agent SHOULD send a User-Agent header field in
   each request." https://www.rfc-editor.org/rfc/rfc9110.txt (lines 4552-4555, 4661-4662)
5. [S5] Common Crawl, *CCBot*: user agent "CCBot/2.0 (https://commoncrawl.org/faq/)"; site owners block it with
   `User-agent: CCBot` / `Disallow: /`. https://commoncrawl.org/ccbot
6. [S6] Google Search Central, *Googlebot*: both Googlebot crawlers "obey the same product token (user agent token) in
   robots.txt", and a request claiming that name should be verified by reverse DNS.
   https://developers.google.com/search/docs/crawling-indexing/googlebot
7. [S7] Google developer documentation style guide, *Placeholders*: "Use uppercase characters with underscore
   delimiters", followed by a "Replace the following:" list that explains each one "even if the placeholder value is
   intuitive to you". https://developers.google.com/style/placeholders
8. [S8] clap, *Derive reference*: a bare `T` field is a "required argument" (`.required(!has_default)`), and `short`
   without a value "defaults to first character in the case-converted field name".
   https://docs.rs/clap/latest/clap/_derive/index.html
9. [S9] The rustup book, *Windows (MSVC)*: Rust needs "a linker, libraries and Windows API import libraries", which for
   `msvc` come from Visual Studio, at minimum "MSVC v143 - VS 2022 C++ x64/x86 build tools (Latest)" and "Windows 11
   SDK". https://rust-lang.github.io/rustup/installation/windows-msvc.html
10. [S10] Clones and release, read for this review: rustmapper 0.1.3 sdist `src/cli.rs`, `src/network.rs`,
    `src/frontier.rs`, `src/state.rs`, `src/bfs_crawler.rs`, `src/main.rs`, `PKG-INFO`. Rust-sitemap at 32c2651
    `src/cli.rs` and its full-history clone (`git shortlog`, the trailer count, test attributes). Scrapy at 96e7a1a
    (`git shortlog`, trailers). ideal-url-organizer at 159968a `README.md`. `assets/stats.json`
    (`edition`, `routes`, `handoffs`, `runcheck`, `repos`).
