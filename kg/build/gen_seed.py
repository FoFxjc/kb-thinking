import csv, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
import seed_v03
from seed_v03 import TIER, JUR
from seed_concepts import C, R

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "seed")
os.makedirs(OUT, exist_ok=True)
VERSION = "seed-v0.3"

SCHEME = {"asset": "asset_class", "inst": "instrument", "risk": "risk", "metric": "metric",
          "strat": "strategy", "macro": "macro", "market": "market", "suit": "suitability",
          "behav": "behavioral", "term": "terms", "local": "scheme_local"}
REF = {
    "instrument": ("FIBO - Financial Industry Business Ontology (EDM Council, MIT)", "https://spec.edmcouncil.org/fibo/"),
    "asset_class": ("Investor.gov Glossary (U.S. SEC)", "https://www.investor.gov/introduction-investing/investing-basics/glossary"),
    "risk": ("Investor.gov Glossary (U.S. SEC)", "https://www.investor.gov/introduction-investing/investing-basics/glossary"),
    "metric": ("Investor.gov Glossary (U.S. SEC)", "https://www.investor.gov/introduction-investing/investing-basics/glossary"),
    "strategy": ("Investor.gov Glossary (U.S. SEC)", "https://www.investor.gov/introduction-investing/investing-basics/glossary"),
    "market": ("Investor.gov Glossary (U.S. SEC)", "https://www.investor.gov/introduction-investing/investing-basics/glossary"),
    "macro": ("Central bank / statistics agency glossary (to be selected)", ""),
    "suitability": ("Local regulator suitability rules (to be selected)", ""),
    "behavioral": ("Behavioral finance literature (to be cited)", ""),
    "terms": ("Fund / product offering documents and local regulator rules (to be selected)", ""),
    "scheme_local": ("MAS / CPF Board / IRAS official pages", "https://www.mas.gov.sg/"),
}
CJK = re.compile(r"[一-鿿]")

def lang_of(t):
    return "zh" if CJK.search(t) else "en"

def norm(t):
    t = unicodedata.normalize("NFKC", t).lower().strip()
    t = re.sub(r"[\-_]+", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t

ZH_PROPER = set("久期 国债 债基 股基 货基 定投 止损 对冲 加息 降息 通胀 通缩 牛市 熊市 票息 股息 派息 净值 年化 公募 私募 固收 凸性 杠杆 择时 期权 期货 保本 刚兑 年金 利差 评级 市值 久期 回撤 复利 分红 估值 做空 卖空 信托 理财 定投 免疫".split())
EN_PROPER = {"immunization","volatility","diversification","rebalancing","hedging","compounding","annuity","sharpe","sortino",
             "convexity","deflation","inflation","recession","dividend","equities","bonds","securities","derivatives","alternatives",
             "futures","options","swaps","stocks","shares","reits","perpetual","endowment","commodities","gold","unemployment","overconfidence","anchoring","herding","payout ratio"}
def kind_of(t):
    n = norm(t)
    if re.fullmatch(r"[A-Z0-9/&.\-]{2,8}", t) and any(ch.isalpha() for ch in t):
        return "abbr" if len(re.sub(r"[^A-Za-z0-9]", "", t)) >= 3 else "hidden"
    if lang_of(t) == "zh":
        return "alt" if len(t) >= 3 or t in ZH_PROPER else "hidden"
    words = n.split()
    if len(words) >= 2:
        return "alt"
    return "alt" if n in EN_PROPER else "hidden"

SCOPE = {
 "suit.accredited_investor": "SFA s4A individual tests (verify current MAS rules): net personal assets > S$2m (primary residence counted up to S$1m), or net financial assets > S$1m, or income >= S$300k in the preceding 12 months; opt-in required and typically reconfirmed annually.",
 "suit.expert_investor": "SFA s4A; verify current definition with MAS.",
 "local.srs": "Verify with IRAS: annual contribution cap (S$15,300 for citizens/PRs, S$35,700 for foreigners at time of writing); withdrawals after statutory retirement age are 50% taxable, spread over up to 10 years; early withdrawal is fully taxable plus a 5% penalty.",
 "local.cpfis": "Verify with CPF Board: minimum OA balance S$20,000 and SA balance S$40,000 before investing; up to 35% of investible savings in shares/property funds and 10% in gold (OA); SA scope narrower; Self-Awareness Questionnaire required.",
 "local.cpf": "Verify CPF interest rates with CPF Board (OA 2.5% floor, SA/MA/RA 4% floor at time of writing, plus extra interest on first tiers).",
 "local.sip": "Listed SIPs (e.g. structured warrants, leveraged ETFs, futures) require a Customer Account Review; unlisted SIPs (structured notes, certain funds, structured deposits, leveraged FX, certain ILPs) require a Customer Knowledge Assessment. Verify current MAS notices.",
 "local.cka": "Pass criteria include relevant education, work experience or prior transactions; validity period set by MAS notices (verify).",
 "local.car": "As for CKA; validity period set by MAS notices (verify).",
 "inst.ssb": "Minimum S$500, individual holding cap (S$200,000 at time of writing); buy with cash or SRS, not CPF. Verify with MAS.",
 "inst.sgs": "Minimum S$1,000; eligible for cash, SRS and CPFIS; no early redemption, secondary-market sale may be above or below cost.",
 "inst.t_bill": "Singapore T-bills: 6-month and 1-year, minimum S$1,000; cash, SRS or CPF eligible.",
 "term.no_capital_gains_tax": "Singapore individuals; frequent trading may be treated as income in rare cases. Verify with IRAS.",
 "inst.unit_trust": "Singapore term; most are EIPs but some (e.g. with derivatives) are SIPs.",
 "inst.ilp": "Many ILPs are SIPs; protection cost rises with age and can erode cash value. Not a savings guarantee.",
 "inst.endowment_plan": "Guaranteed and non-guaranteed components; surrender before maturity may return less than premiums paid.",
 "macro.sora": "Replaced SIBOR/SOR as the SGD benchmark; floating-rate mortgages and products reference compounded SORA.",
 "metric.return": "Distinct from metric.yield: in bond contexts the Chinese '收益率' means yield, not return.",
 "metric.yield": "Chinese '收益率' maps here by default in bond contexts; total return is metric.return.",
 "metric.duration": "Macaulay duration is a time measure; modified duration is the price-sensitivity measure.",
 "metric.annualized_return": "Short-period annualised figures (e.g. 7-day annualised yield) are extrapolations, not achievable returns.",
 "metric.turnover": "Portfolio turnover; the Chinese '换手率' alone usually means stock/market trading turnover.",
 "inst.corporate_bond": "In mainland China 公司债 (CSRC) and 企业债 (NDRC) are distinct instruments.",
 "inst.money_market_fund": "Typical product risk rating R1 (lowest); principal not guaranteed. Matching to investors is done by the suitability rule layer.",
 "inst.government_bond": "Typical product risk rating R1-R2 depending on duration; long-dated bonds carry significant interest rate risk.",
 "inst.bond_fund": "Typical product risk rating R2-R3.",
 "inst.balanced_fund": "Typical product risk rating R3-R4.",
 "inst.equity_fund": "Typical product risk rating R4.",
 "inst.private_fund": "Typical product risk rating R4-R5; qualified investors only.",
 "inst.derivative": "Retail access is subject to jurisdiction-specific suitability tests (e.g. SIP CKA/CAR in Singapore, exchange-set thresholds in mainland China).",
 "inst.structured_deposit": "Classified as a deposit in mainland China (on balance sheet, deposit insurance); return is not guaranteed.",
 "inst.wealth_management_product": "Post-2018 mainland rules: NAV-based, no guarantee of principal or return; broader term 资管产品 covers funds, trusts and WMPs.",
 "inst.cds": "Classified here as a swap (ISDA); commonly referred to as a credit derivative.",
 "inst.inflation_linked_bond": "TIPS are the US variant; other markets have their own linkers.",
 "strat.dca": "Smooths purchase cost; must not be described as reducing risk or raising return (mainland fund marketing rules).",
 "suit.steady": "Mainland China five-level scale: C1 谨慎型, C2 稳健型, C3 平衡型, C4 成长型, C5 进取型. Do not merge 稳健型 with 平衡型.",
 "suit.professional_investor": "Mainland: 专业投资者 under the suitability measures; Singapore: Accredited / Expert / Institutional investor (SFA). Thresholds differ.",
 "suit.retail_investor": "Mainland: 普通投资者; Singapore: retail client. Derivatives access for retail requires additional assessment.",
 "term.past_performance": "Always present with 'not indicative of future results'.",
 "market.risk_free_rate": "Proxy differs by market (e.g. T-bills, SORA, DR007).",
 "suit.investor_risk_category": "Jurisdictions use finer scales (e.g. five levels C1-C5 in mainland China); map local levels onto these three types.",
 "suit.conservative": "Generic type; map to local regulatory levels.",
 "suit.balanced": "Generic type; in mainland China '稳健型' and '平衡型' are distinct levels - do not merge.",
 "suit.aggressive": "Generic type; map to local regulatory levels.",
 "suit.qualified_investor": "Mainland private-fund threshold (financial assets >= RMB 3m or income tests) differs from Singapore accredited-investor tests (e.g. net personal assets >= S$2m); state the jurisdiction.",
 "suit.product_risk_rating": "Scales are firm/jurisdiction-specific (e.g. R1-R5).",
 "asset.private_equity": "Abbreviation 'PE' is shared with the P/E ratio (metric.pe); disambiguate by context.",
 "metric.pe": "Abbreviation 'PE' is shared with private equity (asset.private_equity); disambiguate by context.",
 "macro.yield_curve_inversion": "Historically a leading recession indicator, not a guarantee.",
}
DEFAULT_CONF = {"is_a": 1.0, "part_of": 1.0, "input_of": 1.0, "belongs_to": 1.0, "opposite_of": 0.95,
                "measures": 0.95, "exposed_to": 0.9, "mitigates": 0.85, "affects": 0.85, "related": 0.75}
for y in R:
    if y.get("conf") is None:
        y["conf"] = DEFAULT_CONF[y["rel"]]
concepts, labels, relations, evidence = [], [], [], []
lb = rl = ev = 0

def add_ev(target_type, target_id, etype, source, locator="", lookup="", note=""):
    global ev
    ev += 1
    evidence.append(dict(evidence_id=f"ev-{ev:06d}", target_type=target_type, target_id=target_id,
                         evidence_type=etype, source_name=source, locator=locator, lookup_term=lookup,
                         verified="false", doc_id="", chunk_id="", quote="", note=note, created_by=VERSION))

for x in C:
    scheme = SCHEME[x["id"].split(".")[0]]
    concepts.append(dict(concept_id=x["id"], scheme=scheme, pref_zh=x["zh"], pref_en=x["en"],
                         definition_zh=x["dzh"], definition_en=x["den"], scope_note=SCOPE.get(x["id"], ""),
                         jurisdiction=JUR.get(x["id"], "global"), tier=TIER.get(x["id"], 2),
                         layer="base", status="draft", version=1))
    seen = set()
    for text, kind in [(x["zh"], "pref"), (x["en"], "pref")] + [(a, None) for a in x["alts"]] + [(h, "hidden") for h in x.get("hidden", [])]:
        lang = lang_of(text)
        key = (lang, norm(text))
        if key in seen:
            continue
        seen.add(key)
        lb += 1
        labels.append(dict(label_id=f"lb-{lb:06d}", concept_id=x["id"], text=text, lang=lang,
                           kind=kind or kind_of(text), normalized=norm(text), layer="base", status="draft"))
    add_ev("concept", x["id"], "authoring", "kb-thinking seed v0.2", note="LLM-drafted, revised after independent review (docs/09); pending expert review")
    src, loc = REF[scheme]
    add_ev("concept", x["id"], "reference", src, loc, x["en"], note="Verify definition against source; do not copy text")

def add_rel(src, rel, dst, polarity=None, conf=1.0, note=None):
    global rl
    rl += 1
    rid = f"rl-{rl:06d}"
    relations.append(dict(relation_id=rid, src=src, rel=rel, dst=dst,
                          polarity="" if polarity is None else polarity,
                          confidence=conf, note=note or "", layer="base", status="draft"))
    add_ev("relation", rid, "authoring", "kb-thinking seed v0.2", note="LLM-drafted, revised after independent review (docs/09); pending expert review")

for x in C:
    for p in x["parents"]:
        add_rel(x["id"], "is_a", p)
for y in R:
    add_rel(y["src"], y["rel"], y["dst"], y["polarity"], y["conf"], y["note"])

def write(name, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

write("concept.csv", concepts)
write("label.csv", labels)
write("relation.csv", relations)
write("evidence.csv", evidence)

def export_tier(name, max_tier):
    d = os.path.join(OUT, "tiers", name); os.makedirs(d, exist_ok=True)
    cids = {c["concept_id"] for c in concepts if c["tier"] <= max_tier}
    cs = [c for c in concepts if c["concept_id"] in cids]
    ls = [l for l in labels if l["concept_id"] in cids]
    rs = [r for r in relations if r["src"] in cids and r["dst"] in cids]
    keep = cids | {r["relation_id"] for r in rs} | {l["label_id"] for l in ls}
    es = [e for e in evidence if e["target_id"] in keep]
    for fn, rows in [("concept.csv", cs), ("label.csv", ls), ("relation.csv", rs), ("evidence.csv", es)]:
        with open(os.path.join(d, fn), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"tier {name}: concepts={len(cs)} labels={len(ls)} relations={len(rs)} evidence={len(es)}")
export_tier("basic", 1)
export_tier("advanced", 2)
print(f"concepts={len(concepts)} labels={len(labels)} relations={len(relations)} evidence={len(evidence)}")
