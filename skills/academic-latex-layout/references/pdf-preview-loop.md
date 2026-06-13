# PDF Preview Loop

Use this loop after draft generation or repair whenever compilation is feasible.

## Loop

1. Discover the build command from project files or user instructions. Prefer existing commands over inventing new ones.
2. If no command exists, use a conservative fallback: try `latexmk -pdf <main.tex>` when available; otherwise use the engine implied by the template or user files.
3. Compile with the least invasive command available. Common options are `latexmk`, `make`, `pdflatex`, or `xelatex`, depending on the project.
4. Inspect logs for missing assets, unresolved references, overfull boxes, underfull vboxes, float warnings, package conflicts, too many unprocessed floats, and page count changes.
5. If compilation fails, fix direct-safe blockers first in this order: missing asset paths, unresolved includes, obvious label/reference mistakes, then over-restrictive float specifiers. Do not comment out scientific content unless the user approves a diagnostic-only compile.
6. Preview or inspect the PDF using available tools. If visual preview is unavailable, verify PDF generation and provide bounded assessment.
7. Check PDF-level layout: evidence near explanation, no severe float clusters, no avoidable large blank regions, readable captions/tables, acceptable page/column breaks, and page-limit status.
8. Map each PDF finding to a direct-safe edit or a confirm-first recommendation.
9. Apply only direct-safe edits and repeat the loop.
10. Stop after three direct-safe compile/PDF iterations, when no direct-safe issue remains, when compilation is blocked, or when further improvement requires confirmation.

## Reporting

Always report the command used, whether compilation succeeded, what PDF review found, what was fixed after preview, and what remains unverified.

If the loop stops at the iteration cap, report the remaining issues as a ranked list rather than continuing to churn.

## Bounded Assessment

If no compiler, PDF tool, or source assets are available, state:

- What source-level checks were completed.
- Why compile/PDF preview could not run.
- Which layout claims remain unverified.
- What the user can provide to continue the loop.
