# Orchestration Workflow — Step-by-Step Reference

This file contains the detailed step-by-step workflow for the core orchestrator.
Load this when executing the section drafting loop.

This file is the single detailed execution manual for the core orchestrator. When `SKILL.md` provides only summaries, follow the exact procedures, templates, and fallback paths defined here.

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
2. **Draft language**: Required for formal drafting. Default to English if not specified.
3. **Current section**: Determined by Step 0 if user did not specify.

If venue is known and relevant, read `references/writing-guidelines.md` and form a brief Venue / Language Brief.

**Failure to confirm venue**: Stop and wait. Do not proceed to Step 2. Do not generate Outline or Section Queue until venue is resolved.

## Step 2: Evidence Audit

Create a todo list for evidence items. Dispatch probe agents per section type (parallel when multiple probes are needed):

| Section | Probe tasks |
|---------|-------------|
| Introduction | `existing_draft` |
| Related Work | `existing_draft` |
| Method | `code_structure` + `preprocessing` |
| Experimental Setup | `data_statistics` + `experiment_config` |
| Main Results | `experiment_data` + `baseline_results` |
| Ablation | `ablation_results` |
| Discussion | `interpretability` |

Single probe: dispatch one general subagent with the template below.
Multiple probes: dispatch multiple subagents simultaneously (inter‑independent), each with its own template.

**Dispatch template — 单探查任务：**
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

**Dispatch template — 并行多探查任务（如 Method → code_structure + preprocessing）：**
```yaml
# 同时 dispatch，互不等待，不共享上下文
Task ①:
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

Task ②:
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

After probes return, aggregate into an Evidence Map. Light-weight, section-targeted inventory only.

Determine paper type: empirical / theory / survey / reproducibility / position.

List four categories:
- Known facts
- Missing but blocking facts
- Missing but placeholder-acceptable facts
- Claims needing external validation

### 探查策略：轻量全量探查 + 按需深度探查（混合策略）

首次执行 full-paper-planning 时，Step 2 采用**混合探查策略**：

**Phase 1 — 轻量全量探查（Step 2 执行，并行 dispatch）：**
同时 dispatch 以下 3 个轻量探查任务（每个只需读取目录级信息和配置文件）：

```yaml
Task ①:
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

Task ②:
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

Task ③:
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

3 个探查返回后，汇总为 **Project Overview**，作为 Evidence Map 的索引层。

**Phase 2 — 按需深度探查（各 section 起草前 dispatch）：**
以下深层探查**不在此阶段执行**，而是推迟到对应 section 起草前 dispatch：

| Section 起草前 | dispatch 的深层探查 |
|---------------|-------------------|
| Method | `code_structure`（逐模块的 Module Cards、张量形状、forward 路径） |
| Method | `preprocessing`（数据预处理详细步骤） |
| Experimental Setup | `data_statistics`（受试者级人口统计） |
| Experimental Setup | `experiment_config`（评估协议、划分方式、超参数） |
| Main Results | `experiment_data`（具体数值：ACC/AUC/F1） |
| Main Results | `baseline_results`（基线对比数据） |
| Ablation | `ablation_results`（消融实验数值） |
| Discussion | `interpretability`（可解释性结果、网络重要性） |

每个深层探查使用 Step 2 中定义的 dispatch 模板，传入对应 probe_type。

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

    Red Lines:
    1. 只检索——禁止修改项目中的任何文件
    2. 禁止编造文献、作者、年份、venue、DOI、arXiv 编号
    3. 禁止把 UNVERIFIED 当作 VERIFIED 写入正文
    4. 禁止因"搜索结果第一页看完了"就停止检索
    5. 禁止只引与自己最相似的方法而忽略强基线
    6. 搜索引擎不可用时如实报告，不得伪造

    返回: 结构化输出
```

Input: current section, research keywords, target venue.
Output: Verified References, Exemplar Set (for Intro/RW), Citation-to-Claim Map per `../shared/schemas/verified-references.md`.

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

    Red Lines:
    1. 可运行实验/评估脚本，但禁止修改源代码/数据文件/配置文件
    2. 禁止编造实验结果
    3. 禁止把 user_claim 当作可直接引用的证据
    4. 禁止把领域默认值写成当前项目已确认事实
    5. 禁止因运行受阻就把旧数字重新包装为已验证结果
    6. 若需安装依赖，必须经用户明确同意

    返回: 结构化输出
```

Input: repo path, current section.
Output: Experiment Evidence, Protocol Risks, Remaining Blockers per `../shared/schemas/evidence-inventory.md`.

Introduction / Related Work do not block on this step.

## Step 5: Generate Section Plan

- Create a todo list for plan core modules.
- Read `references/paper-structure.md` and select structure by paper type and venue.
- Generate Evidence Map: section goal, key claims, evidence sources, gaps.

**Introduction / Related Work must generate a Section Blueprint**:
- Exemplar Set observed structures
- Functional units or work clusters to retain
- Narrative duty per paragraph or subsection
- Dense citation spots vs. synthesis spots
- Differentiation from exemplars

**Method sections must generate a Method Blueprint**:
- Recommended subsection order
- Architecture figure placement and intent
- Core vs. standard modules
- Module Card per core module: position, bottleneck, design choice, rationale, expected benefit, cost/limit/boundary, evidence source

## Step 6: Draft v1

- Create a todo list for subtopics to cover.
- Check Evidence Map and Verified References.
- Generate Draft v1 Markdown body.
- Mark todos completed.

Body constraints:
- Paper Body = draft text only; critique/audit notes go to sidecar.
- Only use verified references and confirmed experiment facts for definitive claims.
- **Evidence type annotation**: Every numerical result in body must be annotated with its evidence type:
  - `newly_run` results: append "(newly_run, YYYY-MM-DD)" or similar timestamp
  - `preexisting_artifact` results: append "(preexisting_artifact, source: path/to/file)"
  - Example: "accuracy 86.58% (newly_run, 2026-05-10)" or "AUC 0.9314 (preexisting_artifact, experiments/run_logs/exp001.log)"
- Placeholders:
  - `[REF_NEEDED: claim/topic]`
  - `[FIGURE_NEEDED: purpose | placement | why]`
  - `[TABLE_NEEDED: purpose | columns | why]`
  - `[RESULT_NEEDED: experiment/metric/source]`
  - `[RESULT_UNVERIFIED: claim | why]`
  - `[METHOD_DETAIL_NEEDED: description]`
  - `[RATIONALE_NEEDED: module | missing]`
  - `[DATASET_DETAIL_NEEDED: description]`
  - `[ABSTRACT_NEEDED: 待主要证据稳定后撰写]`

**Method section minimum requirements**:
- Overall framework first, with architecture figure placeholder at proper position.
- Separate subsection per core module.
- Per module: purpose, input/output or tensor dims, core operation, at least one key formula or pseudo-formula.
- Narrative order per core module: (1) pipeline duty (2) why needed (3) why this design (4) core mechanism & formula (5) expected benefit (6) boundary & cost.
- Standard/supporting components: role + input/output + core operation only.
- If design motive is only weakly inferable, downgrade tone explicitly (e.g., "该设计意在...", "从实现结构看...").

Reference list must only contain entries cited in body or declared via `[REF_NEEDED: ...]`.

## Step 7: Placeholder Audit, Architecture Figure Pre-generation, and Debt List（**强制执行，不可跳过**）

After Draft v1, **必须**自动执行以下 5 个子步骤：

### 7a. 扫描全文占位符
统计并分类所有占位符的数量、位置与内容：
- `[FIGURE_NEEDED]`、`[TABLE_NEEDED]`、`[RESULT_NEEDED]`、`[REF_NEEDED]`、`[METHOD_DETAIL_NEEDED]`、`[DATASET_DETAIL_NEEDED]`、`[RATIONALE_NEEDED]`

### 7b. 填补遗漏的架构图占位符（**必须**）
对 Method 节进行结构分析，主动补入缺失的图占位：
- 扫描 Method 节中每个独立模块标题（如 "###"、"####" 或 "1) ..." 等）
- 检查该模块附近是否已有 `[FIGURE_NEEDED]` 占位符
- 若缺失，**必须**在该模块段落末尾插入：
  ```
  [FIGURE_NEEDED: 图X <模块名>模块图 | 对应小节 | 展示内部结构、输入输出与数据流]
  ```
- **不得因"模块描述较清晰"而跳过架构图占位符**

### 7c. 自动触发架构图生成
对每个 `[FIGURE_NEEDED]` 按用途分类处理：
- **架构图类**（purpose 含 architecture / structure / pipeline / diagram / network / flow / 架构 / 模块图 等）：
  按下文 Step 7 的 dispatch 模板委托 `academic-figure` 的 arch-prompt 模式，用生图提示词替换原占位符
- **数据图类**（purpose 含 curve / comparison / ablation / 曲线 / 对比 等）：
  保留占位符，记入待补项列表

### 7d. 追加待补项清单（**必须，不可省略**）
在 Draft v1 末尾（参考文献之后）**必须**追加以下内容。即使某类占位符不存在也要列出（标记为「无」）：

```markdown
---

## 附：待补项清单

*以下内容不作为正式正文，仅作为草稿状态内部记录。*

### 仍待补项

1. [FIGURE_NEEDED] <汇总所有数据图类占位符，逐项列出用途>
2. [TABLE_NEEDED] <汇总所有表格类占位符，逐项列出用途>
3. [RESULT_NEEDED] <汇总所有结果类占位符，逐项列出>
4. [REF_NEEDED] <汇总所有文献类占位符，逐项列出方向>
5. [METHOD_DETAIL_NEEDED] / [DATASET_DETAIL_NEEDED] / [RATIONALE_NEEDED] <如有>
6. （预处理细节补充、多随机种子/交叉验证、英文翻译等其他已知待补项）
```

### 7e. 报告审计结果
将占位符统计信息（`placeholder_debt`）纳入 Section Critique，供 Step 11 Verification 引用。

### 7f. 架构图 dispatch 模板
对架构图类的 `[FIGURE_NEEDED]`，按此模板 dispatch：

```yaml
Task:
  description: "生成架构图提示词 - {module_name}"
  subagent_type: "general"
  prompt: |
    你已加载 academic-figure 子 Skill（skills/academic-figure/SKILL.md）。

    任务: 以 arch-prompt 模式生成架构图生图提示词
    图用途: {从 [FIGURE_NEEDED] 的 purpose 字段提取}
    path: B

    执行步骤:
    1. 读取 skills/academic-figure/SKILL.md，按 B 路径（arch-prompt）执行
    2. 确认模型结构：核心组件列表、数据流方向、关键连接方式（残差/跨层注意力等）
    3. 输出结构化描述式提示词

    输出:
    - 架构分析说明（组件、数据流、连接方式）
    - 生图提示词（通用描述式语言，不含 --ar、--style 等工具参数）
    - 配色建议（学术色板 + 灰度安全）
    - 使用说明

    Red Lines:
    1. 禁止编造不存在的网络结构或模块连接
    2. 禁止在提示词中包含特定生图工具的硬编码参数
    3. 输出必须与代码/论文中的模块定义一致
    4. 禁止虚构数据来生成图表

    返回: 架构分析说明 + 生图提示词
```

## Step 8: Evidence Compliance Review (Phase 1 of Two-Phase Review)

- Create a todo list for evidence compliance checks.
- Delegate to `academic-reviser` in `targeted-evidence-mode` via the dispatch template below.
- Check `evidence_debt` status.

**Dispatch template：**
```yaml
Task:
  description: "证据合规审查 - {section}"
  subagent_type: "general"
  prompt: |
    你已加载 academic-reviser 子 Skill（skills/academic-reviser/SKILL.md）。

    任务: 对 {section} 执行证据合规审查（targeted-evidence-mode）
    Draft: <传入 Draft v1 文本>
    Evidence Map: <传入证据清單>
    Verified References: <传入已核验引用>
    placeholder_debt: <传入占位符统计>

    执行步骤:
    1. 读取 skills/academic-reviser/SKILL.md，按 targeted-evidence-mode 执行
    2. 检查每个 claim 是否在 Evidence Map 中有对应的 newly_run 或 preexisting_artifact 支撑
    3. 检查每个 inline citation 是否对应 Verified References 中已核验条目
    4. 检查所有占位符使用是否符合规范（如 [REF_NEEDED] 含方向说明）
    5. 检查是否存在无证据支撑的"裸 claim"

    输出: evidence_debt (open/closed) + evidence_issues 清单
    **不允许修改正文。**

    Red Lines:
    1. 只审查文本——禁止修改项目中的任何文件
    2. 禁止在 evidence_debt 未闭合时伪装为 closed
    3. 禁止删除占位符
    4. 禁止跳过检查顺序

    返回: 审查结果（evidence_debt + issues）
```

This is Phase 1. Only proceed to Phase 2 (prose polishing) after `evidence_debt = closed`.

Input: Draft v1 text, Evidence Map, Verified References, placeholder_debt from Step 7.
Output: `evidence_debt` (open|closed), `evidence_issues` list.

If protocol risks from Step 4 materially weaken a claim's support (for example: no independent test set, missing strong baselines, or single-run results used for strong conclusions), keep `evidence_debt = open` for that claim until the text is downgraded, the risk is made explicit, or the claim is frozen/blocked.

If `evidence_debt = open`, record issues and return to Step 6. Do not proceed to Step 9 while open.

## Step 9: Prose Quality Gate (Phase 2 of Two-Phase Review)

- Create a todo list for prose checks.
- Confirm Step 8 `evidence_debt = closed` before executing.
- Delegate to `academic-polishing` via the dispatch template below.

**Dispatch template：**
```yaml
Task:
  description: "Prose 质量门 - {section}"
  subagent_type: "general"
  prompt: |
    你已加载 academic-polishing 子 Skill（skills/academic-polishing/SKILL.md）。

    任务: 对 {section} 执行 Prose Quality Gate（含 Claim Strength Audit）
    Draft: <传入 Draft 文本>
    evidence_debt: {evidence_debt}
    section_type: {section_type}

    执行步骤:
    1. 读取 skills/academic-polishing/SKILL.md，按 Step 1-6 执行
    2. 若 evidence_debt = open，只修语法错误，不进行风格强化或措辞润色
    3. 执行通用检查 + 章节专项检查
    4. 执行 Claim Strength Audit
    5. 若为 Method 节，执行 Method Prose Rewrite
    6. Prose Rewrite 最多 2 轮，2 轮后仍 open 则保留状态继续

    Zero-Tolerance（零容忍触发词）——出现时必须检查 Strong 条件，不满足则强制降级:
    - "显著" / "significantly" → 无 p 值/效应量时必须降级
    - "稳定" / "robust" → 无多随机种子/交叉验证时必须降级
    - "作为" / "acts as" → 无因果干预实验时必须降级
    - "表明" / "demonstrates" → 不满足 Strong 条件时必须降级
    - "泛化" / "generalization" → 无独立测试集时必须降级
    - "SOTA" / "state-of-the-art" → 无完整基线对比时必须降级

    输出: prose_debt (open/closed) + failed_items + 改写后文本
    （Method 时额外输出 method_prose_debt）

    Red Lines:
    1. 只修改论文草稿文本——禁止修改项目中的任何文件
    2. 禁止把未核验的 user_claim 改写成确定性结论
    3. 禁止用华丽措辞掩盖 evidence gap
    4. Prose Rewrite 2 轮后不得假装 prose_debt = closed

    返回: 润色后文本 + prose_debt 状态
```

Input: Draft v1 text, current section type.
Output: `prose_debt` (open|closed), `failed_items`, rewritten text. For Method, also `method_prose_debt`.

Prose rewrite loop: max 2 rounds. If still open after 2 rounds, carry `prose_debt: open` forward; final Verification cannot be `passed`.

## Step 10: Expansion Pass (Content Density Check)

- Create a todo list for thin-draft checks.

Thin-draft conditions:
- Introduction <= 2 paragraphs, or only background + contribution list
- Related Work is just paper name listing, no work clusters or synthesis
- Method is only overview, no module breakdown or formulas
- Experimental Setup is only parameter listing, no protocol or risk notes
- Discussion / Conclusion is only generic statements, no boundary analysis

Expansion principle: use only existing evidence and compliant placeholders. Prioritize filling "reader understanding chain" gaps.

## Step 11: Self-Review & Verification

- Create a todo list for review items.
- Delegate to `academic-reviser` via the dispatch template below（full-section-review mode）.
- Check verdict and decide whether to advance or revise.

**Dispatch template：**
```yaml
Task:
  description: "综合验证 - {section}"
  subagent_type: "general"
  prompt: |
    你已加载 academic-reviser 子 Skill（skills/academic-reviser/SKILL.md）。

    任务: 对 {section} 执行完整三轮审查 + Verification（full-section-review）
    Draft: <传入 Expanded Draft>
    Evidence Map: <传入证据清單>
    prose_debt: {prose_debt}
    thin_draft: {thin_draft}
    frozen_claims: {frozen_claims}
    iteration_count: {iteration_count}

    执行步骤:
    1. 读取 skills/academic-reviser/SKILL.md，按 Step 1-6 执行
    2. 第一轮——证据与事实检查（13 项）
    3. 第二轮——论证强度与审稿风险检查（11 项）
    4. 第三轮——结构与风格检查（8 项）
    5. 生成 Revised Draft（必须真正吸收修改点）
    6. 输出 Section Critique + Verification Status

    Verification 判定规则（Gate C strict 模式）:
    - verdict = passed 仅当 prose_debt=closed 且 citation_debt=closed 且 evidence_debt=closed 且 figure_debt=closed 且 thin_draft=no
    - 任何 debt 未闭合 → verdict = blocked（禁止伪装为 passed）
    - blocked 时输出 safe_to_continue + frozen_claims

    输出的 Section Critique 必须明确:
    - 本节已解决的问题
    - 本节仍缺的证据
    - 剩余占位符统计
    - 下一节最合理的候选

    Red Lines:
    1. 只审查论文草稿——禁止修改项目中的任何文件
    2. 必须证据→论证→风格三轮顺序，不得先修风格再查事实
    3. 禁止在 debts 未闭合时判为 passed
    4. 禁止删除占位符而不补真实内容
    5. 禁止因草稿篇幅长就假设它足够可信

    返回: Section Critique + Revised Draft + Verification Status
```

Input: Expanded Draft, Evidence Map, prior step states (`prose_debt`, `thin_draft`, `frozen_claims`, etc.).
Output: Self-Review, Revised Draft vN (must absorb fixes), Section Critique, Verification Status (`passed`/`failed`/`blocked`) per `../shared/schemas/verification-report.md`.

If `blocked`, must include `safe_to_continue` and `frozen_claims`. Only advance if `safe_to_continue = yes`.

## Step 12: Integration & Section Loop (Dependency-Aware)

For `full-paper-planning`, do not end after one section revision.

### 12a. Status Update

- If `failed` and not externally blocked → keep current section active, continue next Step 11 round.
- If `blocked` and `safe_to_continue = yes` → write blockers to Revision Queue, freeze claims, advance.
- If `blocked` and `safe_to_continue = no` → keep active, wait for external evidence.
- Merge into Cumulative Draft; update Section Queue and Revision Queue.

### 12b. Dependency Check

After current section passes Verification, read `references/section-dependency-matrix.md`:

1. Read current section's `depended_by` list.
2. Check which sections in that list are already completed (exist in Cumulative Draft).
3. Check if `shared_claims` changed (compare original Evidence Map vs current draft).
4. If changed → mark corresponding section's `revision_queue` status as `pending`.
5. Before advancing, ask user: "This section changed X (claim), which section Y depends on. Revise Y first?"
   - User confirms → move Y to head of Section Queue.
   - User skips → Y keeps `pending`, auto-rechecked when Y is completed later.

### 12c. Select Next Section

Choose from sections whose `depends_on` are all satisfied and `revision_queue` has no `pending`:

Priority:
1. All `depends_on` completed
2. No `pending` recheck markers among them
3. User-specified section

Continue until:
- Core sections have substantial drafts
- Blocking evidence gaps would significantly increase hallucination risk
- User explicitly requests pause

### 12d. Abstract Generation (Hard Gate D)

Abstract is **not** in the initial Section Queue. It can only be generated after **all** of the following conditions are met:

1. All core sections (Introduction / Related Work / Method / Experiments / Discussion / Conclusion) are completed in Cumulative Draft
2. Each core section's Verification Status = `passed` (`blocked` is insufficient)
3. Main experimental results are stable (`evidence_debt = closed`)

If conditions are not met, retain `[ABSTRACT_NEEDED: 待主要证据稳定后撰写]` in the placeholder system. Do **not** output a complete Abstract.

When generating Abstract:
- It must reflect the actual content of the Cumulative Draft
- Any numerical results must be verified (`newly_run` or `preexisting_artifact`)
- Do not introduce new claims, methods, or terminology not present in the body
- Place Abstract at the beginning of the final Cumulative Draft output

---

## Shared Inputs and References

Cross-skill data contracts, shared concept references, and reference-loading guidance are maintained in `skills/academic-paper-writer/SKILL.md` as the high-level orchestrator index.

When executing a concrete step in this file:
- read the referenced schema under `../shared/schemas/` if the step consumes or produces structured cross-skill data
- read the referenced file under `references/` when that step explicitly calls for it
- use `../shared/references/` for shared evidence, placeholder, paper-type, mode-spectrum, and data-boundary concepts
