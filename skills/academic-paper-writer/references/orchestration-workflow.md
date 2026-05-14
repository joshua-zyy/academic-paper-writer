# Orchestration Workflow — 导航索引

本文件是编排器工作流的导航索引。详细步骤已拆分为 3 个文件，按需加载以节省上下文窗口。

## 执行约束（硬性规则）

- **主 Agent 只撰写论文文本，绝对不得修改项目源代码、配置文件或数据文件**。探查时只读，图表代码生成时创建新文件而非覆盖现有文件。
- 子 Agent 的约束见各自 `agents/xxx_agent.md` 中的 Red Lines。
- 论文正文（Introduction / Related Work / Method / Experiments / Discussion / Conclusion / Abstract）由主 Agent **直接撰写**，不 dispatch 独立写作子代理，以确保叙事风格一致。

---

## 步骤索引

| 阶段 | Steps | 文件 | 核心任务 |
|------|-------|------|---------|
| 准备 | 0–4（含 1b） | `workflow-step-0-4.md` | 判定模式、确认 venue+本地文献库、PDF→MD 转换准备、**并行**证据审计、文献检索、实验复核 |
| 起草 | 5–8 | `workflow-step-5-8.md` | Section Plan、Draft v1、占位符审计与图表、证据合规审查 |
| 审查与整合 | 9–12 | `workflow-step-9-12.md` | Prose Gate、Expansion、Verification、Section Loop |

---

## 加载规则

- 执行 Step N 时，只加载 N 所在的文件，不预加载其他文件
- 跨文件引用的输入/输出通过 Evidence Map、Verified References、debt status 等结构化数据在上下文中传递
- 每个文件都包含独立的 dispatch 模板，无需回溯其他文件

---

## 步骤概要

| Step | 动作 | 委托方式 | 触发方式 |
|------|------|---------|---------|
| 0 | 判定 mode、scope、当前 section | — | 自动 |
| 1 | 确认 venue / 语言 + 本地文献库（Blocking Gate） | — | 自动 |
| 1b | 可选: PDF→MD 转换准备（生成脚本，提示用户运行，不阻塞） | — | 自动（条件执行） |
| 2 | 证据审计（并行 dispatch probe agents） | — | 自动，涉及多 probe 时**必须并行** |
| 3 | 文献检索与核验（3a 本地优先 + 3b 联网 + 3c 聚合） | `academic-citation` + `literature-reader-agent`（并行 dispatch） | 自动 |
| 4 | 实验事实复核 | `academic-experiments`（dispatch 子 Agent） | 自动 |
| 5 | 生成 Section / Method Blueprint | — | 自动 |
| 6 | 起草 Draft v1（含占位符系统 + **待补项清单**） | — | 自动 |
| 7 | 占位符审计 + 图表生成 | `academic-figure`（dispatch 子 Agent，arch-prompt） | 自动 |
| 8 | 证据合规审查（Phase 1） | `academic-reviser`（dispatch 子 Agent） | 自动 |
| 9 | Prose Quality Gate（Phase 2） | `academic-polishing`（**内化调用**，主 Agent 自行执行） | 自动 |
| 10 | Expansion Pass（内容密度检查） | — | 自动 |
| 11 | Self-Review & Verification | `academic-reviser`（dispatch 子 Agent） | 自动 |
| 12 | 整合 & 依赖感知 section loop | — | 自动 |
| 12e | **引用清单生成**（强制） | — | 自动 |

---

## Shared Inputs and References

Cross-skill data contracts, shared concept references, and reference-loading guidance are maintained in `skills/academic-paper-writer/SKILL.md` as the high-level orchestrator index.

When executing a concrete step in this file:
- read the referenced schema under the relevant sub-skill's `references/schemas/` if the step consumes or produces structured cross-skill data
- read the referenced file under `references/` when that step explicitly calls for it
