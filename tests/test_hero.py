"""hero sheet (v10, round 4): contract, determinism, the area law in commit-days, the hand-set slots, the rocks,
the one printed week, honesty (nothing sloping, nothing unmeasured), the cartouche and rose, night weights, budgets,
still editions, motion budget — everything of D2–D7 that a test can read off the built SVGs and the build report."""
from __future__ import annotations

import copy
import json
import math
import os
import re
import shutil
import sys
import tempfile
import tomllib
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import build_assets  # noqa: E402
import edition as E  # noqa: E402
import tokens  # noqa: E402
from sheets import hero  # noqa: E402

STATS = os.path.join(ROOT, "assets", "stats.json")
CFG = os.path.join(ROOT, "chart.toml")
BANNED = re.compile(r"ILLUSTRATIVE|PENDING|SEEDED|NOT FOR NAVIGATION|works at night|Here be dragons|Fair winds",
                    re.I)
ANIM = re.compile(r"<(animate|animateTransform|set)\b")
ALL = tuple(E.EDITION_NAMES) + tuple(E.HERO_EXTRA)
SUBSCRIPTS = "₀₁₂₃₄₅₆₇₈₉"


def _named(stats: dict, cfg: dict, scale: str) -> dict:
    """repo -> (slot, commit_days) for the repositories the hero must name on `scale` (D3)."""
    spec = {f["repo"]: f for f in cfg["features"]}
    out = {}
    for r in stats["repos"]:
        days = int(r.get("commit_days") or 0)
        slot = spec.get(r["name"], {}).get(scale)
        if days >= hero.NAMED_MIN and slot:
            out[r["name"]] = (tuple(slot), days)
    return out


class HeroBuild(unittest.TestCase):
    """One build of every edition (plus a no-sounding set) shared by the tests below."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="hero-test-")
        cls.out = os.path.join(cls.tmp, "v9")
        cls.report_path = os.path.join(cls.tmp, "report.json")
        cls.problems = build_assets.main(sheets=["hero"], out=cls.out, report_path=cls.report_path, quiet=True)
        with open(cls.report_path, encoding="utf-8") as fh:
            cls.report = json.load(fh)
        cls.svg = {}
        for name in ALL:
            with open(os.path.join(cls.out, f"hero-{name}.svg"), encoding="utf-8") as fh:
                cls.svg[name] = fh.read()
        cls.ns_out = os.path.join(cls.tmp, "nosound")
        cls.ns_problems = build_assets.main(sheets=["hero"], editions=["still-day", "phone-still-day"], no_sounding=True,
                                            out=cls.ns_out, report_path=os.path.join(cls.tmp, "ns.json"), quiet=True)
        with open(os.path.join(cls.ns_out, "hero-still-day.svg"), encoding="utf-8") as fh:
            cls.ns_svg = fh.read()
        with open(STATS, encoding="utf-8") as fh:
            cls.stats = json.load(fh)
        with open(CFG, "rb") as fh:
            cls.cfg = tomllib.load(fh)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def entry(self, name):
        return self.report["sheets"][f"hero-{name}"]

    def texts(self, name):
        return self.entry(name)["text"]

    # ---- contract and alt
    def test_contract(self):
        self.assertEqual(hero.NAME, "hero")
        self.assertEqual(hero.KIND, "chart")
        self.assertEqual(hero.SIZES, {"desk": (1280, 740), "phone": (720, 900)})
        self.assertTrue(all(len(b) == 3 for b in hero.BREAKS))
        self.assertEqual(set(self.report["sheets"]), {f"hero-{n}" for n in ALL})
        self.assertEqual(hero.LEVELS, (0.0, 5.0, 10.0), "D4: no 20, no 50")

    def test_alt_is_short_plain_and_from_data(self):
        alt = hero.alt(self.stats, build_assets.load_cfg(CFG))
        self.assertLessEqual(len(alt.split()), 25)
        self.assertFalse(alt.startswith("The"))
        self.assertIn(str(self.stats["repo_count"]), alt)
        self.assertIn("commit-days", alt)
        self.assertTrue(alt.endswith("A boat sails in and anchors."))
        self.assertEqual(alt.split(" ")[-5:], ["A", "boat", "sails", "in", "anchors."][:0] + alt.split(" ")[-5:])
        self.assertIn("islands and rocks", self.cfg["alt"]["hero"], "chart.toml's template agrees with the module")

    # ---- the build itself
    def test_builds_clean_and_deterministic(self):
        self.assertEqual(self.problems, 0, self.report["problems"])
        self.assertEqual(self.ns_problems, 0)
        again = os.path.join(self.tmp, "again")
        self.assertEqual(build_assets.main(sheets=["hero"], editions=["day", "phone-night"], out=again,
                                           report_path=os.path.join(self.tmp, "again.json"), quiet=True), 0)
        for name in ("day", "phone-night"):
            with open(os.path.join(again, f"hero-{name}.svg"), encoding="utf-8") as fh:
                self.assertEqual(fh.read(), self.svg[name], f"hero-{name} differs between two builds")

    def test_refuses_to_invent_weeks(self):
        data = dict(self.stats)
        data["weeks"] = []
        path = os.path.join(self.tmp, "noweeks.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        n = build_assets.main(sheets=["hero"], editions=["still-day"], out=os.path.join(self.tmp, "nw"),
                              report_path=os.path.join(self.tmp, "nw.json"), stats_path=path, quiet=True)
        self.assertGreaterEqual(n, 1)

    # ---- D2: the area law in commit-days
    def test_area_law_in_commit_days(self):
        for name in ("day", "phone-day"):
            e = self.entry(name)
            self.assertEqual(e["area_law"], "area∝commit-days")
            feats = e["features"]
            self.assertTrue(feats)
            k = {}
            for f in feats:
                self.assertTrue(f["ok"], f"{name}: {f['name']} ratio {f['ratio']}")
                self.assertLessEqual(abs(f["ratio"] - 1), 0.08, f"{name}: {f['name']}")
                self.assertLessEqual(abs(f["drawn_ratio"] - 1), 0.08, f"{name}: {f['name']} drawn {f['drawn_ratio']}")
                rec = next(r for r in self.stats["repos"] if r["name"] == f["repo"])
                self.assertEqual(f["commit_days"], rec["commit_days"], "the measure is commit_days, not commits")
                k[f["name"]] = f["target_px"] / f["commit_days"]
            self.assertLess(max(k.values()) - min(k.values()), 1.0, f"one px²-per-day constant for every feature: {k}")
        big = max(self.entry("day")["features"], key=lambda f: f["commit_days"])
        self.assertEqual(big["repo"], "Scrapy")
        self.assertGreaterEqual(big["r"], 76, "Scrapy at 26 days draws at a radius around 80 px")
        self.assertLessEqual(big["r"], 90)
        self.assertAlmostEqual(self.entry("day")["hero"]["field"]["area_scale_px2_per_day"], hero.K_AREA, delta=0.5)

    # ---- D3: slots from chart.toml, the rest as rocks
    def test_slots_from_chart_toml_and_rocks(self):
        for name, scale in (("day", "desk"), ("phone-day", "phone")):
            e = self.entry(name)
            want = _named(self.stats, self.cfg, scale)
            got = {f["repo"]: (f["cx"], f["cy"]) for f in e["features"]}
            self.assertEqual(set(got), set(want), f"{name}: the named features are the slotted ones with ≥ {hero.NAMED_MIN} days")
            for repo, (slot, _days) in want.items():
                self.assertEqual(got[repo], slot, f"{name}: {repo} sits on its chart.toml slot")
            h = e["hero"]
            self.assertEqual(h["unslotted"], [])
            self.assertEqual(h["place"]["dropped"], [])
            n_repos = len(self.stats["repos"])
            self.assertEqual(h["counts"], {"repositories": n_repos, "charted": len(want), "rocks": n_repos - len(want)})
            self.assertEqual(len(h["rocks"]), n_repos - len(want))
            self.assertEqual({r["repo"] for r in h["rocks"]} | set(want), {r["name"] for r in self.stats["repos"]})
            # every rock lies on the hand-set fringe (within its across-jitter), none carries a figure or a name
            import chartlib as c
            fringe = c.catmull_rom([tuple(p) for p in self.cfg["hero"][f"rocks_{scale}"]], 24)
            s = hero.PHONE_S if scale == "phone" else 1.0
            for r in h["rocks"]:
                self.assertLessEqual(c.dist_to_polyline(r["x"], r["y"], fringe), hero.ROCK_ACROSS * s + 1.5, r)
                self.assertFalse(any(t["key"] == f"days:{r['repo']}" for t in e["text"]), f"{r['repo']} is a rock: no figure")
            line = f"{n_repos} REPOSITORIES · {len(want)} CHARTED · {n_repos - len(want)} AS ROCKS"
            self.assertIn(line, [t["s"] for t in e["text"]])
            self.assertGreaterEqual(self.svg[name].count("h0M") + self.svg[name].count('h0"'), 4 * len(h["rocks"]),
                                    "four dots per rock, round caps on zero-length segments")

    def test_data_change_moves_no_feature(self):
        """D3: a feature whose data grows changes its figure, never its place; a repository that crosses
        NAMED_MIN days without a slot is a rock and reported, never placed by a search."""
        sim = copy.deepcopy(self.stats)
        for r in sim["repos"]:
            if r["name"] == "FashionDB":
                r["commit_days"] += 4
            if r["name"] == "game_engine":
                r["commits"] *= 3
            if r["name"] == "Course_crusader":
                r["commit_days"] = hero.NAMED_MIN + 2      # no slot in chart.toml → a rock, reported
        sp = os.path.join(self.tmp, "sim.json")
        with open(sp, "w", encoding="utf-8") as fh:
            json.dump(sim, fh)
        rep = os.path.join(self.tmp, "sim-report.json")
        n = build_assets.main(sheets=["hero"], editions=["day"], out=os.path.join(self.tmp, "sim"), report_path=rep,
                              stats_path=sp, quiet=True)
        self.assertEqual(n, 0)
        with open(rep, encoding="utf-8") as fh:
            e = json.load(fh)["sheets"]["hero-day"]
        before = {f["repo"]: f for f in self.entry("day")["features"]}
        after = {f["repo"]: f for f in e["features"]}
        self.assertEqual(set(before), set(after))
        for repo in before:
            self.assertEqual((before[repo]["cx"], before[repo]["cy"]), (after[repo]["cx"], after[repo]["cy"]), repo)
        self.assertGreater(after["FashionDB"]["r"], before["FashionDB"]["r"])
        self.assertEqual(after["FashionDB"]["commit_days"], before["FashionDB"]["commit_days"] + 4)
        self.assertEqual(after["game_engine"]["r"], before["game_engine"]["r"], "commits do not move the measure")
        self.assertEqual(e["hero"]["unslotted"], ["Course_crusader"])
        self.assertIn("Course_crusader", {r["repo"] for r in e["hero"]["rocks"]})

    # ---- D4/D5: only the high-water week prints, measured, upright, flagged as a sweep
    def test_only_high_water_prints(self):
        for name in ("day", "phone-day"):
            h = self.entry(name)["hero"]
            causes = {b[6] for b in h["bracket"]}
            self.assertFalse(causes - {"unresolved"}, f"{name}: bracket failures {h['bracket']}")
            figs = [t for t in self.texts(name) if (t["key"] or "").startswith("week:")]
            self.assertEqual(len(figs), 1, f"{name}: one week figure, high water")
            self.assertEqual(h["soundings_printed"], 1)
            hw = self.stats["tide"]["hw"]
            self.assertEqual(figs[0]["s"], str(hw["n"]))
            self.assertEqual(figs[0]["key"], f"week:{hw['start']}")
            self.assertEqual(figs[0]["slant"], "upright")
            self.assertEqual(figs[0]["truth"], "measured")
            self.assertEqual(figs[0]["origin"], "sounding")
            self.assertGreaterEqual(figs[0]["size"], tokens.FLOORS["phone" if "phone" in name else "desk"]["semantic"])
        cap = [t for t in self.texts("day") if t["key"] == "high-water"]
        self.assertEqual(len(cap), 1, "the desk prints the high-water caption")
        sweeps = [s for s in self.stats["sweeps"] if self.stats["tide"]["hw"]["start"] <= s["date"]]
        if sweeps:
            self.assertTrue(cap[0]["s"].startswith("HW · SWEEP "), cap[0]["s"])
        self.assertEqual(cap[0]["truth"], "measured")

    def test_course_clear_of_features_and_harbour_open(self):
        for name in ("day", "phone-day"):
            h = self.entry(name)["hero"]
            s = hero.PHONE_S if "phone" in name else 1.0
            self.assertEqual(h.get("course_too_close", []), [])
            self.assertGreaterEqual(h["place"]["min_course_clearance"], hero.CLEAR_COURSE * s - 1)
            self.assertGreaterEqual(h["place"]["min_pair_clearance"], 30 * s, "features keep clear of each other")
        self.assertIn('href="#hero-h-sym-anchorage"', self.svg["day"])

    # ---- budgets
    def test_budgets(self):
        target_raw, target_gz = tokens.BUDGETS["targets_kb"]["hero"]
        for name in ALL:
            e = self.entry(name)
            self.assertLessEqual(e["elements"], tokens.BUDGETS["elements"], name)
            self.assertLessEqual(e["bytes"], target_raw * 1024, f"{name}: {e['bytes']} B raw")
            self.assertLessEqual(e["gz"], target_gz * 1024, f"{name}: {e['gz']} B gz")
            if name.startswith("phone"):
                self.assertLessEqual(e["bytes"], tokens.BUDGETS["phone_svg_kb"] * 1024, name)
            self.assertLessEqual(e["glyph_defs"], 160, name)

    # ---- honesty: strings, slant, still editions
    def test_no_banned_strings_or_elements(self):
        for name, svg in self.svg.items():
            self.assertIsNone(BANNED.search(svg), name)
            for bad in ("<text", "<tspan", "<textPath", "<pattern", "<filter", "animateMotion", "<script", "<image"):
                self.assertNotIn(bad, svg, f"{name}: {bad}")
            texts = " ".join(t["s"] for t in self.texts(name))
            self.assertIsNone(BANNED.search(texts), name)
            for gone in ("SEE SHEET", "SMALL-SCALE EDITION", "see Sheet"):
                self.assertNotIn(gone, texts, f"{name}: {gone!r} is gone (D4)")
            self.assertFalse(any(t["s"] == "PA" or t["s"] == "N" for t in self.texts(name)), f"{name}: no PA, no N")
            self.assertFalse(any(t["s"].endswith("°") for t in self.texts(name)), f"{name}: no bearings")
        self.assertIsNone(BANNED.search(self.ns_svg))

    def test_still_editions_are_frozen_finished_sheets(self):
        for name in ALL:
            if "still" in name:
                self.assertIsNone(ANIM.search(self.svg[name]), name)
                self.assertEqual(self.entry(name)["motion"]["class"], "still")
        day = sorted(t["s"] for t in self.texts("day"))
        still = sorted(t["s"] for t in self.texts("still-day"))
        self.assertEqual(day, still)

    def test_nothing_sloping_nothing_unmeasured(self):
        """D5: every printed figure is measured and upright; no italic run carries a digit; no subscripts."""
        figure_keys = ("days:", "week:", "first:", "high-water", "variation", "chart-edition", "repositories",
                       "chart-number", "surveys", "imprint")
        for name in ("day", "phone-day", "night"):
            for t in self.texts(name):
                if any(ch.isdigit() for ch in t["s"]):
                    self.assertEqual(t["slant"], "upright", f"{name}: sloping figure {t}")
                if t["key"] and t["key"].startswith(figure_keys):
                    self.assertEqual(t["truth"], "measured", f"{name}: unmeasured figure {t}")
                    self.assertEqual(t["slant"], "upright", t)
                self.assertFalse(any(ch in SUBSCRIPTS for ch in t["s"]), f"{name}: subscript in {t['s']!r}")
            keyed = {t["key"] for t in self.texts(name) if t["key"]}
            self.assertTrue({"chart-edition", "repositories", "surveys", "week:" + self.stats["tide"]["hw"]["start"]} <= keyed, keyed)
            heights = [t for t in self.texts(name) if (t["key"] or "").startswith("days:")]
            feats = {f["repo"]: f for f in self.entry(name)["features"]}
            self.assertEqual(len(heights), len(feats), "one figure per named feature")
            for t in heights:
                repo = t["key"].split(":", 1)[1]
                self.assertEqual(t["s"], str(feats[repo]["commit_days"]), t)
        texts = [t["s"] for t in self.texts("day")]
        self.assertTrue(any(s.startswith(f"CHART NO. {self.stats['repo_count']} · SHEET 1") for s in texts), texts)
        self.assertTrue(any(s.endswith("REDRAWN WEEKLY") for s in texts), "the imprint says weekly")
        self.assertIn("SOUNDINGS IN COMMIT-DAYS", texts)
        self.assertIn("sitemap.xml lies again", texts)
        self.assertEqual(sum(1 for s in texts if s.startswith("(") and s.endswith(")")), 2, "the two report dates")
        marks = [t for t in self.texts("day") if t["s"].startswith(('R "2"', 'G "1"'))]
        self.assertEqual(len(marks), 2)
        for t in marks:
            self.assertEqual(t["slant"], "upright")

    # ---- D4/D7: the cartouche, the rose, the type
    def test_cartouche_rose_and_type(self):
        for name in ("day", "phone-day"):
            e = self.entry(name)
            sc = "phone" if "phone" in name else "desk"
            floors = tokens.FLOORS[sc]
            for t in e["text"]:
                self.assertGreaterEqual(t["size"], floors["semantic"], f"no texture type on the hero: {t}")
                if t["role"] == "place-water":
                    self.assertEqual(t["slant"], "italic")
            caps = [t for t in e["text"] if t["role"] == "label-caps" and t["key"] not in ("folio", "chart-number")]
            self.assertLessEqual(len(caps), 1, [t["s"] for t in caps])
            box = list(hero.CARTOUCHE[sc])
            block = [t for t in e["text"] if t["within"] == box]
            self.assertGreaterEqual(len(block), 8, "name (two runs), thesis, five title lines")
            for t in block:
                self.assertGreaterEqual(t["x0"], box[0] - 0.5, t)
                self.assertLessEqual(t["x1"], box[0] + box[2] + 0.5, t)
                self.assertGreaterEqual(t["y0"], box[1] - 0.5, t)
                self.assertLessEqual(t["y1"], box[1] + box[3] + 0.5, t)
            lefts = {round(t["x0"]) for t in block if t["role"] in ("label", "label-caps")}
            self.assertEqual(len(lefts), 1, f"the title lines share one left edge: {lefts}")
            title = [t for t in block if t["role"] in ("label", "label-caps")]
            self.assertEqual(len(title), 5)
            self.assertEqual({t["tracking"] for t in title}, {hero.TITLE_TRACK[sc]})
            self.assertEqual(sorted({t["size"] for t in title}), sorted({25, 19} if sc == "desk" else {30, 26}))
            numerals = [t["s"] for t in e["text"] if t["within"] == list(hero.ROSE_BOX[sc])]
            self.assertTrue({"00", "06", "12", "18"} <= set(numerals), numerals)
            names = {f["name"].upper() for f in e["features"] if f["kind"] in hero.LAND_KINDS and f["kind"] != "harbour"}
            land = [t for t in e["text"] if t["s"] in names]
            self.assertEqual(len(land), len(names))
            for t in land:
                self.assertEqual(t["tracking"], hero.CAPS_TRACK[sc], t)
        day = self.texts("day")
        thesis = [t for t in day if t["s"] == "I survey a web that is wrong about itself."]
        self.assertEqual(len(thesis), 1)
        self.assertEqual(thesis[0]["font"], "serif-italic")
        self.assertEqual(thesis[0]["tracking"], -0.2)
        name = [t for t in day if t["s"] in ("Ben", "Russell")]
        self.assertEqual(len(name), 2)
        self.assertEqual({t["size"] for t in name}, {hero.NAME_SIZE["desk"]})
        var = [t for t in day if t["key"] == "variation"]
        self.assertEqual(len(var), 1)
        self.assertEqual(var[0]["s"], f"VAR {self.stats['variation']['hour']:02d}h ({self.stats['variation']['year']})")
        self.assertEqual(tokens.ROLES["desk"]["label-caps"][2], 1.6)
        self.assertEqual(tokens.ROLES["desk"]["sea-name"][2], 0.0)
        # the rose's ticks are the hour histogram: one LINE tick per hour with commit-days, a HAIR stub without
        hours = self.stats["hours"]
        svg = self.svg["still-day"]
        rose = svg[svg.index('transform="rotate(0 '):]
        rose = rose[:rose.index("</g>")]
        self.assertEqual(rose.count('stroke-width="2.1"'), 1)
        bars = re.search(r'<path d="([^"]*)" fill="none" stroke="[^"]*" stroke-width="2.1"', rose).group(1)
        self.assertEqual(bars.count("M"), sum(1 for v in hours if v > 0))
        if any(v == 0 for v in hours):
            stubs = re.search(r'<path d="([^"]*)" fill="none" stroke="[^"]*" stroke-width="0.8"', rose).group(1)
            self.assertEqual(stubs.count("M"), sum(1 for v in hours if v == 0))

    def test_accent_objects(self):
        theme = tokens.THEMES["day"]
        svg = self.svg["still-day"]
        body = svg.split("</defs>", 1)[1]
        self.assertEqual(body.count(f'fill="{theme.accent}"'), 1, "the sail alone (no rose arrowhead)")
        self.assertEqual(body.count('href="#hero-h-sym-nun"'), 1)
        defs = svg[:svg.index("</defs>")]
        self.assertEqual(defs.count(f'fill="{theme.accent}"'), 3, "sloop main, sloop-glyph main and the nun, in the defs")

    # ---- D6: night redrawn
    def test_night_redrawn_not_swapped(self):
        night, day = tokens.THEMES["night"], tokens.THEMES["day"]
        self.assertEqual(night.land, "#263040")
        self.assertEqual(night.shallow_b, "#1A4470")
        self.assertEqual((night.ink2, night.muted), ("#98A7BF", "#8894A6"), "ink2 out-ranks muted at night")
        import checks.contrast as contrast
        self.assertGreater(contrast.rel_lum(night.ink2), contrast.rel_lum(night.muted))
        self.assertGreaterEqual(contrast.de_ok(night.shallow_a, night.land), 0.04)
        self.assertEqual(tokens.NIGHT_WEIGHT, 1.2)
        allowed_day = {*tokens.W.values(), 0.8, 0.22, 0.45}
        allowed_night = {*tokens.W_NIGHT.values(), 0.8, 0.18, 0.45}
        for name in ALL:
            widths = {float(w) for w in re.findall(r'stroke-width="([\d.]+)"', self.svg[name])}
            if "night" in name:
                self.assertTrue(widths <= allowed_night, f"{name}: {widths - allowed_night}")
                self.assertIn(tokens.W_NIGHT["PEN"], widths)
                self.assertNotIn(tokens.W["PEN"], widths, f"{name}: a day-weight PEN stroke on the night sheet")
            else:
                self.assertTrue(widths <= allowed_day, f"{name}: {widths - allowed_day}")
        import chartlib as c
        self.assertEqual(c.weight_factor(), 1.0, "the night factor is reset after the build")

    # ---- motion (MASTERPLAN 2.1 / 7.3)
    def test_motion_budget(self):
        m = self.entry("day")["motion"]
        self.assertEqual(m["violations"], [])
        self.assertEqual(m["opening_end_s"], 4.0)
        self.assertEqual(m["indefinite"], 2)
        self.assertLessEqual(m["repaints_per_s"], 1.0)
        self.assertEqual(m["continuous_windows"][-1][1], 28.0)
        self.assertEqual(m["snapped"], [])
        svg = self.svg["day"]
        self.assertIn('id="hero-g1-flash" attributeName="opacity" begin="0s" dur="4s" repeatCount="indefinite"', svg)
        self.assertIn('id="hero-r2-flash" attributeName="opacity" begin="2s" dur="4s" repeatCount="indefinite"', svg)
        self.assertEqual(svg.count('id="hero-r2-lit"'), 1)
        self.assertEqual(svg.count('id="hero-g1-lit"'), 1)
        self.assertIn('id="hero-sail" attributeName="transform" type="translate" begin="4s" dur="24s" fill="freeze"', svg)
        self.assertEqual(svg.count('repeatCount="indefinite"'), 2)
        p = self.entry("phone-day")["motion"]
        self.assertEqual(p["indefinite"], 0, "phone lights are lit, not flashing (≤ 0.25 repaints/s)")
        self.assertEqual(p["violations"], [])
        self.assertEqual(self.entry("day")["hero"]["sail"]["tacks"], [])
        self.assertEqual(self.entry("phone-day")["hero"]["sail"]["fixes"], 7)
        psvg = self.svg["phone-day"]
        self.assertEqual(psvg.count('calcMode="discrete"'), 1, "the phone boat is one discrete translate")
        self.assertEqual(psvg.count("<set "), 0, "no <set> on the phone: one repaint per fix")
        self.assertEqual(sorted(lt["character"] for lt in self.entry("day")["lights"]), ["Fl G 4s", "Fl R 4s"])

    # ---- the pencil note when the soundings were not taken
    def test_no_sounding_pencil_note(self):
        self.assertTrue(self.ns_svg.startswith("<?xml"))
        with open(os.path.join(self.tmp, "ns.json"), encoding="utf-8") as fh:
            ns = json.load(fh)
        texts = [t["s"] for t in ns["sheets"]["hero-still-day"]["text"]]
        self.assertTrue(any(s.startswith("NO SOUNDINGS") for s in texts), texts)
        self.assertFalse(any(s.startswith("NO SOUNDINGS") for s in [t["s"] for t in self.texts("still-day")]))


class HeroScale(unittest.TestCase):
    """A repository busier than the sheet can hold steps the whole scale down (area ∝ commit-days still holds)
    and moves nothing."""

    def test_busier_flagship_still_builds_in_place(self):
        with open(STATS, encoding="utf-8") as fh:
            stats = json.load(fh)
        sim = copy.deepcopy(stats)
        for r in sim["repos"]:
            if r["name"] == "Scrapy":
                r["commit_days"] = 40
        out = tempfile.mkdtemp(prefix="v10-hero-scale-")
        sp = os.path.join(out, "stats.json")
        with open(sp, "w", encoding="utf-8") as fh:
            json.dump(sim, fh)
        rep = os.path.join(out, "build-report.json")
        n = build_assets.main(sheets=["hero"], editions=["day"], out=out, report_path=rep, stats_path=sp, quiet=True)
        self.assertEqual(n, 0)
        with open(rep, encoding="utf-8") as fh:
            e = json.load(fh)["sheets"]["hero-day"]
        self.assertLess(e["hero"]["field"]["area_scale_px2_per_day"], hero.K_AREA)
        with open(CFG, "rb") as fh:
            cfg = tomllib.load(fh)
        slots = {f["repo"]: tuple(f["desk"]) for f in cfg["features"]}
        for f in e["features"]:
            self.assertLessEqual(abs(f["ratio"] - 1), 0.08, f"{f['name']} ratio {f['ratio']}")
            self.assertEqual((f["cx"], f["cy"]), slots[f["repo"]])
        big = next(f for f in e["features"] if f["repo"] == "Scrapy")
        self.assertEqual(big["commit_days"], 40)
        self.assertLessEqual(big["r"], 90)
        shutil.rmtree(out, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
