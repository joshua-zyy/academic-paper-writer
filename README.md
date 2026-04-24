# Academic Paper Writer

一个面向 CS / AI / ML 领域的**证据驱动、分节推进**的论文写作 Agent Skill。它将论文写作视为带验证闸门的迭代过程，而非一次性生成整篇文稿的模板工具。

---

## 核心理念

- **先找证据，再写定论** —— 不编造文献、作者、年份、venue、DOI、实验结果或图表。
- **分节推进，逐段闭环** —— 默认按 section unit 串行推进，每节经历 Draft → Self-Review → Revision → Verification。
- **证据分级，claim 可控** —— 区分 `newly_run`、`preexisting_artifact` 与 `user_claim`，只把前两类当作可直接引用的证据。
- **去 AI 化文体** —— 正文应读起来像经验丰富的人类学者撰写，而非模板驱动的机器输出。

---

## 适用场景

| 场景 | 说明 |
|------|------|
| 📝 **完整论文起草** | 从研究概要、代码仓库或实验产物启动，按 section 串行生成 substantial draft |
| 🔧 **单节撰写** | 针对 `Introduction`、`Related Work`、`Method`、`Experiments` 等某一节深度写作 |
| 🔄 **单节修订** | 在现有段落基础上补证据、降强 claim、补图表占位、优化 prose |
| 📚 **补文献与引用** | 检索并核验参考文献，建立 `Citation-to-Claim Map`，补全 inline citation |
| 🧪 **补实验与证据** | 盘点本地实验产物、复核指标、整理表格、撰写实验章节 |

---

## 核心特性

### 1. 五种任务模式

- **`full-paper-planning`** — 从概要或仓库启动完整论文，输出 `Outline` + 串行 `section loop`
- **`section-drafting`** — 聚焦单节，只收集该节所需证据，交付该节草稿与下一步建议
- **`section-revision`** — 局部证据核验与局部重写，不自动扩展成整篇重写
- **`related-work-or-citation-pass`** — 以文献检索和引用映射为主，补全相关章节
- **`experiment-evidence-pass`** — 以本地实验证据链为主，整理结果与表格

### 2. 严格的迭代质量控制

每个核心章节默认经历：

```
Draft v1
  → Prose Quality Gate（去 AI 化、文体检查）
  → Method Prose Rewrite（Method 专项正文化）
  → Expansion Pass（内容密度扩写）
  → Self-Review（事实 / 论证 / 风格三轮检查）
  → Revised Draft v2
  → Verification（ verdict: passed / failed / blocked ）
```

若 `Verification` 未通过，继续下一轮 `Self-Review → Revision`，直到满足退出条件。

### 3. 丰富的参考体系

本项目内置多份结构化参考文档，指导 Agent 在写作各阶段做出一致、专业的决策：

| 参考文件 | 用途 |
|---------|------|
| `references/paper-structure.md` | CS/AI 论文默认结构、各节写作建议、缺失证据时的降级规则 |
| `references/writing-guidelines.md` | 目标 venue 风格适配、Claim 强度控制、去 AI 化学术文体规范 |
| `references/revision-loop.md` | 自检与迭代修订的标准流程 |
| `references/reference-library.md` | 真实文献检索、筛选、核验与引用映射指南 |
| `references/experiment-and-artifacts.md` | 本地代码运行、实验复核、指标整理与产物管理 |
| `references/test-scenarios.md` | 对关键写作步骤的回归验证场景 |
| `references/exemplar-sections/*.md` | 经典论文各章节范例（Transformer / ResNet / BERT / ViT / GAT） |

### 4. 安全的占位符系统

当证据不足时，使用显式占位符维持结构完整性，而非压缩成极短说明或编造内容：

- `[REF_NEEDED: claim/topic]` — 待补文献
- `[FIGURE_NEEDED: ...]` — 待补图表
- `[TABLE_NEEDED: ...]` — 待补表格
- `[RESULT_NEEDED: ...]` — 待补实验结果
- `[METHOD_DETAIL_NEEDED: ...]` — 待补方法细节
- `[RATIONALE_NEEDED: ...]` — 待补设计动机与预期收益

---

## 项目结构

```
academic-paper-writer/
├── SKILL.md                           # 核心技能定义：非协商规则、任务模式、工作流
├── agents/
│   └── openai.yaml                    # Agent 接口配置（OpenAI 等 LLM 平台适配）
└── references/                        # 结构化参考文档
    ├── paper-structure.md             # 论文结构与各节写作建议
    ├── writing-guidelines.md          # 风格适配、Claim 强度、去 AI 化规范
    ├── revision-loop.md               # 自检与迭代修订流程
    ├── reference-library.md           # 文献检索与引用映射
    ├── experiment-and-artifacts.md    # 实验复核与产物管理
    ├── test-scenarios.md              # 回归测试场景
    └── exemplar-sections/             # 经典论文章节范例
        ├── abstract.md
        ├── introduction.md
        ├── related-work.md
        ├── method.md
        └── experiments.md
```

---

## 快速开始

### 安装

本 Skill 无需额外依赖，可直接集成到支持 Skill 机制的 LLM Agent 平台（如 OpenCode、Claude Code 等）。

1. 将本仓库克隆或复制到你的 Skill 目录：
   ```bash
   git clone https://github.com/joshua-zyy/academic-paper-writer.git
   ```

2. 根据你使用的平台，在 Agent 配置中引用 `SKILL.md` 与 `agents/openai.yaml`。

### 使用示例

在 Agent 对话中，直接描述你的需求即可触发对应任务模式：

**示例 1：启动完整论文起草**
> "我有一个关于图神经网络的代码仓库，想写一篇投 NeurIPS 的论文，先帮我规划大纲，然后逐节推进。"

Agent 将自动进入 `full-paper-planning` 模式，依次输出：
- `Evidence Inventory`（证据盘点）
- `Venue / Language Brief`（目标会议与语言简报）
- `Outline / Section Queue`（论文大纲与章节队列）
- 串行 section loop：每节交付 Draft + Critique + Verification

**示例 2：撰写 Method 章节**
> "请根据我的代码，写 Method 章节。"

Agent 将自动进入 `section-drafting` 模式，优先确认目标 venue 与语言，然后：
- 审计代码结构与实验产物
- 划分核心 / 非显然设计选择 vs. 标准 / 支撑性组件
- 为每个核心模块生成 `Module Card`
- 输出带公式、输入输出、设计动机与边界的 Method 草稿

**示例 3：修订现有段落**
> "我这节 Introduction 的 claim 太强了，请帮我降强度并补引用。"

Agent 将自动进入 `section-revision` 模式，执行局部证据核验、claim 强度降级与引用补全。

---

## 工作流详解

### Step 0：判定任务模式与当前章节

- 先判断是 `full-paper-planning`、`section-drafting`、`section-revision`、`related-work-or-citation-pass` 还是 `experiment-evidence-pass`
- 若用户未指定章节但要求写论文，先生成 `Outline`，再进入串行 `section loop`

### Step 1：确认关键信息

- 目标期刊 / 会议
- 本轮草稿语言（默认英文，除非上下文强烈指向中文）
- 当前要写的 section

### Step 2：审计证据

- 轻量 inventory，不做无差别全仓库扫描
- 按当前 section 定点读取：代码、配置、日志、结果表、旧草稿等
- 判断论文类型：`empirical` / `theory` / `survey` / `reproducibility` / `position`

### Step 3：文献检索与核验

- 建立同领域 `Exemplar Set`，学习章节组织与论证顺序（不是复制措辞）
- 优先使用官方 proceedings、OpenReview、PMLR、ACL Anthology、arXiv、DBLP 等一级来源
- 只有 `VERIFIED` 文献才能写入正文；未核验条目保留在候选列表

### Step 4：实验复核（empirical paper）

- 识别可运行环境、入口命令、关键配置、checkpoint、输出目录
- 能运行则优先做"最小可复核执行"
- 不能运行则明确报告阻塞点，不得伪造结果

### Step 5：生成 Section Plan

- 按 `paper-structure.md` 选择结构，目标 venue 优先
- 生成 `Evidence Map` 与 `Section Blueprint`（或 `Method Blueprint`）
- 明确各段落承担的叙述职责

### Step 6：起草 Draft v1

- 默认输出 Markdown
- `Paper Body` 只放正文，审查备注进 sidecar
- 使用已核验文献和已确认事实写定论，缺证据处用占位符

### Step 6.3 ~ 6.5：Prose 质量闸门

- 通用 prose 检查：去提纲句、去元评论口吻、去代码讲解口吻
- Method 专项 prose 强化："问题 → 设计 → 机制 → 收益/边界"叙事

### Step 7：Expansion Pass

- 检查内容密度，优先补足读者理解链条，不靠臆造补长度

### Step 8：Self-Review & Verification

- 事实 / 证据检查 → 论证强度 / 审稿风险检查 → 结构 / 风格检查
- 输出 `Section Critique` 与 `Verification Status`
- 判定 `passed` / `failed` / `blocked`，并明确 `prose_debt`、`thin_draft`、`remaining_issues`

### Step 9：整合并继续 Section Loop

- 将当前节并入 `Cumulative Draft`
- 更新 `Section Queue` 与 `Revision Queue`
- 判断下一节是否应立即继续

---

## 注意事项

1. **不编造任何信息**
   - 不编造文献、作者、年份、venue、DOI、arXiv 编号
   - 不编造实验结果、图表、运行日志或命令

2. **区分证据类型**
   - `newly_run`：本轮实际运行的实验
   - `preexisting_artifact`：已有产物（checkpoint、日志、CSV）
   - `user_claim`：用户口述，无本地或外部证据支撑，需显式标注待核验

3. **Abstract / Conclusion 后置**
   - 默认在主要证据稳定后再写，避免用未核验结果充当摘要卖点

4. **双输出优先**
   - 默认同时交付 `paper body` 文件 + `sidecar critique / debt log` 文件
   - 不要把内部审查说明混进论文正文

5. **不是万能工具**
   - 本 Skill 是**写作代理**，不是实验运行器、不是文献数据库、不是 LaTeX 编译器
   - 它帮助你结构化地组织证据、生成 prose、控制 claim 强度，但无法替代你的原创研究与真实实验

---

## 贡献

欢迎通过 Issue 或 PR 提出建议与改进，特别是在以下方面：

- 补充更多领域的 `exemplar-sections` 范例
- 改进 `writing-guidelines.md` 的去 AI 化规则
- 扩展 `test-scenarios.md` 的覆盖场景
- 适配更多 LLM 平台的 `agents/*.yaml` 配置

---

## 许可

[MIT License](LICENSE)

---

> **免责声明**：本 Skill 旨在辅助学术写作的结构化与质量控制，最终论文的学术诚信、实验真实性与引用准确性由使用者本人负责。请始终遵守目标期刊/会议的投稿规范与学术伦理要求。
