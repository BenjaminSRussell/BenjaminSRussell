# Design — Steampunk plane

`BSR∴SP∴3.0.0` · seed `EC8AC918`

## Intent

Antique-mechanical. Calm. Connected. Cool and clean words.
Not neon cyberpunk. Not frantic HUD pulse.
Steam from valves serves the story: gather → clean → ship.

## Palette

| Token | Hex |
|-------|-----|
| walnut | `#1A120B` |
| soot | `#2C241C` |
| parchment | `#E8DCC8` |
| brass | `#B08D57` |
| copper | `#B87333` |
| amber | `#D4A574` |
| oxidized teal | `#5F7A6A` (quiet accent only) |

## Spine

1. Open — sigil + Ben + scrape → clean → ship  
2. Story — `story-flow.svg` (gather → clean → ship + steam)  
3. Rust-sitemap — hero + `act-rust-sitemap-flow.svg`  
4. Clean — `data-clean.svg` (L→R, steam works)  
5. Scrapy — hero  
6. Gallery — real project names in `<details>`  
7. Snake — brass crawl  
8. Close — footer  

## Motion

Slow only: gear rotate ~36–56s, steam drift ~14s, dial sweep ~18s.
Visible steam plumes from valves/pipes. No flicker. Walnut field (no white gaps).

## Actions failure playbook (badges / snake / score)

Workflows that keep the profile alive:

| Workflow | File | Purpose |
|----------|------|---------|
| Score commits | `.github/workflows/score-commits.yml` | Regenerates `assets/score-commits.svg` via GraphQL lifetime totals |
| Snake | `.github/workflows/snake.yml` | Publishes contribution snake to the `output` branch |
| Link check | `.github/workflows/links.yml` | Lychee shelf hrefs (weekly cron) |

### Manual re-run when badges go stale

1. Open **Actions** → pick the failed workflow → **Re-run all jobs**.
2. If GraphQL quota / Platane/snk flakes: wait ~1h and re-run once; do not hammer.
3. If `output` branch snake SVG 404s: re-run **Snake**, then hard-refresh the profile.
4. If score SVG is blank >7 days: the committed fallback `assets/score-commits-fallback.svg` is safe to point README at until Actions recovers.

### Stale-score fallback

`assets/score-commits-fallback.svg` is a static brass/parchment placeholder matching the steampunk field. Prefer the live Action artifact; swap the README `<img>` `src` to the fallback only when live generation has failed for >7 days.
