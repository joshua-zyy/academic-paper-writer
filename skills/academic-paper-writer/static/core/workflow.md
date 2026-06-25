# 编排器工作流摘要（Orchestrator Workflow Summary）

本文件只概述现有 workflow，不替代详细 references。

## Step 顺序

1. Step 0: 任务接收与 mode 选择。
2. Step 1: 阻塞上下文确认（Blocking context confirmation）。
3. Step 2: 本地 PDF 文献库 MinerU 转换提示与 MD 目录确认（条件执行，阻塞）。
4. Step 3: 项目上下文提取。
5. Step 4: Venue research 与 Venue Brief。
6. Step 5: 证据审计（Evidence audit）。
7. Step 6: Citation retrieval and verification。
8. Step 7: Experiment evidence pass。
9. Step 8: Section Blueprint 与 Section Contract。
10. Step 9: Section Complete Loop。
11. Step 10: Section loop progression。
12. Step 11: Citation list 与 citation count gate。
13. Step 12: Figure handling 与最终 publication-readiness debt 检查。

## 详细参考

- `references/orchestration-workflow.md`: 完整 workflow 与 dispatch 模板。
- `references/workflow-step-0-7.md`: intake、本地文献库 MinerU 转换确认、venue、evidence、citation 与 experiment setup。
- `references/workflow-step-8-9.5.md`: blueprint、drafting、placeholder、figure 与 evidence checks。
- `references/workflow-step-9.6-12.md`: polishing、revision、verification、integration、citation list 与最终 figure handling。
