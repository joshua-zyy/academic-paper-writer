---
name: academic-paper-writer
description: "Core orchestrator for writing CS/AI/ML papers from scratch. Coordinates evidence audit, citation search, experiment verification, prose polishing, peer review, and figure generation across 6 sub-skills. Uses section-by-section drafting with Draft→Quality Gate→Expansion→Self-Review→Revision→Verification closed loop. Use when: writing a full paper draft from research notes or code repo, drafting paper sections one-by-one, coordinating multi-skill paper writing workflow, managing evidence-to-citation closed loop. Triggers on: 写论文, paper draft, 初稿, write introduction, draft method, 论文起草, full paper outline, section-by-section drafting, 证据闭环, 分节起草, academic paper writing, research paper drafting, write CS paper, draft AI paper, 从零写论文, 逐节写作."
---

# Academic Paper Writer (Core Orchestrator)

将此 skill 视为"证据闭环型、分节推进的论文编排代理"。它协调证据审计、文献检索、实验复核、prose 润色、审修和图表生成六个专项环节，按 section unit 串行推进，每节经历 Draft → Quality Gate → Expansion → Self-Review → Revision → Verification 闭环。

## Step 1 执行清单（Blocking Gate，9 项）

执行 Step 1 时，**必须**按顺序逐项完成。任一未完成不得进入 Step 2。

详细 checklist 和模板见 `references/workflow-step-0-4.md` Step 1 节。

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

Step 0→1(Blocking Gate)→1.5(Venue Research)→1b(可选)→2(证据审计)→3(文献检索)→4(实验复核)→5(Blueprint)→6(Section Complete Loop)→7(section loop)→8(引用清单)→9(图片批量生成)

Step 1 九项确认清单见 `references/workflow-step-0-4.md`。

**核心概念：Section Complete Loop（Step 6）** — 每个 section 都经历 6.0→6.9 的完整流程（起草→审查润色→整合），不可跳过。**Draft v1 ≠ 初稿完成**，只有完成 Step 6.8 的 section 才算初稿完成。

## Red Lines（绝对禁止）

1. **主 Agent 只撰写论文文本，绝对不得修改项目源代码、配置文件或数据文件**。探查时只读，图表代码生成时创建新文件而非覆盖现有文件。
2. 编造文献、作者、年份、venue、DOI、arXiv 编号
3. 编造实验结果、图表、命令或运行日志
4. 把 UNVERIFIED 文献当作 VERIFIED 写入正文
5. 把 user_claim（用户口述）当作可直接引用的证据
6. 把内部验证包装成外部泛化或 SOTA 结论
7. 把领域常见默认值写成当前项目已确认事实
8. 在正文没有任何 inline citation 的情况下输出参考文献列表
9. 把审查备注、元评论、代码讲解口吻混入 Paper Body
10. **能并行时必须并行**：当 dispatch 模板明确标注"必须并行"时，能并行时必须并行。平台不支持并行时允许串行降级，但必须在输出中标注 `dispatched_sequentially: true`。故意串行等待（非平台限制）→ Skill 执行失败。

## 非协商规则

1. **证据优先**：先找证据，再写定论。区分三类证据：`newly_run`、`preexisting_artifact`、`user_claim`。只把前两类当作可直接引用的证据。
2. **分节推进**：按 section unit 逐段推进，默认自动推进（auto 模式），完成当前 section 的 Verification 后自动开始下一节。用户可要求 step-by-step 模式逐节确认。
3. **上下文确认**：任务进入论文起草或正式章节写作时，必须先询问目标期刊/会议、本轮写作语言和本地文献库，不得直接开写。
4. **venue 优先**：目标 venue 已知时，章节结构优先遵循官方作者指南或模板，不套用通用结构。venue 要求必须通过 Step 1.5 实际调研并生成 Venue Brief，仅记录 venue 名称但不调研其要求等同于未确认 venue。
5. **占位符保留**：缺失模型架构图、实验流程图、表格、方法细节或数据集细节时，必须在正文对应位置留下显式占位标记，不得静默略过。
6. **方法深度**：Method 不得只写概述。对核心或非显然设计选择，必须交代：解决什么瓶颈、为什么采用这种设计、预期收益、代价/局限性/适用边界。
7. **Introduction/Related Work**：不得按通用模板直接开写。必须先调研同领域 exemplar papers，抽取常见叙述单元、比较框架与引用密度。
8. **审查备注分离**：审查备注、Critique/Audit Notes 不得混入论文正文。论文正文写入 `paper_draft.md`，审查备注在 agent 上下文中维护或按需在对话中输出。
9. **Abstract/Conclusion 后置**：必须等到主要证据稳定后再写，不得在结果未稳时抢先写成完整定稿。
10. **引用闭合**：需要文献支撑的段落必须有 inline citation 或 `[REF_NEEDED: ...]`。参考文献列表只能包含正文中被引用或已声明的条目。
11. **Section Complete Loop**：每节必须完成 Step 6 的完整闭环（Phase 1 起草 → Phase 2 审查润色 → Phase 3 整合）。**Draft v1 ≠ 初稿完成**，只有完成 Step 6.8（综合验证）的section才算初稿完成。
12. **失败不伪装**：Verification 未通过且非外部阻塞时，必须继续下一轮修订，不得直接结束或假装通过。
13. **完整流程执行**：执行 full-paper-planning 时，必须按 Step 0→1→1.5(Venue Requirements Research)→1b(若适用)→2→3(3a→3b→3c→3d)→4→5→6(6.0→6.9)→7→8→9 的顺序逐一执行，不得跳步。用户催促时也不得跳过 Step 1.5（Venue Requirements Research）、证据审计（Step 2）、文献检索（Step 3）、实验复核（Step 4）、Hard Gates（A/B/C）中的任何一个。
14. **引用产物必输出**：Step 3 完成后，必须在上下文中维护 Verified References 列表和 Citation-to-Claim Map。缺少任一 → 不得进入 Step 6。
15. **引用数量下限**：整篇完整论文的总引用数（含本地文献库和外部文献，去重后）不得少于 `min_citations`（默认 35，short paper 建议 20，workshop 建议 15）。**Step 1 必须询问用户预期引用数量**，用户指定时记录为 `min_citations`，未指定时使用默认值。论文完成后 Step 8 生成引用清单时自动核验。
16. **两阶段写作**：Step 5 Blueprint 可使用 bullet points 和提纲式结构，但 Step 6 Draft v1 必须是完整 prose 段落。bullet points 仅用于规划阶段，不得出现在最终论文正文中。
17. **最大迭代次数**：修订循环（Step 6.7→6.8→7）最多执行 3 轮。3 轮后仍有未闭合 debt 时，标记为 `unresolvable`，输出修订报告并终止循环，不得继续重试。
18. **Section Contract 先于 prose**：每节在 Step 5 必须根据 `references/section-writing-contracts.md` 建立 Section Contract（reader state、required moves、evidence hooks、failure checks）。Step 6 Draft v1 不得跳过该 contract 直接写正文；润色只能在 contract debt 基本闭合后执行。
19. **数字引用格式（默认）**：正文中所有 inline citation 默认使用数字格式 `[1]`, `[2]`, `[1,3,5]`, `[2-4]`。当 `venue-brief.md` 中 `Citation Format` 明确指定为 author-year 格式时，遵循 venue 要求，使用作者-年份格式。参考文献列表的编号/格式与正文引用一一对应。

## 文件输出规范

1. **输出目录**：`./docs/paper-drafts/`
2. **论文文件**：`paper_draft.md` — 论文正文 + 参考文献 + 待补项清单，逐步追加更新
3. **Blueprint文件**：`section_blueprint.md` — Section Blueprint（Step 5输出，每节更新）
4. **图片目录**：`figures/` — `figure_prompts.md`（架构图提示词）+ `plot_*.py`（数据图代码）
5. **对话输出限制**：禁止在对话中输出完整论文正文，仅显示简短进度摘要
6. **写入时机**：每节 Draft 生成后、Verification 完成后，均须使用 Write/Edit 工具更新 `paper_draft.md`
7. **中间状态**：Evidence Inventory、Verified References、Revision Queue 等在 agent 上下文中维护
8. **Venue Brief**：`venue-brief.md` — venue 投稿要求摘要（Step 1.5 输出，后续步骤必参考）

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
| DP-1 | Step 1.5 完成后 | Venue Brief 摘要（venue、语言、min_citations、venue 要求、本地文献库状态） | 确认/修正 |
| DP-2 | Step 5 Blueprint 完成后 | Section Blueprint（章节结构、每节要点、证据来源） | 确认/调整 Blueprint |
| DP-3 | Step 6.2 Draft v1 完成后 | Draft 摘要（当前节、段落数、待补项清单摘要） | 确认方向/指出问题 |
| DP-4 | Step 6.8 Verification 完成后 | Verification Status（verdict、overall score、未闭合问题） | 确认通过/要求修订 |

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

除纯 pass-through 模式（如 `related-work-or-citation-pass`、`experiment-evidence-pass`）外，所有起草/修订模式都必须执行同一组 Hard Gates 与 Step 0 → 9 闭环；`section-drafting` 只是缩小证据范围，不缩短流程。

推进模式详见上方"推进模式"节。默认 auto 模式，用户可切换。

## 完整性门控（Hard Gates）

以下门控是不可跳过的完整性检查关卡。任一未通过不得进入下一阶段。详细条件和失败处理见 `references/orchestration-workflow.md`。

| Gate | 触发位置 | 核心条件 | 失败处理 |
|------|---------|---------|---------|
| E: Venue 调研 | Step 1 → Step 2 | venue 确认后必须完成 Step 1.5，生成 venue-brief.md | 阻塞，不得进入 Step 2 |
| A: 证据完备 | Step 2 → Step 6 | 至少一条可引用证据（`newly_run`/`preexisting_artifact`） | 降级路径或阻塞 |
| B: 引用就绪 | Step 3 → Step 6 | 至少一条 `VERIFIED` 引用或明确"无需文献" | 按 section 分流，Intro/RW 阻塞，Method 可占位 |
| C: Verification | Step 6.8 → Step 7 | 所有硬 debt 闭合 + thin_draft = no（figure_debt 为软约束，open 时可 blocked + safe_to_continue） | passed/blocked/failed，详细见 workflow |
| D: 引用数量 | Step 8 → 输出 | 全文去重后引用总数 >= `min_citations`（默认 35） | 未达标时提醒用户，可继续补充后重检 |

## 默认交付物

详见 `references/orchestration-workflow.md`。输出目录 `./docs/paper-drafts/`。

## 默认 section queue

详见 `references/paper-structure.md`。Abstract 为后置章节，不在初始队列中。

## 迭代控制

详见 `references/iteration-control.md`。修订循环最多 3 轮，详见 `references/orchestration-workflow.md`。

## 工作流概要

详见 `references/orchestration-workflow.md` 获取步骤索引、完整执行细节和 dispatch 模板。

### Step 6: Section Complete Loop（详细说明）

每节必须完成以下完整流程，**Draft v1 ≠ 初稿完成**：

- **Phase 1**: 6.0 核对 Section Contract → 6.1 前置探查 → 6.2 Draft v1 → 6.3 写入文件
- **Phase 2**: 6.4 占位符审计+图表 → 6.5 证据合规 → 6.6 Prose 质量门 → 6.7 扩写检查 → 6.8 综合验证
- **Phase 3**: 6.9 整合 → 推进到下一节

详细执行清单见 `references/workflow-step-5-6.5.md` Step 6 节。

### 6.1 前置探查规则表

详见 `references/workflow-step-5-6.5.md` Step 6.1 节。

### 各步骤详细参考

详见 `references/workflow-step-5-6.5.md` Step 6.4–6.5 和 `references/workflow-step-6.6-9.md` Step 6.6–6.8。

## 跨技能数据契约（Schemas）

详见 `references/orchestration-workflow.md` 的"Shared Inputs and References"节。Schema 文件位于各子 skill 的 `references/schemas/` 目录。

## Agent 资源与执行架构

Agent 定义、dispatch 模板、职责边界见各子 skill 的 `agents/` 目录。主 Agent 负责论文正文和跨节一致性，子 Agent 提供专项输出。

## 何时读取 references/

详见 `references/orchestration-workflow.md` 的"Shared Inputs and References"节。按步骤加载对应文件，不预加载。

## 不适用场景

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

三个端到端使用场景（full-paper-planning、section-drafting、section-revision）详见 `references/examples/example-usage.md`。首次使用时建议读取。
