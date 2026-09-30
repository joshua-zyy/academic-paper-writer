# 引用—主张映射契约（source of truth）

文献身份已确认不等于原文支持主张。academic-citation 返回，主 agent 使用，验收者回查。

```yaml
citation_to_claim_map:
  items:
    - claim_id: C001
      claim: string
      ref_id: R001
      purpose: background | method_comparison | baseline | dataset_source | gap_motivation | evidence_support | interpretation
      source_locator: string        # URL/PDF页/MD章节/图表
      source_excerpt: string        # 必要的原文片段，不编造引语
      support_status: supported | partial | contradicted | not_checked
      boundary: string              # 原文实际范围
      relevant_sections: [string]
      inline_marker: string         # [1]、[1,3]、[2-4] 或指定 author-year
```

`partial` 只支持匹配其范围的改写；`contradicted` 不得作为该主张支持；`not_checked` 不得声称引用内容已核验。仅摘要可读时记录摘要定位，不声称全文阅读。
