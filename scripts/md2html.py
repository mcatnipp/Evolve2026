#!/usr/bin/env python3
"""Minimal Markdown -> HTML for uploading project documents to Google Drive as Google Docs.
Handles headings, paragraphs, bullet and numbered lists, pipe tables, bold, italic, code and links.
Usage: python3 scripts/md2html.py docs/file.md > out.html
"""
import html
import re
import sys


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*]+)\*(?!\w)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|/[^)\s]*)\)", r'<a href="\2">\1</a>', s)
    return s


def convert(md):
    out, i, lines = [], 0, md.splitlines()
    para = []

    def flush():
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para)))
            para.clear()

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            flush(); i += 1; continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush(); out.append("<h%d>%s</h%d>" % (len(m.group(1)), inline(m.group(2)), len(m.group(1)))); i += 1; continue
        if line.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.match(r"^:?-{2,}:?$", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                head = "".join("<th>%s</th>" % inline(c) for c in rows[0])
                body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in rows[1:])
                out.append('<table border="1" cellpadding="6" style="border-collapse:collapse"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (head, body))
            continue
        if re.match(r"^\s*[-*]\s+", line) or re.match(r"^\s*\d+[.)]\s+", line):
            flush()
            ordered = bool(re.match(r"^\s*\d+[.)]\s+", line))
            items = []
            while i < len(lines) and (re.match(r"^\s*[-*]\s+", lines[i]) or re.match(r"^\s*\d+[.)]\s+", lines[i])):
                items.append(re.sub(r"^\s*(?:[-*]|\d+[.)])\s+", "", lines[i]))
                i += 1
                while i < len(lines) and lines[i].startswith("  ") and lines[i].strip() and not re.match(r"^\s*(?:[-*]|\d+[.)])\s+", lines[i]):
                    items[-1] += " " + lines[i].strip(); i += 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
            continue
        if line.startswith("```"):
            flush()
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i]); i += 1
            i += 1
            out.append("<pre>%s</pre>" % html.escape("\n".join(code)))
            continue
        if line.strip() == "---":
            flush(); out.append("<hr>"); i += 1; continue
        para.append(line.strip()); i += 1
    flush()
    return "\n".join(out)


if __name__ == "__main__":
    src = open(sys.argv[1], encoding="utf-8").read()
    body = convert(src)
    title = re.search(r"^#\s+(.+)$", src, re.M)
    sys.stdout.write('<html><head><meta charset="utf-8"><title>%s</title></head><body style="font-family:Arial,sans-serif;font-size:11pt;line-height:1.45">%s</body></html>'
                     % (html.escape(title.group(1)) if title else "Document", body))
