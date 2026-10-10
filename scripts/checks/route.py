"""route — the hero claims only what rustmapper does (round 6, SPEC §7).

ROUTE-UNVERIFIED (fail): an entry of routes.<name> none of whose wordings holds: its anchors at HEAD or in the release,
  or the run-check probes it names (`runs` passed, `fails` failed); it names the entry and every reason. The sheet
  leaves such an entry out, and the gate refuses to ship the gap.
ROUTE-HEADER (fail): the project sentence's anchors or its run-check steps do not hold.
ROUTE-ENTRANCE (fail): runcheck.rustmapper missing, failed, for another version than edition.version, or dated more
  than 14 days before `taken`.
ROUTE-LABEL (fail): a source file drawn on the hero (a `machine` run ending .rs, .py or .toml) that is not the tail of
  a path among its entry's anchors, at HEAD and in the release (only the release for an entry of release scope): the
  release anchors are files of the sdist, so every rustmapper source file it names is in that release. Review round 3: the one exception is the hand-off's reader, which must be that hand-off's `reader`,
  read in the receiving repository at its `to_sha`, with state `runs`.
TYPE-CODE (fail, review round 3): a hero text run outside the code face holding code (`_`, `--`, `.rs`, `.jsonl`,
  export-sitemap): one face for code.
HERO-SELF-TWICE (fail, review round 3): a run of TWICE_SELF words or more drawn twice in one edition (the alt left out).
ROUTE-HANDOFF (info): each hand-off's computed state.
ROUTE-STRINGS (fail): a text run on the hero whose key is not one of the sources the spec allows, or whose truth is
  not `measured`.
ROUTE-WORDS (fail): a theme word on the hero or in its alt text (T-WORDS).
ROUTE-HEIGHT (fail): desk sheet taller than HEIGHT (review round 5: C1 on one line, the kill clause in the README's
  block; see HEIGHT for today's heights and those of the edition with S2 drawn, once P1 lands).
ROUTE-PAINT (fail, review round 5): a ring, bar or word group painted before the track, the loop or the line past the
  end; SVG paints in document order, and a line drawn last strikes through every ring.
ROUTE-RELEASE (fail, review round 5): the release label more than RELEASE_GAP_MAX after the end of the install command
  on its baseline, or, when it drops, not at the rows' left edge on the next line: far from its command it reads as
  the drawing's date.
ROUTE-ARROW (fail, review round 5): the loop's arrowhead comes within ring_r + 2 of a ring's centre row.
ROUTE-CODE-SPACE (fail, review round 5): a code-face run of a row's words that holds a space (code spans set their
  spaces at the label's word space, as separate runs), or a gap between two code runs of one line wider than 1.3
  times the label's space.
ROUTE-LEFT-EDGE (fail, review round 4): the words of every drawn row of the route (stops, the note, the hazard, the
  step) do not start at one x, right of the track; file labels left of the track are not rows' words.
ROUTE-PHONE-PX (fail): a phone text run under MIN_PX at PHONE_SCREEN, or under MIN_PX_NARROW at NARROW_SCREEN.
  Review round 6: GitHub's mobile profile shows the README image at the viewport less 82 px (measured on the live
  page, 10 Oct 2026): 308 px on a 390 px iPhone, 278 px on a 360 px Android; the sheet's own width is read from the
  build report.
ROUTE-PURPOSE (fail): a drawn element without a row in the sheet's PURPOSE table.
ROUTE-HEAD-GAP (fail, review round 8): on a phone edition the project's name sits less than HEAD_GAP_PITCHES times
  the role line's own pitch under the role's last baseline: closer, "PYTHON AND RUST / rustmapper" reads as one
  block of three lines, not as a role and then the drawing's heading.
"""
from __future__ import annotations

import datetime as dt
import re

from check import Finding, fail, info, warn
from data import route as R

TIER = "fast"
PROJECT = "rustmapper"
MAX_AGE = 14
SOURCES = ("routes", "handoffs", "edition", "repos", "repo_count", "taken", "copy", "identity", "runcheck")
THEME_WORDS = ("chart", "sea", "ship", "harbour", "harbor", "survey", "unsurveyed", "buoy", "light", "berth",
               "approach", "pilot", "mariner", "nautical", "sail", "anchorage", "ahoy", "arr")
WORDS_RE = re.compile(r"\b(" + "|".join(THEME_WORDS) + r")\b", re.I)
# review round 6: S1 takes a second desk line (571; with S2 drawn 607). The phone sheet is 600 wide and must stay
# inside one screen at 308 px: 640 px on screen is 1,246 units (today 1,169; with S2 drawn 1,246, after the phone's
# title gap and foot gave back 18 units; LOG round 6)
# review round 12: the mid sheet (820 wide) is served up to a 1199 px viewport, a 765 px column; drawn at most 900 px
# tall there (checks/column.py TALL_PX) is 964 units. Today 707 (S2 drawn would add about 2 lines, 56 units)
HEIGHT = {"desk": 620, "phone": 1246, "mid": 964}
# review round 8: today desk 571, phone 1,121 (the title gap is 70, F1 three phone lines); with S2 drawn about 1,198
HEAD_GAP_PITCHES = 2
RELEASE_GAP_MAX = 40
CODE_SPACE_MAX = 1.3
TWICE_SELF = 4
SOURCE_FILE = re.compile(r"[\w./-]+\.(rs|py|toml)$")
PHONE_SCREEN, MIN_PX = 308, 13.0          # review round 6: the image on a 390 px phone (viewport − 82)
NARROW_SCREEN, MIN_PX_NARROW = 278, 11.0   # on a 360 px phone


def _iso(s):
    try:
        return dt.date.fromisoformat(str(s)[:10])
    except (TypeError, ValueError):
        return None


def theme_words(text: str) -> list[str]:
    return sorted({m.group(1).lower() for m in WORDS_RE.finditer(text or "")})


def label_ok(label: str, entry: dict) -> bool:
    """True when `label` is the tail of a path among the entry's anchors on each side it describes."""
    paths = entry.get("paths") or {}

    def named(side):
        return any(p == label or p.endswith("/" + label) for p in paths.get(side) or [])
    return named("release") and (entry.get("scope") == "release" or named("head"))


def labels(route: dict, texts: list[dict], where: str, handoffs: list[dict] | None = None) -> list[Finding]:
    """ROUTE-LABEL: every source file drawn on the hero is a file of its entry, in the code it describes, or the
    reader of a hand-off that runs, read at the receiving repository's `to_sha`."""
    by = {str(e.get("id")): e for e in route.get("entries") or []}
    hos = {str(h.get("id")): h for h in handoffs or []}
    out = []
    for t in texts:
        key, s = str(t.get("key") or ""), str(t.get("s") or "")
        if t.get("role") != "machine" or not SOURCE_FILE.search(s.strip()):
            continue
        src, _, ident = key.partition(":")
        if src == "handoffs":
            h = hos.get(ident)
            if not h or h.get("reader") != s or h.get("state") != "runs" or not h.get("to_sha"):
                out.append(fail("ROUTE-LABEL", f"{s!r} is drawn as a hand-off's reader but is not the reader of a "
                                "hand-off that runs, read at its to_sha", where))
            continue
        e = by.get(ident) if src == "routes" else None
        if e is None or not label_ok(s, e):
            out.append(fail("ROUTE-LABEL", f"{s!r} is drawn ({key or 'no key'}) but is not a file among its entry's "
                            "anchors in both trees", where))
    return out


def code_face(texts: list[dict], where: str) -> list[Finding]:
    """TYPE-CODE: code is set in the code face (`machine`), wherever it is drawn."""
    from sheets.route import CODE_TOKENS
    out = []
    for t in texts:
        s = str(t.get("s") or "")
        if t.get("role") != "machine" and any(tok in s for tok in CODE_TOKENS):
            out.append(fail("TYPE-CODE", f"{s!r} holds code but is set in {t.get('role')}", where))
    return out


def self_twice(texts: list[dict], where: str, n: int = TWICE_SELF) -> list[Finding]:
    """HERO-SELF-TWICE: one edition says a run of `n` words once (review round 3: one home per fact, in the image
    too). Runs are joined per element (key) so a phrase broken across lines still counts."""
    from checks.strings import _words
    by: dict[str, list[str]] = {}
    for t in texts:
        by.setdefault(str(t.get("key") or ""), []).extend(_words(t.get("s")))
    seen: dict[tuple, str] = {}
    out = []
    for key, w in by.items():
        grams = {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}
        for g in grams:
            if g in seen and seen[g] != key:
                out.append(fail("HERO-SELF-TWICE", f"{' '.join(g)!r} is drawn twice ({seen[g]}, {key})", where))
            seen.setdefault(g, key)
    return out


def left_edge(entry: dict, where: str) -> list[Finding]:
    """ROUTE-LEFT-EDGE: the leftmost run right of the track, per drawn row, is at one x in the edition."""
    rep = entry.get("route") or {}
    track = [m["box"] for m in rep.get("marks") or [] if m.get("kind") == "track"]
    if not track:
        return []
    right = max(b[2] for b in track)
    ids = [st["id"] for st in rep.get("steps") or []]
    xs = {}
    for t in entry.get("text") or []:
        key = str(t.get("key") or "")
        if key.startswith("routes:") and key[7:] in ids and float(t.get("x0", 0)) > right:
            xs[key[7:]] = min(xs.get(key[7:], 1e9), float(t["x0"]))
    if xs and max(xs.values()) - min(xs.values()) > 0.5:
        return [fail("ROUTE-LEFT-EDGE", "rows start at " + ", ".join(f"{k} {v:.1f}" for k, v in xs.items()), where)]
    return []


def paint_order(svg: str, where: str) -> list[Finding]:
    """ROUTE-PAINT: every group that is not a line (R5 the track, R6 the loop, R15 the line past the end) comes after
    all of them in the document, so rings, bars and words are painted on top."""
    ids = re.findall(r'<g id="hero-([A-Z]\d+)"', svg or "")
    lines = [i for i, g in enumerate(ids) if g in ("R5", "R6", "R15")]
    if not lines:
        return []
    early = [g for i, g in enumerate(ids) if g not in ("R5", "R6", "R15") and i < max(lines)]
    return [fail("ROUTE-PAINT", f"{', '.join(early)} painted under a line", where)] if early else []


def release_near(entry: dict, where: str) -> list[Finding]:
    """ROUTE-RELEASE: the release label follows its command (RELEASE_GAP_MAX), or sits under it at the left edge."""
    rl = (entry.get("route") or {}).get("release_label")
    if not rl:
        return []
    if abs(rl["y"] - rl["cmd_y"]) < 0.5:
        gap = rl["x"] - rl["cmd_end"]
        if not 0 < gap <= RELEASE_GAP_MAX:
            return [fail("ROUTE-RELEASE", f"the release label starts {gap:.0f} after the command (> {RELEASE_GAP_MAX})",
                         where)]
        return []
    steps = (entry.get("route") or {}).get("steps") or []
    left = min((st["x"] for st in steps), default=rl["x"])
    if rl["y"] < rl["cmd_y"] or abs(rl["x"] - left) > 0.5:
        return [fail("ROUTE-RELEASE", f"the release label at ({rl['x']}, {rl['y']}) is neither after nor under the "
                     "command", where)]
    return []


def arrow_clear(entry: dict, where: str) -> list[Finding]:
    """ROUTE-ARROW: the loop's arrowhead keeps ring_r + 2 from every ring's centre row."""
    rep = entry.get("route") or {}
    a, r = rep.get("loop_arrow"), rep.get("ring_r")
    if not a or r is None:
        return []
    out = []
    for ring in rep.get("rings") or []:
        d = 0.0 if a[0] <= ring["cy"] <= a[1] else min(abs(ring["cy"] - a[0]), abs(ring["cy"] - a[1]))
        if d < r + 2:
            out.append(fail("ROUTE-ARROW", f"the loop's arrowhead is {d:.1f} from {ring['id']}'s ring (< {r + 2})", where))
    return out


def code_spaces(texts: list[dict], where: str, label_space: float) -> list[Finding]:
    """ROUTE-CODE-SPACE: in a row's words, a code run holds no space, and two code runs on one line are no further
    apart than CODE_SPACE_MAX label spaces."""
    out = []
    rows: dict[tuple, list[dict]] = {}
    for t in texts:
        key = str(t.get("key") or "")
        if not key.startswith("routes:"):
            continue
        if t.get("role") == "machine" and " " in str(t.get("s") or ""):
            out.append(fail("ROUTE-CODE-SPACE", f"{t.get('s')!r} sets its spaces in the code face", where))
        rows.setdefault((key, round(float(t.get("y", 0)), 1)), []).append(t)
    for (key, y), ts in rows.items():
        ts = sorted(ts, key=lambda t: float(t["x0"]))
        for a, b in zip(ts, ts[1:]):
            if a.get("role") == b.get("role") == "machine":
                gap = float(b["x0"]) - float(a["x1"])
                if gap > CODE_SPACE_MAX * label_space + 0.5:
                    out.append(fail("ROUTE-CODE-SPACE", f"{a.get('s')!r} and {b.get('s')!r} are {gap:.1f} apart "
                                    f"(> {CODE_SPACE_MAX} × {label_space:.1f})", where))
    return out


def head_gap(texts: list[dict], where: str, pitches: float = HEAD_GAP_PITCHES) -> list[Finding]:
    """ROUTE-HEAD-GAP: the gap from the role line's last baseline to the project name's, against the role's pitch."""
    role = sorted(float(t["y"]) for t in texts if t.get("key") == "copy:role_line" and t.get("y") is not None)
    proj = [float(t["y"]) for t in texts if t.get("key") == "routes:project" and t.get("y") is not None]
    if len(role) < 2 or not proj:
        return []
    pitch = role[1] - role[0]
    gap = min(proj) - role[-1]
    if gap < pitches * pitch - 1e-6:
        return [fail("ROUTE-HEAD-GAP", f"the project's name is {gap:g} under the role line, under {pitches:g} x its "
                     f"pitch ({pitch:g})", where)]
    return []


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    stats = ctx.stats or {}
    route = (stats.get("routes") or {}).get(PROJECT)
    if not isinstance(route, dict):
        return [fail("ROUTE-MISSING", f"stats.json has no routes.{PROJECT}: run build_stats.py")]
    rc = (stats.get("runcheck") or {}).get(PROJECT)
    for e in R.unverified(route, rc):
        out.append(fail("ROUTE-UNVERIFIED", f"{e.get('id')} {e.get('text')!r} is not drawn: "
                        + "; ".join(e.get("missing") or ["no reason recorded"]), "stats.json routes"))
    hok, hmiss = R.header_ok(route, rc)
    if route.get("header") and not hok:
        out.append(fail("ROUTE-HEADER", "the project sentence does not hold: " + "; ".join(hmiss), "stats.json routes"))
    ed = stats.get("edition") or {}
    if not isinstance(rc, dict):
        out.append(fail("ROUTE-ENTRANCE", "no run check recorded (scripts/runcheck.py, the workflow's runcheck job)"))
    else:
        taken, when = _iso(stats.get("taken")), _iso(rc.get("date"))
        if not rc.get("ok"):
            bad = [s.get("cmd") for s in rc.get("steps") or [] if not s.get("ok") and s.get("gate", True)]
            out.append(fail("ROUTE-ENTRANCE", f"the run check failed: {'; '.join(bad) or 'no step passed'}"))
        if str(rc.get("version")) != str(ed.get("version")):
            out.append(fail("ROUTE-ENTRANCE", f"the run check tested {rc.get('version')}; the release is {ed.get('version')}"))
        if not taken or not when or (taken - when).days > MAX_AGE:
            out.append(fail("ROUTE-ENTRANCE", f"the run check is dated {rc.get('date')}, more than {MAX_AGE} days "
                            f"before {stats.get('taken')}"))
        if not out or all(f.code != "ROUTE-ENTRANCE" for f in out):
            out.append(info("ROUTE-ENTRANCE", f"run check passed {rc.get('date')} on {rc.get('runner')} "
                            f"({rc.get('install') or 'install not recorded'})"))
    for h in stats.get("handoffs") or []:
        out.append(info("ROUTE-HANDOFF", f"{h.get('id')}: {h.get('state')}"))

    for name, e in ((ctx.report or {}).get("sheets") or {}).items():
        if not name.startswith("hero-") or name not in ctx.svgs:
            continue
        phone = "phone" in name
        sc = "phone" if phone else ("mid" if "-mid-" in name else "desk")
        h = float(e.get("h") or 0)
        if h > HEIGHT[sc]:
            out.append(fail("ROUTE-HEIGHT", f"sheet is {h:g} tall > {HEIGHT[sc]}", name))
        texts = [t for t in e.get("text") or [] if isinstance(t, dict)]
        for t in texts:
            key = str(t.get("key") or "")
            if key.split(":", 1)[0] not in SOURCES or t.get("truth") != "measured":
                out.append(fail("ROUTE-STRINGS", f"{t.get('s')!r} (key {key or 'none'}, truth {t.get('truth')}) "
                                "does not come from a checked source", name))
            if phone:
                sw = float(e.get("w") or 600)
                for screen, floor in ((PHONE_SCREEN, MIN_PX), (NARROW_SCREEN, MIN_PX_NARROW)):
                    px = float(t.get("size") or 0) * screen / sw
                    if px < floor - 1e-6:
                        out.append(fail("ROUTE-PHONE-PX", f"{t.get('s')!r} is {px:.1f} px in a {screen} px image "
                                        f"(< {floor:g})", name))
        words = theme_words(" ".join(str(t.get("s", "")) for t in texts) + " " + str(e.get("alt", "")))
        if words:
            out.append(fail("ROUTE-WORDS", f"theme words on the hero or in its alt: {', '.join(words)}", name))
        if sc in ("phone", "mid"):          # the stacked editions: the route's heading under the role line
            out += head_gap(texts, name)
        out += labels(route, texts, name, stats.get("handoffs"))
        out += left_edge(e, name)
        out += code_face(texts, name)
        out += self_twice(texts, name)
        out += release_near(e, name)
        out += arrow_clear(e, name)
        sp = (e.get("route") or {}).get("label_space")
        if sp:
            out += code_spaces(texts, name, float(sp))
        drawn = (e.get("route") or {}).get("drawn") or []
        purpose = e.get("purpose") or {}
        for gid in drawn:
            if gid not in purpose:
                out.append(fail("ROUTE-PURPOSE", f"element {gid} is drawn but has no PURPOSE row", name))
        svg = ctx.svg_text(name)
        out += paint_order(svg, name)
        ids = re.findall(r'<g id="hero-([A-Z]\d+)"', svg)
        if sorted(ids) != sorted(drawn):
            out.append(fail("ROUTE-PURPOSE", f"element groups {sorted(ids)} differ from the report {sorted(drawn)}", name))
    return out
