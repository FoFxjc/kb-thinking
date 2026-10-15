# 09 · 概念图谱建模规则

两轮独立评审（见 [10](10-kg-review-log.md)）的共同结论是：先把规则写下来，再按规则回填数据。本文是概念图谱的**强制规则**，`kg/tools/validate.py` 逐条检查。

## 1. 辖区与语言

- 主辖区：**新加坡（SG）**。概念的 `jurisdiction` 取 `global` / `SG` / `CN`；`global` 为默认。
- 中国大陆（CN）概念保留，作为第二辖区，用于中文语境的对照（如 C1–C5 分级），但 Agent 默认按 SG 回答。
- 所有概念都有中英文首选名和定义。定义自行撰写，不复制外部来源。
- 监管门槛、税率、额度等**会变化的数字只写在 `scope_note` 里并标注"以 MAS / IRAS 当前规定为准"**，不进定义。

## 2. 层级（tier）

| tier | 名称 | 目标 | 规模 |
|---|---|---|---|
| 1 | 基础 Basic | 零售客户问答必需：主要资产类别、常见产品、主要风险、常用指标、基本策略、适当性与本地制度 | ~110 |
| 2 | 进阶 Advanced | 顾问日常：细分产品、债券与估值指标、宏观传导、费用与条款、行为偏差 | ~210 |
| 3 | 完整 Full | 全部：衍生品细分、专业指标、另类资产、跨境制度 | 全部 |

规则：**基础 ⊂ 进阶 ⊂ 完整**；一个概念的 `is_a` / `part_of` 父节点的 tier 不得高于它自己（父节点必须在同一层级或更基础的层级出现）。导出某层级时，只保留两端都在该层级内的关系。

## 3. 分类（scheme）

`asset_class` 资产类别 · `instrument` 产品与工具 · `risk` 风险 · `metric` 指标 · `strategy` 策略与配置 · `macro` 宏观 · `market` 市场与交易 · `terms` 产品条款与费用 · `suitability` 适当性与投资者 · `scheme_local` 本地制度（CPF、SRS、SIP 等） · `behavioral` 行为金融

## 4. 关系语义（强制）

| 关系 | 含义 | src → dst 的 scheme 约束 | 对称 | 备注 |
|---|---|---|---|---|
| `is_a` | src 是 dst 的一种（分类） | **同一 scheme** | 否 | 只表分类，不表组成 |
| `part_of` | src 是 dst 的**组成部分** | 同一 scheme | 否 | 不用于"阶段""操作""公式输入" |
| `input_of` | src 是指标 dst 的计算输入 | dst 必须是 metric | 否 | |
| `belongs_to` | 工具 src 归入资产类别 dst | instrument → asset_class | 否 | 工具与资产类别之间**只能**用它 |
| `measures` | 指标 src 度量 dst | metric / macro → risk / macro / market | 否 | 宏观统计量（CPI、GDP）度量宏观变量 |
| `affects` | src 影响 dst，`polarity` +1 / −1 / 空 | macro / market / terms / behavioral → 任意 | 否 | 恒等关系（债价 ↔ 收益率）不用 affects |
| `exposed_to` | src 承担风险 dst | asset_class / instrument / strategy / scheme_local → risk | 否 | |
| `mitigates` | src 缓释风险 dst | strategy / instrument / asset_class → risk | 否 | |
| `opposite_of` | 相对概念 | 同一 scheme | 是 | |
| `related` | 弱关联 | 任意 | 是 | 只在以上关系都不适用时使用 |
| `suitable_for` | **保留给规则层** | — | — | 基础层禁止出现 |

## 5. 标签规则（强制）

| kind | 用途 | 判定 |
|---|---|---|
| `pref` | 展示名，每概念每语言恰好一个 | 必须脱离上下文可理解（"开放式基金"而不是"开放式"） |
| `alt` | 可直接匹配的别名 | 中文 ≥ 3 字，或 2 字但为金融专名（如"久期""国债"）；英文 ≥ 2 个词，或单词但为金融专名（Duration 不算，Immunization 算） |
| `abbr` | 可直接匹配的缩写 | 全大写 ≥ 3 字符且在金融语境无歧义（ETF、CDS、YTM、NAV、VaR、SAA）。2 字符缩写一律 hidden（PE、PB、ES、IR） |
| `hidden` | 只在上下文消歧后匹配，不展示 | 泛词（指数、基准、费用、流动性、商品）、英文日常词（return、option、cash、fund）、希腊字母 |

补充：
- 同一词不得同时是两个概念的 `pref` / `alt`；允许同为 `hidden`
- 删除某标签时，若该词是高频术语，必须有另一概念接住（如"企业债"→ `inst.enterprise_bond`）
- 中文"收益率"默认指 `metric.yield`；"回报率"指 `metric.return`

## 6. 置信度（强制默认值，专家审核时可改）

| 关系 | 默认 |
|---|---|
| is_a, part_of, input_of, belongs_to | 1.0 |
| opposite_of, measures | 0.95 |
| exposed_to | 0.9 |
| affects, mitigates | 0.85 |
| related | 0.75 |

有争议的边手工下调并在 `note` 写原因。

## 7. 合规措辞

- 任何可能被理解为保本、保收益、避险的定义，必须带"不保证本金 / 不代表无价格风险"
- 产品的典型风险等级只写在 `scope_note`（"MAS 框架下通常归为 SIP / EIP；机构内部风险评级通常为 …"），不做 `suitable_for` 边
- 历史规律（收益率曲线倒挂 → 衰退）一律写"历史上通常……，不构成预测"
- 定投只能写"平滑买入成本"，不能写"降低风险 / 提高收益"
