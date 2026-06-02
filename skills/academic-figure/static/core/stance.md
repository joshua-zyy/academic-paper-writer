# Figure Stance

Academic figures are visual arguments. Start from the claim and evidence chain before choosing chart type, colors, or layout.

## Python-Only Plotting

For quantitative data figures, use Python scripts for drawing, previewing, exporting, and QA. The primary vector output is SVG with editable text. PDF and TIFF/PNG exports may be added when needed for submission bundles.

## Figure Contract First

Before plotting or prompting, establish:

1. `Core conclusion`: the one-sentence claim the figure supports.
2. `Evidence chain`: data, artifacts, or architecture evidence behind each panel.
3. `Panel mapping`: each panel's unique role; remove redundant panels.
4. `Reviewer risk`: what a skeptical reviewer may challenge.
5. `Export bundle`: script, source data, vector output, caption, and QA report.

## Non-Negotiable Rules

1. Figures must serve a claim — no visual decoration for its own sake.
2. Each panel must answer a unique question — no redundant panels.
3. When axes start from a non-zero value, must mark the truncation point — do not silently zoom.
4. Error bars / confidence intervals must include their meaning (std / SEM / 95% CI) — do not draw unexplained whiskers.
5. Color must not rely on hue as the sole differentiator — combine with luminance difference, texture, or labels for colorblind-safe accessibility.
6. SVG output for data plots must have editable text — do not render all text as paths.
7. Source data (CSV/TSV) must be delivered alongside the figure — do not deliver image-only outputs.
8. Follow `../shared/core/non-invention-rules.md`. Never invent data values, model modules, architecture connections, losses, datasets, or training flows.

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
- Use short labels in generated architecture images; move long explanations to captions or legends.
- Color must not rely on hue as the sole differentiator — combine with luminance difference, texture, or labels for colorblind-safe accessibility.
- When axes start from a non-zero value, must mark the truncation point — do not silently zoom.

## Scope

Non-academic commercial charts, interactive plotting (Plotly, Bokeh, D3.js), Adobe Illustrator / TikZ completed figures needing no modification, and EDA-only statistics without publication target are out of scope.
