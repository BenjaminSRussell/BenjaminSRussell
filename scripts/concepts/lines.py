"""lines.py — concept still 3, "The survey lines" (round 4, D9; crit-infodesign §4).

One strip plot: one row per repository sorted by commit-days (the ten with most named, the rest on one
grouped row), x = Sep 2025 → the survey date, one dot per commit-day with area ∝ commits that day
(repos[].days from stats.json), name at left with commit-days · months · commits upright, sweep days as
pecked verticals labelled with their repo count and date, the hatched margin right of today as the
unsurveyed, and the 24-hour rose as a radial histogram of commit-days by hour. Name and thesis as the
title block. Every figure is from assets/stats.json; the thesis from chart.toml.

    python3 scripts/concepts/lines.py            → concepts/lines.svg
"""
from __future__ import annotations

import datetime as dt
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _concept import Concept, S, op, Jitter, hatch, fmt, day, long_date, thousands, MONTHS  # noqa: E402

W, H = 1280, 760
NAMED = 10

c = Concept("lines")
th = c.theme
st = c.stats
jit = Jitter(c.cfg["chart"]["seed"], "concept/lines")
thesis = c.cfg["copy"]["thesis"]

# ------------------------------------------------------------------ data
repos = sorted(st["repos"], key=lambda r: (-r["commit_days"], -r["commits"], r["name"]))
named, rest = repos[:NAMED], repos[NAMED:]
taken = c.taken
start = dt.date(2025, 9, 1)
span_days = (taken - start).days

X0, X1 = 604, 1150               # Sep 1 2025 → today
HX1 = W - 18                     # hatch to the sheet edge (the neat line is cut there)
ROW0, PITCH = 318, 33
rows = named + ([{"group": True, "repos": rest}] if rest else [])
Y_AXIS = ROW0 + PITCH * len(rows) + 2

def xd(d: dt.date | str) -> float:
    d = day(d) if isinstance(d, str) else d
    return X0 + (X1 - X0) * (d - start).days / span_days

def radius(n: int) -> float:
    return 1.55 * math.sqrt(n)


body: list[str] = []
defs: list[str] = []

# ------------------------------------------------------------------ neat line (double rule)
body.append(f'<path d="M18 18H{W-18}V{H-18}H18Z" fill="none" {S("LINE", th.ink, 0.9, caps="butt")}/>')
body.append(f'<path d="M24 24H{W-24}V{H-24}H24Z" fill="none" {S("HAIR", th.ink, 0.6, caps="butt")}/>')

# ------------------------------------------------------------------ title block
nx, ny = 56, 160
ben = c.t("Ben", nx, ny, "display")
wb = c.w("Ben ", "display")
body.append(ben + c.t("Russell", nx + wb, ny, "display"))
body.append(c.t(thesis, 60, 214, "thesis", fill=th.ink2))
sum_days = sum(r["commit_days"] for r in repos)
body.append(c.t(f"SURVEY LINES · {st['repo_count']} REPOSITORIES · {sum_days} COMMIT-DAYS · "
                f"{thousands(st['commits'])} COMMITS · SEP 2025 – {MONTHS[taken.month-1].upper()} {taken.year}",
                60, 250, "label-caps", tracking=1.6, fill=th.ink2))

# ------------------------------------------------------------------ the rose: commit-days by hour
RX, RY, RR = 1120, 128, 64
hours = st["hours"]
hmax = max(hours)
modal = st["variation"]["hour"]
rose = [f'<circle cx="{RX}" cy="{RY}" r="{RR}" fill="none" {S("HAIR", th.ink, 0.6)}/>',
        f'<circle cx="{RX}" cy="{RY}" r="{fmt(RR*0.22)}" fill="none" {S("HAIR", th.ink, 0.45)}/>']
# 24 wedges, length ∝ commit-days in that hour (a radial histogram: the quantity is in the bar length)
wedges = []
r_in = RR * 0.22
for h, n in enumerate(hours):
    a0 = math.radians(h * 15 - 90 - 6.2)
    a1 = math.radians(h * 15 - 90 + 6.2)
    r1 = r_in + (RR - 6 - r_in) * n / hmax
    p = (f"M{fmt(RX + r_in*math.cos(a0))} {fmt(RY + r_in*math.sin(a0))}"
         f"L{fmt(RX + r1*math.cos(a0))} {fmt(RY + r1*math.sin(a0))}"
         f"A{fmt(r1)} {fmt(r1)} 0 0 1 {fmt(RX + r1*math.cos(a1))} {fmt(RY + r1*math.sin(a1))}"
         f"L{fmt(RX + r_in*math.cos(a1))} {fmt(RY + r_in*math.sin(a1))}Z")
    wedges.append((p, h == modal))
rose.append(f'<path d="{"".join(p for p, m in wedges if not m)}" fill="{th.shallow_b}" {S("PEN", th.ink, 0.85, caps="butt")}/>')
rose.append(f'<path d="{"".join(p for p, m in wedges if m)}" fill="{th.accent}" fill-opacity=".85" {S("PEN", th.ink, 0.85, caps="butt")}/>')
# hour ticks on the ring, the four cardinal hours lettered
tk = []
for h in range(24):
    a = math.radians(h * 15 - 90)
    L = 7 if h % 6 == 0 else 3.5
    tk.append(f"M{fmt(RX + RR*math.cos(a))} {fmt(RY + RR*math.sin(a))}l{fmt(L*math.cos(a))} {fmt(L*math.sin(a))}")
rose.append(f'<path d="{"".join(tk)}" fill="none" {S("HAIR", th.ink, 0.8, caps="butt")}/>')
rose.append(c.t("00", RX, RY - RR - 12, "label", anchor="middle"))
rose.append(c.t("12", RX, RY + RR + 24, "label", anchor="middle"))
rose.append(c.t("06", RX + RR + 13, RY + 6, "label"))
rose.append(c.t("18", RX - RR - 13, RY + 6, "label", anchor="end"))
rose.append(c.t("COMMIT-DAYS BY HOUR", RX - RR - 44, RY - 4, "label-caps", tracking=1.6, anchor="end", fill=th.ink2))
rose.append(c.t(f"author-local · most at {modal}h ({hmax} days)", RX - RR - 44, RY + 18, "label-italic",
                anchor="end", fill=th.muted))
body.extend(rose)

# ------------------------------------------------------------------ column heads
HEAD_Y = ROW0 - 24
COL_DAYS, COL_MONTHS, COL_COMMITS = 372, 468, 576
body.append(c.t("REPOSITORY", 60, HEAD_Y, "label-caps", tracking=1.6, fill=th.ink2))
body.append(c.t("DAYS", COL_DAYS, HEAD_Y, "label-caps", tracking=1.6, anchor="end", fill=th.ink2))
body.append(c.t("MONTHS", COL_MONTHS, HEAD_Y, "label-caps", tracking=1.6, anchor="end", fill=th.ink2))
body.append(c.t("COMMITS", COL_COMMITS, HEAD_Y, "label-caps", tracking=1.6, anchor="end", fill=th.ink2))
body.append(f'<path d="M60 {HEAD_Y+9}H{X1}" fill="none" {S("HAIR", th.ink, 0.6, caps="butt")}/>')

# ------------------------------------------------------------------ rows
row_rules, dots_d = [], []
for i, r in enumerate(rows):
    y = ROW0 + PITCH * i + PITCH / 2
    row_rules.append(f"M{X0} {fmt(y)}H{X1}")
    yb = y + 8                                   # text baseline for a 25/19 run centred on the row
    if r.get("group"):
        rs = r["repos"]
        n_days = sum(q["commit_days"] for q in rs)
        n_commits = sum(q["commits"] for q in rs)
        body.append(c.t(f"{len(rs)} more repositories", 60, yb, "place-water", fill=th.ink2))
        body.append(c.t(str(n_days), COL_DAYS, yb, "label", anchor="end"))
        body.append(c.t("–", COL_MONTHS, yb, "label", anchor="end", fill=th.muted))
        body.append(c.t(thousands(n_commits), COL_COMMITS, yb, "label", anchor="end"))
        days = [d for q in rs for d in q["days"]]
    else:
        nm = r["name"]
        body.append(c.t(nm, 60, yb, "place-land"))
        known = {"Rust-sitemap": "rustmapper", "Scrapy": "Scrapy Harbor"}.get(nm)
        if known:
            body.append(c.t(known, 60 + c.w(nm, "place-land") + 8, yb, "label-italic", fill=th.muted))
        body.append(c.t(str(r["commit_days"]), COL_DAYS, yb, "label", anchor="end"))
        body.append(c.t(str(r["months_active"]), COL_MONTHS, yb, "label", anchor="end"))
        body.append(c.t(thousands(r["commits"]), COL_COMMITS, yb, "label", anchor="end"))
        days = r["days"]
    for d in days:
        dots_d.append(f'<circle cx="{fmt(xd(d["d"]))}" cy="{fmt(y)}" r="{fmt(radius(d["n"]))}"/>')
body.append(f'<path d="{"".join(row_rules)}" fill="none" {S("HAIR", th.ink, 0.35, caps="butt")}/>')

# ------------------------------------------------------------------ sweeps (pecked verticals through every row)
Y_TOP, Y_BOT = ROW0 - 4, Y_AXIS - 4
sweeps = sorted(st["sweeps"], key=lambda s: s["date"])
sw_d = []
for s in sweeps:
    x = xd(s["date"])
    sw_d.append(f"M{fmt(x)} {Y_TOP}V{Y_BOT}")
body.append(f'<path d="{"".join(sw_d)}" fill="none" {S("PEN", th.accent, 0.9, "PECK", caps="butt")}/>')
# labels: adjacent sweeps share one label; the sweep on the survey date reads to the left of its line
def sweep_label(group: list[dict]) -> str:
    """'sweep · 18 repos · 7 Oct'; the year is on the axis below."""
    if len(group) == 1:
        s = group[0]
        d = day(s["date"])
        return f"sweep · {s['repos']} repos · {d.day} {MONTHS[d.month-1]}"
    counts = " and ".join(str(s["repos"]) for s in group)
    d0, d1 = day(group[0]["date"]), day(group[-1]["date"])
    when = f"{d0.day}–{d1.day} {MONTHS[d1.month-1]}" if d0.month == d1.month else f"{d0.day} {MONTHS[d0.month-1]} – {d1.day} {MONTHS[d1.month-1]}"
    return f"sweeps · {counts} repos · {when}"

groups: list[list[dict]] = []
for s in sweeps:
    if groups and (day(s["date"]) - day(groups[-1][-1]["date"])).days <= 2:
        groups[-1].append(s)
    else:
        groups.append([s])
# labels sit above the plot; a sweep within ten days of the survey date reads leftward from its line, the
# latest on the lower tier and the one before it on the upper tier, so neither runs into the other
recent = [g for g in groups if day(g[-1]["date"]) >= taken - dt.timedelta(days=10)]
for g in groups:
    x = xd(g[-1]["date"])
    txt = sweep_label(g)
    if g in recent:
        tier = Y_TOP - 30 if g is recent[-1] else Y_TOP - 52
        body.append(c.t(txt, xd(recent[-1][-1]["date"]) - 6, tier, "label", anchor="end", fill=th.accent))
    else:
        body.append(c.t(txt, x + 7, Y_TOP - 8, "label", fill=th.accent))

# ------------------------------------------------------------------ the dots (over the sweeps, under nothing)
body.append(f'<g fill="{th.ink}" fill-opacity=".48">{"".join(dots_d)}</g>')

# ------------------------------------------------------------------ the unsurveyed margin (right of today)
hd, hb = hatch((X1, ROW0 - 30, HX1 - X1, Y_AXIS + 30 - (ROW0 - 30)), th, jit.sub("band"), "unsurveyed", "lines-unsurv",
               ramp=(X1, X1 + 30))
defs.append(hd)
body.append(hb)
body.append(f'<path d="M{X1} {ROW0-30}V{Y_AXIS+30}" fill="none" {S("PEN", th.ink, 0.9, "LIMIT", caps="butt")}/>')
body.append(c.t(f"LIMIT OF SURVEY · {long_date(taken).upper()}", X1 + 46, (ROW0 + Y_AXIS) / 2, "label-caps",
                tracking=1.6, anchor="middle", rotate=-90))
body.append(c.t("UNSURVEYED", X1 + (HX1 - X1) * 0.86, (ROW0 + Y_AXIS) / 2, "label-caps", tracking=1.6,
                anchor="middle", rotate=-90))

# ------------------------------------------------------------------ the month axis
ticks, labels = [], []
m = dt.date(start.year, start.month, 1)
while m <= taken:
    x = xd(m)
    big = m.month == 1 or m == start
    ticks.append(f"M{fmt(x)} {Y_AXIS}v{9 if big else 5}")
    lab = MONTHS[m.month - 1].upper()
    labels.append(c.t(lab, x + 4, Y_AXIS + 20, "label", fill=th.ink2 if big else th.muted))
    if big:
        labels.append(c.t(str(m.year), x + 4, Y_AXIS + 40, "label", fill=th.ink2))
    m = dt.date(m.year + (m.month == 12), m.month % 12 + 1, 1)
body.append(f'<path d="M{X0} {Y_AXIS}H{X1}{"".join(ticks)}" fill="none" {S("HAIR", th.ink, 0.8, caps="butt")}/>')
body.extend(labels)

# ------------------------------------------------------------------ key and imprint
ky = H - 60
body.append(f'<g fill="{th.ink}" fill-opacity=".48">'
            f'<circle cx="68" cy="{ky-5}" r="{fmt(radius(1))}"/><circle cx="92" cy="{ky-5}" r="{fmt(radius(10))}"/>'
            f'<circle cx="126" cy="{ky-5}" r="{fmt(radius(100))}"/></g>')
body.append(c.t("1 · 10 · 100 commits in a day", 152, ky, "label", fill=th.ink2))
body.append(c.t(f"GITHUB.COM/BENJAMINSRUSSELL · SURVEYED {long_date(taken).upper()}", 60, H - 36,
                "label-caps", tracking=1.6, fill=th.ink2))

c.write("concepts/lines.svg", W, H, "".join(body), "".join(defs),
        title=f"Survey lines: Ben Russell's {st['repo_count']} repositories, one dot per commit-day, Sep 2025 to {long_date(taken)}.")
