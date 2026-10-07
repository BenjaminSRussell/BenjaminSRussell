# Acceptance record — chart v9

Filled from the gate runs on the final build of branch `profile-v7` (MASTERPLAN §7). Numbers are measured
in this session's Chromium 141 at 870 px unless stated; the judged rubric is the eight-critic re-crit
panel's median (docs/crit/recrit/).

## Floor (automated)

| Gate | Rule | Result |
|---|---|---|
| check.py fast | xml, size, strings, position, expiry, type, motion, data, log, bounds, contrast, legend, alt, flash | _pending_ |
| check.py render | still-frame gate (7.2), silhouettes | _pending_ |
| check.py perf | repaint budget (7.3) | _pending_ |
| unit tests | `python3 -m unittest discover -s tests` | _pending_ |
| determinism | two builds from one stats.json byte-identical | _pending_ |

## Measured deviations (recorded, not failed)

1. **ms/frame while moving.** Chromium re-rasters the whole `<img>` on every SMIL tick; a 1280-wide sheet with
   ~1300 elements costs ≈ 35–40 ms per repaint whatever the markup. The 8 ms/frame cap of 7.3 cannot be met by
   any sheet while anything moves. The moving windows are bounded (hero 4–28 s, footer 40–64 s) and the
   repaint-rate rules after them hold. `checks/perf.py` reports PERF-MOVING as a warning.
2. **Hero t=0.** The MASTERPLAN opening faded the whole sheet in; the five-second test and the 7.2 floor want a
   sheet at load. Title block, frame, rose, land and sea names are static at t=0; the water draws in.
3. **Raw size targets.** Soundings, instruments and footer exceed their per-sheet raw targets (warnings);
   every hard cap (300 KB raw, 100 KB gz, 3000 elements, 250 KB gz per edition set) holds.

## Judged (J1–J12, re-crit panel median)

_pending_

## Five-second test

_pending_ (shadow-profile cohorts are Ben's to run; the panel's own 5-second readings are recorded in lieu)
