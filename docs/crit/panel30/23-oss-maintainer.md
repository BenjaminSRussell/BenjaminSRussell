# Crit 23 — the open-source maintainer

Long-time maintainer (packaging, releases, triage); I judge a profile by whether the links survive the click. I read README.md, README.draft.md, BRIEF.md, STANDARDS/CHANGELIST, the specs and page-day-full.png, then did what a visitor does: opened PyPI's JSON, the Rust-sitemap and Scrapy repos via the public API, and the profile repo's workflows and fonts.

## What is good

- The nav line puts **rustmapper · Scrapy · PyPI · Email · Colophon** one click under the hero. The right five, plainly.
- The page is a reproducible build. `scripts/build_assets.py`, `build_stats.py`, DESIGN.md and vendored fonts *with their license texts* (`scripts/fonts/LICENSE-*.txt`) are committed. The daily Actions job already fetches the PyPI edition (`pypi_edition()` → `stats.json["edition"]` = 0.1.3, 2025‑11‑08, 4 releases). The plumbing for a real changelog exists; it just is not pointed at one.
- The draft's **Instruments** strip (mono columns, no badge chips) and the italic‑numeral convention are exactly how a maintainer wants claims presented: measured upright, estimated italic, no shields.io wallpaper.

## What is bad, ranked

1. **The links do not survive the click.** The one shipped artefact, rustmapper, from the outside: repo `Rust-sitemap` has **no LICENSE file** (API `license: null`) while pyproject declares `license = "MIT"` and `license-files = ["LICENSE"]`; **zero releases, zero tags**; description "This program runs a rust webscraper to create a sitemap that goes until it reaches end points "; no topics; 1 star; 14 open issues, all self‑filed; README with no CI badge, changelog or contributing note. On PyPI: **0.1.0 → 0.1.3 were all uploaded within 74 minutes on 2025‑11‑08** (a publishing‑debug burn, not a cadence) and nothing since, 11 months; the only wheel is `cp313-macosx_11_0_arm64` plus an sdist, so "the fast path is one `pip install rustmapper` away" is true on one platform and one Python version and compiles Rust from source everywhere else; the PyPI summary says **256 workers**, the page says **512**; `requires-python >= 3.8` with a wheel for 3.13 only. A maintainer reads this in ninety seconds and the chart's confidence becomes a liability.
2. **Scrapy shows 930 open issues on a 1‑star repo**, all opened by the owner as a task list. To a visitor that is either spam or abandoned triage. There is no `bug` label a real user could find.
3. **"Corrected through Notice 5" is currently fiction.** On a chart, Notices to Mariners are dated corrections with a source. The draft's Notices are five principles. Good copy, wrong document type. Two reviewers asked for a changelog; nobody checked whether anything exists to generate one from. Today: no releases, four PyPI uploads in one hour.
4. **"If you like it, borrow it" with no LICENSE in the profile repo.** Default copyright means nothing is borrowable. `scripts/fonts/` still carries unused Inter and DejaVu (v7 leftovers) next to the OFL files.
5. **The contribution invitation is in an HTML comment.** "corrections are welcome and will be entered as notices" is the best possible invite; nobody can see it.
6. **`snake.yml` still runs nightly** and pushes to `output` although the CHANGELIST kills the snake. Cron noise is how a maintainer spots neglect.
7. **Three names for one project** (repo `Rust-sitemap`, package `rustmapper`, binary `rust_sitemap`), and a 20‑repo shelf where fourteen have under 40 commits. The fold helps; the status does not. "Below the waterline" should mean something checkable (archived), not "less interesting".

## What needs to be done

- **F1 Release hygiene for Rust-sitemap (one afternoon, before the chart ships).** Add `LICENSE` (MIT, matching pyproject). Tag `v0.1.3` at the published commit and create a GitHub Release with notes. Set description and topics. Reconcile 256/512. Add `CHANGELOG.md` (Keep a Changelog) and a `release.yml` using `PyO3/maturin-action` with a wheel matrix (manylinux x86_64/aarch64, macOS arm64/x86_64, Windows) and **abi3** so one wheel per platform covers 3.8+. Then cut **0.2.0**, not 0.1.4: "fail‑closed robots" (2026‑10‑07) is a behaviour change; 0.x semver says minor bump. Rename the repo `rustmapper`; GitHub redirects.
- **F2 Make Notices to Mariners the generated changelog.** `build_stats.py` already has `contents: write` and the PyPI call. Add `GET /repos/{owner}/{repo}/releases?per_page=5` for Rust-sitemap and Scrapy; store `stats["notices"] = [{repo, tag, date, title}]`; render them in the README between `<!-- notices:start -->` / `<!-- notices:end -->` markers (the job already commits `assets/*`; add `README.md` to `git add`). "Corrected through Notice N" becomes `N = len(notices)`. Fallback until releases exist: PyPI versions with upload dates, which honestly prints "four notices, one day": the incentive to fix F1. Keep the five principles as **Sailing Directions**, the standing rules.
- **F3 Edition line always carries the date**: `EDITION 0.1.3 · 8 NOV 2025`, upright. Under rustmapper in the README, one plain sentence until wheels ship: "Prebuilt wheel for macOS arm64; elsewhere `pip` builds from source and needs a Rust toolchain."
- **F4 License the profile repo.** `LICENSE` = MIT for `scripts/`; add to the colophon: "Code MIT; sheets and copy CC BY 4.0; fonts under their own licenses in `scripts/fonts/`." Delete the unused Inter and DejaVu files. The OFL files stay; Reserved Font Names mean a borrower may not rename them.
- **F5 Visible invite, one line under Notices**: "Found a wrong depth? Open an issue on the repo it came from; corrections are entered as notices." A defined path with a real consequence is how you invite without begging.
- **F6 Delete `snake.yml`** and the `output` branch.
- **F7 Scrapy's tracker**: move the 930 self‑filed items to a GitHub Project or a `roadmap` milestone; keep `bug` and `good first issue` populated with three real items each.
- **F8 Below the waterline = archived.** Archive the four "Also" repos; `isArchived` is already fetched, so they become `Wk` wreck marks for free.

## Improvements and ideas

- **Bold: the release is the redraw.** A `repository_dispatch` from rustmapper's release workflow fires the profile's `daily soundings` job: the moment a version is published, the hero's edition changes and a new Notice appears. The Release notes end with "Chart redrawn: edition 0.2.0", linking back. A visitor who clicks PyPI → GitHub → profile sees the same version at every stop.
- **A pasteable quickstart.** The log sheet types `pip install rustmapper`, but nobody can copy from an SVG. Put a three‑line fenced block under the rustmapper bullets (`pip install rustmapper` / `rustmapper crawl --start-url …` / `rustmapper export-sitemap …`). The first command a visitor can run outranks any sheet.
- **"Three soundings wanted."** Label three real Rust-sitemap issues `good first issue` (the CT‑seeder fixtures, #42, is a natural one) and link them from the page as a small numbered list. Issues answered from strangers do not exist yet; this is the honest way to start them.
- **Borrow it as a template.** Mark the profile repo "Template repository" and add `chart.toml` (login, repos to name, palette) so a fork needs no code edits. Template forks become the first measurable trace of other humans.

## What the page says about its maker

Now: a solo builder with real taste and a strong voice whose only shipped package has the infrastructure of a first upload: no license file, no tag, four versions in an hour, one wheel, and a stale edition dressed in a confident cartouche. The design promises a maintainer; the repos deliver an experimenter. It should say: someone who labels an alpha as an alpha, ships on a cadence, keeps a changelog you can read on the chart itself, and licenses what he invites you to borrow. The metaphor suits a maintainer: a chart's whole value is that it is kept corrected.

## Five lines

1. Before the chart ships, fix rustmapper's shelf: add the missing LICENSE, tag and release v0.1.3, reconcile 256/512, publish a wheel matrix with abi3, then cut 0.2.0.
2. Generate Notices to Mariners from GitHub Releases in `build_stats.py` (markers in README, `N = len(notices)`); until releases exist it prints the ugly truth, which is the point.
3. Add a LICENSE to the profile repo (MIT code, CC BY 4.0 sheets and copy) or delete "borrow it"; remove the unused Inter/DejaVu fonts.
4. Edition line always dated; one plain sentence that `pip install` builds from source outside macOS arm64; a pasteable three‑line quickstart under rustmapper.
5. Scrapy's 930 self‑filed issues go to a Project; delete `snake.yml`; archive the four shelf repos so "below the waterline" is checkable.
