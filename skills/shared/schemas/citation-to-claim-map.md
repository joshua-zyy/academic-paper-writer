# Citation-to-Claim Map Schema — 跨技能数据契约

**本文件为权威版本（source of truth）。**

**用途**: 文献检索技能到论文编排器之间的引用-主张映射数据交换格式。
**生产者**: `academic-citation`
**消费者**: `academic-paper-writer` (Step 6), `academic-reviser` (Step 6.5)

## 结构

```yaml
citation_to_claim_map:
  section: string
  items:
    - claim: string
      ref_id: string
      purpose: enum  # background / method_comparison / baseline / dataset_source / gap_motivation / evidence_support
      inline_marker: string  # 如 [1], [2-4], [1,3,5]
```

## 示例

```yaml
citation_to_claim_map:
  section: introduction
  items:
    - claim: "Graph neural networks have shown strong performance on molecular property prediction"
      ref_id: R003
      purpose: background
      inline_marker: "[3]"
    - claim: "Existing methods struggle with long-range dependencies"
      ref_id: R005
      purpose: gap_motivation
      inline_marker: "[5]"
```
