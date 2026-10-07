"""The four supporting sheets (T9): soundings, log, instruments, footer.

Builds every edition once into a temp folder through build_assets (the real runner, the real
stats.json and log.json), then checks the T9 §5 criteria that can be automated without a
browser: determinism, hard budgets, frozen sheets carry zero animation, the log keeps header plus
ten entries, the footer's indefinite count, banned strings, italic numerals on the computed log,
alts, fittings resolve, the heartbeat agrees with the soundings dateline, and that a changed
sounding moves the tide table while a missing one fails the build.
"""
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

SHEETS = ("soundings", "log", "instruments", "footer")
FROZEN_SHEETS = ("soundings", "instruments")
ANIM = re.compile(rb"<(animate|animateTransform|animateMotion|set)\b")
STATS = os.path.join(ROOT, "assets", "stats.json")


def _banned_patterns():
    try:
        sys.path.insert(0, os.path.join(SCRIPTS, "checks"))
        import importlib
        strings = importlib.import_module("strings")
        return strings.PATTERNS
    except Exception:  # noqa: BLE001 — the plug-in needs check.py on the path; fall back to T9 §5.1's own list
        return [(s, re.compile(re.escape(s), re.I)) for s in ("ILLUSTRATIVE", "PENDING", "SEEDED", "example.com")]


class Built:
    """One build of the four sheets, shared by every test in the module."""
    tmp = out = report_path = None
    report: dict = {}
    files: dict[str, bytes] = {}

    @classmethod
    def build(cls):
        if cls.tmp:
            return
        cls.tmp = tempfile.mkdtemp(prefix="v9-supporting-")
        cls.out = os.path.join(cls.tmp, "v9")
        cls.report_path = os.path.join(cls.tmp, "build-report.json")
        cls.problems = build_assets.main(sheets=list(SHEETS), out=cls.out, report_path=cls.report_path, quiet=True)
        with open(cls.report_path, encoding="utf-8") as fh:
            cls.report = json.load(fh)
        cls.files = {f: open(os.path.join(cls.out, f), "rb").read() for f in sorted(os.listdir(cls.out))}

    @classmethod
    def text_of(cls, name: str) -> list[dict]:
        return cls.report["sheets"][name]["text"]


class SupportingSheets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Built.build()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(Built.tmp, ignore_errors=True)
        Built.tmp = None

    # ---------------------------------------------------------------- the build itself
    def test_build_is_clean_and_complete(self):
        self.assertEqual(Built.problems, 0, Built.report.get("problems"))
        expected = {f"{s}-{e}.svg" for s in SHEETS for e in E.EDITION_NAMES}
        self.assertEqual(set(Built.files), expected)
        for name, e in Built.report["sheets"].items():
            w, h = e["w"], e["h"]
            mod = build_assets.load_sheet(e["sheet"])
            self.assertEqual((w, h), tuple(mod.SIZES["phone" if "phone" in name else "desk"]), name)

    def test_two_builds_are_byte_identical(self):
        out2 = os.path.join(Built.tmp, "again")
        n = build_assets.main(sheets=list(SHEETS), editions=["day", "phone-night"], out=out2,
                              report_path=os.path.join(Built.tmp, "again.json"), quiet=True)
        self.assertEqual(n, 0)
        for f in os.listdir(out2):
            with open(os.path.join(out2, f), "rb") as fh:
                self.assertEqual(fh.read(), Built.files[f], f)

    def test_budgets(self):
        b = tokens.BUDGETS
        for name, e in Built.report["sheets"].items():
            self.assertLessEqual(e["bytes"], b["svg_kb"] * 1024, name)
            self.assertLessEqual(e["gz"], b["gz_kb"] * 1024, name)
            self.assertLessEqual(e["elements"], b["elements"], name)
            if "phone" in name:
                self.assertLessEqual(e["bytes"], b["phone_svg_kb"] * 1024, name)
            # per-sheet raw/gz targets (hero 170/60 …) are warnings in check.py, not asserted here; the glyph
            # library alone is 20–35 KB raw per sheet, so they are reported in S-report.md instead
        # one desktop edition set of the four stays well inside its share of the page's 250 KB gz
        day = sum(e["gz"] for n, e in Built.report["sheets"].items() if n.endswith("-day") and "phone" not in n and "still" not in n)
        self.assertLess(day, 100 * 1024)

    # ---------------------------------------------------------------- motion
    def test_frozen_sheets_carry_no_animation(self):
        for f, data in Built.files.items():
            sheet = f.split("-")[0]
            frozen = sheet in FROZEN_SHEETS or "-still" in f or "-phone" in f
            if frozen:
                self.assertIsNone(ANIM.search(data), f)
        for name in ("soundings", "instruments"):
            for ed in E.EDITION_NAMES:
                m = Built.report["sheets"][f"{name}-{ed}"]["motion"] or {}
                self.assertEqual(m.get("indefinite", 0), 0, f"{name}-{ed}")
                self.assertEqual(m.get("violations"), [], f"{name}-{ed}")

    def test_footer_is_the_ambient_sheet_within_budget(self):
        for ed in ("day", "night"):
            m = Built.report["sheets"][f"footer-{ed}"]["motion"]
            self.assertEqual(m["class"], "ambient")
            self.assertLessEqual(m["indefinite"], 12)
            self.assertEqual(m["violations"], [])
            self.assertEqual(m["longest_loop_s"], 96.0)
            data = Built.files[f"footer-{ed}.svg"].decode()
            self.assertEqual(data.count('repeatCount="indefinite"'), m["indefinite"])
            for p in set(re.findall(r'repeatCount="indefinite"[^>]*?dur="([\d.]+)s"', data) +
                         re.findall(r'dur="([\d.]+)s"[^>]*?repeatCount="indefinite"', data)):
                self.assertIn(float(p), [float(x) for x in tokens.LOOP_PERIODS], p)
            # the sloop arrives 40–64 s and the serpent first rises at 84 s (MASTERPLAN §2.1)
            self.assertIn('begin="40s" dur="24s"', data)
            self.assertIn('begin="84s"', data)
            self.assertIn("footer-sym-anchorage", data)
        self.assertEqual(Built.report["sheets"]["footer-still-day"]["motion"]["class"], "still")

    def test_log_motion_is_the_heartbeat_and_the_cursor(self):
        for ed in ("day", "night"):
            m = Built.report["sheets"][f"log-{ed}"]["motion"]
            self.assertEqual(m["indefinite"], 1)                 # the cursor blink
            self.assertLessEqual(m["repaints_per_s"], 2.0)
            self.assertEqual(m["violations"], [])
            data = Built.files[f"log-{ed}.svg"].decode()
            self.assertIn('class="typed"', data)
            sets = [float(t) for t in re.findall(r'<set attributeName="opacity" to="1" begin="([\d.]+)s"', data)]
            self.assertTrue(sets and min(sets) >= 44.0 and max(sets) <= 49.0, (min(sets), max(sets)))
            blink = re.search(r'id="log-cursor-blink"[^>]*begin="([\d.]+)s" dur="1s" repeatCount="indefinite"', data)
            self.assertIsNotNone(blink)
            self.assertGreaterEqual(float(blink.group(1)), 48.5)
        still = Built.files["log-still-day.svg"]
        self.assertIsNone(ANIM.search(still))
        self.assertIn("heartbeat", [t.get("key") for t in Built.text_of("log-still-day")])

    def test_no_heartbeat_means_no_typing(self):
        out3 = os.path.join(Built.tmp, "nohb")
        n = build_assets.main(sheets=["log"], editions=["day"], out=out3, report_path=os.path.join(Built.tmp, "nohb.json"),
                              quiet=True, heartbeat=False)
        self.assertEqual(n, 0)
        with open(os.path.join(out3, "log-day.svg"), encoding="utf-8") as fh:
            data = fh.read()
        self.assertNotIn('<set attributeName="opacity"', data)
        self.assertNotIn('<g class="typed">', data)
        self.assertIn('id="log-cursor-blink"', data)

    # ---------------------------------------------------------------- the log's content
    def test_log_frames_keep_header_and_ten_entries(self):
        for ed in E.EDITION_NAMES:
            if "phone" in ed:
                continue
            runs = Built.text_of(f"log-{ed}")
            times = {t["key"] for t in runs if t.get("key") and t["key"].startswith("row.") and t["key"].endswith(".time")}
            self.assertEqual(len(times), 10, ed)
            texts = [t["s"] for t in runs]
            self.assertTrue(any(s.startswith("Log of the") for s in texts), ed)
            for head in ("TIME", "REMARKS", "WIND"):
                self.assertIn(head, texts, ed)
            # every entry is static (no base opacity 0 outside the typed heartbeat)
            data = Built.files[f"log-{ed}.svg"].decode()
            body = re.sub(r'<g class="typed">.*?</g>', "", data, flags=re.S)
            body = re.sub(r"<rect class=\"typed\".*?</rect>", "", body, flags=re.S)
            self.assertNotIn('opacity="0"', body, ed)

    def test_log_numerals_are_italic_except_the_heartbeat(self):
        """T9 §5.3: computed log → every numeral in the italic cut, the heartbeat row and folio upright."""
        with open(os.path.join(ROOT, "assets", "log.json"), encoding="utf-8") as fh:
            log = json.load(fh)
        for ed in ("day", "still-night"):
            for t in Built.text_of(f"log-{ed}"):
                if not re.search(r"\d", t["s"]) or t.get("key") in ("heartbeat", "folio"):
                    continue
                if log.get("measured"):
                    self.assertEqual(t["slant"], "upright", t)
                else:
                    self.assertEqual(t["slant"], "italic", f"{ed}: {t['s']!r} in {t['font']}")
            hb = [t for t in Built.text_of(f"log-{ed}") if t.get("key") == "heartbeat"]
            self.assertTrue(hb and all(t["slant"] == "upright" for t in hb))

    def test_log_signature_is_gated_on_measured(self):
        """36: a computed log is closed but unsigned; only a measured session carries the initials."""
        with open(os.path.join(ROOT, "assets", "log.json"), encoding="utf-8") as fh:
            log = json.load(fh)
        for ed in ("day", "phone-day"):
            texts = [t["s"] for t in Built.text_of(f"log-{ed}")]
            if log.get("measured"):
                self.assertIn(log["signoff"]["initials"], texts)
            else:
                self.assertNotIn(log["signoff"]["initials"], texts)
                self.assertTrue(any("unsigned" in s for s in texts), ed)
        if not log.get("measured"):
            self.assertIn("unsigned", Built.report["sheets"]["log-day"]["alt"])

    def test_log_remarks_stay_in_their_column(self):
        for t in Built.text_of("log-day"):
            if t.get("within"):
                self.assertGreaterEqual(t["x0"], t["within"][0] - 0.5, t)
                self.assertLessEqual(t["x1"], t["within"][0] + t["within"][2] + 0.5, t)

    def test_heartbeat_matches_the_soundings_dateline(self):
        """T9 §5.9: the heartbeat's HHMM is updated_at to the minute and the soundings dateline agrees."""
        with open(STATS, encoding="utf-8") as fh:
            stats = json.load(fh)
        upd = stats["updated_at"]
        hhmm, hm = upd[11:13] + upd[14:16], upd[11:16]
        hb = next(t["s"] for t in Built.text_of("log-day") if t.get("key") == "heartbeat")
        self.assertTrue(hb.startswith(hhmm + " UTC"), hb)
        self.assertIn(f"{stats['commits']:,} commits", hb)
        self.assertIn(f"{stats['repo_count']} repositories", hb)
        dateline = next(t["s"] for t in Built.text_of("soundings-day") if t.get("key") == "dateline")
        self.assertIn(f"{hm} UTC", dateline)

    # ---------------------------------------------------------------- honesty
    def test_no_banned_strings(self):
        pats = _banned_patterns()
        for f, data in Built.files.items():
            text = data.decode("utf-8")
            for label, pat in pats:
                self.assertIsNone(pat.search(text), f"{label!r} in {f}")
        for name, e in Built.report["sheets"].items():
            manifest = "\n".join(t["s"] for t in e["text"])
            for label, pat in pats:
                self.assertIsNone(pat.search(manifest), f"{label!r} in {name} manifest")
                self.assertIsNone(pat.search(e["alt"]), f"{label!r} in {name} alt")

    def test_no_raw_text_patterns_or_filters(self):
        for f, data in Built.files.items():
            text = data.decode("utf-8")
            for tag in ("<text", "<tspan", "<textPath", "<pattern", "<filter", "<animateMotion", "<script", "<style"):
                self.assertNotIn(tag, text, f"{tag} in {f}")
            for m in re.finditer(r'stroke-width="([\d.]+)"', text):
                self.assertIn(float(m.group(1)), (*tokens.W.values(), 0.8, 0.22, 0.18, 0.45), f"{f}: stroke {m.group(1)}")

    def test_512_is_never_upright_on_the_log(self):
        """Decision 14: the worker count is disputed, so 512 appears only in the log, italic (the soundings
        register prints game_engine's 512 *commits* upright: a different, measured figure)."""
        for name, e in Built.report["sheets"].items():
            if e["sheet"] != "log" or e["form"] == "phone":
                continue
            hits = [t for t in e["text"] if "512" in t["s"]]
            self.assertTrue(hits, name)
            for t in hits:
                self.assertEqual(t["slant"], "italic", f"{name}: {t['s']!r}")

    def test_soundings_unit_and_both_instruments(self):
        runs = Built.text_of("soundings-day")
        caps = [t for t in runs if t["role"] == "label-caps" and t.get("key") != "folio"]
        self.assertEqual(len(caps), 1)
        self.assertEqual(caps[0]["s"], "SOUNDINGS IN COMMITS")
        keys = {t.get("key"): t for t in runs if t.get("key")}
        for k in ("commits", "all_hands", "calendar_total", "tide.hw", "tide.lw", "tide.median", "tide.slack"):
            self.assertIn(k, keys)
            self.assertEqual(keys[k]["slant"], "upright", k)
        with open(STATS, encoding="utf-8") as fh:
            stats = json.load(fh)
        self.assertEqual(keys["commits"]["s"], f"{stats['commits']:,}")
        self.assertEqual(keys["all_hands"]["s"], f"{stats['all_hands']:,}")
        self.assertEqual(keys["calendar_total"]["s"], f"{stats['calendar_total']:,}")
        # 52 upright soundings along the traverse, one per week, from sounding()
        weeks = [t for t in runs if (t.get("key") or "").startswith("week.")]
        self.assertEqual(len(weeks), len(stats["weeks"]))
        self.assertTrue(all(t["origin"] == "sounding" and t["slant"] == "upright" for t in weeks))
        # one line per repository in the register, under the chart's own names where chart.toml gives one
        reg = [t for t in runs if (t.get("key") or "").startswith("repo.")]
        self.assertEqual(len(reg), len(stats["repos"]))
        names = {t["s"] for t in runs}
        cfg = build_assets.load_cfg()
        for f in cfg["features"]:
            if f.get("aliases") and any(r["name"] == f["repo"] for r in stats["repos"]):
                self.assertIn(f["aliases"][0].upper(), names, f["repo"])
        self.assertNotIn("SCRAPY", names)

    def test_changing_a_sounding_moves_the_tide_and_no_weeks_fails(self):
        """T9 §5.2."""
        with open(STATS, encoding="utf-8") as fh:
            stats = json.load(fh)
        hw_i = max(range(len(stats["weeks"])), key=lambda i: stats["weeks"][i]["n"])
        stats["weeks"][hw_i]["n"] += 1000
        stats["tide"]["hw"]["n"] += 1000
        p = os.path.join(Built.tmp, "stats-plus.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(stats, fh)
        out = os.path.join(Built.tmp, "plus")
        rep = os.path.join(Built.tmp, "plus.json")
        n = build_assets.main(sheets=["soundings"], editions=["day"], out=out, report_path=rep, quiet=True, stats_path=p)
        self.assertEqual(n, 0)
        with open(rep, encoding="utf-8") as fh:
            runs = json.load(fh)["sheets"]["soundings-day"]["text"]
        hw = next(t["s"] for t in runs if t.get("key") == "tide.hw")
        self.assertIn(f"HW {stats['tide']['hw']['n']:,}", hw)
        with open(os.path.join(out, "soundings-day.svg"), "rb") as fh:
            self.assertNotEqual(fh.read(), Built.files["soundings-day.svg"])
        del stats["weeks"]
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(stats, fh)
        n = build_assets.main(sheets=["soundings"], editions=["day"], out=out, report_path=rep, quiet=True, stats_path=p)
        self.assertGreaterEqual(n, 1)
        with open(rep, encoding="utf-8") as fh:
            problems = json.load(fh)["problems"]
        self.assertTrue(any("no soundings" in s for s in problems), problems)

    # ---------------------------------------------------------------- alts, fittings, folios
    def test_alts(self):
        for name, e in Built.report["sheets"].items():
            words = e["alt"].split()
            self.assertLessEqual(len(words), 25, f"{name}: {len(words)} words")
            self.assertFalse(e["alt"].startswith("The"), name)
            self.assertNotIn("serpent", e["alt"].lower(), name)
        poem = Built.report["poem"]
        cfg = build_assets.load_cfg()
        want = cfg["alt"]["alt_poem"]
        self.assertEqual(poem, [want[1], want[3], want[4], want[5]])

    def test_fittings_resolve_and_bold_means_active(self):
        cfg = build_assets.load_cfg()
        with open(STATS, encoding="utf-8") as fh:
            stats = json.load(fh)
        repos = {r["name"]: r for r in stats["repos"]}
        runs = Built.text_of("instruments-day")
        by_text = {t["s"]: t for t in runs}
        for item in cfg["fittings"]["items"]:
            self.assertIn(item["repo"], repos, item)
            run = by_text.get(item["name"])
            self.assertIsNotNone(run, item["name"])
            self.assertEqual((run["role"], run["size"]), ("label", 17), item["name"])
            self.assertIn(f"fitted.{item['name']}", {t.get("key") for t in runs}, item["name"])
        # bold = active: the one active fitting carries the spread stroke
        svg = Built.files["instruments-day.svg"].decode()
        active = [i["name"] for i in cfg["fittings"]["items"] if repos[i["repo"]]["active"]]
        self.assertEqual(svg.count('stroke-width="0.45" paint-order="stroke"'), len(active))
        # the phone edition stacks the three groups: a caps head per group and every fitting named
        phone = Built.text_of("instruments-phone-day")
        texts = " ".join(t["s"] for t in phone)
        for code, _gloss in cfg["fittings"]["groups"]:
            self.assertIn(code.upper(), [t["s"] for t in phone])
        for item in cfg["fittings"]["items"]:
            self.assertIn(item["name"], texts)
        self.assertEqual([t["key"] for t in phone if t.get("key")], ["folio"])

    def test_folio_on_every_sheet(self):
        for name, e in Built.report["sheets"].items():
            folios = [t for t in e["text"] if t.get("key") == "folio"]
            self.assertEqual(len(folios), 1, name)
            self.assertRegex(folios[0]["s"], r"^CHART NO\. \d+ · SHEET [2-6]$")
            caps = [t for t in e["text"] if t["role"] == "label-caps" and t.get("key") != "folio"]
            self.assertLessEqual(len(caps), 1, name)

    def test_phone_editions_are_redrawn(self):
        for sheet in SHEETS:
            desk = Built.text_of(f"{sheet}-day")
            phone = Built.text_of(f"{sheet}-phone-day")
            self.assertLess(len(phone), len(desk), sheet)
            for t in phone:
                self.assertIn(t["size"], tokens.SCALE_PHONE, f"{sheet}: {t}")
                if t["semantic"]:
                    self.assertGreaterEqual(t["size"], tokens.FLOORS["phone"]["semantic"], t)


if __name__ == "__main__":
    unittest.main()
