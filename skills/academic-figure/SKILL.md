---
name: academic-figure
description: "Create, revise, or audit academic figures for CS/AI/ML papers using Python-generated editable SVG as the default output. Supports publication-ready data plots, model architecture SVGs, method flow diagrams, mechanism diagrams, overview figures, figure blueprints, figure audits, and figure revisions. Use when: generating model framework SVGs, overview figures, module detail diagrams, data plots from experiment results, auditing existing figures, suggesting figure types for paper sections, revising figure colors/layouts/labels. Only use arch-prompt when the user explicitly asks for external image prompts. Triggers on: 绘图, figure, chart, 画图, 实验图, 训练曲线, 消融实验, 对比图, 混淆矩阵, 架构图, 模型框架图, overview figure, model architecture, plot, publication figure, 数据可视化, generate plot, architecture diagram, figure blueprint, 建议图表类型, figure audit, 审查图表, figure revision, 修改图表."
---

# Academic Figure

CS/AI/ML academic-figure router. 默认交付可编辑 SVG：数据图使用 Python/matplotlib；架构图、流程图和机制图使用 Python 矢量元素绘制。提示词不是默认交付物。

## Router Protocol

1. Read `manifest.yaml`. It declares `always_load` files, `axes`, and `references.on_demand`.
2. Read every file listed under `always_load`. These are the skill's binding rules — not reference material.
3. Apply the loaded material as constraints:
   - `stance.md` defines Python-only plotting, figure contract, visual policy, and scope.
   - `red-lines.md` defines absolute prohibitions. Do not negotiate these.
   - `output-contract.md` defines deliverables per mode.
   - `anti-patterns.md` defines known failure modes and their correct alternatives.
4. Select exactly one `mode` from the manifest. If ambiguous, ask one concise clarification only when data source, architecture evidence, or target use is missing.
5. Echo the selected mode to the user before executing.
6. Reach for `references/` only when the manifest's `references.on_demand` condition is satisfied.

## Modes

| Mode | Use when |
|---|---|
| `chart-from-data` | Data files or numeric results, needs publication plot |
| `architecture-svg` | 模型结构、方法流程、机制图、overview figure，需要直接生成可编辑 SVG |
| `arch-prompt` | 仅当用户明确要求外部生图提示词时使用；不是默认路径 |
| `figure-blueprint` | Wants figure suggestions for a paper section |
| `figure-audit` | Existing figure reviewed for publication readiness |
| `figure-revision` | Existing figure needs revision |

## Agent Dispatch

`agents/figure_agent.md` is dispatched by the orchestrator at Step 6.4. The agent returns figure artifacts, scripts, SVG paths, and reports; it must not independently edit project source code or experimental data.

## Completion Criteria

- `chart-from-data`: Figure Contract, Python script, source data, editable SVG, QA report — all pass.
- `architecture-svg`: Architecture Contract, Python 绘图脚本, 可编辑 SVG, caption draft, 事实核对清单.
- `arch-prompt`: 仅交付外部工具兼容提示词，并明确标注“非默认路径”.
- `figure-audit`: Every QA item has pass/fail status and concrete remediation.
- `figure-blueprint`: Every suggested figure maps to a paper claim and data/evidence source.
- `figure-revision`: Revised artifact or instructions, QA report, unchanged evidence traceability.
