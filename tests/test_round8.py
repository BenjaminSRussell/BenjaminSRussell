"""Review round 8 (docs/crit/round6/review-r08-*.md): what each fix promises, held by a test.

One count for ideal-url-organizer across the page; the phone's heading stands apart from the role line; go_go_go and
Ai_code_detector say what they do; rule 3 states its measured days and every cite has one form; F1 says the per-host
cap while 0.1.3's governor cannot slow a site; C1 gives its caution and the line that says it is done; the two levers
for the load warning, on a probe; what rustmapper cannot see; which Compose the Scrapy quickstart needs.
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
import runcheck  # noqa: E402
from checks import audit_cover, notices as notices_check, route as route_check, strings  # noqa: E402
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


def entry(cfg, gid):
    return next(e for e in cfg["route"]["rustmapper"]["entry"] if e["id"] == gid)


def also_line(text, repo):
    return next(ln for ln in text.splitlines() if ln.startswith("- ") and f"/{repo})" in ln)


class Ctx:
    def __init__(self, stats=None, cfg=None, readme="", report=None):
        self.stats, self.cfg, self.readme, self.report = stats or {}, cfg or {}, readme, report


def release_only(e):
    """A route entry with its head anchors dropped, so a fixture release tree alone decides it."""
    e = copy.deepcopy(e)
    for c in [e] + e.get("instead", []):
        c.pop("head", None)
    e["scope"] = "release"
    return e


class OneCount(unittest.TestCase):
    """r08-1 #1, r08-2 #2, r08-3 #1: 25 ways, said as 21 and 4 more, with the image's 21."""

    ROWS = [{"text": "3 ways", "repo": "o", "glob": "m_*.py", "count": 3, "parts": ["2 from", "1 more"]},
            {"text": "2 from", "repo": "o", "path": "main.py", "keys": "self.methods", "count": 2},
            {"text": "1 more", "repo": "o", "glob": "m_*.py", "contains": "List[PageContent]", "count": 1}]
    FILES = {"main.py": "class P:\n    def __init__(self):\n        self.methods = {'a': 1, 'b': 2}\n",
             "m_1.py": "def organize(urls): pass", "m_2.py": "def organize(urls): pass",
             "m_3.py": "def organize(self, pages: List[PageContent]): pass"}

    def records(self, files):
        return proof.figure_records(self.ROWS, {"o": "gd"}, read=lambda gd, p: files.get(p),
                                    ls=lambda gd: sorted(files))

    def test_parts_add_up(self):
        recs = {r["text"]: r for r in self.records(self.FILES)}
        self.assertEqual([recs[t]["measured"] for t in ("3 ways", "2 from", "1 more")], [3, 2, 1])
        self.assertTrue(all(r["holds"] for r in recs.values()), recs)

    def test_parts_that_do_not_add_up(self):
        files = dict(self.FILES, **{"m_2.py": "def organize(self, pages: List[PageContent]): pass"})
        recs = {r["text"]: r for r in self.records(files)}
        self.assertFalse(recs["1 more"]["holds"], "two files take PageContent now")
        self.assertFalse(recs["3 ways"]["holds"])

    def test_strings_count(self):
        hero = ["sorted 21 ways by ideal-url-organizer"]
        repos = ["ideal-url-organizer", "go_go_go"]
        only25 = "- [**ideal-url-organizer**](https://github.com/x/ideal-url-organizer) — 25 ways to sort a pile of URLs.\n"
        self.assertTrue(strings.count_mismatch(hero, only25, repos))
        both = only25.replace("URLs.", "URLs: 21 from the URLs, 4 more from the pages.")
        self.assertEqual(strings.count_mismatch(hero, both, repos), [])
        self.assertTrue(strings.count_mismatch(hero, "no list line at all", repos))

    def test_committed(self):
        cfg, stats = load()
        line = also_line(read(README), "ideal-url-organizer")
        self.assertIn("25 ways to sort a pile of URLs: 21 from the URLs and their crawl records", line)
        self.assertIn("4 more from the fetched pages", line)
        recs = {f["text"]: f for f in stats["figures"] if f["repo"] == "ideal-url-organizer"}
        self.assertEqual((recs["21 from"]["measured"], recs["4 more"]["measured"], recs["25 ways"]["measured"]),
                         (21, 4, 25))
        self.assertEqual(recs["21 from"]["measured"], recs["21 ways"]["measured"], "the image and the page agree")
        self.assertTrue(all(r["holds"] for r in recs.values()))


class PhoneHeading(unittest.TestCase):
    """r08-1 #2, r08-3 #3: the project's name stands two role pitches under the role line on the phone."""

    def texts(self, gap):
        return [{"key": "copy:role_line", "y": 204}, {"key": "copy:role_line", "y": 238},
                {"key": "routes:project", "y": 238 + gap}]

    def test_check(self):
        self.assertTrue(route_check.head_gap(self.texts(50), "phone"))
        self.assertEqual(route_check.head_gap(self.texts(70), "phone"), [])
        self.assertEqual(route_check.head_gap(self.texts(68), "phone"), [])

    def test_layout(self):
        G = sheet.L["phone"]
        self.assertGreaterEqual(G["head_after_title"], route_check.HEAD_GAP_PITCHES * G["role_pitch"])
        self.assertEqual(G["head_after_title"], 70)
        self.assertIsNone(sheet.L["desk"]["head_after_title"], "the desk sets the route in its own column")


class AlsoLines(unittest.TestCase):
    """r08-1 #3, #6: go_go_go without browser impersonation; Ai_code_detector says what `aicd scan` does."""

    def test_go_go_go(self):
        line = also_line(read(README), "go_go_go")
        self.assertNotRegex(line, r"(?i)fingerprint|imperson|JA3|stealth|evad")
        self.assertIn("plus optional headless-Chrome rendering and SQLite storage with full-text search", line)
        cfg, stats = load()
        rows = {f["text"]: f for f in stats["figures"] if f["repo"] == "go_go_go"}
        self.assertEqual(set(rows), {"resume and export-sitemap commands", "optional headless-Chrome rendering",
                                     "SQLite storage with full-text search"})
        self.assertTrue(all(r["holds"] for r in rows.values()), rows)
        self.assertNotIn("tls-fingerprint", read(CFG))

    def test_ai_code_detector(self):
        line = also_line(read(README), "Ai_code_detector")
        self.assertIn("`aicd scan` scores each file of a repository for signs of AI authorship", line)
        self.assertIn("says why it flagged it", line)
        _, stats = load()
        rows = [f for f in stats["figures"] if f["repo"] == "Ai_code_detector"]
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(r["holds"] for r in rows), rows)


class RuleDays(unittest.TestCase):
    """r08-1 #4: "Measure from the start.", the days computed from git."""

    RULES = [{"n": 3, "key": "prometheus", "found": True, "date": "2025-10-01", "repo_first": "2025-09-25"},
             {"n": 3, "key": "grafana", "found": True, "date": "2025-10-06", "repo_first": "2025-09-25"}]
    BODY = "Metrics {days:prometheus} days in, a dashboard {days:prometheus..grafana} days later."

    def test_fixture_dates(self):
        self.assertEqual(proof.fill_days(self.BODY, 3, self.RULES),
                         ("Metrics 6 days in, a dashboard 5 days later.", []))

    def test_not_computed(self):
        rules = [dict(self.RULES[0], repo_first=None), self.RULES[1]]
        text, missing = proof.fill_days(self.BODY, 3, rules)
        self.assertEqual(missing, ["{days:prometheus}"])
        self.assertIn("?", text)
        cfg = {"notices": [{"n": 3, "title": "T.", "body": self.BODY, "cite": "Scrapy, {month:prometheus}: m.",
                            "date": "2025-10", "anchors": [{"key": "prometheus", "repo": "Scrapy", "text": "p"},
                                                           {"key": "grafana", "repo": "Scrapy", "text": "g"}]}]}
        stats = {"rules": [dict(r, first_is_his=True, sha="x", text="p") for r in rules]}
        self.assertIn("NOTICE-DATE", [f.code for f in notices_check.check(Ctx(stats, cfg)) if f.level == "fail"])

    def test_repo_first(self):
        notices = [{"n": 3, "body": "{days:p}", "anchors": [{"key": "p", "repo": "S", "text": "t"}]}]
        commits = [{"sha": "a" * 40, "date": "2025-10-01", "name": "Ben Russell", "email": "e"}]
        recs = proof.rule_records(notices, {"S": "gd"}, {"names": ["Ben Russell"], "emails": []},
                                  adding=lambda gd, t, p=None: commits, first_of=lambda gd: "2025-09-25")
        self.assertEqual(recs[0]["repo_first"], "2025-09-25")

    def test_committed(self):
        cfg, stats = load()
        block = rr.notices_block(cfg, stats).replace("\u00a0", " ")
        self.assertIn("3. **Measure from the start.** Metrics were exported 6 days after the first commit, and a "
                      "dashboard was up 5 days after that.", block)
        self.assertNotIn("before speed", block)
        bodies = {n["n"]: n for n in cfg["notices"]}
        for n in range(1, 5):          # no body opens on its title's first word unless it carries a figure
            title, body = bodies[n]["title"].split()[0].lower().strip("."), bodies[n]["body"]
            first = body.split()[0].lower()
            self.assertTrue(first != title or re.search(r"\d|\{days:", body), n)
        recs = [r for r in audit_figures.records(cfg) if r.get("rule") == 3]
        self.assertEqual(sum("{days:" in r["printed"] for r in recs), 2)


class CiteForm(unittest.TestCase):
    """r08-1 #5: every printed cite reads "<repo>, <Mon YYYY>: <what>."."""

    def test_committed(self):
        cfg, stats = load()
        for nt in sorted(cfg["notices"], key=lambda n: n["n"])[:4]:
            text, missing = proof.fill_cite(nt["cite"], nt["n"], stats["rules"])
            self.assertEqual(missing, [])
            self.assertRegex(text, notices_check.CITE_FORM, nt["n"])
        self.assertIn("*Scrapy, Oct\u00a02025: raw pages written to Delta Lake with `write_deltalake`.*", read(README))

    def test_comma_fails(self):
        cfg, stats = load()
        bad = copy.deepcopy(cfg)
        next(n for n in bad["notices"] if n["n"] == 2)["cite"] = "Scrapy, {month:delta}, the Delta Lake tables."
        codes = [f.code for f in notices_check.check(Ctx(stats, bad)) if f.level == "fail"]
        self.assertEqual(codes, ["NOTICE-CITE"])
        self.assertEqual([f.code for f in notices_check.check(Ctx(stats, cfg)) if f.level == "fail"], [])


GOVERNOR = """
async fn governor_task() {{
    const THROTTLE_THRESHOLD_MS: f64 = 500.0;
    let current_permits = permits.available_permits();
    if commit_ewma_ms > THROTTLE_THRESHOLD_MS {{ {guard} {{ shrink(); }} }} else {{ permits.add_permits(1); }}
}}
"""
SCOPE = {"src/bfs_crawler.rs": "frontier.add_links(discovered_links); BfsCrawler::is_same_domain(a, b);",
         "src/url_utils.rs": "fn is_same_domain() { url_domain.ends_with(base_domain) || base_domain.ends_with(url_domain) }",
         "src/state.rs": "HostState { max_inflight: 20, }",
         "src/frontier.rs": "if current_inflight >= host_state.max_inflight { requeue(); }"}
RC = {"version": "0.1.3", "ok": True, "steps": [{"id": "crawl_ctrl_c", "ok": True}]}


class PerHostCap(unittest.TestCase):
    """r08-2 #1: F1 says the per-host cap while the governor stops at a floor of idle permits."""

    def resolve(self, guard):
        cfg, _ = load()
        files = dict(SCOPE, **{"src/main.rs": GOVERNOR.format(guard=guard)})
        route = R.verify_route({"repo": "x", "entry": [release_only(entry(cfg, "F1"))]}, None, files.get, None, "0.1.3")
        return R.resolve(route, RC)[0]

    def test_with_the_floor(self):
        got = self.resolve("if current_permits > MIN_PERMITS")
        self.assertTrue(got["verified"], got)
        self.assertEqual(got["text"], "fetches up to 20 pages at a time from each host; queues their links to your "
                                      "site, its subdomains and its parent domain")

    def test_without_the_floor(self):
        got = self.resolve("if true")
        self.assertTrue(got["text"].startswith("fetches pages, fewer at once when saves average over 500 ms;"), got)

    def test_committed(self):
        cfg, stats = load()
        drawn = {e["id"]: e for e in R.drawn(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"])}
        self.assertIn("each host", drawn["F1"]["text"])
        self.assertNotIn("to one host", drawn["L1"]["text"], "the per-host 20 is said once, in the image")
        self.assertIn("at most 256 at a time across all hosts", drawn["L1"]["text"])
        self.assertIn("from one host", sheet.PURPOSE["F1"][0])


SHUTDOWN = """
async fn main() {{
    tokio::spawn(async move {{
        println!("Press Ctrl+C again to force quit");
        {a}
        {b}
        let path = dir.join("sitemap.jsonl");
    }});
}}
"""
EXIT = 'tokio::spawn(async move { eprintln!("Force quit requested, exiting immediately..."); std::process::exit(1); });'
EXPORT = 'if let Err(e) = c.export_to_jsonl(&path).await { } else { println!("Saved to: {}", path.display()); }'


class SecondCtrlC(unittest.TestCase):
    """r08-3 #2: C1's caution and the line that says it is done, on anchors and the second_ctrl_c probe."""

    def resolve(self, src, second_ok=True):
        cfg, _ = load()
        rc = {"version": "0.1.3", "ok": True, "steps": [{"id": "crawl_ctrl_c", "ok": True},
                                                       {"id": "second_ctrl_c", "ok": second_ok}]}
        route = R.verify_route({"repo": "x", "entry": [release_only(entry(cfg, "C1"))]}, None,
                               {"src/main.rs": src}.get, None, "0.1.3")
        return R.resolve(route, rc)[0]["text"]

    def test_caution(self):
        self.assertEqual(self.resolve(SHUTDOWN.format(a=EXIT, b=EXPORT)),
                         "press Ctrl-C once; a second press before `Saved to:` quits without writing the file")

    def test_fallbacks(self):
        old = "press Ctrl-C once to write `data/sitemap.jsonl`"
        self.assertEqual(self.resolve(SHUTDOWN.format(a=EXIT, b=EXPORT), second_ok=False), old)
        self.assertEqual(self.resolve(SHUTDOWN.format(a=EXPORT, b=EXIT)), old, "the export before the exit handler")

    def test_verdict(self):
        self.assertTrue(runcheck.second_verdict(1, False, False)[0])
        self.assertFalse(runcheck.second_verdict(0, True, True)[0])
        self.assertFalse(runcheck.second_verdict(1, True, True)[0])

    def test_committed(self):
        _, stats = load()
        steps = {s["id"]: s for s in stats["runcheck"]["rustmapper"]["steps"]}
        self.assertTrue(steps["second_ctrl_c"]["ok"] and not steps["second_ctrl_c"]["gate"])
        self.assertIn("second Ctrl-C", sheet.PURPOSE["C1"][0])


class Levers(unittest.TestCase):
    """r08-2 #3: the two flags that turn it down, printed while probe workers_cap passed."""

    def test_max_open(self):
        self.assertEqual(runcheck.max_open([(0, 1, "/"), (1, 2, "/a"), (2, 3, "/b")]), 1)
        self.assertEqual(runcheck.max_open([(0, 1, "/"), (1, 2.5, "/a"), (1.2, 2.2, "/b")]), 2)
        ok, _ = runcheck.workers_verdict([(0, 1, "/"), (1, 2, "/a"), (1, 2, "/b")], [(0, 1, "/"), (1, 2, "/a"), (2, 3, "/b")])
        self.assertTrue(ok)
        self.assertFalse(runcheck.workers_verdict([(0, 1, "/"), (1, 2, "/a")], [(0, 1, "/"), (1, 2, "/a")])[0],
                         "a site that never overlaps cannot show the cap")

    def test_printed_on_the_probe(self):
        _, stats = load()
        route = stats["routes"]["rustmapper"]
        rc = copy.deepcopy(stats["runcheck"]["rustmapper"])
        printed = " ".join(rr.text_entries(route, rc, stats["edition"]))
        self.assertIn("`--workers 1` holds it to one request at a time; `--seeding-strategy none` starts from your URL",
                      printed)
        next(s for s in rc["steps"] if s["id"] == "workers_cap")["ok"] = False
        self.assertNotIn("--workers 1", " ".join(rr.text_entries(route, rc, stats["edition"])))

    def test_register(self):
        cfg, stats = load()
        row = next(r for r in audit_figures.records(cfg) if r.get("entry") == "L2")
        self.assertIn("workers_cap", row["definition"])
        self.assertEqual(audit_cover.uncovered_readme(read(README), audit_figures.records(cfg), stats, cfg), [])


class WhatItSees(unittest.TestCase):
    """r08-2 #5: rustmapper reads the HTML it is sent; go_go_go renders."""

    def resolve(self, cargo):
        cfg, _ = load()
        route = R.verify_route({"repo": "x", "entry": [entry(cfg, "L3")]}, None, {"Cargo.toml": cargo}.get, None, "0.1.3")
        return R.resolve(route)[0]

    def test_html_only(self):
        self.assertTrue(self.resolve('[dependencies]\nscraper = "0.20"\n')["verified"])
        self.assertFalse(self.resolve('[dependencies]\nscraper = "0.20"\nchromiumoxide = "0.7"\n')["verified"])

    def test_committed_paragraphs(self):
        text = read(README)
        self.assertRegex(text, r"\n\nIt reads links from the HTML a server sends; no JavaScript runs\. go_go_go can "
                               r"render pages in headless Chrome\. 0\.1\.3 writes one `sitemap\.xml`")


class Compose(unittest.TestCase):
    """r08-2 #4: the Scrapy quickstart names the hyphenated command start.py looks for."""

    def test_committed(self):
        text = read(README)
        self.assertIn("It needs Docker and the `docker-compose` command: Docker Desktop has it; on Linux, where "
                      "Docker's Compose plugin answers only to `docker compose`, install Compose standalone as well.",
                      text)
        self.assertNotIn("alias", text, "a shell alias is not found by shutil.which")
        _, stats = load()
        row = next(f for f in stats["figures"] if f["text"] == "the `docker-compose` command")
        self.assertTrue(row["holds"], row)


if __name__ == "__main__":
    unittest.main()
