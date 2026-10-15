# v0.2 revision of the seed, applied as transformations on v0.1 (seed_concepts.py)
# so every change is traceable to a review finding.
import seed_concepts as s
C, R = s.C, s.R
byid = {x["id"]: x for x in C}

def concept(cid): return byid[cid]
def drop_alts(cid, *alts):
    concept(cid)["alts"] = [a for a in concept(cid)["alts"] if a not in alts]
def add_alts(cid, *alts):
    concept(cid)["alts"] += [a for a in alts if a not in concept(cid)["alts"]]
def hidden(cid, *alts):                       # keep for matching, never shown
    drop_alts(cid, *alts); concept(cid).setdefault("hidden", []).extend(alts)
def redefine(cid, zh=None, en=None, dzh=None, den=None):
    x = concept(cid)
    if zh: x["zh"] = zh
    if en: x["en"] = en
    if dzh: x["dzh"] = dzh
    if den: x["den"] = den
def drop_rel(src, rel, dst):
    R[:] = [y for y in R if not (y["src"] == src and y["rel"] == rel and y["dst"] == dst)]
def rel(src, r, dst, polarity=None, conf=None, note=None):
    drop_rel(src, r, dst)
    R.append(dict(src=src, rel=r, dst=dst, polarity=polarity, conf=conf, note=note))
def new(cid, parents, zh, en, dzh, den, alts=()):
    s.c(cid, parents, zh, en, dzh, den, alts); byid[cid] = C[-1]
def reparent(cid, *parents): concept(cid)["parents"] = list(parents)

# ---------------------------------------------------------------- 1. compliance
R[:] = [y for y in R if y["rel"] != "suitable_for"]          # §6: no suitable_for in base layer
redefine("inst.money_market_fund",
  dzh="主要投资于货币市场工具、追求较低波动和高流动性的基金；不保证本金不受损失。",
  den="A fund investing mainly in money market instruments, seeking low volatility and high liquidity; principal is not guaranteed.")
redefine("inst.wealth_management_product", zh="理财产品", en="Wealth management product",
  dzh="由银行或理财子公司等发行、代客投资管理的集合投资产品；实行净值化管理，不保证本金和收益。",
  den="A pooled investment product issued by banks or their wealth management subsidiaries; net-asset-value based, with neither principal nor return guaranteed.")
drop_alts("inst.wealth_management_product", "资管产品")
redefine("inst.structured_deposit",
  dzh="在存款基础上嵌入衍生品的产品，本金按存款保障，收益与利率、汇率或指数等挂钩而浮动。",
  den="A deposit with an embedded derivative: principal is protected as a deposit while the return floats with rates, currencies or indices.")
redefine("asset.gold",
  dzh="常被视为避险和价值储藏手段的贵金属；价格波动较大，并不保证保值。",
  den="A precious metal often regarded as a safe haven and store of value; its price is volatile and value preservation is not guaranteed.")
redefine("inst.government_bond",
  dzh="由中央政府发行的债券，通常被视为本币信用风险最低的债券，但仍承担利率风险和价格波动。",
  den="A bond issued by a national government, usually seen as carrying the lowest credit risk in its currency, while still subject to interest rate risk and price fluctuation.")
redefine("suit.suitability",
  dzh="金融机构应承担的义务：将合适的产品销售给合适的投资者，并充分揭示风险。",
  den="The obligation of financial institutions to sell suitable products to suitable investors and to disclose risks adequately.")
redefine("suit.qualified_investor",
  dzh="达到监管规定的资产、收入或经验门槛、可投资私募等高风险产品的投资者；门槛因辖区而异。",
  den="An investor meeting regulatory wealth, income or experience thresholds and eligible for higher-risk products such as private funds; thresholds differ by jurisdiction.")
drop_alts("suit.qualified_investor", "Accredited investor")

# ---------------------------------------------------------------- 2. definitions
redefine("metric.return", zh="投资回报率", en="Return",
  dzh="一段时间内投资的盈亏占初始投入的比例，含价格变动和现金收入。",
  den="The gain or loss on an investment over a period as a proportion of the amount invested, including price change and income.")
drop_alts("metric.return", "回报率"); add_alts("metric.return", "回报率", "投资收益率")
redefine("metric.duration",
  dzh="债券现金流的加权平均回收期；也常泛指债券价格对收益率变动的敏感程度，久期越长利率风险越大。",
  den="The weighted-average time to receive a bond's cash flows; also commonly used for a bond's price sensitivity to yield changes, with longer duration meaning higher interest rate risk.")
redefine("metric.modified_duration", dzh="收益率变动 1 个百分点时债券价格的近似百分比变化。",
  den="The approximate percentage change in a bond's price for a one-percentage-point change in yield.")
redefine("metric.eps", dzh="归属于母公司股东的净利润除以加权平均股本。",
  den="Net profit attributable to shareholders divided by the weighted-average number of shares outstanding.")
redefine("metric.turnover", zh="组合换手率", en="Portfolio turnover")
drop_alts("metric.turnover", "周转率"); hidden("metric.turnover", "换手率")
drop_alts("metric.dividend_yield", "分红率")
drop_alts("inst.corporate_bond", "企业债")
drop_alts("suit.kyc", "客户尽职调查")
drop_alts("inst.mutual_fund", "Public fund"); add_alts("inst.mutual_fund", "Publicly offered fund")
hidden("risk.tail", "黑天鹅风险")

# ---------------------------------------------------------------- 3. hierarchy
reparent("metric.risk_adjusted_return")                       # ratios are not returns
reparent("inst.structured_deposit", "inst.deposit")
rel("inst.structured_deposit", "related", "inst.structured_product")
drop_rel("inst.structured_deposit", "related", "inst.deposit")
reparent("risk.reinvestment", "risk.interest_rate")
concept("asset.multi_asset")["id"] = "strat.multi_asset"; byid["strat.multi_asset"] = byid.pop("asset.multi_asset")
for y in R:
    for k in ("src", "dst"):
        if y[k] == "asset.multi_asset": y[k] = "strat.multi_asset"
reparent("strat.multi_asset", "strat.asset_allocation")
drop_rel("strat.multi_asset", "related", "strat.asset_allocation")
reparent("inst.wealth_management_product", "inst.fund")
# fund: two axes - by offering (mutual/private) and by investment type; type nodes also is_a mutual_fund
for f in ["inst.etf", "inst.index_fund", "inst.money_market_fund", "inst.bond_fund",
          "inst.equity_fund", "inst.balanced_fund", "inst.fund_of_funds", "inst.target_date_fund"]:
    reparent(f, "inst.fund", "inst.mutual_fund")
# instrument -> asset class: use exposed-to-style 'belongs_to' instead of cross-scheme is_a
XS = [("inst.stock","asset.equity"),("inst.bond","asset.fixed_income"),("inst.deposit","asset.cash"),
      ("inst.money_market_instrument","asset.cash")]
for i, a in XS:
    concept(i)["parents"] = [p for p in concept(i)["parents"] if p != a]
    rel(i, "belongs_to", a)
for i, a in [("inst.reit","asset.real_estate"),("inst.hedge_fund","asset.alternative"),
             ("inst.private_fund","asset.alternative"),("inst.equity_fund","asset.equity"),
             ("inst.bond_fund","asset.fixed_income"),("inst.money_market_fund","asset.cash"),
             ("inst.balanced_fund","strat.multi_asset")]:
    drop_rel(i, "related", a); rel(i, "belongs_to", a)
concept("asset.gold")["parents"] = []; rel("asset.gold", "belongs_to", "asset.commodity")

# ---------------------------------------------------------------- 4. relation semantics
# part_of = composition only; phases -> related; formula inputs -> input_of
rel("macro.yield_curve_inversion", "related", "macro.yield_curve"); drop_rel("macro.yield_curve_inversion", "part_of", "macro.yield_curve")
rel("macro.recession", "related", "macro.business_cycle"); drop_rel("macro.recession", "part_of", "macro.business_cycle")
for src, dst in [("market.risk_free_rate","metric.sharpe"),("metric.tracking_error","metric.information_ratio"),
                 ("metric.eps","metric.pe"),("market.dividend","metric.total_return"),("market.coupon","metric.total_return")]:
    drop_rel(src, "part_of", dst); rel(src, "input_of", dst)
rel("macro.rate_hike", "affects", "macro.policy_rate", 1); drop_rel("macro.rate_hike", "related", "macro.policy_rate")
rel("macro.rate_cut", "affects", "macro.policy_rate", -1)
drop_rel("macro.monetary_policy", "affects", "macro.policy_rate"); rel("macro.policy_rate", "part_of", "macro.monetary_policy")
drop_rel("risk.inflation", "related", "macro.inflation"); rel("macro.inflation", "affects", "risk.inflation", 1)
drop_rel("risk.fx", "related", "macro.exchange_rate"); rel("macro.exchange_rate", "affects", "risk.fx", None, note="Exchange-rate volatility drives currency risk; direction depends on exposure")
drop_rel("market.liquidity", "related", "risk.liquidity"); rel("market.liquidity", "affects", "risk.liquidity", -1)
rel("inst.equity_fund", "exposed_to", "risk.equity_price"); rel("inst.equity_fund", "exposed_to", "risk.market")
rel("inst.bond_fund", "exposed_to", "risk.interest_rate"); rel("inst.bond_fund", "exposed_to", "risk.credit")
drop_rel("strat.leverage", "exposed_to", "risk.leverage"); rel("strat.leverage", "related", "risk.leverage", note="Leveraged strategies carry leverage risk")
drop_rel("inst.derivative", "related", "suit.qualified_investor")
rel("inst.derivative", "related", "suit.suitability", note="Most jurisdictions impose extra suitability requirements on retail derivatives trading")
rel("suit.investment_horizon", "related", "asset.equity", conf=0.7, note="Horizon is one suitability input for equity allocation")
rel("strat.glide_path", "related", "strat.strategic_aa")
rel("risk.tail", "related", "metric.var", note="VaR does not measure losses beyond the threshold; see CVaR")
rel("macro.yield_curve_inversion", "related", "macro.recession", conf=0.8, note="Historically often precedes recessions; not a forecast")

# ---------------------------------------------------------------- 5. alias cleanup
GENERIC = {
 "asset.commodity": ["商品"], "market.index": ["指数", "Index"], "market.benchmark": ["基准"],
 "market.fees": ["费用", "交易成本", "Fees"], "metric.credit_rating": ["评级"], "market.liquidity": ["流动性"],
 "macro.recession": ["衰退"], "macro.yield_curve_inversion": ["倒挂"], "inst.stock": ["股份", "Share", "Shares"],
 "inst.forward": ["远期", "Forward"], "inst.swap": ["掉期", "Swaps"], "inst.security": ["Securities"],
 "inst.option": ["Options"], "inst.future": ["Futures", "Future"], "asset.cash": ["Cash"],
 "inst.fund": ["Fund"], "asset.real_estate": ["Property"], "inst.deposit": ["定期存款", "Bank deposit"],
 "inst.government_bond": ["Treasury"], "market.bull_market": ["Bull"], "market.bear_market": ["Bear"],
 "strat.hedging": ["Hedge"], "strat.leverage": ["Leverage"], "inst.convertible_bond": ["Convertible"],
 "market.maturity": ["Maturity date"], "inst.inflation_linked_bond": ["TIPS", "Linker"],
 "metric.alpha": ["α", "Alpha收益"], "metric.beta": ["β"], "metric.var": ["VaR"], "metric.nav": ["NAV"],
 "metric.pb": ["PB"], "market.risk_free_rate": ["Rf"], "metric.expense_ratio": ["TER"],
 "macro.quantitative_easing": ["QE"], "strat.strategic_aa": ["SAA"], "strat.tactical_aa": ["TAA"],
 "macro.policy_rate": ["基准利率"], "suit.conservative": ["Conservative"], "suit.aggressive": ["Aggressive"],
 "inst.bond": ["Bonds"], "asset.equity": ["Equities"], "metric.annualized_return": ["年化回报"],
 "metric.standard_deviation": ["Std dev"], "market.coupon": ["Coupon"], "asset.alternative": ["Alternatives"],
}
for cid, alts in GENERIC.items():
    present = [a for a in alts if a in concept(cid)["alts"]]
    for a in present:
        if a in ('SAA','TAA','QE','TIPS','NAV','VaR','TER','Rf') or a in ('Equities','Bonds','Alternatives','Securities','Options','Futures','Future','Swaps','Shares','Share','Cash','Fund','Property','Treasury','Bull','Bear','Hedge','Leverage','Convertible','Coupon','Std dev','年化回报','Alpha收益','定期存款','Bank deposit','Maturity date','基准利率','Conservative','Aggressive','Linker','PB','α','β'):
            pass  # rule-based kind_of decides
        else:
            hidden(cid, a)
add_alts("strat.esg", "ESG投资"); add_alts("strat.core_satellite", "核心卫星策略")
add_alts("metric.alpha", "超额收益率"); add_alts("macro.rate_hike", "利率上升", "利率上行")
add_alts("macro.rate_cut", "利率下降", "利率下行"); add_alts("metric.nav", "净值")
add_alts("inst.mutual_fund", "公募"); add_alts("inst.private_fund", "私募")
add_alts("metric.annualized_return", "年化")

# ---------------------------------------------------------------- 6. gaps
new("metric.yield", [], "收益率", "Yield",
  "资产每年产生的现金收入（利息、股息）相对其价格的比率；债券语境下通常指到期收益率。",
  "Annual cash income (interest, dividends) from an asset relative to its price; in bond contexts usually the yield to maturity.",
  ["Yields"])
for m in ["metric.ytm", "metric.dividend_yield", "metric.coupon_rate"]:
    reparent(m, "metric.yield")
rel("metric.yield", "affects", "market.bond_price", -1, note="Bond price and yield move inversely")
drop_rel("market.bond_price", "affects", "metric.ytm")
new("metric.cvar", [], "条件风险价值", "Conditional value at risk",
  "超过风险价值阈值的损失的期望值，用于刻画尾部损失幅度。",
  "The expected loss beyond the value-at-risk threshold, used to characterise the size of tail losses.",
  ["预期损失", "CVaR", "Expected shortfall", "ES"])
rel("metric.cvar", "measures", "risk.tail"); rel("metric.cvar", "related", "metric.var")
new("metric.downside_risk", [], "下行风险", "Downside risk",
  "收益低于目标或零的波动部分，是索提诺比率的分母。",
  "The portion of volatility from returns below a target or zero; the denominator of the Sortino ratio.",
  ["下行波动", "Downside deviation"])
rel("metric.downside_risk", "input_of", "metric.sortino"); rel("metric.downside_risk", "measures", "risk.market")
new("metric.capital_gain", [], "资本利得", "Capital gain",
  "资产卖出价高于买入价所实现的收益。",
  "The gain realised when an asset is sold for more than its purchase price.",
  ["资本增值", "价差收益"])
rel("metric.capital_gain", "input_of", "metric.total_return")
new("metric.compounding", [], "复利", "Compounding",
  "收益再投资后继续产生收益，使资产随时间加速增长的过程。",
  "The process by which reinvested returns earn further returns, accelerating growth over time.",
  ["复合增长", "Compound growth"])
rel("metric.compounding", "related", "metric.annualized_return"); rel("metric.compounding", "related", "strat.buy_and_hold")
new("metric.investment_grade", ["metric.credit_rating"], "投资级", "Investment grade",
  "信用评级达到较高等级（如 BBB-/Baa3 及以上）、违约风险较低的评级区间。",
  "The rating band (e.g. BBB-/Baa3 and above) indicating relatively low default risk.",
  ["投资级评级"])
new("metric.speculative_grade", ["metric.credit_rating"], "投机级", "Speculative grade",
  "信用评级低于投资级、违约风险较高的评级区间。",
  "The rating band below investment grade, indicating higher default risk.",
  ["非投资级", "高收益级", "Sub-investment grade"])
rel("metric.investment_grade", "opposite_of", "metric.speculative_grade")
rel("inst.high_yield_bond", "related", "metric.speculative_grade")
new("term.fee_structure", [], "费用结构", "Fee structure",
  "投资产品收取的各类费用的组成，如管理费、托管费、申购赎回费、销售服务费和业绩报酬。",
  "The composition of charges on an investment product, such as management, custody, subscription/redemption, distribution and performance fees.",
  ["收费结构"])
rel("term.fee_structure", "related", "market.fees"); rel("term.fee_structure", "related", "metric.expense_ratio")
for cid, zh, en, dzh, den, alts in [
  ("term.management_fee", "管理费", "Management fee", "基金管理人按资产规模比例收取的费用。", "A fee charged by the manager as a percentage of assets.", []),
  ("term.custody_fee", "托管费", "Custody fee", "托管机构保管基金资产收取的费用。", "A fee charged by the custodian for safekeeping fund assets.", []),
  ("term.subscription_redemption_fee", "申购赎回费", "Subscription and redemption fees", "投资者买入或卖出基金份额时支付的费用。", "Fees paid by investors when buying or selling fund units.", ["申购费", "赎回费"]),
  ("term.performance_fee", "业绩报酬", "Performance fee", "管理人在业绩超过约定基准时按超额部分提取的报酬，常见于私募基金。", "A fee the manager takes from returns above an agreed hurdle, common in private funds.", ["业绩提成", "Carried interest"]),
]:
    new(cid, ["term.fee_structure"], zh, en, dzh, den, alts)
rel("term.performance_fee", "related", "inst.private_fund")
new("term.redemption_terms", [], "赎回条款", "Redemption terms",
  "产品何时、以何种条件允许投资者取回资金的规定，如开放日、锁定期和赎回费。",
  "The rules on when and how investors can get their money back, such as dealing days, lock-ups and redemption fees.",
  ["流动性条款", "Liquidity terms"])
new("term.open_end", ["term.redemption_terms"], "开放式", "Open-ended",
  "投资者可在开放日按净值申购和赎回的基金运作方式。",
  "A fund structure in which investors can subscribe and redeem at net asset value on dealing days.",
  ["开放式基金", "Open-end fund"])
new("term.closed_end", ["term.redemption_terms"], "封闭式", "Closed-ended",
  "在封闭期内不接受申购赎回、份额只能在二级市场转让的运作方式。",
  "A fund structure with no subscriptions or redemptions during the closed period; units trade on the secondary market.",
  ["封闭式基金", "Closed-end fund"])
new("term.lock_up", ["term.redemption_terms"], "锁定期", "Lock-up period",
  "投资者不得赎回的最短持有期限。",
  "The minimum holding period during which investors cannot redeem.",
  ["封闭期", "最短持有期", "Lock-up"])
rel("term.open_end", "opposite_of", "term.closed_end")
rel("term.redemption_terms", "related", "risk.liquidity"); rel("term.redemption_terms", "related", "suit.liquidity_needs")
rel("term.lock_up", "related", "inst.private_fund")
new("term.principal_protection", [], "本金保障", "Principal protection",
  "产品是否承诺到期归还本金；多数投资产品不保本，存款受存款保险保障。",
  "Whether a product promises to return principal; most investment products do not, while deposits are covered by deposit insurance.",
  ["保本", "Capital guarantee"])
new("term.nav_based", [], "净值化", "Net-asset-value based",
  "产品按实际投资结果计算净值、收益随市场波动、不承诺固定回报的管理方式。",
  "Managing a product so that its value reflects actual investment results, fluctuating with markets and promising no fixed return.",
  ["净值型", "非保本浮动收益"])
new("term.implicit_guarantee", [], "刚性兑付", "Implicit guarantee",
  "发行机构在产品亏损时仍自行承担损失、保证兑付的做法；资管新规要求打破刚兑。",
  "The practice of an issuer absorbing losses to honour payouts regardless of performance; regulators in mainland China require this to be broken.",
  ["刚兑", "打破刚兑"])
rel("term.nav_based", "opposite_of", "term.implicit_guarantee")
rel("inst.wealth_management_product", "related", "term.nav_based")
rel("inst.deposit", "related", "term.principal_protection"); rel("inst.structured_deposit", "related", "term.principal_protection")
rel("term.principal_protection", "related", "risk.default")
new("term.past_performance", [], "过往业绩", "Past performance",
  "产品或管理人历史上的收益表现；不代表未来表现，也不构成收益承诺。",
  "The historical returns of a product or manager; not indicative of future results and not a promise of return.",
  ["历史业绩", "历史表现", "Track record"])
rel("term.past_performance", "related", "metric.return"); rel("term.past_performance", "related", "suit.risk_disclosure")
new("risk.call", ["risk.interest_rate"], "赎回风险", "Call risk",
  "发行人在利率下降时提前赎回债券，投资者被迫以更低收益率再投资的风险。",
  "The risk that an issuer redeems a bond early when rates fall, forcing reinvestment at lower yields.",
  ["提前赎回风险", "Prepayment risk"])
new("inst.callable_bond", ["inst.bond"], "可赎回债券", "Callable bond",
  "发行人有权在到期前按约定价格赎回的债券。",
  "A bond the issuer may redeem before maturity at a set price.",
  ["含赎回权债券"])
rel("inst.callable_bond", "exposed_to", "risk.call")
new("inst.perpetual_bond", ["inst.bond"], "永续债", "Perpetual bond",
  "没有固定到期日、发行人可选择赎回的债券，常见于银行资本工具。",
  "A bond with no fixed maturity that the issuer may call, common among bank capital instruments.",
  ["永续债券", "Perpetual"])
rel("inst.perpetual_bond", "exposed_to", "risk.call"); rel("inst.perpetual_bond", "exposed_to", "risk.interest_rate")
new("inst.annuity", ["inst.financial_instrument"], "年金保险", "Annuity",
  "由保险公司发行、按约定在未来定期给付的保险产品，常用于退休收入规划。",
  "An insurance product paying regular amounts in the future, often used for retirement income.",
  ["年金", "养老年金"])
rel("inst.annuity", "related", "suit.retirement_planning"); rel("inst.annuity", "exposed_to", "risk.inflation")
new("inst.insurance_product", ["inst.financial_instrument"], "保险类理财产品", "Insurance-based investment product",
  "兼具保障与储蓄或投资功能的人身保险产品，如增额终身寿险、分红险、投连险。",
  "Life insurance products combining protection with savings or investment, such as participating and unit-linked policies.",
  ["投资型保险", "储蓄型保险", "分红险", "投连险"])
rel("inst.insurance_product", "related", "inst.annuity"); rel("inst.insurance_product", "exposed_to", "risk.liquidity")
new("term.tax", [], "投资税收", "Investment taxation",
  "投资收益涉及的税负及税收优惠安排，如资本利得税、股息税和税收递延账户。",
  "Taxes on investment returns and tax-advantaged arrangements, such as capital gains tax, dividend tax and tax-deferred accounts.",
  ["税收", "税务", "税优账户", "Capital gains tax"])
rel("term.tax", "affects", "metric.total_return", -1); rel("term.tax", "related", "risk.regulatory"); rel("term.tax", "related", "suit.retirement_planning")
new("inst.cross_border_channel", [], "跨境投资通道", "Cross-border investment channel",
  "居民投资境外市场的合规渠道，如 QDII、沪深港通、跨境理财通。",
  "Regulated channels for investing in overseas markets, such as QDII, Stock Connect and Wealth Management Connect.",
  ["QDII", "沪深港通", "港股通", "跨境理财通", "Stock Connect"])
rel("inst.cross_border_channel", "exposed_to", "risk.fx"); rel("inst.cross_border_channel", "exposed_to", "risk.country")
# investor classification by jurisdiction
new("suit.retail_investor", ["suit.investor_risk_category"], "普通投资者", "Retail investor",
  "未被认定为专业投资者的个人投资者，享有更高程度的适当性保护。",
  "An individual investor not classified as professional, receiving a higher level of suitability protection.",
  ["零售投资者", "个人投资者"])
new("suit.professional_investor", ["suit.investor_risk_category"], "专业投资者", "Professional investor",
  "满足资产、收入或经验标准、被认定为具备专业判断能力的投资者；认定标准因辖区而异。",
  "An investor meeting asset, income or experience criteria and deemed able to judge risks independently; criteria differ by jurisdiction.",
  ["Accredited investor", "Expert investor"])
rel("suit.retail_investor", "opposite_of", "suit.professional_investor")
rel("suit.professional_investor", "related", "suit.qualified_investor")
new("suit.cautious", ["suit.investor_risk_category"], "谨慎型投资者", "Cautious investor",
  "风险承受能力最低、几乎不能承受本金损失的投资者类型（中国大陆 C1）。",
  "The lowest risk-tolerance type, barely able to bear any loss of principal (C1 in mainland China).",
  ["C1"])
new("suit.steady", ["suit.investor_risk_category"], "稳健型投资者", "Steady investor",
  "可承受较小波动、以稳健收益为目标的投资者类型（中国大陆 C2）。",
  "An investor type able to bear small fluctuations and seeking steady returns (C2 in mainland China).",
  ["稳健型", "C2"])
new("suit.growth", ["suit.investor_risk_category"], "成长型投资者", "Growth investor",
  "可承受较大波动、追求资产增长的投资者类型（中国大陆 C4）。",
  "An investor type able to bear larger fluctuations and seeking asset growth (C4 in mainland China).",
  ["成长型", "C4"])
add_alts("suit.conservative", "C1"); drop_alts("suit.conservative", "C1")   # keep C1 on cautious only
add_alts("suit.balanced", "C3"); add_alts("suit.aggressive", "C5", "激进型投资者")
rel("suit.product_risk_rating", "related", "suit.retail_investor")
# macro -> asset affects
rel("macro.interest_rate", "affects", "asset.equity", -1, conf=0.6, note="Higher discount rates weigh on valuations; effect varies")
rel("macro.interest_rate", "affects", "asset.gold", -1, conf=0.6, note="Via real rates / opportunity cost")
rel("macro.interest_rate", "affects", "macro.exchange_rate", None, note="Rate differentials drive currencies; direction depends on relative moves")
rel("macro.economic_growth", "affects", "asset.equity", 1, conf=0.7)
rel("macro.recession", "affects", "asset.equity", -1, conf=0.8)
rel("macro.recession", "affects", "metric.credit_spread", 1, conf=0.8)
rel("macro.inflation", "affects", "asset.gold", 1, conf=0.6, note="Inconsistent hedge")
rel("macro.inflation", "affects", "market.bond_price", -1, conf=0.8, note="Via higher yields")
# instrument -> risk exposed_to
rel("inst.reit", "exposed_to", "risk.interest_rate"); rel("inst.reit", "exposed_to", "risk.equity_price")
rel("inst.convertible_bond", "exposed_to", "risk.equity_price"); rel("inst.convertible_bond", "exposed_to", "risk.credit")
rel("inst.hedge_fund", "exposed_to", "risk.leverage"); rel("inst.hedge_fund", "exposed_to", "risk.liquidity")
for rk in ["risk.market", "risk.credit", "risk.liquidity"]:
    rel("inst.wealth_management_product", "exposed_to", rk)
rel("inst.money_market_fund", "exposed_to", "risk.credit", conf=0.8, note="Low but not zero")
rel("inst.money_market_fund", "exposed_to", "risk.liquidity", conf=0.7)
rel("inst.etf", "exposed_to", "risk.market"); rel("inst.index_fund", "exposed_to", "risk.market")
rel("inst.target_date_fund", "exposed_to", "risk.market")
rel("inst.structured_product", "exposed_to", "risk.market")

# ---------------------------------------------------------------- 7. confidence defaults
for y in R:
    if y["conf"] is None:
        y["conf"] = {"is_a": 1.0, "part_of": 1.0, "input_of": 1.0, "belongs_to": 1.0, "opposite_of": 0.95,
                     "measures": 0.95, "exposed_to": 0.9, "mitigates": 0.85, "affects": 0.85, "related": 0.75}[y["rel"]]
