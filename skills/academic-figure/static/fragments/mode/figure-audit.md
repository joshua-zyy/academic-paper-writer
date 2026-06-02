# Mode: figure-audit

Use this mode when the user asks whether an existing figure is publication-ready.

## Workflow

1. Confirm audit scope: one figure, all figures, or selected panels.
2. Run QA using `references/qa-contract.md`. Check: claim visibility, panel redundancy, source-data traceability, statistical completeness, color safety, text editability, export format, axis ethics, and grayscale readability.
3. For architecture images, verify modules, arrows, labels, and caption claims against provided evidence.
4. Return pass/fail QA table with concrete revisions. Failed items must include specific fix instructions.

Open `references/qa-contract.md` before starting the audit — it is the mandatory checklist, not an optional reference.
