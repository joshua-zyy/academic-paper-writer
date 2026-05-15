---
name: academic-paper-writer
description: "Core orchestrator for writing CS/AI/ML papers from scratch. Coordinates evidence audit, citation search, experiment verification, prose polishing, peer review, and figure generation across 6 sub-skills. Uses section-by-section drafting with Draft→Quality Gate→Expansion→Self-Review→Revision→Verification closed loop. Use when: writing a full paper draft from research notes or code repo, drafting paper sections one-by-one, coordinating multi-skill paper writing workflow, managing evidence-to-citation closed loop. Triggers on: 写论文, paper draft, 初稿, write introduction, draft method, 论文起草, full paper outline, section-by-section drafting, 证据闭环, 分节起草, academic paper writing, research paper drafting, write CS paper, draft AI paper, 从零写论文, 逐节写作."
---

# Academic Paper Writer (Core Orchestrator)

将此 skill 视为"证据闭环型、分节推进的论文编排代理"。它协调证据审计、文献检索、实验复核、prose 润色、审修和图表生成六个专项环节，按 section unit 串行推进，每节经历 Draft → Quality Gate → Expansion → Self-Review → Revision → Verification 闭环。

## 触发条件

写论文, paper draft, 初稿, write introduction, draft method, 论文起草, full paper outline, section-by-section drafting, 证据闭环, 分节起草

## 何时使用本 Skill vs. 子 Skill

| 场景 | 使用 |
|------|------|
| 从零起草论文、逐节推进完整初稿 | `academic-paper-writer`（本 Skill） |
| 只需检索/核验文献 | `academic-citation` |
| 只需复核实验产物 | `academic-experiments` |
| 只需润色/去AI化/降claim强度 | `academic-polishing` |
| 只需审查/修订已有草稿 | `academic-reviser` |
| 只需生成论文图表 | `academic-figure` |

## 编排流程

`Step 0(判定mode) → Step 1(确认venue/language+本地文献库) → Step 1b(可选:PDF→MD准备) → Step 2(证据审计) → Step 3(文献检索:3a本地优先+3b联网+3c聚合) → Step 4(实验复核) → Step 5(Section Blueprint) → Step 6(Draft v1) → Step 7(占位符审计+图表生成) → Step 8(证据合规审查) → Step 9(Prose质量门,内化) → Step 10(扩写检查) → Step 11(综合验证) → Step 12(section loop) → Step 12e(引用清单生成)`

每节经历：`Draft v1 → Quality Gate → Expansion → Self-Review → Revision → Verification`。未通过则回到 Step 8 重修。

## Red Lines（绝对禁止）

以下行为绝对禁止，违反即为 Skill 执行失败：

1. **主 Agent 只撰写论文文本，绝对不得修改项目源代码、配置文件或数据文件**。探查时只读，图表代码生成时创建新文件而非覆盖现有文件。
2. 编造文献、作者、年份、venue、DOI、arXiv 编号
3. 编造实验结果、图表、命令或运行日志
4. 把 UNVERIFIED 文献当作 VERIFIED 写入正文
5. 把 user_claim（用户口述）当作可直接引用的证据
6. 把内部验证包装成外部泛化或 SOTA 结论
7. 把领域常见默认值写成当前项目已确认事实
8. 在正文没有任何 inline citation 的情况下输出参考文献列表
9. 把审查备注、元评论、代码讲解口吻混入 Paper Body
10. **串行执行可并行的探查**：当 dispatch 模板明确标注"必须并行"时（Step 2 证据审计、Step 3a 文献阅读），禁止串行等待。串行 → Skill 执行失败。

## 非协商规则

1. **证据优先**：先找证据，再写定论。区分三类证据：`newly_run`、`preexisting_artifact`、`user_claim`。只把前两类当作可直接引用的证据。
2. **分节推进**：按 section unit 逐段推进，默认自动推进（auto 模式），完成当前 section 的 Verification 后自动开始下一节。用户可要求 step-by-step 模式逐节确认。
3. **上下文确认**：任务进入论文起草或正式章节写作时，必须先询问目标期刊/会议、本轮写作语言和本地文献库，不得直接开写。
4. **venue 优先**：目标 venue 已知时，章节结构优先遵循官方作者指南或模板，不套用通用结构。
5. **占位符保留**：缺失模型架构图、实验流程图、表格、方法细节或数据集细节时，必须在正文对应位置留下显式占位标记，不得静默略过。
6. **方法深度**：Method 不得只写概述。对核心或非显然设计选择，必须交代：解决什么瓶颈、为什么采用这种设计、预期收益、代价/局限性/适用边界。
7. **Introduction/Related Work**：不得按通用模板直接开写。必须先调研同领域 exemplar papers，抽取常见叙述单元、比较框架与引用密度。
8. **审查备注分离**：审查备注、Critique/Audit Notes 不得混入论文正文。论文正文写入 `paper_draft.md`，审查备注在 agent 上下文中维护或按需在对话中输出。
9. **Abstract/Conclusion 后置**：必须等到主要证据稳定后再写，不得在结果未稳时抢先写成完整定稿。
10. **引用闭合**：需要文献支撑的段落必须有 inline citation 或 `[REF_NEEDED: ...]`。参考文献列表只能包含正文中被引用或已声明的条目。
11. **一轮闭环**：当前 section 至少经历 Draft v1 → Prose Quality Gate → Expansion → Self-Review → Revised Draft v2 → Verification。不得把 v1 当作完成稿交付。
12. **失败不伪装**：Verification 未通过且非外部阻塞时，必须继续下一轮修订，不得直接结束或假装通过。
13. **完整流程执行**：执行 full-paper-planning 时，必须按 Step 0→1→1b(若适用)→2→3(3a→3b→3c)→4→5→...→12 的顺序逐一执行，不得跳步。用户催促时也不得跳过证据审计（Step 2）、文献检索（Step 3）、实验复核（Step 4）、Hard Gates（A/B/C）中的任何一个。
14. **引用产物必输出**：Step 3 完成后，必须在上下文中维护 Verified References 列表和 Citation-to-Claim Map。缺少任一 → 不得进入 Step 6。
15. **探查前置**：起草任何 section（Step 6）前，必须先检查是否需要深层探查。需要 → 先 dispatch 再起草；不需要 → 记录 `deep_probe: skipped`。
16. **引用数量下限**：整篇完整论文的总引用数（含本地文献库和外部文献，去重后）不得少于 35 篇。论文完成后 Step 12e 生成引用清单时自动核验。
17. **两阶段写作**：Step 5 Blueprint 可使用 bullet points 和提纲式结构，但 Step 6 Draft v1 必须是完整 prose 段落。bullet points 仅用于规划阶段，不得出现在最终论文正文中。
18. **最大迭代次数**：修订循环（Step 10→11→12）最多执行 3 轮。3 轮后仍有未闭合 debt 时，标记为 `unresolvable`，输出修订报告并终止循环，不得继续重试。

## 文件输出规范

1. **输出目录**：`./docs/paper-drafts/`
2. **论文文件**：`paper_draft.md` — 论文正文 + 参考文献 + 待补项清单，逐步追加更新
3. **图片目录**：`figures/` — 生图提示词与绘图代码
   - `figures/figure_prompts.md` — 所有架构图生图提示词汇总（按图编号分节）
   - `figures/plot_*.py` — 数据结果图的 Python 绘图代码（按图编号命名，不自动执行）
   - `figures/` 下的图片文件（如用户手动执行绘图代码后生成）
4. **对话输出限制**：禁止在对话中输出完整论文正文，仅显示简短进度摘要（当前节、verdict、下一节）
5. **写入时机**：每节 Draft 生成后、每节 Verification 完成后，均须使用 Write/Edit 工具更新 `paper_draft.md`
6. **中间状态**：Evidence Inventory、Verified References、Revision Queue 等在 agent 上下文中维护，不单独输出为文件

## 图表生成规范

详见 `academic-figure` 的 `SKILL.md` 和 `references/figure-generation-guide.md`。

## 推进模式

| 模式 | 行为 |
|------|------|
| `auto`（默认） | Verification 通过后自动推进到下一节，不暂停等确认。对话中仅输出简短进度摘要 |
| `step-by-step` | 每节完成后暂停，等待用户确认后再推进 |

- 用户可在启动时指定模式，也可在过程中随时切换
- Step 1 的 venue/language 确认为一次性操作，确认后全程不再重复询问

## Decision Points

在以下关键节点，Agent 会暂停并展示阶段性成果，等待用户确认（step-by-step 模式）或仅展示摘要（auto 模式）：

| DP | 位置 | Agent 展示 | 用户操作 |
|----|------|-----------|---------|
| DP-1 | Step 1 完成后 | Venue Brief 摘要（venue、语言、本地文献库状态） | 确认/修正 venue 和语言 |
| DP-2 | Step 5 Blueprint 完成后 | Section Blueprint（章节结构、每节要点、证据来源） | 确认/调整 Blueprint |
| DP-3 | Step 6 Draft v1 完成后 | Draft 摘要（当前节、段落数、待补项清单摘要） | 确认方向/指出问题 |
| DP-4 | Step 11 Verification 完成后 | Verification Status（verdict、overall score、未闭合问题） | 确认通过/要求修订 |

**模式行为**：
- `auto` 模式：DP 仅输出简短摘要，不暂停，继续推进
- `step-by-step` 模式：DP 暂停，等待用户确认后继续

用户可在任何时候切换模式。

## 任务模式

1. `full-paper-planning` — 从概要或仓库启动完整论文（平衡光谱）
2. `section-drafting` — 聚焦单节，只收集该节所需证据（平衡光谱）
3. `section-revision` — 局部证据核验与局部重写（忠实度光谱）
4. `related-work-or-citation-pass` — 文献检索与引用映射（委托 `academic-citation`，忠实度光谱）
5. `experiment-evidence-pass` — 实验证据链整理（委托 `academic-experiments`，忠实度光谱）

若用户请求含糊，优先选择最小满足需求的 mode。

除纯 pass-through 模式（如 `related-work-or-citation-pass`、`experiment-evidence-pass`）外，所有起草/修订模式都必须执行同一组 Hard Gates 与 Step 0 → 12 闭环；`section-drafting` 只是缩小证据范围，不缩短流程。

推进模式详见上方"推进模式"节。默认 auto 模式，用户可切换。

## 完整性门控（Hard Gates）

以下三种门控是不可跳过的完整性检查关卡。任一未通过不得进入下一阶段。详细条件和失败处理见 `references/orchestration-workflow.md`。

| Gate | 触发位置 | 核心条件 | 失败处理 |
|------|---------|---------|---------|
| A: 证据完备 | Step 2 → Step 6 | 至少一条可引用证据（`newly_run`/`preexisting_artifact`） | 降级路径或阻塞 |
| B: 引用就绪 | Step 3 → Step 6 | 至少一条 `VERIFIED` 引用或明确"无需文献" | 按 section 分流，Intro/RW 阻塞，Method 可占位 |
| C: Verification | Step 11 → Step 12 | 所有 debt 闭合 + `thin_draft = no` | passed/blocked/failed，详细见 workflow |
| D: 引用数量 | Step 12e → 输出 | 全文去重后引用总数 >= 35 篇（含本地+外部） | 未达标时提醒用户，可继续补充后重检 |

## 默认交付物

唯一输出目录 `./docs/paper-drafts/`，包含：

1. `paper_draft.md` — 论文正文（逐节追加，含 inline 占位符标记）+ 参考文献列表 + 待补项清单
2. `figures/figure_prompts.md` — 所有架构图生图提示词汇总（按图编号分节）
3. `figures/plot_*.py` — 数据结果图的 Python 绘图代码（按图编号命名，不自动执行）
4. `referenced-literature-checklist.md` — 引用文献清单（**强制，论文完成时必生成**）
5. `referenced-literature-inventory.md` — 引用文献过程记录（Step 3c 后生成，逐节追加）

对话中仅输出简短进度摘要，不输出完整论文正文。

## 可选产物（用户请求时生成）

以下产物不纳入强制流程，在用户明确要求或 venue 需要时生成：

| 产物 | 说明 | 何时需要 |
|------|------|---------|
| `abstract.md` | 单独提取的 Abstract | venue 要求独立提交时 |
| `cover-letter.md` | 投稿信模板 | 期刊投稿时 |
| `highlights.md` | 3-5 条核心贡献 | venue 要求时（如 Cell Press） |
| `venue-checklist.md` | venue-specific 提交检查清单 | 始终建议生成 |

## 默认 section queue

### empirical CS/AI paper

1. Introduction
2. Related Work
3. Method / Approach
4. Experimental Setup
5. Main Results
6. Ablation / Analysis
7. Discussion / Limitations
8. Conclusion

**Abstract 为后置章节**，不在初始 Section Queue 中。仅在 Section Queue 全部完成且所有核心章节 Verification = passed 后才允许生成。在此之前，在占位符系统中使用 `[ABSTRACT_NEEDED: 待主要证据稳定后撰写]`。

### 其他类型

先根据 `references/paper-structure.md` 选结构。Abstract 仍后置。

## 迭代控制

详见 `references/iteration-control.md`。

节级最小闭环：`Draft v1 → 证据合规审查 → Prose Quality Gate → Expansion → Self-Review → Revised Draft v2 → Verification`。

退出当前 section 的条件：
- Verification passed
- Verification blocked 且 safe_to_continue = yes
- 用户明确要求暂停

不退出条件：
- Verification failed 且非外部阻塞 → 继续下一轮修订
- Verification blocked 且 safe_to_continue = no → 等待外部证据

## 工作流概要

详见 `references/orchestration-workflow.md` 获取每个步骤的完整执行细节。

| Step | 动作 | 委托方式 | 触发方式 |
|------|------|---------|---------|
| 0 | 判定 mode、scope、当前 section | — | 自动 |
| 1 | 确认 venue / 语言 + 本地文献库询问（Blocking Gate） | — | 自动 |
| 1b | 可选：PDF→MD 转换准备（生成脚本+提示用户，不阻塞） | — | 自动（条件执行） |
| 2 | 证据审计（dispatch probe agents） | — | 自动 |
| 3 | 文献检索与核验（3a 本地优先 + 3b 联网 + 3c 聚合） | `academic-citation` + `literature-reader-agent`（并行 dispatch） | 自动 |
| 4 | 实验事实复核 | `academic-experiments`（dispatch 子 Agent） | 自动 |
| 5 | 生成 Section / Method Blueprint | — | 自动 |
| 6 | 起草 Draft v1（含占位符系统 + **待补项清单**） | — | 自动 |
| 7 | 占位符审计 + 图表生成 | `academic-figure`（dispatch 子 Agent，arch-prompt） | 自动 |
| 8 | 证据合规审查（Phase 1） | `academic-reviser`（dispatch 子 Agent） | 自动 |
| 9 | Prose Quality Gate（Phase 2） | `academic-polishing`（**内化调用**，主 Agent 自行执行） | 自动 |
| 10 | Expansion Pass（内容密度检查） | — | 自动 |
| 11 | Self-Review & Verification | `academic-reviser`（dispatch 子 Agent） | 自动 |
| 12 | 整合 & 依赖感知 section loop | — | 自动 |
| 12e | **引用清单生成**（强制，论文完成时必执行） | — | 自动 |

**核心约束**：Draft v1 → Evidence Review → Prose Review → Expansion → Verification → Advance（或 Revise）。

**执行细则**：每个委托步骤的 Task dispatch 模板、输入输出格式、子步骤顺序与失败处理统一定义在 `references/` 下的 `workflow-step-*.md` 文件中。执行时以导航索引 `references/orchestration-workflow.md` 为入口，按步骤加载对应文件。

### Step 6 必附：待补项清单

Draft v1 生成后，**必须**在正文末尾追加待补项清单。模板见 `references/workflow-step-5-8.md` Step 7d。

## 跨技能数据契约

数据契约定义在各子 Skill 的 `references/schemas/` 中：

| 契约 | 生产者 → 消费者 |
|------|----------------|
| `academic-experiments/references/schemas/evidence-inventory.md` | `academic-experiments` → Step 6 |
| `academic-citation/references/schemas/verified-references.md` | `academic-citation` → Step 6 |
| `academic-citation/references/schemas/literature-reading-report.md` | `literature-reader-agent` → Step 3 |
| `academic-reviser/references/schemas/verification-report.md` | `academic-reviser` → Step 11 |

各 Skill 的独立参考文件：

| 文件 | 用途 |
|------|------|
| `references/evidence-classification.md` | 三类证据定义 |
| `references/placeholder-guide.md` | 占位符系统规范 |
| `references/paper-types.md` | 论文类型定义 |

## Agent 资源与执行架构

主 Agent 直接撰写论文正文，确保叙事风格一致。子 Agent 仅提供工具型输出。

### 可 dispatch 的子 Agent

| 步骤 | 子 Skill | Agent 文件 | 职责 |
|------|---------|-----------|------|
| Step 2 | `academic-paper-writer` | `agents/probe-agent.md` | 只读探查 |
| Step 3 | `academic-citation` | `agents/citation_agent.md` | 检索与核验 |
| Step 3a/3b | `academic-citation` | `agents/literature-reader-agent.md` | 阅读并输出报告 |
| Step 4 | `academic-experiments` | `agents/experiment_agent.md` | 实验复核 |
| Step 7 | `academic-figure` | `agents/figure_agent.md` | 图表生成 |
| Step 8/11 | `academic-reviser` | `agents/reviser_agent.md` | 审查与验证 |

### 内化调用

| 步骤 | Skill | 说明 |
|------|-------|------|
| Step 9 | `academic-polishing` | 主 Agent 自行执行，确保风格一致 |

### 职责边界

- **主 Agent**：Section Blueprint、Draft v1、Expansion Pass、Cumulative Draft、Abstract、跨节一致性
- **子 Agent**：提供专项输出，不直接修改 Cumulative Draft

## 何时读取 references/

| Reference 文件 | 打开条件 |
|---------------|---------|
| `references/paper-structure.md` | 选章节结构时 |
| `references/writing-guidelines.md` | venue 风格适配时 |
| `references/iteration-control.md` | 进入修订循环时 |
| `references/content-density.md` | Step 10 Expansion Pass |
| `references/figure-generation-guide.md` | Step 7 生成图表时 |
| `references/exemplar-introduction.md` 等 | 写对应章节前（Exemplar < 3 篇时） |
| `references/evidence-classification.md` | Step 2 证据审计 |
| `references/placeholder-guide.md` | Step 6 生成 Draft |
| `references/mode-spectrum.md` | Step 0 选择模式 |
| `references/data-access-levels.md` | 理解数据访问边界 |
| `references/reporting-checklist.md` | Step 8 证据合规审查 / 实验相关 section 检查 |
| `skills/academic-citation/scripts/convert-pdfs-to-md.py` | Step 1b PDF→MD |
| `shared/references/concepts.md` | 跨技能共享概念速查 |

## 不适用场景

本 Skill 不适用于：
- 非 CS/AI/ML 领域的论文（如纯实验生物学、临床医学、人文社科）
- 已有完整 LaTeX 稿只需排版调整的场景
- 用户明确要求单次生成整篇论文且拒绝分节推进的场景（此时仍不能跳过证据检查）

## 失败处理

- **文献搜不到**：如实报告，不补假引文
- **代码跑不通**：报告阻塞点和环境需求，不伪造结果
- **运行成本过高**：退回 preexisting_artifact 盘点或最小复核
- **证据不足**：降级为带占位符的草稿，说明当前不能下哪些结论
- **用户要求一次成稿**：仍先给 Outline / Section Queue，再分节推进

## Anti-Patterns

| 模式 | 问题 | 正确做法 |
|------|------|---------|
| 跳过证据审计 | 不盘点证据直接开写 | 必须 Step 2 完成证据审计后再 Step 6 起草 |
| 批量输出整篇 | 同时多节起草导致证据一致性差 | 分节推进，逐节完成 Draft→Quality→Verification 闭环 |
| Abstract 前置 | 证据未稳时就先写 Abstract | Abstract 必须后置，等主体章节证据稳定后再写 |
| 无证据式 SOTA | 未与强基线比较就声称 SOTA | 任何 SOTA / state-of-the-art 表述必须附 baseline 比较表 |
| 自我审查赦免 | 因接近截止期就缩短审查流程 | Hard Gates 不可跳过，每种核实步骤都至少执行一遍 |

## Example Usage

### 场景 1: full-paper-planning — 从研究概要启动完整论文

**用户输入**：
> 我有一个基于双分支 Transformer 的 EEG 情绪识别项目，代码在 `./eeg-emotion/`，想用这个仓库写一篇完整论文投到 IEEE T-AFFC。

**执行流程摘要**：
```
Step 0: mode=full-paper-planning, scope=empirical CS/AI paper
Step 1: Venue Brief → IEEE T-AFFC, 英文, 双栏, 12页
Step 2: 并行 dispatch probe agents 探查代码/数据/配置
Step 3: 并行 dispatch citation agent + literature reader → Verified References (12篇本地+8篇外部)
Step 4: dispatch experiment agent → Evidence Inventory (3个newly_run结果, 2个preexisting_artifact)
Step 5: Section Blueprint → 8节结构 + 每节要点
Step 6: Draft v1 (Introduction) → 5段完整prose + 待补项清单
Step 7: arch-prompt 生成架构图提示词
Step 8: evidence compliance review → evidence_debt: closed
Step 9: prose quality gate → prose_debt: closed
Step 10: expansion pass → thin_draft: no
Step 11: verification → Verdict: passed, Score: 8/10
Step 12: 推进到 Related Work...
```

**对话输出**（auto 模式）：
> ✅ Introduction 完成 | Verdict: passed | Score: 8/10 | 下一节: Related Work

---

### 场景 2: section-drafting — 聚焦单节起草

**用户输入**：
> 帮我写 Method 节，代码在 `./model/`，重点讲清楚双分支架构和注意力机制。

**执行流程摘要**：
```
Step 0: mode=section-drafting, section=Method
Step 2: probe agent 探查代码 → 识别核心模块 (TemporalBranch, SpatialBranch, FusionModule)
Step 3: 文献检索 → 相关 attention 机制文献 (6篇VERIFIED)
Step 5: Blueprint → 整体框架 → 模块拆解 → 训练目标
Step 6: Draft v1 → 完整prose + [FIGURE_NEEDED: overall architecture] + 待补项清单
Step 7: arch-prompt 生成分支架构图提示词
Step 8-11: 审查闭环 → Verdict: passed
```

**输出片段**（Draft v1 Method 开头）：
> The proposed dual-branch Transformer architecture processes EEG signals through
> parallel temporal and spatial pathways... [后续展开模块细节]

---

### 场景 3: section-revision — 修订已有草稿

**用户输入**：
> 这是我的 Related Work 草稿，帮我审查修订：[粘贴草稿文本]

**执行流程摘要**：
```
Step 0: mode=section-revision, section=Related Work
Step 8: evidence compliance review → 发现3处裸claim无citation
Step 9: prose quality gate → prose_debt: open (罗列式段落)
Step 10: expansion pass → 补充work cluster综合比较
Step 11: verification → Verdict: passed, Score: 7/10
```

**输出**（Section Critique 摘要）：
> - Issues fixed: 补充3处inline citation, 将罗列式段落重组为2个work clusters
> - Claims weakened: "outperforms all existing methods" → "achieves competitive results"
> - Evidence still missing: [REF_NEEDED: recent GNN-based EEG methods]
