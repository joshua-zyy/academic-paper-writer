# Polishing Output Contract

## Deliverable Format

```markdown
## Prose Quality Gate Result
- prose_debt: open|closed
- section_contract_debt: open|closed
- failed_items:
- method_prose_debt: open|closed (if applicable)

## Rewritten Text
[revised prose or safe local repair]

## Claim Strength Changes
- Original: ...
- Revised: ...
- Reason: ...
```

## Completion Criteria

- **prose-quality-gate / de-ai-pass**: Max 2 rewrite rounds. After 2 rounds, deliver with prose_debt status.
- **method-prose-rewrite**: 问题 → 设计 → 机制 → 收益/边界 narrative established.
- **claim-strength-audit**: All zero-tolerance trigger words checked. All mismatched claims downgraded.

If structural or evidence_debt prevents safe polishing, return the diagnosis and the smallest safe text repair instead of rewriting the whole section.
