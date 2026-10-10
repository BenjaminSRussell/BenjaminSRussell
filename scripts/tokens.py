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
ROLES = {"desk": _DESK, "phone": _PHONE}
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


def markdown_tables() -> str:
    """The palette / line / type tables for DESIGN.md, generated so docs cannot drift."""
    out = ["| Token | Day | Night | Use |", "|---|---|---|---|"]
    uses = {"paper": "the sheet", "paper_log": "the ship's log paper", "land": "islands, coast",
            "ink": "type, primary strokes", "ink2": "secondary type, lines", "muted": "captions",
            "shallow_a": "water under 10", "shallow_b": "water under 5", "accent": "red lateral marks",
            "ok": "green lateral marks", "flare": "light flares and halos (chart magenta)",
            "light_core": "the flashing core of a light", "hair": "hairlines, sheet edge",
            "unsurveyed": "hatch ink for the unsurveyed band"}
    d, n = asdict(THEMES["day"]), asdict(THEMES["night"])
    for key, use in uses.items():
        out.append(f"| {key} | `{d[key]}` | `{n[key]}` | {use} |")
    out += ["", "| Weight | day px | night px |", "|---|---|---|"] + [f"| {k} | {v} | {W_NIGHT[k]} |" for k, v in W.items()]
    out += ["", "| Role | Font | Size | Tracking | Case |", "|---|---|---|---|---|"]
    for r, (f, s, t, c, _g) in _DESK.items():
        out.append(f"| {r} | {f} | {s} | {t:+.1f} | {c} |")
    out += ["", f"Scale: {' · '.join(str(s) for s in SCALE)} (phone: {' · '.join(str(s) for s in SCALE_PHONE)}). "
            f"Floors: desk {FLOORS['desk']}, phone {FLOORS['phone']}."]
    return "\n".join(out)


DESIGN_HEAD = """# DESIGN — how the chart is drawn

Generated by `python3 scripts/tokens.py --md > DESIGN.md`; edit `scripts/tokens.py`, not this file.
The authoritative plan is `docs/crit/tech/MASTERPLAN.md`; this page is the short form a reader needs
to understand what the sheets mean and what the build will refuse.

## The idea

Round 6 (docs/crit/round6/SPEC.md, reviews 1 to 5): the hero is the way into rustmapper. It answers one sentence: how
you start it, what it does with each page, where a stranger goes wrong and how to get out, and where the output goes
next. Vertical position is the order of a run: the start bar, `pip install rustmapper` with the release and its date
set right after the command, the stops on the magenta track (what happens there, every row's words at one left edge;
the track is painted first, so each ring sits on it), the governor as a line under the fetch stop's words with its
500 ms threshold, the write path (the write-ahead log, fsynced, then redb), the rows that repeat for every page closed
by one line back up the left side, the one hazard on that loop, which names its release, with its words (and the line
of output that says the crawl is done) ringed by a dotted line in the accent, the reader's one step (Ctrl-C once) on
the next row, the end bar, `data/sitemap.jsonl` with its real field names, and a thin line on to ideal-url-organizer,
which sorts that file and tests the join. While the release never stops by itself the track breaks under the loop and
starts again just above Ctrl-C, so the shape alone says the only way on is the reader's. Code inside a row's words is
set in the code face, its spaces at the text's word space. What to do after a kill is a comment in the README's code
block, where the reader types. The title block on the left is his name and what he builds. Nothing has a size that
depends on data. Each drawn element is a `<g id>` with a row in `scripts/sheets/route.py` `PURPOSE` (what a stranger
learns, which visitor question, the source).

A stop or trap is drawn only when its anchors hold in the code at HEAD and in the released sdist
(`scripts/data/route.py`): every rustmapper source file it rests on is in that release, and the reader the line past
the end points to is read at the commit `stats.json` names (`handoffs[].to_sha`). The install lines are drawn only when
the weekly run check passed (`scripts/runcheck.py`: install, then a crawl of a local three-page site with
`--seeding-strategy none`, one Ctrl-C, a kill and an export); the line past the end only when the reader's fields are
in the writer's struct. `check.py` fails while any entry does not hold.

## Honesty conventions

- **Upright numerals are measured** from the survey (`stats.json`). **Italic numerals are illustrative**
  or computed (the ship's log until a real run is recorded). An **underlined** figure is above datum.
- Doubt marks follow chart practice: `ED` existence doubtful, `Rep` reported, `SD` sounding doubtful,
  `PA` position approximate. The disputed worker count is never set upright.
- Two commit instruments are shown wherever one is: commits by the author (identity-filtered) and
  all hands. Hours are commit-days in the author's local time, not UTC.
- Nothing proposed is drawn as built: the rustmapper → Scrapy channel is pecked and unlit.
- No placeholder, disclaimer or borrowed phrase ships in artwork (`scripts/checks/strings.py`).

## Editions

The hero ships four: `day`, `night`, `phone-day`, `phone-night`; nothing on it moves, so it has no still editions and
the README's `<picture>` carries no reduced-motion sources (phone + dark, phone, dark, then the day `<img>`). The
supporting sheets, built on request, keep their six (`day`, `night`, `still-day`, `still-night`, `phone-day`,
`phone-night`). Night is designed, not inverted, at +20 % stroke weight with the Light cuts of the sans and mono. Phone
editions are redrawn at the phone scale, not shrunk, and break lines at the same words as the day edition.

GitHub shows a 1280 px sheet at about 870 px in the README column (×0.68). The desk scale carries that factor: the
floors below (19 semantic · 16 texture · 25 serif on the sheet) are 13 · 11 · 17 px as the page shows them. The phone
sheet is 720 wide, shown at 390 on an iPhone (×0.54): 26 px on the sheet is 14 px on the screen. The hero's height
follows its content (desk ≤ 640, phone ≤ 1200). Sheets are published to the orphan `chart` branch under `assets/v9/`.

## Motion

The hero does not move. The supporting sheets keep the page-wide 96 s timeline, SMIL only: only `opacity` and
`transform` animate, every discrete instant on a 0.5 s grid, loop periods from {1, 4, 10, 15, 30, 96} s; the footer is
the only ambient sheet.

## Actions playbook

| Workflow | File | Purpose |
|---|---|---|
| chart | `.github/workflows/profile.yml` | weekly (Sunday 06:20 UTC) and on push to `main`: the run check on macos-14 (`runcheck.py`) → survey (`build_stats.py --runcheck`) → build → render → `check.py --tier fast,render` → commit figures and README → publish the `chart` branch |
| perf | `.github/workflows/perf.yml` | repaint budgets on `scripts/**` pushes and Sundays |
| README links | `.github/workflows/links.yml` | lychee over README.md weekly and on pull requests |

When a sheet is stale or missing: open **Actions → chart → Run workflow**. A red run never publishes; the
previous `chart` branch stays up and the README keeps rendering it. If the survey fails (GraphQL quota, a
clone timing out), the run falls back to the cached figures and draws the pencil-note edition; it does not
invent numbers. Do not hammer re-runs: the survey clones every public repository.

## Tokens
"""


def design_md() -> str:
    return DESIGN_HEAD + "\n" + markdown_tables()


if __name__ == "__main__":
    if "--md" in sys.argv:
        print(design_md())
    else:
        print(f"{len(THEMES)} themes, {len(W)} weights, {len(_DESK)} desk roles, {len(_PHONE)} phone roles")
