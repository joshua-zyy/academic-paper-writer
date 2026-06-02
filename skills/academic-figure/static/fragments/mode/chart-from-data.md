# Mode: chart-from-data

Use this mode when the user provides data files, tables, metrics, or numeric experiment results and wants a publication plot.

## Workflow

1. Confirm the core conclusion, data source, target venue, and export needs.
2. Build the Figure Contract using `references/figure-contract.md`.
3. Select chart type using `references/chart-types.md`.
4. Generate Python plotting code using `references/api.md` and existing scripts as templates.
5. Export SVG with editable text; add PDF/TIFF/PNG only when needed.
6. Run QA using `references/qa-contract.md` and `scripts/qa_figure.py` when an SVG exists.
7. If any QA item fails, revise code and re-run. Maximum **2 QA rounds**. After 2 rounds, deliver with marked failures.

Do not invent missing values. If required statistics or sample sizes are missing, mark them as missing and weaken any caption claim. Prefer editable SVG as primary output; source data (CSV/TSV) must be delivered alongside the figure.
