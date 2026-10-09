"""vessel.py — concept still 1, "The vessel, in section" (round 4, D9; crit-creative §2).

An engineering drawing of rustmapper the way a shipyard draws a hull: an inboard profile, bow right,
with the machine's parts in their compartments, a midship section beside it, and a title block. A label
with a commit sha is a claim stats.json can source (claims.workers, claims.shards; claims.scrape_interval
belongs to Scrapy and is printed in Scrapy's line of the register, not on the hull). Every other label is a
structural part the README's rustmapper bullets name; nothing is drawn that the README does not say is
built. The figures: the three claims, the edition (version, date, wheel) and rustmapper's commit count
as the drawing's revision, all from assets/stats.json; the thesis from chart.toml.

    python3 scripts/concepts/vessel.py           → concepts/vessel.svg
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _concept import Concept, S, op, Jitter, hatch, fmt, long_date, thousands  # noqa: E402

W, H = 1280, 760
c = Concept("vessel")
th = c.theme
st = c.stats
jit = Jitter(c.cfg["chart"]["seed"], "concept/vessel")
thesis = c.cfg["copy"]["thesis"]

rm = c.repo("Rust-sitemap")
ed = st["edition"]
workers, shards, scrape = c.claim("workers"), c.claim("shards"), c.claim("scrape_interval")
lo, hi = workers["value"].split("–")
sources = st["sources"]


def src_file(claim: dict, base: bool = False) -> str:
    """'Rust-sitemap:src/lib.rs (num_cpus::get())' → 'src/lib.rs' (base: 'lib.rs')."""
    f = claim["source"].split(":", 1)[1].split(" ")[0]
    return os.path.basename(f) if base else f


body: list[str] = []
defs: list[str] = []

# ------------------------------------------------------------------ geometry (sheet space)
DECK, WL, KEEL, BL = 272, 398, 480, 506
X_TR, X_BOW = 230, 976                    # transom, stem head
BULK = (348, 586, 720, 878)               # bulkheads
MAST_X = 786
X_SEC = 1132                              # midship section centre


def dot(x, y, r=2.2):
    return f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}" fill="{th.ink}"/>'


def leader(px, py, lx, ly, lines, anchor="start", sha=None, also=None):
    """A label of one or two lines at (lx, ly) with a HAIR leader to a dot at the part (px, py); `also`
    is a second part (x, y) the same label names. The leader meets the label at its top when the part is
    above it and at its foot when below, so it never crosses the text. `sha` (figure · source · sha) is
    set in caps texture, muted, on its own line under the label."""
    n = len(lines) + (1 if sha else 0)
    foot = ly + 21 * (n - 1) + 4
    sx = lx - 8 if anchor == "start" else lx + 8
    out = []
    for qx, qy in [(px, py)] + ([also] if also else []):
        ay = ly - 5 if qy < ly else foot
        out.append(dot(qx, qy))
        out.append(f'<path d="M{fmt(qx)} {fmt(qy)}L{fmt(sx)} {fmt(ay)}" fill="none" {S("HAIR", th.ink, 0.8, caps="butt")}/>')
    y = ly
    for i, s in enumerate(lines):
        role = "label-caps" if i == 0 else "label"
        kw = {"tracking": 1.6} if role == "label-caps" else {}
        out.append(c.t(s, lx, y, role, anchor=anchor, fill=th.ink if i == 0 else th.ink2, **kw))
        y += 21
    if sha:
        out.append(c.t(sha, lx, y, "texture", anchor=anchor, fill=th.muted, tracking=0.6))
    return "".join(out)


# ------------------------------------------------------------------ sea and datum lines
body.append(f'<path d="M110 {WL}H1010" fill="none" {S("HAIR", th.ink2, 0.7, caps="butt")}/>')
body.append(f'<path d="M110 {BL}H1010" fill="none" {S("HAIR", th.ink2, 0.5, "PECK", caps="butt")}/>')
body.append(c.t("WL", 104, WL + 6, "texture", anchor="end", fill=th.ink2))
body.append(c.t("BL", 104, BL + 6, "texture", anchor="end", fill=th.ink2))
stations = []
for k in range(11):
    x = X_TR + (X_BOW - 30 - X_TR) * k / 10
    stations.append(f"M{fmt(x)} {BL - 4}v8")
    body.append(c.t(str(k), x, BL + 20, "texture", anchor="middle", fill=th.ink2))
body.append(f'<path d="{"".join(stations)}" fill="none" {S("HAIR", th.ink, 0.8, caps="butt")}/>')

# ------------------------------------------------------------------ the hull, inboard profile
hull = (f"M{X_TR} {DECK}Q600 {DECK + 28} {X_BOW} {DECK - 4}"                      # sheer
        f"Q{X_BOW - 10} 330 {X_BOW - 24} 372Q{X_BOW - 44} 440 {X_BOW - 84} {KEEL - 2}"  # stem, forefoot
        f"L{X_TR + 22} {KEEL - 6}Z")                                                 # keel, raked transom
body.append(f'<path d="{hull}" fill="{th.paper}" {S("LINE", th.ink, 1.0)}/>')
body.append(f'<path d="M{X_TR + 4} {DECK + 7}Q600 {DECK + 35} {X_BOW - 10} {DECK + 3}" fill="none" {S("PEN", th.ink, 0.8)}/>')
body.append(f'<path d="M{X_TR + 22} {KEEL - 13}L{X_BOW - 88} {KEEL - 10}" fill="none" {S("PEN", th.ink, 0.6)}/>')
body.append(f'<path d="{"".join(f"M{x} {DECK + 26}V{KEEL - 13}" for x in BULK)}" fill="none" {S("PEN", th.ink, 0.9)}/>')
body.append(f'<path d="M{X_TR + 10} {WL}H{X_BOW - 32}" fill="none" {S("PEN", th.ink, 0.9, caps="butt")}/>')

# ------------------------------------------------------------------ parts
# seeds: three pipes through the transom, lettered A B C
pipes = []
for i, src in enumerate(sources):
    y = 334 + i * 26
    pipes.append(f"M156 {y}H{BULK[0] - 20}")
    body.append(f'<circle cx="{X_TR - 22}" cy="{y}" r="5.5" fill="{th.paper}" {S("PEN", th.ink)}/>')
    body.append(c.t(src["letter"], X_TR - 22, y + 4, "texture", anchor="middle"))
    body.append(c.t(src["name"].title().replace("Ct Logs", "CT logs"), 148, y + 5, "label", anchor="end", fill=th.ink2))
body.append(f'<path d="{"".join(pipes)}" fill="none" {S("PEN", th.ink, 0.9, caps="butt")}/>')
body.append(c.t("SEEDS", 148, 312, "label-caps", tracking=1.6, anchor="end"))

# frontier: shard bins in the hold, the last one pecked (shards = num_cpus: the count is the host's)
bx0, bw, bg = BULK[0] + 18, 26, 8
bins_d, pecked_d = [], []
nb = 6
for k in range(nb):
    x = bx0 + k * (bw + bg)
    d = f"M{x} 318H{x + bw}V{WL - 8}H{x}Z"
    (pecked_d if k == nb - 1 else bins_d).append(d)
    if k < nb - 1:
        g = jit.sub(f"bin{k}")
        marks = "".join(f"M{fmt(x + 4 + g.uniform(0, bw - 8))} {fmt(326 + g.uniform(0, WL - 40))}h3" for _ in range(5 + k % 3))
        body.append(f'<path d="{marks}" fill="none" {S("PEN", th.ink2, 0.7, caps="butt")}/>')
body.append(f'<path d="{"".join(bins_d)}" fill="none" {S("PEN", th.ink, 0.9)}/>')
body.append(f'<path d="{"".join(pecked_d)}" fill="none" {S("PEN", th.ink, 0.7, "PECK")}/>')
# section mark at frame 3, for the drawing at right
sx = X_TR + (X_BOW - 30 - X_TR) * 3 / 10
body.append(f'<path d="M{fmt(sx)} {DECK - 30}V{DECK - 14}M{fmt(sx)} {KEEL + 2}V{KEEL + 18}" fill="none" {S("PEN", th.ink, 0.9, caps="butt")}/>')
body.append(f'<path d="M{fmt(sx)} {DECK - 22}l9 -5v10zM{fmt(sx)} {KEEL + 10}l9 -5v10z" fill="{th.ink}"/>')

# governor: a gauge, needle between the two permit figures, a pecked sense line down to redb
GX, GY, GR = 652, 380, 42
body.append(f'<path d="M{fmt(GX - GR)} {GY}A{GR} {GR} 0 0 1 {fmt(GX + GR)} {GY}" fill="none" {S("PEN", th.ink, 0.9)}/>')
tk = "".join(f"M{fmt(GX + GR*math.cos(math.radians(a)))} {fmt(GY - GR*math.sin(math.radians(a)))}"
             f"l{fmt(-6*math.cos(math.radians(a)))} {fmt(6*math.sin(math.radians(a)))}" for a in (0, 45, 90, 135, 180))
body.append(f'<path d="{tk}" fill="none" {S("HAIR", th.ink, 0.9, caps="butt")}/>')
body.append(f'<path d="M{GX} {GY}L{fmt(GX + (GR-10)*math.cos(math.radians(118)))} {fmt(GY - (GR-10)*math.sin(math.radians(118)))}" '
            f'fill="none" {S("PEN", th.accent, 1.0)}/>')
body.append(f'<circle cx="{GX}" cy="{GY}" r="3" fill="{th.ink}"/>')
body.append(c.t(lo, GX - GR - 2, GY + 18, "texture", anchor="middle"))
body.append(c.t(thousands(int(hi)), GX + GR + 2, GY + 18, "texture", anchor="middle"))
body.append(c.t("permits", GX, GY + 36, "texture-italic", anchor="middle", fill=th.ink2))
body.append(f'<path d="M{GX} {GY + 24}V{KEEL - 16}H{BULK[2] + 40}" fill="none" {S("HAIR", th.ink2, 0.8, "PECK", caps="butt")}/>')

# the worker pool: ranks of permits between governor and the bow bulkhead; the upper rank pecked (it grows)
pool_d, pool_p = [], []
for r in range(3):
    for k in range(6):
        x = BULK[2] + 16 + k * 22
        y = WL - 18 - r * 20
        (pool_p if r == 2 else pool_d).append(f"M{x} {y}h14v12h-14z")
body.append(f'<path d="{"".join(pool_d)}" fill="none" {S("PEN", th.ink, 0.9)}/>')
body.append(f'<path d="{"".join(pool_p)}" fill="none" {S("PEN", th.ink, 0.7, "PECK")}/>')

# the write-ahead log along the keel, CRC32-framed: a long tank with its frames
WX0, WX1, WY0, WY1 = 370, 702, WL + 18, KEEL - 22
body.append(f'<rect x="{WX0}" y="{WY0}" width="{WX1 - WX0}" height="{WY1 - WY0}" rx="8" fill="{th.shallow_a}" {S("PEN", th.ink, 0.9)}/>')
body.append(f'<path d="{"".join(f"M{x} {WY0}V{WY1}" for x in range(WX0 + 24, WX1 - 8, 24))}" fill="none" {S("HAIR", th.ink, 0.7, caps="butt")}/>')
# frontier → WAL (every event goes down first), WAL → redb, redb → up and out at the bow
fx = bx0 + 3 * (bw + bg) - bg / 2
body.append(f'<path d="M{fmt(fx)} {WL - 6}V{WY0 - 2}" fill="none" {S("PEN", th.ink, 0.9, caps="butt")}/>')
body.append(f'<path d="M{fmt(fx - 4)} {WY0 - 9}l4 7l4 -7z" fill="{th.ink}"/>')
RX0, RX1 = 752, 860
body.append(f'<rect x="{RX0}" y="{WL + 14}" width="{RX1 - RX0}" height="{KEEL - 18 - WL - 14}" rx="4" fill="{th.shallow_b}" {S("PEN", th.ink, 0.9)}/>')
body.append(f'<path d="{"".join(f"M{RX0 + 10} {WL + 30 + 12*k}H{RX1 - 10}" for k in range(3))}" fill="none" {S("HAIR", th.ink, 0.7, caps="butt")}/>')
body.append(f'<path d="M{WX1} {fmt((WY0+WY1)/2)}H{RX0 - 2}" fill="none" {S("PEN", th.ink, 0.9, caps="butt")}/>')
body.append(f'<path d="M{RX0 - 9} {fmt((WY0+WY1)/2 - 4)}l7 4l-7 4z" fill="{th.ink}"/>')
# the riser: redb → up to the deck → forward along it → out over the bow as sitemap.xml
OUT_Y = DECK - 12
body.append(f'<path d="M{RX1} {WL + 36}H{BULK[3] + 30}V{OUT_Y}H{X_BOW + 30}" fill="none" {S("PEN", th.ink, 0.9, caps="butt")}/>')
body.append(f'<path d="M{X_BOW + 28} {OUT_Y - 5}l10 5l-10 5z" fill="{th.ink}"/>')
body.append(c.t("sitemap.xml", X_BOW + 42, OUT_Y + 5, "machine"))

# mast, lookout, pennant with the edition
body.append(f'<path d="M{MAST_X} {DECK + 12}V104" fill="none" {S("LINE", th.ink, 1.0, caps="butt")}/>')
body.append(f'<rect x="{MAST_X - 16}" y="156" width="32" height="10" fill="{th.paper}" {S("PEN", th.ink, 0.9)}/>')
body.append(f'<path d="M{MAST_X} 104l66 9l-66 9z" fill="{th.accent}"/>')
body.append(c.t(ed["version"], MAST_X + 7, 117, "texture", fill=th.paper))

# ------------------------------------------------------------------ labels (leaders only where the README or a sha sources them)
body.append(leader(bx0 + 2.5 * (bw + bg) - bg / 2, 318, 250, 146,
                   ["Frontier", "rendezvous-hashed by registrable domain · one shard per core"],
                   sha=f"shards = {shards['value']} · {src_file(shards)} · {shards['sha'][:8]}"))
body.append(leader(GX - 22, GY - 34, 452, 214,
                   ["Governor and worker pool", "reads redb commit latency, sizes the pool"],
                   sha=f"{workers['value']} {workers['unit']} · {src_file(workers, base=True)} · {workers['sha'][:8]}",
                   also=(BULK[2] + 16 + 2 * 22 + 7, WL - 18 - 40)))
body.append(leader(MAST_X + 66, 113, 866, 110, ["PyPI", f"rustmapper {ed['version']} · {long_date(ed['date'])} · maturin wheel"],
                   sha=ed["wheels"][0].replace("-", " · ") if ed.get("wheels") else None))
body.append(leader(MAST_X + 16, 161, 866, 186, ["Lookout", "robots.txt read first, its crawl-delay honoured"]))
body.append(leader(WX0 + 150, WY1, 300, 566, ["Write-ahead log", "every frontier event, CRC32-framed, rkyv, before it reaches redb"]))
body.append(leader(RX0 + 54, KEEL - 18, 830, 598, ["redb", "the store; a killed crawl resumes at the last record"]))

# ------------------------------------------------------------------ midship section, looking forward, at frame 3
CX, hw = X_SEC, 92
sec = (f"M{CX - hw} {DECK}V{DECK + 70}Q{CX - hw + 6} {KEEL - 34} {CX} {KEEL - 6}"
       f"Q{CX + hw - 6} {KEEL - 34} {CX + hw} {DECK + 70}V{DECK}Z")
body.append(f'<path d="{sec}" fill="{th.paper}" {S("LINE", th.ink, 1.0)}/>')
body.append(f'<path d="M{CX - hw + 4} {DECK + 7}H{CX + hw - 4}" fill="none" {S("PEN", th.ink, 0.8)}/>')
body.append(f'<path d="M{CX - hw - 18} {WL}H{CX + hw + 18}" fill="none" {S("PEN", th.ink, 0.9, caps="butt")}/>')
body.append(f'<path d="M{CX} {DECK - 4}V{KEEL + 8}" fill="none" {S("HAIR", th.ink, 0.6, "LIMIT", caps="butt")}/>')
cells, cells_p = [], []
ncell, cw, cg = 6, 23, 5
cx0 = CX - (ncell * cw + (ncell - 1) * cg) / 2
for k in range(ncell):
    x = cx0 + k * (cw + cg)
    (cells_p if k in (0, ncell - 1) else cells).append(f"M{fmt(x)} 318H{fmt(x + cw)}V{WL - 8}H{fmt(x)}Z")
body.append(f'<path d="{"".join(cells)}" fill="none" {S("PEN", th.ink, 0.9)}/>')
body.append(f'<path d="{"".join(cells_p)}" fill="none" {S("PEN", th.ink, 0.7, "PECK")}/>')
body.append(f'<circle cx="{CX}" cy="{fmt((WY0 + WY1) / 2 + 2)}" r="{fmt((WY1 - WY0) / 2)}" fill="{th.shallow_a}" {S("PEN", th.ink, 0.9)}/>')
body.append(c.t("SECTION AT FRAME 3", CX, KEEL + 42, "label-caps", tracking=1.6, anchor="middle"))
body.append(c.t("looking forward", CX, KEEL + 63, "label", anchor="middle", fill=th.ink2))
body.append(c.t("INBOARD PROFILE", X_TR + 4, DECK - 40, "label-caps", tracking=1.6))

# ------------------------------------------------------------------ thesis above
body.append(c.t(thesis, 60, 76, "thesis", fill=th.ink2))

# ------------------------------------------------------------------ the two names, below
body.append(c.t("rustmapper", 60, 660, "title"))
body.append(c.t("a concurrent sitemap crawler in Rust,", 60, 686, "label", fill=th.ink2))
body.append(c.t("shipped to PyPI as a Python package", 60, 707, "label", fill=th.ink2))
body.append(c.t("Scrapy Harbor", 430, 660, "title"))
body.append(c.t("where a run is operated: Scrapy stages,", 430, 686, "label", fill=th.ink2))
body.append(c.t(f"Delta Lake, Prometheus scraped every {scrape['value']} {scrape['unit']}", 430, 707, "label", fill=th.ink2))
body.append(c.t(f"{src_file(scrape)} · {scrape['sha'][:8]}", 430, 726, "texture", fill=th.muted, tracking=0.6))

# ------------------------------------------------------------------ title block
TX, TY, TW, ROW = 810, 636, 410, 28
body.append(f'<rect x="{TX}" y="{TY}" width="{TW}" height="{ROW * 3}" fill="none" {S("PEN", th.ink, 0.9)}/>')
body.append(f'<path d="M{TX} {TY + ROW}H{TX + TW}M{TX} {TY + 2*ROW}H{TX + TW}M{TX + 176} {TY}V{TY + 2*ROW}" fill="none" '
            f'{S("HAIR", th.ink, 0.8, caps="butt")}/>')
body.append(c.t("Ben Russell", TX + 12, TY + 22, "place-land"))
body.append(c.t("SURVEY VESSEL · IN SECTION", TX + 188, TY + 20, "label-caps", tracking=1.6))
body.append(c.t(f"drawn {long_date(c.taken)}", TX + 12, TY + ROW + 20, "label", fill=th.ink2))
body.append(c.t(f"revision {rm['commits']} · {rm['commit_days']} commit-days", TX + 188, TY + ROW + 20, "label", fill=th.ink2))
body.append(c.t("pip install rustmapper", TX + 12, TY + 2*ROW + 20, "machine-strong"))

# ------------------------------------------------------------------ neat line
body.append(f'<path d="M18 18H{W-18}V{H-18}H18Z" fill="none" {S("LINE", th.ink, 0.9, caps="butt")}/>')
body.append(f'<path d="M24 24H{W-24}V{H-24}H24Z" fill="none" {S("HAIR", th.ink, 0.6, caps="butt")}/>')

c.write("concepts/vessel.svg", W, H, "".join(body), "".join(defs),
        title=f"rustmapper, the survey vessel, drawn in section: seeds, frontier, governor, write-ahead log, redb, sitemap out. {thesis}")
