# Review round 7, reviewer 2: the data engineer

10 Oct 2026. My lens: every number on the image and the page needs a definition that the audit stands behind and
the code agrees with. I checked every figure against `assets/stats.json`, `docs/data/AUDIT.md` §7, the Rust-sitemap
clone at `32c2651`, the 0.1.3 sdist (`scratchpad/r6/sdist013/rustmapper-0.1.3`), ideal-url-organizer at `159968a`
and Scrapy at `96e7a1a`. Renders: `scratchpad/r6/build/round-06/` (desk 870 day and night, phone 390 and 308 day and
night, the page on desk 1280, phone 390 and 360).

**Verdict: 7 / 10. It does not meet the goal yet. I would not ship it as is.**

## The first question: does it meet the owner's goal?

Mostly, yes. The islands are gone. Nothing in the picture has a size that means something, so the owner's question
("is it based on the size of the project or how many commits?") has the answer "nothing has a size". The image reads
top to bottom as one real thing: how you install his crawler, where its URLs come from, the fetch loop, how it
saves, the one catch in 0.1.3, how to stop it, the file you get, and which of his other projects reads that file. A
stranger learns how to run his main project and what can go wrong, faster than from the README. It reads on a phone
(26-unit text, 13.3 px at 308 px). No word names the theme. The magenta line you follow and the dotted box around the
danger give the manner without saying it.

What stops me shipping it is two numbers drawn on that route. A route earns trust only if every mark on it was
checked against what the code *does*. Both numbers were checked against a name in the code, and the code does
something else:

1. **"saved to redb, every 50 ms" is not what the writer does.** `BATCH_TIMEOUT_MS = 50` exists in both trees, and
   the code comment says "Drain batches every 50 ms". But `drain_batch` (sdist `src/writer_thread.rs:245-276`, HEAD
   `:258-289`) blocks with `recv_deadline` *only until the first event arrives*, at most 50 ms. Then it drains
   whatever is already queued with `try_recv` (up to `MAX_BATCH_SIZE`, 5,000) and returns at once. flume's docs say
   the same: `recv_deadline` waits "for an incoming value … returning an error if … the deadline has passed", and
   `try_recv` returns at once when the channel is empty [1]. So during a crawl the batches are written back to back,
   as fast as fsync and the redb commit allow. 50 ms is how long the writer waits when there is nothing to write. It
   is not how often it saves. PostgreSQL's docs make the same split: `commit_delay` is a wait for others to join one
   flush, not a flush period [3]. Every earlier round, mine included, read the constant and the comment and stopped
   there (r02-1 :44, r03-1 :82, r03-2 :134, r03-3 :134, r04-1 :80). The W1 anchors check only that the constant
   exists and goes into `Duration::from_millis`. They never check how it is used.
2. **"sorted 25 ways by ideal-url-organizer" overstates the hand-off.** 25 is the count of
   `src/organizers/method_*.py` files. The importer the hand-off rests on, `scripts/import_rust_sitemapper.py`,
   converts the file to `URLRecord`s and runs `./run.sh --all`, which is `src/main.py --full`. That runs
   `self.methods`, and that dict has **21** entries (method_01 to method_21). The importer's own docstring says "the
   URLRecord/methods-1-21 pathway". Methods 22 to 25 take `PageContent` from the organizer's own crawler
   (`method_24_by_page_authority.py` imports `src.core.web_crawler.PageContent`), and nothing outside their own files
   calls them. rustmapper's output is sorted 21 ways. Round 6's r1-3 assumed the pipeline runs all 25 sorts
   (review-r06-1.md:55). It doesn't.

Both are one-line text fixes, but they need anchors that pin the behaviour so the wrong number can't come back.

## Figures checked

| Where | Printed | Key / source | Measured | Defined in AUDIT §7 | Holds |
|---|---|---|---|---|---|
| image R2 | 0.1.3 · 8 Nov 2025 | `edition.version`, `.date` | 0.1.3, first upload 2025-11-08T19:52:41 | yes | yes |
| image S1 | "by default" | sdist `cli.rs` `default_value = "all"` | all | via routes row | yes |
| image G1 | 500 ms | sdist `main.rs:90` `THROTTLE_THRESHOLD_MS = 500.0` vs commit EWMA (α 0.4, `metrics.rs:169`) | 500 | **no row** | yes |
| image W1 | every 50 ms | sdist `writer_thread.rs:11`; `drain_batch` | a wait for the first event, not a period | yes, **with the wrong definition** ("committed … every 50 ms") | **no** |
| image H1 | 0.1.3 | `edition.version`; probe `ends_by_itself` false, `quiet_after_last_page` true | | no image row | yes |
| image H1 | `Received work item` | sdist `bfs_crawler.rs:433` | present | | yes |
| image R13 | url, depth, status_code, title | `SitemapNode` in both trees | present | | yes |
| image R15 | 25 ways | `figures[]` glob `method_*.py` = 25 | the hand-off runs 21 | no image row | **no** |
| facts | `32c2651`, 176 tests, CI passed 7 Oct 2026, 16k lines of Rust | `head`, `test_functions`, `ci` (head_sha = head), `lines.Rust` 16,390 | CI runs `cargo test --all-features` and `pytest python/tests`; no `#[ignore]` at HEAD | yes | yes |
| install note | CPython 3.13, Apple silicon | `edition.wheels` `cp313-cp313-macosx_11_0_arm64` | | yes | yes |
| install note | 3 min, cold cache, 4-core Linux x86_64 | `runcheck…install` runs 168.2 / 171.4 / 174.3 s, `cache: cold`, `cpus: 4` | 2.8–2.9 min | yes | yes |
| L1 | 20 per host, 256 in all | sdist `state.rs:285` `max_inflight: 20`; `cli.rs:31` `default_value = "256"` | | **no §7 row** (anchored in `routes`) | yes |
| L1 | no pause | probe `robots_read`: closest two fetches 1 ms apart | | no row | yes |
| X1 | 50,000 URLs per file | sitemaps.org protocol: "no more than 50,000 URLs", 50 MB uncompressed [2] | external constant | **no row, no source** | yes |
| Scrapy facts | `96e7a1a`, 1,920 tests, CI passed 8 Oct 2026, MIT, 69k lines | `head`, `test_functions`, `ci`, `license`, `lines.Python` 69,036 | see finding below on the 1,920 | yes, except `license` | yes, but see below |
| Scrapy prose | 50,000 characters, stage 3/4, 5 URLs, 60 s, localhost:3000 | `figures[]`, all `holds` | | yes | yes |
| Also | 25 ways (to sort a pile of URLs) | `figures[]` | 25 method files; 22–25 sort pages its own crawler fetched | yes | yes, as worded there |
| details | 15 more | 22 − profile − 2 flagships − 4 Also | 15; list has 11 + 4 | yes | yes |
| rules | Sep 2025, Oct 2025, Oct 2025 (prometheus 1 Oct, then grafana 6 Oct), Nov 2025 (2be623e, his) | `rules` | | yes | yes |
| data line | 0.1.3, 10 Oct 2026, Linux x86_64, 3-page site, seeding off | `runcheck` | | yes | yes |
| data line | 45 of 146; 71 of 499 | Rust-sitemap `others` Claude 45 / `all_hands` 146; Scrapy jules 49 + Claude 22 / 499 (dependabot 8 in the 499, not the 71) | | yes | yes |

**The Scrapy test count and CI.** "1,920 tests · CI passed 8 Oct 2026" reads as "1,920 tests pass". The CI job that
passed (`main.yml:112-114`) runs `pytest tests/ -m "not slow and not kafka and not performance"`, and pytest
deselects marked tests under `-m "not …"` [4]. My AST count over `Scraping_project/tests` (script:
`scratchpad/r7tools/marks.py`): 1,904 test functions, **25 deselected by those markers and 38 marked skip**, so
about 1,841 run in the job. The gap is 3 %, small but real. Rust-sitemap has no such gap. The audit defines "N tests"
as functions at HEAD. The page sets that number beside "CI passed", so a reader takes it as the number CI ran.

**The co-author trailers.** The data line counts the commits agents *authored* (45, 71). It leaves out that 30 of
his 420 Scrapy commits, and 1 of his 101 Rust-sitemap commits, carry a Claude co-author trailer
(`coauthored.agent`). AUDIT §5 allows it: "print the agent count only beside `agent_authored`", and that is exactly
where this line puts it. Leaving it out understates the agent share on Scrapy from 20 % to 14 %.

**The register itself.** `scripts/audit_figures.py` holds a hand-kept `HERO` dict with two rows (R2, W1) and a
`FIXED` list for the build blocks. G1's 500 ms, H1's release, R15's count, L1's 20 and 256, X1's 50,000 and the
facts line's "MIT license" have no §7 row. Everything except X1's 50,000 is anchored somewhere (`routes`,
`[[figures]]`), so the gates hold. But the brief's rule is "never print a figure without a definition the audit stands
behind", and the audit's own register is where a reviewer goes to find it. X1's 50,000 is not in the code at all.
It is the sitemap protocol's limit, and no file in the audit cites the protocol.

## Every element of the image

| Element | What a visitor learns | Verdict | Why |
|---|---|---|---|
| Name "Ben Russell" | whose page this is | keep | the first fact |
| Role line "Crawl and data infrastructure / Python and Rust" | what he builds, in two lines | keep | matches the route below it, so the role is shown, not just claimed |
| Empty left column under the role (desk) | nothing | keep | empty space with no figures in it is better than the old fine print. Nothing in this repository needs to fill it |
| "rustmapper" + "Crawls a site and writes one line for every URL it finds." | which project and what it does | keep | true for a file that also holds 404 links (`status_code` null) |
| Start bar + `pip install rustmapper` + "0.1.3 · 8 Nov 2025" | the line that gets it, and that the release is 11 months old | keep | both figures check out. The date is the one honest "how old" signal |
| S1 seeds | it finds URLs without links, and calls outside services by default | keep | `default_value = "all"` in the release |
| F1 fetch | what it follows: your site, its subdomains, its parent domain | keep | `is_same_domain` anchors, both trees |
| G1 governor, 500 ms | it slows itself when saving lags, at a threshold you can check | keep | the threshold is a commit-latency EWMA (α 0.4). "saves average" is a fair plain word for it |
| W1 "logged to disk, then saved to redb, every 50 ms" | (claimed) the save cadence | **change** | the number is the idle wait, not a period. Say "in batches" with no number (must-fix 1) |
| Loop bracket with up-arrow | fetch, save and the trap repeat | keep | it is why "never stops by itself" sits inside it |
| H1 dotted box "0.1.3 never stops by itself; done when `Received work item` lines stop" | the one catch, and how to tell when you're done | keep | probes `ends_by_itself` false and `quiet_after_last_page` true. The red dots are a graphic, not text colour, so they don't need text contrast |
| C1 "press Ctrl-C once to write `data/sitemap.jsonl`" | how to stop it without losing the file | keep | probe `crawl_ctrl_c`: exit 2.0 s after one SIGINT, three lines written |
| End bar + `data/sitemap.jsonl` + fields | what you get, with the struct's own field names | keep | `SitemapNode` in both trees. The file name now sits on two lines in a row (C1, then R13). It costs one phone line. I'd accept that: the first is the action, the second is the result |
| R15 arrow + "sorted 25 ways by ideal-url-organizer" | his projects join up: this output feeds another one | **change** | 21, not 25 (must-fix 2). The join itself is real and tested (`test_import_rust_sitemapper.py`) |
| Magenta track | the one path, read top to bottom | keep | magenta has marked the course to follow on US charts since the 1912 Inside Route charts [8] |
| Night editions | same content, night paper | keep | contrast table in SPEC §2.3 holds by eye in the renders |
| Phone stacking | everything above, in one column | keep | 600 units wide, 1,169 tall, 13.3 px text at 308 |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Link line | where to go next | keep | |
| Builds / Languages / Stack | who he is, in three lines | keep | |
| Pick sentence (rustmapper vs Scrapy) | which project to open, by need | keep | gate `no_services` holds |
| About rustmapper | pip gives a CLI; the Python API is unreleased | keep | `edition.modules` is `[]` |
| rustmapper facts line | it is alive and tested on main | keep | every figure holds; `head_sha` = HEAD |
| rustmapper code block | the commands, copyable | keep | 33-column comment line: see must-fix 3 |
| Wheel note | whether pip will just work, and the cost if not | keep | cold, three runs, measured |
| L1 + X1 paragraph | how hard it hits a site; one-file sitemap limit | keep, **register** | true; 20, 256 and 50,000 have no §7 row, and 50,000 has no source (must-fix 4) |
| `handoffs` marker (empty) | nothing | keep | it prints nothing while its join has no reader, as designed |
| Scrapy sentence | what Scrapy is | keep | |
| Scrapy facts line | alive and tested | **change** | 1,920 next to "CI passed", while CI deselects 25 and skips 38 (must-fix 5) |
| Scrapy code block | how to run it, and its two catches | **change** | at 360 px it shows 32 columns and clips five lines; at 390 it clips "…your own sit" (must-fix 3) |
| Grafana / spider-name sentence | two things that trip a stranger | keep | `figures[]` holds |
| Scrapy bullets 1–4 | the design, in checkable terms | keep | all figures hold |
| Also (4 lines) | his other serious work | keep | "25 ways" is right there: it describes the organizer, not the hand-off |
| "15 more" details | the rest, folded | keep | count holds |
| Working rules | how he works, each dated to his own commit | keep | all four dates and authors check |
| "Found a mistake?" | where to report one | keep | |
| Data line | how the drawing was checked, and who wrote the code | **change** | add the co-author trailers beside the authored counts (must-fix 6) |
| License line | | keep | |

## Must fix, ranked

1. **W1: drop the 50 ms, and anchor the batching it really does** (`chart.toml` W1, about line 476;
   `scripts/audit_figures.py` `HERO["W1"]`; AUDIT.md routes row and §7; one test; about 15 lines).
   - Text: "logged to disk, then saved to redb, in batches". On the desk it is still one line, on the phone still two.
   - Replace the `const = "BATCH_TIMEOUT_MS"` anchor and the `Duration::from_millis(BATCH_TIMEOUT_MS)` anchor with
     two `fn = "drain_batch"` anchors in both trees: `recv_deadline(deadline)` and `try_recv()`. Keep the order
     anchors.
   - Add an alternative "… every {const:BATCH_TIMEOUT_MS} ms" that holds only when `writer_loop` sleeps on the
     constant between flushes (`fn = "writer_loop"`, `text = "sleep(Duration::from_millis(BATCH_TIMEOUT_MS))"`).
     Then the number comes back by itself if the code ever adopts a timed flush.
   - Delete the W1 row from `HERO` and regenerate §7. In the AUDIT routes row, change "saved every 50 ms" and
     "committed … every 50 ms" to "drained in batches of up to 5,000 as events arrive; 50 ms is the wait for the
     first one".
   - Test: a fixture `drain_batch` with `recv_deadline` + `try_recv` verifies "in batches" and fails the "every N ms"
     alternative.
   - Why: it is the only number on the route whose meaning is wrong, and a storage engineer who opens
     `writer_thread.rs` will find that in a minute.
2. **R15: "sorted 21 ways by ideal-url-organizer"** (`chart.toml [[figures]]`, a new row; `sheets/route.py`
   `handoff_words()`; AUDIT §7; one test; about 12 lines).
   - New figures row `text = "21 ways"`, `repo = "ideal-url-organizer"`, `path = "src/main.py"`, counting the
     `'method_NN_…'` keys of the `self.methods = {…}` literal. Use `ast`, not a regex, the way SPEC §5 reads
     `URL_RECORD_FIELDS`. Mark it `handoff = true`.
   - Add a second anchor that `scripts/import_rust_sitemapper.py` calls `run.sh` with `--all`, and a third that
     `run.sh --all` runs `src/main.py --full`.
   - `handoff_words()` reads the `handoff = true` row, not the `method_*.py` glob. The Also line keeps "25 ways to
     sort a pile of URLs" from the glob row: that is a description of the organizer, and it is true.
   - Test: the fixture dict with 21 keys prints "21 ways"; with no `--all` call, the fallback is "sorted by
     ideal-url-organizer".
   - Why: the label claims what happens to *this* file, and 4 of the 25 sorts never see it.
3. **Code blocks fit the column GitHub actually shows** (`scripts/checks/readme.py:20` `CODE_COLUMNS = 38` → 32;
   README Scrapy block and the rustmapper comment; about 10 lines).
   - The renders measure 36 visible columns at 390 px (`page-phone-3.png`: "# or only discovery, on your own sit")
     and 32 at 360 px (`page-phone-360-3.png`). The docstring's "about 38 columns" was never measured.
   - Six lines are over 32: "# sitemap.xml, even after a kill:" (33), "# the whole pipeline (needs docker" (34),
     "# and docker-compose); it crawls a" (34), "# or only discovery, on your own site:" (38),
     "docker-compose run --rm scraper \" (33), "    -a allowed_domains=<domain> \" (33).
   - Rewrap: "# sitemap.xml, after a kill too:"; "# the whole pipeline; needs docker" / "# and docker-compose; it
     crawls" / "# a university's sample site"; "# or discovery only, on your site:"; `docker-compose run \` /
     `    --rm scraper \`; indent `-a` lines by 2.
   - Record the measurement (viewport, font, visible columns) in the check's docstring, as HERO-COLUMN-PX does.
4. **Complete the register; generate the image rows** (`scripts/audit_figures.py`; a new AUDIT-COVER in
   `scripts/checks/`; AUDIT §5 adds the sitemap protocol as a cited constant; about 40 lines).
   - Build `HERO` rows from route entries whose text holds `{const:}`, `{field:}`, `{arg:}` or `{release}`, and
     from `handoff_words()`'s row. Today that gives G1 500 ms, H1 0.1.3, R15 21 ways.
   - Add rows for the text entries: L1 (20, 256, "no pause" from probe `robots_read`) and X1 (50,000, with the
     source "sitemaps.org protocol, 'no more than 50,000 URLs'" and no code anchor). Add `repos[].license` for "MIT
     license".
   - AUDIT-COVER (fast tier) fails any digit run in the hero SVG's text or the README's visible text that no §7 row
     covers.
   - Why: today the register lists 2 of the image's 5 figures. A reviewer who checks it finds the gap before
     finding the fact.
5. **Scrapy's test count says what CI runs** (`scripts/data/tree.py` or `derive.py`; `render_readme.py` facts;
   AUDIT §2 and §7; about 30 lines and a test).
   - Measure `repos[].ci_deselected`. Read the `-m` expression from the passing workflow's pytest step, then count
     test functions under the step's path that carry those markers, or a skip mark, at function, class or module
     level (the AST walk in `scratchpad/r7tools/marks.py`). Today Scrapy has 25 + 38; Rust-sitemap 0.
   - When it is above 0, print "1,920 tests (CI runs all but 63)". The phone gets one more short line.
   - Why: "N tests · CI passed" is read as N passing tests.
6. **The data line names the co-signed commits** (`render_readme.py` `survey`; AUDIT §7 row; a test; one clause).
   - "… coding agents (Claude, jules) authored 45 of rustmapper's 146 commits and 71 of Scrapy's 499, and co-signed 1
     and 30 of mine." Source `repos[].coauthored.agent`.
   - Why: the audit's own rule allows it beside `agent_authored`, and leaving it out understates the agent share.

Not ranked, and not mine to fix here: S2 is still not drawn and ROUTE-UNVERIFIED still fails until P1 lands in
Rust-sitemap (round 6 log). The image doesn't go to `main` before that.

## Sources (new this round)

1. flume 0.11 docs, `Receiver::recv_deadline` and `try_recv`: waits "for an incoming value … the deadline has
   passed"; `try_recv` errors "if the channel is empty". https://docs.rs/flume/0.11.1/flume/struct.Receiver.html
2. sitemaps.org, *Sitemaps XML format*: "no more than 50,000 URLs and must be no larger than 50MB (52,428,800
   bytes)"; index files group several sitemaps. https://www.sitemaps.org/protocol.html
3. PostgreSQL docs, *WAL Configuration*: `commit_delay` is a group-commit wait, applied only when a commit needs a
   flush, "not periodic". https://www.postgresql.org/docs/current/wal-configuration.html
4. pytest docs, *Working with custom markers*: `-m "not webtest"` runs "all tests except the webtest ones" ("1
   deselected"). https://docs.pytest.org/en/stable/example/markers.html
5. redb docs, `Durability::Immediate`: commits "are guaranteed to be persistent as soon as `WriteTransaction::commit`
   returns". rustmapper never sets durability, so "saved to redb" means durable at commit.
   https://docs.rs/redb/latest/redb/enum.Durability.html
6. Python Packaging, *Binary distribution format*: `{distribution}-{version}.data/scripts/` holds the scripts
   installers put on the path. This confirms `edition.scripts` = `rust_sitemap`.
   https://packaging.python.org/en/latest/specifications/binary-distribution-format/
7. *Britannia (atlas)*, Wikipedia: Ogilby's 1675 strip maps draw a road as a ribbon with what you meet along it
   (hills, bridges, ferries, towns) and measured miles. A route drawn as an ordered strip is a real map form when the
   subject is a way through, which this image now is. https://en.wikipedia.org/wiki/Britannia_(atlas)
8. Power & Motoryacht, *The vanishing magenta line*: NOAA found the long-unmaintained ICW route line "passes on the
   wrong side of aids to navigation; crosses shoals". The lesson for this image: a drawn route is trusted only while
   each mark on it is re-checked against what is really there.
   https://powerandmotoryacht.com/electronics/vanishing-magenta-line-icw-charts/
9. Clone evidence: ideal-url-organizer `src/main.py` `self.methods` (21 keys), `run.sh` (`--all` → `main.py
   --full`), `scripts/import_rust_sitemapper.py` docstring ("methods-1-21 pathway"); Scrapy
   `.github/workflows/main.yml:112-114`; Rust-sitemap and sdist `src/writer_thread.rs` `drain_batch`.
