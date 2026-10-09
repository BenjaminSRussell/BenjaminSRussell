# Round 5 — the navigator's memo

Deck officer, 38, paper and ECDIS. A real chart is terse because every mark is something you steer by. v10 has invented lights, a compass rose that corrects nothing, and a hatched "unsurveyed" margin when `stats.json` says `unsurveyed: []`.

## 1. What a visitor needs to know about Ben

1. **What he builds.** Crawl and data infrastructure, Python and Rust. Answered by the role line; the image says nothing.
2. **What I can use today.** `pip install rustmapper`, 0.1.3 on PyPI. Answered in text; the image hides it as "edition".
3. **What is alive and what is parked.** Scrapy Harbor (26 commit-days since Sep 2025) and rustmapper (22) are the working projects; most of the other 19 are a day or four. Not answered. (Audit: 18 repos share `last: 2026-10-07`, one sweep day.)
4. **How deep the engineering goes.** Governor, WAL, shards, breakers, raw-first storage. Answered by the bullets; the image carries none of it.
5. **What will bite me.** Non-Apple `pip` needs a Rust toolchain; the worker-pool figure is reported three ways. Buried in bullet five.
6. **Where and when he works.** Eastern time (every commit is -0400/-0500), afternoons, all week. Answered only as "VAR 14h", which nobody decodes.
7. **How to reach him.** Email only; LinkedIn and résumé slots are empty.
8. **Can I trust the numbers.** Three commit totals in the survey log say no.

## 2. What a real chart carries, and which conventions map honestly

On watch, in order: datum and date (can I trust it), contours (where is safe water), lights (what will I see and when), hazards, the channel (the way in), notices (what changed), title block. Everything else is edge.

**Honest**

- **Datum and survey date** = "author's commits on main, 7 Oct 2026". The one piece of fine print that must stay.
- **Source diagram** = provenance: clones live, GraphQL cached, REST partial. A small box, not a sentence with three totals.
- **Contours** = activity bands by month. Water of like depth, months of like work. Answers item 3.
- **Light character** = something in his code that repeats on a fixed period. Two measured ones: Prometheus scrapes every 15 s (sha-cited); the governor samples redb every 250 ms. *Fl 15s* on Scrapy Harbor is true the way a light list is true. *Fl R 4s* in v10 is invented, and a sailor spots that first.
- **Buoyed channel** = the documented way in: the three-line install block. Draw the code block, not buoys.
- **Clearing limits** = robots.txt, crawl-delay honoured, per-host throttle. Limits the crawler stays outside by design.
- **Hazard mark** = a known gotcha: the toolchain requirement; 148 stale branches on `game_engine`.
- **(rep.)** = reported, not surveyed. The pool is 256–1024 in code, 32–512 in the README, 256 on PyPI. A chart prints exactly that as *256–1024 (rep.)*.
- **Limit of survey** = today's date at the right edge. Honest as a date; hatching beyond it claims unsounded ground that does not exist.
- **IALA Region B** = he is in the Americas. True; one word, never a buoy scheme.

**Forced (wince)**

- **Soundings in commit-days.** A sounding is useful because the reader has a draught. Nobody has a draught in commit-days.
- **Compass rose, VAR 14h.** Variation is a correction you apply to a bearing. A peak hour corrects nothing.
- **HW / tidal diamonds.** Tides are periodic. "HW sweep 7 Oct 358" is one day touching 18 repos, the opposite of a tide.
- **Rocks.** A rock is a hazard to the reader. A four-commit repo is shallow water: a small figure, unnamed at this scale.
- **Small corrections 2026—5—173.** Charts cite the last notice applied; 173 is the profile repo's commit count. Fabricated provenance.
- **Chart names** (*Profile Shoal*, *Data Science Bank*). A feature carries what the locals call it: `Data_science_dev`.
- Leading lines, tidal streams, the boat: no fact behind them.

## 3. The proposal

One sheet, chart-styled, geography is time. Desk 870×460; phone 390×560 portrait.

**Desk.** A coastline runs left to right. The bottom edge is a scale from Sep 2025 to Oct 2026 drawn like a latitude scale: month ticks, no word "time". Right edge is 7 Oct 2026, nothing beyond it. Title block top-left, three lines: *Ben Russell* large; *Crawl and data infrastructure · Python and Rust*; in 11 px, *21 repositories · author's commits on main · 7 Oct 2026 · Eastern time*.

The nine repos with seven commit-days or more are shaded banks spanning first to last active month, tinted in three contour bands by commit-days per month, no figures inside. Labels are repo names as written, 13 px minimum. Scrapy Harbor is the largest feature and carries the one light, *Fl 15s*. rustmapper carries a berth mark, *0.1.3 · PyPI*, the figure *256–1024 (rep.)*, and one hazard mark noted *pip builds from source off Apple silicon; needs Rust*. The other twelve repos are plain soundings: a small figure at their first active month, no name, no symbol. Bottom-right, a source-diagram box: *clones live · GraphQL cached · REST partial*. Nothing else.

**Phone.** The same sheet as a strip chart, the way an Intracoastal pilot runs along the route: title on top, scale down the left edge, coast running down, labels to the right, nothing under 13 px, nothing overlapping. The twelve soundings become one line at the foot: *12 more below seven commit-days*.

**What moves.** The light only, at its real character: a beat every 15 s. Reduced motion gets a still. Nothing sails.

**The page under it**, in order, text kept unless struck below: links; *builds / Languages / Stack*; rustmapper, bullets, install block (toolchain sentence promoted to bullet one); Scrapy Harbor and bullets; the four other repos; the fold; the renamed rules list; one provenance line.

## 4. Details and one-off words

1. **(rep.)** after 256–1024. The joke a sailor repeats.
2. **Fl 15s** on the harbour, cited to `prometheus.yml`.
3. **Eastern time** in the title block; on the page, *afternoons, seven days a week*.
4. **0.1.3 · the fourth upload that evening.** Four releases between 18:38 and 19:52 on 8 Nov 2025. True, once.
5. **Not to be used for navigation**, 7 px, bottom margin, desk only. Every reproduction chart carries it. Riskiest; cut if anyone groans.

## 5. Kill list

- *SOUNDINGS IN COMMIT-DAYS*: names the metaphor; the unit helps no one.
- *CHART NO. 21 · SHEET 1 · SMALL CORRECTIONS 2026—5—173*: fake provenance.
- The eight-line title block: keep three lines.
- Compass rose and *VAR 14h*: corrects nothing.
- *Fl R 4s*, *Fl G 4s*, buoys, dashed track: invented lights, a channel into nothing.
- *HW · SWEEP 7 OCT 358*: a sweep dressed as a tide.
- Rocks fringe: his small repos are not hazards.
- *LIMIT OF SURVEY*, hatched *UNSURVEYED*: `unsurveyed: []`. End of the world, not smart.
- Sailboat and anchor: not drawn well enough.
- *sitemap.xml lies again*: a pencil note means an uncorrected chart; here, a joke that needs explaining.
- Chart-style feature names: use the repo names.
- Text: *survey vessel*, *where a run is operated*, *mark in the channel*, *leaves the harbor*, *Other waters*, *Below the waterline*, *Notices to mariners*, *Found a wrong depth?*, *Survey log*. Each says it is a ship. Headings become *Also*, *15 more repositories*, *Working rules*, *Found an error?*
- Three commit totals: one number or none.
- Alt text *A boat sails in and anchors*: say what the sheet shows.

## 6. The two-second test

**Two seconds, iPhone:** a name, "crawl and data infrastructure, Python and Rust", a coastline with two big named features and a date scale. It reads as a chart and never says so.

**Thirty seconds:** two real projects, one on PyPI since Nov 2025 and still worked on, the other a crawl platform whose monitoring blinks every 15 s; the rest small and dated; one figure marked reported, not measured, which is the moment the reader decides the rest of the page is honest.
