# 文献身份记录契约（source of truth）

生产者 academic-citation。消费者主 agent 与验收者。身份状态不替代引用—主张映射中的支持状态。

```yaml
verified_references:
  items:
    - ref_id: R001
      title: string
      authors: [string]
      year: integer | null
      venue: string | null
      doi: string | null
      arxiv: string | null
      citation_key: string
      identity_status: VERIFIED | UNVERIFIED | CONFLICTING
      checked_fields: [title, authors, year, venue]
      identity_sources: [string]   # 实际打开并比对的原始/权威来源
      notes: string
  exemplar_set: []                # 按任务需要提供，不是每节启动条件
```

身份核验必须说明核对来源与字段；未知不默认 VERIFIED。多源冲突保留，不能以 URL 可访问或 Crossref 无结果单独判真伪。候选文献与正文采用的已确认条目分开，min_citations 仅作建议。
