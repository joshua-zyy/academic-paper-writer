# Evidence Inventory Schema — 跨技能数据契约

**本文件为权威版本（source of truth）。**

**用途**: 实验技能到论文编排器之间的实验证据数据交换格式。
**生产者**: `academic-experiments`, `academic-paper-writer` (Step 2)
**消费者**: `academic-paper-writer` (Step 6), `academic-reviser` (Step 6.5/6.8)

## 结构

```yaml
evidence_inventory:
  section: string              # 所属章节
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
  known_facts: string[]        # 已知事实
  missing_blocking: string[]   # 缺失但阻塞当前 section 的事实
  missing_placeholder: string[] # 缺失但可占位的事实
  needs_external_validation: string[] # 需要外部核验的主张
```

## 示例

```yaml
evidence_inventory:
  section: method
  paper_type: empirical
  items:
    - evidence_id: E001
      type: newly_run
      source_path: "experiments/run_logs/exp001.log"
      claim_summary: "Proposed module achieves 92.3% accuracy on CIFAR-10"
      verification_status: verified
      verified_at: "2026-05-10"
      used_in_draft: true
      risks: []
  known_facts:
    - "Model uses ResNet-50 backbone"
    - "Trained for 200 epochs with cosine annealing"
  missing_placeholder:
    - "Ablation study results on module size"
```
