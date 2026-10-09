# Round 5 review — the skeptic

Checked against rust-sitemap 00a877d, scrapy 74fd4f7, and fresh bare clones of both at HEAD (9 Oct).

## 1. Verdict

**SHIP AFTER FIXES.** It tells you about him without saying it's a boat, but the one mark meant to be a measurement is wrong, and one figure makes his best-tested project look untested.

## 2. What works

- The bullets are true: governor at 250 ms, CRC32 WAL with replay, rendezvous shards per core, crawl-delay, CT and Common Crawl seeders, merge schema evolution, the OPTIMIZE/VACUUM queue, HTTP/Delta/Redis breakers, MinHash LSH, bart-large-cnn. Holding back the worker-pool number until his README agrees with the code was right.
- Feb to Aug 2026 is empty water. That's true, it's the first thing a hirer checks, and it matches his contribution graph.
- The facts lines are the most useful thing on the page. "63 AI co-author trailers" is correct.

## 3. What must change

1. **`Fl 15s` is false** (every sheet render). 15 s is Prometheus's global default. The crawler's own job, `scrapy_app`, scrapes every **30 s**: `prometheus.yml` line 28 at the cited sha, unchanged at HEAD. The only thing on 15 s is Prometheus scraping itself. Fix: point `claims.scrape_interval` at the `scrapy_app` job, letter **Fl 30s**, beat every 30 s. Otherwise cut the light. A light with the wrong character is worse than none.
2. **"3 test files" sells rustmapper short** (page-desk-1, page-phone-2). The 3 are two Python files and one integration test. `src/` has 115 `#[test]`/`#[tokio::test]` functions. Fix: count test functions for both repos ("115 tests"). Also make Scrapy's "Built on" the deps that say what it is: `deltalake, redis, psycopg2, prometheus-client, datasketch`. Pandas and numpy are filler.
3. **The count doesn't add up, and one row is this README** (sheet-desk-day). The title says 21 repositories, but 7 rows plus "9 MORE" is 16. Five repos vanish without a word. And `BENJAMINSRUSSELL`, ten days spent making this page, is shown as his fourth-biggest work. That's lazy and self-referential. Fix: merge the profile repo into the last row and letter it **15 MORE**, so 6 + 15 = 21.
4. **One-day months draw as land, and the image is tidy, not memorable** (sheet-desk-day, rustmapper May and Aug). With a 3 px floor, one day draws almost as thick as five. rustmapper's August "bank" is one design-doc commit. Every bank is the same grey cigar, so nobody screenshots it. Fix: drop the floor to 1 px, draw any month with ≤2 days as a sounding dot on the centreline, and fill the band at 12 days instead of 15, so Oct 2025 reads as real land with its 10-day tint. The contrast between autumn 2025 and the empty spring is the picture. Make it loud.
5. **The dates disagree and the last tick hits the frame.** The sheet renders say 7 OCT 2026 and the page says "Measured 9 Oct 2026". Take both from `stats.taken`. The final "O" sits on the neatline (page-desk-1, sheet-phone-day): end the axis 14 px inside, or anchor it `end`.

## 4. The owner's test

**Two seconds, iPhone:** a name, "crawl and data infrastructure, Python and Rust", and a chart with named rows. **Thirty seconds:** Scrapy and rustmapper are the work. He was heavy in autumn 2025, quiet through summer 2026 and back in September. There's a Rust crawler on PyPI, a monitored platform with tests and passing CI, and facts you can check.

It never says "chart" or "ship". The border, `DATUM: MAIN` and the light carry the theme. Nothing is cringe and there's no pirate talk. It's helpful knowledge. The only dishonest mark is the 15 s light. The lazy data is the README row and the one-day banks. Fix those five and I'd open his repos from it.
