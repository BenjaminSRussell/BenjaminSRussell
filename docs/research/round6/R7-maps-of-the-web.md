# R7. Maps of the web: what crawl engineers and researchers actually draw, and which one Ben's tools can honestly make

Round 6 research, 9 Oct 2026. The question for the owner: of the real maps of the web and the internet, which one
would be an honest, buildable map subject for a crawl engineer's profile, made from data his own tools produce, and
which one teaches a visitor something true about his projects that the text can't teach faster?

How this was gathered. The shared web-search budget for this run ran out before this researcher's first query
(the tool reported the limit of 200 searches per turn as used). So every external source below was fetched directly
by URL with WebFetch and read, or downloaded as a PDF and its text extracted locally. Where a page did not contain
a figure, this file does not give that figure. Sources marked "secondary" were read only through an encyclopedia or
a summary page. Project facts come from the clones, read on 9 Oct 2026.

## Sources

Maps of the internet (networks, addresses)

1. Lyon, Barrett. The Opte Project, "About." opte.org, c. 2022 (page footer "© 2022"). https://www.opte.org/about
2. Wikipedia. "Opte Project." Accessed 9 Oct 2026. https://en.wikipedia.org/wiki/Opte_Project
3. Lyon, Barrett. The Opte Project, "The Internet" (the 1997-2021 sequence and the 2003 and 2010 images).
   https://www.opte.org/the-internet
4. CAIDA. "AS Core" visualization project, editions 2000-2020. https://www.caida.org/projects/as-core/
5. USC/ISI ANT Project. "Internet Address Space" maps and census, 2003 onward. https://ant.isi.edu/address/
6. Heidemann, J., Pradkin, Y., Govindan, R., Papadopoulos, C., Bartlett, G., Bannister, J. "Census and Survey of the
   Visible Internet." ACM IMC 2008, Vouliagmeni. PDF read in full text: https://ant.isi.edu/~johnh/PAPERS/Heidemann08c.pdf
7. Munroe, Randall. xkcd #195, "Map of the Internet" (IPv4 space "as of 2006", Hilbert curve). https://xkcd.com/195/
8. Wikipedia. "Hilbert curve." Accessed 9 Oct 2026. https://en.wikipedia.org/wiki/Hilbert_curve
9. Wikipedia. "Carna botnet" (the Internet Census 2012). Accessed 9 Oct 2026. https://en.wikipedia.org/wiki/Carna_botnet
10. Dodge, Martin. "An Atlas of Cyberspaces." Cyber-Geography Research, University of Manchester, 1997-2004.
    https://personalpages.manchester.ac.uk/staff/m.dodge/cybergeography/atlas/atlas.html

Maps of online space as jokes that still state their measure

11. Munroe, Randall. xkcd #256, "Online Communities" (c. 2007; the page shows no date). https://xkcd.com/256/
12. Munroe, Randall. xkcd #802, "Online Communities 2" (data from spring and summer 2010). https://xkcd.com/802/

Maps of the web graph (pages and links)

13. Broder, A., Kumar, R., Maghoul, F., Raghavan, P., Rajagopalan, S., Stata, R., Tomkins, A., Wiener, J. "Graph structure
    in the Web." Computer Networks 33 (2000) 309-320. Full text extracted from the PDF:
    https://snap.stanford.edu/class/cs224w-readings/broder00bowtie.pdf
14. Meusel, R., Lehmberg, O., Bizer, C., Vigna, S. Web Data Commons, "Hyperlink Graphs" (2012 and 2014 graphs from
    Common Crawl). https://webdatacommons.org/hyperlinkgraph/
15. Meusel, R., Vigna, S., Lehmberg, O., Bizer, C. "Graph Structure in the Web - Revisited." WWW 2014, Seoul; figures read
    from the WDC topology page for the 2012 graph. https://webdatacommons.org/hyperlinkgraph/2012-08/topology.html
16. Albert, R., Jeong, H., Barabási, A.-L. "The diameter of the world wide web." Nature 401 (1999) 130-131; arXiv
    cond-mat/9907038 (abstract only read). https://arxiv.org/abs/cond-mat/9907038

Common Crawl

17. Common Crawl. "Statistics of Common Crawl Monthly Archives" (cc-crawl-statistics). https://commoncrawl.github.io/cc-crawl-statistics/
18. Common Crawl. "Overview." https://commoncrawl.org/overview
19. Common Crawl. "September 2026 Crawl Archive Now Available" (CC-MAIN-2026-39), released 19 Sep 2026.
    https://commoncrawl.org/blog/september-2026-crawl-archive-now-available
20. Common Crawl. "Latest crawl." https://commoncrawl.org/latest-crawl
21. Common Crawl. "Web Graphs" (host- and domain-level). https://commoncrawl.org/web-graphs
22. Common Crawl. CDX URL index server. https://index.commoncrawl.org/
23. Common Crawl. "CCBot." https://commoncrawl.org/ccbot

A site's own description of itself: robots.txt and sitemap.xml

24. Koster, M., Illyes, G., Zeller, H., Sassman, L. RFC 9309, "Robots Exclusion Protocol." IETF, Sep 2022.
    https://www.rfc-editor.org/rfc/rfc9309.html
25. sitemaps.org. "Sitemaps XML format" (protocol 0.9). https://www.sitemaps.org/protocol.html
26. Google Search Central. "Introduction to robots.txt" (last updated 10 Dec 2025).
    https://developers.google.com/search/docs/crawling-indexing/robots/intro
27. Google Search Central. "What is a sitemap" (overview). https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
28. Google. "Crawl budget management for large sites." https://developers.google.com/crawling/docs/crawl-budget
29. Wikipedia. "robots.txt" (history: Koster 1994, Stross, RFC 9309, AI-crawler blocking). Secondary. https://en.wikipedia.org/wiki/Robots.txt
30. Wikipedia. "Sitemaps" (history: Google 0.84 in 2005, joint support 2006, robots.txt discovery 2007). Secondary.
    https://en.wikipedia.org/wiki/Sitemaps
31. Indigo, J., Smart, D., Araújo, M., Lewittes, M. (authors); HTTP Archive. "SEO," Web Almanac 2024.
    https://almanac.httparchive.org/en/2024/seo
32. Longpre, S., Mahari, R., et al. (49 authors). "Consent in Crisis: The Rapid Decline of the AI Data Commons."
    arXiv 2407.14933, 2024 (abstract read). https://arxiv.org/abs/2407.14933
33. Graham, Mark. "Robots.txt meant for search engines don't work well for web archives." Internet Archive Blogs,
    17 Apr 2017. https://blog.archive.org/2017/04/17/robots-txt-meant-for-search-engines-dont-work-well-for-web-archives/

Certificate Transparency as a list of hosts

34. Laurie, B., Langley, A., Kasper, E. RFC 6962, "Certificate Transparency." IETF (Experimental), Jun 2013.
    https://www.rfc-editor.org/rfc/rfc6962.html
35. certificate.transparency.dev. "How CT works." https://certificate.transparency.dev/howctworks/
36. Wikipedia. "Certificate Transparency" (history, Chrome requirement for all certificates since April 2018, internal
    names becoming searchable). Secondary. https://en.wikipedia.org/wiki/Certificate_Transparency
37. Google Chrome. "Chrome Certificate Transparency Policy." https://googlechrome.github.io/CertificateTransparency/ct_policy.html
38. crt.sh certificate search (© Sectigo Limited 2015-2026). https://crt.sh/

How crawlers and crawl tools draw a crawl

39. Najork, M., Heydon, A. "High-Performance Web Crawling." Compaq Systems Research Center, SRC Research Report 173,
    26 Sep 2001 (Mercator). Full text extracted: https://www.cs.cornell.edu/courses/cs685/2002fa/mercator.pdf
40. Wikipedia. "Web crawler" (frontier, seeds, policies; Cho, Garcia-Molina and Page 1998; Najork and Wiener 2001).
    Secondary. https://en.wikipedia.org/wiki/Web_crawler
41. Screaming Frog. "SEO Spider User Guide: General" (crawl and directory tree visualisations).
    https://www.screamingfrog.co.uk/seo-spider/user-guide/general/
42. Scrapy developers. "Frequently Asked Questions" (crawl order). https://docs.scrapy.org/en/latest/faq.html
43. Scrapy developers. "Settings" (DEPTH_LIMIT, DEPTH_PRIORITY, DEPTH_STATS_VERBOSE, ROBOTSTXT_OBEY).
    https://docs.scrapy.org/en/latest/topics/settings.html

The owner's projects (clones, read 9 Oct 2026)

44. rustmapper (repo Rust-sitemap), HEAD 00a877d (7 Oct 2026): `src/cli.rs` (`--seeding-strategy sitemap, ct, commoncrawl,
    all, none`; `--ignore-robots`; `--max-urls`; `--duration`), `src/bfs_crawler.rs` (seeding at lines 225-280, depth at
    line 590), `src/state.rs:131` (`SitemapNode`), `src/sitemap_seeder.rs`, `src/ct_log_seeder.rs`,
    `src/common_crawl_seeder.rs`, `src/frontier.rs`, `src/robots.rs`, `src/sitemap_writer.rs`. Path: `/home/user/rust-sitemap`.
45. Scrapy (the owner's pipeline), `Scraping_project/src/scrapy_prometheus.py` lines 161-172 (hidden-URL categories and
    routes). Path: `.../scratchpad/clones/Scrapy`.
46. ideal-url-organizer, `README.md` (organization methods "By Crawl Depth", "Hierarchical Tree", "By Crawl Status").
    Path: `.../scratchpad/clones/ideal-url-organizer`.
47. The current image, `.../scratchpad/r6/current-sheet-desk-870.png`, and the round brief `.../scratchpad/r6/BRIEF.md`
    (the owner's words of 9 Oct 2026).

## Findings

F1. Every serious map of the internet says what position, size and colour mean, and each of those is a measured
property of the thing mapped. In Opte, networks that are "more extensive and more connected" sit near the centre,
fringe networks with only a couple of providers sit on the outer ring, colour is the regional registry and shade is
network size [1]. The data was traceroute at first, then BGP routing tables, starting from RouteViews captures in
1997 [2, 3]. CAIDA's AS Core plots each network in polar coordinates, with radius from its transit degree, and each
map is a year of traceroute samples from its Ark monitors [4]. The ISI census lays the 32-bit address space out on a
Hilbert curve, so neighbouring addresses stay neighbours. Each point is a /16 block, colour is the reply type and
hatching marks space that was never probed [5, 8]. Nothing on these maps is decoration. Every visual variable answers
the question "what does this mean?"

F2. Even the joke maps state what area means, and the author changed the measure when it stopped telling the truth.
xkcd #256 says "Geographic area represents estimated size of membership" and adds "should not be used for
navigation" [11]. Three years later, #802 switched to the "volume of Daily Social activity," because total
membership no longer reflected how big and healthy a community was [12]. xkcd #195 places every /8 block by a stated
rule, the Hilbert curve [7]. The current image has islands sized by the number of days with commits in a week [47],
and nothing on the image says what that size means. That is the owner's question, "Is it based on the size of the
project or how many commits?" A cartoon answers that question, and the current image does not.

F3. A map of the web is a record of one crawl. Broder et al. built the bow tie from two AltaVista crawls of more than
200 million pages and 1.5 billion links each. They ran forward and backward breadth-first searches from 570 random
start pages [13]. They found a strongly connected core of about 56 million pages, with IN, OUT and TENDRILS each about
44 million. Pages in OUT include "corporate Websites that contain only internal links." For a random source and
destination, a directed path exists only 24% of the time. When one exists, it averages about 16 links [13]. The shape
depends on the crawl. The Common Crawl 2012 page graph has a core of 51.3% of its pages, more than 1.82 billion
[15]. The 2014 graph, gathered with a fixed seed list of about 6 billion URLs, has a core of only 19%. The WDC
authors attribute the difference to the crawl strategy [14]. The lesson for a profile map: the seed, the limits and
the date make up the map's legend. A crawl map that omits them misleads.

F4. Distance on the web is measured in links from a starting page. Breadth-first crawling makes that distance the
crawl's own order. Cho, Garcia-Molina and Page compared crawl orders on 180,000 stanford.edu pages [40, secondary].
Najork and Wiener found that a breadth-first crawl of 328 million pages reaches high-PageRank pages early [40,
secondary]. Albert, Jeong and Barabási modelled the web's diameter from local link measurements [16; abstract only].
Crawler tools draw exactly this. Screaming Frog's force-directed diagram puts the start URL at the centre, with pages
"smaller and lighter with increasing crawl depth." An edge is the first link to a page, and red marks a
non-indexable page so that "problematic areas" stand out [41]. Scrapy exposes the same quantity. DEPTH_LIMIT caps
it, DEPTH_PRIORITY switches between breadth-first and depth-first, and DEPTH_STATS_VERBOSE records a request count for
each depth [43]. The default order is depth-first [42].

F5. Ben's own crawler already records the geography those tools draw. Each rustmapper `SitemapNode` carries `depth`,
`parent_url`, `status_code`, `response_time_ms`, `content_type`, `link_count`, `discovered_at` and `crawled_at` [44,
`state.rs:131`]. A link found on a page gets `job.depth + 1` and the page as parent [44, `bfs_crawler.rs:590`]. So a
finished crawl is a tree. Each page has a depth from the start URL and a parent link, and the fetch outcome is known.
His ideal-url-organizer already sorts URLs "By Crawl Depth," as a "Hierarchical Tree" and "By Crawl Status" [46].

F6. A site describes itself in two files, and both are claims, not facts. robots.txt holds per-agent groups of allow
and disallow rules, and the longest match wins. A 4xx means the crawler may fetch anything, and a 5xx means it must
assume complete disallow. The rules "are not a form of access authorization" [24]. Google says the file is "not a
mechanism for keeping a web page out of Google," and that its main use is to keep crawlers from overloading a site
[26]. A sitemap lists `loc`, an optional `lastmod`, `changefreq` (a "hint and not a command") and `priority`, up to
50,000 URLs and 50 MB per file. It can be declared from robots.txt with a `Sitemap:` line [25]. Google says a sitemap
"doesn't guarantee" crawling. It helps most on large, new or poorly linked sites, because crawlers find pages
"mainly by following links" [27]. Across the web, about 84% of robots.txt requests returned 200 and about 14%
returned 404 in 2024. Only 0.06% of files exceeded the 500 KiB parsing limit [31]. Google applies crawl budget
thinking to sites of 1 million or more pages, or 10,000 or more pages that change daily [28]. Of the two files, the
sitemap is the site's account of what it contains. A crawl from the homepage is the account of what its links
actually reach. Comparing the two is a basic crawl-engineering check.

F7. Certificate Transparency is a public list of hostnames, not a map of pages. The logs are append-only Merkle trees
that anyone can submit to. Operators "MUST NOT impose any conditions on retrieving or sharing data from the log"
[34]. Chrome and Safari require SCTs, which are proof that a certificate was logged [35]. Chrome's policy asks for 2
or 3 SCTs from distinct logs, depending on certificate lifetime, and from at least two distinct operators [37]. The
requirement has covered all certificates since April 2018 [36, secondary]. So the publicly trusted HTTPS hostnames
under a domain are, in practice, searchable at crt.sh [38]. A side effect: names meant for internal networks
"become publicly searchable" once logged [36]. CT tells you which hosts exist. It tells you nothing about how pages
link.

F8. Common Crawl is an outside record of which URLs exist, at a scale no individual can match. CC-MAIN-2026-39
(4-17 Sep 2026) holds 2.17 billion pages and 361.4 TiB uncompressed, from 40.4 million hosts and 33.2 million
registered domains, and 587.2 million of its URLs were not in earlier crawls [19, 20]. Its statistics are computed
from the URL index [17]. It also publishes host- and domain-level link graphs over rolling three-month windows,
the latest being cc-main-2026-jul-aug-sep [21]. Any domain can be queried through the CDX index [22]. CCBot can be
opted out through robots.txt [23]. These are maps of the whole web. Ben did not make them, and putting them on his
profile would describe Common Crawl, not him.

F9. rustmapper uses three of these outside maps to get into a site, which makes it unusual. `--seeding-strategy` takes
`sitemap`, `ct`, `commoncrawl`, `all` or `none` [44, `cli.rs`]. The sitemap seeder reads robots.txt for `Sitemap:`
lines, follows sitemap indexes, probes common paths if none are declared, and drops URLs the robots rules disallow
[44, `sitemap_seeder.rs`]. The CT seeder queries `crt.sh/?q=%.{domain}&output=json&exclude=expired`, caps the result
at 50,000 entries, and checks names by DNS in chunks of 100 with a 5 s timeout [44, `ct_log_seeder.rs`]. The Common
Crawl seeder reads `collinfo.json`, then queries `{crawl}-index?url=*.{domain}&output=json&fl=url` [44,
`common_crawl_seeder.rs`]. Robots compliance is on by default, and `--ignore-robots` turns it off [44, `cli.rs`]. A
sitemap can be written back out [44, `sitemap_writer.rs`]. In other words, the four ways into a site covered in this
file (links, the site's own sitemap, CT logs, Common Crawl) are four code paths in his crawler.

F10. A limit in the data, found in the code. Seeded URLs enter the frontier at depth 0 with no parent, the same as
the start URL [44, `bfs_crawler.rs` lines 246 and 276]. The frontier also deduplicates, so when seeders run together, a node
does not record which source found it. A per-source map therefore needs one run per strategy (`sitemap`, `ct`,
`commoncrawl`, `none`), or a new `source` field in `SitemapNode`. Without one of those, any "found by" figure would
be inferred, which breaks the standing rule against estimates.

F11. Where a crawler keeps its frontier is a real structure, and his matches the published design. Mercator's
frontier "controls the crawler's download schedule." It uses a FIFO queue per host, so no host gets hit by parallel
requests [39]. rustmapper's frontier is sharded, and each host is held in a min-heap ordered by the time it may next
be fetched (`ReadyHost { host, ready_at }`) [44, `frontier.rs`]. Scrapy's metrics route each hidden URL to
`depth_crawl`, `js`, `offsite`, `low_value` or `duplicate` [45]. So the route a URL takes through his tools can be
sourced line by line from code. No public "frontier visualization" turned up in the sources this run could reach
without search. This file does not claim one exists.

F12. How the data was gathered is part of the map's honesty. The Internet Census 2012 counted about 1.3 billion
used IPv4 addresses with a botnet of about 420,000 devices that had default passwords, and its map is tainted by
that [9]. Heidemann's census, by contrast, says plainly what it cannot see. Only 3.6% of allocated addresses were
visibly occupied, and firewalls and private space hide the rest [6]. Consent around crawling is getting stricter. In
2024 audits, 5% or more of C4's tokens were fully restricted, as were 28% or more of its most critical sources [32].
The Internet Archive stopped honouring robots.txt for archiving [33]. In 2023, 306 of the 1,000 most-visited sites
blocked GPTBot [29, secondary]. A crawl drawn on a public profile must show its own good conduct: robots obeyed,
small caps, a stated date.

F13. Famous internet maps get admired as images, but nobody uses them to navigate. Opte is in MoMA's collection and
a permanent Boston Museum of Science exhibit [2]. Dodge's atlas says such maps "help us visualise and comprehend"
digital space and help people navigate it [10]. On a profile, a whole-internet map gives a visitor no way to act
on it. A map of one crawl from one start URL does: it shows how deep the site goes, what failed, and what the
sitemap claims that the links never reach.

## What this means for the owner's image and page

Each point is tied to his goal: every map and every element has a purpose drawn from the projects themselves.

I1. Retire the week-islands. The test: for every mark, a stranger can say what its size means and what that tells
them about a project. The islands fail on both counts [F2, 47]. Even xkcd states its measure in a caption [11, 12].
Days with commits in a week is not a property of Scrapy or rustmapper. It teaches nothing about what they do.

I2. The one honest map subject his tools can produce is a crawl of one site by rustmapper: pages by depth from the
start URL, with the fetch result for each [F4, F5]. This is a real geography a reader moves through: a start, links,
depths, dead ends. It is what crawl tools themselves draw [41]. The visitor learns what his crawler does and how a
site looks to it. They could not get that from reading "concurrent web crawler in Rust." Test: every count on the map
can be recomputed from a committed crawl record (the JSONL of `SitemapNode` rows) with one script.

I3. The strongest form of I2 shows his tool's distinct ability: the four ways in [F9]. For the same domain and date,
draw what the links reached (`none`), what the sitemap declared (`sitemap`), the hosts CT lists (`ct`) and what Common
Crawl holds (`commoncrawl`), and where they overlap and differ. Test: each source is a separate run with its own
recorded count, never inferred from a mixed run [F10]. Alternatively, add a `source` field to `SitemapNode` in
rustmapper before drawing. The route labels are the real names (robots.txt, sitemap.xml, crt.sh, Common Crawl), which
crawl engineers recognize. No theme words.

I4. The crawl's terms go in the fine print, because the terms shape the map [F3, F12]: start URL, date, rustmapper
version (0.1.3 on PyPI), `--max-urls` or `--duration`, and "robots.txt obeyed." Test: AUDIT.md gets a row for each
crawl figure, with its definition and the command that produced it, before the figure appears.

I5. Pick a target he owns or has permission to crawl, keep it small, and do not run it against a third party from
CI. Never draw a CT host list for someone else's domain on a public page, since CT exposes internal names [36]
[F7, F12]. Test: the target, the permission, and the caps are recorded in the repository. A frozen, dated crawl
record committed once is preferable to a live crawl in every build.

I6. If no crawl target is acceptable, the honest fallback is a route map drawn from code: the path a URL takes
through rustmapper. Seed sources lead to the per-host frontier (`ReadyHost`, `ready_at`), then the robots check,
fetch, parse, WAL, and sitemap export [F11]. Scrapy's routes (`depth_crawl`, `js`, `offsite`, `low_value`,
`duplicate`) can be drawn the same way [45]. Test: every box and arrow cites a file and line at a stated sha, and
nothing on it is a count.

I7. Do not use Opte, CAIDA, the bow tie, a Hilbert IPv4 map or Common Crawl's web graph as the picture. They are
others' measurements of the whole internet, and Ben's tools cannot produce them [F1, F8, F13]. At most, a small fact
from one of them belongs where his tool plugs into it, for example "seeds from Common Crawl's index" [22, 44]. Test:
every element on the image is produced by his code or his repositories.

I8. Draw depth as rows (0, 1, 2, 3...), not as a force-directed hairball, so it reads at 390 px. Status codes and
counts stay legible at that width, while Screaming Frog's radial diagram needs a desktop screen to read [41]. This
is reasoning, not a sourced finding. It needs checking on the phone render. Test: at 390 px every depth row and its
count is readable without zooming.

I9. Each element must earn its place by what the visitor learns. Depth answers how far in the site goes. Status
answers what broke. Sitemap minus links answers what the site claims but does not link. Hosts from CT answer what
exists beyond the links. A mark that answers none of these, such as a light, a compass or shallows, goes [F2, 47].
