# 文献检索、筛选与核验指南

## 目录

- 使用定位
- 检索广度要求
- 查询设计
- 来源优先级
- 核验规则
- 与正文的映射
- 利用本地 PDF 或现有草稿
- 禁止行为
- 何时可以降低检索强度

## 使用定位

本文件用于把“引用”从装饰项改成证据项。

默认策略是：

- 只要正文需要真实引用，就主动检索和核验。
- 不把在线检索降级为“可选候选文献”。
- 不把“用户没给文献”当作 Related Work 可以随便写的理由。
- 不接受“文末有参考文献列表，但正文没有 inline citation”这种伪完成状态。

---

## 1. 检索广度要求

除非课题极其小众，否则完整 empirical paper 的检索至少覆盖：

1. 问题背景或应用背景
2. 直接相关方法
3. 强基线或经典方法
4. 最近 2-4 年的代表性工作

经验性下限：

- 完整论文：优先达到 8-15 篇 `VERIFIED` 文献
- 短论文或 early draft：优先达到 4-8 篇 `VERIFIED` 文献

不要在找到三四篇相似论文后就停止。检索结束的标准应是“覆盖充分”，而不是“搜索引擎第一页看完了”。

对 `Introduction` 与 `Related Work`，除正文引用外，还应额外建立 `Exemplar Set`：

- `Introduction`：默认优先观察 3-5 篇同任务、同模态或相近方法论文的引言
- `Related Work`：默认优先观察 4-8 篇同领域论文的相关工作组织方式
- `Exemplar Set` 用于提炼章节组织、比较框架和引用密度，不等于都必须写进正文
- 即使某篇 exemplar 最终不进入正文引用，也可以用于学习该领域如何展开叙述

---

## 2. 查询设计

至少从下列四类查询中取材：

### 问题导向查询

示例模式：

- `<task> review`
- `<task> benchmark`
- `<domain> <task> survey`

目标：

- 找到问题背景、主流数据集、评价指标、经典方法谱系

### 方法导向查询

示例模式：

- `<method family> for <task>`
- `<architecture> <task>`
- `<task> graph transformer`

目标：

- 找到与你的方法最接近的直接比较对象
- 找到可作为 `Exemplar Set` 的直接邻近论文

### 基线导向查询

示例模式：

- `<task> baseline`
- `<dataset> classification method`
- `<classical model> <task>`

目标：

- 避免只引用和自己最像的深度模型，而忽略强传统基线

### 时间导向查询

示例模式：

- `<task> 2024`
- `<task> 2025`
- `<method family> recent`

目标：

- 补充近年的代表性工作，避免 Related Work 停留在旧文献

### 章节组织导向查询

示例模式：

- `<task> introduction`
- `<task> related work`
- `<task> graph transformer Alzheimer's disease fMRI`
- `<dataset or modality> classification review`

目标：

- 找到同领域论文如何组织引言与相关工作
- 观察常见的段落功能单元、比较框架和 work clusters

---

## 3. 来源优先级

推荐优先级如下：

1. 官方或权威索引源
   - 会议/期刊官方 proceedings
   - OpenReview
   - PMLR
   - ACL Anthology
   - IEEE Xplore
   - ACM Digital Library
   - PubMed
   - arXiv 官方页面
   - DBLP
2. 学术搜索与聚合平台
   - Google Scholar
   - Semantic Scholar
3. 二手页面
   - 博客
   - 实验室主页
   - 经验整理帖

规则：

- 一级来源优先用于确定元数据。
- 二级来源可辅助发现论文，但不能替代元数据核验。
- 三级来源最多帮助发现线索，不能作为正式引用依据。

---

## 4. 核验规则

### `VERIFIED`

只有在以下信息能从可信来源确认时，才可标为 `VERIFIED`：

- 标题准确
- 作者列表准确
- venue 准确
- 年份准确
- 来源链接可定位到原始论文页面或权威索引页面

### `UNVERIFIED`

出现以下任一情况时，应标为 `UNVERIFIED`：

- 只能从搜索结果或摘要卡片看到标题，未打开原始来源
- 作者、venue、年份存在不一致
- 只有博客、二手网页或截图
- 仅凭模型记忆生成条目

`UNVERIFIED` 条目不得直接写成正文中的确定性引用。

---

## 5. 与正文的映射

对每条正文使用的文献，至少记录：

- `title`
- `authors`
- `venue`
- `year`
- `source link`
- `status`
- `why it matters`
- `used in`
- `inline citation marker`

推荐输出格式：

```md
## Verified References

1. Title: ...
   Authors: ...
   Venue: ...
   Year: ...
   Source Link: ...
   Status: VERIFIED
   Why It Matters: ...
   Used In: Introduction / Related Work / Baseline comparison / Discussion
   Inline Citation Marker: [1]
```

若只是候选而非正文已用文献，可放在 `Candidate References` 中，但不要混写。

若用于章节组织学习而非直接正文引用，可额外维护：

```md
## Exemplar Set

1. Title: ...
   Why exemplar: ...
   Observed structure: ...
   Reusable moves: ...
   Not reusable: ...
```

`Exemplar Set` 的用途是帮助写出更像该领域论文的 `Introduction` 或 `Related Work`，不是提供可复制原文。

正文映射规则：

- 若一条文献已进入 `Verified References` 且被正文使用，则正文中必须出现对应的 inline citation marker。
- 若正文中存在需要文献支撑的背景事实、方法比较或数据来源说明，却没有可用文献，则在该处直接保留 `[REF_NEEDED: ...]`。
- 不要先生成 bibliography 再假设读者会自己猜哪些句子对应哪些参考文献。
- 若目标 venue 未知，优先使用简单一致的 numeric style，例如 `[1]`, `[2]`。

---

## 6. 利用本地 PDF 或现有草稿

若仓库中已有 PDF、BibTeX、旧草稿或参考文献列表：

- 将它们作为 seed sources
- 读取题目、作者、年份和方法关键词
- 再回到一级来源核验，而不是直接照抄旧草稿

旧草稿里的引文不是天然可信，只能视为检索线索。

---

## 7. 禁止行为

以下行为应明确禁止：

- 编造并不存在的论文
- 猜测作者列表、年份或 venue
- 只因为“这句话看起来需要引用”就随意补一篇文献
- 只引用与你最相似的方法，故意忽略强基线或不利比较
- 把未核验候选文献伪装成已确认引用
- 在正文没有任何 inline citation 的情况下输出完整参考文献列表

---

## 8. 何时可以降低检索强度

只有在以下场景中才可降低检索强度：

- 用户明确只要大纲，不要正文
- 用户明确表示后续自己补引文
- 当前任务是修一句话或局部改写，而不是完整论文写作

即便如此，也不能编造引用；缺失处应保留 `[REF_NEEDED: ...]`。
