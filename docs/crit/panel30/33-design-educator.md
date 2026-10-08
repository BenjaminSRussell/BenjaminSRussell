# 33 — Design educator (typography and visual communication; I grade crits)

I teach fundamentals and grade them. I looked at every render (page day/night full and top, hero day/night 2x, approach-scrapy, survey-rustmapper, log, soundings, legend, footer), then README.draft, STANDARDS, CHANGELIST and the three specs, to grade the current state and check the direction against the principles.

## Grades, sheet by principle

Hierarchy · Alignment · Proximity · Contrast · Repetition · White space · Figure/ground · Grid (and its violations).

| Sheet | Hier | Align | Prox | Contr | Rep | Space | Fig/gnd | Grid | Sheet |
|---|---|---|---|---|---|---|---|---|---|
| Hero | A | A- | B- | B+ | A- | B+ | A | A- | **A-** |
| Soundings | C | B | B- | C+ | B | D | B | C | **C+** |
| Approach (Scrapy) | B | B+ | B- | B | B- | B | B | C+ | **B-** |
| Survey (rustmapper) | B- | B | C | B | C | B- | B- | C+ | **B-** |
| Log | B+ | A- | B+ | B | A | C | A- | A- | **B+** |
| Legend | C+ | A- | B | C | B | B | B | A- | **C+** |
| Footer | B | B | B | C+ | B | B+ | C+ | B | **B-** |

- **Hero.** One left axis (eyebrow, name, deck, cartouche text) carries the sheet; the type sits *on* the chart with a cleared halo and both read. Proximity fails where "SCALE OF DISCOVERED URLS · NOT FOR NAVIGATION" escapes its cartouche and overprints the border and a sounding; the rose ring cuts Rustmapper Shoal and its "S" bumps "Delta Lake". Contrast is size and slant only: no weight, and one 11px mono for eyebrow, bearings and soundings alike.
- **Soundings.** Five figures, one size; "Oct 2024" is widest so it wins, though 1,828 is the headline. Column rules fall where numerals end, so gutters are unequal: content set the grid. The right 35% is not white space, it is absence with a caption.
- **Approach.** Four tiers on the left (96 / 34 / 13 / chips), none on the right, where URLS, OPEN WATER and BREAKER CLOSED share one style. Three subsystems set as three equally spaced lines, so the grouping is invisible. The pink sector wedge is the largest colour field on the page and means nothing yet. Text column and graticule share no module.
- **Survey.** Same template as Approach, so repetition becomes sameness. Two focal points fight (96px title, 96px "512"). Soundings pile up where the fan converges (56/56/57/55 overlap at the vessel): geometry turned proximity into collision.
- **Log.** Best grid on the page: tabular columns, ruled rows, semantic colour. Forty percent empty rows in a still, and the best sentence at the lowest contrast, inside a table row it does not belong to.
- **Legend.** Perfect four-column alignment of a list with no hierarchy; bold first row is the whole idea; icons repeat without meaning.
- **Footer.** The one sheet that uses emptiness as content, then under-commits: six dots for a drop, half the sheet empty water, caption at an arbitrary height.

Page level: every sheet is the same rounded double-rule box, so the page reads as seven cards. Each thing is titled three times (Markdown H2, sheet title, sheet eyebrow). Sheet text is indented ~25px rendered inside the prose column: nested boxes. The snake is a borrowed widget in borrowed colours (deletion is correct).

## The most common student mistake here

**One style for all small type.** Eyebrow, bearing, legend header, column head, status label, sign-off: all 11px tracked caps mono. The student builds two tiers, display and caption, and asks the caption tier to do eight jobs. When everything is secondary, nothing is. It is also why the scale has a hole between 34 and 176 and why night blooms: the system was set at display size and copied down. The fix is roles, not more sizes: three named small styles (label, note, texture), each with a size, a slant rule and a place.

## The most advanced move

The hero's figure/ground: 176px high-contrast serif directly over a dense contour field, a halo cleared rather than a box drawn, the letter hairlines in conversation with the contour weight. Most students would panel the name. Not panelling it makes the sheet an image rather than a header, and the Approaches spec's "titles are place names set in the chart" is that same move applied where it is needed.

## What needs to be done

1. **Role-based small type.** Label 13 upright (marks, heads), Note 13–14 italic or rotated (marginalia), Texture 11 (soundings only). Build fails on any 11px string that is not a sounding.
2. **Captions stay inside containers.** Scale caption inside the cartouche or the cartouche widens; rose exclusion includes ring and cardinal letters; cull soundings within 28px of each other and within the fan's first 120px.
3. **Status beside its light.** BREAKER CLOSED belongs at the sector light, not loose in a corner (its position even differs between the 2x and page renders).
4. **One grid per sheet.** Make the Approaches graticule module (1280/16 = 80px) the measure of the text column, so cartouches sit on graticule lines.
5. **Group by spacing.** 1.5× leading between subsystem groups, 1× within, or numbered notes as specified. Equal columns on Soundings, or no rules.
6. **Vary the frame.** Neat line with minute bars on the hero only; thin rule on Approaches; none on log and instruments; footer bleeds. The page stops being cards without new drawing.
7. **Title once.** The H2 names the section; the sheet eyebrow becomes a folio ("Chart 24 · Sheet 3") and nothing more.

## Three exercises, A- to the piece that gets someone hired

1. **Silhouette thumbnails.** All six sheets at 10% as grey masses: type, map, empty. No two alike; at most one top-left title. Pass: a stranger covers the titles and still names every sheet.
2. **Phone first.** Design the 360px hero and Approaches before touching 1280: 18px floor, twelve soundings, one light, one shoal; then scale up, adding texture as room appears. Pass: printed 90mm wide, every semantic word readable at arm's length. Hierarchies designed small survive enlargement; the reverse never does.
3. **Subtraction with a ledger.** Remove 30% of the hero's marks without losing information, writing each deletion and why it was safe (soundings that duplicate contours, the fourth dash pattern). Add back one thing: a running marginalia system (folio, catchline, "corrected through") identical on every sheet. Pass: fewer marks, more reading.

## Improvements and ideas

- **Bold: a spread, not a stack.** Treat the page as a bound atlas: hero as cover, Approaches as the double-page spread (tall, bleeding to the column edge, unframed), everything else a plate with a folio. Wide–short–tall–medium–strip–edge is a composition; the current even stack is a list.
- **Weight as edition.** Day and night should differ by a decision, not an inversion: Plex Light at night (type designer) plus no graticule at night, so night is lights and ink on dark water.
- **One sentence per sheet.** Write what each sheet does that no other does ("the log is the only place the machine speaks"). Two matching sentences means merge. Approaches passed; Legend did not, and folding it in is right.

## The "months of work" ambition, honestly

Months of team work looks calmer, not fuller. Real depth is few decisions that interlock and survive scaling: the same slant meaning the same thing everywhere; a legend explaining marks actually drawn; a compass that is data; a frame that varies for a reason. More stuff is extra sheets, easter eggs and loops. STANDARDS is right about the interlocks and at risk on the trinkets: four uncaptioned layers plus a serpent is a quota, and quotas produce ornament. Keep each layer that makes the first reading truer when found (true soundings, the variation note); drop any that is only a wink. The hiring test is simple: a reviewer points at any mark, the maker says in one sentence what it is for, and the mark still reads on a phone.

## What the page says now, and what it should say

Now: a maker with a real eye and one great image, who set the type system at display size and let the rest inherit it; who knows the fundamentals well enough to break the grid on purpose on the hero and then forgot to build one below it. It should say: someone who treats hierarchy as roles, proximity as meaning and the frame as a decision; whose small type was designed before the large; who removed more than he added. That is what "workshopped for years" looks like, and the hero proves he can do it.

## Five most important lines

1. The systemic fault is one small-type style doing eight jobs (11px tracked caps mono for eyebrow, bearing, legend head, status, sign-off); define three named roles (label 13 upright, note 13–14 italic/rotated, texture 11 soundings-only) and fail the build on any other 11px string.
2. Proximity bugs are collisions, not taste: the hero scale caption escapes its cartouche and overprints a sounding, the rose ring cuts Rustmapper Shoal, survey soundings pile up at the fan origin, BREAKER CLOSED floats away from its light; add exclusion boxes that include rings and letters, cull soundings under 28px apart, pin status to its mark.
3. Vary the frame (minute bars on hero only, thin rule on Approaches, none on log/instruments, footer bleeds) and title each thing once (H2 names it, eyebrow becomes a folio); this alone stops the page reading as seven identical cards.
4. Run three exercises before the rebuild ships: silhouette thumbnails at 10% (no two alike), phone-first design of hero and Approaches at 360px then scale up, and a 30% subtraction pass with a written ledger plus one shared marginalia system.
5. Months of work looks calmer, not fuller: keep second-look layers that make the first reading truer, drop any that is only a wink, and judge the piece by whether every mark can be justified in one sentence and still read on a phone.
