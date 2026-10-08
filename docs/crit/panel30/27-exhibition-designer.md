# 27 — Museum exhibition designer

I plan galleries: the walk, the hang, wall-text hierarchy, where the showstopper sits and what the exit does to the entrance. I read the page as a gallery: page-day-full / page-night-full for the walk, the 2x sheets as objects, README.draft.md as wall text, spec-*.md for the planned hang (740 / 240 / 880 / 440 / 230 / 270).

## What is good

- **The entrance works.** The hero is a proper threshold piece: one object, a name at 176px, one italic promise, a course leaving the frame to the right. A visitor who stops at the first wall leaves with the premise. The link row beneath is wayfinding signage, not a label; correct.
- **The sheets are one collection.** Same paper, neat-line and two typefaces: nobody doubts the objects belong together. That is the hardest thing in a group hang and it is done.
- **The planned hang varies height.** Current renders are 640 / 268 / 420 / 420 / 440 / 317 / 253: three objects within 20px of each other at near-equal intervals. The spec's tall / strip / tallest / medium / strip / strip is a real rhythm. Keep it.
- **The log is a different paper.** The one object that is not a framed chart; the room needs exactly one. The draft's alt text for it is a true object label: what it is before what to think.

## What is bad, ranked

1. **The second half of the gallery is empty wall.** Measured on page-day-full: objects occupy ~36% of the scroll, and from y≈3400 to the end (~2,000px, 38% of the walk) there is no object except the snake (being removed) and a 150px footer. The visitor leaves the last room through a corridor of reading (Other waters, Colophon, Off the clock) and meets an exit the size of a fire-door sign. The draft helps (Instruments after Notices, shelf folded) but still has ~1,200px of text before a 270px exit. This is the room people walk through with their coat on.
2. **Every label repeats its object.** Scrapy sheet: three mono lines of features plus nine chips. Markdown under it: a bold lead and four bullets with the same features. Alt text: a third pass. The spec keeps three layers (cartouche NOTES 1–5, bullets, alt). Museum rule: the label never describes what the visitor can see; it supplies what the object cannot show. The sheet carries drawable facts (marks, numbers, names); the markdown carries only the undrawable (purpose, link, date, one line of judgement).
3. **Equal hang, equal frame, equal width.** Even with varied heights, every object is full column width, same cream frame, same corner radius, serif title top-left, mono eyebrow top-right (approach-scrapy and survey-rustmapper share one silhouette). Everything the same width in the same frame reads as a catalogue, not a show. GitHub allows `align="right"` and `width` on `<img>`: at least one object must hang smaller and off-axis.
4. **Two showstoppers compete.** The spec'd hero (archipelago, rose, cartouche, 34 soundings, course, buoys, pencil notes, source diagram) will match the Approaches sheet it calls the climax. A show has one hook at the door and one showstopper deep in the walk; they are not the same piece. If the hero shows everything, the 880px room is a repeat.
5. **Lighting logic differs between editions.** Day: cream object on a white wall, visible paper edge, a mounted sheet. Night: navy on GitHub's near-navy, edge almost gone, a chart printed on the wall. A museum fixes the mounting and changes only the light. And at night the brightest thing on the hero is 176px of white type; the spec wants lights brightest, but the name will out-shout them.
6. **The exit does not re-read the entrance.** "End of chart · fair winds" is a credits roll; the spec's "LIMIT OF SURVEY" is a better closing panel but still a destination, not a turn.
7. **Rest points are uniform.** Every gap is one `<br>`. Pacing comes from unequal rests: long before the climax, short after.

## What needs to be done

- **Give the exit an object worth walking to.** Fold Colophon and the shelf into closed `<details>`; the last 400px of the walk become Instruments strip → one line → footer. The colophon is the back of the catalogue, not the gallery wall.
- **One label per object, one job each.** Cartouche notes: numbers and names only. Bullets: two per system, both about purpose or consequence ("the last two are how you find the subdomains nobody links to" stays; "up to 512 workers" goes, it is on the chart). Alt: tombstone first ("Sheet 3, Approaches, 1280×880"), then the note.
- **Break the hang once.** Instruments at `width="62%" align="right"` beside the Other waters list so text wraps a narrow strip; Soundings full-bleed with no neat-line (spec does this) so "not a framed chart" registers twice.
- **Thin the hook, feed the climax.** Hero: ~20 soundings, no pencil notes, no source diagram. Move pencil notes, source diagram and legend to Approaches, the reading material of the climax room.
- **Fix the mounting.** Night paper two steps lighter than `#0d1117` (≈`#132037`), neat-line at the same relative contrast as day. Night name at `ink2`; only lights, the accent arrow and the sail reach full value.
- **Unequal rests.** Two `<br>` before Approaches, none between its sheet and its bullets, two before the footer.

## Improvements and high-level ideas

1. **The exit recontextualises the entrance (bold).** The footer carries a real chart convention, the **index of adjoining sheets**: a small diagram of rectangles in which the hero's extent is one shaded rectangle marked "1" and the rest are blank, hatched UNSURVEYED. On the way out the visitor learns that the chart they took for the whole web at the door was the surveyed corner of a sheet whose neighbours are empty. Nothing invented: the repos are the surveyed area; the blank is honestly blank. Sixty lines of chartlib.
2. **"Joins Sheet N" at the margins.** Charts print the adjoining chart's number where plates meet. Hero right margin: "joins Sheet 3"; Approaches west edge: "joins Sheet 1"; footer limit line: "no adjoining sheet". The hang becomes a sequence and the markdown gaps become seams between plates rather than dead wall.
3. **One vitrine with the thing itself.** Every object is a painting of the work. Build the log from a genuine session (spec F1), and add one specimen: the first twelve lines of a real `sitemap.xml` rustmapper emitted, 13px mono in the Approaches legend corner, labelled "specimen · output of a run". If it cannot be shown truthfully, the log alone carries it.
4. **A density curve, not a plateau.** Marks per unit area must rise to Approaches and fall after it: hero moderate, soundings sparse, Approaches peak, log medium, Instruments sparse, footer sparse with one dense corner (the index). Test: the eye accelerates toward the climax and slows after.
5. **Night as a lit gallery, not a dimmed one.** At night drop the graticule and cut contours further so the hero becomes dark water with lights, a name and a course; by day it is a full printed sheet. Two readings of one object is what lighting is for.

## What the page says about its maker

Now: someone who can design one superb object, then hangs six more at equal spacing, labels each twice, and leaves the visitor to find the door through a corridor of reading. The craft is evident; the curation is not. It should say: someone who knows a page is walked, not viewed; that the work is the object and the words are the label; that one room is the climax and the exit is a turn; and that the lights come on at night for a reason. The spec gets the objects right. The hang, the labelling discipline and the exit remain.

## Five most important lines

1. 38% of the walk (y≈3400 to the end) has no object; fold Colophon and the shelf into closed `<details>` so the exit is Instruments → footer.
2. One label per object, one job each: cartouche carries drawable facts, bullets carry purpose and link (two each), alt opens with a tombstone.
3. Break the equal hang once: Instruments at `width="62%" align="right"`; Soundings full-bleed without a neat-line.
4. Footer = index of adjoining sheets: the hero's extent is one shaded rectangle among blank hatched ones, so the exit re-reads the entrance.
5. Mount the object the same way in both editions (night paper ≈ `#132037`, name at `ink2`) so at night only the lights reach full value.
