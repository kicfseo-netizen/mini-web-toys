# Figures for the report (matplotlib, Nanum fonts).
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.font_manager as fm

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figs")
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False
NAVY = "#1F3864"; BLUE = "#2E75B6"; LIGHT = "#DCE6F2"; PALE = "#EEF3FA"; ORANGE = "#C55A11"
GRAY = "#7F7F7F"; LGRAY = "#F2F2F2"; GREEN = "#548235"; LGREEN = "#E2EFDA"; LORANGE = "#FBE5D6"
BOLD = "NanumGothic"


def canvas(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w * 10); ax.set_ylim(0, h * 10); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc=LIGHT, ec=NAVY, tc="black", fs=11, bold=False, r=0.8, lw=1.2, ha="center"):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=%s" % r, fc=fc, ec=ec, lw=lw)
    ax.add_patch(p)
    tx = x + w / 2 if ha == "center" else x + 1.2
    ax.text(tx, y + h / 2, text, ha=ha, va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", linespacing=1.45)


def arrow(ax, x1, y1, x2, y2, c=GRAY, lw=1.6, style="-|>", ms=14, ls="-"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms, color=c, lw=lw, linestyle=ls)
    ax.add_patch(a)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, facecolor="white")
    plt.close(fig)


def f_flow():
    fig, ax = canvas(10, 6.6)
    steps = [("문제 제기", "대덕특구 기업의\n연구개발·전문인력 부족"),
             ("이론·선행연구", "고숙련 이주·혁신클러스터\n유학생 정주 결정요인"),
             ("현황 진단", "특구 기업·외국인 인재 통계\n선행보고서 설문 재분석"),
             ("수요·장애요인", "기업 심층인터뷰\n대학·지원기관 의견수렴"),
             ("사례 분석", "국내 타 지역\n해외 혁신클러스터"),
             ("전략 도출", "비전·추진전략·과제\n로드맵·성과지표")]
    for i, (t, d) in enumerate(steps):
        y = 54 - i * 9
        box(ax, 4, y, 22, 7, t, fc=NAVY, ec=NAVY, tc="white", fs=12, bold=True)
        box(ax, 29, y, 40, 7, d, fc=PALE, ec=BLUE, fs=10.5)
        if i < len(steps) - 1:
            arrow(ax, 15, y, 15, y - 2)
    meth = ["문헌·정책 조사", "통계·2차 자료 분석", "선행보고서 설문 재분석", "심층인터뷰·의견수렴", "국내외 벤치마킹", "전문가 자문·검토"]
    ax.text(85, 62.3, "주요 연구 방법", ha="center", fontsize=12, fontweight="bold", color=NAVY)
    for i, t in enumerate(meth):
        y = 54 - i * 9
        box(ax, 73, y, 24, 7, t, fc=LGRAY, ec=GRAY, fs=10.5)
        arrow(ax, 69.2, y + 3.5, 72.8, y + 3.5, c="#BFBFBF", lw=1, style="<|-|>", ms=8)
    save(fig, "f1_flow.png")


def f_pushpull():
    fig, ax = canvas(10, 4.6)
    box(ax, 2, 10, 26, 28, "출신국(배출 요인)\n\n· 낮은 임금·연구 기회\n· 연구 인프라 부족\n· 정치·경제 불안\n· 일자리 부족", fc=LORANGE, ec=ORANGE, fs=10.5)
    box(ax, 72, 10, 26, 28, "대덕특구(흡인 요인)\n\n· 연구·고용 기회\n· 첨단 연구 인프라\n· 장학·연구비 지원\n· 정주·체류 안정성", fc=LIGHT, ec=NAVY, fs=10.5)
    box(ax, 36, 14, 28, 20, "중간 장애요인\n\n· 체류자격·비자 요건\n· 언어·문화 장벽\n· 정보 비대칭\n· 이동·정착 비용", fc=LGRAY, ec=GRAY, fs=10.5)
    arrow(ax, 28.5, 24, 35.5, 24, c=ORANGE, lw=2.2)
    arrow(ax, 64.5, 24, 71.5, 24, c=NAVY, lw=2.2)
    ax.text(50, 41, "개인 요인: 연령·전공·학위·가족·네트워크·경력 목표", ha="center", fontsize=10.5, color=NAVY)
    ax.text(50, 5, "※ Lee(1966: 50)의 이동 결정요인 4범주를 외국인 과학기술 인재에 적용하여 연구진 재구성", ha="center", fontsize=9, color=GRAY)
    save(fig, "f2_pushpull.png")


def f_framework():
    fig, ax = canvas(10, 6.4)
    box(ax, 3, 52, 94, 9, "대덕특구 기업경쟁력 제고를 위한 외국인 인재 활용 전략", fc=NAVY, ec=NAVY, tc="white", fs=13, bold=True)
    cols = [("수요 측(기업)", "· 인력 부족 직무·분야\n· 채용 의향·조건\n· 수용 역량(HR·언어)\n· 채용 애로요인", LIGHT, NAVY),
            ("공급 측(외국인 인재)", "· 전공·학위·연구역량\n· 취업·정주 의향\n· 희망 직무·처우\n· 정보 접근성", LGREEN, GREEN),
            ("제도·지역 환경", "· 체류자격·비자\n· 대학·지원기관 연계\n· 정주 여건(주거·교육)\n· 지역 산업생태계", LORANGE, ORANGE)]
    for i, (t, d, fc, ec) in enumerate(cols):
        x = 3 + i * 32
        box(ax, x, 41, 30, 7, t, fc=ec, ec=ec, tc="white", fs=11.5, bold=True)
        box(ax, x, 22, 30, 18, d, fc=fc, ec=ec, fs=10.5)
        arrow(ax, x + 15, 21.5, 50 if i == 1 else (x + 15 + (50 - x - 15) * 0.5), 17.5)
    box(ax, 15, 9, 70, 8, "매칭 갭(Gap) 진단 → 전략·과제 도출 → 실행체계·성과지표", fc=PALE, ec=BLUE, fs=11.5, bold=True)
    box(ax, 15, 1, 70, 6, "분석 자료: 통계·문헌 / 선행보고서 설문 재분석 / 심층인터뷰 / 국내외 사례", fc=LGRAY, ec=GRAY, fs=10)
    save(fig, "f3_framework.png")


def f_visa():
    fig, ax = canvas(10, 4.4)
    nodes = [("D-2\n유학", 2), ("D-10\n구직", 21), ("E-7 / E-3\n전문·연구", 40), ("F-2-7 / F-2-R\n거주", 59), ("F-5\n영주", 78)]
    for t, x in nodes:
        box(ax, x, 22, 17, 12, t, fc=NAVY if x in (40,) else LIGHT, ec=NAVY, tc="white" if x == 40 else "black", fs=11, bold=True)
    for (a, xa), (b, xb) in zip(nodes, nodes[1:]):
        arrow(ax, xa + 17.3, 28, xb - 0.3, 28, c=NAVY, lw=2)
    arrow(ax, 10.5, 21.8, 48.5, 21.8, c=ORANGE, lw=1.6, style="-|>", ls="--")
    ax.text(29, 16.2, "졸업 즉시 취업(D-2→E-7 직접 변경)", ha="center", fontsize=9.5, color=ORANGE)
    arrow(ax, 10.5, 34.2, 67.5, 34.2, c=GREEN, lw=1.6, style="-|>", ls="--")
    ax.text(39, 37.3, "지역특화형 비자(F-2-R): 인구감소지역 취업·거주 요건 충족 시", ha="center", fontsize=9.5, color=GREEN)
    ax.text(50, 6.5, "탑티어 비자·K-Tech Pass: 해외 최상위 인재 → 거주(F-2) 즉시 부여, 3년 후 영주 가능", ha="center", fontsize=10, color=NAVY)
    ax.text(50, 2, "※ 법무부 체류자격 체계를 바탕으로 연구진 작성(세부 요건은 법무부 고시에 따름)", ha="center", fontsize=8.5, color=GRAY)
    save(fig, "f4_visa.png")


def f_sales():
    fig, ax1 = plt.subplots(figsize=(8, 4))
    yrs = ["2005", "2020", "2023", "2024"]
    sales = [2.57, 19.28, 26.69, 27.51]
    b = ax1.bar(yrs, sales, color=[LIGHT, BLUE, BLUE, NAVY], width=0.55, edgecolor=NAVY)
    for r, v in zip(b, sales):
        ax1.text(r.get_x() + r.get_width() / 2, v + 0.5, "%.1f조원" % v, ha="center", fontsize=10)
    ax1.set_ylabel("입주기업 매출액(조원)")
    ax1.set_ylim(0, 32)
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.set_title("대덕특구 입주기업 매출액 추이", fontsize=12)
    fig.text(0.01, 0.01, "주: 2005년은 2023년 매출이 2005년 대비 10.4배라는 재단 공표치로 역산한 추정값", fontsize=8, color=GRAY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "f5_sales.png")


def f_students():
    yrs = list(range(2015, 2026))
    v = [91332, 104262, 123858, 142205, 160165, 153695, 152281, 166892, 181842, 208962, 253434]
    fig, ax = plt.subplots(figsize=(8.5, 4))
    ax.plot(yrs, [x / 10000 for x in v], marker="o", color=NAVY, lw=2.2)
    ax.fill_between(yrs, [x / 10000 for x in v], color=LIGHT, alpha=0.6)
    for x, y in zip(yrs, v):
        ax.text(x, y / 10000 + 0.6, "%.1f" % (y / 10000), ha="center", fontsize=9)
    ax.set_ylabel("외국인 유학생 수(만 명)")
    ax.set_xticks(yrs)
    ax.set_ylim(0, 29)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("국내 고등교육기관 외국인 유학생 추이(각 연도 4월 1일 기준)", fontsize=12)
    fig.tight_layout()
    save(fig, "f6_students.png")


def f_daejeon():
    gu = ["유성구", "동구", "서구", "대덕구", "중구"]
    v = [10045, 8108, 6855, 4083, 2231]
    fig, ax = plt.subplots(figsize=(8, 3.8))
    b = ax.barh(gu[::-1], v[::-1], color=[LIGHT, LIGHT, BLUE, BLUE, NAVY], edgecolor=NAVY)
    for r, x in zip(b, v[::-1]):
        ax.text(x + 150, r.get_y() + r.get_height() / 2, "{:,}명 ({:.1f}%)".format(x, x / 31322 * 100), va="center", fontsize=10)
    ax.set_xlim(0, 13000)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlabel("외국인주민 수(명)")
    ax.set_title("대전광역시 자치구별 외국인주민 분포(총 31,322명)", fontsize=12)
    fig.tight_layout()
    save(fig, "f7_daejeon.png")


def f_d10():
    fig, ax = plt.subplots(figsize=(8, 3.8))
    import numpy as np
    x = np.arange(2); w = 0.35
    a = [1528, 3090]; b2 = [499, 599]
    r1 = ax.bar(x - w / 2, a, w, label="D-10(구직) → E-7 변경 허가", color=NAVY)
    r2 = ax.bar(x + w / 2, b2, w, label="D-2(유학) → E-7 직접 변경 허가", color=BLUE)
    for rs in (r1, r2):
        for r in rs:
            ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 50, "{:,}".format(int(r.get_height())), ha="center", fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels(["2021년", "2025년"])
    ax.set_ylim(0, 3700); ax.legend(frameon=False, fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylabel("허가 건수")
    ax.set_title("유학생 출신 외국인의 전문인력(E-7) 체류자격 변경 허가 추이", fontsize=12)
    fig.tight_layout()
    save(fig, "f8_d10.png")


def f_swot():
    fig, ax = canvas(10, 6.6)
    q = [("S  강점(Strengths)", "· 출연연·KAIST 등 세계적 연구 인프라 집적\n· 딥테크·연구소기업 중심 기술기반 기업군\n· 지역 대학의 이공계 외국인 석·박사 풀\n· 글로벌 인재 비자센터 등 지원 기반", 3, 34, LIGHT, NAVY),
         ("W  약점(Weaknesses)", "· 중소·벤처 중심의 낮은 임금·인지도\n· 외국인 채용 경험·HR 역량 부족\n· 한국어 중심 업무환경\n· 대학–기업 간 외국인 인재 정보 단절", 51, 34, LORANGE, ORANGE),
         ("O  기회(Opportunities)", "· 외국인 유학생 25만 명 시대·이공계 비중 확대\n· 탑티어 비자·K-Tech Pass 등 제도 개선\n· 지역특화형 비자·RISE 등 지역 주도 정책\n· 딥테크 기업의 해외 진출 수요 확대", 3, 2, LGREEN, GREEN),
         ("T  위협(Threats)", "· 수도권·해외로의 인재 유출\n· 주요국의 글로벌 인재 유치 경쟁 심화\n· 비자·체류 제도의 잦은 변경과 복잡성\n· 정착 지원 인프라(주거·교육) 부족", 51, 2, LGRAY, GRAY)]
    for t, d, x, y, fc, ec in q:
        box(ax, x, y, 46, 30, "", fc=fc, ec=ec, lw=1.6)
        ax.text(x + 2, y + 26.5, t, fontsize=12.5, fontweight="bold", color=ec, va="center")
        ax.text(x + 2, y + 12.5, d, fontsize=10.5, va="center", linespacing=1.6)
    save(fig, "f9_swot.png")


def f_barriers():
    fig, ax = canvas(10, 5.6)
    box(ax, 36, 22, 28, 12, "외국인 인재\n채용·정착의 장애", fc=NAVY, ec=NAVY, tc="white", fs=12.5, bold=True)
    items = [("기업 측", "· 비자·행정 절차 부담\n· 한국어 소통·조직문화\n· 인건비·이직 위험\n· 외국인 HR 경험 부족", 2, 34, LIGHT, NAVY),
             ("인재 측", "· 기업·직무 정보 부족\n· 처우·경력 전망 불확실\n· 한국어 능력 제약\n· 가족 동반·정주 부담", 66, 34, LGREEN, GREEN),
             ("제도 측", "· E-7 요건(임금·직무·전공)\n· D-10 기간 및 전환 요건\n· 부처별 분절된 지원사업\n· 제도 정보의 낮은 접근성", 2, 2, LORANGE, ORANGE),
             ("지역 측", "· 대학별 개별 취업지원\n· 특구–대학 연계 플랫폼 부재\n· 주거·자녀교육·의료 인프라\n· 외국인 커뮤니티 기반 약함", 66, 2, LGRAY, GRAY)]
    for t, d, x, y, fc, ec in items:
        box(ax, x, y, 32, 20, "", fc=fc, ec=ec)
        ax.text(x + 16, y + 17, t, ha="center", fontsize=12, fontweight="bold", color=ec)
        ax.text(x + 2, y + 7.5, d, fontsize=10.2, va="center", linespacing=1.55)
        cx = x + 32 if x < 50 else x
        cy = y + 10
        arrow(ax, cx, cy, 36 if x < 50 else 64, 28, c=ec, lw=1.8)
    save(fig, "f10_barriers.png")


def f_bench():
    fig, ax = plt.subplots(figsize=(8, 5.2))
    pts = {"미국": (8.4, 4.3), "캐나다": (7.5, 7.5), "독일": (6.8, 6.5), "네덜란드": (7.2, 8.0), "일본": (6.0, 5.5),
           "싱가포르": (8.8, 5.0), "대만": (7.0, 6.0), "영국": (7.8, 5.2), "한국(현재)": (5.0, 4.0), "대덕특구(목표)": (8.3, 9.2)}
    for k, (x, y) in pts.items():
        c = ORANGE if "대덕" in k else (GRAY if "한국" in k else NAVY)
        ax.scatter(x, y, s=260 if "대덕" in k else 140, color=c, alpha=0.85, edgecolor="white", zorder=3)
        ax.text(x + 0.15, y + 0.2, k, fontsize=10.5, color=c, fontweight="bold" if "대덕" in k else "normal")
    ax.annotate("", xy=(8.2, 9.05), xytext=(5.1, 4.15), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.5, ls="--"))
    ax.axhline(6, color="#D9D9D9", lw=1); ax.axvline(6.5, color="#D9D9D9", lw=1)
    ax.set_xlim(3, 10); ax.set_ylim(2, 10)
    ax.set_xlabel("유치 개방성(비자 신속성·요건 유연성)  →", fontsize=11)
    ax.set_ylabel("정착·활용 지원(매칭·정주·통합)  →", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("주요국 고숙련 인재 정책의 상대적 포지셔닝(개념도)", fontsize=12)
    fig.text(0.01, 0.01, "주: 제6장 사례 검토를 바탕으로 연구진이 정성적으로 배치한 개념도이며 계량 지표가 아님", fontsize=8, color=GRAY)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, "f11_bench.png")


def f_vision():
    fig, ax = canvas(10, 8.2)
    box(ax, 3, 72, 94, 9, "비전 : 글로벌 인재가 머물고 성장하는 대덕, 세계로 뻗는 특구 기업", fc=NAVY, ec=NAVY, tc="white", fs=13.5, bold=True)
    box(ax, 3, 61, 94, 9, "목표('31) : 지역 대학 외국인 석·박사 특구기업 취업 연 100명 / 외국인 인재 채용기업 누적 200개사 / 1년 정착률 80%", fc=PALE, ec=BLUE, fs=11, bold=True)
    strat = [("전략 1", "연결", "대학–기업\n인재매칭 플랫폼"), ("전략 2", "채용", "체류·채용\n원스톱 지원"),
             ("전략 3", "수용", "기업 수용역량\n강화"), ("전략 4", "정착", "정주·커뮤니티\n여건 개선"),
             ("전략 5", "확장", "글로벌 진출\n연계 활용"), ("전략 6", "기반", "협력 거버넌스\n·데이터")]
    w = 15
    for i, (a, b, c) in enumerate(strat):
        x = 3 + i * (w + 0.8)
        box(ax, x, 49, w, 9, a + "\n" + b, fc=BLUE, ec=BLUE, tc="white", fs=11, bold=True)
        box(ax, x, 36, w, 12, c, fc=LIGHT, ec=BLUE, fs=10.5, bold=True)
    tasks = ["· 대덕 글로벌\n 인재허브 구축\n· 통합 DB·잡매칭\n· 산학 프로젝트\n· 인턴십·잡페어",
             "· 비자 컨설팅\n 데스크\n· 지역특화형 비자\n 대전 참여\n· E-7 특례 건의",
             "· 외국인 채용\n HR 컨설팅\n· 초기 인건비\n 매칭 지원\n· 영어 업무환경",
             "· 주거·의료·\n 자녀교육 지원\n· 가족 정착\n· 커뮤니티센터\n· 한국어 교육",
             "· 출신국 시장\n 진출 연계\n· 글로벌 BD\n 인재 활용\n· 동문 네트워크",
             "· 특구 외국인\n 인재협의체\n· 성과지표·통계\n· 중앙정부\n 제도 건의"]
    for i, t in enumerate(tasks):
        x = 3 + i * (w + 0.8)
        box(ax, x, 7, w, 28, t, fc="white", ec="#BFBFBF", fs=9.6, ha="left", r=0.5)
    box(ax, 3, 0.5, 94, 5, "추진 원칙 : 수요 기반 · 전주기 연계 · 지역 주도 · 성과 관리", fc=LGRAY, ec=GRAY, fs=10.5, bold=True)
    save(fig, "f12_vision.png")


def f_lifecycle():
    fig, ax = canvas(10, 6.4)
    import math
    stages = [("유치", "해외 홍보·장학\n공동학위"), ("학업", "산학 연구과제\n한국어·직무교육"), ("매칭", "인재DB·잡페어\n인턴십"),
              ("채용", "비자 컨설팅\n인건비 지원"), ("정착", "주거·가족\n커뮤니티"), ("성장·순환", "경력개발·창업\n글로벌 네트워크")]
    cx, cy, R = 50, 32, 22
    for i, (t, d) in enumerate(stages):
        ang = math.pi / 2 - i * 2 * math.pi / 6
        x = cx + R * 1.45 * math.cos(ang); y = cy + R * math.sin(ang)
        c = Circle((x, y), 7.3, fc=NAVY if i % 2 == 0 else BLUE, ec="white", lw=2)
        ax.add_patch(c)
        ax.text(x, y, t, ha="center", va="center", color="white", fontsize=12, fontweight="bold")
        dx = 14.5 if math.cos(ang) > 0.1 else (-14.5 if math.cos(ang) < -0.1 else 0)
        dy = 0
        if not dx:
            dx = 16
        ax.text(x + dx, y + dy, d, ha="center", va="center", fontsize=9.5, color="black", linespacing=1.4)
        ang2 = math.pi / 2 - (i + 0.5) * 2 * math.pi / 6
    for i in range(6):
        a1 = math.pi / 2 - i * 2 * math.pi / 6 - 0.33
        a2 = math.pi / 2 - (i + 1) * 2 * math.pi / 6 + 0.33
        arrow(ax, cx + R * 1.45 * math.cos(a1), cy + R * math.sin(a1), cx + R * 1.45 * math.cos(a2), cy + R * math.sin(a2), c=GRAY, lw=1.6)
    ax.text(cx, cy + 1.5, "대덕특구\n외국인 인재\n전주기 지원", ha="center", va="center", fontsize=12.5, fontweight="bold", color=NAVY)
    save(fig, "f13_lifecycle.png")


def f_hub():
    fig, ax = canvas(10, 6.6)
    box(ax, 33, 26, 34, 15, "대덕 글로벌 인재허브\n(Daedeok Global Talent Hub)\n\n인재DB · 매칭 · 비자상담 · 정착지원", fc=NAVY, ec=NAVY, tc="white", fs=11, bold=True)
    actors = [("지역 대학\nKAIST·UST·충남대·한밭대", 3, 52, "외국인 석·박사 인재 정보\n산학 프로젝트"),
              ("특구 기업\n연구소기업·첨단기술기업", 67, 52, "채용 수요·직무 등록\n인턴십·공동연구"),
              ("정부출연연구기관", 3, 4, "연구 인턴·박사후연구원\n기술이전 연계"),
              ("법무부·대전출입국\n글로벌 인재 비자센터", 67, 4, "체류자격 상담\n지역특화형 비자"),
              ("대전시·특구재단", 35, 52, "예산·사업 총괄\n정주 인프라"),
              ("외국인 커뮤니티\n·동문 네트워크", 35, 2, "멘토링·생활정보\n해외 네트워크")]
    for t, x, y, d in actors:
        box(ax, x, y, 30, 10, t, fc=LIGHT, ec=BLUE, fs=10.3, bold=True)
        ty = y - 3 if y > 30 else y + 13
        ax.text(x + 15, ty, d, ha="center", va="center", fontsize=9, color=GRAY, linespacing=1.3)
        sx = x + 15; sy = y if y > 30 else y + 10
        tx = 50 + (sx - 50) * 0.35; tyy = 41 if y > 30 else 26
        arrow(ax, sx, sy - (6 if y > 30 else -5), tx, tyy, c=BLUE, lw=1.5, style="<|-|>", ms=10)
    save(fig, "f14_hub.png")


def f_matching():
    fig, ax = canvas(10, 3.6)
    steps = [("① 수요 발굴", "기업 직무·역량\n수요 조사"), ("② 인재 풀 구축", "대학 추천·자기등록\n역량 프로파일"),
             ("③ 사전 연결", "산학 프로젝트\n단기 인턴십"), ("④ 채용 매칭", "잡페어·추천채용\n면접 지원"),
             ("⑤ 채용 후 관리", "비자·정착 지원\n6·12개월 점검")]
    for i, (t, d) in enumerate(steps):
        x = 1.5 + i * 19.6
        box(ax, x, 18, 17.5, 9, t, fc=NAVY, ec=NAVY, tc="white", fs=11, bold=True)
        box(ax, x, 4, 17.5, 12.5, d, fc=PALE, ec=BLUE, fs=10)
        if i < 4:
            arrow(ax, x + 17.7, 22.5, x + 19.4, 22.5, c=NAVY, lw=2)
    ax.text(50, 32, "데이터 환류: 매칭 성과·정착률을 인재DB와 사업 설계에 반영", ha="center", fontsize=10.5, color=ORANGE)
    save(fig, "f15_matching.png")


def f_onestop():
    fig, ax = canvas(10, 5)
    box(ax, 2, 18, 17, 14, "특구 기업\n채용 결정", fc=LIGHT, ec=NAVY, fs=11, bold=True)
    box(ax, 27, 30, 30, 14, "① 사전 진단\n직무·임금·전공 요건 확인\n(E-7/E-3/F-2-R 경로 판정)", fc=PALE, ec=BLUE, fs=9.8)
    box(ax, 27, 12, 30, 14, "② 서류 준비 대행·검토\n고용사유서·직무기술서\n추천서 발급(특구재단·대전시)", fc=PALE, ec=BLUE, fs=9.8)
    box(ax, 64, 21, 17, 14, "③ 체류자격\n변경 신청\n(비자센터)", fc=NAVY, ec=NAVY, tc="white", fs=10.5, bold=True)
    box(ax, 85, 21, 13, 14, "④ 정착\n연계", fc=LGREEN, ec=GREEN, fs=10.5, bold=True)
    arrow(ax, 19.3, 27, 26.7, 36, c=NAVY); arrow(ax, 42, 29.7, 42, 26.3, c=NAVY)
    arrow(ax, 57.3, 19, 63.7, 26, c=NAVY); arrow(ax, 81.3, 28, 84.7, 28, c=NAVY)
    box(ax, 2, 1, 96, 7, "목표 처리기간 : 상담 접수 후 4주 이내 체류자격 변경 신청 완료(서류 보완 포함)", fc=LGRAY, ec=GRAY, fs=10.5, bold=True)
    save(fig, "f16_onestop.png")


def f_gov():
    fig, ax = canvas(10, 6.4)
    box(ax, 25, 52, 50, 9, "대덕특구 외국인 인재 활용 협의체\n(공동위원장: 대전시 · 연구개발특구진흥재단)", fc=NAVY, ec=NAVY, tc="white", fs=11.5, bold=True)
    box(ax, 30, 38, 40, 9, "실무 사무국(대덕 글로벌 인재허브)", fc=BLUE, ec=BLUE, tc="white", fs=11, bold=True)
    arrow(ax, 50, 51.7, 50, 47.3, c=NAVY)
    groups = [("인재양성 분과", "KAIST·UST·충남대·\n한밭대 국제처·취업센터"),
              ("기업수요 분과", "특구 기업협회·\n연구소기업·벤처기업"),
              ("체류·제도 분과", "대전출입국·외국인사무소\n글로벌 인재 비자센터"),
              ("정주·생활 분과", "대전시 외국인 지원기관\n국제학교·의료기관")]
    for i, (t, d) in enumerate(groups):
        x = 2 + i * 24.5
        box(ax, x, 22, 22, 8, t, fc=LIGHT, ec=BLUE, fs=11, bold=True)
        box(ax, x, 9, 22, 12, d, fc="white", ec="#BFBFBF", fs=9.6)
        arrow(ax, 50, 37.7, x + 11, 30.3, c=GRAY, lw=1.2)
    box(ax, 2, 0.5, 96, 6.5, "중앙정부 연계: 과기정통부(특구·인재) · 법무부(체류) · 산업부(K-Tech Pass) · 교육부(유학생·RISE)", fc=LGRAY, ec=GRAY, fs=10)
    box(ax, 80, 52, 18, 9, "자문단\n(외국인 재직자·전문가)", fc=LORANGE, ec=ORANGE, fs=9.6)
    arrow(ax, 79.7, 56.5, 75.3, 56.5, c=ORANGE, style="<|-|>", ms=9)
    save(fig, "f17_gov.png")


def f_roadmap():
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    years = ["2027", "2028", "2029", "2030", "2031"]
    tasks = [("대덕 글로벌 인재허브 구축·운영", 0, 5, NAVY), ("외국인 인재 통합DB·매칭 플랫폼", 0, 5, NAVY),
             ("산학 프로젝트·인턴십 확대", 0.5, 4.5, NAVY), ("비자 컨설팅 데스크(원스톱)", 0, 5, BLUE),
             ("지역특화형 비자 대전 참여·특례 건의", 0.5, 2.5, BLUE), ("외국인 채용 HR 컨설팅", 0.5, 4.5, GREEN),
             ("초기 인건비 매칭 지원(시범→확대)", 1, 4, GREEN), ("정주 패키지(주거·교육·의료)", 1, 4, ORANGE),
             ("외국인 커뮤니티센터·동문망", 1.5, 3.5, ORANGE), ("글로벌 진출 연계 프로그램", 2, 3, GRAY),
             ("협의체·성과관리·통계 체계", 0, 5, GRAY)]
    for i, (t, s, d, c) in enumerate(tasks):
        ax.barh(i, d, left=s, color=c, alpha=0.85, height=0.55)
    ax.set_yticks(range(len(tasks))); ax.set_yticklabels([t[0] for t in tasks], fontsize=10)
    ax.invert_yaxis()
    ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5]); ax.set_xticklabels(years, fontsize=10.5)
    ax.set_xlim(0, 5)
    for x in range(1, 5):
        ax.axvline(x, color="#D9D9D9", lw=0.8)
    ax.axvspan(0, 1, color=LIGHT, alpha=0.35); ax.axvspan(1, 3, color=LGREEN, alpha=0.25); ax.axvspan(3, 5, color=LORANGE, alpha=0.25)
    ax.text(0.5, -1.2, "1단계: 기반 구축", ha="center", fontsize=10.5, fontweight="bold", color=NAVY)
    ax.text(2, -1.2, "2단계: 확산", ha="center", fontsize=10.5, fontweight="bold", color=GREEN)
    ax.text(4, -1.2, "3단계: 고도화·자립", ha="center", fontsize=10.5, fontweight="bold", color=ORANGE)
    ax.set_ylim(len(tasks) - 0.4, -1.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.tight_layout()
    save(fig, "f18_roadmap.png")


def f_cycle():
    fig, ax = canvas(10, 5.6)
    import math
    items = ["지역 대학의\n외국인 인재 양성", "특구 기업\n취업·채용", "기술혁신·\n해외시장 진출", "기업 성장·\n고용 확대", "지역경제 활성화·\n정주 매력 제고"]
    cx, cy = 50, 27; R = 20
    for i, t in enumerate(items):
        a = math.pi / 2 - i * 2 * math.pi / 5
        x = cx + 1.9 * R * math.cos(a); y = cy + R * math.sin(a)
        box(ax, x - 11, y - 5.5, 22, 11, t, fc=NAVY if i == 0 else LIGHT, ec=NAVY, tc="white" if i == 0 else "black", fs=10.5, bold=True)
    for i in range(5):
        a1 = math.pi / 2 - i * 2 * math.pi / 5 - 0.42; a2 = math.pi / 2 - (i + 1) * 2 * math.pi / 5 + 0.42
        arrow(ax, cx + 1.9 * R * math.cos(a1), cy + R * math.sin(a1), cx + 1.9 * R * math.cos(a2), cy + R * math.sin(a2), c=ORANGE, lw=2)
    ax.text(cx, cy, "외국인 인재\n선순환 구조", ha="center", va="center", fontsize=13, fontweight="bold", color=ORANGE)
    save(fig, "f19_cycle.png")


def f_retention():
    # conceptual policy-lever chart: stage drop-off (illustrative, placeholders)
    fig, ax = canvas(10, 4.2)
    stages = [("지역 대학 외국인\n이공계 석·박사 졸업", 96), ("국내 취업 희망", 80), ("특구 기업 인지", 58),
              ("지원·면접", 42), ("채용·정착", 28)]
    for i, (t, w) in enumerate(stages):
        x = 50 - w / 2; y = 34 - i * 7.6
        box(ax, x, y, w, 6.6, t.replace("\n", " "), fc=[NAVY, BLUE, "#5B9BD5", "#9DC3E6", LIGHT][i], ec="white",
            tc="white" if i < 3 else "black", fs=10.5, bold=True, r=0.3)
    ax.text(50, 1.2, "※ 단계별 이탈(누수) 구조를 나타낸 개념도로, 막대 길이는 실측 비율이 아님", ha="center", fontsize=8.8, color=GRAY)
    save(fig, "f20_funnel.png")


if __name__ == "__main__":
    for f in [f_flow, f_pushpull, f_framework, f_visa, f_sales, f_students, f_daejeon, f_d10, f_swot, f_barriers,
              f_bench, f_vision, f_lifecycle, f_hub, f_matching, f_onestop, f_gov, f_roadmap, f_cycle, f_retention]:
        f()
    print("ok")


def f_budget():
    import numpy as np
    yrs = ["2027", "2028", "2029", "2030", "2031"]
    data = {"전략1 연결": [6, 7, 7.5, 7.5, 7.5], "전략2 채용": [1.5] * 5, "전략3 수용": [2, 6, 8, 8, 8],
            "전략4 정착": [1.5, 5, 6, 6, 6], "전략5 확장": [0.5, 2, 3, 3.5, 3.5], "전략6 기반": [1] * 5}
    cols = [NAVY, BLUE, GREEN, ORANGE, "#BF9000", GRAY]
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    bottom = np.zeros(5)
    for (k, v), c in zip(data.items(), cols):
        ax.bar(yrs, v, bottom=bottom, color=c, label=k, width=0.55)
        bottom += np.array(v)
    for x, t in zip(yrs, bottom):
        ax.text(x, t + 0.4, "%.1f" % t, ha="center", fontsize=10, fontweight="bold")
    ax.set_ylabel("억 원"); ax.set_ylim(0, 33)
    ax.legend(ncol=3, frameon=False, fontsize=9.5, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("전략별 연차 소요 예산(개략 추정, 총 117억 원)", fontsize=12)
    fig.tight_layout(); save(fig, "f21_budget.png")


def f_kpi():
    fig, axes = plt.subplots(1, 3, figsize=(9.5, 3.4))
    items = [("특구기업 취업(명/년)", [50, 100]), ("채용기업 누적(개사)", [80, 200]), ("1년 정착률(%)", [70, 80])]
    for ax, (t, v) in zip(axes, items):
        b = ax.bar(["2028", "2031"], v, color=[BLUE, NAVY], width=0.55)
        for r, x in zip(b, v):
            ax.text(r.get_x() + r.get_width() / 2, x * 1.02, str(x), ha="center", fontsize=10.5, fontweight="bold")
        ax.set_title(t, fontsize=11); ax.set_ylim(0, max(v) * 1.25)
        ax.spines[["top", "right"]].set_visible(False); ax.set_yticks([])
    fig.suptitle("핵심 성과지표 목표", fontsize=12)
    fig.tight_layout(); save(fig, "f22_kpi.png")


def f_cotransfer():
    fig, ax = canvas(10, 4.6)
    box(ax, 2, 16, 24, 14, "정부출연연구기관\n\n기술 보유·연구과제\nUST 외국인 학생 연구 참여", fc=LIGHT, ec=NAVY, fs=10.3, bold=False)
    box(ax, 38, 16, 24, 14, "연구소기업·기술이전 기업\n\n기술 사업화\n인력 수요 발생", fc=PALE, ec=BLUE, fs=10.3)
    box(ax, 74, 16, 24, 14, "시장·해외 진출\n\n제품화·매출\n출신국 시장 연계", fc=LGREEN, ec=GREEN, fs=10.3)
    arrow(ax, 26.3, 26, 37.7, 26, c=NAVY, lw=2.2); ax.text(32, 28, "기술이전", ha="center", fontsize=10, color=NAVY)
    arrow(ax, 26.3, 20, 37.7, 20, c=ORANGE, lw=2.2); ax.text(32, 16.3, "인재 동반 이동", ha="center", fontsize=10, color=ORANGE)
    arrow(ax, 62.3, 23, 73.7, 23, c=GREEN, lw=2.2)
    box(ax, 20, 2, 60, 8, "인재허브: 매칭·비자(E-3/E-7/F-2)·정착 지원 / 특구재단: 연구소기업 지원 연계", fc=LGRAY, ec=GRAY, fs=10.3)
    ax.text(50, 41, "출연연–UST–연구소기업 '기술·인재 동반 이전' 모델", ha="center", fontsize=12.5, fontweight="bold", color=NAVY)
    save(fig, "f23_cotransfer.png")


def f_logic():
    fig, ax = canvas(10, 3.2)
    st = [("투입", "예산·인력\n협력기관"), ("활동", "매칭·비자\n컨설팅·정착"), ("산출", "DB 등록·매칭\n컨설팅 건수"), ("성과", "취업·채용기업\n1년 정착률"), ("영향", "기업 혁신·해외진출\n매출·고용 증가")]
    for i, (t, d) in enumerate(st):
        x = 1 + i * 19.8
        box(ax, x, 17, 17.5, 8, t, fc=[GRAY, BLUE, BLUE, NAVY, ORANGE][i], ec="white", tc="white", fs=12, bold=True)
        box(ax, x, 3, 17.5, 12.5, d, fc="white", ec="#BFBFBF", fs=10)
        if i < 4:
            arrow(ax, x + 17.7, 21, x + 19.6, 21, c=GRAY, lw=2)
    save(fig, "f24_logic.png")


if __name__ == "__main__":
    for f in [f_budget, f_kpi, f_cotransfer, f_logic]:
        f()
