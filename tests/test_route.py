"""The hero, round 6 (docs/crit/round6/SPEC.md §7): the way into rustmapper.

The data half (scripts/data/route.py): anchors at HEAD and in the release, "true in both", the command the wheel
installs, the platform note, the hand-offs proved from the reading side. The sheet half (scripts/sheets/route.py):
four editions, nothing with a data-driven size, one <g id> per element and a PURPOSE row for each, no theme words,
the alt from the route, budgets, floors, determinism, and the live-like stats file.
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

import build_assets  # noqa: E402
import render_readme as rr  # noqa: E402
import tokens  # noqa: E402
from checks import route as route_check  # noqa: E402
from data import route as R  # noqa: E402
from sheets import route as sheet  # noqa: E402

STATS = os.path.join(ROOT, "assets", "stats.json")
CFG = os.path.join(ROOT, "chart.toml")
LIVE = os.environ.get("HERO_LIVE_STATS",
                      "/tmp/claude-0/-home-user-BenjaminSRussell/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/v92/live-stats.json")
EDITIONS = ("day", "night", "mid-day", "mid-night", "phone-day", "phone-night")


def scale_of(e: str) -> str:
    """Review round 12: "phone-day" -> phone, "mid-night" -> mid, "day" -> desk."""
    return "phone" if "phone" in e else ("mid" if e.startswith("mid") else "desk")
SHAPES = re.compile(r"<(rect|circle|path|line|polygon)\b([^>]*)/?>")


def load_cfg() -> dict:
    with open(CFG, "rb") as fh:
        return tomllib.load(fh)


def tree(files: dict[str, str]):
    """A fixture tree: path -> text; the reader returns None for a missing file."""
    return lambda path: files.get(path)


def all_verified(stats: dict) -> dict:
    """The committed stats with every route entry's HEAD anchors holding (what the sheet draws once P1 lands). The
    run-check probes stay as measured. Review round 8: the release's anchors stay as read (the release is what pip
    installs; P1 lands on main), so a wording that waits on a new release (F1's governor) stays undrawn."""
    s = copy.deepcopy(stats)
    for e in s["routes"]["rustmapper"]["entries"]:
        rel_missing = [m for m in e.get("missing") or [] if not m.startswith("head")]
        e.update(verified_head=True, verified_release=not rel_missing, missing=rel_missing)
    return s


def _build(tmp, tag, stats_path=STATS, editions=None):
    out = os.path.join(tmp, tag)
    rep = os.path.join(tmp, f"{tag}.json")
    n = build_assets.main(sheets=["hero"], editions=editions, out=out, report_path=rep, stats_path=stats_path,
                          cfg_path=CFG, quiet=True)
    with open(rep, encoding="utf-8") as fh:
        return n, json.load(fh), out


def _write(tmp, data, tag):
    p = os.path.join(tmp, f"{tag}.stats.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    return p


# ================================================================ the data half

class Anchors(unittest.TestCase):
    SPEC = {"repo": "Rust-sitemap", "header": "h", "entry": [
        {"id": "S1", "kind": "stop", "file": "a.rs", "text": "one",
         "head": [{"path": "src/a.rs", "text": "fn a"}], "release": [{"path": "src/a.rs"}]},
        {"id": "H1", "kind": "trap", "text": "two",
         "head": [{"path": "src/cli.rs", "absent": "max_depth"}], "release": [{"path": "src/cli.rs", "absent": "max_depth"}]},
    ]}

    def test_anchor_missing_file_text_and_absent(self):          # T-ANCHOR
        head = tree({"src/a.rs": "pub fn b() {}", "src/cli.rs": "max_depth: u32"})
        rel = tree({"src/cli.rs": "fn main() {}"})
        r = R.verify_route(self.SPEC, head, rel, "abc", "0.1.3")
        s1, h1 = r["entries"]
        self.assertFalse(s1["verified_head"])
        self.assertIn("head src/a.rs: no 'fn a'", s1["missing"])
        self.assertFalse(s1["verified_release"])
        self.assertIn("release src/a.rs: file missing", s1["missing"])
        self.assertFalse(h1["verified_head"])
        self.assertIn("head src/cli.rs: contains 'max_depth'", h1["missing"])
        self.assertTrue(h1["verified_release"])
        self.assertEqual(R.drawn(r), [])

    def test_true_in_both_or_not_drawn(self):                     # T-BOTH: the crt.sh hazard of concept A
        spec = {"repo": "x", "entry": [{"id": "H9", "kind": "trap", "text": "crt.sh may stall it",
                                        "head": [{"path": "src/cli.rs", "text": 'default_value = "all"'}],
                                        "release": [{"path": "src/cli.rs", "text": 'default_value = "all"'}]}]}
        r = R.verify_route(spec, tree({"src/cli.rs": 'default_value = "none"'}),
                           tree({"src/cli.rs": 'default_value = "all"'}), "abc", "0.1.3")
        e = r["entries"][0]
        self.assertFalse(e["verified_head"])
        self.assertTrue(e["verified_release"])
        self.assertEqual(R.drawn(r), [])
        self.assertEqual([x["id"] for x in R.unverified(r)], ["H9"])

    def test_no_tree_verifies_nothing(self):
        r = R.verify_route(self.SPEC, None, None, None, None)
        self.assertEqual(R.drawn(r), [])
        self.assertTrue(all(e["missing"] for e in r["entries"]))

    def test_committed_route_names_the_p1_test(self):
        with open(STATS, encoding="utf-8") as fh:
            stats = json.load(fh)
        route = stats["routes"]["rustmapper"]
        by = {e["id"]: e for e in route["entries"]}
        self.assertEqual([e["id"] for e in route["entries"]],
                         ["S1", "S2", "F1", "W1", "H1", "C1", "R13", "L1", "L4", "L2", "L5", "L3", "X3", "X2", "X1",
                      "M1"])
        # r7: G1 in F1; r8: L2, L3; r9: L4 (the robots clause, its own item), X2 (what the file cannot say)
        if not by["S2"]["verified_head"]:
            self.assertIn("head tests/robots_4xx_allows_crawl.rs: file missing", by["S2"]["missing"])
        rc = stats["runcheck"]["rustmapper"]
        drawn = {e["id"]: e for e in R.drawn(route, rc)}
        for gid in ("S1", "F1", "W1", "H1", "C1", "R13", "L1", "L4", "L2", "L3", "X1", "X2"):
            self.assertIn(gid, drawn, [e for e in R.unverified(route, rc) if e["id"] == gid])
        # review round 6: main's idle test runs with --ignore-robots, so M1 is retired (not printed, not unverified)
        m1 = next(e for e in R.resolve(route, rc) if e["id"] == "M1")
        self.assertTrue(m1["verified"] and m1["retired"], m1)
        self.assertEqual(m1.get("gate"), "cargo")
        # review round 6: L1 says what 0.1.3 does with robots.txt, on the probe that watched it (robots_read failed)
        # review round 9: that clause is L4, its own item
        self.assertIn("ignores `Crawl-delay`, and asks for `robots.txt` only over https", drawn["L4"]["text"])
        self.assertNotIn("unless", drawn["L1"]["text"])
        self.assertEqual(drawn["L4"]["fails"], ["robots_read"])
        # the release's words: seeds by default, never ends by itself, a kill writes nothing (run check, 0.1.3)
        self.assertIn("by default", drawn["S1"]["text"])
        # review round 3: H1 states its cause (no exit once the pages run out), not the crawl's scope; review round 4:
        # with the line of output that says the crawl is done, while the run check saw it go quiet
        # review round 5: the hazard names its release (the sheet fills {release} from edition.version)
        # review round 7: "exits", not "stops": the crawl stops, the process does not exit
        # review round 9: the clearing mark with its number (computed, quiet_secs; probe quiet_slow_page)
        self.assertEqual(drawn["H1"]["text"], "{release} never exits by itself; done when `Received work item` lines stop for 60 s")
        # review round 5: the image keeps one command; what to do after a kill is a comment in the README's block
        # review round 8: with its caution and the line that says it is done (probe second_ctrl_c passed)
        self.assertEqual(drawn["C1"]["text"],
                         "press Ctrl-C once; a second press before the `Saved to` line quits without writing the file")
        # review round 6: the scope in a visitor's words, not the code's ("above or below")
        # review round 8: F1 says the per-host cap; 0.1.3's governor stops at 32 idle permits and never slows a site
        self.assertEqual(drawn["F1"]["text"], "fetches up to 20 pages at a time from each host; queues their "
                                              "links to your site, its subdomains and its parent domain")
        self.assertEqual(drawn["F1"]["scope"], "release")
        # review round 9: a verb; round 11: after the command it names
        self.assertTrue(drawn["S1"]["text"].startswith("`{script} crawl` starts from your URL; "))
        # review round 7: the write path in its order, in batches: 50 ms is drain_batch's wait for the first event
        # review round 13: the row says what that buys (export-sitemap after a kill), on the probes that showed it
        self.assertEqual(drawn["W1"]["text"], "saved as it goes; export works after a kill")
        self.assertEqual((drawn["W1"]["runs"], drawn["W1"]["fails"]), (["export_after_kill"], ["kill_writes_file"]))
        self.assertEqual(m1["ci"], "Test")
        self.assertNotIn("keeps the crawl", drawn["W1"]["text"], "a kill writes no file and resume fails (r13-3 #3)")
        self.assertNotIn("resume", " ".join(e["text"] for e in drawn.values()))


class Probes(unittest.TestCase):
    """Round 6, review 1: an entry rests on running the tool, not only on finding strings."""
    SPEC = {"repo": "x", "entry": [
        {"id": "H1", "kind": "trap", "scope": "release", "text": "never ends by itself",
         "release": [{"path": "src/cli.rs", "absent": "max_urls"}], "fails": ["ends_by_itself"],
         "instead": [{"text": "stop it with --max-urls N", "release": [{"path": "src/cli.rs", "text": "max_urls"}]},
                     {"text": "a 3-page crawl ended in {secs:ends_by_itself} s", "release": [{"path": "src/cli.rs"}],
                      "runs": ["ends_by_itself"]}]},
        {"id": "W1", "kind": "stop", "text": "export after a kill", "head": [{"path": "src/wal.rs"}],
         "release": [{"path": "src/wal.rs"}], "runs": ["export_after_kill"]},
    ]}

    @staticmethod
    def rc(**probes):
        return {"version": "0.1.3", "ok": True,
                "steps": [{"id": k, "ok": v, "gate": False, "secs": 91.4} for k, v in probes.items()]}

    def route(self, cli="fn main() {}"):
        files = {"src/cli.rs": cli, "src/wal.rs": "wal"}
        return R.verify_route(self.SPEC, tree(files), tree(files), "abc", "0.1.3")

    def test_release_scope_needs_no_head(self):
        e = self.route()["entries"][0]
        self.assertTrue(e["verified_head"] and e["verified_release"])
        self.assertEqual(e["scope"], "release")

    def test_probe_picks_the_words(self):
        r = self.route()
        by = {e["id"]: e for e in R.resolve(r, self.rc(ends_by_itself=False, export_after_kill=True))}
        self.assertEqual(by["H1"]["text"], "never ends by itself")
        self.assertTrue(by["W1"]["verified"])
        by = {e["id"]: e for e in R.resolve(r, self.rc(ends_by_itself=True, export_after_kill=True))}
        self.assertEqual(by["H1"]["text"], "a 3-page crawl ended in 91 s")
        by = {e["id"]: e for e in R.resolve(self.route("max_urls: Option<usize>"), self.rc(ends_by_itself=False))}
        self.assertEqual(by["H1"]["text"], "stop it with --max-urls N")

    def test_a_failed_probe_is_not_drawn(self):
        r = self.route()
        un = {e["id"]: e for e in R.unverified(r, self.rc(ends_by_itself=False, export_after_kill=False))}
        self.assertIn("W1", un)
        self.assertIn("export_after_kill failed", " ".join(un["W1"]["missing"]))
        self.assertEqual([e["id"] for e in R.unverified(r, None)], ["H1", "W1"])     # no run check: nothing rests on faith
        other = dict(self.rc(ends_by_itself=False, export_after_kill=True), version="0.1.2")
        self.assertEqual([e["id"] for e in R.unverified(r, other)], ["H1", "W1"])    # a run of another release

    def test_runcheck_gate_ignores_probes(self):
        import runcheck
        steps = []
        runcheck._step(steps, "install", "pip install", True, secs=180.0)
        runcheck._step(steps, "ends_by_itself", "crawl alone", False, gate=False)
        self.assertEqual(steps[0]["secs"], 180.0)
        self.assertFalse(steps[1]["gate"])

    def test_install_detail_names_cache_toolchain_and_spread(self):
        import runcheck
        self.assertEqual(runcheck.median([3.0, 1.0, 2.0]), 2.0)
        d = runcheck.install_detail("sdist (built with Rust)", "1.97.0", 4, [250.0, 240.5, 262.1], "ok")
        self.assertIn("cache cold", d)
        self.assertIn("rustc 1.97.0", d)
        self.assertIn("4 CPUs", d)
        self.assertIn("3 runs: median 250.0 s, range 240.5-262.1 s", d)


class Quiet(unittest.TestCase):
    """Review round 4: H1 says when the crawl is done, from its own output, only while the run check saw it go quiet."""

    def test_quiet_verdict(self):
        import runcheck
        stamps = [(10.0, "http://127.0.0.1:1/"), (10.2, "http://127.0.0.1:1/a.html"), (10.3, "http://127.0.0.1:1/b.html")]
        ok, detail = runcheck.quiet_verdict(stamps, 160.0, 3)
        self.assertTrue(ok, detail)
        self.assertIn("3 work-item lines for 3 URLs, the last 150 s before the SIGINT; 3 lines in sitemap.jsonl", detail)
        self.assertFalse(runcheck.quiet_verdict(stamps, 60.0, 3)[0], "under 100 s of quiet")
        self.assertFalse(runcheck.quiet_verdict(stamps, 160.0, 2)[0], "a URL started but not written")
        self.assertFalse(runcheck.quiet_verdict(stamps, None, 3)[0], "it ended by itself: no SIGINT")
        self.assertFalse(runcheck.quiet_verdict([], 160.0, 0)[0])
        self.assertTrue(runcheck.WORK_ITEM.search("Crawler: Received work item: http://x/ (depth 0)"))

    QUIET_FILES = {
        "src/cli.rs": 'Crawl {\n #[arg(short, long, default_value = "20", help = "t")]\n timeout: u64,\n}',
        "src/network.rs": "let client = Client::builder().timeout(Duration::from_secs(timeout_secs));",
        # review round 10: every seeder runs before the first shard worker takes a URL
        "src/main.rs": "crawler.initialize(&seeding_strategy).await?;\nshard.process_incoming_urls(&d).await;",
        "src/state.rs": ("impl HostState { pub const MAX_FAILURES_THRESHOLD: u32 = 3;\n"
                         "pub fn is_permanently_failed(&self) -> bool { self.failures >= Self::MAX_FAILURES_THRESHOLD }\n"
                         "pub fn record_failure(&mut self) { let b = (2_u32.pow(self.failures.min(8))).min(300); } }")}

    def test_h1_takes_the_quiet_words_only_on_the_probe(self):
        spec = {"repo": "x", "entry": [e for e in load_cfg()["route"]["rustmapper"]["entry"] if e["id"] == "H1"]}
        body = ('pub async fn start_crawling(&self) { loop { tokio::select! { else => { eprintln!("Crawl complete: '
                'frontier empty"); } } eprintln!("Crawler: Received work item: {}", u); } }'
                # review round 11: the line is printed before the task waits up to 30 s for a network permit
                ' async fn process_url_streaming(&self) { let _p = tokio::time::timeout(Duration::from_secs(30), '
                'network_permits.acquire_owned()).await; }')
        r = R.verify_route(spec, None, tree({"src/bfs_crawler.rs": body, **self.QUIET_FILES}), None, "0.1.3")

        def words(**probes):
            rc = {"version": "0.1.3", "ok": True, "steps": [{"id": k, "ok": v} for k, v in probes.items()]}
            return {e["id"]: e for e in R.resolve(r, rc)}["H1"]
        # review round 9: the clearing mark with its number, on both quiet probes
        self.assertEqual(words(crawl_ctrl_c=True, ends_by_itself=False, quiet_after_last_page=True,
                               quiet_slow_page=True)["text"],
                         "{release} never exits by itself; done when `Received work item` lines stop for 60 s")
        self.assertEqual(words(crawl_ctrl_c=True, ends_by_itself=False, quiet_after_last_page=True)["text"],
                         "{release} never exits by itself, even after the last page", "no slow-page probe: no number")
        self.assertEqual(words(crawl_ctrl_c=True, ends_by_itself=False, quiet_after_last_page=False,
                               quiet_slow_page=True)["text"],
                         "{release} never exits by itself, even after the last page")
        self.assertEqual(words(crawl_ctrl_c=True, ends_by_itself=False)["text"],
                         "{release} never exits by itself, even after the last page", "no quiet probe recorded: the cause alone")
        self.assertTrue(words(crawl_ctrl_c=True, ends_by_itself=True, quiet_after_last_page=False)["retired"])
        # a release that no longer prints the line: the quiet wording's anchor fails, the cause alone is drawn
        r = R.verify_route(spec, None, tree({"src/bfs_crawler.rs": body.replace("Received work item", "item"),
                                             **self.QUIET_FILES}), None, "0.1.3")
        rc = {"version": "0.1.3", "ok": True, "steps": [{"id": "crawl_ctrl_c", "ok": True},
                                                        {"id": "ends_by_itself", "ok": False},
                                                        {"id": "quiet_after_last_page", "ok": True},
                                                        {"id": "quiet_slow_page", "ok": True}]}
        self.assertEqual({e["id"]: e for e in R.resolve(r, rc)}["H1"]["text"],
                         "{release} never exits by itself, even after the last page")


class StringDefaults(unittest.TestCase):
    """Review round 4: a clap default that is a path, narrowed to one subcommand, prints as the file's name."""
    CLI = ('Crawl {\n #[arg(short, long, default_value = "./data", help = "d")]\n data_dir: String,\n},\n'
           'ExportSitemap {\n #[arg(short, long, default_value = "./out", help = "d")]\n data_dir: String,\n'
           ' #[arg(short, long, default_value = "./sitemap.xml", help = "o")]\n output: String,\n}')

    def test_block_and_string_arg(self):
        self.assertEqual(R.arg_value(self.CLI, "output"), "./sitemap.xml")
        self.assertEqual(R.block_body(self.CLI, "ExportSitemap").count("default_value"), 2)
        spec = {"repo": "x", "entry": [{"id": "C1", "kind": "step", "text": "export writes `{arg:output}`",
                                        "head": [{"path": "c.rs", "block": "ExportSitemap", "arg": "output"}],
                                        "release": [{"path": "c.rs", "block": "ExportSitemap", "arg": "output"}]}],
                "release_gates": {"export_defaults": [
                    {"path": "c.rs", "block": "ExportSitemap", "arg": "data_dir", "equals": "./data"}]}}
        r = R.verify_route(spec, tree({"c.rs": self.CLI}), tree({"c.rs": self.CLI}), "abc", "0.1.3")
        self.assertEqual(r["entries"][0]["text"], "export writes `sitemap.xml`")
        g = r["gates"]["export_defaults"]
        self.assertFalse(g["ok"], "ExportSitemap's data_dir is ./out here, not Crawl's ./data")
        self.assertIn("release c.rs ExportSitemap: arg data_dir is ./out, not ./data", g["missing"])
        self.assertIn("no Missing", R.check_anchor(tree({"c.rs": self.CLI}), {"path": "c.rs", "block": "Missing", "arg": "x"}))

    def test_release_gate_without_sdist_fails(self):
        r = R.verify_route({"repo": "x", "entry": [], "release_gates": {"no_services": [{"path": "c.rs"}]}},
                           None, None, None, None)
        self.assertFalse(r["gates"]["no_services"]["ok"])

    def test_committed_gates_hold(self):
        with open(STATS, encoding="utf-8") as fh:
            g = json.load(fh)["routes"]["rustmapper"]["gates"]
        self.assertTrue(g["export_defaults"]["ok"], g["export_defaults"])
        self.assertTrue(g["no_services"]["ok"], g["no_services"])


class HandoffVerb(unittest.TestCase):
    """Review round 4: the arrow past the end says what the next project does with the file, from its reader."""
    SPEC = {"id": "j", "kind": "fields", "from": "a", "to": "b", "file": "data/sitemap.jsonl", "writer": "s.rs",
            "writer_struct": "N", "reader": "r.py", "reader_list": "F", "test": "t.py",
            "does": {"verb": "sorted by", "text": ["run.sh", "--all"]}}

    def state(self, reader):
        w = tree({"s.rs": "pub struct N {\n pub url: String,\n}"})
        return R.handoff_state(self.SPEC, w, w, tree({"r.py": reader, "t.py": ""}), None, "1" * 40, "2" * 40, "0.1.3")

    def test_verb_from_the_reader(self):
        self.assertEqual(self.state('F = ["url"]\nsubprocess.run(["./run.sh", "--all"])')["does"], "sorted by")
        h = self.state('F = ["url"]\n')
        self.assertEqual(h["state"], "runs")
        self.assertIsNone(h["does"])

    def test_committed_handoff_is_sorted(self):
        with open(STATS, encoding="utf-8") as fh:
            h = next(x for x in json.load(fh)["handoffs"] if x["state"] == "runs")
        self.assertEqual(h["does"], "sorted by")


class Constants(unittest.TestCase):
    """Round 6, review 2: W1's figure is the writer's constant, read from the code, not typed."""
    SPEC = {"repo": "x", "entry": [
        {"id": "W1", "kind": "stop", "file": "writer_thread.rs", "text": "saved every {const:BATCH_TIMEOUT_MS} ms",
         "head": [{"path": "src/writer_thread.rs", "const": "BATCH_TIMEOUT_MS"},
                  {"path": "src/export.rs", "fn": "run_export", "absent": "WalReader"}],
         "release": [{"path": "src/writer_thread.rs", "const": "BATCH_TIMEOUT_MS"},
                     {"path": "src/main.rs", "fn": "run_export", "text": "CrawlerState::new"},
                     {"path": "src/main.rs", "fn": "run_export", "absent": "WalReader"}]}]}
    MAIN = ("fn build() { let r = WalReader::new(d); }\n"
            "async fn run_export(d: String) -> Result<(), E> {\n    let s = CrawlerState::new(&d)?;\n    { inner(); }\n}\n")

    def route(self, head_ms="50", rel_ms="50", main=MAIN):
        head = tree({"src/writer_thread.rs": f"const BATCH_TIMEOUT_MS: u64 = {head_ms}; // drain",
                     "src/export.rs": "pub async fn run_export(d: String) { let s = CrawlerState::new(&d); }"})
        rel = tree({"src/writer_thread.rs": f"const BATCH_TIMEOUT_MS: u64 = {rel_ms};", "src/main.rs": main})
        return R.verify_route(self.SPEC, head, rel, "abc", "0.1.3")["entries"][0]

    def test_anchor_const_prints_the_code_value(self):            # T-ANCHOR, const
        self.assertEqual(self.route()["text"], "saved every 50 ms")
        e = self.route("75", "75")
        self.assertEqual(e["text"], "saved every 75 ms")
        self.assertTrue(e["verified_head"] and e["verified_release"])

    def test_const_differs_between_trees(self):
        e = self.route("75", "50")
        self.assertFalse(e["verified_head"])
        self.assertIn("head BATCH_TIMEOUT_MS = 75, release BATCH_TIMEOUT_MS = 50: the figure differs", e["missing"])

    def test_fn_narrows_to_the_body(self):                       # T-ANCHOR, fn
        self.assertTrue(self.route()["verified_release"])          # WalReader is in build(), not in run_export()
        e = self.route(main=self.MAIN.replace("CrawlerState::new(&d)?", "WalReader::new(&d)?"))
        self.assertFalse(e["verified_release"])
        self.assertTrue(any("fn run_export" in m for m in e["missing"]), e["missing"])
        e = self.route(main="fn other() {}")
        self.assertTrue(any("no fn run_export" in m for m in e["missing"]), e["missing"])

    def test_label_only_when_the_file_is_anchored_in_both(self):  # ROUTE-LABEL
        self.assertEqual(self.route()["file"], "writer_thread.rs")  # anchored in both trees
        spec = {"repo": "x", "entry": [
            {"id": "G1", "kind": "note", "file": "governor.rs", "text": "slows",
             "head": [{"path": "src/orchestration/governor.rs"}], "release": [{"path": "src/main.rs"}]},
            {"id": "F1", "kind": "stop", "file": "bfs_crawler.rs", "text": "fetch",
             "head": [{"path": "src/bfs_crawler.rs"}], "release": [{"path": "src/bfs_crawler.rs"}]},
            {"id": "S1", "kind": "stop", "scope": "release", "file": "seeder.rs", "text": "seeds",
             "release": [{"path": "src/seeder.rs"}]}]}
        files = {"src/orchestration/governor.rs": "", "src/main.rs": "", "src/bfs_crawler.rs": "", "src/seeder.rs": ""}
        r = R.verify_route(spec, tree(files), tree(files), "abc", "0.1.3")
        by = {e["id"]: e for e in R.drawn(r)}
        self.assertIsNone(by["G1"]["file"])                         # 0.1.3 keeps the governor in main.rs
        self.assertEqual(by["F1"]["file"], "bfs_crawler.rs")
        self.assertEqual(by["S1"]["file"], "seeder.rs")             # release scope: the release's file
        texts = [{"s": "governor.rs", "role": "machine", "key": "routes:G1"},
                 {"s": "bfs_crawler.rs", "role": "machine", "key": "routes:F1"}]
        found = route_check.labels(r, texts, "hero-day")
        self.assertEqual([f.code for f in found], ["ROUTE-LABEL"])
        self.assertIn("governor.rs", found[0].msg)


class Commands(unittest.TestCase):
    def test_scripts(self):                                       # T-SCRIPTS
        self.assertEqual(R.command_name(["rust_sitemap"]), "rust_sitemap")
        self.assertEqual(R.command_name(["rust_sitemap", "rustmapper"]), "rustmapper")
        with self.assertRaises(RuntimeError):
            R.command_name([])
        with open(STATS, encoding="utf-8") as fh:
            stats = json.load(fh)
        cfg = load_cfg()
        for scripts, want in ((["rust_sitemap"], "rust_sitemap crawl --start-url <site>"),
                              (["rust_sitemap", "rustmapper"], "rustmapper crawl --start-url <site>")):
            s = copy.deepcopy(stats)
            s["edition"]["scripts"] = scripts
            s["runcheck"]["rustmapper"]["scripts"] = scripts
            # review round 5: the image names no command but `pip install`; the block names them as the wheel does
            for e in sheet.plan(s, cfg)["steps"]:
                self.assertNotIn("export-sitemap", e["text"], e["id"])
                self.assertNotIn("{script}", e["text"])
                self.assertNotIn("{release}", e["text"])
            block = rr.install_block(s, "Rust-sitemap", cfg)
            self.assertIn(want.split()[0] + " crawl \\\n    --start-url <your-site>", block)
            self.assertIn("# sitemap.xml, even after a kill\n" + want.split()[0] + " export-sitemap", block)
        s = copy.deepcopy(stats)
        s["edition"]["scripts"] = []
        with self.assertRaises(RuntimeError):
            sheet.plan(s, cfg)

    def test_install_block_says_how_it_ends(self):               # review round 4
        with open(STATS, encoding="utf-8") as fh:
            stats = json.load(fh)
        cfg = load_cfg()
        block = rr.install_block(stats, "Rust-sitemap", cfg)
        code = block.split("```")[1]
        self.assertEqual(code.strip().splitlines()[1:], ["pip install rustmapper", "rust_sitemap crawl \\",
                                                         "    --start-url <your-site>",
                                                         # review round 10: the stop rule where the reader acts
                                                         "# 0.1.3 runs until stopped: when",
                                                         '# "Received work item" stops',
                                                         "# for 60 s, then Ctrl-C once",
                                                         "",       # review round 11: the two comments apart
                                                         "# sitemap.xml, even after a kill",
                                                         "rust_sitemap export-sitemap"])
        self.assertTrue(all(len(ln) <= 38 for ln in code.splitlines()))
        # review round 5: the kill comment only while a kill writes no file and the export on what it left worked,
        # and the release's export reads the stored state (release gate export_after_kill)
        for sid, ok in (("kill_writes_file", True), ("export_after_kill", False)):
            s = copy.deepcopy(stats)
            for st in s["runcheck"]["rustmapper"]["steps"]:
                if st["id"] == sid:
                    st["ok"] = ok
            self.assertNotIn("after a kill", rr.install_block(s, "Rust-sitemap", cfg), sid)
        s = copy.deepcopy(stats)
        s["routes"]["rustmapper"]["gates"]["export_after_kill"] = {"ok": False, "missing": ["WalReader"]}
        self.assertNotIn("after a kill", rr.install_block(s, "Rust-sitemap", cfg))
        s = copy.deepcopy(stats)
        for st in s["runcheck"]["rustmapper"]["steps"]:
            if st["id"] == "ends_by_itself":
                st["ok"] = True
        self.assertNotIn("Ctrl-C", rr.install_block(s, "Rust-sitemap", cfg), "a crawl that ends needs no stop line")
        s = copy.deepcopy(stats)
        s["routes"]["rustmapper"]["gates"]["export_defaults"] = {"ok": False, "missing": ["changed"]}
        self.assertIn("    --data-dir ./data \\\n    --output sitemap.xml", rr.install_block(s, "Rust-sitemap", cfg),
                      "a release with other defaults gets its flags back")

    def test_wheels(self):                                        # T-WHEELS
        self.assertEqual(R.wheel_words(["cp313-cp313-macosx_11_0_arm64"]),
                         "prebuilt for macOS arm64 + Python 3.13; elsewhere pip needs Rust")
        self.assertEqual(R.wheel_words(["cp313-cp313-manylinux_2_17_x86_64", "cp313-cp313-macosx_11_0_arm64",
                                        "cp313-cp313-win_amd64"]), "")
        self.assertEqual(R.wheel_words([]), "no prebuilt wheel; pip needs Rust")

    def test_wheel_record(self):
        import io
        import zipfile
        from data import pypi
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("rustmapper-0.1.3.data/scripts/rust_sitemap", b"\x7fELF")
            z.writestr("rustmapper-0.1.3.dist-info/entry_points.txt", "[console_scripts]\nrustmapper = rustmapper:main\n")
            z.writestr("rustmapper-0.1.3.dist-info/RECORD",
                       "rustmapper-0.1.3.data/scripts/rust_sitemap,sha256=x,4\nrustmapper-0.1.3.dist-info/RECORD,,\n")
        self.assertEqual(pypi.scripts_in_wheel(buf.getvalue()), ["rust_sitemap", "rustmapper"])


class Handoffs(unittest.TestCase):
    WRITER = "pub struct SitemapNode {\n    pub url: String,\n    pub depth: u32,\n    // pub hidden: u8,\n    pub title: Option<String>,\n}\n"
    READER = 'URL_RECORD_FIELDS = [\n    "url",\n    "depth",\n]\n'
    SPEC = {"id": "j", "kind": "fields", "from": "a", "to": "b", "file": "data/sitemap.jsonl", "writer": "src/state.rs",
            "writer_struct": "SitemapNode", "reader": "scripts/r.py", "reader_list": "URL_RECORD_FIELDS",
            "test": "tests/test_r.py"}

    def state(self, writer=WRITER, reader=READER, test=True):
        w = tree({"src/state.rs": writer})
        rd = tree({"scripts/r.py": reader, **({"tests/test_r.py": "def test(): pass"} if test else {})})
        return R.handoff_state(self.SPEC, w, w, rd)

    def test_fields_states(self):                                 # T-HANDOFF
        self.assertEqual(R.struct_fields(self.WRITER, "SitemapNode"), ["url", "depth", "title"])
        self.assertEqual(self.state()["state"], "runs")
        self.assertEqual(self.state(writer=self.WRITER.replace("    pub depth: u32,\n", ""))["state"], "fields differ")
        self.assertEqual(self.state(test=False)["state"], "no test")
        with self.assertRaises(ValueError):
            self.state(reader="FIELDS = ['url']\n")
        with self.assertRaises(ValueError):
            R.struct_fields("struct Other {}", "SitemapNode")

    def test_handoff_line_drawn_only_when_it_runs(self):
        with open(STATS, encoding="utf-8") as fh:
            stats = all_verified(json.load(fh))
        cfg = load_cfg()
        self.assertIsNotNone(sheet.plan(stats, cfg)["handoff"])
        for h in stats["handoffs"]:
            if h["to"] == "ideal-url-organizer":
                h["state"] = "fields differ"
        self.assertIsNone(sheet.plan(stats, cfg)["handoff"])


class RoundThree(unittest.TestCase):
    """Review round 3: H1's cause, retirement, value anchors, the hand-off reader's label, code in the code face."""

    @staticmethod
    def h1_spec():
        spec = load_cfg()["route"]["rustmapper"]
        return {"repo": spec["repo"], "entry": [e for e in spec["entry"] if e["id"] == "H1"]}

    SELECT = ("pub async fn start_crawling(&self) -> R {\n    loop {\n        tokio::select! {\n"
              "            Some(r) = in_flight.join_next() => {}\n"
              "            else => {\n                if self.frontier.is_empty() {\n"
              "                    eprintln!(\"Crawl complete: frontier empty and no tasks in flight\");\n"
              "                    break;\n                }\n            }\n        }\n    }\n}\n")
    TIMER = SELECT.replace("else => {", "_ = idle.tick() => {")

    @staticmethod
    def rc(**probes):
        return {"version": "0.1.3", "ok": True,
                "steps": [{"id": k, "ok": v, "gate": False, "secs": 150} for k, v in probes.items()]}

    def test_h1_rests_on_the_select_else_arm(self):              # T-ANCHOR, review round 3
        rel = tree({"src/bfs_crawler.rs": self.SELECT})
        r = R.verify_route(self.h1_spec(), None, rel, None, "0.1.3")
        res = R.resolve(r, self.rc(ends_by_itself=False, crawl_ctrl_c=True))
        self.assertTrue(res[0]["verified"])
        self.assertEqual(res[0]["text"], "{release} never exits by itself, even after the last page")
        self.assertNotRegex(res[0]["text"], r"limit|depth|same-site|parent")    # no scope given as the cause
        # the completion check moved to a timer (d751cf0) while the probe still fails: H1 does not hold
        r = R.verify_route(self.h1_spec(), None, tree({"src/bfs_crawler.rs": self.TIMER}), None, "0.1.3")
        self.assertEqual([e["id"] for e in R.unverified(r, self.rc(ends_by_itself=False, crawl_ctrl_c=True))], ["H1"])

    def test_a_crawl_that_ends_retires_h1(self):
        r = R.verify_route(self.h1_spec(), None, tree({"src/bfs_crawler.rs": self.TIMER}), None, "0.1.3")
        rc = self.rc(ends_by_itself=True, crawl_ctrl_c=True)
        self.assertEqual(R.drawn(r, rc), [])
        self.assertEqual(R.unverified(r, rc), [])
        self.assertTrue(R.resolve(r, rc)[0]["retired"])

    def test_field_and_arg_anchors(self):                        # T-ANCHOR, field / arg
        spec = {"repo": "x", "entry": [{"id": "L1", "kind": "text", "scope": "release",
                                        "text": "{field:max_inflight} per host, {arg:workers} in all",
                                        "release": [{"path": "s.rs", "field": "max_inflight"},
                                                    {"path": "s.rs", "field": "crawl_delay_secs", "equals": "0"},
                                                    {"path": "c.rs", "arg": "workers"}]}]}
        cli = ('#[arg(short, long, default_value = "256", help = "n")]\n        workers: usize,\n'
               '#[arg(long, default_value = "20")]\n        timeout: u64,')
        st = "pub max_inflight: usize,\n HostState { crawl_delay_secs: 0, max_inflight: 20, }"
        e = R.verify_route(spec, None, tree({"s.rs": st, "c.rs": cli}), None, "0.1.3")["entries"][0]
        self.assertEqual(e["text"], "20 per host, 256 in all")
        self.assertTrue(e["verified_release"])
        e = R.verify_route(spec, None, tree({"s.rs": st.replace("crawl_delay_secs: 0", "crawl_delay_secs: 1"),
                                             "c.rs": cli}), None, "0.1.3")["entries"][0]
        self.assertFalse(e["verified_release"])
        self.assertIn("release s.rs: field crawl_delay_secs is 1, not 0", e["missing"])
        self.assertEqual(R.arg_value(cli, "timeout"), "20")

    def test_x1_retires_when_the_release_splits(self):
        spec = {"repo": "x", "entry": [e for e in load_cfg()["route"]["rustmapper"]["entry"] if e["id"] == "X1"]}
        head = tree({"src/sitemap_writer.rs": "pub const DEFAULT_MAX_URLS_PER_SITEMAP: usize = 50_000;"})
        one = tree({"src/main.rs": "fn run_export_sitemap_command(output: String) { SitemapWriter::new(&output); "
                                   "if node.status_code == Some(200) {} }",
                    "src/sitemap_writer.rs": "pub struct SitemapWriter {}"})
        rc = {"version": "0.1.3", "ok": True, "steps": [{"id": "sitemap_keeps_noindex", "ok": True, "gate": False}]}
        e = R.drawn(R.verify_route(spec, head, one, "abc", "0.1.3"), rc)[0]
        self.assertIn("allows 50,000 URLs per file", e["text"])
        split = tree({"src/main.rs": "SitemapIndexWriter", "src/sitemap_writer.rs": "pub struct SitemapIndexWriter {}"})
        r = R.verify_route(spec, head, split, "abc", "0.1.4")
        self.assertEqual((R.drawn(r), R.unverified(r)), ([], []))

    def test_handoff_reader_label(self):                          # ROUTE-LABEL, the hand-off's reader
        route = {"entries": []}
        texts = [{"s": "scripts/import_rust_sitemapper.py", "role": "machine", "key": "handoffs:j"}]
        ok = [{"id": "j", "reader": "scripts/import_rust_sitemapper.py", "state": "runs", "to_sha": "1" * 40}]
        self.assertEqual(route_check.labels(route, texts, "hero-day", ok), [])
        for bad in ([dict(ok[0], state="fields differ")], [dict(ok[0], to_sha=None)], [dict(ok[0], reader="x.py")], []):
            self.assertEqual([f.code for f in route_check.labels(route, texts, "hero-day", bad)], ["ROUTE-LABEL"])
        # output and field names are code but not source files: no label rule applies
        texts = [{"s": "data/sitemap.jsonl", "role": "machine", "key": "routes:C1"}]
        self.assertEqual(route_check.labels(route, texts, "hero-day", []), [])

    def test_code_face_and_self_twice(self):                      # TYPE-CODE, HERO-SELF-TWICE
        texts = [{"s": "run export-sitemap", "role": "label", "key": "routes:C1"},
                 {"s": "status_code", "role": "machine", "key": "routes:R13"}]
        self.assertEqual([f.code for f in route_check.code_face(texts, "hero-day")], ["TYPE-CODE"])
        texts = [{"s": "one line per page", "role": "label", "key": "routes:R0"},
                 {"s": "one line per page: url", "role": "label", "key": "routes:R13"}]
        self.assertEqual([f.code for f in route_check.self_twice(texts, "hero-day")], ["HERO-SELF-TWICE"])


class RoundFive(unittest.TestCase):
    """Review round 5: the write path's order, the governor's threshold, what main has fixed (M1, gated by CI)."""
    LOOP = ("fn writer_loop(x: u8) { for r in batch { if let Err(e) = wal.append(&record) {} } "
            "let f = wal.fsync(); match state.apply_event_batch(&batch) { _ => {} } }")

    def test_order_anchor(self):
        a = {"path": "w.rs", "fn": "writer_loop", "text": "wal.fsync()", "before": "state.apply_event_batch(&batch)"}
        self.assertIsNone(R.check_anchor(tree({"w.rs": self.LOOP}), a))
        swapped = ("fn writer_loop(x: u8) { match state.apply_event_batch(&batch) { _ => {} } "
                   "let f = wal.fsync(); }")
        self.assertIn("comes after", R.check_anchor(tree({"w.rs": swapped}), a))
        self.assertIn("no 'state.apply_event_batch(&batch)'",
                      R.check_anchor(tree({"w.rs": "fn writer_loop() { wal.fsync(); }"}), a))

    def test_committed_w1_rests_on_the_order_in_both_trees(self):
        w1 = next(e for e in load_cfg()["route"]["rustmapper"]["entry"] if e["id"] == "W1")
        for side in ("head", "release"):
            befores = [(a["text"], a["before"]) for a in w1[side] if "before" in a]
            self.assertEqual(len(befores), 2, side)
            self.assertTrue(befores[1][1] == "state.apply_event_batch(&batch)" and "fsync" in befores[1][0], side)
        self.assertIn("then saved to redb", w1["instead"][0]["text"])
        self.assertEqual(w1["text"], "saved as it goes; export works after a kill")   # review round 13: what it buys

    def test_threshold_prints_as_a_whole_number(self):
        spec = {"repo": "x", "entry": [{"id": "G1", "kind": "note", "scope": "release",
                                        "text": "fewer at once over {const:THROTTLE_THRESHOLD_MS} ms",
                                        "release": [{"path": "m.rs", "const": "THROTTLE_THRESHOLD_MS"}]}]}
        for src, want in (("const THROTTLE_THRESHOLD_MS: f64 = 500.0;", "over 500 ms"),
                          ("const THROTTLE_THRESHOLD_MS: f64 = 2000.0;", "over 2000 ms"),
                          ("const THROTTLE_THRESHOLD_MS: f64 = 250.5;", "over 250.5 ms")):
            r = R.verify_route(spec, None, tree({"m.rs": src}), None, "0.1.3")
            self.assertIn(want, R.drawn(r)[0]["text"])

    def test_ci_ok(self):
        sha = "3" * 40
        repo = {"head": {"sha": sha}, "ci": {"conclusion": "success", "head_sha": sha,
                                            "jobs": [{"name": "Test (ubuntu-latest, stable)", "conclusion": "success"}]}}
        self.assertEqual(R.ci_ok(repo, sha, "Test"), (True, ""))
        self.assertFalse(R.ci_ok(dict(repo, ci=dict(repo["ci"], head_sha="4" * 40)), sha, "Test")[0])
        self.assertFalse(R.ci_ok(dict(repo, ci=dict(repo["ci"], conclusion="failure")), sha, "Test")[0])
        self.assertFalse(R.ci_ok(dict(repo, ci=dict(repo["ci"], jobs=[{"name": "Clippy", "conclusion": "success"}])),
                                 sha, "Test")[0])
        self.assertFalse(R.ci_ok(repo, "5" * 40, "Test")[0], "the route read another commit than CI ran")

    def test_m1_says_what_main_fixed_only_on_its_evidence(self):
        with open(STATS, encoding="utf-8") as fh:
            stats = json.load(fh)
        cfg = load_cfg()
        want = ("On main, a crawl stops by itself once the site runs out of pages: `tests/crawl_exits_when_idle.rs` "
                "passes in CI at `32c2651`. That fix is not on PyPI yet.")
        # review round 6: not printed today. The test runs with --ignore-robots (M1 retires), and the cargo gate fails
        self.assertNotIn("On main", rr.install_block(stats, "Rust-sitemap", cfg))
        self.assertFalse(stats["routes"]["rustmapper"]["gates"]["cargo"]["ok"])
        self.assertNotRegex(want, r"\d+ s\b|seconds", "no idle timing: the test runs with 1 s flags")
        m1 = next(e for e in cfg["route"]["rustmapper"]["entry"] if e["id"] == "M1")
        self.assertEqual(m1["gate"], "cargo")
        spec = {"repo": "x", "entry": [m1]}
        rel = tree({"src/bfs_crawler.rs": 'pub async fn start_crawling(&self) { else => { "Crawl complete: frontier empty" } }'})
        ci_yml = {".github/workflows/ci.yml": "cargo test --all-features"}
        robots_on = dict(ci_yml, **{"tests/crawl_exits_when_idle.rs": "#[test]\nfn crawl_exits_after_frontier_drains() {}"})
        robots_off = dict(ci_yml, **{"tests/crawl_exits_when_idle.rs":
                                     '#[test]\nfn crawl_exits_after_frontier_drains() { "--ignore-robots", }'})
        rc0 = {"version": "0.1.3", "ok": True, "steps": [{"id": "ends_by_itself", "ok": False}]}
        sha = "3" * 40
        repo = {"name": "Rust-sitemap", "head": {"sha": sha}, "ci": {"conclusion": "success", "head_sha": sha,
                "jobs": [{"name": "Test (ubuntu-latest, stable)", "conclusion": "success"}]}}

        def printed(head_files, cargo_ok):
            r = R.verify_route(spec, tree(head_files), rel, sha, "0.1.3")
            r["gates"] = {"cargo": {"ok": cargo_ok, "missing": []}}
            return " ".join(rr.text_entries(r, rc0, {"version": "0.1.3"}, repo))
        # the test runs with robots checks on and the cargo gate holds: printed
        self.assertIn("On main, a crawl stops by itself", printed(robots_on, True))
        # the gate fails (P1's and P2's tests not at HEAD): not printed, whatever the test says
        self.assertEqual(printed(robots_on, False), "")
        # the gate holds but the test still runs with --ignore-robots: the empty alternative retires it
        self.assertEqual(printed(robots_off, True), "")
        r = R.verify_route(spec, tree(robots_off), rel, sha, "0.1.3")
        self.assertEqual([(e["verified"], e["retired"]) for e in R.resolve(r, rc0)], [(True, True)])
        # CI ran at another sha than the route read: not printed
        r = R.verify_route(spec, tree(robots_on), rel, sha, "0.1.3")
        r["gates"] = {"cargo": {"ok": True}}
        self.assertEqual(rr.text_entries(r, rc0, {"version": "0.1.3"}, dict(repo, ci=dict(repo["ci"], head_sha="0" * 40))), [])
        # the test file is gone at HEAD: the entry does not hold
        rel = tree({"src/bfs_crawler.rs": 'pub async fn start_crawling(&self) { else => { "Crawl complete: frontier empty" } }'})
        head = tree({".github/workflows/ci.yml": "cargo test --all-features --verbose"})
        rc = {"version": "0.1.3", "ok": True, "steps": [{"id": "ends_by_itself", "ok": False}]}
        self.assertEqual([e["id"] for e in R.unverified(R.verify_route(spec, head, rel, None, "0.1.3"), rc)], ["M1"])
        # a release that ends by itself retires M1 with H1
        head = tree({".github/workflows/ci.yml": "cargo test --all-features", "tests/crawl_exits_when_idle.rs":
                     "#[test]\nfn crawl_exits_after_frontier_drains() {}"})
        r = R.verify_route(spec, head, rel, None, "0.1.3")
        self.assertEqual([e["id"] for e in R.drawn(r, rc)], ["M1"])
        done = {"version": "0.1.4", "ok": True, "steps": [{"id": "ends_by_itself", "ok": True}]}
        r = R.verify_route(spec, head, rel, None, "0.1.4")
        self.assertEqual((R.drawn(r, done), R.unverified(r, done)), ([], []))

    def test_h1_names_the_release(self):
        with open(STATS, encoding="utf-8") as fh:
            stats = json.load(fh)
        h1 = next(e for e in sheet.plan(stats, load_cfg())["steps"] if e["id"] == "H1")
        self.assertTrue(h1["text"].startswith(f"{stats['edition']['version']} never exits by itself"), h1["text"])


# ================================================================ the sheet half

class RouteSheet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="route-test-")
        with open(STATS, encoding="utf-8") as fh:
            cls.stats = json.load(fh)
        cls.cfg = load_cfg()
        cls.problems, cls.report, cls.out = _build(cls.tmp, "committed")
        cls.full = _write(cls.tmp, all_verified(cls.stats), "full")
        cls.fproblems, cls.freport, cls.fout = _build(cls.tmp, "full", cls.full)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def svg(self, out, ed):
        with open(os.path.join(out, f"hero-{ed}.svg"), encoding="utf-8") as fh:
            return fh.read()

    def test_contract_and_editions(self):
        self.assertEqual(sheet.NAME, "hero")
        self.assertEqual(sheet.KIND, "chart")
        self.assertEqual(sheet.EDITIONS, EDITIONS)
        self.assertEqual(build_assets.load_sheet("hero"), sheet)
        self.assertEqual(set(self.report["sheets"]), {f"hero-{e}" for e in EDITIONS})
        self.assertEqual(self.problems, 0, self.report["problems"])
        self.assertEqual(self.fproblems, 0, self.freport["problems"])
        for e in EDITIONS:
            self.assertNotRegex(self.svg(self.out, e), r"<(animate|animateTransform|set)\b")

    def test_heights(self):
        for e in EDITIONS:
            ent = self.freport["sheets"][f"hero-{e}"]
            self.assertLessEqual(ent["h"], route_check.HEIGHT[scale_of(e)], e)
            self.assertEqual(ent["h"], int(round(ent["route"]["last_baseline"] + sheet.L[scale_of(e)]["foot"])))

    def test_unverified_entry_is_not_drawn(self):
        unv = [e["id"] for e in R.unverified(self.stats["routes"]["rustmapper"], self.stats["runcheck"]["rustmapper"])]
        for e in EDITIONS:
            drawn = self.report["sheets"][f"hero-{e}"]["route"]["drawn"]
            for gid in unv:
                self.assertNotIn(gid, drawn)
            self.assertNotIn("robots.txt", " ".join(t["s"] for t in self.report["sheets"][f"hero-{e}"]["text"])
                             if "S2" in unv else "")

    def test_nothing_has_a_size(self):                            # T-NOSIZE
        a = all_verified(self.stats)
        b = copy.deepcopy(a)
        for r in b["repos"]:
            r["test_functions"] = (r.get("test_functions") or 0) * 3 + 7
            r["commits"] = r["commits"] * 2 + 1
            if isinstance(r.get("lines"), dict):
                r["lines"] = {k: v * 5 for k, v in r["lines"].items()}
        b["repo_count"] = a["repo_count"] + 9
        pa, pb = _write(self.tmp, a, "na"), _write(self.tmp, b, "nb")
        _, _, oa = _build(self.tmp, "na", pa)
        _, _, ob = _build(self.tmp, "nb", pb)
        for e in EDITIONS:
            self.assertEqual(self.shapes(self.svg(oa, e)), self.shapes(self.svg(ob, e)),
                             f"{e}: a shape moved or changed size with the counts")

    @staticmethod
    def shapes(svg):
        """Every non-text shape: rects and circles, and paths that carry their own stroke or fill (a glyph's
        outline is a bare path inside a text group)."""
        out = []
        for m in SHAPES.finditer(svg):
            tag, attrs = m.group(1), m.group(2)
            if tag != "path" or "stroke=" in attrs or "fill=" in attrs:
                out.append(m.group(0))
        return out

    def test_two_builds_byte_identical(self):                     # T-SAME
        _, _, again = _build(self.tmp, "again", self.full)
        for e in EDITIONS:
            self.assertEqual(self.svg(again, e), self.svg(self.fout, e), e)

    def test_every_element_has_a_purpose(self):                   # T-PURPOSE
        ids = set(sheet.PURPOSE)
        for e in EDITIONS:
            svg = self.svg(self.fout, e)
            groups = re.findall(r'<g id="hero-([A-Z]\d+)"', svg)
            self.assertEqual(len(groups), len(set(groups)), f"{e}: an element id repeats")
            self.assertTrue(set(groups) <= ids, f"{e}: drawn without a PURPOSE row: {set(groups) - ids}")
            want = ids
            self.assertEqual(set(groups), want, f"{e}: PURPOSE rows without an element: {want - set(groups)}")
            # every visible mark sits inside an element group
            body = svg.split("<defs>", 1)[-1].split("</defs>", 1)[-1]
            outside = re.sub(r'<g id="hero-[A-Z]\d+">.*?</g>(?=<g id="hero-|\s*</svg>)', "", body, flags=re.S)
            self.assertNotRegex(outside, r"<(path|circle|rect|use)\b", f"{e}: a mark outside every element group")
        for gid, (learns, q, src) in sheet.PURPOSE.items():
            self.assertTrue(learns.strip(), gid)
            self.assertRegex(q, r"^Q[1-5]$", gid)
            self.assertTrue(src.strip(), gid)

    def test_alt_from_the_route(self):                            # T-ALT
        alt = sheet.alt(self.stats, self.cfg)
        self.assertLessEqual(len(alt.split()), 25)
        self.assertNotEqual(alt.split()[0].lower(), "the")
        self.assertIn("rustmapper", alt)
        self.assertIn("data/sitemap.jsonl", alt)
        self.assertIn("Ctrl-C", alt)
        # review round 9: the image's one command is the install; the crawl command lives in the code block
        self.assertTrue(alt.startswith("How to install "), alt)

    def test_no_theme_words(self):                                # T-WORDS
        for rep in (self.report, self.freport):
            for name, e in rep["sheets"].items():
                text = " ".join(t["s"] for t in e["text"]) + " " + e["alt"]
                self.assertEqual(route_check.theme_words(text), [], name)
        self.assertEqual(route_check.theme_words("CT logs, logged before stored"), [])
        self.assertEqual(route_check.theme_words("a sailor's chart"), ["chart"])

    def test_breaks_name_a_fact(self):                            # T-BREAKS
        for what, how, why in sheet.BREAKS:
            self.assertTrue(what and how and why)
            self.assertEqual(route_check.theme_words(why), [], why)
            self.assertNotRegex(why, r"\b(land|sea|water)\b")

    def test_every_run_measured_from_an_allowed_source(self):
        for name, e in self.freport["sheets"].items():
            for t in e["text"]:
                self.assertEqual(t["truth"], "measured", t["s"])
                self.assertIn(t["key"].split(":")[0], route_check.SOURCES, t["s"])

    def test_floors_and_roles(self):
        for name, e in self.freport["sheets"].items():
            phone = "phone" in name
            for t in e["text"]:
                self.assertNotEqual(t["role"], "label-caps")
                self.assertGreaterEqual(t["size"], tokens.FLOORS["phone" if phone else "desk"]["semantic"], t["s"])
                if phone:
                    self.assertGreaterEqual(t["size"] * 390 / 720, 14 - 1e-6)

    def test_trap_is_ringed_by_a_dotted_line(self):               # CONTRAST-DANGER, review round 3
        from checks.contrast import wcag
        for e in EDITIONS:
            svg = self.svg(self.fout, e)
            th = tokens.THEMES["night" if "night" in e else "day"]
            g = re.search(r'<g id="hero-H1">(.*?)</g>(?=<g id="hero-)', svg, re.S).group(1)
            rect = re.search(rf'<rect[^>]*rx="{sheet.DANGER_RX}"[^>]*/>', g).group(0)
            for want in ('fill="none"', f'stroke="{th.accent}"', 'stroke-linecap="round"'):
                self.assertIn(want, rect)
            self.assertRegex(rect, r'stroke-dasharray="0\.1 [0-9.]+"')
            self.assertNotRegex(g, r'<rect[^>]*fill="(?!none)', "no band under the words")
            self.assertNotIn("clipPath", g, "no hatch")
            self.assertGreaterEqual(wcag(th.accent, th.paper), 3.0)
            mk = [m for m in self.freport["sheets"][f"hero-{e}"]["route"]["marks"] if m["kind"] == "danger"]
            self.assertEqual(len(mk), 1)
            words = [t for t in self.freport["sheets"][f"hero-{e}"]["text"] if t["key"] == "routes:H1"]
            x0, y0, x1, y1 = mk[0]["box"]
            for t in words:      # the words sit inside the line, at least the padding away
                self.assertGreaterEqual(t["x0"] - x0, sheet.DANGER_PAD - 0.5)
                self.assertGreaterEqual(x1 - t["x1"], sheet.DANGER_PAD - 0.5)

    def test_the_gap_shows_without_colour(self):                  # review round 3: the shape alone says it
        for e in EDITIONS:
            svg = self.svg(self.out, e)
            grey = re.sub(r'(fill|stroke)="#[0-9A-Fa-f]{6}"', r'\1="#000000"', svg)
            d = re.search(r'<g id="hero-R5"><path d="([^"]+)"', grey).group(1)
            segs = [tuple(map(float, m)) for m in re.findall(r"M[0-9.]+ ([0-9.]+)V([0-9.]+)", d)]
            self.assertEqual(len(segs), 2, f"{e}: the track breaks once, under the loop")
            gap = segs[1][0] - segs[0][1]
            self.assertGreaterEqual(gap, 14, e)
            rep = self.report["sheets"][f"hero-{e}"]["route"]
            self.assertTrue(rep["gap"])
            loop = next(m for m in rep["marks"] if m["kind"] == "line" and m["id"] == "R6")
            self.assertAlmostEqual(segs[0][1], loop["box"][3] - 1.5, places=1)   # it stops at the loop's foot
        # a release that ends by itself: H1 retired, the track whole
        s = copy.deepcopy(self.stats)
        for st in s["runcheck"]["rustmapper"]["steps"]:
            if st["id"] == "ends_by_itself":
                st["ok"] = True
        p = sheet.plan(s, self.cfg)
        self.assertFalse(p["gap"])
        self.assertNotIn("H1", [x["id"] for x in p["steps"]])
        self.assertEqual(p["unverified"], [x["id"] for x in R.unverified(s["routes"]["rustmapper"],
                                                                       s["runcheck"]["rustmapper"])])
        self.assertNotIn("H1", p["unverified"])

    def test_wrap_keeps_lines_long_and_notes_in_the_label_column(self):   # review round 3
        for e in EDITIONS:
            ent = self.report["sheets"][f"hero-{e}"]
            G = sheet.L[scale_of(e)]
            for gid in ("S1", "F1", "C1", "H1"):
                runs = [t for t in ent["text"] if t["key"] == f"routes:{gid}" and t["x0"] >= G["text_x"] - 1]
                lines: dict[float, list] = {}
                for t in runs:
                    lines.setdefault(round(t["y"], 1), []).append(t)
                if len(lines) < 2:
                    continue
                measure = G["right"] - min(t["x0"] for t in runs)
                for y, ts in lines.items():
                    w = max(t["x1"] for t in ts) - min(t["x0"] for t in ts)
                    self.assertGreaterEqual(w, 0.45 * measure, f"{e} {gid}: a line of {w:.0f} at {y}")

    def test_governor_is_a_clause_of_fetch(self):                 # review round 7: no line of its own
        for e in EDITIONS:
            ent = self.report["sheets"][f"hero-{e}"]
            rep = ent["route"]
            self.assertFalse([m for m in rep["marks"] if m["id"] == "G1"], f"{e}: G1 has a mark of its own")
            self.assertNotIn("tick", {m["kind"] for m in rep["marks"]})
            # no note entry renders as its own line under a stop
            self.assertFalse([st for st in rep["steps"] if st.get("under") or st["kind"] == "note"], e)
            f1 = " ".join(t["s"] for t in ent["text"] if t["key"] == "routes:F1")
            # review round 8: 0.1.3's governor cannot cut the fetches in flight, so the clause is the per-host cap
            self.assertIn("fetches up to 20 pages at a time from each host;", f1, e)
            self.assertNotIn("500 ms", f1, e)
            self.assertLess(f1.index("each host"), f1.index("queues"), e)
            th = tokens.THEMES["night" if "night" in e else "day"]
            svg = self.svg(self.out, e)
            f1_fill = set(re.findall(r'fill="(#[0-9A-F]{6})"', re.search(r'<g id="hero-F1">(.*?)</g>', svg, re.S).group(1))) - {th.paper}
            self.assertIn(th.ink, f1_fill, e)

    def test_one_left_edge_and_desk_files_left_of_the_track(self):   # review round 4: ROUTE-LEFT-EDGE
        for e in EDITIONS:
            ent = self.report["sheets"][f"hero-{e}"]
            self.assertEqual(route_check.left_edge(ent, e), [], e)
            G = sheet.L[scale_of(e)]
            xs = {st["x"] for st in ent["route"]["steps"]}
            self.assertEqual(xs, {G["text_x"]}, e)
            files = [t for t in ent["text"] if t["key"].startswith("routes:") and t["x1"] <= G["track_x"]]
            # review round 5: seeder.rs one baseline under the role line read as a line of the title, so on today's
            # stats no desk label is drawn, and the desk teaches what the phone does
            self.assertEqual(files, [], f"{e}: no file names")
            self.assertFalse(ent["route"]["file_labels"], e)
        bad = copy.deepcopy(self.report["sheets"]["hero-day"])
        for t in bad["text"]:
            if t["key"] == "routes:W1" and t["x0"] > sheet.L["desk"]["track_x"]:
                t["x0"] += 30
        self.assertEqual([f.code for f in route_check.left_edge(bad, "hero-day")], ["ROUTE-LEFT-EDGE"])

    def test_lines_are_painted_under_the_marks(self):             # review round 5: ROUTE-PAINT
        for e in EDITIONS:
            svg = self.svg(self.out, e)
            track = svg.index('<g id="hero-R5">')
            for m in re.finditer(r"<circle", svg):
                self.assertGreater(m.start(), track, f"{e}: a ring painted under the track")
            self.assertLess(svg.index('<g id="hero-R6">'), svg.index('<g id="hero-F1">'), e)
            self.assertEqual(route_check.paint_order(svg, e), [], e)
            rep = self.report["sheets"][f"hero-{e}"]["route"]
            self.assertEqual(rep["drawn"][:3], ["T1", "T2", "R0"], "the report keeps the reading order")
        bad = '<g id="hero-S1"><circle/></g><g id="hero-R5"><path/></g>'
        self.assertEqual([f.code for f in route_check.paint_order(bad, "x")], ["ROUTE-PAINT"])

    def test_release_label_follows_its_command(self):             # review round 5: ROUTE-RELEASE
        for e in EDITIONS:
            ent = self.report["sheets"][f"hero-{e}"]
            rl = ent["route"]["release_label"]
            if "phone" in e:      # review round 6: at 600 units it does not fit after the command; it drops under it
                self.assertEqual(rl["x"], sheet.L["phone"]["text_x"], e)
                self.assertEqual(rl["y"], rl["cmd_y"] + sheet.L["phone"]["line"], e)
            else:
                self.assertEqual(rl["y"], rl["cmd_y"], e)
                self.assertLessEqual(rl["x"] - rl["cmd_end"], route_check.RELEASE_GAP_MAX, e)
                self.assertGreater(rl["x"], rl["cmd_end"], e)
            self.assertEqual(route_check.release_near(ent, e), [])
        far = {"route": {"release_label": {"cmd_end": 735, "cmd_y": 178, "x": 1062, "y": 178, "w": 162}, "steps": []}}
        self.assertEqual([f.code for f in route_check.release_near(far, "x")], ["ROUTE-RELEASE"])
        under = {"route": {"release_label": {"cmd_end": 735, "cmd_y": 178, "x": 484, "y": 206, "w": 162},
                           "steps": [{"x": 484}]}}
        self.assertEqual(route_check.release_near(under, "x"), [], "dropped under the command at the left edge")

    def test_loop_arrow_is_on_bare_line(self):                    # review round 5: ROUTE-ARROW
        for e in EDITIONS:
            ent = self.report["sheets"][f"hero-{e}"]
            rep = ent["route"]
            a, r = rep["loop_arrow"], rep["ring_r"]
            for ring in rep["rings"]:
                self.assertTrue(ring["cy"] < a[0] - r - 2 or ring["cy"] > a[1] + r + 2, f"{e} {ring['id']}")
            self.assertEqual(route_check.arrow_clear(ent, e), [])
        near = {"route": {"loop_arrow": [300, 310], "ring_r": 6, "rings": [{"id": "W1", "cy": 314}]}}
        self.assertEqual([f.code for f in route_check.arrow_clear(near, "x")], ["ROUTE-ARROW"])

    def test_code_spaces_are_word_spaces(self):                   # review round 5: ROUTE-CODE-SPACE
        for e in EDITIONS:
            ent = self.report["sheets"][f"hero-{e}"]
            texts = ent["text"]
            sp = ent["route"]["label_space"]
            self.assertEqual(route_check.code_spaces(texts, e, sp), [], e)
            h1 = sorted([t for t in texts if t["key"] == "routes:H1" and t["role"] == "machine"], key=lambda t: (t["y"], t["x0"]))
            self.assertEqual([t["s"] for t in h1], ["Received", "work", "item"], e)
            for a, b in zip(h1, h1[1:]):
                if a["y"] == b["y"]:
                    self.assertLessEqual(b["x0"] - a["x1"], 1.3 * sp + 0.5, e)
            # the code block keeps real spacing for pasting
        block = rr.install_block(self.stats, "Rust-sitemap", load_cfg())
        self.assertIn("rust_sitemap crawl \\", block)
        wide = [{"key": "routes:H1", "role": "machine", "s": "Received work", "x0": 0, "x1": 50, "y": 1}]
        self.assertEqual([f.code for f in route_check.code_spaces(wide, "x", 4.0)], ["ROUTE-CODE-SPACE"])

    def test_desk_file_labels_need_a_line_under_the_title(self):  # review round 5: proximity, not only overlap
        saved = copy.deepcopy(sheet.L["desk"])
        try:
            sheet.L["desk"]["head_y"] = saved["head_y"] + 80        # the rows a line and more below the role line
            n, rep, _out = _build(self.tmp, "farlabels", _write(self.tmp, self.stats, "farlabels"), editions=["day"])
        finally:
            sheet.L["desk"].clear()
            sheet.L["desk"].update(saved)
        self.assertTrue(rep["sheets"]["hero-day"]["route"]["file_labels"], "far enough from the title: drawn")

    def test_desk_files_all_or_none(self):                        # review round 4: a label that would touch the title
        s = copy.deepcopy(self.stats)
        for x in s["routes"]["rustmapper"]["entries"]:
            if x["id"] == "S1":
                x["file"] = "a_very_long_source_file_name_that_reaches_the_role.rs"
        n, rep, _out = _build(self.tmp, "longlabel", _write(self.tmp, s, "longlabel"), editions=["day"])
        self.assertEqual(n, 0, rep["problems"])
        ent = rep["sheets"]["hero-day"]
        self.assertFalse(ent["route"]["file_labels"])
        self.assertFalse([t for t in ent["text"] if t["key"].startswith("routes:") and t["x1"] <= sheet.L["desk"]["track_x"]])

    def test_code_is_in_the_code_face(self):                      # TYPE-CODE on the build
        for e in EDITIONS:
            texts = self.report["sheets"][f"hero-{e}"]["text"]
            self.assertEqual(route_check.code_face(texts, e), [])
            self.assertEqual(route_check.self_twice(texts, e), [])
            mono = [t["s"] for t in texts if t["role"] == "machine" and t["key"] == "routes:C1"]
            # review round 8: C1 names the line that says it is done, `Saved to:` (its space at the label's word space);
            # the file is named once, by the end row
            self.assertEqual(mono, ["Saved", "to"], e)
            self.assertEqual([t["s"] for t in texts if t["role"] == "machine" and t["key"] == "routes:R13"][:1],
                             ["data/sitemap.jsonl"], e)
            ho = [t["s"] for t in texts if t["key"].startswith("handoffs:")]
            # review round 6: what you get, one run on both editions, the count from figures[] "25 ways"; no script
            # path and no ", with a test" (the test is the gate, not the words)
            self.assertEqual(ho, ["sorted 21 ways by ideal-url-organizer"], e)

    def test_title_block_is_name_and_role(self):
        for e in EDITIONS:
            texts = [t for t in self.report["sheets"][f"hero-{e}"]["text"]]
            self.assertFalse(any(t["key"] in ("repo_count", "repos:ci") for t in texts), e)
            self.assertNotIn("1 OF", " ".join(t["s"] for t in texts))

    def test_budgets(self):
        for name, e in self.freport["sheets"].items():
            self.assertLess(e["bytes"], tokens.BUDGETS["phone_svg_kb" if "phone" in name else "svg_kb"] * 1024)
            self.assertLess(e["elements"], tokens.BUDGETS["elements"])

    def test_missing_route_refuses(self):
        s = copy.deepcopy(self.stats)
        s.pop("routes")
        n, _rep, _out = _build(self.tmp, "noroute", _write(self.tmp, s, "noroute"), editions=["day"])
        self.assertGreaterEqual(n, 1)

    def test_failed_runcheck_hides_the_entrance(self):
        s = all_verified(self.stats)
        s["runcheck"]["rustmapper"]["ok"] = False
        p = sheet.plan(s, self.cfg)
        self.assertIsNone(p["install"])
        s = all_verified(self.stats)
        s["runcheck"]["rustmapper"]["version"] = "0.1.2"
        self.assertFalse(sheet.entrance_ok(s)[0])

    @unittest.skipUnless(os.path.exists(LIVE), "live-like stats file not present")
    def test_live_like_stats(self):
        """The live-like file predates the round-6 instruments: with the committed routes, hand-offs, run check,
        heads and scripts grafted on, it builds clean with its own counts (23 repositories, no CI record)."""
        with open(LIVE, encoding="utf-8") as fh:
            live = json.load(fh)
        for key in ("routes", "handoffs", "runcheck"):
            live[key] = copy.deepcopy(self.stats[key])
        live["edition"]["scripts"] = list(self.stats["edition"]["scripts"])
        heads = {r["name"]: r.get("head") for r in self.stats["repos"]}
        for r in live["repos"]:
            if heads.get(r["name"]):
                r["head"] = heads[r["name"]]
        n, rep, _out = _build(self.tmp, "live", _write(self.tmp, live, "live"))
        self.assertEqual(n, 0, rep["problems"])
        texts = " ".join(t["s"] for t in rep["sheets"]["hero-day"]["text"])
        self.assertNotIn(f"1 OF {live['repo_count']}", texts)     # review round 2: the title block is name and role
        self.assertNotIn("CI ON MAIN", texts)


if __name__ == "__main__":
    unittest.main()
