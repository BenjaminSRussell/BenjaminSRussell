# 34 — Philosopher / essayist: charting a territory that lies

I work on epistemology and the philosophy of representation (Korzybski, Borges, Harley's "Deconstructing the Map", Bowker and Star on classification). I read README.md, README.draft.md, the skeptic, cartographer and poet critiques, the hero spec and assets/stats.json, and looked at hero-day, footer-night and legend-night.

## 2. What is good

The thesis is a real philosophical position, not a slogan. "The web is wrong about itself" says: a site's self-description (sitemap, robots, link graph) and its behaviour diverge, and the only remedy is empirical: go and sound it. That is the epistemology of the hydrographic survey, which exists because mariners died trusting charts drawn from testimony. Crawl-as-survey is an identity, not a decoration, so chart grammar can carry argument here. Three conventions in the direction carry the argument honestly: upright versus italic numerals (measured versus illustrative), UNSURVEYED hatching at the margin (the chart confessing its silence, which Harley says maps never do), and "Corrected through Notice 5" (knowledge as a corrected series, not a fixed object). The seed sources are the deepest idea on the page: a sitemap is what a site says about itself; a Certificate Transparency log is what it did, recorded by a third party; Common Crawl is what others saw. Testimony, record and witness, drawn as a source diagram. Few profiles have a theory of knowledge; this one does.

## 3. What is bad, ranked

1. **The chart of a web that is wrong about itself is, right now, wrong about itself.** stats.json says `"seeded": true`. It holds two commit counts, 1,828 (GraphQL) and 1,868 (clones), and the sheet shows one. The brief says 24 public repos; the file holds 21, and the chart number depends on which. Thirteen repos share a `first` date of 2025-11-09 and a `last` of 2026-10-07, the survey date, so the surveyor's own wake may be reading as the territory's activity. The current hero prints "DEPTHS IN TRUSTED ROWS" over random soundings. The sin the thesis accuses the web of is committed on the sheet.
2. **Depth means two things.** On the hero a sounding is a commit count: how much he worked. On Approaches a sounding is a verified row: what the crawler checked. One sheet measures labour, the other knowledge, under one word. The page has not noticed the difference.
3. **The map contains its maker and does not know it.** The profile repo (169 commits) is a feature on the chart (Profile Shoal). The chart number counts repositories, so the chart counts itself. Royce's map of England containing a map of England; the best joke available, and unmade.
4. **The metaphor breaks on time and the break is unused.** A coast moves slowly, so charts are corrected by notice. The web moves nightly, so the sheet is redrawn nightly. Two kinds of correction are at work: of fact (automated, every morning) and of judgment (the five Notices, by hand). The draft blurs them into one word.
5. **Classification is read as value.** Area by commits makes a ten-day sprint (game_engine, 585) the largest feature while the shipped tool (rustmapper, 126) is a shoal. Bowker and Star: every classification hides the choice behind it. Area will be read as importance unless the choice is shown.
6. **"Not for navigation" is a souvenir disclaimer.** The italic convention and the datum already do its work.

## 4. What needs to be done

- **Show the two instruments.** Cartouche or soundings strip: "SOUNDINGS BY TWO INSTRUMENTS · GRAPHQL 1,828 · CLONE 1,868", or print the surveyed figure and footnote the other. Charts do this ("from surveys of 1931 and 1962"). A declared discrepancy is a credential; a hidden one is a lie.
- **Build check: no sheet ships while `seeded` is true.** The apologies left the artwork, so honesty must live in the build: fail, or render every sounding italic, while the cache is seeded. Verify the thirteen `last = today` dates and the repo count before the first real render.
- **Declare the unit per sheet.** Hero: SOUNDINGS IN COMMITS. Approaches: SOUNDINGS IN URLS. One line each; the conflict becomes a series convention.
- **Date the survey per area in the source diagram.** The diagram's job on a real chart is survey dates. Add them from stats.json: "A — rustmapper, Oct 2025 to date; D — game_engine, 4–14 Jan 2026, ten days". The sprint is then an honest fact, not an inflated feature.
- **One sentence for the colophon:** "The chart number includes this repository; the chart is one of the things it charts." The whole Borges in sixteen words; nothing after it.
- **One sentence for the rustmapper bullet** (replacing the clause the poet cut): "Sitemaps are what a site says about itself; certificate logs are what it did." Thesis and mechanism in one line.
- **Separate the two corrections in the Notices lede:** "Figures correct themselves nightly. These five I had to be told." Then the list.
- Drop "Not for navigation".

## 5. Improvements and high-level ideas

1. **A surveyor's ethics line, true to the code.** Surveying what nobody published for you (CT logs find subdomains the owner never linked) raises a consent question, and chart tradition answers it: the vessel slows in shoal water. rustmapper's adaptive throttling and go_go_go's per-host politeness are real. A note by the survey lines, "VESSEL REDUCES SPEED IN SHOAL WATER", says the ethics without a sermon. Claim robots.txt only if the code honours it; if it does not, that is the better fix.
2. **Make the nightly redraw visible as philosophy.** The edition date says: true as of a morning. Put the survey date where charts put it, below the neat line, so the footer's line means what it should: the chart ends because the survey stopped, not because the web does.
3. **Bold: the Profile Shoal carries the recursion.** Its sounding is its own commit count; a pencil note beside it: "this chart, surveyed from itself". The 46 beside it is checkable in the sidebar, which the narrative designer noticed. A reader who finds that one feature is the maker's own self-description, measured by the instrument he uses on the web, has understood the page: he applies the thesis to himself.
4. **Honesty as a legend entry with teeth.** Beside the upright/italic key: "Where two surveys disagree, the smaller figure is shown." Stated once, it reads as an engineering ethic.

## 6. What the page says about its maker

The renders say: a maker who loves the look of certainty and wrote "trusted rows" over numbers he had not measured. The direction says better: a person who holds that self-description is not evidence. What it should say, one sentence and one build check away, is that he applies the rule to himself: his own chart marks its unsurveyed margin, prints both instruments when they disagree, dates each survey, counts itself among the things it counts, and is redrawn every morning because the territory moved. A surveyor who surveys his own chart is the only kind whose chart of anything else you would trust.

## 7. Five most important lines

1. The chart of a web that is wrong about itself is currently wrong about itself: `seeded: true`, 1,828 vs 1,868 commits, 21 vs 24 repos, thirteen `last` dates equal to the survey date. Fail the build on `seeded`; show both instruments.
2. Depth means labour on the hero and knowledge on Approaches; declare the unit per sheet (COMMITS / URLS).
3. Add one colophon sentence: "The chart number includes this repository; the chart is one of the things it charts."
4. Date the survey per area in the source diagram from stats.json, so game_engine's ten-day sprint reads as a dated survey, not as the largest feature.
5. Separate correction of fact from correction of judgment: "Figures correct themselves nightly. These five I had to be told." Add "VESSEL REDUCES SPEED IN SHOAL WATER" only as far as the code makes it true.
