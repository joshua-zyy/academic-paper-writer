# Mode: figure-blueprint

Use this mode when the user provides a paper section, outline, or claim list and asks what figures are needed.

## Workflow

1. Identify section purpose and key claims. Confirm paper context and venue figure conventions.
2. Map each figure candidate to one claim and one evidence source. Scan for visualizable content: method flow → architecture, results → training/comparison curves, analysis → distribution/scatter.
3. Classify figure type: architecture, pipeline, comparison, ablation, trend, distribution, or diagnostic.
4. Mark missing data or architecture evidence explicitly.
5. Recommend only executable figures; do not propose figures that require unavailable evidence unless marked as blocked.

Output: a suggestion list with figure type, target section, core claim, data source, and whether data coverage exists.
