# Academic Paper Writer (Core Orchestrator)

CS/AI/ML 领域**证据驱动、分节推进**的论文编排核心 Skill。它协调证据审计、文献检索、实验复核、prose 润色和审修五个专项环节，按 section unit 串行推进完整论文起草流程。

## 触发方式

- "帮我写一篇论文初稿"
- "根据这个代码仓库起草 Method section"
- "为这篇研究写 Introduction"
- "paper draft for NeurIPS submission"

## 核心能力

| 能力 | 说明 |
|------|------|
| 论文编排 | 确认 venue → 审计证据 → 生成 blueprint → 起草 → 质量闸门 → 审修 → 集成 |
| 五种任务模式 | full-paper-planning / section-drafting / section-revision / citation-pass / experiment-pass |
| 委托协调 | 在文献检索、实验复核、prose 润色、审修环节委托专项子 Skill |
| 双输出 | 正文草稿 + sidecar critique / debt log |

## 与其他 Skill 的关系

本 Skill 是编排核心，在以下步骤委托专项子 Skill：

| 步骤 | 委托 Skill |
|------|-----------|
| Step 3: 文献检索与核验 | `academic-citation` |
| Step 4: 实验事实复核 | `academic-experiments` |
| Steps 6.3-6.5: Prose 质量闸门 | `academic-polishing` |
| Step 8: 自我审查与 Verification | `academic-reviser` |

四个子 Skill 均可独立触发使用，详见各子 Skill 的 README。
