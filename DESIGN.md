# Design System — BenjaminSRussell Profile

Internal craft notes. Not for the profile face.

## Principles

1. **Beauty and clarity win.** Whitespace is a feature. Each cool thing gets its own stage.
2. **Show, don't tell.** Almost no prose. Geometry, rhythm, and sparse live signal carry meaning.
3. **Hand-authored, seed-fingerprinted geometry.** SVGs are drawn for this profile. Positions and curves derive from a personal seed so the field is unique — quietly, not as a tech demo.
4. **Verified hosts only.** skillicons, profile-summary-cards (radical), github-readme-stats-one-bice, streak-stats.demolab, socialify.git.ci, raw snake, komarev ghpvc, typing-svg. Never primary github-readme-stats.vercel.app, never activity-graph, never trophies.
5. **Refined luxury tech.** Void / deep blacks, violet `#7C3AED`, cyan `#22D3EE`, mist `#A78BFA`, bone `#E8E4DF`. Soft glow, not neon overload.

## Signature seed

```
SEED_STRING = "BenjaminSRussell"
SEED_DIGEST = SHA-256(SEED_STRING) hex
SEED_HEX    = DIGEST[:8] → EC8AC918
SEED_U64    = int(DIGEST[:16], 16)
```

PRNG: xorshift64* forked per asset (`hero`, `flow`, `constellation`, `sigil`) via XOR salts.
Controls: node xy, radii, pulse delays, bezier control offsets, flow arc amplitude, sigil satellite angles.

Documented in every SVG HTML comment and in `assets/design-tokens.json`.
Regenerate: `python3 gen_assets.py` (bit-identical for a given seed).

**Anti-replication (quiet):** Pasting the README into a chatbot will not reproduce the feel — the soul lives in committed SVG math keyed to Ben's name hash. Uniqueness is a fingerprint, not a gimmick stack.

## Asset map

| Asset | Role | Twin |
|-------|------|------|
| `hero.svg` | Full-width identity + seeded node field | `hero-light.svg` |
| `sigil.svg` | BR data-node monogram (footer accent) | `sigil-light.svg` |
| `flow.svg` | Thin connector / breath between stages | `flow-light.svg` |
| `constellation.svg` | Glyph-labeled project plane + flowing edges | `constellation-light.svg` |
| `label-*.svg` | Section marks (FIELD / MOTION / ARCHIVE) | `*-light.svg` |
| `frame.svg` / `footer.svg` | Quiet rules | light twins |
| `glyph-*.svg` | `<details>` summary icons | — |
| `design-tokens.json` | Colors, spacing, seed meta | — |

**Not shipping (culled for air):** `hud.svg`, `noise-field.svg`, diff/ANSI panels, triple-nested details, duplicate metric stacks.

## Open-view recipe (scan in ~5s)

1. Hero → spacer  
2. Short typing line  
3. Stats + streak pair (~46% / gap / 46%)  
4. Flow divider  
5. Constellation + 2 featured socialify cards  
6. Snake alone (MOTION)  
7. Compact skillicons  
8. Sigil + footer + views  

Extras (more repos, mermaid, secondary cards) live inside collapsed `<details>`.

## Motion

SMIL only (GitHub-safe): node pulse ~5.2s, edge dash travel ~6.4s, field drift ~22s, gradient shift ~14s. Subtle. Breathing.

## Roadmap

| Phase | Focus |
|-------|--------|
| **v1 craft** (now · 1.2.0) | Seeded custom SVGs, dark/light twins, airy README, verified embeds |
| **v2 metrics actions** | Optional GitHub Action to refresh a single local metrics SVG; still no widget collage |
| **v3 generative seasons** | Seasonal palette shifts from the same seed (winter mist, summer cyan) — one regen, same geometry |

## Signature

`BSR⋄DP⋄1.2.0` — BenjaminSRussell · Data Plane · seed `EC8AC918`
