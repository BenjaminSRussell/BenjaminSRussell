"""route.py — the hero (round 6, SPEC.md): the way into rustmapper.

The image answers one sentence: how you start rustmapper, what happens to a URL inside it in order, where a stranger
goes wrong, and where the output goes next. Vertical position is the order a URL goes through the tool. Nothing on
the sheet has a size that depends on data: every shape is a fixed mark (a bar, a ring, a hatch block, a line), and
every word comes from `stats.json` (routes, handoffs, edition, repos[].ci, repos[].head, runcheck, repo_count, taken)
or from chart.toml [copy] / [identity].

Left column, the title block: the name, the role line, then what was selected and how fresh it is (one of N public
repositories, the code's sha and date, the project's CI on main, the date the build read it all). Right, the route:
the project's name and one sentence, the start bar, the install line and the command the wheel actually installs,
the platform note, then the stops (a ring on the magenta track, the file name, what happens there) and the traps
(a hatched block on the left of the track) in order, the end bar, the file you get and its real field names, the
second output, and a thin line on to the one other project of his that reads that file and tests the join.

A route entry is drawn only when routes.<name> says it holds at HEAD and in the release (scripts/data/route.py);
the install lines only when the run check passed (SPEC §6); the line past the end only when the hand-off's state
is `runs`. Nothing else is drawn: no border, no axis, no tint, no motion, no legend.

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
RUNCHECK_MAX_AGE = 14    # days before `taken` a passing run check still counts (SPEC §7, ROUTE-ENTRANCE)

# id -> (what a stranger learns, the visitor question, where it comes from). SPEC §2.2; T-PURPOSE holds the sheet to it.
PURPOSE: dict[str, tuple[str, str, str]] = {
    "T1": ("whose page this is", "Q1", "chart.toml [identity]"),
    "T2": ("what he builds, in the first two words", "Q1", "chart.toml [copy] role_line"),
    "T3": ("this is one chosen project of several, listed below the image", "Q2", "stats.json repo_count"),
    "T4": ("which version of the code the drawing was checked against, and how recent it is", "Q3",
           "stats.json repos[Rust-sitemap].head"),
    "T5": ("the project's own tests pass on main, and when that was measured", "Q3", "stats.json repos[Rust-sitemap].ci"),
    "T6": ("when the build read all of this, so a stale pass cannot look current", "Q3", "stats.json taken"),
    "R0": ("which project, and what it does, before any detail", "Q2", "stats.json routes.rustmapper.header"),
    "R1": ("where you begin", "Q4", "R1-I5 (the entrance is a fixed point)"),
    "R2": ("the line that gets it, and that the release is older than the code drawn below", "Q4",
           "stats.json edition.version, edition.date; runcheck.rustmapper"),
    "R3": ("the command that actually runs after pip", "Q4", "stats.json edition.scripts; runcheck.rustmapper"),
    "R4": ("whether pip will just work on their machine", "Q5", "stats.json edition.wheels"),
    "R5": ("there is one way through, read top to bottom", "Q4", "R1-F3 (the line you follow)"),
    "S1": ("where URLs come from, and that he doesn't rely on links alone", "Q1", "stats.json routes.rustmapper S1"),
    "S2": ("it is polite by construction: one queue per host, paced by robots.txt", "Q1", "stats.json routes.rustmapper S2"),
    "H1": ("pointed at a big site, it crawls every subdomain to the bottom", "Q5", "stats.json routes.rustmapper H1"),
    "S3": ("the crawl slows when it cannot save what it found, not when the network is slow", "Q1",
           "stats.json routes.rustmapper S3"),
    "S4": ("a crash doesn't lose the crawl, and there is a resume command", "Q1", "stats.json routes.rustmapper S4"),
    "H2": ("the output file exists only once the crawl stops; a second Ctrl-C exits without it", "Q5",
           "stats.json routes.rustmapper H2"),
    "R12": ("where you end up", "Q4", "R2-F2 item 7 (the end of the route)"),
    "R13": ("what you get and where it is on disk, with the real field names", "Q4", "stats.json routes.rustmapper R13"),
    "R14": ("the second output, and the command for it", "Q4", "stats.json routes.rustmapper R14; edition.scripts"),
    "R15": ("his projects are one body of work: this output feeds another, and that join is tested", "Q2",
            "stats.json handoffs[sitemap-jsonl→ideal-url-organizer]"),
}

BREAKS: list[tuple[str, str, str]] = [
    ("Caps lines in role `label`",
     "the role line and the title block are set through role `label` in capitals with explicit tracking "
     "(desk 1.6, phone 1.0); no run uses `label-caps`",
     "check_type allows one label-caps run per sheet; the title block has six caps lines"),
    ("Name at 88 on the desk",
     "the desk name is set at 88 (phone 132)",
     "the title column is 56 to 410 px, and the name at 141 would be over 500 px wide"),
    ("Order is position",
     "the route runs top to bottom in the order a URL goes through rustmapper: seeds, frontier, governor, write-ahead "
     "log, output; each trap sits at the stop where it bites",
     "the order of the tool's own pipeline (SPEC §2.2) is the one thing a list cannot show next to the traps"),
    ("Fixed marks, no sizes",
     "every bar, ring, hatch block and line has a fixed size; only the number of lines of text moves anything",
     "the owner could not tell what the old islands' sizes meant (9 Oct 2026); here nothing has a size to read"),
    ("Drawn only when checked",
     "an entry is drawn only when its anchors hold in the code at HEAD and in the released sdist; the install lines "
     "only when the run check passed; the line past the end only when the reader's fields are in the writer's struct",
     "the image claims only what the tool does (SPEC §5, §6)"),
    ("Trap text in ink",
     "the trap's words are set in ink; only its hatch block is in the accent colour",
     "accent on day paper is 4.1:1, under the 4.5:1 text needs; a graphic needs 3:1"),
    ("Phone role line at 204",
     "on the phone the role line sits at 204 (SPEC: 196) and everything under it 8 lower",
     "at 196 its text box meets the descent of the name set at 132 (the bounds check measures the font's boxes)"),
    ("Phone drops file names and the export line",
     "on the phone the stops carry their rules only and the export command is left to the code block under the image",
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
             "role_pitch": 28, "fine_y": 262, "fine_pitch": 28, "track_x": 456, "text_x": 484, "rule_x": 640,
             "right": 1224, "head_y": 84, "sent_gap": 34, "line": 28, "bar_gap": 30, "bar_w": 24, "bar_h": 4,
             "r2_gap": 30, "entry_gap": 42, "pitch": 36, "end_gap": 30, "r13_gap": 30, "ring_r": 6, "ring_dy": 6,
             "hatch": (432, 450, 13, 1), "after_end": 26, "tip": 8, "label_gap": 14, "arrow_w": 10, "lang_gap": 16,
             "rule_after_file": 20, "foot": 36},
    "phone": {"title_x": 40, "title_w": 640, "name_size": 132, "name_track": -2.0, "name_y": 140, "role_y": 204,
              "role_pitch": 34, "fine_y": 284, "fine_pitch": 34, "track_x": 56, "text_x": 88, "rule_x": None,
              "right": 688, "head_y": 420, "sent_gap": 40, "line": 34, "bar_gap": 28, "bar_w": 24, "bar_h": 4,
              "r2_gap": 38, "entry_gap": 46, "pitch": 46, "end_gap": 24, "r13_gap": 38, "ring_r": 8, "ring_dy": 9,
              "hatch": (26, 48, 17, 1), "after_end": 24, "tip": 8, "label_gap": 14, "arrow_w": 12, "lang_gap": 16,
              "rule_after_file": None, "foot": 30},
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

def ci_words(ci: dict | None) -> str | None:
    """success -> PASSED, failure -> FAILED, any other value -> LAST RUN <VALUE>; None when there is no record."""
    if not isinstance(ci, dict) or not ci.get("conclusion") or not ci.get("date"):
        return None
    v = str(ci["conclusion"]).lower()
    word = {"success": "PASSED", "failure": "FAILED"}.get(v, f"LAST RUN {v.replace('_', ' ').upper()}")
    return f"CI ON MAIN {word} {_date(ci['date'])}"


def entrance_ok(data: dict, project: str = PROJECT) -> tuple[bool, str]:
    """(True, "") when runcheck.<project> passed for the current release within RUNCHECK_MAX_AGE days of `taken`."""
    rc = (data.get("runcheck") or {}).get(project)
    ed = data.get("edition") or {}
    if not isinstance(rc, dict):
        return False, "no run check recorded"
    if not rc.get("ok"):
        bad = next((s.get("cmd") for s in rc.get("steps") or [] if not s.get("ok")), "a step")
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
    repo = _repo(data, repo_name)
    ed = data.get("edition") or {}
    aliases = (cfg.get("hero") or {}).get("aliases") or {}
    entries = R.drawn(route)
    ok, why = entrance_ok(data, project)
    cmd = R.command_name(ed.get("scripts"), project) if ok else None
    head = repo.get("head") or {}
    p = {
        "project": aliases.get(repo_name, project),
        "repo": repo_name,
        "language": repo.get("main_language"),
        "header": route.get("header") if route.get("header_verified") else None,
        "role": [s.strip() for s in str((cfg.get("copy") or {}).get("role_line") or "").split("·") if s.strip()],
        "repo_count": data.get("repo_count") or len(data.get("repos") or []),
        "head": head if head.get("short") and head.get("date") else None,
        "ci": ci_words(repo.get("ci")),
        "taken": str(data.get("taken") or "")[:10],
        "entrance": ok, "entrance_why": why,
        "install": f"pip install {ed.get('project') or project}" if ok and ed.get("version") else None,
        "release": f"{ed['version']} · {_date(ed['date'])}" if ok and ed.get("version") and ed.get("date") else None,
        "command": f"{cmd} crawl --start-url <site>" if cmd else None,
        "cmd": cmd,
        "wheels": R.wheel_words(ed.get("wheels")) if ed.get("version") else "",
        "steps": [e for e in entries if e["kind"] in ("stop", "trap")],
        "end": next((e for e in entries if e["kind"] == "end"), None),
        "export": next((e for e in entries if e["kind"] == "export"), None),
        "handoff": None,
        "unverified": [e["id"] for e in R.unverified(route)],
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
        """Lines that fit `max_w`, broken at the strongest separator first (a semicolon, a colon, a middle dot, a
        comma), so a name like "Common Crawl" or "Python 3.13" is never split; words only as a last resort. A
        middle dot at a break is dropped; other punctuation stays at the end of its line."""
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
                    lines.extend(wrap(piece, max_w, role, seps[i + 1:]))
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

    # ================================================================ the title block (T1–T6)
    tx = G["title_x"]
    nsz, ntr = G["name_size"], G["name_track"]
    ben = k.text("Ben", tx, G["name_y"], "display", size=nsz, tracking=ntr, edition=ed, scale=sc, truth="measured",
                 key="identity:name")
    wb = k.text_width("Ben ", "display", size=nsz, tracking=ntr, edition=ed, scale=sc)
    russ = k.text("Russell", tx + wb, G["name_y"], "display", size=nsz, tracking=ntr, edition=ed, scale=sc,
                  truth="measured", key="identity:name")
    put("T1", ben + russ)
    for i, line in enumerate(p["role"]):
        lbl(line, tx, G["role_y"] + G["role_pitch"] * i, "T2", "copy:role_line", caps=True)
    fy = G["fine_y"]
    fine = []
    if not phone:
        fine.append(("T3", [("label", f"1 OF {p['repo_count']} PUBLIC REPOSITORIES", "repo_count")]))
    if p["head"]:
        fine.append(("T4", [("label", "CODE ", "repos:head"), ("machine", p["head"]["short"], "repos:head"),
                            ("label", f" · {_date(p['head']['date'])}", "repos:head")]))
    if p["ci"]:
        fine.append(("T5", [("label", p["ci"], "repos:ci")]))
    if phone:      # one line for T3 and T6: what was selected, and as of when
        fine.append(("T3+T6", None))
    else:
        fine.append(("T6", [("label", f"AS OF {_date(p['taken'])}", "taken")]))
    for gid, parts in fine:
        x = tx
        if gid == "T3+T6":
            t3 = f"1 OF {p['repo_count']} REPOSITORIES"
            lbl(t3 + " · ", x, fy, "T3", "repo_count", fill=theme.muted, caps=True)
            x += width(t3 + " · ", caps=True)
            lbl(f"AS OF {_date(p['taken'])}", x, fy, "T6", "taken", fill=theme.muted, caps=True)
        else:
            for role, text, key in parts:
                if role == "machine":
                    lbl(text, x, fy, gid, key, role="machine", fill=theme.muted)
                    x += width(text, "machine")
                else:
                    lbl(text, x, fy, gid, key, fill=theme.muted, caps=True)
                    x += width(text, caps=True)
        fy += G["fine_pitch"]

    # ================================================================ the route (R0–R15)
    X, TX, RIGHT, LH = G["track_x"], G["text_x"], G["right"], G["line"]
    y = G["head_y"]
    lbl(p["project"], TX, y, "R0", "routes:project", role="project")
    if p["language"]:
        lw = width(p["project"], "project")
        lbl(p["language"], TX + lw + G["lang_gap"], y, "R0", "repos:main_language", fill=theme.muted, caps=True)
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
        y += LH
    if p["command"]:
        lbl(p["command"], TX, y, "R3", "edition:scripts", role="machine")
        last = y
        y += LH
    note = p["wheels"]
    if note:
        for line in wrap(note, RIGHT - TX):
            lbl(line, TX, y, "R4", "edition:wheels", fill=theme.muted)
            last = y
            y += LH
    y = last + G["entry_gap"]
    track_top = bar_top + bh
    step_report = []
    for e in p["steps"]:
        gid = e["id"]
        if e["kind"] == "stop":
            cy = y - G["ring_dy"]
            r = G["ring_r"]
            put(gid, f'<circle cx="{E.fmt(X)}" cy="{E.fmt(cy)}" r="{r}" fill="{theme.paper}" {c.stroke("PEN", theme.ink)}/>')
            mark("ring", gid, (X - r - 1, cy - r - 1, X + r + 1, cy + r + 1))
            if phone or not G["rule_x"]:
                lines = wrap(e["text"], RIGHT - TX)
                for i, line in enumerate(lines):
                    lbl(line, TX, y + LH * i, gid, f"routes:{gid}")
            else:
                if e.get("file"):
                    lbl(e["file"], TX, y, gid, f"routes:{gid}", role="machine", fill=theme.ink2)
                rx = max(G["rule_x"], TX + (width(e["file"], "machine") + 20 if e.get("file") else 0))
                lines = wrap(e["text"], RIGHT - rx)
                for i, line in enumerate(lines):
                    lbl(line, rx, y + LH * i, gid, f"routes:{gid}")
        else:   # a trap: the hatch block on the left of the track, the words in ink
            x0, x1, up, dn = G["hatch"]
            y0, y1 = y - up, y + dn
            clip = f"hatch-{gid}"
            strokes = []
            span = (x1 - x0) + (y1 - y0)
            for q in range(3):
                off = span * (q + 1) / 4
                # 45° strokes, lower-left to upper-right, clipped to the block
                strokes.append(f"M{E.fmt(x0 + off - (y1 - y0))} {E.fmt(y1)}L{E.fmt(x0 + off)} {E.fmt(y0)}")
            put(gid, f'<clipPath id="{clip}"><rect x="{x0}" y="{E.fmt(y0)}" width="{x1 - x0}" height="{E.fmt(y1 - y0)}"/>'
                     f'</clipPath><path d="{"".join(strokes)}" fill="none" clip-path="url(#{clip})" '
                     f'{c.stroke("LINE", theme.accent, caps="butt")}/>')
            mark("hatch", gid, (x0, y0, x1, y1))
            lines = wrap(e["text"], RIGHT - TX)
            for i, line in enumerate(lines):
                lbl(line, TX, y + LH * i, gid, f"routes:{gid}")
        step_report.append({"id": gid, "kind": e["kind"], "y": round(y, 1), "lines": len(lines)})
        last = y + LH * (len(lines) - 1)
        y = last + G["pitch"]
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
    ex = p["export"]
    if ex and not phone and p["cmd"]:
        lbl(f"{p['cmd']} {ex['text']} → {ex['file']}", TX, y, "R14", "routes:R14", role="machine", fill=theme.ink2)
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
        return "How to start Ben Russell's crawler rustmapper and what happens to a URL inside it."
    traps = sum(1 for e in p["steps"] if e["kind"] == "trap")
    end = (p["end"] or {}).get("file")
    first = f"How to start Ben Russell's crawler {p['project']} and what happens to a URL inside it."
    if not end:
        return first
    n = {0: "no traps are", 1: "one trap is", 2: "two traps are", 3: "three traps are"}.get(traps, f"{traps} traps are")
    return f"{first} It ends at {end}; {n} marked."


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
