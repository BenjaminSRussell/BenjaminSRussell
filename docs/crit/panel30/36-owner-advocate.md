# 36 — The owner's advocate (Ben in 2028)

I have to live with this page: change a word, add a repo, notice a red morning job, explain the build to a stranger. I read DESIGN.md, the four build scripts, profile.yml, README.draft.md, the specs, stats.json and the hero render; I build on 21 (SRE) and 23 (maintainer) rather than repeat them.

## What is good

- **The v9 skeleton is the right shape.** One module per sheet, `build(theme, data)`, data loaded once from `stats.json`, `check_bounds` on every sheet, glyphs as `<use>`. `common.py` puts the honesty convention in code (`measured()` / `illustrative()`), so the rule lives in one place.
- **Where failure was thought about, it fails the right way:** `pypi_edition()` returns `None` and the cached edition stays; no token means "re-render from cache". Blobless bare clones are the cheapest honest source of per-repo history.

## What is bad, ranked

1. **As committed, the pipeline redraws nothing.** `SHEETS` lists six modules; `scripts/sheets/` has only `common.py` and `_v8_reference.py`. Every run prints "(no module yet)", `render_all` calls it with `check=False`, and the workflow commits `assets/*.svg` anyway while the colophon says "redrawn nightly". A green tick that means nothing is the owner's worst failure.
2. **`repos` means two things.** `fetch()` sets `stats["repos"] = 24` (int); `fetch_repodata.main()` writes a *list* under the same key to the file on disk while `build_stats` holds another dict in memory and merges three keys back by hand. If the clone step fails (caught, printed), `for r in stats.get("repos", [])` iterates an int and the job dies later with a TypeError. The committed cache still says `"seeded": true`.
3. **The archipelago is not stable under the operations that will happen.** Slots are keyed by repo *name*; `go_go_go` is force-placed because the course sights it. Rename `Rust-sitemap` to `rustmapper` (23's own ask) and the shoal drops to a rank slot and the sea rearranges overnight. A hung clone (180 s timeout × 24 repos in a 10-minute job) silently drops a repo and an island vanishes for a day.
4. **The chart draws itself growing.** The profile repo is the fourth-largest island (169 commits) and the bot adds a commit a day to it. And 14 regenerated SVGs are ~1.4 MB of churn a day on `main`; path data deltas badly, so the repo a reader clones fills with yesterday's contours.
5. **Copy is buried in the generator, and the frozen numbers are plural.** v8: `cap(t, "Chart No. 27 · The open web · Soundings in rows", 72, 76, 11, t.ink2)`: copy, coordinate and size in one call, 466 lines of them. "CORRECTED THROUGH NOTICE 5" is specified on hero, footer, alt text and prose; "lately in Rust", "Oct 2024", `Wk 'YY`, `rustmapper-0.1.3` in the log and `design-tokens.json` at `8.0.0` with v8 sheet names all expire. The `svg()` header still says "v7".
6. **No kill switch for motion** and nothing honours `prefers-reduced-motion`.
7. **Docs and harness lag a release.** DESIGN.md describes rhumb lines, the sweeping beam and `snake.yml`, with no "how to change X". Nothing parses the XML, enforces 300 KB or greps banned words; the `.preview/` PNGs came from tooling not in the repo. The commit clock uses `%at` (UTC), so the VAR note names the wrong hour in his own timezone.

## What needs to be done

- **F1 Honest job.** `build_assets.py` exits non-zero on a missing module or a bounds warning; `render_all` uses `check=True`; the workflow fails rather than commits. Add `concurrency: {group: soundings, cancel-in-progress: true}` and `git pull --rebase` before push (cron and the `scripts/**` push trigger can overlap). Pin `fonttools` in `scripts/requirements.txt`.
- **F2 One data model.** `survey()` returns dicts; `build_stats` merges in memory and writes once. Rename: `repo_count`, `repos` (list), and choose between `commits` (1,828, GraphQL) and `commits_surveyed` (1,868) for the hero figure, naming the source in the legend. Validate against a schema; on failure render from cache with 21's pencil note.
- **F3 Stable layout.** Slots keyed by `chart.toml`: `[[features]] repo="Rust-sitemap" aliases=["rustmapper"] slot="named-5"`. Commit `assets/layout.lock.json` (feature → centre, radius); the build warns when a centre moves > 40 px, so a rename or dropped clone is a readable diff, not a rearranged sea. A repo that fails to clone keeps yesterday's record with `stale: true`.
- **F4 Keep the chart out of the chart.** Exclude the profile repo and `github-actions[bot]` from the survey. Push generated SVGs to an orphan branch `chart` as one force-pushed commit (`raw.githubusercontent.com/.../chart/assets/...`); `main` stays small and human-authored.
- **F5 Copy out of code.** `chart.toml` holds every printed string: thesis, cartouche lines, pencil notes, alt texts, `position = ""` (empty omits the slot everywhere, no placeholder), and `[[notices]]` as the only source: README section rendered between `<!-- notices:start/end -->`, `N = len(notices)` fed to hero, footer and alt. A sixth notice is six lines of TOML. "Lately in Rust" and "Oct 2024" become fields or go.
- **F6 Motion switch.** `anim()/set_at()/draw_in()/flash()` return the end state under `MOTION=off`; the build also writes `*-still.svg`, served via `<source media="(prefers-reduced-motion: reduce)">`. Verify once on a scratch repo that GitHub's sanitizer keeps that `media` value: a ten-minute check, not an assumption.
- **F7 Five-second harness.** `scripts/check.py`, locally and as the CI gate before commit: XML parses; each file < 300 KB; zero hits for `ILLUSTRATIVE|PENDING|SEEDED`; `_EXTENTS` records size so semantic text < 13 px fails; layout-lock diff; stats schema. `scripts/preview.py` with `resvg` regenerates the crit PNGs, so the next review costs a command, not a session.
- **F8 Fix the clock.** `git log --date=iso-strict` and parse the author offset: busiest hour in his wall clock, still right if he moves.
- **F9 Docs.** DESIGN.md: pipeline diagram, motion table (CHANGELIST K), and a runbook: add / archive / rename a repo, change a line, add a notice, fill POSITION, turn motion off, what a red morning means. Delete the snake paragraph, Inter and DejaVu (23's F4); bump tokens; fix "v7".

## Improvements and high-level ideas

1. **Bold: the chart changes only when the world does.** With the lock file, aliased slots and the bot excluded, every visible change has a cause: islands grow by commits, a wreck appears when a repo is archived, a notice when a release ships (23's dispatch). No churn, only consequences.
2. **Weekly surveys, daily soundings.** Clone the 24 repos on Sundays; take the cheap GraphQL/PyPI soundings daily. Fewer failure modes, a 2 KB commit most days.
3. **Expiry dates on prose.** Each `chart.toml` string may carry `review = "2027-06"`; `check.py` warns when a line is past review. The joke that aged is caught before a recruiter finds it.

## What the page says about its maker

Now: someone who can design a system and ship its first version, but who is handing his future self a green tick that redraws nothing, a map that reshuffles on a rename, a repository that swells a megabyte a day, and copy spread across hundreds of coordinate calls. It should say: this person builds the operating layer first. The chart has a lock file, a schema, a still edition, a five-second check and a one-page runbook; Ben in 2028 edits a line of TOML, pushes, and the sheets redraw with no surprises. The generator becomes the proof of what the Notices claim.

## Five lines

1. The committed pipeline redraws nothing (no sheet modules, `check=False`, commit anyway): a missing module or bounds warning must fail the job; add `concurrency`, `pull --rebase`, pinned fonttools.
2. `repos` is an int in one function and a list in another, merged through the file on disk; a failed clone crashes the job later. One in-memory model with a schema; stale repos kept, not dropped.
3. Key feature slots by `chart.toml` aliases, not live names, and commit `layout.lock.json`: a rename or dropped clone surfaces as a readable diff, never as a rearranged sea.
4. Keep the chart out of the chart: exclude the profile repo and bot authors; push generated SVGs to an orphan `chart` branch so `main` stays small and human.
5. All copy, notices, `position` and the motion switch live in `chart.toml`; `N = len(notices)` everywhere; `MOTION=off` emits still editions behind `prefers-reduced-motion`; `scripts/check.py` is the five-second local test and the CI gate.
