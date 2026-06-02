# Figure Output Contract

## `chart-from-data`

- Figure Contract
- Python plotting script
- Source data path or derived clean source data file
- Editable SVG as primary output
- Optional PDF and TIFF/PNG submission exports
- QA report referencing `references/qa-contract.md`

## `architecture-image`

- Architecture Contract
- Image Prompt Spec
- Generated image path or prompt fallback
- Caption draft
- Human-verifiable architecture checklist
- Unconfirmed items marked with `[VERIFY_ARCH: ...]`

## `arch-prompt`

- Architecture analysis
- Tool-agnostic prompt text
- Component list
- Data-flow and connection notes
- Explicit unconfirmed items

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
