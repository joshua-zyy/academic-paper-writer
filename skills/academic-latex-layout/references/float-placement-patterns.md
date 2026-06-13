# Float Placement Patterns

These are heuristics, not universal rules. Venue templates may override them.

## Placement Specifiers

| Pattern | Use when | Caution |
|---|---|---|
| `[t]` | Most two-column paper figures/tables that should appear near the top of a column | May still drift if float density is high |
| `[tbp]` | Flexible placement is better than exact placement | Can move to float page if backlog grows |
| `[!t]` | A top placement is strongly preferred and template allows mild constraint relaxation | Do not use as a blanket default |
| `[htbp]` | Single-column documents or local floats where here-placement is acceptable | `h` is only a suggestion, not a guarantee |
| `[p]` | A float page is preferable to severe text/float separation or backlog | Use sparingly; explain the reading-flow tradeoff |
| `[H]` | Rare emergency for small floats that must remain exactly in place | Never apply globally; often creates blank space |

## Two-Column Layout

- Use `figure` or `table` for column-width content.
- Use `figure*` or `table*` only when details are unreadable in one column or the claim needs a full-width comparison.
- Full-width floats usually appear at page tops; plan around the PDF result, not the source location.
- Bottom placement for full-width floats may require packages such as `stfloats` or `dblfloatfix`; treat those as confirm-first package changes after template compatibility checks.

## Barriers and Page Breaks

- Prefer moving floats and reducing float density before adding barriers.
- Use `\FloatBarrier` sparingly at meaningful section boundaries.
- Avoid placing barriers so densely that less than a few paragraphs of text can flow between them.
- Avoid `\clearpage` unless the paper intentionally starts a new major part and the user accepts the break.
- `\afterpage{\clearpage}` can be a controlled alternative for deferred float flushing, but it is still confirm-first unless the project already uses the pattern safely.

## Sizes and Captions

- Start with `width=\columnwidth` for column floats and `width=\textwidth` for full-width floats.
- Reduce width only while axis labels, legends, and table text remain readable.
- Captions are content. Shorten only with confirmation unless fixing punctuation or label consistency.
- Caption font or spacing changes are layout changes, not content changes, but still require template compatibility checks.

## Consolidation

- Consolidating related small figures into subfigures can reduce float pressure, but changing figure grouping or numbering is confirm-first.
- Reorganizing panels inside an existing multi-panel figure is direct-safe only when labels, captions, and meaning stay unchanged.

## Readability Guardrails

- Do not shrink plots below the point where axis labels, legends, markers, or table values are readable in the compiled PDF.
- If readability is uncertain, classify the shrink as confirm-first and report the PDF preview uncertainty.

## Float Density

If several floats cluster in one section, first check whether some belong earlier or later according to their semantic map. Do not solve density by pushing evidence away from explanation.
