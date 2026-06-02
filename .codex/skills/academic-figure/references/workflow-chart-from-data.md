# chart-from-data 工作流

## 入口

用户请求 → 判断为实验数据图 → chart-from-data 模式

## Step 1：确认图表用途与核心结论

- 谁在什么数据上做了什么对比？
- 支持论文中的哪个 claim？
- 目标期刊/会议的图表规范（宽度、格式、dpi）
- 每个 panel 是否提供独特证据？不能支撑核心 claim 的 panel 应删除或合并。
- skeptical reviewer 最可能质疑什么：样本量、统计检验、baseline、公平性、坐标轴还是数据选择？

输出一句话 `Core conclusion`，后续图形选择和视觉层级都服务这句话。

## Step 1b：判断 Figure Archetype

借鉴 high-impact journal figure workflow，先判断图在论文中的角色，而不是直接套 chart type。

| Archetype | 使用场景 | 布局倾向 |
|-----------|----------|----------|
| `quantitative grid` | 多数据集、多指标、多方法比较 | 对齐轴线、共享 legend、紧凑网格 |
| `hero metric + supports` | 一个主结果 + 若干稳健性/消融支持 | 主 panel 更大，support panels 更安静 |
| `ablation ladder` | 逐步移除/替换模块验证贡献 | 同色系透明度或亮度递进 |
| `trend with uncertainty` | 训练曲线、scaling law、时间趋势 | line + CI/std band，直接标注关键事件 |
| `distribution comparison` | 多组分布、误差、稳定性 | box/violin/point-range，避免只看均值 |

## Step 2：选择图表类型

根据数据维度和 claim 类型匹配最佳图表：

| 数据特征 | 推荐图表类型 |
|---------|-------------|
| 单变量随 epoch 变化（多条方法） | 训练/验证曲线（line + std band） |
| 离散分组 + 数值（含 baseline） | 分组柱状图（+ error bar） |
| 矩阵形式（分类结果、相关性） | 热力图（混淆矩阵） |
| 高维嵌入（t-SNE/UMAP output） | 散点图（聚类着色） |
| 多轮实验分布 | 箱线图 / 小提琴图 |
| 多维度对比（速度/精度/参数量） | 雷达图 |
| 多数据集效果汇总 | 森林图 / 点范围图 |

详见 `references/chart-types.md`。

## Step 3：生成 Figure Contract

含核心结论、图表类型、面板映射、目标 venue 要求。详见 `references/figure-contract.md`。

Figure Contract 必须包含：
- `Core Conclusion`
- `Evidence Hierarchy`
- `Figure Archetype`
- `Panel Mapping`
- `Reviewer Risk`
- `Export Bundle`

若用户只给数据、没有说明 claim，先从数据请求中推断 provisional claim，并在输出中标记 `claim_needs_confirmation: yes`。

## Step 4：检查 Python 运行时

```python
required = ["matplotlib", "seaborn", "numpy", "pandas", "scipy"]
```

若缺失 → 报告 blocker 并提供安装命令，不得自动 fallback。

## Step 5：生成 Python 代码

- 使用 `references/api.md` 中定义的辅助函数
- 设置全局样式：`apply_pub_style()`
- 按合约布局生成各面板
- 代码中嵌入数据读取（CSV/TSV/Numpy）
- 使用色板 `PALETTE`（参考 `references/design-theory.md`）
- 多方法同族比较优先使用低饱和 `NMI pastel` 色板，避免每个方法都使用高饱和独立色相
- 需要大 legend 时使用 legend-only axis，不挤占数据区域
- 消融实验优先使用同一色相的透明度/亮度梯度
- 分组柱状图或密集柱状图必须考虑 hatch，以保证灰度打印可辨

## Step 6：执行代码并导出

- 主格式：SVG（`svg.fonttype='none'`，文字可编辑）
- 源数据（CSV/TSV）随图交付

## Step 7：QA Contract

详见 `references/qa-contract.md`。逐项检查 → 若失败则修订代码并重跑 → 最多 2 轮。

自动 QA 至少运行：

```powershell
python skills/academic-figure/scripts/qa_figure.py --input <svg_path> --venue <venue>
```

人工 QA 重点：
- core conclusion 是否可见
- panel 是否冗余
- 误差棒、样本量、统计检验是否解释
- 颜色和 hatch 是否灰度/色盲友好
- y 轴是否有误导性截断

## Step 8：交付

1. 绘图脚本（`.py`）
2. 源数据文件（CSV/TSV）
3. SVG（矢量主文件）
4. QA 报告
