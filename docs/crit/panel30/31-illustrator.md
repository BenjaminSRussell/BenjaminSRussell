# 31 — Illustrator: the drawn objects

Editorial and children's-book illustrator; character in as few marks as possible. I read `boat`, `buoy`, `lateral_mark`, `light_structure`, `wreck`, `anchorage`, `serpent`, `course`, `out_and_back` in chartlib.py, the footer and lighthouse code in `_v8_reference.py`, the boat/serpent/spray paragraphs of the specs, panels 17 and 26; looked at hero-day-2x, footer-night-2x, approach-scrapy-day-2x at 6× crops, and rendered a prototype of the proposal (`scratchpad/crops/boat-proto.svg`). I have not seen the avatar itself, only the brief's description; nothing below invents it.

## 2. What is good

- **The wreck is the best drawing on the page**: a true S-4 hull-and-mast, 1.1px round caps, nothing filled. It looks drawn by the surveyor's pen in the same ink as the soundings. Make it the reference for everything.
- **The anchor** is close behind: open line, one weight, legible at 14px.
- **The accent as the lit thing.** One red sail and a flashing lantern on a navy sheet: the eye knows where the person is. The footer-night boat as the only warm object is right.
- **The serpent idea** (silent, uncaptioned, 2.4 s in 96) is the right kind of moment: a thing you might have imagined.

## 3. What is bad, ranked

1. **The boat is rigged backwards.** `boat()` puts the mast at x=−1 and draws the big sail `M1,-32 L21,-3` *forward* of it toward the bow; the small sail hangs aft. A mainsail cannot be in front of its mast: the boat is sailing stern-first, or that is a flagpole with a flag. This is the avatar's object, on three sheets, wrong in its gesture, which is the first thing an eye reads. (Panel 26 saw the toy; this is why it is one.)
2. **The hull is a symmetrical trapezoid**: no bow, no stern, no sheer, no direction. Every drawn boat since the Bayeux tapestry says "forward" with a raised, raked stem. With `rotate="auto"` on a plan-view chart it also sails uphill (13–25° on hero legs).
3. **The lighthouse is clip art.** A striped tower with a red lantern is the emoji in paper colours, and the only object drawn in a different language (paper fill + outline + stripes) from the wreck and anchor. On a chart a light is a star and a flare; the tower belongs in the harbour inset at most, and even there 42×14 is squat.
4. **Buoys are map pins.** Filled 9–11px shapes with a hairline *under* them read as web-map markers. Chart buoys are canted a few degrees with a position circle at the waterline; the lean says "floating".
5. **The specified serpent is a sine wave with two eyes.** Three identical `c20,-26 40,-26 60,0` humps are a mechanical repeat; two eye dots looking at the reader is a cartoon. A creature tapers, its humps grow toward the head, it has one eye in profile and a gaze with an object (the boat).
6. **Spray is confetti**: seven circles bobbing on linear timers; the lip of the fall is a pipe-bend (`q14,2 18,16 v40`). Water leaving a lip is a parabola; at the base there is mist, not marbles.
7. **Line weight is a different number in every function**: mast 1.4, buoy 0.8, waypoint 1/0.8, wreck 1.1, anchor 1.3, lighthouse 1.2/1.0, sector 0.6–0.9, serpent 2.2; caps on some, not others. On a page whose premise is "one pen", that is the tell that it was generated.
8. **The jib is nearly the hull's colour** (`ink2` beside `ink`), so at README size it merges into the hull as a lump. Three values are needed: hull ink, main accent, jib paper.
9. **"Heel" in a profile drawing is pitch.** The spec's `rotate -3;3;-3` and panel 26's "heel to leeward" both rotate a side view; heel is roll about the long axis and is invisible in profile. You are drawing a bathtub nodding. A profile sloop says "under way" with a steady bow-up trim, full sails and a bow wave; it says "held" with 0°.

## 4. What needs to be done

**One boat, two drawings, chosen by scale.** `boat(ink, sail, paper, scale, detail)`: detail where rendered width ≥ 28px at 1280 (hero, footer), glyph for the packet boat and the phone edition. Origin at the waterline centre, bow right, mast 40% from the bow raked 2° aft, sails on the correct sides. Prototyped and checked at 6×, 1×, 0.68×, 0.37×:

```
DETAIL (11 commands for the silhouette; mast and tiller are two optional strokes)
hull   M-17,-2 L-14,4 L10,4 L18,-6 Q0,-1 -17,-2 Z   fill ink     (transom, keel, raked stem, sheer)
main   M3,-39 Q-9,-24 -15,-7 L3.5,-7 Z               fill accent  (aft of mast, roach on the leech)
jib    M2.5,-34 L17.5,-6 L5,-8 Z                      fill paper, stroke ink .9, linejoin round
mast   M4,-3 L2.5,-40    stroke ink 1.1 round
tiller M-17,-2 L-21,-4   stroke ink 1.1 round
GLYPH (7 commands)
hull   M-8,-1 L-6,3 L5,3 L9,-3 Z     fill ink
main   M2,-3 L1,-20 L-7,-4 Z         fill accent
jib    M1,-17 L8,-4 L2,-4 Z          fill none, stroke ink .9
```

- **Gesture.** No `rotate="auto"` anywhere; mirror with `scale(-1,1)` at the turn. Under way: fixed `rotate(-4)` (bow up) plus the 10 s `sea` translate-y `0;-2;0`. Held: `rotate(0)`. Delete every ±2.5°/±3° rock.
- **Wake and bow wave, profile only** (footer): bow wave `M17,0 q4,-2 7,1` 0.7px; wake `M-16,2 l-14,3 M-16,2 l-12,-1` at .4, fading over 1.5 s when she holds. On the plan-view hero the dotted course *is* the wake; add a 1.2px position dot at the waterline centre so the symbol sits on its fix.
- **Lights as chart grammar.** `light()` = 5-point star r 4 ink + flare `M0,0 q-3,-9 0,-14 q3,5 0,14` rotated 45° in accent .8 + label. Pictorial tower only in the harbour inset, redrawn 5:1, 1.1px taper lines, gallery rail, no stripes, lantern lit only when flashing.
- **Buoys**: outline 1.1 ink, IALA fill .85, body `rotate(8)` about the base, position circle r 1.2 at the waterline, no underline. Shapes stay Region B.
- **Line-weight contract**, three constants: `HAIR 0.6` (graticule, tracks, sectors), `PEN 1.1` (every symbol stroke, mast, course, waypoint), `BRUSH 1.6` (serpent, fall lip). Round caps and joins throughout; the build asserts no other stroke-width inside a symbol group.
- **Serpent** as a creature, three strokes and a dot, humps growing toward a head that faces the boat ahead of it: `M-96,0 c8,-10 18,-10 26,0` · `M-58,0 c10,-20 28,-20 40,0` · `M-6,0 c8,-30 22,-40 34,-34 q6,3 8,10` · eye `circle(24,-32) r1.3`. No mouth. Rise head-first, humps +0.25 s and +0.5 s behind on the same `settle`: a wave passing down a body is what makes it alive.
- **Fall and spray.** Lip `M e,hy c10,0 16,4 19,12 c3,8 4,24 4,42`; fall lines fan 2–8px at the base; three mist arcs `M0,0 q6,-10 14,-6` in HAIR, opacity .5→0 and translate-y 0→−8 over 1.6 s `settle`, staggered on the 10 s grid; at most three of the spec's parabolic droplets.
- **Sail values**: hull `ink`, main `accent`, jib `paper` with an ink outline, both editions.

## 5. Improvements and ideas

1. **The tack is the illustrative moment (bold).** The spec flips the hull with `scale(1,-1)`: a hard frame. Let her go about instead: sail group `animateTransform type="scale" values="1 1;0.06 1;-1 1" keyTimes="0;.5;1" dur="1.2s"` about the mast x, hull `<set>`-mirrored at 0.6 s when the sails are flat and the flip is invisible. Sails luff, then fill on the other side. Sailors know exactly what they saw; everyone else sees a boat turn gracefully. In the footer, when she arrives and holds, the main luffs once (scale 1→0.6→1, 0.8 s). One gesture that could only come from someone who watched a boat.
2. **One pictorial object per sheet**, everything else a PEN-weight symbol. The boat earns the exception because it is the avatar; the moment the lighthouse is pictorial too, the boat stops being special. Write it into DESIGN.md.
3. **The mast's reflection** in the footer: one dashed hairline under the hull, `M3,4 V18`, dasharray `2 3`, opacity .3, moving with the swell. No chart does this; it is one observed detail in the chart's own pen.
4. **Leave the serpent's night eye out of the legend.** Every other accent dot is a labelled light; the one unaccounted for is the second look.
5. **Phone edition uses the glyph at 1.4×**, not the detail boat at 1.15×: a jib outline survives 360px where a mast line does not.

## 6. What the page says about its maker

Now the drawn objects say: someone with a chart book open who has not yet looked at a boat; each symbol written as a function on a different day with a different pen, and the one object that is his rigged backwards and rocking like a toy in a bath. It should say: one hand drew this. Soundings, wreck, buoy, light and serpent share a 1.1px line; the single pictorial thing is his boat, correct in eleven commands, trimmed bow-up when it moves and level when it holds, going about on the far leg with its sails luffing; and once in 96 seconds something rises behind it and looks at it, the only joke, told without a caption.

## 7. Five lines

1. `boat()` is rigged backwards (big sail forward of the mast). Replace with the eleven-command sloop above: raked stem, sheer, transom, main aft of a 2°-raked mast at 40% from the bow, paper jib on the forestay; plus a seven-command glyph, chosen by scale.
2. Drop `rotate="auto"` and all ±3° rocking; a profile boat shows pitch, not heel. Under way: fixed 4° bow-up + 10 s swell lift; held: level. Mirror only at the turn, inside a 1.2 s tack where the sails luff and refill.
3. Lights are a star and a flare, not a striped tower; buoys are canted outlines with a position circle, not filled pins with an underline. One pictorial object per sheet: the boat.
4. One pen: HAIR 0.6 / PEN 1.1 / BRUSH 1.6, round caps everywhere, asserted in the build; the wreck is already right and is the reference.
5. Serpent: tapering humps growing toward a head that faces the boat, one eye, no mouth, rising head-first; spray as three fading mist arcs over a parabolic lip, not seven bobbing circles.
