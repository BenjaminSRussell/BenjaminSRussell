# Round 5 — the skeptic (systems engineer, 61, has shipped crawlers and storage engines)

I checked the claims against the clones at `/home/user/rust-sitemap` (00a877d) and `/home/user/scrapy` (74fd4f7) before writing. Most hold. The page's problem is not honesty; it is that the honest numbers it prints are the ones that say the least, and the one number an engineer asks for is missing.

## 1. What a visitor needs to know about Ben

1. **What he builds.** Crawl and storage plumbing, Python and Rust. Answered, first line under the chart.
2. **That one system is real end to end.** rustmapper: governor reads redb commit latency every 250 ms, permits 256–1,024 (`governor.rs`, true); WAL framed `[len][crc32][seqno][payload]` with replay and truncate-after-commit (`wal.rs`, true; the comment says crc32c, the code is crc32); rendezvous shards by registrable domain, `num_cpus` of them (true); crawl-delay honoured; CT-log and Common Crawl seeders exist. Scrapy Harbor: `schema_mode="merge"`, OPTIMIZE/VACUUM from a maintenance queue, three named breakers (HTTP, Delta, Redis in `retry.py`), MinHash LSH at 128 permutations, `bart-large-cnn`. All true. Answered, but not cited where a reader can see it.
3. **Whether it has run at load.** Not answered, and it is the only question that matters for data-infrastructure work. rustmapper's README says "50–200 URLs/minute, network I/O bound". A 1,024-permit pool doing three URLs a second is either politeness-limited or unmeasured. Permits without throughput, and an engineer assumes the worst. Scrapy has `test_pipeline_10k.py`; whether it passed, in what wall time, is nowhere.
4. **Whether the repo agrees with the page.** It does not: the rustmapper README says 32–512 workers, PyPI says 256, the code says 256–1,024. chart.toml knows (`measured = false`). Fix the README; until then the figure is a liability.
5. **Whether it is alive.** Contaminated. 18 of 21 repos have `last = 2026-10-07`: one sweep day, not life. rustmapper's last non-sweep commit is in 2025. Say so or say nothing.
6. **How he works.** 45 of 132 rustmapper commits are authored "Claude"; game_engine has 512 commits in 8 days, 201 in one, 148 stale branches. "Author's commits only" is the right filter, but a 2026 hirer will open the log. One plain line.
7. **Where and when.** Offsets −4/−5, so US Eastern; the rose says it in a way nobody decodes. Position, résumé, LinkedIn empty.
8. **How he thinks.** Notices 1–3. The best text on the page.

## 2. What a real chart carries, and which conventions are honest here

A chart earns trust because every mark was measured and has one meaning.

- **Sounding.** Water under you; your margin. Days with commits is an honest margin: shallow is a weekend, 26 is five months of evenings. Works. But 26 is the deepest water on the sheet; do not tint it like an ocean.
- **Contour and tint.** Honest only if derived. Two tints are enough.
- **Rock, drying, awash.** Something there, no safe water. A repo under seven days. Already right.
- **Wreck (Wk).** Large, abandoned, can still hole you. game_engine. Honest; use once.
- **Light character.** Identifies a mark and says it is watched. Honest mapping: a lit feature is an instrumented project; the period is the Prometheus scrape interval, 15 s, sha-cited. Scrapy Harbor lit; rustmapper has no exporter, unlit. "Fl R 4s" today is invented: forced as drawn, honest if re-derived.
- **Buoyed channel.** A sequence you pass in order: the pipeline stages. Harbour-entrance buoys that mean nothing are decoration.
- **Caution box.** The known gotcha: "wheel for macOS arm64, CPython 3.13 only; elsewhere pip needs a Rust toolchain." Honest.
- **Source diagram.** Which instrument surveyed what, how reliably. Your provenance line is exactly this. Keep as text.
- **Datum, edition, chart number.** Main; 0.1.3 but say alpha (four uploads in 74 minutes is a release day, not a cadence); 21 repos. Honest, small.
- **Tide, high water.** Forced. Tides are periodic; commits are not. Your HW is 358 commits on a sweep day, 42 % from a browser game.
- **Variation.** True versus magnetic. Modal commit hour is a pun. Forced.
- **Limit of survey.** Honest in principle, but it costs 15 % of phone width. Thin hatch, no word.

## 3. The proposal

One sheet, 870 wide on the desk, 390 on the phone, drawn from stats.json plus a `[claims]` table where every printed figure carries a sha.

**Desk.** Cartouche top-left: name; "Crawl and data infrastructure · Python and Rust"; three title lines (CHART 21 · DATUM MAIN · 7 OCT 2026 / DEPTHS IN DAYS WITH COMMITS / 21 REPOSITORIES · 9 CHARTED · 12 AS ROCKS). Chart fills the right 60 %. Scrapy Harbor is the one harbour, its channel four lateral buoys in sequence named by stage in 9-px caps (SCOUT, ANALYSE, DEDUP, SUMMARISE), one light at the head, **Fl 15s**, sha in the title block's sources line. rustmapper is the bank beside it, sounding 22, three survey lines fanning off its edge (SITEMAPS, CT LOGS, COMMON CRAWL), unlit. One caution box bottom-left, two lines. Seven islands with soundings, no "I." suffixes; game_engine carries Wk. Rocks as today. No rose, tide, corrections line or IALA. Nothing moves.

**Phone.** Cartouche stacked above, chart below at full width, 1.1:1. Labels on five features only: Scrapy Harbor, rustmapper, the caution, Wk, Fl 15s. Other islands carry a sounding and nothing else.

**Under it, 350 words:** links row plus position and "US Eastern"; rustmapper, four bullets with the README's throughput line beside the permits; install block; Scrapy Harbor, three bullets; one line on method ("some commits by an agent under review, counted separately"); notices 1–3; the provenance line. Cut the rest.

## 4. Details and one-off words

1. **Wk** on game_engine. Says "learned why engines are hard" without a sentence.
2. **Fl 15s** with a sha. The one joke that is also a measurement.
3. The caution in the chart's register: "Wheel: macOS arm64, CPython 3.13. Elsewhere, bring a Rust toolchain."
4. Survey lines off rustmapper, unlabelled on the phone.
5. "Found a wrong depth? Open an issue." The one themed line that is useful.

## 5. Kill list

- **HW · SWEEP 7 OCT 358.** Your high water is housekeeping. Lazy data.
- **Rose and VAR 14h.** A clock nobody reads to learn "afternoons, Eastern".
- **SMALL CORRECTIONS 2026 — 5 — 173.** A self-own: 173 commits on a README, 87 on the crawler.
- **R "2" Fl R 4s / G "1" Fl G 4s.** Invented. Nothing on a chart is invented.
- **IALA REGION B, "survey vessel", "Other waters", "Below the waterline", "Notices to mariners", "Survey log".** Each names the costume. "Log", "Other work", "More", "Notices".
- **"sitemap.xml lies again"** stays only beside the Common Crawl line it refers to.
- **The permit figure as printed.** Throughput beside it, or neither until the repo README agrees with the code.
- **UNSURVEYED at full width.** Thin hatch, no word.

## 6. The two-second test

**Two seconds, iPhone:** a name, "crawl and data infrastructure, Python and Rust", a drawn chart with one big harbour and numbered islands. Not what the numbers mean, but that they are numbers.

**Thirty seconds:** the harbour is a four-stage pipeline that is monitored, the bank beside it a Rust crawler seeded from three sources, one project is a wreck and he is not hiding it, depths are days of work and the deepest is 26, the wheel builds on one platform, and the figures carry commit hashes. That is a page I would open the repos from. Today I would not.
