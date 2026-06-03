# 图表立场（Figure Stance）

学术图表是视觉论证。先确定 claim 与证据链，再选择图表类型、配色或布局。

## Hybrid Output Policy

实验数据图默认直接生成可编辑 SVG：使用 Python/matplotlib，PDF 和 TIFF/PNG 可作为投稿补充格式，但不能替代 SVG 主输出。

模型框架图、overview figure、复杂模块图和机制图默认使用生图模型制作：先建立 Architecture Contract，再生成高分辨率 PNG/WebP/TIFF 等图像。若图中需要精确文字、编号或投稿排版，优先使用短标签/编号，并可追加可编辑 SVG/PDF 标注层；不要把复杂架构强行塞进 Python 矢量元素。简单流程图或用户明确要求可编辑矢量时，才使用 `architecture-svg` 兼容路径。

提示词不是默认最终交付物。只有用户明确要求外部 prompt，或当前环境无法调用生图模型时，才交付提示词并说明状态。

## Figure Contract First

Before plotting or prompting, establish:

1. `Core conclusion`: the one-sentence claim the figure supports.
2. `Evidence chain`: data, artifacts, or architecture evidence behind each panel.
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
9. 用户要求“绘制论文图”时，不得只交付 prompt；数据图必须交付可编辑 SVG，架构图必须尝试生图模型或明确说明缺失哪些证据/运行环境导致无法绘制。

## AI Intervention Boundary (Traffic Light)

| 🟢 Green — Direct | 🟡 Yellow — Cautious | 🔴 Red — Forbidden |
|---|---|---|
| Auto-select axis ranges from data | Auto-preset significance level (must confirm) | Invent data or network structures |
| Apply colormap rules (academic palette, fonts) | Guess missing statistics | Output final publication version without review |
| Add panel labels (a/b/c/d) | Auto-choose chart type (must confirm ambiguous requests) | Use 3D bar charts instead of 2D |
| Standard layout and alignment | Merge separate charts into multi-panel | Use colorblind-unfriendly palettes |
| Detect missing dependencies and prompt install | Speculate missing modules in architecture diagrams | Treat placeholder images as final output |

## Visual Policy

- Prefer restrained academic palettes and direct labels.
- Use one visual hierarchy per figure: one hero message plus supporting evidence when appropriate.
- Treat statistics, sample size, error-bar meaning, source-data traceability, and image-integrity notes as part of the figure, not afterthoughts.
- Use short labels or numbered callouts in generated architecture images; move long explanations to captions or legends.
- Color must not rely on hue as the sole differentiator — combine with luminance difference, texture, or labels for colorblind-safe accessibility.
- When axes start from a non-zero value, must mark the truncation point — do not silently zoom.

## Scope

Non-academic commercial charts, interactive plotting (Plotly, Bokeh, D3.js), Adobe Illustrator / TikZ completed figures needing no modification, and EDA-only statistics without publication target are out of scope.
