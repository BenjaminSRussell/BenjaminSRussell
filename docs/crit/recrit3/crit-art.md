# Art direction review — v9.1, judged at GitHub size

Judged from the 870 px sheets, the 1100 px page (light and dark) and the 390 px phone page. Pixel checks were made where a claim rested on one (noted inline). I measured, and retracted, one impression: the night hatch band is *not* brighter than the water (mean L 34 vs 40), so it is not in the findings.

## Scores — 25 / 36

| | Score | One line |
|---|---|---|
| J1 thesis once | 2 | Said once on the hero in one line, then paraphrased three more times: the hero sub-line, the prose paragraph, "sitemap says yes; the lead says no" on sheet 3, and the footer's "The chart ends here. The web doesn't." |
| J2 cover the name | 2 | The survey edge is present (hatch, limit line, pecked track, boat) but drawn at hairline; the largest mass on the sheet is Game Engine I., then the six-line title block. The hero argues "many islands", not "survey". |
| J3 cover the titles | 2 | Five of six name themselves by silhouette. Sheet 5 reads as a magazine sidebar (three rotated words, dotted leaders), not a chart. |
| J4 region, unit, datum | 2 | Sheets 1–3 state unit and datum in the margin. Sheet 6's soundings (9 8 7 5 4 3, 14) carry no unit; sheet 5 has no datum line at all ("dated by first commit" lives only in the alt text). |
| J5 point at any mark | 2 | Sheet 3's legend covers its marks at desk. On the hero the source diagram, "233°", "VAR 14h" and the ring-island on the limit have nothing; the footer's black hook is unexplained; the phone legend is 13 of 36 entries. |
| J6 changes with the data | 2 | Tide curve, HW/LW labels, island area and the cursor line move with the survey. The log is "computed from settings", and the phone log keeps none of its data rows. |
| J7 honesty | 3 | Upright/italic/underline discipline holds on every sheet I sampled; PA, SD, ED, Rep used as chart practice; "computed from settings · unsigned" on the log. |
| J8 every still finished | 1 | Bottom marginalia overprinted by the neatline on sheets 1 and 3 (day and night, verified at 3×); "429 Shoal" clipped to "429 Shoa" on phone sheet 3; "Delta Lake" overprinted by the leading line and a contour figure; an empty header row on the markdown table. |
| J9 once, no borrowed jokes | 1 | 1,665 / 1,966 / 21 appear four times; the survey date three times on one screen; "corrected through Notice 9" three times; languages and stack three times; sheet 3's notes panels restate the bullets beneath them. "Nothing on fire." is a stock quip. |
| J10 recruiter in 60 s | 3 | The three-row table under the hero does it; Email sits in the link row. |
| J11 night designed | 2 | Designed: the lights are the brightest marks and the hatch recedes (measured). But the three unframed night sheets have no edge against GitHub dark, and sheet 3's SCRAPY HARBOR drops a weight at night. |
| J12 second-look layers | 3 | Rose as a 24-h commit clock, the source diagram, area ∝ commits, per-repo tide marks under the table names, eight shard columns, the island sitting on the limit of survey, the sheet index in the footer. |

## Findings, ranked

The first three would raise the page most.

### 1. The hero's argument is drawn at the lightest weight on the sheet (hero, right half) — M
**What I see.** At 870 px the pecked track from rustmapper (PA 87₆) across the limit of survey into Scrapy Harbor is a HAIR dotted line; the inset "SEE SHEET 3" is a HAIR dashed box whose edge runs through "265₅" and "SCRAPY HARBOR"; the boat is ~12 px. Meanwhile Game Engine I. is the heaviest object after the name, and the six-line caps title block at bottom-left is the heaviest text mass after the thesis.
**Why it matters.** Cover the name and the sheet says "a lot of islands, one big one"; the survey story (vessel, track, limit, harbour) is a second-look layer when it should be the first.
**Change.** Raise the track and the inset box from HAIR to PEN (1.3); raise the limit-of-survey dotted line to PEN on the hero only. Cut the title block from six lines to four by dropping `CORRECTED THROUGH NOTICE 9` (the footer carries it) and `SOURCES · A SITEMAPS · B CT LOGS · C COMMON CRAWL` (the source diagram beside it already says it; sheet 3's Zones table says it a third time). Move the inset box so its edge does not cross the harbour label or the 265₅ figure.

### 2. Finish defects visible at page size (sheets 1, 3; phone sheet 3; README table) — S
**What I see.** (a) hero-day/night-870 and approaches-day/night-870: the bottom margin line (`CHART NO. 21 · SHEET 1 · SMALL CORRECTIONS…`, `CHART NO. 21 · SHEET 3 · APPROACHES…`) sits with its cap height under the dashed neatline; the footer sheet places the same line correctly below the frame. (b) approaches-phone-360: "429 Shoal" is cut by the right neatline to "429 Shoa". (c) approaches-870: the leading line and the "20" contour figure print over "Delta Lake"; "stage2_page_analysis" overlaps the Summarization Wks glyph. (d) readme-light/dark: the `| | |` header renders as an empty bordered row above "Ben Russell builds".
**Why it matters.** J8 is the rubric line a stranger notices first; each is a one-pixel tell that the sheets are generated rather than drawn.
**Change.** Give sheets 1 and 3 the footer's bottom-margin offset (the marginalia baseline must clear the neatline by at least one PEN). On phone sheet 3, pull "429 Shoal" inboard or anchor it to the left of the shoal. On sheet 3, break the leading line under the "Delta Lake" label (chart practice: lines yield to names) and shift `stage2_page_analysis` one line down. For the table, either give the header row words or render the three rows as a definition list.

### 3. The page says its figures four times (page, Soundings screen and sheet 3) — S
**What I see.** On the Soundings screen alone: the sheet's top-left line (date), the sheet's bottom line (`Source · 21 public repositories cloned … 1,665 commits · 1,966 all hands · 1,828 …`), and the `<sub>` line 20 px below it (`1,665 commits of mine · 1,966 all hands · 21 repositories surveyed … soundings taken 7 Oct 2026`). The log's cursor line repeats 1,665 and 21 again. Sheet 3's two notes panels (`2 One shard per core · permits 256–1024`, `3 Sized by redb commit latency · 250 ms`, `4 WAL crc32 · rkyv…`) are the same facts as the five bullets printed directly under the sheet.
**Why it matters.** Repetition is the thing that reads as template-y; a chart states a figure in one place and the reader trusts it.
**Change.** Remove the `<sub>` figures line under Soundings (the sheet is the source). Remove the two notes panels from sheet 3 and return the ~100 px to the chart (sheet 3 is the tallest on the page at 761 px); the prose beneath already carries every note. Keep the Source line on the sheet, since it is chart furniture; it is the only place the 1,828 figure belongs.

### 4. Sheet 5 is not a chart (instruments, whole sheet) — M/L
**What I see.** Three rotated words at 41 px with hairline rules fill the left 30 %; above LEAD and LOG is dead paper. The right 70 % is a contents-page device: name, dotted leader, date. The group headers already say LEAD · LANGUAGES / LOG · STORES / LOOKOUT · DECK, so the rotated words say the same thing twice on one sheet. No neatline, no unit, no datum.
**Why it matters.** It is the one sheet a stranger could not name by silhouette, and it is the sheet that duplicates the README table (Languages, Stack) third time round.
**Change.** Redraw as a chart's own list: a List of Lights block (Name · Character · First lit · the bold "underway" state as a lit/unlit character), set in the `machine` 19 px role with a neatline and `SOUNDINGS IN …`-style margin line naming the datum ("dated by first commit"). Drop the rotated words or shrink them to the margin as a sheet index. At minimum: delete the rotated words and let the three columns span the sheet.

### 5. The phone log keeps the wrong rows (log-phone-360) — S
**What I see.** The phone edition shows "remarks · nothing to report", "Nothing on fire.", "Log closed 1550 · unsigned" and the cursor line. Every row with a figure (fetched 230, 12,440 urls, 1h 43m) is dropped.
**Why it matters.** On a phone the log shows two jokes and a close; J6 fails there.
**Change.** Phone row selection: keep the `$ rustmapper crawl` line, `fetched 230`, `crawl complete · 12,440 urls` and `Log closed`; drop the two remark rows.

### 6. Sheet 3's explanatory lines are captions in chart clothing (approaches, left column and mid-sheet) — S
**What I see.** `write-ahead log · one cell per sounding`, `one shard per core · 8 here`, `Local knowledge advised · see Notices 1–5`, and the Zones table footnote `A: as declared by the site. B, C: as found.` Each explains a mark instead of letting the legend do it. The left column stacks nine labels in 150 px (SCRAPY HARBOR, Prometheus, stage4, stage1, Delta Lake, stage2, Redis, Traffic Sig, PostgreSQL, Summarization Wks), the densest text block on the page.
**Why it matters.** "Show, don't tell" is the owner's rule; the legend already decodes Track line, Hatch and Zone.
**Change.** Remove the four lines. Move the Redis/PostgreSQL/Summarization symbol stack into the SYMBOLS panel (they are symbols), which frees the left column for the three stage marks at their proper spacing.

### 7. One gazetteer, two spellings (hero vs soundings table) — S
**What I see.** Sheet 1: `COURSE CRUSADER I.`, `IDEAL-URL-ORGANIZER I.`, `DATA-VISUALIZER I.`, `GO GO GO I.` Sheet 2: `COURSE CRUSADER`, `IDEAL URL ORGANIZER`, `DATA VISUALIZER`, `GO GO GO`; only `GAME ENGINE I.` keeps its suffix, and the hyphens vanish.
**Why it matters.** Two hands drew these. A chart's names come from one gazetteer.
**Change.** One name function feeding both sheets; pick the "I." form for every island or for none, and keep hyphens or drop them everywhere.

### 8. Every sheet is titled three times (page rhythm) — S
**What I see.** H2 "Approaches" → sheet title "SHEET 3 / Approaches to Scrapy Harbor" → bottom margin "CHART NO. 21 · SHEET 3 · APPROACHES TO SCRAPY HARBOR". Same for Soundings and Ship's log. Framed/unframed alternates 1-framed, 2-plain, 3-framed, 4-plain, 5-plain, 6-framed, so the page has no beat.
**Why it matters.** The repetition is why the page feels long; the alternation is why it feels assembled.
**Change.** Bottom margin on every sheet reduced to `CHART NO. 21 · SHEET n` (as sheets 2, 4, 5, 6 already do). Give sheets 2, 4 and 5 the same dashed neatline as 1, 3, 6, or give 1, 3, 6 none; one rule for the set.

### 9. Footer furniture (footer, right third) — S
**What I see.** A BRUSH-weight black hook curls off the anchorage pool at the hatch corner and reads as a stray stroke; `9 notices · corrected through Notice 9` says 9 twice in one line (and the hero says it a third time); the soundings 9 8 7 5 4 3 and "14 · good holding" have no unit on the sheet.
**Change.** Draw the anchor cable at PEN as a dotted line to the anchor symbol, or drop it; `corrected through Notice 9` alone; add `SOUNDINGS IN …` to the footer's top margin as on sheets 1–3.

### 10. Phone hero crowding (hero-phone-360, right third) — S
**What I see.** `UNSURVEYED` and `SMALL-SCALE EDITION` stand rotated side by side in a 40 px hatch band; `Data Science Bank` runs into the hatch edge; the rose's `00` is overprinted by the ring and the N arrow; 265₅, 358₁, the boat and two lateral marks share 30 px.
**Change.** Move `SMALL-SCALE EDITION` to the title block at the bottom (it is an edition note, not a sea area); nudge the rose labels inboard by one texture size (18 phone); push `Data Science Bank` left of the bank's outline.

### 11. The rose's label crashes the water (hero, top right) — S
**What I see.** `VAR 14h (2026)` / `AUTHOR'S LOCAL TIME` stack as two centred lines under the rose and the second line runs into the channel's water edge at "TIME". The rose itself reads as a clock before it reads as a rose, which is the point, but the label gives it away as a caption.
**Change.** One line, `VAR 14h (2026)`, left-aligned to the ring at label-caps 19; drop `AUTHOR'S LOCAL TIME` (the colophon states it, and a chart's variation note never explains its timezone).

### 12. Night edges and one lost weight (dark page; approaches-night) — S
**What I see.** Night paper (#0F1A2B) and paper_log (#121C30) are within a few L* of GitHub dark; sheets 2, 4 and 5 have no neatline, so they float as edgeless slabs and sheet 5's rotated words hang in the void. On sheet 3 at night `SCRAPY HARBOR` is set in ink2 (#8894A6) where the day sheet sets it in ink, so the harbour name loses a step of hierarchy after dark.
**Change.** Either the shared neatline from finding 8, or a one-HAIR `hair` (#2A3A55) edge on the unframed night sheets. Set sea-name/place-land in `ink` on both editions.

## Overall
The sheets are the best thing on GitHub of their kind and the honesty discipline is complete. What keeps this from world class is not taste but finish and economy: four small overprints a stranger will catch, a hero whose argument is the thinnest line on it, and a page that states its figures, its titles and its sources three or four times each. Findings 1–3 are a day's work and would move J2, J8 and J9 together.
