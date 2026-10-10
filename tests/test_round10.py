"""Review round 10 (docs/crit/round6/review-r10-*.md): what each fix promises, held by a test.

The Scrapy run sentence says what start.py does (no seeds without --reset-delta; the bundled seeds counted, and
whose site they are); the cautions list names the release it describes, and no item repeats it; the stop rule has a
text home in the code block; H1's clock starts once the work-item lines stop, not at launch; the scope lever (start
at the bare domain) is the 7th item; each lever starts its own line, so a flag never splits on a phone.
"""
from __future__ import annotations

import copy
import json
import os
import shutil
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
from checks import figures as figures_check, readme as readme_check, strings as strings_check  # noqa: E402
from checks import wrap as wrap_check  # noqa: E402
from data import proof, route as R  # noqa: E402

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


class ScrapyRun(unittest.TestCase):
    """r10-1 #1: the run sentence says what `python start.py` does at 96e7a1a."""

    SENTENCE = ("Run these from the folder you cloned [Scrapy](https://github.com/BenjaminSRussell/Scrapy) into. "
                "`python start.py` starts PostgreSQL, Redis, Grafana and a worker for each of the four stages. It needs "
                "Docker and the `docker-compose` command (Docker Desktop has it; on Linux, install Compose standalone). "
                "It loads no seeds: the last command gives the spider your site.\n\nBefore you run it:\n\n"
                "- The spider obeys `robots.txt` and its `Crawl-delay`, and names itself `<your-bot>` (without that "
                "line, `UConn-Discovery-Crawler/1.0`).\n"
                "- The stage 2 worker then fetches every link the spider queued, disallowed ones too, 4 at a time per "
                "host, as `Python/3.11 aiohttp/3.13.1`.")   # review round 15: the same form as rustmapper's list

    def test_committed(self):
        text = read(README)
        self.assertIn(self.SENTENCE, text)
        self.assertNotIn("sample site", text)
        self.assertNotIn("--reset-delta", text)
        _, stats = load()
        rows = {f["text"]: f for f in stats["figures"]}
        for t in ("a worker for each of the four stages", "It loads no seeds:"):
            self.assertTrue(rows[t]["holds"], rows[t])
        self.assertNotIn("143,208", rows)
        self.assertEqual(figures_check.uncovered(text, stats["figures"]), [])
        self.assertEqual(figures_check.unbacked_claims(text, stats["figures"]), [])

    def test_csv_rows(self):
        src = ('https://a.uconn.edu/x\n\nhttps://uconn.edu/\n"https://b.uconn.edu/open-quote\nhttps://swallowed.org/"\n'
               'https://other.org/\nhttps://notuconn.edu/\n')
        self.assertEqual(proof.csv_rows(src), 5, "the blank line goes; a quote open across a line break is one row")
        self.assertEqual(proof.csv_rows(src, "uconn.edu"), 3, "notuconn.edu is not on uconn.edu")
        rec = proof.figure_records([{"text": "2", "repo": "x", "path": "u.csv", "csv_rows": True, "count": 2}],
                                   {"x": "gd"}, read=lambda gd, p: "a\nb\n")[0]
        self.assertTrue(rec["holds"], rec)
        rec = proof.figure_records([{"text": "3", "repo": "x", "path": "u.csv", "csv_rows": True, "count": 3}],
                                   {"x": "gd"}, read=lambda gd, p: "a\nb\n")[0]
        self.assertFalse(rec["holds"])
        self.assertIn("2 rows", rec["why"])

    def test_sample_site_needs_a_row(self):
        old = "`python start.py` runs all four stages and crawls a university's sample site."
        self.assertTrue(figures_check.unbacked_claims(old, []))
        self.assertEqual(figures_check.unbacked_claims(old, [{"text": "crawls a university's sample site",
                                                              "holds": True}]), [])


class ReleaseLead(unittest.TestCase):
    """r10-1 #2: the list names the release it describes, once, in its lead."""

    def test_committed(self):
        text = read(README)
        head = install(text).split("```", 1)[0]          # review round 11: before the code block
        paras = [p for p in head.split("\n\n") if p.strip()]
        self.assertEqual(paras[1], "Before you run 0.1.3:")
        for it in paras[2].strip().splitlines():
            self.assertFalse(it[2:].startswith("0.1.3"), it)
        _, stats = load()
        self.assertEqual(readme_check.cautions_scope(text, stats), [])

    def test_texts(self):
        cfg, _ = load()
        for gid in ("L4", "X1", "X2"):
            e = entry(cfg, gid)
            for c in [e] + list(e.get("instead") or []):
                self.assertFalse(str(c["text"]).startswith("{release}"), (gid, c["text"]))
        self.assertTrue(entry(cfg, "H1")["text"].startswith("{release} "), "the image has no lead-in: H1 keeps it")

    def test_the_check_bites(self):
        text = read(README)
        _, stats = load()
        self.assertTrue(readme_check.cautions_scope(text.replace("Before you run 0.1.3:", "Before you run it:"), stats))
        self.assertTrue(readme_check.cautions_scope(text.replace("- Its `sitemap.xml`", "- 0.1.3's `sitemap.xml`"), stats))


class StopLines(unittest.TestCase):
    """r10-2 #1 with r10-3 #1's words: the stop rule in the code block, while H1 is drawn with its number."""

    def block(self, stats):
        cfg, _ = load()
        return rr.install_block(stats, "Rust-sitemap", cfg).split("```")[1]

    def test_drawn(self):
        _, stats = load()
        code = self.block(stats)
        self.assertIn('# 0.1.3 runs until stopped: when\n# "Received work item" stops\n# for 60 s, then Ctrl-C once\n',
                      code)
        self.assertNotIn("# stop it with one Ctrl-C", code)
        self.assertTrue(all(len(ln) <= readme_check.CODE_COLUMNS for ln in code.splitlines()), code)
        self.assertIn(rr.STOP_QUIET[0].format(release="0.1.3", quiet=60), install(read(README)))

    def test_without_the_number(self):
        _, stats = load()
        s = copy.deepcopy(stats)
        next(st for st in s["runcheck"]["rustmapper"]["steps"] if st["id"] == "quiet_slow_page")["ok"] = False
        code = self.block(s)
        self.assertIn("# stop it with one Ctrl-C", code)
        self.assertNotIn("30 s", code)

    def test_retired(self):
        _, stats = load()
        s = copy.deepcopy(stats)
        next(st for st in s["runcheck"]["rustmapper"]["steps"] if st["id"] == "ends_by_itself")["ok"] = True
        code = self.block(s)
        self.assertNotIn("Ctrl-C", code)
        self.assertNotIn("30", code)
        self.assertNotIn("Received work item", code)

    def test_twice_allowed(self):
        self.assertIn("received work item", strings_check.TWICE_ALLOW)


class Clock(unittest.TestCase):
    """r10-3 #1: H1's clock starts once the work-item lines stop; every seeder runs before the first work item."""

    FILES = {
        "src/bfs_crawler.rs": ('pub async fn start_crawling(&self) { loop { tokio::select! { else => { eprintln!("Crawl '
                               'complete: frontier empty"); } } eprintln!("Crawler: Received work item: {}", u); } }'
                               ' async fn process_url_streaming(&self) { let _p = tokio::time::timeout('
                               'Duration::from_secs(30), network_permits.acquire_owned()).await; }'),
        "src/cli.rs": 'Crawl {\n #[arg(short, long, default_value = "20", help = "t")]\n timeout: u64,\n}',
        "src/network.rs": "let client = Client::builder().timeout(Duration::from_secs(timeout_secs));",
        "src/state.rs": ("impl HostState { pub const MAX_FAILURES_THRESHOLD: u32 = 3;\n"
                         "pub fn is_permanently_failed(&self) -> bool { self.failures >= Self::MAX_FAILURES_THRESHOLD }\n"
                         "pub fn record_failure(&mut self) { let b = (2_u32.pow(self.failures.min(8))).min(300); } }"),
        "src/main.rs": "crawler.initialize(&seeding_strategy).await?;\nshard.process_incoming_urls(&d).await;"}
    RC = {"version": "0.1.3", "ok": True, "steps": [{"id": "crawl_ctrl_c", "ok": True}, {"id": "ends_by_itself", "ok": False},
                                                    {"id": "quiet_after_last_page", "ok": True},
                                                    {"id": "quiet_slow_page", "ok": True}]}

    def h1(self, files):
        cfg, _ = load()
        r = R.verify_route({"repo": "x", "entry": [entry(cfg, "H1")]}, None, tree(files), None, "0.1.3")
        return R.resolve(r, self.RC)[0]

    def test_words(self):
        cfg, stats = load()
        self.assertEqual(entry(cfg, "H1")["text"],
                         "{release} never exits by itself; done when `Received work item` lines stop for {quiet} s")
        drawn = {e["id"]: e for e in R.drawn(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"])}
        self.assertEqual(drawn["H1"]["quiet"], 60)     # review round 11: 30 (permit) + 20 + 4 + 1 -> 60

    def test_order_anchor(self):
        self.assertIn("lines stop for 60 s", self.h1(self.FILES)["text"])
        flipped = dict(self.FILES, **{"src/main.rs": "shard.process_incoming_urls(&d).await;\n"
                                                     "crawler.initialize(&seeding_strategy).await?;"})
        self.assertEqual(self.h1(flipped)["text"], "{release} never exits by itself, even after the last page",
                         "shards before the seeders: the quiet rule is not verified")

    def test_phone_lines(self):
        """The new words keep the phone row at two lines (today's height, 1,087 units)."""
        cfg, stats = load()
        from sheets import route as sheet
        plan = sheet.plan(stats, cfg)
        h1 = next(e for e in plan["steps"] if e["id"] == "H1")
        self.assertIn("lines stop for 60 s", h1["text"])


class ScopeLever(unittest.TestCase):
    """r10-3 #2: start at the bare domain, the 7th item."""

    WORDS = ("From `www.<site>` it skips sibling hosts such as `blog.`, even ones crt.sh lists. Start at the bare "
             "domain to take them all.")
    URL_UTILS = ("pub fn is_same_domain(url_domain: &str, base_domain: &str) -> bool { url_domain == base_domain || "
                 "(url_domain.ends_with(base_domain)) || (base_domain.ends_with(url_domain)) }")
    FRONTIER = ("async fn add_url_to_local_queue_unchecked(&mut self) { "
                "if !Self::is_same_domain(&url_domain, start_url_domain) { return false; } }")

    def files(self, **over):
        f = {"src/url_utils.rs": self.URL_UTILS, "src/frontier.rs": self.FRONTIER,
             "src/bfs_crawler.rs": "let root_domain = self.get_root_domain(&start_url_domain);",
             "src/ct_log_seeder.rs": ('const DEFAULT_CRTSH_BASE: &str = "https://crt.sh"; format!("{}/?q=%.{}&output=json", b, d); '
                                      'format!("https://crt.sh/?q=%.{}&output=json", d)')}
        f.update(over)
        return f

    def resolve(self, files):
        cfg, _ = load()
        r = R.verify_route({"repo": "x", "entry": [entry(cfg, "L5")]}, tree(files), tree(files), "abc", "0.1.3")
        return R.resolve(r, {"version": "0.1.3", "ok": True, "steps": []})[0]

    def test_committed(self):
        # review round 13: the open list is the four cautions you act on before you run; the rest are in a fold
        items = install(read(README)).split("Before you run 0.1.3:", 1)[1].split("<details>", 1)[0].strip().splitlines()
        self.assertEqual(len(items), 6)      # review round 15: L7 (its name) and L6 (the robots.txt stall)
        self.assertEqual(items[5], "- " + self.WORDS)
        self.assertLessEqual(len(self.WORDS.split()), rr.LIST_MAX_WORDS)
        self.assertEqual(rr.LIST_MAX_ITEMS, 7)

    def test_anchors(self):
        e = self.resolve(self.files())
        self.assertTrue(e["verified"] and not e["retired"], e)
        self.assertEqual(e["text"], self.WORDS)
        siblings = self.files(**{"src/url_utils.rs": self.URL_UTILS.replace("(base_domain.ends_with(url_domain))",
                                                                           "(root(url_domain) == root(base_domain))")})
        e = self.resolve(siblings)
        self.assertTrue(e["verified"] and e["retired"], "a release that takes siblings retires the item")
        unfiltered = self.files(**{"src/frontier.rs": "async fn add_url_to_local_queue_unchecked(&mut self) { }"})
        self.assertTrue(self.resolve(unfiltered)["retired"], "seeds not filtered: the item retires")


class Levers(unittest.TestCase):
    """r10-2 #2: a lever starts its own line, so a flag never splits on a phone."""

    def test_lever_line(self):
        self.assertEqual(rr.lever_line("It sends up to 256. `--workers 1` sends one."),
                         "It sends up to 256.<br>`--workers 1` sends one.")
        self.assertEqual(rr.lever_line("It writes one `sitemap.xml` however many."), "It writes one `sitemap.xml` however many.")
        self.assertEqual(rr.lever_line("It reads HTML. go_go_go can render."), "It reads HTML. go_go_go can render.")

    def test_committed(self):
        text = install(read(README))
        self.assertIn("across all hosts.<br>`--workers 1` sends one at a time.", text)
        self.assertIn("about your domain.<br>`--seeding-strategy none` asks no one.", text)
        _, stats = load()
        self.assertEqual(readme_check.cautions(read(README), rr.LIST_MAX_ITEMS, rr.LIST_MAX_WORDS), [])

    def test_split_rule(self):
        rows = [{"width": 360, "pad": 41, "code": "--workers 1", "at": 2},
                {"width": 360, "pad": 16, "code": "--workers 1", "at": 10},
                {"width": 390, "pad": 16, "code": "--seeding-strategy none", "at": -1},
                {"width": 390, "pad": 16, "code": "sitemap.xml", "at": 4}]
        bad = wrap_check.split_flags(rows)
        self.assertEqual(len(bad), 1)
        self.assertIn("'--' | 'workers 1' at 360 px", bad[0])

    def test_blocks_html(self):
        blocks = wrap_check.blocks_html("Intro with `--flag`.\n\n```sh\n--not-prose\n```\n\n- one `--x 1`\n- two\n")
        self.assertEqual(blocks, [("p", "Intro with <code>--flag</code>."), ("li", "one <code>--x 1</code>"), ("li", "two")])

    def test_items_html(self):
        items = wrap_check.items_html(read(README))
        self.assertTrue(any("<br><code>--workers 1</code>" in i for i in items), items)
        self.assertTrue(any("<code>www.&lt;site&gt;</code>" in i for i in items), items)

    @unittest.skipUnless(shutil.which("node"), "node is not installed")
    def test_render(self):
        """Render tier, in Chromium: the committed items split no flag at 320 to 430 px; the round-9 joins did."""
        blocks = [b for b in wrap_check.blocks_html(read(README)) if "<code>-" in b[1]]
        # review round 14: the Scrapy run sentence lost its one flag (--reset-delta) with the sentence
        # review round 15: and rustmapper's --user-agent lever (L7)
        self.assertEqual([t for t, _ in blocks], ["li", "li", "li"], "the three levers")
        rows = wrap_check.measure(ROOT, blocks)
        if rows is None:
            self.skipTest("render.mjs wrap could not start Chromium")
        self.assertEqual(wrap_check.split_flags(rows), [])
        old = wrap_check.split_flags(wrap_check.measure(ROOT, [(t, h.replace("<br>", " ")) for t, h in blocks]))
        self.assertTrue(any("'--workers 1'" in b for b in old), old)
        self.assertTrue(any("'--seeding-strategy none'" in b for b in old), old)


if __name__ == "__main__":
    unittest.main()
