# Crit 26 — the sailor and coastal navigator

I race offshore and do my own pilotage on paper and a plotter; not a designer. I looked at hero-day-2x, approach-scrapy-day-2x, footer-night-2x, log-day-2x, read README.draft.md, the three specs, STANDARDS and CHANGELIST, and checked `chartlib.boat`, `course` and `out_and_back`.

## 2. What is good

- **The bearings are right.** `course()` computes atan2 from north, clockwise, three digits; 077° then 106° on the hero is what a protractor gives. Most "nautical" pages get this wrong.
- **"Soundings in commits · Datum: main"** is the best line on the page for a sailor: chart datum is the level every depth is reduced to, and `main` is exactly that.
- **The approaches spec has real buoyage.** I plotted it: channel ~067° into the anchorage; G"1" and G"3" fall north (port returning), R"2" and R"4" south. Odd greens, even reds, numbered from seaward: red right returning holds. Health Ldg Lts on 070° ("on the line = passing") and Grafana Lt Fl(3) 10s would make any sailor grin.
- **Soundings thinning toward the limit of survey**, dashed approximate contours and the hatched UNSURVEYED band are how old sheets look at the edge; a vessel running parallel lines with the lead going is how you do it. This gets the *feeling* of unknown water right: slow down, sound, write it down.

## 3. What is bad, ranked

1. **The two sheets disagree about where the harbor entrance is.** On the hero the course arrives from the unsurveyed *east* and enters Scrapy Harbor heading ~276° (W). On Approaches the unsurveyed water is *west* and the channel runs 067° (ENE) into the same anchorage. A navigator cross-referencing sheets of one series finds the harbor mouth on opposite sides. One of them is wrong.
2. **The hero boat is a toy, not a vessel.** The hull is a symmetric trapezoid with no bow, no sheer, no rudder, mast stepped amidships. With `rotate="auto"` a *profile* boat on a *plan-view* chart tilts 13–25° on every leg: it sails uphill. The ±3° symmetric heel is a boat rolling at anchor, not a boat under way; under sail you heel to leeward and stay there.
3. **The log columns do not mean what they say.** Req/s is boat speed, not wind; cumulative URLs is *distance run*, which is literally what the log instrument records. Times with colons (14:02) and a "watch ended 14:12" ten minutes after it began would not pass a skipper; a watch is four hours.
4. **The footer boat cannot do what the caption says.** Under sail, no wind, no anchor, 60 px above a fall in a current, it does not "hold". A sailor's first thought at the avatar: *where is his anchor?* Second: *river, mast up, above a weir: he is being set, not sailing.* The page should answer that.
5. **Current render: landlubber tells.** Red cans / green cones (Region A shapes under Region B words); a pictorial striped lighthouse where a chart uses a star and flare; one red and one green at opposite ends of a course, which is not a lateral pair; terminal checkmarks in a log; six course alterations with nothing to clear. The specs fix most of this; the pictorial lighthouse survives.
6. **"Breaker Lt · sector unlit = closed" reads as a failed light.** An unlit light is a Notice to Mariners item. Sector lights are always lit: white toward the fairway, red over the danger, and red is what you see when standing into it.

## 4. What needs to be done

- **Orient the sheets together.** Keep the hero (edge east, enter heading W). Either flip Approaches so survey ground is east and the channel runs west (Ldg Lts become 247°), or keep left-to-right and add a north arrow on Approaches pointing left: harbor plans are routinely oriented to the channel. Either way, draw a "SEE SHEET 3" coverage box around the harbor on the hero; that is the real convention.
- **Redraw `boat()`:** raked stem forward, small transom aft, 4 px tiller stub, mast at 40% from the bow. Drop `rotate="auto"` on hero and footer; mirror with `scale(-1,1)` at the turn only. Heel −8° to leeward steady plus a 0–4° puff on a 10 s `sea` curve; upright at anchor.
- **Log columns:** `TIME` (1402, no colon) · `LOG · URLS` (distance run) · `SPEED · REQ/S` · `WIND` (what the hosts push back: *light*, *fresh, 429s*, *calm*) · `REMARKS`. Last remark of a quiet entry: "nothing to report"; sign-off "Log closed 1412 · B.S.R." not "watch ended". Keep "Nothing on fire."
- **Footer: anchor the boat.** At x=980 drop a rode (dashed hairline to the bottom), the anchor glyph, and `14 · good holding` in 13 px upright. Good holding is where the raw layer lives; the boat stops at the edge because it *can*. (Heaving to, jib backed, is the purist alternative; only sailors will read it.)
- **Sector light:** lit, white 2 px dot toward the channel; red arc hairline over the foul ground only; label `Breaker Lt · Fl(2) WR 6s`. Red sector = breaker open = standing into danger.
- **Lights as star + magenta flare** on the chart; the pictorial tower only inside the harbor inset.
- **Add one clearing bearing** on the shoal nearest the hero course, `NMT 095°`, 13 px. Navigators plot them; nobody else draws them.

## 5. Improvements and ideas

1. **Chart abbreviations as the honesty vocabulary.** Charts already have words for "the web is wrong about itself": `SD` (sounding doubtful), `PA` (position approximate), `ED` (existence doubtful), `Rep` (reported, unverified). Put `SD` once beside each italic sounding field, define it in the legend, and mark sitemap-only features on Approaches `PA`.
2. **Lead, log and lookout.** The three oldest instruments map exactly: lead = crawlers sounding, log = WAL and Delta Lake, lookout = Prometheus/Grafana. Use it as the three-column grouping of the Instruments strip. Not a cliché; the correct term.
3. **Date the fixes (bold).** A plot marks every fix as a dot in a circle with a time. Make the hero waypoints fixes labelled with real dates from stats.json, the first-commit month of the feature each is taken off (`1025` at Rustmapper Shoal, `0925` at the harbor). The course becomes his actual two-year passage, uncaptioned. Between fixes, one DR semicircle: *the sitemap is dead reckoning; the crawl is the fix.* That sentence belongs in the README.
4. **"Local knowledge advised · see Notices 1–5"** at the harbor entrance, 13 px. Real chart phrase; points a skimmer at the principles. And label 00/06/12/18 on the commit clock so the trick can be noticed.

## 6. What the page says about its maker

Now: someone who has looked hard at charts and loves them but has not stood a watch; the drawing is better than the seamanship, and a sailor sees a handsome chart with a bathtub on it and a harbor that moves between sheets. It should say: this person navigates. He checks his datum, numbers his marks from seaward, keeps the log in the log's own columns, anchors where the holding is good, and marks a doubtful sounding as doubtful instead of guessing. That is also what a good crawler engineer does, which is the point of the metaphor.

## 7. Five lines

1. Hero and Approaches put Scrapy Harbor's entrance on opposite sides (enter heading W vs 067°); orient one sheet to the other and add a "SEE SHEET 3" coverage box on the hero.
2. Redraw `boat()` with a bow, transom and tiller; drop `rotate="auto"` on a profile boat; heel steadily to leeward, not ±3° symmetric.
3. Log columns: TIME (1402) · LOG · URLS (distance run) · SPEED · REQ/S · WIND (host pushback) · REMARKS; "Log closed", not "watch ended".
4. Footer: anchor the boat at the limit of survey, `14 · good holding`; a sailboat cannot hold station above a fall under sail.
5. Use chart abbreviations SD / PA / ED for the honesty convention, and "lead, log and lookout" as the Instruments grouping; sector light lit, red over danger.
