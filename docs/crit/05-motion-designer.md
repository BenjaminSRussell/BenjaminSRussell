# 05 · Motion designer — choreography crit of "Chart" v8

## 1. First impression

The stills are composed; the motion is not. Nothing here is choreographed: every loop starts at t=0 with no relation to any other, every curve is linear, and the page never has a moment where the chart *comes alive*. It moves the way a screensaver moves, not the way a system does.

## 2. What works

The restraint. Five slow things on a quiet page is the right budget, and 48 s for the hero boat is the right order of magnitude. The survey and the log are the right *ideas*: soundings appearing in order and a session typing itself are motion that means something. The `<use>`-based glyphs keep the animated sheets light enough that this is fixable without a size fight.

## 3. Problems, ranked by impact

1. **No opening sequence.** Zero `begin=` chains, zero `fill="freeze"`, zero `keySplines` in the whole build. The page loads fully drawn and then idles. The one thing a chart of the open web should do on first load is *survey itself*: contours tracing, soundings being taken, the name being set. Right now the hero is 275 KB of static ink with a 9 px boat crawling on it.
2. **Empty-state still frames.** The survey (`LOOP=14`) wipes everything at 0.95 and the right half of the sheet is blank from 13.3 s to 14.6 s; the log is a blank ledger for its first 0.4 s and again at the wrap. Screenshots, social previews and anyone glancing at the wrong second get an unfinished sheet. A loop must be designed so *every* frame is composed.
3. **Linear everywhere.** Footer boat bobbing is a `rotate -2.5;2.5;-2.5` triangle wave; spray droplets rise and fall at constant velocity (water is parabolic); the crawl bar fills at constant speed (crawls are bursty); typing is a smooth clip wipe that slices through glyph bowls instead of landing character by character. This is the single biggest "low effort" tell for anyone who notices motion.
4. **Hard seams.** Hero boat teleports from the last waypoint to the first every 48 s; the packet boat snaps back every 16 s; the footer boat, captioned "never quite gets there", jumps 900 px backwards every 70 s, contradicting its own caption. The WAL tape (7 s) fills then slams back to 0.2 opacity.
5. **Motion that lies on a chart that is otherwise honest.** The light is labelled `Fl(3) 10s` but rendered as a continuously rotating 9 s beam, sweeping across land. A chart reader sees the mismatch immediately. The hero boat uses `calcMode="linear"` without `keyPoints`, so it moves at different speeds per Bézier segment for no reason (drop the attribute; `paced` is the default and the right one).
6. **Survey vessel doesn't survey.** The soundings appear along a fan but the boat sits still and nothing connects the two. The WAL tape runs twice per loop, unrelated to how many soundings exist.
7. **No shared timing scale.** Durations in play: 1.1, 4, 6, 7, 9, 14, 16, 48, 70. Nothing ever phase-aligns, so the page is a roomful of clocks.
8. **Performance shape is backwards.** An SVG with SMIL inside `<img>` is re-rasterised every frame it changes. The indefinite loops sit on the heaviest sheet (hero: ~180 paths + hundreds of `<use>`) while the lightest sheet (footer, 28 KB) could carry ambient motion for free. Seven sheets animating forever is also the mobile battery case.

## 4. Expectations: what "months of team work" looks like

- A **motion spec** in DESIGN.md: three principles, one timing scale, three named easings, and a table of every animated element with its duration, delay, easing, and loop behaviour.
- **One-shot opening, ambient after.** First 4 s: the system draws itself in dependency order. After that, one or two slow loops per sheet, nothing more.
- **Still-frame test**: scrub each SVG at 0, 25, 50, 75, 99 % of its longest loop; every frame must look like a finished sheet. Automate it with resvg at those times in `build_assets.py`.
- **Light characters are real.** Every lit mark on the chart flashes its labelled rhythm. If the label says `Fl(3) 10s`, the light does three 0.3 s flashes in 10 s.
- **Reduced motion edition.** `<picture>` already switches on `prefers-color-scheme`; add `<source media="(prefers-reduced-motion: reduce)">` pointing at frozen editions (build with the opening at `fill="freeze"` and loops removed). Verify GitHub's sanitiser keeps the media query; it is the same attribute path as the scheme switch.
- **Budget**: ≤ 60 animated elements per sheet, ≤ 2 indefinite animations on the hero after the opening.

## 5. Proposals (ranked)

### Motion system

**Principles.** (1) Motion is survey work: things appear because the boat has been there. (2) Nothing loops that could freeze; nothing freezes that should breathe. (3) Rhythm is nautical: light characters, tide, swell.

**Timing scale** (ms): 150 · 250 · 400 · 650 · 1000 · 1600 · 2600 for transitions; 10 s · 24 s · 48 s · 96 s for loops (all divide into 96 s, so sheets phase-align every 96 s).

**Easings** (keySplines):
- `settle` = `0.16 0.84 0.44 1` (fast out, long landing; for things arriving)
- `draw` = `0.4 0 0.2 1` (pen on paper; for stroke tracing)
- `sea` = `0.37 0 0.63 1` (sinusoidal; the only easing allowed on loops)

### Per-sheet choreography

**P1 · Hero: the chart surveys itself (the "oh").** Order is meaning: water first, then marks, then the name, then the boat sails. Give every contour `pathLength="1"` so one dash value works for all lengths, and stagger by level so deep water draws first:

```xml
<path d="…" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">
  <animate id="c0" attributeName="stroke-dashoffset" to="0" dur="1.6s"
    begin="0.2s" calcMode="spline" keySplines="0.4 0 0.2 1" fill="freeze"/>
</path>
<!-- level i: begin="{0.2 + i*0.12}s" -->
```

Soundings then appear in the order the boat will pass them (sort by projection onto the course), 40 ms apart, each a 250 ms `settle` fade with a 3 px rise. Name at 2.6 s: a 650 ms clip reveal left-to-right (a nib, not a wipe through glyphs: use `calcMode="discrete"` per word, three steps). Cartouche rules draw last. Boat starts at `begin="name.end+0.4s"`, sails **out and back** so there is no seam and no empty frame:

```xml
<animateMotion dur="96s" repeatCount="indefinite" rotate="auto" path="{sd}"
  keyPoints="0;1;1;0;0" keyTimes="0;0.44;0.5;0.94;1"
  calcMode="spline" keySplines="0.37 0 0.63 1;0 0 1 1;0.37 0 0.63 1;0 0 1 1"/>
```
Add a 4 s `sea` heel of ±3° on the hull group, and swap the sail path with `<set>` at the turn so it tacks.

**P2 · Survey: the lead line.** The vessel moves. Nine short `animateMotion` legs along the fan (one per survey line, 2.6 s each, `settle`), chained `begin="leg3.end+0.4s"`. A 300 ms vertical dash drops from the hull at each stop; the sounding nearest the boat appears on `begin="drop.end"`. Contours fade in at 0.6 opacity *after* the last line, and **freeze**. The WAL tape advances one cell per sounding taken, not on its own clock. The second loop is just the boat idling at the last station with a 10 s `sea` bob. No wipe, ever.

**P3 · Approach: real light characters (a layer of meaning).** Replace the rotating wedge with the labelled rhythm:

```xml
<animate attributeName="opacity" values="0;1;0;1;0;1;0;0"
  keyTimes="0;.03;.06;.13;.16;.23;.26;1" dur="10s" repeatCount="indefinite"/>
```
Buoys get `Fl R 4s` / `Fl G 4s` halos, offset 2 s so the channel blinks alternately like a real fairway. The "breaker closed" dot pulses on the same 10 s as the light: the health check *is* the lighthouse. Packet boat runs the channel with `settle` into the anchorage, holds 6 s, fades 400 ms, reappears at open water: no snap.

**P4 · Log: discrete typing, bursty crawl, never blank.** Per-character reveal with `calcMode="discrete"` and jittered keyTimes (60–110 ms per glyph, 240 ms after spaces). Crawl bar in three bursts via keySplines (`0 0 .2 1` then plateaus) while "12,044 → 31,870 → 48,213" swap with discrete opacity. Make the whole session a **one-shot with `fill="freeze"`**; the only loop is the final cursor (`sea`, 1.1 s). The sheet is complete forever after 14 s instead of wiping every 14 s.

**P5 · Soundings sheet: tide draws in.** Currently inert. Tide curve traces with `pathLength="1"` over 1.6 s `draw`; figures rise from a clip 400 ms each, staggered 120 ms; language bar segments fill in sequence. All frozen after 3 s.

**P6 · Footer: the second-look reward.** Boat approaches the edge with `settle` over 24 s and freezes 60 px short, bobbing on `sea`. Then every 96 s, for 2.4 s, a single dark arc (three Béziers, two dots for eyes) rises from the swell behind the boat and sinks: *Here be dragons*, honoured once a minute and a half. `begin="arrive.end+72s; dragon.end+94s"`. Droplets become parabolic (`keySplines="0.33 0 0.67 1"` up, inverse down).

**P7 · Delight: the compass settles.** On load the needle overshoots north by 12° and damps back over 1.6 s (three keyTimes, `sea`). Every 96 s a 3° swing: the chart is on a boat.

### Performance and mobile

- After the opening, only three indefinite animations remain on the page: hero boat, lighthouse character, footer bob. Survey, log and soundings freeze. This cuts per-frame raster from seven sheets to three, and the heavy hero carries one small moving group.
- Keep opening animations under 4 s; frozen SMIL is near-free.
- Mobile at 360 px: soundings are 2.7 px, so the opening must read as *texture appearing*, which the ordered stagger does. Typing is unreadable at that size; the crawl bar and green checks carry the log, so give them the strongest easing.
- Avoid animating `patternTransform` (inconsistent in WebKit); the hatch stays still.

## 6. What it says now vs. what it should say

Now: someone who knows SMIL exists and added motion as a final pass. The chart metaphor is carried entirely by the drawing; the motion contradicts it (a sweeping light labelled as a flasher, a boat that teleports under "never gets there").

Should: someone who understands that on a chart every mark has a rhythm, and who choreographed the page so that it is surveyed in front of you, settles into a composed still, and rewards the person who stays. That is the difference between "animated" and "alive".
