"""Review round 6 (docs/crit/round6/review-r06-*.md): what each fix promises, held by a test.

M1 waits on the cargo gate and a robots-on test; L1 says what 0.1.3 does with robots.txt, on a probe; a condition
needs a probe or the code that decides it; the hand-off label says what you get; rule 4 cites his own commit; the
phone sheet is sized for the 308 px image GitHub shows; the phone sheet is served below a 1200 px viewport.
"""
from __future__ import annotations

import copy
import json
import os
import sys
import tomllib
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import check  # noqa: E402,F401  (plug-ins import Finding from it)
import render_readme as rr  # noqa: E402
import runcheck  # noqa: E402
from checks import column, notices, route as route_check  # noqa: E402
from data import proof, route as R  # noqa: E402
from sheets import route as sheet  # noqa: E402

STATS = os.path.join(ROOT, "assets", "stats.json")
CFG = os.path.join(ROOT, "chart.toml")
README = os.path.join(ROOT, "README.md")


def load():
    with open(CFG, "rb") as fh:
        cfg = tomllib.load(fh)
    with open(STATS, encoding="utf-8") as fh:
        stats = json.load(fh)
    return cfg, stats


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def tree(files):
    return lambda p: files.get(p)


def entry(cfg, gid):
    return next(e for e in cfg["route"]["rustmapper"]["entry"] if e["id"] == gid)


class Conditions(unittest.TestCase):
    """Review r06-2 #1: a setter in a file is not evidence that anything calls it with a value."""

    SETTER_SRC = "fn apply(&mut self) { host_state.crawl_delay_secs = delay; }"
    PRODUCER_NONE = "let event = StateEvent::UpdateHostStateFact { crawl_delay_secs: None };"

    def spec(self, **kw):
        e = {"id": "L9", "kind": "text", "scope": "release",
             "text": "no pause between them unless the site's `robots.txt` sets a `Crawl-delay`.",
             "release": [{"path": "src/state.rs", "text": "host_state.crawl_delay_secs = delay"}]}
        e.update(kw)
        return {"repo": "x", "entry": [e]}

    def test_setter_alone_does_not_verify_a_condition(self):
        rel = tree({"src/state.rs": self.SETTER_SRC, "src/frontier.rs": self.PRODUCER_NONE})
        r = R.verify_route(self.spec(), None, rel, None, "0.1.3")
        self.assertEqual([e["id"] for e in R.unverified(r)], ["L9"])
        self.assertTrue(any("'unless' states a condition" in m for m in r["entries"][0]["missing"]), r["entries"][0])

    def test_a_setter_marked_producer_still_does_not(self):
        rel = tree({"src/state.rs": self.SETTER_SRC})
        spec = self.spec(release=[{"path": "src/state.rs", "text": "host_state.crawl_delay_secs = delay", "producer": True}])
        self.assertEqual([e["id"] for e in R.unverified(R.verify_route(spec, None, rel, None, "0.1.3"))], ["L9"])

    def test_a_probe_or_a_producer_does(self):
        rel = tree({"src/state.rs": self.SETTER_SRC, "src/frontier.rs": "crawl_delay_secs: parse_crawl_delay_secs(&body)"})
        rc = {"version": "0.1.3", "ok": True, "steps": [{"id": "crawl_delay_obeyed", "ok": True}]}
        r = R.verify_route(self.spec(runs=["crawl_delay_obeyed"]), None, rel, None, "0.1.3")
        self.assertEqual([e["id"] for e in R.drawn(r, rc)], ["L9"])
        spec = self.spec(release=[{"path": "src/frontier.rs", "text": "crawl_delay_secs: parse_crawl_delay_secs(",
                                   "producer": True}])
        self.assertEqual([e["id"] for e in R.drawn(R.verify_route(spec, None, rel, None, "0.1.3"))], ["L9"])

    def test_every_committed_conditional_wording_has_a_probe_or_producer(self):
        cfg, _ = load()
        for e in cfg["route"]["rustmapper"]["entry"]:
            for c in [e] + list(e.get("instead") or []):
                if R.CONDITIONAL.search(str(c.get("text") or "")):
                    self.assertTrue(c.get("runs") or c.get("fails") or R.producers(c), (e["id"], c["text"]))


class LoadSentence(unittest.TestCase):
    """Review r06-2 #1: L1 says what 0.1.3 does with robots.txt."""

    def test_l1_today(self):
        cfg, stats = load()
        text = " ".join(rr.text_entries(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"], stats["edition"],
                                        rr._repo(stats, "Rust-sitemap")))
        # review round 8: the per-host 20 is said by F1 in the image; L1 keeps the total and the pace. Review round 9:
        # L1 with its lever, the robots clause its own item (L4)
        self.assertIn("It sends requests with no pause between them, up to 256 at a time across all hosts. "
                      "`--workers 1` sends one at a time.", text)
        self.assertIn("0.1.3 ignores `Crawl-delay`, and asks for `robots.txt` only over https, so a plain-http site's "
                      "rules are not read.", text)
        self.assertNotIn("unless", text)
        self.assertNotIn("On main", text, "M1 waits on the cargo gate (review r06-1 #1)")

    def test_l1_follows_the_probe_and_the_parser(self):
        cfg, _ = load()
        spec = {"repo": "x", "entry": [entry(cfg, "L4")]}      # review round 9: the robots clause is L4
        base = {"src/state.rs": "HostState { max_inflight: 20, crawl_delay_secs: 0 }",
                "src/cli.rs": '#[arg(long, default_value = "256")]\n    workers: usize,',
                "src/robots.rs": 'pub async fn fetch_robots_txt(h: &H, d: &str) { let u = format!("https://{}/robots.txt", d); }'}
        failed = {"version": "0.1.3", "ok": True, "steps": [{"id": "robots_read", "ok": False}]}
        read = {"version": "0.1.4", "ok": True, "steps": [{"id": "robots_read", "ok": True}]}
        r = R.verify_route(spec, None, tree(base), None, "0.1.3")
        self.assertIn("only over https", R.drawn(r, failed)[0]["text"])
        r = R.verify_route(spec, None, tree(base), None, "0.1.4")
        self.assertTrue(R.drawn(r, read)[0]["text"].endswith("{release} ignores `Crawl-delay`."))
        parsed = dict(base, **{"src/robots.rs": base["src/robots.rs"] + "\npub fn parse_crawl_delay_secs(b: &str) {}"})
        r = R.verify_route(spec, None, tree(parsed), None, "0.1.4")
        self.assertEqual(R.drawn(r, read), [], "the old wording needs a probe that saw the pause")
        self.assertEqual([e["id"] for e in R.unverified(r, read)], ["L4"])

    def test_robots_verdict(self):
        ok, detail = runcheck.robots_verdict([(0.0, "/"), (0.001, "/open.html"), (0.002, "/secret.html")])
        self.assertFalse(ok)
        self.assertIn("/robots.txt never asked for", detail)
        self.assertIn("/secret.html (disallowed) fetched", detail)
        ok, detail = runcheck.robots_verdict([(0.0, "/robots.txt"), (0.1, "/"), (5.1, "/open.html")])
        self.assertTrue(ok, detail)
        self.assertIn("5000 ms apart", detail)

    def test_robots_fixture(self):
        robots = read(os.path.join(runcheck.ROBOTS_SITE, "robots.txt"))
        self.assertIn("Disallow: /secret.html", robots)
        self.assertIn('href="secret.html"', read(os.path.join(runcheck.ROBOTS_SITE, "index.html")))

    def test_committed_probe(self):
        _, stats = load()
        st = {s["id"]: s for s in stats["runcheck"]["rustmapper"]["steps"]}
        self.assertFalse(st["robots_read"]["ok"])
        self.assertFalse(st["robots_read"]["gate"])
        self.assertIn("/robots.txt never asked for", st["robots_read"]["detail"])


class Gates(unittest.TestCase):
    """Review r06-1 #1 / r06-2 #2: a text entry with `gate` prints only while that gate holds."""

    def test_gate_key_reaches_the_record(self):
        cfg, stats = load()
        self.assertEqual(entry(cfg, "M1")["gate"], "cargo")
        m1 = next(e for e in stats["routes"]["rustmapper"]["entries"] if e["id"] == "M1")
        self.assertEqual(m1["gate"], "cargo")
        self.assertIn({"path": "tests/crawl_exits_when_idle.rs", "absent": "--ignore-robots"}, entry(cfg, "M1")["head"])

    def test_any_gated_text_entry_is_skipped_while_its_gate_fails(self):
        spec = {"repo": "x", "entry": [{"id": "T9", "kind": "text", "gate": "cargo", "text": "said on main.",
                                        "head": [{"path": "a"}], "release": [{"path": "b"}]}]}
        r = R.verify_route(spec, tree({"a": ""}), tree({"b": ""}), None, "0.1.3")
        r["gates"] = {"cargo": {"ok": False}}
        self.assertEqual(rr.text_entries(r, None, {"version": "0.1.3"}), [])
        r["gates"] = {"cargo": {"ok": True}}
        self.assertEqual(rr.text_entries(r, None, {"version": "0.1.3"}), ["said on main."])
        r["gates"] = {}
        self.assertEqual(rr.text_entries(r, None, {"version": "0.1.3"}), [], "a gate never computed does not hold")


class HandOff(unittest.TestCase):
    """Review r06-1 #3: "sorted 25 ways by ideal-url-organizer", no path, no ", with a test"."""

    def test_words(self):
        ho = {"to": "ideal-url-organizer", "does": "sorted by"}
        # review round 7: the row marked `handoff` (the methods run.sh --all runs), not the method-file glob
        rows = [{"text": "21 ways", "repo": "ideal-url-organizer", "holds": True, "handoff": True}]
        self.assertEqual(sheet.handoff_words(ho, {"figures": rows}), "sorted 21 ways by ideal-url-organizer")
        glob = [{"text": "25 ways", "repo": "ideal-url-organizer", "holds": True}]
        self.assertEqual(sheet.handoff_words(ho, {"figures": glob}), "sorted by ideal-url-organizer")
        self.assertEqual(sheet.handoff_words(ho, {"figures": [dict(rows[0], holds=False)]}),
                         "sorted by ideal-url-organizer")
        self.assertEqual(sheet.handoff_words(ho, {"figures": [dict(rows[0], repo="Scrapy")]}),
                         "sorted by ideal-url-organizer")
        self.assertEqual(sheet.handoff_words({"to": "x"}, {"figures": rows}), "read by x")
        self.assertIn("21 ways", sheet.PURPOSE["R15"][0])


class RuleFour(unittest.TestCase):
    """Review r06-1 #6: the rule cites his own commit."""

    def finding(self, rec, anchors=None):
        cfg, stats = load()
        nts = copy.deepcopy(cfg["notices"])
        if anchors is not None:
            nts[3]["anchors"] = anchors
        rules = [r for r in stats["rules"] if r["n"] != 4] + [rec]
        ctx = type("C", (), {"stats": dict(stats, rules=rules), "cfg": dict(cfg, notices=nts)})()
        return [f for f in notices.check(ctx) if f.code == "NOTICE-AUTHOR"]

    def test_committed(self):
        cfg, stats = load()
        nt = next(n for n in cfg["notices"] if n["n"] == 4)
        self.assertNotIn("Claude", nt["cite"])
        self.assertFalse(nt.get("names_agent"))
        self.assertEqual(nt["anchors"][0]["author"], "self")
        rec = next(r for r in stats["rules"] if r["n"] == 4)
        self.assertEqual((rec["scope"], rec["found"], rec["sha"], rec["date"]), ("self", True, "2be623e", "2025-11-13"))
        self.assertEqual(proof.fill_cite(nt["cite"], 4, stats["rules"])[0],
                         "ideal-url-organizer, Nov 2025: URLs split with `urllib.parse`.")
        self.assertEqual(self.finding(rec), [])

    def test_scoped_anchor_fails_without_his_commit(self):
        _, stats = load()
        rec = dict(next(r for r in stats["rules"] if r["n"] == 4), found=False, sha=None, date=None)
        self.assertEqual(len(self.finding(rec)), 1)
        rec = {k: v for k, v in next(r for r in stats["rules"] if r["n"] == 4).items() if k != "scope"}
        self.assertEqual(len(self.finding(rec)), 1, "a record computed without the scope does not count")

    def test_unscoped_anchor_still_fails_on_an_agent_first(self):
        _, stats = load()
        rec = {k: v for k, v in next(r for r in stats["rules"] if r["n"] == 4).items() if k != "scope"}
        self.assertEqual(len(self.finding(rec, [{"key": "urlparse", "repo": "ideal-url-organizer",
                                                 "text": "urllib.parse"}])), 1)

    def test_rule_records_carry_the_scope(self):
        commits = [{"sha": "a" * 40, "date": "2025-11-09", "name": "Claude", "email": "noreply@anthropic.com"},
                   {"sha": "b" * 40, "date": "2025-11-13", "name": "Benjamin Russell",
                    "email": "benjamin.sheldon.russell@gmail.com"}]
        cfg, _ = load()
        recs = proof.rule_records([{"n": 4, "anchors": [{"key": "k", "repo": "r", "text": "t", "author": "self"}]}],
                                  {"r": "/x"}, cfg["identity"], adding=lambda *a: commits)
        self.assertEqual((recs[0]["scope"], recs[0]["sha"], recs[0]["first_is_his"]), ("self", "bbbbbbb", False))


class PhoneSize(unittest.TestCase):
    """Review r06-3 #2: the phone sheet for the 308 px image GitHub shows on a 390 px phone."""

    def test_constants(self):
        self.assertEqual(sheet.SIZES["phone"][0], 600)
        self.assertEqual((route_check.PHONE_SCREEN, route_check.MIN_PX), (308, 13.0))
        self.assertEqual((route_check.NARROW_SCREEN, route_check.MIN_PX_NARROW), (278, 11.0))
        self.assertLessEqual(route_check.HEIGHT["phone"] * 308 / 600, 640)

    def test_a_720_sheet_fails_at_308(self):
        ent = {"w": 720, "h": 900, "text": [{"s": "x", "size": 26, "key": "routes:S1", "truth": "measured"}]}
        ctx = type("C", (), {"stats": {}, "report": {"sheets": {"hero-phone-day": ent}}, "svgs": {"hero-phone-day": "x"},
                             "svg_text": lambda self, n: ""})()
        _, stats = load()
        ctx.stats = stats
        codes = [f.code for f in route_check.check(ctx) if f.code == "ROUTE-PHONE-PX"]
        self.assertEqual(len(codes), 2, "11.1 px at 308 (< 13) and 10.0 px at 278 (< 11)")
        ent["w"] = 600
        self.assertEqual([f.code for f in route_check.check(ctx) if f.code == "ROUTE-PHONE-PX"], [])


class Columns(unittest.TestCase):
    """Review r06-3 #1: the sheet each viewport is served, at the column GitHub gives it."""

    SHEETS = {"hero-day": {"w": 1280, "text": [{"size": 19}]}, "hero-phone-day": {"w": 600, "text": [{"size": 26}]}}

    def readme(self, bp):
        return (f'<source media="(max-width: {bp}px) and (prefers-color-scheme: dark)" srcset="https://x/v9/hero-phone-night.svg">'
                f'<source media="(max-width: {bp}px)" srcset="https://x/v9/hero-phone-day.svg">'
                '<source media="(prefers-color-scheme: dark)" srcset="https://x/v9/hero-night.svg">')

    def test_table(self):
        self.assertEqual([column.column_px(v) for v in (390, 767, 768, 1011, 1012, 1279, 1280, 1920)],
                         [308, 685, 398, 641, 578, 845, 846, 846])

    def test_the_old_breakpoint_fails_on_tablets(self):
        bad = column.worst(self.readme(767), self.SHEETS)
        vws = [b[0] for b in bad]
        self.assertIn(768, vws)
        self.assertIn(1024, vws)
        self.assertAlmostEqual(next(b[2] for b in bad if b[0] == 768), 19 * 398 / 1280)

    def test_1199_passes_from_360(self):
        self.assertEqual(column.worst(self.readme(1199), self.SHEETS), [])
        self.assertEqual(column.phone_max(self.readme(1199)), 1199)

    def test_committed_readme_and_chart(self):
        cfg, _ = load()
        self.assertEqual(cfg["chart"]["breakpoint_px"], 1199)
        self.assertEqual(column.phone_max(read(README)), 1199)


class Wording(unittest.TestCase):
    """Review r06-1 #4, #5; r06-2 #3, #5, #6; r06-3 #3."""

    def test_route_words(self):
        cfg, _ = load()
        self.assertEqual(cfg["route"]["rustmapper"]["header"], "Crawls a site and writes one line for every URL it finds.")
        self.assertNotIn("above or below", entry(cfg, "F1")["text"])
        s1 = entry(cfg, "S1")
        self.assertTrue(s1["text"].startswith("starts from your URL; by default also from sitemaps"))   # round 9
        self.assertIn("if asked", s1["instead"][0]["text"])
        anchor = {"path": "src/ct_log_seeder.rs", "text": 'format!("https://{}/", subdomain)'}
        self.assertIn(anchor, s1["head"])
        self.assertIn(anchor, s1["release"])

    def test_readme_words(self):
        text = read(README)
        self.assertNotIn("Circuit breakers wrap the HTTP, Delta Lake and Redis services", text)
        self.assertIn("Each host has its own circuit breaker: after 5 URLs on it fail every retry, it is left alone for "
                      "60 s.", text.replace("\u00a0", " "))
        self.assertNotIn("costs the caller nothing", text)
        self.assertIn("logged only after the client has its last byte", text)
        self.assertNotIn("concurrent sitemap crawler written in Rust", text)
        cfg, _ = load()
        for t in ("5 URLs", "60 s"):
            row = next(f for f in cfg["figures"] if f["text"] == t)
            self.assertIn("DEFAULT_STAGE2_BREAKER_", row["literal"])


if __name__ == "__main__":
    unittest.main()
