# Academic Reviser

独立可用的学术论文章节审查与修订技能。执行结构化的三轮自审（证据→论证→风格）并输出 Verification 判定。

## 触发方式

- "帮我 self review 这节 Method"
- "检查这篇草稿的引用是否闭合"
- "verification check on Introduction"
- "审修当前章节"

## 核心能力

| 能力 | 说明 |
|------|------|
| 三轮自审 | 第一轮：证据与事实 → 第二轮：论证强度与审稿风险 → 第三轮：结构与风格 |
| Verification 判定 | passed / failed / blocked，含 prose_debt、thin_draft、safe_to_continue |
| Frozen Claims 管理 | 记录冻结原因、替代写法、解冻条件 |
| 跨章节一致性检查 | 摘要 vs 正文 vs 表格 vs 结论一致 |

## 与其他 Skill 的关系

- 被 `academic-paper-writer` 在 Step 8（自我审查与 Verification）中委托调用
- 可独立使用于任何需要审修和验证的学术段落
