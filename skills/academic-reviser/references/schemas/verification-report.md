# Verification Report Schema — 跨技能数据契约

本文件的权威版本维护在 `skills/shared/schemas/verification-report.md`。
如需查看完整结构定义和示例，请读取该文件。

**用途**: 审修技能到论文编排器之间的验证状态交换格式。
**生产者**: `academic-reviser`
**消费者**: `academic-paper-writer` (Step 11)

## 结构

```yaml
verification_report:
  section: string
  verdict: enum               # passed / failed / blocked
  overall_score: integer      # 1-10, 快速质量指示
  checks_run:
    - check_id: string
      check_name: string
      status: enum            # pass / fail / na
      details: string
  prose_debt: enum            # open / closed
  citation_debt: enum         # open / closed
  evidence_debt: enum         # open / closed
  figure_debt: enum           # open / closed
  thin_draft: boolean
  frozen_claims:              # 仅 blocked 时有
    - claim: string
      reason: string
      safe_to_continue: boolean
  remaining_issues: string[]
  iteration_count: integer
  next_action: string         # continue_revision / advance_section / wait_external
```

## 字段说明

| 字段 | 含义 | 判定标准 |
|------|------|---------|
| `overall_score` | 整体质量评分（1-10） | 9-10: 所有 debt 闭合，内容充实; 7-8: 硬 debt 闭合，少量可改进; 5-6: 主要 debt 闭合，中等改进空间; 3-4: 部分 debt 未闭合; 1-2: 多个 debt 未闭合 |
| `prose_debt` | 文体质量缺口 | `academic-polishing` Step 9 输出 |
| `citation_debt` | 引用缺口 | 正文中存在未闭合 `[REF_NEEDED]` 或裸 claim |
| `evidence_debt` | 证据缺口 | 存在无证据支撑的 claim 或 `[RESULT_UNVERIFIED]` |
| `figure_debt` | 图表缺口 | 存在未替换的 `[FIGURE_NEEDED]` 或 `[TABLE_NEEDED]` |
| `thin_draft` | 内容过薄 | Expansion Pass 判定 |

**通过条件**：`verdict = passed` 要求 `prose_debt = closed` 且 `citation_debt = closed` 且 `evidence_debt = closed`。`figure_debt` 和 `thin_draft` 为软约束，可标记但允许 `safe_to_continue = yes`。

## 示例

```yaml
verification_report:
  section: method
  verdict: failed
  checks_run:
    - check_id: C001
      check_name: "evidence_consistency"
      status: pass
      details: "All claims match experiment data"
    - check_id: C002
      check_name: "citation_completeness"
      status: fail
      details: "Missing citation for backbone claim"
  prose_debt: closed
  citation_debt: open
  evidence_debt: closed
  figure_debt: open
  thin_draft: false
  remaining_issues:
    - "Module B design rationale needs supporting citation"
    - "Architecture figure placeholder not yet replaced"
  iteration_count: 1
  next_action: continue_revision
```
