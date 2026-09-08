#!/usr/bin/env python3
"""Build the website image catalog as CSV.

Scans dist/ to record exactly where each image is used, joins that with the
image registry in data.py, and adds the replacement brief and generation prompt
for every asset plus the pages that still need dedicated photography.
Output: docs/image-catalog.csv (also printed to stdout when --stdout is given).
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import data as D  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

STYLE = ("Photorealistic editorial documentary photograph, natural or practical light, shallow depth of field, "
         "true-color grading, no CGI, no neon or blue server-room glow, no visible customer names, logos or signage "
         "other than Evolve, no text overlays.")

# Replacement briefs keyed by image registry key.
BRIEFS = {
    "shop": {
        "issue": "Best photo in the set but only 2,429 px wide; slight motion blur; no person clearly visible.",
        "need": "Hero-grade landscape, 4,000 px or wider, 21:9-safe framing of the fabrication shop with the Evolve crane banner readable and one or two technicians at work.",
        "prompt": STYLE + " Wide interior of a steel fabrication shop: a welded data-center module frame under a yellow 25-ton overhead crane carrying an 'evolve' banner, two technicians in hard hats and red Evolve polos working at the frame, sparks or measuring tape in hand, late-afternoon light through the bay door, landscape 21:9.",
        "source": "Reshoot at the Evolve fabrication shop with a photographer; keep the banner in frame.",
        "priority": "High",
    },
    "frame": {
        "issue": "Phone photo stored rotated; 2,475 px after rotation; no people; composition is tight.",
        "need": "Landscape photo of the structural frame in fabrication with a welder or fitter in frame, 3,000 px or wider.",
        "prompt": STYLE + " Structural steel frame of a prefabricated data-center module inside a fabrication shop, a welder in a hood working at a corner joint, shop lights overhead, raw steel and weld beads visible, landscape 3:2.",
        "source": "Reshoot in the Evolve shop during frame fabrication.",
        "priority": "High",
    },
    "crane-lift": {
        "issue": "Only 990 px wide, phone quality, portrait; crane company branding is prominent.",
        "need": "High-resolution landscape of a module being lifted from the trailer with Evolve crew visible; crop away third-party crane branding.",
        "prompt": STYLE + " A crane lifts a prefabricated data-center module off a flatbed trailer on a cleared job site, rigging straps taut, one Evolve technician in a hi-vis vest and red polo guiding with a tag line, overcast sky, pine trees behind, landscape 3:2.",
        "source": "Capture at the next module set; ask the crane vendor for clearance or frame out their logos.",
        "priority": "High",
    },
    "crane-set": {
        "issue": "Only 990 px wide, phone quality, portrait.",
        "need": "High-resolution landscape of two cranes setting a module on its foundation with the crew in frame.",
        "prompt": STYLE + " Two cranes set a prefabricated data-center module onto a concrete foundation, spreader bars and blue straps visible, a small crew in hard hats watching the placement, cleared site with sand and pines, landscape 3:2.",
        "source": "Capture at the next module set.",
        "priority": "High",
    },
    "yard": {
        "issue": "1,651 px wide, wide-angle distortion, harsh midday light; bright sky fights the dark hero treatment.",
        "need": "Higher-resolution photo of branded Evolve trucks and a generator package at a facility, shot early or late in the day, 3,000 px or wider.",
        "prompt": STYLE + " White Evolve service trucks parked beside a containerized generator package and a data-center building, a technician opening an enclosure door, warm early-morning light, long shadows, landscape 21:9.",
        "source": "Reshoot at the equipment yard or a customer site with permission; golden-hour timing.",
        "priority": "Medium",
    },
    "module-wall": {
        "issue": "1,050 px wide; tree shadows across the wall; no people.",
        "need": "Clean landscape of an installed module with roof-mounted cooling units, 2,400 px or wider, ideally with a technician on the access platform.",
        "prompt": STYLE + " Exterior of an installed data-center module in a wooded clearing, roof-mounted condensing units in a row, a technician on the steel access platform checking a disconnect, dappled afternoon light, landscape 3:2.",
        "source": "Capture at an operating module site with owner permission.",
        "priority": "Medium",
    },
    "module-entry": {
        "issue": "688 px wide; soft; fine for cards but not for heroes.",
        "need": "High-resolution version of the module entrance with stair, disconnects and bollards, 2,400 px or wider.",
        "prompt": STYLE + " Entrance stair of a prefabricated data-center module with yellow handrails, wall-mounted electrical disconnects and yellow bollards, a technician carrying a tool bag up the steps, blue sky with light clouds, landscape 3:2.",
        "source": "Reshoot at an operating module site.",
        "priority": "Medium",
    },
    "module-exterior": {
        "issue": "552 px wide; deck-quality only.",
        "need": "High-resolution exterior of an installed module with entry platform and side-mounted cooling, 2,400 px or wider.",
        "prompt": STYLE + " Three-quarter view of an installed prefabricated data-center module with an entry platform, side-mounted cooling units and a service door, pine trees behind, mid-morning light, landscape 3:2.",
        "source": "Reshoot at an operating module site.",
        "priority": "Medium",
    },
    "power-louvers": {
        "issue": "542 px wide; heavy compression; safety cones and cabling clutter the foreground.",
        "need": "High-resolution photo of an enclosed power module with intake louvers and access platform, tidy site, 2,400 px or wider.",
        "prompt": STYLE + " Enclosed generator power module with large intake louvers and a galvanized access platform, a technician on the platform opening the control door, clean gravel pad, distant row of matching modules, clear sky, landscape 3:2.",
        "source": "Capture at a power-module installation.",
        "priority": "High",
    },
    "power-aerial": {
        "issue": "570 px wide; low-altitude phone shot; useful composition.",
        "need": "Drone photo of a row of installed power modules with Evolve trucks, 4,000 px or wider, landscape.",
        "prompt": STYLE + " Aerial drone photograph of a row of five containerized power modules on concrete pads beside a data-center building, white Evolve service trucks parked nearby, cable trenches visible, green field around the site, soft late-afternoon light, landscape 16:9.",
        "source": "Commission a drone shoot at a completed power installation.",
        "priority": "High",
    },
    "switchgear": {
        "issue": "306 px wide portrait; phone photo; usable only in mosaics.",
        "need": "High-resolution landscape or portrait of a switchgear lineup in an electrical room, 2,400 px or wider.",
        "prompt": STYLE + " Low-voltage switchgear lineup inside a data-center electrical room, breaker cubicles with status indicators, a technician reading a meter with a clipboard, cool overhead lighting, landscape 3:2.",
        "source": "Capture during a commissioning or maintenance visit with owner permission.",
        "priority": "High",
    },
    "electrical-room": {
        "issue": "307 px wide portrait; phone photo.",
        "need": "High-resolution photo of an electrical room corridor between distribution panels, 2,400 px or wider.",
        "prompt": STYLE + " Corridor between rows of gray electrical distribution panels and transformers in a data-center electrical room, overhead conduit and cable tray, a technician walking away with a torque wrench, landscape 3:2.",
        "source": "Capture during a commissioning or maintenance visit with owner permission.",
        "priority": "High",
    },
    "data-hall-aisle": {
        "issue": "306 px wide portrait; phone photo; reflective containment glare.",
        "need": "High-resolution data-hall aisle with containment doors and raised floor, 2,400 px or wider, no customer signage.",
        "prompt": STYLE + " Contained cold aisle inside a data hall, glass containment doors, raised access floor with perforated tiles, rack fronts with blanking panels, a technician with a laptop cart at the far end, neutral white lighting, landscape 3:2.",
        "source": "Capture in a completed data hall with owner permission, or in the Evolve modular data hall before handover.",
        "priority": "High",
    },
    "data-hall-grated": {
        "issue": "306 px wide portrait; phone photo.",
        "need": "High-resolution data-hall aisle with grated floor tiles between rack rows, 2,400 px or wider.",
        "prompt": STYLE + " Data hall aisle with black rack rows on both sides and a strip of grated floor tiles down the center, overhead busway and lighting, a technician racking equipment mid-aisle, neutral white lighting, landscape 3:2.",
        "source": "Capture in a completed data hall or a modular hall before handover.",
        "priority": "High",
    },
}

HEADSHOT_TEMPLATE = ("Leadership headshot template (scripts/headshot-template.swift): 4:5 portrait, face about one third of the frame height with headroom, "
                     "subject lifted onto a neutral gray studio backdrop, black-and-white grade, delivered at 800x1000 and 400x500. "
                     "Wardrobe standard: collared shirt and sports coat with no tie for men; professional business wear for women.")
RETOUCH = ("Retouch brief (Photoshop Generative Fill, Firefly or a retoucher), keep the face, expression and lighting untouched, photorealistic, no AI look: ")

HEADSHOTS = {
    "tye-johnson": {"file": "Tye-intro.jpg", "size": "598 x 598", "priority": "High",
                    "issue": "Source is a tight, casual outdoor crop; no jacket or collar visible; little headroom.",
                    "need": "Wardrobe to the standard and a looser crop, or a new studio headshot.",
                    "prompt": RETOUCH + "add a charcoal sports coat over an open-collar white dress shirt, extend the canvas for headroom and shoulders.",
                    "source": "Preferred: reshoot on the template spec. " + HEADSHOT_TEMPLATE},
    "clay-bludau": {"file": "Clay-intro.jpg", "size": "551 x 551", "priority": "High",
                    "issue": "Wearing a baseball cap; casual outdoor photo; tight crop.",
                    "need": "Cap removed and wardrobe to the standard, or a new studio headshot.",
                    "prompt": RETOUCH + "remove the baseball cap and reconstruct natural short hair, add a navy sports coat over an open-collar light blue shirt, extend headroom.",
                    "source": "Preferred: reshoot on the template spec."},
    "zeeshan-siddiqui": {"file": "zeeshan-siddiqui.jpg", "size": "800 x 800", "priority": "Medium",
                         "issue": "Studio headshot in a suit with a tie; the standard is no tie.",
                         "need": "Tie removed with an open collar.",
                         "prompt": RETOUCH + "remove the necktie, open the top collar button naturally, keep the suit jacket.",
                         "source": "Retouch is sufficient; no reshoot needed."},
    "chuck-haigh": {"file": "b2ap3_large_Haigh_Chuck.jpg (blog version, 791 x 1200)", "size": "791 x 1200", "priority": "Low",
                    "issue": "Meets the standard: studio portrait, gray sports coat, open-collar plaid shirt.",
                    "need": "None; higher-resolution original if available.",
                    "prompt": "No retouch required.", "source": "Reference example for the template."},
    "matt-gibson": {"file": "matt-gibson.jpg", "size": "389 x 389", "priority": "Medium",
                    "issue": "Meets the standard (dark jacket, open collar) but only 389 px; slightly soft at card size.",
                    "need": "Higher-resolution original from Evolve.",
                    "prompt": "No wardrobe retouch required.", "source": "Request the original file."},
    "lindy-devitt": {"file": "lindy-devitt.jpg", "size": "400 x 400", "priority": "Low",
                     "issue": "Meets the standard (professional black top with Evolve mark); 400 px source.",
                     "need": "Higher-resolution original if available.",
                     "prompt": "No retouch required.", "source": "Request the original file."},
    "bo-williamson": {"file": "bo-williamson.jpg", "size": "791 x 791", "priority": "High",
                      "issue": "Wearing a white Evolve cap and a polo shirt; outdoor photo.",
                      "need": "Cap removed and wardrobe to the standard, or a new studio headshot.",
                      "prompt": RETOUCH + "remove the cap and reconstruct natural hair, replace the polo with an open-collar white shirt and charcoal sports coat.",
                      "source": "Preferred: reshoot on the template spec."},
    "doug-herron": {"file": "doug-herron.jpg", "size": "298 x 298", "priority": "High",
                    "issue": "Casual indoor photo, 298 px only; collared shirt but no jacket; tight crop.",
                    "need": "Sports coat added and a higher-resolution photo, or a new studio headshot.",
                    "prompt": RETOUCH + "add a navy sports coat over the existing light collared shirt, extend headroom and shoulders.",
                    "source": "Preferred: reshoot on the template spec."},
    "molly-petty": {"missing": True, "priority": "High",
                    "issue": "No photograph exists on the current site or in the Drive folders; a placeholder tile is shown.",
                    "need": "New headshot to the template spec.",
                    "prompt": "No generation: request a photograph. " + HEADSHOT_TEMPLATE,
                    "source": "Request from Evolve marketing or schedule with the leadership photo session."},
    "terra-lewis": {"file": "terra-lewis.jpg", "size": "278 x 278", "priority": "Medium",
                    "issue": "Professional business wear meets the standard, but the source is a 278 px indoor phone photo.",
                    "need": "Higher-resolution photo or a new studio headshot.",
                    "prompt": "No wardrobe retouch required.", "source": "Preferred: reshoot on the template spec."},
    "isaiah-amador": {"file": "isaiah-amador.jpg", "size": "640 x 640", "priority": "Low",
                      "issue": "Meets the standard: studio portrait, gray jacket, open collar.",
                      "need": "None.", "prompt": "No retouch required.", "source": "Reference example for the template."},
    "steven-eickenhorst": {"file": "steven-eickenhorst.jpg", "size": "235 x 235", "priority": "High",
                           "issue": "Wearing an Astros cap and a dark T-shirt; 235 px phone photo.",
                           "need": "New studio headshot to the template spec.",
                           "prompt": RETOUCH + "remove the cap and reconstruct natural hair, add an open-collar shirt and charcoal sports coat; resolution will remain limited.",
                           "source": "Reshoot required; retouch is a stopgap only."},
    "krista-bouquet": {"missing": True, "priority": "High",
                       "issue": "No photograph exists on the current site or in the Drive folders; a placeholder tile is shown. Listed title is a department name.",
                       "need": "New headshot to the template spec and a confirmed title.",
                       "prompt": "No generation: request a photograph. " + HEADSHOT_TEMPLATE,
                       "source": "Request from Evolve marketing or schedule with the leadership photo session."},
}

# Pages that currently have no dedicated hero photograph.
PAGE_NEEDS = [
    ("/design-build/planning-feasibility/", "Planning & Feasibility", "2x2 mosaic of existing photos",
     "Site and power planning imagery: an Evolve planner and an owner reviewing site drawings at a cleared site or over a table with a plan set.",
     STYLE + " Two people in Evolve polos and hard hats reviewing a rolled site plan on the hood of a white Evolve truck at a cleared development site, transmission towers on the horizon, early morning light, landscape 21:9."),
    ("/design-build/commissioning-turnover/", "Commissioning & Turnover", "2x2 mosaic of existing photos",
     "Commissioning imagery: technicians testing switchgear or a generator with instruments and a checklist.",
     STYLE + " A commissioning technician with a clamp meter and tablet checklist in front of an open switchgear section while a colleague watches the display, electrical room, focused expressions, landscape 3:2."),
    ("/design-build/hyperscale-data-centers/", "Hyperscale Data Centers", "2x2 mosaic of existing photos",
     "Scale imagery: a large data-center campus under construction or a long row of installed power modules.",
     STYLE + " Aerial drone photograph of a large data-center construction site with multiple building pads, tower cranes and a long row of installed power modules, access roads and laydown yards, wide flat Texas landscape, landscape 16:9."),
    ("/design-build/ai-data-centers/", "AI Data Centers", "2x2 mosaic of existing photos",
     "High-density hall imagery: dense rack rows with liquid-cooling manifolds or overhead busway, no vendor logos.",
     STYLE + " Data hall with dense rack rows, overhead busway and coolant distribution manifolds, a technician connecting a hose at a rear door, neutral white light, no visible vendor logos, landscape 3:2."),
    ("/power-generation/backup-power-systems/", "Backup Power Systems", "2x2 mosaic of existing photos",
     "Backup power imagery: generator enclosure with a technician performing a load test or checking fuel.",
     STYLE + " Technician in an Evolve polo drawing a fuel sample from a generator day tank into a test jar beside a containerized generator, morning light, landscape 3:2."),
    ("/maintenance/preventive-maintenance/", "Preventive Maintenance", "2x2 mosaic of existing photos",
     "Maintenance imagery: a technician servicing a generator, UPS or switchgear with a clipboard or tablet.",
     STYLE + " Technician kneeling at an open generator enclosure replacing a filter, tools laid out on a cloth, a service truck behind, overcast soft light, landscape 3:2."),
    ("/data-center-markets/", "Data Center Markets", "2x2 mosaic of existing photos",
     "Facility-type overview imagery: a completed data-center exterior at dusk with practical lighting.",
     STYLE + " Exterior of a completed single-story data-center building at dusk, exterior wall packs lit, generator yard and cooling equipment behind a fence, parking lot with Evolve truck, blue-hour sky, landscape 21:9."),
    ("/data-center-markets/colocation/", "Colocation Data Centers", "2x2 mosaic of existing photos",
     "Colocation imagery: cage or suite corridor with multiple customer areas, no customer branding.",
     STYLE + " Corridor between locked colocation cages in a data hall, mesh partitions, raised floor, a technician escorting a client with a badge, neutral lighting, landscape 3:2."),
    ("/data-center-markets/enterprise/", "Enterprise Data Centers", "2x2 mosaic of existing photos",
     "Enterprise retrofit imagery: work in a live electrical room or an older facility being upgraded.",
     STYLE + " Technicians installing a new distribution panel beside an older lineup in a live enterprise electrical room, temporary barriers and lockout tags visible, landscape 3:2."),
    ("/insights/", "Insights hub and eight articles", "Dark technical panel (no photo)",
     "Optional editorial imagery per article: planning tables, drone site views, commissioning tests, maintenance findings.",
     STYLE + " Close-up of an engineer's hands annotating a single-line diagram with a red pen beside a laptop, desk lamp light, landscape 3:2."),
    ("/about/", "About Evolve", "Fabrication shop hero",
     "People-forward team imagery: field crew and office team, no headshots required. Also 13 leadership portraits if a Leadership page is added.",
     STYLE + " Small group of Evolve field technicians and project managers in red and black polos standing in front of a white Evolve service truck and a prefabricated module, relaxed, mid-morning light, landscape 3:2."),
    ("/", "Home (optional alternate hero)", "Fabrication shop hero",
     "A second hero option showing a completed installation with people, to rotate with the fabrication shop.",
     STYLE + " A crane sets a prefabricated data-center module beside one already running, Evolve crew guiding it, sunrise light, wide landscape 21:9."),
    ("sitewide", "Open Graph share image", "Fabrication shop crop, no logo",
     "Designed 1200x630 share image with the approved white logo over an approved photo.",
     "Compose in design software: approved Evolve white logo on the left third over a darkened fabrication-shop photograph; no generated imagery required."),
    ("sitewide", "Favicon and app icon", "Crop of the approved red e",
     "Brand-owner confirmation that the red e may stand alone as favicon and app icon, or an approved icon file.",
     "No generation needed; request approval or an approved icon from the brand owner."),
]


def usage_index():
    """Map image file base -> sorted list of 'page (role)' strings by scanning dist."""
    uses = {}
    for f in DIST.rglob("index.html"):
        rel = "/" + str(f.parent.relative_to(DIST)).replace("\\", "/") + "/"
        rel = "/" if rel == "/./" else rel
        if rel in D.REDIRECTS:
            continue
        html = f.read_text(encoding="utf-8")
        for key, im in D.IMAGES.items():
            base = im["file"]
            if base not in html:
                continue
            roles = []
            if re.search(r'class="hero-media">\s*<img src="/img/%s' % base, html) or re.search(r'class="hero-figure">\s*<img src="/img/%s' % base, html):
                roles.append("hero")
            if re.search(r'class="mosaic-tile">\s*<img src="/img/%s' % base, html):
                roles.append("hero mosaic")
            if re.search(r'class="card-media">\s*<img src="/img/%s' % base, html):
                roles.append("card")
            if re.search(r'class="strip-tile">\s*<img src="/img/%s' % base, html):
                roles.append("photo strip")
            if re.search(r'<figure>\s*<img src="/img/%s' % base, html):
                roles.append("section image")
            if re.search(r'class="leader-photo">\s*<img src="/img/%s' % base, html):
                roles.append("headshot")
            label = D.LABEL_BY_PATH.get(rel, rel)
            uses.setdefault(key, []).append("%s (%s)" % (label, ", ".join(roles) or "inline"))
    return uses


def main():
    uses = usage_index()
    rows = []
    header = ["#", "Image", "File", "Type", "Used on (page and role)", "Current source", "Native size (px)",
              "Issue with current image", "What is needed", "Generation prompt", "Sourcing brief", "Priority"]
    n = 0
    for key, im in D.IMAGES.items():
        n += 1
        if key.startswith("team-"):
            slug = key[5:]
            h = HEADSHOTS.get(slug, {})
            rows.append([n, key, "public/img/%s-*.jpg" % im["file"], "Leadership headshot (template applied)",
                         "; ".join(sorted(set(uses.get(key, [])))) or "unused",
                         "evolveincorporated.com/images/leadership (cleared for use 2026-09-08); source file %s" % h.get("file", "?"),
                         h.get("size", "?"), h.get("issue", ""), h.get("need", ""), h.get("prompt", ""), h.get("source", "Request a new headshot from Evolve if retouching is not acceptable."), h.get("priority", "Medium")])
            continue
        stock = key not in BRIEFS
        origin = im.get("source", "")
        if stock and origin == "current":
            default = {"issue": "Photo from the current Evolve site; cleared for use 2026-09-08. Resolution and provenance still worth confirming with Evolve.",
                       "need": "Original file from Evolve if a larger version exists.",
                       "prompt": STYLE + " " + im["alt"] + ", landscape 3:2.",
                       "source": "Request the original from Evolve marketing.", "priority": "Low"}
            src_label = "Current site evolveincorporated.com (cleared for use 2026-09-08)"
        elif stock and origin == "both":
            default = {"issue": "Appears on both the current site and the mockup; stock use approved for review 2026-09-08, license to confirm before production.",
                       "need": "License confirmation or an Evolve-owned photo of the same subject.",
                       "prompt": STYLE + " " + im["alt"] + ", landscape 3:2.",
                       "source": "Confirm the license or reshoot.", "priority": "Medium"}
            src_label = "Both sites (2026-09-08 import)"
        else:
            default = {"issue": "Imported mockup stock; approved for review use 2026-09-08 (M. Atnipp). License must be confirmed before production.",
                       "need": "License confirmation or an Evolve-owned photo of the same subject.",
                       "prompt": STYLE + " " + im["alt"] + ", landscape 3:2.",
                       "source": "Confirm the license or reshoot.", "priority": "Medium"}
            src_label = "Mockup site (stock, 2026-09-08 import)"
        b = BRIEFS.get(key, default)
        rows.append([n, key, "public/img/%s-*.jpg" % im["file"],
                     ("Evolve site photograph (imported)" if origin == "current" else "Stock photograph (imported)") if stock else "Photograph",
                     "; ".join(sorted(set(uses.get(key, [])))) or "unused",
                     (src_label if stock else "Evolve qualification decks (Aug 2026) and Evolve Website Build folder"),
                     "%d x %d" % (im["w"], im["h"]), b["issue"], b["need"], b["prompt"], b["source"], b["priority"]])
    for slug, h in HEADSHOTS.items():
        if h.get("missing"):
            n += 1
            rows.append([n, "team-" + slug, "(none)", "Leadership headshot (missing)", "Leadership (placeholder tile)",
                         "No photograph on evolveincorporated.com or in the Drive asset folders", "n/a", h["issue"], h["need"], h["prompt"],
                         h["source"], h["priority"]])
    n += 1
    rows.append([n, "Approved logos", "public/assets/Evolve_Logo_* and Evolve_Wordmark_*", "Logo",
                 "Header, footer, 404 (all pages)", "APPROVED - Evolve Brand Assets and Sales Materials",
                 "1688 x 673 / 1688 x 496", "None; approved flat-color files used unmodified.",
                 "SVG versions of the approved logo for crisper rendering at every size.", "No generation; request vector files from the brand owner.",
                 "Brand owner", "Low"])
    for url, name, current, need, prompt in PAGE_NEEDS:
        n += 1
        media = D.PAGE_MEDIA.get(url, {})
        if media.get("hero"):
            kind = "Evolve deck photo" if media["hero"] in BRIEFS else "imported photo"
            current = "%s '%s'%s%s" % (kind, media["hero"], (" with support image '%s'" % media["support"]) if media.get("support") else "",
                                       "" if media["hero"] in BRIEFS else " (imported 2026-09-08, license unconfirmed)")
        rows.append([n, "REPLACE WITH EVOLVE PHOTO: %s" % name, "", "Evolve-owned replacement wanted", "%s (%s)" % (name, url), "n/a", "n/a",
                     "Currently: %s" % current, need, prompt,
                     "Prefer Evolve-owned photography; the brand guideline bans stock and renders. Use generated images only as review placeholders labeled conceptual.",
                     "Medium" if "optional" in name.lower() or url == "/insights/" else "High"])
    out = ROOT / "docs" / "image-catalog.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print("Wrote %s with %d rows" % (out, len(rows)))
    if "--stdout" in sys.argv:
        print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
