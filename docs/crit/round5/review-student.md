# Round 5 review: the student (19, phone, never read a chart)

## 1. Verdict

**SHIP AFTER FIXES.** The costume is gone and it finally tells you about him, but it overcorrected: on a phone it reads as a timeline on old paper, not a chart, so nobody thinks "why is his readme shipping themed?" and nobody screenshots it.

## 2. What works

- Honest, and it's him. Scrapy and rustmapper are the fattest rows; he worked Sep–Jan, went quiet, came back in September. I get his year in ten seconds with no legend.
- The pink flare on Scrapy with `Fl 15s` (sheet-phone-night-390) is the one thing that feels alive. I don't know what Fl means and don't need to.
- "Built on … · 257 test files · 5 workflows, last run passed · last worked 8 Oct 2026" is the most helpful line on the page. It's what I check before I star.

## 3. What must change

1. **It doesn't read as land and water** (sheet-phone-day-390). Banks are 4–8 px tan slivers in 40 px rows on tan paper. Fix: tint the row field with v10's shallow blue (day ~#d6e4ec, night one step off the paper). Keep the land tan with its dark coast and put a 2 px pale halo outside each coast. Double the scale: 15 commit-days = 14 px half-thickness at 1x on phone, floor 4 px. Blue, tan and a wiggly coast reads as "map" in a second.
2. **The count doesn't add up** (sheet-phone-day-390). The title says 21 REPOSITORIES; the sheet shows 7 rows + "9 MORE" = 16. Five repos (Course_crusader, Elusive_trades_data, Spotify_to_apple_music, rust_llm_logger, mlx_Qwen_data_entry) only have sweep days, and rust_llm_logger sits under "Also" on the page with no land at all. Fix: label the row "14 MORE". Audit whether 9 Nov 2025 was a sweep or the day he actually pushed those projects.
3. **Things hit the frame.** The Sep–Oct 2026 banks and the "O" tick touch the right neatline (sheet-phone-day-390). On desk, SCRAPY sits about 6 px under the top border and the URL is crammed below the frame (sheet-desk-day-870). Fix: end the axis 16 px inside the neatline, start the desk rows 24 px below the border, set the URL 8 px inside the foot margin.
4. **Page text** (page-phone-1, -2, -3, -5). Cut the centred caption "Crawl and data infrastructure · Python and Rust"; the sheet already says it. Cut "Generated from my repositories by scripts/build_assets.py", a generated-by footer the standing rules ban; move the DESIGN.md link into License. The two `<sub>` "Built on…" lines render on a phone as three double-spaced grey lines that look broken. Make each one a normal italic paragraph.
5. **BENJAMINSRUSSELL is row four.** His fourth-biggest project is this page? Merge it into the "more" row.

## 4. The owner's test

**Two seconds, iPhone:** big name, a human line, smudges on a timeline, a pink sparkle. My read: "old paper, cute." Not "shipping." The theme stopped announcing itself and stopped showing up.

**Thirty seconds:** crawlers, Python and Rust; Scrapy and rustmapper are the real ones; rustmapper is on PyPI; he's active this month. That's helpful knowledge, and a follow.

**A layer of shipping that never says so:** only `DATUM: MAIN`, `Fl 15s` and a dashed neatline, visible only if you already know charts. Fix 1 brings it back without adding a word.

**Cringe:** none. **Lazy:** the slivers. **Dishonest:** "21" over 16 drawn.

**Screenshot?** Not this one. It's tidy. With blue water, fat tan banks and that pink flare blinking on Scrapy, yes. I'd send it with "look at this guy's readme."
