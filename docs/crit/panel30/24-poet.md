# 24 — Poet / prose stylist: the sound of the sentences

I write poems and I write for designers; my ear is for cadence, for where a sentence is alive and where it is upholstery. I read README.md and README.draft.md aloud, read the alt texts and cartouche lines as a text of their own, and looked at hero-day-2x and footer-night-2x against the specs.

## 2. What is good

- The draft has learned the plain declarative. "The crawlers take the soundings." "Raw pages land in Delta Lake and stay raw." One stress each; the page breathes between them. The current README never breathes.
- "a dashboard says where the boat is **while that still matters**": the clause arrives late and turns the sentence.
- "**you are not meant to wait for it**" (colophon). It tells the reader how to read the page by refusing to ask for attention. Best sentence of prose on the page.
- "nothing to report" → "Nothing on fire." is set up and paid off in two lines; the spec gives it the only serif in the body. A change of voice is the typographic form of a joke landing.
- The alt texts have a secret structure: each ends on a short sentence with a verb of settling. "A boat sails out and back." "The curve draws in once and holds." "Types once; only the cursor keeps time."

## 3. What is bad, ranked

1. **The thesis is said twice in 200 pixels.** Hero: "I survey a web that is wrong about itself." Intro, first sentence: "survey work on a web that is wrong about itself." The best line on the page is spent before the eye leaves the fold.
2. **The footer says its one thing twice.** The serif line, then "surveyed to this line · beyond it, no data" in mono. At the edge of the chart, two lines is noise; one is a statement.
3. **The Notices have a fixed meter.** Bold rule / explaining sentence / italic "Entered from…", five times; by Notice 3 the reader hears the template. "Parse, don't pattern-match" is glossed three times on the page.
4. **Self-explanation survives.** "The title block reads 'Corrected through Notice 5' because of this list." Finding that and counting is a pleasure; being told is a lecture. The rustmapper bullet's "how you find the subdomains nobody links to" restates the intro's "appear in neither", and the intro's is the better music.
5. **Stacked hinges.** "Scrapy is the harbor the survey feeds, where the fleet is run": two relative clauses in nine words. "not the framework itself. It is where a run is operated": a disambiguation and a passive thud, both in the lede.
6. **Three nautical labels on one small section.** "Other waters / smaller work / Shorter crossings. / Below the waterline."
7. **"Chart" appears 13 times.** The images carry the conceit; each use after the fifth lowers the value of the first.
8. **Two alt endings are inventory, not line.** "Legend panel and source diagram in the corners." "Chart number repeated outside the rule." They break the poem the others are writing.

## 4. What needs to be done

- **Intro, first sentence:** "Most of what I build is survey work. The sitemap and the site disagree; the subdomains nobody links to appear in neither." Then the draft as written. The thesis phrase now lives only in the hero.
- **rustmapper bullet 3:** stop at "the Common Crawl index".
- **Approaches lede:** "rustmapper goes out first and finds the coastline. Scrapy is the harbor it reports to, where the fleet is run."
- **Scrapy lede:** "**Scrapy is the harbor:** a multi-stage crawler platform, built on the framework of that name, from which a run is operated." If "not the framework itself" must stay, set it as an italic note after the bullets.
- **Notices:** cut the lede's second sentence. Let one rule stand bare: "4. **Parse, don't pattern-match.** *Entered from ideal-url-organizer.*" The silence after the shortest rule is the loudest thing in the list.
- **Footer:** the serif line only; the mono caption is already in the alt.
- **Colophon, Variation:** "…turned so the busiest hour sits at north. That is the variation."
- **Alt endings:** approaches → "The soundings fill in behind the vessel." Instruments → "The daily driver in bold; the rest when asked." Cut "Shorter crossings."

### The thesis line

"I survey a web that is wrong about itself." Four rising beats with a weak "that is" that lets the line breathe before "wrong". Its one cost is "a web", where there is one web; the article is a hedge. Five alternates, same meaning, different music:

1. **"The web is wrong about itself. I go and check."** The second sentence is deliberately plain, and the plainness is the wit.
2. **"I chart a web that is wrong about itself."** Lighter verb; rhymes the system's own name.
3. **"Where the web is wrong about itself, I take the soundings."** Periodic; the sounding lands last. Two lines at 40px.
4. **"Surveyor of a web that is wrong about itself."** No "I": the cartouche register, as if the chart subtitled itself.
5. **"The web is wrong about itself. I measure where."** Shortest second beat; "where" is the whole job.

Keep the original or take (1), the only one that gets funnier the second time.

### The closing line

"The chart ends here. The web doesn't." Four stresses, then a falling trochee; the contraction is right, a person speaking and not a chart note. Three alternates:

1. **"Limit of survey. The web has none."** Colder; matches the hatching.
2. **"Surveyed to this line. Beyond it, the web."** Absorbs the caption; ends on the noun.
3. **"The chart ends here. The web was never going to."** Rueful and falling; better aloud, worse at 360px.

Keep the original. Delete the caption under it.

## 5. Improvements and ideas

- **The alt poem (bold).** Make the last sentence of every alt text a line of one poem printed nowhere. Read that way, the draft is already: *A boat sails out and back. / The curve draws in once and holds. / Legend panel and source diagram in the corners. / Types once; only the cursor keeps time. / Chart number repeated outside the rule. / The web doesn't.* Fix lines 3 and 5 and it is a poem about an instrument that works while no one watches. Add a build step that prints this concatenation, so whoever edits an alt text sees the poem they are editing.
- **The cartouche as the second poem.** CHART NO. 24 · EDITION 0.1.3 / SOUNDINGS IN COMMITS · DATUM: MAIN / IALA REGION B · CORRECTED THROUGH NOTICE 5 / SCALE OF DISCOVERED URLS · NOT FOR NAVIGATION / VAR 21h00 (2026) · ANNUAL CHANGE SEE COLOPHON / LIMIT OF SURVEY 2026 / UNSURVEYED. The middots are caesuras; each line has a literal half and a half that is true about him. Rule: no cartouche line may be a label only. "DATUM: MAIN" is the model; the current "RUSTMAPPER ON PYPI · SCRAPY PLATFORM" is a label and is rightly gone.
- **Date the Notices from data.** stats.json has first-commit dates per repo. "Entered from Scrapy, 2025-02" is true provenance in chart form and breaks the meter without a word of gloss.
- **Ration "chart"** to headings, colophon and footer; target seven.
- **Dare the two-sentence intro.** "The sitemap and the site disagree, and the subdomains nobody links to appear in neither. Most of what I build goes and looks." Hero has the thesis, Approaches the mechanism, Notices the values, colophon the taste; the intro is the only place that says all four again. If the hiring manager vetoes it, §4's version is the floor.

## 6. What the page says about its maker

Now: someone with a real ear who has just found it and keeps checking the mirror. The best lines are short and unexplained; the worst are the sentences after them that make sure you noticed. It should say: a person who can put down one true sentence and leave, who trusts a chart to be read the way charts are read, slowly and by the few who need them. The images have learned restraint. The prose is one cut away: say the thesis once, end the footer on one line, let one Notice stand bare, and let the alt texts finish the poem they have started.

## 7. Five most important lines

1. "Wrong about itself" appears once on the page, in the hero; strike it from the intro's first sentence (replacement in §4).
2. The footer carries one line, "The chart ends here. The web doesn't."; the mono caption goes to the alt text only.
3. Break the Notices' meter: cut the lede's second sentence; set Notice 4 as the bare rule plus provenance, no gloss.
4. Make the last sentence of each alt text a line of one hidden poem; rewrite the approaches and instruments endings and print the concatenation as a build check.
5. Unstack the Approaches ledes: "rustmapper goes out first and finds the coastline. Scrapy is the harbor it reports to, where the fleet is run."
