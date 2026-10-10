# Review round 9, reviewer 2: the deck officer and yacht navigator

10 Oct 2026. I use paper charts, chartplotters and pilot books for real passages, and I judge each mark by what it is
for. A mark on a chart earns its ink when the person at the wheel can act on it. If they can't, it's decoration.

What I looked at: every PNG in `scratchpad/r6/build/round-08/`. That covers the desk sheet at 870 px (day and night),
the phone sheet at 390 and 308 px (day and night), the desk page (two screens), and the phone page at 390 (six
screens) and 360 (seven screens). I also zoomed into the track region of the desk and phone day sheets, and read the
four SVGs in `build/assets/` for element IDs and type sizes. I read `README.md`, `SPEC.md`, `LOG.md` through round 8,
every review from rounds 1 to 8, `chart.toml` `[route.rustmapper]`, and the sheet's `PURPOSE` table. I don't repeat
anything already fixed.

I checked every figure against `assets/stats.json` and the 0.1.3 sdist (`scratchpad/r6/sdist013/rustmapper-0.1.3`).
I ran one new probe against the 0.1.3 binary the run check installed (`scratchpad/r6/rc2/work/v/bin/rust_sitemap`):
a local site with one page that answers 429 (`scratchpad/r9n_probe/`).

Verdict: **not yet. 8 / 10.** All of round 8's fixes landed, and I checked each one in the renders:

- The phone heading now stands clear of the role line.
- 21 against 25 is explained.
- C1 gives its caution, with `Saved to:` as the mark that says you're done.
- F1 states the per-host cap that actually governs a site crawl.
- go_go_go no longer leads with impersonation.
- The rules, the levers (L2), the Compose sentence and L3 are in.

The image does what a strip chart of one passage should do. In order, it shows:

1. the entrance (`pip install`) and its edition date;
2. what the tool does on the way, in the order it does it;
3. the rows that repeat;
4. the one danger, sitting where you'd expect the way out;
5. the one manoeuvre (Ctrl-C) and the mistake to avoid there;
6. where you arrive (`data/sitemap.jsonl`);
7. where the output goes next.

Nothing has a size, and no word names the sea.

Two things stop me shipping it, and one small thing should be fixed while the file is open.

1. **The output's `status_code` field is shown to strangers, and it doesn't hold what the name says.** In 0.1.3 it is
   200 or empty. A page that answers 429 or 503 is written with no status and no title. The crawler doesn't slow
   down for it, doesn't ask for it again, and never follows its links. I measured this. The page says nothing about
   it.
2. **The danger mark has a clearing mark with no number on it.** "Done when it stops printing `Received work item`"
   is the right kind of mark. But a 0.1.3 crawl normally goes quiet for up to 20 s while it waits on a slow
   response. A stranger who presses Ctrl-C at the first pause gets a partial file. And in 0.1.3, `resume` doesn't
   rescue them.
3. The alt text says "How to start", but the image's only command is the install.

## The first question: does it meet the owner's goal?

- **Every map has a deep purpose.** Yes. It is the one route a URL takes through rustmapper. The bracket and the
  break in the track show something a list can't: those rows repeat, and the line doesn't carry you out of them.
  Take the colour and the hatching away and it still reads as directions.
- **It teaches something true and useful about his actual projects.** Every line of the image is true (figures
  below). Each one is useful, with one reservation: R13 names a field, `status_code`, that a stranger will read as
  "this tells me which pages are broken". In 0.1.3 it can't. That is must-fix 1. Fixing it doesn't mean changing the
  drawing. It means telling the stranger, in the text, what the file can't tell them.
- **Nothing chases a reason.** Yes. Every mark has a job (table below).
- **Nothing announces the theme.** Yes. The manner carries it:
  - a magenta line you follow;
  - a dotted danger line with a clearing mark;
  - the release date at the entrance;
  - a continuation arrow at the foot;
  - a source note under the text.
- **Reads on a phone.** Yes. At 308 px every text run is 26 sheet units, about 13.3 px on screen. The heading gap is
  fixed, and the sheet is 1,121 units high, under the 1,246 gate.

## What a navigator asks of a danger mark

On a chart, a clearing line is "a straight line … that marks the boundary between a safe and a dangerous area" (IHO
S-32) [S1]. It is useful only because it comes with a number you can check from the wheel: "as long as our clearing
bearing reads less than 045°M we're in safe water; if it reads more than 045°M we're heading into danger" [S2]. The
Japan Transport Safety Board's worked example states every clearing line the same way: "If Kuroshima's peak exceeds
a true bearing of 60°, the vessel enters the danger zone." The point of a clearing line, it says, is that
"deviations into dangerous areas can be immediately detected without frequent position checks" [S3]. A clearing mark
with no number makes the helmsman guess.

H1's clearing mark has no number. "Done when it stops printing `Received work item`" doesn't say for how long. Here
is how long the line can normally go quiet in 0.1.3:

- **Each fetch can run up to its timeout before the next line appears.** The `--timeout` default is 20 s
  (`sdist:src/cli.rs:49-51`). It is set on the reqwest client (`network.rs:33`), and reqwest applies it "from when
  the request starts connecting until the response body has finished" [S4].
- **On a single site, a quiet terminal is normal.** One host takes at most 20 fetches at once
  (`state.rs` `max_inflight`, `frontier.rs:652-670`), and the next URL waits until one finishes. When the site is
  slow, the terminal is quiet while work is still going on.
- **After a permanent error, the host is held back for 2 s, then 4 s.** That is `record_failure`, `2^failures`
  (`state.rs:316-323`), counted in whole seconds. After the third failure the host is dropped
  (`MAX_FAILURES_THRESHOLD = 3`, `state.rs:268`; "[BLOCKED] Permanently skipping", `frontier.rs:615-621`).

So a pause of up to about 25 s (20 + 4 + 1) is normal in 0.1.3 and doesn't mean it's finished. What does an early
Ctrl-C cost? The file holds only what was found so far. `resume` after a stop doesn't work in 0.1.3: the run check's
`resume_after_kill` step failed with "Database creation error". Today's probe `quiet_after_last_page` can't catch
any of this: it waits 100 s on a local site that answers in 1 ms.

Other crawlers state this condition as a number. Scrapy's `CLOSESPIDER_TIMEOUT_NO_ITEM` closes a spider "if it has
produced no items for the configured number of seconds" [S5]. Scrapy's own idle rule and Crawlee's
`isFinishedFunction` stop by themselves once nothing is pending [S6]. 0.1.3 does neither, so the drawing has to give
the number. Ctrl-C is also the passage's commitment point. A port's passage plan states the point of no return with a
distance ("approximately ½ to 1 nm from the fairway buoy … from this point onward the vessel is committed") [S7].
The reader needs a mark they can check before they commit.

## What the file says about a page that refused

I served four pages on 127.0.0.1, ran `rust_sitemap crawl --seeding-strategy none` from the run check's 0.1.3 venv,
and sent one SIGINT at 12 s. `/b.html` answered **429** with `Retry-After: 2` and linked to `/d.html`.

```
server log: /  /b.html  /a.html  /c.html          (b.html asked for once; d.html never)
sitemap.jsonl:
  /        200   i
  /a.html  200   a
  /b.html  None  None
  /c.html  200   c
```

The code says why (`sdist:src/bfs_crawler.rs:786-816`). Only a 200 goes on to parsing. Any other status returns
`Ok(Vec::new())` before a `ParseJob` exists, and `status_code` is set only from that job (`:393`, `state.rs:183`).
Then `record_success` resets the host's failures (`frontier.rs:939-948`). So a 429 or a 503 gets:

- no backoff;
- no second request;
- no status in the file;
- none of its links followed.

`export-sitemap` keeps only `status_code == Some(200)` (`main.rs:408`), so `sitemap.xml` just drops the page. Main
at `32c2651` is the same: its only 429 handling is in the seeders (`ct_log_seeder.rs:33`,
`common_crawl_seeder.rs:51`). So his seeders back off when crt.sh says 429, but his crawler doesn't back off when your
site says it.

This matters to the stranger in two ways:

- **It can't find broken links.** A 404, a 429, a 503, a PDF and a link never fetched all look the same in the file:
  an empty `status_code`. R13 puts that field name in front of them.
- **The URL list can be missing whole branches without saying so.** A site behind a rate limiter answers 20
  simultaneous requests with 429s. L1 already says rustmapper sends with no pause. A stranger reading it needs the
  consequence too. Google's crawler, the yardstick a site owner brings, "reduces your site's crawl rate" on 429 and
  503 (cited in round 8). A tool that should tell the user what state it's in [S8] shouldn't let a refusal look like
  a missing page.

## Figures checked

Against `assets/stats.json` (`taken` 2026-10-10), the 0.1.3 sdist, the Rust-sitemap clone at `32c2651` and the run
check's steps.

| Printed | Source | Holds |
|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `edition.date`; all four uploads 2025-11-08 | yes |
| by default: sitemaps, certificate logs, Common Crawl | sdist `cli.rs` `default_value = "all"`; `bfs_crawler.rs:188-211`; `routes` S1 verified both | yes |
| up to 20 pages at a time from each host | sdist `state.rs` `max_inflight: 20`; `frontier.rs:652` | yes |
| its subdomains and its parent domain | `url_utils.rs:81-91`, dot-boundary checks both ways; seeds pass the same filter (`frontier.rs:492`) | yes |
| logged to disk, then saved to redb, in batches | `routes` W1 fallback (`drain_batch`) | yes |
| never exits by itself; `Received work item` | `runcheck` `ends_by_itself` false at 150 s; `bfs_crawler.rs:433` | yes, with no time (must-fix 2) |
| press Ctrl-C once; a second press before `Saved to:` … | `second_ctrl_c` ok (exit 1, no file) | yes |
| fields `url, depth, status_code, title` | `SitemapNode`, both trees | names yes; `status_code` is 200 or empty (must-fix 1) |
| sorted 21 ways | `figures` `self.methods` 21 | yes |
| 25 ways: 21 from …, 4 more | `figures` 25 = 21 + 4 (`List[PageContent]`) | yes |
| 176 tests · CI 7 Oct 2026 · 16k lines · `32c2651` | `repos[Rust-sitemap]` 176; success 2026-10-07; Rust 16,390 | yes |
| 1,920 tests (CI selects all but 41) · 8 Oct · MIT · 69k · `96e7a1a` | `repos[Scrapy]`; `not_selected` 41 (16 + 25); Python 69,036 | yes |
| 3 min, cold cache, 4-core Linux | `runcheck` install median 171.4 s, 4 CPUs, empty `CARGO_HOME` | yes |
| at most 256 at a time; `--workers 1` one at a time | `cli.rs` "256"; `workers_cap` (2 open by default, 1 with the flag) | yes |
| 50,000 URLs per file | X1 `DEFAULT_MAX_URLS_PER_SITEMAP` at HEAD | yes |
| 6 days, then 5 | `67446a4` 25 Sep → `d571e6e` 1 Oct → `e8cbe15` 6 Oct 2025 | yes |
| rule cites Oct 2026, Oct 2025, Oct 2025, Nov 2025 | `rules[]` `099dd6c`, `52dcbd8`, `d571e6e`, `2be623e` | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | 101 + 45; 420 + 49 + 22 + 8, agents 49 + 22; `coauthored.agent` | yes |
| 15 more | 22 − profile − 2 − 4 | yes |
| 5 URLs, 60 s, 50,000 characters, `localhost:3000` | `figures` rows, all hold | yes |
| 10 Oct 2026, Linux x86_64, seeding off, 3-page site | `runcheck.date`, `runner`, step 3 | yes |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell", serif | whose page | keep | read first, as a chart's title is |
| Role line, two caps lines | crawl and data infrastructure, Python and Rust | keep | the route under it proves both |
| Empty left column under the role (desk) | nothing, on purpose | keep | blank land keeps the eye on the route |
| "rustmapper" + header sentence | which project, and what it writes | keep | the gap from the role line is fixed |
| Start bar | where you begin | keep | the departure point |
| `pip install rustmapper` | the way in | keep | the one command |
| "0.1.3 · 8 NOV 2025" | how old the release you install is | keep | an edition date where you use the chart |
| Magenta track | one way through, read downwards | keep | the line you follow |
| S1 ring and seeds | URLs come from more than links, and what it contacts by default | keep | a stranger should know crt.sh and Common Crawl get their domain |
| F1 ring, fetch and scope | the loop, the load one site takes, how far it reaches | keep | the cap a site feels, in the clause it belongs to |
| W1 ring, write path | it saves as it goes | keep | the data-infrastructure signal, and why export works after a kill |
| Loop bracket, arrow up | which rows repeat | keep | the one fact only a drawing gives |
| Break in the track under the loop | no way out but yours | keep | |
| H1 dotted box | the catch in 0.1.3, and the mark that says you're done | change | the clearing mark needs its number (must-fix 2) |
| C1 ring and words | the one manoeuvre and its caution | keep | the commitment point, with what not to do there |
| End bar | where you arrive | keep | |
| `data/sitemap.jsonl` + fields | what you get, in the struct's own words | keep | true names. Its one misleading field is answered in text (must-fix 1) |
| Hand-off line, arrow, "sorted 21 ways by ideal-url-organizer" | his projects feed each other | keep | a continuation note, and it agrees with the page now |
| Night editions | the same in dark mode | keep | magenta and the danger dots hold on navy |
| Phone editions (600 wide, shown at 308) | the same on one screen | keep | heading gap fixed, 1,121 high |
| Alt text | what the drawing shows | change | "How to start" promises a command the image doesn't show (must-fix 3) |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Link line | where to go | keep | |
| "Ben Russell builds …" | what he builds | keep | |
| Languages, Stack | what he builds with | keep | from the data |
| Pick sentence | which tool for which job | keep | |
| rustmapper sentence | the Python API isn't released | keep | |
| rustmapper facts line | alive, tested, size, which commit | keep | "On main at" keeps it apart from the 0.1.3 drawing |
| rustmapper code block | how to run, stop and recover | keep | copyable directions; fits 360 px |
| Wheel note | when pip just works | keep | a condition of the entrance |
| L1 + L2 (load, robots, the two levers) | what it does to a site, and how to turn it down | keep | the book's caution paragraph, with its remedy |
| L3 + X1 (what it can't see; one sitemap file) | its limits | change | add what the file can't tell you (must-fix 1) |
| Scrapy sentence + facts | the second tool, measured | keep | |
| Scrapy run sentence + code block | how to start it | keep | long on the phone (11 lines before the block), but every clause stops a real failure |
| Grafana note + bullets | what Scrapy does that rustmapper doesn't | keep | |
| Also: ideal-url-organizer, go_go_go, rust_llm_logger, Ai_code_detector | four more tools, each by what it does | keep | round 8 fixes hold |
| 15 more | the rest | keep | |
| Working rules 1 to 4 | how he works, each with a dated commit behind it | keep | |
| Found a mistake? | the page can be corrected | keep | |
| Data line | which release was drawn, how it was checked, who wrote the code | keep | |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **Say what `sitemap.jsonl` can't tell you** (`chart.toml`, one new text entry `X2`, scope `release`, after `X1`
   in the same paragraph; `scripts/runcheck.py`, one probe; one AUDIT §7 row; one fixture test; about 50 lines).
   - Text: "{release} records a status only for a page that answers 200: a 404, a 429 or a 503 is written with no
     status, is not asked for again, and its links are not followed." That's about 3 lines at 390 px and 2 at desk.
     It goes in the README only, not the image.
   - Release anchors (sdist):
     - `src/bfs_crawler.rs`, fn `process_url_streaming`, text `Ok(response) if response.status().as_u16() == 200`
       before `Ok(_) =>`, and text `result: Ok(Vec::new())`;
     - `src/bfs_crawler.rs` `status_code: job.status_code` (the only setter);
     - `absent = "Retry-After"` in `src/bfs_crawler.rs` and `src/frontier.rs`;
     - `absent = "429"` in `src/bfs_crawler.rs`.
   - New probe `non200_status` (gate false, like `robots_read`). Serve the fixture with one page answering 429 with
     `Retry-After: 2` and linking to a fifth page, and one link to a page that 404s. Pass if the server log shows the
     429 page asked for once in 12 s, the fifth page never asked for, and both the 429 and the 404 rows in
     `sitemap.jsonl` have `status_code` null. The entry has `runs = ["non200_status"]`. It retires by itself (an
     empty `instead`) once a release records statuses or retries a 429.
   - Owner, in Rust-sitemap: record the status for every response, and back off on 429/503 the way the seeders
     already do.
   - Why: the image names `status_code` as a field, and a stranger will use it to find broken pages. In 0.1.3 every
     non-200 looks the same, and a page that refused is silently dropped with its whole branch. L1 says the tool
     sends with no pause; this is what that costs the user's own file. Measured above.

2. **Give H1's clearing mark its number** (`chart.toml` H1 text and its first `instead`; one audit note; one
   fixture test; the run-check probe widened; no new drawing).
   - Text: "{release} never exits by itself; done once `Received work item` is quiet for {quiet} s". The value is
     30. The desk line is about 76 characters, under its 740-unit measure. The phone line may wrap to 3 lines
     (+34 units, 1,121 → about 1,155, under 1,246).
   - The figure is computed, not chosen. `data/route.py` adds `{quiet}`: the release's `--timeout` default (cli.rs,
     `arg = "timeout", equals = "20"`), plus the longest backoff before a host is dropped. That backoff is
     `2^(MAX_FAILURES_THRESHOLD − 1)` = 4 s (`state.rs` `record_failure`, `MAX_FAILURES_THRESHOLD`), plus 1 s for
     whole-second counting, rounded up to the next 10. The audit note says exactly that.
   - Anchors to add: `network.rs` `.timeout(Duration::from_secs(timeout_secs))`; `state.rs` `const = MAX_FAILURES_THRESHOLD`
     and `2_u32.pow(self.failures.min(8))`.
   - Probe change: `quiet_after_last_page` gets a fixture page that holds its answer 15 s and links to one more page.
     Pass if the gap between two consecutive `Received work item` lines is at least 15 s (silence under the bound is
     not the end) and the file is complete after `{quiet}` s of quiet.
   - Why: a clearing mark is only as good as its number [S1–S3]. Today a normal 20 s wait on a slow page looks
     like "done". An early Ctrl-C gives a partial file, and 0.1.3's `resume` fails. Other crawlers state this stop
     condition in seconds [S5].

3. **The alt text says what the image does** (`scripts/render_readme.py` `alt_for`; one word; T-ALT updated).
   - "How to install Ben Russell's crawler rustmapper, what it does with each page, and how to stop it. It loops
     until one Ctrl-C writes data/sitemap.jsonl." That's 25 words, unchanged.
   - Why: the image's one command is `pip install`. The crawl command lives only in the code block (round 2, "one
     home per fact"), so "start" promises a screen-reader user something the image doesn't hold.

**Owner, outside this repository, not re-ranked** (rounds 4 to 8): fix P1 and the idle test, ship 0.1.4, LICENSE,
`start.py` accepting `docker compose`, the governor, the second Ctrl-C message, `resume`. New from this round:
record every response's status, and back off on 429/503.

**Noted, not ranked.**
- The image never shows the binary's name (`rust_sitemap`). A stranger reading only the image would type
  `rustmapper crawl` and get "command not found". Round 2 moved the command to the code block on purpose, and P4
  (a `rustmapper` script in 0.1.4) fixes it at the source, so I don't reopen it.
- On the phone, the data line is 8 lines at about 27 px pitch for about 11 px text, because GitHub's `<sub>` lowers
  the baseline and opens the line box. MDN reserves `<sub>` for typographic subscripts [S9]. If GitHub's sanitizer
  ever allows a plain small-text element, use it.

## Sources (new this round)

1. [S1] IHO S-32 Hydrographic Dictionary, "clearing line" (entry 835): "A straight line, on a CHART, that marks the
   BOUNDARY between a safe and a dangerous area":
   https://portal.iho.int/iho-ohi/S32/engView.php?page=42
2. [S2] Practical Boat Owner, "Nav in a nutshell: clearing bearings": "as long as our clearing bearing reads less
   than 045°M we're in safe water … if it reads more than 045°M we're heading into danger":
   https://www.pbo.co.uk/seamanship/nav-in-a-nutshell-clearing-bearings-23176
3. [S3] Japan Transport Safety Board, JTSB Digest No. 45, Column 3 "Clearing Line": deviations "can be immediately
   detected without frequent position checks"; "If Kuroshima's peak exceeds a true bearing of 60°, the vessel enters
   the danger zone": https://jtsb.mlit.go.jp/bunseki-kankoubutu/jtsbdigests_e/jtsbdigests_No45/No45_pdf/jtsbdi-45_column03.pdf
4. [S4] reqwest `ClientBuilder::timeout`: "The timeout is applied from when the request starts connecting until the
   response body has finished": https://docs.rs/reqwest/latest/reqwest/struct.ClientBuilder.html
5. [S5] Scrapy documentation, Extensions, CloseSpider: `CLOSESPIDER_TIMEOUT_NO_ITEM` closes the spider "if it has
   produced no items for the configured number of seconds": https://docs.scrapy.org/en/latest/topics/extensions.html
6. [S6] Crawlee, `AutoscaledPoolOptions.isFinishedFunction`: "called only when there are no tasks to be processed";
   when it resolves true the run ends on its own: https://crawlee.dev/js/api/core/interface/AutoscaledPoolOptions
7. [S7] Northport (Marsden Point, NZ), Passage Plan NTPIL0101-1 Rev 7: "The point of no return should be considered
   to be approximately ½ to 1 nm from the fairway buoy … From this point onward the vessel is committed to the
   channel"; "All areas outside the marked channel are to be considered NO GO areas":
   https://northport.co.nz/sites/default/files/Passage%20Plan%20-%20NTPIL0101-1%20Rev7%20MP.pdf
8. [S8] Nielsen Norman Group, "Visibility of System Status": systems should "always keep users informed about what is
   going on"; users "need to know whether the interaction was successful":
   https://www.nngroup.com/articles/visibility-system-status/
9. [S9] MDN, `<sub>`: "should be used only for typographical reasons … rather than solely for presentation or
   appearance purposes" (this page was cited in an earlier round for another point; it is used here only for the
   unranked note): https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/sub

Code and data: `assets/stats.json` (`edition`, `routes.rustmapper`, `runcheck.rustmapper` steps including
`quiet_after_last_page` and `resume_after_kill`, `figures`, `rules`, `repos[]`). Sdist 0.1.3:
- `bfs_crawler.rs:168-260` (seeding), `:374`, `:393`, `:433`, `:500-560`, `:628-676`, `:780-900`;
- `frontier.rs:143-215`, `:470-500`, `:600-700`, `:935-985`;
- `state.rs:228-350`;
- `url_utils.rs:14-29`, `:81-91`;
- `network.rs:22-55`; `cli.rs:49-51`; `main.rs:408`; `ct_log_seeder.rs:1-330`.

Rust-sitemap `32c2651` (429 handled only in `ct_log_seeder.rs` and `common_crawl_seeder.rs`). The probe:
`scratchpad/r9n_probe/srv.py`, `req.log`, `crawl.log`, `d/sitemap.jsonl`.
