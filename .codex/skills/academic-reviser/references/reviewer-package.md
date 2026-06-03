# 模拟审稿人包（Mock Reviewer Package）

仅在 `mock-reviewer-package` mode 下使用本参考。该模式用于投稿前发现审稿风险，生成 reviewer-style assessment。它不能替代 `Verification Status`，也不得写成编辑部决定信。

## 必要设置

输出必须先包含以下结构：

```markdown
## Review Setup
- Input scope:
- Assessment boundary:
- Shared manuscript claim summary:
- Visible evidence base:
- Missing materials affecting confidence:
```

如果输入只是局部草稿，继续做有边界的 review，并明确标记不可评估项。

## 输出结构

以下标题和字段作为结构化输出契约保留英文：

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

## 不得编造规则（Non-Invention Rules）

- 不得编造 reviewer identities、institutions、seniority、specialties 或 hidden expertise。
- 不得编造 experiments、controls、datasets、citations、figure panels、line numbers 或 prior-work distinctions。
- 不得陈述 editorial decision，也不得声称可以确定 venue acceptance。
- 不同 reviewer 只能体现关注重点差异，不能假装他们掌握不同事实。

## 与 Verification 的关系

生成 reviewer package 后，如果编排器需要，仍必须提供或保留正常的 `Verification Status`。Reviewer reports 是诊断性输出；`Verification Status` 才是机器可消费的门控输出。
