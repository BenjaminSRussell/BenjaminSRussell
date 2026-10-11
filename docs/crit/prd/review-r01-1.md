# PRD review round 1, reviewer 1: Ben, the owner, reading the PRD as the person who has to live with the page

11 Oct 2026. I read `docs/crit/prd/owner-messages.md` twice, end to end, before opening the PRD. Then `docs/PRD.md`
(531 lines), `README.md`, `SPEC.md` §0, `DECISIONS.md`, the round-16 entry of `round6/LOG.md`, `review-r16-1.md`,
`chart.toml`, `docs/BEN-TODO.md`, `scripts/checks/route.py` (THEME_WORDS), `scripts/build_assets.py` (SHEETS), and
every round-16 render named in the brief: the sheet on the phone at 390 (day, night), desk at 870 (day, night), mid at
746, the page at desk (2 screens) and at 390 (7 screens). I ran `python3 -m unittest` (539 tests, OK, 21.8 s) and
read `round-16/gate.txt` (0 fail, 4 warn, exit 2). There is no earlier PRD round and no `prd/LOG.md`, so nothing here
can be a repeat. Every number below that is about the repository, I counted myself.

Verdict on the PRD: **7 / 10.** Honest, thorough, and it holds my rules to real gates. It fails as *my* document in
four places: it leaves out one of my briefs from the goal table, it reports the yardstick (my messages) with the wrong
count, it puts the one decision in front of me without what I need to make it, and it carries two things I settled
(the commit counts, the position line) as open items under my name instead of ruling on them with my words.

---

## 1. Is the product this PRD defines what I asked for?

**Yes, with one condition, and the PRD already names the condition.**

The sentence that decides it is from 9 Oct 11:37: *"If I was a fucking sailor pilot... what I'd want are very helpful
information. Things that very help. The map, very helpful. The fucking log, not really... It should be telling you
about me, but with a layer of a theme of shipping... It has to be helpful knowledge."* The product in §1 and §5 is
exactly that: one image that is directions a stranger uses (install, the loop, the two catches, the one key, the
file, where it goes next), a page that is lookup material, and nothing that says the word for what it is. §5.1's
"Drawn only when" column is the answer to my 9 Oct 20:50 sentence, *"Everything, single thing inside of this needs a
purpose, not a fucking chasing a reason"*: every mark has a row, every row has a source, and a mark with no purpose
can't be drawn. That is the page I asked for.

The condition is the one §0 calls "the blocker outside this repository". The top of the page today, as rendered
(`sheet-phone-day-390.png`, `page-desk-1.png`), says: my name, what I build, rustmapper, what it does, `pip install`,
two rows of how it runs, then a red dotted box with *"0.1.3 never exits by itself"*, and under the image a six-item
"Before you run 0.1.3" list. That is true, and I asked for true. But my 7 Oct sentence, *"tells a lot about me"*, is
also binding, and what the first screen tells a stranger about me today is that my flagship ships with a stop-rule
you have to learn from my profile. So: the PRD defines the page I want; the page as it ships under option 3 is not
the page I want. Option 1 in §9.1 is the right recommendation, and §2 of this review says what the PRD has to add so I
can take it.

Is §5 something I'd screenshot and send? The image, yes. It looks like a page torn from a manual that a careful
person wrote, and nothing in it announces what it is. The page, not yet: the facts line and the cautions list are
what a stranger would screenshot, and they are not what I'd send.

## 2. Must-fixes, ranked

Each: where (section, line of `docs/PRD.md`), what to change, why (my words or a source), and whether it is about
the PRD text or the product it defines.

### MF1. §9.1 does not give me what I need to decide (PRD text; lines 353–364)

The decision is framed as "what the top of the profile says about rustmapper 0.1.3" with three options. The question I
would ask is the one §0 already asks for me: *what is the first sentence a stranger reads about me under each
option?* The table answers "what ships" in pipeline terms (box gone, S2 drawn) and "cost" as a list of nine fixes
with no size. To decide, I need, in the table or under it:

1. **A render of the option-1 outcome.** `LOG.md` round 1 says the pipeline already built a "once-p1-lands" sheet
   from a fixture `stats.json` (`scratchpad/r6/build/round-01/once-p1-lands/`). §5.4 lists what a 0.1.4 retires. Build
   the sheet and the page from a fixture where every §5.4 probe passes, and put the paths in §9.1 next to the
   round-16 paths. I decide between two pictures, not between two table rows.
2. **The size of option 1, in days, and what HEAD already has.** §5.4 lists eight fixes; §11 adds the packaging one
   (`[project.scripts]`). For each: already at HEAD (yes/no), test exists (yes/no), estimate. The PRD cites the
   clones (`32c2651`), so it can say this today.
3. **The first-screen sentence for each option, in words.** Option 1: "name, role, rustmapper, install, the loop,
   the key, the file." Option 3: the same with "never exits by itself" in a red box. Option 2: option 3's image with
   a shorter page. Write it so.
4. **The middle option is missing.** Between "move every caution off the page" (2) and "ship as is" (3): keep the
   image, keep the box (it is true of the release the image names), and cut the page's list to the two faults a
   stranger meets in the first minute (never exits; no contact in the UA), folding the other four under the
   existing `<details>`. Two items is under the "few" every hiring-side source below sets. It needs no work in
   Rust-sitemap and retires the same way. Add it as option 2b with its gate changes, or say why not.

Why: my 9 Oct 20:50 instruction, *"is it accomplishing my goal? Not just what I'm saying"*: my goal is a page that
tells a stranger about me; the PRD should let me judge the options by that, not by which probes pass. Atlassian's
guide says a PRD exists to "keep track of all the open questions you need to answer" [S8]; an open question with no
sized options is a note, not a decision.

### MF2. §3 leaves out my 7 Oct 17:40 brief (PRD text; lines 69–89)

The goal table has 19 rows and quotes 7 Oct 15:30 (G1) and then nothing of mine until 8 Oct 14:52 (G2). The three
messages between are only in Appendix A. Two of them are instructions, not mood:

- 7 Oct 17:40: *"is it interesting does it draw in the user what does it say about the person who made it... it
  should say more than it literally says and should have layers of depth and thoughts associated with it."*
- 8 Oct 14:22: *"The images are not cool enough."*

Add rows (after G1):

| # | His words (date) | What it means here | Held by |
|---|---|---|---|
| G1a | "it should say more than it literally says and should have layers of depth" (7 Oct) | a second reading finds more: the loop bracket (rows repeat), the gap in the track under the box (the release never exits), the thin line past the end (his projects hand each other files) | review; name the second-reading marks in §8.3 q.1 |
| G1b | "is it interesting does it draw in the user what does it say about the person who made it" (7 Oct) | the page says what kind of engineer made it without saying so: measured figures, run commands, faults stated with their fix | review (§8.3 q.4) |
| G1c | "stunning and fun" (7 Oct) / "The images are not cool enough" (8 Oct) | finish and wit; overridden on 9 Oct for anything that names the theme ("cringy") | review; **state the trade in §3**: "fun" was traded for "not on the nose" by his 9 Oct words, and the two winks are the remainder |

Why: these are my words and the table claims to be "in the owner's words". G1a is in fact met by the product (I can
point at the three marks), and the PRD should take credit for it in writing rather than lose it. G1c is a trade I made
on 9 Oct, and the PRD should say that I made it, so no later round re-opens "fun" without re-reading 9 Oct.

### MF3. The position line is a warning, not a gate (product; §8.2 line 329, §9.2 line 368)

`[position] text` is `""`, so the only lines about me on the whole page are "Ben Russell", "CRAWL AND DATA
INFRASTRUCTURE / PYTHON AND RUST" and "Ben Russell builds web crawlers, discovery pipelines, raw-first storage and the
dashboards that watch them." No city, no timezone, no "open to" or "currently", no LinkedIn, no resume
(`[contact]` is `""` too; I checked `chart.toml` lines 23–30). The PRD's own `BEN-TODO.md` calls it "the one line a
hiring manager came for", and §8.2 lets it stand as a warning on the merge commit.

Change: move POSITION-EMPTY from §8.2 ("warnings allowed today") to §8.1 ("must all hold on the commit that
merges") as item 6: "`[position] text` and at least one of `[contact] linkedin` / `resume` are set." Owner: me. The
PRD may not merge my profile with the one line a visitor came for left blank, whoever's job it is to fill it.

Why: my 7 Oct words, *"tells a lot about me"*. Underdog's hiring-manager piece: a cold visitor "should know within
half a minute what you build" and reviewers start with "the profile (bio, photo, links)" [S1]. Stanford's guidelines
4 and 5: show that real people stand behind the page, and make it easy to contact you [S6]. The page has an email
link and nothing else.

### MF4. The commit counts on the facts lines contradict G8 and the PRD punts (product; §3 line 78, §9.2 lines 369–370, §10.5)

The rustmapper facts line prints *"coding agents (Claude) authored 45 of its 146 commits and co-signed 1 of his own
101"* and Scrapy's prints *"authored 71 of its 499 commits and co-signed 30 of his own 420"* (`README.md`, the two
`facts:` blocks; `page-desk-1.png`, `page-phone-2.png`). G8 quotes me, *"We don't need to show the commits... it feels
lazy"*, then says the facts lines print them anyway as "owner's call, §9.2". §9.2 says two memos argued hiding them
costs more than stating them.

Change: rule on it in the PRD. My words are the rule until I overturn them, so the default is **off**: G8's "Held by"
becomes "`chart.toml [facts] agent_clause = false`; the renderer prints no commit count of any kind", §10.5's switch is
implemented, and §9.2 keeps the memo's argument as the case for turning it on. If the memos' point is that an
engineer who reads the clones will find the agent commits anyway, the honest and shorter form is a clause with no
numbers in the provenance `<sub>`, which already says who is counted.

Why: my sentence. Also the research below: faults and caveats help credibility when each comes with what to do
about it [S9, S10]; a count of commits an agent wrote is a caveat with no action for the reader, which is the kind
the two-sided-message reviews find least persuasive [S11].

### MF5. The yardstick is miscounted (PRD text; line 8 and Appendix A)

Line 8: "the owner's 26 messages in this session (appendix A, verbatim)". `owner-messages.md` has 21 messages
(`grep -c '^## 2026'`). Appendix A quotes 14 of them. The seven it drops are short ("Start now", "Don't stop",
"Continue", "Resolve all merge conflicts...", "Merged but all images are unavailable", "Merged check and this needs
higher reviews", and 11 Oct later: *"Review and ensure this is something I want to see rounds of reviews and
research"*). Change line 8 to "the owner's 21 messages (appendix A quotes the 15 that set a rule; the file has all 21)"
and add the 11 Oct (later) message to Appendix A: it is the instruction this round runs under.

Why: the PRD says my words are the standard. A standard with the wrong count on its first page is the kind of error
Stanford's guideline 10 is about: "Avoid errors of all types, no matter how small they seem" [S6].

### MF6. §2 reverses what I said about devices, and the product pays for it on the desk (PRD text, line 61; product, §5.3 row 6)

I said (9 Oct 11:32): *"if someone's going to look at your profile, likely look at it on the web and maybe on your
iPhone. If they're looking at your repos, it's definitely on the web."* §2 renders that as "an iPhone first, then a
laptop". Both must work; the phone is the stricter constraint; the web is the likelier reader. Reword line 61 to
that.

The product cost is visible in `page-desk-1.png`: in an 846 px column the code block reads

```
rust_sitemap crawl \
    --start-url <your-site>
# 0.1.3 runs until stopped: when
# "Received work item" stops
# for 60 s, then Ctrl-C once
```

because README-CODE-WIDTH caps every line at 32 columns for the 360 px phone. Markdown serves one block to both, so
the desk reader, the likelier one, sees phone-wrapped comments with two thirds of the column empty. The PRD should
state this trade in §11 ("Risks") in my words, and §5.3 row 6 should say the comment lines are the only lines that
wrap for the phone's sake. If a reviewer finds a way to join the three comment lines into one ≤ 32-column line
("# runs until stopped; Ctrl-C once" is 33), take it.

### MF7. Theme strings I asked to kill still live in `chart.toml` (product; §7.1 lines 222–225)

`chart.toml [copy]` still carries `unit_chart = "SOUNDINGS IN COMMIT-DAYS"`, `unit_hero = "SOUNDINGS IN COMMITS"`,
`unit_approaches = "SOUNDINGS IN URLS · THOUSANDS"`, `limit_label = "LIMIT OF SURVEY 2026"` and `footer_line = "The
chart ends here. The web doesn't."` I grepped: `unit_chart` is read by nothing; the other four are read only by
`scripts/sheets/soundings.py`, `approaches.py` and `footer.py`, which `build_assets.py` lists in `ALL_SHEETS` but
not in `SHEETS = ["hero"]`, so they are retired modules. §7.1 gates theme words on the image, the alt and DESIGN.md;
STRINGS-BANNED reads `chart.toml` for phrases but not for THEME_WORDS.

Change: §7.1, new row: "No theme word in `chart.toml` strings that any live sheet reads; retired sheet modules and
their strings are deleted, not kept" with a gate (extend `theme_words` to `[copy]` values). Then do it: delete the
five keys and the three retired sheet modules (and `log.py`, `instruments.py`, whose `log.shards` warning §8.2 calls
"harmless"; delete the module and the warning goes with it).

Why: `BenjaminSRussell/BenjaminSRussell` is a public repository, and `chart.toml` is the file the PRD tells me to
edit. An engineer who clicks through from the profile reads "The chart ends here. The web doesn't." in the config.
That is the thesis-line voice I cut on 9 Oct 19:39 (*"survey the web that is wrong about itself come the fuck on"*),
and 9 Oct 11:32: *"Fuck saying ship's log."* It is not on the page, so it is a repository finding; but the PRD's §7.6
says the repository is part of the product's process, and the rule should reach it.

### MF8. §8.3 has no "would you screenshot it" question (PRD text; lines 334–343)

The five judged questions are purpose, truth, phone, tells-about-him, ship. On 8 Oct (round 4, `BEN-TODO.md`) the
question put to me was "which one you would screenshot", and that is still the test for *"stunning"* and *"one of a
kind"*. Add q.6: "Would the reviewer screenshot the image and send it to someone, and what would they say it was?"
The second half catches the §11 flowchart risk, which today no round is asked to look for.

Why: 7 Oct 15:30, *"world class one of a kind beautiful... stunning"*; §11 names the flowchart risk and then says the
round-13 and round-16 reviewers "did not raise it", which is not the same as having been asked.

## 3. The 19 goal rows against my sentences

| Row | Missing, softened, or reinterpreted? |
|---|---|
| G1 | **Softened.** "stunning and fun" became "the standard of finish". See MF2: write the trade down. |
| G2, G5 | Held. The image has no theme word (ROUTE-WORDS); my grep of README prose finds only project words ("Helm chart", "full-text search", "authorship", "lightweight"), which is what §10.1's allow-list is for. Right. |
| G3 | Held, and visibly: one left edge, one pitch in every render. The phone sheet is the same drawing at its own width, not a shrink. |
| G4 | Held except the device check, which the PRD says plainly is open (§9.3). Fair. But §2 reverses the order I gave (MF6). |
| G6 | Held. I checked: nothing on the image is also in the prose except `pip install rustmapper` and `Received work item`, the two exceptions the gate lists. |
| G7 | Held, and this is the row that answers my *"how is the data gathered?"* best: every figure on the page has a source commit beside it. |
| G8 | **Reinterpreted** to the image only; the page prints commit counts (MF4). |
| G9, G12 | Held. No ship, no rose, no "unsurveyed", no cliff. The red dotted box is the only mark with any charge. |
| G10 | Held. Two winks on the page ("Boring under load.", "why engines are hard"); none nautical. Right amount. |
| G11 | Held. The log sheet and its kin are off the page (but their code is not out of the repository: MF7). |
| G13 | Held. Third person; "Ben Russell builds". |
| G14 | Held. No thesis line anywhere on the page. |
| G15, G16 | Held, and the strongest two rows: T-NOSIZE (two stats fixtures differing in every count give identical geometry) is exactly the test for *"Is it based on the size of the project or how many commits?"* |
| G17, G18, G19 | Done as process: 48 review files, 16 rounds, 360 sources in seven files. Note that the PRD's "no round reached a unanimous ship verdict" is honest; it would have been easy to write "reviewed 16 times". |
| 7 Oct 17:40 | **Missing** (MF2). |
| 8 Oct 14:22 | **Missing** ("images are not cool enough"; "Wording is weird but it's cool"). |

## 4. The top of the page, as rendered

`sheet-phone-day-390.png`: name, role, rustmapper, one sentence, the install line with its date, the loop, the red
box, the key, the file, the hand-off. Every word is legible at 390; I can read `Received work item` in the mono face
inside the box. Night (`sheet-phone-night-390.png`) is a redraw, not an inversion: the magenta is lighter, the paper
is navy, and nothing thins out. Desk at 870 has air; the mid at 746 is the same drawing. The first phone screen of
the page (`page-phone-1.png`) shows the whole image and the link row. That meets "one screen".

Is it something I want strangers to see first? The top half, yes, without reservation. The red box, only once 0.1.4
exists (MF1). The facts line and the six-item list under it, no: they are what the second screen says about me, and
on a phone (`page-phone-2.png`, `page-phone-3.png`) the list runs a screen and a half before the code block. The
research below says why that order costs more than it earns.

## 5. Research

### 5.1 What convinces a senior engineer or a hiring manager on a GitHub profile in 2026

Eight sources, mostly practitioner guides (none is a controlled study; the one academic item, a 2024 interview study
of 15 recruiters [S4], surfaced only as a preprint listing). They agree on five things:

1. **Order of reading:** profile line and links, then pinned repos, then each README, then commits and code [S1, S2].
   The PRD's Q1–Q5 order matches.
2. **Time:** "scanned for only seconds"; "30–90 seconds. The pinned repos and their READMEs do almost all the work"
   [S1, S2]. §2's "about 7 s" for a screener is shorter than any source I found; it comes from R4, which I did not
   re-read. The PRD should cite the R4 source number beside it.
3. **Few finished things over many:** "Four polished projects beat six random ones every time" [S1]; "pin fewer
   rather than padding" [S2]. The page's two projects plus four "Also" plus a fold of 15 is the right shape.
4. **A README's order:** what it is, why, how to try it, how it works, *then its status* [S2]. The page puts status
   (six cautions) before the how-to-try code block. That is the reverse of the order the hiring-side source gives.
5. **What hurts:** "pinning ambitious but unfinished work" [S1]; "'Work in progress' warnings without recent commits"
   read as abandoned [S2]; promotional copy, which users "detested", and visible exaggeration [S5]. The page has no
   marketese at all; that is a strength the PRD should claim in §11 or §8.3.

GitHub's own doc says only that the profile README is "to tell other people about yourself" [S7], which is my 7 Oct
sentence in their words, and the one the page is thinnest on (MF3). For contrast, a working engineer's profile I
opened (antfu's) is seventeen lines of links and nothing else [S13]: the minimal end of the range the guides
recommend. Mine is the other end, and that is fine if every line earns its place.

### 5.2 Do a tool's known faults on its author's own profile help or hurt?

Six sources, and the answer is conditional:

- **Stating limits is standard and reads as trust.** Caltech Library's README template carries a "Known issues and
  limitations" section, placed *after* Usage [S9]; a FOSS README guide says a project should say early if it is
  experimental or pre-release, and that "clear limits build trust" and cut support load [S10].
- **Two-sided messages raise credibility, most for sceptical readers, and most when each weakness comes with its
  answer.** Crowley and Hoyer's framework [S11a]; a 2022 consumer study found the credibility gain only among the
  sceptical [S11b]; the Allen review as summarised found refuted counterarguments most persuasive and unrefuted ones
  least [S11c]. Engineers reading a crawler's profile are the sceptical audience. Four of the page's six cautions
  carry their fix (`--workers 1`, `--user-agent`, `--seeding-strategy none`, "start at the bare domain"); two do not
  (the robots.txt timing, the https stall). The image's H1 carries its answer ("quit when..."); H0 does not.
- **Admitting a flaw helps when credibility is in doubt and hurts when it is already established** [S12]. A stranger
  has no prior on me, so the admission helps; a reader who already rates the tool reads the box as noise.
- **Bad impressions form faster and resist correction** (Baumeister et al. 2001, via a summary [S14]). This is the
  case for MF1's render: the first screen sets the impression, and a later screen does not undo it.
- **Hiring-side:** "Honest failure states and useful messages beat happy-path demos" [S1], but unfinished work pinned
  at the top hurts [S1, S2].

So: faults on the profile help when they are few, each has its fix beside it, and they come after what-it-is and
how-to-try. The image does this (two faults, in the loop, one with its answer). The page's list does not: six items
before the code block, two without a fix. That is the evidence behind MF1's option 2b and MF4.

## 6. What I checked and found correct

| PRD claim | Checked | Holds |
|---|---|---|
| 539 tests pass | `python3 -m unittest`: Ran 539 tests, OK | yes |
| 28 gate plug-ins | `ls scripts/checks/*.py` less `__init__` = 28 | yes |
| 48 reviews, 16 rounds | `ls docs/crit/round6/review-r*.md` = 48 | yes |
| round-16 gate: 0 fail, 4 warn, exit 2 | `round-16/gate.txt` | yes |
| best round 9/9/8 (round 13) | `LOG.md` line 842 | yes |
| provenance ≤ 60 words | 40 words | yes |
| no theme word in README prose | my grep: only project words | yes |
| THEME_WORDS as listed in §7.1 | `checks/route.py:60–61` | yes |
| the page prints no commit total of his own | it prints agent counts and "his own 101" / "his own 420" (MF4) | partly |
| 26 owner messages | 21 (MF5) | **no** |

## 7. Score

**7 / 10** for the PRD. It is the first document in this session that puts my rules, their gates and their gaps in
one place, and it is honest about what was never reached. Three points off: a brief of mine is missing from the
table (MF2), the decision I am asked to make is not sized or shown (MF1), and two things I said are carried as open
under my name instead of ruled on (MF3, MF4). Fix those and it is the document I'd hand to someone who had to rebuild
the page from nothing.

## Sources

1. Underdog, "What Hiring Managers Look for on GitHub: Land Your 2026 Job",
   https://underdog.io/blog/what-hiring-managers-look-for-on-github — reading order (profile, pinned, README, commits);
   "scanned for only seconds"; "should know within half a minute what you build"; "Four polished projects beat six
   random ones"; "Honest failure states and useful messages beat happy-path demos"; pinning unfinished work is the
   commonest mistake.
2. TechInterview, "GitHub Profile Polish for Engineers: Pinned Repos, READMEs, What Recruiters Click On",
   https://www.techinterview.org/post/3233474626/github-profile-engineers/ — "30–90 seconds. The pinned repos and
   their READMEs do almost all the work"; README order what / why / how to try / how it works / status; "pin fewer
   rather than padding"; WIP warnings without commits read as abandoned; "A clean, minimal profile README is better
   than a flashy one".
3. Instahyre, "GitHub profile checklist", https://resources.instahyre.com/blog/github-profile-checklist/ — 2–4
   polished pinned projects; 40 half-finished repos read worse than 3 polished ones.
4. Figueiredo et al., 2024 preprint, interviews with 15 recruiters on GitHub data in hiring,
   https://homepages.dcc.ufmg.br/~figueiredo/publications/latam2024preprint.pdf — surfaced as a listing; findings not
   read; cited only as the one academic item found.
5. Jakob Nielsen, Alertbox 1 Oct 1997, "How Users Read on the Web" (mirror),
   https://paginaspersonales.deusto.es/abaitua/konzeptu/sgml/9710a.html — 79 % scan, 16 % read; credibility rises
   with good writing and outbound links; users "detested" marketese; "Credibility suffers when users clearly see that
   the site exaggerates".
6. Stanford Web Credibility Project, guidelines, https://credibility.stanford.edu/guidelines/index.html — guideline
   4 (honest people behind the site), 5 (easy to contact), 6 (looks professional), 10 (avoid errors of all types).
7. GitHub Docs, "Managing your profile README",
   https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
   — a profile README is to "tell other people about yourself".
8. Atlassian, "How to create a product requirements document (PRD)",
   https://www.atlassian.com/agile/product-management/requirements — a PRD keeps "track of all the open questions you
   need to answer" (from the search summary; the page body did not fetch).
9. Caltech Library README template, https://github.com/caltechlibrary/template — "Known issues and limitations"
   section after Usage; omit it or write "none are known at this time".
10. FOSShub, "README" resource, https://www.fosshub.com/resources/development/readme/ — say early if experimental or
    pre-release; clear limits build trust and cut support requests (from the search summary; the page returned 410
    on fetch).
11. Two-sided messages: (a) Crowley & Hoyer 1994, *J. Consumer Research* 20(4),
    https://ideas.repec.org/a/oup/jconrs/v20y1994i4p561-74.html; (b) "When transparency pays off", *Int. J. Consumer
    Studies* 2022,
    https://edisciplinas.usp.br/pluginfile.php/7947675/mod_resource/content/1/2022%20Int%20J%20Consumer%20Studies%20When%20transparency%20pays%20off%20Enticing%20sceptical%20consumers%20with%20two%E2%80%90sided.pdf
    (credibility gain only for sceptical readers); (c) Allen 1991 review as summarised at
    https://customerthink.com/?p=109916 (refuted counterarguments most persuasive, unrefuted least).
12. "The credibility dilemma: When acknowledging a (perceived) lack of credibility can make a boast more believable",
    *Org. Behavior and Human Decision Processes* 183 (2024),
    https://ideas.repec.org/a/eee/jobhdp/v183y2024ics0749597824000438.html — disclaimers help when credibility is in
    doubt, are useless or harmful when it is established.
13. antfu's profile README, https://raw.githubusercontent.com/antfu/antfu/main/README.md — seventeen lines of
    links; the minimal end of the range.
14. Baumeister, Bratslavsky, Finkenauer & Vohs 2001, "Bad is Stronger than Good", via summary at
    https://andrewclark.super.site/all-media/bad-is-stronger-than-good — "Bad impressions ... are quicker to form and
    more resistant to disconfirmation than good ones".
15. Reskilll, "GitHub Profile That Gets You Hired: The 2026 Developer Portfolio Guide",
    https://blogs.reskilll.com/github-profile-gets-you-hired-2026-developer-portfolio-guide/ — the profile README is
    read first, then pinned repos, then the graph.
16. Repository files read: `/home/user/wt-v12/docs/PRD.md`; `/home/user/wt-v12/docs/crit/prd/owner-messages.md`;
    `/home/user/wt-v12/README.md`; `/home/user/wt-v12/chart.toml`; `/home/user/wt-v12/docs/BEN-TODO.md`;
    `/home/user/wt-v12/docs/crit/round6/SPEC.md`, `DECISIONS.md`, `LOG.md` (rounds 1, 13, 16), `review-r16-1.md`;
    `/home/user/wt-v12/scripts/checks/route.py`; `/home/user/wt-v12/scripts/build_assets.py`;
    `/home/user/wt-v12/assets/stats.json`; renders under
    `/tmp/claude-0/-home-user/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/r6/build/round-16/` (`gate.txt`,
    `sheet-phone-day-390.png`, `sheet-phone-night-390.png`, `sheet-desk-day-870.png`, `sheet-desk-night-870.png`,
    `sheet-mid-day-746.png`, `page-desk-1.png`, `page-desk-2.png`, `page-phone-1.png` to `page-phone-7.png`).
