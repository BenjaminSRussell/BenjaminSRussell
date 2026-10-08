# T7 — Data & honesty

Owns `assets/stats.json` v2, `assets/log.json`, `fetch_repodata.py`, the data half of `build_stats.py`, and the honesty checks in `scripts/check.py`. One rule: a number is **upright only if the build can point at the measurement that produced it**; otherwise italic or absent. No schema key is ever a placeholder.

## 1. Decisions

1. **One population, Ben's.** `commits` counts authors matching `chart.toml [identity]` (names `Benjamin Russell`, `Ben Russell`, `BenjaminSRussell`; emails `benjamin.sheldon.russell@gmail.com`, `russell27sail@gmail.com`, the login's `@users.noreply.github.com`). Bots and agents (`google-labs-jules[bot]`, `github-actions[bot]`, `Claude`) go into `repos[].others[]` by name and appear nowhere unlabelled (per 32, 08, 20).
2. **Two instruments, declared.** The Ben-filtered clone count is the hero figure; GraphQL `totalCommitContributions` is `calendar_total`, printed once in the source line. Disagreement >10 % marks the figure `SD` and shows the smaller (per 34).
3. **Hours and weekdays are commit-days in the author's own offset** (`%ai`, keep `±hhmm`), never UTC instants, so a 585-commit fortnight cannot set north (per 32, 08). "Works at night" is dead: 21h UTC was 4–5 pm.
4. **Variation is stated in full from data**: `Var. {h}h ({year})` plus `increasing|decreasing {d}h annually` only when both twelve-month windows hold ≥60 commit-days; otherwise the clause is omitted, not faked (per 13, 32).
5. **The tide is Ben's weekly commit-days from the clones, upright**; the GraphQL calendar is a cross-check. The even-spread fallback is deleted; a repo that fails to clone keeps yesterday's record, `stale:true`, marked `Rep (year)` (per 32, 08, 36).
6. **Chart number = `repo_count`** from GraphQL (public, owned, non-fork). Repos in that count that return no history are listed in `unsurveyed[]` and lettered `ED` in the margin band: existence doubtful is literally true of an empty repository (per 22, 34).
7. **The chart includes itself.** The profile repo stays a feature; decision 1 already excludes the Actions bot, so it grows only when Ben edits it. Against 36's exclusion because 34's recursion is the better sentence once the bot problem is gone.
8. **Wrecks = `archived == true`**, not a `SHELVED` constant. Four shelf repos become wrecks the day Ben archives them (per 23, 36).
9. **Area ∝ commits is asserted, not assumed**: drawn polygon area within ±8 % of `K·commits`, every feature cut at one level; build fails otherwise (per 08).
10. **Active = commits in ≥3 of the last 12 weeks; dormant = no commit-day in 90 days; both on commit-days with sweep days removed** (a sweep day touches ≥⅓ of repos; 7 Oct 2026 touched 17 of 21) (per 32, brief).
11. **Edition = PyPI latest version and upload date, upright, always dated**; `releases=4` is never printed as "four editions"; `provisional` is appended only while the PyPI classifier says Alpha (per 23, 19).
12. **Notices are dated corrections with provenance**: flagship GitHub Releases → PyPI uploads (prints "four, one day": the incentive) → profile-repo commits whose subject starts `Notice:`. N = `len(notices)`; the five principles become Sailing Directions (per 23, 34, 13). The imprint's small-corrections table is a separate, always-real series from the profile repo's human commits by year.
13. **Liveness is a dateline, not a promise**: `updated_at` ISO UTC; "LAST SOUNDING 06:34 UTC · 7 OCT 2026" on the tide table; a failure heartbeat pencils "no sounding taken {date}" and dashes the datum rule (per 21, 32).
14. **The log is computed-consistent until measured**: `position = Σ rate·Δt`, `in_flight = rate × latency`, ≤2 req/s on one host; `measured:true` flips numerals upright (per 21, 22, 19).
15. **Honesty is one convention, defined once** on the Approaches legend and mirrored in the Colophon: upright measured; italic illustrative or computed; `ED`/`Rep (yr)`/`SD` for existence doubtful / reported-not-verified / two instruments disagree (per 22, 26, 34, 09).
16. **`seeded` is deleted**; `provenance.mode` ∈ `live|cache|cache-failed` replaces it, and `check.py` fails unless mode is `live` or `cache` with `taken` ≤ 8 days old (per 34, 36).

## 2. stats.json v2 schema

One in-memory model, written once. `m` measured, `d` derived, `i` illustrative.

| key | type | source | class |
|---|---|---|---|
| `schema` | `2` | constant | — |
| `updated_at`, `taken` | ISO UTC string, `YYYY-MM-DD` | build clock | m |
| `run_id` | string | `GITHUB_RUN_ID` or `local` | m |
| `provenance.mode` | `live\|cache\|cache-failed` | build | m |
| `provenance.failed_at` | ISO or null | failure step | m |
| `provenance.soundings_taken` | `{taken:int, of:int}` | `git log` of stats.json, last 150 days | m |
| `login`, `account_since` | string, `YYYY-MM-DD` | GraphQL `createdAt` (not printed as "since") | m |
| `repo_count` | int | GraphQL `repositories.totalCount` | m |
| `followers`, `stars` | int | GraphQL (schema only; not printed) | m |
| `commits` | int | Σ `repos[].commits` | d |
| `all_hands` | int | Σ all authors | d |
| `calendar_total` | int or null | GraphQL yearly `totalCommitContributions` | m |
| `first_commit` | date | min `repos[].first` | d |
| `days_surveyed` | int | `taken − first_commit` | d |
| `languages[]` | `{name, share, bytes}` | GraphQL languages, "by bytes" | m |
| `repos[]` | see below | clones + GraphQL | m |
| `unsurveyed[]` | `[{name, reason}]` | GraphQL minus clones | m |
| `hours[24]`, `weekdays[7]` | int | Σ per-repo commit-days, author-local | d |
| `variation` | `{hour, year, prior_hour, annual_change:int\|null, basis_days:[n,n]}` | hours by 12-month window | d |
| `weeks[52]` | `[{start, n, repos:{name:n}}]` | per-repo weekly commit-days | d |
| `tide` | `{hw:{start,n,cause,cause_days}, lw:{start,n}, median, slack:{start,end,month}}` | weeks | d |
| `sweeps[]` | `[{date, repos:int}]` | days touching ≥⅓ of repos | d |
| `edition` | `{project, version, date, releases, status, wheels:[tags]}` | PyPI JSON | m |
| `notices[]` | `[{repo, tag, date, title, url, source:"release\|pypi\|commit"}]` | Releases API → PyPI → `git log --grep` | m |
| `corrections` | `{year: [commit ordinals]}` | profile repo human commits | m |
| `claims` | `{id: {value, unit, source, sha, measured}}` | `chart.toml [claims]` + fetch | m/i |
| `trial` | `{date, host, rows:{table:n}, delta_versions:{}, wall_s, fivexx_rate}` or null | `exports/run-*.json` in Scrapy if present | m |

`repos[]` entry: `{name, commits, all_hands, others:[{name, commits, bot:bool}], first, last, commit_days:int, hours[24], weekdays[7], weeks[52], active:bool, dormant:bool, archived:bool, stale:bool, stale_since:date|null, language, stars, span:"Sep 2025–"|"Jan 2026"}`. Invariant checked: `sum(hours) == sum(weekdays) == commit_days` for every repo (hours count days, not commits).

Removed: `seeded`, `since`, `commits_surveyed`, `repo_meta`, bare-int `weeks`. `survey()` returns dicts; `build_stats` merges in memory, validates against `scripts/stats_schema.json`, writes once.

## 3. Which numbers appear where

| sheet | figure | key | set |
|---|---|---|---|
| Hero title block | CHART NO. · EDITION {version} · {d MON YYYY} · Var. line · imprint date · small corrections | `repo_count`, `edition`, `variation`, `taken`, `corrections` | upright |
| Hero features | spot height = `commits` with subscript = human `others` count when >0; survey span under name | `repos[]` | upright |
| Hero water | last 34 weeks `n` along the course, oldest seaward; these blobs generate the contours | `weeks` | upright |
| Hero margin | `ED {name}` for `unsurveyed[]`; `Rep (yr)` beside stale features; `Wk 'YY` for archived | `unsurveyed`, `repos` | upright |
| Soundings strip | `{commits}` large · `{repo_count} public repos` · `{n} languages` · `{days_surveyed} days surveyed` · `since {first_commit}` · tide curve · `HW {n} · wk of {d Mon} · {cause}, {cause_days} days` · `LW` · dotted `typical week {median}` · `slack water · {month}` · `SOUNDINGS TAKEN {d MON YYYY} · {n} REPOSITORIES · LAST SOUNDING {HH:MM} UTC` · source line, both instruments | `tide`, `weeks`, … | upright |
| Approaches | worker permits, shard count, light period, Fl from `scrape_interval`, basin soundings | `claims`, `trial`, `log` | upright only when `claims[id].measured`; else italic |
| Log | TIME · POSITION · WIND · REMARKS · health line · machine watch line | `log.json`, `stats` | italic unless `measured`; watch line upright |
| Instruments | `fitted {YYYY-MM} · {repo}` · `LAST SOUNDING` repeat | `repos[].first`, `updated_at` | upright |
| Footer | `No. {repo_count}` · `corrected through Notice {N}` · `Obstn rep. {year} (PA)` | `repo_count`, `notices`, `taken` | upright |

Followers, stars, 512, 256, 90 % and "Oct 2024" appear on no sheet; 512/256 return only as reconciled `claims`.

## 4. Derivations

- **Author filter.** `is_ben(name, email)`; one `git log --format=%H%x09%ai%x09%an%x09%ae HEAD` per repo feeds every statistic. UA on every HTTP call: `profile-stats (+https://github.com/BenjaminSRussell/BenjaminSRussell)`.
- **Commit-days.** `(repo, author-local date)`. `hours[h]` += 1 per commit-day whose modal hour is `h` (ties → earliest); `weekdays` likewise; `commit_days` = distinct local dates.
- **Variation.** `hour = argmax(hist(taken−365d, taken))`; `prior_hour` for the year before; `annual_change = circ_diff(hour, prior_hour)` in ±12, null unless both windows hold ≥60 commit-days. Today: ≈16h, prior window thin → `Var. 16h (2026)` alone.
- **Weeks.** 52 ISO weeks ending at `taken`'s week, from per-repo commit-days; `n` = sum. GraphQL `contributionCalendar` → `calendar_weeks`, for `check.py` only (warn if Σ differs >10 %).
- **Tide.** `hw` = argmax `n`; `cause` = repo with the largest share that week; `cause_days` = that repo's consecutive commit-day run through the week; `lw` = min over non-trailing weeks; `median` over the 51 complete weeks; `slack` = lowest rolling 4-week sum, `month` at its midpoint.
- **Area.** T6's `islands()` returns polygon area; `check_area` asserts `|area/(K·commits) − 1| ≤ .08` for every non-wreck feature at the common cut level. K is T2's; the check is mine.
- **Dormancy.** `sweeps` first; then `active` and `dormant` on remaining commit-days.
- **Edition.** `status` from the `Development Status` classifier; `wheels` from `releases[version][].filename`, so T8 prints the one-wheel sentence from data.
- **Small corrections.** Profile repo `git log` (needs `fetch-depth: 0`), Ben-filtered, enumerated per year: `2025 — 1…41. 2026 — 42…`, upright.
- **Dateline.** `updated_at = now(UTC)`; `taken = updated_at[:10]`.
- **Heartbeat.** Success: the log gets a synthetic last entry `{kind:"watch", time:"06:34", text:"watch kept by cron · {commits} commits · {repo_count} repos · {change|no change}", measured:true}`, computed at render. Failure (`if: failure()`, T1): `build_assets.py --no-sounding` renders from cache with `mode="cache-failed"`, pencil note "no sounding taken {date}", dashed datum rule. Cache-failed may publish once; a second consecutive failure fails the job.
- **Fallbacks, never placeholders.** PyPI down → cached `edition`, `stale:true`, no visible change. Releases down → cached `notices`. Clone fails → yesterday's record, `Rep (yr)`. No cache and no clone → build fails; nothing ships.

## 5. Honesty conventions (defined once, T3's legend; mirrored by T8)

Legend rows: `58 upright · measured` / `*58* italic · illustrative, computed to be consistent` / `ED · existence doubtful (repository without history)` / `Rep (2026) · reported, not re-surveyed since` / `SD · two instruments disagree; the smaller is shown`. Colophon `<details>How we counted</details>`: commit, author, hour, week, active, edition, exclusions — T8's wording, my definitions. `common.measured()` / `illustrative()` are the only numeral entry points; both register `(sheet, key, value, style)` into `k.FIGURES`.

## 6. log.json schema and the computed-consistent formula

```json
{"schema":2,"vessel":"rustmapper","version":"0.1.3","target":"<domain Ben controls>",
 "date":"2026-10-07","measured":false,"source":"computed|session|cc-index",
 "machine":{"cores":null,"host":null},
 "params":{"hosts":1,"per_host_rps":2.0,"latency_p95_s":0.8,"workers_requested":512,"yield_urls_per_fetch":1.6},
 "entries":[{"t":"14:02:00","kind":"cmd","text":"pip install rustmapper"},
            {"t":"14:03:10","kind":"crawl","rate_rps":2.0},
            {"t":"14:05:00","kind":"health"},
            {"t":"14:06:00","kind":"beat","text":"Nothing on fire."},
            {"t":"18:12:00","kind":"cmd","text":"rustmapper export-sitemap --data-dir ./data --output sitemap.xml"}],
 "signoff":{"initials":"B.S.R.","time":"18:14"}}
```

`kind` ∈ `cmd|out|crawl|health|remark|beat|watch`. Numbers are **not stored** while `measured:false`; `build_assets.log()` computes them: `rate_i = min(per_host_rps·hosts, workers/latency)`, `position_i = Σ_{j<i} rate_j·Δt_j` (URLs fetched), `discovered_i = round(position_i·yield)`, `in_flight_i = round(rate_i·latency_p95_s)` (Little's law), `elapsed = t_last − t_crawl`. Defaults give 2 req/s, in-flight 2 ("512 requested · 2 in flight · one host"), position ≈ 230 at 14:05, ≈ 21,700 after three hours. Health-line fields (`fetched · timeout % · failed % · p95 fetch · wal fsync p95 · permits`) derive from `params`, italic. `check_log()` asserts monotone position, `Δposition ≤ rate·Δt·1.02`, `rate ≤ 2·hosts`, `in_flight ≤ min(workers, ceil(rate·latency)+1)`, ≤10 entries, no `example.com`. A real session (`source:"session"`, `measured:true`) uses stored numbers verbatim, upright; option B is a Common Crawl index query (`cc-index`), measured and load-free (per 22).

## 7. Build checks (`scripts/check.py`, CI gate, T10 integrates)

1. `provenance.mode` not in `{live, cache}` or `taken` > 8 days old → fail. Any `seeded` key → fail.
2. Banned strings in every SVG and README: `ILLUSTRATIVE|PENDING|SEEDED|TODO|TBD|lorem|example\.com|NOT FOR NAVIGATION|Oct 2024` → fail.
3. Schema validation; per-repo invariant `sum(hours)==sum(weekdays)==commit_days`; `commits + Σothers == all_hands`.
4. Contrast from theme dicts: every text role ≥4.5:1 on paper and land in both editions; coastline, contours, marks ≥3:1 (09's values are the floor).
5. Night: OKLCH L of every light flare > L of body text (per 15).
6. Alt: ≤25 words each; last sentences concatenated and diffed against `chart.toml alt_poem[]`; print the poem; fail on mismatch (per 24, 09).
7. `check_area` ±8 %; features drawn = `len(repos) − archived`, `ED` count = `len(unsurveyed)`.
8. Cross-sheet consistency: every `(key, value)` in `k.FIGURES` equals `stats[key]`; README `<!-- stat:key -->…<!-- /stat -->` spans equal the same values; `repo_count` identical on hero, soundings, footer; `N` identical on hero, footer, README.
9. `check_log` as above; `measured:false` ⇒ every log numeral italic; `measured:true` ⇒ upright.
10. Every `claims[id]` printed upright has `measured:true` and a `source`+`sha`.

## 8. Fixes to request from Ben (exact wording for T1's hygiene list)

1. "Rust-sitemap: add `LICENSE` (MIT, matching pyproject), tag `v0.1.3` at the published commit, create a GitHub Release with notes. Until then the Notices fall back to PyPI uploads and print 'four notices, one day'."
2. "Pick one worker figure from `governor.rs` (min 256 / max 1024, 250 ms EWMA) and make README, PyPI summary and `cli.rs` agree. '512' stays italic until all four match; then `claims.workers` sets it upright."
3. "Scrapy: gate CI at `--cov-fail-under=85` and publish the badge, or the coverage number leaves every sheet and bullet. No third option."
4. "Archive `3d-swift-widget`, `2d-swift-widgets`, `MLX_convertion`, `Course_crusader` (or whichever four you would not defend); archived repos become `Wk` marks."
5. "Profile repo: add `LICENSE` (MIT for `scripts/`; sheets and copy CC BY 4.0). Delete `snake.yml`, the `output` branch, and `scripts/fonts/Inter*`, `DejaVu*`."
6. "Record one real rustmapper session on a domain you control (`rustmapper crawl … | tee assets/log.raw`), or a Common Crawl index query; commit it as `assets/log.json`, `measured:true`. Expect ~2 req/s on one host; the restraint is the demonstration."
7. "Scrapy: commit one `exports/run-YYYY-MM-DD.json` (rows per Delta table, `_delta_log` versions, wall-clock, host, 5xx rate, breaker trips); the anchorage soundings become those counts, upright."
8. "Add a maturin-action release workflow (abi3 wheels: linux x86_64/aarch64, macOS x86_64/arm64, Windows), drop `target-cpu=native`, cut 0.2.0. The edition line changes itself."
9. "go_go_go: make header rotation opt-in with an identifying default UA, or the profile calls it 'browser-faithful fetching', not 'per-host politeness'."
10. "Replace the bio 'Scraping enthusiast and full stack developer' with T8's position line; fill `position` in `chart.toml` (empty omits the slot)."

## Interfaces

**Provide.** `assets/stats.json` v2 (keys above); `assets/log.json` v2; `scripts/stats_schema.json`; `fetch_repodata.survey(repo, workdir, identity) -> dict|None`; `build_stats.main(mode: "live"|"cache"|"cache-failed") -> Stats`; `build_stats.derive(repos, calendar, pypi, releases) -> dict`; `check.py` functions `check_provenance, check_strings, check_schema, check_contrast(themes), check_lights(themes), check_alt(readme, poem), check_area(features, stats, K), check_figures(k.FIGURES, stats, readme), check_log(log), check_claims(stats)`; `common.measured/illustrative(..., key=None, sub=None)` registering into `k.FIGURES`; `chart.toml` sections `[identity]`, `[claims.*]`, `alt_poem`.

**Need.** T1: `fetch-depth: 0`, `concurrency`, `if: failure()` step calling `build_assets.py --no-sounding`, `chart.toml` loader, orphan-branch decision. T2: constant `K`, open-water blobs from `weeks[-34:]`, spot heights from `repos[].commits`, `repos[].span`, `ED`/`Rep`/`Wk` placement. T3: legend rows (§5), `claims` rendering, basins from `trial`. T4: still edition for `check_figures`. T5: `sub=` subscripts, italic mono face. T6: `islands()` returning `(area, cx, cy, level)`. T8: markers `<!-- stat:key -->`, `<!-- notices:start/end -->`, "How we counted", `alt_poem`. T9: `log.json` consumer honouring `measured`, `watch` entry, trial basins. T10: `check.py` as the CI gate.

## Build order, effort, risks, omissions

1. Identity filter, commit-days, author offsets, `repos[].weeks`, schema, schema validation, write-once model — **5 h**.
2. Derivations (`variation`, `tide`, `sweeps`, `active`, `corrections`, `unsurveyed`, `edition.status/wheels`) — **4 h**.
3. Notices (Releases → PyPI → commits), `claims` loader, `trial` reader — **3 h**.
4. `log.json` v2 + computed-consistent renderer + `check_log` — **3 h**.
5. `check.py` (ten checks) and `k.FIGURES` registry — **5 h**.
6. Heartbeat and failure mode with T1 — **2 h**. Total ≈ **22 h**.

Risks: calendar and clones count differently (cross-check only); `repo_count` 24 vs 21 surveyed must be verified on the first live run before `ED` marks are trusted; a fourth identity string may exist. Left out deliberately: followers and stars on any sheet; 08's per-repo sparklines sheet (later edition); a public SLI endpoint; Mercator-of-time graticule.

## Acceptance criteria

- `grep -E 'ILLUSTRATIVE|PENDING|SEEDED|example\.com|Oct 2024' assets/*.svg README.md` → 0; `jq .seeded assets/stats.json` → null.
- Change `repos[Scrapy].commits` by +50 → hero feature area changes within ±8 % of the new target, soundings total changes, README `<!-- stat:commits -->` changes, `check_figures` passes.
- Hours in stats.json for Rust-sitemap sum to its `commit_days`, not its `commits`; `variation.hour` ≠ 21 when game_engine is deleted from the input or not.
- `build_stats.py` with no network renders from cache and prints `mode=cache`; with a corrupted cache it exits non-zero and writes no SVG.
- `check_log` rejects the v8 log (48,213 URLs in 60 s) and accepts the default computed log; flipping `measured:true` without stored numbers fails.
- Tide HW label names a repo and a day span; `typical week` equals the median of 51 complete weeks; the source line names both instruments.
- Night edition: every light flare's OKLCH L exceeds body text L; both editions pass 4.5:1 on all text roles.
- Alt poem printed in the build log matches `chart.toml alt_poem` line for line; every alt ≤25 words.
