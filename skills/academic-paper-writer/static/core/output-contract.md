# Orchestrator Output Contract

The orchestrator owns writes under `./docs/paper-drafts/` during full-paper generation.

## Default Files

- `paper_draft.md`: paper body, references, and pending items.
- `section_blueprint.md`: current Section Blueprint and Section Contract.
- `venue-brief.md`: target venue requirements and style notes.
- `figures/`: figure outputs and `figure_prompts.md`.
- `figures/codes/`: generated Python plotting scripts.

## Write Boundary

Sub-skills return structured content and suggested paths. The orchestrator performs final writes when running the complete paper workflow. Independent sub-skill use may create new files only when the user explicitly asks for file output.
