# 图表输出契约（Figure Output Contract）

## `chart-from-data`

- Figure Contract
- Python plotting script
- Source data path or derived clean source data file
- Editable SVG as primary output
- Optional PDF and TIFF/PNG submission exports
- QA report referencing `references/qa-contract.md`

## `architecture-image`

- Architecture Contract
- Figure scope decision and Visual Director Brief
- Evidence-grounded generation prompt
- Generated high-resolution image as primary output
- Optional editable SVG/PDF annotation overlay for labels, callouts, or final typography
- Caption draft
- Human-verifiable architecture checklist
- Unconfirmed items marked with `[VERIFY_ARCH: ...]`

## `architecture-svg`（简单/显式矢量兼容路径）

- Architecture Contract
- Python vector drawing script
- Editable SVG as primary output
- Caption draft
- Human-verifiable architecture checklist
- Unconfirmed items marked with `[VERIFY_ARCH: ...]`

## `arch-prompt`（仅限用户明确要求）

- Architecture analysis
- Tool-agnostic prompt text
- Component list
- Data-flow and connection notes
- Explicit unconfirmed items
- Must state that this is not the default drawing path

## `figure-blueprint`

- Suggested figures by section
- Core claim per figure
- Data or evidence required
- Feasibility and missing-input notes

## `figure-audit`

- Figure scope
- Pass/fail QA table
- Risk flags
- Concrete revision recommendations

## `figure-revision`

- Revision target
- Execution path: script rerun, prompt revision, or audit-only recommendation
- Revised artifact or revised instructions
- QA report
