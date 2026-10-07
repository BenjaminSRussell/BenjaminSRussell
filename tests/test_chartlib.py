"""Tests for scripts/chartlib (T6). Run: python3 -m unittest discover -s tests -v"""
from __future__ import annotations

import math
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import chartlib as c  # noqa: E402
from tokens import THEMES, W  # noqa: E402


def lbl(text, x, y, role, **kw):
    # the callback is handed coordinates already rounded to one decimal; assert that here
    assert round(x, 1) == x and round(y, 1) == y, (text, x, y)
    return f'<text x="{x}" y="{y}" data-role="{role}">{text}</text>'


class FieldTests(unittest.TestCase):
    def test_single_bump_contour_closed_and_area(self):
        f = c.Feature("Shoal", 100, "shoal", 400, 300, r=40)
        F = c.Field.from_soundings(800, 600, [], base=20, features=[f], coast=c.Coast((0, 0, 800, 600)))
        cs = [k for k in c.contours(F, [5.0]) if k.closed]
        self.assertEqual(len(cs), 1)
        k = cs[0]
        self.assertTrue(k.shallow_inside)
        self.assertAlmostEqual(k.area() / (math.pi * 40 * 40), 1.0, delta=0.08)
        self.assertEqual(c.closed_check(c.contours(F, [5.0, 10.0])), [])
        # the shoal never breaks the surface, the ring is at r
        self.assertGreaterEqual(F.value(400, 300), 2.0 - 1e-9)
        self.assertAlmostEqual(F.value(440, 300), 5.0, places=6)

    def test_island_breaks_surface_with_shelf(self):
        g = c.Feature("Isle", 300, "island", 400, 300, r=60)
        F = c.Field.from_soundings(800, 600, [], base=20, features=[g])
        land = [k for k in c.contours(F, [0.0]) if k.closed]
        self.assertEqual(len(land), 1)
        self.assertTrue(land[0].shallow_inside)
        self.assertLess(F.value(400, 300), 0)
        self.assertLess(land[0].area(), math.pi * 60 * 60)   # coastline inside the 5-ring

    def test_from_soundings_reproduces_samples(self):
        import random
        rng = random.Random(7)
        samples = [(rng.uniform(80, 720), rng.uniform(80, 520), rng.uniform(2, 60)) for _ in range(52)]
        f = c.Feature("Shoal", 100, "shoal", 400, 300, r=40)
        F = c.Field.from_soundings(800, 600, samples, base=20, features=[f])
        for x, y, v in samples:
            self.assertAlmostEqual(F.value(x, y), v, delta=1e-6)
        self.assertLess(F.report.residual_max, 1e-6)
        # zero weeks are solved to the floor, not to land
        F0 = c.Field.from_soundings(800, 600, [(300, 300, 0)], base=20)
        self.assertAlmostEqual(F0.value(300, 300), 0.5, places=6)

    def test_ridge_solve_handles_clustered_points(self):
        samples = [(300, 300, 10), (300.5, 300, 30), (500, 400, 20)]
        F = c.Field.from_soundings(800, 600, samples, base=20)
        self.assertTrue(all(math.isfinite(k.amp) for k in F.kernels))
        self.assertLess(abs(F.value(500, 400) - 20), 1e-6)

    def test_lu_solve(self):
        A = [[4, 1, 0], [1, 3, 1], [0, 1, 2]]
        x = c.lu_solve(A, [1, 2, 3])
        for i in range(3):
            self.assertAlmostEqual(sum(A[i][j] * x[j] for j in range(3)), [1, 2, 3][i], places=9)

    def test_bracket_test(self):
        samples = [(200, 200, 3), (400, 200, 8), (600, 200, 30), (400, 400, 70)]
        F = c.Field.from_soundings(800, 600, samples, base=20, coast=c.Coast((0, 0, 800, 600), unsurveyed_x=None))
        cs = c.contours(F, c.DEFAULT_LEVELS)
        self.assertEqual(c.bracket_test(cs, samples, base=20), [])
        self.assertEqual(c.band_of(cs, 100, 500, c.DEFAULT_LEVELS, base=20), 50.0)   # ambient water is under 50

    def test_coast_closes_everything(self):
        import random
        rng = random.Random(3)
        samples = [(rng.uniform(40, 1200), rng.uniform(40, 700), rng.uniform(1, 80)) for _ in range(40)]
        F = c.Field.from_soundings(1280, 740, samples, base=20, coast=c.Coast((24, 24, 1232, 692)))
        self.assertEqual(c.closed_check(c.contours(F, [5.0, 10.0, 50.0])), [])


class PathTests(unittest.TestCase):
    def test_compact_path_round_trips(self):
        pts = [(100.4, 100.2), (120.6, 101), (140.1, 110.7), (160, 130), (150, 150.2), (120, 160), (100, 140), (90.3, 120)]
        d = c.compact_path(pts, True, every=1)
        self.assertTrue(d.startswith("M100 100"))
        self.assertTrue(d.endswith("Z"))
        self.assertEqual(c.parse_path(d), [(round(x), round(y)) for x, y in pts])
        d3 = c.compact_path(pts * 3, False, every=3)
        back = c.parse_path(d3)
        self.assertEqual(back[0], (100, 100))
        self.assertEqual(back[-1], (90, 120))
        # no decimals anywhere
        self.assertNotIn(".", d3)

    def test_smooth_and_monotone_paths_have_sane_numbers(self):
        pts = [(0, 0), (10, 5), (20, 3), (30, 9), (40, 9), (50, 2)]
        s = c.smooth_path(pts, False, every=1)
        self.assertTrue(s.startswith("M0 0c"))
        m = c.monotone_path(pts, baseline=20)
        self.assertTrue(m.endswith("V20H0Z"))
        for n in re.findall(r"-?\d+\.\d+", m + s):
            self.assertLessEqual(len(n.split(".")[1]), 1)

    def test_clip_polyline(self):
        ins, outs = c.clip_polyline([(0, 5), (20, 5)], (5, 0, 10, 10))
        self.assertEqual(len(ins), 1)
        self.assertEqual(len(outs), 2)
        self.assertAlmostEqual(ins[0][0][0], 5)
        self.assertAlmostEqual(ins[0][-1][0], 15)

    def test_contour_labels_and_draw(self):
        f = c.Feature("Shoal", 300, "shoal", 400, 300, r=70)
        F = c.Field.from_soundings(800, 600, [], base=20, features=[f])
        cs = c.contours(F, [5.0, 10.0])
        breaks = c.contour_labels(cs, min_len=160, gap=20)
        self.assertEqual(len(breaks), 2)
        k, i0, i1 = breaks[0]
        x, y, ang = c.break_anchor(k, i0, i1)
        self.assertLessEqual(abs(ang), 30)
        svg = c.draw_contours(cs, [10.0], THEMES["day"], breaks=breaks, approx_clip=(440, 200, 200, 200))
        self.assertIn('stroke-dasharray="3 3"', svg)
        self.assertEqual(len(re.findall(r"<path", svg)), 4)


class PlaceTests(unittest.TestCase):
    def _builder(self, feats):
        return c.Field.from_soundings(1280, 740, [], base=20, features=feats, coast=c.Coast((24, 24, 1232, 692)))

    def test_solve_radii_converges(self):
        feats = [c.Feature("A", 585, "island", 838, 376), c.Feature("B", 331, "shoal", 1004, 482),
                 c.Feature("C", 40, "islet", 500, 600), c.Feature("W", 10, "wreck", 1040, 300)]
        reps = c.solve_radii(self._builder, feats, k_area=32.2)
        self.assertEqual(len(reps), 3)
        for r in reps:
            self.assertTrue(r.ok, r)
            self.assertAlmostEqual(r.ratio, 1.0, delta=0.08)
        F = self._builder(feats)
        cs = c.contours(F, [5.0])
        polys = c.feature_polygons(cs, feats)
        self.assertEqual(set(polys), {"A", "B", "C"})
        self.assertEqual(c.closed_check(cs), [])

    def test_place_features_slots_halton_and_clearances(self):
        feats = [c.Feature("scrapy", 400, "harbour", r=58, alias="scrapy"),
                 c.Feature("rustmapper", 120, "shoal", r=36, alias="rustmapper")]
        feats += [c.Feature(f"r{i}", 30 - i, "islet" if i > 4 else "island", r=max(6, 30 - 2 * i)) for i in range(10)]
        course = [(1136, 296), (1046, 360), (900, 470), (842, 580), (776, 556)]
        rep = c.place_features(feats, (24, 24, 1232, 692), [(40, 40, 800, 280), (920, 80, 160, 195), (1080, 24, 200, 692)],
                               course, 2709, {"scrapy": (760, 560), "rustmapper": (1004, 482)}, cap=8)
        self.assertEqual(feats[0].x, 760)
        self.assertEqual(len(rep.placed), 8)
        self.assertEqual(len(rep.beyond_cap), 4)
        placed = [f for f in feats if f.placed]
        for i, a in enumerate(placed):
            for b in placed[i + 1:]:
                if "harbour" in (a.kind, b.kind) and (a.slot or b.slot):
                    continue
                self.assertGreaterEqual(math.hypot(a.x - b.x, a.y - b.y) + 1e-6, a.r + b.r + 44)
        for f in placed:
            if f.kind != "harbour" and not f.slot:
                self.assertGreaterEqual(c.dist_to_polyline(f.x, f.y, course) + 1e-6, f.r + 30)
                self.assertFalse(40 - f.r - 28 <= f.x <= 840 + f.r + 28 and 40 - f.r - 28 <= f.y <= 320 + f.r + 28)
        # deterministic
        feats2 = [c.Feature(f.name, f.value, f.kind, r=f.r, alias=f.alias) for f in feats]
        c.place_features(feats2, (24, 24, 1232, 692), [(40, 40, 800, 280), (920, 80, 160, 195), (1080, 24, 200, 692)],
                         course, 2709, {"scrapy": (760, 560), "rustmapper": (1004, 482)}, cap=8)
        self.assertEqual([(f.x, f.y) for f in feats], [(f.x, f.y) for f in feats2])

    def test_soundings_along_and_spot_heights(self):
        course = [(1136, 296), (1046, 360), (900, 470), (842, 580), (776, 556)]
        pts = c.soundings_along(course, list(range(52)))
        self.assertEqual(len(pts), 52)
        self.assertTrue(all(isinstance(x, int) and isinstance(y, int) for x, y, _ in pts))
        self.assertTrue(all(abs(l) <= 2.5 for l in c.soundings_lean(course, pts)))
        f = c.Feature("A", 300, "island", 400, 300, r=60)
        F = c.Field.from_soundings(800, 600, [], base=20, features=[f])
        sh = c.spot_heights([f], c.contours(F, [5.0]))
        self.assertEqual(sh[0][1:], (400, 290, 0))


class SymbolTests(unittest.TestCase):
    def test_symbol_defs_ids_prefixed_and_sloop_commands(self):
        defs = c.symbol_defs(THEMES["day"], "hero", "day")
        ids = re.findall(r'id="([^"]+)"', defs)
        for n in c.SYMBOL_NAMES:
            self.assertIn(f"hero-sym-{n}", ids)
        self.assertTrue(all(i.startswith("hero-") for i in ids))
        self.assertIn("hero-light-lit", ids)
        self.assertIn("hero-traffic-lit", ids)
        self.assertIn("hero-halo-lit", ids)
        self.assertNotIn("<pattern", defs)
        self.assertNotIn("filter", defs)
        silhouette = "".join(c.SLOOP_DETAIL[k] for k in ("hull", "main", "jib"))
        self.assertLessEqual(len(re.findall(r"[MLQCA]", silhouette)), 12)
        glyph = "".join(c.SLOOP_GLYPH.values())   # 31's exact paths: 10 drawing commands, 3 closes
        self.assertLessEqual(len(re.findall(r"[MLQCA]", glyph)), 12)
        self.assertLess(len(glyph), len(silhouette))
        # day misregisters colour fills; night does not
        self.assertIn("translate(0.6 0.4)", defs)
        self.assertNotIn("translate(0.6 0.4)", c.symbol_defs(THEMES["night"], "hero", "night"))

    def test_strokes_only_from_W(self):
        theme = THEMES["day"]
        jit = c.Jitter(27, "t")
        svg = (c.symbol_defs(theme, "p", "day") + c.serpent(theme) + c.frame(400, 300, theme) +
               c.two_ring_rose(200, 150, 72, theme, [1] * 24, 3, label_cb=lbl) +
               c.course([(10, 10), (100, 60), (200, 50)], theme, jit, label_cb=lbl) +
               c.restricted_line([(10, 10), (100, 10), (100, 80), (10, 80)], theme) +
               c.track_lines(0, 0, 100, 0, 4, 10, theme)[0] + c.paper(400, 300, theme, "day", jit)[1])
        widths = {float(w) for w in re.findall(r'stroke-width="([\d.]+)"', svg)}
        self.assertTrue(widths <= set(W.values()), widths)
        for n in re.findall(r'[ "](-?\d+\.\d+)', svg):
            self.assertLessEqual(len(n.split(".")[1]), 1, n)
        with self.assertRaises(KeyError):
            c.stroke("THIN", "#000")

    def test_use_and_doubt(self):
        self.assertEqual(c.use("can", 10, 20, "ap"), '<use href="#ap-sym-can" x="10" y="20"/>')
        self.assertIn('rotate(-4)', c.use("sloop", 0, 0, "ap", scale=1.4, rotate=-4))
        self.assertIn("Rep", c.doubt("Rep", 100, 100, lbl, "ap"))


class WaterTests(unittest.TestCase):
    def test_tints_coast_danger_hatch(self):
        theme = THEMES["day"]
        jit = c.Jitter(27, "hero")
        f = c.Feature("Shoal", 100, "shoal", 400, 300, r=40)
        g = c.Feature("Isle", 300, "island", 600, 300, r=60)
        F = c.Field.from_soundings(800, 600, [], base=20, features=[f, g], coast=c.Coast((0, 0, 800, 600)))
        cs = c.contours(F, c.DEFAULT_LEVELS)
        tb = c.tint_bands(cs, theme)
        self.assertEqual(tb.count("<path"), 3)
        self.assertIn(theme.land, tb)
        self.assertIn('fill-rule="evenodd"', tb)
        self.assertEqual(c.coastline(cs, theme).count("<path"), 2)
        dl = c.danger_lines(cs, 5.0, theme, jit, inside=[(400, 300)])
        self.assertEqual(dl.count("<path"), 1)
        self.assertRegex(dl, r'stroke-dasharray="0\.1 4\.[0-6]"')
        self.assertIn("stroke-dashoffset", dl)
        defs, body = c.hatch((1080, 150, 200, 430), theme, jit, "unsurveyed", "hu", ramp=(1080, 1120))
        self.assertIn("linearGradient", defs)
        self.assertNotIn("clipPath", defs)
        self.assertNotIn("<pattern", body)
        self.assertLessEqual(body.count("<path"), 4)
        self.assertGreater(body.count("M"), 50)
        land = c.level_polygons(cs, 0.0)[0]
        v = c.coast_vignette(land, theme, jit)
        self.assertEqual(v.count("<path"), 3)

    def test_jitter_is_deterministic_and_keyed(self):
        a, b = c.Jitter(27, "hero/danger"), c.Jitter(27, "hero/danger")
        self.assertEqual([a.uniform(0, 1) for _ in range(5)], [b.uniform(0, 1) for _ in range(5)])
        self.assertNotEqual(c.Jitter(27, "hero/x").uniform(0, 1), c.Jitter(27, "hero/y").uniform(0, 1))
        self.assertNotEqual(c.Jitter(27, "a").uniform(0, 1), c.Jitter(28, "a").uniform(0, 1))
        # two identical builds are byte-identical
        t = THEMES["night"]
        s1 = c.paper(1280, 740, t, "night", c.Jitter(27, "p"))[1] + c.hatch((0, 0, 100, 100), t, c.Jitter(27, "h"))[1]
        s2 = c.paper(1280, 740, t, "night", c.Jitter(27, "p"))[1] + c.hatch((0, 0, 100, 100), t, c.Jitter(27, "h"))[1]
        self.assertEqual(s1, s2)


class FurnitureTests(unittest.TestCase):
    def test_course_samples_and_offsets(self):
        pts = [(1136, 296), (1046, 360), (900, 470), (842, 580), (776, 556)]
        s = c.course_samples(pts, 64)
        self.assertEqual(len(s), 64)
        self.assertEqual((s[0][0], s[0][1]), (1136.0, 296.0))
        self.assertEqual((s[-1][0], s[-1][1]), (776.0, 556.0))
        self.assertAlmostEqual(c.compass_bearing((842, 580), (776, 556)), 290, delta=1.5)
        leg = ((842, 580), (776, 556))
        sx, sy = c.lateral_offset(leg, 0.5, "starboard", 24)
        px, py = c.lateral_offset(leg, 0.5, "port", 24)
        self.assertLess(sy, py)   # heading 290°: starboard is north (smaller y)

    def test_frame_kinds(self):
        theme = THEMES["day"]
        self.assertEqual(c.frame(1280, 740, theme, "none"), "")
        full = c.frame(1280, 740, theme, "minute-bars")
        broken = c.frame(1280, 740, theme, "broken", gaps=[("right", 150, 580)])
        self.assertLess(len(broken), len(full))
        self.assertEqual(c.frame(1280, 740, theme, "double").count("<path"), 2)

    def test_lettering_roles_exist(self):
        from tokens import ROLES
        for cls, (role, slant) in c.LETTERING.items():
            self.assertIn(role, ROLES["desk"], cls)
            self.assertIn(slant, ("upright", "italic"))


if __name__ == "__main__":
    unittest.main()
