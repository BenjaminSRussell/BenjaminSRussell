# Crit 01 — Editorial / brand designer

Reviewed: page-day-full, page-night-full, hero (day/night 2x), approach-scrapy (day), survey-rustmapper (night), log (day), soundings (night), legend (night), footer (night); DESIGN.md, README.md, build_assets.py sizes.

## 1. First impression

This is the first version with a real idea, and the hero earns its stage: the 176px Instrument Serif against a bathymetric field is a genuine image, not a header. Below the hero, though, the page decays into a sequence of landscape "cards with a nautical skin", and by Sheet 6 the chart has become a four-column tech-stack table with anchor icons. A top studio would ship the hero and the footer as they are and send Sheets 2–6 back as a first draft.

## 2. What works

- The hero. Type scale (176 / 34 / 11), the negative tracking on the serif, and the cartouche are correct and confident. Islands named for projects and "Scale of discovered URLs · not for navigation" are exactly the kind of line that says more than it says.
- One ink, one paper, two signal colours. The palette discipline is real and the day/night editions hold up; night is actually the stronger edition because the hatching reads as blueprint.
- The footer concept (the boat, the waterfall, "Here be dragons") closes the arc with the avatar's own joke.
- Copy voice is consistent and literate ("Pages drift, encodings shoal"). Much of the "depth" the owner wants is already in the writing; the design isn't yet matching it.

## 3. Problems, ranked by impact

1. **No editorial arc after the opening.** Hero = overture. Then: a stats strip, two near-identical project cards, a terminal, a table, a thin footer. Every sheet is 1280 wide, every one has a title top-left and a mono caption top-right, every one is a double-ruled rectangle. Rhythm is metronomic. There is no climax; the richest sheet (hero) is the first thing you see and nothing afterward asks you to lean in. The full-page render reads as "one great image + a GitHub README."

2. **Approach and Survey are the same sheet twice.** Both: 96px serif title at (44,152), an italic deck, three lines of dot-separated mono, a row of pill chips, a 50/50 split with a chart on the right. The two projects are different in kind (platform vs. engine) and the design should be as well. Also the Scrapy harbour's actual map sits in a 50% column with the typography piled on the left: the title block is doing all the work and the chart is decoration.

3. **Caption type does not survive the medium.** Caps mono at 9–11px, tracked +1.8, rendered at 68% in the README column becomes ~7px; on a phone ~3px. The entire system of sheet numbers, bearings, "SURVEYED 2024 – 2026", "GRAFANA LT · FL(3) 10S", legend headers, the log's TIME/ENTRY heads, and all footer copy is set at this size. At production scale most of the detail you built is illegible, which means the "layers of depth" are invisible unless someone opens the SVG. The soundings numbers are fine as texture, but anything that carries meaning needs a floor of 13–14px at 1280.

4. **Soundings (Sheet 2) is half empty.** The right 35% is a dashed placeholder and a caption "TIDE TABLE ARRIVES WITH THE FIRST REFRESH". Shipping an empty state on the second most prominent sheet is a first-draft tell. The five figures are also set in Instrument Serif at display size with nothing to contrast them: "Oct 2024" at the same weight and size as "1,828" flattens the hierarchy (one of these is a headline number; the others are footnotes).

5. **Legend (Sheet 6) is a template.** Four columns, bullets replaced by anchor/square/buoy/star glyphs, bold first row. The icons are decorative: the anchor on "Python" and the anchor on "SQL" mean nothing different. On a real chart the legend explains marks used *elsewhere on the chart*. Here the marks appear only in the legend. A design director will stop here and think "skills section with a costume."

6. **The log is 40% blank rows.** Rules with nothing on them in a still image read as unfinished, not as "typing live". The one italic aside bottom-right ("Wind light, visibility good. Nothing on fire.") is the best line on the sheet and it is set at the smallest contrast.

7. **Pill chips (Approach, Survey) are the one UI element that breaks the metaphor.** Rounded 1px bordered chips are the universal README tech-badge; they drag both sheets straight back to v7. A chart has no chips.

8. **Mono body in the sheets is set as plain centered-ish text lines** ("Scout spider · JS-heavy page detection · adaptive rate limits"), three lines of equal visual weight. It's a bullet list with the bullets removed. Measure is ~80 characters, leading is loose, and nothing is emphasized.

9. **Micro.** Hero: the compass sits exactly between "Rustmapper Shoal" and the right margin and competes with the title's right edge; "Scale of discovered URLs · not for navigation" collides with soundings ("...NAVIGATION" over a 20). Footer: 200px tall with ~60% empty paper; the waterfall is 6 dots. Soundings: legend swatches for the language bar are tiny unlabelled squares. Night ink `#DCE4F0` on `#0F1A2B` at 176px is fine but at 11px tracked caps it blooms.

## 4. What "months of team work" would look like (testable)

- A storyboard: each sheet has a *different* job and a *different* composition (full-bleed map, dense data page, near-empty page, typographic page). Test: cover the titles; can you tell the sheets apart by silhouette alone?
- A type spec with three sizes that survive 68% and 28% scaling. Test: screenshot the profile on a 360px phone; every word in a sheet that is not pure texture is readable.
- The chart metaphor applied *structurally*, not as skin: the legend explains marks that actually appear on the hero and approaches; the soundings on the hero correspond to something (commits per week, repo sizes); a bearing or depth that appears twice means the same thing both times. Test: pick any symbol; can you point to where it is defined and where it is used?
- No empty states in a still. Test: every render from the build is shippable as a poster.
- One climax sheet that a reader would screenshot and post.

## 5. Proposals (ranked, buildable with SMIL/outlines/<300KB)

1. **Make Sheet 2 a real tide table of commits (meaning layer).** Replace the stats strip with a 52-week tide curve drawn as a proper tide graph: weekly commit counts as a smooth bathymetric line, high-water / low-water marks labelled with the actual week ("HW 2026-03: 212 commits"), the five figures shrunk to a sidebar in 14px mono. Honest data, already fetched by build_stats. The empty placeholder disappears; the curve fills in with SMIL.

2. **Merge Approach and Survey into one tall "Approaches" sheet, 1280×900, map-first (arc + meaning).** One continuous chart: open water on the left where rustmapper's survey fan takes soundings, a buoyed channel leading into Scrapy Harbour on the right. The two projects become geography of the *same* pipeline (discovery → crawl → storage → dashboards), which is literally how they relate. Titles become place-names set in the chart, not headers; the README text below carries the bullet detail. This is the climax sheet.

3. **Make the legend true (meaning).** Symbols in the legend must appear on the chart: red cans = infra you operate (Postgres, Redis, Docker), green cones = things you ship (PyPI, CLI), the lighthouse = observability (Grafana), anchorage = storage (Delta Lake), survey lines = languages. Then the legend can be a small panel on the merged Approaches sheet or a narrow 1280×220 strip, and reading it changes how you read the hero. Drop the four-column stack table; the stack is listed in the README text anyway.

4. **Kill the chips; set the fact lines as chart notes.** Replace pill rows with a cartouche-style block: "NOTES: 1. Python 3.11 … 2. Delta Lake raw …", numbered, 13px mono, left-aligned, ruled. Same information, no README badge smell, and it rhymes with the hero cartouche.

5. **Type floor and hierarchy.** Captions 13px / tracking +1.2 for anything semantic; keep 9–11px only for soundings texture. Give the soundings figures a scale: one hero figure (commits) at 110px, the rest at 46px. Italic asides at 24px minimum. Headers at the top of the secondary sheets drop to 64px; 96px on a 420px-tall card is shouting.

6. **Delight: the log should be the full log.** Fill all rows; the last entries become the easter eggs: "14:11 sitemap.xml exported · 48,213 urls", "14:12 ⚓ anchored". Make the still state the *finished* log and animate the typing from the start when loaded. Add a hairline "page 27 of —" in the corner.

7. **Delight: the footer boat should actually reach the edge.** Over 70s the boat sails toward the fall; at the last 2s the sail tips over the drop and resets — the one joke the avatar sets up and the page currently refuses to pay off. Also make the footer 320px tall and put the colophon's "Off the clock" aside *inside* the sheet in italic so the last thing read is on paper, not in Markdown.

8. **Second-look layer on the hero:** replace a handful of random soundings with real figures that reward noticing (24 repos, 46 followers, 512, 256, 0.1.3) and mark one with a tiny asterisk in the cartouche: "Some soundings are true." Costs nothing, and it's the sort of thing people screenshot.

9. **Pagination and rhythm.** Vary sheet heights deliberately (900 / 268 / 440 / 220 / 320) and add a hairline running sheet number + "Chart No. 27" in the same corner of every sheet, so the page reads as a bound atlas rather than six images.

## 6. What it says now vs. what it should say

Now: "A developer with real taste who found a strong concept, executed the first image beautifully, then ran out of time and skinned a standard README in the same palette." The hero says *designer*; Sheets 2–6 say *template with a theme*. The intensity of attention is uneven, which is the opposite of the "years of workshopping" brief.

Should say: "Someone who treats a profile the way he treats a crawler: the surface is part of the system." That requires every sheet to carry one idea that is structurally true about the work, legible at phone size, and set with the same confidence as the hero. The concept is good enough to get there; the remaining work is subtraction (chips, the stack table, empty states) and one act of consolidation (the merged Approaches chart).
