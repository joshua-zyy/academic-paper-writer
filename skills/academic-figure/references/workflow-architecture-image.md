# Workflow: architecture-image

用于生成 CS/AI/ML 论文中的模型框架图、overview figure、复杂模块细节图或机制图。默认使用生图模型完成主体视觉，而不是用 Python/SVG 手工拼 boxes/arrows。

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

## Step 2: Image Generation Plan

将 Architecture Contract 转换为生图计划：

- Figure role: framework / overview / module detail / graphical abstract / mechanism.
- Composition: central framework / layered pipeline / multi-panel overview / module zoom-in / schematic-led composite.
- Direction: left-to-right / top-to-bottom / converging branches / circular or asymmetric hero layout.
- Label strategy: short labels, numbered callouts, or no embedded text with external legend. 避免让生图模型生成长段技术文字。
- Visual hierarchy: core module > auxiliary module > input/output > training/inference path.
- Overlay need: 是否需要后处理的可编辑 SVG/PDF 标注层来保证文字准确。

不要加入 Contract 之外的模块、数据集、损失、性能 claim、箭头或标签。

## Step 3: Generation Prompt

提示词必须证据约束、结构完整、少长文字。推荐结构：

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
[left-to-right layered pipeline / multi-branch fusion / central overview / module zoom-in]

Text policy:
Use only short module labels or callout numbers. Avoid paragraphs and invented labels.

Negative constraints:
No unsupported modules, no fake datasets, no performance numbers, no decorative 3D clutter,
no unreadable tiny text, no watermark.
```

## Step 4: Generate Image

优先使用可用的生图能力；在 Codex 环境中如可用，应调用 `imagegen` skill 或等价生图模型。建议输出：

```text
./docs/paper-drafts/figures/fig<N>_arch.png
```

可同时导出 WebP/TIFF 或高分辨率 PNG。若当前环境无法调用生图模型，交付 Architecture Contract、完整 generation prompt、目标路径和 blocker；不得伪造已生成图片。

## Step 5: Post-Generation Label and Overlay Pass

生成后必须检查文字和连接。如果图片中文字扭曲、模块名错误或箭头方向不一致：

1. 首选重新生成，减少内嵌文字，只保留编号/短标签。
2. 如需要精确排版，创建可编辑 SVG/PDF 标注层覆盖在图片上。
3. 不接受错误文字，不把 caption 当作修补错误图像的借口。

## Step 6: Verification

逐项核对，不只检查美观。

- 所有模块是否来自 Architecture Contract？
- 所有箭头方向是否与 Data Flow 一致？
- 图片中是否出现未确认的损失函数、数据集、指标、性能数字或公式？
- 是否存在错误、乱码、AI 生成的伪文字？
- 核心阅读路径是否清晰，视觉层级是否突出核心贡献？
- 分辨率是否满足目标版面，缩放后短标签/编号是否可读？
- 是否存在 `[VERIFY_ARCH: ...]` 未确认项？若存在，不得标记为最终投稿图。

## Step 7: Delivery

默认交付：

- Generated image path
- Generation prompt
- Architecture Contract
- Optional editable annotation overlay path
- Caption Draft
- Verification Report

仅当用户明确要求简单可编辑矢量图时，才转入 `architecture-svg` 兼容路径。仅当用户明确要求外部生图提示词且不需要本轮出图时，才转入 `arch-prompt`。
