---
name: "academic-reviser"
description: "Use when self-reviewing, auditing, or verifying academic paper drafts — structured critique, verification gate, revision loop. Triggers on: 审修, self review, 自查, verification, revise, 修订, check draft."
version: "1.0.0"
status: "stable"
---

# Academic Reviser

将此 skill 视为"挑剔审稿人代理"——像 peer reviewer 一样审查自己的草稿，按证据→论证→风格三轮顺序执行检查，并输出可执行的修订与 Verification 判定。

## Red Lines（绝对禁止）

1. 禁止跳过检查顺序：必须证据→论证→风格，不得先修风格再查事实
2. 禁止输出批评说明后沿用原稿：Revised Draft 必须真正吸收修改点
3. 禁止在 citation debt / protocol debt / result debt / prose debt 未闭合时判为 passed
4. 禁止删除占位符而不补真实内容
5. 禁止因草稿篇幅长就假设它足够可信
6. 禁止用更华丽的写法掩盖内容不足（如 related work 薄用漂亮 prose 包装）

## 非协商规则

1. 代码与方法一致性、实验与表格一致性必须检查。
2. 修订必须针对性修正，保持 evidence-first 原则：不确定的修正用占位符，不臆造。
3. 只有满足终止条件时才能标记为 passed；否则输出"当前最佳版本 + 未闭合问题清单"。
4. 遇到自欺信号（只修措辞不修证据、用长度代替可信度）必须主动标记为 failed。

## 任务模式

1. **full-section-review** — 对单个 section 执行完整三轮审查 + Verification
2. **cross-section-review** — 跨章节一致性检查（摘要 vs 正文 vs 表格 vs 结论）
3. **verification-only** — 仅执行 Verification 判定（不重做自审）
4. **targeted-review** — 针对特定问题做定向审查（如仅检查引用闭合）

## 工作流

### Step 1: 接收当前草稿与前序状态

确认输入：
- 当前 section 的 Draft（经过 Expansion Pass 之后的版本）
- 前序步骤的状态：`prose_debt`、`thin_draft`、`Evidence Map`
- 若来自 core 的委托，还应收到 `safe_to_continue` 和 `frozen_claims`（若适用）

### Step 2: 第一轮 — 证据与事实检查

详见 `references/revision-checklist.md`，逐项检查 13 项事实性问题。

若任一项失败，先修事实，再谈语言。

### Step 3: 第二轮 — 论证强度与审稿风险检查

详见 `references/revision-checklist.md`。从怀疑者视角提问 11 个审稿风险问题。

对这些问题，要么补证据，要么弱化表述，要么把风险显式写出。

### Step 4: 第三轮 — 结构与风格检查

详见 `references/revision-checklist.md`。只有在前两轮基本通过后，才检查 8 个结构/风格项。

注意：不得把语言润色放在事实检查之前。

### Step 5: 生成 Revised Draft

- 真正吸收 Self-Review 中发现的修改点
- 不是"重新生成一遍"，而是针对性修正后输出
- 保持 evidence-first 原则：不确定的修正用占位符

### Step 6: 输出 Section Critique 与 Verification Status

详见 `references/verification-status.md`。

**Section Critique** 明确：
- 本节已解决的问题
- 本节仍缺的证据
- 本节是否仍存在 formula-heavy / rationale-thin / prose debt 问题
- 下一节最合理的候选

**Verification Status** 明确：
- 判定：`passed` / `failed` / `blocked`
- `prose_debt`: open / closed
- `thin_draft`: yes / no
- 本轮实际做了哪些检查
- 仍未闭合的问题属于可继续自修，还是外部阻塞
- 若 blocked：`safe_to_continue: yes|no` 和 `frozen_claims`

**完整输出示例**（passed 场景）：

```md
## Section Critique

- Issues fixed:
  - 补充了 3 处缺失的 inline citation（此前为 [REF_NEEDED: ...]）
  - 降级了 2 处过度表述：将 "outperforms" 改为内部验证表述
  - 在讨论节明确了当前评估受限于单数据集

- Claims weakened or clarified:
  - "Our method achieves SOTA" → "achieves competitive results on the evaluated benchmarks"
  - "demonstrates strong generalization" → "shows promising results on internal validation"

- Evidence still missing:
  - 外部测试集评估结果（[RESULT_NEEDED: external test set evaluation]）
  - 与 [StrongBaseline2024] 的比较（实验排队中）

- Risks to carry into next section:
  - 当前 split 为 file-level，subject-level 泄漏风险需在 Limitations 中讨论

- Missing figure/table/formula placements: none

- Missing or inconsistent inline citations: 已全部闭合

## Verification Status

- Verdict: passed
- prose_debt: closed
- thin_draft: no
- Checks performed:
  - [x] 事实与证据检查（13项）
  - [x] 论证强度与审稿风险检查（11项）
  - [x] 结构与风格检查（8项）
  - [x] 代码与方法一致性检查
  - [x] 引用闭合检查
- Remaining issues:
  - 外部测试集结果待补充（不阻塞继续，已标记 [RESULT_NEEDED]）
- Can move to next section: yes
```

**完整输出示例**（blocked 场景）：

```md
## Section Critique

- Issues fixed:
  - 降级了 3 处强结论，改为中等强度表述

- Claims weakened or clarified:
  - "significantly improves" → "appears to improve"
  - "robust to domain shift" → 改为 [RESULT_NEEDED: domain shift evaluation]

- Evidence still missing:
  - 核心模块 X 的设计动机无法从代码恢复
  - 缺少 baseline Y 的比较结果

- Risks to carry into next section:
  - 当前 results section 依赖未闭合的 [RATIONALE_NEEDED]

## Verification Status

- Verdict: blocked
- prose_debt: closed
- thin_draft: no
- Checks performed:
  - [x] 事实与证据检查（13项）
  - [x] 论证强度与审稿风险检查（11项）
  - [x] 结构与风格检查（8项）
- Remaining issues:
  - [RATIONALE_NEEDED: 模块X设计动机] — 外部阻塞
  - [RESULT_NEEDED: baseline Y comparison] — 外部阻塞
- safe_to_continue: no
- frozen_claims:
  - Claim: "模块X通过机制M缓解了问题P"
    Reason frozen: 设计动机无法从代码恢复，需要作者提供设计文档
    Alternative text: "[RATIONALE_NEEDED: 模块X采用机制M的设计动机 | 预期缓解问题P | 需要作者提供]
    Unfreeze condition: 作者提供模块X的设计文档或会议记录
  - Claim: "方法在 baseline Y 上取得优势"
    Reason frozen: 缺少 baseline Y 的完整比较数据
    Alternative text: "[RESULT_NEEDED: baseline Y comparison | main results table]"
    Unfreeze condition: 完成 baseline Y 实验并获得可复核指标
```

## 何时读取 references/

| Reference 文件 | 打开条件 |
|---------------|---------|
| `references/revision-checklist.md` | 执行三轮审查时（Step 2-4） |
| `references/verification-status.md` | 输出 Verification Status 时（Step 6） |
| `references/common-pitfalls.md` | 自查是否存在自欺行为时 |

## 不适用场景

本 Skill 不适用于：
- 非学术文体的通用文本审查
- 需要领域专家知识才能判断的技术正确性（如特定医学诊断逻辑）
- 仅需拼写/语法检查的场景（应使用 `academic-polishing` 的 de-ai-pass）

## 终止条件

只有以下条件基本满足时，才标记为 passed：
- 关键主张有对应证据
- 主要风险已被显式讨论
- 未核验内容被清楚标记
- 结果、表格、摘要相互一致
- style brief 与正文不冲突（若适用）
- 核心章节不再只是骨架式短稿
- 无未闭合的 citation debt、protocol debt、result debt、prose debt、rationale debt

否则，输出"当前最佳版本 + 未闭合问题清单"。
