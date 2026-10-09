"""tests/test_approaches.py — Sheet 3 (approaches): determinism, budgets, legend ⊇ used symbol ids,
honesty (no banned strings, "512" never printed, upright figures only where measured), frozen stills
and phones, the discrete motion plan, Region B buoyage on a 290° leading line, and T3 §10.7 (data
drives geometry). One build of the six editions is shared by the class."""
from __future__ import annotations

import gzip
import json
import math
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

import check  # noqa: E402,F401  (registers the Finding record the plug-ins import)
import build_assets as BA  # noqa: E402
import chartlib as c  # noqa: E402
import edition as E  # noqa: E402
import timeline as T  # noqa: E402
import tokens  # noqa: E402
import typeset as k  # noqa: E402
from checks import motion as motion_check  # noqa: E402
from checks import strings as strings_check  # noqa: E402
from sheets import approaches as A  # noqa: E402

ANIM_RE = re.compile(r"<(animate|animateTransform|animateMotion|set)\b")
USE_SYM_RE = re.compile(r'href="#approaches-c-sym-([a-z-]+)"')
ALLOWED_MEASURED_KEYS = {"chart-number", "edition", "scrapy_commits", "scrape_interval", "shards", "wheel",
                         "rows_stage1_discovery", "rows_stage2_page_analysis", "rows_stage4_summaries"}


def _gz(data: bytes) -> int:
    return len(gzip.compress(data, compresslevel=9, mtime=0))


def build_direct(ed_name: str = "day", log=None, data_patch=None):
    """Build one edition straight from the module (for the data → geometry tests)."""
    cfg = BA.load_cfg()
    data, _sha, _raw = BA.load_stats()
    log = BA.load_log(cfg) if log is None else log
    if data_patch:
        data = {**data, **data_patch}
    ed = E.EDITIONS[ed_name]
    k.begin_asset("approaches")
    tl = T.Timeline("approaches", motion=ed.motion)
    ctx = BA.Ctx(ed=ed, data=data, cfg=cfg, tl=tl, k=k, sheet="approaches", log=log, extra={"size": A.SIZES[ed.scale]})
    doc = A.build(ctx)
    return doc, k.run_records(), ctx


class Approaches(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="approaches-")
        cls.out = os.path.join(cls.tmp, "v9")
        cls.report_path = os.path.join(cls.tmp, "build-report.json")
        cls.problems = BA.main(sheets=["approaches"], out=cls.out, report_path=cls.report_path, quiet=True)
        with open(cls.report_path, encoding="utf-8") as fh:
            cls.rep = json.load(fh)
        cls.svgs = {}
        for name in E.EDITION_NAMES:
            with open(os.path.join(cls.out, f"approaches-{name}.svg"), "rb") as fh:
                cls.svgs[name] = fh.read()
        cls.cfg = BA.load_cfg()
        cls.stats, _s, _r = BA.load_stats()
        cls.log = BA.load_log(cls.cfg) or {}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def entry(self, name):
        return self.rep["sheets"][f"approaches-{name}"]

    def texts(self, name):
        return self.entry(name)["text"]

    # ------------------------------------------------------------- contract
    def test_contract_and_alt(self):
        self.assertEqual(A.NAME, "approaches")
        self.assertEqual(A.KIND, "chart")
        self.assertEqual(A.SIZES, {"desk": (1280, 892), "phone": (720, 1960)})
        self.assertTrue(A.BREAKS and all(len(b) == 3 for b in A.BREAKS))
        alt = A.alt(self.stats, self.cfg)
        self.assertLessEqual(len(alt.split()), 25, alt)
        self.assertFalse(alt.startswith("The"), alt)
        # true of every edition: the phone is rotated and its key is its own (no "east"/"west", no "every symbol")
        for word in ("east", "west", "legend"):
            self.assertNotIn(word, alt, alt)
        self.assertTrue(alt.endswith(self.cfg["alt"]["alt_poem"][2]), alt)   # the sheet's line of the poem

    def test_only_the_documented_glyph_budget_problems(self):
        """check_type is clean, bounds are clean, motion has no violations: the only build problems
        allowed are D's per-sheet glyph-library budget (reported as a deviation in P-report.md)."""
        others = [p for p in self.rep["problems"] if "type budget" not in p]
        self.assertEqual(others, [])

    def test_six_editions_sizes_and_budgets(self):
        self.assertEqual(set(self.rep["sheets"]), {f"approaches-{n}" for n in E.EDITION_NAMES})
        for name, data in self.svgs.items():
            e = self.entry(name)
            w, h = A.SIZES["phone" if "phone" in name else "desk"]
            self.assertEqual((e["w"], e["h"]), (w, h), name)
            self.assertIn(f'viewBox="0 0 {w} {h}"', data.decode(), name)
            self.assertLessEqual(len(data), tokens.BUDGETS["svg_kb"] * 1024, name)
            self.assertLessEqual(_gz(data), tokens.BUDGETS["targets_kb"]["approaches"][1] * 1024, name)
            if "phone" in name:
                self.assertLessEqual(len(data), tokens.BUDGETS["phone_svg_kb"] * 1024, name)
            self.assertLessEqual(e["elements"], tokens.BUDGETS["elements"], name)
            self.assertNotIn(E.STATS_SHA_PLACEHOLDER, data.decode(), name)

    def test_two_builds_are_byte_identical(self):
        out2 = os.path.join(self.tmp, "again")
        rep2 = os.path.join(self.tmp, "again.json")
        BA.main(sheets=["approaches"], editions=["day", "phone-night"], out=out2, report_path=rep2, quiet=True)
        for name in ("day", "phone-night"):
            with open(os.path.join(out2, f"approaches-{name}.svg"), "rb") as fh:
                self.assertEqual(fh.read(), self.svgs[name], name)

    # ------------------------------------------------------------- the legend
    def test_legend_defines_every_symbol_and_covers_every_use(self):
        # drawn things the legend plug-in allows; "correction" has no referent on any sheet, so no row (v9.2)
        every = set(c.SYMBOL_NAMES) - {"sloop", "sloop-glyph", "halo", "flare", "correction"}
        allow = {"sloop", "sloop-glyph", "halo", "flare"}
        for name, data in self.svgs.items():
            text = data.decode()
            used = set(USE_SYM_RE.findall(text))
            e = self.entry(name)
            self.assertTrue(used, name)
            if "phone" not in name:
                legend = set(e["legend"])
                self.assertEqual(legend, every, name)                    # the page's single legend
                self.assertTrue(used <= legend | allow, (name, used - legend - allow))   # legend ↔ sheet <use> diff
                self.assertEqual(set(e["symbols_used"]), used, name)     # the report names every href
            else:
                self.assertTrue(used <= every | allow, (name, used - every - allow))
                self.assertGreaterEqual(len(e["legend"]), 8, name)        # the phone carries its own compact legend
                self.assertNotIn("correction", used, name)
            # every symbol id a <use> points at is defined once in the file
            for sym in used:
                self.assertEqual(text.count(f'id="approaches-c-sym-{sym}"'), 1, (name, sym))

    # ------------------------------------------------------------- honesty
    def test_no_banned_strings_no_512_no_coverage(self):
        for name, data in self.svgs.items():
            text = data.decode()
            self.assertEqual([f.msg for f in strings_check.scan(text, name)], [], name)
            manifest = "\n".join(str(t["s"]) for t in self.texts(name))
            self.assertEqual([f.msg for f in strings_check.scan(manifest, name)], [], name)
            self.assertNotIn("512", manifest, name)
            self.assertIsNone(re.search(r"\d+\s*%", manifest), name)      # no coverage figure anywhere
            for t in self.texts(name):
                if "512" in t["s"]:
                    self.fail(f"{name}: 512 printed ({t['slant']})")

    def test_upright_figures_are_the_measured_ones(self):
        """Measured (truth=measured) runs carry one of the known keys or are the legend's example drawn
        from stats.json; every other sounding on the sheet is sloping (illustrative)."""
        scrapy = next(r for r in self.stats["repos"] if r["name"] == "Scrapy")
        for name in ("day", "night", "still-day"):
            upright_soundings = []
            for t in self.texts(name):
                if t.get("truth") == "measured":
                    if t.get("key") in ALLOWED_MEASURED_KEYS:
                        continue
                    self.assertEqual(t["origin"], "sounding", (name, t["s"]))
                    hw = max(w["n"] for w in self.stats["weeks"])
                    self.assertTrue(t["s"].startswith(str(scrapy["commits"])) or t["s"].startswith(str(hw)), (name, t["s"]))
                # nothing on any sheet is above datum, so nothing is underlined (v9.2)
                self.assertNotEqual(t.get("truth"), "datum", (name, t["s"]))
                if t["origin"] == "sounding" and t["slant"] == "upright":
                    upright_soundings.append(t["s"])
            # the legend's 265₅, the HW week and the upright sample (the real 265)
            self.assertLessEqual(len(upright_soundings), 3, (name, upright_soundings))
            self.assertTrue(all(s.startswith(str(scrapy["commits"])) or s.startswith(str(max(w["n"] for w in self.stats["weeks"])))
                                for s in upright_soundings), (name, upright_soundings))
            # the shard count is drawn (track lines, mole cells), never printed (v9.2: show, don't tell)
            self.assertEqual([t for t in self.texts(name) if t.get("key") == "shards"], [], name)
            # light characters: Grafana's goes upright only on a measured claim; the mole head's and the leading
            # lights' F are never measured and slope
            claim = (self.stats.get("claims") or {}).get("scrape_interval") or {}
            grafana = [t for t in self.texts(name) if t["s"].startswith("Fl ") and t["x0"] < 400]
            self.assertEqual(len(grafana), 1, (name, grafana))
            if claim.get("measured") and claim.get("sha"):
                self.assertEqual((grafana[0]["slant"], grafana[0].get("key"), grafana[0].get("truth")),
                                 ("upright", "scrape_interval", "measured"), name)
            else:
                self.assertEqual((grafana[0]["slant"], grafana[0].get("truth")), ("italic", "illustrative"), name)
            fs = [t for t in self.texts(name) if t["s"] == "F"]
            self.assertEqual(len(fs), 2, (name, fs))                       # the mole head and the leading line
            self.assertTrue(all(t["slant"] == "italic" and t.get("truth") == "illustrative" for t in fs), name)
            # the survey line slopes while no run is recorded
            srv = [t for t in self.texts(name) if t["s"].startswith("Surveyed by rustmapper")]
            self.assertEqual(len(srv), 1, name)
            self.assertEqual(srv[0]["slant"], "upright" if isinstance(self.stats.get("trial"), dict) else "italic", name)

    def test_legend_at_19_and_no_notes_or_captions(self):
        for name in ("day", "night"):
            recs = self.texts(name)
            legend = [r for r in recs if r["within"] == list(A.LEGEND) and r["role"] == "label"]
            self.assertGreaterEqual(len(legend), 30, name)
            # show, don't tell: the figure convention is two legend entries, not a sentence; the legend defines
            # every symbol used and nothing it does not use (v9.2)
            texts = {r["s"] for r in legend}
            for want in ("Upright · measured", "Sloping · not measured", "Obstn · reported obstruction",
                         "Inset · larger scale, Sheet 3", "Zone · seed source", "Track line · one shard"):
                self.assertIn(want, texts, (name, want))
            for gone in ("Underlined · above datum", "Correction · revised"):
                self.assertNotIn(gone, texts, (name, gone))
            self.assertFalse(any("upright figures are measured" in r["s"] for r in recs), name)
            self.assertTrue(all(r["size"] == A.PANEL_SIZE for r in legend), [(r["s"], r["size"]) for r in legend if r["size"] != A.PANEL_SIZE])
            # no notes panels and no captions: the README prints the facts once, the key decodes the marks
            manifest = "\n".join(r["s"] for r in recs)
            for gone in ("NOTES", "write-ahead log", "one shard per core", "Local knowledge advised",
                         "as declared by the site", "PyPI", "Frontier hashed"):
                self.assertNotIn(gone, manifest, (name, gone))
            self.assertIn("IALA Region B · marks numbered from seaward", manifest, name)
            self.assertFalse(hasattr(A, "BLOCK_RM"))

    def test_unit_line_once_and_one_label_caps(self):
        for name in ("day", "phone-day"):
            caps = [t for t in self.texts(name) if t["role"] == "label-caps"]
            self.assertEqual(len(caps), 1, (name, [t["s"] for t in caps]))
            self.assertEqual(caps[0]["s"], self.cfg["copy"]["unit_approaches"].upper())
            folio = [t for t in self.texts(name) if t.get("key") == "folio"]
            self.assertEqual(len(folio), 1, name)
            self.assertEqual(folio[0]["s"], f"CHART NO. {self.stats['repo_count']} · SHEET 3")   # no title repeat (v9.2)

    # ------------------------------------------------------------- motion
    def test_stills_and_phones_carry_no_animation(self):
        for name, data in self.svgs.items():
            if "still" in name or "phone" in name:
                self.assertIsNone(ANIM_RE.search(data.decode()), name)
                self.assertEqual(self.entry(name)["motion"]["indefinite"], 0, name)

    def test_motion_plan_is_discrete_and_within_budget(self):
        for name in ("day", "night"):
            text = self.svgs[name].decode()
            fails = [f for f in motion_check.scan(text, f"approaches-{name}.svg") if f.level in ("fail", "error")]
            self.assertEqual([f.msg for f in fails], [], name)
            m = self.entry(name)["motion"]
            self.assertEqual(m["class"], "lights", name)
            self.assertEqual(m["violations"], [], name)
            self.assertLessEqual(m["repaints_per_s"], 2.0, name)
            self.assertLessEqual(m["indefinite"], 10, name)
            self.assertEqual(m["longest_loop_s"], 96.0, name)
            self.assertEqual(m["continuous_windows"], [], name)        # nothing continuous on this sheet
            periods = {lp["period"] for lp in m["loops"]}
            self.assertTrue(periods <= set(float(p) for p in tokens.LOOP_PERIODS), periods)
            self.assertIn(4.0, periods)                                # Fl 4s outer pair
            self.assertIn(10.0, periods)                               # Fl(2) 10s entrance gate
            self.assertIn(96.0, periods)                               # the packet boat's 96 s plot
            self.assertNotIn("animateMotion", text)
            self.assertNotIn("<pattern", text)
            self.assertNotIn("<filter", text)
            # survey vessel: fixes at 28, 30 … 42 s; sounding k and WAL cell k <set> at fix k
            begins = sorted({float(b) for b in re.findall(r'<set[^>]*begin="([\d.]+)s"', text)})
            self.assertTrue({28.0 + 2 * i for i in range(8)} <= set(begins) | {28.0}, begins)
            self.assertTrue(all(abs(b / 0.5 - round(b / 0.5)) < 1e-6 for b in begins), begins)   # on the 0.5 s grid
            # the packet boat: seven fixes every 4 s on a 96 s period
            boat = re.search(r'id="approaches-packet"[^>]*begin="0s" dur="96s"[^>]*keyTimes="([^"]+)"', text)
            self.assertIsNotNone(boat, "packet boat animateTransform")
            kts = [round(float(x) * 96, 3) for x in boat.group(1).split(";")]
            self.assertEqual(kts, [0, 4, 8, 12, 16, 20, 24])
            # lights: four laterals + Grafana (main and inset) flash, reds begin at 2 s
            self.assertIn('id="approaches-lt-r2-fl"', text)
            r2 = re.search(r'id="approaches-lt-r2-fl"[^>]*begin="([\d.]+)s" dur="4s"', text)
            self.assertEqual(r2.group(1), "2")
            g1 = re.search(r'id="approaches-lt-g1-fl"[^>]*begin="([\d.]+)s" dur="4s"', text)
            self.assertEqual(g1.group(1), "0")
            si = (self.stats.get("claims") or {}).get("scrape_interval") or {}
            period = int(si["value"]) if si.get("measured") and si.get("value") is not None else 15   # the sheet's fallback
            self.assertRegex(text, rf'id="approaches-lt-grafana-fl"[^>]*dur="{period}s"')
            self.assertRegex(text, r'id="approaches-lt-g3-fl"[^>]*dur="10s"')
            self.assertRegex(text, r'id="approaches-lt-r4-fl"[^>]*dur="10s"')

    # ------------------------------------------------------------- chart grammar (T3 §10.3)
    def test_region_b_buoyage_on_a_290_leading_line(self):
        self.assertAlmostEqual(c.compass_bearing(A.W4, A.ANCH), A.LDG_BRG, delta=0.6)
        self.assertAlmostEqual(c.compass_bearing(A.W1, A.ANCH), A.LDG_BRG, delta=0.6)   # collinear inner legs
        # the leading marks sit on the line astern of the anchorage
        for pt in (A.LDG_FRONT, A.LDG_REAR):        # seen from seaward, the marks are in transit on 290°
            self.assertAlmostEqual(c.compass_bearing(A.W1, pt), A.LDG_BRG, delta=1.0)
        legs = [(A.W0, A.W1), (A.W1, A.W2), (A.W2, A.W3), (A.W3, A.W4)]
        for leg, (kind, side) in zip(legs, (("can", "port"), ("nun", "starboard"), ("can", "port"), ("nun", "starboard"))):
            mx, my = c.lateral_offset(leg, 0.5, side, 24)
            mid_y = (leg[0][1] + leg[1][1]) / 2
            brg = c.compass_bearing(*leg)
            self.assertTrue(270 <= brg <= 330, brg)
            if kind == "can":
                self.assertGreater(my, mid_y, "odd greens south of a channel heading WNW")
            else:
                self.assertLess(my, mid_y, "even reds north of a channel heading WNW")
        # the sheet says so in its labels
        s = "\n".join(t["s"] for t in self.texts("day"))
        for lab in ('G "1" URLS', 'R "2" SCOUT', 'G "3" ANALYZE', 'R "4" SUMMARIZE', "Health Ldg Lts 290°", "Fl G 4s", "Fl R 4s",
                    "Fl(2) G 10s", "Fl(2) R 10s"):
            self.assertIn(lab, s)
        self.assertIn("proposed · unlit", s)

    def test_chart_number_position_matches_the_series(self):
        for name in ("day", "night", "still-day"):
            cn = [t for t in self.texts(name) if t.get("key") == "chart-number"]
            self.assertEqual(len(cn), 1)
            self.assertEqual(cn[0]["s"], str(self.stats["repo_count"]))
            self.assertAlmostEqual(cn[0]["x1"], 1262, delta=0.6)   # anchor end at x 1262, decision 27
            self.assertEqual(cn[0]["y"], 19)
            folio = [t for t in self.texts(name) if t.get("key") == "folio"][0]
            self.assertEqual((round(folio["x0"]), folio["y"]), (24, A.SIZES["desk"][1] - 8))
            # both margin lines clear the outer rule by at least one PEN, and the margin holds a 19 px line + 6
            r0 = A.RULES["desk"][0]
            self.assertGreaterEqual(r0, 19 + 6)
            self.assertGreaterEqual(r0 - cn[0]["y"], tokens.W["PEN"])
            self.assertGreaterEqual(folio["y0"] - (A.SIZES["desk"][1] - r0), tokens.W["PEN"], (folio["y0"], A.SIZES["desk"][1] - r0))

    # ------------------------------------------------------------- data drives geometry (T3 §10.7)
    def test_shards_change_the_track_lines_and_the_tape(self):
        log = json.loads(json.dumps(self.log))
        log["profile"]["shards"] = 12
        doc, recs, ctx = build_direct("still-day", log=log)
        sh = A._Sheet(ctx)
        self.assertEqual(len(sh.survey_lines()), 12)
        self.assertEqual(doc.count('class="wal"'), 11 * 6 + 8)        # one mole block per sounding
        self.assertEqual([r for r in recs if r.get("key") == "shards"], [])   # drawn, not printed (v9.2)
        self.assertNotIn("12 here", "\n".join(r["s"] for r in recs))

    def test_scrape_interval_changes_the_light_character(self):
        claims = json.loads(json.dumps(self.stats["claims"]))
        claims["scrape_interval"] = {"value": 10, "unit": "s", "source": "Scrapy:monitoring/prometheus.yml", "sha": "abc", "measured": True}
        doc, recs, _ctx = build_direct("day", data_patch={"claims": claims})
        self.assertIn("Grafana Lt · ", [r["s"] for r in recs])
        self.assertRegex(doc, r'id="approaches-lt-grafana-fl"[^>]*dur="10s"')
        ch = [r for r in recs if r.get("key") == "scrape_interval"]
        self.assertEqual([(r["s"], r["slant"], r.get("truth")) for r in ch], [("Fl 10s", "upright", "measured")])
        # the guard: an unmeasured claim (or the fallback) letters the character sloping, with no key
        claims["scrape_interval"] = {"value": None, "unit": "s", "source": None, "sha": None, "measured": False}
        doc, recs, _ctx = build_direct("day", data_patch={"claims": claims})
        self.assertRegex(doc, r'id="approaches-lt-grafana-fl"[^>]*dur="15s"')
        ch = [r for r in recs if r["s"] == "Fl 15s"]
        self.assertEqual([(r["slant"], r.get("truth"), r.get("key")) for r in ch], [("italic", "illustrative", None)])

    def test_a_trial_export_makes_the_basin_soundings_upright(self):
        trial = {"date": "2026-10-01", "tables": {"stage1_discovery": {"rows": 12345, "version": 3},
                                                  "stage2_page_analysis": {"rows": 4200, "version": 2},
                                                  "stage4_summaries": {"rows": 900, "version": 1}}}
        _doc, recs, _ctx = build_direct("still-day", data_patch={"trial": trial})
        basin = [r for r in recs if r["origin"] == "sounding" and r["s"].startswith("12")]
        self.assertTrue(any(r["slant"] == "upright" and r["s"] == "12₃" for r in basin), [r["s"] for r in basin])
        # and the title block's survey line goes upright with it
        srv = [r for r in recs if r["s"].startswith("Surveyed by rustmapper")]
        self.assertEqual([r["slant"] for r in srv], ["upright"])

    def test_doubt_marks_agree_with_the_zoc_table(self):
        """Rep and ED in zone A (existence doubtful), SD on the zone B line (may not answer), nothing in C."""
        za, zb, zc = A.ZONE_Y["A"], A.ZONE_Y["B"], A.ZONE_Y["C"]
        self.assertLess(abs(A.REP[1] - A.ED_[1]), 4)
        self.assertLess(abs(A.REP[1] - za), (zb - za) / 2)
        self.assertLess(abs(A.SD[1] - zb), 12)
        for pt in (A.REP, A.ED_, A.SD):
            self.assertGreater(abs(pt[1] - zc), (zc - zb) / 2)

    def test_leading_marks_are_lights_and_wrecks_follow_the_data(self):
        scrapy = next(r for r in self.stats["repos"] if r["name"] == "Scrapy")
        for name in ("day", "night"):
            text = self.svgs[name].decode()
            ids = {lt["id"] for lt in self.entry(name)["lights"]}
            self.assertTrue({"lt-ldg-front", "lt-ldg-rear", "lt-mole", "lt-grafana"} <= ids, ids)
            self.assertEqual(sum(1 for lt in self.entry(name)["lights"] if lt["id"].startswith("lt-ldg")), 2)
            if name == "night":
                self.assertIn('id="approaches-lt-ldg-front-halo"', text)
            # one wreck per charted dead branch (plus the legend's sample), never more than two
            n = len(scrapy.get("stale_branches") or [])
            self.assertEqual(text.count('href="#approaches-c-sym-wreck"'), min(n, 2) + 1, name)
            for br in (scrapy.get("stale_branches") or [])[:2]:
                self.assertIn(str(br["last"])[:4][2:], "\n".join(t["s"] for t in self.texts(name) if t["s"].startswith("Wk")))
            # the leading line is cut under "Delta Lake": the path from the front mark has two pieces
            m = re.search(rf'<path d="(M{A.LDG_FRONT[0]} {A.LDG_FRONT[1]}L[^"]*)" fill="none" stroke="#[0-9A-Fa-f]{{6}}" stroke-width="2.1"', text)
            self.assertIsNotNone(m, "leading line")
            self.assertEqual(m.group(1).count("M"), 2, m.group(1))

    # ------------------------------------------------------------- phone (T3 §10.6)
    def test_phone_floors_and_kept_names(self):
        for name in ("phone-day", "phone-night"):
            recs = self.texts(name)
            self.assertTrue(recs)
            for r in recs:
                self.assertGreaterEqual(r["size"], tokens.FLOORS["phone"]["texture"], (name, r["s"], r["size"]))
                if r["semantic"]:
                    self.assertGreaterEqual(r["size"], tokens.FLOORS["phone"]["semantic"], (name, r["s"]))
            s = "\n".join(r["s"] for r in recs)
            for want in ("SCRAPY HARBOR", "Delta Lake", "UNSURVEYED", 'G "1"', 'R "2"', 'G "3"', 'R "4"', "Grafana Lt",
                         "LIMIT OF SURVEY 2026", "robots.txt", "Rep", "ED", "SD"):
                self.assertIn(want, s, (name, want))
            soundings = [r for r in recs if r["origin"] == "sounding" and r["y"] < A.PH_LEGEND_Y]   # on the water
            self.assertTrue(5 <= len(soundings) <= 8, len(soundings))             # thinned, not shrunk (v9.2)
            self.assertTrue(all(r["slant"] == "italic" for r in soundings))
            self.assertNotIn("upright figures measured", s)
            # the phone key defines every symbol the phone sheet draws (v9.2): 24 rows, the zone letters named
            key = [r for r in recs if r["y"] >= A.PH_LEGEND_Y and r["role"] == "label" and r["origin"] != "sounding"
                   and len(r["s"]) > 1 and r["s"] != "SYMBOLS" and r.get("key") != "folio"]
            self.assertEqual(len(key), 24, [r["s"] for r in key])
            texts = {r["s"] for r in key}
            for want in ("Zone · seed source", "sitemaps", "CT logs", "Common Crawl", "Fix · position", "Waypoint · stage",
                         "Track line · one shard", "Hatch · unsurveyed", "Tints · under 5, 10", "Height · commits, mos.",
                         "Upright · measured", "Sloping · not measured", "Ldg line · health check"):
                self.assertIn(want, texts, (name, want))
            # both columns stand 10 px inside the rules, and no row's text runs into the other column's glyph
            x_in = A.RULES["phone"][1] + A.PH_LEGEND_INSET
            self.assertTrue(all(r["x0"] >= x_in and r["x1"] <= 720 - x_in for r in key), name)
            left = [r for r in key if r["x0"] < 360]
            right_glyphs = [r for r in recs if r["y"] >= A.PH_LEGEND_Y and 340 < r["x0"] < 400 and r["origin"] == "sounding"]
            for g in right_glyphs:
                beside = [r for r in left if abs(r["y"] - g["y"]) < 6]
                self.assertTrue(all(r["x1"] < g["x0"] - 4 for r in beside), (name, g["s"], [r["s"] for r in beside]))
            # R "4"'s label stands above its mark, clear of the leading line; "429 Shoal" ends inside the rule
            shoal = next(r for r in recs if r["s"] == "429 Shoal")
            self.assertLessEqual(shoal["x1"], 720 - A.RULES["phone"][1] - 8)


if __name__ == "__main__":
    unittest.main()
