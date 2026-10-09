# Round 5 · information designer

One test: does the reader get the fact faster and surer because of the form, or is the form in the way. On v10 it is in the way, and I can say where.

## 1. What a visitor needs to know about Ben

1. What he builds: crawl and data infrastructure. Answered by the subtitle under the image. The image does not say it.
2. What you can use today: rustmapper on PyPI (0.1.3), Scrapy Harbor. Text answers; on the chart they are two blobs among nine.
3. Is he active now, and on what. Not answered. No time axis.
4. Languages: Python, Rust, then Swift, C. One text line answers it; the chart carries no language.
5. Evidence he is serious: the governor, the write-ahead log, the breakers. The bullets answer it; the chart carries none of it.
6. Where he works from: all 1,665 commits are US Eastern (tz offsets -0400/-0500). True, cheap, nowhere on the page.
7. How to reach him. Answered.
8. Whether the numbers can be trusted. Three totals in the survey line (1,665 / 1,966 / 1,828); the reader believes none.

## 2. What a real chart carries and why it helps

One scale. A hierarchy of ink: hazards heaviest, land next, soundings light, grid lightest. Encodings that need no legend because the convention is the legend. One title block, the only place that explains.

Honest mappings (convention and fact mean the same kind of thing):

- Date and limit of survey = the as-of line and a hairline at "today", hatched ground beyond. Keep, with only the date on it.
- Sloping figures for an unreliable sounding = a figure the sources disagree on (the 256–1,024 permits that README, PyPI and code give three ways). Already in chart.toml; the best idea in it.
- A sounding = effort in one unit: days he worked.
- An isolated-danger mark = a known gotcha ("pip builds from source and needs a Rust toolchain").
- A light's character, Fl 7d = the page redraws weekly. One periodic thing, one light.

Forced:

- Island, bank, shoal, vessel. Assigned by hand; nothing about Data_science_dev is "bank".
- Weekly commit counts as soundings along the course: wrong unit under a "commit-days" title line, and suspect totals.
- HW 7 Oct, 358. That day touches 18 of 21 repositories: a sweep, not work. Drawn as the deepest water, the chart lies with its own number.
- The boat. The one mark that names the theme.

Why v10 is dense in one corner and empty elsewhere. Area ∝ commit-days puts Scrapy at r ≈ 80 and the seven-day islands at r ≈ 41: the whole data range is one doubling of radius, so eight of nine features read the same size and are told apart only by a printed figure. The area channel carries nothing. The top right stacks eight label families (bank, course, soundings, buoys, HW, limit, "unsurveyed", pencil note) in about 200 × 250 px. The left 55 % is a title block of seven caps lines: one fact about him, six facts about the sheet. The bottom left is twelve identical crosses: 57 % of the repositories get zero information. On the phone the labels collide (Game Engine I. over Data Science Bank, URL Organizer I. over its own figure). The hours dial has angle but no magnitude scale: decoration.

## 3. The proposal

One sheet, one scale, one unit, no legend. Time runs along the sheet; one mark is one day he committed.

Desk, 870 × 360. Title block top left, 300 px wide: "Ben Russell", the thesis, the role line, then one line "ONE MARK = ONE DAY WITH COMMITS · SEP 2025 – OCT 2026 · US EASTERN", and the as-of date. That is the whole explanation.

Body, 540 px wide, running under the block: a time axis Sep 2025 to Oct 2026, month ticks lettered S O N D J F M A M J J A S O, years at Sep 2025 and Jan 2026. Nine rows, the repositories with seven or more commit-days, ordered by commit-days: Scrapy Harbor 26, rustmapper 22, Data Science Tycoon 11, this profile 9, game_engine 8, Data-visualizer 8, Wheel 8, FashionDB 7, ideal-url-organizer 7. Each row: real name at left in the sheet's small caps, a two-letter language tag in lighter ink (PY, RS, TS, C, JS), one 2 px tick per commit-day in sounding ink, the figure at the right edge in sounding figures. A tenth row, "12 more", with their ticks merged in the lightest ink. One hazard mark on the rustmapper row at 8 Nov 2025, a small filled triangle, "0.1.3 · PyPI". A hairline at 7 Oct 2026 full height, hatching to its right, the date at its foot. The 7 Oct sweep draws as one vertical run of ticks; until the audit rules on it, those ticks are hollow and each affected row's figure is printed sloping, because the sheet is not sure.

Phone, 390 wide. Title block on top, four lines. Rows stack: name and figure on one line, the strip beneath, 34 px per row; the axis compresses to 300 px, a month is 23 px, a day is 1 px. Nothing moves on either.

Under it, all existing text in its present order, with the survey line cut to one total and the date.

## 4. Details and one-off words

- Sloping figures where sources disagree.
- Hatched ground right of today, with only the date on it.
- The border's minute band: reads as a chart in a second, says nothing.
- "US Eastern" in the unit line. A sailor reads a time zone and nods.
- "Datum: main", once, in the title block. The one joke, and it is true.

## 5. Kill list

- Boat, anchor, course line, buoys and their characters: they name the theme ("don't show me ships").
- Weekly soundings and HW SWEEP 7 OCT 358: suspect totals, wrong unit, a batch day drawn as deepest water ("the data looks all over the place").
- "9 charted · 12 as rocks", "IALA Region B", "Chart no. 21 · Sheet 1 · Small corrections", "Unsurveyed": metadata about the sheet, not him; together they are the dense corner.
- Island, Bank, Shoal, "survey vessel", "where a run is operated", "Other waters", "Below the waterline", "Notices to mariners", "Found a wrong depth?": each tells you it is a shoe. "Notices" alone; "15 more repositories" alone.
- The hours dial, "VAR 14h": a histogram with no magnitude axis. Give it a scale or remove it.
- Three commit totals in the survey line: print one or none.
- The alt text "A boat sails in and anchors."

## 6. The two-second test

Two seconds, iPhone: a name, a line saying he surveys a web that is wrong about itself, and a sheet of ticks along a year that is obviously a working record, drawn like a chart. Thirty seconds: nine projects by name, which two he worked most, a dead stretch Feb to Jul 2026, one release on PyPI in Nov 2025, Python and Rust on the big rows, Eastern time, the date the sheet was drawn. Nothing told them it was nautical; they will think it anyway.
