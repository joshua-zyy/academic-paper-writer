# Mock Reviewer Package

Use this reference only for `mock-reviewer-package` mode. This mode produces reviewer-style assessment for pre-submission risk discovery. It does not replace `Verification Status` and must not act as an editor decision letter.

## Required Setup

Start with:

```markdown
## Review Setup
- Input scope:
- Assessment boundary:
- Shared manuscript claim summary:
- Visible evidence base:
- Missing materials affecting confidence:
```

If the input is partial, continue with a bounded review and mark non-assessable items explicitly.

## Output Structure

```markdown
## Reviewer 1
- Emphasis: technical soundness / evidence chain
- Overall assessment:
- Major strengths:
- Major concerns:
- Technical failings that need to be addressed before the case is established:
- Unsupported or not-assessable claims:

## Reviewer 2
- Emphasis: originality / significance
- Overall assessment:
- Major strengths:
- Major concerns:
- Technical failings that need to be addressed before the case is established:
- Unsupported or not-assessable claims:

## Reviewer 3
- Emphasis: readability / broader audience / framing
- Overall assessment:
- Major strengths:
- Major concerns:
- Technical failings that need to be addressed before the case is established:
- Unsupported or not-assessable claims:

## Cross-Review Synthesis
- Consensus strengths:
- Consensus risks:
- Where emphasis differs:
- Most important issues to resolve:

## Risk / Unsupported Claims
- [specific unsupported or not-assessable item]
```

## Non-Invention Rules

- Do not invent reviewer identities, institutions, seniority, specialties, or hidden expertise.
- Do not invent experiments, controls, datasets, citations, figure panels, line numbers, or prior-work distinctions.
- Do not state an editorial decision or claim certainty about venue acceptance.
- Reviewer differences may reflect emphasis only, not access to different facts.

## Relation to Verification

After the reviewer package, still provide or preserve the normal `Verification Status` if the orchestrator expects it. Reviewer reports are diagnostic; `Verification Status` remains the machine-consumable gate output.
