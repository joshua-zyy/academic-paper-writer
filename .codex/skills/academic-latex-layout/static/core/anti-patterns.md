# Anti-Patterns

| Anti-pattern | Why it fails | Correct alternative |
|---|---|---|
| Global `[H]` rescue | Creates blank space, breaks float optimization, and ignores two-column constraints | Diagnose float backlog and apply local placement, sizing, barriers, or `figure*` choices |
| Syntax-only draft conversion | Produces compilable TeX but not a readable paper layout | Build a template profile and semantic float map before inserting figures/tables |
| Spacing-hack page fitting | Negative spacing hides root causes and can violate venue/readability constraints | Fix float density, widths, captions, and placement first; ask before readability-reducing compression |
| Source-only success claim | `.tex` may look reasonable while the PDF still has float clusters or blank pages | Compile and inspect the PDF when feasible |
| Blind `\clearpage` | Flushes floats by creating disruptive page breaks | Use local movement, barriers, or float sizing; reserve page breaks for intentional section transitions |
| Unconfirmed semantic edit | Changes the paper to satisfy layout rather than preserving the research argument | Ask before text shortening, figure splitting/merging, numbering changes, or claim edits |
| Template override | Local aesthetics can violate submission rules | Preserve official class/style files and document any unknown venue constraint |
