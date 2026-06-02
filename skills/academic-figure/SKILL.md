---
name: academic-figure
description: "Create, revise, or audit academic figures for CS/AI/ML papers using Python-only data plotting and structured architecture-figure prompts. Supports publication-ready plots, model framework images, tool-agnostic architecture prompts, figure blueprints, figure audits, and figure revisions. Use when: generating model framework images, overview figures, module detail figures, data plots from experiment results, auditing existing figures, suggesting figure types for paper sections, revising figure colors/layouts/labels. Triggers on: 绘图, figure, chart, 画图, 实验图, 训练曲线, 消融实验, 对比图, 混淆矩阵, 架构图, 模型框架图, overview figure, model architecture, plot, publication figure, 数据可视化, generate plot, architecture diagram, figure blueprint, 建议图表类型, figure audit, 审查图表, figure revision, 修改图表."
---

# Academic Figure

CS/AI/ML academic-figure router. Python-only for data plots: use Python scripts and matplotlib/seaborn-style outputs.

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
| `architecture-image` | Model structure, wants framework/overview/module image |
| `arch-prompt` | Wants tool-agnostic architecture image prompt |
| `figure-blueprint` | Wants figure suggestions for a paper section |
| `figure-audit` | Existing figure reviewed for publication readiness |
| `figure-revision` | Existing figure needs revision |

## Agent Dispatch

`agents/figure_agent.md` is dispatched by the orchestrator at Step 6.4. The agent returns figure artifacts, scripts, prompts, and reports; it must not independently edit project source code or experimental data.

## Completion Criteria

- `chart-from-data`: Figure Contract, Python script, source data, editable SVG, QA report — all pass.
- `architecture-image`: Architecture Contract, prompt spec, generated image, caption draft, verification checklist.
- `arch-prompt`: Tool-agnostic prompt covers components, data flow, labels, visual hierarchy, unconfirmed items.
- `figure-audit`: Every QA item has pass/fail status and concrete remediation.
- `figure-blueprint`: Every suggested figure maps to a paper claim and data/evidence source.
- `figure-revision`: Revised artifact or instructions, QA report, unchanged evidence traceability.
