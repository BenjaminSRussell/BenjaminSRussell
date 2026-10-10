"""tokens.py — the single source of truth for colour, line, dash, type scale and roles.

Every other module imports from here; DESIGN.md's tables are generated from here
(`python3 scripts/tokens.py --md`). Values come from the workshop: colour from
panel 15 (OKLCH-designed, nothing semantic derived by alpha), line weights from T6
(≥1.6× apart), type scale and roles from T5, floors from MASTERPLAN decision 6.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import sys


@dataclass(frozen=True)
class Theme:
    edition: str        # "day" | "night"
    paper: str          # the sheet
    paper_log: str      # the ship's log paper (warmer / darker)
    land: str           # islands and coast fill
    ink: str            # type and primary strokes
    ink2: str           # secondary type and lines
    muted: str          # captions (Lc >= 75 at 11px)
    shallow_a: str      # water under 10 (opaque result colour)
    shallow_b: str      # water under 5 (opaque result colour, deeper tint)
    accent: str         # red lateral marks (vermilion); never lights
    ok: str             # green lateral marks; deliberately darker than red by day
    flare: str          # chart magenta: every light's flare and halo
    light_core: str     # the flashing core of a light (white light)
    hair: str           # hairline rules, sheet edge
    unsurveyed: str     # hatch ink for the unsurveyed band


THEMES: dict[str, Theme] = {
    "day": Theme(
        edition="day",
        paper="#F4EEE1", paper_log="#F8EEDB", land="#E9DFCA",
        ink="#1B2A41", ink2="#34465F", muted="#56657B",
        shallow_a="#D8E7F1", shallow_b="#BEDAEC",
        accent="#D73626", ok="#227A48", flare="#C81392", light_core="#F8F5EE",
        hair="#CDC3AE", unsurveyed="#34465F",
    ),
    "night": Theme(
        edition="night",
        paper="#0F1A2B", paper_log="#121C30", land="#263040",
        ink="#BBC5D1", ink2="#98A7BF", muted="#8894A6",
        shallow_a="#12325A", shallow_b="#1A4470",   # D6 asked #13304F; #12325A is the nearest that keeps ΔE_ok ≥ .04 from the land
        accent="#FF6853", ok="#45E499", flare="#FF5ACD", light_core="#F8F5EE",
        hair="#2A3A55", unsurveyed="#8894A6",
    ),
}

# Line weights (px in 1280-space), each >= 1.6x the previous. `stroke()` in chartlib is the only emitter.
# v9.1: weights carry the DISPLAY factor (a 1280 sheet is shown at ~870 px in the README column, x0.68):
# HAIR 0.8 prints at 0.55 px, PEN at 0.9 px.
W = {"HAIR": 0.8, "PEN": 1.3, "LINE": 2.1, "BRUSH": 3.4}
# v10 (round 4, D6): night is redrawn, not swapped — light-on-dark reads thinner, so every weight is ×1.2 at
# night. chartlib.stroke() applies the factor when a sheet calls chartlib.set_night(True) for its night build.
NIGHT_WEIGHT = 1.2
W_NIGHT = {k: round(v * NIGHT_WEIGHT, 2) for k, v in W.items()}
# Opacity levels for ink (T6 / 15): five levels, named.
INK = {"full": 1.0, "strong": 0.85, "mid": 0.62, "soft": 0.45, "faint": 0.25}
# Dash patterns; {g} is the danger-line gap chosen per feature circumference by chartlib.
DASH = {"DANGER": "0.1 {g}", "COURSE": "0.1 7", "TRACK": "1 5", "PECK": "4 4",
        "LIMIT": "1.5 4", "APPROX": "3 3", "RESTRICT": "6 3"}

# Type scale (sheet space). Any size off the scale fails check_type.
# v9.1 (decision 6 revised): GitHub shows a 1280 sheet at ~870 px (DISPLAY 0.68), so the desk scale is
# T5's scale divided by that factor: the floors below are the old display floors (11 / 13 / 17) made to
# hold on the page, not on the sheet. The phone scale (720 shown at ~360) already carried its factor.
DISPLAY = 0.68
SCALE = (16, 19, 25, 32, 41, 53, 68, 88, 141, 176)
SCALE_PHONE = (18, 26, 30, 40, 132)
FLOORS = {"desk": {"semantic": 19, "texture": 16, "serif": 25},
          "phone": {"semantic": 26, "texture": 18, "serif": 30}}
FLOORS["mid"] = FLOORS["desk"]   # review round 12: the mid edition keeps the desk's sizes, so the desk's floors

# Roles: role -> (font key, size, tracking px, case, grade)
#   fonts: serif, serif-italic, cond, cond-italic, cond-light, plex, plex-light, plex-medium
#   case: "mixed" | "caps" | "figures" | "typed"; grade: "spread" (day stroke .22) | "choke" (night .18) | "none"
_DESK = {
    "display":     ("serif", 176, -3.0, "mixed", "none"),
    "figure":      ("serif", 141, -2.0, "figures", "none"),
    "figure-2":    ("serif", 68, -1.0, "figures", "none"),
    "thesis":      ("serif-italic", 41, -0.2, "mixed", "none"),
    "title":       ("serif", 41, -1.0, "mixed", "grade"),
    "project":     ("serif", 41, -1.0, "mixed", "none"),             # round 6: the project's name on the hero
    "sea-name":    ("serif-italic", 41, 0.0, "mixed", "grade"),      # v10 (D7): italics untracked
    "place-water": ("serif-italic", 25, 0.0, "mixed", "grade"),
    "place-land":  ("serif", 25, 0.0, "mixed", "grade"),
    "note":        ("serif-italic", 25, 0.0, "mixed", "grade"),
    "label":       ("cond", 19, 0.0, "mixed", "none"),
    "label-italic": ("cond-italic", 19, 0.0, "mixed", "none"),
    "label-caps":  ("cond", 19, 1.6, "caps", "none"),                # v10 (D7): chart caps are spaced
    "texture":     ("cond", 16, 0.0, "figures", "none"),
    "texture-italic": ("cond-italic", 16, 0.0, "figures", "none"),
    "machine":     ("plex", 19, 0.0, "typed", "none"),
    "machine-strong": ("plex-medium", 19, 0.0, "typed", "none"),
    "contour-figure": ("cond", 16, 0.0, "figures", "none"),
}
_PHONE = {
    "display":     ("serif", 132, -2.0, "mixed", "none"),
    "thesis":      ("serif-italic", 40, -0.2, "mixed", "none"),
    "title":       ("serif", 30, -0.5, "mixed", "grade"),
    "project":     ("serif", 40, -0.5, "mixed", "none"),             # round 6: the project's name on the hero
    "place-land":  ("serif", 30, 0.0, "mixed", "grade"),
    "place-water": ("serif-italic", 30, 0.0, "mixed", "grade"),
    "label":       ("cond", 26, 0.0, "mixed", "none"),
    "label-italic": ("cond-italic", 26, 0.0, "mixed", "none"),
    "label-caps":  ("cond", 26, 1.0, "caps", "none"),
    "texture":     ("cond", 18, 0.0, "figures", "none"),
    "texture-italic": ("cond-italic", 18, 0.0, "figures", "none"),
    "machine":     ("plex", 26, 0.0, "typed", "none"),
    "machine-strong": ("plex-medium", 26, 0.0, "typed", "none"),
    "figure":      ("serif", 132, -2.0, "figures", "none"),
}
# Night swaps the sans/mono roles to the Light cuts (T5): applied by the type engine, not duplicated here.
NIGHT_LIGHT_CUTS = {"cond": "cond-light", "plex": "plex-light"}
# Review round 12: the hero's mid edition (820 wide, shown at 482 to 765 px) sets the desk's roles at the desk's
# sizes: 19 units there are 11.2 px at 482 and 17.7 px at 765, against 11.4 to 12.6 px for the desk sheet itself.
_MID = dict(_DESK)
ROLES = {"desk": _DESK, "phone": _PHONE, "mid": _MID}
GRADE = {"day": ("spread", 0.22), "night": ("choke", 0.18)}

# Motion tokens (T4): easings, loop periods, the discrete grid.
EASE = {"settle": "0.16 0.84 0.44 1", "draw": "0.4 0 0.2 1", "sea": "0.37 0 0.63 1", "linear": "0 0 1 1"}
LOOP_PERIODS = (1, 4, 10, 15, 30, 96)   # 30: the Scrapy light, claims.scrape_interval (scrapy_app job, round 5 F2)
QUANTUM = 0.5
PAGE_PERIOD = 96.0

# Budgets (MASTERPLAN 7.3)
BUDGETS = {"svg_kb": 300, "gz_kb": 100, "elements": 3000, "phone_svg_kb": 120, "page_gz_kb": 250,
           "targets_kb": {"hero": (170, 60), "approaches": (245, 75), "soundings": (80, 25),
                          "log": (95, 30), "instruments": (50, 18), "footer": (75, 25)}}


# ---------------------------------------------------------------- DESIGN.md
# Review round 12 (the copy editor): DESIGN.md is the page the data line's "drawing" link opens, so it describes the
# picture on the profile in plain words and lists only what that picture draws with. Its opening paragraph is written
# from the drawn route (`sheets/route.py` `plan`, which follows `routes.rustmapper` in stats.json), so a reworded row
# cannot leave it stale; checks/design.py (DESIGN-FRESH) fails when the committed file differs from this output.

HERO_TOKENS = {"paper": "the sheet",
               "ink": "the words and the rings",
               "ink2": "the line that names the project reading the file",
               "muted": "the release and its date",
               "flare": "the track to follow, the loop, the start and end bars, the arrow",
               "accent": "the dotted line round the 0.1.3 catch"}
HERO_WEIGHTS = {"PEN": "the rings", "LINE": "the loop and the arrow", "BRUSH": "the track and the dotted line"}
HERO_ROLES = {"display": "his name", "label": "every row's words, and the role line in capitals",
              "project": "the project's name", "machine": "commands, file names and field names"}
IDEA_MAX_WORDS = 120


def _first_clause(text: str) -> str:
    return str(text).split(";")[0].strip()


def idea(stats: dict, cfg: dict) -> str:
    """The opening paragraph, from the drawn route: what each row is, and what decides that it is drawn."""
    from sheets import route as sheet
    p = sheet.plan(stats, cfg)
    ed = stats.get("edition") or {}
    v = str(ed.get("version") or "the release")
    head = str(((stats.get("routes") or {}).get(sheet.PROJECT) or {}).get("head_sha") or "")[:7]
    stops = [e for e in p["steps"] if e["kind"] == "stop"]
    trap = next((e for e in p["steps"] if e["kind"] == "trap"), None)
    step = next((e for e in p["steps"] if e["kind"] == "step"), None)
    lead = f"The picture shows how to run {p['project']} {v}, top to bottom"
    out = [lead + (f", along the magenta line from `{p['install']}`." if p["install"] else ".")]
    if stops:
        out.append("Its rings are the tool's steps: " + "; ".join(f"“{_first_clause(e['text'])}”" for e in stops) + ".")
    if any(e.get("loop") for e in p["steps"]):
        out.append("The line up the left side marks the rows that repeat for every page.")
    if trap:
        out.append(f"The dotted line marks the catch: “{_first_clause(trap['text'])}”.")
    if step:
        out.append(f"Then your step: “{_first_clause(step['text'])}”.")
    end = p.get("end")
    if end:
        out.append(f"It ends at `{end['file']}`" + (f", “{sheet.handoff_words(p['handoff'], stats)}”."
                                                   if p.get("handoff") else "."))
    out.append(f"A row is drawn only when its anchors hold at `{head}` and in the {v} sdist; the install "
               "and stop rows only when the run check passed.")
    return " ".join(out)


def markdown_tables() -> str:
    """The hero's tokens, weights and roles, with what each draws; generated so the page cannot drift."""
    from sheets import route as sheet
    out = ["Only what the picture on the profile draws with. Other tokens in `scripts/tokens.py` serve sheets not on "
           "the profile.", "", "| Token | Day | Night | Use |", "|---|---|---|---|"]
    d, n = asdict(THEMES["day"]), asdict(THEMES["night"])
    for key, use in HERO_TOKENS.items():
        out.append(f"| {key} | `{d[key]}` | `{n[key]}` | {use} |")
    out += ["", "| Weight | Day px | Night px | Use |", "|---|---|---|---|"]
    out += [f"| {k} | {W[k]} | {W_NIGHT[k]} | {use} |" for k, use in HERO_WEIGHTS.items()]
    out += ["", f"The dotted line is `DANGER` (`{DASH['DANGER']}`), its gap chosen so the dots space evenly round it.",
            "", "| Role | Font | Desk | Mid | Phone | Use |", "|---|---|---|---|---|---|"]
    for r, use in HERO_ROLES.items():
        sizes = []
        for sc in ("desk", "mid", "phone"):
            sizes.append(sheet.L[sc]["name_size"] if r == "display" else ROLES[sc][r][1])
        out.append(f"| {r} | {_DESK[r][0]} | {sizes[0]} | {sizes[1]} | {sizes[2]} | {use} |")
    out += ["", f"Floors (sheet units): desk and mid {FLOORS['desk']['semantic']}, phone {FLOORS['phone']['semantic']}."]
    return "\n".join(out)


DESIGN_HEAD = """<!-- Generated by `python3 scripts/tokens.py --md > DESIGN.md` from scripts/tokens.py, chart.toml and
assets/stats.json; edit those, not this file. check.py fails (DESIGN-FRESH) when this file and that output differ. -->

# How the picture is drawn

{idea}

The run check (`scripts/runcheck.py`) installs the release, crawls a local three-page site with `--seeding-strategy
none`, presses Ctrl-C once and exports the sitemap; its probes check each caution the README prints. What each
element is for is in `scripts/sheets/route.py` (`PURPOSE`); `check.py` fails while any row does not hold.

## Editions

The picture ships six editions: `day` and `night` for a laptop, `mid-day` and `mid-night` for an iPad held sideways
or a laptop window under 1,200 px, `phone-day` and `phone-night`. Nothing on it moves, so there are no still
editions. Night is redrawn, not inverted: strokes 20 % heavier and the thinner cuts of the sans and the mono. The mid
and phone editions are redrawn at their own width, not shrunk: the title on top, the route under it, the same rows in
the same order.

GitHub's README column, measured on the live profile page on 10 Oct 2026 (Playwright Chromium, iOS Safari user agent):
under a 768 px viewport it is the viewport less 82 px (278 at 360, 308 at 390); from 768 to 1011 the viewport less
370; from 1012 to 1279 the viewport less 434; from 1280 on, 846. The README serves the phone sheet (600 wide) up to
{pmax} px, the mid sheet (820 wide) from {mid} to {bp} px (`chart.toml` `mid_from_px`, `breakpoint_px`) and the desk
sheet (1280 wide) from {desk}. Above {pmax} px the phone sheet would be drawn over {tall} px tall; at {mid} the mid
sheet's 19-unit text is {mid_px} px, and at {desk} the desk sheet's is {desk_px} px. `checks/column.py`
(HERO-COLUMN-PX) holds every viewport from 360 to 1920 px to 11 px text and, from 768, to a picture at most {tall} px
tall; `checks/route.py` holds the phone sheet's text to 13 px at 308 and 11 px at 278, and the heights to desk
{h_desk}, mid {h_mid} and phone {h_phone} units. Re-measure when GitHub changes the profile layout; the table is in
`checks/column.py`. The sheets are published to the `chart` branch under `assets/v9/`.

## Actions playbook

| Workflow | File | Purpose |
|---|---|---|
| `chart` | `.github/workflows/profile.yml` | weekly (Sunday 06:20 UTC) and on push to `main`: the run check on macos-14 (`runcheck.py`), the data step (`build_stats.py --runcheck`), build, render, `check.py --tier fast,render`, commit the figures, README.md and DESIGN.md, publish the `chart` branch |
| `perf` | `.github/workflows/perf.yml` | repaint budgets on `scripts/**` pushes and Sundays |
| README links | `.github/workflows/links.yml` | lychee over README.md weekly and on pull requests |

When a sheet is stale or missing: open **Actions**, then `chart`, then **Run workflow**. A red run never publishes;
the previous `chart` branch stays up and the README keeps showing it. If the data step fails (GraphQL quota, a clone
timing out), the run falls back to the cached figures and publishes the edition drawn from them; it does not invent
numbers. Do not hammer re-runs: the data step clones every public repository.

## Tokens
"""


def _load(stats: dict | None, cfg: dict | None) -> tuple[dict, dict]:
    import json
    import os
    import tomllib
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    if stats is None:
        with open(os.path.join(root, "assets", "stats.json"), encoding="utf-8") as fh:
            stats = json.load(fh)
    if cfg is None:
        with open(os.path.join(root, "chart.toml"), "rb") as fh:
            cfg = tomllib.load(fh)
    return stats, cfg


def design_md(stats: dict | None = None, cfg: dict | None = None) -> str:
    """DESIGN.md, from the committed stats.json and chart.toml unless given."""
    stats, cfg = _load(stats, cfg)
    from checks import route as route_check
    from checks import column
    ch = cfg.get("chart") or {}
    bp = int(ch.get("breakpoint_px", 1199))
    mid = int(ch.get("mid_from_px") or bp + 1)
    head = DESIGN_HEAD.format(
        idea=idea(stats, cfg), pmax=mid - 1, mid=mid, bp=bp, desk=bp + 1, tall=f"{column.TALL_PX:g}",
        mid_px=f"{FLOORS['mid']['semantic'] * column.column_px(mid) / 820:.1f}",
        desk_px=f"{FLOORS['desk']['semantic'] * column.column_px(bp + 1) / 1280:.1f}",
        h_desk=route_check.HEIGHT["desk"], h_mid=route_check.HEIGHT["mid"], h_phone=f"{route_check.HEIGHT['phone']:,}")
    return head + "\n" + markdown_tables()


if __name__ == "__main__":
    if "--md" in sys.argv:
        print(design_md())
    else:
        print(f"{len(THEMES)} themes, {len(W)} weights, {len(_DESK)} desk roles, {len(_PHONE)} phone roles")
