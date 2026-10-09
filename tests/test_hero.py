"""hero sheet (v11, round 5, D1): the coast of the year. Rows from the data with sweep days out, their order and
threshold, the merged row, the repositories with no non-sweep day, the one light (period from claims), the one
edition mark and its lettering in the water, the axis, honesty (nothing sloping, nothing unmeasured, no banned
words), phone floors, still editions, budgets, night weights, alt agreement, and the live-like stats file."""
from __future__ import annotations

import copy
import json
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
LIVE = os.environ.get("HERO_LIVE_STATS",
                      "/tmp/claude-0/-home-user-BenjaminSRussell/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/v92/live-stats.json")
BANNED = re.compile(
    r"SOUNDINGS|LIMIT OF SURVEY|UNSURVEYED|CHART NO|\bSHEET\b|SMALL CORRECTIONS|IALA|\bVAR\b|\bHW\b|ROCKS|CHARTED|"
    r"Harbor|Harbour|\bBank\b|Shoal|\bI\.$|sitemap\.xml lies|ILLUSTRATIVE|PENDING|SEEDED|NOT FOR NAVIGATION|"
    r"survey vessel|Fair winds|Here be dragons", re.I)
NO_SYMBOLS = ("sloop", "sloop-glyph", "anchorage", "can", "nun", "waypoint", "wreck", "station", "rock")
ANIM = re.compile(r"<(animate|animateTransform|set)\b")
ALL = tuple(E.EDITION_NAMES) + tuple(E.HERO_EXTRA)


def expected_rows(stats: dict, named_min: int, aliases: dict) -> tuple[list, list, list]:
    """Independent of the module: (named [(name, days)] ordered, small repos, zero repos) with every sweep day
    excluded for every repository."""
    sweeps = {s["date"] for s in stats.get("sweeps") or []} | set(stats.get("sweep_dates") or [])
    named, small, zero, seen = [], [], [], set()
    for r in stats["repos"]:
        if r["name"] in seen:
            continue
        seen.add(r["name"])
        days = len({d["d"] for d in r.get("days") or [] if d["d"] not in sweeps})
        name = aliases.get(r["name"], r["name"])
        (named if days >= named_min else small if days else zero).append((name, days, r["name"]))
    named.sort(key=lambda t: (-t[1], t[0].lower()))
    return named, small, zero


def _build(tmp, tag, stats=None, cfg_path=CFG, editions=None):
    out = os.path.join(tmp, tag)
    rep = os.path.join(tmp, f"{tag}.json")
    kw = {"stats_path": stats} if stats else {}
    n = build_assets.main(sheets=["hero"], editions=editions, out=out, report_path=rep, cfg_path=cfg_path,
                          quiet=True, **kw)
    with open(rep, encoding="utf-8") as fh:
        return n, json.load(fh), out


class HeroBuild(unittest.TestCase):
    """One build of every edition from the cached stats, shared by the tests below."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="hero-test-")
        cls.problems, cls.report, cls.out = _build(cls.tmp, "v9")
        cls.svg = {}
        for name in ALL:
            with open(os.path.join(cls.out, f"hero-{name}.svg"), encoding="utf-8") as fh:
                cls.svg[name] = fh.read()
        with open(STATS, encoding="utf-8") as fh:
            cls.stats = json.load(fh)
        with open(CFG, "rb") as fh:
            cls.cfg = tomllib.load(fh)
        cls.named_min = int(cls.cfg["hero"]["named_min"])
        cls.aliases = dict(cls.cfg["hero"].get("aliases", {}))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def entry(self, name):
        return self.report["sheets"][f"hero-{name}"]

    def texts(self, name):
        return self.entry(name)["text"]

    def write_stats(self, data, tag):
        p = os.path.join(self.tmp, f"{tag}.stats.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        return p

    # ---- contract and the build itself
    def test_contract(self):
        self.assertEqual(hero.NAME, "hero")
        self.assertEqual(hero.KIND, "chart")
        self.assertEqual(hero.SIZES["desk"][0], 1280)
        self.assertEqual(hero.SIZES["phone"][0], 720)
        self.assertTrue(590 <= hero.SIZES["desk"][1] <= 660, "desk 1280 × ~620")
        self.assertTrue(all(len(b) == 3 for b in hero.BREAKS))
        self.assertEqual(set(self.report["sheets"]), {f"hero-{n}" for n in ALL})

    def test_builds_clean_and_deterministic(self):
        self.assertEqual(self.problems, 0, self.report["problems"])
        n, _rep, again = _build(self.tmp, "again", editions=["day", "phone-night"])
        self.assertEqual(n, 0)
        for name in ("day", "phone-night"):
            with open(os.path.join(again, f"hero-{name}.svg"), encoding="utf-8") as fh:
                self.assertEqual(fh.read(), self.svg[name], f"hero-{name} differs between two builds")

    def test_refuses_to_invent_days(self):
        data = copy.deepcopy(self.stats)
        for r in data["repos"]:
            r.pop("days", None)
            r.pop("months", None)
        n, _rep, _out = _build(self.tmp, "nodays", self.write_stats(data, "nodays"), editions=["still-day"])
        self.assertGreaterEqual(n, 1)

    # ---- the rows: from the data, sweeps out, ordered, thresholded, merged
    def test_rows_from_data_with_sweeps_out(self):
        named, small, zero = expected_rows(self.stats, self.named_min, self.aliases)
        for name in ("day", "phone-day", "night"):
            h = self.entry(name)["hero"]
            rows = [r for r in h["rows"] if not r["more"]]
            self.assertEqual([(r["name"], r["days"]) for r in rows], [(n, d) for n, d, _ in named], name)
            for r in rows:
                self.assertEqual(sum(r["months"].values()), r["days"])
            more = [r for r in h["rows"] if r["more"]]
            self.assertEqual(len(more), 1 if small else 0)
            if small:
                self.assertEqual(more[0]["name"], f"{len(small)} more")
                self.assertEqual(more[0]["days"], sum(d for _n, d, _r in small))
                self.assertEqual(sorted(more[0]["repos"]), sorted(r for _n, _d, r in small))
            self.assertEqual(sorted(h["zero"]), sorted(r for _n, _d, r in zero))
            self.assertEqual(h["counts"]["repositories"], self.stats["repo_count"])
        # today's figures (7 Oct cache): the brief's numbers, sweeps out
        days = {r["name"]: r["days"] for r in self.entry("day")["hero"]["rows"]}
        self.assertEqual(days["Scrapy"], 24)
        self.assertEqual(days["rustmapper"], 19)
        self.assertEqual(days["Data_science_dev"], 10)
        scrapy = next(r for r in self.entry("day")["hero"]["rows"] if r["repo"] == "Scrapy")
        self.assertEqual((scrapy["first_ns"], scrapy["last_ns"]), ("2025-09-25", "2026-09-21"))
        self.assertNotIn("2026-10", scrapy["months"], "the 7 Oct sweep is not Scrapy's work")

    def test_threshold_gives_six_to_nine_rows(self):
        rows = self.entry("day")["hero"]["rows"]
        self.assertTrue(6 <= len(rows) <= 9, len(rows))
        self.assertEqual(self.entry("day")["hero"]["named_min"], self.named_min)
        for r in rows:
            if not r["more"]:
                self.assertGreaterEqual(r["days"], self.named_min)

    def test_named_min_is_read_from_chart_toml(self):
        with open(CFG, encoding="utf-8") as fh:
            text = fh.read()
        p = os.path.join(self.tmp, "cfg7.toml")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(re.sub(r"(?m)^named_min = \d+", "named_min = 7", text))
        n, rep, _out = _build(self.tmp, "nm7", cfg_path=p, editions=["day"])
        self.assertEqual(n, 0)
        rows = rep["sheets"]["hero-day"]["hero"]["rows"]
        self.assertEqual([r["name"] for r in rows if not r["more"]],
                         ["Scrapy", "rustmapper", "Data_science_dev", "BenjaminSRussell", "game_engine"])

    def test_repo_with_no_non_sweep_day_is_not_land(self):
        data = copy.deepcopy(self.stats)
        sweeps = [s["date"] for s in data["sweeps"]]
        ghost = copy.deepcopy(next(r for r in data["repos"] if r["name"] == "Wheel"))
        ghost["name"] = "Ghost_repo"
        ghost["days"] = [{"d": d, "h": 12, "n": 40} for d in sweeps]     # busy, but only on sweep days
        ghost["commit_days"] = len(sweeps)
        data["repos"].append(ghost)
        n, rep, _out = _build(self.tmp, "ghost", self.write_stats(data, "ghost"), editions=["day"])
        self.assertEqual(n, 0)
        h = rep["sheets"]["hero-day"]["hero"]
        self.assertIn("Ghost_repo", h["zero"])
        self.assertFalse(any(r["repo"] == "Ghost_repo" or "Ghost_repo" in (r["repos"] or []) for r in h["rows"]))
        self.assertNotIn("GHOST_REPO", [t["s"] for t in rep["sheets"]["hero-day"]["text"]])

    def test_data_builder_keys_are_read_when_present(self):
        """repos[].months / first_ns / last_ns from build_stats draw the same sheet as the sheet's own count."""
        data = copy.deepcopy(self.stats)
        sweeps = {s["date"] for s in data["sweeps"]}
        for r in data["repos"]:
            days = sorted(d["d"] for d in r.get("days") or [] if d["d"] not in sweeps)
            months = {}
            for d in days:
                months[d[:7]] = months.get(d[:7], 0) + 1
            r["months"], r["first_ns"], r["last_ns"] = months, (days[0] if days else None), (days[-1] if days else None)
        n, rep, out = _build(self.tmp, "keyed", self.write_stats(data, "keyed"), editions=["day"])
        self.assertEqual(n, 0)
        with open(os.path.join(out, "hero-day.svg"), encoding="utf-8") as fh:
            keyed = fh.read()
        self.assertEqual(keyed.split("\n", 2)[2], self.svg["day"].split("\n", 2)[2])
        # and the keys win: a months record the days do not show is what is drawn
        r = next(r for r in data["repos"] if r["name"] == "game_engine")
        r["months"] = {"2026-01": 8, "2026-03": 4}
        n, rep, _out = _build(self.tmp, "keyed2", self.write_stats(data, "keyed2"), editions=["day"])
        ge = next(x for x in rep["sheets"]["hero-day"]["hero"]["rows"] if x["repo"] == "game_engine")
        self.assertEqual(ge["months"], {"2026-01": 8, "2026-03": 4})

    def test_rows_never_overlap(self):
        for name in ("day", "phone-day"):
            h = self.entry(name)["hero"]
            spec = hero.ROWS["phone" if "phone" in name else "desk"]
            for r in h["rows"]:
                top, bottom = r["band"]
                for b in r["blocks"]:
                    self.assertGreaterEqual(b["top"], top + spec["label_dy"] + 4, f"{name} {r['name']}: bank meets its name")
                    self.assertLessEqual(b["bottom"], bottom - spec["gap"] + 1.5, f"{name} {r['name']}")
                    self.assertGreaterEqual(b["x0"], h["axis"]["x0"] - 0.5)
                    self.assertLessEqual(b["x1"], h["axis"]["x_end"] + 0.5)
            # the gap below a bank (to the next name) is wider than the gap from a name to its bank
            self.assertGreater(spec["gap"] + spec["label_dy"] - tokens.ROLES["phone" if "phone" in name else "desk"]["label"][1] * 0.75,
                               spec["bank_dy"] - spec["label_dy"])
            for a, b in zip(h["rows"], h["rows"][1:]):
                self.assertLessEqual(a["band"][1], b["band"][0] + 0.01)

    def test_thickness_is_one_scale_and_steps_down(self):
        data = copy.deepcopy(self.stats)
        r = next(r for r in data["repos"] if r["name"] == "Scrapy")
        r["days"] = list(r["days"]) + [{"d": f"2026-03-{d:02d}", "h": 12, "n": 1} for d in range(1, 31)]
        n, rep, _out = _build(self.tmp, "busy", self.write_stats(data, "busy"), editions=["day"])
        self.assertEqual(n, 0)
        s0 = self.entry("day")["hero"]["scale"]
        s1 = rep["sheets"]["hero-day"]["hero"]["scale"]
        self.assertEqual(s1["max_month"], 30)
        self.assertLess(s1["half_px_per_day"], s0["half_px_per_day"])
        self.assertAlmostEqual(s1["half_px_per_day"] * 30, s1["half_max"], delta=0.05)

    # ---- the axis
    def test_axis_runs_to_the_survey_date(self):
        for name in ("day", "phone-day"):
            h = self.entry(name)["hero"]
            self.assertEqual(h["axis"]["start"], "2025-09-01")
            self.assertEqual(h["axis"]["end"], self.stats["taken"])
            self.assertEqual(h["axis"]["letters"], "SONDJFMAMJJASO")
            self.assertEqual(h["axis"]["years"], [2025, 2026])
            years = [t for t in self.texts(name) if (t["key"] or "").startswith("year:")]
            self.assertEqual([t["s"] for t in years], ["2025", "2026"])
            w = hero.SIZES["phone" if "phone" in name else "desk"][0]
            for t in self.texts(name):
                self.assertLessEqual(t["x1"], w - hero.RULES["phone" if "phone" in name else "desk"][1] + 0.5
                                     if t["key"] != "imprint" else w, f"{name}: {t['s']!r} lettered beyond the survey date")

    # ---- the light and the mark
    def test_one_light_period_from_claims(self):
        period = int(self.stats["claims"]["scrape_interval"]["value"])
        for name in ("day", "night", "phone-day", "phone-night"):
            e = self.entry(name)
            self.assertEqual(len(e["lights"]), 1, name)
            lt = e["lights"][0]
            self.assertEqual(lt["character"], f"Fl {period}s")
            self.assertEqual(lt["row"], "Scrapy")
            svg = self.svg[name]
            self.assertEqual(svg.count('repeatCount="indefinite"'), 1, name)
            self.assertIn(f'dur="{period}s"', svg)
            m = e["motion"]
            self.assertEqual(m["indefinite"], 1)
            self.assertEqual(m["opening_end_s"], 0.0)
            self.assertEqual(m["violations"], [])
            self.assertEqual(m["continuous_windows"], [])
            chars = [t for t in e["text"] if t["key"] == "light"]
            self.assertEqual([t["s"] for t in chars], [f"Fl {period}s"])
        # the period is the claim's, not a constant
        data = copy.deepcopy(self.stats)
        data["claims"]["scrape_interval"]["value"] = 10
        n, rep, out = _build(self.tmp, "fl10", self.write_stats(data, "fl10"), editions=["day"])
        self.assertEqual(n, 0)
        self.assertEqual(rep["sheets"]["hero-day"]["lights"][0]["character"], "Fl 10s")
        # an unmeasured claim draws no light
        data["claims"]["scrape_interval"]["measured"] = False
        n, rep, _out = _build(self.tmp, "nolight", self.write_stats(data, "nolight"), editions=["day"])
        self.assertEqual(n, 0)
        self.assertEqual(rep["sheets"]["hero-day"]["lights"], [])

    def test_one_edition_mark_in_the_water(self):
        ed = self.stats["edition"]
        for name in ("day", "phone-day"):
            e = self.entry(name)
            marks = [t for t in e["text"] if t["key"] == "edition"]
            self.assertEqual([t["s"] for t in marks], [f"{ed['version']} · PyPI"])
            mk = e["hero"]["mark"]
            self.assertEqual((mk["row"], mk["date"]), ("Rust-sitemap", ed["date"]))
            for p in e["hero"]["placements"]:
                self.assertGreaterEqual(p["clear"], hero.CLEAR, f"{name}: {p['text']} sits on a coast")
                self.assertIn(p["side"], ("right", "left"))

    def test_no_theme_symbols(self):
        for name, svg in self.svg.items():
            body = svg.split("</defs>", 1)[1]
            for sym in NO_SYMBOLS:
                self.assertNotIn(f'href="#hero-h-sym-{sym}"', body, f"{name}: {sym}")

    # ---- honesty: strings, slant, still editions
    def test_no_banned_strings(self):
        for name, svg in self.svg.items():
            for bad in ("<text", "<tspan", "<textPath", "<pattern", "<filter", "animateMotion", "<script", "<image"):
                self.assertNotIn(bad, svg, f"{name}: {bad}")
            texts = [t["s"] for t in self.texts(name)]
            for s in texts:
                self.assertIsNone(BANNED.search(s), f"{name}: {s!r}")
            datum = [s for s in texts if "DATUM" in s.upper()]
            self.assertEqual(len(datum), 1, name)
            self.assertEqual(datum[0].count("DATUM"), 1)
            self.assertIn("DATUM: MAIN", datum[0])
            self.assertIsNone(BANNED.search(self.entry(name)["alt"]))

    def test_nothing_sloping_nothing_unmeasured(self):
        for name in ALL:
            for t in self.texts(name):
                if any(ch.isdigit() for ch in t["s"]):
                    self.assertEqual(t["slant"], "upright", f"{name}: sloping figure {t['s']!r}")
                    self.assertEqual(t["truth"], "measured", f"{name}: unmeasured figure {t['s']!r}")
                if t["truth"] is not None:
                    self.assertEqual(t["truth"], "measured")
        texts = [t["s"] for t in self.texts("day")]
        n = self.stats["repo_count"]
        self.assertIn(f"{n} REPOSITORIES · AUTHOR'S COMMITS", texts)
        self.assertIn("DATUM: MAIN · SWEEP DAYS EXCLUDED", texts)
        self.assertIn("7 OCT 2026 · EASTERN TIME", texts)
        self.assertIn("CRAWL AND DATA INFRASTRUCTURE", texts)
        self.assertIn("GITHUB.COM/BENJAMINSRUSSELL · 7 OCT 2026", texts)
        self.assertEqual(sum(1 for s in texts if s in ("Ben", "Russell")), 2)
        phone = [t["s"] for t in self.texts("phone-day")]
        self.assertFalse(any(s.startswith("GITHUB.COM") for s in phone), "no imprint line on the phone")
        self.assertIn("CRAWL AND DATA INFRASTRUCTURE · PYTHON AND RUST", phone)

    def test_row_names_as_written(self):
        names = {t["s"] for t in self.texts("day") if (t["key"] or "").startswith("row:")}
        self.assertIn("RUSTMAPPER", names)
        self.assertIn("SCRAPY", names)
        self.assertIn("DATA_SCIENCE_DEV", names)
        self.assertNotIn("RUST-SITEMAP", names)
        tags = [t["s"] for t in self.texts("day") if t["s"] in ("PYTHON", "RUST")]
        self.assertEqual(sorted(tags), ["PYTHON", "RUST"], "language tags where the data knows them")

    def test_type_floors(self):
        for name in ALL:
            sc = "phone" if "phone" in name else "desk"
            for t in self.texts(name):
                self.assertGreaterEqual(t["size"], tokens.FLOORS[sc]["semantic"], f"{name}: {t['s']!r} {t['size']}")
        for t in self.texts("phone-day"):
            self.assertGreaterEqual(t["size"], 26, "nothing under 26 px sheet type on the phone (13 px on screen)")

    def test_still_editions_are_frozen_finished_sheets(self):
        for name in ALL:
            if "still" in name:
                self.assertIsNone(ANIM.search(self.svg[name]), name)
                self.assertEqual(self.entry(name)["motion"]["class"], "still")
        self.assertEqual(sorted(t["s"] for t in self.texts("day")), sorted(t["s"] for t in self.texts("still-day")))
        self.assertIn('id="hero-light-lit"', self.svg["still-day"], "the still edition's light is lit")

    # ---- budgets and night
    def test_budgets(self):
        target_raw, target_gz = tokens.BUDGETS["targets_kb"]["hero"]
        for name in ALL:
            e = self.entry(name)
            self.assertLessEqual(e["elements"], tokens.BUDGETS["elements"], name)
            self.assertLessEqual(e["bytes"], target_raw * 1024, f"{name}: {e['bytes']} B raw")
            self.assertLessEqual(e["gz"], target_gz * 1024, f"{name}: {e['gz']} B gz")
            if name.startswith("phone"):
                self.assertLessEqual(e["bytes"], tokens.BUDGETS["phone_svg_kb"] * 1024, name)

    def test_night_redrawn_not_swapped(self):
        for name in ALL:
            widths = {float(w) for w in re.findall(r'stroke-width="([\d.]+)"', self.svg[name])}
            allowed = set(tokens.W_NIGHT.values() if "night" in name else tokens.W.values()) | {0.22, 0.18}
            self.assertTrue(widths <= allowed, f"{name}: {widths - allowed}")
        import chartlib as c
        self.assertEqual(c.weight_factor(), 1.0, "the night factor is reset after the build")

    # ---- alt
    def test_alt_is_short_plain_and_agrees_with_chart_toml(self):
        alt = hero.alt(self.stats, build_assets.load_cfg(CFG))
        self.assertLessEqual(len(alt.split()), 25)
        self.assertFalse(alt.lower().startswith("the"))
        self.assertIn(f"{self.stats['repo_count']} repositories", alt)
        self.assertIn("Scrapy and rustmapper", alt)
        last = alt.rsplit(". ", 1)[-1]
        self.assertEqual(last, self.cfg["alt"]["alt_poem"][0])
        self.assertTrue(self.cfg["alt"]["hero"].endswith(last))
        self.assertIn("coastline", self.cfg["alt"]["hero"])

    # ---- the live-like stats file (the second gate)
    @unittest.skipUnless(os.path.exists(LIVE), "live-like stats file not present")
    def test_live_like_stats_build_clean(self):
        n, rep, _out = _build(self.tmp, "live", LIVE)
        self.assertEqual(n, 0, rep["problems"])
        h = rep["sheets"]["hero-day"]["hero"]
        names = [r["name"] for r in h["rows"]]
        self.assertEqual(len(names), len(set(names)), "a repository listed twice is drawn once")
        for e in rep["sheets"].values():
            for p in e["hero"]["placements"]:
                self.assertGreaterEqual(p["clear"], hero.CLEAR)


if __name__ == "__main__":
    unittest.main()
