const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.APPLY_THEME_PATH || "./apply_theme.js");

const THEME = {
  name: "Hanbat Startup Theory",
  headFontFace: "맑은 고딕",
  bodyFontFace: "맑은 고딕",
  colors: {
    dk1: "262626", lt1: "FFFFFF", dk2: "002060", lt2: "F2F2F2",
    accent1: "002060", accent2: "C0504D", accent3: "17869E", accent4: "E39B2D",
    accent5: "E6EDF7", accent6: "FBEAEA", hlink: "17869E", folHlink: "6B4C9A",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "창업 이론의 이해";
pres.author = "국립한밭대학교";
const C = pres.SchemeColor;
const NAVY = C.text2, RED = C.accent2, TEAL = C.accent3, AMBER = C.accent4;
const ICE = C.accent5, PINK = C.accent6, GRAY = C.background2, WHITE = C.background1, TXT = C.text1;

// ---------- Layout: user's template (navy rule + logo) + numbered title bar ----------
pres.defineSlideMaster({
  title: "HANBAT_CONTENT",
  background: { color: WHITE },
  objects: [
    { rect: { x: 0, y: 0.535, w: 8.02, h: 0.035, fill: { color: NAVY }, line: { type: "none" } } },
    { image: { path: "logo.png", x: 8.2, y: 0.34, w: 1.64, h: 0.3 } },
    { rect: { x: 0.4, y: 0.75, w: 0.6, h: 0.46, fill: { color: WHITE }, line: { color: NAVY, width: 1.25 } } },
    { rect: { x: 1.08, y: 0.75, w: 8.52, h: 0.46, fill: { color: NAVY }, line: { type: "none" } } },
    { placeholder: { options: { name: "num", type: "body", x: 0.4, y: 0.75, w: 0.6, h: 0.46, fontSize: 16, bold: true, color: NAVY, align: "center", valign: "middle", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 1.2, y: 0.75, w: 8.3, h: 0.46, fontSize: 19, bold: true, color: WHITE, align: "left", valign: "middle", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 9.1, y: 5.3, w: 0.5, h: 0.25, fontSize: 9, color: NAVY, align: "right" },
});

// ---------- helpers ----------
function newSlide(num, title, section) {
  const s = pres.addSlide({ masterName: "HANBAT_CONTENT", sectionTitle: section });
  s.addText(num, { placeholder: "num" });
  s.addText(title, { placeholder: "title" });
  return s;
}
function box(s, x, y, w, h, fill, name, extra = {}) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.06, fill: { color: fill }, line: { type: "none" }, objectName: name, ...extra });
}
function txt(s, text, o) {
  s.addText(text, { isTextBox: true, fontSize: 11, color: TXT, valign: "top", margin: 0.06, ...o });
}
// "CASE" motif: tinted card + red chip
function caseBox(s, x, y, w, h, title, body, opts = {}) {
  box(s, x, y, w, h, opts.fill || PINK, "case-card");
  s.addShape(pres.ShapeType.roundRect, { x: x + 0.12, y: y + 0.1, w: 0.62, h: 0.24, rectRadius: 0.05, fill: { color: RED }, line: { type: "none" }, objectName: "case-chip" });
  txt(s, "CASE", { x: x + 0.12, y: y + 0.1, w: 0.62, h: 0.24, fontSize: 9, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
  txt(s, title, { x: x + 0.82, y: y + 0.07, w: w - 0.92, h: 0.32, fontSize: opts.titleSize || 12, bold: true, color: RED, valign: "middle" });
  txt(s, body, { x: x + 0.12, y: y + 0.42, w: w - 0.24, h: h - 0.48, fontSize: opts.size || 10.5, paraSpaceAfter: 2 });
}
function source(s, text) {
  txt(s, "출처: " + text, { x: 0.4, y: 5.3, w: 8.6, h: 0.25, fontSize: 8, italic: true, valign: "middle", margin: 0 });
}
const bullets = (arr, o = {}) => arr.map((t, i) => ({ text: t, options: { bullet: { indent: 12 }, breakLine: i < arr.length - 1, ...o } }));

// ======================= 01. 설문: 창업 실패 이유 =======================
pres.addSection({ title: "01 창업 실패 이유 설문" });
{
  const s = newSlide("01", "창업자가 말하는 실패 이유: 글로벌 설문(CB Insights)", "01 창업 실패 이유 설문");
  txt(s, "폐업한 스타트업 101곳의 사후 분석(Post-mortem) – 실패 원인 응답 비율(%, 복수응답)", { x: 0.4, y: 1.33, w: 5.6, h: 0.3, fontSize: 11, bold: true, color: NAVY });
  const labels = ["시장 니즈 없음", "자금 소진", "팀 구성 문제", "경쟁에서 밀림", "가격·원가 문제", "제품 완성도 부족", "비즈니스 모델 부재", "마케팅 부족", "고객 의견 무시"];
  const vals = [42, 29, 23, 19, 18, 17, 17, 14, 14];
  s.addChart(pres.ChartType.bar, [{ name: "응답 비율", labels: labels.slice().reverse(), values: vals.slice().reverse() }], {
    x: 0.4, y: 1.62, w: 5.6, h: 3.6, barDir: "bar", barGapWidthPct: 45,
    chartColors: ["002060"], invertedColors: ["002060"],
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 10, dataLabelColor: TXT, dataLabelFormatCode: '0"%"',
    dataLabelFontFace: "+mn-lt", catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
    catAxisLabelFontSize: 10, catAxisLabelColor: TXT, valAxisHidden: true, valAxisMaxVal: 50,
    valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false,
  });
  // highlight top-2
  box(s, 6.3, 1.33, 3.3, 1.55, ICE, "takeaway");
  txt(s, [
    { text: "응답 1·2위", options: { fontSize: 11, bold: true, color: NAVY, breakLine: true } },
    { text: "니즈 42% · 자금 29%", options: { fontSize: 18, bold: true, color: RED, breakLine: true } },
    { text: "창업자 스스로는 ‘고객이 원하지 않았다’, ‘돈이 떨어졌다’를 가장 큰 실패 원인으로 꼽음", options: { fontSize: 10.5 } },
  ], { x: 6.42, y: 1.4, w: 3.1, h: 1.42 });
  caseBox(s, 6.3, 3.0, 3.3, 2.22, "주서로(Juicero), 2017",
    bullets([
      "1.2억 달러 투자 유치, 700달러짜리 와이파이 착즙기 출시",
      "블룸버그: 전용 팩은 손으로 짜도 동일하게 착즙됨",
      "출시 16개월 만에 폐업 → 대표적 ‘시장 니즈 없음’ 사례",
    ]));
  source(s, "CB Insights, “The Top 20 Reasons Startups Fail”(101개 스타트업 사후분석); Bloomberg(2017.4)");
  s.addNotes("CB Insights가 실제로 폐업한 스타트업 101곳의 창업자 회고(포스트모템)를 분석한 결과입니다. 1위는 시장 니즈 없음(42%), 2위는 자금 소진(29%)입니다. 이후 2021년 업데이트(111건)에서는 자금 소진·투자유치 실패 38%, 시장 니즈 없음 35%로 순위가 바뀌었지만 상위 두 요인은 동일합니다. 주서로는 1.2억 달러를 투자받고도 '고객이 실제로 필요로 하는가'를 검증하지 않아 실패한 사례입니다.");
}
{
  const s = newSlide("01", "국내 창업자가 말하는 장애요인과 생존율", "01 창업 실패 이유 설문");
  txt(s, "창업 준비 시 장애요인 (중소벤처기업부 창업기업실태조사, 2023년 기준, 복수응답)", { x: 0.4, y: 1.33, w: 9.2, h: 0.3, fontSize: 11, bold: true, color: NAVY });
  const stats = [
    ["53.7%", "자금 확보의 어려움", RED],
    ["45.9%", "실패에 대한 두려움", NAVY],
    ["36.7%", "창업 지식·능력·경험 부족", TEAL],
  ];
  stats.forEach(([n, l, c], i) => {
    const x = 0.4 + i * 3.1;
    box(s, x, 1.68, 2.9, 1.2, GRAY, "stat-" + i);
    txt(s, n, { x: x + 0.15, y: 1.73, w: 2.6, h: 0.65, fontSize: 30, bold: true, color: c, valign: "middle" });
    txt(s, l, { x: x + 0.15, y: 2.38, w: 2.6, h: 0.4, fontSize: 12, bold: true });
  });
  // survival
  box(s, 0.4, 3.05, 4.4, 2.17, ICE, "survival");
  txt(s, "신생기업 생존율 (통계청 기업생멸행정통계, 2022)", { x: 0.55, y: 3.12, w: 4.1, h: 0.3, fontSize: 11, bold: true, color: NAVY });
  txt(s, "64.1%", { x: 0.55, y: 3.5, w: 1.9, h: 0.6, fontSize: 26, bold: true, color: NAVY });
  txt(s, "1년 생존율", { x: 0.55, y: 4.1, w: 1.9, h: 0.3, fontSize: 11 });
  txt(s, "34.3%", { x: 2.6, y: 3.5, w: 1.9, h: 0.6, fontSize: 26, bold: true, color: RED });
  txt(s, "5년 생존율", { x: 2.6, y: 4.1, w: 1.9, h: 0.3, fontSize: 11 });
  txt(s, "→ 창업기업 3곳 중 2곳은 5년 안에 문을 닫는다", { x: 0.55, y: 4.55, w: 4.1, h: 0.55, fontSize: 11.5, bold: true, color: RED });
  caseBox(s, 5.0, 3.05, 4.6, 2.17, "타다(VCNC), 2018~2020",
    bullets([
      "출시 1년여 만에 회원 약 170만 명 확보 → 고객 니즈는 분명했음",
      "2020년 여객자동차법 개정으로 ‘타다 베이직’ 서비스 중단",
      "설문의 ‘규제·외부환경’형 실패: 사업모델이 제도 리스크를 검증하지 못함",
    ]));
  source(s, "중소벤처기업부·창업진흥원 「창업기업실태조사」(2025 발표, 2023년 기준); 통계청 「2022년 기업생멸행정통계」(2023.12)");
  s.addNotes("국내 조사에서도 창업자들이 가장 크게 느끼는 장애요인은 '자금'입니다(53.7%, 2021년 기준 조사에서는 71.0%). 주목할 것은 3위 '창업 지식·능력·경험 부족' 36.7%입니다. 이것이 다음 장에서 전개할 핵심 논리의 단서입니다. 통계청 자료에 따르면 신생기업의 5년 생존율은 34.3%에 불과합니다.");
}

// ======================= 02. 실패의 진짜 원인 =======================
pres.addSection({ title: "02 실패의 진짜 원인" });
{
  const s = newSlide("02", "설문 응답은 ‘증상’이다: 근본 원인은 방법론의 부재", "02 실패의 진짜 원인");
  txt(s, "설문 응답 (증상)", { x: 0.4, y: 1.3, w: 3.1, h: 0.3, fontSize: 12, bold: true, color: RED });
  txt(s, "근본 원인 (방법을 모르고 창업)", { x: 4.0, y: 1.3, w: 5.6, h: 0.3, fontSize: 12, bold: true, color: NAVY });
  const rows = [
    ["시장 니즈 없음 (42%)", "고객 문제를 검증하지 않고 제품부터 개발", "→ 고객개발·디자인 씽킹"],
    ["자금 소진 (29%)", "제품-시장 적합성(PMF) 전에 인력·마케팅 과잉 확장", "→ 린 스타트업·고객 검증"],
    ["비즈니스 모델 부재 (17%)", "수익 구조를 가설로 세우고 검증하지 않음", "→ BMC·린 캔버스"],
    ["제품 완성도·타이밍", "기술 성숙도와 사업화 단계 관리 부재", "→ TRL·졸리 모델"],
  ];
  rows.forEach(([a, b, c], i) => {
    const y = 1.65 + i * 0.6;
    box(s, 0.4, y, 3.1, 0.5, PINK, "sym-" + i);
    txt(s, a, { x: 0.5, y, w: 2.9, h: 0.5, fontSize: 11.5, bold: true, valign: "middle" });
    s.addShape(pres.ShapeType.rightArrow, { x: 3.58, y: y + 0.13, w: 0.34, h: 0.24, fill: { color: NAVY }, line: { type: "none" }, objectName: "arrow-" + i });
    box(s, 4.0, y, 5.6, 0.5, ICE, "root-" + i);
    txt(s, [{ text: b + "  ", options: { bold: true } }, { text: c, options: { color: TEAL, bold: true } }], { x: 4.1, y, w: 5.4, h: 0.5, fontSize: 11, valign: "middle" });
  });
  // evidence + case
  box(s, 0.4, 4.12, 4.5, 1.1, GRAY, "evidence");
  txt(s, [
    { text: "74%", options: { fontSize: 24, bold: true, color: RED } },
    { text: "  고성장 스타트업 실패 원인 = 성급한 확장", options: { fontSize: 11, bold: true, breakLine: true } },
    { text: "(Startup Genome, 3,200여 개사 분석) – 자금 부족은 결과이지 원인이 아니다", options: { fontSize: 10 } },
  ], { x: 0.5, y: 4.15, w: 4.3, h: 1.05, valign: "middle" });
  caseBox(s, 5.1, 4.12, 4.5, 1.1, "퀴비(Quibi), 2020",
    "17.5억 달러(약 2조 원)를 모으고도 출시 6개월 만에 폐업. ‘돈’이 아니라 고객 검증 없는 대규모 실행이 문제였다.", { size: 10 });
  source(s, "Startup Genome, “Report Extra on Premature Scaling”(2011); CB Insights 애널리스트 A. Sanwal 인터뷰; WSJ(2020.10)");
  s.addNotes("설문 응답은 창업자가 '마지막에 경험한 현상'입니다. CB Insights의 Anand Sanwal도 '자금 부족은 실패의 원인이 아니라 증상'이라고 말했습니다. 시장 니즈가 없었던 것은 고객을 검증하는 방법(고객개발, 디자인 씽킹)을 몰랐기 때문이고, 돈이 떨어진 것은 검증 전에 확장했기 때문입니다. 퀴비는 2조 원을 모았기 때문에 '자금 부족'으로 실패할 수 없는 회사였지만, 6개월 만에 문을 닫았습니다.");
}
{
  const s = newSlide("02", "같은 시대, 같은 온라인 유통: 승패를 가른 것은 ‘방법’", "02 실패의 진짜 원인");
  // Webvan
  box(s, 0.4, 1.35, 4.5, 2.95, PINK, "webvan");
  txt(s, "웹밴(Webvan) – 실패", { x: 0.55, y: 1.42, w: 4.2, h: 0.35, fontSize: 15, bold: true, color: RED });
  txt(s, bullets([
    "1999년 온라인 식료품 배송 / IPO 포함 약 8억 달러 조달",
    "고객 검증 전, 10억 달러 규모 자동화 물류창고 계약",
    "수요가 계획에 못 미쳐 2001년 파산",
    "실패 원인: 사업계획서대로 ‘실행’만 하고 ‘검증’ 단계가 없었음",
  ]), { x: 0.55, y: 1.85, w: 4.2, h: 2.4, fontSize: 11.5, paraSpaceAfter: 6 });
  // Zappos
  box(s, 5.1, 1.35, 4.5, 2.95, ICE, "zappos");
  txt(s, "자포스(Zappos) – 성공", { x: 5.25, y: 1.42, w: 4.2, h: 0.35, fontSize: 15, bold: true, color: TEAL });
  txt(s, bullets([
    "1999년 창업자가 동네 신발가게 사진을 찍어 웹에 게시",
    "주문이 들어오면 매장에서 사서 직접 배송 → 재고 없이 수요 검증",
    "검증 후 단계적 확장, 2009년 아마존이 약 12억 달러에 인수",
    "성공 요인: 최소 비용으로 ‘고객이 온라인으로 신발을 살까?’를 먼저 확인",
  ]), { x: 5.25, y: 1.85, w: 4.2, h: 2.4, fontSize: 11.5, paraSpaceAfter: 6 });
  caseBox(s, 0.4, 4.45, 9.2, 0.78, "드롭박스(Dropbox), 2007",
    "제품 완성 전 3분짜리 데모 영상(MVP)만 공개 → 하룻밤 사이 베타 대기자 5,000명에서 75,000명으로 증가. 개발 전에 수요를 증명했다.", { size: 10.5 });
  source(s, "S. Blank, 「The Startup Owner’s Manual」(2012); E. Ries, 「The Lean Startup」(2011)");
  s.addNotes("웹밴과 자포스는 같은 시기(1999년)에 같은 '온라인 유통'으로 출발했습니다. 웹밴은 고객 검증 없이 거대한 물류 인프라에 투자했고, 자포스는 사진 몇 장으로 수요부터 검증했습니다. 스티브 블랭크는 웹밴을 '제품개발 모델'만 따른 실패의 대표 사례로, 에릭 리스는 자포스와 드롭박스를 MVP의 대표 사례로 소개합니다.");
}
{
  const s = newSlide("02", "결론: 창업 실패를 줄이는 것은 ‘방법론의 숙지’다", "02 실패의 진짜 원인");
  box(s, 0.4, 1.35, 9.2, 0.85, NAVY, "thesis");
  txt(s, "창업은 아이디어와 자금만으로 하는 것이 아니라,\n검증된 기술사업화·창업 방법론으로 불확실성을 체계적으로 줄여가는 과정이다", { x: 0.6, y: 1.35, w: 8.8, h: 0.85, fontSize: 14, bold: true, color: WHITE, valign: "middle", align: "center" });
  const steps = [
    ["기술사업화", "기술을 시장으로\n(TRL·졸리 모델)", NAVY],
    ["창업가 사고", "고객에서 기회를\n(디자인 씽킹)", TEAL],
    ["모델 설계", "수익구조를 가설로\n(BMC·린 캔버스)", AMBER],
    ["고객 검증", "현장에서 증명\n(고객개발·TSOM)", RED],
  ];
  steps.forEach(([h, d, c], i) => {
    const x = 0.4 + i * 2.33;
    s.addShape(pres.ShapeType.chevron, { x, y: 2.4, w: 2.25, h: 0.55, fill: { color: c }, line: { type: "none" }, objectName: "chev-" + i });
    txt(s, h, { x: x + 0.25, y: 2.4, w: 1.75, h: 0.55, fontSize: 13, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    txt(s, d, { x, y: 3.0, w: 2.2, h: 0.6, fontSize: 11, align: "center" });
  });
  caseBox(s, 0.4, 3.75, 9.2, 1.47, "미국 국립과학재단(NSF) I-Corps 프로그램, 2011~",
    bullets([
      "기술은 있으나 사업화에 실패하는 연구자 창업팀을 위해 NSF가 스티브 블랭크의 고객개발 방법론을 정식 교육과정으로 도입",
      "참여팀은 약 7주 동안 100명 이상의 잠재고객을 인터뷰하며 비즈니스 모델 가설을 검증 → 국가 차원에서 ‘방법론 교육’을 창업 지원의 핵심으로 채택",
    ]), { size: 10.5 });
  source(s, "U.S. National Science Foundation, Innovation Corps(I-Corps) 프로그램 안내");
  s.addNotes("따라서 이 강의의 핵심 주장은 '방법을 알고 창업하라'입니다. 기술사업화 → 창업가 사고 → 비즈니스 모델 설계 → 고객 검증의 4단계 방법론을 차례로 다룹니다. 미국 NSF는 이 문제의식에서 2011년부터 연구자 창업팀에게 고객개발 방법론을 필수로 교육하고 있습니다.");
}

// ======================= 03. 연대별 개관 =======================
pres.addSection({ title: "03 창업 이론의 진화" });
{
  const s = newSlide("03", "연대별 개관: 50년간 창업·기술사업화 이론의 진화", "03 창업 이론의 진화");
  const cols = [
    { era: "1970~1990s", name: "기술사업화·관리", c: RED, q: "개발된 기술을 어떻게 관리하고 시장에 확산할 것인가?",
      items: [["1974/1995", "Technology Readiness Level"], ["1986", "Stage-Gate"], ["1991", "Crossing the Chasm"], ["1997", "Commercializing New Technologies"]],
      ex: "3M 포스트잇: 실패한 접착제 → 12년 사업화" },
    { era: "2000s", name: "창업가 사고·전략", c: TEAL, q: "불확실성 속에서 어떻게 기회를 발견하고 만들 것인가?",
      items: [["2001", "Effectuation"], ["2005", "Blue Ocean Strategy"], ["2005~2009", "Design Thinking"]],
      ex: "에어비앤비: 호스트 방문·사진 개선으로 매출 2배" },
    { era: "2010s", name: "스타트업 방법론·도구", c: NAVY, q: "어떻게 빠르게 검증하고 반복·확장할 것인가?",
      items: [["2010", "Business Model Generation"], ["2010", "Lean Canvas"], ["2011", "Lean Startup"], ["2012", "The Startup Owner’s Manual"], ["2013", "Disciplined Entrepreneurship"], ["2015", "Traversing the Valley of Death"], ["2016", "Jobs-to-be-Done"], ["2016", "Design Sprint"]],
      ex: "드롭박스: 데모 영상 MVP로 수요 검증" },
  ];
  const xs = [0.4, 3.0, 5.6], ws = [2.45, 2.45, 4.0];
  cols.forEach((col, i) => {
    const x = xs[i], w = ws[i];
    s.addShape(pres.ShapeType.rect, { x, y: 1.32, w, h: 0.62, fill: { color: col.c }, line: { type: "none" }, objectName: "colhead-" + i });
    txt(s, [{ text: col.era, options: { fontSize: 9, breakLine: true } }, { text: col.name, options: { fontSize: 13, bold: true } }], { x: x + 0.08, y: 1.32, w: w - 0.16, h: 0.62, color: WHITE, valign: "middle" });
    s.addShape(pres.ShapeType.rect, { x, y: 1.94, w, h: 2.62, fill: { color: GRAY }, line: { type: "none" }, objectName: "colbody-" + i });
    txt(s, col.q, { x: x + 0.08, y: 2.0, w: w - 0.16, h: 0.45, fontSize: 9.5, italic: true, color: col.c });
    const runs = [];
    col.items.forEach(([yr, nm], j) => {
      runs.push({ text: yr + "  ", options: { bold: true, color: i === 2 ? NAVY : RED } });
      runs.push({ text: nm, options: { bold: true, color: NAVY, breakLine: j < col.items.length - 1 } });
    });
    txt(s, runs, { x: x + 0.08, y: 2.5, w: w - 0.16, h: 2.0, fontSize: i === 2 ? 10.5 : 10.5, paraSpaceAfter: 3 });
    box(s, x, 4.66, w, 0.56, PINK, "colcase-" + i);
    txt(s, [{ text: "사례 ", options: { bold: true, color: RED } }, { text: col.ex }], { x: x + 0.06, y: 4.66, w: w - 0.12, h: 0.56, fontSize: 9.5, valign: "middle" });
  });
  source(s, "각 이론 원전(아래 슬라이드 참조)");
  s.addNotes("창업 이론은 크게 세 시기로 진화했습니다. 1970~90년대에는 '이미 개발된 기술을 어떻게 관리·확산할 것인가'(기술사업화), 2000년대에는 '불확실성 속에서 기회를 어떻게 발견·창출할 것인가'(창업가 사고), 2010년대에는 '어떻게 빠르게 검증하고 반복할 것인가'(스타트업 방법론)가 핵심 질문이었습니다. 각 시기별 대표 사례를 함께 제시했습니다.");
}
function theoryCards(s, items, cols, top, cardH, opts = {}) {
  const gap = 0.2, W = 9.2, w = (W - gap * (cols - 1)) / cols;
  items.forEach((it, i) => {
    const r = Math.floor(i / cols), c = i % cols;
    const x = 0.4 + c * (w + gap), y = top + r * (cardH + gap);
    box(s, x, y, w, cardH, GRAY, "card-" + i);
    txt(s, [{ text: it.yr + "  ", options: { color: opts.accent || RED } }, { text: it.name, options: { color: NAVY } }], { x: x + 0.08, y: y + 0.05, w: w - 0.16, h: opts.headH || 0.32, fontSize: opts.head || 12, bold: true, valign: "middle" });
    const dy = (opts.headH || 0.32) - 0.32;
    txt(s, it.who, { x: x + 0.08, y: y + 0.36 + dy, w: w - 0.16, h: 0.24, fontSize: 9, italic: true });
    txt(s, it.what, { x: x + 0.08, y: y + 0.6 + dy, w: w - 0.16, h: opts.whatH || 0.75, fontSize: opts.size || 10.5 });
    const cy = y + cardH - (opts.caseH || 0.62) - 0.06;
    box(s, x + 0.06, cy, w - 0.12, opts.caseH || 0.62, PINK, "card-case-" + i);
    txt(s, [{ text: "사례 ", options: { bold: true, color: RED } }, { text: it.ex }], { x: x + 0.1, y: cy, w: w - 0.2, h: opts.caseH || 0.62, fontSize: opts.caseSize || 9.5, valign: "middle" });
  });
}
{
  const s = newSlide("03", "1970~1990s 기술사업화·관리: 기술을 시장으로", "03 창업 이론의 진화");
  theoryCards(s, [
    { yr: "1974/1995", name: "TRL (기술성숙도)", who: "NASA – S. Sadin(1974) / J. Mankins(1995, 9단계)", what: "기초원리 발견(1)부터 실제 운용(9)까지 기술의 성숙 단계를 객관적으로 측정하는 척도", ex: "NASA 우주 프로젝트 평가 기준 → 국내 정부 R&D 과제도 TRL로 목표·성과 관리" },
    { yr: "1986", name: "Stage-Gate", who: "Robert G. Cooper", what: "신제품 개발을 단계(Stage)로 나누고 각 관문(Gate)에서 진행/중단을 결정해 위험을 관리", ex: "P&G·3M 등 다수 글로벌 제조기업이 신제품 개발 프로세스로 도입" },
    { yr: "1991", name: "Crossing the Chasm", who: "Geoffrey A. Moore", what: "혁신 수용자와 초기 다수 사이의 ‘캐즘(단절)’을 넘으려면 틈새시장 집중이 필요", ex: "테슬라: 로드스터(얼리어답터) → 모델S → 모델3로 단계적 대중시장 진입" },
    { yr: "1997", name: "Commercializing New Technologies", who: "Vijay K. Jolly (졸리 모델)", what: "기술사업화를 5단계 하위 프로세스와 4개 연결다리(이해관계자 동원)로 체계화", ex: "3M 포스트잇: 실패한 접착제(1968) → 전국 출시(1980)" },
  ], 2, 1.35, 1.82, { whatH: 0.55, caseH: 0.5 });
  source(s, "Mankins(1995) Technology Readiness Levels; Cooper(1990) Stage-Gate Systems; Moore(1991); Jolly(1997)");
  s.addNotes("1세대 이론은 대기업·연구소가 '이미 개발된 기술'을 어떻게 관리하고 시장에 내보낼지에 집중했습니다. TRL은 기술의 성숙도를, Stage-Gate는 개발 프로세스를, 캐즘은 시장 확산을, 졸리 모델은 기술사업화 전 과정을 다룹니다.");
}
{
  const s = newSlide("03", "2000s 창업가 사고·전략: 불확실성 속 기회 창출", "03 창업 이론의 진화");
  theoryCards(s, [
    { yr: "2001", name: "Effectuation", who: "Saras Sarasvathy", what: "목표에서 출발하는 인과적 사고가 아니라, ‘지금 가진 자원’에서 출발해 감당 가능한 손실 범위 안에서 기회를 만들어가는 전문 창업가의 사고방식", ex: "스팽스(Spanx): 사라 블레이클리가 저축 5,000달러로 시작 – 감당 가능한 손실 원칙" },
    { yr: "2005", name: "Blue Ocean Strategy", who: "W. Chan Kim & Renée Mauborgne", what: "경쟁이 치열한 레드오션 대신 가치 혁신(차별화+저비용)으로 경쟁 없는 새 시장을 창출", ex: "태양의 서커스: 동물쇼·스타 없앤 공연예술형 서커스 / 닌텐도 Wii" },
    { yr: "2005~2009", name: "Design Thinking", who: "IDEO · Stanford d.school · T. Brown(2008)", what: "공감–정의–아이디어–프로토타입–테스트로 고객의 숨은 니즈에서 해결책을 도출하는 인간중심 혁신 방법", ex: "GE 헬스케어 ‘어드벤처 MRI’, 에어비앤비 초기 성장" },
  ], 3, 1.35, 3.85, { whatH: 1.7, caseH: 0.95, size: 12, caseSize: 10.5 });
  source(s, "Sarasvathy(2001) AMR; Kim & Mauborgne(2005) Blue Ocean Strategy; Brown(2008) HBR “Design Thinking”");
  s.addNotes("2000년대에는 창업가 개인의 사고방식과 전략으로 관심이 옮겨갑니다. 이 중 디자인 씽킹은 '고객의 니즈를 어떻게 찾는가'라는, 설문 1위 실패요인(시장 니즈 없음)에 직접 답하는 방법론이라 뒤에서 자세히 다룹니다.");
}
{
  const s = newSlide("03", "2010s 스타트업 방법론·도구: 빠른 검증과 반복", "03 창업 이론의 진화");
  theoryCards(s, [
    { yr: "2010", name: "Business Model Generation", who: "Osterwalder & Pigneur", what: "9블록 캔버스로 비즈니스 모델 시각화", ex: "네스프레소 캡슐 모델" },
    { yr: "2010", name: "Lean Canvas", who: "Ash Maurya", what: "BMC를 스타트업용 문제·해결 중심으로 변형", ex: "우버 초기 모델" },
    { yr: "2011", name: "Lean Startup", who: "Eric Ries", what: "MVP로 만들고-측정-학습 루프 반복", ex: "드롭박스 데모 영상 MVP" },
    { yr: "2012", name: "Startup Owner’s Manual", who: "Steve Blank & Bob Dorf", what: "고객개발 4단계로 사업모델 검색·실행", ex: "NSF I-Corps 교육과정" },
    { yr: "2013", name: "Disciplined Entrepreneurship", who: "Bill Aulet (MIT)", what: "시장 선정부터 확장까지 24단계 체크리스트", ex: "MIT 창업교육 표준 교재" },
    { yr: "2015", name: "Traversing the Valley of Death", who: "Markham & Mugge", what: "R&D와 사업화 사이 ‘죽음의 계곡’ 극복 가이드", ex: "제록스 PARC GUI → 애플이 사업화" },
    { yr: "2016", name: "Jobs-to-be-Done", who: "Clayton Christensen", what: "고객이 제품을 ‘고용’해 해결하려는 과업에 집중", ex: "맥도날드 밀크셰이크(출근길 과업)" },
    { yr: "2016", name: "Design Sprint", who: "Jake Knapp (Google Ventures)", what: "5일 만에 문제정의~프로토타입~고객테스트", ex: "블루보틀 커피 온라인 스토어" },
  ], 4, 1.32, 1.86, { head: 10.5, headH: 0.45, size: 9.5, whatH: 0.5, caseH: 0.5, caseSize: 9 });
  source(s, "각 저서 원전; Ries(2011); Blank & Dorf(2012); Christensen et al.(2016) Competing Against Luck; Knapp(2016) Sprint");
  s.addNotes("2010년대에는 '빠르게 검증하고 반복하라'는 스타트업 방법론과 실무 도구가 쏟아졌습니다. 이 중 비즈니스 모델을 설계하는 BMC와 린 캔버스, 그리고 검증 프로세스를 다루는 스타트업 오너스 매뉴얼을 뒤에서 자세히 비교·설명합니다.");
}
{
  const s = newSlide("03", "심화 학습 로드맵: 시대별 핵심 이론 하나씩 깊게", "03 창업 이론의 진화");
  const cols = [
    ["기술사업화·관리", "졸리 모델", "기술이 시장에 이르는 5단계와 4개의 다리", "3M 포스트잇", RED],
    ["창업가 사고·전략", "디자인 씽킹", "고객 공감에서 시작하는 5단계 혁신 프로세스", "GE 헬스케어 · 에어비앤비", TEAL],
    ["스타트업 방법론·도구", "BMC vs 린 캔버스\n+ 스타트업 오너스 매뉴얼", "비즈니스 모델 설계 도구 비교와 고객개발 검증 프로세스", "네스프레소 · 우버 · 배달의민족", NAVY],
  ];
  cols.forEach(([era, th, d, ex, c], i) => {
    const x = 0.4 + i * 3.1, w = 2.9;
    box(s, x, 1.35, w, 3.87, GRAY, "road-" + i);
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.15, y: 1.5, w: 0.55, h: 0.55, fill: { color: c }, line: { type: "none" }, objectName: "road-dot-" + i });
    txt(s, String(i + 4).padStart(2, "0"), { x: x + 0.15, y: 1.5, w: 0.55, h: 0.55, fontSize: 13, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    txt(s, era, { x: x + 0.8, y: 1.5, w: w - 0.9, h: 0.55, fontSize: 11, bold: true, color: c, valign: "middle" });
    txt(s, th, { x: x + 0.15, y: 2.2, w: w - 0.3, h: 0.75, fontSize: 15, bold: true, color: NAVY });
    txt(s, d, { x: x + 0.15, y: 3.0, w: w - 0.3, h: 0.9, fontSize: 11 });
    box(s, x + 0.1, 4.2, w - 0.2, 0.9, PINK, "road-case-" + i);
    txt(s, [{ text: "다룰 사례", options: { bold: true, color: RED, breakLine: true } }, { text: ex, options: { bold: true } }], { x: x + 0.2, y: 4.2, w: w - 0.4, h: 0.9, fontSize: 11, valign: "middle" });
  });
  source(s, "본 강의 구성");
  s.addNotes("이제 각 시기를 대표하는 핵심 이론을 하나씩 깊게 다룹니다. 기술사업화에서는 졸리 모델, 창업가 사고에서는 디자인 씽킹, 스타트업 방법론에서는 BMC와 린 캔버스 비교, 그리고 스타트업 오너스 매뉴얼입니다.");
}

// ======================= 04. 졸리 모델 =======================
pres.addSection({ title: "04 졸리 모델" });
{
  const s = newSlide("04", "기술사업화: 졸리(Jolly) 모델의 5단계와 4개의 다리", "04 졸리 모델");
  txt(s, "Vijay K. Jolly(1997), 「Commercializing New Technologies」 – 기술사업화는 단계(Stage)와, 단계 사이에서 이해관계자를 동원하는 다리(Bridge)의 연속", { x: 0.4, y: 1.3, w: 9.2, h: 0.4, fontSize: 10.5, italic: true });
  const stages = [["Imagining", "상상", "기술+시장 기회 구상"], ["Incubating", "배양", "사업화 가능성 검토"], ["Demonstrating", "시연", "시제품·제품화 실증"], ["Promoting", "촉진", "시장 출시·수용 확대"], ["Sustaining", "지속", "수익 창출·확장"]];
  const bridges = ["관심과 지지\n확보", "시연 자원\n확보", "시장 구성원\n동원", "보완 자산\n확보"];
  stages.forEach(([en, ko, d], i) => {
    const x = 0.4 + i * 1.9, w = 1.5;
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.85, w, h: 1.3, rectRadius: 0.08, fill: { color: NAVY }, line: { type: "none" }, objectName: "stage-" + i });
    txt(s, [{ text: `${i + 1}. ${ko}`, options: { fontSize: 14, bold: true, breakLine: true } }, { text: en, options: { fontSize: 9.5, breakLine: true } }, { text: d, options: { fontSize: 9.5 } }], { x: x + 0.05, y: 1.85, w: w - 0.1, h: 1.3, color: WHITE, align: "center", valign: "middle" });
    if (i < 4) {
      s.addShape(pres.ShapeType.rightArrow, { x: x + 1.52, y: 2.33, w: 0.36, h: 0.34, fill: { color: RED }, line: { type: "none" }, objectName: "bridge-arrow-" + i });
      box(s, x + 0.95, 3.3, 1.5, 0.6, PINK, "bridge-" + i);
      txt(s, bridges[i], { x: x + 0.95, y: 3.3, w: 1.5, h: 0.6, fontSize: 10, bold: true, color: RED, align: "center", valign: "middle", margin: 0 });
    }
  });
  txt(s, "▲ 다리(Bridge): 다음 단계로 넘어가기 위해 투자자·파트너·고객 등 이해관계자를 동원하는 활동", { x: 0.4, y: 3.95, w: 9.2, h: 0.3, fontSize: 10, bold: true, color: RED });
  caseBox(s, 0.4, 4.3, 9.2, 0.92, "국내 공공기술 이전 사업화",
    "대학·출연연 기술이전 후 사업화에 실패하는 다수의 사례는 ‘기술(시연)’ 단계는 넘었지만 ‘시장 구성원 동원(다리 3)’과 ‘보완 자산 확보(다리 4)’를 설계하지 않은 경우다. 졸리 모델은 기술 단계와 함께 각 다리의 이해관계자 동원 계획을 요구한다.", { size: 10 });
  source(s, "Jolly, V. K.(1997), Commercializing New Technologies: Getting from Mind to Market, Harvard Business School Press");
  s.addNotes("졸리 모델의 핵심은 '단계'만이 아니라 단계 사이의 '다리'입니다. 상상→배양 사이에는 관심과 지지를, 배양→시연 사이에는 시연을 위한 자원을, 시연→촉진 사이에는 유통·고객 등 시장 구성원을, 촉진→지속 사이에는 생산·서비스 등 보완 자산을 동원해야 합니다. 기술은 좋은데 사업화에 실패하는 경우는 대개 이 다리를 놓지 못한 것입니다.");
}
{
  const s = newSlide("04", "졸리 모델로 본 사례: 3M 포스트잇(Post-it)", "04 졸리 모델");
  const tl = [
    ["1968", "상상", "스펜서 실버, 약한 접착제 개발 – ‘실패작’으로 분류", NAVY],
    ["1974", "배양", "아트 프라이, 성가대 악보 책갈피로 용도 착안", NAVY],
    ["1977", "시연", "4개 도시 시험판매(Press ’n Peel) – 반응 저조", NAVY],
    ["1978", "촉진", "아이다호 보이시 무료 샘플 대량 배포 – 재구매 의향 급증", NAVY],
    ["1980", "지속", "미국 전국 출시 → 이후 세계적 사무용품으로 정착", NAVY],
  ];
  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 2.25, w: 8.8, h: 0.04, fill: { color: NAVY }, line: { type: "none" }, objectName: "timeline" });
  tl.forEach(([yr, st, d], i) => {
    const x = 0.4 + i * 1.86;
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.62, y: 2.07, w: 0.4, h: 0.4, fill: { color: i === 2 ? RED : NAVY }, line: { color: WHITE, width: 2 }, objectName: "tl-dot-" + i });
    txt(s, yr, { x, y: 1.4, w: 1.65, h: 0.35, fontSize: 16, bold: true, color: NAVY, align: "center" });
    txt(s, st, { x, y: 1.72, w: 1.65, h: 0.3, fontSize: 11, bold: true, color: RED, align: "center" });
    box(s, x, 2.6, 1.65, 1.15, GRAY, "tl-card-" + i);
    txt(s, d, { x: x + 0.05, y: 2.62, w: 1.55, h: 1.1, fontSize: 10, valign: "middle" });
  });
  caseBox(s, 0.4, 3.9, 9.2, 1.32, "다리(Bridge)가 성패를 가른 지점",
    bullets([
      "다리 1·2: 사내 ‘15% 규칙’과 경영진 지지로 실패한 기술에 개발 자원 확보",
      "다리 3: 시험판매 실패 후 포기하지 않고 ‘써보게 하는’ 무료 샘플로 시장 구성원(사무직 고객) 동원",
      "교훈: 기술 자체가 아니라 단계 사이 이해관계자 동원이 사업화 기간 12년을 결정",
    ]), { size: 10.5 });
  source(s, "3M Company, “History of Post-it Notes”; Jolly(1997) 사례 분석 틀 적용");
  s.addNotes("포스트잇은 졸리 모델의 5단계가 그대로 드러나는 사례입니다. 특히 1977년 시험판매 실패 이후 보이시 지역에 무료 샘플을 뿌려 고객을 직접 동원한 것이 '시장 구성원 동원'이라는 다리를 놓은 결정적 장면입니다.");
}

// ======================= 05. 디자인 씽킹 =======================
pres.addSection({ title: "05 디자인 씽킹" });
{
  const s = newSlide("05", "창업가 사고: 디자인 씽킹(Design Thinking) 5단계", "05 디자인 씽킹");
  const steps = [["공감", "Empathize", "관찰·인터뷰로 고객의 감정과 맥락 이해"], ["정의", "Define", "진짜 문제를 ‘사용자 관점’으로 재정의"], ["아이디어", "Ideate", "판단 유보, 많은 해결책 발산"], ["프로토타입", "Prototype", "싸고 빠르게 만들어 보기"], ["테스트", "Test", "고객 반응으로 학습·반복"]];
  steps.forEach(([ko, en, d], i) => {
    const x = 0.4 + i * 1.86, w = 1.72;
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.46, y: 1.35, w: 0.8, h: 0.8, fill: { color: i % 2 ? NAVY : TEAL }, line: { type: "none" }, objectName: "dt-dot-" + i });
    txt(s, String(i + 1), { x: x + 0.46, y: 1.35, w: 0.8, h: 0.8, fontSize: 22, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    txt(s, [{ text: ko, options: { fontSize: 14, bold: true, color: NAVY, breakLine: true } }, { text: en, options: { fontSize: 9.5, italic: true } }], { x, y: 2.2, w, h: 0.55, align: "center" });
    txt(s, d, { x, y: 2.75, w, h: 0.6, fontSize: 10, align: "center" });
  });
  txt(s, "※ 단계는 선형이 아니라 반복(Iterative) – 테스트 결과에 따라 공감·정의로 되돌아감", { x: 0.4, y: 3.35, w: 9.2, h: 0.28, fontSize: 10, italic: true, color: TEAL });
  caseBox(s, 0.4, 3.7, 9.2, 1.52, "GE 헬스케어 ‘어드벤처 시리즈’ MRI (더그 디츠)",
    bullets([
      "공감: 개발자 더그 디츠가 병원에서 자신이 만든 MRI를 보고 겁에 질려 우는 아이를 목격",
      "정의: 문제는 ‘장비 성능’이 아니라 ‘아이가 느끼는 공포’ → 아이들에게 무서운 검사를 모험으로 바꾸자",
      "결과: 기기는 그대로 두고 해적선·우주선 테마로 재디자인 → 진정제 투여 감소, 환자 만족도 90% 상승",
    ]), { size: 10.5 });
  source(s, "Stanford d.school, “An Introduction to Design Thinking”; Doug Dietz, TEDx(2012); IDEO");
  s.addNotes("디자인 씽킹은 '시장 니즈 없음'이라는 1위 실패 요인을 예방하는 방법론입니다. 기술이나 아이디어가 아니라 고객의 감정과 맥락에서 출발합니다. GE 헬스케어 사례는 기술을 바꾸지 않고도 고객 경험의 문제를 재정의해 성과를 낸 대표 사례입니다.");
}
{
  const s = newSlide("05", "디자인 씽킹 사례: 에어비앤비의 첫 성장", "05 디자인 씽킹");
  txt(s, "2009년, Y Combinator 참여 당시 에어비앤비의 주간 매출은 약 200달러에서 정체", { x: 0.4, y: 1.3, w: 9.2, h: 0.3, fontSize: 11.5, bold: true, color: NAVY });
  const rows = [
    ["공감", "창업자들이 직접 뉴욕으로 날아가 호스트 집에 머물며 이용 과정을 관찰"],
    ["정의", "문제는 서비스가 아니라 ‘휴대폰으로 찍은 어둡고 흐린 숙소 사진’ – 게스트가 신뢰할 수 없음"],
    ["아이디어", "전문 사진 촬영을 무료로 제공하면 예약이 늘어날 것이라는 가설"],
    ["프로토타입", "확장 가능한지 따지지 않고, 창업자가 카메라를 빌려 직접 숙소를 촬영(Do things that don’t scale)"],
    ["테스트", "1주일 만에 주간 매출 약 400달러로 2배 → 이후 전문 사진 프로그램으로 공식화"],
  ];
  rows.forEach(([k, v], i) => {
    const y = 1.7 + i * 0.58;
    s.addShape(pres.ShapeType.homePlate, { x: 0.4, y, w: 1.6, h: 0.48, fill: { color: i % 2 ? NAVY : TEAL }, line: { type: "none" }, objectName: "ab-step-" + i });
    txt(s, k, { x: 0.45, y, w: 1.35, h: 0.48, fontSize: 12, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    box(s, 2.1, y, 4.6, 0.48, GRAY, "ab-row-" + i);
    txt(s, v, { x: 2.18, y, w: 4.45, h: 0.48, fontSize: 9.5, valign: "middle" });
  });
  caseBox(s, 6.9, 1.7, 2.7, 2.82, "핵심 교훈",
    [
      { text: "$200 → $400", options: { fontSize: 18, bold: true, color: RED, breakLine: true } },
      { text: "주간 매출 2배", options: { fontSize: 11, bold: true, breakLine: true } },
      { text: " ", options: { fontSize: 6, breakLine: true } },
      { text: "코드 한 줄 바꾸지 않고, 고객 현장에서 문제를 다시 정의해 해결", options: { fontSize: 10.5 } },
    ]);
  txt(s, "“사무실에서 데이터만 보면 답이 나오지 않는다. 고객을 직접 만나라.” – 조 게비아(에어비앤비 공동창업자)", { x: 0.4, y: 4.7, w: 9.2, h: 0.5, fontSize: 10.5, italic: true, color: TEAL, valign: "middle" });
  source(s, "Joe Gebbia 인터뷰(First Round Review); Paul Graham, “Do Things that Don’t Scale”(2013)");
  s.addNotes("에어비앤비는 디자인 씽킹을 창업 초기에 적용한 대표 사례입니다. 공동창업자 조 게비아는 RISD 디자인 전공자였고, 매출 정체의 원인을 데이터가 아니라 고객 현장에서 찾았습니다.");
}

// ======================= 06. BMC vs Lean Canvas =======================
pres.addSection({ title: "06 BMC vs 린 캔버스" });
function canvas(s, cells, colorMap) {
  // 5 columns x top 2 rows, bottom 2 cells
  const X = 0.4, Y = 1.35, W = 9.2, colW = W / 5, topH = 2.5, half = topH / 2, botY = Y + topH + 0.06, botH = 1.12;
  const pos = {
    c1: [X, Y, colW, topH], c2a: [X + colW, Y, colW, half], c2b: [X + colW, Y + half, colW, half],
    c3: [X + 2 * colW, Y, colW, topH], c4a: [X + 3 * colW, Y, colW, half], c4b: [X + 3 * colW, Y + half, colW, half],
    c5: [X + 4 * colW, Y, colW, topH], b1: [X, botY, W / 2, botH], b2: [X + W / 2, botY, W / 2, botH],
  };
  Object.entries(cells).forEach(([k, [title, body]]) => {
    const [x, y, w, h] = pos[k];
    s.addShape(pres.ShapeType.rect, { x, y, w, h, fill: { color: colorMap[k] || GRAY }, line: { color: WHITE, width: 2 }, objectName: "cell-" + k });
    txt(s, [{ text: title, options: { bold: true, color: NAVY, fontSize: 10, breakLine: true } }, { text: body, options: { fontSize: 10 } }], { x: x + 0.04, y: y + 0.02, w: w - 0.08, h: h - 0.04 });
  });
}
{
  const s = newSlide("06", "비즈니스 모델 캔버스(BMC) 9블록 – 사례: 네스프레소", "06 BMC vs 린 캔버스");
  canvas(s, {
    c1: ["⑧ 핵심 파트너", "커피머신 제조사(크룹스·드롱기 등), 커피 원두 농가, 물류 파트너"],
    c2a: ["⑦ 핵심 활동", "캡슐 생산, 마케팅·브랜딩, 매장·온라인 유통 관리"],
    c2b: ["⑥ 핵심 자원", "캡슐 특허, 생산 설비, 프리미엄 브랜드"],
    c3: ["② 가치 제안", "집에서 버튼 하나로 즐기는 카페 품질 에스프레소, 다양한 맛과 일관된 품질"],
    c4a: ["④ 고객 관계", "네스프레소 클럽 회원제, 전용 부티크 서비스"],
    c4b: ["③ 채널", "부티크 매장, 온라인·전화 주문, 백화점"],
    c5: ["① 고객 세그먼트", "프리미엄 커피를 원하는 가정·사무실 고객"],
    b1: ["⑨ 비용 구조", "캡슐 생산·유통비, 마케팅비(광고·모델), 매장 운영비"],
    b2: ["⑤ 수익원", "머신은 저렴하게, 캡슐 반복 구매로 지속 수익 (면도기-면도날 모델)"],
  }, { c3: PINK, c5: ICE, b2: ICE });
  txt(s, "Osterwalder & Pigneur(2010): 고객–가치–인프라–재무 9요소로 기존·신규 기업 모두의 비즈니스 모델을 한 장에 시각화", { x: 0.4, y: 5.0, w: 9.2, h: 0.28, fontSize: 9.5, italic: true, color: TEAL });
  source(s, "Osterwalder, A. & Pigneur, Y.(2010), Business Model Generation; Nestlé Nespresso 공개자료");
  s.addNotes("BMC는 오른쪽(고객·가치·채널·관계·수익)과 왼쪽(파트너·활동·자원·비용)을 가치제안이 연결하는 구조입니다. 네스프레소는 머신을 싸게 팔고 캡슐 반복 구매로 수익을 내는 '면도기-면도날' 패턴의 대표 사례로, 이미 작동하는 사업의 구조를 한눈에 보여줍니다.");
}
{
  const s = newSlide("06", "린 캔버스 9블록 – 사례: 우버 초기(2009~2010)", "06 BMC vs 린 캔버스");
  canvas(s, {
    c1: ["① 문제 ★", "택시 잡기 어려움, 언제 올지 모름, 현금 결제 불편\n기존 대안: 길에서 손 흔들기, 콜택시"],
    c2a: ["④ 해결책 ★", "앱 호출, GPS 실시간 위치, 자동 결제"],
    c2b: ["⑧ 핵심 지표 ★", "주간 탑승 수, 픽업 대기시간, 재이용률"],
    c3: ["③ 고유 가치 제안", "버튼 한 번으로 부르는 나만의 기사\n(Everyone’s Private Driver)"],
    c4a: ["⑨ 경쟁 우위 ★", "기사–승객 네트워크 효과, 운행 데이터"],
    c4b: ["⑤ 채널", "입소문, 추천 코드, 도시별 런칭 이벤트"],
    c5: ["② 고객 세그먼트", "도시 직장인·출장자 / 차량 보유 기사\n얼리어답터: 샌프란시스코 테크 종사자"],
    b1: ["⑦ 비용 구조", "기사 모집·인센티브, 앱 개발·서버, 마케팅"],
    b2: ["⑥ 수익원", "운행 요금의 일정 비율(수수료)"],
  }, { c1: PINK, c2a: PINK, c2b: PINK, c4a: PINK, c3: ICE });
  txt(s, "Ash Maurya(2010): ★ 4블록을 스타트업용으로 교체 – 아직 증명되지 않은 ‘가설’을 적고 검증 우선순위(①→⑨)대로 채움", { x: 0.4, y: 5.0, w: 9.2, h: 0.28, fontSize: 9.5, italic: true, color: TEAL });
  source(s, "Maurya, A.(2012), Running Lean; Uber 초기 서비스(UberCab, 2010) 공개자료 재구성");
  s.addNotes("린 캔버스는 BMC의 핵심 파트너→문제, 핵심 활동→해결책, 핵심 자원→핵심 지표, 고객 관계→경쟁 우위로 바꾼 것입니다. 스타트업은 파트너나 자원보다 '고객의 문제가 진짜인가'가 먼저이기 때문입니다. 우버 초기 모델로 채워 보았습니다.");
}
{
  const s = newSlide("06", "BMC vs 린 캔버스 비교: 언제 무엇을 쓸 것인가", "06 BMC vs 린 캔버스");
  const head = { bold: true, color: WHITE, fill: { color: NAVY }, align: "center", valign: "middle", fontSize: 11 };
  const k = { bold: true, color: NAVY, fill: { color: GRAY }, fontSize: 10.5, valign: "middle" };
  const v = { fontSize: 10.5, valign: "middle", color: TXT };
  const rows = [
    [{ text: "구분", options: head }, { text: "비즈니스 모델 캔버스(BMC)", options: head }, { text: "린 캔버스(Lean Canvas)", options: head }],
    [{ text: "개발자·연도", options: k }, { text: "Osterwalder & Pigneur, 2010", options: v }, { text: "Ash Maurya, 2010", options: v }],
    [{ text: "주 대상", options: k }, { text: "기존 기업·사업 구조 분석/혁신", options: v }, { text: "초기 스타트업·신사업 아이디어", options: v }],
    [{ text: "관점", options: k }, { text: "가치 전달 인프라(파트너·자원·활동) 중심", options: v }, { text: "고객 문제·해결책·검증 지표 중심", options: v }],
    [{ text: "고유 블록", options: k }, { text: "핵심 파트너·핵심 활동·핵심 자원·고객 관계", options: v }, { text: "문제·해결책·핵심 지표·경쟁 우위", options: v }],
    [{ text: "작성 내용", options: k }, { text: "현재 작동하는 ‘사실’ 정리", options: v }, { text: "검증해야 할 ‘가설’ 나열·우선순위화", options: v }],
    [{ text: "강점/한계", options: k }, { text: "전체 구조 파악에 탁월 / 시장 리스크 표현 약함", options: v }, { text: "리스크 중심 빠른 검증 / 운영 구조 표현 약함", options: v }],
  ];
  s.addTable(rows, { x: 0.4, y: 1.35, w: 9.2, colW: [1.5, 3.85, 3.85], rowH: 0.36, border: { type: "solid", pt: 1, color: "FFFFFF" }, fontFace: THEME.bodyFontFace });
  caseBox(s, 0.4, 4.05, 4.5, 1.17, "BMC가 맞는 경우: 네스프레소",
    "이미 작동하는 사업에서 ‘머신 판매’ 대신 ‘캡슐 반복 구매’로 수익 구조를 재설계 – 전체 구조 변경이 핵심", { size: 10, titleSize: 11 });
  caseBox(s, 5.1, 4.05, 4.5, 1.17, "린 캔버스가 맞는 경우: 우버 초기",
    "‘사람들이 낯선 기사의 차를 앱으로 부를까?’라는 문제·해결 가설을 샌프란시스코에서 먼저 검증", { size: 10, titleSize: 11 });
  source(s, "Osterwalder & Pigneur(2010); Maurya(2012) Running Lean");
  s.addNotes("정리하면 BMC는 '어떻게 돌아가는 사업인가'를, 린 캔버스는 '무엇을 먼저 검증해야 하는가'를 보여줍니다. 실무에서는 초기에 린 캔버스로 가설을 검증하고, 사업이 안정되면 BMC로 운영 구조를 설계하는 순서로 함께 쓰는 것이 일반적입니다.");
}

// ======================= 07. Startup Owner's Manual =======================
pres.addSection({ title: "07 스타트업 오너스 매뉴얼" });
{
  const s = newSlide("07", "스타트업 오너스 매뉴얼: 고객개발 4단계", "07 스타트업 오너스 매뉴얼");
  txt(s, "Steve Blank & Bob Dorf(2012) – “스타트업은 대기업의 축소판이 아니라, 반복 가능하고 확장 가능한 비즈니스 모델을 ‘탐색’하는 임시 조직이다”", { x: 0.4, y: 1.3, w: 9.2, h: 0.45, fontSize: 10.5, italic: true });
  // search vs execute bands
  box(s, 0.4, 1.85, 4.5, 0.32, ICE, "band-search");
  txt(s, "탐색(Search) – 비즈니스 모델 검증", { x: 0.4, y: 1.85, w: 4.5, h: 0.32, fontSize: 10.5, bold: true, color: NAVY, align: "center", valign: "middle" });
  box(s, 5.1, 1.85, 4.5, 0.32, PINK, "band-exec");
  txt(s, "실행(Execute) – 비즈니스 모델 확장", { x: 5.1, y: 1.85, w: 4.5, h: 0.32, fontSize: 10.5, bold: true, color: RED, align: "center", valign: "middle" });
  const st = [["1", "고객 발굴", "Customer Discovery", "문제·고객 가설을 현장 인터뷰로 검증", TEAL], ["2", "고객 검증", "Customer Validation", "실제 판매로 반복 가능한 판매 모델 확인", TEAL], ["3", "고객 창출", "Customer Creation", "검증된 모델로 수요 창출·마케팅 확대", NAVY], ["4", "회사 설립", "Company Building", "스타트업 → 실행 중심 조직·부서 구축", NAVY]];
  st.forEach(([n, ko, en, d, c], i) => {
    const x = 0.4 + i * 2.33;
    s.addShape(pres.ShapeType.chevron, { x, y: 2.3, w: 2.25, h: 0.62, fill: { color: c }, line: { type: "none" }, objectName: "cd-" + i });
    txt(s, `${n}. ${ko}`, { x: x + 0.25, y: 2.3, w: 1.75, h: 0.62, fontSize: 13, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    txt(s, [{ text: en, options: { italic: true, bold: true, color: c, breakLine: true } }, { text: d }], { x, y: 2.97, w: 2.2, h: 0.75, fontSize: 10, align: "center" });
  });
  txt(s, "↺ 검증 실패 시 1단계로 되돌아가 피벗(Pivot) – 실패가 아닌 학습", { x: 0.4, y: 3.72, w: 9.2, h: 0.28, fontSize: 10.5, bold: true, color: RED });
  caseBox(s, 0.4, 4.05, 9.2, 1.17, "웹밴 vs 고객개발 – 블랭크가 책에서 든 반면교사",
    "웹밴은 1단계(고객 발굴)·2단계(검증)를 건너뛰고 곧바로 3·4단계(대규모 마케팅·물류센터·조직 확장)를 실행했다. 사업계획서상의 ‘가정’을 ‘사실’로 착각한 결과, 약 8억 달러를 쓰고 2001년 파산했다.", { size: 10.5 });
  source(s, "Blank, S. & Dorf, B.(2012), The Startup Owner’s Manual, K&S Ranch; Blank, S.(2005), The Four Steps to the Epiphany");
  s.addNotes("스타트업 오너스 매뉴얼의 핵심은 '제품개발'과 나란히 '고객개발' 프로세스를 운영하라는 것입니다. 1·2단계는 비즈니스 모델을 탐색하는 단계, 3·4단계는 검증된 모델을 실행하는 단계입니다. 검증에 실패하면 피벗해 다시 1단계로 돌아갑니다. 웹밴은 탐색 없이 실행부터 한 대표적 실패 사례입니다.");
}
{
  const s = newSlide("07", "고객 발굴 실행법: “Get out of the building”", "07 스타트업 오너스 매뉴얼");
  const ph = [["1", "가설 수립", "비즈니스 모델 캔버스 9블록을 ‘가설’로 작성"], ["2", "문제 검증", "고객이 정말 그 문제를 겪는가? 인터뷰로 확인"], ["3", "해결책 검증", "MVP를 보여주고 고객 반응 측정"], ["4", "검증 또는 피벗", "계속할지, 방향을 바꿀지 결정"]];
  ph.forEach(([n, h, d], i) => {
    const y = 1.35 + i * 0.82;
    s.addShape(pres.ShapeType.ellipse, { x: 0.4, y: y + 0.08, w: 0.56, h: 0.56, fill: { color: i === 3 ? RED : TEAL }, line: { type: "none" }, objectName: "ph-dot-" + i });
    txt(s, n, { x: 0.4, y: y + 0.08, w: 0.56, h: 0.56, fontSize: 15, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    txt(s, [{ text: h, options: { fontSize: 13, bold: true, color: NAVY, breakLine: true } }, { text: d, options: { fontSize: 10.5 } }], { x: 1.08, y, w: 3.7, h: 0.72, valign: "middle" });
  });
  caseBox(s, 5.0, 1.35, 4.6, 3.87, "배달의민족(우아한형제들), 2010",
    [
      { text: "가설: ", options: { bold: true } }, { text: "사람들은 배달 음식점 정보를 쉽게 찾고 싶어한다", options: { breakLine: true } },
      { text: " ", options: { fontSize: 5, breakLine: true } },
      { text: "현장 검증: ", options: { bold: true } }, { text: "창업팀이 직접 거리와 아파트 단지를 돌며 버려진 전단지를 수집해 음식점 데이터를 구축", options: { breakLine: true } },
      { text: " ", options: { fontSize: 5, breakLine: true } },
      { text: "문제 재정의: ", options: { bold: true } }, { text: "전단지 정보가 흩어져 있다는 고객 불편 + 광고 효과를 알 수 없다는 사장님 불편을 동시에 확인", options: { breakLine: true } },
      { text: " ", options: { fontSize: 5, breakLine: true } },
      { text: "결과: ", options: { bold: true } }, { text: "양면 고객의 문제를 검증한 뒤 서비스 확장 → 2019년 딜리버리히어로가 약 40억 달러 가치로 인수 합의", options: { color: RED, bold: true } },
    ], { size: 10.5 });
  txt(s, "핵심 원칙: 사무실 안에는 사실(Fact)이 없다. 모든 가설은 고객을 만나 검증한다.", { x: 0.4, y: 4.75, w: 4.4, h: 0.47, fontSize: 10.5, bold: true, color: RED, valign: "middle" });
  source(s, "Blank & Dorf(2012); 우아한형제들 창업 스토리(언론 보도); Delivery Hero 발표(2019.12)");
  s.addNotes("고객 발굴은 BMC 9블록을 가설로 적고, 사무실 밖으로 나가 고객을 만나 하나씩 검증하는 과정입니다. 배달의민족 창업팀이 전단지를 직접 주우며 데이터를 모은 일화는 국내의 대표적인 'Get out of the building' 사례입니다.");
}

// ======================= 08. 종합 =======================
pres.addSection({ title: "08 종합" });
{
  const s = newSlide("08", "종합: 설문 속 실패 원인을 막는 방법론과 사례", "08 종합");
  const head = { bold: true, color: WHITE, fill: { color: NAVY }, align: "center", valign: "middle", fontSize: 11 };
  const k = { bold: true, color: RED, fill: { color: PINK }, fontSize: 10.5, valign: "middle" };
  const v = { fontSize: 10.5, valign: "middle", color: TXT };
  const vb = { fontSize: 10.5, valign: "middle", color: NAVY, bold: true };
  const rows = [
    [{ text: "설문 속 실패 원인(증상)", options: head }, { text: "예방하는 방법론", options: head }, { text: "실패 사례", options: head }, { text: "성공 사례", options: head }],
    [{ text: "시장 니즈 없음 (42%)", options: k }, { text: "디자인 씽킹 · 고객 발굴", options: vb }, { text: "주서로, 퀴비", options: v }, { text: "에어비앤비, GE 헬스케어", options: v }],
    [{ text: "자금 소진 (29%)", options: k }, { text: "고객개발 4단계(탐색→실행)", options: vb }, { text: "웹밴", options: v }, { text: "자포스, 드롭박스", options: v }],
    [{ text: "비즈니스 모델 부재 (17%)", options: k }, { text: "BMC · 린 캔버스", options: vb }, { text: "주서로(수익 모델 지속 불가)", options: v }, { text: "네스프레소, 우버", options: v }],
    [{ text: "기술·제품 사업화 실패", options: k }, { text: "졸리 모델 · TRL", options: vb }, { text: "제록스 PARC(GUI 사업화 실패)", options: v }, { text: "3M 포스트잇", options: v }],
  ];
  s.addTable(rows, { x: 0.4, y: 1.35, w: 9.2, colW: [2.4, 2.4, 2.2, 2.2], rowH: 0.48, border: { type: "solid", pt: 1, color: "FFFFFF" }, fontFace: THEME.bodyFontFace });
  box(s, 0.4, 4.0, 9.2, 1.22, NAVY, "closing");
  txt(s, [
    { text: "창업 실패의 진짜 원인은 ‘돈’이나 ‘운’이 아니라 ‘방법’이다", options: { fontSize: 15, bold: true, breakLine: true } },
    { text: "기술사업화(졸리) → 고객 공감(디자인 씽킹) → 모델 설계(BMC·린 캔버스) → 현장 검증(고객개발)의 순서를 숙지하고 창업하라", options: { fontSize: 11 } },
  ], { x: 0.6, y: 4.0, w: 8.8, h: 1.22, color: WHITE, valign: "middle", align: "center" });
  source(s, "본 강의 종합(CB Insights; Startup Genome; Jolly 1997; Osterwalder 2010; Maurya 2012; Blank & Dorf 2012)");
  s.addNotes("설문에서 창업자들이 꼽은 실패 원인들은 모두 이번 강의에서 다룬 방법론으로 예방할 수 있습니다. 각 원인에 대응하는 방법론과 실패·성공 사례를 다시 정리했습니다. 창업 실패의 진짜 원인은 '방법을 모르고 창업하는 것'입니다.");
}

(async () => {
  await pres.writeFile({ fileName: "startup_theory.pptx" });
  await applyTheme("startup_theory.pptx", THEME);
  console.log("done");
})();
