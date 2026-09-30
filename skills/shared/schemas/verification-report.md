# 验收报告契约（source of truth）

生产者：academic-reviser。消费者：主 agent。验收只检查本次 scope 的产物，不评判创新性、录用或实验方法学优劣。

```yaml
verification_report:
  scope: section | manuscript | targeted | recheck
  target: string                 # 章节 ID、全文或问题 ID
  draft_version: string          # 当前文件版本或内容标识
  verdict: passed | needs_revision | needs_author_input
  checks_run:
    - check_id: string
      status: pass | fail | not_checked | na
      details: string
  issues:
    - issue_id: string
      category: prose | logic | consistency | protocol_description | citation | figure
      disposition: fix | author_input | suggestion
      location: string           # 文件+章节/段落/图表定位，不能编造行号
      problem: string
      basis: string              # 具体原文/来源/质量要求
      acceptance_condition: string
      affected_sections: [string]
  checked_sources: [string]
  unchecked_items: [string]
  next_action: revise | advance | ask_author
```

## 判定

- 存在 `fix` → `needs_revision`。主 agent 修复，验收者只复核问题及受影响范围。
- 无 `fix`，但存在 `author_input` → `needs_author_input`。材料缺失或未解决事实冲突不能伪装通过；不受影响部分继续。
- 其余 → `passed`，可保留 `suggestion`。未查项目显式列出，通过只适用于已声明 scope。
- 引用数量低于建议值、纯风格偏好、可选扩展实验不是失败项。
- 协议检查是否交代清楚并与材料一致，不评价实验是否最优或要求额外研究。
- 同一问题连续两轮无实质进展，保留 issue 并交作者决定，不输出新 verdict 枚举、不无限循环。

## 交付状态与验收分离

任务交付使用 `delivery_level: usable_draft | partial_draft | structured_outline`，由主 agent 根据实际内容判断；不是验收 verdict。

`usable_draft` 有实质论证与正文；`partial_draft` 已有正文加局部框架；`structured_outline` 以框架和补充建议为主。任何等级均附未解决项，不表示投稿就绪。接受带缺口交付不改变原问题状态。
