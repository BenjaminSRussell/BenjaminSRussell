# 29 — UX researcher (eye-tracking, usability testing, comprehension studies)

I run 5-second tests, first-click studies and think-alouds. I predicted the gaze path on page-day-top.png and page-day-full.png at 870px and 360px, then read README.md, README.draft.md, spec-hero.md and 18-recruiter.md, which I build on rather than repeat.

## What is good

- **Fixation order on the hero is correct.** Fixation 1: "Ben Russell" (176 → ~120px rendered). Fixation 2: the italic thesis beneath it (40 → 27px). Both land inside 1.5 s, and they are the only two things a scanner must read.
- **The F-stem passes through the cartouche**: after the two horizontal bars the eye drops down the left edge into the title block. Its position is right; only its size is wrong.
- **Blue links are the only blue**, so the link row is a reliable third fixation and a trusted exit.
- **Big numerals on Soundings** pull a fixation each; numbers over 40px are read before any word, so the sheet works as a stat row for a reader who has never met the word.
- **Dual-register headings** are the right mechanism for a medium with no toggle: the plain word arrives in the same fixation as the metaphor.

## What is bad, ranked

1. **Small tracked mono caps is the metadata register, and scanners skip it.** The cartouche's SURVEYED / PYTHON · RUST · SWIFT · C lines (~9px rendered), the Soundings labels (~7px), the Approaches feature lines and the whole Legend (~7px), the buoy labels URLS / SCOUT / ANALYZE / SUMMARIZE (~8px): all read as form footer. Prediction for a 5-second test: 0/10 recall the languages, 0/10 the pipeline stages, ~3/10 "Full-stack developer" because it is serif italic. The harbor chart's one fact, the four stages, lives only in 8px labels.
2. **The draft thesis is a riddle at fixation 2.** "I survey a web that is wrong about itself" is read by everyone and understood by the engineer who already knows what a CT log is. Fixation 2 is too expensive for a line that pays off a paragraph later; the current "I build crawlers that survive the open web…" is plain and lands.
3. **"6" without its label is a comprehension hole.** On Soundings the numerals are legible and the labels are not, so the sheet says "1,828 · 24 · 46 · 6 · Oct 2024" and the reader guesses. A figure whose label is under 11px rendered has no meaning.
4. **Empty states read as broken.** The Soundings still shows a dashed empty tide box; the log still shows blank ruled paper. A scroller gives each sheet ~1.5 s; blank paper at that budget means "image failed". The draft fixes the tide; the log still depends on an animation that may or may not have run when the reader arrives.
5. **"Approaches" is a false friend**: to a non-sailor it means *methods*; the section delivers *projects*, and it is the first H2. "Soundings" is safer than it looks (the idiom is common and the numerals disambiguate). "Notices to mariners" has zero unaided comprehension. "Below the waterline" reads as *sunk / abandoned* to about half of readers, which is not what the fold holds.
6. **The `<details>` fold hides breadth behind an opaque label.** Closed folds with metaphor labels open in low single digits in my studies. The draft fold holds Swift, C, games and widgets, exactly what the engineer persona scrolls for ("is he only a crawler person?"). No count, no plain words; the decision to open is blind.
7. **The position-line slot is invisible by design.** An HTML comment has no affordance for the reader and no failure mode for the author, so pages ship with comments in them. The cartouche mirror (~15px rendered, 4px on a phone) sits in the zone the eye skips.
8. **At 360px the hero is a name and a texture**: thesis 11px, cartouche 4px. The phone edition (spec C9) must be tested, not assumed.

## Three personas, by the clock

| | 10 s | 60 s | 300 s |
|---|---|---|---|
| **Recruiter** | name; field in plain words; role, place, open-to; a contact | two systems in hiring words; languages in text; seniority cues; résumé link | does not exist; she forwards the link |
| **Engineer peer** | what he builds, in what, one proof it is real (PyPI) | the two systems' bullets; the five principles; a click into a repo | checks the log's arithmetic; opens an SVG source; reads the colophon; the metaphor is a feature if every number is real |
| **Designer** | type, palette, hero composition | do the sheets differ; is motion intentional; is night deliberate | colophon, DESIGN.md, second-look layers; judges the seams between sheets and GitHub's default markdown |

The recruiter is served only by plain text (18). The engineer is who the metaphor is for and who punishes an italic that does not add up (21). The designer judges the 60% of page height that is un-designed markdown; caption discipline there matters more to her than another sheet.

## What needs to be done

1. **Two type tiers, by gaze.** Add to Standard 5: *scan tier* ≥ 22px at 1280 (≥ 15px rendered), serif, in the F-path (top 25% or left 40% of the sheet); *texture tier* everything else. Anything a persona needs within 60 s is scan tier or in markdown. The job title, the four channel stages and the Soundings labels are currently texture.
2. **Decide the thesis by test.** Run the 5-second test with both lines; the winner goes in the hero, the other opens the intro where its colon-gloss follows at once. Prediction: the plain line wins recruiters by 30 points and ties engineers.
3. **Fold summary carries contents and count:** `<summary><b>Below the waterline</b> · 12 more repositories: Swift, C, games, tooling</summary>`. Or keep the current three open groups, which cost nothing and act as sub-heads.
4. **Position line as a visible element with a hard failure.** Body-size text, not mono caps, directly under the link row; the build fails if the placeholder remains. Mirror in the cartouche second.
5. **Glosses in reader vocabulary, not in-metaphor:** Soundings · *stats, daily* / Approaches · *the two main projects* / Ship's log · *one run, line by line* / Notices to mariners · *five principles* / Instruments · *languages and stack* / Other waters · *smaller projects*. "Five corrections" and "one session" are still inside the metaphor. Gloss *sounding* at first use in the intro; *Datum: main* and *Region B* in the legend. "Corrected through Notice 5" is read in the hero before the Notices exist: let the Notices heading echo it, or drop it from the hero.
6. **No empty still, ever.** The log's t=0 frame carries the header row and first entry; the tide box never shows a placeholder.

## Protocol (two afternoons)

**A. Five-second test**, unmoderated, 3 cohorts × 10 (recruiters, engineers, designers), stimulus = live GitHub screenshot at 870px day; repeat at 360px and night. Questions in order: (1) What does this person do? (2) What words do you remember? (3) What is he called? (4) Where is he and what is he looking for? (5) What is "Scrapy" on this page? Two arms: current hero vs draft hero.

**B. First-click**, static full page, 5 tasks: find his programming languages; contact him; open his biggest project's code; find how he thinks about his work; find a Swift project. Record first click and time.

**C. Think-aloud**, moderated, 5 per cohort, 15 min, live page on a throwaway account, desktop then phone. Prompts: "Say what *Soundings* means here." "What is the ruled paper?" "Would you keep scrolling? Why?" "What does *Below the waterline* contain?" "One thing you'd tell a colleague about this person." Post-task definitions scored 0/1/2: Soundings, Approaches, Notices to mariners, Below the waterline, Datum: main.

## Success criteria

- 5 s: ≥ 80% name the field; ≥ 60% recall the name; ≤ 10% call him a Scrapy maintainer; ≥ 50% state role or place once the position line exists.
- First-click: languages ≥ 70% on text, not an image; contact ≥ 90% on Email; Swift project ≥ 50% open the fold unaided.
- Comprehension: glossed headings mean ≥ 1.5/2; anything under 1.0 is re-glossed.
- Time to first useful fact ≤ 3 s; to role ≤ 8 s. Scroll: ≥ 60% reach Notices, ≥ 40% the colophon. Phone: ≥ 80% read name and thesis at 360px.
- Text-in-image audit: every 60-second fact exists in markdown; the recruiter's CI check enforces it.

## Improvements and ideas

- **Bold: a shadow profile as the test rig.** A throwaway account whose README is the candidate build; every change re-screenshots it at 870/360, day/night, and those screenshots are the stimuli. Test the medium, not the mock-up, with v8 as the baseline arm.
- **Plain-twin lint.** `build_assets.py` fails if any H2 lacks a `<sub>` or any `<picture>` is not followed by one plain line. A convention a machine does not hold is a hope.
- **Mono caps as a budget**: one tracked-caps line per sheet plus the chart number, so the one that remains reads as a stamp instead of a footer.
- **Let "Approaches" work both ways.** Open with "Two projects, and how I approach them": the false friend becomes a pun and the risk becomes a layer.

## What the page says about its maker

Now: a maker who designs for the reader he is, a sailor-engineer with a large screen and time, and who has not yet watched a stranger spend five seconds on it. It should say: he knows what a reader does in five seconds, puts the fact where the eye lands and the metaphor where the eye lingers, and he tested it. "The surface is part of the system" is already Notice 5; this is how he proves it.

## Five most important lines

1. Small tracked mono caps is skipped by scanners; the job title, the languages, the Soundings labels and the four channel stages are all in that register, so the sheets carry none of the 60-second facts.
2. Decide the hero thesis by a two-arm 5-second test (plain "I build crawlers…" vs riddle "I survey a web…"); I predict the plain line wins recruiters by 30 points and ties engineers.
3. Add a scan tier to the type standard: anything a persona needs within 60 s is ≥ 22px at 1280, serif, in the F-path, or it lives in markdown.
4. The fold summary must show contents and count ("Below the waterline · 12 more repositories: Swift, C, games, tooling"); opaque closed folds open in single digits.
5. Glosses in reader vocabulary at first use, a ban on empty stills for log and tide, and a shadow-profile test rig with the criteria above as the ship gate.
