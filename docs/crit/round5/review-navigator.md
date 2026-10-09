# Round 5 review — navigator

## 1. Verdict

**SHIP AFTER FIXES.** It finally tells you about him without saying "ship", but it has no water on it, so it reads as a tidy Gantt chart on chart paper and nobody screenshots it.

## 2. What works

- **The light is right.** A magenta flare and `Fl 15s` on Scrapy, from a sha-cited `prometheus.yml`: the mark a sailor checks first, and it is true. Keep it.
- **The datum line is honest.** `AUTHOR'S COMMITS · DATUM: MAIN · SWEEP DAYS EXCLUDED · 9 OCT 2026 · EASTERN TIME`: what, against what, when. A real title block.
- **The page reads straight.** The headings are plain, and the toolchain gotcha sits under the install block, where a hazard note belongs.

## 3. What must change

1. **There is no sea.** In `sheet-desk-day-870` the banks are buff slivers about 10 px tall in rows 42 px apart. You cannot see the thickness, so each row reads as a bar. Fix: bank thickness = √(commit-days that month), scaled so the biggest month fills 0.8 of the row pitch (34 px desk, 28 px phone). Add a 6 px blue shallows band along every coastline (v10's shallows tint, plus a night variant). Buff land, blue shallows, white water: a chart in two seconds, no words.
2. **Names sit away from their land.** `DATA_SCIENCE_DEV` is lettered at the left edge and its land starts in December. Fix: put each name 4 px above the left end of its first bank, clamped inside the frame. `9 MORE` stays on the left.
3. **The sheet charts itself.** `BENJAMINSRUSSELL`, the fourth row, is mostly days spent building this README; a stranger reads it as a major project. Fix: `hero.exclude_named = ["BenjaminSRussell"]` merges it into the bottom row (`10 MORE`).
4. **The scale runs into the neatline.** On `sheet-phone-day-390` the axis ends `A S O`, with the `O` on the border, so it reads "SO". Fix: no partial-month label; a tick at the survey date lettered `9 OCT`, 12 px clear of the frame.
5. **The weights are inverted.** On the phone the role line has the same size and ink as the two datum lines, so three caps lines blur into fine print. Fix: role line at 30 sheet-px in ink, a 12 px gap, then the datum lines at 22 px in secondary ink. On the page, the `Built on … · 3 test files · …` line is the most useful fact there, but it is set as `<sub>` (`page-phone-2`). Make it body text. Cut the centred caption under the image (the role line, a third time). And reconcile: stats has 502 commits with any co-author trailer, 63 naming an agent; the foot line prints 63 unqualified. Write "agent-named", or the audit explains the 439.

## 4. The owner's test

**Two seconds, iPhone:** a name, his line, *crawl and data infrastructure, Python and Rust*, and rows of land on a dated scale with one blinking light. "Why is his README a chart?" comes through only faintly, because without blue it could be a timeline.

**Thirty seconds:** Scrapy and rustmapper are the real work; the rest are short bursts. rustmapper is on PyPI. Under each project you get its tests, workflows, lines of code and the last day it was worked on. Helpful knowledge.

**Cringe, lazy, dishonest:** nothing cringe, and nothing invented on the sheet. The empty paper is lazy, and the co-author figure is not yet reconciled. Fix 1 is the difference between tidy and worth a screenshot.
