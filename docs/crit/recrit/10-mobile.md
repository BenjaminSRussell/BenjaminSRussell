# Re-crit 10 — Mobile / responsive (built v9 "Chart" README)

Reviewer 10 (docs/crit/panel30/10-mobile.md). Judged from the PNGs and the README render, not the code.
Material looked at: the six `<qa>/sheets/*-phone.png` (360 CSS px, DPR 3), the day/night desk stills,
the crops, the hero filmstrip, `check.md`, README.md source order. Because `<qa>` has no night-phone
renders and no phone-width README render, I made my own in my scratchpad (`recrit10/`): the six phone
SVGs at 360×DPR 3 in dark scheme, a hero-phone filmstrip at 0.3/2/4.5/14/31 s, and the QA README
harness at a real 360 px layout viewport (the harness HTML has no `<meta viewport>`, so its own 360 render
laid out at 980 px and picked the desktop sources; with the meta injected and GitHub's 16 px gutters,
`img.currentSrc` is the phone edition for all six pictures in both schemes, 328 CSS px wide). perf.json is
absent from `<qa>`, so §7.3's hero-phone repaint gate is unverified here; I judged it from the SVG timeline.

## 1. Scores J1–J12 (phone-weighted where the criterion names the phone)

| # | Score | Evidence |
|---|---|---|
| J1 | 3 | hero-phone.png y≈300–400: two-line italic thesis under the name, ~17 CSS px, said once; the footer's "The chart ends here. The web doesn't." is a coda, not a repeat. |
| J2 | 3 | hero-phone with the name covered: hatched UNSURVEYED band, "SMALL-SCALE" pencil note, soundings thinning westward, a boat anchored in Scrapy Harbor. The survey edge is the picture. |
| J3 | 2 | Silhouettes differ: portrait hero, curve strip, tall chart, four ruled lines, shelf with a boat. But instruments-phone.png is a 1080×72 hairline with a sheet number: covered, it is an `<hr>`, not a sheet. |
| J4 | 2 | Unit on every phone sheet ("SOUNDINGS IN COMMITS", "IN URLS · THOUSANDS"), datum "MAIN" twice. Region is gone: the desk cartouche's "IALA REGION B" was cut from the four phone lines; no light character ("Fl G 4s") survives on any phone sheet. |
| J5 | 1 | approaches-phone.png: G "1", R "2", Wk '25, Rep, ED, SD, boxes A/B/C, a pecked Ldg 290° line — and no legend anywhere on the phone page, while the caption under it says "The legend on this sheet defines every symbol used on the page". |
| J6 | 3 | The same figures recur on four sheets and in the prose (21, 0.1.3, 1,665, HW 358 · 5 Oct, LW 0 · 24 Aug, Notice 9), including the log-phone coda "1947 · 1,665 commits · 21 repos". Not re-run; judged from consistency. |
| J7 | 2 | Both instruments in the sub ("1,665 commits of mine · 1,966 all hands"); "charted as proposed; nothing runs it yet"; edition "provisional". Against: the phone approaches sets sloping soundings whose convention is defined nowhere a phone reader can see; footer soundings 7 5 3 14 have no unit. |
| J8 | 3 | hero-phone-t300: name, thesis, cartouche and islands already present (no empty frame); contours draw 0.2–2 s; boat is plotted in six discrete fixes at 4-s intervals to 28 s, then nothing (26 `<animate>`, 6 `<set>`, no `animateMotion`, no indefinite). Five other phone sheets are frozen. |
| J9 | 2 | Glossed headings everywhere ("Soundings · stats"). But README.md l.199: the colophon's Editions bullet ends mid-sentence at an open backtick because the footer picture was written into it; and "Notices to mariners · five principles" lists nine items. |
| J10 | 3 | readme-vp-light-fold: hero fills 410 of 780 CSS px; caption, then the link row (rustmapper · Scrapy Harbor · PyPI · Email · How it's built) at y≈450; the builds/languages/stack table starts at y≈520. Field is also on the sheet itself, line 2 of the cartouche. |
| J11 | 2 | Night-phone (my render): lights are magenta glows and the brightest things; name in pale ink; water tints navy, not inverted. But cartouche lines 3–4, "VAR 14h (2026)", "LW 0 · 24 Aug", footer "corrected through Notice 9" sit at ≈.55–.6 opacity on navy: gone in sunlight at 13 CSS px. |
| J12 | 2 | Present on the phone: real figures in the lagoon (0 · 17 · 108), "SMALL-SCALE" note, Wk '25, the last log line, VAR 14h. But the VAR note cannot resolve because the colophon is truncated (see defect 1), and the footer serpent does not exist on the static phone footer. |

**J-total 28/36.** No zero; J1/J2/J7/J10 ≥ 2. Below the 30 pass line, carried down by J5 (phone legend) and the README truncation.

## 2. The five-second test

**870 px, day.** A cream chart with a serif name across it, an italic line under it, an archipelago shoaled
toward a hatched right edge, a compass that is a clock. It says: a person who makes maps of code, careful,
a little old-fashioned, with a thesis. The eye reaches "CRAWL AND DATA INFRASTRUCTURE · PYTHON AND RUST" by
about second four because the cartouche sits at the lower left of the first screen.

**360 px, day.** Better than the desk, which I did not expect. The hero is 328×410 CSS px and fills 53 % of
the first screen: "Ben Russell" at ~60 px, the thesis on two lines at ~17 px, the compass, the islands, and
the four cartouche lines at 13 px, all without zooming. In five seconds a thumb-width reader has the name,
the thesis, the field and the stack, and has seen that the right-hand quarter of the map is hatched
"UNSURVEYED". What they do not get in five seconds: that it is a *small-scale edition* (the rotated note is
there but collides with the shoals), and anything about the marks.

**Night.** The name goes pale, the paper goes navy, the three lights go pink and are the only saturated
things on the screen besides the boat's sail; it reads as a night chart, not an inverted PNG. The thesis
holds. The cartouche's last two lines and the compass note fall to the edge of legibility; a reader on a
phone in sunlight gets name, thesis, field, and loses unit, datum, chart number and edition.

## 3. Top 5 defects

**1. The footer sheet has been written into the collapsed Colophon, mid-sentence.**
*Where.* README.md ll.199–209: the Editions bullet reads "Your system picks the edition through `" and then
the footer `<picture>` block, two `<!-- picture:footer:end -->` markers, `</li>`; the colophon's remaining
bullets (motion, variation, license) are gone and the file ends there. readme-vp-light-part2 / readme-light.png:
the page's last visible line is "▶ Colophon · how the sheets are drawn…". No reader, on any device, sees
the edge sheet unless they open a details element whose summary does not mention it.
*Why it matters.* STANDARDS thesis and STD 7: "the footer is where the water finally goes over the edge";
the arc has no end. STD 13 / J12: the VAR note "only resolves in the colophon", and the colophon is cut.
J9: a visibly broken sentence in the one place that explains the editions.
*Fix.* In `scripts/render_readme.py`, anchor the block-marker match to a whole line
(`^<!-- picture:footer:start -->\s*$` … `^<!-- picture:footer:end -->\s*$`, MULTILINE) so the marker quoted
in the inline code span of the Editions bullet is not treated as the slot; finish that bullet
("…through `<picture>` media queries: phone under 768 px, night with `prefers-color-scheme: dark`, still
with `prefers-reduced-motion`."); restore the motion/variation/license bullets; emit the footer block after
`</details>` as the last element; delete the duplicate end marker; add a render test that every picture
block is a direct child of the document, not inside `<details>`, `<li>` or a code span.
*Cost.* S.

**2. The climax sheet has no legend on the phone, and the caption says it does.**
*Where.* approaches-phone.png, whole sheet (720×1240): G "1", R "2", R "4", G "3", Wk '25, Rep, ED, SD,
boxes A/B/C, a dashed "robots.txt" rectangle, a pecked line "Ldg 290°", sloping and upright soundings. The
desk sheet's 1280-wide legend and zones-of-confidence key are simply absent. The README caption directly
under it: "The legend on this sheet defines every symbol used on the page and says which figures are
measured."
*Why it matters.* J5 (point at any mark; reads on a phone) scores 1. STD 1: the upright/italic honesty
convention is "defined once in the legend", so on the phone it is defined nowhere. STD 4: light characters
are not on the sheet.
*Fix.* Extend the phone approaches to 720×1400 and set a five-row key across the foot, inside the neat line,
mono 26 (13 CSS px): `G can · port  R nun · starboard  Fl G 4s · Fl R 4s` / `Wk '25 wreck, year ·
Ldg leading line` / `Rep reported · ED existence doubtful · SD sounding doubtful` / `A B C seed source
zones: sitemaps · CT logs · Common Crawl` / `upright measured · sloping illustrative`. Add "Fl G 4s" and
"Fl R 4s" to the G "1" / R "2" labels. Keep the mobile legend to those rows; the desk legend stays as is.
*Cost.* M.

**3. Edge and label collisions on three phone sheets.**
*Where.* (a) approaches-phone.png rows 0–30 and 1830–1860 (720-space y≈0 and y≈1238): "SOUNDINGS IN URLS ·
THOUSANDS", "21" and "CHART NO. 21 · SHEET 3" are set flush to the top and bottom edges with no margin (see
`recrit10/crop-appr-top.png`, `crop-appr-bottom.png`); on GitHub the image abuts text above and the caption
below, so the running head reads as part of the page, not the sheet. (b) footer-phone.png, 720-space
(≈430–700, 300): "corrected through Notice 9" is set across the bottom neat line; the rule passes through the
x-height (`crop-footer-br.png`). (c) hero-phone.png 720-space x≈600–630, y≈420–600: the rotated
"SMALL-SCALE" note is set over the dashed danger lines and the 0-soundings of the rustmapper lagoon, not in
the hatch band (`crop-hero-entrance.png`).
*Why it matters.* STD 5 (type survives the medium) and the still-frame gate's spirit: a finished sheet has
margins. The small-scale note is the one honest phone-only layer and it is the one thing that collides.
*Fix.* (a) viewBox `0 0 720 1264`, translate content by 12 px, head and foot labels at y=14 and y=1254.
(b) Lower the footer frame's bottom rule to y=296 and set the two foot labels in a 24 px margin band
below it, or move "corrected through Notice 9" inside the frame above the rule. (c) Move "SMALL-SCALE"
20 px right so it sits inside the hatch, left of "UNSURVEYED", and shorten the dashed shoal that reaches
x≈640 by the same amount; or set the note horizontally under the cartouche's fourth line.
*Cost.* S.

**4. The instruments phone sheet reads as a broken image.**
*Where.* instruments-phone.png: 1080×72, one grey rule and "CHART NO. 21 · SHEET 5" right-aligned; on the
page (readme-vp-light-part2, y≈6420) it sits between the heading's sentence and the `<sub>` stack list and
looks like an `<hr>` with a stray caption.
*Why it matters.* J3: covered, it is not a sheet. The "omit" mechanism was my own proposal, so this is not
a re-litigation: the build shows that a sheet number on an empty sheet is an apology (STD 1 in spirit).
*Fix.* Make the hairline a running head for the plain-text list beneath it: 720×64, left "INSTRUMENTS ·
LEAD · LOG · LOOKOUT" in condensed caps 26, with the three glosses ("what measures depth · what keeps the
record · what watches") on a second line at 22, right "CHART NO. 21 · SHEET 5". Then the `<sub>` under it
reads as the table the head announces. Alternatively drop the sheet number from the phone edition
entirely and keep the bare rule.
*Cost.* S.

**5. Night-phone semantic ink below the floor, and the region dropped from the cartouche.**
*Where.* My night renders: hero cartouche lines 3–4 ("SOUNDINGS IN COMMITS · DATUM: MAIN", "CHART NO. 21 ·
EDITION 0.1.3 · NOTICE 9") and "VAR 14h (2026)" at ≈.55; soundings-phone "LW 0 · 24 Aug" at .55; footer
"CHART NO. 21 · SHEET 6" and "corrected through Notice 9" at ≈.5–.6; log-phone "Log closed 1550 · B.S.R." at
.55. In the SVGs: `opacity=".55"` ×10 in hero-phone-night, `.55/.60` in log and soundings. Day cartouche
also lacks the region: the desk has "IALA REGION B", the phone has none.
*Why it matters.* Panel F5 and STD 5: night-phone semantic text ≥ .85; phones are read in sunlight with no
hover to recover anything. J4: a hydrographer cannot name the region from any phone sheet.
*Fix.* In the night-phone editions raise every semantic text node to ≥ .85 (keep .5–.6 for texture
soundings only); change hero-phone cartouche line 3 to "SOUNDINGS IN COMMITS · DATUM: MAIN · IALA B".
*Cost.* S.

Also noted, not ranked: `perf.json` is missing from `<qa>`, so the §7.3 hero-phone gate
(≤ 0.25 repaints/s after 6 s) is unverified; the SVG timeline (one-shot 0–4 s, six discrete fixes
4–28 s, nothing after) says it should pass. The `<img>` fallback is the 1280 hero; whether the GitHub
app honours `<picture>` is still unverified (panel idea 4). The recruiter table's blank header row
renders as an empty 2×40 px strip at 360 px.

## 4. Three things that must not be touched

1. **The hero-phone composition.** 720×900, name ~132, thesis on two lines, four cartouche lines at 13 CSS
   px, compass r 60 with N and VAR, fourteen soundings, four names, the boat plotted in discrete fixes.
   It is the first screen of the page on a phone and it passes the five-second test unaided; it is the
   proof that the small-scale edition is a redrawing, not a shrink.
2. **The `<picture>` plumbing.** `(max-width: 767px)` to match GitHub's single-column break; sources most
   specific first (phone+still+dark, phone+still, phone+dark, phone, still+dark, still, dark, img); phone
   editions static except the hero, so six entries per sheet and eight for the hero; no `<a>` around any
   sheet. Verified at 360 px: `currentSrc` is the phone edition for all six pictures in both schemes.
3. **The log and soundings phone sheets.** "1430 remarks · nothing to report / 1431 Nothing on fire. /
   Log closed 1550 · B.S.R. / 1947 · 1,665 commits · 21 repos" in four ruled lines, and the 52-week tide
   curve with dated HW/LW and "Heights observed, not predicted." Both are complete sheets at 328 px with
   nothing to pinch for.

## 5. Does it look like months of work?

On a phone, yes, for the first time: six sheets that were "navy rectangles" in my panel review are now six
different objects, each redrawn for the width rather than shrunk, with a type floor that holds at 13 CSS
px and a boat that is plotted instead of sailed. The hero on a 360 px screen is better than most desktop
portfolio headers. What still looks like a template is the chrome around the sheets rather than the sheets:
the hairline "instruments" with a sheet number, the recruiter table's empty header strip, a caption
promising a legend the phone does not carry, and a page that ends on a collapsed "▶ Colophon" because the
footer was written into the wrong slot. What still looks like a diagram is the phone approaches: without
its legend it is a handsome chart with unexplained letters on it, and the one marginal note that says
"this is the small-scale edition" is set over the shoals it is apologising for. Fix the renderer bug, give
the phone approaches its five-row key, and clear the three margins, and the phone edition is the one I
would show first.
