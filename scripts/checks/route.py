"""route — the hero claims only what rustmapper does (round 6, SPEC §7).

ROUTE-UNVERIFIED (fail): an entry of routes.<name> none of whose wordings holds: its anchors at HEAD or in the release,
  or the run-check probes it names (`runs` passed, `fails` failed); it names the entry and every reason. The sheet
  leaves such an entry out, and the gate refuses to ship the gap.
ROUTE-HEADER (fail): the project sentence's anchors or its run-check steps do not hold.
ROUTE-ENTRANCE (fail): runcheck.rustmapper missing, failed, for another version than edition.version, or dated more
  than 14 days before `taken`.
ROUTE-LABEL (fail): a source file drawn on the hero (a `machine` run ending .rs, .py or .toml) that is not the tail of
  a path among its entry's anchors, at HEAD and in the release (only the release for an entry of release scope): the
  release anchors are files of the sdist, so the data line's "every rustmapper source file it names is in that
  release" holds. Review round 3: the one exception is the hand-off's reader, which must be that hand-off's `reader`,
  read in the receiving repository at its `to_sha`, with state `runs`.
TYPE-CODE (fail, review round 3): a hero text run outside the code face holding code (`_`, `--`, `.rs`, `.jsonl`,
  export-sitemap): one face for code.
HERO-SELF-TWICE (fail, review round 3): a run of TWICE_SELF words or more drawn twice in one edition (the alt left out).
ROUTE-HANDOFF (info): each hand-off's computed state.
ROUTE-STRINGS (fail): a text run on the hero whose key is not one of the sources the spec allows, or whose truth is
  not `measured`.
ROUTE-WORDS (fail): a theme word on the hero or in its alt text (T-WORDS).
ROUTE-HEIGHT (fail): desk sheet taller than 620, phone taller than 1100 (review round 4: C1 on two lines, H1 with the
  line that says the crawl is done; today 571 and 1051, and the edition with S2 drawn, once P1 lands, 607 and 1094).
ROUTE-LEFT-EDGE (fail, review round 4): the words of every drawn row of the route (stops, the note, the hazard, the
  step) do not start at one x, right of the track; file labels left of the track are not rows' words.
ROUTE-PHONE-PX (fail): a phone text run under 14 px on a 390 px screen.
ROUTE-PURPOSE (fail): a drawn element without a row in the sheet's PURPOSE table.
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
HEIGHT = {"desk": 620, "phone": 1100}   # review round 4: C1 on two lines, H1 with its mark; S2 drawn, see LOG round 4
TWICE_SELF = 4
SOURCE_FILE = re.compile(r"[\w./-]+\.(rs|py|toml)$")
PHONE_W, PHONE_SCREEN, MIN_PX = 720, 390, 14.0


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
        h = float(e.get("h") or 0)
        if h > HEIGHT["phone" if phone else "desk"]:
            out.append(fail("ROUTE-HEIGHT", f"sheet is {h:g} tall > {HEIGHT['phone' if phone else 'desk']}", name))
        texts = [t for t in e.get("text") or [] if isinstance(t, dict)]
        for t in texts:
            key = str(t.get("key") or "")
            if key.split(":", 1)[0] not in SOURCES or t.get("truth") != "measured":
                out.append(fail("ROUTE-STRINGS", f"{t.get('s')!r} (key {key or 'none'}, truth {t.get('truth')}) "
                                "does not come from a checked source", name))
            if phone and float(t.get("size") or 0) * PHONE_SCREEN / PHONE_W < MIN_PX - 1e-6:
                out.append(fail("ROUTE-PHONE-PX", f"{t.get('s')!r} is {float(t['size']) * PHONE_SCREEN / PHONE_W:.1f} px "
                                f"on a {PHONE_SCREEN} px screen (< {MIN_PX:g})", name))
        words = theme_words(" ".join(str(t.get("s", "")) for t in texts) + " " + str(e.get("alt", "")))
        if words:
            out.append(fail("ROUTE-WORDS", f"theme words on the hero or in its alt: {', '.join(words)}", name))
        out += labels(route, texts, name, stats.get("handoffs"))
        out += left_edge(e, name)
        out += code_face(texts, name)
        out += self_twice(texts, name)
        drawn = (e.get("route") or {}).get("drawn") or []
        purpose = e.get("purpose") or {}
        for gid in drawn:
            if gid not in purpose:
                out.append(fail("ROUTE-PURPOSE", f"element {gid} is drawn but has no PURPOSE row", name))
        svg = ctx.svg_text(name)
        ids = re.findall(r'<g id="hero-([A-Z]\d+)"', svg)
        if sorted(ids) != sorted(drawn):
            out.append(fail("ROUTE-PURPOSE", f"element groups {sorted(ids)} differ from the report {sorted(drawn)}", name))
    return out
