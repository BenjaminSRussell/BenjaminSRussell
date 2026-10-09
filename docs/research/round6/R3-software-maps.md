# R3. Maps of software: what they can honestly show, and what fails

Round 6 research, 9 Oct 2026. The question this file answers for the owner: when is a map of code worth drawing,
what must its space mean, and what does that say about the week-islands in the current image?

Everything below was read for this round. Where only an abstract or a secondary summary was available, the source
line says so. Figures quoted from papers are the papers' own.

## Sources

Software maps and software cities

1. Wettel, R., Lanza, M., Robbes, R. "Software Systems as Cities: A Controlled Experiment." ICSE 2011, pp. 551-560.
   https://2011.icse-conferences.org/content/software-systems-cities-controlled-experiment.html
2. Wettel, R., Lanza, M., Robbes, R. "Empirical Validation of CodeCity: A Controlled Experiment." Technical report,
   University of Lugano, 2010 (the full write-up of [1]; read in full: per-task results, sections 8.1-8.3).
   https://www.inf.usi.ch/faculty/lanza/PUBS/M/Wett2010a.pdf
3. Wettel, R., Lanza, M. "Visual Exploration of Large-Scale System Evolution." WCRE 2008 (abstract).
   https://www.si.usi.ch/assets/publications/conf/wcre/wcre2008/WettelL08.pdf
4. Kuhn, A., Erni, D., Nierstrasz, O. "Towards Improving the Mental Model of Software Developers through
   Cartographic Visualization." 2010 (abstract). https://arxiv.org/abs/1001.2386
5. Kuhn, A., Erni, D., Nierstrasz, O. "Embedding Spatial Software Visualization in the IDE: an Exploratory Study."
   SoftVis 2010 (read in full: observations 6.2, 6.3, 6.5). https://arxiv.org/pdf/1007.4303
6. Kuhn, A., Loretan, P., Nierstrasz, O. "Consistent Layout for Thematic Software Maps." WCRE 2008.
   https://arxiv.org/abs/1209.5490
7. Erni, D. "Codemap: Improving the Mental Model of Software Developers through Cartographic Visualization."
   MSc thesis, University of Bern, 2010. https://scg.unibe.ch/assets/archive/masters/Erni10a.pdf
8. Schreiber, A., Misiak, M. "Visualizing Software Architectures in Virtual Reality with an Island Metaphor."
   VAMR / HCII 2018, LNCS; and Misiak et al., "IslandViz," VISSOFT 2018 (abstracts). https://elib.dlr.de/123314
9. Fittkau, F., Krause, A., Hasselbring, W. ExplorViz: hierarchical software landscape visualization, controlled
   experiments, VISSOFT 2015 and Information and Software Technology 2017 (abstracts).
   https://oceanrep.geomar.de/id/eprint/29386/1/vissoft15main-mainid8-p-fca6e5d-25093-preprint.pdf
10. Steinbrückner, F., Lewerentz, C. "Representing Development History in Software Cities." SoftVis 2010, pp. 193-202;
    and "Understanding Software Evolution with Software Cities," Information Visualization 12, 2013 (abstracts).
    https://opus4.kobv.de/opus4-UBICO/frontdoor/index/index/docId/8901
11. Moreno-Lumbreras, D., Minelli, R., Villaverde, A., González-Barahona, J. M., Lanza, M. "CodeCity: A Comparison
    of On-Screen and Virtual Reality." Information and Software Technology 153, 2023.
    https://susi.usi.ch/usi/documents/329624
12. Balzer, M., Deussen, O., Lewerentz, C. "Voronoi Treemaps for the Visualization of Software Metrics." SoftVis 2005.
    https://graphics.uni-konstanz.de/publikationen/Balzer2005VoronoiTreemapsVisualization/index.html
13. Savidis, A., Vasilopoulos, C. "Code Arcades: 3D Visualization of Classes, Dependencies and Software Metrics."
    2025 (abstract). https://arxiv.org/abs/2509.23297

Treemaps, line maps, evolution views, activity animations

14. Shneiderman, B. "Treemaps for space-constrained visualization of hierarchies" (history page, HCIL, University of
    Maryland, updated through 2015). https://www.cs.umd.edu/hcil/treemap-history/
15. Johnson, B., Shneiderman, B. "Tree-maps: A Space-Filling Approach to the Visualization of Hierarchical Information
    Structures." IEEE Visualization 1991. https://drum.lib.umd.edu/items/e6de7036-e026-4c44-885d-c2f1eec7f651/full
16. Shneiderman, B. "The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations." IEEE Symposium on
    Visual Languages 1996. https://drum.lib.umd.edu/handle/1903/5784
17. Eick, S. G., Steffen, J. L., Sumner, E. E. "Seesoft: A Tool for Visualizing Line Oriented Software Statistics."
    IEEE TSE 18(11), 1992 (abstract). https://dblp.dagstuhl.de/pid/46/2917.html
18. Lanza, M. "The Evolution Matrix: Recovering Software Evolution using Software Visualization Techniques." IWPSE 2001.
    https://www.inf.usi.ch/lanza/Downloads/Lanz2001c.pdf
19. Lanza, M., Ducasse, S. "Polymetric Views: A Lightweight Visual Approach to Reverse Engineering." IEEE TSE 29(9),
    2003. https://scg.unibe.ch/archive/papers/Lanz03dTSEPolymetricSCG.pdf
20. Caudwell, A. Gource, official site and man page. https://gource.io/ ; https://man.archlinux.org/man/gource.1.en
21. Ogawa, M., Ma, K.-L. "code_swarm: A Design Study in Organic Software Visualization." IEEE TVCG 15(6), 2009; UC Davis
    news release, 2008. https://www.ucdavis.edu/news/visualizing-open-source-software-development
22. Wattenberger, A. (GitHub Next). "Visualizing a Codebase." 2021. https://githubnext.com/projects/repo-visualization/
23. Tornhill, A. "Your Code as a Crime Scene." Pragmatic Bookshelf, 2015 (2nd ed. 2024); InfoQ report of the QCon talk,
    2015. https://www.infoq.com/news/2015/03/code-as-a-crime-scene

Architecture diagrams and code maps in tools

24. Brown, S. The C4 model for visualising software architecture. https://c4model.com/
25. Brown, S. C4 model, "Notation." https://c4model.com/diagrams/notation
26. Brown, S. C4 model, "System context diagram." https://c4model.com/diagrams/system-context
27. Brown, S. C4 model, "Container." https://c4model.com/abstractions/container ; Brown's "maps of your code ... like
    Google Maps" framing as quoted at https://supportportal.moodinternational.com/hc/en-us/articles/360015465100
28. Kruchten, P. "Architectural Blueprints: The 4+1 View Model of Software Architecture." IEEE Software 12(6), 1995.
    https://arxiv.org/pdf/2006.04975
29. Scrapy developers. "Architecture overview." Scrapy documentation (latest).
    https://docs.scrapy.org/en/latest/topics/architecture.html
30. Microsoft. "Map dependencies across your solutions" (Code Maps), Visual Studio 2015 documentation.
    https://learn.microsoft.com/en-us/previous-versions/visualstudio/visual-studio-2015/modeling/map-dependencies-across-your-solutions
31. Coati Software. Sourcetrail repository, archived 14 Dec 2021. https://github.com/coatisoftware/sourcetrail
32. Woodward, M., Biagianti, A. "Include diagrams in your Markdown files with Mermaid." GitHub Blog, 14 Feb 2022.
    https://github.blog/2022-02-14-include-diagrams-markdown-files-mermaid/

How developers actually understand code

33. Brooks, F. P. "No Silver Bullet: Essence and Accidents of Software Engineering." IEEE Computer, 1987 (section
    "Invisibility"). https://www.cgl.ucsf.edu/Outreach/pc204/NoSilverBullet.html
34. Cherubini, M., Venolia, G., DeLine, R., Ko, A. J. "Let's Go to the Whiteboard: How and Why Software Developers Use
    Drawings." CHI 2007, pp. 557-566 (abstract and secondary summary). https://arxiv.org/pdf/2210.16089
35. LaToza, T. D., Venolia, G., DeLine, R. "Maintaining Mental Models: A Study of Developer Work Habits." ICSE 2006.
    https://www.st.cs.uni-saarland.de/edu/empirical-se/2006/PDFs/latoza06.pdf
36. Sillito, J., Murphy, G. C., De Volder, K. "Asking and Answering Questions during a Programming Change Task."
    FSE 2006 / IEEE TSE 2008 (44 question types). https://open.library.ubc.ca/collections/831/items/1.0052042
37. Maalej, W., Tiarks, R., Roehm, T., Koschke, R. "On the Comprehension of Program Comprehension." ACM TOSEM 2014
    (builds on Roehm et al., ICSE 2012). https://neverworkintheory.org/2015/02/13/on-comprehension-of-program-comprehension.html
38. Petre, M. "UML in Practice." ICSE 2013, pp. 722-731. https://www.ics.uci.edu/~andre/informatics223s2017/petre.pdf
39. Storey, M.-A., Fracchia, F. D., Müller, H. A. "Cognitive Design Elements to Support the Construction of a Mental
    Model during Software Exploration." Journal of Systems and Software 44, 1999.
    https://webhome.cs.uvic.ca/~mstorey/teaching/infovis/course_notes/softviz.pdf

Evaluations and critiques of the field

40. Merino, L., Ghafari, M., Anslow, C., Nierstrasz, O. "A Systematic Literature Review of Software Visualization
    Evaluation." Journal of Systems and Software, 2018. https://scg.unibe.ch/research/softvis-eval
41. Müller, R., Zeckzer, D. "Past, Present, and Future of 3D Software Visualization: A Systematic Literature
    Analysis." IVAPP 2015 (read). https://scitepress.org/Papers/2015/53257/pdf/index.html
42. Teyseyre, A. R., Campo, M. R. "An Overview of 3D Software Visualization." IEEE TVCG 15(1), 2009 (as cited in [41]).
    https://doi.org/10.1109/TVCG.2008.86
43. Roberts, J. C., Mearman, J. W., Butcher, P. W. S., Al-Maneea, H. M., Ritsos, P. D. "3D Visualisations Should Not be
    Displayed Alone: Encouraging a Need for Multivocality in Visualisation." EG UK CGVC 2021 (read).
    https://arxiv.org/pdf/2108.04680

Perception, notation and maps in general

44. Moody, D. "The 'Physics' of Notations: Toward a Scientific Basis for Constructing Visual Notations in Software
    Engineering." IEEE TSE 35(6), 2009. https://ieeexplore.ieee.org/document/5353439
45. Mackinlay, J. "Automating the Design of Graphical Presentations of Relational Information." ACM TOG 5(2), 1986.
    https://courses.ischool.berkeley.edu/i247/f05/readings/Mackinlay_APT_TOG86.pdf
46. Munzner, T. "Visualization Analysis and Design." CRC Press, 2014; course slides "Marks and channels."
    https://www.cs.ubc.ca/~tmm/courses/436V-20/slides/marks.pdf
47. Cleveland, W. S., McGill, R. "Graphical Perception: Theory, Experimentation, and Application to the Development of
    Graphical Methods." JASA 79, 1984 (via course notes). https://info3312.infosci.cornell.edu/ae/graphical-perception.html
48. Heer, J., Bostock, M. "Crowdsourcing Graphical Perception: Using Mechanical Turk to Assess Visualization Design."
    CHI 2010. https://idl.uw.edu/papers/crowdsourcing-graphical-perception
49. Montello, D. R., Fabrikant, S. I., Ruocco, M., Middleton, R. S. "Testing the First Law of Cognitive Geography on
    Point-Display Spatializations." COSIT 2003, LNCS 2825 (read). https://user.geo.uzh.ch/sfabri/pubs/montello_etal_cosit03.pdf
50. Tobler, W. "A Computer Movie Simulating Urban Growth in the Detroit Region." Economic Geography, 1970 (the first
    law of geography). https://en.wikipedia.org/wiki/Tobler%27s_first_law_of_geography
51. Lynch, K. "The Image of the City." MIT Press, 1960. https://en.wikipedia.org/wiki/The_Image_of_the_City
52. Monmonier, M. "How to Lie with Maps." University of Chicago Press, 1991 (via the Christian Science Monitor review,
    1991). https://www.csmonitor.com/1991/0918/18122.html
53. Tufte, E. "The Visual Display of Quantitative Information." Graphics Press, 1983 (data-ink, chartjunk; via
    Georgia Tech notes). https://faculty.cc.gatech.edu/~stasko/4460/Notes/tufte.pdf
54. Bateman, S., Mandryk, R., Gutwin, C., Genest, A., McDine, D., Brooks, C. "Useful Junk? The Effects of Visual
    Embellishment on Comprehension and Memorability of Charts." CHI 2010.
    https://vis.csail.mit.edu/classes/6.859/readings/pdfs/Bateman-UsefulJunk.pdf

What visitors to a GitHub profile look for

55. Marlow, J., Dabbish, L. "Activity Traces and Signals in Software Developer Recruitment and Hiring." CSCW 2013
    (read). https://www.cs.cmu.edu/~xia/resources/Documents/Marlow-cscw13.pdf
56. Moldon, L., Strohmaier, M., Wachs, J. "How Gamification Affects Software Developers: Cautionary Evidence from a
    Natural Experiment on GitHub." ICSE 2021. https://ar5iv.labs.arxiv.org/html/2006.02371
57. Prana, G. A. A., Treude, C., Thung, F., Atapattu, T., Lo, D. "Categorizing the Content of GitHub README Files."
    Empirical Software Engineering 24(3), 2019. https://arxiv.org/abs/1802.06997
58. GitHub Docs. "Why are my contributions not showing up on my profile?"
    https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/managing-contribution-settings-on-your-profile/why-are-my-contributions-not-showing-up-on-my-profile

The owner's projects and this repository (read-only clones and files)

59. Scrapy repository README, "What It Does" and "Architecture" (two Mermaid diagrams: URLs to Scout Spider to Analysis
    to Summarization to Delta Lake; stage workers 2-4, LakehouseManager, Redis, Postgres).
    `scratchpad/clones/Scrapy/README.md` lines 20-35 and 120-161.
60. Rust-sitemap (rustmapper) README and `src/lib.rs`: seeders (sitemap, CT logs, Common Crawl), sharded frontier with
    bloom dedup and per-host politeness, governor 32-512 workers, redb state plus WAL, Redis mode, outputs
    `sitemap.jsonl`, `sitemap.xml`, tech report; troubleshooting table; `pyproject.toml` version 0.1.3.
    `scratchpad/clones/Rust-sitemap/README.md` lines 1-60, 86-123, 209-232.
61. `docs/data/AUDIT.md` (how every figure is gathered; the 7 Oct 2026 merge day; `repos[].months`).
62. Current render: `scratchpad/r6/current-sheet-desk-870.png`.

62 sources, 58 of them outside this repository.

## Findings

**F1. Software has no ground of its own, so a map of code must decide what position means, or the space means
nothing.** Brooks: "Software is invisible and unvisualizable. The reality of software is not inherently embedded in
space," and when we diagram it we find "not one, but several, general directed graphs superimposed one upon another"
[33]. Kuhn and colleagues say the same from the other side: there is no natural mapping of software to two
dimensions, and in most software visualizations position and distance carry no meaning at all [6]. Every serious
software map in the literature answers the question "what does where mean?" explicitly: districts are packages in
CodeCity [1, 2], position is vocabulary similarity in Codemap [6], area is size inside the directory tree in treemaps
[14, 15], each island is one deployable module in IslandViz [8]. A map that cannot say what its axes or distances mean
is drawing a picture of a map, not a map.

**F2. Readers take distance and position as meaning whether or not the designer meant it.** Montello, Fabrikant and
colleagues tested the "first law of cognitive geography," that people believe closer things are more similar, and
their results largely support it [49], an echo of Tobler's "near things are more related than distant things" [50].
In the Codemap field study, participants "tended to interpret visual distance as a measure of structural
dependencies, even though they were aware of the underlying lexical implementation"; one said "this is a very useful
tool but the layout does not make sense" [5, obs. 6.5]. So every pair of shapes that sit close together on a map will be
read as related.

**F3. Small isolated shapes draw the eye and are read as important.** Same study: participants "were attracted to
isolated elements, rather than exploring clusters", because "those (isolated) elements looked more important as they
visually stick out of the rest of the map" [5, obs. 6.3]. The authors suggest hiding isolated elements or muting them
so they do not draw attention [5]. The most salient mark on a map has to be the most important fact, or the map
teaches the wrong thing first.

**F4. Spatial software maps beat plain tools only on overview questions, and only when the space encodes real
structure.** CodeCity (districts = packages, building height = methods, base = attributes, colour = lines of code)
raised correctness by 24.26 % and cut completion time by 12.01 % against Eclipse plus a spreadsheet, over 41
participants [1, 2]. The gain came from overview tasks: how widely a term is spread (29-38 % better on A2.2) and the
impact of a change through a class's callees (40-50 % better on A3). On precise lookups, such as "the three classes
with the most methods," CodeCity did not do better, "because Excel is extremely efficient in finding precise answers
(e.g., the largest, the top 3, etc.)" [2, §8.3.1]. ExplorViz found a significant correctness gain for a hierarchical
landscape over a flat one [9]. Codemap users used the map to see "quantity and dispersion of search results and call
graphs" and rarely to navigate [5, obs. 6.2]. Put simply: a map helps with "where is it, how spread is it, what does it
touch"; a list or a table helps with "how many, which is biggest."

**F5. Islands work as a metaphor only when an island is a separate thing and what links islands is shown.** In
IslandViz each OSGi module is its own island and the dependencies between modules are what the user explores [8].
Codemap's hills are clusters of files with shared vocabulary [6, 7]. In both the land is a body of code and the water
between islands means "not directly connected." None of the literature uses an island for a span of time. In the
current image an island is one week of commits in one repository, sized by the days that week had commits [62]; it is
neither a body of code nor a place, and the sea between two islands means only "weeks passed." The owner's question,
"is it based on the size of the project or how many commits?", has no good answer, because the shape answers a question
nobody brings to a profile.

**F6. Area is the weakest common channel for a number, and coastline detail adds marks that mean nothing.** Cleveland
and McGill rank position on a common scale first, then length, angle and slope, with area near the bottom [47]; Heer and
Bostock replicated the ranking and extended it to rectangles and circles [48]. Shneiderman says mapping a linear
variable to area "goes against a graphic design guideline" and that small items merge into a dark mass [14]. Mackinlay's
expressiveness criterion [45], restated by Munzner as "express all of, and only, the information in the dataset
attributes" [46], rules out any encoding that implies data that is not there. The island's outline, the blue shallows and
the varying shapes imply terrain; the datum underneath is one integer from 1 to 7.

**F7. A symbol should look like what it means.** Moody's semantic transparency, "the extent to which the meaning of a
symbol can be inferred from its appearance," is one of nine principles for notations that work [44]. A landmass
suggests a place, a body, something that exists; a week is an interval. The island symbol points the reader the wrong
way, which Moody's framework counts as worse than a neutral mark.

**F8. Pictures of commit activity over time belong to an impressionistic genre, built to engage rather than to inform.**
Gource draws "an animated tree with the root directory of the project at its centre" and presents itself as an
animation, with no claims about analysis [20]. code_swarm was designed as "organic" visualization for a general
audience, modelled on music videos, giving an impression of a project's dynamics [21]. The serious per-entity-over-time
form is Lanza's Evolution Matrix (rows are classes, columns are versions, mark size encodes metrics), and its point is a
vocabulary of patterns a reader can look for, such as classes that grow, stall, or die [18, 19]. The current image is an
evolution matrix of repositories with island decoration and no patterns the reader is meant to find [62]. Wettel and
Lanza add that metrics over time "often lead to overly simplistic insights" when characterizing evolution [3].

**F9. Commit activity is a weak and noisy signal of the work, and visitors know it.** GitHub's own calendar counts only
commits on the default branch or gh-pages, from a linked email, in a non-fork repository [58]. This repository's audit
found one day (7 Oct 2026) carrying 514 of the owner's commits across 19 repositories, 198 of them merge commits and 442
made through the web merge button [61]: real, but a day of merging, not of building. When GitHub removed streak
counters, developer behaviour changed measurably (fewer long streaks, fewer one-commit days kept up to protect them, less
weekend work) [56], which shows how much the activity display shapes, rather than reports, the work. Employers
interviewed by Marlow and Dabbish distrusted popularity counts; they looked at "the project where the applicant had made
the most commits" and then "assessing the actual code that was written there," and read side projects as a sign of
enthusiasm [55]. Commit counts point a visitor at a project; they do not describe it.

**F10. What people draw when they want someone else to understand a system: the system, its neighbours, and what flows
between them, every box and line labelled.** The C4 model's system context diagram puts one system in the middle with
the people and systems it talks to, and "detail isn't important here"; it is meant for everyone, technical or not [26].
Its notation rules: every diagram has a title; every element has "a short description, to provide an 'at a glance' view
of key responsibilities"; "every line should be labelled, the label being consistent with the direction and intent of
the relationship"; the diagram should be "(mostly) understood without a narrative" [25]. Brown describes C4 as maps of
code at several levels of detail, the way one zooms in and out on Google Maps [27]. Kruchten's 4+1 model gives each
stakeholder the view that answers their concern, and ties them together with a few walked-through scenarios [28].
Scrapy's own documentation explains the framework with one architecture diagram plus nine numbered steps that walk a
request from the engine through the scheduler, downloader, spider and item pipeline, then loop [29]. That is the honest
map of a crawler: a route with named stops.

**F11. Developers rely on informal drawings and conversation, not on formal or dedicated map tools.** At Microsoft,
developers drew code mostly to talk about it face to face, in informal notations; formal modelling tools did not fit
that need [34]. Mental models of code are kept mostly in heads and conversation, and design documents fall short [35].
Among 50 professional engineers, 35 used no UML at all and none used it wholeheartedly [38]. Dedicated comprehension
tools go unused, and developers often do not know the comprehension features their IDE already has [37]; Visual
Studio's Code Maps were an Enterprise-edition feature [30], and Sourcetrail, an interactive dependency explorer, was
archived in 2021 [31]. The questions programmers ask during change tasks, catalogued as 44 kinds, are about where
things are, what calls what, and how data gets from one place to another [36]. A visitor's first questions about a
project are the same kind: what goes in, where does it go, what comes out.

**F12. If the picture is rebuilt on a schedule, its layout must stay put unless the subject changed.** Software-city
work treats a stable layout as the condition for a reader's mental map surviving updates [10]; Kuhn's consistent layout
exists so that different thematic maps of the same system stay comparable [6]. A layout keyed to calendar weeks shifts
every week by construction. A layout keyed to a project's structure moves only when the code does.

**F13. Activity data is useful as a layer on top of structure, never as the ground.** Tornhill's hotspot method lays
change frequency from version control over the code's structure to show where effort and risk concentrate, and warns of
false positives [23]. Kuhn's software cartography keeps one stable base layout and swaps thematic overlays (call
graphs as flow lines, coverage as shading) on top [5, 6]. Seesoft colours each line of code by a statistic so the
statistic sits where the code is [17]. In each case the time data answers "which part of the thing," because the
thing is drawn first.

**F14. "It is a map" is not evidence that it helps.** 62 % of the software visualization approaches published at
SOFTVIS and VISSOFT include no evaluation [40]. Of 155 papers on 3D software visualization, 53 % rest on anecdotal case
studies and 16 % have no evaluation [41]; the call for more empirical evaluation [42] still stands. Even advocates of 3D
argue a single spatial view should not be shown alone, because each depiction affords different tasks [43]. A design is
justified by the questions a reader can answer from it, not by the genre it belongs to.

**F15. A static README image cannot lean on hover, zoom, or a learned visual language.** Wattenberger's repository
circles (colour = file type, size = file size) "might take a minute to wrap your head around", and imports had to be
shown on hover because drawing them all was too cluttered [22]. Shneiderman's "overview first, zoom and filter, then
details-on-demand" assumes interaction [16]; an SVG in a README has none. Treemap novices needed 10-15 minutes of
training [14]. Whatever the image shows must be readable at first sight, with its words on it. GitHub renders Mermaid
diagrams in Markdown natively [32], and the owner's Scrapy README already explains the project as two Mermaid flow
diagrams [59]: the projects' own documentation already thinks in routes.

**F16. Embellishment is allowed when it is memorable and does not cost accuracy; decoration that carries no data is
the thing to cut.** Embellished charts were read as accurately as plain ones and remembered better after two to three
weeks [54]; Tufte's rule is that ink should vary with the data [53]. Monmonier: every map selects and simplifies, and
the question is whether the selection serves the reader or the mapmaker [52]. Lynch's study of how people hold a city
in mind found five elements (paths, edges, districts, nodes, landmarks) [51]; a map is legible when those are present
and true. The theme can live in the line work and the type as long as each mark that looks like information is
information.

**F17. The owner's two main projects have a real geography a reader can travel.** rustmapper: URLs enter from seeders
(site sitemaps, certificate-transparency logs, Common Crawl), pass into a sharded frontier with bloom-filter dedup and
per-host politeness, are fetched by 32 to 512 workers under an adaptive governor, are parsed and classified, are made
durable in redb with a write-ahead log, and leave as `sitemap.jsonl`, `sitemap.xml` and a tech-stack report; Redis
mode adds shared locks and work stealing; it ships as `pip install rustmapper` (0.1.3) and as a Rust binary [60].
Scrapy: URLs go to the stage 1 discovery spiders, then to the LakehouseManager over Delta Lake, then to stage 2
analysis, stage 3 summaries and stage 4 large documents, with Redis holding seen sets and queues and Postgres taking
metrics [59]. rustmapper's README also lists real hazards: seeders stalling on crt.sh or Common Crawl rate limits,
timeouts from unreachable hosts in CT logs, memory blow-up from too many large pages, and a crawl that exits on purpose
when Redis is misconfigured [60]. These are the entry points, routes, stores and hazards that F1, F4 and F10 say
justify a map.

## What this means for the owner's image and page

Each implication is stated so that a reviewer can check it against the image, and each is tied to his goal: every map
and every element has a purpose that comes from the projects themselves.

1. **Remove the week-islands as the base of the picture.** For each mark, write: the datum, and the question a visitor
   brings that it answers. The island's datum is "commit-days in week w for repository r" and no visitor brings that
   question (F5, F8, F9). Test: if the sentence "a visitor learns ___ from this, and it has to be a picture because ___"
   cannot be completed from the projects, the mark goes. This is his "chasing a purpose instead of having a purpose,"
   turned into a check.

2. **Make position mean the path the data takes.** The base geography of the main chart is the route through his crawl
   work: where URLs come from, where they wait, what fetches them, where they are stored, what comes out (F1, F10, F17).
   Test: a visitor can trace one URL from entry to output in under ten seconds at 870 px and at 390 px, and every stop
   on the route names a real module or store that exists in the repository (`frontier.rs`, `wal.rs`, `sitemap_writer.rs`,
   `src/lakehouse/`, Delta Lake, Redis), checkable with `grep` against the clones.

3. **If a shape looks like land, it must be a thing that exists, and the water between shapes must mean "not connected."**
   An island may stand for a separately shipped thing (the PyPI package, the Rust binary, the Scrapy pipeline) and a
   line between two islands must be a real hand-off of data or a real dependency (F2, F5, F7). Test: for every pair of
   shapes drawn close together, a reviewer can point to the real relation in the code; if there is none, move them apart
   or merge them.

4. **The most salient mark must be the most important fact.** Isolated small marks pull the eye first (F3). Test: show
   the image for five seconds and ask what the eye landed on first; the answer must be the thing he most wants a
   visitor to know (for example, the route a URL takes through rustmapper, or that it is installable today), never a
   stray one-day blip.

5. **Numbers go on position and length, with units and a definition the audit backs.** No area-coded counts, no
   outlines or shallows that vary without data (F6). Every printed figure comes from the README, the code, or
   `AUDIT.md` with its definition (for example "32-512 workers, adaptive" from [60], "0.1.3 on PyPI" from
   `pyproject.toml`). Test: each number in the SVG has a source line in a table in the build script or the audit.

6. **Drop commit activity from the picture, or keep it only as a light overlay on the structure.** He already said
   "we don't need to show the commits," and the research agrees: activity is a weak, noisy signal of the work and
   visitors look past it to the code (F9). If any time data stays, it marks which part of the route changed recently
   (Tornhill, Kuhn overlays, F13), never weeks as places. Test: no element's position is set by a date.

7. **Label the data, never the theme.** Every element carries a short plain description and every line says what moves
   along it ("URLs," "fetched pages," "rows to JSONL"), per the C4 notation rules (F10). That is different from
   labelling the genre, which he has ruled out ("don't tell the user show the user"). Test: no word in the image names
   the theme; every line and stop has a label that names a real thing.

8. **One picture, one graph.** Brooks says software is several graphs on top of each other (F1). Choose data flow for
   the crawl projects and do not overlay time, language and activity on the same space. Test: a reviewer can say in one
   sentence what the space of the chart stands for.

9. **Hazards drawn on the chart must be real, documented failure modes.** The conventions a navigator relies on
   (route, waypoints, hazards) earn their place only when they encode facts (F16, F17). rustmapper's README documents
   real ones: seeder stalls from rate-limited crt.sh or Common Crawl, timeouts from unreachable CT-log hosts, memory
   from too many large pages, a fatal stop on bad Redis config. Test: each hazard mark cites a line in the project's
   README or code, and the mark sits on the stop where that failure happens.

10. **Things a list answers faster stay as text.** "Which other repositories, in what language" is a lookup, where
    plain tools beat maps (F4). The "15 more" row and per-repository language labels belong in the README text, not in
    the chart. Test: remove an element and ask whether the text above or below the image already says it; if yes, it
    stays out.

11. **The layout must not move unless the code moved.** Positions come from the route, not the calendar (F12). Test:
    two builds a week apart, with no change to the projects' modules, produce the same node positions byte for byte.

12. **Make the chart a door into the code.** Visitors who judge work go to the project with the most work and read
    its code (F9). Node names should be the repository's own names for things, so a visitor who opens the repository
    finds the same words in the file tree. Test: every node label appears as a file, directory or README heading in the
    linked repository.

13. **Readable at first sight on a phone, with no hover and no legend to learn.** A route reads top to bottom at
    390 px; a 13-month timeline squeezed to 390 px does not (F15). Test: at 390 px every label is at least the README's
    body size, and nothing on the chart needs a key to decode.

14. **Judge the new image by tasks, not by genre.** Because "it looks like a chart" proves nothing (F14), each review
    round should ask three or four visitors' questions the image must answer at a glance: "What does his main project
    do with a URL?", "Where does the data end up?", "Can I use it today, and how?", "What can go wrong, and does it handle
    it?" Test: a reviewer who has not read the README answers all of them from the image alone, correctly.
