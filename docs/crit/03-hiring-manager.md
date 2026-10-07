# Crit 03 — the hiring manager

Lens: I hire full-stack and data/infra engineers. I read this three times: a 10-second skim, a 60-second scan, a 5-minute read with the repos open.

## 1. First impression

At 10 seconds this is the most confident, best-set GitHub profile I have seen this year, and I immediately trust that the person has taste. At 60 seconds I still do not know what he does for a living, for whom, at what level, or what he wants next, and the one sheet that should tell me (Soundings) tells me "46 followers, joined 22 months ago, stats pending." At 5 minutes I like the writing a great deal and I have found two things I would click, but I have found no evidence that anything described has run at the scale it describes, and no evidence he has ever worked with another engineer.

## 2. What works

- The hero. Big Instrument Serif name, one honest two-line thesis, a chart that is clearly hand-built. Seniority of taste in one glance; the day/night editions prove craft without saying so.
- Sheet 3 (Scrapy approach) is the metaphor earning its keep: URLs → Scout → Analyze → Summarize as a buoyed channel, Grafana as the light, breaker status in the corner. That is an architecture diagram a skimmer can read.
- "Notes to mariners" are the strongest lines on the page. "Boring under load", "Raw before clean, always", "Dashboards and breakers belong in version one" read as scar tissue, not slogans. That is what I want more of.
- The rust_llm_logger one-liner ("a stream-tee forwards tokens to the client while parsing them for metrics, so logging costs the caller nothing") is the most specific technical sentence here. I would click it.
- Alt text is excellent; almost nobody does this.

## 3. Problems, ranked by impact

1. **It never answers the hiring question.** No role, no level, no location/timezone, no "currently", no "looking for", no résumé/LinkedIn. The bio box on the hero says "Full-stack developer · scraping enthusiast": "enthusiast" is the word a hobbyist uses, and "full-stack" contradicts the entire page, which argues he is a crawl/data-infra engineer. Pick the lane the page already picked.
2. **Soundings is a vanity sheet that hurts.** 1,828 lifetime commits says nothing (solo churn? squash habits?). 46 followers says "nobody is watching." "Since Oct 2024" says "two years of public history" in 80pt type. These are the only numbers a stranger can trust, and they front-load his weakest signal. Then the right half is empty: "seeded, first refresh pending", "tide table arrives with the first refresh." A stats sheet shipped with a placeholder is the one unforgivable thing on a page whose thesis is "lights before speed."
3. **The one place with concrete operational numbers is labelled fake.** Sheet 5: "numbers illustrative, the package is real." 48,213 URLs discovered from `example.com`, which has one page. Anyone who has built a crawler knows that log is invented; the disclaimer confirms it. Not charming: it reads as "I have not actually run this." Same with "sized for 100M+ URLs" and "up to 512 workers": capacity claims, never a measured run. "Built to be operated rather than demoed", yet every artefact is a demo.
4. **"Scrapy" is a naming collision with the most famous Python crawling framework.** My first assumption was a fork; my second was confusion. The legend lists "Scrapy" as the daily driver under Data, which makes it worse: is that the framework or his platform? Three names for the other project (Rust-sitemap, rustmapper, Rustmapper Shoal) compounds it. Also "Scrapy Harbor" (hero) vs "SCRAPY HARBOUR" (sheet 3): the README is American, the sheet is British.
5. **Zero collaboration signal.** Every repo is solo; no upstream PRs, no co-authors, no issues from strangers, no write-ups, no talks. The only "social" number on the page is 46. For someone claiming systems-at-scale work, the absence of a second human is the biggest gap after the role statement.
6. **The metaphor hides the information architecture.** A skimmer reading headings gets Approaches / Soundings / Notes to mariners / Legend / Other waters / Colophon. None of those say Projects, Principles, Stack, Experience. The chart voice is lovely once you are in it; it is a toll gate for everyone who is not.
7. **Proportion: more words about the page than about any system.** The Colophon is the longest technical passage here and it describes the README. "Off the clock" promises a human and delivers a paragraph about the avatar. There is no comparable depth for how Scrapy behaved on day forty.
8. **"Other waters" dilutes.** Fourteen repos plus four "also on the shelf": a prize wheel, two games, a farming sim, three widgets. The breadth reads as scatter and pulls the median down. The contribution-snake is the one templated item on a page that twice says "drawn, not templated."
9. Small: "Chart No. 27" invites "why 27?" and has no answer. "Not for navigation" is a nice period detail on its own; stacked with "numbers illustrative" and "first refresh pending" it becomes a third hedge.

## 4. What "months of team work" would look like

Testable standards:

- Every number on the page is real, sourced, and dated. No "illustrative", no "pending". If a stat cannot be made real, the sheet is cut.
- One documented run per flagship system: URLs, hosts, wall-clock, hardware, error/retry rate, what broke, linked to the artefact (committed log, Actions run, or a short write-up). Readers can check it.
- A single sentence under the name that answers role, focus, location, availability.
- A reader who ignores every image still gets a complete, ordinary résumé-shaped read from headings and bold text alone.
- One canonical name per project; one spelling of harbor; the repo is renamed or the page says "not the framework."
- At least two artefacts involving another human: an upstream PR, a reviewed design doc, a user issue answered.
- Shelf trimmed to what you would defend in an interview; everything else archived or folded closed.

## 5. Proposals, ranked

1. **Turn Soundings into "Sea trials."** Replace commits/followers/since with measured numbers from real runs: "rustmapper 0.1.3 · 2.1M URLs · 38k hosts · 6h12m · M2 Pro · 0.4% 5xx", with the run log committed and linked. Layer of meaning: on a chart, soundings *are* measurements; make them actual measurements, and the sheet says "I measure what I build" without saying it. Keep the PyPI download count as the only social number.
2. **Make the log real.** Record a real session (`script`/asciinema → SMIL) against a domain you are entitled to crawl, with real timestamps that match the release commit date. Delete the disclaimer. Second-look delight: the log's final line is the actual exported sitemap URL, and it resolves.
3. **Position fix on the hero.** Replace "Chart No. 27" with a position box: "Backend / data-infra · <city or TZ> · open to <what> from <when>." Layer: a fix is where you are and the course is where you are heading; end the plotted course at a labelled waypoint named for what he wants to build next.
4. **Disambiguate Scrapy.** Rename the repo (the harbor already has a name; use it) or add "not the framework; a platform built on it" in the first line.
5. **Dual-register headings.** Keep the chart title, add a plain gloss a skimmer reads: "Approaches · the two systems", "Soundings · measured", "Notes to mariners · five rules", "Other waters · smaller work".
6. **Notices to mariners as a changelog.** Real charts are kept current by dated notices. Add a thin sheet of three to five dated corrections from real commits: "2026-03 · rate limiter rewritten after X hosts returned 429 in bursts." Layer: says "I operate and revise" with evidence, not adjectives.
7. **Encode real data in the hero soundings.** The depth numbers on the chart become weekly commit counts (or URLs/week from a real crawl), with one line in the legend saying so. Second-look delight: the decorative numbers were data all along.
8. **Fold the shelf.** Six repos open; the rest in a closed `<details>` titled "Below the waterline." Drop the snake, or own it as the one borrowed instrument on board.
9. **Collaboration line.** "Lights tended elsewhere": two or three upstream PRs or answered issues. If none exist yet, that is this month's job; the page should not launch without it.
10. **"Off the clock"** gets one real off-the-clock thing or is cut; the avatar paragraph belongs in the Colophon.

## 6. What it says vs what it should say

It currently says: a solo, early-career builder with unusually good taste and real range, who writes beautifully, has the right instincts about observability and raw-first storage, and may care more about presenting systems than about proving they ran. The scale words (100M, 512, "survive the open web") are all capacity, not history, and the honest stats quietly contradict the confident voice.

It should say: an engineer who builds crawl and data infrastructure, runs it, measures it, revises it, can explain the tradeoffs in one paragraph, and happens to be able to design. The chart is a brilliant delivery vehicle. Right now it is also the cargo.

What would make me message him: one real run report, one real log, one sentence about what he wants, and one trace of another human.
