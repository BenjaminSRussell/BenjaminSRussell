"""data — the measurements behind the chart (T7).

Modules: survey (bare clones → per-repo history), github (GraphQL / REST metadata), pypi (edition),
releases (notices), claims (chart.toml [claims.*]), derive (tide, variation, sweeps, …), model
(schema + validate), logsim (computed-consistent ship's log). One rule: a number is upright only
if the build can point at the measurement that produced it.
"""
from __future__ import annotations

import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ASSETS = os.path.join(ROOT, "assets")
STATS_PATH = os.path.join(ASSETS, "stats.json")
LOG_PATH = os.path.join(ASSETS, "log.json")
CHART_TOML = os.path.join(ROOT, "chart.toml")
LOGIN = "BenjaminSRussell"
USER_AGENT = "profile-stats (+https://github.com/BenjaminSRussell/BenjaminSRussell)"


def load_chart_toml(path: str = CHART_TOML) -> dict:
    """chart.toml as a dict, or {} when it is not there yet (T1 owns the file)."""
    try:
        import tomllib
        with open(path, "rb") as fh:
            return tomllib.load(fh)
    except (FileNotFoundError, ValueError):
        return {}
    except Exception:  # malformed toml: behave as absent, the T1 loader reports it
        return {}
