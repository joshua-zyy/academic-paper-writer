---
name: academic-citation
description: "Search, verify, and map citations for CS/AI/ML papers. Produces VERIFIED/UNVERIFIED reference lists with Citation-to-Claim maps and Exemplar Sets."
---

# Academic Citation

将此 skill 视为"文献取证代理"，而不是搜索结果搬运器。

## 触发条件

找引用, 文献检索, citation pass, find references, reference check, 补文献, citation verification, Exemplar Set

## Red Lines（绝对禁止）

1. 禁止编造文献、作者、年份、venue、DOI、arXiv 编号
2. 禁止把 UNVERIFIED 条目当作 VERIFIED 写入正文
3. 禁止在正文没有任何 inline citation 的情况下输出参考文献列表
4. 禁止只引用与自己最相似的方法而故意忽略强基线或不利比较
5. 禁止因为"搜索结果第一页看完了"就停止检索

## 非协商规则

1. 只有经过核验的文献才能进入 `Verified References`；未核验条目必须标 `UNVERIFIED`。
2. 优先使用一级来源（官方 proceedings、期刊官网、OpenReview、PMLR、ACL Anthology、IEEE Xplore、ACM Digital Library、PubMed、arXiv、DBLP）核验元数据。
3. 检索结束的标准是覆盖充分，而非看了几页搜索结果。完整论文至少达到 8-15 篇 VERIFIED 文献，短论文至少 4-8 篇。
4. 对 Introduction 或 Related Work，除正文引用外，还必须建立同领域 `Exemplar Set`（3-5 篇 Introduction exemplars + 4-8 篇 Related Work exemplars），用于学习章节组织与论证顺序，而非复制原文措辞。
5. 每条用于正文的引用必须有对应的 inline citation marker 和 Citation-to-Claim 映射记录。
6. 参考文献列表只能包含正文中已被引用或以 `[REF_NEEDED: ...]` 声明的条目。

## 任务模式

1. **full-citation-pass** — 为完整论文或核心章节执行全覆盖检索与核验
2. **targeted-citation-search** — 为特定 claim、section 或主题检索文献
3. **exemplar-set-only** — 只构建 Exemplar Set 用于学习章节组织，不强制全部进入正文引用
4. **citation-verification** — 核验已有候选文献列表的元数据准确性

## 工作流

### Step 1: 确认检索目标与范围

- 明确当前是为哪个 section 做引用（Introduction / Related Work / Method / Experiments / Discussion）
- 提取关键检索词：任务名、方法家族、数据集、模态
- 若为 Introduction 或 Related Work，额外确认是否需要 Exemplar Set

### Step 2: 执行多轮检索

至少覆盖四类查询（详见 `references/search-strategy.md`）：

1. **问题导向查询** — `<task> review`、`<task> survey`
2. **方法导向查询** — `<method family> for <task>`
3. **基线导向查询** — `<task> baseline`、`<classical model> <task>`
4. **时间导向查询** — `<task> 2024`、`<task> 2025`

对 Introduction / Related Work，增加章节组织导向查询，用于构建 Exemplar Set。

### Step 3: 核验每篇候选文献

详见 `references/verification-protocol.md`。

逐篇确认：标题准确、作者列表准确、venue 准确、年份准确、来源链接可定位到原始论文页面。

全部确认 → `VERIFIED`。任一无法确认 → `UNVERIFIED`，不得写入正文确定性引用。

### Step 4: 构建 Exemplar Set（Introduction / Related Work 时）

- Introduction：至少观察 3-5 篇同任务、同模态或相近方法论文的引言
- Related Work：至少观察 4-8 篇同领域论文的相关工作组织方式

提炼内容（不是复制段落）：
- 常见章节功能单元
- 每段承担的论证职责
- 文献分组方式（work clusters）
- 贡献点如何与已有工作拉开距离

### Step 5: 建立 Citation-to-Claim 映射（强制输出）

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

### Step 6: 输出

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

## Agent 资源

本 Skill 目录下的 `agents/` 文件夹包含以下辅助文件：

| 文件 | 用途 |
|------|------|
| `agents/citation_agent.md` | 文献检索策略（4 类查询模板、输出 schema） |

**使用方式**：由 `academic-paper-writer` 核心编排器在 Step 3 委托时，按 `academic-paper-writer/references/orchestration-workflow.md` 中的 dispatch 模板创建工具型子代理执行。**此 agent 只执行检索与核验，绝对不得修改项目中的任何文件，也不得独立撰写论文正文**。

## 何时读取 references/

| Reference 文件 | 打开条件 |
|---------------|---------|
| `references/search-strategy.md` | 设计检索查询时（Step 2） |
| `references/verification-protocol.md` | 核验候选文献时（Step 3） |
| `references/citation-mapping.md` | 建立 Citation-to-Claim 映射时（Step 5） |
| `references/schemas/verified-references.md` | 理解输出数据格式（Step 6） |

## 不适用场景

本 Skill 不适用于：
- 生成 LaTeX/BibTeX 格式化引用书目（仅负责检索核验与映射）
- 非 CS/AI/ML 领域的文献检索（如临床医学、法律）
- 用户已有完整引用列表且明确不需要核验的场景

## 失败处理

- **文献搜不到**：如实报告"未找到足够可靠来源"，不补假引文。
- **无法联网**：明确哪些引用无法核验，相关结论降级为占位或待核验表述。
- **遇本地 PDF 或旧草稿中的引文**：作为 seed source，仍须回到一级来源核验。

## 何时降低检索强度

仅在以下场景降低检索强度：
- 用户明确只要大纲，不要正文引用
- 用户明确表示后续自己补引文
- 当前任务是修一句话或局部改写

即便如此，也不能编造引用；缺失处保留 `[REF_NEEDED: ...]`。

## Anti-Patterns

| 模式 | 问题 | 正确做法 |
|------|------|---------|
| 快速扫描型检索 | 只翻了搜索结果第一页就确认引用 | 至少覆盖 4 类查询，完整论文 8-15 篇合格文献 |
| 单信源核验 | 仅靠 Google Scholar 标题核验 | 优先使用一级来源（官方 proceedings、DOI 解析） |
| 引用孤立 | 参考文献列表有正文未引用的条目 | 列表只能包含正文中已引用或 [REF_NEEDED] 声明的条目 |
| 偏误引用 | 只引与自己最相似的方法，忽略强基线 | 对等引用，不利比较也要反映在文中 |
