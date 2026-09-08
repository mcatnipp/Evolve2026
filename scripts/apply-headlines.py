#!/usr/bin/env python3
"""Apply the direct-response headline layer (H1, hero intro, CTAs, final CTA) to every
governed page block in content/*.md, and write the variant set used by the headline test.

Voice: Dan Kennedy direct response, fact-bound. Every figure comes from the approved claims
(CLM-001 to CLM-014, CLM-039): 2,200+ mission-critical projects, 5.3+ GW deployed, 20+ years,
zero injuries recorded since 2010, founded 2004, Houston, nationwide, self-performed modular
fabrication, Plan / Design / Build / Power / Maintain. No superlatives, no guarantees,
no response-time promises, no invented facts.

Usage:  python3 scripts/apply-headlines.py            # apply "control" headlines
        python3 scripts/apply-headlines.py --winners   # apply winners from docs/headline-test-winners.json
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

# url -> headline layer. "alts" are the test variants (B and C); "h1" is the control (A).
HEADLINES = {
    "/": {
        "h1": "One accountable team for your data center, from the first plan to the last maintenance visit.",
        "alts": ["2,200+ mission-critical projects and 5.3+ GW deployed. One team from plan to maintain.",
                 "Stop handing your data center from firm to firm. Plan, design, build, power and maintain it with one team."],
        "intro": "Evolve builds data centers and nothing else. Founded in 2004, we have planned, designed, built, powered and maintained mission-critical facilities nationwide: 2,200+ projects, 5.3+ GW of power deployed and zero injuries recorded since 2010. Here is what that means for the program in front of you.",
        "primary": "Tell Us About Your Facility", "secondary": "See How Design & Build Works",
        "final_heading": "Put the whole program on one table before the schedule, the utility or the change orders decide it for you.",
        "final_description": "Send the facility type, target capacity, site status and timeline. You get a straight answer on fit, scope and the next decision.",
        "final_cta": "Tell Us About Your Facility", "final_secondary": "Contact Evolve",
    },
    "/design-build/": {
        "h1": "Design-build for data centers, run by people who also have to power and maintain what they build.",
        "alts": ["The data-center design-build partner that stays on the hook after turnover.",
                 "Why data-center owners hand Evolve the plan, the build and the power in one contract."],
        "intro": "Most delivery problems are interface problems: design handed to procurement, procurement handed to the field, the field handed to commissioning. Evolve keeps planning, design, preconstruction, construction, commissioning and turnover inside one data-center-only team, so the handoffs stop costing you weeks.",
        "primary": "Discuss a Data Center Project", "secondary": "Explore Data Center Types",
        "final_heading": "Define the scope now, or let the project define it for you at change-order prices.",
        "final_description": "Bring the facility type, capacity target and the constraint you are most worried about. We will tell you which decisions have to be made first and what they will cost you if they slip.",
        "final_cta": "Discuss a Data Center Project", "final_secondary": "Contact Evolve",
    },
    "/design-build/modular-data-centers/": {
        "h1": "Modular data centers built in our own Houston shop, then connected to your site, your power and your commissioning plan.",
        "alts": ["Factory-built capacity that arrives ready for the site because the same team designed the site.",
                 "Modular only works when the interfaces are designed with the modules. We design both."],
        "intro": "Evolve self-performs modular fabrication. That means the module, the pad, the power feed and the acceptance test are planned by one team instead of negotiated between three vendors. If you need capacity on a controlled schedule, start here.",
        "primary": "Discuss a Modular Project", "secondary": "Compare Delivery Approaches",
        "final_heading": "Tell us the capacity, the site and the date. We will tell you what modular delivery can and cannot do for it.",
        "final_description": "A straight answer on module boundaries, site work and schedule, before anyone orders steel.",
        "final_cta": "Discuss a Modular Project", "final_secondary": "Compare Delivery Approaches",
    },
    "/design-build/hyperscale-data-centers/": {
        "h1": "Hyperscale delivery that protects the first operating phase without boxing in the next three.",
        "alts": ["Phase one on schedule. Phases two through four still possible. That is the hyperscale job.",
                 "If your campus phase plan lives in three different vendors' spreadsheets, read this first."],
        "intro": "Large campuses fail on interfaces, not on ambition. Evolve carries Plan, Design, Build, Power and Maintain as one framework so phasing, utility strategy and operational readiness are decided together, by a team with 2,200+ mission-critical projects behind it.",
        "primary": "Discuss a Hyperscale Project", "secondary": "Review Planning & Power",
        "final_heading": "Put the phase plan, the power strategy and the delivery path on the same table, this month.",
        "final_description": "Share the campus target, the utility position and the first-phase date. We will show you where the plan is exposed.",
        "final_cta": "Discuss a Hyperscale Project", "final_secondary": "Contact Evolve",
    },
    "/design-build/ai-data-centers/": {
        "h1": "AI data centers: get the power, cooling and building decided as one system before the GPUs are ordered.",
        "alts": ["The GPU order is the easy part. The facility around it is where AI programs lose a year.",
                 "Building for AI density? Here is what has to be settled before design starts."],
        "intro": "AI infrastructure is a whole-facility decision. Evolve coordinates the planning, design, construction, power, commissioning and long-term support around your compute assumptions, so the facility is built to the workload instead of to a template.",
        "primary": "Discuss an AI Data Center", "secondary": "Review AI Infrastructure Planning",
        "final_heading": "Start with an approved technical basis, not an assumed template.",
        "final_description": "Send the compute assumptions, the site and the date you need capacity. We will lay out the decisions that control the schedule.",
        "final_cta": "Discuss an AI Data Center", "final_secondary": "Review AI Infrastructure Planning",
    },
    "/design-build/planning-feasibility/": {
        "h1": "Find out whether your data-center plan can actually be built, powered and paid for, before you commit to it.",
        "alts": ["The decisions that make or break a data-center plan are made in the first ninety days. Make them on purpose.",
                 "Feasibility is not a report. It is the list of decisions that decide whether your site ever energizes."],
        "intro": "Evolve organizes the early requirements, assumptions and constraints so design, construction, power and operating decisions start from one basis. You leave with a clear picture of what is known, what is assumed and what still has to be resolved.",
        "primary": "Request a Planning Discussion", "secondary": None,
        "final_heading": "Bring the knowns, the assumptions and the open questions. Leave with a decision list.",
        "final_description": "A planning discussion costs you an hour. An unexamined assumption costs you a quarter.",
        "final_cta": "Request a Planning Discussion", "final_secondary": None,
    },
    "/design-build/design-engineering/": {
        "h1": "Data-center design that the same company has to procure, build, commission and maintain.",
        "alts": ["Design decisions are cheap on paper and expensive in the field. Make them with the builder in the room.",
                 "Turn operating requirements into a design your contractor will not have to re-engineer."],
        "intro": "Evolve connects design and engineering decisions to procurement, construction, power, commissioning and long-term support. When the designer and the builder are the same team, the drawings reflect what can be bought, built and operated.",
        "primary": "Start a Project", "secondary": None,
        "final_heading": "Put the full facility requirement behind the design, not just the load letter.",
        "final_description": "Share the operating requirements, the site and the schedule. We will show you what the design has to resolve first.",
        "final_cta": "Start a Project", "final_secondary": None,
    },
    "/design-build/preconstruction-procurement/": {
        "h1": "Preconstruction that finds the long-lead equipment, the scope gaps and the field constraints while they are still cheap to fix.",
        "alts": ["Every surprise in the field was visible in preconstruction. Here is how we look for them.",
                 "Buy the right equipment early, sequence the site correctly and stop paying for the gap between them."],
        "intro": "Evolve ties preconstruction and procurement to the approved design, the delivery plan, the power requirement and the commissioning needs. Scope, lead times and site constraints get resolved before construction accelerates and the cost of change climbs.",
        "primary": "Submit a Project Brief", "secondary": None,
        "final_heading": "Give the project team one delivery basis before the first purchase order goes out.",
        "final_description": "Send the design status, the equipment list and the date you need to break ground.",
        "final_cta": "Submit a Project Brief", "final_secondary": None,
    },
    "/design-build/data-center-construction/": {
        "h1": "Data-center construction by a team with 2,200+ mission-critical projects and zero injuries recorded since 2010.",
        "alts": ["New builds, expansions, retrofits and live-environment work, built against a controlled technical basis.",
                 "The construction team that also has to make the facility pass commissioning."],
        "intro": "Evolve builds new data centers and works inside operating ones: expansions, upgrades, retrofits, power conversions and live-environment work. Every scope is built against a defined technical and operating basis, not a set of assumptions.",
        "primary": "Start a Project", "secondary": None,
        "final_heading": "Bring the construction scope into the full facility plan before the crews mobilize.",
        "final_description": "Tell us the scope, the site condition and the operating constraint. We will tell you how it gets built without surprising the systems around it.",
        "final_cta": "Start a Project", "final_secondary": None,
    },
    "/design-build/commissioning-turnover/": {
        "h1": "Commissioning that proves the facility is ready, not paperwork that says it is finished.",
        "alts": ["A signed test log is not readiness. Here is what commissioning has to prove before you accept the facility.",
                 "The questions to settle before final testing, from the team that will maintain the systems afterward."],
        "intro": "Evolve includes commissioning within its documented construction capability and connects turnover to the operating responsibilities that follow. Readiness is defined before the acceptance line, so nobody discovers the gaps at 2 a.m. on the first live weekend.",
        "primary": "Discuss Commissioning Scope", "secondary": None,
        "final_heading": "Define readiness before the facility reaches the acceptance line.",
        "final_description": "Share the system list, the schedule and who owns operations on day one. We will show you what still has to be proven.",
        "final_cta": "Discuss Commissioning Scope", "final_secondary": None,
    },
    "/design-build/expansions-retrofits/": {
        "h1": "Expand or retrofit a live data center without putting the systems that are already running at risk.",
        "alts": ["The facility is running. The change still has to happen. Here is how it gets done safely.",
                 "Live-environment expansions and retrofits, planned around the operating constraint first."],
        "intro": "Evolve supports expansions, retrofits, upgrades, power conversions and work in live environments across Plan, Design, Build, Power and Maintain. The existing condition and the operating constraint come first; the construction plan is built around them.",
        "primary": "Discuss an Existing Facility", "secondary": None,
        "final_heading": "Start with the existing condition and the operating constraint, then plan the change.",
        "final_description": "Tell us what is running, what has to change and what cannot be interrupted.",
        "final_cta": "Discuss an Existing Facility", "final_secondary": None,
    },
    "/power-generation/": {
        "h1": "5.3+ GW deployed. Bring power into the data-center plan on day one, not after the utility says no.",
        "alts": ["Power is the schedule. Plan it with the facility, not after it.",
                 "The generation and critical-power team that has deployed 5.3+ GW for mission-critical facilities."],
        "intro": "Evolve connects power-generation requirements to planning, design, construction, commissioning and maintenance. When generation is decided with the facility instead of bolted on later, the schedule, the site and the operating plan stop fighting each other.",
        "primary": "Discuss a Power Requirement", "secondary": "Explore Backup Power Systems",
        "final_heading": "Define the power requirement in the context of the facility, before the equipment gets chosen for you.",
        "final_description": "Send the load, the site, the utility position and the date. We will lay out the generation decisions that control the schedule.",
        "final_cta": "Discuss a Power Requirement", "final_secondary": "Contact Evolve",
    },
    "/power-generation/backup-power-systems/": {
        "h1": "Backup power designed as part of the facility, so it performs when the facility needs it.",
        "alts": ["A generator on a pad is not a backup power system. The integration is.",
                 "Backup power that is designed, built, commissioned and maintained by the same team."],
        "intro": "Evolve connects backup-power requirements to the data center's design, construction, commissioning and maintenance plan. The operating requirement comes before the equipment package, so the system is sized, tested and supported for the facility it protects.",
        "primary": "Discuss Backup Power", "secondary": None,
        "final_heading": "Define the operating requirement before the equipment package.",
        "final_description": "Tell us the critical load, the runtime expectation and the facility it protects.",
        "final_cta": "Discuss Backup Power", "final_secondary": None,
    },
    "/maintenance/": {
        "h1": "Data-center maintenance from the team that stays engaged after turnover, because the work does not end at acceptance.",
        "alts": ["The facility is live. Now the real work starts. Keep it that way with a team that knows the systems.",
                 "Monitoring, maintenance and long-term support built around the facility that is actually operating."],
        "intro": "Evolve remains engaged after turnover through monitoring, maintenance and long-term support. The program starts with an accurate understanding of the operating facility, its systems and its constraints, not a generic task list.",
        "primary": "Request Service", "secondary": "Explore Preventive Maintenance",
        "final_heading": "Define the facility, the operating constraint and the service need. We will build the program around them.",
        "final_description": "For emergencies, call 832-375-0099. For everything else, send the facility details and the systems in scope.",
        "final_cta": "Request Service", "final_secondary": "Contact Evolve",
    },
    "/maintenance/preventive-maintenance/": {
        "h1": "Preventive maintenance that produces decisions, not just a stamp that says the task was done.",
        "alts": ["A maintenance visit should tell you something. Ours is built to.",
                 "Build the maintenance plan around the equipment you actually run, not a template."],
        "intro": "Evolve connects planned maintenance to current asset information, operating requirements and documented responsibilities. Each visit is designed to establish what was serviced, what was observed and what decision it points to next.",
        "primary": "Request a Maintenance Discussion", "secondary": None,
        "final_heading": "Start with the systems, their current condition and the operating requirement.",
        "final_description": "Send the equipment list and the facility details. We will map the program to them.",
        "final_cta": "Request a Maintenance Discussion", "final_secondary": None,
    },
    "/data-center-markets/": {
        "h1": "Colocation, enterprise, hyperscale, AI or modular: the facility type changes the decisions. The discipline does not.",
        "alts": ["Every data-center market has its own failure points. Here is how Evolve plans for each.",
                 "One lifecycle, applied to the facility you actually operate."],
        "intro": "Evolve applies Plan, Design, Build, Power and Maintain to the distinct requirements of AI, hyperscale, modular, colocation and enterprise data centers. Start with your facility type to see how the decisions change.",
        "primary": "Discuss a Data Center Project", "secondary": None,
        "final_heading": "Define the facility type, the project stage and the constraint you are up against.",
        "final_description": "We route the conversation to the right planning, design, construction, power or operations team.",
        "final_cta": "Discuss a Data Center Project", "final_secondary": None,
    },
    "/data-center-markets/colocation/": {
        "h1": "Add colocation capacity without interrupting the customers already paying for the floor.",
        "alts": ["Colocation expansions planned around the tenants, not just the equipment.",
                 "New halls, power upgrades and retrofits inside a live colocation facility. Done with the operating floor in view."],
        "intro": "Evolve connects planning, design, construction, power, commissioning and long-term support for colocation operators. The capacity objective and the operating constraints are handled in one plan, so growth does not become a customer-facing incident.",
        "primary": "Discuss a Colocation Project", "secondary": None,
        "final_heading": "Bring the capacity objective and the operating constraints into one discussion.",
        "final_description": "Tell us the target capacity, the live systems and the date the sales team already promised.",
        "final_cta": "Discuss a Colocation Project", "final_secondary": None,
    },
    "/data-center-markets/enterprise/": {
        "h1": "Modernize the enterprise data center around the systems that are already keeping the business running.",
        "alts": ["Your enterprise facility is not a greenfield site. Plan the upgrade like it matters.",
                 "Enterprise data-center upgrades, retrofits and power conversions, planned around uptime first."],
        "intro": "Evolve supports enterprise data-center planning, design, construction, power, commissioning, monitoring and maintenance for new and existing facilities. The existing condition and the required future state are defined together before anything is touched.",
        "primary": "Discuss an Enterprise Facility", "secondary": None,
        "final_heading": "Define the existing condition and the required future state, then plan the path between them.",
        "final_description": "Send the facility details, the systems in service and what has to change.",
        "final_cta": "Discuss an Enterprise Facility", "final_secondary": None,
    },
    "/insights/": {
        "h1": "Straight answers to the data-center questions that cost the most when they are answered late.",
        "alts": ["Practical guidance for data-center decisions, written by people who have to build what they recommend.",
                 "Read this before the site visit, the RFP or the design kickoff."],
        "intro": "Evolve Insights examine the planning, design, construction, power, commissioning and maintenance questions that shape a facility across its lifecycle. Each guide is also available as a downloadable checklist or brief.",
        "primary": "Discuss a Project", "secondary": "Explore Design & Build",
        "final_heading": "Need to apply the guidance to a real facility?",
        "final_description": "Bring the site, the requirement and the open questions. We will work through them with you.",
        "final_cta": "Discuss a Project", "final_secondary": "Explore Design & Build",
    },
    "/about/": {
        "h1": "Data centers are the work. They have been for more than 20 years.",
        "alts": ["Founded in Houston in 2004. 2,200+ mission-critical projects. 5.3+ GW deployed. Still specialized in one thing.",
                 "Why a company that only builds data centers is worth a conversation before your next one."],
        "intro": "Founded in 2004 and headquartered in Houston, Texas, Evolve Data Center Solutions specializes in data centers and serves a nationwide market. No general construction, no side businesses: planning, design, construction, power, monitoring and maintenance for mission-critical facilities.",
        "primary": "Start a Project", "secondary": "Contact Evolve",
        "final_heading": "Put the facility, the power and the operating requirements into one lifecycle discussion.",
        "final_description": "Tell us what you are planning, building, changing or supporting.",
        "final_cta": "Start a Project", "final_secondary": "Contact Evolve",
    },
    "/about/leadership/": {
        "h1": "The people accountable for the work.",
        "alts": ["Meet the team that stays on the hook from the first plan to the last maintenance visit.",
                 "Thirteen leaders. One accountable team. Here is who carries your program."],
        "intro": "Evolve's leadership team carries data-center programs through planning, design, construction, power and long-term maintenance, and stays accountable across every stage.",
        "primary": "Contact Evolve", "secondary": "Start a Project",
        "final_heading": "Talk with the team that will carry your program.",
        "final_description": "Tell Evolve about the facility, the stage you are in and the decision in front of you.",
        "final_cta": "Contact Evolve", "final_secondary": "Start a Project",
    },
    "/contact/": {
        "h1": "Reach the right Evolve team the first time.",
        "alts": ["Contact Evolve Data Center Solutions", "Tell us what you need. We route it to the people who can act on it."],
        "intro": "Choose the reason for your inquiry so it reaches the right Evolve team. New projects, service requests, existing-customer support, careers and vendor inquiries each follow a defined path. For emergencies, call 832-375-0099.",
        "primary": "Route My Inquiry", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/support/": {
        "h1": "Existing-customer support, routed to the people who know your facility.",
        "alts": ["Existing-customer support", "Already an Evolve customer? Start here."],
        "intro": "Use this page to route a support request connected to an existing Evolve engagement. For emergencies, call 832-375-0099. New projects and general maintenance inquiries follow separate paths.",
        "primary": "Request Support", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/start-a-project/": {
        "h1": "Tell us about the facility. Get a straight answer on fit, scope and the next decision.",
        "alts": ["Start a data-center project discussion", "Five minutes here saves the first three meetings."],
        "intro": "Tell Evolve what is being planned, built, changed or supported. The brief routes to the right Plan, Design, Build, Power or Maintain team, and the qualifying questions below let us come back with something useful instead of a sales deck.",
        "primary": "Submit Project Brief", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/request-service/": {
        "h1": "Request service for a data center that is already running.",
        "alts": ["Request a data-center service discussion", "Something needs service. Tell us the facility and the system, and we route it today."],
        "intro": "Provide the facility context, the service need and the operating constraints so Evolve can route the request to the right team. If the facility is in an emergency condition right now, call 832-375-0099 instead of waiting on a form.",
        "primary": "Submit Service Request", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/thank-you/": {
        "h1": "Received. Here is what happens next.",
        "alts": ["Thank you. Your information has been received.", "Got it. Your brief is on its way to the right team."],
        "intro": "Evolve routes the submission using the inquiry type and details you provided, and the right team follows up on the next step.",
        "primary": "Start a Project", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/sitemap/": {
        "h1": "Website sitemap",
        "alts": ["Every Evolve page in one place.", "Find the service, market or guide you need."],
        "intro": "Use this page to reach Evolve's services, data-center markets, resources and company information.",
        "primary": "Start a Project", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/solutions/": {
        "h1": "Start from the facility you have to deliver. We will show you the decisions that come with it.",
        "alts": ["AI, edge, modular, colocation, greenfield or retrofit: pick the program, see the path.",
                 "Six ways a data-center program begins. One lifecycle that carries all of them."],
        "intro": "Every Evolve solution applies the same Plan, Design, Build, Power and Maintain lifecycle to a specific kind of program, from a new AI campus to a retrofit inside a live facility. Pick the one that matches yours.",
        "primary": "Discuss a Data Center Project", "secondary": "Explore Design & Build",
        "final_heading": "Tell Evolve which kind of facility you are delivering.",
        "final_description": "Share the facility type, the project stage and the constraint that matters most right now.",
        "final_cta": "Discuss a Data Center Project", "final_secondary": None,
    },
    "/solutions/ai-hpc-data-centers/": {
        "h1": "AI and HPC facilities built for the workload, not for a template.",
        "alts": ["Build the facility to the GPUs you are actually deploying, and the ones you will deploy next.",
                 "High-density halls take a whole-facility plan. Here is how Evolve runs it."],
        "intro": "Evolve coordinates the planning, design, construction, power, commissioning and long-term support that AI and high-performance-computing facilities demand, starting from your compute assumptions and carrying them through every decision.",
        "primary": "Discuss an AI Data Center", "secondary": "Review AI Infrastructure Planning",
        "final_heading": "Put the workload, the power and the building on one table.",
        "final_description": "Send the compute plan, the site and the date. We will show you the decisions that control it.",
        "final_cta": "Discuss an AI Data Center", "final_secondary": "Review AI Infrastructure Planning",
    },
    "/solutions/edge-data-centers/": {
        "h1": "Edge capacity you can repeat: designed once, fabricated in our shop, delivered where the demand is.",
        "alts": ["Repeatable capacity, delivered where the demand is.",
                 "Stop designing every edge site from scratch. Standardize it, fabricate it, set it."],
        "intro": "Evolve applies its planning, fabrication, construction, power and support capability to smaller, distributed deployments. Define the standard once, then deliver it site after site with the same team behind it.",
        "primary": "Discuss Distributed Infrastructure", "secondary": "Explore Modular Data Centers",
        "final_heading": "Define the standard once, then deliver it where it is needed.",
        "final_description": "Tell us the site count, the capacity per site and the rollout window.",
        "final_cta": "Discuss Distributed Infrastructure", "final_secondary": "Explore Modular Data Centers",
    },
    "/solutions/modular-data-centers/": {
        "h1": "Fabricate the data center where the work is controlled. Set it where the demand is.",
        "alts": ["Modules built in our own Houston shop, connected to your site, power and commissioning plan.",
                 "Move the risky work off the site and into a shop we own."],
        "intro": "Evolve builds data-center modules in its own shop and connects them to the site, the power and the commissioning plan. One team owns the module boundaries and the site reality, so nothing gets lost between them.",
        "primary": "Discuss a Modular Project", "secondary": "Compare Delivery Approaches",
        "final_heading": "Start with the module boundaries and the site reality.",
        "final_description": "Send the capacity, the site and the date. We will tell you what modular delivery can do for it.",
        "final_cta": "Discuss a Modular Project", "final_secondary": "Compare Delivery Approaches",
    },
    "/solutions/colocation-data-centers/": {
        "h1": "Add colocation capacity without interrupting the customers already on the floor.",
        "alts": ["New capacity for the operating colocation facility, planned around the tenants first.",
                 "Grow the facility. Keep the SLAs you already signed."],
        "intro": "Evolve delivers new colocation capacity, expansions and power changes with the operating facility in view, so growth stays a business decision instead of becoming a customer incident.",
        "primary": "Discuss a Colocation Project", "secondary": "Explore Expansions & Retrofits",
        "final_heading": "Bring the capacity objective and the operating constraints into one plan.",
        "final_description": "Tell us the target capacity, the live systems and the commitments already made.",
        "final_cta": "Discuss a Colocation Project", "final_secondary": "Explore Expansions & Retrofits",
    },
    "/solutions/greenfield-new-builds/": {
        "h1": "From open ground to an operating data center, as one program with one accountable team.",
        "alts": ["A new site is a hundred decisions in the right order. We keep them in order.",
                 "Greenfield data centers: feasibility, design, construction, power, commissioning and turnover under one roof."],
        "intro": "Evolve takes a new data-center site through planning, design, construction, power, commissioning and turnover with a single accountable team, so the decisions that control the schedule get made once and stay made.",
        "primary": "Start a Project", "secondary": "Explore Planning & Feasibility",
        "final_heading": "Bring the site, the requirement and the open questions.",
        "final_description": "We will tell you which decisions have to be made first and what they control.",
        "final_cta": "Start a Project", "final_secondary": "Explore Planning & Feasibility",
    },
    "/solutions/brownfield-retrofit/": {
        "h1": "Change the facility without losing the one that is running.",
        "alts": ["Retrofits, upgrades and power conversions inside live facilities, planned around the operating constraint.",
                 "The building already exists. The load already matters. Here is how the change gets made safely."],
        "intro": "Evolve plans and executes retrofits, upgrades, expansions and power conversions inside operating data centers and existing buildings. The operating constraint is the first design input, not an afterthought.",
        "primary": "Discuss an Existing Facility", "secondary": "Explore Expansions & Retrofits",
        "final_heading": "Start with the existing condition and the operating constraint.",
        "final_description": "Tell us what is running, what has to change and what cannot be interrupted.",
        "final_cta": "Discuss an Existing Facility", "final_secondary": "Explore Expansions & Retrofits",
    },
    # Insights: keep the SEO keyword in the H1, add the hook.
    "/insights/data-center-site-selection-power-planning/": {
        "h1": "Data Center Site Selection and Power Planning: Settle the Decision Basis Before You Sign Anything",
        "alts": ["Data Center Site Selection and Power Planning: Build the Decision Basis First",
                 "Data Center Site Selection and Power Planning: The Questions That Decide Whether the Site Ever Energizes"],
        "intro": None, "primary": "Request a Planning Discussion", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/insights/modular-vs-traditional-data-center-delivery/": {
        "h1": "Modular vs. Traditional Data Center Delivery: Compare the Interfaces, Not the Labels",
        "alts": ["Modular vs. Traditional Data Center Delivery: Which Work Belongs in a Shop and Which Belongs on Site",
                 "Modular vs. Traditional Data Center Delivery: The Comparison Buyers Should Actually Run"],
        "intro": None, "primary": "Discuss a Modular Project", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/insights/ai-data-center-infrastructure-planning/": {
        "h1": "AI Data Center Infrastructure Planning: Start With a Whole-System Basis",
        "alts": ["AI Data Center Infrastructure Planning: What to Settle Before the GPU Order",
                 "AI Data Center Infrastructure Planning: The Decisions That Control the Schedule"],
        "intro": None, "primary": "Discuss an AI Data Center", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/insights/hyperscale-campus-phasing/": {
        "h1": "Hyperscale Campus Phasing: Protect the First Delivery Without Closing Off the Next",
        "alts": ["Hyperscale Campus Phasing: How to Deliver Phase One Without Sabotaging Phase Four",
                 "Hyperscale Campus Phasing: The Plan Has Two Jobs. Most Do One."],
        "intro": None, "primary": "Discuss a Hyperscale Project", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/insights/data-center-commissioning-checklist/": {
        "h1": "Data Center Commissioning Checklist: The Questions to Settle Before Final Testing",
        "alts": ["Data Center Commissioning Checklist: What Has to Be Proven Before You Accept the Facility",
                 "Data Center Commissioning Checklist: Readiness, Not Paperwork"],
        "intro": None, "primary": "Discuss Commissioning Scope", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/insights/data-center-preventive-maintenance/": {
        "h1": "Data Center Preventive Maintenance: Build a Program That Produces Useful Decisions",
        "alts": ["Data Center Preventive Maintenance: Why a Completed Task List Is Not a Program",
                 "Data Center Preventive Maintenance: What Every Visit Should Tell You"],
        "intro": None, "primary": "Request a Maintenance Discussion", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/insights/data-center-monitoring-vs-dcim/": {
        "h1": "Data Center Monitoring vs. DCIM: Start With the Operating Decision",
        "alts": ["Data Center Monitoring vs. DCIM: Define the Decision Before You Buy the Dashboard",
                 "Data Center Monitoring vs. DCIM: Two Terms, One Question You Have to Answer First"],
        "intro": None, "primary": "Explore Service & Maintenance", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
    "/insights/responsible-data-center-development/": {
        "h1": "Responsible Data Center Development: Put the Local Questions Into the Project Plan",
        "alts": ["Responsible Data Center Development: Answer the Community Before the Hearing Does",
                 "Responsible Data Center Development: Power, Water, Noise and Land, Planned on Purpose"],
        "intro": None, "primary": "Request a Planning Discussion", "secondary": None,
        "final_heading": None, "final_description": None, "final_cta": None, "final_secondary": None,
    },
}


def split_blocks(text):
    """Yield (start, end) spans of each '# PAGE-' block."""
    matches = list(re.finditer(r"^# PAGE-(\d+) — ([^\n]+)$", text, re.M))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        yield m.start(), end


def apply_to_block(block, h):
    url_m = re.search(r"^\*\*URL:\*\*\s+`([^`]+)`", block, re.M)
    url = url_m.group(1) if url_m else None
    pub = re.search(r"^## Publishable (?:page copy|article)\s*$", block, re.M)
    meta = re.search(r"^## Metadata recommendation\s*$", block, re.M)
    if not (url and pub and meta):
        return block, False
    head, body, tail = block[:pub.end()], block[pub.end():meta.start()], block[meta.start():]
    changed = False
    # H1
    m = re.search(r"^# (.+)$", body, re.M)
    if m and h.get("h1") and m.group(1).strip() != h["h1"]:
        body = body[:m.start(1)] + h["h1"] + body[m.end(1):]
        changed = True
    # Hero intro: first paragraph after the H1 (only when the page has a Hero block and an intro is supplied)
    if h.get("intro") and re.search(r"^### Hero\s*$", body, re.M):
        m = re.search(r"^# .+\n\n([^\n]+(?:\n(?!\n)[^\n]+)*)", body, re.M)
        if m:
            para = m.group(1)
            if not para.startswith("**") and para != h["intro"]:
                body = body[:m.start(1)] + h["intro"] + body[m.end(1):]
                changed = True
    elif h.get("intro") and not re.search(r"^### Hero\s*$", body, re.M):
        # Utility pages without a Hero block: first paragraph after H1 is the lead.
        m = re.search(r"^# .+\n\n([^\n#*][^\n]*)", body, re.M)
        if m and m.group(1).strip() != h["intro"]:
            body = body[:m.start(1)] + h["intro"] + body[m.end(1):]
            changed = True
    # Hero CTAs
    for key, label in (("primary", "Primary CTA"), ("secondary", "Secondary CTA")):
        val = h.get(key)
        hero = re.search(r"^### Hero\s*$([\s\S]*?)(?=^###\s+)", body, re.M)
        if not hero:
            continue
        seg = hero.group(1)
        pat = re.compile(r"^\*\*%s:\*\*\s*([^\n]+)$" % label, re.M)
        mm = pat.search(seg)
        if val and mm and mm.group(1).strip() != val:
            seg = seg[:mm.start(1)] + val + seg[mm.end(1):]
        elif val and not mm and key == "secondary":
            pm = re.search(r"^\*\*Primary CTA:\*\*[^\n]*$", seg, re.M)
            if pm:
                seg = seg[:pm.end()] + "  \n**Secondary CTA:** " + val + seg[pm.end():]
        elif not val and mm and key == "secondary":
            seg = seg[:mm.start()] + seg[mm.end():].lstrip("\n")
        if seg != hero.group(1):
            body = body[:hero.start(1)] + seg + body[hero.end(1):]
            changed = True
    # Final CTA block
    fin = re.search(r"^#{2,3} (?:Final CTA|CTA)\s*$([\s\S]*)$", body, re.M)
    if fin and h.get("final_heading"):
        seg = fin.group(1)
        hm = re.search(r"^## (.+)$", seg, re.M)
        if hm and hm.group(1).strip() != h["final_heading"]:
            seg = seg[:hm.start(1)] + h["final_heading"] + seg[hm.end(1):]
        if h.get("final_description"):
            dm = re.search(r"^## .+\n\n([^\n*#][^\n]*)", seg, re.M)
            if dm:
                if dm.group(1).strip() != h["final_description"]:
                    seg = seg[:dm.start(1)] + h["final_description"] + seg[dm.end(1):]
            else:
                hm2 = re.search(r"^## .+$", seg, re.M)
                seg = seg[:hm2.end()] + "\n\n" + h["final_description"] + seg[hm2.end():]
        cm = re.search(r"^\*\*(?:Primary )?CTA:\*\*\s*([^\n]+)$", seg, re.M)
        if cm and h.get("final_cta") and cm.group(1).strip() != h["final_cta"]:
            seg = seg[:cm.start(1)] + h["final_cta"] + seg[cm.end(1):]
        sm = re.search(r"^\*\*Secondary CTA:\*\*\s*([^\n]+)$", seg, re.M)
        if h.get("final_secondary"):
            if sm and sm.group(1).strip() != h["final_secondary"]:
                seg = seg[:sm.start(1)] + h["final_secondary"] + seg[sm.end(1):]
            elif not sm:
                cm2 = re.search(r"^\*\*(?:Primary )?CTA:\*\*[^\n]*$", seg, re.M)
                if cm2:
                    seg = seg[:cm2.end()] + "  \n**Secondary CTA:** " + h["final_secondary"] + seg[cm2.end():]
        elif sm:
            seg = seg[:sm.start()] + seg[sm.end():].lstrip("\n")
        if seg != fin.group(1):
            body = body[:fin.start(1)] + seg + body[fin.end(1):]
            changed = True
    return head + body + tail, changed


def main():
    winners = None
    if "--winners" in sys.argv:
        winners = json.loads((ROOT / "docs" / "headline-test-winners.json").read_text())
    applied = 0
    for f in sorted(CONTENT.glob("Evolve_Copy_0*.md")):
        text = f.read_text(encoding="utf-8")
        out, pos = [], 0
        for start, end in split_blocks(text):
            out.append(text[pos:start])
            block = text[start:end]
            url_m = re.search(r"^\*\*URL:\*\*\s+`([^`]+)`", block, re.M)
            url = url_m.group(1) if url_m else None
            h = HEADLINES.get(url)
            if h:
                h = dict(h)
                if winners and url in winners:
                    h["h1"] = winners[url]
                block, changed = apply_to_block(block, h)
                applied += changed
            out.append(block)
            pos = end
        out.append(text[pos:])
        new = "".join(out)
        if new != text:
            f.write_text(new, encoding="utf-8")
    variants = {u: [h["h1"]] + h["alts"] for u, h in HEADLINES.items()}
    (ROOT / "docs" / "headline-variants.json").write_text(json.dumps(variants, indent=2), encoding="utf-8")
    print("headline layer applied to %d page blocks; %d urls with variants" % (applied, len(variants)))


if __name__ == "__main__":
    main()
