"""Review round 7 (docs/crit/round6/review-r07-*.md): what each fix promises, held by a test.

The code blocks fit a 360 px phone; the Languages line comes from the data; the governor is a clause of the fetch
row; rule 1 cites the breakers that run and every rule's code is still there; the writer saves in batches, not on a
period; the hand-off counts the sorts the importer runs; every printed figure has a register row; the Scrapy test
count says what CI selects; the data line names the co-signed commits; his Scrapy is told from the framework; H1
says "exits"; the rules are plain claims; dates and units stay on one line; one spelling system; S1 punctuated.
"""
from __future__ import annotations

import copy
import json
import os
import re
import sys
import tomllib
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import check  # noqa: E402,F401  (plug-ins import Finding from it)
import audit_figures  # noqa: E402
import render_readme as rr  # noqa: E402
from checks import audit_cover, notices_live, readme as readme_check  # noqa: E402
from data import proof, route as R, tree  # noqa: E402
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


def entry(cfg, gid):
    return next(e for e in cfg["route"]["rustmapper"]["entry"] if e["id"] == gid)


def visible(text):
    """README text a reader sees, code blocks out, comments, tags and link targets removed."""
    t = re.sub(r"^```.*?^```", " ", text, flags=re.S | re.M)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\]\([^)]*\)", "]", t)


class Ctx:
    def __init__(self, stats=None, cfg=None, readme="", report=None):
        self.stats, self.cfg, self.readme, self.report = stats or {}, cfg or {}, readme, report


class CodeColumns(unittest.TestCase):
    """r07-1 #1, r07-2 #3: 32 columns fit a 360 px phone; the explanations sit before the Scrapy block."""

    def test_no_fenced_line_over_32(self):
        self.assertEqual(readme_check.CODE_COLUMNS, 32)
        text = read(README)
        for m in re.finditer(r"^```[^\n]*\n(.*?)^```", text, re.S | re.M):
            for ln in m.group(1).splitlines():
                self.assertLessEqual(len(ln), 32, ln)
        self.assertIn("# sitemap.xml, even after a kill\n", text)
        scrapy = re.search(r"```sh\ncd Scrapy/Scraping_project\n(.*?)```", text, re.S)
        self.assertIsNotNone(scrapy)
        self.assertNotIn("#", scrapy.group(1), "the explanations are before the block, not comments in it")
        self.assertEqual(readme_check.code_too_wide("```sh\n" + "x" * 33 + "\n```\n"), [(2, "x" * 33)])

    def test_no_this_repository(self):
        text = read(README)
        self.assertNotRegex(visible(text), re.compile("this repository", re.I))
        found = readme_check.check(type("C", (), {"readme": text.replace("Run these from", "In this repository, run"),
                                                  "stats": {}, "root": ROOT})())
        self.assertIn("THIS-REPO", [f.code for f in found])


class Languages(unittest.TestCase):
    """r07-1 #2: every main_language of his public repositories, and nothing else."""

    def test_from_the_data(self):
        cfg, stats = load()
        line = rr.languages_line(stats, cfg)
        names = [x.strip() for x in re.split(r"[;,]", line)]
        want = {r["main_language"] for r in stats["repos"] if r.get("main_language") and r["name"] != cfg["chart"]["login"]}
        self.assertEqual(set(names), want)
        self.assertEqual(len(names), len(want))
        self.assertTrue(line.startswith("Python, Rust; "), line)
        self.assertIn("JavaScript", names)
        self.assertIn(f"**Languages** <!-- n:languages -->{line}<!-- /n -->.", read(README))

    def test_order(self):
        stats = {"repos": [{"name": "a", "main_language": "Go", "lines": {"Go": 10}},
                           {"name": "b", "main_language": "C", "lines": {"C": 99}},
                           {"name": "c", "main_language": "Go", "lines": {"Go": 5}},
                           {"name": "d", "main_language": "Swift", "lines": {"Swift": 1}},
                           {"name": "me", "main_language": "Ruby"}]}
        cfg = {"chart": {"login": "me"}, "copy": {"languages_lead": ["Swift", "Rust"]}}
        self.assertEqual(rr.languages_line(stats, cfg), "Swift; Go, C", "Rust is no repository's: left out")


class Governor(unittest.TestCase):
    """r07-1 #3: no note line under a stop; the qualifier sits by its verb."""

    def test_folded_into_f1(self):
        cfg, stats = load()
        ids = [e["id"] for e in cfg["route"]["rustmapper"]["entry"]]
        self.assertNotIn("G1", ids)
        self.assertFalse([e for e in cfg["route"]["rustmapper"]["entry"] if e.get("kind") == "note"])
        f1 = entry(cfg, "F1")
        self.assertEqual(f1["scope"], "release")
        self.assertIn("{const:THROTTLE_THRESHOLD_MS}", f1["text"])
        self.assertTrue(any(a.get("producer") for a in f1["release"]))
        drawn = {e["id"]: e for e in R.drawn(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"])}
        # review round 8: the governor wording is first and does not hold for 0.1.3 (its floor of 32 idle permits)
        self.assertTrue(f1["text"].startswith("fetches pages, fewer at once when saves average over"))
        self.assertTrue(drawn["F1"]["text"].startswith("fetches up to 20 pages at a time from each host; "))
        self.assertNotIn("G1", sheet.PURPOSE)


class RuleOne(unittest.TestCase):
    """r07-1 #4, r07-3 #3: rule 1 cites the per-host breakers he wrote; every rule's code is still at HEAD."""

    def test_anchor_and_cite(self):
        cfg, stats = load()
        n1 = next(n for n in cfg["notices"] if n["n"] == 1)
        self.assertEqual(n1["anchors"], [{"key": "breaker", "repo": "Scrapy", "text": "_host_breakers", "author": "self"}])
        rec = next(r for r in stats["rules"] if r["n"] == 1)
        self.assertEqual((rec["sha"], rec["date"], rec["scope"], rec["at_head"]), ("099dd6c", "2026-10-08", "self", True))
        block = rr.notices_block(cfg, stats).replace(NB, " ")
        self.assertIn("*Scrapy, Oct 2026: a circuit breaker for each host in stage 2.*", block)

    def test_notice_live(self):
        cfg, stats = load()
        self.assertEqual(notices_live.check(Ctx(stats, cfg)), [])
        gone = copy.deepcopy(stats)
        next(r for r in gone["rules"] if r["n"] == 1)["at_head"] = False
        self.assertEqual([f.code for f in notices_live.check(Ctx(gone, cfg))], ["NOTICE-LIVE"])
        unchecked = copy.deepcopy(stats)
        next(r for r in unchecked["rules"] if r["n"] == 2).pop("at_head")
        self.assertEqual([f.code for f in notices_live.check(Ctx(unchecked, cfg))], ["NOTICE-LIVE"])

    def test_plain_claims(self):
        cfg, _ = load()
        bodies = [n["body"] for n in sorted(cfg["notices"], key=lambda n: n["n"])[:3]]
        frame = re.compile(r"^(The|A) \w+ .* is (the one|one|a \w+) ")
        self.assertLessEqual(sum(bool(frame.search(b)) for b in bodies), 1)
        for b in bodies:
            self.assertNotRegex(b, r"you cannot .* you cannot")
        # review r11-1 #2: the rule carries the breaker's numbers; the Scrapy bullet no longer says it
        self.assertEqual(bodies[0], "When 5 URLs in a row on one host fail every retry, that host is left alone for 60 s; "
                                    "the rest of the crawl goes on.")      # review round 13: in a row
        self.assertTrue(bodies[2].startswith("Metrics were exported {days:prometheus} days"), bodies[2])


WRITER = """
const BATCH_TIMEOUT_MS: u64 = 50;
fn writer_loop() {{ {sleep} for r in batch {{ wal.append(&record); }} wal.fsync(); state.apply_event_batch(&batch); }}
fn drain_batch() {{ let deadline = now + Duration::from_millis(BATCH_TIMEOUT_MS);
  match event_rx.recv_deadline(deadline) {{ Ok(e) => {{}} }} loop {{ match event_rx.try_recv() {{ _ => break }} }} }}
"""


class Writer(unittest.TestCase):
    """r07-2 #1: 50 ms is drain_batch's wait for the first event, not a save period."""

    def resolve(self, sleep=""):
        cfg, _ = load()
        w1 = copy.deepcopy(entry(cfg, "W1"))
        for c in [w1] + w1.get("instead", []):
            c.pop("head", None)
        w1["scope"] = "release"
        files = {"src/writer_thread.rs": WRITER.format(sleep=sleep), "src/wal.rs": "fn fsync() { f.sync_all(); }",
                 "src/state.rs": "use redb::Database;"}
        route = R.verify_route({"repo": "x", "entry": [w1]}, None, files.get, None, "0.1.3")
        return R.resolve(route)[0]

    def test_in_batches(self):
        got = self.resolve()
        self.assertTrue(got["verified"], got)
        self.assertEqual(got["text"], "logged to disk, then saved to redb, in batches")

    def test_no_period_wording(self):
        # review round 13: the "every 50 ms" wording is gone (no tree ever slept between flushes); a timed flush
        # changes nothing the row says
        got = self.resolve("thread::sleep(Duration::from_millis(BATCH_TIMEOUT_MS));")
        self.assertEqual(got["text"], "logged to disk, then saved to redb, in batches")
        cfg, _ = load()
        self.assertFalse(any("BATCH_TIMEOUT_MS" in c["text"] for c in [entry(cfg, "W1")] + entry(cfg, "W1")["instead"]))

    def test_committed(self):
        _, stats = load()
        w1 = next(e for e in R.drawn(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"]) if e["id"] == "W1")
        self.assertEqual(w1["text"], "saved as it goes; export works after a kill")      # review round 13
        self.assertNotIn("every 50 ms", sheet.PURPOSE["W1"][0])


MAIN = """
class P:
    def __init__(self):
        self.methods = {
            'method_01_by_domain': (A, 'x'),
            'method_02_by_depth': (B, 'y'),
        }
"""


class HandOffCount(unittest.TestCase):
    """r07-2 #2: the count is the methods `run.sh --all` runs, read with ast."""

    ROW = {"text": "2 ways", "handoff": True, "repo": "o", "path": "src/main.py", "keys": "self.methods", "count": 2,
           "also": [{"path": "scripts/imp.py", "literal": '[str(run_sh), "--all"]'}]}

    def records(self, files, row=None):
        return proof.figure_records([row or self.ROW], {"o": "gd"}, read=lambda gd, p: files.get(p), ls=lambda gd: [])

    def test_keys(self):
        self.assertEqual(proof.dict_keys(MAIN, "self.methods"), ["method_01_by_domain", "method_02_by_depth"])
        self.assertIsNone(proof.dict_keys("x = 1", "self.methods"))
        files = {"src/main.py": MAIN, "scripts/imp.py": 'subprocess.run([str(run_sh), "--all"])'}
        rec = self.records(files)[0]
        self.assertTrue(rec["holds"] and rec["handoff"] and rec["measured"] == 2, rec)
        ho = {"to": "o", "does": "sorted by"}
        self.assertEqual(sheet.handoff_words(ho, {"figures": [rec]}), "sorted 2 ways by o")

    def test_without_the_all_call(self):
        files = {"src/main.py": MAIN, "scripts/imp.py": "subprocess.run([str(run_sh)])"}
        rec = self.records(files)[0]
        self.assertFalse(rec["holds"])
        self.assertEqual(sheet.handoff_words({"to": "o", "does": "sorted by"}, {"figures": [rec]}), "sorted by o")
        wrong = self.records({"src/main.py": MAIN, "scripts/imp.py": '[str(run_sh), "--all"]'}, dict(self.ROW, count=3))[0]
        self.assertFalse(wrong["holds"])

    def test_committed(self):
        cfg, stats = load()
        row = next(f for f in stats["figures"] if f.get("handoff"))
        self.assertEqual((row["text"], row["measured"], row["holds"]), ("21 ways", 21, True))
        # review r11-3 #4: the Also line prints the image's count, not the 25 files
        self.assertIn("21 ways to sort a pile of URLs", read(README))


class Register(unittest.TestCase):
    """r07-2 #4: every digit the page prints has a row in AUDIT.md §7."""

    def test_rows_from_the_route(self):
        cfg, _ = load()
        recs = audit_figures.records(cfg)
        wheres = [r["where"] for r in recs]
        for w in ("image F1", "image H1", "README L1", "README X1", "image R15", "image R2"):
            self.assertIn(w, wheres)
        x1 = next(r for r in recs if r["where"] == "README X1")
        self.assertIn("sitemaps.org", x1["definition"])
        l1 = next(r for r in recs if r["where"] == "README L1")
        self.assertIn("robots_read", l1["definition"])
        self.assertIn("MIT license", [r["printed"] for r in recs])

    def test_cover(self):
        cfg, stats = load()
        recs = audit_figures.records(cfg)
        self.assertEqual(audit_cover.uncovered_readme(read(README), recs, stats, cfg), [])
        extra = read(README).replace("Found a mistake?", "Found 7 mistakes?")
        self.assertEqual(len(audit_cover.uncovered_readme(extra, recs, stats, cfg)), 1)
        report = {"sheets": {"hero-day": {"text": [{"s": "fetches 500", "key": "routes:F1"},
                                                    {"s": "12 islands", "key": "routes:Z9"}]}}}
        self.assertEqual(len(audit_cover.uncovered_hero(report, recs)), 1)


WORKFLOW = """name: CI/CD Pipeline
jobs:
  test:
    steps:
    - name: Run default test suite
      working-directory: proj
      run: |
        # comment
        python -m pytest tests/ \\
          -m "not slow and not kafka" \\
          -o addopts=
    - name: other
      run: pip install pytest
"""
TESTS = """
import pytest
pytestmark = pytest.mark.unit

def test_a(): pass

@pytest.mark.slow
def test_b(): pass

class TestC:
    @pytest.mark.kafka
    def test_c(self): pass

    @pytest.mark.skipif(True, reason="x")
    def test_d(self): pass
"""


class CiSelection(unittest.TestCase):
    """r07-2 #5: "N tests" beside "CI passed" says how many the passing workflow does not select."""

    def test_parse(self):
        self.assertEqual(tree.workflow_name(WORKFLOW), "CI/CD Pipeline")
        self.assertEqual(tree.pytest_commands(WORKFLOW),
                         [{"cwd": "proj", "paths": ["tests"], "not_markers": ["slow", "kafka"]}])
        self.assertIsNone(tree.pytest_commands(WORKFLOW.replace('"not slow and not kafka"', '"smoke or slow"')))

    def test_count(self):
        files = {"proj/tests/test_x.py": TESTS, "proj/tools/test_y.py": "def test_z(): pass\n"}
        rec = tree.ci_selection(list(files), files.get, "r", None, WORKFLOW, 5)
        # test_b (slow) and test_c (kafka) deselected; test_d's skipif is decided at run time; test_z is outside tests/
        self.assertEqual((rec["deselected"], rec["outside"], rec["not_selected"]), (2, 1, 3))
        rust = {"src/lib.rs": "#[test]\nfn a() {}\n#[test]\n#[ignore]\nfn b() {}\n"}
        self.assertEqual(tree.ci_selection(list(rust), rust.get, "r", None, "run: cargo test --all\n", 2)["not_selected"], 1)
        self.assertEqual(tree.ci_selection(list(rust), rust.get, "r", None, "run: echo\n", 2)["not_selected"], 2)

    def test_facts(self):
        stats = {"repos": [{"name": "x", "test_functions": 1920, "ci": {"conclusion": "success", "date": "2026-10-08"},
                            "ci_selection": {"not_selected": 41, "of": 1920}}]}
        self.assertIn("1,920 test functions (CI selects all but 41) · CI passed", rr.facts_block(stats, "x"))
        stats["repos"][0]["ci_selection"] = {"not_selected": 0, "of": 1920}
        self.assertNotIn("selects", rr.facts_block(stats, "x"))
        stats["repos"][0]["ci_selection"] = {"not_selected": 41, "of": 1900}
        self.assertNotIn("selects", rr.facts_block(stats, "x"), "measured against another count: not printed")
        _, live = load()
        sc = rr._repo(live, "Scrapy")
        self.assertEqual(sc["ci_selection"]["not_selected"], sc["ci_selection"]["outside"] + sc["ci_selection"]["deselected"])


class Cosigned(unittest.TestCase):
    """r07-2 #6, r07-3 #7: the co-signed commits beside the authored ones; "shows"; the Scrapy repository's."""

    def test_clause(self):
        # review round 14: per repository, on its facts line; co-signed only beside the authored count, and only > 0
        a = {"name": "A", "all_hands": 10, "commits": 6, "others": [{"name": "Claude", "commits": 4, "bot": True}],
             "coauthored": {"agent": 1}}
        self.assertEqual(rr.agent_clause(a), "coding agents (Claude) authored 4 of its 10 commits and co-signed 1 of "
                                             "his own 6")
        self.assertNotIn("co-signed", rr.agent_clause(dict(a, coauthored={"agent": 0})))
        a.pop("coauthored")
        self.assertNotIn("co-signed", rr.agent_clause(a))

    def test_committed(self):
        text = read(README).replace(NB, " ")
        self.assertIn("The [drawing](DESIGN.md) shows rustmapper 0.1.3", text)
        self.assertIn("coding agents (jules, Claude) authored 71 of its 499 commits and co-signed 30 of his own 420*",
                      text)


class Framework(unittest.TestCase):
    """r07-3 #1: his Scrapy is told from the Scrapy framework at first mention."""

    def test_first_mention(self):
        text = read(README)
        body = text[text.index("<!-- picture:hero:end -->"):]
        link_line = re.search(r'<a href="https://github.com/BenjaminSRussell/Rust-sitemap"><b>rustmapper</b></a>.*', body).group(0)
        self.assertLess(link_line.index("PyPI"), link_line.index("<b>Scrapy</b>"), "PyPI beside the project it belongs to")
        plain = re.sub(r"\[[^\]]*\]\([^)]*\)", "", re.sub(r"<a [^>]*>.*?</a>", "", body))
        plain = re.sub(r"<!--.*?-->", "", plain, flags=re.S)
        first = re.search(r"\bScrapy\b", plain)
        self.assertTrue(plain[:first.start()].rstrip("* ").endswith("His"), plain[first.start() - 30:first.end()])
        self.assertIn("is his crawl system on top of the Scrapy framework, in four stages", text)
        self.assertNotIn("A scout spider goes first", text)
        self.assertNotIn("pipeline that needs Docker", text)


class Wording(unittest.TestCase):
    """r07-3 #2, #5, #6."""

    def test_h1_exits(self):
        cfg, _ = load()
        h1 = entry(cfg, "H1")
        # review round 9: the clearing mark with its number
        self.assertEqual(h1["text"], "{release} never exits by itself; done when `Received work item` lines stop for {quiet} s")
        self.assertEqual(h1["instead"][0]["text"], "{release} never exits by itself, even after the last page")

    def test_one_spelling(self):
        text = visible(read(README))
        for word in ("summarise", "summarised", "organise", "optimise", "recognise", "normalise", "summarisation"):
            self.assertNotRegex(text, re.compile(rf"\b{word}", re.I))
        self.assertIn("summarized", read(README))

    def test_s1(self):
        cfg, _ = load()
        s1 = entry(cfg, "S1")
        # review round 9: with a verb, as every other row
        # review round 11 (r11-2 #1): the command it names first, then the old words while the probe is missing
        self.assertEqual(s1["text"], "`{script} crawl` starts from your URL; by default also from sitemaps, "
                                     "certificate logs and Common Crawl")
        self.assertTrue(s1["instead"][0]["text"].startswith("`{script} crawl` starts from your URL; if asked, also from "))
        self.assertEqual(s1["instead"][1]["text"], "starts from your URL; by default also from sitemaps, certificate "
                                                   "logs and Common Crawl")


class KeepTogether(unittest.TestCase):
    """r07-3 #4: a phone never ends a line on "CI passed 8" or "16k lines of"."""

    def test_visible_text(self):
        text = visible(read(README))
        months = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
        self.assertFalse(re.findall(rf"\d (?:{months})\b|\b(?:{months}) \d{{4}}", text), "a date split by a plain space")
        self.assertFalse(re.findall(r"\d (?:ms|s|min|characters)\b", text), "a number split from its unit")
        self.assertFalse(re.findall(r"\d+k lines of \w+", text))
        self.assertIn(f"16k{NB}lines{NB}of{NB}Rust", text)
        self.assertIn(f"CI passed 7{NB}Oct{NB}2026", text)

    def test_helpers(self):
        self.assertEqual(rr.fmt_date("2026-10-07"), f"7{NB}Oct{NB}2026")
        self.assertEqual(rr.keep_together("in 3 min and `60 s` code"), f"in 3{NB}min and `60 s` code")


if __name__ == "__main__":
    unittest.main()
