#!/usr/bin/env python3
"""Post-build validation for the Evolve site.

Fails (exit 1) on: blocked-claim patterns, broken internal links, missing
images, duplicate titles or descriptions, pages without exactly one H1,
links to gated routes, or sitemap/manifest mismatches.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import data as D

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

BLOCKED_PATTERNS = [
    (r"\b1,000\+", "retired 1,000+ figure"),
    (r"\b110\+", "110+ facilities figure"),
    (r"\b52 (?:customer )?facilities", "52 facilities monitored"),
    (r"\b1,000\+? (?:power|facilities|projects|Texas)", "1,000+ maintenance/project figure"),
    (r"\b(?:2,900|3,000)\+", "retired project counts"),
    (r"\b6,000\+? ?MW", "retired 6,000 MW figure"),
    (r"\b350\+ facilities", "retired 350+ facilities"),
    (r"\$1B\+?|\$650 million", "unapproved financial figures"),
    (r"\b4[05]\+ (?:member|team|people)", "unapproved headcount"),
    (r"since 2004", "retired safety date (must be since 2010)"),
    (r"world'?s first|patented|patent[- ]pending", "unapproved patent claims"),
    (r"zero[- ]downtime", "zero-downtime claim"),
    (r"largest (?:24/7|service|maintenance|team|network)", "superlative service claims"),
    (r"24/7/365|guaranteed response", "response guarantees"),
    (r"\b(?:Europe|Africa|Canada|United Kingdom|UK expansion)\b", "international claims"),
    (r"\b(?:Verizon|Foxconn|Rice University|Texas A&M|Aramco|DHL|Dow Chemical|Waste Management|Bank of America|Google|Microsoft|Meta|Amazon Web Services|Yahoo|QTS|CyrusOne|Stream Data|DataBank|Vantage|H5 Data|CloudBurst|Cloudburst|San Marcos|Providence|Holder)\b", "named customers or projects"),
    (r"\b(?:HIPAA|PCI|FedRAMP|FISMA)\b", "compliance credential claims"),
    (r"lorem ipsum|\[first_category\]|STOP! Edit", "placeholder content"),
    (r"\bNetZero\b|\bNet Zero\b", "NetZero product claim"),
    (r"\b(?:3\.5 MW|500 kW)\b", "Evolution Series specifications"),
    (r"kW per rack|kW racks|\b100 kW\b", "rack-density specifics"),
    (r"DO NOT PUBLISH|CONTENT HOLD|\[UNRESOLVED|claims ledger|approval ledger", "editorial leakage"),
]

GATED_URLS = {r["url"] for r in D.__dict__.get("_ledger_rows", [])}


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.imgs, self.h1, self.title, self.desc = [], [], 0, None, None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.imgs.append(a.get("src", ""))
            for part in (a.get("srcset") or "").split(","):
                u = part.strip().split(" ")[0]
                if u:
                    self.imgs.append(u)
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data


def text_only(html_text):
    body = re.sub(r"<script[\s\S]*?</script>", "", html_text)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", body)


def main():
    manifest = json.loads((DIST / "build-manifest.json").read_text())
    page_urls = {p["url"] for p in manifest["pages"]}
    gated = {e["url"] for e in manifest["excluded"]}
    problems = []
    titles, descs = {}, {}
    files = sorted(p for p in DIST.rglob("index.html"))
    redirect_paths = set(D.REDIRECTS.keys())
    for f in files:
        rel = "/" + str(f.parent.relative_to(DIST)).replace("\\", "/") + "/"
        rel = "/" if rel == "/./" else rel
        if rel in redirect_paths:
            continue
        html_text = f.read_text(encoding="utf-8")
        text = text_only(html_text)
        for pat, why in BLOCKED_PATTERNS:
            m = re.search(pat, text)
            if m:
                problems.append("%s: blocked claim (%s): '%s'" % (rel, why, m.group(0)))
        p = LinkCollector()
        p.feed(html_text)
        if p.h1 != 1:
            problems.append("%s: %d H1 elements" % (rel, p.h1))
        if p.title in titles:
            problems.append("%s: duplicate title with %s" % (rel, titles[p.title]))
        titles[p.title] = rel
        if p.desc in descs:
            problems.append("%s: duplicate description with %s" % (rel, descs[p.desc]))
        descs[p.desc] = rel
        for href in p.links:
            if href.startswith(("http", "tel:", "mailto:", "#")):
                continue
            path = href.split("?")[0].split("#")[0]
            if not path:
                continue
            if path in gated:
                problems.append("%s: links to gated route %s" % (rel, path))
            target = DIST / path.strip("/") / "index.html" if path.endswith("/") else DIST / path.strip("/")
            if path == "/":
                target = DIST / "index.html"
            if not target.exists():
                problems.append("%s: broken link %s" % (rel, href))
        for src in p.imgs:
            if src.startswith("/") and not (DIST / src.strip("/")).exists():
                problems.append("%s: missing image %s" % (rel, src))
    sitemap = (DIST / "sitemap.xml").read_text()
    for u in page_urls - D.NOINDEX_PATHS:
        if D.SITE["base_url"] + u not in sitemap:
            problems.append("sitemap missing %s" % u)
    for u in gated:
        if D.SITE["base_url"] + u in sitemap:
            problems.append("sitemap includes gated %s" % u)
    if problems:
        print("\n".join(problems))
        print("\nFAIL: %d problem(s)" % len(problems))
        sys.exit(1)
    print("PASS: %d pages checked, no blocked claims, no broken links, unique metadata, one H1 per page." % len(page_urls))


if __name__ == "__main__":
    main()
