# PRD review round 4, reviewer 1: Ben, the owner, reading the PRD as the person who has to live with the page

11 Oct 2026. I read `docs/crit/prd/owner-messages.md` twice, end to end, before opening anything else. Then
`docs/PRD.md` (832 lines, at `92b1bef`), `docs/crit/prd/LOG.md` (rounds 1 to 3: applied and declined),
`docs/crit/prd/review-r03-1.md` (so that nothing below repeats it), `README.md`, `chart.toml` (`[position]`,
`[contact]`, `[copy]` at 20–40, C1 at 1000–1030, the ids and `fold = true` lines of the route entries),
`scripts/render_readme.py:455–475`, `scripts/checks/position.py:25–40`, `scripts/checks/data.py:56–74`,
`scripts/checks/route.py:60–70`, `scripts/checks/strings.py` (`BANNED`, 20 entries), `scripts/runcheck.py:1–12`,
`docs/BEN-TODO.md`, `docs/crit/round6/LOG.md` round 16, `assets/stats.json` (`edition`, the two `ci` records), the
round-16 `gate.txt`, and every `file:line` the PRD cites that I could print in one pass (56 of them; the result is
§6). I ran `python3 -m unittest`: 539 tests, OK, 22.7 s. Renders: every round-16 file named in the brief
(`sheet-phone-day-390`, `sheet-phone-night-390`, `sheet-desk-day-870`, `sheet-mid-day-746`, `page-desk-1`, `-2`,
`page-phone-1` to `-7`), the 1a sheet (`scratchpad/prd-r02/once-1a/sheet-phone-day-390.png`) and the 2b second
screen (`scratchpad/prd-r03/once-2b/page-phone-2.png`). Where I say what a file or a page contains, I opened it.

Verdict on the PRD: **7 / 10.** Round 3 did what I asked: §9.0 lists what only I do, the 2b render exists, C1's
wrong step under a release that exits is now a named gap, my 7 Oct sentences have a row (G1d), the q.6 answers have a
home. The LOG's own next-round question was whether I can answer (a), (b) and (c) from the PRD alone. (b) yes, (c)
nearly, (a) is mine and has been since 8 Oct. What stops a higher score is that the PRD now contradicts itself in
three places I would trip over on the day I merge: the option it recommends (2b) is shaped against the argument it
gives for it; the merge is blocked on my bio line while the same section says every week unmerged is the costliest
row; and §10.12 says no PRD round should run until the register has a test, and this one ran, and found drift again.

---

## 1. Is the product this PRD defines what I asked for?

**Yes.** The sentence that decides it is 9 Oct 11:37: *"It should be telling you about me, but with a layer of a
theme of shipping. [...] It has to be helpful knowledge. If you were a fucking real sailor, if you were a real
person, you'd want it to be helpful data that you're looking at [...] and it's in a cool format."* Tested by 9 Oct
20:50: *"Everything, single thing inside of this needs a purpose, not a fucking chasing a reason."*

§1 defines one image that is the way into rustmapper and lookup text under it; §5.1 gives every mark a row, a
question and a source; nothing on it has a size (G15); no word on it names what it is (G2, G5). The round-16 phone
sheet is that page: my name, what I build, the one project, the install line, two rows of what it does, the box with
the two catches, the one key, the file with its real field names, and the line to the project that reads the file.
That is what a stranger with a terminal open would want, in order. My 11 Oct instruction, *"Review and ensure this is
something I want to see rounds of reviews and research"*, is the yardstick the PRD's §8.3 opens with and is why this
review exists.

The yes has the same condition as rounds 1 to 3, and I do not repeat it as a must-fix: the page as it ships today
prints the agent-authorship counts on both facts lines (§8.1 item 7, blocking) and the retired theme strings sit in
the public `chart.toml` (item 8, blocking). Both are recorded and owned.

**Would I screenshot §5's product and send it?** The image, yes, and I would call it "how you get into my crawler",
the same words as round 3. Logged for G13a. The page under it: yes once items 7 and 8 are done and my line is in.

## 2. Must-fixes, ranked

Each: where (section, line of `docs/PRD.md` at `92b1bef`), what to change, why (my words or a source), and whether
it is about the PRD text or the product it defines.

### MF1. Option 2b folds the text of two marks that are drawn on the first screen (product the PRD defines; §9.1 row 2b line 530, §9.0 (c) lines 502–503, §10.19 line 655, §5.3 row 6 line 183)

The 2b row keeps L1 and L7 open and folds L4, L6, L2 and L5, and gives as its reason that *"an admitted fault
persuades only with its refutation beside it: L1 and L7 carry one, L4 and L6 carry none"*. Two of the four it folds
are the text for marks on the image's first screen:

- **S1** (`sheet-phone-day-390.png`, the first row of the route): *"by default also from sitemaps, certificate logs
  and Common Crawl"*. Its lever is **L2**: *"By default it asks crt.sh and Common Crawl about your domain.
  `--seeding-strategy none` asks no one."* (`README.md:50`). L2 carries a refutation; 2b folds it.
- **H0** (the dotted box): *"on https, pages behind a disallowed link wait"*. It has no lever on the image (round 3
  §4 said so). Its only explanation on the page is **L6**: *"On https, pages queued behind a link that `robots.txt`
  disallows wait for a new link to that host. The sign: `blocked by robots.txt`."* (`README.md:49`). 2b folds it.

So under 2b a stranger reads the fault on screen one and the sign of it is behind a click on screen two. I opened
`once-2b/page-phone-2.png`: two items, then the closed fold, no `blocked by robots.txt` anywhere on that screen. That
breaks G6 as the PRD states it (*"the image keeps what a list cannot show, the text keeps what you copy or look
up"*): the sign and the flag are lookups, and the page hides them for the two facts the image chose to draw.

Change: define 2b's open list by a rule, not a count. **Open: every item that is either the text of a mark on the
first screen or carries its lever. Fold the rest.** Today that is L1, L7, L2, L6 open (four), and L4, L5 folded. The
fold then holds six (L4, L5, L3, X3, X2, X1), under the cap of 7, so §10.19 shrinks to two `fold = true` lines in
`chart.toml`, no cap change, no new test, and no reversal of round 13's ruling (`render_readme.py:670`: "back to 7,
for the open list and for the fold each"). §9.1's 2b cell: *"four items (L1, L7, L2, L6), each the text of a drawn
mark or with its lever; L4 and L5 folded"*. §9.0 (c): the same. Rebuild the 2b render from the two-line fixture so I
see the second screen before I say yes.

Why: 9 Oct 11:37, *"It has to be helpful knowledge. If you were a fucking real sailor [...] you'd want it to be
helpful data"*: the sign of the stall is the thing you need in minute two, and the image put the stall on screen one.
9 Oct 11:35 (G6): *"the images and the text need to kind of like either differentiate themselves"*, which the PRD
reads as a contract between them, and 2b breaks the contract for the two rows it drew. The literature the PRD itself
cites (Allen 1991, O'Keefe 1999, via `LOG.md` round 3) says the refutation has to be *beside* the claim; a fold is
not beside. Four is still "few": TechInterview's scan is "30–90 seconds" [S11], GreatFrontEnd's is "the first
minute" [S12], and NN/g's finding is that readers "jump around pages, skipping some content" [S10], so a four-item
list with bold levers is scanned, a `<details>` is not.

### MF2. The merge is blocked on my bio line while the PRD says every week unmerged is the costliest row (PRD text; §8.1 item 6 lines 394–398, §9.0 (a) lines 500–501, §9.1 row 0 line 526, the default bullet line 541)

§8.1 item 6: *"The page does not merge with the one line a visitor came for left blank"*, owner me, 6a the position
line, 6b one contact. §9.1 row 0: leaving `main` as it is *"keeps up a page that breaks G8, G13, G14, G15, §7.3 and
§7.5, and its job failed on 11 Oct. The costliest row in what strangers see"*. The default bullet: *"merge 2b now"*.
These cannot all hold. The position and contact slots have been on my list since round 4 (8 Oct, `BEN-TODO.md`
round-4 first ask) and round 5 (9 Oct, third ask), and `chart.toml:26, 30–31` are `""` on 11 Oct: I checked. The
evidence is that the line waits on me, and the PRD makes the rejected page wait with it.

The code already handles the empty slot the right way: `position.py:31` warns (POSITION-EMPTY), the renderer omits
the slot, and a push to `main` that touches `chart.toml` triggers a build (`profile.yml` push paths, §6), so the day
I set the line the page prints it without anyone else's work.

Change: item 6 stops blocking the merge. Rewrite it: *"6. Owner: Ben. `[position] text` and one of `[contact]
linkedin` / `resume` are set before or after the merge; POSITION-EMPTY stays a warning (`position.py:31`) and the
slot prints on the next build after he sets them. Not a merge blocker: §9.1 row 0 is the cost of waiting."* §9.0 (a)
keeps its place as the first thing only I do, with "not needed for the merge" after it, as (c) already says of
1a/1b. §10.21's CONTACT-EMPTY stays as a warning, not a blocker. §8.3 q.4's link-line tick becomes "one contact
beyond Email, or the slot omitted with POSITION-EMPTY on the build".

Why: 8 Oct 09:04, *"all PRs need to be ready to merge"*; the PRD's own row 0. Round 1's reviewer 1 moved item 6 to
blocking before round 2 costed row 0; with row 0 costed, the earlier ruling is the wrong trade and I reverse it.

### MF3. §10.12 says no PRD round runs until the register has a test; this round ran, and found drift again (PRD text, and one session item; §10 row 12 line 648, §0 first bullet lines 22–29, §6 line 248, §7.3 line 317)

§10.12, "Blocks: the next PRD round (the register cannot score above 7 while it is checked by nobody; three rounds
have each found drift in it with no code change)". This is the next PRD round. `tests/test_prd.py` does not exist
(`ls tests/test_prd.py`: no such file). I printed 56 of the PRD's cites in one pass (§6 below). Two have drifted
with no code change since `027f081` (`git diff --stat 027f081..HEAD -- . ':!docs'` is empty, I ran it):

- §6 line 248: *"`runcheck.py:7` still says it 'probes four behaviours'"*. Line 7 is blank; the sentence is line 8.
- §7.3 line 317: *"`data.calendar` is `info` when no GraphQL window was fetched (`checks/data.py:70`)"*. The `info`
  finding is line 69; line 70 is `for r in stats.get("repos", []):`.

Both are off by one, both harmless, and both are exactly what §10.12's test would have caught, as it says. A rule
that blocks a round and is then ignored by the round is worse than no rule: I stop trusting the others.

Change: one of two, and the PRD says which. Either (i) `tests/test_prd.py` is written before round 5, with the list
§10.12 already gives, and §10.12's status reads *"open; round 4 ran without it and found two line drifts (§6
`runcheck.py:7` → 8; §7.3 `data.py:70` → 69)"*; or (ii) §10.12's "Blocks" becomes "nothing" and §0's first bullet
says the register is hand-checked each round and will stay so. I want (i): the test is a loop over the document, and
the drift is the kind that only a loop catches. Fix the two lines either way.

Why: 9 Oct 20:50, *"Use multiple agents and review and check and review and check"*: a check that nobody runs is not
a check. 11 Oct 01:12, *"review all of the do and donts and specifically all of the rules [...] and review how they
are implemented"*: the PRD's own rule for itself is implemented by nothing.

### MF4. The device check is a fourth thing only I can do, and §9.0 says there are three (PRD text; §9.0 lines 498–505, §8.4 lines 452–466, §10 row 4 line 640)

§9.0: *"Everything else is a session's."* §8.4: *"Owner: Ben (the session has no device)."* §10.4: owner Ben, blocks
the merge through §8.3 "Done". So the one list of what waits on me leaves out one of the things that waits on me,
and the thing it leaves out is a blocker. And §8.4 asks me to *"Log the result in `docs/crit/round6/LOG.md` under the
round that merges, with the screenshots' paths"*: I will look at the page on my phone; I will not write a LOG entry
in a repository file in a session's format.

Change: §9.0 gains *(d) Open the profile on an iPhone in Safari, light and dark, and in the GitHub app, and send the
screenshots (§8.4); a session writes the LOG entry from them.* §8.4's "Log the result" line becomes the session's.
If (d) is to block the merge, say so in (d); if it is to happen on the live page after the merge (the realistic
order, since the branch is not on `main` and a phone sees `main`), say that instead and move §10.4's "Blocks" to
"the first week after merge". I want the second: I cannot look at this branch on my phone until it is live.

Why: 9 Oct 11:32, *"I'm looking at iPhone. I think the iPhone experience is going to be a very common one"*: I said
I would look, and the PRD should ask me for the look, not the paperwork. StatCounter's September 2026 figure is
58.99 % of web traffic on mobile [S7]; the look matters and the LOG line does not.

### MF5. "Stunning and fun" is held by the one question that cannot fail (PRD text; G1 line 89, G1c line 92, §8.3 q.6 lines 441–444, "Done" line 446)

7 Oct 15:30 is my first sentence: *"world class one of a kind beautiful profile readme that is stunning and fun and
tells a lot about me"*. G1c says *"'Stunning' and 'fun' still stand as goals, judged at §8.3 q.6"*. §8.3 q.6 opens
*"Advisory"*. "Done" counts three yeses on q.1–4; q.6 is logged and never counted. So the first thing I asked for is
the only goal in the table whose holder has no pass condition, while the sentences I said later all have gates. That
is the softening the brief asks me to look for.

Change: q.6's first line becomes a bar line, the same shape as q.4's "name the sentence": *"Would you screenshot the
image and send it to someone? A no is a must-fix, and the reviewer says what would make it a yes."* The second line
(what they would call it) stays logged for G13a; the third (G1d, where the care shows) stays as it is. "Done" reads
*"three reviewers answer yes to questions 1–4 and to q.6's first line"*. G1 and G1c point at that line. q.5 stays
advisory; it is the reviewer's taste about shipping, not my word.

Why: it is my sentence and it was first. The sources on first impressions say the judgement is made before any
reading: "between 17 and 50 milliseconds", on "visual complexity" and "prototypicality", with a strong preference
for designs that look "both simple (low complexity) and familiar" [S3]; a profile should be "a useful index, not a
sticker board" [S12]; "A clean, minimal profile README is better than a flashy one" [S11]. The round-16 sheet is
simple and familiar, which is why three reviewers in rounds 2 and 3 said yes to the screenshot question; making it
a bar costs nothing today and stops a later round trading it away.

## 3. The 19 goal rows against my sentences

| Row | Missing, softened, or reinterpreted? |
|---|---|
| G1 | Softened: held by an advisory question (MF5). |
| G1a | Held; the bracket, the gap and the hand-off line are on `sheet-phone-day-390.png` where it says. |
| G1b | Held. |
| G1c | Softened the same way as G1 (MF5); the 9 Oct trade is carried in my words and is right. |
| G1d | Held now (round 3); the third line of q.6 is the right place. |
| G2, G5 | Held; `THEME_WORDS` is the 18 words §7.1 lists (`route.py:60–61`, I read them). |
| G3 | Held on all five sheets I opened. |
| G4 | Held except §8.4 (mine; MF4) and §9.1b (default a stands). |
| G6 | Held today; **broken by option 2b** for S1/L2 and H0/L6 (MF1). |
| G7 | Held; the strongest row. |
| G8 | Open on the page, blocking (§8.1 item 7). Not repeated. |
| G9, G12 | Held on the branch. |
| G10 | Held; the two winks are fine and nothing bars a third. |
| G11 | Held; the retired strings block the merge (item 8). Not repeated. |
| G13, G13a | Held; the q.6 log in `LOG.md` works. |
| G14 | Held on the branch; §10.10 open. |
| G15, G16 | Held. |
| G17–G19 | Done as process; G19's cell now cites my 11 Oct sentence, right. |

Nothing is reinterpreted. One goal is softened (G1/G1c), and one is held today and broken by the recommended option
(G6).

## 4. The top of the page, as rendered

`sheet-phone-day-390.png`: my name, the two-line role, "rustmapper" and its sentence, `pip install rustmapper` with
`0.1.3 · 8 NOV 2025`, `rust_sitemap crawl` and what it starts from, the fetch row, the red dotted box (H0, H1), the
Ctrl-C row, `data/sitemap.jsonl` with its fields, "sorted 21 ways by ideal-url-organizer". The night sheet is a
redraw, not an inversion; the mid sheet at 746 has the same rows at one pitch. `page-phone-1.png`: the whole sheet,
the link line (rustmapper · PyPI · Scrapy · Email) and "Ben Russell builds…" on one screen. `page-phone-2.png`: the
pick, the facts line with the counts (blocking), the platform note, "Before you run 0.1.3:" and the first three
items. `page-desk-1.png`: all of that, the six items, the fold and the code block on one screen, the comment lines
wrapped at 32 columns (§11).

Do I want strangers to see the top first? The sheet, yes. It reads as a page from a manual by someone who measured
what he wrote, and the Google finding [S3] says that is the right first 50 ms. What I would change on it is already
sequenced and I do not repeat it: the date beside the install line and the two names for one tool (§9.1, a release),
and the competence line (CI passed 7 Oct 2026, 176 test functions, 16k lines) a screen below the fault box (round 3
§4). What is new this round is the second screen under 2b (MF1): the first screen draws two defaults and a stall,
and the recommended option hides their flag and their sign.

What is right and should stay: no stats card, no badge row, no first person, no "generated weekly" a visitor can
read, the fold of 15, "Also" and "Working rules" as the only headings. Every 2026 guide I read says the same thing
in its own words: keep "badge rows, stats cards, contribution snake animations, and long tech-icon grids out of the
top section" [S12]; avoid "Visitor counter widgets, animated stock 'coding' GIFs, long technology lists" [S11]; the
question is "What kind of engineer shows up if we hire this person?" [S9].

## 5. Research

### 5.1 What convinces a senior engineer or a hiring manager on a GitHub profile in 2026

Thirteen sources read in full this round, none of them read by the round-3 owner review (which used F1 Jobs, Reczee,
Noon, Rockstar, the pratfall and two-sided-message pages, OpenSSF, JHU, Snyk). Where they agree:

1. **Order and time.** Recruiters look at the profile page, then "scan pinned repos for ones that match the bullets
   they read on the resume", then open one or two; "Total time: 30–90 seconds" [S11]. The reviewer should know the
   target role "In the first minute" and read a pinned README in five [S12]. The Nexus IT playbook frames the profile
   scan as "In under a minute" and puts the contribution graph first only as "the quickest first pass", then pinned
   repositories, then "Start with the README" [S2]. GitHub's own docs say nothing about where the README sits
   relative to pins or how long it may be; the only rules are a public repository named for the user with a root
   `README.md` [S5], and up to six pinned items [S6]. So the first screen of the README is the one thing on the
   profile the owner controls entirely, and the PRD's "first screen" rule, not a seconds figure, is the right basis.
2. **What a reader is answering.** "What kind of engineer shows up if we hire this person?" [S9]; "Public GitHub
   should be treated as evidence, not a verdict" [S2]. Underdog's 2026 piece wants "recent, sustained work" over
   totals, "sensible trade-offs and narrow, finished projects", and a README that "states the problem, the reasoning,
   setup steps, an architecture overview, and a demo" [S9]. The route sheet is setup steps and a demo in one; the
   Working rules are the reasoning; the facts lines are the recent work.
3. **What hurts.** "Chaotic profiles full of unlabeled forks, half-finished experiments, and stale repos are harder
   to trust at a glance"; "Weak profiles often pin random coursework, abandoned experiments, or forks with no
   explanation" [S2]. "'Work in progress' warnings without recent commits" and "TODO sections in READMEs" read as
   abandonment [S11]. "Pinning ambitious but unfinished work, unexplained rewrites, vague commit messages" [S9]. The
   page prints none of these; what it does print is a release eleven months old beside a CI date three days old,
   which the PRD already prices (§9.1).
4. **Older hiring voices say the same, more bluntly.** Built In's 2018 panel: "Write code that is readable,
   well-formatted, well-tested, well-documented"; "what I'm really looking for is activity"; "We don't weigh GitHub
   profiles too heavily [...] not everyone codes as a hobby"; "GitHub should remain an imperfect window into a
   person's personal laboratory" [S1]. The 2026 search summaries add that recruiters "don't count your green
   contribution squares" and that "Quality of a few repos beats quantity of many" [S14].
5. **Reading behaviour.** "People rarely read online"; scanning "all of the text on a page, or even a majority, is
   still extremely rare"; they "jump around pages, skipping some content"; front-load, use lists and bold [S10].
   That is the case for four bold-levered items open (MF1) rather than two open and four under a click.
6. **The first 50 ms.** Aesthetic judgement forms "between 17 and 50 milliseconds", driven by visual complexity and
   prototypicality; users "strongly prefer website designs that look both simple (low complexity) and familiar (high
   prototypicality)" [S3]. The sheet is simple; it is "familiar" as a manual page, which is the double reading §1
   intends. This is why MF5 can make the screenshot question a bar without risk to today's page.
7. **Mobile.** 58.99 % of worldwide web traffic was mobile in September 2026 [S7]. Octoverse 2025 publishes nothing
   on how developers read GitHub by device [S17]; the PRD's "the phone the stricter constraint, the web the likelier
   reader" stays my sentence (9 Oct 11:32), not a measured share of GitHub readers.

### 5.2 Do a tool's known faults on its author's own profile help or hurt?

Rounds 1 to 3 covered two-sided messages, the blemishing effect and the pratfall effect. This round's sources add
two findings and one warning, and together they settle the shape of the list (MF1) rather than its existence:

- **Admitted faults raise credibility when they are specific and measured.** Spiegel (Northwestern): "negative
  reviews can have a positive impact because they establish credibility and authenticity"; purchase likelihood
  "peaks at ratings in the 4.0–4.7 range" and "begins to decrease as ratings approach 5.0"; displaying reviews at all
  lifts conversion "190%" for cheaper and "380%" for dearer goods [S4]. The analogy is loose (a product page, not a
  profile) and I say so; the direction is the same as Allen and O'Keefe. The Harvard interview study, via Adam Grant
  (search summary only, [S15]): 23 % of candidates named a real weakness, 77 % hid it in a humblebrag, and evaluators
  were "30 percent more interested in hiring the candidates who acknowledged a legitimate weakness". The page's
  faults are real ones with probes, not humblebrags.
- **The fault must not read as abandonment.** "'Work in progress' warnings without recent commits" and TODO
  sections read as abandonment [S11]; "ownership" means getting projects "into a usable state, not just starting
  them" [S9]; "put a note at the top of the README saying that development has slowed down or stopped" is the advice
  for a project that has [S13]. H1 on screen one ("0.1.3 never exits by itself") is the one item that can be read
  that way by a reader who has not reached the CI date on screen two. The release (1a) is the fix, and the PRD
  sequences it; nothing in the text can do it.
- **Limitations belong beside the claim, and a static list drifts.** The README-practice sources say limitations
  belong "close to the claims they qualify" and that a shipped list of known problems "is soon out-of-date" (Apache
  UIMA, search summary [S16]). The page answers both: the box at the stop where the fault bites, each item gated by a
  probe that retires it. 2b as written breaks the first half for L2 and L6 (MF1).

So: faults on the author's own profile help when each is measured, each carries its fix or its sign, each sits
beside the claim it qualifies, and the competence evidence comes first. Today's page does the first and third; 2b
with MF1 keeps the second; only a release does the fourth.

### 5.3 Two facts re-checked against the world today

- PyPI JSON for rustmapper: `info.version` 0.1.3, newest file uploaded 2025-11-08T19:52:42, releases 0.1.0 to
  0.1.3, nothing newer [S8]. `stats.json` `edition` agrees (0.1.3, 2025-11-08, scripts `["rust_sitemap"]`).
- The Rust-sitemap `ci` record in `stats.json`: success, 2026-10-07; Scrapy: success, 2026-10-08. The facts lines
  print both dates.

## 6. What I checked and found correct, and what drifted

| PRD claim | Checked | Holds |
|---|---|---|
| 539 tests pass | `python3 -m unittest`: Ran 539, OK | yes |
| round-16 gate: 0 fail, 4 warn, exit 2; the four named | `round-16/gate.txt` | yes |
| 28 plug-ins | `ls scripts/checks/`: 28 `.py` plus `__init__.py` | yes |
| `BANNED` has 20 entries | imported `strings.py`, `len(BANNED)` = 20 | yes |
| THEME_WORDS = the 18 words in §7.1 | `route.py:60–61` | yes |
| `[position] text`, `[contact]` are `""` | `chart.toml:26, 30–31` | yes |
| `agent_clause(r)` called unconditionally | `render_readme.py:459` | yes |
| `LIST_MAX_ITEMS = 7` "for the open list and for the fold each" | `render_readme.py:670` | yes |
| four `fold = true` today; L2, L6 open | `grep '^fold = true' chart.toml` = 4; `README.md:49–50` | yes |
| C1's two wordings name no `ends_by_itself` | `chart.toml:1005–1030` | yes |
| `position.py:31` warns on `""` | read | yes |
| the 2b render: two items, closed fold | `once-2b/page-phone-2.png` | yes |
| the 1a render: no box, Ctrl-C row unchanged | `once-1a/sheet-phone-day-390.png` | yes |
| 51 other `file:line` cites (tests, column.py, readme.py, route.py, profile.yml, chart.toml, tokens.py, publish_chart.py, repos.py, data/route.py) | printed each line | yes |
| `runcheck.py:7` "probes four behaviours" | line 8 | **off by one** (MF3) |
| `data.calendar` `info` at `checks/data.py:70` | line 69 | **off by one** (MF3) |
| `tests/test_prd.py` before the next PRD round (§10.12) | no such file | **not done** (MF3) |

## 7. Score

**7 / 10.** The PRD is the one honest record of my rules, their gaps and who owns each; round 3's fixes held and I
can now answer (b) and, with MF1's render, (c) from the document alone. It does not go higher because its
recommended option is shaped against its own argument (MF1); because it blocks the merge on a line it also says is
the costliest thing to wait for (MF2); because it set itself a rule for this round and did not keep it, and the
drift the rule was for is there again (MF3); because the list of what waits on me is short by one (MF4); and because
my first sentence is the only goal with no pass condition (MF5). Fix MF1 and MF2 and I merge 2b the day items 7 and
8 are done.

## Sources

Outside, read in full this round:

1. Built In, "Here's What 4 Companies Really Look for on Your GitHub Profile" (Andreas Rekdal, 8 May 2018),
   https://builtin.com/articles/what-companies-look-for-on-github — read: Raise, "Write code that is readable,
   well-formatted, well-tested, well-documented", "displays a pragmatic approach via the commit history"; CapTech,
   "what I'm really looking for is activity"; Mac & Mia, "We don't weigh GitHub profiles too heavily", "not everyone
   codes as a hobby", "GitHub should remain an imperfect window into a person's personal laboratory"; avoid
   "commits with environment variables included".
2. Nexus IT Group, "Recruit on GitHub: Step-by-Step Playbook 2026", https://nexusitgroup.com/recruit-on-github/ —
   read: the order (graph as "the quickest first pass", then pinned, then "Start with the README", then commits,
   then PR discussions); "In under a minute, the goal is not to decide whether someone should be hired"; "Chaotic
   profiles full of unlabeled forks, half-finished experiments, and stale repos are harder to trust at a glance";
   "Public GitHub should be treated as evidence, not a verdict"; stars and followers "should never carry the
   evaluation on their own".
3. Google Research blog, Javier Bargas-Avila, "Users love simple and familiar designs – Why websites need to make a
   great first impression" (29 Aug 2012),
   https://research.google/blog/users-love-simple-and-familiar-designs-why-websites-need-to-make-a-great-first-impression/
   — read: "between 17 and 50 milliseconds"; the two factors, visual complexity and prototypicality; "users strongly
   prefer website designs that look both simple (low complexity) and familiar (high prototypicality)".
4. Spiegel Research Center, Northwestern, "How Online Reviews Influence Sales" (page dated 4 Dec 2025, findings
   first published 2017), https://spiegel.medill.northwestern.edu/how-online-reviews-influence-sales/ — read:
   "purchase likelihood typically peaks at ratings in the 4.0 – 4.7 range" and "begins to decrease as ratings
   approach 5.0"; "negative reviews can have a positive impact because they establish credibility and
   authenticity"; conversion "increased 190%" (lower-priced) and "380%" (higher-priced) with reviews shown; the
   page gives no method for this report.
5. GitHub Docs, "Managing your profile README",
   https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
   — read: shown "if all of the following are true" (public repository named for the user, root `README.md`, any
   content); nothing on placement, length, images or HTML.
6. GitHub Docs, "Pinning items to your profile",
   https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/pinning-items-to-your-profile
   — read: "Select up to six repositories and gists, combined"; nothing on where pins sit relative to the README.
7. StatCounter, "Desktop vs Mobile vs Tablet Market Share Worldwide",
   https://gs.statcounter.com/platform-market-share/desktop-mobile-tablet/worldwide — read: September 2026, mobile
   58.99 %, desktop 39.26 %, tablet 1.76 %.
8. PyPI JSON for rustmapper, https://pypi.org/pypi/rustmapper/json — read: `info.version` 0.1.3; newest file
   2025-11-08T19:52:42; releases 0.1.0–0.1.3; summary "Sitemap crawler and URL discovery tool built with Rust (256
   workers, sharded frontier, WAL persistence, optional Redis)"; nothing newer.
9. Underdog, "What Hiring Managers Look for on GitHub: Land Your 2026 Job" (19 Jun 2026),
   https://underdog.io/blog/what-hiring-managers-look-for-on-github — read: "What kind of engineer shows up if we
   hire this person?"; "recent, sustained work" over totals; ownership as getting projects "into a usable state";
   a strong README "states the problem, the reasoning, setup steps, an architecture overview, and a demo"; four
   polished pins beat six random ones; what hurts: "Pinning ambitious but unfinished work, unexplained rewrites,
   vague commit messages".
10. Nielsen Norman Group, Kate Moran, "How People Read Online: New and Old Findings" (5 Apr 2020),
    https://www.nngroup.com/articles/how-people-read-online/ — read: "People rarely read online"; scanning "all of
    the text on a page, or even a majority, is still extremely rare"; "They still jump around pages, skipping some
    content"; front-load, "bulleted lists and bold text", clear headings, plain language; nothing on the first
    screen or mobile.
11. TechInterview, "GitHub Profile Polish for Engineers: Pinned Repos, READMEs, What Recruiters Click On" (updated
    30 Jun 2026), https://www.techinterview.org/post/3233474626/github-profile-engineers/?format=md — read: profile
    page first, then "They scan pinned repos for ones that match the bullets they read on the resume"; "Total time:
    30–90 seconds"; "2–3 sentence description"; "A clean, minimal profile README is better than a flashy one";
    flags "Visitor counter widgets, animated stock 'coding' GIFs, long technology lists", "'Work in progress'
    warnings without recent commits", TODO sections; nothing on mobile.
12. GreatFrontEnd, "Frontend Developer GitHub Profile: How to Stand Out to Recruiters (2026)" (20 Jul 2026),
    https://www.greatfrontend.com/blog/frontend-developer-github-profile — read: the five reviewer questions (role,
    which work first, can I test the UI, "Can I trust the code?", contact); "short enough to scan and specific
    enough to direct attention"; "Do not use all six just because the slots exist"; "Keep badge rows, stats cards,
    contribution snake animations, and long tech-icon grids out of the top section"; "a useful index, not a sticker
    board"; "In the first minute"; "Clean folders, recent fixes, no secrets, and readable project notes".
13. Make a README, https://www.makeareadme.com/ — read: the section order (Name … Usage … Roadmap … License,
    Project status); "show the expected output if you can"; "the smallest example of usage that you can
    demonstrate"; on a stalled project, "put a note at the top of the README saying that development has slowed
    down or stopped completely"; "too long is better than too short".

Search summaries only (the page itself refused the fetch or was not opened; cited as summaries):

14. Search, `what hiring managers look for in a GitHub profile 2026 senior engineer` (Underdog, Instahyre,
    TechInterview, Medium, Nexus IT, Parse.gl, Reczee) — summary: "Quality of a few repos beats quantity of many";
    recruiters "don't count your green contribution squares"; "many senior developers don't contribute to open
    source, and that this is a valid choice"; "I didn't find hiring-manager research from 2026 that directly covers
    senior candidates". Instahyre (403) and Medium (403) could not be read.
15. Search, `admitting weaknesses makes you more persuasive HBR study candidates disclose flaws` (WEF and Quartz
    on Adam Grant) — summary: the Harvard interview study, 23 % named a real weakness, 77 % a humblebrag, evaluators
    "30 percent more interested in hiring the candidates who acknowledged a legitimate weakness"; self-promotion
    "not significantly more likely to get job offers". WEF (403) and Quartz (403) could not be read.
16. Search, `README "known issues" OR "limitations" section open source trust` (FOSSHub, SFM docs, DNSResolver PR
    #146, Apache UIMA-998, standard-readme) — summary: limitations belong "close to the claims they qualify"; a
    status section (stable / preview / occasionally maintained / archived); UIMA: a shipped list of known problems
    "is soon out-of-date". FOSSHub (410) could not be read.
17. Search, `GitHub Octoverse 2025 mobile app usage share` (github.blog 28 Oct 2025, It's FOSS, others) — summary:
    no figure on reading GitHub by device; headline numbers only.

Repository files and renders:

18. `/home/user/wt-v12/docs/PRD.md` (at `92b1bef`); `/home/user/wt-v12/docs/crit/prd/owner-messages.md`;
    `/home/user/wt-v12/docs/crit/prd/LOG.md`; `/home/user/wt-v12/docs/crit/prd/review-r03-1.md`;
    `/home/user/wt-v12/README.md`; `/home/user/wt-v12/chart.toml` (20–40, 563, 667, 900, 1000–1035, 1059–1419 ids,
    the `fold = true` lines); `/home/user/wt-v12/scripts/render_readme.py` (455–465, 665–675);
    `/home/user/wt-v12/scripts/checks/position.py` (25–40); `/home/user/wt-v12/scripts/checks/data.py` (56–74);
    `/home/user/wt-v12/scripts/checks/route.py` (43, 60–62, 70); `/home/user/wt-v12/scripts/checks/strings.py`
    (`BANNED`); `/home/user/wt-v12/scripts/runcheck.py` (1–12); `/home/user/wt-v12/scripts/checks/` (listing);
    `/home/user/wt-v12/docs/BEN-TODO.md`; `/home/user/wt-v12/docs/crit/round6/LOG.md` (round 16);
    `/home/user/wt-v12/assets/stats.json` (`edition`, `ci`); `/home/user/wt-v12/.github/workflows/profile.yml`
    (13, 25, 106, 160); the test files at the lines the PRD cites (`tests/test_route.py`, `test_round6.py`,
    `test_proof.py`, `test_pipeline.py`, `test_round7.py`, `test_round12.py`, `test_round13.py`,
    `test_round15.py`); `python3 -m unittest` (539, OK); `git diff --stat 027f081..HEAD -- . ':!docs'` (empty).
19. Renders: `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/`
    (`sheet-phone-day-390.png`, `sheet-phone-night-390.png`, `sheet-desk-day-870.png`, `sheet-mid-day-746.png`,
    `page-desk-1.png`, `page-desk-2.png`, `page-phone-1.png` to `page-phone-7.png`, `gate.txt`);
    `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/prd-r02/once-1a/sheet-phone-day-390.png`;
    `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/prd-r03/once-2b/page-phone-2.png`.
