---
name: academic-citation
description: "Search, verify, and map citations for CS/AI/ML papers. Produces VERIFIED/UNVERIFIED reference lists with Citation-to-Claim maps and Exemplar Sets. Use when: finding references for a paper section, verifying citation accuracy, building exemplar sets for introduction/related work learning, checking if existing citations are real and accurate, supplementing local literature library. Triggers on: 找引用, 文献检索, citation pass, find references, reference check, 补文献, citation verification, Exemplar Set, search papers, verify citation, 核验文献, 查引用, literature search, reference verification."
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
3. 检索结束的标准是覆盖充分，而非看了几页搜索结果。整篇完整论文的总引用数（去重后）应达到至少 35 篇（含本地文献库和外部文献）。单节检索不应少于 4 类查询覆盖。
4. 对 Introduction 或 Related Work，除正文引用外，还必须建立同领域 `Exemplar Set`（3-5 篇 Introduction exemplars + 4-8 篇 Related Work exemplars），用于学习章节组织与论证顺序，而非复制原文措辞。
5. 每条用于正文的引用必须有对应的 inline citation marker 和 Citation-to-Claim 映射记录。
6. 参考文献列表只能包含正文中已被引用或以 `[REF_NEEDED: ...]` 声明的条目。
7. **本地文献库优先**：当提供了 `local_lit_md_dir` 时，必须优先在本地 MD 库中检索和阅读全文，充分搜索后再联网补充。
8. **Subagent 阅读只提炼不决策**：`literature-reader-agent` 的输出（LiteratureReadingReport）仅作为主 agent 的参考输入，最终是否引用由主 agent 基于论文整体论证结构决定。
9. **原文 vs 推断隔离**：`literature-reader-agent` 必须严格区分原文提取和自身推断。主 agent 引用时，只能以 `source: 原文` 的内容作为引用依据。

## 任务模式

1. **full-citation-pass** — 为完整论文或核心章节执行全覆盖检索与核验
2. **targeted-citation-search** — 为特定 claim、section 或主题检索文献
3. **exemplar-set-only** — 只构建 Exemplar Set 用于学习章节组织，不强制全部进入正文引用
4. **citation-verification** — 核验已有候选文献列表的元数据准确性
5. **local-citation-pass** — 优先从本地文献库（`papersToMd/`）检索与核验引用，不足时再联网补充。依赖 `literature-reader-agent` 进行全文阅读。
6. **citation-verification-with-reading** — 对已下载到本地文献库的引用文献，逐篇阅读全文并验证引用合理性（claim_accuracy 检查）。用于论文撰写完毕后的引用确认流程。

## 工作流

详见 `references/workflow-citation-pass.md` 获取完整步骤。概要如下：

| Step | 动作 | 关键规则 |
|------|------|---------|
| 1 | 确认检索目标与范围 | 明确 section、检索词、是否需要 Exemplar Set |
| 1a | 本地文献库优先检索 | 有 `local_lit_md_dir` 时先搜本地，2+ 篇候选**必须并行** dispatch reader agent |
| 2 | 执行多轮检索 | 至少覆盖 4 类查询（问题/方法/基线/时间导向），详见 `references/search-strategy.md` |
| 3 | 核验每篇候选文献 | 详见 `references/verification-protocol.md`，全部确认→VERIFIED，任一失败→UNVERIFIED |
| 3a | 联网文献全文获取与阅读 | 优先开放来源获取全文，多篇**必须并行**执行 |
| 3b | Subagent 阅读结果聚合 | 按 relevance + recommendation 排序，主 agent 评估是否引用 |
| 4 | 构建 Exemplar Set | Introduction 3-5 篇，Related Work 4-8 篇，提炼叙述功能而非复制段落 |
| 5 | Citation-to-Claim 映射 | **强制步骤**，详见 `references/citation-mapping.md` |
| 6 | 输出 | 按 `references/schemas/verified-references.md` 格式输出 Verified References + Exemplar Set + Citation-to-Claim Map |

## Agent 资源

本 Skill 目录下的 `agents/` 文件夹包含以下辅助文件：

| 文件 | 用途 |
|------|------|
| `agents/citation_agent.md` | 文献检索策略（4 类查询模板、输出 schema） |
| `agents/literature-reader-agent.md` | 文献阅读与提炼代理（输入 MD 全文，输出 LiteratureReadingReport） |

**使用方式**：由 `academic-paper-writer` 核心编排器在 Step 3 委托时，按 `academic-paper-writer/references/orchestration-workflow.md` 中的 dispatch 模板创建工具型子代理执行。**此 agent 只执行检索与核验，绝对不得修改项目中的任何文件，也不得独立撰写论文正文**。

`literature-reader-agent` 由 `citation_agent` 或 `academic-paper-writer` 在 Step 3a/3b 中并行 dispatch，用于阅读本地 MD 文献或联网获取的全文。

## 何时读取 references/

| Reference 文件 | 打开条件 |
|---------------|---------|
| `references/search-strategy.md` | 设计检索查询时（Step 2） |
| `references/verification-protocol.md` | 核验候选文献时（Step 3） |
| `references/citation-mapping.md` | 建立 Citation-to-Claim 映射时（Step 5） |
| `references/schemas/verified-references.md` | 理解输出数据格式（Step 6） |
| `references/schemas/literature-reading-report.md` | subagent 阅读输出格式（Step 1a/3a） |
| `agents/literature-reader-agent.md` | 文献阅读代理模板（Step 1a/3a 并行 dispatch） |

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
