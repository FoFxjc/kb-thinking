# v0.3: applied after seed_v02. Implements docs/09-kg-rules.md, fixes round-2 findings,
# adds Singapore localisation, CN high-frequency terms, tiers and jurisdiction.
import seed_v02 as v2
from seed_v02 import C, R, byid, concept, drop_alts, add_alts, hidden, redefine, drop_rel, rel, new, reparent

JUR = {}      # concept_id -> SG / CN (default global)
TIER = {}     # concept_id -> 1 / 3 (default 2)
def jur(cid, j): JUR[cid] = j
def tier(*cids_tier):
    t = cids_tier[-1]
    for cid in cids_tier[:-1]: TIER[cid] = t

# ------------------------------------------------------------ B. round-2 regressions
reparent("asset.gold", "asset.commodity"); drop_rel("asset.gold", "belongs_to", "asset.commodity")
drop_alts("metric.alpha", "超额收益率"); add_alts("metric.excess_return", "超额收益率")
drop_alts("macro.rate_hike", "利率上升", "利率上行"); drop_alts("macro.rate_cut", "利率下降", "利率下行")
new("macro.rates_rising", [], "利率上行", "Rising interest rates",
  "市场利率或债券收益率上升的阶段；可由加息、通胀预期或供需变化引起。",
  "A phase of rising market interest rates or bond yields, driven by policy tightening, inflation expectations or supply and demand.",
  ["利率上升", "收益率上行", "Rising rates"])
new("macro.rates_falling", [], "利率下行", "Falling interest rates",
  "市场利率或债券收益率下降的阶段。",
  "A phase of falling market interest rates or bond yields.",
  ["利率下降", "收益率下行", "Falling rates"])
rel("macro.rates_rising", "opposite_of", "macro.rates_falling")
rel("macro.rate_hike", "affects", "macro.rates_rising", 1, conf=0.8, note="Policy tightening usually, not always, lifts market rates")
rel("macro.rates_rising", "affects", "market.bond_price", -1)
rel("macro.rates_rising", "related", "macro.interest_rate")
drop_alts("metric.cvar", "ES"); hidden("metric.cvar", "ES")
drop_alts("risk.call", "Prepayment risk")
new("risk.prepayment", ["risk.interest_rate"], "提前偿付风险", "Prepayment risk",
  "借款人提前偿还本金（常见于按揭和资产支持证券），使投资者被迫在较低利率下再投资的风险。",
  "The risk that borrowers repay principal early (common in mortgages and asset-backed securities), forcing reinvestment at lower rates.",
  [])
rel("risk.prepayment", "related", "risk.call")
drop_rel("term.nav_based", "opposite_of", "term.implicit_guarantee"); rel("term.nav_based", "related", "term.implicit_guarantee", note="NAV-based products replace implicitly guaranteed ones")
drop_rel("metric.yield", "affects", "market.bond_price"); rel("metric.yield", "related", "market.bond_price", conf=0.95, note="Price and yield are two expressions of the same valuation and move inversely")
drop_rel("macro.inflation", "affects", "risk.inflation"); rel("macro.inflation", "related", "risk.inflation")
drop_rel("macro.exchange_rate", "affects", "risk.fx"); rel("macro.exchange_rate", "related", "risk.fx")
for s_, d_ in [("macro.rate_hike", "macro.monetary_policy"), ("macro.rate_cut", "macro.monetary_policy"),
               ("market.ipo", "market.primary_market"), ("strat.glide_path", "inst.target_date_fund")]:
    drop_rel(s_, "part_of", d_); rel(s_, "related", d_)
# fees / redemption: composition, not classification
for f in ["term.management_fee", "term.custody_fee", "term.subscription_redemption_fee", "term.performance_fee"]:
    reparent(f); rel(f, "part_of", "term.fee_structure")
new("term.fund_structure", [], "基金运作方式", "Fund dealing structure",
  "基金接受申购赎回的安排方式，分为开放式和封闭式。",
  "How a fund handles subscriptions and redemptions: open-ended or closed-ended.",
  [])
redefine("term.open_end", zh="开放式基金", en="Open-ended fund"); drop_alts("term.open_end", "开放式基金", "Open-end fund"); add_alts("term.open_end", "开放式", "Open-end fund")
redefine("term.closed_end", zh="封闭式基金", en="Closed-ended fund"); drop_alts("term.closed_end", "封闭式基金", "Closed-end fund"); add_alts("term.closed_end", "封闭式", "Closed-end fund")
reparent("term.open_end", "term.fund_structure"); reparent("term.closed_end", "term.fund_structure")
reparent("term.lock_up"); rel("term.lock_up", "part_of", "term.redemption_terms")
rel("term.fund_structure", "related", "term.redemption_terms")
# compounding -> terms; cross-border -> scheme_local
for old, newid in [("metric.compounding", "term.compounding"), ("inst.cross_border_channel", "local.cross_border_channel")]:
    concept(old)["id"] = newid; byid[newid] = byid.pop(old)
    for y in R:
        for k in ("src", "dst"):
            if y[k] == old: y[k] = newid
jur("local.cross_border_channel", "CN")
# fund two axes: type nodes is_a fund only; offering axis separate; 'commonly offered as' via related
for f in ["inst.etf", "inst.index_fund", "inst.money_market_fund", "inst.bond_fund",
          "inst.equity_fund", "inst.balanced_fund", "inst.fund_of_funds", "inst.target_date_fund"]:
    reparent(f, "inst.fund"); rel(f, "related", "inst.mutual_fund", note="Commonly offered publicly; private variants exist")
new("inst.asset_management_product", ["inst.financial_instrument"], "资管产品", "Asset management product",
  "由持牌机构受托管理投资者资金的集合投资产品的统称，包括基金、理财产品、信托计划等。",
  "The umbrella term for pooled products managed by licensed institutions on behalf of investors, including funds, wealth management products and trust schemes.",
  ["资产管理产品"])
reparent("inst.fund", "inst.asset_management_product"); reparent("inst.wealth_management_product", "inst.asset_management_product")
jur("inst.wealth_management_product", "CN")
# input_of coverage
for s_, d_ in [("metric.excess_return", "metric.sharpe"), ("metric.volatility", "metric.sharpe"),
               ("metric.excess_return", "metric.information_ratio"), ("metric.beta", "metric.alpha"),
               ("metric.standard_deviation", "metric.volatility"), ("metric.market_cap", "metric.pb"),
               ("metric.dividend_yield", "strat.income")]:
    if d_.startswith("metric."): drop_rel(s_, "related", d_); rel(s_, "input_of", d_)
drop_rel("metric.standard_deviation", "related", "metric.volatility")
rel("metric.max_drawdown", "measures", "risk.tail", conf=0.8)
# payout ratio; enterprise bond etc (CN)
new("metric.payout_ratio", [], "股利支付率", "Dividend payout ratio",
  "公司分红占净利润的比例。",
  "Dividends paid as a proportion of net profit.",
  ["分红率", "派息率", "Payout ratio"])
rel("metric.payout_ratio", "related", "metric.dividend_yield")
new("inst.enterprise_bond", ["inst.credit_bond"], "企业债", "Enterprise bond (CN)",
  "中国大陆由发改委审核、主要由国企和城投平台发行的债券，与证监会监管的公司债为不同品种。",
  "A mainland China bond category approved by the NDRC and issued mainly by state-owned enterprises and local financing vehicles; distinct from CSRC-regulated corporate bonds.",
  []); jur("inst.enterprise_bond", "CN")
new("inst.financial_bond", ["inst.bond"], "金融债", "Financial bond",
  "由银行和其他金融机构发行的债券。", "A bond issued by banks and other financial institutions.", ["金融债券"])
new("inst.local_government_bond", ["inst.government_bond"], "地方政府债", "Local government bond",
  "由地方政府发行的债券。", "A bond issued by a sub-national government.", ["地方债", "Municipal bond"])
new("inst.ncd", ["inst.money_market_instrument"], "同业存单", "Negotiable certificate of deposit",
  "银行在银行间市场发行的可转让定期存款凭证。", "A transferable time-deposit certificate issued by banks in the interbank market.", ["NCD"])
new("inst.trust_scheme", ["inst.asset_management_product"], "信托计划", "Trust scheme",
  "由信托公司设立、受托管理投资者资金的集合投资计划。", "A pooled investment scheme established and managed by a trust company.", ["信托产品", "集合资金信托"]); jur("inst.trust_scheme", "CN")
new("strat.fixed_income_plus", ["strat.asset_allocation"], "固收+", "Fixed income plus",
  "以债券为底仓、搭配少量权益或衍生品以增强收益的配置策略。", "An allocation that holds mostly bonds with a small equity or derivative sleeve to enhance returns.", ["固收加", "Fixed-income plus"])
rel("strat.fixed_income_plus", "related", "inst.balanced_fund"); rel("strat.fixed_income_plus", "exposed_to", "risk.equity_price", conf=0.8)
new("metric.seven_day_yield", ["metric.yield"], "七日年化收益率", "Seven-day annualised yield",
  "货币基金最近七天收益折算成年化后的数值；仅为换算，不代表未来收益。", "A money market fund's last seven days of income annualised; an extrapolation, not a forecast.", ["7日年化", "七日年化"])
rel("metric.seven_day_yield", "related", "inst.money_market_fund")
new("term.expected_return_product", ["term.redemption_terms"], "预期收益型产品", "Expected-return product",
  "以预期收益率而非净值表述收益的产品形态；资管新规后逐步被净值型产品取代。", "A product form quoting an expected return rather than a net asset value; being phased out in favour of NAV-based products.", []); jur("term.expected_return_product", "CN")
reparent("term.expected_return_product"); rel("term.expected_return_product", "opposite_of", "term.nav_based")
new("macro.lpr", ["macro.policy_rate"], "贷款市场报价利率", "Loan prime rate",
  "中国大陆银行贷款定价的基准利率。", "The benchmark lending rate in mainland China.", ["LPR"]); jur("macro.lpr", "CN")

# ------------------------------------------------------------ investor classification: three subtrees
# 1) generic risk category (global): conservative / balanced / aggressive
drop_alts("suit.balanced", "C3"); drop_alts("suit.aggressive", "C5"); drop_alts("suit.conservative", "保守型")
add_alts("suit.conservative", "保守型投资者"); add_alts("suit.aggressive", "进取型")
# 2) CN five-level scale (jurisdiction CN)
for cid in ["suit.cautious", "suit.steady", "suit.growth"]:
    reparent(cid)
new("suit.cn_risk_level", ["suit.investor_risk_category"], "大陆投资者风险等级", "Mainland China investor risk level",
  "中国大陆适当性管理下按风险承受能力划分的五级：C1 谨慎型、C2 稳健型、C3 平衡型、C4 成长型、C5 进取型。",
  "The five-level risk tolerance scale under mainland China suitability rules: C1 cautious, C2 steady, C3 balanced, C4 growth, C5 aggressive.",
  ["C1-C5", "五级分类"]); jur("suit.cn_risk_level", "CN")
for cid in ["suit.cautious", "suit.steady", "suit.growth"]:
    reparent(cid, "suit.cn_risk_level"); jur(cid, "CN")
new("suit.cn_balanced", ["suit.cn_risk_level"], "平衡型（C3）", "Balanced (C3)",
  "大陆五级分类中的第三级。", "Level three of the mainland five-level scale.", ["C3"]); jur("suit.cn_balanced", "CN")
new("suit.cn_aggressive", ["suit.cn_risk_level"], "进取型（C5）", "Aggressive (C5)",
  "大陆五级分类中的最高级。", "The top level of the mainland five-level scale.", ["C5"]); jur("suit.cn_aggressive", "CN")
rel("suit.cn_balanced", "related", "suit.balanced"); rel("suit.cn_aggressive", "related", "suit.aggressive"); rel("suit.cautious", "related", "suit.conservative")
# 3) investor qualification (by eligibility, not risk)
new("suit.investor_qualification", [], "投资者资格分类", "Investor qualification",
  "按资产、收入、知识或机构属性划分的投资者类别，决定可购买的产品范围和保护程度。",
  "Investor classes based on wealth, income, knowledge or institutional status, determining product access and the level of protection.",
  ["投资者分类"])
for cid in ["suit.retail_investor", "suit.professional_investor"]:
    reparent(cid, "suit.investor_qualification")
reparent("suit.qualified_investor", "suit.investor_qualification"); jur("suit.qualified_investor", "CN")
jur("suit.professional_investor", "CN"); drop_alts("suit.professional_investor", "Accredited investor", "Expert investor")
redefine("suit.professional_investor", en="Professional investor (CN)")
redefine("suit.retail_investor", zh="零售投资者", en="Retail investor",
  dzh="未被归入认可、专家或机构投资者的个人投资者，享有最高程度的监管保护。",
  den="An individual investor not classified as accredited, expert or institutional, receiving the highest level of regulatory protection.")
drop_alts("suit.retail_investor", "零售投资者"); add_alts("suit.retail_investor", "普通投资者", "Retail client")
new("suit.accredited_investor", ["suit.investor_qualification"], "认可投资者", "Accredited investor",
  "新加坡《证券期货法》下满足资产或收入门槛并选择加入（opt-in）的个人或实体，可获得的监管保护少于零售投资者。",
  "Under Singapore's Securities and Futures Act, an individual or entity meeting wealth or income thresholds who opts in to reduced regulatory protection.",
  ["AI", "合格投资者（新加坡）"]); jur("suit.accredited_investor", "SG")
new("suit.expert_investor", ["suit.investor_qualification"], "专家投资者", "Expert investor",
  "新加坡《证券期货法》下以投资为业或具备相应专业能力的投资者类别。",
  "A Singapore SFA class for persons whose business involves investing or who have equivalent expertise.",
  ["EI"]); jur("suit.expert_investor", "SG")
new("suit.institutional_investor", ["suit.investor_qualification"], "机构投资者", "Institutional investor",
  "银行、保险公司、基金管理人、政府机构等按机构属性认定的投资者类别。",
  "Investor class defined by institutional status, such as banks, insurers, fund managers and government bodies.",
  ["II", "机构客户"])
rel("suit.retail_investor", "opposite_of", "suit.accredited_investor")
drop_rel("suit.retail_investor", "opposite_of", "suit.professional_investor")
rel("suit.accredited_investor", "related", "suit.qualified_investor", note="Analogous classes in SG and CN; thresholds differ")
rel("suit.accredited_investor", "related", "inst.private_fund"); rel("suit.accredited_investor", "related", "inst.hedge_fund")
drop_rel("suit.professional_investor", "related", "suit.qualified_investor")
drop_rel("suit.product_risk_rating", "related", "suit.retail_investor")

# ------------------------------------------------------------ Singapore localisation
SG = [
 ("local.mas", [], "新加坡金融管理局", "Monetary Authority of Singapore",
  "新加坡的中央银行和综合金融监管机构。", "Singapore's central bank and integrated financial regulator.", ["MAS", "金管局"]),
 ("local.sfa", [], "证券期货法", "Securities and Futures Act",
  "新加坡规范资本市场产品、投资者分类和持牌活动的主要法律。", "Singapore's principal law governing capital markets products, investor classes and licensed activities.", ["SFA"]),
 ("local.faa", [], "财务顾问法", "Financial Advisers Act",
  "新加坡规范财务顾问及其代表提供投资建议的法律，要求建议有合理依据并基于了解客户。", "Singapore's law governing financial advisers and their representatives, requiring recommendations to have a reasonable basis and be based on knowing the client.", ["FAA"]),
 ("local.fair_dealing", [], "公平对待客户准则", "Fair Dealing Guidelines",
  "MAS 发布的指引，要求金融机构以客户利益为中心，提供适合目标客户的产品和有质量的建议。", "MAS guidelines requiring financial institutions to put fair dealing at the centre of their culture and to offer suitable products and quality advice.", ["Fair Dealing"]),
 ("local.sip", [], "特定投资产品", "Specified Investment Product",
  "MAS 认定为结构较复杂、零售客户购买前需评估知识或经验的产品，如结构性票据、部分基金、衍生品、结构性存款。", "Products MAS deems more complex, for which retail customers must be assessed for knowledge or experience before dealing, such as structured notes, certain funds, derivatives and structured deposits.", ["SIP", "复杂产品"]),
 ("local.eip", [], "除外投资产品", "Excluded Investment Product",
  "结构较简单、无需知识评估即可向零售客户销售的产品，如普通股票和部分 ETF；简单不等于低风险。", "Simpler products that can be sold to retail customers without a knowledge assessment, such as plain shares and some ETFs; simple does not mean low risk.", ["EIP"]),
 ("local.cka", [], "客户知识评估", "Customer Knowledge Assessment",
  "零售客户购买非上市特定投资产品前，机构对其教育背景、工作经验和投资经验的评估。", "An assessment of a retail customer's education, work experience and investment experience before dealing in unlisted Specified Investment Products.", ["CKA"]),
 ("local.car", [], "客户账户审查", "Customer Account Review",
  "零售客户交易上市特定投资产品前，机构对其相关知识和经验的审查。", "A review of a retail customer's knowledge and experience before trading listed Specified Investment Products.", ["CAR"]),
 ("local.cpf", [], "中央公积金", "Central Provident Fund",
  "新加坡的强制性社会保障储蓄计划，分为普通账户、特别账户、保健账户和退休账户。", "Singapore's mandatory social security savings scheme, with Ordinary, Special, MediSave and Retirement accounts.", ["CPF", "公积金"]),
 ("local.cpf_oa", ["local.cpf"], "公积金普通账户", "CPF Ordinary Account",
  "可用于住房、教育和获批投资的公积金账户。", "The CPF account usable for housing, education and approved investments.", ["OA", "普通账户"]),
 ("local.cpf_sa", ["local.cpf"], "公积金特别账户", "CPF Special Account",
  "用于退休储蓄、利率较高、投资范围较窄的公积金账户。", "The CPF account for retirement savings, earning a higher rate with a narrower investment scope.", ["SA", "特别账户"]),
 ("local.cpfis", [], "公积金投资计划", "CPF Investment Scheme",
  "允许会员将超过规定余额的普通账户和特别账户资金投资于获批产品的计划；股票和黄金有比例上限。", "A scheme allowing members to invest Ordinary and Special Account savings above set balances in approved products, with caps on shares and gold.", ["CPFIS"]),
 ("local.cpf_life", [], "公积金终身入息计划", "CPF LIFE",
  "以退休账户储蓄购买、提供终身每月给付的国家年金计划。", "A national annuity scheme funded from Retirement Account savings that pays monthly for life.", ["CPF LIFE", "终身入息"]),
 ("local.srs", [], "退休辅助计划", "Supplementary Retirement Scheme",
  "自愿参加的退休储蓄计划，供款可抵扣应税收入，资金可投资，退休后提取部分征税。", "A voluntary retirement savings scheme: contributions are tax-deductible, funds can be invested, and withdrawals after retirement age are partly taxable.", ["SRS"]),
 ("inst.ssb", ["inst.government_bond"], "新加坡储蓄债券", "Singapore Savings Bond",
  "面向个人发行、期限最长十年、利率逐年递增、任何月份可无罚金赎回的政府债券。", "A government bond for individuals with tenor up to ten years, step-up interest and penalty-free redemption in any month.", ["SSB", "储蓄债券"]),
 ("inst.sgs", ["inst.government_bond"], "新加坡政府债券", "Singapore Government Securities",
  "新加坡政府发行、期限两年至五十年、每半年付息、可在二级市场买卖的债券。", "Bonds issued by the Singapore government with tenors of two to fifty years, semi-annual coupons and secondary-market trading.", ["SGS"]),
 ("inst.t_bill", ["inst.government_bond"], "短期国库券", "Treasury bill",
  "期限一年以内、折价发行、到期按面值兑付的政府短期债务工具。", "Short-term government debt with tenor up to one year, issued at a discount and redeemed at par.", ["T-bill", "T-bills", "国库券"]),
 ("inst.unit_trust", ["inst.mutual_fund"], "单位信托", "Unit trust",
  "新加坡市场对公开发售的集合投资基金的常用称呼。", "The common Singapore term for a publicly offered collective investment fund.", ["Unit trusts"]),
 ("inst.ilp", ["inst.insurance_product"], "投资联结保单", "Investment-linked policy",
  "保费扣除保障成本后投资于基金、现金价值随基金表现波动的人寿保险产品。", "A life insurance product whose premiums, net of protection costs, are invested in funds, with cash value moving with fund performance.", ["ILP", "投连险（新加坡）"]),
 ("inst.endowment_plan", ["inst.insurance_product"], "储蓄保险", "Endowment plan",
  "到期或身故时给付约定金额、兼具储蓄功能的保险产品；提前退保可能损失本金。", "An insurance product paying an agreed sum at maturity or death with a savings element; early surrender may lose principal.", ["储蓄计划", "Endowment"]),
 ("inst.s_reit", ["inst.reit"], "新加坡房地产投资信托", "Singapore REIT",
  "在新加坡交易所上市的房地产投资信托。", "A real estate investment trust listed on the Singapore Exchange.", ["S-REIT", "S-REITs"]),
 ("inst.dual_currency_investment", ["inst.structured_product"], "双货币投资", "Dual currency investment",
  "挂钩汇率、到期可能以另一货币偿付本金的结构化存款类产品；本金不受保障。", "A structured deposit-like product linked to an exchange rate whose principal may be repaid in the alternate currency; principal is not protected.", ["DCI"]),
 ("market.sgx", ["market.secondary_market"], "新加坡交易所", "Singapore Exchange",
  "新加坡的证券和衍生品交易所。", "Singapore's securities and derivatives exchange.", ["SGX", "新交所"]),
 ("market.sti", ["market.index"], "海峡时报指数", "Straits Times Index",
  "新加坡股市的基准指数，由新交所主要上市公司组成。", "Singapore's benchmark equity index of leading SGX-listed companies.", ["STI"]),
 ("macro.sora", ["macro.interest_rate"], "新加坡隔夜平均利率", "Singapore Overnight Rate Average",
  "新加坡元无担保隔夜借贷的基准利率，用于浮动利率贷款和产品定价。", "The benchmark overnight unsecured borrowing rate in Singapore dollars, used to price floating-rate loans and products.", ["SORA"]),
 ("term.no_capital_gains_tax", ["term.tax"], "无资本利得税", "No capital gains tax",
  "新加坡对个人投资的资本利得不征税；股息在一级税制下免税；个人存款和政府债券利息通常免税。", "Singapore does not tax individuals' capital gains; dividends are tax-exempt under the one-tier system; individuals' bank and government bond interest is generally exempt.", []),
 ("strat.robo_advisor", ["strat.passive"], "智能投顾", "Robo-advisor",
  "以算法按风险问卷自动构建和再平衡组合的数字化投资服务。", "A digital service that builds and rebalances portfolios algorithmically from a risk questionnaire.", ["机器人投顾", "Robo advisor"]),
]
for cid, parents, zh, en, dzh, den, alts in SG:
    new(cid, parents, zh, en, dzh, den, alts); jur(cid, "SG")
jur("suit.institutional_investor", "global"); jur("inst.t_bill", "global"); jur("strat.robo_advisor", "global")
# SG relations
rel("local.sip", "opposite_of", "local.eip")
rel("local.cka", "related", "local.sip"); rel("local.car", "related", "local.sip"); rel("local.cka", "related", "suit.suitability"); rel("local.car", "related", "suit.suitability")
rel("local.sfa", "related", "suit.investor_qualification"); rel("local.faa", "related", "suit.suitability"); rel("local.fair_dealing", "related", "suit.suitability")
rel("local.mas", "related", "local.sfa"); rel("local.mas", "related", "local.faa"); rel("local.mas", "related", "macro.monetary_policy")
rel("local.cpfis", "related", "local.cpf_oa"); rel("local.cpfis", "related", "local.cpf_sa"); rel("local.cpfis", "related", "suit.retirement_planning")
rel("local.cpf_life", "related", "inst.annuity"); rel("local.cpf_life", "related", "suit.retirement_planning")
rel("local.srs", "related", "term.tax"); rel("local.srs", "related", "suit.retirement_planning")
rel("local.cpfis", "exposed_to", "risk.market", conf=0.8, note="Investing CPF savings forgoes the guaranteed CPF interest")
rel("inst.ssb", "mitigates", "risk.interest_rate", conf=0.8, note="Redeemable at par any month, so no price loss on exit")
rel("inst.ssb", "mitigates", "risk.liquidity", conf=0.9)
rel("inst.sgs", "exposed_to", "risk.interest_rate"); rel("inst.t_bill", "exposed_to", "risk.reinvestment")
rel("inst.ilp", "exposed_to", "risk.market"); rel("inst.endowment_plan", "exposed_to", "risk.liquidity"); rel("inst.endowment_plan", "related", "term.principal_protection")
rel("inst.dual_currency_investment", "exposed_to", "risk.fx"); rel("inst.dual_currency_investment", "related", "local.sip")
rel("inst.structured_product", "related", "local.sip"); rel("inst.derivative", "related", "local.sip"); rel("inst.structured_deposit", "related", "local.sip")
rel("inst.stock", "related", "local.eip"); rel("inst.etf", "related", "local.eip", conf=0.7, note="Only plain ETFs; leveraged or synthetic ETFs are SIPs")
rel("inst.s_reit", "related", "market.sgx"); rel("market.sti", "related", "market.sgx"); rel("macro.sora", "related", "market.risk_free_rate")
rel("strat.robo_advisor", "related", "strat.asset_allocation"); rel("strat.robo_advisor", "related", "strat.rebalancing")
rel("term.no_capital_gains_tax", "related", "metric.capital_gain"); rel("term.no_capital_gains_tax", "related", "market.dividend")
drop_rel("inst.derivative", "related", "suit.suitability")

# ------------------------------------------------------------ tiers
tier("asset.equity","asset.fixed_income","asset.cash","asset.alternative","asset.real_estate","asset.commodity","asset.gold",
     "inst.financial_instrument","inst.security","inst.stock","inst.bond","inst.government_bond","inst.corporate_bond","inst.deposit",
     "inst.asset_management_product","inst.fund","inst.mutual_fund","inst.unit_trust","inst.etf","inst.index_fund","inst.money_market_fund",
     "inst.bond_fund","inst.equity_fund","inst.balanced_fund","inst.reit","inst.s_reit","inst.insurance_product","inst.ilp","inst.endowment_plan",
     "inst.annuity","inst.ssb","inst.sgs","inst.t_bill","inst.structured_deposit","inst.structured_product","inst.derivative",
     "risk.investment_risk","risk.market","risk.interest_rate","risk.credit","risk.default","risk.liquidity","risk.inflation","risk.fx",
     "risk.concentration","risk.equity_price",
     "metric.return","metric.yield","metric.total_return","metric.annualized_return","metric.volatility","metric.max_drawdown",
     "metric.dividend_yield","metric.credit_rating","metric.expense_ratio","metric.nav","metric.pe","metric.duration",
     "strat.asset_allocation","strat.diversification","strat.rebalancing","strat.dca","strat.buy_and_hold","strat.passive","strat.active",
     "strat.robo_advisor",
     "macro.interest_rate","macro.rate_hike","macro.rate_cut","macro.rates_rising","macro.rates_falling","macro.inflation","macro.economic_growth","macro.recession",
     "market.bond_price","market.index","market.benchmark","market.bull_market","market.bear_market","market.dividend","market.coupon",
     "market.maturity","market.fees","market.sgx","market.sti","market.risk_free_rate",
     "term.fee_structure","term.management_fee","term.subscription_redemption_fee","term.redemption_terms","term.lock_up","term.fund_structure",
     "term.open_end","term.closed_end","term.principal_protection","term.past_performance","term.tax","term.no_capital_gains_tax","term.compounding",
     "suit.suitability","suit.kyc","suit.investor_profile","suit.risk_tolerance","suit.investment_horizon","suit.liquidity_needs",
     "suit.investment_objective","suit.investor_risk_category","suit.conservative","suit.balanced","suit.aggressive","suit.product_risk_rating",
     "suit.risk_disclosure","suit.retirement_planning","suit.emergency_fund","suit.investor_qualification","suit.retail_investor","suit.accredited_investor",
     "local.mas","local.sip","local.eip","local.cka","local.car","local.cpf","local.cpf_oa","local.cpf_sa","local.cpfis","local.cpf_life","local.srs",
     "behav.behavioral_bias","behav.loss_aversion","behav.herding","behav.fomo", 1)
tier("asset.private_equity","asset.private_credit","asset.infrastructure",
     "inst.preferred_stock","inst.zero_coupon_bond","inst.inflation_linked_bond","inst.callable_bond","inst.perpetual_bond","inst.cds",
     "inst.interest_rate_swap","inst.swap","inst.forward","inst.future","inst.option","inst.call_option","inst.put_option","inst.hedge_fund",
     "inst.fund_of_funds","inst.ncd","inst.financial_bond","inst.local_government_bond","inst.enterprise_bond","inst.trust_scheme",
     "inst.dual_currency_investment","inst.money_market_instrument","inst.private_fund",
     "risk.counterparty","risk.leverage","risk.tail","risk.sequence_of_returns","risk.country","risk.call","risk.prepayment","risk.commodity_price",
     "metric.cvar","metric.var","metric.dv01","metric.convexity","metric.modified_duration","metric.sortino","metric.information_ratio",
     "metric.tracking_error","metric.ev_ebitda","metric.roe","metric.aum","metric.turnover","metric.bid_ask_spread","metric.downside_risk",
     "metric.seven_day_yield","metric.payout_ratio","metric.speculative_grade","metric.investment_grade",
     "strat.risk_parity","strat.immunization","strat.laddering","strat.long_short","strat.factor","strat.leverage","strat.market_timing",
     "strat.fixed_income_plus","strat.esg","strat.tactical_aa","strat.strategic_aa","strat.glide_path",
     "macro.quantitative_easing","macro.yield_curve_inversion","macro.credit_cycle","macro.lpr","macro.sora","macro.deflation",
     "market.margin_trading","market.short_selling","market.primary_market","market.ipo",
     "term.performance_fee","term.custody_fee","term.implicit_guarantee","term.expected_return_product",
     "suit.expert_investor","suit.institutional_investor","suit.professional_investor","suit.qualified_investor","suit.cn_risk_level",
     "suit.cautious","suit.steady","suit.growth","suit.cn_balanced","suit.cn_aggressive",
     "local.sfa","local.faa","local.fair_dealing","local.cross_border_channel",
     "behav.home_bias","behav.mental_accounting","behav.confirmation_bias", 3)

# ------------------------------------------------------------ validator findings
tier("inst.credit_bond", "metric.valuation_multiple", "market.secondary_market", 1)
drop_rel("market.margin_trading", "exposed_to", "risk.leverage"); rel("market.margin_trading", "related", "risk.leverage")
drop_rel("market.short_selling", "part_of", "strat.long_short"); rel("market.short_selling", "related", "strat.long_short")
drop_rel("inst.balanced_fund", "belongs_to", "strat.multi_asset"); rel("inst.balanced_fund", "related", "strat.multi_asset")
