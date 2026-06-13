# Stance

Treat LaTeX layout as evidence placement, not decoration. A figure or table is well placed only when the compiled PDF lets the reader encounter the supporting evidence near the text that explains it.

## Core Rules

- Build a semantic float map before moving or inserting floats: label, caption, first reference, first meaningful discussion, supported claim, source asset, and target section.
- Obey the user's venue template. Preserve document class, official style files, required packages, bibliography style, caption rules, and page geometry unless the user explicitly asks otherwise.
- Prefer local, reversible layout edits over global tuning.
- Compile and inspect the PDF when feasible. Source-level inspection alone is not enough to claim layout success.
- If compilation or preview is unavailable, provide a bounded assessment that states what was checked and what remains unverified.
- Treat compile logs, generated PDFs, existing source files, and user claims as different evidence types. Do not present user-described layout symptoms or venue rules as verified unless checked against files, logs, or PDFs.
- Keep the paper's framework, argument order, and semantic rhythm. Layout optimization must not rewrite the scientific story.

## Edit Risk Tiers

| Tier | Examples | Action |
|---|---|---|
| Direct-safe | Move float environments near relevant text, adjust local placement specifiers, tune widths within readability limits, add limited section barriers | May edit directly |
| Confirm-first | Shorten body text, split/merge figures, change numbering order, add risky packages, alter global geometry, reduce readability for page limits | Ask user first |
| Prohibited by default | Global `[H]`, repeated negative `\vspace`, blind `\clearpage`, template file edits, semantic changes for layout convenience | Do not do unless user explicitly overrides and risk is documented |

## PDF Evidence

When a PDF is available, judge layout from the PDF, not from the `.tex` diff. Check figure-text proximity, float clusters, blank regions, page and column breaks, caption/table readability, unresolved references, and page-limit fit.

Limit direct-safe repair loops to three compile/PDF review iterations unless the user explicitly asks to continue. After that, report remaining issues and ranked next options.
