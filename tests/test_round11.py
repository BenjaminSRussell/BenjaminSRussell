"""Review round 11 (docs/crit/round6/review-r11-*.md): what each fix promises, held by a test.

Working rule 4 is cut; the circuit breaker is told once, in rule 1, with its numbers; excel-and-vba is a bare link;
the image names the command (`rust_sitemap crawl`, from edition.scripts); the wheel note and the cautions come
before the code block, and the stop rule and the kill caption are apart; X2 says what a blank row means (every
answer but an HTML 200); H1's quiet includes the permit wait (60 s); the facts lines name their unit; the organizer
has one count on the page; AUDIT §7 lists the wording that is drawn.
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
from checks import audit_cover, figures as figures_check, notices as notices_check  # noqa: E402
from data import route as R  # noqa: E402
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


def ctx(cfg, stats, readme=""):
    return type("C", (), {"cfg": cfg, "stats": stats, "readme": readme})()


class RuleFourCut(unittest.TestCase):
    """r11-1 #1: three rules; "Parse, don't pattern-match." is gone from the page and from chart.toml."""

    def test_committed(self):
        cfg, stats = load()
        self.assertEqual((rr.NOTICES_ON_PAGE, notices_check.ON_PAGE), (3, 3))
        block = rr.notices_block(cfg, stats)
        self.assertEqual([r.split(".", 1)[0] for r in block.splitlines() if r.strip()], ["1", "2", "3"])
        self.assertNotIn("Parse, don't pattern-match", read(README))
        self.assertFalse(any(n["n"] == 4 for n in cfg["notices"]))
        self.assertFalse(any(r["key"] == "urlparse" for r in stats["rules"]))
        self.assertNotIn("README rule 4", audit_figures.block(cfg, stats))


class BreakerOnce(unittest.TestCase):
    """r11-1 #2: the breaker is said in one block of the visible prose, rule 1, and its numbers are checked there."""

    @staticmethod
    def blocks(readme):
        text = audit_cover.visible(readme)
        out = []
        for para in re.split(r"\n\s*\n", text):
            out += [b for b in re.split(r"\n(?=\s*- )", para) if b.strip()]
        return out

    def test_committed(self):
        hits = [b for b in self.blocks(read(README)) if re.search(r"circuit breaker|left alone", b, re.I)]
        self.assertEqual(len(hits), 1, hits)
        self.assertIn("Boring under load.", hits[0])
        self.assertIn("When 5 URLs in a row on one host fail every retry, that host is left alone for 60", hits[0])
        self.assertIn("- Prometheus metrics on Grafana dashboards. Docker Compose and a Helm chart for Kubernetes.",
                      read(README))

    def test_the_check_reads_the_rules(self):
        cfg, stats = load()
        self.assertEqual([f for f in figures_check.check(ctx(cfg, stats, read(README)))], [])
        nts = copy.deepcopy(cfg["notices"])
        nts[0]["body"] = "When 7 URLs on one host fail every retry, that host is left alone for 60 s."
        bad = figures_check.check(ctx(dict(cfg, notices=nts), stats, read(README)))
        msgs = " ".join(f.msg for f in bad)
        self.assertIn("'7'", msgs, "a typed number in a rule needs a row")
        self.assertIn("'5 URLs in a row on one host' is marked for the working rules", msgs, "a notices row must be printed")


class BareLink(unittest.TestCase):
    """r11-1 #3: excel-and-vba on the bare Also line; the count stays 15."""

    def test_committed(self):
        text = read(README)
        details = text.split('<a name="also"></a>', 1)[1].split("<details>", 1)[1].split("</details>", 1)[0]
        bare = next(ln for ln in details.splitlines() if ln.startswith("- Also: "))
        self.assertIn("[excel-and-vba](https://github.com/BenjaminSRussell/excel-and-vba)", bare)
        self.assertNotIn("spreadsheet automation", text)
        described = [ln for ln in details.splitlines() if ln.startswith("- [**")]
        self.assertEqual((len(described), len(re.findall(r"\]\(", bare))), (10, 5))
        self.assertIn("<!-- n:more_count -->15<!-- /n -->", text)


class CommandInImage(unittest.TestCase):
    """r11-2 #1: S1 names the command the release ships, in the mono face; without the probe, the old words."""

    def test_drawn(self):
        cfg, stats = load()
        s1 = next(e for e in sheet.plan(stats, cfg)["steps"] if e["id"] == "S1")
        self.assertEqual(s1["text"], "`rust_sitemap crawl` starts from your URL; by default also from sitemaps, "
                                     "certificate logs and Common Crawl")
        s = copy.deepcopy(stats)
        s["edition"]["scripts"] = ["rust_sitemap", "rustmapper"]
        s1 = next(e for e in sheet.plan(s, cfg)["steps"] if e["id"] == "S1")
        self.assertTrue(s1["text"].startswith("`rustmapper crawl` starts"), "P4: the word follows the release")

    def test_without_the_probe(self):
        cfg, stats = load()
        rc = copy.deepcopy(stats["runcheck"]["rustmapper"])
        next(st for st in rc["steps"] if st["id"] == "crawl_help")["ok"] = False
        s1 = {e["id"]: e for e in R.resolve(stats["routes"]["rustmapper"], rc)}["S1"]
        self.assertEqual(s1["text"], "starts from your URL; by default also from sitemaps, certificate logs and "
                                     "Common Crawl")
        self.assertEqual(s1["wording"], 2)

    def test_mono_and_height(self):
        import shutil
        import tempfile
        import build_assets
        tmp = tempfile.mkdtemp(prefix="r11-s1-")
        try:
            rep = os.path.join(tmp, "report.json")
            build_assets.main(sheets=["hero"], editions=None, out=os.path.join(tmp, "assets"), report_path=rep,
                              stats_path=STATS, cfg_path=CFG, quiet=True)
            with open(rep, encoding="utf-8") as fh:
                report = json.load(fh)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        for ed in ("hero-day", "hero-phone-day"):
            runs = [t for t in report["sheets"][ed]["text"] if t.get("key") == "routes:S1"]
            self.assertEqual([t["s"] for t in runs if t.get("role") == "machine"], ["rust_sitemap", "crawl"], ed)
        # review r11-2 #1's sizes: phone 1,121 (gate 1,246), desk 571 (gate 620)
        self.assertLessEqual(report["sheets"]["hero-phone-day"]["h"], 1246)
        self.assertLessEqual(report["sheets"]["hero-day"]["h"], 620)


class InstallOrder(unittest.TestCase):
    """r11-2 #2 and #3: the conditions before the commands; the stop rule and the kill caption apart."""

    def test_order(self):
        body = install(read(README)).strip()
        paras = [p.strip() for p in body.split("\n\n")]
        self.assertTrue(paras[0].startswith("Prebuilt for"), paras[0])
        self.assertEqual(paras[1], "Before you run 0.1.3:")
        self.assertTrue(body.startswith("Prebuilt for") and body.endswith("```"), body[-60:])
        self.assertLess(body.index("- It sends requests"), body.index("```sh"))

    def test_blank_line(self):
        cfg, stats = load()
        code = rr.install_block(stats, "Rust-sitemap", cfg).split("```")[1].splitlines()
        at = code.index("# sitemap.xml, even after a kill")
        self.assertEqual((code[at - 2], code[at - 1], code[at + 1]),
                         ("# for 60 s, then Ctrl-C once", "", "rust_sitemap export-sitemap"))
        # no stop lines (a release that exits by itself): no blank line opens the comments
        self.assertEqual(rr.stop_lines({"steps": [{"id": "kill_writes_file", "ok": False},
                                                  {"id": "export_after_kill", "ok": True}]},
                                       {"export_after_kill": {"ok": True, "values": {}}}),
                         ["# sitemap.xml, even after a kill"])


class BlankRows(unittest.TestCase):
    """r11-3 #1: X2 says every answer but an HTML 200 is blank; it rests on the error handler and the HTML gate."""

    def test_anchor_goes(self):
        cfg, _ = load()
        spec = {"repo": "x", "entry": [entry(cfg, "X2")]}
        body = ("async fn process_url_streaming(&self) { match f { Ok(response) if response.status().as_u16() == 200 => { "
                "if url_utils::is_html_content_type(ct) {} } "
                "Ok(_) => { return CrawlResult { result: Ok(Vec::new()) }; } } }\nlet n = SitemapNode { status_code: job.status_code };"
                "\nfn handle_crawl_error(&self) { let b = false // Don't block host for transient errors\n; }")
        ok = R.verify_route(spec, None, tree({"src/bfs_crawler.rs": body, "src/frontier.rs": ""}), None, "0.1.3")
        self.assertTrue(ok["entries"][0]["verified_release"])
        gone = body.replace("// Don't block host for transient errors", "// requeue")
        bad = R.verify_route(spec, None, tree({"src/bfs_crawler.rs": gone, "src/frontier.rs": ""}), None, "0.1.3")
        self.assertFalse(bad["entries"][0]["verified_release"], "a release that requeues transient errors")

    def test_fixture(self):
        index = read(os.path.join(ROOT, "tests", "fixtures", "status-site", "index.html"))
        for href in ("busy.html", "gone.html", "err", "feed", "hang.html"):
            self.assertIn(f'href="{href}"', index)
        import runcheck
        self.assertGreater(runcheck.STATUS_HOLD, runcheck.STATUS_TIMEOUT)
        self.assertEqual(runcheck.NON200_PAGES, ("busy.html", "gone.html", "err", "feed", "hang.html"))


class PermitWait(unittest.TestCase):
    """r11-3 #2: the quiet includes the wait for a network permit, read from the release."""

    def test_value(self):
        src = "let p = tokio::time::timeout(Duration::from_secs(30), network_permits.acquire_owned()).await;"
        self.assertEqual(R.wait_value(src, "network_permits.acquire_owned()"), "30")
        self.assertIsNone(R.wait_value("network_permits.acquire_owned().await", "network_permits.acquire_owned()"))

    def test_committed(self):
        cfg, stats = load()
        h1 = {e["id"]: e for e in R.drawn(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"])}["H1"]
        self.assertEqual(h1["quiet"], 60)
        anchor = {"path": "src/bfs_crawler.rs", "fn": "process_url_streaming", "wait": "network_permits.acquire_owned()"}
        self.assertIn(anchor, entry(cfg, "H1")["release"])
        self.assertIn("# for 60 s, then Ctrl-C once", read(README))
        step = next(s for s in stats["runcheck"]["rustmapper"]["steps"] if s["id"] == "quiet_slow_page")
        self.assertGreaterEqual(step["quiet_secs"], 60)

    def test_without_the_anchor(self):
        cfg, _ = load()
        files = {
            "src/bfs_crawler.rs": ('pub async fn start_crawling(&self) { loop { tokio::select! { else => { eprintln!("Crawl '
                                   'complete: frontier empty"); } } eprintln!("Crawler: Received work item: {}", u); } }'),
            "src/cli.rs": 'Crawl {\n #[arg(short, long, default_value = "20", help = "t")]\n timeout: u64,\n}',
            "src/network.rs": "let client = Client::builder().timeout(Duration::from_secs(timeout_secs));",
            "src/state.rs": ("impl HostState { pub const MAX_FAILURES_THRESHOLD: u32 = 3;\n"
                             "pub fn is_permanently_failed(&self) -> bool { self.failures >= Self::MAX_FAILURES_THRESHOLD }\n"
                             "pub fn record_failure(&mut self) { let b = (2_u32.pow(self.failures.min(8))).min(300); } }"),
            "src/main.rs": "crawler.initialize(&seeding_strategy).await?;\nshard.process_incoming_urls(&d).await;"}
        r = R.verify_route({"repo": "x", "entry": [entry(cfg, "H1")]}, None, tree(files), None, "0.1.3")
        rc = {"version": "0.1.3", "ok": True, "steps": [{"id": "crawl_ctrl_c", "ok": True},
                                                        {"id": "ends_by_itself", "ok": False},
                                                        {"id": "quiet_after_last_page", "ok": True},
                                                        {"id": "quiet_slow_page", "ok": True}]}
        self.assertEqual(R.resolve(r, rc)[0]["text"], "{release} never exits by itself, even after the last page",
                         "no permit anchor: no number, never a guessed one")


class TestUnit(unittest.TestCase):
    """r11-3 #3: the facts lines say what they count."""

    def test_committed(self):
        text = read(README)
        self.assertIn("· 176 test functions ·", text)
        self.assertIn("· 1,920 test functions (CI selects all but 41) ·", text)
        self.assertNotRegex(text, r"\d tests\b")


class OneCount(unittest.TestCase):
    """r11-3 #4: the organizer's sorts are counted once, 21, on the page and in the image."""

    def test_committed(self):
        cfg, stats = load()
        self.assertFalse(any(f["text"] in ("25 ways", "4 more", "21 from") for f in cfg["figures"]))
        line = next(ln for ln in read(README).splitlines() if "**ideal-url-organizer**" in ln)
        self.assertIn("— 21 ways to sort a pile of URLs from their crawl records (domain, crawl depth, subdomain, …).",
                      line)
        self.assertEqual(next(f for f in stats["figures"] if f.get("handoff"))["measured"], 21)
        self.assertIn("sorted 21 ways", audit_figures.block(cfg, stats))


class DrawnRegister(unittest.TestCase):
    """r11-3 #5: AUDIT §7 lists the wording the build drew."""

    def test_rows(self):
        cfg, stats = load()
        rows = {r["entry"]: r for r in audit_figures.route_rows(cfg, stats)}
        self.assertEqual(rows["F1"]["printed"], "`{field:max_inflight}`")
        self.assertIn("drawn instead when", rows["F1"]["definition"])
        self.assertIn("THROTTLE_THRESHOLD_MS", rows["F1"]["definition"])
        self.assertNotIn("W1", rows)
        self.assertNotIn("M1", rows, "retired: nothing printed")
        loose = {r["entry"]: r for r in audit_figures.route_rows(cfg)}
        self.assertIn("{const:THROTTLE_THRESHOLD_MS}", loose["F1"]["printed"], "with no stats, every wording")
        # review round 13: no W1 wording prints a figure now (the "every 50 ms" one is gone)
        self.assertNotIn("W1", loose)
        self.assertIn("X1", loose)

    def test_register_follows_the_stats(self):
        cfg, stats = load()
        text = read(os.path.join(ROOT, "docs", "data", "AUDIT.md"))
        self.assertEqual(audit_figures.render(text, cfg, stats), text)
        self.assertIn("| image F1 | `{field:max_inflight}` |", text)


if __name__ == "__main__":
    unittest.main()
