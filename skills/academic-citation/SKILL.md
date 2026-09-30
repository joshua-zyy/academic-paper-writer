---
name: academic-citation
description: "检索、阅读和核验 CS/AI/ML 文献，分别确认文献身份与原文对主张的支持，提供可定位引用映射。本地文献库优先，支持单条核验、局部补引用、解释性分析引用复查及全文引用整理。用于找引用、文献检索、引用确认、全文阅读验证、citation pass、reference check 或 exemplar 学习。"
---

# Academic Citation

1. 读 manifest 与 always_load，按当前请求选 workflow，复用已确认目标和已读证据。
2. 全文或本地建库任务启动时主动建议 MinerU PDF→MD，提供 scripts/convert-pdfs-to-md.py 用法；API 上传敏感材料需确认。局部元数据核验无需全文转换。
3. 有本地材料先检索；有索引用索引，无索引定向搜索文件名/可读内容，不因缺 `_index_ref.json` 全局暂停。所需原文不可读时明确该主张未核验，可建议转换。
4. 身份状态使用 verified-references 契约；正文内容支持使用 citation-to-claim-map 契约。身份确认不能替代原文阅读与支持范围。
5. 子代理只返回证据与建议，主 agent 决定采用并整合正文。读者数量按内容/能力安排，独立工作并行，不固定配额或每节重读全部库。
6. 局部调用只做指定任务；未知 venue、无全篇证据包不阻塞。元数据核验不追加检索，除非解决具体冲突。

| workflow | 用途 |
|---|---|
| full-citation-pass | 全文必要背景、方法、数据、解释支持 |
| targeted-citation-search | 一个主张或章节补引用 |
| citation-verification | 已有条目身份字段核对 |
| citation-verification-with-reading | 核对引用是否支持正文陈述 |
| local-citation-pass | 本地优先定向阅读后补公开来源 |
| exemplar-set-only | 学习章节组织，非复制原文 |

按需读 references/verification-protocol.md 与 workflow-citation-pass.md。min_citations 仅建议，不为达标堆引用。citation_audit.py 只查 numeric 结构，退出0也不是身份或内容支持通过；author-year 明确未检查。
