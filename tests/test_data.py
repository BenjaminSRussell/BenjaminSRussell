"""tests for scripts/data (T7): identity filter, commit-days, derive() on a fixture, validate(), logsim arithmetic."""
from __future__ import annotations

import copy
import datetime as dt
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))

from data import derive as D, logsim, model, releases  # noqa: E402
from data.claims import claims, upright_ok  # noqa: E402
from data.survey import Commit, commit_days, is_ben, is_bot, span_label, summarize, week_starts  # noqa: E402
import build_stats  # noqa: E402

TAKEN = dt.date(2026, 10, 7)
EST = dt.timezone(dt.timedelta(hours=-5))
EDT = dt.timezone(dt.timedelta(hours=-4))
BEN = ("Benjamin Russell", "benjamin.sheldon.russell@gmail.com")
BOT = ("google-labs-jules[bot]", "161369871+google-labs-jules[bot]@users.noreply.github.com")


def c(y, m, d, h, who=BEN, tz=EDT, subject="work", mi=0) -> Commit:
    return Commit(f"{y}{m:02d}{d:02d}{h:02d}{mi:02d}", dt.datetime(y, m, d, h, mi, tzinfo=tz), who[0], who[1], subject)


def fixture_records() -> list[dict]:
    """Three repos: a steady one, a one-fortnight sprint with a bot, and a dormant one."""
    steady = []
    day = dt.date(2025, 10, 6)  # a Monday
    for k in range(52):          # one commit-day a week for 52 weeks, at 16h local, two commits
        d = day + dt.timedelta(weeks=k)
        steady += [c(d.year, d.month, d.day, 16), c(d.year, d.month, d.day, 16, mi=30)]
    sprint = []
    for k in range(10):          # 4–13 Jan 2026, 20 commits a day at 21h UTC == 16h EST, plus a bot
        d = dt.date(2026, 1, 4) + dt.timedelta(days=k)
        sprint += [c(d.year, d.month, d.day, 16, tz=EST, mi=i) for i in range(20)]
        sprint.append(c(d.year, d.month, d.day, 3, who=BOT, tz=EST))
    dormant = [c(2025, 11, 9, 14), c(2025, 11, 10, 14), c(2026, 10, 7, 9)]  # last touch on the sweep day only
    sweep = c(2026, 10, 7, 9, mi=5)                                         # 7 Oct 2026 touches all three repos
    return [summarize("steady", steady + [sweep], None, TAKEN), summarize("sprint", sprint + [sweep], None, TAKEN),
            summarize("dormant", dormant, None, TAKEN)]


def fixture_stats() -> dict:
    recs = fixture_records()
    gh = {"account_since": "2024-10", "followers": 46, "stars": 1, "repo_count": 4, "calendar_total": 900,
          "calendar_weeks": None, "languages": [{"name": "Python", "share": 1.0, "bytes": 10}]}
    ed = {"project": "rustmapper", "version": "0.1.3", "date": "2025-11-08", "releases": 4, "status": "alpha",
          "wheels": ["cp313-cp313-macosx_11_0_arm64"], "stale": False}
    notices = releases.from_pypi("Rust-sitemap", {**ed, "uploads": [{"version": "0.1.3", "date": "2025-11-08", "time": "x"}]})
    return build_stats.assemble(recs, TAKEN, "2026-10-07T06:34:00Z", "local", "cache", gh, ed, notices, {"2026": []},
                                claims({}), None, [{"letter": "A", "name": "SITEMAPS", "first": None}],
                                [{"name": "ghost", "reason": "no history"}],
                                {"clones": "live", "graphql": "cache", "rest": "none", "pypi": "live", "releases": "none"})


class Identity(unittest.TestCase):
    def test_names_and_emails(self):
        self.assertTrue(is_ben("Benjamin Russell", "x@y"))
        self.assertTrue(is_ben("Ben Russell", "x@y"))
        self.assertTrue(is_ben("someone", "russell27sail@gmail.com"))
        self.assertTrue(is_ben("BenjaminSRussell", "benjamin@users.noreply.github.com"))  # the fourth string
        self.assertTrue(is_ben("x", "123+benjaminsrussell@users.noreply.github.com"))
        self.assertFalse(is_ben("Claude", "noreply@anthropic.com"))
        self.assertFalse(is_ben(*BOT))

    def test_bots(self):
        self.assertTrue(is_bot("Claude"))
        self.assertTrue(is_bot("dependabot[bot]"))
        self.assertFalse(is_bot("Benjamin Russell"))

    def test_toml_identity_merges(self):
        from data.survey import identity_from_toml
        ident = identity_from_toml({"identity": {"names": ["Only Me"]}, "chart": {"login": "me"}})
        self.assertEqual(ident["names"], ["Only Me"])
        self.assertEqual(ident["login"], "me")
        self.assertIn("russell27sail@gmail.com", ident["emails"])


class CommitDays(unittest.TestCase):
    def test_author_local_dates_and_modal_hour(self):
        # 21h UTC on 5 Jan is 16h EST: the day and the hour are the author's, not UTC's
        cs = [c(2026, 1, 5, 16, tz=EST, mi=i) for i in range(3)] + [c(2026, 1, 5, 23, tz=EST)]
        days = commit_days(cs)
        self.assertEqual(days, [{"d": "2026-01-05", "h": 16, "n": 4}])

    def test_tie_goes_to_earliest_hour(self):
        self.assertEqual(commit_days([c(2026, 1, 5, 9), c(2026, 1, 5, 7)])[0]["h"], 7)

    def test_summarize_invariants(self):
        r = fixture_records()[1]
        self.assertEqual(sum(r["hours"]), r["commit_days"])
        self.assertEqual(sum(r["weekdays"]), r["commit_days"])
        self.assertEqual(r["commits"] + sum(o["commits"] for o in r["others"]), r["all_hands"])
        self.assertEqual(r["commits"], 201)
        self.assertEqual(r["others"], [{"name": BOT[0], "commits": 10, "bot": True}])
        self.assertEqual(r["commit_days"], 11)
        self.assertEqual(r["hours"][16], 10)           # hours count DAYS, not the 200 commits
        self.assertEqual(sum(r["weeks"]), 201)
        self.assertEqual(r["tz_offsets"], {"-0500": 200, "-0400": 1})
        self.assertEqual(r["span"], "Jan 2026–")

    def test_span(self):
        self.assertEqual(span_label("2025-09-25", "2026-10-07", TAKEN), "Sep 2025–")
        self.assertEqual(span_label("2025-09-25", "2026-03-01", TAKEN), "Sep 2025–Mar 2026")


class Derive(unittest.TestCase):
    def setUp(self):
        self.recs = fixture_records()
        self.d = D.derive(self.recs, TAKEN)

    def test_weeks_sum_and_units(self):
        self.assertEqual(len(self.d["weeks"]), 52)
        self.assertEqual(sum(w["n"] for w in self.d["weeks"]), sum(sum(r["weeks"]) for r in self.recs))
        self.assertEqual(self.d["weeks"][-1]["start"], week_starts(TAKEN)[-1].isoformat())
        for w in self.d["weeks"]:
            self.assertEqual(w["n"], sum(w["repos"].values()))

    def test_tide_hw_cause_and_run(self):
        t = self.d["tide"]
        self.assertEqual(t["hw"]["cause"], "sprint")
        self.assertEqual(t["hw"]["start"], "2026-01-05")
        self.assertEqual(t["hw"]["n"], 7 * 20 + 2)          # Mon–Sun 5–11 Jan: 140 sprint + 2 steady
        self.assertEqual(t["hw"]["cause_days"], 10)        # the consecutive 4–13 Jan run
        self.assertIsInstance(t["median"], (int, float))
        self.assertIn("month", t["slack"])
        self.assertEqual(t["lw"]["n"], min(w["n"] for w in self.d["weeks"][:-1]))

    def test_sweeps_active_dormant(self):
        self.assertEqual(self.d["sweep_threshold"], 2)      # 3 repos → ceil(3/3) = 1, floored at 2
        dates = {s["date"] for s in self.d["sweeps"]}
        self.assertIn("2026-10-07", dates)                 # all three repos
        self.assertIn("2025-11-10", dates)                 # a Monday: steady + dormant = 2 repos
        self.assertNotIn("2025-11-09", dates)              # dormant alone is not a sweep
        by = {r["name"]: r for r in self.d["repos"]}
        self.assertTrue(by["steady"]["active"])
        self.assertFalse(by["dormant"]["active"])
        self.assertTrue(by["dormant"]["dormant"])            # its only recent day was a sweep day
        self.assertEqual(D.sweep_threshold(21), 5)
        self.assertEqual(D.sweep_threshold(9), 3)

    def test_variation_thin_prior_window(self):
        v = self.d["variation"]
        self.assertEqual(v["hour"], 16)
        self.assertIsNone(v["annual_change"])              # prior window holds < 60 commit-days
        self.assertEqual(v["year"], 2026)
        self.assertEqual(D.circ_diff(1, 23), 2)
        self.assertEqual(D.circ_diff(23, 1), -2)
        self.assertEqual(D.circ_diff(16, 4), 12)

    def test_hours_are_commit_days(self):
        self.assertEqual(sum(self.d["hours"]), sum(r["commit_days"] for r in self.recs))
        self.assertEqual(self.d["hours_basis"], "author-local commit-days")

    def test_corrections_and_unsurveyed(self):
        cs = [c(2025, 11, 22, 10, subject="profile v1"), c(2026, 1, 2, 10, subject="fix"), c(2026, 1, 3, 10, who=BOT)]
        corr = D.corrections(cs)
        self.assertEqual([x["n"] for x in corr["2025"]], [1])
        self.assertEqual([x["n"] for x in corr["2026"]], [2])
        self.assertEqual(D.unsurveyed(["a", "b", "c"], ["a"], ["c"]),
                         [{"name": "b", "reason": "no history"}, {"name": "c", "reason": "clone failed"}])


class Validate(unittest.TestCase):
    def test_fixture_is_valid(self):
        s = fixture_stats()
        self.assertEqual(model.validate(s, today=TAKEN), [])
        self.assertEqual(s["commits"], 105 + 201 + 3)
        self.assertEqual(s["all_hands"], 105 + 211 + 3)
        self.assertEqual(s["notices"][0]["n"], 1)
        self.assertEqual(s["repo_count"], 4)
        self.assertEqual(s["repos"][0]["name"], "sprint")

    def test_rejects(self):
        s = fixture_stats()
        bad = copy.deepcopy(s); bad["seeded"] = False
        self.assertTrue(any("seeded" in e for e in model.validate(bad, today=TAKEN)))
        bad = copy.deepcopy(s); bad["provenance"]["mode"] = "cache-failed"
        self.assertTrue(any("provenance.mode" in e for e in model.validate(bad, today=TAKEN)))
        self.assertFalse(any("provenance.mode" in e for e in model.validate(bad, today=TAKEN, allow_failed=True)))
        bad = copy.deepcopy(s)
        self.assertTrue(any("days old" in e for e in model.validate(bad, today=TAKEN + dt.timedelta(days=9))))
        bad = copy.deepcopy(s); bad["repos"][0]["hours"][3] += 1
        self.assertTrue(any("sum(hours)" in e for e in model.validate(bad, today=TAKEN)))
        bad = copy.deepcopy(s); bad["repos"][0]["others"][0]["commits"] += 1
        self.assertTrue(any("all_hands" in e for e in model.validate(bad, today=TAKEN)))
        bad = copy.deepcopy(s); bad["repos"] = {r["name"]: r for r in s["repos"]}
        self.assertIn("repos must be a list", model.validate(bad, today=TAKEN))
        bad = copy.deepcopy(s); bad["claims"]["workers"]["measured"] = True
        self.assertTrue(any("measured without source" in e for e in model.validate(bad, today=TAKEN)))

    def test_schema_validator(self):
        sch = {"type": "object", "required": ["a"], "properties": {"a": {"type": "integer", "minimum": 1},
               "b": {"anyOf": [{"type": "null"}, {"type": "string", "pattern": "^x"}]}}, "additionalProperties": False}
        self.assertEqual(model.schema_errors({"a": 1, "b": None}, sch), [])
        self.assertTrue(model.schema_errors({"a": 0}, sch))
        self.assertTrue(model.schema_errors({"a": True}, sch))          # bool is not an integer
        self.assertTrue(model.schema_errors({"a": 1, "b": "y"}, sch))
        self.assertTrue(model.schema_errors({"a": 1, "z": 1}, sch))
        self.assertTrue(model.schema_errors({}, sch))

    def test_charted_branches_drop_a_bots(self):
        ident = {"bots": ["Claude"]}
        brs = [{"name": "claude/x", "last": "2025-11-09", "author": "Claude"},
               {"name": "fix/1", "last": "2025-11-09", "author": "Benjamin Russell"},
               {"name": "old-cache", "last": "2025-01-01"},
               {"name": "dep", "last": "2025-02-01", "author": "dependabot[bot]"}]
        self.assertEqual([b["name"] for b in build_stats.charted_branches(brs, ident)], ["fix/1", "old-cache"])
        self.assertEqual(build_stats.charted_branches(None, ident), [])

    def test_stats_carries_the_toml_claims(self):
        """A chart.toml claim with measured = true and a sha passes through claims() into the committed stats.json."""
        import json
        from data import load_chart_toml, STATS_PATH
        cfg = load_chart_toml()
        if not (cfg.get("claims") or {}).get("scrape_interval"):
            self.skipTest("no chart.toml claims")
        want = claims(cfg)
        self.assertTrue(upright_ok(want["scrape_interval"]))
        with open(STATS_PATH, encoding="utf-8") as fh:
            got = json.load(fh).get("claims") or {}
        self.assertEqual(got, want)

    def test_claims_default_never_upright(self):
        for cid, cl in claims({}).items():
            self.assertFalse(cl["measured"], cid)
            self.assertFalse(upright_ok(cl))
        ok = claims({"claims": {"workers": {"value": "512", "unit": "permits", "source": "x", "sha": "abc", "measured": True}}})
        self.assertTrue(upright_ok(ok["workers"]))
        no_sha = claims({"claims": {"workers": {"value": "512", "source": "x", "measured": True}}})
        self.assertFalse(no_sha["workers"]["measured"])


class LogSim(unittest.TestCase):
    def setUp(self):
        self.log = logsim.default_log("0.1.3", "2026-10-07")

    def test_arithmetic(self):
        p = self.log["profile"]
        self.assertEqual(logsim.rate_of(p), 2.0)
        self.assertIsNone(logsim.in_flight(p))                              # v9.2: no p95 in the settings, no Little's law
        self.assertEqual(logsim.in_flight({**p, "p95_fetch_ms": 812}), 2)   # a measured p95 brings it back: 2 of 512
        self.assertEqual(logsim.wind(p), "")                                # no measured ratios: the sheet prints a dash
        self.assertEqual(logsim.wind({**p, "failed_ratio": 0.004}), "light")
        self.assertAlmostEqual(logsim.position(120, p), 230)                # 1405
        self.assertAlmostEqual(logsim.position(1620, p), 3230)              # 1430
        self.assertAlmostEqual(logsim.position(5, p), 2.5)                  # inside the ramp: r·t²/2·ramp
        self.assertEqual(logsim.position(10_000, p), 12440)                 # plateau
        self.assertEqual(logsim.t_complete(p), 6225)
        self.assertEqual(logsim.elapsed_label(6225), "1h 43m")
        self.assertEqual(logsim.hhmm("1403", 6225), "1546")

    def test_rows(self):
        rows = logsim.simulate(self.log["profile"], self.log["entries"], 1, "1403")
        by = {(r.time, r.kind): r for r in rows}
        self.assertEqual(by[("1405", "health")].log, 230)
        self.assertEqual(by[("1405", "health")].text, "fetched 230 · 512 permits")   # v9.2: settings only
        for word in ("p95", "fsync", "failed", "timeout", " of 512"):
            self.assertNotIn(word, by[("1405", "health")].text)
        self.assertIsNone(by[("1405", "health")].wind)
        self.assertEqual(by[("1546", "out")].log, 12440)
        self.assertEqual(by[("1546", "out")].speed, 0.0)
        self.assertEqual(by[("1546", "out")].text, "crawl complete · plateau · 12,440 urls")   # no elapsed time
        self.assertNotIn("1h 43m", " ".join(r.text for r in rows))
        self.assertIsNone(by[("1402", "cmd")].log)
        self.assertIn("frontier 8 shards", by[("1403", "out")].text)
        logs = [r.log for r in rows if r.log is not None]
        self.assertEqual(logs, sorted(logs))

    def test_rate_cap_per_host(self):
        p = {**self.log["profile"], "rate_rps": 50}
        self.assertEqual(logsim.rate_of(p, hosts=1), 2.0)
        self.assertEqual(logsim.rate_of(p, hosts=3), 6.0)

    def test_check_log_accepts_default(self):
        self.assertEqual(logsim.check_log(self.log), [])
        self.assertEqual(model.schema_errors(self.log, model.load_schema(model.LOG_SCHEMA_PATH)), [])

    def test_check_log_rejects_v8(self):
        v8 = copy.deepcopy(self.log)
        v8.update({"source": "session", "measured": True, "target": "example.com"})
        v8["profile"]["rate_rps"] = 2.0
        v8["entries"] = [
            {"time": "1403", "kind": "crawl", "text": "rustmapper crawl --start-url example.com --workers 512", "log": 0, "speed": 0},
            {"time": "1404", "kind": "out", "text": "crawl under way · 512 in flight", "log": 48213, "speed": 203},
            {"time": "1405", "kind": "remark", "text": "remarks · nothing to report", "log": 48213, "speed": 203},
        ]
        errs = logsim.check_log(v8)
        self.assertTrue(any("example.com" in e for e in errs))
        self.assertTrue(any("Δposition" in e for e in errs))
        self.assertTrue(any("speed" in e for e in errs))

    def test_check_log_rules(self):
        bad = copy.deepcopy(self.log); bad["measured"] = True
        self.assertTrue(any("computed cannot be measured" in e for e in logsim.check_log(bad)))
        bad = copy.deepcopy(self.log); bad["source"] = "session"; bad["measured"] = True
        self.assertTrue(any("no stored log" in e for e in logsim.check_log(bad)))
        bad = copy.deepcopy(self.log); bad["entries"][4]["log"] = 230
        self.assertTrue(any("stores numbers while measured:false" in e for e in logsim.check_log(bad)))
        bad = copy.deepcopy(self.log); bad["entries"] = bad["entries"] + [{"time": "+1m", "kind": "out", "text": "x"}]
        self.assertTrue(any("entries" in e for e in logsim.check_log(bad)))
        bad = copy.deepcopy(self.log); bad["machine"]["cores"] = 4
        self.assertTrue(any("decision 14" in e for e in logsim.check_log(bad)))
        bad = copy.deepcopy(self.log); bad["profile"]["rate_rps"] = 5
        self.assertTrue(any("rate_rps" in e for e in logsim.check_log(bad)))

    def test_measured_session_accepted(self):
        s = copy.deepcopy(self.log)
        s.update({"source": "session", "measured": True})
        s["entries"] = [
            {"time": "1403", "kind": "crawl", "text": "rustmapper crawl --start-url http://127.0.0.1:8080"},
            {"time": "1405", "kind": "health", "text": "fetched 230", "log": 230, "speed": 1.9, "wind": "calm"},
            {"time": "1430", "kind": "remark", "text": "nothing to report", "log": 3100, "speed": 1.9, "wind": "calm"},
        ]
        self.assertEqual(logsim.check_log(s), [])


class Plugins(unittest.TestCase):
    def test_checks_run_on_fixture(self):
        from checks import data as cdata, log as clog
        ctx = {"stats": fixture_stats(), "today": TAKEN, "log": logsim.default_log("0.1.3", "2026-10-07")}
        fails = [f for f in cdata.check(ctx) if f.level == "fail"]
        self.assertEqual(fails, [])
        self.assertEqual([f for f in clog.check(ctx) if f.level == "fail"], [])

    def test_committed_assets_if_present(self):
        from data import STATS_PATH, LOG_PATH
        if not (os.path.exists(STATS_PATH) and os.path.exists(LOG_PATH)):
            self.skipTest("assets not built")
        with open(STATS_PATH, encoding="utf-8") as fh:
            stats = json.load(fh)
        if stats.get("schema") != 2:
            self.skipTest("stats.json is not v2 yet")
        taken = dt.date.fromisoformat(stats["taken"])
        self.assertEqual(model.validate(stats, today=taken), [])
        self.assertNotIn("seeded", stats)
        with open(LOG_PATH, encoding="utf-8") as fh:
            self.assertEqual(logsim.check_log(json.load(fh)), [])


if __name__ == "__main__":
    unittest.main()


class LivePath(unittest.TestCase):
    """The first live run on GitHub failed: derive() adds `calendar_check` when a GraphQL calendar is present,
    and the schema rejected it. Re-derive the committed stats with a synthetic calendar and validate."""

    def test_live_calendar_model_validates(self):
        import copy
        import datetime as dt
        import json
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
        from data import derive as derive_mod, model
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "stats.json"),
                  encoding="utf-8") as fh:
            stats = json.load(fh)
        calendar = [{"start": w["start"], "n": w["n"] + (1 if i % 7 == 0 else 0)} for i, w in enumerate(stats["weeks"])]
        live = copy.deepcopy(stats)
        live.update(derive_mod.derive(stats["repos"], dt.date.fromisoformat(stats["taken"]), calendar))
        self.assertIn("calendar_check", live)
        self.assertEqual(set(live["calendar_check"]), {"clone", "calendar", "disagreement"})
        errors = model.validate(live, today=dt.date.fromisoformat(stats["taken"]))
        self.assertEqual(errors, [], "a live-mode model must validate against stats_schema.json")
