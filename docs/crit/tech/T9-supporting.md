# T9 — Supporting sheets: Soundings · Ship's log · Instruments · Limit of survey

Base: spec-supporting.md. Integer sheet px (per 12). T5 type roles: `label` 13 upright mono, `note` serif-italic 14–17 or rotated mono 13, `texture` 11 (soundings only). Italic numeral = illustrative, upright = measured, defined once on T3's legend. No sheet below the hero plays an opening at t=0 (per 12, 16, 11): each is finished work at load; the two remaining motions are delayed or ambient.

## 1. Decisions

1. **Soundings stays a sheet but stops being a stats card;** the five figures move to T8's plain-text block. Per 35, 18, 08.
2. **The small-multiples "fleet register" joins the Soundings sheet (1280×400), not a seventh sheet:** 21 per-repo 52-week sparklines on one shared y-scale under the tide. Per 08 (bold), 32; no new sheet per 33.
3. **No even-spread fallback; the build fails without `weeks`.** Tide = GitHub calendar weeks (upright) else the sum of `repos[].weeks` from clone timestamps (italic). Per 32, 08.
4. **HW labelled with its cause; typical-week median rule; baseline zero; monotone cubic curve.** Per 32, 08.
5. **Dateline, not slogan** (`SOUNDINGS TAKEN 7 OCT 2026 · 06:34 UTC · 21 REPOSITORIES`, from `updated_at`); footnote "Heights observed, not predicted." Per 32, 21, 25.
6. **Language bar deleted.** It keyed no mark and spent the accent. Per 08, 17.
7. **The log is a record:** every entry on paper at t=0, only the heartbeat line being entered (begins 30 s), the cursor the one loop; crawl bar and swaps cut. Per 35, 12, 16.
8. **Session computed-consistent** (position = ∫rate·dt, in-flight by Little's law), one host at 2 req/s over hours; example.com gone; `measured:true` flips it upright. Per 21, 22, 19.
9. **The log's own columns:** `TIME 1402 · LOG · URLS · SPEED · REQ/S · WIND · REMARKS`; "Log closed". WIND is host pushback in words. Per 26.
10. **Real health line with real metric names at 1405; heartbeat line appended by the daily job, upright.** Per 21.
11. **"Nothing on fire." in the same mono as every other remark.** Per 25.
12. **Instruments drawn at 800×290, hung `align="right" width="62%"`, mirrored in Markdown; groups LEAD · LOG · LOOKOUT; bold = fitted in a repository active this quarter (≥3 of the last 12 weeks).** Per 27, 18, 26, 32.
13. **Instruments and Soundings carry no motion.** Per 12, 27.
14. **The footer carries one line of prose;** mono caption and "Notice 5" leave it. Per 24, 25.
15. **Footer boat anchors at the limit line** (rode, anchor, `14 · good holding`); main luffs once; no rocking. Per 26, 31.
16. **Footer = hero's UNSURVEYED band in elevation** (same hatch id and "LIMIT OF SURVEY 2026") plus an index of adjoining sheets. Per 16, 27.
17. **Serpent gets a witness:** first rise `arrive.end+20s`, ripples 20 s, head-first; `Obstn rep. 2026 (PA)` where it rises; alt silent. Per 16, 31, 25.
18. **Footer is the one ambient loop (≤4 ms/frame); the approach is a one-shot delayed to 40 s.** Per 12.
19. **Phone editions static:** Soundings 720×360, Log 720×220, Instruments 720×48, Footer 720×320. Per 10.

## 2. Sheets

### A. Soundings — 1280×400, full bleed, no neat line

Paper only (no sheet stroke, per 27). Head baseline y=40: dateline `label` ink at (48,40); `CHART NO. {N} · SHEET 2` muted anchor end at (1232,40). Rule 0.8 at y=50, x=48..1232.

**Tide plot** x=48..1232, y=64..200; baseline y=200 = 0; HW at y=72 (full scale, no broken axis). Points x=48+i·1184/51. Curve `chartlib.monotone_path` (T6), PEN, ink; area fill `cool` .10 day / .12 night to baseline. **Typical week** = median of 52, dotted `1 4`, label `typical week {median}` muted anchor end (1228, y−4). **HW** ink dot r 3.5; label upright ink `HW {n} · wk of {d Mon} · {cause}`, cause = the repo contributing most to that week, with `, {span} days` when that repo's `last − first ≤ 14` (T2's sprint rule). **LW** hollow dot r 3 at the minimum non-trailing week; label muted `LW {n} · wk of {d Mon}`. **Slack water** bracket 0.6 at y=206 under the lowest rolling 4-week sum; label `slack water · {Mon}` centred. Month ticks 4 px at each first week of a month; letters `O N D J F M A M J J A S` muted at y=222.

**Fleet register** y=236..380: 7×3 cells 160×44 at x=48+c·169, y=236+r·48; repos by commits desc. Each: name label ink (underscores → spaces, ≤18 chars), commits upright anchor end (spot height), 52-week sparkline h=24 on the **shared** scale (max weekly count of any repo), 1.0 ink .8, hair baseline. game_engine reads as a spike, Scrapy as a year.

Foot baseline y=392: `Heights observed, not predicted.` serif-italic 17 ink2 at (48,392); muted label anchor end at (1232,392): `Source · git history of {N} public repositories · GitHub contribution calendar · author's commits only`.

Marking: calendar tide numerals upright, clone-sum italic, spot heights upright. Night: sparklines ink2, curve ink .85, no accent. Stale (`stale_days ≥ 2`): dateline keeps the last `updated_at`, baseline dashed, pencil note serif-italic 14 at (48,218) `no sounding taken {date}` (per 21).

Alt: "Tide table of weekly commits: high water {n}, week of {date}, {cause}; low water {n}; typical week {median}. Below, one 52-week line per repository."

Phone 720×360: dateline `{d MON YYYY} · {N} REPOS` 26; curve x=16..704, y=60..240; HW/LW labels 26 (`HW 290 · 4 Jan`); median rule unlabelled; no register; footnote serif-italic 30.

### B. Ship's log — 1280×490, ruled paper, no neat line

Stock: T6 token `paper_log` (one step warmer than chart paper), full bleed, no frame. Red margin 1 px accent .55 at x=104 (stationery; the sheet's only accent; `$` is ink plex-medium). Rules 0.8 hair at y=118+30k, k=0..11; the first drawn 1 px ink .6.

Header: `Log of the rustmapper` serif-italic 30 at (120,64); muted label anchor end (1236,60) `{target} · {version} · {d MON YYYY}`. Column heads baseline 100: `TIME` x=44 · `LOG · URLS` x=120 · `SPEED · REQ/S` x=250 · `WIND` x=340 · `REMARKS` x=470. Entries i=0..9 at baseline 140+30i: TIME mono 13 muted, no colon; LOG mono 14.5 anchor end x=226; SPEED anchor end x=318; WIND mono 13 muted x=340; REMARKS mono 14.5 ink x=470 (build asserts width ≤ 766). Sign-off baseline 440 anchor end (1236,440) serif-italic 18 ink2: `Log closed 1550 · B.S.R.` Heartbeat baseline 470, mono 14.5 upright: `0634 UTC · watch kept by cron · 1,828 commits · 21 repositories`.

Example session, computed from `profile` (1403:00 = t 0; log(t) = r·(t − ramp/2) after the ramp; in-flight = r × p95 = 1.6 → "2 of 512 permits"):

| TIME | LOG | SPEED | WIND | REMARKS |
|---|---|---|---|---|
| 1402 | — | — | — | `$ pip install rustmapper` |
| 1402 | — | — | — | `Successfully installed rustmapper-0.1.3` |
| 1403 | *0* | — | — | `$ rustmapper crawl --start-url http://127.0.0.1:8080 --workers 512` |
| 1403 | *0* | — | calm | `seeded · sitemap · 1 host · robots.txt read · delay 0.5 s · frontier 8 shards · wal on` |
| 1405 | *230* | *2.0* | calm | `fetched 230 · timeout 0% · failed 0.4% · p95 812 ms · wal fsync 3 ms · 2 of 512 permits` |
| 1430 | *3,230* | *2.0* | light | `remarks · nothing to report` |
| 1431 | *3,350* | *2.0* | light | `Nothing on fire.` |
| 1546 | *12,440* | *0* | calm | `crawl complete · plateau · 12,440 urls · 1h 44m` |
| 1548 | *12,440* | — | — | `$ rustmapper export-sitemap --data-dir ./data --output sitemap.xml` |
| 1548 | *12,440* | — | — | `wrote sitemap.xml · 12,440 urls` |

All numerals italic until `measured:true`; the heartbeat line is always upright. WIND from ratios: `calm` (429 and timeout both 0), `light` (< 1%), `fresh · 429s` (≥ 1%).

**`assets/log.json` (schema 2):**
```json
{"schema":2,"vessel":"rustmapper","version":"0.1.3","target":"http://127.0.0.1:8080","hosts":1,
 "date":"2026-10-07","measured":false,
 "profile":{"rate_rps":2.0,"ramp_s":10,"p95_fetch_ms":812,"wal_fsync_p95_ms":3,"urls_total":12440,
            "failed_ratio":0.004,"timeout_ratio":0.0,"r429_ratio":0.0,"permits":512,"shards":8},
 "start":"1403",
 "entries":[{"time":"1402","kind":"cmd","text":"pip install rustmapper"},
            {"time":"1402","kind":"out","text":"Successfully installed rustmapper-0.1.3"},
            {"time":"1403","kind":"cmd","text":"rustmapper crawl --start-url http://127.0.0.1:8080 --workers 512"},
            {"time":"1403","kind":"out","text":"seeded · sitemap · 1 host · robots.txt read · delay 0.5 s · frontier {shards} shards · wal on"},
            {"time":"1405","kind":"health"},
            {"time":"1430","kind":"remark","text":"remarks · nothing to report"},
            {"time":"1431","kind":"remark","text":"Nothing on fire."},
            {"time":"complete","kind":"out","text":"crawl complete · plateau · {log} urls · {elapsed}"},
            {"time":"+2m","kind":"cmd","text":"rustmapper export-sitemap --data-dir ./data --output sitemap.xml"},
            {"time":"+2m","kind":"out","text":"wrote sitemap.xml · {log} urls"}],
 "signoff":{"text":"Log closed","time":"+4m","initials":"B.S.R."},
 "heartbeat":{"template":"{HHMM} UTC · watch kept by cron · {commits} commits · {repos} repositories"}}
```
`kind` ∈ cmd · out · remark · health. `sheets/log.py:simulate(profile, entries)` fills `log`, `speed`, `wind` from the time column (`complete`, `+Nm` resolve from the profile) unless an entry supplies them; with `measured:true` all values come from the file and the build only warns when speed ≠ Δlog/Δt ± 25%. Refuses > 10 entries. Every `cmd` flag must be in T7's `CLI_FLAGS` (verified against the Rust-sitemap README) or the build fails; `health` fields come from T7's verified `METRICS` (21 names `urls_timeout_total`, `urls_failed_total`, `wal_fsync_latency`, `throttle_permits_held`; verify in `src/metrics.rs`).

Motion: static except the heartbeat line: per-glyph `<animate opacity calcMode="discrete">`, 36–60 ms jitter (LCG seeded on row), +160 ms after spaces, `begin="30s"`, freeze; cursor rect rides `animateTransform translate` on the same discrete keyTimes, then blinks `1;1;0;0` keyTimes `0;.5;.5;1` dur 1.1 s indefinite (1.8 repaints/s). Without `updated_at` the open line is `$ ▮`; nothing types. Night: remarks ink ≥ .85.

Alt: "Ship's log, rustmapper {version}: {n} entries, {start}–{close}, {log} URLs on {hosts} host; closed by {initials}; the night watch kept by the daily job."

Phone 720×220: TIME · REMARKS, mono 26, four lines: `1430 remarks · nothing to report` / `1431 Nothing on fire.` / `Log closed 1550 · B.S.R.` / `0634 · 1,828 commits · 21 repos`; static cursor.

### C. Instruments — 800×290, hung at 62% right

`<img align="right" width="62%">` (T1/T10 verify the sanitizer keeps `align`; the fallback, a 62%-wide stacked image, stays legible: 800 px at 540 is the 0.675 scale every sheet gets). Columns x=0/267/534 (w 266); vertical rules 0.6 at x=266, 533, y=40..236. Rotated group labels mono 13 tracked, `rotate(-90)`, baseline x=16, reading upward from y=236: `LEAD · LANGUAGES` · `LOG · STORES & QUEUES` · `LOOKOUT · DECK`. Rows pitch 28, baselines 72..212: name mono 14 at x+32 (plex-medium ink when bold, plex ink2 otherwise); dot leader hair `1 4` from name end +8 to x+232; `fitted` muted anchor end x+240 as `YYYY-MM`. Foot baseline 272: muted at (32,272) `bold · underway this quarter      fitted · first commit of its repository`; `CHART NO. {N} · SHEET 5` anchor end (784,272).

| LEAD | repo | LOG | repo | LOOKOUT | repo |
|---|---|---|---|---|---|
| Python | Scrapy | Delta Lake ⚓ | Scrapy | Prometheus · Grafana ☆ | Scrapy |
| Rust ⫽ | Rust-sitemap | PostgreSQL | Scrapy | Docker · Kubernetes | Scrapy |
| Swift | 3d-swift-globe-widget | Redis | Scrapy | GitHub Actions | BenjaminSRussell |
| C | game_engine | Parquet · Arrow | Scrapy | tokio | Rust-sitemap |
| TypeScript | Data_science_dev | redb · WAL | Rust-sitemap | maturin · PyPI | Rust-sitemap |
| Go | go_go_go | fastbloom | Rust-sitemap | MLX · Qwen | mlx_Qwen_data_entry |

`FITTINGS` lives in `chart.toml` (T1); `fitted = repos[name].first[:7]`, bold = `repos[name].active`. Missing repo → empty cell, leader to the margin. T7 verifies each fitting in its repo's manifest before it ships. Symbols: exactly the three T3's legend defines (track line, anchorage, light), chartlib glyphs at 0.55, PEN, ink2. No motion. Night: names ink .85.

Alt: "Instruments carried, by column: languages, stores and queues, deck. Bold where the repository is active this quarter; dates are each repository's first commit."

Phone 720×48: hair rule y=24, x=16..704; `CHART NO. {N} · SHEET 5` 26 anchor end (704,40). The stack is in the Markdown line above it.

### D. Limit of survey — 1280×270

Neat line 1 px ink .8 at x=14..1266, y=14..240, **broken on the right y=112..226**. The only prose: `The chart ends here. The web doesn't.` serif-italic 28 ink at (48,78).

**Index of adjoining sheets:** `INDEX OF ADJOINING SHEETS` label muted at (48,160); box (48,166,200,60) paper fill, 1 px ink; 4×3 cells 50×20; cell (1,1) filled `land` with `1` upright centred; every other cell `url(#unsurv)` (T6's hatch, the hero's own id). Water hy=150, PEN, x=40..1040; lip `M1040,150 c10,0 16,4 19,12 c3,8 4,24 4,42` BRUSH; three fall lines fanning 2–8 px, HAIR, dash `3 7`, dashoffset loop 10 s; swell `q24,-5 48,0` at hy+9 translating 0→−48 over 10 s `sea`, `id="sea10"`, indefinite. Mist: three arcs `M0,0 q6,-10 14,-6` HAIR at (1056,226)/(1066,228)/(1076,224), opacity `.5;0;0` keyTimes `0;.16;1` with translate-y 0→−8 in the same window, dur 10 s, begins `sea10.begin+0/3.3/6.6s`.

Limit line x=1000 dotted `1 5` round caps, y=30..226, PEN; night .85. Rotated `LIMIT OF SURVEY 2026` tracked at x=992 reading upward from y=226. Hatch `#unsurv` over `land` at x=1000..1266, y=30..150 and x=1120..1266, y=150..226; `UNSURVEYED` tracked at (1130,72). Six italic 11 soundings thinning x=700..980, y=180..220. Chart note `Obstn rep. 2026 (PA)` label muted .7 anchor end (980,136).

**Boat** (T6's 11-command sloop, scale 1.0, waterline 149): t=0 at x=90, `rotate(-4)` under way, lifted by `sea10` (translate-y `0;-2;0`, 10 s). `arrive`: `animateTransform translate 90→980`, `begin="40s"`, dur 24 s, `settle`, freeze; at `arrive.end` `<set>` rotate 0, main luffs once (`scale` about the mast `1 1;.6 1;1 1`, 0.8 s); rode HAIR dash `2 3` from (996,149) to (1006,224) drawn by `pathLength` in 0.6 s; anchor glyph (1006,220) s 0.8; `14 · good holding` anchor end (984,236), italic 14, upright words. The bow faces the fall; the anchor lies on the line.

**Serpent** per 31: three strokes + eye, BRUSH, `translate(880,150)`, clipped y<150, head-first (humps +0.25 s, +0.5 s): up 0.9 s `settle`, hold 0.6, down 0.9 `draw`; `id="serpent"`, `begin="arrive.end+20s; serpent.end+93.6s"`, opacity .7. Ripples: three ellipses at (900,152), rx 6→60, ry 1.5→6, opacity .5→0 over 20 s `settle`, staggered 0.6 s, `begin="serpent.end"`. Night: eye accent .8, kept out of the legend (31); day ink.

Outside the neat line: (16,258) `CHART NO. {N} · SHEET 6`; (1264,258) anchor end `NO ADJOINING SHEET`. Night paper per T6 (≈ #132037, per 27); sail accent in both editions.

Stills: t<40 s boat under way at x=90; 40–64 s approaching; ≥64 s anchored, swell, mist, serpent 2.4 s in 96; never a frame without a boat.

Alt: "Limit of survey. Sailboat anchored short of where the water leaves the sheet; beyond the line, unsurveyed hatching. The chart ends here. The web doesn't."

Phone 720×320: static end state; serif 40 on two lines at (24,72)/(24,118); hy=200; limit line x=560; glyph boat ×1.4 anchored at 548; no index, no serpent; folio 26 at (16,308).

## 3. Interfaces

**From T7:** `stats.updated_at` (ISO UTC), `stale_days`, `repo_count`, `commits` (author-filtered), `weeks: [{start, n}]` (calendar, Sunday starts), `repos[].weeks[52]` on the same starts from `git log --format=%at %an` filtered to Ben's identities, `repos[].first/last/commits/active` (≥3 of the last 12 weeks), `delta_commits`, verified `CLI_FLAGS` and `METRICS`, manifest check for `FITTINGS`.
**From T6:** `monotone_path(pts)`, `boat(ink, sail, paper, scale, detail)`, `serpent()` per 31, `anchorage()`, `wave()`, hatch id `unsurv` with final spacing/opacity, `HAIR/PEN/BRUSH`, tokens `paper_log`, night `paper`, `land`.
**From T5:** roles `label/note/texture`, mono 14.5/14 with tnum, tracking cap, serif grade strokes at 17/18/28/30, phone floor 26, `text_width` for the 766 px assertion.
**From T4:** `type_in(text, x, y, begin, seed)` (discrete glyphs + cursor translate), `blink(begin)`, timeline ids `sea10`, `arrive`, `serpent`, the 30 s and 40 s delays in the choreography table, `motion=False` and `build_phone` conventions.
**From T3:** legend rows for track line, anchorage, light (reused on Instruments) and `(PA) · position approximate`.
**From T2:** `N`, the `unsurv` hatch and `LIMIT OF SURVEY 2026` string, the ≤14-day sprint rule.
**From T1:** `assets/log.json` path in `chart.toml`; workflow writes `updated_at` and runs `build_assets.py --heartbeat`; `if: failure()` sets `stale_days`; sanitizer check for `align`.
**To T8:** the four alts, the Instruments `<img align="right" width="62%">` markup, the plain-text stack (table C), "how we counted" definitions (typical week, active, HW cause, heartbeat). **To T10:** §5. **To all:** `sheets/{soundings,log,instruments,footer}.py` exposing `NAME`, `build(t, data)`, `build_phone(t, data)`, `ALT(data)`.

## 4. Build order, effort, risks, left out

Order: log.json + `simulate()` (3 h) → log sheet (6 h) → soundings plumbing with T7 and sheet (9 h) → instruments (4 h) → footer once T6's boat/serpent land (8 h) → phone editions (6 h) → tests (5 h). ≈ 41 h.
Risks: `align` stripped by the sanitizer (fallback acceptable); calendar/clone week misalignment (assert equal `start` arrays); CLI flags and metric names unverified until T7 clones; a localhost crawl may still read as a demo (the 2-of-512-permits line helps; only Ben's real run cures it); footer cost creeping past 4 ms/frame (gate it).
Left out: stat tiles, language bar, crawl bar and swaps, the 3 s tide draw-in, leader animation, footer mono caption, "Notice 5" on the footer, seven droplets, the two-eyed serpent, 32's dateline strip (its anecdotes fold into the fleet register and T2's sprint note).

## 5. Acceptance

1. `grep -c "ILLUSTRATIVE\|PENDING\|SEEDED\|example.com"` over the four sheets = 0.
2. Change `weeks[k].n` → HW/LW/median/sparkline move; delete `weeks` → build fails "no soundings".
3. Every numeral in log-*.svg uses `plex-italic` glyph ids unless `measured:true` or on the heartbeat row; `simulate()` yields monotone `log` and `speed = Δlog/Δt ± 25%`.
4. Perf harness: soundings and instruments 0 repaints; log ≤ 2 repaints/s after 33 s; footer ≤ 4 ms/frame and the only continuously repainting sheet.
5. Filmstrip at 0/25/50/75/99 % of 96 s: a boat in every footer frame; header + ≥ 10 entries in every log frame.
6. OCR of 360 px renders recovers every 26 px string; Instruments phone is a rule plus folio.
7. Alt strings ≤ 25 words, built from data, none naming the serpent.
8. Day muted text ≥ 4.5:1 with T6's corrected tokens; night semantic ink ≥ .85.
9. Every `FITTINGS` name resolves to a repo in stats.json; the heartbeat line equals `updated_at` to the minute and matches the Soundings dateline.
