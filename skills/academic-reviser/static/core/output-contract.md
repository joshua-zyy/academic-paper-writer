# 修订器输出契约（Reviser Output Contract）

## Verification Status

输出遵循 `skills/shared/schemas/verification-report.md`。

**Debt types**（8 个，字段名必须保留）：
- `prose_debt`, `section_contract_debt`, `citation_debt`, `evidence_debt`, `figure_debt`, `protocol_debt`, `result_debt`, `rationale_debt`

## 交付物

### full-section-review / targeted-review

- Section Critique
- Revised Draft（必须真正吸收修复点）
- Verification Status（`passed`/`failed`/`blocked`）

### cross-section-review

- 跨章节一致性报告
- 标记出的冲突项

### verification-only

- 仅输出 Verification Status，不重新审稿

### targeted-evidence-mode

- `evidence_debt: open|closed`
- `evidence_issues` list
- 不修改 prose

### mock-reviewer-package

- 3 份 reviewer-style reports + cross-review synthesis
- 可选输出，不能替代 Verification Status
- 不得编造 reviewer identities 或未提供的 evidence
