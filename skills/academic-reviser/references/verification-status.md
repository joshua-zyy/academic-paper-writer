# Verification Status 判定指南

## 输出格式

### Section Critique

```md
## Section Critique

- Issues fixed:
- Claims weakened or clarified:
- Evidence still missing:
- Risks to carry into next section:
- Missing figure/table/formula placements:
- Missing or inconsistent inline citations:
```

### Verification Status

```md
## Verification Status

- Verdict: passed / failed / blocked
- section_contract_debt: open / closed
- prose_debt: open / closed
- citation_debt: open / closed
- evidence_debt: open / closed
- figure_debt: open / closed
- thin_draft: yes / no
- Checks performed:
- Remaining issues:
- Can move to next section: yes / no
```

若判定为 `blocked`，必须额外包含：

```md
- safe_to_continue: yes / no
- frozen_claims:
  - Claim: ...
    Reason frozen: ...
    Alternative text: ...
    Unfreeze condition: ...
```

---

## 判定规则

### passed

条件：核心章节满足以下所有条件：
- 关键主张有对应证据
- 主要风险已被显式讨论
- 未核验内容被清楚标记
- 结果、表格、摘要相互一致
- 核心章节不再只是骨架式短稿
- 无未闭合的 citation debt、evidence debt、protocol debt、result debt、section_contract_debt、prose debt、rationale debt、figure debt
- 无 thin_draft

### failed

条件：问题可以通过继续修订解决（非外部阻塞）：
- 信息充分但文体仍不适合作为论文正文 → failed（如仍存在明显 prose debt）
- 证据足以继续修订但当前写法仍偏"公式罗列型" → failed
- thin_draft = yes 且可继续扩写 → failed

### blocked

条件：需要外部证据或额外实验才能补齐：
- 缺口来自外部证据缺失，而不是本轮可通过继续改写解决的问题
- 必须依赖额外证据才能把说明文改写为合格正文 → blocked
- thin_draft = yes 且需要外部证据才能消除内容密度缺口 → blocked
- 核心 / 非显然模块缺少足够证据支撑模块级动机 → blocked

---

## safe_to_continue 判断

若判定为 `blocked`，判断是否允许继续其他 section。

**允许继续（safe_to_continue: yes）**的条件（必须同时满足）：
1. 缺口来自外部证据缺失，不是本轮可通过继续改写解决的问题
2. 受影响内容可以冻结为占位或保守表述，不会在后续章节中被扩写成确定性结论
3. 继续写其他 section 不会放大幻觉风险，也不会迫使后文依赖未闭合 claim

**不允许继续（safe_to_continue: no）**的条件：
- 后续章节会依赖未闭合 claim
- 继续写会显著增加幻觉风险

---

## frozen_claims 记录

每个条目至少记录：
- 冻结原因
- 正文中的替代写法
- 解冻条件

---

## debt 类型速查

| debt 类型 | 含义 | 影响 |
|-----------|------|------|
| citation debt | 需要文献支撑的段落缺少 inline citation 或 [REF_NEEDED] | passed 失效 |
| evidence debt | 存在无证据支撑的 claim 或 [RESULT_UNVERIFIED] | passed 失效 |
| figure debt | 存在未替换的 [FIGURE_NEEDED] 或 [TABLE_NEEDED] | 软约束，可 safe_to_continue |
| protocol debt | 实验协议细节不可确认或混入领域默认值 | passed 失效 |
| result debt | 缺实验结果、表格或指标 | passed 失效 |
| section contract debt | 缺少对应 section 的 required moves、reader-state 转换或 evidence hooks | passed 失效 |
| rationale debt | 核心模块缺设计动机/预期收益/边界说明 | passed 失效 |
| prose debt | 正文仍存在元评论、代码讲解、审稿人对话口吻或 checklist 痕迹 | passed 失效 |

citation debt、evidence debt、protocol debt、result debt、section contract debt、rationale debt、prose debt 任一存在 → passed 判定失效 → 至少为 failed 或 blocked。figure_debt 为软约束，可标记但允许 safe_to_continue = yes。
