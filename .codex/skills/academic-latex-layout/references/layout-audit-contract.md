# Layout Audit Contract

Use `layout-audit` when the user wants diagnosis only or when edits are unsafe without confirmation.

## Rules

- Do not edit files.
- You may compile or preview the PDF if the user request and environment permit read/build operations.
- Separate source-level findings from PDF-level findings.
- Rank issues by severity and reading impact.
- Classify every proposed fix as direct-safe or confirm-first.

## Severity

| Severity | Meaning |
|---|---|
| P0 | Layout blocks compilation, hides content, or violates venue constraints |
| P1 | Figure/table is far from its explanation or float clusters harm readability |
| P2 | Blank space, weak caption/table readability, or inefficient placement affects flow |
| P3 | Minor polish: local spacing, label wording, or consistency |

## Required Output

Use `report-format.md` and include enough evidence for the user to decide whether to allow repair mode.
