# Round 5 memo: the student (19, CS, lives on a phone, never read a chart)

## 1. What a visitor needs to know about Ben

Ranked by what I check before I follow, star or DM.

1. **What he builds, in one line.** Answered, but in 9 px caps inside the picture. It should be the second thing my eye hits, not the sixth.
2. **Is he active right now or is this a dead account.** Not answered. Stats say Scrapy, rustmapper and Data_science_dev all have commits on 7 Oct 2026; Scrapy has 26 working days. That fact is nowhere.
3. **One thing I can try in 30 seconds.** Answered: `pip install rustmapper`, three phone screens down.
4. **Is there real code behind this.** Answered in the bullets: the 250 ms governor, the CRC32 write-ahead log, rendezvous hashing. Receipts.
5. **The two things to look at.** Answered: two links. Good.
6. **Does he have taste / is he funny.** Half. "I survey a web that is wrong about itself" is good. "sitemap.xml lies again" is the only funny thing on the sheet. The rest is costume.
7. **Anything I would screenshot and send to someone.** No. Nothing legible enough to crop on a phone.

## 2. What a real reference object in my field carries

What I use and trust: **Spotify Wrapped**, **Apple Maps in transit mode**, **the map screen in Breath of the Wild**, **the GitHub contribution graph**.

Why they help and do not cringe: one number per screen, from my own data, never explained. Wrapped's numbers are fine; its *voice* is the cringe. Transit maps are one line with stops; the blue dot pulses to say *you are here* and nobody needed that explained. Game maps use fog for where you have not been and dotted lines for a route, and never say "this is a map". Green squares: everyone reads them, no legend.

Chart conventions that read to me with no legend: blue = water, tan = land, dotted line = a route someone took, hatched edge = fog of war, pulsing dot = current position, a handwritten note = a human was here. A number in water I would guess means depth, so bigger = more.

Honest mappings:
- **Track with dated fixes = his year, repos placed where they started.** A track is literally positions with dates. Per-repo first-commit dates are sound. Works.
- **Current-position dot = the repo he touched last.** Works; answers item 2 with zero words.
- **Hatching past today = not surveyed yet.** Works only if it starts at 7 Oct 2026. The word "Unsurveyed", no.
- **Pencil note on the chart = a known gotcha.** "sitemap.xml lies again". Works; the one place a joke belongs.
- **Depth number = commit-days.** Borderline: reads as size, honest enough, but if the audit kills the totals, kill the numbers.
- **Forced:** lit buoys ("R '2' FL R 4s"), variation, tide heights, "IALA Region B", "Datum", "Edition", "Small corrections". None mean anything about him.

## 3. The proposal

**One image: his track.** A soft-blue sheet, no border decoration. A thin dashed line runs from 25 Sep 2025 (left on desk, top on phone) to 7 Oct 2026. Along it, a dot per repository at the month of its first commit, sized by commit-days (Scrapy 26 and rustmapper 22 big; game_engine, Wheel, Data-visualizer 8 small; the twelve under 7 days are pinpricks, no label). Real repo names, as on GitHub, no "I.", no "Bank". Only the two big dots get a second line: *rustmapper · sitemap crawler, Rust, on PyPI* and *Scrapy Harbor · crawl platform, Scrapy + Delta Lake*. At the end of the line, a filled dot with a halo that pulses every few seconds (the only motion; still under reduced-motion). Past it, light hatching to the edge, no word. One pencil note near rustmapper: *sitemap.xml lies again*. Top-left: **Ben Russell**, the thesis line, the role line at a readable size. Nothing else printed. No clock, compass, buoys or boat.

Desk (870 px): landscape, about 870 × 420, track horizontal, labels beside dots. Phone (390 px): portrait, about 390 × 560, track vertical down the left third, labels right at 13 px minimum, name stacked on top. Same data, rotated.

Build caveat: 17 repos show "last" = 2026-10-07, which looks like a bulk touch. Place the end dot by author commits in the last 30 days, not that field.

**Page under it:** the three links on one line. rustmapper, three bullets (governor, write-ahead log, seeds), `pip install` block directly under. Scrapy Harbor, three bullets. The four other repos as a plain list. The four rules under the heading "Notes", citations kept. The collapsed fifteen. Two phone screens, done.

## 4. Details and one-off words (max 5)

1. The pulsing dot at today. Every map app does it. No label.
2. *sitemap.xml lies again*, in pencil, next to rustmapper. One joke, said once.
3. The unmeasured figure (256–1,024 permits) set slanted in the text. A nerd notices.
4. Hatching that starts exactly at today, with no word on it.
5. One-off word: the collapsed section titled **Laid up** instead of "Below the waterline".

## 5. Kill list

- "SOUNDINGS IN COMMIT-DAYS": explains the unit, which explains the theme. If it looks like a shoe, do not say shoe.
- "CHART NO. 21 · EDITION 0.1.3 · IALA REGION B · DATUM: MAIN · SMALL CORRECTIONS": fine print on a parking ticket.
- "LIMIT OF SURVEY 2026" and "UNSURVEYED": his words, not smart.
- The two buoys and the boat: cosplay; on a phone the boat is a 6 px triangle. Not drawn well at 390 px.
- "Data Science Bank", "Profile Shoal", "Game Engine I.": renaming his projects to fit the costume.
- Numbers in the blobs (11, 8, 26, 358) and the twelve crosses along the bottom: numbers in blobs and plus signs with no names. "Kind of cool but lazy."
- The clock/compass with VAR 14h: a clock that says nothing.
- Text: "is the survey vessel", "is where a run is operated", "Other waters", "Notices to mariners", "Found a wrong depth?", and the "Survey log" with three commit totals (1,665 / 1,966 / 1,828). Each names the theme or prints a number he does not trust.
- Alt text "A boat sails in and anchors."

## 6. The two-second test

**v10 on the phone, two seconds:** a name, a beige old-map thing, blue blobs. Is this a game? Is he a sailor? No idea what he does. Top half is caps I skip; bottom half is blobs I cannot read.

**v10, thirty seconds:** I find the good line about the web. I skip six lines of small caps. I see "Game Engine I.", "Profile Shoal", "358", "UNSURVEYED" and file it as a fake antique map of something. If I pinch-zoom I find "CRAWL AND DATA INFRASTRUCTURE" and finally know. No screenshot; no clean crop holds together.

**The proposal, two seconds:** his name, one line that sounds like a person, one line across water with two big labelled dots and a pulse at the end. I know he builds crawlers and that he committed this week.

**Thirty seconds:** two project names, one on PyPI, the dot sizes, the pencil joke, and I am at `pip install rustmapper`. That is a follow.

**What makes me screenshot it:** it looks like my year in Wrapped but it is a map, it has a dot that is alive, and it never once tells me it is a map. That is the one I send with "look at this guy's readme".
