# Verification Report Schema — 跨技能数据契约

**用途**: 审修技能到论文编排器之间的验证状态交换格式。
**生产者**: `academic-reviser`
**消费者**: `academic-paper-writer` (Step 10)

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
  thin_draft: boolean
  frozen_claims:              # 仅 blocked 时有
    - claim: string
      reason: string
      safe_to_continue: boolean
  remaining_issues: string[]
  iteration_count: integer
  next_action: string         # continue_revision / advance_section / wait_external
```

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
  thin_draft: false
  remaining_issues:
    - "Module B design rationale needs supporting citation"
  iteration_count: 1
  next_action: continue_revision
```
