# Workflow: architecture-image

用于生成 CS/AI/ML 论文中的模型框架图、overview figure、复杂模块细节图或机制图。默认使用生图模型完成主体视觉，而不是用 Python/SVG 手工拼 boxes/arrows。

核心策略：agent 先做论文方法编辑和视觉导演，再写生图 prompt。不得从 Architecture Contract 直接跳到泛化 prompt；中间必须明确图的范围、阅读路径、信息密度、标签策略和画面分区。

## Step 0: Scope Gate

如果用户只说“画模型框架图/架构图/overview”，但缺少目标用途、证据来源或图的范围，先给出最小推荐并确认关键缺口。不要为了确认风格而阻塞已有充分证据的单图任务。

推荐范围：

| 需求 | 默认建议 |
|---|---|
| 论文/README 总览 | 1 张 framework/overview figure |
| 方法较复杂，含 2+ 核心机制 | 1 张 overview + 1-2 张 module detail |
| 需要解释训练/推理差异 | overview 中分层标注，或拆成 train/inference 两张 |
| 只缺一张投稿图 | 1 张双栏 paper-figure 风格架构图 |

必须确认或显式记录：

- Target use: paper submission / README / slide / graphical abstract.
- Figure count: one overview or multiple mechanism/detail figures.
- Language policy: short English labels / short Chinese labels / numbered callouts with external legend.
- Evidence status: confirmed / partial / needs verification.

若用户已经明确“生成一张双栏英文模型框架图”并提供足够结构证据，可直接进入 Step 1。

## Step 1: Architecture Contract

生成图片前必须先建立合约。没有合约不得生成架构图。

```markdown
## Architecture Contract

### Core Figure Claim
[该图要帮助读者理解的核心机制、系统流程或模型贡献]

### Evidence Source
- Source: [用户描述 / 论文草稿 / 代码文件 / README / 已确认图示]
- Confidence: [confirmed / partial / needs verification]

### Components
| ID | Label | Role | Evidence |
|----|-------|------|----------|
| C1 | [模块名] | [输入/编码器/融合/预测头/损失/检索器等] | [来源] |

### Data Flow
| From | To | Meaning | Evidence |
|------|----|---------|----------|
| C1 | C2 | [张量、特征、token、embedding、graph message 等] | [来源] |

### Unconfirmed Items
- [VERIFY_ARCH: 缺失的模块、连接、输入输出、训练路径或推理路径]
```

如果模型结构证据不足，先输出 `Unconfirmed Items` 并询问或标记待确认。允许生成带有 `[VERIFY_ARCH: ...]` 风险说明的概念草图，但不得把它标为最终投稿图。

## Step 2: Visual Director Brief

将 Architecture Contract 转换为具体到画面层级的视觉导演 brief。这里还不是 prompt，而是说明这张图到底如何让读者看懂方法。

```markdown
## Visual Director Brief

### Figure Role
[framework / overview / module detail / mechanism / graphical abstract]

### Canvas and Target
- Target use: [paper submission / README / slide]
- Aspect/column: [single-column / double-column / 16:9 / 4:3]
- Language policy: [short English labels / short Chinese labels / numbered callouts]

### Reading Path
[left-to-right / top-to-bottom / parallel branches converge / encoder-decoder bridge / central module with zoom-in]

### Layout Zones
- Zone A: [input and preprocessing, location, visual form]
- Zone B: [core module, location, visual form]
- Zone C: [output/head/loss/result inset, location, visual form]

### Element-Level Instructions
- [C1] appears as [box/token grid/matrix stack/graph/module group] at [location].
- Arrow [C1 -> C2] is [solid/dashed/color] and means [data flow].
- Add zoom-in/inset for [core mechanism] if needed.

### Mandatory Labels
- In-image labels: [only short labels, module names, variables, or callout numbers]
- External legend/caption: [long explanations, formulas, evidence notes]

### Information Density Decision
- Main diagram should occupy about 70-85% of the image area.
- If sparse: add module zoom-in, tensor shape, token/matrix example, before/after path, or attention/graph heatmap inset.
- If crowded: split into overview + mechanism detail instead of shrinking labels.

### Style Boundary
- Style: clean CS/AI/ML paper figure, white or near-white background, flat 2D vector-like modules, restrained academic palette.
- Avoid: decorative 3D, stock illustration, fake UI, fake datasets, performance numbers, long paragraphs, unreadable microtext.

### Overlay Plan
[none / SVG label overlay / PDF label overlay; explain which labels must be exact]
```

不要加入 Contract 之外的模块、数据集、损失、性能 claim、箭头或标签。

## Step 3: Image Generation Plan

从 Visual Director Brief 生成生图计划：

- Figure role: framework / overview / module detail / graphical abstract / mechanism.
- Composition: central framework / layered pipeline / multi-panel overview / module zoom-in / schematic-led composite.
- Direction: left-to-right / top-to-bottom / converging branches / circular or asymmetric hero layout.
- Label strategy: short labels, numbered callouts, or no embedded text with external legend. 避免让生图模型生成长段技术文字。
- Visual hierarchy: core module > auxiliary module > input/output > training/inference path.
- Overlay need: 是否需要后处理的可编辑 SVG/PDF 标注层来保证文字准确。

## Step 4: Generation Prompt

提示词必须从 Architecture Contract 和 Visual Director Brief 派生，证据约束、结构完整、空间描述具体、少长文字。推荐结构：

```text
Create a publication-quality scientific model architecture figure for [task/model].
White background, clean CS/AI/ML publication figure style, restrained academic palette,
clear module hierarchy, precise data-flow arrows, minimal text labels, numbered callouts.

Core components from evidence:
1. [C1 label]: [role]
2. [C2 label]: [role]

Data flow:
- [C1] -> [C2]: [meaning]

Composition:
[reading path and layout zones from Visual Director Brief]

Visual details:
- Main diagram occupies 70-85% of the canvas.
- Use [short labels / numbered callouts].
- Include [zoom-in / tensor shape / matrix grid / token example / graph inset] only if specified by the brief.

Text policy:
Use only short module labels or callout numbers. Avoid paragraphs and invented labels.

Negative constraints:
No unsupported modules, no fake datasets, no performance numbers, no decorative 3D clutter,
no unreadable tiny text, no watermark.
```

不要只写“高级、精美、顶会风格”。必须把画面分区、核心模块、箭头语义和标签策略写清楚。

## Step 5: Generate Image

优先使用可用的生图能力；在 Codex 环境中如可用，应调用 `imagegen` skill 或等价生图模型。建议输出：

```text
./docs/paper-drafts/figures/fig<N>_arch.png
```

可同时导出 WebP/TIFF 或高分辨率 PNG。若当前环境无法调用生图模型，交付 Architecture Contract、完整 generation prompt、目标路径和 blocker；不得伪造已生成图片。

## Step 6: Post-Generation Label and Overlay Pass

生成后必须检查文字和连接。如果图片中文字扭曲、模块名错误或箭头方向不一致：

1. 首选重新生成，减少内嵌文字，只保留编号/短标签。
2. 如需要精确排版，创建可编辑 SVG/PDF 标注层覆盖在图片上。
3. 不接受错误文字，不把 caption 当作修补错误图像的借口。

## Step 7: Verification

逐项核对，不只检查美观。

- 所有模块是否来自 Architecture Contract？
- 所有箭头方向是否与 Data Flow 一致？
- 图片是否执行了 Visual Director Brief 的阅读路径、布局分区、标签策略和信息密度决策？
- 图片中是否出现未确认的损失函数、数据集、指标、性能数字或公式？
- 是否存在错误、乱码、AI 生成的伪文字？
- 核心阅读路径是否清晰，视觉层级是否突出核心贡献？
- 主体图解是否占据约 70-85% 画面？若过空，是否补充了机制 inset、维度、矩阵/token/graph 示例或对比路径？
- 若画面拥挤，是否拆分为 overview + detail，而不是压缩文字？
- 分辨率是否满足目标版面，缩放后短标签/编号是否可读？
- 是否存在 `[VERIFY_ARCH: ...]` 未确认项？若存在，不得标记为最终投稿图。

## Step 8: Delivery

默认交付：

- Generated image path
- Generation prompt
- Architecture Contract
- Visual Director Brief
- Optional editable annotation overlay path
- Caption Draft
- Verification Report

仅当用户明确要求简单可编辑矢量图时，才转入 `architecture-svg` 兼容路径。仅当用户明确要求外部生图提示词且不需要本轮出图时，才转入 `arch-prompt`。
