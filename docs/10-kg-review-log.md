# 10 · 概念图谱评审日志

每个版本都经过一次**独立评审**（评审者未参与编写），本文记录发现与处理。规则见 [09](09-kg-rules.md)。

## v0.1 → 第一轮评审（2026-10-15）

| 类别 | 主要发现 | 处理（v0.2） |
|---|---|---|
| 合规 | `suitable_for` 边会让 Agent 输出"XX 适合 XX 投资者"；"国债适合保守型"尤其危险 | 基础层删除全部 `suitable_for`，schema 禁止；典型风险等级写入 `scope_note` |
| 定义 | 货基 / 理财 / 结构性存款 / 黄金 / 国债缺"不保本"措辞 | 定义补齐 |
| 术语 | 中文"收益率"在债券语境指 yield，却映射到 return | 新建 `metric.yield` |
| 层级 | 夏普等比率经传递成"一种收益率"；结构性存款应是存款；再投资风险属利率风险 | 修正 |
| 关系 | `part_of` 混用"组成 / 阶段 / 公式输入" | 新增 `input_of`，阶段改 `related` |
| 别名 | 泛词（商品、指数、评级）和单词级英文别名误伤严重 | 降为 `hidden` |
| 缺口 | 费用结构、赎回条款、保本 / 刚兑、投资级、CVaR、年金、税收、宏观→资产 | 新增 32 个概念 |

## v0.2 → 第二轮评审（2026-10-15）

评分 6 / 10。结论："规则没定清就改数据"导致系统性不一致。

| 发现 | 处理（v0.3） |
|---|---|
| 黄金改成 `belongs_to` 是改坏了 | 恢复 `is_a 大宗商品` |
| "超额收益率"错挂 alpha | 移到 `metric.excess_return` |
| "利率上行"并入"加息"，但债市语境指市场利率 | 新建 `macro.rates_rising / rates_falling` |
| 普通 / 专业投资者混进风险承受类型树 | 拆成三棵子树：通用风险类型、大陆 C1–C5（`suit.cn_risk_level`）、投资者资格（零售 / 认可 / 专家 / 机构 / 专业 / 合格） |
| 费用、赎回条款子树用 `is_a` 表组成 | 改 `part_of`；新建"基金运作方式"承接开放式 / 封闭式 |
| 8 类基金被钉死为公募 | 只 `is_a` 基金；与公募用 `related` 标注"通常公开发售" |
| "ES"与 Elasticsearch 冲突；提前偿付 ≠ 赎回风险 | ES 降 hidden；新建 `risk.prepayment` |
| 债价 ↔ 收益率是恒等关系，不是 affects | 改 `related` |
| 缩写降级无规则（SAA 降了、ETF 没降） | 规则化：≥3 字符无歧义缩写为 `abbr`，2 字符一律 `hidden`，由生成器按规则判定 |
| 删了"企业债 / 资管产品"无概念接住 | 新建 `inst.enterprise_bond`（CN）、`inst.asset_management_product` |
| 置信度只给新边设默认值 | 全部按关系类型回填，手工下调的保留 |
| docs/03 与 schema 不同步 | 同步 |

## v0.3 新增

- **规则文档** [09](09-kg-rules.md)，校验器强制执行：关系的 scheme 约束、`is_a` / `part_of` 父节点层级不高于子节点、可见标签不得跨概念重复、2 字符缩写必须 hidden、置信度非空
- **新加坡本地化**（`jurisdiction = SG`，27 个概念）：MAS、SFA、FAA、Fair Dealing、SIP / EIP、CKA / CAR、认可 / 专家 / 机构投资者、CPF（OA / SA）、CPFIS、CPF LIFE、SRS、SSB、SGS、T-bill、单位信托、ILP、储蓄保险、S-REIT、双货币投资、SGX、STI、SORA、无资本利得税。监管数字只写在 `scope_note` 并标"以 MAS / IRAS 当前规定为准"
- **大陆高频术语**（`jurisdiction = CN`，14 个）：企业债、金融债、地方债、同业存单、信托计划、固收+、七日年化、预期收益型、LPR、C1–C5
- **三个层级**：基础 135 · 进阶 183 · 完整 278 个概念，导出在 `kg/seed/tiers/`

校验器首次运行即抓到 11 处违反规则的边（如 `margin_trading exposed_to`、`short_selling part_of long_short`），全部修正。

## v0.3 → 第三轮评审

见下方更新。
