# 17 — Brand strategist: position, distinctive assets, memory

Brand strategist (Sharp's "be remembered", Neumeier's "be the only"). I read README.md, README.draft.md, STANDARDS, CHANGELIST and spec-hero; looked at page-day-full, hero-day-2x, approach-scrapy-day-2x, footer-night-2x; and at the GitHub bio and the names around the page, because the brand lives there too.

## 1. What is good

- **There is a position, and it is true.** "The web is wrong about itself; I survey what is off the chart" is a claim, not a description, and it rests on a fact a competitor cannot copy by adopting the font: rustmapper and go_go_go seed from CT logs and Common Crawl, which is how you find the subdomains nobody links to. The metaphor is grounded in the mechanism. That is the whole game and the draft has it.
- **One repeatable memory structure.** A stranger can say "his GitHub is a sea chart" in five words. Most portfolios cannot be described at all.
- **The Scrapy approach sheet** is the one place where asset and content are the same object (stages as marks, Grafana as the light). That is what owning a metaphor looks like.
- **The draft thesis** ("I survey a web that is wrong about itself") beats the current hero line, which is category wallpaper.

## 2. What is bad, ranked

1. **The most-seen brand line contradicts the page.** The GitHub bio reads "Scraping enthusiast and full stack developer." It appears on every hover card, PR and search result, far more often than the README. "Enthusiast" is a hobbyist word; "full stack" is the lane the page spends 5,000 pixels arguing against.
2. **The flagship has three names.** Rust-sitemap (repo), rustmapper (PyPI, prose), Rustmapper Shoal (chart). Memory needs one name on one asset. Worse, the spec names the product after a hazard. Chart grammar can justify it; the brand cannot.
3. **"Scrapy" is a collision, not a name.** The platform is called Scrapy and built on Scrapy, so the draft must hedge ("not the framework itself"). A name that forces a disclaimer is a cost paid every time it is said, and it is unsearchable.
4. **The personal asset is buried.** The boat at the waterfall is the only asset with a story that is Ben's (avatar, the "sail" in his handle). It sits in the footer, drawn as a different boat from the hero's, under a borrowed joke.
5. **The metaphor attaches to the name, not the competence.** A day later the stranger remembers "the chart guy", which files him as a designer. Every link from asset to competence must be literal (soundings = commits, marks = stages, course = crawl, limit of survey = the unlinked web). Where it is not (snake, "fair winds", dragons), the metaphor eats the person.
6. **Borrowed assets treated as owned.** Instrument Serif plus warm red on cream/navy is the 2024–25 portfolio uniform. Fine to use; not distinctive. The ownable assets are the chart grammar, the italic-numeral convention, the unsurveyed hatch and the boat. The page treats the font as the identity and the hatch as texture; it is the other way round.
7. **The accent means four things**: can, north point, cursor, sail, light. An accent is an asset only when it means one thing.

## 3. What needs to be done

- **Rewrite the bio to the position, under 160 characters**, and let it be the missing position line: "Crawl and data infrastructure, Python and Rust. The web is wrong about itself; I survey the part that isn't linked." Pin the two systems. Repo descriptions and the PyPI summary carry the same sentence.
- **One name for the vessel.** Rename Rust-sitemap to rustmapper (GitHub redirects). On the chart rustmapper is **the vessel, not a place**: the survey boat carries "rustmapper" as a hull label. The product is the instrument that pushes the edge back; drawing it as the hazard says the opposite.
- **Give the platform the chart's name.** "Scrapy Harbor" is a legitimate product name that acknowledges the framework honestly. Use it everywhere on the page and drop the hedge; renaming the repo is Ben's call.
- **One boat.** Redraw the hero, approach and footer boat as the avatar's boat in chart grammar. The footer scene is the avatar drawn as a chart. Avatar, hero and footer become a single asset seen three times.
- **Codify the accent**: accent = "lit" (lights, sail, cursor, north). Cans are orange by IALA convention and the legend says so; nothing else is.
- **Thesis stays metaphor, lane goes literal.** Hero: "I survey a web that is wrong about itself." Cartouche subtitle: "Crawl and data infrastructure · Python and Rust." Claim and proof in one block is the brand.

## 4. Improvements and ideas

1. **A mark, not just a chart (bold).** Make the unsurveyed hatch his cartographer's stamp: a 24 px hatched square with a broken neat-line, in the colophon, in each flagship repo's README header, as the PyPI logo. No other portfolio has it, it encodes the position, and it travels where the page cannot.
2. **Make the page a series.** It is already "Chart No. 24 · Edition 0.1.3 · Corrected through Notice 5". Keep previous editions in `assets/editions/` and a public, dated Notices list. The brand demonstrates "keep the log" on itself, and the notice count becomes the proof of time the hiring manager said was missing.
3. **A ten-word test in the build.** Assert that the bio, the hero alt, the first 160 characters of README prose and the PyPI summary each contain "web", "survey" or "crawl", and the lane. Positioning rot becomes a build failure, like a missing font.
4. **Taglines that are claims**, ranked: (1) I survey a web that is wrong about itself. (2) The sitemap is not the site. (3) Most of the web isn't linked to. I crawl that part. (4) Sitemaps lie. I take soundings. (5) I chart the web beyond its sitemap. Reject every "I build X that Y": it describes, it does not claim.
5. **Never do.** Never explain the trick (the compass line is the one allowed exception). Never hedge inside the artwork; honesty is a convention (italic), not a disclaimer. Never borrow a joke the word "nautical" would hand to anyone. Never add a nautical word with no literal referent in the work. Never let an asset change form between sheets; that is how assets stop being assets. Never change the font to chase distinctiveness; it lives in the grammar, not the glyphs.

## 5. What the page says, and what it should say

Now the page says: a developer with unusually good taste, fond of the sea, who builds crawlers and is a little pleased with his chart. The memory it leaves is "designer", and the bio outside the page says "hobbyist". It should say, from every touchpoint at once: a crawl and data-infrastructure engineer whose claim is that the web is wrong about itself, who has a named vessel that proves it (rustmapper, on PyPI, seeded from CT logs and Common Crawl) and a named harbor where the fleet is run, and whose care for the surface is the same care he brings to the system. The chart is the proof of the claim, the boat is his, and a stranger a day later says "the one who surveys the unlinked web" before "the one with the map".

## 6. Five lines

1. Rewrite the GitHub bio to the position (no "enthusiast", no "full stack"); it is seen more than the README and currently contradicts it.
2. One name per thing: rename Rust-sitemap to rustmapper; make rustmapper the vessel on the chart, never a shoal; settle "Scrapy Harbor" as the platform's name and drop the hedge.
3. One boat: the avatar's boat, drawn in chart grammar, on hero, approaches and footer; the footer is the avatar as a chart.
4. Thesis stays metaphor ("I survey a web that is wrong about itself"); the cartouche lane goes literal ("Crawl and data infrastructure · Python and Rust"); the accent means "lit" and nothing else.
5. Own the hatch: the unsurveyed square becomes his mark on colophon, repo headers and PyPI, and the page keeps its editions and notices so the chart number records time.
