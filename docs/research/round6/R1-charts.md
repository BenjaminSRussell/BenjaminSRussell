# R1. What each element on a real chart is for

Round 6 research, 9 Oct 2026. The question: what is each part of a nautical chart, harbour plan, chartlet or approach
chart actually for, how do navigators use them, and what do charts leave out on purpose? Then: what does that mean for
the first image on Ben's profile? The test throughout is the owner's goal: every map, and every element in it, has to
have a real purpose, rather than being a reason found after the fact.

"Read" means I opened the document and quoted from its text. "Abstract" means I worked from the abstract, catalogue
record or a reliable summary only. Project facts come from the clones in
`/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/clones/` and from `assets/stats.json`.

---

## Sources

### Chart standards and official guides
1. *U.S. Chart No. 1: Symbols, Abbreviations and Terms used on Paper and Electronic Navigational Charts*, 13th ed.
   NOAA and NGA, 2019. https://nauticalcharts.noaa.gov/publications/docs/us-chart-1/ChartNo1.pdf (read: introduction,
   "Information on selected chart features", Section A schematic, ECDIS depth pages)
2. *The American Practical Navigator* (Bowditch), Pub. 9, Vol. 1, Ch. 4 "Nautical Charts". NGA, 2017.
   https://thenauticalalmanac.com/2017_Bowditch-_American_Practical_Navigator/Volume-_1/03-%20Part%201-%20Fundamentals/Chapter%204-%20Nautical%20Charts.pdf (read)
3. Bowditch, Ch. 5 "ECDIS: Electronic Chart Display and Information Systems". NGA, 2017. Same site, Part 1. (read)
4. Bowditch, Part 2 "Piloting" (Ch. 7 Short-Range Aids to Navigation; Ch. 10 Piloting). NGA, 2017.
   https://thenauticalalmanac.com/2017_Bowditch-_American_Practical_Navigator/Volume-_1/04-%20Part%202-%20Piloting/Part%202-%20Piloting.pdf (read: §713, §718–720, §1002)
5. Bowditch, Ch. 27 "Navigation Processes", §2707 The Passage Plan. NGA, 2017. Same site, Part 7. (read)
6. IMO Resolution A.893(21), *Guidelines for Voyage Planning*. IMO, 1999. French text read at
   https://ppa.gc.ca/standard/pilotage/2018-07/IMO%20A.893.pdf ; English at
   https://fms.maritime.edu:8452/assets/images/IMO_Resolution_A.893(21).pdf (read, §1–3)
7. IHO S-4, *Regulations for International (INT) Charts and Chart Specifications of the IHO*, Ed. 4.9.0. IHO, March 2021.
   https://iho.int/uploads/user/pubs/standards/s-4/S4_V4-9-0_March_2021.pdf (read: B-100 purpose, generalization
   section, leading and clearing lines, compass roses, insets; the PDF uses shifted font encodings, decoded locally)
8. IHO S-67, *Mariners' Guide to Accuracy of Depth Information in Electronic Navigational Charts*, Ed. 1.0.0. IHO, 2020.
   https://iho.int/uploads/user/pubs/standards/S-67/S-67%20Ed%201.0.0%20Mariners%20Guide%20to%20Accuracy%20of%20Depth%20Information%20in%20an%20ENC_EN.pdf (read)
9. IHO S-52, *Specifications for Chart Content and Display Aspects of ECDIS*, Ed. 6.1.1. IHO, 2015.
   https://iho.int/uploads/user/pubs/standards/s-52/S-52%20Edition%206.1.1%20-%20June%202015.pdf (read: §1.4, §2.1–2.2)
10. "ENC Display Modes" (summary of S-52 display categories). Starpath School of Navigation, n.d.
    https://www.starpath.com/ENC/ENC_Display_Modes.pdf (read)
11. IHO Circular Letter 58/2013 on S-4 B-410 sounding selection ("shoal-biased", triangular selection). IHO, 2013.
    https://legacy.iho.int/mtg_docs/circular_letters/english/2013/CL58e.pdf (abstract)
12. "IALA Buoyage System". Trinity House, 2016. https://trinityhouse.co.uk/mariners-information/navigation-buoys/iala-buoyage-system (read)
13. *Symbols and Abbreviations used on ADMIRALTY Paper Charts* (NP5011, INT 1), 8th ed. UKHO, 2020. Listing:
    https://www.stanfords.co.uk/np5011-symbols-and-abbreviations-used-on-admiralty-charts-8th-edition-9780707746210 (abstract)
14. *Chart No. 1 / Carte no 1*. Canadian Hydrographic Service, 2019.
    https://waves-vagues.dfo-mpo.gc.ca/Library/chs-shc-chart1-carte1-2019-41033954.pdf (abstract: INT 1 adopted, lettered sections)
15. "Keeping ADMIRALTY Leisure Charts up to date". UKHO, n.d.
    https://msi.admiralty.co.uk/nms/leisure/Keeping%20ADMIRALTY%20Leisure%20Charts%20up-to-date.pdf (read)
16. "Notices to Mariners: blocks". Netherlands Hydrographic Service, n.d. https://english.defensie.nl/topics/notices-to-mariners/blocks (abstract)
17. *United States Coast Pilot 4*, Ch. 1. NOAA Office of Coast Survey, current ed.
    https://nauticalcharts.noaa.gov/publications/coast-pilot/files/cp4/CPB4_C01_WEB.pdf (read, opening page)

### Practice: pilotage and passage planning
18. B. Meakins, "5 hand-bearing pilotage tips". *Practical Boat Owner*, 2015.
    https://www.pbo.co.uk/seamanship/5-tips-for-using-bearings-and-transits-20914 (read)
19. J. Stevens (via C. Beeson), "10 classic pilotage mistakes". *Yachting Monthly*, 2015.
    https://www.yachtingmonthly.com/sailing-skills/10-classic-pilotage-mistakes-in-navigation-31890 (read)
20. "How to write a pilotage plan". Classic Sailing (RYA training centre), n.d.
    https://classic-sailing.com/article/how-write-pilotage-plan-skipper-skills/ (abstract)
21. "Pilotage" guide. Sailtrain, n.d. https://sailtrain.org.uk/?p=1629 (abstract)
22. Passage-plan minimum contents (no-go areas, margins of safety per leg, abort points). The Shipowners' Club, n.d.
    https://shipownersclub.com/generate_pdf/697/6224 (abstract; server returned 503 on fetch)
23. MAIB investigation annexes, *Berit* (passage planning). UK Government, n.d.
    https://assets.publishing.service.gov.uk/media/547c7079ed915d4c0d0000a3/Berit_Annexes.pdf (abstract)
24. "Light characteristic". Wikipedia, current. https://en.wikipedia.org/wiki/Light_characteristic (abstract; used only for notation)
25. Reeds Nautical Almanac harbour chartlets (orientation, "not to be used for navigation"). Bloomsbury, annual; secondary
    report https://crm.avenza.com/book/browse/fetch.php/Rya%20Training%20Almanac.pdf (abstract, weak)

### Cartography and generalisation
26. F. Töpfer and W. Pillewizer, "The Principles of Selection". *The Cartographic Journal* 3(1), 1966. As discussed in
    B. Jiang, X. Liu, T. Jia, "Scaling of geographic space as a universal rule for map generalization", 2013,
    https://arxiv.org/pdf/1102.1561 (read: Jiang; Töpfer via Jiang)
27. R. McMaster and K. S. Shea, *Generalization in Digital Cartography*. Association of American Geographers, 1992.
    Summary: https://en.wikipedia.org/wiki/Cartographic_generalization (abstract)
28. M. Monmonier, *How to Lie with Maps*, 3rd ed. University of Chicago Press, 2018 (1st ed. 1991).
    https://www.press.uChicago.edu/dam/ucp/books/pdf/course_intro/978-0-226-43592-3_course_intro.pdf (abstract)
29. A. M. MacEachren, *How Maps Work: Representation, Visualization, and Design*. Guilford, 1995.
    https://serc.carleton.edu/resources/1051.html (abstract)
30. J. Bertin, *Semiology of Graphics* (1967; English 1983). Summary of visual variables: Axis Maps,
    https://axismaps.com/guide/visual-variables (abstract)

### Maps of things that are not places
31. D. R. Montello, S. I. Fabrikant, M. Ruocco, R. S. Middleton, "Testing the First Law of Cognitive Geography on
    Point-Display Spatializations". COSIT 2003, LNCS 2825. https://user.geo.uzh.ch/sfabri/pubs/montello_etal_cosit03.pdf (read)
32. S. I. Fabrikant, D. R. Montello, D. M. Mark, "The Distance-Similarity Metaphor in Region-Display Spatializations".
    *IEEE Computer Graphics and Applications* 26(4), 2006, doi:10.1109/MCG.2006.90 (abstract)
33. A. Kuhn, P. Loretan, O. Nierstrasz, "Consistent Layout for Thematic Software Maps". WCRE 2008.
    https://scg.unibe.ch/assets/archive/papers/Kuhn08bSoftwareMap.pdf (read)
34. A. Kuhn, D. Erni, P. Loretan, O. Nierstrasz, "Software Cartography: Thematic Software Visualization with Consistent
    Layout". *J. Software Maintenance and Evolution* 22(3), 2010. https://boris.unibe.ch/4952 (abstract)
35. A. Skupin, "A Cartographic Approach to Visualizing Conference Abstracts". *IEEE CG&A* 22(1), 2002.
    https://geog.sdsu.edu/People/Pages/skupin/research/pubs/IEEECGA2002.pdf (read)
36. A. Kashcha (anvaka), "Map of GitHub", README. 2023, rev. May 2025. https://raw.githubusercontent.com/anvaka/map-of-github/main/README.md (read)

### Perception of graphics
37. W. S. Cleveland and R. McGill, "Graphical Perception: Theory, Experimentation, and Application to the Development of
    Graphical Methods". *JASA* 79(387), 1984. Summary: https://info3312.infosci.cornell.edu/ae/graphical-perception.html (abstract)
38. J. Heer and M. Bostock, "Crowdsourcing Graphical Perception: Using Mechanical Turk to Assess Visualization Design".
    CHI 2010. https://homes.cs.washington.edu/~jheer/files/2010-MTurk-CHI.pdf (read)
39. E. Tufte, *The Visual Display of Quantitative Information*. Graphics Press, 1983. Summary:
    https://data.europa.eu/apps/data-visualisation-guide/chart-junk-and-data-ink-origins (abstract)

### The projects themselves (clones, read-only)
40. `Scrapy/README.md` (Quick Start note on `Scraping_project/`, #334; spider names, #489) and
    `Scrapy/Scraping_project/monitoring/prometheus.yml`, `.../k8s/helm/scraping-pipeline/values.yaml` and
    `templates/prometheus-statefulset.yaml` (scrape intervals).
41. `Rust-sitemap/README.md` (pip package versus CLI binary), `pyproject.toml` (version 0.1.3), commit
    "Export crawl JSONL to Parquet/Delta for Scrapy handoff (#33) (#68)", 2026-10-07.
42. `ideal-url-organizer/README.md`, section "Handoff: seed export for Scrapy / Rust-sitemap".
43. `Data-visualizer/README.md` and `config/__init__.py` (PostgreSQL tables `urls`, `classifications`, `patterns`;
    crawl JSONL inputs `data/input/site_01.jsonl`).
44. `/home/user/wt-v12/assets/stats.json` (per-repository `commit_days`, `first`, `last`) and
    `docs/crit/round5/DECISIONS.md` (what round 5 chose and why).

That is 44 sources: 27 read in full or in the relevant sections, 17 from abstracts, listings or summaries.

---

## Findings

**F1. A chart has one job, and its content is chosen against that job.** S-4 opens Part B with it: "The primary purpose
of nautical charts is to provide the information required to enable the mariner to plan and execute safe navigation."
It goes on: the mariner needs "appropriate, relevant, accurate and unambiguous information", and "particular care must
be exercised to avoid ... situations where the mariner may be faced with too much information, chart clutter or
irrelevant information which causes confusion or distraction." On paper charts, "the cartographer's expertise in design
and selection, biased towards safety, is essential to achieve the required clarity" [7]. S-67 repeats the purpose
sentence word for word [8]. S-52 makes it a rule for screens: symbols must follow "the priority of prominence on the
display in proportion to importance to safety of navigation" and "should avoid any increase in clutter" [9]. So on a
chart, how prominent something is depends on how much it matters, not on how much of it there is.

**F2. Everything outside the drawing answers a question you have to settle before you trust the drawing.** Bowditch:
"The chart title block should be the first thing a navigator looks at." It gives the area, the scale and projection,
the vertical and horizontal datums, and the source notes or diagrams with survey dates [2]. Chart No. 1's Section A
schematic lists each marginal item along with what it is for. Explanatory notes are "to be read before using chart".
Cautionary notes give "information on particular features, to be read before using chart". The source diagram is there
because "navigators should be cautious where surveys are inadequate". The edition date and Notice to Mariners
corrections say how current the chart is. Adjoining-chart and larger-scale references say where to go next [1].
Soundings mean nothing until you know the datum, and "the sounding datum reference is stated in the chart title" [1].
The source diagram and zones of confidence exist because "a chart can be considered as a patchwork of individual
surveys". ZOC ratings let mariners "assess the associated level of risk to navigate in a particular area" [2, 8]. Each
of these elements tells you how far to trust the rest. None of them is there for looks.

**F3. A chart's layout is the space you actually travel through, and it is drawn to suit the trip.** Positions on a
chart are real positions. Where they are not exact, the chart says so: floating aids get "position approximate" circles
because "they move around their moorings" [2]. NOS small-craft "strip charts" are "not 'north-up' in presentation, but
are aligned with the waterway they depict, whatever its orientation is", and are placed "course-up in front of the
helmsman" [2]. The direction of the drawing follows the route the user will take.

**F4. Scale and chart type are chosen by task.** Sailing charts (smaller than 1:600,000) are for planning and open-sea
plotting: "only offshore soundings, principal navigational lights, outer buoys, and landmarks visible at considerable
distances are shown". General, coastal and harbour charts follow as the vessel nears land [2]. "The classification of a
chart is best determined by its purpose" [2]. Navigators "should use the largest scale chart available ... especially
when operating in the vicinity of hazards" [2], and the piloting checklist starts with "Choose the largest scale chart
available for the harbor approach" [4]. Insets and plans are "small charts with their own borders included within the
limits of a larger chart. A plan is a large scale inset ... for example a port plan" [7]. They exist where the main
scale cannot show what the user needs. Almanac chartlets orient the user and highlight the key features of a harbour,
and are to be used alongside a proper chart [25]. A colour block is a patch for a change too dense to draw by hand
[15, 16]. Every format is a choice of how much detail a particular moment needs.

**F5. Generalisation keeps what changes a decision, not what is biggest.** "As scale decreases, the amount of detail
which can be shown decreases also. Cartographers selectively decrease the detail in a process called generalization"
[2]. S-4 says generalisation is "the elimination of the least essential information", and that its purpose "is
primarily to avoid over-crowding charts where space is very limited". It also aims "to induce navigators ... to use
larger scale charts" [7]. For depths, the selection is shoal-biased: "least depths are shown first. This conservative
sounding pattern provides safety and ensures an uncluttered chart appearance" [2, 11], and rounding is always to the
shoaler side [11]. Even at its most extreme, "minimal depiction" still shows "a 'diagrammatic' picture of the length and
orientation of channels" [7]. When labels have to go, a light's height goes first, then its period. "Characteristic and
color will almost always be shown" [2]. Töpfer's radical law gives how many features survive a change of scale, but not
which ones [26]. Jiang's head/tail rule keeps the few large and drops the many small, and it describes generalisation of
geographic features, not of importance [26]. Monmonier's point is that every useful map tells "white lies" [28]. The
lie has to serve the reader's task, which is what McMaster and Shea's "why generalize" phase asks [27].

**F6. Colour on a chart is a code with fixed meanings.** Chart No. 1: "Color conveys the nature and importance of
features." Magenta marks elements "significant to marine navigation". "Shades of blue depict potential hazards to
navigation, typically shallow water and submerged obstructions." Deep water believed clear is white, and land is buff
[1]. On ECDIS the tints are recomputed for each ship: water shoaler than the safety contour is blue, deeper water is
off-white [1]. Blue on a chart does not mean "sea". It means "careful, shallow".

**F7. Depths matter relative to the reader's own draught.** ECDIS asks the mariner for a "safety depth" and a "safety
contour". Soundings at or shoaler than the safety depth turn black, deeper ones grey. The safety contour gets an "extra
thick line", and the system alarms if the planned track crosses it [1]. Paper practice does the same job by hand: "Mark
the Minimum Depth Contour ... Do this step before doing any other harbor navigation planning. Highlight this outline in
a bright color" [4]. A depth on its own tells you little. What matters is whether it is enough for your vessel.

**F8. A light's character exists so you can tell which light you are looking at.** "The light characteristic of an aid
to navigation is one of the methods for distinguishing one light signal from another and for conveying specific marine
safety information. For example, a quick flashing light in a lateral system typically indicates that the axis of the
waterway or channel changes direction" [4]. Bowditch warns that "a powerful, distant light may sometimes be confused
with a smaller closer light with similar characteristics", so "every light signal observed should be carefully
evaluated" [4]. The notation (Fl, Oc, Iso, period in seconds) is a lookup key into the Light List [1, 24]. A character
only works if it differs from the neighbouring lights and the reader knows how to decode it.

**F9. Buoys and beacons sit where a decision has to be made, and the mark itself tells you the decision.** Lateral marks
show "port and starboard hand sides of the route to be followed". Cardinal marks show where the best water is.
Isolated-danger marks sit on a small hazard with water all round. Safe-water marks show open water all round [12, 1].
Shape, colour, topmark and light rhythm are redundant on purpose, so the mark can still be read if the light is out or
the topmark is missing [12]. Chart No. 1 adds that prudent mariners "will not rely solely on any single aid" [1].

**F10. Leading lines, clearing lines and danger bearings turn a hazard into a simple test you can check.** S-4: "A
leading line is a straight line passing through two or more clearly defined objects (leading marks) along which a
vessel may approach safely." "A clearing line is a straight line on the chart that marks the boundary between a safe and
a dangerous area." When the marks are easy to identify, "no legend or symbol is necessary; only the bearing should be
charted along the line" [7]. Bowditch's danger bearing is labelled "NMT 074.0°T", which means you are safe as long as
the bearing stays below that value. Turn bearings mark "the track point at which the rudder must be put over" [4].
Yachtsmen use the same tools: two posts in line bring you in, "if the posts are not in line, head towards the front
marker", and a channel can be kept "between bearings of 235° and 250°" [18]. Each line is one rule that keeps you off
one hazard.

**F11. A passage plan, the reason the chart is consulted, runs berth to berth and lists the hazards, turns and fallback
points.** A.893 sets out four stages: appraisal, planning, execution, monitoring. The plan should be drawn "on charts of
an appropriate scale", showing the true track, "all areas of danger", turning points, the methods and frequency of
position fixing, and contingency plans to reach deep water or a port of refuge [6]. Bowditch calls the plan a shared
"mental model of how the entire voyage is to proceed ... from berth to berth" [5]. Industry checklists add no-go areas,
margins of safety for each leg, and abort points [22, 23]. Yachting guidance boils it down to "a detailed pilotage plan
with the bearing and distance to the next mark from each known position", including "every change of course", plus
"expected soundings" [19, 20, 21].

**F12. Even the furniture on a chart has a mechanical job.** S-4 places compass roses "so as to limit the sliding
distance of parallel rulers", and keeps them out of "the approaches to harbour entrances", "clear of chart folds and of
critical features (dangers, navigational aids, etc.)" [7]. On a real chart the compass rose is a tool for taking
bearings.

**F13. What charts leave out, and where it goes instead.** The Coast Pilot exists because "much of the content cannot
be shown graphically on the charts" [17]. In ECDIS, text "causes so much clutter, and is seldom vital for safe
navigation" that it sits under the "all other information" level [3]. The IMO display base is a "permanent display base
of essentials ... making the remaining information selectable" [3, 10]. Admiralty guidance tells leisure users to skip
corrections that do not matter to their vessel, such as a change to a very deep sounding [15]. One thing is never left
out: "no data", "unsurveyed" and "incompletely surveyed area" are in the display base that cannot be turned off [10].
On paper, "large blank areas or absence of depth contours generally indicate lack of soundings", so blank is a warning,
not a sign of safe water [2].

**F14. Planning views and glancing views are designed differently.** S-52: route planning is "viewed, without urgency,
from the normal screen viewing distance of about 70 cm, and so the display can contain considerable detail". Route
monitoring is "used for immediate decision-making ... viewed from a distance of several metres" and "should therefore
be planned to present only the immediately relevant information ... Text ... should be kept to a minimum" [9]. Split
screens pair "a north-up small-scale overview ... alongside a course-up large-scale view" [3].

**F15. When something that is not a place gets drawn as a map, readers still treat position as meaning.** Montello et
al. state a "first law of cognitive geography ... people believe closer things are more similar", and their
experiments "largely support" it [31]. Fabrikant et al. extend this to region displays [32]. Kuhn et al.: "since
software has no physical shape, there is no 'natural' mapping of software to a two-dimensional space. As a consequence
most visualizations tend to use a layout in which position and distance have no meaning". Their fix is to derive
position from something real, in their case shared vocabulary [33, 34]. Skupin says the map metaphor breaks down when
"labels are imbued with too little interpretable meaning", and that cartographic method helps only when the layout comes
from the content [35]. The Map of GitHub works because each dot's position comes from data: "Dots are close to each
other if they have a lot of common stargazers" [36]. Without such a basis, a map layout makes claims about the projects
that the data does not support.

**F16. Area is one of the weakest ways to show a number, and irregular shapes are worse.** Cleveland and McGill rank
position on a common scale first, then length, with area well below [37]. Heer and Bostock's replication finds that
people appear to "use 1D length comparisons to help estimate area" [38]. Bertin classes size as ordered, and only weakly
quantitative [30]. A blob whose area is set by days of activity is hard to compare by eye with its neighbour. Tufte's
test applies here too: ink that tells the reader nothing new is chartjunk [39].

**F17. The projects do have a real structure a reader can move through, and real hazards on the way in.** From the
clones:
- `ideal-url-organizer` exports seeds for the crawlers: "Handoff: seed export for Scrapy / Rust-sitemap ... Rust-sitemap:
  use the `url` field as `--start-url` entries. Scrapy: map `url`/`priority`/`labels` in seed_manager" [42].
- `Rust-sitemap` (published as `rustmapper`, version 0.1.3) gained "Export crawl JSONL to Parquet/Delta for Scrapy handoff
  (#33)" on 2026-10-07 [41]. Scrapy's pipeline ends in Delta Lake (README diagram: URLs, Scout Spider, Analysis,
  Summarization, Delta Lake) [40].
- `Data-visualizer` stores `urls`, `classifications` and `patterns` in PostgreSQL and reads crawl JSONL inputs [43].
  I did not check that it reads the crawlers' exact output schema.
- The documented hazards on the way in: "Always work from `Scraping_project/` ... From the clone root, `python start.py`
  fails" (#334); "Run spiders by their scrapy name (not the file name) ... `scrapy crawl scout` not `scrapy crawl
  scout_spider`" (#489) [40]; "`pip install rustmapper` installs the Python library. The command-line tool is the Rust
  binary `rust_sitemap`" [41].
- The current light "Fl 30s" on Scrapy has a basis: the `scrapy_app` job in the docker-compose `prometheus.yml` scrapes
  every 30 s. But the global default in the same file is 15 s, the Helm chart uses 15 s and 10 s, and round 5's
  decision text said 15 s [40, 44]. The figure depends on which deployment you look at. To most visitors it is also a
  code they cannot read.
- Sixteen of the 21 repositories show `last: 2026-10-07` in stats.json. That is the sweep day round 5 excluded from
  shapes, so "last commit" is not a safe freshness signal unless sweeps are removed [44].

---

## What this means for the owner's image and page

Each point below is tied to the goal: the picture has to teach a visitor something true and useful about Ben's projects,
faster than the text could, the way a chart teaches a navigator what they need to get somewhere. Each point has a test
that a reviewer can check against the rendered image.

**I1. Every element passes a written purpose test, or it goes.** For each mark, write down the single question it
answers for a visitor, and the source in the repositories that makes the answer true. "It makes it look like a chart"
does not count. That is the S-4 standard: appropriate, relevant, accurate, unambiguous, and no clutter (F1, F2, F12).
*Test:* the build carries a table, element → question → source file. Any element without a row fails.

**I2. Remove the islands.** They fail on every count in this research. They show weekly commit-days as irregular areas,
one of the least readable ways to show a number (F16). They surround activity with blue, which on a chart means danger
(F6). They are laid out on a strip, so readers will look for meaning in how close they are and find none (F15). And a
week of commits is not something a visitor travels through (F3). This is the owner's objection, "is it based on the size
of the project or how many commits? There's nothing about that teaches you anything", backed by the standards.
*Test:* ask a first-time viewer what one island means and what they would do differently because of it. Unless they can
answer both, the element fails.

**I3. If the image is a chart, its layout has to be a real route through his work, with every link sourced.** The repos
do have one (F17). URL seeds come from `ideal-url-organizer`. `Scrapy` or `rustmapper` crawl them. Output moves on as
JSONL/Parquet/Delta. `Data-visualizer` holds URLs, classifications and patterns. That is a chain a visitor or user moves
along, from a list of sites to a dashboard. It is the kind of structure Kuhn and Skupin say a software map needs, where
position comes from something real (F15). It is also what a strip chart does: drawn along the route, not north-up and
not time-up (F3). *Test:* every connection drawn cites a file and line in a clone (a handoff section, an export
command, a config input). If no file supports a link, it is not drawn. This replaces round 5's decision D1 that "time is
the honest geography".

**I4. Hazards are real, documented gotchas, each with the single rule that avoids it.** That is what a clearing line is:
one boundary with one simple check (F10), sitting where a decision has to be made (F9). The clones supply them: work
from `Scraping_project/` (#334), crawl by spider name `scout` (#489), and `pip install rustmapper` gives the library
while the CLI is `rust_sitemap` (F17). This is "helpful data" in the owner's sense: the thing a sailor would want marked.
*Test:* every hazard mark quotes text present in that repo's README or issue, and the rule is short enough to read at
390 px.

**I5. Each flagship gets one way in, drawn as the line you follow.** A leading line is the one safe approach (F10). For
a project, that is the shortest correct start: `pip install rustmapper` then `rustmapper crawl --start-url ...`;
`cd Scraping_project && scrapy crawl scout`. *Test:* each command runs on a fresh clone. A CI step or a script in
`scripts/check.py` could run it, and the line is not drawn unless it passes.

**I6. A light only stays if it identifies something and says a fact a visitor uses.** Light characters exist to tell one
light from another and to carry safety information (F8). "Fl 30s" fails on three counts: visitors cannot decode it, it
does not help them pick Scrapy out from anything, and the same repo says 10, 15 or 30 s depending on deployment (F17).
*Test:* a reviewer who does not know Prometheus can say what the mark tells them. If not, cut it or replace it with plain
words in the text.

**I7. Select by importance, not by volume.** Charts choose soundings that change a decision (least depths first) and
keep a light's character over its height. They do not keep whatever is largest (F5). Ranking rows by commit-days is
selection by volume. Choose what appears by whether a visitor would use or need it: the projects on the route, the
published package, the hazards. Name what was left out honestly in the text ("15 more" is fine; drawing them as faint
blobs is not). *Test:* for each project shown, state why a visitor needs it. "It had the most commit-days" is not an
answer.

**I8. Keep the fine-print line, and give it the job a title block has.** A title block tells the reader what is
measured, against what reference, from which sources, and as of when (F2). "Datum: main" is a true datum: every count is
taken on the main branch. The date and the time zone are true too. A short "source" note, saying which figures come
from clones and which from the API, is the honest version of a source diagram. It must not name the theme. *Test:*
every figure on the sheet can be traced to a definition in `docs/data/AUDIT.md`.

**I9. Use chart colours only with their chart meanings, or not at all.** Blue for caution (a hazard), magenta for the one
thing a visitor should act on (the way in), buff for what exists, white for clear water (F6). Decorative blue around
activity says the opposite of what it means. *Test:* list every colour in the SVG with its meaning. Any blue that does
not mark a caution fails.

**I10. The phone gets the monitoring view, the desk can get the planning view.** S-52 separates the glance view (only
what is needed right now, very little text) from the 70 cm planning view (detail allowed) (F14). On a 390 px phone,
show the route and its hazards and nothing else. On the 870 px desk column, one inset or plan can show a single
flagship's internal stages (Scrapy: scout, analysis, summarization, Delta Lake), the way a port plan sits inside a
coastal chart (F4). *Test:* at 390 px no label is under 13 px on screen, and every element on the phone layout is also
in the purpose table (I1).

**I11. What can be said in text goes in the text.** The Coast Pilot exists for what a chart cannot show (F13). Figures
such as commit counts, co-authorship shares and dates are table material for the README. The image should carry only
what is spatial: what connects to what, where the way in is, and where the traps are. *Test:* if removing an element
from the image and putting the same fact in a README sentence loses nothing, it belongs in the README.

**I12. Do not draw "nothing" where the truth is "unknown".** On charts, a blank area warns of missing data, and "no
data" is a display-base item that cannot be switched off (F13). A gap in activity is not the same as a gap in
knowledge. If the image shows an absence, it has to be a true absence, stated without theme words ("unsurveyed" stays
banned). Freshness should come from non-sweep dates only (F17). *Test:* no date or gap in the image comes from a sweep
day.

**I13. The theme lives in how the image works, never in labels.** A real chart never tells you it is a chart. It works
like one: a title block read first, marks where decisions sit, one way in, hazards with clearing rules, prominence by
importance (F1–F12). That matches the owner's "if it looks like a shoe ... you don't need to tell me it's a shoe".
*Test:* no word on the sheet names the theme, and a reviewer can still say which element is the way in and which is a
hazard without a legend.
