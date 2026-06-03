# Workflow: architecture-svg

用于生成 CS/AI/ML 论文中的模型框架图、overview figure、复杂模块细节图或机制流程图。默认输出为可编辑 SVG，而不是 prompt 或 raster image。

## Step 1: Architecture Contract

生成 SVG 前必须先建立合约。没有合约不得绘制架构图。

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

如果模型结构证据不足，先输出 `Unconfirmed Items`。允许生成带有 `[VERIFY_ARCH: ...]` 标注的 SVG 草图，但不得把它标为最终投稿图。

## Step 2: SVG Layout Plan

将 Architecture Contract 转换为可绘制布局计划：

- Composition: central overview / layered pipeline / module zoom-in / multi-panel overview
- Direction: left-to-right / top-to-bottom / radial / grouped blocks
- Drawing primitives: rounded boxes, arrows, grouping frames, callouts, matrices, mini-plots
- Label strategy: short module labels only; long explanations move to caption
- Visual hierarchy: core module > auxiliary module > input/output > training/inference path

不要加入 Contract 之外的模块、数据集、损失、性能 claim、箭头或标签。

## Step 3: Python Vector Drawing Script

生成 Python 绘图脚本，默认使用 matplotlib patches/text/annotate 绘制矢量元素。

脚本必须设置：

```python
import matplotlib as mpl

mpl.rcParams.update({
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
})
```

脚本保存到：

```text
./docs/paper-drafts/figures/codes/draw_fig<N>_arch.py
```

## Step 4: Generate Editable SVG

执行脚本生成：

```text
./docs/paper-drafts/figures/fig<N>_arch.svg
```

若当前 Python 或 matplotlib 不可用，交付可运行脚本、Architecture Contract 和缺失依赖说明；不得降级为 prompt 作为默认最终图。

## Step 5: Caption Draft

图注应覆盖：

- 图展示的模型或系统名称
- 输入、核心处理路径、输出
- 关键创新模块的作用
- 训练/推理路径差异（如有）
- 图中编号 callout 的解释

不要在图注中加入未被实验或文本支持的性能 claim。

## Step 6: Verification

逐项核对 SVG，不只检查美观。

### Required checks

- 所有模块是否来自 Architecture Contract？
- 所有箭头方向是否与 Data Flow 一致？
- SVG 中是否出现了未确认的损失函数、数据集、指标、性能数字或公式？
- 标签是否准确、可读、无乱码？
- 文字是否保持为可编辑 SVG text？
- 是否把复杂文字移入 caption 或编号图例？
- 视觉层级是否突出核心贡献，而非平均铺满所有模块？
- 是否存在 `[VERIFY_ARCH: ...]` 未确认项？若存在，不得标记为最终投稿图。

## Step 7: Delivery

默认交付：

- `./docs/paper-drafts/figures/fig<N>_arch.svg`
- `./docs/paper-drafts/figures/codes/draw_fig<N>_arch.py`
- Architecture Contract
- Caption Draft
- Verification Report

仅当用户明确要求外部生图工具提示词时，才转入 `arch-prompt` 路径。
