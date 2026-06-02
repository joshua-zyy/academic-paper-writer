# Orchestration Workflow — Part 2: Drafting (Step 5–6.5)

本文件包含编排器 Step 5–6.5 的详细执行流程。按需加载，避免一次性加载全部步骤。

完整步骤索引见 `orchestration-workflow.md`。

---

## Step 5: Generate Section Plan

- Create a todo list for plan core modules.
- Read `references/paper-structure.md` and select structure by paper type and venue.
- Read `references/section-writing-contracts.md` and create a Section Contract for each planned section: reader state before/after, required moves, evidence hooks, and section-specific failure checks.
- Generate Evidence Map: section goal, key claims, evidence sources, gaps.
- The Section Blueprint must map each paragraph/subsection to a required move in the contract. If a move lacks evidence, record the proper placeholder instead of silently omitting it.

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

## Two-Stage Writing Process

**Stage 1: Blueprint (Bullet Points)** — Step 5 输出
- 使用 bullet points 组织论点结构
- 标注关键引用位置
- 规划段落职责和论证顺序

**Stage 2: Draft v1 (Flowing Prose)** — Step 6 输出
- 将 bullet points 转换为完整段落
- 添加过渡句和逻辑连接
- 自然融入 inline citations（统一使用数字格式 `[1]`, `[2]`）
- 确保段落内因果/递进/转折的深层逻辑

**转换示例**：

Blueprint (Stage 1):
```
- Background: Transformer 在 NLP 中成功，但在 EEG 中应用有限
  * Cite: [1] Vaswani 2017 (attention), [2-4] Recent EEG-transformer attempts
- Gap: EEG 的时间-空间双重特性未被现有 transformer 充分建模
  * 现有方法只处理时间或空间，未联合建模
- Our approach: 双分支 transformer 联合建模时空特征
  * 时间分支: temporal self-attention
  * 空间分支: graph attention on electrode topology
```

Draft v1 (Stage 2):
```
The Transformer architecture has achieved remarkable success in natural
language processing since its introduction [1], yet its
application to electroencephalography (EEG) signals remains limited [2-4].
Unlike textual data, EEG recordings exhibit dual temporal-spatial
characteristics: temporal dynamics within each electrode channel and spatial
correlations across the electrode topology. Existing approaches typically
address only one of these dimensions—either applying temporal self-attention
to individual channels or using spatial graph convolution without modeling
temporal dependencies—leaving the joint spatiotemporal modeling problem
unresolved. To bridge this gap, we propose a dual-branch Transformer that...
```

## Step 6: Section Complete Loop — Phase 1: Drafting (6.0–6.3)

### Step 6.0: Section Contract Gate

- Create a todo list for subtopics to cover.
- **Section Contract Gate**: before writing prose, check the current Section Contract from Step 5. Draft v1 must satisfy the section's required moves or preserve explicit debt placeholders. If the contract is missing, return to Step 5 instead of drafting.

### Step 6.1: Pre-Draft Deep Probe

- **前置检查：是否需要深层探查** — 在起草前检查当前 section 类型，按以下规则决定是否需要 dispatch 深层探查：
  | 当前 section | 需 dispatch 的探查 | 并行策略 |
  |-------------|-------------------|---------|
  | Introduction | `existing_material`（项目已有材料）+ 本地文献深度探索 + 外部文献定向搜索 | **必须并行**（同时发出 3 个 Task） |
  | Related Work | `existing_material`（项目已有材料）+ 本地文献深度探索 + 外部文献定向搜索 | **必须并行**（同时发出 3 个 Task） |
  | Method | `code_structure`（Module Cards + 张量形状 + forward 路径）+ `preprocessing`（预处理步骤） | **必须并行** |
  | Experimental Setup | `experiment_setup`（超参数、数据集划分、人口统计） | 单探查 |
  | Main Results / Ablation | `experiment_results`（主结果、基线对比、消融数值） | 单探查 |
  | Discussion | `interpretability`（可解释性结果、网络分析） | 单探查 |
  - 需要探查 → **必须先 dispatch 再起草**，不得跳过。
  - 项目探查 dispatch 模板见 `references/workflow-step-0-4.md` 的 `### 单探查 dispatch 模板` 和 `### 并行 dispatch 模板（强制并行）`。
  - Introduction / Related Work 的文献深度探索模板见下方"Section 文献深度探索 dispatch 模板"。
  - Method 场景也可直接使用下方的内联模板。
  - 不需要 → 跳过，记录 "deep_probe: skipped"

**Method 深层探查内联 dispatch 模板（**必须同时发出，互不等待**）**：
```yaml
Task A:
  description: "Probe code_structure for Method"
  subagent_type: "general"
  prompt: |
    Role: 项目探查代理（只读）
    probe_type: code_structure
    target_path: <项目根目录>
    section_type: method
    加载 skills/academic-paper-writer/agents/probe-agent.md 的 code_structure schema。
    输出 Module Cards 表 + 张量形状。
    Red Lines: 只读，不编造，不递归全仓库。

Task B:
  description: "Probe preprocessing for Method"
  subagent_type: "general"
  prompt: |
    Role: 项目探查代理（只读）
    probe_type: preprocessing
    target_path: <项目根目录>
    section_type: method
    加载 skills/academic-paper-writer/agents/probe-agent.md 的 preprocessing schema。
    输出预处理步骤列表。
    Red Lines: 只读，不编造，不递归全仓库。
```
其他 section 类型的单探查 dispatch 见 `references/workflow-step-0-4.md` 的 `### 单探查 dispatch 模板`。

**Introduction 文献深度探索 dispatch 模板（**必须同时发出 3 个 Task，互不等待**）**：
```yaml
# ===== 同时发出以下 3 个 Task，互不等待 =====

Task A:
  description: "项目信息探查 - Introduction"
  subagent_type: "general"
  prompt: |
    你已加载 probe-agent 模板。按照以下要求执行。

    Role: 项目探查代理（只读）
    probe_type: existing_material
    target_path: <项目根目录>
    section_type: introduction

    加载 skills/academic-paper-writer/agents/probe-agent.md 的 existing_material schema。
    输出项目已有材料：研究目标、核心贡献、关键方法概述、已有草稿/笔记中的 Introduction 相关描述。

    Red Lines（硬性约束）:
    1. 只读——禁止修改任何项目文件
    2. 找不到就标记 null，不编造
    3. 只探查指定路径及其直接子目录

    返回: 结构化 existing_material 结果

Task B:
  description: "本地文献探索 - Introduction"
  subagent_type: "general"
  prompt: |
    你已加载 literature-reader-agent 模板。

    Role: 文献阅读代理（只读）
    section_type: introduction
    local_lit_md_dir: <local_lit_md_dir，若无则为 null>

    任务: 从本地文献库中搜索与 Introduction 高度相关的文献，并深度阅读。

    执行步骤:
    1. 扫描 local_lit_md_dir 中的 MD 文件，搜索与项目主题（task/method/domain）相关的论文
    2. 选取 3-5 篇最相关的论文进行全文阅读
    3. 按 skills/academic-citation/agents/literature-reader-agent.md 的 schema 输出 LiteratureReadingReport

    重点提取:
    - 领域背景和关键问题（Background）
    - 现有方法的共同假设与限制（Gap context）
    - Introduction 中常见的叙事结构（从论文中观察）
    - 可用于对比的 precedent works

    约束:
    1. 只读 + 只返回结构化内容，不修改、不创建、不写入、不删除任何文件
    2. 严格区分原文提取与推断
    3. 无本地文献库时返回"无本地文献"

    返回: 多篇 LiteratureReadingReport 的综合摘要

Task C:
  description: "外部文献搜索 - Introduction"
  subagent_type: "general"
  prompt: |
    你已加载 academic-citation 子 Skill（skills/academic-citation/SKILL.md）。

    Role: 文献检索代理
    section_type: introduction
    task_keywords: {项目任务描述、方法关键词、数据集关键词}
    target_venue: <venue>

    任务: 对外部文献库进行 Introduction 定向搜索。

    执行步骤:
    1. 读取 skills/academic-citation/SKILL.md，按 targeted-citation-search 模式执行
    2. 至少覆盖 4 类查询：
       - 问题导向: "<task> survey/review/state-of-the-art"
       - 方法导向: "<method family> for <task>"
       - 基线导向: "<task> baseline approaches"
       - 时间导向: "<task> 2024/2025/recent"
    3. 逐篇核验元数据（title/authors/venue/year/source link）
    4. 对高相关度论文尝试获取全文阅读

    输出:
    - Verified References（含 VERIFIED/UNVERIFIED 状态）
    - Exemplar Set（3-5 篇 Introduction exemplars）
    - Citation-to-Claim Map（每篇引用→对应 Introduction 中的主张）
    - 领域 gap 分析：现有方法共同的限制是什么？

    约束: 遵循 academic-citation Red Lines。不得编造引用。

    返回: 完整结构化输出
```

**Related Work 文献深度探索 dispatch 模板（**必须同时发出 3 个 Task，互不等待**）**：
```yaml
# ===== 同时发出以下 3 个 Task，互不等待 =====

Task A:
  description: "项目信息探查 - Related Work"
  subagent_type: "general"
  prompt: |
    你已加载 probe-agent 模板。按照以下要求执行。

    Role: 项目探查代理（只读）
    probe_type: existing_material
    target_path: <项目根目录>
    section_type: related_work

    加载 skills/academic-paper-writer/agents/probe-agent.md 的 existing_material schema。
    输出项目已有材料：核心贡献、关键区别点、与 baseline 的已知差异、已有草稿中的 Related Work 相关描述。

    Red Lines（硬性约束）:
    1. 只读——禁止修改任何项目文件
    2. 找不到就标记 null，不编造

    返回: 结构化 existing_material 结果

Task B:
  description: "本地文献探索 - Related Work"
  subagent_type: "general"
  prompt: |
    你已加载 literature-reader-agent 模板。

    Role: 文献阅读代理（只读）
    section_type: related_work
    local_lit_md_dir: <local_lit_md_dir，若无则为 null>

    任务: 从本地文献库中搜索与 Related Work 高度相关的文献，并深度阅读。

    执行步骤:
    1. 扫描 local_lit_md_dir 中的 MD 文件，搜索与项目方法相关、baseline 相关、数据集相关的论文
    2. 选取 4-8 篇最相关的论文进行全文阅读
    3. 按 skills/academic-citation/agents/literature-reader-agent.md 的 schema 输出 LiteratureReadingReport

    重点提取:
    - 可形成的工作簇（work clusters）：共享 idea + 代表工作 + 能力 + 限制
    - 最接近的竞争方法和精确差异
    - Related Work 中常见的组织方式（按技术路线/按任务/按限制类型）

    约束:
    1. 只读 + 只返回结构化内容，不修改、不创建、不写入、不删除任何文件
    2. 严格区分原文提取与推断
    3. 无本地文献库时返回"无本地文献"

    返回: 多篇 LiteratureReadingReport 的综合摘要（含工作簇分类建议）

Task C:
  description: "外部文献搜索 - Related Work"
  subagent_type: "general"
  prompt: |
    你已加载 academic-citation 子 Skill（skills/academic-citation/SKILL.md）。

    Role: 文献检索代理
    section_type: related_work
    task_keywords: {项目方法名称、技术路线关键词、baseline 名称}
    target_venue: <venue>

    任务: 对外部文献库进行 Related Work 定向搜索。

    执行步骤:
    1. 读取 skills/academic-citation/SKILL.md，按 targeted-citation-search 模式执行
    2. 至少覆盖 4 类查询：
       - 方法簇导向: "<method cluster> papers"
       - 竞争方法导向: "<competing method> for <task>"
       - 基线导向: "<baseline> comparison <task>"
       - 最新导向: "related work <task> 2024/2025"
    3. 逐篇核验元数据
    4. 对高相关度论文尝试获取全文阅读

    输出:
    - Verified References（至少 8-15 篇 Related Work 候选）
    - Exemplar Set（4-8 篇 Related Work exemplars）
    - Citation-to-Claim Map（每篇引用→对应 Related Work 中的工作簇论述）
    - 工作簇分类建议 + 每簇的代表能力与限制

    约束: 遵循 academic-citation Red Lines。不得编造引用。

    返回: 完整结构化输出
```
### Step 6.2: Draft v1 Generation

- Check Evidence Map and Verified References.
- Generate Draft v1 Markdown body.
- Mark todos completed.

Body constraints:
- Paper Body = draft text only; critique/audit notes go to sidecar.
- Only use verified references and confirmed experiment facts for definitive claims.
- Draft paragraphs must follow the current Section Contract rather than generic templates. Fluent prose is not sufficient if reader state, required moves, evidence hooks, or failure checks remain unresolved.
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

### Step 6.3: Write Draft v1 to File

### 文件写入（强制）

Draft v1 生成后，**必须**立即将正文内容写入 `./docs/paper-drafts/paper_draft.md`。使用 Write 工具（首次）或 Edit 工具（追加/替换）更新文件。

**禁止在对话中输出完整 Draft 正文。** 对话中仅输出简短进度摘要：

> **{Section}**: Draft v1 已写入文件，进入审查阶段

---

### ⚠️ Section 完成门控（强制，每节必执行）

> **Draft v1 ≠ 初稿完成。** 只有完成 Step 6.4 → 6.9 全部子步骤后，当前 section 才算初稿完成，方可推进到下一节。

**本门控为概要清单。以下每个子步骤均有各自的详细执行清单**（如 6.4 有 6.4a→6.4h 八项子清单、6.6 有零容忍触发词规则等）。**仅勾选概要项而未执行详细子步骤，视为未完成。**

**以下清单必须在离开本节前逐项完成。任一未完成，禁止开始下一节。用户催促时也不得跳过 6.4→6.9 审查阶段。**

- [ ] **6.4** 占位符审计 + 图表生成（详细清单: 6.4a→6.4h，即使无占位符也必须执行扫描）
- [ ] **6.5** 证据合规审查（Review Phase 1 — dispatch academic-reviser，`evidence_debt = closed` 方可继续）
- [ ] **6.6** Prose Quality Gate（Review Phase 2 — 内化调用 academic-polishing，含零容忍触发词规则）
- [ ] **6.7** Expansion Pass（内容密度检查，参考 `content-density.md` 的 thin draft 判定）
- [ ] **6.8** Self-Review & Verification（dispatch academic-reviser，verdict = passed 方可继续）
- [ ] **6.9** 更新 Cumulative Draft → 推进到下一节

**违反门控的典型错误**：Draft v1 写入文件后直接跳到下一节，跳过 6.4→6.9 审查阶段。
**正确行为**：Draft v1 写入 → 逐项按详细清单执行 6.4 → 6.5 → 6.6 → 6.7 → 6.8 → 6.9 → 然后才推进下一节。

---

## Step 6.4: Placeholder Audit, Figure Contract, Architecture Figure Pre-generation, and Debt List（**强制执行，不可跳过**）

**⚠️ 此步骤为硬性要求。即使 Draft v1 中没有任何占位符，也必须执行 6.4a（占位符扫描）和 6.4b（主动补入检查），确保没有遗漏图表。**

### Step 6.4 执行清单（必须逐项完成）

- [ ] **6.4a** 扫描全文占位符（统计 + 分类）
- [ ] **6.4b** 主动补入遗漏的图表占位符（不可跳过，即使无遗漏也要确认）
- [ ] **6.4c** 为每个 `[FIGURE_NEEDED]` 建立 Figure Contract
- [ ] **6.4d** 双路径图表处理（architecture → prompts，data → code）
- [ ] **6.4e** 追加待补项清单到 Draft 末尾
- [ ] **6.4f** 报告审计结果（`placeholder_stats`）
- [ ] **6.4g** Dispatch 架构图子代理（对每个架构图类占位符）
- [ ] **6.4h** Dispatch 数据图子代理（对每个数据图类占位符）

**未完成以上全部子步骤前，禁止进入 Step 6.5。**

---

After Draft v1, **必须**自动执行以下子步骤：

### 6.4a. 扫描全文占位符
统计并分类所有占位符的数量、位置与内容：
- `[FIGURE_NEEDED]`、`[TABLE_NEEDED]`、`[RESULT_NEEDED]`、`[REF_NEEDED]`、`[METHOD_DETAIL_NEEDED]`、`[DATASET_DETAIL_NEEDED]`、`[RATIONALE_NEEDED]`

### 6.4b. 主动补入遗漏的图表占位符（**必须**，不可跳过）
**适用范围**：Introduction、Related Work、Method、Experimental Setup、Main Results、Ablation、Discussion 等所有 section。

**检查规则**：对当前 section 进行结构分析，主动补入缺失的图占位：
- **Method 节**：扫描每个独立模块标题（如 "###"、"####" 或 "1) ..." 等），检查该模块附近是否已有 `[FIGURE_NEEDED]` 占位符。若缺失，**必须**在该模块段落末尾插入：
  ```
  [FIGURE_NEEDED: 图X <模块名>模块图 | 对应小节 | 展示内部结构、输入输出与数据流]
  ```
  **不得因"模块描述较清晰"而跳过架构图占位符。**
- **Main Results 节**：检查每个结果表/指标段落附近是否有对应的数据图占位符，若缺失则插入。
- **Ablation 节**：检查每个消融实验附近是否有对应的消融结果图占位符，若缺失则插入。
- **Introduction / Related Work / Discussion 节**：若结构上需要 overview figure 或 taxonomy figure，主动标记。

### 6.4c. Figure Contract（前置步骤，在生成任何图表之前**必须**完成）

对每个 `[FIGURE_NEEDED]` 占位符，在生成提示词或代码之前，**必须**先完成 Figure Contract：

1. **Core conclusion**：用一句话陈述该图必须捍卫的论点
2. **Evidence chain**：将每个计划面板映射到该论点，删除不承载独立证据的面板
3. **Archetype**：将图分类为 `quantitative grid`、`schematic-led composite`、`image plate + quant` 或 `asymmetric mixed-modality figure`
4. **Export contract**：设定最终尺寸、可编辑文本、源数据、统计信息、图像完整性说明和导出格式

### 6.4d. 双路径图表处理

对每个 `[FIGURE_NEEDED]` 按 Figure Contract 的分类结果进行双路径处理：

**arch-prompt 模式 — 架构图提示词**（purpose 含 architecture / structure / pipeline / diagram / network / flow / 架构 / 模块图 / framework / overview 等）：
- 按下文 Step 6.4g 的 dispatch 模板委托 `academic-figure` 的 arch-prompt 模式
- 生成的提示词写入 `./docs/paper-drafts/figures/figure_prompts.md`（按图编号分节）
- 正文中的占位符替换为图编号引用（如 `Figure X` 或 `图X`）
- 若 `./docs/paper-drafts/figures/figure_prompts.md` 不存在，使用 Write 工具创建；若已存在，使用 Edit 工具追加

**chart-from-data 模式 — 数据图绘图代码**（purpose 含 curve / comparison / ablation / result / 曲线 / 对比 / 消融 / 结果 / plot / chart / bar 等）：
- 按下文 Step 6.4h 的 dispatch 模板生成 Python 绘图代码
- 绘图代码写入 `./docs/paper-drafts/figures/codes/plot_fig{N}.py`
- 正文保留占位符，记入待补项列表
- **不自动执行绘图代码**（全文完成后 Step 9 统一批量执行）

### 6.4e. 追加待补项清单（**必须，不可省略**）
在 Draft v1 末尾（参考文献之后）**必须**追加以下内容。即使某类占位符不存在也要列出（标记为「无'）：

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

### 6.4f. 报告审计结果
将占位符统计信息（`placeholder_stats`）纳入 Section Critique，供 Step 6.8 Verification 引用。

### 6.4g. 架构图 dispatch 模板（arch-prompt 模式）
对架构图类的 `[FIGURE_NEEDED]`，按此模板 dispatch：

```yaml
Task:
  description: "生成架构图提示词 - {module_name}"
  subagent_type: "general"
  prompt: |
    你已加载 academic-figure 子 Skill（skills/academic-figure/SKILL.md）。

    任务: 以 arch-prompt 模式生成架构图生图提示词
    图用途: {从 [FIGURE_NEEDED] 的 purpose 字段提取}
    mode: arch-prompt

     Figure Contract:
    - Core conclusion: {Step 6.4c 中定义的论点}
    - Evidence chain: {面板→论点映射}
    - Archetype: {图分类}
    - Export contract: {尺寸、格式等}

    风格要求：参考 NeurIPS / CVPR / AAAI / ICLR 等顶会论文插图风格。
    详见 skills/academic-figure/references/architecture-prompting.md 的「顶会风格参考」。
    确保最终输出达到发表级质量。

    执行步骤:
    1. 读取 skills/academic-figure/SKILL.md，按 arch-prompt 模式执行
    2. 确认模型结构：核心组件列表、数据流方向、关键连接方式（残差/跨层注意力等）
    3. 按 skills/academic-figure/agents/figure_agent.md 中 arch-prompt 模式的 Output Schema 输出结构化结果

    Output Schema (arch-prompt 模式):
    ```yaml
    prompt: string              # 生图提示词（完整可执行的提示词文本，不得包含引用、占位符或 `[见...]` 类标记）
    figure_description:
      components: string[]      # 核心组件列表
      data_flow: string         # 数据流方向说明
      connections: string[]     # 关键连接方式
      annotations: string[]     # 标注要求
    ```

    约束:
    - 遵循 academic-figure SKILL.md 中的 Red Lines
    - `prompt` 字段必须包含完整可执行的提示词文本，不得使用引用或占位符替代

    返回: 严格按上述 YAML 格式输出，不附加任何额外文本
```

dispatch 返回后，从子代理返回的结构化输出中提取 `prompt` 字段的完整文本内容，原样写入 `./docs/paper-drafts/figures/figure_prompts.md`。**禁止**使用引用、指针或 `[见...]` 类占位符替代实际提示词文本。同时将正文中的占位符替换为图编号引用。

### 6.4h. 数据图绘图代码 dispatch 模板（chart-from-data 模式）
对数据图类的 `[FIGURE_NEEDED]`，按此模板 dispatch：

```yaml
Task:
  description: "生成数据图绘图代码 - {figure_id}"
  subagent_type: "general"
  prompt: |
    任务: 为 {figure_id} 生成 Python 绘图代码
    模式: chart-from-data
    图用途: {从 [FIGURE_NEEDED] 的 purpose 字段提取}
    数据来源: {实验数据路径或 Evidence Map 中的对应条目}

    Figure Contract:
    - Core conclusion: {Step 6.4c 中定义的论点}
    - Evidence chain: {面板→论点映射}
    - Archetype: {图分类}
    - Export contract: SVG

    绘图代码规范（强制）:
    1. 脚本最前面必须包含以下初始化:
       ```python
       import matplotlib as mpl
       import matplotlib.pyplot as plt
        mpl.rcParams.update({
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
            "svg.fonttype": "none",
            "font.size": 16,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.linewidth": 2.5,
            "legend.frameon": False,
        })
       ```
    2. 配色使用学术色板: blue_main=#0F4D92, green_3=#8BCF8B, red_strong=#B64342, teal=#42949E, violet=#9A4D8E
    3. 同一方法在不同面板中保持颜色一致
    4. 多面板遵循 overview → deviation → relationship 三层递进
    5. 反冗余检查：无两个面板回答同一科学问题
     6. 导出 SVG 到 ./docs/paper-drafts/figures/ 目录
     7. 代码末尾包含 savefig 语句

    输出:
    - 完整可执行的 Python 绘图代码
    - 图表说明（面板含义、数据映射）

    约束: 遵循 academic-figure SKILL.md 中的 Red Lines

    返回: Python 绘图代码 + 图表说明
```

dispatch 返回后，**必须**将绘图代码写入 `./docs/paper-drafts/figures/codes/plot_fig{N}.py`。**不自动执行代码**。

## Step 6.5: Evidence Compliance Review (Review Phase 1: Evidence)

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
    Evidence Map: <传入证据清单>
    Verified References: <传入已核验引用>
    placeholder_stats: <传入占位符统计>

     执行步骤:
     1. 读取 skills/academic-reviser/SKILL.md，按 targeted-evidence-mode 执行
     2. 检查每个 claim 是否在 Evidence Map 中有对应的 newly_run 或 preexisting_artifact 支撑
     3. 检查每个 inline citation 是否对应 Verified References 中已核验条目
     4. 检查是否存在"正文有引用但 Verified References 中无对应条目"
     5. 检查是否存在"只有搜索列表但没有 Verified References + Citation-to-Claim Map"的未完成状态
     6. 检查所有占位符使用是否符合规范（如 [REF_NEEDED] 含方向说明）
     7. 检查是否存在无证据支撑的"裸 claim"

    输出: evidence_debt (open/closed) + evidence_issues 清单
    **不允许修改正文。**

    约束: 遵循 academic-reviser SKILL.md 中的 Red Lines

    返回: 审查结果（evidence_debt + issues）
```

This is Review Phase 1 (Evidence). Only proceed to Review Phase 2 (Prose Gate) after `evidence_debt = closed`.

Input: Draft v1 text, Evidence Map, Verified References, placeholder_stats from Step 6.4.
Output: `evidence_debt` (open|closed), `evidence_issues` list.

If protocol risks from Step 4 materially weaken a claim's support (for example: no independent test set, missing strong baselines, or single-run results used for strong conclusions), keep `evidence_debt = open` for that claim until the text is downgraded, the risk is made explicit, or the claim is frozen/blocked.

If `evidence_debt = open`, record issues and return to Step 6. Do not proceed to Step 6.6 while open.
