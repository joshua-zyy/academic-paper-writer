# Orchestration Workflow — Part 1: Preparation (Step 0–4)

本文件包含编排器 Step 0–4 的详细执行流程。按需加载，避免一次性加载全部步骤。

完整步骤索引见 `orchestration-workflow.md`。

---

## 执行约束（硬性规则）

- **主 Agent 只撰写论文文本，绝对不得修改项目源代码、配置文件或数据文件**。探查时只读，图表代码生成时创建新文件而非覆盖现有文件。
- 子 Agent 的约束见各自 `agents/xxx_agent.md` 中的 Red Lines。
- 论文正文（Introduction / Related Work / Method / Experiments / Discussion / Conclusion / Abstract）由主 Agent **直接撰写**，不 dispatch 独立写作子代理，以确保叙事风格一致。

---

## Step 0: Mode, Scope, and Current Section

- Determine whether the task is full-paper planning, single-section drafting, revision, citation pass, or experiment pass.
- If the user names a section, set it as the current section unit.
- If the user asks to "write a paper," form an Outline / Section Queue and enter the serial section loop.
- For `full-paper-planning`, maintain two lists: Section Queue (pending) and Revision Queue (drafted but needs revision).

## Step 1: Confirm Key Information (Blocking Gate)

Blocking confirmations — must stop and ask if missing:

1. **Target venue**: **Blocking requirement** for `full-paper-planning`, formal drafting, or substantial revision.
   - **Do not proceed to Step 2 until venue is confirmed.** This is a hard block.
   - If user says "undecided": provide 2-3 venue suggestions and ask user to confirm or specify.
   - If user explicitly declines to specify: record `venue = user_declined`, warn that "generic structure may not meet specific venue requirements," and require explicit user acknowledgment before proceeding.
   - Only if user explicitly says "you decide" may the agent autonomously select a venue and inform the user.
   - **一次性确认**：venue 确认后全程不再重复询问，后续 section 无需再次确认。
2. **Draft language**: Required for formal drafting. Default to English if not specified.
   - **一次性确认**：语言确认后全程不再重复询问。
3. **Continuation mode**: Default to `auto` (automatic section advancement). If user prefers step-by-step confirmation, record `continuation_mode = step-by-step`.
4. **Current section**: Determined by Step 0 if user did not specify.

If venue is known and relevant, read `references/writing-guidelines.md` and form a brief Venue / Language Brief.

**Failure to confirm venue**: Stop and wait. Do not proceed to Step 2. Do not generate Outline or Section Queue until venue is resolved.

## Step 2: Evidence Audit

Create a todo list for evidence items. Dispatch probe agents per section type.

### 并行 dispatch 规则（强制）

所有 probe_type 均设计为**独立可并行**——它们只读文件系统、不产生副作用、不共享状态。
因此，在以下情况下**必须使用并行 dispatch**，而非串行：

| 场景 | 可并行的探查 | 执行方式 |
|------|-------------|---------|
| Method 分析 | `code_structure` + `preprocessing` | **必须并行**（二者互不依赖，探查不同层面） |
| 轻量全量扫描 | code structure + data & artifacts + config | **必须并行**（Phase 1 的三个探查完全独立） |
| 其他场景 | 单个 probe | 单 subagent |

**并行执行方式（正确 vs 错误）：**

```
✅ 正确 — 在一个消息中同时发出多个 Task 调用
   Task(code_structure) + Task(preprocessing)
   两者同时运行，互不等待

❌ 错误 — 串行等待
   Task(code_structure) → 等待返回 → Task(preprocessing)
   不必要地将探查时间翻倍
```

### 平台不支持并行时的降级

若当前运行环境不支持同时 dispatch 多个子 Agent，按以下顺序串行执行：

```
Method 场景:
  1. code_structure（优先——影响 Method 结构）
  2. preprocessing
  合并结果时标注 dispatched_sequentially: true，不影响下游步骤

Phase 1 轻量扫描:
  1. code structure
  2. data & artifacts
  3. config
```

### 单探查 dispatch 模板

适用于只涉及一个 probe_type 的场景（如 Introduction → existing_material）：

```yaml
Task:
  description: "Probe {probe_type} for {section_type}"
  subagent_type: "general"
  prompt: |
    你已加载 probe-agent 模板。按照以下要求执行。

    Role: 项目探查代理（只读）

    probe_type: {probe_type}
    target_path: <项目根目录>
    section_type: {section_type}

    加载并执行 skills/academic-paper-writer/agents/probe-agent.md 中对应 probe_type 的 schema。
    输出对应 probe_type 的结构化结果。若目标路径不存在，在 blocked_items 中列出。

    Red Lines（硬性约束）:
    1. 只读——禁止修改任何项目文件。绝对不得创建、修改、删除、重命名任何文件。
    2. 找不到就标记 null，不编造
    3. 只探查指定路径及其直接子目录，不递归全仓库

    返回: 按对应 probe schema 的结构化结果
```

### 并行 dispatch 模板（强制并行）

适用于涉及多个 probe_type 的场景（如 Method → code_structure + preprocessing）。
**必须同时发出以下所有 Task，不得串行：**

```yaml
# ===== 同时发出，互不等待 =====

Task A:
  description: "Probe code_structure for Method"
  subagent_type: "general"
  prompt: |
    你已加载 probe-agent 模板。按照以下要求执行。

    Role: 项目探查代理（只读）
    probe_type: code_structure
    target_path: <项目根目录>
    section_type: method

    加载 skills/academic-paper-writer/agents/probe-agent.md 的 code_structure 探查 schema。
    产出 Module Cards 表 + 张量形状。区分 artifact-verified / inferred-from-gap / missing。

    Red Lines（硬性约束）:
    1. 只读——禁止修改任何项目文件
    2. 找不到就标记 null，不编造
    3. 不递归遍历整个仓库

    返回: 结构化 Module Cards

Task B:
  description: "Probe preprocessing for Method"
  subagent_type: "general"
  prompt: |
    你已加载 probe-agent 模板。按照以下要求执行。

    Role: 项目探查代理（只读）
    probe_type: preprocessing
    target_path: <项目根目录>
    section_type: method

    加载 skills/academic-paper-writer/agents/probe-agent.md 的 preprocessing 探查 schema。
    输出预处理步骤列表。

    Red Lines（硬性约束）:
    1. 只读——禁止修改任何项目文件
    2. 找不到就标记 null，不编造
    3. 不递归遍历整个仓库

    返回: 结构化预处理步骤列表
```

两个 Task 都返回后，合并结果为完整的 Evidence Map。

### 探查与 section 的对应关系

| Section | Probe tasks | 并行策略 |
|---------|-------------|---------|
| Introduction | `existing_material` | 单探查 |
| Related Work | `existing_material` | 单探查 |
| Method | `code_structure` + `preprocessing` | **必须并行** |
| Experimental Setup | `experiment_setup` | 单探查 |
| Main Results | `experiment_results` | 单探查 |
| Ablation | `experiment_results` | 单探查 |
| Discussion | `interpretability` | 单探查 |

### 汇总 Evidence Map

After probes return, aggregate into an Evidence Map. Light-weight, section-targeted inventory only.

Determine paper type: empirical / theory / survey / reproducibility / position.

List four categories:
- Known facts
- Missing but blocking facts
- Missing but placeholder-acceptable facts
- Claims needing external validation

### 探查策略：轻量全量探查 + 按需深度探查（混合策略）

首次执行 full-paper-planning 时，Step 2 采用**混合探查策略**：

**Phase 1 — 轻量全量探查（Step 2 执行，必须并行 dispatch）：**
同时 dispatch 以下 3 个轻量探查任务（每个只需读取目录级信息和配置文件）。**必须同时发出，不得串行：**

```yaml
# ===== 同时发出，互不等待 =====

Task A:
  description: "Project overview: code structure"
  subagent_type: "general"
  prompt: |
    只读探查——列出项目的模块清单、文件组织方式、核心类/函数签名。
    目标路径: <项目根目录>

    输出:
    - 文件结构摘要（模块名、文件路径）
    - 核心代码模块列表（model.py、dataset.py、train.py 等）
    - 各模块的职责（1-2 句）

    Red Lines:
    1. 只读——禁止修改任何文件
    2. 只探查顶层目录和直接子目录，不递归进 __pycache__/ .git/ 等

Task B:
  description: "Project overview: data & artifacts"
  subagent_type: "general"
  prompt: |
    只读探查——定位数据集 CSV、checkpoint 文件、日志文件、配置文件的路径。
    目标路径: <项目根目录>

    输出:
    - 实验产出目录列表（如 AD_NC/、EMIC_LMCI/）
    - 每个目录下的文件类型（best_model.pth、checkpoints、explain_outputs 等）
    - 是否存在训练日志、指标 CSV、可解释性结果

    Red Lines:
    1. 只读——禁止修改任何文件

Task C:
  description: "Project overview: config"
  subagent_type: "general"
  prompt: |
    只读探查——读取 config.py 等关键配置文件，提取超参数摘要。
    目标路径: <项目根目录>

    输出:
    - 关键超参数列表（学习率、batch size、epochs、hidden_dim 等）
    - 路径配置（数据目录、输出目录）

    Red Lines:
    1. 只读——禁止修改任何文件
```

3 个探查全部返回后，汇总为 **Project Overview**，作为 Evidence Map 的索引层。

**Phase 2 — 按需深度探查（各 section 起草前 dispatch）：**
以下深层探查**不在此阶段执行**，而是推迟到对应 section 起草前 dispatch：

| Section 起草前 | dispatch 的深层探查 | 并行策略 |
|---------------|-------------------|---------|
| Method | `code_structure`（逐模块 Module Cards、张量形状、forward 路径） | **与 preprocessing 并行** |
| Method | `preprocessing`（数据预处理详细步骤） | **与 code_structure 并行** |
| Experimental Setup | `experiment_setup`（超参数、数据集划分、人口统计） | 单探查 |
| Main Results | `experiment_results`（主结果、基线对比、消融数值） | 单探查 |
| Ablation | `experiment_results`（消融实验数值） | 单探查 |
| Discussion | `interpretability`（可解释性结果、网络重要性） | 单探查 |

每个深层探查使用上方的并行或单探查 dispatch 模板，传入对应 probe_type。

For Introduction / Related Work, also audit exemplar paper candidates.
For Method, also audit model data flow, module boundaries, tensor shapes, recoverable formulas.

## Step 3: Literature Search and Verification

- Create a todo list for keywords and expected reference counts.
- Determine search keywords and scope (e.g., task_name, method_family, dataset).
- Delegate to `academic-citation` via the dispatch template below.
- Mark todo completed after return.

**Dispatch template：**
```yaml
Task:
  description: "文献检索 - {section}"
  subagent_type: "general"
  prompt: |
    你已加载 academic-citation 子 Skill（skills/academic-citation/SKILL.md）。

    任务: 为 {section} 执行文献检索与核验
    关键词: {keywords}
    目标 venue: {venue}

    执行步骤:
    1. 读取 skills/academic-citation/SKILL.md，按 Step 1-6 执行
    2. 至少覆盖 4 类查询：问题导向 / 方法导向 / 基线导向 / 时间导向
    3. 逐篇核验元数据，优先一级来源（official proceedings、DOI）
    4. 完整论文至少 8-15 篇 VERIFIED 文献，短论文至少 4-8 篇
    5. Introduction/Related Work 时额外构建 Exemplar Set（3-5 篇）
    6. 输出时同时输出 Citation-to-Claim Map

    输出:
    - Verified References（含 VERIFIED/UNVERIFIED 状态、来源链接）
    - Exemplar Set（Introduction/Related Work 时必选）
    - Citation-to-Claim Map（每篇引用→对应主张的映射）
    - Missing References（[REF_NEEDED: ...] 方向列表）

    约束: 遵循 academic-citation SKILL.md 中的 Red Lines

    返回: 结构化输出
```

Input: current section, research keywords, target venue.
Output: Verified References, Exemplar Set (for Intro/RW), Citation-to-Claim Map per `academic-citation/references/schemas/verified-references.md`.

Constraint: only VERIFIED references enter the draft body. UNVERIFIED entries stay in candidate lists.

For Introduction / Related Work: if retries still produce zero VERIFIED references and the user cannot provide usable seed papers, block before Step 6. Do **not** proceed with a `[REF_NEEDED]`-only draft for these sections.

## Step 4: Experiment Evidence Verification

- Create a todo list for experiment evidence items.
- Delegate to `academic-experiments` via the dispatch template below (only when empirical paper and current section needs experiment facts).

**Dispatch template：**
```yaml
Task:
  description: "实验复核 - {section}"
  subagent_type: "general"
  prompt: |
    你已加载 academic-experiments 子 Skill（skills/academic-experiments/SKILL.md）。

    任务: 对项目路径 {repo_path} 执行实验证据盘点与复核
    当前 section: {section}
    目标 venue: {venue}

    执行步骤:
    1. 读取 skills/academic-experiments/SKILL.md，按 Step 1-5 执行
    2. 先盘点已有产物（preexisting_artifact）：checkpoint、日志、CSV、配置文件
    3. 优先评估已有 checkpoint（最小可复核命令），不重训
    4. 确有必要才尝试运行，运行前置验证环境
    5. 每条结果必须标注 evidence_type（newly_run / preexisting_artifact / user_claim）
    6. 评估协议风险（数据泄漏、验证集调参、基线缺失、单次运行等）

    输出:
    - Evidence Inventory（含 evidence_type 标注）
    - Protocol Risks（逐项列出风险类型与严重程度）
    - Remaining Blockers（可执行/数据/环境缺失）

    约束: 遵循 academic-experiments SKILL.md 中的 Red Lines

    返回: 结构化输出
```

Input: repo path, current section.
Output: Experiment Evidence, Protocol Risks, Remaining Blockers per `academic-experiments/references/schemas/evidence-inventory.md`.

Introduction / Related Work do not block on this step.
