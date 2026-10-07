<!-- The chart's review checklist (T10 §5). Delete lines that do not apply; keep the ones you checked. -->

## What changed

<!-- one or two sentences: which sheet, which key, why -->

## Checklist

- [ ] `python3 scripts/check.py` exits 0 locally; summary pasted below.
- [ ] Which `chart.toml` / `tokens.py` key changed; no hex colour or raw type size under `scripts/sheets/`.
- [ ] Every printed number has a `key` into stats.json or is set italic.
- [ ] New symbol → legend row on Sheet 3 → `symbol_defs` id.
- [ ] New motion: class declared in the sheet's timeline, no animated geometry attribute, no filter under it, loop period on the 1/4/10/15/96 s grid, base `opacity="0"` on frozen fade-ins.
- [ ] New text: role from `tokens.ROLES`, tier, rendered ≥ 9 px, collision-free (`check.py` bounds clean).
- [ ] Alt ≤ 25 words, first word not "The"; the alt poem re-read.
- [ ] Filmstrip and contact sheet attached (from the `perf` workflow artefact) when motion or layout changed.
- [ ] Goldens re-blessed only with a reason, written here.
- [ ] No banned phrase; "chart" ≤ 7 times in the README; no explained trick.
- [ ] `scripts/**` changed → the `perf` workflow (`check.py --release`) is green.
- [ ] README changed → `gh api /markdown -f mode=gfm -F text=@README.md` diffed against the previous run.

## check.py summary

```
<!-- paste -->
```
