# 19 — Senior Rust engineer (tokio / reqwest / PyO3 / redb). Does the rustmapper story ring true?

I build crawlers and network services in Rust and review maturin packages before my team depends on them. I read the README, the draft, the specs and the survey and log renders, then cloned Rust-sitemap (00a877d, 13,350 lines of Rust, 3 `unsafe`) and pulled the PyPI JSON for `rustmapper`, because a Rust reader does exactly that within ninety seconds of landing here.

## 2. What is good

- **The repo is better than the page.** Cargo.toml is a serious crawler's manifest: `reqwest` with `hickory-dns`, `redb` 2.1, `rkyv` with validation, `fastbloom`, `psl`, `robotstxt`, `async-compression` (gzip/br/deflate/zstd), `tracing`; edition 2024; `lto = "fat"`, `codegen-units = 1`, `strip`. CI tests on three OSes in debug and release.
- **Real mechanisms.** `frontier.rs` rendezvous-hashes URLs by *registrable domain* onto one shard per core, so a host's politeness state lives on one shard and never takes a cross-shard lock. `wal.rs` is a hand-framed log, `[u32 len][u32 crc32][u128 seqno][payload]`, with instance-scoped sequence numbers, batched fsync and truncation after checkpoint into redb; replay goes through `rkyv::archived_root`, zero-copy. `completion_detector.rs` ends a crawl on a discovery plateau plus grace period. `network.rs` streams bodies behind a 10 MB cap. `lib.rs` releases the GIL around the crawl.
- **The seed story is the differentiator, and the page has it.** `ct_log_seeder.rs` (361 lines) and `common_crawl_seeder.rs` (433 lines) are the two files no other sitemap tool has. The A/B/C braces pushing the limit of survey west in spec-approaches is the right picture.

## 3. What is bad (ranked)

1. **The headline number exists nowhere once.** Profile: 512 workers. PyPI summary: 256. Repo README: 32–512 "based on commit latency". `governor.rs` defaults: min 256, max 1024. `cli.rs` has a preset `'ben'` = 1024, robots ignored. The spec then sets `512` as an *upright* (measured) sounding and builds the survey on "16 lines × 32 = 512". That geometry is invented: shards are `num_cpus::get()`, workers are a semaphore the governor resizes. Under the page's own convention, 512 is italic until the code says 512.
2. **"WAL with redb" undersells and misdescribes.** redb is the state store; the WAL is Ben's own CRC-framed file in front of it. That is the more impressive fact.
3. **"One `pip install` away" is a trap.** Each release has exactly one wheel, `cp313-macosx_11_0_arm64`; pyproject advertises Python 3.8–3.12, which no wheel covers. Linux, Intel Mac, Windows and Python ≤3.12 get the sdist and need cargo. `.cargo/config.toml` sets `target-cpu=native`, so the wheel is compiled for the laptop that built it. The Python `Crawler` in `python/rustmapper/__init__.py` is a `subprocess` wrapper around the CLI; the PyO3 `Crawler` in `lib.rs` is a second API. "Built with maturin" is true; "fast path is one pip install away" is not yet.
4. **The log sheet contradicts his own frontier.** `--workers 512` against `example.com` (one page), "512 in flight", 48,213 discovered. His code hashes a host to one shard and applies a per-host crawl delay, honouring robots crawl-delay. 512 in flight on one host is impossible by design. Italics do not fix wrong behaviour.
5. **HTTP/3 is a flag that prints a line.** `#[cfg(feature = "http3")]` wraps an `eprintln!`; the work is `reqwest/http3` behind `--cfg reqwest_unstable`. Fine as a flag, marketing as a bullet. Keep it off the profile.
6. **The things peers look for are absent, and absence reads as inexperience.** No `benches/` (CI echoes "No benchmarks configured"), no `tests/` directory (about 110 inline `#[test]`s, respectable, so say so), clippy `|| true`, `cargo audit` `continue-on-error`, no release workflow, which is how a one-wheel release happens. State it plainly; that earns more trust than omission.
7. **Smaller.** Edition 0.1.3 is dated 2025-11-08 while the repo merged PR #53 today: live repo, stale package.

## 4. What needs to be done

- **One worker figure from the code**, agreed across governor defaults, repo README and PyPI summary; then upright. Replace "16 × 32" with the truth: track lines = shards = cores on the drawing machine (the build job reads `os.cpu_count()`; caption "one shard per core · 16 here"); lead lines = semaphore permits, drawn as a count that moves between the governor's min and max. The survey animation then *is* the governor.
- **Approaches title-block notes** (four 13px mono lines): `1 Frontier: rendezvous-hashed by registrable domain, one shard per core` · `2 Permits governed by redb commit latency, adjusted every 250 ms` · `3 WAL: crc32-framed rkyv events, fsync batched, checkpointed into redb` · `4 Seeds: sitemaps · CT logs · Common Crawl; robots crawl-delay honoured`. Redis moves to the README.
- **README bullets:** "Up to N workers" → "A governor sizes the worker pool from storage commit latency, not from the network: the crawl slows when it cannot persist what it found." WAL → "Every frontier event is written to a CRC-framed write-ahead log (rkyv, zero-copy replay) before it reaches redb; a killed crawl resumes at the last record." Packaging → "Rust CLI and a Python package via maturin; prebuilt wheel for Apple silicon on CPython 3.13, source build with cargo elsewhere."
- **Log sheet obeys the code.** A real run (the spec already wants `assets/log.json`) against a host he may crawl, real shard count, real in-flight count. If 512 are requested and 4 are in flight because of politeness, print that: it demonstrates the frontier better than any bullet.
- **Edition line:** `Edition 0.1.3 · provisional · 2025-11-08 · macOS arm64 · cp313`. NOAA issues preliminary charts without apology; "provisional" is the chart word for Alpha.
- **Repo hygiene the page then quotes:** a `maturin-action` release workflow building abi3 wheels for linux x86_64/aarch64, macOS x86_64/arm64, Windows; drop `target-cpu=native` for release; one `criterion` bench (frontier dispatch, WAL append); `clippy -D warnings`.

## 5. Improvements and ideas

1. **Bold: four releases in 74 minutes becomes Notice 0.** PyPI timestamps: 0.1.0 at 18:38 and 0.1.1 at 18:41 with 155 KB wheels (no compiled extension); 0.1.2 at 19:51 at 2.7 MB with the binary; 0.1.3 at 19:52. A published mistake corrected within the hour is literally a Notice to Mariners. "Notice 0: editions 0.1.0 and 0.1.1 were issued without the engine; corrected by 0.1.2 the same evening." It turns the weakest fact on the page into evidence for principle two.
2. **The survey vessel as governor.** Lead lines over the side rise and fall during the 24 s one-shot, coupled to how fast the WAL tape fills against how fast the anchorage takes it. Same rule as the code, no caption.
3. **Depth = commit latency.** Illustrative soundings in the survey ground follow the shape of a real redb commit EWMA trace (ms, italic), the throttle threshold drawn as the 5-contour danger line. A reader who knows governors sees the mechanism in the bathymetry.
4. **Second-look layer for peers:** one upright `0.01` among the soundings (`BLOOM_FILTER_FALSE_POSITIVE_RATE`) and `10` as the drying height on Rate Limit Shoal (MB body cap). Uncaptioned.
5. **Instruments strip gets a "Hull" column:** `tokio · reqwest+hickory · redb · rkyv · fastbloom · maturin`.

## 6. What the page says, and what it should

Today: a developer with excellent taste who reached for the biggest numbers in the README, and whose Python package you probably cannot install. The code says something better: someone who chose rendezvous hashing by registrable domain, wrote his own CRC-framed WAL in front of redb, throttles on storage latency, honours crawl-delay, detects completion by plateau and streams bodies behind a cap, in 13k lines with three `unsafe`s and CI on three platforms, and is honest enough to label it Alpha. Say the second thing, with one worker figure, one install truth and a log that behaves like the frontier. The sentence that would make me click: **"The throttle watches the database, not the network: a governor reads redb commit latency every 250 ms and grows or shrinks the tokio permit pool, so the crawl slows when it cannot persist what it found."**

## 7. Five lines

1. The worker count is 512 on the page, 256 on PyPI, 32–512 in the repo README and 256–1024 in `governor.rs`; pick one from the code, make all sources agree, and only then set it upright.
2. "16 lines × 32 = 512" is invented geometry: shards are `num_cpus`, workers a semaphore the governor resizes; draw shards as cores and lead lines as permits that change during the survey.
3. "One `pip install` away" is untrue off Apple silicon + CPython 3.13 (one wheel, `target-cpu=native`, sdist needs cargo); say "wheel for macOS arm64, source build elsewhere" until a maturin-action release workflow exists.
4. The log shows 512 in flight on example.com, which his own per-host politeness forbids; record a real run and let the frontier's restraint be the demonstration.
5. Lead with the true mechanism (governor sized from redb commit latency, CRC-framed rkyv WAL checkpointed into redb, frontier rendezvous-hashed by registrable domain) and turn the four same-day PyPI releases into "Notice 0" instead of hiding them.
