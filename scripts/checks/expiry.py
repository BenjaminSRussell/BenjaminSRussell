"""expiry — copy with a review date that has passed (T10 check 16): a warning, never a fail.

`[copy.review] key = "YYYY-MM"` (or "YYYY-MM-DD") means "re-read [copy] key by then"."""
from __future__ import annotations

import datetime as dt
import re

from check import Finding, warn

TIER = "fast"
_DATE = re.compile(r"^(\d{4})-(\d{2})(?:-(\d{2}))?$")


def parse(s: str) -> dt.date | None:
    m = _DATE.match(str(s).strip())
    if not m:
        return None
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3) or 1)
    try:
        if m.group(3):
            return dt.date(y, mo, d)
        # "YYYY-MM" expires at the end of that month
        nxt = dt.date(y + (mo // 12), mo % 12 + 1, 1)
        return nxt - dt.timedelta(days=1)
    except ValueError:
        return None


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    review = ctx.cfg.get("copy", {}).get("review", {})
    copy = ctx.cfg.get("copy", {})
    for key, when in (review.items() if isinstance(review, dict) else []):
        d = parse(when)
        if d is None:
            out.append(warn("EXPIRY-FORMAT", f"[copy.review] {key} = {when!r} is not YYYY-MM or YYYY-MM-DD"))
            continue
        if key not in copy:
            out.append(warn("EXPIRY-KEY", f"[copy.review] {key} names no [copy] key"))
        if d < ctx.today:
            out.append(warn("EXPIRY-PASSED", f"[copy] {key} was due for review by {when}: re-read it ({copy.get(key, '')!r})"))
    return out
