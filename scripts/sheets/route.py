"""route.py — the hero (round 6, SPEC.md, review round 1): the way into rustmapper.

The image answers one sentence: how you start rustmapper, what it does with each page, where a stranger goes wrong
and how to get out, and where the output goes next. Vertical position is the order of a run: what you type, what
happens to each URL, how you stop it, what you get. The rows that repeat for every page are closed by one line back
up the left side: the crawl is a loop, and the one hazard sits on that loop, with its way out on the next row.
Nothing on the sheet has a size that depends on data: every shape is a fixed mark (a bar, a ring, a dotted line, a
line), and every word comes from `stats.json` (routes, handoffs, edition, runcheck) or from
chart.toml [copy] / [identity].

Left column, the title block: the name and the role line, nothing else (review round 2: the project's name is the
route's header, and the counts and CI live in the text). Right, the route: the project's name and one sentence, the
start bar, the install line with the release, the image's one command, then the stops (a ring on the magenta
track; review round 4: every row's words start at one left edge, and on the desk each stop's source file stands
right-aligned in the empty column left of the track), the governor as a line under the fetch stop's words (no mark of
its own), the hazard (its words ringed by a dotted danger line in the accent, review round 3; with the line of output
that says the crawl is done) and the way out, the end bar, the file you get and its real field names, and a thin
line on to the one other project of his that reads that file, says what it does with it, and tests the join. Everything a reader copies or looks up (the crawl command, the install time, the CI) is in
the README, once.

A route entry is drawn only when routes.<name> says its anchors hold and the run-check probes it names came out as
stated (scripts/data/route.py `resolve`); a desk file label only when that file is among the entry's anchors in the
code it describes; the install line only when the run check passed (SPEC §6); the line past the end only when the
hand-off's state is `runs`. Nothing else is drawn: no border, no axis, no motion, no legend.

Review round 3: while the release never stops by itself (a drawn trap on the loop whose `fails` probe failed), the
track stops at the foot of the loop and starts again just above the next row's ring: the shape says, without words,
that the only way on from the loop is the reader's Ctrl-C. Once a release ends by itself the trap is retired and the
gap closes. Geometry follows that probe, never a count. Code inside a row's words (`backticked` in chart.toml) is set
in the code face at the row's size.

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
DANGER_PAD = 6           # the danger line round the trap's words: padding, corner radius, dot pitch (desk, phone)
DANGER_RX = 6
DANGER_PITCH = {"desk": 6, "phone": 8}
CODE_TOKENS = ("_", "--", ".rs", ".jsonl", "export-sitemap")   # TYPE-CODE: these are code and take the code face
RUNCHECK_MAX_AGE = 14    # days before `taken` a passing run check still counts (SPEC §7, ROUTE-ENTRANCE)

# id -> (what a stranger learns, the visitor question, where it comes from). SPEC §2.2; T-PURPOSE holds the sheet to it.
PURPOSE: dict[str, tuple[str, str, str]] = {
    "T1": ("whose page this is", "Q1", "chart.toml [identity]"),
    "T2": ("what he builds, in the first two words", "Q1", "chart.toml [copy] role_line"),
    "R0": ("which project, and what it does, before any detail", "Q2", "stats.json routes.rustmapper.header"),
    "R1": ("where you begin", "Q4", "R1-I5 (the entrance is a fixed point)"),
    "R2": ("the line that gets it, and how old the release is: the image's one command", "Q4",
           "stats.json edition.version, edition.date; runcheck.rustmapper"),
    "R5": ("one way through, in the order of a run; while the release never stops by itself the line breaks under the "
           "loop, so the only way on is the reader's Ctrl-C", "Q4", "R1-F3 (the line you follow); runcheck ends_by_itself"),
    "R6": ("the crawl is a loop: the rows it spans repeat for every page", "Q1",
           "Rust-sitemap src/bfs_crawler.rs frontier.add_links; Mercator (SRC-173 §3)"),
    "S1": ("where URLs come from, and what the release contacts by default", "Q5", "stats.json routes.rustmapper S1"),
    "S2": ("it is polite by construction: one queue per host, paced by robots.txt", "Q1", "stats.json routes.rustmapper S2"),
    "F1": ("each page is fetched and its links are queued again, on the domain of the URL you gave, its parent "
           "domains and subdomains included", "Q1", "stats.json routes.rustmapper F1 (url_utils.rs is_same_domain)"),
    "G1": ("the crawl slows when it cannot save what it found, not when the network is slow: a note on the fetch "
           "stop, since it changes how many fetches run", "Q1", "stats.json routes.rustmapper G1"),
    "W1": ("what it has found is saved to its database as it goes, every 50 ms, so an export after a kill has "
           "something to read", "Q5", "stats.json routes.rustmapper W1 (writer_thread.rs BATCH_TIMEOUT_MS; redb)"),
    "H1": ("the one catch: the release does not stop by itself, and the line of its own output that says it is done; "
           "the dotted line marks it", "Q5", "stats.json routes.rustmapper H1 (bfs_crawler.rs select! else arm, "
           "'Received work item'); runcheck ends_by_itself, quiet_after_last_page"),
    "C1": ("the reader's one step: Ctrl-C once writes the file; after a kill, the command, as installed, that writes "
           "sitemap.xml from what was saved", "Q5",
           "stats.json routes.rustmapper C1; edition.scripts; runcheck crawl_ctrl_c, kill_writes_file, export_after_kill"),
    "R12": ("where you end up", "Q4", "R2-F2 item 7 (the end of the route)"),
    "R13": ("what you get and where it is on disk, with the real field names", "Q4", "stats.json routes.rustmapper R13"),
    "R15": ("his projects are one body of work: this output is sorted by another, and that join is tested", "Q2",
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
     "page (fetch, the governor under it, the log), closed by one line back up the left side; the hazard sits on "
     "that line and its way out on the next row",
     "a crawler is a loop: links found on a page go back on the queue (bfs_crawler.rs frontier.add_links); the "
     "release never stops by itself (run check, ends_by_itself), and a list cannot show where the repeat closes"),
    ("The governor is a note under fetch",
     "the governor's words are the last line of the fetch stop's row, in the secondary ink, with no mark on the track",
     "it changes how many fetches run at once (governor THROTTLE_THRESHOLD_MS, add_permits), so it qualifies that "
     "stop; on a metro map a short tick is a station, which it is not (review round 4)"),
    ("Fixed marks, no sizes",
     "every bar, ring, dotted line and line has a fixed size; only the number of lines of text moves anything",
     "the owner could not tell what the old islands' sizes meant (9 Oct 2026); here nothing has a size to read"),
    ("Drawn only when checked",
     "an entry is drawn only when its anchors hold in the code at HEAD and in the released sdist; the install lines "
     "only when the run check passed; the line past the end only when the reader's fields are in the writer's struct",
     "the image claims only what the tool does (SPEC §5, §6)"),
    ("Trap text in ink, ringed by dots",
     "the trap's words are set in ink inside a dotted line of the accent with no fill (review round 3: the band and "
     "the hatch are cut)",
     "accent on day paper is 4.1:1, under the 4.5:1 text needs, and over 3:1 as a line in both themes; a dotted line "
     "round a danger marks it without a fill (INT 1, K1), and a filled band read as an editor's highlight"),
    ("A gap in the track under the loop",
     "while the release never stops by itself, the track ends at the loop's foot and starts again just above the "
     "next row's ring, and that row moves down by the gap",
     "the run check's crawl of a three-page site was still running at 150 s (ends_by_itself); a line that ran on "
     "would say the run ends on its own"),
    ("Code in the code face",
     "file names, field names and subcommands inside a row's words are set in the code face at the row's size",
     "the end row's file name was already set that way, and one face for code tells a reader what to type"),
    ("Phone role line at 204",
     "on the phone the role line sits at 204 (SPEC: 196) and everything under it 8 lower",
     "at 196 its text box meets the descent of the name set at 132 (the bounds check measures the font's boxes)"),
    ("Phone drops file names",
     "on the phone the stops carry their rules only",
     "720 px leaves 600 px for text at the 26 px floor"),
    ("Desk file names left of the track",
     "on the desk every row's words start at x 484, as on the phone, and each stop's source file is set in the code "
     "face, muted, right-aligned to x 424 on the row's first baseline; if one would touch the title block, none is "
     "drawn",
     "with each rule after its own file name the rows started at four different x's and read as a rendering bug "
     "(review round 4); the column under the role line was empty"),
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
             "role_pitch": 28, "fine_gap": 52, "fine_pitch": 28, "track_x": 456, "text_x": 484, "file_right": 424,
             "right": 1224, "head_y": 84, "head_after_title": None, "sent_gap": 34, "line": 28, "bar_gap": 30,
             "bar_w": 24, "bar_h": 4, "r2_gap": 30, "entry_gap": 42, "pitch": 36, "end_gap": 30, "r13_gap": 30,
             "ring_r": 6, "ring_dy": 6, "loop_out": 14,
             "loop_dy": 13, "loop_arrow": (8, 10), "gap": 16, "stub": 10, "after_end": 26, "tip": 8, "label_gap": 14,
             "arrow_w": 10, "rule_after_file": 20, "foot": 36},
    "phone": {"title_x": 40, "title_w": 640, "name_size": 132, "name_track": -2.0, "name_y": 140, "role_y": 204,
              "role_pitch": 34, "fine_gap": 46, "fine_pitch": 34, "track_x": 56, "text_x": 88, "file_right": None,
              "right": 688, "head_y": None, "head_after_title": 60, "sent_gap": 40, "line": 34, "bar_gap": 28,
              "bar_w": 24, "bar_h": 4, "r2_gap": 38, "entry_gap": 46, "pitch": 43, "end_gap": 24, "r13_gap": 38,
              "ring_r": 8, "ring_dy": 9, "loop_out": 18,
              "loop_dy": 15, "loop_arrow": (10, 12), "gap": 18, "stub": 12, "after_end": 24, "tip": 8, "label_gap": 14,
              "arrow_w": 12, "rule_after_file": None, "foot": 30},
}
TRACK = {"desk": 1.6, "phone": 1.0}
FILE_CLEAR = 4           # review round 4: a desk file label keeps this far from the title block's boxes


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
    """`ink` laid over `paper` at `alpha`, as one opaque colour."""
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
    cmd = R.command_name(ed.get("scripts"), project)  # raises when the release ships no command: nothing to install
    header_ok, _ = R.header_ok(route, rc)
    p = {
        "project": aliases.get(repo_name, project),
        "repo": repo_name,
        "header": route.get("header") if header_ok else None,
        "role": [s.strip() for s in str((cfg.get("copy") or {}).get("role_line") or "").split("·") if s.strip()],
        "entrance": ok, "entrance_why": why,
        "install": f"pip install {ed.get('project') or project}" if ok and ed.get("version") else None,
        "release": f"{ed['version']} · {_date(ed['date'])}" if ok and ed.get("version") and ed.get("date") else None,
        # review round 4: a command in a row's words is named as the wheel installs it, as in the README's block
        "steps": [dict(e, text=str(e["text"]).replace("{script}", cmd)) for e in entries
                  if e["kind"] in ("stop", "step", "note", "trap")],
        "end": next((e for e in entries if e["kind"] == "end"), None),
        "handoff": None,
        "unverified": [e["id"] for e in R.unverified(route, rc)],
    }
    # review round 3: the track breaks under the loop while a trap on it names a probe that failed (the release does
    # not stop by itself); drawn() only returns that trap while its `fails` probes failed
    p["gap"] = any(e["kind"] == "trap" and e.get("loop") and e.get("fails") for e in p["steps"])
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

    label_size = tokens.ROLES[sc]["label"][1]

    def segments(text):
        """`a `code` b` -> [("a ", False), ("code", True), (" b", False)]; an unclosed span runs to the end."""
        out, code = [], False
        for i, piece in enumerate(str(text).split("`")):
            if i:
                code = not code
            if piece:
                out.append((piece, code))
        return out

    def fit(text, role="label"):
        """Width for line breaking, measured in the day cut: night's Light cuts are narrower, so a line that fits
        by day fits by night, and both editions break at the same words. Code spans measure in the code face."""
        total = 0.0
        for piece, code in segments(text):
            if code and role == "label":
                total += k.text_width(piece, "machine", edition=day_ed, scale=sc, size=label_size)
            else:
                total += k.text_width(piece, role, edition=day_ed, scale=sc)
        return total

    def balance(lines):
        """Re-open a code span cut by a line break on the next line, so each line's backticks pair up."""
        out, open_ = [], False
        for ln in lines:
            s_ = ("`" if open_ else "") + ln
            open_ = open_ ^ (ln.count("`") % 2 == 1)
            if open_:
                s_ += "`"
            out.append(s_.replace("``", ""))
        return out

    def wrap(text, max_w, role="label", seps=("; ", ": ", " · ", ", ")):
        """Lines that fit `max_w`: broken at the strongest separator (a semicolon, a colon, a middle dot, a comma),
        so a name like "Common Crawl" or "Python 3.13" is not split, unless breaking at words takes fewer lines or
        the separator leaves a line under 45 % of the measure (review round 3: "start URL;" alone read as its own
        item). Word breaks are balanced: the narrowest measure that keeps the same number of lines."""
        by_sep = _wrap_sep(text, max_w, role, seps)
        by_word = _balanced(text, max_w, role)
        short = len(by_sep) > 1 and any(fit(ln, role) < 0.45 * max_w for ln in by_sep)
        return balance(by_word if len(by_word) < len(by_sep) or short else by_sep)

    def _balanced(text, max_w, role):
        lines = _wrap_sep(text, max_w, role, ())
        if len(lines) < 2:
            return lines
        lo, hi = max(fit(wd, role) for wd in str(text).split()), float(max_w)
        for _ in range(24):
            mid = (lo + hi) / 2
            if len(_wrap_sep(text, mid, role, ())) <= len(lines):
                hi = mid
            else:
                lo = mid
        return _wrap_sep(text, hi, role, ())

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

    def say(text, x, y, gid, key, fill=None):
        """One line of a row's words: plain runs in the label face, code spans in the code face at the same size.
        Returns the line's drawn width."""
        x0 = x
        for piece, code in segments(text):
            if code:
                lbl(piece, x, y, gid, key, role="machine", fill=fill, size=label_size)
                x += width(piece, "machine", size=label_size)
            else:
                lbl(piece, x, y, gid, key, fill=fill)
                x += width(piece)
        return x - x0

    def mark(kind, gid, box):
        k.exclude(f"{kind}:{gid}", box[0], box[1], box[2] - box[0], box[3] - box[1])
        marks.append({"kind": kind, "id": gid, "box": [round(v, 1) for v in box]})

    def _danger(row):
        """Review round 3: a dotted danger line round the trap's words, in the accent, with no fill (INT 1, K1): a
        rounded rectangle DANGER_PAD outside the text block (the font's ascent over the first baseline to its descent
        under the last, the widest line across), its dots spaced evenly round the perimeter near DANGER_PITCH. Its
        four edges are exclusions, so no text may cross the line. Its size follows the trap's words only."""
        asc, desc = k.extent("label", edition=ed, scale=sc)
        pad, rx = DANGER_PAD, DANGER_RX
        x0, x1 = row["x"] - pad, row["x"] + row["w"] + pad
        y0, y1 = row["y"] - asc - pad, row["last"] + desc + pad
        w_, h_ = x1 - x0, y1 - y0
        per = 2 * (w_ + h_) - 8 * rx + 2 * 3.141592653589793 * rx
        gap = per / max(1, round(per / DANGER_PITCH[sc]))
        put(row["id"], f'<rect x="{E.fmt(x0)}" y="{E.fmt(y0)}" width="{E.fmt(w_)}" height="{E.fmt(h_)}" rx="{rx}" '
                       f'fill="none" {c.stroke("BRUSH", theme.accent, dash_key="DANGER", gap=gap)}/>')
        t = float(c.width("BRUSH")) / 2 + 0.5
        for nm, box in (("top", (x0 - t, y0 - t, x1 + t, y0 + t)), ("bottom", (x0 - t, y1 - t, x1 + t, y1 + t)),
                        ("left", (x0 - t, y0 - t, x0 + t, y1 + t)), ("right", (x1 - t, y0 - t, x1 + t, y1 + t))):
            k.exclude(f"danger-{nm}:{row['id']}", box[0], box[1], box[2] - box[0], box[3] - box[1])
        marks.append({"kind": "danger", "id": row["id"], "box": [round(v, 1) for v in (x0, y0, x1, y1)]})

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
    n_asc, n_desc = k.extent("display", edition=ed, scale=sc, size=nsz)
    title_boxes = [(tx, G["name_y"] - n_asc, tx + wb + k.text_width("Russell", "display", size=nsz, tracking=ntr,
                                                                    edition=ed, scale=sc), G["name_y"] + n_desc)]
    l_asc, l_desc = k.extent("label", edition=ed, scale=sc)
    for i, line in enumerate(p["role"]):
        title_last = G["role_y"] + G["role_pitch"] * i
        lbl(line, tx, title_last, "T2", "copy:role_line", caps=True)
        title_boxes.append((tx, title_last - l_asc, tx + width(line, caps=True), title_last + l_desc))

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
    gap_rows: list[dict] = []     # the row the track starts again above, when the loop has no way out
    prev_loop = False
    files: list[tuple[str, float, str]] = []     # desk file labels, drawn once every row is placed (review round 4)
    for e in p["steps"]:
        gid = e["id"]
        kind = e["kind"]
        # review round 4: the governor changes how many fetches run at once, so it is a line under the fetch stop's
        # words in the secondary ink, with no mark of its own (on a metro map a tick is a station)
        host = rows[-1] if (kind == "note" and rows and rows[-1]["kind"] in ("stop", "step")
                            and bool(rows[-1]["loop"]) == bool(e.get("loop"))) else None
        if host is not None:
            lines = wrap(e["text"], RIGHT - host["x"])
            for i, ln in enumerate(lines):
                say(ln, host["x"], host["last"] + LH * (i + 1), gid, f"routes:{gid}", fill=theme.ink2)
            host["last"] += LH * len(lines)
            host["notes"] = host.get("notes", []) + [gid]
            step_report.append({"id": gid, "kind": kind, "y": round(host["last"] - LH * (len(lines) - 1), 1),
                                "lines": len(lines), "loop": bool(e.get("loop")), "x": round(host["x"], 1),
                                "under": host["id"]})
            last = host["last"]
            y = last + G["pitch"]
            continue
        if p["gap"] and prev_loop and not e.get("loop"):
            y += G["gap"] - (G["pitch"] - G["ring_dy"] - G["ring_r"] - G["stub"] - G["loop_dy"])
        r = G["ring_r"]
        cy = y - G["ring_dy"]
        if kind in ("stop", "step"):
            put(gid, f'<circle cx="{E.fmt(X)}" cy="{E.fmt(cy)}" r="{r}" fill="{theme.paper}" {c.stroke("PEN", theme.ink)}/>')
            mark("ring", gid, (X - r - 1, cy - r - 1, X + r + 1, cy + r + 1))
        ink = theme.ink2 if kind == "note" else theme.ink
        # review round 4: one left edge for every row's words, the phone's and the desk's; the desk's file labels
        # stand in the empty column left of the track, right-aligned, on the row's first baseline
        rx = TX
        if kind in ("stop", "note") and G["file_right"] and e.get("file"):
            files.append((str(e["file"]), y, gid))
        lines = wrap(e["text"], RIGHT - rx)
        wmax = 0.0
        for i, ln in enumerate(lines):
            wmax = max(wmax, say(ln, rx, y + LH * i, gid, f"routes:{gid}", fill=ink))
        row = {"id": gid, "kind": kind, "y": y, "cy": cy, "last": y + LH * (len(lines) - 1), "loop": e.get("loop"),
               "x": rx, "w": wmax}
        rows.append(row)
        if e.get("loop"):
            loop_rows.append(row)
        elif prev_loop and p["gap"]:
            gap_rows.append(row)
        prev_loop = bool(e.get("loop"))
        step_report.append({"id": gid, "kind": kind, "y": round(y, 1), "lines": len(lines), "loop": bool(e.get("loop")),
                            "x": round(rx, 1)})
        last = row["last"]
        y = last + G["pitch"]
    # the desk file labels: all of them or none (review round 4). Each is right-aligned to file_right, clear of the
    # title block's boxes by FILE_CLEAR and of the loop's line on the left of the track; if one cannot be, none is
    # drawn, so the column never reads as half a table.
    labels_drawn = False
    if files:
        f_asc, f_desc = k.extent("machine", edition=ed, scale=sc)
        bracket = X - G["loop_out"] - G["loop_arrow"][0] / 2
        fits = G["file_right"] <= bracket - 8
        for name, fy, _gid in files:
            x0 = G["file_right"] - width(name, "machine")
            box = (x0 - FILE_CLEAR, fy - f_asc - FILE_CLEAR, G["file_right"] + FILE_CLEAR, fy + f_desc + FILE_CLEAR)
            if x0 < G["title_x"] or any(box[0] < b[2] and b[0] < box[2] and box[1] < b[3] and b[1] < box[3]
                                        for b in title_boxes):
                fits = False
        if fits:
            for name, fy, fgid in files:
                lbl(name, G["file_right"], fy, fgid, f"routes:{fgid}", role="machine", fill=theme.muted, anchor="end")
            labels_drawn = True
    # ---- the loop: one line back up the left side, from under the last repeating row to the first one's ring
    y_bot = None
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
    for row in rows:            # the hazard's words, ringed by the danger line
        if row["kind"] == "trap":
            _danger(row)
    end_top = last + G["end_gap"]
    # ---- the track: one segment from the start bar to the end bar, or, while the loop has no way out, two: down to
    # the loop's foot, then again from just above the next row's ring
    segs = [(track_top, end_top)]
    if p["gap"] and y_bot is not None and gap_rows:
        resume = gap_rows[0]["cy"] - G["ring_r"] - G["stub"]
        segs = [(track_top, y_bot), (resume, end_top)]
    d = "".join(f"M{E.fmt(X)} {E.fmt(a_)}V{E.fmt(b_)}" for a_, b_ in segs)
    put("R5", f'<path d="{d}" fill="none" {c.stroke("BRUSH", theme.flare, caps="butt")}/>')
    for a_, b_ in segs:
        mark("track", "R5", (X - 2, a_, X + 2, b_))
    put("R12", f'<rect x="{E.fmt(X - bw / 2)}" y="{E.fmt(end_top)}" width="{bw}" height="{bh}" fill="{theme.flare}"/>')
    mark("bar", "R12", (X - bw / 2, end_top, X + bw / 2, end_top + bh))
    y = end_top + G["r13_gap"]
    last = end_top
    end = p["end"]
    if end:
        if phone:
            lbl(end["file"], TX, y, "R13", "routes:R13", role="machine")
            for i, ln in enumerate(wrap(end["text"], RIGHT - TX)):
                y += LH
                say(ln, TX, y, "R13", "routes:R13")
        else:
            lbl(end["file"], TX, y, "R13", "routes:R13", role="machine")
            rx = TX + width(end["file"], "machine") + G["rule_after_file"]
            say(end["text"], rx, y, "R13", "routes:R13")
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
        verb = ho.get("does") or "read by"      # review round 4: what the next project does with the file
        if phone:
            lbl(f"{verb} {to}, with a test", TX, ly, "R15", "handoffs:" + ho["id"], fill=theme.ink2)
        else:
            x = TX
            first = f"{verb} {to}: "
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
                    "last_baseline": round(last, 1), "height": h,
                    "track": [[round(a_, 1), round(b_, 1)] for a_, b_ in segs], "gap": bool(len(segs) > 1),
                    "file_labels": labels_drawn}
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
