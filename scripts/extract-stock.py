#!/usr/bin/env python3
"""Crawl the two reference sites and download every photograph they use.

Sources: the Cloudways WordPress mockup and the current evolveincorporated.com.
Collects <img src/srcset/data-src>, inline background-image styles, Elementor
data-settings backgrounds and background images in the Elementor CSS files.
Writes originals to the target folder with a manifest CSV (url, page, bytes).
Usage: python3 scripts/extract-stock.py <out_dir>
"""
import csv
import hashlib
import html as htmlmod
import re
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path

CTX = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) EvolveSiteBuild/1.0"}

MOCKUP = "https://wordpress-1597787-6262585.cloudwaysapps.com"
CURRENT = "https://www.evolveincorporated.com"

MOCKUP_PAGES = ["/", "/services/design-build/", "/services/power-generation/", "/services/facility-management/",
                "/services/elert-monitoring/", "/industries/", "/industries/healthcare/", "/industries/financial-services/",
                "/industries/telecom/", "/industries/government-education/", "/industries/energy/",
                "/industries/colocation-providers/", "/industries/manufacturing-industrial/", "/solutions/",
                "/solutions/ai-hpc-data-centers/", "/solutions/edge-data-centers/", "/solutions/modular-data-centers/",
                "/solutions/colocation-data-centers/", "/solutions/greenfield-new-builds/", "/solutions/brownfield-retrofit/",
                "/ai-ready-data-centers/"]
CURRENT_PAGES = ["/", "/design-and-build", "/power-generation", "/preventative-maintenance", "/elert-tm-monitoring",
                 "/evolve-energy", "/markets-we-serve", "/markets-we-serve/telecom", "/markets-we-serve/energy",
                 "/markets-we-serve/hospitals", "/markets-we-serve/colocation", "/markets-we-serve/crypto-mining",
                 "/markets-we-serve/schools-and-government", "/markets-we-serve/modular-data-centers", "/about",
                 "/leadership", "/company-news", "/contact"]

IMG_EXT = re.compile(r"\.(jpe?g|png|webp)(\?.*)?$", re.I)
SKIP = re.compile(r"(logo|icon|favicon|seal|badge|arrow|group-\d|frame-\d|placeholder|spinner|loading|\.svg)", re.I)


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", errors="ignore")


def collect_urls(page_html, base):
    found = set()
    for m in re.finditer(r'(?:src|data-src|data-lazy-src|href|data-bg|data-background)=["\']([^"\']+)["\']', page_html):
        found.add(m.group(1))
    for m in re.finditer(r'(?:srcset|data-srcset)=["\']([^"\']+)["\']', page_html):
        for part in m.group(1).split(","):
            u = part.strip().split(" ")[0]
            if u:
                found.add(u)
    for m in re.finditer(r'url\((["\']?)([^)"\']+)\1\)', page_html):
        found.add(m.group(2))
    for m in re.finditer(r'"url"\s*:\s*"([^"]+)"', htmlmod.unescape(page_html)):
        found.add(m.group(1).replace("\\/", "/"))
    out = set()
    for u in found:
        u = htmlmod.unescape(u).strip()
        if not u or u.startswith("data:"):
            continue
        absu = urllib.parse.urljoin(base, u)
        if IMG_EXT.search(absu) and not SKIP.search(absu):
            out.add(absu)
    return out


def original_candidates(url):
    """WordPress sized variants -> try the original first."""
    cands = []
    m = re.match(r"^(.*)-\d{2,4}x\d{2,4}(\.[a-z]+)$", url, re.I)
    if m:
        cands.append(m.group(1) + m.group(2))
    cands.append(url)
    return cands


def main():
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "raw-stock")
    out_dir.mkdir(parents=True, exist_ok=True)
    seen_hash = {}
    rows = []
    jobs = [(MOCKUP, p, "mockup") for p in MOCKUP_PAGES] + [(CURRENT, p, "current") for p in CURRENT_PAGES]
    for base, path, tag in jobs:
        page_url = base + path
        try:
            page_html = fetch(page_url)
        except Exception as e:  # noqa: BLE001
            print("skip page", page_url, e)
            continue
        urls = collect_urls(page_html, page_url)
        # Elementor per-post CSS holds background images.
        for css_url in set(re.findall(r'href=["\']([^"\']*elementor/css/post-\d+\.css[^"\']*)["\']', page_html)):
            try:
                urls |= collect_urls(fetch(urllib.parse.urljoin(page_url, css_url)), page_url)
            except Exception:  # noqa: BLE001
                pass
        for u in sorted(urls):
            key = re.sub(r"-\d{2,4}x\d{2,4}(\.[a-z]+)$", r"\1", u.split("?")[0], flags=re.I)
            if key in seen_hash:
                rows.append([seen_hash[key], u, page_url, tag, "dup"])
                continue
            data = None
            got = None
            for cand in original_candidates(u):
                try:
                    data = fetch(cand, binary=True)
                    got = cand
                    break
                except Exception:  # noqa: BLE001
                    continue
            if not data or len(data) < 25000:
                continue
            digest = hashlib.md5(data).hexdigest()[:10]
            ext = re.search(r"\.(jpe?g|png|webp)", got, re.I).group(1).lower().replace("jpeg", "jpg")
            name = "%s-%s-%s.%s" % (tag, digest, re.sub(r"[^a-z0-9]+", "-", Path(urllib.parse.urlparse(got).path).stem.lower())[:40].strip("-"), ext)
            (out_dir / name).write_bytes(data)
            seen_hash[key] = name
            rows.append([name, got, page_url, tag, len(data)])
            print("saved", name, len(data))
    with (out_dir / "manifest.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "url", "page", "site", "bytes"])
        w.writerows(rows)
    print("done: %d files" % len(seen_hash))


if __name__ == "__main__":
    main()
