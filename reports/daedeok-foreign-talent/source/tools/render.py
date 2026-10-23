# Render the report: content/*.md -> HWPX/HWP (+ DOCX proxy for page estimation).
import sys, os, re, glob, json, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from markup import parse, inline_runs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
FIGS = os.path.join(ROOT, "figs")
TITLE = "대덕특구 기업경쟁력 제고를 위한\n외국인 인재 활용 전략"


def load_main():
    files = sorted(glob.glob(os.path.join(CONTENT, "c*.md")))
    blocks = []
    for f in files:
        blocks += parse(open(f, encoding="utf-8").read())
    return blocks


def number_blocks(blocks):
    """Assign <표 n-m>/[그림 n-m] numbers by chapter; collect toc/lot/lof."""
    chap = 0; tn = 0; fn = 0
    toc, lot, lof = [], [], []
    for k, b in enumerate(blocks):
        b["k"] = k
        if b["t"] == "h1":
            m = re.match(r"제(\d+)장", b["text"])
            if m:
                chap = int(m.group(1)); tn = fn = 0
                prefix = str(chap)
            else:
                chap = b["text"]; tn = fn = 0
                prefix = "부"
            b["prefix"] = prefix
            toc.append((1, b["text"], b))
        elif b["t"] == "h2":
            toc.append((2, b["text"], b))
        elif b["t"] == "h3":
            toc.append((3, b["text"], b))
        elif b["t"] == "table" and b["opts"].get("title") and b["opts"].get("nocap") != "1":
            tn += 1
            pre = b.get("prefix") or (str(chap) if isinstance(chap, int) else "부")
            b["cap"] = "<표 %s-%d> %s" % (pre if isinstance(chap, int) else "부", tn, b["opts"]["title"]) \
                if isinstance(chap, int) else "<부표 %d> %s" % (tn, b["opts"]["title"])
            lot.append((b["cap"], b))
        elif b["t"] == "fig":
            fn += 1
            b["cap"] = "[그림 %s-%d] %s" % (chap, fn, b["opts"]["title"]) if isinstance(chap, int) \
                else "[부도 %d] %s" % (fn, b["opts"]["title"])
            lof.append((b["cap"], b))
    return toc, lot, lof


def h1_runs(text):
    m = re.match(r"(제\d+장)\s+(.*)", text)
    return m.groups() if m else (None, text)


def emit(bld, blocks, kind):
    for b in blocks:
        t = b["t"]
        if t == "h1":
            chapno, title = h1_runs(b["text"])
            bld.gothic = False
            bld.page_break()
            if chapno:
                bld.para([(chapno, "h1s")], "h1top")
                bld.para([(title, "h1")], "h1")
            else:
                bld.para([(title, "h1")], "h1top")
        elif t == "h2":
            bld.para([(b["text"], "h2")], "h2")
        elif t == "h3":
            bld.para([(b["text"], "h3")], "h3")
        elif t == "h4":
            bld.para([(b["text"], "h4")], "h4")
        elif t == "pb":
            bld.page_break()
        elif t == "p":
            bld.para(inline_runs(b["text"]), b["style"])
        elif t == "plain":
            bld.para(inline_runs(b["text"]), "plain")
        elif t == "note":
            bld.para(inline_runs(b["text"], "note"), "note")
        elif t == "quote":
            bld.para(inline_runs(b["text"]), "quote")
        elif t == "ref":
            bld.para(inline_runs(b["text"]), "ref")
        elif t == "table":
            o = b["opts"]
            if b.get("cap"):
                bld.para([(b["cap"], "cap")], "cap")
            if o.get("unit"):
                bld.para([("(단위: %s)" % o["unit"], "note")], "right")
            rows = b["rows"]
            widths = [float(x) for x in o["widths"].split(",")] if o.get("widths") else None
            aligns = o.get("align")
            merges = []
            if o.get("merge"):
                for m in o["merge"].split(";"):
                    merges.append(tuple(int(x) for x in m.split(",")))
            hr = int(o.get("head", "1"))
            font = o.get("font", "tbl")
            ncols = max(len(r) for r in rows)
            rows = [r + [""] * (ncols - len(r)) for r in rows]
            from hwpbuild import BF_HEAD, BF_SHADE
            cell_bf = {}
            for ri, row in enumerate(rows):
                for ci, cell in enumerate(row):
                    if cell.startswith("^^"):
                        cell_bf[(ri, ci)] = BF_HEAD
                        row[ci] = "\n".join("**%s**" % x if x else x for x in cell[2:].strip().split("\n"))
                    elif cell.startswith("~~"):
                        cell_bf[(ri, ci)] = BF_SHADE
                        row[ci] = cell[2:].strip()
            bld.table(rows, widths=widths, header_rows=hr, aligns=aligns, merges=merges, font=font, cell_bf=cell_bf)
            if o.get("src"):
                bld.para(inline_runs("자료: " + o["src"], "note"), "note")
            elif o.get("note"):
                bld.para(inline_runs(o["note"], "note"), "note")
            else:
                bld.para([("", "note")], "note")
        elif t == "box":
            paras = []
            if b["title"]:
                paras.append(("boxt", [(b["title"], "boxt")]))
            for it in b["items"]:
                paras.append(("boxp", inline_runs(it, "boxb")))
            bld.box(paras)
            bld.para([("", "note")], "note")
        elif t == "fig":
            o = b["opts"]
            path = os.path.join(FIGS, o["file"])
            bld.picture(path, float(o.get("width", 150)))
            bld.para([(b["cap"], "cap")], "capfig")
            if o.get("src"):
                bld.para(inline_runs("자료: " + o["src"], "note"), "note")


def cover(bld):
    for _ in range(4):
        bld.para("", "cover")
    bld.para([("최종보고서", "cover4")], "cover")
    bld.para("", "cover")
    bld.para("", "cover")
    for line in TITLE.split("\n"):
        bld.para([(line, "cover1")], "cover")
    bld.para("", "cover")
    bld.para([("Strategies for Utilizing Foreign Talent to Enhance", "cover4")], "cover")
    bld.para([("the Competitiveness of Firms in Daedeok Innopolis", "cover4")], "cover")
    for _ in range(9):
        bld.para("", "cover")
    bld.para([("2026. 10.", "cover2")], "cover")
    for _ in range(5):
        bld.para("", "cover")
    bld.para([("【연구수행기관명】", "cover3")], "cover")


def submission(bld):
    bld.page_break()
    for _ in range(3):
        bld.para("", "cover")
    bld.para([("제 출 문", "h1")], "h1")
    bld.para("", "cover")
    bld.para([("【발주기관장】 귀하", "bodyb")], "plain")
    bld.para("", "plain")
    bld.para("본 보고서를 「대덕특구 기업경쟁력 제고를 위한 외국인 인재 활용 전략」 연구의 최종보고서로 제출합니다.", "body")
    bld.para("", "plain")
    bld.para("본 연구는 대덕연구개발특구 기술기반 기업의 연구개발·전문기술 인력 부족 실태와 외국인 전문인력 채용수요 및 장애요인을 분석하고, 한국과학기술원(KAIST), 과학기술연합대학원대학교(UST), 충남대학교, 국립한밭대학교 등 지역 대학에서 양성된 외국인 과학기술 인재를 기업의 연구개발, 기술사업화 및 해외시장 진출에 활용하기 위한 실천적 전략을 제시하였습니다.", "body")
    for _ in range(4):
        bld.para("", "plain")
    bld.para([("2026년 10월", "cover3")], "cover")
    for _ in range(4):
        bld.para("", "plain")
    rows = [["연구기관", "【연구수행기관명】"], ["연구책임자", "【성명 / 소속·직위】"],
            ["공동연구원", "【성명 / 소속·직위】"], ["연구보조원", "【성명 / 소속·직위】"],
            ["연구기간", "2026. 8. 1. ∼ 2026. 10. 31.(3개월)"]]
    bld.table(rows, widths=[1, 2.6], header_rows=0, aligns="cl", repeat=False)


def toc_pages(bld, toc, lot, lof, pages):
    bld.gothic = True
    try:
        _toc_pages(bld, toc, lot, lof, pages)
    finally:
        bld.gothic = False


def _toc_pages(bld, toc, lot, lof, pages):
    def pg(b):
        return str(pages.get(b["k"], "")) if pages else "0"
    bld.page_break()
    bld.para([("목  차", "h1")], "h1")
    for lvl, text, b in toc:
        st = {1: "toc1", 2: "toc2", 3: "toc3"}[lvl]
        bld.para([(text + "\t" + pg(b), st)], st)
    bld.page_break()
    bld.para([("표 목 차", "h1")], "h1")
    for cap, b in lot:
        bld.para([(cap + "\t" + pg(b), "toc3")], "toc2")
    if not lof:
        return
    bld.page_break()
    bld.para([("그 림 목 차", "h1")], "h1")
    for cap, b in lof:
        bld.para([(cap + "\t" + pg(b), "toc3")], "toc2")


def build(bld, pages=None, front_only=False):
    blocks = load_main()
    toc, lot, lof = number_blocks(blocks)
    cover(bld)
    submission(bld)
    summ = parse(open(os.path.join(CONTENT, "summary.md"), encoding="utf-8").read())
    first = True
    for b in summ:
        if b["t"] == "h1":
            b["t"] = "h1x"
    bld.page_break()
    bld.para([("요  약", "h1")], "h1")
    emit(bld, [b for b in summ if b["t"] != "h1x"], "front")
    toc_pages(bld, toc, lot, lof, pages)
    if front_only:
        return blocks, toc, lot, lof
    if hasattr(bld, "new_section"):
        bld.new_section()
    else:
        bld.new_main_section()
    emit(bld, blocks, "main")
    bld.gothic = False
    return blocks, toc, lot, lof
