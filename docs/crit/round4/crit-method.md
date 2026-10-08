# Methodology crit — how the Chart profile is being designed, judged and built

Read: MASTERPLAN.md (29 decisions, §7 rubric), acceptance.md (three rounds), recrit3/crit-owner.md and crit-art.md in full, the findings lists of crit-hydro.md and crit-mobile.md, the first-panel skeptic (06), the "five lines" of four panel-30 reviewers, BEN-TODO.md, the git log, and the current renders (readme-light.png in five crops, hero-day-870.png, the top of readme-390.png).

Numbers the diagnosis rests on:

- Written about the page: ~150,000 words (panel30 42k, tech leads 27k, plan/specs/build reports 43k, three re-crit rounds 37k). The README is ~1,200 words.
- Built to draw the page: ~4,000 lines in `sheets/`, ~4,400 in chartlib/timeline/typeset, ~1,900 in `check.py` + 18 check modules, 63 BREAKS entries, 11 test files, two workflows.
- Calendar: v9 landed 7 Oct; v9.1, v9.2 and three review rounds happened 7–8 Oct. The plan budgeted 287 lead-hours. The "team of ten leads, thirty critics, eight builders" is one session wearing hats.
- Human judgments of the page in the record: the owner's, three times ("mediocre", "crushed / weird / not cool enough", "I still don't like the design and methodology"). The one human test in the gate (§7.1 five-second test) is marked *pending* and was replaced by "the panel's own 5-second readings".
- Score history: 30 → 34 → 24–27 with the page improving the whole time. The score tracks the panel's brief, not the page.

---

## 1. Diagnosis of the method

### Where the effort goes versus where the dissatisfaction lives

The effort went into making the page a *correct chart*: depth-as-count, IALA Region B buoys, doubt marks (PA/SD/ED/Rep), zones of confidence, upright/italic honesty numerals, a 96-second page-wide SMIL timeline on a 0.5 s grid, still-frame ink-coverage ≥ 0.95, silhouette L1 ≥ 0.25, determinism across builds, repaint budgets per sheet, per-edition size caps, a legend that must match the symbol ids across sheets, a gazetteer so names agree, a lock file so islands do not drift. Every one of these is defensible in isolation and together they are the whole budget.

The owner's words were "world class, one of a kind, beautiful, stunning, fun, tells a lot about me" (BRIEF), then "crushed, weird, not cool enough" (acceptance v9.1), then "I don't like the design". *Stunning*, *fun*, *cool* and *beautiful* do not appear in the rubric. Not one of J1–J12 asks whether anyone wants to look at the page, screenshot it, or send it to someone. Nine of the twelve criteria (J3, J4, J5, J7, J8, J9, J11, J12, half of J6) measure conformance of the artefact to its own concept: is it a proper chart, is it honest, is every still finished, does night follow the rule, are there four hidden layers. The rubric is a conformance audit of the conceit. It cannot register "I don't like it" because disliking is not a line item.

Look at what the render is at 870 px. The hero is a big serif name, one italic line, a clock, and a scatter of 21 small blue-grey blobs each carrying a subscripted number. The second sheet is a tide curve over a 5×5 table of repos. The third is a legend of 36 rows under a plane of small sloped numbers. The fourth is a terminal table. The fifth is a contents page with dotted leaders. The sixth is the one with a mood. The page is 4,900 px tall at 1,100 wide. It is dense, accurate and quiet. Nothing on it is large except the name; nothing on it is a single image you remember. "Not cool enough" is an accurate reading, and it is a composition verdict, not a correctness one. The method has no instrument for composition verdicts, so it keeps fixing collisions.

### Is the rubric measuring the right things?

No, and it was never checked against the brief. The rubric was synthesised by the first six critics into STANDARDS.md, then T10 turned STANDARDS into J1–J12, and CRIT2-BRIEF told the next thirty critics to "treat all of that as the CURRENT DIRECTION". From that moment the method was structurally unable to question the direction: thirty professionals were asked to add what their profession sees *within* the chart conceit. The three re-crit panels then scored the page against the rubric those standards produced. The loop is closed on itself: the panel finds what the rubric tells it to look for (duplicated figures, 8 px type, an unlit leading light, a legend row with no referent), the builder fixes those, the next panel finds the next layer of the same kind.

Worse, two rubric lines actively work against what the owner asked for. J12 rewards *uncaptioned* second-look layers; J9 and the `strings.py` check ban jokes, self-explanation and borrowed phrases. The first-panel skeptic said the page lacked "fingerprints, exceptions and one joke that pays off late"; the method's answer was rules that prohibit fingerprints. The honesty machinery (J7) has turned "no invented numbers" into a visual system of hedges: at page size a stranger reads *unsigned*, *computed from settings*, *not measured*, *existence doubtful*, *position approximate*, *provisional*, *proposed · unlit*, *sloping · not measured*. The page says "I am not sure" a dozen times in small type. That is honest and it is not stunning.

### Is the panel-then-fix loop converging?

It is converging, on a local optimum: a hydrographically correct chart with no collisions. Evidence:

- Round 1 defects: colophon swallowing the footer, nine notices under "five principles", 8 px legend type, harbour-mouth sounding cluster, floating hatch. Round 2: a crowded square inch at 208°, zeros reading as stippling, two phone label collisions, 8–9 px footer fine print. Round 3: neatline through the folio, "429 Shoa" clipped, Delta Lake overprinted, thesis said five times, figures said four times. These are the same class of finding each round: finish, duplication, type size. Each round is polish for the previous round's fixes. The art director's own summary of round 3 says "what keeps this from world class is not taste but finish and economy" — and that is the premise the owner has rejected three times.
- The score went *down* in round 3 while the page got better, because the brief said "harder". A gate whose reading is set by the brief is not a measurement.
- The crush (13 px sheet type shown at 8.8 px) was predictable from the BRIEF's first page ("sheets are 1280 wide and scale to ~68%"), was dropped as a rule in decision 6 by arithmetic, and was discovered by the owner on the live page. The thirty critics and the 1,900 lines of checks all read 1280 px renders. The method tested the artefact, not the experience.
- The one owner's-advocate finding that is structural rather than polish (round 3, #1: the datum crowns a game engine, so the chart says his biggest work is an 8-day voxel toy) has been in the data since v9 and was not caught by three rounds, because it is correct chart-making and the rubric scores correctness.

### What has never been tested

1. A real stranger. Zero humans other than the owner have looked at this page. The five-second test is the only human gate and it is *pending*, delegated to "Ben to run". The panel wrote its own answers in lieu.
2. The live GitHub page as the design surface. Everything was judged on 1280 px (then 870 px) PNGs of individual sheets; the owner judges on github.com in his browser, scrolling. Even now, v9.2's review set did not include the live profile.
3. An alternative. Since v8 the only alternatives built have been fixes. No concept sketch has ever been placed next to the chart for the owner to compare. v3–v7 were alternatives, each built fully and rejected after the fact; nobody has yet produced three cheap stills and asked "which?".
4. The owner's taste directly. Nobody has asked him for three profiles, posters or objects he finds cool, or shown him two directions and watched which one he lingers on. His stated wants were translated once (BRIEF → STANDARDS) and never consulted again. "Fun" was translated into a sea serpent every 96 seconds.
5. The page cut by half. Every round adds a sheet or a rule; the owner's advocate had to argue, in round 3, for cutting Instruments. Subtraction has never been tried as a method.

---

## 2. Which MASTERPLAN decisions are load-bearing for the dissatisfaction

**Reopen.**

- **The literalism of the conceit, not the conceit.** The nautical metaphor is sound: the avatar is a sailboat going over a waterfall, the e-mail handle has "sail" in it, crawling as surveying is a real idea, and the first second ("Ben Russell" against contours) was praised by the harshest first-panel critic. What is load-bearing is the decision, taken implicitly across STANDARDS 4 and decisions 14–21, that "chart" means *faithful hydrographic reproduction*: IALA buoy numbering, doubt marks, zones of confidence, datum lines, a 36-row legend, small corrections ranges. That literalism is what generates the small type, the hedges, the marginalia and the length. A poster-maker uses a chart's vocabulary; a hydrographer uses its grammar. The page was built by the hydrographer.
- **Six sheets (decision 4, 5, 11, and the "arc with a climax" in STANDARDS 7).** Load-bearing for "long", for "says everything four times", and for the sheets that look generated (Instruments, Log). Six separate drawings also multiply every rule by six and every edition by six (38 files). Reopen to one or two.
- **Area ∝ commits (decision 15, STANDARDS 3).** Load-bearing for "weird": the honest unit makes Game Engine I. the largest mass on the hero and Data Science Bank the high-water event, while the two flagships are smaller and the survey vessel is a 10 px glyph. The chart tells a stranger the wrong story and does so provably. The owner's advocate's fix (commit-days) is a patch; the real reopening is whether the portfolio should be a data-driven archipelago at all, or a composed one where the two flagships are drawn large because they are the flagships and the rest are a dotted fringe.
- **Honesty typography as a visual system (decisions 14, 20, STANDARDS 1–2, J7).** Keep the principle (nothing invented) and drop the expression. A page meant to persuade should not show what it has not measured; it should leave it out. The computed ship's log, the sloped URL soundings on Sheet 3, the italic worker count, the "unsigned" sign-off: every one of these exists only because the method chose show-and-hedge over omit. Omission needs no legend row.
- **Nightly re-layout (decisions 8, 12, 16–18, the placer, lock file, Halton slots).** Load-bearing for "weird" in a second way: composition is being done by an algorithm, nightly, with a lock file and drift warnings to keep it from rearranging the sea. ~1,500 lines exist to place islands a designer would place once by hand. Keep nightly *numbers*; stop nightly *composition*. A hand-placed hero whose figures and a few sizes update is both more stable and more beautiful.
- **The acceptance definition (§7).** Reopen entirely: a 12-line conformance rubric judged by personas, a five-second test nobody ran, and 40 lines of perf/still-frame gates. Replace with the owner's eye and five strangers (§3).

**Sound; keep.**

- No JS, SMIL-only, `<picture>` editions, outlined type, sanitizer-proven markup, orphan `chart` branch (decisions 8, 9, risk 1). These are the platform; they are not why the page is disliked.
- "Nothing invented" as a principle (BRIEF hard constraint). Keep it; stop illustrating it.
- One data source (`stats.json`), a schema, a red build that never publishes half a page (phase 0a, owner's advocate round 1). Good engineering, cheap to keep.
- The two flagships as the subject; plain-text field/languages/stack/contact under the hero (J10). This is the only part of the page every reviewer agrees works.
- Night as a designed edition rather than an inversion (decision 21). Keep, but it is finish, not direction; it should not consume another round.

**Sound in principle, overbuilt in practice; freeze, do not extend.** The check tiers, the still-frame and silhouette gates, repaint budgets, BREAKS lists, the decisions log. They stop regressions in a design that is not yet wanted. No new checks until the design is chosen.

---

## 3. The method for the next round

**Premise.** Three rounds of convergent fixing have not moved the owner. The next round must be divergent, judged by eyes, decided by the owner, and built with a tenth of the ceremony. Timebox: one week.

### Generate: five concept stills, not fixes

Each concept is *one image* at 870×~600, hand-composed (SVG by hand, or even a raster mock), no pipeline, no data feed, placeholder numbers clearly marked in the file name as mock. Each must start from a different premise, and at least two must not be a hydrographic chart. Suggested set, each with its one-line bet:

1. **Poster chart.** The current conceit at poster scale: one sheet only, the name, the thesis, *five* islands (two flagships drawn large, three others small, the rest a dotted fringe labelled "and 16 more"), one boat, the unsurveyed hatch as a third of the sheet. No legend, no buoys, no doubt marks. Bet: the chart was right, the hydrographer was wrong.
2. **The waterfall.** The avatar's image as the page: the boat at the edge where the charted web ends, drawn as one illustration with the thesis; two plain-text project blocks below. Bet: one strong picture beats six correct ones.
3. **The log as the page.** No chart at all; the page is a single typed survey log of a real rustmapper run on a domain Ben controls, with real numbers, upright, and the name as the header. Bet: evidence is cooler than metaphor, and it forces BEN-TODO item 7 to happen.
4. **The current page cut to 40 %.** Hero (re-weighted per round-3 art #1), the at-a-glance lines, the two project blocks, footer. Sheets 2, 4, 5 and the Notices deleted outright. Bet: it was good and buried.
5. **Something that is not nautical.** Whatever the builder finds genuinely exciting that still says "crawl and data infrastructure, Python and Rust, two systems, honest numbers". Bet: the conceit is the problem.

Each concept comes with one paragraph of what it says about Ben and a list of the three things that would be nightly data. Nothing else. No rubric, no BREAKS, no plan.

### Judge: eyes, strangers, the live frame

- Push all five into the scratch repo's README one after another (render.mjs shadow already exists) so each is looked at **on github.com at the owner's screen and on his phone**, not as a PNG.
- The owner looks at each for ten seconds, then answers three questions per concept, in writing, in one line each: *Would you screenshot this and send it to someone? What does it say you do? What do you want to keep looking at?* Then a rank order. His answers are the record; no scores.
- Five real strangers (not personas): friends, a Discord, a design subreddit, a colleague's partner. Show each the top two concepts for five seconds each, ask: what does this person do, what do you remember, which do you prefer. Five people is enough to kill a concept; it is not a study and should not be dressed as one.
- Optional, cheap: one professional designer paid for an hour to say which concept has a future. One, not thirty.

### Decide

The owner picks one concept and writes one sentence why. If none clears "I'd screenshot it", the round repeats with five new premises; it does not proceed to building a concept he merely tolerates. The sentence goes at the top of DESIGN.md and replaces the thesis paragraph of the MASTERPLAN as the thing every later choice is tie-broken against.

### Build: hand first, data second, one PR

- Start from the chosen still. Turn it into a working SVG by hand. Only then automate the numbers that must change nightly (commit counts, dates, the edition); positions are fixed by hand and committed. If a data change would require moving a thing, the thing does not move; the number does.
- One builder, one reviewer, one PR, at most two editions per image (day/night; phone only if the desk page is loved first).
- Reuse from the pipeline: `build_stats.py`, the schema, the `chart` branch publish, the XML/size/sanitizer checks, `render.mjs shadow`. Delete or leave dormant: the placer, the lock file, the timeline grid, the still-frame and silhouette gates, the perf harness, BREAKS, the honesty typography registry, `strings.py`.
- Ship it live. Leave it up for a week. The owner reads it on his phone on a Tuesday. Only then any crit, and that crit is three people, 300 words each, no scores, each required to attach one sketch of the change they want.

### Stop doing

- Panels of personas scoring rubrics; rounds "at a harder bar"; medians of imaginary reviewers.
- Writing plans, decisions logs and acceptance records that are longer than the page. The MASTERPLAN is 29 decisions nobody will reopen because reopening one re-solves twelve others.
- Treating a check as a design. No gate has ever made a page cool; a gate keeps a cool page from breaking.
- Hedging on the page. If a figure is not measured, it is not on the page.
- Six of anything. Six sheets, six editions, 36 legend rows, twelve rubric lines.
- Delegating the only human test to the owner and then substituting a persona's reading for it.
- Judging renders. Judge the page where it will be read.

---

## 4. Process changes, ranked

| # | What | Why | Effort |
|---|---|---|---|
| 1 | **Owner's eye before build:** five hand-made concept stills from different premises, viewed on the live scratch profile, ranked by the owner with three written one-line answers each. | Three convergent rounds have not moved him; nothing divergent has been shown to him since v8. His taste is the acceptance test and it has never been sampled directly. | 2 days to make; 20 minutes of his. |
| 2 | **Replace J1–J12 with three stranger questions and the owner's veto;** run them on five real people via the scratch repo. | The rubric audits conformance to the conceit and cannot register dislike; its score fell while the page improved. Five real strangers beat thirty personas. | Hours. |
| 3 | **Judge only on github.com, at the owner's screen and phone.** No more PNG-of-a-sheet review sets. | The crush shipped because everyone read 1280 px PNGs; the owner reads a browser. `render.mjs shadow` already does the push. | Hours; already built. |
| 4 | **Freeze the engineering until the design is chosen:** no new checks, gates, BREAKS or decisions; delete nothing yet, add nothing. | ~8,000 lines of pipeline and 1,900 of checks protect a design that is not wanted. Every added rule raises the cost of the change that is actually needed. | Zero; it is restraint. |
| 5 | **Compose by hand, drive by data.** Fixed positions in the file; nightly updates numbers and a few sizes within hand-set bounds. Retire the placer, lock file and drift warnings. | Algorithmic composition is why the survey reads "weird" and why the biggest island is a game engine. A composed hero is both stabler and better. | Medium (a rewrite of the hero, a deletion elsewhere); net fewer lines. |
| 6 | **Hard length and count budget:** at most two generated images, at most two screens at 870 px, each fact said once, nothing not measured. Enforce by cutting, not by adding a check. | Every reviewer in round 3 ranked repetition and length in their top three; the page has grown each round. | Small; it is deletion. |
| 7 | **Honesty by omission.** Keep "nothing invented"; remove the upright/italic/doubt-mark system and every unmeasured sheet (computed log, sloped soundings) until the real run exists. | The hedge system puts a dozen apologies on the page in small type; a stranger reads uncertainty, not rigour. The real log is one afternoon of Ben's time and is cooler than any simulation. | Small to cut; L for the real run, which is worth it. |
| 8 | **Change the crit format:** three reviewers, 300 words, no scores, one attached sketch each of the single change they would make. Crit only after a week live. | Prose findings lists of twelve S-items generate polish rounds; a sketch forces a reviewer to commit to a direction. Scores were never measurements. | Zero. |

The short version: the method built a studio to produce certainty and got a page that is certain and not liked. Stop certifying it. Show the owner five things he has not seen, let him point, and build the one he points at by hand.
