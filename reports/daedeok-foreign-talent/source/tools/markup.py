# Markup parser -> block list, shared by the HWPX and DOCX renderers.
import re

BULLETS = [("□ ", "b1"), ("○ ", "b2"), ("- ", "b3"), ("· ", "b4"), ("※ ", "b3")]


def inline_runs(text, base="body"):
    """Return [(text, charkey)] handling **bold** and 【red】."""
    out = []
    for part in re.split(r"(\*\*.+?\*\*|【[^】]*】)", text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            k = {"body": "bodyb", "boxb": "boxb", "note": "note", "tbl": "tblb"}.get(base, "bodyb")
            out.append((part[2:-2], k))
        elif part.startswith("【"):
            k = {"note": "notered", "tbl": "tblred"}.get(base, "redb" if base == "bodyb" else "red")
            out.append((part, k))
        else:
            out.append((part, base))
    return out


def parse(text):
    blocks = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        i += 1
        if not ln.strip():
            continue
        if ln.startswith("%%"):
            continue
        if ln.startswith("# "):
            blocks.append({"t": "h1", "text": ln[2:].strip()})
        elif ln.startswith("## "):
            blocks.append({"t": "h2", "text": ln[3:].strip()})
        elif ln.startswith("### "):
            blocks.append({"t": "h3", "text": ln[4:].strip()})
        elif ln.startswith("#### "):
            blocks.append({"t": "h4", "text": ln[5:].strip()})
        elif ln.startswith("!pb"):
            blocks.append({"t": "pb"})
        elif ln.startswith("!tbl"):
            parts = [p.strip() for p in ln[4:].split("|")]
            opts = {"title": parts[0]}
            for p in parts[1:]:
                if "=" in p:
                    k, v = p.split("=", 1)
                    opts[k.strip()] = v.strip()
            rows = []
            while i < len(lines) and not lines[i].startswith("!end"):
                row = lines[i]
                i += 1
                if not row.strip():
                    continue
                rows.append([c.strip().replace("\\n", "\n") for c in row.split(" | ")])
            i += 1
            blocks.append({"t": "table", "opts": opts, "rows": rows})
        elif ln.startswith("!box"):
            title = ln[4:].strip()
            items = []
            while i < len(lines) and not lines[i].startswith("!end"):
                if lines[i].strip():
                    items.append(lines[i].rstrip())
                i += 1
            i += 1
            blocks.append({"t": "box", "title": title, "items": items})
        elif ln.startswith("!fig"):
            parts = [p.strip() for p in ln[4:].split("|")]
            opts = {"file": parts[0], "title": parts[1] if len(parts) > 1 else ""}
            for p in parts[2:]:
                if "=" in p:
                    k, v = p.split("=", 1)
                    opts[k.strip()] = v.strip()
            blocks.append({"t": "fig", "opts": opts})
        elif ln.startswith("> "):
            blocks.append({"t": "note", "text": ln[2:]})
        elif ln.startswith('" '):
            blocks.append({"t": "quote", "text": ln[2:]})
        elif ln.startswith("!ref "):
            blocks.append({"t": "ref", "text": ln[5:]})
        elif ln.startswith("!plain "):
            blocks.append({"t": "plain", "text": ln[7:]})
        else:
            st = "body"
            for pre, s in BULLETS:
                if ln.startswith(pre):
                    st = s
                    break
            blocks.append({"t": "p", "style": st, "text": ln})
    return blocks
