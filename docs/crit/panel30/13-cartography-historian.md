# Crit 13 — historian of cartography: which chart is this pretending to be?

I study sea charts as printed objects: Blaeu and Van Keulen, engraved Admiralty sheets 1800–1950, US Coast Survey, the lithographic colour charts after 1968, Imray's house style. I looked at hero-day/night-2x, approach-scrapy-day-2x, footer-night-2x, page-day-full, then STANDARDS, CHANGELIST and the three specs.

## What is good

- **The restraint is Admiralty restraint.** One ink on cream, red and green only where buoyage needs them, no shading, no vignettes. This is a Hydrographic Office sheet, not a gift-shop reproduction, and it is the page's strongest decision.
- **Double neat line with alternating minute bars** is correct 19th–20th-century furniture and says "chart" to anyone who has handled one. It also gives the hero its silhouette.
- **"Grafana Lt · Fl(3) 10s"** is a properly formed post-1930 light characteristic; one exact detail buys credibility for the sheet.
- **Water names italic, land names upright** (Rustmapper Shoal vs Scrapy Harbor): the one lettering rule applied, and the right one.
- **The specs already repair the worst historical errors**: star rose and rhumb lines gone, hatched islands become tinted shoals, "Here be dragons" (one globe, c. 1510, never a sea chart) becomes LIMIT OF SURVEY, the pictorial sector wedge becomes a ruled sector. Endorsed.

## What is bad, ranked

1. **The page does not know what era it is.** Portolan star and rhumb lines are 1550–1700; the galleon in open water is Blaeu; minute bars and a graduated rose are 1800+; tinted depth contours are post-1870 and in colour only post-1968; Fl(3) 10s is 1930s; IALA Region B is 1980; mono tracked caps are Leroy stick lettering from US Coast & Geodetic Survey sheets of the 1960s–80s. The mixture reads as costume because each prop is sincere about a different century. The specs remove the Blaeu props, but nobody has written down the era to commit to. **It should be the late paper chart, c. 1985–2000**, the last Admiralty/NOAA sheets before ECDIS: everything the page wants (metric-style soundings, blue tints, buff land, IALA marks, light abbreviations, stick-lettered notes) belongs to that decade and nothing else does.
2. **The cartouche is the wrong object.** A left-aligned, double-ruled box with tagline and scale bar reads as a Mapbox attribution panel. A period title block is open (no frame), centred, stacked in a strict size hierarchy, placed in quiet water: region in spaced small caps, chart name large, survey authority and dates, SOUNDINGS IN FATHOMS, natural scale, datum. The *imprint* is never inside it: "Published at the Admiralty 1st Jan. 1853 under the Superintendence of Rear-Admiral Washington, Hydrographer" sits centred below the bottom neat line, and the **small-corrections table** sits bottom-left outside the frame: "Small corrections 1932 — 1247. 1933 — 212, 468." Spec-hero keeps the box and puts the imprint data inside it. Both are wrong, and both throw away a meaning slot.
3. **"NOT FOR NAVIGATION" is the one genuine tourist-shop convention on the page.** Hydrographic offices never printed it; it is the disclaimer on decorative reprints and web previews. It says "souvenir". Drop it; honesty is carried by datum, edition and the italic convention.
4. **Eleven evenly spaced contours is hypsometric topography, not hydrography.** Charts of the era draw 2, 5, 10, 20, 30, 50, 100 and tint to 10 m; the index figure sits *in a break of the line*. Evenly stepped unlabelled lines are a landscape in disguise.
5. **Soundings on a grid, all one weight.** Real soundings follow survey lines, thicken on hazards, thin in deep water, and are condensed, slightly slanted numerals with a subscript for the sub-unit (3₂ = 3 fathoms 2 feet). A lattice of two-digit numbers is a spreadsheet on paper. The spec fixes placement, not figure style.
6. **Square interior graticule.** Mercator parallels are not equally spaced, and interior lines are few and labelled at the margin. Graph paper quietly undoes the minute bars.
7. **Two-class lettering.** Period sheets used five or six: title caps, land names roman, water names italic, lights and notes upright sans, soundings slanted condensed, cautions in colour. Here everything that is not a name is one mono size in tracked caps, so there is no middle register. Imhof's Swiss rule: hierarchy is what makes small type legible.
8. **Pictorial lighthouse** (approach): a drawn tower is 17th-century; from the 1850s it is a star with a flare. "Harbour" vs "Harbor" with Region B: if the region is the Americas, spell like NOAA.

## What needs to be done

- **Era note in DESIGN.md**: "drawn as a 1990s hydrographic office sheet; nothing older than 1950 except the display serif of the name," which stands in for engraved title lettering and is the one allowed anachronism.
- **Open title block**, centre-stacked, no frame, under the name: `THE OPEN WEB` / *Full-stack developer · mostly crawlers, lately in Rust* / `SOUNDINGS IN COMMITS · DATUM: MAIN` / `NATURAL SCALE 1:{commits}` / `IALA REGION B`.
- **Imprint outside the neat line, bottom centre**, Plex 13: `Published at github.com/BenjaminSRussell · {build date} · under the superintendence of scripts/build_assets.py`. True, dry, the first joke an expert gets.
- **Small-corrections table, bottom-left outside the neat line**, generated from the profile repo's commit history: `Small corrections 2025 — 3, 17, 41. 2026 — 5, 9.` The sheet records its own revisions in the slot charts reserve for it, and replaces the invented "Corrected through Notice 5" with a real one.
- **Contours**: 5–6 levels at chart intervals, tint to the second, figures in line breaks.
- **Sounding style**: condensed, 4° slant, and a legitimate subscript: `58₃` = 58 commits, 3 contributors, defined once in the legend. Two real numbers in one glyph, exactly the fathoms-and-feet pattern.
- **Variation stated in full** as the era did: `Var. 21h (2026) increasing 1h annually`, change computed from 2025 vs 2026 modal hour. "See colophon" is coy.
- **Graticule**: drop interior lines; label two meridians and two parallels at the margin.
- **Unit caution in colour**: during the metric change the only coloured margin text was `SOUNDINGS IN METRES` in magenta. Set `SOUNDINGS IN COMMITS` in the accent outside the neat line, top centre: a real convention, and it is where the metaphor is declared.

## Improvements and ideas

1. **Adjoining-chart index** on the legend sheet: a small rectangle diagram of how Sheets 1–6 abut, numbered, as every series carried. The reward for noticing the sheets are one chart.
2. **"New Edition" line** dated to the rustmapper PyPI release, plus the cancellation convention: "Cancels Chart 27 (v7)". Honest, funny, and exact.
3. **Bold: a Mercator of time.** Space the parallels by Mercator's secant stretching with latitude = weeks since Oct 2024, so recent weeks are exaggerated the way Greenland is, and the margin labels are months. The projection becomes an argument about recency in a profile, and it fixes the graticule.
4. **Imray-style legend discipline**: every symbol on the page appears once in the legend with its S-4 meaning and its meaning here; nothing appears that the legend does not define. Make it a build check.

## What the page says now, and should

Now: a developer with real taste who loves the *look* of old charts and assembled it from the best bits of four centuries; the disclaimer stamp, the galleon, the star rose and the dragons tell an expert it was learned from reproductions. It should say: someone who treats his crawl as a survey and knows an inference from a measurement, drawn as a 1990s hydrographic sheet with its imprint, small corrections and datum in the right places, each convention both correct and literally true of his work. Commit to one era and the costume becomes a uniform.

## Five most important lines

1. Commit to one era, c. 1985–2000 (late paper Admiralty/NOAA); write it in DESIGN.md and purge everything pre-1950 except the display serif.
2. Replace the boxed cartouche with an open, centre-stacked title block; move the imprint below the neat line and add a real small-corrections table from the README's commit history.
3. Delete "NOT FOR NAVIGATION": it is the one genuine souvenir convention on the page.
4. Chart-interval contours (5–6, figures in line breaks), slanted condensed soundings with a legend-defined subscript (commits, contributors), no interior square grid.
5. State the variation in full, "Var. 21h (2026) increasing 1h annually", from data, and set "SOUNDINGS IN COMMITS" in the accent outside the neat line as the era's unit caution.
