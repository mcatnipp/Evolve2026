#!/usr/bin/env python3
"""Validate one or more copy packages without touching dist/.

Checks every page block in the given content files:
  * structure markers the generator depends on are present (URL, Publishable copy, Metadata, Title, Meta description)
  * the rendered page text contains no blocked-claim patterns (same list as check.py)
  * no new numbers appear that are not in the approved set or in the original git version of the file
  * banned hype words are absent
Usage: python3 scripts/validate-copy.py content/Evolve_Copy_01_Core_Design_Build_2026-09-07.md [more files]
Exit code 1 on any problem.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build as B  # noqa: E402
import check as C  # noqa: E402

BANNED = re.compile(r"\b(best|largest|leading|world[- ]class|premier|unmatched|unrivaled|number one|#1|cutting[- ]edge|state[- ]of[- ]the[- ]art|revolutionary|industry[- ]leading|24/7/365|fastest)\b", re.I)
# "guarantee" is only banned as a positive promise; the governed phrase "does not create a ... response guarantee" and
# editorial negations ("cannot guarantee") are allowed.
PROMISE = re.compile(r"\b(?:we|evolve|our team)\s+(?:can\s+)?guarantees?\b|\bguaranteed\s+(?:response|uptime|schedule|delivery|savings|results?)\b", re.I)
APPROVED_NUMBERS = {"2,200", "5.3", "20", "2010", "2004", "10555", "77070", "832", "375", "0099", "2026", "2025", "2024", "30", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "12", "15", "24", "48", "60", "90", "100", "13"}


def original_text(path):
    try:
        return subprocess.run(["git", "show", "HEAD:%s" % path.relative_to(ROOT)], capture_output=True, text=True, cwd=ROOT, check=True).stdout
    except Exception:
        return ""


def numbers(text):
    text = re.sub(r"\b(?:PAGE|CLM|INTENT|COPY|ARCH|GOV|DS|AD|RQ|ISSUE|CHG|SRC|BUILD)-[\w\.-]+", " ", text)
    text = re.sub(r"\b20\d\d-\d\d-\d\d\b|\bv\d+\.\d+\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, 20\d\d", " ", text)
    return {n.rstrip(".,") for n in re.findall(r"\d[\d,\.]*", text)}


def main(paths):
    problems = []
    ledger = B.parse_csv((B.CONTENT / "Evolve_Copy_Approval_Ledger_2026-09-07.csv").read_text(encoding="utf-8"))
    ready = {r["page_id"].replace("PAGE-", ""): r for r in ledger if r["publication_decision"].startswith("READY")}
    all_items = B.extract_pages()
    pages = [p for p in (B.page_from_block(i, ready[i["id"]]) for i in all_items if i["id"] in ready) if p]
    by_url = {p["url"]: p for p in pages}
    for path in paths:
        path = pathlib.Path(path).resolve()
        text = path.read_text(encoding="utf-8")
        orig = original_text(path)
        orig_numbers = numbers(orig) | APPROVED_NUMBERS
        for m in re.finditer(r"^# PAGE-(\d+) — ([^\n]+)$", text, re.M):
            pid = m.group(1)
            block_end = text.find("\n# PAGE-", m.end())
            block = text[m.start(): block_end if block_end > 0 else len(text)]
            if pid not in ready:
                continue
            for marker in (r"^\*\*URL:\*\*", r"^## Publishable (?:page copy|article)", r"^## Metadata recommendation", r"\*\*Title:\*\*", r"\*\*Meta description:\*\*"):
                if not re.search(marker, block, re.M):
                    problems.append("PAGE-%s: missing marker %s" % (pid, marker))
            item = next((i for i in all_items if i["id"] == pid), None)
            page = B.page_from_block(item, ready[pid]) if item else None
            if not page:
                problems.append("PAGE-%s: page_from_block failed (structure broken)" % pid)
                continue
            html = B.page_html(page, by_url)
            plain = C.text_only(html)
            for pat, why in C.BLOCKED_PATTERNS:
                mm = re.search(pat, plain)
                if mm:
                    problems.append("PAGE-%s (%s): blocked claim (%s): '%s'" % (pid, page["url"], why, mm.group(0)))
            for mm in BANNED.finditer(plain):
                problems.append("PAGE-%s (%s): banned word '%s'" % (pid, page["url"], mm.group(0)))
            for mm in PROMISE.finditer(plain):
                before = plain[max(0, mm.start() - 40):mm.start()].lower()
                if re.search(r"\b(?:not|no|never|without|cannot|isn't|doesn't|does not|is not|rather than|does|can|will|should)\b[^.]{0,30}$", before):
                    continue
                problems.append("PAGE-%s (%s): promise language '%s'" % (pid, page["url"], mm.group(0)))
            new_nums = numbers(block) - orig_numbers if orig else set()
            if new_nums:
                problems.append("PAGE-%s (%s): new numbers not in original or approved set: %s" % (pid, page["url"], sorted(new_nums)))
    if problems:
        print("\n".join(problems))
        print("FAIL: %d problem(s)" % len(problems))
        sys.exit(1)
    print("PASS: %d file(s) validated, no blocked claims, no banned words, no new numbers, structure intact." % len(paths))


if __name__ == "__main__":
    main(sys.argv[1:] or [str(p) for p in sorted(B.CONTENT.glob("Evolve_Copy_0*.md"))])
