# HWPX builder on top of python-hwpx: custom header styles + raw section XML.
import copy, io, zipfile, random
from lxml import etree
from hwpx import HwpxDocument

SKEL = "/usr/local/lib/python3.13/dist-packages/hwpx/data/Skeleton.hwpx"
NS = {
    "hh": "http://www.hancom.co.kr/hwpml/2011/head",
    "hp": "http://www.hancom.co.kr/hwpml/2011/paragraph",
    "hc": "http://www.hancom.co.kr/hwpml/2011/core",
    "hs": "http://www.hancom.co.kr/hwpml/2011/section",
}
HH = "{%s}" % NS["hh"]; HP = "{%s}" % NS["hp"]; HC = "{%s}" % NS["hc"]
UCHAR = "http://www.hancom.co.kr/hwpml/2016/HwpUnitChar"

TEXT_W = 42520  # 150 mm

FONTS = ["휴먼명조", "HY헤드라인M", "맑은 고딕", "휴먼고딕"]  # appended ids 2,3,4,5
F_MJ, F_HD, F_GO, F_HG = 2, 3, 4, 5

# key: (font, size_pt, bold, color)
CHARS = {
    "body": (F_MJ, 12, False, "#000000"),
    "bodyb": (F_MJ, 12, True, "#000000"),
    "red": (F_MJ, 12, False, "#C00000"),
    "redb": (F_MJ, 12, True, "#C00000"),
    "tbl": (F_HG, 10, False, "#000000"),
    "tblb": (F_HG, 10, True, "#000000"),
    "tblred": (F_HG, 10, False, "#C00000"),
    "note": (F_MJ, 9.5, False, "#000000"),
    "notered": (F_MJ, 9.5, False, "#C00000"),
    "cap": (F_MJ, 11, True, "#000000"),
    "h1": (F_HD, 20, False, "#000000"),
    "h1s": (F_HD, 14, False, "#1F3864"),
    "h2": (F_HD, 15, False, "#000000"),
    "h3": (F_MJ, 13, True, "#000000"),
    "h4": (F_MJ, 12, True, "#000000"),
    "cover1": (F_HD, 24, False, "#000000"),
    "cover2": (F_HD, 16, False, "#000000"),
    "cover3": (F_MJ, 15, True, "#000000"),
    "cover4": (F_HD, 13, False, "#1F3864"),
    "toc1": (F_HG, 12, True, "#000000"),
    "toc2": (F_HG, 12, False, "#000000"),
    "toc3": (F_HG, 11, False, "#000000"),
    "tocH": (F_HG, 20, True, "#000000"),
    "boxt": (F_HG, 13, True, "#1F3864"),
    "boxb": (F_HG, 11.5, False, "#000000"),
    "boxbb": (F_HG, 11.5, True, "#000000"),
    "small": (F_MJ, 10, False, "#000000"),
    "pgnum": (F_MJ, 10, False, "#000000"),
}

for _k, (_f, _s, _b, _c) in list(CHARS.items()):
    CHARS["g_" + _k] = (F_HG if _f in (F_MJ, F_HD) else _f, _s, _b, _c)

# key: (align, left, indent(first-line; negative=hanging), prev, next, linespacing%, keepNext, tab)
# lengths in pt
PARAS = {
    "body": ("JUSTIFY", 0, 12, 0, 6, 160, 0, None),
    "plain": ("JUSTIFY", 0, 0, 0, 4, 160, 0, None),
    "b1": ("JUSTIFY", 0, -15, 4, 4, 160, 0, None),        # □
    "b2": ("JUSTIFY", 14, -14, 0, 4, 160, 0, None),       # ○
    "b3": ("JUSTIFY", 28, -10, 0, 3, 160, 0, None),       # -
    "b4": ("JUSTIFY", 40, -9, 0, 3, 160, 0, None),        # ·
    "quote": ("JUSTIFY", 24, 0, 2, 8, 150, 0, None),
    "center": ("CENTER", 0, 0, 0, 0, 160, 0, None),
    "right": ("RIGHT", 0, 0, 0, 0, 160, 0, None),
    "h1": ("CENTER", 0, 0, 0, 24, 160, 1, None),
    "h1top": ("CENTER", 0, 0, 0, 2, 160, 1, None),
    "h2": ("LEFT", 0, 0, 18, 10, 160, 1, None),
    "h3": ("LEFT", 0, 0, 12, 6, 160, 1, None),
    "h4": ("LEFT", 0, 0, 8, 4, 160, 1, None),
    "cap": ("CENTER", 0, 0, 10, 4, 140, 1, None),
    "capfig": ("CENTER", 0, 0, 4, 12, 140, 0, None),
    "note": ("LEFT", 0, 0, 2, 10, 130, 0, None),
    "tblc": ("CENTER", 0, 0, 0, 0, 130, 0, None),
    "tbll": ("LEFT", 0, 0, 0, 0, 130, 0, None),
    "tblj": ("JUSTIFY", 0, 0, 0, 0, 130, 0, None),
    "toc1": ("LEFT", 0, 0, 7, 1, 150, 0, "toc"),
    "toc2": ("LEFT", 12, 0, 0, 1, 150, 0, "toc"),
    "toc3": ("LEFT", 24, 0, 0, 1, 150, 0, "toc"),
    "fig": ("CENTER", 0, 0, 6, 2, 100, 1, None),
    "ref": ("JUSTIFY", 24, -24, 0, 5, 150, 0, None),
    "cover": ("CENTER", 0, 0, 0, 0, 150, 0, None),
    "boxp": ("JUSTIFY", 12, -12, 2, 6, 170, 0, None),
    "boxt": ("CENTER", 0, 0, 2, 10, 160, 0, None),
}

BF_TABLE, BF_HEAD, BF_BOX, BF_NONE, BF_SHADE, BF_TITLE = 3, 4, 5, 6, 7, 8


def pt(v):
    return int(round(v * 100))


def _border(tag, kind, width="0.12 mm", color="#000000"):
    return '<hh:%s type="%s" width="%s" color="%s"/>' % (tag, kind, width, color)


def _bf_xml(bid, sides, fill=None, width="0.12 mm"):
    l, r, t, b = sides
    x = ('<hh:borderFill xmlns:hh="%s" xmlns:hc="%s" id="%d" threeD="0" shadow="0" centerLine="NONE" breakCellSeparateLine="0">'
         '<hh:slash type="NONE" Crooked="0" isCounter="0"/><hh:backSlash type="NONE" Crooked="0" isCounter="0"/>'
         % (NS["hh"], NS["hc"], bid))
    x += _border("leftBorder", l, width) + _border("rightBorder", r, width)
    x += _border("topBorder", t, width) + _border("bottomBorder", b, width)
    x += '<hh:diagonal type="SOLID" width="0.1 mm" color="#000000"/>'
    if fill:
        x += '<hc:fillBrush><hc:winBrush faceColor="%s" hatchColor="#999999" alpha="0"/></hc:fillBrush>' % fill
    x += "</hh:borderFill>"
    return etree.fromstring(x)


def build_header(head):
    rl = head.find(HH + "refList")
    # fonts
    for ff in rl.find(HH + "fontfaces"):
        base = ff.findall(HH + "font")[-1]
        for i, name in enumerate(FONTS):
            f = copy.deepcopy(base)
            f.set("id", str(2 + i)); f.set("face", name)
            ff.append(f)
        ff.set("fontCnt", str(len(ff.findall(HH + "font"))))
    # border fills
    bfs = rl.find(HH + "borderFills")
    S = "SOLID"; N = "NONE"
    bfs.append(_bf_xml(BF_TABLE, (S, S, S, S)))
    bfs.append(_bf_xml(BF_HEAD, (S, S, S, S), "#DCE6F2"))
    bfs.append(_bf_xml(BF_BOX, (S, S, S, S), "#F2F2F2", "0.4 mm"))
    bfs.append(_bf_xml(BF_NONE, (N, N, N, N)))
    bfs.append(_bf_xml(BF_SHADE, (S, S, S, S), "#F2F2F2"))
    bfs.append(_bf_xml(BF_TITLE, (N, N, N, N), "#1F3864"))
    bfs.set("itemCnt", str(len(bfs)))
    # tab for toc
    tps = rl.find(HH + "tabProperties")
    tab = etree.SubElement(tps, HH + "tabPr", {"id": "3", "autoTabLeft": "0", "autoTabRight": "0"})
    sw = etree.SubElement(tab, HP + "switch")
    case = etree.SubElement(sw, HP + "case", {HP + "required-namespace": UCHAR})
    pos = TEXT_W - 200
    etree.SubElement(case, HH + "tabItem", {"pos": str(pos), "type": "RIGHT", "leader": "DOT", "unit": "HWPUNIT"})
    de = etree.SubElement(sw, HP + "default")
    etree.SubElement(de, HH + "tabItem", {"pos": str(pos * 2), "type": "RIGHT", "leader": "DOT"})
    tps.set("itemCnt", str(len(tps)))
    # char props
    cps = rl.find(HH + "charProperties")
    base = cps.find(HH + "charPr")
    cid = {}
    nid = len(cps)
    for key, (font, size, bold, color) in CHARS.items():
        c = copy.deepcopy(base)
        c.set("id", str(nid)); c.set("height", str(pt(size))); c.set("textColor", color)
        fr = c.find(HH + "fontRef")
        for a in fr.attrib:
            fr.set(a, str(font))
        if key in ("h1", "h2", "cover1", "cover2", "h1s", "boxt", "cover4"):
            sp = c.find(HH + "spacing")
            for a in sp.attrib:
                sp.set(a, "-3")
        if bold:
            off = c.find(HH + "offset")
            off.addnext(etree.Element(HH + "bold"))
        cps.append(c)
        cid[key] = nid
        nid += 1
    cps.set("itemCnt", str(len(cps)))
    # para props
    pps = rl.find(HH + "paraProperties")
    base = pps.find(HH + "paraPr")
    pid = {}
    nid = len(pps)
    for key, (align, left, ind, prev, nxt, ls, keep, tab) in PARAS.items():
        p = copy.deepcopy(base)
        p.set("id", str(nid))
        if tab == "toc":
            p.set("tabPrIDRef", "3")
        p.find(HH + "align").set("horizontal", align)
        bs = p.find(HH + "breakSetting")
        bs.set("keepWithNext", str(keep))
        bs.set("breakNonLatinWord", "KEEP_WORD")
        if key.startswith("h"):
            bs.set("keepLines", "1")
        sw = p.find(HP + "switch")
        for branch, mult in ((sw.find(HP + "case"), 1), (sw.find(HP + "default"), 2)):
            m = branch.find(HH + "margin")
            vals = {"intent": ind, "left": left, "right": 0, "prev": prev, "next": nxt}
            for k, v in vals.items():
                m.find(HC + k).set("value", str(pt(v) * mult))
            branch.find(HH + "lineSpacing").set("value", str(ls))
        pps.append(p)
        pid[key] = nid
        nid += 1
    pps.set("itemCnt", str(len(pps)))
    return cid, pid


def make_template():
    zin = zipfile.ZipFile(SKEL)
    out = io.BytesIO()
    zout = zipfile.ZipFile(out, "w")
    ids = None
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "Contents/header.xml":
            head = etree.fromstring(data)
            ids = build_header(head)
            data = etree.tostring(head, xml_declaration=True, encoding="UTF-8", standalone=True)
        zout.writestr(item, data)
    zout.close()
    return out.getvalue(), ids


_pid_counter = [1000]


def _new_id():
    _pid_counter[0] += 1
    return str(_pid_counter[0])


class Builder:
    def __init__(self):
        data, (self.cid, self.pid) = make_template()
        self.doc = HwpxDocument.open(io.BytesIO(data))
        self.sec = self.doc.sections[0]
        self._pending_break = False
        self.tbl_no = 0

    # ----- paragraphs
    def para(self, runs, style="body", page_break=False):
        """runs: str or list of (text, charkey)."""
        if isinstance(runs, str):
            runs = [(runs, None)]
        el = etree.SubElement(self.sec.element, HP + "p", {
            "id": _new_id(), "paraPrIDRef": str(self.pid[style]), "styleIDRef": "0",
            "pageBreak": "1" if (page_break or self._pending_break) else "0",
            "columnBreak": "0", "merged": "0"})
        self._pending_break = False
        self._fresh = False
        default_char = {"h1": "h1", "h1top": "h1", "h2": "h2", "h3": "h3", "h4": "h4", "cap": "cap",
                        "capfig": "cap", "note": "note", "tblc": "tbl", "tbll": "tbl", "tblj": "tbl",
                        "toc1": "toc1", "toc2": "toc2", "toc3": "toc3", "boxp": "boxb", "boxt": "boxt"}.get(style, "body")
        if not runs:
            runs = [("", None)]
        for text, ck in runs:
            self._run(el, text, ck or default_char)
        self.sec.mark_dirty()
        return el

    def _run(self, parent, text, ck):
        if getattr(self, "gothic", False) and ("g_" + ck) in self.cid:
            ck = "g_" + ck
        r = etree.SubElement(parent, HP + "run", {"charPrIDRef": str(self.cid[ck])})
        t = etree.SubElement(r, HP + "t")
        parts = text.split("\t")
        t.text = parts[0]
        for part in parts[1:]:
            tab = etree.SubElement(t, HP + "tab", {"width": "4000", "leader": "0", "type": "1"})
            tab.tail = part
        return r

    def page_break(self):
        if not getattr(self, "_fresh", False):
            self._pending_break = True

    def _margins(self, sec):
        sp = sec.element.find(".//" + HP + "secPr")
        m = sp.find(HP + "pagePr").find(HP + "margin")
        mm = lambda v: str(int(round(v * 283.465)))
        m.set("left", mm(30)); m.set("right", mm(30)); m.set("top", mm(20)); m.set("bottom", mm(15))
        m.set("header", mm(15)); m.set("footer", mm(12))
        return sp

    def new_main_section(self):
        self._margins(self.sec)
        sec = self.doc.add_section()
        self.sec = sec
        sp = self._margins(sec)
        sp.find(HP + "startNum").set("page", "1")
        self.doc.page.set_page_number(section=sec, prefix="- ", suffix=" -")
        self._pending_break = False
        self._fresh = True

    # ----- tables
    def table(self, rows, widths=None, header_rows=1, aligns=None, merges=(), font="tbl",
              row_shade=(), cell_bf=None, para_style=None, repeat=True, margin=(510, 141)):
        nrows = len(rows); ncols = max(len(r) for r in rows)
        if widths is None:
            widths = [1] * ncols
        tot = sum(widths)
        cw = [int(TEXT_W * w / tot) for w in widths]
        cw[-1] += TEXT_W - sum(cw)
        anchor = etree.SubElement(self.sec.element, HP + "p", {
            "id": _new_id(), "paraPrIDRef": str(self.pid["tblc"]), "styleIDRef": "0",
            "pageBreak": "1" if self._pending_break else "0", "columnBreak": "0", "merged": "0"})
        self._pending_break = False
        self._fresh = False
        run = etree.SubElement(anchor, HP + "run", {"charPrIDRef": str(self.cid["tbl"])})
        tbl = etree.SubElement(run, HP + "tbl", {
            "id": _new_id(), "zOrder": "0", "numberingType": "TABLE", "textWrap": "TOP_AND_BOTTOM",
            "textFlow": "BOTH_SIDES", "lock": "0", "dropcapstyle": "None", "pageBreak": "CELL",
            "repeatHeader": "1" if (repeat and header_rows) else "0", "rowCnt": str(nrows), "colCnt": str(ncols),
            "cellSpacing": "0", "borderFillIDRef": str(BF_TABLE), "noAdjust": "0"})
        rowh = 1800
        etree.SubElement(tbl, HP + "sz", {"width": str(TEXT_W), "widthRelTo": "ABSOLUTE",
                                          "height": str(rowh * nrows), "heightRelTo": "ABSOLUTE", "protect": "0"})
        etree.SubElement(tbl, HP + "pos", {"treatAsChar": "1", "affectLSpacing": "0", "flowWithText": "1",
                                           "allowOverlap": "0", "holdAnchorAndSO": "0", "vertRelTo": "PARA",
                                           "horzRelTo": "COLUMN", "vertAlign": "TOP", "horzAlign": "LEFT",
                                           "vertOffset": "0", "horzOffset": "0"})
        etree.SubElement(tbl, HP + "outMargin", {"left": "0", "right": "0", "top": "0", "bottom": "0"})
        etree.SubElement(tbl, HP + "inMargin", {"left": str(margin[0]), "right": str(margin[0]), "top": str(margin[1]), "bottom": str(margin[1])})
        # merges: list of (r, c, rowspan, colspan)
        covered = set(); spans = {}
        for (r0, c0, rs, cs) in merges:
            spans[(r0, c0)] = (rs, cs)
            for rr in range(r0, r0 + rs):
                for cc in range(c0, c0 + cs):
                    if (rr, cc) != (r0, c0):
                        covered.add((rr, cc))
        for r in range(nrows):
            tr = etree.SubElement(tbl, HP + "tr")
            for c in range(ncols):
                if (r, c) in covered:
                    continue
                rs, cs = spans.get((r, c), (1, 1))
                is_head = r < header_rows
                bf = BF_HEAD if is_head else (BF_SHADE if r in row_shade else BF_TABLE)
                if cell_bf and (r, c) in cell_bf:
                    bf = cell_bf[(r, c)]
                tc = etree.SubElement(tr, HP + "tc", {"name": "", "header": "1" if is_head else "0",
                                                      "hasMargin": "1" if margin != (510, 141) else "0", "protect": "0", "editable": "0",
                                                      "dirty": "1", "borderFillIDRef": str(bf)})
                sub = etree.SubElement(tc, HP + "subList", {
                    "id": "", "textDirection": "HORIZONTAL", "lineWrap": "BREAK", "vertAlign": "CENTER",
                    "linkListIDRef": "0", "linkListNextIDRef": "0", "textWidth": "0", "textHeight": "0",
                    "hasTextRef": "0", "hasNumRef": "0"})
                txt = rows[r][c] if c < len(rows[r]) else ""
                if isinstance(txt, list):
                    for pst2, runs2 in txt:
                        p = etree.SubElement(sub, HP + "p", {"id": _new_id(), "paraPrIDRef": str(self.pid[pst2]),
                                                             "styleIDRef": "0", "pageBreak": "0",
                                                             "columnBreak": "0", "merged": "0"})
                        for t2, k2 in runs2:
                            self._run(p, t2, k2)
                    txt = None
                al = "c" if is_head else ((aligns[c] if aligns else "c"))
                pst = para_style or {"c": "tblc", "l": "tbll", "j": "tblj"}[al]
                for line in ([] if txt is None else str(txt).split("\n")):
                    p = etree.SubElement(sub, HP + "p", {"id": _new_id(), "paraPrIDRef": str(self.pid[pst]),
                                                         "styleIDRef": "0", "pageBreak": "0",
                                                         "columnBreak": "0", "merged": "0"})
                    ck = (font + "b") if is_head and font + "b" in self.cid else font
                    for seg_text, seg_red in split_marks(line):
                        k = ck
                        if seg_red:
                            k = "tblred" if font == "tbl" else "notered"
                        if seg_text.startswith("**") and seg_text.endswith("**") and len(seg_text) > 4:
                            seg_text = seg_text[2:-2]; k = font + "b" if font + "b" in self.cid else k
                        self._run(p, seg_text, k)
                etree.SubElement(tc, HP + "cellAddr", {"colAddr": str(c), "rowAddr": str(r)})
                etree.SubElement(tc, HP + "cellSpan", {"colSpan": str(cs), "rowSpan": str(rs)})
                w = sum(cw[c:c + cs])
                etree.SubElement(tc, HP + "cellSz", {"width": str(w), "height": str(rowh * rs)})
                etree.SubElement(tc, HP + "cellMargin", {"left": str(margin[0]), "right": str(margin[0]), "top": str(margin[1]), "bottom": str(margin[1])})
        self.sec.mark_dirty()
        return tbl

    def box(self, paras):
        """paras: list of (parastyle, runs). One-cell shaded box."""
        old = getattr(self, "gothic", False)
        self.gothic = True
        t = self.table([[paras]], widths=[1], header_rows=0, cell_bf={(0, 0): BF_BOX}, repeat=False, margin=(1700, 1100))
        self.gothic = old
        return t

    # ----- pictures
    def picture(self, path, width_mm, height_mm=None):
        from PIL import Image
        im = Image.open(path)
        if height_mm is None:
            height_mm = width_mm * im.height / im.width
        data = open(path, "rb").read()
        fmt = path.rsplit(".", 1)[1].lower()
        if self._pending_break:
            self.para("", "center")  # carrier for break
        obj = self.doc.add_picture(data, fmt, width_mm=width_mm, height_mm=height_mm, align="CENTER",
                                   para_pr_id_ref=self.pid["fig"])
        return obj

    def save(self, path_hwpx, path_hwp=None):
        self.doc.save_to_path(path_hwpx)
        _fix_manifest(path_hwpx)
        if path_hwp:
            d2 = HwpxDocument.open(path_hwpx)
            d2.save_to_path(path_hwp)


def split_marks(line):
    """Split text on 【...】 markers: returns (text, is_red) segments (markers kept)."""
    out = []; i = 0
    while i < len(line):
        a = line.find("【", i)
        if a < 0:
            out.append((line[i:], False)); break
        b = line.find("】", a)
        if b < 0:
            out.append((line[i:], False)); break
        if a > i:
            out.append((line[i:a], False))
        out.append((line[a:b + 1], True))
        i = b + 1
    return out or [("", False)]


def _fix_manifest(path):
    """Register every BinData part in content.hpf (python-hwpx drops some after add_section)."""
    import shutil, os, re as _re
    zin = zipfile.ZipFile(path)
    hpf = zin.read("Contents/content.hpf").decode("utf-8")
    bins = [n for n in zin.namelist() if n.startswith("BinData/")]
    add = ""
    for b in bins:
        if 'href="%s"' % b in hpf:
            continue
        iid = os.path.splitext(os.path.basename(b))[0]
        ext = b.rsplit(".", 1)[1].lower()
        mt = {"png": "image/png", "jpg": "image/jpg", "jpeg": "image/jpg"}.get(ext, "image/" + ext)
        add += '<opf:item id="%s" href="%s" media-type="%s" isEmbeded="1" />' % (iid, b, mt)
    if not add:
        return
    hpf = hpf.replace("</opf:manifest>", add + "</opf:manifest>")
    tmp = path + ".tmp"
    zout = zipfile.ZipFile(tmp, "w")
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "Contents/content.hpf":
            data = hpf.encode("utf-8")
        zout.writestr(item, data)
    zout.close(); zin.close()
    shutil.move(tmp, path)
