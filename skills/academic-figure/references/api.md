# Python API 参考

CS/AI/ML 论文图表的 Python 辅助函数库。agent 在 `chart-from-data` 模式的 Step 5 中调用此处的常量和函数。

## 色板

```python
# CS/AI/ML 学术色板（色盲友好，灰度打印友好）
PALETTE = ["#3B6BA5", "#E8822B", "#5DA85D", "#C44E52", "#8A5B9E", "#5D8A8A", "#B87A4A"]

PALETTE_ABLATION = ["#3B6BA5", "#7BA0CC", "#A0C4E8", "#C4D8F0"]

PALETTE_COMPARISON = ["#3B6BA5", "#C44E52", "#5DA85D", "#E8822B", "#8A5B9E"]

PALETTE_HEATMAP = ["#FFFFFF", "#DCE4F0", "#9BB7D4", "#5D8AB5", "#1A3A5C"]

CMAP_DIVERGING = "RdBu_r"
```

## 全局样式

```python
import matplotlib
matplotlib.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
    "font.size": 8,
    "axes.titlesize": 9,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "legend.frameon": False,
    "legend.handlelength": 1.5,
    "figure.subplot.left": 0.12,
    "figure.subplot.right": 0.95,
    "figure.subplot.bottom": 0.12,
    "figure.subplot.top": 0.95,
})


def apply_pub_style():
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
    })
```

## 图表生成器

### 训练曲线

```python
def make_training_curve(data, x_col="epoch", y_cols=None, std_cols=None,
                        labels=None, colors=None, figsize=(4, 3),
                        xlabel="Epoch", ylabel="Loss/Accuracy",
                        show_legend=True):
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=figsize)
    if colors is None:
        colors = PALETTE

    for i, col in enumerate(y_cols):
        x = data[x_col].values
        y = data[col].values
        color = colors[i % len(colors)]
        label = labels[i] if labels else col

        ax.plot(x, y, color=color, linewidth=1.2, label=label, zorder=3)

        if std_cols and i < len(std_cols):
            std = data[std_cols[i]].values
            ax.fill_between(x, y - std, y + std, color=color,
                            alpha=0.15, linewidth=0, zorder=2)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if show_legend:
        ax.legend()
    apply_pub_style()
    return fig, ax
```

### 分组柱状图（含 error bar）

```python
def make_grouped_bar(data, group_col, value_col, error_col=None,
                     hue_col=None, figsize=(4, 3),
                     xlabel=None, ylabel=None, colors=None):
    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=figsize)
    if colors is None:
        colors = PALETTE

    if hue_col is None:
        groups = data[group_col].unique()
        values = data[value_col].values
        x = range(len(groups))
        ax.bar(x, values, color=colors[0], width=0.6, zorder=3)
        if error_col and error_col in data.columns:
            err = data[error_col].values
            ax.errorbar(x, values, yerr=err, fmt="none", ecolor="black",
                        capsize=3, capthick=0.8, elinewidth=0.8, zorder=4)
        ax.set_xticks(x)
        ax.set_xticklabels(groups)
    else:
        sns.barplot(data=data, x=group_col, y=value_col, hue=hue_col,
                    palette=colors, ax=ax, edgecolor="black", linewidth=0.5,
                    errorbar=("ci", 95) if error_col is None else None)
        if error_col and error_col in data.columns:
            _overlay_errorbars(ax, data, group_col, value_col, hue_col, error_col)

    ax.set_xlabel(xlabel or group_col)
    ax.set_ylabel(ylabel or value_col)
    apply_pub_style()
    return fig, ax


def _overlay_errorbars(ax, data, group_col, value_col, hue_col, error_col):
    """在 seaborn barplot 上手动叠加 error bar。统计每个 (group, hue) 的均值和误差。"""
    grouped = data.groupby([group_col, hue_col])[value_col]
    means = grouped.mean()
    errs = data.groupby([group_col, hue_col])[error_col].mean()
    labels = list(grouped.groups.keys())
    n_groups = len(data[group_col].unique())
    n_hues = len(data[hue_col].unique())

    for i, (g_val, h_val) in enumerate(labels):
        group_idx = list(data[group_col].unique()).index(g_val)
        hue_idx = list(data[hue_col].unique()).index(h_val)
        offset = (hue_idx - (n_hues - 1) / 2) * 0.8 / n_hues
        x = group_idx + offset
        y = means.loc[(g_val, h_val)]
        yerr = errs.loc[(g_val, h_val)]
        ax.errorbar(x, y, yerr=yerr, fmt="none", ecolor="black",
                    capsize=3, capthick=0.8, elinewidth=0.8, zorder=4)


### 热力图

```python
def make_heatmap(matrix, xticklabels=None, yticklabels=None,
                 cmap=None, figsize=(4, 3.5),
                 annot=True, fmt=".2f", cbar_label=None,
                 vmin=None, vmax=None):
    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=figsize)
    if cmap is None:
        cmap = sns.color_palette(PALETTE_HEATMAP, as_cmap=True)

    sns.heatmap(matrix, xticklabels=xticklabels, yticklabels=yticklabels,
                cmap=cmap, annot=annot, fmt=fmt, cbar=True,
                linewidths=0.3, linecolor="white",
                vmin=vmin, vmax=vmax, ax=ax,
                cbar_kws={"shrink": 0.8, "label": cbar_label or ""})
    apply_pub_style()
    return fig, ax
```

### 散点图（聚类）

```python
def make_scatter(embeddings, labels=None, colors=None, figsize=(4, 4),
                 xlabel="Component 1", ylabel="Component 2",
                 alpha=0.7, s=8, legend=True):
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=figsize)
    if colors is None:
        colors = PALETTE

    if labels is not None:
        unique_labels = np.unique(labels)
        for i, label in enumerate(unique_labels):
            mask = labels == label
            ax.scatter(embeddings[mask, 0], embeddings[mask, 1],
                       color=colors[i % len(colors)], s=s, alpha=alpha,
                       label=str(label), edgecolors="none", zorder=3)
        if legend:
            ax.legend(markerscale=2)
    else:
        ax.scatter(embeddings[:, 0], embeddings[:, 1],
                   color=colors[0], s=s, alpha=alpha,
                   edgecolors="none", zorder=3)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    apply_pub_style()
    return fig, ax
```

### 箱线图

```python
def make_boxplot(data, category_col, value_col, hue_col=None,
                 figsize=(4, 3), xlabel=None, ylabel=None, colors=None):
    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=figsize)
    if colors is None:
        colors = PALETTE

    if hue_col:
        sns.boxplot(data=data, x=category_col, y=value_col, hue=hue_col,
                    palette=colors, ax=ax, linewidth=0.8, fliersize=2)
    else:
        sns.boxplot(data=data, x=category_col, y=value_col,
                    palette=colors, ax=ax, linewidth=0.8, fliersize=2)

    ax.set_xlabel(xlabel or category_col)
    ax.set_ylabel(ylabel or value_col)
    apply_pub_style()
    return fig, ax
```

### 雷达图

```python
def make_radar(categories, values_list, labels=None, colors=None,
               figsize=(4, 4), ylim=None):
    import matplotlib.pyplot as plt
    import numpy as np

    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))
    if colors is None:
        colors = PALETTE

    for i, values in enumerate(values_list):
        values_closed = values + values[:1]
        ax.plot(angles, values_closed, color=colors[i % len(colors)],
                linewidth=1.2, label=labels[i] if labels else f"Method {i+1}")
        ax.fill(angles, values_closed, color=colors[i % len(colors)], alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=7)
    if ylim:
        ax.set_ylim(ylim)
    if labels:
        ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    apply_pub_style()
    return fig, ax
```

### 消融实验专用

```python
def make_ablation(baseline_label, ablation_cols, values,
                  errors=None, figsize=(4, 3.5),
                  ylabel="Performance", colors=None):
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=figsize)
    all_labels = [baseline_label] + ablation_cols
    x = range(len(all_labels))

    if colors is None:
        colors = PALETTE_ABLATION[:len(all_labels)]

    ax.bar(x, values, color=colors, width=0.6,
           edgecolor="black", linewidth=0.5, zorder=3)
    if errors:
        ax.errorbar(x, values, yerr=errors, fmt="none", ecolor="black",
                    capsize=3, capthick=0.8, elinewidth=0.8, zorder=4)

    ax.set_xticks(x)
    ax.set_xticklabels(all_labels, rotation=15, ha="right")
    ax.set_ylabel(ylabel)
    apply_pub_style()
    return fig, ax
```

## 多面板组合说明

上述辅助函数均内部调用 `plt.subplots()` 创建独立的 Figure。在 multi-panel 场景下不应直接调用这些函数，而应使用原生 matplotlib 控制布局：

```python
fig = plt.figure(figsize=(7.5, 3.5))
gs = fig.add_gridspec(1, 2, wspace=0.4)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# 手动在各自的 axes 上绘制
sns.lineplot(data=train_data, x="epoch", y="ours_mean", ax=ax1)
ax1.fill_between(train_data["epoch"],
                 train_data["ours_mean"] - train_data["ours_std"],
                 train_data["ours_mean"] + train_data["ours_std"],
                 alpha=0.15)
# ... 更多手动绘图调用

finalize_figure(fig, "multi_panel")
```

## 导出

```python
def finalize_figure(fig, name, formats=("svg", "pdf", "tiff"), dpi=300):
    if "svg" in formats:
        fig.savefig(f"{name}.svg", format="svg")
    if "pdf" in formats:
        fig.savefig(f"{name}.pdf", format="pdf")
    if "tiff" in formats or "tif" in formats:
        fig.savefig(f"{name}.tiff", format="tiff", dpi=dpi)
    print(f"Exported: {name}.{', '.join(formats)}")
```
