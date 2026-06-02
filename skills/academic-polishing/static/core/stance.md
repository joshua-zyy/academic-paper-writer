# Polishing Stance

Academic polishing improves clarity, prose quality, and claim calibration. It must not repair missing evidence by making unsupported text sound more convincing.

## Non-Negotiable Rules

1. 正文必须读起来像经验丰富的人类学者撰写，不得有模板驱动的机器输出痕迹。
2. 句子之间必须建立因果、递进、转折或并列补足的深层逻辑，不得只靠连接词维持表面连贯。
3. 正文不得残留元评论口吻、审稿人对话口吻、代码讲解口吻或 checklist 痕迹。
4. Claim 强度必须与证据等级严格匹配：强结论需有本地可复核结果 + 无协议缺陷。
5. Method 相关 section 必须形成"问题 → 设计 → 机制 → 收益/边界"叙事，不得停留于公式罗列。
6. 当输入中包含 `evidence_debt = open` 时，对标记为证据不足的句子仅修正语法错误，不得进行风格强化或措辞润色——避免将无证据支撑的主张打磨得更有说服力。
7. 当输入中包含 `section_contract_debt = open` 或明显缺少 section-level required moves 时，仅输出问题定位和最小语言修正；不得代替 `academic-paper-writer` 重新设计整节结构。

## AI Intervention Boundary (Traffic Light)

| Green — Direct | Yellow — Cautious | Red — Forbidden |
|---|---|---|
| Replace empty adjectives with concrete descriptions | Infer design motivation from code/implementation (must weaken tone) | Invent experimental evidence, fabricated values |
| Replace typical AI connectors | Supplement method detail descriptions (must mark inference source) | Generate fake citations or fake data |
| Adjust sentence cohesion and logic connections | Expand domain explanations in Discussion (must have literature) | Rewrite user_claim as strong conclusions |
| Fix grammar errors and unnatural expressions | Downgrade mismatched claim strength | Delete placeholders without adding content |
| Rewrite outline sentences into full paragraphs | Rewrite weak inference as determinate author intent | Add "significantly improve" type language without evidence |

## Claim Strength

| Level | Condition | Typical Expression |
|---|---|---|
| Strong | Locally verifiable + no protocol defects | show, demonstrate, outperform |
| Medium | Internal validation / incomplete baselines | suggest, indicate, appears to improve |
| Weak | user_claim only / unverifiable | may, could, requires further validation |

Must proactively downgrade mismatched claims. Internal validation presented as external generalization → must downgrade. Results missing baselines written as SOTA → must downgrade.

### Zero-Tolerance Trigger Words

| Trigger Word | Required Evidence | Downgrade If Missing |
|---|---|---|
| "显著(地)" / "significantly" | p < 0.05 or effect size / CI | Delete or replace with specific numerical difference |
| "稳定(的)" / "robust" / "stable" | Multiple random seeds / cross-validation / external test set | "consistent within observed..." |
| "作为" / "acts as" / "serves as" | Causal intervention experiment or consensus literature | "may serve as a candidate..." |
| "表明" / "demonstrates" | All Strong conditions met | "suggests" / "consistent with" |
| "泛化" / "generalization" | Independent test set or multi-dataset validation | "on ... dataset(s)" |
| "SOTA" / "state-of-the-art" | Complete baseline comparison + independent test set | "compared with the current comparison scope..." |

## Evidence-Aware Boundary

- If `evidence_debt = closed`, perform full prose quality gate, de-AI pass, and claim-strength audit.
- If `evidence_debt = open`, perform only safe repair: grammar, clarity, removal of meta-commentary, and claim weakening.
- If `section_contract_debt = open`, diagnose the structural gap and apply only local safe edits.

## Structural Debt Is Not Prose Debt

Missing section moves, missing reader-state transitions, absent evidence hooks, and rationale gaps must be returned to `academic-paper-writer` or `academic-reviser`; do not hide them with smoother prose.

## Shared Rules

Use `../shared/core/evidence-policy.md` and `../shared/core/non-invention-rules.md` for evidence and invention boundaries.

## Scope

本 Skill 不适用于：
- 非学术文体的通用文本润色
- 已有明确 LaTeX 格式且不需内容修改的场景
- 内容补全（如补实验数据、补引用）——应使用 `academic-experiments` 或 `academic-citation`
