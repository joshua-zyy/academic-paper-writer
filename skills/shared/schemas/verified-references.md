# Verified References Schema — 跨技能数据契约

**本文件为权威版本（source of truth）。**

**用途**: 文献检索技能到论文编排器之间的引用数据交换格式。
**生产者**: `academic-citation`
**消费者**: `academic-paper-writer` (Step 6), `academic-polishing` (Step 6.6)

## 结构

```yaml
verified_references:
  section: string              # 目标章节
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
  exemplar_set:                  # 按目标 section 分类，不限类型
    introduction:                # 当前仅 Introduction / Related Work 时必选
      - ref_id: string
        notes: string            # 该 exemplar 可学习的叙述结构、论证顺序、引用密度
    related_work:
      - ref_id: string
        notes: string
    method:                      # 可选，对 Method 写作有帮助的 exemplar
      - ref_id: string
        notes: string
```

## 示例

```yaml
verified_references:
  section: introduction
  items:
    - ref_id: R001
      title: "Attention Is All You Need"
      authors: "Vaswani et al."
      year: 2017
      venue: "NeurIPS"
      doi: "10.5555/3295222.3295349"
      arxiv: "1706.03762"
      verification_method: primary_source
      verification_status: VERIFIED
      citation_key: "vaswani2017attention"
      claim_mapping: "Transformer architecture as baseline reference"
  exemplar_set:
    introduction:
      - ref_id: R002
        notes: "Opens with task importance -> identifies limitations of prior work -> proposes solution"
```
