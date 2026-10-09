# Round 5 review · data

## 1. Verdict

**SHIP AFTER FIXES.** The image no longer says it's a chart and the 358 is gone. But two encodings still make the work look bigger than it was, and one printed figure has no denominator.

## 2. What works

- Sweep days are out of every shape. Scrapy (25 commit-days) and rustmapper (19) now rank first and second, which is true.
- Every facts-line figure matches stats.json, the audit's definitions and my clone counts (3 / 1 / 16k; 257 / 5 / 69k; CI = push runs on main). Zero commit totals.
- Nothing names the metaphor. `DATUM: MAIN` and `EASTERN TIME` are true and quiet.

## 3. What must change

1. **Bank length encodes "at least one day that month".** In page-desk-1, rustmapper's May and Aug 2026 are one commit-day each but are drawn a month long. DATA-VISUALIZER's 5 days read as two months. Fix: bin by ISO week (about 6 px a week at 390), set half-thickness ∝ non-sweep commit-days in the week (0–7), and draw a lone day as a one-week bead.
2. **"63 commits carry an AI co-author trailer" (page-desk-2) has no denominator and hides most of the story.** The 63 counts all days, sweeps included, inside a sentence that says sweeps are excluded. It also leaves out the 297 commits agents authored outright (`Claude` 172, `google-labs-jules[bot]` 125). Fix: "The chart leaves out sweep days (9–10 Nov 2025, 1 and 7 Oct 2026). Of 2,032 commits authored as me, 63 carry an AI co-author trailer; agents authored 297 more, not counted as mine."
3. **The rows don't add up.** The title says 21 REPOSITORIES, but 7 rows + "9 MORE" is 16: five sweep-only repositories vanish without a word. The fourth row, BENJAMINSRUSSELL, is this page's own build, so the chart's fourth-biggest project is the chart. Fix: merge the profile repository into the last row and letter it `15 MORE` (6 + 15 = 21).
4. **Language tags depend on which API answered.** BENJAMINSRUSSELL has no tag in sheet-desk-day-870 and reads PYTHON in page-desk-1. DATA_SCIENCE_DEV and GAME_ENGINE are blank, because `language` comes from REST, which answers for three repositories. Fix: take each tag from `lines` (largest language at HEAD, present for all 21).
5. **It's tidy, not screenshot-worthy.** Two thirds of the right panel is bare paper with lumpy worms on it. Soundings are what make a chart worth reading, and here they are the data. Fix: at desk, print commit-days as an 11 px italic figure on the bank wherever the bin is ≥ 5; on the phone, print only each row's largest figure. Define them once in the fine print: `FIGURES: COMMIT-DAYS`.

## 4. The owner's test

**Two seconds, iPhone:** the name, the thesis, crawl and data infrastructure in Python and Rust, an old-looking sheet. Odd that it's a chart; good.

**Thirty seconds:** which projects he worked and when (a real gap Feb–Jul 2026), then what the two projects are built on, their tests and CI. Helpful knowledge; the facts lines are the most useful thing on the page.

**Layer without saying so:** yes. Nothing is cringe.

**Lazy:** no totals, no calendar.

**Dishonest:**
- By encoding: item 1.
- By omission: item 2.
- `Fl 15s` is a true period, but it is set at Oct 2025 on a time axis, which gives it a date it doesn't have. Put it at the right end of Scrapy's row.
- rustmapper's "last run passed 7 Oct · last worked 8 Aug" reads as a contradiction; item 2 defines sweeps before it.
