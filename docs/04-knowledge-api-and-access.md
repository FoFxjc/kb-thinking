# 04 · Knowledge API 与访问层

## 1. 原则

- **Knowledge API 是唯一访问入口**：Portal 与 Agent 都不直连 ES 或 Postgres
- **身份透传**：每次调用都带真实用户身份（OIDC），Agent 以 on-behalf-of 方式调用
- **权限只执行一次**：在 Knowledge API 内统一做 ACL 过滤

## 2. Knowledge API（逻辑接口）

| 能力 | 说明 | 后端 |
|---|---|---|
| `search` | 混合检索（BM25 + kNN），支持按概念、来源、时间过滤 | ES |
| `ask` | 检索 + 概念推理 + LLM 生成，返回答案与引用 | ES + 概念图谱 + 回答层 |
| `resolve_terms` | 文本 → 标准概念 | 概念图谱 |
| `get_concept` | 概念详情 | 概念图谱 |
| `explain_path` | 两概念之间的关系链 | 概念图谱 |
| `expand_query` | 概念扩展检索词 | 概念图谱 |
| `get_source` | 返回 chunk 的溯源信息与原文访问链接（先校验权限） | ES + Hub DB |

## 3. 入口

### 3.1 MCP server（MVP 主入口）

把上述能力以工具形式暴露给 Agent；工具粒度与 Knowledge API 一一对应，便于审计。

### 3.2 Thin portal（内部用户）

- **Search**：结果带高亮、出处（Ozone 路径、页码）、概念标签
- **Ask**：带引用的回答，展示用到的概念关系
- MVP 不做 Graph explore 可视化

## 4. 回答层与合规护栏

MVP 的基础护栏：

1. **必须引用**：回答中的事实需对应到具体 chunk
2. **免责声明**：投资相关回答统一附带
3. **不给个性化投资建议**：识别"我该买什么"类问题，转为知识性解释
4. **术语一致**：使用概念图谱中的标准定义

是否面向终端客户会极大改变护栏的要求（适当性规则、话术审核、留痕），这是第 0 阶段必须确认的问题。

## 5. 权限（MVP）

- **集合级 ACL**：一个文档集合对应一组可访问用户组，写入每个 chunk 的 `acl_groups`
- 概念图谱本身视为内部通用知识，MVP 不做细粒度权限
- 文档级 ACL 同步属于 MVP 之后

## 6. 审计

每次 `ask` 记录：用户、问题、用到的概念、引用的 `chunk_id` 与文档版本、模型版本、时间。MVP 存于 Hub DB（或独立审计表），将来可导出到 Iceberg。
