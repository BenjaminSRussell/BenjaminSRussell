# Round 4 — decisions (8 Oct 2026)

Six critics read the merged v9.2 with a brief to question the design and the method, not to polish:
creative director, information designer, GitHub-profile pragmatist, typographer, a cold-read stranger,
and a methodology critic. Their reviews are beside this file. The owner's verdict that set the round:
"I still don't like the design and methodology."

## What they agreed on

1. **The page is three times too long and says everything twice.** Five of the six sheets re-ask the
   reader to learn the conceit; the markdown headings repeat the sheets' own titles; the sheet-3 notes,
   the tide figures and the tool list repeat the prose. The hero is the asset; everything after it dilutes it.
2. **The hero's measure contradicts its thesis.** Area ∝ commits crowns an eight-day game engine and a
   browser game; a 7 Oct housekeeping sweep is "high water"; the two flagships are third and fifth and the
   survey vessel is a 10 px glyph. Commit-days (in the data for every repository) put Scrapy and rustmapper
   first and second by a wide margin and are immune to sweeps and bursts.
3. **The hero is a wordmark dropped on a bubble chart.** The name has no relation to the title block; the
   middle of the sheet is a scatter of twenty islets no hand would draw; the harbour the thesis names is a
   dashed inset. The phone edition, with seven islands, composes; the desk edition does not.
4. **Honesty by hedge reads as apology.** Sloping figures, a computed log, "unsigned", "PA", "SD", "ED" put
   a dozen disclaimers on the page in small type. A figure that was not measured should not be printed.
5. **The method certified conformance.** The rubric audits fidelity to the conceit and cannot vote to cut
   a sheet; three rounds produced the same class of finish findings; no real stranger and no alternative
   has ever been shown to the owner; everything was judged on PNGs, not the live page.

## Decisions

**D1. One chart.** The page is the hero and written text. Sheets 2–6 leave the README and the default
build (the modules stay in the tree, buildable on request). The markdown headings that repeated sheet
titles go with them.

**D2. The measure is commit-days.** Island area ∝ commit-days; the printed figure is commit-days, upright,
no subscripts. The unit line says SOUNDINGS IN COMMIT-DAYS. Commits, months and languages live in a written
register below the chart. One glyph, one meaning.

**D3. Compose by hand, drive by data.** The named features (commit-days ≥ 7, eight today) have hand-set
slots in chart.toml; their radii follow the data; the rest of the repositories are rocks (small marks, no
figure) in a dotted fringe, counted in the title block. The placer, the lock file and the drift warnings
retire. If a data change would need a feature moved, the figure changes, not the place.

**D4. The hero is composed around the harbour.** One cartouche top-left: the name, the thesis, then the
title lines at two sizes on one left edge; the chart fills the rest with Scrapy Harbor large and
rustmapper's ground beside it, the course from the limit of survey into the harbour, the boat sailing in
once. 20- and 50-contours and their figures go; 5 and 10 tints stay, generalised. The rose stays as the
24-hour clock, smaller, under the cartouche, with the hour histogram drawn as its ticks. The unsurveyed
band stays. No inset box, no SEE SHEET 3, no legend. The pencil note reads "sitemap.xml lies again".

**D5. Nothing unmeasured is printed.** No sloping figures, no computed log, no illustrative soundings. The
upright/sloping convention retires as an expression; "nothing invented" stays as a rule. The survey's own
real log (what was cloned, when, which instruments were live) appears as text under the chart.

**D6. Night is redrawn, not swapped.** Night weights +20 %; land `#263040`; tints `#13304F` / `#1A4470`;
the night `ink2` and `muted` values swap so secondary type out-ranks captions.

**D7. Type.** Caps labels tracked +1.6, title lines +2.0, italics untracked; condensed at 19 and 25 only
(16 reserved for nothing on the hero now). The faces stay this round.

**D8. The page.** Hero → one written line (field · languages · position slot) and the links row (with the
résumé/LinkedIn slots) → the three bold lines → rustmapper (bullets, install block) → Scrapy Harbor
(bullets) → other work (four lines, the rest folded) → notices 1–4 → the survey log and a one-line
colophon. `<img>` tags carry width and height so the page does not jump. Target ≤ 2,200 px at 870.

**D9. The method.** The rubric panel stops being the acceptance test. Acceptance is the owner's eye on the
live page and three strangers asked one question ("what does he build, and would you click?"). Three
concept stills from different premises are built alongside this round for the owner to compare on GitHub:
the vessel in section, the waterfall, the survey lines. Engineering is frozen: no new gates, decisions or
BREAKS until the owner chooses a direction. The workflow runs on push and weekly; the render and perf
tiers leave CI and stay as dev tools.

**D10. Asks of the owner** (docs/BEN-TODO.md): fill the position and contact slots; record one real
rustmapper run on a host you may crawl, so the page can show measured crawl figures; look at the three
concept stills on the preview branch and say which you would screenshot.
