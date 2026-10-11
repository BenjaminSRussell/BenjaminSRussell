# PRD review round 4, reviewer 2: A product manager who has shipped from PRDs and rejects the vague ones

11 Oct 2026. Branch `v12/purpose`, worktree `/home/user/wt-v12`, HEAD `92b1bef` (the round-3 fix commit). I read
`docs/PRD.md` end to end (831 lines, 17,288 words; 775 lines at round 3), every message in
`docs/crit/prd/owner-messages.md`, `docs/crit/prd/LOG.md` (nothing below repeats a round-1, 2 or 3 fix), my own
round-3 review, `README.md` on the branch and on `main` (`git show main:README.md`), `.github/workflows/profile.yml`
whole, `scripts/publish_chart.py` lines 1–95, `scripts/render.mjs` lines 1–25, `scripts/checks/position.py` 28–36,
`scripts/checks/column.py` 44–51, `scripts/render_readme.py` 455–462 and 670–671, `chart.toml` 24–40, 665–669 and
1003–1031, `tests/test_route.py` 829, 894, 1052, `docs/BEN-TODO.md`, `.gitignore`, and the round-16 renders
`sheet-phone-day-390.png`, `page-phone-1.png`, `page-desk-1.png`. I ran `git ls-files | grep -c '\.png$'` (0),
`ls tests/` (24 files, no `test_prd.py`), `ls scripts/checks/*.py` (28 plug-ins plus `__init__`), and a word count per
section. Outside: 15 sources (Sources, at the end).

My brief is the document as a PRD: could a builder who was not in the room build and accept this product from it
alone, and could the owner accept or reject the result from it.

## 1. Is the product this PRD defines what he wants?

**Yes.** The sentence that decides it is 9 Oct 11:37: *"It has to be helpful knowledge. If you were a fucking real
sailor, if you were a real person, you'd want it to be helpful data that you're looking at. You're going through,
you're like, oh, it's very helpful, and it's in a cool format."* The image §1 and §5.1 define is directions a
stranger uses (the install line, the command, what each page meets, the two catches, the one key, the file, who
reads it next) and nothing else; the phone sheet at 390 px carries T1, T2, R0, R2, S1, F1, H0, H1, C1, R13, R15 and
no legend, symbol or sized shape. The test he set on 20:50, *"Everything, single thing inside of this needs a
purpose, not a fucking chasing a reason"*, is §5.1's table with a Q for every row.

His last message, 11 Oct (later), *"Review and ensure this is something I want to see rounds of reviews and
research"*, deserves a straight answer beyond "yes". The product is one he wants. The rounds are another matter:
three PRD rounds have changed only `docs/` (`git diff --stat 027f081..HEAD -- . ':!docs'` is empty; the PRD says so
at line 7), while §10 carries eight open items owned by "a session" and §8.1 carries two that fail today. The reviews
are improving the description of a page that is not moving toward his profile. That is the fact this round should
put in front of him, and MF1, MF4 and MF6 are about it.

## 2. Verdict on the document

**6 / 10 as a PRD**, down from 7. What rounds 1–3 built still holds: §5.1 and §5.4 are the best-written requirements
I have reviewed in this series (EARS-shaped "drawn only when" conditions, each checked against a resolver run); §8.1
items 1–3 are commands a stranger can run; §6.1 names a rollback; §10 has owners and blocking states; the baseline
header is true at HEAD. The register (§7) is what he asked for on 11 Oct 01:12 and I do not ask for it to be cut.

What takes the point: the document now describes everything about the page except how it reaches his profile. The
first merge has no sequence, and the three rules that govern it (§8.1 item 5, §8.4 "before merge", appendix D "never
push to `main`") cannot all hold as written, because the branch's sheets share paths with the live v11 sheets and a
non-dry `workflow_dispatch` on the branch pushes the branch to `main` (MF1). The renders every decision in §9 rests
on are in a session scratchpad, not in the repository, so the person the PRD asks to decide "with the 2b render open"
cannot open it (MF2). §9.1 calls two different things "what undecided means" (MF3). §9.0 says three inputs are his
and "everything else is a session's", when a fourth blocker is his and a session exists only when he starts one
(MF4). §6.1 tells a session to commit to `main` and appendix D forbids it (MF5). §10.12 says it blocks this round,
and this round ran (MF6). None of these is long to fix; all of them are the kind of gap a reader not in the room
falls into on the day of the merge.

## 3. Must-fixes, ranked

### MF1. The first merge has no sequence, and the rules that govern it contradict each other (product and PRD)

- **Where:** §8.1 item 4 (line 391), item 5 (line 393); §8.4 heading "(once, before merge)" and its first sentence
  "Open the profile on an iPhone" (lines 452–454); §6 bullet 1 (lines 233–240); §11's stale-sheet bullet (lines
  669–680); appendix D row 1 (line 823).
- **What I checked:**
  - `git show main:README.md | grep -o 'chart/assets/v9/[a-z0-9-]*\.svg' | sort -u` → `hero-day`, `hero-night`,
    `hero-phone-day`, `hero-phone-night`, `hero-phone-still-day`, `hero-phone-still-night`, `hero-still-day`,
    `hero-still-night`. The branch's `README.md` names `hero-day`, `hero-night`, `hero-phone-day`, `hero-phone-night`,
    `hero-mid-day`, `hero-mid-night`. Four paths are shared. `publish_chart.py` (docstring, lines 2–14) force-pushes one
    orphan commit holding only what the build report names. So the first v12 publish replaces the live page's four
    sheets under v11's text and alt ("22 repositories by week…") and removes the four `still` paths v11's `<source>`
    lines point at; until then, a v12 README on `main` names two `mid` editions the `chart` branch lacks, the exact
    8 Oct 11:13 surprise (§7.4's last-but-two row).
  - `profile.yml`: job `chart` checks out `actions/checkout@v4` with no `ref` (lines 72–74), so a `workflow_dispatch`
    on the branch builds the branch; the commit step (lines 150–186) runs `git pull --rebase --autostash origin main
    && git push origin HEAD:main` whenever `dry_run` is false. A non-dry dispatch on `v12/purpose` therefore rebases
    the branch onto `main` and pushes it: it *is* the merge, done by the bot, not by him. The PRD never says so;
    §8.1 item 4 asks for a dry run and leaves the reader to discover what the other setting does.
  - GitHub's docs: the dispatch button exists because `main` has a `profile.yml` with the same `dry_run` input
    (`git show main:.github/workflows/profile.yml` lines 14–16); "To trigger the `workflow_dispatch` event, your
    workflow must be in the default branch", and the branch to run on is chosen in the UI or with `gh workflow run
    --ref` [1, 2].
  - §8.4 says "Open the profile". The profile shows `main`'s README [3]. Before the merge the v12 page exists only
    at the branch view (`github.com/BenjaminSRussell/BenjaminSRussell/tree/v12/purpose`), and its image exists on
    GitHub only after a publish. So the device check cannot be "before merge" and "the profile" at once.
- **What to change:** a new §8.1 item 9, **"The first merge, in order"**, as a decision with the two sequences
  costed: *(A) publish first:* from a branch build, `python3 scripts/publish_chart.py` (a session with push, or Ben),
  then Ben merges within the hour; cost: for that hour the live v11 page shows the v12 hero under v11's text and its
  `still` sources 404; gain: item 5 holds on the merge commit, and §8.4 can be run on the branch view before the
  merge. *(B) merge first:* Ben merges; the push to `main` (it touches `scripts/`, `profile.yml:21–27`) runs the job,
  which publishes before it commits; cost: until that run's publish step (minutes, longer under load), the profile
  shows the new text over the old hero and broken `mid` images; item 5 does not hold on the merge commit and must be
  reworded "on the first run after the merge". Recommend A, decided with §9.0 (c). Either way add one sentence to
  item 4: *"A `workflow_dispatch` with `dry_run` false on any branch pushes that branch's HEAD to `main`
  (`profile.yml:150–186`); only the dry run is permitted before his merge."* §8.4 becomes "(once; the branch view
  after the publish, or the profile within a day of the merge, with §6.1 as the back-out)". §11 gains the first-merge
  window beside the weekly one.
- **Why:** Cagan: release criteria are "often just hand-waved", and supportability is one of them [5]; the Scrum
  Guide: an Increment that does not meet the Definition of Done "cannot be released" [8], and here the Definition
  (§8.1 item 5) cannot be met by the route the document leaves open; his 8 Oct 11:13 "Merged but all images are
  unavailable" is the very event this sequence exists to prevent, and his 8 Oct 09:04 "all PRs need to be ready to
  merge" means ready for *him* to merge, not for a bot.
- **About:** the product (a publish step and one workflow warning) and the PRD (the sequence and the §8.4 wording).

### MF2. The evidence the decisions rest on is outside the repository (PRD)

- **Where:** header Sources (line 14: "the round-16 renders", no path); §9.1 (lines 551, 563: "at the session's
  `scratchpad/prd-r02/once-1a/`", "`scratchpad/prd-r03/once-2b/`"); §9.0 (c) ("yes or no to merging 2b", which
  §9.1 says to decide "with the renders in hand", line 541); §8.3 q.3 and q.4, which tick against "the first two
  phone screens"; §10.16 and §11, which cite `page-desk-1.png`.
- **What I checked:** `git ls-files | grep -c '\.png$'` → 0. `.gitignore` excludes `out/` and `assets/v9/`. The 1a
  and 2b directories exist in this session's scratchpad (`ls` shows `page-phone-1..7.png`, `sheet-phone-day-390.png`,
  `preview.mjs`, `preview_phone.mjs`, `preview_mid.mjs`), and nowhere else; the page previews are made by those
  three `.mjs` files, which are not in `scripts/` (`scripts/render.mjs` has a `phone` mode for an SVG and a `matrix`
  mode marked "placeholder… needs the README preview page", lines 12–13). So a reader of the repository can rebuild
  the SVGs (`build_assets.py`) but not the page screenshots, and cannot see any of the three renders §9.1 compares.
- **What to change:** commit the three render sets under `docs/crit/prd/renders/{round-16,once-1a,once-2b}/` (at
  least `sheet-phone-day-390.png`, `page-phone-1.png`, `page-phone-2.png`, `page-desk-1.png`, and the fixture
  `stats-once-*.json`), and the three preview scripts under `scripts/preview/`; cite the repository paths in §9.1,
  §10.16, §11 and the Sources line. If the fix pass may not add binaries, say so in §0 in one sentence ("the renders
  are not in the repository; a session rebuilds them with …") so the document stops presenting them as available.
- **Why:** the brief's test is a reader not in the room; Cagan: "If it's not in the PRD, put it in the PRD" [5], and
  his later view that the prototype, not the prose, is what engineers build from [my round-3 source 2, not re-read],
  which this PRD agrees with by pointing at renders; Google's design-doc lifecycle keeps the doc as the lasting
  record of the trade-offs [7]. His 9 Oct 20:50 *"Review the mapping again, the first map"* is a request to look at
  the thing; the PRD asks him to decide on a picture it cannot show him.
- **About:** the PRD (its sources and the §9.0 ask); no page change.

### MF3. §9.1 labels two different things "what undecided means" (PRD)

- **Where:** §9.1 table row 0, line 526: *"0. Leave `main` as it is (what 'undecided' means)"*; §9.1 bullet 1, line
  541: *"Default while undecided: merge 2b now"*. Also §9.2's "Default: strike; not yet implemented" (line 600) uses
  "default" for a state that is not the state of the page.
- **What I checked:** only Ben merges (appendix D row 1), so "merge 2b now" cannot happen without his (c); what
  happens if he does nothing is row 0. The two sentences give "default" opposite meanings 15 lines apart.
- **What to change:** line 541: *"**Recommended:** merge 2b now, then decide 1a against 1b with the renders in hand.
  **If nothing is decided:** row 0, every week."* §9.2: *"Recommended: strike. Today: the counts print (G8 open).
  Blocks the merge through §8.1 item 7."* Keep "default" for the one place it is true, §9.1b (option a is what the
  code does today).
- **Why:** Nygard's decision record separates "proposed" from "accepted" and keeps the superseded state visible [9];
  Spolsky: a debate "never resolved" is the project most likely to fail [6]; ISO 29148's set characteristic that
  requirements do not contradict each other and terminology is consistent [12].
- **About:** the PRD.

### MF4. §9.0 is short one blocker, and "a session" is not an owner (PRD)

- **Where:** header line 3 ("Waits on three inputs from Ben"); §9.0 (lines 500–505: (a), (b), (c); "Everything
  else is a session's"); §8.4 (owner Ben; §8.3 "Done" requires it logged; §10.4 "blocks: merge"); the Owner column
  of §10 and §8.2 (26 lines name "a session"); §8.5 ("A failed run is a session's to fix"); §9.0 (b) and §8.1 item 7
  ("unless Ben has written 'keep' or 'share'… in `docs/crit/prd/LOG.md`").
- **What I checked:** §8.4's owner is Ben and nothing else can do it ("the session has no device"); it blocks Done;
  it is not in §9.0, so "three inputs" is four. Every "a session" item waits on him opening a session; the PRD never
  says so, and §8.5's maintenance owner is therefore nobody until he does. On the recording mechanism: his 21
  messages are all session messages; `owner-messages.md` is how they reach the repository; nothing in the history
  shows him editing a `docs/` file, and `BEN-TODO.md` asks him to edit `chart.toml`, not logs.
- **What to change:** §9.0: *"(d) The device check, §8.4, after MF1's publish or within a day of the merge."* Then one
  sentence: *"A session acts only while Ben has one open. Every owner below that reads 'a session' is work he starts;
  until he does, those rows do not move, and §8.5's failed-run fix has no one."* §9.0 (b) and §8.1 item 7: *"his word
  in a session (which the session records verbatim in `owner-messages.md` and as one line in `LOG.md`)"* instead of
  "Ben has written … in `LOG.md`". Header: "four inputs".
- **Why:** Atlassian's template opens with "Who is on the core team?" because an owner who cannot act is no owner
  [10]; Cagan's "must-have… the product should not ship if even one… is not ready" presumes someone holds each one
  [5]; the Scrum Guide puts the Definition of Done on a team that exists [8]. His 9 Oct 20:50 *"It should not be
  done until it goes over at least 10 reviews"* names reviews, not a device; the device check is a rule the PRD made
  from his 11:32 words and it must say who, when, and that only he can.
- **About:** the PRD.

### MF5. §6.1's rollback breaks appendix D's first rule (PRD)

- **Where:** §6.1 row 3, line 261: *"Rollback is local: Ben or a session checks out the last good `assets/stats.json`,
  runs … and commits `stats.json`, `README.md` and `DESIGN.md` to `main`"*. Appendix D row 1, line 823: *"Never push
  to `main`; the owner merges PRs."*
- **What I checked:** `profile.yml` `push: paths` (lines 21–27) are `scripts/**`, `chart.toml`, `assets/log.json`,
  `requirements.txt`, the workflow; `README.md`, `assets/stats.json` and `DESIGN.md` are not among them, so a
  rollback PR that touches only those three does not re-survey on merge, which is what §6.1 wants. One that also
  reverts code or `chart.toml` does re-survey, and the rebuild must then pass the gate.
- **What to change:** *"…and opens a PR with `stats.json`, `README.md` and `DESIGN.md`; Ben merges it (appendix D).
  Those three paths are not in `push: paths` (`profile.yml:21–27`), so the merge does not re-survey; if the fault is
  in code or `chart.toml`, that revert is a second PR, and its merge re-surveys."*
- **Why:** ISO 29148: a requirement set is consistent [12]; a rollback a builder follows to the letter against a
  standing rule is the worst kind of instruction; his "never push to `main`" is a standing instruction (appendix A's
  last paragraph).
- **About:** the PRD.

### MF6. §10.12 says it blocks this round; this round ran without it (PRD; one product item)

- **Where:** §10.12, line 648: *"Blocks: the next PRD round (the register cannot score above 7 while it is checked by
  nobody…)"*; §0 bullet 1 (lines 26–28); `LOG.md` round 3 "Next round": *"since §10.12 now blocks the round"*.
- **What I checked:** `ls tests/` → 24 files, no `test_prd.py`; the PRD's register was not re-checked by a script in
  this round's brief. So the one row whose "Blocks" cell names a PRD round did not block it. The same column marks
  §10.5 and §10.8 as blocking the merge; a reader who sees one blocking cell ignored discounts the others.
- **What to change:** either the test exists before round 5 (a session; the spec is already written in the row), or
  the cell reads "nothing" and §0's "cannot score above 7" goes. A "Blocks" column that is not enforced is removed,
  not kept as advice. If the test is written, the PRD's hand-check sentence in §0 becomes "`tests/test_prd.py` holds
  the register".
- **Why:** Cagan's must-have classification "must not be taken lightly… the product should not ship if even one…
  is not ready" [5]; the Scrum Guide's Definition of Done is "a formal description", not a wish [8]; his 11 Oct 01:12
  asks how the rules "are implemented", and the PRD's own rule about itself is the one implemented by nothing.
- **About:** the PRD (the column) and the product (one test file).

### MF7. The C1 wrong-step fact, added in round 3, has six homes (PRD)

- **Where:** §5.1 C1's "Drawn only when" cell (line 147); §5.4 row 1 "Needs here" (line 208); §5.4's closing paragraph
  (lines 217–220); §9.1 row 1a (line 527); §9.1's 1a-render bullet (lines 559–560); §10.9 (line 645).
- **What I checked:** `grep -n "Ctrl-C\|ends_by_itself" docs/PRD.md`; each of the six states the whole fact (both
  wordings hold on `crawl_ctrl_c`/`second_ctrl_c`; neither names `ends_by_itself`; the sheet still says "press
  Ctrl-C"), four of them with the `chart.toml:1005–1030` cite. Round 3 applied my round-3 MF2 ("§5.4's table and
  §10.9 are the two homes") and then added this fact to four more places in the same pass.
- **What to change:** §5.4 row 1 and §10.9 keep the full text. §5.1 C1's cell ends at "probes as stated; a release
  that exits leaves this row wrong (§5.4 row 1)". §9.1 1a: "Ctrl-C once stops early, once §10.9's C1 wording exists".
  The 1a-render bullet: "the Ctrl-C row is unchanged (§5.4 row 1)". §5.4's closing paragraph drops "and leaves a wrong
  step on C1" (the table above it says so).
- **Why:** the PRD's own one-home rule (§9.1b, line 579) and §4's "This is the one home of that rule"; ISO 29148's
  "singular" and the set's "consistent" [12]: six copies are six places to drift when §10.9 is done.
- **About:** the PRD.

### MF8. §4 should name the profile-README conventions the page rejects, as choices (PRD)

- **Where:** §4 Non-goals, lines 111–123.
- **What I checked:** the conventions a stranger expects of a GitHub profile README, from GitHub's own page (the
  generated file "is pre-populated with a template to give you some inspiration" [3]) and the curated list every
  guide links (16 categories: GitHub Actions, Game Mode, Dynamic Realtime, Badges, Icons, GIFs, Just Images, Retro…;
  the tools it lists are stats cards, streak and trophy cards, shields, visitor counters [14]), are: a photo or
  avatar, a greeting and bio paragraph, a "currently learning / open to" line, a badge or icon grid for the stack,
  pinned-repo cards, a visitor counter, a social-badge row. The page has none of a photo, a bio paragraph, badges,
  icons, counters or cards (`page-phone-1.png`, `page-desk-1.png`: the Stack line is plain text). §4 excludes the
  stats card, the themed poster, the methods section, the to-do list, the second image and animation; it does not
  say the bio, the badge grid and the pinned cards were considered and left out, or why. A builder not in the room
  reads "tells a lot about me" (7 Oct 15:30) and adds a paragraph and a badge row.
- **What to change:** three bullets: *"Not a bio. No photo, no greeting, no narrative paragraph, no timeline; the
  one line of status is `[position] text` (8 Oct 14:52: 'Don't tell the user show the user'). Not a badge wall. No
  shields, icon grid or visitor counter; the Stack line is words (G1d: decoration is not care). Not a card deck. No
  pinned-repo or stats cards; 'Also' and the 15-more fold are the only lists."*
- **Why:** Google: non-goals are "things that could reasonably be goals, but are explicitly chosen not to be goals"
  [7]; Shape Up's "No-gos: anything specifically excluded from the concept: functionality or use cases we
  intentionally aren't covering" [13]; Spolsky: "start culling features right away… with a 'nongoals' section" [6].
- **About:** the PRD; the page already complies.

### MF9. Loose ends (PRD)

- §8.1 item 2 says warnings "only from §8.2", and §8.2's `log.shards` row says it "goes with the retired `log`
  module (§10.8)", which item 8 deletes before the merge; after item 8 the allowed set is two warnings, and the
  table should say so or the merge commit fails item 2 by its own wording.
- §0 "Built" (line 31) carries "4 warnings (§8.2), exit 2" while §8.2 lists three and names POSITION-EMPTY as the
  fourth in prose; one number in one place.
- Length: 17,288 words. The sections §0 names for building and accepting (§1, 2, 4, 5, 8, 9, 11) are 434 lines and
  7,930 words; the register and appendices are the rest. I do not ask for a cut beyond MF7; the register is what he
  asked for. But the header should say the reading split in words, so a builder budgets an hour, not a day.

## 4. What holds, so nobody rewrites it

- The baseline header is true at `92b1bef`: no product file has changed since `027f081`; every line cite I opened
  (`render_readme.py:459` `agent_clause(r)`; `position.py:31` POSITION-EMPTY on empty text only, 32–35 placeholders
  only; `column.py:47–50` `TALL_FROM`, `TALL_PX`, `DESK_MIN_PX`; `chart.toml:26, 30–31` empty, `:35–39` the five
  keys, `:1005–1030` C1 with `runs = ["crawl_ctrl_c", "second_ctrl_c"]`; `test_route.py:829, 894, 1052`;
  `render_readme.py:670–671`) points where the PRD says.
- §5.1 matches the round-16 phone sheet element for element; the desk page (`page-desk-1.png`) shows the facts line
  with the agent-authorship counts, as §8.1 item 7 says it does today.
- §8.1 item 4 is real and safe as written (`dry_run` skips publish and commit: `profile.yml:143–153`).
- §5.4's table is the right shape for a product that is a function of another repository's state; nothing like it
  is in any template I read, and it should stay.
- §9.1b is a decision done properly: options, cost, who, default that is the code's behaviour.
- The non-goals that are there are real non-goals and the renders break none of them.

## 5. Research notes my lens needed

- **What a PRD must settle before building.** Cagan: release criteria "often just hand-waved" (performance,
  scalability, reliability, usability, supportability, localizability); a schedule described as "context and
  motivation for the timeframe"; the two completeness tests (an engineer, the QA team); "If it's not in the PRD, put
  it in the PRD… record these decisions in the PRD" [5]. Spolsky: a spec's first version may leave open issues, but
  "by the time the programmers start work, all of these need to be stomped out", and "the spec always reflects our
  best collective understanding of how the product is going to work" [6]. This PRD's open issue is the merge itself
  (MF1).
- **Decisions.** Nygard's record has title, context, decision, status (proposed, accepted, deprecated, superseded),
  consequences, and is "one or two pages long" because "large documents are never kept up to date" [9]. The PRD's
  §9 rows are close to this; MF3 is the status field. Shape Up's pitch has five ingredients, and "no-gos" is one of
  them [13].
- **Length and form.** Amazon's PR/FAQ is a one-page press release and a FAQ of about five pages, "around six pages"
  in all; "the FAQ is where the rigor lives" [11, 15]. Google's sweet spot is "10–20ish pages", with non-goals that
  "could reasonably be goals" and "alternatives considered" as "one of the most important" sections [7]. Atlassian's
  template opens with target release, status and the core team, and ends with "what's out of scope" [10]. At 17k
  words this PRD is far past all three; the brief says not to add ceremony, so my asks are a sequence, a status word,
  an owner sentence, and cuts.
- **Testability.** ISO 29148's characteristics for a requirement (unambiguous, singular, verifiable, complete,
  feasible) and for the set (complete, consistent, feasible) [12]; MF3, MF5 and MF7 are set-consistency failures.
  The Scrum Guide's Definition of Done: work that does not meet it "cannot be released or even presented" [8].
- **GitHub mechanics the merge depends on.** `workflow_dispatch` needs the file on the default branch and runs on
  the branch chosen in the UI or `--ref` [1, 2]; the profile README shows when the repository named after the user
  is public with a non-empty root `README.md` [3]; relative paths resolve "based on whatever branch you're currently
  on", which is why the branch view is a usable pre-merge check [4].
- **Profile README conventions.** The curated list's categories and tools [14] are the vocabulary a stranger
  brings; MF8 names what the page rejects from it.

## 6. Score

**6 / 10.** The product is what he asked for, by 9 Oct 11:37 and 20:50. The PRD describes it well enough to build
and to judge, and its facts check. It loses a point for the merge it does not describe and the three rules that
cannot all hold on the day (MF1); a point for resting its one decision on renders a reader cannot open (MF2); a
point for the contradictions a careful reader trips on (MF3, MF5, MF7) and for the blocking state it set for itself
and then ignored (MF6); and a point for the owners who cannot act (MF4). Each fix is a new item, a sentence, a
committed directory or a deletion; none adds a section.

## Sources

Outside sources (read with WebFetch unless marked otherwise):

1. GitHub Docs, *Events that trigger workflows*, "workflow_dispatch",
   https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows
   — "This event will only trigger a workflow run if the workflow file exists on the default branch"; "Once a
   workflow has run at least once, you can dispatch it against any branch or tag via the GitHub API or GitHub CLI";
   inputs arrive in `github.event.inputs`.
2. GitHub Docs, *Manually running a workflow*,
   https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow — "To trigger the
   `workflow_dispatch` event, your workflow must be in the default branch"; "Select the Branch dropdown menu and
   click a branch to run the workflow on"; "To run a workflow on a branch other than the repository's default branch,
   use the `--ref` flag".
3. GitHub Docs, *Managing your profile README*,
   https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
   — the four conditions (repository named after the user, public, root `README.md`, any content); the generated
   file "is pre-populated with a template to give you some inspiration"; removed when the file is emptied, the
   repository made private, or the names stop matching.
4. GitHub Docs, *About READMEs*,
   https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
   — "GitHub will automatically transform your relative link or image path based on whatever branch you're
   currently on"; the README is surfaced from `.github`, the root or `docs`.
5. Martin Cagan, *How To Write a Good PRD* (SVPG, 2005), https://www.svpg.com/assets/Files/goodprd.pdf — text
   extracted locally from the fetched PDF: "The release criteria are often just hand-waved, but a good PRD puts
   considerable thought into what the true minimum requirements are" (performance, scalability, reliability,
   usability, supportability, localizability); Schedule: "describe the context and motivation for the timeframe";
   "The product manager should have an extremely high bar for anything flagged as 'must-have'. This literally means
   that the product should not ship if even one of the 'must-have' features is not ready"; Step 9 "Can an engineer
   get enough understanding of the target… Can the QA team get enough information to design a test plan"; Step 10
   "If it's not in the PRD, put it in the PRD… record these decisions in the PRD"; "the PRD is a living document".
6. Joel Spolsky, *Painless Functional Specifications, Part 2: What's a Spec?*,
   https://www.joelonsoftware.com/2000/10/03/painless-functional-specifications-part-2-whats-a-spec/ — "You have to
   start culling features right away, and the best way to do this is with a 'nongoals' section of the spec"; "It's
   OK for the first version of the spec to leave open issues… By the time the programmers start work, all of these
   need to be stomped out"; "Specs Need To Stay Alive… The spec always reflects our best collective understanding of
   how the product is going to work".
7. Malte Ubl, *Design Docs at Google*, https://www.industrialempathy.com/posts/design-docs-at-google/ — non-goals
   are "things that could reasonably be goals, but are explicitly chosen not to be goals"; "Alternatives considered"
   is "one of the most important" sections, about each option's trade-offs; "around 10–20ish pages" for a larger
   project; the lifecycle (creation, review in rounds, implementation "definitely update the doc", maintenance).
8. Scrum.org, *The Scrum Guide*, https://scrumguides.org/scrum-guide.html — "The Definition of Done is a formal
   description of the state of the Increment when it meets the quality measures required"; "If a Product Backlog
   item does not meet the Definition of Done, it cannot be released or even presented at the Sprint Review"; a team
   without an organisational standard "must create a Definition of Done appropriate for the product".
9. Michael Nygard, *Documenting Architecture Decisions*,
   https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions — Title, Context, Decision, Status
   ("proposed", "accepted", "deprecated", "superseded"), Consequences; "The whole document should be one or two
   pages long"; "Large documents are never kept up to date"; a reversed decision is kept "but mark[ed] as superseded".
10. Atlassian, *Product requirements template* (Confluence),
    https://www.atlassian.com/software/confluence/templates/product-requirements — the top table: "What's your target
    release date? What's the current status? Who is on the core team?"; Objective, Success metrics, Assumptions,
    Options, supporting documentation, a table for open questions; "list what's out of scope for this feature or
    release".
11. Koji, *Working Backwards: How to Write an Amazon PR/FAQ*, https://www.koji.so/docs/working-backwards-pr-faq-guide
    — "A one-page mock press release written from a future date"; the whole document "typically around six pages";
    the internal FAQ's "hard business and technical questions" ("What are the biggest risks?", "What do we need to
    believe for this to work?"); "The FAQ is where the rigor lives"; "Killing ideas is a feature, not a bug".
12. Modern Requirements, *ISO/IEC/IEEE 29148 requirement characteristics*, https://www.modernrequirements.com/?p=32595
    — individual: verifiable (no subjective wording), unambiguous, singular ("exactly one action or capability"),
    complete, feasible; the set: complete, consistent ("none of the requirements contradict each other and… the
    terminologies are consistent"), feasible.
13. Basecamp, *Shape Up*, chapter 6 "Write the Pitch", https://basecamp.com/shapeup/1.5-chapter-06 — the five
    ingredients (Problem, Appetite, Solution, Rabbit holes, No-gos); "No-gos: anything specifically excluded from the
    concept: functionality or use cases we intentionally aren't covering"; "spelling it out patches a potential
    rabbit hole".
14. abhisheknaiidu, *awesome-github-profile-readme*, https://github.com/abhisheknaiidu/awesome-github-profile-readme
    — "A curated list of awesome Github Profile READMEs"; 16 categories (GitHub Actions, Game Mode, Code Mode,
    Dynamic Realtime, A Little Bit of Everything, Descriptive, Simple but Innovative Ones, Typing.. Mode, Anime,
    Minimalistic, GIFS, Just Images, Badges, Fancy Fonts, Icons, Retro); tools listed: GitHub Readme Stats, Streak
    Stats, Profile Trophy, Shields, Visitor Badge and counters.
15. WebSearch, "Amazon working backwards PR/FAQ 'five pages'": reader's notes on Bryar and Carr, *Working Backwards*
    (https://www.goodreads.com/notes/55297149-working-backwards/50759819-thomas-hefke?page=2): the press release
    "always less than one page", the FAQ "five pages or less"; the a16z and Product Mastery Now summaries agree on
    the one-page press release (search-level; the book itself not read).

Files in this repository (all under `/home/user/wt-v12/`) and the renders:

16. `docs/PRD.md` (831 lines, 17,288 words at `92b1bef`; per-section word counts by a Python loop over `## `
    headings); `docs/crit/prd/LOG.md`; `docs/crit/prd/owner-messages.md` (21 messages); `docs/crit/prd/review-r03-2.md`
    (my round-3 review; its source 2 is cited above as "round-3 source 2", not re-read).
17. `.github/workflows/profile.yml`: lines 13–27 (schedule, `dry_run`, `push: paths`), 67–74 (job `chart`, checkout
    with no `ref`), 143–153 (publish, dry run, the commit step's `if`), 150–186 (`git push origin HEAD:main`);
    `git show main:.github/workflows/profile.yml` lines 9–16 (same name and `dry_run` input on `main`).
18. `git show main:README.md | grep -o 'chart/assets/v9/[a-z0-9-]*\.svg' | sort -u` (eight paths, four shared with
    the branch, four `still`); `README.md` on the branch (six paths, lines 7–13).
19. `scripts/publish_chart.py` lines 1–14 (docstring: one orphan commit, force-pushed, only what the report names)
    and 81–93 (`unshipped`); `scripts/render.mjs` lines 1–25 (`phone` mode; `matrix` "placeholder… needs the README
    preview page").
20. `git ls-files | grep -c '\.png$'` → 0; `.gitignore` (`out/`, `assets/v9/`, `social/`); the session's
    `scratchpad/prd-r02/once-1a/` and `scratchpad/prd-r03/once-2b/` listings (renders, fixtures, `preview.mjs`,
    `preview_phone.mjs`, `preview_mid.mjs`).
21. `ls tests/` (24 files, no `test_prd.py`); `ls scripts/checks/*.py` (28 plug-ins and `__init__.py`).
22. `scripts/render_readme.py` 455–462 (`agent_clause(r)` unconditional) and 670–671; `scripts/checks/position.py`
    28–36; `scripts/checks/column.py` 44–51; `chart.toml` 24–40, 665–669, 1003–1031; `tests/test_route.py` 829, 894,
    1052; `docs/BEN-TODO.md` (what he is asked to edit: `chart.toml`, `render_readme.py`; no log file).
23. `git log --oneline -3` (`92b1bef`, `107a988`, `e17cc80`); `git diff --stat 027f081..HEAD -- . ':!docs'` (empty,
    as the PRD's line 7 states).
24. Renders, `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/`:
    `sheet-phone-day-390.png`, `page-phone-1.png`, `page-desk-1.png`.
