"""hero sheet (T2): contract, determinism, the area law, budgets, banned strings, still editions,
motion budget, lettering rules and the entrance — everything of T2 §5 that a test can read off the
built SVGs and the build report."""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import tempfile
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

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def entry(self, name):
        return self.report["sheets"][f"hero-{name}"]

    # ---- contract and alt
    def test_contract(self):
        self.assertEqual(hero.NAME, "hero")
        self.assertEqual(hero.KIND, "chart")
        self.assertEqual(hero.SIZES, {"desk": (1280, 740), "phone": (720, 900)})
        self.assertTrue(all(len(b) == 3 for b in hero.BREAKS))
        self.assertEqual(set(self.report["sheets"]), {f"hero-{n}" for n in ALL})

    def test_alt_is_short_plain_and_from_data(self):
        alt = hero.alt(self.stats, build_assets.load_cfg(CFG))
        self.assertLessEqual(len(alt.split()), 25)
        self.assertFalse(alt.startswith("The"))
        self.assertIn(str(self.stats["repo_count"]), alt)
        self.assertTrue(alt.endswith("A boat sails in and anchors."))

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

    # ---- the field: area law, brackets, every repo charted
    def test_area_law_every_feature(self):
        for name in ("day", "phone-day"):
            feats = self.entry(name)["features"]
            self.assertTrue(feats)
            for f in feats:
                self.assertTrue(f["ok"], f"{name}: {f['name']} ratio {f['ratio']}")
                self.assertLessEqual(abs(f["ratio"] - 1), 0.08, f"{name}: {f['name']}")
                if f["drawn_ratio"] is not None:
                    self.assertLessEqual(abs(f["drawn_ratio"] - 1), 0.08, f"{name}: {f['name']} drawn {f['drawn_ratio']}")
        desk = {f["name"] for f in self.entry("day")["features"]}
        surveyed = [r for r in self.stats["repos"] if r.get("commits")]
        self.assertEqual(len(desk), len(surveyed), "every surveyed repo is a feature on the desk sheet")
        h = self.entry("day")["hero"]
        self.assertEqual(h["place"]["dropped"], [])
        self.assertEqual(h["place"]["beyond_cap"], [])

    def test_soundings_bracketed(self):
        for name in ("day", "phone-day"):
            h = self.entry(name)["hero"]
            causes = {b[6] for b in h["bracket"]}
            self.assertFalse(causes - {"unresolved"}, f"{name}: bracket failures {h['bracket']}")
        self.assertGreaterEqual(self.entry("day")["hero"]["soundings_printed"], 36)
        # every printed sounding is a week from stats.json, upright, measured
        weeks = {str(w["n"]) for w in self.stats["weeks"]}
        figs = [t for t in self.entry("day")["text"] if t["origin"] == "sounding" and (t["key"] or "").startswith("week:")]
        self.assertGreaterEqual(len(figs), 36)
        for t in figs:
            self.assertIn(t["s"], weeks)
            self.assertEqual(t["slant"], "upright")
            self.assertEqual(t["truth"], "measured")

    def test_course_clear_of_features_and_harbour_open(self):
        h = self.entry("day")["hero"]
        self.assertEqual(h.get("course_too_close", []), [])
        self.assertGreaterEqual(h["place"]["min_course_clearance"], hero.CLEAR_COURSE - 1)
        self.assertGreaterEqual(h["place"]["min_pair_clearance"], 30, "islet pairs keep 30 px, islands 44")

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
            texts = " ".join(t["s"] for t in self.entry(name)["text"])
            self.assertIsNone(BANNED.search(texts), name)
        self.assertIsNone(BANNED.search(self.ns_svg))

    def test_still_editions_are_frozen_finished_sheets(self):
        for name in ALL:
            if "still" in name:
                self.assertIsNone(ANIM.search(self.svg[name]), name)
                self.assertEqual(self.entry(name)["motion"]["class"], "still")
        # the still carries the same lettering as the motion edition (the t = 95 s frame)
        day = sorted(t["s"] for t in self.entry("day")["text"])
        still = sorted(t["s"] for t in self.entry("still-day")["text"])
        self.assertEqual(day, still)

    def test_figures_are_measured_and_upright(self):
        for t in self.entry("day")["text"]:
            if t["key"] and (t["key"].startswith("commits:") or t["key"].startswith("week:")):
                self.assertEqual(t["slant"], "upright", t)
                self.assertEqual(t["truth"], "measured", t)
        heights = [t for t in self.entry("day")["text"] if (t["key"] or "").startswith("commits:")]
        self.assertEqual(len(heights), len(self.entry("day")["features"]), "one spot height per feature")
        # the chart number is the repo count and the notices line counts the notices
        texts = [t["s"] for t in self.entry("day")["text"]]
        self.assertIn(f"CHART NO. {self.stats['repo_count']} · SHEET 1", texts)
        self.assertTrue(any(s == f"CORRECTED THROUGH NOTICE {len(self.stats['notices'])}" for s in texts), texts)

    # ---- lettering rules (T2 §5.4) and the thesis said once
    def test_type_rules(self):
        for name in ("day", "phone-day"):
            e = self.entry(name)
            floors = tokens.FLOORS[e["form"] if e["form"] == "phone" else "desk"]
            for t in e["text"]:
                if t["semantic"]:
                    self.assertGreaterEqual(t["size"], floors["semantic"], t)
                else:
                    self.assertIn(t["size"], (floors["texture"], floors["semantic"]), t)
            caps = [t for t in e["text"] if t["role"] == "label-caps" and t["key"] not in ("folio", "chart-number")]
            self.assertLessEqual(len(caps), 1, [t["s"] for t in caps])
        thesis = [t for t in self.entry("day")["text"] if t["s"] == "I survey a web that is wrong about itself."]
        self.assertEqual(len(thesis), 1)
        self.assertEqual(thesis[0]["font"], "serif-italic")
        self.assertEqual(sum(1 for t in self.entry("day")["text"] if t["s"] in ("Ben", "Russell")), 2)
        block = [t for t in self.entry("day")["text"] if t["within"] == [70, 540, 540, 130]]
        self.assertGreaterEqual(len(block), 6)
        for t in block:
            self.assertGreaterEqual(t["x0"], 69.5, t)
            self.assertLessEqual(t["x1"], 610.5, t)
            self.assertGreaterEqual(t["y0"], 539.5, t)
            self.assertLessEqual(t["y1"], 670.5, t)
        # water names slope, land names stand upright
        for t in self.entry("day")["text"]:
            if t["role"] == "place-water":
                self.assertEqual(t["slant"], "italic")

    def test_three_accent_objects_clear_of_the_name(self):
        theme = tokens.THEMES["day"]
        svg = self.svg["still-day"]
        body = svg.split("</defs>", 1)[1]
        self.assertEqual(body.count(f'fill="{theme.accent}"'), 2, "arrowhead and the sail")
        self.assertEqual(body.count('href="#hero-h-sym-nun"'), 1)
        defs = svg[:svg.index("</defs>")]
        self.assertEqual(defs.count(f'fill="{theme.accent}"'), 3, "sloop main, sloop-glyph main and the nun, in the defs")
        arrow = re.search(r'<path d="M1000 \d+l-5 -11h10z" fill="' + theme.accent, svg)
        self.assertIsNotNone(arrow)

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
        self.assertEqual(sorted(lt["character"] for lt in self.entry("day")["lights"]), ["Fl G 4s", "Fl R 4s"])

    # ---- the pencil note when the soundings were not taken
    def test_no_sounding_pencil_note(self):
        self.assertTrue(self.ns_svg.startswith("<?xml"))
        with open(os.path.join(self.tmp, "ns.json"), encoding="utf-8") as fh:
            ns = json.load(fh)
        texts = [t["s"] for t in ns["sheets"]["hero-still-day"]["text"]]
        self.assertTrue(any(s.startswith("NO SOUNDINGS TONIGHT") for s in texts), texts)
        self.assertFalse(any(s.startswith("NO SOUNDINGS") for s in [t["s"] for t in self.entry("still-day")["text"]]))


if __name__ == "__main__":
    unittest.main()
