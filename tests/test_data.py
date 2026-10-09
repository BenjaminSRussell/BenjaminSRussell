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
from data import github, tree  # noqa: E402
from data.survey import Commit, commit_days, is_ben, is_bot, parse_log, span_label, summarize, week_starts  # noqa: E402
import build_stats  # noqa: E402

TAKEN = dt.date(2026, 10, 7)
EST = dt.timezone(dt.timedelta(hours=-5))
EDT = dt.timezone(dt.timedelta(hours=-4))
BEN = ("Benjamin Russell", "benjamin.sheldon.russell@gmail.com")
BOT = ("google-labs-jules[bot]", "161369871+google-labs-jules[bot]@users.noreply.github.com")


def c(y, m, d, h, who=BEN, tz=EDT, subject="work", mi=0, parents=1, co=()) -> Commit:
    return Commit(f"{y}{m:02d}{d:02d}{h:02d}{mi:02d}", dt.datetime(y, m, d, h, mi, tzinfo=tz), who[0], who[1], subject,
                  parents, tuple(co))


def fixture_calendar() -> dict:
    """github.fetch()'s window block as the live run would carry it: commits per surveyed repo, plus the
    other contribution kinds that the green squares add up (never compared with the clones)."""
    return {"from": week_starts(TAKEN)[0].isoformat(), "to": TAKEN.isoformat(), "commits": 290, "issues": 930,
            "pull_requests": 40, "reviews": 3, "restricted": 0, "all": 1263,
            "commits_by_repo": {"steady": 100, "sprint": 190, "ghost": 0}, "commits_elsewhere": 0}


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
          "calendar_weeks": None, "calendar": fixture_calendar(),
          "languages": [{"name": "Python", "share": 1.0, "bytes": 10}]}
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
        self.assertEqual((r["merges"], r["coauthored"]), (0, {"count": 0, "share": 0.0, "agent": 0, "names": {}}))
        self.assertEqual((r["tests"], r["workflows"], r["manifest"], r["lines"]), (None, None, None, None))

    def test_merges_and_co_authors_are_counted_not_reattributed(self):
        claude = ("Claude", "noreply@anthropic.com")
        commits = [c(2026, 3, 1, 10), c(2026, 3, 1, 11, parents=2, subject="Merge pull request #4"),
                   c(2026, 3, 2, 9, co=["Claude Sonnet 5 <noreply@anthropic.com>"]),
                   c(2026, 3, 2, 11, co=["Benjamin Russell <russell27sail@gmail.com>"]),   # GitHub's squash adds the PR author
                   c(2026, 3, 2, 10, who=claude, co=["Benjamin Russell <russell27sail@gmail.com>"])]
        r = summarize("r", commits, None, TAKEN)
        self.assertEqual(r["commits"], 4)              # the trailer naming Ben does not make Claude's commit his
        self.assertEqual(r["merges"], 1)
        self.assertEqual(r["coauthored"], {"count": 2, "share": 0.5, "agent": 1, "names": {"Claude Sonnet 5": 1}})
        self.assertEqual(r["others"], [{"name": "Claude", "commits": 1, "bot": True}])

    def test_first_and_last_are_the_authors_own(self):
        bot_only = [c(2025, 1, 1, 9, who=BOT), c(2026, 9, 9, 9, who=BOT)]
        r = summarize("bots", bot_only, None, TAKEN)
        self.assertEqual((r["commits"], r["first"], r["last"], r["span"]), (0, None, None, None))
        mixed = [c(2025, 1, 1, 9, who=BOT), c(2026, 2, 2, 9), c(2026, 9, 9, 9, who=BOT)]
        r = summarize("mixed", mixed, None, TAKEN)
        self.assertEqual((r["first"], r["last"]), ("2026-02-02", "2026-02-02"))

    def test_parse_log_records(self):
        out = ("a1\x1f2026-03-01T10:00:00-04:00\x1fBenjamin Russell\x1fbenjamin.sheldon.russell@gmail.com\x1fp1 p2\x1f"
               "Merge pull request #4\x1fClaude <noreply@anthropic.com>\x1dBen Russell <ben@users.noreply.github.com>\x1e\n"
               "b2\x1f2026-03-02T09:00:00-04:00\x1fBenjamin Russell\x1fbenjamin.sheldon.russell@gmail.com\x1fp1\x1fwork\x1f\x1e\n")
        cs = parse_log(out)
        self.assertEqual([x.sha for x in cs], ["a1", "b2"])
        self.assertEqual((cs[0].parents, cs[0].co_authors), (2, ("Claude <noreply@anthropic.com>", "Ben Russell <ben@users.noreply.github.com>")))
        self.assertEqual((cs[1].parents, cs[1].co_authors, cs[1].subject), (1, (), "work"))

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

    def test_sweep_days_are_named_not_removed(self):
        last = self.d["weeks"][-1]                         # 5–11 Oct 2026: only the 7 Oct sweep, one commit per repo
        self.assertEqual((last["n"], last["sweep"], last["days"]), (3, 3, 1))
        sweep_dates = {sw["date"] for sw in self.d["sweeps"]}     # threshold 2: the sprint's two Mondays are sweeps too
        on_sweeps = sum(d["n"] for r in self.recs for d in r["days"] if d["d"] in sweep_dates)
        self.assertEqual(sum(w["sweep"] for w in self.d["weeks"]), on_sweeps)
        hw = self.d["tide"]["hw"]                          # 5–11 Jan: Mon 5 Jan is 20 sprint + 2 steady of 142
        self.assertEqual(hw["sweep_share"], round(22 / 142, 3))
        self.assertEqual(sum(w["n"] for w in self.d["weeks"]), sum(sum(r["weeks"]) for r in self.recs))  # nothing removed
        self.assertEqual(self.d["merges"], 0)
        self.assertEqual(self.d["coauthored_total"], {"count": 0, "share": 0.0, "agent": 0, "names": {}})
        self.assertEqual(self.d["sweep_dates"], [sw["date"] for sw in self.d["sweeps"]])

    def test_months_first_last_without_sweeps(self):
        by = {r["name"]: r for r in self.d["repos"]}
        sweeps = set(self.d["sweep_dates"])
        self.assertIn("2026-10-07", sweeps)
        dormant = by["dormant"]      # 9 Nov 2025, 10 Nov 2025 (a Monday: steady's too, so a sweep at threshold 2), 7 Oct 2026
        self.assertEqual(dormant["months"], {"2025-11": 1})
        self.assertEqual((dormant["first_ns"], dormant["last_ns"]), ("2025-11-09", "2025-11-09"))
        self.assertEqual((dormant["first"], dormant["last"]), ("2025-11-09", "2026-10-07"))   # raw dates untouched
        for r in self.d["repos"]:
            self.assertEqual(sum(r["months"].values()), sum(1 for d in r["days"] if d["d"] not in sweeps))
        sprint = by["sprint"]
        self.assertEqual(sprint["months"], {"2026-01": 10 - 2})       # the two sprint Mondays are sweeps (threshold 2)
        self.assertEqual((sprint["first_ns"], sprint["last_ns"]), ("2026-01-04", "2026-01-13"))

    def test_calendar_check_compares_the_surveyed_repos_only(self):
        d = D.derive(self.recs, TAKEN, fixture_calendar())
        cc = d["calendar_check"]
        clone = sum(w["n"] for w in d["weeks"])
        self.assertEqual((cc["clone"], cc["calendar"]), (clone, 290))   # "ghost" is unsurveyed: not counted
        self.assertEqual(cc["disagreement"], round(abs(clone - 290) / 290, 3))
        self.assertEqual((cc["from"], cc["to"]), (week_starts(TAKEN)[0].isoformat(), "2026-10-07"))
        self.assertNotIn("calendar_check", D.derive(self.recs, TAKEN, None))
        self.assertNotIn("calendar_check", D.derive(self.recs, TAKEN, [{"start": "2026-10-05", "n": 9}]))  # the old list

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


class Instruments(unittest.TestCase):
    def test_cached_graphql_figures_need_a_dated_fetch(self):
        undated = {"schema": 2, "followers": 46, "stars": 0, "calendar_total": 1828, "account_since": "2024-10",
                   "languages": [{"name": "Python", "share": 0.46}], "provenance": {"graphql_at": None}}
        gh = build_stats.cache_fields(undated)
        self.assertIsNone(gh.get("calendar_total"))
        self.assertIsNone(gh.get("followers"))
        self.assertIsNone(gh.get("account_since"))
        self.assertEqual(gh["languages"], [])
        self.assertEqual(build_stats.cache_fields({"commits": 1828, "since": "Oct 2024", "seeded": True}).get("calendar_total"), None)
        dated = dict(undated, provenance={"graphql_at": "2026-10-08T06:20:00Z"}, calendar=fixture_calendar())
        gh = build_stats.cache_fields(dated)
        self.assertEqual((gh["calendar_total"], gh["followers"], gh["account_since"], gh["graphql_at"]),
                         (1828, 46, "2024-10", "2026-10-08T06:20:00Z"))
        self.assertEqual(gh["calendar"]["commits_by_repo"], {"steady": 100, "sprint": 190, "ghost": 0})
        self.assertEqual(build_stats.cache_fields({}), {})

    def test_fetch_itemises_the_window(self):
        calls = []

        def fake_gql(token, query, variables):
            calls.append((query, variables))
            if "createdAt" in query:
                return {"user": {"createdAt": "2024-10-03T00:00:00Z", "followers": {"totalCount": 46},
                                 "repositories": {"totalCount": 2, "nodes": [
                                     {"name": "steady", "stargazerCount": 1, "isArchived": False, "pushedAt": "2026-10-07T00:00:00Z",
                                      "createdAt": "2025-09-25T00:00:00Z", "primaryLanguage": {"name": "Python"},
                                      "languages": {"edges": [{"size": 10, "node": {"name": "Python"}}]}},
                                     {"name": "sprint", "stargazerCount": 0, "isArchived": False, "pushedAt": None, "createdAt": None,
                                      "primaryLanguage": None, "languages": {"edges": []}}]}}}
            if "totalIssueContributions" in query:
                return {"user": {"contributionsCollection": {
                    "totalCommitContributions": 300, "totalIssueContributions": 930, "totalPullRequestContributions": 40,
                    "totalPullRequestReviewContributions": 3, "restrictedContributionsCount": 7,
                    "contributionCalendar": {"totalContributions": 1280, "weeks": [
                        {"contributionDays": [{"contributionCount": 2, "date": "2025-10-12"}, {"contributionCount": 3, "date": "2025-10-13"}]},
                        {"contributionDays": []}]},
                    "commitContributionsByRepository": [
                        {"repository": {"name": "steady", "owner": {"login": "BenjaminSRussell"}, "isPrivate": False}, "contributions": {"totalCount": 100}},
                        {"repository": {"name": "sprint", "owner": {"login": "BenjaminSRussell"}, "isPrivate": False}, "contributions": {"totalCount": 190}},
                        {"repository": {"name": "secret", "owner": {"login": "BenjaminSRussell"}, "isPrivate": True}, "contributions": {"totalCount": 6}},
                        {"repository": {"name": "theirs", "owner": {"login": "someone"}, "isPrivate": False}, "contributions": {"totalCount": 4}}]}}}
            return {"user": {"contributionsCollection": {"totalCommitContributions": 500}}}

        lo = week_starts(TAKEN)[0]
        gh = github.fetch("t", "BenjaminSRussell", (lo, TAKEN), gql=fake_gql)
        cal = gh["calendar"]
        self.assertEqual((cal["from"], cal["to"]), (lo.isoformat(), "2026-10-07"))
        self.assertEqual((cal["commits"], cal["issues"], cal["pull_requests"], cal["reviews"], cal["restricted"], cal["all"]),
                         (300, 930, 40, 3, 7, 1280))
        self.assertEqual(cal["commits_by_repo"], {"steady": 100, "sprint": 190})   # private and others' repos stay out
        self.assertEqual(cal["commits_elsewhere"], 10)
        self.assertEqual(gh["calendar_weeks"], [{"start": "2025-10-12", "n": 5}])
        self.assertEqual(gh["calendar_total"], 500 * 3)                            # 2024, 2025, 2026
        self.assertEqual((gh["stars"], gh["repo_count"], gh["account_since"]), (1, 2, "2024-10-03"))
        window = next(v for q, v in calls if "totalIssueContributions" in q)
        self.assertEqual((window["from"], window["to"]), (f"{lo.isoformat()}T00:00:00Z", "2026-10-07T23:59:59Z"))

    def test_calendar_finding_names_what_is_compared(self):
        from checks import data as cdata
        s = fixture_stats()
        s["calendar_check"] = {"clone": 1894, "calendar": 1700, "disagreement": 0.114, "from": "2025-10-13", "to": "2026-10-07",
                               "basis": "x"}
        msgs = [f.msg for f in cdata.check({"stats": s, "today": TAKEN}) if f.code == "data.calendar"]
        self.assertEqual(len(msgs), 1)
        self.assertIn("surveyed repositories", msgs[0])
        self.assertIn("GitHub credits 1700", msgs[0])
        s["calendar_check"]["disagreement"] = 0.05
        self.assertEqual([f for f in cdata.check({"stats": s, "today": TAKEN}) if f.code == "data.calendar"], [])


class Tree(unittest.TestCase):
    CFG = {"exclude_dirs": tree.EXCLUDE_DIRS, "exclude": {"game_engine": ["src/engine"]}}

    def test_patterns_and_exclusions(self):
        paths = ["tests/test_a.py", "pkg/b_test.go", "web/c.test.ts", "Tests/DTests.swift", "tests/e.rs", "src/f.rs",
                 "node_modules/x/test_y.py", "conftest.py", ".github/workflows/ci.yml", ".github/workflows/cd.yaml",
                 ".github/workflows/README.md", "src/engine/test_gen.py"]
        self.assertEqual(tree.count_tests(paths, "r", self.CFG), 6)
        self.assertEqual(tree.count_tests(paths, "game_engine", self.CFG), 5)   # src/engine/test_gen.py is excluded there
        self.assertEqual(tree.count_workflows(paths), 2)
        self.assertTrue(tree.excluded("target/debug/a.rs", "r", self.CFG))
        self.assertFalse(tree.excluded("src/target.rs", "r", self.CFG))

    def test_manifest_parsers(self):
        self.assertEqual(tree.deps_from("Cargo.toml", '[package]\nname="x"\n[dependencies]\ntokio = { version = "1" }\nredb = "2"\n'
                                        '[dev-dependencies]\ncriterion = "0.5"\n'), ["tokio", "redb"])
        self.assertEqual(tree.deps_from("pyproject.toml", '[project]\nname="x"\ndependencies = ["scrapy>=2.11", "Delta-Lake[extra] ; python_version>\'3\'", "pyarrow"]\n'),
                         ["scrapy", "delta-lake", "pyarrow"])
        self.assertEqual(tree.deps_from("package.json", '{"dependencies": {"three": "^0.160", "lit": "3"}, "devDependencies": {"vite": "5"}}'),
                         ["three", "lit"])
        self.assertEqual(tree.deps_from("go.mod", "module m\n\ngo 1.22\n\nrequire (\n\tgithub.com/PuerkitoBio/goquery v1.9.2\n"
                                        "\tgithub.com/chromedp/chromedp v0.9.5\n\tgithub.com/x/y/v3 v3.0.1\n\tgolang.org/x/net v0.25.0 // indirect\n)\n"),
                         ["goquery", "chromedp", "y"])
        self.assertEqual(tree.deps_from("Package.swift", 'let p = Package(dependencies: [.package(url: "https://github.com/a/SwiftUIX.git", from: "1.0"),'
                                        ' .package(name: "Local", path: "../Local")])'), ["SwiftUIX", "Local"])
        self.assertEqual(tree.deps_from("Cargo.toml", "not = toml ["), [])

    def test_lines_by_language_from_a_real_repository(self):
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@x",
                   "PATH": os.environ.get("PATH", "")}
            subprocess.run(["git", "init", "-q", d], check=True, env=env)
            os.makedirs(os.path.join(d, "src", "engine")); os.makedirs(os.path.join(d, "node_modules", "x"))
            open(os.path.join(d, "main.py"), "w").write("a\nb\nc\n")
            open(os.path.join(d, "src", "lib.rs"), "w").write("fn main() {}\n// two")        # no final newline: 2 lines
            open(os.path.join(d, "src", "engine", "gen.c"), "w").write("x\n" * 50)
            open(os.path.join(d, "node_modules", "x", "i.js"), "w").write("y\n" * 9)
            open(os.path.join(d, "README.md"), "w").write("not code\n")
            open(os.path.join(d, "blob.py"), "wb").write(b"\x00\x01\n\n")
            open(os.path.join(d, "big.js"), "w").write("z\n" * 300000)                   # 600 KB: data, skipped
            subprocess.run(["git", "-C", d, "add", "-A"], check=True, env=env)
            subprocess.run(["git", "-C", d, "commit", "-q", "-m", "x"], check=True, env=env)
            git_dir = os.path.join(d, ".git")
            self.assertEqual(tree.lines_by_language(git_dir, "r", self.CFG), {"C": 50, "Python": 3, "Rust": 2})
            self.assertEqual(tree.lines_by_language(git_dir, "game_engine", self.CFG), {"Python": 3, "Rust": 2})
            facts = tree.tree_facts(git_dir, "r", self.CFG)
            self.assertEqual((facts["tests"], facts["workflows"], facts["manifest"]), (0, 0, None))
        self.assertIsNone(tree.lines_by_language("/nonexistent/.git", "r", self.CFG))

    def test_rest_runs_reads_main_push_runs(self):
        calls = []

        def fake_rest(path, token=None, timeout=20):
            calls.append(path)
            return {"workflow_runs": [
                {"name": "CI", "conclusion": "success", "updated_at": "2026-10-07T23:59:21Z", "html_url": "u1"},
                {"name": "CI", "conclusion": "failure", "updated_at": "2026-10-07T20:00:00Z", "html_url": "u2"}]}
        orig = github._rest
        github._rest = fake_rest
        try:
            ci = github.rest_runs("o", "r", None, "main")
            self.assertEqual(ci, {"workflow": "CI", "conclusion": "success", "date": "2026-10-07", "url": "u1",
                                  "recent": ["success", "failure"]})
            self.assertIn("branch=main&event=push&status=completed", calls[0])
            github._rest = lambda *a, **k: None
            self.assertIsNone(github.rest_runs("o", "r"))
            github._rest = lambda *a, **k: {"workflow_runs": []}
            self.assertIsNone(github.rest_runs("o", "r"))
        finally:
            github._rest = orig


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
        calendar = dict(fixture_calendar(), commits_by_repo={r["name"]: sum(r["weeks"]) + (i % 3) for i, r in enumerate(stats["repos"])})
        live = copy.deepcopy(stats)
        live["calendar"] = calendar
        live.update(derive_mod.derive(stats["repos"], dt.date.fromisoformat(stats["taken"]), calendar))
        self.assertIn("calendar_check", live)
        self.assertEqual(set(live["calendar_check"]), {"clone", "calendar", "disagreement", "from", "to", "basis"})
        errors = model.validate(live, today=dt.date.fromisoformat(stats["taken"]))
        self.assertEqual(errors, [], "a live-mode model must validate against stats_schema.json")
