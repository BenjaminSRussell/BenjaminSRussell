# PRD review round 6, reviewer 2: A product manager who has shipped from PRDs and rejects the vague ones

11 Oct 2026. Branch `v12/purpose`, worktree `/home/user/wt-v12`, HEAD `b6cca2c` (the round-5 fix commit). I read
`docs/PRD.md` end to end (933 lines, 20,277 words by `wc -l -w`, which agrees with the header; the reading-order
subset §1, §2, §4, §5, §8, §9, §11 is 9,335 words by `wc -w` over those line ranges, which also agrees), every message
in `docs/crit/prd/owner-messages.md`, `docs/crit/prd/LOG.md` rounds 1–5 in full (nothing below repeats a fix those
rounds applied; where I touch a declined item I say so), my own round-5 review and the must-fix headings of
`review-r05-1.md` and `review-r05-3.md`, `docs/crit/round6/LOG.md` round 16 (lines 1101–1175), `README.md` on the
branch (lines 36–40, 84–88, 149–152), `chart.toml` 20–40 and 1250–1260, `scripts/render_readme.py` 455–462,
`scripts/checks/column.py` 45–50, `scripts/checks/alt.py` 48–52, `scripts/runcheck.py` 1–12, `scripts/publish_chart.py`
1–16, `tests/test_route.py` 827–831, `.github/workflows/profile.yml` 10–30, `docs/crit/prd/renders/round-16/gate.txt`.
I ran: `python3 -m unittest` (539 tests, OK, 24 s); `ls scripts/checks/*.py | grep -v __init__ | wc -l` (28);
`python3 scripts/check.py --tier fast` on the committed tree with no build (`4599 fail · 8 warn · 0 error`, exit 1, as
§10.7 says); `git diff --stat 027f081..HEAD -- . ':!docs'` (empty: no product file has changed in six PRD commits);
`grep` for `agent_clause` in `chart.toml` (none) and `keep-current` in `publish_chart.py` (none); `grep -n "fold =
true" chart.toml` (lines 1257, 1276, 1308, 1357: L3, X3, X2, X1; L4 and L5 are not folded); and `git show
<sha>:docs/PRD.md | wc -l -w` for each of the six PRD commits. Renders: round-16 `sheet-phone-day-390.png`,
`sheet-desk-night-870.png`, `page-desk-1.png`, `page-phone-2.png`. Outside: 16 sources (Sources, at the end).

My brief is the document as a PRD: could a builder who was not in the room build and accept this product from it
alone, is every requirement testable and every must tied to a criterion, are the non-goals explicit, are the open
decisions decidable, is anything said twice, is it longer than it needs to be or missing a section, and does it
mistake its own history for requirements.

## 1. Is the product this PRD defines what he wants, by his own words?

**Yes.** The sentence that decides it is 9 Oct 11:37: *"It has to be helpful knowledge. If you were a fucking real
sailor, if you were a real person, you'd want it to be helpful data that you're looking at. You're going through,
you're like, oh, it's very helpful, and it's in a cool format."* The phone sheet (`sheet-phone-day-390.png`) is that
sentence drawn: the install line with the release's date, the command and where it looks by default, what each host
feels, the two catches in a dotted box, the one key that stops it, the file with its real field names, and which of
his other tools reads it next. I matched it to §5.1 row by row: T1, T2, R0, R1, R2, R5, R6, S1, F1, H0, H1, C1, R12,
R13 and R15 are drawn as the table says; S2 and W1 are not, as the table says. Nothing on it is a count or an
ornament, which is his 20:50 test (*"Everything, single thing inside of this needs a purpose, not a fucking chasing a
reason"*). The desk page (`page-desk-1.png`) under it is the lookup material of §1: the link line, one sentence of
what he builds, Languages, Stack, the pick, the facts line, the cautions with a lever each, the code block.

The judged lines §8.3 asks of every reviewer, so the log has them: **q.1, first line (G3a).** I had read §1 before I
looked, as §8.3 now says a PRD reviewer has; the sentence I would have written from the phone sheet is *"pip-install
rustmapper, run `rust_sitemap crawl` on a URL, it fetches twenty pages at a time per host, waits behind robots.txt on
https and never stops on its own, one Ctrl-C writes `data/sitemap.jsonl`."* A tool, an install, a command, an output.
**q.6.** Yes, I would screenshot it and send it; I would call it "a tool's whole run drawn as one route". Third line
(G1d, G1e): the care is in the release date set small in grey beside the install line, the gap the magenta track
leaves under the dotted box, and the night edition being a redraw (heavier strokes, the same cream-to-ink
relationship reversed by hand, `sheet-desk-night-870.png`), not an inversion. Someone who designs for a living would
see one left edge and one pitch before anything else.

**His last message, answered straight.** *"Review and ensure this is something I want to see rounds of reviews and
research"* (11 Oct, later). The product: yes, by the sentences above. The rounds: this is the sixth PRD round, and
`git diff --stat 027f081..HEAD -- . ':!docs'` is still empty. In those six commits the PRD went from 8,287 words
(`9e3db34`) to 12,505, 15,948, 17,288, 18,825 and now 20,277, while the four code changes it says block the merge
(`[facts] agent_clause`: not in `chart.toml`; the five `[copy]` keys: still at lines 35–39; `fold = true` on L4 and
L5: not set; `--keep-current`: not in `publish_chart.py`) have been "open; blocks the merge" since rounds 1, 2, 4 and
5. His 9 Oct 20:50 asks for *"at least 10 reviews of, is it matching what I'm saying? Is it doing what I'm saying?"*
A review of a document cannot answer "is it doing what I'm saying"; only a build can. What he wants rounds of is the
page against his words, and the page has not moved since `027f081`. MF1 and MF2 are about that.

## 2. Verdict on the document

**6 / 10 as a PRD**, down from my 7 in round 5. Everything I asked for in round 5 was applied or declined with a
reason I accept (the status has an exit, §8.6 holds the first merge, §10.13 and §10.20 are closed, the glossary
exists, the "verified" clauses are gone, §8.5 says what Ben does with the email). §5.1 and §5.4 remain the
best-written requirements in this series, and every "must" I grepped (19 lines) still resolves to a gate, a test or
a ticked line in §8.3. The non-goals are explicit and the renders break none. The facts I re-checked reproduce.

What costs it a point this round rather than earning one: the document wrote itself a stop rule in §0 and the header
("no PRD round 6 until a fix round has done…"), and the rule was broken by this round within hours, because the
owner's own sentence asked for rounds; a PRD that schedules its own reviews and then cannot keep the schedule is
carrying process it has no authority over (MF1). Its definition of Done requires three reviewers' yes on the merge
candidate, and the sequence it prints as the next step has no round in which anyone could say it (MF2). It grew
1,452 words in a round whose PM reviewer asked for 830 to go, and the growth is status, operations history and
quoted evidence (MF3). One decision has seven homes and had to be rewritten in all seven when the recommendation
flipped in round 5 (MF4). §10 is now a 24-row backlog with no rank, 14 rows owned by a party the document says does
not exist until Ben opens a session (MF5). Three of §9.2's decisions have no decide-by and no default (MF6). None of
these needs a new section; five of the six are deletions or a column.

## 3. Must-fixes, ranked

### MF1. The PRD carries a review schedule and a stop rule it has no authority over, and the rule was broken the day it was written (PRD; and the product it keeps from shipping)

- **Where:** header, lines 3–7 (*"Next step, in order: a product fix round on §8.1 items 7 and 8, §10.19 and §10.23
  … then the PR (§10.17), then his yes. PRD review rounds stop at approval, and none runs before that fix round (§0)"*;
  *"a session, which is open: his 11 Oct message was typed in it"*); §0 last bullet, lines 44–48 (*"**Stop rule:** no
  PRD round 6 until a fix round has done §8.1 items 7 and 8, §10.19 and §10.23 and the branch has a PR"*; *"his 11 Oct
  sentence's object is 'something I want': the reviews are the means"*); §10 preamble, lines 726–728 (*"a session-owned
  row that blocks the merge is done in the next session before any further PRD round"*); appendix D G19, line 918
  (*"the PRD rounds stop at approval (header, §0)"*).
- **What I checked:** this is PRD round 6; the four changes the stop rule names are not made (the greps in the
  preamble); no PR exists for the branch (§10.17 still "open"). The sentence that triggered this round is his, verbatim
  in `owner-messages.md`: *"Review and ensure this is something I want to see rounds of reviews and research"*. The
  PRD's gloss on it (line 46–47: the reviews are the means, the object is the page) is the session reading his
  sentence against its plain words to justify a rule he did not set. The header's clause "a session, which is open:
  his 11 Oct message was typed in it" is a claim about the present that is false the moment the session closes, inside
  a document whose own rule (line 3) is that the text changes only when the product changes.
- **What to change:** delete the stop rule from §0 (lines 44–48, from *"**Stop rule:**"* to the bullet's end) and the
  "Next step, in order" and "which is open" clauses from the header (lines 4–7), and the "before any further PRD round"
  clause from §10's preamble (line 728). Replace them with one sentence in the header: *"**Reviewed:** the page is
  reviewed against §8.3 whenever it changes or Ben asks (9 Oct 20:50; 11 Oct); this text is corrected when a review
  finds it wrong, and not otherwise."* The sequence (fix round, PR, his yes) is a plan, and its one home is
  `docs/crit/prd/LOG.md` "Next round", where it already is. G19's cell keeps his words and loses "the PRD rounds stop
  at approval". The product half of this must-fix is the same as rounds 1–5's: make the four changes; a PRD round is
  not the place to do it and I do not ask this round to.
- **Why:** his words first: 20:50, *"Use multiple agents and review and check and review and check"*, and 11 Oct
  (later), *"rounds of reviews and research"*: the rounds are his to call, and a document that forbids one he has just
  called is wrong by his yardstick. IEEE 830 §4.8: *"The SRS should address the software product, not the process of
  producing the software product"*, and it lists what does not belong: *"Delivery schedules; Reporting procedures; …
  Acceptance procedures"* [2]. Google's design-doc lifecycle has review "(may be in multiple rounds)" and then
  implementation, and the doc is updated when the design changes, not re-reviewed on a schedule the doc sets [4].
  Commoncog on PR/FAQs, already in this series: *"Don't let the process drive you"*. Spolsky: the spec is revised
  because revising prose is cheap, but it is the programmers who then start [10].
- **About:** the PRD (four passages) and the product (the four unmade changes).

### MF2. "Done" cannot be reached by the sequence the document prints (PRD)

- **Where:** §8.3, lines 487–492 (*"**Done** = §8.1 all hold on the merge commit **and** §9.1 is decided by Ben **and**
  three reviewers answer yes to questions 1–4 and to q.6's first line with no must-fix left open"*); header lines 4–5
  (fix round, PR, his yes); §9.0 (c), lines 588–593 (*"This is the one input the merge waits on, and his yes approves
  this document"*); §9.1's first sentence, line 602 (*"Only row 2b is decided now"*).
- **What I checked:** `docs/crit/round6/LOG.md` line 1104: round 16's three reviewers, *"None meets the goal yet"*.
  The round-16 fixes are `027f081`, the baseline this PRD describes. No product review round has judged that build:
  the last product entry in that log is round 16, and the fix round the header plans (items 7 and 8, §10.19, §10.23)
  changes the facts line, `chart.toml`, the fold and the publish step, after which no round is planned before the PR
  and his yes. So the third clause of Done has never been true of this product and the printed sequence gives it no
  chance to become true. The second clause, "§9.1 is decided by Ben", conflicts with §9.1's own first line and §9.0's
  last sentence: only 2b is decided now and 1a-against-1b "comes after a release and is not needed for the merge".
- **What to change:** Done becomes: *"**Done** = §8.1 all hold on the merge commit **and** §9.0 (c) is a yes **and**
  one product review round on that commit's build (three reviewers, §8.3 q.1–4 and q.6's first line, no must-fix
  left open)."* And the plan in `LOG.md` "Next round" (not the header, MF1) reads: fix round → build and gate (§8.1
  item 2) → product review round 17 on that build → PR → his yes. If the session would rather his merge be the only
  acceptance, say that instead and cut the three-yes clause; but his 20:50 put the three questions on reviewers
  (*"It should not be done until it goes over at least 10 reviews of, is it matching what I'm saying?"*), so I
  recommend keeping the clause and adding the round.
- **Why:** his 20:50 sentence above. The Scrum Guide's Definition of Done is *"a formal description of the state of the
  Increment"*, a state a reader can check, and an Increment that misses it *"cannot be released or even presented"*
  (cited in my round-5 review, source 8 there); Cagan's must-have bar, *"the product should not ship if even one of the
  'must-have' features is not ready"* [3]; IEEE 830 §4.3.4, consistency: no two requirements may conflict, and here
  Done's second clause conflicts with §9.0's last sentence [2].
- **About:** the PRD.

### MF3. The document grew 1,452 words in a round whose PM reviewer asked for 830 to go, and the growth is status, operations history and quoted evidence (PRD)

- **Where, with `wc -w` over the line ranges:** §0, lines 25–48 (402 words: the reading order, the baseline, the
  stop rule, "What waits on whom", all of which restate the header, lines 3–21); §8.5's first bullet, lines 515–531
  (the rule, who gets the email and what Ben does, is 90 words; the rest, *"State today: the job has run 12 times …
  run 12 … failed at `Unit tests` … REST, run `38140965684`"*, is operations history that `LOG.md` round 2 holds);
  §8.6, lines 543–577 (517 words for three orders of which one is recommended and blocks the merge; A and B are 250
  words of alternatives with their windows costed twice, here and in §11 lines 778–780); §9.2's first bullet, lines
  685–692 (150 words of quotations from TechInterview, CoderPad and Stack Overflow, which the PRD's own convention
  elsewhere, §4 and §9.1, gives as "sources in `docs/crit/prd/LOG.md`, round N"); §9.1's table, lines 617–624 (772
  words, of which row 0 and row 3 describe states nobody recommends).
- **What I checked:** `git show <sha>:docs/PRD.md | wc -l -w` over the six PRD commits: 530 / 8,287 → 691 / 12,505 →
  775 / 15,948 → 831 / 17,288 → 897 / 18,825 → 933 / 20,277. Two and a half times the words, no product change.
  Round 5's log says the growth is "reviewer 1's and reviewer 3's additions, each a requirement or a holder" (round 3's
  declined-in-part note says the same); the five passages above are none of those.
- **What to change:** §0 to two bullets: the reading order with its counts, and "Built / Reviewed" as pointers (about
  120 words); "What waits on whom" is the header's job and §9.0's. §8.5 bullet 1: keep the rule and what Ben does;
  the run-12 story becomes *"(state on 11 Oct 2026: `LOG.md` round 2)"*. §8.6: C in full; A and B one line each
  (*"A: publish then merge within the hour; reduced-motion readers see a broken image for that hour. B: merge and let
  the job publish; 852–1,199 px readers see a broken image for minutes. Neither unless Ben says so."*); §11's
  restatement (lines 778–780) becomes a pointer. §9.2 bullet 1: the three hiring sentences become *"(the 2026
  hiring-side evidence and its cost: `LOG.md`, round 5)"*. §9.1: row 0 to one line (it is a cost, not an option) and
  row 3 to one line. That is about 900 words out, no requirement lost.
- **Why:** Nygard: *"Large documents are never kept up to date"* and the whole record should be *"one or two pages"*
  [5]; Google: 10–20 pages for a large project, and if a doc grows well past that *"the problem may need to be split"*
  [4]; Lenny's favoured templates are one-pagers and the one long one is marked "a bit long" [7]; Eriksson: PRDs are
  *"as out of date as the time it took to write them"* [6]; IEEE 830 §4.3.7 on redundancy: *"a requirement may be
  altered in only one of the places where it appears. The SRS then becomes inconsistent"* [2]. His own 11 Oct 01:12
  asked for the rules and how they are implemented, which is §3, §5, §7 and §8; it did not ask for the run history.
- **About:** the PRD.

### MF4. One decision has seven homes, and the round-5 flip had to be written in all seven (PRD)

- **Where:** the agent-authorship line: G8, line 116 (*"Ruled on the owner lens: on by default"*); §5.3 row 5, line 206
  (*"§9.2 recommends keeping them; §8.1 item 7 blocks the merge on the switch"*); §7.3, line 348 (*"§9.2 recommends keep;
  switch §10.5"*); §8.1 item 7, lines 428–433 (*"defaults to `true` … unless Ben has said 'strike' or 'share'"*); §9.0
  (b), lines 585–587 (*"until he says one, keep is what §8.1 item 7 implements"*); §9.2 bullet 1, lines 674–695
  (*"Recommended: keep, as printed"*); §10.5, line 736 (*"decided on by default in §9.2, his word reverses it"*). The
  same for "a session acts only while Ben has one open": header lines 6–7, §8.5 line 520, §9.0 lines 594–596.
- **What I checked:** `LOG.md` round 5's applied table (r1 MF3) lists the places the flip from strike to keep had to
  be written: *"G8 ruled … §8.1 item 7's switch defaults to `true` … §9.0 (b) … §5.3 row 5, §7.3's totals row and
  §10.5 follow"*. Seven edits for one decision is the failure IEEE 830 describes, and it is the second time (rounds 1–2
  wrote strike into the same places). The PRD's own one-home rule (§4's "This is the one home of that rule", §9.1b's
  "This is the one home of the trade") is not applied to its largest open decision.
- **What to change:** §9.2 bullet 1 is the one home of the decision (options, recommendation, who, and what prints
  until he speaks). §8.1 item 7 is the one acceptance line, and reads only: *"7. `[facts] agent_clause` exists in
  `chart.toml`, a test holds both states, and its value on the merge commit is §9.2's standing answer. Owner: a
  session (§10.5). Fails today: no key (`chart.toml:667`), `render_readme.py:459` unconditional."* G8's cell, §5.3
  row 5, §7.3's row, §9.0 (b) and §10.5 point: *"(§9.2; §8.1 item 7)"*. The "acts only while Ben has one open"
  sentence lives in §9.0 only.
- **Why:** IEEE 830 §4.3.7, quoted above, and §4.3.4 on consistency [2]; Nygard's rule that a reversed decision is
  one record marked superseded, not a rewrite of every page that cites it [5]; Atlassian's template keeps each open
  question in one table with its answer and date [8].
- **About:** the PRD.

### MF5. §10 is a backlog without a rank, and 14 of its rows are owned by a party the PRD says does not exist until Ben acts (PRD)

- **Where:** §10, lines 721–755: 24 rows, 18 open, 14 with Owner "a session", 11 of those with Blocks "nothing"
  (rows 1, 11, 12, 15, 16, 18, 21, 22, 24 and the non-blocking halves of 7 and 9); the preamble, lines 723–728
  (*"Rows owned by 'a session' are held open by the PRD fix pass's scope"*); §9.0, lines 594–596 (*"a session acts only
  while Ben has one open … until he does, those rows do not move"*).
- **What I checked:** the Blocks column has three values (merge / 1a or 1b / nothing) and no row says when a
  "nothing" row would be done or why it matters more than another. A builder reading §10 cannot tell whether §10.22
  (a `workflow_dispatch` with `dry_run` false on a branch pushes that branch to `main` by the bot's hand, `profile.yml`
  line 174) is a hazard to fix this week or a note; it is, by its content, the most dangerous row in the table, and it
  sits between a docstring fix (18) and a contact warning (21) with the same "nothing".
- **What to change:** add one column, **Rank**, with three values and no more: *must before the merge* (5, 8, 19, 23:
  already §8.1 lines), *should before the next release of rustmapper* (7: a fresh clone's gate; 9: the release fails
  the build; 22: the bot can merge a branch), *nice* (the rest). Replace the Owner value "a session" with *"next
  session"* and delete the two sentences explaining what "a session" is (MF4 keeps one in §9.0). Closed rows (2, 3,
  6, 13, 14, 20) go to one line under the table: *"Closed: 2, 3, 6, 13, 14, 20 (reasons in `LOG.md`)"*, which keeps
  their ids citable.
- **Why:** Cagan, step 8: *"it is important to prioritize and rank-order every one of your requirements"* with a high
  bar for must-have [3]; IEEE 830 §4.3.5, *"ranked for importance and/or stability"* [2]; Shape Up: an appetite is set
  before the work, and what does not fit it is a no-go, not a row that waits [9]; Plane (cited in round 5): engineers
  stop reading at *"stale documents with unclear ownership"*.
- **About:** the PRD.

### MF6. Three of §9.2's decisions have a decider and no decide-by, no default and no place among his inputs (PRD)

- **Where:** §9.2 bullets 2–4, lines 696–704: the printed name (*"Decides: Ben; one line in `chart.toml`"*), the
  README's worker figure (*"Decides: Ben, in Rust-sitemap"*), Scrapy's politeness work (*"Nothing here changes either
  way. Decides: Ben, in Scrapy"*); §9.0, lines 583–597, which lists his inputs as (a)–(d) and names none of the three.
- **What I checked:** bullet 1 and §9.1b both say what stands until he decides and by when; bullets 2–4 say neither.
  Bullets 3 and 4 are work in other repositories that change nothing on this page by the PRD's own words, so they are
  not decisions about this product; they are `BEN-TODO.md` rows (appendix D: *"Asks that only he can do go in
  `docs/BEN-TODO.md`"*). Bullet 2 is a product decision (the first screen prints the name) with a recommendation and
  no default stated, though the default is what prints today.
- **What to change:** bullet 2 gains *"Until he says otherwise, `rustmapper` stands (it is what prints). Decide by:
  before a release that adds `[project.scripts]`, when the two names become one (§11)."* and §9.0 gains it as (e),
  "not needed for the merge". Bullets 3 and 4 move to `BEN-TODO.md` and §9.2 keeps one line: *"Work in his other
  repositories that would change a clause here (the worker figure; Scrapy's robots check, delay and name):
  `docs/BEN-TODO.md`"*. The fifth bullet (the overtaken round-4 ask) is already an instruction to strike and belongs in
  the same line.
- **Why:** the brief's own test for an open decision (options, costs, a recommendation, who decides, and, I add, by
  when and what stands meanwhile); Atlassian's questions table records *"the answer and the date it was answered"*
  [8]; IEEE 830 §4.8 puts work owed by other parties outside the SRS [2]; his 9 Oct 11:37 *"It has to be helpful
  knowledge"* is about what prints, and bullets 3–4 print nothing.
- **About:** the PRD.

### MF7. Loose ends (PRD)

- §8.3 q.3, line 471–472: *"no two adjacent rows differ in pitch (the density rule, by construction)"*. A line a
  reviewer ticks must be observable; "by construction" is not. Replace with *"ROUTE-LEFT-EDGE and ROUTE-HEAD-GAP
  pass, and the reviewer names any area that reads denser than another (G3); none is the pass."* Gherkin's rule for
  a Then step: *"only verify an outcome that is observable"* [11].
- §8.1 item 2, lines 412–417: the three commands are right, and the sentence after them (why the build comes first)
  is a §10.7 restatement; one pointer.
- Header line 9–12: *"the figures were read at `e17cc80`, and no product file has changed since"* is true, and the
  figures were last re-read in round 5 at `0a557ff` by its log; say the round-5 sha or drop the clause, since the
  header is the one place a reader checks the baseline.
- §8.5, line 539–540: *"No success metric is set; 'done' is §8.3"* stands from round 1's declined item, and I do not
  reopen it; one line that names where the referrer check would be recorded if he runs it (`LOG.md`) would close the
  loop.
- Appendix D's process table and G17–G19 are the right home for process; after MF1, "the PRD rounds stop at
  approval" in G19 is the only process sentence left outside it.

## 4. What holds, so nobody rewrites it

- Every cite I opened points where the PRD says: `column.py:47–50` (`TALL_FROM = 768`, `TALL_PX = 900.0`,
  `DESK_MIN_PX = 14.5`); `test_route.py:829` (`assertRegex(q, r"^Q[1-5]$")`); `alt.py:50` (`warn("ALT-POEM", …)`);
  `runcheck.py:8` ("probes four behaviours"); `render_readme.py:459` (`agents = agent_clause(r)`); `chart.toml:26,
  30–31` (`""`), `:35–39` (the five keys), `:1257` (L3's `fold = true`); `profile.yml:13` (`"20 6 * * 0"`), `:22–27`
  (push paths); `publish_chart.py:2–14` (one parentless commit, nothing kept); `README.md:38, 86` (the counts), `:151`
  ("on 10 Oct 2026"); `gate.txt` (0 fail, 4 warn, exit 2; the four of §8.2).
- The hand check reproduces: 539 tests OK; 28 plug-ins; 4,599 fails on the committed report; no product change since
  `027f081`.
- §5.1 matches the phone sheet element for element; §5.2's served-at rule matches the six `<source>` lines; §4's
  non-goals hold on both renders (no photo, badge, counter, card, activity graph, ship, legend).
- §5.4's table, §6.1, §8.6 order C, §9.1b and §9.0 (c) are things a stranger can do or answer in order. The glossary
  sentence in §1 works: I never wondered which object a sentence meant.
- The 19 "must" sentences each resolve to a holder: "both must work" to ROUTE-PHONE-PX / DESK-PX; "the committed
  README must equal" to README-STALE; "21 ways must match" to STRINGS-COUNT; "must have passed or failed" to
  ROUTE-UNVERIFIED; "must agree between trees" to T-ANCHOR; "must not be one the run check saw fail" to
  README-SUBCOMMAND; "must be able to run" to README-RENDER; "must name a tool…" to §8.3 q.1's logged line; "A session
  must not edit that line" is a process must and belongs in appendix D (MF1's spirit; not repeated as a must-fix).

## 5. Research notes my lens needed

- **Process in a requirements document.** IEEE 830-1998 §4.8 is the clearest statement I know: the SRS addresses
  the product, not the process of producing it; delivery schedules, reporting procedures, QA, V&V criteria and
  acceptance procedures go in a development plan or statement of work [2]. ISO 29148, its successor, keeps the
  split between requirements processes (clause 6) and the information items (clause 7) [15]. Google's design-doc
  lifecycle runs review in rounds and then implementation; the doc is maintained, not re-reviewed on a timetable it
  sets [4]. MF1 follows.
- **"Must" and testability.** RFC 2119 defines MUST as *"an absolute requirement of the specification"* and says
  imperatives *"must be used with care and sparingly"*, only where required or *"to limit behavior which has potential
  for causing harm"* [1]; the PRD's musts pass this (each is held). Gherkin: a Then step verifies *"an outcome that is
  observable for the user"* [11]; the acceptance-criteria guides agree ("can a tester write a test from this?") [16].
  §8.3 q.3's "by construction" line fails it (MF7).
- **When a document is done and how big it is.** Cagan: test completeness by whether an engineer and QA can work
  from it, then *"Resolve all questions about requirements by pointing people to the PRD"*, a living document through
  launch [3]; Nygard: one or two pages, status proposed → accepted → superseded, large documents never kept up to date
  [5]; Google: 10–20 pages, split when it grows past that [4]; Lenny: one-pagers, non-goals (Yien), success criteria
  (Morin) [7]; Atlassian: a top table with status and target release, a questions table with answers and dates, a
  "Not doing" list [8]; Shape Up: problem, appetite, solution, rabbit holes, no-gos [9]; Eriksson: PRDs go stale by
  the time they are written and are no substitute for talking [6]; Spolsky: a spec is cheap to revise and exists so
  the programmers can start [10]; Vogels on working backwards: write the launch documents first, the press release
  *"very clear and to the point"* [14]. MF2–MF6 follow.
- **Profile README conventions.** GitHub's page: a profile README is to *"tell other people about yourself"*, shown
  when the repository matches the username, is public and has a non-empty root `README.md`; the generated file is a
  template *"to give you some inspiration"* [12]. The curated list's sixteen categories (GitHub Actions, Game Mode,
  Dynamic Realtime, Badges, Icons, Fancy Fonts, …) and its tools section (stats cards, shields, visitor counters)
  are the conventions §4 rejects by name, correctly [13]. The page meets GitHub's four conditions on the branch.

## 6. Score

**6 / 10.** The product is what he asked for, by 9 Oct 11:37 and 20:50, and the renders prove it. The document can
still be built from and judged by, and its facts reproduce. It loses a point for carrying a review schedule it had no
authority over and could not keep (MF1); a point for a Done that its own next-step list cannot reach and that
conflicts with §9.0 (MF2); a point for growing a quarter again in a round that asked for cuts, with the growth being
status, history and quotation (MF3); and a point for the seven-home decision, the unranked backlog and the three
undecidable decisions, which are the same disease, requirements and plans mixed (MF4–MF6). Every fix above is a
deletion, a pointer, a column, or one sentence. The best next round is still not a PRD round; it is the fix round and
product review round 17, and this document should stop saying when either happens.

## Sources

Outside sources (read with WebFetch, or with curl and `pdftotext` where marked):

1. IETF, RFC 2119, *Key words for use in RFCs to Indicate Requirement Levels*,
   https://www.rfc-editor.org/rfc/rfc2119 — MUST means "an absolute requirement of the specification"; SHOULD
   admits "valid reasons in particular circumstances to ignore a particular item"; §6: imperatives "must be used with
   care and sparingly", only where "actually required for interoperation" or "to limit behavior which has potential
   for causing harm".
2. IEEE Std 830-1998, *Recommended Practice for Software Requirements Specifications*, the PDF at
   https://people.eecs.ku.edu/~hossein/Teaching/Stds/0830.pdf (curl + `pdftotext`) — §4.8 "Embedding project
   requirements in the SRS": "The SRS should address the software product, not the process of producing the software
   product"; the excluded items "Cost; Delivery schedules; Reporting procedures; Software development methods;
   Quality assurance; Validation and verification criteria; Acceptance procedures"; §4.3.5 "Ranked for importance
   and/or stability"; §4.3.7 "Not be redundant … a requirement may be altered in only one of the places where it
   appears. The SRS then becomes inconsistent"; §4.3.4 consistency and "standard terminology".
3. Martin Cagan, *How To Write a Good PRD* (SVPG, 2005), https://www.svpg.com/assets/Files/goodprd.pdf (curl +
   `pdftotext`) — step 8 "prioritize and rank-order every one of your requirements"; "the product should not ship if
   even one of the 'must-have' features is not ready"; step 9 "Can an engineer get enough understanding of the target
   … Can the QA team get enough information to design a test plan"; step 10 "Resolve all questions about requirements
   by pointing people to the PRD. If it's not in the PRD, put it in the PRD"; "the PRD is a living document, and you
   should track all features in the PRD through product launch".
4. Malte Ubl, *Design Docs at Google*, https://www.industrialempathy.com/posts/design-docs-at-google/ — the
   lifecycle "Creation and rapid iteration", "Review (may be in multiple rounds)", "Implementation and iteration",
   "Maintenance and learning"; "the sweet spot for a larger project seems to be around 10-20ish pages", past which
   "the problem may need to be split"; a "mini design doc" of 1–3 pages; not a requirements doc, not an
   "implementation manual".
5. Michael Nygard, *Documenting Architecture Decisions*,
   https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions — status "proposed", "accepted",
   "deprecated" or "superseded"; "The whole document should be one or two pages long"; "Large documents are never
   kept up to date"; "If a decision is reversed, we will keep the old one around, but mark it as superseded".
6. Martin Eriksson, *Product Requirement Documents Must Die* (Mind the Product),
   https://www.mindtheproduct.com/product-requirement-documents-must-die/ — PRDs are "as out of date as the time it
   took to write them"; "The person who reads them and has to act on them is generally not the person who wrote
   them"; "There is no replacement for high bandwidth communication"; talk, build, learn.
7. Lenny Rachitsky, *My favorite templates* (issue 37),
   https://www.lennysnewsletter.com/p/my-favorite-templates-issue-37 — nine PRD and one-pager templates; Kevin
   Yien's "Non-Goals"; Steve Morin's "success criteria and risks"; Adam Thomas's "keep these to one page, at least to
   start"; Product Hunt's "a bit long".
8. Atlassian, *Product requirements template* (Confluence),
   https://www.atlassian.com/software/confluence/templates/product-requirements — the top table (target release,
   status, core team); success metrics; assumptions; the requirements table with importance; a questions table
   with "their answers, and the date each was answered"; "Not doing": "list what's out of scope for this feature or
   release", "be as specific as possible".
9. Basecamp, *Shape Up*, chapter 6 "Write the Pitch", https://basecamp.com/shapeup/1.5-chapter-06 — the five
   ingredients: Problem, Appetite ("The amount of time we want to spend on a project, as opposed to an estimate"),
   Solution, Rabbit holes, No-gos ("Anything specifically excluded from the concept").
10. Joel Spolsky, *Painless Functional Specifications, Part 1: Why Bother?*,
    https://www.joelonsoftware.com/2000/10/02/painless-functional-specifications-part-1-why-bother/ — "The most
    important function of a spec is to design the program"; revising prose takes minutes, revising code weeks;
    "without a detailed spec, it's impossible to make a schedule"; a spec settles design debates so work can start.
11. Cucumber, *Gherkin Reference*, https://cucumber.io/docs/gherkin/reference/ — Given "the initial context", When
    "an event, or an action", Then "an expected outcome"; "a concrete example that illustrates a business rule";
    "only verify an outcome that is observable for the user (or external system)"; 3–5 steps.
12. GitHub Docs, *Managing your profile README*,
    https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
    — "to tell other people about yourself"; shown when the repository name matches the username, is public, has a
    root `README.md` with content; the generated file is "pre-populated with a template to give you some
    inspiration".
13. abhisheknaiidu, *awesome-github-profile-readme*, https://github.com/abhisheknaiidu/awesome-github-profile-readme
    — sixteen categories (GitHub Actions, Game Mode, Code Mode, Dynamic Realtime, A Little Bit of Everything,
    Descriptive, Simple but Innovative, Typing Mode, Anime, Minimalistic, GIFS, Just Images, Badges, Fancy Fonts,
    Icons, Retro); tools: GitHub Readme Stats, GitHub Stats, GitCard Studio, Shields, Markdown Badges, Visitor Badge,
    visitor counters.
14. Werner Vogels, *Working Backwards* (All Things Distributed, 2006),
    https://www.allthingsdistributed.com/2006/11/working_backwards.html — "we start by writing the documents we'll
    need at launch (the press release and the faq)"; the order press release, FAQ, customer experience, user manual;
    the press release "needs to be very clear and to the point".
15. WebSearch, ISO/IEC/IEEE 29148: arXiv 2408.10886 (https://arxiv.org/pdf/2408.10886) for the nine
    individual-requirement characteristics (singular, unambiguous, verifiable among them); the Modern Requirements
    page (https://www.modernrequirements.com/?p=32595) for the three pillars, requirements processes (clause 6)
    apart from information items (clause 7); the 2011 preview (https://webstore.ansi.org/preview-pages/ISO/preview_ISO+IEC+IEEE+29148-2011.pdf)
    for the table of contents (search-level; the standard's text is not free).
16. WebSearch, acceptance criteria and the Definition of Done: Visual Paradigm
    (https://skills.visual-paradigm.com/?p=1099), Parallel HQ (https://www.parallelhq.com/blog/what-acceptance-criteria),
    Docsio (https://docsio.co/blog/acceptance-criteria) — "Can a tester write a test from this?"; replace "The system
    should work" with an observable, timed outcome; Given–When–Then; more than five criteria means the story is too
    broad (vendor guides; search-level).

Files in this repository (all under `/home/user/wt-v12/`) and the renders:

17. `docs/PRD.md` at `b6cca2c` (933 lines, 20,277 words by `wc -l -w`; the reading-order subset by `wc` over lines
    52–73, 74–93, 127–147, 148–245, 404–578, 579–720, 757–792: 9,335 words; `wc -w` over lines 25–48: 402, 515–531
    and 515–541: 419, 543–577: 517, 685–692: 150, 617–624: 772; `grep -n -i '\bmust\b'`: 19 lines; `grep -c "a
    session"`: 41; `grep -n "| a session |"`: 14 rows); `git show {9e3db34,e17cc80,107a988,92b1bef,0a557ff,b6cca2c}:docs/PRD.md
    | wc -l -w` (530/8,287; 691/12,505; 775/15,948; 831/17,288; 897/18,825; 933/20,277).
18. `docs/crit/prd/owner-messages.md` (21 messages; the 11 Oct (later) sentence); `docs/crit/prd/LOG.md` rounds 1–5
    (applied, declined, the hand-check commands); `docs/crit/prd/review-r05-2.md` (mine), the must-fix headings of
    `review-r05-1.md` and `review-r05-3.md`; `docs/crit/round6/LOG.md` lines 1101–1175 (round 16: "None meets the
    goal yet"; the fixes applied; no later round).
19. `git log --oneline -15` (HEAD `b6cca2c`, six PRD commits over `027f081`); `git diff --stat 027f081..HEAD -- .
    ':!docs'` (empty); `git status --short` (clean); `git branch --show-current` (`v12/purpose`).
20. `chart.toml` 20–40 (`[position] text = ""`, `[contact]` both `""`, the five `[copy]` keys at 35–39, no `[facts]
    agent_clause`), 1250–1260 (L3 `fold = true`); `grep -n "fold = true" chart.toml` (1257, 1276, 1308, 1357);
    `grep -n agent_clause chart.toml scripts/render_readme.py` (only `render_readme.py:459, 925, 1027, 1040`).
21. `scripts/render_readme.py` 455–462; `scripts/checks/column.py` 45–50; `scripts/checks/alt.py` 48–52;
    `scripts/runcheck.py` 1–12; `scripts/publish_chart.py` 1–16 (`grep -n keep-current`: none); `tests/test_route.py`
    827–831; `.github/workflows/profile.yml` 10–30.
22. `python3 -m unittest` (Ran 539 tests, OK); `ls scripts/checks/*.py | grep -v __init__ | wc -l` (28); `python3
    scripts/check.py --tier fast` on the committed tree (`FAIL (exit 1) · 4599 fail · 8 warn · 0 error`);
    `docs/crit/prd/renders/round-16/gate.txt` (0 fail, 4 warn, exit 2: `log.shards`, POSITION-EMPTY,
    LICENSE-FLAGSHIP, ROUTE-WAITING S2); `README.md` 36–40, 84–88, 149–152.
23. Renders, `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/`:
    `sheet-phone-day-390.png` (T1, T2, R0, the start bar, R2 with "0.1.3 · 8 NOV 2025", the track, the loop bracket,
    S1, F1, the dotted box with H0 and H1, C1, the end bar, R13 with its fields, R15), `sheet-desk-night-870.png`
    (the redraw: heavier strokes, pink track on navy, the same gap under the box), `page-desk-1.png` (link line,
    "Ben Russell builds", Languages, Stack, the pick, the facts line with "authored 45 of its 146 commits and
    co-signed 1 of his own 101", the platform note, six cautions with a lever each, the fold, the code block with
    its three wrapped comment lines), `page-phone-2.png` (the pick, the facts line, the platform note, "Before you
    run 0.1.3:" and the first three items at 390 px).
