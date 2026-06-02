# Orchestrator Output Contract

The orchestrator owns writes under `./docs/paper-drafts/` during full-paper generation.

## Default Files

- `paper_draft.md`: paper body, references, and pending items
- `section_blueprint.md`: current Section Blueprint and Section Contract
- `venue-brief.md`: target venue requirements and style notes
- `figures/`: figure outputs and `figure_prompts.md`
- `figures/codes/`: generated Python plotting scripts

## Write Boundary

Sub-skills return structured content and suggested paths. The orchestrator performs final writes when running the complete paper workflow.

## Default Deliverables

- **full-paper-planning**: paper_draft.md (complete), section_blueprint.md, venue-brief.md, figures/, Verified References + Citation-to-Claim Map
- **section-drafting**: Updated paper_draft.md (single section)
- **section-revision**: Revised section text or revised section blueprint

## Completion Criteria

- All Hard Gates (A-E) passed
- Thin draft resolved (content density check)
- Final verification passed (all hard debts closed)
- Citations >= min_citations (Gate D)
