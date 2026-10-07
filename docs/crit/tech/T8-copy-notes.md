# T8 — Copy & IA: notes to the integrator

Companion to `T8-README.final.md`; base README.draft.md.

## Decisions

1. **Thesis once.** "Wrong about itself" lives only in the hero and its alt (an alt replaces the image); the intro opens "Most of what I build is survey work…" (24, 25). The recruiter's plain line is the at-a-glance table, not a softened hero (29 vs 17/24; a 5-second test may still swap the hero line).
2. **Position line: visible text, hard gate** (18, 29, 36). `⟨role⟩ · ⟨city or timezone⟩ · ⟨open to⟩` between `position:start/end`; `check.py` fails on `⟨`; explicit `[position] text=""` omits the line with a warning (T1 §2.2, T10 check 12). We cannot invent it and must not ship a comment.
3. **At-a-glance table** under the links: Builds / Languages / Stack; "Ben Russell" its first two words (18, 29, 09).
4. **Headings glossed in reader vocabulary** as `<sub><i>…</i></sub>`; `<a name>` anchors before each H2; no numeric `height` (29, 09, 11).
5. **One name per thing** (17, 18, 03): rustmapper (link stays `/Rust-sitemap`; GitHub redirects); **Scrapy Harbor** everywhere. "Built on the Scrapy framework" is a fact, not the banned hedge.
6. **Honest Approaches** (19, 20, 22, 23): every bullet is a verified code fact from TECH-BRIEF (governor 256–1,024 permits; CRC32 rkyv WAL; one shard per core; wheel caveat; quickstart checked against the repo README; Arrow schemas, MinHash, BART locally; breakers on HTTP/Delta/Redis). Politeness sentence for rustmapper only; no 90%; the channel "is charted as proposed; nothing runs it yet"; go_go_go loses "per-host politeness".
7. **Notices**: lede "Figures correct themselves nightly. These five I had to be told." (34); no "because of this list" (25); provenance = repo + first-commit month, italic, no rationale (24, 25); Notice 4 bare; Notice 5 the one self-reference. Visible invite line (23 F5, 16).
8. **Log**: "Nothing on fire." is T9's, in body mono (25); the README never names it; lede and alt are column-agnostic (26).
9. **Never mention the avatar** (25); the footer carries one line and nothing follows it (24).
10. **Captions**: visible `<sub>` under every sheet but the footer; soundings carries build-filled figures and a dateline (32, 21); instruments mirrors T9's `FITTINGS`. Alts ≤25 words, plain (09).
11. **Folds**: shelf summary carries count and contents (29); Colophon folded so the exit is Instruments → one line → footer (27). Declined 27's 62%-wide Instruments: 13px type would land near 5px (07, 10).
12. **License/fork bullet** gated on T1's LICENSE + `chart.toml` (23, 35).
13. **Explained tricks**: only the Variation line and 34's chart-number sentence (17); no "works at night" (32).
14. **Cut**: thesis repeat, "Shorter crossings", "because of this list", "not the framework itself", "90%+", "512 workers", "one pip install away", footer mono caption, "borrow it", avatar, CHANGELIST A4. Nautical "chart" five times; "X, not Y" twice; one tricolon.

## GitHub bio (<160 chars)

Primary: **Crawl and data infrastructure, Python and Rust. The web is wrong about itself; I survey the part that isn't linked.** (113)
Alternate: **Crawl and data infrastructure in Python and Rust. rustmapper on PyPI; Scrapy Harbor on GitHub.** Also set location, website, hireable; pin both repos; reuse the sentence as repo description and PyPI summary (17, 18).

## Position-line gate (→ T10 `check.py`, T1 `render_readme.py`)

Fail on `⟨`/`⟩` outside comments; fail if `[position].text` is unset (explicit `""` = warning, slot omitted everywhere); fail if any of {Python, Rust, crawler, PostgreSQL, Redis, Kubernetes, Docker, "data infrastructure", Ben Russell} is missing from image-stripped text (18); fail if an H2 lacks `<sub>` or a sheet lacks a caption (29); fail if the `license` block ships without `LICENSE`; print the alt poem, diffed against `alt_poem[]` (T7 check 6).

## The alt poem

> A boat sails out and back.
> The curve draws in once and holds.
> The soundings fill in behind the vessel.
> Types once; only the cursor keeps time.
> The daily driver in bold; the rest when asked.
> The chart ends here; the web doesn't.

## Interfaces

**Provide**: README template and markers (`position`, `contact`, `figures`, `notices`, `instruments`, `license`), alts, captions, `alt_poem[]`, anchors, bio. **Need**: T1 `<source>` lines and `chart.toml` keys; T2 cartouche mirror of `position` and the lane line; T3 legend row for the proposed channel and the upright/italic definition; T7 figures, dateline, notice dates, `edition.wheels`; T9 `FITTINGS`, `log.json`.

## Open questions for Ben

1. Role · place · open-to; LinkedIn and résumé URLs, or an explicit "none".
2. Rename `Rust-sitemap` → `rustmapper` and `Scrapy`? Copy works either way.
3. One worker figure across code (256–1,024), repo README (32–512), PyPI (256).
4. Add a dated "Notice 0" (0.1.0/0.1.1 shipped without the engine, fixed that evening)?
5. Commit total 1,828 or 1,868; 21 repos surveyed vs 24 public.
6. LICENSE for both repos; until then the License bullet does not ship.
7. Any collaboration artefact for one line (03)? None verified, so none written.
