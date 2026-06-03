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

先判断图在 CS/AI/ML 论文中的实验论证角色，而不是直接套 chart type。

| Evidence role | 使用场景 | 布局倾向 |
|-----------|----------|----------|
| `benchmark matrix` | 多数据集、多指标、多方法比较 | 对齐轴线、共享 legend、紧凑网格 |
| `claim-primary result + supports` | 一个主结果 + 若干稳健性/消融/效率支持 | 主结论 panel 更大，support panels 更安静 |
| `ablation ladder` | 逐步移除/替换模块验证贡献 | 同色系透明度或亮度递进 |
| `training dynamics` | loss/accuracy 曲线、收敛速度、scaling、稳定性 | line + CI/std band，直接标注关键训练事件 |
| `efficiency-performance tradeoff` | 性能与 latency/FLOPs/params/memory/energy 权衡 | Pareto scatter / connected frontier |
| `robustness slice` | 跨域、噪声、缺失模态、OOD、公平性分组 | point-range / box / violin，标注样本量 |
| `error diagnosis` | 混淆矩阵、failure taxonomy、case-level analysis | 突出高风险错误，说明归一化方式 |
| `representation analysis` | t-SNE/UMAP/PCA、attention map、feature clustering | 标注降维方法、随机种子和采样策略 |

## Step 1c：CS/AI/ML chart design gate

每个 `chart-from-data` 任务都必须先读取 `references/cs-ai-chart-design-patterns.md`，并把下列设计决策写入 Figure Contract：

- 图的实验论证角色：benchmark, ablation, training dynamics, efficiency tradeoff, robustness, error diagnosis, representation analysis, 或 method-result composite。
- 是否需要 claim-primary panel，或是否应保持 benchmark matrix / quantitative grid。
- 是否使用 shared legend、legend-only axis，或直接标注 direct labels。
- 是否需要按证据重要性分配 panel 面积，而不是把所有 panel 强行等宽等高。
- 是否需要 hatch / texture / luminance contrast 来保证灰度打印。
- 是否统一方法、模型规模、数据集或任务的视觉编码，避免同一对象在不同 panel 中换色。
- 是否需要把实验设置、统计信息、`n`、重复次数、误差棒定义和 source-data traceability 放入图注/QA。

只有单张非常简单的实验图可以把该 gate 标记为 `minimal_applicable`，但仍需说明 palette、legend、axis 和 export 的选择。

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
- 应用 Step 1c 的 CS/AI/ML chart design gate，不允许绕过实验角色、布局、legend、direct labels、palette、hatch 的选择记录
- 按合约布局生成各面板
- 代码中嵌入数据读取（CSV/TSV/Numpy）
- 使用色板 `PALETTE`（参考 `references/design-theory.md`）
- 多方法同族比较优先使用低饱和 CS/AI/ML family 色板，避免每个方法都使用高饱和独立色相
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
