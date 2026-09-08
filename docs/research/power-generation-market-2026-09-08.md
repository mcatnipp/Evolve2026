# Data-Center Power Generation: 2025–2026 US Market, Buyer Questions, Competitor Positioning and Review-Site Blind Spots

**Research ID:** MKT-002 (Power service line) v1.0
**Prepared:** September 8, 2026
**Builds on:** MKT-001 v1.1 (September 7, 2026): conclusions MKT-001/002/007/018, the Caterpillar, Aggreko and ERock competitor entries, the "Data-center power" search cluster, questions AEO-026 to AEO-030B, the "Evolution Series is named but not technically defined" gap, positions P-002 and P-007, and open question RQ-003. Facts already in that document are referenced, not repeated.
**Governance:** GOV-001 v1.0. Approved Evolve facts used here: data-center specialist; Houston, Texas; founded 2004 (20+ years); Plan, Design, Build, Power, Maintain; 2,200+ mission-critical projects; 5.3+ GW of power deployed; zero injuries recorded since 2010. Nothing else about Evolve is asserted. Every open item is phrased as a question for Evolve. External figures describe the market, never an Evolve capability.
**Pages reviewed:** review build `/power-generation/` and `/power-generation/backup-power-systems/`, plus a keyword scan of all 43 built pages in `dist/` (a `/resources/` section with five gated PDF guides, including a site-selection and power-planning checklist, was added to the build by another workstream while this research ran; those pages were scanned too and contain none of the power topics below); the current site's `/power-generation` page (local copy). The current `/evolve-energy` page could not be retrieved (the server rejected every fetch), so Evolve Energy is treated only as "an affiliate that markets powered sites."

---

## 1. Market snapshot, 2025–2026

| Topic | Dated evidence | Status | Why it matters for the Power pages |
|---|---|---|---|
| National interconnection queues | 2,061 GW of generation and storage was actively seeking interconnection at the end of 2025; the median project reaching operation in 2025 had waited 61 months, up from 36 in 2015 (LBNL, *Queued Up: 2026 Edition*, June 2026). | Fact | Buyers arrive already convinced the grid is slow; they want to know what can be energized sooner. |
| Federal large-load reform | DOE directed FERC on Oct. 23, 2025 to accelerate large-load interconnection (White & Case, Oct. 2025). On June 18, 2026 FERC issued show-cause orders to all six RTOs, defining a large load as >50 MW at >69 kV; responses were due Aug. 17, 2026 (FERC; White & Case, June 2026). | Fact | Rules will keep moving through 2027. Inference: buyers value a partner who tracks them, but the site cannot claim interconnection consulting until approved. |
| ERCOT large-load queue | 63 GW at end-2024 → 226 GW in Nov. 2025, ~77% data centers (Latitude Media, Dec. 3, 2025, citing ERCOT's Dec. 2, 2025 planning update) → 233 GW at end-2025, >70% data centers, ~300% annual growth; ERCOT's VP of system planning: "We have outgrown the process" (Utility Dive, Jan. 6, 2026) → reported above 410 GW (RTO Insider, Sept. 4, 2026). | Fact | Evolve is headquartered in the most congested large-load market in the country and the review site never mentions ERCOT or Texas outside the footer address. |
| Houston specifically | CenterPoint has 3.5 GW of data-center load under construction, expects 8 GW energized by 2029 and 12.2 GW "firmly committed"; its CEO calls Houston "firmly established as a location of choice" for hyperscalers (Utility Dive, Apr. 23, 2026). A Bloom Energy survey projects Texas at 30% of US data-center load by 2028 (Bloom, Jan. 20, 2026). | Fact (Bloom figure is survey-based) | Local demand is large enough to justify a Houston/Texas power path on the site. |
| Texas SB 6 and PUCT rule | SB 6 (signed June 2025) covers loads ≥75 MW: interconnection standards, disclosure of on-site backup generation sized at ≥50% of load, and ERCOT authority to require deployment of that backup generation or curtailment during grid emergencies (Utility Dive, June 2025; McGuireWoods, July 2025). PUCT voted Mar. 12, 2026 to publish draft 16 TAC §25.194 implementing it (Greenberg Traurig, Mar. 2026). ERCOT's "Batch Zero" (filed Mar. 2026) fast-tracks loads with site control and executed agreements; controllable-load and bring-your-own-generation pathways reward on-site generation (PA Consulting; GPU Lease Index guide, 2026, secondary). | Fact; pathway detail is secondary-sourced | Backup generation is now a regulatory asset in Texas, not just insurance. Nobody on the review site says so. |
| Texas Backup Power Package | PUCT adopted the rule May 7, 2026: $1.8 billion under the Texas Energy Fund, grants up to $500/kW, projects ≤2.5 MW at critical facilities (hospitals, water, emergency services); applications expected late 2026 or 2027 (PUCT, May 7, 2026; Univ. of Houston, 2025). | Fact | Not a data-center program. Relevant only if Evolve still serves the hospitals, schools and utilities listed on its current site (question for Evolve). |
| Behind-the-meter (BTM) and on-site generation | 46 data centers planning 56 GW of BTM power, ~30% of planned US capacity, 90% announced in 2025 (APPA summarizing Cleanview, Feb. 21, 2026). Cleanview's mid-2026 update: 59 facilities, ~90 GW announced, >25% of planned capacity, only ~2 GW operating (2.2%), 2.8–3.2 GW expected by end-2026 and 5–10 GW by end-2027; predominantly natural gas (Cleanview, mid-2026). Bloom's survey expects roughly one-third of data centers to run on 100% on-site power by 2030 and finds utility delivery timelines 1.5–2 years longer than developers expect (Bloom, Jan. 20, 2026). | Fact | On-site and bridge power is the fastest-growing power conversation, and the review site has no page for it (PAGE-240 is gated). |
| Reciprocating gas engines | INNIO's largest order ever: 2.3 GW for VoltaGrid, 92 packs × 25 MW (INNIO, Oct. 21, 2025). Caterpillar, Boyd CAT and AIP: 2 GW of G3516 sets, deliveries Sept. 2026–Aug. 2027, zero-to-full load in ~7 seconds (Caterpillar, Jan. 28, 2026). Wärtsilä 412 MW in Ohio and 1.6 GW across four US data-center projects; INNIO–Rehlko 1.25 GW framework; Nscale/Caterpillar 2 GW in West Virginia (Power Engineering, Apr. 16, 2026). Utilities are quoting developers "three to seven years" for grid power (POWER, Oct. 28, 2025). | Fact | Engines, not turbines, are the default bridge/prime technology at 1–3 MW blocks. |
| Gas turbines | GE Vernova: 100 GW under contract in Q1 2026 (44 GW backlog + 56 GW slot reservations), ~20% data-center customers, ~3-year lead times on heavy-duty units, only ~10 GW of capacity left across 2029–2030 (Power Engineering, Apr. 23, 2026); backlog reported at 116 GW after Q2 (Turbomachinery, 2026, not opened). PROENERGY: 13 × 50 MW PE6000 aeroderivative sets for Crusoe, 5-minute start (PROENERGY, Apr. 2026). | Fact | Turbines are a hyperscale/developer play; the site should explain when they apply rather than sell them. |
| Fuel cells | Bloom Energy on track for 2 GW of annual production by end-2026 (Utility Dive, accessed Sept. 8, 2026); large Oracle and AEP offtake deals reported in early 2026 (EnkiAI summaries, secondary). | Fact / secondary | A credible options page must at least define the category. |
| Batteries and BESS | Data-center BESS is typically sized for 2–4 hours and is used for AI load transients and grid services; AIP's 2 GW gas campus pairs engines with BESS; Oracle has multiple BESS deployments (Data Center Knowledge, May 15, 2026). 438 GWh of global storage installations projected for 2026, +62%; the same piece asserts generator backup coverage has fallen to 15–40% on some new projects (ESS News, July 15, 2026; single-source claim). Generac and EPC Power launched integrated BESS for data centers (Generac, Mar. 2026). | Fact; the 15–40% figure is a single-source claim | Buyers now ask "generator plus BESS?" as a design question. |
| Generator lead times | Diesel 1,250–3,250 kW: 52–70 weeks; 750–1,000 kW: 12–39 weeks; 4,000 A transfer switches: 31 weeks; start procurement 12–18 months ahead and consider surplus units or alternate OEMs (Global Power Supply, May 11, 2026). Caterpillar Q2 2026: backlog $72.1 billion, Power Generation sales +29% to $3.1 billion "primarily in data center applications," orders extending to 2030, and a restart of its 10 MW medium-speed gas platform (~1.5 GW) (Caterpillar, Aug. 4, 2026; Manufacturing Dive; CNBC). Generac bought a Sussex, WI plant for data-center demand (IEN, Jan. 2026). A reported $150 million Cummins Fridley expansion (Feb. 2026) appears only in a secondary blog and is unverified. | Fact (Cummins item unverified) | Lead time is now a design input. Any Evolve statement about delivery speed remains DO NOT PUBLISH. |
| Outage risk | Power is still the leading cause of impactful outages; UPS, transfer-switch and generator failures dominate; grid constraints and high-density loads add new pressure; 57% of major outages cost >$100,000 and 1 in 5 >$1 million (Uptime Institute, May 13, 2026). Power caused 45% of impactful outages (Network World, May 14, 2026). Uptime's 2026 Resiliency Survey (1,035 respondents, Q1 2026) as reported: 39% cite UPS failure, 34% transfer switches, 28% generator failure (Direct LTx, 2026). | Fact (survey) | Maintenance and testing content has a market-sourced reason to exist. |
| Fuel and testing standards | 12 hours of on-site fuel at N load is the Tier baseline; Tier III/IV fuel paths must be concurrently maintainable or fault tolerant (Uptime Institute Journal, accessed Sept. 8, 2026). NFPA 110: annual load-bank test (30/50/75% sequence) when monthly runs do not reach 30% load, a full-load test every 36 months, and a written maintenance program under §8.1.1 (Uptime Compliance, 2026; Generator Source). Contracted emergency fueling agreements with priority dispatch should be signed before hurricane season (Mansfield Energy, June 9, 2026). | Fact | Every buyer RFP asks about fuel autonomy, testing and refueling. The review site never uses the words "fuel" or "load bank" outside a disclaimer. |
| EPA emissions rules | Emergency stationary engines under 40 CFR 60 Subpart IIII may certify to Tier 2/3 rather than Tier 4 Final, limited to 100 h/yr of maintenance and testing, within which 50 h may serve non-emergency demand response (Power Generation Enterprises, 2026). EPA's May 1, 2025 fact sheet and FAQ clarified non-emergency operation for local supply support (Sidley; Kirkland, May 2025). EPA proposed on July 7, 2026 (91 FR 41591) to drop the federal 30-day public-notice requirement for minor-source permits; comments closed Aug. 21, 2026 (Environmental Protection Network, Aug. 20, 2026; Axios Atlanta, Aug. 12, 2026). | Fact | Emergency-versus-non-emergency classification decides whether a backup fleet can also be a bridge or grid asset. |
| TCEQ and Texas permitting | Common paths are Permit by Rule 30 TAC §106.511 and the natural-gas EGU standard permit (TCEQ, RG-616 revised Jan. 2026). Since 2024, 38 Texas data centers have authorized 2,100+ backup diesel generators under minor permits, permitted for ~2,500 tons/yr of NOx; 15 gas plants are tied to data centers; individual sites were permitted at 249.1 and 99.8 tons/yr, just under review thresholds (Texas Tribune, July 9, 2026). ERM notes a single incomplete resubmission can add 3–9 months (ERM, accessed Sept. 8, 2026). | Fact | Permitting is a schedule risk buyers ask about; competitors' EPC pages name it. |
| State Tier 4 trend | Virginia requires Tier 4-equivalent controls on new diesel permit applications from July 1, 2026, and its Sept. 30, 2025 DEQ memo lets Tier 2 units run for planned utility outages with ≤14 days' notice; Illinois' CRGA requires Tier 4 for new diesel backup sets (Encino Environmental, Feb. 21, 2026). | Fact | A nationwide site must acknowledge that Tier 4 is spreading state by state. |
| Decarbonization | HVO is approved by Caterpillar, Cummins, Kohler/Rehlko and Rolls-Royce mtu (BIS Research); Cummins' Centum series is approved for EN 15940 paraffinic fuels (Cummins); Generac markets HVO-compatible engines; Bridge Data Centres piloted HVO in 2026 (domain-b, 2026). | Fact | HVO is the easy decarbonization answer for standby diesel and is absent from the site. |
| Commercial models | PPAs run 10–20 years; in colocation the developer often buys power and resells it as a service inside the lease (Pillsbury). Enchanted Rock's draft IPO filing: ~1,000 MW across ~400 sites, $1.22 billion contracted backlog (+436% YoY), service contracts of 5–15 years, resiliency-as-a-service, bridge, backup and flexible-capacity modes (SEC DRS, Feb. 17, 2026). VoltaGrid raised $1 billion from Blackstone and Halliburton (VoltaGrid, May 2026). | Fact | "Who owns the asset and who is paid how" is now a first-round buyer question. |
| Rental and bridge fleets | Aggreko launched modular microgrids for data-center bridging (Aggreko, June 3, 2026). Sunbelt advertises >100 MW of temporary capacity and 13.8 kV medium-voltage units for commissioning; United Rentals sells load-bank testing for commissioning (Sunbelt; United Rentals, accessed Sept. 8, 2026). Houston's Worldwide Power Products publishes a 20 kW–2 MW rental fleet and paralleled bridge power to 40 MW (WPP, accessed Sept. 8, 2026). | Fact (self-published) | Local peers publish ranges; the review site publishes none. |

**Implication (inference):** the buyer's power question has shifted from "which generator" to "how do I get firm power on my schedule, keep it permitted, keep it fueled and tested, and decide who owns it." The review site currently answers only the coordination part of that question.

---

## 2. What buyers search for and ask

Volumes were not measured (RQ-001 remains open); phrases below are derived from competitor page titles, regulatory vocabulary and the sources above.

**Search phrases by intent**

- Speed to power: "data center bridge power," "temporary power for data center," "behind the meter power data center," "on-site power generation data center," "data center microgrid," "ERCOT large load interconnection," "SB 6 backup generation requirement," "speed to power Texas data center."
- Backup design: "data center generator sizing," "N+1 vs 2N generators," "paralleling switchgear data center," "diesel vs natural gas generator data center," "data center fuel storage 12 / 48 / 72 hours," "DCC rating generator," "Tier III generator requirements."
- Testing and maintenance: "generator load bank testing NFPA 110," "data center generator maintenance program," "integrated systems test generators," "fuel polishing data center," "emergency fuel contract generator."
- Permitting: "data center generator air permit Texas," "TCEQ permit by rule generator," "Tier 4 vs Tier 2 emergency generator," "EPA 100 hour rule," "demand response backup generator 50 hours."
- Commercial: "generator lease data center," "energy as a service data center," "bridge power rental MW," "generator lead times 2026," "2 MW generator quick delivery."
- Technology options: "BESS data center backup," "fuel cell data center," "gas turbine data center power," "HVO generator data center."

**RFP and evaluation criteria that recur in the sources**

1. Topology and redundancy: N+1, 2N, 2N+1; concurrently maintainable fuel and switchgear paths (Uptime; CSE).
2. Fuel autonomy and refueling: 12-hour Tier minimum, 48–96 hours commonly specified; contracted priority delivery (Uptime; Mansfield).
3. Genset rating and transient class: standby, prime or Data Center Continuous; ISO 8528-5 G3 response (Build.inc; Cummins).
4. Emissions classification and permit path: emergency vs non-emergency, Tier level, hour limits, state rules (EPA; TCEQ; Encino).
5. Paralleling, controls and AI-transient behavior: VoltaGrid markets ±5% voltage and ±2% frequency under 40–70% load swings.
6. Commissioning support: temporary power for Level 2–5 commissioning and load-bank/IST plans (VoltaGrid; Sunbelt; United Rentals).
7. Maintenance program: written NFPA 110 program, EGSA-certified or factory-trained technicians, parts availability (EGSA; Uptime Compliance).
8. Delivery model: turnkey EPC vs equipment supply vs RaaS/PPA/lease; asset ownership and term (Pillsbury; ERock; Enchanted Rock DRS).
9. Lead-time and slot security across gensets, switchgear and transformers (Global Power Supply; Caterpillar).
10. Texas-specific: SB 6 backup-generation disclosure and curtailment readiness for loads ≥75 MW (McGuireWoods; GT Law).
11. Decarbonization path: HVO, gas, BESS hybrid, Scope 1 reporting (BIS Research; DCK).
12. Safety prequalification: EMR and TRIR against client caps of roughly 1.0 in ISNetworld/Avetta-style systems (EHS Inc.; CrewCompliance).

**Direct questions to add to the Power FAQ set (extending AEO-026 to AEO-030B)**

- How much on-site fuel should a data center hold, and who refuels it in a regional emergency?
- When does an "emergency" generator become a "non-emergency" engine under EPA rules, and what changes?
- Which air-permit path applies to backup generators in Texas, and how long does it take?
- What does SB 6 require from a ≥75 MW load in ERCOT, and how does backup generation affect the interconnection study?
- Can standby generators be paralleled and used for bridge or demand-response duty? What does that do to warranty, emissions and hours?
- How do gas engines, gas turbines, fuel cells and BESS compare on speed, footprint, emissions and runtime?
- What load-bank and integrated-systems tests should the commissioning plan require?
- Turnkey EPC, equipment supply or a resiliency-as-a-service contract: how do responsibilities differ?
- What is the realistic order-to-energization timeline for a multi-megawatt generator package in 2026?

---

## 3. How competitors position power offers

| Competitor (type) | Page structure observed | Proof and specs | Lead magnets | CTAs | Takeaway |
|---|---|---|---|---|---|
| Caterpillar (OEM + dealer network) | Industry hub by project stage: design, installation, service, bridge power, products, resources (MKT-001 SRC-CMP-013; page timed out on re-fetch Sept. 8, 2026) | Global dealer network; customer stories; 2 GW AIP/Boyd CAT alliance with 7-second ramp claim (Jan. 28, 2026) | Application guides, customer stories | Dealer contact | Stage-based taxonomy and dealer proximity; OEM-centric. |
| Cummins (OEM) | Data-center page: Centum series, QSK95, DCC rating, HVO approval, 24/7 data-center support (search summary; page blocked fetch) | Model names, ratings, Tier III/IV language, EN 15940 approval | Spec sheets, Power Integration Center | Contact | Publishes ratings and fuel approvals as proof. |
| Generac Industrial (OEM) | Hero, three pillars, 2.25–3.25 MW platform, six differentiators, portfolio, case studies, microgrid, segments (hyperscale, colocation, edge) | 65+ years; 24/7 network; 13 MW paralleled MPS case; Tier 4 aftertreatment; HVO; 50°C cooling; 99.999% uptime case study | 2025 data-center brochure, case-study PDFs, white papers, Power Design Pro | "Talk to an Expert," "Find a Distributor" | Publishes MW range, engine and alternator names, and segment paths. |
| Mustang Cat (Houston Cat dealer) | Generic electric-power page: new sets, pre-owned, learn more | Family-owned since 1952, 35 counties, EPA compliance | None | "Contact Us," "Find a Location" | Weak data-center content locally; an opening for a Houston specialist. |
| Worldwide Power Products (Houston dealer/service) | Data-center page: hero, segments (enterprise to modular), services grid (turnkey, selection, rentals, support, parts, service), featured project | 2–4 MW new units "quick delivery," rental 20 kW–2 MW, bridge to 40 MW, load-bank testing, fuel polishing, remote monitoring, "round-the-clock" support | Power calculator, fuel-consumption charts, financing page, FAQ | "Get a Custom Power Solution," "Schedule Service," "Request a Custom Quote" | Closest Houston analogue: publishes ranges, services and financing; no certifications. |
| Aggreko (rental / bridge) | Exact-intent bridging page: problem, solution, lifecycle stages, two offers, technology, case studies, six FAQs | 25 kW–1.5 MW modular Tier 4 Final/gas, BESS 24 kW–1 MW, "deploy in days," three case studies; June 3, 2026 microgrid launch | Case studies (no gated download) | "Contact our experts," phone | Best model for a narrow bridge-power page. |
| VoltaGrid (bridge / prime developer) | Short-term bridge, long-term bridge, commissioning power (L2–L5), StabilAI platform | 1.5–2.3 GW INNIO orders, $1 billion Blackstone/Halliburton, ±5%/±2% power quality, remote operations center, case study | Gated keynote video, case study | Phone, "View Case Study," contact form | Sells firm power as a service with commissioning power as a distinct offer. |
| Enchanted Rock / ERock (on-site developer) | Data-center page: bridge-to-grid, flexible capacity, RaaS, backup; products RockBlock and ERT500; education hub | "Up to 99% lower emissions," "days or weeks" runtime; DRS: ~1,000 MW, ~400 sites, $1.22 billion backlog | White paper "Speed-to-Power Bottlenecks Undermine US AI Dominance," webinars, newsletter | "Explore Solutions," "Contact Us Today," "Access Now" | Use-case taxonomy plus a policy-flavored white paper as lead magnet. |
| Mainspring (linear generator OEM) | "Delivering power on your timeline," product, solutions, performance metrics, industries | 46% efficiency, <1.5 ppm NOx, 0–100% dispatch, >1 GW pipeline, Fortune 500 logos | Perspectives blog (Aug. 2026) | "Get Power" | Hard specs and a two-word CTA. |
| PROENERGY (turbine packager / EPC) | PE6000 product page: overview, specs, emissions, manufacturing, reliability, testing, case study | 50.2 MW, 5-minute start, 25 ppm NOx, 99% start reliability, factory test-fit before shipment | Case-study PDF | Phone | Spec-first credibility for large blocks. |
| Burns & McDonnell (EPC) | Hero, market framing, advantage, AI-era solutions, projects, named contact, insights | Names on-site power, bridging power, utility interconnection, long-lead procurement, phased substations, long-term monitoring; no numbers | White paper "Rapid Response Power Solutions Enable Large Load Centers…," underground transmission paper | "Send Us a Note," named VP contact | An EPC can compete on scope clarity and a named expert without publishing metrics. |
| Sunbelt / United Rentals (rental) | Lifecycle-phase pages (planning, construction, commissioning, maintenance); load-bank guides | >100 MW temporary capacity, 13.8 kV units, load banks for commissioning | Blog guides on load-bank rental for commissioning | Quote/branch contact | Commissioning power and load banks are productized. |

**Patterns across the set (observation):** exact-intent pages per use case; published kW–MW ranges and engine/alternator names; a commercial-model statement (rental, lease, RaaS, EPC); a permitting or emissions line (Tier 4 Final, NOx ppm, HVO); FAQs; one downloadable proof asset; a CTA that names the next step ("Get Power," "Talk to an Expert," "Get a Custom Power Solution"). None of the twelve publishes EMR, TRIR or EGSA credentials on the page, so a governed safety and credential block would be differentiating rather than table stakes.

---

## 4. Blind spots on the review site

**Method.** Keyword scan of all 43 built pages: no body-copy occurrence of bridge, on-site/behind-the-meter, microgrid, battery/BESS, fuel cell, turbine, load bank, N+1/2N, paralleling, ERCOT, Tier 4, TCEQ, NFPA, EGSA, rental, lease, PPA, financing or natural gas. "Generator" appears only in image alt text; "fuel," "interconnection" and "emission" appear only inside scope disclaimers; "Texas" appears only in the address; the header on every page reads "24/7 emergency service: 832-375-0099." The five new `/resources/` guides also contain no mention of generators, fuel, load banks, bridge power, ERCOT or interconnection, so the site's only power-adjacent lead magnet is a site-selection checklist that stops at the planning stage.

| # | Blind spot | What buyers and competitors emphasize | Review site today | Severity | Question for Evolve |
|---|---|---|---|---|---|
| 1 | On-site and bridge power as a distinct offer | ~90 GW of BTM capacity announced; Aggreko, VoltaGrid, ERock, Burns & McDonnell all run bridge/on-site pages | No page; PAGE-240 gated under RQ-003 | High | Does Evolve deliver bridge or prime on-site power (EPC, supply, O&M), and in which technologies? |
| 2 | Technology options explained neutrally | Buyers compare gas engines, turbines, fuel cells, BESS, hybrids; OEMs publish specs | Backup page says "no universal configuration" and stops | High | Which technologies has Evolve installed or integrated (gas recip, turbine, BESS, fuel cell)? |
| 3 | Speed to power, interconnection and Texas rules | ERCOT queue >400 GW; SB 6 backup-gen disclosure and curtailment; Batch Zero; CenterPoint 12.2 GW | One disclaimer sentence; no Texas or ERCOT content | High | Does Evolve support utility/ERCOT applications, load studies or SB 6 compliance planning? |
| 4 | Permitting and emissions support | EPA emergency/non-emergency rules; TCEQ PBR and standard permit; Tier 4 spreading; 3–9 month resubmission risk | "Emissions" appears once as a project-specific variable | High | Does Evolve prepare or coordinate TCEQ/EPA generator permits and emissions strategy? |
| 5 | Generator maintenance, load-bank and NFPA 110 program | NFPA 110 written program and annual load-bank testing; EGSA-certified technicians; UPS/ATS/generator failures lead outages | PAGE-320 gated; no load-bank mention even in the commissioning checklist | High | What is the exact power-generation maintenance scope, testing capability, territory and technician credential (AD-006)? |
| 6 | Fuel strategy and logistics | 12-hour Tier baseline, 48–96 h specs, fuel polishing, contracted priority delivery, HVO | Absent | Medium-high | Does Evolve provide fuel-system design, tank monitoring, polishing or fueling contracts (the current site lists "fuel contingency planning")? |
| 7 | Published equipment ranges, OEM relationships and fleet | Generac 2.25–3.25 MW; WPP 20 kW–40 MW; Aggreko 25 kW–1.5 MW | None | Medium-high | What kW–MW range, OEM relationships (dealer, integrator, multi-OEM) and rental/bridge fleet can Evolve state? |
| 8 | Commercial models and financing | RaaS, PPA, lease, EaaS; WPP publishes a financing page | Absent | Medium | Does Evolve offer or partner on leasing, RaaS or financing? |
| 9 | Credentials and safety metrics | EMR/TRIR thresholds in hyperscale prequalification; EGSA, NFPA, ISO credentials | "Zero injuries since 2010" appears on Home, About, Design & Build and Greenfield, but not on either Power page; no EMR, no certifications | Medium | What are Evolve's current EMR and TRIR, prequalification memberships and technician certifications? |
| 10 | Response commitments | Competitors state "24/7" freely; buyers ask for response terms | Header promises "24/7 emergency service" on every page while Maintain pages say no response terms are published (CLM-030/031) | Medium (consistency risk) | Is the header line approved under CLM-030/031, or should it change to a plain phone label? |
| 11 | Evolution Series definition | Generac markets "scalable, redundant" paralleled MPS; the category is contested | Placeholder card; current-site claims (patent, "world's first," "zero downtime," "eliminate load banks, rental power and day tanks") on hold | Medium | What is the approved, engineering-substantiated definition and differentiator (AD-002)? |
| 12 | Evolve Energy and powered sites | Developers pay for "powered land"; Cleanview counts 59 BTM sites | Absent; page not retrievable | Medium | What does Evolve Energy offer, where, and how should the site reference it? |
| 13 | Commissioning power and pre-energization testing | VoltaGrid L2–L5 commissioning power; Sunbelt >100 MW; WPP case study | Commissioning page silent on temporary power and load banks | Medium | Does Evolve supply or coordinate temporary power and load banks for commissioning? |
| 14 | Grid programs and demand response | EPA 50-hour rule; ERCOT controllable-load pathways; SB 6 deployment | Absent | Low-medium | Has Evolve designed backup fleets for demand-response or SB 6 deployment duty? |
| 15 | Non-data-center critical facilities | Current site lists hospitals, schools, fire pumps, utilities; Texas Backup Power Package funds ≤2.5 MW sites | Review site is data-center-only by architecture | Decision | Should power-only work for non-data-center critical facilities have any public path? |

---

## 5. Recommended actions

**Site changes we can make now with approved facts**

1. Publish a technology-neutral Insight, "Power options for a data center in 2026" (standby diesel, gas engines, turbines, fuel cells, BESS, bridge), using only the cited market facts and an explicit "Evolve's scope is defined per engagement" boundary. Answers blind spots 2 and 1 without claiming an offer.
2. Publish "Speed to power in ERCOT: what SB 6 and the PUCT rule mean for a ≥75 MW load" as market education citing the sources above; no Evolve service claim. Blind spot 3.
3. Add a "What to define before a backup-power RFP" checklist and FAQ to `/backup-power-systems/` (topology, fuel autonomy, rating class, emissions classification, testing, maintenance, delivery model), all market-answerable. Blind spots 5, 6, 8.
4. Add a permitting primer FAQ (EPA emergency-engine limits, TCEQ PBR vs standard permit, state Tier 4 trend) with a scope disclaimer. Blind spot 4.
5. Add the approved safety line ("zero injuries recorded since 2010") and "Houston, Texas headquarters, nationwide work" to both Power pages; add a load-bank/IST explainer link from the commissioning checklist. Blind spots 9, 13.
6. Extend the Power FAQ with the nine direct questions in Section 2, answered from market sources.

**Needs a fact or approval from Evolve**

7. Resolve RQ-003 with a capability matrix: standby, prime, bridge, BTM, microgrid, BESS, turbine, fuel cell; delivery model per row (EPC, supply, O&M, partner). Unlocks PAGE-240 and PAGE-230.
8. Approve a published equipment range, OEM relationships and any rental/bridge fleet figure; approve paralleling-switchgear and controls scope. Blind spot 7.
9. Approve the power-generation maintenance scope (AD-006): load-bank testing, NFPA 110 programs, fuel polishing, technician credentials, territory. Unlocks PAGE-320.
10. Confirm EMR, TRIR and prequalification memberships for a governed credentials block; confirm whether the "24/7 emergency service" header is approved under CLM-030/031.
11. Deliver the Evolution Series claim pack (AD-002) and an Evolve Energy definition; until then keep both as held placeholders.
12. Decide whether non-data-center critical-facility power work gets a public path (blind spot 15).

**New offer or lead-magnet ideas** (distinct from the five planning, modular, commissioning, AI and maintenance guides now in `/resources/`)

13. "Backup Power Requirements Worksheet": a one-page intake (load by phase, runtime target, site, utility position, permit status) offered as the primary Power CTA in place of a generic contact form.
14. "ERCOT SB 6 Readiness Checklist for ≥75 MW loads": gated download tied to the Insight in action 2.
15. "Generator procurement timeline planner": a simple lead-time calendar (order, switchgear, transformer, permit, commissioning) built from the cited 2026 lead-time ranges, refreshed quarterly.
16. "Fuel autonomy estimator": hours of runtime from load, tank volume and consumption charts, following the pattern WPP uses.
17. Quarterly "Power permitting and interconnection briefing" webinar with a named Evolve reviewer, once the reviewer and scope are approved.

---

## Sources

Market, regulatory and technology
- LBNL, *Queued Up: 2026 Edition*, June 2026. https://emp.lbl.gov/publications/queued-2026-edition-characteristics
- White & Case, "DOE directs FERC to accelerate interconnection of data centers," Oct. 2025. https://www.whitecase.com/insight-alert/doe-directs-ferc-accelerate-interconnection-data-centers
- FERC, "FERC Launches Aggressive Targeted Action to Speed Large Load Integration," June 18, 2026. https://www.ferc.gov/news-events/news/ferc-launches-aggressive-targeted-action-speed-large-load-integration
- White & Case, "FERC orders grid operators to promptly revise or justify interconnection rules," June 2026. https://www.whitecase.com/insight-alert/ferc-orders-grid-operators-promptly-revise-or-justify-interconnection-rules-data
- Latitude Media, "ERCOT's large load queue has nearly quadrupled in a single year," Dec. 3, 2025. https://www.latitudemedia.com/news/ercots-large-load-queue-has-nearly-quadrupled-in-a-single-year/
- Utility Dive, "ERCOT's large load queue jumped almost 300% last year," Jan. 6, 2026. https://www.utilitydive.com/news/ercots-large-load-queue-jumped-almost-300-last-year-official/808820/
- RTO Insider, "ERCOT Large Load Interconnection Queue Hits 410 GW," Sept. 4, 2026. https://www.rtoinsider.com/129421-ercot-large-load-requests-soar-again/
- Utility Dive, "CenterPoint to energize 8 GW of data center load by 2029," Apr. 23, 2026. https://www.utilitydive.com/news/centerpoint-energy-data-center-load-earnings/818293/
- Bloom Energy, "Data Centers Plan to Reduce Reliance on Grid," Jan. 20, 2026. https://investor.bloomenergy.com/press-releases/press-release-details/2026/Data-Centers-Plan-to-Reduce-Reliance-on-Grid-Finds-Bloom-Energys-2026-Power-Report/default.aspx
- Utility Dive, "Texas law gives grid operator power to disconnect data centers during crisis," June 2025. https://www.utilitydive.com/news/texas-law-gives-grid-operator-power-to-disconnect-data-centers-during-crisi/751587/
- McGuireWoods, "Texas Senate Bill 6 Significantly Expands Regulatory Oversight Over Large Loads in ERCOT," July 2025. https://www.mcguirewoods.com/client-resources/alerts/2025/7/texas-senate-bill-6-significantly-expands-regulatory-oversight-over-large-loads-in-ercot/
- Greenberg Traurig, "Texas Senate Bill 6 Update: Proposed Interconnection Standards," Mar. 2026. https://www.gtlaw.com/en/insights/2026/3/texas-senate-bill-6-update-what-data-centers-large-load-customers-should-know-about-proposed-interconnection-standards
- GPU Lease Index, "ERCOT Data Center Interconnection: Batch Zero, CLR, BYOG & Queue Guide," 2026 (secondary). https://gpuleaseindex.com/readiness/ercot-interconnection-guide
- PA Consulting, "Bring Your Own Generation (BYOG)," accessed Sept. 8, 2026. https://www.paconsulting.com/insights/bring-your-own-generation-byog-accelerating-the-path-to-power-supply-solutions
- PUCT, "PUCT Adopts Rule for Texas Backup Power Package Program," May 7, 2026. https://ftp.puc.texas.gov/public/puct-info/agency/resources/pubs/news/2026/PUCT-Adopts-Rule-for-Texas-Backup-Power-Package-Program.pdf
- University of Houston, "Texas Finalizes $1.8 Billion for Microgrid Program," 2025. https://www.uh.edu/uh-energy-innovation/news-events/energy/stories/2025/microgirdresilience.php
- Cleanview, "Bypassing the Grid: How Data Center Developers Are Building Their Own Power Plants," mid-2026 update. https://cleanview.co/reports/behind-the-meter-data-centers
- American Public Power Association, "Study Details How Data Centers are Building Their Own Power Plants," Feb. 21, 2026. https://www.publicpower.org/periodical/article/study-details-how-data-centers-are-building-their-own-power-plants
- INNIO, "INNIO Secures Largest Order in Company History with VoltaGrid," Oct. 21, 2025. https://www.innio.com/en/news-media/press-releases/innio-secures-largest-order-in-company-history-with-voltagrid-delivering-power-generation-for-one-of-the-worlds-largest-data-centers/
- Caterpillar, "American Intelligence & Power Forms Strategic Alliance with Caterpillar and Boyd CAT," Jan. 28, 2026. https://investors.caterpillar.com/news/news-details/2026/American-Intelligence--Power-Forms-Strategic-Alliance-with-Caterpillar-and-Boyd-CAT-to-Deploy-2-Gigawatts-of-Dedicated-Power-for-Hyperscale-AI-Infrastructure/default.aspx
- Power Engineering, "Data center power crunch lifts engines, aeroderivatives into larger role," Apr. 16, 2026. https://www.power-eng.com/gas/data-center-power-crunch-lifts-engines-aeroderivatives-into-larger-role/
- POWER, "Data Centers Are Turning to Gas Generators for Prime Power," Oct. 28, 2025. https://www.powermag.com/data-centers-are-turning-to-gas-generators-for-prime-power-to-eliminate-long-lead-times-for-grid-connections/
- Power Engineering, "Data centers drive record surge in GE Vernova power equipment orders," Apr. 23, 2026. https://www.power-eng.com/gas/turbines/data-centers-drive-record-surge-in-ge-vernova-power-equipment-orders-as-turbine-slots-tighten-through-2030/
- Turbomachinery Magazine, "GE Vernova's Gas Turbine Backlog Hits 116 GW," 2026 (not opened). https://www.turbomachinerymag.com/view/ge-vernova-gas-turbine-backlog-hits-116-gw-as-power-orders-more-than-double
- PROENERGY, "PROENERGY To Deliver Major Generating Equipment To Power Crusoe AI Factories," Apr. 2026. https://www.proenergyservices.com/2026/04/proenergy-to-deliver-major-generating-equipment-to-power-crusoe-ai-factories/
- Utility Dive, "Bloom Energy says it's on track for 2 GW annual production capacity," accessed Sept. 8, 2026. https://www.utilitydive.com/news/bloom-energy-says-its-on-track-for-2-gw-annual-production-capacity/804291/
- Data Center Knowledge, "BESS Steps Up as a Diesel Alternative for Data Centers," May 15, 2026. https://www.datacenterknowledge.com/energy-power-supply/battery-storage-gains-ground-as-data-centers-seek-diesel-alternatives
- ESS News, "Battery storage reshapes power infrastructure for AI data centers," July 15, 2026. https://www.ess-news.com/2026/07/15/data-center-power-shifts-favor-bess-solid-state-transformers/
- Generac, "Generac and EPC Power to Deploy Fully Integrated Energy Solutions for Data Center Applications," Mar. 2026. https://www.generac.com/about/news/generac-and-epc-power-to-deploy-fully-integrated-energy-solutions-for-data-center-applications/
- Industrial Equipment News, "Generac Acquires New Factory to Meet Surging Data Center Demand," Jan. 2026. https://www.ien.com/operations/news/22957891/generac-acquires-new-factory-to-meet-surging-data-center-demand
- Global Power Supply, "Generator Lead Times in 2026," May 11, 2026. https://www.globalpwr.com/blog/generator-lead-times-in-2026/
- Caterpillar, "Caterpillar Reports Second-Quarter 2026 Results," Aug. 4, 2026. https://www.caterpillar.com/en/news/corporate-press-releases/h/2q26-results-caterpillar-inc.html
- Manufacturing Dive, "Caterpillar sales surpass $20B as data center generators take off," Aug. 2026. https://www.manufacturingdive.com/news/caterpillar-sales-surpass-20b-growing-data-center-demand-q2-2026/827068/
- CNBC, "Caterpillar lifts 2026 sales growth target on strong data center demand," Aug. 4, 2026. https://www.cnbc.com/2026/08/04/caterpillar-cat-q2-2026-earnings.html
- Savrn, "AI Data Center Supply Chain: 2026 Lead-Time Survival Guide," 2026 (secondary; Cummins Fridley claim unverified). https://savrn.com/blog/ai-data-center-supply-chain
- Uptime Institute, "Uptime Announces Annual Outage Analysis Report 2026," May 13, 2026. https://uptimeinstitute.com/about-ui/press-releases/uptime-announces-annual-outage-analysis-report-2026
- Network World, "Network outages, power failures strain data center resiliency," May 14, 2026. https://www.networkworld.com/article/4171277/network-outages-power-failures-strain-data-center-resiliency.html
- Direct LTx, "Survey: Failing Power Infrastructure Causing Outages," 2026 (reporting Uptime's 2026 Resiliency Survey). https://www.directltx.com/direct-ltx-news/survey-failing-power-infrastructure-causing-outages
- Uptime Institute Journal, "Data center fuel system design and reliability," accessed Sept. 8, 2026. https://journal.uptimeinstitute.com/fuel-system-design-reliability/
- Uptime Compliance, "NFPA 110 Compliance Checklist: Generator Testing Requirements (2026)." https://uptimecompliance.com/pages/nfpa-110
- Generator Source, "Professional Load Bank Testing for NFPA 110 Compliance," accessed Sept. 8, 2026. https://generatorsource.com/industries-served/data-centers/professional-load-bank-testing-for-nfpa-110-compliance/
- Consulting-Specifying Engineer, "Know the electrical, power components in a data center," accessed Sept. 8, 2026. https://www.csemag.com/know-the-electrical-power-components-in-a-data-center/
- Build.inc, "Data Center Backup Power Requirements: What Developers Need to Verify," accessed Sept. 8, 2026. https://build.inc/insights/data-center-backup-power-requirements
- Mansfield Energy, "Why Fuel Planning Matters More This Hurricane Season," June 9, 2026. https://mansfield.energy/2026/06/09/why-fuel-planning-matters-more-this-hurricane-season/
- Power Generation Enterprises, "Tier 4 Generator Requirements: Compliance Guide 2026." https://powergenenterprises.com/tier-4-generator-requirements-compliance-guide-2026/
- Sidley Austin, "EPA Clarifies Rules for Backup Generator Use," May 2025. https://www.sidley.com/en/insights/newsupdates/2025/05/us-epa-issues-new-guidance-on-data-center-emergency-generator-operations
- Kirkland & Ellis, "New EPA Guidance Clarifies When Data Centers … May Utilize Emergency Backup Generators," May 2025. https://www.kirkland.com/publications/kirkland-alert/2025/05/new-epa-guidance-clarifies-when-data-centers-and-other-operators-may-utilize-emergency-backup
- Environmental Protection Network, "EPA Proposal Threatens Public Notice for Some Data Center Air Permits," Aug. 20, 2026. https://www.environmentalprotectionnetwork.org/20260820_nrs-comment_release/
- Axios Atlanta, "EPA plan could reduce public scrutiny of Georgia data center air permits," Aug. 12, 2026. https://www.axios.com/local/atlanta/2026/08/12/georgia-data-centers-diesel-generators-public-comment-pollution
- TCEQ, "Air Permits by Rule" index and RG-616 permit fact sheet (revised Jan. 2026). https://www.tceq.texas.gov/permitting/air/permitbyrule/air-pbr ; https://www.tceq.texas.gov/assets/public/permitting/air/factsheets/permit-factsheet.pdf
- TCEQ, "Air Quality Standard Permit for Natural Gas Electric Generating Units." https://www.tceq.texas.gov/downloads/permitting/air/nsr/combustion/ngegu-standard-permit.pdf/@@download/file/ngegu-standard-permit.pdf
- Texas Tribune, "Planned Texas data centers could emit significant pollution," July 9, 2026. https://www.texastribune.org/2026/07/09/texas-data-centers-ai-power-plants-pollution-state-permits/
- Encino Environmental Services, "States Are Tightening the Rules for Data Center Backup Generators," Feb. 21, 2026. https://encinoenviron.com/states-are-tightening-the-rules-for-data-center-backup-generators/
- ERM, "Future-proofing Data Centers: Insights from 20 years of air permitting leadership," accessed Sept. 8, 2026. https://www.erm.com/insights/future-proofing-data-centers-insights-from-20-years-of-air-permitting-leadership/
- BIS Research, "Why Are Data Centers Switching to HVO for Backup Power?" accessed Sept. 8, 2026. https://bisresearch.com/insights/why-are-data-centers-switching-to-hvo-for-backup-power
- Cummins, "Centum Series Generators" (EN 15940/HVO approval). https://www.cummins.com/en-na/generators/standby-power/centum-series
- domain-b, "Bridge Data Centres pilots HVO biofuel for low-emission backup power," 2026. https://www.domain-b.com/environment-1/bridge-data-centres-hvo-biofuel-backup-power-2026
- Pillsbury, "Power Purchase and Interconnection Agreements for Data Centers," accessed Sept. 8, 2026. https://www.pillsburylaw.com/en/news-and-insights/power-purchase-interconnection-agreements-data-centers.html
- Enchanted Rock, Inc., Form DRS (draft registration statement), Feb. 17, 2026. https://www.sec.gov/Archives/edgar/data/0002110029/000119312526054926/filename1.htm
- EGSA, "Generator Technician Certification." https://egsa.org/Education/EGSA-Certifications/Generator-Technician-Certifications
- EHS Inc., "ISNetworld vs. Avetta vs. Veriforce," accessed Sept. 8, 2026. https://ehs.inc/ehs/isnetworld-vs-avetta-vs-veriforce
- CrewCompliance, "Avetta Contractor Prequalification Guide," accessed Sept. 8, 2026. https://crewcompliance.org/avetta-prequalification-guide

Competitor pages (all self-published; retrieved Sept. 8, 2026 unless noted)
- Caterpillar, Data Centers hub (timed out on re-fetch; observation carried from MKT-001). https://www.cat.com/en_US/by-industry/electric-power/electric-power-industries/data-centers.html
- Cummins, "Reliable Generators for Data Centers" (fetch blocked; search summary). https://www.cummins.com/en-na/generators/data-centers
- Generac Industrial, "Data Center Backup Power Generators." https://www.generac.com/industrial/industry-expertise/data-centers/
- Mustang Cat, "Electric Power Generation." https://www.mustangcat.com/by-industry/electric-power-generation/
- Worldwide Power Products, "Backup Power Solutions for Data Centers." https://www.wpowerproducts.com/industries-served/data-centers/
- Aggreko, "Bridging Power Solutions for Data Centers." https://www.aggreko.com/en-us/sectors/data-centres/bridging-power-solutions
- Aggreko, "Aggreko Bridges the Grid Power Gap … with Modular Microgrids," June 3, 2026. https://www.globenewswire.com/news-release/2026/06/03/3306069/0/en/aggreko-bridges-the-grid-power-gap-for-data-centers-and-industrial-power-with-modular-microgrids.html
- VoltaGrid, "Data Centers." https://voltagrid.com/data-centers
- ERock (Enchanted Rock), "Data Centers" and "Onsite Power." https://erock.com/data-centers/ ; https://erock.com/onsite-power/
- Mainspring Energy, homepage. https://www.mainspringenergy.com/
- PROENERGY, "PE6000." https://www.proenergyservices.com/solutions/manufactured-equipment/pe6000/
- Burns & McDonnell, "Data Centers & Switch Centers." https://www.burnsmcd.com/services/buildings/mission-critical-buildings/data-centers-switch-centers
- Sunbelt Rentals, "Data Center Construction, Building & Maintenance Equipment Rentals" (fetch blocked; search summary). https://www.sunbeltrentals.com/industries/data-centers/
- United Rentals, "Faster Load Bank Testing for Data Center Commissioning." https://www.unitedrentals.com/project-uptime/equipment/faster-load-bank-testing-data-center-commissioning

Evolve materials
- Review build: https://evolve2026-review.netlify.app/power-generation/ and /power-generation/backup-power-systems/ (noindex); keyword scan of `dist/` in the Evolve2026 repository, Sept. 8, 2026.
- Current site: https://evolveincorporated.com/power-generation (local copy captured Sept. 8, 2026); https://evolveincorporated.com/evolve-energy (not retrievable Sept. 8, 2026).
- MKT-001 v1.1 research handoff, Sept. 7, 2026; COPY-001B v1.0 Power and Maintain copy package; Evolve_Copy_Approval_Ledger_2026-09-07.csv; docs/REVIEW-NOTES.md.
