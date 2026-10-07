"""edition.py: the edition table, id prefixing, the SVG envelope, integer formatting, write()."""
from __future__ import annotations

import hashlib
import os
import re
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(HERE), "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import edition as E  # noqa: E402
import tokens  # noqa: E402


class EditionTable(unittest.TestCase):
    def test_six_plus_two(self):
        self.assertEqual(E.EDITION_NAMES, ("day", "night", "still-day", "still-night", "phone-day", "phone-night"))
        self.assertEqual(E.HERO_EXTRA, ("phone-still-day", "phone-still-night"))
        self.assertEqual(set(E.EDITIONS), set(E.EDITION_NAMES) | set(E.HERO_EXTRA))

    def test_flags(self):
        for name, ed in E.EDITIONS.items():
            self.assertEqual(ed.name, name)
            self.assertEqual(ed.motion, "still" not in name, name)
            self.assertEqual(ed.scale, "phone" if name.startswith("phone") else "desk", name)
            self.assertEqual(ed.width, 720 if ed.phone else 1280, name)
            self.assertIs(ed.theme, tokens.THEMES["night" if name.endswith("night") else "day"], name)
        self.assertEqual(E.EDITIONS["day"].form, "desk")
        self.assertEqual(E.EDITIONS["still-day"].form, "still")
        self.assertEqual(E.EDITIONS["phone-night"].form, "phone")
        self.assertFalse(E.EDITIONS["day"].as_still().motion)

    def test_file_names(self):
        self.assertEqual(E.file_name("hero", E.EDITIONS["phone-still-day"]), "hero-phone-still-day.svg")
        self.assertEqual(E.file_name("footer", "night"), "footer-night.svg")
        with self.assertRaises(KeyError):
            E.edition("dusk")


class IdPrefixing(unittest.TestCase):
    def test_every_reference_form(self):
        body = ('<clipPath id="neat"/><g clip-path="url(#neat)" fill="url(#hatch)">'
                '<use href="#g-13-48"/><use xlink:href="#boat"/>'
                '<animate id="arrive" begin="sea10.begin+3.3s; serpent.end+93.6s" end="arrive.end"/>'
                '<a href="https://example.org/x#frag">x</a></g>')
        out = E.prefix_ids(body, "footer")
        self.assertIn('id="footer-neat"', out)
        self.assertIn('url(#footer-neat)', out)
        self.assertIn('url(#footer-hatch)', out)
        self.assertIn('href="#footer-g-13-48"', out)
        self.assertIn('xlink:href="#footer-boat"', out)
        self.assertIn('id="footer-arrive"', out)
        self.assertIn('begin="footer-sea10.begin+3.3s; footer-serpent.end+93.6s"', out)
        self.assertIn('end="footer-arrive.end"', out)
        self.assertIn('href="https://example.org/x#frag"', out, "external hrefs are not ids")

    def test_idempotent(self):
        once = E.prefix_ids('<rect id="a" fill="url(#b)"/><use href="#a"/>', "hero")
        self.assertEqual(E.prefix_ids(once, "hero"), once)
        self.assertNotIn("hero-hero-", once)

    def test_numeric_begin_untouched(self):
        self.assertEqual(E.prefix_ids('<animate begin="4s" dur="24s"/>', "hero"), '<animate begin="4s" dur="24s"/>')


class Envelope(unittest.TestCase):
    def test_header_paper_and_prefix(self):
        ed = E.EDITIONS["night"]
        doc = E.svg(ed, 1280.0, 740, '<rect id="x" width="10" height="10"/>', '<clipPath id="c"/>', sheet="hero")
        self.assertTrue(doc.startswith('<?xml version="1.0" encoding="UTF-8"?>\n<!-- chart v9 · sheet hero · edition night'))
        self.assertIn("built by scripts/build_assets.py", doc)
        self.assertIn(E.STATS_SHA_PLACEHOLDER, doc)
        self.assertIn("do not edit", doc)
        self.assertIn('viewBox="0 0 1280 740" width="1280" height="740"', doc)
        # the paper is the first element and is opaque in the theme's paper colour
        m = re.search(r'<svg[^>]*>\n(<rect [^>]*/>)', doc)
        self.assertIsNotNone(m)
        self.assertIn(f'fill="{tokens.THEMES["night"].paper}"', m.group(1))
        self.assertNotIn("opacity", m.group(1))
        self.assertIn('<defs><clipPath id="hero-c"/></defs>', doc)
        self.assertIn('id="hero-x"', doc)
        self.assertIn('data-edition="night"', doc)
        stamped = E.stamp(doc, "abc123def456")
        self.assertNotIn(E.STATS_SHA_PLACEHOLDER, stamped)
        self.assertIn("stats.json abc123def456", stamped)

    def test_no_timestamps(self):
        doc = E.svg(E.EDITIONS["day"], 100, 100, "", sheet="t")
        self.assertIsNone(re.search(r"20\d\d-\d\d-\d\dT", doc))


class Numbers(unittest.TestCase):
    def test_I_rounds_half_away_from_zero(self):
        self.assertEqual(E.I(2.5), 3)
        self.assertEqual(E.I(3.5), 4)
        self.assertEqual(E.I(-2.5), -3)
        self.assertEqual(E.I(2.4999), 2)
        self.assertEqual(E.I(0), 0)
        self.assertIsInstance(E.I(7.0), int)

    def test_fmt(self):
        self.assertEqual(E.fmt(12.0), "12")
        self.assertEqual(E.fmt(12.25), "12.3")
        self.assertEqual(E.fmt(12.24), "12.2")
        self.assertEqual(E.fmt(-0.04), "0")
        self.assertEqual(E.fmt(0.5), "0.5")
        self.assertEqual(E.fmt(-3.10), "-3.1")
        self.assertEqual(E.fmt(1.004, 2), "1")
        self.assertEqual(E.pt(3.4, 7.6), "3,8")


class Writing(unittest.TestCase):
    def test_write_returns_sizes_and_is_stable(self):
        doc = E.svg(E.EDITIONS["day"], 200, 100, '<rect id="r" width="5" height="5"/>' * 50, sheet="t")
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "sub", "t-day.svg")
            nbytes, gz = E.write(path, doc)
            with open(path, "rb") as fh:
                data = fh.read()
            self.assertEqual(nbytes, len(data))
            self.assertEqual(gz, E.gz_size(data))
            self.assertLess(gz, nbytes)
            sha = hashlib.sha256(data).hexdigest()
            self.assertEqual(E.write(path, doc), (nbytes, gz))
            with open(path, "rb") as fh:
                self.assertEqual(hashlib.sha256(fh.read()).hexdigest(), sha)
        self.assertEqual(E.count_elements(doc), 2 + 50)   # svg + paper + 50 rects
        self.assertEqual(E.count_paths(doc), 0)


if __name__ == "__main__":
    unittest.main()
