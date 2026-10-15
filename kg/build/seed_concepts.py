# Seed concept definitions for the finance investment concept graph (v0.1).
# Each concept: (id, parents, zh, en, def_zh, def_en, alt_labels)
# parents -> generates is_a relations.

C = []
def c(cid, parents, zh, en, dzh, den, alts=()):
    C.append(dict(id=cid, parents=list(parents), zh=zh, en=en, dzh=dzh, den=den, alts=list(alts)))

# ---------------------------------------------------------------- asset_class
c("asset.equity", [], "权益类资产", "Equity",
  "代表对企业所有权的资产，收益来自分红和价格上涨，波动通常高于固定收益。",
  "Assets representing ownership in companies, earning returns through dividends and price appreciation, typically more volatile than fixed income.",
  ["股权类资产", "股票类资产", "Equities"])
c("asset.fixed_income", [], "固定收益", "Fixed income",
  "按约定支付利息并到期还本的债务类资产，收益相对稳定，主要受利率和信用影响。",
  "Debt assets that pay contractual interest and return principal at maturity; returns are relatively stable and driven mainly by interest rates and credit.",
  ["固收", "债券类资产", "Fixed-income"])
c("asset.cash", [], "现金及现金等价物", "Cash and cash equivalents",
  "流动性极高、价格波动极小的资产，如活期存款和短期货币市场工具。",
  "Highly liquid assets with minimal price fluctuation, such as demand deposits and short-term money market instruments.",
  ["现金类资产", "货币类资产", "Cash"])
c("asset.alternative", [], "另类资产", "Alternative assets",
  "股票、债券和现金之外的资产类别，通常流动性较低、估值较复杂。",
  "Asset classes outside stocks, bonds and cash, usually less liquid and harder to value.",
  ["另类投资", "Alternatives", "Alternative investments"])
c("asset.real_estate", ["asset.alternative"], "房地产", "Real estate",
  "以土地和建筑物为基础的资产，收益来自租金和资产增值。",
  "Assets based on land and buildings, earning returns from rent and capital appreciation.",
  ["不动产", "Property"])
c("asset.commodity", ["asset.alternative"], "大宗商品", "Commodities",
  "能源、金属、农产品等可标准化交易的实物商品。",
  "Standardised, tradable physical goods such as energy, metals and agricultural products.",
  ["商品", "Commodity"])
c("asset.gold", ["asset.commodity"], "黄金", "Gold",
  "常被视为避险和价值储藏手段的贵金属。",
  "A precious metal often regarded as a safe haven and store of value.",
  ["Gold bullion"])
c("asset.private_equity", ["asset.alternative"], "私募股权", "Private equity",
  "投资于未公开上市企业股权的资产类别，持有期长、流动性低。",
  "Investment in equity of companies that are not publicly listed, with long holding periods and low liquidity.",
  ["PE", "私募股权投资"])
c("asset.private_credit", ["asset.alternative"], "私募信贷", "Private credit",
  "由非银行机构直接向企业提供、不在公开市场交易的贷款类资产。",
  "Loans provided directly to companies by non-bank lenders and not traded on public markets.",
  ["私人信贷", "Direct lending"])
c("asset.infrastructure", ["asset.alternative"], "基础设施", "Infrastructure",
  "投资于交通、能源、公用事业等长期基础设施项目的资产类别。",
  "An asset class investing in long-lived projects such as transport, energy and utilities.",
  ["基建资产"])
c("asset.multi_asset", [], "多资产", "Multi-asset",
  "在同一组合中同时配置多种资产类别的投资方式。",
  "An approach that combines several asset classes within one portfolio.",
  ["多元资产", "Multi asset"])

# ---------------------------------------------------------------- instrument
c("inst.financial_instrument", [], "金融工具", "Financial instrument",
  "具有货币价值、可交易或可转让的合约或凭证的统称。",
  "A general term for contracts or certificates with monetary value that can be traded or transferred.",
  ["金融产品", "Financial product"])
c("inst.security", ["inst.financial_instrument"], "证券", "Security",
  "代表所有权或债权、可在市场上交易的金融工具，如股票和债券。",
  "A tradable financial instrument representing ownership or a creditor claim, such as stocks and bonds.",
  ["有价证券", "Securities"])
c("inst.stock", ["inst.security", "asset.equity"], "股票", "Stock",
  "代表持有者对公司部分所有权的证券。",
  "A security representing partial ownership of a company.",
  ["股份", "Share", "Shares"])
c("inst.common_stock", ["inst.stock"], "普通股", "Common stock",
  "享有投票权和剩余收益分配权、清偿顺序最后的股票。",
  "Stock carrying voting rights and a residual claim on earnings, ranking last in liquidation.",
  ["Ordinary share"])
c("inst.preferred_stock", ["inst.stock"], "优先股", "Preferred stock",
  "在股息分配和清偿顺序上优先于普通股、通常无投票权的股票。",
  "Stock with priority over common stock for dividends and liquidation, usually without voting rights.",
  ["Preference share", "Preferred share"])
c("inst.bond", ["inst.security", "asset.fixed_income"], "债券", "Bond",
  "发行人向投资者借款并承诺按期付息、到期还本的债务证券。",
  "A debt security in which the issuer borrows from investors and promises periodic interest and repayment of principal at maturity.",
  ["Bonds"])
c("inst.government_bond", ["inst.bond"], "国债", "Government bond",
  "由中央政府发行的债券，通常被视为本币信用风险最低的债券。",
  "A bond issued by a national government, usually seen as carrying the lowest credit risk in its currency.",
  ["政府债券", "Sovereign bond", "Treasury"])
c("inst.credit_bond", ["inst.bond"], "信用债", "Credit bond",
  "由非政府主体发行、需承担发行人信用风险的债券。",
  "A bond issued by a non-government entity, exposing investors to the issuer's credit risk.",
  ["信用债券"])
c("inst.corporate_bond", ["inst.credit_bond"], "公司债", "Corporate bond",
  "由企业发行、用于融资的债券。",
  "A bond issued by a company to raise financing.",
  ["企业债", "Corporate bonds"])
c("inst.high_yield_bond", ["inst.credit_bond"], "高收益债", "High-yield bond",
  "信用评级低于投资级、以较高收益补偿较高违约风险的债券。",
  "A bond rated below investment grade that offers higher yield to compensate for higher default risk.",
  ["垃圾债", "Junk bond", "HY bond"])
c("inst.convertible_bond", ["inst.bond"], "可转换债券", "Convertible bond",
  "持有人可在约定条件下转换为发行人股票的债券。",
  "A bond that the holder can convert into the issuer's shares under specified terms.",
  ["可转债", "Convertible"])
c("inst.zero_coupon_bond", ["inst.bond"], "零息债券", "Zero-coupon bond",
  "不支付票息、以折价发行并到期按面值兑付的债券。",
  "A bond that pays no coupon, is issued at a discount and redeems at face value at maturity.",
  ["贴现债券", "Zero coupon bond"])
c("inst.inflation_linked_bond", ["inst.bond"], "通胀挂钩债券", "Inflation-linked bond",
  "本金或利息随通胀指数调整的债券。",
  "A bond whose principal or interest is adjusted in line with an inflation index.",
  ["抗通胀债券", "TIPS", "Linker"])
c("inst.money_market_instrument", ["inst.financial_instrument", "asset.cash"], "货币市场工具", "Money market instrument",
  "期限通常在一年以内、流动性高的短期债务工具，如短期票据和回购。",
  "Short-term, highly liquid debt instruments, typically under one year, such as commercial paper and repos.",
  ["短期货币工具"])
c("inst.deposit", ["inst.financial_instrument", "asset.cash"], "存款", "Deposit",
  "存放在银行等存款机构、按约定计息的资金。",
  "Funds placed with a bank or deposit-taking institution that earn agreed interest.",
  ["银行存款", "定期存款", "Bank deposit"])
c("inst.fund", ["inst.financial_instrument"], "投资基金", "Investment fund",
  "汇集多名投资者资金、由专业管理人统一投资的集合投资工具。",
  "A collective investment vehicle pooling money from many investors and managed by a professional manager.",
  ["基金", "集合投资计划", "Fund", "Collective investment scheme"])
c("inst.mutual_fund", ["inst.fund"], "公募基金", "Mutual fund",
  "向公众公开募集、受严格监管的投资基金。",
  "An investment fund offered to the public and subject to strict regulation.",
  ["共同基金", "Public fund"])
c("inst.etf", ["inst.fund"], "交易所交易基金", "Exchange-traded fund",
  "在交易所上市、可像股票一样买卖的基金，多数跟踪指数。",
  "A fund listed on an exchange and traded like a stock, most tracking an index.",
  ["ETF", "交易型开放式指数基金"])
c("inst.index_fund", ["inst.fund"], "指数基金", "Index fund",
  "以复制特定市场指数表现为目标的基金。",
  "A fund that aims to replicate the performance of a specific market index.",
  ["指数型基金"])
c("inst.money_market_fund", ["inst.fund"], "货币市场基金", "Money market fund",
  "主要投资于货币市场工具、追求本金稳定和高流动性的基金。",
  "A fund investing mainly in money market instruments, seeking capital stability and high liquidity.",
  ["货币基金", "货基", "MMF"])
c("inst.bond_fund", ["inst.fund"], "债券基金", "Bond fund",
  "主要投资于债券的基金。",
  "A fund that invests mainly in bonds.",
  ["债券型基金", "债基"])
c("inst.equity_fund", ["inst.fund"], "股票型基金", "Equity fund",
  "主要投资于股票的基金。",
  "A fund that invests mainly in stocks.",
  ["股票基金"])
c("inst.balanced_fund", ["inst.fund"], "混合型基金", "Balanced fund",
  "同时投资股票和债券、在两者之间灵活配置的基金。",
  "A fund that invests in both stocks and bonds, allocating flexibly between them.",
  ["混合基金", "平衡型基金", "Hybrid fund"])
c("inst.fund_of_funds", ["inst.fund"], "基金中的基金", "Fund of funds",
  "以其他基金为主要投资对象的基金。",
  "A fund whose main holdings are other funds.",
  ["FOF"])
c("inst.target_date_fund", ["inst.fund"], "目标日期基金", "Target-date fund",
  "按预设目标日期逐步降低风险资产比例的基金，常用于养老规划。",
  "A fund that gradually reduces risky assets as a preset target date approaches, often used for retirement.",
  ["养老目标日期基金", "Target date fund", "Lifecycle fund"])
c("inst.private_fund", ["inst.fund"], "私募基金", "Private fund",
  "仅向合格投资者非公开募集的投资基金。",
  "An investment fund raised privately and only from qualified investors.",
  ["私募投资基金"])
c("inst.hedge_fund", ["inst.private_fund"], "对冲基金", "Hedge fund",
  "运用杠杆、做空和衍生品等多种策略追求绝对收益的私募基金。",
  "A private fund using strategies such as leverage, short selling and derivatives to pursue absolute returns.",
  ["Hedge funds"])
c("inst.reit", ["inst.security"], "房地产投资信托", "Real estate investment trust",
  "持有并经营收益性房地产、将大部分收益分配给投资者的可交易工具。",
  "A tradable vehicle that owns and operates income-producing real estate and distributes most income to investors.",
  ["REIT", "REITs", "不动产投资信托"])
c("inst.derivative", ["inst.financial_instrument"], "衍生品", "Derivative",
  "价值取决于股票、利率、汇率、商品等基础资产的金融合约。",
  "A financial contract whose value depends on an underlying asset such as stocks, rates, currencies or commodities.",
  ["金融衍生品", "衍生工具", "Derivatives"])
c("inst.option", ["inst.derivative"], "期权", "Option",
  "赋予买方在约定期限内以约定价格买入或卖出基础资产权利的合约。",
  "A contract giving the buyer the right, but not the obligation, to buy or sell an underlying asset at a set price within a set period.",
  ["Options"])
c("inst.call_option", ["inst.option"], "看涨期权", "Call option",
  "赋予买方以约定价格买入基础资产权利的期权。",
  "An option giving the buyer the right to buy the underlying asset at the strike price.",
  ["认购期权"])
c("inst.put_option", ["inst.option"], "看跌期权", "Put option",
  "赋予买方以约定价格卖出基础资产权利的期权。",
  "An option giving the buyer the right to sell the underlying asset at the strike price.",
  ["认沽期权"])
c("inst.future", ["inst.derivative"], "期货", "Futures contract",
  "在交易所交易、约定未来以确定价格交割标准化资产的合约。",
  "An exchange-traded contract to deliver a standardised asset at a set price on a future date.",
  ["期货合约", "Futures", "Future"])
c("inst.forward", ["inst.derivative"], "远期合约", "Forward contract",
  "双方私下约定未来以确定价格买卖资产的非标准化合约。",
  "A privately negotiated, non-standardised contract to buy or sell an asset at a set price in the future.",
  ["远期", "Forward"])
c("inst.swap", ["inst.derivative"], "互换", "Swap",
  "双方约定在一段时间内交换现金流的衍生品合约。",
  "A derivative contract in which two parties exchange cash flows over a period of time.",
  ["掉期", "Swaps"])
c("inst.interest_rate_swap", ["inst.swap"], "利率互换", "Interest rate swap",
  "双方交换固定利率与浮动利率利息支付的互换。",
  "A swap in which parties exchange fixed-rate and floating-rate interest payments.",
  ["利率掉期"])
c("inst.cds", ["inst.swap"], "信用违约互换", "Credit default swap",
  "买方定期付费、在参考实体违约时获得补偿的信用衍生品。",
  "A credit derivative in which the buyer pays a periodic fee and is compensated if a reference entity defaults.",
  ["CDS"])
c("inst.structured_product", ["inst.financial_instrument"], "结构化产品", "Structured product",
  "将固定收益工具与衍生品组合、收益与特定标的挂钩的产品。",
  "A product combining fixed income with derivatives so that returns are linked to a specified underlying.",
  ["结构性产品", "Structured note"])
c("inst.structured_deposit", ["inst.structured_product"], "结构性存款", "Structured deposit",
  "在存款基础上嵌入衍生品、收益与利率、汇率或指数等挂钩的产品。",
  "A deposit with an embedded derivative whose return is linked to rates, currencies or indices.",
  ["结构存款"])
c("inst.wealth_management_product", ["inst.financial_instrument"], "理财产品", "Wealth management product",
  "由银行或资产管理机构发行、为客户进行投资管理的产品统称。",
  "A general term for investment products issued by banks or asset managers to manage client money.",
  ["银行理财", "资管产品", "WMP"])

# ---------------------------------------------------------------- risk
c("risk.investment_risk", [], "投资风险", "Investment risk",
  "实际投资结果偏离预期、包括可能发生损失的不确定性。",
  "The uncertainty that actual investment outcomes differ from expectations, including the possibility of loss.",
  [])
c("risk.systematic", ["risk.investment_risk"], "系统性风险", "Systematic risk",
  "影响整个市场、无法通过分散化消除的风险。",
  "Risk affecting the whole market that cannot be eliminated through diversification.",
  ["不可分散风险", "Undiversifiable risk"])
c("risk.unsystematic", ["risk.investment_risk"], "非系统性风险", "Unsystematic risk",
  "仅影响个别公司或行业、可通过分散化降低的风险。",
  "Risk specific to individual companies or sectors that can be reduced through diversification.",
  ["特有风险", "可分散风险", "Idiosyncratic risk", "Specific risk"])
c("risk.market", ["risk.investment_risk"], "市场风险", "Market risk",
  "因市场价格（股价、利率、汇率、商品价格）变动导致损失的风险。",
  "The risk of loss from movements in market prices such as equity prices, interest rates, exchange rates and commodity prices.",
  ["价格风险"])
c("risk.equity_price", ["risk.market"], "股价风险", "Equity price risk",
  "因股票价格下跌导致损失的风险。",
  "The risk of loss from falling stock prices.",
  ["股票价格风险", "Equity risk"])
c("risk.interest_rate", ["risk.market"], "利率风险", "Interest rate risk",
  "因利率变动导致资产价值变化的风险，利率上升时债券价格通常下跌。",
  "The risk that changes in interest rates alter asset values; bond prices usually fall when rates rise.",
  [])
c("risk.fx", ["risk.market"], "汇率风险", "Currency risk",
  "因汇率变动导致以本币计价的投资价值变化的风险。",
  "The risk that exchange-rate movements change the home-currency value of an investment.",
  ["外汇风险", "货币风险", "FX risk", "Exchange rate risk"])
c("risk.commodity_price", ["risk.market"], "商品价格风险", "Commodity price risk",
  "因大宗商品价格变动导致损失的风险。",
  "The risk of loss from changes in commodity prices.",
  [])
c("risk.credit", ["risk.investment_risk"], "信用风险", "Credit risk",
  "借款人或发行人信用状况恶化甚至违约而导致损失的风险。",
  "The risk of loss because a borrower or issuer's creditworthiness deteriorates or it defaults.",
  ["信贷风险"])
c("risk.default", ["risk.credit"], "违约风险", "Default risk",
  "发行人无法按时足额支付本金或利息的风险。",
  "The risk that an issuer fails to pay principal or interest in full and on time.",
  [])
c("risk.counterparty", ["risk.credit"], "交易对手风险", "Counterparty risk",
  "交易对手未能履行合约义务而造成损失的风险，常见于场外衍生品。",
  "The risk that the other party fails to meet its contractual obligations, common in OTC derivatives.",
  ["对手方风险", "Counterparty credit risk"])
c("risk.liquidity", ["risk.investment_risk"], "流动性风险", "Liquidity risk",
  "无法以合理价格及时买卖资产的风险。",
  "The risk of being unable to buy or sell an asset quickly at a fair price.",
  ["变现风险"])
c("risk.inflation", ["risk.investment_risk"], "通胀风险", "Inflation risk",
  "通货膨胀侵蚀投资实际购买力的风险。",
  "The risk that inflation erodes the real purchasing power of an investment.",
  ["购买力风险", "Purchasing power risk"])
c("risk.reinvestment", ["risk.investment_risk"], "再投资风险", "Reinvestment risk",
  "收到的利息或本金只能以更低收益率再投资的风险。",
  "The risk that cash flows received must be reinvested at lower yields.",
  [])
c("risk.concentration", ["risk.investment_risk"], "集中度风险", "Concentration risk",
  "组合过度集中于少数资产、行业或地区而放大损失的风险。",
  "The risk of amplified losses from concentrating a portfolio in few assets, sectors or regions.",
  ["集中风险"])
c("risk.leverage", ["risk.investment_risk"], "杠杆风险", "Leverage risk",
  "使用借入资金或衍生品放大收益的同时也放大损失的风险。",
  "The risk that borrowing or derivatives magnify losses as well as gains.",
  [])
c("risk.tail", ["risk.investment_risk"], "尾部风险", "Tail risk",
  "发生概率很低但损失极大的极端事件风险。",
  "The risk of rare events that cause extreme losses.",
  ["黑天鹅风险"])
c("risk.sequence_of_returns", ["risk.investment_risk"], "收益顺序风险", "Sequence-of-returns risk",
  "在持续取款阶段，早期出现亏损会显著缩短资产可支撑时间的风险。",
  "The risk that poor returns early in a withdrawal phase significantly shorten how long savings last.",
  ["Sequence risk"])
c("risk.regulatory", ["risk.investment_risk"], "政策与监管风险", "Regulatory risk",
  "法律、监管或税收政策变化影响投资价值的风险。",
  "The risk that changes in law, regulation or tax policy affect investment value.",
  ["政策风险", "监管风险"])
c("risk.country", ["risk.investment_risk"], "国别风险", "Country risk",
  "因特定国家的政治、经济或资本管制因素导致损失的风险。",
  "The risk of loss arising from political, economic or capital-control factors in a specific country.",
  ["国家风险"])

# ---------------------------------------------------------------- metric
c("metric.return", [], "收益率", "Return",
  "一段时间内投资的盈亏占初始投入的比例。",
  "The gain or loss on an investment over a period, as a proportion of the amount invested.",
  ["回报率", "投资回报"])
c("metric.total_return", ["metric.return"], "总回报", "Total return",
  "包含价格变动及分红、利息等收入在内的全部收益。",
  "The full return including price change plus income such as dividends and interest.",
  ["总收益"])
c("metric.annualized_return", ["metric.return"], "年化收益率", "Annualized return",
  "将不同期限的收益换算为每年平均复合收益的指标。",
  "A return expressed as an average compound rate per year, enabling comparison across periods.",
  ["年化回报"])
c("metric.real_return", ["metric.return"], "实际收益率", "Real return",
  "扣除通货膨胀影响后的收益率。",
  "The return after adjusting for inflation.",
  ["真实收益率"])
c("metric.excess_return", ["metric.return"], "超额收益", "Excess return",
  "投资收益超出基准或无风险利率的部分。",
  "The portion of return above a benchmark or the risk-free rate.",
  ["超额回报"])
c("metric.risk_adjusted_return", ["metric.return"], "风险调整后收益", "Risk-adjusted return",
  "在考虑所承担风险后对收益进行衡量的一类指标。",
  "A family of measures that evaluate return relative to the risk taken.",
  ["风险调整收益"])
c("metric.sharpe", ["metric.risk_adjusted_return"], "夏普比率", "Sharpe ratio",
  "单位总波动所获得的超过无风险利率的收益。",
  "Return in excess of the risk-free rate per unit of total volatility.",
  ["夏普", "Sharpe"])
c("metric.sortino", ["metric.risk_adjusted_return"], "索提诺比率", "Sortino ratio",
  "只以下行波动衡量风险的风险调整后收益指标。",
  "A risk-adjusted return measure that uses only downside volatility as risk.",
  ["Sortino"])
c("metric.information_ratio", ["metric.risk_adjusted_return"], "信息比率", "Information ratio",
  "相对基准的超额收益除以跟踪误差，衡量主动管理效率。",
  "Excess return over a benchmark divided by tracking error, measuring active management efficiency.",
  [])
c("metric.alpha", [], "阿尔法", "Alpha",
  "在扣除市场风险贡献后，投资相对基准的超额表现。",
  "Performance relative to a benchmark after removing the contribution of market risk.",
  ["α", "Alpha收益", "Jensen's alpha"])
c("metric.beta", [], "贝塔系数", "Beta",
  "衡量资产相对整个市场波动敏感程度的指标。",
  "A measure of how sensitive an asset's returns are to movements of the overall market.",
  ["贝塔", "β"])
c("metric.volatility", [], "波动率", "Volatility",
  "资产价格或收益变动幅度的度量，通常以年化标准差表示。",
  "A measure of how much an asset's price or return fluctuates, usually expressed as annualised standard deviation.",
  ["波动性"])
c("metric.standard_deviation", [], "标准差", "Standard deviation",
  "衡量收益偏离其平均值程度的统计量。",
  "A statistic measuring how far returns deviate from their average.",
  ["Std dev"])
c("metric.max_drawdown", [], "最大回撤", "Maximum drawdown",
  "一段时间内资产净值从最高点到随后最低点的最大跌幅。",
  "The largest peak-to-trough decline in value over a period.",
  ["MDD", "Max drawdown"])
c("metric.var", [], "风险价值", "Value at risk",
  "在给定置信水平和期限内，组合可能遭受的最大损失估计。",
  "An estimate of the maximum loss a portfolio may suffer over a given horizon at a given confidence level.",
  ["在险价值", "VaR"])
c("metric.tracking_error", [], "跟踪误差", "Tracking error",
  "组合收益与基准收益之差的波动程度。",
  "The volatility of the difference between portfolio and benchmark returns.",
  [])
c("metric.correlation", [], "相关系数", "Correlation",
  "衡量两种资产收益同向变动程度的指标，取值在 -1 到 1 之间。",
  "A measure from -1 to 1 of how closely two assets' returns move together.",
  ["相关性"])
c("metric.duration", [], "久期", "Duration",
  "衡量债券价格对利率变动敏感程度的指标，久期越长利率风险越大。",
  "A measure of a bond's price sensitivity to interest rate changes; longer duration means higher interest rate risk.",
  ["Bond duration"])
c("metric.modified_duration", ["metric.duration"], "修正久期", "Modified duration",
  "利率变动 1% 时债券价格的近似百分比变化。",
  "The approximate percentage change in a bond's price for a 1% change in yield.",
  [])
c("metric.convexity", [], "凸性", "Convexity",
  "衡量债券价格与收益率关系弯曲程度、用于修正久期估计的指标。",
  "A measure of the curvature in the bond price-yield relationship, used to refine duration estimates.",
  [])
c("metric.dv01", [], "基点价值", "DV01",
  "收益率变动一个基点时债券价格的变动金额。",
  "The change in a bond's price for a one-basis-point change in yield.",
  ["PVBP", "BPV", "Dollar value of a basis point"])
c("metric.ytm", [], "到期收益率", "Yield to maturity",
  "按当前价格买入并持有至到期时债券的年化收益率。",
  "The annualised return of a bond if bought at the current price and held to maturity.",
  ["YTM"])
c("metric.coupon_rate", [], "票面利率", "Coupon rate",
  "债券每年支付的利息占面值的比例。",
  "The annual interest paid by a bond as a percentage of its face value.",
  ["息票率"])
c("metric.credit_spread", [], "信用利差", "Credit spread",
  "信用债收益率与同期限无风险债券收益率之差，反映信用风险补偿。",
  "The yield difference between a credit bond and a risk-free bond of the same maturity, reflecting compensation for credit risk.",
  [])
c("metric.credit_rating", [], "信用评级", "Credit rating",
  "评级机构对发行人或债券偿债能力和违约可能性的评估等级。",
  "An agency's assessment of an issuer's or bond's ability to repay and likelihood of default.",
  ["评级"])
c("metric.dividend_yield", [], "股息率", "Dividend yield",
  "每股年度股息占股价的比例。",
  "Annual dividends per share divided by the share price.",
  ["股息收益率", "分红率"])
c("metric.valuation_multiple", [], "估值倍数", "Valuation multiple",
  "以价格或企业价值与财务指标之比衡量估值高低的一类指标。",
  "A family of ratios comparing price or enterprise value to a financial metric to gauge valuation.",
  ["估值指标"])
c("metric.pe", ["metric.valuation_multiple"], "市盈率", "Price-to-earnings ratio",
  "股价与每股收益之比。",
  "Share price divided by earnings per share.",
  ["PE", "P/E"])
c("metric.pb", ["metric.valuation_multiple"], "市净率", "Price-to-book ratio",
  "股价与每股净资产之比。",
  "Share price divided by book value per share.",
  ["PB", "P/B"])
c("metric.ev_ebitda", ["metric.valuation_multiple"], "企业价值倍数", "EV/EBITDA",
  "企业价值与息税折旧摊销前利润之比。",
  "Enterprise value divided by earnings before interest, taxes, depreciation and amortisation.",
  ["EV/EBITDA倍数"])
c("metric.eps", [], "每股收益", "Earnings per share",
  "公司净利润除以总股本。",
  "A company's net profit divided by the number of shares outstanding.",
  ["EPS"])
c("metric.roe", [], "净资产收益率", "Return on equity",
  "净利润与股东权益之比，衡量股东资本的盈利能力。",
  "Net profit divided by shareholders' equity, measuring profitability on shareholder capital.",
  ["ROE"])
c("metric.market_cap", [], "市值", "Market capitalization",
  "公司股价乘以总股本得到的市场价值。",
  "The market value of a company: share price multiplied by shares outstanding.",
  ["总市值", "Market cap"])
c("metric.expense_ratio", [], "费用率", "Expense ratio",
  "基金年度运营费用占基金资产的比例。",
  "A fund's annual operating expenses as a percentage of its assets.",
  ["总费用率", "TER", "Total expense ratio"])
c("metric.nav", [], "基金净值", "Net asset value",
  "基金资产减去负债后按份额计算的价值。",
  "A fund's assets minus liabilities, expressed per share or unit.",
  ["单位净值", "NAV"])
c("metric.aum", [], "资产管理规模", "Assets under management",
  "管理人代客户管理的资产总市值。",
  "The total market value of assets a manager manages on behalf of clients.",
  ["管理规模", "AUM"])
c("metric.turnover", [], "换手率", "Turnover ratio",
  "一段时间内组合买卖交易金额相对资产规模的比例。",
  "Trading volume over a period relative to the size of a portfolio.",
  ["周转率", "Portfolio turnover"])
c("metric.bid_ask_spread", [], "买卖价差", "Bid-ask spread",
  "最高买价与最低卖价之差，反映交易成本和流动性。",
  "The difference between the highest bid and lowest ask price, reflecting trading cost and liquidity.",
  ["买卖差价", "Bid-offer spread"])

# ---------------------------------------------------------------- strategy
c("strat.asset_allocation", [], "资产配置", "Asset allocation",
  "根据目标和风险承受能力，在不同资产类别之间分配投资比例。",
  "Dividing a portfolio among asset classes according to objectives and risk tolerance.",
  ["大类资产配置"])
c("strat.strategic_aa", ["strat.asset_allocation"], "战略资产配置", "Strategic asset allocation",
  "基于长期目标设定的长期目标资产比例。",
  "Long-term target asset weights set according to long-term objectives.",
  ["SAA"])
c("strat.tactical_aa", ["strat.asset_allocation"], "战术资产配置", "Tactical asset allocation",
  "根据中短期市场判断对战略比例进行的主动偏离。",
  "Active short- to medium-term deviations from strategic weights based on market views.",
  ["TAA"])
c("strat.risk_parity", ["strat.asset_allocation"], "风险平价", "Risk parity",
  "让各类资产对组合风险贡献大致相等的配置方法。",
  "An allocation approach in which each asset class contributes roughly equally to portfolio risk.",
  [])
c("strat.core_satellite", [], "核心-卫星策略", "Core-satellite strategy",
  "以低成本被动核心持仓为主、辅以少量主动卫星持仓的组合构建方法。",
  "A portfolio approach combining a low-cost passive core with smaller active satellite positions.",
  ["核心卫星策略", "Core-satellite"])
c("strat.diversification", [], "分散化投资", "Diversification",
  "将资金分散到相关性较低的多种资产，以降低组合整体风险。",
  "Spreading money across assets with low correlation to reduce overall portfolio risk.",
  ["分散投资", "分散化"])
c("strat.rebalancing", [], "再平衡", "Rebalancing",
  "定期或在偏离阈值时将组合调整回目标配置比例。",
  "Periodically or at drift thresholds bringing a portfolio back to its target weights.",
  ["组合再平衡"])
c("strat.dca", [], "定期定额投资", "Dollar-cost averaging",
  "按固定周期投入固定金额，以平滑买入成本。",
  "Investing a fixed amount at regular intervals to smooth the average purchase cost.",
  ["定投", "DCA"])
c("strat.buy_and_hold", [], "买入并持有", "Buy and hold",
  "长期持有资产、不因短期波动频繁交易的策略。",
  "A strategy of holding assets for the long term without frequent trading on short-term moves.",
  ["长期持有"])
c("strat.market_timing", [], "择时", "Market timing",
  "试图通过预测市场涨跌来决定买入卖出时机的做法。",
  "Trying to decide when to buy or sell by predicting market moves.",
  ["市场择时"])
c("strat.passive", [], "被动投资", "Passive investing",
  "以跟踪指数为目标、低成本低换手的投资方式。",
  "A low-cost, low-turnover approach that aims to track an index.",
  ["指数化投资", "被动管理", "Passive management"])
c("strat.active", [], "主动投资", "Active management",
  "管理人通过选券和择时力图跑赢基准的投资方式。",
  "An approach in which managers use security selection and timing to try to beat a benchmark.",
  ["主动管理", "Active investing"])
c("strat.value", [], "价值投资", "Value investing",
  "买入价格低于内在价值证券的投资风格。",
  "An investment style buying securities priced below their intrinsic value.",
  ["价值风格"])
c("strat.growth", [], "成长投资", "Growth investing",
  "投资于盈利预期高速增长企业的投资风格。",
  "An investment style focused on companies expected to grow earnings rapidly.",
  ["成长风格"])
c("strat.factor", [], "因子投资", "Factor investing",
  "系统性地暴露于价值、动量、质量、低波等收益因子的投资方法。",
  "Systematically targeting return factors such as value, momentum, quality and low volatility.",
  ["Smart Beta", "聪明贝塔"])
c("strat.hedging", [], "对冲", "Hedging",
  "建立反向头寸以降低特定风险敞口的做法。",
  "Taking an offsetting position to reduce a specific risk exposure.",
  ["风险对冲", "Hedge"])
c("strat.immunization", [], "免疫策略", "Immunization",
  "使债券组合久期与负债期限匹配，以抵消利率变动影响的策略。",
  "Matching a bond portfolio's duration to its liability horizon to offset the impact of rate changes.",
  ["利率免疫"])
c("strat.laddering", [], "债券阶梯", "Bond laddering",
  "将资金分散投资于不同到期日的债券，按期滚动再投资。",
  "Spreading money across bonds with staggered maturities and reinvesting as each matures.",
  ["阶梯式投资", "Bond ladder"])
c("strat.leverage", [], "杠杆投资", "Leveraged investing",
  "借入资金或使用衍生品以放大投资敞口。",
  "Using borrowed money or derivatives to magnify investment exposure.",
  ["加杠杆", "Leverage"])
c("strat.income", [], "收益型投资", "Income investing",
  "以获取稳定利息、股息等现金收入为主要目标的投资方式。",
  "An approach aiming primarily at steady cash income such as interest and dividends.",
  ["收入型投资"])
c("strat.esg", [], "ESG 投资", "ESG investing",
  "在投资决策中纳入环境、社会和公司治理因素的方法。",
  "Incorporating environmental, social and governance factors into investment decisions.",
  ["可持续投资", "责任投资", "ESG", "Sustainable investing"])
c("strat.glide_path", [], "下滑轨道", "Glide path",
  "随目标日期临近逐步降低风险资产比例的配置路径。",
  "The schedule by which risky-asset weight declines as a target date approaches.",
  ["下滑曲线"])
c("strat.stop_loss", [], "止损", "Stop-loss",
  "在价格跌至预设水平时卖出以限制损失的规则。",
  "A rule to sell when the price falls to a preset level, limiting losses.",
  ["止损策略", "Stop loss"])
c("strat.long_short", [], "多空策略", "Long-short strategy",
  "同时买入看好的资产并卖空看淡的资产的策略。",
  "A strategy that buys assets expected to rise and short sells those expected to fall.",
  ["股票多空", "Long/short"])

# ---------------------------------------------------------------- macro
c("macro.interest_rate", [], "利率", "Interest rate",
  "借贷资金的价格，以本金的百分比表示。",
  "The price of borrowing money, expressed as a percentage of principal.",
  ["利息率"])
c("macro.policy_rate", ["macro.interest_rate"], "政策利率", "Policy rate",
  "中央银行用以实施货币政策的基准利率。",
  "The benchmark rate a central bank uses to implement monetary policy.",
  ["基准利率"])
c("macro.rate_hike", [], "加息", "Rate hike",
  "中央银行上调政策利率。",
  "A central bank raising its policy rate.",
  ["升息", "Rate increase"])
c("macro.rate_cut", [], "降息", "Rate cut",
  "中央银行下调政策利率。",
  "A central bank lowering its policy rate.",
  ["减息", "Rate reduction"])
c("macro.monetary_policy", [], "货币政策", "Monetary policy",
  "中央银行通过利率和货币供应调节经济的政策。",
  "Central bank policy that steers the economy through interest rates and money supply.",
  [])
c("macro.quantitative_easing", ["macro.monetary_policy"], "量化宽松", "Quantitative easing",
  "中央银行大规模购买资产以压低长期利率、增加流动性的政策。",
  "Large-scale central bank asset purchases to lower long-term rates and add liquidity.",
  ["QE"])
c("macro.fiscal_policy", [], "财政政策", "Fiscal policy",
  "政府通过税收和支出调节经济的政策。",
  "Government policy that steers the economy through taxation and spending.",
  [])
c("macro.inflation", [], "通货膨胀", "Inflation",
  "一般物价水平持续上涨、货币购买力下降的现象。",
  "A sustained rise in the general price level, reducing the purchasing power of money.",
  ["通胀"])
c("macro.deflation", [], "通货紧缩", "Deflation",
  "一般物价水平持续下降的现象。",
  "A sustained fall in the general price level.",
  ["通缩"])
c("macro.cpi", [], "消费者价格指数", "Consumer price index",
  "衡量居民消费商品和服务价格变化的指数，常用于衡量通胀。",
  "An index tracking prices of consumer goods and services, commonly used to measure inflation.",
  ["CPI"])
c("macro.economic_growth", [], "经济增长", "Economic growth",
  "一个经济体产出随时间的增加。",
  "An increase in an economy's output over time.",
  [])
c("macro.gdp", [], "国内生产总值", "Gross domestic product",
  "一定时期内一国境内生产的全部最终产品和服务的价值。",
  "The value of all final goods and services produced within a country over a period.",
  ["GDP"])
c("macro.business_cycle", [], "经济周期", "Business cycle",
  "经济活动在扩张与收缩之间交替的周期性波动。",
  "The recurring fluctuation of economic activity between expansion and contraction.",
  ["景气周期", "Economic cycle"])
c("macro.recession", [], "经济衰退", "Recession",
  "经济活动显著且持续下滑的阶段。",
  "A significant, sustained decline in economic activity.",
  ["衰退"])
c("macro.unemployment", [], "失业率", "Unemployment rate",
  "劳动力中没有工作但在寻找工作的人口比例。",
  "The share of the labour force that is without work but seeking it.",
  [])
c("macro.yield_curve", [], "收益率曲线", "Yield curve",
  "同一信用等级债券收益率与期限关系的曲线。",
  "A curve showing yields of bonds of the same credit quality across maturities.",
  ["利率期限结构", "Term structure"])
c("macro.yield_curve_inversion", [], "收益率曲线倒挂", "Yield curve inversion",
  "短期收益率高于长期收益率的现象，常被视为衰退先行信号。",
  "When short-term yields exceed long-term yields, often seen as a leading signal of recession.",
  ["倒挂", "Inverted yield curve"])
c("macro.exchange_rate", [], "汇率", "Exchange rate",
  "一种货币兑换另一种货币的价格。",
  "The price of one currency in terms of another.",
  ["外汇汇率", "FX rate"])
c("macro.credit_cycle", [], "信用周期", "Credit cycle",
  "信贷扩张与收缩交替出现的周期。",
  "The alternating expansion and contraction of credit availability.",
  [])

# ---------------------------------------------------------------- market
c("market.bond_price", [], "债券价格", "Bond price",
  "债券在市场上的交易价格，与收益率呈反向变动。",
  "The market price of a bond, which moves inversely to its yield.",
  ["债价"])
c("market.index", [], "市场指数", "Market index",
  "按规则选取一篮子证券、反映市场或板块整体表现的指标。",
  "A rules-based basket of securities measuring the performance of a market or segment.",
  ["指数", "Index"])
c("market.benchmark", [], "业绩比较基准", "Benchmark",
  "用于评价投资组合表现的参照标准，通常为指数。",
  "A reference, usually an index, against which portfolio performance is evaluated.",
  ["基准", "比较基准"])
c("market.liquidity", [], "市场流动性", "Market liquidity",
  "资产能以接近公允价格快速成交的程度。",
  "The degree to which an asset can be traded quickly near its fair price.",
  ["流动性"])
c("market.bull_market", [], "牛市", "Bull market",
  "价格持续上涨、投资者情绪乐观的市场阶段。",
  "A market phase of sustained rising prices and optimistic sentiment.",
  ["Bull"])
c("market.bear_market", [], "熊市", "Bear market",
  "价格持续下跌、投资者情绪悲观的市场阶段。",
  "A market phase of sustained falling prices and pessimistic sentiment.",
  ["Bear"])
c("market.primary_market", [], "一级市场", "Primary market",
  "证券首次发行、资金从投资者流向发行人的市场。",
  "The market where securities are first issued and money flows from investors to issuers.",
  ["发行市场"])
c("market.secondary_market", [], "二级市场", "Secondary market",
  "已发行证券在投资者之间交易的市场。",
  "The market where previously issued securities trade between investors.",
  ["交易市场"])
c("market.ipo", [], "首次公开发行", "Initial public offering",
  "公司首次向公众发行股票并上市。",
  "A company's first sale of shares to the public and listing on an exchange.",
  ["IPO"])
c("market.dividend", [], "股息", "Dividend",
  "公司从利润中分配给股东的现金或股票。",
  "Cash or shares a company distributes to shareholders from its profits.",
  ["分红", "派息"])
c("market.coupon", [], "票息", "Coupon payment",
  "债券按期向持有人支付的利息。",
  "The periodic interest a bond pays to its holder.",
  ["债券利息", "Coupon"])
c("market.maturity", [], "到期日", "Maturity",
  "债券或其他债务工具偿还本金的日期。",
  "The date on which a bond or other debt instrument repays its principal.",
  ["Maturity date"])
c("market.fees", [], "投资费用", "Investment fees",
  "投资过程中支付的管理费、托管费、交易佣金等成本。",
  "Costs paid when investing, such as management fees, custody fees and trading commissions.",
  ["费用", "交易成本", "Fees"])
c("market.margin_trading", [], "融资融券", "Margin trading",
  "向券商借入资金买入证券或借入证券卖出的交易方式。",
  "Borrowing money from a broker to buy securities, or borrowing securities to sell.",
  ["保证金交易"])
c("market.short_selling", [], "卖空", "Short selling",
  "借入证券卖出、期望日后以更低价格买回获利的交易。",
  "Selling borrowed securities in the hope of buying them back later at a lower price.",
  ["做空", "Shorting"])
c("market.risk_premium", [], "风险溢价", "Risk premium",
  "投资者因承担风险而要求的高于无风险利率的额外收益。",
  "The extra return above the risk-free rate that investors require for bearing risk.",
  ["Equity risk premium"])
c("market.risk_free_rate", [], "无风险利率", "Risk-free rate",
  "理论上不承担违约风险的投资收益率，常以短期国债利率代表。",
  "The return on an investment with theoretically no default risk, often proxied by short-term government bill rates.",
  ["Rf"])

# ---------------------------------------------------------------- suitability
c("suit.suitability", [], "投资者适当性", "Suitability",
  "要求将合适的产品销售给合适投资者的原则和管理制度。",
  "The principle and rules requiring that the right products are sold to the right investors.",
  ["适当性管理", "适当性"])
c("suit.kyc", [], "了解你的客户", "Know your customer",
  "在提供服务前识别并了解客户身份、财务状况和投资需求的流程。",
  "The process of identifying a client and understanding their finances and needs before providing services.",
  ["KYC", "客户尽职调查"])
c("suit.investor_profile", [], "投资者画像", "Investor profile",
  "描述投资者目标、期限、风险承受能力和流动性需求的综合信息。",
  "A summary of an investor's objectives, horizon, risk tolerance and liquidity needs.",
  ["客户画像", "Client profile"])
c("suit.risk_tolerance", [], "风险承受能力", "Risk tolerance",
  "经评估确定的投资者在财务和心理上能够承受的损失程度。",
  "The assessed degree of loss an investor can bear financially and psychologically.",
  ["风险承受度", "风险承受等级"])
c("suit.risk_appetite", [], "风险偏好", "Risk appetite",
  "投资者主观上愿意承担风险的意愿。",
  "An investor's subjective willingness to take risk.",
  ["风险态度", "Risk attitude"])
c("suit.investment_horizon", [], "投资期限", "Investment horizon",
  "投资者计划持有投资直到需要使用资金的时间长度。",
  "How long an investor plans to hold investments before needing the money.",
  ["持有期限", "Time horizon"])
c("suit.liquidity_needs", [], "流动性需求", "Liquidity needs",
  "投资者在一定时间内需要动用资金的程度。",
  "How much and how soon an investor may need access to their money.",
  ["资金流动性需求"])
c("suit.investment_objective", [], "投资目标", "Investment objective",
  "投资者希望通过投资实现的目标，如保值、收入或增值。",
  "What an investor wants to achieve, such as capital preservation, income or growth.",
  ["理财目标", "Investment goal"])
c("suit.investor_risk_category", [], "投资者风险类型", "Investor risk category",
  "根据风险承受能力对投资者划分的等级。",
  "A classification of investors by assessed risk tolerance.",
  [])
c("suit.conservative", ["suit.investor_risk_category"], "保守型投资者", "Conservative investor",
  "以保本和稳定为首要目标、只能承受很小波动的投资者类型。",
  "An investor type prioritising capital preservation and stability, able to bear only small fluctuations.",
  ["保守型", "Conservative"])
c("suit.balanced", ["suit.investor_risk_category"], "平衡型投资者", "Balanced investor",
  "在收益和风险之间寻求平衡、可承受中等波动的投资者类型。",
  "An investor type balancing return and risk, able to bear moderate fluctuations.",
  ["平衡型", "Moderate investor"])
c("suit.aggressive", ["suit.investor_risk_category"], "进取型投资者", "Aggressive investor",
  "追求较高收益、可承受较大波动和亏损的投资者类型。",
  "An investor type seeking higher returns and able to bear large fluctuations and losses.",
  ["进取型", "激进型", "Aggressive"])
c("suit.product_risk_rating", [], "产品风险等级", "Product risk rating",
  "机构根据产品风险特征对其划分的等级，用于与投资者风险类型匹配。",
  "A grade assigned to a product by its risk characteristics, used to match investor risk categories.",
  ["产品风险评级"])
c("suit.qualified_investor", [], "合格投资者", "Qualified investor",
  "达到监管规定的资产或收入门槛、可投资私募等高风险产品的投资者。",
  "An investor meeting regulatory wealth or income thresholds, eligible for higher-risk products such as private funds.",
  ["Accredited investor"])
c("suit.risk_disclosure", [], "风险揭示", "Risk disclosure",
  "向投资者充分说明产品风险的义务和文件。",
  "The obligation, and documents, to explain product risks fully to investors.",
  ["风险提示", "风险揭示书"])
c("suit.retirement_planning", [], "退休规划", "Retirement planning",
  "为退休后的生活需求进行储蓄和投资安排的过程。",
  "The process of saving and investing to fund living needs in retirement.",
  ["养老规划"])
c("suit.emergency_fund", [], "应急资金", "Emergency fund",
  "为应对突发支出而预留的高流动性资金。",
  "Highly liquid money set aside for unexpected expenses.",
  ["应急储备金", "紧急备用金"])

# ---------------------------------------------------------------- behavioral
c("behav.behavioral_bias", [], "行为偏差", "Behavioral bias",
  "系统性偏离理性决策、影响投资判断的心理倾向。",
  "A psychological tendency that systematically departs from rational decision-making and affects investment judgement.",
  ["认知偏差", "Cognitive bias"])
c("behav.loss_aversion", ["behav.behavioral_bias"], "损失厌恶", "Loss aversion",
  "同等金额的损失带来的痛苦大于收益带来的快乐的倾向。",
  "The tendency to feel losses more strongly than gains of the same size.",
  [])
c("behav.herding", ["behav.behavioral_bias"], "羊群效应", "Herding",
  "跟随多数人的投资行为而忽视自身判断的倾向。",
  "The tendency to follow the crowd's investment behaviour instead of one's own judgement.",
  ["从众心理", "Herd behavior"])
c("behav.overconfidence", ["behav.behavioral_bias"], "过度自信", "Overconfidence",
  "高估自身判断准确性和能力的倾向。",
  "The tendency to overestimate the accuracy of one's own judgement and abilities.",
  [])
c("behav.anchoring", ["behav.behavioral_bias"], "锚定效应", "Anchoring",
  "过度依赖最初获得的信息（如买入价）作出判断的倾向。",
  "The tendency to rely too heavily on initial information, such as a purchase price, when deciding.",
  ["锚定偏差", "Anchoring bias"])
c("behav.disposition_effect", ["behav.behavioral_bias"], "处置效应", "Disposition effect",
  "过早卖出盈利资产、过久持有亏损资产的倾向。",
  "The tendency to sell winners too early and hold losers too long.",
  [])
c("behav.recency_bias", ["behav.behavioral_bias"], "近因偏差", "Recency bias",
  "过度看重近期事件、以为近期趋势会持续的倾向。",
  "The tendency to overweight recent events and assume recent trends will continue.",
  ["近期偏差"])
c("behav.confirmation_bias", ["behav.behavioral_bias"], "确认偏误", "Confirmation bias",
  "只关注支持自己既有观点信息的倾向。",
  "The tendency to seek out information that supports one's existing views.",
  ["证实偏差", "确认偏差"])
c("behav.mental_accounting", ["behav.behavioral_bias"], "心理账户", "Mental accounting",
  "将资金按来源或用途分别看待、而非整体考虑的倾向。",
  "The tendency to treat money differently depending on its source or intended use rather than as a whole.",
  [])
c("behav.home_bias", ["behav.behavioral_bias"], "本土偏好", "Home bias",
  "过度投资于本国或熟悉市场的倾向。",
  "The tendency to over-invest in one's home or familiar market.",
  ["本国偏好"])
c("behav.fomo", ["behav.behavioral_bias"], "错失恐惧", "Fear of missing out",
  "担心错过上涨机会而仓促追涨的心理。",
  "Anxiety about missing gains that leads to hasty buying into rallies.",
  ["FOMO", "怕错过"])


# ------------------------------------------------------------------ relations
# (src, rel, dst, polarity, confidence, note)
R = []
def r(src, rel, dst, polarity=None, conf=None, note=None):
    R.append(dict(src=src, rel=rel, dst=dst, polarity=polarity, conf=conf, note=note))

# rates & bonds
r("macro.interest_rate", "affects", "market.bond_price", -1, note="Rates up -> bond prices down")
r("macro.rate_hike", "affects", "market.bond_price", -1)
r("macro.rate_cut", "affects", "market.bond_price", 1)
r("macro.rate_hike", "opposite_of", "macro.rate_cut")
r("macro.rate_hike", "part_of", "macro.monetary_policy")
r("macro.rate_cut", "part_of", "macro.monetary_policy")
r("macro.rate_hike", "related", "macro.policy_rate")
r("macro.monetary_policy", "affects", "macro.policy_rate", None, note="Direction depends on stance")
r("macro.quantitative_easing", "affects", "macro.interest_rate", -1, conf=0.8, note="Mainly long-term rates")
r("market.bond_price", "affects", "metric.ytm", -1, note="Price and yield move inversely")
r("metric.duration", "measures", "risk.interest_rate")
r("metric.convexity", "measures", "risk.interest_rate")
r("metric.dv01", "measures", "risk.interest_rate")
r("metric.dv01", "related", "metric.duration")
r("metric.convexity", "related", "metric.duration")
r("asset.fixed_income", "exposed_to", "risk.interest_rate")
r("asset.fixed_income", "exposed_to", "risk.credit")
r("asset.fixed_income", "exposed_to", "risk.inflation")
r("asset.fixed_income", "exposed_to", "risk.reinvestment")
r("inst.high_yield_bond", "exposed_to", "risk.default")
r("inst.credit_bond", "exposed_to", "risk.credit")
r("inst.inflation_linked_bond", "mitigates", "risk.inflation")
r("inst.zero_coupon_bond", "mitigates", "risk.reinvestment", conf=0.9, note="No coupons to reinvest before maturity")
r("strat.immunization", "mitigates", "risk.interest_rate")
r("strat.laddering", "mitigates", "risk.reinvestment")
r("strat.laddering", "mitigates", "risk.interest_rate", conf=0.8)
r("inst.interest_rate_swap", "mitigates", "risk.interest_rate")
r("inst.cds", "mitigates", "risk.credit")
r("metric.credit_spread", "measures", "risk.credit")
r("metric.credit_rating", "measures", "risk.credit")
r("metric.ytm", "related", "metric.coupon_rate")
r("market.coupon", "related", "metric.coupon_rate")
r("market.maturity", "related", "metric.duration")
r("macro.yield_curve", "related", "macro.interest_rate")
r("macro.yield_curve_inversion", "part_of", "macro.yield_curve")
r("macro.yield_curve_inversion", "related", "macro.recession", conf=0.8, note="Historically a leading signal, not a guarantee")
r("macro.credit_cycle", "related", "metric.credit_spread")

# inflation
r("macro.inflation", "affects", "metric.real_return", -1)
r("macro.inflation", "affects", "macro.interest_rate", 1, conf=0.7, note="Tendency via central bank reaction")
r("macro.cpi", "measures", "macro.inflation")
r("macro.deflation", "opposite_of", "macro.inflation")
r("risk.inflation", "related", "macro.inflation")
r("asset.cash", "exposed_to", "risk.inflation")
r("asset.commodity", "mitigates", "risk.inflation", conf=0.6, note="Partial and inconsistent hedge")

# equity & risk metrics
r("asset.equity", "exposed_to", "risk.equity_price")
r("asset.equity", "exposed_to", "risk.systematic")
r("metric.beta", "measures", "risk.systematic")
r("metric.volatility", "measures", "risk.market")
r("metric.standard_deviation", "related", "metric.volatility")
r("metric.max_drawdown", "measures", "risk.market")
r("metric.var", "measures", "risk.market")
r("risk.tail", "related", "metric.var")
r("market.risk_free_rate", "part_of", "metric.sharpe")
r("market.risk_free_rate", "related", "macro.policy_rate")
r("metric.tracking_error", "part_of", "metric.information_ratio")
r("metric.tracking_error", "related", "inst.index_fund")
r("metric.tracking_error", "related", "market.benchmark")
r("metric.alpha", "related", "metric.excess_return")
r("metric.alpha", "related", "metric.beta")
r("metric.eps", "part_of", "metric.pe")
r("metric.roe", "related", "metric.pb")
r("market.dividend", "related", "metric.dividend_yield")
r("market.dividend", "part_of", "metric.total_return")
r("market.coupon", "part_of", "metric.total_return")
r("market.risk_premium", "related", "asset.equity")
r("market.risk_premium", "related", "market.risk_free_rate")
r("market.fees", "affects", "metric.total_return", -1)
r("metric.expense_ratio", "related", "market.fees")
r("metric.nav", "related", "inst.fund")

# risk structure
r("risk.systematic", "opposite_of", "risk.unsystematic")
r("risk.market", "related", "risk.systematic")
r("strat.diversification", "mitigates", "risk.unsystematic")
r("strat.diversification", "mitigates", "risk.concentration")
r("metric.correlation", "related", "strat.diversification")
r("strat.hedging", "mitigates", "risk.market")
r("strat.hedging", "related", "inst.derivative")
r("inst.put_option", "mitigates", "risk.equity_price")
r("inst.forward", "mitigates", "risk.fx", conf=0.9, note="Common FX hedging tool")
r("inst.derivative", "exposed_to", "risk.counterparty", conf=0.8, note="Mainly OTC derivatives")
r("inst.derivative", "exposed_to", "risk.leverage")
r("strat.leverage", "exposed_to", "risk.leverage")
r("market.margin_trading", "exposed_to", "risk.leverage")
r("market.margin_trading", "related", "strat.leverage")
r("metric.bid_ask_spread", "measures", "risk.liquidity")
r("market.liquidity", "related", "risk.liquidity")
r("asset.private_equity", "exposed_to", "risk.liquidity")
r("asset.real_estate", "exposed_to", "risk.liquidity")
r("inst.private_fund", "exposed_to", "risk.liquidity")
r("inst.structured_product", "exposed_to", "risk.liquidity")
r("inst.structured_product", "exposed_to", "risk.credit", note="Issuer credit risk")
r("risk.fx", "related", "macro.exchange_rate")
r("strat.stop_loss", "mitigates", "risk.market", conf=0.7, note="Limits loss per position; gaps can exceed stop")

# strategy
r("strat.rebalancing", "part_of", "strat.asset_allocation")
r("strat.core_satellite", "related", "strat.asset_allocation")
r("strat.core_satellite", "related", "strat.passive")
r("strat.passive", "opposite_of", "strat.active")
r("inst.index_fund", "related", "strat.passive")
r("inst.etf", "related", "strat.passive")
r("strat.value", "opposite_of", "strat.growth")
r("strat.factor", "related", "strat.passive")
r("strat.factor", "related", "strat.active")
r("strat.dca", "related", "strat.market_timing", note="DCA avoids timing decisions")
r("strat.buy_and_hold", "related", "strat.market_timing", note="Often contrasted")
r("strat.income", "related", "market.dividend")
r("strat.income", "related", "inst.bond")
r("strat.glide_path", "part_of", "inst.target_date_fund")
r("strat.long_short", "related", "inst.hedge_fund")
r("market.short_selling", "part_of", "strat.long_short")
r("asset.multi_asset", "related", "strat.asset_allocation")
r("inst.equity_fund", "related", "asset.equity")
r("inst.bond_fund", "related", "asset.fixed_income")
r("inst.balanced_fund", "related", "asset.multi_asset")
r("inst.money_market_fund", "related", "inst.money_market_instrument")
r("inst.reit", "related", "asset.real_estate")
r("inst.preferred_stock", "related", "asset.fixed_income")
r("inst.convertible_bond", "related", "inst.stock")
r("inst.structured_deposit", "related", "inst.deposit")
r("inst.hedge_fund", "related", "asset.alternative")

# suitability
for x in ["suit.risk_tolerance", "suit.risk_appetite", "suit.investment_horizon",
          "suit.liquidity_needs", "suit.investment_objective"]:
    r(x, "part_of", "suit.investor_profile")
for x in ["suit.kyc", "suit.investor_profile", "suit.product_risk_rating", "suit.risk_disclosure"]:
    r(x, "part_of", "suit.suitability")
r("suit.investor_risk_category", "related", "suit.risk_tolerance")
r("suit.product_risk_rating", "related", "suit.investor_risk_category")
SF = "Indicative only; actual matching uses the product risk rating"
r("inst.money_market_fund", "suitable_for", "suit.conservative", conf=0.7, note=SF)
r("inst.deposit", "suitable_for", "suit.conservative", conf=0.7, note=SF)
r("inst.government_bond", "suitable_for", "suit.conservative", conf=0.6, note=SF)
r("inst.balanced_fund", "suitable_for", "suit.balanced", conf=0.6, note=SF)
r("inst.equity_fund", "suitable_for", "suit.aggressive", conf=0.6, note=SF)
r("inst.private_fund", "related", "suit.qualified_investor")
r("inst.derivative", "related", "suit.qualified_investor", conf=0.7)
r("suit.emergency_fund", "related", "asset.cash")
r("suit.emergency_fund", "related", "suit.liquidity_needs")
r("suit.investment_horizon", "related", "asset.equity", conf=0.7, note="Longer horizons can absorb equity volatility")
r("suit.retirement_planning", "related", "risk.sequence_of_returns")
r("suit.retirement_planning", "related", "strat.glide_path")
r("suit.retirement_planning", "related", "inst.target_date_fund")

# macro
r("macro.fiscal_policy", "related", "macro.economic_growth")
r("macro.gdp", "measures", "macro.economic_growth")
r("macro.recession", "part_of", "macro.business_cycle")
r("macro.economic_growth", "related", "macro.business_cycle")
r("macro.unemployment", "related", "macro.business_cycle")
r("macro.business_cycle", "related", "macro.credit_cycle")

# market
r("market.bull_market", "opposite_of", "market.bear_market")
r("market.ipo", "part_of", "market.primary_market")
r("market.primary_market", "related", "market.secondary_market")
r("market.index", "related", "inst.index_fund")
r("market.benchmark", "related", "market.index")

# behavioral
r("behav.home_bias", "affects", "risk.concentration", 1)
r("behav.overconfidence", "affects", "metric.turnover", 1, conf=0.8, note="Overconfident investors tend to trade more")
r("behav.herding", "related", "behav.fomo")
r("behav.loss_aversion", "related", "behav.disposition_effect")
r("behav.recency_bias", "related", "behav.herding")
r("behav.fomo", "related", "strat.market_timing")
r("behav.anchoring", "related", "behav.disposition_effect")

# fill isolated
r("metric.aum", "related", "inst.fund")
r("metric.market_cap", "related", "asset.equity")
r("metric.market_cap", "related", "market.index", note="Many indices are cap-weighted")
r("strat.esg", "related", "strat.factor", conf=0.6, note="ESG often implemented as a tilt alongside factors")
r("strat.esg", "related", "strat.active", conf=0.6)

# link macro drivers to the risks they create
r("risk.interest_rate", "related", "macro.interest_rate")
r("market.bond_price", "related", "risk.interest_rate", note="Rate-driven bond price moves are interest rate risk")
