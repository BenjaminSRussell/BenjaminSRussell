# PRD review round 6, reviewer 1: Ben, the owner, reading the PRD as the person who has to live with the page

11 Oct 2026. Document under review: `docs/PRD.md` at `b6cca2c` (933 lines, 20,277 words by `wc`, as its header
says). Product at `027f081`; `git diff --stat 027f081..HEAD -- . ':!docs'` is empty, so the renders under
`scratchpad/r6/build/round-16/` and `docs/crit/prd/renders/round-16/` are the product this document describes. I read
`owner-messages.md` twice, the PRD whole, every render named in the brief, `README.md`, `chart.toml:24–39`,
`render_readme.py:459, 925`, `publish_chart.py` (no `--keep-current`), the `hero-*` group ids in
`assets/v9/hero-phone-day.svg`, the PyPI record for rustmapper, the remote's refs and PR list, and
`docs/crit/prd/LOG.md` rounds 1–5 so as not to repeat a fixed finding. `python3 -m unittest`: 539 tests, OK, 21.6 s.

## 1. Is the product this PRD defines what I asked for?

**Yes.** The sentence that decides it is 9 Oct 20:50: *"How does it help the user see my project? What is it
showing? [...] My goal is to have a purpose behind each map. Every single, not even just maps. Everything, single
thing inside of this needs a purpose, not a fucking chasing a reason."* The image is the way into rustmapper and
nothing else: fifteen `hero-*` groups in the phone SVG (T1, T2, R0, R1, R2, R5, R6, S1, F1, H0, H1, C1, R12, R13,
R15), each with a row in §5.1 saying what a stranger learns and from which file, and the two undrawn rows (S2, W1)
say why they are not drawn. That is a purpose per thing, not a reason chased. The sentence that says what the page
is *for* is 9 Oct 11:37: *"It should be telling you about me, but with a layer of a theme of shipping. [...] It has
to be helpful knowledge."* The route is helpful knowledge (install, start, what it contacts, where it stalls, how to
stop it, what file you get, which tool reads it next); the manner is in the track, the dotted line and the paper, and
no word names it (G2, G5, G9, G10, G12 all hold on the renders: I looked for a ship, a rose, a legend, a themed
heading or a pirate word and found none).

**My one sentence for G3a** (§8.3 q.1's first line; I had read §1 before I looked, as every PRD reviewer has, and I
say so): *"A crawler called rustmapper: pip-install it, run it on a URL, it loops over pages, on https it can hang
behind robots.txt and the release never stops by itself, so you press Ctrl-C once and get a JSONL of URLs that
another of his tools sorts."* Tool, start, output. Log it against G3a.

**Would I screenshot the image and send it?** Yes: "how you get into my crawler" (as rounds 3, 4 and 5; log for
G13a). The gap in the track under the box is real at phone size: I cropped `sheet-phone-day-390.png` at 4× and the
magenta line stops at the loop's foot and starts again above the Ctrl-C ring with cream between (G1a). Made with
care (G1d, G1e): the name in a serif over a tracked sans, the release's own date set small beside the install line,
the real field names in the mono, night redrawn with heavier strokes rather than inverted (compare
`sheet-desk-day-870.png` with `sheet-desk-night-870.png`: the dotted box and the rings are heavier, not the same
pixels on a dark ground).

So the product is what I asked for, and the condition is the same as in rounds 1 to 5: it is not live. Which is
where my 11 Oct sentence comes in, and why this round's first must-fix is about the rounds.

## 2. Must-fixes, ranked

Each: where (section, line of `docs/PRD.md` at `b6cca2c`), what to change, why (my words or a source), and whether
it is about the PRD text or the product it defines.

### MF1. This round ran against the PRD's own stop rule, and two of the three code items it waits on change nothing a visitor sees (PRD text and what it blocks; §0 lines 42–48, §8.1 items 7–8 lines 428–437, §10 rows 5 and 8 lines 736 and 739, G19 line 918)

§0 line 44: *"Stop rule: no PRD round 6 until a fix round has done §8.1 items 7 and 8, §10.19 and §10.23 and the
branch has a PR."* I checked each: `grep agent_clause chart.toml` finds nothing (item 7 not done); `chart.toml:35–39`
still carries `unit_chart`, `unit_hero`, `unit_approaches`, `limit_label`, `footer_line` (item 8 not done);
`chart.toml` has `fold = true` at lines 1257, 1276, 1308, 1357 only, none on L4 or L5 (§10.19 not done);
`grep keep-current scripts/publish_chart.py` finds nothing (§10.23 not done); the remote has zero PRs from
`v12/purpose` in any state (§10.17 not done). Round 6 is running anyway. That is the answer to my 11 Oct sentence,
*"Review and ensure this is something I want to see rounds of reviews and research"*: the product, yes; a sixth
round of reviewing the document while `main` serves the map I rejected on 9 Oct, no. A rule the process ignores is
not a rule, and the PRD cannot enforce it from inside a document, so the fix has to make the blockers small enough
that the next session clears them before it can do anything else.

Two of the three blockers are the wrong trade on my own lens, and I reverse round 2's ruling (made on this lens)
the way round 4 reversed item 6:

- **Item 7, the `[facts] agent_clause` switch.** Since round 5 the default is *keep*, which is what prints today
  (`README.md:38, 86`). A switch whose default reproduces the page as it is changes nothing on the merge commit. It
  is needed on the day I say "strike" or "share", not before. Move it to §8.5 (after merge; a session, the week I
  answer (b)). §9.0 (b) stays as it is.
- **Item 8, the five `[copy]` keys and the retired modules.** Nothing on the page reads them (`build_assets.SHEETS =
  ["hero"]`; the PRD says so itself at §7.1 line 305). My rule, 8 Oct 14:52, is about what the user is shown. A
  string in a config file no visitor opens does not break it. Deleting 91 tests and five modules is housekeeping,
  and housekeeping does not outrank row 0's cost ("every week undecided keeps up a page that breaks G8, G13, G14,
  G15"). Move it to the first fix PR after the merge.
- **§10.19 (two `fold = true` lines) and §10.23 (`--keep-current`) stay**, because the first changes what the second
  phone screen shows (my yes to 2b) and the second is 8 Oct 11:13, *"Merged but all images are unavailable"*, which
  I will not see twice.

Change: §0's stop rule reads *"The next session is the fix round: §10.19, §10.23, the PR (§10.17), then Ben's yes.
No PRD round runs before the merge; the first after it reads the document once against the live page."* §8.1 items
7 and 8 become one line each pointing at §8.5 and §10; §10 rows 5 and 8 read "Blocks: nothing; after merge". G19's
cell keeps the sentence and adds that round 6 ran against the rule, so the log shows it. Also: §0 and §10 carry the
honest count, six PRD rounds, no product change.

Why: 9 Oct 20:50, *"It should not be done until it goes over at least 10 reviews"*: the page has had 16. 8 Oct
09:04, *"all PRs need to be ready to merge"*: this branch has none. 11 Oct, *"ensure this is something I want"*: the
object is the page, and the page is not live.

### MF2. §9.1 costs every option by the first *phone* screen, when my words make the web the likelier reader, and on the web the whole fault list is on screen one beside the image (PRD text; §9.1 table lines 617–624, intro lines 602–606; §2 lines 89–92)

§2 quotes me: *"If they're looking at your repos, it's definitely on the web"*, and states the rule: *"the phone
the stricter constraint, the web the likelier reader."* §9.1's table then has one column, "What the first screen
says", and every cell in it is the 390 px phone. I opened `renders/round-16/page-desk-1.png` (1,280 px): the image,
the link line, "Ben Russell builds…", the pick, the facts line, the platform note, **all six "Before you run 0.1.3"
items**, the fold's summary and the top of the code block are on the first screen. I opened
`renders/once-2b/page-desk-1.png`: the same with **four** items. So for the reader I said is likelier, 2b against 3
is four faults against six on the first screen, beside the image and under the facts line, and the PRD's own
phrase for that, *"a warning label on his flagship"* (line 604), is truer of the desk than of the phone it costs.
The decision is still 2b (four items, each the text of a mark on the image or its lever, is the best the page can
do without a release), but I am being asked to decide it on the wrong screen.

Change: the column becomes two, "First phone screen (390)" and "First desk screen (1,280)", and the desk cell is
filled from the committed renders for rows 0 (the v11 page), 2b and 3; §9.0 (c) adds `renders/round-16/page-desk-1.png`
against `renders/once-2b/page-desk-1.png` to the pair it tells me to compare. §2's sentence then has a consequence
in the one table where my decision lives.

Why: 9 Oct 11:32, quoted above, and 9 Oct 20:50, *"is it doing what I'm saying?"*: the PRD says the web is
likelier and then prices only the phone.

### MF3. The reason given for the missing PR is false: the branch is already on the remote (PRD text; §10.17 line 748, appendix D line 925, §0 line 43)

§10.17: *"the fix passes do not push, so a session with push does it, or Ben"*; LOG round 2 declined opening the PR
because *"a PR needs the branch on the remote."* `git ls-remote --heads origin v12/purpose` returns `9e3db34`, the
commit after `027f081` (the first PRD commit); `git branch -r --contains 027f081` lists `origin/v12/purpose`. Every
product file is on the remote; the five local commits ahead of it are the PRD rounds (`git log --oneline
9e3db34..HEAD | wc -l` = 5), docs only. A PR for the product could have been opened in round 1 with no push at all,
and `gh api repos/…/pulls?state=all&head=BenjaminSRussell:v12/purpose` returns 0: none ever was.

Change: §10.17 reads *"the branch is on `origin` at `9e3db34` with every product file; `gh pr create --head
v12/purpose` needs no push; the fix round opens it first, before any code change, so the PR is the place the four
items land."* Appendix D's row drops "the fix passes do not push" as the reason.

Why: 8 Oct 09:04, *"all PRs need to be ready to merge"*; a PR that was possible for five rounds and not opened for a
reason that was not true is the kind of thing I asked the rounds to catch.

### MF4. G8's meaning column still says "no commit total printed, of any kind" while its holder and §9.2 keep two of them on the page by default (PRD text; G8 line 116, §4 line 129)

Round 5 ruled keep. G8's meaning cell was not rewritten with it: it opens *"no commit activity drawn; no commit
total printed, of any kind"* and closes *"on by default"*. The facts lines print "45 of its **146** commits" and "71
of its **499** commits" (`README.md:38, 86`; `page-phone-2.png`): those are commit totals. §4's first bullet, "No
stars, followers, streaks, commit totals (the provenance-line test, §5.3 row 12)", is true of the provenance line
and false of the facts line two screens up. A reader of §3 and §4 alone would say the page breaks G8; it does not,
by the ruling the same document makes at §9.2.

Change: G8's meaning: *"no commit activity drawn; no commit total on the image or in the provenance line; the facts
lines' agent-authorship clause (which names each repository's commit count) prints by default and his word
reverses it (§9.2, §9.0 (b))."* §4: *"No stars, followers, streaks, activity graphs, language pie; no commit total
except inside the agent-authorship clause of the facts lines (G8)."*

Why: 11 Oct 01:12, *"review all of the do and donts and specifically all of the rules that must be followed and
review how they are implemented"*: a rule that says one thing and is implemented as another is the case that
sentence names. On (b) itself I do not reverse round 5: both my sentences stand, the 2026 hiring-side sources §9.2
quotes say name the tool beside shipped work, and that the owner lens went strike in rounds 1–2 and keep in round
5 is itself a sign the rounds have exhausted what the text can settle. It is my word, in a session.

### MF5. "Is it interesting, does it draw in the user" has no home (PRD text; G1b line 105, §8.3 q.6 line 481)

G1b quotes 7 Oct 17:40 whole, then its meaning keeps only the second half, *"what it says about the person who made
it"*. "Interesting" and "draw in" are a different test: not what a stranger learns, but whether the first screen
makes them scroll to the second. Nothing in §8.3 asks it. q.6 asks for a screenshot (stunning) and q.4 asks what the
first two screens tell (informative); neither asks what on screen one made the reviewer go on.

Change: G1b's meaning gains *"and screen one makes a stranger scroll"*; §8.3 q.6 gains a fourth line, advisory:
*"what on the first screen made you scroll to the second; if nothing, say so."* No gate, no test, said so.

Why: 7 Oct 17:40 in my own words; and Underdog's June 2026 line, *"make an initial call in a very short review
window"* [S1]: the window is screen one, and the page's job there is to buy screen two.

## 3. The goal rows against my sentences

I tested every row of §3 (23 rows: G1, G1a–e, G2, G3, G3a, G4–G16, G13a) against the message it cites. Held as
said: G1, G1a, G1c, G1d, G1e, G2, G3, G3a, G4, G5, G6, G7, G9, G10, G11, G12, G13, G13a, G14, G15, G16. Softened or
inconsistent: G1b (MF5), G8 (MF4). Reinterpreted: none. Missing: nothing I typed is without a row, counting
appendix D's G17–G19 for how the work is done; appendix A's 21 messages match `owner-messages.md` (I counted the
headings). On G19 the document reads my 11 Oct sentence correctly (the object is the page); the process did not
(MF1).

## 4. The decision in §9.1, as I would frame it

The question I face is one: **merge this week with the box and six-or-four cautions, or wait for 0.1.4.** The PRD
answers it the way I would: merge 2b now, because a release retires the box on its own and a merge costs nothing a
release would undo (lines 626–643), and row 0 says what every week of waiting costs. The renders it tells me to
compare exist in the repository (`renders/round-16/`, `renders/once-2b/`: I listed them). What it does not do is
price the desk (MF2), and what it still waits on is partly not worth waiting for (MF1). §9.1b (the mid window): a,
accept; no device I named sits there. §9.0 (a): mine, after the merge. §9.0 (d): mine, after the merge.

## 5. The top of the page, as rendered

`sheet-phone-day-390.png`: my name; the role; "rustmapper" and one sentence; `pip install rustmapper` with
`0.1.3 · 8 NOV 2025`; `rust_sitemap crawl`; the fetch row with the loop bracket; the red dotted box; the Ctrl-C row;
the file with its field names; "sorted 21 ways by ideal-url-organizer". `page-phone-1.png`: the sheet, the link
line and "Ben Russell builds…" on one screen; `page-phone-2.png`: the pick, the facts line, the platform note and
three cautions; `page-phone-3.png`: three more, the fold, the code block. `page-desk-1.png`: all of it on one
screen (MF2). The night sheets are redraws. The mid sheet at 746 has the same rows at one pitch.

Do I want strangers to see the top first? The sheet, yes: it reads as a page from a manual written by someone who
ran what he wrote. The two things I would change are sequenced and not must-fixes: the date beside the install
line is eleven months old and will be older each week (PyPI: four releases, the last 8 Nov 2025, nothing since; I
fetched the JSON), and one tool has two names on the first screen. Only a release changes either (§9.1 rows 1a, §11).
The research below gives me one more reason to cut it soon, in §6.2.

What is right and stays: no stats card, no badges, no first person, no schedule line a visitor reads, "Also" and
"Working rules" as the only headings, the fold of 15, one `DESIGN.md` link at the foot.

## 6. Research

### 6.1 What convinces a senior engineer or a hiring manager on a GitHub profile in 2026

The 2026 guides agree with each other and with the page, and none of them is data: they are recruiter and
practitioner writing, and I weight them as such.

- Underdog (19 Jun 2026) [S1]: *"The profile itself tells me whether you understand presentation, judgment, and
  prioritization"*; *"A pinned repository is your headline artifact"*; *"Four polished projects beat six random ones
  every time"*; *"A weak README forces the reviewer to do detective work"*; *"Honest failure states and useful
  messages beat happy-path demos"*; comments should capture *"why a trade-off was chosen."* The page's facts line
  (CI date and gates, test count, what it is built on) and the three working rules with their cites are the
  "why" and "judgment" lines; the fold of 15 against four named projects is "four polished, not six random".
- TechInterview, "GitHub Profile Polish for Engineers" (updated 30 Jun 2026) [S2]: *"Profile page loads. They see:
  profile picture, bio, pinned repositories, contribution graph"*; *"Total time: 30–90 seconds"*; a profile README
  should hold *"a 2–3 sentence description of who you are and what you work on"*, a pinned list with context, and
  it advises against *"animated GIFs, visitor counters, long technology lists, and excessive emoji"*; the graph is
  *"a coarse activity signal, not as a primary evaluation factor"*; *"Don't fabricate side projects to fill the
  profile; recruiters can tell."* The page has the sentence ("Ben Russell builds…"), no GIF, no counter, no graph.
- GreatFrontEnd (20 Jul 2026) [S3]: *"In the first minute, a recruiter should understand your target role"*;
  *"Keep badge rows, stats cards, contribution snake animations, and long tech-icon grids out of the top section"*;
  *"Do not use all six just because the slots exist"*; *"If your best work is private, do not fake it."* The role
  line is on screen one; §4's non-goals are this list.
- BuiltIn, four companies [S4]: Raise's VP wants code *"readable, well-formatted, well-tested, well-documented"* and
  *"a pragmatic approach via the commit history"*; CapTech's recruiter wants *"activity"*; Mac & Mia says *"not
  everyone spends their free time programming."* The one reader here who counts activity is the one the page
  gives least to, by my rule (G8), and I accept that.
- Pin, "GitHub recruiting" (updated 30 May 2026) [S5], citing Octoverse 2024 [S6]: *"82% of GitHub contributions
  happen in private repositories"*, so *"Just 18 percent is public, which is all recruiters can access"*; *"A pinned
  project last updated three years ago tells a different story than one with commits from last week"*; *"Clear
  documentation, setup instructions, and architecture explanations signal communication skills."* Octoverse itself
  [S6]: *"More than 82% of GitHub contributions are made to private repositories"*; *"Python becomes the most used
  language on GitHub"*; *"Rust continues to gain popularity."* The page's facts line prints the HEAD sha and the CI
  date, which is the recency signal Pin names, and the role line is the two languages Octoverse names.
- CoderPad, "The 2026 State of Tech Hiring" (11 Mar 2026, 650+ respondents) [S7]: hiring leaders value candidates
  who *"Explain trade-offs and correctness"* and *"Catch and fix AI mistakes"*; *"Raw output alone is no longer a
  sufficient signal of skill."* This is the case for keeping the agent-authorship clause (§9.2) and for the
  working rules, which are trade-offs explained.
- GitHub docs, "Managing your profile README" [S8]: *"You can add a README to your GitHub profile to tell other
  people about yourself"*; the template is *"to give you some inspiration"*. No required content. The page's
  choice to make it a manual page rather than a bio is permitted and unusual, which is G1's "one of a kind".

What this adds to the PRD: nothing it contradicts, and one thing it sharpens. Every guide puts the role and the
"what he builds" sentence in the first seconds; the page does, on the image and the line under it. Every guide
wants fewer, finished things; the page names two tools and four more, and folds fifteen. The screen that buys the
second (MF5) is the one these sources describe and the PRD does not test.

### 6.2 Do a tool's known faults on its author's own profile help or hurt?

- Ein-Gar, Shiv and Tormala, "When Blemishing Leads to Blossoming", *Journal of Consumer Research* 38(5), 2012
  [S9]: *"people will be more favorably disposed to a product when a small dose of negative information is added"*,
  and the effect holds *"when the information is processed effortlessly rather than effortfully"* and *"when the
  negative information follows rather than precedes positive information."* Two conditions, and the page meets one:
  the faults are read effortlessly (one line each, a lever on the line). It fails the other on the phone: the box
  ("never exits by itself") is on screen one inside the image, and the positive (CI passed, 176 tests, 16k lines) is
  on screen two. That is negative-before-positive, the order the paper says does not blossom. Not a must-fix: the
  box is true of the release and 1a retires it; it is one more reason the release is worth cutting soon, and I put
  it in §5 above rather than in the PRD.
- Sage, *Encyclopedia of Health Communication*, "Message sidedness" [S10]: *"two-sided refutational messages were
  demonstrated to be the most persuasive across topics and contexts"*; one-sided beat two-sided nonrefutational. The
  page's list is refutational where an item carries its lever (L1 `--workers 1`, L7 `--user-agent`, L2
  `--seeding-strategy none`) and nonrefutational where it does not (L4, L5; L6 gives the sign, not a fix). 2b opens
  the refuted ones and folds two of the unrefuted ones, which is what this literature would do; that is why 2b is
  right and 3 is not, and §9.1 already says so with the same sources.
- Rust issue #34057 (3 Jun 2016, still open) [S11]: a standard way to document known bugs *"could prevent
  unnecessary bug reports"* and *"encourage dialogue about known limitations."* The stated faults are the issues a
  first user would otherwise file against the author in public.
- NuGet, "Write a high-quality README" [S12]: *"Start with a clear and concise description of what your package is
  and does, and what problem it solves"*; *"note any installation prerequisites or setup, then walk through real
  examples"*; *"Provide information on how to troubleshoot common issues."* The page's order is this order.
- OpenSSF Scorecard, Maintained check [S13]: top score needs *"at least one commit per week over the previous 90
  days"*; *"A project which is not active might not be patched, have its dependencies patched, or be actively tested
  and used."* The page's facts line shows the repository is active (CI 7 Oct 2026 at `32c2651`); the install line
  shows the *release* is not (8 Nov 2025). A reader who knows Scorecard reads both; the honest fix is the release,
  not a sentence.
- Underdog [S1] again: *"Honest failure states and useful messages beat happy-path demos."*

Verdict on the question: stated faults with their fix beside them help; stated faults without a fix, before the
positive, hurt a little; faults on the author's own page are read as the author's judgment, not the tool's weakness,
when the page also shows the author measured them (the provenance line: "its commands were run"). The page is on
the right side of each of these except the order on the phone, which a release fixes.

## 7. What I checked and found correct, and what drifted

Correct: 28 plug-ins (`ls scripts/checks/*.py | grep -v __init__ | wc -l`); 539 tests pass; the header's line and
word counts (`wc -l -w docs/PRD.md` = 933, 20,277); 21 messages in `owner-messages.md`; 15 drawn `hero-*` groups
plus S2 and W1 undrawn = §5.1's 17 rows; six editions in `assets/v9/`; `README.md:7–13` names six sources and no
`still`; `origin/main` at `d253286` names four `prefers-reduced-motion` sources (`grep -c` = 4), as §8.6 says; the
four `fold = true` lines at `chart.toml:1257, 1276, 1308, 1357`; `render_readme.py:459` calls `agent_clause(r)`
unconditionally; PyPI's last release 2025-11-08T19:52:41; the renders §9.1 cites exist at the paths it gives.

Drifted: §10.17's reason (MF3); G8's meaning after round 5's ruling (MF4); the stop rule, by the process (MF1).

## 8. Score

**6 / 10.** The text is the best it has been: every rule I set has a row, a holder and a line in the code, the
decision I have to make is one word, and the renders it asks me to compare are in the repository. I take a point
off from round 5's seven because the document's one job now is to get the page I want in front of strangers, and
it has spent a sixth round on itself while blocking the merge on a switch that changes nothing and on dead code
(MF1), and because the one table where my decision lives prices the reader I said was less likely (MF2). Fix MF1
and MF3 in the next session, before anything else, and this document is done until the page is live.

## Sources

Outside, read with WebFetch on 11 Oct 2026:

1. [S1] Underdog, "What Hiring Managers Look for on GitHub: Land Your 2026 Job", 19 Jun 2026,
   https://underdog.io/blog/what-hiring-managers-look-for-on-github
2. [S2] TechInterview, "GitHub Profile Polish for Engineers: Pinned Repos, READMEs, What Recruiters Click On",
   updated 30 Jun 2026, https://www.techinterview.org/post/3233474626/github-profile-engineers/
3. [S3] GreatFrontEnd, "Frontend Developer GitHub Profile: How to Stand Out to Recruiters (2026)", 20 Jul 2026,
   https://www.greatfrontend.com/blog/frontend-developer-github-profile
4. [S4] BuiltIn, "Here's What 4 Companies Really Look for on Your GitHub Profile",
   https://builtin.com/articles/what-companies-look-for-on-github
5. [S5] Pin, "GitHub recruiting", 17 Mar 2025, updated 30 May 2026, https://www.pin.com/blog/github-recruiting/
6. [S6] GitHub, "Octoverse 2024", https://github.blog/news-insights/octoverse/octoverse-2024/
7. [S7] CoderPad, "New Research: The 2026 State of Tech Hiring", 11 Mar 2026,
   https://coderpad.io/blog/hiring-developers/new-research-the-2026-state-of-tech-hiring-what-ai-means-for-developers-and-hiring-teams/
8. [S8] GitHub Docs, "Managing your profile README",
   https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
9. [S9] Ein-Gar, Shiv, Tormala, "When Blemishing Leads to Blossoming: The Positive Effect of Negative
   Information", *Journal of Consumer Research* 38(5), 2012, https://academic.oup.com/jcr/article/38/5/846/1816731
10. [S10] Sage, *Encyclopedia of Health Communication*, "Message sidedness",
    https://sk.sagepub.com/ency/edvol/embed/encyclopedia-of-health-communication/chpt/message-sidedness
11. [S11] rust-lang/rust issue #34057, "Provide mechanism for documenting known bugs or shortcomings", 3 Jun 2016,
    https://github.com/rust-lang/rust/issues/34057
12. [S12] Microsoft, "Write a high-quality README for NuGet packages",
    https://devblogs.microsoft.com/nuget/write-a-high-quality-readme-for-nuget-packages/
13. [S13] OpenSSF Scorecard, checks documentation, "Maintained",
    https://github.com/ossf/scorecard/blob/main/docs/checks.md
14. PyPI JSON for rustmapper (releases 0.1.0–0.1.3; 0.1.3 uploaded 2025-11-08T19:52:41),
    https://pypi.org/pypi/rustmapper/json

Two fetches failed and are not cited: Instahyre's checklist (403) and FOSS Resources' README guide (410).

In the repository: `docs/PRD.md` (`b6cca2c`); `docs/crit/prd/owner-messages.md`; `docs/crit/prd/LOG.md` rounds 1–5;
`docs/crit/prd/review-r05-1.md`; `docs/crit/round6/LOG.md` (round 16); `README.md`; `chart.toml:24–39, 1257, 1276,
1308, 1357`; `scripts/render_readme.py:459, 925`; `scripts/publish_chart.py`; `scripts/checks/` (28 files);
`assets/v9/hero-phone-day.svg` (group ids); `docs/BEN-TODO.md`; the renders under
`scratchpad/r6/build/round-16/` (sheet-phone-day-390, sheet-phone-night-390, sheet-desk-day-870,
sheet-desk-night-870, sheet-mid-day-746, page-desk-1, page-desk-2, page-phone-1 to -7) and
`docs/crit/prd/renders/{round-16,once-2b}/page-desk-1.png`; `git ls-remote`, `git branch -r --contains`, `gh api`
on the repository's pulls.
