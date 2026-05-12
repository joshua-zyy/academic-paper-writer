# 文献检索策略

## 检索广度要求

除非课题极其小众，否则完整 empirical paper 的检索至少覆盖：

1. 问题背景或应用背景
2. 直接相关方法
3. 强基线或经典方法
4. 最近 2-4 年的代表性工作

经验性下限：
- 完整论文：优先达到 8-15 篇 VERIFIED 文献
- 短论文或 early draft：优先达到 4-8 篇 VERIFIED 文献

不要在找到三四篇相似论文后就停止。检索结束的标准应是"覆盖充分"，而不是"搜索引擎第一页看完了"。

---

## 四类查询设计

### 1. 问题导向查询

示例模式：
- `<task> review`
- `<task> benchmark`
- `<domain> <task> survey`

目标：找到问题背景、主流数据集、评价指标、经典方法谱系。

### 2. 方法导向查询

示例模式：
- `<method family> for <task>`
- `<architecture> <task>`
- `<task> graph transformer`

目标：找到与你的方法最接近的直接比较对象；找到可作为 Exemplar Set 的直接邻近论文。

### 3. 基线导向查询

示例模式：
- `<task> baseline`
- `<dataset> classification method`
- `<classical model> <task>`

目标：避免只引用和自己最像的深度模型，而忽略强传统基线。

### 4. 时间导向查询

示例模式：
- `<task> 2024`
- `<task> 2025`
- `<method family> recent`

目标：补充近年的代表性工作，避免 Related Work 停留在旧文献。

---

## 章节组织导向查询（Introduction / Related Work 专用）

示例模式：
- `<task> introduction`
- `<task> related work`
- `<task> graph transformer Alzheimer's disease fMRI`
- `<dataset or modality> classification review`

目标：找到同领域论文如何组织引言与相关工作；观察常见的段落功能单元、比较框架和 work clusters。

---

## Exemplar Set 构建

### Introduction Exemplar Set

默认优先观察 3-5 篇同任务、同模态或相近方法论文的引言。

提炼目标：
- opening 如何建立问题重要性
- 中段如何组织已有路线与主要缺口
- 结尾如何过渡到本文与贡献
- 学的是叙述功能与段落职责，不是照抄句式或段落

### Related Work Exemplar Set

默认优先观察 4-8 篇同领域论文的相关工作组织方式。

提炼目标：
- 常见 work clusters
- 各 cluster 的比较维度
- 代表工作与共同局限
- 本文应如何落位

即使某篇 exemplar 最终不进入正文引用，也可用于学习该领域如何展开叙述。

---

## 来源优先级

1. **一级来源**（优先用于确定元数据）：官方 proceedings、OpenReview、PMLR、ACL Anthology、IEEE Xplore、ACM Digital Library、PubMed、arXiv 官方页面、DBLP
2. **二级来源**（辅助发现论文）：Google Scholar、Semantic Scholar
3. **三级来源**（仅作线索）：博客、实验室主页、经验整理帖

一级来源优先用于确定元数据。二级来源可辅助发现论文，但不能替代元数据核验。三级来源最多帮助发现线索，不能作为正式引用依据。
