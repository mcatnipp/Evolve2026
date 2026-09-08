# Review notes — Evolve website, build of September 8, 2026

## What this review build contains

- 42 governed pages (September 8 afternoon build adds a Solutions section of seven pages and a Leadership page): Home; Design & Build hub and its ten child pages (Planning & Feasibility, Design & Engineering, Preconstruction & Procurement, Data Center Construction, Commissioning & Turnover, Expansions & Retrofits, Modular, Hyperscale and AI Data Centers); Power Generation and Backup Power Systems; Service & Maintenance and Preventive Maintenance; Data Center Markets, Colocation and Enterprise; Insights hub and eight technical guides; About; Contact; Support; Start a Project; Request Service; form confirmation; HTML sitemap.
- 31 legacy and draft URL redirects (one-hop 301 at the host), a branded 404, XML sitemap, robots file, security headers.
- Four Netlify-backed forms (general inquiry, support, project brief, service request) with honeypot spam control.
- Structured data: Organization, WebSite, WebPage/CollectionPage/ContactPage/AboutPage, Service and BreadcrumbList. FAQ and Article schema are intentionally withheld until eligibility and reviewer requirements are met.

## Design decisions taken for review

| Decision | Choice | Why |
|---|---|---|
| Visual direction | Black, white and Evolve red; condensed uppercase display headings; full-width dark mega menus; photo and mosaic heroes | Matches the 2026 WordPress mockup while staying inside the DS-001 palette and logo rules |
| Typography | Barlow Condensed (display) and Barlow (body) via Google Fonts | Free, close to the Nimbus Sans Narrow direction, and the mockup already uses Barlow Condensed. Swap for licensed Nimbus files if the brand owner requires them (DS-001 hold FONT-001) |
| Imagery | Evolve deck photography plus 44 photographs imported from the 2026 mockup and evolveincorporated.com, renamed with descriptive filenames; every page has a hero and a supporting image | Stock use approved for the review build on 2026-09-08 (M. Atnipp); all evolveincorporated.com imagery is cleared for use; mockup stock licenses still need confirmation before production |
| Photo resolution | Interior heroes use split layouts and 2×2 mosaics | Most deck photos are 300–1,000 px wide, so full-bleed use would look soft. Higher-resolution originals will allow full-bleed heroes on interior pages |
| Copy | Verbatim from COPY-001 with the QA-approved removals of editorial language | No new Evolve facts were introduced |
| Proof | Static, crawlable statistics only | No animated counters (recovery report conflict register) |

## Copy adjustments made in code (not in the copy packages)

- Removed "Save the confirmation reference shown on this page" and "Keep the confirmation reference for follow-up" because no reference is generated.
- Softened the Evolution Series card on the Power page to "Detailed product information will be published after technical and legal review."
- All other removals mirror the September 7 QA fix list (FIX-003 editorial leakage) and are listed in `prepare_public_body()` in `build.py`.

## Held content (not built)

Evolution Series; Power Planning & Integration; On-Site & Bridge Power; Power Generation Maintenance; Critical Infrastructure Maintenance; Facility Assessments; Emergency Service; eLERT and its assessment form; Edge & Distributed; Healthcare; Financial Services; Telecommunications; Government & Education; Energy & Industrial; Careers; Privacy Policy; Accessibility; Terms of Use. Each needs the named approval recorded in the approval ledger (decisions AD-002 to AD-006).

## Assets still needed

- Higher-resolution photography of fabrication, installation, power modules and data-hall interiors, plus at least one people-forward field photo per the brand guideline.
- Approved Open Graph share image (a fabrication-shop crop is used as a placeholder).
- Confirmation that the red "e" crop may serve as favicon and app icon.
- Leadership headshots: two people (Molly Petty, Krista Bouquet) have no photograph anywhere and show a placeholder tile; five headshots need wardrobe retouching or a reshoot to meet the standard (caps on Clay Bludau, Bo Williamson and Steven Eickenhorst; tie on Zeeshan Siddiqui; casual shirt on Doug Herron and Tye Johnson). Four sources are under 400 px. Details and retouch briefs are in the image catalog sheet.

## Before publication (from the prelaunch QA report)

ISSUE-101 page approvals · ISSUE-102 form routing, privacy notice, retention and consent · ISSUE-103 complete legacy URL export · ISSUE-104 contact and safety reconfirmation · ISSUE-105 named reviewers and dates on the eight insights · ISSUE-106 browser, device and assistive-technology QA on staging · ISSUE-107 analytics and consent plan · ISSUE-108 hosting headers, TLS and caching checks · ISSUE-109 legal pages · ISSUE-110 eLERT and Evolution Series scope · ISSUE-111 maintenance metric · ISSUE-112 custom 404 verification on the host.

## Approvals recorded on September 8, 2026

- Solutions pages (PAGE-900 to PAGE-960) approved for publication by Marc Atnipp, FDI Creative. Ledger decisions now read READY (APPROVED 2026-09-08).
- Stock photography approved for the review build; all imagery on evolveincorporated.com cleared for use. Mockup stock licenses remain to be confirmed before production.

## Leadership page (added September 8, 2026)

- `/about/leadership/` lists the 13 people published on evolveincorporated.com/leadership with title and LinkedIn link (Clay Bludau and Krista Bouquet have no LinkedIn profile on the current site). No biographies exist in the source material, so none are published.
- Title wording to confirm: Doug Herron is shown as "Director, Monitoring Systems" because eLERT content is held (AD-006); Krista Bouquet's current listing gives a department, "Evolve Power Generation", rather than a title. Abbreviated titles (CEO, CFO, COO) are spelled out.
- Headshot template (`scripts/headshot-template.swift`, macOS Vision + Core Image): face-aware 4:5 crop, subject lifted onto a neutral studio backdrop, black-and-white grade, 800x1000 and 400x500 outputs in `public/img/team/`. The template cannot change clothing or remove hats; those items are flagged per person in the image catalog for a retoucher or a reshoot.
- Navigation: About is now a mega menu (Company, Connect, Insights). Legacy `/leadership` and `/leadership/<name>` URLs redirect to the new page.
- Structured data: Person entries (name, jobTitle, image, sameAs LinkedIn) inside an ItemList, plus the Organization node.

## Fact audit against the current site and the handoff (September 8, 2026)

Sources compared: evolveincorporated.com as served on 2026-09-08 (its statistics are animated counters, so the target values were read from the page scripts), the handoff claims ledger (GOV-001 recovery report) and the August 2026 qualification decks it cites.

| Fact | Current site | Handoff claims ledger | Review site | Result |
|---|---|---|---|---|
| Power deployed | "5.3 GW+ Deployed"; "over 5.3 gigawatts" (Design & Build page) | CLM-007: 5,300+ MW, with a note not to restate as GW | 5.3+ GW / "more than 5.3 GW" | Changed to GW on 2026-09-08 at Marc Atnipp's direction (CHG-002). Same quantity as CLM-007 |
| Projects completed | 2,000+ (About counter); 50+ (Design & Build counter) | CLM-006: 2,200+ mission-critical projects (decks, Aug 2026) | 2,200+ | Review site follows the newer approved decks; the current site is internally inconsistent |
| Years in business | 25+ Years Experience (About counter) | CLM-008: 20+ years; CLM-009: founded 2004 | 20+ years; founded 2004 | Conflict on the current site (25+ vs a 2004 founding). Evolve to confirm the founding year and the years figure |
| Safety | not stated | CLM-010: zero injuries since 2010 | Zero injuries since 2010 | Asset-sourced; reconfirm at launch (ISSUE-104) |
| Address | 10555 Cossey Road, Houston, Texas 77070 | CLM-039 | Same | Match |
| Main phone | (832) 375-0099 | CLM-039 | 832-375-0099 | Match |
| Second phone | (832) 375-0097 in the footer | not in ledger | not shown | Confirm purpose (fax or support line) before adding |
| Email addresses | Sales@EvolveIncorporated.com, support@evolveincorporated.com | not in ledger | not shown; forms only | Decision needed: publish addresses or keep forms only |
| $1B projects managed and partnered | About counter | CLM-023: do not publish | not shown | Excluded per ledger |
| 24/7 or 24/7/365 support | all service pages | CLM-031: do not publish | not shown | Excluded per ledger |
| 1,000+ customers or facilities maintained | Power Generation and Preventative Maintenance pages | CLM-015/017: conflicted, do not publish | not shown | Excluded pending a defined metric (ISSUE-111) |
| 0% downtime focus | Power Generation page | CLM-029: do not publish | not shown | Excluded per ledger |
| Contract number 25/033MR-15 and CP seal | footer | CLM-038: do not publish | not shown | Excluded per ledger; confirm whether the cooperative contract must be displayed |
| Leadership names, titles, LinkedIn | 13 people on /leadership | CLM-040 flags Clay Bludau's title as "to be confirmed" | 13 people; titles as on the current site with two edits | Names and links match. Confirm Clay Bludau's title (President on the current site), Doug Herron's wording and Krista Bouquet's title |
| Services and markets named on the current site | Design & Build, Power Generation, Preventative Maintenance, eLERT Monitoring, Evolve Energy; Telecom, Energy, Hospitals, Colocation, Crypto-Mining, Schools & Government, Modular | Held items AD-002 to AD-006 | Design & Build, Power Generation, Service & Maintenance, Solutions, Markets (Colocation, Enterprise) | Structure follows the approved architecture; eLERT, Evolve Energy and five markets remain held |
| Lifecycle | not used as a framework | CLM-004: Plan, Design, Build, Power, Maintain | Used throughout | Approved |

## Change log

| Change ID | Date | Change | Reason | Directed by |
|---|---|---|---|---|
| CHG-002 | 2026-09-08 | CLM-007 wording changed from "5,300+ MW of power deployed" to "5.3+ GW of power deployed" in `data.py`, all copy packages and the README. | Matches the current site's "5.3 GW+ Deployed"; the ledger note against GW restatement is superseded by this direction. | Marc Atnipp, FDI Creative |
| CHG-003 | 2026-09-08 | Leadership headshot grid reduced to six across on desktop (four on tablet), with the 400 px derivative served on high-density screens. | Larger tiles upscaled low-resolution source photos and looked soft. | Marc Atnipp, FDI Creative |

## Direct-response round (September 8, 2026, afternoon)

Directed by Marc Atnipp: emergency contact in the header and footer; market research per service line with blind spots; copy developed in a Dan Kennedy direct-response style within the approved facts; Russell Brunson lead-generation funnels; headline effectiveness testing. Everything is documented here and in the linked files.

### Emergency contact

- Utility bar: "24/7 emergency service: 832-375-0099" and support@evolveincorporated.com. Footer: emergency block with the phone, support email, the existing-customer support portal (support.evolveincorporated.com) and the online service request. Values come from the current site's footer and service pages; the second number on the current site, (832) 375-0097, is a fax line (icon on the current site) and was not added.
- Reconfirm with Evolve that the line is staffed around the clock; if not, the label drops "24/7". The ledger's rule against response guarantees is respected: no response time is promised anywhere.

### Copy (Dan Kennedy style, fact-bound)

- Rules: `docs/copy-voice-guide.md`. The only facts allowed are CLM-001 to CLM-014 and CLM-039.
- Headline layer (H1, hero intro, calls to action, final call to action) on all pages: `scripts/apply-headlines.py`. Body sections rewritten page by page in the copy packages and validated by `scripts/validate-copy.py` (blocked claims, banned words, promise language, new numbers, structure) plus the build gate.
- Page-by-page record: `docs/copy-system-2026-09-08.md`.

### Funnels (Russell Brunson lead generation)

- Five PDF guides exported from the approved Insights (`scripts/make-pdfs.sh`), each with a squeeze page under `/resources/`, a thank-you page with the download and the next-step application, and mid-page offer bands on the matching service pages. The project brief now qualifies on facility type, capacity, stage, site status and timeline. The generic thank-you page carries a "what happens next" ladder.
- Map, forms, follow-up email sequences and metrics: `docs/funnels-2026-09-08.md`.
- Nine Netlify forms in total; notifications route to marc@fdicreative.com for review.

### Headline test

- Every page's H1 has three variants (control plus two challengers, `docs/headline-variants.json`). Each was scored by a heuristic model and by a blind three-persona buyer panel (developer, facilities director, owner's engineer). Winners were applied; runners-up are the first live split test once analytics exist. Report: `docs/headline-test-2026-09-08.md`.

### Market research and blind spots

- Five reports in `docs/research/` (design-build, modular/edge/AI, power generation, service and maintenance, markets and buyers), each with dated sources and actions labeled "site change now", "needs Evolve fact or approval" or "new offer". Consolidated discussion list: `docs/market-blind-spots-2026-09-08.md`.

### Also found during this round

- Canonical domain: the current site serves from the apex domain; `www.evolveincorporated.com` does not respond over HTTPS. The build's canonical base URL is now `https://evolveincorporated.com`.
- Around 1 PM Central on 2026-09-08 the current site stopped answering over HTTPS from this machine ("tlsv1 alert protocol version") and returned HTTP 406 over plain HTTP. It had served normally earlier in the day. Evolve's host should check the certificate and TLS configuration.
