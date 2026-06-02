# Polishing Output Contract

Return:

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

If structural or evidence_debt prevents safe polishing, return the diagnosis and the smallest safe text repair instead of rewriting the whole section.
