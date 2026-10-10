# Review round 10, reviewer 3: the systems engineer

10 Oct 2026. Lens: someone who has shipped crawlers and storage engines and checks every printed claim against the
code. I looked at every PNG in `scratchpad/r6/build/round-09/`: the sheet on desk (870) and phone (390, 308), day
and night, and the whole page on desk, at 390 and at 360. I read `README.md`, `SPEC.md`, `LOG.md` through round 9,
the round 1 to 9 reviews and `review-r10-2.md`. I don't repeat anything already fixed or declined.

Score: **8 / 10**. Meets the goal: **no**. The image is the right picture. One of its rows has a hole in the
configuration a stranger actually runs, and one scope fact that bites most first crawls has no home anywhere.

## The owner's goal, first

- **Every map and every element has a purpose.** Yes. The sheet is a strip map of one run of rustmapper 0.1.3:
  the way in, the rows that repeat for every page, the one catch, the one key you press, and the file you get. Each
  row is a property of the tool you can check in the sdist. Nothing has a size, so nobody asks what a size means.
  The islands, the light and the axis the owner hated are gone, and nothing replaced them for decoration.
- **It teaches something true and useful about his actual projects.** Yes, with one exception. Every figure I
  checked holds (table below). The exception is H1's 30-second rule. The number came from a run check with seeding
  off, but 0.1.3 seeds by default, and the seeders print nothing that rule counts. Followed literally, the image's
  one actionable number can tell a stranger to stop a default crawl before it has fetched a page (must-fix 1).
- **Nothing chases a reason.** Yes. The loop bracket, the break in the track and the dotted danger line each carry
  a fact: which rows repeat, that the loop has no exit but yours, and where the catch is.
- **Nothing announces the theme.** True. No word names it. You have to know charts to read the magenta line you
  follow or the clearing line round the catch.
- **Reads on a phone.** The image reads at 390 and at 308. Review 2's flag-wrap fix covers the page.

## Figures checked this round (against `assets/stats.json` and the trees)

| Printed | Checked in | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `edition.date`; four uploads, all 8 Nov 2025 | yes |
| starts from your URL; by default also sitemaps, certificate logs, Common Crawl | sdist `cli.rs:58` `default_value = "all"`; `bfs_crawler.rs:195-212` | yes |
| up to 20 pages at a time from each host | sdist `state.rs:285` `max_inflight: 20`, enforced at `frontier.rs:655` | yes |
| your site, its subdomains and its parent domain | sdist `url_utils.rs:81-91`; base is the start URL's host (`bfs_crawler.rs:962` `extract_host`) | yes, but see must-fix 2 |
| `Received work item` | sdist `bfs_crawler.rs:433`, `eprintln!` | yes |
| quiet for 30 s | `routes.rustmapper` H1; probe `quiet_slow_page` ok | yes with seeding off; see must-fix 1 |
| second press before `Saved to:` | sdist `main.rs:519` and `:539`; probe `second_ctrl_c` exit 1, no file | yes |
| fields `url, depth, status_code, title` | sdist `state.rs:98-113` `SitemapNode` | yes |
| sorted 21 ways by ideal-url-organizer | `figures` 21 (`self.methods`); importer reads `sitemap.jsonl` (`scripts/import_rust_sitemapper.py:8`) | yes |
| 176 tests · 16k lines of Rust | clone at `32c2651`: 161 Rust attributes + 15 `def test_` = 176; 16,390 Rust lines | yes |
| 1,920 tests (CI selects all but 41) | clone at `96e7a1a`: 1,910 Python in collected files + 10 Rust in `kafka-delta-ingest/src/main.rs` = 1,920. CI runs no `cargo test`, so those 10 count in `outside` (16) | yes |
| 69k lines of Python | 69,036 | yes |
| CI passed 7 Oct / 8 Oct, gates | `repos[].ci` success, `gates` | yes |
| 45 of 146 · 71 of 499 · co-signed 1 and 30 | `Rust-sitemap.git`: 146 commits, 45 by Claude, 1 of his with an agent trailer. `Scrapy.git`: 499, 49 jules + 22 Claude = 71, 30 of his with an agent trailer | yes |
| up to 256 at a time across all hosts | sdist `cli.rs:32` `default_value = "256"` | yes |
| `sitemap.xml`, even after a kill | probe `export_after_kill` 3 `<loc>`. Export reads redb only, never the WAL (`main.rs:397`), so a kill can lose the last batch that is not yet committed (at most 50 ms of work). Fine for a comment. | yes |
| 3 min from a cold cache, 4-core Linux | `runcheck` install median 171.4 s, 4 CPUs | yes |
| 15 more | 22 repositories in `repos`, minus the profile, minus the 6 named = 15 | yes |
| Rule 3: 6 days, then 5 | `rules` prometheus 2025-10-01, grafana 2025-10-06, `repo_first` 2025-09-25 | yes |

## What I measured

**1. The startup is silent for longer than the image allows (seedprobe).** I served the three-page fixture
(`tests/fixtures/route-site/`) on 127.0.0.1 and ran the installed 0.1.3 binary
(`scratchpad/r6/runcheck/work/v/bin/rust_sitemap`) with **default seeding**:
`crawl --start-url http://localhost:<port>/ --data-dir d` (`scratchpad/r10-3/seedprobe.py`). Timestamps:

```
  0.6s Running 3 seeder(s)...
  0.6s Querying CT logs for domain: localhost ...
  1.3s CT log query returned 502, retrying in 1000ms (attempt 1/3)
  2.4s CT log query returned 502, retrying in 2000ms (attempt 2/3)
  4.5s CT log query returned 502, retrying in 4000ms (attempt 3/3)
  8.6s Seeder 'ct-logs' streamed 0 URLs
 14.9s Seeder 'common-crawl' streamed 0 URLs
 14.9s Crawler: Received work item: http://localhost:52479/ (depth 0)
```

The first `Received work item` came 14.9 s after start. That was the **fast** case: crt.sh answered 502 in under a
second each time (a plain `curl` of `crt.sh/?q=%25.toscrape.com&output=json` got 502 in 0.79 s too), and Common
Crawl failed on the network. The code allows a far longer silence. In `main.rs:552`,
`crawler.initialize(&seeding_strategy).await?` runs every seeder to the end before any shard worker starts. The CT
seeder makes up to four attempts at reqwest's 20 s total deadline (`--timeout` default, and reqwest's timeout runs
"until the response body has finished" [S6]) with 1 + 2 + 4 s of backoff between them: 87 s. Then it checks DNS
for every name it found, 100 at a time, up to 5 s for each batch (`ct_log_seeder.rs:10-16`). After that Common
Crawl gets its own requests. crt.sh's 502s and slow answers are well documented by its operator and its users
[S3, S4], and the Common Crawl index is "heavily rate limited" [S5].

So H1, "done once `Received work item` is quiet for 30 s", is true only after the first such line. Before it, the
line is "quiet" too. Someone who reads the image literally can press Ctrl-C at 30 s, during seeding, and get a
`sitemap.jsonl` that holds nothing.

**2. Seeds from certificate logs are dropped when you start at `www.`.** Both seeders query the root domain:
`get_root_domain(&start_url_domain)` (`bfs_crawler.rs:177`), crt.sh `%.{domain}` (`ct_log_seeder.rs:179`), Common
Crawl `url=*.{domain}` (`common_crawl_seeder.rs:185`). Every seed then passes through the shard's
`add_url_to_local_queue_unchecked`, which drops anything that fails `is_same_domain(url_domain, start_url_domain)`
(`frontier.rs:492`). The base is the start URL's **host**. From `https://www.example.com/`, `blog.example.com` and
`docs.example.com` are siblings. They are dropped, even when crt.sh lists them, and links to them are never
followed. From `https://example.com/`, all of them are in scope. Most people paste a `www.` URL. The image's F1
wording is true, but you have to know the code to see this in it. The page doesn't say it anywhere.

It's the same convention the reference crawlers follow, which is why the lever is worth printing. Heritrix
rejects `http://foo.org/` for a seed of `http://www.foo.org/` and says: "To allow every subdomain of foo.org, you
could use the seed http://foo.org" [S2]. Wget stays on the starting host unless it's told to span hosts [S9].

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose work this is | keep | the image travels without GitHub's header (previews, screenshots) |
| Role line, two caps lines | crawl and data infrastructure, Python and Rust | keep | the route under it proves the first half; Scrapy below proves the second |
| Empty left column (desk) | nothing | keep | quiet paper puts the route first; review 2 notes the room it leaves for later |
| "rustmapper" + header sentence | which tool, and what it gives you | keep | true: one JSONL line per node, including non-200s (X2) |
| Start bar | where you begin | keep | the fixed point at the entrance |
| `pip install rustmapper` + "0.1.3 · 8 NOV 2025" | the way in, and how old that release is | keep | the run check installs exactly this |
| Magenta track | one way through, read top to bottom | keep | one line, one path, in the colour kept for it |
| S1: starts from your URL; by default also sitemaps, certificate logs, Common Crawl | where URLs come from, and that third parties are asked | keep | true in 0.1.3. It is also why the startup is silent (must-fix 1) |
| F1: up to 20 pages at a time per host; queues links to your site, its subdomains, its parent domain | the load one host feels, and how far it reaches | keep | true. The lever that follows from it goes in text (must-fix 2), not here |
| W1: logged to disk, then saved to redb, in batches | it saves as it goes | keep | true; it's why `export-sitemap` works after a kill |
| Loop bracket + up arrow | which rows repeat for every page | keep | the one fact only the drawing gives |
| Break in the track under the loop | the loop has no exit but yours | keep | costs nothing, never wrong |
| H1, dotted line: never exits; done once `Received work item` is quiet for 30 s | the catch, and the mark that says you're done | **change** | the clock must start at the first line, not at launch (must-fix 1) |
| C1: Ctrl-C once; a second press before `Saved to:` loses the file | your one move, and what not to do | keep | matches the clig.dev rule: say what a second Ctrl-C will do when it is destructive [S1] |
| End bar + `data/sitemap.jsonl` + fields | what you get, in the struct's own names | keep | |
| Thin continuation + "sorted 21 ways by ideal-url-organizer" | this output feeds another of his projects | keep | the only tested join; 21 agrees with the Also line's "21 from the URLs" |
| Night editions | the same in dark mode | keep | |
| Phone editions (390, 308) | the same on one screen | keep | |
| Alt text | install, loop, stop | keep | its 25 words can't carry the rule; the text block will (review 2's must-fix 1) |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Link line | where to go | keep | |
| Builds, Languages, Stack | what he builds, in what, on what | keep | every stack item appears in a manifest or the image |
| Pick sentence | which tool for which job | keep | "no services to run" holds: Redis only with `--enable-redis` (sdist `cli.rs:63`) |
| rustmapper facts line | commit, tests, what CI blocks on, size | keep | all hold |
| Install code block | install, run, stop, recover | change | review 2's must-fix 1 puts the stop rule here; use must-fix 1's words below, not "is quiet" |
| Wheel note | will pip just work | keep | measured |
| "Before you run it:" + six items | load, robots, third parties, no JS, one sitemap file, what the file leaves out | change | the scope lever is missing (must-fix 2); the flag wrap is review 2's must-fix 2 |
| Scrapy sentence, facts, three bullets | the second tool and the data-infrastructure evidence | keep | |
| Scrapy run sentence, block, Grafana note | how to start it | keep | |
| Also (four) | four more tools by what they do | keep | |
| 15 more | the rest | keep | 15 holds |
| Working rules 1 to 4 | how he works, each with a dated cite | keep | dates hold; rule 4 cites his own commit |
| Found a mistake? | the page can be corrected | keep | |
| Data line | what was run, on what, and who wrote the code | keep | "with seeding off" is honest. It also says exactly where H1's number wasn't tested |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **H1's clock starts at the first `Received work item`, not at launch.** (`chart.toml [route.rustmapper]` H1
   text and anchors; `data/route.py` nothing new; the same words in review 2's code-block comment; about 10 lines
   and two tests.)
   - Image, desk and phone: "{release} never exits by itself; done once `Received work item` lines stop for
     {quiet} s". If `typeset` takes the phone row to a third line, use "…done once `Received work item` stops for
     {quiet} s", which is 3 characters shorter than today's. "Stop" says the lines were coming; "is quiet" doesn't.
   - New release anchors on H1, so the wording can't outlive the fact: `src/main.rs` contains
     `crawler.initialize(&seeding_strategy).await?` before the first `process_incoming_urls(` (seeders run to the
     end before any work item), and `src/bfs_crawler.rs` contains `Received work item`. An order anchor of this kind
     already exists for W1.
   - If review 2's must-fix 1 lands, its three comment lines become (each ≤ 32 columns):
     `# 0.1.3 runs until stopped: once` / `# "Received work item" stops` / `# for 30 s, press Ctrl-C once`.
   - Tests: T-WORDS/STRINGS unchanged. A fixture `main.rs` with the shard spawn before `initialize` leaves H1
     unverified. The H1 run on every edition stays within today's line count.
   - Not a probe: the run check rightly calls no third party, so the seeding delay can't be measured there. The
     anchor is the check. The data line already says the run was made with seeding off.
   - Why: a rule a navigator acts on has to hold from where they stand when they apply it [review 2's S4]. Here it
     doesn't hold during the first seconds of every default run, and I measured 14.9 s of silence in the fastest
     case. "If your program displays no output for a while, it will look broken" [S1]. The image shouldn't add
     "and it looks finished" to that.

2. **Print the scope lever: start at the bare domain.** (`chart.toml`, one new text entry on F1's existing scope
   anchors plus two; `README-CAUTIONS` cap from 6 to 7 items; about 15 lines and two tests.)
   - New item, release scope, after L2: "From `www.<site>` it skips sibling hosts such as `blog.`, even ones
     crt.sh lists. Start at the bare domain to take them all." (23 words, under the 25-word cap.)
   - Anchors (release and HEAD): `url_utils.rs` `is_same_domain`'s two branches (already F1's);
     `frontier.rs` `if !Self::is_same_domain(&url_domain, start_url_domain)` inside
     `add_url_to_local_queue_unchecked` (seeds are filtered there); `bfs_crawler.rs`
     `get_root_domain(&start_url_domain)` (the seeders ask about the root). Retire the item if any of them goes.
   - Cap: 7 is still inside the 2 to 7 range LOG round 9 cited. The phone cost is about 3 lines at 390.
   - Tests: the fast tier finds the item while the anchors hold; a fixture where `is_same_domain` takes siblings
     retires it.
   - Why: this is the one lever that decides how much of a site a first crawl reaches, and it fails silently. The
     tool asks crt.sh for every subdomain and then drops them. Heritrix documents the same trap and the same cure
     [S2]. Google's procedure guide says to give the reader context before the action [S7]. The list is the
     before-you-run-it context.

Review 2's two must-fixes (the stop rule in the code block, and each lever on its own line) I agree with as
written, with must-fix 1's words in place of "is quiet".

## Notes (true, not ranked)

1. **Text over pictures of text.** WCAG 1.4.5 prefers real text wherever it can do the job [S8]. The image is an
   image of text by necessity on GitHub. That's why each row the user acts on (install, stop, scope) needs a text
   twin in the block. The rows that only explain (W1, the loop) don't.
2. **`is_same_domain` takes every ancestor, not one "parent".** From `www.example.co.uk` the hosts `co.uk` and
   `uk` are in scope too (`url_utils.rs:88-90`). This is harmless in practice and "parent domain" is fair, so leave
   it. The fix is Ben's: use `get_registrable_domain` as the floor. Owner, outside this repository, next to the
   seeder fix carried from round 9.
3. **Owner, outside this repository, new:** have 0.1.4 print a line when seeding ends and crawling starts
   ("Seeding done: N URLs; crawling"), so the user doesn't need the rule above. clig.dev: "print something before
   you [make a network request] so it doesn't hang and look broken" [S1].
4. **The export after a kill** reads redb only (`main.rs:397`, no `WalReader`). At most the last uncommitted batch
   is lost. The comment "sitemap.xml, even after a kill" is fair at that size; don't add words.

## Sources (new this round)

1. [S1] *Command Line Interface Guidelines* (clig.dev): "Tell the user what will happen when they hit Ctrl-C
   again, in case it is a destructive action"; "If your program displays no output for a while, it will look
   broken"; "If you're making a network request, print something before you do it." https://clig.dev/
2. [S2] Heritrix user manual, *Common Heritrix Use Cases*: a `www` seed rejects `http://foo.org/`; "To allow every
   subdomain of foo.org, you could use the seed http://foo.org".
   https://archive-crawler.sourceforge.net/articles/user_manual/usecases.html
3. [S3] crt.sh Google Group, "crt.sh giving 502 BAD Gateway error" and "crt.sh slow and unusable for the past 24
   hours": the operator ties the 502s to overloaded front ends and to database queries cut off during replication.
   https://groups.google.com/g/crtsh/c/V16OrB494d4 · https://groups.google.com/g/crtsh/c/_xdEUGq_xwA
4. [S4] Let's Encrypt Community, "Crt.sh availability", 5 Aug 2026: crt.sh "frequently returns 502 Bad Gateway".
   https://community.letsencrypt.org/t/crt-sh-availability/250058
5. [S5] Common Crawl FAQ: "Our CDX API endpoint is frequently abused and therefore heavily rate limited"; on 503,
   "slow down your request rate". https://commoncrawl.org/faq
6. [S6] reqwest `ClientBuilder::timeout`: "applied from when the request starts connecting until the response body
   has finished". https://docs.rs/reqwest/latest/reqwest/struct.ClientBuilder.html
7. [S7] Google developer documentation style guide, *Procedures*: "Write in the order that the reader needs to
   follow"; give the context of an action before the action. https://developers.google.com/style/procedures
8. [S8] W3C, *Understanding SC 1.4.5: Images of Text*: "If authors can use text to achieve the same visual effect,
   they should present the information as text." https://www.w3.org/WAI/WCAG22/Understanding/images-of-text.html
9. [S9] GNU Wget manual (1.8.1), *Spanning Hosts*: recursive retrieval "normally refuses to visit hosts different
   than the one you specified on the command line"; `-H` / `-D` to widen.
   https://gnu.cs.utah.edu/Manuals/wget-1.8.1/html_node/wget_15.html
10. [S10] Measured here: `scratchpad/r10-3/seedprobe.py` on the run check's 0.1.3 binary (first work item at
    14.9 s with default seeding), and a direct `curl` of crt.sh's JSON endpoint (502 in 0.79 s and 0.71 s).

Code and data: sdist 0.1.3 (`cli.rs:24-75, 130-155`, `main.rs:180-250, 387-430, 519-571`, `bfs_crawler.rs:172-265,
360-385, 433, 962-972`, `frontier.rs:143-210, 327-470, 480-495, 655`, `url_utils.rs:7-29, 81-91`,
`ct_log_seeder.rs:10-16, 136-200`, `common_crawl_seeder.rs:180-190`, `state.rs:98-113, 285`); clones
`Rust-sitemap.git` at `32c2651`, `Scrapy.git` at `96e7a1a`, `ideal-url-organizer` at `159968a`;
`assets/stats.json` (`edition`, `repos[]`, `routes.rustmapper`, `runcheck.rustmapper`, `rules`, `figures`,
`agent_authored`, `coauthored_total`); `scripts/data/tree.py` (`scan_head`, `ci_selection`).
