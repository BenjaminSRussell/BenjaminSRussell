# PRD review round 5, reviewer 2: A product manager who has shipped from PRDs and rejects the vague ones

11 Oct 2026. Branch `v12/purpose`, worktree `/home/user/wt-v12`, HEAD `0a557ff` (the round-4 fix commit). I read
`docs/PRD.md` end to end (897 lines and 18,825 words by `wc`; the header says 895 and 18,901 by its own loop), every
message in `docs/crit/prd/owner-messages.md`, `docs/crit/prd/LOG.md` rounds 1–4 (nothing below repeats a fix those
rounds applied; where I touch a declined item I say so), my own round-3 and round-4 reviews and the must-fix headings
of `review-r04-1.md` and `review-r04-3.md`, `README.md` on the branch, `.github/workflows/profile.yml` (the `if:`
lines and the failed-fetch step, 189–191), `scripts/render_readme.py` 459 and 1003–1017, `scripts/checks/position.py`
28–36, `chart.toml` 665–669, `scripts/runcheck.py` 8, `scripts/checks/data.py` 69, `docs/BEN-TODO.md` 30–42,
`docs/crit/prd/renders/round-16/gate.txt`, and the round-16 renders `sheet-phone-day-390.png`, `page-phone-1.png`
and `page-desk-1.png`. I ran the round-4 hand check from `LOG.md` (every command but the build, which dirties a
tracked file this review may not touch): 28 plug-ins, 169 code-shaped strings, `FIGURES` at `figures.py:93–104` and
`TYPE` at `type.py:35`, 25 run-check steps of which 7 gate, 17 `PURPOSE` keys, `runcheck.py:8` and `data.py:69` as
cited, `git diff --stat 027f081..HEAD -- . ':!docs'` empty, 24 files in `tests/` and no `test_prd.py`. All agree
with the PRD. Outside: 16 sources (Sources, at the end).

My brief is the document as a PRD: could a builder who was not in the room build and accept this product from it
alone, is every requirement testable and every must tied to a criterion, are the non-goals explicit, are the open
decisions decidable, is anything said twice, is it longer than it needs to be or missing a section, and does it
mistake its own history for requirements.

## 1. Is the product this PRD defines what he wants?

**Yes.** The sentence that decides it is 9 Oct 11:37: *"It has to be helpful knowledge. If you were a fucking real
sailor, if you were a real person, you'd want it to be helpful data that you're looking at. You're going through,
you're like, oh, it's very helpful, and it's in a cool format."* What §1 and §5.1 define, and what the round-16 phone
sheet shows element for element (T1, T2, R0, R2, S1, F1, H0, H1, C1, R13, R15; `sheet-phone-day-390.png`), is the
helpful part of that sentence: the install line with the release's date, the command, what each page meets, the two
catches, the one key to press, the file and who reads it next. Nothing on it is a count or a decoration. His test of
20:50, *"Everything, single thing inside of this needs a purpose, not a fucking chasing a reason"*, is §5.1's table,
a Q beside every row.

The judged lines §8.3 asks of every reviewer, answered here so the log has them:

- **q.1, first line (G3a).** My one sentence, written from the phone sheet: *"How to install a crawler called
  rustmapper, what it does with each page, where it stalls, the one key that stops it, and the file it leaves."* It
  names a tool, an install, and an output. One honesty note: the brief hands a reviewer the PRD before the renders,
  so I had read §1 before I looked; the line as written cannot be answered uncontaminated by anyone who reviews the
  PRD, only by a product reviewer who is given the image first. §8.3 should say which reviewer answers it.
- **q.6, first line.** Yes, I would screenshot it and send it, to show someone that install notes can be drawn as
  one route down a page. Second line: I would call it "a crawler's run, drawn top to bottom". Third line (G1d): the
  care is visible in the gap the track leaves under the dotted box and in the release date set small and grey beside
  the install line; both are things a template cannot produce.

**His last message deserves the same straight answer it got in round 4.** *"Review and ensure this is something I
want to see rounds of reviews and research"* (11 Oct, later). The product: yes, by the sentences above. The rounds:
five PRD rounds have now changed no product file (`git diff --stat 027f081..HEAD -- . ':!docs'` is empty at
`0a557ff`; the PRD says so at line 8), while the PRD's own merge blockers, §8.1 items 7 and 8 and §10.19, are three
code changes a session could make in an afternoon and have been "open; blocks the merge" since rounds 1 and 2. Round
4's largest finding was two line numbers off by one. A document whose reviews now find drift and not requirements is
a document that is finished enough to build from. MF1 is about that.

## 2. Verdict on the document

**7 / 10 as a PRD**, up from my 6 in round 4. Everything I asked for in round 4 was applied or declined with a
reason I accept: the first merge has a sequence (§8.1 item 9), the renders are in the repository, "default" means
one thing, "a session" is defined, §6.1's rollback is a PR, the C1 fact has two homes, §4 names the conventions it
rejects, §8.2 states the merge-commit warning set. §5.1 and §5.4 remain the best-written requirements in this series:
"drawn only when" conditions in EARS's shape, each tied to an anchor and a probe. The 22 sentences with "must" in
them all resolve to a gate, a test or a judged line in §8.3 (I grepped them; the one-sentence rule of §1 is held by
q.1, "both must work" by the ROUTE-PHONE-PX / DESK-PX pair, "21 ways must match" by STRINGS-COUNT). The non-goals
are explicit and the renders break none. The open decisions in §9 have options, costs, a recommendation and a name.

What keeps it from higher: the document has no way to stop being a draft, and the people it names as owners of the
blockers are the people writing it (MF1); it asks the owner for one technical choice it has already made (MF2);
§8.1's heading promises "must all hold" over an item that says "not a merge blocker" and a procedure (MF3); two
decisions sit in the gaps table with no options or recommendation (MF4); about 830 words of verification notes,
fixture descriptions and audit history sit inside the requirements, one of them in breach of the document's own
round-3 rule (MF5); and the one object the whole document is about has five names (MF6). None of these needs a new
section. Three of them are deletions.

## 3. Must-fixes, ranked

### MF1. The PRD has no exit from "draft", and its merge blockers are owned by the people editing it (PRD; and the product it keeps from shipping)

- **Where:** header, lines 3–6 (*"Status: draft. Waits on four inputs from Ben … and three session items"*); §0
  bullet 4 (lines 41–44); §8.1 items 7 and 8 (lines 427–435); §10 rows 5, 8, 19 (lines 705, 708, 719, each "open;
  blocks the merge"); §9.0's last sentence (lines 562–565: *"a session acts only while Ben has one open"*);
  appendix D G19 (line 883: *"the PRD itself is reviewed the same way"*).
- **What I checked:** the three blockers are, by the PRD's own fix cells, a `[facts] agent_clause` switch read at
  `render_readme.py:459` (one `if`, one key, one test), the deletion of five `chart.toml` keys and five retired
  modules with their tests, and two `fold = true` lines. Each round's fix pass declined them with the same sentence
  ("Product changes; this pass edits only the PRD", `LOG.md` rounds 1, 2, 3, 4). The session that could make them
  is open: his 11 Oct message was typed in it, and the PRD's own definition of an acting owner ("while Ben has one
  open") is met. So the thing that holds the blockers open is the fix pass's scope rule, not Ben and not a missing
  owner, and the PRD never says so. Nor does it say what moves its status from "draft" to anything else: the header
  names four inputs, but (a), (b) and (d) are "not needed for the merge", and a yes to (c) is nowhere stated to be
  the approval of the document.
- **What to change:** the header's Status line becomes: *"**Status:** draft. **Approved when** Ben answers §9.0 (c);
  from then on the text changes only when the product changes (§0). **Next step, in order:** a fix round on §8.1
  items 7 and 8 and §10.19 (three code changes; a session, now open), then the PR (§10.17), then his yes. PRD review
  rounds stop at approval."* And one sentence in §10's preamble: *"Rows owned by 'a session' are blocked by the fix
  pass's scope (PRD and log only), not by Ben; a product fix round clears them."* If the workflow cannot run a
  product fix round, the PRD should say that instead, so the reader stops expecting one.
- **Why:** his 9 Oct 20:50 *"It should not be done until it goes over at least 10 reviews"* set a floor, and the
  product has had 16 rounds; his 11 Oct (later) asks whether this is what he wants rounds of reviews on, and a
  review that finds two off-by-one line numbers is no longer earning its round. Nygard: a decision record's status
  moves from "proposed" to "accepted", and *"Large documents are never kept up to date"* [10]; Google's design-doc
  lifecycle has a review phase that ends and an implementation phase in which the doc is updated, not re-reviewed
  [4]; Cagan: *"the PRD is a living document, and you should track all features in the PRD through product launch"*,
  which presumes a launch [1]; Spolsky: open issues must be *"stomped out"* *"by the time the programmers start
  work"*, and here the programmers are the blocker [14]; Commoncog on PR/FAQs: *"Don't let the process drive you"*
  [13]; Plane names *"stale documents with unclear ownership"* as a reason engineers stop reading [12].
- **About:** the PRD (the status line and the owner sentence) and the product (the three changes it has described
  since round 1 and never made).

### MF2. §9.0 (c) asks him for a technical choice the PRD already made (PRD)

- **Where:** §9.0 (c), lines 559–561 (*"Yes or no to merging 2b … and A or B for the order of the first merge (§8.1
  item 9). This is the one input the merge waits on"*); §8.1 item 9, lines 436–449 (*"(A) Publish, then merge within
  the hour (recommended)"*; *"decided with §9.0 (c)"*).
- **What I checked:** item 9 costs both orders and recommends A; the difference between them is which of two
  windows the live page shows (an hour of the new hero under old text, or minutes of new text over the old hero
  with the mid sources broken), a fact about `publish_chart.py` and `profile.yml:142–153`, not about what the page
  says. Round 4's reviewer 1 objected to the PRD asking him for paperwork (the device check, conflict 1 in `LOG.md`
  round 4), and the fix pass agreed. (c) still asks him to read 714 words of §8.1 item 9 and 1,709 of §9.1 to return
  two tokens, one of which is a choice between two publish timings.
- **What to change:** §9.0 (c): *"(c) One word, yes or no, to merging 2b (§9.1; the render is
  `renders/once-2b/page-phone-2.png` and `-3.png`). A yes means: a session sets the two `fold = true` lines (§10.19),
  publishes the six sheets (§8.1 item 9, order A), opens the PR, and he merges within the hour. B only if he says
  so."* §8.1 item 9 keeps both orders and loses "decided with §9.0 (c)"; A is what happens.
- **Why:** his 8 Oct 09:04, *"all PRs need to be ready to merge"*: ready means he merges, not that he sequences the
  merge; Shape Up's pitch asks stakeholders to judge *"whether the bet is worth making"*, not how it is deployed
  [5]; Atlassian's open-questions table records *"the answer and the date it was answered"* by whoever can answer,
  and a publish order is a session's answer [2]; Plane: name *"who owns answering"* each open item [12].
- **About:** the PRD.

### MF3. §8.1 says "must all hold on the commit that merges" and contains an item that says it need not, and a procedure (PRD)

- **Where:** §8.1 heading, line 400; item 6, lines 420–426 (*"Not a merge blocker"*); item 9, lines 436–449 (a
  two-order procedure); items 1–5, lines 404–419 (no owner named; items 6–9 each name one).
- **What I checked:** the position line now has five homes: §8.1 item 6, §8.2's POSITION-EMPTY row (line 458),
  §9.0 (a) (lines 555–557), §9.2's first bullet (line 654) and §10.21 (line 721); four of them say "not a merge
  blocker" in four wordings. Item 4 (the dry run) says what must not be done on a branch but not who runs the dry
  run or who reads its result. Item 9 is a procedure with a recommendation, which is §9's shape, inside the list
  whose heading says every line holds on the merge commit.
- **What to change:** item 6 becomes one line: *"6. `[position] text` and a contact: §9.0 (a); not a merge
  blocker."* and §9.0 (a) keeps the full text (it is the owner's section). §9.2's first bullet goes (it is a
  pointer to a pointer). Item 9 moves out of 8.1 to a new heading **§8.6 The first merge** with its text unchanged,
  and item 5 points there as it does now. Items 1–5 gain *"Owner: a session"* once, in the sentence above the list
  (*"Items 1–5 are run by a session on the branch; 6–8 name their owner"*).
- **Why:** ISO 29148's set characteristic that requirements are consistent and *"none of the requirements
  contradict each other"* [15]; Cagan's bar for must-have, *"the product should not ship if even one of the
  'must-have' features is not ready"*, which a list cannot carry if one of its items opts out [1]; the Scrum Guide's
  Definition of Done is *"a formal description of the state of the Increment"*, a state, not a procedure [8]; the
  PRD's own one-home rule (§4, §9.1b).
- **About:** the PRD.

### MF4. Two decisions sit in the gaps table with no options, no cost and no recommendation (PRD; one closes)

- **Where:** §10.13, line 713 (*"decide whether a mark exists on the route sheet or the page … Ben (whether)"*);
  §10.20, line 720 (*"only if Ben wants the window shorter … Ben (whether)"*); the table's preamble, line 694
  (*"Rules held only by a reviewer's eye, or by nothing, with the proposed fix"*).
- **What I checked:** the failed-fetch path is real: `profile.yml:189–191` runs `build_assets.py --no-sounding
  --heartbeat` when `steps.stats.outcome == 'failure'`, and `no_sounding` is read by `build_assets.py` (sets
  `data["no_sounding"]`, line 433) and by nothing under `scripts/sheets/route.py`, as §6 says. But the page already
  carries a mark of the stale survey: the provenance line prints the run check's date from `stats.json`
  (`render_readme.py:1017`, *"its commands were run … on"* + `runcheck.rustmapper.date`, which is `2026-10-10` in
  the committed file), and a rebuild from last week's `stats.json` prints last week's date. §6 itself says the page
  comes back *"with their old dates"*. So the question §10.13 leaves to Ben has an answer the PRD can give: the
  date is the mark; a second mark would say the same thing twice (G6). §10.20's answer is also already written: §11
  accepts the lag and costs the run-named-sheet alternative.
- **What to change:** §10.13 → *"closed: the provenance line's date (`render_readme.py:1017`, from
  `runcheck.rustmapper.date`) is the mark; a rebuild from an older `stats.json` prints the older date; no second
  mark (G6)"*, with §6.1 row 1's "nothing to undo" cell saying *"the provenance date shows the week"*. §10.20 →
  either *"closed: accepted in §11; reopen if Ben asks for a shorter window"* or a §9 row with the two options and
  "accept" recommended. Either way the gaps table holds gaps, and decisions live in §9.
- **Why:** the brief's own test (options, costs, a recommendation, who decides); Atlassian's template keeps open
  questions in one table with a recorded answer [2]; Nygard: a decision carries a status, and one that is reversed
  or settled is marked so, never left as a question [10]; Google: a design doc that lists alternatives without
  trade-offs *"reads like an implementation manual"* [4]; his 9 Oct 11:35, *"how is the data gathered? The data
  doesn't look exactly accurate"*, is answered by a date on the page, which is what the line already does.
- **About:** the PRD; no page change.

### MF5. Verification notes, fixture descriptions and audit history sit inside the requirements (PRD)

- **Where:** §5.4's "Needs here" column, lines 223–229: eight *"verified: …"* clauses (65 words in parentheses)
  recording how the cell was checked, not what the product needs; §9.1's two render bullets, lines 611–635 (393
  words) describing fixtures (`ends_by_itself` and `robots_read` passing…), gate artefacts (*"one fail,
  REPORT-STATS, which hashes `assets/stats.json` rather than the fixture"*) and where the other seven screens live
  in a scratchpad; §7's preamble, lines 283–292 (164 words) on the grep that counts codes, its three false
  positives and two misses; §0 bullet 1, lines 25–34 (209 words) on how the register was hand-checked, ending
  *"(round 4: 56 cites printed, two off by one, fixed)"*.
- **What I checked:** each of the four is already in `LOG.md` (round 1 for the resolver runs, rounds 2–4 for the
  fixtures and renders, rounds 3–4 for the grep, round 4 for the 56 cites). The "round 4" clause in §0 is the kind
  the round-3 fix pass removed everywhere else under my MF1 of that round (*"Every 'PRD round N' … clause outside
  the header removed"*, `LOG.md` round 3), and it was added back in round 4. Together the four passages are about
  830 words, four and a half per cent of the document, and none states a requirement, a holder or a decision.
- **What to change:** §5.4: drop the eight "verified" parentheticals and keep the intro's sentence that every cell
  was checked by a resolver run and the clone (lines 216–219 already say so). §9.1's render bullets become two
  lines each: the path, what the first phone screen shows that differs from round-16, and "fixture and gate notes:
  `LOG.md` rounds 2 and 4". §7's preamble: *"168 live codes from 28 plug-ins, counted by the grep in `LOG.md` round
  4; the number is a grep, not a register (§10.12)."* §0 bullet 1: delete from *"The register's own claims"* to the
  bullet's end and keep *"Line numbers are as of `027f081`; the register is hand-checked each round until §10.12
  exists."* No requirement is lost.
- **Why:** Nygard: *"Large documents are never kept up to date"* and are *"too large to open, read, or update"*
  [10]; Mind the Product: PRDs are *"almost always out of date"* by the time they are written, and the cure is
  fewer words that go stale [11]; Google: a doc that becomes an implementation manual should not have been written
  as a doc [4]; the brief's test, "does it mistake the process history for requirements", which these passages
  fail; the document's own rule from round 3.
- **About:** the PRD.

### MF6. The object the document is about has five names (PRD)

- **Where:** throughout. Counted by grep: "the image" 46 times, "edition" 30, "the sheet" 12, "the track" 9, "the
  route" 7, "the picture" 3, "hero" in every id and gate name (`hero-ID`, HERO-COLUMN-PX, HERO-FALLBACK) and in the
  README comment; "drawing" is what the page itself calls it in the provenance line (*"The drawing shows rustmapper
  0.1.3"*) and in the `DESIGN.md` link. §1 defines "the track" (R5) and nothing else. "Sheet" is used for the
  drawing (*"the phone sheet"*, §5.2) and for the paper (*"a cream sheet"*, §1; *"Sheet height ≤ 770"*, §7.4).
- **What I checked:** a reader who has not seen the code cannot tell from §5.2's table ("Edition | Sheet | Served
  at") whether an edition is a sheet, or from §8.3 q.3 ("the image is one screen") whether that is the phone
  edition or all six. The code's own names (`hero`, `route`, `edition`, `sheet`) are each right in their place; the
  PRD never says which word it uses for which thing.
- **What to change:** one sentence at the end of §1's first paragraph: *"Words: **the image** is what the page
  shows at the top, in any of its six **editions** (one SVG each, named `hero-*` in the code and the gates); a
  **sheet** is one edition's drawn area, measured in units; **the route** is the drawn order of a run, and **the
  track** its magenta line (R5). The page calls the image 'the drawing'."* Then use those words; §5.2's header
  becomes "Edition | Sheet, units | Served at | Column | Smallest text".
- **Why:** ISO 29148 asks that *"the terminologies are consistent"* across a set [15]; EARS works because it fixes
  a small vocabulary, and the PRD adopted its clause shape in §5.1 without its vocabulary [7]; Cagan's step 9, *"Can
  an engineer get enough understanding of the target"* [1]; his 8 Oct 14:52 "label everything" was about the page,
  and a glossary is the one place labels belong.
- **About:** the PRD.

### MF7. Loose ends (PRD)

- §8.5's first bullet tells the reader where a failure email goes and that the fix is *"nobody's until he opens
  one"*; it does not say what Ben does with the email. One line: *"Ben: open a session and paste the run's link;
  the session fixes it and opens a PR."* That is the whole maintenance runbook and the PRD is the only place it can
  live (Plane: assign one owner and keep the doc the central reference [12]).
- §6's fourth bullet, "Review: three independent reviewers per round…", is how the work is done, and appendix D is
  the one home the round-3 fix pass gave the process rows. Move it.
- §8.3 q.1's first line should say who answers it (a product reviewer given the image first; see §1 above), or it
  will be answered by people who have read §1, as I did.
- The header's line and word counts (895, 18,901) differ from `wc` (897, 18,825). One method, named, or no number:
  a figure that disagrees with the first tool a reader reaches for costs trust for nothing.
- §9.1's table is 1,709 words, and §9.0 says the only row the merge needs is 2b. Put the sentence *"Only row 2b is
  decided now; rows 1a and 1b are what a release does later"* above the table, so the reader who came for (c) does
  not read the 1b column first.

## 4. What holds, so nobody rewrites it

- Every cite I opened points where the PRD says: `render_readme.py:459` `agent_clause(r)`; `position.py:31`
  POSITION-EMPTY on empty text, 32–35 placeholders only; `chart.toml:665–669` `[facts]` with no switch;
  `runcheck.py:8` "four behaviours"; `data.py:69` `data.calendar` info; `profile.yml:143, 147, 154` (`dry_run`
  guards) and 189–191 (the failed-fetch rebuild).
- The round-4 hand check reproduces: 28 plug-ins, 169 strings, `FIGURES` and `TYPE` where stated, 25 steps / 7
  gates, 17 `PURPOSE` keys, no product change since `027f081`, no `test_prd.py`; `gate.txt`: 0 fail, 4 warn, exit 2,
  and the four warnings are §8.2's four.
- §5.1 matches the phone sheet element for element; the desk page shows the agent-authorship counts on the facts
  line, as §8.1 item 7 says it does today; the page has no photo, bio paragraph, badge, counter or card (§4).
- §8.1 item 9 and §6.1 are now things a stranger can do in order; §9.1b is a decision done properly; §4's non-goals
  are real non-goals with the convention each rejects named.
- §5.4's table is the right shape for a product that is a function of another repository's state, and it should
  stay; only its verification notes should go (MF5).

## 5. Research notes my lens needed

- **When a PRD is done.** Cagan tests completeness by whether an engineer and the QA team can work from it (step
  9) and then manages by it: *"If it's not in the PRD, put it in the PRD"*, *"a living document … through product
  launch"* [1]. Nygard's records have a status that moves to "accepted" and are one or two pages because *"Large
  documents are never kept up to date"* [10]. Google's lifecycle is creation, review, implementation, maintenance
  [4]. Commoncog on Amazon: most PR/FAQs are killed, the team *"must decide if they will keep working on the
  product"*, and *"Don't let the process drive you"* [13]. Spolsky: open issues are *"stomped out"* before the
  programmers start, and the spec has *"one person"* as owner [14]. This PRD has the review phase and no exit from
  it (MF1).
- **Who answers what.** Atlassian's open-questions table records the answer and its date; its top table names the
  core team [2]. Plane: name who owns answering each TBD; stale documents with unclear ownership are why engineers
  stop reading [12]. Shape Up: the pitch is for judging the bet, and over-specifying *"boxes in"* the people who do
  the work [5]. MF2 and MF4 follow.
- **Length and what goes stale.** Amazon: a one-page press release, a FAQ *"five pages or less"* by the book, about
  six pages in all [16]; Google: 10–20 pages for a large project, 1–3 for incremental work [4]; Lenny's favourite
  templates are one-pagers, *"keep these to one page, at least to start"* [3]; Plane: 3–6 pages, *"no longer a
  20-page blueprint"* [12]; Mind the Product: PRDs go stale by the time they are written [11]. This PRD is about 60
  pages. I do not ask for the register to go (he asked for it, 11 Oct 01:12); I ask for the 830 words that are
  neither rule nor holder (MF5).
- **Testability and consistency.** ISO 29148's nine characteristics of a requirement (unambiguous, verifiable,
  singular, …) and the set's completeness and consistency, including consistent terminology [15]; EARS's fixed
  keywords (While, When, Where, If/Then) are what §5.1's "drawn only when" column already is [7]; the Scrum Guide's
  Definition of Done is a state, and an Increment that misses it *"cannot be released or even presented"* [8]. MF3
  and MF6 follow.
- **Profile README conventions.** GitHub's own page says a profile README is a way to *"tell other people about
  yourself"* and gives a template *"to give you some inspiration"*; the repository must match the username, be
  public, and hold a non-empty root `README.md` [6]. ProductPlan's definition of a PRD, *"the document of record that
  the entire release is based on"*, with every capability tied to a use case, is what §5.3's Q column does [9]. The
  page meets GitHub's four conditions on the branch and rejects the template's bio-and-badges shape by §4's choice.

## 6. Score

**7 / 10.** The product is what he asked for, by 9 Oct 11:37 and 20:50. The document can be built from and judged
by, its facts reproduce from the commands it names, and round 4's gaps are closed. It loses a point for having no
exit from draft while its own blockers wait on the people editing it (MF1); a point for the contradictions and the
technical ask a reader trips on (MF2, MF3); and a point for the history and the five-named object that make it
longer and less precise than its requirements (MF4, MF5, MF6). Every fix above is a status line, a moved item, a
closed row, a deletion or one glossary sentence. The best next round is not a PRD round.

## Sources

Outside sources (read with WebFetch unless marked otherwise):

1. Martin Cagan, *How To Write a Good PRD* (SVPG, 2005), https://www.svpg.com/assets/Files/goodprd.pdf — fetched
   with curl and read with `pdftotext` (the WebFetch of the same URL returned the SVPG home page): "The release
   criteria are often just hand-waved, but a good PRD puts considerable thought into what the true minimum
   requirements are"; "The product manager should have an extremely high bar for anything flagged as 'must-have'.
   This literally means that the product should not ship if even one of the 'must-have' features is not ready";
   Step 9 "Can an engineer get enough understanding of the target … Can the QA team get enough information to design
   a test plan"; Step 10 "If it's not in the PRD, put it in the PRD … record these decisions in the PRD"; "the PRD is
   a living document, and you should track all features in the PRD through product launch".
2. Atlassian, *Product requirements template* (Confluence),
   https://www.atlassian.com/software/confluence/templates/product-requirements — the top table (target release,
   status, core team: "Set the scene by using the top table"); success metrics; an options table per requirement;
   an open-questions table with "the answer and the date it was answered"; "list what's out of scope for this
   feature or release … Be as specific as possible". (The guide at
   https://www.atlassian.com/agile/product-management/requirements was fetched and came back truncated to its
   navigation; not relied on.)
3. Lenny Rachitsky, *My favorite templates* (issue 37),
   https://www.lennysnewsletter.com/p/my-favorite-templates-issue-37 — nine PRD and one-pager templates; Kevin
   Yien's (Square) praised for its "Non-Goals" section; Steve Morin's for "the focus on success criteria and risks";
   Adam Thomas's "keep these to one page, at least to start"; Product Hunt's "a bit long".
4. Malte Ubl, *Design Docs at Google*, https://www.industrialempathy.com/posts/design-docs-at-google/ — "the sweet
   spot for a larger project seems to be around 10–20ish pages"; "1–3 page 'mini design doc'" for incremental work;
   the lifecycle (creation and rapid iteration, review, implementation and iteration, maintenance and learning);
   "If the designed system hasn't shipped yet, then definitely update the doc"; docs "tend to get out of sync with
   reality over time"; non-goals are "things that could reasonably be goals, but are explicitly chosen not to be
   goals"; a doc that reads like an "implementation manual" with no trade-offs was not worth writing.
5. Basecamp, *Shape Up*, chapter 6 "Write the Pitch", https://basecamp.com/shapeup/1.5-chapter-06 — the five
   ingredients (Problem, Appetite, Solution, Rabbit holes, No-gos); stakeholders judge "whether the bet is worth
   making"; "No-gos … functionality or use cases we intentionally aren't covering"; wireframes and high-fidelity
   mocks "box in the designers who do the work later".
6. GitHub Docs, *Managing your profile README*,
   https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
   — a way to "tell other people about yourself"; the generated file is "pre-populated with a template to give you
   some inspiration"; the repository must match the username, be public, and have a root `README.md` with content.
7. Alistair Mavin, *EARS: Easy Approach to Requirements Syntax*, https://alistairmavin.com/ears/ — ubiquitous,
   state-driven (While), event-driven (When), optional (Where), unwanted behaviour (If/Then), complex; natural
   language is "inherently imprecise" and EARS "reduces or even eliminates common problems found in natural
   language requirements".
8. Scrum.org, *The Scrum Guide*, https://scrumguides.org/scrum-guide.html — the Definition of Done is "a formal
   description of the state of the Increment"; an item that does not meet it "cannot be released or even presented
   at the Sprint Review"; the Sprint Review's purpose is "to inspect the outcome of the Sprint and determine future
   adaptations".
9. ProductPlan, *Product Requirements Document* (glossary),
   https://www.productplan.com/glossary/product-requirements-document/ — "the document of record that the entire
   release is based on"; every capability with a use case; a PRD "may not dictate a specific implementation"; UX
   notes are not "the place for pixel-perfect mockups".
10. Michael Nygard, *Documenting Architecture Decisions*,
    https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions — status "proposed" or "accepted", then
    "deprecated" or "superseded"; "The whole document should be one or two pages long"; "Large documents are never
    kept up to date" and are "too large to open, read, or update"; a reversed decision is kept "but mark it as
    superseded".
11. Martin Eriksson, *Product Requirement Documents Must Die* (Mind the Product),
    https://www.mindtheproduct.com/product-requirement-documents-must-die/ — PRDs are "almost always out of date" by
    the time they are written; the person who acts on a PRD is not its writer; the alternative is "high bandwidth
    communication" and prototypes.
12. Plane, *How to write a PRD that engineers actually read*,
    https://plane.so/blog/how-to-write-a-prd-that-engineers-actually-read — "no longer a 20-page blueprint",
    "typically runs between 3 and 6 pages"; engineers stop reading for missing context, ambiguous scope, vague
    language, no success metrics, and "stale documents with unclear ownership"; "precise, observable requirements";
    mark undecided items TBD and name "who owns answering"; one owner updates the doc after major decisions.
13. Cedric Chin, *Putting Amazon's PR/FAQ to Practice* (Commoncog),
    https://commoncog.com/putting-amazons-pr-faq-to-practice/ — "a one-page press release" that is "fiercely
    constraining"; "the FAQ portion addresses the assumptions you're making"; "The fact that most PR/FAQs don't get
    approved is a feature, not a bug"; the team "must decide if they will keep working on the product"; "Don't let
    the process drive you".
14. Joel Spolsky, *Painless Functional Specifications, Part 2: What's a Spec?*,
    https://www.joelonsoftware.com/2000/10/03/painless-functional-specifications-part-2-whats-a-spec/ — open issues
    are fine in a first draft but "By the time the programmers start work, all of these need to be stomped out"; a
    "nongoals" section; "The spec always reflects our best collective understanding"; specs "should be owned and
    written by one person".
15. WebSearch, ISO/IEC/IEEE 29148 requirement characteristics: arXiv 2408.10886 (*Leveraging LLMs for the Quality
    Assurance of Software Requirements*, https://arxiv.org/pdf/2408.10886) lists the standard's nine characteristics
    of an individual requirement (appropriate, complete, conforming, correct, feasible, necessary, singular,
    unambiguous, verifiable), "unambiguous" as one interpretation and "verifiable" as provable or measurable; arXiv
    1611.08847 (*Rapid quality assurance with Requirements Smells*, https://arxiv.org/pdf/1611.08847) on the split
    between set characteristics (completeness, consistency) and individual ones; Modern Requirements
    (https://www.modernrequirements.com/?p=32595) for the set's consistency including consistent terminology
    (search-level; the standard's text is not free).
16. WebSearch, Amazon working backwards PR/FAQ: reader's notes on Bryar and Carr, *Working Backwards*
    (https://www.goodreads.com/notes/55297149-working-backwards/50759819-thomas-hefke?page=2), the press release
    "always less than one page" and the FAQ "five pages or less"; Koji's guide
    (https://www.koji.so/docs/working-backwards-pr-faq-guide), "typically around six pages" (search-level; the book
    not read).

Files in this repository (all under `/home/user/wt-v12/`) and the renders:

17. `docs/PRD.md` at `0a557ff` (897 lines, 18,825 words by `wc -l -w`; per-section words and lines by an awk loop
    over `## ` and `### ` headings; grep counts for "must" (22 lines), "a session" (35), "the image" (46), "edition"
    (30), "the sheet" (12), "the track" (9), "the route" (7), "the picture" (3); "verified" clauses in lines
    207–236 (8, 65 words); words in lines 611–635 (393), 283–292 (164), 25–34 (209)); `docs/crit/prd/LOG.md`
    rounds 1–4; `docs/crit/prd/owner-messages.md` (21 messages); `docs/crit/prd/review-r03-2.md`,
    `review-r04-2.md` (mine); the must-fix headings of `review-r04-1.md` and `review-r04-3.md`.
18. `.github/workflows/profile.yml`: line 16 (`dry_run`), 110 (`build_assets.py --heartbeat`), 143, 147, 154 (the
    `dry_run` guards), 189–191 (`if: failure() && steps.stats.outcome == 'failure' && !inputs.dry_run` →
    `build_assets.py --no-sounding --heartbeat`).
19. `scripts/build_assets.py` 21, 187–188, 339–347, 423–445 (`no_sounding` set on `data`); `grep -rn no_sounding
    scripts/*.py scripts/sheets/*.py` (no reader under `sheets/route.py`); `scripts/sheets/log.py` 9–47
    (heartbeat).
20. `scripts/render_readme.py` 459 (`agents = agent_clause(r)`), 1003–1017 (the provenance line prints the run
    date); `assets/stats.json` `runcheck.rustmapper` (`date: 2026-10-10`, `runner: Linux x86_64`, `version: 0.1.3`,
    `scripts: ["rust_sitemap"]`; 25 steps, 7 gate).
21. `scripts/checks/position.py` 28–36; `scripts/checks/figures.py` 93–104 and `type.py` 35 (`FIGURES`, `TYPE`);
    `scripts/runcheck.py` 8; `scripts/checks/data.py` 69; `chart.toml` 665–669; `ls scripts/checks/*.py` (28);
    `grep -ohE '"[A-Z][A-Z0-9]*(-[A-Z0-9]+)+"|"(data|log)\.[a-z_]+"' scripts/checks/*.py | sort -u | wc -l` (169);
    `python3 -c "from sheets import route; len(route.PURPOSE)"` (17); `ls tests/` (24, no `test_prd.py`).
22. `git rev-parse --short HEAD` (`0a557ff`); `git diff --stat 027f081..HEAD -- . ':!docs'` (empty); `git log
    --oneline -5` (the four PRD fix commits over `9e3db34`).
23. `docs/BEN-TODO.md` 30–42 (the concept-stills ask; the bio sentence; the position line's shape);
    `docs/crit/prd/renders/round-16/gate.txt` (0 fail, 4 warn, exit 2: `log.shards`, POSITION-EMPTY,
    LICENSE-FLAGSHIP, ROUTE-WAITING S2).
24. Renders, `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/`:
    `sheet-phone-day-390.png` (the eleven elements of §5.1 that are drawn; the dotted box; the gap in the track under
    it), `page-phone-1.png` (the image, the link line, "Ben Russell builds", Languages, Stack), `page-desk-1.png`
    (the facts line with "authored 45 of its 146 commits and co-signed 1 of his own 101"; the code block's three
    comment lines wrapped at 32 columns; no photo, badge, counter or card); `README.md` on the branch (the
    provenance line "on 10 Oct 2026").
