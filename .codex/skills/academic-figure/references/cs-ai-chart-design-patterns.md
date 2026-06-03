# CS/AI/ML Chart Design Patterns

用于 `chart-from-data` 模式的领域适配设计 gate。目标不是模仿某个期刊风格，而是让 CS/AI/ML 论文中的实验图可复核、可比较、信息密度合适，并直接服务论文 claim。

## Operating Rules

- 先判断实验论证角色，再选 chart type；图表必须回答一个明确的 reviewer question。
- 优先按 CS/AI/ML 证据类型组织：benchmark、ablation、training dynamics、efficiency tradeoff、robustness、error diagnosis、representation analysis。
- 多 panel 图按证据层级分配面积；核心结论 panel 可以更大，但不能为了视觉冲击压缩关键对照。
- 同一方法、模型规模、数据集或任务在所有 panel 中保持稳定编码。
- 颜色用于语义编码，不用于装饰；方法家族、模型规模、方向性变化和风险提示必须区分。
- 图表必须交代统计含义、样本量或重复次数、source-data traceability、坐标轴截断和实验配置差异。
- 不把非 CS/AI/ML 的期刊页面模式当作默认目标；只吸收可迁移原则，如共享图例、直接标注、灰度可读和多面板层级。

## Pattern 1: Benchmark Matrix

适用于多数据集、多指标、多 baseline 的主结果。

- 数据集和指标的排列顺序应对应论文叙事，而不是按文件顺序。
- 方法颜色固定；同一方法跨 panel 不换色。
- 方法过多时使用 shared legend 或 legend-only panel，不重复图例。
- 若轴范围不同，必须标注原因；相同任务的同类指标优先共享尺度。

## Pattern 2: Claim-Primary Result + Supports

适用于一个主结果需要消融、稳健性或效率作为支撑的图。

- 主 panel 展示论文最核心的实验 claim。
- 支撑 panel 只回答必要问题：为什么有效、在哪些条件下有效、代价是什么。
- 支撑 panel 使用更安静的视觉层级，但不能牺牲可读性。

## Pattern 3: Ablation Ladder

适用于模块贡献、损失项、训练策略或数据处理步骤验证。

- 完整模型最醒目；逐步移除/替换的变体使用同色系亮度或透明度递进。
- 只比较真正可归因的变体，避免把多个改动混在一个 ablation 条目里。
- 图注说明每个变体具体移除了什么，不用模糊缩写。

## Pattern 4: Training Dynamics

适用于 loss/accuracy 曲线、收敛速度、scaling 或稳定性分析。

- 使用 line + std/CI band；band 必须说明为 std、SEM 或 95% CI。
- 标注关键训练事件：warmup、augmentation switch、early stopping、scheduler milestone。
- 不把平滑曲线当作原始曲线；若平滑，说明窗口或方法。

## Pattern 5: Efficiency-Performance Tradeoff

适用于 accuracy/F1/AUC 与 latency、FLOPs、params、memory、energy 的权衡。

- 优先使用 Pareto scatter / connected frontier，而不是只排性能柱状图。
- 主方法若声称“更高效”，必须同时展示性能和成本轴。
- 标注硬件、batch size、precision 和测量协议，否则效率 claim 不成立。

## Pattern 6: Robustness and Generalization Slice

适用于跨域、噪声、缺失模态、长尾类别、OOD 或公平性分组结果。

- 分组顺序按难度或语义组织，不按随机标签顺序。
- 使用 point-range / box / violin 展示稳定性；不要只展示均值。
- 明确每个 slice 的样本量，避免小样本组被误读。

## Pattern 7: Error Diagnosis

适用于混淆矩阵、failure taxonomy、case-level analysis。

- 混淆矩阵使用感知均匀的单色或双向色板，标注归一化方式。
- failure taxonomy 的类别必须来自真实错误样本，不得凭直觉编造。
- 重点突出高风险错误，而不是把所有格子同等强调。

## Pattern 8: Representation and Embedding Map

适用于 t-SNE/UMAP/PCA、attention map、feature clustering。

- 明确降维方法、随机种子、距离度量和采样策略。
- embedding 图只支持结构性观察，不直接证明性能优越。
- 类别很多时优先直接标注关键簇或使用小 multiples，避免不可读大 legend。

## Pattern 9: Method-Result Composite

适用于方法示意和实验数据需要合成一页时。

- 方法示意解释机制，实验 panel 只验证该机制相关 claim。
- 数据 panel 的编码必须和方法示意保持语义一致。
- 若方法示意复杂，走 `architecture-image`，不要用数据图 workflow 强行画复杂框架。

## Pattern 10: Source Data Traceability

每张实验图必须能追溯到源数据。

- 交付 CSV/TSV 或说明原始实验产物路径。
- 图注说明 `n`、重复次数、误差棒含义、统计检验。
- 若坐标轴截断，图中必须标记 break。
