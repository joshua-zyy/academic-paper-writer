---
name: academic-paper-writer
description: "基于作者现有材料和想法，一次启动持续产出 CS/AI/ML 论文内容初稿；材料不足时形成实质正文、章节框架与补充建议。也支持独立章节起草与局部改写。主 agent 唯一写作，subagent 并行探查与验收。用于写论文、初稿、paper draft、逐节写作、论文框架、章节起草或修改。"
---

# Academic Paper Writer

目标是可用内容稿，不是投稿包或录用保证。主 agent 负责所有正文与修订；subagent 只取证、验收或生成分配的数据图。

## 路由

1. 读取 `manifest.yaml` 及 `always_load`，遵循共享证据、禁止编造和输出边界。
2. 判定 full-paper-planning、section-drafting、section-revision 或专项转交；已确认信息与已加载规则在后续复用。
3. 简短告知范围。局部任务不启动整篇 intake，不强制 venue、全文证据包或完整文献库。
4. 全文任务读 `references/orchestration-workflow.md`；准备、写作、验收分别按需读对应步骤文件。只加载当前工作需要的章节指南。

## 全文路径

集中确认必要信息 → 首轮并行探查 → 主 agent 汇总主张与主线、作者确认 → 分节写作与验收 → 全文整合与验收 → 内容稿交付。

- 自动推进默认开启，保留逐节确认选择，可随时切换；不是每节都问“继续吗”。
- 启动建议用 MinerU 将本地 PDF 转 Markdown 建库，区分参考库与风格库；不将转换和索引缺失设为全局阻塞。
- venue 未定允许通用初稿。已知 venue 时按需调研，官方内容要求优先于风格观察。
- 探查证据跨节复用，只因具体缺口或来源变更追加任务。独立任务能并行则并行，能力不足可串行并如实说明。
- 材料够则写实质正文；不够则搭好框架、明确建议补什么，不硬凑、不断言未观察结果。
- academic-polishing 内化执行；academic-reviser 仅验收，不返回改写稿。
- min_citations 仅建议；正文引用身份与支持关系必须准确记录。

## 交付与恢复

输出规则见 `static/core/output-contract.md`；正文默认 `paper_draft.md`，来源记录 `evidence_inventory.yaml`，必要任务状态 `task_state.yaml`。恢复先读实际产物、已确认主线及待办，只重做受影响工作。

交付区分 usable_draft、partial_draft、structured_outline，不把交付完成称为全部验收通过。架构图由作者提供；LaTeX 排版仅在明确请求时使用独立技能，不进入默认完成条件。
