# 15 — Colour scientist / colour designer

I design and measure palettes (OKLCH, WCAG 2 and APCA, CVD simulation, screen-vs-print appearance). I measured `CHART_LIGHT` / `CHART_DARK` in `scripts/svgkit.py`, the effective colours after the opacities in `chartlib.py` / `_v8_reference.py`, and sampled pixels from hero-day-2x, hero-night-2x, page-day-full, page-night-full. Figures are OKLCH L/C/h, WCAG ratio, APCA Lc.

## What is good

- **The ink/paper pair is right.** Day ink `#1B2A41` L .284 C .047 h 259 on paper `#F4EEE1` L .950 C .018 h 86: a cool ink on a warm paper, near-complementary hues at low chroma, which is why it reads as a printed sheet and not as dark-blue UI. 12.5:1, Lc 91. Night ink on `#0F1A2B` is 13.6:1, Lc 88.
- **The cream reads as paper on GitHub white.** ΔE_ok(paper, #FFFFFF) = .053, about 2.5 JNDs (JND ≈ .02 in OKLab): visible as an object without looking dirty. Night: ΔE_ok(#0F1A2B, #0D1117) = .047 and the hue shift to 259° makes the sheet a navy object on near-black. Correct in both editions.
- **The accent shifts hue and lightness between editions** (day `#D9442B` L .60 h 32 → night `#FF6A3D` L .70 h 37), compensating for the Helmholtz–Kohlrausch effect on dark grounds instead of inverting a hex. This is why the editorial designer found night the stronger edition.

## What is bad (ranked)

1. **Night: text is the brightest thing, not the lights.** Night ink L .916 > green `#4ADE9B` .806 > cool .770 > accent .704. Spec-hero §6 wants "lights the brightest objects" but keeps the palette, so halos will still sit under a 176 px name at Lc −88, a glare slab at bridge brightness. A night chart dims ink and lets lights carry the hierarchy: text to L ≈ .82, lines to ≈ .62, flares at L .74–.85, C ≥ .17.
2. **Red/green marks fail for deuteranopes.** Simulated deuteranopia (Machado): day red → `#958524`, green → `#827B5E`, ΔE_ok .078 with a lightness gap of only .016. At a 9×10 px mark rendered at 6 px they are the same buoy. Night is better (ΔE .119) only because green happens to be .10 lighter. Nun/can shape and R-even/G-odd numbers are the right redundancy and already specified, but the shapes are 6 px and nothing enforces a lightness gap.
3. **The shallow tint is not blue.** `cool #2E6FB0` at .10 over cream composites to `#E0E1DC`: L .908, C .007, h 116, a grey-green ΔE .028 from land `#E6DCC6` (L .897). Only band B (.18 stacked) reaches blue at L .838. Night: band A L .263 vs land .272, the same collision. Alpha-stacking a saturated blue over warm paper is the cause; the result colours must be designed, not derived.
4. **Hatching has no tonal value.** 0.7 px lines, spacing 5, opacity .22 → 14 % coverage, mean L .881 vs land .897: ΔE .016, under one JND. The sampled shoal in hero-day averages `#E5DCC8`, i.e. the land fill. The unsurveyed band (spacing 7, .28) averages L .935 on .950 paper. At 68 % the lines are 0.48 px and antialias into the fill; on a phone they are gone.
5. **Sub-pixel strokes lose contrast proportionally.** Contours at ink .42 are Lc 43; 0.6 px → 0.4 px rendered → effective Lc ≈ 17. The graticule at .10 is already invisible at 870 px. Dotted danger lines at 1.1 px survive.
6. **Readable figures are set like texture.** Soundings at ink .55 = `#7D8289`, Lc 56 at 9.5 px: fine as texture, but 24, 46, 512, 256, 0.1.3 are set identically. Muted `#6B7A90` captions are Lc 60 at 11 px tracked caps; APCA wants Lc ≥ 75 under 14 px.
7. **`cool` does three jobs** (tint, source diagram, language key) and at .14 is the same grey as the tint above.

## What needs to be done

**Palette spec, OKLCH → sRGB.** Day: paper .950/.018/86 `#F4EEE1`; ink .284/.047/259 `#1B2A41`; ink2 .390/.049/257; muted .50/.04/258 (Lc ≥ 75); land .905/.030/85 `#E9DFCA`; shallow A .915/.035/235 `#CEE7F7`; shallow B .870/.060/235 `#AFDBF7`; red nun .58/.20/30 `#D73626`; green can .52/.13/155, deliberately darker than red; flare magenta .56/.23/345 `#C81392`. Night: paper .217/.037/259 `#0F1A2B`; ink text .82/.02/250 `#BBC5D1`; ink2 lines .62/.03/255 `#7A8798`; land .27/.02/250 `#1F2730` (desaturated, so it reads as not-water); shallow A .26/.05/250 `#0F253B`; shallow B .31/.07/250 `#103252`; red nun .72/.20/30 `#FF6853`; green can .82/.17/158 `#45E499`; flare magenta .74/.24/345 `#FF5ACD`; white light .97/.01/90 `#F8F5EE`, the only near-white on the night sheet. Add `shallow_a`, `shallow_b`, `flare` to `Theme`; nothing semantic is derived by alpha.

- **Tints**: paint as opaque result colours, deepest band first, land last, 0.8 px coastline in ink2. Two bands (the 0–6 / 6–18 ft convention) is right; three is noise at 870 px.
- **Night hierarchy**: text `ink` (L .82), rules and contours `ink2`, soundings `ink2` .7. Lights: 3 px core at L ≥ .95 plus a blurred halo in flare/red/green, peak .95. Build assertion: max L of any lit object > max L of any text.
- **Marks for CVD**: nun base 12 px, can 11×13 at 1280 (≥ 8 px rendered), 13 px number labels, the lightness gap above; a deutan+protan simulation in the build fails if any semantic pair has ΔE_ok < .06.
- **Hatch**: spacing 8 (5.4 px rendered), stroke 1.0, ink .45 → ~12 % coverage of a much darker line, apparent ΔL ≈ .045. Foul at spacing 6, unsurveyed at 8, so they remain two textures.
- **Strokes**: contours 0.9 px, index 1.3 px, ink .55; graticule .18; nothing under 0.8 px.
- **Red-orange vs vermilion**: h 32 is already vermilion; keep it for marks, but not for lights. Charts print all flares magenta because under a red lamp red → `#D90802` (L .56), green → `#2F1105` (black), paper → `#F41D0B`, while magenta keeps L .51 and separates from both. Magenta flares with the colour written in the character ("Fl R 4s") is the real grammar, and it gives the night edition its one new hue.

## Improvements and ideas

1. **Colour CI (bold).** `build_assets.py` renders each sheet at 870 and 360 px, converts to OKLab and asserts: every semantic pair ΔE ≥ .06 under normal, deutan and protan vision; hatch differs from its fill by ΔL ≥ .04; readable soundings Lc ≥ 75; night lights brighter than text. The colophon says it once: "colours checked for two kinds of colour-blindness on every build."
2. **Depth as a data-fed tint scale.** Band thresholds from commit quantiles, printed in the legend as "≤ 5 · ≤ 10 commits/wk". Depth-is-trust becomes colour, not caption.
3. **Paper, not flat fill.** A 2 % warm radial fall-off toward the neat line (a gradient; feTurbulence is too costly under SMIL) and a half-tone cream outside the neat line, so the sheet has a surface. Night gets a 2 % cooler centre.
4. **Magenta wherever something is lit at night**: flares, the log cursor, the HW dot on the tide curve. Red stays for marks; orange disappears.

## What the page says

Now: someone with real palette discipline who chose a beautiful ink and paper, then let alpha compositing and sub-pixel strokes decide the actual colours, so shoals, tints and hatching are one grey and the night chart glares where it should glow. Should: someone who designs colour as a measured result, whose sheet passes the tests a hydrographic office applies (magenta lights, buff land, blue shallows, legible in red light and to a colour-blind mate), and who says so in one line.

## Five most important lines

1. Night inverts the hierarchy: text L .916 outshines every light (green .806, accent .704); drop night ink to L .82, lines to .62, lights to L .74–.85 with halos, and assert lights > text in the build.
2. Shallow tint A composites to `#E0E1DC` (h 116, grey-green), ΔE .028 from land; design band colours as opaque OKLCH results (`#CEE7F7` / `#AFDBF7` day, `#0F253B` / `#103252` night), two bands, land last with a coastline.
3. Red/green marks are ΔE_ok .078 for deuteranopes with a .016 lightness gap; keep nun/can + numbers, enforce the L gap (green darker by .06 day, lighter by .10 night), marks ≥ 8 px rendered, deutan check in CI.
4. Hatching averages ΔL .016 from its fill (sub-JND) and vanishes at 68 %; use spacing 8, stroke 1.0, ink .45 for apparent ΔL ≈ .045; contours ≥ 0.9 px at ink .55.
5. Keep vermilion (h 32) for marks and print every light flare magenta (.56/.23/345 day, .74/.24/345 night) as real charts do; it survives red light and is the night edition's one new colour.
