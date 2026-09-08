"""Site configuration for the Evolve Data Center Solutions website.

Everything the generator needs that is not page copy lives here: identity,
governed proof claims, navigation, footer, forms, redirects, imagery and
per-page presentation hints. Copy itself comes from content/*.md.
"""

REVIEW_BUILD = True          # noindex, robots disallow, review pill, review footer note
BUILD_DATE = "2026-09-08"

SITE = {
    "name": "Evolve Data Center Solutions",
    "short_name": "Evolve",
    "base_url": "https://www.evolveincorporated.com",
    "phone_display": "832-375-0099",
    "phone_href": "+18323750099",
    "address_lines": ["10555 Cossey Road", "Houston, Texas 77070"],
    "description": "Evolve specializes in data centers and connects Plan, Design, Build, Power and Maintain for owners, developers and operators nationwide.",
    "tagline": "Plan. Design. Build. Power. Maintain.",
    "build_version": "BUILD-002 v0.1 (review)",
    "content_version": "COPY-001 v1.0",
    "governance_version": "GOV-001 v1.0",
    "architecture_version": "ARCH-001 v1.0",
    "design_version": "DS-001 v1.0 + mockup visual direction",
}

# Governed proof statistics. Only these values may render as statistics.
CLAIMS = {
    "CLM-006": {"value": "2,200+", "label": "Mission-critical projects completed"},
    "CLM-007": {"value": "5,300+ MW", "label": "Power deployed"},
    "CLM-008": {"value": "20+ years", "label": "In business"},
    "CLM-010": {"value": "Zero injuries", "label": "Recorded since 2010"},
}

PROOF_BY_PAGE = {
    "001": ["CLM-006", "CLM-007", "CLM-008"],
    "100": ["CLM-006", "CLM-008", "CLM-010"],
    "140": ["CLM-006", "CLM-008", "CLM-010"],
    "170": ["CLM-006", "CLM-007"],
    "180": ["CLM-006", "CLM-007"],
    "190": ["CLM-006", "CLM-007"],
    "200": ["CLM-007"],
    "300": ["CLM-008"],
    "500": ["CLM-006", "CLM-007"],
    "510": ["CLM-006", "CLM-007"],
}

NAVIGATION = [
    {
        "label": "Design & Build",
        "href": "/design-build/",
        "groups": [
            {"label": "Plan", "links": [
                ["Planning & Feasibility", "/design-build/planning-feasibility/"],
                ["Preconstruction & Procurement", "/design-build/preconstruction-procurement/"],
            ]},
            {"label": "Design", "links": [
                ["Design & Engineering", "/design-build/design-engineering/"],
            ]},
            {"label": "Build", "links": [
                ["Data Center Construction", "/design-build/data-center-construction/"],
                ["Commissioning & Turnover", "/design-build/commissioning-turnover/"],
                ["Expansions & Retrofits", "/design-build/expansions-retrofits/"],
            ]},
            {"label": "Data Center Types", "links": [
                ["Modular Data Centers", "/design-build/modular-data-centers/"],
                ["Hyperscale Data Centers", "/design-build/hyperscale-data-centers/"],
                ["AI Data Centers", "/design-build/ai-data-centers/"],
            ]},
        ],
        "cta": ["Discuss a Data Center Project", "/start-a-project/"],
    },
    {
        "label": "Power Generation",
        "href": "/power-generation/",
        "groups": [
            {"label": "Power", "links": [
                ["Power Generation Overview", "/power-generation/"],
                ["Backup Power Systems", "/power-generation/backup-power-systems/"],
            ]},
            {"label": "Related", "links": [
                ["AI Data Centers", "/design-build/ai-data-centers/"],
                ["Hyperscale Data Centers", "/design-build/hyperscale-data-centers/"],
                ["Modular Data Centers", "/design-build/modular-data-centers/"],
            ]},
        ],
        "cta": ["Discuss a Power Requirement", "/start-a-project/?interest=power-generation"],
    },
    {
        "label": "Service & Maintenance",
        "href": "/maintenance/",
        "groups": [
            {"label": "Maintain", "links": [
                ["Service & Maintenance Overview", "/maintenance/"],
                ["Preventive Maintenance", "/maintenance/preventive-maintenance/"],
            ]},
            {"label": "Requests", "links": [
                ["Request Service", "/request-service/"],
                ["Existing-Customer Support", "/support/"],
            ]},
        ],
        "cta": ["Request Service", "/request-service/"],
    },
    {
        "label": "Data Center Markets",
        "href": "/data-center-markets/",
        "groups": [
            {"label": "High-Growth Facilities", "links": [
                ["AI Data Centers", "/design-build/ai-data-centers/"],
                ["Hyperscale Data Centers", "/design-build/hyperscale-data-centers/"],
                ["Modular Data Centers", "/design-build/modular-data-centers/"],
            ]},
            {"label": "Operating Environments", "links": [
                ["Colocation Data Centers", "/data-center-markets/colocation/"],
                ["Enterprise Data Centers", "/data-center-markets/enterprise/"],
            ]},
        ],
        "cta": ["Discuss This Facility Type", "/start-a-project/"],
    },
    {"label": "Insights", "href": "/insights/"},
    {"label": "About", "href": "/about/"},
]

FOOTER_GROUPS = [
    {"label": "Design & Build", "links": [
        ["Design & Build", "/design-build/"],
        ["Planning & Feasibility", "/design-build/planning-feasibility/"],
        ["Design & Engineering", "/design-build/design-engineering/"],
        ["Preconstruction & Procurement", "/design-build/preconstruction-procurement/"],
        ["Data Center Construction", "/design-build/data-center-construction/"],
        ["Commissioning & Turnover", "/design-build/commissioning-turnover/"],
        ["Expansions & Retrofits", "/design-build/expansions-retrofits/"],
    ]},
    {"label": "Data Center Types", "links": [
        ["Modular Data Centers", "/design-build/modular-data-centers/"],
        ["Hyperscale Data Centers", "/design-build/hyperscale-data-centers/"],
        ["AI Data Centers", "/design-build/ai-data-centers/"],
        ["Colocation Data Centers", "/data-center-markets/colocation/"],
        ["Enterprise Data Centers", "/data-center-markets/enterprise/"],
        ["All Data Center Markets", "/data-center-markets/"],
    ]},
    {"label": "Power & Maintain", "links": [
        ["Power Generation", "/power-generation/"],
        ["Backup Power Systems", "/power-generation/backup-power-systems/"],
        ["Service & Maintenance", "/maintenance/"],
        ["Preventive Maintenance", "/maintenance/preventive-maintenance/"],
        ["Request Service", "/request-service/"],
        ["Existing-Customer Support", "/support/"],
    ]},
    {"label": "Company", "links": [
        ["About Evolve", "/about/"],
        ["Insights", "/insights/"],
        ["Contact", "/contact/"],
        ["Start a Project", "/start-a-project/"],
        ["Website Sitemap", "/sitemap/"],
    ]},
]

LABEL_BY_PATH = {
    "/": "Home",
    "/design-build/": "Design & Build",
    "/design-build/planning-feasibility/": "Planning & Feasibility",
    "/design-build/design-engineering/": "Design & Engineering",
    "/design-build/preconstruction-procurement/": "Preconstruction & Procurement",
    "/design-build/data-center-construction/": "Data Center Construction",
    "/design-build/commissioning-turnover/": "Commissioning & Turnover",
    "/design-build/expansions-retrofits/": "Expansions & Retrofits",
    "/design-build/modular-data-centers/": "Modular Data Centers",
    "/design-build/hyperscale-data-centers/": "Hyperscale Data Centers",
    "/design-build/ai-data-centers/": "AI Data Centers",
    "/power-generation/": "Power Generation",
    "/power-generation/backup-power-systems/": "Backup Power Systems",
    "/maintenance/": "Service & Maintenance",
    "/maintenance/preventive-maintenance/": "Preventive Maintenance",
    "/data-center-markets/": "Data Center Markets",
    "/data-center-markets/colocation/": "Colocation",
    "/data-center-markets/enterprise/": "Enterprise",
    "/insights/": "Insights",
    "/insights/data-center-site-selection-power-planning/": "Site Selection & Power Planning",
    "/insights/modular-vs-traditional-data-center-delivery/": "Modular vs. Traditional Delivery",
    "/insights/ai-data-center-infrastructure-planning/": "AI Infrastructure Planning",
    "/insights/hyperscale-campus-phasing/": "Hyperscale Campus Phasing",
    "/insights/data-center-commissioning-checklist/": "Commissioning Checklist",
    "/insights/data-center-preventive-maintenance/": "Preventive Maintenance Guide",
    "/insights/data-center-monitoring-vs-dcim/": "Monitoring vs. DCIM",
    "/insights/responsible-data-center-development/": "Responsible Development",
    "/about/": "About Evolve",
    "/contact/": "Contact",
    "/support/": "Support",
    "/start-a-project/": "Start a Project",
    "/request-service/": "Request Service",
    "/thank-you/": "Submission Received",
    "/sitemap/": "Website Sitemap",
}

# Which lifecycle stages a page belongs to (drives the technical panel accent).
STAGES_BY_PATH = {
    "/design-build/": ["Plan", "Design", "Build"],
    "/design-build/planning-feasibility/": ["Plan"],
    "/design-build/design-engineering/": ["Design"],
    "/design-build/preconstruction-procurement/": ["Plan", "Build"],
    "/design-build/data-center-construction/": ["Build"],
    "/design-build/commissioning-turnover/": ["Build", "Maintain"],
    "/design-build/expansions-retrofits/": ["Plan", "Design", "Build"],
    "/design-build/modular-data-centers/": ["Design", "Build"],
    "/design-build/hyperscale-data-centers/": ["Plan", "Design", "Build"],
    "/design-build/ai-data-centers/": ["Plan", "Design", "Build", "Power"],
    "/power-generation/": ["Power"],
    "/power-generation/backup-power-systems/": ["Power"],
    "/maintenance/": ["Maintain"],
    "/maintenance/preventive-maintenance/": ["Maintain"],
}

FORM_DEFINITIONS = {
    "720": {
        "id": "general-inquiry",
        "eyebrow": "General inquiry form",
        "title": "Send a general inquiry",
        "intro": "Select the reason for your inquiry so it reaches the right Evolve team.",
        "submit": "Route My Inquiry",
        "fields": [
            {"type": "select", "id": "inquiry-type", "label": "Inquiry type", "required": True, "options": ["New data-center project", "Power generation", "Maintenance or service", "Existing-customer support", "Careers", "Vendor or subcontractor", "General inquiry"]},
            {"type": "text", "id": "name", "label": "Name", "required": True, "autocomplete": "name"},
            {"type": "text", "id": "company", "label": "Company", "required": True, "autocomplete": "organization"},
            {"type": "email", "id": "email", "label": "Work email", "required": True, "autocomplete": "email"},
            {"type": "tel", "id": "phone", "label": "Phone", "required": False, "autocomplete": "tel"},
            {"type": "textarea", "id": "message", "label": "Message", "required": True, "wide": True},
        ],
    },
    "730": {
        "id": "support-request",
        "eyebrow": "Existing customers",
        "title": "Request support",
        "intro": "Use an approved facility or agreement reference when one is available. Do not submit passwords or access credentials.",
        "submit": "Request Support",
        "fields": [
            {"type": "text", "id": "name", "label": "Name", "required": True, "autocomplete": "name"},
            {"type": "text", "id": "company", "label": "Company", "required": True, "autocomplete": "organization"},
            {"type": "email", "id": "email", "label": "Work email", "required": True, "autocomplete": "email"},
            {"type": "tel", "id": "phone", "label": "Phone", "required": True, "autocomplete": "tel"},
            {"type": "text", "id": "reference", "label": "Existing Evolve reference", "required": False},
            {"type": "textarea", "id": "description", "label": "Describe the support need", "required": True, "wide": True},
        ],
    },
    "800": {
        "id": "project-brief",
        "eyebrow": "Project intake",
        "title": "Submit a project brief",
        "intro": "Tell Evolve what is being planned, built or changed and which decision is controlling progress.",
        "submit": "Submit Project Brief",
        "fields": [
            {"type": "text", "id": "name", "label": "Name", "required": True, "autocomplete": "name"},
            {"type": "text", "id": "company", "label": "Company", "required": True, "autocomplete": "organization"},
            {"type": "email", "id": "email", "label": "Work email", "required": True, "autocomplete": "email"},
            {"type": "tel", "id": "phone", "label": "Phone", "required": True, "autocomplete": "tel"},
            {"type": "select", "id": "interest", "label": "Primary interest", "required": True, "options": ["Design & Build", "Modular Data Centers", "Hyperscale Data Centers", "AI Data Centers", "Power Generation", "Service & Maintenance", "Other"]},
            {"type": "select", "id": "stage", "label": "Project stage", "required": True, "options": ["Concept", "Planning", "Design", "Procurement", "Construction", "Commissioning", "Operating facility"]},
            {"type": "text", "id": "region", "label": "State or region", "required": True, "autocomplete": "address-level1"},
            {"type": "textarea", "id": "summary", "label": "Project summary and immediate constraint", "required": True, "wide": True},
        ],
    },
    "810": {
        "id": "service-request",
        "eyebrow": "Service intake",
        "title": "Submit a service request",
        "intro": "Provide the facility context, service need and operating constraints.",
        "submit": "Submit Service Request",
        "fields": [
            {"type": "text", "id": "name", "label": "Name", "required": True, "autocomplete": "name"},
            {"type": "text", "id": "company", "label": "Company", "required": True, "autocomplete": "organization"},
            {"type": "email", "id": "email", "label": "Work email", "required": True, "autocomplete": "email"},
            {"type": "tel", "id": "phone", "label": "Phone", "required": True, "autocomplete": "tel"},
            {"type": "select", "id": "customer-status", "label": "New or existing customer", "required": True, "options": ["New inquiry", "Existing customer"]},
            {"type": "select", "id": "service-interest", "label": "Service interest", "required": True, "options": ["Preventive Maintenance", "Power-related maintenance", "Critical-infrastructure maintenance", "Existing-customer support", "Other"]},
            {"type": "select", "id": "facility-status", "label": "Facility status", "required": True, "options": ["Operating", "Commissioning", "Construction", "Planned"]},
            {"type": "textarea", "id": "summary", "label": "Request summary and operating constraint", "required": True, "wide": True},
        ],
    },
}

INSIGHT_PATHS = {
    "/insights/data-center-site-selection-power-planning/",
    "/insights/modular-vs-traditional-data-center-delivery/",
    "/insights/ai-data-center-infrastructure-planning/",
    "/insights/hyperscale-campus-phasing/",
    "/insights/data-center-commissioning-checklist/",
    "/insights/data-center-preventive-maintenance/",
    "/insights/data-center-monitoring-vs-dcim/",
    "/insights/responsible-data-center-development/",
}

_SOURCES = {
    "jll": ("JLL, 2026 Global Data Center Outlook", "https://www.jll.com/content/dam/jllcom/en/global/documents/reports/research-reports/26-research-global-data-center-outlook-new.pdf", "January 2026"),
    "cbre": ("CBRE, North America Data Center Trends H1 2026", "https://www.cbre.com/insights/books/north-america-data-center-trends-h1-2026", "August 27, 2026"),
    "uptime": ("Uptime Institute, Global Data Center Survey 2026", "https://datacenter.uptimeinstitute.com/rs/711-RIA-145/images/UptimeInstitute.GlobalDataCenterSurvey.2026.pdf", "July 2026"),
    "ashrae": ("ASHRAE / PNNL / NEMA, AI Data Center Energy Performance Framework", "https://www.ashrae.org/technical-resources/ai-data-center-framework", "retrieved September 7, 2026"),
}

INSIGHT_SOURCES = {
    "/insights/data-center-site-selection-power-planning/": [_SOURCES["jll"], _SOURCES["cbre"]],
    "/insights/modular-vs-traditional-data-center-delivery/": [_SOURCES["jll"]],
    "/insights/ai-data-center-infrastructure-planning/": [_SOURCES["jll"], _SOURCES["uptime"], _SOURCES["ashrae"]],
    "/insights/hyperscale-campus-phasing/": [_SOURCES["jll"], _SOURCES["cbre"]],
    "/insights/data-center-preventive-maintenance/": [_SOURCES["uptime"]],
    "/insights/data-center-monitoring-vs-dcim/": [_SOURCES["uptime"]],
    "/insights/responsible-data-center-development/": [_SOURCES["jll"], _SOURCES["ashrae"]],
}

# Short descriptions for insight cards on the hub (from each article's meta description).
INSIGHT_TOPICS = {
    "/insights/data-center-site-selection-power-planning/": "Planning & Power",
    "/insights/responsible-data-center-development/": "Planning & Power",
    "/insights/modular-vs-traditional-data-center-delivery/": "Delivery Approaches",
    "/insights/hyperscale-campus-phasing/": "Delivery Approaches",
    "/insights/ai-data-center-infrastructure-planning/": "AI Infrastructure",
    "/insights/data-center-commissioning-checklist/": "Commissioning & Operations",
    "/insights/data-center-preventive-maintenance/": "Commissioning & Operations",
    "/insights/data-center-monitoring-vs-dcim/": "Commissioning & Operations",
}

NOINDEX_PATHS = {"/start-a-project/", "/request-service/", "/thank-you/"}

# Legacy and draft routes -> canonical destinations (one-hop 301 at the host).
REDIRECTS = {
    "/index.php": "/",
    "/index.php/": "/",
    "/services/design-build/": "/design-build/",
    "/design-and-build/": "/design-build/",
    "/services/power-generation/": "/power-generation/",
    "/services/facility-management/": "/maintenance/",
    "/service-and-maintenance/": "/maintenance/",
    "/preventative-maintenance/": "/maintenance/preventive-maintenance/",
    "/services/elert-monitoring/": "/maintenance/",
    "/elert-tm-monitoring/": "/maintenance/",
    "/industries/": "/data-center-markets/",
    "/markets-we-serve/": "/data-center-markets/",
    "/markets-we-serve/colocation/": "/data-center-markets/colocation/",
    "/markets-we-serve/modular-data-centers/": "/design-build/modular-data-centers/",
    "/solutions/": "/design-build/",
    "/solutions/ai-hpc/": "/design-build/ai-data-centers/",
    "/solutions/ai-hpc-data-centers/": "/design-build/ai-data-centers/",
    "/ai-ready-data-centers/": "/design-build/ai-data-centers/",
    "/solutions/modular/": "/design-build/modular-data-centers/",
    "/solutions/modular-data-centers/": "/design-build/modular-data-centers/",
    "/solutions/colocation/": "/data-center-markets/colocation/",
    "/solutions/colocation-data-centers/": "/data-center-markets/colocation/",
    "/solutions/edge/": "/data-center-markets/",
    "/solutions/edge-data-centers/": "/data-center-markets/",
    "/industries/colocation-providers/": "/data-center-markets/colocation/",
    "/solutions/greenfield/": "/design-build/planning-feasibility/",
    "/solutions/greenfield-new-builds/": "/design-build/planning-feasibility/",
    "/solutions/brownfield/": "/design-build/expansions-retrofits/",
    "/solutions/brownfield-retrofit/": "/design-build/expansions-retrofits/",
    "/company-news/": "/insights/",
    "/leadership/": "/about/",
}

# ---------------------------------------------------------------------------
# Imagery. Every image here is Evolve-owned project photography extracted from
# the August 2026 qualification decks or the Evolve Website Build folder.
# No stock, renders, customer names or identifiable projects.
# ---------------------------------------------------------------------------
IMAGES = {
    "shop": {"file": "evolve-fabrication-shop", "widths": [1920, 1280, 800], "w": 2429, "h": 1369,
             "alt": "Steel module frame under the 25-ton overhead crane inside the Evolve modular fabrication shop"},
    "frame": {"file": "evolve-module-steel-frame", "widths": [1600, 1000, 640], "w": 2475, "h": 1396,
              "alt": "Welded structural steel frame of a data-center module in fabrication"},
    "crane-lift": {"file": "evolve-module-crane-lift", "widths": [990, 640], "w": 990, "h": 1027,
                   "alt": "A crane lifts a prefabricated data-center module from a trailer while a technician guides the set"},
    "crane-set": {"file": "evolve-module-crane-set", "widths": [990, 640], "w": 990, "h": 1027,
                  "alt": "Two cranes set a prefabricated data-center module onto its foundation"},
    "yard": {"file": "evolve-equipment-yard", "widths": [1600, 1000, 640], "w": 1651, "h": 861,
             "alt": "Evolve service trucks and a generator package staged beside a data-center building"},
    "module-wall": {"file": "evolve-module-cooling-wall", "widths": [1050, 640], "w": 1050, "h": 706,
                    "alt": "Exterior wall of an installed data-center module with roof-mounted cooling units"},
    "module-entry": {"file": "evolve-module-entry", "widths": [688], "w": 688, "h": 465,
                     "alt": "Entrance stair and electrical disconnects on an installed data-center module"},
    "module-exterior": {"file": "evolve-module-exterior", "widths": [552], "w": 552, "h": 457,
                        "alt": "Installed data-center module with entry platform and side-mounted cooling"},
    "power-louvers": {"file": "evolve-power-module-louvers", "widths": [542], "w": 542, "h": 407,
                      "alt": "Enclosed power module with intake louvers and access platform on site"},
    "power-aerial": {"file": "evolve-power-modules-aerial", "widths": [570], "w": 570, "h": 407,
                     "alt": "Aerial view of a row of installed power modules with Evolve service trucks"},
    "switchgear": {"file": "evolve-switchgear-lineup", "widths": [306], "w": 306, "h": 407,
                   "alt": "Low-voltage switchgear lineup inside a data-center electrical room"},
    "electrical-room": {"file": "evolve-electrical-room", "widths": [307], "w": 307, "h": 407,
                        "alt": "Electrical room corridor between distribution panels and overhead conduit"},
    "data-hall-aisle": {"file": "evolve-data-hall-aisle", "widths": [306], "w": 306, "h": 407,
                        "alt": "Contained cold aisle inside a data hall with raised access floor"},
    "data-hall-grated": {"file": "evolve-data-hall-grated", "widths": [306], "w": 306, "h": 407,
                         "alt": "Data hall aisle with perforated floor tiles between rack rows"},
}

# Per-page hero presentation and section-level media hints.
PAGE_MEDIA = {
    "/": {"hero": "shop", "hero_style": "full",
          "bands": {"Power cannot be treated as a late-stage package": "yard",
                    "The work continues after turnover": "module-wall"}},
    "/design-build/": {"hero": "crane-lift", "strip": ["shop", "frame", "crane-set", "module-entry"]},
    "/design-build/planning-feasibility/": {"mosaic": ["yard", "power-aerial", "module-entry", "crane-set"]},
    "/design-build/design-engineering/": {"hero": "frame"},
    "/design-build/preconstruction-procurement/": {"hero": "shop"},
    "/design-build/data-center-construction/": {"hero": "crane-set", "strip": ["switchgear", "electrical-room", "data-hall-aisle", "data-hall-grated"]},
    "/design-build/commissioning-turnover/": {"mosaic": ["switchgear", "electrical-room", "data-hall-aisle", "data-hall-grated"]},
    "/design-build/expansions-retrofits/": {"hero": "module-wall"},
    "/design-build/modular-data-centers/": {"hero": "frame", "strip": ["crane-lift", "crane-set", "module-entry", "module-exterior"]},
    "/design-build/hyperscale-data-centers/": {"mosaic": ["yard", "power-aerial", "data-hall-grated", "crane-lift"]},
    "/design-build/ai-data-centers/": {"mosaic": ["data-hall-grated", "switchgear", "data-hall-aisle", "electrical-room"]},
    "/power-generation/": {"hero": "yard", "strip": ["power-louvers", "power-aerial", "switchgear", "electrical-room"]},
    "/power-generation/backup-power-systems/": {"mosaic": ["power-louvers", "switchgear", "power-aerial", "electrical-room"]},
    "/maintenance/": {"hero": "module-entry", "strip": ["switchgear", "power-louvers", "module-exterior", "electrical-room"]},
    "/maintenance/preventive-maintenance/": {"mosaic": ["switchgear", "electrical-room", "module-exterior", "power-louvers"]},
    "/data-center-markets/": {"mosaic": ["data-hall-aisle", "yard", "module-wall", "crane-set"]},
    "/data-center-markets/colocation/": {"mosaic": ["data-hall-grated", "electrical-room", "module-entry", "switchgear"]},
    "/data-center-markets/enterprise/": {"mosaic": ["electrical-room", "data-hall-aisle", "module-exterior", "switchgear"]},
    "/about/": {"hero": "shop", "strip": ["yard", "crane-lift", "frame", "module-entry"]},
}

# Card imagery keyed by the destination URL of the card's link.
CARD_IMAGES = {
    "/design-build/": "shop",
    "/design-build/planning-feasibility/": "yard",
    "/design-build/design-engineering/": "frame",
    "/design-build/preconstruction-procurement/": "module-exterior",
    "/design-build/data-center-construction/": "crane-lift",
    "/design-build/commissioning-turnover/": "switchgear",
    "/design-build/expansions-retrofits/": "module-wall",
    "/design-build/modular-data-centers/": "crane-set",
    "/design-build/hyperscale-data-centers/": "power-aerial",
    "/design-build/ai-data-centers/": "data-hall-grated",
    "/power-generation/": "yard",
    "/power-generation/backup-power-systems/": "power-louvers",
    "/maintenance/": "module-entry",
    "/maintenance/preventive-maintenance/": "electrical-room",
    "/data-center-markets/colocation/": "data-hall-aisle",
    "/data-center-markets/enterprise/": "electrical-room",
}

LIFECYCLE = ["Plan", "Design", "Build", "Power", "Maintain"]
LIFECYCLE_LINKS = {
    "Plan": "/design-build/planning-feasibility/",
    "Design": "/design-build/design-engineering/",
    "Build": "/design-build/data-center-construction/",
    "Power": "/power-generation/",
    "Maintain": "/maintenance/",
}

# Section titles rendered as emphasis callouts rather than running prose.
CALLOUT_TITLES = {
    "proof", "approved proof", "approved aggregate experience", "proof presented accurately",
    "proof without project disclosure", "experience and safety",
    "experience without exposing confidential work", "safety",
    "confidentiality is part of professional conduct", "evolve's role",
    "aggregate experience", "experience at a glance",
}
