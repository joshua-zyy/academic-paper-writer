# Example Usage — 端到端使用场景

## 场景 1: full-paper-planning — 从研究概要启动完整论文

**用户输入**：
> 我有一个基于双分支 Transformer 的 EEG 情绪识别项目，代码在 `./eeg-emotion/`，想用这个仓库写一篇完整论文投到 IEEE T-AFFC。

**执行流程摘要**：
```
Step 0: mode=full-paper-planning, scope=empirical CS/AI paper
Step 1: Venue Brief → IEEE T-AFFC, 英文, 双栏, 12页
Step 2: 并行 dispatch probe agents 探查代码/数据/配置
Step 3: 并行 dispatch citation agent + literature reader → Verified References (12篇本地+8篇外部)
Step 4: dispatch experiment agent → Evidence Inventory (3个newly_run结果, 2个preexisting_artifact)
Step 5: Section Blueprint → 8节结构 + 每节要点
Step 6: Draft v1 (Introduction) → 5段完整prose + 待补项清单
Step 7: arch-prompt 生成架构图提示词
Step 8: evidence compliance review → evidence_debt: closed
Step 9: prose quality gate → prose_debt: closed
Step 10: expansion pass → thin_draft: no
Step 11: verification → Verdict: passed, Score: 8/10
Step 12: 推进到 Related Work...
```

**对话输出**（auto 模式）：
> ✅ Introduction 完成 | Verdict: passed | Score: 8/10 | 下一节: Related Work

---

## 场景 2: section-drafting — 聚焦单节起草

**用户输入**：
> 帮我写 Method 节，代码在 `./model/`，重点讲清楚双分支架构和注意力机制。

**执行流程摘要**：
```
Step 0: mode=section-drafting, section=Method
Step 2: probe agent 探查代码 → 识别核心模块 (TemporalBranch, SpatialBranch, FusionModule)
Step 3: 文献检索 → 相关 attention 机制文献 (6篇VERIFIED)
Step 5: Blueprint → 整体框架 → 模块拆解 → 训练目标
Step 6: Draft v1 → 完整prose + [FIGURE_NEEDED: overall architecture] + 待补项清单
Step 7: arch-prompt 生成分支架构图提示词
Step 8-11: 审查闭环 → Verdict: passed
```

**输出片段**（Draft v1 Method 开头）：
> The proposed dual-branch Transformer architecture processes EEG signals through
> parallel temporal and spatial pathways... [后续展开模块细节]

---

## 场景 3: section-revision — 修订已有草稿

**用户输入**：
> 这是我的 Related Work 草稿，帮我审查修订：[粘贴草稿文本]

**执行流程摘要**：
```
Step 0: mode=section-revision, section=Related Work
Step 8: evidence compliance review → 发现3处裸claim无citation
Step 9: prose quality gate → prose_debt: open (罗列式段落)
Step 10: expansion pass → 补充work cluster综合比较
Step 11: verification → Verdict: passed, Score: 7/10
```

**输出**（Section Critique 摘要）：
> - Issues fixed: 补充3处inline citation, 将罗列式段落重组为2个work clusters
> - Claims weakened: "outperforms all existing methods" → "achieves competitive results"
> - Evidence still missing: [REF_NEEDED: recent GNN-based EEG methods]
