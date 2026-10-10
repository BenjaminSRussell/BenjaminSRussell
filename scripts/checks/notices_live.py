"""notices_live — a working rule's cite points at code that is still there (review round 7).

NOTICE-LIVE (fail): a printed rule (the first three since review round 11) whose anchor text is not in any file at the repository's HEAD
  outside its documentation (`rules[].at_head`, computed by scripts/data/proof.py `live_paths`), or whose record
  was computed without the check. Rule 1 used to cite `class CircuitBreaker` in `src/common/error_handling.py`
  (fd33c11), a class nothing called, deleted six days later; it now cites his per-host breakers (`_host_breakers`,
  099dd6c), which run. A rule may cite the month he started a practice although its first file was rebuilt later
  (rules 2 and 3: the Delta and Prometheus code of Oct 2025 was rewritten on 5 Oct 2025), so the check asks that
  the thing is in the code at HEAD, not that the first file survives.
"""
from __future__ import annotations

from check import Finding, fail

TIER = "fast"
ON_PAGE = 3     # review round 11: rules 1–3


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    rules = (ctx.stats or {}).get("rules") or []
    hand = sorted((n for n in (ctx.cfg or {}).get("notices", []) if isinstance(n, dict)), key=lambda n: n.get("n", 0))
    for nt in hand[:ON_PAGE]:
        n = int(nt.get("n") or 0)
        for r in (x for x in rules if x.get("n") == n):
            if r.get("at_head") is None:
                out.append(fail("NOTICE-LIVE", f"rule {n}: {r.get('text')!r} in {r.get('repo')} was not checked at HEAD",
                                "stats.json rules"))
            elif not r["at_head"]:
                out.append(fail("NOTICE-LIVE", f"rule {n}: {r.get('text')!r} is no longer in {r.get('repo')}'s code at "
                                "HEAD; the cite points at code that is gone", "stats.json rules"))
    return out
