# 证据记录契约（source of truth）

探查者返回、主 agent 维护，验收者可回查。来源与核验含义遵循 `../core/evidence-policy.md`。

```yaml
evidence_inventory:
  items:
    - evidence_id: E001
      type: newly_run | preexisting_artifact | author_provided | user_claim
      content_kind: method | protocol | result | rationale | hypothesis | literature
      source_locator: string       # 文件+位置，或作者提供的消息/附件
      fact: string
      verification_status: verified | unverified | conflicting | unavailable
      verified_against: string | null
      conditions: string           # 数据集、划分、单位、实际运行配置等
      relevant_sections: [string]
  conflicts:
    - description: string
      source_locators: [string]
      author_decision_needed: boolean
  missing:
    - item: string
      affected_sections: [string]
      suggested_material: string
      writing_use: string
  execution_records: []             # 仅经授权执行时填命令、授权范围、产物
```

不得返回论文段落。结果数字与单位、分母、汇总方式和划分一起记录；不知道的字段标明未确认，不按领域惯例填补。没有代码仓库时也可盘点作者表格、笔记与草稿，不强制请求 repo_path。
