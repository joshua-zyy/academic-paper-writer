---
name: academic-figure
description: "Create, revise, or audit academic figures for CS/AI/ML papers. Two paths: architecture figure prompting (tool-agnostic structured prompts) and data figure code generation (publication-ready Python scripts with matplotlib/seaborn). Use when: generating model architecture diagram prompts, creating publication-quality data plots from experiment results, auditing existing figures for publication standards, suggesting figure types for paper sections, revising figure colors/layouts/labels. Triggers on: 绘图, figure, chart, 画图, 实验图, 训练曲线, 消融实验, 对比图, 混淆矩阵, 架构图, model architecture, plot, publication figure, 数据可视化, generate plot, architecture diagram."
---

# Academic Figure

将此 skill 视为"学术论文图表代理"——负责 CS/AI/ML 论文中两类图表的生产：

| 路径 | 类型 | 产出方式 |
|------|------|---------|
| **A** | 实验数据图（训练曲线、消融实验、性能对比、混淆矩阵等） | Python (matplotlib/seaborn) 生成代码→执行→SVG/PDF/TIFF |
| **B** | 模型架构图（网络结构、流程图） | 生成结构化生图提示词→用户自行生图 |

## Red Lines（绝对禁止）

1. 禁止用虚构数据绘图——必须使用用户提供的实验数据或已核验的证据
2. 禁止使用彩虹/jet/viridis 等高饱和度非学术色板
3. 禁止在无 error bar 或统计信息时用强视觉效果暗示不确定性
4. 禁止在架构图中编造不存在的网络结构、模块连接或数据流
5. 禁止输出仅 PNG 位图——必须提供可编辑矢量格式（SVG/PDF）
6. 禁止在生图提示词中包含无法实现的渲染细节（如"完美 3D 透视"）
7. 禁止跳过 QA Contract

## AI 介入边界（Traffic Light）

| 🟢 Green — 直接执行 | 🟡 Yellow — 谨慎执行 | 🔴 Red — 禁止 |
|---------------------|---------------------|-------------|
| 从数据文件自动选择坐标范围 | 自动预设显著性水平（需确认用户预期） | 编造数据或网络结构 |
| 应用配色规则（学术色板、字体） | 猜测缺失的统计数据 | 输出最终出版版本未经 review |
| 添加 panel label (a/b/c/d) | 自动选择图类型（含糊请求须确认） | 用 3D 柱状图替代 2D |
| 标准布局排版与对齐 | 将多张分离图表合为 multi-panel | 使用色盲不友好的配色 |
| 检测缺失依赖包并提示安装 | 对架构图推测缺失的模块 | 把占位图当作最终输出 |

## 非协商规则

1. 图表必须服务 claim，不得为"好看"而堆砌视觉效果。
2. 每个 panel 必须回答一个独特问题，不得出现冗余面板。
3. 坐标轴从非零起点时必须标注截断标记，不得静默缩放。
4. 误差棒 / 置信区间必须标注含义（std / SEM / 95% CI），不得只画不解释。
5. 配色不得依赖纯色相作为唯一区分方式——必须结合亮度差、纹理或标注。
6. 向量输出（SVG/PDF）必须是文字可编辑格式，不得将所有文字渲染为 path。
7. 源数据（CSV/TSV）必须与图表同时交付，不得只给图片。
8. 架构图提示词必须是工具无关的描述式语言，不得内嵌特定工具参数（--ar、--style 等）。

## 任务模式

| Mode | 用途 |
|------|------|
| `chart-from-data` | 给定实验数据和图表类型，出实验数据图（Python 代码生成 + 执行） |
| `arch-prompt` | 给定模型结构描述，出架构图生图提示词 |
| `figure-blueprint` | 给定论文章节，建议需要哪些图和对应图表类型 |
| `figure-audit` | 审查现有 figure 是否符合发表标准 |
| `figure-revision` | 修改已有 figure（换色、调布局、加标注、修改风格） |

若用户请求含糊，优先选择最小满足需求的 mode。

## 工作流

### 入口分流

```
用户请求 → 判断图类型
  ├─ 实验数据图 → chart-from-data 模式
  └─ 模型架构图 → arch-prompt 模式

自动触发：academic-paper-writer 的 Step 6.4 在 Draft v1 完成后，会自动扫描正文中的 [FIGURE_NEEDED] 占位符，
对架构图类占位符以 arch-prompt 模式调用本 Skill 的生图提示词生成能力。
```

### 路径 A — chart-from-data（实验数据图）

详见 `references/workflow-chart-from-data.md`。核心步骤：确认用途 → 选择图表类型 → Figure Contract → 检查运行时 → 生成代码 → 执行导出 → QA Contract → 交付。

### 路径 B — arch-prompt（模型架构图）

详见 `references/workflow-arch-prompt.md`。核心步骤：确认模型结构 → 选择提示词模板 → 生成结构化提示词 → 输出 + 使用说明。

### figure-blueprint 模式

**Step 1**：确认论文上下文（章节结构、venue 图表惯例）。
**Step 2**：扫描章节，识别可图示化内容（方法流程→架构图，实验结果→训练曲线/对比图，分析→分布图/散点图）。
**Step 3**：输出建议清单（图类型、对应章节、核心 claim、数据来源、是否已有数据覆盖）。

### figure-audit 模式

**Step 1**：确认审查范围（单张图或全文所有图）。
**Step 2**：逐项执行 QA（详见 `references/qa-contract.md`）：核心结论、配色、可读性、统计信息、SVG 可编辑性、坐标轴伦理。
**Step 3**：输出审查报告（Figure、Verdict、Passed items、Failed items、Risk flags）。

### figure-revision 模式

**Step 1**：确认修改目标（文件路径、修改内容）。
**Step 2**：判断可执行路径（有脚本→修改重跑，仅有图片→简单调整，架构图→修改提示词）。
**Step 3**：执行修改 → QA → 交付。

## 默认交付物

### chart-from-data
1. Figure Contract
2. Python 绘图脚本
3. 源数据文件
4. SVG / PDF / TIFF
5. QA 报告

### arch-prompt
1. 架构分析说明
2. 生图提示词（通用格式）
3. 使用说明

### figure-blueprint
1. 针对当前章节的图类型建议列表
2. 每个建议图的核心 claim 与数据需求

### figure-audit
1. QA 判定清单（pass / fail per item）
2. 具体问题列表与修改建议

## Agent 资源

本 Skill 目录下的 `agents/` 文件夹包含以下辅助文件：

| 文件 | 用途 |
|------|------|
| `agents/figure_agent.md` | 图表类型选择与生成规范 |

**使用方式**：由 `academic-paper-writer` 核心编排器在 Step 6.4 委托时，按 `academic-paper-writer/references/workflow-step-5-8.md` 中的 dispatch 模板创建工具型子代理执行。**此 agent 只生成图表，绝对不得修改项目源代码、配置文件或数据文件，也不得独立撰写论文正文**。

## 何时读取 references/

| Reference 文件 | 打开条件 |
|---------------|---------|
| `references/api.md` | chart-from-data 模式的 Step 5（代码生成） |
| `references/chart-types.md` | chart-from-data 模式的 Step 2（类型选择） |
| `references/design-theory.md` | 所有涉及配图输出的场景（全局规范） |
| `references/architecture-prompting.md` | arch-prompt 模式（架构图提示词生成） |
| `references/figure-contract.md` | chart-from-data 模式的 Step 3 |
| `references/qa-contract.md` | chart-from-data 的 Step 7 / figure-audit 的 Step 2 |
| `references/tutorials.md` | 用户需要端到端参考示例时 |

## 终止条件

图表视为完成（可交付）须满足：

### chart-from-data
- 所有 QA 项 pass
- SVG 文字可编辑验证通过
- 源数据文件已随图交付
- 统计信息（误差棒含义、样本量、检验方法）已在图注中说明

### arch-prompt
- 提示词覆盖了核心组件、数据流、配色、标注
- 无特定生图工具的硬编码参数
- 提示词中无虚构的模块或连接

### figure-audit
- 所有审查项已完成判定
- Failed items 含具体修改建议

### figure-blueprint
- 每个建议的图表都有对应的 claim 和数据来源说明
- 无建议出不可执行的图表（如缺数据）

## 不适用场景

- 非学术文体的通用商业图表
- 需要交互式绘图（Plotly、Bokeh、D3.js）
- 已有 Adobe Illustrator / TikZ 完成图且无需修改
- 仅需数据统计汇报（EDA 图），无发表目标

## Anti-Patterns

| 模式 | 问题 | 正确做法 |
|------|------|---------|
| 美观优先 | 用彩虹/jet 色板使图表"好看" | 灰度安全色调 + 简洁明晰的学术风格 |
| 无 QA 出图 | 代码跑通就直接交付用户 | 必须经过 QA Contract：可读性、数据一致性、格式合规 |
| 硬编码路径 | 图中路径写死开发者本地路径 | 使用相对路径或参数化配置 |
| 虚构架构 | 生图提示词中包含不存在的模块连接 | 架构描述必须与代码/论文中的模块定义一致 |
