# kg · 金融投资概念图谱

Agent 的"投资顾问大脑"：金融投资概念、术语与关系（不含具体公司、证券、持仓）。

定位见 [docs/03](../docs/03-concept-graph.md)，建模规则见 [docs/09](../docs/09-kg-rules.md)，评审日志见 [docs/10](../docs/10-kg-review-log.md)。主辖区新加坡（SG），中国大陆（CN）为第二辖区，中英文双语。

| 文件 | 内容 |
|---|---|
| `schema.sql` | PostgreSQL DDL：`concept` / `label` / `relation` / `evidence` / `call_audit` |
| `load.sql` | 把 `seed/*.csv` 装载进数据库（在仓库根目录执行） |
| `queries.sql` | Agent 工具背后的参考查询：resolve_terms、get_concept、explain_path、expand_query，以及写入 call_audit |
| `seed/concept.csv` | 278 个概念（11 个分类，含 `tier` 层级与 `jurisdiction` 辖区） |
| `seed/label.csv` | 988 个中英文标签（pref / alt / abbr / hidden） |
| `seed/relation.csv` | 450 条关系 |
| `seed/evidence.csv` | 1006 条证据 |
| `seed/tiers/basic/` | 基础版：135 个概念 |
| `seed/tiers/advanced/` | 进阶版：183 个概念 |
| `tools/validate.py` | 按 [docs/09](../docs/09-kg-rules.md) 校验 |
| `build/` | 生成脚本：`seed_concepts.py`（v0.1）→ `seed_v02.py` → `seed_v03.py` → `gen_seed.py`；运行 `python3 kg/build/gen_seed.py` 重建全部 CSV |

```bash
python3 kg/tools/validate.py
psql -d <db> -f kg/schema.sql
psql -d <db> -f kg/load.sql
```

> 种子 v0.3 全部为 `draft`，需投资专家审核后才能用于生产。生成脚本 `kg/build/` 是事实来源：修改脚本后重跑生成，不要直接改 CSV。
