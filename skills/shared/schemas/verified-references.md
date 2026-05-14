# Verified References Schema — 跨技能数据契约

**用途**: 文献检索技能到论文编排器之间的引用数据交换格式。
**生产者**: `academic-citation`
**消费者**: `academic-paper-writer` (Step 6), `academic-polishing` (Step 9)

## 结构

```yaml
verified_references:
  section: string
  items:
    - ref_id: string           # 如 R001
      title: string
      authors: string
      year: integer
      venue: string            # 会议/期刊全称
      doi: string|null
      arxiv: string|null
      verification_method: enum # primary_source / cross_check / web_fetch
      verification_status: enum # VERIFIED / UNVERIFIED
      citation_key: string     # 正文引用 key
      claim_mapping: string    # 该引用支撑的主张描述
  exemplar_set:
    introduction:
      - ref_id: string
        notes: string
    related_work:
      - ref_id: string
        notes: string
    method:
      - ref_id: string
        notes: string
```
