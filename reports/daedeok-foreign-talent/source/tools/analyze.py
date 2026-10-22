import pickle, re, json, sys
from collections import Counter, OrderedDict
S = sys.argv[1]
hdr, R = pickle.load(open(S + "/survey.pkl", "rb"))
R = [r for k, r in enumerate(R) if not (k in (76, 209))]  # test entries
N = len(R)
out = OrderedDict(N=N)
def s(v): return "" if v is None else str(v).strip()
def pct(a, b): return round(100.0 * a / b, 1) if b else 0.0
def single(i, base=None):
    rows = [r for r in R if s(r[i])] if base is None else [r for r in base if s(r[i])]
    c = Counter(s(r[i]) for r in rows); n = len(rows)
    return n, [(k, v, pct(v, n)) for k, v in c.most_common()]
def num(v):
    v = s(v).replace(",", "")
    m = re.findall(r"[\d.]+", v)
    if not m: return None
    try: return float(m[0])
    except: return None
# A
out["A3"] = single(3); out["A6"] = single(7)
A7L = [("나노·반도체", ["나노, 반도체", "나노 · 반도체", "나노·반도체", "나노,반도체"]), ("바이오헬스", ["바이오헬스"]), ("우주항공", ["우주항공"]),
       ("국방", ["국방"]), ("양자", ["양자"]), ("로봇", ["로봇"]), ("제조", ["제조"]), ("건설·환경", ["건설 · 환경", "건설, 환경", "건설·환경", "건설•환경"])]
c = Counter(); other = 0; n7 = 0
for r in R:
    v = s(r[8])
    if not v: continue
    n7 += 1; rest = v
    for lab, alts in A7L:
        if any(a in v for a in alts):
            c[lab] += 1
            for a in alts: rest = rest.replace(a, "")
    if re.sub(r"[,\s·]", "", rest): c["기타(정보통신·원자력 등)"] += 1
out["A7"] = (n7, [(k, v, pct(v, n7)) for k, v in c.most_common()])
def bucket(vals, edges, labels):
    c = Counter()
    for x in vals:
        for e, l in zip(edges, labels):
            if x < e: c[l] += 1; break
    return c
sales = [num(r[4]) for r in R]; sales = [x for x in sales if x is not None]
sb = bucket(sales, [1000, 5000, 10000, 50000, 1e18], ["10억 미만", "10억∼50억 미만", "50억∼100억 미만", "100억∼500억 미만", "500억 이상"])
out["A4"] = (len(sales), [(l, sb[l], pct(sb[l], len(sales))) for l in ["10억 미만", "10억∼50억 미만", "50억∼100억 미만", "100억∼500억 미만", "500억 이상"]])
emp = [num(r[5]) for r in R]; emp = [x for x in emp if x is not None]
eb = bucket(emp, [5, 10, 30, 50, 1e18], ["5인 미만", "5∼9인", "10∼29인", "30∼49인", "50인 이상"])
out["A5"] = (len(emp), [(l, eb[l], pct(eb[l], len(emp))) for l in ["5인 미만", "5∼9인", "10∼29인", "30∼49인", "50인 이상"]])
fe = [num(r[6]) or 0 for r in R]
out["A5f"] = {"n": N, "employ": sum(1 for x in fe if x > 0), "total": sum(fe)}
out["emp_median"] = sorted(emp)[len(emp)//2]
# B1
out["B1"] = single(12)
B1yes = [r for r in R if s(r[12]).startswith("예")]
jobs = ["연구개발(R&D)", "홍보, 마케팅", "생산관리", "첨단제품생산", "해외영업, 판로개척", "기타"]
res = []
for j, i in zip(jobs, range(13, 19)):
    vals = [s(r[i]) for r in B1yes if s(r[i])]
    def nn(v):
        if "이상" in v: return 6.0
        if "~" in v: return 1.5
        return num(v) or 0
    tot = sum(nn(v) for v in vals)
    res.append((j, len(vals), pct(len(vals), len(B1yes)), round(tot)))
out["B1_1"] = (len(B1yes), res)
# B2
out["B2"] = single(19)
B2yes = [r for r in R if s(r[19]).startswith("예")]
c = Counter(); n = 0
for r in B2yes:
    v = s(r[20])
    if not v: continue
    n += 1
    for j in ["연구개발(R&D)", "홍보, 마케팅", "생산관리", "첨단제품생산", "해외영업, 판로개척"]:
        if j in v: c[j] += 1
    if re.sub(r"(연구개발\(R&D\)|홍보, 마케팅|생산관리|첨단제품생산|해외영업, 판로개척|[,\s])", "", v): c["기타"] += 1
out["B2_1"] = (n, [(k, v, pct(v, n)) for k, v in c.most_common()])
visas = ["기술연수(C-4)", "연구(E-3)", "기술지도(E-4)", "전문직업(E-5)", "특정활동(E-7)", "기타"]
vr = []
for v_, i in zip(visas, range(21, 27)):
    vals = [s(r[i]) for r in B2yes if s(r[i]) and "명" in s(r[i])]
    ppl = sum(6 if "이상" in v else (num(v) or 0) for v in vals)
    vr.append((v_, len(vals), int(ppl)))
out["B2_2"] = vr
out["B2_3"] = single(28, B2yes)
out["B3"] = single(29)
B3yes = [r for r in R if s(r[29]).startswith("예")]
B3no = [r for r in R if s(r[29]).startswith("아니오")]
def rank(cols, labels, base):
    resp = [r for r in base if any(s(r[i]) for i in cols)]
    n = len(resp); rows = []
    for lab, i in zip(labels, cols):
        firsts = sum(1 for r in resp if "1순위" in s(r[i]))
        any_ = sum(1 for r in resp if "순위" in s(r[i]))
        score = 0
        for r in resp:
            for k, w in (("1순위", 4), ("2순위", 3), ("3순위", 2), ("4순위", 1)):
                if k in s(r[i]): score += w; break
        rows.append((lab, firsts, pct(firsts, n), any_, pct(any_, n), score))
    rows.sort(key=lambda x: -x[5])
    return n, rows
out["C1"] = rank(range(30, 38), ["학위", "해당분야 유사경력", "한국어 능력", "영어 능력", "출신 국가", "급여 수준", "문화", "인성"], B3yes)
out["C2"] = rank(range(40, 45), ["지인 등 개인 네트워크", "대학 산학연계 프로그램", "채용박람회 등 대면 행사", "헤드헌팅·스카우팅", "온라인 채용플랫폼"], B3yes)
out["C3"] = single(47, B3yes)
out["C4"] = rank(range(48, 56), ["내국인 전문인력 채용의 어려움", "인건비 절감", "해외마케팅 강화", "기술개발 강화", "첨단제품 생산", "조직 외국어 역량 강화", "새로운 아이디어 발굴", "IT 개발인력 부족"], B3yes)
majors = ["반도체, 디스플레이", "이차전지", "첨단 모빌리티", "차세대 원자력", "첨단 바이오", "우주항공, 해양", "수소", "사이버보안", "인공지능", "차세대 통신", "첨단로봇, 제조", "양자", "경영", "IT, 컴퓨터사이언스"]
c = Counter(); n = 0
for r in B3yes:
    v = s(r[56])
    if not v: continue
    n += 1
    for m in majors:
        if m in v: c[m] += 1
out["C5"] = (n, [(k, v, pct(v, n)) for k, v in c.most_common()])
out["C6"] = single(57, B3yes)
diff = ["채용 절차 복잡·장기 소요", "정부 지원자금 부재", "인력 기초정보(전문성·배경) 확인 곤란", "언어 소통 장벽", "문화적 차이", "비자·고용계약 절차 정보 부족", "외국인 인력의 빠른 이탈"]
out["C7"] = rank(range(58, 65), diff, B3yes)
out["D1"] = rank(range(67, 74), diff, B3no)
out["D2"] = single(76, B3no)
# E1
c = Counter(); n = 0
for r in R:
    v = s(r[77])
    if not v: continue
    n += 1
    if "없음" in v: c["없음"] += 1
    for k in "12345":
        if k + "번" in v: c[k] += 1
out["E1"] = (n, [(k, v, pct(v, n)) for k, v in sorted(c.items())])
out["E2"] = rank(range(78, 85), ["구인구직 정보시스템 구축", "채용 절차 등 행정처리 간소화", "채용 인건비 지원", "재교육 교육훈련 시스템", "채용 상담회·박람회", "주거·생활·문화 정주여건 지원", "상시 채용 전문 코디네이터"], R)
out["E3"] = rank(range(87, 92), ["비자 발급 절차 간소화", "주거 및 생활 지원", "교육훈련 프로그램 지원", "세금 혜택", "문화적응 프로그램 지원"], R)
# cross tabs by A6 (in/out of Daedeok)
def yes(rows, i): 
    rr = [r for r in rows if s(r[i])]; return len(rr), sum(1 for r in rr if s(r[i]).startswith("예"))
xt = {}
for g, lab in (("예", "특구 내"), ("아니오", "특구 외")):
    grp = [r for r in R if s(r[7]).startswith(g)]
    xt[lab] = {"n": len(grp), "B1": yes(grp, 12), "B2": yes(grp, 19), "B3": yes(grp, 29), "lab": sum(1 for r in grp if s(r[3]) == "있음")}
out["xt"] = xt
xr = {}
for g in ("있음", "없음"):
    grp = [r for r in R if s(r[3]) == g]
    xr[g] = {"n": len(grp), "B1": yes(grp, 12), "B2": yes(grp, 19), "B3": yes(grp, 29)}
out["xr"] = xr
out["E4"] = [s(r[94]) for r in R if len(s(r[94])) > 15]
json.dump(out, open(S + "/stats.json", "w"), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(k, json.dumps(v, ensure_ascii=False)[:900])
