---
name: "academic-citation"
description: "Use when searching, verifying, or mapping citations for academic papers — literature search, reference verification, citation-to-claim mapping, or exemplar set construction. Triggers on: 找引用, 文献检索, citation pass, find references, reference check, 补文献."
---

# Academic Citation

将此 skill 视为"文献取证代理"，而不是搜索结果搬运器。

## 非协商规则

- 不编造文献、作者、年份、venue、DOI、arXiv 编号。
- 只有经过核验的文献才能进入 `Verified References`；未核验条目必须标 `UNVERIFIED`。
- 优先使用一级来源（官方 proceedings、期刊官网、OpenReview、PMLR、ACL Anthology、IEEE Xplore、ACM Digital Library、PubMed、arXiv、DBLP）核验元数据。
- 不要因为"搜索结果第一页看完了"就停止检索；检索结束的标准是覆盖充分。
- 对 `Introduction` 或 `Related Work`，除正文引用外，还必须建立同领域 `Exemplar Set`，用于学习章节组织与论证顺序，而非复制原文措辞。
- 每条用于正文的引用必须有对应的 inline citation marker 和 Citation-to-Claim 映射记录。
- 不输出"有参考文献列表但正文没有 inline citation"的状态。
- 参考文献列表只能包含正文中已被引用或以 `[REF_NEEDED: ...]` 声明的条目；不生成与正文脱节的 bibliography。

## 任务模式

1. **full-citation-pass** — 为完整论文或核心章节执行全覆盖检索与核验
2. **targeted-citation-search** — 为特定 claim、section 或主题检索文献
3. **exemplar-set-only** — 只构建 Exemplar Set 用于学习章节组织，不强制全部进入正文引用
4. **citation-verification** — 核验已有候选文献列表的元数据准确性

## 工作流

### Step 1: 确认检索目标与范围

- 明确当前是为哪个 section 做引用（Introduction / Related Work / Method / Experiments / Discussion）
- 提取关键检索词：任务名、方法家族、数据集、模态
- 若为 `Introduction` 或 `Related Work`，额外确认是否需要 Exemplar Set

### Step 2: 执行多轮检索

至少覆盖四类查询（详见 `references/search-strategy.md`）：

1. **问题导向查询** — `<task> review`、`<task> survey`
2. **方法导向查询** — `<method family> for <task>`
3. **基线导向查询** — `<task> baseline`、`<classical model> <task>`
4. **时间导向查询** — `<task> 2024`、`<task> 2025`

对 `Introduction` / `Related Work`，增加章节组织导向查询，用于构建 Exemplar Set。

检索量级下限：
- 完整论文：优先达到 8-15 篇 VERIFIED 文献
- 短论文或 early draft：优先达到 4-8 篇 VERIFIED 文献

### Step 3: 核验每篇候选文献

详见 `references/verification-protocol.md`。

逐篇确认：标题准确、作者列表准确、venue 准确、年份准确、来源链接可定位到原始论文页面。

只有以上全部确认的条目才能标为 `VERIFIED`。任一信息无法确认则标为 `UNVERIFIED`，不得写入正文确定性引用。

### Step 4: 构建 Exemplar Set（Introduction / Related Work 时）

- Introduction：优先观察 3-5 篇同任务、同模态或相近方法论文的引言
- Related Work：优先观察 4-8 篇同领域论文的相关工作组织方式

提炼内容（不是复制段落）：
- 常见章节功能单元
- 每段承担的论证职责
- 文献分组方式（work clusters）
- 贡献点如何与已有工作拉开距离

### Step 5: 建立 Citation-to-Claim 映射

详见 `references/citation-mapping.md`。

为每条正文使用的文献记录：
- 支撑的段落或主张
- 在正文中的 inline citation marker
- 引用目的（背景事实 / 方法比较 / 基线来源 / 数据集来源 等）

### Step 6: 输出

输出至少包含：

```md
## Verified References
[N] Title: ...
    Authors: ...
    Venue: ... Year: ...
    Source Link: ...
    Status: VERIFIED
    Why It Matters: ...
    Used In: Introduction / Related Work / Baseline comparison
    Inline Citation Marker: [N]

## Exemplar Set (if applicable)
[N] Title: ...
    Why exemplar: ...
    Observed structure: ...
    Reusable moves: ...

## Citation-to-Claim Map
- Claim/Sentence: "..." → [N]
- Claim/Sentence: "..." → [REF_NEEDED: topic]

## Missing References
- [REF_NEEDED: ...] — 哪些主张仍缺文献支撑
```

## 失败处理

- 文献搜不到：如实报告"未找到足够可靠来源"，不补假引文。
- 无法联网：明确哪些引用无法核验，相关结论降级为占位或待核验表述。
- 遇本地 PDF 或旧草稿中的引文：作为 seed source，仍须回到一级来源核验。

## 何时降低检索强度

仅在以下场景降低检索强度：
- 用户明确只要大纲，不要正文引用
- 用户明确表示后续自己补引文
- 当前任务是修一句话或局部改写

即便如此，也不能编造引用；缺失处保留 `[REF_NEEDED: ...]`。
