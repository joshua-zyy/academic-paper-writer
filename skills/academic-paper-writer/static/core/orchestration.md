# Orchestration Control

## Push Modes

| Mode | Behavior |
|---|---|
| `auto`（默认） | Verification 通过后自动推进到下一节，不暂停等确认。对话中仅输出简短进度摘要 |
| `step-by-step` | 每节完成后暂停，等待用户确认后再推进 |

- 用户可在启动时指定模式，也可在过程中随时切换
- Step 1 的 venue/language 确认为一次性操作，确认后全程不再重复询问

## Hard Gates (A-E)

以下门控是不可跳过的完整性检查关卡。任一未通过不得进入下一阶段。详细条件和失败处理见 `references/orchestration-workflow.md`。

| Gate | 触发位置 | 核心条件 | 失败处理 |
|------|---------|---------|---------|
| E: Venue 调研 | Step 1 → Step 5 | 若用户提供本地 PDF 文献库，必须先完成 Step 2 并验证 MD 目录；venue 确认后必须完成 Step 4，生成 venue-brief.md | 阻塞，不得进入 Step 5 |
| A: 证据完备 | Step 5 → Step 9 | 至少一条可引用证据（`newly_run`/`preexisting_artifact`） | 降级路径或阻塞 |
| B: 当前节引用就绪 | Step 6 → Step 9 | 当前 section 的关键 claims 有 VERIFIED 引用、Citation-to-Claim Map 或显式 `[REF_NEEDED]` 占位 | 按 section 分流，Intro/RW 阻塞，Method/Results 可带占位进入但必须记录 debt |
| C: Verification | Step 9.8 → Step 10 | 所有硬 debt 闭合 + thin_draft = no（figure_debt 为软发布债务，open 时不单独阻止当前 section passed） | passed/blocked/failed，详细见 workflow |
| D: 全文引用数量 | Step 11 → 输出 | 全文去重后引用总数 >= `min_citations` | 未达标时提醒用户，可继续补充后重检 |

## 9.1 Pre-Draft Probe Rules

起草前根据当前 section 类型 dispatch 深层探查。需要探查 → **必须先 dispatch 再起草**，不得跳过。

| 当前 section | 需 dispatch 的探查 | 并行策略 |
|-------------|-------------------|---------|
| Introduction | `existing_material`（项目已有材料）+ 本地文献深度探索 + 外部文献定向搜索 | **必须并行**（同时发出 3 个 Task） |
| Related Work | `existing_material`（项目已有材料）+ 本地文献深度探索 + 外部文献定向搜索 | **必须并行**（同时发出 3 个 Task） |
| Method | `code_structure`（Module Cards + 张量形状 + forward 路径）+ `preprocessing`（预处理步骤） | **必须并行** |
| Experimental Setup | `experiment_setup`（超参数、数据集划分、人口统计） | 单探查 |
| Main Results / Ablation | `experiment_results`（主结果、基线对比、消融数值） | 单探查 |
| Discussion | `interpretability`（可解释性结果、网络分析） | 单探查 |

Dispatch 模板见 `references/workflow-step-0-7.md` 和 `references/workflow-step-8-9.5.md`。

## Default Section Queue

Abstract 为后置章节，不在初始队列中。默认顺序：Introduction → Related Work → Method → Experimental Setup → Results → Discussion → Conclusion → Abstract。详见 `references/paper-structure.md`。

## Decision Points

在关键节点展示阶段性成果。`auto` 模式仅输出简短摘要不暂停；`step-by-step` 模式暂停等待确认。

| DP | 位置 | Agent 展示 |
|----|------|-----------|
| DP-1 | Step 4 完成后 | Venue Brief 摘要（venue、语言、min_citations） |
| DP-2 | Step 8 Blueprint 完成后 | Section Blueprint（章节结构、每节要点、证据来源） |
| DP-3 | Step 9.2 Draft v1 完成后 | Draft 摘要（当前节、段落数、待补充清单） |
| DP-4 | Step 9.8 Verification 完成后 | Verification Status（verdict、未闭合问题） |

## File Output Rules

1. **输出目录**：`./academic-paper-writer/paper-drafts/`
2. **论文文件**：`paper_draft.md` — 正文 + 参考文献 + 待补项，逐步追加
3. **Blueprint文件**：`section_blueprint.md` — 每节更新
4. **图片目录**：`figures/` — SVG 数据图输出与手工图表需求记录；`figures/codes/` — `plot_*.py`
5. **对话输出限制**：禁止在对话中输出完整论文正文，仅显示简短进度摘要
6. **写入时机**：每节 Draft 生成后、Verification 完成后使用 Write/Edit 更新 `paper_draft.md`
7. **中间状态**：Evidence Inventory、Verified References、Revision Queue 等在 agent 上下文中维护
8. **Venue Brief**：`venue-brief.md` — Step 4 输出，后续步骤必参考
