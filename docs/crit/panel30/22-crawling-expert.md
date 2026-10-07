# 22 — Web crawling / search infrastructure. Does the crawler story survive someone who runs crawlers?

## 1. Who I am, what I looked at

I build and operate large crawls: frontier design, politeness, dedup, Common Crawl and CT-log tooling, sitemap protocol work. I read README.draft.md, STANDARDS, CHANGELIST, both specs, the log/approach/survey renders, and the real READMEs of Rust-sitemap, Scrapy and go_go_go, because a hiring crawl engineer will click through and compare.

## 2. What is good, and why

- **The thesis is technically true.** Sitemaps lie about themselves: `lastmod` is routinely the deploy time or a constant; `changefreq` and `priority` are ignored by every major engine; sitemaps list 404s and redirects (ghost URLs) and omit the long tail. A reader who runs crawls trusts the author after that sentence.
- **The seed trio is correct and clever.** For the panel: every publicly trusted TLS certificate has been logged to Certificate Transparency since 2018, and each certificate names its hosts, so `staging.`, `grafana.`, `old-api.` appear in CT the moment they got a cert, linked or not. CT finds **hosts**; Common Crawl's index finds **URLs** that were once linked; sitemaps give you what the site *wants* seen. Three sources, three blind spots. It is also the honest reason "512 workers" makes sense: spread across hundreds of hosts, because on one host they would idle behind politeness.
- **The approach chart's grammar maps onto real crawl architecture**: track lines (per-host queues), cross-lines (hydrographers run check lines to verify soundings: dedup), the WAL tape, breakers as a sector light, health checks as leading lights. Nothing here is bad engineering in costume.
- **Rust-sitemap's own README is honest**: `--ignore-robots false` by default, "Many timeouts: internal hosts from CT discovery", throughput "50–200 URLs/minute, network-bound". An asset the profile has not used.

## 3. What is bad, ranked

1. **The log's example.com run is impossible on its face and contradicts the repo.** example.com is one page. The sheet claims `48,213 discovered`, `512 in flight`, wind 188–412 req/s, `48,213 urls · 4m 12s`. That is ~190 URLs/s against one host: 60–100× the 50–200 URLs/**minute** Rust-sitemap's README reports, and 512 concurrent connections to one origin is the definition of impolite. Italic numerals do not rescue it; an expert reads "demo target, invented throughput, and he did not notice it would be abusive." This one sheet can lose the technical reader.
2. **The profile never says the sentence every crawl engineer looks for.** Respects robots.txt (both crawlers do by default). One connection per host. Backs off on 429/503. Identifies itself. The draft says "per-host politeness" once, for go_go_go only. Politeness is *the* professional signal in this field; its absence reads as inexperience.
3. **go_go_go's first line is "advanced anti-bot evasion capabilities"**: JA3 spoofing via utls, rotating fake browser header sets (`--use-header-rotation` default **true**), "personas". The profile calls it "per-host politeness, Bloom-filter dedup". A reviewer who clicks reads spin. You cannot claim "my crawlers identify themselves" while one rotates Chrome/Safari fingerprints by default. Scrapy's README also sells "Aggressive crawling · 1000+ req/min".
4. **Precision slips an expert will catch.** "CT logs and Common Crawl are how you find the subdomains nobody links to": CT finds hosts, Common Crawl finds URLs. `rustmapper export-sitemap` emits `changefreq` and `default_priority=0.5`, the two fields engines ignore, while the thesis mocks sitemaps for being wrong about themselves.
5. **"Rate Limit Shoal" has the physics backwards.** A rate limit is the harbour's rule, not a hazard to route around; the polite boat slows.

## 4. What needs to be done (buildable now)

- **Log, option A (best):** Ben pastes a real `rustmapper` session on a domain he controls, `measured:true`, numerals upright. **Option B** (real, zero load on anyone): a **Common Crawl index query** session: `cdx` lookup of `*.{his-domain}/*` on `index.commoncrawl.org` for one `CC-MAIN` crawl, captures returned, distinct hosts, a CT count, then a polite crawl at 1–2 req/s per host. Reproducible by anyone. **Option C** (fallback): plausible italics: one host, `workers 512` idle behind politeness, wind **2 req/s**, position in the hundreds, duration in hours.
- **The politeness line, once, where the two systems are introduced:** "Both crawlers read robots.txt first, keep one line per host, back off on 429 and 503, and say who they are." Only what the defaults make true; if go_go_go's UA rotation stays, write "rustmapper and Scrapy".
- **go_go_go, upstream (an hour's work):** rename the feature "browser-faithful fetching", make it opt-in with an identifying default UA (`gogogoscraper/x (+repo URL)`), keep robots non-overridable when impersonation is on, turn the "ethical use warning" into policy. Then the profile can say "optional browser-faithful fetching for sites whose WAF misclassifies honest clients; robots.txt respected regardless." If the repo stays as is, the profile must not imply a fleet-wide policy or headline go_go_go with "per-host politeness".
- **Precision:** "CT logs name every host that ever got a certificate; Common Crawl remembers URLs that were once linked." Drop `changefreq/priority` from the shown export. Rename the shoal "429 Shoal · reduce speed" and add a chart **speed limit** mark on the channel: `Speed 2 req/s · per host`.
- **`build_stats.py` UA:** `profile-stats (+https://github.com/BenjaminSRussell/BenjaminSRussell)`: the habit the profile claims, visible in the build.

## 5. Improvements and high-level ideas

1. **Robots.txt as a restricted area.** Charts mark restricted areas with a T-dashed magenta boundary and "Entry prohibited". Draw one on Approaches labelled `Disallow: /admin · robots.txt`; track lines stop at it; the packet boat's course bends around it. Nobody is told the crawler obeys robots; they watch it.
2. **Track lines = per-host queues; spacing = crawl-delay.** Caption "16 lines × 32 = 512 workers · one vessel per line"; legend `Track line · one host, one connection`. Name the spec's cross-lines **check lines**: "a sounding taken twice is written once" (the Bloom filter, and what cross-lines are for).
3. **Bold: a Zones-of-Confidence diagram instead of a plain source diagram.** Real charts rate survey quality by zone (CATZOC A1–D). Rate the three seeds honestly in that corner: **A sitemaps** "position good, existence doubtful" (ghost URLs); **B CT logs** "existence certain, many unreachable" (the README's own troubleshooting row); **C Common Crawl** "reported {year}, not since verified". Then use the hydrographer's doubt marks on the chart: `ED` (existence doubtful) by a CT islet that timed out, `Rep (2024)` by a sitemap URL that 404s, `SD` (sounding doubtful) where lastmod and page disagree. The thesis becomes notation, which is how serious crawl teams talk about seed quality.
4. **Real crawl metrics in one remarks line:** `200 ×…  3xx ×…  404 ×…  429 ×…  robots-denied ×…  dup ×…  p99 fetch …ms  hosts active …`. Even italic, it shows he knows the dials.
5. **Dedup on the WAL tape.** A few cells hatched instead of lit, "already sounded"; one `SD` cell for the Bloom filter's false positive. The quietest honest second-look layer on the page.

## 6. What the page says about its maker now, and what it should say

Now: someone who understands discovery deeply (the seed trio, raw-before-clean, breakers and dashboards) but whose demonstration run would get an IP blocked, who calls a crawler advertising "anti-bot evasion" polite, and who has not written down the rules a crawler lives by. Talent without operating scars. It should say: a crawl engineer who knows the web is wrong about itself *and* behaves correctly toward it anyway; who seeds from three sources because each lies differently, and rates the lies; who obeys robots unasked, runs one line per host, and whose one logged session is real, slow where it should be, and reproducible by anyone who copies the command.

## 7. Five most important lines

1. The example.com log is impossible (48,213 URLs on a one-page domain at ~190 URLs/s, 512 in flight) and contradicts Rust-sitemap's README (50–200 URLs/minute); replace it with a real session on a domain Ben controls or a Common Crawl index query, else make the italics plausible (one host, 2 req/s, hours).
2. Add the politeness sentence once: robots.txt first, one connection per host, back off on 429/503, identifying User-Agent; only for the crawlers whose defaults make it true.
3. Fix go_go_go's "anti-bot evasion" upstream (opt-in browser-faithful fetching, identifying default UA, robots non-overridable) before the profile implies a fleet-wide policy; until then describe it accurately, not as "per-host politeness".
4. Encode politeness and dedup in chart grammar: a T-dashed restricted area `Disallow: … · robots.txt` that tracks and course skirt; "one vessel per line"; cross-lines named check lines.
5. Replace the source diagram with a Zones-of-Confidence diagram and put `ED` / `Rep (year)` / `SD` on the chart for CT hosts that never answered, sitemap ghosts and lastmod lies: the thesis as notation.
