# kg · 金融投资概念图谱

Agent 的"投资顾问大脑"：金融投资概念、术语与关系（不含具体公司、证券、持仓）。

设计与调研见 [docs/08-concept-graph-seed.md](../docs/08-concept-graph-seed.md)，定位见 [docs/03-concept-graph.md](../docs/03-concept-graph.md)。

| 文件 | 内容 |
|---|---|
| `schema.sql` | PostgreSQL DDL：`concept` / `label` / `relation` / `evidence` / `call_audit` |
| `load.sql` | 把 `seed/*.csv` 装载进数据库（在仓库根目录执行） |
| `queries.sql` | Agent 工具背后的参考查询：resolve_terms、get_concept、explain_path、expand_query，以及写入 call_audit |
| `seed/concept.csv` | 197 个概念（9 个分类） |
| `seed/label.csv` | 692 个中英文标签 |
| `seed/relation.csv` | 265 条关系 |
| `seed/evidence.csv` | 659 条证据 |
| `tools/validate.py` | 校验 CSV（引用完整、无环、关系类型等） |

```bash
python3 kg/tools/validate.py
psql -d <db> -f kg/schema.sql
psql -d <db> -f kg/load.sql
```

> 种子 v0.1 全部为 `draft`，需投资专家审核后才能用于生产。CSV 是唯一的事实来源。
