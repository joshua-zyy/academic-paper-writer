# Citation Pass 工作流

## Step 1: 确认检索目标与范围

- 明确当前是为哪个 section 做引用（Introduction / Related Work / Method / Experiments / Discussion）
- 提取关键检索词：任务名、方法家族、数据集、模态
- 若为 Introduction 或 Related Work，额外确认是否需要 Exemplar Set

## Step 1a: 本地文献库优先检索

当配置了 `local_lit_md_dir` 时，在联网检索之前执行：

1. 读取 `<local_lit_md_dir>/_index.json`，用关键词搜索索引
2. 命中的候选文献，dispatch `literature-reader-agent` 并行阅读 MD 全文
3. 每个阅读任务产出 LiteratureReadingReport，包含核心主张、方法概述、关键结果、可引用 claim 列表、关联度评估、引用建议
4. 主 agent 综合所有报告，决定是否引用及用于何处
5. 若本地搜索结果充分且内容匹配 → 跳过联网检索
6. 若不足或不匹配 → 进入 Step 2 联网检索

**并行 dispatch 规则**：当有 2 篇以上候选文献时，**必须并行** dispatch reader agent（同一次消息中发出多个 Task），不得串行等待。

## Step 2: 执行多轮检索

至少覆盖四类查询（详见 `references/search-strategy.md`）：

1. **问题导向查询** — `<task> review`、`<task> survey`
2. **方法导向查询** — `<method family> for <task>`
3. **基线导向查询** — `<task> baseline`、`<classical model> <task>`
4. **时间导向查询** — `<task> 2024`、`<task> 2025`

对 Introduction / Related Work，增加章节组织导向查询，用于构建 Exemplar Set。

## Step 3: 核验每篇候选文献

详见 `references/verification-protocol.md`。

逐篇确认：标题准确、作者列表准确、venue 准确、年份准确、来源链接可定位到原始论文页面。

全部确认 → `VERIFIED`。任一无法确认 → `UNVERIFIED`，不得写入正文确定性引用。

## Step 3a: 联网文献全文获取与阅读

对 Step 3 中检索到的非本地候选文献：

1. **优先获取全文**：
   - 尝试从 arXiv、OpenReview、PMLR、ACL Anthology 等开放来源获取全文 HTML 或 PDF
   - 获取成功 → 将内容转化为纯文本，dispatch `literature-reader-agent` 阅读全文
   - 获取失败（付费墙等）→ 降级为摘要 + 元数据，标注 `source_of_content: abstract_only`
2. **并行 dispatch**：多篇候选文献的阅读**必须并行**执行
3. 阅读报告参与引用决策：以 report 中的 `citable_claims`（`source: 原文`）为主要引用依据

## Step 3b: Subagent 阅读结果聚合

所有 `literature-reader-agent` 返回后：

1. 按 `relevance_to_current_work` + `recommendation` 排序
2. 主 agent 逐条评估：该文献是否写入 Verified References？关联到哪个 claim？插入哪个 section？
3. 将采纳的文献写入 Citation-to-Claim Map

## Step 4: 构建 Exemplar Set（Introduction / Related Work 时）

- Introduction：至少观察 3-5 篇同任务、同模态或相近方法论文的引言
- Related Work：至少观察 4-8 篇同领域论文的相关工作组织方式

提炼内容（不是复制段落）：
- 常见章节功能单元
- 每段承担的论证职责
- 文献分组方式（work clusters）
- 贡献点如何与已有工作拉开距离

## Step 5: 建立 Citation-to-Claim 映射（强制输出）

详见 `references/citation-mapping.md`。

**此步骤为强制步骤，不可跳过。** 为每条正文使用的文献记录：支撑的段落或主张、inline citation marker、引用目的（背景事实/方法比较/基线来源/数据集来源）。

输出格式要求：

```md
## Citation-to-Claim Map

| 正文主张/句子 | Inline Citation | 文献 | 引用目的 | 所在章节 |
|--------------|----------------|------|---------|---------|
| "AD 占痴呆病例 60%–70%" | [1] | Alzheimer's Association, 2025 | 背景事实 | Introduction |
| "早期方法依赖静态 FC 矩阵" | [2] | Badhwar et al., 2017 | 方法历史 | Introduction |
```

**检查清单**：
- [ ] 每条 Verified Reference 都有对应的 inline citation 位置
- [ ] 每个 inline citation 都对应一条 Verified Reference
- [ ] 无"裸 claim"（需要文献支撑但无 citation 或 [REF_NEEDED]）
- [ ] 无孤立引用（Reference 列表中有但正文未引用）

## Step 6: 输出

按 `references/schemas/verified-references.md` 中定义的数据结构输出。

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
