"""Review round 12 (docs/crit/round6/review-r12-*.md): what each fix promises, held by a test.

A mid edition of the hero for 852 to 1199 px viewports, and HERO-COLUMN-PX holds the drawn height; no "resume" next
to rustmapper while its probe fails; the spider-name sentence is cut and Scrapy's block says where its output lands;
DESIGN.md is generated from the drawn route, in plain words (DESIGN-FRESH); C1 has no colon mid-sentence and "once"
is C1's alone; Scrapy's bullet credits each job to its tool; the fold label names the largest group; rule 3's title
matches its body; the cautions say what 0.1.3 does with a redirect, and what its sitemap.xml keeps.
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

import check  # noqa: E402,F401  (plug-ins import Finding from it)
import build_assets  # noqa: E402
import edition as E  # noqa: E402
import publish_chart  # noqa: E402
import render_readme as rr  # noqa: E402
import runcheck  # noqa: E402
import tokens  # noqa: E402
from checks import column, design, figures as figures_check, readme as readme_check  # noqa: E402
from checks import route as route_check  # noqa: E402
from data import route as R  # noqa: E402
from sheets import route as sheet  # noqa: E402

STATS = os.path.join(ROOT, "assets", "stats.json")
CFG = os.path.join(ROOT, "chart.toml")
README = os.path.join(ROOT, "README.md")
DESIGN = os.path.join(ROOT, "DESIGN.md")


def load():
    with open(CFG, "rb") as fh:
        cfg = tomllib.load(fh)
    with open(STATS, encoding="utf-8") as fh:
        stats = json.load(fh)
    return cfg, stats


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def entry(cfg, eid):
    return next(e for e in cfg["route"]["rustmapper"]["entry"] if e["id"] == eid)


def drawn(stats):
    return {e["id"]: e for e in R.drawn(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"])}


class MidEdition(unittest.TestCase):
    """r12-1 #1: the phone sheet was drawn 1,080 to 1,429 px tall at 1,012 to 1,199 px; the mid edition fits."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="mid-test-")
        cls.report_path = os.path.join(cls.tmp, "build-report.json")
        n = build_assets.main(sheets=["hero"], out=os.path.join(cls.tmp, "v9"), report_path=cls.report_path,
                              stats_path=STATS, cfg_path=CFG, quiet=True)
        assert n == 0, n
        with open(cls.report_path, encoding="utf-8") as fh:
            cls.sheets = json.load(fh)["sheets"]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_editions(self):
        self.assertIn("mid-day", sheet.EDITIONS)
        self.assertIn("mid-night", sheet.EDITIONS)
        ed = E.EDITIONS["mid-night"]
        self.assertEqual((ed.scale, ed.width, ed.dark, ed.mid, ed.phone), ("mid", 820, True, True, False))
        self.assertEqual(tokens.ROLES["mid"]["label"], tokens.ROLES["desk"]["label"], "the desk's type sizes")
        self.assertEqual(self.sheets["hero-mid-day"]["w"], 820)

    def test_served_and_derived(self):
        text = read(README)
        for vw, name in ((851, "hero-phone-day"), (852, "hero-mid-day"), (1180, "hero-mid-day"),
                         (1199, "hero-mid-day"), (1200, "hero-day"), (390, "hero-phone-day")):
            self.assertEqual(column.served(text, vw), name, vw)
        d = column.derive(self.sheets)
        cfg, _ = load()
        self.assertEqual(d["phone_until"] + 1, cfg["chart"]["mid_from_px"], "852 comes from the column table")
        self.assertGreaterEqual(d["mid_w_max"], 820, "820 units hold 11 px text at 852")
        self.assertEqual(column.worst(text, self.sheets), [])
        self.assertEqual(column.tallest(text, self.sheets), [])
        for vw in (852, 1024, 1180, 1199):
            self.assertLessEqual(column.drawn_h(self.sheets["hero-mid-day"], vw), column.TALL_PX, vw)

    def test_the_old_serving_fails(self):
        old = read(README)
        old = re.sub(r'<source media="\(min-width: 852px\)[^>]*>\n', "", old).replace("max-width: 851px", "max-width: 1199px")
        tall = column.tallest(old, self.sheets)
        self.assertEqual((tall[0][0], tall[-1][0]), (852, 1199))
        self.assertGreater(max(h for _, _, h in tall), 1400)

    def test_stacked_like_the_phone(self):
        for ed in ("mid-day", "mid-night"):
            ent = self.sheets[f"hero-{ed}"]
            texts = ent["text"]
            role = max(t["y"] for t in texts if t["key"] == "copy:role_line")
            proj = min(t["y"] for t in texts if t["key"] == "routes:project")
            self.assertGreater(proj, role, "the route's heading is under the role line")
            self.assertEqual(route_check.head_gap(texts, ed), [])
            ids = [s["id"] for s in ent["route"]["steps"]]
            self.assertEqual(ids, [s["id"] for s in self.sheets["hero-phone-day"]["route"]["steps"]], "same rows")
            self.assertLessEqual(ent["h"], route_check.HEIGHT["mid"])

    def test_publish_needs_every_named_edition(self):
        files = [("x", f"assets/v9/hero-{e}.svg") for e in ("day", "night", "phone-day", "phone-night")]
        self.assertEqual(publish_chart.unshipped(files, README), ["hero-mid-day.svg", "hero-mid-night.svg"])
        files += [("x", "assets/v9/hero-mid-day.svg"), ("x", "assets/v9/hero-mid-night.svg")]
        self.assertEqual(publish_chart.unshipped(files, README), [])


class Resume(unittest.TestCase):
    """r12-1 #2: no `resume` next to rustmapper while resume_after_kill fails."""

    def test_committed(self):
        _, stats = load()
        text = read(README)
        self.assertIn("with the same crawl and export-sitemap commands", text)
        self.assertEqual(readme_check.failed_subcommands(text, stats), [])
        st = next(s for s in stats["runcheck"]["rustmapper"]["steps"] if s["id"] == "resume_after_kill")
        self.assertFalse(st["ok"])

    def test_the_check_bites(self):
        _, stats = load()
        bad = read(README).replace("same crawl and export-sitemap", "same crawl, resume and export-sitemap")
        self.assertEqual(len(readme_check.failed_subcommands(bad, stats)), 1)
        ok = copy.deepcopy(stats)
        next(s for s in ok["runcheck"]["rustmapper"]["steps"] if s["id"] == "resume_after_kill")["ok"] = True
        self.assertEqual(readme_check.failed_subcommands(bad, ok), [], "a release that resumes may say so")


class ScrapyBlock(unittest.TestCase):
    """r12-1 #3, r12-3 #2, r12-2 #4: the spider-name sentence goes, the output's place comes, each job to its tool."""

    def test_committed(self):
        text = read(README)
        self.assertNotIn("Spiders run by name", text)
        self.assertIn("Grafana opens on `localhost:3000`. The crawl's output lands in Delta tables under `data/delta/`; "
                      "[DATA_USAGE.md](https://github.com/BenjaminSRussell/Scrapy/blob/main/Scraping_project/docs/"
                      "guides/DATA_USAGE.md) lists them and shows how to read or export them.", text)
        self.assertIn("Repeat URLs are dropped by their hash. In stage 3 a page's "
                      "summary is its first five sentences;", text)
        self.assertNotIn("extractive summary", text)

    def test_rows_hold(self):
        _, stats = load()
        rows = {f["text"]: f for f in stats["figures"]}
        for t in ("first five sentences", "Delta tables under `data/delta/`", "crawl and export-sitemap commands"):
            self.assertTrue(rows[t]["holds"], t)
        self.assertEqual(figures_check.uncovered(read(README), stats["figures"]), [])


class DesignPage(unittest.TestCase):
    """r12-2 #1: DESIGN.md is generated, current, in plain words, and lists only what the hero draws with."""

    def test_fresh(self):
        self.assertEqual(read(DESIGN), tokens.design_md() + "\n")
        self.assertEqual(design.theme_words(read(DESIGN)), [])

    def test_head(self):
        text = read(DESIGN)
        self.assertTrue(text.startswith("<!-- Generated by"), "the maintainer note is a comment")
        self.assertIn("\n# How the picture is drawn\n", text)
        for gone in ("Honesty conventions", "## Motion", "500 ms", "pencil-note", "survey", "sea-name"):
            self.assertNotIn(gone, text)
        self.assertIn("the dotted line round the 0.1.3 catches", text)     # review round 15: two catches, one line
        self.assertIn("the track to follow", text)

    def test_idea_follows_the_route(self):
        cfg, stats = load()
        idea = tokens.idea(stats, cfg)
        self.assertLessEqual(len(idea.split()), tokens.IDEA_MAX_WORDS)
        self.assertIn("“fetches up to 20 pages at a time from each host”", idea)
        s2 = copy.deepcopy(stats)
        f1 = next(e for e in s2["routes"]["rustmapper"]["entries"] if e["id"] == "F1")
        for c in [f1] + list(f1.get("instead") or []):
            c["text"] = "fetches pages; queues their links"
        self.assertIn("“fetches pages”", tokens.idea(s2, cfg), "a reworded row rewrites the page")

    def test_the_check_bites(self):
        old = read(DESIGN).replace("the track to follow", "the ship's track through the islands")
        self.assertEqual(design.theme_words(old), ["islands", "ship's"])
        self.assertEqual(design.theme_words("`survey` in code <!-- datum --> is fine"), [])


class Wording(unittest.TestCase):
    """r12-2 #2, #3, #5, #6."""

    def test_c1_has_no_colon_mid_sentence(self):
        cfg, stats = load()
        c1 = drawn(stats)["C1"]["text"]
        self.assertEqual(c1, "press Ctrl-C once and wait for `Saved to`; a second press quits without writing the file")
        self.assertNotIn("Saved to:", c1)
        # the anchors still test the tool's own line, colon and all
        self.assertTrue(any('println!("Saved to: ' in str(a.get("before")) for a in entry(cfg, "C1")["release"]))

    def test_once_is_c1s_alone(self):
        _, stats = load()
        rows = drawn(stats)
        steps = [e for e in rows.values() if e["kind"] in ("stop", "step", "note", "trap", "end")]
        with_once = [e["id"] for e in steps if re.search(r"\bonce\b", e["text"])]
        self.assertEqual(with_once, ["C1"])
        self.assertIn("quit when `Received work item` lines stop for 60 s", rows["H1"]["text"])

    def test_fold_label_names_the_largest_group(self):
        groups = {"scrapers and data tools": ["FashionDB", "Data-visualizer", "Elusive_trades_data",
                                              "mlx_Qwen_data_entry", "MLX_convertion", "Course_crusader"],
                  "Swift apps": ["3d-swift-globe-widget", "Spotify_to_apple_music", "3d-swift-widget",
                                 "2d-swift-widgets"],
                  "games": ["cozy-game", "Data_science_dev", "Wheel"],
                  "a C game engine": ["game_engine"],
                  "": ["excel-and-vba"]}
        text = read(README)
        fold = text.split('<a name="also"></a>', 1)[1].split("<details>", 1)[1].split("</details>", 1)[0]
        listed = re.findall(r"\(https://github\.com/BenjaminSRussell/([\w.-]+)\)", fold)
        self.assertEqual(sorted(listed), sorted(n for v in groups.values() for n in v), "the table is the fold")
        label = re.search(r"<summary>(.*?)</summary>", text.split('<a name="also"></a>', 1)[1]).group(1)
        named = [g for g in groups if g and g in label]
        largest = max(groups, key=lambda g: len(groups[g]))
        self.assertEqual(named[0], largest, "the label leads with the largest group")
        self.assertIn("15<!-- /n --> more repositories: scrapers and data tools, Swift apps, games, a C game engine",
                      label)

    def test_rule_three_title(self):
        text = read(README)
        self.assertIn("3. **Measure in week one.** Metrics were exported 6 days after the first commit", text)


class Redirects(unittest.TestCase):
    """r12-3 #1: X2 true after a redirect, X3 says what 0.1.3 does with one, X1 what its sitemap.xml keeps."""

    def test_committed(self):
        _, stats = load()
        rows = drawn(stats)
        self.assertEqual(rows["X3"]["text"], "After a redirect it keeps the old address and reads the page's links "
                         "from it: if `/docs` redirects to `/docs/`, `a.html` is fetched as `/a.html`.")
        self.assertIn("redirected or not", rows["X2"]["text"])
        self.assertIn("It keeps `noindex`, canonicalized and disallowed pages.", rows["X1"]["text"])
        steps = {s["id"]: s for s in stats["runcheck"]["rustmapper"]["steps"]}
        self.assertTrue(steps["redirect_kept"]["ok"] and steps["sitemap_keeps_noindex"]["ok"])
        items = rr.text_paragraphs(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"], stats["edition"],
                                   items=True)
        self.assertEqual(len(items), 10)      # review round 15: L7 and L6
        for fold in (False, True):      # review round 13: the open list and the fold, each within the cap
            self.assertLessEqual(len(rr.text_paragraphs(stats["routes"]["rustmapper"], stats["runcheck"]["rustmapper"],
                                                        stats["edition"], items=True, fold=fold)), rr.LIST_MAX_ITEMS)
        for t in items:
            self.assertLessEqual(len(t.split()), rr.LIST_MAX_WORDS, t)
        self.assertEqual(readme_check.cautions(read(README)), [])

    def test_retires_when_fixed(self):
        _, stats = load()
        rc = copy.deepcopy(stats["runcheck"]["rustmapper"])
        next(s for s in rc["steps"] if s["id"] == "redirect_kept")["ok"] = False
        res = {e["id"]: e for e in R.resolve(stats["routes"]["rustmapper"], rc)}
        self.assertTrue(res["X3"]["verified"] and res["X3"]["retired"])
        self.assertFalse(res["X2"]["verified"], "X2's redirect clause needs the probe too")

    def test_anchors(self):
        cfg, _ = load()
        spec = {"repo": "x", "entry": [entry(cfg, "X3")]}

        def tree(files):
            return lambda p: files.get(p)
        head = {"src/bfs_crawler.rs": "let effective_base = base_href.as_deref().unwrap_or(&job.url).to_string();",
                "src/network.rs": "Client::builder()"}
        rel = {"src/bfs_crawler.rs": "base_href.as_deref().unwrap_or(&job_url_clone).to_string()",
               "src/network.rs": "Client::builder()"}
        e = R.verify_route(spec, tree(head), tree(rel), "abc", "0.1.3")["entries"][0]
        self.assertTrue(e["verified_head"] and e["verified_release"], e["missing"])
        fixed = dict(rel, **{"src/bfs_crawler.rs": rel["src/bfs_crawler.rs"] + " let u = response.url().clone();"})
        e = R.verify_route(spec, tree(head), tree(fixed), "abc", "0.1.4")["entries"][0]
        self.assertFalse(e["verified_release"])

    def test_verdicts(self):
        paths = [(0, "/"), (1, "/old"), (1, "/new.html"), (1, "/dir"), (1, "/dir/"), (2, "/child.html")]
        recs = {"old": {"status_code": 200, "title": "New"}}
        self.assertTrue(runcheck.redirect_verdict(paths, recs)[0])
        self.assertFalse(runcheck.redirect_verdict(paths + [(3, "/dir/child.html")], recs)[0])
        self.assertFalse(runcheck.redirect_verdict(paths, {"old": {"status_code": 301}})[0])
        self.assertTrue(runcheck.keeps_verdict(["index.html", "canon.html", "dir", "new.html", "old"])[0])
        self.assertFalse(runcheck.keeps_verdict(["index.html", "new.html"])[0])
        self.assertIn("redirect_kept", runcheck.PROBES)
        for f in ("index.html", "new.html", "canon.html", "dir/index.html", "dir/child.html"):
            self.assertTrue(os.path.isfile(os.path.join(runcheck.REDIRECT_SITE, f)), f)
        self.assertIn('content="noindex"', read(os.path.join(runcheck.REDIRECT_SITE, "canon.html")))


if __name__ == "__main__":
    unittest.main()
