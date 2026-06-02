# Orchestrator Anti-Patterns

| 模式 | 问题 | 正确做法 |
|------|------|---------|
| 跳过证据审计 | 不盘点证据直接开写 | 必须 Step 2 完成证据审计后再 Step 6 起草 |
| 批量输出整篇 | 同时多节起草导致证据一致性差 | 分节推进，逐节完成 Draft→Quality→Verification 闭环 |
| Abstract 前置 | 证据未稳时就先写 Abstract | Abstract 必须后置，等主体章节证据稳定后再写 |
| 无证据式 SOTA | 未与强基线比较就声称 SOTA | SOTA 表述必须附 baseline 比较表 |
| 自我审查赦免 | 因接近截止期就缩短审查流程 | Hard Gates 不可跳过，每种核实步骤都至少执行一遍 |
| Draft v1 即完成 | Draft v1 写入文件后直接跳到下一节 | 必须完成 6.4→6.9 全部审查阶段后再推进 |
| 自行规划 Todo | 不按标准化模板创建 TodoWrite | 按规则 20 强制使用 `standard-todo-template.md` |
| 子 Agent 写文件 | literature-reader-agent 在项目目录下创建文件 | 子 Agent 只返回结构化内容，文件写入由主 Agent 负责 |
