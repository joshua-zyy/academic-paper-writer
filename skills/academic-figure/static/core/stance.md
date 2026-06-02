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

## Non-Invention Rules

Use `skills/shared/core/non-invention-rules.md`. Never invent data values, model modules, architecture connections, losses, datasets, or training flows.

## Visual Policy

- Prefer restrained academic palettes and direct labels.
- Use one visual hierarchy per figure: one hero message plus supporting evidence when appropriate.
- Treat statistics, sample size, error-bar meaning, source-data traceability, and image-integrity notes as part of the figure, not afterthoughts.
- Use short labels in generated architecture images; move long explanations to captions or legends.
