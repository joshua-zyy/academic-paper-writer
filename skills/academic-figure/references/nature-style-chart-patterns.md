# Nature-Style Chart Patterns for CS/AI/ML

借鉴 `nature-figure` 的出版级实验数据图经验，但面向 CS/AI/ML 论文改写。用于 `chart-from-data` 模式中选择布局和视觉编码。

## Pattern 1: Hero Metric + Supporting Panels

适用于主结果很明确，同时需要消融、稳健性或效率作为支撑的图。

- 主 panel 占更大面积，展示核心 claim。
- 支撑 panel 使用较安静的颜色和更小尺寸。
- 共享 legend，避免每个 panel 重复图例。

## Pattern 2: Quantitative Grid

适用于多个数据集、多个指标、多个 baseline 的性能比较。

- 统一方法颜色。
- 轴范围一致，除非明确标注差异。
- 若方法名很多，使用 legend-only panel。

## Pattern 3: Ablation Ladder

适用于模块贡献验证。

- 使用同一 hue 的透明度或亮度梯度。
- 完整模型最醒目，逐步 ablate 的模型逐渐变浅。
- 不用红/绿表达普通类别，红/绿只用于下降/上升提示。

## Pattern 4: Trend With Uncertainty

适用于训练曲线、scaling law、时间序列。

- 使用 line + std/CI band。
- band 必须在图注解释为 std、SEM 或 95% CI。
- 关键事件可以用箭头或直接标注，不要用长 legend。

## Pattern 5: Print-Safe Dense Bars

适用于密集分组柱状图。

- 使用 hatch 编码增强灰度可读性。
- 大量类别时隐藏 x tick label，将方法名放在 legend panel。
- 避免 3D bar、阴影 bar、渐变 bar。

## Pattern 6: Direct Labels Over Legends

适用于线条较少、类别空间固定的图。

- 在线条末端或点附近直接标注方法名。
- legend 只保留给密集或重复类别。
- 直接标注必须避免遮挡数据。

## Pattern 7: Source Data Traceability

每张实验图必须能追溯到源数据。

- 交付 CSV/TSV 或说明原始实验产物路径。
- 图注说明 `n`、误差棒含义、统计检验。
- 若坐标轴截断，图中必须标记 break。
