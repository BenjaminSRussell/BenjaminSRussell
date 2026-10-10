"""Review round 16 (docs/crit/round6/review-r16-*.md): what each fix promises, held by a test.

H1 says when to quit, not that the crawl is done, because H0 one row up can stall it; H0 says what waits, in the
visitor's words. L6 gives the stall's sign, the fold says that a page never reached is a blank row too, and the code
block counts the blank rows, on a probe that checks the count. The fold says 0.1.3's sitemap.xml keeps the disallowed
pages it fetched, on a probe. Scrapy's "deduplicated" rests on the URL dedup that runs, and bullet 2 no longer names
MinHash. The dotted line has paper round its words sideways (BOX-PAD). C1 gives the instruction first. The Scrapy
block's pronouns and lists are repaired, and the page has no serial comma.
"""
from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import tomllib
import types
import unittest
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import build_assets  # noqa: E402  (before sheets.route, which registers its report hook on it)
import check  # noqa: E402,F401  (plug-ins import Finding from it)
import render_readme as rr  # noqa: E402
import runcheck  # noqa: E402
from checks import audit_cover, boxpad, strings  # noqa: E402
from data import route as R  # noqa: E402
from sheets import route as sheet  # noqa: E402

STATS = os.path.join(ROOT, "assets", "stats.json")
CFG = os.path.join(ROOT, "chart.toml")
README = os.path.join(ROOT, "README.md")
DESIGN = os.path.join(ROOT, "DESIGN.md")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def load():
    with open(CFG, "rb") as fh:
        cfg = tomllib.load(fh)
    return cfg, json.loads(read(STATS))


def entry(cfg, gid):
    return copy.deepcopy(next(e for e in cfg["route"]["rustmapper"]["entry"] if e["id"] == gid))


def drawn():
    _, stats = load()
    return {e["id"]: e for e in R.drawn(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"])}


def steps():
    _, stats = load()
    return {s["id"]: s for s in stats["runcheck"]["rustmapper"]["steps"]}


def install_text():
    text = read(README)
    return text.split("<!-- install:Rust-sitemap:start -->", 1)[1].split("<!-- install:Rust-sitemap:end -->", 1)[0]


def scrapy_text():
    text = read(README)
    return text.split("**[Scrapy](https://github.com/BenjaminSRussell/Scrapy)** is", 1)[1].split('<a name="also">', 1)[0]


class QuitNotDone(unittest.TestCase):
    """r16-1 #1: after a stall the lines stop too, so H1 says when to quit."""

    def test_committed(self):
        d = drawn()
        self.assertIn("quit when `Received work item` lines stop for 60 s", d["H1"]["text"])
        self.assertNotIn("done when", d["H1"]["text"])

    def test_pairing(self):
        cfg, _ = load()
        d = drawn()
        if "H0" in d and not d["H0"].get("retired"):
            self.assertNotIn("done", d["H1"]["text"].lower())
        for c in [entry(cfg, "H1")] + entry(cfg, "H1").get("instead", []):
            self.assertNotIn("done when", c["text"])


class StallWords(unittest.TestCase):
    """r16-1 #3, r16-2 #4: H0 says what waits, not that the host stalls."""

    def test_committed(self):
        d = drawn()
        self.assertEqual(d["H0"]["text"], "on https, pages behind a disallowed link wait")
        self.assertNotIn("stalls its host", read(README) + read(DESIGN))
        self.assertIn("“on https, pages behind a disallowed link wait”", read(DESIGN))
        self.assertNotIn("stalls its host", sheet.PURPOSE["H0"][0].replace('"stalls its host"', ""))


class Sign(unittest.TestCase):
    """r16-1 #2, r16-3 #3: L6 names the line the terminal shows, and has its "that"."""

    def test_committed(self):
        d = drawn()
        self.assertIn("a link that `robots.txt` disallows", d["L6"]["text"])
        self.assertIn("`blocked by robots.txt`", d["L6"]["text"])
        self.assertLessEqual(len(d["L6"]["text"].split()), rr.LIST_MAX_WORDS)
        self.assertIn("The sign: `blocked by robots.txt`.", install_text())

    def test_the_sign_is_in_the_anchor(self):
        cfg, _ = load()
        lit = [a["text"] for a in entry(cfg, "L6")["release"] if "text" in a]
        self.assertTrue(any("blocked by robots.txt" in t for t in lit), lit)


class BlankRows(unittest.TestCase):
    """r16-2 #1, r16-1 #2: a page never reached is a blank row too, and the block counts them."""

    def test_fold(self):
        d = drawn()
        self.assertIn("pages never reached", d["X2"]["text"])
        self.assertIn("pages never reached are left blank", install_text())
        self.assertLessEqual(len(d["X2"]["text"].split()), rr.LIST_MAX_WORDS)
        self.assertIn("blank_rows", d["X2"]["runs"])

    def test_code_block(self):
        code = install_text().split("```sh", 1)[1].split("```", 1)[0].splitlines()
        at = code.index("# count the blank rows")
        self.assertEqual(code[at + 1:at + 3], ["grep -c '\"crawled_at\":null' \\", "  data/sitemap.jsonl"])
        self.assertTrue(all(len(ln) <= 32 for ln in code))
        self.assertLess(code.index("# for 60 s, then Ctrl-C once"), at)
        self.assertLess(at, code.index("# sitemap.xml, even after a kill"))

    def test_committed_probe(self):
        st = steps()
        self.assertTrue(st["blank_rows"]["ok"], st["blank_rows"])
        self.assertIn("6 never asked for", st["blank_rows"]["detail"])
        self.assertIn("counts 6", st["blank_rows"]["detail"])
        ids = list(st)
        self.assertEqual(ids.index("blank_rows"), ids.index("robots_stall") + 1)

    def test_verdict(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "sitemap.jsonl"
            p.write_text('{"url":"https://localhost/","crawled_at":1,"status_code":200}\n'
                         '{"url":"https://localhost/a.html","crawled_at":null,"status_code":null}\n')
            ok, skipped, detail = runcheck.blank_verdict([(0.0, "/")], p)
            self.assertTrue(ok and not skipped, detail)
            # a page never asked for, but written with a time: the blank is not what it says
            p.write_text('{"url":"https://localhost/","crawled_at":1,"status_code":200}\n'
                         '{"url":"https://localhost/a.html","crawled_at":5,"status_code":null}\n')
            self.assertFalse(runcheck.blank_verdict([(0.0, "/")], p)[0])
            # pretty-printed JSON: the README's grep would count nothing
            p.write_text('{"url":"https://localhost/","crawled_at":1}\n{"url":"https://localhost/a.html", '
                         '"crawled_at": null}\n')
            self.assertFalse(runcheck.blank_verdict([(0.0, "/")], p)[0])
            # every page reached: nothing to show
            self.assertTrue(runcheck.blank_verdict([(0.0, "/"), (0.1, "/a.html")], p)[1])
            self.assertTrue(runcheck.blank_verdict([], Path(tmp) / "none.jsonl")[1])

    def test_lines_follow_gate_and_probe(self):
        gate = {"blank_rows": {"ok": True, "values": {"arg:data_dir": "./data"}}}
        self.assertEqual(rr.blank_lines({"blank_rows": {"ok": True}}, gate)[1:],
                         ["# count the blank rows", "grep -c '\"crawled_at\":null' \\", "  data/sitemap.jsonl"])
        self.assertEqual(rr.blank_lines({"blank_rows": {"ok": False, "skipped": True}}, gate)[0], "")
        self.assertEqual(rr.blank_lines({"blank_rows": {"ok": False}}, gate), [], "a failed probe drops it")
        self.assertEqual(rr.blank_lines({}, gate), [], "no probe, no line")
        self.assertEqual(rr.blank_lines({"blank_rows": {"ok": True}}, {"blank_rows": {"ok": False}}), [])

    def test_x2_without_https(self):
        cfg, stats = load()
        rc = copy.deepcopy(stats["runcheck"]["rustmapper"])
        for s in rc["steps"]:
            if s["id"] == "blank_rows":
                s.update(ok=False, skipped=True)
        x2 = {e["id"]: e for e in R.resolve(stats["routes"]["rustmapper"], rc)}["X2"]
        self.assertTrue(x2["verified"] and x2["wording"] == 1, x2)
        self.assertIn("pages never reached", x2["text"])


class SitemapKeepsDisallowed(unittest.TestCase):
    """r16-2 #2: 0.1.3's sitemap.xml lists the disallowed pages it fetched."""

    def test_committed(self):
        d = drawn()
        self.assertIn("It keeps `noindex`, canonicalized and disallowed pages.", d["X1"]["text"])
        self.assertLessEqual(len(d["X1"]["text"].split()), rr.LIST_MAX_WORDS)
        st = steps()
        self.assertTrue(st["sitemap_keeps_disallowed"]["ok"])
        self.assertIn("10 of the 10 disallowed pages", st["sitemap_keeps_disallowed"]["detail"])
        ids = list(st)
        self.assertEqual(ids.index("sitemap_keeps_disallowed"), ids.index("robots_late") + 1)

    def test_anchor(self):
        cfg, _ = load()
        x1 = entry(cfg, "X1")
        self.assertIn({"path": "src/main.rs", "fn": "run_export_sitemap_command", "absent": "robots"}, x1["release"])

    def test_verdict(self):
        fetched = ["/secret1.html", "/secret2.html"]
        self.assertTrue(runcheck.disallowed_verdict(["index.html", "secret1.html", "secret2.html"], fetched)[0])
        self.assertFalse(runcheck.disallowed_verdict(["index.html", "secret1.html"], fetched)[0])
        self.assertFalse(runcheck.disallowed_verdict([], [])[0])

    def test_fallbacks(self):
        _, stats = load()
        for state, want in (({"ok": False, "skipped": True}, 1), ({"ok": False}, 2)):
            rc = copy.deepcopy(stats["runcheck"]["rustmapper"])
            for s in rc["steps"]:
                if s["id"] == "sitemap_keeps_disallowed":
                    s.pop("skipped", None)
                    s.update(state)
            x1 = {e["id"]: e for e in R.resolve(stats["routes"]["rustmapper"], rc)}["X1"]
            self.assertTrue(x1["verified"], x1)
            self.assertEqual(x1["wording"], want)
            self.assertNotIn("disallowed", x1["text"])


class ScrapyDedup(unittest.TestCase):
    """r16-2 #3: bullet 2 says only what runs; "deduplicated" rests on the URL dedup."""

    def test_committed(self):
        t = scrapy_text()
        self.assertNotIn("MinHash", t)
        self.assertIn("- Repeat URLs are dropped by their hash. In stage 3", t)
        cfg, stats = load()
        row = next(f for f in cfg["figures"] if f["text"] == "deduplicated")
        self.assertNotEqual(row.get("literal"), "MinHashLSH")
        self.assertIn("RFPDupeFilter", row["literal"])
        rec = next(f for f in stats["figures"] if f["text"] == "deduplicated")
        self.assertTrue(rec["holds"], rec)
        self.assertIn("deduplicated and summarized", read(README))


class ScrapyCopy(unittest.TestCase):
    """r16-3 #4: the Scrapy block's zeugma, pronouns and lists."""

    def test_committed(self):
        t = scrapy_text()
        self.assertIn("and Grafana dashboards show them.", t)
        self.assertIn("The crawl's output lands in Delta tables under `data/delta/`", t)
        self.assertIn("Run the commands below from the folder you cloned", t)
        self.assertIn("(without the `USER_AGENT` line, `UConn-Discovery-Crawler/1.0`)", t)
        self.assertIn("starts PostgreSQL, Redis, Prometheus, Grafana and a worker for each of the four stages", t)
        for gone in ("What it writes", "that line,", "Run these"):
            self.assertNotIn(gone, t)

    def test_prometheus_is_anchored(self):
        cfg, stats = load()
        row = next(f for f in cfg["figures"] if f["text"] == "a worker for each of the four stages")
        self.assertIn({"path": "Scraping_project/docker-compose.yml", "literal": "\n  prometheus:"}, row["also"])
        self.assertTrue(next(f for f in stats["figures"] if f["text"] == row["text"])["holds"])


class SerialComma(unittest.TestCase):
    """r16-3 #5: no comma before "and" in a list, as everywhere else on the page."""

    def test_committed(self):
        text = read(README)
        self.assertIn("raw-first storage and the dashboards that watch them", text)
        self.assertIn("what it does with each page and how to stop it.", text)
        self.assertNotIn("storage, and the", text)
        self.assertNotIn("each page, and how", text)


class StepFirst(unittest.TestCase):
    """r16-3 #2: C1 gives the instruction, then the warning with its own subject."""

    def test_committed(self):
        d = drawn()
        self.assertEqual(d["C1"]["text"],
                         "press Ctrl-C once and wait for `Saved to`; a second press quits without writing the file")


class Breaks(unittest.TestCase):
    """r16-2 #5: BREAKS gives no reason for a mark that is not drawn."""

    def test_no_log_row(self):
        row = next(b for b in sheet.BREAKS if b[0] == "Order is position; the loop is a line")
        self.assertNotIn("and the log", row[1])
        self.assertIn("the crawl that never exits", row[1])
        self.assertNotIn("under the log", sheet.__doc__)


class BoxPad(unittest.TestCase):
    """r16-1 #4: paper round the words inside the dotted line, sideways only."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        out = os.path.join(cls.tmp.name, "o")
        rep = os.path.join(cls.tmp.name, "r.json")
        n = build_assets.main(sheets=["hero"], out=out, report_path=rep, stats_path=STATS, cfg_path=CFG, quiet=True)
        assert n == 0
        cls.report = json.loads(read(rep))
        cls.svgs = {f[:-4]: os.path.join(out, f) for f in os.listdir(out) if f.endswith(".svg")}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def ctx(self, report=None):
        return types.SimpleNamespace(report=report or self.report, svgs=self.svgs,
                                     svg_text=lambda n: read(self.svgs[n]))

    def test_every_edition_clears(self):
        found = boxpad.check(self.ctx())
        self.assertEqual([f.code for f in found if f.level == "fail"], [], found)
        for name, ent in self.report["sheets"].items():
            for _ids, left, right in boxpad.clearances(ent, read(self.svgs[name])):
                self.assertGreaterEqual(min(left, right), sheet.BOX_PAD_MIN, name)

    def test_height_does_not_move(self):
        self.assertEqual(sheet.DANGER_PAD_Y, 6)
        self.assertEqual(self.report["sheets"]["hero-phone-day"]["h"], 1121)
        self.assertEqual(self.report["sheets"]["hero-day"]["h"], 707)
        box = next(m["box"] for m in self.report["sheets"]["hero-phone-day"]["route"]["marks"] if m["kind"] == "danger")
        bracket = next(m["box"] for m in self.report["sheets"]["hero-phone-day"]["route"]["marks"] if m["id"] == "R6")
        self.assertGreater(box[0], bracket[2], "the box is clear of the loop bracket")
        self.assertLess(box[2], 600)

    def test_the_check_bites(self):
        rep = copy.deepcopy(self.report)
        for t in rep["sheets"]["hero-phone-day"]["text"]:
            if t.get("key") in ("routes:H0", "routes:H1"):
                t["x1"] = float(t["x1"]) + 6
        self.assertIn("BOX-PAD", [f.code for f in boxpad.check(self.ctx(rep)) if f.level == "fail"])


class Clean(unittest.TestCase):
    """r16-1 #2: AUDIT-COVER and STRINGS-TWICE stay clean on the committed page."""

    def test_audit_cover(self):
        import audit_figures
        cfg, stats = load()
        recs = audit_figures.records(cfg, stats)
        self.assertEqual(audit_cover.uncovered_readme(read(README), recs, stats, cfg), [])

    def test_strings_twice(self):
        cfg, stats = load()
        with tempfile.TemporaryDirectory() as tmp:
            rep = os.path.join(tmp, "r.json")
            build_assets.main(sheets=["hero"], out=os.path.join(tmp, "o"), report_path=rep, stats_path=STATS,
                              cfg_path=CFG, quiet=True)
            ctx = check.make_ctx(ROOT, out_dir=os.path.join(tmp, "o"), report_path=rep)
            twice = [f for f in strings.check(ctx) if f.code == "STRINGS-TWICE" and f.level == "fail"]
        self.assertEqual(twice, [])


if __name__ == "__main__":
    unittest.main()
