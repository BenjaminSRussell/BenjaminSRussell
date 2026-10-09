"""symbols.py — the symbol library (T6 §2.6, 31's drawings).

One pen for every symbol (PEN, round caps), one pictorial object (the sloop). Symbols are drawn
once in <defs> as <g id="{prefix}-sym-{name}"> and placed with use(); legend cells call the same
use(), so the build can diff legend ids against sheet ids. Every lit symbol has one child with
id="{prefix}-{name}-lit" whose opacity T4 animates discretely; the halo is a static radial-gradient
circle (no filter). Day misregisters colour fills (+0.6, +0.4) from their outlines; night does not.
Text (mark numbers, characters, doubt abbreviations) goes through label_cb.
"""
from __future__ import annotations

import math

from .field import fmt
from .furniture import stroke, op

__all__ = ["SYMBOL_NAMES", "symbol_defs", "symbol_ids", "use", "sloop", "lateral", "light", "flare", "halo",
           "traffic_signal", "horn", "anchorage", "wreck", "waypoint", "station", "fix", "ldg_triangle",
           "rep_ring", "ed_islet", "correction_mark", "correction", "doubt", "serpent", "lit_core", "tick",
           "rock", "rock_d", "SLOOP_DETAIL", "SLOOP_GLYPH"]

SYMBOL_NAMES = ("sloop", "sloop-glyph", "can", "nun", "light", "flare", "traffic", "horn", "anchorage", "wreck",
                "waypoint", "station", "fix", "ldg", "halo", "correction", "rep", "ed")

# 31's sloop: origin at the waterline centre, bow right, mast 40 % from the bow raked 2° aft.
SLOOP_DETAIL = {
    "hull": "M-17 -2L-14 4L10 4L18 -6Q0 -1 -17 -2Z",      # transom, keel, raked stem, sheer
    "main": "M3 -39Q-9 -24 -15 -7L3.5 -7Z",                # aft of the mast, roach on the leech
    "jib": "M2.5 -34L17.5 -6L5 -8Z",                        # on the forestay, paper with an ink outline
    "mast": "M4 -3L2.5 -40",
    "tiller": "M-17 -2L-21 -4",
}
SLOOP_GLYPH = {
    "hull": "M-8 -1L-6 3L5 3L9 -3Z",
    "main": "M2 -3L1 -20L-7 -4Z",
    "jib": "M1 -17L8 -4L2 -4Z",
}
MISREG = (0.6, 0.4)


def _g(prefix: str, name: str, inner: str) -> str:
    return f'<g id="{prefix}-sym-{name}">{inner}</g>'


def symbol_ids(prefix: str) -> list[str]:
    return [f"{prefix}-sym-{n}" for n in SYMBOL_NAMES]


def use(name: str, x, y, prefix: str, scale: float = 1.0, rotate: float = 0, extra: str = "") -> str:
    """<use> of the sheet's symbol `name` at (x, y); scale/rotate about the symbol origin."""
    href = f'href="#{prefix}-sym-{name}"'
    ex = f" {extra}" if extra else ""
    if scale == 1.0 and rotate == 0:
        return f'<use {href} x="{fmt(x)}" y="{fmt(y)}"{ex}/>'
    t = f"translate({fmt(x)} {fmt(y)})"
    if rotate:
        t += f" rotate({fmt(rotate)})"
    if scale != 1.0:
        t += f" scale({fmt(scale)})"
    return f'<use {href} transform="{t}"{ex}/>'


# ------------------------------------------------------------------ the boat
def sloop(theme, detail: bool = True, rig: bool = True) -> str:
    """31's eleven-command sloop (detail) or seven-command glyph. Hull ink, main accent, jib paper
    with an ink outline; detail adds the PEN mast and tiller and a 1.2 px position dot at the
    waterline so the symbol sits on its fix. Choose detail where rendered width ≥ 28 px."""
    if detail:
        P = SLOOP_DETAIL
        out = [f'<path d="{P["hull"]}" fill="{theme.ink}"/>',
               f'<path d="{P["main"]}" fill="{theme.accent}"/>',
               f'<path d="{P["jib"]}" fill="{theme.paper}" {stroke("PEN", theme.ink)}/>']
        if rig:
            out.append(f'<path d="{P["mast"]}{P["tiller"]}" fill="none" {stroke("PEN", theme.ink)}/>')
        out.append(f'<circle r="1.2" fill="{theme.ink}"/>')
        return "".join(out)
    P = SLOOP_GLYPH
    return (f'<path d="{P["hull"]}" fill="{theme.ink}"/>'
            f'<path d="{P["main"]}" fill="{theme.accent}"/>'
            f'<path d="{P["jib"]}" fill="none" {stroke("PEN", theme.ink)}/>')


# ------------------------------------------------------------------ marks
def lateral(kind: str, number=None, theme=None, misreg: bool = True) -> str:
    """Region B lateral mark: 'can' (green, 11×13) or 'nun' (red cone, base 12). Outline PEN ink,
    IALA fill .85 (misregistered by day), body canted rotate(8) about the base, position circle
    r 1.2 at the waterline, no underline. `number` is lettered by the caller (label_cb)."""
    if kind == "can":
        d, col = "M-5.5 0v-13h11v13z", theme.ok
    elif kind == "nun":
        d, col = "M-6 0L6 0L0 -14Z", theme.accent
    else:
        raise ValueError(kind)
    mx, my = MISREG if misreg else (0, 0)
    fill = (f'<path d="{d}" fill="{col}" fill-opacity=".85"'
            + (f' transform="translate({fmt(mx)} {fmt(my)})"' if misreg else "") + "/>")
    return (f'<g transform="rotate(8)">{fill}<path d="{d}" fill="none" {stroke("PEN", theme.ink)}/></g>'
            f'<circle r="1.2" fill="{theme.paper}" {stroke("PEN", theme.ink)}/>')


def _star(r_out: float, r_in: float, points: int = 5) -> str:
    d = []
    for i in range(points * 2):
        a = math.radians(i * 180 / points - 90)
        rr = r_out if i % 2 == 0 else r_in
        d.append(("M" if i == 0 else "L") + f"{fmt(rr * math.cos(a))} {fmt(rr * math.sin(a))}")
    return "".join(d) + "Z"


FLARE_D = "M0 0q-3 -9 0 -14q3 5 0 14"


def flare(theme, opacity: float = 0.8) -> str:
    """The magenta flare petal, rotated 45° (NE), on every light."""
    return f'<path d="{FLARE_D}" transform="rotate(45)" fill="{theme.flare}" fill-opacity="{op(opacity)}"/>'


def light(theme, prefix: str = "sym", core_r: float = 1.5) -> str:
    """A light: 5-point star r 4 PEN ink + flare + the flashing core (id {prefix}-light-lit) in
    light_core, ringed in ink by day so it reads on paper."""
    core_stroke = stroke("PEN", theme.ink) if theme.edition == "day" else ""
    return (flare(theme)
            + f'<path d="{_star(4, 1.7)}" fill="none" {stroke("PEN", theme.ink)}/>'
            + f'<circle id="{prefix}-light-lit" r="{fmt(core_r)}" fill="{theme.light_core}" {core_stroke}/>')


def halo(theme, prefix: str = "sym", r: float = 14, color: str | None = None) -> tuple[str, str]:
    """(gradient def, circle). Static radial-gradient halo in `flare`; its opacity is T4's."""
    col = color or theme.flare
    gid = f"{prefix}-halo-g"
    grad = (f'<radialGradient id="{gid}"><stop offset="0" stop-color="{col}" stop-opacity=".95"/>'
            f'<stop offset=".45" stop-color="{col}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')
    return grad, f'<circle id="{prefix}-halo-lit" r="{fmt(r)}" fill="url(#{gid})"/>'


def lit_core(x, y, theme, lit_id: str, r: float = 1.5, halo_r: float | None = None, prefix: str = "sym",
             color: str | None = None) -> str:
    """A positioned flashing core with its own id (per-instance timing for T4), optionally with a
    halo circle (id lit_id + '-halo') using the sheet's halo gradient from symbol_defs()."""
    out = []
    if halo_r:
        out.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(halo_r)}" fill="url(#{prefix}-halo-g)" id="{lit_id}-halo"/>')
    col = color or theme.light_core
    ring = stroke("PEN", theme.ink) if theme.edition == "day" else ""
    out.append(f'<circle id="{lit_id}" cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="{col}" {ring}/>')
    return "".join(out)


def traffic_signal(theme, prefix: str = "sym") -> str:
    """Port traffic signal: a mast with three stacked lamps (paper, PEN outline); the top lamp
    carries id {prefix}-traffic-lit."""
    lamps = []
    for i, cy in enumerate((-16, -10.5, -5)):
        lid = f' id="{prefix}-traffic-lit"' if i == 0 else ""
        lamps.append(f'<circle cx="0" cy="{fmt(cy)}" r="2.2"{lid} fill="{theme.paper}" {stroke("PEN", theme.ink)}/>')
    return f'<path d="M0 0V-19M-3 0h6" fill="none" {stroke("PEN", theme.ink)}/>' + "".join(lamps)


def horn(theme) -> str:
    """Fog signal: three HAIR arcs radiating from the light, to the east."""
    d = []
    for r in (6, 9.5, 13):
        a0, a1 = math.radians(-35), math.radians(35)
        d.append(f"M{fmt(r * math.cos(a0))} {fmt(r * math.sin(a0))}A{r} {r} 0 0 1 {fmt(r * math.cos(a1))} {fmt(r * math.sin(a1))}")
    return f'<path d="{"".join(d)}" fill="none" {stroke("HAIR", theme.ink, 0.6, caps="butt")}/>'


def anchorage(theme) -> str:
    """The reference anchor (31): open line, one weight."""
    return (f'<circle cx="0" cy="-9" r="2.4" fill="none" {stroke("PEN", theme.ink)}/>'
            f'<path d="M0 -6.5V9M-6 -1H6M-8 4Q-8 10 0 10Q8 10 8 4" fill="none" {stroke("PEN", theme.ink)}/>')


def wreck(theme) -> str:
    """The reference drawing (31): S-4 hull and mast, PEN round caps, nothing filled, in a dotted
    position ring r 11."""
    return (f'<path d="M-9 2Q0 7 9 2M-9 2L-6 -3L6 -3L9 2M0 -3V-11M-4 -8H4" fill="none" {stroke("PEN", theme.ink)}/>'
            f'<circle r="11" fill="none" {stroke("PEN", theme.ink, 0.7, "DANGER", gap=3.4)}/>')


def waypoint(theme) -> str:
    return (f'<circle r="4" fill="none" {stroke("PEN", theme.ink)}/>'
            f'<circle r="1.2" fill="{theme.ink}"/>')


def station(theme) -> str:
    """△ survey station with its centre dot."""
    return (f'<path d="M0 -6L5.5 3.5L-5.5 3.5Z" fill="none" {stroke("PEN", theme.ink)}/>'
            f'<circle cy="0.5" r="1" fill="{theme.ink}"/>')


def tick(theme) -> str:
    """A gutter tick for a chart's own lists (v9.2, sheet 5): one short PEN dash, no charted meaning, so
    it is not in SYMBOL_NAMES and the legend never has to define it. A sheet puts it in its own <defs>
    as <g id="{prefix}-sym-tick"> and places it with use()."""
    return f'<path d="M-3.5 0H3.5" fill="none" {stroke("PEN", theme.ink, 0.85)}/>'


ROCK_ARM = 4.5        # half-length of the cross
ROCK_DOT = 3.0        # the four dots sit at (±ROCK_DOT, ±ROCK_DOT): a rock awash, chart grammar


def rock_d(x, y) -> str:
    """Path data for one rock mark at (x, y): a cross with a dot in each quadrant (the chart's rock awash),
    for a round-capped PEN stroke — the dots are zero-length segments the caps round into points. The hero
    draws every rock of its fringe as one <path> of these (v10, D3)."""
    a, d = ROCK_ARM, ROCK_DOT
    return (f"M{fmt(x - a)} {fmt(y)}H{fmt(x + a)}M{fmt(x)} {fmt(y - a)}V{fmt(y + a)}"
            + "".join(f"M{fmt(x + sx * d)} {fmt(y + sy * d)}h0" for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1))))


def rock(theme) -> str:
    """The rock mark as a symbol body (origin at the rock). Like tick(), it is not in SYMBOL_NAMES: a sheet
    that places it with use() puts it in its own <defs> as <g id="{prefix}-sym-rock">."""
    return f'<path d="{rock_d(0, 0)}" fill="none" {stroke("PEN", theme.ink)}/>'


def fix(theme) -> str:
    """A plotted fix: small circle with crossed PEN ticks."""
    return (f'<circle r="2.5" fill="none" {stroke("PEN", theme.ink)}/>'
            f'<path d="M-5 0h10M0 -5v10" fill="none" {stroke("PEN", theme.ink)}/>')


def ldg_triangle(theme) -> str:
    """One leading-line triangle (the caller places front and rear)."""
    return f'<path d="M0 -7L4 1L-4 1Z" fill="{theme.ink}"/>'


def rep_ring(theme) -> str:
    """Rep: reported, not found — a dotted ring r 7."""
    return f'<circle r="7" fill="none" {stroke("PEN", theme.ink, 0.9, "DANGER", gap=3.2)}/>'


def ed_islet(theme) -> str:
    """ED: existence doubtful — a dotted islet r 4 in land colour."""
    return f'<circle r="4" fill="{theme.land}" {stroke("PEN", theme.ink, 0.9, "DANGER", gap=2.6)}/>'


def correction_mark(theme) -> str:
    """The manuscript strike: one PEN diagonal in chart magenta."""
    return f'<path d="M-5 5L5 -5" fill="none" {stroke("PEN", theme.flare, 0.85)}/>'


# ------------------------------------------------------------------ positioned, lettered things
def correction(x, y, old: str, new: str, theme, label_cb, old_w: float | None = None, size: float = 11) -> str:
    """A data-driven manuscript correction (14 idea 1): `old` set upright in ink, struck through
    with one PEN diagonal in `flare`, `new` set italic in `flare` just right of it. old_w is the
    measured width of `old` (defaults to 0.5·size per glyph)."""
    w = old_w if old_w is not None else 0.5 * size * len(old)
    out = [label_cb(old, x, y, "texture", anchor="start"),
           f'<path d="M{fmt(x - 1)} {fmt(y + 2)}L{fmt(x + w + 1)} {fmt(y - size * 0.75)}" fill="none" '
           f'{stroke("PEN", theme.flare, 0.85)}/>',
           label_cb(new, x + w + 4, y, "texture-italic", anchor="start", fill=theme.flare)]
    return "".join(out)


def doubt(kind: str, x, y, label_cb=None, prefix: str | None = None, theme=None) -> str:
    """The chart's doubt marks (26): ED (dotted islet), Rep (dotted ring), SD and PA (letters only),
    the abbreviation 8 px right in italic via label_cb."""
    out = []
    if kind == "ED":
        out.append(use("ed", x, y, prefix) if prefix else f'<g transform="translate({fmt(x)} {fmt(y)})">{ed_islet(theme)}</g>')
        dx = 4 + 8
    elif kind == "Rep":
        out.append(use("rep", x, y, prefix) if prefix else f'<g transform="translate({fmt(x)} {fmt(y)})">{rep_ring(theme)}</g>')
        dx = 7 + 8
    elif kind in ("SD", "PA"):
        dx = 0
    else:
        raise ValueError(kind)
    if label_cb:
        out.append(label_cb(kind, x + dx, y + 4, "label-italic", anchor="start"))
    return "".join(out)


def serpent(theme) -> str:
    """31's creature: three strokes and a dot, humps growing toward a head facing +x, tapering
    head-first through the weights (BRUSH head, LINE, PEN tail); one eye, no mouth. Parts carry
    classes hump-1 / hump-2 / head so T4 can stagger them (+0.25 / +0.5 s)."""
    eye = theme.accent if theme.edition == "night" else theme.ink
    return (f'<g class="serpent" fill="none">'
            f'<path class="hump-1" d="M-96 0c8 -10 18 -10 26 0" {stroke("PEN", theme.ink)}/>'
            f'<path class="hump-2" d="M-58 0c10 -20 28 -20 40 0" {stroke("LINE", theme.ink)}/>'
            f'<path class="head" d="M-6 0c8 -30 22 -40 34 -34q6 3 8 10" {stroke("BRUSH", theme.ink)}/>'
            f'<circle class="eye" cx="24" cy="-32" r="1.3" fill="{eye}"/></g>')


# ------------------------------------------------------------------ the defs
def symbol_defs(theme, prefix: str, edition: str) -> str:
    """Every symbol as <g id="{prefix}-sym-{name}"> plus the halo gradient. Day editions misregister
    colour fills; night (and any edition containing 'night') does not. The caller puts this inside
    its <defs>."""
    misreg = "night" not in edition and theme.edition == "day"
    grad, halo_circle = halo(theme, prefix)
    parts = [
        grad,
        _g(prefix, "sloop", sloop(theme, True)),
        _g(prefix, "sloop-glyph", sloop(theme, False)),
        _g(prefix, "can", lateral("can", None, theme, misreg)),
        _g(prefix, "nun", lateral("nun", None, theme, misreg)),
        _g(prefix, "light", light(theme, prefix)),
        _g(prefix, "flare", flare(theme)),
        _g(prefix, "traffic", traffic_signal(theme, prefix)),
        _g(prefix, "horn", horn(theme)),
        _g(prefix, "anchorage", anchorage(theme)),
        _g(prefix, "wreck", wreck(theme)),
        _g(prefix, "waypoint", waypoint(theme)),
        _g(prefix, "station", station(theme)),
        _g(prefix, "fix", fix(theme)),
        _g(prefix, "ldg", ldg_triangle(theme)),
        _g(prefix, "halo", halo_circle),
        _g(prefix, "correction", correction_mark(theme)),
        _g(prefix, "rep", rep_ring(theme)),
        _g(prefix, "ed", ed_islet(theme)),
    ]
    return "".join(parts)
