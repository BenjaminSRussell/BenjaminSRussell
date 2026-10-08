# Technical team brief — turn 36 critiques + 3 specs into ONE cohesive, buildable masterpiece plan

You are one of ten technical leads. Each of you owns a domain and writes ONE section of the
implementation plan to tech/<NN>-<domain>.md. An integrator then merges all ten into MASTERPLAN.md.
You are "working together": read your neighbours' domains below, name every interface you depend on
or provide (function signatures, data keys, file names, timing ids), and put them in a section headed
`## Interfaces` so the integrator can reconcile them. Where critics disagree, DECIDE, and say why in
one line. Everything must be honest (no invented facts), buildable under the constraints in BRIEF.md,
and consistent with STANDARDS.md unless you explicitly amend a standard (then say so).

## Read, in this order
1. BRIEF.md (facts, constraints), STANDARDS.md, CHANGELIST.md
2. The six first-panel critiques 01–06 (skim) and ALL thirty second-panel documents in panel30/
   (read the "five most important lines" of every one; read in full the ones in your domain)
3. spec-hero.md, spec-approaches.md, spec-supporting.md, README.draft.md
4. The code: /home/user/BenjaminSRussell/scripts/{svgkit.py, chartlib.py, build_assets.py,
   build_stats.py, fetch_repodata.py}, scripts/sheets/{common.py,_v8_reference.py},
   .github/workflows/profile.yml, assets/stats.json, DESIGN.md

## Verified facts that override earlier assumptions (from reviewers who cloned the repos)
- rustmapper worker count: page says 512, PyPI summary 256, repo README "32–512", governor.rs defaults
  min 256 / max 1024 adjusting every 250 ms on redb commit-latency EWMA. Shards = num_cpus, not 16.
  The WAL is Ben's own CRC32-framed rkyv log checkpointed into redb. Frontier rendezvous-hashes by
  registrable domain. Per-host politeness + robots crawl-delay honoured. fastbloom dedup.
- PyPI rustmapper 0.1.3: four releases within 74 minutes on 2025-11-08; only wheel is cp313 macOS
  arm64; elsewhere pip builds from source. No LICENSE file in the Rust-sitemap repo; no tags/releases.
- Scrapy (the platform): "90%+ coverage" is NOT enforced (fail_under=70, CI --cov-fail-under=0);
  circuit breakers wrap http/delta/redis services, not crawled hosts; rustmapper does NOT feed Scrapy
  (zero references); real strengths: typed Arrow schemas per table, schema_mode=merge, partition by
  domain, OPTIMIZE/VACUUM queue, URL-hash + MinHash dedup, BART-large-CNN summaries run locally.
  930 open self-filed issues; some commits authored by bots/"Claude".
- GitHub bio reads "Scraping enthusiast and full stack developer". Profile repo has no LICENSE.
- GitHub does NOT lazy-load README images: all sheets load at once, so one-shot openings below the
  hero finish before the reader scrolls there; lower sheets are seen in their frozen END state.
- Day-edition small text fails WCAG AA (muted 3.77:1, accent 3.77:1, green 3.49:1); night passes.
- Data caveats (per 08, 34): stats.json still says seeded:true and carries two commit totals (1,828 GraphQL
  for Ben; 1,868 surveyed across all authors incl. bots/co-authors) → filter by author in fetch_repodata;
  thirteen repos have last=2026-10-07 because Ben pushed a batch today (verified: Wheel's 16 commits are
  all his, same day), so "last" and hour histograms are skewed by batch days → use commit-DAYS per hour
  and author timezone offsets, not UTC instants; hero soundings and contours must derive from the same
  data (soundings generate the field), never two drawings of one noise field.
- Real data available now in assets/stats.json: 21 repos surveyed (commits, first/last, authors,
  hours, weekdays), edition 0.1.3 (2025-11-08). Weekly contributions arrive from GraphQL in Actions.

## Measured rendering facts (per 12, Chromium trace of SVG-in-<img>) — binding on T4/T6/T10
- One moving pixel re-rasters the WHOLE sheet; per-frame cost = sheet complexity (hero 18+3 ms/frame = 127% of a
  core for a 9px boat). After its opening, no sheet over 8 ms/frame may carry continuous animation. The footer
  (~3 ms/frame) is the one permitted ambient loop. Hero and Approaches loops must be change-only.
- Change-only invalidation exists only for `opacity` and `animateTransform`; `animateMotion` and geometry
  attributes (x, cx, width, y2) repaint every frame even while holding. Boats: animateTransform translate+rotate
  with `values` sampled from the path (or discrete dead-reckoning fixes every 2–4 s); lights: discrete opacity;
  cursor: discrete translate; crawl bar: transform not width.
- The SMIL clock runs offscreen: openings below the first viewport finish unseen. Only the hero gets an opening
  sequence; every other sheet is finished work at t=0 (or its opening is a deliberate long delay).
- Integer sheet coordinates: −23% gzip, −16% raster. No feGaussianBlur on anything that loops; gradient-circle halos.
  Graticule as a pattern. Opacity on leaves, not groups. CI gate: frozen sheets 0 repaints, lights ≤2 repaints/s,
  footer ≤4 ms/frame, plus a 360px DPR3 run (harness at scratchpad/perf/harness.js).
- Also binding: boat() is rigged backwards (31) — replace with the illustrator's 11-command sloop and 7-command glyph;
  pitch not heel for a profile boat; no rotate="auto". 21h UTC peak = 4–5pm author-local (32): count hours in author
  offset; never say "works at night". 17/21 repos have last=today (sweep day): dormancy rules must use commit-days.

## Domains (one per lead)
T1 Architecture & pipeline: module layout, data flow, Actions job, editions (day/night/phone/
   reduced-motion), caching, budgets, failure modes, kill switches, LICENSE, repo hygiene tasks for Ben.
T2 Hero sheet: final composition decisions (era, open title block vs cartouche, imprint outside the
   neat line, rose, archipelago algorithm from data, course, soundings encoding, unsurveyed margin,
   phone edition), reconciling spec-hero with panel findings (historian, color, printmaker, AD).
T3 Approaches sheet: geography = the pipeline but HONEST (rustmapper→Scrapy as a proposed channel
   until real), survey geometry from the real governor/shards, lateral marks, lights derived from
   real config, breaker as port traffic signal vs sector, insets, legend panel, basins = real tables.
T4 Motion engine: SMIL scheduler in svgkit (timeline ids, begin chains, easing, freeze), per-sheet
   choreography tables, still-frame guarantee, loop budget, reduced-motion edition generation.
T5 Type & lettering engine: type roles/scale (≥4 sizes), italic/upright semantics, slanted condensed
   soundings with subscripts, text-on-path for water names, tracking rules, accessibility floors,
   glyph budget, any additional OFL face decision.
T6 Chart drawing engine: contour intervals (chart-style, with figures in line breaks), tint bands as
   opaque OKLCH colours, coastline strokes, hatching as generated lines, line-weight system (4 weights),
   paper/plate texture within budget, seeded jitter, path compaction (relative integers), size targets.
T7 Data & honesty: exactly which numbers are measured vs illustrative and where each is set upright
   or italic; derivations (area ∝ sqrt commits; weekly tide; hour clock; variation + annual change;
   chart number; edition; notices from releases/commits); fallbacks that are never placeholders;
   liveness (updated_at, "last sounding"), build checks (contrast, lights>text, no PENDING strings,
   alt-text poem), what to ask Ben to fix in his repos (worker count, coverage gate, LICENSE, releases).
T8 Copy & IA: final README structure integrating the writer, poet, comedy writer, recruiter, UX,
   accessibility and brand findings: plain-text position/at-a-glance block, keyword presence, dual-
   register headings, alt ≤25 words plain + visible <sub> captions, cut list, the single thesis use,
   Notices as dated corrections with provenance (no explained callbacks), bio rewrite proposal, naming
   decisions (rustmapper as the vessel; "Scrapy Harbor" as the platform's name), LICENSE line.
T9 Supporting sheets: soundings/tide-table, ship's log (log.json schema; computed-consistent
   illustrative numbers OR a real run; measured flag; heartbeat line), instruments (plain-text stack
   mirror), footer (limit of survey; serpent with a witness; "Obstn rep." note; one boat).
T10 QA & verification: still-frame filmstrips, bounds, size, XML, contrast CI, CVD simulation,
   360px renders, GitHub-render verification (what to check after merge), a11y checklist, regression
   harness, review checklist for every future change, and the acceptance test for "masterpiece".

## Output format for your section (1200–2500 words)
1. Decisions (numbered; each one line + why; cite the critics by number, e.g. "per 13, 15").
2. Design/implementation detail: concrete, with coordinates/signatures/data keys where relevant.
3. Interfaces (what you provide / what you need from other domains, by T-number).
4. Build order and effort estimate (hours), risks, and what you deliberately leave out.
5. Acceptance criteria for your domain (testable).
