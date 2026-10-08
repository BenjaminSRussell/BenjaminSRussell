"""build_assets / check / render_readme / publish_chart, run end-to-end on the _blank sheet."""
from __future__ import annotations

import hashlib
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
import check  # noqa: E402
import edition as E  # noqa: E402
import publish_chart  # noqa: E402
import render_readme  # noqa: E402

CFG = os.path.join(ROOT, "chart.toml")
STATS = os.path.join(ROOT, "assets", "stats.json")


class BuildAssets(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="v9-")
        self.out = os.path.join(self.tmp, "v9")
        self.report = os.path.join(self.tmp, "build-report.json")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def build(self, sheets, **kw):
        return build_assets.main(sheets=sheets, out=self.out, report_path=self.report, quiet=True, **kw)

    def test_pencil_note_edition_builds_clean(self):
        """The failure path of the chart workflow (survey failed → --no-sounding --heartbeat) must build
        with zero problems; the first live run tripped the log's glyph budget here."""
        n = self.build(["log"], no_sounding=True, heartbeat=True)
        self.assertEqual(n, 0)
        with open(self.report, encoding="utf-8") as fh:
            self.assertEqual(json.load(fh).get("problems"), [])

    def test_missing_module_is_a_failure(self):
        n = self.build(["no_such_sheet"])
        self.assertGreaterEqual(n, 1)
        with open(self.report, encoding="utf-8") as fh:
            rep = json.load(fh)
        self.assertTrue(any("no sheet module" in p for p in rep["problems"]))
        self.assertEqual(build_assets.cli(["no_such_sheet", "--out", self.out, "--report", self.report, "-q"]), 1)

    def test_blank_sheet_renders_six_editions(self):
        self.assertEqual(self.build(["_blank"]), 0)
        files = sorted(os.listdir(self.out))
        self.assertEqual(files, sorted(f"_blank-{e}.svg" for e in E.EDITION_NAMES))
        with open(self.report, encoding="utf-8") as fh:
            rep = json.load(fh)
        self.assertEqual(set(rep["sheets"]), {f"_blank-{e}" for e in E.EDITION_NAMES})
        with open(STATS, "rb") as fh:
            self.assertEqual(rep["stats_sha"], hashlib.sha256(fh.read()).hexdigest())
        for name, e in rep["sheets"].items():
            with open(os.path.join(self.tmp, e["svg"]) if not os.path.isabs(e["svg"]) else e["svg"], "rb") as fh:
                data = fh.read()
            self.assertEqual(e["sha256"], hashlib.sha256(data).hexdigest(), name)
            self.assertEqual(e["bytes"], len(data))
            self.assertEqual((e["w"], e["h"]), (720, 120) if "phone" in name else (1280, 200))
            self.assertIn(rep["stats_sha"][:12], data.decode())
            self.assertNotIn(E.STATS_SHA_PLACEHOLDER, data.decode())
            for key in ("text", "exclusions", "symbols_used", "legend", "lights", "features", "breaks"):
                self.assertIsInstance(e[key], list, key)
            if "still" in name:
                self.assertIsNone(re.search(rb"<(animate|set)\b", data), name)
        self.assertEqual(rep["poem"], ["Nothing is charted here yet."])

    def test_two_builds_are_byte_identical(self):
        self.assertEqual(self.build(["_blank"], editions=["day", "phone-night"]), 0)
        first = {f: open(os.path.join(self.out, f), "rb").read() for f in os.listdir(self.out)}
        self.assertEqual(set(first), {"_blank-day.svg", "_blank-phone-night.svg"})
        self.assertEqual(self.build(["_blank"], editions=["day", "phone-night"]), 0)
        for f, data in first.items():
            with open(os.path.join(self.out, f), "rb") as fh:
                self.assertEqual(fh.read(), data, f)

    def test_report_hooks_fill_the_skeleton(self):
        def hook(ctx, svg, entry):
            entry["text"].append({"s": ctx.sheet, "role": "label"})
        build_assets.report_hooks.append(hook)
        try:
            self.assertEqual(self.build(["_blank"], editions=["day"]), 0)
        finally:
            build_assets.report_hooks.remove(hook)
        with open(self.report, encoding="utf-8") as fh:
            self.assertEqual(json.load(fh)["sheets"]["_blank-day"]["text"], [{"s": "_blank", "role": "label"}])

    def test_unknown_edition_rejected(self):
        self.assertEqual(self.build(["_blank"], editions=["dusk"]), 1)


class Gate(unittest.TestCase):
    """A throw-away repo root: chart.toml and stats.json copied, a clean README, the _blank build."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gate-")
        os.makedirs(os.path.join(self.tmp, "assets"))
        shutil.copyfile(CFG, os.path.join(self.tmp, "chart.toml"))
        shutil.copyfile(STATS, os.path.join(self.tmp, "assets", "stats.json"))
        with open(os.path.join(self.tmp, "README.md"), "w", encoding="utf-8") as fh:
            fh.write("# chart\n<!-- position:start -->\n<!-- position:end -->\n"
                     "<sub>since <!-- n:account_since -->Oct 2024<!-- /n --></sub>\n")
        self.out = os.path.join(self.tmp, "assets", "v9")
        self.report = os.path.join(self.tmp, "assets", "build-report.json")
        self.assertEqual(build_assets.main(sheets=["_blank"], out=self.out, report_path=self.report,
                                           stats_path=os.path.join(self.tmp, "assets", "stats.json"), quiet=True), 0)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_gate(self, only):
        return check.main(only=only, tiers=("fast",), root=self.tmp, quiet=True)

    def test_discovers_my_plugins(self):
        names = {p.name for p in check.discover()}
        self.assertTrue({"xml", "size", "strings", "position", "expiry"} <= names, names)

    def test_clean_build_passes_xml_size_strings(self):
        self.assertEqual(self.run_gate(["xml", "size", "strings", "expiry"]), 0)

    def test_readme_placeholder_and_banned_figure_fail(self):
        readme = os.path.join(self.tmp, "README.md")
        with open(readme, "a", encoding="utf-8") as fh:
            fh.write("<p>⟨role⟩</p>\n")
        self.assertEqual(self.run_gate(["position"]), 1)
        with open(readme, "w", encoding="utf-8") as fh:
            fh.write("# chart\n<sub>since Oct 2024</sub>\n")   # hand-typed figure outside n: markers
        self.assertEqual(self.run_gate(["strings"]), 1)

    def test_position_empty_is_a_warning(self):
        self.assertEqual(self.run_gate(["position"]), 2)

    def test_broken_svg_fails(self):
        path = os.path.join(self.out, "_blank-day.svg")
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("<unclosed>")
        self.assertEqual(self.run_gate(["xml"]), 1)
        self.assertEqual(self.run_gate(["size"]), 1, "sha256 no longer matches the report")

    def test_unprefixed_id_and_banned_word_fail(self):
        path = os.path.join(self.out, "_blank-night.svg")
        with open(path, encoding="utf-8") as fh:
            s = fh.read()
        s = s.replace("</svg>", '<rect id="loose" width="1" height="1"/><!-- Here be dragons --></svg>')
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(s)
        self.assertEqual(self.run_gate(["xml"]), 1)
        self.assertEqual(self.run_gate(["strings"]), 1)

    def test_nothing_to_check_is_exit_3(self):
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        self.assertEqual(check.main(only=["xml"], tiers=("fast",), root=self.tmp, out_dir=empty, quiet=True), 3)


class Readme(unittest.TestCase):
    def setUp(self):
        self.cfg, self.stats = render_readme.load(CFG, STATS)

    def test_picture_order(self):
        hero = render_readme.picture("hero", self.cfg, 'A "boat" & co').splitlines()
        self.assertEqual(len(hero), 10)
        order = [re.search(r"/hero-([\w-]+)\.svg", l).group(1) for l in hero[1:-1]]
        self.assertEqual(order, ["phone-still-night", "phone-still-day", "phone-night", "phone-day",
                                 "still-night", "still-day", "night", "day"])
        self.assertIn('alt="A &quot;boat&quot; &amp; co"', hero[-2])
        self.assertNotIn("height=", "".join(hero))
        log = render_readme.picture("log", self.cfg, "x").splitlines()
        self.assertEqual(len(log), 8)
        self.assertTrue(log[1].startswith('<source media="(max-width: 767px) and (prefers-color-scheme: dark)"'))
        self.assertTrue(log[-2].startswith('<img src="https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/log-day.svg"'))

    def test_blocks_and_inline_are_idempotent(self):
        tmpl = ("<!-- picture:footer:start -->old<!-- picture:footer:end -->\n"
                "<!-- position:start — note kept -->\n<p>⟨role⟩</p>\n<!-- position:end -->\n"
                "<!-- figures:start -->\n<!-- figures:end -->\n"
                "<!-- instruments:start -->x<!-- instruments:end -->\n"
                "<!-- notices:start -->\n<!-- notices:end -->\n"
                "<sub>since <!-- n:account_since -->?<!-- /n --> · <!-- n:repo_count -->0<!-- /n --></sub>\n"
                "<picture><img src=\"https://x/main/assets/hero-light.svg\"></picture>\n")
        once = render_readme.main(tmpl, self.cfg, self.stats, use_sheet_alts=False)
        self.assertEqual(render_readme.main(once, self.cfg, self.stats, use_sheet_alts=False), once)
        self.assertIn("<!-- position:start — note kept -->\n<!-- position:end -->", once, "empty position omits the slot")
        self.assertNotIn("⟨", once)
        self.assertIn("<!-- n:account_since -->Oct 2024<!-- /n -->", once)
        self.assertIn("<!-- n:repo_count -->21<!-- /n -->", once)
        self.assertIn("<!-- picture:hero:start -->\n<picture>\n<source media=", once, "bare pictures are wrapped")
        self.assertIn("1. **Boring under load.**", once)
        self.assertIn("<!-- instruments:start -->\n<!-- instruments:end -->", once, "v9.1: the sheet shows it, no mirror")
        self.assertIn("/footer-still-day.svg", once)

    def test_figures_from_v1_and_v2(self):
        live = render_readme.figures(self.stats, self.cfg)     # whatever stats.json holds today
        self.assertRegex(live["commits"], r"^\d{1,3}(,\d{3})*$")
        self.assertTrue(int(live["repo_count"]) > 0)
        self.assertRegex(live["taken"], r"^\d{1,2} [A-Z][a-z]{2} \d{4}$")
        v1 = render_readme.figures({"commits": 1828, "repos": [{}] * 21, "since": "Oct 2024", "updated": "2026-10-07",
                                    "seeded": True}, self.cfg)
        self.assertEqual((v1["commits"], v1["repo_count"], v1["account_since"], v1["taken"]), ("1,828", "21", "Oct 2024", "7 Oct 2026"))
        v2 = render_readme.figures({"repo_count": 24, "commits": 1700, "account_since": "2024-10-03",
                                    "taken": "2026-10-07", "updated_at": "2026-10-07T06:34:12Z"}, self.cfg)
        self.assertEqual((v2["commits"], v2["repo_count"], v2["account_since"], v2["taken"], v2["taken_time"]),
                         ("1,700", "24", "Oct 2024", "7 Oct 2026", "06:34 UTC"))

    def test_alts_within_budget(self):
        figs = render_readme.figures(self.stats, self.cfg)
        for sheet in render_readme.SHEETS:
            alt = render_readme.alt_for(sheet, self.stats, self.cfg, figs, use_sheets=False)
            self.assertTrue(alt, sheet)
            self.assertLessEqual(len(alt.split()), 25, (sheet, alt))
            self.assertNotEqual(alt.split()[0].lower(), "the", sheet)
        self.assertEqual(len(self.cfg["alt"]["alt_poem"]), 6)


class Publish(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="pub-")
        self.out = os.path.join(self.tmp, "assets", "v9")
        self.report = os.path.join(self.tmp, "assets", "build-report.json")
        self.assertEqual(build_assets.main(sheets=["_blank"], out=self.out, report_path=self.report, quiet=True), 0)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_collect_lists_exactly_the_report(self):
        files = publish_chart.collect(self.tmp, self.report, os.path.join(self.tmp, "social"))
        dsts = [d for _, d in files]
        self.assertEqual(dsts[-1], "build-report.json")
        self.assertEqual(len(dsts), 7)
        self.assertTrue(all(d.startswith("assets/v9/_blank-") and d.endswith(".svg") for d in dsts[:-1]), dsts)
        staging = os.path.join(self.tmp, "stage")
        publish_chart.stage(staging, files)
        self.assertTrue(os.path.isfile(os.path.join(staging, "assets", "v9", "_blank-day.svg")))
        self.assertTrue(os.path.isfile(os.path.join(staging, "build-report.json")))

    def test_refuses_half_built_sets(self):
        os.remove(os.path.join(self.out, "_blank-day.svg"))
        with self.assertRaises(publish_chart.PublishError):
            publish_chart.collect(self.tmp, self.report, os.path.join(self.tmp, "social"))
        with open(self.report, encoding="utf-8") as fh:
            rep = json.load(fh)
        rep["problems"] = ["x"]
        with open(self.report, "w", encoding="utf-8") as fh:
            json.dump(rep, fh)
        with self.assertRaises(publish_chart.PublishError):
            publish_chart.collect(self.tmp, self.report, os.path.join(self.tmp, "social"))


if __name__ == "__main__":
    unittest.main()
