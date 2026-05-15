# Orchestration Workflow — Part 2: Drafting (Step 5–8)

本文件包含编排器 Step 5–8 的详细执行流程。按需加载，避免一次性加载全部步骤。

完整步骤索引见 `orchestration-workflow.md`。

---

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

## Two-Stage Writing Process

**Stage 1: Blueprint (Bullet Points)** — Step 5 输出
- 使用 bullet points 组织论点结构
- 标注关键引用位置
- 规划段落职责和论证顺序

**Stage 2: Draft v1 (Flowing Prose)** — Step 6 输出
- 将 bullet points 转换为完整段落
- 添加过渡句和逻辑连接
- 自然融入 inline citations
- 确保段落内因果/递进/转折的深层逻辑

**转换示例**：

Blueprint (Stage 1):
```
- Background: Transformer 在 NLP 中成功，但在 EEG 中应用有限
  * Cite: Vaswani 2017 (attention), Recent EEG-transformer attempts
- Gap: EEG 的时间-空间双重特性未被现有 transformer 充分建模
  * 现有方法只处理时间或空间，未联合建模
- Our approach: 双分支 transformer 联合建模时空特征
  * 时间分支: temporal self-attention
  * 空间分支: graph attention on electrode topology
```

Draft v1 (Stage 2):
```
The Transformer architecture has achieved remarkable success in natural
language processing since its introduction by Vaswani et al. (2017), yet its
application to electroencephalography (EEG) signals remains limited. Unlike
textual data, EEG recordings exhibit dual temporal-spatial characteristics:
temporal dynamics within each electrode channel and spatial correlations
across the electrode topology. Existing approaches typically address only
one of these dimensions—either applying temporal self-attention to
individual channels or using spatial graph convolution without modeling
temporal dependencies—leaving the joint spatiotemporal modeling problem
unresolved. To bridge this gap, we propose a dual-branch Transformer that...
```

## Step 6: Draft v1

- Create a todo list for subtopics to cover.
- **前置检查：是否需要深层探查** — 在起草前检查当前 section 类型，按以下规则决定是否需要 dispatch 深层探查：
  | 当前 section | 需 dispatch 的探查 | 并行策略 |
  |-------------|-------------------|---------|
  | Method | `code_structure`（Module Cards + 张量形状 + forward 路径）+ `preprocessing`（预处理步骤） | **必须并行** |
  | Experimental Setup | `experiment_setup`（超参数、数据集划分、人口统计） | 单探查 |
  | Main Results / Ablation | `experiment_results`（主结果、基线对比、消融数值） | 单探查 |
  | Discussion | `interpretability`（可解释性结果、网络分析） | 单探查 |
  | Introduction / Related Work | 无需深层探查（已在 Step 2 完成） | — |
  - 需要探查 → **必须先 dispatch 再起草**，不得跳过。
  - dispatch 模板见 `references/workflow-step-0-4.md` 的 `### 单探查 dispatch 模板` 和 `### 并行 dispatch 模板（强制并行）`。
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

### 文件写入（强制）

Draft v1 生成后，**必须**立即将正文内容写入 `./docs/paper-drafts/paper_draft.md`。使用 Write 工具（首次）或 Edit 工具（追加/替换）更新文件。

**禁止在对话中输出完整 Draft 正文。** 对话中仅输出简短进度摘要：

> **{Section}**: Draft v1 已写入文件，进入审查阶段

## Step 6.4: Placeholder Audit, Figure Contract, Architecture Figure Pre-generation, and Debt List（**强制执行，不可跳过**）

After Draft v1, **必须**自动执行以下子步骤：

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

### 7c. Figure Contract（前置步骤，在生成任何图表之前**必须**完成）

对每个 `[FIGURE_NEEDED]` 占位符，在生成提示词或代码之前，**必须**先完成 Figure Contract：

1. **Core conclusion**：用一句话陈述该图必须捍卫的论点
2. **Evidence chain**：将每个计划面板映射到该论点，删除不承载独立证据的面板
3. **Archetype**：将图分类为 `quantitative grid`、`schematic-led composite`、`image plate + quant` 或 `asymmetric mixed-modality figure`
4. **Export contract**：设定最终尺寸、可编辑文本、源数据、统计信息、图像完整性说明和导出格式

### 7d. 双路径图表处理

对每个 `[FIGURE_NEEDED]` 按 Figure Contract 的分类结果进行双路径处理：

**路径 A — 架构图类**（purpose 含 architecture / structure / pipeline / diagram / network / flow / 架构 / 模块图 等）：
- 按下文 Step 6.4g 的 dispatch 模板委托 `academic-figure` 的 arch-prompt 模式
- 生成的提示词写入 `./docs/paper-drafts/figures/figure_prompts.md`（按图编号分节）
- 正文中的占位符替换为图编号引用（如 `Figure X` 或 `图X`）
- 若 `figures/figure_prompts.md` 不存在，使用 Write 工具创建；若已存在，使用 Edit 工具追加

**路径 B — 数据图类**（purpose 含 curve / comparison / ablation / result / 曲线 / 对比 / 消融 / 结果 等）：
- 按下文 Step 6.4h 的 dispatch 模板生成 Python 绘图代码
- 绘图代码写入 `./docs/paper-drafts/figures/plot_fig{N}.py`
- 正文保留占位符，记入待补项列表
- **不自动执行绘图代码**

### 7e. 追加待补项清单（**必须，不可省略**）
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

### 7f. 报告审计结果
将占位符统计信息（`placeholder_debt`）纳入 Section Critique，供 Step 6.8 Verification 引用。

### 7g. 架构图 dispatch 模板（路径 A）
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

     Figure Contract:
    - Core conclusion: {Step 6.4c 中定义的论点}
    - Evidence chain: {面板→论点映射}
    - Archetype: {图分类}
    - Export contract: {尺寸、格式等}

    风格要求：参考 NeurIPS / CVPR / AAAI / ICLR 等顶会论文插图风格。
    详见 skills/academic-figure/references/architecture-prompting.md 的「顶会风格参考」。
    确保最终输出达到发表级质量。

    执行步骤:
    1. 读取 skills/academic-figure/SKILL.md，按 B 路径（arch-prompt）执行
    2. 确认模型结构：核心组件列表、数据流方向、关键连接方式（残差/跨层注意力等）
    3. 按 skills/academic-figure/agents/figure_agent.md 中 B 路径的 Output Schema 输出结构化结果

    Output Schema (B 路径):
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

### 7h. 数据图绘图代码 dispatch 模板（路径 B）
对数据图类的 `[FIGURE_NEEDED]`，按此模板 dispatch：

```yaml
Task:
  description: "生成数据图绘图代码 - {figure_id}"
  subagent_type: "general"
  prompt: |
    任务: 为 {figure_id} 生成 Python 绘图代码
    图用途: {从 [FIGURE_NEEDED] 的 purpose 字段提取}
    数据来源: {实验数据路径或 Evidence Map 中的对应条目}

    Figure Contract:
    - Core conclusion: {Step 6.4c 中定义的论点}
    - Evidence chain: {面板→论点映射}
    - Archetype: {图分类}
    - Export contract: SVG + PNG 300dpi

    绘图代码规范（强制）:
    1. 脚本最前面必须包含以下初始化:
       ```python
       import matplotlib as mpl
       import matplotlib.pyplot as plt
       mpl.rcParams.update({
           "font.family": "sans-serif",
           "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
           "svg.fonttype": "none",
           "pdf.fonttype": 42,
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
    6. 导出 SVG（主要）+ PNG 300dpi（次要预览）
    7. 代码末尾包含 savefig 语句，输出到 ./docs/paper-drafts/figures/ 目录

    输出:
    - 完整可执行的 Python 绘图代码
    - 图表说明（面板含义、数据映射）

    约束: 遵循 academic-figure SKILL.md 中的 Red Lines

    返回: Python 绘图代码 + 图表说明
```

dispatch 返回后，**必须**将绘图代码写入 `./docs/paper-drafts/figures/plot_fig{N}.py`。**不自动执行代码**。

## Step 6.5: Evidence Compliance Review (Phase 1 of Two-Phase Review)

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
    placeholder_debt: <传入占位符统计>

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

This is Phase 1. Only proceed to Phase 2 (prose polishing) after `evidence_debt = closed`.

Input: Draft v1 text, Evidence Map, Verified References, placeholder_debt from Step 6.4.
Output: `evidence_debt` (open|closed), `evidence_issues` list.

If protocol risks from Step 4 materially weaken a claim's support (for example: no independent test set, missing strong baselines, or single-run results used for strong conclusions), keep `evidence_debt = open` for that claim until the text is downgraded, the risk is made explicit, or the claim is frozen/blocked.

If `evidence_debt = open`, record issues and return to Step 6. Do not proceed to Step 6.6 while open.
