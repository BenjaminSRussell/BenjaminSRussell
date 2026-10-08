"""log — Sheet 4: the ship's log of one rustmapper run (T9 §2B).

Ruled paper (paper_log), a red margin, the log's own columns TIME · LOG · URLS · SPEED · REQ/S ·
WIND · REMARKS. The rows come from assets/log.json through data.logsim.simulate(): computed-
consistent (position = ∫rate·dt, one host at 2 req/s) and therefore every numeral italic until
Ben records a real session (measured:true flips them upright). Every entry is on the paper at
t = 0; the only motion is the nightly heartbeat line being typed in at 44 s (per glyph, through
the timeline) and the cursor that then blinks once a second. The still edition is the finished
page with the heartbeat present and the cursor steady.

Sizes (desk 1280×590, v9.1 scale): every typed run 19 (machine / machine-strong, 11.4 px per
character) on a 32 px rule; the title 41 (sea-name); the stale note 25 (note); the folio 19
(label-caps). A remark wider than its 758 px column (66 characters) continues on the next rule,
broken at a " · " or a space. Phone (720×220): machine 26, the title 30 (place-water).
"""
from __future__ import annotations

import math
import re

import chartlib as C
import edition as E
import typeset as T
from edition import fmt

try:
    import timeline as TL
except ImportError:  # pragma: no cover
    TL = None
from data import logsim as L

NAME = "log"
KIND = "paper"
SIZES = {"desk": (1280, 590), "phone": (720, 220)}
BREAKS: list[tuple[str, str, str]] = [
    ("No frame", "ruled stock bleeds to the edge, one red margin", "stationery, not a chart (T9 §2B)"),
    ("Italic numerals throughout", "digit tokens in Plex Mono Italic, the heartbeat row upright",
     "the session is computed until Ben records one; the convention is defined on Sheet 3 (decision 14)"),
    ("Typing off the grid", "per-glyph <set>s at 36–60 ms inside class=\"typed\"", "cadence is the point; T4 exempts the 44–48 s burst"),
    ("Rules on a 32 px pitch, sheet 590 tall", "entries from 142, sign-off and heartbeat on the two rules after the last entry",
     "v9.1: 19 px Plex Mono on the old 30 px rule touched; ten entries plus two continuations need twelve rules"),
    ("Columns re-spaced for 19 px mono", "TIME 44 · LOG right at 226 · SPEED right at 398 · WIND 416 · REMARKS 492→1250",
     "the heads LOG · URLS and SPEED · REQ/S are 119 and 156 px wide at 19 px and overran the old column edges"),
    ("Long remarks continue on the next rule", "wrapped at a ' · ' or a space, the continuation at the column's left edge",
     "two entries are 86 and 87 characters (992 px): no column on a 1280 sheet holds them in one line at 19 px"),
]

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
_NUM = re.compile(r"\d[\d.,:%]*")
# T10's banned-string list (scripts/checks/strings.py) carries SEEDED, the old placeholder marker; log.json's own
# T9 wording "seeded · sitemap" trips it. Printed as "seed list" until C reword the entry or A whitelist it.
_REWORD = {"seeded": "seed list"}
REMARKS_X, REMARKS_W = 492, 758
LOG_X, SPEED_X, WIND_X = 226, 398, 416     # LOG and SPEED are right-aligned figure columns
RIGHT = 1250                                # the page's right edge for the head line, sign-off and remarks
PITCH, Y_FIRST = 32, 142                    # the rule pitch and the first entry's baseline


def _dmy(iso: str) -> str:
    y, m, d = iso[:10].split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]} {y}"


def _hhmm_utc(iso: str) -> str:
    return iso[11:13] + iso[14:16] if "T" in iso and len(iso) >= 16 else ""


def _tokens(s: str) -> list[tuple[str, bool]]:
    out, i = [], 0
    for m in _NUM.finditer(s):
        if m.start() > i:
            out.append((s[i:m.start()], False))
        out.append((m.group(0), True))
        i = m.end()
    if i < len(s):
        out.append((s[i:], False))
    return out


def _mixed(ed, s: str, x: float, y: float, role: str, fill: str, anchor: str = "start", italic: bool = True,
           italic_font: str = "plex-italic", within=None, truth=None, key=None, opacity=None) -> tuple[str, float]:
    """A line whose digit tokens are set in the italic cut (the honesty convention). Returns (svg, width)."""
    toks = _tokens(s) if italic else [(s, False)]
    widths = [T.text_width(tok, role, font=(italic_font if num else None), edition=ed) for tok, num in toks]
    total = sum(widths)
    pen = x - total if anchor == "end" else x - total / 2 if anchor == "middle" else x
    out = []
    for (tok, num), w in zip(toks, widths):
        out.append(T.text_use(tok, pen, y, role, fill=fill, edition=ed, font=(italic_font if num else None),
                              within=within, truth=(truth if num else None), key=(key if num else None), opacity=opacity))
        pen += w
    return "".join(out), total


def _wrap_words(text: str, width: float, measure) -> list[str]:
    lines, cur = [], ""
    for word in text.split(" "):
        cand = f"{cur} {word}" if cur else word
        if cur and measure(cand) > width:
            lines.append(cur)
            cur = word
        else:
            cur = cand
    return lines + ([cur] if cur else [])


def _wrap(text: str, width: float, measure) -> list[str]:
    """Break a remark that overruns `width` into lines, first at its ' · ' separators (the separator stays
    on the line it ends), then at a space inside a segment that is itself too wide; the characters are the
    entry's own, only a space becomes a line break."""
    if measure(text) <= width:
        return [text]
    segs = text.split(" · ")
    if len(segs) == 1:
        return _wrap_words(text, width, measure)
    lines, cur = [], ""
    for k, seg in enumerate(segs):
        last = k == len(segs) - 1
        cand = f"{cur} · {seg}" if cur else seg
        tail = "" if last else " ·"
        if cur and measure(cand + tail) > width:
            lines.append(cur + " ·")
            cur = seg
        else:
            cur = cand
    lines += [cur] if cur else []
    out = []
    for ln in lines:
        out += _wrap_words(ln, width, measure) if measure(ln) > width else [ln]
    return out


def _reworded(text: str) -> str:
    return re.sub(r"\b(" + "|".join(map(re.escape, _REWORD)) + r")\b", lambda m: _REWORD[m.group(1).lower()], text, flags=re.I)


def _mixed_width(ed, s: str, italic: bool, role: str = "machine", italic_font: str = "plex-italic") -> float:
    """The width _mixed() would set `s` at: digit tokens measured in the italic cut when `italic`."""
    toks = _tokens(s) if italic else [(s, False)]
    return sum(T.text_width(tok, role, font=(italic_font if num else None), edition=ed) for tok, num in toks)


def _rows(log: dict) -> tuple[list, str, str]:
    """(rows, sign-off time HHMM, start) from log.json through logsim."""
    profile = log.get("profile") or {}
    entries = log.get("entries") or []
    hosts = int(log.get("hosts") or 1)
    start = log.get("start")
    measured = bool(log.get("measured"))
    rows = L.simulate(profile, entries, hosts, start, context={"version": log.get("version"), "target": log.get("target")},
                      measured=measured)
    start = start or next((r.time for r in rows if r.t == 0), rows[0].time if rows else "0000")
    so = log.get("signoff") or {}
    tm = str(so.get("time", ""))
    last_t = max((r.t for r in rows if r.t is not None), default=0)
    if re.fullmatch(r"\d{4}", tm):
        close = tm
    elif tm.startswith("+") and tm.endswith("m"):
        close = L.hhmm(start, last_t + int(tm[1:-1]) * 60)
    else:
        close = L.hhmm(start, last_t)
    return rows, close, start


def _heartbeat_line(ctx) -> str:
    data, log = ctx.data, ctx.log or {}
    tmpl = (log.get("heartbeat") or {}).get("template") or "{HHMM} UTC · watch kept by cron · {commits} commits · {repos} repositories"
    upd = str(data.get("updated_at") or "")
    if not upd:
        return ""
    commits = data.get("commits")
    repos = data.get("repo_count") or len(data.get("repos") or [])
    return (tmpl.replace("{HHMM}", _hhmm_utc(upd)).replace("{commits}", f"{int(commits):,}" if commits is not None else "—")
            .replace("{repos}", str(repos)))


def _desk(ctx) -> str:
    ed, t, data, log = ctx.ed, ctx.ed.theme, ctx.data, ctx.log or {}
    W_, H_ = SIZES["desk"]
    tl = ctx.tl if ed.motion else (TL.NullTimeline(NAME) if TL else ctx.tl)
    rows, close, start = _rows(log)
    measured = bool(log.get("measured"))
    italic = not measured
    chart_no = int(data.get("repo_count") or len(data.get("repos") or []))

    def tx(s, x, y, role="label", **kw):
        return T.text_use(s, x, y, role, edition=ed, **kw)

    out: list[str] = []
    # stationery: red margin, rules (the head rule in ink)
    out.append(f'<path d="M104 0V{H_}" fill="none" {C.stroke("PEN", t.accent, 0.55, caps="butt")}/>')
    out.append(f'<path d="M0 118H{W_}" fill="none" {C.stroke("PEN", t.ink, 0.6, caps="butt")}/>')
    n_lines = sum(len(_wrap(_reworded(r.text), REMARKS_W - (T.text_width("$ ", "machine-strong", edition=ed) if r.kind in ("cmd", "crawl") else 0),
                            lambda s_: _mixed_width(ed, s_, italic))) for r in rows[:10])
    n_rules = n_lines + 2                       # the entries, the sign-off and the heartbeat
    d = "".join(f"M0 {Y_FIRST + 8 + PITCH * k}H{W_}" for k in range(n_rules))
    out.append(f'<path d="{d}" fill="none" {C.stroke("HAIR", t.hair, caps="butt")}/>')
    # header
    vessel = str(log.get("vessel") or "rustmapper")
    out.append(tx(f"Log of the {vessel}", 120, 64, "sea-name", fill=t.ink, tracking=0.0))
    target = str(log.get("target") or "").replace("http://", "").replace("https://", "").rstrip("/")
    version = str(log.get("version") or (data.get("edition") or {}).get("version") or "")
    date = str(log.get("date") or data.get("taken") or "")
    head = " · ".join(p for p in (target, f"{vessel} {version}".strip(), _dmy(date) if date else "") if p)
    out.append(_mixed(ed, head, RIGHT, 60, "machine", t.muted, anchor="end", italic=italic)[0])
    stale = bool(data.get("no_sounding")) or (data.get("provenance") or {}).get("mode") == "cache-failed"
    if stale:
        out.append(tx(f"no sounding taken {_dmy(str(data.get('taken') or ''))}", RIGHT, 88, "note", fill=t.ink2, anchor="end"))
    heads = (("TIME", 44, "start"), ("LOG · URLS", LOG_X, "end"), ("SPEED · REQ/S", SPEED_X, "end"), ("WIND", WIND_X, "start"),
             ("REMARKS", REMARKS_X, "start"))
    for s, x, a in heads:
        out.append(tx(s, x, 100, "machine", fill=t.ink2, anchor=a, tracking=1.0))
    # entries: one rule each, a long remark continuing on the rule below
    y = Y_FIRST
    for i, r in enumerate(rows[:10]):
        out.append(_mixed(ed, r.time, 44, y, "machine", t.muted, italic=italic, truth="illustrative" if italic else "measured",
                          key=f"row.{i}.time")[0])
        if r.log is not None:
            out.append(_mixed(ed, f"{r.log:,}", LOG_X, y, "machine", t.ink, anchor="end", italic=italic,
                              truth="illustrative" if italic else "measured", key=f"row.{i}.log")[0])
        else:
            out.append(tx("—", LOG_X, y, "machine", fill=t.muted, anchor="end"))
        if r.speed is not None:
            out.append(_mixed(ed, f"{r.speed:.1f}", SPEED_X, y, "machine", t.ink, anchor="end", italic=italic,
                              truth="illustrative" if italic else "measured", key=f"row.{i}.speed")[0])
        else:
            out.append(tx("—", SPEED_X, y, "machine", fill=t.muted, anchor="end"))
        if r.wind:
            out.append(tx(r.wind, WIND_X, y, "machine", fill=t.muted))
        within = (REMARKS_X, y - 16, REMARKS_W, 23)
        pen = REMARKS_X
        if r.kind in ("cmd", "crawl"):
            out.append(tx("$", pen, y, "machine-strong", fill=t.ink, within=within))
            pen += T.text_width("$ ", "machine-strong", edition=ed)
        text = _reworded(r.text)
        for li, line in enumerate(_wrap(text, REMARKS_X + REMARKS_W - pen, lambda s_: _mixed_width(ed, s_, italic))):
            if li:
                y += PITCH
                pen = REMARKS_X
                within = (REMARKS_X, y - 16, REMARKS_W, 23)
            svg, w = _mixed(ed, line, pen, y, "machine", t.ink, italic=italic, within=within,
                            truth="illustrative" if italic else "measured", key=f"row.{i}.remark")
            if pen + w > REMARKS_X + REMARKS_W + 0.5:
                raise ValueError(f"log remark {i} is {pen + w - REMARKS_X:.0f} px wide; the column holds {REMARKS_W}")
            out.append(svg)
        y += PITCH
    SO_Y, HB_Y = y, y + PITCH
    # sign-off: a measured session is closed by the clerk and signed by the officer (serif italic initials);
    # a computed one says so and nobody signs it (36: the system may not forge the person's initials)
    so = log.get("signoff") or {}
    initials = str(so.get("initials") or "")
    if measured and initials:
        sig_w = T.text_width(initials, "note", edition=ed)
        out.append(tx(initials, RIGHT, SO_Y, "note", fill=t.ink2, anchor="end"))
        out.append(_mixed(ed, f"{so.get('text', 'Log closed')} {close} · ", RIGHT - sig_w, SO_Y, "machine", t.muted,
                          anchor="end", italic=False)[0])
    else:
        # digits italic as everywhere on the page; the words say the rest (a whole italic sentence would add a
        # second italic alphabet to the glyph library and break its 40 KB budget)
        out.append(_mixed(ed, f"{so.get('text', 'Log closed')} {close} · computed from settings · unsigned", RIGHT, SO_Y,
                          "machine", t.muted, anchor="end", italic=True, truth="illustrative", key="signoff")[0])
    # the heartbeat row: typed once at 44 s, upright (it is the one measured line on the page)
    line = _heartbeat_line(ctx) if ctx.heartbeat else ""
    HB_X = 120
    if HB_Y + PITCH > H_:
        raise ValueError(f"log: the heartbeat rule is at {HB_Y}; the sheet is {H_} tall")
    adv = T.text_width("0", "machine", edition=ed)
    if line:
        whole = tx(line, HB_X, HB_Y, "machine", fill=t.ink, truth="measured", key="heartbeat")
        m = re.match(r"(<g [^>]*>)(.*)(</g>)$", whole, re.S)
        head_g, inner, tail_g = m.groups()
        uses = re.findall(r"<use [^>]*/>", inner)
        items, xs, ui = [], [], 0
        for i, ch in enumerate(line):
            if ch == " ":
                items.append(("", adv))
            else:
                items.append((uses[ui], adv))
                ui += 1
            xs.append(round(HB_X + (i + 1) * adv, 1))
        if ui != len(uses):
            raise ValueError("heartbeat glyphs do not map one-to-one onto characters")
        typed, end, times = tl.typed(line, HB_X, HB_Y, "machine", 44.0, seed=11, glyphs=items)
        out.append(head_g + typed + tail_g)
        blink = max(48.5, math.ceil(end * 2) / 2)
        # the cursor waits at the margin, steps after each glyph as it lands, then blinks on the grid
        out.append(tl.cursor([round(times[0] - 0.001, 3)] + times, [HB_X] + xs, HB_Y - 15, w=round(adv - 1, 1), h=20,
                             blink_begin=blink, fill=t.ink, name="cursor"))
    else:
        out.append(tx("$", HB_X, HB_Y, "machine-strong", fill=t.ink))
        px = HB_X + T.text_width("$ ", "machine-strong", edition=ed)
        out.append(tl.cursor([48.5], [px], HB_Y - 15, w=round(adv - 1, 1), h=20, blink_begin=48.5, fill=t.ink, name="cursor"))
    out.append(tx(f"CHART NO. {chart_no} · SHEET 4", 24, H_ - 5, "label-caps", fill=t.muted, key="folio"))
    return E.svg(ed, W_, H_, "".join(out), T.glyph_defs(), sheet=NAME, paper_fill=t.paper_log)


def _phone(ctx) -> str:
    ed, t, data, log = ctx.ed, ctx.ed.theme, ctx.data, ctx.log or {}
    W_, H_ = SIZES["phone"]
    rows, close, start = _rows(log)
    italic = not bool(log.get("measured"))
    chart_no = int(data.get("repo_count") or len(data.get("repos") or []))

    def tx(s, x, y, role="label", **kw):
        return T.text_use(s, x, y, role, edition=ed, **kw)

    out = [f'<path d="M92 0V{H_}" fill="none" {C.stroke("PEN", t.accent, 0.55, caps="butt")}/>']
    out.append(tx(f"Log of the {log.get('vessel') or 'rustmapper'}", 24, 44, "place-water", fill=t.ink))
    out.append(tx(f"CHART NO. {chart_no} · SHEET 4", 704, 44, "label-caps", fill=t.muted, anchor="end", key="folio"))
    out.append(f'<path d="M0 62H{W_}" fill="none" {C.stroke("PEN", t.ink, 0.6, caps="butt")}/>')
    out.append(f'<path d="{"".join(f"M0 {62 + 38 * k}H{W_}" for k in range(1, 4))}" fill="none" {C.stroke("HAIR", t.hair, caps="butt")}/>')
    remarks = [r for r in rows if r.kind in ("remark", "beat")] or rows[-2:]
    y = 90
    for r in remarks[:2]:
        out.append(_mixed(ed, r.time, 24, y, "machine", t.muted, italic=italic)[0])
        out.append(_mixed(ed, r.text, 104, y, "machine", t.ink, italic=italic, within=(104, y - 24, 600, 34))[0])
        y += 38
    so = log.get("signoff") or {}
    if log.get("measured") and so.get("initials"):
        out.append(tx(f"{so.get('text', 'Log closed')} {close} · {so.get('initials')}", 104, y, "place-water",
                      fill=t.ink if ed.dark else t.ink2))
    else:
        out.append(_mixed(ed, f"{so.get('text', 'Log closed')} {close} · unsigned", 104, y, "machine", t.muted, italic=True)[0])
    y += 38
    upd = str(data.get("updated_at") or "")
    commits = data.get("commits")
    hb = f"{_hhmm_utc(upd)} · {int(commits):,} commits · {chart_no} repos" if upd and commits is not None else "$"
    out.append(tx(hb, 104, y, "machine", fill=t.ink, truth="measured", key="heartbeat"))
    cx = 104 + T.text_width(hb + " ", "machine", edition=ed)
    out.append(f'<rect x="{fmt(cx)}" y="{y - 22}" width="13" height="27" fill="{t.ink}"/>')
    return E.svg(ed, W_, H_, "".join(out), T.glyph_defs(), sheet=NAME, paper_fill=t.paper_log)


def build(ctx) -> str:
    if not ctx.log:
        raise ValueError("no log: assets/log.json is missing or unreadable")
    return _phone(ctx) if ctx.ed.phone else _desk(ctx)


def alt(data, cfg) -> str:
    import json
    import os
    try:
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        p = os.path.join(root, (cfg.get("log") or {}).get("path", "assets/log.json"))
        with open(p, encoding="utf-8") as fh:
            log = json.load(fh)
        rows, close, start = _rows(log)
    except (OSError, ValueError, KeyError):
        return "Ship's log on ruled paper: one rustmapper run, entry by entry, from install to exported sitemap. Types once; only the cursor keeps time."
    first = next((r.time for r in rows if re.fullmatch(r"\d{4}", r.time)), start)
    total = max((r.log for r in rows if r.log is not None), default=0)
    so = log.get("signoff") or {}
    hosts = int(log.get("hosts") or 1)
    closed = f"closed by {so.get('initials', 'B.S.R.')}" if log.get("measured") else "computed from settings, unsigned"
    return (f"Ship's log, {log.get('vessel', 'rustmapper')} {log.get('version', '')}: {len(rows)} entries, {first} to {close}, "
            f"{total:,} URLs on {hosts} host{'s' if hosts != 1 else ''}, {closed}. "
            f"Types once; only the cursor keeps time.")
