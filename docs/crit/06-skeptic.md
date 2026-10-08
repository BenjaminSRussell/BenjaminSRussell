# 06 — The skeptic. Tells, costume, and what a thesis would look like.

## 1. First impression

Handsome, competent, and I knew exactly how the page would end before I scrolled: about, stats, two projects, principles, stack, the rest, contact. The nautical idea is applied with a roller, evenly, to every surface, which is how you can tell it took hours and not months; months leave fingerprints, exceptions and one joke that pays off late. It is a very well-dressed template, and it is still a template.

## 2. What works

Instrument Serif at display size is the right call and "Ben Russell" against the contours is a genuinely good first second. The two-edition build (day/night via `<picture>`, red that goes orange at night) is real craft. The hero scale bar in URLs and "Surveyed 2024 – 2026" are the two places where the metaphor says something true instead of decorating. The Scrapy channel (pipeline stages as buoys) is the one sheet where the concept and the content are the same object. The prose is above the GitHub median and the honesty constraint is taken seriously.

## 3. Problems, ranked by how badly they hurt

1. **The snake.** The single most generic widget on GitHub, dropped into the middle of a "one of a kind" chart, with a caption trying to costume it ("eaten nightly"). It undoes the entire premise in one scroll.

2. **Seven sheets, one chrome.** Double rule, tracked-caps eyebrow "SHEET N · X · Y" top-right, italic serif subtitle, mono spec lines, a row of pill chips. Hero, approach, survey, log, soundings, legend all carry the same furniture at the same weight. Real chart series have insets, source diagrams, folded panels, a different paper for the pilot book. Here it is a component library. Procedural uniformity is the loudest tell on the page.

3. **The pill chips.** `Python 3.11` `Scrapy` `Delta Lake` in rounded boxes are a 2023 web UI pattern. There is no such thing on a chart. They flatten the costume into a Tailwind card.

4. **Depth means nothing.** The soundings are random numbers on a jittered grid. A chart's whole authority is that every digit was measured. "Depths in trusted rows" is claimed on the title block and then nothing on the sheet is a trusted row. The same goes for the islands: why is rustmapper a *shoal* (a hazard)? Why is Delta Lake a tiny island on a sea chart? Why does the course visit none of them? Names were assigned, not derived.

5. **Apologising eyebrows.** "NUMBERS ILLUSTRATIVE, THE PACKAGE IS REAL." "SEEDED, FIRST REFRESH PENDING." "TIDE TABLE ARRIVES WITH THE FIRST REFRESH." "NOT FOR NAVIGATION" (which also collides with Common Crawl Bank). You are shipping placeholders and disclaimers inside the artwork.

6. **Clichés doing the emotional work.** "Here be dragons." "Nothing on fire." "Fair winds." "Thanks for reading this far." "I'm told that's a mood." These are the first five things anyone writes when handed the word *nautical*. The footer, which should be the payoff, is three clichés and a dribble of dots.

7. **Explaining the trick.** "This page is drawn, not templated" appears twice; the colophon narrates the compass pointing to the accent and the marching squares. Confident work does not annotate its own cleverness. The reader should discover the compass; you told them.

8. **The log is a terminal in a hat.** Timestamps, `$` prompts, a progress bar, checkmarks, four empty ruled lines. A ship's log has position, weather, bearing, remarks, a signature. This is the sheet where the metaphor could *generate* content, and it only decorates.

9. **The legend explains nothing on the chart.** It is a stack list with four bullet glyphs. The actual symbols on the hero (crosshair waypoints, cans, cones, hatch, bearings) are never defined. A legend that is really a "skills" section is the template showing through.

10. **Type lives at exactly three sizes.** 180px display, 36px italic, 11px tracked mono. No middle. No small serif numerals, no italic/upright distinction, no rotation, nothing that follows a contour. The chart idiom is *rich* in typographic rules and you used none of them.

11. **Nothing hand-made, nothing broken on purpose.** Every stroke is 1px, every contour is a smooth Bézier, every island is a blob, every grid is even. There is no marginalia, no correction, no asymmetry, no element that bleeds the frame.

12. **Small-screen death.** At 360px the soundings numerals and eyebrows are ~4px. The phone reader gets a navy rectangle with a name on it.

13. **Minor:** "harbour" on the sheet, "harbor" in the prose; "Chart No. 27" is arbitrary; the lighthouse beam is a clip-art pink wedge.

## 4. What "months of a team" would look like here, concretely

- **A thesis the whole page argues**, not a costume. The latent one is sitting right there in the copy: *the web is wrong about itself; I chart what is off the chart* (CT logs and Common Crawl find the subdomains nobody links to). The waterfall is the edge of the surveyed world. Today the waterfall is a footer gag.
- **A system with rules AND exceptions.** Testable: name three rules a reader could infer unaided (e.g. red = failure mode, green = guarantee, italic numeral = illustrative) and one place the system deliberately breaks them and why.
- **Data-derived form.** Testable: change a number in `build_stats.py` and the chart visibly changes shape. Today only five digits and a bar change.
- **A recurring idea that transforms**: the same boat, course or edge appears on every sheet in a different role, and the last appearance recontextualises the first.
- **One joke that pays off on the third sheet**, not five that land on contact.
- **Zero placeholders, zero disclaimers in the artwork.** Honesty expressed as a *convention* (a legend entry), never as an apology.
- **A phone edition** or a composition that survives 360px.

## 5. Proposals, ranked

1. **Delete the snake.** Replace with nothing. If you need contribution motion, finish the tide curve in Soundings and let it be the only live graph. (Immediate.)

2. **Honesty as a chart convention, not a disclaimer.** Real charts set drying heights and doubtful soundings differently. Rule: *upright numerals are measured, italic numerals are illustrative.* Put it in the Legend, drop every "numbers illustrative" eyebrow, and set the log's `48,213` and the hero's open-water soundings in italic. Says more than it says; buildable in svgkit today.

3. **Make the islands the portfolio and depth real.** Every public repo is an island whose area is its commit count (from the same Actions job that fetches stats), named, the 24 of them forming an archipelago; soundings around each island are stars/forks/age. "Other waters" becomes literal: the small islets. Now the hero *is* the data, redraws itself nightly, and "depths in trusted rows" becomes true.

4. **The edge of the chart as the structural idea.** Every sheet's right edge is where the survey stops: hatched "unsurveyed" ground, soundings thinning to nothing, the neatline broken. The footer is where the water finally goes over. In the rustmapper sheet, the survey fan is what *pushes the edge back*: label the three seed sources at the fan tips with the sources that find the unlinked web. The idea recurs on every sheet and transforms at the end.

5. **Break the chrome.** Hero: full neatline. Approaches: *insets* (chart-within-chart, offset, with a source diagram corner). Legend: fold it into the hero's title block or run it as a narrow panel at 60% width, right-aligned. Log: a different paper stock (ruled, warmer cream, no neatline). Soundings: a tide-table strip, short and wide. Vary widths; let one sheet be taller than wide.

6. **Rewrite the log as a log.** Columns: TIME · POSITION (a URL count, honest) · WIND (requests/s, illustrative in italic) · REMARKS. Entries in chart voice drawn from the real CLI. Sign it. Drop the checkmarks and progress bar. Cut "nothing on fire."

7. **Marginalia in a third register** (delight on second look). Small Instrument Serif italic, slightly rotated, as pencilled corrections: "sitemap.xml wrong about itself again, see Notice 3" pointing at a shoal. Two or three per page, never more. Tie them to *Notes to mariners*, so the five rules are found on the chart before they are read as a list.

8. **Compass variation as a running gag** (second-look delight). Replace the stock rose annotation with "VAR: see colophon". In the colophon, one line: the rose points at the accent colour because that is the only fixed thing on the chart. Tell it once, at the end, as a reward, and delete every other self-explanation.

9. **Chart number that means something.** Chart No. = current public repo count, updated by Actions. Edition = latest `rustmapper` version, with date. Now the eyebrow is data.

10. **Replace pill chips** with a chart-style "Instruments" table in the title block: two columns of mono, no boxes, the daily driver set in bold.

11. **Kill list.** "Here be dragons", "Fair winds", "Thanks for reading this far", "I'm told that's a mood", "drawn, not templated" (both), the pink beam wedge (use ruled light sectors), the empty tide panel until it has data.

12. **Phone edition.** A `<picture>` `media="(max-width: 600px)"` source per sheet, generated from the same engine at 720px wide with soundings culled and type scaled. Or stack the hero into two sheets on phones.

## 6. What it says about its maker, vs what it should

**Now:** a careful, tasteful developer who found a metaphor, applied it uniformly, labelled everything, apologised where unsure, and explained the tricks in case nobody noticed. Thorough, pleasant, slightly anxious, interchangeable with the next tasteful nautical profile.

**Should:** someone with a *position* about the web (it lies about itself, and he surveys the parts that are off the chart), who builds systems with rules he can state and exceptions he can justify, who trusts the reader enough to leave the compass unexplained and the joke unlabelled, and whose chart gets a little more accurate every night because it is drawn from the same data he spends his days collecting.
