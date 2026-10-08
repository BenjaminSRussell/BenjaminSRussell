# Crit 02 — the cartographer's lens: is this a chart, or a picture of one?

## 1. First impression

Handsome, far above the GitHub median, and "NOT FOR NAVIGATION" made me smile because that stamp is real. To someone who has drawn sheets, though, it reads as a topographic map wearing a sailor's hat: no blue water, land where there should be shoals, a portolan star beside modern light characteristics. The metaphor is announced loudly and then not used to say anything a bullet list could not.

## 2. What works

- "Grafana Lt · Fl(3) 10s" is a correctly formed light characteristic; the one place the chart grammar is used exactly, and the best detail on the page.
- Survey vessel = crawler, soundings = rows, lights = observability, anchorage = storage, WAL tape = the log. These mappings are sound and the copy ("depths in trusted rows") makes depth mean trust. Lean on that.
- Soundings kept clear of the course, index contours heavier than intermediates, double neat-line, 3-digit bearings: whoever wrote `chartlib.py` has looked at a sheet.
- Honest live stats and a "tide table arrives with the first refresh" placeholder rather than a fake curve.

## 3. Problems, ranked by impact

1. **No shallow-water tint (hero, approach, survey).** What makes a chart read as a chart is blue tint between the 0 and 5/10 m contours, buff land, nothing else coloured. Here water is paper and land is hatched buff; hatching on a chart means foul ground or a dredged limit, not land. Eleven unlabelled contours look like hillsides. `cool` is "reserved" in the palette; this is what it is for.
2. **Shoals drawn as islands (hero).** "Rustmapper Shoal" and "Common Crawl Bank" are submerged features: tinted water inside a dotted danger line, soundings inside, name in italic *because* it is a water feature. You set the names italic (correct) and filled them as land (wrong); "Delta Lake" is an island. The fix is the better story: shoals are where soundings matter, which is where his tools work.
3. **Buoyage is internally inconsistent (hero, approach).** The code says "starboard hand, returning" for red, which is IALA Region B (Americas). But in Region B red marks are *nuns* (conical) and green are *cans*; red-can / green-cone is Region A (Europe). Pick a region. The hero also puts a red/green pair at both ends of one course, so one end is entered the wrong way round.
4. **Mixed eras (hero).** A 16-point portolan star with rhumb lines is 16th century; minute bars, Fl(3) 10s and Plex Mono are 20th. A modern rose is two graduated rings (true outside, magnetic inside, variation noted), no star, no E/S/W letters. The rhumb lines carry no information and are the main source of the "decorative" feel.
5. **Survey geometry is wrong (survey sheet).** A fan from a stationary boat is a sonar cartoon. Survey is parallel track lines at fixed spacing with cross-lines for checks: 512 workers = parallel lines (draw 16, label "×32"); a sharded frontier = lettered survey blocks. The fan says less than the truth would.
6. **Missing title-block furniture (hero).** A title carries name, number, scale (1:n), projection, datum, "SOUNDINGS IN METRES", edition and date, "Corrected through NM nn/yy", source diagram, publisher. Yours has a tagline, a scale bar and a date range; the missing items are the ones that could carry meaning (§5). Also "NOT FOR NAVIGATION" escapes the cartouche on the right; a title block never leaks.
7. **"Here be dragons" (footer).** One 16th-century globe and every tea towel since; experts wince. The real edge conventions, "UNSURVEYED", "LIMIT OF SURVEY 2026", "Continued on Chart 28", all say "what I have not built yet", a better ending.
8. **Soundings scale and conventions.** 9.5 px soundings at 68% become 6.5 px, ~3 px on a phone: texture, not data. Real sheets distinguish upright (surveyed) from slanted (unreliable) soundings and never write "open water" on open water. 30 larger soundings would beat 56.
9. **Rotating beam vs Fl(3) 10s (approach).** A group-flashing light does not sweep; it flashes three times in ten seconds. An opacity `keyTimes` sequence does it and is more hypnotic than a wedge.
10. **Spelling drift.** "Scrapy Harbor" (hero, README) vs "SCRAPY HARBOUR" (approach render); "metres" vs US buoyage. Pick a hydrographic office and spell like it.

## 4. Expectations: what months of team work looks like

Testable: (a) a hydrographer can name the IALA region, sounding unit and datum from the sheet alone; (b) every symbol used appears in the legend with its S-4 meaning *and* its meaning here; (c) nothing is purely decorative: each contour, mark and note traces to a repo, stat, date or principle; (d) day and night editions differ in *what is visible*, not only palette; (e) a 360 px render still shows name, shoals, marks and one light; (f) chart number and sheet series agree across all seven sheets and the README; (g) nothing bleeds outside its frame.

## 5. Proposals, ranked

**Meaning (say more than they literally say)**

1. **Source diagram in the title block.** The inset every chart carries, dividing the sheet into lettered areas with a table: "A — rustmapper, 2025–26, full coverage; B — Scrapy scout, partial; C — Common Crawl index, 2024, lead line only". It is literally how his seeding works and tells an engineer in two seconds that he knows surveyed from inferred. One 120×60 px inset, three caption lines.
2. **Shoals as the project sites, with blue tint and danger lines.** Tint `cool` at 12–18% inside the shallow contours, dotted danger line round each shoal, soundings dense inside and sparse in deep water. Depth = trust is then drawn, not captioned. Add a datum note that is true and funny: "SOUNDINGS REDUCED TO RAW LAYER (DELTA LAKE)", principle 2 stated as a chart datum.
3. **Notices to Mariners as the changelog.** "Corrected through NM 40/26" in the title and a four-line NM table on the legend sheet: rustmapper 0.1.3 on PyPI, Scrapy platform, this chart's edition, real dates from the repos. The reader learns he ships and maintains.
4. **Numbered lateral marks for the pipeline (approach).** G "1" URLS, R "2" SCOUT, G "3" ANALYZE, R "4" SUMMARIZE, numbered from seaward, each with its light ("Fl G 4s"). The pipeline order becomes navigational fact. One sector light at the entrance mapped to the circuit breaker: red sector drawn = breaker open, so "breaker closed" is an unlit sector, not a green dot.
5. **The tidal diamond, honestly fed.** A lettered diamond ◇A on the hero keyed to the tide table on Sheet 2, built from real data `build_stats.py` can fetch: commits by hour or weekday as "HW" and rates. Cross-sheet references are how a series works, and the empty "TIDE" slot is waiting.
6. **Wrecks for the shelved repos.** The "also on the shelf" four become wreck symbols with a sounding over them, "Wk" and the year. A chart that admits hazards is more trustworthy; so is a profile.

**Delight on second look**

7. **A real night edition.** Under red bridge light red ink vanishes and green goes black, which is why charts print lights and cautions in magenta. By night you steer by lights, by day by marks. So: night dims ink to `ink2`, lowers contour opacity, and makes the lights the brightest things on the sheet (`feGaussianBlur` halo, buoys flashing their characteristics in SMIL); day has no beams and shows the structures. Two editions that differ in content, and the difference *is* principle 3, "lights before speed".
8. **Replace the star rose with a two-ring rose whose inner ring is a 24-hour clock.** Outer: 360° true, 1° ticks. Inner: 24 hours, rotated so his modal commit hour sits at north, noted "VAR 23h (2026)" or whatever the data says. A hydrographer sees a variation note; a reader learns when he works. Drop the rhumb lines.
9. **Chart number outside the neat line, in the corners,** plus a tiny series diagram on the legend sheet showing how Sheets 1–7 adjoin: a reward for noticing the sheets are one chart.
10. **Footer as "LIMIT OF SURVEY".** Keep the boat and the fall, drop the dragons: dotted limit line, "UNSURVEYED", and one true line: "beyond this line, work not yet started".

## 6. What it says about him now vs what it should

Now: someone with real taste who found a beautiful metaphor and dressed his work in it. An expert sees props (star rose, rhumb lines, hatched islands, dragons) arranged pleasantly, and props say "I liked the look of charts".

It should say: here is a person who treats a web crawl as a hydrographic survey because that is what it is, who knows a sounding from an inference, labels his datum, numbers his marks, notes his corrections and admits his wrecks. Each is a chart convention and each is an engineering virtue he actually has. Make the claims in the chart's grammar and the metaphor stops being a costume and becomes the argument.
