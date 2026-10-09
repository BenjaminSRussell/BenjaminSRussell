# Round 5 review: tone (the deadpan copy editor)

## 1. Verdict

**SHIP AFTER FIXES.** The words no longer know they are themed, but the drawing has gone so quiet that a stranger
sees "old paper, a timeline", not "why is his readme shipping themed? odd."

## 2. What works

- **The page is written straight.** I read the README line by line and found no costume word: `Scrapy`, **Also**,
  **Working rules**, "Found a mistake?". The bullets play it straight, so you believe them.
- **`DATUM: MAIN` and `Fl 15s` are the only winks, and both are true.** Neither has a caption. A sailor sees a
  15-second light on Scrapy; everyone else sees a small code.
- **The empty water from Feb to Jul 2026 has no caption.** Honest, deadpan; keep it.

## 3. What must change

1. **The coastline is too timid** (sheet-desk-day-870, sheet-phone-day-390). Most banks are 4–8 px slivers, so the
   theme now lives only in the border. Fix: the busiest
   month (Scrapy, Oct 2025, 15 days) fills about 80 % of the row pitch; a one-day month gets at least 6 px. Fill the
   land in buff with a 3 px shallow-water blue band outside each coastline. No new words.
2. **The count doesn't add up** (sheet-desk-day-870). The sheet says `21 REPOSITORIES`, then shows 7 rows plus
   `9 MORE`, which is 16. Fix: `14 MORE` (five add no land, truly). Language tags appear on 2 of
   the 7 rows, which looks forgotten: take each tag from the row's largest language by lines, or drop the tags.
3. **Nobody is told what "sweep" means** (all sheet renders, page-desk-2). Fix: drop `SWEEP DAYS EXCLUDED` from the
   sheet. In the footnote, write `bulk-edit days (9–10 Nov 2025, 1 and 7 Oct 2026, when one change touched most
   repositories) excluded`.
4. **Repeats, a generated-by footer, a coined idiom** (page-desk-1, -2).
   - The role line appears three times in the first screen. Cut the centred `<p>` under the image.
   - `Generated from my repositories by scripts/build_assets.py` is the banned generated-by footer. Cut it, and
     move `how it's built → DESIGN.md` to the end of the License line.
   - The alt text "as a coastline" names the shoe. Rewrite it as `Ben Russell's repositories by month, Sep 2025 to
     Oct 2026, one row each; Scrapy and rustmapper busiest, quiet Feb to Jul 2026.`
   - `Lights before speed.` is the last idiom made up for the page, and next to `Fl 15s` it winks. Rewrite it as
     `Instrument before you optimize.`
5. **The facts lines: wrong register, and they break on a phone** (page-phone-2, -3). The `<sub>` spreads over three
   double-spaced lines. "Last worked" reads like a résumé gap. "3 test files" under the flagship reads like a
   confession. Fix: `tokio, redb, rkyv, reqwest, clap · CI passed 7 Oct 2026 · 16k lines of Rust · last commit 8 Aug
   2026`, set in plain italic. Drop the test-file counts from both lines.

## 4. The owner's test

**Two seconds, iPhone:** name, thesis, role line, an old chart. Right.

**Thirty seconds:** Scrapy and rustmapper were built Sep–Dec 2025; rustmapper is on PyPI; it went quiet until Sep 2026.
Helpful knowledge about him.

**Is the shipping there without being said?** The words never say it, and now the picture barely says it either. Fix 1
puts it back where it belongs.

**Cringe:** none left. **Lazy:** "3 test files" and "last worked". **Dishonest:** 21 claimed, 16 drawn.

The image is tidy, but nobody would screenshot it yet. A real coastline would earn the screenshot without another
word.
