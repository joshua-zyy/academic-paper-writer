# CS/AI 论文结构建议

## 目录

- 使用原则
- empirical CS/AI 论文默认结构
- 理论论文默认结构
- Survey / Position / Reproduction 论文提示
- 各节写作建议

## 使用原则

本文件提供的是默认建议，不是跨所有论文类型都成立的硬规则。

- 目标期刊/会议的官方结构要求优先于本文件中的通用模板。
- 先判断论文类型，再套结构。
- 在写完整正文前，先形成 `Outline / Evidence Map`。
- 每个核心小节都要标出证据来源；没有证据的地方保留占位符。
- 对 empirical method paper，可优先使用标准实验论文结构。
- 对理论论文、survey、position paper、复现实验报告，应按论文类型调整结构。
- 如果研究概要缺失实验结果、图表或方法细节，应保留占位符，不得为了套模板而编造内容。
- 需要补图或补表时，在正文对应位置插入显式占位符，而不是仅在附录清单里提醒。
- `paper draft` 默认应是“可阅读的完整 prose 草稿”，而不是提纲式骨架。若证据不足，应通过占位符维持结构完整性，而不是把章节压缩成极短说明。

---

## 1. empirical CS/AI 论文默认结构

仅在目标 venue 未提供、未确认，或官方结构无法获取时使用本节默认结构。

典型结构如下：

```text
1. Abstract
2. Introduction
3. Related Work
4. Method / Approach
5. Experiments
   5.1 Experimental Setup
   5.2 Main Results
   5.3 Ablation / Analysis
6. Discussion / Limitations (optional but recommended)
7. Conclusion
[References]
[Appendix / Supplementary]
```

适用场景：

- 提出新模型、新模块、新训练策略
- 有实验结果与 baseline 对比
- 需要展示方法、实验、分析之间的完整闭环

证据映射要求：

- `Introduction` 要有背景和问题定义证据。
- `Related Work` 要有方法谱系和直接比较对象。
- `Method` 要与本地代码、伪代码或用户提供机制一致。
- `Experiments` 要标明每张表、每个数值来自 `newly_run`、`preexisting_artifact` 还是外部文献。
- `Discussion / Limitations` 不要省略评估协议、数据划分或泛化边界的风险。
- 若 `Method` 是论文的核心卖点，默认按“整体框架 -> 模块拆解 -> 训练/推理细节”的顺序写，而不是只写概述段。

可选变化：

- 短论文可将 `Related Work` 并入 `Introduction`
- 简短论文可将 `Method` 与 `Experiments` 合并
- 若没有 ablation，可改为 `Analysis` 或完全省略
- 若论文更偏系统实现，可加入 `System Design` 或 `Implementation Details`

---

## 2. 理论论文默认结构

可参考如下结构：

```text
1. Abstract
2. Introduction
3. Background / Preliminaries
4. Problem Formulation
5. Main Theory / Method
6. Theoretical Analysis / Proof Sketch
7. Experiments or Case Study (optional)
8. Conclusion
[References]
[Appendix]
```

说明：

- 不应强行要求架构图、SOTA 对比或消融实验。
- 若存在实验，其角色通常是辅助说明，而不是论文唯一支撑。
- 若没有实验，重点应转移到定义、假设、理论边界和证明结构。

---

## 3. Survey / Position / Reproduction 论文提示

- `Survey`: 重点在分类框架、文献脉络、方法比较，不强制要求方法节和实验节。
- `Position Paper`: 重点在问题定义、论证路径、立场边界，不强制要求量化结果。
- `Reproducibility Paper`: 重点在复现设置、偏差来源、失败案例、与原论文差异，不要伪装成原创方法论文。

当研究概要明显属于这些类型时，应优先贴合其论证目标，而不是机械套用 empirical paper 模板。

---

## 4. 各节写作建议

### Abstract

默认建议：

- 交代背景问题、现有不足、本文方法或核心主张、主要发现、意义。
- empirical 论文通常应包含量化结果，但只在结果可验证时才写成定论。

缺失结果时的降级规则：

- 若用户未提供真实结果且本地无法复核，可输出摘要草稿。
- 摘要草稿中允许使用 `[RESULT_NEEDED: ...]` 或 `[RESULT_UNVERIFIED: ...]`。
- 不得生成未经核验的数值、提升幅度或排名表述。
- 即便是摘要草稿，也应包含背景、方法、当前可支持的结果边界和意义，不要只剩一句“提出了某方法”。

### Introduction

默认建议：

- 说明研究问题的重要性与背景。
- 说明现有方法的局限。
- 引出本文的核心想法。
- 列出贡献点。
- 在正式起草前，优先调研同领域 exemplar papers 的引言组织方式，再形成当前论文自己的 `Introduction Blueprint`。

额外要求：

- 背景事实需要引用支撑。
- 局限性陈述不能只批评对手，不反思自身假设。
- `Introduction` 若作为初稿输出，最低应覆盖四个功能单元：
  - 问题背景与重要性
  - 现有方法缺口
  - 本文核心想法 / 论文定位
  - 贡献点
- 不要把引言写成“背景 + 一句我们提出方法 + 贡献列表”的瘦结构。
- 默认优先观察 3-5 篇同任务、同模态或相近方法论文的引言，提炼：
  - opening 如何建立问题重要性
  - 中段如何组织已有路线与主要缺口
  - 结尾如何过渡到本文与贡献
- 学的是叙述功能与段落职责，不是照抄句式或段落。

### Related Work

默认建议：

- 按主题、方法类别或时间线组织。
- 不只罗列文献，还要说明与本文的关系。
- 在正式起草前，优先调研同领域 exemplar papers 的 `Related Work` 如何分组、比较与收束，再形成 `Related Work Blueprint`。

引用安全规则：

- 没有可靠参考文献时，使用 `[REF_NEEDED: ...]`。
- 不得为了让段落完整而编造论文、作者、年份或 venue。
- `Related Work` 的初稿不应只罗列文献。至少要形成 2 个以上有内部逻辑的 work clusters，并说明它们与本文的关系。
- 默认至少观察多篇同领域论文的 related-work 组织方式，并提炼：
  - 常见 work clusters
  - 各 cluster 的比较维度
  - 代表工作与共同局限
  - 本文应如何落位
- 若当前工作处于交叉方向，优先按“最直接邻近工作 -> 支撑性背景工作”的顺序组织，而不是平均铺陈所有方向。

### Method / Approach

默认建议：

- 先说明整体思路，再进入模块细节。
- 对核心模块说明输入、输出、目标、与已有方法的区别。
- 若是 empirical method paper，优先拆成：
  - `Problem Definition / Notation`
  - `Overall Architecture`
  - `Core Module 1..N`
  - `Training Objective / Optimization`
  - `Inference / Prediction Aggregation`（若适用）

条件性建议：

- 对 empirical method paper，架构图通常是强烈建议，但不是绝对硬性要求。
- 若用户尚未提供模型架构图、流程图或模块图，应在正文中保留 `[FIGURE_NEEDED: ...]`。
- 若缺方法细节，可用 `[METHOD_DETAIL_NEEDED: ...]`。
- 若缺训练目标、损失函数、推理流程，也应显式占位。
- 若本地有代码，应优先与代码保持一致，而不是为了“写起来更像论文”而改写成另一套方法。

对方法节的最小完备要求：

- 在整体框架描述后，给出架构图放置点，若图尚未完成，显式占位。
- 每个核心模块至少写出：
  - 模块作用
  - 输入 / 输出
  - 关键张量或符号
  - 核心操作流程
  - 关键公式、伪公式或严格的算子描述
  - 与代码一致的特殊实现选择
- 若方法由多个阶段串联，明确阶段顺序与信息流，不要只说“通过若干模块提取特征”。
- 若使用 cross-attention、graph attention、pooling、dFC 摘要、损失加权、对抗增强等操作，应说明它们在整体中的位置与作用，而不是只在实验设置里补一句。
- 若存在实现上重要但论文中容易被忽略的设计，例如阈值策略、残差来源、边门控方式、推理聚合规则，应在正文中写明；不要把这些全留到代码层。
- 若方法节作为初稿仍显得单薄，优先补：
  - 变量与记号说明
  - 模块之间的顺序关系
  - 关键超参数的角色
  - 从代码可恢复的运算定义
  - 图表占位与公式解释

推荐的架构图占位写法：

- `[FIGURE_NEEDED: overall model architecture showing input branches, module order, and fusion point | Method section after overall framework paragraph | final diagram not prepared yet]`
- `[FIGURE_NEEDED: module-level detail for <module name> | Method subsection <x.x> | clarify tensor flow and operations]`

### Experiments

默认建议：

- 交代数据集、指标、实现细节。
- 展示主结果。
- 若适用，再加入 ablation、效率分析、错误分析、定性分析。

缺失结果时的降级规则：

- 可以写实验设计与评估计划。
- 可以写已有观察，但必须明确哪些是本地复核事实，哪些只是待确认结论。
- 缺数据集细节时用 `[DATASET_DETAIL_NEEDED: ...]`。
- 缺对比结果时用 `[RESULT_NEEDED: ...]` 或 `[TABLE_NEEDED: ...]`。
- `Experiments` 初稿至少应覆盖：
  - 数据与预处理
  - 划分与评价协议
  - 实现细节
  - 主结果或结果占位
  - 风险与局限性提醒
- 对 `Data` / `Experimental Setup`：
  - 优先只写可由 repo、日志、脚本、配置或已有 artifact 确认的协议事实
  - 若某些细节只是领域常见默认值，但当前项目尚未证实，不要直接写成确定性陈述；改为占位或待核验说明

### Discussion / Limitations

默认建议：

- 讨论模型为何有效，以及为何可能失效。
- 承认评估协议、数据质量、可解释性或泛化边界的限制。
- 对 reviewer 最可能质疑的问题提前做方法学回应。

注意：

- 这一节对 empirical paper 尤其重要。
- 若当前证据只支持内部验证，应明确写明，不要用修辞淡化。
- 若已有结果尚不充分，也不要让 `Discussion` 退化成一句“需要未来工作”；至少要解释当前证据支持什么、不支持什么。
- 对解释性段落，优先采用两层写法：
  - 第一层：模型观察到了什么
  - 第二层：这些观察与哪些已核验文献相符
- 若第二层缺文献支撑，只保留第一层观察结论，不要把推测性的生物学或领域机制解释写成定论。

### Conclusion

默认建议：

- 总结工作与主要发现。
- 重申局限性边界。
- 给出未来工作方向。

注意：

- 若当前仍是早期草稿，可把结论写成“当前证据支持的有限结论”，避免过度承诺。
- 即便是早期结论，也应回扣方法贡献、当前结果边界和下一步最关键补强项。

### Appendix / Supplementary

可包含：

- 更多实验
- 推导与证明
- 实现细节
- 额外图表
- 复现实验命令和超参数

如果目前材料不全，可先标记应补充的附录内容，而不是强行补齐。
