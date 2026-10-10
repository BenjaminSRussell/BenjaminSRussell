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

    def test_round_three_page(self):
        """Review round 3: the hero links to the project; the pick, about, license and load sentences follow the data;
        the page speaks of him in the third person."""
        pic = render_readme.picture("hero", self.cfg, "x", render_readme.hero_link(self.cfg))
        self.assertTrue(pic.startswith('<a href="https://github.com/BenjaminSRussell/Rust-sitemap">\n<picture>'))
        self.assertTrue(pic.endswith("</picture>\n</a>"))
        # pick: only while its Scrapy rows hold and the route's header holds
        rows = [{"text": f["text"], "repo": f["repo"], "use": "pick", "holds": True}
                for f in self.cfg["figures"] if f.get("use") == "pick"]
        ok = {"header_verified": True, "gates": {"no_services": {"ok": True}}}
        s = dict(self.stats, figures=rows, routes={"rustmapper": ok})
        self.assertIn("**rustmapper**", render_readme.pick_block(s, self.cfg))
        self.assertIn("from one binary, with no services to run", render_readme.pick_block(s, self.cfg))
        # review round 5: the names first, where a scanning reader starts each sentence
        self.assertTrue(render_readme.pick_block(s, self.cfg).startswith("**rustmapper** "))
        self.assertIn(". **Scrapy** keeps", render_readme.pick_block(s, self.cfg))
        self.assertNotIn("one command", render_readme.pick_block(s, self.cfg))   # review round 4: it takes three steps
        # review round 4: "no services" only while the release's crawl takes Redis as an opt-in flag
        self.assertEqual(render_readme.pick_block(dict(s, routes={"rustmapper": dict(ok, gates={"no_services": {"ok": False}})}),
                                                  self.cfg), "")
        self.assertEqual(render_readme.pick_block(dict(s, figures=[dict(rows[0], holds=False)] + rows[1:]), self.cfg), "")
        self.assertEqual(render_readme.pick_block(dict(s, routes={"rustmapper": {"header_verified": False}}), self.cfg), "")
        # about: the 0.1.3 wheel has no module, so the Python API is main's while main has it
        gates = {"rustmapper": {"repo": "Rust-sitemap", "gates": {"python_api": {"ok": True}}}}
        s = dict(self.stats, edition={"version": "0.1.3", "modules": []}, routes=gates)
        self.assertIn("is on main and not yet released", render_readme.about_block(s, "Rust-sitemap"))
        s = dict(s, edition={"version": "0.1.4", "modules": ["rustmapper"]})
        self.assertIn("its command line and a Python API, built with maturin", render_readme.about_block(s, "Rust-sitemap"))
        s = dict(s, edition={"version": "0.1.3"})          # never read: no claim either way
        self.assertTrue(render_readme.about_block(s, "Rust-sitemap").endswith("gives you its command line."))
        # review round 6: one description per screen; the image's header and the pick sentence introduce the tool
        for ed_ in ({"version": "0.1.3", "modules": []}, {"version": "0.1.4", "modules": ["rustmapper"]}, {}):
            self.assertNotIn("sitemap crawler written in Rust", render_readme.about_block(dict(s, edition=ed_), "Rust-sitemap"))
        # license: printed only when GitHub detects one; null warns
        base = {"repos": [{"name": "Rust-sitemap", "test_functions": 3, "license": None}]}
        self.assertNotIn("MIT", render_readme.facts_block(base, "Rust-sitemap"))
        base["repos"][0]["license"] = "MIT"
        self.assertIn(" · MIT license", render_readme.facts_block(base, "Rust-sitemap"))
        from checks import readme as readme_check
        text = "<!-- facts:Rust-sitemap:start -->"
        self.assertEqual([f.code for f in readme_check.license_flagship(text, {"repos": [{"name": "Rust-sitemap",
                                                                                        "license": None}]})],
                         ["LICENSE-FLAGSHIP"])
        self.assertEqual(readme_check.license_flagship(text, base), [])

    def test_no_first_person_on_the_page(self):
        """Review round 3: the page is about him, in his name: no I, my, mine or me in its visible prose."""
        from checks.strings import readme_visible
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            text = re.sub(r"```.*?```", " ", fh.read(), flags=re.S)
        prose = readme_visible(text)
        self.assertEqual(re.findall(r"\b(?:I|my|mine|me|My|Me|Mine)\b", prose), [])

    def test_picture_order(self):
        hero = render_readme.picture("hero", self.cfg, 'A "boat" & co').splitlines()
        self.assertEqual(len(hero), 6)       # round 6: the hero does not move, so no reduced-motion sources
        order = [re.search(r"/hero-([\w-]+)\.svg", l).group(1) for l in hero[1:-1]]
        self.assertEqual(order, ["phone-night", "phone-day", "night", "day"])
        self.assertIn('alt="A &quot;boat&quot; &amp; co"', hero[-2])
        # no pixel height: GitHub's markdown CSS keeps it while it narrows the width (letterboxed sheet)
        self.assertNotIn("height=", "".join(hero))
        self.assertIn('width="100%"', hero[-2])
        log = render_readme.picture("log", self.cfg, "x").splitlines()
        self.assertEqual(len(log), 8)
        # review round 6: the phone sheet up to a 1199 px viewport, where GitHub's README column is under 766 px
        self.assertTrue(log[1].startswith('<source media="(max-width: 1199px) and (prefers-color-scheme: dark)"'))
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
        figs = render_readme.figures(self.stats, self.cfg)    # account_since is null without a dated GraphQL fetch
        self.assertIn(f"<!-- n:account_since -->{figs['account_since']}<!-- /n -->", once)
        self.assertIn(f"<!-- n:repo_count -->{self.stats['repo_count']}<!-- /n -->", once)
        self.assertIn("<!-- picture:hero:start -->\n<a href=\"https://github.com/BenjaminSRussell/Rust-sitemap\">\n"
                      "<picture>\n<source media=", once, "bare pictures are wrapped, the hero in its project's link")
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
        """D5 / F3.4: measured when, from how many clones, my commits on their default branches, the bulk-edit days
        named and defined; the agent share and the agent-authored commits; no commit total, no instruments."""
        figs = render_readme.figures(self.stats, self.cfg)
        block = render_readme.survey_block(self.stats, figs, ["Rust-sitemap", "Scrapy"], {"Rust-sitemap": "rustmapper"})
        self.assertTrue(block.startswith("<sub>The [drawing](DESIGN.md) is rustmapper ") and block.endswith(".</sub>"),
                        block)
        # review round 5: what a visitor needs: which release is drawn and that it was run; no build process, no
        # schedule (a generated-by footer), no flags (DESIGN.md has them)
        # review round 6: the run's one flag that changes what the printed command does is named, in words
        self.assertIn("is rustmapper 0.1.3, the release pip installs; its commands were run, with seeding off, against a "
                      "local 3-page site on 10 Oct 2026 (Linux x86_64).", block)
        for word in ("regenerated", "generated", "weekly", "Tests and CI measured", "public repositories",
                     "--seeding-strategy", "source file", "the reader it points to"):
            self.assertNotIn(word, block, word)
        self.assertLessEqual(len(block.split()), 60, "two facts, not a methods section")
        for figure in ("commits", "all_hands", "calendar_total"):
            if self.stats.get(figure):          # a null figure is not printed anywhere, so there is nothing to look for
                self.assertNotIn(render_readme.fmt_n(self.stats[figure]), block, figure)
        for word in ("all hands", "calendar", "surveyed", "instruments", "GraphQL", "clones live", "Data</b>", "sweep",
                     "author's commits", f"{(self.stats.get('coauthored_total') or {}).get('agent')} commits"):
            self.assertNotIn(word, block, word)
        self.assertNotIn("bulk-edit", block)      # round 6: no figure on the page uses commit-days
        # review round 4: the AI clause qualifies the printed tests and lines, per repository with a facts line
        self.assertNotIn("co-author trailer", block)
        self.assertNotIn("not counted as his", block)
        self.assertIn("Tests and lines are counted per repository, whoever wrote them: coding agents (Claude, jules) "
                      "authored 45 of rustmapper's 146 commits and 71 of Scrapy's 499.</sub>", block)
        # F3.4's own example, from a fixture carrying the keys the data builder adds
        full = {"taken": "2026-10-09", "repo_count": 21, "commits": 2032,
                "sweep_dates": ["2025-11-10", "2025-11-09", "2026-10-07", "2026-10-01"],
                "coauthored_total": {"count": 502, "share": 0.247, "agent": 63, "agent_share": 0.031,
                                     "names": {"Claude Sonnet 5": 45}},
                "agent_authored": {"total": 297, "names": {"google-labs-jules[bot]": 125, "Claude": 172}}}
        self.assertEqual(render_readme.survey_block(full), "", "no route and no repository with a facts line: nothing")
        # round 6: with the route and the run check, the line says which release is drawn and that it was run
        routed = dict(full, edition={"project": "rustmapper", "version": "0.1.3"},
                      routes={"rustmapper": {"repo": "Rust-sitemap", "entries": []}},
                      repos=[{"name": "Rust-sitemap", "head": {"sha": "3" * 40, "short": "32c2651", "date": "2026-10-07"}}],
                      runcheck={"rustmapper": {"ok": True, "date": "2026-10-09", "version": "0.1.3",
                                               "runner": "macOS arm64", "install": "prebuilt wheel",
                                               "steps": [{"id": i, "ok": True} for i in
                                                         ("install", "crawl_ctrl_c", "kill_writes_file", "export")]}})
        self.assertEqual(render_readme.survey_block(routed),
                         "<sub>The [drawing](DESIGN.md) is rustmapper 0.1.3, the release pip installs; its commands "
                         "were run on 9 Oct 2026 (macOS arm64).</sub>")
        # a run check of another release, or a failed one: the release only, no run claimed
        other = dict(routed, runcheck={"rustmapper": dict(routed["runcheck"]["rustmapper"], version="0.1.2")})
        self.assertEqual(render_readme.survey_block(other),
                         "<sub>The [drawing](DESIGN.md) is rustmapper 0.1.3, the release pip installs.</sub>")
        # review round 2: the crawl says what it ran against, from the step's own command
        step = {"id": "crawl_ctrl_c", "ok": True, "detail": "exit 0; 3 lines; keys present",
                "cmd": "rust_sitemap crawl --start-url http://127.0.0.1:<port>/ --seeding-strategy none --data-dir d"}
        # review round 6: a flag the printed block does not have is named (in words when known); where it writes is not
        self.assertEqual(render_readme.crawl_words(step), ", with seeding off, against a local 3-page site")
        self.assertEqual(render_readme.crawl_words(dict(step, cmd="rust_sitemap crawl --start-url https://x.org/")), "")
        self.assertEqual(render_readme.crawl_words(dict(step, cmd="rust_sitemap crawl --start-url http://127.0.0.1:1/ "
                                                        "--data-dir d (one SIGINT)")), " against a local 3-page site")
        odd = dict(step, cmd="rust_sitemap crawl --start-url http://127.0.0.1:1/ --seeding-strategy none --workers 4")
        self.assertEqual(render_readme.crawl_words(odd), ", with seeding off and with `--workers 4`, against a local "
                                                         "3-page site")
        # every flag the run check's crawl used and the block does not show is named or declared immaterial
        printed = {f for f, _ in render_readme.BLOCK_CRAWL_FLAGS}
        for f, v in render_readme.cmd_flags(step["cmd"]):
            if f not in printed:
                self.assertTrue((f, v) in render_readme.FLAG_WORDS or f in render_readme.IMMATERIAL, f)
        block = render_readme.install_block(self.stats, "Rust-sitemap", self.cfg)
        for f, v in render_readme.BLOCK_CRAWL_FLAGS:
            self.assertIn(f"{f} {v}", block)
        self.assertNotIn("2,032", render_readme.survey_block(full), "no commit total")
        clause = render_readme.agent_clause
        repos = {"repos": [{"name": "Rust-sitemap", "all_hands": 146, "others": [{"name": "Claude", "commits": 45, "bot": True}]},
                           {"name": "Scrapy", "all_hands": 499, "others": [
                               {"name": "google-labs-jules[bot]", "commits": 49, "bot": True},
                               {"name": "Claude", "commits": 22, "bot": True},
                               {"name": "dependabot[bot]", "commits": 8, "bot": True},
                               {"name": "A Person", "commits": 3, "bot": False}]}]}
        al = {"Rust-sitemap": "rustmapper"}
        self.assertEqual(clause(repos, ["Rust-sitemap", "Scrapy"], al),
                         "Tests and lines are counted per repository, whoever wrote them: coding agents (Claude, jules) "
                         "authored 45 of rustmapper's 146 commits and 71 of Scrapy's 499")
        self.assertEqual(clause(repos, ["Scrapy"], al).split(": ")[1],
                         "coding agents (jules, Claude) authored 71 of Scrapy's 499 commits", "dependabot is not an agent")
        self.assertEqual(clause(repos, [], al), "")
        self.assertEqual(clause(repos, ["nowhere"], al), "", "a repository without its counts is left out")
        none = {"repos": [{"name": "x", "all_hands": 9, "others": [{"name": "dependabot[bot]", "commits": 2, "bot": True}]}]}
        self.assertEqual(clause(none, ["x"]), "", "no agent commits, nothing to qualify")
        self.assertEqual([render_readme.agent_short(n) for n in ("google-labs-jules[bot]", "Claude", "Claude Haiku 4.5", "other[bot]")],
                         ["jules", "Claude", "Claude", "other"])
        self.assertEqual(render_readme.fmt_days(["2026-03-01", "2026-03-02", "2026-03-03", "2026-03-09", "2026-05-20"]),
                         "1–3 and 9 Mar 2026, 20 May 2026")
        # a thin stats.json prints only what it holds; nothing is guessed
        self.assertEqual(render_readme.survey_block({"taken": "2026-10-07", "commits": 12, "repo_count": 2}), "")
        self.assertEqual(render_readme.survey_block({}), "")
        failed = render_readme.survey_block(dict(routed, provenance={"mode": "cache-failed",
                                                                     "failed_at": "2026-10-11T06:20:00Z"}))
        self.assertIn(" The last run failed on 11 Oct 2026; these figures are from the run before.</sub>", failed)

    def test_facts_block_prints_only_present_keys(self):
        """D4 / F3.3: one plain italic line under a flagship; an absent key is omitted, never estimated."""
        full = {"repos": [{"name": "Rust-sitemap", "aliases": ["rustmapper"],
                           "manifest": {"files": ["Cargo.toml"], "deps": ["clap", "rkyv", "rkyv_derive", "redb", "reqwest", "tokio", "serde"]},
                           "tests": 3, "test_functions": 115, "workflows": 1, "main_language": "Rust",
                           "ci": {"workflow": "CI", "conclusion": "success", "date": "2026-10-07", "url": "https://x", "recent": ["success"]},
                           "lines": {"Rust": 16234, "Python": 412}, "last_ns": "2026-08-08"},
                          {"name": "Scrapy", "tests": 257, "workflows": 5,
                           "ci": {"workflow": "CI/CD", "conclusion": "failure", "date": "2026-10-08", "stale": True},
                           "lines": {"Python": 69120, "Rust": 1003}, "main_language": "Python", "last_ns": None}]}
        self.assertEqual(render_readme.facts_block(full, "rustmapper", self.cfg),
                         "*Built on tokio, redb, rkyv, reqwest, clap · 115 tests · CI passed 7 Oct 2026 · 16k lines of Rust*")
        # no test_functions, no tests item (a file count reads wrong for inline Rust tests); stale CI says so; null last_ns omitted
        self.assertEqual(render_readme.facts_block(full, "Scrapy"),
                         "*CI failed 8 Oct 2026 (last known run) · 69k lines of Python*")
        self.assertEqual(render_readme.facts_block(full, "nowhere"), "")
        self.assertEqual(render_readme.facts_block({"repos": [{"name": "Scrapy", "commits": 900, "tests": 257}]}, "Scrapy"), "",
                         "no D2 keys the line prints, no line")
        self.assertEqual(render_readme.facts_block({"repos": [{"name": "x", "test_functions": 1}]}, "x"), "*1 test*")
        self.assertEqual(render_readme.facts_block({"repos": [{"name": "x", "workflows": 2}]}, "x"), "*2 CI workflows*",
                         "workflows without a CI result")
        lang = {"repos": [{"name": "x", "lines": {"Python": 900, "Rust": 2000}, "main_language": "Python"}]}
        self.assertEqual(render_readme.facts_block(lang, "x"), "*900 lines of Python*", "main_language wins over the largest")
        self.assertEqual(render_readme.facts_block({"repos": [{"name": "x", "lines": {"Python": 900, "Rust": 2000}}]}, "x"),
                         "*2k lines of Rust*")
        # Built on: chart.toml [facts] built_on in its order, only where the manifest has it; else the first five non-helpers
        cfg = {"facts": {"built_on": {"Scrapy": ["deltalake", "Redis", "psycopg2", "prometheus_client", "not-in-manifest"]}}}
        scrapy = {"repos": [{"name": "Scrapy", "manifest": {"deps": ["scrapy", "redis", "psycopg2-binary", "deltalake", "prometheus-client"]}}]}
        self.assertEqual(render_readme.facts_block(scrapy, "Scrapy", cfg), "*Built on deltalake, Redis, psycopg2, prometheus_client*",
                         "case and -/_ ignored, a -binary build matches, an absent name is skipped")
        helpers = {"repos": [{"name": "Rust-sitemap", "manifest": {"files": ["Cargo.toml"], "deps": [
            "clap", "rkyv", "rkyv_derive", "redb", "serde-derive", "reqwest", "tokio_macros", "tokio-macros", "tokio", "url"]}}]}
        self.assertEqual(render_readme.facts_block(helpers, "Rust-sitemap"), "*Built on clap, rkyv, redb, reqwest, tokio*")
        self.assertEqual(render_readme.facts_block({"repos": [{"name": "x", "manifest": {"deps": ["derive", "macros"]}}]}, "x"),
                         "*Built on derive, macros*", "a crate named only 'derive' is not a helper")
        # every name chart.toml lists is in the committed manifest, so the configured line prints in full
        for repo, wanted in self.cfg["facts"]["built_on"].items():
            r = render_readme._repo(self.stats, repo)
            self.assertIsNotNone(r, repo)
            deps = r["manifest"]["deps"]
            for name in wanted:
                self.assertTrue(render_readme._in_manifest(name, deps), f"{repo}: {name} is not in its manifest")
            head = r["head"]["short"]
            self.assertTrue(render_readme.facts_block(self.stats, repo, self.cfg).startswith(
                f"*On main at `{head}`: built on " + ", ".join(wanted) + " · "), "review round 2: the snapshot is named")
        for name in ("Scrapy", "Rust-sitemap"):     # the committed stats.json: each printed figure is the file's own
            r, live = render_readme._repo(self.stats, name), render_readme.facts_block(self.stats, name, self.cfg)
            self.assertTrue(live.startswith("*") and live.endswith("*") and "<sub>" not in live, live)
            self.assertNotIn("test file", live)
            self.assertNotIn("last worked", live)
            if isinstance(r.get("test_functions"), int):
                self.assertIn(f" · {render_readme._plural(r['test_functions'], 'test')} · ", live, name)
            if (r.get("ci") or {}).get("conclusion") == "success":
                self.assertIn(f"CI passed {render_readme.fmt_date(r['ci']['date'])}", live)
            self.assertNotIn("last commit", live)     # round 6: the code date on the hero answers "alive"
        tmpl = ("<!-- facts:Rust-sitemap:start -->\nold\n<!-- facts:Rust-sitemap:end -->\n"
                "<!-- facts:Scrapy:start -->\n<!-- facts:Scrapy:end -->\n<!-- facts:nowhere:start -->x<!-- facts:nowhere:end -->\n")
        once = render_readme.main(tmpl, self.cfg, full, use_sheet_alts=False)
        self.assertIn("<!-- facts:Rust-sitemap:start -->\n*Built on tokio, redb, rkyv, reqwest, clap · 115 tests", once)
        self.assertIn("<!-- facts:Scrapy:start -->\n*CI failed", once)
        self.assertIn("<!-- facts:nowhere:start -->\n<!-- facts:nowhere:end -->", once, "an unknown repository prints nothing")
        self.assertEqual(render_readme.main(once, self.cfg, full, use_sheet_alts=False), once)
        self.assertEqual(render_readme.fmt_k(950), "950")
        self.assertEqual(render_readme.fmt_k(1_300_000), "1.3M")

    def test_page_sheets_and_position_inline(self):
        self.assertEqual(render_readme.page_sheets("<!-- picture:footer:start -->\n<!-- picture:hero:start -->"), ["hero", "footer"])
        self.assertEqual(render_readme.page_sheets("no pictures"), [])
        cfg = dict(self.cfg, position={"text": "open to work · UTC−5"})
        self.assertEqual(render_readme.position_block(cfg), "<i>open to work · UTC−5</i><br>")
        self.assertEqual(render_readme.position_block(self.cfg), "", "chart.toml's position is empty today")
        self.assertIn("**This profile** Code MIT", render_readme.license_block())
        # review round 4: the terms only; no "how it's built" footer (the data line's "drawing" links DESIGN.md)
        self.assertTrue(render_readme.license_block().endswith("[`scripts/fonts/`](scripts/fonts/).</sub>"))
        self.assertNotIn("chart.toml", render_readme.license_block())
        self.assertTrue(render_readme.license_block().startswith("<sub>"))

    def test_committed_readme_is_the_one_chart_page(self):
        """D1/D8: the README carries the hero's picture block and no other sheet, in the decided order."""
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            text = fh.read()
        self.assertEqual(render_readme.page_sheets(text), ["hero"])
        for sheet in ("soundings", "approaches", "log", "instruments", "footer"):
            self.assertNotIn(f"/{sheet}-day.svg", text, sheet)
        order = ["<!-- picture:hero:end -->", "<!-- position:start", '<a href="https://github.com/BenjaminSRussell/Rust-sitemap"><b>rustmapper</b></a>',
                 "<!-- contact:start", "**Ben Russell builds**", "**Languages**", "**Stack**",
                 "<!-- pick:start -->",
                 "**[rustmapper](https://github.com/BenjaminSRussell/Rust-sitemap)**: `pip install` gives you",
                 "<!-- facts:Rust-sitemap:start -->", "<!-- install:Rust-sitemap:start -->",
                 "pip install rustmapper", "Prebuilt for Apple silicon",
                 "<!-- handoffs:start -->", "**[Scrapy](https://github.com/BenjaminSRussell/Scrapy)** is a multi-stage",
                 "<!-- facts:Scrapy:start -->", "# in a clone of this repository;", "# start.py runs only from here",
                 "cd Scraping_project", "python start.py",
                 "# or only discovery, on your own site:", "docker-compose run --rm scraper", "scrapy crawl scout", "**Also**", "more repositories:", "**Working rules**",
                 "<!-- notices:start -->", "4. **Parse, don't pattern-match.**", "Found a mistake? [Open an issue]",
                 "<!-- survey:start -->", "<sub>The [drawing](DESIGN.md) is rustmapper", "Tests and lines are counted",
                 "<!-- license:start -->", "**This profile** Code MIT"]
        positions = [text.index(m) for m in order]
        self.assertEqual(positions, sorted(positions), "the page's blocks are out of D8's order")
        for gone in ("## Soundings", "## Approaches", "## Ship's log", "## Instruments", "<summary><b>Colophon</b>",
                     "5. **The surface", "editions:", "<!-- figures:start", "<!-- instruments:start", "<!-- log_lede:start",
                     # v11: the text is written straight; the theme lives in the image only
                     "survey vessel", "Other waters", "Below the waterline", "Notices to mariners", "Survey log",
                     "wrong depth", "all hands", "mark in the channel", "leaves the harbor", "sheets and copy", "redraw",
                     # round 5, D3: the real name, no worker figure until the repository agrees with itself, no "provisional"
                     "**Other repositories**", "256 and 1,024", "provisional", "pre-1.0", "<b>Data</b>",
                     # round 5, F3: the role caption repeats the sheet; no generated-by footer; facts in plain italic
                     "Crawl and data infrastructure · Python and Rust", "Generated from my repositories", "test files",
                     "last worked", "<sub>Built on",
                     # round 6: no command that fails, no last-commit date, no pun on the theme
                     "rustmapper crawl --start-url", "last commit", "Lights before speed", "100M+"):
            self.assertNotIn(gone, text, gone)
        # review round 5: no generated-by footer anywhere a reader sees ("AI-generated code" is a project's subject)
        visible = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        self.assertIsNone(re.search(r"(?<!-)\b(re)?generated\b", visible, re.I), "a generated-by footer")
        # review round 5: GitHub autolinks a bare URL, so a local address is code, not a link to the visitor's machine
        self.assertNotIn("http://localhost", visible)
        self.assertIn("`localhost:3000`", visible)
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
