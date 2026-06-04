# 图表立场（Figure Stance）

学术图表是视觉论证。先确定 claim 与证据链，再选择图表类型、配色或布局。

## Output Policy

实验数据图默认直接生成可编辑 SVG：使用 Python/matplotlib，PDF 和 TIFF/PNG 可作为投稿补充格式，但不能替代 SVG 主输出。

模型框架图、架构图、overview figure、复杂模块图和机制图不属于本 skill 的自动绘制范围。遇到此类需求时，只能输出人工绘制需求、证据清单、caption 草案或 figure blueprint notes；不得生成图片、SVG 或外部生图 prompt 作为替代交付。

## Figure Contract First

Before plotting or prompting, establish:

1. `Core conclusion`: the one-sentence claim the figure supports.
2. `Evidence chain`: data, artifacts, or manual figure evidence behind each panel.
3. `Panel mapping`: each panel's unique role; remove redundant panels.
4. `Reviewer risk`: what a skeptical reviewer may challenge.
5. `Export bundle`: script, source data, vector output, caption, and QA report.

## 不可协商规则

1. Figures must serve a claim — no visual decoration for its own sake.
2. Each panel must answer a unique question — no redundant panels.
3. When axes start from a non-zero value, must mark the truncation point — do not silently zoom.
4. Error bars / confidence intervals must include their meaning (std / SEM / 95% CI) — do not draw unexplained whiskers.
5. Color must not rely on hue as the sole differentiator — combine with luminance difference, texture, or labels for colorblind-safe accessibility.
6. Data-plot SVG output must have editable text — do not render all text as paths.
7. Source data (CSV/TSV) must be delivered alongside the figure — do not deliver image-only outputs.
8. Follow `../shared/core/non-invention-rules.md`. Never invent data values, model modules, architecture connections, losses, datasets, or training flows.
9. 用户要求“绘制论文图”时，不得只交付 prompt；数据图必须交付可编辑 SVG。模型框架图、架构图和复杂机制图应标记为人工绘制需求或超出自动绘制范围。

## AI Intervention Boundary (Traffic Light)

| 🟢 Green — Direct | 🟡 Yellow — Cautious | 🔴 Red — Forbidden |
|---|---|---|
| Auto-select axis ranges from data | Auto-preset significance level (must confirm) | Invent data or network structures |
| Apply colormap rules (academic palette, fonts) | Guess missing statistics | Output final publication version without review |
| Add panel labels (a/b/c/d) | Auto-choose chart type (must confirm ambiguous requests) | Use 3D bar charts instead of 2D |
| Standard layout and alignment | Merge separate charts into multi-panel | Use colorblind-unfriendly palettes |
| Detect missing dependencies and prompt install | Mark model diagrams as manual figure needs | Treat placeholder images as final output |

## Visual Policy

- Prefer restrained academic palettes and direct labels.
- Use one visual hierarchy per figure: one hero message plus supporting evidence when appropriate.
- Treat statistics, sample size, error-bar meaning, source-data traceability, and image-integrity notes as part of the figure, not afterthoughts.
- Color must not rely on hue as the sole differentiator — combine with luminance difference, texture, or labels for colorblind-safe accessibility.
- When axes start from a non-zero value, must mark the truncation point — do not silently zoom.

## Scope

Non-academic commercial charts, interactive plotting (Plotly, Bokeh, D3.js), model framework/architecture/overview/mechanism diagrams, Adobe Illustrator / TikZ completed figures needing no modification, and EDA-only statistics without publication target are out of scope.
