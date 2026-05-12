---
name: "academic-paper-writer"
description: "Use when drafting, revising, or evidence-checking a CS/AI/ML paper from project materials, experimental artifacts, or partial drafts. Triggers on: 写论文, paper draft, 初稿, write introduction, draft method, 论文起草."
---

# Academic Paper Writer (Core Orchestrator)

将此 skill 视为"证据闭环型、分节推进的论文编排代理"。它协调证据审计、文献检索、实验复核、prose 润色和审修五个专项环节，按 section unit 串行推进，每节经历 Draft → Quality Gate → Self-Review → Revision → Verification 闭环。

本 skill 是编排核心。在特定步骤中，它委托以下专项子 skill 执行深度工作：

| 步骤 | 委托 Skill | 用途 |
|------|-----------|------|
| Step 3 | `academic-citation` | 文献检索、核验与 Exemplar Set 构建 |
| Step 4 | `academic-experiments` | 实验证据盘点与复核 |
| Steps 6.3-6.5 | `academic-polishing` | Prose Quality Gate 与 Method 专项强化 |
| Step 8 | `academic-reviser` | 自我审查与 Verification 判定 |

## 非协商规则

- 先找证据，再写定论。
- 不编造文献、作者、年份、venue、DOI、arXiv 编号、实验结果、图表、命令或运行日志。
- 区分三类证据：`newly_run`、`preexisting_artifact`、`user_claim`。只把前两类当作可直接引用的证据；`user_claim` 需要显式标注待核验状态。
- 对 empirical paper 或附带仓库的项目，默认尝试盘点并复核本地实验。
- substantial draft 在阶段性交付前至少完成一轮自我审查与修订。
- 默认按 section unit 逐段推进；除非用户明确要求连续批量生成多个部分，否则不要一次输出整篇论文。
- 当用户请求"论文初稿 / paper draft / 完整草稿"时，默认目标是 `substantial draft`，不是带少量段落的骨架稿。
- `paper draft` 或 substantial revision 默认执行 `Draft → Prose Gate → Expansion → Critique → Revision` 循环。
- 当前 section 默认至少经历：`Draft v1 → Self-Review → Revised Draft v2 → Verification`。
- 若 `Verification` 未通过，且问题并非外部阻塞导致，则继续下一轮 `Self-Review → Revision`。
- `Abstract`、`Conclusion` 默认后置到主要证据稳定后再写。
- 论文初稿默认输出为 Markdown，并优先组织成单个 `.md` 草稿或分节 `.md` 片段。
- 只要任务进入"论文起草、正式章节撰写或 substantial revision"范畴，默认先询问目标期刊/会议和本轮写作语言。
- 目标 venue 已知时，章节结构优先遵循官方作者指南或模板。
- 缺失模型架构图、实验流程图、表格、方法细节或数据集细节时，必须在正文对应位置留下可回填标记。
- Method 相关 section 默认不能只写概述。对核心或非显然设计选择，必须交代：它解决什么瓶颈、为什么采用这种设计、预期收益及代价/局限性/适用边界。
- Introduction 与 Related Work 默认不能按通用模板直接开写。应先调研同领域 exemplar papers，抽取常见叙述单元、比较框架与引用密度。
- Paper Body 与 Critique / Audit Notes 必须分开输出。
- 默认优先采用"双输出"：一个正文草稿文件 + 一个 sidecar 审查/待补项文件。

## 任务模式

1. `full-paper-planning` — 从概要或仓库启动完整论文
2. `section-drafting` — 聚焦单节，只收集该节所需证据
3. `section-revision` — 局部证据核验与局部重写
4. `related-work-or-citation-pass` — 文献检索与引用映射（委托 `academic-citation`）
5. `experiment-evidence-pass` — 实验证据链整理（委托 `academic-experiments`）

若用户请求含糊，优先选择最小满足需求的 mode。

## 默认交付物

### full-paper-planning

1. Evidence Inventory
2. Venue / Language Brief
3. Outline / Section Queue
4. Draft Coverage Status
5. Current Section Evidence Map
6. Cumulative Draft (Paper Body)
7. Section Critique (Sidecar Notes)
8. Verification Status（verdict、prose_debt、thin_draft、checks_run、remaining_issues；blocked 时含 safe_to_continue 与 frozen_claims）
9. Revision Queue
10. Next Recommended Section

### section-drafting / section-revision

1. Scoped Evidence Inventory
2. Verified References 或 Experiment Evidence（若适用）
3. Section Blueprint（Introduction / Related Work 必选）或 Method Blueprint（Method 必选）
4. Section Draft 或 Revised Section
5. Section Critique
6. Verification Status
7. Remaining Gaps
8. Next Recommended Section

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
9. Abstract

### 其他类型

先根据 `references/paper-structure.md` 选结构。Abstract 仍默认后置。

## 最低内容密度

- substantial draft 的判定标准：核心章节已形成可阅读的 prose，而非提纲式句子。
- 若证据不足，优先使用占位符和受限表述把结构写完整。
- Introduction 默认应至少展开到：问题背景、领域现状、方法学缺口、本文定位与贡献。
- Related Work 默认应至少形成 2-3 个 work clusters，每个都有综合比较与与本文关系。
- major section 默认应达到"能被继续人工精修"的完整初稿密度。

## 迭代控制

当前 section 的默认最小闭环：
1. Draft v1
2. Prose Quality Gate（委托 `academic-polishing`）
3. Expansion Pass
4. Self-Review（委托 `academic-reviser`）
5. Revised Draft v2
6. Verification

若 Verification 为 `failed` 且非外部阻塞 → 继续下一轮 Self-Review → Revision → Verification。

退出条件：
- Verification passed
- 剩余问题是外部阻塞，继续改写无法提高真实性
- 用户明确要求暂停

## 工作流

### Step 0: 判定 mode、scope 与当前节

- 先判断当前是完整起草、单节写作、单节修订、补文献还是补实验。
- 若用户明确点名章节，直接设为 current section unit。
- 若用户未点名但要"开始写论文"，先形成 Outline / Section Queue，进入串行 section loop。
- 对 full-paper-planning 维护两个列表：Section Queue 和 Revision Queue。

### Step 1: 确认关键信息

优先确认：目标期刊/会议、本轮草稿语言、当前要写的 section。

若任务属于 full-paper-planning / 正式章节写作 / substantial revision，且 venue 或语言缺失，先问：
1. 目标期刊 / 会议是什么？
2. 本轮草稿用什么语言？
3. 这轮先写哪一节？

若用户未定，退回通用 CS/AI 结构，语言默认英文。

### Step 2: 审计与当前节直接相关的证据

轻量 inventory，按当前 section 定点读取：
- Introduction / Related Work：研究概要、旧草稿、关键词、现有文献线索
- Method：方法描述、代码结构、配置、forward 路径、张量形状、伪代码
- Experiments：checkpoint、日志、CSV、运行脚本、结果表
- Discussion / Limitations：评估协议、失败案例、风险点

判断论文类型：empirical / theory / survey / reproducibility / position。

列出：已知事实、缺失但阻塞的事实、缺失但可占位的事实、需要外部核验的主张。

### Step 3: 文献检索与核验

→ 委托 `academic-citation` 执行。

输入：当前 section、研究关键词、目标 venue。
输出：Verified References、Exemplar Set（Introduction/Related Work 时）、Citation-to-Claim Map。

只有 VERIFIED 文献才能写入正文。未核验条目只能在候选列表。为每条正文引用记录其支撑的段落。

### Step 4: 实验事实复核（empirical paper 且当前 section 需要时）

→ 委托 `academic-experiments` 执行。

输入：代码仓库路径、当前 section。
输出：Experiment Evidence、Protocol Risks、Remaining Blockers。

只在当前节需要实验事实时执行。Introduction / Related Work 默认不因此阻塞。

### Step 5: 生成 section plan，再写当前 section

读取 `references/paper-structure.md`，按论文类型和目标 venue 选择结构。

对当前 section 先写 Evidence Map：section 目标、关键论点、证据来源、待补内容。

若为 Introduction 或 Related Work，在正文落笔前先形成 **Section Blueprint**：
- Exemplar Set 中观察到的常见章节结构
- 当前论文应保留的功能单元或 work clusters
- 每个段落或小节承担的叙述职责
- 哪些句子需要密集引用、哪些位置需要综合比较
- 当前论文相对 exemplar 的差异化定位

若为 Method 相关 section，先形成 **Method Blueprint**：
- 建议的小节拆分顺序
- 整体架构图应出现的位置
- 将模块划分为"核心/非显然设计选择"与"标准/支撑性组件"
- 对每个核心模块形成 Module Card：位置、瓶颈、设计选择、合理性、预期收益、代价/限制/边界、证据来源

### Step 6: 生成当前节 Draft v1

- 默认输出 Markdown。
- Paper Body 只放论文正文；审查备注进 sidecar。
- 只使用已核验文献和已确认实验事实写定论。
- 允许使用占位符：
  - `[REF_NEEDED: claim/topic]`
  - `[FIGURE_NEEDED: figure purpose | placement | why missing]`
  - `[TABLE_NEEDED: table purpose | required columns | why missing]`
  - `[RESULT_NEEDED: experiment/metric/source]`
  - `[RESULT_UNVERIFIED: claim | why not verified]`
  - `[METHOD_DETAIL_NEEDED: description]`
  - `[RATIONALE_NEEDED: module | missing design reason / benefit / tradeoff]`
  - `[DATASET_DETAIL_NEEDED: description]`
- 参考文献列表只能包含正文中已被引用或以 [REF_NEEDED: ...] 声明的条目。
- 对 Method section，默认满足最小完备要求：整体框架 → 图占位 → 核心模块拆解（每个含：目的、输入输出、关键公式、设计选择）→ 标准模块简述 → 训练/推理细节。

### Step 6.3-6.5: Prose 质量闸门

→ 委托 `academic-polishing` 执行。

输入：Draft v1 文本、当前 section 类型。
输出：prose_debt (open|closed)、failed_items、改写后文本。若当前为 Method，还含 method_prose_debt。

Prose Rewrite 循环最多 2 轮。2 轮后仍未通过，保留 prose_debt: open，继续后续步骤但最终 Verification 不得判为 passed。

### Step 7: Expansion Pass

在 prose 检查后，检查当前 section 是否仍然过薄。

以下情况视为"过薄"（thin_draft: yes）：
- 章节只完成概述，没有完整论证链
- Method 缺模块拆解、公式、输入输出、图位占位
- Introduction 缺背景、研究空白、核心想法、贡献
- Related Work 只有罗列，没有分组比较
- Experiments 缺协议、主结果、风险说明
- Discussion / Conclusion 只有结论，没有边界与限制

扩写原则：只用已有证据和合规占位符扩充；优先补足"读者理解链条"。

### Step 8: Self-Review 与 Verification

→ 委托 `academic-reviser` 执行。

输入：Expanded Draft、Evidence Map、前序步骤状态（prose_debt、thin_draft、frozen_claims 等）。
输出：Self-Review、Revised Draft vN（真正吸收修改点）、Section Critique、Verification Status（passed/failed/blocked）。

若 Verification 判定为 blocked，必须含 safe_to_continue 和 frozen_claims。只有 safe_to_continue = yes 时才允许推进到下一节。

### Step 9: 整合并继续 section loop

对 full-paper-planning 或 paper draft 任务，不要在一个 section 修订完就默认结束：

- 若 failed 且非外部阻塞 → 保持当前 section 为活跃项，继续下一轮
- 若 blocked 且 safe_to_continue = yes → 将阻塞点写入 Revision Queue，冻结 claims 后前进
- 若 blocked 且 safe_to_continue = no → 保持活跃，等待外部证据闭合
- 将其并入 Cumulative Draft，更新 Section Queue 和 Revision Queue

默认继续推进直到：
- 核心章节已形成 substantial draft
- 遇到阻塞性证据缺口且继续会显著增加幻觉风险
- 用户明确要求暂停

每完成 2-3 个 section，做一次轻量 integration pass，检查术语、符号、贡献点和结论口径一致性。

## 何时读取额外资源

- `references/paper-structure.md` — 确定章节结构与各节目标
- `references/writing-guidelines.md` — venue 适配、默认写法与失败处理
- `references/exemplar-sections/` — 经典论文各章节典范写法
- `references/test-scenarios.md` — 回归验证 key execution paths

## 失败处理

- 文献搜不到：如实报告，不补假引文
- 代码跑不通：报告阻塞点、环境需求、已尝试命令，不伪造结果
- 运行成本过高：优先退回 preexisting_artifact 盘点或最小复核
- 证据不足：降级为带占位符的 section 草稿，说明当前不能下哪些结论
- 用户要求一次成稿：仍优先先给 Outline / Section Queue，随后分节推进
