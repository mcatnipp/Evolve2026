#!/usr/bin/env python3
"""Write docs/copy-system-2026-09-08.md: the page-by-page headline layer as built, with word counts,
so the copy can be reviewed in one place without opening the packages."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build as B  # noqa: E402
import data as D  # noqa: E402


def words(text):
    return len(re.findall(r"[A-Za-z0-9'’]+", B.strip_md(text or "")))


def main():
    ledger = B.parse_csv((B.CONTENT / "Evolve_Copy_Approval_Ledger_2026-09-07.csv").read_text(encoding="utf-8"))
    ready = {r["page_id"].replace("PAGE-", ""): r for r in ledger if r["publication_decision"].startswith("READY")}
    pages = [p for p in (B.page_from_block(i, ready[i["id"]]) for i in B.extract_pages() if i["id"] in ready) if p]
    out = ["# Copy system as built, September 8, 2026\n",
           "Voice rules: `docs/copy-voice-guide.md`. Headline test: `docs/headline-test-2026-09-08.md`. Funnels: `docs/funnels-2026-09-08.md`.\n",
           "Every page below was rewritten on 2026-09-08 in the direct-response voice within the approved claims. "
           "The H1, hero intro, calls to action and final call to action were set by `scripts/apply-headlines.py`; "
           "body sections were rewritten in the copy packages and validated with `scripts/validate-copy.py` and the build gate (`check.py`).\n",
           "| Page | H1 | Hero intro (first words) | Primary CTA | Final CTA heading | Body words |",
           "|---|---|---|---|---|---|"]
    total = 0
    for p in pages:
        body_words = words(p["body"])
        total += body_words
        out.append("| %s | %s | %s… | %s | %s | %d |" % (
            p["url"], p["h1"].replace("|", "/"), " ".join(B.strip_md(p["intro"]).split()[:12]).replace("|", "/"),
            p["primary"], (p["final_heading"] or "").replace("|", "/"), body_words))
    out.append("\nPages: %d. Body words across the site: %d. Lead magnets: %d. Funnel bands: %d pages.\n" % (len(pages), total, len(D.LEAD_MAGNETS), len(D.FUNNELS)))
    (ROOT / "docs" / "copy-system-2026-09-08.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("wrote docs/copy-system-2026-09-08.md for %d pages" % len(pages))


if __name__ == "__main__":
    main()
