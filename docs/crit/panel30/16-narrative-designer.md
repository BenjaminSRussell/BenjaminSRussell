# 16 — Narrative / game designer

I design environmental storytelling and reward schedules: what a player finds in ten seconds, what keeps them moving, what they screenshot. I looked at page-day-full, hero-day-2x, footer-night-2x, the other renders, README.draft.md, STANDARDS.md item 13, spec-hero.md §7, the footer section of spec-supporting.md, and stats.json.

## What is good

- **The avatar is already a three-act structure.** The GitHub avatar (a sailboat about to go over a waterfall) is act one; the hero boat sailing a course is act two; the footer boat at the edge is act three. The reader assembles the arc unprompted, from an asset that exists before the README loads. Few profiles have a protagonist.
- **The hero's 10-second read is complete.** Name, thesis, chart, boat, course. A visitor who leaves after one screen has the hook (a chart of the web), the promise (soundings, a course into harbour) and a reason to scroll: the course leaves the frame to the right, into the UNSURVEYED band.
- **The log is the best diegetic UI on the page.** A document the character wrote, not a card about him. "14:05 nothing to report / Nothing on fire" is a two-beat joke in the form; the second beat lands because the first was dull.
- **Spec-hero §7 is a real second-look layer.** Pencil notes pointing to Notices, underlined true heights, "VAR 21h00 · see colophon" as a question the colophon answers: the start of a collectible structure.

## What is bad, ranked

1. **The reward schedule is front-loaded.** Discovery lives almost entirely in the hero. In the current renders sheets 2–6 are exposition: a stats row, two project cards with the same silhouette, a stack table. A 10-second visitor gets everything; a 2-minute reader gets a list; the person who opens the SVG source gets the same text as the page. Three audiences, one layer. The spec improves the middle but still schedules nearly every secret on sheet 1.
2. **The collectible loop is one-directional.** Marginalia say "see Notice 3"; the Notices say "entered from ideal-url-organizer". Nothing in the Notices sends the reader back *up* to find the correction on the chart. A collectible that never makes you scroll back is a caption.
3. **The footer resolves nothing.** Today it is a credits roll ("End of chart · Fair winds · Thanks for reading this far") and six dots of waterfall. The spec's "LIMIT OF SURVEY" is a better line but is still a destination, not a recontextualisation: nothing in the footer changes what the hero means on a second scroll-up.
4. **The serpent has no witness.** 2.4 s every 96 s, first at 96 s, on the bottom sheet of a page people spend perhaps 40 s on. Discovery probability per visit is a few percent; a secret nobody finds is a cost. Related: every one-shot opening on a lower sheet plays while the reader is still on the hero, unless GitHub lazy-loads README images so the SMIL clock starts on entry.
5. **True soundings have no confirmation moment.** The aha of a hidden true number needs a way to check it. 512 and 256 are checkable only by someone who already read the bullets. One figure has its proof on screen: 46, because GitHub prints the follower count in the sidebar beside the README. The spec puts it beside Profile Shoal, which is right, but the design does not know how good that is.
6. **The best real story in the data is never told.** game_engine: 585 commits between 2026-01-04 and 2026-01-14, the largest feature on the chart, surveyed in ten days and left. A dormant island with a sprint behind it. The page treats it as a radius.
7. **Non-diegetic debris.** Pill chips, stat cards, the snake. The rule is binary: inside an SVG everything is in-world; in Markdown everything is plain.

## What needs to be done

- **F1 Close the Notices loop.** Each corrected feature carries a small Δ and its notice number in `plex` 13 (Δ3 at the sitemap shoal, Δ2 at the anchorage, Δ4 at ideal-url-organizer's islet). Each Notice in the list ends "Δ on Chart No. N", linked to `#top`. Real charts tally hand corrections in the lower-left margin: add "CORRECTIONS 1 2 3 4 5" there. Five things to find, and the list tells you to go look.
- **F2 Footer as the hero's edge seen from the water.** The hero shows the UNSURVEYED band in plan; the footer shows the same band in elevation: identical hatch pattern, identical "LIMIT OF SURVEY 2026" text set horizontal, chart number outside the frame on both, the footer boat on the hero course's final bearing. On scroll-up the margin becomes the fall. Cost: matching pattern IDs.
- **F3 Give the serpent a trace.** First rise at `arrive.end + 20s`, not 72 s; leave three ripple rings decaying over 20 s where it dived, so a glance shows something was there.
- **F4 One marginal note for game_engine.** `serif-italic` 16, rotated: "surveyed in ten days · Jan 2026", leader to Game Engine I. Generated only when `last − first ≤ 14 days`, so it is a rule, not a hard-coded line.
- **F5 Keep 46 beside Profile Shoal with the △ glyph** and add nothing. The sidebar is the confirmation.
- **F6 Make the SVG source the third layer.** `<title>` on each feature group (repo, commits, first/last dates); short XML comments in the hydrographer's voice before each section. Under 4 KB. The person who opens the source is the one most likely to hire or link.
- **F7 Confirm lazy-load behaviour** of README images and record it in DESIGN.md. If eager, delay or drop every one-shot opening except the hero's.

## Improvements and high-level ideas

- **Bold: let readers correct the chart.** The HTML comment already says "corrections are welcome and will be entered as notices." Make it literal: an issue template "Notice to Mariners" (hazard, position, source), a `notice` label, and `build_stats.py` counting closed `notice` issues so "Corrected through Notice N" and the margin tally are live. The reader becomes a mariner reporting a shoal. Honest, participatory, and the one mechanic that gives a stranger a reason to send the page on: "report a hazard on this guy's chart."
- **Adjoining-sheet chain.** Every sheet carries "continued on sheet N+1" at its right edge and "from sheet N−1" at its left, as adjoining charts do. The footer's right edge reads "no adjoining sheet". The sheets become one chart you walk across; the chain breaks only at the fall.
- **The night edition has a reason.** The compass clock says the busiest hour is 21h. The colophon's variation line should resolve two things in one sentence: why north points where it does, and why a night chart exists at all. Said once, at the end.
- **The log ends at a position, not a sign-off.** "14:12 · anchored · next watch resumes from WAL offset". The last diegetic word points forward, which is what brings a reader back to see whether the figures changed.

## What the page says about its maker

Now: someone with one great image and a genuine idea who ran out of story after the first screen and signs off with other people's jokes. It says "I can design a hero." It should say: this person builds systems that keep records, and the page is itself such a record, corrected over time, its edge honestly marked, with more in it the longer you look. Pacing is the tell: a page that rewards a second scroll-up is made by someone who expects to be read twice.

## Five most important lines

1. Verify whether GitHub lazy-loads README images; if not, every one-shot opening below the hero plays to an empty room and must be cut or delayed.
2. Close the collectible loop: Δ-marks with notice numbers on the chart, a margin tally "CORRECTIONS 1 2 3 4 5", and each Notice in the list pointing back up to the chart.
3. Make the footer the hero's UNSURVEYED band seen in elevation (same hatch, same text, same chart number) so scrolling back up recontextualises the margin as the fall.
4. The serpent needs a witness: first rise at +20 s and decaying ripples where it dived; a secret with a 3% discovery rate is a cost, not a reward.
5. Bold: make "corrections are welcome" literal with a "Notice to Mariners" issue template that drives "Corrected through Notice N"; it is the only mechanic on the page that gives a stranger a reason to share it.
