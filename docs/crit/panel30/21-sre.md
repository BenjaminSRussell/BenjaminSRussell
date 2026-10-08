# 21 — SRE / observability engineer. Lights, breakers, SLIs, and whether the page has a pulse.

I run Prometheus, Grafana and on-call for a living. I read README.draft.md, STANDARDS, CHANGELIST, both specs, the approach-scrapy and log renders, profile.yml and stats.json, and, because the metaphors describe real systems, the Scrapy repo's `alerting_rules.yml`, `recording_rules.yml`, `monitoring/prometheus.yml` and Rust-sitemap's `src/metrics.rs`.

## What is good

- **"Lights before speed" is a real operating philosophy, well expressed.** "A crawler you cannot watch is a crawler you cannot trust; dashboards and breakers go in version one" is how SREs talk, and the repo backs it: a Prometheus config, ~30 alerting rules, recording rules down to `scrapy:response_time:p95` and a composite `pipeline:health:score`. Earned, not borrowed.
- **Two mappings in the Approaches spec are exactly right.** Leading lights for the health check: "on the line" is a readiness probe, drift is degradation, Iso 2s is a plausible probe period. Rate Limit Shoal as a submerged hazard: rate limits are not land; you can be over them and not know.
- **The watch log is the right form for a run.** TIME · POSITION · WIND · REMARKS, a sign-off and a watch end is an incident timeline in the right clothes. "Nothing to report / Nothing on fire" is the handover cadence every on-call knows.

## What is bad, ranked

1. **The breaker is the wrong light, and the chart says the light is broken.** A circuit breaker has three states: *closed* (traffic flows), *open* (refused), *half-open* (one probe through). A sector light has none: its red sector is permanent and means "this bearing leads onto danger". The spec draws "Breaker Lt · Fl(2) R 6s · sector unlit" because the breaker is closed. On a chart an extinguished light with a published character is a *defect*, the first item in any Notice to Mariners; an SRE reads it as a configured alert that is not firing. The current render's green "BREAKER CLOSED" dodges that but imports the one term that confuses every non-engineer (closed = good).
2. **Grafana Lt Fl(3) 10s is decorative.** Nothing in the repo flashes three times in ten seconds. The global `scrape_interval` is 15s and every job scrapes at 30s; those are the rhythms the dashboard lives on.
3. **The illustrative numbers do not add up, which is what "illustrative" costs.** Log row 4: start 14:03; by 14:04 position is 48,213 at 188→412 req/s. Sixty seconds at 412 req/s is 24,720. Row 6: wind 41 req/s, position unchanged. Italic says unmeasured; arithmetic says never computed. The second is the credibility leak, and the person you most want to impress is the one who checks.
4. **The page has no status of its own.** `profile.yml` runs at 06:20 UTC and commits SVGs. If `build_stats.py` fails, the sheets stay silently stale while the colophon says "fetched each morning": precisely the failure "lights before speed" condemns. `stats.json` keeps `updated` as a date only, and GitHub cron fires late or drops under load, so 06:20 is the scheduled time, not when a sounding was taken.
5. **No SLIs.** For a crawler the five that matter are fetch success ratio, p95 fetch latency, politeness violations (429s, robots denials, backoffs), frontier/queue depth and WAL lag. The repos expose all five under real names (`scrapy:error_rate:ratio`, `scrapy:response_time:p95`, `throttle_adjustments`, `kafka:consumer_lag:current`, `wal_fsync_latency`, `wal_truncate_offset`). The sheets show none. WIND = req/s is the vanity metric; the principle says speed comes second.
6. **No alerting in the harbour.** Dashboards are for when you can see; paging is for when you cannot. The repo ships `alertmanager.yml`; the chart has no fog signal.

## What needs to be done

- **F1. Port traffic signal for the breaker.** International Port Traffic Signals are a real charted convention with the breaker's exact semantics: three green = "vessels may proceed" (closed); three flashing red = "emergency, all vessels stop" (open); green/white/green = "a vessel may proceed only on specific orders" (half-open, one probe). Small mast on the breakwater at (1068,532), three stacked 3px dots, label "Traffic Sig · per-host breakers" 13px upright, lit green. Legend row: three mini-stacks, named *proceed · stop · one at a time*. No open/closed anywhere.
- **F2. Derive light characters.** Grafana Lt: Fl 15s from `scrape_interval`, read from the repo's `prometheus.yml` in the build so it changes when the config does; upright because measured. Ldg Lts period from the readiness probe in `k8s/deployment.yaml` if one exists.
- **F3. Fog signal.** A charted "Horn" mark beside Grafana Lt, 13px label; the truth under it is Alertmanager. Night: horn arc at .3 opacity. This is the missing half of the principle.
- **F4. Simulate the log, do not type it.** `build_assets.log()` takes `start`, `workers`, a latency and a rate profile from `log.json` and computes position = ∑ wind·Δt, in-flight = rate × latency (Little's law), export time = elapsed. Still italic, now consistent. Better: `rustmapper crawl … | tee assets/log.raw`, parsed to `log.json` with `measured:true`. One real session is worth every italic on the page.
- **F5. A real health line at 14:05**, before "nothing to report": `fetched 48,213 · timeout 0.4% · failed 1.1% · p95 fetch 812 ms · wal fsync p95 3 ms · throttle 512→418→512`. Every field exists in `metrics.rs` (`urls_timeout_total`, `urls_failed_total`, `wal_fsync_latency`, `throttle_permits_held`). Italic until measured.
- **F6. Heartbeat.** `build_stats.py` writes `updated_at` (ISO UTC) and `run_id`. Tide-table head line: `LAST SOUNDING 06:34 UTC · 7 OCT`; the Instruments foot repeats it. In `profile.yml`, a step `if: failure()` runs `build_assets.py --no-sounding`: same sheets, same figures, plus a pencil note "no sounding taken {date}" and the datum rule drawn dashed. The page degrades visibly.
- **F7. Politeness on the chart.** Harbour charts carry "5 kn · no wake"; add "Per-host limit" in the channel, figure from `config.rs` or italic.

## Improvements and high-level ideas

1. **The log is the heartbeat (bold).** Let the 06:20 job append one line to the ship's log: `06:34 UTC · watch kept by cron · 1,828 commits · 21 repos · no change`, upright because measured. The human watch ends at 14:12 and hands over to the machine, which keeps it overnight. The page becomes a system that reports on itself, which is what Ben says he builds.
2. **Ldg Lts fed by `pipeline:health:score`.** The rule exists. If a public read endpoint ever appears, the build pulls the last value and shifts the rear mark off the line by the deficit. Until then, print the formula's weights as the Ldg Lts note; a hiring SRE recognises a composite SLO.
3. **An error budget for the chart.** Beside "Corrected through Notice 5": `soundings taken 143 of 150 days`, from `git log` on `assets/stats.json`. The page admits its missed runs, the most SRE sentence a profile can say.
4. **Notice 3 should cite what is checkable.** "Grafana Lt, the first thing built on the Scrapy approach" is a chronology claim nobody verified. Replace with the alerting-rule count and date from git, or drop the clause.

## What the page says about its maker

Now: an engineer who knows observability matters, has the vocabulary, and decorated a harbour with it. The light flashes a made-up character, the breaker is a dark lamp, the log's numbers do not add up, and the page has no pulse. It should say: this person instruments by reflex. His light characters come from his scrape config, his breaker shows three states in a convention older than Prometheus, his log carries a health line a stranger can sanity-check, and when the nightly job fails the chart says so in pencil. Then "lights before speed" is demonstrated by the artefact rather than asserted by it.

## Five lines

1. Replace the breaker's sector light (wrong metaphor; an unlit charted light means a defect) with a three-lamp port traffic signal: proceed / stop / one at a time = closed / open / half-open.
2. Derive light characters from the repo (Grafana Lt Fl 15s from `scrape_interval`) and add a Horn mark for Alertmanager: lights are for seeing, horns for paging; the page has half the principle.
3. Compute the log's illustrative numbers (position = ∑ rate·Δt, in-flight = rate × latency) or paste a real run; 48,213 URLs in sixty seconds at 412 req/s is impossible and the reviewer who matters will notice.
4. Give the page a heartbeat: `updated_at` in stats.json, "LAST SOUNDING 06:34 UTC" on the tide table, and an `if: failure()` build that pencils "no sounding taken" instead of staying silently stale.
5. Put real SLIs on the sheet under their real names (`scrapy:error_rate:ratio`, `scrapy:response_time:p95`, `wal_fsync_latency`, `throttle_adjustments`); req/s alone is a vanity metric.
