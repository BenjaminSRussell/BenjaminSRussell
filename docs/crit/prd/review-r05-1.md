# PRD review round 5, reviewer 1: Ben, the owner, reading the PRD as the person who has to live with the page

11 Oct 2026. I read `docs/crit/prd/owner-messages.md` twice, end to end, before anything else. Then `docs/PRD.md`
(898 lines, at `0a557ff`; its header says the product baseline is `027f081`, and `git diff --stat 027f081..HEAD --
. ':!docs'` is still empty, so the page under review is the one the PRD describes), `docs/crit/prd/LOG.md` (rounds 1
to 4, applied and declined), `docs/crit/prd/review-r04-1.md` (so that nothing below repeats it), `README.md`,
`git show main:README.md` (the live page's `<picture>`), `scripts/publish_chart.py` (docstring and its argparse
options), `scripts/render_readme.py:43–52, 455–465`, `scripts/checks/position.py:28–36`, `scripts/checks/route.py:55–61`,
`scripts/runcheck.py:1–12`, `chart.toml:20–39`, `DESIGN.md:1–30`, `docs/BEN-TODO.md`. Renders: round-16
`sheet-phone-day-390`, `sheet-phone-night-390`, `sheet-desk-day-870`, `sheet-mid-day-746`, `page-desk-1`, `-2`,
`page-phone-1`, `-2`, `-3`, and `renders/once-2b/page-phone-2.png`. I cropped and enlarged the track under the dotted
box on the phone and desk sheets (scratchpad `gap-crop.png`, `gap-crop-desk.png`) to see whether G1a's gap is really
there at phone size. Where I say what a file or a render contains, I opened it.

Verdict on the PRD: **7 / 10.** Round 4 did what I asked: 2b is defined by a rule and rendered, my bio line no
longer blocks the merge, the device check is mine and after the merge, "stunning and fun" has a pass condition, the
renders are in the repository. The LOG's own question for this round was whether I can say yes to 2b and pick A or B
from the PRD and the committed renders alone. **Yes to 2b, from `once-2b/page-phone-2.png`: four items, each with
its flag or its sign, the fold closed under them.** A or B: **no**, and that is the first must-fix: both orders put a
broken image in front of some readers of the live page, which is the one thing I said on 8 Oct 11:13 that I never
want to see again, and the PRD's own rule in §7.4 says the sheets are on `chart` before the README names them. What
else stops a higher score: my first sentence of 7 Oct is still only half carried (the "massive interest in design"
half has no row); the one decision §9.2 asks of me is recommended on a reading of my 11:35 sentence that the
sentence does not support, with none of this year's hiring evidence beside it; and five PRD rounds have now changed
no product file while `main` serves the page I rejected on 9 Oct.

---

## 1. Is the product this PRD defines what I asked for?

**Yes.** The sentence that decides it is 9 Oct 20:50, the test I set: *"How does it help the user see my project?
What is it showing? [...] is it matching what I'm saying? Is it doing what I'm saying? Is it accomplishing my goal?
Not just what I'm saying. My goal is to have a purpose behind each map. [...] Everything, single thing inside of
this needs a purpose."* The image shows how a stranger gets into my main project and what comes out of it; every
mark on it has a row that says what it teaches and from which file (§5.1, 17 rows); nothing on it has a size
(G15). That is "accomplishing my goal", not only matching my words. The second sentence, 9 Oct 11:37, says what the
page is for: *"It should be telling you about me, but with a layer of a theme of shipping. [...] It has to be helpful
knowledge."* The route is helpful knowledge; the manner is in the track, the dotted line and the paper, and no word
names it (G2, G5).

**My one sentence for G3a** (§8.3 q.1's first line; I had read §1 before I looked, so this is the sentence I would
have written from the phone sheet alone, and I say so): *"pip-install a crawler, run it on a URL, it loops over
pages, on https it can hang behind robots.txt and it never stops by itself, Ctrl-C once writes a JSONL of URLs that
another of his tools sorts."* It names a tool, how you start it and an output. Log it against G3a.

**Would I screenshot the image and send it?** Yes, and I would call it "how you get into my crawler" (the same words
as rounds 3 and 4; log for G13a). Does it look made with care (G1d)? Yes: the name in a serif over a tracked sans,
code in a mono at the word space, the release's own date, the real field names, and the gap in the track under the
box, which I checked at phone size: the magenta line stops at the loop's foot and starts again above the Ctrl-C
ring, with cream between (`gap-crop.png`). That is a second reading a stranger can find and nobody announces.

The yes has the same condition as rounds 1 to 4 and I do not repeat it as a must-fix: the page prints the
agent-authorship counts (§8.1 item 7) and the retired theme strings sit in `chart.toml` (item 8). Both are owned and
blocking. What I add this round is that the merge, as §8.1 item 9 plans it, is not something I want to see (MF1).

## 2. Must-fixes, ranked

Each: where (section, line of `docs/PRD.md` at `0a557ff`), what to change, why (my words or a source), and whether it
is about the PRD text or the product it defines.

### MF1. Both orders of the first merge show a broken image to some readers of the live page (product the PRD defines; §8.1 item 9 lines 436–449, §7.4 row line 370, §10.20 line 720, §11 lines 745–746, §9.0 (c) lines 559–561)

What I checked. `main`'s README (`git show main:README.md`, lines 6–13) names eight sheets on the `chart` branch:
`hero-phone-still-night`, `hero-phone-still-day` (both under `(max-width: 767px) and (prefers-reduced-motion:
reduce)`), `hero-phone-night`, `hero-phone-day`, `hero-still-night`, `hero-still-day` (both under
`(prefers-reduced-motion: reduce)`), `hero-night`, and `hero-day` as the `<img>`. The branch's README names six
(`README.md:7–13`), none of them a `still`; the branch's renderer has no reduced-motion source any more
(`grep prefers-reduced-motion README.md` = 0; the `still` rows survive only as comments at `render_readme.py:43–52`).
`publish_chart.py` ships "every SVG named in assets/build-report.json" as a parentless commit and nothing else (its
docstring, lines 6–9); its options are `--dry-run`, `--branch`, `--remote`, `--report`, `--social`, `-m` (lines
155–160); there is no way to keep what the `chart` branch holds now.

So under **order A** (publish, then merge within the hour), from the publish until my merge every reader of the live
page whose browser reports `prefers-reduced-motion: reduce`, at any width, is served a `<source>` whose file is gone.
The browser does not move on to the next source when the chosen one fails: the HTML spec picks "one image source
from sourceSet" and an image whose fetch yields no data is "broken" [S10]; MDN describes selection by `media`,
`srcset` and `type` only, and says nothing about retrying after a failed load [S9]. That reader sees a broken image
for up to an hour. Under **order B** (merge, then let the job publish), every reader between 852 and 1,199 px sees a
broken image until the job's publish lands (minutes; "longer under load", §6), because the v12 README names two
`mid` editions the `chart` branch lacks. The PRD prices both windows as "the v12 hero under v11's text" and "the new
text over the old hero" (lines 444–448); it does not say that in each window some readers get no image at all.

That is 8 Oct 11:13, *"Merged but all images are unavailable"*, planned in advance, and it contradicts the PRD's own
rule at §7.4 line 370, *"The six editions are on the `chart` branch before `README.md` names them (8 Oct 11:13)"*,
which item 9 then admits holds "on the merge commit" (A) or "on the first run after the merge" (B) but not for the
page a visitor loads in the window.

Change, in two parts. **(i) Add order C and recommend it:** the first publish keeps the eight sheets `main` names
beside the six the report names, so no `<source>` on either README ever points at a missing file; then I merge at my
own pace, with no hour to keep to. Cost: one option in `publish_chart.py` (`--keep-current`: read the tree of the
current `chart` tip and stage its files first, then the report's over them; the commit stays parentless), one test
(`test_publish_keeps_main_sources`: every path `main:README.md` names is in the staged tree), and `unshipped()`
(`publish_chart.py:81`) run against both READMEs. The next weekly run after the merge republishes without `--keep`
and the four `still` and two old sheets go then, when nothing names them. **(ii) In the PRD:** §8.1 item 9 gains
order C as the recommended one, A and B keep their windows with the sentence "some readers see a broken image for
the window" added to each; §7.4's row says "held on the live page, not only on the merge commit, once C exists";
§10 gains a row (23: `--keep-current`, blocks the merge, a session); §9.0 (c) asks me for "yes to 2b" only, since
with C the order is no longer a choice I need to make.

Why: 8 Oct 11:13 is my sentence, and it is the only one in which I reported a thing that had already gone wrong on
the live page rather than a thing I disliked in a draft. A plan that knows it will repeat it for a window is not one
I want to see merged. The research this round agrees in a smaller way: popular projects' READMEs are "well organised
using lists and images" [S4], and the image is what a reader sees first (§2); a broken one is worse than none.

### MF2. The first half of my first sentence has no goal row (PRD text; §3 G1 line 96, G1b line 98, G1d line 100, §8.3 q.6 lines 490–494, appendix A line 767)

7 Oct 15:30 opens: *"This readme does not show an expert or high level smart person who has a massive interest in
design."* G1 quotes the second half of the message ("world class one of a kind beautiful profile readme...") and
G1b carries "what it says about the person who made it" as *measured figures, commands that were run, faults stated
with their fix*. That is the "expert" half. Nothing in §3 says where a reader sees "a massive interest in design",
and the page's answer to it is real and specific: the type system (a serif for the name, a tracked sans for the role,
a mono for code set at the word space, floors per edition), the night edition redrawn with heavier strokes and
lighter cuts rather than inverted (§5.2), the one pitch and one left edge (G3), the column measured on the live page
and written down (`DESIGN.md`, "GitHub's README column, measured on the live profile page on 10 Oct 2026"), and
the one `DESIGN.md` link, which sits in the provenance `<sub>` at the foot of the page (`README.md:151`, "The
[drawing](DESIGN.md) shows...").

Change: a row **G1e**, "does not show an expert or high level smart person who has a massive interest in design"
(7 Oct 15:30, the first half), meaning: *the design interest shows in how the page is made, not in ornament: three
faces with a reason each, night redrawn, one pitch, the column measured, and `DESIGN.md` one click from the page;
held by review*. §8.3 q.6's third line gains the words "and whether someone who designs for a living would see a
designer's hand, and where". Appendix A already carries the sentence whole; nothing else changes.

Why: it is the first thing I said, and it is the one that names what the old page failed at. "Expert" and "design"
are two claims, and the page proves them by two different means. The PRD prints the first and leaves the second to
be inferred from G1d's "the care shows".

### MF3. §9.2's recommendation on the agent-authorship counts rests on a sentence that is about something else, and the 2026 evidence is not beside it (PRD text; §9.2 lines 655–666, §9.0 (b) lines 557–559, §8.1 item 7 lines 427–431, G8 line 108)

The PRD asks me for one word, strike / keep / share, and recommends strike "on the owner lens", reading 9 Oct 11:35
(*"We don't need to show the commits are kind of cool. The data is kind of cool that we're pulling, but at the same
time, it feels lazy"*) as a rule against printing any commit figure. Read that message again as I said it: it is
about the v8 chart that *showed* the commits, as a picture, and called the picture lazy. The line in question
("coding agents (Claude) authored 45 of its 146 commits and co-signed 1 of his own 101", `README.md:38`) is a
disclosure of who wrote the code, which I have never named in any message; `docs/BEN-TODO.md` has asked me about it
since round 5 ("Strike it if you'd rather not") and I have not answered. So the recommendation is the agents'
reading, and the PRD says the opposite memos are "the agents' judgement, not his" while treating its own reading as
mine.

What the evidence this round says, none of it in the PRD: in 2026 the hiring-side guides want AI use named with the
tool and tied to shipped work, not hidden: "Name the specific tool you used, like Cursor, Claude Code, Copilot";
"Mention AI tool use in the context of work you actually shipped, not as a separate skills line"; what hurts is
"'AI-powered' or 'AI-driven' as buzzwords without specific work behind them" [S6]. CoderPad's 2026 survey of 650+
developers and hiring leaders: "The question isn't whether candidates use AI"; what is valued is "Catch and fix AI
mistakes" and "Explain trade-offs and correctness"; "Raw output alone is no longer a sufficient signal of skill"
[S7]. Revelo, September 2026: "85% of the vetted engineers surveyed use AI while shipping features" [S8]. And the
other side: developers "actively distrust the accuracy of AI tools (46%)" more than trust it (33%), 66 % name
"almost right" solutions as their top frustration, 45.2 % say debugging AI code takes longer [S2]. GitHub's own
Octoverse: "80% of new developers on GitHub use Copilot in their first week" [S1]. Put together: the risk a screener
weighs is not that agents wrote some commits, it is that the author cannot tell which, or hides it. The line as
printed is the former: the tool named, the count measured, the author's own commits counted apart (§7.3 row
"Agent-authored commits are counted apart and never as his").

Change: (a) §9.2 bullet 2: replace *"Recommended: strike (the owner lens)"* with *"Recommended: keep, as printed
(tool named, counts measured, his own apart); the strike reading of 11:35 is about the v8 picture of commits, not
this line, and the 2026 hiring guides read a named, measured disclosure beside shipped work as a positive signal and
vague or hidden AI use as the risk (sources in `docs/crit/prd/LOG.md`, round 5)"*, with the two sentences [S6] and
[S7] quoted in the cell and [S2]'s figures as the cost. (b) §8.1 item 7 keeps the switch (it is right that it exists
either way), but its default while I am silent follows the recommendation, so `agent_clause = true` until I say
"strike"; the item then no longer blocks the merge on its own, only on the switch existing. (c) G8's "Ruled on the
owner lens: off by default" becomes "ruled: on by default, the switch exists, his word reverses it". For the record,
my own word as this review's reader is **keep**; the PRD's rule is that only my word in a session counts, and this
is a reviewer writing in my lens, so (b) stays open until I say it there.

Why: 9 Oct 11:37, *"Talking about my commits. Talking about my work. That is what this should all be about"*, and 9
Oct 11:35, *"how is the data gathered?"*: the line answers both, and it is the one fact on the page a 2026 screener
will ask about first.

### MF4. Five PRD rounds, no product change, and the sentence that licenses the rounds is read as a mandate for more of them (PRD text and process; §0 lines 25–44, G19 line 883, §9.0 line 562–564, §10 lines 694–697)

`docs/crit/prd/LOG.md` records four rounds that applied 60-odd must-fixes to the document; reviewer 2's answer in
round 4 stands and is now five: no product file has changed since `027f081`. Meanwhile `main` serves the v11 map I
rejected on 9 Oct 20:50, its weekly job fails every Sunday (§8.5), and the three things that block the merge (§8.1
items 7 and 8, §10.19) are, by the PRD's own description, a switch read at one line (`render_readme.py:459`), five
keys and their dead modules, and two `fold = true` lines. G19 cites my 11 Oct sentence, *"Review and ensure this is
something I want to see rounds of reviews and research"*, as the rule for "the PRD itself is reviewed the same way".
Read it as I typed it: the object is *"something I want"*; the reviews and research are how you make sure of that,
and they are for the page, not for the register. A round that re-checks 56 line cites by hand (§0) while the page it
describes is not live is not what that sentence asks for.

Change: §0 gains a stop rule, one line: *"No PRD round 6 until a fix round has done §8.1 items 7 and 8, §10.19 and
MF1's `--keep-current`, and the branch has a PR (§10.17); the next PRD round then reads the document once against
the merged page."* G19's cell cites the 11 Oct sentence for "ensure this is something I want", and cites 9 Oct 20:50
("at least 10 reviews") for the count, which is already met (16 product rounds). §10's rule line (694–697) adds:
*"a row owned by 'a session' that blocks the merge is done in the next session before any further PRD round"*.

Why: 9 Oct 20:50, *"It should not be done until it goes over at least 10 reviews"*, is a floor on reviews of the
page, and the page has had 16; 8 Oct 09:04, *"all PRs need to be ready to merge"*, and this branch has none. The
PRD has reached the point where its remaining faults are in what it waits for, not in what it says.

### MF5. §9.0 (c) asks me to decide "what the top of the profile says" when nothing in (c) changes the top (PRD text; §9.1 title line 567, intro lines 569–573, §9.0 (c) lines 559–561)

§9.1 is titled "The one decision: what the top of the profile says about rustmapper 0.1.3" and opens with the box
and the six faults. The input it needs from me, (c), is yes or no to 2b, and 2b's first-screen cell reads "as today,
with the box". The image is identical under 0 → 2b → 3; only 1a and 1b change it, and those need a release. So the
decision I am asked for is about the second phone screen (four items open or six), and the PRD tells me so only in
the row's third column and in "The rows are not alternatives" five paragraphs down. Round 4 said the renders let me
decide; they do, once I know which two to compare.

Change: §9.0 (c) reads: *"Yes or no to 2b: the list under the image goes from six open items to four, the rest fold;
the image does not change (only a release changes it, §9.1 rows 1a/1b). Compare `renders/round-16/page-phone-2.png`
with `renders/once-2b/page-phone-2.png`. Then (with MF1's order C) nothing else."* §9.1's title becomes "The
decisions: what the page says about rustmapper 0.1.3, now and after a release", and its intro says in its first
sentence which rows a merge reaches and which a release does.

Why: 9 Oct 20:50, *"is it doing what I'm saying?"*: the PRD asks the right question of me and labels it with the
wrong thing, and on merge day I will read the label.

## 3. The goal rows against my sentences

§3 has 22 rows (G1–G1d, G2, G3, G3a, G4–G13, G13a, G14–G16); appendix D has G17–G19.

| Row | Missing, softened, or reinterpreted? |
|---|---|
| G1 | Held for the second half of 7 Oct 15:30; the first half has no row (MF2). q.6's first line is now a bar (round 4), right. |
| G1a | Held; I enlarged the gap and the hand-off line is on every sheet I opened. |
| G1b | Held. |
| G1c | Held; the 9 Oct trade is in my words. |
| G1d | Held; the third line of q.6 is the right home, and MF2 adds the design half to it. |
| G2, G5 | Held; `THEME_WORDS` is the 18 words (`route.py:60–61`, read). |
| G3, G3a | Held; my one sentence is in §1 above. |
| G4 | Held on the branch; §8.4 is mine after the merge; §9.1b default a stands. **Broken for a window of the live page by §8.1 item 9 as planned** (MF1): "The images are all crushed" was 8 Oct 14:22, "all images are unavailable" 8 Oct 11:13, and item 9 repeats the second. |
| G6 | Held under round 4's 2b (L2 and L6 open, checked on `once-2b/page-phone-2.png`). |
| G7 | Held; the strongest row. |
| G8 | Open on the page, blocking; **reinterpreted** in its ruling (MF3): 11:35 is read as a ban on a line it never named. |
| G9, G12 | Held on the branch. |
| G10 | Held; two winks, nothing bars a third. |
| G11 | Held; the retired strings block the merge (item 8). Not repeated. |
| G13, G13a | Held; the q.6 log works. |
| G14 | Held on the branch; §10.10 open; `BEN-TODO.md:39` still carries the thesis line for my bio (I read it; it is not something I will paste anywhere). |
| G15, G16 | Held. |
| G17, G18 | Done as process. |
| G19 | **Reinterpreted** (MF4): my 11 Oct sentence is cited as a reason for more rounds of the document; its object is "something I want". |

Nothing is missing from the page; one sentence is missing from the register (MF2); two rows read my words wider
than I said them (G8, G19).

## 4. The top of the page, as rendered

`sheet-phone-day-390.png`: my name; "CRAWL AND DATA INFRASTRUCTURE / PYTHON AND RUST"; "rustmapper" and its one
sentence; `pip install rustmapper` with `0.1.3 · 8 NOV 2025`; `rust_sitemap crawl` and what it starts from; the
fetch row with the loop bracket up the left; the red dotted box with the two catches; the Ctrl-C row; the file with
its field names; "sorted 21 ways by ideal-url-organizer". The night sheet is a redraw (heavier strokes, the thinner
cuts), not an inversion. The mid sheet at 746 has the same rows at one pitch. `page-phone-1.png`: the whole sheet,
the link line and "Ben Russell builds…" on one screen. `page-phone-2.png`: the pick, the facts line with the counts,
the platform note, "Before you run 0.1.3:" and three items. `page-desk-1.png`: all of that plus the six items, the
closed fold and the code block on one screen, its three comment lines wrapped at the phone's 32 columns (§11, §10.16).

Do I want strangers to see the top first? The sheet, yes. It is a page from a manual by someone who measured what he
wrote, and that is the right first impression for the readers §2 names. What I would change on it is sequenced and
I do not repeat it: the release date beside the install line and the two names for one tool (`rustmapper` on the
install line, `rust_sitemap crawl` on the next; the packaging spec makes the command name the entry point's name,
not the distribution's [S12], so this is one `[project.scripts]` line in Rust-sitemap, §5.4 row 6), and the
competence line a screen below the box. Two things the research this round adds, neither a must-fix: the README
studies find "What" and "How" common and "purpose and status" rare [S3], and early READMEs "favor brevity and
standardized instructions" [S5]; the page's "Ben Russell builds…" line and the CI date with its gates are the purpose
and status those READMEs lack, and they are on screens one and two. And the one guide that addresses a slowed
project says "put a note at the top of the README saying that development has slowed down or stopped" [S11]: the
page does the honest version of this by printing the release's own date beside the install line rather than a note,
and the date is eleven months old. Only a release changes that (§9.1), and I would rather a stranger read the date
than a sentence about it.

What is right and should stay: no stats card, no badge row, no first person, no "generated weekly" a visitor can
read, the fold of 15, "Also" and "Working rules" as the only headings, the `DESIGN.md` link once at the foot.

## 5. Research

### 5.1 What convinces a senior engineer or a hiring manager on a GitHub profile in 2026

Twelve sources read in full this round, none of them read by the round-3 or round-4 owner reviews (those used Built
In, Nexus IT, Underdog, TechInterview's profile piece, GreatFrontEnd, NN/g, Bargas-Avila, Spiegel, StatCounter,
F1 Jobs, Reczee, Noon, Rockstar, OpenSSF, Snyk, JHU, Apache UIMA, Adam Grant). Where they bear on the page:

1. **The reader's question has moved from "can he code" to "can he tell what the machine got wrong".** CoderPad,
   650+ developers and hiring leaders, March 2026: "The question isn't whether candidates use AI"; the behaviours
   valued are "Catch and fix AI mistakes", "Explain trade-offs and correctness", "Improve AI output through
   iteration"; "Raw output alone is no longer a sufficient signal of skill" [S7]. TechInterview, May 2026: name the
   tool, tie it to shipped work, and "Resume integrity matters in the AI era because the depth of follow-up questions
   has increased" [S6]. Revelo, September 2026: 85 % of its vetted engineers "use AI while shipping features" [S8].
   The page's answer is the facts line (MF3) and the "Before you run" list: each item is a fault the author found in
   his own tool, with its probe. That is "catch and fix mistakes" shown, not claimed.
2. **Trust in AI output is falling while use rises**, so a reader will want to know who wrote what: 84 % use or plan
   to use AI tools; 46 % distrust their accuracy against 33 % who trust it; 66 % name "almost right" as the top
   frustration [S2]. Octoverse: 180 million-plus developers, "80% of new developers on GitHub use Copilot in their
   first week", and "Key repository files like README or a LICENSE file are more than formalities", with ~63 % of
   public repositories carrying a README [S1]. Nothing in Octoverse says how developers read profiles or by what
   device; the PRD's "phone the stricter constraint, web the likelier reader" stays my sentence, not a measured share.
3. **What a README is for, measured.** Prana et al., 4,226 sections from 393 repositories: "What" and "How" are
   common; "many README files lack information regarding the purpose and status of a repository" [S3]. Venigalla and
   Chimalakonda, 1,950 READMEs: popular projects' READMEs are "well organised using lists and images" and link out
   [S4]. Gaughan et al., 2025: first READMEs "favor brevity and standardized instructions" [S5]. The page is one
   image, lists, and links out to the two projects, PyPI and the tools' own READMEs; its purpose line and CI status
   are the two things the studies say are usually missing.
4. **Length.** "too long is better than too short", with the advice to move surplus into other documentation rather
   than cut it [S11]. The page's fold of 15 and the `DESIGN.md` link are that move.

### 5.2 Do a tool's known faults on its author's own profile help or hurt?

Rounds 1 to 4 covered two-sided messages, blemishing, the pratfall effect, Spiegel's review-rating curve and the
Harvard weakness study, and settled the shape of the list (short, after the positive, each item with its fix). This
round's sources add one point and one warning:

- **In 2026 the admitted fault is the signal.** When hiring teams assess "debugging AI-generated code" and valuing
  those who "Catch and fix AI mistakes" [S7], a list of measured faults in one's own release, each with its flag and
  its probe, is the profile-page form of that assessment. The stop rule in the box ("0.1.3 never exits by itself;
  quit when `Received work item` lines stop for 60 s") is exactly the kind of "almost right" behaviour [S2] a reader
  will have met in their own tools; stating it with the sign to watch for reads as the author having done the
  debugging.
- **The warning is unchanged: the fault must not read as abandonment.** The one guide that addresses it says to put
  a note at the top when development has slowed [S11]; the page's equivalent is the eleven-month-old date beside the
  install line, three days from a green CI date one screen down. The honest fix is the release, and the PRD
  sequences it (§9.1 1a). Nothing in the text should try to do it.

So: faults on the author's own profile help when measured, levered and beside the claim, and in 2026 they help a
little more than they did, because the reader's question has become whether you can find them. The page does this;
2b keeps it on the first two screens; what it must not do is appear under a broken image (MF1).

### 5.3 Two facts re-checked

- The HTML spec on a chosen `<source>` whose fetch fails: "choose one image source from sourceSet"; an image whose
  fetch obtains no data is "broken"; no step retries the next source [S10]. MDN agrees by silence: selection by
  `media`, `srcset`, `type` only, and the `<img>` fallback is for "no matches", not for a failed load [S9]. This is
  the mechanism behind MF1.
- `console_scripts`: "the name of the entry point should be usable as a command in a system shell after the package
  is installed"; nothing requires it to match the distribution name [S12]. So `rustmapper` as the command is one
  entry in `[project.scripts]`, as §5.4 row 6 and §11 say.

## 6. What I checked and found correct, and what drifted

| PRD claim | Checked | Holds |
|---|---|---|
| no product file changed since `027f081` | `git diff --stat 027f081..HEAD -- . ':!docs'` at `0a557ff`: empty | yes |
| `main`'s README names four `hero-*-still-*` editions; the branch's names six with `mid` | `git show main:README.md` lines 6–13; `README.md:7–13` | yes |
| `publish_chart.py` ships only what the report names, one parentless commit | docstring lines 6–9; argparse lines 155–160 (no keep option) | yes |
| `[position] text`, `[contact]` are `""` | `chart.toml:26, 30–31` | yes |
| five retired `[copy]` keys at `chart.toml:35–39` | read | yes |
| `agent_clause(r)` called unconditionally | `render_readme.py:459` | yes |
| POSITION-EMPTY warns at `position.py:31` | read | yes |
| THEME_WORDS = 18 words | `route.py:60–61` | yes |
| `runcheck.py:8` "probes four behaviours" | line 8 | yes (§10.18 open) |
| G1a's gap in the track under the box | enlarged crops of the phone and desk sheets | yes, visible at phone size |
| the 2b render: four items, the fold closed | `once-2b/page-phone-2.png` | yes |
| `DESIGN.md` linked once, from the provenance line | `README.md:151` | yes |
| `BEN-TODO.md:39` still carries the thesis line | read | yes (§10.10 open) |
| 22 rows in §3, three in appendix D | `grep '^| G' docs/PRD.md` | yes (the brief's "19" is off) |

No line cite I printed had drifted this round.

## 7. Score

**7 / 10.** The PRD is the one honest record of my rules and who owns each gap, and from it and the renders I can say
yes to 2b. It does not go higher because the merge it plans would repeat the one failure I reported from the live
page, and its own §7.4 rule says so if read against item 9 (MF1); because the first half of my first sentence has no
row (MF2); because the one word it asks of me is recommended on a reading of my words I do not recognise, with none
of this year's evidence beside it (MF3); because it has become a document that is reviewed instead of a page that is
merged (MF4); and because the decision label on merge day is the wrong one (MF5). Do MF1 and the three blocking
items, open the PR, and I merge 2b.

## Sources

Outside, read in full this round:

1. GitHub, "Octoverse: A new developer joins GitHub every second as AI leads TypeScript to #1" (28 Oct 2025, updated
   28 Feb 2026), https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-TypeScript-to-1/
   — read: "180 million-plus developers"; "80% of new developers on GitHub use Copilot in their first week"; "~63% of
   public repositories include a README"; "Key repository files like README or a LICENSE file are more than
   formalities"; nothing on how profiles are read or on device.
2. Stack Overflow, 2025 Developer Survey, AI section, https://survey.stackoverflow.co/2025/ai — read: "84% of
   respondents are using or planning to use AI tools"; "More developers actively distrust the accuracy of AI tools
   (46%) than trust it (33%)"; 66 % "almost right, but not quite"; 45.2 % "Debugging AI-generated code is more
   time-consuming".
3. Prana, Treude, Thung, Atapattu, Lo, "Categorizing the Content of GitHub README Files", Empirical Software
   Engineering 24(3), 2018, https://arxiv.org/abs/1802.06997 — read: 4,226 sections, 393 repositories; "What" and
   "How" very common; "many README files lack information regarding the purpose and status of a repository".
4. Venigalla, Chimalakonda, "An Empirical Study On Correlation between Readme Content and Project Popularity"
   (2022), https://arxiv.org/abs/2206.10772v1 — read: 1,950 READMEs, ten languages; popular projects' READMEs "well
   organised using lists and images", link to external sources.
5. Gaughan, Champion, Hwang, Shaw, "The Introduction of README and CONTRIBUTING Files in Open Source Software
   Development" (2025), https://arxiv.org/abs/2502.18440v1 — read: "projects create minimal READMEs proactively";
   first versions "favor brevity and standardized instructions".
6. TechInterview, "AI-Era Resume Framing: How to Position AI Tool Fluency in 2026" (4 May 2026, updated 13 Jul 2026),
   https://www.techinterview.org/post/3233474934/ai-era-resume-framing-2026/ — read: "Name the specific tool you
   used, like Cursor, Claude Code, Copilot"; "Mention AI tool use in the context of work you actually shipped";
   buzzwords "without specific work behind them" hurt; "Resume integrity matters in the AI era because the depth of
   follow-up questions has increased".
7. CoderPad, "New Research: The 2026 State of Tech Hiring" (11 Mar 2026), https://coderpad.io/blog/hiring-developers/new-research-the-2026-state-of-tech-hiring-what-ai-means-for-developers-and-hiring-teams/
   — read: 650+ respondents; "The question isn't whether candidates use AI"; "Catch and fix AI mistakes"; "Explain
   trade-offs and correctness"; "Raw output alone is no longer a sufficient signal of skill"; vendor source, no
   method stated.
8. Revelo, "How AI Is Changing How US Companies Hire Software Engineers in 2026" (9 Sep 2026),
   https://www.revelo.com/blog/how-ai-is-changing-how-us-companies-hire-software-engineers-in-2026 — read: "85% of
   the vetted engineers surveyed use AI while shipping features"; nothing on GitHub or README review; vendor source.
9. MDN, `<picture>`, https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/picture — read: "choose
   the best match among them. If no matches are found [...] the URL of the `<img>` element's `src` attribute is
   selected"; selection by `srcset`, `media`, `type`; nothing on a failed load.
10. WHATWG HTML Living Standard, "Images" (selecting an image source; updating the image data),
    https://html.spec.whatwg.org/multipage/images.html — read: "choose one image source from sourceSet"; the Broken
    state where "no data could be obtained"; no step retries another source after a failed fetch.
11. Make a README, https://www.makeareadme.com/ — read: "too long is better than too short"; "Use examples liberally,
    and show the expected output if you can"; for a slowed project "put a note at the top of the README saying that
    development has slowed down or stopped completely".
12. Python Packaging User Guide, "Entry points specification",
    https://packaging.python.org/en/latest/specifications/entry-points/ — read: `console_scripts`; "the name of the
    entry point should be usable as a command in a system shell after the package is installed"; the command name is
    the entry point's, not the distribution's.

Searched but not opened in full (403 / 410, or snippets only): Instahyre's GitHub profile checklist; FOSShub's README
resource; the Noei & Lyons Java README study (catalog entry); arXiv 2312.03819 and 2010.02472.

In the repository and the session, read this round:

13. `/home/user/wt-v12/docs/crit/prd/owner-messages.md` — all 21 messages, twice.
14. `/home/user/wt-v12/docs/PRD.md` at `0a557ff` — whole.
15. `/home/user/wt-v12/docs/crit/prd/LOG.md` — rounds 1–4.
16. `/home/user/wt-v12/docs/crit/prd/review-r04-1.md` — whole, so nothing here repeats it.
17. `/home/user/wt-v12/README.md`; `git show main:README.md` lines 6–13.
18. `/home/user/wt-v12/scripts/publish_chart.py` — docstring, `unshipped()` at 81, argparse at 155–160.
19. `/home/user/wt-v12/scripts/render_readme.py:43–52, 455–465`; `scripts/checks/position.py:28–36`;
    `scripts/checks/route.py:55–61`; `scripts/runcheck.py:1–12`; `chart.toml:20–39`.
20. `/home/user/wt-v12/DESIGN.md:1–30`; `/home/user/wt-v12/docs/BEN-TODO.md`.
21. Renders: `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/`
    `sheet-phone-day-390.png`, `sheet-phone-night-390.png`, `sheet-desk-day-870.png`, `sheet-mid-day-746.png`,
    `page-desk-1.png`, `page-desk-2.png`, `page-phone-1.png`, `-2.png`, `-3.png`;
    `/home/user/wt-v12/docs/crit/prd/renders/once-2b/page-phone-2.png`; my crops `scratchpad/gap-crop.png`,
    `gap-crop-desk.png` (PIL, nearest-neighbour, ×4).
22. `git diff --stat 027f081..HEAD -- . ':!docs'` (empty); `grep -c '^| G' docs/PRD.md` (26 rows, 22 in §3).
