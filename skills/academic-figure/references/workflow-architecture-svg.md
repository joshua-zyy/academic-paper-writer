# Workflow: architecture-svg

用于直接生成 CS/AI/ML 论文中的可编辑模型架构 SVG。该路径适用于用户要求“画架构图”“生成 SVG”“可投稿/可编辑架构图”，或 `academic-paper-writer` 在正文中发现架构图类 `[FIGURE_NEEDED]` 占位符时。

## Step 1: Architecture Contract

在写 SVG 前先建立合约。没有合约不得绘图。

```markdown
## Architecture Contract

### Core Figure Claim
[该架构图要帮助读者理解的核心机制或系统流程]

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

### Target Output
- File: `figures/architecture_fig<N>.svg`
- Width: [single-column / double-column / full-width]
- Caption need: [yes/no]
```

如果模型结构证据不足，停止绘图，输出 `Unconfirmed Items`，不要靠常识补模块。

## Step 2: Layout Plan

按论文叙事选择最简单的布局。

| Layout | 使用场景 | 默认方向 |
|--------|----------|----------|
| `left-to-right pipeline` | 预处理、编码、融合、预测的顺序流程 | 左到右 |
| `encoder-decoder` | Transformer、seq2seq、autoencoder、生成模型 | 左到右或上下 |
| `dual-branch fusion` | 多模态、双视图、双分支特征融合 | 两路汇入中部 |
| `retrieval-augmented pipeline` | RAG、检索增强、知识库辅助模型 | query 与 corpus 分层 |
| `graph/neural module stack` | GNN、message passing、多层模块 | 层叠或循环箭头 |
| `training-inference split` | 训练损失与推理路径不同 | 上下双泳道 |

布局计划必须说明：
- 主阅读路径
- 哪些模块是核心模块，哪些是辅助模块
- 箭头语义（data flow、supervision、skip connection、feedback）
- 颜色语义（数据、模型模块、损失、输出、外部资源）

## Step 3: SVG Generation Rules

生成原生 SVG，不生成截图式 SVG。

必须满足：
- 使用 `<svg>`、`<rect>`、`<path>`、`<line>`、`<polyline>`、`<text>`、`<marker>` 等原生元素。
- 所有文字保留为 `<text>`，不得转 path。
- 所有数据流箭头使用 `<marker>` 和 `marker-end` / `marker-start`。
- 白底或透明底，低饱和配色，适合双栏论文缩放。
- 字体使用 Arial、Helvetica、DejaVu Sans 或 sans-serif fallback。
- 模块标签短而稳定，必要时用图注解释细节。
- 不使用 `<image>` 嵌入 PNG/JPG 作为主体。

禁止：
- 编造未确认模块、连接、损失函数、数据集或输入输出。
- 使用花哨 3D、阴影堆叠、渐变光效来暗示不存在的机制。
- 在 SVG 内写本地绝对路径或暴露私有文件名。
- 用颜色作为唯一语义通道；必要时结合 label、线型或分组标题。

## Step 4: Caption Draft

图注应包含：
- 图展示的模型或系统名称
- 输入、核心处理路径、输出
- 关键创新模块的作用
- 若存在训练/推理差异，明确哪条路径属于训练或推理

不要在图注中加入未被实验或文本支持的性能 claim。

## Step 5: SVG QA

生成后必须运行：

```powershell
python skills/academic-figure/scripts/qa_figure.py --input <svg_path> --type architecture-svg
```

若目标 venue 已知，同时传入：

```powershell
python skills/academic-figure/scripts/qa_figure.py --input <svg_path> --type architecture-svg --venue neurips
```

QA 必须检查：
- SVG text 可编辑
- 无 banned colormap
- 配色灰度可辨
- 尺寸不超过 venue 限制
- 架构图含 `<text>` 标签、箭头 marker、无 raster-only `<image>`

QA 失败时最多修订 2 轮。2 轮后仍失败，交付当前文件时必须标明失败项。

## Step 6: Delivery

默认交付：
- `figures/architecture_fig<N>.svg`
- Architecture Contract
- Layout Plan
- Caption Draft
- QA Report

如果由 `academic-paper-writer` 自动调用，不在对话中输出完整 SVG 源码，只写入文件并输出简短摘要。
