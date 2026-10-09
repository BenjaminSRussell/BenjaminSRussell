# How the profile's figures are gathered — audit, 9 Oct 2026

Branch `v11/data`, from `main` at eeea9d1. Everything below was checked by reading the code, running the
builder in cache mode (`python3 scripts/build_stats.py --mode cache`), and cloning the 21 repositories into a
scratch directory to count things the builder did not count yet. GitHub's GraphQL API is not reachable from
this machine, so the live-only figures (`calendar_*`, followers, stars) could not be re-measured here; what
they mean is established from the queries and from GitHub's documented rules.

## 1. What was wrong, in four lines

1. The page printed three commit numbers side by side without saying what each counted: `1,665 commits`
   (yours, all time, 21 public repositories, 7 Oct), `1,966 all hands` (everyone's, same clones), `1,828 by
   GitHub's calendar`. The third one was never measured by this pipeline: it is a number the v7 README
   carried with `seeded: true` and the v2 builder kept copying forward with the instrument marked "GraphQL
   cached". The v2 validator forbids a `seeded` key, but the value had already lost that label.
2. The CI warning `clones 1894 vs calendar 6487: 71 % apart` compared two different things. 1,894 is your
   commits in the last 52 weeks from the clones; 6,487 is GitHub's "contributions" over the same year, which
   adds issues, pull requests and reviews to commits. You filed 930 issues on Scrapy in the last year (917 of
   them in September 2026) and opened about 250 pull requests, so the two numbers were never going to agree.
   The check has been rewritten to compare commits with commits, on the same repositories, over the same days.
3. The weekly series is dominated by one day. 7 Oct 2026 carries 514 of your commits across 19 repositories;
   198 of them are merge commits of pull requests (132 from `bot/` branches) and 442 were committed through
   GitHub's web merge button. It is a real day of merging, not a week of hand work, and the data did not say so.
   `weeks[].sweep` and `tide.hw.sweep_share` now carry that fact (71 % of the current top week).
4. Smaller leaks: a repository's `first`/`last` dates fell back to other people's commits when yours were
   absent; `--out` silently doubled as the cache path; the top-level `stars` (seeded 0) disagreed with the
   per-repository stars read live (Scrapy 1, Rust-sitemap 1).

## 2. How each figure is produced

Files: `scripts/build_stats.py` (the builder), `scripts/data/survey.py` (clones and `git log`),
`scripts/data/derive.py` (everything computed from the per-repository records), `scripts/data/github.py`
(GraphQL and REST), `scripts/checks/data.py` (the CI gate's data checks). Line numbers are for `v11/data`.

**Which repositories.** Live: GraphQL `repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC,
first: 100)` (`github.py:36`), so public, non-fork, owned by the account, archived ones included, at most 100.
Cache mode: the names in the previous `stats.json` (`build_stats.py:234`). Each is cloned bare and without
file contents (`--bare --filter=blob:none`, `survey.py:109`), 180 s timeout, six at a time; a clone that fails
keeps its previous record marked `stale` (`build_stats.py:273`). Only `HEAD` is read: the default branch and
everything merged into it. Other branches are only looked at for the stale-branch count.

**Whose commits.** A commit is yours when its *author* name is one of `[identity] names`, or its author email
is one of `[identity] emails`, or it is a `@users.noreply.github.com` address containing your login
(`survey.py:77`, list in `chart.toml [identity]`). The committer field is ignored, so a squash made through
GitHub's merge button (committer "GitHub") is yours. `Co-authored-by` trailers do not move a commit: a commit
authored by "Claude" with you as co-author is Claude's; a commit authored by you with a Claude trailer is yours
(it is now counted in `co_authored`). Merge commits count like any other commit (now counted in `merges`).
Bots are not dropped from `all_hands`; they are listed in `others[]` with `bot: true`.

**Over what window.** All-time for `commits`, `all_hands`, `commit_days`, `hours`, `weekdays`, `first`,
`last`; the last 52 ISO weeks (Monday starts, the week containing `taken` included) for `weeks[]`, `tide`
and `calendar_check` (`survey.py:201`); the last 365 days and the 365 before for `variation`
(`derive.py:139`). On 9 Oct 2026 the 52-week window starts 13 Oct 2025 and leaves out 142 of your commits
made between 25 Sep and 12 Oct 2025.

| key | how it is produced |
|---|---|
| `commits` | Σ over repositories of commits on `HEAD` whose author matches `[identity]` (`survey.py:238,264`; sum at `derive.py:182`). All time. Cache 7 Oct: 1,665. Today: 2,032. |
| `merges` (new) | Of `commits`, those with two or more parents (`survey.py:265`). Today: 405 (20 %). |
| `coauthored` (new) | Of `commits`, those carrying a `Co-authored-by` trailer: `{count, share, agent, names}` (`survey.py`, `coauthored()`). `count` = any trailer; `agent` = a trailer naming a `[identity] bots` name (exactly or as its first word, "Claude Sonnet 5") or a `[bot]` account; `names` = the non-self co-author names with counts. Today: 502 (25 %) carry a trailer, 440 of them naming you yourself (GitHub's squash-merge adds the PR author), 63 naming a Claude model. Top-level `coauthored_total` is the same shape over every repository. |
| `all_hands` | Every commit on `HEAD` by anyone, bots included (`survey.py`, `summarize()`). 7 Oct: 1,966 = 1,665 yours + 301 others (jules 125, Claude 162, dependabot 4, …). |
| `calendar_total` | GraphQL `contributionsCollection(from, to).totalCommitContributions`, one query per calendar year since the account was created, summed (`github.py:105`). GitHub's own rule: commits on the default branch (or `gh-pages`) of any non-fork repository the viewer can see, where the commit's author email is linked to the account. Private repositories only if the profile shows private contributions. **The cached 1,828 was seeded in v7 and never measured by this pipeline** (`git show 4b1c299:assets/stats.json`: `"seeded": true`). Cache mode now carries it only when `provenance.graphql_at` says when it was fetched (`build_stats.py:56`); until the next live run it is `null`. |
| `calendar` (new) | The same collection asked once for the 52 clone weeks: `commits`, `issues`, `pull_requests`, `reviews`, `restricted` (private), `all` (the green squares) and `commits_by_repo` for your own public repositories (`github.py:50,121-143`). Live only. |
| `calendar_weeks` | The green-square calendar per week over that window: every contribution type, Sunday-start weeks (`github.py:124`). Live only. It is not comparable with `weeks[]` and is no longer compared with it. |
| `calendar_check` | Σ `weeks[].n` against Σ `calendar.commits_by_repo` over the surveyed repositories (`derive.py:202`). Both are commits, by you, on default branches, on the same repositories, over the same days. Remaining differences: an author email not linked to the account (GitHub drops it), UTC days vs author-local days at the window's edges. The gate warns above 10 % (`checks/data.py:27,62`). |
| `repo_count` | GraphQL `repositories.totalCount` under the filter above, else surveyed + unsurveyed (`build_stats.py:144`). The "24" in v7 was seeded and most likely GitHub's public-repository count, which includes forks; the GraphQL filter excludes them, hence 21. Not confirmable from this machine (the user listing is blocked here); the next live run's `unsurveyed[]` is the arbiter. |
| `first_commit` / `days_surveyed` | Earliest `repos[].first` (`derive.py:185`) and the days from it to `taken` (`derive.py:186`). `first` is now the earliest of *your* commits in that repository (`survey.py:256`); before this branch a repository with none of your commits reported someone else's dates. 25 Sep 2025; 379 days. Note the name: it is the span of the history, not of the surveying. |
| `hours[24]` / `weekdays[7]` / `hours_basis` | Per repository, one entry per author-local commit-day: the day's most common hour (ties to the earliest) and its weekday (`survey.py:207,254`); summed over repositories (`derive.py:187`). The unit is repository-days: a day you touched 18 repositories counts 18 times (7 Oct does). `hours_basis` is the constant string that says so. 150 repository-days on 77 distinct dates (7 Oct). |
| `tz_offsets` | Count of your commits per author offset (`survey.py:259`, summed `derive.py:190`). 7 Oct: `-0400` 1,003, `-0500` 662, nothing else: every commit was authored on US Eastern time (daylight / standard). True and unused. |
| `variation` | Most common commit-day hour in the last 365 days (`hour`) and the 365 before (`prior_hour`); `annual_change` only when both windows have ≥ 60 commit-days (`derive.py:137`). Today: 14 h vs 13 h, prior window has 15 days, so no change is stated. Unit: repository-days. |
| `weeks[52]` | `n` = your commits per ISO week summed over repositories; `days` = distinct dates in the week with a commit (≤ 7); `repos` = commits per repository; `sweep` (new) = commits in the week that fell on sweep days (`derive.py:61`). Unit: **commits**, not days. |
| `tide` | `hw` = the week with most commits (`n`, the repository with most of them as `cause`, that repository's longest run of consecutive commit-days overlapping the week as `cause_days`, `cause_share`, and now `sweep_share`); `lw` = the fewest commits among complete weeks; `median` of complete weeks; `slack` = the lowest four-week sum (`derive.py:97`). 7 Oct cache: `hw` = week of 5 Oct, 358 commits, 100 % of them on the 7 Oct sweep day. Today: 725, 71 % on sweep days. |
| `sweeps` / `sweep_dates` | Dates on which ≥ `sweep_threshold` repositories had a commit-day of yours; threshold = ⅓ of the repositories, capped at 5, never under 2 (`derive.py:35,40`); `sweep_dates` is the plain list. They are removed from `active`/`dormant` and from the round-5 keys `months`, `first_ns`, `last_ns` (`derive.py`, `months_without_sweeps()`), never from `weeks`, `tide`, `hours` or `commit_days`. Four today: 9 Nov 2025 (13 repos, 31 commits), 10 Nov 2025 (10, 15), 1 Oct 2026 (6, 13), 7 Oct 2026 (19, 514). |
| `repos[].months` (new) | Commit-days of yours per month, `{YYYY-MM: days}`, sweep days excluded; a month with none is absent. Rust-sitemap: `{"2025-10": 7, "2025-11": 9, "2025-12": 1, "2026-05": 1, "2026-08": 1}`. The series D1 draws. |
| `repos[].first_ns` / `last_ns` (new) | First and last commit-day of yours that is not a sweep day; `null` when every day was a sweep (Course_crusader, Elusive_trades_data, Spotify_to_apple_music, rust_llm_logger, mlx_Qwen_data_entry today). Rust-sitemap: 20 Oct 2025 – 8 Aug 2026 (its raw `last` reads 7 Oct 2026, the sweep). |
| `repos[].tests` (new) | Files at `HEAD` named `test_*.py`, `*_test.py`, `*_test.go`, `*.test.ts/.tsx/.js`, `*.spec.ts`, `*Tests.swift`, or any `.rs` under a `tests/` directory, vendored directories excluded (`tree.py`, `TEST_PATTERNS`). Scrapy 257, Rust-sitemap 3, cozy-game 0. A count of files, not of tests or of coverage. |
| `repos[].workflows` (new) | Files `.github/workflows/*.yml|yaml` at `HEAD` (`tree.py`, `WORKFLOW`). Scrapy 5, Rust-sitemap 1; cozy-game and 2d-swift-widgets 0. |
| `repos[].manifest` (new) | `{files, deps}`: the manifests found at the root or one directory down (`Cargo.toml`, `pyproject.toml`, `package.json`, `go.mod`, `Package.swift`) and the dependency names they declare, in file order, deduplicated, capped at 40, dev/test groups and transitive dependencies left out, Go module paths reduced to their last segment (`tree.py`, `deps_from()`). `null` when there is no manifest; `requirements.txt` is not read. Rust-sitemap: `clap, rkyv, rkyv_derive, redb, reqwest, tokio, …` (40). |
| `repos[].lines` (new) | `{language: lines}` at `HEAD` from a depth-1 clone (`survey.py`, `clone_head()`; `tree.py`, `lines_by_language()`): newlines of files whose extension names a programming language (`tree.LANGUAGES`), skipping binary files, files over 512 KB, the directories in `chart.toml [lines] exclude_dirs` (node_modules, vendor, target, build, dist, .venv, venv, __pycache__, site-packages, third_party) and the per-repository `[lines.exclude]` paths (game_engine `src/engine`, 5,212 generated C files). Rust-sitemap `{"Rust": 16390, "Python": 848}`; Scrapy `{"Python": 69036, "JavaScript": 2561, "Shell": 2334, "HTML": 1883, "Rust": 1003, "SQL": 232}`. Lines in the clone, not lines you typed: game_engine still holds 151,872 lines of C outside `src/engine`. |
| `repos[].ci` (new, flagships only) | REST `actions/runs?branch=<default>&event=push&status=completed&per_page=5` (`github.py`, `rest_runs()`): the project's own CI on its default branch, latest run's `{workflow, conclusion, date, url}` and the last five conclusions as `recent`. Pull-request runs and Dependabot's updater runs are left out on purpose (Scrapy's latest run of any kind is a failed Dependabot update). Absent when the API does not answer; carried from the cache with `stale: true` when it did before. Scrapy: `CI/CD Pipeline`, success, 8 Oct 2026, recent `[success, cancelled, cancelled, cancelled, success]`; Rust-sitemap: `CI`, success, 7 Oct 2026, five successes. |
| `repos[].commit_days` / `months_active` / `days[]` | Distinct author-local dates with a commit of yours in that repository; distinct months; the per-date list (`survey.py:207`). 155 repository-days today. |
| `repos[].active` / `dormant` | Commit-days in ≥ 3 of the last 12 weeks; no commit-day in 90 days; both with sweep days removed (`derive.py:51`). |
| `languages` | Live: GraphQL bytes per language, top 8 per repository, summed over the public non-fork repositories, top 5 + Other (`github.py:160`). Cache mode: the REST `/languages` endpoint per repository (all languages, not top 8) when it answered for every repository, else nothing (`build_stats.py:239-243`). These are GitHub's linguist byte counts and include vendored and generated files as linguist classifies them. The cached shares were seeded in v7 and are no longer carried. |
| `stars` / `followers` / `account_since` | GraphQL: Σ `stargazerCount` over the same repositories, `followers.totalCount`, `createdAt` (`github.py:98-118`). Cache mode now: `stars` = Σ REST stars when every repository answered (`build_stats.py:244`); the other two `null` without a dated fetch. The seeded values were 0 / 46 / Oct 2024. |
| `repos[].stars` / `language` / `archived` | GraphQL node or REST `/repos/{owner}/{repo}` per repository (`github.py:188`, `build_stats.py:282-284`). |
| `unsurveyed` | Repositories GraphQL listed that produced no record: clone failed with no cached record, or `HEAD` has no commits (`derive.py:230`). Always empty in cache mode (no GraphQL list). |
| `claims` | `chart.toml [claims.*]`: figures about the code, not about you; `measured` only with a `source` and `sha` (`claims.py:26`). Not a measurement of the clones. |
| `sources` | `chart.toml [[sources]]` labels (`build_stats.py:202`). Copy, not data. |
| `provenance` | `mode` (live / cache / cache-failed), `instruments` (each of clones, graphql, rest, pypi, releases: live / partial / cache / none), `soundings_taken` = days in the last 150 on which `assets/stats.json` was committed (`build_stats.py:78`; needs `fetch-depth: 0`, `profile.yml:49`), `graphql_at`. |
| `edition` / `notices` | PyPI JSON for `rustmapper` (`pypi.py:62`: latest version, its first upload date, release count, wheel tags, every version's first upload); notices from the flagship's GitHub Releases, else the PyPI uploads, plus `Notice:` commits of yours in the profile repository, plus `chart.toml [[notices]]` (`releases.py:66`). Fact: the four PyPI uploads are 0.1.0 at 18:38, 0.1.1 at 18:41, 0.1.2 at 19:51 and 0.1.3 at 19:52 UTC on 8 Nov 2025, 74 minutes end to end. |
| `trial` | Scrapy's `exports/run-YYYY-MM-DD.json` at `HEAD`, latest by name (`build_stats.py:92`). None exists: `null`. |
| `corrections` | Your commits in the profile repository, numbered per year (`derive.py:220`). 4 in 2025, 169 in 2026 (cache). |

**The workflow** (`.github/workflows/profile.yml`): Sundays 06:20 UTC and on pushes to `main` that touch the
scripts; `permissions: contents: write`; the builder runs with `secrets.GITHUB_TOKEN` (`profile.yml:74`), the
repository's own installation token. That token reads public data only: GraphQL sees your public
contributions and whatever private contributions the profile chooses to show as a bare count
(`restrictedContributionsCount`); it cannot list or read private repositories. Live mode is "token present".

**Cache mode vs live.** Cache mode clones exactly as live does; it differs in three things: the repository
list comes from the previous file, not GraphQL; the GraphQL figures come from the previous file (now only when
that file records a dated fetch), not from the API; repository metadata comes from unauthenticated REST (60
requests per hour; 21 repositories need 42) and is marked `partial` when any request fails. The committed file
on `main` is a cache-mode file from a local run on 7 Oct; the live runs on GitHub have not committed their
output (the `chart` workflow's commit step pushed nothing that reached `main`), so the live `6,487` exists only
in a job log.

## 3. Reconciling the numbers

| number | what it is |
|---|---|
| **1,665** | Your commits on `HEAD` of 21 public repositories, all time, from clones taken 7 Oct 2026 19:47 UTC. |
| **1,966** | Everyone's commits on the same `HEAD`s: 1,665 + 301 by Claude (162), google-labs-jules (125), dependabot (4) and others. |
| **1,828** | Seeded in v7 (`"seeded": true`), copied into v2 as `calendar_total` and labelled "GraphQL cached". Not a measurement of anything this pipeline did. Dropped until a live fetch replaces it. |
| **1,894** | Your commits in the 52 ISO weeks ending 11 Oct 2026, from the live run's clones (8 Oct). My clone on 9 Oct gives 1,890 for the same window; the 4 extra are most likely commits in repositories GraphQL listed that the cache does not (the live set may be larger than 21), or history rewritten since. Not the same quantity as 1,665: the window starts 13 Oct 2025 and leaves out 142 commits. |
| **6,487** | GitHub's contributions over that year: commits **plus** issues, pull requests and reviews, across every repository GitHub credits to you. Measured parts: 930 issues you filed on Scrapy in the last 365 days (980 all time, all by you, 917 in September 2026), ~250 pull requests of yours on Scrapy alone (278 all time; dependabot 53). The remainder beyond the 1,894 commits is pull requests and issues on the other repositories, reviews, and any private contributions the profile shows; the new `calendar` block itemises this on the next live run. |
| **2,032 / 2,337 / 1,890** | The same three clone figures on 9 Oct 2026 (your commits, everyone's, yours in the 52 weeks). 367 of your commits were added between 7 and 9 Oct: Data_science_dev +159, Scrapy +155, Rust-sitemap +14, the profile +10, … |

The 7 Oct 2026 day: 514 of your commits across 19 repositories; 198 are merge commits (`Merge pull request #N
from BenjaminSRussell/bot/…` 132 times, `fix/…`, `feat/…`, `chore/…`); 442 have committer "GitHub"
(the web merge button); 238 carry a `Co-authored-by` trailer. The week of 5 Oct is 725 commits, 514 of them on
that day, 198 merges. Eighteen of the 21 repositories have `last = 2026-10-07` because of it.

Other facts the memos asked for, from the clones: 20 of 21 repositories carry GitHub Actions workflows
(`.github/workflows/*.yml`; cozy-game has none) and test files (Data_science_dev 375, Scrapy 327, game_engine
110; cozy-game none), so "no CI/tests detected" is not what the clones show; **no repository has a single git
tag**, so there are no release tags anywhere (rustmapper's four versions exist on PyPI only).

## 4. Verdicts

Keep = well defined and measured; Define = keep only with the plain-words definition printed beside it;
Drop = ill defined or unmeasured, leave off the page and the sheets.

| figure | definition (plain words) | unit | verdict |
|---|---|---|---|
| `commits` | commits authored by you on the default branch of the N public non-fork repositories, all time, counted from clones on `taken` | commits | Define (say "authored by me", "default branches", the count of repositories, the date) |
| `merges` | of those, merge commits (two or more parents) | commits | Keep, new |
| `co_authored` | of those, commits carrying a Co-authored-by trailer (mostly your own PR-squash trailer; 63 name a Claude model) | commits | Keep, new; print only with the breakdown |
| `all_hands` | commits by anyone on the same branches, bots included | commits | Define ("by anyone, bots included") or drop from the page; it is not about you |
| `calendar_total` | commits GitHub credits to the account since it was created, any repository it can see, default branches, by linked email | commits | Drop from the page (the cached one was seeded; the live one counts a different set of repositories) |
| `calendar.all` / `calendar_weeks` | GitHub's green squares: commits + issues + PRs + reviews | contributions | Drop from the page; keep in the file as context |
| `calendar_check` | your commits on the surveyed repositories in the 52 weeks, clones vs GitHub | commits | Keep as a CI check only |
| `repo_count` | public non-fork repositories you own | repositories | Keep ("public repositories", not "repositories") |
| `first_commit` / `days_surveyed` | date of your earliest commit in any surveyed repository; days from it to `taken` | date / days | Define ("first commit 25 Sep 2025", never "days surveyed") |
| `weeks[].n` | your commits per ISO week (Monday start) | commits | Define (unit on the axis); draw `sweep` differently |
| `weeks[].days` | distinct dates in the week with a commit of yours | days | Keep |
| `weeks[].sweep` | of `n`, commits on days that touched ≥ threshold repositories | commits | Keep, new |
| `tide.hw` | the week with most commits; `sweep_share` says how much of it was a sweep day | commits | Define; a week that is ≥ ½ sweep should not be drawn as the deepest point without saying so |
| `tide.lw` / `median` / `slack` | fewest commits in a complete week; median; lowest four-week sum | commits | Keep |
| `sweeps` | dates with a commit-day in ≥ threshold repositories (5 today) | repositories | Keep |
| `repos[].commit_days` | distinct author-local dates with a commit of yours in that repository | days | Keep |
| `hours` / `weekdays` | repository-days by the day's most common hour / by weekday, author-local | repository-days | Define ("days with a commit, counted per repository") or show the modal hour only |
| `tz_offsets` | your commits by author UTC offset: 100 % −04:00 / −05:00 | commits | Keep; worth one plain sentence ("every commit authored on US Eastern time") |
| `variation` | modal hour this year vs last; change stated only with ≥ 60 days each side | repository-days | Keep (it already refuses to state a change on 15 days) |
| `repos[].active` / `dormant` | ≥ 3 of the last 12 weeks with a commit-day, sweep days removed / none in 90 days | — | Keep |
| `languages` | GitHub's linguist bytes, top 5 + Other, over the public non-fork repositories | bytes | Define ("by bytes, as GitHub classifies files") or replace with a count from the clones (§6) |
| `stars` / `followers` / `account_since` | GraphQL account figures | — | Keep when fetched live; the cached ones were seeded and are now dropped |
| `edition` | PyPI: latest version, first upload date, release count, wheel tags | — | Keep |
| `notices` from PyPI | four uploads on 8 Nov 2025 within 74 minutes | — | Keep as dates; it is what happened |
| `claims` | figures about the code with a source file and sha | — | Keep, upright only when measured |
| `trial`, `sources` | Scrapy export (absent), label copy | — | Not data; nothing to show |
| `provenance.soundings_taken` | days in the last 150 on which stats.json was committed | days | Define ("the survey ran on 1 of the last 150 days") or drop; it measures the workflow, not you |

## 5. Fixes made on this branch

- **`calendar_check` compares like with like** (`derive.py:202`, `github.py:50`): the live run now asks
  GitHub for commits per repository over the clone window and compares your commits on the surveyed
  repositories only; issues, pull requests, reviews, private and unsurveyed repositories are itemised in the
  new `calendar` block instead of being summed into a commit comparison. The old Sunday-week to Monday-week
  mapping (which matched each GitHub week to a clone week overlapping it by one day) is gone with it.
- **The warning says what it compares** (`checks/data.py:62`): "commits on the surveyed repositories over
  2025-10-13..2026-10-09: clones count N, GitHub credits M".
- **A cached GraphQL figure needs a dated fetch** (`build_stats.py:56`): without `provenance.graphql_at`,
  `calendar_total`, `calendar_weeks`, `followers`, `stars`, `account_since` and `languages` are not carried
  and the instrument reads `none`. **Meaning change to notice:** until the next live run, the committed
  cache's 1,828 / 46 / 0 / Oct 2024 become `null`, so the README's survey line drops "by GitHub's calendar"
  and the "since" figure. They were seeded, not measured.
- **`stars` from REST when every repository answered** (`build_stats.py:244`), so the account total agrees
  with the per-repository figures.
- **`first`/`last` are your own** (`survey.py:256`): a repository with none of your commits reports `null`,
  not another author's dates.
- **New measurements from the same `git log`** (`survey.py:117`): `merges` and `coauthored` per repository
  and in total (`coauthored_total`); `weeks[].sweep`, `tide.hw.sweep_share` and `sweep_dates`. The validator
  checks `merges ≤ commits`, `coauthored.count ≤ commits`, `agent ≤ count`, `sweep ≤ n`, `Σ months ≤
  commit_days` and the totals (`model.py`), and the schema admits the keys. Nothing is removed from `weeks`,
  `tide` or `commit_days`: the sweep is named, not hidden; the round-5 keys below leave it out and say so.
- **`--cache`** (`build_stats.py:194`): the previous file is `assets/stats.json` unless `--cache` says
  otherwise; `--out` no longer silently means "no cache" when it points elsewhere.
- **Round 5, D2** (second commit on this branch): per repository `months`, `first_ns`, `last_ns`,
  `coauthored`, `tests`, `workflows`, `manifest`, `lines` and, for the flagships, `ci`; top-level
  `coauthored_total` and `sweep_dates`. A new module `scripts/data/tree.py` reads `HEAD`'s file list from the
  history clone and the lines from a second, depth-1 clone per repository (`survey.py`, `clone_head()`; the
  whole cache-mode build of 21 repositories took 31 s here; Data_science_dev's depth-1 clone is 0.9 GB).
  `chart.toml [lines]` holds the exclusions. Cache mode produces every key the same way (it clones); a
  repository whose clone fails keeps its previous record, new keys included, marked `stale`. `commits`,
  `all_hands` and `calendar_total` stay in the file and are printed nowhere. The calendar comparison is
  re-scoped as described above (commits against commits on the surveyed public repositories) rather than
  removed; it stays a CI warning only.
- Tests: `tests/test_data.py` covers the log parser, merge/co-author counting and classification, first/last,
  the dated-fetch rule, the itemised fetch with a fake GraphQL, the like-for-like check, the warning text,
  months/first_ns/last_ns without sweeps, the test/workflow patterns, the five manifest parsers, the line
  count on a real temporary repository (exclusions, binary and oversize files) and the CI reader.
  `python3 -m unittest`: 212 tests, all passing (199 before).

Not changed, by design: what the README and the sheets print (their builders own that); `assets/stats.json`
(the workflow regenerates it; the committed 7 Oct file still validates).

Known small differences left as they are: live `languages` takes the top 8 languages per repository
(`github.py:46`) while cache-mode REST takes all of them; GraphQL lists at most 100 repositories.

### The D4 line, from these keys

Under rustmapper: `manifest.deps[:4]` → "Built on clap, rkyv, rkyv_derive, redb" (the page may prefer tokio, redb,
rkyv, reqwest: all four are in the list; the file order is the crate's own), `tests` 3 → "3 test files",
`workflows` 1 and `ci` → "1 workflow, last run passed 7 Oct 2026", `lines` → "16k lines of Rust", `last_ns` →
"last worked 8 Aug 2026". Under Scrapy: "Built on scrapy, deltalake, pyarrow, pandas · 257 test files · 5
workflows, last run passed 8 Oct 2026 · 69k lines of Python · last worked 8 Oct 2026". The D5 line:
`sweep_dates` → "sweep days (9–10 Nov 2025, 1 and 7 Oct 2026) excluded", `coauthored_total.agent` → "63 commits
carry agent co-author trailers" (or `.count` 502 for any trailer; the page should say which).

## 6. What is worth showing, and what else the clones can say

Worth showing, named in plain words:

- "2,032 commits authored by me on the default branches of 21 public repositories, counted from clones on
  9 Oct 2026; 405 of them merge commits." One number, one definition, one date.
- "Every commit authored on US Eastern time; most often at 14:00." (`tz_offsets`, `variation.hour`)
- "First commit 25 Sep 2025." (`first_commit`)
- The weekly series with its unit written on it (commits per week) and the sweep days hatched or footnoted:
  "7 Oct 2026: 514 commits, 198 of them pull-request merges across 19 repositories."
- Per repository: commits, days with a commit, first and last month (`span`). All from the clones.

Not worth showing: `all_hands` (it is about other people and bots), `calendar_total` and the green-square
totals (a different count of a different set), `days_surveyed` under that name, `soundings_taken`.

Cool and honest, from the same clones, not yet measured (cost is build time per weekly run and code):

| measurement | how | cost |
|---|---|---|
| Lines added/removed per language, your commits only | `git log --numstat --author=…` on the blobless clone; group by file extension. Blobless clones fetch no file contents, but `--numstat` needs the blobs of changed files, so either fetch them (`git fetch --filter` off, roughly the full repository size) or use `--shortstat` on a full clone. | ~2–5 minutes extra per run; 60 lines of code |
| Files and lines at `HEAD` by extension (a language count that does not depend on GitHub's linguist) | `git ls-tree -r -l HEAD` gives sizes without blobs; counting lines needs the blobs of `HEAD` only (one `git fetch` of the tree's blobs, far smaller than history) | ~1 minute; 40 lines |
| First and latest commit per repository, and the longest streak of consecutive commit-days | already in `repos[].first/last` and `days[]`; the streak is `derive.consecutive_run` over all days | zero; 10 lines |
| Release dates from tags | `git tag --format` on the clones; today there are none in any repository, so this shows nothing until tags exist | zero |
| Days with a commit in the last 365, and the longest gap | from `days[]` | zero; 10 lines |
| Commits that were pull-request merges vs direct, per repository | `merges` is there now; the PR number is in the subject | zero |
| Share of commits with a Claude co-author trailer, per repository | `co_authored` is there; the trailer text is parsed but not kept; keep the name only | 5 lines |
| Issues and pull requests you opened per repository | REST `/repos/{o}/{r}/issues?state=all` per repository (980 + 331 on Scrapy alone); one request per 100 items | ~20 requests per run; 30 lines |
| Commit size distribution (files touched per commit) | `--numstat` as above | with the first item |
