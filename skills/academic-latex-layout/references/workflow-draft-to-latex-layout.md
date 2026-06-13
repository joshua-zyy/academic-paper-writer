# Draft To LaTeX Layout Workflow

Use this workflow when the input is a paper draft plus a target LaTeX template and existing figure/table assets or captions.

## Steps

1. Inventory inputs: draft source, template files, bibliography, figure/table assets, captions, target venue, page limit, and expected compile command if provided.
2. Build the template profile using `template-constraints.md` before writing content into the template.
3. Validate asset existence before writing `\includegraphics` or table inputs. Missing assets block compilation and must be reported early.
4. Preserve section order and argument flow from the draft. Do not reorganize the paper to fit floats.
5. Build a semantic float map for every asset: file path, caption, label, evidence type, related claim, first textual reference, first meaningful discussion, and target section.
6. Check anonymity-sensitive assets when the venue is double blind: visible logos, author names, institution names, and identifying file metadata. Infer double-blind risk from venue name/template when possible; ask if unclear. Ask before modifying assets.
7. Convert the draft to LaTeX using the template's existing structure. Keep package additions minimal and template-compatible.
8. Insert floats near first meaningful discussion. A forward pointer such as "we later show" is not automatically the best insertion point.
9. Use `figure`, `figure*`, `table`, or `table*` according to column mode and readability. Use `width=\columnwidth` for normal column figures and `width=\textwidth` for full-width floats when justified.
10. Convert static figure/table mentions to `\ref{...}` only when labels are stable or generated unambiguously.
11. Compile and run the PDF preview loop from `pdf-preview-loop.md`.
12. Report generated files, float map, compile/PDF findings, and confirm-first recommendations.

## Stop Conditions

- Required template or assets are missing.
- A figure/table cannot be mapped to a relevant claim or paragraph.
- The next improvement requires shortening text, splitting/merging figures, adding risky packages, or changing template files.
