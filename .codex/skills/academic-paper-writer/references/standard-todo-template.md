# 标准化 Todo 模板

本文件定义了 `academic-paper-writer` 编排器的标准化 Todo 列表。Agent **必须**在任务开始时使用 TodoWrite 工具创建此列表，不得自行规划或跳过子步骤。

模板分两种模式：`full-paper-planning` 和 `section-drafting`。Agent 根据 Step 0 判定的模式选择对应模板。

---

## 模式 A: full-paper-planning（完整论文起草）

```
[ ] Step 0: 判定 mode、scope、当前 section
[ ] Step 1: Blocking Gate（9 项检查清单，逐一完成）
  [ ] 1.1 确认 venue
  [ ] 1.2 确认 language
  [ ] 1.3 确认 min_citations（可选）
  [ ] 1.4 确认推进模式
  [ ] 1.5 询问本地风格参考文献库
  [ ] 1.6 询问本地文献库
  [ ] 1.7 本地文献库处理（若适用）
  [ ] 1.8 进入 Step 1.5（Venue Requirements Research）
  [ ] 1.9 全部完成确认
[ ] Step 1.5: Venue Requirements Research（强制）
[ ] Step 1b: PDF→MD 转换准备（条件执行，提示用户运行后立即进入 Step 2）
[ ] Step 2: 证据审计（并行 dispatch probe agents）
[ ] Step 3: 文献检索与核验
  [ ] 3a: 本地文献库优先搜索（关键词搜索 _index_ref.json）
  [ ] 3b: 联网文献检索 + 全文获取与阅读
  [ ] 3c: 聚合 + Citation-to-Claim 映射
  [ ] 3d: 生成引用文献清单文件
[ ] Step 4: 实验事实复核
[ ] Step 5: 生成 Section Contract + Blueprint
[ ] Step 6: Section Complete Loop（逐节执行）
  [ ] [当前节名] 6.0 核对 Section Contract
  [ ] [当前节名] 6.1 前置探查（按 section 类型 dispatch）
  [ ] [当前节名] 6.2 Draft v1
  [ ] [当前节名] 6.3 写入 paper_draft.md
  [ ] [当前节名] 6.4 占位符审计 + 图表生成
  [ ] [当前节名] 6.5 证据合规审查
  [ ] [当前节名] 6.6 Prose Quality Gate
  [ ] [当前节名] 6.7 Expansion Pass
  [ ] [当前节名] 6.8 Self-Review & Verification
  [ ] [当前节名] 6.9 更新 Cumulative Draft
  [ ] （每节 6.9 后 → Step 7 依赖检查 + 选择下一节 → 回到 6.0 或推进）
  [ ] [下一节名] 重复 6.0–6.9 …
[ ] Step 7: 整合 & Abstract 生成（所有 section + Verification 完成后）
[ ] Step 8: 引用清单生成（强制，全文完成后）
[ ] Step 9: 数据图批量生成（强制，全文完成后）
```

### 使用说明

1. **Step 1 的 9 项子清单**：必须逐项完成，每项打勾后方可进入下一项。详见 `workflow-step-0-4.md` Step 1 节。
2. **Step 6 的 Section Complete Loop**：每个 section 都必须完成 6.0→6.9 全部子步骤。Draft v1（6.2/6.3）只是起草阶段，不是完成标志。**只有完成 6.8 的 section 才算初稿完成。**
3. **Section 动态追加**：当 Section Queue 中有多个 section 时，每完成一个 section 的 6.9，在 Step 6 下新增下一个 section 的 6.0→6.9 子项。
4. **Step 7-9 位置**：
   - **Step 7（跨节一致性检查）**：在每节 6.8 Verification 完成后执行，用于依赖检查、标记回修队列、选择下一节。Step 7 是 section 循环控制器，与 Step 6 交替执行，不应推到所有 section 完成后。
   - **Step 8（引用清单）**：在所有 section 完成 + Abstract 生成后执行。
   - **Step 9（数据图批量生成）**：在所有 section 完成 + Abstract 生成后执行，位于 Step 8 之后。

---

## 模式 B: section-drafting（单节起草）

```
[ ] Step 0: 判定当前 section
[ ] Step 1: Blocking Gate（简化——仅确认 venue/language/min_citations，若已确认则跳过）
[ ] Step 1.5: Venue Requirements Research（若 venue-brief.md 不存在则执行）
[ ] Step 2: 证据审计（针对当前 section）
[ ] Step 3: 文献检索（针对当前 section）
  [ ] 3a: 本地优先
  [ ] 3b: 联网
  [ ] 3c: 聚合
  [ ] 3d: 清单
[ ] Step 4: 实验复核（若适用）
[ ] Step 5: 生成 Section Contract + Blueprint
[ ] Step 6: Section Complete Loop
  [ ] 6.0 核对 Section Contract
  [ ] 6.1 前置探查
  [ ] 6.2 Draft v1
  [ ] 6.3 写入 paper_draft.md
  [ ] 6.4 占位符审计 + 图表生成
  [ ] 6.5 证据合规审查
  [ ] 6.6 Prose Quality Gate
  [ ] 6.7 Expansion Pass
  [ ] 6.8 Self-Review & Verification
  [ ] 6.9 更新 Cumulative Draft
[ ] Step 7: 依赖检查（若本 section 为多节论文的一部分）+ Abstract（若适用）
[ ] Step 8: 引用清单（若本 section 已完成为独立单元）
[ ] Step 9: 图表批量生成（若本 section 有待生成图表）
```

> **注意**：`section-drafting` 模式缩小证据范围，但不缩短流程（见 SKILL.md 规则 13）。Step 7-9 在此模式下可能被简化但不可完全跳过。若 Section Queue 只有本节，Step 7 可简化为 Abstract 生成检查（若适用）。

---

## 常见违规行为与纠正

| 违规行为 | 正确做法 |
|---------|---------|
| 跳过 Step 1 的某些 item（如不询问风格参考文献库） | 9 项清单逐项完成，不得跳过 |
| 过早执行 Step 8/9（在各节之间而非全文完成后） | Step 7（7a-7c）在每节后循环执行；Step 8/9 在所有 section + Abstract 完成后执行 |
| Draft v1 写入后直接跳到下一节 | 必须完成 6.4→6.9 后再推进，参考"Section 完成门控" |
| 自行规划 todo 替代此模板 | 严格按照此模板创建 TodoWrite，可追加具体细节但不可删除条目 |
| 将多个子步骤合并为一个 todo 项 | 每个 `[ ]` 应为一个独立的 TodoWrite 条目 |
