---
name: "academic-paper-writer"
description: "Use when drafting, revising, or evidence-checking a CS/AI/ML paper from project materials, experimental artifacts, or partial drafts. Triggers on: 写论文, paper draft, 初稿, write introduction, draft method, 论文起草."
metadata:
  version: "1.0.0"
  last_updated: "2026-05-13"
  status: stable
  data_access_level: verified_only
  task_type: open-ended
  related_skills:
    - academic-citation
    - academic-experiments
    - academic-figure
    - academic-polishing
    - academic-reviser
---

# Academic Paper Writer (Core Orchestrator)

将此 skill 视为"证据闭环型、分节推进的论文编排代理"。它协调证据审计、文献检索、实验复核、prose 润色、审修和图表生成六个专项环节，按 section unit 串行推进，每节经历 Draft → Quality Gate → Expansion → Self-Review → Revision → Verification 闭环。

## 何时使用本 Skill vs. 子 Skill

| 场景 | 使用 |
|------|------|
| 从零起草论文、逐节推进完整初稿 | `academic-paper-writer`（本 Skill） |
| 只需检索/核验文献 | `academic-citation` |
| 只需复核实验产物 | `academic-experiments` |
| 只需润色/去AI化/降claim强度 | `academic-polishing` |
| 只需审查/修订已有草稿 | `academic-reviser` |
| 只需生成论文图表 | `academic-figure`（实验数据图自动出图 / 架构图提供生图提示词） |

本 Skill 在以下步骤委托子 Skill 执行专项任务：

| Step | 委托 Skill | 用途 |
|------|-----------|------|
| Step 3 | `academic-citation` | 文献检索、核验与 Exemplar Set 构建 |
| Step 4 | `academic-experiments` | 实验证据盘点与复核 |
| Step 4.5 | `academic-figure` | 根据实验证据生成论文图表（可选，仅用户要求出图时触发） |
| Step 7 | `academic-polishing` | Prose Quality Gate 与 Method 专项强化 |
| Step 9 | `academic-reviser` | 自我审查与 Verification 判定 |

## Red Lines（绝对禁止）

以下行为绝对禁止，违反即为 Skill 执行失败：

1. 编造文献、作者、年份、venue、DOI、arXiv 编号
2. 编造实验结果、图表、命令或运行日志
3. 把 UNVERIFIED 文献当作 VERIFIED 写入正文
4. 把 user_claim（用户口述）当作可直接引用的证据
5. 把内部验证包装成外部泛化或 SOTA 结论
6. 把领域常见默认值写成当前项目已确认事实
7. 在正文没有任何 inline citation 的情况下输出参考文献列表
8. 把审查备注、元评论、代码讲解口吻混入 Paper Body

## 非协商规则

1. **证据优先**：先找证据，再写定论。区分三类证据：`newly_run`、`preexisting_artifact`、`user_claim`。只把前两类当作可直接引用的证据。
2. **分节推进**：按 section unit 逐段推进，除非用户明确要求连续批量生成多个部分，否则不得一次输出整篇论文。
3. **上下文确认**：任务进入论文起草或正式章节写作时，必须先询问目标期刊/会议和本轮写作语言，不得直接开写。
4. **venue 优先**：目标 venue 已知时，章节结构优先遵循官方作者指南或模板，不套用通用结构。
5. **占位符保留**：缺失模型架构图、实验流程图、表格、方法细节或数据集细节时，必须在正文对应位置留下显式占位标记，不得静默略过。
6. **方法深度**：Method 不得只写概述。对核心或非显然设计选择，必须交代：解决什么瓶颈、为什么采用这种设计、预期收益、代价/局限性/适用边界。
7. **Introduction/Related Work**：不得按通用模板直接开写。必须先调研同领域 exemplar papers，抽取常见叙述单元、比较框架与引用密度。
8. **双输出**：Paper Body 与 Critique/Audit Notes 必须分开输出为两个文件。审查备注不得混入论文正文。
9. **Abstract/Conclusion 后置**：必须等到主要证据稳定后再写，不得在结果未稳时抢先写成完整定稿。
10. **引用闭合**：需要文献支撑的段落必须有 inline citation 或 `[REF_NEEDED: ...]`。参考文献列表只能包含正文中被引用或已声明的条目。
11. **一轮闭环**：当前 section 至少经历 Draft v1 → Prose Quality Gate → Expansion → Self-Review → Revised Draft v2 → Verification。不得把 v1 当作完成稿交付。
12. **失败不伪装**：Verification 未通过且非外部阻塞时，必须继续下一轮修订，不得直接结束或假装通过。

## 任务模式

1. `full-paper-planning` — 从概要或仓库启动完整论文（平衡光谱）
2. `section-drafting` — 聚焦单节，只收集该节所需证据（平衡光谱）
3. `section-revision` — 局部证据核验与局部重写（忠实度光谱）
4. `related-work-or-citation-pass` — 文献检索与引用映射（委托 `academic-citation`，忠实度光谱）
5. `experiment-evidence-pass` — 实验证据链整理（委托 `academic-experiments`，忠实度光谱）

若用户请求含糊，优先选择最小满足需求的 mode。

模式光谱详情见 `../shared/references/mode-spectrum.md`。

## 完整性门控（Hard Gates）

以下三种门控是不可跳过的完整性检查关卡。任一关卡未通过不得进入下一阶段。

### Gate A: 证据完备门控（Step 2 → Step 6）

**触发位置**：Step 2（证据审计）完成后、Step 6（Draft v1 生成）开始前。

**条件**：
- Evidence Inventory 必须包含至少一条与当前 section 直接相关的可引用证据（`newly_run` 或 `preexisting_artifact`）
- 若本节完全不涉及实验事实（如纯理论推导），必须有明确的 "no experiment required" 记录

**门控失败处理**：
- 领域论文类型不是需要实验证据的类型 → 降级为理论/position 结构并记录 paper_type，继续
- 实质性缺失且无替代方案 → 阻塞，向用户报告：当前 section 无可用证据，需要用户提供材料或改变 section 范围
- 不得在证据为零时生成 Draft v1

### Gate B: 引用资源就绪门控（Step 3 → Step 6）

**触发位置**：Step 3（文献检索与核验）完成后、Step 6（Draft v1 生成）开始前。

**检查内容**：引用资源是否可用，而非检查正文（正文尚未生成）。

**条件**：
- 至少有一条与当前 section 相关的 `VERIFIED` 引用已到位，或
- 明确记录"当前 section 不需要文献支撑"（如纯方法推导部分在无外部引用时）
- 所有候选条目已标注 `VERIFIED` 或 `UNVERIFIED`

**门控失败处理**：
- 全部为空（零引用）→ 对于 Introduction / Related Work 必须阻塞并提示至少找到 1-2 篇 seed reference 后再开始；对于其他 section 可以先起草但必须标注引用缺口

**正文引用约束**（Step 6 起草时执行，非门控检查项）：
- Draft v1 中每个需要文献支撑的 claim 必须有 `VERIFIED` 引用或 `[REF_NEEDED: ...]` 占位符
- 不能在正文中出现既无引用又无占位符的 "裸 claim"
- 未核验条目不能作为确定引用，只能以 `[REF_NEEDED: ...]` 形式出现

### Gate C: Verification 阶段通过门控（Step 9 → Step 10）

**触发位置**：Step 9（Self-Review & Verification）完成后、Step 10（section loop 推进）开始前。

**条件**（基于 Step 9 输出判定）：
- `verdict = passed` → 可自由推进到下一节
- `verdict = blocked` 且 `safe_to_continue = yes` → 可推进，阻塞点进入 Revision Queue
- `verdict = failed` 或 `blocked` 且 `safe_to_continue = no` → **禁止推进**，必须继续当前 section 的修订

**门控失败处理**：
- failed → 自动回到 Step 9 进入下一轮修订（最多 3 轮仍未通过 → 冻结所有未闭合 claims，标记为 `verdict: escalated`，报告给用户决策是否继续）
- blocked + safe_to_continue = no → 终止当前 section 活动，等待用户提供外部证据
- 不得在 failed 状态下伪推进到下一节

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

先根据 `references/paper-structure.md` 选结构。Abstract 仍后置。

## 迭代控制

详见 `references/iteration-control.md`。

节级最小闭环：`Draft v1 → Prose Quality Gate → Expansion → Self-Review → Revised Draft v2 → Verification`。

退出当前 section 的条件：
- Verification passed
- Verification blocked 且 safe_to_continue = yes
- 用户明确要求暂停

不退出条件：
- Verification failed 且非外部阻塞 → 继续下一轮修订
- Verification blocked 且 safe_to_continue = no → 等待外部证据

## 工作流

### Step 0: 判定 mode、scope 与当前节

- 判断当前是完整起草、单节写作、单节修订、补文献还是补实验。
- 若用户明确点名章节，直接设为 current section unit。
- 若用户未点名但要求"写论文"，先形成 Outline / Section Queue，进入串行 section loop。
- 对 full-paper-planning 维护两个列表：Section Queue（待起草）和 Revision Queue（已起草但需修订）。

### Step 1: 确认关键信息（Blocking Gate）

以下为阻塞性确认——信息缺失时必须停止并提问，不得继续执行：

1. **目标期刊/会议**：若任务属于 full-paper-planning / 正式章节写作 / substantial revision，则 venue 为必问项。仅当用户明确表示"未定/你来决定"时，才退回通用 CS/AI 结构。
2. **本轮草稿语言**：若任务进入正式章节写作且语言未给出，必须询问。默认英文。
3. **当前要写的 section**：若用户未指定，由 Step 0 决定。

若 venue 已知且对当前 section 有影响，读取 `references/writing-guidelines.md` 并形成简短 Venue / Language Brief。

### Step 2: 审计与当前节直接相关的证据

轻量 inventory，按当前 section 定点读取。不做无差别全仓库扫描。

按 section 定向读取：
| Section | 读取材料 |
|---------|---------|
| Introduction / Related Work | 研究概要、旧草稿、关键词、现有文献线索 |
| Method | 方法描述、代码结构、配置、forward 路径、张量形状、伪代码 |
| Experiments | checkpoint、日志、CSV、运行脚本、结果表 |
| Discussion / Limitations | 评估协议、失败案例、风险点 |

判断论文类型：empirical / theory / survey / reproducibility / position。

列出四类信息：
- 已知事实
- 缺失但阻塞当前 section 的事实
- 缺失但可占位的事实
- 需要外部核验的主张

若当前为 Introduction 或 Related Work，额外审计同领域 exemplar papers 候选集合。

若当前为 Method，额外审计：模型整体数据流、核心模块边界、输入输出张量形状、可从代码恢复的公式。

### Step 3: 文献检索与核验

→ 委托 `academic-citation` 执行。

输入：当前 section、研究关键词、目标 venue。
输出：按 `../shared/schemas/verified-references.md` 组织：Verified References、Exemplar Set（Introduction/Related Work 时）、Citation-to-Claim Map。

约束：只有 VERIFIED 文献才能写入正文。未核验条目只能在候选列表。

### Step 4: 实验事实复核

→ 委托 `academic-experiments` 执行（仅当 empirical paper 且当前 section 需要实验事实时）。

输入：代码仓库路径、当前 section。
输出：按 `../shared/schemas/evidence-inventory.md` 组织：Experiment Evidence、Protocol Risks、Remaining Blockers。

Introduction / Related Work 不因此步骤阻塞。

### Step 5: 生成 section plan

读取 `references/paper-structure.md`，按论文类型和目标 venue 选择结构。

对当前 section 先生成 Evidence Map：section 目标、关键论点、证据来源、待补内容。

**Introduction / Related Work 必须生成 Section Blueprint**：
- Exemplar Set 中观察到的常见章节结构
- 当前论文应保留的功能单元或 work clusters
- 每个段落或小节承担的叙述职责
- 哪些句子需要密集引用、哪些位置需要综合比较
- 当前论文相对 exemplar 的差异化定位

**Method 相关 section 必须生成 Method Blueprint**：
- 建议的小节拆分顺序
- 整体架构图应出现的位置与图注意图
- 将模块划分为"核心/非显然设计选择"与"标准/支撑性组件"
- 对每个核心模块形成 Module Card：位置、瓶颈、设计选择、合理性、预期收益、代价/限制/边界、证据来源（artifact-verified / inferred-from-gap / missing）

### Step 6: 生成 Draft v1

- 输出 Markdown。
- Paper Body 只放论文正文；审查备注进 sidecar。
- 只使用已核验文献和已确认实验事实写定论。
- 使用占位符：
  - `[REF_NEEDED: claim/topic]`
  - `[FIGURE_NEEDED: figure purpose | placement | why missing]`
  - `[TABLE_NEEDED: table purpose | required columns | why missing]`
  - `[RESULT_NEEDED: experiment/metric/source]`
  - `[RESULT_UNVERIFIED: claim | why not verified]`
  - `[METHOD_DETAIL_NEEDED: description]`
  - `[RATIONALE_NEEDED: module | missing design reason / benefit / tradeoff]`
  - `[DATASET_DETAIL_NEEDED: description]`

**Method section 最小完备要求**：
- 先给整体框架说明，在应放置总架构图的位置插入图占位
- 为每个核心模块单列小节
- 每个模块写出：目的、输入/输出或张量维度、核心操作、至少一个关键公式或伪公式
- 对每个核心模块，叙述顺序为：(1) 在流水线中的职责 (2) 为何需要存在 (3) 为什么采用这种设计 (4) 核心机制与公式 (5) 预期收益 (6) 边界与代价
- 标准/支撑性组件简写为：作用 + 输入输出 + 核心操作
- 若设计动机只能有限推断，正文必须显式降级语气，使用"该设计意在……""从实现结构看……"等保守表述

参考文献列表只能包含正文中被引用或以 `[REF_NEEDED: ...]` 声明的条目。

### Step 7: Prose Quality Gate

→ 委托 `academic-polishing` 执行。

输入：Draft v1 文本、当前 section 类型。
输出：prose_debt (open|closed)、failed_items、改写后文本。若当前为 Method，还包含 method_prose_debt。

Prose Rewrite 循环最多 2 轮。2 轮后仍未通过，保留 prose_debt: open，继续后续步骤但最终 Verification 不得判为 passed。

### Step 8: Expansion Pass（内容密度检查）

检查当前 section 是否仍过薄。详细阈值见 `references/content-density.md`。

以下情况视为过薄（thin_draft: yes）：
- Introduction ≤ 2 段，或只有背景+贡献列表
- Related Work 仅罗列论文名，无 work clusters 和综合比较
- Method 仅概述段，无模块拆解和公式
- Experimental Setup 仅参数罗列，无协议与风险说明
- Discussion/Conclusion 仅泛泛而谈，无边界分析

扩写原则：只用已有证据和合规占位符扩充，优先补足"读者理解链条"。

### Step 9: Self-Review & Verification

→ 委托 `academic-reviser` 执行。

输入：Expanded Draft、Evidence Map、前序步骤状态（prose_debt、thin_draft、frozen_claims 等）。
输出：按 `../shared/schemas/verification-report.md` 组织：Self-Review、Revised Draft vN（必须吸收修改点）、Section Critique、Verification Status（passed/failed/blocked）。

若 Verification 判定为 blocked，必须含 safe_to_continue 和 frozen_claims。只有 safe_to_continue = yes 时才允许推进到下一节。

### Step 10: 整合 & section loop

对 full-paper-planning 任务，不得在一个 section 修订完就结束：

- 若 failed 且非外部阻塞 → 保持当前 section 为活跃项，继续下一轮 Step 9
- 若 blocked 且 safe_to_continue = yes → 将阻塞点写入 Revision Queue，冻结 claims 后前进
- 若 blocked 且 safe_to_continue = no → 保持活跃，等待外部证据闭合
- 将其并入 Cumulative Draft，更新 Section Queue 和 Revision Queue

继续推进直到：
- 核心章节已形成 substantial draft
- 遇到阻塞性证据缺口且继续会显著增加幻觉风险
- 用户明确要求暂停

## 跨技能数据契约

本 Skill 与其委托的子 Skill 之间通过规范化数据契约交换信息。数据契约定义在 `../shared/schemas/` 中：

| 契约 | 生产者 → 消费者 | 用途 |
|------|----------------|------|
| `../shared/schemas/evidence-inventory.md` | `academic-experiments`, Step 2 → Step 6 | 实验证据盘点数据 |
| `../shared/schemas/verified-references.md` | `academic-citation` → Step 6 | 核验后的文献引用数据 |
| `../shared/schemas/verification-report.md` | `academic-reviser` → Step 10 | 审修验证状态数据 |

共享参考文件在 `../shared/references/` 中：

| 文件 | 用途 |
|------|------|
| `../shared/references/evidence-classification.md` | 三类证据的定义与使用规范 |
| `../shared/references/placeholder-guide.md` | 占位符系统规范 |
| `../shared/references/paper-types.md` | 论文类型定义与选择方法 |

## 何时读取 references/

| Reference 文件 | 打开条件 |
|---------------|---------|
| `references/paper-structure.md` | 确定章节结构、各节目标时 |
| `references/writing-guidelines.md` | 确认 venue 风格适配时 |
| `references/iteration-control.md` | 进入 Draft → Revision → Verification 循环时 |
| `references/content-density.md` | 执行 Expansion Pass（Step 8）时 |
| `references/exemplar-sections/` | 写 Introduction / Related Work / Method / Experiments / Abstract 前 |
| `references/test-scenarios.md` | 修改 Skill 后做回归验证时 |
| `../shared/schemas/evidence-inventory.md` | Step 4 接收实验证据时 |
| `../shared/schemas/verified-references.md` | Step 3 接收文献引用时 |
| `../shared/schemas/verification-report.md` | Step 9 接收审修结果时 |
| `../shared/references/evidence-classification.md` | Step 2 审计证据时 |
| `../shared/references/placeholder-guide.md` | Step 6 生成 Draft 使用占位符时 |
| `../shared/references/mode-spectrum.md` | 选择或理解任务模式时（Step 0） |
| `../shared/references/data-access-levels.md` | 理解跨技能数据访问边界时 |

## 不适用场景

本 Skill 不适用于：
- 非 CS/AI/ML 领域的论文（如纯实验生物学、临床医学、人文社科）
- 已有完整 LaTeX 稿只需排版调整的场景
- 用户明确要求单次生成整篇论文且拒绝分节推进的场景（此时仍不能跳过证据检查）

## 失败处理

- **文献搜不到**：如实报告"未找到足够可靠来源"，不补假引文。
- **代码跑不通**：报告阻塞点、环境需求、已尝试命令，不伪造结果。
- **运行成本过高**：优先退回 preexisting_artifact 盘点或最小复核。
- **证据不足**：降级为带占位符的 section 草稿，说明当前不能下哪些结论。
- **用户要求一次成稿**：仍优先先给 Outline / Section Queue，随后分节推进。

## Anti-Patterns

| 模式 | 问题 | 正确做法 |
|------|------|---------|
| 跳过证据审计 | 不盘点证据直接开写 | 必须 Step 2 完成证据审计后再 Step 6 起草 |
| 批量输出整篇 | 同时多节起草导致证据一致性差 | 分节推进，逐节完成 Draft→Quality→Verification 闭环 |
| Abstract 前置 | 证据未稳时就先写 Abstract | Abstract 必须后置，等主体章节证据稳定后再写 |
| 无证据式 SOTA | 未与强基线比较就声称 SOTA | 任何 SOTA / state-of-the-art 表述必须附 baseline 比较表 |
| 自我审查赦免 | 因接近截止期就缩短审查流程 | Hard Gates 不可跳过，每种核实步骤都至少执行一遍 |
