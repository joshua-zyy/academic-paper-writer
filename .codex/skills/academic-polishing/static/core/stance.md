# Polishing Stance

Academic polishing improves clarity, prose quality, and claim calibration. It must not repair missing evidence by making unsupported text sound more convincing.

## Evidence-Aware Boundary

- If `evidence_debt = closed`, perform full prose quality gate, de-AI pass, and claim-strength audit.
- If `evidence_debt = open`, perform only safe repair: grammar, clarity, removal of meta-commentary, and claim weakening.
- If `section_contract_debt = open`, diagnose the structural gap and apply only local safe edits.

## Structural Debt Is Not Prose Debt

Missing section moves, missing reader-state transitions, absent evidence hooks, and rationale gaps must be returned to `academic-paper-writer` or `academic-reviser`; do not hide them with smoother prose.

## Shared Rules

Use `skills/shared/core/evidence-policy.md` and `skills/shared/core/non-invention-rules.md` for evidence and invention boundaries.
