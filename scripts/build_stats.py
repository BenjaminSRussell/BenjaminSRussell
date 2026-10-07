#!/usr/bin/env python3
"""Fetch live GitHub numbers and render assets/stats-{dark,light}.svg.

    GITHUB_TOKEN=... python3 scripts/build_stats.py     # fetch + render
    python3 scripts/build_stats.py                        # render from assets/stats.json

Runs daily from .github/workflows/profile.yml. With no token it re-renders the
last cached numbers so the design can be iterated offline.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
import svgkit as k  # noqa: E402
from svgkit import Theme  # noqa: E402

LOGIN = "BenjaminSRussell"
ROOT = os.path.join(os.path.dirname(__file__), "..")
CACHE = os.path.join(ROOT, "assets", "stats.json")
W = 1280
MONO = "mono"

QUERY_USER = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 8, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
  }
}"""
QUERY_TIDE = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { weeks { contributionDays { contributionCount } } }
    }
  }
}"""
QUERY_YEAR = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) { totalCommitContributions }
  }
}"""


def gql(token: str, query: str, variables: dict) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.load(r)
    if "errors" in out:
        raise RuntimeError(out["errors"])
    return out["data"]


def fetch(token: str) -> dict:
    u = gql(token, QUERY_USER, {"login": LOGIN})["user"]
    created = dt.datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    commits = 0
    for year in range(created.year, now.year + 1):
        d = gql(token, QUERY_YEAR, {"login": LOGIN, "from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"})
        commits += d["user"]["contributionsCollection"]["totalCommitContributions"]
    langs: dict[str, int] = {}
    stars = 0
    for repo in u["repositories"]["nodes"]:
        stars += repo["stargazerCount"]
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
    other = total - sum(v for _, v in top)
    languages = [{"name": n, "share": round(v / total, 4)} for n, v in top]
    if other > 0:
        languages.append({"name": "Other", "share": round(other / total, 4)})
    tide = gql(token, QUERY_TIDE, {"login": LOGIN})["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in tide]
    return {
        "weeks": weeks,
        "updated": now.strftime("%Y-%m-%d"),
        "since": created.strftime("%b %Y"),
        "commits": commits,
        "repos": u["repositories"]["totalCount"],
        "followers": u["followers"]["totalCount"],
        "stars": stars,
        "languages": languages,
        "seeded": False,
    }


def fmt(n: int) -> str:
    return f"{n:,}"


def render(t: Theme, s: dict) -> str:
    """Sheet 2 — Soundings. Figures set in Instrument Serif, a tide curve of the last 52 weeks."""
    import chartlib as c  # noqa: F401  (same drawing vocabulary as the other sheets)
    H = 268
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{t.paper}" stroke="{t.hair}"/>',
         f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="{t.ink}" stroke-width="0.9" stroke-opacity=".8"/>',
         f'<rect x="19" y="19" width="{W-38}" height="{H-38}" fill="none" stroke="{t.ink}" stroke-width="0.5" stroke-opacity=".6"/>']

    def cap(txt, x, y, size=10, fill=None, anchor="start", tracking=1.8):
        return k.text_use(txt.upper(), x, y, "plex", size, fill or t.muted, anchor=anchor, tracking=tracking)

    b.append(k.text("Soundings", 48, 70, "serif-italic", 30, t.ink))
    note = f"Sheet 2  ·  refreshed daily  ·  {s['updated']}" + ("  ·  seeded, first refresh pending" if s.get("seeded") else "")
    b.append(cap(note, W - 44, 66, 9.5, t.muted, anchor="end"))

    cells = [
        (fmt(s["commits"]), "lifetime commits"),
        (fmt(s["repos"]), "public repos"),
        (fmt(s["followers"]), "followers"),
        (fmt(s["stars"]), "stars earned") if s.get("stars", 0) >= 5 else (str(len(s["languages"])), "languages in play"),
        (s["since"], "on github since"),
    ]
    cw = 152
    for i, (big, capt) in enumerate(cells):
        x = 48 + i * cw
        b.append(k.text(big, x - 2, 150, "serif", 58, t.ink, tracking=-1))
        b.append(cap(capt, x, 174, 9.5, t.muted))
        if i:
            b.append(f'<line x1="{x-18}" y1="112" x2="{x-18}" y2="180" stroke="{t.ink}" stroke-width="0.6" stroke-opacity=".5"/>')

    # language mix as a depth scale (tonal ramp, one accent)
    y = 208
    x0, total_w = 48, 5 * cw - 22
    cols = [t.accent, t.ink, t.ink2, t.muted, t.soft, t.hair]
    b.append(f'<rect x="{x0}" y="{y}" width="{total_w}" height="6" fill="none" stroke="{t.ink}" stroke-width="0.6" stroke-opacity=".6"/>')
    lx = x0
    legend = []
    for i, lang in enumerate(s["languages"]):
        w = max(total_w * lang["share"], 2)
        col = cols[i % len(cols)]
        b.append(f'<rect x="{lx:.1f}" y="{y}" width="{w:.1f}" height="6" fill="{col}"/>')
        legend.append((lang["name"], f"{round(lang['share']*100)}%", col))
        lx += w
    tx = x0
    for name, pct, col in legend:
        b.append(f'<rect x="{tx:.1f}" y="226" width="7" height="7" fill="{col}"/>')
        b.append(k.text_use(name, tx + 12, 233, "plex", 10.5, t.ink2))
        tx += k.text_width(name, "plex", 10.5) + 16
        b.append(k.text_use(pct, tx, 233, "plex", 10, t.muted))
        tx += k.text_width(pct, "plex", 10) + 22

    # tide curve: contributions per week, last 52 weeks
    tx0, ty0, tw, th = 846, 96, 386, 96
    weeks = s.get("weeks") or []
    b.append(f'<line x1="{tx0}" y1="{ty0+th}" x2="{tx0+tw}" y2="{ty0+th}" stroke="{t.ink}" stroke-width="0.8" stroke-opacity=".7"/>')
    for i in range(0, 53, 13):
        xx = tx0 + tw * i / 52
        b.append(f'<line x1="{xx:.1f}" y1="{ty0+th}" x2="{xx:.1f}" y2="{ty0+th+5}" stroke="{t.ink}" stroke-width="0.8" stroke-opacity=".7"/>')
    if len(weeks) >= 8:
        hi = max(weeks) or 1
        pts = [(tx0 + tw * i / (len(weeks) - 1), ty0 + th - th * v / hi) for i, v in enumerate(weeks)]
        import chartlib as cl
        curve = cl.smooth_path(pts, False)
        area = curve + f" L{tx0+tw},{ty0+th} L{tx0},{ty0+th} Z"
        b.append(f'<path d="{area}" fill="{t.ink}" fill-opacity=".08"/>')
        b.append(f'<path d="{curve}" fill="none" stroke="{t.ink}" stroke-width="1.3"/>')
        hx, hy = max(pts, key=lambda p: -p[1])
        b.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="3" fill="{t.accent}"/>')
        b.append(cap(f"high water {hi}", min(hx + 8, tx0 + tw - 90), hy - 6, 8.5, t.accent))
        b.append(cap(f"contributions · last 52 weeks · {sum(weeks):,} total", tx0, ty0 + th + 22, 9, t.muted))
    else:
        b.append(f'<line x1="{tx0}" y1="{ty0+th-28}" x2="{tx0+tw}" y2="{ty0+th-28}" stroke="{t.ink}" stroke-width="0.8" stroke-dasharray="2 6" stroke-opacity=".5"/>')
        b.append(cap("tide table arrives with the first refresh", tx0, ty0 + th + 22, 9, t.muted))
    b.append(cap("52 wks ago", tx0, ty0 + th + 36, 8, t.muted))
    b.append(cap("now", tx0 + tw, ty0 + th + 36, 8, t.muted, anchor="end"))
    b.append(cap("tide", tx0, ty0 - 2, 9, t.ink2))

    label = f"{fmt(s['commits'])} commits, {s['repos']} public repos, {s['followers']} followers, on GitHub since {s['since']}"
    return k.svg(W, H, "".join(b), label, k.glyph_defs())


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        stats = fetch(token)
        with open(CACHE, "w", encoding="utf-8") as fh:
            json.dump(stats, fh, indent=2)
            fh.write("\n")
        print("fetched", stats)
    else:
        with open(CACHE, encoding="utf-8") as fh:
            stats = json.load(fh)
        print("no GITHUB_TOKEN; rendering cached", CACHE)
    for t in k.CHART_THEMES:
        k.begin_asset()
        out = render(t, stats)
        for problem in k.check_bounds(W, 30):
            print("WARNING soundings:", problem)
        k.write(os.path.join(ROOT, "assets", f"soundings-{t.name}.svg"), out)


if __name__ == "__main__":
    main()
