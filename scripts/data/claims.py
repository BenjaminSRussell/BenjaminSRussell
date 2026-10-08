"""claims — figures about the code (workers, shards, scrape interval) that are NOT measurements of Ben.

    claims(cfg=None) -> dict[id, {value, unit, source, sha, measured}]

Read from chart.toml `[claims.<id>]`. `measured` is true only when the toml says so AND a
`source` and `sha` are given; otherwise false, and the sheets set the figure italic. Nothing is
upright unless measured (MASTERPLAN decision 14: "512" is never upright). Without chart.toml the
defaults carry TECH-BRIEF's verified facts, all `measured:false`.
"""
from __future__ import annotations

from . import load_chart_toml

DEFAULTS: dict[str, dict] = {
    "workers": {"value": "256–1024", "unit": "permits", "source": "Rust-sitemap:src/governor.rs", "sha": None,
                "measured": False},
    "shards": {"value": "num_cpus", "unit": "shards", "source": "Rust-sitemap:src/frontier.rs", "sha": None,
               "measured": False},
    "scrape_interval": {"value": None, "unit": "s", "source": None, "sha": None, "measured": False},
}


def normalize(cid: str, raw: dict) -> dict:
    src = raw.get("source") or None
    sha = raw.get("sha") or None
    measured = bool(raw.get("measured")) and bool(src) and bool(sha)
    value = raw.get("value")
    return {"value": value if value not in ("",) else None, "unit": raw.get("unit") or None,
            "source": src, "sha": sha, "measured": measured}


def claims(cfg: dict | None = None) -> dict[str, dict]:
    cfg = load_chart_toml() if cfg is None else cfg
    sec = (cfg or {}).get("claims") or {}
    out = {cid: normalize(cid, dict(raw)) for cid, raw in DEFAULTS.items()}
    for cid, raw in sec.items():
        if isinstance(raw, dict):
            out[cid] = normalize(cid, raw)
    return out


def upright_ok(claim: dict) -> bool:
    """check 10: a claim may print upright only with measured:true and a source + sha."""
    return bool(claim.get("measured")) and bool(claim.get("source")) and bool(claim.get("sha"))
