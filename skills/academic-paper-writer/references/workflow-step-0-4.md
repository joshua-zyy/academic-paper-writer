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
3. **Continuation mode**: **必须询问**用户选择逐节撰写还是自动全部生成初稿。
   - 询问方式："选择逐节撰写（每节完成后暂停确认）还是自动全部生成初稿？（默认自动）"
   - 用户选择"逐节" → 记录 `continuation_mode = step-by-step`
   - 用户选择"自动"或未指定 → 记录 `continuation_mode = auto`
   - **一次性确认**：确认后全程不再重复询问，用户可随时切换
4. **Current section**: Determined by Step 0 if user did not specify.
5. **预期引用数量（min_citations）**：**必须询问**用户预期的参考文献数量。
   - 询问方式："您预期这篇论文的参考文献数量大约是多少篇？（默认 35 篇，short paper 建议 20 篇，workshop 建议 15 篇）"
   - 用户指定时记录为 `min_citations`
   - 用户未指定或说"默认"时使用默认值 35
   - **一次性确认**：确认后全程不再重复询问，Step 8 生成引用清单时自动核验。

If venue is known and not `user_declined`, **必须进入 Step 1.5** 执行 Venue Requirements Research，使用 webfetch 访问官方页面获取投稿要求并生成 `venue-brief.md`。

### 本地文献库（强制询问，与 venue 同属 Blocking Gate）

**venue/language/min_citations 确认后立即询问，在进入 Step 2 前必须给出明确答案**：

- 是否在当前项目中维护了本地文献库（存放待引用 PDF 论文的目录）？
  - 有 → 记录路径为 `local_lit_pdf_dir`
  - 没有 → `local_lit_pdf_dir = null`，跳过本地文献流程
- 如果有，告知将在其同级创建 `papersToMd/` 目录存放转换后的 MD 文档
- **必须检查 `markitdown` 是否已安装**，未安装时提供命令：
  ```
  pip install markitdown
  ```
- 接下来进入 **Step 1b** 的 PDF→MD 转换准备
- 若用户明确没有本地文献库或跳过转换：`local_lit_md_dir = null`，跳过 Step 1b

**Failure to confirm venue**: Stop and wait. Do not proceed to Step 2. Do not generate Outline or Section Queue until venue is resolved.

### Step 1 完整执行清单（9 项，Blocking Gate）

执行Step 1时，**必须按以下顺序逐项完成**。任一未完成不得进入Step 2。

- [ ] 1. **确认venue**（Blocking）
      - 询问："目标期刊/会议是？"
      - 用户未决定 → 提供2-3个建议
      - 用户说"你决定" → agent自主选择并告知

- [ ] 2. **确认language**
      - 询问："论文用中文还是英文撰写？"
      - 未指定 → 默认英文

- [ ] 3. **确认min_citations**
      - 询问："预期参考文献数量？（默认35篇，short paper建议20，workshop建议15）"
      - 未指定 → 默认35

- [ ] 4. **确认推进模式**
      - 询问："选择逐节撰写（每节完成后暂停确认）还是自动全部生成初稿？（默认自动）"
      - 用户选择"逐节" → 记录 `continuation_mode = step-by-step`
      - 用户选择"自动"或未指定 → 记录 `continuation_mode = auto`
      - **一次性确认**：确认后全程不再重复询问，用户可随时切换

- [ ] 5. **询问本地风格参考文献库**
      - 询问："是否有本地目标期刊风格参考文献库（存放目标期刊近年论文PDF的目录）？"
      - 有 → 记录路径为 `local_style_ref_dir`，进入第6项
      - 没有 → 跳过第6项，提示用户可以创建一个用于分析目标期刊写作风格

- [ ] 6. **询问本地文献库**
      - 询问："是否有本地文献库（存放PDF的目录）？"
      - 有 → 记录路径，进入第7项
      - 没有 → 跳过第7项

- [ ] 7. **本地文献库处理**（仅当第6项为"有"时）
      - 检查markitdown是否已安装
      - 未安装 → 提供安装命令：`pip install markitdown`
      - 输出PDF→MD转换提示（见下方模板）
      - 确认用户已收到提示

- [ ] 8. **进入 Step 1.5**（强制）— venue 确认后，必须执行 Venue Requirements Research（详见下方 Step 1.5），不可跳过

- [ ] 9. **以上全部完成**（含 Step 1.5） → 进入Step 2

### Step 1b 转换提示模板（第7项使用）

当用户有本地文献库时，**必须**输出以下提示：

```
本地文献库已确认: <local_lit_pdf_dir>

请先确保 markitdown 已安装（如未安装）, 需注意python版本>=3.12：
  pip install markitdown

然后从项目根目录运行以下命令：
  python skills/academic-citation/scripts/convert-pdfs-to-md.py <local_lit_pdf_dir> <local_lit_md_dir>

转换完毕后请告知我，我将从本地文献库中搜索可引用的文献。
（在此期间我将先进行项目证据审计和联网文献检索）
```

输出提示后，**立即进入Step 2**，不等待转换完成。

---

## Step 1.5: Venue Requirements Research（强制）

**条件**: venue 已确认且非 `user_declined` 时**必须执行**。不可跳过，不可推迟到起草阶段。

**跨模式适用性**：
- `full-paper-planning`：必须执行
- `section-drafting` / `section-revision`：若 venue-brief.md 已存在（同一项目、同一 venue），可复用，无需重复执行；若不存在，必须执行
- `related-work-or-citation-pass` / `experiment-evidence-pass`：若 venue 影响执行策略（如引用格式），且 venue-brief.md 不存在，必须执行

### 1.5.1 执行方式

**委托方式**：dispatch `academic-venue-research` 子skill

**Dispatch 模板**：
```yaml
Task:
  description: "Venue Requirements Research - {venue}"
  subagent_type: "general"
  prompt: |
    你已加载 academic-venue-research 子 Skill（skills/academic-venue-research/SKILL.md）。

    任务: 对目标 venue {venue} 执行完整调研（投稿要求 + 写作风格）
    venue: {venue}
    local_style_ref_dir: {local_style_ref_dir | null}
    research_type: full
    output_path: ./docs/paper-drafts/venue-brief.md

    执行步骤:
    1. 读取 skills/academic-venue-research/SKILL.md，按 Step 1-4 执行
    2. 调研投稿要求（使用 webfetch 访问官方页面）
    3. 调研写作风格（读取本地风格参考文献库或通过其他方式获取论文）
    4. 生成 venue-brief.md 文件

    约束: 遵循 academic-venue-research SKILL.md 中的 Red Lines

    返回: venue-brief.md 文件路径 + 调研摘要
```

**输入**：
- `venue`：目标 venue 名称
- `local_style_ref_dir`：本地风格参考文献库路径（可选，来自 Step 1 第5项）
- `research_type`：调研类型（full / requirements / style）
- `output_path`：输出路径（默认 `./docs/paper-drafts/venue-brief.md`）

**输出**：
- `venue-brief.md` 文件
- 调研摘要（在对话中输出）

### 1.5.2 生成 Venue Brief 文件

**必须**将调研结果写入 `./docs/paper-drafts/venue-brief.md`，格式如下：

```markdown
# Venue Brief

- Venue: {venue 名称}
- Official Source: {官方页面 URL}
- Language: {语言} [User Config]
- Min Citations: {预期引用数} [User Config]

## 投稿要求

- Page Limit: {页数限制，含说明}
- Required Structure: {必需章节列表}
- Template: {模板要求}
- Anonymous Review: {是否双盲}
- Citation Format: {引用格式}
- Appendix Policy: {附录政策}
- File Format: {文件格式要求}
- Other Requirements: {其他特殊要求}

## 写作风格备注

### 调研来源
- 调研论文数量：{数量}
- 调研论文列表：{论文标题列表}
- 调研方法：{本地文献库 / 开放获取论文 / 摘要分析}

### 论文结构偏好
- Introduction 长度：{平均段落数 / 页数}
- Introduction 组织方式：{常见结构}
- Related Work 位置：{独立章节 / Method 内 / Introduction 内}
- Related Work 组织方式：{按技术路线 / 按任务 / 按限制类型}
- Method 详细程度：{高 / 中 / 低}
- Experimental Setup 详细程度：{高 / 中 / 低}

### 写作风格偏好
- 语气：{正式 / 半正式 / 非正式}
- 用词偏好：{技术术语多 / 少 / 适中}
- 句式结构：{长句多 / 短句多 / 混合}
- 段落长度：{长段落 / 短段落 / 混合}

### 引用密度
- 平均引用数量：{数量}
- 引用格式：{数字 / 作者-年份}

### 图表使用偏好
- 平均图表数量：{数量}
- 图表类型偏好：{架构图 / 数据图 / 混合}
- 图表说明详细程度：{高 / 中 / 低}

### 各个部分的写法
- Abstract：{长度 / 结构 / 信息密度}
- Introduction：{背景介绍方式 / 问题陈述方式 / 贡献总结方式}
- Method：{详细程度 / 公式使用 / 算法描述}
- Experiments：{结果展示方式 / 分析深度}

## 信息完整性

| 信息项 | 状态 | 来源 |
|--------|------|------|
| Page Limit | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Required Structure | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Template | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Anonymous Review | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Citation Format | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Appendix Policy | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
```

### 1.5.3 对后续步骤的影响

Venue Brief 生成后，在后续步骤中**必须参考**：

| 后续步骤 | 如何使用 Venue Brief |
|----------|---------------------|
| Step 3 (文献检索) | 根据 Citation Format 确定引用核验策略 |
| Step 4 (实验复核) | 根据 Page Limit 确定实验结果展示的详略程度 |
| Step 5 (Blueprint) | 根据 Required Structure 调整 section queue |
| Step 6 (Draft) | 根据 Page Limit 控制各节篇幅 |
| Step 6 (Draft) | 根据 Citation Format 使用正确的引用格式 |
| Step 6 (Draft) | 根据 Anonymous Review 决定是否去除可识别信息 |
| Step 8 (引用清单) | 根据 Appendix Policy 决定附录内容 |
| Step 9 (图片生成) | 根据 Template 确定图片尺寸和分辨率要求 |

### 1.5.4 失败处理

- webfetch 无法访问官方页面 → 依次尝试：(1) 其他官方 URL (2) agent 已知知识（标注 `agent_knowledge (unverified)`）(3) 标注 Unknown 并警告用户
- 用户提供 venue 但明确说"你决定" → agent 自主选择 venue 后仍需执行 1.5
- venue = user_declined → 跳过 1.5，使用通用结构，警告用户"未指定 venue，通用结构可能不满足投稿要求"
- 二级证据（已录用论文）仅用于风格偏好，不能定义 venue 规范
- **信息来源透明**：所有 Venue Brief 中的信息必须标注来源（`webfetch` / `agent_knowledge (unverified)` / `Unknown`），不得隐藏信息来源

---

## Step 1b: Local Literature PDF→MD Conversion

**条件**: 仅在 `local_lit_pdf_dir != null` 且用户愿意进行转换时执行。与 Step 2 等后续步骤并行进行（不阻塞主流程）。

### 1b.1 生成转换脚本（一次性）

检查 `skills/academic-citation/scripts/convert-pdfs-to-md.py` 是否存在：
- 不存在 → 使用 Write 工具创建该脚本（写入 `skills/academic-citation/scripts/convert-pdfs-to-md.py`）
- 已存在 → 跳过

### 1b.2 确定 MD 输出目录

计算 MD 输出目录：
```python
md_output_dir = <local_lit_pdf_dir>/../papersToMd/
# 例: D:\AI\literature\ → D:\AI\papersToMd\
```
记录为 `local_lit_md_dir`。

### 1b.3 提示用户运行（强制，不可跳过）

**必须**在对话中输出以下提示，**然后立即进入 Step 2**，不等待转换完成。此提示为强制输出，不得因任何原因跳过：

```
本地文献库已确认: <local_lit_pdf_dir>

请先确保 markitdown 已安装（如未安装）：
  pip install markitdown

然后从项目根目录运行以下命令：
  python skills/academic-citation/scripts/convert-pdfs-to-md.py <local_lit_pdf_dir> <local_lit_md_dir>

转换完毕后请告知我，我将从本地文献库中搜索可引用的文献。
（在此期间我将先进行项目证据审计和联网文献检索）
```

### 1b.4 延迟等待

当 Step 3 即将开始（Step 2 完成后），检查 `local_lit_md_dir` 目录是否存在且包含 MD 文件：
- 存在 → 进入 **Step 3a**（本地优先搜索，使用 MD 文件）
- 不存在但有 `local_lit_pdf_dir` 且 PDF 可读 → **降级进入 Step 3a**（使用 PDF 直接搜索）
  - 使用 agent 的文件读取能力逐篇扫描 PDF，提取摘要/开头内容
  - `source_of_content` 标记为 `pdf_direct`
  - 后续引用核验时优先建议用户完成 MD 转换
- 两者皆不可用 → 在对话中提示"请运行转换命令"，然后继续 Step 3b（仅联网搜索）
- 用户转换完毕后可随时告知 agent，agent 回到 Step 3a 补充 MD 模式搜索

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

**深层探查不在此处执行**。各 section 起草前的深度探查规则已移至 `references/workflow-step-5-6.5.md` Step 6 的"前置检查：是否需要深层探查"表中。起草对应 section 前须按该表 dispatch。

For Introduction / Related Work, also audit exemplar paper candidates.
For Method, also audit model data flow, module boundaries, tensor shapes, recoverable formulas.

## Step 3: Literature Search and Verification（四步流程）

本步骤分为四个子步骤：
- **Step 3a**：本地文献库优先搜索（条件执行）
- **Step 3b**：联网文献检索 + 全文获取与阅读
- **Step 3c**：Subagent 阅读结果聚合 + Citation-to-Claim 映射
- **Step 3d**：生成引用文献清单文件（过程记录）

---

### Step 3a: 本地文献库优先搜索

**条件**: 仅在 `local_lit_md_dir != null` 且目录中存在 MD 文件时执行。

1. 读取 `<local_lit_md_dir>/_index.json`（由 `convert-pdfs-to-md.py` 生成）
2. 用从 section 提取的关键词在索引中搜索（匹配 title、first_500_chars）
3. 命中的候选文献，使用 **并行 dispatch** 模板（见下方"并行阅读 dispatch 模板"）同时 dispatch 多个 `literature-reader-agent`
4. 每个 reader 返回 LiteratureReadingReport
5. 主 agent 综合报告决定是否引用

**判定路径**：
- 若本地搜索找到 0 篇候选 → 跳过 Step 3a，直接进入 Step 3b
- 若找到候选但所有 `recommendation` 均为 `skip` → 进入 Step 3b 补充
- 若找到候选且至少部分被采纳 → 采纳的进入 Verified References，不足处继续 Step 3b

**并行阅读 dispatch 模板（N 篇候选同时执行）：**
```yaml
# ===== 同时发出以下 N 个 Task，互不等待 =====

{R001}:
  description: "阅读文献 R001 - {section}"
  subagent_type: "general"
  prompt: |
    你已加载 literature-reader-agent（skills/academic-citation/agents/literature-reader-agent.md）。

    任务: 阅读并提炼以下论文
    markdown_content: {从 local_lit_md_dir/R001.md 读取的全文内容}
    paper_metadata:
      title: {title}
      authors: {authors}
      year: {year}
      venue: {venue}
      source: {local MD}
    task_context: {当前论文的任务/方法/数据集描述}

    执行步骤:
    1. 读取 skills/academic-citation/agents/literature-reader-agent.md
    2. 遵循 Constraints (Red Lines)，严格区分 `[原文]` 与 `[推断]`
    3. 按 Reading Guidance 顺序提取信息
    4. 输出遵循 literature-reading-report.md schema

    Red Lines:
    1. 只阅读，不修改任何文件
    2. 禁止编造论文中不存在的内容
    3. 严格区分原文提取与推断

    返回: 完整 LiteratureReadingReport

{R002}:
  description: "阅读文献 R002 - {section}"
  # 同上模板，不同的 markdown_content
```

**所有 Task 返回后**，按 `relevance_to_current_work` + `recommendation` 排序，暂存为 `local_reading_reports`。

---

### Step 3b: 联网文献检索 + 全文获取与阅读

**在本地搜索完成后（或跳过 Step 3a 时），执行联网检索。**

**强制 checklist（必须全部完成，缺一不可）**：
- [ ] 至少覆盖 4 类查询（问题导向 / 方法导向 / 基线导向 / 时间导向）
- [ ] 逐篇核验元数据（venue / DOI / 年份 / 作者）
- [ ] 输出 Verified References（含 VERIFIED / UNVERIFIED 状态）
- [ ] 输出 Citation-to-Claim Map（每篇引用→对应主张）
- [ ] Introduction / Related Work 时额外构建 Exemplar Set
- [ ] 目标：全篇各节累计达到至少 35 篇引用（当前节尽可能多收集）

**未完成 checklist 前，不得进入 Step 4。Dispatch `academic-citation` 完成检索：**

**Dispatch template：**
```yaml
Task:
  description: "文献检索 - {section}"
  subagent_type: "general"
  prompt: |
    你已加载 academic-citation 子 Skill（skills/academic-citation/SKILL.md）。
    任务: 为 {section} 执行文献检索与核验
    关键词: {keywords} | 目标 venue: {venue}
    local_lit_md_dir: {local_lit_md_dir | null}

    必须完成以下所有产出，缺一不可：
    1. 4 类查询覆盖 + 本地检索（如有）
    2. 逐篇元数据核验 + 全文获取尝试
    3. Verified References（含 VERIFIED/UNVERIFIED 标注）
    4. LiteratureReadingReports（每篇候选文献）
    5. Citation-to-Claim Map
    6. Exemplar Set（Introduction/Related Work 时）

    约束: 遵循 academic-citation Red Lines；reader 输出必须区分原文与推断
    返回: 完整结构化输出
```

Input: current section, research keywords, target venue, local_lit_md_dir.
Output: Verified References, Exemplar Set (for Intro/RW), Reading Reports, Citation-to-Claim Map.

Constraint: only VERIFIED references enter the draft body.

---

### Step 3c: 聚合与 Citation-to-Claim 映射

合并 Step 3a 的 `local_reading_reports` 和 Step 3b 的返回结果：

1. 对所有候选文献按 `relevance_to_current_work` + `recommendation` 综合排序
2. 主 agent 逐条评估：
   - `strongly_cite` / `cite` → 写入 Verified References
   - `consider` → 记录为候选，判断是否论述需要
   - `skip` → 放弃
3. 根据 report 中的 `citable_claims`（仅 `source: 原文`），建立每个引用→正文主张的映射
4. 输出完整的 Citation-to-Claim Map

**重要规则**：
- Subagent 的 `recommendation` 仅为参考。主 agent 基于论文整体论证结构做最终决定
- 仅 `source: 原文` 的 `citable_claims` 可作为确定性引用依据
- `source: 推断` 的内容最多用于背景描述，且须在正文中降级表述（如"我们认为...可能..."）

For Introduction / Related Work: if retries still produce zero VERIFIED references and the user cannot provide usable seed papers, block before Step 6. Do **not** proceed with a `[REF_NEEDED]`-only draft for these sections.

### Step 3d: 生成引用文献清单文件（过程记录）

**用途**：生成一个独立于论文正文的引用清单文件，方便用户随时查看已引用文献、逐篇下载 PDF。

**执行时机**：Step 3c 完成后立即执行。后续每完成一个 section 的起草，追加该节新增的引用。

1. 将当前所有 Verified References 写入 `./docs/paper-drafts/referenced-literature-inventory.md`
2. 每篇记录：标题、作者、venue、年份、DOI/arXiv、来源链接、引用章节
3. 后续每完成一个 section，检查该节新增的引用并追加到此文件

**输出格式**：
```markdown
# 引用文献清单（过程记录）

以下文献在论文撰写过程中被引用。可据此逐篇下载 PDF。

| # | 文献 | Venue | 年份 | DOI/arXiv | 来源 | 引用章节 |
|---|------|-------|------|-----------|------|---------|
| 1 | Author et al., "Title" | NeurIPS | 2024 | arXiv:2401.12345 | https://arxiv.org/abs/2401.12345 | Introduction |
| 2 | Author et al., "Title2" | CVPR | 2023 | 10.1109/CVPR.2023.00123 | https://openaccess.thecvf.com/... | Method |
```

**与 Step 8 的区别**：
- Step 3d = 过程记录，逐节追加，方便用户随时下载
- Step 8 = 终版核验清单，论文完成后一次性生成，用于确认引用合理性

## Step 4: Experiment Evidence Review

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
    experiment_config:
      mode: minimal_reproducible      # 默认最小可复核模式
      timeout_minutes: 30

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
