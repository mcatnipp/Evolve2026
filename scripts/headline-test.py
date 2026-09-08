#!/usr/bin/env python3
"""Headline effectiveness test (pre-launch).

Two evidence streams are combined for every page's three H1 variants (A = control):
  1. Heuristic scoring (this script): length, readability, specificity, reader address,
     power/decision language, keyword carry, hype check. Weighted to 40% of the final score.
  2. Synthetic buyer panel (docs/headline-panel/*.json, written by persona reviewers):
     clarity, relevance, specificity, credibility, pull, 1-5 each, plus a winner pick.
     Weighted to 60% of the final score.

Outputs docs/headline-test-2026-09-08.csv, docs/headline-test-2026-09-08.md and
docs/headline-test-winners.json (url -> winning headline). Apply winners with
`python3 scripts/apply-headlines.py --winners`.
"""
import csv
import glob
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

POWER = {"you", "your", "before", "without", "stop", "never", "now", "first", "one", "straight", "proof", "proven",
         "decide", "decision", "decisions", "cost", "costs", "risk", "ready", "readiness", "accountable", "control",
         "controlled", "settle", "settled", "protect", "safely", "actually", "here", "why", "how", "what", "mistake",
         "easy", "hard", "lose", "loses", "keep", "free", "specific", "questions", "answers", "answer"}
HYPE = {"best", "largest", "leading", "world-class", "premier", "unmatched", "unrivaled", "guaranteed", "revolutionary",
        "cutting-edge", "state-of-the-art", "fastest", "industry-leading"}
CONCRETE = re.compile(r"\b(?:\d[\d,\.]*\+?|GW|MW|GPU|GPUs|Houston|Texas|shop|module|modules|switchgear|utility|commissioning|"
                      r"turnover|retrofit|retrofits|live|floor|plan|design|build|power|maintain|maintenance|site|sites|"
                      r"capacity|schedule|change orders|checklist|phase|campus|colocation|enterprise|AI|HPC|edge|modular|"
                      r"hyperscale|data center|data centers|data-center|facility|facilities|team|engineer)\b", re.I)


def syllables(word):
    w = word.lower().strip("'\".,:;!?")
    if not w:
        return 0
    v = re.findall(r"[aeiouy]+", w)
    n = len(v)
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n)


def keyword(url):
    parts = [p for p in url.split("/") if p]
    if not parts:
        return ["data center"]
    slug = parts[-1].replace("-", " ")
    return [w for w in slug.split() if len(w) > 3]


def heuristic(h1, url):
    words = re.findall(r"[A-Za-z0-9,\.\+']+", h1)
    n = len(words)
    chars = len(h1)
    # 1. Length: 8-16 words and <= 110 chars is the sweet spot for a B2B hero H1.
    length = 1.0 if 8 <= n <= 16 else (0.75 if 6 <= n <= 20 else 0.4)
    if chars > 130:
        length -= 0.25
    # 2. Readability: mean syllables per word (lower is clearer).
    spw = sum(syllables(w) for w in words) / max(1, n)
    read = 1.0 if spw <= 1.55 else (0.8 if spw <= 1.75 else 0.6)
    # 3. Specificity: concrete nouns, numbers, proper nouns.
    spec = min(1.0, 0.25 + 0.15 * len(CONCRETE.findall(h1)))
    # 4. Reader address ("you/your") or direct imperative.
    you = 1.0 if re.search(r"\b(you|your)\b", h1, re.I) else (0.7 if re.match(r"^(?:Stop|Find|Get|Add|Expand|Change|Bring|Put|Start|Tell|Build|Fabricate|Compare|Settle)\b", h1) else 0.5)
    # 5. Power/decision language density.
    pw = sum(1 for w in words if w.lower().strip(".,:") in POWER)
    power = min(1.0, 0.3 + 0.18 * pw)
    # 6. Keyword carry (page slug words present).
    kws = keyword(url)
    kw = sum(1 for k in kws if re.search(r"\b%s" % re.escape(k[:5]), h1, re.I)) / max(1, len(kws))
    kw = 0.5 + 0.5 * kw
    # 7. Hype penalty.
    hype = 0.0 if any(w.lower() in HYPE for w in words) else 1.0
    score = (0.15 * length + 0.15 * read + 0.2 * spec + 0.15 * you + 0.15 * power + 0.1 * kw + 0.1 * hype)
    return round(score * 100, 1), {"words": n, "chars": chars, "syl/word": round(spw, 2), "concrete": len(CONCRETE.findall(h1)),
                                   "power": pw, "you": bool(re.search(r"\b(you|your)\b", h1, re.I))}


def main():
    variants = json.loads((DOCS / "headline-variants.json").read_text())
    panels = []
    for f in sorted(glob.glob(str(DOCS / "headline-panel" / "*.json"))):
        try:
            panels.append((pathlib.Path(f).stem, json.loads(pathlib.Path(f).read_text())))
        except Exception as e:  # noqa: BLE001
            print("skipping", f, e)
    rows, winners, md = [], {}, []
    md.append("# Headline test, September 8, 2026\n")
    md.append("Method: every page's H1 has three variants (A = control applied on 2026-09-08). Each variant is scored two ways: "
              "a heuristic model (length, readability, specificity, reader address, decision language, keyword carry, hype check; 40%%) "
              "and a blind synthetic buyer panel of %d personas (clarity, relevance, specificity, credibility, pull; 60%%). "
              "Panel members did not know which variant was the control. Winners below are applied as the live H1; "
              "the runner-up is the recommended first live A/B test once traffic and analytics exist.\n" % len(panels))
    md.append("| Page | Variant | Headline | Heuristic | Panel | Final | Panel picks |\n|---|---|---|---|---|---|---|")
    for url, hs in variants.items():
        best, best_score = None, -1
        for i, h1 in enumerate(hs):
            label = "ABC"[i]
            heur, detail = heuristic(h1, url)
            panel_scores, picks = [], 0
            for name, data in panels:
                entry = data.get(url) or {}
                sc = (entry.get("scores") or {}).get(label) or {}
                vals = [v for v in sc.values() if isinstance(v, (int, float))]
                if vals:
                    panel_scores.append(sum(vals) / len(vals) / 5 * 100)
                if entry.get("winner") == label:
                    picks += 1
            panel = round(sum(panel_scores) / len(panel_scores), 1) if panel_scores else None
            final = round(0.4 * heur + 0.6 * panel, 1) if panel is not None else heur
            rows.append([url, label, h1, heur, panel if panel is not None else "", final, picks, json.dumps(detail)])
            md.append("| %s | %s | %s | %s | %s | %s | %s |" % (url, label, h1.replace("|", "/"), heur, panel if panel is not None else "n/a", final, picks))
            if final > best_score:
                best, best_score = h1, final
        winners[url] = best
    (DOCS / "headline-test-2026-09-08.csv").write_text("")
    with open(DOCS / "headline-test-2026-09-08.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["url", "variant", "headline", "heuristic_score", "panel_score", "final_score", "panel_picks", "heuristic_detail"])
        w.writerows(rows)
    changed = [u for u, h in winners.items() if h != variants[u][0]]
    md.append("\n## Result\n")
    md.append("%d pages tested, %d where a challenger beat the control and was applied: %s\n" % (len(variants), len(changed), ", ".join(changed) or "none"))
    (DOCS / "headline-test-2026-09-08.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (DOCS / "headline-test-winners.json").write_text(json.dumps(winners, indent=2), encoding="utf-8")
    print("scored %d variants across %d pages with %d panel files; %d challengers won" % (len(rows), len(variants), len(panels), len(changed)))


if __name__ == "__main__":
    main()
