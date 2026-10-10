"""Review round 13 (docs/crit/round6/review-r13-*.md): what each fix promises, held by a test.

Working rule 1 says "5 URLs in a row" and rests on the breaker's reset; the cautions you act on before you run stay
open and the four about the files go in one labelled fold, at most 7 items a list; the cautions run in the drawing's
order; W1 says what saving as it goes buys, in one line on every edition; DESIGN.md says which cautions a probe ran;
the Scrapy command names who it says it is and gives the lever; the pick sentence says Scrapy obeys robots.txt,
Crawl-delay and Retry-After, and drops that clause when a row fails.
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
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import check  # noqa: E402,F401  (plug-ins import Finding from it)
import build_assets  # noqa: E402
import render_readme as rr  # noqa: E402
import tokens  # noqa: E402
from checks import readme as readme_check  # noqa: E402
from data import proof  # noqa: E402
from data import route as R  # noqa: E402

STATS = os.path.join(ROOT, "assets", "stats.json")
CFG = os.path.join(ROOT, "chart.toml")
README = os.path.join(ROOT, "README.md")
DESIGN = os.path.join(ROOT, "DESIGN.md")


def load():
    with open(CFG, "rb") as fh:
        cfg = tomllib.load(fh)
    with open(STATS, encoding="utf-8") as fh:
        stats = json.load(fh)
    return cfg, stats


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def install(text):
    return text.split("<!-- install:Rust-sitemap:start -->", 1)[1].split("<!-- install:Rust-sitemap:end -->", 1)[0]


def drawn(stats, rc=None):
    return {e["id"]: e for e in R.drawn(stats["routes"]["rustmapper"], rc or stats["runcheck"]["rustmapper"])}


def rows(cfg, text):
    return [f for f in cfg["figures"] if f["text"] == text]


def check_rows(figs, files):
    """figure_records over a fixture tree for the Scrapy repository."""
    return proof.figure_records(figs, {"Scrapy": "fixture"}, read=lambda _gd, p: files.get(p),
                                ls=lambda _gd: list(files))


RETRY = '''class CircuitBreaker:
    def __init__(self):
        self.failure_count = 0
        self.state = "closed"

    def record_success(self):
        if self.state == "half-open":
            self.success_count += 1
        else:
            self.failure_count = 0

    def record_failure(self):
        self.failure_count += 1
'''
STAGE2 = "DEFAULT_STAGE2_BREAKER_FAILURES = 5\nself._host_breakers = {}\n                breaker.record_success()\n"


class RuleOne(unittest.TestCase):
    """r13-1 #1: the breaker counts failures in a row; one success puts the count back to zero."""

    def test_committed(self):
        cfg, stats = load()
        body = sorted(cfg["notices"], key=lambda n: n["n"])[0]["body"]
        self.assertTrue(body.startswith("When 5 URLs in a row on one host fail every retry, that host is left alone "
                                        "for 60 s"), body)
        self.assertIn("When 5 URLs in a row on one host fail every retry", read(README).replace(" ", " "))
        (row,) = rows(cfg, "5 URLs in a row on one host")
        self.assertIn({"path": "Scraping_project/src/utils/retry.py",
                       "literal": "        else:\n            self.failure_count = 0\n\n    def record_failure"}, row["also"])
        got = {r["text"]: r for r in stats["figures"]}
        self.assertTrue(got["5 URLs in a row on one host"]["holds"])
        self.assertNotIn("5 URLs on one host", got)

    def test_reset_anchor_bites(self):
        cfg, _ = load()
        figs = rows(cfg, "5 URLs in a row on one host")
        files = {"Scraping_project/src/stage2/stage2_worker.py": STAGE2, "Scraping_project/src/utils/retry.py": RETRY}
        self.assertTrue(check_rows(figs, files)[0]["holds"], check_rows(figs, files)[0]["why"])
        no_reset = RETRY.replace("        else:\n            self.failure_count = 0\n", "")
        self.assertFalse(check_rows(figs, dict(files, **{"Scraping_project/src/utils/retry.py": no_reset}))[0]["holds"],
                         "a breaker that keeps its count across successes is not 'in a row'")
        no_call = STAGE2.replace("breaker.record_success()", "pass")
        self.assertFalse(check_rows(figs, dict(files, **{"Scraping_project/src/stage2/stage2_worker.py": no_call}))[0]
                         ["holds"], "stage 2 must report each success")


class Fold(unittest.TestCase):
    """r13-1 #2: the cautions you act on stay open; what the files hold goes in one labelled fold; 7 a list."""

    OPEN = ["L1", "L4", "L2", "L5"]
    FOLD = ["L3", "X3", "X2", "X1"]

    def test_cap(self):
        self.assertEqual(rr.LIST_MAX_ITEMS, 7)

    def test_committed(self):
        cfg, stats = load()
        body = install(read(README))
        head, rest = body.split("<details>", 1)
        fold, after = rest.split("</details>", 1)
        self.assertTrue(after.lstrip().startswith("```sh"), "the fold sits right before the code block")
        self.assertIn("<summary>What 0.1.3's files miss or get wrong</summary>", fold)
        rows_ = drawn(stats)
        open_items = [ln[2:] for ln in head.split("Before you run 0.1.3:", 1)[1].splitlines() if ln.startswith("- ")]
        fold_items = [ln[2:] for ln in fold.splitlines() if ln.startswith("- ")]
        line = lambda gid: rr.lever_line(rr.keep_together(rows_[gid]["text"]))     # noqa: E731
        self.assertEqual(open_items, [line(g) for g in self.OPEN])
        self.assertEqual(fold_items, [line(g) for g in self.FOLD])
        for gid in self.FOLD:
            self.assertTrue(rows_[gid].get("fold"), gid)
        for gid in self.OPEN:
            self.assertFalse(rows_[gid].get("fold"), gid)
            # each open item has its lever (a flag, or where to start) or is L4, which says what the release ignores
            self.assertTrue("<br>`--" in line(gid) or "Start at" in line(gid) or gid == "L4", gid)
        self.assertEqual(readme_check.cautions(read(README), rr.LIST_MAX_ITEMS), [])
        self.assertEqual(readme_check.cautions_placed(read(README), stats), [])
        self.assertEqual(readme_check.cautions_scope(read(README), stats), [])

    def test_no_folded_item_in_the_open_list(self):
        _, stats = load()
        route = copy.deepcopy(stats["routes"]["rustmapper"])
        blocks = rr.text_blocks(route, stats["runcheck"]["rustmapper"], stats["edition"])
        open_list = next(b for b in blocks if b.startswith("Before you run"))
        for e in R.drawn(route, stats["runcheck"]["rustmapper"]):
            if e.get("fold"):
                self.assertNotIn(e["text"][:40], open_list, e["id"])

    def test_the_check_bites(self):
        _, stats = load()
        text = read(README)
        body = install(text)
        x1 = next(ln for ln in body.splitlines() if ln.startswith("- Its `sitemap.xml`"))
        moved = text.replace(x1 + "\n", "", 1).replace("- From `www.<site>`", x1 + "\n- From `www.<site>`", 1)
        msgs = " ".join(readme_check.cautions_placed(moved, stats))
        self.assertIn("X1 is not printed inside the fold", msgs)
        gone = text.replace(x1 + "\n", "", 1)
        self.assertIn("X1 is not printed", " ".join(readme_check.cautions_placed(gone, stats)))
        eight = text.replace("- From `www.<site>`", "\n".join(["- a b c"] * 4) + "\n- From `www.<site>`", 1)
        self.assertIn("8 items in the list (at most 7)", " ".join(readme_check.cautions(eight, 7)))

    def test_no_label_no_fold(self):
        _, stats = load()
        route = copy.deepcopy(stats["routes"]["rustmapper"])
        route.pop("fold_lead")
        blocks = rr.text_blocks(route, stats["runcheck"]["rustmapper"], stats["edition"])
        self.assertFalse(any("<details>" in b for b in blocks))


class Order(unittest.TestCase):
    """r13-2 #2: the cautions run in the order of the drawing above them."""

    def test_committed(self):
        cfg, stats = load()
        stages = list(R.STAGES)
        items = [e for e in cfg["route"]["rustmapper"]["entry"] if e.get("item")]
        self.assertEqual([e["id"] for e in items], ["L1", "L4", "L2", "L5", "L3", "X3", "X2", "X1"])
        for e in items:
            self.assertIn(e.get("stage"), stages, e["id"])
            self.assertTrue(e.get("short"), e["id"])
        body = install(read(README))
        rows_ = drawn(stats)
        printed = [ln[2:] for ln in body.splitlines() if ln.startswith("- ")]
        by_line = {rr.lever_line(rr.keep_together(e["text"])): e for e in rows_.values() if e.get("item")}
        order = [stages.index(by_line[p]["stage"]) for p in printed]
        self.assertEqual(order, sorted(order), "the rendered items run in non-decreasing stage order")
        self.assertEqual(by_line[printed[-1]]["id"], "X1", "the export caution sits right above the export command")

    def test_the_check_bites(self):
        _, stats = load()
        text = read(README)
        body = install(text)
        x3 = next(ln for ln in body.splitlines() if ln.startswith("- After a redirect"))
        x1 = next(ln for ln in body.splitlines() if ln.startswith("- Its `sitemap.xml`"))
        swapped = text.replace(x3, "\0").replace(x1, x3).replace("\0", x1)
        self.assertIn("stage order", " ".join(readme_check.cautions_placed(swapped, stats)))

    def test_stage_is_checked(self):
        spec = {"repo": "x", "entry": [{"id": "Z", "kind": "text", "item": True, "stage": "harbour", "text": "x."}]}
        with self.assertRaises(ValueError):
            R.verify_route(spec, None, None, None, None)


class WriteRow(unittest.TestCase):
    """r13-1 #3, r13-3 #3: W1 says what saving as it goes buys, true after a kill, in one line on every edition."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="r13-")
        report = os.path.join(cls.tmp, "build-report.json")
        n = build_assets.main(sheets=["hero"], out=os.path.join(cls.tmp, "v9"), report_path=report,
                              stats_path=STATS, cfg_path=CFG, quiet=True)
        assert n == 0, n
        with open(report, encoding="utf-8") as fh:
            cls.sheets = json.load(fh)["sheets"]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_committed(self):
        _, stats = load()
        w1 = drawn(stats)["W1"]
        self.assertEqual(w1["text"], "saved as it goes; export works after a kill")
        self.assertEqual((w1["runs"], w1["fails"]), (["export_after_kill"], ["kill_writes_file"]))
        self.assertNotIn("keeps the crawl", w1["text"])
        self.assertNotIn("redb", w1["text"])

    def test_one_line_everywhere(self):
        self.assertEqual(len(self.sheets), 6)
        for name, ent in self.sheets.items():
            w1 = next(s for s in ent["route"]["steps"] if s["id"] == "W1")
            self.assertEqual(w1["lines"], 1, name)
        self.assertEqual(self.sheets["hero-phone-day"]["route"]["height"], 1121)

    def test_kill_that_writes_brings_the_old_words_back(self):
        _, stats = load()
        rc = copy.deepcopy(stats["runcheck"]["rustmapper"])
        next(s for s in rc["steps"] if s["id"] == "kill_writes_file")["ok"] = True
        self.assertEqual(drawn(stats, rc)["W1"]["text"], "logged to disk, then saved to redb, in batches")
        rc = copy.deepcopy(stats["runcheck"]["rustmapper"])
        next(s for s in rc["steps"] if s["id"] == "export_after_kill")["ok"] = False
        self.assertEqual(drawn(stats, rc)["W1"]["text"], "logged to disk, then saved to redb, in batches")

    def test_design_opening_follows(self):
        self.assertIn("“saved as it goes”", read(DESIGN))
        self.assertNotIn("saved to redb", read(DESIGN))


class DesignProbed(unittest.TestCase):
    """r13-2 #1: DESIGN.md says which cautions a probe ran and which were checked in the code only."""

    def test_committed(self):
        _, stats = load()
        items = [e for e in drawn(stats).values() if e.get("kind") == "text" and e.get("item")]
        bare = [e for e in items if not (e.get("runs") or e.get("fails"))]
        self.assertEqual((len(items), len(bare)), (8, 3))
        self.assertEqual(sorted(e["id"] for e in bare), ["L2", "L3", "L5"])
        sentence = tokens.probed(stats)
        self.assertEqual(sentence, "Its probes test 5 of the 8 cautions the README prints; the other 3 (seeding, the www "
                                   "scope, JavaScript) are checked in the code only")
        self.assertIn(sentence + ".", read(DESIGN))
        self.assertNotIn("check each caution", read(DESIGN))

    def test_counts_follow_the_route(self):
        _, stats = load()
        s = copy.deepcopy(stats)
        x3 = next(e for e in s["routes"]["rustmapper"]["entries"] if e["id"] == "X3")
        x3["runs"] = []
        self.assertEqual(tokens.probed(s), "Its probes test 4 of the 8 cautions the README prints; the other 4 "
                                           "(seeding, the www scope, JavaScript, redirects) are checked in the code only")
        for e in s["routes"]["rustmapper"]["entries"]:
            if e.get("item"):
                e["runs"], e["fails"] = ["x"], []
        steps = s["runcheck"]["rustmapper"]["steps"]
        steps.append({"id": "x", "ok": True, "cmd": "x"})
        self.assertEqual(tokens.probed(s), "Its probes test every caution the README prints")


SETTINGS = 'USER_AGENT = _scrapy_config.get("user_agent", "UConn-Discovery-Crawler/1.0")\n'
CONFIG = "redis:\n  host: localhost\nstage1:\n  spiders:\n    scout:\n      concurrent_requests: 1024\n"
SPIDER_CONFIG = ('"ROBOTSTXT_OBEY": bool(spider_config.get("robotstxt_obey", True)),\n'
                 '"scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware": None,\n'
                 '"src.stage1.middlewares.robots_middleware.PoliteRobotsTxtMiddleware": 100,\n'
                 '"src.stage1.middlewares.retry_after_middleware.RetryAfterMiddleware": 560,\n')


class UserAgent(unittest.TestCase):
    """r13-3 #1: the page's Scrapy command says who it is, and gives the lever."""

    def files(self, **over):
        f = {"Scraping_project/src/settings.py": SETTINGS, "Scraping_project/config.yml": CONFIG,
             "Scraping_project/src/stage1/middlewares/spider_config.py": SPIDER_CONFIG}
        f.update(over)
        return f

    def test_committed(self):
        cfg, stats = load()
        text = read(README)
        self.assertIn("The last command crawls your site as `<your-bot>`; without that line, its requests say "
                      "`UConn-Discovery-Crawler/1.0`.", text)
        block = text.split("python start.py\n", 1)[1].split("```", 1)[0]
        self.assertIn("  scraper scrapy crawl scout \\\n  -s USER_AGENT=<your-bot> \\\n  -a allowed_domains=", block)
        self.assertTrue(all(len(ln) <= readme_check.CODE_COLUMNS for ln in block.splitlines()))
        got = {r["text"]: r for r in stats["figures"]}
        self.assertTrue(got["`UConn-Discovery-Crawler/1.0`"]["holds"])

    def test_retires_with_a_config(self):
        cfg, _ = load()
        figs = rows(cfg, "`UConn-Discovery-Crawler/1.0`")
        self.assertTrue(check_rows(figs, self.files())[0]["holds"])
        named = self.files(**{"Scraping_project/config.yml": CONFIG + "scrapy:\n  user_agent: x\n"})
        self.assertFalse(check_rows(figs, named)[0]["holds"], "a scrapy: section can name another agent")
        other = self.files(**{"Scraping_project/src/settings.py": SETTINGS.replace("UConn-Discovery-Crawler/1.0",
                                                                                  "Scrapy-discovery/1.0")})
        self.assertFalse(check_rows(figs, other)[0]["holds"], "a new default")
        spider = self.files(**{"Scraping_project/src/stage1/middlewares/spider_config.py":
                               SPIDER_CONFIG + '"USER_AGENT": "x",\n'})
        self.assertFalse(check_rows(figs, spider)[0]["holds"], "the scout's own settings")


class Politeness(unittest.TestCase):
    """r13-3 #2: the pick sentence says Scrapy obeys robots.txt and its Crawl-delay and waits out a Retry-After."""

    CLAUSE = "It obeys `robots.txt` and its `Crawl-delay`, and waits out a `Retry-After`."

    def files(self, **over):
        f = {"Scraping_project/src/stage1/middlewares/spider_config.py": SPIDER_CONFIG,
             "Scraping_project/src/stage1/scout_spider.py": 'custom_settings = get_spider_settings("scout")\n',
             "Scraping_project/config.yml": CONFIG,
             "Scraping_project/tests/unit/stage1/test_robots_policy.py":
                 "def test_disallowed_path_is_never_requested_and_crawl_delay_is_capped():\n",
             "Scraping_project/tests/unit/stage1/test_retry_after.py": "# Retry-After\n"}
        f.update(over)
        return f

    def test_committed(self):
        cfg, stats = load()
        self.assertEqual(cfg["copy"]["pick_polite"], self.CLAUSE)
        self.assertIn("and needs Docker. " + self.CLAUSE + "\n<!-- pick:end -->", read(README))
        self.assertEqual(len([f for f in cfg["figures"] if f.get("use") == "pick_polite"]), 3)

    def test_rows_hold_on_the_fixture(self):
        cfg, _ = load()
        figs = [f for f in cfg["figures"] if f.get("use") == "pick_polite"]
        self.assertTrue(all(r["holds"] for r in check_rows(figs, self.files())), check_rows(figs, self.files()))
        off = self.files(**{"Scraping_project/config.yml": CONFIG + "      robotstxt_obey: false\n"})
        self.assertFalse(check_rows(figs, off)[0]["holds"], "robots.txt turned off under the scout")

    def test_clause_drops_when_a_row_fails(self):
        cfg, stats = load()
        self.assertTrue(rr.pick_block(stats, cfg).endswith(self.CLAUSE))
        s = copy.deepcopy(stats)
        next(r for r in s["figures"] if r.get("use") == "pick_polite")["holds"] = False
        out = rr.pick_block(s, cfg)
        self.assertNotIn("robots.txt", out)
        self.assertTrue(out.endswith("and needs Docker."), "the rest of the sentence stays")
        s = copy.deepcopy(stats)
        s["figures"] = [r for r in s["figures"] if r.get("text") != "its `Crawl-delay`"]
        self.assertNotIn("Crawl-delay", rr.pick_block(s, cfg), "a missing row is a failed row")


if __name__ == "__main__":
    unittest.main()
