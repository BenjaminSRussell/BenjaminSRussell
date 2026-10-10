"""Review round 9 (docs/crit/round6/review-r09-*.md): what each fix promises, held by a test.

The rustmapper cautions are one short list; no line about what is not released, and the project's link heads its
facts line; the Scrapy run sentence agrees with its `cd`, and what Scrapy does comes before how to run it; S1 has a
verb; the file's `status_code` is explained (X2, probe non200_status); H1's quiet mark has its number ({quiet},
probe quiet_slow_page); the alt text promises the install; the facts lines name the checks CI blocks on.
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
from checks import readme as readme_check  # noqa: E402
from data import route as R, tree as T  # noqa: E402
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


def tree(files):
    return lambda p: files.get(p)


def install(text):
    return text.split("<!-- install:Rust-sitemap:start -->", 1)[1].split("<!-- install:Rust-sitemap:end -->", 1)[0]


class Cautions(unittest.TestCase):
    """r09-1 #1, r09-3 #3: one prose paragraph after the code block (the wheel note), then one short list."""

    def test_committed(self):
        text = read(README)
        self.assertEqual(readme_check.cautions(text), [])
        tail = install(text).split("```", 2)[2]
        paras = [p for p in tail.split("\n\n") if p.strip()]
        self.assertTrue(paras[0].startswith("Prebuilt for Apple silicon"), paras[0])
        self.assertEqual(paras[1], "Before you run 0.1.3:")      # review round 10: the lead names the release
        items = paras[2].strip().splitlines()
        self.assertEqual(len(items), 7)                    # review round 10: L5, the scope lever
        for it in items:
            self.assertTrue(it.startswith("- "), it)
            self.assertLessEqual(len(it[2:].split()), rr.LIST_MAX_WORDS, it)
        self.assertIn("<br>`--workers 1` sends one at a time.", items[0])
        self.assertIn("crt.sh and Common Crawl", items[2])
        self.assertIn("<br>`--seeding-strategy none` asks no one.", items[2])
        self.assertNotIn("20 pages", tail, "the per-host 20 is said once, in the image")

    def test_the_check_bites(self):
        head = "<!-- install:Rust-sitemap:start -->\n```sh\npip install rustmapper\n```\n\nWheel note.\n\n"
        end = "\n<!-- install:Rust-sitemap:end -->\n"
        self.assertEqual(readme_check.cautions(head + "Lead:\n\n- one\n- two" + end), [])
        self.assertTrue(readme_check.cautions(head + "A second paragraph of cautions." + end))
        self.assertTrue(readme_check.cautions(head + "Lead:\n\n" + "\n".join(f"- item {i}" for i in range(8)) + end))
        self.assertTrue(readme_check.cautions(head + "Lead:\n\n- " + " ".join(["word"] * 26) + end))

    def test_retired_items_drop_and_the_lead_goes(self):
        _, stats = load()
        route = copy.deepcopy(stats["routes"]["rustmapper"])
        rc = stats["runcheck"]["rustmapper"]
        blocks = rr.text_blocks(route, rc, stats["edition"])
        self.assertTrue(blocks[0].startswith("Before you run 0.1.3:\n\n- "))
        for e in route["entries"]:
            if e.get("item"):
                e["instead"] = [{"text": "", "verified_head": True, "verified_release": True, "missing": []}]
                e["verified_release"] = False
                e["missing"] = ["retired for the test"]
        self.assertEqual(rr.text_blocks(route, rc, stats["edition"]), [], "no item left: no lead-in")

    def test_lead_in_from_the_route(self):
        cfg, stats = load()
        self.assertEqual(cfg["route"]["rustmapper"]["list_lead"], "Before you run {release}:")
        self.assertEqual(stats["routes"]["rustmapper"]["list_lead"], "Before you run {release}:")


class NothingUnreleased(unittest.TestCase):
    """r09-1 #2, r09-3 #5: no to-do sentence; the project's link heads the facts line."""

    def test_committed(self):
        text = read(README)
        self.assertEqual(readme_check.not_released(text), [])
        self.assertNotIn("not yet released", text)
        facts = text.split("<!-- facts:Rust-sitemap:start -->\n", 1)[1].split("\n", 1)[0]
        self.assertTrue(facts.startswith("**[rustmapper](https://github.com/BenjaminSRussell/Rust-sitemap)** · *on main at `"),
                        facts)
        about = text.split("<!-- about:Rust-sitemap:start -->", 1)[1].split("<!-- about:Rust-sitemap:end -->", 1)[0]
        self.assertEqual(about.strip(), "")

    def test_the_check_bites(self):
        self.assertTrue(readme_check.not_released("The Python API is on main and not yet released."))
        self.assertEqual(readme_check.not_released("Not yet released: build it with `cargo install --git …`."), [])


class ScrapyOrder(unittest.TestCase):
    """r09-1 #3, r09-3 #1, #2: the run sentence agrees with its cd; what Scrapy does before how to run it."""

    def test_committed(self):
        text = read(README)
        self.assertEqual(readme_check.cd_agrees(text), [])
        i = text.index("<!-- facts:Scrapy:end -->")
        self.assertLess(i, text.index("- Raw pages land in Delta Lake"))
        self.assertLess(text.index("- Prometheus metrics on Grafana dashboards."), text.index("Run these from the folder you cloned"))
        self.assertLess(text.index("Run these from the folder you cloned"), text.index("cd Scrapy/Scraping_project"))
        # review round 10: the cd says where to stand; the sentence says what start.py does
        self.assertIn("Run these from the folder you cloned [Scrapy](https://github.com/BenjaminSRussell/Scrapy) into. `python start.py` starts", text)

    def test_the_check_bites(self):
        old = ("Run these from a clone of [Scrapy](https://x), in `Scraping_project` (`start.py` runs only there).\n\n"
               "```sh\ncd Scrapy/Scraping_project\npython start.py\n```\n")
        self.assertTrue(readme_check.cd_agrees(old))


class Seeds(unittest.TestCase):
    """r09-1 #4: S1 has a verb, as every other row."""

    def test_words(self):
        cfg, stats = load()
        s1 = entry(cfg, "S1")
        self.assertTrue(s1["text"].startswith("starts from your URL; by default also from "))
        self.assertNotIn("rather than followed", s1["text"])
        drawn = {e["id"]: e for e in R.drawn(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"])}
        self.assertEqual(drawn["S1"]["text"], s1["text"])


class StatusCode(unittest.TestCase):
    """r09-2 #1: what sitemap.jsonl cannot tell you, on the release's code and probe non200_status."""

    def test_verdict(self):
        paths = [(0, "/"), (1, "/a.html"), (1, "/busy.html"), (1, "/gone.html")]
        recs = {"busy.html": {"status_code": None}, "gone.html": {"status_code": None}}
        ok, detail = runcheck.status_verdict(paths, recs)
        self.assertTrue(ok, detail)
        self.assertIn("status_code null", detail)
        self.assertFalse(runcheck.status_verdict(paths + [(3, "/busy.html")], recs)[0], "asked for again")
        self.assertFalse(runcheck.status_verdict(paths + [(3, "/beyond.html")], recs)[0], "its link followed")
        self.assertFalse(runcheck.status_verdict(paths, dict(recs, **{"busy.html": {"status_code": 429}}))[0])

    def test_committed(self):
        _, stats = load()
        rc = copy.deepcopy(stats["runcheck"]["rustmapper"])
        route = stats["routes"]["rustmapper"]
        x2 = {e["id"]: e for e in R.resolve(route, rc)}["X2"]
        self.assertTrue(x2["verified"] and not x2["retired"], x2)
        self.assertIn("gives no `status_code` to a page that answers 404, 429 or 503", x2["text"])
        self.assertIn("- It gives no `status_code`", read(README))
        # a release that records statuses or asks again: the probe fails and the item retires
        next(s for s in rc["steps"] if s["id"] == "non200_status")["ok"] = False
        x2 = {e["id"]: e for e in R.resolve(route, rc)}["X2"]
        self.assertTrue(x2["verified"] and x2["retired"], x2)

    def test_anchors(self):
        cfg, _ = load()
        spec = {"repo": "x", "entry": [entry(cfg, "X2")]}
        body = ("async fn process_url_streaming(&self) { match f { Ok(response) if response.status().as_u16() == 200 => {} "
                "Ok(_) => { return CrawlResult { result: Ok(Vec::new()) }; } } }\nlet n = SitemapNode { status_code: job.status_code };")
        files = {"src/bfs_crawler.rs": body, "src/frontier.rs": ""}
        self.assertTrue(R.verify_route(spec, None, tree(files), None, "0.1.3")["entries"][0]["verified_release"])
        files = dict(files, **{"src/frontier.rs": 'let wait = headers.get("Retry-After");'})
        self.assertFalse(R.verify_route(spec, None, tree(files), None, "0.1.3")["entries"][0]["verified_release"])


class QuietNumber(unittest.TestCase):
    """r09-2 #2: the clearing mark has its number, computed and probed."""

    def test_formula(self):
        self.assertEqual(R.quiet_secs(20, 3), 30)       # 20 + 4 + 1 = 25 -> 30
        self.assertEqual(R.quiet_secs(30, 3), 40)
        self.assertEqual(R.quiet_secs(25, 3), 30)       # exactly 30 stays 30
        self.assertEqual(R.quiet_secs(20, 4), 30)       # 20 + 8 + 1 = 29 -> 30

    def test_probe_must_wait_as_long(self):
        _, stats = load()
        rc = copy.deepcopy(stats["runcheck"]["rustmapper"])
        route = stats["routes"]["rustmapper"]
        h1 = {e["id"]: e for e in R.resolve(route, rc)}["H1"]
        self.assertEqual(h1["text"], "{release} never exits by itself; done once `Received work item` lines stop for 30 s")
        next(s for s in rc["steps"] if s["id"] == "quiet_slow_page")["quiet_secs"] = 20
        h1 = {e["id"]: e for e in R.resolve(route, rc)}["H1"]
        self.assertEqual(h1["text"], "{release} never exits by itself, even after the last page")

    def test_slow_verdict(self):
        recs = {p: {"status_code": 200} for p in ("index.html", "slow.html", "after.html")}
        stamps = [(0.0, "/"), (0.1, "/slow.html"), (15.2, "/after.html")]
        self.assertTrue(runcheck.slow_verdict(stamps, 46.0, recs)[0])
        self.assertFalse(runcheck.slow_verdict(stamps, 40.0, recs)[0], "SIGINT before the quiet had run its length")
        self.assertFalse(runcheck.slow_verdict([(0.0, "/"), (0.1, "/slow.html"), (2.0, "/after.html")], 40.0, recs)[0],
                         "the slow page was not held")
        self.assertFalse(runcheck.slow_verdict(stamps, 46.0, dict(recs, **{"after.html": {}}))[0], "a page missing")
        self.assertFalse(runcheck.slow_verdict(stamps, None, recs)[0])
        self.assertEqual(runcheck.QUIET_BOUND, 30)

    def test_audited(self):
        import audit_figures
        cfg, _ = load()
        row = next(r for r in audit_figures.records(cfg) if r.get("entry") == "H1")
        self.assertIn("`{quiet}`", row["printed"])
        self.assertIn("quiet_slow_page", row["definition"])


class AltText(unittest.TestCase):
    """r09-2 #3: the image's one command is the install."""

    def test_alt(self):
        cfg, stats = load()
        alt = sheet.alt(stats, cfg)
        self.assertTrue(alt.startswith("How to install Ben Russell's crawler rustmapper"), alt)
        self.assertLessEqual(len(alt.split()), 25)
        self.assertIn('alt="How to install', read(README))


CI_RS = """name: CI
on: [push]
jobs:
  test:
    name: Test
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: cargo test --all-features --verbose
  clippy:
    name: Clippy
    runs-on: ubuntu-latest
    steps:
      - name: Run clippy
        # legacy debt
        run: cargo clippy --all-features --message-format=short || true
  fmt:
    name: Format
    steps:
      - name: Check formatting
        run: cargo fmt --all -- --check
  security-audit:
    name: Security Audit
    continue-on-error: true
    steps:
      - name: Install cargo-audit
        run: cargo install cargo-audit --locked
      - name: Run security audit
        run: cargo audit
        continue-on-error: true  # advisory debt
  benchmark:
    name: Benchmark
    steps:
      - name: Run benchmarks
        run: cargo bench --verbose || echo "No benchmarks configured"
"""

CI_PY = """name: CI/CD Pipeline
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - name: Install
      run: |
        pip install pytest ruff
    - name: Lint with ruff
      working-directory: Scraping_project
      run: |
        ruff check src/ --select F
    - name: Type check with mypy
      run: |
        mypy src/ --config-file mypy.ini
    - name: Security check with bandit
      run: |
        # Blocking at medium+
        bandit -r src/ -ll
    - name: Run default test suite
      run: |
        python -m pytest tests/ \\
          -m "not slow"
  smoke:
    runs-on: ubuntu-latest
    steps:
    - name: bring-up
      run: |
        set +e
        timeout 20 python -m pytest tests/smoke
        set -e
"""

JOBS_RS = [{"name": n, "conclusion": "success"} for n in
           ("Test (ubuntu-latest, stable)", "Clippy", "Format", "Security Audit", "Benchmark")]
JOBS_PY = [{"name": "test (3.11)", "conclusion": "success"}, {"name": "test (3.12)", "conclusion": "success"},
           {"name": "smoke", "conclusion": "success"}]


class CiGates(unittest.TestCase):
    """r09-3 #4: the facts lines name the checks CI blocks on."""

    def test_rust_fixture(self):
        self.assertEqual(T.ci_gates(CI_RS, JOBS_RS), ["tests", "rustfmt"])

    def test_python_fixture(self):
        self.assertEqual(T.ci_gates(CI_PY, JOBS_PY), ["tests", "ruff", "mypy", "bandit"])
        failed = [dict(j, conclusion="failure") if j["name"].startswith("test") else j for j in JOBS_PY]
        self.assertEqual(T.ci_gates(CI_PY, failed), [], "a job that did not pass in the run holds nothing")
        self.assertIsNone(T.ci_gates(None, JOBS_PY))

    def test_facts_line(self):
        base = {"repos": [{"name": "x", "ci": {"conclusion": "success", "date": "2026-10-07", "gates": ["tests", "rustfmt"]}}]}
        self.assertIn("CI passed 7 Oct 2026: tests, rustfmt", rr.facts_block(base, "x"))
        base["repos"][0]["ci"].pop("gates")
        line = rr.facts_block(base, "x")
        self.assertTrue(line.endswith("CI passed 7 Oct 2026*"), line)
        text = "<!-- facts:x:start -->\n<!-- facts:x:end -->"
        self.assertEqual([f.code for f in readme_check.ci_gates_missing(text, base)], ["CI-GATES"])

    def test_committed(self):
        _, stats = load()
        by = {r["name"]: r for r in stats["repos"]}
        self.assertEqual(by["Scrapy"]["ci"]["gates"], ["tests", "ruff", "mypy", "bandit"])
        self.assertEqual(by["Rust-sitemap"]["ci"]["gates"], ["tests", "rustfmt"])
        text = read(README)
        self.assertIn("CI passed 8 Oct 2026: tests, ruff, mypy, bandit", text)
        self.assertIn("CI passed 7 Oct 2026: tests, rustfmt", text)


if __name__ == "__main__":
    unittest.main()
