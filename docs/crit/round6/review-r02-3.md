# Review round 2, reviewer 3: every number needs a definition

10 Oct 2026. Reviewer: a data engineer. For every figure on the image and the page, I look for its key in
`assets/stats.json`, its row in `docs/data/AUDIT.md`, and its source in the clones, the 0.1.3 sdist
(`scratchpad/r6/sdist013`) or the live page it claims to measure. Build looked at: `scratchpad/r6/build/round-01/`
(desk and phone sheets, day and night; desk screens 1–2, phone screens 1–5; `gate.txt`), `README.md`, `SPEC.md`,
`LOG.md`, and reviews r01-1 to r01-3, r02-1 and r02-2. Findings fixed in round 1 are not repeated. Where r02-1 or
r02-2 already raised something (the `governor.rs` label, the run claim that leaves out `--seeding-strategy none`,
the WAL "because", "1 of 21" with no noun, "needs Rust"), I agree and don't argue it again. Everything below is new.

Verdict: **does not meet the goal. 5 / 10.** I would not ship it as is.

## The first question: does it meet the owner's goal?

The image does now. It teaches a stranger something true and useful about one of his real projects: how to start
rustmapper, the loop it runs for every page, the one way it goes wrong, the one way out, and the file you end up
with. The loop is the one thing a picture shows that a list can't. Nothing has a size, nothing names the theme, and
it reads at 390 px. Strip the colour and it still reads as directions. On purpose, the image passes.

The goal also has a standing rule: "honest data only, nothing invented or estimated; never print a figure without
a definition the audit stands behind". The page fails that rule in seven places. I could check each one in under a
minute from the clones or the live GitHub page, and so could any engineer who looks.

1. **The repository count is wrong: he has 22 public repositories, not 21.** His GitHub Repositories tab, filtered
   to Sources (no forks), lists **22**. The extra one is `excel-and-vba`: public, not a fork, 4 commits, updated
   7 Oct 2026. The README already links it inside "15 more". It is not in `stats.json` and was never cloned. The
   cause is in `build_stats.py:247`: with no GraphQL (`provenance.mode` `cache`, `graphql` `none`), the list of
   repositories is the previous file's names, so a repository made after the last live run can never be found. The
   page counts it once and the data leaves it out once: "1 OF 21" in the image, "clones of 21 public repositories"
   in the data line, and `commits` 2,033 doesn't include its 4. "15 more" is right only because it is typed by hand
   (2 flagships + 4 "Also" + 15 + the profile = 22).
2. **Three of the four working rules cite the wrong month, and one cites code an agent wrote.** The rules are the
   page's evidence for how he thinks, so their dates are data. The clones' history:
   - Rule 1, "Scrapy, Sep 2025: breakers on the Delta Lake, Redis and HTTP services". `HTTP_CIRCUIT_BREAKER`,
     `DELTA_CIRCUIT_BREAKER` and `REDIS_CIRCUIT_BREAKER` (`src/utils/retry.py:249-261`) first appear on
     **9 Nov 2025** in `e6fe879`, authored by **Claude**, on a sweep day. Delta Lake didn't exist in Scrapy until
     4 Oct 2025. What he wrote in September is one generic `CircuitBreaker` class (`error_handling.py`, `fd33c11`,
     29 Sep 2025, his own commit). The data line says agent commits "are not counted as mine", and the rule above it
     credits him with one.
   - Rule 2, "Scrapy, Sep 2025, the Delta Lake tables": the first `deltalake` code is **4 Oct 2025** (`52dcbd8`).
     "rustmapper, Oct 2025, the write-ahead log": `src/wal.rs` is added on **3 Nov 2025** (`4334458`). In October
     the repository had no WAL.
   - Rule 3, "Scrapy, Sep 2025: Prometheus and Grafana": September has only plan documents that mention them. The
     first `prometheus_client` code is **1 Oct 2025** (`d571e6e`) and the first Grafana dashboard is **6 Oct 2025**
     (`e8cbe15`).
   - Rule 4, "ideal-url-organizer, Nov 2025": holds (first commit and first `urllib.parse`, 9 Nov 2025).

   All four come from `chart.toml [[notices]]` with `source = "toml"`. Nothing checks them.
3. **"3 min on Linux x86_64" was measured on a warm cache, once, on an unnamed machine.** The run that produced
   179.8 s (`scratchpad/r6/rc2/runcheck.json`, written 23:55 UTC on 9 Oct) ran with `~/.cargo/registry` already
   holding **489 downloaded crates** (319 dated 21:35 and 170 dated 22:32 that evening, from earlier builds). It
   also ran with Rust 1.97.0 already installed, on 8 cores. `--no-cache-dir` stops pip reusing a wheel, but cargo's
   own cache is in `CARGO_HOME`, and pip doesn't touch it. So the figure leaves out downloading the crates and
   installing Rust, and it is a single run. AUDIT.md says it is "the time of that one run on that runner, not a
   forecast", but on the image it reads as a forecast for anyone on Linux.
4. **The facts line describes a different build from the one the page tells you to install.** "176 tests · 16k lines
   of Rust" are counts at `main` 32c2651 (161 Rust test attributes + 15 Python; 16,390 lines, both re-counted
   here). `pip install rustmapper` gives 0.1.3, which has **65** test attributes and **7,984** lines of Rust. The
   image draws 0.1.3, the code block installs 0.1.3, and the facts line between them gives main's numbers without
   saying so. That's two snapshots on one screen with nothing to tell them apart.
5. **"CI passed" has a definition the reader can't see.** Run 37704909539 did test 32c2651 on main, and its
   conclusion is success. Its Security Audit job ran `cargo audit` and exited 1, which shows as an annotation on
   the run. `ci.yml` marks that job `continue-on-error: true` at job and step level ("advisory debt; do not block"),
   and GitHub's docs say that setting lets "a workflow run to pass when this job fails". Every job runs on
   `ubuntu-latest` only, and the only prebuilt wheel is for macOS arm64. "Passed" is true as the workflow defines
   it. AUDIT.md's `ci` row should say what that definition leaves out.
6. **Three numbers typed into the prose have no source, and two are wrong.**
   - "25+ ways to sort a pile of URLs": `src/organizers/` holds exactly **25** `method_NN_*.py` files. The "+"
     comes from the repo's README heading, not from a count.
   - "Ai_code_detector … across seven languages": nothing in the repository says seven. The default config ingests
     12 extensions, which is **9 languages** (`configs/default.yaml supported_extensions`). Tree-sitter parsing
     covers 5. `LANGUAGE_MAP` names more than 20.
   - "Most pages get an extractive summary in stage 3": "most" is a share nobody measured. The code routes by a
     threshold of 50,000 characters of visible text (`stage2_worker.py:954-960`, verified). It doesn't count pages.
7. **AUDIT.md no longer describes what is printed.** It still says "The hero prints the first as 'CODE 32c2651 ·
   7 OCT 2026'" (cut in round 1). It still gives `claims.scrape_interval` the verdict "it is the light's period"
   (the light is gone), `commits` "2,032" (the file says 2,033), automation "dependabot 8" (the file adds
   github-actions 1), and routes "7 of 8 hold" (the entries changed). It has no row for the rules' dates and none
   for the hand-typed figures. The owner's rule is a definition "the audit stands behind". An audit that drifts from
   the page can't stand behind it.

None of this needs the image changed beyond one number. It needs the figures gathered, not typed. Until then, a
careful visitor's first check of a number finds it wrong, and that is the owner's oldest complaint: "the data
doesn't look exactly accurate."

## Figures checked

| Figure as printed | Key / source | Measured | Holds |
|---|---|---|---|
| 1 OF 21 (image); 21 public repositories (data line) | `repo_count` 21, cache mode, from previous names | GitHub Sources tab: **22**; `excel-and-vba` public, non-fork, unsurveyed | **no** |
| CI ON MAIN PASSED 7 OCT 2026; CI passed 7 Oct 2026 | `repos[Rust-sitemap].ci`; run 37704909539 | success on 32c2651, 23:54 UTC 7 Oct; Security Audit exit 1 under `continue-on-error`; ubuntu only | yes as the workflow defines it; definition unstated |
| 0.1.3 · 8 NOV 2025 | `edition.version/date`; PyPI JSON fetched today | 0.1.3 latest; wheel 19:52:41, sdist 19:52:42 UTC | yes |
| 3 min on Linux x86_64 | `runcheck.steps[install].secs` 179.8 | warm cargo registry (489 crates), Rust 1.97 present, n = 1, 8 cores | **not as a stranger's time** |
| `rust_sitemap` | `edition.scripts` | `["rust_sitemap"]` | yes |
| url, depth, status_code, title | routes R13; `sdist:src/state.rs` | present | yes |
| "with a test" | `handoffs[0].test` | `tests/test_import_rust_sitemapper.py` | yes |
| 176 tests · 16k lines of Rust | `test_functions` 176, `lines.Rust` 16,390 at 32c2651 | re-counted 161 + 15; 16,390. 0.1.3: 65 and 7,984 | yes for main; **unlabelled** next to a 0.1.3 install |
| 1,920 tests · CI passed 8 Oct 2026 · 69k lines of Python | Scrapy record | 1,920; success 8 Oct (recent: 1 success, 3 cancelled, 1 success); 69,036 | yes |
| CPython 3.13, Apple silicon | `edition.wheels` | `cp313-cp313-macosx_11_0_arm64` | yes |
| localhost:3000 | `docker-compose.yml:249` `"3000:3000"` | | yes |
| 50,000 characters | `config.py:389` `massive_doc_threshold=50000`; `len(text)` | characters of visible text | yes |
| "Most pages" | none | not measured | **no definition** |
| 25+ ways | none | 25 method files | **no** (25) |
| seven languages | none | 9 ingested, 5 parsed, 20+ mapped | **no** |
| 15 more repositories | hand-typed | 22 − 1 profile − 2 − 4 = 15 | yes, by luck |
| Rule 1 "Sep 2025" | `chart.toml` notices | named breakers 9 Nov 2025, authored by Claude | **no** |
| Rule 2 "Sep 2025" / "Oct 2025" | `chart.toml` notices | Delta Lake 4 Oct 2025; WAL 3 Nov 2025 | **no** |
| Rule 3 "Sep 2025" | `chart.toml` notices | Prometheus 1 Oct, Grafana 6 Oct 2025 | **no** |
| Rule 4 "Nov 2025" | `chart.toml` notices | 9 Nov 2025 | yes |
| measured 10 Oct 2026; run 9 Oct 2026 | `taken`; `runcheck.date` | | yes |
| 3 %; 297 | `coauthored_total.agent_share` 63/2,033; `agent_authored.total` | | yes, over 21 of 22 repositories |
| `32c2651` | `repos[Rust-sitemap].head.short` | | yes |

## Every element of the image

| Element | What a stranger learns | Verdict | Why |
|---|---|---|---|
| Name | whose page | keep | |
| Role line, two caps lines | crawlers and data; Python and Rust | keep | the drawing below proves it |
| "RUSTMAPPER · 1 OF 21" | one project picked from his public work | change | the number is wrong (22). Print "1 OF 22 PUBLIC REPOSITORIES", which a visitor can check against his Repositories tab in one click. The noun comes from r02-2 |
| "CI ON MAIN PASSED 7 OCT 2026" | main is tested and recent | keep, once defined | true by the workflow's definition; AUDIT must say what that leaves out (audit advisory, Linux only). r02-1's repeat finding stands |
| "rustmapper" + sentence | what it does | keep | |
| Start and end bars | where it begins and ends | keep | they bracket the loop |
| `pip install rustmapper` + 0.1.3 · 8 NOV 2025 | how to get it; the release's age | keep | both figures verified today on PyPI |
| "3 min on Linux x86_64: pip builds it from source" | what installing costs | change | a single warm-cache run on a machine with Rust. Measure it cold, or cut the figure (must-fix 3) |
| `rust_sitemap crawl --start-url <site>` | the command that exists | keep | `edition.scripts`; r02-1's repeat finding stands |
| Track | read in order | keep | |
| Loop line + up arrow | which rows repeat for every page | keep | the one thing only a drawing shows |
| seeder ring + line | where URLs come from, by default | keep | true for 0.1.3 (`cli.rs:58` `"all"`) |
| fetch ring + line, `bfs_crawler.rs` | it's a crawl loop on one site | keep | anchors hold in both trees |
| governor tick + line | it slows when storage lags | keep | r02-2's label fix stands |
| WAL ring + line | a kill doesn't lose the record | keep | r02-1's cause fix stands |
| Hatch + hazard line | it never ends by itself; scope is wider than you think | keep | probe `ends_by_itself` false at 150 s; `url_utils.rs:88-90` |
| Ctrl-C ring + line | the only exit, and what each exit leaves | keep | probes `crawl_ctrl_c`, `kill_writes_file` |
| `data/sitemap.jsonl` + fields | the output, with the real field names | keep | `SitemapNode` in both trees |
| Thin line, arrow, "read by ideal-url-organizer …, with a test" | his projects connect, and the join is tested | keep | `handoffs[0].state` `runs` |
| Night edition | the same in dark | keep | |

## Every block of the page

| Block | What it teaches | Verdict | Why |
|---|---|---|---|
| Image | how to run his main tool, how it behaves | change | one number (must-fix 1) and the install figure (3) |
| Alt text | the image in 25 words | keep | no figures in it |
| Link line | where to go | keep | |
| Builds / Languages / Stack | who he is | keep | |
| rustmapper sentence | what it is | keep | |
| rustmapper facts line | tested, alive, how big | change | label the snapshot: these are main's counts, not the release's (must-fix 4) |
| Install code block | copyable commands | keep | |
| Wheel note | when pip just works | keep | the right home for the install condition and any measured time |
| Scrapy sentence, facts line | the second project | change | same snapshot label (must-fix 4) |
| Scrapy code block + note | how to start it, three catches | keep | port 3000 and the `scout` name verified |
| Scrapy bullets | how it's built | change | bullet 3: drop "Most" (must-fix 6) |
| Also | four more projects | change | "25+" → "25"; "seven languages" → "nine languages" or no number (must-fix 6) |
| 15 more `<details>` | the rest | change | compute the 15, and gate the list against the surveyed set (must-fix 1) |
| Working rules | how he works, each with dated proof | change | three of the four dates are wrong and rule 1 cites agent code (must-fix 2) |
| Found a mistake? | the page can be corrected | keep | it is the right invitation, and I used it |
| Data line | what was checked, when, on what | change | 21 → 22; the install's conditions (must-fix 3); r02-2's clauses stand |
| License | terms, how to fork | keep | |

## Must fix, ranked

1. **Count every public repository, and gate the page against the count.** (`scripts/build_stats.py`,
   `scripts/data/github.py`, new check `scripts/checks/repos.py`; about 60 lines.) In cache mode, list repositories
   with REST `GET /users/{login}/repos?type=owner&per_page=100` (one request, public data only, each row has
   `fork`). Keep `fork == false` and take the union with the cached names. Clone any new one the way live mode does.
   `repo_count` then reads 22, and `excel-and-vba`'s commits join `commits`. New fast-tier check REPO-SET: every
   `github.com/<login>/<name>` linked in README.md's visible text is a key of `stats.repos`, and every key except
   the profile repository is linked exactly once. Write the "15 more" number from `repo_count − 1 − flagships −
   also`, and fail if the `<details>` list has a different length. Image fine print: "1 OF 22 PUBLIC REPOSITORIES"
   (desk `label` 19, tracking 1.6; check it fits x 56–410; else "1 OF 22 PUBLIC REPOS"). Data line "22". Why: the
   one number in the title block is wrong, and the pipeline can't see new work.
2. **Compute the rules' dates from the history, and cite only his own commits.** (`chart.toml [[notices]]`,
   `scripts/data/notices.py` or `claims.py`, `scripts/checks/notices.py`.) Give each cite an anchor
   `{repo, text}`. The build runs `git log --reverse --format='%as %an' -S<text>` on the history clone and takes the
   first commit whose author matches `[identity]`. The printed month is that commit's month. NOTICE-DATE fails if
   the typed month differs. NOTICE-AUTHOR fails if the first commit adding the anchor is by an agent, unless the
   cite names the agent. Corrected text for today: rule 1 "Scrapy, Sep 2025: a circuit breaker in the error
   handler" (anchor `class CircuitBreaker`, `fd33c11`). Rule 2 "Scrapy, Oct 2025, the Delta Lake tables;
   rustmapper, Nov 2025, the write-ahead log" (`write_deltalake`, `52dcbd8`; `src/wal.rs`, `4334458`). Rule 3
   "Scrapy, Oct 2025: Prometheus metrics, then Grafana dashboards" (`prometheus_client`, `d571e6e`; dashboard,
   `e8cbe15`). Rule 4 unchanged. Add an AUDIT row. Why: a dated claim on his working habits that a stranger can
   disprove from `git log` costs more than having no date.
3. **Measure the install cold, or don't print a time.** (`scripts/runcheck.py` install step, about 15 lines.) Run
   the install with `CARGO_HOME` set to a fresh temporary directory, so the crates are downloaded inside the timed
   step. Record `rustc --version` (or "none"), `os.cpu_count()` and `cache: "cold"` in the step's `detail`. Run it 3
   times and keep the median and the range. The sheet prints the figure only when `cache == "cold"`, and the wheel
   note carries the condition: "elsewhere pip compiles it from source, which needs a Rust toolchain: 3–4 min on an
   8-core Linux machine". If the image keeps an install line, it carries no number until the macos-14 job supplies
   the wheel's time. Add a test: a step without `cache: "cold"` prints no time. Why: one run on a warm cache with
   an unnamed machine fails the most basic benchmarking rule, which is to state the platform and the variance.
4. **Label each facts line with the snapshot it counts.** (`scripts/render_readme.py` facts writer.) Write "On main
   at `32c2651`: 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust" from `repos[].head.short`. Do the same for
   Scrapy (`96e7a1a`). Don't add the release's counts. Just say which snapshot this is. Add a test: the facts line
   contains `head.short`. Why: the image and the code block are 0.1.3 (65 tests, 8k lines) and the line between
   them is main (176, 16k). Unlabelled, the reader takes them as one thing.
5. **Define "CI passed" in the audit, from the jobs.** (`scripts/data/github.py rest_runs()`, AUDIT `ci` row.) Also
   fetch `GET /repos/{o}/{r}/actions/runs/{id}/jobs` and store each job's `name`, `conclusion` and `labels`
   (`runs-on`). The AUDIT row reads: "the conclusion of the latest completed push run on the default branch, as the
   workflow defines it: jobs marked continue-on-error (Rust-sitemap: Security Audit) don't count; every job ran on
   ubuntu-latest". If any job's conclusion is `failure`, the words become "CI passed, <job> failed (not
   blocking)". Today that can't happen, because the step-level setting reports success. The words stay "CI passed"
   and the definition is in the audit, where an engineer looks. Why: a green check with a hidden red job is the
   pattern engineers have learned not to trust.
6. **Remove the hand-typed numbers that nothing backs, and gate the rest.** (README prose, new `chart.toml
   [[figures]]`, new fast check FIGURES.) ideal-url-organizer "25+ ways" → "25 ways". Ai_code_detector "across
   seven languages" → "across nine languages" (source `src/ai_code_detector/configs/default.yaml
   supported_extensions`) or drop the number. Scrapy bullet 3 "Most pages get" → "Pages get". FIGURES: every digit
   run or number word in README visible text and in the hero's text, outside generated marker blocks, must match a
   `[[figures]]` row `{text, repo, path, literal}` that holds at that repository's HEAD. Today's rows: 25, nine,
   50,000, 3000, 3.13. Why: the owner's rule covers every figure, not just the generated ones.
7. **Bring AUDIT.md level with the page.** (`docs/data/AUDIT.md`.) Fix the stale rows: hero prints, scrape-interval
   verdict, 2,033, github-actions 1 (total 306), current route entries. Add a §7 "Printed figures" table, one row
   per figure on the page (the "Figures checked" table above is a start) → key or `[[figures]]` row → definition →
   check. Better, generate that table with `scripts/audit_figures.py` from the sheet's `PURPOSE` table, the marker
   blocks and `[[figures]]`, so it can't drift. Why: the definition has to live where the reader is sent, and today
   that place is out of date.

## Sources (fresh this round)

1. GitHub, BenjaminSRussell's Repositories tab, Sources filter, read 10 Oct 2026: "22 results", `excel-and-vba`
   among them, no forks. https://github.com/BenjaminSRussell?tab=repositories&type=source (must-fix 1)
2. GitHub, `BenjaminSRussell/excel-and-vba`: public, not a fork, 4 commits.
   https://github.com/BenjaminSRussell/excel-and-vba (must-fix 1)
3. GitHub REST, "List repositories for a user": public repositories of a user, `type=owner`, each with a required
   `fork` boolean. https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user (must-fix 1)
4. git-log documentation: `--reverse`; `%as` author date versus `%cs` committer date (rebases keep the author
   date). https://git-scm.com/docs/git-log (must-fix 2: date the rules by author date, oldest first)
5. GitHub Docs, "Creating a commit with multiple authors": how the `Co-authored-by` trailer attributes a commit.
   https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors
   (must-fix 2: authorship decides whose work a rule may cite)
6. The Cargo Book, "Cargo Home": downloaded crates are kept in `registry/cache` and unpacked into `registry/src`;
   the location moves with `CARGO_HOME`. https://doc.rust-lang.org/cargo/guide/cargo-home.html (must-fix 3)
7. Gernot Heiser, "Systems Benchmarking Crimes": "Raw averages, without any indication of variance, can be highly
   misleading"; "it is essential that the evaluation platform is well-specified".
   https://gernot-heiser.org/benchmarking-crimes.html (must-fix 3)
8. rustup book, Installation: a new user installs `rustc` and `cargo` through rustup before any source build.
   https://rust-lang.github.io/rustup/installation/index.html (must-fix 3: the time a stranger waits includes this)
9. maturin, "Distribution": building from the sdist compiles the Rust code; `maturin generate-ci` and manylinux
   images build wheels for other platforms. https://www.maturin.rs/distribution.html (must-fix 3)
10. GitHub Docs, Workflow syntax, `jobs.<job_id>.continue-on-error`: "Set to `true` to allow a workflow run to pass
    when this job fails"; steps: "allow a job to pass when this step fails".
    https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax (must-fix 5)
11. Onur Kesim, "Do not trust the green checkmark" (DEV): a step with `continue-on-error: true` reports
    `conclusion: success`; the failure sits only in `outcome`. https://dev.to/onurkesim/do-not-trust-the-green-checkmark-48i5
    (must-fix 5: why the run's success can't show the audit failure)
12. GitHub REST, "List jobs for a workflow run": per-job `conclusion`, `labels` and steps.
    https://docs.github.com/en/rest/actions/workflow-jobs#list-jobs-for-a-workflow-run (must-fix 5)
13. GitHub Actions run 37704909539, Rust-sitemap: push to main, commit 32c2651, 7 Oct 2026 23:54, Success; Security
    Audit "Process completed with exit code 1"; jobs on ubuntu-latest only.
    https://github.com/BenjaminSRussell/Rust-sitemap/actions/runs/37704909539 (finding 5)
14. Google, *Site Reliability Engineering*, ch. 4 "Service Level Objectives": "standardize on common definitions
    for SLIs" (aggregation interval, region, frequency, which requests, how the data is acquired).
    https://sre.google/sre-book/service-level-objectives/ (must-fix 6, 7: one written definition per figure)
15. PyPI JSON for rustmapper, fetched 10 Oct 2026: 0.1.3 latest; one cp313 macOS arm64 wheel (19:52:41) and the
    sdist (19:52:42). https://pypi.org/pypi/rustmapper/json (figures table)
16. Clones and release, checked for this review: Scrapy `e6fe879` (Claude, 9 Nov 2025, the three named breakers,
    `src/utils/retry.py:249-261`), `fd33c11` (`class CircuitBreaker`, 29 Sep 2025), `52dcbd8` (`write_deltalake`,
    4 Oct 2025), `d571e6e` (`prometheus_client`, 1 Oct 2025), `e8cbe15` (Grafana dashboard, 6 Oct 2025),
    `docker-compose.yml:249`, `src/core/config.py:389`, `src/stage2/stage2_worker.py:950-960`; Rust-sitemap
    `4334458` (`src/wal.rs` added, 3 Nov 2025), `.github/workflows/ci.yml:44, 150-166`, 161 test attributes and
    16,390 lines at 32c2651; sdist 0.1.3: 65 attributes, 7,984 lines; ideal-url-organizer `src/organizers/` (25
    `method_*.py`), `6e8087f` (9 Nov 2025); Ai_code_detector `configs/default.yaml:5-17`,
    `ingest/file_filter.py:25-50`, `analysis/tree_sitter_parser.py`; `~/.cargo/registry/cache` (489 crates, 21:35
    and 22:32 UTC, 9 Oct) and `scratchpad/r6/rc2/runcheck.json` (23:55 UTC); `scripts/build_stats.py:247`.
