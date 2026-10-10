"""Review round 15 (docs/crit/round6/review-r15-*.md): what each fix promises, held by a test.

S2 ("paced by that host's robots.txt") is drawn only from a release with a Crawl-delay parser, never beside "It
ignores `Crawl-delay`"; while it waits for that release the gate warns (ROUTE-WAITING) and the true editions publish,
and the workflow publishes the sheets before it commits the README. The robots.txt stall is drawn in the loop (H0)
and listed (L6), the robots.txt that comes late is in L4, and both rest on https probes that are `skipped`, never
passed, when port 443 cannot be had. The name rustmapper sends is listed (L7). The Scrapy block lists what each stage
does to a site under "Before you run it:". The <img> is the phone edition. The install note names the platform the
source build was run on, and the data line names both schemes once the https probes ran.
"""
from __future__ import annotations

import copy
import json
import os
import re
import socket
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
from checks import column  # noqa: E402
from checks import readme as readme_check  # noqa: E402
from checks import route as route_check  # noqa: E402
from data import route as R  # noqa: E402
from sheets import route as sheet  # noqa: E402

STATS = os.path.join(ROOT, "assets", "stats.json")
CFG = os.path.join(ROOT, "chart.toml")
README = os.path.join(ROOT, "README.md")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "profile.yml")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def load():
    with open(CFG, "rb") as fh:
        cfg = tomllib.load(fh)
    return cfg, json.loads(read(STATS))


def entry(cfg, gid):
    return copy.deepcopy(next(e for e in cfg["route"]["rustmapper"]["entry"] if e["id"] == gid))


def tree(files):
    return lambda p: files.get(p)


def ctx_for(stats):
    return types.SimpleNamespace(stats=stats, report={}, svgs={}, svg_text=lambda _n: "")


def codes(findings):
    return [f.code for f in findings]


# ---------------------------------------------------------------- fixtures: the trees S2 and L4 read
ROBOTS_013 = ('pub async fn fetch_robots_txt(h: &H, d: &str) -> Option<String> {\n'
              '    let u = format!("https://{}/robots.txt", d);\n}\n')
ROBOTS_PARSER = ROBOTS_013 + "pub fn parse_crawl_delay_secs(body: &str) -> Option<u64> { None }\n"
FRONTIER = ('pub struct ReadyHost { host: String }\n'
            'pub async fn get_next_url(&mut self) {\n'
            '    "missing robots.txt, fetching in background (allowing crawl)";\n'
            "    // Proceed with crawling - don't block on robots.txt\n}\n")


def release(robots):
    return {"src/frontier.rs": FRONTIER, "src/robots.rs": robots}


HEAD_P1 = {"src/frontier.rs": FRONTIER, "src/robots.rs": ROBOTS_PARSER, "tests/robots_4xx_allows_crawl.rs": "#[test]"}


class S2Release(unittest.TestCase):
    """r15-1 #1: S2 is drawn only from a release whose robots.rs parses Crawl-delay, and never with L4's "ignores"."""

    RC_013 = {"version": "0.1.3", "ok": True, "steps": [{"id": "robots_read", "ok": False},
                                                         {"id": "robots_late", "ok": True}]}

    def route(self, rel):
        cfg, _ = load()
        spec = {"repo": "x", "entry": [entry(cfg, "S2"), entry(cfg, "L4")]}
        return R.verify_route(spec, tree(HEAD_P1), tree(rel), "abc", "0.1.3")

    def test_anchor_is_in_the_chart(self):
        cfg, _ = load()
        s2 = entry(cfg, "S2")
        self.assertIn({"path": "src/robots.rs", "text": "fn parse_crawl_delay"}, s2["release"])
        self.assertEqual(s2.get("waits"), "release")
        # the mirror of the cautions' own anchor
        self.assertIn({"path": "src/robots.rs", "absent": "fn parse_crawl_delay"}, entry(cfg, "L4")["release"])
        self.assertIn({"path": "src/robots.rs", "absent": "fn parse_crawl_delay"}, entry(cfg, "L1")["release"])

    def test_013_with_p1_at_head_leaves_s2_out(self):
        r = self.route(release(ROBOTS_013))
        got = {e["id"]: e for e in R.resolve(r, self.RC_013)}
        self.assertFalse(got["S2"]["verified"])
        self.assertIn("release src/robots.rs: no 'fn parse_crawl_delay'", " ".join(got["S2"]["missing"]))
        self.assertTrue(got["S2"]["verified_head"], "P1 at HEAD alone")
        self.assertIn("ignores `Crawl-delay`", got["L4"]["text"])

    def test_a_release_with_the_parser_draws_it(self):
        r = self.route(release(ROBOTS_PARSER))
        got = {e["id"]: e for e in R.resolve(r, self.RC_013)}
        self.assertTrue(got["S2"]["verified"])

    def test_never_both(self):
        for rel in (release(ROBOTS_013), release(ROBOTS_PARSER)):
            for rc in (self.RC_013, {"version": "0.1.3", "ok": True, "steps": [
                    {"id": "robots_read", "ok": True}, {"id": "robots_late", "ok": False},
                    {"id": "crawl_delay_obeyed", "ok": True}]}):
                d = {e["id"]: e for e in R.drawn(self.route(rel), rc)}
                self.assertFalse("S2" in d and "ignores `Crawl-delay`" in str((d.get("L4") or {}).get("text")),
                                 (sorted(d), rel["src/robots.rs"][-40:]))

    def test_s2_drawn_has_its_purpose(self):
        """Built from stats where S2 holds on both sides: its group is drawn, with its PURPOSE row."""
        _, stats = load()
        s = copy.deepcopy(stats)
        for e in s["routes"]["rustmapper"]["entries"]:
            if e["id"] == "S2":
                e.update(verified_head=True, verified_release=True, missing=[])
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "s.json")
            Path(p).write_text(json.dumps(s))
            rep = os.path.join(tmp, "r.json")
            n = build_assets.main(sheets=["hero"], editions=["day"], out=os.path.join(tmp, "o"), report_path=rep,
                                  stats_path=p, cfg_path=CFG, quiet=True)
            self.assertEqual(n, 0)
            drawn = json.loads(read(rep))["sheets"]["hero-day"]["route"]["drawn"]
        self.assertIn("S2", drawn)
        self.assertIn("S2", sheet.PURPOSE)


class Waiting(unittest.TestCase):
    """r15-1 #2: while S2 waits for a release the gate warns, so the true editions publish; anything else fails."""

    def test_today_warns_once(self):
        _, stats = load()
        got = route_check.check(ctx_for(stats))
        self.assertEqual(codes(got).count("ROUTE-WAITING"), 1)
        self.assertNotIn("ROUTE-UNVERIFIED", codes(got))
        self.assertFalse([f for f in got if f.level == "fail"], [(f.code, f.msg) for f in got
                                                                    if f.level == "fail"])
        w = next(f for f in got if f.code == "ROUTE-WAITING")
        self.assertEqual(w.level, "warn")
        self.assertIn("S2", w.msg)
        self.assertIn("fn parse_crawl_delay", w.msg)

    def test_release_holds_head_does_not_fails(self):
        _, stats = load()
        s = copy.deepcopy(stats)
        s2 = next(e for e in s["routes"]["rustmapper"]["entries"] if e["id"] == "S2")
        s2.update(verified_release=True, verified_head=False, missing=["head src/frontier.rs: no 'struct ReadyHost'"])
        self.assertIn("ROUTE-UNVERIFIED", codes(route_check.check(ctx_for(s))))
        self.assertNotIn("ROUTE-WAITING", codes(route_check.check(ctx_for(s))))

    def test_without_waits_it_fails(self):
        _, stats = load()
        s = copy.deepcopy(stats)
        s2 = next(e for e in s["routes"]["rustmapper"]["entries"] if e["id"] == "S2")
        s2.pop("waits")
        self.assertIn("ROUTE-UNVERIFIED", codes(route_check.check(ctx_for(s))))
        f1 = next(e for e in s["routes"]["rustmapper"]["entries"] if e["id"] == "F1")
        f1.update(verified_release=False, missing=["release x"])
        for alt in f1.get("instead") or []:
            alt.update(verified_release=False, missing=["release x"])
        self.assertIn("F1", " ".join(f.msg for f in route_check.check(ctx_for(s)) if f.code == "ROUTE-UNVERIFIED"))

    def test_waits_takes_release_only(self):
        cfg, _ = load()
        spec = {"repo": "x", "entry": [dict(entry(cfg, "S2"), waits="head")]}
        with self.assertRaises(ValueError):
            R.verify_route(spec, tree(HEAD_P1), tree(release(ROBOTS_013)), "abc", "0.1.3")

    def test_publish_before_commit(self):
        text = read(WORKFLOW)
        pub = text.index("- name: Publish sheets to the orphan chart branch")
        dry = text.index("- name: Publish, dry run")
        social = text.index("- name: Social preview PNGs")
        commit = text.index("- name: Commit stats, log, lock and README to main")
        self.assertLess(social, pub)
        self.assertLess(pub, commit)
        self.assertLess(dry, commit)
        # the gate still allows exit 2 (warnings), which ROUTE-WAITING is
        self.assertIn('if [ "$rc" -ne 0 ] && [ "$rc" -ne 2 ]; then exit "$rc"; fi', text)


class ScrapyList(unittest.TestCase):
    """r15-1 #3: Scrapy's effect on a site has rustmapper's form: a lead and a list."""

    def test_committed(self):
        text = read(README)
        block = text.split("**[Scrapy](", 1)[1].split("```sh", 1)[0]
        self.assertIn("It loads no seeds: the last command gives the spider your site.\n\nBefore you run it:\n\n", block)
        items = [ln[2:] for ln in block.split("Before you run it:", 1)[1].strip().splitlines() if ln.startswith("- ")]
        self.assertEqual(len(items), 2)
        self.assertIn("`Crawl-delay`", items[0])
        self.assertIn("`UConn-Discovery-Crawler/1.0`", items[0])
        self.assertIn("`Python/3.11 aiohttp/3.13.1`", items[1])
        self.assertIn("disallowed ones too", items[1])
        _, stats = load()
        got = {r["text"]: r for r in stats["figures"]}
        self.assertTrue(got["The spider obeys `robots.txt` and its `Crawl-delay`"]["holds"])
        self.assertIn("- The spider obeys `robots.txt` and its `Crawl-delay`, and names", block)


class Stall(unittest.TestCase):
    """r15-2 #1, #2, #4: the stall is listed (L6) and drawn in the loop (H0), on the https probes."""

    STALL_SRC = {"src/frontier.rs": ('pub async fn get_next_url(&mut self) {\n'
                                     '                                eprintln!(\n'
                                     '                                    "Shard {}: URL {} blocked by robots.txt",\n'
                                     '                                    self.shard_id, queued.url\n'
                                     '                                );\n'
                                     '                                continue;\n}\n'
                                     'async fn add_url_to_local_queue_unchecked(&mut self) {\n'
                                     '        self.push_ready_host(ReadyHost {\n'
                                     '            host: host.clone(),\n }); }\n'),
                 "src/robots.rs": ROBOTS_013}

    def route(self, files=None):
        cfg, _ = load()
        spec = {"repo": "x", "entry": [entry(cfg, "H0"), entry(cfg, "L6")]}
        return R.verify_route(spec, None, tree(files or self.STALL_SRC), None, "0.1.3")

    def rc(self, stall=True, resume=True, skipped=False):
        st = [{"id": "robots_stall", "ok": stall}, {"id": "robots_resume", "ok": resume}]
        if skipped:
            st = [dict(s, ok=False, skipped=True) for s in st]
        return {"version": "0.1.3", "ok": True, "steps": st}

    def test_committed(self):
        cfg, stats = load()
        d = {e["id"]: e for e in R.drawn(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"])}
        self.assertEqual(d["H0"]["text"], "on https, pages behind a disallowed link wait")
        self.assertEqual(d["H0"]["runs"], ["robots_stall", "robots_resume"])
        self.assertTrue(d["L6"]["text"].startswith("On https, pages queued behind a link that `robots.txt` disallows wait"))
        self.assertLessEqual(len(d["L6"]["text"].split()), rr.LIST_MAX_WORDS)
        order = [e["id"] for e in R.drawn(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"])
                 if e["kind"] in ("stop", "trap", "step")]
        self.assertEqual(order, ["S1", "F1", "H0", "H1", "C1"], "H0 under F1, inside the loop")
        self.assertTrue(d["H0"]["loop"])
        items = [ln for ln in read(README).split("Before you run 0.1.3:", 1)[1].split("<details>", 1)[0].splitlines()
                 if ln.startswith("- ")]
        self.assertTrue(items[3].startswith("- On https, pages queued behind"), items)       # right after L4
        self.assertIn("H0", sheet.PURPOSE)

    def test_probes_decide(self):
        got = {e["id"]: e for e in R.resolve(self.route(), self.rc())}
        self.assertTrue(got["H0"]["verified"] and not got["H0"].get("retired"))
        self.assertEqual(got["H0"]["wording"], 0)
        # a release that re-pushes the host: the stall probe fails, both retire
        got = {e["id"]: e for e in R.resolve(self.route(), self.rc(stall=False))}
        self.assertTrue(got["H0"]["retired"] and got["L6"]["retired"])
        # it stalls for good (a new link no longer resumes it): the words "wait for a new link" are false
        got = {e["id"]: e for e in R.resolve(self.route(), self.rc(resume=False))}
        self.assertFalse(got["L6"]["verified"])

    def test_skipped_is_not_a_pass(self):
        got = {e["id"]: e for e in R.resolve(self.route(), self.rc(skipped=True))}
        self.assertEqual(got["H0"]["wording"], 1, "the code-only wording")
        self.assertEqual(got["L6"]["wording"], 1)
        self.assertFalse(got["L6"].get("retired"), "a skipped probe never retires it")
        # and the run_missing reason says so
        self.assertIn("skipped", " ".join(R.run_missing({"runs": ["robots_stall"]},
                                                        {"robots_stall": {"ok": False, "skipped": True}})))
        self.assertEqual(R.run_missing({"skipped": ["robots_stall"]}, {"robots_stall": {"ok": True}}),
                         ["run check: robots_stall ran (passed), not skipped"])

    def test_code_anchor_bites(self):
        pushed = dict(self.STALL_SRC, **{"src/frontier.rs": self.STALL_SRC["src/frontier.rs"].replace(
            "                                continue;", "                                self.push_ready_host(r);\n"
            "                                continue;")})
        got = {e["id"]: e for e in R.resolve(self.route(pushed), self.rc())}
        self.assertFalse(got["H0"]["verified"] and not got["H0"].get("retired") and got["H0"]["wording"] == 0)

    def test_phone_height_holds_at_851(self):
        with tempfile.TemporaryDirectory() as tmp:
            rep = os.path.join(tmp, "r.json")
            n = build_assets.main(sheets=["hero"], out=os.path.join(tmp, "o"), report_path=rep, stats_path=STATS,
                                  cfg_path=CFG, quiet=True)
            self.assertEqual(n, 0)
            sheets = json.loads(read(rep))["sheets"]
        for name, ent in sheets.items():
            ids = [s["id"] for s in ent["route"]["steps"]]
            self.assertNotIn("W1", ids, name)
            self.assertEqual(next(s for s in ent["route"]["steps"] if s["id"] == "H0")["lines"], 1, name)
            self.assertEqual(sorted(m["id"] for m in ent["route"]["marks"] if m["kind"] == "danger"), ["H0", "H1"])
        ph = sheets["hero-phone-day"]
        self.assertLessEqual(column.drawn_h(ph, 851), column.TALL_PX)
        self.assertEqual(column.tallest(read(README), sheets), [])


class Probes(unittest.TestCase):
    """r15-2 #4: the https probes' verdicts; a probe that cannot run is skipped, never passed."""

    def test_stall_verdict(self):
        p = [(0, "/robots.txt"), (0, "/")] + [(1, f"/p{i}.html") for i in range(1, 6)]
        self.assertEqual(runcheck.stall_verdict(p)[:2], (True, False))
        self.assertEqual(runcheck.stall_verdict(p + [(2, f"/p{i}.html") for i in range(6, 11)])[:2], (False, False))
        self.assertEqual(runcheck.stall_verdict([])[:2], (False, True))
        self.assertEqual(runcheck.stall_verdict(p + [(1, "/secret.html")])[:2], (False, True), "rules not in time")
        self.assertEqual(runcheck.stall_verdict([(0, "/")])[:2], (False, True), "no robots.txt asked")

    def test_resume_verdict(self):
        base = [(0, "/robots.txt"), (0, "/"), (1.0, "/p1.html")] + [(1.0, f"/p{i}.html") for i in range(2, 6)]
        after = [(4.1, "/new.html")] + [(4.1, f"/p{i}.html") for i in range(6, 11)]
        self.assertEqual(runcheck.resume_verdict(base + after)[:2], (True, False))
        early = base + [(1.2, "/p6.html")] + after[1:] + [(4.1, "/new.html")]
        self.assertEqual(runcheck.resume_verdict(early)[:2], (False, False))
        self.assertEqual(runcheck.resume_verdict([])[:2], (False, True))

    def test_late_verdict(self):
        self.assertEqual(runcheck.late_verdict([(0, "/"), (0.1, "/secret1.html"), (0.6, "/robots.txt")])[:2],
                         (True, False))
        self.assertEqual(runcheck.late_verdict([(0, "/"), (0.6, "/robots.txt"), (0.7, "/p1.html")])[:2],
                         (False, False))
        self.assertEqual(runcheck.late_verdict([])[:2], (False, True))

    def test_ua_verdict(self):
        ok, detail, ua = runcheck.ua_verdict([("RustSitemapCrawler/1.0", None)] * 3)
        self.assertTrue(ok)
        self.assertEqual(ua, "RustSitemapCrawler/1.0")
        self.assertFalse(runcheck.ua_verdict([("bot/1.0 (+https://x.org/bot)", None)])[0])
        self.assertFalse(runcheck.ua_verdict([("bot/1.0", "me@x.org")])[0])
        self.assertFalse(runcheck.ua_verdict([])[0])

    def test_unbound_port_is_skipped(self):
        busy = socket.socket()
        busy.bind(("127.0.0.1", 0))
        busy.listen(1)
        port = busy.getsockname()[1]
        try:
            with tempfile.TemporaryDirectory() as tmp:
                cert, key, why = runcheck.make_cert(Path(tmp))
                if cert is None:
                    self.skipTest(why)
                httpd, paths, why = runcheck.serve_https(runcheck.STALL_SITE, cert, key, port=port)
                self.assertIsNone(httpd)
                self.assertIn(f"port {port} could not be bound", why)
                steps = []
                runcheck._skip(steps, "robots_stall", "x", why)
                self.assertEqual((steps[0]["ok"], steps[0]["skipped"], steps[0]["gate"]), (False, True, False))
        finally:
            busy.close()

    def test_committed_run(self):
        _, stats = load()
        steps = {s["id"]: s for s in stats["runcheck"]["rustmapper"]["steps"]}
        for sid in ("robots_stall", "robots_resume", "robots_late", "ua_seen"):
            self.assertTrue(steps[sid]["ok"], steps[sid])
            self.assertFalse(steps[sid].get("skipped"), sid)
        self.assertIn("10 of 10 disallowed pages fetched", steps["robots_late"]["detail"])
        self.assertEqual(steps["ua_seen"]["ua"], "RustSitemapCrawler/1.0")
        self.assertNotIn("ROUTE-PROBE-SKIPPED", codes(route_check.check(ctx_for(stats))))
        s = copy.deepcopy(stats)
        for st in s["runcheck"]["rustmapper"]["steps"]:
            if st["id"] == "robots_late":
                st.update(ok=False, skipped=True)
        self.assertIn("ROUTE-PROBE-SKIPPED", codes(route_check.check(ctx_for(s))))


class LateRobots(unittest.TestCase):
    """r15-2 #3: L4 says it fetches before robots.txt is back, on robots_late; skipped, the old words."""

    def route(self):
        cfg, _ = load()
        return R.verify_route({"repo": "x", "entry": [entry(cfg, "L4")]}, None, tree(release(ROBOTS_013)), None, "0.1.3")

    def text(self, steps):
        return R.resolve(self.route(), {"version": "0.1.3", "ok": True, "steps": steps})[0]

    def test_wordings(self):
        got = self.text([{"id": "robots_read", "ok": False}, {"id": "robots_late", "ok": True}])
        self.assertEqual(got["text"], "Until a host's `robots.txt` is back, it fetches that host's pages, disallowed "
                                      "ones too. It ignores `Crawl-delay`, and reads `robots.txt` only over https.")
        self.assertLessEqual(len(got["text"].split()), rr.LIST_MAX_WORDS)
        old = ("It ignores `Crawl-delay`, and asks for `robots.txt` only over https, so a plain-http site's rules are "
               "not read.")
        self.assertEqual(self.text([{"id": "robots_read", "ok": False},
                                    {"id": "robots_late", "ok": False, "skipped": True}])["text"], old)
        self.assertEqual(self.text([{"id": "robots_read", "ok": False}, {"id": "robots_late", "ok": False}])["text"], old)
        self.assertFalse(self.text([{"id": "robots_read", "ok": False}])["verified"], "no late probe at all")


class Name(unittest.TestCase):
    """r15-3 #2: the name rustmapper sends, and the flag that changes it, after L1."""

    CLI = ('pub enum Commands {\n    Crawl {\n        #[arg(short, long, default_value = "RustSitemapCrawler/1.0", '
           'help = "User agent string for requests")]\n        user_agent: String,\n    },\n}\n')
    NET = "let client = Client::builder().user_agent(&user_agent).build();\n"

    def resolve(self, cli=None, net=None, ok=True):
        cfg, _ = load()
        r = R.verify_route({"repo": "x", "entry": [entry(cfg, "L7")]}, None,
                           tree({"src/cli.rs": cli or self.CLI, "src/network.rs": net or self.NET}), None, "0.1.3")
        return R.resolve(r, {"version": "0.1.3", "ok": True, "steps": [{"id": "ua_seen", "ok": ok}]})[0]

    def test_fixture_holds(self):
        got = self.resolve()
        self.assertTrue(got["verified"], got["missing"])
        self.assertEqual(rr.lever_line(got["text"]), "It names itself `RustSitemapCrawler/1.0`, with no way to reach "
                                                     "you.<br>`--user-agent <your-bot>` sends your name instead.")

    def test_a_contact_fails_it(self):
        contact = self.CLI.replace('"RustSitemapCrawler/1.0"', '"rustmapper/0.1.4 (+https://github.com/x/y)"')
        self.assertFalse(self.resolve(cli=contact)["verified"])
        self.assertFalse(self.resolve(net=self.NET + '.header(header::FROM, contact)')["verified"])
        self.assertFalse(self.resolve(ok=False)["verified"], "the probe saw a contact or a From")

    def test_committed(self):
        text = read(README)
        items = [ln for ln in text.split("Before you run 0.1.3:", 1)[1].split("<details>", 1)[0].splitlines()
                 if ln.startswith("- ")]
        self.assertTrue(items[0].startswith("- It sends requests with no pause"))
        self.assertEqual(items[1], "- It names itself `RustSitemapCrawler/1.0`, with no way to reach you.<br>"
                                   "`--user-agent <your-bot>` sends your name instead.")
        _, stats = load()
        self.assertEqual(readme_check.cautions_placed(text, stats), [])


class Fallback(unittest.TestCase):
    """r15-3 #1: every width is served by a <source>, and the <img> is the phone edition."""

    SHEETS = {"hero-day": {"w": 1000, "h": 707, "text": [{"size": 19}]},
              "hero-mid-day": {"w": 820, "h": 707, "text": [{"size": 19}]},
              "hero-phone-day": {"w": 600, "h": 1121, "text": [{"size": 26}]}}
    WANT = {360: "hero-phone-day", 390: "hero-phone-day", 851: "hero-phone-day", 852: "hero-mid-day",
            1199: "hero-mid-day", 1200: "hero-day", 1920: "hero-day"}

    def test_committed(self):
        text = read(README)
        pic = text.split("<picture>", 1)[1].split("</picture>", 1)[0]
        self.assertEqual(pic.count("<source "), 6)
        self.assertRegex(pic, r'<img src="[^"]*/hero-phone-day\.svg"')
        for vw, name in self.WANT.items():
            self.assertEqual(column.served(text, vw), name, vw)
        self.assertEqual(column.fallback_faults(text, self.SHEETS), [])

    def test_the_check_bites(self):
        text = read(README)
        desk_img = re.sub(r'(<img src="[^"]*/)hero-phone-day(\.svg")', r"\1hero-day\2", text)
        faults = " ".join(column.fallback_faults(desk_img, self.SHEETS))
        self.assertIn("not a phone edition", faults)
        self.assertIn("5.", faults.split("sets its smallest text at", 1)[1][:4])      # 19 x 278 / 1000 = 5.3 px
        gap = re.sub(r'<source media="\(min-width: 1200px\)" srcset="[^"]*">\n', "", text)
        self.assertIn("1200–1920 px match no <source>", " ".join(column.fallback_faults(gap, self.SHEETS)))


class Wheel(unittest.TestCase):
    """r15-3 #3: the install note names the platforms a source build was run on; the rest are not tried."""

    WHEELS = ["cp313-cp313-macosx_11_0_arm64"]
    LINUX = {"runner": "Linux x86_64", "install": "sdist (built with Rust)",
             "steps": [{"id": "install", "ok": True, "secs": 171.4, "cache": "cold", "cpus": 4,
                        "runs": [168.2, 171.4, 174.3]}]}

    def test_one_runner(self):
        self.assertEqual(rr._wheel_sentence(self.WHEELS, self.LINUX),
                         "Prebuilt for Apple silicon on CPython 3.13. On Linux x86_64, `pip` builds it from source, "
                         "which needs a Rust toolchain (3 min from a cold cache on a 4-core machine); other platforms "
                         "were not tried.")

    def test_two_runners(self):
        win = dict(self.LINUX, runner="Windows x86_64")
        got = rr._wheel_sentence(self.WHEELS, [self.LINUX, win])
        self.assertIn("On Linux x86_64 and Windows x86_64, `pip` builds it from source", got)
        self.assertNotIn("other platforms", got, "the three common platforms are covered")

    def test_no_run_check(self):
        self.assertEqual(rr._wheel_sentence(self.WHEELS, None),
                         "Prebuilt for Apple silicon on CPython 3.13. `pip` builds it from source elsewhere, which "
                         "needs a Rust toolchain; this was not tried.")
        mac = {"runner": "macOS arm64", "install": "prebuilt wheel", "steps": [{"id": "install", "ok": True}]}
        self.assertIn("this was not tried", rr._wheel_sentence(self.WHEELS, mac))

    def test_committed(self):
        self.assertIn("Prebuilt for Apple silicon on CPython 3.13. On Linux x86_64, `pip` builds it from source",
                      read(README))
        self.assertNotIn("elsewhere `pip`", read(README))


class DataLine(unittest.TestCase):
    """r15-2 #5: the data line names both schemes once the https probes ran, and only then."""

    def test_follows_the_probes(self):
        cfg, stats = load()
        line = rr.route_clause(stats, {})
        self.assertIn("its commands were run, with seeding off, against local test sites over http and https on "
                      "10 Oct 2026 (Linux x86_64).", line)
        s = copy.deepcopy(stats)
        for st in s["runcheck"]["rustmapper"]["steps"]:
            if st["id"] == "robots_stall":
                st.update(ok=False, skipped=True)
        self.assertIn("against a local 3-page site on", rr.route_clause(s, {}))
        self.assertIn("over http and https", read(README))


if __name__ == "__main__":
    unittest.main()
