# Round 5 — the skeptic (systems engineer, 61, has shipped crawlers and storage engines)

I read the claims against the clones at `/home/user/rust-sitemap` (00a877d) and `/home/user/scrapy` (74fd4f7) before writing a word. Most of them hold. The page's problem is not honesty; it is that the honest numbers it chose to print are the ones that say the least, and the one number an engineer would ask for is missing.

## 1. What a visitor needs to know about Ben

1. **What he builds.** Crawl and storage plumbing, Python and Rust. Answered, first line under the chart. Good.
2. **That one system is real end to end.** rustmapper: governor reads redb commit latency every 250 ms, permits 256–1,024 (`governor.rs`, confirmed); WAL framed `[len][crc32][seqno][payload]` with replay and truncate-after-commit (`wal.rs`, confirmed, crc32fast; the comment says crc32c, the code does not); rendezvous shards by registrable domain, `num_cpus` of them (confirmed); crawl-delay honoured; CT-log and Common Crawl seeders exist. Scrapy Harbor: Delta writes with `schema_mode="merge"`, OPTIMIZE/VACUUM from a maintenance queue, three named circuit breakers (HTTP, Delta, Redis in `retry.py`), MinHash LSH with 128 permutations, `bart-large-cnn` for summaries. All true. Answered, but not cited: the page prints one sha nowhere a reader can see it.
3. **Whether it has ever run at load.** Not answered, and it is the only question that matters for data-infrastructure work. rustmapper's own README says "50–200 URLs/minute, network I/O bound". A 1,024-permit pool doing three URLs a second is either a politeness-limited crawl or a number nobody measured. Print the permits without the throughput and an engineer assumes the worst. Scrapy has `test_pipeline_10k.py`; whether it passed, and in what wall time, is nowhere.
4. **Whether the repo's own story agrees with the page.** It does not: the rustmapper README says 32–512 workers, default `--workers 512`; PyPI says 256; the code says 256–1,024. chart.toml already knows (`measured = false`). Fix the README in the repo; until then the figure is a liability on the profile.
5. **Whether it is alive.** Half answered and contaminated. 18 of 21 repos have `last = 2026-10-07`; that is one sweep day, not life. Real recent work: Data_science_dev (Sep 2026), BenjaminSRussell (Sep 2026, 173 commits of README), ideal-url-organizer (Aug 2026). rustmapper's last non-sweep day is in 2025. Say so or say nothing.
6. **How he works.** 45 of 132 rustmapper commits and 22 of 340 Scrapy commits are authored "Claude"; game_engine has 148 stale branches and 512 commits in 8 days, 201 of them in one day. The page counts "author's commits only", which is the right filter, but a 2026 hirer will open the log and should not be surprised. One plain line.
7. **Where and when.** Timezone −4/−5, so US Eastern; the rose says it in a way nobody decodes. Position slot empty, no résumé, no LinkedIn.
8. **How he thinks.** Notices 1–3 do this well and are the best text on the page.

## 2. What a real chart carries, and which conventions are honest here

A chart earns trust because every mark was measured and every mark has one meaning. Taking them in turn:

- **Sounding (depth figure).** Measured water under you; your margin. Days with commits is an honest margin figure: shallow is a weekend, 26 is five months of evenings. Works. But 26 is the deepest water on the sheet; do not tint it like an ocean.
- **Depth contour and tint.** Generalised soundings. Honest only if the contour is derived, not drawn. Works at two tints; the 5-and-10 pair is enough.
- **Rock, drying height, "awash".** Something there, no safe water. A repo under seven days. Honest and already right.
- **Wreck (Wk).** A large thing, abandoned, that can still hole you. game_engine: 512 commits, dormant since Jan 2026, 148 stale branches. Honest, and a sailor nods. Use once.
- **Light character ("Fl 15s", range).** Identifies a mark from a distance and tells you it is watched. Honest mapping: a lit feature is an instrumented project; the period is the Prometheus scrape interval, 15 s, cited by sha. Scrapy Harbor is lit. rustmapper has internal metrics and no exporter: unlit. "Fl R 4s" and "Fl G 4s" today are invented. Forced as drawn, honest if re-derived.
- **Lateral buoys, fairway, channel.** A sequence you pass in order. The pipeline stages (scout → analysis → dedup → summary) are honestly a buoyed channel. Harbour-entrance buoys that mean nothing are decoration.
- **Caution / notes box.** The known gotcha. "Wheel for macOS arm64, CPython 3.13 only; elsewhere pip needs a Rust toolchain" is a real caution. Also honest: "sitemap.xml lies again."
- **Source diagram / zone of confidence.** Which instrument surveyed which part and how reliable. Your provenance line (clones live, GraphQL cached, REST partial) is exactly this. Keep it as text; do not draw it.
- **Chart datum, edition, chart number.** Datum: main. Edition: rustmapper 0.1.3 — but call it alpha, four uploads in 74 minutes on one evening is a release day, not a cadence. Chart No. = 21 repos. Small and honest.
- **Tide table, high water.** Forced. Tides are periodic; commits are not. Your HW is 358 commits on a sweep day, 42 % from a browser game. Kill.
- **Variation.** Difference between true and magnetic north. Mapping it to modal commit hour is a pun. Forced.
- **Anchorage.** Where you stop and stay: the install block. Fine, unlabelled.
- **Limit of survey.** Honest in principle (data stops at 7 Oct 2026) but it costs 15 % of phone width to say so. A thin hatched margin, no words.

## 3. The proposal

One sheet, 870 wide on the desk, 390 on the phone, drawn from stats.json plus a `[claims]` table where every printed figure carries a sha.

**Desk.** Cartouche top-left, shortened to: name; "Crawl and data infrastructure · Python and Rust"; three title lines (CHART 21 · DATUM MAIN · 7 OCT 2026 / DEPTHS IN DAYS WITH COMMITS / 21 REPOSITORIES · 9 CHARTED · 12 AS ROCKS). The chart occupies the right 60 %. Scrapy Harbor is the one harbour, with its channel drawn as four lateral buoys in sequence, named by stage in 9-px caps (SCOUT, ANALYSE, DEDUP, SUMMARISE), and one light at the head: **Fl 15s** with the Prometheus sha in the title block's sources line. rustmapper is the bank beside it, sounding 22, with the three seed sources as three survey lines fanning off its edge (SITEMAPS, CT LOGS, COMMON CRAWL), unlit. One caution box bottom-left, two lines, the wheel caveat. Seven islands with soundings, no "I." suffixes. game_engine carries Wk. Rocks as today. No rose, no tide, no corrections line, no IALA. Nothing moves.

**Phone.** Cartouche stacked above the chart at full width; chart below at full width, 1.1:1. Labels on five features only: Scrapy Harbor, rustmapper, the caution, Wk, Fl 15s. Every other island carries its sounding and nothing else.

**Under it, in order, 350 words total:** the links row (add position and timezone, "US Eastern"); rustmapper, four bullets with the throughput line from its README beside the permits, honestly; the install block; Scrapy Harbor, three bullets; one line on method ("some commits by an agent under review, counted separately"); notices 1–3; the provenance line. Cut the rest.

## 4. Details and one-off words

1. **Wk** on game_engine. Says "learned why engines are hard" without a sentence.
2. **Fl 15s** with a sha. The only joke on the sheet that is also a measurement.
3. The caution box in the chart's own register: "Wheel: macOS arm64, CPython 3.13. Elsewhere, bring a Rust toolchain."
4. Survey lines fanning off rustmapper, unlabelled on the phone.
5. "Found a wrong depth? Open an issue." Keep; it is the one line of theme that is useful.

## 5. Kill list

- **HW · SWEEP 7 OCT 358.** Your high water is housekeeping. Lazy data.
- **The rose and VAR 14h.** A clock nobody reads to learn "afternoons, Eastern".
- **SMALL CORRECTIONS 2026 — 5 — 173.** Honest and a self-own: 173 commits on a README, 87 on the crawler.
- **R "2" Fl R 4s / G "1" Fl G 4s.** Invented characters. Nothing on a chart is invented.
- **IALA REGION B, "survey vessel", "Other waters", "Below the waterline", "Notices to mariners", "Survey log".** Each names the costume. "Log", "Other work", "More", "Notices" are the words.
- **"sitemap.xml lies again"** stays only if it sits beside the Common Crawl line it refers to. Floating, it is a wink.
- **The permit figure as printed.** Either put the throughput next to it or print neither until the repo README agrees with the code.
- **UNSURVEYED band at full width.** Thin hatch, no word.

## 6. The two-second test

**Two seconds, iPhone:** a name, "crawl and data infrastructure, Python and Rust", and a drawn chart with one big harbour and a few numbered islands. Not what the numbers mean yet, but that they are numbers.

**Thirty seconds:** the harbour is a four-stage crawl pipeline that is monitored (the light), the bank beside it is a Rust crawler seeded from three sources, one project is a wreck and he is not hiding it, the depths are days of work and the deepest is 26, the wheel only builds on one platform, and the figures come with commit hashes. That is a page I would open the repos from. Today I would not.
