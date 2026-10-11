# PRD review round 2, reviewer 2: A product manager who has shipped from PRDs and rejects the vague ones

11 Oct 2026. Branch `v12/purpose`, worktree `/home/user/wt-v12`, HEAD `e17cc80` (the round-1 fix commit). I read
`docs/PRD.md` (691 lines; 530 at the round-1 commit `9e3db34`) end to end, every message in
`docs/crit/prd/owner-messages.md`, `docs/crit/prd/LOG.md` (so nothing below repeats a round-1 fix), my own round-1
review and the other two, `README.md`, `docs/crit/round6/SPEC.md` §0, `.github/workflows/profile.yml` in full,
`scripts/publish_chart.py` (docstring), `scripts/build_stats.py` (modes), `scripts/build_assets.py` (arguments),
`scripts/checks/column.py`, `expiry.py`, `readme.py`, `scripts/render_readme.py` (`agent_clause`, `LIST_MAX_*`),
`chart.toml` (`[copy]`, `[facts]`, the `crawl_delay_obeyed` comments), `tests/test_route.py:812–829`,
`tests/test_round13.py:258`, `tests/test_round7.py:91, 370`, `tests/test_pipeline.py:307`, `assets/stats.json`
(the run-check record: 7 gates, 18 probes, 22 repositories) and `docs/BEN-TODO.md:39`. I ran `python3 -m unittest`
(539 tests, OK, 22.1 s; `test_supporting` 24, `test_timeline` 26, `test_approaches` 19). I read the round-16
`gate.txt` (0 fail, 4 warn, exit 2) and looked at `sheet-phone-day-390.png`, `sheet-desk-day-870.png`,
`sheet-mid-day-746.png`, `page-desk-1.png`, `page-desk-2.png`, `page-phone-1.png`, `page-phone-2.png`,
`page-phone-3.png`. Through the REST API I read the live README on `main`, `main`'s last five commits, PR #17, and
the twelve runs of `profile.yml` with the failing step of run 12. I read 15 outside sources (Sources, at the end).

My brief is the document as a PRD: could a builder who was not in the room build and accept this product from it
alone, and could the owner accept or reject the result from it.

## 1. Is the product this PRD defines what he wants?

**Yes.** The sentence that decides it is 9 Oct 11:37: *"It has to be helpful knowledge. If you were a fucking real
sailor, if you were a real person, you'd want it to be helpful data that you're looking at. You're going through,
you're like, oh, it's very helpful, and it's in a cool format."* §1 and §5.1 define exactly that: one image that is
the way into his main tool (install, what happens to a URL in order, the two catches, the one key, the file, who
reads it next) and a page of lookup material under it. I checked the renders against §5.1 again this round: the
phone sheet at 390 px carries T1, T2, R0, R2, S1, F1, H0, H1, C1, R13 and R15 and nothing else; the desk sheet at
870 px the same rows on fewer lines; nothing on either has a size. His second deciding sentence, 9 Oct 20:50,
*"Everything, single thing inside of this needs a purpose, not a fucking chasing a reason"*, is §5.1's table, and
`test_every_element_has_a_purpose` (`tests/test_route.py:812`) holds the drawing to it.

One sentence of his cuts the other way, and it is about the default, not the product: 9 Oct 11:35, *"We don't need
to show the commits... it feels lazy."* What is live on `main` today (REST `readme`, line 13 alt text) is *"Ben
Russell's 22 repositories by week, Sep 2025 to Oct 2026: Scrapy and rustmapper busiest, quiet Feb to Apr 2026"*,
with *"last commit 8 Aug 2026"* on a facts line and *"my commits... regenerated weekly"* in the footer. §9.1's
"default while undecided" keeps that page up. The PRD defines the page he wants; its default leaves the page he
said he did not want on his profile for as long as he does not decide (MF2).

## 2. Verdict on the document

**7 / 10 as a PRD**, up from 6. Round 1 fixed the things that made it undecidable: "done" is defined (§8.3), the
judged questions have lines a reviewer ticks, §9.1 has options with what the first screen says under each, §6.1 and
§8.5 exist, the yardstick is counted right. §5.1 and §5.4 remain the best parts: a builder can draw the image from
§5.1 and predict what a release does to it from §5.4, and I re-verified the counts that back them (28 plug-ins, 539
tests, 7 + 18 run-check steps, 22 repositories so "15 more" holds, the four warnings in `gate.txt` equal §8.2 plus
POSITION-EMPTY).

What still fails it, in order: §6.1's rollback row describes a path the workflow does not have, and the one live
fact about the pipeline this week (run 12 failed) is not in the document; §9.1's default has a cost the table does
not print, and it is the cost his own sentence names; "a fresh build" in §8.1 is two different things and the PRD's
own baseline drifts with no status header; §10 has become a review log inside the requirements, with no owner or
blocking state on half its items; the mid-window trade is a decision filed under "not yet verified", said in five
places, with no recommendation. None of these needs a new section. Three need one table row each.

## 3. Must-fixes, ranked

### MF1. §6.1's rollback path does not exist, and the pipeline's one live failure is missing (product and PRD)

- **Where:** §6.1, line 246 (the third row): *"Ben, or a session, `git revert`s the bot commit on `main`; a
  `workflow_dispatch` with `dry_run: false` rebuilds the sheets from the reverted `stats.json`."* Also §0 line 21
  ("Built") and §6 lines 220–227.
- **What I checked:** `profile.yml` has one `chart` job for every trigger, and its step `Take the day's soundings`
  runs `python3 scripts/build_stats.py --runcheck runcheck/runcheck.json` (lines 95–99) before anything is drawn.
  `build_stats.py` (docstring lines 4–6) has modes `live`, `cache` and `cache-failed`, and in CI it runs live with
  `GITHUB_TOKEN`. So a `workflow_dispatch` never rebuilds "from the reverted `stats.json`": it re-surveys and
  overwrites `stats.json`, and if the wrong figure came from the data it comes back. Worse, the revert itself
  triggers that: the bot commit stages `assets/log.json` (workflow lines 148–152) and `push: paths` lists
  `assets/log.json` (line 24), so `git revert` of the bot commit is a push that starts a fresh survey. The only path
  that redraws from a chosen `stats.json` is local: `build_assets.py` reads `assets/stats.json` directly
  (`DEFAULT_STATS`, line 55), then `render_readme.py`, `check.py --tier fast,render`, `publish_chart.py`, by someone
  with push rights. And the facts: the workflow has run 12 times on `main` (8–11 Oct); it committed once
  (`d253286`, `chart: soundings 2026-10-09`, by `github-actions[bot]`); run 12, the only scheduled run, failed today
  at the step `Unit tests` on `main`'s v11 code (`FAILED (failures=2)`:
  `test_hero.HeroBuild.test_alt_is_short_plain_and_agrees_with_chart_toml`,
  `test_pipeline.Readme.test_blocks_and_inline_are_idempotent`). The PRD says nothing about either.
- **What to change:** Replace the third row with:
  > | a build passes the gates and prints something wrong | the new page | **No CI path rebuilds from an older `stats.json`**: every trigger re-surveys (`build_stats.py` live), and reverting the bot commit is itself a push that re-surveys (`assets/log.json` is in `push: paths`). To roll back: (1) a session or Ben, locally, checks out the last good `assets/stats.json`, runs `build_assets.py`, `render_readme.py`, `check.py --tier fast,render`, `publish_chart.py`, commits `stats.json` + `README.md` + `DESIGN.md` to `main`; (2) if the fault is in code or `chart.toml`, revert that commit first or the next weekly run reprints it. The `chart` branch has no history (`publish_chart.py` docstring), so there is no older sheet to point at. |
  And add to §0 "Built": *"The weekly job has run 12 times on `main` since 8 Oct and committed once (9 Oct). Run
  12 (11 Oct, scheduled) failed at `Unit tests` on `main`'s v11 code; the live page is run 11's."* Add the same to
  §8.5's first bullet as its first instance: who noticed it (this review), who fixes it (a session; the failing
  tests are on `main`, not this branch).
- **Why:** Cagan: release criteria "are often just hand-waved, but a good PRD puts considerable thought into what
  the true minimum requirements are", reliability and supportability among them [1]; the PRD's own §7.3 rule is
  that nothing it says about the pipeline is untrue. A rollback a builder would try and find missing is the worst
  kind of requirement.
- **About:** the product (no rollback path exists in CI; the weekly run is red) and the PRD text.

### MF2. §9.1's default has a cost the table does not print, and his sentence names it (PRD, and the decision)

- **Where:** §9.1, line 448: *"Default while undecided: the branch stays unmerged; `main` and the live page do not
  change."* The option table, lines 440–446, has no row for the default.
- **What I checked:** the live README (REST `readme`, `main` at `d253286`): the image is the v11 sheet, alt *"22
  repositories by week... Scrapy and rustmapper busiest, quiet Feb to Apr 2026"*; both facts lines print *"last
  commit <date>"*; the footer is first person (*"my commits on their default branches... 3 % of my commits carry an
  AI co-author trailer"*) and ends *"regenerated weekly"*. Against the PRD: an activity drawing (G8, 9 Oct 11:35
  *"We don't need to show the commits... it feels lazy"*; §4 "No... activity graphs"), shapes sized by data (G15),
  "last commit" (§7.3 "No commit totals, no 'last commit'"), first person (§7.5, G13), a schedule in the provenance
  (§7.5). Four of the rules this PRD holds with gates are broken on the page that stays up by default, and its
  weekly job failed today (MF1).
- **What to change:** Add a first row to the table:
  > | **0. Leave `main` as it is** (today's default) | "22 repositories by week... busiest... quiet Feb to Apr 2026"; "last commit 8 Aug 2026"; "my commits"; "regenerated weekly" | the v11 page: an activity sheet, first person, a schedule line | every week undecided keeps up a page that breaks G8, G13, G15, §7.3 and §7.5; its job failed on 11 Oct | nothing; the next scheduled run re-fails |
  Then make the recommendation two-step, because the pipeline makes it one: *"Merge 2b now (two first-minute
  cautions on the open list, the rest folded; no Rust-sitemap work), then 1a/1b in Rust-sitemap. Every §5.4 row
  that a release fixes retires on the next weekly run or on `release-published` without a further merge, so
  merging first costs nothing that 1a/1b would not undo by itself."* State that 0 → 2b is reversible (`git
  revert` of the merge; §6.1) so it is a decision that can be made with what is known today. Keep "decide by:
  before the merge" only for 1a vs 1b.
- **Why:** His words set the cost: the default keeps commits on his profile. Bezos: "most decisions should probably
  be made with somewhere around 70% of the information you wish you had... Many decisions are reversible, two-way
  doors. Those decisions can use a light-weight process" [8]; Shape Up: "Instead of comparing up against the ideal,
  compare down to baseline" [4], and the baseline here is the v11 page. Cagan: "If someone decides to cut a
  requirement, it can be difficult to understand the full impact of this cut. The mapping from requirements to
  objectives helps make this clear" [1]; the same for not deciding.
- **About:** the PRD (the decision table), and it sets the product's next step.

### MF3. "A fresh build" is two things, and the document has no status header (PRD)

- **Where:** §8.1 item 2, line 357: *"`check.py --tier fast,render` on a fresh build"*; line 3: *"Branch
  `v12/purpose` at `027f081` plus this document"* (HEAD is `e17cc80`, two commits on); §0 line 23–26 (scores that
  "go stale the day the next round runs").
- **What I checked:** a "fresh build" from the committed `assets/stats.json` is `build_assets.py` →
  `render_readme.py` → `check.py` and needs no network; a fresh *survey* is `build_stats.py` live, which needs
  `GITHUB_TOKEN`, the clones, PyPI and a `runcheck.json` from a macOS run (workflow lines 48–66). The two give
  different `stats.json` files and can give different wordings (§11 says so for macOS). §8.1 does not say which; a
  builder in a clean checkout cannot tell whether item 2 passes with the file in git or only after a survey they
  cannot run without the owner's token.
- **What to change:** Item 2: *"from the committed `assets/stats.json`: `python3 scripts/build_assets.py && python3
  scripts/render_readme.py --check && python3 scripts/check.py --tier fast,render`; 0 fail, 0 error, warnings only
  from §8.2. A fresh survey is item 4's job, not this item."* Replace lines 3–4 with a four-line header: *Status*
  (draft, blocked on §9.1), *Owner of the decision* (Ben), *Owner of the text* (the session; edited only in a PRD
  review round or when the product changes), *Baseline* (the commit the figures were read at; today `e17cc80`),
  *Last updated* (date, round). Keep §0's scores but under "as of the baseline above".
- **Why:** Spolsky: "Your specs should be owned and written by one person", with a disclaimer that says whether
  the spec is complete [2]; Aha!'s template carries a status field and warns a PRD "becomes outdated quickly if
  teams do not actively maintain it" [6]; Cagan: "the PRD is a living document, and you should track all features
  in the PRD through product launch" [1]. INCOSE C3/C7: a statement that can be read two ways is not verifiable [9].
- **About:** the PRD.

### MF4. §10 is a review log inside the requirements: no owner, no blocking state on items 10–16 (PRD)

- **Where:** §10, lines 487–553. Line 490–491: *"None of 1–8 blocks the merge; 9 blocks option 1b."* Nothing is
  said of 10–16, and no item names who does it.
- **What I checked:** §10 grew from 7 items to 16 in one round and each is a paragraph; items 5, 8, 9, 10, 11 and
  13 are product changes that round 1 declined as "this pass edits only the PRD" (`LOG.md`), so they are open work
  with no home but this list. Item 12 (`tests/test_prd.py`) would make most of §7 and appendix B self-checking,
  which is what my round-1 MF9 and reviewer 3's MF8 both asked for; it has no owner either.
- **What to change:** Make §10 a table with six columns: id, gap (one line), fix (one line, the file), blocks
  (merge / option 1b / nothing), owner (Ben / a session), status (open / done, with the round). Today's values I
  can set from the text: blocks merge: none; blocks 1b: 9; nothing: the rest. Owner Ben: 4 (the device), 8 (he is
  told to edit `chart.toml`), 10 (`BEN-TODO.md`); a session: the others. Move each item's reasoning to the
  reviewer's review it cites. When an item closes, move it to `docs/crit/prd/LOG.md`; §10 lists open gaps only.
  One rule at the top: *"A §10 item that blocks the merge is also a line in §8.1."*
- **Why:** Spolsky on open issues: "It's OK for the first version of the spec to leave open issues... By the time
  the programmers start work, all of these need to be stomped out" [2]; Nygard's decision records carry a status
  and are superseded, not rewritten [3]; the Scrum Guide's Definition of Done is a shared list of what finished
  means, and work that does not meet it "cannot be released" [5]. A gap list that does not say whether it blocks is
  neither.
- **About:** the PRD.

### MF5. The mid-window trade is a decision filed under "not yet verified", stated in five places, with no recommendation (PRD)

- **Where:** §9.3 bullet 3, lines 479–481; also §5.2 line 150, §7.4 line 309, §10.14 lines 546–547, §11 lines
  564–566.
- **What I checked:** `column.py`: `MIN_PX = 11.0` (line 45) is the mid floor; `TALL_FROM = 768`; `column_px()` gives
  482 px at 852 and 765 at 1,199 (lines 56–63). The 11.2 px at 852 is right. The three options the PRD names (accept
  in writing; a second breakpoint at 931; a narrower mid sheet) have no cost column, no recommendation and no
  default, which is the shape §9.1 was given in round 1 for a reason.
- **What to change:** Move the trade to §9 as **§9.1b** (or a second table under §9.1) in the same five columns:
  > | a. Accept 11.2–13 px at 852–930 in writing (**recommended**) | as today | nothing | zero; no device he named sits there (a 1,024 px iPad sideways gets 13.7 px); written in §11 | nothing |
  > | b. Serve the phone sheet to 930 (`breakpoint_px` 931 in `chart.toml:9`) | the phone sheet in a 482–560 px column, 26-unit text ≈ 21–24 px | the mid edition starts at 931 | one number; six `<source>` lines regenerate; HERO-COLUMN-PX must still hold ≤ 900 px at 852–930, which needs checking (the phone sheet is 1.87 × the column: 901 px at 482) | a build |
  > | c. A narrower mid sheet | smaller type everywhere on the mid | — | a redesign of one edition | a build and a round |
  Default: a. Decides: Ben (9 Oct 11:32, *"accepting of all different formats"*). Then §5.2, §7.4, §10.14 and §11
  each become one pointer to it.
- **Why:** My round-1 MF6 (applied) was one home per requirement; this one was added by round 1 in five homes.
  Cagan's "unambiguous" and Spolsky's "open issues" [1, 2]; INCOSE C5 (singular) and the set characteristic that a
  requirement appears once [9].
- **About:** the PRD.

### MF6. A "default" that the merge commit does not implement is not a default (product and PRD)

- **Where:** §9.2 bullet 2, lines 461–468: *"strike (his words; the default from PRD round 1)... Until the switch
  exists the page prints the counts, and G8 is marked open"*; §8.1 (no item for it); §8.3 "Done".
- **What I checked:** `render_readme.py:459` still calls `agent_clause(r)` unconditionally; `chart.toml [facts]`
  (line 667) has `built_on.*` only, no switch; the committed `README.md` prints *"authored 45 of its 146 commits
  and co-signed 1 of his own 101"* and *"71 of its 499... 30 of his own 420"*. §8.3's "Done" is §8.1 + §8.4 + §9.1 +
  three yeses on q.1–4, and q.1–4 do not ask about G8. So a page can be "Done" by this PRD while printing what his
  sentence bans and what the PRD says is off by default. Round 1 ruled the default (applied, r1 MF4 / r2 MF5) and
  declined the implementation as product work; the gap this round is that the ruling has no acceptance hook.
- **What to change:** Add §8.1 item 7: *"`[facts] agent_clause` exists in `chart.toml`, defaults to `false`, and
  the facts lines carry no commit counts on the merge commit, unless Ben has written 'keep' or 'share' against §9.2
  in `LOG.md`."* Mark §10.5 "blocks the merge" (MF4's column). Until then §9.2 should say *"default: strike; not yet
  implemented; blocks the merge"* rather than "the default from PRD round 1".
- **Why:** His sentence, 9 Oct 11:35. Scrum Guide: a Definition of Done exists so that "everyone [has] a shared
  understanding" of what finished means [5]; Cagan's must-have "literally means that the product should not ship
  if even one of the must-have features is not ready" [1].
- **About:** the product (one switch, one test) and the PRD (§8.1).

### MF7. §8.4 has no owner and names a log that exists twice; §8.3 has two end states (PRD)

- **Where:** §8.4, line 409: *"Pass conditions, logged in `LOG.md`"*; §8.3 lines 396–397 and 402–405.
- **What I checked:** there are two `LOG.md` files (`docs/crit/round6/LOG.md`, 1,100+ lines, and
  `docs/crit/prd/LOG.md`); neither has a device entry (grep for iPhone/Safari in `round6/LOG.md` finds only a
  round-12 note on 320 px). §10.4 says "by him or on a device the session can reach"; this session has no device, so
  the owner is Ben and the PRD does not say so. §8.3 says "Done = ..." and two lines earlier "Only Ben's own 'ship
  it' closes the product"; a reader cannot tell whether his ship-it is part of Done or after it. "No must-fix left
  open" does not say whether a PRD-review must-fix (this document's) counts.
- **What to change:** §8.4 first line: *"Owner: Ben (the session has no device). Log the result in
  `docs/crit/round6/LOG.md` under the round that merges, with the screenshots' paths."* §8.3: *"Done = [the four
  conditions]. Done means ready for Ben to merge; his merge is the acceptance (§7.6: he merges PRs). 'Must-fix'
  here means a product-review must-fix (`review-rNN-*.md`); PRD-review must-fixes are §10's."*
- **Why:** The Scrum Guide separates the Definition of Done from the act of release [5]; Spolsky: one owner per
  decision [2]; a pass condition without an assignee is a wish.
- **About:** the PRD.

### MF8. §11 misses the stale-image window every weekly run opens (PRD; one product option)

- **Where:** §11, lines 555–575; §8.5 lines 420–429; §7.4 row "editions on the `chart` branch before README.md
  names them" (line 318).
- **What I checked:** the `<picture>` sources point at `raw.githubusercontent.com/.../chart/assets/v9/hero-*.svg`
  (`README.md` lines 7–13); GitHub serves Markdown images through Camo and tells authors whose images do not update
  to check `Cache-Control` and, as a last resort, `curl -X PURGE` the Camo URL [10]. GitHub staff in the community
  thread on stale raw files: "The cache is set for 5 minutes", with users reporting hours in some regions [11]; an
  independent project found raw.githubusercontent.com "hardwired behind an HTTP varnish cache that does not allow
  updates more frequently than every 300 seconds" [12]. `publish_chart.py` force-pushes the new sheets to the same
  paths. So after every weekly run a visitor can see the new README with last week's sheet for minutes, sometimes
  longer. Round 15's rule (sheets before README) covers a *missing* sheet, not a *stale* one. The week a §5.4 row
  retires, the page's cautions list would drop H1's comment while the image still shows the box.
- **What to change:** A §11 bullet: *"After each run the sheet and the text can disagree for minutes to hours:
  raw.githubusercontent.com caches 300 s and Camo caches on top; the same paths are force-pushed. Accepted: both
  states are true of the release. If it must be shorter, `publish_chart.py` can name the sheets by the run
  (`hero-day-<date>.svg`) so the README's new URLs miss the cache; cost: one line in `publish_chart.py`, one in
  `render_readme.py`, and HERO-FALLBACK's path check."* And in §8.5: who purges if a sheet stays stale past a day
  (Ben; the Camo URL is in the page source).
- **Why:** Cagan's release criteria, supportability [1]; ProductPlan's rule from round 1, "if it isn't included in
  the PRD, it won't be included in the release"; the owner's own 8 Oct 11:13 ("Merged but all images are
  unavailable") is the same class of surprise.
- **About:** the PRD text; the product only if he wants the window closed.

### MF9. Loose ends (PRD)

- §0 line 23: "PRD review round 1 (11 Oct): 7/6/6" will be "round 2" tomorrow; with MF3's header the scores can
  go, and §0 keeps the reading order and the blocker.
- §6 line 221: "Sunday 06:20 UTC" is the cron; GitHub ran it at 12:52 UTC today (run 12). Say "scheduled for";
  a builder timing the first live run should not wait for 06:20.
- §5.3 row 6 and §7.4 row "Cautions: ≤ 7 items, ≤ 25 words" are held by `render_readme.py:670–671`
  (`LIST_MAX_ITEMS = 7`, `LIST_MAX_WORDS = 25`) and read by `checks/readme.py:318`; name the constants once so 2b's
  "README-CAUTIONS' open-list limit" (§9.1) points at a number.
- §9.2 bullets 3–5 (the printed name, the worker figure, Scrapy's filter) are still to-dos without options; my
  round-1 smaller note stands: an options row each, or move them to `docs/BEN-TODO.md` and link once.
- Line 10 names "the clone of `Rust-sitemap` at `32c2651`" as a source with no path; `build_stats.py` makes the
  clones and a builder cannot find the one the PRD read. Give the path, or say "a clone at that commit".

## 4. What holds, so nobody rewrites it

- §5.1 is still the spec a builder draws from; §5.4's "At HEAD" and "Needs here" columns are the right way to say
  what a release does, and the round-1 resolver runs behind them are recorded in `LOG.md`.
- §6.1 rows 1 and 2 are right (I read the `Pencil-note edition` step and the gate's exit handling, workflow lines
  120–127 and 177–189).
- §8.1 items 1, 3, 5 and 6 are mechanical and I could run or read each; §8.2 equals `gate.txt`.
- §8.3 q.1–4 now have tickable lines; q.5 and q.6 are marked advisory. Right call.
- Every count I re-checked holds: 28 plug-ins (`ls scripts/checks/*.py` is 29 with `__init__.py`), 539 tests and
  the 69 off-page ones, 7 gates and 18 probes in `stats.json`, 22 repositories, six `<source>`s, `[copy]` without
  `thesis`, `BEN-TODO.md:39` still carrying the bio line (§10.10 is right to keep it open), PR #17 open and
  mergeable (REST), `CODE_COLUMNS = 32`, `TALL_FROM = 768`, `MIN_PX = 11.0`, `DESK_MIN_PX = 14.5`.
- The non-goals (§4) are real non-goals and nothing in this round's renders breaks one.

## 5. Research notes my lens needed

- **PRDs and done.** Cagan's completeness test ("Can the QA team get enough information to design a test plan?")
  passes for §5 and §8.1 and fails for §6.1 (MF1) [1]. The Scrum Guide's Definition of Done is a checklist with one
  consequence, "cannot be released", and that is the shape §8.3 now has; MF7 only asks it to say who releases [5].
  Shape Up's "compare down to baseline" is the test §9.1 fails: the baseline is the v11 page, and the table never
  looks at it [4].
- **Decisions.** Nygard's records have a status and are superseded rather than edited [3]; Bezos's letter is the
  argument for deciding §9.1 as a two-way door [8]. Figma's template puts a launch-readiness checklist with named
  sign-offs at the end of the PRD, which is what §8.1 + §8.4 are once each line has an owner [7].
- **Document hygiene.** Spolsky: one author, a disclaimer of completeness, open issues killed before build [2]; his
  tip against templates is why I ask for a four-line header and not a cover page [13]. Aha!: status, and "evolve
  alongside development" [6]. INCOSE's characteristics (C3 unambiguous, C5 singular, C7 verifiable) are the grounds
  for MF3 and MF5 [9].
- **GitHub profile READMEs.** GitHub's docs set only the four conditions for a profile README to show [14]; the
  2026 recruiter-side guide says the first minute must give the target role and "an obvious way to contact this
  person", and that the README should be "a useful index, not a sticker board" [15]. The page meets the index test;
  the contact test is §8.1 item 6, already blocking. The image-cache behaviour (MF8) is GitHub's own documentation
  plus two independent reports [10, 11, 12].

## 6. Score

**7 / 10.** The product is what he asked for, by 9 Oct 11:37 and 20:50. The PRD is now decidable where round 1
was not, and traceable throughout. It loses a point for a rollback path that does not exist and a red weekly run it
does not know about (MF1), a point for a default whose cost is his own sentence (MF2), and a point for the
housekeeping that lets a document grow 30 % a round without anyone owning its open items (MF3–MF5). MF6–MF9 are a
table row or a line each.

## Sources

Outside sources (read with WebFetch unless marked "via search summary"):

1. Martin Cagan, *How To Write a Good PRD* (SVPG, 2005), https://www.svpg.com/assets/Files/goodprd.pdf — text
   extracted locally from the PDF: "Release Criteria... are often just hand-waved, but a good PRD puts considerable
   thought into what the true minimum requirements are" (performance, scalability, reliability, usability,
   supportability, localizability); Step 9 "Test Completeness" ("Can the QA team get enough information to design a
   test plan"); Step 10 "the PRD is a living document, and you should track all features in the PRD through product
   launch"; traceability ("the mapping from requirements to objectives helps make this clear").
2. Joel Spolsky, *Painless Functional Specifications, Part 2: What's a Spec?*,
   https://www.joelonsoftware.com/2000/10/03/painless-functional-specifications-part-2-whats-a-spec/ — disclaimer,
   one author ("Your specs should be owned and written by one person"), nongoals, open issues ("By the time the
   programmers start work, all of these need to be stomped out").
3. Michael Nygard, *Documenting Architecture Decisions*,
   https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions — title, context, decision, status
   (proposed / accepted / deprecated / superseded), consequences; "If a decision is reversed, we will keep the old one
   around, but mark it as superseded."
4. Basecamp, *Shape Up*, ch. 14 "Decide When to Stop", https://basecamp.com/shapeup/3.5-chapter-14 — "Instead of
   comparing up against the ideal, compare down to baseline"; scope hammering; QA as "a level-up, not a gate".
5. Scrum.org, *The Scrum Guide*, https://scrumguides.org/scrum-guide.html — the Definition of Done "creates
   transparency by providing everyone a shared understanding"; work that does not meet it "cannot be released or
   even presented at the Sprint Review".
6. Aha!, *What is a good product requirements document template?*,
   https://www.aha.io/roadmapping/guide/requirements-management/what-is-a-good-product-requirements-document-template
   — sections (objective, assumptions, scope, requirements, open questions), a status field ("on track" / "at
   risk"), "product managers typically own the document", PRDs become "outdated quickly if teams do not actively
   maintain it" and should "evolve alongside development".
7. Yuhki Yamashita, *Figma's approach to product requirement docs*,
   https://docs.superhuman.com/@yuhki/figmas-approach-to-product-requirement-docs — problem alignment, solution
   alignment, launch readiness as a checklist with named sign-offs; the doc as "single source of truth" whose status
   is pulled, not retyped.
8. Jeff Bezos, *2016 Letter to Shareholders*, https://www.aboutamazon.com/news/company-news/2016-letter-to-shareholders
   — "most decisions should probably be made with somewhere around 70% of the information you wish you had"; "Many
   decisions are reversible, two-way doors. Those decisions can use a light-weight process"; disagree and commit.
9. INCOSE Requirements Working Group, *Guide to Writing Requirements v4, summary sheet* (via search summary; the
   PDF returned 403),
   https://www.incose.org/docs/default-source/working-groups/requirements-wg/guidetowritingrequirements/incose_rwg_gtwr_v4_summary_sheet.pdf
   — C1 necessary, C3 unambiguous ("can be interpreted in only one way"), C5 singular, C7 verifiable; the 2018
   Boeing/INCOSE slides at https://www.incose.org/wp-content/uploads/legacy/presentation/IS2018-pdf/6-6-1.pdf.
10. GitHub Docs, *About anonymized URLs*,
    https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-anonymized-urls — Camo
    proxies Markdown images; check `Cache-Control`; `curl -X PURGE` on the Camo URL as a last resort ("Purging the
    cache forces every GitHub user to re-request the image").
11. GitHub Community discussion #46691, *Why does the raw file still show previous data?*,
    https://github.com/orgs/community/discussions/46691 — GitHub staff: "The cache is set for 5 minutes";
    `max-age=300` observed, 86400 on some repositories; users report delays from minutes to 24–48 h in some
    regions; commit-hash URLs as the workaround.
12. Fluid Project issue FLUID-6626, https://issues.fluidproject.org/browse/FLUID-6626/ — raw.githubusercontent.com
    is "hardwired behind an HTTP varnish cache that does not allow updates more frequently than every 300 seconds"
    and ignores client cache-control headers.
13. Joel Spolsky, *Painless Functional Specifications, Part 4: Tips*,
    https://www.joelonsoftware.com/2000/10/15/painless-functional-specifications-part-4-tips/ — write for humans,
    keep it simple, review and reread, "Avoid the temptation to make a standard template for specs"; the spec that
    "goes up on the shelf, never to be taken down again".
14. GitHub Docs, *Managing your profile README*,
    https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
    — the four conditions (repository named after the user, public, `README.md` at the root, any content); no
    stated limits on content.
15. GreatFrontEnd, *Frontend Developer GitHub Profile: How to Stand Out to Recruiters (2026)*,
    https://www.greatfrontend.com/blog/frontend-developer-github-profile — in the first minute "a recruiter should
    understand your target role"; the README "short enough to scan and specific enough to direct attention", "a
    useful index, not a sticker board"; pins chosen by what they prove; "an obvious way to contact this person".

Files in this repository (all under `/home/user/wt-v12/`) and the renders:

16. `docs/PRD.md` (691 lines at `e17cc80`; 530 at `9e3db34`), `docs/crit/prd/LOG.md`, `docs/crit/prd/owner-messages.md`
    (21 messages), `docs/crit/prd/review-r01-{1,2,3}.md`.
17. `.github/workflows/profile.yml` — lines 13–28 (triggers; `assets/log.json` in `push: paths`), 48–66 (the macOS
    run check), 95–99 (`build_stats.py` live on every trigger), 120–127 (gate exit codes), 148–165 (the bot commit's
    files), 177–189 (the pencil-note path).
18. `scripts/build_stats.py` lines 2–13, 34 (modes live / cache / cache-failed); `scripts/build_assets.py` lines 55,
    504–515 (`--stats`, `--no-sounding`); `scripts/publish_chart.py` lines 1–16 (one orphan commit, force-pushed).
19. `scripts/checks/column.py` lines 44–63 (`MIN_PX`, `TALL_FROM`, `TALL_PX`, `DESK_MIN_PX`, `column_px`);
    `scripts/checks/expiry.py` lines 30–45 (all three codes warn); `scripts/checks/readme.py` lines 28, 318
    (`CODE_COLUMNS`, the cautions limits); `scripts/render_readme.py` lines 459, 670–671, 925 (`agent_clause`,
    `LIST_MAX_ITEMS`, `LIST_MAX_WORDS`).
20. `chart.toml` lines 30–39 (`[copy]`, the five retired keys), 667–672 (`[facts]`, no switch), 1074–1082 and
    1150–1162 (`crawl_delay_obeyed` named, "not written yet").
21. `tests/test_route.py` lines 812–829; `tests/test_round13.py` line 258; `tests/test_round7.py` lines 91, 370;
    `tests/test_pipeline.py` line 307. `python3 -m unittest`: 539 OK in 22.1 s.
22. `assets/stats.json` — `runcheck.rustmapper.steps`: 25 (7 gates, 18 probes; `ends_by_itself`, `robots_read`,
    `kill_writes_file`, `resume_after_kill` failed), 22 `repos`. `docs/BEN-TODO.md:39`.
23. Live data via REST: `repos/BenjaminSRussell/BenjaminSRussell/readme` (the v11 page: alt text, "last commit",
    "my commits", "regenerated weekly"); `commits?sha=main` (`d253286` by `github-actions[bot]`, 9 Oct);
    `pulls/17` (open, mergeable, `v11.1/no-thesis`); `actions/workflows/profile.yml/runs` (12 runs; run 12 scheduled,
    11 Oct 12:52 UTC, failed at `Unit tests`: `test_alt_is_short_plain_and_agrees_with_chart_toml`,
    `test_blocks_and_inline_are_idempotent`).
24. Renders, `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/`:
    `sheet-phone-day-390.png`, `sheet-desk-day-870.png`, `sheet-mid-day-746.png`, `page-desk-1.png`,
    `page-desk-2.png`, `page-phone-1.png`, `page-phone-2.png`, `page-phone-3.png`, `gate.txt`.
