# 36 — Owner's advocate · re-crit round 2 (final build)

Judged from the regenerated `<qa>` (readme/, sheets/, crops/, frames/, check.md, perf-stdout.txt), README.md and chart.toml. Round 1 scored 28 and failed the floor.

## Scores

| # | Was | Now | Evidence |
|---|---|---|---|
| J1 | 3 | 3 | Thesis once, hero + alt (readme-light y≈300); intro prose still opens "Most of what I build is survey work." |
| J2 | 3 | 3 | Hero alone still argues the edge: soundings thin east, LIMIT OF SURVEY 2026, hatched UNSURVEYED, rose at VAR 14h. |
| J3 | 2 | 3 | Six silhouettes now on the page: footer renders at the bottom of readme-light (y≈5000), "The chart ends here. The web doesn't.", last block of the file. |
| J4 | 3 | 3 | Cartouche SOUNDINGS IN COMMITS · DATUM: MAIN · IALA REGION B; approaches nuns red/starboard, cans green/port (readme-light y≈1600). |
| J5 | 2 | 3 | approaches-phone.png now carries a 12-row SYMBOLS legend (y≈1680–1900) with "upright figures measured · sloping not"; desktop legend strip unchanged. |
| J6 | 3 | 3 | 21 / HW 358 wk of 5 Oct / VAR 14h / 0.1.3 / 169–173 / 1,665·1,966·1,828 all trace to stats.json; footer "9 notices" = 5 toml + 4 releases. |
| J7 | 1 | 2 | Log sign-off now "Log closed 1550 · computed from settings · unsigned" (log-day y≈240), lede says "computed from the crawler's own settings, not yet measured", alt says "unsigned". Still: "Python and Rust most days" over a sheet that bolds only TypeScript (readme-light y≈4560 vs 4740). |
| J8 | 2 | 2 | Hero strip: name+thesis+cartouche at t=0, boat anchored by 24 s, sheet still at 95/600 s; footer strip boat reaches the limit by 84.5 s and holds. perf-stdout: PERF-MOVING hero 35.7 ms/frame while moving, cap 8. |
| J9 | 2 | 2 | "Five principles" now heads exactly five, with "Notices 6–9, editions:" as a sub-line (y≈3410) — coherent. The nightly mechanism is still said three ways (caption, "Figures correct themselves nightly.", "watch kept by cron"). |
| J10 | 2 | 2 | Table reads in <10 s; links present. `[position] text = ""` still (check.md POSITION-EMPTY); empty header row still renders above the table (y≈720). |
| J11 | 3 | 3 | Night: navy paper, cream ink, R"2"/G"1" halos brightest (hero-entrance-night.png); footer-night sail is the one warm thing on the strip. |
| J12 | 3 | 3 | Footer now shows "14 · good holding", soundings 9 8 7 5 4 3, "Obstn rep. 2026 (PA)" (crops/footer.png); Colophon Variation and Figures bullets restored so VAR 14h and italics resolve for a prose reader. |

**J-total: 32 / 36** (was 28). Clears the floor: ≥ 30 and J7 ≥ 2.

## Round-1 defects

**Fixed**
1. Footer swallowed by Colophon — fixed. `_PICTURE_RE` is now line-anchored (`^<picture>`), Colophon has Type/Editions/Motion/Variation/Figures/Build/License, `</details>` closes, footer `<picture>` is the last block and renders in both editions. *Partial:* check.py still has no `<details>`-balance / footer-last / picture-inside-details rule (grep finds none), so the regression is guarded only by the regex.
2. Log asserted a run and Ben signed it — fixed. Sheet closes "computed from settings · unsigned", no *B.S.R.*; lede names the source and the upright-on-measurement promise in one sentence; alt says "computed from settings, unsigned". (log.json still carries `signoff.initials: "B.S.R."` but the sheet gates it off.)
3. "Five principles" over nine — fixed by demotion rather than regrouping: five numbered principles, releases as one `<sub>` line "Notices 6–9, editions", N = 9 on hero, footer and footer-phone, "see Notices 1–5" on approaches now literally true.
- Also-noted (b) instruments phone: now a real three-row LEAD/LOG/LOOKOUT list (instruments-phone.png), not a bare folio.
- Also-noted (e) approaches phone legend: present.
- Also-noted (d) BOUNDS-TEXTURE: five collisions down to one (`15₂`/`108₄`, 18 px, still a warn).

**Not fixed**
4. "Python and Rust most days; … when the work asks for them" (Instruments lede) against sheet 5's "bold · underway this quarter (1 of 21)" = TypeScript; alt still "The daily driver in bold". Same fix as round 1, cost S.
5. Hero imprint still "SUPERINTENDENCE: BUILD_ASSETS.PY" (hero-day y≈620, both editions); the only superintendence on the page is a script. "Figures correct themselves nightly." still opens the Notices lede alongside the caption. Cost S.
- Also-noted (a) empty `<thead>` row over the at-a-glance table (readme-light y≈720). S.
- Also-noted (c) "chart number is the public repository count" vs 24-vs-21 — not verifiable from the snapshot; still owed a live check.
- POSITION-EMPTY remains Ben's to fill.

## New defect
- **Phone log drops the source clause.** log-phone.png closes "Log closed *1550* · unsigned" — "computed from settings" is cut for width, so a phone reader has only italics and "unsigned" to tell them the run never happened; the lede above it does say so, but the sheet should carry it too ("1550 · computed · unsigned" fits). S.
- **PERF-MOVING** on hero-day (35.7 ms/frame moving, cap 8; perf-stdout.txt) is new in this snapshot and would be a dropped-frame sail-in on a laptop; MASTERPLAN budget question, not a copy one. M.

## Five-second read
**870 px, day.** Same as round 1 and still right: a very large serif name, an italic thesis, a cream chart of blue-ringed islands with soundings, a compass — a person who charts something he owns. Field arrives in seconds 6–10 from the table. **360 px.** Name, thesis in two lines, rose, Profile Shoal, Scrapy Harbor with two lit marks, and the cartouche legible with the field on it; then the Instruments strip now says something (LEAD/LOG/LOOKOUT lists) and the phone footer carries the exit line, the boat at the limit and "14 · good holding". **Night.** Designed, not inverted; name brightest text, the two lights brightest things, footer sail the one warm mark. **What it says about the person.** Careful, with a thesis, prints the unflattering figures (typical week 0; HW on a browser-game week) and now also prints "unsigned" over the one sheet he did not observe. The page finally ends where the arc was built to end. What still reads as the machine's page rather than his: the script's name on the imprint and the lede that says "most days" when the chart says otherwise.

---
J-total 32 (was 28); passes the floor.
Fixed: defects 1, 2, 3; also-noted (b), (e), (d) reduced to one warn.
Still open: defect 4 (most days / daily driver), defect 5 (superintendence imprint, nightly said 3×), (a) empty table header, (c) 24-vs-21 live check, POSITION-EMPTY, check.py details/footer-last gate from fix 1(c).
New: log-phone drops "computed from settings"; PERF-MOVING hero 35.7 ms/frame vs 8 cap.
