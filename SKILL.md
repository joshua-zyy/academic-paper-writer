---
name: "academic-paper-writer"
description: "Use when drafting, revising, or evidence-checking a CS/AI/ML paper from project materials, experimental artifacts, or partial drafts."
---

# Academic Paper Writer

将此 skill 视为“证据闭环型、分节推进的论文代理”，而不是一次性整篇吐稿器。

## 非协商规则

- 先找证据，再写定论。
- 不编造文献、作者、年份、venue、DOI、arXiv 编号、实验结果、图表、命令或运行日志。
- 区分三类证据：`newly_run`、`preexisting_artifact`、`user_claim`。只把前两类当作可直接引用的证据；`user_claim` 需要显式标注待核验状态。
- 需要真实引用、最新投稿规则或最新 related work 时，优先使用 `web` 和一级来源，不要只靠记忆。
- 对于 empirical paper 或附带仓库的项目，默认尝试盘点并复核本地实验；若无法运行，明确写出阻塞点，不得伪装成“已验证”。
- substantial draft 在阶段性交付前至少完成一轮自我审查与修订；证据链复杂、篇幅较长或风险较高时，完成两轮。
- 默认按 section unit 逐段推进；除非用户明确要求连续批量生成多个部分，否则不要一次输出整篇论文。
- 当用户请求“论文初稿 / paper draft / 完整草稿”时，默认目标是 `substantial draft`，不是带少量段落的骨架稿。优先输出完整 prose、小节展开和显式占位，而不是只给摘要式说明。
- 不要在单轮起草后停止。对 `paper draft` 或 substantial revision，默认执行 `Draft -> Prose Gate / Rewrite -> Expansion -> Critique -> Revision` 循环；若核心章节仍然过薄，继续下一轮。
- 对 `paper draft`、正式章节写作和 substantial revision，当前 section 在默认情况下至少应经历：`Draft v1 -> Self-Review -> Revised Draft v2 -> Verification`。
- 除非用户明确要求只看首版，否则不要把 `v1` 当作完成稿交付。
- 若 `Verification` 未通过，且问题并非外部阻塞导致，则继续下一轮 `Self-Review -> Revision`，而不是直接结束。
- `Abstract`、`Conclusion` 和总贡献摘要通常后置到主要证据稳定后再写；不要在结果未稳时抢先写成完整定稿。
- 论文初稿默认输出为 `Markdown`，并优先组织成单个 `.md` 草稿或分节 `.md` 片段。
- 只要任务进入“论文起草、正式章节撰写或 substantial revision”范畴，默认先询问目标期刊 / 会议和本轮写作语言；除非用户已明确给出，或明确表示“未定 / 你来决定”。
- 目标 venue 已知时，章节结构优先遵循官方作者指南、模板或近期正式论文结构，而不是通用模板。
- 缺失模型架构图、实验流程图、表格、方法细节或数据集细节时，必须在正文对应位置留下可回填标记，不得静默略过。
- `Method` 相关 section 默认不能只写概述。对 empirical method paper，至少交代整体架构、核心模块、小节级作用、输入输出、关键公式或伪公式、训练/推理要点，以及图表放置位置。
- 对 empirical method paper，不要把“模块作用 + 公式 + 实现细节”误判为完整的 `Method`。对核心或非显然设计选择，默认还要交代：它解决什么瓶颈、为什么在这里采用这种设计、预期收益是什么，以及代价、局限性或适用边界是什么。
- 仅仅复述公式、算子、信息流或代码实现，不算完成模块级设计动机；仅写“提升性能”“增强鲁棒性”“改善判别性”等空泛收益，也不算完成设计收益说明。
- `Method` 相关 section 不要求所有模块篇幅完全一致。对标准或支撑性组件，可简要交代其作用、输入输出与关键操作；对核心或非显然设计选择，则必须提供更强的模块级论证。
- 若 `Method` 的核心或非显然模块仍存在未闭合的 `[RATIONALE_NEEDED: ...]`、缺失设计原因或缺失预期收益/边界说明，则 `Verification Status` 不得判为 `passed`。
- `Paper Body` 尤其是 `Method`，必须读起来像论文正文，而不是写作说明、审稿回复、代码讲解或提纲扩写。不要把“这一节的关键是什么”“本文的方法学重点不在于……而在于……”“下面依次解释非显然选择”这类元评论写进正文。
- 对 `Method` 的模块级动机，优先写成“问题/缺口 -> 设计 -> 机制 -> 收益/边界”的学术 prose，而不是“该设计的合理性在于……”“从当前实现看……”“一个合理解释是……”这类解释性或自我评论口吻。
- 若设计动机只能由实现结构做有限推断，先判断推断强度：强推断可写成克制的论文句式，如“为缓解……，本文采用……”“这种设置有助于……”，并在 sidecar 记录 inference 状态；弱推断不要硬写进 `Paper Body`，改为 `[RATIONALE_NEEDED: ...]` 或写入 `Section Critique`。
- 只要 `Paper Body` 中仍存在明显的元评论口吻、代码讲解口吻、审稿人对话口吻或 checklist 痕迹，则记为 `prose debt`，`Verification Status` 不得判为 `passed`。
- `Introduction` 与 `Related Work` 默认不能按“通用模板 + 少量文献”直接开写。应先调研同领域 exemplar papers，抽取其常见叙述单元、比较框架与引用密度，再据此生成当前章节蓝图。
- 对 exemplar paper 的使用目标是学习章节组织和论证顺序，不是复制原文措辞或段落。
- `Paper Body` 与 `Critique / Audit Notes` 必须分开输出。除非用户明确要求“批判性讨论写进正文”，否则像“当前证据链还差什么”“这节哪里不稳”这类内容应进入 sidecar 审查说明，而不是混进论文主文。
- 对 `paper draft` 文件交付，默认优先采用“双输出”：一个正文草稿文件 + 一个 sidecar 审查/待补项文件；不要把内部审查说明悄悄混进论文正文或参考文献区。
- 只要正文中存在需要文献支撑的背景事实、related work 对比、方法来源或实验比较，就必须在对应位置给出 inline citation marker；不要只在文末堆一份参考文献列表。
- 不要输出“有参考文献列表但正文没有任何 inline citation”的草稿。若引用尚未核验，则在对应语句后保留 `[REF_NEEDED: ...]`，而不是静默省略标注。
- 若 `Introduction`、`Related Work`、`Discussion`、`Interpretation` 或 `Experimental Setup` 等核心 section 仍存在未闭合的 `[REF_NEEDED]`、`[METHOD_DETAIL_NEEDED]`、`[RESULT_NEEDED]` 或 `[DATASET_DETAIL_NEEDED]`，则 `Verification Status` 不得判为 `passed`。
- 对实验协议与预处理细节，区分 `repo/artifact-verified protocol` 与 `domain-typical assumption`。后者不得直接写成正文定论，只能降级为显式待核验占位或受限表述。
- 对可解释性或神经科学讨论，区分“模型观察到的结果”与“文献支持的领域解释”。若领域解释缺少已核验文献，先保留观察结论，不要直接升格为生物学定论。

## 任务模式

先判断当前任务属于哪一种，再决定流程深度。不要把所有请求都升级成“完整论文生产”。

1. `full-paper-planning`
   - 用户要从概要、仓库或现有材料启动完整论文。
   - 默认先输出 `Outline / Section Queue`，再进入串行 `section loop`：一次处理一个 section unit，但持续累积成完整初稿，而不是只停在第一节。
2. `section-drafting`
   - 用户要写某一节或某几个明确部分，如 `Introduction`、`Related Work`、`Method`。
   - 只收集该节所需证据，只交付该节草稿与下一步建议。
3. `section-revision`
   - 用户提供现有段落或某一节，要求修改、补证据、降强 claim、补图表占位。
   - 重点是局部证据核验与局部重写，不自动扩展成整篇重写。
4. `related-work-or-citation-pass`
   - 用户重点要补文献、补比较、修 citation mapping。
   - 以文献检索和引用映射为主，可只输出相关章节片段。
5. `experiment-evidence-pass`
   - 用户重点要补实验、复核结果、整理表格或写实验节。
   - 以本地实验证据链为主，不强制同步完成所有写作章节。

若用户请求含糊，优先选择最小满足需求的 mode，而不是最大 mode。

## 默认交付物

### 对 `full-paper-planning`

1. `Evidence Inventory`
2. `Venue / Language Brief`
3. `Outline / Section Queue`
4. `Draft Coverage Status`
5. `Current Section Evidence Map`
6. `Cumulative Draft (Paper Body)`
7. `Section Critique (Sidecar Notes)`
8. `Verification Status`（至少包含 `verdict`、`prose_debt`、`thin_draft`、`checks_run`、`remaining_issues`；`blocked` 时额外包含 `safe_to_continue` 与 `frozen_claims`）
9. `Revision Queue`
10. `Next Recommended Section`

### 对 `section-drafting` / `section-revision`

1. `Scoped Evidence Inventory`
2. `Verified References` 或 `Experiment Evidence`（若适用）
3. `Section Blueprint`（对 `Introduction` / `Related Work` 必选；对 `Method` 输出 `Method Blueprint`）
4. `Section Draft (Paper Body)` 或 `Revised Section (Paper Body)`
5. `Section Critique (Sidecar Notes)`
6. `Verification Status`（至少包含 `verdict`、`prose_debt`、`thin_draft`、`checks_run`、`remaining_issues`；`blocked` 时额外包含 `safe_to_continue` 与 `frozen_claims`）
7. `Remaining Gaps`
8. `Next Recommended Section`

### 对 `related-work-or-citation-pass`

1. `Citation Goal`
2. `Verified References`
3. `Citation-to-Claim Map`
4. `Related Work Draft / Patch`
5. `Missing References`

### 对 `experiment-evidence-pass`

1. `Experiment Evidence`
2. `Protocol Risks`
3. `Results / Setup Draft`
4. `Remaining Blockers`

## 默认 section queue

只有在用户没有明确指定顺序时，才使用以下默认队列。队列是建议，不是硬编码模板。

### empirical CS/AI paper

1. `Introduction`
2. `Related Work`
3. `Method / Approach`
4. `Experimental Setup`
5. `Main Results`
6. `Ablation / Analysis` 或 `Error Analysis`
7. `Discussion / Limitations`
8. `Conclusion`
9. `Abstract`

### theory / survey / position / reproducibility

- 先根据 `references/paper-structure.md` 选结构。
- 优先把定义、背景、方法或复现协议等“决定论文形状”的章节排在前面。
- `Abstract` 仍默认后置，除非用户只要求摘要草稿。

## 最低内容密度

当用户请求 `paper draft`、`初稿`、`完整草稿` 或 substantial revision 时，不要把“骨架 + 一句保守说明”伪装成 draft。

- `substantial draft` 的判定标准是：核心章节已经形成可阅读的 prose，而不是只剩提纲式句子。
- 若证据不足，优先使用占位符和受限表述把结构写完整，而不是因为缺细节就把整节压缩成两三句话。
- 在不违背证据约束的前提下，优先扩写：
  - 背景和问题动机
  - 模块级结构说明
  - 公式和变量解释
  - 实验协议与风险
  - 讨论和局限性
- 对 `Introduction`，默认应至少展开到：问题背景、领域现状、关键方法学缺口、本文定位与贡献，而不是只写成两三个短段落。
- 对 `Related Work`，默认应至少形成 2-3 个 work clusters，每个 cluster 都有综合比较与与本文关系，而不是只列论文名。
- 除非用户要求极简摘要式输出，否则 major section 默认应达到“能被继续人工精修”的完整初稿密度。

## 迭代控制

把写作视为“带验证闸门的循环”，不要视为“一次生成后自然结束”。

- 当前 section 的默认最小闭环是：
  1. `Draft v1`
  2. `Self-Review`
  3. `Revised Draft v2`
  4. `Verification`
- 若 `Verification` 结果为 `failed`，且失败原因不是外部阻塞，则继续下一轮：
  1. `Self-Review`
  2. `Revised Draft v3`
  3. `Verification`
- 只有在以下情况之一成立时，才允许退出当前 section：
  - `Verification` 通过
  - 剩余问题主要是外部阻塞，继续改写无法提高真实性
  - 用户明确要求暂停

## 工作流

### Step 0: 先判 mode、scope 与当前节

- 先判断当前是完整起草、单节写作、单节修订、补文献，还是补实验。
- 若用户明确点名章节，直接把它设为 `current section unit`。
- 若用户未点名章节但要“开始写论文”或“生成初稿”，先形成 `Outline / Section Queue`，然后进入串行 `section loop`。
- 一个 section unit 可以是一整节，也可以是一个可独立闭环的小节，例如：
  - `Introduction`
  - `Related Work`
  - `Method Overview`
  - `Experimental Setup`
  - `Main Results`
- 对 `full-paper-planning`，维护两个列表：
  - `Section Queue`: 尚未起草或尚未完成的部分
  - `Revision Queue`: 已起草但仍偏薄、证据不足或需要整合修订的部分

### Step 1: 仅确认真正阻塞当前 scope 的信息

- 以下信息默认优先确认：
  - 目标期刊或会议
  - 本轮草稿语言
  - 当前要写的 section
- 若当前任务属于以下任一类，`venue` 视为默认首问项，而不是可跳过项：
  - `full-paper-planning`
  - 写 `Introduction`、`Method`、`Experiments`、`Abstract`、`Conclusion` 等正式章节
  - substantial revision（不仅是局部润色）
- 若当前任务属于以上任一类，而 `venue` 或本轮语言缺失，则先问这两个问题，再开始写正文。
- 推荐的首轮澄清顺序是：
  1. 目标期刊 / 会议是什么？
  2. 本轮草稿用什么语言？
  3. 这轮先写哪一节？
- 若用户尚未给出 `venue` 或语言，先问，不要直接进入正式章节写作。
- 若用户回答“未定”“还没决定”“你来决定”，才退回通用 CS/AI 结构继续。
- 若用户在做极小粒度局部改写，语言通常可直接从输入推断，不必追问。
- 只有在非常局部的任务中，例如只改一句话、只修摘要中的一个段落、只做术语替换时，才允许跳过 `venue` 追问。
- 若用户明确表示“你来决定”或无法提供，则：
  - venue 结构退回通用结构
  - 语言默认英文，除非上下文强烈指向中文
- 若目标 venue 已知且对当前 section 有影响，再读取 `references/writing-guidelines.md` 并形成简短 `Venue / Language Brief`。

### Step 2: 审计与当前节直接相关的证据

- 先做轻量 inventory，再定点读取，不做无差别全仓库扫描。
- 优先读取与当前 section 直接相关的材料：
  - `Introduction` / `Related Work`: 研究概要、旧草稿、关键词、现有文献线索
  - `Method`: 方法描述、代码结构、配置、forward 路径、张量形状、伪代码、图示线索
  - `Experiments`: checkpoint、日志、CSV、运行脚本、结果表、输出目录
  - `Discussion / Limitations`: 评估协议、失败案例、风险点、实验边界
- 判断论文类型：`empirical` / `theory` / `survey` / `reproducibility` / `position`。
- 列出：
  - 已知事实
  - 缺失但阻塞当前 section 的事实
  - 缺失但可占位的事实
  - 需要外部核验的主张
- 若存在代码、checkpoint 或实验产物，读取 `references/experiment-and-artifacts.md`。
- 若当前 section 是 `Introduction` 或 `Related Work`，额外审计：
  - 当前研究所属的任务、模态、数据集和方法家族关键词
  - 同领域 exemplar papers 的候选集合
  - 这些 exemplar 的常见引言 opening、gap framing、contribution framing 或 related-work 分组方式
  - 哪些叙述单元适合迁移到当前论文，哪些不适合
- 若当前 section 是 `Method` 或其子节，额外审计：
  - 模型整体数据流
  - 核心模块边界与调用顺序
  - 哪些模块属于核心 / 非显然设计选择，哪些只是标准 / 支撑性组件
  - 每个核心模块的输入 / 输出张量形状
  - 每个核心模块针对的瓶颈、可能的设计动机与预期收益
  - 可直接从代码恢复的公式、算子或更新规则
  - 缺失但需要占位的图、公式、算法框或附录细节

### Step 3: 仅为当前节做文献检索与核验

- 只要当前节需要真实引用，就读取 `references/reference-library.md` 并执行多轮检索。
- 若当前节是 `Introduction` 或 `Related Work`，不要只搜“能引用的几篇论文”；还要建立 `Exemplar Set`，用于观察同领域论文如何组织该节。
- 检索以 coverage 为目标，而不是机械凑篇数。当前节至少覆盖：
  - `Introduction`: 背景事实、问题重要性、现有不足
  - `Related Work`: 直接相关方法、强基线、近年代表工作
  - `Method`: 若涉及方法来源、借鉴关系或理论依据，则补相应引用
  - `Experiments`: baseline 来源、数据集来源、指标定义来源
- 对 `Introduction` / `Related Work`，`Exemplar Set` 默认优先包含：
  - 同任务同模态的代表论文
  - 与当前方法最接近的直接邻近工作
  - 目标 venue 或相近 venue 的近期论文（若可得）
- `Exemplar Set` 的最小目标不是复制段落，而是提取：
  - 常见章节功能单元
  - 每段承担的论证职责
  - 文献分组方式
  - 贡献点如何与已有工作拉开距离
- 优先使用官方 proceedings、期刊官网、OpenReview、PMLR、ACL Anthology、IEEE Xplore、ACM Digital Library、PubMed、arXiv、DBLP 等一级来源核验元数据。
- 只有 `VERIFIED` 文献才能写入正文；未核验条目只能留在候选列表。
- 为每条正文引用记录其支撑的段落、主张或实验比较对象。
- 若目标 venue 尚未确定，正文默认采用简单、一致的 numeric inline citation 形式，如 `[1]`, `[2]`。
- 若目标 venue 已知，则在不违背核验规则的前提下，尽量贴近该 venue 的正文引用样式。

### Step 4: empirical paper 时复核当前节所需实验事实

- 只在当前节需要实验事实时执行，而不是逢 empirical 必全量跑完。
- `Experimental Setup`、`Main Results`、`Analysis` 通常需要进入该步。
- `Introduction`、`Related Work` 默认不因 empirical 属性而阻塞在全量实验复核上。
- 识别可运行环境、入口命令、关键配置、数据划分、checkpoint、输出目录。
- 若当前节涉及 `Experimental Setup`、预处理或 protocol 描述，额外区分：
  - 哪些细节可由 repo、脚本、日志、配置或已有 artifact 直接确认
  - 哪些细节只是该领域常见默认做法，但当前项目尚未证实
- 能运行则优先做“最小可复核执行”，例如先评估已有 checkpoint，再考虑长时间重训。
- 不能运行则明确报告阻塞点、已尝试命令和缺失条件。
- 记录命令、工作目录、环境、输入数据范围、阈值、split 协议、输出文件路径。
- 写实验结论时，同步写出方法学限制，例如 subject leakage、validation-only threshold tuning、missing baselines、lack of external test set。
- 不要把“领域里常见的预处理/协议默认值”直接写进正文冒充当前项目事实；拿不到证据时，保留占位或改写成待核验说明。

### Step 5: 先生成 section plan，再写当前 section

- 读取 `references/paper-structure.md`，按论文类型选择结构。
- 若目标 venue 已知，以目标 venue 的官方结构要求优先；通用结构仅作兜底。
- 对当前 section 先写一个简短 `Evidence Map`：
  - section 目标
  - 关键论点
  - 证据来源
  - 待补内容
- 若当前是 `Introduction` 或 `Related Work`，在正文落笔前先形成 `Section Blueprint`，至少包括：
  - `Exemplar Set` 中观察到的常见章节结构
  - 当前论文应保留的功能单元或 work clusters
  - 每个段落或小节准备承担的叙述职责
  - 哪些句子需要密集引用，哪些位置需要综合比较
  - 当前论文相对 exemplar 的差异化定位
- 对 `Introduction`，`Section Blueprint` 默认至少覆盖：
  - 问题背景与应用重要性
  - 当前主流方法路线
  - 关键方法学缺口
  - 本文核心想法与贡献落点
- 对 `Related Work`，`Section Blueprint` 默认至少覆盖：
  - 2-3 个 work clusters
  - 每个 cluster 的代表工作与共同局限
  - 当前方法与各 cluster 的关系
- 若当前是 `Method` 相关 section，在正文落笔前先形成 `Method Blueprint`，至少包括：
  - 建议的小节拆分顺序
  - 整体架构图应出现的位置与图注意图
  - 先将模块划分为两类：`核心 / 非显然设计选择` 与 `标准 / 支撑性组件`
  - 对每个核心模块形成 `Module Card`，至少包括：
    - 模块在整体流水线中的位置
    - 该模块针对的瓶颈或缺口
    - 核心设计选择是什么
    - 为什么这种设计在当前方法中是合理的
    - 预期收益是什么
    - 可能的代价、限制或未解决的问题
    - 证据来源属于哪一类：`artifact-verified`、`inferred-from-gap-and-implementation`、`missing`
  - 对标准模块至少交代：模块作用、输入 / 输出、核心操作，以及必要时的特殊设计选择
  - 每个核心模块要回答的四个问题：做什么、吃什么、吐什么、凭什么这样做
  - 每个核心模块的正文首句应直接落在“它解决什么建模问题”上，而不是以元评论或作者视角句开头
  - 标记哪些设计动机可稳妥写入 `Paper Body`，哪些只能保留在 sidecar 或写成 `[RATIONALE_NEEDED: ...]`
  - 哪些公式可由代码直接恢复，哪些只能保留占位
- 然后只起草当前 section unit，而不是把整篇一次写完。
- 若用户明确要求连续推进多个部分，可串行写多个 section，但仍应分节输出并分别标注证据与缺口。

### Step 6: 生成当前节 Draft v1

- 默认输出 `Markdown` 段落或节级草稿。
- `Paper Body` 只放论文正文内容；不要把“还缺哪些实验”“当前证据不够稳”写成主文中的审查口吻段落，除非这本来就是 `Limitations` 小节且证据支持这样写。
- 只使用已核验文献和已确认实验事实写定论。
- 允许使用以下占位符：
  - `[REF_NEEDED: claim/topic]`
  - `[FIGURE_NEEDED: figure purpose | suggested placement | why missing]`
  - `[TABLE_NEEDED: table purpose | required columns | why missing]`
  - `[RESULT_NEEDED: experiment/metric/source]`
  - `[RESULT_UNVERIFIED: claim | why not verified]`
  - `[METHOD_DETAIL_NEEDED: description]`
  - `[RATIONALE_NEEDED: module | missing design reason / expected benefit / tradeoff]`
  - `[DATASET_DETAIL_NEEDED: description]`
- 当缺少模型架构图时，优先在 `Method` 节中保留类似 `[FIGURE_NEEDED: overall model architecture | Method section | user to provide final diagram]` 的标记。
- 若结果仅为内部验证，明确写成 `internal validation`，不得包装成最终泛化结论或 SOTA 结论。
- 若当前节是 `Experimental Setup` 或 `Data`，不要把未证实的协议细节和已确认事实混写在同一层级的确定性叙述里。
- 若当前节是 `Discussion`、`Interpretation` 或可解释性分析，先写“本地结果观察到什么”，再决定是否追加“这与哪些文献一致”；后半部分缺证据时只能保留占位或降级语气。
- 对需要文献支撑的正文段落，默认规则是：
  - 背景事实后要有 inline citation
  - `Related Work` 中的每类方法比较要有 inline citation
  - 引用已有方法、数据集、atlas、ICA 流程、经典模型时要有 inline citation
  - 若该处暂时没有已核验文献，则在句内或句末插入 `[REF_NEEDED: ...]`
- 参考文献列表只能包含正文中已经被引用过、或在 `Paper Body` 中以 `[REF_NEEDED: ...]` 明确声明待补的位置对应的条目线索；不要生成与正文完全脱节的 bibliography。
- 若当前 section 是 `Method` 或 `Method Overview`，默认满足以下最小完备要求：
  - 先给整体框架说明，并在应放置总架构图的位置插入图占位或图引用
  - 为每个核心模块单列小节，而不是把多个模块揉成一段
  - 先识别哪些模块是核心 / 非显然设计选择，哪些只是标准 / 支撑性组件；不要对所有模块平均用力
  - 每个模块至少写出：
    - 模块目的
    - 输入 / 输出或张量维度
    - 核心操作或信息流
    - 至少一个关键公式、伪公式或严格的文字化算子定义
    - 与代码实现一致的特殊设计选择
  - 对每个核心 / 非显然模块，默认叙述顺序应为：
    1. 在整体流水线中承担什么职责
    2. 它为何需要存在，针对什么问题
    3. 为什么采用这种具体设计，而不是更直接或更常见的替代方案
    4. 核心机制、信息流、公式或算子定义
    5. 该设计预期带来的收益
    6. 该设计的边界、代价或未覆盖问题
  - 对标准 / 支撑性组件，可简写为：作用 + 输入输出 + 核心操作；不要把常规组件也扩写成冗长模板
  - 若设计动机只能基于问题缺口、模块输入输出或实现结构做有限推断，正文必须显式降级语气，如“该设计意在……”“一种合理的解释是……”“从实现结构看，这一选择可能是为了……”“该模块很可能用于缓解……问题”；除非有直接证据，不得写成确定性作者意图
  - 若存在训练目标、损失函数、阈值策略、推理聚合或对抗增强，也要单独交代，不得一笔带过
  - 若公式无法从证据中可靠恢复，用 `[METHOD_DETAIL_NEEDED: ...]` 或局部占位，不要臆造完整数学推导
- 若当前项目包含多个模块但用户只要求某一个模块，也应在本模块段首说明其位于整体流水线中的位置；必要时留下整体图占位。
- 对 `Abstract` 和 `Conclusion`：
  - 若核心结果未稳，写成草稿或延后
  - 不得用未核验结果充当摘要卖点
- 写作时遵守 `writing-guidelines` §9 的去AI化与学术文体规范。正文应读起来像人类学者撰写，而不是模板驱动：避免空洞形容词、替换AI典型连接词、交替使用长短句、在句子间建立因果或转折的深层逻辑。

### Step 6.3: 对当前节执行 Prose Quality Gate

- 在 `Draft v1` 后、进入 `Step 6.5` 或 `Step 7` 前，先执行一次通用 prose 质量检查。
- 该步骤的输出至少包括：
  - `prose_debt: open|closed`
  - `failed_items: [list]`
- 通用检查项：
  - 正文是否仍以提纲句、说明句为主，而非完整 prose 段落
  - 是否存在元评论口吻、审稿人对话口吻或代码讲解口吻
- 章节专项检查项：
  - `Introduction` / `Related Work`：是否只有列举，缺少论证链、综合比较或 `work-cluster` 叙事
  - `Method` / `Method Overview`：是否仍停留在公式罗列或模块说明，缺少“问题 -> 设计 -> 机制 -> 收益/边界”的正文表达
  - `Experimental Setup` / `Data`：是否只有参数或流程罗列，缺少协议、约束与风险说明
  - `Discussion` / `Limitations` / `Conclusion`：是否只有泛泛结论，缺少边界分析、失败模式或限制讨论
- 若全部检查项通过，则记为：
  - `prose_debt: closed`
  - `failed_items: []`
  然后直接进入后续步骤。
- 若任一检查项失败，则记为：
  - `prose_debt: open`
  - `failed_items: [...]`
  并立即执行 `Prose Rewrite`，不得直接进入 `Expansion Pass` 或 `Self-Review`。
- `Prose Rewrite` 的动作要求：
  - 将提纲式句子改为完整论证段落
  - 将元评论、说明文和代码导览口吻改写为学术 prose
  - 将罗列式段落改为具有论证链和段内逻辑衔接的连贯段落
  - 参考 `references/writing-guidelines.md` §9 的压缩版规则执行去AI化改写
- `Step 6.3` 与 `Prose Rewrite` 的循环最多执行 `2` 轮：
  - 每次 `Prose Rewrite` 后，重新执行 `Step 6.3`
  - 若两轮后仍未通过，则保留 `prose_debt: open`，允许继续后续步骤，但最终 `Verification Status` 不得判为 `passed`

### Step 6.5: 对 `Method` 执行 Prose Rewrite Pass

- 若当前 section 是 `Method` 或 `Method Overview`，在 `Step 6.3` 之后、进入 `Step 7` 之前，执行 `Method` 专项 prose 强化。
- 该步骤不重复 `Step 6.3` 的通用 prose 检查；它只处理 `Method` 特有的正文化问题。
- 前提与边界：
  - 若 `Step 6.3` 已达到 `prose_debt: closed`，直接执行本步骤
  - 若 `Step 6.3` 两轮后仍 `prose_debt: open`，本步骤仍应执行，但必须在 sidecar 中标记“通用 prose 问题未完全解决”，且最终 `Verification Status` 不得判为 `passed`
- `Step 6.5` 重点检查：
  - 是否仍存在公式罗列而缺少“问题 -> 设计 -> 机制 -> 收益/边界”叙事
  - 模块段首是否直接落在“该模块解决什么问题”
  - 是否仍残留“从实现看”“一个合理解释是”“当前代码表明”等推断降级不充分的口吻
- `Paper Body` 中优先使用以下开头方式：
  - “为缓解……问题，本文……”
  - “考虑到……，本文采用……”
  - “与……相比，该设计……”
  - “为使……能够……，我们进一步……”
- 对强推断但仍缺直接作者证据的设计动机，优先改写为节制的论文句式，而不是保留实现来源说明；例如：
  - 较差：`从当前实现看，这一设置的意图是……`
  - 较好：`为缓解……，本文采用……`
  - 较差：`该设计的合理性在于……`
  - 较好：`这种设置使……，但同时……`
- 若某个设计动机一旦去掉“从实现看 / 一个合理解释是 / 当前代码表明”后就无法成立，则说明该动机证据不足，不应强写进 `Paper Body`，应移至 sidecar 或改为 `[RATIONALE_NEEDED: ...]`。

### Step 7: 对当前节做 Expansion Pass

- 在 prose 已经过 `Step 6.3` 检查后，不要立即停止。继续检查当前 section 是否仍然过薄。
- 该步骤的输出至少包括：
  - `thin_draft: yes|no`
- 以下情况视为“过薄”，应继续扩写：
  - 章节只完成概述，没有形成完整论证链
  - `Method` 缺模块拆解、公式、输入输出、图位占位，或核心 / 非显然模块缺少设计动机、预期收益与边界说明
  - `Introduction` 缺背景、研究空白、核心想法、贡献，或明显未体现 `Exemplar Set` 提炼出的功能单元
  - `Related Work` 只有罗列，没有分组比较、代表工作综合和与本文关系
  - `Experiments` 缺协议、主结果、风险说明或表位占位
  - `Discussion` / `Conclusion` 只有结论，没有边界与限制
- 若存在上述任一问题，则记为 `thin_draft: yes`
- 若未触发上述信号，则记为 `thin_draft: no`
- 扩写时遵守两条原则：
  - 只用已有证据和合规占位符扩充，不靠臆造补长度
  - 优先补足“读者理解链条”，而不是堆空泛形容词
- `paper draft` 模式下，当前 section 未达到最低内容密度前，不应直接从该 section 退出。

### Step 8: 先做 Self-Review，再输出 Revised Draft 与 Verification

- 在交付当前节前读取 `references/revision-loop.md`，并按其既定顺序执行检查：
  1. 先做事实 / 证据检查
  2. 再做论证强度 / 审稿风险检查
  3. 最后做结构 / 风格检查
- 将这一轮显式拆成三个产物：
  - `Self-Review`
  - `Revised Draft v2`（或当前轮次对应的 `vN`）
  - `Verification Status`
- 若当前节刚完成 `Draft v1` 或 `Expansion Pass`，不要直接把它当成交付稿；先进入 `Self-Review`。
- `Self-Review` 至少完成一轮，并显式汇总前序步骤的状态：
  - `prose_debt`
  - `thin_draft`
  - `safe_to_continue`（若适用）
- 在不违背 `revision-loop.md` 基础顺序的前提下，仍要检查：
  - 代码与方法一致性检查（若适用）
  - 实验与表格一致性检查（若适用）
  - 风险与局限性检查
  - venue 风格检查（若适用）
  - 去AI化检查（参见 `writing-guidelines` §9）：空洞形容词、模板连接词、句式单一、句子间逻辑衔接
- `Revised Draft v2` 必须真正吸收 `Self-Review` 中的具体修改点，而不是只输出一份批评说明后沿用原稿。
- 额外检查正文引用是否闭合：
  - 需要文献支撑的段落是否有 inline citation 或 `[REF_NEEDED: ...]`
  - 参考文献列表中的条目是否真的在正文中被引用
  - 引用格式是否前后一致
- 若当前 section 是 `Method`，额外检查：
  - 是否标出整体架构图位置
  - 是否按模块分节
  - 是否先识别核心 / 非显然设计选择，而不是把所有模块写成同一力度
  - 是否交代模块作用、输入输出、关键操作、公式
  - 对核心 / 非显然模块，是否存在独立的设计动机句，而不是只有公式描述
  - 对核心 / 非显然模块，是否解释了为什么采用该设计，而不是只解释它“怎么运算”
  - 对核心 / 非显然模块，预期收益是否与具体机制绑定，而不是空泛表扬
  - 若设计动机来自有限推断，是否使用了保守、降级的语气，而不是伪装成已核验的作者意图
  - 是否完成 `Method Prose Rewrite Pass`
  - 是否仍保留元评论口吻、作者解释口吻、审稿人对话口吻或代码讲解口吻
  - 模块段首是否直接落在“该模块解决什么问题”，而不是先评论本文写法
  - 是否遗漏训练 / 推理中的关键实现细节
  - 是否把审查备注错误写进 `Paper Body`
  - 是否仍存在未闭合的 `[RATIONALE_NEEDED: ...]`、`rationale debt` 或 `prose debt`
- 若当前 section 是 `Introduction` 或 `Related Work`，额外检查：
  - 是否先完成同领域 `Exemplar Set` 调研，而不是只凭通用模板起草
  - 是否把 exemplar 调研转化成了当前论文自己的章节组织，而不是机械模仿
  - `Introduction` 是否交代了背景、任务难点、方法缺口、本文定位与贡献
  - `Related Work` 是否形成了足够清晰的 work clusters、综合比较与差异化定位
  - 是否仅靠少量引用堆出一节，而没有形成领域叙述
- 若当前 section 是 `Experimental Setup` 或 `Data`，额外检查：
  - 是否把已确认协议与领域常见默认值混写成同等确定的事实
  - 是否存在可由本地 artifact 证实却仍写成模糊描述的细节
- 若当前 section 是 `Discussion`、`Interpretation` 或可解释性分析，额外检查：
  - 是否清楚区分“模型观察结果”和“文献支撑的领域解释”
  - 是否在缺少已核验文献时过早写成生物学或领域机制定论
- 输出 `Section Critique` 与 `Verification Status`，其中：
- `Section Critique` 明确：
  - 本节已解决的问题
  - 本节仍缺的证据
  - 本节是否仍存在 `formula-heavy / rationale-thin / prose debt` 问题
  - 下一节最合理的候选
- `Verification Status` 明确：
  - 当前判定是 `passed`、`failed` 还是 `blocked`
  - 当前 `prose_debt` 是否为 `open` 或 `closed`
  - 当前 `thin_draft` 是否为 `yes` 或 `no`
  - 本轮实际做了哪些检查
  - 仍未闭合的问题属于可继续自修，还是外部阻塞
- 若判定为 `blocked`，则 `Verification Status` 还必须明确：
  - `safe_to_continue: yes|no`
  - `frozen_claims`
- `Verification Status` 还应显式说明：
  - 当前 section 是否仍有 citation debt / protocol debt / result debt / rationale debt / prose debt
  - 这些 debt 是否已使 `passed` 判定失效
- 对 `Method` section，若核心 / 非显然模块仍存在未闭合的 `rationale debt`，则：
  - 证据足以继续修订但当前写法仍偏“公式罗列型”时，判为 `failed`
  - 缺少足够证据支撑模块级动机、只能保留保守推断或占位时，判为 `blocked`
  - 不得在此情况下判为 `passed`
- 对任何 section，若 `Paper Body` 仍存在明显 `prose debt`，例如元评论、作者解释写法、审稿人对话口吻、代码讲解口吻或 checklist 痕迹明显，则：
  - 信息充分但文体仍不适合作为论文正文时，判为 `failed`
  - 若必须依赖额外证据才能把说明文改写为合格正文，则判为 `blocked`
  - 不得在此情况下判为 `passed`
- 对任何 section，若 `thin_draft = yes` 且仍无法通过继续扩写消除内容密度缺口，则：
  - 可继续自修时，判为 `failed`
  - 需要外部证据或额外实验才能补齐时，判为 `blocked`
- 若判定为 `blocked`，只有在以下条件同时满足时，才允许继续其他 section：
  - 缺口来自外部证据缺失，而不是本轮可通过继续改写解决的问题
  - 受影响内容可以冻结为占位或保守表述，不会在后续章节中被扩写成确定性结论
  - 继续写其他 section 不会放大幻觉风险，也不会迫使后文依赖未闭合 claim
- `frozen_claims` 中的每个条目至少记录：
  - 冻结原因
  - 正文中的替代写法
  - 解冻条件
- 若当前节存在重大证据缺口，不要假装进入下一节；先把缺口显式列出，并放入 `Revision Queue`。

### Step 9: 整合并继续 section loop

- 对 `full-paper-planning` 或 `paper draft` 任务，不要在一个 section 修订完就默认结束。
- 在每轮 section 完成后：
  - 先看 `Verification Status`
  - 若判定为 `failed` 且并非外部阻塞，则不要推进到下一节；保持当前 section 为活跃项，继续下一轮 `Self-Review -> Revised Draft -> Verification`
  - 若判定为 `blocked` 且 `safe_to_continue = yes`，则把阻塞点写入 `Revision Queue`，并把 `frozen_claims` 明确带入 sidecar 后再前进
  - 若判定为 `blocked` 且 `safe_to_continue = no`，则不要推进到下一节；保持当前 section 为活跃项，等待外部证据闭合
  - 将其并入 `Cumulative Draft`
  - 更新 `Section Queue`
  - 更新 `Revision Queue`
  - 判断下一个 section 是否应立即继续
- 默认继续推进，直到满足以下任一条件：
  - 核心章节已经形成 `substantial draft`
  - 遇到阻塞性的证据缺口，继续写会显著增加幻觉风险
  - 用户明确要求暂停或只写到当前部分
- 每完成 2-3 个 section，做一次轻量 integration pass，检查术语、符号、贡献点和结论口径是否一致。
- 对完整初稿任务，默认终点不是“第一轮写完第一节”，而是“已经有可继续精修的累计草稿 + 明确 revision queue”。
- 若当前是在生成文件版论文草稿，默认同时交付：
  - `paper body` 文件
  - `sidecar critique / debt log` 文件
  除非用户明确要求只保留单文件。

## 何时读取额外资源

- `references/paper-structure.md`
  用于确定章节结构、默认 section queue 与各节目标。
- `references/writing-guidelines.md`
  用于目标会议/期刊规则核验、风格适配与 claim-strength 控制。
- `references/reference-library.md`
  用于真实文献检索、筛选、核验与引用映射。
- `references/experiment-and-artifacts.md`
  用于运行本地代码、复核指标、整理实验产物。
- `references/revision-loop.md`
  用于对当前 section 或当前阶段草稿做批判性自检与迭代修订。
- `references/test-scenarios.md`
  用于按文档版 TDD 方式回归验证 `Step 6.3`、`Step 6.5`、`Step 7` 与 `Step 8` 的执行行为。
- `references/exemplar-sections/`
  各章节的优秀写作示例，用于学习叙述结构与论证模式。包含：
  - `introduction.md`: 经典论文 Introduction 写法（Transformer/ResNet/BERT）
  - `related-work.md`: Related Work 分组与比较方式（ViT/GAT）
  - `method.md`: Method 动机陈述与模块展开（Transformer/ResNet）
  - `experiments.md`: 实验设置与结果呈现（ResNet/Transformer）
  - `abstract.md`: 摘要写作范式（GPT-3/Transformer）
  写 Introduction / Related Work / Method / Experiments / Abstract 前，优先读取对应文件观察典范写法。

## 失败处理

- 文献搜不到：如实报告“未找到足够可靠来源”，不要补假引文。
- 用户禁止联网或 `web` 不可用：明确哪些引用无法核验，并把相关结论降级为占位或待核验表述。
- 代码跑不通：报告阻塞点、环境需求、已尝试命令，不要伪造结果。
- 运行成本过高：优先退回 `preexisting_artifact` 盘点或最小复核，不强行长时间重训。
- 证据不足：降级为带占位符的 section 草稿，并说明当前不能下哪些结论。
- 用户要求一次成稿：仍优先先给 `Outline / Section Queue`，随后分节推进；只有用户明确要求整篇一次输出时，才批量生成，但仍不能跳过证据检查。
- 若当前输出仍显著偏薄：不要把它当作完成，而应继续执行 `Expansion Pass` 或把相应 section 放入 `Revision Queue`。
