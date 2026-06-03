---
name: academic-figure
description: "Create, revise, or audit academic figures for CS/AI/ML papers. Data/result plots default to Python-generated editable SVG with CS/AI/ML-specific design rules for benchmarks, ablations, training dynamics, robustness, diagnostics, and efficiency tradeoffs; model framework, overview, and complex mechanism diagrams default to an evidence-grounded image-generation workflow. Use when: generating model framework images, overview figures, module detail diagrams, data plots from experiment results, auditing figures, suggesting figure types, revising colors/layouts/labels. Use architecture-svg only for simple explicit vector requests; use arch-prompt only when the user explicitly asks for external prompts. Triggers on: 绘图, figure, chart, 画图, 实验图, 训练曲线, 消融实验, 对比图, 混淆矩阵, 架构图, 模型框架图, overview figure, model architecture, plot, publication figure, 数据可视化, generate plot, architecture diagram, figure blueprint, 建议图表类型, figure audit, 审查图表, figure revision, 修改图表."
---

# Academic Figure

CS/AI/ML academic-figure router. 实验数据图默认交付 Python/matplotlib 可编辑 SVG，并执行 CS/AI/ML 图表设计 gate。模型框架图、overview figure、复杂模块图和机制图默认走 `architecture-image`：先建立事实合约，再用生图模型生成高分辨率图像，必要时追加可编辑标注层。提示词不是默认最终交付物。

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
| `chart-from-data` | Data files or numeric results, needs publication plot with CS/AI/ML chart design gate |
| `architecture-image` | 模型框架图、overview figure、复杂模块图、机制图；默认使用生图模型生成 |
| `architecture-svg` | 仅用于简单流程/结构图，或用户明确要求可编辑 SVG 的兼容路径 |
| `arch-prompt` | 仅当用户明确要求外部生图提示词且不需要本轮出图时使用 |
| `figure-blueprint` | Wants figure suggestions for a paper section |
| `figure-audit` | Existing figure reviewed for publication readiness |
| `figure-revision` | Existing figure needs revision |

## Agent Dispatch

`agents/figure_agent.md` is dispatched by the orchestrator at Step 6.4. The agent returns figure artifacts, scripts, SVG paths, and reports; it must not independently edit project source code or experimental data.

## Completion Criteria

- `chart-from-data`: Figure Contract, CS/AI/ML chart design gate, Python script, source data, editable SVG, QA report — all pass.
- `architecture-image`: Architecture Contract, generation prompt, generated high-resolution image path, optional editable annotation overlay, caption draft, factual/visual verification report.
- `architecture-svg`: Architecture Contract, Python 绘图脚本, 可编辑 SVG, caption draft, 事实核对清单；仅作为简单/显式矢量路径.
- `arch-prompt`: 仅交付外部工具兼容提示词，并明确标注“非默认出图路径”.
- `figure-audit`: Every QA item has pass/fail status and concrete remediation.
- `figure-blueprint`: Every suggested figure maps to a paper claim and data/evidence source.
- `figure-revision`: Revised artifact or instructions, QA report, unchanged evidence traceability.
