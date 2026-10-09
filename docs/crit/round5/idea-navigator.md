# Round 5 — the navigator's memo

Deck officer, 38, paper and ECDIS. A real chart is terse because every mark on it is something you steer by. v10 is the other kind: an eight-line title block, invented lights, a compass rose that corrects nothing, and a hatched "unsurveyed" margin when `stats.json` says `unsurveyed: []`. That is the test below.

## 1. What a visitor needs to know about Ben

1. **What he builds.** Crawl and data infrastructure, Python and Rust. Answered by the role line; the image says nothing.
2. **What I can use today.** `pip install rustmapper`, 0.1.3 on PyPI. Answered in text; the image hides it as "edition".
3. **What is alive and what is parked.** Scrapy Harbor (26 commit-days since Sep 2025) and rustmapper (22) are the working projects; most of the other 19 are a day or four. Not answered. (For the audit: 18 repos share `last: 2026-10-07`, one sweep day, not 18 live projects.)
4. **How deep the engineering goes.** Governor on redb latency, CRC32 WAL, rendezvous shards, breakers, raw-first Delta Lake. Answered well by the bullets; the image carries none of it.
5. **What will bite me.** Non-Apple `pip` needs a Rust toolchain; the worker-pool figure is reported three ways. Half answered, in bullet five.
6. **Where and when he works.** Eastern time (every commit is -0400/-0500), afternoons, all week. Answered only as "VAR 14h", which nobody decodes.
7. **How to reach him.** Email only; LinkedIn and résumé slots are empty.
8. **Can I trust the numbers.** Not answered: three commit totals in the survey log talk the reader out of the rest.

## 2. What a real chart carries, and which conventions map honestly

On watch, in order: datum and date (can I trust it), soundings and contours (where is safe water), lights and characters (what will I see and when), hazards (what will sink me), the buoyed channel (the safe way in), notices (what changed), title block (what the sheet is for). Everything else is edge.

**Honest**

- **Datum and survey date** = "author's commits on main, 7 Oct 2026". The one piece of fine print that must stay.
- **Source diagram** (which survey each part came from) = provenance: clones live, GraphQL cached, REST partial. Exactly what the box is for. A box, not a sentence with three totals.
- **Contours** = activity bands by month. Water of like depth, months of like work. Answers item 3.
- **Light character** = something in his code that repeats on a fixed period. He has two measured ones: Prometheus scrapes every 15 s (sha-cited); the governor samples redb every 250 ms. *Fl 15s* on Scrapy Harbor is true the way a light list is true. *Fl R 4s* in v10 is invented, and a sailor sees an invented character before anything else.
- **Buoyed channel** = the documented safe way in: the three-line install block. Draw the code block, not buoys.
- **Clearing limits** = robots.txt, crawl-delay honoured, per-host throttle. Limits the crawler stays outside by design.
- **Hazard mark** = a known gotcha: the toolchain requirement; 148 stale branches on `game_engine`. Wreck = an archived repo (none yet).
- **(rep.)** = reported, not surveyed. The pool is 256–1024 in code, 32–512 in the README, 256 on PyPI. *256–1024 (rep.)* is how a chart prints exactly that.
- **Scale and inset** = the two real projects at large scale, the rest small. The text does this; the image should.
- **Limit of survey** = today's date at the right edge. Honest as a date; hatching beyond it claims unsounded ground that does not exist.
- **IALA Region B** = he is in the Americas. True, cheap, lands once as a word; never as a buoy scheme.

**Forced (wince)**

- **Soundings in commit-days.** A sounding is useful because the reader has a draught. Nobody has a draught in commit-days. Measured, so not a lie; still decoration.
- **Compass rose, VAR 14h.** Variation is a correction applied to a bearing, printed with year and annual change. A peak hour corrects nothing.
- **HW / tidal diamonds.** Tides are periodic. "HW sweep 7 Oct 358" is one day touching 18 repos, the opposite of a tide.
- **Rocks.** A rock is a hazard to the reader. A four-commit repo is shallow water: a small figure, unnamed at this scale.
- **Small corrections 2026—5—173.** Charts cite the last notice applied; 173 is the profile repo's commit count. Fabricated provenance is worse than none.
- **Chart names** (*Profile Shoal*, *Data Science Bank*). A feature carries what the locals call it: `Data_science_dev`.
- Leading lines, tidal streams, the boat: no fact behind them.

## 3. The proposal

One sheet, chart-styled, geography is time. Desk 870×460; phone 390×560 portrait.

**Desk.** A coastline runs left to right. The bottom edge is a scale from Sep 2025 to Oct 2026 drawn like a latitude scale: month ticks, no word "time". Right edge is 7 Oct 2026, nothing beyond it. Title block top-left, three lines: *Ben Russell* large; *Crawl and data infrastructure · Python and Rust*; in 11 px, *21 repositories · author's commits on main · 7 Oct 2026 · Eastern time*.

Along the coast, the nine repos with seven commit-days or more are shaded banks spanning first to last active month, contour-tinted in three bands by commit-days per month, no figures inside. Labels are repo names as written, 13 px minimum. Scrapy Harbor is the largest feature and carries the one light, *Fl 15s*. rustmapper carries a berth mark, *0.1.3 · PyPI*, the figure *256–1024 (rep.)*, and one hazard mark noted *pip builds from source off Apple silicon; needs Rust*. The other twelve repos are plain soundings: a small figure at their first active month, no name, no symbol. Bottom-right, a source-diagram box: *clones live · GraphQL cached · REST partial*. Nothing else.

**Phone.** The same sheet as a strip, the way a river or Intracoastal pilot runs along the route: title on top, scale down the left edge, coast running down, labels to the right, nothing under 13 px, nothing overlapping. The twelve soundings become one line at the foot: *12 more below seven commit-days*.

**What moves.** The light only, at its real character: a beat every 15 s. Reduced motion gets a still. Nothing sails.

**The page under it**, in order, existing text kept unless struck below: links line; *builds / Languages / Stack*; rustmapper, bullets, install block (the toolchain sentence promoted to bullet one); Scrapy Harbor and bullets; the four other repos; the fold with fifteen; the renamed rules list; one provenance line.

## 4. Details and one-off words

1. **(rep.)** after 256–1024. The joke a sailor repeats to someone else.
2. **Fl 15s** on the harbour, cited to `prometheus.yml`.
3. **Eastern time** in the title block; on the page, *afternoons, seven days a week*.
4. **0.1.3 · the fourth upload that evening.** Four releases between 18:38 and 19:52 on 8 Nov 2025. True, once.
5. **Not to be used for navigation**, 7 px, bottom margin, desk only. Every reproduction chart carries it. Riskiest; cut if anyone groans.

## 5. Kill list

- *SOUNDINGS IN COMMIT-DAYS*: names the metaphor; the unit helps no one.
- *CHART NO. 21 · SHEET 1 · SMALL CORRECTIONS 2026—5—173*: fake provenance.
- *IALA REGION B · DATUM: MAIN · 9 CHARTED · 12 AS ROCKS*: eight lines nobody reads; keep three.
- Compass rose and *VAR 14h*: corrects nothing.
- *R "2" Fl R 4s*, *G "1" Fl G 4s*, buoys, dashed track: invented lights, a channel into nothing.
- *HW · SWEEP 7 OCT 358*: a sweep dressed as a tide; totals are suspect anyway.
- Rocks fringe: his small repos are not hazards.
- *LIMIT OF SURVEY*, hatched *UNSURVEYED*: `unsurveyed: []`. End of the world, not smart.
- Sailboat and anchor: not drawn well enough to earn the exemption.
- *sitemap.xml lies again*: a pencil note means the sheet is uncorrected; here it is a joke that needs explaining.
- Chart-style feature names: use the repo names.
- Text: *is the survey vessel*, *is where a run is operated*, *its own mark in the channel*, *nothing leaves the harbor*, *Other waters*, *Below the waterline*, *Notices to mariners*, *Found a wrong depth?*, *Survey log*. Each says it is a ship. Headings become *Also*, *15 more repositories*, *Working rules*, *Found an error?*
- Three commit totals: one number or none.
- Alt text *A boat sails in and anchors*: say what the sheet shows.

## 6. The two-second test

**Two seconds, iPhone:** a name, "crawl and data infrastructure, Python and Rust", a drawn coastline with two big named features and a date scale. It reads as a chart and never says so.

**Thirty seconds:** two real projects, one installable from PyPI since Nov 2025 and still worked on, the other a crawl platform whose monitoring blinks every 15 s; the rest small and dated; the worker figure marked reported, not measured, which is the moment the reader decides the rest of the page is honest.
