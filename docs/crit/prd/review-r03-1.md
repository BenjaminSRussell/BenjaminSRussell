# PRD review round 3, reviewer 1: Ben, the owner, reading the PRD as the person who has to live with the page

11 Oct 2026. I read `docs/crit/prd/owner-messages.md` twice, end to end, before anything else. Then `docs/PRD.md`
(776 lines, at `107a988`), `docs/crit/prd/LOG.md` (rounds 1 and 2: what was applied, what was declined), the three
round-2 reviews, `README.md`, `chart.toml` (`[position]`, `[contact]`, `[copy]`, the C1 entry at lines 1005–1030, the
four `fold = true` lines), `scripts/render_readme.py:459, 670–671`, `scripts/checks/readme.py:318`,
`assets/stats.json` (`edition`, the Rust-sitemap `ci` record), `docs/BEN-TODO.md`, `docs/crit/round6/SPEC.md` §0, and
the round-6 reviews and LOG for anything that had already raised what I raise here. Renders: every round-16 file named
in the brief (`sheet-phone-day-390`, `sheet-phone-night-390`, `sheet-desk-day-870`, `sheet-mid-day-746`,
`page-desk-1`, `page-desk-2`, `page-phone-1` to `-4`) and the 1a render round 2 built
(`scratchpad/prd-r02/once-1a/sheet-phone-day-390.png`, `page-phone-2.png`, `README-1a.md`). Nothing below repeats a
finding `LOG.md` marks applied. Where I say what a file contains, I opened it.

Verdict on the PRD: **7 / 10.** Round 2 did what I asked: row 0 prices the live page, the default is "merge 2b now",
the 1a render exists, my jokes rule and the "layer of a theme" half of 11:37 are carried whole. The LOG's own
next-round question was whether §9.1 now lets me decide in one sitting. Nearly. What stops it: the thing it asks me
to merge now (2b) is the one option with no render, while the option that needs Rust work (1a) has one; the
document still says it is "blocked on §9.1 (Ben's decision)" when the default is already decided and what actually
waits on me is three inputs that §8.1 and §9.2 scatter; and the 1a render shows a wording fault on the first screen
that §5.4 row 1 calls "nothing needed here".

---

## 1. Is the product this PRD defines what I asked for?

**Yes.** The sentence that decides it is still 9 Oct 11:37: *"It should be telling you about me, but with a layer of
a theme of shipping. [...] It has to be helpful knowledge. If you were a fucking real sailor, if you were a real
person, you'd want it to be helpful data that you're looking at [...] and it's in a cool format."* Tested by
9 Oct 20:50: *"Everything, single thing inside of this needs a purpose, not a fucking chasing a reason."*

§1 and §5.1 define that page and the renders are that page: one image that is the way into rustmapper (the install
line, what happens to a URL in order, where it bites, the one key, the file, who reads the file next), lookup text
under it, every mark with a PURPOSE row, nothing sized by a count, no word naming what it is. On
`sheet-phone-day-390.png` every word is readable, the night edition is a redraw, and the three second-reading marks
(the bracket, the gap under the box, the line past the end bar) are where G1a says. The message that triggered this
round, *"Review and ensure this is something I want to see rounds of reviews and research"*, is answered by G17–G19
and by this review existing: three reviewers, sources, a fix round between.

**Would I screenshot §5's product and send it?** The image, yes. I would call it "how you get into my crawler". A
stranger who knows the forms sees where the colours come from; one who does not sees a route. Logged for G13a, as
§8.3 q.6 asks. The page under it: not with the commit counts on its second screen (§8.1 item 7, already blocking;
not repeated).

## 2. Must-fixes, ranked

Each: where (section, line of `docs/PRD.md` at `107a988`), what to change, why (my words or a source), and whether it
is about the PRD text or the product it defines.

### MF1. The option I am asked to merge now has no render, and the PRD does not say what I, specifically, have to do (PRD text, and one build; §0 line 3 and lines 40–44, §9.1 lines 508–515 and 523–546, §9.3 lines 589–596)

§0 line 3: *"Status: draft, blocked on §9.1 (Ben's decision)."* §9.1's default bullet (line 523): *"merge 2b now,
then decide 1a against 1b with the renders in hand."* So the PRD has already chosen what to merge; what it calls my
decision is 1a-against-1b, which by its own sequencing comes after the merge and after a release I have not cut. What
actually stands between the branch and `main` is listed elsewhere: §8.1 item 6 (my position line and one contact;
`chart.toml:26, 30–31` are `""` today, I checked), §8.1 items 7 and 8 and §10.19 (session work), and §9.2's
strike/keep line. The document asks me to decide the far thing and buries the near things.

And the near thing has no picture. The 1a render exists (`scratchpad/prd-r02/once-1a/`, I opened it); there is no
`once-2b` anywhere under the scratchpad (`ls -d scratchpad/*2b*`: nothing). 2b is four `fold = true` lines in
`chart.toml` and a cap (§10.19); the render is the second phone screen with two items instead of six. My test is
9 Oct 20:50, *"is it accomplishing my goal? Not just what I'm saying"*, and I judge a screen by looking at it. The
PRD recommends the one option it has not shown me.

Change:

1. §0 line 3: *"Status: draft. Waits on three inputs from Ben (§9.0) and three session items (§8.1 items 7, 8;
   §10.19)."*
2. A new §9.0, four lines, before §9.1: **What only Ben does, in order.** (a) `[position] text` and one of
   `[contact] linkedin` / `resume` (§8.1 item 6; the shape is in `BEN-TODO.md`: "role · city or timezone · open to /
   currently"). (b) One word against §9.2: strike / keep / share. (c) Yes or no to merging 2b (§9.1). Everything else
   is a session's, and the 1a/1b choice comes after a release and is not needed for the merge.
3. Build the 2b render the way round 2 built 1a (`fold = true` on L4, L6, L2, L5; the fold cap at 8 or a separate
   open-list cap), and put `page-phone-2.png` beside round-16's and 1a's in §9.1. Until it exists §9.1's intro says
   so in its first line, as it did for 1a in round 2.

Why: 8 Oct 09:04, *"all PRs need to be ready to merge"*; 9 Oct 20:50 on judging by the goal, not the words. The
hiring-side sources are one-voiced that the second screen is where a stranger decides whether to keep reading
("Hiring managers are trying to answer a simple question under time pressure: can this person probably do the work?"
[S4]; a cold read should convey what you can do "in two minutes" [S1]). The two-sided-message literature (§5.2) says
2b is the right shape; a render is what shows whether it reads that way.

### MF2. Under 1a the first screen tells a stranger to Ctrl-C a tool that exits by itself (product; §5.1 line 153, §5.4 line 213, §9.1 line 511, §10.9 line 615)

§5.4 row 1 (line 213), the "exits when the frontier drains" fix: *"Needs here, first: nothing (verified: H1 → `""`,
retired)."* §9.1's 1a row (line 511) lists the first screen as *"… fetches up to 20 pages; press Ctrl-C once;
`data/sitemap.jsonl`; …"* as if that were fine.

It is not. The 1a render (`once-1a/sheet-phone-day-390.png`) prints, with no box above it, *"press Ctrl-C once and
wait for `Saved to`; a second press quits without writing the file."* A stranger who has just read that the loop
closes on the fetch row and that nothing stops the run by hand is now told the one step is to kill it. The reason
is in `chart.toml:1005–1030`: C1's first wording holds on `runs = ["crawl_ctrl_c", "second_ctrl_c"]`, both of which
pass whether or not the crawl exits; its `instead` (line 1025, "press Ctrl-C once to write `data/sitemap.jsonl`")
holds on `crawl_ctrl_c` alone. Neither wording names `ends_by_itself`, so a release that exits changes nothing on
this row. Round-6 LOG line 267 said "C1's kill clause" retires on 0.1.4; the resolver shows it does not. The 1a code
block (`README-1a.md`) is right (the three stop-rule comment lines are gone); the image is wrong.

Change: in `chart.toml`, give C1's first wording `fails = ["ends_by_itself"]` (with its existing `runs`), and add a
wording for a release that exits, held by `runs = ["ends_by_itself", "crawl_ctrl_c", "second_ctrl_c"]`: *"stops when
the queue drains and writes the file; Ctrl-C once stops early and still writes it; a second press quits without."*
(the `second_ctrl_c` anchors as today). In the PRD: §5.4 row 1's "Needs here" becomes *"a C1 wording for a release
that exits (§10.9)"*; §0's "four of the eight retire on their own" becomes three; §10.9 gains the row; §9.1's 1a
first-screen cell reads *"… Ctrl-C once stops early …"* once the wording exists, and until then says the render shows
the old line. This is the §5.4 "Needs here" check the LOG's round-1 next-round note asked for, applied to the one
row it marked clean.

Why: 9 Oct 11:37, *"It has to be helpful knowledge. If you were a fucking real sailor … you'd want it to be helpful
data."* A step that is wrong for the release the image names is the opposite. And §7.3's own rule: "Figures retire by
themselves when the tool changes" is claimed true of this row and is not.

### MF3. Two of my 7 Oct sentences are in appendix A and nowhere in the goal table (PRD text; §3 lines 96–99, appendix A lines 673–679)

Appendix A quotes 7 Oct 17:18, *"It's mediocre and not exciting or well designed and intercut this feels basic"*, and
7 Oct 17:40, *"this should appear like it took a team months of work and years of workshopping to create and design
and manufacture"*. §3 carries the rest of 17:40 (G1a "say more than it literally says", G1b "what does it say about
the person who made it") and 15:30 (G1, G1c). The standard of *apparent effort* ("appear like it took a team
months") and the negative that set it ("feels basic") have no row, so no round asks the question. The brief for this
review is whether anything I said is missing from the 19 rows; this is.

Change: add G1d, *"this should appear like it took a team months of work and years of workshopping" (7 Oct 17:40);
"not exciting or well designed … feels basic" (7 Oct 17:18)*. Meaning: *the care shows without being announced: one
pitch and one edge (G3), real field names and version dates, every figure with its source commit, the two
second-reading marks, and the one link to `DESIGN.md` for a reader who wants to see how it was made.* Held by:
*review (§8.3 q.6, with a third line: does it look made with care, and where did the reviewer see it).* No gate; no
test; say so. And in §8.3 q.6 add that line.

Why: it is my sentence, and the PRD's rule (§3 preamble) is that each row is "a thing he said". The sources agree
that the signal is care, not decoration: "They usually notice clarity before complexity" and "A profile README
should not be a wall of badges or animations" [S4]; "Honest specificity is more convincing than inflated ambiguity"
[S4]; "Stronger READMEs explain decisions" [S4]. A row that names where the care is visible keeps a later round from
adding decoration to meet "months of work".

### MF4. §9.1's first-screen column leaves out the two first-screen facts a merge does not change: the release's age and the tool's two names (PRD text; §9.1 lines 508–515, §11 lines 653–655)

The 2b and 3 rows say the first screen is *"as today, with the box"*. What "today" prints on the first screen, in the
line above the box (`sheet-phone-day-390.png`): `pip install rustmapper` **0.1.3 · 8 NOV 2025**, and on the next
row `rust_sitemap crawl`. PyPI's JSON confirms 0.1.3 uploaded 2025-11-08 and no later release [S12]; the facts line
two screens down says `main` passed CI on 7 Oct 2026. So a stranger's first screen says: the release is eleven
months old (at merge), the code is alive, and the thing you install is not the thing you type. The product reviews
saw both and kept both ("an honest age; the fix is a release", r14-2, r15-2, r15-3, r16-2; "three names for one
tool … the owner's", r13-2). The PRD prices neither into the decision. R2's row (§5.1 line 144) even says what the
stranger learns is "how old the release is", and then §9.1 does not say it.

Change: in the 2b and 3 rows' first-screen cell, after "with the box": *"and `0.1.3 · 8 NOV 2025` (eleven months
old at merge, and older each week) over `rust_sitemap crawl` (the wheel's command; the image says `rustmapper` two
lines up). Only a release changes either (§5.4 row 6; §11)."* In the 1a row: *"`pip install rustmapper` 0.1.4 ·
<date>; `rustmapper crawl` (one name)."* And in the "Rows are not alternatives" paragraph, say that the age and the
two names are the two first-screen facts that make the release worth cutting soon, not only the cautions.

Why: 9 Oct 11:32, *"especially if you want to be able to know what the fuck it's trying to say about me"*: the
first screen is what strangers read about me, and the PRD should price everything on it, not only the box. The
sources treat age as a signal in its own right: OpenSSF Scorecard's Maintained check scores commit activity in "the
previous 90 days" and its risk line is "A project which is not active might not be patched" [S8]; Snyk labels a
package by "npm versions cadence, the repository activity, and other data points" and prints "Last Release: 9 months
ago" beside "INACTIVE" [S11]; the hiring guides warn against "stale demos in featured projects, since reviewers may
assume the rest of your work is equally rough" [S4] and against "Overselling" that "invites the interviewer to test
that claim" [S1]. The page is honest about the age; the decision table should be too.

### MF5. Loose ends in the record (PRD text; §3 line 118, §8.3 lines 446–448, G13a line 112)

- G19's "Held by" cell cites `docs/crit/prd/review-r01-{1,2,3}.md` only. Round 2 and this round exist; write
  `review-rNN-{1,2,3}.md` as the product rows do.
- G13a logs the round-2 q.6 answers in the table cell. That cell will not scale; log q.6 answers in
  `docs/crit/prd/LOG.md` per round and have the cell point there. My round-3 answer is in §1 above.
- §8.3 q.6's parenthesis cites "round 4's question to him was which one he would screenshot"; that question
  (`BEN-TODO.md`, round 4, third ask) is still on my list unanswered. Either strike it from BEN-TODO as overtaken
  by round 6, or say in §9.2 that it is open. It is overtaken; strike it. (§10.10 already covers BEN-TODO's thesis
  line; this is a different item.)

Why: 11 Oct 01:12, *"review all of the do and donts and specifically all of the rules … and review how they are
implemented"*: a register that cites the wrong round is one I stop trusting.

## 3. The 19 goal rows against my sentences

| Row | Missing, softened, or reinterpreted? |
|---|---|
| G1 | Held as review; the q.1–4 proxy is honest. |
| G1a | Held; the three marks are on `sheet-phone-day-390.png` where it says. Note for the record: under 1a the second mark (the gap) goes with the fault it marked, and the PRD says so (line 540). Right. |
| G1b | Held. |
| G1c | Held now; the round-2 fix carries my trade in my words. |
| **(missing)** | 7 Oct 17:18 "feels basic" and 17:40 "appear like it took a team months of work" have no row (MF3). |
| G2, G5 | Held. "Helm chart" is the only theme word in the prose and it is a project fact. |
| G3 | Held, visibly, on all five sheets. |
| G4 | Held except §8.4 (mine to do) and §9.1b (default a stands). |
| G6 | Held. |
| G7 | Held; the strongest row. |
| G8 | Open on the page, blocking (§8.1 item 7). Not repeated. |
| G9, G12 | Held on the branch. |
| G10 | Held now (round 2). The two winks are fine. |
| G11 | Held; the retired strings block the merge (§8.1 item 8). Not repeated. |
| G13, G13a | Held; G13a's log needs a home (MF5). |
| G14 | Held on the branch; §10.10 open. |
| G15, G16 | Held, and C1 under 1a is the one place the PURPOSE row ("the reader's one step") stops being true of the words (MF2). |
| G17, G18, G19 | Done as process; G19's cell is stale (MF5). |

Nothing in the table is softened or reinterpreted this round. One thing I said is missing (MF3), and one row's
holder is wrong for one release state (MF2).

## 4. The top of the page, as rendered

`sheet-phone-day-390.png`: my name, the two-line role, "rustmapper" and its sentence, the install line with the
version and date, two rows of how it runs, the red dotted box with the two catches, the Ctrl-C row, the file with its
real field names, the hand-off line. `page-phone-1.png`: the whole sheet, the link line and "Ben Russell builds…" on
the first screen. `page-phone-2.png`: the pick, the facts line (with the counts, blocking), the platform note, the
first three cautions. `page-desk-1.png`: all of that and the six cautions and the code block on one screen, the code
comments wrapped at 32 columns (§11; §10.16).

Do I want strangers to see the top first? The sheet, yes. It looks like a page from a manual written by someone who
measured what he wrote. The box, yes, on one condition the research in §5.2 makes exact: the positive has to come
first and the admitted fault has to carry its fix. On the first screen the positive before the box is one sentence
("Crawls a site and writes one line for every URL it finds") and an install line that is eleven months old; the
competence evidence (CI passed 7 Oct 2026, 176 test functions, 16k lines) is on screen two. H1 in the box carries its
fix ("quit when `Received work item` lines stop for 60 s"); H0 ("on https, pages behind a disallowed link wait")
carries none. So the box is two-thirds the right shape. That is not a must-fix, because the honest fix is the
release (1a), and the PRD already sequences it; it is why MF4 wants the age on the decision table and why the 2b
render (MF1) matters: the second screen under 2b is where the positive-then-fault order is either met or not.

What is right and should stay: no stats card, no badge row, no first person, no marketese; the fold of 15; "Also"
and "Working rules" as the only headings. Every guide I read this round says the same ("A good README feels like a
helpful front desk. It points people to the right things fast" [S4]; "Pinned repositories" first, then the README,
then commit messages, graph "a sanity check" [S1]).

## 5. Research

### 5.1 What convinces a senior engineer or a hiring manager on a GitHub profile in 2026

Eight practitioner sources this round (none a controlled study; the search summaries say so and so do I), read
against round 2's nine. Where they agree, and what it means for this page:

1. **Order and time.** Pinned repositories, then the top project's README, then commit messages, then whether the
   code runs; the graph last, "a sanity check" [S1]. "Developers pin what they consider their best work" [S3]. A
   cold read should land "in two minutes"; an opened project "in five minutes" [S1]. No source measures it; the
   30-second figure "is not sourced" (search summary, S13). The PRD's Q1–Q5 order and its "first screen" rule (not a
   number) are the right reading of this.
2. **The question under time pressure.** "Hiring managers are trying to answer a simple question under time
   pressure: can this person probably do the work?" [S4]. "Employers care more about proof than motion" [S4]. The
   facts lines (CI conclusion with its date, test counts, lines) are proof; the commit-authorship counts are motion,
   which bears on §9.2 (strike).
3. **Seniority is read from decisions and clarity.** "They usually notice clarity before complexity"; senior
   engineers "look at naming, documentation, testing, and how you explain tradeoffs"; "Stronger READMEs explain
   decisions" [S4]. The Working rules block with dated cites is the page's answer; the `DESIGN.md` link is the
   second. MF3 names where the care shows so a later round does not reach for decoration.
4. **What hurts.** A missing or one-line README is "one of the fastest ways to lose interest" [S1]; "If a reviewer
   clones it and it breaks immediately, that's worse than not having the project at all" [S1]; "'production-grade'
   for a weekend project invites the interviewer to test that claim" [S1]; "stale demos in featured projects, since
   reviewers may assume the rest of your work is equally rough" [S4]; "Heavily forked repos with no substantive
   commits of your own read as inactivity dressed up as activity" [S1]; green squares "can be gamed, so open the
   actual commits" [S3]; "Followers … correlate with public visibility, not engineering ability" [S3]. The page prints
   none of these; the eleven-month release is the one staleness it does print (MF4).
5. **Self-awareness is a plus.** Say "what you'd improve with more time", since that "shows self-awareness" [S1]. A
   README should state "a simple 'one-time' setup guide" and "how and where bugs should be reported" [S10]. The
   cautions with their levers, the code block and "Found a mistake? Open an issue." are exactly that.
6. **Recruiter-side sources still start from the graph** ("shortlist based on the number of green squares" [S2]) and
   then say to look past it ("essential to look beyond these indicators" [S2]). Nothing on the page feeds the graph;
   nothing on it should (§4).

### 5.2 Do a tool's known faults on its author's own profile help or hurt?

Rounds 1 and 2 covered two-sided messages and the blemishing effect. This round adds the two findings that decide
the shape of the list, and both point the same way as §9.1's 2b default:

- **Refutation is the condition.** Allen's 1991 meta-analysis of 26 studies: "the order of the most effective
  messages should be two-sided with refutation, one-sided, and two-sided with no refutation"; "the least persuasive
  messages were two-sided with no refutations" [S6]. O'Keefe's 1999 meta-analysis of 107 studies, about 20,000
  participants, the same: two-sided messages that "don't refute the opposing view can be significantly less
  persuasive than a comparable one-sided argument", and refuting them brings "a boost in our credibility" [S7]. On the
  page a "refutation" is a lever beside the fault. L1 (`--workers 1`) and L7 (`--user-agent`) have one; L2 and L5
  have one; L4 and L6 have none. 2b keeps the two best-refuted items open and folds the rest; 3 puts two unrefuted
  items on the second screen. So the literature ranks 2b above 3 and, on the open list, 2b above today. The PRD's 2b
  row should cite this as the reason, not only "few".
- **Competence first.** The pratfall effect (Aronson, Willerman and Floyd, 1966): "a knowledgeable blunderer was
  rated to be more attractive", while the mediocre one's appeal fell; later work (Mettee and Wilkins, 1972) found a
  competent person's minor blunder costs "a negligible drop in liking and a small drop in respect", and a less
  competent person's "any blunder loses liking" [S5]. The condition is prior competence. On this page the competence
  evidence is on screen two and the box is on screen one (§4). That is the honest reason the release matters more
  than the cautions alone, and why MF4 asks the decision table to price the age.
- **Convention.** Limitations belong beside the claims they qualify, and "candor about limitations … builds trust
  and reduces support load" (search summary, S9). The page does both: the box at the stop where the fault bites, the
  list under the install note.

So: faults on the profile help when each carries its fix, when they come after the competence signal, and when they
are few. 2b meets the first and third today; the second only a release meets. The PRD's sequencing (2b now, 1a soon)
is the right order, and MF1, MF2 and MF4 are what it needs to put in front of me to say yes in one sitting.

### 5.3 One thing I checked against GitHub's own docs

GitHub's writing syntax page says only "The `<picture>` HTML element is supported" and nothing about `<source
media>` width queries [S9b]. The PRD's claim that the mid and desk editions switch at 852 and 1,200 px rests on
"measured on the live page 10 Oct 2026" (§8.5, §11), not on documentation; that is the right basis and the PRD says
so. Nothing to change.

## 6. What I checked and found correct

| PRD claim | Checked | Holds |
|---|---|---|
| `[position] text`, `[contact]` empty | `chart.toml:26, 30–31` | yes |
| `agent_clause` called unconditionally; no `[facts]` switch | `render_readme.py:459`; `grep agent_clause chart.toml`: none | yes |
| `[copy]` theme strings survive at `chart.toml:35–39` | read | yes |
| `LIST_MAX_ITEMS = 7`, `LIST_MAX_WORDS = 25`, read by `checks/readme.py:318` | read | yes |
| the 1a render exists with the fixture and `README-1a.md` | `scratchpad/prd-r02/once-1a/` | yes |
| the 1a render shows no box, no gap, `rustmapper crawl`, five items | `once-1a/sheet-phone-day-390.png`, `README-1a.md:44–50` | yes |
| §5.4 row 1 "Needs here: nothing" | `chart.toml:1005–1030`; the 1a sheet prints "press Ctrl-C once and wait for `Saved to`" | **no** (MF2) |
| edition 0.1.3, 2025-11-08, scripts `["rust_sitemap"]`; CI success 2026-10-07 at `32c2651` | `stats.json`; PyPI JSON [S12] | yes |
| 2b "recommended now" with a render | none exists | **no render** (MF1) |
| G19 held by `review-r01-{1,2,3}.md` | line 118 | stale (MF5) |

## 7. Score

**7 / 10.** The document now prices the live page, sequences the decision, and carries my sentences whole; it is the
one place my rules and their gaps are written down honestly, and round 2's fixes held. It does not go higher because
the option it asks me to merge is the one it has not rendered and the inputs it actually needs from me are not
listed in one place (MF1); because the one §5.4 row it marked clean prints a wrong step on the first screen under
1a (MF2); because two of my 7 Oct sentences are quoted in the appendix and held by nothing (MF3); and because the
decision table prices the box and not the date beside it (MF4). Fix MF1 and MF2 and I can say yes to 2b from the
PRD alone.

## Sources

1. F1 Jobs, "What Your GitHub Commit History Should Look Like Before a Technical Screen",
   https://www.f1jobs.io/resources/blog/github-commit-history-before-technical-screen — read in full: reviewers
   "skim in a predictable order" (pinned, the top README, commit messages, does it run, graph "a sanity check");
   a cold read "in two minutes", an opened project "in five minutes"; "one of the fastest ways to lose interest";
   "If a reviewer clones it and it breaks immediately, that's worse than not having the project at all";
   "'production-grade' for a weekend project invites the interviewer to test that claim"; say what you'd improve,
   it "shows self-awareness".
2. Reczee, "Evaluating GitHub profiles: a recruiter's guide",
   https://reczee.com/blog/evaluating-github-profiles-a-recruiters-guide — read in full: recruiters "shortlist based
   on the number of green squares" then must look "beyond these indicators"; merged PRs to popular projects "can
   signal a higher quality contribution"; "well-documented, functional projects"; clear READMEs as a professional
   sign; no time figure.
3. Noon, "How to source on GitHub", https://www.noon.ai/blog/how-to-source-on-github — read in full: "Developers pin
   what they consider their best work"; READMEs reveal communication; graphs "can be gamed, so open the actual
   commits"; "Followers … correlate with public visibility, not engineering ability"; "An empty public GitHub is weak
   negative evidence at best".
4. Rockstar Developer University, "GitHub profile: get hired",
   https://rockstardeveloperuniversity.com/github-profile-get-hired/ — read in full: "Hiring managers are trying to
   answer a simple question under time pressure: can this person probably do the work?"; "They usually notice
   clarity before complexity"; "if I dropped this person into our codebase, would they create confidence?";
   "Employers care more about proof than motion"; "A good README feels like a helpful front desk"; "Stronger READMEs
   explain decisions"; "Honest specificity is more convincing than inflated ambiguity"; avoid "a wall of badges or
   animations" and "stale demos in featured projects, since reviewers may assume the rest of your work is equally
   rough".
5. Wikipedia, "Pratfall effect", https://en.wikipedia.org/wiki/Pratfall_effect — read: Aronson, Willerman and Floyd
   1966 (92 % vs 30 % contestants, the coffee spill); "a knowledgeable blunderer was rated to be more attractive";
   the mediocre one's appeal fell; Mettee and Wilkins 1972 on severity: a competent person's minor blunder "a
   negligible drop in liking and a small drop in respect", a less competent person's "any blunder loses liking".
6. CustomerThink, "One-Sided vs. Two-Sided Arguments", https://customerthink.com/one-sided-vs-two-sided-arguments/
   — read: Allen 1991, 26 studies; "the order of the most effective messages should be two-sided with refutation,
   one-sided, and two-sided with no refutation"; "the least persuasive messages were two-sided with no refutations";
   best "for an educated and involved audience, if done right".
7. PsyBlog (spring.org.uk), "Balanced Arguments Are More Persuasive", https://www.spring.org.uk/?p=12521 — read:
   O'Keefe 1999, 107 studies, about 20,111 participants; two-sided arguments that "don't refute the opposing view can
   be significantly less persuasive than a comparable one-sided argument"; refuting brings "a boost in our
   credibility".
8. OpenSSF Scorecard, `docs/checks.md`, https://github.com/ossf/scorecard/blob/main/docs/checks.md — read the
   Maintained, Packaging and Signed-Releases sections: "This check determines whether the project is actively
   maintained"; "at least one commit per week during the previous 90 days" for the top score; risk "A project which
   is not active might not be patched, have its dependencies patched, or be actively tested and used"; no check
   scores release age directly.
9. Search summary over README-practice templates (Glama "README Best Practices", FOSShub "README", Caltech Library
   template, JHU OSPO), query `README "known limitations" section best practice open source trust` — summary only:
   put caveats "right beside the relevant instructions"; "candor about limitations … builds trust and reduces
   support load"; hidden limitations as an anti-pattern.
9b. GitHub Docs, "Basic writing and formatting syntax",
   https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
   — read: "The `<picture>` HTML element is supported"; nothing on `<source media>` width queries.
10. Johns Hopkins OSPO, "Public code repository best practices",
    https://ospo.library.jhu.edu/learn-grow/public-code-repository-best-practices/ — read: a README's four parts
    (identification, evaluation, usage, engagement); "a simple 'one-time' setup guide"; "Describe how and where bugs
    should be reported"; review the README "annually, during a major release".
11. Snyk, package page for npm `link`, https://security.snyk.io/package/npm/link — read: "INACTIVE" under
    Maintenance; "Last Release: 9 months ago"; health score "61/100"; maintenance judged on "npm versions cadence,
    the repository activity, and other data points". (The `dev.snyk.io/advisor` URL redirects here; Advisor is being
    retired, per the search summary.)
12. PyPI JSON for rustmapper, https://pypi.org/pypi/rustmapper/json — read: `info.version` "0.1.3"; `upload_time`
    "2025-11-08T19:52:41"; releases 0.1.0–0.1.3; summary "Sitemap crawler and URL discovery tool built with Rust (256
    workers, sharded frontier, WAL persistence, optional Redis)"; project URLs to `Rust-sitemap`. (The HTML page
    returned "A required part of this site couldn't load.")
13. Search summary, query `what hiring managers look for GitHub profile README 2026 senior engineer` (Underdog,
    Instahyre, Reskilll, Reczee, TechInterview, Parse.gl, Rockstar Developer University) — summary only, beyond the
    pages read above: "quality of a few repos beats quantity"; the profile README "the first thing they read"; the
    30-second figure "is not sourced".
14. Round-2 sources re-used by number from `docs/crit/prd/review-r02-1.md` (Underdog, TechInterview, CoderCops,
    GreatFrontEnd, McTaba, Reskilll, Reczee, Stanford GSB on the blemishing effect, INT 1, AM Nautical): not re-read
    this round; cited only where §5 says "round 2".
15. Repository files read: `/home/user/wt-v12/docs/PRD.md`; `/home/user/wt-v12/docs/crit/prd/owner-messages.md`;
    `/home/user/wt-v12/docs/crit/prd/LOG.md`; `/home/user/wt-v12/docs/crit/prd/review-r02-{1,2,3}.md`;
    `/home/user/wt-v12/README.md`; `/home/user/wt-v12/chart.toml` (lines 20–39, 1005–1041, the `fold = true` lines
    1257, 1276, 1308, 1357); `/home/user/wt-v12/scripts/render_readme.py` (459, 670–671, 925);
    `/home/user/wt-v12/scripts/checks/readme.py:318`; `/home/user/wt-v12/assets/stats.json` (`edition`, the
    Rust-sitemap `ci` record); `/home/user/wt-v12/docs/BEN-TODO.md`; `/home/user/wt-v12/docs/crit/round6/SPEC.md`
    §0; `/home/user/wt-v12/docs/crit/round6/LOG.md` (lines 107, 267, 545); `docs/crit/round6/review-r03-3.md:113`,
    `r07-3.md:213`, `r13-2.md:58`, `r14-2.md:69`, `r15-2.md:102`, `r15-3.md:121`, `r16-2.md:131`.
16. Renders: `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/`
    (`sheet-phone-day-390.png`, `sheet-phone-night-390.png`, `sheet-desk-day-870.png`, `sheet-mid-day-746.png`,
    `page-desk-1.png`, `page-desk-2.png`, `page-phone-1.png` to `page-phone-4.png`) and
    `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/prd-r02/once-1a/`
    (`sheet-phone-day-390.png`, `page-phone-2.png`, `README-1a.md`).
