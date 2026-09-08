#!/usr/bin/env python3
"""Static site generator for Evolve Data Center Solutions.

Reads the governed copy packages in content/, keeps only pages whose approval
ledger decision starts with READY, and renders a designed multi-route static
site into dist/. Standard library only.
"""
import csv
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

import data as D

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
PUBLIC = ROOT / "public"
DIST = ROOT / "dist"
ASSETS = {"css": "/css/site.css", "js": "/js/site.js"}


def fingerprint_assets():
    """Rename css/js with a content hash so browsers and CDNs never serve a stale copy."""
    for key, rel in (("css", "css/site.css"), ("js", "js/site.js")):
        src = DIST / rel
        digest = hashlib.md5(src.read_bytes()).hexdigest()[:10]
        target = src.with_name("%s.%s%s" % (src.stem, digest, src.suffix))
        src.rename(target)
        ASSETS[key] = "/" + str(target.relative_to(DIST)).replace("\\", "/")

# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def esc(s=""):
    return html.escape(str(s), quote=True)


INLINE_LINK = re.compile(r"\[([^\]]+)\]\(((?:/[^)\s]*|https?://[^)\s]+|tel:[^)\s]+|mailto:[^)\s]+))\)")


def inline(s=""):
    out = esc(s)
    out = INLINE_LINK.sub(lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)), out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def strip_md(s=""):
    s = INLINE_LINK.sub(lambda m: m.group(1), s)
    return re.sub(r"[*`]", "", s).strip()


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", strip_md(s).lower()).strip("-")
    return s or "section"


def parse_csv(text):
    return list(csv.DictReader(text.splitlines()))


# ---------------------------------------------------------------------------
# Markdown block parser
# ---------------------------------------------------------------------------
LINK_ONLY = re.compile(r"^\[([^\]]+)\]\(([^)\s]+)\)$")
STAT_LINE = re.compile(r"^\*\*[^*]+\*\*$")
LABEL_LINE = re.compile(r"^\*\*([^*:]+):\*\*\s*(.+)$")


def parse_blocks(md):
    """Return a flat list of blocks: (kind, ...) tuples."""
    blocks = []
    para = []
    lst = None
    table = []

    def flush_para():
        nonlocal para
        if para:
            blocks.append(("p", para))
            para = []

    def flush_list():
        nonlocal lst
        if lst:
            blocks.append(lst)
            lst = None

    def flush_table():
        nonlocal table
        if table:
            rows = [[c.strip() for c in row.strip("|").split("|")] for row in table]
            if len(rows) >= 2 and all(re.match(r"^:?-+:?$", c) for c in rows[1]):
                rows.pop(1)
            blocks.append(("table", rows))
            table = []

    for raw in md.strip().split("\n"):
        line = raw.rstrip("\n")
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            flush_para(); flush_list(); table.append(s); continue
        flush_table()
        if not s:
            flush_para(); flush_list(); continue
        m = re.match(r"^(#{1,6})\s+(.+)$", s)
        if m:
            flush_para(); flush_list()
            blocks.append(("h", len(m.group(1)), m.group(2).strip()))
            continue
        m = re.match(r"^[-*]\s+(.+)$", s)
        if m:
            flush_para()
            if not lst or lst[0] != "ul":
                flush_list(); lst = ("ul", [])
            lst[1].append(m.group(1).strip()); continue
        m = re.match(r"^\d+\.\s+(.+)$", s)
        if m:
            flush_para()
            if not lst or lst[0] != "ol":
                flush_list(); lst = ("ol", [])
            lst[1].append(m.group(1).strip()); continue
        flush_list()
        m = LINK_ONLY.match(s)
        if m:
            flush_para(); blocks.append(("link", m.group(1).strip(), m.group(2).strip())); continue
        if STAT_LINE.match(s):
            flush_para()
            text = s.strip("*").strip()
            blocks.append(("label-head", text.rstrip(":")) if text.endswith(":") else ("stat", text))
            continue
        m = re.match(r"^\*\*(Plan|Design|Build|Power|Maintain)\*\*\s+(.+)$", s)
        if m:
            flush_para(); blocks.append(("label", m.group(1), m.group(2).strip())); continue
        m = LABEL_LINE.match(s)
        if m:
            flush_para(); blocks.append(("label", m.group(1).strip(), m.group(2).strip())); continue
        para.append((s, line.endswith("  ")))
    flush_para(); flush_list(); flush_table()
    return blocks


def para_html(para):
    parts = []
    for text, br in para:
        parts.append(inline(text) + ("<br>" if br else " "))
    return "<p>%s</p>" % "".join(parts).strip()


def is_link_item(item):
    return bool(LINK_ONLY.match(item.strip()))


def sectionize(blocks):
    levels = [b[1] for b in blocks if b[0] == "h" and b[1] > 1]
    top = min(levels) if levels else 3
    sections = []
    cur = {"title": None, "blocks": []}
    for b in blocks:
        if b[0] == "h" and b[1] == 1:
            continue
        if b[0] == "h" and b[1] == top:
            sections.append(cur)
            title = b[2]
            cur = {"title": title[:1].upper() + title[1:], "blocks": []}
        else:
            cur["blocks"].append(b)
    sections.append(cur)
    return [s for s in sections if s["title"] or s["blocks"]], top


def split_subs(section, top):
    lead, subs = [], []
    cur = None
    for b in section["blocks"]:
        if b[0] == "h" and b[1] == top + 1:
            cur = {"title": b[2], "blocks": []}
            subs.append(cur)
        elif cur is None:
            lead.append(b)
        else:
            cur["blocks"].append(b)
    return lead, subs


# ---------------------------------------------------------------------------
# Copy extraction (page blocks from the governed packages)
# ---------------------------------------------------------------------------

def extract_pages():
    items = []
    for f in sorted(CONTENT.glob("Evolve_Copy_0*.md")):
        text = f.read_text(encoding="utf-8")
        matches = list(re.finditer(r"^# PAGE-(\d+) — ([^\n]+)$", text, re.M))
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            items.append({"id": m.group(1), "name": m.group(2).strip(), "file": f.name, "block": text[m.start():end]})
    return items


def first(pattern, text, flags=re.M):
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else None


def prepare_public_body(body, page_id):
    """Remove editorial and implementation language from public copy (QA FIX-003 lineage)."""
    out = re.sub(r"^#{2,3} (?:Final CTA|CTA)\s*$[\s\S]*$", "", body, flags=re.M)
    if page_id == "720":
        out = re.sub(r"^#### Careers\s*$[\s\S]*?(?=^#### |^### )", "", out, flags=re.M)
        out = re.sub(r"^### General inquiry form\s*$[\s\S]*$", "", out, flags=re.M)
    if page_id == "730":
        out = re.sub(r"^### Support request fields\s*$[\s\S]*?(?=^### )", "", out, flags=re.M)
    if page_id == "800":
        out = re.sub(r"^### Form fields\s*$[\s\S]*$", "", out, flags=re.M)
    if page_id == "810":
        out = re.sub(r"^### Form fields\s*$[\s\S]*?(?=^### )", "", out, flags=re.M)
    out = re.sub(r"^#{3,4} (?:How many facilities does Evolve maintain\?|Does Evolve publish a facilities-maintained count\?)\s*$[\s\S]*?(?=^#{2,4} |\Z)", "", out, flags=re.M)
    out = re.sub(r"^.*(?:should be added here only after|should remain unpublished until|Add the Careers link|Add approved maintenance children|Add Privacy Policy, Accessibility and Terms of Use links).*$", "", out, flags=re.M)
    out = re.sub(r"\s*A formal Evolve assessment offering remains gated until its deliverable is approved, but ", " ", out)
    out = re.sub(r"\s*Additional market pages remain gated until their commercial priority and supporting Evolve claims are approved\.", "", out)
    out = re.sub(r"\s*The website uses that exact approved statement and does not substitute earlier, conflicting dates\.", "", out)
    out = re.sub(r"\s*Evolve-specific density and cooling limits are not represented as universal claims\.", "", out)
    out = re.sub(r"\s*Evolve-specific rack-density and cooling limits are not approved for publication and are not asserted here\.", "", out)
    out = re.sub(r"\s*Competitor pages commonly publish detailed level taxonomies, but Evolve will not claim a standard commissioning scope until that scope is separately approved\.", "", out)
    out = re.sub(r"\s*eLERT is an Evolve monitoring offering, but its detailed public definition, coverage, integrations and service model remain under governance review\. This article does not represent those unapproved features\.", "", out)
    out = re.sub(r"\s*Dedicated power-generation, critical-infrastructure and eLERT paths should be added only after their public scopes are approved\.", "", out)
    out = re.sub(r"^No facilities-maintained number is shown because[^\n]+$", "", out, flags=re.M)
    out = out.replace("Detailed public product claims are being governed and will appear only after technical and legal approval.",
                      "Detailed product information will be published after technical and legal review.")
    out = out.replace("The correct website path begins with the decision the buyer is making—not a generic industry label.",
                      "The right starting point is the decision the buyer is making—not a generic industry label.")
    out = out.replace("Evolve capability statements remain tied to the approved claims ledger.",
                      "Evolve capability statements remain tied to reviewed company sources.")
    out = out.replace("Use this page to reach Evolve's published services, data-center markets, resources and company information. Gated or unpublished pages must not appear.",
                      "Use this page to reach Evolve's services, data-center markets, resources and company information.")
    out = out.replace("Evolve does not currently publish a facilities-maintained count or guaranteed response time.",
                      "Facility counts and response terms are not represented as universal service commitments.")
    out = out.replace("Evolve does not publish a universal rack-density range, cooling capability or performance guarantee. The technical basis must come from the approved requirements for the individual program.",
                      "Rack density, cooling capability and performance criteria must be defined for the individual program.")
    out = out.replace("Evolve does not publish a universal speed or savings claim.", "Schedule and savings outcomes depend on project conditions and scope.")
    out = out.replace("This page does not publish a standard asset list or universal interval.", "The program must reflect the actual facility rather than a universal asset list or interval.")
    out = out.replace("Does Evolve publish a standard schedule or savings claim?", "Does Evolve promise a standard schedule or savings outcome?")
    out = out.replace("Does Evolve publish a guaranteed response time?", "Does Evolve offer a standard response time?")
    out = out.replace("No general response-time promise is published. Availability, escalation and response terms must be defined in the specific service agreement.",
                      "Availability, escalation and response terms are defined in the specific service agreement.")
    out = out.replace("This form does not publish or create a guaranteed response time. Service availability, escalation and response terms are governed by the applicable agreement.",
                      "Service availability, escalation and response terms are governed by the applicable agreement.")
    out = out.replace("What proof can Evolve publish?", "What experience does Evolve bring to power work?")
    out = out.replace("The website does not imply completed work in every state.", "Nationwide service does not imply completed work in every state.")
    out = out.replace("The public eLERT page should remain unpublished until AD-003 is resolved.", "")
    out = out.replace(" Save the confirmation reference shown on this page.", "")
    out = out.replace(" Keep the confirmation reference for follow-up.", "")
    out = out.replace("Evolve will publish that figure only after the metric and reporting date are approved.", "")
    voice = [
        (r"Evolve's approved ", "Evolve's documented "),
        (r"its approved ", "its documented "),
        (r"approved public paths", "current public paths"),
        (r"approved Design & Build practice", "Design & Build practice"),
        (r"approved lifecycle", "defined lifecycle"),
        (r"approved technical basis", "defined technical basis"),
        (r"approved aggregate experience", "aggregate experience"),
        (r"approved aggregate proof", "aggregate proof"),
        (r"approved proof", "experience at a glance"),
        (r"approved capability", "documented capability"),
        (r"approved project requirements", "project requirements"),
        (r"approved requirements", "defined requirements"),
        (r"approved design basis", "current design basis"),
        (r"approved basis", "project basis"),
        (r"approved scope", "defined scope"),
        (r"approved direction", "coordinated direction"),
        (r"approved results", "accepted results"),
        (r"approved intervals", "defined intervals"),
        (r"approved load", "defined load"),
        (r"approved plan", "project plan"),
        (r"approved system basis", "defined system basis"),
    ]
    for pat, rep in voice:
        out = re.sub(pat, rep, out, flags=re.I)
    out = out.replace("defined in the defined scope", "defined in the project scope")
    return re.sub(r"\n{3,}", "\n\n", out).strip()


def parent_path(url):
    if url == "/":
        return "/"
    parts = [p for p in url.split("/") if p]
    parts.pop()
    return "/" + "/".join(parts) + "/" if parts else "/"


def page_from_block(item, ledger_row):
    block = item["block"]
    url = first(r"^\*\*URL:\*\*\s+`([^`]+)`", block)
    m = re.search(r"^## Publishable (?:page copy|article)\s*$([\s\S]*?)(?=^## Metadata recommendation\s*$)", block, re.M)
    if not url or not m:
        return None
    pub = m.group(1).strip()
    meta = first(r"^## Metadata recommendation\s*$([\s\S]*?)(?=^## Schema recommendation|^## Claim review|^---$)", block) or ""
    title = first(r"\*\*Title:\*\*\s*([^\n]+)", meta) or "%s | Evolve" % item["name"]
    description = first(r"\*\*Meta description:\*\*\s*([^\n]+)", meta) or D.SITE["description"]
    og_title = first(r"\*\*Open Graph title:\*\*\s*([^\n]+)", meta) or title
    og_description = first(r"\*\*Open Graph description:\*\*\s*([^\n]+)", meta) or description
    h1 = first(r"^#\s+(.+)$", pub) or item["name"]
    has_hero = re.search(r"^### Hero\s*$", pub, re.M) is not None
    parent_label = D.LABEL_BY_PATH.get(parent_path(url))
    eyebrow = first(r"^\*\*Eyebrow:\*\*\s*([^\n]+)", pub) or (parent_label if parent_label and parent_label != "Home" else "Evolve Data Center Solutions")
    primary = (first(r"^\*\*Primary CTA:\*\*\s*([^\n]+)", pub)
               or first(r"^\*\*Primary action:\*\*\s*([^\n]+)", block)
               or first(r"^\*\*Primary CTA:\*\*\s*([^\n]+)", block)
               or "Start a Project")
    secondary = first(r"^\*\*Secondary CTA:\*\*\s*([^\n]+)", pub)
    h1_idx = re.search(r"^#\s+", pub, re.M)
    after_h1 = re.sub(r"^#\s+[^\n]+\n+", "", pub[h1_idx.start():]) if h1_idx else pub
    im = re.match(r"^([^#\n*][^\n]*(?:\n(?!\n|#|\*\*)[^\n]+)*)", after_h1, re.M)
    raw_intro = im.group(1).replace("\n", " ").strip() if im else description
    intro = prepare_public_body(raw_intro, item["id"])

    body = pub
    body = re.sub(r"^### Hero\s*$[\s\S]*?(?=^###\s+)", "", body, count=1, flags=re.M)
    body = re.sub(r"^### Proof bar\s*$[\s\S]*?(?=^###\s+)", "", body, count=1, flags=re.M)
    body = re.sub(r"^#\s+[^\n]+\n?", "", body, count=1, flags=re.M)
    body = body.lstrip()
    if not has_hero:
        body = re.sub(r"^[^\n]+(?:\n(?!\n)[^\n]+)*\n+", "", body, count=1)
    body = re.sub(r"^\*\*Eyebrow:\*\*[^\n]+\n?", "", body, flags=re.M)
    body = re.sub(r"^\*\*(?:Primary|Secondary) CTA:\*\*[^\n]+\n?", "", body, flags=re.M)
    body = re.sub(r"^\*\*CTA:\*\*[^\n]+\n?", "", body, flags=re.M)

    final_block = first(r"^#{2,3} (?:Final CTA|CTA)\s*$([\s\S]*)$", body) or ""
    final_heading = first(r"^##\s+([^\n]+)", final_block)
    after_heading = re.sub(r"^##\s+[^\n]+\n+", "", final_block, count=1, flags=re.M) if final_heading else final_block
    inline_final = re.search(r"^\*\*([^*:]+)\*\*\s*[—-]\s*([^\n]+)", after_heading, re.M)
    final_action = (first(r"^\*\*(?:Primary )?CTA:\*\*\s*([^\n]+)", after_heading)
                    or (inline_final.group(1).strip() if inline_final else None)
                    or primary)
    final_secondary = first(r"^\*\*Secondary CTA:\*\*\s*([^\n]+)", after_heading)
    final_description = ((inline_final.group(2).strip() if inline_final else None)
                         or first(r"^([^#*\n][^\n]*)", after_heading)
                         or intro)
    body = prepare_public_body(body, item["id"])
    return {
        "id": item["id"], "name": item["name"], "file": item["file"], "url": url,
        "title": title, "description": description, "og_title": og_title, "og_description": og_description,
        "h1": h1, "eyebrow": eyebrow, "intro": intro, "body": body.strip(),
        "primary": primary, "secondary": secondary,
        "final_heading": final_heading, "final_description": final_description,
        "final_action": final_action, "final_secondary": final_secondary,
        "ledger": ledger_row,
    }


# ---------------------------------------------------------------------------
# Routing helpers
# ---------------------------------------------------------------------------

def action_href(label, page):
    v = label.lower()
    if page["id"] in D.FORM_DEFINITIONS and re.match(r"^(route|request|submit)", v):
        return "#form"
    if "support" in v:
        return "/support/"
    if v.startswith("explore") and ("service" in v or "maintenance" in v):
        return "/maintenance/"
    if v.startswith("explore") and "backup" in v:
        return "/power-generation/backup-power-systems/"
    if v.startswith("explore") and "preventive" in v:
        return "/maintenance/preventive-maintenance/"
    if v.startswith("explore") and "project types" in v:
        return "#data-center-types"
    if v.startswith("explore") and "insight" in v:
        return "/insights/"
    if "existing facility" in v:
        return "/start-a-project/?interest=expansions-retrofits"
    if "service" in v or "maintenance" in v:
        return "/request-service/"
    if "contact" in v:
        return "/contact/"
    if "insight" in v:
        return "/insights/"
    if "design & build" in v:
        return "/design-build/"
    if "compare delivery" in v:
        return "/insights/modular-vs-traditional-data-center-delivery/"
    if "review ai infrastructure" in v:
        return "/insights/ai-data-center-infrastructure-planning/"
    if "review planning" in v:
        return "/design-build/planning-feasibility/"
    interest = None
    for key, val in [("modular", "modular-data-centers"), ("hyperscale", "hyperscale-data-centers"), ("ai data", "ai-data-centers"),
                     ("backup", "power-generation"), ("power", "power-generation"), ("planning", "planning-feasibility"),
                     ("commission", "commissioning"), ("construction", "data-center-construction"),
                     ("colocation", "colocation"), ("enterprise", "enterprise"), ("technical requirements", "ai-data-centers"),
                     ("distributed", "edge"), ("project brief", "design-build")]:
        if key in v:
            interest = val
            break
    return "/start-a-project/?interest=%s" % interest if interest else "/start-a-project/"


def breadcrumbs(url):
    if url == "/":
        return []
    crumbs = [("Home", "/")]
    current = ""
    for part in [p for p in url.split("/") if p]:
        current += "/" + part
        href = current + "/"
        crumbs.append((D.LABEL_BY_PATH.get(href, part.replace("-", " ").title()), href))
    return crumbs


def stage_set(url):
    if url in D.STAGES_BY_PATH:
        return D.STAGES_BY_PATH[url]
    if url.startswith("/data-center-markets/") or url == "/" or url == "/about/":
        return D.LIFECYCLE
    return []


# ---------------------------------------------------------------------------
# Image helpers
# ---------------------------------------------------------------------------

def img_tag(key, sizes, cls="", eager=False, alt=None):
    im = D.IMAGES[key]
    widths = im["widths"]
    largest = widths[0]
    srcset = ", ".join("/img/%s-%d.jpg %dw" % (im["file"], w, w) for w in widths)
    src = "/img/%s-%d.jpg" % (im["file"], widths[min(1, len(widths) - 1)])
    height = round(largest * im["h"] / im["w"])
    attrs = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    return ('<img src="%s" srcset="%s" sizes="%s" width="%d" height="%d" alt="%s"%s%s>'
            % (src, srcset, sizes, largest, height, esc(im["alt"] if alt is None else alt), attrs,
               ' class="%s"' % cls if cls else ""))


def tech_panel(url):
    active = set(stage_set(url))
    items = "".join('<li%s><span class="tech-num">%02d</span><span class="tech-label">%s</span></li>'
                    % (' class="is-active"' if s in active else "", i + 1, s) for i, s in enumerate(D.LIFECYCLE))
    return ('<div class="tech-panel" aria-hidden="true"><ol class="tech-stages">%s</ol>'
            '<p class="tech-mark">Plan. Design. Build. Power. Maintain.</p></div>' % items)


def mosaic(keys):
    return '<div class="mosaic">%s</div>' % "".join(
        '<figure class="mosaic-tile">%s</figure>' % img_tag(k, "(min-width: 80rem) 20rem, (min-width: 48rem) 22vw, 45vw") for k in keys)


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------

def nav_markup(current_url):
    out = []
    for i, item in enumerate(D.NAVIGATION):
        is_section = current_url != "/" and current_url.startswith(item["href"])
        cur_attr = ' aria-current="page"' if current_url == item["href"] else ""
        cls = "nav-item" + (" has-menu" if item.get("groups") else "") + (" is-section" if is_section else "")
        if item.get("groups"):
            groups = "".join(
                '<div class="mega-group"><p class="mega-label">%s</p><ul>%s</ul></div>' % (
                    esc(g["label"]),
                    "".join('<li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == current_url else "", esc(l)) for l, h in g["links"]))
                for g in item["groups"])
            cta = ''
            if item.get("cta"):
                cta = '<div class="mega-cta"><p class="mega-label">Next step</p><a class="button button-primary" href="%s">%s</a></div>' % (item["cta"][1], esc(item["cta"][0]))
            out.append(
                '<li class="%s"><div class="nav-trigger"><a class="nav-link" href="%s"%s>%s</a>'
                '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu-%d"><span class="sr-only">Open %s menu</span></button></div>'
                '<div class="mega" id="menu-%d"><div class="shell mega-inner">%s%s</div></div></li>'
                % (cls, item["href"], cur_attr, esc(item["label"]), i, esc(item["label"]), i, groups, cta))
        else:
            out.append('<li class="%s"><a class="nav-link" href="%s"%s>%s</a></li>' % (cls, item["href"], cur_attr, esc(item["label"])))
    return "".join(out)


def header_markup(url):
    s = D.SITE
    return (
        '<a class="skip-link" href="#main">Skip to main content</a>'
        '<header class="site-header">'
        '<div class="utility"><div class="shell utility-inner">'
        '<a class="utility-phone" href="tel:%s"><svg aria-hidden="true" viewBox="0 0 24 24" width="14" height="14"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25c1.1.37 2.3.57 3.6.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1L6.6 10.8z"/></svg>%s</a>'
        '<nav class="utility-nav" aria-label="Utility"><a href="/contact/">Contact</a><a href="/support/">Support</a></nav>'
        '</div></div>'
        '<div class="masthead"><div class="shell masthead-inner">'
        '<a class="brand" href="/" aria-label="Evolve Data Center Solutions home"><img class="brand-full" src="/assets/evolve-logo-white-440.png" width="440" height="175" alt="Evolve Data Center Solutions"><img class="brand-mark" src="/assets/evolve-wordmark-white-360.png" width="360" height="106" alt="Evolve"></a>'
        '<button class="menu-button" type="button" aria-expanded="false" aria-controls="primary-nav"><span class="menu-bars" aria-hidden="true"><i></i><i></i><i></i></span><span class="menu-label">Menu</span></button>'
        '<nav id="primary-nav" class="primary-nav" aria-label="Primary"><ul class="nav-list">%s</ul>'
        '<div class="nav-actions"><a class="button button-primary nav-cta" href="/start-a-project/">Start a Project</a>'
        '<a class="nav-phone" href="tel:%s">%s</a></div></nav>'
        '<a class="button button-primary masthead-cta" href="/start-a-project/">Start a Project</a>'
        '</div></div></header>'
        % (s["phone_href"], esc(s["phone_display"]), nav_markup(url), s["phone_href"], esc(s["phone_display"]))
    )


def footer_markup():
    s = D.SITE
    groups = "".join(
        '<nav class="footer-col" aria-label="%s"><h2>%s</h2><ul>%s</ul></nav>' % (
            esc(g["label"]), esc(g["label"]), "".join('<li><a href="%s">%s</a></li>' % (h, esc(l)) for l, h in g["links"]))
        for g in D.FOOTER_GROUPS)
    note = ("<p class=\"footer-review\">Review build %s. Not for publication. Copy package %s under %s." % (D.BUILD_DATE, esc(s["content_version"]), esc(s["governance_version"]))
            if D.REVIEW_BUILD else "")
    return (
        '<footer class="site-footer"><div class="shell footer-grid">'
        '<div class="footer-brand"><img src="/assets/evolve-logo-white-440.png" width="440" height="175" loading="lazy" alt="Evolve Data Center Solutions">'
        '<p class="footer-tag">%s</p><p class="footer-desc">Data-center planning, design, construction, power, monitoring and maintenance.</p>'
        '<address>%s<br><a href="tel:%s">%s</a></address></div>%s</div>'
        '<div class="shell footer-base"><p>&copy; 2026 Evolve Data Center Solutions. Founded in 2004 and headquartered in Houston, Texas.</p>'
        '<ul class="footer-legal"><li><a href="/sitemap/">Sitemap</a></li><li><a href="/contact/">Contact</a></li><li><a href="/support/">Support</a></li></ul>%s</div></footer>'
        % (esc(s["tagline"]), "<br>".join(esc(l) for l in s["address_lines"]), s["phone_href"], esc(s["phone_display"]), groups, note)
    )


def proof_markup(page_id):
    ids = D.PROOF_BY_PAGE.get(page_id, [])
    if not ids:
        return ""
    items = "".join('<div class="proof-item" data-claim-id="%s"><strong>%s</strong><span>%s</span></div>'
                    % (cid, esc(D.CLAIMS[cid]["value"]), esc(D.CLAIMS[cid]["label"])) for cid in ids)
    return '<section class="proof" aria-label="Evolve experience"><div class="shell proof-grid proof-%d">%s</div></section>' % (len(ids), items)


def hero_markup(page):
    url = page["url"]
    media = D.PAGE_MEDIA.get(url, {})
    crumbs = breadcrumbs(url)
    crumb_html = ""
    if crumbs:
        crumb_html = '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>%s</ol></nav>' % "".join(
            '<li>%s</li>' % ('<span aria-current="page">%s</span>' % esc(l) if i == len(crumbs) - 1 else '<a href="%s">%s</a>' % (h, esc(l)))
            for i, (l, h) in enumerate(crumbs))
    eyebrow = page["eyebrow"]
    if url in D.INSIGHT_PATHS:
        eyebrow = "Insight · %s" % D.INSIGHT_TOPICS.get(url, "Technical guidance")
    actions = '<a class="button button-primary" href="%s">%s</a>' % (action_href(page["primary"], page), esc(page["primary"]))
    if page.get("secondary"):
        actions += '<a class="button button-inverse" href="%s">%s</a>' % (action_href(page["secondary"], page), esc(page["secondary"]))
    text = ('%s<p class="eyebrow">%s</p><h1>%s</h1><p class="lead">%s</p><div class="actions">%s</div>'
            % (crumb_html, esc(eyebrow), esc(page["h1"]), inline(page["intro"]), actions))
    if media.get("hero_style") == "full" and media.get("hero"):
        return ('<section class="hero hero-full"><div class="hero-media">%s</div><div class="hero-scrim" aria-hidden="true"></div>'
                '<div class="shell hero-content">%s</div>'
                '<div class="hero-strapline" aria-hidden="true"><span>Plan</span><span>Design</span><span>Build</span><span>Power</span><span>Maintain</span></div></section>'
                % (img_tag(media["hero"], "100vw", eager=True), text))
    if media.get("hero"):
        visual = '<figure class="hero-figure">%s</figure>' % img_tag(media["hero"], "(min-width: 80rem) 40rem, (min-width: 48rem) 48vw, 100vw", eager=True)
    elif media.get("mosaic"):
        visual = mosaic(media["mosaic"])
    else:
        visual = tech_panel(url)
    compact = " hero-compact" if url in D.INSIGHT_PATHS or page["id"] in D.FORM_DEFINITIONS or url in ("/thank-you/", "/sitemap/", "/insights/") else ""
    return ('<section class="hero hero-split%s"><div class="shell hero-split-inner"><div class="hero-text">%s</div><div class="hero-visual">%s</div></div></section>'
            % (compact, text, visual))


def links_grid(links, title=None, tone="light"):
    tiles = "".join('<li><a href="%s">%s<span class="arrow" aria-hidden="true"></span></a></li>' % (h, esc(re.sub(r"^Explore ", "", l))) for l, h in links)
    return '<ul class="link-grid">%s</ul>' % tiles


def collect_links(blocks):
    links = []
    for b in blocks:
        if b[0] == "link":
            links.append((b[1], b[2]))
        elif b[0] in ("ul", "ol"):
            for item in b[1]:
                m = LINK_ONLY.match(item.strip())
                if m:
                    links.append((m.group(1), m.group(2)))
    return links


def blocks_html(blocks, skip_links=False):
    out = []
    for b in blocks:
        k = b[0]
        if k == "p":
            out.append(para_html(b[1]))
        elif k == "h":
            lvl = min(6, max(3, b[1]))
            out.append("<h%d>%s</h%d>" % (lvl, inline(b[2]), lvl))
        elif k in ("ul", "ol"):
            out.append("<%s>%s</%s>" % (k, "".join("<li>%s</li>" % inline(i) for i in b[1]), k))
        elif k == "table":
            rows = b[1]
            head = "".join("<th scope=\"col\">%s</th>" % inline(c) for c in rows[0])
            body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in rows[1:])
            out.append('<div class="table-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (head, body))
        elif k == "link":
            if not skip_links:
                out.append('<p class="arrow-link"><a href="%s">%s<span class="arrow" aria-hidden="true"></span></a></p>' % (b[2], esc(b[1])))
        elif k == "stat":
            out.append('<p class="stat-inline">%s</p>' % inline(b[1]))
        elif k == "label":
            out.append("<p><strong>%s:</strong> %s</p>" % (inline(b[1]), inline(b[2])))
        elif k == "label-head":
            out.append('<p class="copy-label">%s</p>' % inline(b[1]))
    return "".join(out)


def section_head(title, lead_blocks, wide=False):
    if not title and not lead_blocks:
        return ""
    lead = "".join(para_html(b[1]) for b in lead_blocks if b[0] == "p")
    return '<div class="section-head%s">%s%s</div>' % (" section-head-wide" if wide else "", "<h2>%s</h2>" % inline(title) if title else "", lead)


def render_cards(sec, top, page):
    lead, subs = split_subs(sec, top)
    cards = []
    for sub in subs:
        links = collect_links(sub["blocks"])
        href = links[0][1] if links else None
        label = re.sub(r"^Explore ", "", links[0][0]) if links else None
        img_key = D.CARD_IMAGES.get(href) if href else None
        body_blocks = [b for b in sub["blocks"] if b[0] != "link"]
        list_of_links = any(b[0] in ("ul", "ol") and all(is_link_item(i) for i in b[1]) for b in body_blocks)
        media = '<div class="card-media">%s</div>' % img_tag(img_key, "(min-width: 80rem) 26rem, (min-width: 48rem) 45vw, 100vw") if img_key else ""
        if list_of_links:
            inner = '<div class="card-body"><h3>%s</h3><ul class="card-list">%s</ul></div>' % (
                inline(sub["title"]), "".join('<li><a href="%s">%s</a></li>' % (h, esc(l)) for l, h in links))
            cards.append('<div class="card card-static">%s%s</div>' % (media, inner))
        elif href:
            inner = '<div class="card-body"><h3>%s</h3>%s<span class="card-cta">%s<span class="arrow" aria-hidden="true"></span></span></div>' % (
                inline(sub["title"]), blocks_html(body_blocks, skip_links=True), esc(label))
            cards.append('<a class="card" href="%s">%s%s</a>' % (href, media, inner))
        else:
            inner = '<div class="card-body"><h3>%s</h3>%s</div>' % (inline(sub["title"]), blocks_html(body_blocks))
            cards.append('<div class="card card-static">%s%s</div>' % (media, inner))
    n = len(subs)
    cols = "cards-2" if n in (2, 4) else "cards-3"
    has_media = any('card-media' in c for c in cards)
    return section_head(sec["title"], lead) + '<div class="cards %s%s">%s</div>' % (cols, " cards-media" if has_media else "", "".join(cards))


def render_insight_cards(sec, top, page, pages_by_url):
    lead, subs = split_subs(sec, top)
    cards = []
    for sub in subs:
        for label, href in collect_links(sub["blocks"]):
            p = pages_by_url.get(href)
            if not p:
                continue
            img_key = D.CARD_IMAGES.get(href)
            media = '<div class="card-media">%s</div>' % img_tag(img_key, "(min-width: 80rem) 26rem, (min-width: 48rem) 45vw, 100vw") if img_key else ""
            cards.append('<a class="card card-insight" href="%s">%s<div class="card-body"><p class="eyebrow">%s</p><h3>%s</h3><p>%s</p><span class="card-cta">Read the guide<span class="arrow" aria-hidden="true"></span></span></div></a>'
                         % (href, media, esc(sub["title"]), esc(p["name"]), esc(p["description"])))
    return section_head(sec["title"], lead) + '<div class="cards cards-3 cards-media">%s</div>' % "".join(cards)


def render_steps(sec, top, page):
    lead, subs = split_subs(sec, top)
    items = "".join('<li><span class="step-num" aria-hidden="true">%02d</span><div class="step-body"><h3>%s</h3>%s</div></li>'
                    % (i + 1, inline(re.sub(r"^\d+\.\s*", "", s["title"])), blocks_html(s["blocks"])) for i, s in enumerate(subs))
    return section_head(sec["title"], lead) + '<ol class="steps">%s</ol>' % items


def render_points(sec, top, page):
    lead, subs = split_subs(sec, top)
    items = "".join('<div class="point"><span class="point-num" aria-hidden="true">%02d</span><h3>%s</h3>%s</div>'
                    % (i + 1, inline(s["title"]), blocks_html(s["blocks"])) for i, s in enumerate(subs))
    return section_head(sec["title"], lead) + '<div class="points">%s</div>' % items


def render_faq(sec, top, page):
    lead, subs = split_subs(sec, top)
    items = "".join('<details class="faq-item"><summary><h3>%s</h3><span class="faq-icon" aria-hidden="true"></span></summary><div class="faq-answer">%s</div></details>'
                    % (inline(s["title"]), blocks_html(s["blocks"])) for s in subs)
    return '<div class="faq-layout">%s<div class="faq">%s</div></div>' % (section_head(sec["title"] or "Direct answers", lead), items)


def render_lifecycle(sec, top, page, from_labels=False):
    lead, subs = split_subs(sec, top)
    stages = []
    if from_labels:
        for b in lead:
            if b[0] == "label":
                stages.append((b[1], b[2], D.LIFECYCLE_LINKS.get(b[1])))
        lead = [b for b in lead if b[0] != "label"]
    else:
        for s in subs:
            links = collect_links(s["blocks"])
            paras = "".join(para_html(b[1]) for b in s["blocks"] if b[0] == "p")
            stages.append((s["title"], paras, links[0][1] if links else None))
    items = []
    for i, (name, text, href) in enumerate(stages):
        body = text if text.startswith("<p>") else "<p>%s</p>" % inline(text)
        link = '<a class="stage-link" href="%s">Explore<span class="arrow" aria-hidden="true"></span></a>' % href if href else ""
        items.append('<li class="stage"><span class="stage-num">%02d</span><h3>%s</h3>%s%s</li>' % (i + 1, esc(name), body, link))
    return section_head(sec["title"], lead) + '<ol class="lifecycle">%s</ol>' % "".join(items)


def render_callout(sec, top, page):
    lead, subs = split_subs(sec, top)
    stats = [b for b in lead if b[0] == "stat"]
    rest = [b for b in lead if b[0] != "stat"]
    stat_html = ""
    if stats:
        stat_html = '<div class="stat-row">%s</div>' % "".join('<div class="stat"><strong>%s</strong></div>' % inline(b[1]) for b in stats)
    body = blocks_html(rest)
    title = sec["title"]
    return '<div class="callout-inner">%s%s<div class="callout-body">%s</div></div>' % ("<h2>%s</h2>" % inline(title) if title else "", stat_html, body)


def render_split(sec, top, page, img_key):
    lead, subs = split_subs(sec, top)
    links = collect_links(lead)
    body = blocks_html([b for b in lead if b[0] != "link"])
    button = '<a class="button button-primary" href="%s">%s</a>' % (links[0][1], esc(links[0][0])) if links else ""
    return ('<div class="split-inner"><div class="split-text"><h2>%s</h2>%s%s</div><div class="split-media"><figure>%s</figure></div></div>'
            % (inline(sec["title"]), body, button, img_tag(img_key, "(min-width: 80rem) 36rem, (min-width: 48rem) 48vw, 100vw")))


def render_support(sec, top, page, img_key):
    """First prose section with a supporting photograph beside it."""
    lead, subs = split_subs(sec, top)
    inner = blocks_html(lead)
    for s in subs:
        inner += "<h3>%s</h3>%s" % (inline(s["title"]), blocks_html(s["blocks"]))
    return ('<div class="split-inner split-light"><div class="split-text prose"><h2>%s</h2>%s</div>'
            '<div class="split-media"><figure>%s</figure></div></div>'
            % (inline(sec["title"]), inner, img_tag(img_key, "(min-width: 80rem) 36rem, (min-width: 48rem) 48vw, 100vw")))


def render_fit(sec, top, page):
    lead, subs = split_subs(sec, top)
    links = collect_links(lead)
    body = blocks_html([b for b in lead if b[0] != "link"])
    buttons = "".join('<a class="button button-secondary" href="%s">%s</a>' % (h, esc(l)) for l, h in links)
    return '<div class="fit"><h2>%s</h2>%s<div class="actions">%s</div></div>' % (inline(sec["title"]), body, buttons)


def render_address(sec, top, page):
    s = D.SITE
    return ('<div class="address-card"><h2>%s</h2><address><strong>%s</strong><br>%s<br><a href="tel:%s">%s</a></address>'
            '<p class="address-note">Founded in 2004. Serving a nationwide market from Houston, Texas.</p></div>'
            % (inline(sec["title"]), esc(s["name"]), "<br>".join(esc(l) for l in s["address_lines"]), s["phone_href"], esc(s["phone_display"])))


def render_links(sec, top, page):
    lead, subs = split_subs(sec, top)
    links = collect_links(lead)
    extra = "".join(para_html(b[1]) for b in lead if b[0] == "p")
    return section_head(sec["title"], []) + extra + links_grid(links)


def render_prose(sec, top, page):
    lead, subs = split_subs(sec, top)
    inner = blocks_html(lead)
    for s in subs:
        inner += "<h3>%s</h3>%s" % (inline(s["title"]), blocks_html(s["blocks"]))
    return '<div class="prose">%s%s</div>' % ("<h2>%s</h2>" % inline(sec["title"]) if sec["title"] else "", inner)


LINK_DESC = re.compile(r"^\[([^\]]+)\]\(([^)\s]+)\)\s*[\u2014\u2013-]\s*(.+)$")


def link_desc_list(blocks):
    for b in blocks:
        if b[0] == "ul" and b[1] and all(LINK_DESC.match(i.strip()) for i in b[1]):
            return b
    return None


def render_linkcards(sec, top, page):
    lead, subs = split_subs(sec, top)
    lst = link_desc_list(lead)
    rest = [b for b in lead if b is not lst]
    cards = []
    for item in lst[1]:
        m = LINK_DESC.match(item.strip())
        label, href, desc = m.group(1), m.group(2), m.group(3)
        img_key = D.CARD_IMAGES.get(href)
        media = '<div class="card-media">%s</div>' % img_tag(img_key, "(min-width: 80rem) 26rem, (min-width: 48rem) 45vw, 100vw") if img_key else ""
        cards.append('<a class="card" href="%s">%s<div class="card-body"><h3>%s</h3><p>%s</p><span class="card-cta">Explore<span class="arrow" aria-hidden="true"></span></span></div></a>'
                     % (href, media, inline(label), inline(desc[:1].upper() + desc[1:])))
    cols = "cards-2" if len(cards) in (2, 4) else "cards-3"
    return section_head(sec["title"], rest) + '<div class="cards %s cards-media">%s</div>' % (cols, "".join(cards))


def classify(sec, top, page):
    title = (sec["title"] or "").strip()
    t = title.lower().rstrip(".")
    lead, subs = split_subs(sec, top)
    sub_titles = [s["title"] for s in subs]
    media = D.PAGE_MEDIA.get(page["url"], {})
    if title in media.get("bands", {}):
        return "split"
    if not title:
        return "prose"
    if not subs and link_desc_list(lead):
        return "linkcards"
    if t.startswith("direct answers"):
        return "faq"
    if t == "contact information":
        return "address"
    if t.startswith("where evolve fits"):
        return "fit"
    if page["url"] == "/insights/" and t == "featured topics":
        return "insight-cards"
    if sub_titles == D.LIFECYCLE:
        return "lifecycle"
    labels = [b[1] for b in lead if b[0] == "label"]
    if labels == D.LIFECYCLE:
        return "lifecycle-labels"
    stats = [b for b in lead if b[0] == "stat"]
    if t in D.CALLOUT_TITLES or (stats and not subs):
        return "callout"
    if not subs:
        links = collect_links(lead)
        non_link = [b for b in lead if b[0] not in ("link",) and not (b[0] in ("ul", "ol") and all(is_link_item(i) for i in b[1]))]
        if links and all(b[0] != "p" for b in non_link) and (t.startswith("related") or t.startswith("relevant") or t.startswith("where existing") or not non_link):
            return "links"
        return "prose"
    has_links = any(collect_links(s["blocks"]) for s in subs)
    if has_links:
        return "cards"
    numbered = all(re.match(r"^\d+\.\s", s) for s in sub_titles)
    if numbered or re.search(r"approach|sequence|process|framework|structure|path$|lifecycle|decision sequence|change process", t):
        return "steps"
    return "points"


def render_sections(page, pages_by_url):
    blocks = parse_blocks(page["body"])
    sections, top = sectionize(blocks)
    media = D.PAGE_MEDIA.get(page["url"], {})
    out = []
    tone = "white"
    strip_done = False
    prose_count = 0
    for idx, sec in enumerate(sections):
        kind = classify(sec, top, page)
        anchor = ' id="%s"' % ("data-center-types" if (sec["title"] or "").lower().startswith("data-center types") else slug(sec["title"] or "section-%d" % idx))
        if kind in ("callout", "split"):
            if kind == "split":
                inner = render_split(sec, top, page, media["bands"][sec["title"]])
                out.append('<section class="band band-dark split"%s><div class="shell">%s</div></section>' % (anchor, inner))
            else:
                out.append('<section class="band band-dark callout"%s><div class="shell">%s</div></section>' % (anchor, render_callout(sec, top, page)))
            tone = "white"
            continue
        if kind == "faq":
            inner = render_faq(sec, top, page)
        elif kind == "cards":
            inner = render_cards(sec, top, page)
        elif kind == "linkcards":
            inner = render_linkcards(sec, top, page)
        elif kind == "insight-cards":
            inner = render_insight_cards(sec, top, page, pages_by_url)
        elif kind == "steps":
            inner = render_steps(sec, top, page)
        elif kind == "points":
            inner = render_points(sec, top, page)
        elif kind == "lifecycle":
            inner = render_lifecycle(sec, top, page)
        elif kind == "lifecycle-labels":
            inner = render_lifecycle(sec, top, page, from_labels=True)
        elif kind == "fit":
            inner = render_fit(sec, top, page)
        elif kind == "address":
            inner = render_address(sec, top, page)
        elif kind == "links":
            inner = render_links(sec, top, page)
        elif media.get("support") and prose_count == 0 and sec["title"]:
            inner = render_support(sec, top, page, media["support"])
            kind = "support"
            prose_count += 1
        else:
            inner = render_prose(sec, top, page)
            prose_count += 1
        band = "band-fog" if tone == "fog" else "band-white"
        out.append('<section class="band %s kind-%s"%s><div class="shell">%s</div></section>' % (band, kind, anchor, inner))
        tone = "fog" if tone == "white" else "white"
        if media.get("strip") and not strip_done and kind in ("prose", "support") and prose_count == 1:
            out.append(photo_strip(media["strip"]))
            strip_done = True
    return "".join(out)


def photo_strip(keys):
    figs = "".join('<figure class="strip-tile">%s</figure>' % img_tag(k, "(min-width: 80rem) 19rem, (min-width: 48rem) 24vw, 48vw") for k in keys)
    return ('<section class="band band-strip" aria-label="Field photographs"><div class="shell"><p class="eyebrow">Field photographs</p>'
            '<div class="strip-grid">%s</div><p class="strip-note">Evolve fabrication, delivery and installation work. Customer and project identities are not published.</p></div></section>' % figs)


def form_markup(page):
    f = D.FORM_DEFINITIONS.get(page["id"])
    if not f:
        return ""

    def field(x):
        req = " required" if x.get("required") else ""
        ac = ' autocomplete="%s"' % x["autocomplete"] if x.get("autocomplete") else ""
        fid = "%s-%s" % (f["id"], x["id"])
        label = '<label for="%s">%s%s</label>' % (fid, esc(x["label"]), "" if x.get("required") else ' <span class="optional">(optional)</span>')
        if x["type"] == "textarea":
            control = '<textarea id="%s" name="%s" rows="5"%s></textarea>' % (fid, x["id"], req)
        elif x["type"] == "select":
            control = '<select id="%s" name="%s"%s><option value="">Select one</option>%s</select>' % (
                fid, x["id"], req, "".join("<option>%s</option>" % esc(o) for o in x["options"]))
        else:
            control = '<input type="%s" id="%s" name="%s"%s%s>' % (x["type"], fid, x["id"], ac, req)
        return '<div class="field%s">%s%s</div>' % (" field-wide" if x.get("wide") else "", label, control)

    review_note = ('<p class="form-note form-note-review"><strong>Review environment:</strong> submissions are captured in the Netlify dashboard for testing and are not routed to Evolve.</p>'
                   if D.REVIEW_BUILD else "")
    return (
        '<section class="band band-fog form-band" id="form" aria-labelledby="form-title"><div class="shell form-layout">'
        '<div class="form-intro"><p class="eyebrow">%s</p><h2 id="form-title">%s</h2><p>%s</p>'
        '<p class="form-note">All fields are required unless marked optional. Do not submit passwords, access credentials or confidential technical files.</p>%s</div>'
        '<form class="form" name="%s" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="bot-field">'
        '<input type="hidden" name="form-name" value="%s"><input type="hidden" name="source-page" value="%s">'
        '<p class="hidden-field"><label>Leave this field empty <input name="bot-field"></label></p>'
        '<div class="form-grid">%s</div>'
        '<div class="form-actions"><button class="button button-primary" type="submit">%s</button>'
        '<p class="form-micro">Submission begins a qualification discussion. It does not create a contract, schedule commitment, response guarantee or confidentiality agreement.</p></div>'
        '</form></div></section>'
        % (esc(f["eyebrow"]), esc(f["title"]), esc(f["intro"]), review_note, f["id"], f["id"], page["url"], "".join(field(x) for x in f["fields"]), esc(f["submit"]))
    )


def provenance_markup(page):
    if page["url"] not in D.INSIGHT_PATHS:
        return ""
    sources = D.INSIGHT_SOURCES.get(page["url"], [])
    src = ""
    if sources:
        src = "<h2>Sources</h2><ul>%s</ul>" % "".join('<li><a href="%s" rel="noopener">%s</a> <span>(%s)</span></li>' % (u, esc(t), esc(d)) for t, u, d in sources)
    return ('<section class="band band-white"><div class="shell"><aside class="provenance" aria-label="Article provenance">'
            '<p><strong>Prepared by Evolve Data Center Solutions.</strong> Market sources retrieved September 7, 2026. Market facts are attributed to their sources and are not Evolve performance claims.</p>%s</aside></div></section>' % src)


def closing_markup(page):
    if page["id"] in D.FORM_DEFINITIONS or page["url"] in ("/thank-you/", "/sitemap/"):
        return ""
    heading = page.get("final_heading") or page["final_action"]
    secondary = page.get("final_secondary")
    buttons = '<a class="button button-primary" href="%s">%s</a>' % (action_href(page["final_action"], page), esc(page["final_action"]))
    if secondary:
        buttons += '<a class="button button-inverse" href="%s">%s</a>' % (action_href(secondary, page), esc(secondary))
    elif page["url"] != "/contact/":
        buttons += '<a class="button button-inverse" href="/contact/">Contact Evolve</a>'
    return ('<section class="band closing"><div class="shell closing-inner"><div class="closing-text"><p class="eyebrow">Next step</p><h2>%s</h2><p>%s</p></div>'
            '<div class="closing-actions">%s</div></div></section>' % (esc(heading), inline(page["final_description"]), buttons))


def schema_for(page):
    base = D.SITE["base_url"]
    url = page["url"]
    if url == "/contact/":
        ptype = "ContactPage"
    elif url == "/about/":
        ptype = "AboutPage"
    elif url in ("/sitemap/", "/insights/", "/data-center-markets/", "/solutions/"):
        ptype = "CollectionPage"
    else:
        ptype = "WebPage"
    graph = [{"@type": ptype, "@id": base + url + "#webpage", "url": base + url, "name": page["title"],
              "description": page["description"], "isPartOf": {"@id": base + "/#website"}}]
    if url == "/":
        graph.append({"@type": "WebSite", "@id": base + "/#website", "url": base + "/", "name": D.SITE["name"], "publisher": {"@id": base + "/#organization"}})
    if url in ("/", "/about/", "/contact/"):
        graph.append({"@type": "Organization", "@id": base + "/#organization", "name": D.SITE["name"], "url": base,
                      "logo": base + "/assets/Evolve_Logo_Full_Black_RedE.png", "telephone": D.SITE["phone_href"], "foundingDate": "2004",
                      "address": {"@type": "PostalAddress", "streetAddress": "10555 Cossey Road", "addressLocality": "Houston", "addressRegion": "TX", "postalCode": "77070", "addressCountry": "US"}})
    if re.match(r"^/(design-build|power-generation|maintenance|data-center-markets|solutions)/.+", url) or url in ("/design-build/", "/power-generation/", "/maintenance/"):
        graph.append({"@type": "Service", "name": page["h1"], "description": page["description"], "provider": {"@id": base + "/#organization"},
                      "areaServed": {"@type": "Country", "name": "United States"}})
    bc = breadcrumbs(url)
    if bc:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": base + href} for i, (name, href) in enumerate(bc)]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}).replace("<", "\\u003c")


FONTS = "https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;0,900;1,800&family=Barlow:wght@400;500;600;700&display=swap"


def head_markup(page, robots):
    base = D.SITE["base_url"]
    og_type = "article" if page["url"] in D.INSIGHT_PATHS else "website"
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>%s</title>\n<meta name="description" content="%s">\n<meta name="robots" content="%s">\n'
        '<link rel="canonical" href="%s%s">\n'
        '<meta property="og:type" content="%s"><meta property="og:site_name" content="%s"><meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s%s"><meta property="og:image" content="%s/img/og-evolve.jpg"><meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="theme-color" content="#0B0D0F">\n'
        '<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png"><link rel="icon" type="image/png" sizes="64x64" href="/assets/favicon-64.png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="%s">\n<link rel="stylesheet" href="%s">\n'
        '<script type="application/ld+json">%s</script>\n<script src="%s" defer></script>\n</head>\n'
        % (esc(page["title"]), esc(page["description"]), robots, base, page["url"], og_type, esc(D.SITE["name"]), esc(page["og_title"]),
           esc(page["og_description"]), base, page["url"], base, FONTS, ASSETS["css"], schema_for(page), ASSETS["js"])
    )


def page_html(page, pages_by_url):
    url = page["url"]
    if D.REVIEW_BUILD:
        robots = "noindex,nofollow" if url == "/thank-you/" else "noindex,follow"
    else:
        robots = "noindex,nofollow" if url == "/thank-you/" else ("noindex,follow" if url in D.NOINDEX_PATHS else "index,follow")
    review_pill = '<div class="review-pill" role="note"><span class="dot" aria-hidden="true"></span>Review build · %s</div>' % D.BUILD_DATE if D.REVIEW_BUILD else ""
    body_class = "page-%s" % page["id"] + (" page-insight" if url in D.INSIGHT_PATHS else "") + (" page-home" if url == "/" else "")
    return (
        head_markup(page, robots)
        + '<body class="%s" data-page="%s">\n' % (body_class, page["id"])
        + header_markup(url)
        + '<main id="main">'
        + hero_markup(page)
        + proof_markup(page["id"])
        + render_sections(page, pages_by_url)
        + provenance_markup(page)
        + form_markup(page)
        + closing_markup(page)
        + "</main>"
        + footer_markup()
        + review_pill
        + "\n</body>\n</html>\n"
    )


def not_found_html():
    review = "noindex"
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="%s">'
        '<title>Page Not Found | Evolve</title><link rel="stylesheet" href="%s"><link rel="stylesheet" href="%s"><script src="%s" defer></script></head>'
        '<body class="page-404">%s<main id="main"><section class="hero hero-split hero-compact"><div class="shell hero-split-inner"><div class="hero-text"><p class="eyebrow">Error 404</p><h1>This page is not available.</h1>'
        '<p class="lead">The address may have changed or the page may have been removed. Use the paths below to continue.</p>'
        '<div class="actions"><a class="button button-primary" href="/">Return Home</a><a class="button button-inverse" href="/sitemap/">Website Sitemap</a></div></div><div class="hero-visual">%s</div></div></section>'
        '<section class="band band-white"><div class="shell"><ul class="link-grid">%s</ul></div></section></main>%s</body></html>'
        % (review, FONTS, ASSETS["css"], ASSETS["js"], header_markup("/404/"), tech_panel("/404/"),
           "".join('<li><a href="%s">%s<span class="arrow" aria-hidden="true"></span></a></li>' % (h, l) for l, h in [
               ("Design &amp; Build", "/design-build/"), ("Power Generation", "/power-generation/"), ("Service &amp; Maintenance", "/maintenance/"),
               ("Data Center Markets", "/data-center-markets/"), ("Insights", "/insights/"), ("Contact Evolve", "/contact/")]),
           footer_markup())
    )


def write_route(url, content):
    target = DIST / "index.html" if url == "/" else DIST / url.strip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def redirect_stub(to):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=%s">'
            '<link rel="canonical" href="%s%s"><title>Redirecting | Evolve</title></head><body><p>This page has moved to <a href="%s">%s</a>.</p></body></html>'
            % (to, D.SITE["base_url"], to, to, to))


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(PUBLIC, DIST)
    fingerprint_assets()
    ledger = parse_csv((CONTENT / "Evolve_Copy_Approval_Ledger_2026-09-07.csv").read_text(encoding="utf-8"))
    ready = {r["page_id"].replace("PAGE-", ""): r for r in ledger if r["publication_decision"].startswith("READY")}
    pages = [p for p in (page_from_block(i, ready[i["id"]]) for i in extract_pages() if i["id"] in ready) if p]
    pages_by_url = {p["url"]: p for p in pages}
    for p in pages:
        write_route(p["url"], page_html(p, pages_by_url))
    for src, dst in D.REDIRECTS.items():
        if src.endswith("/"):
            write_route(src, redirect_stub(dst))
    (DIST / "404.html").write_text(not_found_html(), encoding="utf-8")

    indexable = [p for p in pages if p["url"] not in D.NOINDEX_PATHS]
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n'
        % "\n".join("  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>" % (D.SITE["base_url"], p["url"], D.BUILD_DATE) for p in indexable), encoding="utf-8")
    if D.REVIEW_BUILD:
        (DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    else:
        (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % D.SITE["base_url"], encoding="utf-8")

    lines = ["# Legacy and draft routes -> canonical destinations (forced one-hop 301)"]
    for src, dst in D.REDIRECTS.items():
        lines.append("%s %s 301!" % (src, dst))
        if src.endswith("/") and src != "/":
            lines.append("%s %s 301!" % (src.rstrip("/"), dst))
    lines.append("/index.html / 301!")
    (DIST / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")

    headers = [
        "/*",
        "  X-Frame-Options: DENY",
        "  X-Content-Type-Options: nosniff",
        "  Referrer-Policy: strict-origin-when-cross-origin",
        "  Permissions-Policy: camera=(), microphone=(), geolocation=()",
        "  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; script-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'",
    ]
    if D.REVIEW_BUILD:
        headers.append("  X-Robots-Tag: noindex")
    for path in ("/css/*", "/js/*"):
        headers += [path, "  Cache-Control: public, max-age=31536000, immutable"]
    for path in ("/img/*", "/assets/*"):
        headers += [path, "  Cache-Control: public, max-age=86400, must-revalidate"]
    (DIST / "_headers").write_text("\n".join(headers) + "\n", encoding="utf-8")

    manifest = {
        "build": D.SITE["build_version"], "date": D.BUILD_DATE, "review": D.REVIEW_BUILD,
        "pages": [{"id": "PAGE-" + p["id"], "name": p["name"], "url": p["url"], "title": p["title"], "decision": p["ledger"]["publication_decision"]} for p in pages],
        "redirects": D.REDIRECTS,
        "excluded": [{"id": r["page_id"], "url": r["url"], "decision": r["publication_decision"]} for r in ledger if not r["publication_decision"].startswith("READY")],
    }
    (DIST / "build-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("Built %d governed pages, %d redirect stubs, sitemap with %d URLs." % (len(pages), len(D.REDIRECTS), len(indexable)))


if __name__ == "__main__":
    build()
