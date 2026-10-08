# Crit 28 — Advertising art director (print and campaign)

I judge posters: does the hero stop you in half a second, does one image plus one line carry the idea, is every other sheet an execution of it. Looked at hero-day-2x, hero-night-2x, page-day-top and page-night-top at README scale, the name and cartouche crops, and spec-hero.md.

## 1. What is good

- **There is a stopping element.** "Ben Russell" at 176 Instrument Serif on a bathymetric field is the one thing a stranger's eye cannot pass: 120px tall at 870, 49px at 360, first read at both. Most developer pages have no first read.
- **The three-register system in the spec is right and rare.** Headline carries the metaphor ("I survey a web that is wrong about itself"), cartouche the literal ("Full-stack developer · mostly crawlers, lately in Rust"), README the detail. Line, tag, body. Keep it on every sheet.
- **Night is a real second poster, not an inversion.** Ink recedes, shoals read as blueprint, the accent becomes a light instead of a paint colour. Lights brightest at night, structures carry the day: same layout, different protagonist.
- **Small decisions a reader feels without naming**: the italic's 8px optical indent, the chart number outside the neat line. More of those, fewer features.

## 2. What is bad, ranked

1. **The hero fails the one-image-one-line test.** Cover the name: the picture is a chart with a beige blob and a compass. The current line describes a job; the picture shows a decorative field; neither needs the other. The new line fixes half of it ("wrong about itself" has a turn). The picture still shows nothing wrong. A headline that alleges an error over an immaculate image is a claim without evidence in frame.
2. **Read order in the first half-second is name → beige blob → red needle → thesis.** The thesis is fourth. In page-day-top the 100px red needle at the name's own height is the second-loudest object. The spec's 10px arrowhead and .10/.18 tints fix most of this; the thesis must be the second read or the line never lands.
3. **Two focal points is a committee.** Name top-left, rose top-right, same height, same weight. The spec keeps the rose at r 80 with twelve numerals and a 24-bar ring: still a second headline. A poster has one hero; the rose is cast.
4. **Craft tells that say "computer".** Soundings on a visible ~40px lattice at one size and opacity; identical waypoint glyphs; metronomic dashes; minute bars that never miss. Perfect evenness reads as fill even to people who cannot say why. No decision, no author. (Line weights and grain: see the printmaker.)
5. **A production bug.** "SCALE OF DISCOVERED URLS · NOT FOR NAVIGATION" runs out of the cartouche and over the chart (x ≈ 905–1025). A client pulls the proof for this alone.
6. **The big idea is in the margin, and the margin is too thin.** The survey edge is the thesis made visible, and the spec gives it x 1150→1280: 10% of the width, 36px on a phone.
7. **Over-design in the spec.** Nine cartouche lines, source diagram with key, stray A/B/C letters on the chart, two pencil notes, three sounding classes, a two-line VAR note, numerals every 30°. A poster is one thing you cannot stop looking at and five things you find later. Stray letters at 68% read as typos.

## 3. What needs to be done

- **Put the evidence in the picture.** Draw Rustmapper Shoal twice: the reported coastline dotted and labelled "as charted (sitemap)", the surveyed coastline solid, offset 20–30px, captioned only by the pencil note "sitemap.xml lies again — see Notice 3". Real chart grammar (reported vs surveyed, PA/ED), no invented numbers, and the image says what the line says.
- **Widen the unsurveyed band to x 1080→1280** (15%) and make it the only pattern fill on the sheet; let one contour and the seaward waypoint cross into it. Eye path: name, line, edge.
- **Demote the rose.** Keep both rings and the commit clock (that is a story); numerals become ticks plus "N" at .6; no red beyond the arrowhead. Maximum three accent objects on the sheet (arrowhead, nun, sail), none within 120px of the name's baseline.
- **Add decision to the evenness.** Soundings dense within 60px of the course, sparse in open water (surveyors sound where the ship went, which is also the story); two numeral sizes (11, 13); waypoint glyphs by kind (fix, DR, anchorage); seeded dash phase. Hand-kern the name: tighten "Ru", open "ss" a hair, check "ll" at 176.
- **Cut from the spec**: A/B/C letters on the chart (inset only), one pencil note, one VAR line, region and notice merged into the edition line. Rule: anything at 13px occurring more than twice is texture; set it at .5 or remove it.
- **Fix the overrun** and assert in the build that cartouche text stays inside the inner rule. Confirm the thesis is one line in every edition.

## 4. Improvements and high-level ideas

1. **The series lock-up.** "CHART NO. N · SHEET k" in the same position outside the neat line on every sheet is the campaign device. Extend it off the profile: a one-line header strip at the top of the rustmapper and Scrapy READMEs ("Chart No. 21 · Sheet 3 · Approaches"), built by the same script.
2. **Social previews as sheets.** Generate the two flagship repos' social-preview images (1280×640) from chartlib with the same chrome and number, so every unfurl on Slack or X is a page from the same atlas. Buildable, honest, the most-seen surface after the profile.
3. **Night is the true edition.** The hour histogram is real: he works at 21h. Give the night cartouche one line the day edition lacks, "SURVEYED AFTER DARK · VAR 21h00". Day is the chart, night is the chart being made.
4. **Bold: the name goes over the edge.** Let the final "ll" of "Russell" sit in the unsurveyed band, half-hatched: the surveyor is himself off the chart. It wins or embarrasses; test at 360px and drop it if it fights the thesis read.
5. **Bold: make the poster a poster.** Export Sheet 1 as an A2 PDF in the repo and link it in the colophon ("Sheet 1, for the wall"). If it does not hold at A2 with no README under it, the hero is not finished.

## 5. What the page says about its maker

Now: a developer with unusual taste who found a strong aesthetic and let the generator fill the sheet; a great first read that the rest of the page explains rather than extends. It should say: someone who knows the difference between a picture and an idea, whose one idea (the web is wrong about itself; he surveys the edge) is stated in a line, proven in an image, and executed in six sheets that each do one job in the same hand. The confidence to cut is what months of team work look like on a poster: nobody sees the forty things removed, everybody feels the one left.

## Five most important lines

1. The hero must pass "cover the name, read the picture": draw Rustmapper Shoal twice, as charted (dotted, sitemap) and as surveyed (solid, offset), captioned only by the Notice 3 pencil note, so the image proves what the line alleges.
2. Read order must be name → thesis → edge; today it is name → blob → red needle → thesis. Tints .10/.18, rose to ticks + N with a 10px arrowhead, no red within 120px of the name's baseline, three accent objects maximum.
3. Widen the UNSURVEYED band to x 1080→1280 and make it the only pattern fill; the big idea cannot be the smallest thing on the sheet.
4. Cut the spec (no A/B/C on the chart, one pencil note, one VAR line, merged region/notice line; 13px text recurring more than twice is texture or gone) and fix the cartouche caption overrun with a build assertion.
5. Campaign: the "CHART NO. N · SHEET k" lock-up goes on every sheet and extends to the flagship repos' README headers and social-preview images from the same scripts, so every surface his work appears on is a page from one atlas.
