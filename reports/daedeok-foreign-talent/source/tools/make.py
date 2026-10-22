# Two-pass build: DOCX proxy -> PDF -> page map -> final HWPX/HWP/DOCX.
import os, sys, re, subprocess, shutil
sys.path.insert(0, os.path.dirname(__file__))
import render
from docxbuild import DocxBuilder
from hwpbuild import Builder

ROOT = render.ROOT
OUT = os.path.join(ROOT, "out")
os.makedirs(OUT, exist_ok=True)
NAME = "대덕특구_외국인인재_활용전략_최종보고서"


def to_pdf(docx):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", OUT, docx],
                   check=True, capture_output=True, timeout=600)
    return docx[:-5] + ".pdf"


def page_texts(pdf):
    out = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    return [re.sub(r"\s+", "", p) for p in out.split("\f")]


def norm(s):
    return re.sub(r"\s+", "", s)


def page_map(pdf, front_pages, items):
    pages = page_texts(pdf)
    res = {}
    cur = front_pages
    for key, text in items:
        t = norm(text)[:40]
        for i in range(cur, len(pages)):
            if t in pages[i]:
                res[key] = i - front_pages + 1
                cur = i
                break
    return res, len(pages) - front_pages


def main():
    # pass 0: front-only page count
    d0 = DocxBuilder(); render.build(d0, front_only=True)
    p0 = os.path.join(OUT, "front.docx"); d0.save(p0)
    front = len(page_texts(to_pdf(p0))) - 1  # trailing formfeed
    # pass 1
    d1 = DocxBuilder(); blocks, toc, lot, lof = render.build(d1)
    p1 = os.path.join(OUT, "pass1.docx"); d1.save(p1)
    pdf1 = to_pdf(p1)
    items = []
    for lvl, text, b in toc:
        title = render.h1_runs(text)[1] if lvl == 1 else text
        items.append((id(b), title))
    # tables/figures are interleaved with headings: build ordered list from blocks
    ordered = []
    for b in blocks:
        if b["t"] in ("h1", "h2", "h3"):
            title = render.h1_runs(b["text"])[1] if b["t"] == "h1" else b["text"]
            ordered.append((b["k"], title))
        elif b.get("cap"):
            ordered.append((b["k"], b["cap"]))
    pages, nmain = page_map(pdf1, front, ordered)
    print("front pages:", front, "main pages:", nmain, "mapped:", len(pages), "/", len(ordered))
    # final
    d2 = DocxBuilder(); render.build(d2, pages=pages)
    fd = os.path.join(OUT, NAME + ".docx"); d2.save(fd)
    pdf2 = to_pdf(fd)
    print("final pdf pages:", len(page_texts(pdf2)) - 1)
    hb = Builder(); render.build(hb, pages=pages)
    hb.save(os.path.join(OUT, NAME + ".hwpx"), os.path.join(OUT, NAME + ".hwp"))
    print("saved")


if __name__ == "__main__":
    main()
