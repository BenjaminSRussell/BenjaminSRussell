# 25 — Comedy writer: deadpan, set-up and payoff, and the cost of winking

## 1. Who I am, what I looked at

Comedy writer, deadpan, for people who distrust jokes in design. Read README.md, README.draft.md, STANDARDS, CHANGELIST, the specs; looked at hero-day, log-day, footer-night.

## 2. What is good, and why it works

**"Not for navigation"** (hero scale bar). The best joke on the page and nobody wrote it. Every real chart carries the line; this one obeys the convention, and the obedience is the comedy. Straight face, true statement, form doing the work. The model for everything else.

**"Sitemaps are wrong about themselves."** A technical fact phrased as a character flaw: a file format given a moral failing. It is also the thesis, so it can carry the hero. But a thesis may be repeated and a joke may not, and the draft says "wrong about itself" in the hero *and* the intro. It is the hero line; the intro gives the evidence and never repeats the verdict.

**"Nothing on fire."** The rebuild (spec-supporting, log entries 5–6) is structurally right: 14:05 `remarks · nothing to report` is the official register; 14:06 "Nothing on fire." is what the operator meant. The gap between the lines is the joke; the minute between them is the beat. The WIND column dropping from *203* to *41* on that row is the straight man: the crawl is winding down, so the remark is literally true. Keep that column as specified.

**Funny only in form, correctly uncaptioned:** `Wk '25` on a shelved repo (a wreck, with the year of its last commit); `Datum: main`; `Corrected through Notice 5`; `VAR 21h00 · ANNUAL CHANGE SEE COLOPHON`; italic numerals meaning "illustrative"; "slack water" on the quiet weeks. None announces itself.

**Rightly cut.** "Here be dragons", "Fair winds", "Thanks for reading this far", "I'm told that's a mood", "The view is best right before the drop". One fault: they are jokes *about the fact that this is nautical*, not jokes that come *from* the chart. A borrowed joke says "I know this is a bit", and that is an apology. The live footer stacks three on one sheet, which is why the sheet that should be the payoff is the weakest.

## 3. What is bad, ranked

1. **The draft explains its own callback.** Notices lede: "The title block reads 'Corrected through Notice 5' because of this list." The hero planted the set-up; the reader was going to connect it to five numbered notices themselves, and the connecting is the reward. This sentence takes the reward and hands back a receipt.
2. **The punchline is typeset as the punchline.** Spec: "Nothing on fire." in Instrument Serif italic 17px, "the only serif in the body." That is underlining the joke. Deadpan requires the remark be set exactly like every other remark. If the reader has to find it, it is twice as good; if the sheet points at it, half.
3. **The footer alt tells the secret.** "Something rises behind the boat now and then." The serpent is uncaptioned by rule, and the alt text captions it.
4. **Each Notice explains why it is funny.** "Entered from Scrapy, whose circuit breakers exist for this reason." A real Notice carries a source, not a rationale.
5. **Five is stated three times.** Heading sub, lede, title block. One is a plant, two a nudge, three a wink.
6. **The tricolon problem is a comedy problem.** Three items is the shape of a joke: set-up, set-up, turn. When the third item is not a turn the sentence promises a laugh and delivers padding, the rhythm readers now hear as machine prose. The one triple that earns its shape is real: sitemaps, CT logs, Common Crawl, where the turn lands on items two and three ("the last two are how you find the subdomains nobody links to"). Keep that; cut every other list of three to two or four.

## 4. What needs to be done

- Delete the "because of this list" sentence. Lede: "Five corrections to this chart." Full stop. Drop the heading sub.
- Set log entry 6 in body mono, same size and colour as entry 5. Serif for the sign-off only.
- Footer and hero alt text describe the still state and nothing else.
- Notice sources in chart form: "Source: Scrapy, circuit breakers." / "Source: Delta Lake anchorage; rustmapper WAL." / "Source: Grafana Lt." / "Source: ideal-url-organizer." / "Source: this chart. Editions one through seven read as a template." The last is the only self-reference the page earns: a correction *to the chart*, in its form.
- Rule of one per sheet: hero, "not for navigation"; tide table, "slack water"; approaches, the red sector; log, "Nothing on fire"; footer, the held boat. Instruments has no joke and should not acquire one. Two on a sheet: cut the weaker.

## 5. Improvements and ideas

**5.1 (bold) A chart note as a 96-second set-up.** Real charts mark unconfirmed hazards "Obstn rep. 2026 (PA)": reported, position approximate. Put it in 11px mono at x≈880 on the footer, where the serpent rises, and nowhere else. A reader who knows charts gets it before the serpent; one who waits gets it after; nobody is told. This is "Here be dragons" said by a hydrographer.

**5.2 Three new lines, all true, all in form.** Under the A/B/C source diagram: **"A: as declared by the site. B, C: as found."** (A sitemap is the site's own declaration; CT logs and Common Crawl are independent. The thesis, without repeating the thesis.) On the Approaches legend: **"Red sector covers hosts that have stopped answering."** (Chart grammar, "Red sector covers Danger Rock", applied to circuit breakers.) Tide-table footnote: **"Heights observed, not predicted."** (Tide tables predict; this one records.)

**5.3 Legend entry for wrecks.** "Wk — repository no longer worked. Year of last commit." A legend entry is form, not caption; it lets `Wk '25` land for anyone who looks it up.

**5.4 Three boats, and the fourth is the avatar.** The hero boat goes out to the unsurveyed margin and returns. The packet boat arrives in the anchorage and holds. The footer boat stops sixty pixels short of the limit of survey. Returns, arrives, holds. The fourth boat is the avatar, outside the README, where the water goes over. That is the one rule-of-three the page should run, and it is structural: no sentence may mention the avatar, the waterfall or the drop. "The chart ends here. The web doesn't." is as far as prose goes.

**5.5 The honesty convention as a long set-up.** `log.json` has `"measured": false`; flipping it sets every numeral upright. The day Ben pastes a real session the italics vanish and the chart stops hedging. Say nothing about it. A page that gets drier as it gets truer is right for a page about surveying.

## 6. What the page says about its maker

Now, in the draft: someone who has found the right register and is nervous you will miss it, so he sets the punchline in a different typeface, explains the callback, and tells you in the alt text where the monster is. The jokes are good; the nerves show. It should say: someone who knows chart grammar well enough to be funny inside it, who trusts "not for navigation" to do more than a paragraph, who can leave a wreck labelled with a year and walk past it, and whose one unmistakable joke, a boat about to go over a waterfall, is the only image on his profile the page never refers to.

## 7. Five lines

1. Cut "The title block reads 'Corrected through Notice 5' because of this list." Connecting hero to Notices is the reward; explaining it is a receipt.
2. Set "Nothing on fire." in the same mono as every other remark. A punchline in its own typeface is a laugh track.
3. Remove "Something rises behind the boat now and then" from the footer alt; replace "Here be dragons" with a chart note, `Obstn rep. 2026 (PA)`, where the serpent rises.
4. Three straight-faced lines in chart form: "A: as declared by the site. B, C: as found." / "Red sector covers hosts that have stopped answering." / "Heights observed, not predicted."
5. Never mention the avatar. Three boats return, arrive and hold; the fourth goes over, and it is not on this page.
