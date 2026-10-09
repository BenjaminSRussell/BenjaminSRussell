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

    def test_default_build_is_the_hero(self):
        """D1: the default build is the page's one chart; the other sheets stay buildable by name."""
        self.assertEqual(build_assets.SHEETS, ["hero"])
        self.assertEqual(build_assets.ALL_SHEETS[0], "hero")
        self.assertTrue({"soundings", "approaches", "log", "instruments", "footer"} <= set(build_assets.ALL_SHEETS))
        for name in build_assets.ALL_SHEETS:
            build_assets.load_sheet(name)


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

    def test_unmeasured_figure_on_the_hero_fails(self):
        """D5: a text run on the hero whose report truth is not measured fails the strings check."""
        with open(self.report, encoding="utf-8") as fh:
            rep = json.load(fh)
        entry = dict(rep["sheets"]["_blank-day"])
        entry["text"] = [{"s": "UNSURVEYED", "truth": None}, {"s": "12,440", "truth": "measured"}]
        rep["sheets"]["hero-day"] = entry
        with open(self.report, "w", encoding="utf-8") as fh:
            json.dump(rep, fh)
        self.assertEqual(self.run_gate(["strings"]), 0, "labels and measured figures pass")
        entry["text"].append({"s": "4,096", "truth": "illustrative"})
        with open(self.report, "w", encoding="utf-8") as fh:
            json.dump(rep, fh)
        self.assertEqual(self.run_gate(["strings"]), 1)
        rep["sheets"]["log-day"] = rep["sheets"].pop("hero-day")       # off the page: its figures are its own
        with open(self.report, "w", encoding="utf-8") as fh:
            json.dump(rep, fh)
        self.assertEqual(self.run_gate(["strings"]), 0)

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
        # no pixel height: GitHub's markdown CSS keeps it while it narrows the width (letterboxed sheet)
        self.assertNotIn("height=", "".join(hero))
        self.assertIn('width="100%"', hero[-2])
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
        self.assertIn("/footer-still-day.svg", once, "a picture block the README carries is written")
        self.assertNotIn("/soundings-day.svg", once, "a picture block the README does not carry is not")

    def test_notices_first_four_and_no_release_line(self):
        block = render_readme.notices_block(self.cfg, self.stats)
        rows = [r for r in block.splitlines() if r.strip()]
        self.assertEqual(len(rows), 4, block)
        self.assertTrue(rows[0].startswith("1. **Boring under load.**"))
        self.assertTrue(rows[-1].startswith("4. **Parse, don't pattern-match.**"))
        self.assertNotIn("The surface is part of the system", block)
        self.assertNotIn("editions", block)
        self.assertNotIn("pypi.org", block)

    def test_provenance_line_is_from_stats_only(self):
        """D5: measured when, from how many clones, sweep days out, the co-author count; no totals, no instruments."""
        figs = render_readme.figures(self.stats, self.cfg)
        block = render_readme.survey_block(self.stats, figs)
        self.assertTrue(block.startswith(f"<sub>Measured {figs['taken']} from clones of {figs['repo_count']} public "
                                         "repositories, author's commits on main") and block.endswith(" · regenerated weekly.</sub>"), block)
        # v11: the commit totals are off the page until the data audit settles them
        for figure in ("commits", "all_hands", "calendar_total"):
            self.assertNotIn(f"{figs[figure]} ", block, figure)
        for word in ("all hands", "calendar", "surveyed", "instruments", "GraphQL", "clones live", "Data</b>"):
            self.assertNotIn(word, block, word)
        if self.stats.get("sweeps"):      # the builder already lists the sweep days; D2's sweep_dates wins when present
            self.assertIn("sweep days (", block)
        # D2's keys, when present, print exactly so
        full = {"taken": "2026-10-07", "repo_count": 21, "coauthored_total": 412,
                "sweep_dates": ["2025-11-10", "2025-11-09", "2026-10-07", "2026-10-01"]}
        self.assertEqual(render_readme.survey_block(full),
                         "<sub>Measured 7 Oct 2026 from clones of 21 public repositories, author's commits on main, sweep days "
                         "(9–10 Nov 2025, 1 and 7 Oct 2026) excluded · 412 commits carry agent co-author trailers · regenerated weekly.</sub>")
        self.assertIn(" · 1 commit carries agent", render_readme.survey_block(dict(full, coauthored_total=1)))
        self.assertIn(" · no commits carry agent", render_readme.survey_block(dict(full, coauthored_total=0)))
        self.assertEqual(render_readme.fmt_days(["2026-03-01", "2026-03-02", "2026-03-03", "2026-03-09", "2026-05-20"]),
                         "1–3 and 9 Mar 2026, 20 May 2026")
        # a thin stats.json prints only what it holds; nothing is guessed (no sweeps, no co-author item)
        thin = render_readme.survey_block({"taken": "2026-10-07", "commits": 12, "repo_count": 2})
        self.assertEqual(thin, "<sub>Measured 7 Oct 2026 from clones of 2 public repositories, author's commits on main · regenerated weekly.</sub>")
        self.assertEqual(render_readme.survey_block({}), "")
        failed = render_readme.survey_block({"taken": "2026-10-07", "repo_count": 2,
                                             "provenance": {"mode": "cache-failed", "failed_at": "2026-10-11T06:20:00Z"}})
        self.assertIn(" · the last run failed on 11 Oct 2026; these figures are from the run before · ", failed)

    def test_facts_block_prints_only_present_keys(self):
        """D4: one line under a flagship from D2's keys; an absent key is omitted, never estimated."""
        full = {"repos": [{"name": "Rust-sitemap", "aliases": ["rustmapper"],
                           "manifest": ["tokio", "redb", "rkyv", "reqwest", "clap", "serde"], "tests": 3, "workflows": 2,
                           "ci": {"conclusion": "success", "date": "2026-10-07"},
                           "lines": {"Rust": 16234, "Python": 412}, "last_ns": "2026-08-08"},
                          {"name": "Scrapy", "tests": 257, "workflows": ["ci.yml"], "ci": "failure",
                           "lines": {"by_language": {"Python": 69120}, "total": 69120}}]}
        self.assertEqual(render_readme.facts_block(full, "rustmapper"),
                         "<sub>Built on tokio, redb, rkyv, reqwest, clap · 3 test files · 2 workflows, last run passed 7 Oct 2026 · "
                         "16k lines of Rust · last worked 8 Aug 2026</sub>")
        self.assertEqual(render_readme.facts_block(full, "Scrapy"),
                         "<sub>257 test files · 1 workflow, last run failed · 69k lines of Python</sub>")
        self.assertEqual(render_readme.facts_block(full, "nowhere"), "")
        self.assertEqual(render_readme.facts_block({"repos": [{"name": "Scrapy", "commits": 900}]}, "Scrapy"), "", "no D2 keys, no line")
        self.assertEqual(render_readme.facts_block({"repos": [{"name": "Scrapy", "tests": 1}]}, "Scrapy"), "<sub>1 test file</sub>")
        self.assertEqual(render_readme.facts_block(self.stats, "Scrapy"), "" if "tests" not in render_readme._repo(self.stats, "Scrapy")
                         else render_readme.facts_block(self.stats, "Scrapy"), "today's stats.json has no D2 keys: nothing is printed")
        tmpl = ("<!-- facts:Rust-sitemap:start -->\nold\n<!-- facts:Rust-sitemap:end -->\n"
                "<!-- facts:Scrapy:start -->\n<!-- facts:Scrapy:end -->\n<!-- facts:nowhere:start -->x<!-- facts:nowhere:end -->\n")
        once = render_readme.main(tmpl, self.cfg, full, use_sheet_alts=False)
        self.assertIn("<!-- facts:Rust-sitemap:start -->\n<sub>Built on tokio", once)
        self.assertIn("<!-- facts:Scrapy:start -->\n<sub>257 test files", once)
        self.assertIn("<!-- facts:nowhere:start -->\n<!-- facts:nowhere:end -->", once, "an unknown repository prints nothing")
        self.assertEqual(render_readme.main(once, self.cfg, full, use_sheet_alts=False), once)
        self.assertEqual(render_readme.fmt_k(950), "950")
        self.assertEqual(render_readme.fmt_k(1_300_000), "1.3M")

    def test_page_sheets_and_position_inline(self):
        self.assertEqual(render_readme.page_sheets("<!-- picture:footer:start -->\n<!-- picture:hero:start -->"), ["hero", "footer"])
        self.assertEqual(render_readme.page_sheets("no pictures"), [])
        cfg = dict(self.cfg, position={"text": "open to work · UTC−5"})
        self.assertEqual(render_readme.position_block(cfg), "&nbsp;· <i>open to work · UTC−5</i>")
        self.assertEqual(render_readme.position_block(self.cfg), "", "chart.toml's position is empty today")
        self.assertIn("License", render_readme.license_block())
        self.assertTrue(render_readme.license_block().startswith("<sub>"))

    def test_committed_readme_is_the_one_chart_page(self):
        """D1/D8: the README carries the hero's picture block and no other sheet, in the decided order."""
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            text = fh.read()
        self.assertEqual(render_readme.page_sheets(text), ["hero"])
        for sheet in ("soundings", "approaches", "log", "instruments", "footer"):
            self.assertNotIn(f"/{sheet}-day.svg", text, sheet)
        order = ["<!-- picture:hero:end -->", "Crawl and data infrastructure · Python and Rust", "<!-- position:start",
                 "<!-- contact:start", "**Ben Russell builds**", "**Languages**", "**Stack**",
                 "**[rustmapper](https://github.com/BenjaminSRussell/Rust-sitemap)** is a concurrent sitemap crawler",
                 "<!-- n:edition_version -->", "<!-- facts:Rust-sitemap:start -->", "pip install rustmapper",
                 "- Prebuilt wheel for Apple silicon", "**[Scrapy](https://github.com/BenjaminSRussell/Scrapy)** is a multi-stage",
                 "<!-- facts:Scrapy:start -->", "**Also**", "<summary>15 more repositories", "**Working rules**",
                 "<!-- notices:start -->", "4. **Parse, don't pattern-match.**", "Found a mistake? [Open an issue]",
                 "<!-- survey:start -->", "<sub>Measured ", " · regenerated weekly.</sub>", "Generated from my repositories by", "DESIGN.md",
                 "<!-- license:start -->", "**License**"]
        positions = [text.index(m) for m in order]
        self.assertEqual(positions, sorted(positions), "the page's blocks are out of D8's order")
        for gone in ("## Soundings", "## Approaches", "## Ship's log", "## Instruments", "<summary><b>Colophon</b>",
                     "5. **The surface", "editions:", "<!-- figures:start", "<!-- instruments:start", "<!-- log_lede:start",
                     # v11: the text is written straight; the theme lives in the image only
                     "survey vessel", "Other waters", "Below the waterline", "Notices to mariners", "Survey log",
                     "wrong depth", "all hands", "mark in the channel", "leaves the harbor", "sheets and copy", "redraw",
                     # round 5, D3: the real name, no worker figure until the repository agrees with itself, no "provisional"
                     "**Other repositories**", "256 and 1,024", "provisional", "pre-1.0", "<b>Data</b>"):
            self.assertNotIn(gone, text, gone)
        body = re.sub(r"<!--\s*picture:hero:start\b.*?picture:hero:end\s*-->", "", text, flags=re.S)   # the hero's alt is the hero builder's
        self.assertNotIn("Scrapy Harbor", body, "D3: the project is Scrapy; 'Scrapy Harbor' was coined for the v8 chart")

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
        for sheet in render_readme.SHEETS:       # every sheet the build knows, on the page or built on request
            alt = render_readme.alt_for(sheet, self.stats, self.cfg, figs, use_sheets=False)
            self.assertTrue(alt, sheet)
            self.assertLessEqual(len(alt.split()), 25, (sheet, alt))
            self.assertNotEqual(alt.split()[0].lower(), "the", sheet)
        self.assertEqual(len(self.cfg["alt"]["alt_poem"]), len(render_readme.SHEETS))


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
