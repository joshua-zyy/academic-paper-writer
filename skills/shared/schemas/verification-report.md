# Verification Report Schema — 跨技能数据契约

**用途**: 审修技能到论文编排器之间的验证状态交换格式。
**生产者**: `academic-reviser`
**消费者**: `academic-paper-writer` (Step 11)

## 结构

```yaml
verification_report:
  section: string
  verdict: enum               # passed / failed / blocked
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

## debt 字段说明

| 字段 | 含义 | 硬/软约束 |
|------|------|----------|
| `prose_debt` | 文体质量缺口 | 硬——未闭合时 passed 失效 |
| `citation_debt` | 引用缺口 | 硬——未闭合时 passed 失效 |
| `evidence_debt` | 证据缺口 | 硬——未闭合时 passed 失效 |
| `figure_debt` | 图表缺口 | 软——可标记但允许 safe_to_continue |
| `thin_draft` | 内容过薄 | 软——可标记但允许 safe_to_continue |

**通过条件**：`verdict = passed` 要求 `prose_debt = closed` 且 `citation_debt = closed` 且 `evidence_debt = closed`。
