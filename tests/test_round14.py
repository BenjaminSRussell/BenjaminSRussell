"""Review round 14 (docs/crit/round6/review-r14-*.md): what each fix promises, held by a test.
The Scrapy run sentence says what each stage does to a site (the spider obeys robots.txt and Crawl-delay; stage 2
fetches every queued link, disallowed ones too, 4 at a time per host, as aiohttp's default agent); the pick
sentence's politeness clause is off until stage 2 checks robots.txt and sends its own name, and comes back naming
Scrapy; the --reset-delta sentence is gone; the third Scrapy bullet says how it is run (an alert, the kill switch,
the runbook); the agent counts sit on the facts lines they qualify; the desk sheet is the mid's stacked layout 1000
wide, so its words are 14.6 px or more from 1,200 px up and 16 px at the 846 px column.
"""
from __future__ import annotations

import copy
import json
import os
import re
import shutil
import sys
import tempfile
import tomllib
import types
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import check  # noqa: E402,F401  (plug-ins import Finding from it)
import render_readme as rr  # noqa: E402
import tokens  # noqa: E402
from checks import column  # noqa: E402
from checks import figures as figures_check  # noqa: E402
from checks import route as route_check  # noqa: E402
from data import proof  # noqa: E402
from sheets import route as sheet  # noqa: E402

STATS = os.path.join(ROOT, "assets", "stats.json")
CFG = os.path.join(ROOT, "chart.toml")
README = os.path.join(ROOT, "README.md")
NB = " "


def load():
    with open(CFG, "rb") as fh:
        cfg = tomllib.load(fh)
    with open(STATS, encoding="utf-8") as fh:
        stats = json.load(fh)
    return cfg, stats


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def rows(cfg, text):
    return [f for f in cfg["figures"] if f["text"] == text]


def check_rows(figs, files):
    return proof.figure_records(figs, {"Scrapy": "fixture"}, read=lambda _gd, p: files.get(p),
                                ls=lambda _gd: list(files))


P = "Scraping_project/"
SCOUT = ('''            if content_hint == "html":
                    yield self._queue_for_javascript_spider(url, response.url)
                    yield self._queue_for_stage2(url, response.url, content_hint)

                    self.scout_stats["html_queued_js"] += 1
                    self.scout_stats["pages_queued_stage2"] += 1

                    yield scrapy.Request(
                        url,
                    )

                else:
                    yield self._queue_for_stage2(url, response.url, content_hint)
''')
STAGE2 = ('DEFAULT_STAGE2_PER_HOST_CONCURRENCY = 4\n'
          'return aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=30))\n'
          'response = await session.get(current, allow_redirects=False)\n')
FILES = {
    P + "src/stage1/scout_spider.py": SCOUT,
    P + "src/pipelines.py": '        elif target_stage == "stage2":\n',
    P + "src/stage2/stage2_worker.py": STAGE2,
    P + "src/workers/stage2_worker.py": "run_drain_loop(worker, idle_seconds=30)\n",
    P + "config.yml": "stage2:\n  max_workers: 100\n  per_host_concurrency: 4\n  batch_size: 50\n",
    P + "docker-compose.yml": "  stage2-worker:\n    command: python -m src.workers.stage2_worker\n",
    P + "Dockerfile": "FROM python:3.11-slim as base\n",
    P + "requirements.txt": "    # via aiohttp\naiohttp==3.13.1\n",
}


def files(**over):
    f = dict(FILES)
    f.update({P + k: v for k, v in over.items()})
    return f


class StageTwo(unittest.TestCase):
    """r14-1 #1, r14-2 #1, r14-3 #2: the run sentence says what each stage does to a site."""

    # review round 15 (the owner): the same form as rustmapper's list
    SENT = ("It loads no seeds: the last command gives the spider your site.\n\nBefore you run it:\n\n"
            "- The spider obeys `robots.txt` and its `Crawl-delay`, and names itself `<your-bot>` (without the `USER_AGENT` line, "
            "`UConn-Discovery-Crawler/1.0`).\n"
            "- The stage 2 worker then fetches every link the spider queued, disallowed ones too, 4 at a time per "
            "host, as `Python/3.11 aiohttp/3.13.1`.")

    def test_committed(self):
        cfg, stats = load()
        text = read(README)
        self.assertIn(self.SENT, text)
        got = {r["text"]: r for r in stats["figures"]}
        for t in ("The spider obeys `robots.txt` and its `Crawl-delay`", "disallowed ones too",
                  "4 at a time per host", "`Python/3.11 aiohttp/3.13.1`"):
            self.assertTrue(got[t]["holds"], got[t])
            self.assertIn(t, text)
        # the order a reader acts in: what it starts, what it needs, what it does to a site, then the command
        order = ["`python start.py` starts", "It needs Docker", "It loads no seeds:", "The stage 2 worker then",
                 "cd Scrapy/Scraping_project"]
        self.assertEqual([text.index(o) for o in order], sorted(text.index(o) for o in order))

    def test_rows_hold_on_the_fixture(self):
        cfg, _ = load()
        for t in ("disallowed ones too", "4 at a time per host", "`Python/3.11 aiohttp/3.13.1`"):
            self.assertTrue(check_rows(rows(cfg, t), files())[0]["holds"], (t, check_rows(rows(cfg, t), files())))

    def test_rows_fail_when_stage_two_changes(self):
        cfg, _ = load()
        dis, per, ua = (rows(cfg, t) for t in ("disallowed ones too", "4 at a time per host",
                                                "`Python/3.11 aiohttp/3.13.1`"))
        robots = files(**{"src/stage2/stage2_worker.py": STAGE2 + "if not self._robots.allowed(url):\n"})
        self.assertFalse(check_rows(dis, robots)[0]["holds"], "stage 2 checks robots.txt")
        delay = files(**{"src/stage2/stage2_worker.py": STAGE2 + "await asyncio.sleep(crawl_delay)\n"})
        self.assertFalse(check_rows(dis, delay)[0]["holds"], "stage 2 waits a Crawl-delay")
        after = SCOUT.replace("yield self._queue_for_stage2(url, response.url, content_hint)\n\n                    self",
                              "self", 1)
        self.assertFalse(check_rows(dis, files(**{"src/stage1/scout_spider.py": after}))[0]["holds"],
                         "the scout no longer queues an HTML link before its request")
        named = files(**{"src/stage2/stage2_worker.py": STAGE2.replace(
            "ClientSession(connector=connector,", "ClientSession(connector=connector, headers=HEADERS,")})
        self.assertFalse(check_rows(ua, named)[0]["holds"], "stage 2 sends its own name")
        agent = files(**{"src/stage2/stage2_worker.py": STAGE2 + 'HEADERS = {"User-Agent": UA}\n'})
        self.assertFalse(check_rows(ua, agent)[0]["holds"])
        self.assertFalse(check_rows(ua, files(**{"requirements.txt": "aiohttp==3.14.0\n"}))[0]["holds"],
                         "another aiohttp names another version")
        eight = files(**{"config.yml": FILES[P + "config.yml"].replace("per_host_concurrency: 4", "per_host_concurrency: 8")})
        self.assertFalse(check_rows(per, eight)[0]["holds"])
        env = files(**{"docker-compose.yml": FILES[P + "docker-compose.yml"] + "      - STAGE2_PER_HOST_CONCURRENCY=8\n"})
        self.assertFalse(check_rows(per, env)[0]["holds"], "compose overrides the default")


class PoliteGate(unittest.TestCase):
    """r14-1 #1: the pick clause is off while stage 2 neither checks robots.txt nor sends its own name."""

    def test_today(self):
        cfg, stats = load()
        self.assertTrue(cfg["copy"]["pick_polite"].startswith("Scrapy obeys"), "it cannot be read as rustmapper")
        out = rr.pick_block(stats, cfg)
        self.assertTrue(out.endswith("and needs Docker."), out)
        gate = next(r for r in stats["figures"] if r["text"] == "Scrapy obeys robots.txt in stage 2 too")
        self.assertFalse(gate["holds"])
        # FIGURES does not fail the gate while the clause is off the page, and does once it is printed
        ctx = types.SimpleNamespace(stats=stats, cfg=cfg, readme=read(README))
        self.assertFalse([f for f in figures_check.check(ctx) if "stage 2 too" in f.msg])
        printed = types.SimpleNamespace(stats=stats, cfg=cfg, readme=read(README).replace(
            "and needs Docker.\n<!-- pick:end -->", "and needs Docker. " + cfg["copy"]["pick_polite"] + "\n<!-- pick:end -->"))
        self.assertTrue([f for f in figures_check.check(printed) if "stage 2 too" in f.msg])

    def test_gate_on_the_fixture(self):
        cfg, _ = load()
        gate = rows(cfg, "Scrapy obeys robots.txt in stage 2 too")
        self.assertFalse(check_rows(gate, files())[0]["holds"], "no robots, no headers: fails")
        robots_only = files(**{"src/stage2/stage2_worker.py": STAGE2 + "robots = RobotFileParser()\n"})
        self.assertFalse(check_rows(gate, robots_only)[0]["holds"], "robots.txt, but still aiohttp's agent")
        both = files(**{"src/stage2/stage2_worker.py": STAGE2.replace(
            "ClientSession(connector=connector,", "ClientSession(connector=connector, headers=HEADERS,")
            + "robots = RobotFileParser()\n"})
        self.assertTrue(check_rows(gate, both)[0]["holds"], check_rows(gate, both))

    def test_present(self):
        figs = [{"text": "x", "repo": "Scrapy", "path": "a.py", "present": [{"path": "a.py", "pattern": "(?i)robots"}]}]
        self.assertTrue(check_rows(figs, {"a.py": "Robots here"})[0]["holds"])
        self.assertFalse(check_rows(figs, {"a.py": "nothing"})[0]["holds"])
        self.assertFalse(check_rows([dict(figs[0], present=[{"path": "b.py", "pattern": "x"}])], {"a.py": ""})[0]["holds"])


class ResetCut(unittest.TestCase):
    """r14-1 #2: the --reset-delta sentence and its rows are gone; the no-seeds row reads the guard."""

    def test_committed(self):
        cfg, stats = load()
        text = read(README)
        self.assertNotIn("--reset-delta", text)
        self.assertNotIn("143,208", text)
        self.assertNotIn("uconn.edu", text)
        self.assertFalse([f for f in cfg["figures"] if f.get("csv_rows")])
        row = rows(cfg, "It loads no seeds:")[0]
        self.assertIn("guarded_lake_wipe(DELTA_LAKE, args", [a["literal"] for a in row["also"]])
        self.assertTrue(next(r for r in stats["figures"] if r["text"] == "It loads no seeds:")["holds"])


class BulletThree(unittest.TestCase):
    """r14-2 #3: the third Scrapy bullet says how it is run: an alert on its own metric, the kill switch, a runbook."""

    LINE = ("- Prometheus alerts on its own metrics, such as Delta writes spilling to disk, and Grafana dashboards show them. "
            "A kill switch stops new downloads within 5" + NB + "s, with a runbook. Docker Compose and a Helm chart for "
            "Kubernetes.")

    def test_committed(self):
        cfg, stats = load()
        text = read(README)
        self.assertIn(self.LINE, text)
        got = {r["text"]: r for r in stats["figures"]}
        for t in ("Prometheus alerts on its own metrics", "Delta writes spilling to disk",
                  "stops new downloads within 5 s", "with a runbook"):
            self.assertTrue(got[t]["holds"], got[t])
        self.assertNotRegex(text, r"\b42\b", "no count of alerts")
        self.assertEqual(figures_check.uncovered(text, stats["figures"]), [])

    def test_kill_switch_row(self):
        cfg, _ = load()
        figs = rows(cfg, "stops new downloads within 5 s")
        tree = {P + "src/utils/crawl_guard.py": 'opt("kill_switch_check_secs", 5.0)',
                P + "src/stage1/middlewares/spider_config.py": '"x.CrawlGuardMiddleware": 25,',
                P + "src/stage2/stage2_worker.py": "stop = self._crawl_guard_reason()",
                P + "cli.py": "def cmd_killswitch(args):",
                P + "tests/unit/test_crawl_guard_kill_switch.py": "def test_engage():",
                P + "config.yml": "crawl_safety:\n  max_requests_per_day: 0\n"}
        self.assertTrue(check_rows(figs, tree)[0]["holds"])
        slow = dict(tree, **{P + "config.yml": "crawl_safety:\n  kill_switch_check_secs: 30\n"})
        self.assertFalse(check_rows(figs, slow)[0]["holds"], "config.yml changes the 5 s")


class AgentFacts(unittest.TestCase):
    """r14-2 #2: the agent counts beside the counts they qualify, on each facts line."""

    def test_committed(self):
        cfg, stats = load()
        text = read(README).replace(NB, " ")
        by = {r["name"]: r for r in stats["repos"]}
        for name in ("Rust-sitemap", "Scrapy"):
            a = rr.agent_counts(by[name])
            want = (f"coding agents ({', '.join(a['names'])}) authored {rr.fmt_n(a['authored'])} of its "
                    f"{rr.fmt_n(a['total'])} commits and co-signed {rr.fmt_n(a['cosigned'])} of his own "
                    f"{rr.fmt_n(a['his'])}*")
            block = text.split(f"<!-- facts:{name}:start -->", 1)[1].split(f"<!-- facts:{name}:end -->", 1)[0]
            self.assertIn(want, block)
        self.assertIn("authored 45 of its 146 commits and co-signed 1 of his own 101", text)
        self.assertIn("authored 71 of its 499 commits and co-signed 30 of his own 420", text)
        data = text.split("<!-- survey:start -->", 1)[1].split("<!-- survey:end -->", 1)[0]
        self.assertIn("Tests and lines are counted per repository, whoever wrote them.</sub>", data)
        self.assertNotIn("authored", data)

    def test_none(self):
        r = {"name": "x", "all_hands": 10, "commits": 9, "others": [{"name": "dependabot[bot]", "commits": 1, "bot": True}],
             "coauthored": {"agent": 2}}
        self.assertEqual(rr.agent_clause(r), "", "no agent commit: no clause, not '0 of'")
        self.assertNotIn("0 of", rr.facts_block({"repos": [dict(r, lines={"Go": 100})]}, "x"))
        self.assertEqual(rr.survey_block({"repos": [r]}, repos=["x"]), "")


class DeskStacked(unittest.TestCase):
    """r14-3 #1: from 1,200 px the desk sheet is the mid's stacked layout, 1000 wide."""

    def test_geometry(self):
        self.assertEqual(sheet.SIZES["desk"][0], 1000)
        self.assertEqual(sheet.L["desk"], sheet.L["mid"])
        self.assertIsNot(sheet.L["desk"], sheet.L["mid"])
        self.assertEqual(route_check.HEIGHT["desk"], 770)

    def test_desk_px(self):
        readme = read(README)
        old = {"hero-day": {"w": 1280, "h": 571, "text": [{"size": 19}]},
               "hero-mid-day": {"w": 820, "h": 707, "text": [{"size": 19}]},
               "hero-phone-day": {"w": 600, "h": 1121, "text": [{"size": 26}]}}
        bad = column.desk_small(readme, old, 1200)
        self.assertTrue(bad)
        self.assertAlmostEqual(next(b[2] for b in bad if b[0] == 1280), 19 * 846 / 1280)
        new = copy.deepcopy(old)
        new["hero-day"].update(w=1000, h=707)
        self.assertEqual(column.desk_small(readme, new, 1200), [])
        self.assertAlmostEqual(19 * column.column_px(1200) / 1000, 14.554, places=2)
        self.assertGreaterEqual(19 * column.column_px(1920) / 1000, column.DESK_FULL_PX)
        ctx = types.SimpleNamespace(report={"sheets": old}, readme=readme, cfg={"chart": {"breakpoint_px": 1199}})
        self.assertIn("DESK-PX", [f.code for f in column.check(ctx)])
        ctx.report = {"sheets": new}
        self.assertNotIn("fail", [f.level for f in column.check(ctx) if f.code == "DESK-PX"])

    def test_build(self):
        import build_assets
        sheet._register_hook()        # the report hook registers with build_assets once it is imported
        tmp = tempfile.mkdtemp(prefix="r14-desk-")
        try:
            rep = os.path.join(tmp, "report.json")
            build_assets.main(sheets=["hero"], editions=None, out=os.path.join(tmp, "assets"), report_path=rep,
                              stats_path=STATS, cfg_path=CFG, quiet=True)
            with open(rep, encoding="utf-8") as fh:
                report = json.load(fh)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        desk, mid = report["sheets"]["hero-day"], report["sheets"]["hero-mid-day"]
        self.assertEqual(desk["w"], 1000)
        self.assertEqual(desk["h"], mid["h"], "the same lines as the mid")
        self.assertLessEqual(desk["h"], route_check.HEIGHT["desk"])
        self.assertEqual(desk["route"]["drawn"], mid["route"]["drawn"], "the same elements")
        self.assertEqual(sorted(desk["purpose"]), sorted(mid["purpose"]), "T-PURPOSE: the same IDs")
        self.assertEqual(report["sheets"]["hero-night"]["w"], 1000)

    def test_design_md(self):
        md = " ".join(tokens.design_md().split())
        self.assertIn("the desk sheet, the mid's layout 1000 wide, from 1200.", md)
        self.assertIn("at 1200 the desk sheet's is 14.6 px (16.1 px at the 846 px column", md)


if __name__ == "__main__":
    unittest.main()
