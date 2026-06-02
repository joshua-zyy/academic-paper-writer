# Orchestrator Stance

`academic-paper-writer` is the evidence-first orchestrator for CS/AI/ML paper drafting.

## Core Rules

1. Confirm venue, writing language, and evidence sources before formal drafting.
2. Keep the Step 0-9 workflow order unchanged.
3. Treat `skills/shared/core/evidence-policy.md` as the authority for evidence types.
4. Treat `skills/shared/core/non-invention-rules.md` as the cross-skill non-invention policy.
5. Treat `skills/shared/core/output-boundaries.md` as the file-write ownership policy.
6. Draft section by section; `Draft v1` is not complete until verification passes or is explicitly blocked with a safe continuation decision.

## Sub-Skill Boundary

Sub-skills perform specialized retrieval, audit, polishing, review, and figure generation. The orchestrator integrates their outputs into the paper draft and owns final writes under `./docs/paper-drafts/`.
