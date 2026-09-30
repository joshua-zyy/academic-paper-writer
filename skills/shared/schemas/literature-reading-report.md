# 文献阅读报告契约

reader 返回、citation/主笔使用。实际阅读范围不是身份核验或科学认证。

```yaml
literature_reading_report:
  ref_id: R001
  title: string
  source_of_content: full_text | abstract_only | metadata_only
  sections_read: [string]
  unread_items: [string]
  image_reading: performed | skipped | not_applicable
  image_reading_notes: string
  findings:
    - claim: string
      source: text | image | inference
      source_locator: string | null
      source_excerpt: string | null
      conditions: string
  conflicts: [string]
  recommendation: cite | consider | skip
  recommendation_rationale: string
```

text/image 条目必须可定位；摘录逐字准确，数字只取清晰文本或图中标注。inference 不算原文证据；metadata_only 不产出内容支持。多篇各自 ref_id，不混合来源。最终支持状态由 citation-to-claim-map 显式记录，主笔决定采用。
