"""Round 6, review round 2: every figure on the page has a definition the code stands behind.

The working rules' months come from git and credit only his own commits (data/proof.py, checks/notices.py); the
numbers typed into the README's prose rest on [[figures]] rows (checks/figures.py); the page links every public
repository it counts (checks/repos.py, build_stats.list_repositories); a short repeat of code or a date between the
image and the text fails (checks/strings.py); the install time prints only when it was measured cold; CI's jobs are
read.
"""
from __future__ import annotations

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

import build_stats  # noqa: E402
import render_readme as rr  # noqa: E402
from checks import figures as figures_check  # noqa: E402
from checks import notices as notices_check  # noqa: E402
from checks import repos as repos_check  # noqa: E402
from checks import strings as strings_check  # noqa: E402
from data import github, proof  # noqa: E402

IDENT = {"names": ["Ben Russell", "Benjamin Russell"], "emails": ["b@x"], "bots": ["Claude"], "login": "BenjaminSRussell"}


class Ctx:
    def __init__(self, stats=None, cfg=None, readme=""):
        self.stats, self.cfg, self.readme = stats or {}, cfg or {}, readme


class Rules(unittest.TestCase):
    NOTICES = [{"n": 1, "cite": "Scrapy, {month:breaker}: a breaker.", "date": "2025-09",
                "anchors": [{"key": "breaker", "repo": "Scrapy", "text": "class CircuitBreaker"}]},
               {"n": 4, "cite": "x, {month:p}.", "date": "2025-11", "anchors": [{"key": "p", "repo": "x", "text": "u"}]}]

    def adding(self, commits):
        return lambda gd, text, path=None: commits.get((gd, text), [])

    def test_month_is_his_first_commit(self):
        commits = {("S.git", "class CircuitBreaker"): [
            {"sha": "e6fe879" + "0" * 33, "date": "2025-08-01", "name": "Claude", "email": "noreply@anthropic.com"},
            {"sha": "fd33c11" + "0" * 33, "date": "2025-09-29", "name": "Benjamin Russell", "email": "b@x"}],
            ("x.git", "u"): [{"sha": "2be623e" + "0" * 33, "date": "2025-11-13", "name": "Ben Russell", "email": "b@x"}]}
        rules = proof.rule_records(self.NOTICES, {"Scrapy": "S.git", "x": "x.git"}, IDENT, adding=self.adding(commits))
        r1 = rules[0]
        self.assertEqual((r1["sha"], r1["date"], r1["first_sha"], r1["first_is_his"]),
                         ("fd33c11", "2025-09-29", "e6fe879", False))
        self.assertEqual(proof.fill_cite(self.NOTICES[0]["cite"], 1, rules), ("Scrapy, Sep 2025: a breaker.", []))
        found = notices_check.check(Ctx({"rules": rules}, {"notices": self.NOTICES}))
        self.assertIn("NOTICE-AUTHOR", [f.code for f in found])           # an agent wrote it first
        named = [dict(self.NOTICES[0], names_agent=True), self.NOTICES[1]]
        self.assertNotIn("NOTICE-AUTHOR", [f.code for f in notices_check.check(Ctx({"rules": rules}, {"notices": named}))])

    def test_not_found_or_typed_wrong_fails(self):
        rules = proof.rule_records(self.NOTICES, {"Scrapy": "S.git", "x": "x.git"}, IDENT, adding=self.adding({}))
        self.assertEqual(proof.fill_cite(self.NOTICES[0]["cite"], 1, rules)[1], ["breaker"])
        codes = [f.code for f in notices_check.check(Ctx({"rules": rules}, {"notices": self.NOTICES})) if f.level == "fail"]
        self.assertEqual(codes.count("NOTICE-DATE"), 2)
        commits = {("S.git", "class CircuitBreaker"): [
            {"sha": "a" * 40, "date": "2025-10-04", "name": "Ben Russell", "email": "b@x"}]}
        rules = proof.rule_records(self.NOTICES[:1], {"Scrapy": "S.git"}, IDENT, adding=self.adding(commits))
        msgs = [f.msg for f in notices_check.check(Ctx({"rules": rules}, {"notices": self.NOTICES[:1]})) if f.level == "fail"]
        self.assertTrue(any("2025-09 is not the computed 2025-10" in m for m in msgs), msgs)

    def test_no_clone_carries_the_cache_marked_stale(self):
        cache = [{"n": 1, "key": "breaker", "repo": "Scrapy", "text": "class CircuitBreaker", "found": True,
                  "sha": "fd33c11", "date": "2025-09-29"}]
        rules = proof.rule_records(self.NOTICES[:1], {}, IDENT, cache)
        self.assertTrue(rules[0]["stale"] and rules[0]["found"])

    def test_committed_rules(self):
        with open(os.path.join(ROOT, "assets", "stats.json"), encoding="utf-8") as fh:
            stats = json.load(fh)
        with open(os.path.join(ROOT, "chart.toml"), "rb") as fh:
            cfg = tomllib.load(fh)
        fails = [f for f in notices_check.check(Ctx(stats, cfg)) if f.level == "fail"]
        self.assertEqual(fails, [])
        block = rr.notices_block(cfg, stats).replace("\u00a0", " ")
        # review round 7: rule 1 cites the per-host breakers that run (his 099dd6c), not the uncalled class
        self.assertIn("*Scrapy, Oct 2026: a circuit breaker for each host in stage 2.*", block)
        self.assertIn("*Scrapy, Oct 2025, the Delta Lake tables.*", block)
        self.assertNotIn("write-ahead", block)
        self.assertNotIn("?", block.replace("don't", ""))

    def test_notice_anchors_rule_two_is_not_the_wal(self):
        """NOTICE-ANCHORS, review round 5: rule 2 says the raw layer is appended to and never overwritten. rustmapper's
        write-ahead log is truncated after each checkpoint (src/wal.rs checkpoint(), every 64 commits or 64 MiB), a
        durability buffer, so no rule 2 anchor may point at it, and no rule 2 record may remain in stats.json."""
        with open(os.path.join(ROOT, "chart.toml"), "rb") as fh:
            cfg = tomllib.load(fh)
        with open(os.path.join(ROOT, "assets", "stats.json"), encoding="utf-8") as fh:
            stats = json.load(fh)
        two = next(n for n in cfg["notices"] if n["n"] == 2)
        self.assertIn("never overwritten", two["body"])
        for a in two.get("anchors") or []:
            self.assertNotEqual(a.get("key"), "wal", a)
            self.assertFalse(str(a.get("path") or "").endswith("wal.rs"), a)
            self.assertNotIn("crc32c", str(a.get("text")), a)          # the WAL's record framing, [u32 len][u32 crc32c]
            self.assertNotEqual(a.get("repo"), "Rust-sitemap", a)
        self.assertNotIn("write-ahead", two["cite"])
        self.assertEqual([r["key"] for r in stats["rules"] if r["n"] == 2], ["delta"])


class Figures(unittest.TestCase):
    ROWS = [{"text": "25 ways", "repo": "u", "glob": "src/organizers/method_*.py", "count": 25},
            {"text": "localhost:3000", "repo": "s", "path": "docker-compose.yml", "literal": '"3000:3000"'}]

    def records(self, n_methods=25, compose='ports: ["3000:3000"]'):
        files = {f"src/organizers/method_{i:02d}_x.py" for i in range(n_methods)}
        return proof.figure_records(self.ROWS, {"u": "u.git", "s": "s.git"},
                                    read=lambda gd, p: compose if p == "docker-compose.yml" else None,
                                    ls=lambda gd: sorted(files))

    def test_rows_hold_at_head(self):
        recs = self.records()
        self.assertTrue(all(r["holds"] for r in recs))
        bad = self.records(24, "ports: []")
        self.assertEqual([r["holds"] for r in bad], [False, False])
        self.assertIn("24 files match", bad[0]["why"])

    def test_every_typed_number_needs_a_row(self):
        readme = ("25 ways to sort URLs. Grafana opens on http://localhost:3000. A [3d-swift-widget](x) and a "
                  "Three.js wheel. <!-- n:more_count -->15<!-- /n --> more. <!-- survey:start -->22 repos<!-- survey:end -->"
                  " across seven languages, stage 4.")
        hits = figures_check.uncovered(readme, self.records())
        self.assertEqual(len(hits), 2, hits)                   # "seven" and "4"; the rest is covered or not prose
        self.assertTrue(hits[0].startswith("'seven'") and hits[1].startswith("'4'"), hits)

    def test_committed_readme_has_no_bare_figure(self):
        with open(os.path.join(ROOT, "assets", "stats.json"), encoding="utf-8") as fh:
            stats = json.load(fh)
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            readme = fh.read()
        self.assertEqual([f.msg for f in figures_check.check(Ctx(stats, readme=readme)) if f.level == "fail"], [])
        self.assertNotIn("25+", readme)
        self.assertNotIn("seven languages", readme)
        self.assertNotIn("Most pages", readme)


class Repos(unittest.TestCase):
    def test_list_unites_cache_rest_and_confirmed_links(self):
        names, used = build_stats.list_repositories(
            "B", ["a", "b"], None, rest_repos=lambda o, t: None,
            rest_repo=lambda o, n, t: {"fork": n == "forked", "private": False}, links=["b", "new", "forked"])
        self.assertEqual((names, used), (["a", "b", "new"], ["cache", "readme"]))
        names, used = build_stats.list_repositories("B", ["a"], None, rest_repos=lambda o, t: ["a", "c"],
                                                    rest_repo=lambda o, n, t: None, links=[])
        self.assertEqual((names, used), (["a", "c"], ["cache", "rest"]))

    def test_rest_repos_drops_forks(self):
        orig = github._rest
        github._rest = lambda path, token=None, timeout=20: [{"name": "a", "fork": False}, {"name": "f", "fork": True}]
        try:
            self.assertEqual(github.rest_repos("B"), ["a"])
            github._rest = lambda *a, **k: None
            self.assertIsNone(github.rest_repos("B"))
        finally:
            github._rest = orig

    def test_repo_set(self):
        stats = {"login": "B", "repos": [{"name": "B"}, {"name": "x"}, {"name": "y"}, {"name": "z"}]}
        good = ("[x](https://github.com/B/x) <details><summary><!-- n:more_count -->2<!-- /n --> more repositories: "
                "</summary> [y](https://github.com/B/y) [z](https://github.com/B/z)</details>")
        self.assertEqual([f.level for f in repos_check.check(Ctx(stats, readme=good))], ["info"])
        bad = good.replace("[z](https://github.com/B/z)", "[w](https://github.com/B/w)")
        msgs = [f.msg for f in repos_check.check(Ctx(stats, readme=bad)) if f.level == "fail"]
        self.assertTrue(any("links w" in m for m in msgs) and any("z is a public" in m for m in msgs), msgs)
        short = good.replace("-->2<!--", "-->3<!--")
        self.assertTrue(any("says 3 more" in f.msg for f in repos_check.check(Ctx(stats, readme=short))))

    def test_more_count_is_computed(self):
        text = ("<!-- facts:A:start --><!-- facts:A:end --><!-- facts:B:start --><!-- facts:B:end -->\n**Also**\n\n"
                "- [**c**](u) — c\n- [**d**](u) — d\n\n<details>")
        self.assertEqual(rr.more_count(text, {"repo_count": 22}), 22 - 1 - 2 - 2)
        self.assertIsNone(rr.more_count(text, {}))


class Repeats(unittest.TestCase):
    def test_short_code_and_date_runs_fail(self):
        hero = ["rust_sitemap crawl --start-url <site>", "pip install rustmapper", "0.1.3 · 8 NOV 2025",
                "saved every 50 ms"]
        page = "run rust_sitemap crawl --start-url x; pip install rustmapper; 8 Nov 2025 out; saved every 50 ms"
        self.assertEqual(strings_check.twice(hero, page), ["rust_sitemap crawl --start-url", "8 nov 2025"])
        self.assertTrue(strings_check.code_or_date(("data/sitemap.jsonl", "a", "b")))
        self.assertFalse(strings_check.code_or_date(("saved", "every", "50")))


class InstallTime(unittest.TestCase):
    RC = {"runner": "Linux x86_64", "install": "sdist (built with Rust)",
          "steps": [{"id": "install", "ok": True, "secs": 171.4, "cache": "cold", "cpus": 4, "runs": [168.2, 171.4, 174.3]}]}

    def test_time_only_when_cold(self):
        self.assertEqual(rr.install_time(self.RC), "3 min from a cold cache on a 4-core Linux x86_64 machine")
        warm = {**self.RC, "steps": [dict(self.RC["steps"][0], cache=None)]}
        self.assertIsNone(rr.install_time(warm))
        self.assertIsNone(rr.install_time({**self.RC, "steps": [{"id": "install", "ok": True, "secs": 179.8}]}))
        wheel = {**self.RC, "install": "prebuilt wheel"}
        self.assertIsNone(rr.install_time(wheel))
        note = rr._wheel_sentence(["cp313-cp313-macosx_11_0_arm64"], warm)
        self.assertEqual(note, "Prebuilt for Apple silicon on CPython 3.13; elsewhere `pip` builds it from source, "
                               "which needs a Rust toolchain.")
        self.assertIn("(3 min from a cold cache", rr._wheel_sentence(["cp313-cp313-macosx_11_0_arm64"], self.RC))
        spread = {**self.RC, "steps": [dict(self.RC["steps"][0], runs=[170.0, 250.0])]}
        self.assertTrue(rr.install_time(spread).startswith("3–4 min"))


class CiJobs(unittest.TestCase):
    def test_jobs_and_the_not_blocking_words(self):
        orig = github._rest
        github._rest = lambda path, token=None, timeout=20: {"jobs": [
            {"name": "Test", "conclusion": "success", "labels": ["ubuntu-latest"]},
            {"name": "Security Audit", "conclusion": "failure", "labels": ["ubuntu-latest"]}]}
        try:
            jobs = github.rest_jobs("o", "r", "https://github.com/o/r/actions/runs/37704909539")
            self.assertEqual(jobs[1], {"name": "Security Audit", "conclusion": "failure", "labels": ["ubuntu-latest"]})
            self.assertIsNone(github.rest_jobs("o", "r", None))
        finally:
            github._rest = orig
        stats = {"repos": [{"name": "x", "head": {"short": "32c2651"}, "test_functions": 3,
                            "ci": {"conclusion": "success", "date": "2026-10-07", "jobs": jobs}}]}
        self.assertEqual(rr.facts_block(stats, "x").replace("\u00a0", " "),
                         "*On main at `32c2651`: 3 tests · CI passed 7 Oct 2026, Security Audit failed (not blocking)*")


class Audit(unittest.TestCase):
    def test_register_is_current_and_covers_the_rows(self):
        import audit_figures
        with open(os.path.join(ROOT, "chart.toml"), "rb") as fh:
            cfg = tomllib.load(fh)
        with open(audit_figures.AUDIT, encoding="utf-8") as fh:
            text = fh.read()
        self.assertEqual(audit_figures.render(text, cfg), text, "run python3 scripts/audit_figures.py")
        block = audit_figures.block(cfg)
        for f in cfg["figures"]:
            self.assertIn(f"| sorted {f['text']} by {f['repo']} |" if f.get("handoff") else f"| {f['text']} |", block)
        self.assertIn("{month:breaker}", block)
        self.assertIn("BATCH_TIMEOUT_MS", block)
        # review round 7: every route entry whose words read a figure has a row
        for gid in ("F1", "H1", "L1", "X1"):
            self.assertIn(f"`routes.rustmapper` {gid}", block, gid)
        self.assertNotIn("CODE 32c2651 · 7 OCT 2026\"", text)
        self.assertNotIn("it is the light's period", text)


if __name__ == "__main__":
    unittest.main()
