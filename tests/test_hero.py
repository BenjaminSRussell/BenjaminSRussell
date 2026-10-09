"""hero sheet (v11, round 5, D1 + F1): the coast of the year, by the week. Rows from the data with sweep days out,
their order and threshold, the profile repository merged, rows + N = repo_count, weekly banks on one scale (the
busiest week 0.8 of the band, a one-day week an islet), shallows along every coast, a figure and a language on every
named row, the one light (period from claims, on the latest bank), the one edition mark, mark lettering in the
water, the axis ending at the survey date inside the border, honesty (nothing sloping, nothing unmeasured, no banned
words), floors and the phone hierarchy, still editions, budgets, night weights, alt agreement, live-like stats."""
from __future__ import annotations

import copy
import datetime as dt
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
    r"survey vessel|Fair winds|Here be dragons|AUTHOR'S COMMITS|SWEEP|coastline", re.I)
NO_SYMBOLS = ("sloop", "sloop-glyph", "anchorage", "can", "nun", "waypoint", "wreck", "station", "rock")
ANIM = re.compile(r"<(animate|animateTransform|set)\b")
ALL = tuple(E.EDITION_NAMES) + tuple(E.HERO_EXTRA)


def expected_rows(stats: dict, named_min: int, aliases: dict) -> tuple[list, list]:
    """Independent of the module: (named [(name, days, repo)] ordered, rest [repo]) with every sweep day excluded for
    every repository and the profile repository never named."""
    sweeps = {s["date"] for s in stats.get("sweeps") or []} | set(stats.get("sweep_dates") or [])
    named, rest = [], []
    for r in stats["repos"]:
        days = len({d["d"] for d in r.get("days") or [] if d["d"] not in sweeps})
        if days >= named_min and r["name"] != stats["login"]:
            named.append((aliases.get(r["name"], r["name"]), days, r["name"]))
        else:
            rest.append(r["name"])
    named.sort(key=lambda t: (-t[1], t[0].lower()))
    return named, rest


def _build(tmp, tag, stats=None, cfg_path=CFG, editions=None):
    out = os.path.join(tmp, tag)
    rep = os.path.join(tmp, f"{tag}.json")
    kw = {"stats_path": stats} if stats else {}
    n = build_assets.main(sheets=["hero"], editions=editions, out=out, report_path=rep, cfg_path=cfg_path,
                          quiet=True, **kw)
    with open(rep, encoding="utf-8") as fh:
        return n, json.load(fh), out


class HeroBuild(unittest.TestCase):
    """One build of every edition from the committed stats, shared by the tests below."""

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
        cls.taken = dt.date.fromisoformat(cls.stats["taken"][:10])

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
        n, _rep, _out = _build(self.tmp, "nodays", self.write_stats(data, "nodays"), editions=["still-day"])
        self.assertGreaterEqual(n, 1)

    # ---- the rows: from the data, sweeps out, the profile merged, adding up to the repository count
    def test_rows_from_data_and_they_add_up(self):
        named, rest = expected_rows(self.stats, self.named_min, self.aliases)
        for name in ("day", "phone-day", "night"):
            h = self.entry(name)["hero"]
            rows = [r for r in h["rows"] if not r["more"]]
            self.assertEqual([(r["name"], r["days"]) for r in rows], [(n, d) for n, d, _ in named], name)
            for r in rows:
                self.assertEqual(sum(r["weeks"]), r["days"], f"{name}: {r['name']} weeks add up to its days")
            more = [r for r in h["rows"] if r["more"]]
            self.assertEqual(len(more), 1)
            n_more = self.stats["repo_count"] - len(rows)
            self.assertEqual(more[0]["name"], f"{n_more} more")
            self.assertEqual(len(rows) + more[0]["n"], self.stats["repo_count"], "named rows + N = repo_count")
            self.assertEqual(sorted(more[0]["repos"]), sorted(rest))
            self.assertIn(self.stats["login"], more[0]["repos"], "the profile repository joins the last row")
            self.assertTrue(max(more[0]["weeks"]) <= 7, "a merged week counts a calendar day once")
        texts = [t["s"] for t in self.texts("day")]
        self.assertIn(f"{self.stats['repo_count'] - len(named)} MORE", texts)
        self.assertNotIn(self.stats["login"].upper(), texts)
        # on the committed data: the six named rows
        self.assertEqual([n for n, _d, _r in named],
                         ["Scrapy", "rustmapper", "Data_science_dev", "game_engine", "Wheel", "Data-visualizer"])
        scrapy = next(r for r in self.entry("day")["hero"]["rows"] if r["repo"] == "Scrapy")
        self.assertEqual(scrapy["first_ns"], "2025-09-25")
        self.assertNotIn(scrapy["last_ns"], self.stats.get("sweep_dates") or [])

    def test_named_min_is_read_from_chart_toml(self):
        with open(CFG, encoding="utf-8") as fh:
            text = fh.read()
        p = os.path.join(self.tmp, "cfg7.toml")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(re.sub(r"(?m)^named_min = \d+", "named_min = 7", text))
        n, rep, _out = _build(self.tmp, "nm7", cfg_path=p, editions=["day"])
        self.assertEqual(n, 0)
        rows = rep["sheets"]["hero-day"]["hero"]["rows"]
        named = [r["name"] for r in rows if not r["more"]]
        self.assertEqual(named, [n for n, _d, _r in expected_rows(self.stats, 7, self.aliases)[0]])
        self.assertEqual(len(named) + rows[-1]["n"], self.stats["repo_count"])

    def test_repo_with_no_non_sweep_day_is_not_land(self):
        data = copy.deepcopy(self.stats)
        sweeps = [s["date"] for s in data["sweeps"]]
        ghost = copy.deepcopy(next(r for r in data["repos"] if r["name"] == "Wheel"))
        ghost["name"] = "Ghost_repo"
        ghost["days"] = [{"d": d, "h": 12, "n": 40} for d in sweeps]     # busy, but only on sweep days
        data["repos"].append(ghost)
        data["repo_count"] += 1
        n, rep, _out = _build(self.tmp, "ghost", self.write_stats(data, "ghost"), editions=["day"])
        self.assertEqual(n, 0)
        h = rep["sheets"]["hero-day"]["hero"]
        self.assertIn("Ghost_repo", h["zero"])
        more = h["rows"][-1]
        self.assertIn("Ghost_repo", more["repos"], "counted in the last row")
        self.assertEqual(more["weeks"], self.entry("day")["hero"]["rows"][-1]["weeks"], "but drawn as no land")
        self.assertFalse(any(r["repo"] == "Ghost_repo" for r in h["rows"]))

    # ---- the banks: weekly, one scale, islets, never overlapping
    def test_weekly_bins_one_scale(self):
        for name in ("day", "phone-day"):
            h = self.entry(name)["hero"]
            sc = h["scale"]
            self.assertLessEqual(sc["max_week"], 7)
            self.assertAlmostEqual(sc["half_max"] * 2, hero.FILL * sc["band"], delta=0.2, msg="busiest week 0.8 of the band")
            self.assertAlmostEqual(sc["half_px_per_day"] * sc["max_week"], sc["half_max"], delta=0.05)
            ax = h["axis"]
            self.assertEqual(ax["start"], "2025-09-01")
            self.assertEqual(dt.date.fromisoformat(ax["start"]).weekday(), 0, "ISO weeks start on Monday")
            self.assertEqual(ax["weeks"], (self.taken - dt.date(2025, 9, 1)).days // 7 + 1)
            for r in h["rows"]:
                self.assertEqual(len(r["weeks"]), ax["weeks"])
                for b in r["blocks"]:
                    w0, w1 = b["weeks"]
                    self.assertTrue(all(r["weeks"][i] > 0 for i in range(w0, w1 + 1)), "land only in weeks with days")
                    self.assertTrue(w0 == 0 or r["weeks"][w0 - 1] == 0)
                    width = b["x1"] - b["x0"]
                    self.assertLessEqual(width, (w1 - w0 + 1) * ax["week_px"] + 0.6, "land for those weeks only")
                    thick = b["bottom"] - b["top"]
                    peak = max(r["weeks"][w0:w1 + 1])
                    self.assertAlmostEqual(thick, 2 * sc["half_px_per_day"] * peak, delta=2.0,
                                           msg=f"{name} {r['name']}: thickness linear in days")
            # a one-day week is an islet: about a week wide, a day thick, no floor
            islets = [b for r in h["rows"] for b in r["blocks"] if b["weeks"][0] == b["weeks"][1]
                      and r["weeks"][b["weeks"][0]] == 1]
            self.assertTrue(islets)
            for b in islets:
                self.assertLessEqual(b["bottom"] - b["top"], 2 * sc["half_px_per_day"] + 2)

    def test_rows_never_overlap(self):
        for name in ("day", "phone-day"):
            h = self.entry(name)["hero"]
            spec = hero.ROWS["phone" if "phone" in name else "desk"]
            lbl = tokens.ROLES["phone" if "phone" in name else "desk"]["label"][1]
            for r in h["rows"]:
                top, bottom = r["band"]
                for b in r["blocks"]:
                    self.assertGreaterEqual(b["top"], top + spec["bank_dy"] - 0.5, f"{name} {r['name']}")
                    self.assertLessEqual(b["bottom"], bottom - spec["gap"] + 0.5, f"{name} {r['name']}")
                    self.assertGreaterEqual(b["x0"], h["axis"]["x0"] - 0.5)
                    self.assertLessEqual(b["x1"], h["axis"]["x_end"] + 0.5)
            for a, b in zip(h["rows"], h["rows"][1:]):
                self.assertLessEqual(a["band"][1], b["band"][0] + 0.01)
            if spec["name_dy"] is not None:   # phone: a bank is nearer its own name than the next row's
                own = spec["bank_dy"] - spec["name_dy"]
                nxt = spec["gap"] + spec["name_dy"] - lbl * 0.75
                self.assertGreater(nxt, own)

    def test_shallows_along_every_coast(self):
        th = tokens.THEMES
        for name in ("day", "night", "phone-day", "phone-night"):
            t = th["night" if "night" in name else "day"]
            body = self.svg[name].split("</defs>", 1)[1]
            self.assertIn(f'fill="{t.shallow_a}"', body, name)
            self.assertIn(f'fill="{t.shallow_b}"', body, name)
            self.assertLess(body.index(f'fill="{t.shallow_a}"'), body.index(f'fill="{t.land}"'), "shallows under the land")
        import checks.contrast as contrast
        for t in th.values():
            self.assertGreaterEqual(contrast.de_ok(t.shallow_a, t.land), 0.04)
            self.assertGreaterEqual(contrast.de_ok(t.shallow_b, t.land), 0.04)

    # ---- the row lettering
    def test_figure_and_language_on_every_named_row(self):
        for name in ("day", "phone-day"):
            h = self.entry(name)["hero"]
            texts = self.texts(name)
            rows = [r for r in h["rows"] if not r["more"]]
            for i, r in enumerate(rows):
                fig = [t for t in texts if t["key"] == f"days:{r['repo']}"]
                self.assertEqual(len(fig), 1)
                self.assertEqual(fig[0]["s"], f"{r['days']} DAYS" if i == 0 else str(r["days"]))
                self.assertEqual((fig[0]["truth"], fig[0]["slant"]), ("measured", "upright"))
                rec = next(x for x in self.stats["repos"] if x["name"] == r["repo"])
                want = rec.get("main_language") or max(rec["lines"], key=rec["lines"].get)
                tag = [t for t in texts if t["key"] == f"lang:{r['repo']}"]
                self.assertEqual([t["s"] for t in tag], [want.upper()], f"{name}: {r['name']}")
            more = [t for t in texts if t["key"] == "days:more"]
            self.assertEqual(len(more), 1)
            self.assertEqual(sum(1 for t in texts if t["s"].endswith(" DAYS")), 1, "DAYS after the first figure only")
        names = {t["s"] for t in self.texts("day") if (t["key"] or "").startswith("row:")}
        self.assertIn("RUSTMAPPER", names)
        self.assertNotIn("RUST-SITEMAP", names)

    def test_language_falls_back_to_lines_never_rest(self):
        data = copy.deepcopy(self.stats)
        for r in data["repos"]:
            r.pop("main_language", None)
            r["language"] = "COBOL"
        n, rep, _out = _build(self.tmp, "lang", self.write_stats(data, "lang"), editions=["day"])
        self.assertEqual(n, 0)
        tags = {t["key"]: t["s"] for t in rep["sheets"]["hero-day"]["text"] if (t["key"] or "").startswith("lang:")}
        self.assertNotIn("COBOL", tags.values())
        self.assertEqual(tags["lang:game_engine"], "C")

    # ---- the axis
    def test_axis_ends_at_the_survey_date_inside_the_border(self):
        for name in ("day", "phone-day"):
            h = self.entry(name)["hero"]
            ax = h["axis"]
            self.assertEqual(ax["end"], self.stats["taken"][:10])
            self.assertEqual(ax["border"] - ax["x_end"], hero.INSIDE)
            self.assertEqual(ax["survey"], f"{self.taken.day} {hero.MONTHS[self.taken.month - 1]}")
            self.assertEqual(ax["letters"], "SONDJFMAMJJAS", "no initial for the cut-short survey month")
            self.assertEqual(ax["years"], [2025, 2026])
            tick = [t for t in self.texts(name) if t["key"] == "survey-tick"]
            self.assertEqual([t["s"] for t in tick], [ax["survey"]])
            self.assertLessEqual(tick[0]["x1"], ax["x_end"] + 0.5)
            w, hgt = hero.SIZES["phone" if "phone" in name else "desk"]
            border = ax["border"]
            for t in self.texts(name):
                self.assertLessEqual(t["x1"], border, f"{name}: {t['s']!r} crosses the border")
                self.assertLessEqual(t["y1"], hgt - hero.RULES["phone" if "phone" in name else "desk"][1],
                                     f"{name}: {t['s']!r} below the border")
        tops = [b["top"] for r in self.entry("day")["hero"]["rows"] for b in r["blocks"]]
        self.assertGreaterEqual(min(tops), hero.RULES["desk"][1] + 24, "desk rows start 24 px below the top border")
        for t in self.texts("day"):
            if (t["key"] or "").startswith(("row:", "days:", "lang:")) or t["key"] in ("light", "edition"):
                self.assertGreaterEqual(t["y0"], hero.RULES["desk"][1] + 24 - 6, t["s"])

    # ---- the light and the mark
    def test_one_light_period_from_claims_on_the_latest_bank(self):
        claim = self.stats["claims"]["scrape_interval"]
        period = int(claim["value"])
        src = claim["source"].split(":", 1)[0]
        for name in ("day", "night", "phone-day", "phone-night"):
            e = self.entry(name)
            self.assertEqual(len(e["lights"]), 1, name)
            lt = e["lights"][0]
            self.assertEqual(lt["character"], f"Fl {period}s")
            self.assertEqual(lt["row"], src)
            row = next(r for r in e["hero"]["rows"] if r["repo"] == src)
            last = max(row["blocks"], key=lambda b: b["x0"])
            self.assertTrue(last["x0"] - 1 <= lt["x"] <= last["x1"] + 1, "the light stands on the latest bank")
            svg = self.svg[name]
            self.assertEqual(svg.count('repeatCount="indefinite"'), 1, name)
            self.assertIn(f'dur="{period}s"', svg)
            self.assertEqual(svg.count("<animate"), 1, "one beat per period, nothing else moves")
            m = e["motion"]
            self.assertEqual((m["indefinite"], m["opening_end_s"], m["violations"], m["continuous_windows"]),
                             (1, 0.0, [], []))
            self.assertEqual([t["s"] for t in e["text"] if t["key"] == "light"], [f"Fl {period}s"])
        self.assertIn(period, tokens.LOOP_PERIODS)
        data = copy.deepcopy(self.stats)
        data["claims"]["scrape_interval"]["value"] = 15
        n, rep, _out = _build(self.tmp, "fl15", self.write_stats(data, "fl15"), editions=["day"])
        self.assertEqual(n, 0)
        self.assertEqual(rep["sheets"]["hero-day"]["lights"][0]["character"], "Fl 15s", "the period is the claim's")
        data["claims"]["scrape_interval"]["measured"] = False
        n, rep, _out = _build(self.tmp, "nolight", self.write_stats(data, "nolight"), editions=["day"])
        self.assertEqual(n, 0)
        self.assertEqual(rep["sheets"]["hero-day"]["lights"], [], "an unmeasured claim draws no light")

    def test_one_edition_mark_and_lettering_in_the_water(self):
        ed = self.stats["edition"]
        for name in ("day", "phone-day"):
            e = self.entry(name)
            marks = [t for t in e["text"] if t["key"] == "edition"]
            self.assertEqual([t["s"] for t in marks], [f"{ed['version']} · PyPI"])
            mk = e["hero"]["mark"]
            self.assertEqual((mk["row"], mk["date"]), ("Rust-sitemap", ed["date"]))
            for p in e["hero"]["placements"]:
                self.assertGreaterEqual(p["clear"], hero.CLEAR, f"{name}: {p['text']} sits on a coast")
                row = next(r for r in e["hero"]["rows"] if r["repo"] == (mk["row"] if p["what"] == "edition" else "Scrapy"))
                self.assertGreaterEqual(p["box"][1], row["band"][0] - 0.5, f"{name}: {p['text']} leaves its row")
                self.assertLessEqual(p["box"][3], row["band"][1] + 0.5, f"{name}: {p['text']} leaves its row")

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
            self.assertEqual(datum, [f"{self.stats['repo_count']} REPOSITORIES · DATUM: MAIN"], name)
            self.assertIsNone(BANNED.search(self.entry(name)["alt"]))

    def test_nothing_sloping_nothing_unmeasured(self):
        for name in ALL:
            for t in self.texts(name):
                if any(ch.isdigit() for ch in t["s"]):
                    self.assertEqual(t["slant"], "upright", f"{name}: sloping figure {t['s']!r}")
                    self.assertEqual(t["truth"], "measured", f"{name}: unmeasured figure {t['s']!r}")
                if t["truth"] is not None:
                    self.assertEqual(t["truth"], "measured")
        when = f"{self.taken.day} {self.taken.strftime('%b').upper()} {self.taken.year}"
        texts = [t["s"] for t in self.texts("day")]
        self.assertIn(f"{when} · EASTERN TIME", texts)
        self.assertIn("CRAWL AND DATA INFRASTRUCTURE", texts)
        self.assertIn(f"GITHUB.COM/BENJAMINSRUSSELL · {when}", texts)
        self.assertEqual(sum(1 for s in texts if s in ("Ben", "Russell")), 2)
        phone = [t["s"] for t in self.texts("phone-day")]
        self.assertFalse(any(s.startswith("GITHUB.COM") for s in phone), "no imprint line on the phone")

    def test_type_floors_and_phone_hierarchy(self):
        for name in ALL:
            sc = "phone" if "phone" in name else "desk"
            for t in self.texts(name):
                self.assertGreaterEqual(t["size"], tokens.FLOORS[sc]["semantic"], f"{name}: {t['s']!r} {t['size']}")
        th = tokens.THEMES["day"]
        ph = self.texts("phone-day")
        for t in ph:
            self.assertGreaterEqual(t["size"], 26, "nothing under 26 px sheet type on the phone (13 px on screen)")
        role = [t for t in ph if t["s"] in ("CRAWL AND DATA INFRASTRUCTURE", "PYTHON AND RUST")]
        fine = [t for t in ph if t["key"] in ("repositories", "survey-date")]
        self.assertEqual({t["size"] for t in role}, {30})
        self.assertEqual({t["size"] for t in fine}, {26})
        self.assertGreaterEqual(min(t["y0"] for t in fine) - max(t["y1"] for t in role), 12 - 6,
                                "a 12 px gap between the role line and the fine print")
        svg = self.svg["phone-day"]
        self.assertIn(f'fill="{th.ink2}"', svg)

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
        self.assertNotIn("coastline", alt.lower())
        self.assertIn(f"{self.stats['repo_count']} repositories by week", alt)
        self.assertIn("Scrapy and rustmapper busiest", alt)
        self.assertIn("quiet Feb to Jul 2026", alt)
        last = alt.rsplit(". ", 1)[-1]
        self.assertLessEqual(len(last.split()), 10)
        self.assertEqual(last, self.cfg["alt"]["alt_poem"][0])
        self.assertTrue(self.cfg["alt"]["hero"].endswith(last))

    # ---- the live-like stats file (the second gate)
    @unittest.skipUnless(os.path.exists(LIVE), "live-like stats file not present")
    def test_live_like_stats_build_clean(self):
        n, rep, _out = _build(self.tmp, "live", LIVE)
        self.assertEqual(n, 0, rep["problems"])
        with open(LIVE, encoding="utf-8") as fh:
            live = json.load(fh)
        for e in rep["sheets"].values():
            h = e["hero"]
            rows = [r for r in h["rows"] if not r["more"]]
            self.assertEqual(len(rows) + h["rows"][-1]["n"], live["repo_count"])
            for p in h["placements"]:
                self.assertGreaterEqual(p["clear"], hero.CLEAR)


if __name__ == "__main__":
    unittest.main()
