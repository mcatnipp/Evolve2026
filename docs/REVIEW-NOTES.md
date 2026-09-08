# Review notes — Evolve website, build of September 8, 2026

## What this review build contains

- 34 governed pages: Home; Design & Build hub and its ten child pages (Planning & Feasibility, Design & Engineering, Preconstruction & Procurement, Data Center Construction, Commissioning & Turnover, Expansions & Retrofits, Modular, Hyperscale and AI Data Centers); Power Generation and Backup Power Systems; Service & Maintenance and Preventive Maintenance; Data Center Markets, Colocation and Enterprise; Insights hub and eight technical guides; About; Contact; Support; Start a Project; Request Service; form confirmation; HTML sitemap.
- 31 legacy and draft URL redirects (one-hop 301 at the host), a branded 404, XML sitemap, robots file, security headers.
- Four Netlify-backed forms (general inquiry, support, project brief, service request) with honeypot spam control.
- Structured data: Organization, WebSite, WebPage/CollectionPage/ContactPage/AboutPage, Service and BreadcrumbList. FAQ and Article schema are intentionally withheld until eligibility and reviewer requirements are met.

## Design decisions taken for review

| Decision | Choice | Why |
|---|---|---|
| Visual direction | Black, white and Evolve red; condensed uppercase display headings; full-width dark mega menus; photo and mosaic heroes | Matches the 2026 WordPress mockup while staying inside the DS-001 palette and logo rules |
| Typography | Barlow Condensed (display) and Barlow (body) via Google Fonts | Free, close to the Nimbus Sans Narrow direction, and the mockup already uses Barlow Condensed. Swap for licensed Nimbus files if the brand owner requires them (DS-001 hold FONT-001) |
| Imagery | Real Evolve project photography from the qualification decks only | Brand guideline bans stock and renders; AI renderings in the asset library are excluded |
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
- Leadership content (names, titles, bios, photographs) if a Leadership page is wanted; the current site lists 13 names with no bios or photos.

## Before publication (from the prelaunch QA report)

ISSUE-101 page approvals · ISSUE-102 form routing, privacy notice, retention and consent · ISSUE-103 complete legacy URL export · ISSUE-104 contact and safety reconfirmation · ISSUE-105 named reviewers and dates on the eight insights · ISSUE-106 browser, device and assistive-technology QA on staging · ISSUE-107 analytics and consent plan · ISSUE-108 hosting headers, TLS and caching checks · ISSUE-109 legal pages · ISSUE-110 eLERT and Evolution Series scope · ISSUE-111 maintenance metric · ISSUE-112 custom 404 verification on the host.
