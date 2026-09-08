# Evolve Data Center Solutions — website (2026 rebuild)

Static, review-stage rebuild of [evolveincorporated.com](https://www.evolveincorporated.com/) for Evolve Data Center Solutions. Built from the governed September 7, 2026 handoff (copy packages COPY-001 A–D, architecture ARCH-001, design system DS-001, governance GOV-001) with the visual direction of the 2026 WordPress mockup: black, white and Evolve red, condensed uppercase display type, real project photography.

## Quick start

```bash
python3 build.py      # regenerates dist/ from content/ and public/
python3 check.py      # blocked-claim, link, image, metadata and sitemap validation
python3 -m http.server 8787 --directory dist   # local preview at http://localhost:8787/
```

No dependencies beyond Python 3.8+. The generated `dist/` folder is committed so Netlify deploys it directly (`netlify.toml` sets `publish = "dist"`, no build command).

## Repository layout

| Path | Purpose |
|---|---|
| `content/` | Governed copy packages and the page approval ledger. **Source of truth for every word on the site.** Only pages whose ledger decision starts with `READY` are built. |
| `data.py` | Site identity, governed proof claims, navigation, footer, forms, redirects, image registry and per-page presentation hints. |
| `build.py` | Generator. Parses each page's publishable copy, classifies sections into components (hero, proof bar, lifecycle rail, cards, steps, FAQ, callouts, forms) and writes `dist/`. |
| `check.py` | Post-build gate. Fails on blocked claims, broken links, missing images, duplicate metadata, gated routes or sitemap mismatches. |
| `public/` | Static assets copied into `dist/`: stylesheet, script, approved logos, favicon crops and optimized photography. |
| `scripts/process-images.sh` | Regenerates `public/img/` derivatives from the raw photo staging folder (not committed). |
| `docs/` | Brand rules and review notes. |
| `dist/` | Generated site, including `_redirects`, `_headers`, `sitemap.xml`, `robots.txt`, `404.html` and `build-manifest.json`. |

## Governance rules encoded in the build

- Proof statistics render only from `CLAIMS` in `data.py` (2,200+ mission-critical projects, 5,300+ MW deployed, 20+ years in business, zero injuries since 2010) and carry `data-claim-id` attributes.
- Pages marked DO NOT PUBLISH in the ledger (eLERT, Evolution Series, sector market pages, Careers, legal pages) are never generated, linked, or listed in the sitemap.
- `check.py` scans every page for retired figures, product superlatives, customer names, international claims, compliance credentials and editorial leakage.
- Editorial and implementation language in the copy packages is stripped or softened in `prepare_public_body()`; the copy files themselves are never edited.

## Imagery

All photographs are Evolve-owned project photography extracted from the August 2026 qualification decks and the Evolve Website Build folder: the modular fabrication shop, module steel frames, crane sets, installed modules, power modules, switchgear and data-hall interiors. No stock, renders, customer names or identifiable projects are used, in line with the brand guideline. The four approved logo files are used unmodified; the favicon is a crop of the approved red "e".

## Review build

`REVIEW_BUILD = True` in `data.py` adds `noindex` to every page, a `Disallow: /` robots file, an `X-Robots-Tag: noindex` header, a review pill and a footer note. Forms use Netlify Forms with a honeypot; submissions land in the Netlify dashboard and are not routed anywhere. Flip the flag to `False` for production and reconnect forms to the approved CRM path.

## Deploying to Netlify

1. In Netlify, choose **Add new site → Import an existing project → GitHub** and pick `mcatnipp/Evolve2026`.
2. Leave the build command empty and the publish directory as `dist` (read from `netlify.toml`).
3. Deploy. Legacy URL redirects and security headers are applied from `dist/_redirects` and `dist/_headers`.

## Open items before publication

See `docs/REVIEW-NOTES.md` for the full list. The headline items are the 12 launch blockers from the prelaunch QA report (page approvals, form routing and privacy, complete legacy redirect export, contact and safety reconfirmation, insight reviewers, staging QA, analytics, hosting checks, legal pages, eLERT and Evolution Series scope, the maintenance metric, and custom 404 verification).
