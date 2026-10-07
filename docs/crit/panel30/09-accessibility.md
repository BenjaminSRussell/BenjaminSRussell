# 09 — Accessibility specialist (WCAG 2.2, screen readers, cognition, motion)

I audit for AT users, low vision, colour-vision deficiency, photosensitivity, vestibular disorders and cognitive load. I read README.md and README.draft.md as a screen reader would (alt only), looked at the full-page and 2x renders, read the specs' motion and alt sections, and computed contrast from `CHART_LIGHT` / `CHART_DARK` in `scripts/svgkit.py`.

## What is good

- **Dual-register headings** (`## Notices to mariners <sub>five corrections</sub>`) are the right cognitive mitigation: the plain word arrives inside the same heading, so a screen-reader user hearing the headings list, and a skimmer, both get a map of the page without decoding the metaphor.
- **Day/night via `<picture>`.** Night contrast is strong: ink 13.6:1, muted 5.3:1, accent 6.1:1, green 10.2:1 on paper. Night is the accessible edition.
- **Region B buoyage as specified** (spec-hero §5): numbered `G "1"` / `R "2"`, cone vs flat body, labels in text. IALA was designed for colour-blind mariners (odd green, even red, shapes differ), so the chart grammar is already a colour-independent encoding.
- **Every image has alt**, and every flash character in the specs (`Fl(3) 10s`, `Fl 4s`, `Iso 2s`, cursor 1.1 s) is far below seizure thresholds.

## What is bad, ranked

1. **The day edition fails AA for small text.** `muted` #6B7A90 on paper #F4EEE1 is 3.77:1 (3.20 on land); `accent` #D9442B 3.77:1; `ok` #2F8F5B 3.49:1. AA for text under ~18px is 4.5:1, and these colours carry 9–13px type scaled to 68% in the README column (~6–9px). Night passes everywhere.
2. **Features are tint-only.** Land vs paper is 1.18:1 in both editions; hairline contours 1.5:1; grid 1.3:1. The archipelago is "the portfolio" (Standard 3) and it is invisible to low-vision and most colour-deficient readers. WCAG 1.4.11 asks 3:1 for meaningful graphics.
3. **No reduced-motion edition exists.** Spec-hero §8 names one ("end state with all `<animate>` removed") but nothing wires it into the README, and the rebuilt page still carries three indefinite loops plus 4–24 s openings. WCAG 2.2.2 (Pause, Stop, Hide) requires a way to stop auto-starting motion longer than 5 s. SMIL in `<img>` has no pause control and GitHub offers none; `<picture>` media queries are the only lever.
4. **Alt texts are too long and in the wrong register.** The draft hero alt is ~75 words, the log ~70, Instruments a 30-item comma list. A screen reader reads alt in full with no way to skip inside it, and GitHub shows alt only when the image fails, so sighted users never see this "marginalia". Standard 12 is wrong as a rule: alt is a replacement, not a caption.
5. **Everything in the sheets is outlines.** Paths are invisible to AT, find-in-page, translation and copy. The name "Ben Russell" exists only in the hero image; the stack only in Instruments; the chart notes with real figures (512, 16 shards, 90%) only on Approaches. Images of text (1.4.5) are tolerable only when the same information is in real text.
6. **Red/green buoys are near-identical in luminance** (1.08:1 day, 1.65:1 night). Fine if shape and number read at 68% scale; at 11px labels they do not. The breaker sector light "lit only when open" is a colour+state encoding with no shape fallback.
7. **Glosses are still partly in-metaphor** ("five corrections", "one session"), and the intro uses "survey", "soundings", "datum" before any plain definition.

## What needs to be done

- **Palette (day only).** `muted` → #56657B (5.1:1 paper, 4.35 land); `accent` → #B8341E for text and small marks (5.1:1), keep #D9442B for fills ≥24px; `ok` → #1F6E42 (5.4:1). Give every feature an ink coastline stroke (≥1px, `ink2`, 8.3:1) so islands and shoals read without the tint; index contours ≥3:1 (about #8A7E62 on cream).
- **Reduced-motion edition: four `<source>`s per `<picture>`**, ordered `(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)`, `(prefers-reduced-motion: reduce)`, `(prefers-color-scheme: dark)`, then `<img>`. Emit it with a `motion=False` flag that strips every `<animate*>`/`<set>` and applies end values. GitHub passes `media` through for `prefers-color-scheme`; whether it honours `prefers-reduced-motion` is undocumented, so **test on a throwaway repo first**.
- **Flash rule for DESIGN.md:** no more than 3 flashes in any second (WCAG 2.3.1), and no flashing area over ~25% of a 10° field (~340×256 px at reading distance). `Fl(3) 10s` is three 0.35 s flashes 1.2 s apart (~0.65 Hz); `Iso 2s` is 0.5 Hz; all lights are dots and small halos. Saturated-red flashes (sector light, red buoys) have a stricter threshold; same limit applies.
- **Alt ≤25 words, plain register, built from stats.** What it is + the one fact. Hero: "Nautical chart of Ben Russell's repositories. 24 islands sized by commits, the six largest named. Chart No. 24, edition 0.1.3." Move the marginalia into a visible `<sub>` caption or `<details><summary>Notes on this sheet</summary>` under each image: that is where voice lives, and sighted readers who cannot decode the chart get it too.
- **Mirror every figure in Markdown.** Put **Ben Russell** as the first two words of the intro paragraph. Put the stack as one mono line under the Instruments sheet. The Approaches chart notes are already bullets; keep the numbers identical.
- **Buoys:** labels ≥13px at 1280, number inside the body; breaker light gets a shape change (open vs closed arc) plus the existing "sector unlit" text.
- **Glosses:** "Soundings <sub>the figures</sub>", "Approaches <sub>the two systems</sub>", "Ship's log <sub>a sample run</sub>", "Notices to mariners <sub>five principles</sub>", "Instruments <sub>languages and stack</sub>", "Other waters <sub>smaller projects</sub>". Define "sounding" in a subordinate clause the first time it appears.

## Improvements and ideas

1. **Phone edition is the frozen edition.** The 720px `<source>` (spec-hero §9) already exists; make it motionless. Phone readers are the most motion-sensitive and cannot see a 9px boat anyway.
2. **A plain-chart block at the top:** `<details><summary>Read this page without the chart</summary>` with the profile in six plain lines (what he builds, two systems, languages, principles, links). Serves screen readers, hiring managers on a phone, and anyone for whom the metaphor is a toll gate.
3. **Bold: the legend is the accessibility statement.** The Approaches legend already defines every symbol. Add two rows: "upright numerals = measured, italic = illustrative" and "colour is never the only signal: red marks are even and conical, green odd and flat", and repeat both sentences in the Colophon. A chart that states its own conventions is honest to a sighted reader and a blind one in the same breath.
4. **Night as the contrast reference.** Derive day colours from night by matching ratios (ink 13:1, muted 5:1, accent 6:1) and assert them in `build_assets.py` from the theme dicts; ten lines, and the palette can never regress.

## What the page says about its maker

Now: a designer with real taste who thinks about a sighted reader on a large screen in a dark room, and who has heard of alt text. The day palette, the outlines-only type and the unstoppable loops say he has not yet sat beside someone using a screen reader or 200% zoom. It should say: this is someone who builds crawlers for a web that lies about itself and holds his own page to the standard he holds the web to, where every encoding has a fallback, every figure is in text, and the chart can be switched off without losing a fact. That is "Keep the log. Raw before clean." applied to himself.

## Five most important lines

1. Day edition small text fails AA: muted 3.77:1, accent 3.77:1, green 3.49:1 on cream; use #56657B / #B8341E / #1F6E42 for text-sized marks. Night passes everywhere.
2. Islands and shoals are 1.18:1 tint-only; give every feature an ink coastline stroke so the portfolio survives low vision and CVD.
3. Add a reduced-motion edition: four `<source>`s per `<picture>` ordered reduce+dark, reduce, dark, img; emit the frozen end state with a `motion=False` flag; test that GitHub passes the media query.
4. Alt ≤25 words, plain register, built from stats; move marginalia into visible `<sub>` captions or `<details>`; mirror the name, the stack and every chart figure in Markdown, because outlined type is invisible to AT.
5. Flash rule for DESIGN.md: ≤3 flashes/s and small area (WCAG 2.3.1); `Fl(3) 10s`, `Fl 4s`, `Iso 2s` and the cursor pass; colour never alone (number parity + shape on buoys, arc shape on the sector light).
