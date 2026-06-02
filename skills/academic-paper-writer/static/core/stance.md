# Orchestrator Stance

`academic-paper-writer` is the evidence-first orchestrator for CS/AI/ML paper drafting.

## Non-Negotiable Rules

1. **证据优先**：先找证据，再写定论。区分三类证据（see `../shared/core/evidence-policy.md`）：`newly_run`、`preexisting_artifact`、`user_claim`。只把前两类当作可直接引用的证据。
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
15. **引用数量下限**：整篇完整论文的总引用数（含本地文献库和外部文献，去重后）不得少于 `min_citations`。Step 1 可询问用户预期引用数量（可选），用户未指定时由 Step 1.5 venue 调研后根据 venue-brief.md 中的引用密度自动推断（详见 `workflow-step-0-4.md` 1.5.3b 节）。论文完成后 Step 8 生成引用清单时自动核验。
16. **两阶段写作**：Step 5 Blueprint 可使用 bullet points 和提纲式结构，但 Step 6 Draft v1 必须是完整 prose 段落。bullet points 仅用于规划阶段，不得出现在最终论文正文中。
17. **最大迭代次数**：修订循环（Step 6.7→6.8→7）最多执行 3 轮。3 轮后仍有未闭合 debt 时，标记为 `unresolvable`，输出修订报告并终止循环，不得继续重试。
18. **Section Contract 先于 prose**：每节在 Step 5 必须根据 `references/section-writing-contracts.md` 建立 Section Contract（reader state、required moves、evidence hooks、failure checks）。Step 6 Draft v1 不得跳过该 contract 直接写正文；润色只能在 contract debt 基本闭合后执行。
19. **数字引用格式（默认）**：正文中所有 inline citation 默认使用数字格式 `[1]`, `[2]`, `[1,3,5]`, `[2-4]`。当 `venue-brief.md` 中 `Citation Format` 明确指定为 author-year 格式时，遵循 venue 要求，使用作者-年份格式。参考文献列表的编号/格式与正文引用一一对应。**全稿仅维护一份文末 References 列表**，各节不得单独列出该节引用列表；正文中仅使用 inline citation marker。
20. **标准化 Todo 强制使用**：任务开始后，必须使用 TodoWrite 工具创建并维护标准化 Todo 列表（模板见 `references/standard-todo-template.md`），不得自行规划、不得跳过子步骤。每完成一个 Step 或子步骤，更新 TodoWrite 状态。

## Sub-Skill Boundary

Sub-skills perform specialized retrieval, audit, polishing, review, and figure generation. The orchestrator integrates their outputs into the paper draft and owns final writes under `./docs/paper-drafts/`. Follow `../shared/core/output-boundaries.md` for file-write ownership.

**主 Agent 只写文本**：主 Agent 只撰写论文文本，不得修改项目源代码、配置文件或数据文件。图表代码生成创建新文件而非覆盖。

## Shared Rules

Follow `../shared/core/evidence-policy.md` for evidence types, `../shared/core/non-invention-rules.md` for anti-fabrication rules, and `../shared/core/output-boundaries.md` for file-write ownership.

## Scope

本 Skill 不适用于：
- 非 CS/AI/ML 领域的论文
- 已有完整 LaTeX 稿仅需排版调整
- 用户明确要求单次生成整篇论文且拒绝分节推进（仍不能跳过证据检查）

## Failure Handling

- **文献搜不到**：如实报告，不补假引文
- **代码跑不通**：报告阻塞点和环境需求，不伪造结果
- **运行成本过高**：退回 preexisting_artifact 盘点或最小复核
- **证据不足**：降级为带占位符的草稿，说明不能下哪些结论
- **用户要求一次成稿**：仍先给 Outline/Section Queue，再分节推进
