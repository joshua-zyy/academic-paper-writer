---
name: academic-polishing
description: "Polish academic prose, de-AI-ify text, control claim strength, or rewrite method sections for CS/AI/ML papers. Executes Prose Quality Gate, Claim Strength Audit, and de-AI pass. Use when: removing AI writing patterns from paper text, adjusting claim strength to match evidence level, rewriting method sections with proper narrative flow, improving academic writing quality, checking for overclaiming. Triggers on: 润色, polish, improve writing, 去AI, de-AI, claim strength, 改写, rewrite method, prose quality, 降级表述, remove AI patterns, academic writing polish, 学术润色, 去AI化, 降级结论."
---

# Academic Polishing

将此 skill 视为"学术文体打磨代理"——不是简单润色，而是执行 prose 质量闸门、去AI化改写、claim 强度控制和 Method 专项叙事强化。

## Red Lines（绝对禁止）

1. 禁止将编造内容包装成学术表述
2. 禁止在无数据支撑时使用"显著的""重要的"等空洞强化词
3. 禁止把未核验的 user_claim 改写成确定性的强结论
4. 禁止在 Method 中保留元评论、代码讲解或审稿人对话口吻
5. 禁止用更华丽的措辞掩盖 evidence gap（如用长篇 prose 包装缺失的实验结果）

## AI 介入边界（Traffic Light）

| 🟢 Green — 直接执行 | 🟡 Yellow — 谨慎执行 | 🔴 Red — 禁止 |
|---------------------|---------------------|-------------|
| 替换空洞形容词为具体描述 | 从代码/实现推断设计动机（必须降级语气） | 编造实验证据、虚构数值 |
| 替换 AI 典型连接词 | 补全方法细节描述（必须标注推断来源） | 生成假引用或假数据 |
| 调整句式衔接和逻辑连接 | 扩写 Discussion 中的领域解释（必须有文献） | 把 user_claim 改写成强结论 |
| 改写语法错误和不自然表述 | 降级不匹配的 claim 强度 | 删除占位符但不补内容 |
| 将提纲句改写为完整段落 | 将弱推断改写成确定性作者意图 | 在无证据时添加"显著提升"类表述 |

## 非协商规则

1. 正文必须读起来像经验丰富的人类学者撰写，不得有模板驱动的机器输出痕迹。
2. 句子之间必须建立因果、递进、转折或并列补足的深层逻辑，不得只靠连接词维持表面连贯。
3. 正文不得残留元评论口吻、审稿人对话口吻、代码讲解口吻或 checklist 痕迹。
4. Claim 强度必须与证据等级严格匹配：强结论需有本地可复核结果 + 无协议缺陷。
5. Method 相关 section 必须形成"问题 → 设计 → 机制 → 收益/边界"叙事，不得停留于公式罗列。
6. 当输入中包含 `evidence_debt = open` 时，对标记为证据不足的句子仅修正语法错误，不得进行风格强化或措辞润色——避免将无证据支撑的主张打磨得更有说服力。

## 任务模式

1. **prose-quality-gate** — 执行通用 prose 质量检查与改写
2. **method-prose-rewrite** — Method 专项正文化（问题→设计→机制→收益/边界）
3. **de-ai-pass** — 仅执行去AI化改写
4. **claim-strength-audit** — 审计并调整 claims 强度

## 工作流

### Step 1: 确认当前 section 类型与改写目标

明确是 Introduction / Related Work / Method / Experiments / Discussion / Conclusion。不同 section 有不同的 prose 检查重点。

### Step 2: 执行通用 Prose Quality Gate

**通用检查项：**
- 正文是否仍以提纲句、说明句为主，而非完整 prose 段落
- 是否存在元评论口吻、审稿人对话口吻或代码讲解口吻
- 是否符合去AI化规范（详见 `references/de-ai-patterns.md`）

**章节专项检查项：**
- Introduction / Related Work：是否只有列举，缺少论证链、综合比较或 work-cluster 叙事
- Method：是否仍停留在公式罗列或模块说明，缺少"问题 → 设计 → 机制 → 收益/边界"叙事
- Experimental Setup / Data：是否只有参数或流程罗列，缺少协议、约束与风险说明
- Discussion / Limitations / Conclusion：是否只有泛泛结论，缺少边界分析、失败模式或限制讨论

输出：`prose_debt: open|closed`、`failed_items: [list]`

### Step 3: Prose Rewrite（若 prose_debt 为 open）

- 将提纲式句子改为完整论证段落
- 将元评论、说明文和代码导览口吻改写为学术 prose
- 将罗列式段落改为具有论证链和段内逻辑衔接的连贯段落
- 执行去AI化改写（参考 `references/de-ai-patterns.md`）

Prose Quality Gate + Rewrite 循环最多 2 轮。2 轮后仍未通过，保留 prose_debt: open，允许继续后续步骤但最终 Verification 不得判为 passed。

### Step 4: Method Prose Rewrite（若当前为 Method section）

详见 `references/method-narrative.md`。

重点检查：
- 是否仍存在公式罗列而缺少"问题 → 设计 → 机制 → 收益/边界"叙事
- 模块段首是否直接落在"该模块解决什么问题"
- 是否仍残留"从实现看""一个合理解释是""当前代码表明"等推断降级不充分的口吻

正文中优先使用以下开头方式：
- "为缓解……问题，本文……"
- "考虑到……，本文采用……"
- "与……相比，该设计……"
- "为使……能够……，我们进一步……"

### Step 5: Claim Strength Audit（强制，非可选）

详见 `references/claim-strength.md`。

**零容忍触发词规则**：以下词汇在正文中出现时，必须立即检查是否满足 Strong 条件。若不满足，**强制降级**，不得保留原表述：

| 触发词 | 必须附带的证据 | 不满足时的降级 |
|--------|--------------|--------------|
| "显著(地)" / "significantly" | p 值 < 0.05 或效应量 / 置信区间 | 删除或改为具体数值差异 |
| "稳定(的)" / "robust" / "stable" | 多随机种子 / 交叉验证 / 外部测试集 | 改为"在观察到的...中一致" |
| "作为" / "acts as" / "serves as" | 因果干预实验或领域共识文献 | 改为"可能作为...候选" |
| "表明" / "demonstrates" | Strong 条件全部满足 | 改为"提示" / "与...一致" |
| "泛化" / "generalization" | 独立测试集或多数据集验证 | 改为"在...数据集上" |
| "SOTA" / "state-of-the-art" | 完整基线对比 + 独立测试集 | 改为"与当前比较范围相比..." |

| 强度 | 条件 | 典型表达 |
|------|------|---------|
| Strong | 本地可复核 + 无协议缺陷 | show, demonstrate, outperform |
| Medium | 内部验证 / baseline 不全 | suggest, indicate, appears to improve |
| Weak | 仅 user_claim / 无法复核 | may, could, requires further validation |

必须主动降级不匹配的 claims。把内部验证包装成外部泛化 → 必须降级。把缺失 baseline 的结果写成 SOTA → 必须降级。

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

## Agent 资源与调用方式

### 调用方式

本 Skill 支持两种调用方式：

1. **内化调用**（由 `academic-paper-writer` 在 Step 6.6 使用）：主 Agent 读取本 SKILL.md 及 references/ 下的规则文件后自行执行润色与 claim 强度审计，不 dispatch 独立子 Agent。这确保叙事风格与全文一致，避免上下文传递损失。
2. **独立使用**：用户直接要求润色、去AI化、claim 强度审计时，本 Skill 独立执行。

### 入口分流

| 用户请求特征 | 匹配模式 | 优先级 | 行为 |
|------------|---------|--------|------|
| "润色一下"、"改改语言" | prose-quality-gate | 2（模糊匹配） | 通用 Prose Quality Gate 检查 + 改写，最多 2 轮 |
| "去掉 AI 味"、"不像人类写的" | de-ai-pass | 2（模糊匹配） | 仅去 AI 化改写（AI 连接词、句式调整） |
| "claim 太强了"、"降级结论" | claim-strength-audit | 2（模糊匹配） | 审计所有 claim 强度，零容忍词检查 |
| "改写 Method"、"Method 写得太潦草" | method-prose-rewrite | 2（模糊匹配） | Method 专项叙事：问题→设计→机制→收益/边界 |
| 指定具体模式名称 | 按指定 | 1（用户显式指定） | 忽略自动推断，按指定模式执行 |

### 独立使用时的约束

- **此 Skill 只修改论文草稿文本，绝对不得修改项目源代码、配置文件或数据文件**
- **不得独立撰写整节论文**

## 何时读取 references/

| Reference 文件 | 打开条件 |
|---------------|---------|
| `references/de-ai-patterns.md` | 执行去AI化改写、Prose Quality Gate 通用检查时 |
| `references/claim-strength.md` | 执行 Claim Strength Audit、overclaim 检查或学术风格检查时 |
| `references/method-narrative.md` | 当前为 Method section、执行 Method Prose Rewrite 时 |
| `references/section-moves.md` | 需要按节类型获取 move order、phrase families 或过渡表达参考时 |
| `references/phrasebank-playbook.md` | 需要证据强度用词替换、过渡词族、gap/limitation/implication 短语参考时 |

## 不适用场景

本 Skill 不适用于：
- 非学术文体的通用文本润色
- 已有明确 LaTeX 格式且不需内容修改的场景
- 内容补全（如补实验数据、补引用）——应使用 `academic-experiments` 或 `academic-citation`

## Anti-Patterns

| 模式 | 问题 | 正确做法 |
|------|------|---------|
| 表面润色 | 只改措辞不改 evidence gap | claim 强度必须与证据匹配，无证据时保留占位符 |
| AI 典型用词 | "delve into"、"crucial"、"notably" 过度使用 | 使用领域特定词汇，替换空洞修饰词 |
| 方法缩写 | Method 只写概述不写核心细节 | 核心模块需展开：瓶颈→设计选择→机制→公式→收益→代价 |
| 强词夺理 | 无数据时仍用"显著提升"等强表述 | 降级语气，用保守表述或占位符 |
