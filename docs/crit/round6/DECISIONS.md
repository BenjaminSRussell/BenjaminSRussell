# Round 6 decisions

9 Oct 2026. The owner's brief for this round: the first image "is trying to be a map for no reason". It showed weeks
of commits as islands, and "there's nothing about that teaches you anything". Every map and every element needs a
purpose that comes from the projects. The build is SPEC.md.

## Research

| File | Subject | Numbered sources |
|---|---|---|
| R1-charts | chart standards, what each chart element is for | 44 |
| R2-pilotage | pilot books and how a stranger is led into a harbour | 44 |
| R3-software-maps | software maps and cities, and what programmers ask of code | 62 |
| R4-github-readers | who reads a GitHub profile, and what they look for | 57 |
| R5-metaphor | chartjunk, embellishment, when a borrowed form is earned | 52 |
| R6-the-projects | the 21 repositories themselves: code, READMEs, releases | 54 |
| R7-maps-of-the-web | maps of the internet and of crawls | 47 |
| **Total** | | **360** |

The concept memos cite about 19 more sources. Two of them ran code: concept B built rustmapper and go_go_go and
crawled a test site. About 33,000 words of research and 21,000 of concepts. The synthesis re-checked every code fact
it uses in the clones (Rust-sitemap 32c2651, Scrapy 96e7a1a, ideal-url-organizer 159968a, the 0.1.3 sdist and
wheel).

## Concepts and scores

Three judges scored each concept from 1 to 10 on five criteria. Goal is the owner's goal and is the deciding
criterion.

| Concept | Goal (J1, J2, J3) | Goal sum | All five criteria, sum over three judges | Judges naming it winner |
|---|---|---|---|---|
| A: the way into rustmapper (a route strip from install to output, traps where they bite) | 8, 6, 8 | **22** | 103 | J1, J3 |
| D: what his repositories hand each other (checked from both ends) | 7, 7, 7 | 21 | **112** | J2 |
| C: no map, one card per project | 5, 5, 6 | 16 | 110 | none |
| B: the picture is one of his crawls (depth of books.toscrape.com) | 4, 4, 4 | 12 | 70 | none |

D and C have higher totals than A because they score higher on honesty and on how easy they are to build. A scores
highest on the goal, and two of the three judges chose it.

## The choice

**A, with one route only (rustmapper), corrected and grafted.**

Why A. It is the only concept where the picture has a geography the visitor actually travels: install, run, the
stops a URL passes through in order, the traps at the stop where they bite, and the file you get. It answers "what
is it showing?" in one sentence. Nothing has a size. It is a pilot book's entry for a stranger, which is what the
owner asked for when he said "if I was a pilot ... very helpful information".

Why not D as the picture. Its idea is sound and its checks hold, but on the front page one working join out of six
reads as "his projects don't fit together". It is also Ben's to-do list, not something a visitor uses. Its best
parts are kept: the one tested hand-off is drawn, and the rule "drawn only when code on the receiving side proves
it" is applied to everything.

Why not C. It gives up the map. The owner asked for maps with a deep purpose, not for no maps, and most of the card
is text that Markdown does better. Its visitor questions (Q1 to Q5) and its computed CI line are kept.

Why not B. It teaches the shape of someone else's bookstore, and rustmapper can't produce it today. Its trial found
the most important fact of the round, and that becomes blocking work.

## What changed from concept A, and why

- **The robots.txt bug blocks the image.** At HEAD, a site whose robots.txt is a 404 is never crawled. This goes
  against RFC 9309 §2.3.1.3. The frontier stop can't be drawn until the fix and its test are at HEAD (B, all judges).
  The synthesis also found that the frontier asks for robots.txt over `https://` whatever the site's scheme. That
  needs confirming on Ben's machine.
- **The commands are run, not just quoted.** A weekly macOS arm64 job installs the release, crawls a local site with
  no robots.txt, sends one Ctrl-C, and checks the output. The entrance is drawn only when that passes (B, J1).
- **"True in both" is now applied to HEAD as well.** A's crt.sh hazard was false at HEAD, where the default is
  `none`, so it was cut. The seeds stop now says "plus seeds from" (all judges).
- **The command-name hazard was cut.** It is a packaging bug, to be fixed by releasing 0.1.4 with a `rustmapper`
  command. The command printed comes from the wheel itself, so it updates on its own. The synthesis found that HEAD
  now builds a pyo3 library with no executable, so a 0.1.4 cut as it stands would remove the command line from pip.
  The spec says so.
- **A new trap, found in the code.** The output file is written only when the crawl stops: one Ctrl-C writes it, and
  a second exits without writing it. This is true in both versions.
- **Kept from D:** the line past the end, "read by ideal-url-organizer, with a test", drawn only when the field check
  passes. One sentence of text covers the Scrapy export that nothing reads yet.
- **Kept from C:** a title block with "1 of 21 public repositories", the code's sha and date, a computed CI line
  ("PASSED"/"FAILED"), and "as of".
- **Dropped:** the last-commit date (from the image and the facts lines). It is sweep-adjusted, and it contradicts
  the 7 Oct code date and CI date that sit beside it (J2). The code date answers "is it alive" instead. This goes
  against J1's graft. Recorded here so the next round can overturn it.
- **Dropped:** A's second image, for Scrapy. Scrapy's entrance and its two real traps move into a code block. The
  third-party domain stays off the profile (J1, J3).
- **Fixed regardless:** the BART overstatement, go_go_go's "100M+", rule 3's pun ("Dashboards before speed"), and
  alt text that states the message.

## What this round does not settle

- The owner asked for at least ten rounds of review against his words, each with fresh research. This round was one
  round of research, four concepts and three judge reviews. SPEC.md section 7 gives the tests each later round runs.
  It is the input to the next round, not the end.
- Concept A's risk 1 still stands: with the theme only in the manner, it may read as a flowchart. The answer is
  better drawing of the same marks, never added symbols.
- The phone's first-two-screens claim rests on GitHub's mobile profile header, which is estimated. It must be
  measured on a device.
