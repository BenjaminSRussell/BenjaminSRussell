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
    return {
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
    H = 226
    b = []
    b.append(f'<circle cx="52" cy="46" r="3.5" fill="{t.accent}"/>')
    b.append(k.text("BY THE NUMBERS", 66, 50, MONO, 12.5, t.ink2, tracking=1.6))
    note = f"refreshed daily by actions · {s['updated']}" + ("  ·  seeded, first refresh pending" if s.get("seeded") else "")
    b.append(k.text(note.upper(), W - 48, 50, MONO, 12, t.muted, anchor="end", tracking=1.4))
    b.append(f'<path d="M48,64 H{W-48}" stroke="{t.hair}"/>')

    cells = [
        (fmt(s["commits"]), "lifetime commits"),
        (fmt(s["repos"]), "public repos"),
        (fmt(s["followers"]), "followers"),
        (fmt(s["stars"]), "stars earned") if s.get("stars", 0) >= 5 else (str(len(s["languages"])), "languages in play"),
        (s["since"], "on github since"),
    ]
    cw = (W - 96) / len(cells)
    for i, (big, cap) in enumerate(cells):
        x = 48 + i * cw
        b.append(k.text(big, x, 118, "display-semi", 42, t.ink, tracking=-1.6))
        b.append(k.text(cap.upper(), x + 1, 141, MONO, 12, t.muted, tracking=1.4))
        if i:
            b.append(f'<path d="M{x-24},84 V144" stroke="{t.hair}"/>')

    # language bar
    y = 174
    x = 48
    total_w = W - 96
    cols = [t.accent, t.ink, t.ink2, t.muted, t.soft, t.hair]  # tonal ramp, not a category palette
    b.append(f'<rect x="{x}" y="{y}" width="{total_w}" height="8" rx="4" fill="{t.hair}"/>')
    gap = 3
    lx = x
    legend = []
    for i, lang in enumerate(s["languages"]):
        w = max(total_w * lang["share"] - gap, 2)
        col = cols[i % len(cols)]
        b.append(f'<rect x="{lx:.1f}" y="{y}" width="{w:.1f}" height="8" rx="4" fill="{col}">'
                 f'<animate attributeName="width" values="0;{w:.1f}" dur="1.4s" begin="{i*0.12:.2f}s" fill="freeze"/></rect>')
        legend.append((lang["name"], f"{round(lang['share']*100)}%", col))
        lx += w + gap
    tx = x
    for name, pct, col in legend:
        b.append(f'<rect x="{tx:.1f}" y="195" width="9" height="9" rx="2" fill="{col}"/>')
        b.append(k.text(name, tx + 15, 204, "text-medium", 13.5, t.ink2))
        tx += k.text_width(name, "text-medium", 13.5) + 20
        b.append(k.text(pct, tx, 204, MONO, 12, t.muted))
        tx += k.text_width(pct, MONO, 12) + 28
    label = f"{fmt(s['commits'])} commits, {s['repos']} public repos, {s['followers']} followers, on GitHub since {s['since']}"
    return k.svg(W, H, "".join(b), label)


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
    for t in k.THEMES:
        k.begin_asset()
        out = render(t, stats)
        for problem in k.check_bounds(W):
            print("WARNING stats:", problem)
        k.write(os.path.join(ROOT, "assets", f"stats-{t.name}.svg"), out)


if __name__ == "__main__":
    main()
