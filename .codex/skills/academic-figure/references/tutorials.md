# Tutorials: 端到端示例教程

## 教程 1：训练曲线（chart-from-data）

### 用户输入
"我有三个方法在 ImageNet 上的训练 loss 数据，帮我画出训练曲线对比图。"

### 数据文件（train_loss.csv）
```csv
epoch,ours_mean,ours_std,baseline_a_mean,baseline_a_std,baseline_b_mean,baseline_b_std
1,2.85,0.12,3.12,0.15,3.45,0.18
5,1.72,0.08,2.01,0.10,2.33,0.12
10,0.95,0.05,1.22,0.07,1.51,0.09
15,0.62,0.04,0.85,0.06,1.08,0.07
20,0.45,0.03,0.62,0.05,0.82,0.06
30,0.32,0.02,0.48,0.04,0.61,0.05
40,0.28,0.02,0.42,0.03,0.55,0.04
50,0.25,0.02,0.39,0.03,0.51,0.04
```

### Figure Contract
```
Core Conclusion: 本方法的收敛速度更快且最终 loss 更低
Archetype: training-curve
Panels: 1 panel (全部方法在同一张图对比)
```

### 生成代码
```python
import pandas as pd
from api import make_training_curve, finalize_figure, PALETTE

data = pd.read_csv("train_loss.csv")

fig, ax = make_training_curve(
    data,
    x_col="epoch",
    y_cols=["ours_mean", "baseline_a_mean", "baseline_b_mean"],
    std_cols=["ours_std", "baseline_a_std", "baseline_b_std"],
    labels=["Ours", "Baseline A", "Baseline B"],
    colors=[PALETTE[0], PALETTE[2], PALETTE[3]],
    xlabel="Epoch",
    ylabel="Training Loss",
    figsize=(4, 3),
)

finalize_figure(fig, "training_curve")
```

### 输出
- training_curve.svg
- training_curve.pdf
- training_curve.tiff
- train_loss.csv（源数据）

---

## 教程 2：消融实验（chart-from-data）

### 用户输入
"我们做了消融实验，验证注意力机制和残差连接的贡献，帮我画柱状图。"

### 数据
```csv
variant,accuracy,std
Full Model,92.5,1.2
w/o Attention,88.3,1.5
w/o Residual,87.1,1.4
w/o Both,83.6,1.8
```

### 生成代码
```python
import pandas as pd
from api import make_ablation, finalize_figure

data = pd.read_csv("ablation.csv")

fig, ax = make_ablation(
    baseline_label="Full Model",
    ablation_cols=["w/o Attention", "w/o Residual", "w/o Both"],
    values=data["accuracy"].tolist(),
    errors=data["std"].tolist(),
    ylabel="Accuracy (%)",
    figsize=(4, 3.5),
)

finalize_figure(fig, "ablation_study")
```

---

## 教程 3：混淆矩阵（chart-from-data）

### 用户输入
"我有个 4 类分类的结果，画混淆矩阵。"

### 生成代码
```python
import numpy as np
from api import make_heatmap, finalize_figure

cm = np.array([[920, 35, 25, 20],
               [30, 890, 45, 35],
               [20, 40, 910, 30],
               [15, 25, 35, 925]])

classes = ["Class A", "Class B", "Class C", "Class D"]

fig, ax = make_heatmap(
    matrix=cm,
    xticklabels=classes,
    yticklabels=classes,
    annot=True,
    fmt="d",
    figsize=(4, 3.5),
    cbar_label="Count",
)

finalize_figure(fig, "confusion_matrix")
```

---

## 教程 4：模型架构图（arch-prompt）

### 用户输入
"帮我生成一个 Vision Transformer 架构图的生图提示词，用在论文 Model 部分。"

### 输出
```markdown
## Architecture Analysis

Architecture: Vision Transformer (ViT)
Components: Patch Embedding → [Transformer Encoder × 12] → MLP Head

## Prompt

Scientific diagram of a Vision Transformer (ViT) architecture, white background,
flat 2D vector illustration style, clean and minimal.

Layout: left to right flow with vertical expansion for the encoder block.

Components:
1. [Blue] Input Image: H x W x C
   → Patch Embedding: [P x P patches, linear projection to D dimensions]
   → [Position embedding added, [CLS] token prepended]
2. [Gray arrow]
3. Large vertical block "Transformer Encoder × 12 layers":
   - [Light green] Layer Norm
   - [Light green] Multi-Head Self-Attention: 12 heads, head_dim = 64
     ← [dashed arrow] residual connection
   - [Light green] Layer Norm
   - [Light green] MLP: D → 4D → D (GELU activation)
     ← [dashed arrow] residual connection
4. [Gray arrow]
5. [Orange] MLP Head: [CLS] token → Layer Norm → Linear → num_classes
6. [Red] Output: class prediction

Colors:
- Blue: input processing
- Green: transformer encoder layers
- Orange: classification head
- Red: output
- Gray dashed: residual connections

Annotations:
- [CLS] token marked with a distinct symbol
- Embedding dimension D labeled at key connection points
- Each component labeled with technical name in Arial 10pt
```

## Tutorial 5: Multi-panel 实验图（chart-from-data）

### 用户输入
"我们需要一个 2-panel 图，左边是训练曲线，右边是最后的性能对比柱状图。"

### Figure Contract
```
Core Conclusion: 本方法收敛更快且最终性能最优
Archetype: multi-panel (2 panels)
Panel (a): 训练曲线（ours vs 2 baselines）
Panel (b): 最终性能对比柱状图（3 方法 × 3 数据集）
```

### 生成代码框架
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from api import apply_pub_style, finalize_figure, PALETTE

train_data = pd.read_csv("train_loss.csv")
perf_data = pd.read_csv("performance.csv")

fig = plt.figure(figsize=(7.5, 3))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.2], wspace=0.4)

# Panel (a): 训练曲线（手动在 ax1 上绘制）
ax1 = fig.add_subplot(gs[0])
colors = [PALETTE[0], PALETTE[2], PALETTE[3]]
labels = ["Ours", "Baseline A", "Baseline B"]
for i, (col, std_col) in enumerate(zip(
    ["ours_mean", "baseline_a_mean", "baseline_b_mean"],
    ["ours_std", "baseline_a_std", "baseline_b_std"],
)):
    x = train_data["epoch"].values
    y = train_data[col].values
    s = train_data[std_col].values
    ax1.plot(x, y, color=colors[i], linewidth=1.2, label=labels[i])
    ax1.fill_between(x, y - s, y + s, color=colors[i], alpha=0.15, linewidth=0)
ax1.set_title("(a) Training Convergence", fontsize=9, fontweight="bold", loc="left")
ax1.set_xlabel("Epoch")
ax1.set_ylabel("Training Loss")
ax1.legend()

# Panel (b): 性能对比柱状图（sns 直接绘制）
ax2 = fig.add_subplot(gs[1])
sns.barplot(data=perf_data, x="dataset", y="score", hue="method",
            palette=[PALETTE[0], PALETTE[2], PALETTE[3]], ax=ax2,
            edgecolor="black", linewidth=0.5)
ax2.set_title("(b) Performance Comparison", fontsize=9, fontweight="bold", loc="left")
ax2.set_ylabel("Accuracy (%)")

apply_pub_style()
finalize_figure(fig, "multi_panel_experiment")
```
