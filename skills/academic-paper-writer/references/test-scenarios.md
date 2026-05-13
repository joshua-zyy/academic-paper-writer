# Skill Regression Scenarios

用于在修改 `academic-paper-writer` 后，按文档版 TDD 方式回归验证关键执行路径。每个场景都应检查：

1. 是否在正确位置执行 Step 7 占位符审计、Step 8 证据合规审查、Step 9 Prose Quality Gate、Step 10 Expansion Pass、Step 11 Verification
2. 是否输出 `evidence_debt`、`prose_debt`、`failed_items`、`thin_draft`
3. `Verification Status` 是否与预期一致
4. `Paper Body` 是否满足正面约束，而不是只形式合规

---

## 场景 1：完整论文起草，但文献不足

- 模拟 prompt：
  - “根据这个仓库和现有实验日志，先开始写一篇完整 CS/AI 论文初稿。”
- 重点检查：
  - 是否先形成 `Outline / Section Queue`
  - 写 `Introduction` 或 `Related Work` 时是否显式保留 `[REF_NEEDED: ...]`
  - Step 8 是否将文献缺口标记为 `evidence_debt: open`
  - 若正文仍像提纲，Step 9 是否判 `prose_debt: open`
- 期望：
  - Step 8: 对早期章节通常应先保留 `evidence_debt: open`
  - Step 10: 视内容密度决定 `thin_draft`
  - Step 11: 若文献缺口未闭合，不能轻易判 `passed`

## 场景 2：Introduction 容易写成背景罗列

- 模拟 prompt：
  - “先写这篇论文的 Introduction，要求能直接进入初稿。”
- 重点检查：
  - 是否只罗列背景事实和贡献点
  - 是否形成“背景 -> 难点 -> 缺口 -> 定位 -> 贡献”的连续叙事
- 期望：
  - 若只有背景堆叠和贡献列表，Step 9 判 `prose_debt: open`
  - `failed_items` 包含缺少论证链
  - 完成 Prose Rewrite 后再进入 Step 10 和 Step 11

## 场景 3：Related Work 变成论文名清单

- 模拟 prompt：
  - “补一节 Related Work，先不用太长。”
- 重点检查：
  - 是否只有文献名或方法名罗列
  - 是否形成 `work clusters`、综合比较与与本文关系
- 期望：
  - 罗列式草稿应在 Step 9 被拦下
  - 若结构上仍过薄，Step 10 还应给出 `thin_draft: yes`

## 场景 4：Method 可读，但设计动机只能部分恢复

- 模拟 prompt：
  - “根据代码把 Method section 写出来，不要省略细节。”
- 重点检查：
  - Step 7 是否为核心模块补齐 `[FIGURE_NEEDED]` 占位符
  - Step 9 是否先检查通用 prose 问题，再执行 Method 专项叙事检查
  - 无法稳妥恢复的动机是否进入 `[RATIONALE_NEEDED: ...]` 或 sidecar
- 期望：
  - 若存在公式罗列或“从实现看”口吻，Step 9 不能放行
  - 若两轮 Step 9 Prose Rewrite 后仍有通用 prose 问题，Step 11 最终不得 `passed`

## 场景 5：Results 有日志，但无可复跑环境

- 模拟 prompt：
  - “根据这些结果表和日志，补一节 Main Results。”
- 重点检查：
  - 是否区分 `preexisting_artifact` 与无法复跑的限制
  - 是否把内部验证包装成强泛化结论
- 期望：
  - Step 8 关注结果节是否缺协议或风险说明
  - Step 9 关注 prose 形式与 claim 强度
  - 若核心结果可写但关键协议缺口需要外部证据，Step 11 可判 `blocked`

## 场景 6：blocked 但需要判断能否继续

- 模拟 prompt：
  - “实验还没补全，但先把能写的章节都写出来。”
- 重点检查：
  - `Verification Status` 是否包含 `safe_to_continue`
  - `frozen_claims` 是否记录冻结原因、替代写法、解冻条件
- 期望：
  - 只有满足 safe-continue 条件时才允许前进
  - 若后续章节会依赖未闭合 claim，则必须 `safe_to_continue: no`

## 场景 7：边界场景，Rewrite 一轮后仍有轻微元评论

- 模拟 prompt：
  - “把这段 Method 改成论文正文口吻，但不要改动技术含义。”
- 重点检查：
  - 第一轮 Prose Rewrite 后是否重新执行 Step 9
  - 第二轮后是否允许进入 Step 10
- 期望：
  - Step 9 + Prose Rewrite 循环最多 `2` 轮
  - 第二轮后即使允许继续，若 `prose_debt` 仍 open，Step 11 也必须判 `failed`
