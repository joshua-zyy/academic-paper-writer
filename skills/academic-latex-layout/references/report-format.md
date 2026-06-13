# Report Format

Use concise Markdown reports. Include file paths when edits were made.

## Draft-to-LaTeX Layout Report

```markdown
## LaTeX Layout Generation Report

Status: passed | partial | blocked
Mode: draft-to-latex-layout

### Template Profile
[documentclass, style files, column mode, relevant packages, page limit]

### Generated/Modified Files
| File | Purpose |
|---|---|

### Semantic Float Map
| Float | Asset/Label | Supports | Target placement | Risk |
|---|---|---|---|---|

### Compile and PDF Review
- Compile command:
- Compile status:
- PDF preview status:
- Findings:

### Confirmation Required
- [items requiring user approval, with expected benefit and risk]
```

## Layout Repair Report

```markdown
## LaTeX Layout Repair Report

Status: passed | partial | blocked
Mode: layout-repair

### Symptoms and Root Causes
| Issue | Evidence | Root cause |
|---|---|---|

### Direct Edits Made
| File | Float/Location | Change | Reason |
|---|---|---|---|

### Compile and PDF Review
- Compile command:
- Compile status:
- PDF preview status:
- Remaining PDF findings:

### Confirmation Required
- [high-risk fixes not applied, ranked by readability impact, page savings, and venue risk]
```

## Layout Audit Report

```markdown
## LaTeX Layout Audit Report

Status: audit-only
Mode: layout-audit

### Findings
| Severity | Issue | Evidence | Proposed fix | Risk class |
|---|---|---|---|---|

### Compile and PDF Evidence
- Compile status:
- PDF preview status:
- Bounded assessment:

### Recommended Next Step
[repair mode / provide assets / approve high-risk change / no action]
```
