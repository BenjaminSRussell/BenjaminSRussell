# STANDARDS — what this profile must meet before it ships (synthesis of six critiques)

## The thesis (all six converged on it)
**The web is wrong about itself. Ben surveys the parts that are off the chart.**
Every sheet must argue this, not decorate it. The hero states it in one line. The edge of the
survey is the structural idea on every sheet (soundings thin, "unsurveyed" hatching at the margin)
and the footer is where the water finally goes over the edge. Seed sources (sitemaps, CT logs,
Common Crawl) are literally how he pushes the edge back; they appear as a source diagram.

## Testable standards
1. **Nothing in the artwork is a placeholder or an apology.** No "illustrative", "pending", "seeded".
   Honesty is a *convention*, defined once in the legend: upright numerals are measured, italic
   numerals are illustrative. Test: grep the SVGs for ILLUSTRATIVE / PENDING / SEEDED → 0 hits.
2. **Every number on a sheet is real or italic.** Hero soundings, islands, chart number, edition,
   tide curve, weekday ring: derived from data fetched by build_stats.py (git history, GraphQL,
   PyPI). Test: change a value in stats.json → the chart visibly changes.
3. **Islands are the portfolio.** Each public repo is a feature whose area follows its commit count;
   big ones named. Shoals are *submerged* (tinted water inside a dotted danger line, italic name),
   not hatched land. Hatching means foul ground; use it only for "unsurveyed" margins and wrecks.
4. **Chart grammar is correct.** Blue shallow-water tint between contours; one IALA region
   (Region B, US: red *nuns* to starboard returning, green *cans* to port), numbered marks
   G"1"…R"4" with light characters; lights flash their labelled rhythm; two-ring modern rose
   (no portolan star, no rhumb lines); title block carries number, edition, datum, source diagram,
   "Corrected through Notice 5"; chart number repeated outside the neat line. A hydrographer
   should be able to name the region, unit and datum from the sheet.
5. **Type survives the medium.** Semantic text ≥13px at 1280 (≈9px in the README column);
   9–11px only for texture (soundings). ≥4 distinct sizes; upright vs italic carries meaning;
   at least one rotated marginal note. Test: 360px render still shows name, thesis, shoals, one light.
6. **Sheets are different.** Cover the titles: silhouettes must differ. No shared eyebrow template
   on every sheet. Chrome varies: full neat-line with minute bars (hero), inset panels and a source
   diagram (approaches), ruled log paper with no neat-line (log), a short tide-table strip
   (soundings), a tall climax sheet. No pill chips anywhere. Heights vary deliberately.
7. **An arc with a climax.** Hero (overture) → soundings (short) → one tall merged Approaches
   chart where rustmapper's survey feeds Scrapy Harbor (climax) → log → notices → legend/edge.
8. **Motion is choreographed.** One-shot opening (chart surveys itself: contours by depth, soundings
   in course order, name set, boat sails); after it ≤3 indefinite loops on the page; shared timing
   scale (10/24/48/96 s loops; 150–2600 ms transitions); three named easings; no linear bob/droplet/
   typing; no empty still frame at any time; lights flash real characters; no hard seam (boats sail
   out and back, or arrive and hold). Test: filmstrip at 0/25/50/75/99% of the longest loop: every
   frame is a finished sheet.
9. **Copy says each thing once.** No "I build X that Y"; ≤2 tricolons and ≤2 "X, not Y" per page;
   no "Hi, I'm Ben"; no borrowed nautical jokes (dragons, fair winds, thanks for reading this far,
   that's a mood); no self-explanation of the tricks; correct terms (Notices to Mariners, datum,
   sounding, lateral mark). Dual-register headings so a skimmer gets Projects / Principles / Stack.
10. **The information a hiring manager needs is present** in plain text: what he builds (crawl and
    data infrastructure), languages, the two systems with concrete capabilities, five principles,
    links. No invented role, location, employer or availability (we do not have them; leave the
    position line for Ben to fill).
11. **No borrowed widgets.** The contribution snake is deleted. The tide curve is the only live graph.
12. **Alt text is marginalia** in voice, accurate, and complete.
13. **Second-look layers** (at least four, none captioned): real figures among the soundings; the
    compass variation note that only resolves in the colophon; marginal pencil notes tied to the
    Notices; a silent sea-serpent arc in the footer once every 96 s; the last log entry.
14. **Build quality.** Each SVG < 300 KB; XML valid; bounds check clean; stats refresh daily and the
    hero redraws itself from the same data.
