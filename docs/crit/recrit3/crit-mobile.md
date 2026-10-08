# Mobile + accessibility critique — v9.1 (phone sheets, alt text, Markdown at 360–390 px)

Reviewed: `readme-390.png` (sliced into `crit-mobile/slice-00..05.png`), the six `*-phone-360.png` day editions (also at 2x in `crit-mobile/`), six phone-**night** editions I rasterised myself from `assets/v9/*-phone-night.svg` with `scripts/render.mjs` (`crit-mobile/*-phone-night-360.png`; none were in the review set), the 870 px desk day/night editions, `readme-light.png` / `readme-dark.png`, `/home/user/BenjaminSRussell/README.md` (the current on-disk version, which already has the v9.1 "show, don't tell" cuts: no sheet captions, no heading glosses, empty table header) and `scripts/tokens.py` for the floors.

Measured facts the findings rest on:

- Phone sheets are 720 wide and shown at 355 CSS px (390 viewport) or 328 (360 viewport). Texture type (18 px on the sheet) is therefore **8.9 / 8.2 CSS px**; label type (26 px) is 12.8 / 11.8; machine (26 px) the same. Everything printed at the texture size on a phone is below any practical legibility floor.
- Token contrast (WCAG ratio): day ink/paper 12.5, ink2/paper 8.3, muted/paper 5.1, muted/shallow_b **4.07**; night ink/paper 10.0, ink2/paper 5.7, ink2/shallow_b **3.81**, muted/paper 7.2, ok/paper 10.7, accent/paper 6.1. Text in tinted water at night in ink2 is under AA for small type; on paper everything passes.
- Nothing on any sheet relies on colour alone: cans and nuns differ by shape, HW/LW by filled/hollow dot, "underway" by weight, lights by the star glyph. Good.
- In the phone render the `sh` code block widens the whole document to 633 CSS px (non-white pixels run to x=1259 of 1266 at DPR 2); on GitHub the block scrolls internally instead, but the third command is 62 characters and is cut at about 49 either way.

## Scores (0–3)

| | | Score | One line |
|---|---|---|---|
| J1 | Thesis in one line, said once | 3 | "I survey a web that is wrong about itself." on the hero, once; the prose paragraph elaborates rather than repeats. |
| J2 | Cover the name: hero alone argues the survey edge | 2 | On a phone the hero still argues it (thesis, UNSURVEYED band, SMALL-SCALE EDITION) but the survey vessel itself, rustmapper, is an unnamed `87₆` blob; "sitemap.xml lies again" is gone. |
| J3 | Cover the titles: a stranger names every sheet by silhouette | 2 | Hero, soundings, approaches, log and footer have silhouettes on a phone; the phone Instruments sheet is three lines of text on a paper rectangle and reads as a caption strip, not a sheet. |
| J4 | A hydrographer names region, unit and datum | 3 | Hero phone: The Open Web · soundings in commits · datum main · IALA Region B; Approaches phone: soundings in URLs · thousands · datum main · Region B. Carried. |
| J5 | Point at any mark: one sentence says its job, and it reads on a phone | 1 | On the phone the legend is cut to 13 rows: ✦ waypoints, the A/B/C zone boxes, ◻ and Δ, the pecked channel, the hatch, the tints, the subscript months and the week figures are explained nowhere on any phone sheet; the sources A/B/C are never named at all. And the figures themselves are 9 px. |
| J6 | The chart visibly changes with the data | 2 | Hero features, tide curve, compass variation and the heartbeat row all move; the phone log shows two "nothing to report" rows and the phone Instruments drops the first-commit dates, so two of six phone sheets show almost no data. |
| J7 | Honesty | 1 | The phone log drops "computed from settings", the one phrase that makes the sheet honest, leaving italics that no phone sheet explains; the soundings phone says "HW 358 · 5 Oct" for a week; four alt texts claim things the phone edition does not show. |
| J8 | Every still is finished | 1 | "429 Shoa" is clipped by the neatline; the leading line is drawn through `R "4"`; `265₅ 358₁` abut on the hero; the Markdown shows an empty header row and an orphaned "·". |
| J9 | Copy says each thing once | 2 | "crawl and data infrastructure" appears on the hero band and in the table, the language list on the hero band, the table and the Instruments sheet; defensible as chart-versus-text, but three times is three. |
| J10 | Recruiter finds field, systems, languages, contact in plain text in 60 s | 2 | The table and the Email link sit on screen two of the phone page, which is good; but the table now has two empty header cells (a screen reader announces a nameless two-column table), and heading navigation offers only metaphors. |
| J11 | Night is designed, not inverted | 3 | Phone night editions hold: navy paper, lights are the brightest marks, semantic text lifted to full ink on the phone (instruments.py:214, footer.py:284). |
| J12 | ≥ 4 uncaptioned second-look layers | 3 | Compass as a 24-hour clock, subscript months, upright/italic/underline, A/B/C zones, heartbeat cursor, the chart charting itself. They exist on the phone too, even where they cannot be decoded there (see J5). |

**Total 25 / 36.** The page is a desk page with a phone edition bolted on; the phone sheets look right and are honest in outline, but the data layer is set below legibility, the key that explains it never reaches the phone, and the alt texts describe the desk.

## Findings, ranked

### 1. The phone key is missing: nine kinds of mark on the phone sheets are explained nowhere a phone reader can reach — S/M
**Where.** `approaches-phone-360.png` legend (13 rows) versus `approaches-day-870.png` (33 rows). On the phone Approaches sheet itself: ✦ waypoints (nine of them down column C), the boxed A / B / C zones, ◻ and Δ beside the vessel, the pecked channel, the hatch, the two tints, the italic soundings; on the phone hero: the subscript month figures (`512₁`, `308₄`), the week figures (`358₁`, `17₁`, `0`), the ⊙ fix marks, the unlabelled `87₆`. The desk "Zones of confidence" table and the hero's "SOURCES · A SITEMAPS · B CT LOGS · C COMMON CRAWL" line are both dropped on the phone, so on a phone A/B/C are letters with no meaning anywhere on the page, including the Markdown.
**Why it matters.** J5 is the rubric item written for a phone reader, and on a phone it fails for most of what is drawn. The honesty convention (upright measured, italic not, underlined above datum) survives on the phone only as "12 Sloping · not measured"; "Upright · measured" and "Underlined · above datum" are gone, and the Colophon that would explain them is a closed `<details>`.
**Change.** `scripts/sheets/approaches.py`, `legend_rows()` (line 1037) and the phone legend selection: add the rows the phone sheets actually use — Waypoint · stage, Zone · seed source (with the A/B/C glosses, or a three-line zones-of-confidence block above the legend), Fix · position, Station · profile repo, Proposed channel · unlit, Hatch · unsurveyed, Tints · under 5, 10, Height · commits, months, Sheet 1 · week's commits, days, Upright · measured, Underlined · above datum. Two columns at the current 34 px pitch is about +180 px; the phone sheet is already 1880 tall, so grow `SIZES["phone"]` rather than squeeze. Nothing new is said; the desk rows are reused.

### 2. Everything at the phone texture size is 8–9 CSS px — M
**Where.** `scripts/tokens.py:70` `FLOORS["phone"]["texture"] = 18`. On the sheets: every sounding on the phone Approaches (`43, 36, 27, 23, 19, 18, 15, 11, 10`), the hero's week figures and all subscript months, the footer's `7 5 3`, the legend's `12`. At 355 px (390 viewport) 18/720 is 8.9 CSS px; at 328 px (360 viewport) 8.2.
**Why it matters.** The unit of each chart sheet is a count ("depth is a count"), and on a phone every count is set smaller than any platform's minimum (iOS 11 pt, Android 12 sp, WCAG's working floor of about 12 px). The data layer becomes texture in the literal sense: present, not readable. Where those figures sit in tinted water at night they are also at 3.8:1 (ink2 on shallow_b). Pinch-zoom works on an SVG but the rubric says "reads on a phone", not "reads after a gesture".
**Change.** Raise the phone texture floor to 22 (10.8 CSS px at 390) or better 24 (11.8), and let the soundings thinning already written for the desk traverse (soundings.py "Traverse thinned, not shrunk") apply to the phone Approaches: print half the soundings at the larger size rather than all of them at 18. The hero's week figures (`358₁`, `17₁`, `0`) can be culled to HW alone on the phone, which also fixes the collision in finding 6.

### 3. The phone ship's log drops "computed from settings" — S
**Where.** `log-phone-360.png` sign-off row: "Log closed *1550* · unsigned". `scripts/sheets/log.py:321` builds it without the phrase that the desk sign-off (line 260) carries. The log lede that used to say it in Markdown was removed in v9.1, so on a phone the only remaining signal that the figures are not measured is the italic digits, which finding 1 shows no phone sheet explains.
**Why it matters.** This is the sheet DESIGN.md singles out ("the ship's log until a real run is recorded"); on a phone it is now the one place the honesty convention is silent. A screen-reader user hears "computed from settings" in the alt; a sighted phone reader never sees it.
**Change.** `log.py:321`: carry the phrase. The row is 600 px wide at machine 26 px (about 38 characters); "Log closed 1550 · computed from settings · unsigned" is 50. Either split the sign-off over two rows (the sheet has four 38 px rows; "remarks · nothing to report" is the least informative row on the sheet and can give way), or set the sign-off in the `label` role at 26 px condensed, which fits. Related: the two rows chosen for the phone (`remarks`, `beat`) carry nothing of the run; `1546 crawl complete · plateau · 12,440 urls · 1h 43m` is what a phone reader would want, if the column can be made to hold it.

### 4. Four alt texts describe the desk edition and are untrue of the phone edition they are read with — S
**Where.** `README.md`:
- soundings: "Below, one line per repository." — the phone sheet has no repository lines.
- approaches: "survey ground east, buoyed channel west" — the phone sheet is rotated; the ground is at the top, the harbour at the bottom, N points left. "every symbol in the legend" — not on the phone (finding 1).
- log: "10 entries" — the phone shows two.
- instruments: "dated by first commit. Bold: underway this quarter" — the phone has neither dates nor bold.
**Why it matters.** A `<picture>` has one alt for every `<source>`. A low-vision reader on a phone (zoom plus VoiceOver, the common case) hears one sheet and sees another. All six alts are within 25 words and plain, which is good; it is the edition-specific clauses that break.
**Change.** Either make the alt true of every edition by deleting the clauses above (the cheapest honest fix; alt is not visible copy, so the wording rule need not bind it), or make the phone sheets carry what the alt claims (dates and bold on instruments, more rows on the log, a full legend). Also "Types once; only the cursor keeps time" on the log and "A boat sails in and anchors" on the hero describe motion that the still and phone editions do not have; harmless, but the same class.

### 5. The "At a glance" table has an empty header row — S
**Where.** `README.md` `| | |` / `|---|---|`. Both renders show a blank strip above "Ben Russell builds" (`crit-mobile/glance-header.png`), and the DOM has two empty `<th>` cells.
**Why it matters.** This is the recruiter block, the plain-text answer to J10. A screen reader announces "table, 2 columns, 4 rows" and then reads cells with no column header; a sighted phone reader sees an empty box at the top of a 600 px tall table whose label column takes a third of 358 px, so "Ben Russell builds" wraps the field description to six lines.
**Change.** Put "At a glance" back in the first header cell (it was there last round; the brief still calls it that), or drop the table for three short paragraphs, each starting with the bold label as it is now (`**Ben Russell builds** crawl and data infrastructure: …`). The paragraph form reads better at 360 px and needs no header at all. Wording unchanged either way.

### 6. Hero phone: `265₅ 358₁` abut, and the lateral marks and anchor sit on the Scrapy Harbor figures — S
**Where.** `crit-mobile/hero-harbor-zoom.png` (day) and `hero-phone-night-360.png`: the height figure `265₅` and the week figure `358₁` are set side by side with about 6 px between them, at two sizes, with the can, nun and anchor glyphs drawn across the ring below. At night the two flare halos land on `358₁`.
**Why it matters.** Two different figure kinds (commits-months and week-commits-days) with no phone legend to tell them apart, touching, under three symbols: this is the one place the phone cover is illegible, and it is the cover's main feature. Commit `b37bffb` reserved label boxes for the desk; the phone needs the same.
**Change.** `scripts/sheets/hero.py` around line 648 (`week_boxes`) and 590: on the phone, let a height figure evict a week figure as a land name already does, or print only the HW week figure on the phone and place it off the feature ring. Reserve the lateral-mark glyph boxes on the phone as on the desk (the `if not phone:` at line 595 skips it).

### 7. The survey vessel is unnamed on the phone cover — S
**Where.** `hero-phone-360.png`: `87₆` at the channel mouth has no name; on the desk it is "rustmapper · PA 87₆". `hero.py:590`: `phone_named = {f.name for f in ranked[:4]}` names the four largest features by commits, and rustmapper is fifth.
**Why it matters.** J2. The page's argument is that rustmapper is the survey vessel; the phone hero names Game Engine I., Data Science Bank, Scrapy Harbor and Profile Shoal and leaves the vessel as an anonymous shoal. A phone reader meets "rustmapper" first as a link under the chart with nothing on the chart to attach it to.
**Change.** `hero.py:590`: `phone_named = {f.name for f in ranked[:4]} | {names of the two main projects from chart.toml}`; the `PA` doubt mark should come with it, since that is honest about where it is drawn.

### 8. Approaches phone: "429 Shoal" clipped, `R "4"` crossed, legend flush to the neatline — S
**Where.** `approaches-phone-360.png` / `-night`: the name reads "429 Shoa" against the right neatline (`approaches.py:719`, `anchor="middle"` at the shoal centre, which is 30 px from the rule); the leading line runs through the `R "4"` label (`crit-mobile/codeblock.png` top edge shows it); "SYMBOLS" and the left legend glyphs start at x=52 against a neatline at x=50, while the right column has a 12 px margin.
**Why it matters.** J8: a clipped place name on a chart is the thing a chart reader notices first; a label cut by a line is the second.
**Change.** `approaches.py:719`: `anchor="end"` at `sx + SHOAL_R*s` or clamp `sx` so the run stays inside the rule by 8 px; move the `R "4"` label to the left of its nun as the desk does; give the phone legend the same 16 px inset on the left as on the right.

### 9. The third command overflows the phone — S
**Where.** `README.md` fenced `sh` block, line `rustmapper export-sitemap --data-dir ./data --output sitemap.xml` (62 characters). In `readme-390.png` it widened the document to 633 CSS px (`crit-mobile/codeblock.png`); on GitHub the block scrolls sideways and `--output sitemap.xml` is hidden.
**Why it matters.** The only copy-and-run thing on the page is the one line that needs a sideways scroll on a phone, and a sideways-scrolling block inside a vertically scrolling page is the classic touch trap.
**Change.** Break it with a shell continuation: `rustmapper export-sitemap --data-dir ./data \` / `    --output sitemap.xml`. Code, not copy; nothing is reworded.

### 10. The link row wraps with an orphaned separator — S
**Where.** `crit-mobile/glance-header.png`: line 2 is "· How it's built". Each `&nbsp;·&nbsp;` is on its own source line, so the breakable space sits before the dot, not after it.
**Why it matters.** Small, but it is the first thing under the cover on every phone, and an orphaned dot reads as a bullet for a one-item list.
**Change.** `README.md` link `<p>`: write the separator as `&nbsp;·` followed by a normal space and the next `<a>` on the same line, so a break can only fall after the dot. Also consider whether five links at 16 px with 16 px gaps are the right phone targets; they are inline text and exempt from the 24 px rule, but "PyPI" is a 36 px wide target.

### 11. Phone Instruments: no dates, no "underway", no gloss on LEAD / LOG / LOOKOUT — M
**Where.** `instruments-phone-360.png` versus `instruments-day-870.png`. `instruments.py:203–226` prints the group code and the names only; the desk's "LEAD · LANGUAGES / LOG · STORES AND QUEUES / LOOKOUT · DECK" heads, the first-commit dates and the bold "underway this quarter" weight are all dropped. The `<sub>` line that used to carry the gloss under the sheet was removed in v9.1, so on a phone "LOG" appears a screen after a section called "Ship's log" and means something else.
**Why it matters.** J3 and J6: this is the one phone sheet with no silhouette and no data; the alt promises both. The separator convention also inverts between editions (sheet: "Parquet · Arrow, redb · WAL", where "·" joins; desk and table: "·" separates).
**Change.** `instruments.py` `_phone`: use the desk heads (`LEAD · LANGUAGES` etc.) as the row label, since the gloss is already desk wording; carry the bold weight for the underway fittings; if the dates fit, set the fittings as `name … Mon YYYY` in two columns at 26 px (18 rows at 30 px pitch is 540 px, so the sheet becomes 720 × 600, which is fine on a phone). Use one separator convention.

### 12. Soundings phone: a week labelled as a day, and no time axis — S
**Where.** `soundings-phone-360.png`: "HW 358 · 5 Oct", "LW 0 · 24 Aug" (`soundings.py:386, 391`) where the desk says "wk of 5 Oct" (line 246). The phone curve has no month initials under it; the only time anchor is "52 weeks to 7 Oct 2026".
**Why it matters.** 358 commits on one day is a different claim from 358 in a week, and the chart's whole stance is that figures are exact. Without a time axis the January spike is undated and the HW/LW labels are the only readable points on the curve.
**Change.** `soundings.py:386/391`: keep "wk of" on the phone (it is 5 characters). Add the month initials along the baseline at the 26 px label size: twelve letters at about 15 px each fit in 700 with room. Both are desk wording reused.

## Things that hold up and should not be touched

- The `<source>` order is correct (phone + reduced-motion + dark first, down to the day `<img>`), the non-hero phone editions are frozen so they need no reduced-motion variant, and the hero has its own phone stills.
- Phone night editions are designed: lights brightest, semantic text lifted to full ink, tints readable.
- The page order on a phone is right: cover, links, plain-text table, thesis paragraph, then the sheets in survey order; the legend arrives after the map as on a chart.
- Nothing relies on colour alone.
- "SMALL-SCALE EDITION" on the phone hero is the honest move the other five phone sheets should copy in spirit: say what was left off (findings 1, 3, 11) or carry it.
