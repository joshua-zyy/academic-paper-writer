---
name: academic-figure
description: "Create, revise, or audit academic figures for CS/AI/ML papers using Python-only data plotting and structured architecture-figure prompts. Supports publication-ready plots, model framework images, tool-agnostic architecture prompts, figure blueprints, figure audits, and figure revisions. Use when: generating model framework images, overview figures, module detail figures, data plots from experiment results, auditing existing figures, suggesting figure types for paper sections, revising figure colors/layouts/labels. Triggers on: 绘图, figure, chart, 画图, 实验图, 训练曲线, 消融实验, 对比图, 混淆矩阵, 架构图, 模型框架图, overview figure, model architecture, plot, publication figure, 数据可视化, generate plot, architecture diagram, figure blueprint, 建议图表类型, figure audit, 审查图表, figure revision, 修改图表."
---

# Academic Figure

This skill is the CS/AI/ML academic-figure router. It is Python-only for data plots: use Python scripts and matplotlib/seaborn-style outputs for drawing, previewing, exporting, and QA of quantitative figures.

## Routing Protocol

1. Read `manifest.yaml`.
2. Read every file in `always_load`: `static/core/stance.md` and `static/core/output-contract.md`.
3. Select exactly one `mode` from the manifest unless the user explicitly asks for a multi-step package.
4. Read only the selected mode fragment under `static/fragments/mode/`.
5. Reach for `references/` only when the selected fragment says the deeper detail is needed.

## Modes

| Mode | Use when |
|---|---|
| `chart-from-data` | The user provides data files or numeric results and needs a publication plot. |
| `architecture-image` | The user provides model structure and wants a framework/overview/module image. |
| `arch-prompt` | The user wants a tool-agnostic architecture image prompt. |
| `figure-blueprint` | The user wants figure suggestions for a paper section. |
| `figure-audit` | The user wants an existing figure reviewed for publication readiness. |
| `figure-revision` | The user wants an existing figure revised. |

If the request is ambiguous, choose the smallest mode that satisfies the user request and ask one concise clarification only when data source, architecture evidence, or target use is missing.

## Red Lines

1. Do not invent data, experiment results, model modules, architecture connections, losses, datasets, or training flows.
2. Do not use high-saturation rainbow-style palettes or visual effects that imply certainty without statistics.
3. Do not deliver data plots without an editable vector output, preferably SVG.
4. Do not treat image-generated architecture figures as factual final figures without an Architecture Contract and human-verifiable checklist.
5. Do not overwrite source data or project code. Create new scripts or output files only for figure delivery.

## Reference Loading

| Reference | Open when |
|---|---|
| `references/figure-contract.md` | Building Figure Contract or Architecture Contract. |
| `references/workflow-chart-from-data.md` | Executing `chart-from-data`. |
| `references/workflow-architecture-image.md` | Executing `architecture-image`. |
| `references/workflow-arch-prompt.md` | Executing `arch-prompt`. |
| `references/qa-contract.md` | Before final delivery, audit, or revision. |
| `references/api.md` | Writing Python plotting code. |
| `references/chart-types.md` | Choosing chart type. |
| `references/design-theory.md` | Color, layout, typography, and export rationale. |
| `references/nature-style-chart-patterns.md` | Dense, high-impact multi-panel plot patterns. |
| `references/architecture-prompting.md` | Architecture prompt wording. |
| `references/tutorials.md` | End-to-end examples are needed. |

## Agent Resource

`agents/figure_agent.md` contains the delegated figure-agent contract. In orchestrated use, the agent returns figure artifacts, scripts, prompts, and reports; it must not independently edit project source code or experimental data.

## Completion Criteria

- `chart-from-data`: QA passes, Figure Contract, Python script, source data, editable SVG, and QA report are delivered.
- `architecture-image`: Architecture Contract, prompt spec, generated image path or prompt fallback, caption draft, and verification checklist are delivered.
- `arch-prompt`: Tool-agnostic prompt covers components, data flow, labels, visual hierarchy, and unconfirmed items.
- `figure-audit`: Every QA item has pass/fail status and concrete remediation.
- `figure-blueprint`: Every suggested figure maps to a paper claim and data/evidence source.
- `figure-revision`: Revised artifact or revised instructions, QA report, and unchanged evidence traceability.

## Anti-Patterns

| Pattern | Problem | Correct |
|---|---|---|
| Aesthetics first | Using rainbow/jet palettes to make charts "look good" | Grayscale-safe restrained academic palette |
| No QA delivery | Code runs → delivery without review | QA Contract required: readability, data consistency, format compliance |
| Invented architecture | Prompts include non-existent module connections | Architecture from code/paper evidence only; unconfirmed items marked |
| Delivering unchecked generated images | Image looks professional but modules/arrows may be wrong | Contract first, verify module-by-module after generation |

## Out of Scope

- Non-academic commercial charts
- Interactive plotting (Plotly, Bokeh, D3.js)
- Adobe Illustrator / TikZ completed figures that need no modification
- EDA-only statistics reporting without publication target
