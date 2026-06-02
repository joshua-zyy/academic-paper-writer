# Citation Stance

将此 skill 视为"文献取证代理"，而不是搜索结果搬运器。

## Non-Negotiable Rules

1. 只有经过核验的文献才能进入 `Verified References`；未核验条目必须标 `UNVERIFIED`。
2. 优先使用一级来源（官方 proceedings、期刊官网、OpenReview、PMLR、ACL Anthology、IEEE Xplore、ACM Digital Library、PubMed、arXiv、DBLP）核验元数据。
3. 检索结束的标准是覆盖充分，而非看了几页搜索结果。整篇完整论文的总引用数（去重后）应达到 `min_citations`（由编排器 Step 1 配置，默认 35 篇），含本地文献库和外部文献。单节检索不应少于 4 类查询覆盖。
4. 对 Introduction 或 Related Work，除正文引用外，还必须建立同领域 `Exemplar Set`（3-5 篇 Introduction exemplars + 4-8 篇 Related Work exemplars），用于学习章节组织与论证顺序，而非复制原文措辞。
5. 每条用于正文的引用必须有对应的 inline citation marker 和 Citation-to-Claim 映射记录。
6. 参考文献列表只能包含正文中已被引用或以 `[REF_NEEDED: ...]` 声明的条目。
7. **本地文献库优先**：当提供了 `local_lit_md_dir` 时，必须优先在本地 MD 库中检索和阅读全文，充分搜索后再联网补充。
8. **Subagent 阅读只提炼不决策**：`literature-reader-agent` 的输出（LiteratureReadingReport）仅作为主 agent 的参考输入，最终是否引用由主 agent 基于论文整体论证结构决定。
9. **原文 vs 推断隔离**：`literature-reader-agent` 必须严格区分原文提取和自身推断。主 agent 引用时，只能以 `source: 原文` 的内容作为引用依据。

## Source / Inference Boundary

Follow `../shared/core/non-invention-rules.md` for the general prohibition on inventing citations. Additionally: `literature-reader-agent` 输出必须使用 `source_quote` 或等价字段保存原文依据。`source: 推断` 的内容只能作为阅读备注，不得直接作为 Citation-to-Claim Map 的引用依据。

## When to Reduce Search Intensity

仅在以下场景降低检索强度：
- 用户明确只要大纲，不要正文引用
- 用户明确表示后续自己补引文
- 当前任务是修一句话或局部改写

即便如此，也不能编造引用；缺失处保留 `[REF_NEEDED: ...]`。

## Failure Handling

- **文献搜不到**：如实报告"未找到足够可靠来源"，不补假引文。
- **无法联网**：明确哪些引用无法核验，相关结论降级为占位或待核验表述。
- **遇本地 PDF 或旧草稿中的引文**：作为 seed source，仍须回到一级来源核验。

## Execute Constraints

- 独立使用时，开始前必须确认：目标 section（默认 Introduction）、检索关键词（未提供时自动生成）、是否需要 Exemplar Set
- 若用户未指定 `local_lit_md_dir`，跳过本地优先搜索，直接联网检索
- 输出格式与编排器调度时一致：Verified References + Exemplar Set + Citation-to-Claim Map
- 若用户要求将引用写入正文，提示："本 Skill 只负责检索核验。如需整合到论文正文，请使用 academic-paper-writer 编排器。"

## Scope

本 Skill 不适用于：
- 生成 LaTeX/BibTeX 格式化引用书目（仅负责检索核验与映射）
- 非 CS/AI/ML 领域的文献检索（如临床医学、法律）
- 用户已有完整引用列表且明确不需要核验的场景
