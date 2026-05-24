# Workflow: architecture-image

用于生成 CS/AI/ML 论文中的模型框架图、overview figure、复杂模块细节图或 graphical abstract。该路径使用 Codex 的 image generation 能力生成高质量 raster image，而不是用 SVG 直接绘制模型结构。

## Step 1: Architecture Contract

生成图片前必须先建立合约。没有合约不得调用 image generation。

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

如果模型结构证据不足，先输出 `Unconfirmed Items`。允许生成“概念草图”，但不得把它标为最终投稿图。

## Step 2: Image Prompt Spec

将合约转换为 image prompt。Prompt 必须约束图片不要编造结构。

```text
Use case: scientific-educational
Asset type: high-impact journal model framework figure
Primary request: [用一句话描述要生成的模型框架图]
Subject: [模型名称和核心模块]
Composition/framing: [central overview / layered pipeline / module zoom-in / multi-panel overview]
Style/medium: polished scientific illustration, high-impact journal figure, clean white background
Color palette: low-saturation scientific palette, neutral base with one signal color and one accent color
Text strategy: short module labels only; use numbered callouts for details; no long paragraphs in the image
Required modules: [来自 Architecture Contract 的模块列表]
Required flows: [来自 Architecture Contract 的连接列表]
Caption will explain: [不适合放进图里的细节]
Constraints: do not add modules, datasets, losses, claims, arrows, or labels not listed in the contract
Avoid: decorative 3D, photorealistic lab scenes, busy gradients, unreadable tiny text, invented equations, invented performance numbers, watermark
```

## Step 3: Generate Image

默认使用内置 `image_gen`。不要在 prompt 中要求输出 SVG。输出定位为：

- `PNG`：预览、论文草稿、内部迭代
- `TIFF` 或高分辨率 `PNG`：投稿前版本

生成后保存：
- 图片文件
- 最终 prompt
- Architecture Contract
- Caption Draft

## Step 4: Caption Draft

图注应覆盖：
- 图展示的模型或系统名称
- 输入、核心处理路径、输出
- 关键创新模块的作用
- 训练/推理路径差异（如有）
- 图片中编号 callout 的解释

不要在图注中加入未被实验或文本支持的性能 claim。

## Step 5: Verification

逐项核对图片，不只检查美观。

### Required checks

- 所有模块是否来自 Architecture Contract？
- 所有箭头方向是否与 Data Flow 一致？
- 图片中是否出现了未确认的损失函数、数据集、指标、性能数字或公式？
- 标签是否准确、可读、无乱码？
- 是否把复杂文字移入 caption 或编号图例？
- 视觉层级是否突出核心贡献，而非平均铺满所有模块？
- 是否存在 `[VERIFY_ARCH: ...]` 未确认项？若存在，不得标记为最终投稿图。

## Step 6: Delivery

默认交付：
- `figures/architecture_fig<N>.png` 或 `.tiff`
- `figures/architecture_fig<N>_prompt.md`
- Architecture Contract
- Caption Draft
- Verification Report

若 image generation 不可用，降级为 `arch-prompt`，只交付外部生图工具可用的 prompt 和 contract。
