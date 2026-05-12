---
name: "academic-polishing"
description: "Use when polishing academic prose, de-AI-ifying text, controlling claim strength, or rewriting method sections into proper narrative form. Triggers on: 润色, polish, improve writing, 去AI, de-AI, claim strength, 改写, rewrite method, prose quality."
---

# Academic Polishing

将此 skill 视为"学术文体打磨代理"——不是简单润色，而是执行 prose 质量闸门、去AI化改写、claim 强度控制和 Method 专项叙事强化。

## 非协商规则

- 正文应读起来像经验丰富的人类学者撰写，而非模板驱动的机器输出。
- 空洞强化词必须有数据或 VERIFIED 引用支撑，否则删除或替换为具体描述。
- AI 典型连接词（Moreover、Furthermore、However、Therefore、In summary）必须替换为上下文相关的自然表述。
- 句子之间应建立因果、递进、转折或并列补足的深层逻辑，而非只靠连接词维持表面连贯。
- 正文不得残留元评论口吻、审稿人对话口吻、代码讲解口吻或 checklist 痕迹。
- Claim 强度必须与证据等级匹配：强结论需有本地可复核结果 + 无协议缺陷。
- Method 相关 section 必须形成"问题 → 设计 → 机制 → 收益/边界"叙事，而非公式罗列。

## 任务模式

1. **prose-quality-gate** — 执行通用 prose 质量检查与改写
2. **method-prose-rewrite** — Method 专项正文化（问题→设计→机制→收益/边界）
3. **de-ai-pass** — 仅执行去AI化改写
4. **claim-strength-audit** — 审计并调整 claims 强度

## 工作流

### Step 1: 确认当前 section 类型与改写目标

- 明确是 Introduction / Related Work / Method / Experiments / Discussion / Conclusion
- 不同 section 有不同的 prose 检查重点

### Step 2: 执行通用 Prose Quality Gate

检查以下项目并记录：

**通用检查项：**
- 正文是否仍以提纲句、说明句为主，而非完整 prose 段落
- 是否存在元评论口吻、审稿人对话口吻或代码讲解口吻
- 是否符合去AI化规范（详见 `references/de-ai-patterns.md`）

**章节专项检查项：**
- Introduction / Related Work：是否只有列举，缺少论证链、综合比较或 work-cluster 叙事
- Method：是否仍停留在公式罗列或模块说明，缺少"问题 → 设计 → 机制 → 收益/边界"叙事
- Experimental Setup / Data：是否只有参数或流程罗列，缺少协议、约束与风险说明
- Discussion / Limitations / Conclusion：是否只有泛泛结论，缺少边界分析、失败模式或限制讨论

输出：
- `prose_debt: open|closed`
- `failed_items: [list]`

### Step 3: Prose Rewrite（若 prose_debt 为 open）

- 将提纲式句子改为完整论证段落
- 将元评论、说明文和代码导览口吻改写为学术 prose
- 将罗列式段落改为具有论证链和段内逻辑衔接的连贯段落
- 执行去AI化改写（参考 `references/de-ai-patterns.md`）

### Step 4: Method Prose Rewrite（若当前为 Method section）

在通用 Prose Quality Gate 之后，额外执行 Method 专项强化（详见 `references/method-narrative.md`）：

重点检查：
- 是否仍存在公式罗列而缺少"问题 → 设计 → 机制 → 收益/边界"叙事
- 模块段首是否直接落在"该模块解决什么问题"
- 是否仍残留"从实现看""一个合理解释是""当前代码表明"等推断降级不充分的口吻

正文中优先使用以下开头方式：
- "为缓解……问题，本文……"
- "考虑到……，本文采用……"
- "与……相比，该设计……"
- "为使……能够……，我们进一步……"

### Step 5: Claim Strength Audit（按需）

详见 `references/claim-strength.md`。

| 强度 | 条件 | 典型表达 |
|------|------|---------|
| Strong | 本地可复核 + 无协议缺陷 | show, demonstrate, outperform |
| Medium | 内部验证 / baseline 不全 | suggest, indicate, appears to improve |
| Weak | 仅 user_claim / 无法复核 | may, could, requires further validation |

- 主动降级不匹配的 claims
- 把内部验证包装成外部泛化 → 必须降级
- 把缺失 baseline 的结果写成 SOTA → 必须降级

### Step 6: 输出

```md
## Prose Quality Gate Result
- prose_debt: open|closed
- failed_items: [...]
- method_prose_debt: open|closed (if applicable)

## Rewritten Text
（改写后的正文段落）

## Claim Strength Changes
- Original: "X outperforms Y" → Revised: "X appears to improve over Y on internal validation"
- ...
```
