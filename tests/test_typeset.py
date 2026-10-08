"""Tests for scripts/typeset.py (T5 type engine)."""
from __future__ import annotations

import math
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import tokens  # noqa: E402
import typeset as T  # noqa: E402


def _gaps(font: str, s: str, fix: bool = True) -> tuple[float, float]:
    """Visual gaps (font units) left and right of the middle dot in `s`."""
    saved = T.KERN_FIX
    if not fix:
        T.KERN_FIX = {}
    try:
        glyphs = T.shape(s, font)
    finally:
        T.KERN_FIX = saved
    face = T._face(font)
    pen, pos = 0.0, []
    for g in glyphs:
        pen += g.dx
        if g.inked:
            b = face.bounds(g.name)
            pos.append((g.name, pen + b[0], pen + b[2]))
        pen += g.adv
    i = next(k for k, p in enumerate(pos) if p[0] == "periodcentered")
    return pos[i][1] - pos[i - 1][2], pos[i + 1][1] - pos[i][2]


class ShapeTests(unittest.TestCase):
    def test_liga_fire_is_one_glyph_fewer(self):
        for font in ("serif", "serif-italic"):
            g = T.shape("fire", font)
            self.assertEqual(len(g), 3, font)
            self.assertEqual(g[0].kind, "lig")
            self.assertIn("f", g[0].name)
            self.assertIn("i", g[0].name)
        # office -> o ffi c e in the serif; Condensed has only fi
        self.assertEqual([g.name for g in T.shape("office", "serif")], ["o", "f_f_i", "c", "e"])
        self.assertEqual([g.name for g in T.shape("fire", "cond")][0], "fi")

    def test_kern_pairs_nonzero_for_AV_in_serif(self):
        self.assertLess(T.shape("AV", "serif")[1].dx, -30)
        self.assertLess(T.shape("AV", "cond")[1].dx, 0)
        self.assertEqual(T.shape("AV", "plex")[1].dx, 0)   # mono: no pairs, correctly

    def test_kern_fix_balances_the_middot(self):
        for font, s in (("serif-italic", "developer · scraping"), ("serif-italic", "developer · scraping"),
                        ("serif", "developer · scraping"), ("serif-italic", "of · x")):
            raw_l, raw_r = _gaps(font, s, fix=False)
            left, right = _gaps(font, s, fix=True)
            self.assertLessEqual(abs(left - right) / max(left, right), 0.10, (font, s, left, right))
            self.assertGreater(abs(raw_l - raw_r), abs(left - right), (font, s))
        self.assertLessEqual(abs(T.shape("r·", "serif-italic")[1].dx - 40), 1e-6)

    def test_tracking_not_added_after_space(self):
        a = T.text_width("A", font="cond", size=13, tracking=2.0)
        b = T.text_width("B", font="cond", size=13, tracking=2.0)
        sp = T.text_width(" ", font="cond", size=13)
        ab = T.text_width("A B", font="cond", size=13, tracking=2.0)
        self.assertAlmostEqual(ab, a + sp + b, places=6)
        # between two inked glyphs the tracking IS added
        self.assertAlmostEqual(T.text_width("AB", font="cond", size=13, tracking=2.0),
                               T.text_width("AB", font="cond", size=13) + 2.0, places=6)
        # synthetic spaces: thin .20 em, hair .10 em, nbsp = space
        self.assertAlmostEqual(T.text_width(" ", font="serif", size=100), 20.0, places=6)
        self.assertAlmostEqual(T.text_width(" ", font="serif", size=100), 10.0, places=6)
        self.assertAlmostEqual(T.text_width(" ", font="serif", size=100), T.text_width(" ", font="serif", size=100))

    def test_hand_kern_display(self):
        plain = T.shape("Ru", "serif", 176)[1].dx
        hand = T.shape("Ru", "serif", 176, hand=T.HAND_KERN["display"])[1].dx
        self.assertAlmostEqual(hand - plain, -20 * 176 / 1000, places=6)
        lifts = [g.dy for g in T.shape("Russell", "serif", 176, lift=T.HAND_LIFT["display"])]
        self.assertEqual(lifts[-1], -1.5)
        self.assertEqual(lifts[-2], 0.0)


class TextTests(unittest.TestCase):
    def setUp(self):
        T.begin_asset("hero")

    def test_text_grade_and_precision(self):
        day = T.text("Scrapy Harbor", 100, 200, role="title")
        self.assertIn('paint-order="stroke"', day)
        self.assertIn('stroke-width="0.22"', day)
        night = T.text("Scrapy Harbor", 100, 200, role="title", edition="night")
        self.assertIn(f'stroke="{tokens.THEMES["night"].paper}"', night)
        self.assertIn('stroke-width="0.18"', night)
        self.assertNotIn("paint-order", night)
        big = T.text("Ben Russell", 100, 300, role="display")
        d = re.search(r' d="([^"]+)"', big).group(1)
        self.assertNotIn(".", d, "display paths are integer coordinates")
        small = T.text("Profile Shoal", 100, 300, role="place-land")
        self.assertNotIn("paint-order", T.text("Ben", 0, 0, role="display"))
        self.assertIsNotNone(re.search(r'\d\.\d', re.search(r' d="([^"]+)"', small).group(1)))

    def test_night_uses_light_cuts(self):
        T.begin_asset("log")
        T.text_use("12:04 crawl", 10, 20, role="machine", edition="night")
        T.text_use("Fl R 4s", 10, 40, role="label", edition="night")
        defs = T.glyph_defs()
        self.assertIn("g-plex-light-13-", defs)
        self.assertIn("g-cond-light-13-", defs)
        self.assertNotIn('"g-plex-13-', defs)
        T.begin_asset("log")
        T.text_use("12:04 crawl", 10, 20, role="machine", edition="day")
        self.assertIn("g-plex-13-", T.glyph_defs())

    def test_text_use_one_use_per_glyph_with_xy(self):
        out = T.text_use("Fl(3) 10s", 50, 60, role="label")
        uses = re.findall(r'<use href="#([^"]+)" x="([-\d.]+)" y="([-\d.]+)"/>', out)
        self.assertEqual(len(uses), len("Fl(3)10s"))
        self.assertTrue(all(gid.startswith("g-cond-13-") for gid, _x, _y in uses))

    def test_check_type_flags_off_scale_and_semantic_11(self):
        T.text("fourteen", 10, 20, role="label", size=14)
        T.text_use("eleven", 10, 40, role="label", size=11)
        errs = T.check_type("day", "desk")
        self.assertTrue(any("off scale" in e and "14" in e for e in errs), errs)
        self.assertTrue(any("below floor" in e and "11" in e for e in errs), errs)
        self.assertTrue(any("not made by sounding()" in e for e in errs), errs)
        T.begin_asset("hero")
        T.text("fine", 10, 20, role="label")
        T.sounding(58, 100, 100, sub=3)
        self.assertEqual(T.check_type("day", "desk"), [])

    def test_check_type_serif_floor_within_and_caps_budget(self):
        T.text("Little Shoal", 10, 20, role="place-water", size=13)
        T.text("Soundings in commits", 10, 60, role="label-caps", within=(0, 40, 60, 30))
        T.text("Second stamp", 10, 90, role="label-caps")
        T.text("Chart No. 7", 10, 120, role="label-caps", key="chart-number")
        errs = T.check_type("day")
        self.assertTrue(any("serif below floor 17" in e for e in errs), errs)
        self.assertTrue(any("leaves its box" in e for e in errs), errs)
        self.assertTrue(any("label-caps runs" in e for e in errs), errs)

    def test_phone_scale(self):
        T.begin_asset("hero")
        T.text("Ben Russell", 10, 100, role="display", edition="phone-day")
        T.text_use("Scrapy Harbor", 10, 100, role="label", edition="phone-night", scale="phone")
        self.assertEqual(T.check_type("phone-night"), [])
        self.assertIn("g-cond-light-26-", T.glyph_defs())
        T.text_use("x", 10, 100, role="label", edition="phone-day", scale="phone", size=13)
        self.assertTrue(T.check_type("phone-day", "phone"))

    def test_runs_sets_figures_in_condensed(self):
        out = T.runs([("note", "HW "), ("figures", "312"), ("note", " · game_engine")], 100, 100)
        regs = T.runs_registry()
        fig = [r for r in regs if r.origin == "runs-figure"][0]
        self.assertEqual(fig.font, "cond-italic")
        self.assertAlmostEqual(fig.size, round(17 * 0.86, 1))
        self.assertEqual(T.check_type("day"), [])
        self.assertIn("g-cond-italic-14p6-51", out)

    def test_figures_registry(self):
        T.text("585", 10, 20, role="figure", truth="measured", key="commits")
        T.sounding(4, 50, 50, sub=2, truth="illustrative")
        self.assertEqual(T.FIGURES[0], ("hero", "commits", "585", "upright"))
        self.assertEqual(T.FIGURES[1][3], "italic")

    def test_exclusions_and_exclude(self):
        T.text("Grafana Lt", 100, 100, role="label")
        T.exclude("rose", 500, 500, 120, 120)
        ex = T.exclusions()
        self.assertEqual(len(ex), 2)
        x, y, w, h = ex[0]
        self.assertEqual(x, 100)
        self.assertLess(y, 100)
        self.assertGreater(w, 20)
        self.assertEqual(ex[1], (500, 500, 120, 120))
        named = T.exclusions(named=True)
        self.assertEqual(named[1][0], "rose")

    def test_label_caps_upper_and_tracking(self):
        out = T.text_use("Soundings in commits", 10, 10, role="label-caps")
        self.assertEqual(T.runs_registry()[-1].text, "SOUNDINGS IN COMMITS")
        self.assertEqual(T.runs_registry()[-1].tracked_spaces, 0)
        self.assertIn("g-cond-13-83", out)   # S

    def test_rotated_run_bbox(self):
        T.text("pencil note", 100, 100, role="note", rotate=-6)
        r = T.runs_registry()[-1]
        self.assertEqual(r.angle, -6)
        self.assertLess(r.y0, 100 - 17 * 0.6)
        self.assertGreater(r.x1 - r.x0, 50)


class SoundingTests(unittest.TestCase):
    def setUp(self):
        T.begin_asset("approaches")

    def test_sounding_renders_subscript_glyph(self):
        out = T.sounding(58, 200, 300, sub=3)
        self.assertIn("g-cond-11-8323", out)        # U+2083 subscript three, encoded glyph
        self.assertIn("g-cond-11-53", out)          # 5
        run = T.runs_registry()[-1]
        self.assertFalse(run.semantic)
        self.assertEqual(run.origin, "sounding")
        self.assertEqual(run.text, "58₃")
        self.assertEqual(T.check_type("day"), [])
        d = T.glyph_defs()
        self.assertIn('id="g-cond-11-8323"', d)

    def test_sounding_truths(self):
        ital = T.sounding(12, 10, 10, truth="illustrative")
        self.assertIn("g-cond-italic-11-", ital)
        datum = T.sounding(512, 10, 40, truth="datum", role="label")
        self.assertIn('stroke-width=".8"', datum)
        self.assertIn("H", datum)
        run = T.runs_registry()[-1]
        self.assertTrue(run.semantic)
        self.assertEqual(run.size, 13)
        self.assertEqual(T.FIGURES[-1][3], "datum")
        with self.assertRaises(ValueError):
            T.sounding(1, 0, 0, truth="guess")

    def test_sounding_night_light_cut(self):
        out = T.sounding(20, 10, 10, edition="night")
        self.assertIn("g-cond-light-11-", out)

    def test_sounding_fallback_without_encoded_subscripts(self):
        # serif lacks U+2080-2089: digits at 0.6x shifted down
        out = T.sounding(7, 100, 100, sub=2, role="title")
        self.assertIn("g-serif-28-55", out)
        self.assertIn("g-serif-16p8-50", out)


class PathTests(unittest.TestCase):
    def setUp(self):
        T.begin_asset("hero")

    def test_text_on_path_places_n_glyphs(self):
        pts = [(100 + i * 10, 300 + 12 * math.sin(i / 8)) for i in range(60)]
        out = T.text_on_path("Unsurveyed Sea", pts, role="sea-name")
        uses = re.findall(r'<use href="#g-serif-italic-28-[^"]+" transform="translate\([-\d. ]+\) rotate\([-\d.]+\)"/>', out)
        self.assertEqual(len(uses), len("UnsurveyedSea"))
        run = T.runs_registry()[-1]
        self.assertEqual(run.origin, "path")
        self.assertGreater(run.x1 - run.x0, 100)
        self.assertIn('paint-order="stroke"', out)
        self.assertEqual(T.check_type("day"), [])
        self.assertEqual(T.warnings(), [])

    def test_text_on_path_spread_and_direction(self):
        pts = [(600 - i * 10, 300.0) for i in range(60)]     # right-to-left polyline: read left to right
        out = T.text_on_path("UNSURVEYED", pts, role="label-caps", spread=0.7, start=0.1)
        xs = [float(m) for m in re.findall(r'translate\(([-\d.]+) ', out)]
        self.assertEqual(xs, sorted(xs))
        self.assertGreater(xs[-1] - xs[0], 0.6 * 590)
        self.assertLess(xs[-1] - xs[0], 0.75 * 590)
        self.assertTrue(all(m == "0" for m in re.findall(r'rotate\(([-\d.]+)\)', out)))

    def test_text_on_path_radius_guard(self):
        pts = [(300 + 20 * math.cos(a), 300 + 20 * math.sin(a)) for a in [i * math.pi / 16 for i in range(17)]]
        out = T.text_on_path("Tight", pts, role="place-water")
        self.assertTrue(any("bends too tightly" in w for w in T.warnings()))
        self.assertIn("rotate(", out)
        self.assertEqual(len(re.findall(r"<use ", out)), 5)


class BudgetTests(unittest.TestCase):
    def test_glyph_count_and_budget(self):
        T.begin_asset("hero")
        for i in range(30):
            T.sounding(i, 10 * i, 50)
        self.assertEqual(T.glyph_count(), 10)
        self.assertEqual(T.check_budget(), [])
        self.assertEqual(len(T.run_records()), 30)
        rec = T.run_records()[0]
        for k in ("s", "x0", "x1", "y", "size", "font", "slant", "role", "tier", "truth", "key", "rot"):
            self.assertIn(k, rec)
        self.assertEqual(rec["tier"], "texture")


if __name__ == "__main__":
    unittest.main()
