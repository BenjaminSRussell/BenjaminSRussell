# 04 — Writer / editor: voice, rhythm, specificity, layering

## 1. First impression

The conceit is strong and the typography sells it; the copy is about 60% there and the rest is costume. Several of the best lines on the page are hidden in alt text and cartouche micro-type while the visible prose repeats itself three times and opens with "Hi, I'm Ben" under a 176-pixel "Ben Russell". The humor that lands is deadpan and in the form ("Wind light, visibility good. Nothing on fire."); the humor that doesn't is borrowed ("Here be dragons", "I'm told that's a mood", "thanks for reading this far").

## 2. What works

- "sitemaps are wrong about themselves": true, specific, funny, and the thesis of the whole page.
- "which is how you find the subdomains nobody links to": the only bullet that shows instead of tells.
- Earned chart language: "not for navigation" on the scale bar, "Surveyed 2024 – 2026", "because that is what the lateral marks are", "Log of the rustmapper".
- "No database, no Docker, no passwords." / "Display only, by design." / "Lands on a programming language." Dry and confident.
- The alt text "a waterfall it never quite reaches" is the best line about the avatar, and nobody will see it.

## 3. Problems, ranked by impact

**1. The page says the same thing three times.** "Drawn, not templated" is in the intro and again as the Colophon lede. "If the surface is confusing, the system underneath usually is too" (intro) is rule 5 is the Colophon's premise. "A harbor with the lights on" appears on Sheet 3, in the body, and in a bullet. "The view is best right before the drop" is in Off the clock *and* on the footer sheet.

**2. The hero tagline is the template the page claims not to be.** "I build crawlers that survive the open web, and the systems that make sense of what they bring back" is every developer README's sentence in italic serif; "make sense of" is vapor. The intro's "Crawlers that... Storage that... Instruments that..." is the same brand-deck tricolon, and "before it finds the rocks" is a cliché.

**3. Two rhythmic tics.** Tricolons: "Pages drift, encodings shoal, sitemaps..."; "sharp, exploratory, real code"; "the name, the copy and the palette". "X, not Y": "drawn, not templated" (×2), "operated rather than demoed", "version one, not the polish", "Raw before clean". A dozen is the rhythm readers now associate with machine prose.

**4. Forced verbs.** "Encodings shoal" and "keeps sailing into the same waters" fail the coffee test: nobody would say them aloud to a colleague. "Sitemaps are wrong about themselves" passes.

**5. "Here be dragons."** The most overused phrase in map-themed anything, and wrong for the image: dragons mark unsurveyed interior; the footer is an edge.

**6. Defensive honesty.** "all of it real code", "numbers illustrative, the package is real", "real typefaces". The page keeps swearing it isn't lying. Say it once, in the log, where it is a legitimate chart note.

**7. Register breaks.** "Hi, I'm Ben", "I'm told that's a mood", "daily driver", "golden rule", "slow and purposeful", "thanks for reading this far".

**8. "Notes to mariners" is the wrong term.** The real document is *Notices to Mariners*: periodic corrections you paste into a chart. That is exactly what five hard-won rules are, and the real word unlocks the layer (5.1).

**9. The log is a terminal, not a log.** The sheet promises a ship's log and delivers a shell session. A log has remarks. The closing line knows this; the body doesn't.

**10. Off the clock explains the avatar to death.** A boat about to go over a waterfall is already a complete sentence. "A reminder that... it pays to have checked the chart" turns it into a motivational poster.

**11. No spine.** The section order is chart-like, but the prose restarts the metaphor at each heading instead of advancing a thought, and the one personal note arrives after the Colophon.

## 4. What "months of team work" would look like in the copy

- Every nautical term is a real chart term used correctly (datum, notice, sounding, lateral mark, cartouche). Checkable against a NOAA chart.
- No idea appears twice: grep for "drawn, not templated", "lights on", "before the drop" returns one hit each.
- Every cartouche number means something verifiable (edition = README version; "corrected to Notice 5" = the five rules).
- No sentence starts "I build" or "I'm a". At most two tricolons and two "X, not Y" on the page.
- One understated closing line, and nothing after it.

## 5. Proposals

Layers of meaning: 5.1, 5.2, 5.3, 5.5. Second-look delight: 5.4, 5.6.

**5.1 Notices to Mariners as changelog.** Rename the section and set each rule as a numbered correction tied to the repo that taught it: "Notice 2 · Scrapy · Keep the log. Raw before clean." The rules become a confession that the chart was wrong first and was corrected; the cartouche picks up "Corrected to Notice 5".

**5.2 Soundings as confession.** The tide curve marks "high water". Mark "slack water" on the quietest stretch too. A panel that admits its low tide says more about the person than one that shows only the peak, and it is still just data.

**5.3 Make the cartouche numbers mean something.** "Chart No. 27" is arbitrary. Tie it to something true and label it ("8th edition"). Readers who notice get a second layer; nobody is lied to.

**5.4 Alt texts as the chart's marginalia.** Make every alt a dry chart note in voice; the people who inspect are the people he wants to impress.

**5.5 One line at the edge that reframes the page.** Replace "Here be dragons" and the explained avatar with a statement of scope: the chart is honest about where its survey stops.

**5.6 Make the log a log.** Keep the shell lines; add one remark entry in true log form so "Nothing on fire" is the second beat of a set-up joke, not a stranger at the bottom.

**5.7 Cut entirely.** "Hi, I'm Ben." · "Pages drift, encodings shoal," · "Instruments that show you where the vessel is before it finds the rocks." · the Colophon's "drawn, not templated" · "Some of it sharp, some of it exploratory, all of it real code." · "I'm told that's a mood." · "and purposeful" · the footer's "the view is best right before the drop" · "thanks for reading this far" · "depths in trusted rows" · "golden rule".

### Ten replacement lines, verbatim

1. Hero tagline, one line replacing two: **"I survey a web that is wrong about itself."**
   Puts the page's one great idea in the headline and kills "I build X that Y".

2. Cartouche micro-line, for "Soundings in rows": **"Soundings in commits · Datum: main"**
   Chart datum is a real term; `main` is the real branch. Two true meanings, no explanation.

3. Cartouche subtitle, for "Full-stack developer · scraping enthusiast": **"Full-stack developer · mostly crawlers, lately in Rust"**
   "Enthusiast" undersells 512-worker Rust; this states the real language mix as a direction.

4. Intro, replacing both paragraphs: **"Most of what I build is survey work on a web that is wrong about itself. The crawlers take the soundings. The storage keeps the raw log so any depth can be checked again. The dashboards say where the boat is while that still matters. I care how it looks for the same reason I care that it holds: a chart nobody can read is not a chart."**
   Thesis once, taste once, no greeting, no rocks; "surface is the system" is left to rule 5.

5. Approaches lede, for "One is the platform, the other is the engine": **"Two harbors. rustmapper goes out first and finds the coastline; Scrapy is where the fleet is run."**
   Says what each does rather than its category, in the true order of operations.

6. Section title and lede: **"Notices to mariners"** / **"Five corrections to this chart, written down so I stop making them."**
   The correct term, and rules become a changelog.

7. Rule 4: **"Parse, don't pattern-match. Never regex what a parser already understands."**
   Drops the strained "charts" and the "golden rule" cliché.

8. Other waters lede, for the tricolon: **"Shorter crossings."**
   Two words, in voice, no oath about realness.

9. Log entry before the final line: **"14:05   remarks   nothing to report"**
   The classic log phrase; "Nothing on fire" becomes a punchline instead of a lone wink.

10. Footer, for "Here be dragons." and its caption, with Off the clock cut to its first sentence: **"The chart ends here. The web doesn't."** / micro-caption **"surveyed to this line · beyond it, no data"**
    Restraint instead of cliché, honest about scope, and it explains the avatar without saying so.

Bonus, Colophon motion: **"SMIL only, and slow. The boat takes 48 seconds to cross the hero; you are not meant to wait for it."** True, and it tells the reader how to read the page.

## 6. What it says about him now vs what it should say

Now: a developer with real taste who found a good conceit and didn't trust it, so he explained it, repeated it, and borrowed the obvious jokes to be safe. The craft is in the system; the copy is still auditioning.

Should: someone who knows the chart vocabulary well enough to use each term exactly once, who lets "sitemaps are wrong about themselves" and "Nothing on fire" carry the humor, who writes alt text as carefully as headlines, and who can end a page with nine words and walk away. The design already says "expert". The copy should say "and he doesn't need you to notice".
