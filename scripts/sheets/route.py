"""route.py — the hero (round 6, SPEC.md, review round 1): the way into rustmapper.

The image answers one sentence: how you start rustmapper, what it does with each page, where a stranger goes wrong
and how to get out, and where the output goes next. Vertical position is the order of a run: what you type, what
happens to each URL, how you stop it, what you get. The rows that repeat for every page are closed by one line back
up the left side: the crawl is a loop, and the one hazard sits on that loop, with its way out on the next row.
Nothing on the sheet has a size that depends on data: every shape is a fixed mark (a bar, a ring, a tick, a hatch
block, a band, a line), and every word comes from `stats.json` (routes, handoffs, edition, runcheck) or from
chart.toml [copy] / [identity].

Left column, the title block: the name and the role line, nothing else (review round 2: the project's name is the
route's header, and the counts and CI live in the text). Right, the route: the project's name and one sentence, the
start bar, the install line with the release, the image's one command, then the stops (a ring on the magenta
track), the side note (a tick, no ring: it acts on the fetches from outside), the hazard (a hatched block on the
loop's way back, on a band of the accent at 14 % over paper, so it is the row seen first) and the way out, the end
bar, the file you get and its real field names, and a thin line on to the one other project of his that reads that
file and tests the join. Everything a reader copies or looks up (the crawl command, the install time, the CI) is in
the README, once.

A route entry is drawn only when routes.<name> says its anchors hold and the run-check probes it names came out as
stated (scripts/data/route.py `resolve`); a desk file label only when that file is among the entry's anchors in the
code it describes; the install line only when the run check passed (SPEC §6); the line past the end only when the
hand-off's state is `runs`. Nothing else is drawn: no border, no axis, no motion, no legend.

Every glyph goes through typeset (ctx.k); every stroke width through chartlib.stroke.
"""
from __future__ import annotations

import datetime as dt

import chartlib as c
import edition as E
import tokens
from data import route as R

NAME = "hero"            # the file names and README markers stay hero-*.svg
KIND = "chart"
SIZES = {"desk": (1280, 620), "phone": (720, 1170)}   # nominal: the height is the last baseline + 36 (phone 30)
EDITIONS = ("day", "night", "phone-day", "phone-night")   # nothing moves: no still editions
PROJECT = "rustmapper"
HAZARD_TINT = 0.14       # the hazard band: accent at 14 % over paper (day #F0D4C7, night #312531); ink on it ~10:1
RUNCHECK_MAX_AGE = 14    # days before `taken` a passing run check still counts (SPEC §7, ROUTE-ENTRANCE)

# id -> (what a stranger learns, the visitor question, where it comes from). SPEC §2.2; T-PURPOSE holds the sheet to it.
PURPOSE: dict[str, tuple[str, str, str]] = {
    "T1": ("whose page this is", "Q1", "chart.toml [identity]"),
    "T2": ("what he builds, in the first two words", "Q1", "chart.toml [copy] role_line"),
    "R0": ("which project, and what it does, before any detail", "Q2", "stats.json routes.rustmapper.header"),
    "R1": ("where you begin", "Q4", "R1-I5 (the entrance is a fixed point)"),
    "R2": ("the line that gets it, and how old the release is: the image's one command", "Q4",
           "stats.json edition.version, edition.date; runcheck.rustmapper"),
    "R5": ("one way through, in the order of a run", "Q4", "R1-F3 (the line you follow)"),
    "R6": ("the crawl is a loop: the rows it spans repeat for every page", "Q1",
           "Rust-sitemap src/bfs_crawler.rs frontier.add_links; Mercator (SRC-173 §3)"),
    "S1": ("where URLs come from, and what the release contacts by default", "Q5", "stats.json routes.rustmapper S1"),
    "S2": ("it is polite by construction: one queue per host, paced by robots.txt", "Q1", "stats.json routes.rustmapper S2"),
    "F1": ("each page is fetched and its same-site links are queued again", "Q1", "stats.json routes.rustmapper F1"),
    "G1": ("the crawl slows when it cannot save what it found, not when the network is slow", "Q1",
           "stats.json routes.rustmapper G1"),
    "W1": ("a kill does not lose the pages: the writer saves every 50 ms, and the command that gets them back", "Q5",
           "stats.json routes.rustmapper W1 (writer_thread.rs BATCH_TIMEOUT_MS); runcheck export_after_kill"),
    "H1": ("pointed at a real site, it does not stop, and it goes wider than the start host; the band makes it the "
           "row seen first", "Q5", "stats.json routes.rustmapper H1; runcheck ends_by_itself"),
    "C1": ("how to stop it so the file is written, and what loses it", "Q5",
           "stats.json routes.rustmapper C1; runcheck crawl_ctrl_c, kill_writes_file"),
    "R12": ("where you end up", "Q4", "R2-F2 item 7 (the end of the route)"),
    "R13": ("what you get and where it is on disk, with the real field names", "Q4", "stats.json routes.rustmapper R13"),
    "R15": ("his projects are one body of work: this output feeds another, and that join is tested", "Q2",
            "stats.json handoffs[sitemap-jsonl→ideal-url-organizer]"),
}

BREAKS: list[tuple[str, str, str]] = [
    ("Caps lines in role `label`",
     "the role line is set through role `label` in capitals with explicit tracking (desk 1.6, phone 1.0); no run "
     "uses `label-caps`",
     "check_type allows one label-caps run per sheet; the role line is two caps lines"),
    ("Name at 88 on the desk",
     "the desk name is set at 88 (phone 132)",
     "the title column is 56 to 410 px, and the name at 141 would be over 500 px wide"),
    ("Order is position; the loop is a line",
     "the route runs top to bottom in the order of a run: install, start, seeds, then the rows that repeat for every "
     "page (fetch, the governor beside it, the log), closed by one line back up the left side; the hazard sits on "
     "that line and its way out on the next row",
     "a crawler is a loop: links found on a page go back on the queue (bfs_crawler.rs frontier.add_links); the "
     "release never stops by itself (run check, ends_by_itself), and a list cannot show where the repeat closes"),
    ("The governor has a tick, not a ring",
     "the governor's row is marked by a short tick off the line and set in the secondary ink",
     "it is not a step a URL passes through: it adds and removes semaphore permits from the side (governor.rs)"),
    ("Fixed marks, no sizes",
     "every bar, ring, hatch block and line has a fixed size; only the number of lines of text moves anything",
     "the owner could not tell what the old islands' sizes meant (9 Oct 2026); here nothing has a size to read"),
    ("Drawn only when checked",
     "an entry is drawn only when its anchors hold in the code at HEAD and in the released sdist; the install lines "
     "only when the run check passed; the line past the end only when the reader's fields are in the writer's struct",
     "the image claims only what the tool does (SPEC §5, §6)"),
    ("Trap text in ink, on a band",
     "the trap's words are set in ink on a band of the accent at 14 % over paper; its hatch block is in the accent",
     "accent on day paper is 4.1:1, under the 4.5:1 text needs; ink on the band is 10.3:1 by day and 8.4:1 by night, "
     "and the one catch has to be the row a stranger sees first (owner test 1)"),
    ("Phone role line at 204",
     "on the phone the role line sits at 204 (SPEC: 196) and everything under it 8 lower",
     "at 196 its text box meets the descent of the name set at 132 (the bounds check measures the font's boxes)"),
    ("Phone drops file names",
     "on the phone the stops carry their rules only",
     "720 px leaves 600 px for text at the 26 px floor"),
    ("Release label on the install line, phone too",
     "on the phone the release label is set right-aligned on the install line, as on the desk, not in the platform "
     "note",
     "the note with the release in front is 648 px at 26 px, over the 600 px measure; its third line took the phone "
     "sheet past 1200"),
    ("No motion, no still editions",
     "the four editions are day, night, phone-day and phone-night; nothing moves",
     "nothing in the subject moves on a period"),
]

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
MONTHS_MIXED = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ---------------------------------------------------------------- layout (sheet units, SPEC §2.3)
L = {
    "desk": {"title_x": 56, "title_w": 354, "name_size": 88, "name_track": -1.5, "name_y": 128, "role_y": 182,
             "role_pitch": 28, "fine_gap": 52, "fine_pitch": 28, "track_x": 456, "text_x": 484, "rule_x": 640,
             "right": 1224, "head_y": 84, "head_after_title": None, "sent_gap": 34, "line": 28, "bar_gap": 30,
             "bar_w": 24, "bar_h": 4, "r2_gap": 30, "entry_gap": 42, "pitch": 36, "end_gap": 30, "r13_gap": 30,
             "ring_r": 6, "ring_dy": 6, "hatch": (432, 450, 13, 1), "loop_out": 14, "loop_hatch": (414, 432),
             "loop_dy": 13, "loop_arrow": (8, 10), "tick": (3, 15), "after_end": 26, "tip": 8, "label_gap": 14,
             "arrow_w": 10, "rule_after_file": 20, "foot": 36},
    "phone": {"title_x": 40, "title_w": 640, "name_size": 132, "name_track": -2.0, "name_y": 140, "role_y": 204,
              "role_pitch": 34, "fine_gap": 46, "fine_pitch": 34, "track_x": 56, "text_x": 88, "rule_x": None,
              "right": 688, "head_y": None, "head_after_title": 60, "sent_gap": 40, "line": 34, "bar_gap": 28,
              "bar_w": 24, "bar_h": 4, "r2_gap": 38, "entry_gap": 46, "pitch": 43, "end_gap": 24, "r13_gap": 38,
              "ring_r": 8, "ring_dy": 9, "hatch": (26, 48, 17, 1), "loop_out": 18, "loop_hatch": (8, 30),
              "loop_dy": 15, "loop_arrow": (10, 12), "tick": (4, 20), "after_end": 24, "tip": 8, "label_gap": 14,
              "arrow_w": 12, "rule_after_file": None, "foot": 30},
}
TRACK = {"desk": 1.6, "phone": 1.0}


def _date(iso: str, caps: bool = True) -> str:
    y, m, d = str(iso)[:4], int(str(iso)[5:7]), int(str(iso)[8:10])
    return f"{d} {(MONTHS if caps else MONTHS_MIXED)[m - 1]} {y}"


def _iso(s) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(s)[:10])
    except (TypeError, ValueError):
        return None


def _repo(data: dict, name: str) -> dict:
    return next((r for r in data.get("repos") or [] if r.get("name") == name), {})


# ---------------------------------------------------------------- data -> what the sheet says

def over(paper: str, ink: str, alpha: float) -> str:
    """`ink` laid over `paper` at `alpha`, as one opaque colour (the hazard band: accent at 14 % over paper)."""
    a = [int(paper.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(ink.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02X%02X%02X" % tuple(round(x * (1 - alpha) + y * alpha) for x, y in zip(a, b))


def entrance_ok(data: dict, project: str = PROJECT) -> tuple[bool, str]:
    """(True, "") when runcheck.<project> passed for the current release within RUNCHECK_MAX_AGE days of `taken`."""
    rc = (data.get("runcheck") or {}).get(project)
    ed = data.get("edition") or {}
    if not isinstance(rc, dict):
        return False, "no run check recorded"
    if not rc.get("ok"):
        bad = next((s.get("cmd") for s in rc.get("steps") or [] if not s.get("ok") and s.get("gate", True)), "a step")
        return False, f"the run check failed at: {bad}"
    if str(rc.get("version")) != str(ed.get("version")):
        return False, f"the run check tested {rc.get('version')}, the release is {ed.get('version')}"
    taken, when = _iso(data.get("taken")), _iso(rc.get("date"))
    if not taken or not when or (taken - when).days > RUNCHECK_MAX_AGE:
        return False, f"the run check is dated {rc.get('date')}, more than {RUNCHECK_MAX_AGE} days before {data.get('taken')}"
    return True, ""


def handoff(data: dict, repo: str = "Rust-sitemap", file: str = "data/sitemap.jsonl") -> dict | None:
    """The hand-off drawn past the end: the first one from `repo` writing `file` whose state is `runs`."""
    for h in data.get("handoffs") or []:
        if h.get("from") == repo and h.get("file") == file and h.get("state") == "runs":
            return h
    return None


def plan(data: dict, cfg: dict, project: str = PROJECT) -> dict:
    """Everything the sheet will say, in order, from stats.json and chart.toml alone. Raises when the route was
    never checked (no routes.<project>): the sheet has nothing true to draw."""
    route = (data.get("routes") or {}).get(project)
    if not isinstance(route, dict) or not route.get("entries"):
        raise RuntimeError(f"hero: stats.json carries no routes.{project}; run build_stats.py (scripts/data/route.py)")
    repo_name = route.get("repo") or "Rust-sitemap"
    ed = data.get("edition") or {}
    aliases = (cfg.get("hero") or {}).get("aliases") or {}
    rc = (data.get("runcheck") or {}).get(project)
    entries = R.drawn(route, rc)
    ok, why = entrance_ok(data, project)
    R.command_name(ed.get("scripts"), project)       # raises when the release ships no command: nothing to install
    header_ok, _ = R.header_ok(route, rc)
    p = {
        "project": aliases.get(repo_name, project),
        "repo": repo_name,
        "header": route.get("header") if header_ok else None,
        "role": [s.strip() for s in str((cfg.get("copy") or {}).get("role_line") or "").split("·") if s.strip()],
        "entrance": ok, "entrance_why": why,
        "install": f"pip install {ed.get('project') or project}" if ok and ed.get("version") else None,
        "release": f"{ed['version']} · {_date(ed['date'])}" if ok and ed.get("version") and ed.get("date") else None,
        "steps": [e for e in entries if e["kind"] in ("stop", "step", "note", "trap")],
        "end": next((e for e in entries if e["kind"] == "end"), None),
        "handoff": None,
        "unverified": [e["id"] for e in R.unverified(route, rc)],
    }
    end = p["end"]
    if end:
        h = handoff(data, repo_name, end.get("file") or "")
        if h:
            p["handoff"] = h
    return p


# ---------------------------------------------------------------- the build

def build(ctx) -> str:
    c.set_night(ctx.ed.dark)                    # night is drawn at +20 % weight
    try:
        return _build(ctx)
    finally:
        c.set_night(False)


def _build(ctx) -> str:
    ed, data, cfg, k = ctx.ed, ctx.data, ctx.cfg, ctx.k
    if k is None:
        raise RuntimeError("hero needs the type engine (scripts/typeset.py)")
    theme, sc, phone = ed.theme, ed.scale, ed.phone
    w, h = SIZES[sc]
    G = L[sc]
    track = TRACK[sc]
    p = plan(data, cfg)
    groups: dict[str, list[str]] = {}
    order: list[str] = []
    marks: list[dict] = []

    def put(gid: str, svg: str) -> None:
        if gid not in groups:
            groups[gid] = []
            order.append(gid)
        groups[gid].append(svg)

    def lbl(text, x, y, gid, key, role="label", fill=None, caps=False, anchor="start", size=None, tracking=None):
        if caps:
            text, tracking = str(text).upper(), track if tracking is None else tracking
        put(gid, k.label(str(text), x, y, role, anchor=anchor, fill=fill or theme.ink, edition=ed, scale=sc,
                         tracking=tracking, size=size, truth="measured", key=key))

    def width(text, role="label", caps=False, size=None, tracking=None):
        if caps:
            return k.text_width(str(text).upper(), role, edition=ed, scale=sc, tracking=track, size=size)
        return k.text_width(str(text), role, edition=ed, scale=sc, size=size, tracking=tracking)

    day_ed = E.EDITIONS["phone-day" if phone else "day"]

    def fit(text, role="label"):
        """Width for line breaking, measured in the day cut: night's Light cuts are narrower, so a line that fits
        by day fits by night, and both editions break at the same words."""
        return k.text_width(str(text), role, edition=day_ed, scale=sc)

    def wrap(text, max_w, role="label", seps=("; ", ": ", " · ", ", ")):
        """Lines that fit `max_w`: broken at the strongest separator (a semicolon, a colon, a middle dot, a comma),
        so a name like "Common Crawl" or "Python 3.13" is not split, unless breaking at words takes fewer lines
        (a 26 px phone line holds about 48 characters, and every extra line costs the phone sheet 34 units)."""
        by_sep = _wrap_sep(text, max_w, role, seps)
        by_word = _wrap_sep(text, max_w, role, ())
        return by_word if len(by_word) < len(by_sep) else by_sep

    def _wrap_sep(text, max_w, role, seps):
        text = str(text)
        if fit(text, role) <= max_w:
            return [text]
        for i, sep in enumerate(seps):
            if sep not in text:
                continue
            parts = text.split(sep)
            keep = sep.strip() if sep.strip() != "·" else ""
            pieces = [pt + keep if j < len(parts) - 1 else pt for j, pt in enumerate(parts)]
            joiner = " " if keep else " · "
            lines: list[str] = []
            for piece in pieces:
                if lines and fit(lines[-1] + joiner + piece, role) <= max_w:
                    lines[-1] = lines[-1] + joiner + piece
                elif fit(piece, role) <= max_w:
                    lines.append(piece)
                else:
                    lines.extend(_wrap_sep(piece, max_w, role, seps[i + 1:]))
            return lines
        lines, cur = [], []
        for word in text.split():
            trial = " ".join(cur + [word])
            if cur and fit(trial, role) > max_w:
                lines.append(" ".join(cur))
                cur = [word]
            else:
                cur.append(word)
        if cur:
            lines.append(" ".join(cur))
        if len(lines) >= 2 and len(lines[-1].split()) == 1 and len(lines[-2].split()) >= 3:
            head_, moved = lines[-2].rsplit(" ", 1)     # no one-word last line: take a word down with it
            if fit(f"{moved} {lines[-1]}", role) <= max_w:
                lines[-2:] = [head_, f"{moved} {lines[-1]}"]
        return lines

    def mark(kind, gid, box):
        k.exclude(f"{kind}:{gid}", box[0], box[1], box[2] - box[0], box[3] - box[1])
        marks.append({"kind": kind, "id": gid, "box": [round(v, 1) for v in box]})

    def _hatch(gid, x0, x1, base):
        """Three 45° strokes in the accent colour, clipped to a block beside the row's first baseline."""
        _, _, up, dn = G["hatch"]
        y0, y1 = base - up, base + dn
        clip = f"hatch-{gid}"
        span = (x1 - x0) + (y1 - y0)
        strokes = [f"M{E.fmt(x0 + span * (q + 1) / 4 - (y1 - y0))} {E.fmt(y1)}L{E.fmt(x0 + span * (q + 1) / 4)} {E.fmt(y0)}"
                   for q in range(3)]
        put(gid, f'<clipPath id="{clip}"><rect x="{x0}" y="{E.fmt(y0)}" width="{x1 - x0}" height="{E.fmt(y1 - y0)}"/>'
                 f'</clipPath><path d="{"".join(strokes)}" fill="none" clip-path="url(#{clip})" '
                 f'{c.stroke("LINE", theme.accent, caps="butt")}/>')
        mark("hatch", gid, (x0, y0, x1, y1))

    def _band(row, x0):
        """The hazard's band (review round 2): accent at HAZARD_TINT over paper, from the hatch's left edge to the
        text's right limit, as tall as the row's text block (the font's ascent over the first baseline to its descent
        under the last) plus 6. It goes first in the row's group, so the track, the loop and the words sit on it. Its
        size follows the number of text lines only, like every other mark."""
        asc, desc = k.extent("label", edition=ed, scale=sc)
        y0, y1 = row["y"] - asc - 3, row["last"] + desc + 3
        groups[row["id"]].insert(0, f'<rect x="{E.fmt(x0)}" y="{E.fmt(y0)}" width="{E.fmt(RIGHT - x0)}" '
                                    f'height="{E.fmt(y1 - y0)}" fill="{over(theme.paper, theme.accent, HAZARD_TINT)}"/>')
        marks.append({"kind": "band", "id": row["id"], "box": [round(v, 1) for v in (x0, y0, RIGHT, y1)]})

    # ================================================================ the title block (T1, T2)
    tx = G["title_x"]
    nsz, ntr = G["name_size"], G["name_track"]
    ben = k.text("Ben", tx, G["name_y"], "display", size=nsz, tracking=ntr, edition=ed, scale=sc, truth="measured",
                 key="identity:name")
    wb = k.text_width("Ben ", "display", size=nsz, tracking=ntr, edition=ed, scale=sc)
    russ = k.text("Russell", tx + wb, G["name_y"], "display", size=nsz, tracking=ntr, edition=ed, scale=sc,
                  truth="measured", key="identity:name")
    put("T1", ben + russ)
    title_last = G["name_y"]
    for i, line in enumerate(p["role"]):
        title_last = G["role_y"] + G["role_pitch"] * i
        lbl(line, tx, title_last, "T2", "copy:role_line", caps=True)

    # ================================================================ the route (R0–R15)
    X, TX, RIGHT, LH = G["track_x"], G["text_x"], G["right"], G["line"]
    y = G["head_y"] if G["head_y"] is not None else title_last + G["head_after_title"]
    lbl(p["project"], TX, y, "R0", "routes:project", role="project")
    y += G["sent_gap"]
    last = y - G["sent_gap"]
    if p["header"]:
        for i, line in enumerate(wrap(p["header"], RIGHT - TX)):
            lbl(line, TX, y + LH * i, "R0", "routes:header")
            last = y + LH * i
    bar_top = last + G["bar_gap"]
    bw, bh = G["bar_w"], G["bar_h"]
    put("R1", f'<rect x="{E.fmt(X - bw / 2)}" y="{E.fmt(bar_top)}" width="{bw}" height="{bh}" fill="{theme.flare}"/>')
    mark("bar", "R1", (X - bw / 2, bar_top, X + bw / 2, bar_top + bh))
    y = bar_top + G["r2_gap"]
    last = bar_top
    if p["install"]:
        lbl(p["install"], TX, y, "R2", "edition:project", role="machine")
        if p["release"]:
            lbl(p["release"], RIGHT, y, "R2", "edition:version", fill=theme.muted, caps=True, anchor="end")
        last = y
    y = last + G["entry_gap"]
    track_top = bar_top + bh
    step_report = []
    rows: list[dict] = []
    loop_rows: list[dict] = []
    for e in p["steps"]:
        gid = e["id"]
        kind = e["kind"]
        r = G["ring_r"]
        cy = y - G["ring_dy"]
        if kind in ("stop", "step"):
            put(gid, f'<circle cx="{E.fmt(X)}" cy="{E.fmt(cy)}" r="{r}" fill="{theme.paper}" {c.stroke("PEN", theme.ink)}/>')
            mark("ring", gid, (X - r - 1, cy - r - 1, X + r + 1, cy + r + 1))
        elif kind == "note":   # a short tick off the line: it acts on the run from the side
            t0, t1 = G["tick"]
            put(gid, f'<path d="M{E.fmt(X + t0)} {E.fmt(cy)}H{E.fmt(X + t1)}" fill="none" '
                     f'{c.stroke("LINE", theme.ink2, caps="butt")}/>')
            mark("tick", gid, (X + t0, cy - 1.5, X + t1, cy + 1.5))
        ink = theme.ink2 if kind == "note" else theme.ink
        if kind in ("stop", "note") and not phone and G["rule_x"]:
            if e.get("file"):
                lbl(e["file"], TX, y, gid, f"routes:{gid}", role="machine", fill=theme.ink2)
            rx = max(G["rule_x"], TX + (width(e["file"], "machine") + 20 if e.get("file") else 0))
            lines = wrap(e["text"], RIGHT - rx)
            for i, line in enumerate(lines):
                lbl(line, rx, y + LH * i, gid, f"routes:{gid}", fill=ink)
        else:
            lines = wrap(e["text"], RIGHT - TX)
            for i, line in enumerate(lines):
                lbl(line, TX, y + LH * i, gid, f"routes:{gid}", fill=ink)
        row = {"id": gid, "kind": kind, "y": y, "cy": cy, "last": y + LH * (len(lines) - 1), "loop": e.get("loop")}
        rows.append(row)
        if e.get("loop"):
            loop_rows.append(row)
        step_report.append({"id": gid, "kind": kind, "y": round(y, 1), "lines": len(lines), "loop": bool(e.get("loop"))})
        last = row["last"]
        y = last + G["pitch"]
    # ---- the loop: one line back up the left side, from under the last repeating row to the first one's ring
    if loop_rows and loop_rows[0]["kind"] in ("stop", "step"):
        gx = X - G["loop_out"]
        y_top = loop_rows[0]["cy"]
        y_bot = loop_rows[-1]["last"] + G["loop_dy"]
        r = G["ring_r"]
        aw, al = G["loop_arrow"]
        ya = (y_top + y_bot) / 2 - al / 2          # the arrowhead, pointing up, halfway along the way back
        loop_svg = (f'<path d="M{E.fmt(X)} {E.fmt(y_bot)}H{E.fmt(gx)}V{E.fmt(y_top)}H{E.fmt(X - r - 1)}" fill="none" '
                    f'{c.stroke("LINE", theme.flare, caps="butt")}/>'
                    f'<path d="M{E.fmt(gx - aw / 2)} {E.fmt(ya + al)}H{E.fmt(gx + aw / 2)}L{E.fmt(gx)} {E.fmt(ya)}Z" '
                    f'fill="{theme.flare}"/>')
        put("R6", loop_svg)
        mark("line", "R6", (gx - aw / 2, y_top - 1.5, X, y_bot + 1.5))
        # the hazard on the loop: its hatch block sits beside the way back, on its own row
        for row in loop_rows:
            if row["kind"] == "trap":
                hx0, hx1 = G["loop_hatch"]
                _band(row, hx0)
                _hatch(row["id"], hx0, hx1, row["y"])
    for row in step_report:     # a trap off the loop keeps its block left of the track
        if row["kind"] == "trap" and not row["loop"]:
            x0, x1, _, _ = G["hatch"]
            _band(next(r for r in rows if r["id"] == row["id"]), x0)
            _hatch(row["id"], x0, x1, row["y"])
    end_top = last + G["end_gap"]
    put("R5", f'<path d="M{E.fmt(X)} {E.fmt(track_top)}V{E.fmt(end_top)}" fill="none" '
              f'{c.stroke("BRUSH", theme.flare, caps="butt")}/>')
    mark("track", "R5", (X - 2, track_top, X + 2, end_top))
    put("R12", f'<rect x="{E.fmt(X - bw / 2)}" y="{E.fmt(end_top)}" width="{bw}" height="{bh}" fill="{theme.flare}"/>')
    mark("bar", "R12", (X - bw / 2, end_top, X + bw / 2, end_top + bh))
    y = end_top + G["r13_gap"]
    last = end_top
    end = p["end"]
    if end:
        if phone:
            lbl(end["file"], TX, y, "R13", "routes:R13", role="machine")
            for i, line in enumerate(wrap(end["text"], RIGHT - TX)):
                y += LH
                lbl(line, TX, y, "R13", "routes:R13")
        else:
            lbl(end["file"], TX, y, "R13", "routes:R13", role="machine")
            rx = TX + width(end["file"], "machine") + G["rule_after_file"]
            lbl(end["text"], rx, y, "R13", "routes:R13")
        last = y
        y += LH
    ho = p["handoff"]
    if ho:
        line_end = last + G["after_end"]
        tip = line_end + G["tip"]
        aw = G["arrow_w"]
        put("R15", f'<path d="M{E.fmt(X)} {E.fmt(end_top + bh)}V{E.fmt(line_end)}" fill="none" '
                   f'{c.stroke("LINE", theme.flare, caps="butt")}/>'
                   f'<path d="M{E.fmt(X - aw / 2)} {E.fmt(line_end)}H{E.fmt(X + aw / 2)}L{E.fmt(X)} {E.fmt(tip)}Z" '
                   f'fill="{theme.flare}"/>')
        mark("line", "R15", (X - aw / 2, end_top + bh, X + aw / 2, tip))
        ly = tip + (6 if not phone else G["label_gap"])
        to = ho.get("to") or ""
        if phone:
            lbl(f"read by {to}, with a test", TX, ly, "R15", "handoffs:" + ho["id"], fill=theme.ink2)
        else:
            x = TX
            first = f"read by {to}: "
            lbl(first, x, ly, "R15", "handoffs:" + ho["id"], fill=theme.ink2)
            x += width(first)
            lbl(ho.get("reader") or "", x, ly, "R15", "handoffs:" + ho["id"], role="machine", fill=theme.ink2)
            x += width(ho.get("reader") or "", "machine")
            lbl(", with a test", x, ly, "R15", "handoffs:" + ho["id"], fill=theme.ink2)
        last = ly

    # ================================================================ assemble: one <g id> per element
    h = int(E.I(last + G["foot"]))          # the sheet ends a fixed distance under its last line (SPEC §2.3)
    ctx.extra["height"] = h
    body = "".join(f'<g id="{gid}">{"".join(groups[gid])}</g>' for gid in order)
    rep = ctx.extra
    rep["route"] = {"drawn": order, "unverified": p["unverified"], "entrance": p["entrance"],
                    "entrance_why": p["entrance_why"], "steps": step_report, "marks": marks,
                    "last_baseline": round(last, 1), "height": h, "track": [round(track_top, 1), round(end_top, 1)]}
    return E.svg(ed, w, h, body, k.glyph_defs(), sheet=NAME)


# ---------------------------------------------------------------- alt text

def alt(data, cfg) -> str:
    """Two sentences, ≤ 25 words, from the checked route: what it shows, where it ends, how many traps."""
    try:
        p = plan(data, cfg)
    except Exception:
        return "How to start Ben Russell's crawler rustmapper, what it does with each page, and how to stop it."
    end = (p["end"] or {}).get("file")
    first = f"How to start Ben Russell's crawler {p['project']}, what it does with each page, and how to stop it."
    if not end:
        return first
    loops = any(e.get("loop") for e in p["steps"])
    stop = next((e for e in p["steps"] if e["id"] == "C1"), None)
    if stop and loops:
        return f"{first} It loops until one Ctrl-C writes {end}."
    return f"{first} It ends at {end}."


# ---------------------------------------------------------------- build-report hook

def _report_hook(ctx, svg_text: str, entry: dict) -> None:
    if getattr(ctx, "sheet", None) != NAME or "route" not in ctx.extra:
        return
    entry["route"] = ctx.extra["route"]
    entry["purpose"] = {gid: list(PURPOSE[gid]) for gid in ctx.extra["route"]["drawn"] if gid in PURPOSE}
    entry["area_law"] = "none: no shape has a data-driven size"


def _register_hook() -> None:
    import sys
    for modname in ("build_assets", "__main__"):
        m = sys.modules.get(modname)
        hooks = getattr(m, "report_hooks", None)
        if isinstance(hooks, list) and _report_hook not in hooks:
            hooks.append(_report_hook)


_register_hook()
