# 路径 A: chart-from-data 工作流

## 入口

用户请求 → 判断为实验数据图 → chart-from-data 模式

## Step 1：确认图表用途与核心结论

- 谁在什么数据上做了什么对比？
- 支持论文中的哪个 claim？
- 目标期刊/会议的图表规范（宽度、格式、dpi）

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

## Step 6：执行代码并导出

- 主格式：SVG（`svg.fonttype='none'`，文字可编辑）
- 副格式：PDF（`pdf.fonttype=42`）
- 位图预览：TIFF 300-600dpi
- 源数据（CSV/TSV）随图交付

## Step 7：QA Contract

详见 `references/qa-contract.md`。逐项检查 → 若失败则修订代码并重跑 → 最多 2 轮。

## Step 8：交付

1. 绘图脚本（`.py`）
2. 源数据文件（CSV/TSV）
3. SVG（矢量主文件）
4. PDF / TIFF（副格式）
5. QA 报告
