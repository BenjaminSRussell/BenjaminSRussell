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
EDITIONS = ("day", "night", "phone-day", "phone-night")
SHAPES = re.compile(r"<(rect|circle|path|line|polygon)\b([^>]*)/?>")


def load_cfg() -> dict:
    with open(CFG, "rb") as fh:
        return tomllib.load(fh)


def tree(files: dict[str, str]):
    """A fixture tree: path -> text; the reader returns None for a missing file."""
    return lambda path: files.get(path)


def all_verified(stats: dict) -> dict:
    """The committed stats with every route entry's anchors holding (what the sheet draws once P1 lands). The
    run-check probes stay as measured."""
    s = copy.deepcopy(stats)
    for e in s["routes"]["rustmapper"]["entries"]:
        e.update(verified_head=True, verified_release=True, missing=[])
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
                         ["S1", "S2", "F1", "G1", "W1", "H1", "C1", "R13", "L1", "X1"])
        if not by["S2"]["verified_head"]:
            self.assertIn("head tests/robots_4xx_allows_crawl.rs: file missing", by["S2"]["missing"])
        rc = stats["runcheck"]["rustmapper"]
        drawn = {e["id"]: e for e in R.drawn(route, rc)}
        for gid in ("S1", "F1", "G1", "W1", "H1", "C1", "R13"):
            self.assertIn(gid, drawn, [e for e in R.unverified(route, rc) if e["id"] == gid])
        # the release's words: seeds by default, never ends by itself, a kill writes nothing (run check, 0.1.3)
        self.assertIn("by default", drawn["S1"]["text"])
        # review round 3: H1 states its cause (no exit once the pages run out), not the crawl's scope
        self.assertEqual(drawn["H1"]["text"], "never stops by itself, even after the last page")
        self.assertIn("after a kill, run `export-sitemap`", drawn["C1"]["text"])
        self.assertIn("above or below it", drawn["F1"]["text"])
        self.assertNotIn("kill", drawn["W1"]["text"])
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
            self.assertNotIn("command", sheet.plan(s, cfg))     # review round 2: the command's one home is the README
            block = rr.install_block(s, "Rust-sitemap", cfg)
            self.assertIn(want.split()[0] + " crawl \\\n    --start-url <your-site>", block)
        s = copy.deepcopy(stats)
        s["edition"]["scripts"] = []
        with self.assertRaises(RuntimeError):
            sheet.plan(s, cfg)

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
        self.assertEqual(res[0]["text"], "never stops by itself, even after the last page")
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
        one = tree({"src/main.rs": "fn run_export_sitemap_command(output: String) { SitemapWriter::new(&output); }",
                    "src/sitemap_writer.rs": "pub struct SitemapWriter {}"})
        e = R.drawn(R.verify_route(spec, head, one, "abc", "0.1.3"))[0]
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
            self.assertLessEqual(ent["h"], route_check.HEIGHT["phone" if "phone" in e else "desk"], e)
            self.assertEqual(ent["h"], int(round(ent["route"]["last_baseline"] + (30 if "phone" in e else 36))))

    def test_unverified_entry_is_not_drawn(self):
        unv = [e["id"] for e in self.stats["routes"]["rustmapper"]["entries"]
               if not (e["verified_head"] and e["verified_release"])]
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
            phone = "phone" in e
            G = sheet.L["phone" if phone else "desk"]
            for gid in ("S1", "F1", "C1", "H1"):
                runs = [t for t in ent["text"] if t["key"] == f"routes:{gid}" and t["role"] != "machine" or
                        (t["key"] == f"routes:{gid}" and t["x0"] >= (G["rule_x"] or 0) - 1)]
                lines: dict[float, list] = {}
                for t in runs:
                    lines.setdefault(round(t["y"], 1), []).append(t)
                if len(lines) < 2:
                    continue
                measure = G["right"] - min(t["x0"] for t in runs)
                for y, ts in lines.items():
                    w = max(t["x1"] for t in ts) - min(t["x0"] for t in ts)
                    self.assertGreaterEqual(w, 0.45 * measure, f"{e} {gid}: a line of {w:.0f} at {y}")
            if not phone:
                g1 = [t for t in ent["text"] if t["key"] == "routes:G1"]
                self.assertEqual(round(min(t["x0"] for t in g1)), G["text_x"], "the note starts in the label column")

    def test_code_is_in_the_code_face(self):                      # TYPE-CODE on the build
        for e in EDITIONS:
            texts = self.report["sheets"][f"hero-{e}"]["text"]
            self.assertEqual(route_check.code_face(texts, e), [])
            self.assertEqual(route_check.self_twice(texts, e), [])
            mono = [t["s"] for t in texts if t["role"] == "machine" and t["key"] == "routes:C1"]
            self.assertEqual(mono, ["data/sitemap.jsonl", "export-sitemap"], e)

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
