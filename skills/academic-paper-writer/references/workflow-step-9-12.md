# Orchestration Workflow — Part 3: Review & Integration (Step 9–12)

本文件包含编排器 Step 9–12 的详细执行流程。按需加载，避免一次性加载全部步骤。

完整步骤索引见 `orchestration-workflow.md`。

---

## Step 9: Prose Quality Gate (Phase 2 of Two-Phase Review) — 内化调用

- Create a todo list for prose checks.
- Confirm Step 8 `evidence_debt = closed` before executing.
- **内化调用 `academic-polishing`**：主 Agent 读取 `skills/academic-polishing/SKILL.md` 的规则后自行执行润色与 claim 强度审计，不 dispatch 子 Agent。

**执行方式**：

1. 读取 `skills/academic-polishing/SKILL.md` 及其 references/ 下的相关文件
2. 按 SKILL.md 中的 Step 1-6 执行 Prose Quality Gate
3. 执行 Claim Strength Audit（零容忍触发词规则）
4. 若为 Method 节，执行 Method Prose Rewrite
5. Prose Rewrite 最多 2 轮，2 轮后仍 open 则保留状态继续

**零容忍触发词规则**——出现时必须检查 Strong 条件，不满足则强制降级:
- "显著" / "significantly" → 无 p 值/效应量时必须降级
- "稳定" / "robust" → 无多随机种子/交叉验证时必须降级
- "作为" / "acts as" → 无因果干预实验时必须降级
- "表明" / "demonstrates" → 不满足 Strong 条件时必须降级
- "泛化" / "generalization" → 无独立测试集时必须降级
- "SOTA" / "state-of-the-art" → 无完整基线对比时必须降级

**输出格式**：

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

Input: Draft text (after evidence review), current section type, evidence_debt status.
Output: `prose_debt` (open|closed), `failed_items`, rewritten text. For Method, also `method_prose_debt`.

Prose rewrite loop: max 2 rounds. If still open after 2 rounds, carry `prose_debt: open` forward; final Verification cannot be `passed`.

**内化调用的优势**：
- 主 Agent 保持对叙事风格和术语的完整控制
- 无上下文传递损失
- 润色后的文本与前后节风格一致

## Step 10: Expansion Pass (Content Density Check)

- Create a todo list for thin-draft checks.

Thin-draft conditions（详见 `references/content-density.md`）:
- Introduction <= 2 paragraphs, or only background + contribution list
- Related Work is just paper name listing, no work clusters or synthesis
- Method is only overview, no module breakdown or formulas
- Experimental Setup is only parameter listing, no protocol or risk notes
- Discussion / Conclusion is only generic statements, no boundary analysis

Expansion principle: use only existing evidence and compliant placeholders. Prioritize filling "reader understanding chain" gaps.

## Step 11: Self-Review & Verification

- Create a todo list for review items.
- Delegate to `academic-reviser` via the dispatch template below（full-section-review mode）.
- Check verdict and decide whether to advance or revise.

**Dispatch template：**
```yaml
Task:
  description: "综合验证 - {section}"
  subagent_type: "general"
  prompt: |
    你已加载 academic-reviser 子 Skill（skills/academic-reviser/SKILL.md）。

    任务: 对 {section} 执行完整三轮审查 + Verification（full-section-review）
    Draft: <传入 Expanded Draft>
    Evidence Map: <传入证据清单>
    prose_debt: {prose_debt}
    thin_draft: {thin_draft}
    frozen_claims: {frozen_claims}
    iteration_count: {iteration_count}

    执行步骤:
    1. 读取 skills/academic-reviser/SKILL.md，按 Step 1-6 执行
    2. 第一轮——证据与事实检查（13 项）
    3. 第二轮——论证强度与审稿风险检查（11 项）
    4. 第三轮——结构与风格检查（8 项）
    5. 生成 Revised Draft（必须真正吸收修改点）
    6. 输出 Section Critique + Verification Status

    Verification 判定规则（Gate C strict 模式）:
    - verdict = passed 仅当 prose_debt=closed 且 citation_debt=closed 且 evidence_debt=closed 且 figure_debt=closed 且 thin_draft=no
    - 任何 debt 未闭合 → verdict = blocked（禁止伪装为 passed）
    - blocked 时输出 safe_to_continue + frozen_claims

    输出的 Section Critique 必须明确:
    - 本节已解决的问题
    - 本节仍缺的证据
    - 剩余占位符统计
    - 下一节最合理的候选

    约束: 遵循 academic-reviser SKILL.md 中的 Red Lines

    返回: Section Critique + Revised Draft + Verification Status
```

Input: Expanded Draft, Evidence Map, prior step states (`prose_debt`, `thin_draft`, `frozen_claims`, etc.).
Output: Self-Review, Revised Draft vN (must absorb fixes), Section Critique, Verification Status (`passed`/`failed`/`blocked`) per `academic-reviser/references/schemas/verification-report.md`.

If `blocked`, must include `safe_to_continue` and `frozen_claims`. Only advance if `safe_to_continue = yes`.

### 文件更新（强制）

Revised Draft 生成后，**必须**将更新后的正文写入 `./docs/paper-drafts/paper_draft.md`（Edit 工具替换对应节内容）。

**禁止在对话中输出完整 Revised Draft 正文。** 对话中仅输出进度摘要。

## Step 12: Integration & Section Loop (Dependency-Aware)

For `full-paper-planning`, do not end after one section revision.

### 12a. Status Update

- If `failed` and not externally blocked → keep current section active, continue next Step 11 round.
- If `blocked` and `safe_to_continue = yes` → write blockers to Revision Queue, freeze claims, advance.
- If `blocked` and `safe_to_continue = no` → keep active, wait for external evidence.
- Merge into Cumulative Draft; update Section Queue and Revision Queue.

### 12b. Dependency Check

After current section passes Verification, read `references/section-dependency-matrix.md`:

1. Read current section's `depended_by` list.
2. Check which sections in that list are already completed (exist in Cumulative Draft).
3. Check if `shared_claims` changed (compare original Evidence Map vs current draft).
4. If changed → mark corresponding section's `revision_queue` status as `pending`.
5. Dependency handling by continuation mode:
   - **auto 模式**（默认）：自动处理依赖。若 `shared_claims` 变更，将对应 section 标记 `revision_queue: pending`，自动推进时优先处理。仅在 `safe_to_continue = no` 时暂停询问用户。
   - **step-by-step 模式**：询问用户："本节改变了 X (claim)，是否先回修 Y 节？"
     - User confirms → move Y to head of Section Queue.
     - User skips → Y keeps `pending`, auto-rechecked when Y is completed later.

### 12c. Select Next Section and Advance

Choose from sections whose `depends_on` are all satisfied and `revision_queue` has no `pending`:

Priority:
1. All `depends_on` completed
2. No `pending` recheck markers among them
3. User-specified section

**Continuation mode behavior**:
- **auto 模式**（默认）：自动选择下一节，直接开始起草，**不暂停等待用户确认**
- **step-by-step 模式**：选择下一节后暂停，等待用户确认后再推进

Continue until:
- Core sections have substantial drafts
- Blocking evidence gaps would significantly increase hallucination risk
- User explicitly requests pause

### 12d. Abstract Generation (Hard Gate D)

Abstract is **not** in the initial Section Queue. It can only be generated after **all** of the following conditions are met:

1. All core sections (Introduction / Related Work / Method / Experiments / Discussion / Conclusion) are completed in Cumulative Draft
2. Each core section's Verification Status = `passed` (`blocked` is insufficient)
3. Main experimental results are stable (`evidence_debt = closed`)

If conditions are not met, retain `[ABSTRACT_NEEDED: 待主要证据稳定后撰写]` in the placeholder system. Do **not** output a complete Abstract.

When generating Abstract:
- It must reflect the actual content of the Cumulative Draft
- Any numerical results must be verified (`newly_run` or `preexisting_artifact`)
- Do not introduce new claims, methods, or terminology not present in the body
- Place Abstract at the beginning of the final Cumulative Draft output

### 12e. External Citation Checklist Generation（**强制**，全文完成后执行）

Abstract 生成后、输出最终 Cumulative Draft 之前，**必须**生成引用文献清单。未生成清单不得输出最终稿。

**触发条件**：
- Abstract 已生成（隐含所有 core sections Verification = passed）
- 本轮尚未生成过引用清单

**执行流程**：

1. 从 Cumulative Draft 中提取所有引用的外部文献条目
2. 为每篇文献记录：标题、作者、venue、引用章节、引用目的
3. **必须**写入 `./docs/paper-drafts/referenced-literature-checklist.md`

**输出模板**：
```markdown
# 引用文献清单

以下文献在论文中被引用。请逐篇下载到本地，agent 可帮助确认引用是否合理。

| # | 文献 | 引用章节 | 引用目的 | 本地确认状态 |
|---|------|---------|---------|------------|
| 1 | Author et al., "Title", Venue 2024 | Introduction | 背景事实 | ⬜ |
| 2 | Author et al., "Title2", NeurIPS 2023 | Method | 基线比较 | ⬜ |

## 确认方式

1. 将上述文献的 PDF 放入本地文献库目录
2. 运行转换命令：
   ```
   python skills/academic-citation/scripts/convert-pdfs-to-md.py <pdf_dir> <papersToMd_dir>
   ```
3. 告知 agent："确认引用"
4. Agent 将 dispatch literature-reader-agent 逐篇阅读，
   对比论文实际内容与 draft 中的引用描述是否一致
5. 每篇输出的确认结果：
   - ✅ **accurate** — 引用准确，描述与原文一致
   - ⚠️ **needs_downgrade** — 引用略有偏差，需降级描述
   - ❌ **incorrect** — 引用不准确，建议删除或重写

## 已确认清单

（逐步更新，每确认一篇更新一行）
```

**执行顺序约束**：12e 完成后，才可执行 12g (Progress Report) 和 12h (File Update)。

### 12g. Progress Report（auto 模式下每节完成后输出）

每节 Verification 完成后，在对话中输出简短进度摘要：

> **{Section}**: {verdict} → Next: {next_section}
> {如有关键问题，最多 1-2 条；否则省略}

此摘要**替代**完整正文的对话输出。完整内容仅在 `./docs/paper-drafts/paper_draft.md` 中可查阅。

### 12h. File Update（强制）

每节 Verification 完成后，**必须**使用 Edit 工具更新 `./docs/paper-drafts/paper_draft.md`，将当前节的最新版本追加或替换到论文文件中。

---

## Shared Inputs and References

Cross-skill data contracts, shared concept references, and reference-loading guidance are maintained in `skills/academic-paper-writer/SKILL.md` as the high-level orchestrator index.

When executing a concrete step in this file:
- read the referenced schema under the relevant sub-skill's `references/schemas/` if the step consumes or produces structured cross-skill data
- read the referenced file under `references/` when that step explicitly calls for it
