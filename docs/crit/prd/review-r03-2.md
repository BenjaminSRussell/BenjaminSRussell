# PRD review round 3, reviewer 2: A product manager who has shipped from PRDs and rejects the vague ones

11 Oct 2026. Branch `v12/purpose`, worktree `/home/user/wt-v12`, HEAD `107a988` (the round-2 fix commit). I read
`docs/PRD.md` end to end (775 lines, 15,948 words; 691 lines at the round-1 fix), every message in
`docs/crit/prd/owner-messages.md`, `docs/crit/prd/LOG.md` (nothing below repeats a round-1 or round-2 fix), my own
round-2 review, `README.md`, `.github/workflows/profile.yml` lines 1–60 and its `dry_run` lines, `scripts/checks/position.py`,
`scripts/checks/alt.py`, `scripts/checks/readme.py` lines 110–130, `scripts/render_readme.py` lines 668–672,
`scripts/sheets/route.py` `PURPOSE` (lines 74–124), `tests/test_route.py` lines 812–830, `docs/crit/round6/SPEC.md` §0,
and `assets/stats.json` (22 repositories). I ran `python3 -m unittest` (539 tests, OK, 21.2 s), `git diff --stat
027f081..HEAD -- . ':!docs'` (empty: no product file has changed since the PRD's baseline), `git log -S` on the cron
line, and counted with `grep` every place the PRD restates a fact. I looked at the round-16 renders
`sheet-phone-day-390.png`, `page-phone-1.png`, `page-phone-2.png`, `page-desk-1.png` and read `gate.txt` (0 fail,
4 warn, exit 2). Outside: 13 sources (Sources, at the end).

My brief is the document as a PRD: could a builder who was not in the room build and accept this product from it
alone, and could the owner accept or reject the result from it.

## 1. Is the product this PRD defines what he wants?

**Yes.** The sentence that decides it is 9 Oct 11:37: *"If I was a fucking sailor pilot, if I am a sailor, if I was a
pilot, or if I was a fucking pirate, or if I was a shipping captain back in that day and age, what I'd want are very
helpful information. Things that very help. The map, very helpful. The fucking log, not really."* §1 defines one
image that is the way into his main tool (install, what happens to a URL in order, the two catches, the one key, the
file, who reads it next) and lookup text under it; I checked the phone sheet at 390 px against §5.1 again and it
carries T1, T2, R0, R2, S1, F1, H0, H1, C1, R13, R15 and nothing else, with no legend, no symbol, no shape sized by a
count. His second deciding sentence, 9 Oct 20:50, *"Everything, single thing inside of this needs a purpose, not a
fucking chasing a reason"*, is §5.1's table, and `route.py PURPOSE` has a row for every id in it.

His last message, 11 Oct (later), *"Review and ensure this is something I want to see rounds of reviews and
research"*, is the question this round answers: the product the PRD defines is the one worth reviewing, and §8.3
q.1–4 are his three questions from 20:50 made tickable. The caveat from my round-2 review still holds and the PRD now
says it itself (§9.1 row 0): until something merges, the page on `main` is the one he rejected on 9 Oct.

## 2. Verdict on the document

**7 / 10 as a PRD**, the same as round 2. What round 2 fixed holds: row 0 and the sequenced default make §9.1
decidable in one sitting; §6.1 describes the rollback that exists; §8.1 items 7 and 8 give the two owner rulings an
acceptance hook; §10 is a table with owners and blocking states; the baseline header is right (HEAD `107a988`
touches only `docs/`, so "code at `027f081`" is still true). A builder can draw the image from §5.1, predict a
release's effect from §5.4, run §8.1 items 1–3 and 5 from a clean checkout, and tick §8.3.

What keeps it at 7: the document grew 84 lines this round and the growth is not requirements. Twenty-five lines now
say which review round added or changed them, a history `LOG.md` already keeps (MF1). The "one home" rule the
PRD states for the mid-window trade is broken by the PRD itself, four times, and the §5.4 "three rows need a probe
here first" fact lives in nine places (MF2). One acceptance item names a gate that does not hold its second half
(MF3). §0 restates §9.1, §5.4 and §10.17 under "Status" (MF4). §2 says a test cuts an element that answers no
visitor question when the test checks only that a tag of the form `Q[1-5]` exists (MF5). §8.5 tells him to watch the
run page for failures that GitHub already emails him about, and says nothing about the 60-day rule that silently
stops a schedule (MF6). And the recommended option in §9.1 forks on a sub-choice whose second branch cannot pass the
gate as written, and whose first branch reverses a cap the code attributes to the owner (MF7). None of these needs
a new section; most are deletions.

## 3. Must-fixes, ranked

### MF1. The edit history is written into the requirements (PRD)

- **Where:** 25 lines of §0–§11 carry a "PRD round N" or "rNN-x MFn" attribution (`grep -n "PRD round"`): lines 6,
  34, 207, 258, 269 ("Corrected in PRD round 2; round 1's row described a path the workflow does not have"), 277
  ("PRD round 1's register cited 50 of them. Round 2 added…"), 389, 403, 407–408, 411–413 ("Added in PRD round 2 on
  the owner lens (r02-1 MF5)…"), 506 ("PRD round 1's 'the live page does not change' was true and not neutral"),
  523–525 ("Changed in PRD round 2 on the owner lens (r02-1 MF1, r02-2 MF2) from round 1's…"), 534, 553 ("PRD round
  1 said it in five places"), 575, 596, 601, 631. G8 (line 106) and G13a (line 112) carry the same inside the goal
  table; G13a even logs two reviewers' round-2 answers in its "Held by" cell.
- **What I checked:** every one of these events is already in `docs/crit/prd/LOG.md` under "Applied", by id, with
  the reasoning. The PRD's header (line 4) says the text is "edited only in a PRD review round", so the round is
  implied for every sentence; naming it inside the sentence tells a builder nothing about the product.
- **What to change:** Delete each attribution clause and keep the requirement. Where the sentence is only the clause
  (line 269's last sentence, line 277's second sentence, line 506's last clause, line 553's parenthesis, line 601's
  "items 1–7 are from the PRD's first draft, 8–16 from PRD review round 1, 17–20 from round 2"), delete the
  sentence. In G13a's "Held by" cell keep "review: §8.3 q.6, logged every round" and move the two round-2 answers to
  `LOG.md`. §8.1 items 6–8: keep the rule, the owner and "fails today: <lines>"; drop "moved here from §8.2 in PRD
  round 1 on the owner lens" and "added in PRD round 2 on the owner lens (r02-1 MF5)…". The one place a round
  belongs is the header's "Last updated".
- **Why:** Spolsky: a spec exists so that "you only have to communicate how the program is supposed to work once"
  [8]; the Google design-doc practice is that later amendments are "isolated into new documents" linked from the
  original rather than threaded through it [3]; Cagan's "record these decisions in the PRD" means the decision, and
  the PRD's own `LOG.md` is where the who-and-when already lives [1]. The owner's 11 Oct 01:12 brief asks for "all
  of the rules that must be followed and… how they are implemented", not when each was written.
- **About:** the PRD.

### MF2. The PRD's own "one home" rule is broken for the mid window and for the §5.4 gap (PRD)

- **Where:** §9.1b line 553 says *"This is the one home of the trade… §5.2, §7.4, §10.14 and §11 point here"*, but
  §5.2 line 167 states the whole trade again ("11.2 px at 852 to 17.7 px at 1,199… Under the phone's 13 px up to a
  930 px window; 13.7 px on a 1,024 px iPad held sideways"), §11 line 637 states it a third time ("The route's words
  are 11.2–13.0 px there, under the 13 px a phone gets. Accepted in writing by default"), and §7.4 line 339 a
  fourth ("11.2 px at 852 (§9.1b)"). The fact that three §5.4 rows need a probe or wording here before a fixed
  release helps is at lines 36–39 (§0), 222–224 (§5.4 prose, after the table already says it per row), 330 (§7.3's
  last row, with the five-and-three split spelled out again), 512 (§9.1 1b), 517–519, 545, 596, 615 (§10.9) and
  656 (§11).
- **What I checked:** `grep -n "11\.2" docs/PRD.md` gives five lines; the §10.9 fact by its wordings gives nine. The
  figures agree with each other and with `column.py` (`MIN_PX = 11.0`, `column_px(852)` = 482); the fault is
  repetition, not error.
- **What to change:** §5.2 mid row's last cell: *"11.2 px at 852 (floor 11, HERO-COLUMN-PX); the 852–930 window is
  §9.1b"*. §11 bullet 3: *"The mid window, 852–930 px: §9.1b, option a stands."* §7.4 row: drop "11.2 px at 852".
  For the §5.4 gap: §5.4's table and §10.9 are the two homes (what, and the fix); §0 bullet 3 becomes *"The blocker
  is outside this repository (§5.4; what must be written here first is §10.9)"*; §7.3's last row keeps its status
  and "§5.4 'Needs here'" and drops the row list; §9.1 1b keeps "plus §10.9"; lines 517–519, 545, 596 and 656 each
  become "(§10.9)".
- **Why:** INCOSE's set characteristic that a requirement appears once and C3 unambiguous [my round-2 source 9, not
  re-read]; the EARS point that free-form restatement is where requirements drift, since each copy is edited
  separately [4]; and the PRD's own rule at line 553. My round-2 MF5 asked for one home and the fix made one home
  plus three restatements.
- **About:** the PRD.

### MF3. §8.1 item 6's second half is held by nothing, and the item says a gate holds it (PRD; one small product change)

- **Where:** §8.1 item 6, lines 401–403: *"`[position] text` is set and at least one of `[contact] linkedin` /
  `resume` is set, so POSITION-EMPTY does not fire."*
- **What I checked:** `scripts/checks/position.py:30–31`: POSITION-EMPTY fires only when `[position] text` is
  empty. Lines 32–35 read `[contact]` and emit CONTACT-PLACEHOLDER only when a value contains ⟨ or ⟩; an empty or
  missing `linkedin`/`resume` emits nothing. `grep -rn contact scripts/checks/` finds no other reader. So a builder
  who sets the position line and leaves both contact keys empty sees POSITION-EMPTY go silent and reads item 6 as
  passed; the "so" in the sentence is false. The round-2 recruiter-side source wanted "an obvious way to contact
  this person" [my round-2 source 15]; the page has `Email` on the link line today (`README.md:21`), so the
  requirement is "one more than email", and nothing checks it.
- **What to change:** Split the item: *"6a. `[position] text` is set (POSITION-EMPTY silent). 6b. At least one of
  `[contact] linkedin` / `resume` is non-empty: CONTACT-EMPTY (warn), one `elif` in `position.py`; until it exists,
  §8.3 q.4's tick line 'the link line' includes 'and one contact beyond Email'."* Add §10 row 21 for the gate
  (owner: a session; blocks: merge through 6b).
- **Why:** Cagan's completeness test: "Can the QA team get enough information to design a test plan" [1]; the
  PRD's own §7 convention that every "must" names its holder; his 7 Oct 15:30 "tells a lot about me" is what item 6
  cites. A criterion that names the wrong gate is worse than one that names none.
- **About:** the PRD (the false "so"), and the product (one warning).

### MF4. §0 is a status report that restates three other sections (PRD)

- **Where:** §0 lines 18–46. Bullet 3 ("The blocker is outside this repository", lines 36–39) is §5.4's closing
  paragraph; bullet 4 ("The owner's decision (§9.1)", lines 40–44) is §9.1's default, row 0 and its cost, restated
  with the same quotes; bullet 5 (lines 45–46) is §7.6's PR row and §10.17; "Built" (lines 26–31) carries the run-12
  story that §8.5's first bullet carries; "Reviewed" (lines 32–35) is `LOG.md`'s summary. The header (lines 3–6)
  already holds Status, Owner, Baseline and Last updated.
- **What I checked:** each bullet against its section; no fact in §0 is only in §0 except the reading order
  (bullet 1) and the three mechanical results in "Built" (tests, gate, the job's run count).
- **What to change:** §0 becomes: bullet 1 as is (what this is, the reading order, the hand-check caveat); "Built"
  cut to its first two sentences plus *"the weekly job's state is §8.5"*; "Reviewed" to one line, *"Product and PRD
  review history: `docs/crit/prd/LOG.md`, `docs/crit/round6/LOG.md`"*; bullets 3–5 replaced by one line, *"Blocked
  on §9.1 (Ben); what must be written here first is §10.9; this branch has no PR (§10.17)."*
- **Why:** Amazon's PR/FAQ caps the whole document at a page plus five because "limiting length is a forcing
  function" [9]; Cagan: "don't worry about how pretty your PRD looks or how thick it is. So long as it's readable and
  understandable, it is the content that matters" [1], and content said twice is harder to keep true, as this
  PRD's own §6.1 history shows. Lenny's one-pager carries status in six prompts, not a page [12]. This is not the
  two-document split round 1 declined; it is cutting what is said elsewhere.
- **About:** the PRD.

### MF5. §2 claims a test cuts an element that answers no question; the test checks a tag's spelling (PRD)

- **Where:** §2 lines 71–73: *"Every element on the image and every block on the page is tagged with the question
  it answers; an element that answers none is cut (test T-PURPOSE, gate ROUTE-PURPOSE)."* §5.1's Q column tags R6
  (the loop bracket), S2 ("polite by construction") and F1 ("fetches up to 20 pages at a time…") as Q1, "Who is this
  and what does he build?".
- **What I checked:** `tests/test_route.py:826–829`: for each `PURPOSE` row the test asserts the learns-string is
  non-empty, `q` matches `^Q[1-5]$`, and the source string is non-empty. ROUTE-PURPOSE (`checks/route.py`) checks a
  drawn group has a row. Neither can tell Q1 from Q5; a builder who adds an element and tags it "Q3" passes. The Q
  tags in `route.py:74–124` match §5.1 exactly, so the PRD is faithful to the code; the overclaim is "answers".
  Whether "fetches up to 20 pages at a time from each host" tells a screener who he is, rather than an engineer what
  a site feels (Q5), is a judgement the PRD presents as gated.
- **What to change:** §2: *"…tagged by the author with the question it answers; T-PURPOSE and ROUTE-PURPOSE hold
  that every drawn element has a row and a tag Q1–Q5, not that the tag is right. The reviewer judges the tags at
  §8.3 q.1."* §8.3 q.1 gains a tick line: *"each element's Q is the question a stranger would ask of it; name any
  you would retag."* Optionally §5.1: retag R6, S2 and F1 as Q4/Q5 or say in one footnote why a fetch cap is a
  Q1 fact (the PRD's G1b argument: measured behaviour says what kind of engineer made it). The retag is product
  (`route.py`), the footnote is PRD; either is one line.
- **Why:** EARS exists because free-form requirements are "inherently imprecise" and the fix is a form whose pass
  condition is stated [4]; the PRD's §7.3 rule that nothing it says about a gate is untrue; the brief's question, is
  every requirement testable, and if not, does the document say so.
- **About:** the PRD (the claim); the product only if the tags are changed.

### MF6. §8.5 has the maintenance facts wrong way round: GitHub notifies, and a schedule can stop by itself (PRD)

- **Where:** §8.5 bullet 1, lines 474–477: *"A failed weekly run is Ben's to notice (the run page; the job's
  `::error::` lines)… noticed by PRD review round 2 (r02-2), not by him."* §6 line 237: *"GitHub ran run 12 at 12:52
  UTC, so a builder timing the first live run does not wait for 06:20"* with no reason given.
- **What I checked:** GitHub's docs: for scheduled workflows, failure notifications go to "the user who originally
  created the workflow", and if "another user edits the `schedule` cron syntax in the workflow file, that user
  receives later notifications instead"; a user can "choose to receive a notification only when a workflow run has
  failed" [5]. `git log -S'cron: "20 6 * * 0"' -- .github/workflows/profile.yml`: the cron line was last changed in
  `eeea9d1` by Benjamin Russell (9 Oct); the later `b466b7e` by "Claude <noreply@anthropic.com>" did not touch it.
  So run 12's failure went to his inbox if Actions notifications are on, and the PRD's "not by him" is unknowable
  from here. Same docs page on `schedule`: "The `schedule` event can be delayed during periods of high loads" (the
  12:52), and "In a public repository, scheduled workflows are automatically disabled when no repository activity
  has occurred in 60 days"; whoever re-enables a disabled schedule "will become the `actor`" for its runs [6]. A
  run that fails the gate commits nothing (§6.1 row 2); nine red Sundays in a row and the schedule stops, and the
  profile freezes on whatever ran last, with no run to be red.
- **What to change:** §8.5 bullet 1: *"GitHub emails the user who last edited the cron line (Ben, `eeea9d1`) when a
  scheduled run fails, if Actions notifications are on in his settings (GitHub docs, "Notifications for workflow
  runs"); a session must not edit that line, or the notifications follow the commit's author, which is no GitHub
  user. A failed run is a session's to fix. Scheduled runs are delayed under load (run 12: 12:52 for a 06:20 cron).
  In a public repository a schedule is disabled after 60 days without repository activity; a gate-failing streak
  commits nothing, so eight weeks red can stop the schedule silently; whoever re-enables it becomes its actor."*
  §6 line 237: replace "so a builder timing…" with the docs' sentence.
- **Why:** Cagan's release criteria include supportability, "often just hand-waved" [1]; ProductPlan: "if it isn't
  included in the PRD, it won't be included in the release" [13], and a maintenance rule that says "watch the page"
  when the platform emails is one a builder would follow to the letter.
- **About:** the PRD (maintenance section); the facts are the platform's.

### MF7. The recommended option forks, one branch cannot pass the gate as written, and the other reverses a cap the code attributes to the owner (PRD; the decision)

- **Where:** §9.1 row 2b, line 514: *"so the fold's cap goes to 8 (round 12 had it there) or the open list gets its
  own cap (§10.19); a session, before the merge."* §10.19, line 625: *"…and raise the fold's cap to 8… or give the
  open list its own cap and leave the fold's at 7; a test for the new state."*
- **What I checked:** `checks/readme.py:119–123`: `cautions(text, max_items=7, …)` caps the open list and the
  `<details>` fold at the same `max_items`. Under 2b the fold holds the four folded today (L3, X3, X2, X1) plus
  L4, L6, L2, L5: eight. "Give the open list its own cap and leave the fold's at 7" therefore fails README-CAUTIONS
  on the fold regardless of what the open list's cap is; the second branch is not an option. The first branch,
  cap 8: `render_readme.py:670`'s comment reads *"review round 13 (the owner): back to 7, for the open list and for
  the fold each (round 12 had raised it to 8 to fit X3)"*. So 2b's one change here reverses a ruling the code
  records as the owner's (round 13), and the PRD's "a session, before the merge" gives it to a session.
- **What to change:** §9.1 row 2b and §10.19: *"The fold's cap goes to 8 (`cautions(max_items=…)` for the fold
  only, or a second argument), which reverses the round-13 '7 for each' ruling recorded at `render_readme.py:670`;
  or one of the eight fold items is cut. Decides: Ben, one word in `LOG.md`; recommended: 8, since the fold is
  behind a click and the round-13 reason was the open list. Implements: a session, with a test."* Delete the
  "own cap for the open list" branch.
- **Why:** The brief's test for an open decision is options, costs, a recommendation and who decides; here one
  option does not work and the owner of the other is wrong. Spolsky: "A terribly common error is having a debate
  over how something should be designed, and then never resolving the debate" [8]; Shape Up's compare-to-baseline
  and the PRD's own §9 format.
- **About:** the PRD (the decision row) and the product change it names.

### MF8. Process rows sit in the goals table and the rules register, and the PRD says so itself (PRD)

- **Where:** §0 line 22: *"§7.6 and G17–G19 are how the session worked, not what the page is."* §3 G17–G19 (lines
  116–118), held by "16 rounds", "R1–R7 (360)", "the Workflow runs"; §7.6 (lines 371–383), ten rows about pushing,
  trailers, the stop hook, `BEN-TODO.md`.
- **What I checked:** none of the thirteen rows has a gate, a test, or a line in §8; three of §7.6's rows say
  "session; not verifiable from the repository". G17–G19 are his words and bind the *process*, which is why the PRD
  keeps them; they do not bind the page.
- **What to change:** Move G17–G19 and §7.6 to an "Appendix D. How the work was done, by his instruction", keeping
  the ids G17–G19 and the §7.6 row texts so every cite (`§7.6`, `G19`) still resolves; §3 and §7 end one row and
  one subsection shorter and renumber nothing. This is the part of round 1's declined r2 MF7 that does not touch
  the section numbers.
- **Why:** The Google design-doc note that "design docs that are really implementation manuals" (or here, process
  manuals) are a sign the content belongs elsewhere [3]; Atlassian's template holds "Not doing" and "Questions" but
  no "how we worked" [11]; a builder reading §3 for goals should not meet "Use multiple agents" as a goal of a web
  page.
- **About:** the PRD.

### MF9. Loose ends (PRD)

- §2's Q1 cell (line 77) is a 60-word research debate inside a table cell (7 s against 30–90 s, three guides
  quoted). Keep "a screener; the first-screen rule rests on 'first screen', not on a number" and put the sources in
  `LOG.md` round 2, where they already are.
- §5.3 row 6 (line 189) explains the comment-wrap trade in a table cell, and §11 bullet 2 explains it again. Row 6
  keeps the rule and the constants; the trade is §11's.
- §6 "Tests" (lines 253–258): the 91 off-page tests and the loader-walk method are §10.8's argument, not a
  requirement of the pipeline. One line: "539 tests; 91 of them belong to retired sheets (§10.8)."
- Header line 5: "`main` is 23 commits behind it" changes with every bot commit and every fix round; drop the
  number or date it.
- §8.3 line 453: "Round 16: no (8/7/8). The must-fixes left were copy (r16-3)…" is status inside the acceptance
  criteria; `LOG.md`'s.
- §9.1b row b: "computed in PRD round 2" (MF1 applies).

## 4. What holds, so nobody rewrites it

- The baseline header is true today: `git diff --stat 027f081..HEAD -- . ':!docs'` is empty, so "the product code
  at `027f081`" and "figures read at `e17cc80`" both stand at `107a988`.
- §8.1 item 4 is real: `profile.yml` has `workflow_dispatch` with a boolean `dry_run` input (lines 15–19) and the
  publish step switches on it (lines 143–148).
- §8.1 items 1 and 2: 539 tests pass here in 21 s; the round-16 `gate.txt` shows exactly the four warnings §8.2
  plus POSITION-EMPTY name, 0 fail, exit 2.
- §5.1's ids and Q tags equal `route.py PURPOSE` (17 rows, S2 and W1 undrawn); the alt text in `README.md:13` is
  25 words, not starting "The", last sentence 10 words, as ALT-* require (`alt.py:32–40`).
- §5.3 row 9: 22 repositories in `stats.json`, so "15 more" (22 − 1 − 2 − 4) holds and the README prints 15.
- §9.1's table now lets him choose from first-screen sentences; row 0 and the sequenced default are right, and the
  1a render exists. Only 2b's sub-choice (MF7) is undecidable.
- §6.1 is the rollback that exists. §8.4 has an owner and the right log. §10 has owners and blocking states.
- The non-goals (§4) are real non-goals and the renders break none: no legend, no symbol, no second image, nothing
  moves.

## 5. Research notes my lens needed

- **What a PRD is for.** Cagan's four areas (purpose, features, release criteria, schedule) and the two tests, "Can
  an engineer get enough understanding of the target" and "Can the QA team… design a test plan" [1]; this PRD
  passes both for §5 and §8.1 except where MF3 and MF5 name a holder that does not hold. Cagan's later view is that
  specs "are seldom read, they don't provide the necessary detail" and the prototype is the spec [2]; here the
  renders are that prototype and the PRD rightly points at them. The Mind the Product critique is that PRDs record
  solutions and garble through hand-offs [10]; this one records the owner's sentences first, which is the right
  defence, and its hand-off risk is length (MF1, MF2, MF4).
- **Length and form.** Amazon's PR/FAQ: a press release "always less than one page", an FAQ "five pages or less",
  because "limiting length is a forcing function" [9]. Google's design docs: "10–20ish pages" for a larger project,
  amendments as separate linked documents, and "implementation manuals" as the sign a doc has the wrong content [3].
  Atlassian's template and Lenny's one-pager are six to eight headings, with "Not doing", "Questions" and "Success"
  [11, 12]; ProductPlan adds assumptions and environment [13]. At 16k words this PRD is three times Amazon's cap and
  past Google's; the brief says not to add ceremony, so my asks are cuts.
- **Testability.** EARS gives the five shapes a testable requirement takes (ubiquitous, while, when, if-then, where)
  [4]; §5.1's "Drawn only when" column is EARS "while/when" in table form and is the best-written part of the
  document. §2's "answers a question" is the one requirement with no shape (MF5).
- **Maintenance on GitHub.** Failure notifications for scheduled workflows go to the workflow's creator or the last
  editor of the cron syntax [5]; schedules are delayed under load and disabled after 60 days without activity in a
  public repository [6]. The profile README itself has four conditions and no content limits [7].
- **Specs as the end of debate.** Spolsky: "having a debate over how something should be designed, and then never
  resolving the debate… These are the most likely projects to fail" [8]; §9.1 2b's fork (MF7) is that debate in
  miniature.

## 6. Score

**7 / 10.** The product is what he asked for, by 9 Oct 11:37 and 20:50. The PRD is decidable and traceable, and its
facts check. It loses a point for carrying its own edit history and its restatements, which a builder must read past
and a fix pass must keep in step (MF1, MF2, MF4, MF8, MF9); a point for the two places a requirement names a holder
that does not hold it (MF3, MF5); and a point for the maintenance section that has the platform's behaviour
backwards and for a recommended option whose sub-choice does not work as written (MF6, MF7). Every fix above is a
deletion, a one-line correction or a table-row edit; none adds a section.

## Sources

Outside sources (read with WebFetch unless marked otherwise):

1. Martin Cagan, *How To Write a Good PRD* (SVPG, 2005), https://www.svpg.com/assets/Files/goodprd.pdf — text
   extracted locally from the PDF: "So long as it's readable and understandable, it is the content that matters";
   "The release criteria are often just hand-waved, but a good PRD puts considerable thought into what the true
   minimum requirements are" (performance, scalability, reliability, usability, supportability, localizability);
   Step 9 "Can an engineer get enough understanding of the target… Can the QA team get enough information to design
   a test plan"; Step 10 "Resolve all questions about requirements by pointing people to the PRD. If it's not in the
   PRD, put it in the PRD… record these decisions in the PRD"; "the PRD is a living document".
2. Martin Cagan, *Revisiting the Product Spec*, https://www.svpg.com/revisiting-the-product-spec/ — "most specs
   take too long to write, they are seldom read, they don't provide the necessary detail"; the spec as "a false
   indicator to management"; "the high-fidelity prototype" as the one form that delivers; the spec "must accurately
   represent the behavior of the software".
3. Malte Ubl, *Design Docs at Google*, https://www.industrialempathy.com/posts/design-docs-at-google/ — "The sweet
   spot for a larger project seems to be around 10-20ish pages"; non-goals "aren't negated goals like 'The system
   shouldn't crash'"; "design docs that are really implementation manuals" as a sign a doc is unnecessary; later
   changes "isolated into new documents" linked from the original; re-read your own docs a year or two later.
4. Alistair Mavin, *EARS (Easy Approach to Requirements Syntax)*, https://alistairmavin.com/ears/ — the five
   patterns (ubiquitous; While; When; If/Then; Where) with their templates; free-form requirements are "inherently
   imprecise" and defects propagate to lower levels.
5. GitHub Docs, *Notifications for workflow runs*,
   https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/monitoring-workflows/notifications-for-workflow-runs
   — the person who triggered a run is notified; for scheduled workflows "the user who originally created the
   workflow", or whoever last "edits the `schedule` cron syntax"; after re-enabling, whoever re-enabled it; the
   option to be notified "only when a workflow run has failed".
6. GitHub Docs, *Events that trigger workflows*, "schedule",
   https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows
   — "The `schedule` event can be delayed during periods of high loads"; "In a public repository, scheduled
   workflows are automatically disabled when no repository activity has occurred in 60 days"; a user who changes the
   cron of a deactivated workflow "will become the `actor` associated with any workflow runs".
7. GitHub Docs, *Managing your profile README*,
   https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
   — the four conditions (repository named after the user, public, `README.md` at the root, any content); the
   README is to "tell other people about yourself"; no stated content limits.
8. Joel Spolsky, *Painless Functional Specifications, Part 1: Why Bother?*,
   https://www.joelonsoftware.com/2000/10/02/painless-functional-specifications-part-1-why-bother/ — "A terribly
   common error is having a debate over how something should be designed, and then never resolving the debate";
   "all the hard decisions are pushed to the end. These are the most likely projects to fail"; "you only have to
   communicate how the program is supposed to work once".
9. Amazon, *An insider look at Amazon's culture and processes*,
   https://aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes — the PR/FAQ: the press
   release "a few paragraphs, always less than one page"; the FAQ "five pages or less"; limiting length is "a forcing
   function—we have seen that it develops better thinkers and communicators". (Found by WebSearch; the page read.)
10. Mind the Product, *Product Requirement Documents Must Die*,
    https://www.mindtheproduct.com/product-requirement-documents-must-die/ — PRDs force solutions "up front" before
    the problem is understood; hand-offs are "playing telephone/chinese whispers with your product"; replace with
    collaborative prototyping and customer testing. (Found by WebSearch; the page read.)
11. Atlassian, *Product requirements template* (Confluence),
    https://www.atlassian.com/software/confluence/templates/product-requirements — sections Objective, Assumptions,
    Options, Success metrics, supporting documentation; "list what's out of scope for this feature or release"; a
    table "to jot down those questions as they come to you"; one "single source of truth".
12. Atlassian, *Lenny's Product Requirements template*,
    https://www.atlassian.com/software/confluence/templates/lennys-product-requirements — six prompts: Description
    "What is it?", Problem, Why "How do we know this is a real problem and worth solving?", Success "How do we know if
    we've solved this problem?", Audience, What.
13. ProductPlan, *Product Requirements Document*, https://www.productplan.com/glossary/product-requirements-document/
    — objective, features ("a description, goal and use case at a minimum"), UX flow, system and environment
    requirements, "Assumptions, Constraints & Dependencies"; the PRD "serves as the document of record that the
    entire release is based on… if it isn't included in the PRD, it won't be included in the release".

Files in this repository (all under `/home/user/wt-v12/`) and the renders:

14. `docs/PRD.md` (775 lines, 15,948 words at `107a988`), `docs/crit/prd/LOG.md`, `docs/crit/prd/owner-messages.md`
    (21 messages), `docs/crit/prd/review-r02-2.md` (my round-2 review; its sources 9 and 15 are cited above as
    "round-2 source", not re-read).
15. `.github/workflows/profile.yml` lines 1–60 (triggers, `dry_run` input, `push: paths`), 143–148 (publish and
    dry-run steps), 189; `git log -S'cron: "20 6 * * 0"' -- .github/workflows/profile.yml` → `eeea9d1` Benjamin
    Russell, 9 Oct; `git log -1 -- .github/workflows/profile.yml` → `b466b7e` Claude, 10 Oct.
16. `scripts/checks/position.py` lines 28–43 (POSITION-EMPTY on empty text only; CONTACT-PLACEHOLDER on ⟨ ⟩ only);
    `grep -rn contact scripts/checks/` (no other reader).
17. `scripts/checks/readme.py` lines 110–130 (`cautions(text, max_items=7, max_words=25)`: the fold capped at
    `max_items` too); `scripts/render_readme.py` lines 668–672 (`LIST_MAX_ITEMS = 7`, the round-13 comment);
    `chart.toml`: four `fold = true` entries.
18. `scripts/sheets/route.py` lines 74–124 (`PURPOSE`: 17 rows, Q tags as in §5.1); `tests/test_route.py` lines
    812–830 (`test_every_element_has_a_purpose`: ids, containment, `^Q[1-5]$`).
19. `scripts/checks/alt.py` lines 3, 32–50; `README.md` line 13 (the alt, 25 words), line 21 (the link line with
    `Email`); `assets/stats.json` (22 `repos`); `docs/crit/round6/SPEC.md` line 14 (§0, the one sentence).
20. `git rev-parse --short HEAD` → `107a988`; `git log --oneline -6`; `git diff --stat 027f081..HEAD -- . ':!docs'`
    (empty); `python3 -m unittest` → 539 tests OK in 21.163 s.
21. Renders, `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/`:
    `sheet-phone-day-390.png`, `page-phone-1.png`, `page-phone-2.png`, `page-desk-1.png`, `gate.txt` (0 fail, 4
    warn: `log.shards`, POSITION-EMPTY, LICENSE-FLAGSHIP, ROUTE-WAITING; exit 2).
