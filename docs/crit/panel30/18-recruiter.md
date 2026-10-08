# Crit 18 — the technical recruiter

Ten years agency and in-house, non-engineer, sixty profiles a day. I gave this what I give every profile: an 8-second scan of page-day-top.png, a 60-second scroll of page-day-full.png, then README.md and README.draft.md read as text with Ctrl-F, which is how I actually work.

## 1. The 8-second scan

My eye goes: huge "Ben Russell", the italic line under it, the blue link row, then I hunt for role / city / status. The current italic line, "I build crawlers that survive the open web, and the systems that make sense of what they bring back", lands: crawlers, backend, data. The box lower left says "Full-stack developer · scraping enthusiast", but it is inside the picture; I read it late and "enthusiast" says hobbyist. Then nothing. No role, no location, no "open to". I am already deciding whether to open the next tab.

The draft replaces the italic line with "I survey a web that is wrong about itself." For me that is a step backward: a riddle, and I have no time for riddles. Keep it if the designers love it, but the plain sentence must then exist somewhere I can see it without decoding a chart.

Search terms I would type (GitHub, Ctrl-F, our ATS), as plain text: Python (weak now, present in draft), Rust (yes), crawler (yes), PostgreSQL / Redis / Kubernetes / Docker (yes, in the bullets), TypeScript / Swift / Go / C (legend image only now; one sentence in the draft), "data pipeline" or "data infrastructure" (absent in both), "engineer" or "full-stack" (once in prose now; in the draft it moves into the hero image), location / role / years / LinkedIn / résumé (absent; the draft has an HTML comment, which I cannot see). Everything inside an SVG is invisible to me, to Ctrl-F and to every sourcing tool I own; the type is outlines, so it is not even selectable. The legend sheet, which is literally the keyword list, is a picture.

## 2. What is good

- The link row: rustmapper · Scrapy · PyPI · Email. A shipped PyPI package is a credential I can verify in one click, and Email is a contact path. 
- The bullets under each system are the best recruiter text here: "Up to 512 workers", "write-ahead log", "Delta Lake, PostgreSQL, Redis", "Docker and Kubernetes manifests, 90%+ test coverage". Hiring managers' words.
- Notices to mariners read senior. "Boring under load" and "dashboards and breakers go in version one" are lines I would quote in the submittal email.
- Memorable. Out of sixty, this is the one I would describe to a colleague ("the nautical chart guy").

## 3. What is bad, ranked

1. **No position line.** Role, seniority, city or timezone, availability: none. The single most damaging thing on the page. I cannot tell whether this is a student, a senior backend engineer, or someone outside the countries I can hire in, and a profile I cannot place gets closed, not messaged. The draft's HTML comment is a note to Ben, not a fix. About half my colleagues stop here.
2. **The job title lives in an image.** "Full-stack developer · mostly crawlers, lately in Rust" is a fine line and the spec sets it in the cartouche, as outlines, in an SVG. Plain text first, chart decoration second.
3. **"Scrapy" collides with the framework.** My one-liner to the hiring manager would have read "Scrapy contributor", wrong and embarrassing for both of us. The draft's "not the framework itself" arrives in paragraph four; the hero island, link row and H2 say Scrapy with no gloss. rustmapper has three names (Rust-sitemap, rustmapper, Rustmapper Shoal).
4. **The headings are not my words.** Approaches, Soundings, Ship's log, Notices to mariners, Instruments, Other waters. I skim for Projects, Skills, Experience, Contact. "Five corrections" does not say Principles; only "the stack" lands.
5. **The stack is a picture.** Legend now, Instruments in the draft. One plain sentence is not the whole stack.
6. **Seniority cues missing.** Joined Oct 2024, "enthusiast", no employer, years or education, all solo repos. Not asking anyone to invent these; if Ben has them they are the second most valuable text on the page, and there is no slot.
7. **Contact path is thin.** No LinkedIn, no résumé. The résumé is what I forward; a mailto is what I use to ask for one, which costs a day.
8. **The metaphor's toll** is about ten seconds before the first useful fact. I have eight.

## 4. What needs to be done

1. **Position line, plain text, directly under the link row.** Ben fills the blanks, nothing invented: `{Role} · {City or timezone} · {Open to / currently}`. Mirror it in the cartouche, but the markdown line is the one that counts. The page should not ship with the comment in its place.
2. **"At a glance" block in plain text** above the first sheet, three mono lines or a two-column table: *Builds:* crawlers and data infrastructure · *Languages:* Python, Rust, Swift, C, TypeScript, Go · *Runs on:* Delta Lake, PostgreSQL, Redis, Docker, Kubernetes, Prometheus, Grafana. It replaces the Instruments SVG or sits beside it.
3. **Subheads in my words**, searchable as H2 text: "Approaches · projects", "Notices to mariners · principles", "Instruments · stack", "Other waters · more projects".
4. **Disambiguate Scrapy at first mention everywhere:** link row "Scrapy (platform)", first bold line "a crawler platform built on the Scrapy framework", hero island renamed to the platform's own name. Better: rename the repo.
5. **Contact row:** LinkedIn and Résumé slots beside Email; omit only if Ben truly has neither.
6. **GitHub profile fields**, which is where recruiters actually search: bio carrying the plain line, location, website, the hireable toggle, the two systems pinned. The README cannot do this; a checklist for Ben can.

## 5. Improvements and ideas

- **Text-only CI check (bold).** A build step renders README.md with images stripped and fails if the position line is still a comment or any of a keyword list (Python, Rust, crawler, PostgreSQL, Kubernetes, data) is missing from plain text. The SVGs are tested for size and validity; test the page for recruiters the same way.
- **Ship's papers: a one-page résumé PDF** in the repo, drawn by the same chartlib system, linked from the link row. Recruiters forward PDFs, not profiles; the design travels to the one document the signer reads. Content is Ben's.
- **Sailing directions.** Two plain lines near the top: what he wants to work on next and with what kind of team. "Open to" is the highest-response phrase in my inbox, and in his voice it is also a layer of meaning: the chart has a destination.
- **Every sheet gets a plain-text twin.** Alt text is excellent and no recruiter sees it. Follow each image with one markdown line that says the same thing in my register.

## 6. What the page says now, and what it should say

Now: a tasteful, articulate, probably early-career solo builder who loves crawlers and design, lives somewhere, might be a student or a senior engineer, and cannot be placed in a search or a pipeline. The chart is beautiful and it stands between me and him. It should say, on the first screen and in plain text: what I am, what I build and in what, where I am and what I want, how to reach me and where the résumé is; then the chart, as proof that he also has taste.

## 7. Five most important lines

1. Add a plain-text position line (role · city/timezone · open to) directly under the link row; the HTML comment is not a fix, and its absence closes the tab for half of recruiters.
2. Every keyword inside an SVG is invisible: put the job title, languages and stack in markdown text and demote the Instruments/legend image to decoration.
3. Disambiguate "Scrapy" at first mention and use one name for rustmapper; today my summary to a hiring manager would be wrong.
4. Headings must carry recruiter words as searchable text: projects, principles, stack, contact.
5. Add LinkedIn and résumé slots beside Email, fix the GitHub bio/location/hireable fields, and add a text-only CI check so the page cannot ship without them.
