# 20 — Senior Python / data-platform engineer

Lens: I run Scrapy (the framework), Delta Lake, Postgres, Redis and Prometheus in production; I am the person asked "is this real?" before an interview. I read README.md, README.draft.md, spec-approaches.md and the approach-scrapy render, then cloned `BenjaminSRussell/Scrapy` (HEAD 74fd4f7, 2026-10-07) and checked every bullet the profile makes about it against the code.

## What is good

- **The platform is more real than the profile says.** `src/core/schemas.py` holds typed Arrow schemas for every table (discovery, analysis, queue, summaries, large docs, seeds, error log, metrics): data contracts. `src/lakehouse/lakehouse_manager.py` writes with `schema_mode="merge"`, partitions by `domain`, and runs OPTIMIZE and VACUUM from a maintenance queue. `stage2_worker.py` closes queue rows with a Delta MERGE on `url`. `src/utils/retry.py` is a real closed/open/half-open breaker. `start.py` exists; compose has nine services; the Helm chart has HPA, PDBs and network policies. None of this is on the page.
- **The channel as architecture** (approach sheet, spec §1): URLS → SCOUT → ANALYZE → SUMMARIZE is the repo's actual stage order, and "breaker closed" drawn as an *unlit* sector is correct operator semantics.
- **"Raw pages land in Delta Lake and stay raw"** (draft) is true to the code: every stage write is `mode="append"`.
- **The upright/italic honesty convention** is how I would want a dashboard to flag estimated series.

## What is bad, ranked

1. **"90%+ test coverage" is enforced nowhere.** `pytest.ini` has `fail_under = 70`; `.github/workflows/main.yml` runs `--cov-fail-under=0`; `coverage.xml` is an unpublished artifact; no badge. The profile (draft bullet, spec note 5, the planned upright `90` sounding) stakes its honesty convention on a number that fails it. If I find `fail-under=0`, every other upright numeral loses.
2. **The survey vessel does not feed the harbor.** The merged sheet and the draft ("the harbor the survey feeds") assert an integration; `grep -ri rustmapper` in the Scrapy repo returns nothing. The platform seeds from `uconn.edu` sitemaps through its own `sitemap_parser.py`. Intent may be charted (a proposed channel is dashed), not drawn as fact.
3. **"Circuit breakers on the hosts that misbehave" is wrong.** The breakers wrap downstream services: `http` (10 failures/60 s), `delta_lake` (5/30 s), `redis` (5/30 s). Per-host behaviour is AutoThrottle plus a custom rate limiter. "Breakers on the stores, throttles on the hosts" is both accurate and more interesting.
4. **The name.** Repo `Scrapy`; `pyproject` name `uconn-scraping-pipeline`; `BOT_NAME uconn_scraper`; the legend lists "Scrapy" as daily driver under *Data*, which can only mean the framework. "Not the framework itself" is a disclaimer, and STANDARDS §1 banned those. The platform needs a name of its own.
5. **What a data engineer looks for and cannot find:** the dedup key (the code has three: Scrapy request fingerprint, `url_hash`, MinHash via `datasketch`); idempotency (fact tables are append-only with no MERGE key, so a rerun double-writes); backfill (none, only `--reset-delta`); the summarization model and where it runs (`facebook/bart-large-cnn`, in-process via HF transformers, torch an optional extra: local, no API, a selling point); cost; and one measured run (`exports/` empty, zero tags, zero releases, `cd-release.yml` failing).
6. **One click reveals:** 930 open issues (91 of the last 100 self-filed), PR numbers past 1100 in twelve months, 22 commits authored "Claude" on one day, `google-labs-jules[bot]`, five `PHASE_N_STRATEGY.md`, `temp_scripts/` and `trivy-reports/` committed. `stats.json`'s four authors count bots. The page says "operated"; the tracker says "generated".
7. **"Depth is trust" (spec §1) is asserted, not derived.** Approach-water soundings are random italics while the repo has real depths: row counts per Delta table, `_delta_log` versions.

## What needs to be done

- **F1 Coverage.** Gate CI at `--cov-fail-under=85` and publish a badge, then draw `90` upright; or delete bullet and sounding. No third option.
- **F2 Integration honesty.** Draw rustmapper → Scrapy as a *proposed* channel (dashed centre line, marks unlit, legend row "Proposed channel · not yet buoyed") until `seeds.sources: rustmapper` exists. It is a day's work: rustmapper exports `sitemap.xml`, `sitemap_parser.py` already reads one. Then light the marks.
- **F3 Breaker copy and position.** "Breakers on Delta, Redis and HTTP; per-host throttles separately." Move the Breaker Lt into the inset beside PostgreSQL/Redis, where the code puts it.
- **F4 Name.** Rename the repo to the harbor's name (GitHub redirects) or set its description to "<name>: a crawl platform on Scrapy". In Instruments, "Scrapy" moves to *Framework*; the platform gets its own row; one canonical name, alt text included.
- **F5 Replace capacity bullets with code-backed facts:** "Typed Arrow schemas per table; `schema_mode=merge`, partitioned by domain; OPTIMIZE/VACUUM on a maintenance queue; dedup by URL hash and MinHash; BART-large-CNN summaries on the worker, no external API." Each greppable. "1000+ URLs/min" and "100M+ URLs" stay italic or go.
- **F6 One sea trial.** Run against the domain it was built for; commit `exports/run-YYYY-MM-DD.json` (rows per table, Delta versions, wall-clock, host, 5xx rate, breaker trips); have `build_stats.py` read it so the anchorage soundings are those counts, upright.
- **F7 Triage the tracker** before the page links to it.

## Improvements and ideas

1. **Medallion as harbor basins (bold).** The repo has three natural depths in Delta: raw discovery (`stage1_discovery`), analysis (`stage2_page_analysis`), summaries (`stage4_summaries`). Draw the anchorage as three basins separated by sills: the outer basin wide and shoal (raw, cheap, never dredged), the inner deeper, the dock deepest (fewest rows, most refined). Soundings per basin are the table's row count and `_delta_log` version, refreshed nightly. "Depth is trust" becomes literal and "raw before clean" gets a place on the chart. Use bronze/silver/gold in the legend only if Ben adopts the terms in the repo; otherwise label basins by table.
2. **Data contracts as harbour regulations.** Issue #1099 already proposes a schema registry with CI contract checks. Ship the minimal version (export the Arrow schemas, a CI job that diffs them) and the Scrapy title block earns "Harbour regulations: schemas checked in CI", linked. That one line is what a hiring data engineer wants.
3. **Unreleased platform beside a released package: a preliminary chart.** Do not fake symmetry. rustmapper's block reads "PyPI 0.1.3 · 2025-11-08"; Scrapy's should read "Edition: main · 331 commits · harbour works in progress", upright from `stats.json`, with the legend line "Preliminary: survey continuing." Chart convention already has the idea, and it is true.
4. **Where the model runs, as a structure.** A "Summarization Wks · BART · local" building on the quay, with the note that nothing leaves the harbor for an API. For a crawl platform that is a privacy and cost statement, and it is in the code today.

## What the page says about its maker

Now: a developer with excellent taste who knows the data-platform vocabulary and has built most of the parts, but describes the platform by feature table rather than by guarantees, lets a marketing number stand where a measured one should, and draws an integration that is a plan. Reading the code, I find *more* substance than the page claims (schemas, schema evolution, partitioning, maintenance, breakers) and *less* evidence than it implies (no run, no release, no gate). It should say: someone who states what the system guarantees, can show the key it dedups on and the schema it writes, labels the proposed channel as proposed, and has run the thing once with the receipt committed.

## Five most important lines

1. The planned upright `90` (test coverage) is unsupported: `pytest.ini fail_under=70`, CI `--cov-fail-under=0`; gate CI at 85+ with a published badge or remove the number everywhere.
2. rustmapper does not feed Scrapy (zero references in the repo); draw that channel as *proposed* (dashed, marks unlit) until a `seeds.sources: rustmapper` path exists, which is a day's work.
3. Replace capacity bullets with code-backed platform facts: typed Arrow schemas per table, `schema_mode=merge`, partition by domain, OPTIMIZE/VACUUM queue, URL-hash + MinHash dedup, BART-large-CNN summaries run locally on the worker.
4. Fix the breaker claim (breakers wrap Delta/Redis/HTTP, not crawled hosts) and give the platform a name other than "Scrapy"; the legend currently lists the framework as the daily driver.
5. Commit one measured run (`exports/run-*.json`: rows per table, Delta versions, wall-clock, 5xx rate) and draw the anchorage as three basins whose soundings are those counts; triage the 930 open issues before the page links to the repo.
