"""Unit tests for scripts/timeline.py (T4 motion engine)."""
from __future__ import annotations

import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import timeline as T  # noqa: E402
import tokens  # noqa: E402

CUBIC = "M0,0 C 50,100 100,100 150,0"
COURSE = ("M1136,296 C1100,320 1070,340 1046,360 C980,410 930,450 900,470 "
          "C860,500 850,540 842,580 C830,600 790,570 776,556")


def _values(a: str) -> list[str]:
    return re.search(r'values="([^"]*)"', a).group(1).split(";")


def _key_times(a: str) -> list[float]:
    return [float(x) for x in re.search(r'keyTimes="([^"]*)"', a).group(1).split(";")]


class FlashTests(unittest.TestCase):
    def test_fl3_three_pulses_ends_dark(self):
        tl = T.Timeline("t")
        a = tl.flash("Fl(3)", 10)
        vals = _values(a)
        self.assertEqual(vals, ["1", "0", "1", "0", "1", "0"])
        self.assertEqual(vals[-1], "0")
        self.assertEqual(sum(1 for v in vals if v == "1"), 3)
        self.assertEqual(_key_times(a), [0, 0.05, 0.15, 0.2, 0.3, 0.35])
        self.assertIn('repeatCount="indefinite"', a)
        self.assertIn('calcMode="discrete"', a)
        self.assertEqual(T.flash_schedule("Fl(3) 10s"), [(0.0, 0.5), (1.5, 2.0), (3.0, 3.5)])

    def test_character_string_carries_period(self):
        tl = T.Timeline("t")
        a = tl.flash("Fl R 4s", begin=2)
        self.assertIn('dur="4s"', a)
        self.assertIn('begin="2s"', a)
        self.assertEqual(_values(a), ["1", "0"])

    def test_iso_oc_q(self):
        tl = T.Timeline("t")
        self.assertEqual(_key_times(tl.flash("Iso 4s")), [0, 0.5])
        oc = tl.flash("Oc(2) 10s")
        self.assertEqual(_values(oc), ["1", "0", "1", "0"])     # lit, two eclipses, ends dark
        q = tl.flash("Q 4s")
        self.assertEqual(len(_values(q)), 8)                    # one 0.5 s flash each second

    def test_period_validated(self):
        tl = T.Timeline("t")
        with self.assertRaises(ValueError):
            tl.flash("Fl", 7)
        with self.assertRaises(ValueError):
            tl.flash("Fl(4)", 4)   # four flashes do not fit in 4 s

    def test_lights_share_instants(self):
        tl = T.Timeline("t")
        tl.flash("Fl G 4s", begin=0)
        tl.flash("Fl R 4s", begin=2)
        tl.flash("Fl G 4s", begin=0)
        tl.flash("Fl R 4s", begin=2)
        r = tl.report()
        self.assertEqual(r["indefinite"], 4)
        self.assertAlmostEqual(r["repaints_per_s"], 1.0)        # 0,0.5,2,2.5 per 4 s, shared


class SailTests(unittest.TestCase):
    def test_sail_is_animate_transform_with_n_values(self):
        tl = T.Timeline("hero")
        s = tl.sail(COURSE, 4, 24, n=64)
        self.assertIn("<animateTransform", s.anim)
        self.assertIn('type="translate"', s.anim)
        self.assertNotIn("animateMotion", s.anim)
        self.assertNotIn('rotate="auto"', s.anim)
        vals = _values(s.anim)
        self.assertEqual(len(vals), 64)
        kts = _key_times(s.anim)
        self.assertEqual(len(kts), 64)
        self.assertEqual(kts[0], 0.0)
        self.assertEqual(kts[-1], 1.0)
        self.assertTrue(all(b >= a for a, b in zip(kts, kts[1:])))
        for v in vals:                                          # integer coordinates
            self.assertRegex(v, r"^-?\d+ -?\d+$")
        self.assertEqual(s.end, 28.0)
        self.assertEqual(s.facing, -1)                          # the course runs west
        self.assertEqual(s.tacks, [])                           # no reversal on a westward course
        self.assertIn('fill="freeze"', s.anim)
        self.assertEqual(s.transform, "translate(1136 296)")
        self.assertEqual(s.stop, (776, 556))

    def test_sail_detects_reversal(self):
        tl = T.Timeline("t")
        s = tl.sail("M100,100 L400,120 L150,300", 4, 20, n=32)
        self.assertEqual(len(s.tacks), 1)
        self.assertTrue(tl.on_grid(s.tacks[0]))
        self.assertEqual(s.facing, 1)

    def test_ease_warps_key_times(self):
        tl = T.Timeline("t")
        s = tl.sail("M0,0 L100,0", 0, 10, n=11, ease="settle")
        kts = _key_times(s.anim)
        # settle is an ease-out: half the distance is covered well before half the time
        self.assertLess(kts[5], 0.35)
        lin = tl.sail("M0,0 L100,0", 0, 10, n=11, ease="linear")
        self.assertAlmostEqual(_key_times(lin.anim)[5], 0.5, places=3)

    def test_wrap_and_tack(self):
        tl = T.Timeline("t")
        s = tl.sail("M100,100 L400,120 L150,300", 4, 20, n=16)
        g = s.wrap("<path d='M0 0'/>")
        self.assertIn('transform="translate(100 100)"', g)
        self.assertIn("rotate(-4)", g)
        tk = tl.tack(s.tacks[0], 3.0, "<path d='M1 1'/>", facing=s.facing)
        self.assertIn('type="scale"', tk.sails)
        self.assertIn("0.06 1", tk.sails)
        self.assertIn('calcMode="discrete"', tk.hull)
        self.assertEqual(tk.facing, -s.facing)
        self.assertTrue(tl.on_grid(tk.flip_at))


class StillModeTests(unittest.TestCase):
    def test_motion_false_returns_end_state(self):
        tl = T.Timeline("hero", motion=False)
        parts = [
            tl.fade_in('<path d="M0 0"/>', 2.2),
            tl.draw_in('d="M0 0 L1 1" stroke="#000"', begin=0.2),
            tl.reveal('<path d="M1 1"/>', 2.6),
            tl.flash("Fl(3) 10s"),
            tl.flash("Fl R 4s", begin=2),
            tl.anim("opacity", [0, 1], 0.4, 1.0),
            tl.xform("rotate", [12, -4, 0], 1.6, 2.0, ease="sea"),
            tl.fixes([(0, 0), (10, 10), (20, 20)], 0, hold=88, boat='<circle r="2"/>'),
            tl.every("opacity", [(0, 0), (1, 1), (2, 0)], 44, still=0, discrete=True),
        ]
        s = tl.sail(COURSE, 4, 24)
        parts.append(s.wrap("<path d='M0 0'/>"))
        doc = "".join(parts)
        self.assertNotIn("<animate", doc)
        self.assertNotIn("<set", doc)
        self.assertEqual(s.anim, "")
        self.assertEqual(s.transform, "translate(776 556)")      # anchored
        self.assertIn('transform="translate(20 20)"', doc)        # boat at the last fix
        self.assertNotIn('opacity="0"', doc)                      # nothing hidden in the still
        self.assertEqual(tl.report()["class"], "still")
        self.assertEqual(tl.prop("opacity", [0, 1], 0.4, 1.0), ('opacity="1"', ""))
        self.assertEqual(tl.prop("opacity", [1, 0], 0.4, 1.0, still=1), ('opacity="1"', ""))

    def test_loops_require_still(self):
        tl = T.Timeline("t", motion=False)
        with self.assertRaises(ValueError):   # rules hold in still mode too
            tl.every("opacity", [(0, 0), (1, 1, "settle")], 44, still=0)
        with self.assertRaises(ValueError):
            tl.anim("opacity", [1, 0], 4, 0, repeat="indefinite", key_times=[0, 0.5], discrete=True)
        with self.assertRaises(ValueError):
            tl.every("opacity", [(0, 1), (1, 0)], 0, discrete=True)

    def test_null_timeline(self):
        tl = T.NullTimeline("x")
        self.assertFalse(tl.motion)
        self.assertEqual(tl.flash("Fl 4s"), "")


class GridTests(unittest.TestCase):
    def test_off_grid_begin_snaps(self):
        tl = T.Timeline("t")
        a = tl.flash("Fl 4s", begin=2.3)
        self.assertIn('begin="2.5s"', a)
        self.assertEqual(tl.report()["snapped"][0]["to"], 2.5)
        r = tl.reveal("<g/>", 2.85)
        self.assertIn('begin="3s"', r)

    def test_off_grid_key_instant_raises(self):
        tl = T.Timeline("t")
        with self.assertRaises(ValueError):
            tl.anim("opacity", [1, 0], 4, 0, repeat="indefinite", key_times=[0, 0.1], discrete=True, still=1)
        with self.assertRaises(ValueError):
            tl.fixes([(0, 0), (1, 1)], 0, every=4.2)

    def test_continuous_one_shots_need_no_grid(self):
        tl = T.Timeline("t")
        a = tl.anim("opacity", [0, 1], 0.4, 2.3, ease="settle")
        self.assertIn('begin="2.3s"', a)
        self.assertEqual(tl.report()["snapped"], [])


class RuleTests(unittest.TestCase):
    def test_every_and_flash_are_the_only_indefinite_emitters(self):
        src = open(os.path.join(ROOT, "scripts", "timeline.py"), encoding="utf-8").read()
        # the literal lives in anim() once; every other path reaches it through repeat="indefinite"
        self.assertEqual(src.count('repeatCount="indefinite"'), 1)
        tl = T.Timeline("footer", ambient=True)
        tl.every("translate", [(0, "0 30"), (0.9, "0 0", "settle"), (1.5, "0 0"), (2.4, "0 30", "draw")], 44,
                 still="0 30", additive=True)
        tl.flash("Fl 4s")
        tl.fade_in("<g/>", 1)
        tl.draw_in('d="M0 0"')
        tl.sail("M0,0 L10,10", 0, 24)
        tl.reveal("<g/>", 1)
        r = tl.report()
        self.assertEqual(r["indefinite"], 2)
        self.assertEqual(r["class"], "ambient")
        self.assertEqual(r["repaints_per_s"], "continuous")

    def test_indefinite_only_on_opacity_transform(self):
        tl = T.Timeline("t", ambient=True)
        with self.assertRaises(ValueError):
            tl.anim("fill", ["#000", "#fff"], 4, 0, repeat="indefinite", still="#000", discrete=True)
        with self.assertRaises(ValueError):
            tl.every("stroke-dashoffset", [(0, 1), (2, 0, "draw")], 0, still=0)

    def test_continuous_loop_needs_ambient(self):
        tl = T.Timeline("hero")
        with self.assertRaises(ValueError):
            tl.every("translate", [(0, "0 0"), (5, "0 -2", "sea"), (10, "0 0", "sea")], 0, period=10, still="0 0")
        amb = T.Timeline("footer", ambient=True)
        a = amb.every("translate", [(0, "0 0"), (5, "0 -2", "sea"), (10, "0 0", "sea")], 0, period=10, still="0 0")
        self.assertIn('calcMode="spline"', a)
        self.assertIn('dur="10s"', a)

    def test_geometry_rules(self):
        tl = T.Timeline("t")
        with self.assertRaises(ValueError):
            tl.anim("cx", [0, 10], 4, 0, repeat="indefinite", still=0, discrete=True)
        tl.anim("stroke-dashoffset", [1, 0], 6, 0)       # too long: recorded, not raised
        self.assertTrue(any("stroke-dashoffset" in v for v in tl.report()["violations"]))
        ok = T.Timeline("t")
        ok.draw_in('d="M0 0"', dur=1.6, begin=0.2)
        self.assertEqual(ok.report()["violations"], [])

    def test_no_syncbase(self):
        tl = T.Timeline("t")
        with self.assertRaises(ValueError):
            tl.anim("opacity", [0, 1], 1, "arrive.end+0.4s")
        with self.assertRaises(ValueError):
            tl.reveal("<g/>", "x.end")
        self.assertIsNotNone(T.SYNCBASE.search('begin="arrive.end+0.4s"'))
        self.assertIsNone(T.SYNCBASE.search('begin="2.2s"'))

    def test_freeze_ins_have_base_opacity_zero(self):
        tl = T.Timeline("t")
        self.assertTrue(tl.fade_in("<g/>", 1).startswith('<g opacity="0">'))
        self.assertIn('opacity="0"', tl.reveal('<path d="M0 0"/>', 1))
        svg, end, times = tl.typed("ab c", 0, 0, "machine", 44, 7,
                                   glyphs=[("<use href='#a'/>", 8), ("<use href='#b'/>", 8), ("", 8), ("<use href='#c'/>", 8)])
        self.assertEqual(svg.count('opacity="0"'), 3)
        self.assertEqual(svg.count("<set"), 3)
        self.assertEqual(len(times), 4)
        self.assertGreater(times[3] - times[2], 0.16)           # +space after a space
        self.assertGreater(end, times[-1])

    def test_typed_is_deterministic(self):
        glyphs = [(f"<use href='#{c}'/>" if c != " " else "", 8) for c in "ls -la"]
        a = T.Timeline("t").typed("ls -la", 0, 0, "machine", 44, 3, glyphs=glyphs)
        b = T.Timeline("t").typed("ls -la", 0, 0, "machine", 44, 3, glyphs=glyphs)
        c = T.Timeline("t").typed("ls -la", 0, 0, "machine", 44, 4, glyphs=glyphs)
        self.assertEqual(a, b)
        self.assertNotEqual(a[2], c[2])


class SamplerTests(unittest.TestCase):
    def test_sample_path_cubic(self):
        pts = T.sample_path(CUBIC, 9)
        self.assertEqual(len(pts), 9)
        for p in pts:
            self.assertEqual(len(p), 3)
        x0, y0, h0 = pts[0]
        xn, yn, hn = pts[-1]
        self.assertAlmostEqual(x0, 0, places=6)
        self.assertAlmostEqual(xn, 150, places=6)
        self.assertAlmostEqual(yn, 0, places=6)
        self.assertGreater(h0, 0)                               # heading down the sheet at the start
        self.assertLess(hn, 0)                                  # back up at the end
        self.assertAlmostEqual(pts[4][0], 75, places=3)         # symmetric curve: midpoint at x=75
        # equal arc spacing
        import math
        d = [math.dist(pts[i][:2], pts[i + 1][:2]) for i in range(8)]
        self.assertLess(max(d) - min(d), 0.6)

    def test_sample_path_commands(self):
        for d in ("M0 0 L10 0 l0 10 H0 V0 Z", "M0,0 Q50,50 100,0", "m0 0 c10 10 20 10 30 0 s20 -10 30 0",
                  "M0 0 Q10 10 20 0 T40 0"):
            pts = T.sample_path(d, 5)
            self.assertEqual(len(pts), 5)
        with self.assertRaises(ValueError):
            T.sample_path("M0 0 A5 5 0 0 1 10 10", 3)
        self.assertAlmostEqual(T.path_length("M0 0 L3 4"), 5.0)


class ReportTests(unittest.TestCase):
    def test_hero_like_report(self):
        tl = T.Timeline("hero")
        for i in range(4):
            tl.draw_in('d="M0 0"', dur=1.6, begin=0.2 + 0.12 * i)
        tl.fade_in("<g/>", 1.6, 0.65)
        tl.xform("rotate", [12, -4, 0], 1.6, 2.0, ease="sea", key_times=[0, 0.45, 1])
        tl.reveal("<g/>", 2.6)
        tl.fade_in("<g/>", 3.6, 0.4)
        tl.flash("Fl G 4s", begin=0)
        tl.flash("Fl R 4s", begin=2)
        tl.sail(COURSE, 4, 24)
        r = tl.report()
        self.assertEqual(r["opening_end_s"], 4.0)
        self.assertEqual(r["indefinite"], 2)
        self.assertEqual(r["repaints_per_s"], 1.0)
        self.assertEqual(r["continuous_windows"][-1], [0.2, 28.0])   # T4 §2.7: hero window 0–28 s
        self.assertEqual(r["longest_loop_s"], 4)
        self.assertEqual(r["violations"], [])
        self.assertEqual(r["class"], "lights")
        self.assertEqual(tl.cue("opening", 0, 4.0), 4.0)
        self.assertEqual(tl.t("opening"), (0.0, 4.0))

    def test_tokens_are_the_source(self):
        self.assertEqual(T.LOOP_PERIODS, tuple(tokens.LOOP_PERIODS))
        self.assertEqual(T.QUANTUM, tokens.QUANTUM)
        self.assertEqual(T.EASE, tokens.EASE)


if __name__ == "__main__":
    unittest.main()
