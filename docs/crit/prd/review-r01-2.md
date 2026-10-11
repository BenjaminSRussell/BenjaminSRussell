# PRD review round 1, reviewer 2: A product manager who has shipped from PRDs and rejects the vague ones

11 Oct 2026. I read `docs/PRD.md` (531 lines) against every message in `docs/crit/prd/owner-messages.md`, then
`README.md`, `docs/crit/round6/SPEC.md`, `DECISIONS.md`, the round 15 and 16 entries of `LOG.md`, the three round-16
reviews, `.github/workflows/profile.yml`, `scripts/publish_chart.py`, `scripts/build_assets.py`,
`scripts/sheets/route.py`, `scripts/runcheck.py`, `scripts/checks/readme.py`, `scripts/checks/route.py`,
`scripts/checks/design.py`, `tests/test_pipeline.py`, `tests/test_route.py`, `docs/BEN-TODO.md`, `docs/data/AUDIT.md`
and `chart.toml`. I ran `python3 -m unittest` (539 tests, OK, 23.8 s). I looked at the round-16 renders:
`sheet-phone-day-390.png`, `sheet-desk-day-870.png`, `page-phone-1.png`, `page-desk-1.png`. There is no earlier PRD
round and no `docs/crit/prd/LOG.md`, so nothing below can repeat a fixed finding. I read 18 outside sources on PRD
practice and GitHub profile READMEs (Sources, at the end).

My brief is the document as a PRD: could a builder who was not in the room build and accept this product from it
alone, and could the owner accept or reject the result from it.

## 1. Is the product this PRD defines what he wants?

**Yes.** The sentence that decides it is from 9 Oct 11:37: *"It has to be helpful knowledge. If you were a fucking
real sailor, if you were a real person, you'd want it to be helpful data that you're looking at. You're going
through, you're like, oh, it's very helpful, and it's in a cool format."* The product in §1 and §5.1 is exactly that:
the one image is the way into his main tool (install, what happens to a URL in order, where it bites, how you stop
it, what file you get, who reads it next), and the page under it is lookup material. His second deciding sentence,
from 9 Oct 20:50, is *"Everything, single thing inside of this needs a purpose, not a fucking chasing a reason"*,
and §5.1's table gives every drawn mark a purpose, a visitor question and a data source, held by T-PURPOSE and
ROUTE-PURPOSE (I checked both exist: `tests/test_route.py:812`, `scripts/checks/route.py`). His rule on the theme
(8 Oct 14:52, 9 Oct 11:32) is met in the manner described in §1 and held by ROUTE-WORDS and T-WORDS. The renders
agree with the PRD: at 390 px the phone sheet is one screen and nothing on it has a size.

Two reservations, both about his earlier words rather than his later ones. On 7 Oct he asked for *"stunning and
fun"* and *"layers of depth"*; the PRD holds "fun" by two dry winks counted by hand and "stunning" by G1 "review".
That is honest, and his 9 Oct messages narrowed the goal to helpfulness, so I do not count it against the product.
And his last message, *"ensure this is something I want to see rounds of reviews and research"*, means the PRD must
be a thing reviewers can run rounds against. Today it is, mostly, but its "done" bar cannot be met (must-fix 1).

## 2. Verdict on the document

**6 / 10 as a PRD.** It is unusually honest and unusually traceable: every rule names its gate or says "review" or
"open", the non-goals are explicit (§4), the one big decision has options, costs and a recommendation (§9.1), and
the acceptance criteria in §8.1 are mechanical. Cagan's completeness test ("Can the QA team get enough information to
design a test plan?" [1]) passes for the image and for most of the page.

What fails it: the bar for "done" in §8.3 is a taste question that 16 rounds never passed and that the PRD
attributes to the owner, who did not set it; the count of his messages is wrong and the "verbatim" appendix is
excerpted; §6 states a failure behaviour the product does not have; the one contradiction between a rule and the
shipped page (commit counts) is carried in three places instead of decided; and four documents are interleaved
(requirements, implementation register, audit, process history), so a builder reads 531 lines to find the ~200 that
tell them what to build. None of this is hard to fix. The register (§7) is what he asked for on 11 Oct 01:12 and
must stay; it needs to be the second half of the document, not mixed into the first.

## 3. Must-fixes, ranked

### MF1. The "done" bar is undecidable, and it is not the one he set
- **Where:** §8.3, lines 334–343, especially line 342: *"The bar for 'done' that he set: the reviewers answer yes to
  all five."*
- **What to change:** His bar (9 Oct 20:50) was *"at least 10 reviews of, is it matching what I'm saying? Is it
  doing what I'm saying? Is it accomplishing my goal?"* Those are questions 1–4 of §8.3, and 16 rounds have asked
  them. Question 5, "Would the reviewer ship it as is?", is a reviewer's taste, has failed every round, and has no
  pass condition. Replace line 342 with a decidable definition:
  > **Done** = §8.1 all hold on the merge commit **and** §8.4 is logged **and** §9.1 is decided by Ben **and** three
  > reviewers answer yes to §8.3 questions 1–4 with no must-fix left open. Question 5 is advisory; only Ben's own
  > "ship it" closes the product.
  Keep "Round 16: no (8/7/8)" but say what blocked, in one line (it was §9.1, by the PRD's own §0).
- **Why:** Cagan: a must-have "literally means that the product should not ship if even one of the must-have
  features is not ready", so the must-have list has to be finite and checkable [1]; acceptance criteria must be
  "specific, verifiable, and complete" [12]. A criterion nobody can pass is not a criterion, and attributing it to the
  owner misquotes the yardstick.
- **About:** the PRD, and the product's exit from review.

### MF2. The yardstick is miscounted and the "verbatim" appendix is excerpted
- **Where:** line 8 (*"the owner's 26 messages in this session (appendix A, verbatim)"*) and Appendix A, lines
  424–491.
- **What to change:** `docs/crit/prd/owner-messages.md` holds **21** messages (I counted the `## 2026-` headings).
  Appendix A quotes **15** of them, with `[...]` elisions, and omits his last ("Review and ensure this is something I
  want to see rounds of reviews and research"). Write line 8 as *"the owner's 21 messages in this session (the full
  text is `docs/crit/prd/owner-messages.md`; appendix A excerpts the 15 that set a rule)"*, retitle Appendix A
  "excerpts", and add the 11 Oct message, because it is the instruction this review round runs under.
- **Why:** The PRD's own method is "his words are the yardstick" (§3). A yardstick with the wrong count, labelled
  verbatim when it is not, is the one thing in the document a builder cannot verify from the document. Cagan: the PRD
  must "clearly and unambiguously articulate" [1].
- **About:** the PRD.

### MF3. §6 states a failure behaviour the product does not have, and there is no rollback
- **Where:** §6, line 201: *"a failed sounding publishes last week's figures with a dated note."* Also §11, line 420
  ("re-measure when the page looks wrong") and the absence of any rollback section.
- **What to change:** I checked: `profile.yml` lines 187–200 run `build_assets.py --no-sounding --heartbeat` on a
  failed data fetch; `scripts/sheets/route.py` never reads `no_sounding` (grep: only `log.py`, `soundings.py`,
  `approaches.py` do, and those sheets are off the page), and the one test of that path builds `["log"]`
  (`tests/test_pipeline.py:47–49`). So on a failed fetch the route and the README are rebuilt from the last good
  `stats.json` with their old dates, and nothing marks them stale. Either is acceptable; the PRD must say which. And
  `publish_chart.py` force-pushes one orphan commit (its docstring, lines 2–14: "no history ... exactly one commit
  after every run"), so a bad weekly build overwrites the only copy of the six sheets. Add **§6.1 Failure and
  rollback**, three rows:
  | Event | What the visitor sees | How it is undone, by whom |
  |---|---|---|
  | data fetch fails | the page as last week, same dates, no stale mark (or: define the mark and test it on `route`) | nothing to undo |
  | a gate fails | nothing published | nothing to undo |
  | a build passes the gates but prints something wrong | the new page | Ben (or a session) `git revert`s the bot commit on `main`; a `workflow_dispatch` with `dry_run: false` rebuilds the sheets from the reverted `stats.json`; until then the `chart` branch holds the wrong sheets |
  Then correct line 201.
- **Why:** Cagan's release criteria include reliability and supportability, and "are often just hand-waved" [1];
  the Amazon internal FAQ exists to answer "what would make this fail" before launch [6]. A claim about the pipeline
  that the code does not implement is a false requirement, which is the PRD's own cardinal sin (§7.3).
- **About:** the product (the pipeline's failure path) and the PRD text.

### MF4. The one decision is not yet decidable: no size, no default, no owner of the work
- **Where:** §9.1, lines 353–364.
- **What to change:** Option 1's cost is a ten-item list in another repository with no estimate, and the table has
  no default if he does not decide. Make it decidable:
  1. Split option 1 into **1a, minimum**: the two fixes that retire everything inside the dotted line (exits when
     the frontier drains → H1 and the track gap; robots 404/scheme/fail-closed → H0, L6, L4's first clause; §5.4 rows
     1–2) plus `[project.scripts]` (§11 says a release without it loses the command line); and **1b, full**: the rest
     of §5.4. State for each what the cautions list becomes (count the items that remain).
  2. Name who does the Rust-sitemap work (him, or a session with push access, per line 364) and a rough size (days).
  3. State the default: *"Until he decides, option 3 stands: the branch stays unmerged, or merges as is."* Pick one.
  4. Add a "decide by" that is a condition, not a date: before the next weekly run after merge.
- **Why:** Shape Up: "Stating the appetite in the pitch prevents unproductive conversations" and no-gos must be
  marked [5]; Amazon's internal FAQ names the biggest risks and "what the team needs to believe" [6]; Atlassian's
  open-questions table has an answer column and a date [4]. A decision with an unbounded cost on one side is not a
  decision anyone can make.
- **About:** the PRD (and it sets the product's next step).

### MF5. A rule and the shipped page contradict each other, and the PRD carries both
- **Where:** G8 (line 78), §7.3 row "No commit totals" (line 258), §9.2 bullet 2 (lines 368–370), §10.5 (lines
  398–400).
- **What to change:** The rule says "no commit totals printed", marked "test"; the page prints *"coding agents
  (Claude) authored 45 of its 146 commits and co-signed 1 of his own 101"* and *"71 of its 499 commits ... 30 of his
  own 420"* (README facts lines; `page-desk-1.png`). Four places say "his call" and none recommends. Turn it into a
  §9.1-style row: options **keep** (an honest fact a hiring engineer asks: Q3), **strike** (his words), **share only**
  ("about a third of its commits were written by coding agents", no totals). Recommend **strike by default**, because
  his sentence is the yardstick (*"We don't need to show the commits ... it feels lazy"*, 9 Oct 11:35) and the two
  memos that argued "hiding costs more" are the agents' judgement, not his. Implement it as the `chart.toml` switch
  §10.5 already proposes, default off, so either answer is one line. Then mark G8 "gate + switch", not "test".
- **Why:** Cagan: traceability means "clearly identifying exactly which requirements support which product
  objective", and a requirement that is not held must not be marked held [1]; INCOSE: a requirement is "singular" and
  "unambiguous" [11]. The PRD's own rule (§7.3) is that nothing on the page contradicts its register.
- **About:** the product (what the facts lines print) and the PRD.

### MF6. The same requirement is stated in two to four places, in different words
- **Where:** G2 (line 72) and G5 (line 75) are the same rule; the device check is at lines 281, 346–349, 377 and
  396–397; the README-prose theme-word gap at lines 72, 224 and 388–390; the 0.1.4 retirement list at §5.4 (176–185),
  §9.1 (360) and §11 (416–418); "nothing moves" at lines 99, 128 and 143.
- **What to change:** One home per requirement, and every other mention a pointer: merge G5 into G2 ("also: no
  themed headings"); the device check lives in §8.4 only (with its pass condition, MF8), and §7.4, §9.3, §10.4 say
  "§8.4"; the theme-word gap lives in §10.1 only; the retirement list lives in §5.4 only and §9.1 says "retires §5.4
  rows 1–2" (MF4); "nothing moves" lives in §4 only.
- **Why:** Cagan: "unambiguous" [1]; Product Compass: "Do not overload this document" [7]; the PRD's own G6 rule for
  the page, "no fact said twice", applied to itself. Two wordings of one rule drift apart, and a builder does not
  know which one the gate holds.
- **About:** the PRD.

### MF7. Four documents are interleaved; split the requirements from the register
- **Where:** §0 (status and round scores), §6 bullet "Review" (lines 209–211), §7.6 (lines 300–311), G17–G19
  (lines 87–89), Appendix C (lines 523–530), and the "Held by" column of §3 against the whole of §7.
- **What to change:** Keep everything he asked for (11 Oct 01:12: the rules and how they are implemented), but in
  two parts under one title. **Part I, the product:** §1, §2, §4, §5, §8, §9, §11. **Part II, the register:** §3's
  "Held by" column, §7.1–7.5, §10, Appendix B. Move §7.6, G17–G19 and the review-scores sentence of §0 to a short
  "How this document was made" note at the end, and Appendix C to `LOG.md` (it is history, and it says so). A builder
  then reads about 220 lines to build and accept; a reviewer reads the register to check how each rule is held.
- **Why:** Cagan: the PRD is "the product's purpose, features, functionality, and behavior", and process belongs to
  managing it [1]; Google: "sufficiently detailed but short enough to actually be read by busy people" [2]; Mind the
  Product's staleness critique [9] bites hardest on §0, whose scores are out of date the day the next round runs.
  Lenny's note on Waxman's template: a one-page summary before the deep dive [3].
- **About:** the PRD.

### MF8. The judged checklist and the device check have no pass conditions
- **Where:** §8.3 (lines 336–340) and §8.4 (lines 346–349).
- **What to change:** (a) Every rule marked "review" in §7 gets a line in §8.3 with a condition a reviewer ticks:
  winks ≤ 2, and today's two named ("Boring under load.", "why engines are hard", §7.1 line 229); no theme word in
  README prose until §10.1 lands (the grep is the condition); American spelling (a word list, or make it a gate, which
  is one regex); garden paths: none a reviewer had to read twice (name the sentence); even density: no two adjacent
  rows differ in pitch (that is the construction rule, so say it). (b) §8.4 "note which edition each serves" is not
  pass/fail. Write the expected result: Safari on a 390 phone serves phone-day or phone-night by system mode; the
  GitHub app is reported to send the light theme regardless [16], so it should show **phone-day in both modes** via
  the `<img>` fallback (`README.md` line 11, HERO-FALLBACK); the sheet is one screen (≤ 900 CSS px); the first two
  screens show his name, what he builds, rustmapper and Scrapy by name and the link line. Anything else is a fail
  to log.
- **Why:** Pluralsight: testable means "clear, measurable, and complete", and words like "intuitive" are
  unverifiable [11]; Aviator: state what should and should not happen [12]; his words: *"is it matching what I'm
  saying? Is it doing what I'm saying?"* need a list to match against.
- **About:** the PRD.

### MF9. Some page rows name no holder, and one block has four names
- **Where:** §5.3 rows 2, 3, 11 (lines 153, 154, 162); §5.2 line 143 ("The image links to the Rust-sitemap
  repository"); the names "provenance" (163, 296, 403), "survey-line test" (78, 258, 296, 398), "sounding" (201).
- **What to change:** Row 2 (the link line) is held by `tests/test_round7.py:370` and `tests/test_pipeline.py:495`;
  name them. §5.2's link is held by `tests/test_pipeline.py:208`; name it. Row 3's "Python, Rust first, then by
  repository count": I found no test of that order; mark it "open" or point at one. Row 11 ("Found a mistake?") is
  held by nothing; say "none" like the other blank cells, or drop the row. Call block 12 **the provenance line**
  everywhere and name its test, `tests/test_pipeline.py:307 test_provenance_line_is_from_stats_only`; "survey" is a
  marker name a visitor never sees and "sounding" is a workflow comment.
- **Why:** Cagan's completeness test [1]; EARS: one system name, one response, same order every time [8]. A builder
  greps the PRD's name and must land on the code.
- **About:** the PRD.

### MF10. Nothing says what success looks like after merge, or who owns the page then
- **Where:** there is no section; the closest lines are §11 line 420 ("re-measure when the page looks wrong") and
  §8.2's owner column.
- **What to change:** Add **§8.5 After merge**, five lines, no ceremony: (1) owner of a failed weekly run: Ben
  (GitHub's run page; the job's `::error::` lines); (2) owner of the GitHub constants (82 px inset, 846 px column,
  `<picture>` support, line 419–420): re-measured by whoever next opens a round, and on any GitHub changelog that
  names Markdown images; (3) the role line expires 2027-06 (EXPIRY-PASSED, exists); (4) **success measure**: either
  state plainly "none is set; done is §8.3", or set one cheap one: Rust-sitemap's Insights → Traffic referrers
  include the profile within 30 days of merge, read once by Ben. (5) who may edit `chart.toml` copy after merge
  (him; a session only with a review round, per §7.5 line 291).
- **Why:** Cagan: "be very clear to everyone involved just what success looks like" [1]; Atlassian's template opens
  with success metrics [4]; ProductPlan: "if it isn't included in the PRD, it won't be included in the release" [10].
  Profile guides agree the README is the intro a recruiter reads before pinned repositories [17, 18], so whether
  anyone clicks through to rustmapper is the one number that says the image did its job.
- **About:** the PRD (and the product's life after merge).

### MF11. Loose ends in the text
- **Where:** line 45 (*"**What it is not** (§4)."*, a one-line stub); lines 3–6 and §0 say the same thing twice;
  §2 line 56 "about 7 s" cites no source number (R4 is named at line 49; give the finding).
- **What to change:** Delete line 45 (§4 is two screens down). Fold lines 3–6 into §0. Cite "R4-F*n*" for the 7 s.
- **Why:** readability; Google's "succinct" context section [2].
- **About:** the PRD.

## 4. What holds, so nobody rewrites it

- §1 answers Cagan's elevator test in two sentences [1] and names the one sentence the image must answer.
- §4 non-goals are real non-goals in Google's sense, things that could have been goals and were excluded [2].
- §5.1's table is the best part of the document: one row per mark, with what is learned, which question, the data
  source and the condition under which it is drawn. That is a testable spec and the renders match it (I checked T1,
  T2, R0, R2, S1, F1, H0, H1, C1, R13, R15 on `sheet-phone-day-390.png` and `sheet-desk-day-870.png`).
- §5.4 is the right way to write "what changes by itself": a fix, what retires, what the pipeline needs.
- §8.1 is mechanical and I could run items 1–3 (item 1 ran: 539 OK).
- §10 is an honest gap list that names fixes and declines over-engineering (§10.2, §10.3) with reasons.
- Every count I checked holds: 28 plug-ins under `scripts/checks/`, 539 tests, 18 probes in `runcheck.py`'s
  `PROBES` plus `probe_ends`, 22 repositories in `stats.json` so "15 more" = 22 − 1 − 2 − 4, six `<source>`s in
  `README.md`, `[copy]` carries no `thesis`.

## 5. Smaller notes, not ranked

- §5.2's night editions are served by `prefers-color-scheme`; GitHub documents `<picture>` as supported [14, 15]
  and says nothing about the apps; one community report says the apps always report light [16]. The PRD's §8.4 is
  the right place to settle it (MF8), and the `<img>` fallback already makes the worst case phone-day.
- §7.6 "His email is used only to identify him" is a session rule, not a product rule; the product rule is "the
  page's `mailto:` is the one he set", which is already in the cell. Keep only the product half (MF7).
- §9.2 bullets 3–5 (the printed name, the worker figure, Scrapy's filter) are owner to-dos, not open decisions
  with options. Either give each an options row or move them to `docs/BEN-TODO.md` and link once.
- G1's "Held by: review (every round's first question)" is the one goal row with no condition at all. It is honest.
  If it stays, say so in §8.3: "G1 has no test; the reviewer's yes to questions 1–4 is its proxy".

## Sources

Outside sources (read with WebFetch unless marked "via search summary"):

1. Martin Cagan, *How To Write a Good PRD* (SVPG, 2005), https://www.svpg.com/assets/Files/goodprd.pdf — read the
   full text (extracted from the PDF): purpose, user profiles, "Write It Down" (product purpose, features, release
   criteria, schedule), "Prioritize" (must-have means "should not ship if even one ... is not ready"), "Test
   Completeness" (can QA design a test plan from it), traceability from requirements to objectives.
2. Malte Ubl, *Design Docs at Google*, https://www.industrialempathy.com/posts/design-docs-at-google/ — context and
   scope, goals and non-goals ("not negated goals"), "sufficiently detailed but short enough to actually be read",
   10–20 pages for a large project, 1–3 for a mini doc.
3. Lenny Rachitsky, *My favorite templates (issue 37)*, https://www.lennysnewsletter.com/p/my-favorite-templates-issue-37
   — nine PRD/one-pager templates; praise for Yien's non-goals section, Waxman's one-page summary before the deep
   dive, Morin's success criteria and risks, Thomas's one page.
4. Atlassian, *Product requirements template*, https://www.atlassian.com/software/confluence/templates/product-requirements
   — objective, success metrics table, assumptions, requirements table with importance, open questions with answer
   and date, out of scope; "Be as specific as possible".
5. Basecamp, *Shape Up*, ch. 6 "Write the pitch", https://basecamp.com/shapeup/1.5-chapter-06 — problem, appetite,
   solution, rabbit holes, no-gos; "Stating the appetite in the pitch prevents unproductive conversations".
6. Koji, *Working Backwards: how to write an Amazon PR/FAQ*, https://www.koji.so/docs/working-backwards-pr-faq-guide
   — one-page press release, external and internal FAQ (risks, "what the team needs to believe"), about six pages,
   "every assumption as a testable claim".
7. Paweł Huryn, *PRD template*, https://www.productcompass.pm/p/prd-template — summary first, objective with key
   results, release section, "Do not overload this document", link to research instead of duplicating it.
8. Alistair Mavin, *EARS*, https://alistairmavin.com/ears/ — the five patterns, one clause order, "reduces or even
   eliminates common problems found in natural language requirements".
9. Mind the Product, *Product Requirement Documents Must Die*,
   https://www.mindtheproduct.com/product-requirement-documents-must-die/ — "Very little in a product is actually
   required"; "by the time we've written a PRD it is almost always out of date"; prototypes and direct contact.
10. ProductPlan, *Product Requirements Document*, https://www.productplan.com/glossary/product-requirements-document/
    — objective, features with out-of-scope, environment requirements; "if it isn't included in the PRD, it won't be
    included in the release"; QA writes its plan from the PRD's use cases.
11. Pluralsight, *Ensuring requirements are testable in Agile*,
    https://www.pluralsight.com/resources/blog/guides/ensuring-requirements-are-testable-in-agile — via search
    summary: testable = clear, measurable, complete; "intuitive" is unverifiable. Also the INCOSE characteristics
    (unambiguous, singular, feasible) summarised in the Boeing/INCOSE 2018 slides,
    https://www.incose.org/wp-content/uploads/legacy/presentation/IS2018-pdf/6-6-1.pdf (via search summary).
12. Aviator, *Writing effective acceptance criteria*,
    https://docs.aviator.co/verify/how-to-guides/writing-effective-acceptance-criteria — via search summary:
    specific, verifiable, complete; state what should and should not happen; cover error cases.
13. GitHub Docs, *Managing your profile README*,
    https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
    — repository named after the user, public, README.md with content; no prescribed content; when it is removed.
14. GitHub Changelog, *Specify theme context for images in Markdown (beta)*,
    https://github.blog/changelog/2022-05-19-specify-theme-context-for-images-in-markdown-beta/ — `<picture>` with
    `prefers-color-scheme` and an `<img>` fallback; no platform support stated.
15. GitHub Docs, *Basic writing and formatting syntax*,
    https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
    — "The `<picture>` HTML element is supported."; nothing on the apps.
16. Lightrun answers on anuraghazra/github-readme-stats dark mode,
    https://lightrun.com/answers/anuraghazra-github-readme-stats-feature-dark-mode — via search summary: a developer
    reports the GitHub Android/iOS apps "always return the light theme" for `prefers-color-scheme` images.
17. Instahyre, *GitHub profile checklist*, https://resources.instahyre.com/blog/github-profile-checklist/ — via
    search summary: recruiters look at 2–4 pinned repositories with clean READMEs; the profile README is the intro.
18. GreatFrontEnd, *Frontend developer GitHub profile (2026)*,
    https://www.greatfrontend.com/blog/frontend-developer-github-profile — via search summary: what a reviewable
    project README carries (one-sentence summary, setup commands, known limitations).

Files in this repository (all under `/home/user/wt-v12/`):

19. `docs/PRD.md` — the document under review.
20. `docs/crit/prd/owner-messages.md` — 21 messages, counted.
21. `README.md` — the page; six `<source>`s, the facts lines with commit counts, the provenance line.
22. `docs/crit/round6/SPEC.md`, 23. `docs/crit/round6/DECISIONS.md`, 24. `docs/crit/round6/LOG.md` (rounds 15–16),
    25. `docs/crit/round6/review-r16-{1,2,3}.md` — the first 40 lines of each.
26. `.github/workflows/profile.yml` lines 13–28, 48, 143–154, 180–200 — cron, dispatch, dry run, the failure path.
27. `scripts/publish_chart.py` lines 2–14, 62, 141–146 — one orphan commit, force-pushed, no history.
28. `scripts/build_assets.py` lines 7, 187–188, 431–433, 511–515 — `--no-sounding`, `--heartbeat`.
29. `scripts/sheets/route.py` — no reader of `no_sounding` (grep over `scripts/sheets/*.py`).
30. `scripts/runcheck.py` lines 870–872, 964 — `PROBES` and `probe_ends`.
31. `scripts/checks/readme.py`, `scripts/checks/route.py` (lines 60–62, 88, 319), `scripts/checks/design.py`
    (lines 28–30) — where `theme_words` runs and where it does not.
32. `tests/test_pipeline.py` lines 47–49, 208, 246–252, 254–258, 307, 495; `tests/test_route.py` lines 780, 807,
    812, 842–853; `tests/test_round7.py` line 370 — the tests named above. `python3 -m unittest`: 539 OK.
33. `assets/stats.json` — 22 `repos`, `runcheck` keyed `rustmapper`; `chart.toml` — `[copy]` without `thesis`;
    `docs/BEN-TODO.md`; `docs/data/AUDIT.md` (head).
34. Renders, `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/`:
    `sheet-phone-day-390.png`, `sheet-desk-day-870.png`, `page-phone-1.png`, `page-desk-1.png`.
