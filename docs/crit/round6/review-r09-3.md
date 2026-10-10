# Review round 9, reviewer 3: the staff engineer screening for data infrastructure

10 Oct 2026. I screen GitHub profiles for data-infrastructure hires. I look on a phone first, between other things,
then on a laptop for the ones that make the cut. I looked at every PNG in `scratchpad/r6/build/round-08/`: the desk
sheet at 870 (day, night), the phone sheet at 390 and 308 (day, night), the desk page (two screens), the phone page
at 390 (six screens) and at 360 (seven). I read `README.md`, `SPEC.md`, round 8's log and the reviews from rounds 1
to 9 (review-r09-1 included). I don't repeat anything already fixed. Every figure was checked against
`assets/stats.json`, the clones and the 0.1.3 sdist. I did the new research for this round myself (11 sources below,
plus the clones and one live OSV query).

Verdict: **not yet. 8 / 10.** The image meets the goal. I'd show it to a hiring panel as it is, once 0.1.4 passes
the run check. The text around it still hides the part of his work I'm hiring for. In one place it also gives the
same word ("CI passed") to two very different levels of rigour.

## The first question: does it meet the owner's goal?

- **A deep purpose for the map.** Yes. It's directions through one tool: what you install, where its URLs come from,
  the per-page loop, where it bites, how you stop it, what file you get, and who reads that file. A list can't show
  the loop or where the trap sits in it. The bracket and the gap in the track show both in one glance. Nothing in it
  has a size, so the owner's old question, "is it based on the size of the project or how many commits?", has
  nothing left to ask about.
- **True and useful about his projects.** Yes. Every row holds against the 0.1.3 sdist and the run check (table
  below). For my job, two rows do the most work. "logged to disk, then saved to redb, in batches" is a WAL with fsync
  before apply. "fields: url, depth, status_code, title, …" is a real schema in the struct's own names. Those two
  lines tell me he thinks about the storage side.
- **Nothing chases a reason.** In the image, nothing does. On the page, the Python-API line still does (review 1,
  must-fix 2, which I back).
- **Nothing announces the theme.** True. The magenta line, the dotted danger box and the terse rows carry it, and no
  word names it.
- **Reads on a phone.** The image reads on one 390 screen and at 360. The page doesn't serve a screener. "CRAWL AND
  DATA INFRASTRUCTURE" is the claim on screen 1. The evidence for its second half is the Delta Lake raw layer,
  MinHash dedup, per-host breakers and Prometheus, and it doesn't start until phone screen 4. Ahead of it sit
  rustmapper's setup, its cautions and Scrapy's setup. A screener's first pass is short. The Ladders eye-tracking
  study measured 7.4 s on a résumé, and pages with clear sections and headings did better than ones with long
  sentences [S2]. Most people who screen me never get to screen 4.

## Figures checked (independently this round)

| Printed | Source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `.date`, `uploads` | 0.1.3, 2025-11-08 | yes |
| up to 20 pages at a time from each host | sdist `state.rs` `max_inflight: 20` | 20 | yes |
| logged to disk, then saved to redb, in batches | HEAD `wal.rs:81-89` (record, checksum) and the fsync-before-apply order anchors | | yes |
| 0.1.3 never exits by itself; `Received work item` | runcheck `ends_by_itself` false at 150 s; `quiet_after_last_page` ok | | yes |
| second press before `Saved to:` | runcheck `second_ctrl_c`: exit 1, no file | | yes |
| sitemap.xml, even after a kill (code block) | runcheck `kill_writes_file` false, `export_after_kill` 3 `<loc>` | | yes, the comment says what holds |
| sorted 21 ways; Also 25 = 21 + 4 | `figures` rows `21 from`, `4 more`, `25 ways`, all `holds` | | yes |
| 3 min, cold cache, 4-core Linux x86_64 | runcheck install median 171.4 s, 4 CPUs | 2.9 min | yes |
| 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust | `repos[Rust-sitemap]` 176, success 2026-10-07 at `32c2651`, Rust 16,390 | | yes as the workflow defines it (see must-fix 4) |
| 1,920 tests (CI selects all but 41) · 8 Oct · MIT · 69k | `repos[Scrapy]` 1,920, `ci_selection.not_selected` 41, MIT, 69,036 | | yes |
| 45 of 146; 71 of 499; co-signed 1 and 30 | 101 + 45; 420 + 49 + 22 + 8; `coauthored.agent` 1, 30 | | yes |
| "appended to and never overwritten" (rule 2) | Scrapy `lakehouse_manager.py`: raw tables written `mode="append"`; the only deletes are queue GC (`gc_queue_table`, queue tables only), the operator's `repair_unknown_domains` (append before delete) and `truncate_table` | | yes in practice; the repair path is an operator tool, not the pipeline |

## Every element of the image

| Element | What a screener learns | Verdict | Why |
|---|---|---|---|
| "Ben Russell" | whose work this is | keep | first fact read |
| Role line, two caps lines | crawl and data infrastructure; Python and Rust | keep | the image proves "crawl"; the text has to prove "data infrastructure" sooner (must-fix 2) |
| Empty left column (desk) | nothing, on purpose | keep | it makes the route read first |
| "rustmapper" + one-line header | which tool, what it gives you | keep | |
| Start bar + `pip install rustmapper` + 0.1.3 · 8 NOV 2025 | the way in; the release is 11 months old | keep | honest age. The fix is a release, not a hidden date |
| Magenta track | one way through | keep | |
| Stop rings | one step each | keep | |
| S1 seeds | URLs come from more than links, by default | change | review 1 must-fix 4, as written |
| F1 fetch, per-host cap, scope | concurrency is bounded per host; what's in scope | keep | the per-host cap is the politeness fact a crawler screener checks first |
| W1 write path | a WAL, fsync, then batched commits | keep | the strongest data-infra signal on the sheet |
| Loop bracket + arrow | which rows repeat per page | keep | only a drawing shows it |
| Gap under the loop | the loop has no exit but Ctrl-C | keep | |
| H1 red dotted box | the known fault in 0.1.3 and how to tell you're done | keep while 0.1.3 is current | a known issue stated plainly is a maturity signal. It retires itself when 0.1.4 ends |
| C1 Ctrl-C | the one action, and the costly second press | keep | |
| End bar + `data/sitemap.jsonl` + fields | the output contract in the struct's names | keep | a data engineer reads this row first |
| Hand-off + "sorted 21 ways by ideal-url-organizer" | his tools compose | keep | |
| Night editions | the same | keep | |
| Phone editions (390, 308) | the same in one screen | keep | S1 is the only 3-line row |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image + alt | above | keep | |
| Link line | where to go | keep | |
| Builds / Languages / Stack | what he builds on | keep | the Stack line is the screener's keyword pass |
| Pick sentence | which tool for which job | keep | |
| rustmapper about line | packaging state | cut | review 1 must-fix 2 |
| rustmapper facts line | which commit, tests, CI, size | change | "CI passed" doesn't say what passed (must-fix 4) |
| rustmapper code block + wheel note | how to run, stop, recover; will pip just work | keep | |
| Cautions L1, L2, L3, X1 | what it does to a server, the levers, what it can't see | change | review 1 must-fix 1 (one short list) |
| Scrapy sentence + facts | the second tool, measured | keep (facts: must-fix 4) | |
| Scrapy run sentence | where to run it, what it needs | change | review 1 must-fix 3: following it makes the first `cd` fail |
| Scrapy code block + Grafana note | how to start it | keep, move | below the bullets (must-fix 2) |
| Scrapy three bullets | raw Delta layer, schema evolution, partitions, compaction, MinHash, local summarizer, per-host breakers, metrics | keep, move up | this is the data-infrastructure evidence, and today it's the last thing in the block (must-fix 2) |
| Also (four lines) | four more tools by what they do | keep | |
| 15 more | the rest | keep | |
| Working rules 1–4 | how he works, each with a dated cite | keep | rule 3 ("Measure from the start", 6 days then 5) is the line I'd quote in a debrief |
| Found a mistake? | the page can be corrected | keep | |
| Data line | what the drawing was run on; who wrote the code | keep | the agent share, stated per repository, is the honesty a screener now checks for |
| Licence line | the profile's terms | keep | |

## Must fix, ranked

1. **The Scrapy run sentence agrees with its block.** As review 1 wrote it in must-fix 3. It ranks first because
   the first command a stranger types has to work.

2. **Scrapy: what it does before how to run it** (`README.md:69-78`, which is hand-typed; `tests/test_pipeline.py:495`
   order list; about 6 lines moved, one test line, no new words).
   - New order: the Scrapy sentence, then the facts line, then the three bullets (Delta Lake raw layer; MinHash and
     the stage 4 summarizer; Prometheus, per-host breakers, Compose and Helm). After those come the run sentence (as
     corrected in item 1), the code block and the Grafana note.
   - Add `"- Raw pages land in Delta Lake"` to the order test between `<!-- facts:Scrapy:start -->` and
     `"Run these from"`.
   - Phone effect: the bullets go from screen 4 to screen 3 at 390, and no line is added.
   - Why: the inverted pyramid puts "the who, what, when, where and why … at the start", so readers who stop early
     still get the point [S3]. For my job the what of Scrapy is the claim that matters. Employers in Marlow and
     Dabbish's interviews went to the candidate's main project "and then assess[ed] the actual code" [S1]. The
     bullets tell them where to look (`lakehouse_manager.py`, `stage2_worker.py`). The setup steps only help someone
     who has already decided to run it.

3. **The rustmapper cautions become one short list.** As review 1 wrote it in must-fix 1. From my seat it also
   stops the flagship reading as a list of defects before a screener reaches Scrapy.

4. **The facts lines name what CI checks, not only that it passed** (`scripts/data/github.py` or `tree.py`, new
   `repos[].ci.gates`; `render_readme.facts_block` at `:402-414`; AUDIT `ci` row; `stats_schema.json`; about 40 lines
   and three fixture tests).
   - Read the CI workflow file at `ci.head_sha` from the clone. The workflow name is in `ci.workflow`, and the file
     is the one with that `name:`. Count a step as a gate when it meets all three of these:
     - neither its job nor the step has `continue-on-error: true`;
     - its `run` doesn't end in `|| true`, `|| :` or `|| echo …`;
     - it runs a known check: `cargo test` / `pytest` → tests, `cargo fmt … --check` → rustfmt, `cargo clippy` →
       clippy, `cargo audit` → cargo audit, `ruff` → ruff, `mypy` → mypy, `bandit` → bandit.
   - Print "CI passed 8 Oct 2026: tests, ruff, mypy, bandit" for Scrapy and "CI passed 7 Oct 2026: tests, rustfmt"
     for rustmapper. Use no-break spaces as now. That's about one more phone line each.
   - Tests: a fixture `ci.yml` with `cargo clippy … || true`, `cargo bench || echo` and a `continue-on-error` audit
     job gives `["tests", "rustfmt"]`. A Scrapy-like fixture gives four gates. With no workflow file found, the old
     wording stays and `check.py` warns.
   - Why this isn't round 2's finding again: round 2 moved the definition into AUDIT.md and kept the words. What's
     new is that the two flagships differ, and the page hides the difference.
     - Scrapy's `main.yml:19-25` says "ruff / mypy / bandit are blocking (no || true)". That's a real signal of
       rigour, and the page doesn't show it.
     - Rust-sitemap's `ci.yml` has three jobs that can't fail. Clippy runs with `|| true` (`:109`). The audit job is
       `continue-on-error` at job and step level (`:154, :166`). Benchmark runs `cargo bench … || echo "No benchmarks
       configured"` (`:179`), and the repository has no benches.
     - GitHub documents job-level `continue-on-error` as "allow a workflow run to pass when this job fails" [S4].
       Clippy's own guide says to run it with `-Dwarnings` "so that Clippy lints prevent CI from passing" [S5].
     - A screener who opens `ci.yml` finds all of this in a minute. Naming the gates turns "passed" into a
       definition on the page, and it gives Scrapy the credit it has earned.

5. **Cut the Python-API line; the project link heads the facts line.** As review 1 wrote it in must-fix 2.

6. **S1 says what it does, with a verb.** As review 1 wrote it in must-fix 4.

7. **The page renders use GitHub's `sub` rule** (`scratchpad/r6/renderset*.py`, the inline style; one rule).
   - The harness styles `sub{font-size:75%}` only. GitHub's stylesheet sets `sub, sup {font-size: 75%; line-height:
     0; position: relative; vertical-align: baseline}` and `sub {bottom: -0.25em}` [S11].
   - That's why the data line and the licence line show about 54 px between lines on the phone renders
     (`page-phone-6.png`), wider spacing than the body text. GitHub won't show that.
   - Why: reviewers judge the phone page from these renders. A spacing problem that isn't real could get "fixed" in
     the README and break the real page.

## Owner, outside this repository (new this round; not ranked; the carried items stand)

1. **Dependency advisories at `32c2651`.** I sent the 453 packages in Rust-sitemap's `Cargo.lock` to OSV
   (`api.osv.dev/v1/querybatch`, today). 24 crates have advisories [S7]. They include `rkyv 0.7.45` (RUSTSEC-2026-0001
   and -0235), `rustls-webpki 0.103.8` (four, among them RUSTSEC-2026-0098), `h2` (RUSTSEC-2026-0258), `openssl
   0.10.75`, `pyo3 0.22.6`, `quinn-proto`, `time` and `bytes`.
   - rkyv is printed in the "built on" line. RustSec lists the 0.7 series as "no longer supported upstream", with
     the fix only in 0.8.17 [S6].
   - `cargo update` clears most of the list. Then make `cargo audit` blocking, with an explicit `--ignore` for each
     advisory he has judged not to apply [S8], and plan the rkyv 0.8 move.
2. **WAL replay reads unchecked archives.** `orchestration/persistence.rs:47` (and sdist `main.rs:203`) calls
   `unsafe { rkyv::archived_root }` inside `catch_unwind`. `catch_unwind` "only catches unwinding panics" [S9], and
   undefined behaviour from a bad archive isn't a panic. The record's checksum is verified first (`wal.rs:135-143`),
   so this is defence in depth, but it's the first thing a storage reviewer will circle. `check_archived_root` is
   already used for nodes (`state.rs:719`), and the `validation` feature is on (`Cargo.toml:36`).
3. **The WAL's format comment names the wrong checksum.** `wal.rs:68` says `[u32 crc32c]`, but the code hashes with
   `crc32fast` (`:81`), which is "CRC32 (IEEE)", not Castagnoli [S10]. Fix the comment, or switch crates. The route
   anchor for S4 quotes that comment, so update the anchor in the same change.
4. **CI hygiene.** Use `cargo clippy --all-features -- -Dwarnings` and fix what it finds. Delete the Benchmark job
   until there's a bench. With those done, must-fix 4 prints "tests, rustfmt, clippy, cargo audit" for rustmapper by
   itself.
5. Carried: fix P1, ship 0.1.4 (the red box and the gap retire), commit the LICENSE, fix `resume` after a kill, pin
   Rust-sitemap and Scrapy first. I couldn't check upstream contributions from this session. The REST search API is
   closed here. If he has merged PRs in other people's projects, they're the most trusted signal a screener has
   ("third party verification of work quality" [S1]), and a line under "Also" could carry them, gated on the merge
   URL.

## Sources (new this round)

1. [S1] Marlow and Dabbish, "Activity traces and signals in software developer recruitment and hiring", CSCW 2013.
   Employers went to "the project where the applicant had made the most commits … and then assess[ed] the actual
   code". They distrusted watcher and follower counts, and trusted accepted contributions as "third party
   verification of work quality": https://www.cs.cmu.edu/~xia/resources/Documents/Marlow-cscw13.pdf
2. [S2] HR Dive on the Ladders 2018 eye-tracking study: the initial screen averages 7.4 s. Simple layouts with clear
   sections and headings did better than clutter and long sentences:
   https://www.hrdive.com/news/eye-tracking-study-shows-recruiters-look-at-resumes-for-7-seconds/541582/
3. [S3] Nielsen Norman Group, "Inverted Pyramid: Writing for Comprehension": "The who, what, when, where and why
   appear at the start"; it "gets to the point quickly and supports all types of readers":
   https://www.nngroup.com/articles/inverted-pyramid/
4. [S4] GitHub Docs, "Workflow syntax", `jobs.<job_id>.continue-on-error`: "Prevents a workflow run from failing when
   a job fails. Set to `true` to allow a workflow run to pass when this job fails":
   https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions
5. [S5] Clippy book, "Continuous Integration": "It is recommended to run Clippy on CI with `-Dwarnings`, so that
   Clippy lints prevent CI from passing": https://doc.rust-lang.org/clippy/continuous_integration/index.html
6. [S6] RustSec, RUSTSEC-2026-0235 (rkyv): "Insufficient archive validation can cause out-of-bounds reads in
   archives containing Rc/Arc". The 0.7 series is unsupported, and the fix is in 0.8.17:
   https://rustsec.org/advisories/RUSTSEC-2026-0235.html
7. [S7] OSV.dev API, `POST /v1/querybatch`, run today on the 453 `[[package]]` entries of Rust-sitemap's
   `Cargo.lock` at `32c2651`: 24 crates with advisories. Records read back from `/v1/vulns/<id>`:
   https://google.github.io/osv.dev/post-v1-querybatch/
8. [S8] cargo-audit README: it audits `Cargo.lock` "for crates with security vulnerabilities reported to the RustSec
   Advisory Database", has `--ignore` for advisories judged not to apply, and recommends the `audit-check` action on
   GitHub: https://github.com/rustsec/rustsec/blob/main/cargo-audit/README.md
9. [S9] Rust standard library, `std::panic::catch_unwind`: "This function _only_ catches unwinding panics, not those
   that abort the process", and it is "not recommended … for a general try/catch mechanism":
   https://doc.rust-lang.org/std/panic/fn.catch_unwind.html
10. [S10] crc32fast documentation: "Fast, SIMD-accelerated CRC32 (IEEE) checksum computation":
    https://docs.rs/crc32fast/latest/crc32fast/
11. [S11] github-markdown-css 5.8.1, the stylesheet that copies GitHub's Markdown rendering: `.markdown-body sub,
    .markdown-body sup { font-size: 75%; line-height: 0; position: relative; vertical-align: baseline }`:
    https://cdn.jsdelivr.net/npm/github-markdown-css@5.8.1/github-markdown.css

Clones and data:
- Rust-sitemap `32c2651`: `.github/workflows/ci.yml:76, :92, :109, :124, :154, :166, :179`;
  `src/orchestration/persistence.rs:45-70`; `src/state.rs:719`; `src/wal.rs:68, :81-89, :135-143`; `Cargo.toml:36`.
- sdist 0.1.3: `src/main.rs:203`.
- Scrapy `96e7a1a`: `.github/workflows/main.yml:19-25, :79-95`; `src/lakehouse/lakehouse_manager.py:364, :889-920,
  :1330-1460, :1886-1894`.
- ideal-url-organizer `159968a`: no regex URL parsing in `src` (rule 4 holds).
- `assets/stats.json`: `edition`, `runcheck.rustmapper.steps`, `repos[]` (`ci.jobs`, `ci_selection`, `lines`,
  `coauthored`), `figures`, `agent_authored`.
- `scripts/render_readme.py:380-436`; `tests/test_pipeline.py:488-503`; `tests/test_proof.py:230`.
