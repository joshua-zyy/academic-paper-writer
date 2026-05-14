# Evidence Inventory Schema — 跨技能数据契约

**用途**: 论文编排器、实验复核、审修技能之间的证据盘点数据交换格式。
**生产者**: `academic-experiments`, `academic-paper-writer` (Step 2)
**消费者**: `academic-paper-writer` (Step 6), `academic-reviser` (Step 8/11)

## 结构

```yaml
evidence_inventory:
  section: string
  paper_type: string           # empirical / theory / survey / reproducibility / position
  items:
    - evidence_id: string      # 如 E001
      type: enum               # newly_run / preexisting_artifact / user_claim
      source_path: string      # 来源路径（文件、代码位置、或人）
      claim_summary: string    # 该证据支撑的核心主张（一句话）
      verification_status: enum # verified / unverified / blocked
      verified_at: string|null # 验证时间或版本号
      used_in_draft: boolean   # 是否已写入当前草稿
      risks: string[]          # 潜在风险列表
  known_facts: string[]
  missing_blocking: string[]
  missing_placeholder: string[]
  needs_external_validation: string[]
```
