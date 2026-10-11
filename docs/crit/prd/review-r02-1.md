# PRD review round 2, reviewer 1: Ben, the owner, reading the PRD as the person who has to live with the page

11 Oct 2026. I read `docs/crit/prd/owner-messages.md` twice, end to end, before opening anything else. Then
`docs/PRD.md` (692 lines, at `e17cc80`), `docs/crit/prd/LOG.md` (what round 1 fixed and declined), the three round-1
reviews, `README.md`, `chart.toml` (`[position]`, `[contact]`, `[copy]`), `scripts/checks/route.py` (THEME_WORDS),
`scripts/sheets/route.py`, `tests/test_pipeline.py` (`test_no_first_person_on_the_page`, `test_picture_order`),
`docs/BEN-TODO.md`, `SPEC.md` §0–1, `DECISIONS.md`, `assets/stats.json` (`edition`, `runcheck`), the round-16
`gate.txt`, and every render named in the brief: `sheet-phone-day-390`, `sheet-phone-night-390`,
`sheet-desk-day-870`, `sheet-mid-day-746`, `page-desk-1`, `page-desk-2`, `page-phone-1` to `page-phone-7`. I also
looked at what is live: `main`'s `README.md` (local and via `gh api`), the `chart` branch's `hero-day.svg` and its
last commit, and the open PR list. Nothing below repeats a finding `LOG.md` marks applied; two items it marks
"declined for this pass: product change" are carried forward because they are still open and still mine.

Verdict on the PRD: **7 / 10.** Round 1 fixed what I asked: my 7 Oct brief is in the goal table (G1a–c), the decision
has a first-screen column and a middle option (2b), "done" is defined, §5.4 was checked against the resolver. What
it still gets wrong is the thing I most need it to get right: the one decision in §9.1 is framed as if waiting costs
nothing, and it costs me the most of any option, because the page that is live while I wait is the one I rejected
on 9 Oct. Two of my sentences are also narrowed in the table (G10, G13), and the two product changes I ruled on in
round 1 are still not built.

---

## 1. Is the product this PRD defines what I asked for?

**Yes.** The sentence that decides it is 9 Oct 11:37: *"It should be telling you about me, but with a layer of a
theme of shipping. [...] It has to be helpful knowledge. If you were a fucking real sailor, if you were a real person,
you'd want it to be helpful data that you're looking at [...] and it's in a cool format."* And the test I set on
9 Oct 20:50: *"Everything, single thing inside of this needs a purpose, not a fucking chasing a reason."*

§1 and §5.1 define exactly that page: one image that is the way into rustmapper (install, what happens to a URL in
order, where it bites, the one key, the file, who reads it next), a page under it that is lookup material, every mark
with a PURPOSE row, nothing with a size, no word naming what it is. The renders agree with the text. At 390 px
(`sheet-phone-day-390.png`) I can read every word, including `Received work item` in the mono face inside the box;
the night edition is a redraw with the same weights. That is the page I asked for.

The condition from round 1 stands and the PRD still names it: under option 3 the first screen says my flagship ships
with a stop-rule. What round 1 did not see, and what this review is mostly about, is that the live profile today is
not option 3. It is the page before all of this.

**Would I screenshot §5's product and send it?** The image, yes: it looks like a page from a manual a careful person
wrote, and nothing on it announces what it is. If someone asked me what it was I would say "the way into my crawler".
If a stranger asked, the PRD's own §11 risk is the honest answer: they might say "a flowchart". The page under it,
not yet (§4 below).

## 2. Must-fixes, ranked

Each: where (section, line of `docs/PRD.md`), what to change, why (my words or a source), and whether it is about
the PRD text or the product it defines.

### MF1. The default while I decide is the page I rejected, and the PRD says waiting is free (PRD text and product; §0 lines 31–33, §9.1 lines 440–449)

§9.1 line 448: *"Default while undecided: the branch stays unmerged; `main` and the live page do not change."* §0:
*"Until he decides, the branch stays unmerged and `main` does not change."* Written as if the live page were neutral.
It is not. I checked what is live:

- `main` (`gh api`, last commits `d253286` and `e9b111a`, both 9 Oct 19:38–19:40) serves `hero-day.svg` from the
  `chart` branch, whose last commit is `c488907`, "chart: soundings 2026-10-09", 9 Oct 19:40. That SVG's groups are
  `hero-row0`, `hero-row1`, …: the v11 "one sheet of the year" with repositories as rows by week. Its alt text on the
  live README: *"Ben Russell's 22 repositories by week, Sep 2025 to Oct 2026: Scrapy and rustmapper busiest, quiet
  Feb to Apr 2026."*
- That is the map I reviewed at 20:50 the same evening and rejected: *"It's trying to be a fucking map for no reason
  [...] tiny fucking islands [...] Is it based on the size of the project or how many commits? There's nothing about
  that teaches you anything."*
- The live facts lines print *"last commit 8 Aug 2026"* for rustmapper, the figure §7.3 of this PRD bans ("No commit
  totals, no 'last commit' (sweep-adjusted, contradicted the CI date)").
- PR #17 is open (`gh api .../pulls?state=open`: `17 v11.1/no-thesis Cut "I survey a web that is wrong about itself"
  from the sheet`). The PRD says so at §0 and §7.6. What it does not say is what that means: the thesis line I cut on
  9 Oct 19:39 (*"The wording is fucking weird survey the web that is wrong about itself come the fuck on"*) is still
  on the live sheet until that PR or this branch merges. (The SVG is glyph outlines, so I could not grep the words;
  the PR's title and its open state are the evidence.)

So "the live page does not change" means: strangers keep seeing the islands, the last-commit figure, and the
sentence I told you to kill, for as long as I take to decide about 0.1.4. The PRD presents that as the safe default
and recommends the option that takes the longest (1b: eight fixes in Rust-sitemap plus four items here).

Change §9.1 so the decision is sequenced, not a menu:

1. Add a row above the table, **"What is live while this is undecided"**: the v11 sheet (`chart` branch `c488907`),
   "last commit 8 Aug 2026", the thesis line pending PR #17. One sentence each, with the alt text quoted.
2. Say what is true of the pipeline and the PRD already knows (§5.4, §6): **options 1a/1b and 3 are not
   alternatives.** Merging now (as 2b or 3) and releasing 0.1.4 later gives 1a or 1b by itself at the next weekly run,
   because the cautions retire on `release-published` with no edit here (four of the eight; the other three need
   §10.9 first, which is work here, not in Rust-sitemap). The table's "What the pipeline does" column says this in
   each row and the recommendation ignores it.
3. Change the default to: **merge 2b now** (the image with its box, the open list cut to L1 and L7, the rest folded:
   no work in Rust-sitemap, one gate change here), then decide 1a/1b with the renders in hand. If the fix pass thinks
   3 is the better immediate merge, say why; either is better than what is live.
4. Open the PR. 8 Oct 09:04: *"all PRs need to be ready to merge"*; §7.6 marks that rule "not met today" and leaves
   it there.

Why: my 9 Oct 20:50 and 19:39 sentences are the standard this PRD claims, and the live page breaks both. The
hiring-side sources are one-voiced that the first screen decides: "profiles are often scanned for only seconds"
and the heading is "the 30-Second Scan" [S1]; "Total time: 30–90 seconds" [S2]; "recruiters spend '30 seconds on
your GitHub'" [S6]; "If the first screen does not answer these questions, adding more content usually creates more
work for the reviewer" [S4]. Every day of waiting, the first screen is the one I rejected.

### MF2. G10 and G1c narrow my rule on jokes further than I did (PRD text; §3 lines 83 and 92, §7.1 line 266)

G10's "what it means here": *"plain modern copy; at most a dry wink or two about the work, none nautical."* G1c:
*"on 9 Oct he overrode 'fun' for anything that names the theme."*

What I said (9 Oct 11:37): *"Don't say arg like a fucking pirate. Don't use pirate language. We're in a modern era.
[...] And if there's little things, little jokes you can throw in, like one word, one-off words that are referenced
being a pirate or some shit, like that's funny. Making it all about it too fucking much. No one wants that. It's just
cringy."* That is two rules, not one: no pirate talk and no running bit (cringy); a one-off word as a joke is allowed
(funny). The PRD keeps the ban and drops the allowance, then records in G1c that I "overrode fun". I did not. What I
overrode on 9 Oct is naming the theme and making everything about it. "Stunning and fun" (7 Oct) and "The images are
not cool enough" (8 Oct) still stand as goals; "not on the nose" is a constraint on how they are met.

Change G10's meaning column to my two rules in my words: *"plain modern copy; no pirate talk, no running bit; a
one-off word as a joke is allowed ('that's funny'); more than a couple is 'cringy'. Winks today: two, named in §7.1;
whether any wink uses the allowance is the writer's call."* Change G1c's trade sentence to: *"on 9 Oct he overrode
naming the theme and running bits; 'stunning' and 'fun' still stand and are judged at §8.3 q.6."* §7.1's wink row
("about the work, not the sea") should match G10 once G10 is corrected. This is about the PRD's record of my rule;
the two winks on the page today ("Boring under load.", "why engines are hard") are fine and need no change.

Why: a goal table "in the owner's words" that bans what I allowed will stop a later round from doing something I
said was funny, and the PRD's own §10.2 says the count of winks is review-held, so the rule text is all that holds it.

### MF3. G13 drops half of its own quotation (PRD text; §3 line 95; §1 lines 46–47)

G13 quotes *"It should be telling you about me, but with a layer of a theme of shipping"* and defines it as *"the page
is about him and his work, in the third person"*, held by the first-person test and THIS-REPO. The "layer" half of the
sentence, the manner, is held by nothing in the table. It lives in §1 ("A navigator would recognise a route strip, a
magenta track, a dotted danger line and a cream sheet. Nobody is told.") and is asked about only by §8.3 q.6, which no
round has yet answered (it was added in PRD round 1; the round-16 reviews predate it).

Change: split the row. G13 keeps "telling you about me" (third person, the position line, §8.1 item 6). Add G13a,
*"with a layer of a theme of shipping"*: meaning *"the manner is in the marks, never in a word (§1); a reader who
knows the forms recognises them, a reader who does not sees a clean route"*, held by *"review: §8.3 q.6, logged every
round; the first log is this round's answers"*. And ground §1's claim in a source rather than taste: INT 1 prints
routeing symbols in magenta by default ("Unless otherwise specified, symbols are printed on charts in colour, usually
magenta") while recommended tracks themselves are black dashed lines with arrowheads [S11]; a dotted or pecked line
encloses a danger [S12]. So the PRD's sentence is right about magenta for the routeing measure and the dotted line
for a hazard, and loose about "track" (a track is black). One citation and one word fixes it.

My own q.6 answer, for the log: I would screenshot the image. I would call it "the way into my crawler". A stranger
who did not know the forms would call it a route strip or a flowchart; one who did would see where the colours come
from. That is the right place for it to sit. The PRD should say that this is the intended reading, not only a risk.

### MF4. The renders I decide from are still not built (product; §9.1 lines 454–456, §9.3 lines 483–485)

Round 1 MF1 asked for the option-1 render; `LOG.md` declined it for that pass ("a build step, not a PRD edit") and
said *"the 1a render can be built now"*; its "Next round" line says to build it. Nothing was built: the only
`once-p1-lands/` sheets under `scratchpad/r6/build/` are rounds 00–06, from before the current image. Under MF1's
sequencing the 1a render is what tells me whether the Rust work is worth doing, so it is still owed. Put the paths
beside round-16's in §9.1 when it exists; until then §9.1 should say in its first line that the renders are not yet
produced, not only in §9.3.

Why: 9 Oct 20:50, *"is it accomplishing my goal? Not just what I'm saying."* I judge a first screen by looking at it.
"Bad impressions form faster and resist correction" was round 1's source for this [S13 in r01-1]; the blemishing
research adds the order condition: a small negative helps only when it comes *after* the positive and is minor, and
"The effect does not hold if the negative information is 'very strong'" [S8]. Whether the red box reads as minor or
strong is exactly what a render answers.

### MF5. Two product changes I ruled on in round 1 are built by nobody (product; §3 line 90, §5.3 line 171, §9.2, §10.5)

The facts lines still print *"coding agents (Claude) authored 45 of its 146 commits and co-signed 1 of his own 101"*
and Scrapy's *"71 of its 499 … 30 of his own 420"* (`README.md` lines 38 and 86; `page-desk-1.png`, `page-phone-2.png`,
`page-phone-4.png`). Round 1 ruled by my sentence (9 Oct 11:35, *"We don't need to show the commits […] it feels
lazy"*): off by default. `render_readme.py:459` still calls `agent_clause(r)` unconditionally and `chart.toml [facts]`
has no switch (I checked both). The PRD carries it honestly as "open" (G8). Carried forward, not repeated: it is a
one-line switch and a test, and the PRD's acceptance criteria (§8.1) do not include it, so nothing forces it before
merge. Add it to §8.1 as item 7: *"`[facts] agent_clause` exists and is `false` unless Ben sets it."* Same for the
theme strings in `chart.toml [copy]` (round 1 MF7, §10.8): the public config still reads *"The chart ends here. The
web doesn't."* (`chart.toml:39`) and `unit_chart = "SOUNDINGS IN COMMIT-DAYS"` (`chart.toml:35`).

Why: my sentence, and the PRD's own rule that a thing "ruled" is not "done" until it is held by a gate (§7, status
"open"). A page I merge with the counts still on it is a page that contradicts my words on its second screen.

### MF6. §2's "about 7 s" is below every outside source and is the number the whole device argument rests on (PRD text; §2 line 61)

§2: *"a screener, about 7 s (R4-F1: the six facts screened in about 7 s)"*. Every source I read this round gives a
longer first look: "scanned for only seconds" with a "30-Second Scan" heading [S1]; "30–90 seconds" [S2]; "about 30
seconds" as the quick first pass, then a recommended five minutes [S3]; "In the first minute, a recruiter should
understand your target role" [S4]; "30 seconds on your GitHub" [S6]. None of these is a measured study either; two of
the search summaries call the 30-second figure folklore. The PRD should say so: *"7 s is R4's estimate for the six
facts; practitioner guides say 30 s to a minute for the first look; none is measured."* Then the first-screen rule
(§8.3 q.4: name, what he builds, rustmapper and Scrapy, the link line on the first two phone screens) is justified by
"first screen", not by a number nobody measured.

## 3. The 19 goal rows against my sentences

| Row | Missing, softened, or reinterpreted? |
|---|---|
| G1 | Held as "review"; the proxy (q.1–4) is honest. "Stunning" is asked at q.6 now. Fine. |
| G1a | Held, and I can point at the three marks on `sheet-phone-day-390.png`: the bracket up the left, the gap in the track under the box, the thin line past the end bar. Right. |
| G1b | Held. The page reads as the work of someone who measures things and says where the figures came from. |
| G1c | **Softened** (MF2): "he overrode 'fun'" is not what I did. |
| G2, G5 | Held. No theme word on the image (ROUTE-WORDS; I read THEME_WORDS at `route.py:60–61`); none in the README prose except project facts. |
| G3 | Held, visibly: one left edge, one pitch, in all five sheets I looked at. |
| G4 | Held except the device check (§8.4, open) and the mid window (§9.3). The PRD says both plainly. |
| G6 | Held. The only words on both image and prose are the two exceptions the gate lists. |
| G7 | Held, and still the row that answers *"how is the data gathered?"* best. |
| G8 | **Open on the page** (MF5). The PRD says so; the product has not moved. |
| G9, G12 | Held. No ship, no rose, no cliff, no "unsurveyed" on the branch. On the live page: see MF1. |
| G10 | **Reinterpreted** (MF2): the allowance is dropped. |
| G11 | Held. The log sheet is off the page; its strings are still in the config (MF5, second half). |
| G13 | **Half dropped** (MF3). |
| G14 | Held on the branch; on the live page the thesis line stands until PR #17 or this branch merges (MF1). |
| G15, G16 | Held, the strongest two rows: T-NOSIZE and the PURPOSE table are exactly the tests for *"Is it based on the size of the project or how many commits?"* and *"needs a purpose"*. |
| G17, G18, G19 | Done as process. G19 now cites my 11 Oct (later) message and the PRD rounds; this review is that. |

Nothing I said is missing from the table. Three rows carry my words with a narrower meaning than I gave them, and
one of those (G13) is the sentence that decides §1.

## 4. The top of the page, as rendered

`sheet-phone-day-390.png`, top to bottom: my name in the serif, the two-line role, "rustmapper" and its one
sentence, `pip install rustmapper` with "0.1.3 · 8 NOV 2025", two rows of how it runs, the red dotted box with the
two catches, the Ctrl-C row, the file with its real field names, the hand-off line. `page-phone-1.png` shows the whole
sheet, the link line and "Ben Russell builds…" on the first screen; `page-phone-2.png` shows the pick, the facts line
with its commit counts, the platform note and the first three cautions. On the desk (`page-desk-1.png`) the whole
sheet, the link line, the three fact lines, the pick, the facts line, the six cautions and the code block are on one
screen, with the code block's three comment lines wrapped at the phone's 32 columns (§11 records that; it still
reads oddly in an 846 px column and the one-line fix in §10.16 is worth another try).

Do I want strangers to see the top first? The sheet, yes, as it is. The box, yes if the render under 1a shows the
sheet reads worse without it than with it, which I doubt; that is MF4. The second screen, no: a stranger's second
screen about me is a commit-authorship count and a six-item fault list, and the research in §5.2 says a fault list
helps only when it is short, comes after the positive, and each item carries its fix (four of six do). Option 2b
fixes the length and the order without touching Rust-sitemap, which is why MF1 makes it the default.

One thing that is right and the PRD should keep: there is no marketese on the page, no stats card, no badge row.
Every guide I read this round says the same about profile READMEs: "I don't want a manifesto. I want orientation"
[S1]; "A clean, minimal profile README is better than a flashy one" [S2]; "Keep it SHORT. No essays. No emoji walls"
[S6]; "a useful index, not a sticker board" [S4]; against "heavy auto-generated stats" [S5]. The page is on the right
side of all of them.

## 5. Research

### 5.1 What convinces a senior engineer or a hiring manager on a GitHub profile in 2026

Nine practitioner sources, none a controlled study (the search summaries say so, and so do I). Where they agree:

1. **Order.** Profile README and bio first, then pinned repositories, then each README, then commits and code
   [S1, S3, S6]. One lays it out as five questions in order: what role, which work to open first, can I test it, can
   I trust the code, how do I contact them [S4]. The PRD's Q1–Q5 is the same order with "contact" as §8.1 item 6.
2. **Time.** "Scanned for only seconds" / a 30-second scan [S1]; 30–90 s [S2]; a 30-second first pass, five minutes
   if they stay [S3]; "in the first minute" [S4]; "30 seconds" [S6]. See MF6.
3. **Few finished things.** "The mistake I see most often is candidates pinning ambitious but unfinished work" [S1];
   "three complete projects are better than six half-finished repos" [S4]; "Pin two to four strong projects" [S5];
   "Depth on a few well-maintained projects" over breadth [S3]. Two projects, four "Also", a fold of 15: the right
   shape.
4. **Honesty is read as a signal, faking as a red flag.** "Honest failure states and useful messages beat happy-path
   demos" [S1]; padding the graph is "a big red flag" [S7]; "Green squares are easy to fake" [S9]; "If your best work
   is private, do not fake it" [S4]. The page's measured figures with their source commits are the strongest version
   of this, and none of the sources asks for commit totals, which bears on MF5.
5. **What hurts.** Vanity metrics ("Stars and followers are vanity metrics" [S3]); "Work in progress" warnings
   without recent commits [S2]; stale pins, generic bios, starter README text [S4]; "awesome-list" repos and forks
   never touched [S6]. The live page's "last commit 8 Aug 2026" beside a Nov 2025 release is the kind of staleness
   S2 names; the branch prints neither.
6. **Seniority is judged on process.** Review governance, decision records, substantive review comments [S10];
   "architecture notes, migrations, and review examples" for seniors [S4]; commit messages as "the cheapest possible
   signal of how the person communicates" [S9]. The Working rules block with its dated cites is the page's answer; the
   facts lines' CI gates are another.

### 5.2 Do a tool's known faults on its author's own profile help or hurt?

Round 1 covered the two-sided-message literature (its S9–S12). This round adds the order and dose conditions, which
are what §9.1 turns on:

- **Blemishing effect** (Ein-Gar, Shiv, Tormala, *J. Consumer Research* 2012): "Small doses of mildly negative
  information may actually strengthen a consumer's positive impression", but only when the positive comes first, the
  negative is minor, and the reader is not processing hard; "The effect does not hold if the negative information is
  'very strong'", and under focused reading "presenting exclusively positive information still does seem to be more
  compelling" [S8]. An engineer deciding whether to try a crawler is a focused reader. So the box helps least with
  exactly the reader it is aimed at, unless it reads as minor.
- **Two-sided messages help the sceptical and hurt when the admitted flaw is central**: the 2022 IJCS study found the
  credibility gain only among sceptical readers; a 2016 study found a two-sided message cuts purchase probability
  "only when an important attribute is disclaimed" [S14, search summary]. "Never exits by itself" is a central
  attribute of a crawler.
- **Mixed results overall**: a 2021 *Social Sciences* review says the literature "has shown mixed results" and
  proposes tolerance for contradiction as a moderator [S15, search summary; the article page returned 404 on fetch].
- **Convention**: a "Known issues and limitations" section is standard and sits after Usage [S16, round 1's S9]; the
  FOSS guide says "clear limits build trust" [S17, search summary; page 410 on fetch].

So: faults on the profile help when they are few, minor-looking, after the positive, and each with its fix. The
image's box is two items inside the loop with one fix beside it; the page's open list is six items before the code
block with two unfixed. That is the case for 2b now (MF1) and the render before 1a/1b (MF4).

### 5.3 The device claim in §8.4

The one report the PRD cites as unverified I read directly: "Using `prefers color scheme` doesn't work as expected
in Github apps (android / ios) because they always return the `light` theme. I don't know if this is a bug of the
app or it isn't compatible with this feature" [S18]. Undated, one author. GitHub's own docs describe `<picture>` with
a dark source, a light source and a default `<img>` "in case neither of the other images can be matched" [S19]. §8.4's
pass condition ("the app shows `hero-phone-day` in both modes") is consistent with both; nothing to change, and the
check still has to be done on a phone.

## 6. What I checked and found correct

| PRD claim | Checked | Holds |
|---|---|---|
| 21 owner messages; appendix A quotes 15 | `grep -c '^## 2026'` = 21; appendix A lists the six left out | yes |
| round-16 gate: 0 fail, 4 warn, exit 2 | `round-16/gate.txt` | yes |
| `[position] text` and `[contact]` empty | `chart.toml:26, 30–31` | yes |
| `agent_clause` called unconditionally, no switch | `render_readme.py:459`; `grep agent_clause chart.toml` empty | yes |
| `[copy]` theme strings survive | `chart.toml:35–39` | yes |
| THEME_WORDS as listed in §7.1 | `checks/route.py:60–61` | yes |
| `edition` 0.1.3, 2025-11-08, scripts `rust_sitemap` | `stats.json` | yes |
| PR #17 open, head `v11.1/no-thesis` | `gh api pulls?state=open` | yes |
| "main and the live page do not change" is cost-free | live `chart` is v11 (`c488907`); alt "22 repositories by week"; "last commit 8 Aug 2026" | **no** (MF1) |
| the 1a render "can be built now" (LOG) | no new `once-*` directory since round 06 | not built (MF4) |
| §1: a navigator would recognise a magenta track and a dotted danger line | INT 1: routeing symbols magenta by default; recommended tracks black; danger lines dotted/pecked | mostly (MF3) |

## 7. Score

**7 / 10.** The document improved where I asked (G1a–c, 2b, "done", §5.4's two new columns) and it remains the one
place my rules, their gates and their gaps are written down honestly. It does not go higher because the one
decision it exists to put in front of me is framed with a hole in it: the default it calls safe keeps the page I
rejected live, and its recommendation is the slowest route out (MF1); because two of my sentences are carried with
a narrower meaning than I gave them (MF2, MF3); and because what round 1 ruled is still not built or required before
merge (MF5). Fix MF1 and I have a document I can decide from in one sitting.

## Sources

1. Underdog, "What Hiring Managers Look for on GitHub: Land Your 2026 Job",
   https://underdog.io/blog/what-hiring-managers-look-for-on-github — read in full: "profiles are often scanned for
   only seconds"; the "30-Second Scan" heading; "I don't want a manifesto. I want orientation"; "The mistake I see
   most often is candidates pinning ambitious but unfinished work"; "Honest failure states and useful messages beat
   happy-path demos"; nothing on listing known limitations.
2. TechInterview, "GitHub Profile Polish for Engineers: Pinned Repos, READMEs, What Recruiters Click On",
   https://www.techinterview.org/post/3233474626/github-profile-engineers/ — read in full: "Total time: 30–90
   seconds"; README order what / why / how to try / how it works / status; "A clean, minimal profile README is better
   than a flashy one"; "'Work in progress' warnings without recent commits" read as abandoned.
3. CoderCops, "GitHub profile as a hiring signal, 2026",
   https://blog.codercops.com/blog/github-profile-as-hiring-signal-2026 — read in full: the 30-second first pass
   "tells them almost nothing"; recommended five-minute order (graph, commit messages, README, tests, dependencies,
   PRs); "Stars and followers are vanity metrics"; "Depth on a few well-maintained projects"; "A sparse GitHub profile
   is not an absence of skill"; no section on profile READMEs or known limitations.
4. GreatFrontEnd, "Frontend Developer GitHub Profile: How to Stand Out to Recruiters (2026)",
   https://www.greatfrontend.com/blog/frontend-developer-github-profile — read in full: five reviewer questions in
   order; "In the first minute, a recruiter should understand your target role"; "If the first screen does not answer
   these questions, adding more content usually creates more work for the reviewer"; "a useful index, not a sticker
   board"; "three complete projects are better than six half-finished repos"; "If your best work is private, do not
   fake it"; seniors judged on "architecture notes, migrations, and review examples"; pinned READMEs should carry
   "known limitations with next steps".
5. McTaba Labs, "GitHub profile for job seekers", https://mctaba.com/kb/github-profile-job-seekers — read in full:
   "code quality, project structure, and how you think"; "Keep it concise. Three to four sections"; against "heavy
   auto-generated stats"; pin two to four; "WIP" commit messages "suggest chaos"; padding activity "is worse than a
   moderate amount of genuine activity".
6. Reskilll, "GitHub Profile That Gets You Hired: The 2026 Developer Portfolio Guide",
   https://blogs.reskilll.com/github-profile-gets-you-hired-2026-developer-portfolio-guide/ — read in full: profile
   README first, then pinned, then the graph; "Keep it SHORT. No essays. No emoji walls"; "30 seconds on your GitHub";
   what hurts: untouched forks, no-README repos, awesome-lists.
7. Reczee, "What do hiring managers see on my GitHub profile",
   https://www.reczee.com/blog/what-do-hiring-managers-see-on-my-github-profile — read in full: resume first, then
   GitHub for signals; profile README as a resume-style introduction; bio with location and employer; padding the
   graph is "a big red flag for your application"; nothing on stating limitations.
8. Stanford GSB Insights, "The Positive Effect of Negative Information" (on Ein-Gar, Shiv & Tormala, "When
   Blemishing Leads to Blossoming", *J. Consumer Research* 38, 2012),
   https://www.gsb.stanford.edu/insights/positive-effect-negative-information — read in full: "Small doses of mildly
   negative information may actually strengthen a consumer's positive impression"; conditions: positive first, the
   negative minor, low processing; "The effect does not hold if the negative information is 'very strong'"; under
   focused processing "presenting exclusively positive information still does seem to be more compelling".
9. Cadence (withremote.ai), "How to evaluate a developer's GitHub when you're not technical",
   https://cadence.withremote.ai/blog/evaluate-developer-github-non-technical — read in full: "Green squares are easy
   to fake"; "commit messages are the cheapest possible signal of how the person communicates under low stakes"; "Lots
   of strong engineers have thin GitHub profiles"; AI-generated repos "look pristine because they never met a real
   user, a real bug, or a real constraint".
10. SlateGit, "CODEOWNERS as a senior-engineer signal",
    https://slategit.com/blog/github-codeowners-senior-engineer-signal — read in full: seniority judged on whether the
    process "looks like something a team could survive"; review governance, decision documentation and substantive
    review comments as the signals; a one-line README mention "tells a skimming reader what they are looking at".
11. INT 1 (Nippon Foundation mirror of the IHO chart specification), section on routeing measures,
    https://nippon.zaidan.info/seikabutsu/1996/00179/contents/131.htm — read: "Unless otherwise specified, symbols are
    printed on charts in colour, usually magenta"; recommended tracks "dashed lines with arrowheads (colour black)";
    maritime limits of TSSs, precautionary areas, two-way and deep-water routes as a dashed line.
12. AM Nautical, "Nautical Chart Symbols Explained: A Mariner's Field Guide",
    https://www.amnautical.com/blogs/the-mariners-blog/nautical-chart-symbols-explained — read: "When any symbol
    appears inside a dotted or pecked danger line, the entire enclosed area should be treated as hazardous"; its claim
    that magenta is "exclusively" for lights conflicts with INT 1 (S11) and I did not rely on it.
13. Canadian Hydrographic Service, Chart 1, Section M examples,
    https://cartes-charts.gc.ca/publications/chart1-carte1/sections/m-tracks/examples-eng.html — read: the routeing
    measure entries (recommended route 28.1, deep-water route centreline as recommended track 27.3, TSS 20.1); colours
    are in the figure, not the text, so it supports the vocabulary only.
14. "When transparency pays off: Enticing sceptical consumers with two-sided messages", *Int. J. Consumer Studies*
    2022 (PDF mirror at
    https://edisciplinas.usp.br/pluginfile.php/7947675/mod_resource/content/1/2022%20Int%20J%20Consumer%20Studies%20When%20transparency%20pays%20off%20Enticing%20sceptical%20consumers%20with%20two%E2%80%90sided.pdf)
    and the 2016 salesperson study cited beside it in the search summary — search summary only this round (round 1
    read the PDF): credibility gain only among sceptical readers; purchase probability falls "only when an important
    attribute is disclaimed".
15. *Social Sciences* (June 2021) review of two-sided message persuasiveness, listing at
    https://doaj.org/article/e8cab7e0972b49ccbbcbf4b3073ad6e4 — search summary only (the page returned 404 on
    fetch): "mixed results", tolerance for contradiction proposed as a moderator.
16. Caltech Library README template, https://github.com/caltechlibrary/template — "Known issues and limitations"
    section after Usage (round 1's S9; re-cited for placement).
17. FOSShub, "README", https://www.fosshub.com/resources/development/readme/ — search summary only (410 on fetch):
    state early if experimental or pre-release; "clear limits build trust".
18. RodrigoTomeES, `prefers-color-scheme-hack` README, https://github.com/RodrigoTomeES/prefers-color-scheme-hack —
    read: "Using `prefers color scheme` doesn't work as expected in Github apps (android / ios) because they always
    return the `light` theme. I don't know if this is a bug of the app or it isn't compatible with this feature."
    Undated, one author.
19. GitHub Docs, "Quickstart for writing on GitHub" (the `<picture>` dark/light pattern),
    https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github
    — search summary: dark source, light source, default `<img>` "in case neither of the other images can be matched".
20. Instahyre, "GitHub profile checklist", https://resources.instahyre.com/blog/github-profile-checklist/ — search
    summary only (403 on fetch): 2–4 pinned projects; 40 half-finished repos read worse than 3 polished ones; the
    graph "the most over-rated GitHub metric".
21. Repository and live files read: `/home/user/wt-v12/docs/PRD.md`; `/home/user/wt-v12/docs/crit/prd/owner-messages.md`;
    `/home/user/wt-v12/docs/crit/prd/LOG.md`; `/home/user/wt-v12/docs/crit/prd/review-r01-{1,2,3}.md`;
    `/home/user/wt-v12/README.md`; `/home/user/wt-v12/chart.toml`; `/home/user/wt-v12/docs/BEN-TODO.md`;
    `/home/user/wt-v12/docs/crit/round6/SPEC.md`, `DECISIONS.md`; `/home/user/wt-v12/scripts/checks/route.py`;
    `/home/user/wt-v12/scripts/sheets/route.py`; `/home/user/wt-v12/scripts/render_readme.py`;
    `/home/user/wt-v12/tests/test_pipeline.py`; `/home/user/wt-v12/assets/stats.json`; `git show main:README.md`;
    `gh api repos/BenjaminSRussell/BenjaminSRussell/readme`, `.../commits?sha=chart`, `.../commits?sha=main`,
    `.../pulls?state=open`; `https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/hero-day.svg`
    (group ids); renders under `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/`
    (`gate.txt`, `sheet-phone-day-390.png`, `sheet-phone-night-390.png`, `sheet-desk-day-870.png`,
    `sheet-mid-day-746.png`, `page-desk-1.png`, `page-desk-2.png`, `page-phone-1.png` to `page-phone-7.png`).
