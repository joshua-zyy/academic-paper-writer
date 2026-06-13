# Layout Repair Workflow

Use this workflow when a complete `.tex` project already exists and the user reports float pileups, distant figures/tables, blank areas, poor two-column layout, or page-limit pressure.

## Steps

1. Discover the project: main `.tex`, included section files, bibliography, figures directory, build files, generated PDF, and logs.
2. Identify template constraints before editing: class, style files, column mode, loaded float/caption packages, page limit, and prohibited template edits.
3. Inventory every figure/table environment: source file, environment type, placement specifier, caption, label, first `\ref`, first meaningful discussion, size, and section.
4. Diagnose root causes: float backlog, too many floats in one section, oversized assets, wrong `figure*` or `table*`, missing or excessive barriers, static references, unresolved labels, and large float-only gaps.
5. Classify each possible edit as direct-safe, confirm-first, or prohibited by default using `static/core/stance.md`.
6. Apply direct-safe edits only: local movement, local placement tuning, width correction, limited barriers, subfigure organization, and label consistency.
7. Compile using `pdf-preview-loop.md`.
8. Review the PDF outcome. Repeat only for direct-safe fixes that are clearly supported by the PDF findings.
9. Stop when remaining improvements require user confirmation or when compilation/preview is blocked.
10. Produce the layout repair report from `report-format.md`.

## Page-Limit Repair Priority

When the paper is over a hard page limit, try fixes in this order:

1. Remove accidental layout blockers: stale `\clearpage`, excessive barriers, overly restrictive placement specifiers, oversized floats, or missing assets.
2. Move floats according to semantic adjacency to reduce backlog and blank areas.
3. Adjust widths only while labels, legends, and table text remain readable.
4. Use `figure*` or `table*` when full-width placement improves both readability and page flow.
5. Consider local, venue-compatible line recovery such as `\enlargethispage` for one or two lines.
6. Consider caption font or spacing controls only if the template allows them; do not shorten caption text without confirmation.
7. Present ranked confirm-first options when remaining fixes require text cuts, figure consolidation, package additions, or template changes.

## Direct-Safe Repair Examples

| Symptom | Candidate repair |
|---|---|
| Figure appears two pages after first meaningful discussion | Move the float closer to that paragraph and prefer `[t]`, `[tbp]`, or `[!t]` over `[H]` |
| Wide figure is unreadable in one column | Consider `figure*` if the template and reading flow support full-width placement |
| Floats leak into the next section | Add a limited `\FloatBarrier` at the section boundary if `placeins` is already available or safe to add |
| Large blank region before a float | Check whether the asset is too tall/wide, float specifier is too restrictive, or an earlier barrier/page break caused the gap |
| Too many unprocessed floats | Reduce float density by moving floats to semantic locations, relaxing specifiers, or proposing consolidation; do not globally force `[H]` |

## Confirm Before Applying

Ask before shortening text, changing figure order, splitting panels, merging tables, adding risky packages, changing global spacing/page geometry, or applying many local line-recovery commands.

When all remaining options are confirm-first, present two or three ranked choices with readability impact, page savings estimate, and venue risk.

If the user declines all confirm-first options, stop with status `partial` and state that the layout is as improved as possible under direct-safe edits.
