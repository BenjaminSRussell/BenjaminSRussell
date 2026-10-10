# Review round 3, reviewer 3: the developer choosing a crawler

10 Oct 2026. Reviewer: a developer who found this profile while looking for a sitemap crawler or a crawl platform,
and who has to decide whether to try rustmapper, Ben's Scrapy, or neither. Build looked at:
`scratchpad/r6/build/round-02/`. That covers the desk and phone sheets, day and night, and the page on desk (screens
1–2) and on phone (screens 1–5). Read: `README.md`, `SPEC.md`, `LOG.md`, `DECISIONS.md` and the eight earlier reviews
(r01-1 to r03-2). Figures were checked against `assets/stats.json`, the 0.1.3 sdist (`scratchpad/r6/sdist013`), the
clones (Rust-sitemap `32c2651`, Scrapy `96e7a1a`) and the GitHub REST API.

I don't repeat findings already fixed, and I don't re-argue the ones r03-1 and r03-2 already make this round. I
agree with three of them and rank them above everything below: H1 gives the wrong cause (r03-1 #1, r03-2 #1), the
band and the `//` hatch need replacing (r03-1 #2, r03-2 #2), and the two kill clauses need merging (r03-1 #3). My
findings are the ones a person deciding whether to *use* the work runs into.

Verdict: **does not meet the goal yet. 6 / 10.** The image is the most useful thing on the page for my decision.
The page around it leaves out the three facts I check before trying any crawler: can I use it legally, will it hit
the site too hard, and which of his two tools fits my job.

## The first question: does it meet the owner's goal?

Taking his tests one at a time, from where I sit:

- **Every element has a purpose.** In the image, yes, apart from what r03-1/2 flag. I can say what I learn from
  each row. The route does what a list can't: it shows me that fetch, the governor and the writer repeat for every
  page, and that the only way out of the loop is me pressing Ctrl-C. That told me more about running rustmapper
  than its own README did, in about ten seconds.
- **It teaches something true and useful about his projects.** True, yes, once H1's cause is fixed. Useful for my
  decision, only partly. What I learn is how rustmapper 0.1.3 behaves once it's running. I can't tell which of his
  two crawlers fits my job, whether I'm allowed to use rustmapper (finding 1), or how hard it will hit the site I
  point it at (finding 2).
- **Nothing chases a reason.** Yes. No row is there for decoration.
- **Nothing announces the theme.** Yes. To me the image reads as a strip diagram of a CLI. The manner sits
  underneath and never gets in the way.
- **Reads on a phone.** Yes. At 390 px the image is about 480 px tall, the text is at least 14 px, and the link
  line is on screen 1. Both code blocks fit without scrolling sideways.

So the image passes as a picture. The page fails me as a buyer. What I'm missing is a few lines of text, not
another picture.

## What I'd conclude today, as the developer

I read the image top to bottom. Here is what I'd take away: it installs with one line on a Mac with Apple silicon;
on Linux it takes three minutes and needs Rust. By default it also asks crt.sh and Common Crawl about my domain. It
slows itself down when saving falls behind, and it saves every 50 ms. It never stops by itself. Ctrl-C once gets me
the file, and a kill doesn't. The output is a JSONL with real field names.

My verdict as a user would be: **fine on a small site I'm watching, not unattended, not in CI.** That's honest,
and it's what the code does. It's also the answer to "should I try rustmapper", which is the question I came with.
The image does its job. Whether the answer is a good one is up to Rust-sitemap's next release, not this page.

Then I go looking for the other answers, and they aren't there.

## Findings

1. **I can't tell whether I'm allowed to use rustmapper, and the repository says I'm not.** Rust-sitemap has no
   `LICENSE` file at HEAD, and there's none anywhere in its history (`git log --all -- LICENSE` is empty). The
   GitHub API returns `"license": null`, so the repository page shows no license. `pyproject.toml` declares
   `license = "MIT"` with `license-files = ["LICENSE"]`, and the README ends "## License / MIT". But the 0.1.3 sdist
   on PyPI doesn't contain the file either. MIT's one condition is that "the above copyright notice and this
   permission notice shall be included", and here there is no notice to include. GitHub's own docs say that
   "without a license, the default copyright laws apply", and choosealicense.com says that "generally means you have
   no permission … to use, modify, or share the software". In GitHub's 2017 Open Source Survey, 64 % of users said a
   license is "very important in deciding whether to use a project". Scrapy has an MIT `LICENSE` and the API detects
   it. The flagship doesn't. At a company, this is where I stop and pick another tool. The page can't fix it, but
   it can stop hiding it: the only license line on the page ("**License** Code MIT") is about the profile
   repository, and a hurried reader takes it for rustmapper's.

2. **The page never says how hard rustmapper hits a site, and the default is hard.** In both trees each host gets
   `max_inflight: 20` concurrent requests (`sdist:src/state.rs:285`, HEAD `src/state.rs:442`). New hosts start
   with `crawl_delay_secs: 0` (`state.rs:283`, HEAD `:437`). `--workers` defaults to 256 in all (`sdist:src/cli.rs:32`).
   The 50 ms `FRONTIER_CRAWL_DELAY_MS` applies only when a host is already at 20 in flight (`sdist:src/frontier.rs:669`).
   It isn't a delay between requests. The only per-host pacing is a `Crawl-delay` in robots.txt. RFC 9309 doesn't
   define that field, and Google retired its support in 2019, so most sites don't set it. For comparison, the Scrapy
   framework's settings docs give `CONCURRENT_REQUESTS_PER_DOMAIN` = 1 and `DOWNLOAD_DELAY` = 1 for a new project,
   and Ben's own Scrapy platform runs AutoThrottle with a per-host 429/503 backoff (`src/settings.py:179-190`).
   rustmapper's crawl loop doesn't back off on 429. Only its seeders do (`common_crawl_seeder.rs:51`,
   `ct_log_seeder.rs:34`). This is what a site owner asks first, and what decides whether I get blocked. It belongs
   in text, as a lookup next to the install block, not in the image. Side note for Ben: the comment on
   `max_inflight` says "(default: 2)", and the code says 20.

3. **Nothing says which of his two crawlers is for which job.** The page describes rustmapper and Scrapy one after
   the other, each on its own terms. A shopper has to work out the difference from two code blocks and four bullets.
   The difference is real, it's in the code, and it fits in one sentence. rustmapper gives you *the list of a
   site's URLs* (`SitemapNode` rows, then `sitemap.xml`) from one command, with no services. Scrapy keeps *the pages
   themselves* in Delta Lake, drops near-duplicates, summarises them, and needs Docker. The image only draws
   rustmapper, which is right (SPEC §3), and that is why the text has to say what the picture can't. "Which project
   should I look at?" is Q2 in SPEC §0, and today nothing on the page answers it for a visitor with a job to do.

4. **The release's `sitemap.xml` breaks on a large site, and the page hands me that command.** In 0.1.3
   `run_export_sitemap_command` writes every 200-status page into one `<urlset>` with no limit (`sdist:src/main.rs:387-447`,
   `sitemap_writer.rs`). The sitemap protocol allows "no more than 50,000 URLs" and 50 MB per file. Above that, you
   split the URLs across files and list them in an index. Main does exactly that (`SitemapIndexWriter`,
   `DEFAULT_MAX_URLS_PER_SITEMAP = 50_000`, `src/orchestration/export.rs:17`, #32). So for anyone who wants a
   sitemap of a big site, the tool's namesake output is invalid in the version `pip` installs. The README's install
   block prints `export-sitemap … --output sitemap.xml` and says nothing about it. One clause, gated on the release,
   would cover it.

5. **The Scrapy block's last command fails when you paste it.** `python start.py` is standard library only and runs
   `docker-compose up -d` (`start.py:345`). Everything Scrapy needs is installed *inside* the `scraper` image
   (`Dockerfile:22-25`). The next line, `scrapy crawl scout -a …`, runs on the host. On a fresh machine that gives
   `scrapy: command not found`, because the block never installs `requirements.txt`, which pins 143 packages
   (`Scrapy/README.md:496-501` does this in its own setup section). r03-2 #10 reorders the warnings in this block.
   This is a different fault: the command can't run at all. SPEC §7 test 8 ("Run the commands") is meant to catch
   exactly this, and it covers only the rustmapper block.

6. **The repository's own one-line description contradicts the image.** Rust-sitemap's About text, from the API:
   "This program runs a rust webscraper to create a sitemap that goes until it reaches end points". The image's
   loudest line says it never ends by itself. GitHub shows that description on the repository page and on a pinned
   card, so it's the second thing I read after clicking the image. Scrapy's ("…a live dashboard on localhost:3000
   and must have docker installed") agrees with the page. SPEC §4 already lists "make each pin's description match"
   as an owner action, and it hasn't been done. I list it again because it now contradicts the image.

7. **Three names for one tool.** The repository is Rust-sitemap, the package is rustmapper, and the command is
   `rust_sitemap`. The image shows only the package name, the code block only the command, and the link line only
   the package name, linking to the repository. P4 (a `rustmapper` command) is still the fix, and it's an owner
   action. I don't add a must-fix here. It's the reason finding 6 matters more than it looks.

Smaller items, no must-fix: the link line's "PyPI" sits right after "Scrapy", so it reads as Scrapy's PyPI page. It
also repeats the `pip install rustmapper` two blocks below, so the link line would lose nothing without it. All four
rustmapper releases went up within 74 minutes on 8 Nov 2025 (`edition.uploads`), so "0.1.3 · 8 NOV 2025" is
also its only release date. Scrapy's repository shows 570 open issues and pull requests. They are Ben's own backlog
(the first 100 are 87 issues by him, 11 PRs by him and 2 by Dependabot), not users' complaints, but a shopper can't
tell that from the count.

## Figures checked

| Printed | Key / source | Value | Holds |
|---|---|---|---|
| 0.1.3 · 8 NOV 2025 | `edition.version`, `edition.uploads[3]` | 0.1.3, 2025-11-08T19:52:41 | yes |
| pip install rustmapper | `edition.scripts`, runcheck install ok | `["rust_sitemap"]`, median 171.4 s cold | yes |
| by default also sitemaps, certificate logs, Common Crawl | `sdist:src/cli.rs:58` | `default_value = "all"` | yes |
| fetch a page; same-site links go back on the queue | `routes` F1 verified both | | yes |
| fetches fewer pages at once when saving falls behind | `routes` G1 verified both | | yes |
| saved every 50 ms | `BATCH_TIMEOUT_MS` | 50 | yes |
| after a kill, export-sitemap still works | runcheck `export_after_kill` | 3 `<loc>` | yes |
| never ends by itself | runcheck `ends_by_itself` | still running at 150 s | yes (cause: see r03-1 #1) |
| press Ctrl-C once … a second press or a kill skips it | `crawl_ctrl_c` ok 2.0 s; `kill_writes_file` false | | yes |
| url, depth, status_code, title | `SitemapNode`, both trees | | yes |
| read by ideal-url-organizer, with a test | `handoffs[0].state` | `runs` | yes |
| On main at `32c2651` · 176 tests · CI passed 7 Oct 2026 · 16k lines of Rust | `repos[Rust-sitemap]` | 32c2651, 176, success 2026-10-07, 16,390 | yes |
| On main at `96e7a1a` · 1,920 tests · CI passed 8 Oct 2026 · 69k lines of Python | `repos[Scrapy]` | 96e7a1a, 1,920, success 2026-10-08, 69,036 | yes |
| Prebuilt for Apple silicon on CPython 3.13 | `edition.wheels` | `cp313-cp313-macosx_11_0_arm64` only | yes |
| 3 min from a cold cache on a 4-core Linux x86_64 machine | runcheck install | cold, 4 CPUs, 168.2/171.4/174.3 s | yes |
| localhost:3000 | `figures[]`, `docker-compose.yml:249` | `"3000:3000"` | yes |
| 22 public repositories; 15 more | `repo_count`; 22 − 1 − 2 − 4 | | yes |
| 3 %; 297 | `coauthored_total.agent_share`; `agent_authored.total` | 0.031; 297 | yes |
| (not printed) rustmapper's license | GitHub API `license` | `null`; no LICENSE file at HEAD or in the sdist | **missing** (finding 1) |
| (not printed) per-host concurrency | `sdist:src/state.rs:285`, HEAD `:442` | 20, both | **missing** (finding 2) |

`stats.json` carries no `license` key for any repository today. That's why finding 1 never surfaced in the pipeline.

## Every element of the image

| Element | What I learn | Verdict | Why |
|---|---|---|---|
| "Ben Russell" | whose page | keep | |
| Role line | crawlers and data infrastructure, Python and Rust | keep | the drawing proves it |
| Empty desk column under the role | nothing | keep | quiet paper keeps the route the one dense block |
| "rustmapper" | which tool | keep | |
| "Crawls a site and writes one line for every page it reaches." | what it gives me: a URL list, not page content | keep | the line that tells me it isn't a scraper; finding 3's sentence leans on it |
| Start bar | where to begin | keep | |
| `pip install rustmapper` | how to get it | keep | |
| "0.1.3 · 8 NOV 2025" | the release's age, and that it's the only one | keep | true; it's the date I judge maintenance by, next to main's CI date in text |
| Track | one way through, top to bottom | keep, change per r03-1 #2 | the gap below the loop would show my verdict ("not unattended") without words |
| S1 seeder.rs + "start URL; by default also sitemaps, certificate logs, Common Crawl" | by default it sends my domain to crt.sh and Common Crawl | keep (wording per r03-2 #4) | the row I'd most want before running it on an internal or private host. Common Crawl's index rate-limits and blocks IPs for 24 h, and it answered 503 when I fetched it today |
| F1 bfs_crawler.rs + "fetch a page; same-site links go back on the queue" | it's a BFS crawl loop | keep (wording per r03-1 #1) | |
| G1 tick + "fetches fewer pages at once when saving falls behind" | it protects its own store | keep | the only design choice here I haven't seen in other crawlers; it makes me ask "how many at once?", and finding 2's text answers that |
| W1 writer_thread.rs + "saved every 50 ms: …" | a crash loses about 50 ms | keep, change per r03-1 #3 | |
| Loop line + up arrow | which rows repeat | keep | the mark a list can't replace |
| H1 band, hatch, text | the catch | change (r03-1 #1, #2; r03-2 #1, #2) | the fact is the most useful line in the image for my decision, but its cause is wrong and its mark reads as a diff highlight or a `//` comment |
| C1 "press Ctrl-C once …" | how to get the file | keep, change per r03-1 #3 | |
| End bar | where I end up | keep | |
| `data/sitemap.jsonl` + fields | what I get, with the struct's field names | keep | lets me judge whether it feeds my own pipeline before installing |
| Hand-off arrow + "read by ideal-url-organizer, with a test" | his tools connect, and the join is tested | keep | the one line about the body of work; to me as a shopper, it says the JSONL format is stable enough that something else depends on it |
| Night editions | the same | keep | |
| Phone editions | the same, stacked | keep | |

The image has nothing I'd cut beyond what r03-1/2 cut. I'd add nothing either. Findings 1 to 5 are lookups, and
lookups go in text (SPEC §0).

## Every block of the page

| Block | What I learn | Verdict | Why |
|---|---|---|---|
| Image | how rustmapper runs and where it stops | change (r03-1/2) | |
| Alt text | the same in 25 words | keep | |
| Link line | where to go | change (small) | "PyPI" reads as Scrapy's and repeats the install line; drop it or make it "rustmapper on PyPI" |
| Builds / Languages / Stack | who he is | keep | |
| *(new)* which one for what | which of the two fits my job | **add** | finding 3; must-fix 2 |
| rustmapper sentence | what it is | keep (r03-2 #9 changes it) | |
| rustmapper facts line | alive, tested, size, which snapshot | change | add the license from the API (must-fix 1) |
| rustmapper install block | the commands | keep | |
| Wheel note | when pip just works | change | add the load and the 50,000 clauses (must-fix 3) |
| Scrapy sentence + facts | the second tool | change | license from the API ("MIT"), the same rule as rustmapper's |
| Scrapy code block + note | how to start it | change | the last command can't run as pasted (must-fix 4) |
| Scrapy bullets | how it's built | keep | the third and fourth bullets are what tell me it's the throttled, stateful one |
| Also | the next four | keep | go_go_go's headless-Chrome line is the answer to "what if my site needs JavaScript", which rustmapper can't render (no JS engine in `sdist:src/`) |
| 15 more | the rest | keep | |
| Working rules | how he works | keep (r03-2 #7, #8) | rule 3 ("dashboards before speed") is believable because the Scrapy block shows Grafana |
| Found a mistake? | the page can be corrected | keep | |
| Data line | what was checked and run | keep (r03-1 #4, r03-2 #6) | |
| License line | the profile's terms | change | say whose license it is: "**This profile** Code MIT; …", so it isn't read as rustmapper's (must-fix 1) |

## Must fix, ranked

These come after r03-1 #1–3 and r03-2 #1–2, which I endorse and don't repeat.

1. **Show each flagship's license, measured, and make the gap visible to Ben** (`scripts/data/github.py`,
   `scripts/build_stats.py`, `stats_schema.json`, `render_readme.py facts_block`, new check in `scripts/checks/`;
   about 40 lines). Store `repos[].license = license.spdx_id` from the REST repository JSON that `github.py`
   already fetches. Use `null` when GitHub detects none, and add one AUDIT row. The facts line gets "· MIT" (the
   SPDX id) after the CI clause when it's set, and nothing when it's `null`, so the page never states a license
   GitHub doesn't detect. New fast check LICENSE-FLAGSHIP: **warn** when a repository with a facts line has
   `license` null, naming it. Today it warns for Rust-sitemap. The license block's first word becomes "**This
   profile**". Test: a fixture with `license: null` prints no license clause and raises the warning. Owner action,
   two minutes, in Rust-sitemap: commit the MIT `LICENSE` that `pyproject.toml` already names, so 0.1.4's sdist
   ships it. Why: whether I'm allowed to use the tool is the first thing I check, and right now the answer is no
   (finding 1).

2. **One sentence on which tool is for which job** (`chart.toml [copy] pick`, written by `render_readme.py` in a
   new `pick` marker between the Stack line and the rustmapper block; about 20 lines with a test). Text: "For the
   list of a site's URLs from one command, **rustmapper**; to keep the pages themselves, deduplicated and
   summarised, in a pipeline that needs Docker, **Scrapy**." (34 words, 3 lines on a phone.) Its claims rest on
   `[[figures]]`-style anchors that already exist or are trivial to add: `SitemapNode` (rustmapper's output),
   Scrapy `src/stage3/stage3_worker.py` "MinHash" and "extractive summary", and `start.py` `REQUIRED_TOOLS` "docker".
   The FIGURES and STRINGS-TWICE checks must still pass. If STRINGS-TWICE trips on "one line" against the image
   header, word it "the list of a site's URLs". Why: Q2 is the visitor's first decision, and the page makes them
   work it out (finding 3).

3. **Two facts under the rustmapper install block, gated on the code** (`render_readme.py _wheel_sentence` or a
   sibling, `chart.toml`; anchors via the route anchor engine, which already checks both trees; about 30 lines).
   (a) Both trees: "It sends up to {const:max_inflight} requests at a time to one host, {workers} in all, with no
   pause between them unless robots.txt sets a Crawl-delay." Anchors: `src/state.rs` `max_inflight: 20` in
   `HostState::new` (HEAD and sdist), `crawl_delay_secs: 0`, and `src/cli.rs` `default_value = "256"` on `workers`.
   Printed only when every anchor holds in both trees. (b) Release only, while the sdist has no
   `SitemapIndexWriter`: "0.1.3 writes one sitemap.xml however many pages it found; the sitemap format allows 50,000
   URLs per file." Once a release carries `SitemapIndexWriter`, the clause goes. Both clauses go through FIGURES
   (20, 256, 50,000). Why: the load decides whether the crawl gets me blocked, and the 50,000 cap decides whether
   the namesake output is valid. Both are lookups, so they go in text, not the image (findings 2, 4).

4. **Make the Scrapy block runnable as pasted** (`render_readme.py` Scrapy block, `tests/test_pipeline.py`; about 10
   lines). Replace the host-side crawl with the container's:
   ```
   # discovery only, on your own site:
   docker-compose exec scraper \
       scrapy crawl scout \
       -a allowed_domains=<domain> \
       -a start_urls=<url>
   ```
   Every line is at most 38 columns. The `scraper` image installs `requirements.txt` and copies `scrapy.cfg` into
   `/app` (`Dockerfile:12-28`), so nothing has to be installed on the host. This has to be confirmed by running it
   once: either a Scrapy leg in the run check (compose up, then `exec scraper scrapy list` must list `scout`), or by
   hand before merging. If it fails, fall back to `pip install -r requirements.txt` above the host command, with the
   comment "# 143 pinned packages". Combine this with r03-2 #10's comments. Why: the block's last command fails on a
   fresh machine (finding 5).

5. **Owner actions, outside this repository, now contradicted by the image** (finding 6). Set Rust-sitemap's About
   description to the image's header sentence, "Crawls a site and writes one line for every page it reaches." Pin
   Rust-sitemap and Scrapy first (SPEC §4, still not done). Optionally, a fast check DESC-DRIFT that warns when a
   flagship's API `description` contains "until it reaches" or otherwise lacks the header's first three words. Low
   priority. It's here so the warning exists the next time it drifts.

## Sources (fresh this round)

1. choosealicense.com, "No License": without a license "you have no permission from the creators of the software to
   use, modify, or share the software". https://choosealicense.com/no-permission/ (finding 1, must-fix 1)
2. GitHub Docs, "Licensing a repository": "without a license, the default copyright laws apply"; GitHub detects the
   license by comparing "the repository's *LICENSE* file" with Licensee.
   https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
   (finding 1: why the API says `null`)
3. GitHub, Open Source Survey 2017: 64 % of users say a license is "very important in deciding whether to use a
   project". https://opensourcesurvey.org/2017/ (finding 1: why it outranks everything else of mine)
4. sitemaps.org, "Sitemaps XML format": each file "no more than 50,000 URLs" and "no larger than 50MB"; above that,
   split and use a sitemap index. https://www.sitemaps.org/protocol.html (finding 4, must-fix 3b)
5. Scrapy documentation, Settings: `CONCURRENT_REQUESTS_PER_DOMAIN` default 1 (fallback 8), `DOWNLOAD_DELAY` default
   1 (fallback 0), `ROBOTSTXT_OBEY` default True. https://docs.scrapy.org/en/latest/topics/settings.html
   (finding 2: the yardstick a Python developer brings)
6. RFC 9309, Robots Exclusion Protocol, §2.2.4: crawlers "MAY interpret other records that are not part of the
   robots.txt protocol"; crawl-delay isn't defined. https://www.rfc-editor.org/rfc/rfc9309.html (finding 2: robots
   pacing is usually absent)
7. Google Search Central blog, "A note on unsupported rules in robots.txt" (2019): crawl-delay among the unsupported
   rules, code handling them retired 1 Sep 2019.
   https://developers.google.com/search/blog/2019/07/a-note-on-unsupported-rules-in-robotstxt (finding 2)
8. Common Crawl FAQ: "Our CDX API endpoint is frequently abused and therefore heavily rate limited … your IP address
   may be temporarily blocked … please wait 24 hours". https://commoncrawl.org/faq. Also `https://index.commoncrawl.org/`
   answered HTTP 503 to this review's fetch on 10 Oct 2026. (S1 kept: the default seeding calls this service)
9. crt.sh Google Group, "crt.sh slow and unusable for the past 24 hours - 502 Bad Gateway errors" (2020; anecdotal).
   https://groups.google.com/g/crtsh/c/_xdEUGq_xwA (S1 kept: the second outside service the default calls)
10. Screaming Frog, SEO Spider pricing: the free version crawls 500 URLs, paid removes the limit.
    https://www.screamingfrog.co.uk/seo-spider/pricing/ (the tool a sitemap shopper otherwise reaches for; it's why
    "list of a site's URLs from one command" is the selling line in must-fix 2)
11. docs.rs, `spider` crate, `Website`: `with_respect_robots_txt`, `with_delay` ("Delay between request as ms"),
    `with_subdomains`. https://docs.rs/spider/latest/spider/website/struct.Website.html (the Rust alternative a
    shopper compares; delay and subdomain scope are explicit options there, which is why finding 2's number belongs
    on the page)
12. Code: Rust-sitemap `32c2651` (no `LICENSE`; `pyproject.toml:10-11`; `src/state.rs:437,442`;
    `src/orchestration/export.rs:17`; `src/sitemap_writer.rs:134`); sdist 0.1.3 (`src/state.rs:283,285`;
    `src/cli.rs:32,40,58`; `src/frontier.rs:669`; `src/main.rs:387-447`; `src/sitemap_writer.rs`; no `LICENSE`);
    Scrapy `96e7a1a` (`Scraping_project/src/settings.py:139-190`, `start.py:345`, `Dockerfile:12-41`,
    `requirements.txt`: 143 pins, `README.md:496-501`); GitHub REST `repos/BenjaminSRussell/Rust-sitemap`
    (`license: null`, description) and `repos/BenjaminSRussell/Scrapy` (`MIT`).
