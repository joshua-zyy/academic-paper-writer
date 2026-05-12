---
name: "academic-reviser"
description: "Use when self-reviewing, auditing, or verifying academic paper drafts — structured critique, verification gate, revision loop. Triggers on: 审修, self review, 自查, verification, revise, 修订, check draft."
---

# Academic Reviser

将此 skill 视为"挑剔审稿人代理"——像 peer reviewer 一样审查自己的草稿，按证据→论证→风格三轮顺序执行检查，并输出可执行的修订与 Verification 判定。

## 非协商规则

- 先检查事实与证据，再检查论证强度，最后检查结构与风格。不可跳过顺序。
- 修订必须真正吸收 Self-Review 中发现的修改点，而不是只输出批评说明后沿用原稿。
- 代码与方法一致性、实验与表格一致性必须检查。
- 核心章节存在未闭合的 citation debt、protocol debt 或 result debt 时，Verification 不得判为 passed。
- 存在 prose debt 或 thin_draft 时，Verification 不得判为 passed。
- 只有满足终止条件时才能标记为 passed；否则输出"当前最佳版本 + 未闭合问题清单"。

## 任务模式

1. **full-section-review** — 对单个 section 执行完整三轮审查 + Verification
2. **cross-section-review** — 跨章节一致性检查（摘要 vs 正文 vs 表格 vs 结论）
3. **verification-only** — 仅执行 Verification 判定（不重做自审）
4. **targeted-review** — 针对特定问题做定向审查（如仅检查引用闭合）

## 工作流

### Step 1: 接收当前草稿与前序状态

确认输入：
- 当前 section 的 Draft（经过 Expansion Pass 之后的版本）
- 前序步骤的状态：`prose_debt`、`thin_draft`、`Evidence Map`
- 若来自 core 的委托，还应收到 `safe_to_continue` 和 `frozen_claims`（若适用）

### Step 2: 第一轮 — 证据与事实检查

详见 `references/revision-checklist.md`，逐项检查：

1. 每个关键背景事实是否有 VERIFIED 引用
2. 每个定量结果是否能追溯到本地证据
3. 方法描述是否与代码或用户提供机制一致
4. 表格、正文、摘要中的数字是否一致
5. 是否把内部验证说成外部泛化
6. 是否遗漏关键 baseline 或反例
7. 若为 Method：是否写清整体架构、模块边界、输入输出和关键公式
8. 若为 Method：是否给出图表放置位置或显式图占位
9. 需要文献支撑的段落是否有 inline citation 或 [REF_NEEDED: ...]
10. 参考文献列表中的条目是否都在正文中被实际引用
11. 若为 Introduction / Related Work：是否先做过同领域 exemplar 调研
12. 若为 Experimental Setup / Data：是否把领域常见默认协议误写成已确认事实
13. 若为 Discussion / 解释性段落：是否清楚区分"观察结果"和"领域解释"

若任一项失败，先修事实，再谈语言。

### Step 3: 第二轮 — 论证强度与审稿风险检查

从怀疑者视角提问（详见 `references/revision-checklist.md`）：

- Reviewer 最可能攻击哪一条证据链？
- 哪些地方的表述比证据更强？
- 哪些局限性被藏起来了？
- 哪些实验设计会被认为偏乐观？
- 哪些 related work 被遗漏后会显得"选择性比较"？
- 方法节是否只在复述直觉，而没有给出足够具体的结构、公式和实现细节？
- 引言是否过早进入"我们提出了什么"而没有建立领域背景与缺口？
- 相关工作是否只有论文名排队而无 work clusters 和综合比较？
- 讨论中的领域解释是否有已核验文献支撑？

对这些问题，要么补证据，要么弱化表述，要么把风险显式写出。

### Step 4: 第三轮 — 结构与风格检查

只有在前两轮基本通过后，才重点检查（详见 `references/revision-checklist.md`）：

- 段落衔接是否清晰
- 章节顺序是否合理
- 术语是否前后一致
- 图表引用是否完整
- 是否符合目标 venue 的结构和语气
- 正文引用样式是否统一
- 正文中是否残留 AI 典型机械痕迹
- 句子之间是否只靠连接词维持表面连贯

### Step 5: 生成 Revised Draft

- Revised Draft 必须真正吸收 Self-Review 中发现的修改点
- 不是"重新生成一遍"，而是针对性修正后再输出
- 保持 evidence-first 原则：不确定的修正用占位符，不臆造

### Step 6: 输出 Section Critique 与 Verification Status

详见 `references/verification-status.md`。

**Section Critique** 明确：
- 本节已解决的问题
- 本节仍缺的证据
- 本节是否仍存在 formula-heavy / rationale-thin / prose debt 问题
- 下一节最合理的候选

**Verification Status** 明确：
- 判定：`passed` / `failed` / `blocked`
- `prose_debt`: open / closed
- `thin_draft`: yes / no
- 本轮实际做了哪些检查
- 仍未闭合的问题属于可继续自修，还是外部阻塞
- 若 blocked：`safe_to_continue: yes|no` 和 `frozen_claims`

## 常见自欺模式

避免以下行为（详见 `references/common-pitfalls.md`）：
- 只修措辞，不修证据
- 把占位符删掉，却没有补真实内容
- 因为草稿已经很长，就假设它足够可信
- 看到一个高指标，就忽略协议缺陷
- 用更华丽的写法掩盖 related work 不充分

## 终止条件

只有以下条件基本满足时，才把稿子当作当前版本定稿（passed）：
- 关键主张有对应证据
- 主要风险已被显式讨论
- 未核验内容被清楚标记
- 结果、表格、摘要相互一致
- style brief 与正文不冲突
- 核心章节不再只是骨架式短稿
- 无未闭合的 citation debt、protocol debt、result debt、prose debt

否则，输出"当前最佳版本 + 未闭合问题清单"，不假装已经完成。
