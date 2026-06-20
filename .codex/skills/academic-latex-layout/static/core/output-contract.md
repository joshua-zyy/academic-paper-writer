# Output Contract

Every mode must produce a concise report. If editing files, report only changes made by this skill.

## Common Fields

- `mode`: selected mode.
- `template_profile`: document class, venue/style files, column mode, relevant packages, page limit if known.
- `semantic_float_map`: figure/table id, label, caption summary, first reference, first meaningful discussion, target placement.
- `edit_risk`: direct-safe edits made and confirm-first edits proposed.
- `compile_status`: command used, success/failure, important warnings, or bounded assessment.
- `pdf_preview_status`: visual findings from PDF preview, or bounded assessment if preview was unavailable.
- `remaining_risks`: issues that remain unresolved or require user confirmation.

## `draft-to-latex-layout` Report

Include generated/modified TeX files, asset path decisions, label/reference conversion notes, float placement map, compile/PDF review, and confirmation-required items.

## `layout-repair` Report

Include symptoms found, root causes, direct edits made, float movement table, compile/PDF review result, and high-risk recommendations not applied.

## `layout-audit` Report

Do not edit files. Include ranked findings, evidence, proposed fix, risk class, and whether each fix is direct-safe or confirm-first.

## Completion Status

Use one of:

| Status | Meaning |
|---|---|
| `passed` | Direct-safe issues were fixed and compile/PDF review found no blocking layout problems |
| `partial` | Some safe fixes were applied, but remaining issues require confirmation or unavailable tools |
| `blocked` | Required inputs, compilation, assets, or template context are missing |
| `audit-only` | Report-only mode; no edits attempted |
