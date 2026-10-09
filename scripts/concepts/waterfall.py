"""waterfall.py — concept still 2, "The waterfall" (round 4, D9; crit-method §3 concept 2).

One illustration, no diagram: the sloop at the edge where the charted web ends and the water falls off
the sheet, the thesis, the name as a chart title block, the unsurveyed hatch beyond the edge. The only
figures on the sheet are the title block's (repositories, commits, the survey years), all from
assets/stats.json; every line of copy is chart.toml's.

    python3 scripts/concepts/waterfall.py        → concepts/waterfall.svg
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _concept import Concept, S, op, Jitter, hatch, fmt, day, thousands  # noqa: E402

W, H = 1280, 700
c = Concept("waterfall")
th = c.theme
st = c.stats
jit = Jitter(c.cfg["chart"]["seed"], "concept/waterfall")
thesis = c.cfg["copy"]["thesis"]
ends_here = c.cfg["copy"]["footer_line"]

y0, y1 = day(st["first_commit"]).year, c.taken.year
NEAT0, NEAT1 = 18, 24
SEA_Y = 352          # the horizon
EDGE_X = 952         # where the water leaves the chart
FOOT_Y = H - NEAT1   # the inner neat line at the bottom; the fall runs through it
HATCH_X = 1030

body: list[str] = []
defs: list[str] = []


# ------------------------------------------------------------------ the sea, engraved
# The water is drawn the way an engraver draws it: ruled lines, close at the horizon and opening toward
# the foot of the sheet, each broken by hand, and every one of them bends over the lip and falls. There is
# no other sea: the lines are the water, and all of it leaves the chart.
def path_of(pts) -> str:
    return "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}" for i, (x, y) in enumerate(pts))

LIP = EDGE_X - 16
# the body of the water, one tint: horizon → lip → the curl → the foot
body.append(f'<path d="M{NEAT1} {SEA_Y}H{LIP}Q{EDGE_X + 6} {SEA_Y + 2} {EDGE_X + 12} {SEA_Y + 40}'
            f'L{EDGE_X + 30} {FOOT_Y}H{NEAT1}Z" fill="{th.shallow_a}"/>')
body.append(f'<path d="M{LIP - 60} {SEA_Y}H{LIP}Q{EDGE_X + 6} {SEA_Y + 2} {EDGE_X + 12} {SEA_Y + 40}'
            f'L{EDGE_X + 30} {FOOT_Y}H{EDGE_X - 10}Q{EDGE_X - 30} {SEA_Y + 120} {LIP - 60} {SEA_Y + 14}Z" '
            f'fill="{th.shallow_b}" fill-opacity=".5"/>')

lines_far, lines_near, falls, falls_paper = [], [], [], []
g = jit.sub("engrave")
y = SEA_Y + 3.0
step = 4.2
i = 0
while y < FOOT_Y - 2:
    amp = 0.5 + 0.03 * i
    wl = 46 + 2.4 * i
    phase = g.uniform(0, 2 * math.pi)
    # 1–4 segments with hand gaps; the first lines at the horizon run unbroken
    segs = 1 if i < 3 else int(g.uniform(2, 5))
    cuts = sorted(g.uniform(NEAT1 + 10, LIP - 40) for _ in range(2 * (segs - 1)))
    bounds = [NEAT1 + g.uniform(0, 30)] + cuts + [LIP]
    d = []
    for k in range(0, len(bounds), 2):
        x0, x1 = bounds[k], bounds[k + 1]
        if x1 - x0 < 24:
            continue
        pts = []
        x = x0
        while x < x1:
            pts.append((x, y + amp * math.sin(x / wl * 2 * math.pi + phase)))
            x += 10
        pts.append((x1, y + amp * math.sin(x1 / wl * 2 * math.pi + phase)))
        d.append(path_of(pts))
    # every line that reaches the lip goes over it
    reach = bounds[-2] <= LIP - 24
    if reach:
        fan = 4 + 20 * (1 - (y - SEA_Y) / (FOOT_Y - SEA_Y)) + g.offset(2.5)
        d.append(f"M{LIP} {fmt(y)}Q{EDGE_X + 4} {fmt(y + 1)} {fmt(EDGE_X + 6 + fan * 0.35)} {fmt(y + 34)}"
                 f"Q{fmt(EDGE_X + 8 + fan * 0.7)} {fmt((y + FOOT_Y) / 2 + 40)} {fmt(EDGE_X + 10 + fan)} {FOOT_Y + 8}")
    (lines_near if i > 18 else lines_far).append("".join(d))
    y += step
    step *= 1.028
    i += 1
body.append(f'<path d="{"".join(lines_far)}" fill="none" {S("HAIR", th.ink2, 0.62)}/>')
body.append(f'<path d="{"".join(lines_near)}" fill="none" {S("PEN", th.ink2, 0.5)}/>')
# the horizon, PEN ink, over the lip
body.append(f'<path d="M{NEAT1} {SEA_Y}H{LIP}Q{EDGE_X + 6} {SEA_Y + 2} {EDGE_X + 12} {SEA_Y + 40}" fill="none" '
            f'{S("PEN", th.ink, 0.9)}/>')
# a few paper streaks in the fall, so it reads as water and not as ruling
for k in range(6):
    x = EDGE_X + 9 + k * 4.2 + g.offset(1.2)
    top = SEA_Y + 50 + g.uniform(0, 120)
    falls_paper.append(f"M{fmt(x)} {fmt(top)}Q{fmt(x + 3)} {fmt((top + FOOT_Y) / 2)} {fmt(x + 8 + k)} {FOOT_Y + 8}")
body.append(f'<path d="{"".join(falls_paper)}" fill="none" {S("PEN", th.paper, 0.85, caps="butt")}/>')
# mist: arcs rising at the foot, HAIR, fading
mist = []
for i, (cx, cy, r) in enumerate(((EDGE_X + 36, FOOT_Y - 2, 34), (EDGE_X + 58, FOOT_Y - 8, 56), (EDGE_X + 24, FOOT_Y - 14, 82),
                                 (EDGE_X + 76, FOOT_Y - 24, 104))):
    a0, a1 = math.radians(196 + g.uniform(-8, 8)), math.radians(334 + g.uniform(-8, 8))
    mist.append((f"M{fmt(cx + r*math.cos(a0))} {fmt(cy + r*math.sin(a0))}A{r} {r} 0 0 1 "
                 f"{fmt(cx + r*math.cos(a1))} {fmt(cy + r*math.sin(a1))}", 0.55 - i * 0.1))
for d, o in mist:
    body.append(f'<path d="{d}" fill="none" {S("HAIR", th.ink2, o)}/>')

# ------------------------------------------------------------------ the unsurveyed, beyond the edge
hd, hb = hatch((HATCH_X, NEAT1, W - NEAT1 - HATCH_X, FOOT_Y - NEAT1), th, jit.sub("band"), "unsurveyed",
               "waterfall-unsurv", ramp=(HATCH_X, HATCH_X + 70))
defs.append(hd)
body.append(hb)
body.append(c.t("UNSURVEYED", HATCH_X + (W - NEAT1 - HATCH_X) * 0.62, 350, "label-caps", tracking=1.6,
                anchor="middle", rotate=-90))
# the limit, pecked, from the sky down to the lip; its label reads up the line
body.append(f'<path d="M{EDGE_X} {NEAT1 + 40}V{SEA_Y - 40}" fill="none" {S("PEN", th.ink, 0.8, "LIMIT", caps="butt")}/>')
body.append(c.t(f"LIMIT OF SURVEY {y1}", EDGE_X - 10, (NEAT1 + 40 + SEA_Y) / 2 - 30, "label", anchor="middle", rotate=-90))

# ------------------------------------------------------------------ the course in, and the sloop at the edge
# a pecked course along the surface, bearing for the edge
course = []
x = NEAT1 + 60
while x < EDGE_X - 200:
    course.append(f"M{fmt(x)} {fmt(SEA_Y + 52 + 0.03 * (x - NEAT1))}h5")
    x += 12
body.append(f'<path d="{"".join(course)}" fill="none" {S("PEN", th.ink2, 0.6, caps="butt")}/>')

SC = 3.6
BX, BY = EDGE_X - 96, SEA_Y + 80
hull = "M-17 -2L-14 4L10 4L18 -6Q0 -1 -17 -2Z"
main = "M3 -39Q-9 -24 -15 -7L3.5 -7Z"
jib = "M2.5 -34L17.5 -6L5 -8Z"
mast = "M4 -3L2.5 -40M-17 -2L-21 -4"
pennant = "M2.5 -40.5l-7 -2.2l7 -1.6"
pen = 1.3 / SC
body.append(f'<g transform="translate({BX} {BY}) scale({SC})">'
            # the wake and bow wave, under the hull
            f'<path d="M-24 1q4 -1.5 8 0M22 -4q-3 -1 -5 2" fill="none" stroke="{th.ink2}" stroke-width="{fmt(pen, 2)}" stroke-opacity=".6" stroke-linecap="round"/>'
            f'<path d="{hull}" fill="{th.ink}"/>'
            f'<path d="{main}" fill="{th.accent}"/>'
            f'<path d="{jib}" fill="{th.paper}" stroke="{th.ink}" stroke-width="{fmt(pen, 2)}" stroke-linejoin="round"/>'
            f'<path d="{mast}" fill="none" stroke="{th.ink}" stroke-width="{fmt(pen, 2)}" stroke-linecap="round"/>'
            f'<path d="{pennant}" fill="{th.accent}"/>'
            f'<circle r="0.35" fill="{th.ink}"/>'
            '</g>')
# the one note on the water, under the hull, where a chart would print "good holding"
# the one note, in the sky at the brink, short of the sail
body.append(c.t(ends_here, BX - 72, SEA_Y - 18, "note", fill=th.ink2, anchor="end"))

# ------------------------------------------------------------------ title block (the sky)
nx, ny = 56, 190
ben = c.t("Ben", nx, ny, "display")
wb = c.w("Ben ", "display")
body.append(ben + c.t("Russell", nx + wb, ny, "display"))
body.append(c.t(thesis, 60, 250, "thesis", fill=th.ink2))
body.append(c.t(f"CHART OF {st['repo_count']} REPOSITORIES · {thousands(st['commits'])} COMMITS · SURVEYS {y0}–{y1}",
                60, 292, "label-caps", tracking=1.6, fill=th.ink2))

# ------------------------------------------------------------------ neat line, broken where the water leaves
# outer LINE rule: top, left, bottom to the fall; right side only above the surface
body.append(f'<path d="M{W-NEAT0} {NEAT0}H{NEAT0}V{H-NEAT0}H{EDGE_X - 6}M{EDGE_X + 60} {H-NEAT0}H{W-NEAT0}V{NEAT0}" '
            f'fill="none" {S("LINE", th.ink, 0.9, caps="butt")}/>')
body.append(f'<path d="M{W-NEAT1} {NEAT1}H{NEAT1}V{H-NEAT1}H{EDGE_X - 6}M{EDGE_X + 60} {H-NEAT1}H{W-NEAT1}V{NEAT1}" '
            f'fill="none" {S("HAIR", th.ink, 0.6, caps="butt")}/>')

c.write("concepts/waterfall.svg", W, H, "".join(body), "".join(defs),
        title=f"Ben Russell. {thesis} A sloop at the edge where the charted web ends and the water falls off the sheet.")
