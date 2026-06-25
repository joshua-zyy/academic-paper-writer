# 标准化 Todo 模板

本文件定义了 `academic-paper-writer` 编排器的标准化任务列表。Agent **必须**在任务开始时使用当前运行环境可用的任务计划工具创建此列表（Codex 使用 `update_plan`；Claude Code 可使用 `TodoWrite`），不得自行规划或跳过子步骤。

模板分两种模式：`full-paper-planning` 和 `section-drafting`。Agent 根据 Step 0 判定的模式选择对应模板。

---

## 模式 A: full-paper-planning（完整论文起草）

```
[ ] Step 0: 判定 mode、scope、当前 section
[ ] Step 1: Blocking Context Confirmation（6 项检查清单，逐一完成）
  [ ] 1.1 确认 venue
  [ ] 1.2 确认 language
  [ ] 1.3 确认 min_citations（可选）
  [ ] 1.4 确认推进模式
  [ ] 1.5 询问本地风格参考文献库
  [ ] 1.6 询问本地文献库
[ ] Step 2: Local PDF→MD Preparation Gate（条件执行；未验证前不得进入 Step 4）
[ ] Step 3: Project Context Extraction（强制，Venue 调研前置）
[ ] Step 4: Venue Requirements Research（强制）
[ ] Step 5: Evidence Audit（并行 dispatch probe agents）
[ ] Step 6: Citation Retrieval and Verification
  [ ] 6a: 本地文献库优先搜索（关键词搜索 _index_ref.json）
  [ ] 6b: 联网文献检索 + 全文获取与阅读
  [ ] 6c: 聚合 + Citation-to-Claim 映射
  [ ] 6d: 生成引用文献清单文件
  [ ] 6e: 当前节引用就绪检查（Gate B）
[ ] Step 7: Experiment Evidence Review
[ ] Step 8: 生成 Section Contract + Blueprint
[ ] Step 9: Section Complete Loop（逐节执行）
  [ ] [当前节名] 9.0 核对 Section Contract
  [ ] [当前节名] 9.1 前置探查（按 section 类型 dispatch）
  [ ] [当前节名] 9.2 Draft v1
  [ ] [当前节名] 9.3 写入 paper_draft.md
  [ ] [当前节名] 9.4 占位符审计 + 图表生成
  [ ] [当前节名] 9.5 证据合规审查
  [ ] [当前节名] 9.6 Prose Quality Gate
  [ ] [当前节名] 9.7 Expansion Pass
  [ ] [当前节名] 9.8 Self-Review & Verification
  [ ] [当前节名] 9.9 更新 Cumulative Draft
  [ ] （每节 9.9 后 → Step 10 依赖检查 + 选择下一节 → 回到 9.0 或推进）
  [ ] [下一节名] 重复 9.0–9.9 …
[ ] Step 10: Section Progression / Cross-section Integration
[ ] Step 11: Final Citation List / Citation Count Gate
[ ] Step 12: Figure Handling / Publication-readiness Debt
```

### 使用说明

1. **Step 1 的 6 项子清单**：必须逐项完成，每项打勾后方可进入下一项。详见 `workflow-step-0-7.md` Step 1 节。
2. **Step 2 是阻塞门控**：用户提供本地 PDF 文献库时，必须等待用户完成 MinerU 转换并提供 MD 目录；索引验证通过前不得进入 Step 4。
3. **Step 9 的 Section Complete Loop**：每个 section 都必须完成 9.0→9.9 全部子步骤。Draft v1（9.2/9.3）只是起草阶段，不是完成标志。**只有完成 9.8 的 section 才算初稿完成。**
4. **Section 动态追加**：当 Section Queue 中有多个 section 时，每完成一个 section 的 9.9，在 Step 9 下新增下一个 section 的 9.0→9.9 子项。
5. **Step 10-12 位置**：
   - **Step 10（跨节一致性检查）**：在每节 9.8 Verification 完成后执行，用于依赖检查、标记回修队列、选择下一节。Step 10 是 section 循环控制器，与 Step 9 交替执行，不应推到所有 section 完成后。
   - **Step 11（引用清单）**：在所有 section 完成 + Abstract 生成后执行。
   - **Step 12（数据图批量生成）**：在所有 section 完成 + Abstract 生成后执行，位于 Step 11 之后。

---

## 模式 B: section-drafting（单节起草）

```
[ ] Step 0: 判定当前 section
[ ] Step 1: Blocking Context Confirmation（简化——确认 venue/language/min_citations/本地文献库，若已确认则跳过）
[ ] Step 2: Local PDF→MD Preparation Gate（条件执行；未验证前不得进入 Step 4）
[ ] Step 3: Project Context Extraction（若 venue-brief.md 不存在则执行）
[ ] Step 4: Venue Requirements Research（若 venue-brief.md 不存在则执行）
[ ] Step 5: Evidence Audit（针对当前 section）
[ ] Step 6: Citation Retrieval and Verification（针对当前 section）
  [ ] 6a: 本地优先
  [ ] 6b: 联网
  [ ] 6c: 聚合
  [ ] 6d: 清单
  [ ] 6e: 当前节引用就绪检查（Gate B）
[ ] Step 7: Experiment Evidence Review（若适用）
[ ] Step 8: 生成 Section Contract + Blueprint
[ ] Step 9: Section Complete Loop
  [ ] 9.0 核对 Section Contract
  [ ] 9.1 前置探查
  [ ] 9.2 Draft v1
  [ ] 9.3 写入 paper_draft.md
  [ ] 9.4 占位符审计 + 图表生成
  [ ] 9.5 证据合规审查
  [ ] 9.6 Prose Quality Gate
  [ ] 9.7 Expansion Pass
  [ ] 9.8 Self-Review & Verification
  [ ] 9.9 更新 Cumulative Draft
[ ] Step 10: 依赖检查（若本 section 为多节论文的一部分）+ Abstract（若适用）
[ ] Step 11: 引用清单（若本 section 已完成为独立单元）
[ ] Step 12: 图表批量生成（若本 section 有待生成图表）
```

> **注意**：`section-drafting` 模式缩小证据范围，但不缩短流程（见 SKILL.md 规则 13）。Step 10-12 在此模式下可能被简化但不可完全跳过。若 Section Queue 只有本节，Step 10 可简化为 Abstract 生成检查（若适用）。

---

## 常见违规行为与纠正

| 违规行为 | 正确做法 |
|---------|---------|
| 跳过 Step 1 的某些 item（如不询问风格参考文献库） | Step 1 清单逐项完成，不得跳过 |
| 过早执行 Step 11/12（在各节之间而非全文完成后） | Step 10 在每节后循环执行；Step 11/12 在所有 section + Abstract 完成后执行 |
| Draft v1 写入后直接跳到下一节 | 必须完成 9.4→9.9 后再推进，参考"Section 完成门控" |
| 自行规划任务列表替代此模板 | 严格按照此模板创建任务计划，可追加具体细节但不可删除条目 |
| 将多个子步骤合并为一个任务项 | 每个 `[ ]` 应为一个独立任务计划条目 |
