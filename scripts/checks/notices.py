"""notices — the working rules' dates are computed from git, and credit only his own code (round 6, review 2).

NOTICE-DATE (fail): a printed rule (the first three since review round 11) whose cite has a `{month:key}` with no anchor record, or whose
  anchor's first commit by an [identity] author was not found; or whose `date` in chart.toml is not the month of
  its first anchor. A month nobody computed is not printed as fact.
NOTICE-AUTHOR (fail): a printed rule whose anchor was first added by someone else (an agent, usually), unless the
  notice says so (`names_agent = true`, and the cite names the agent). Review round 6: an anchor scoped to his own
  commit (`author = "self"` in chart.toml, `scope: "self"` in its record) fails instead when no commit of his adds
  the text, or when the record was computed without that scope.
  Review round 8: also a body's `{days:…}` that could not be computed.
NOTICE-ANCHORS (fail): a printed rule with a cite and no anchors at all.
NOTICE-CITE (fail, review round 8): a printed cite not in the form "<repo>, <Mon YYYY>: <what>.".
"""
from __future__ import annotations

import re

from check import Finding, fail, info
from data import proof

TIER = "fast"
ON_PAGE = 3                     # review round 11: rules 1–3 (render_readme.NOTICES_ON_PAGE)
CITE_FORM = re.compile(r"[\w.-]+(?: [\w.-]+)*, (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}: \S.*\.")


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    stats = ctx.stats or {}
    rules = stats.get("rules") or []
    hand = sorted((n for n in (ctx.cfg or {}).get("notices", []) if isinstance(n, dict)), key=lambda n: n.get("n", 0))
    for nt in hand[:ON_PAGE]:
        n = int(nt.get("n") or 0)
        cite = str(nt.get("cite") or "")
        anchors = nt.get("anchors") or []
        if cite and not anchors:
            out.append(fail("NOTICE-ANCHORS", f"rule {n} has a cite and no anchors: its month would be typed", "chart.toml"))
            continue
        text, missing = proof.fill_cite(cite, n, rules)
        for key in missing:
            out.append(fail("NOTICE-DATE", f"rule {n}: no commit of his found for {{month:{key}}}", "stats.json rules"))
        _body, no_days = proof.fill_days(str(nt.get("body") or ""), n, rules)
        for ph in no_days:
            out.append(fail("NOTICE-DATE", f"rule {n}: {ph} was not computed (no commit, or no first commit)",
                            "stats.json rules"))
        recs = [r for r in rules if r.get("n") == n]
        first = next((r for r in recs if r.get("key") == (anchors[0] or {}).get("key")), None)
        if first and first.get("date") and str(nt.get("date") or "")[:7] != str(first["date"])[:7]:
            out.append(fail("NOTICE-DATE", f"rule {n}: chart.toml date {nt.get('date')} is not the computed "
                            f"{str(first['date'])[:7]}", "chart.toml"))
        scoped = {str(a.get("key")) for a in anchors if str(a.get("author") or "") == "self"}
        for r in recs:
            if str(r.get("key")) in scoped:
                if r.get("scope") != "self" or not r.get("found"):
                    out.append(fail("NOTICE-AUTHOR", f"rule {n}: {r.get('text')!r} in {r.get('repo')} is cited as his "
                                    "own commit, and no commit of his adding it was found", "stats.json rules"))
                continue
            if r.get("first_is_his") is False and not nt.get("names_agent"):
                out.append(fail("NOTICE-AUTHOR", f"rule {n}: {r.get('text')!r} in {r.get('repo')} was first added by "
                                f"{r.get('first_author')} ({r.get('first_sha')}); the cite credits him", "chart.toml"))
        if text and not CITE_FORM.fullmatch(text):
            out.append(fail("NOTICE-CITE", f"rule {n}: {text!r} is not \"<repo>, <Mon YYYY>: <what>.\"", "chart.toml"))
        if not missing:
            out.append(info("NOTICE-DATE", f"rule {n}: {text}"))
    return out
