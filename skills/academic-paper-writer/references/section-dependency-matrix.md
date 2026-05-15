# Section 依赖矩阵

## 用途

定义 section 之间的前置依赖、后影响（当某节被修订时哪些节需要回检）、共享 claims（两节共同依赖的论点）和 rewrite_trigger（哪些变更会触发本节省略）。编排器在 Step 6.7 执行 section loop 时感知此矩阵，避免跨节一致性问题。

## 矩阵定义

```yaml
sections:
  introduction:
    depends_on: []
    depended_by: [conclusion, abstract]
    shared_claims: ["problem_definition", "contribution_list"]
    evidence_type_required: [user_claim, preexisting_artifact, newly_run]
    rewrite_trigger:
      - paper_type changed
      - contribution_list modified
      - target_venue changed

  related_work:
    depends_on: [introduction]
    depended_by: [method, experimental_setup, discussion]
    shared_claims: ["baseline_refs", "method_family"]
    rewrite_trigger:
      - method_family or core approach changed
      - new strong baseline discovered
      - problem_definition in introduction changed

  method:
    depends_on: [related_work]
    depended_by: [experimental_setup, discussion, conclusion, abstract]
    shared_claims: ["core_mechanism", "design_rationale", "novelty_claim"]
    rewrite_trigger:
      - code or implementation significantly changed
      - core module added or removed
      - design_rationale revised
      - novelty_claim changed

  experimental_setup:
    depends_on: [method]
    depended_by: [main_results, ablation, discussion]
    shared_claims: ["dataset", "protocol", "implementation_details"]

  main_results:
    depends_on: [experimental_setup]
    depended_by: [discussion, conclusion, abstract]
    shared_claims: ["key_metrics", "baseline_comparisons"]
    rewrite_trigger:
      - experimental_setup changed
      - new results available
      - baseline_comparisons updated

  ablation:
    depends_on: [method, main_results]
    depended_by: [discussion]
    shared_claims: ["module_contribution"]

  discussion:
    depends_on: [method, main_results, ablation]
    depended_by: [conclusion]
    shared_claims: ["limitations", "boundary_analysis"]

  conclusion:
    depends_on: [discussion, main_results]
    depended_by: [abstract]
    shared_claims: ["contribution_summary", "future_work"]

  abstract:
    depends_on: [introduction, conclusion, main_results]
    depended_by: []
    shared_claims: ["core_result", "problem_definition"]
    rewrite_trigger:
      - contribution_summary changed
      - core_result changed
      - target_venue changed
```

## 使用规则

### 推进规则

当前 section 完成后（Verification passed 或 safe_to_continue = yes）：

1. 检查 `depended_by` 中的 section 是否在已完成的 section 列表中
2. 若已有，检查 `shared_claims` 是否发生了变更
3. 若有变更，标记对应 section 的 revision_queue 状态为 `pending`
4. 推进到下一 section 时询问使用者："本节改变了 X，是否先回修 Y 节？"

### 选择下一节

优先选择 `depends_on` 全部满足且 revision_queue 中没有 pending 标记的 section。

### 回检触发条件

以下情况需要回检 depended_by 中的 section：
- shared_claims 中的任何一个 claim 被修改
- rewrite_trigger 中的任何条件被激活
- 当前 section 的 evidence map 发生了影响共享 claim 的变化

## 快速参考表

| Section | 前置依赖 | 后影响 | 关键共享 Claims |
|---------|---------|--------|---------------|
| Introduction | 无 | conclusion, abstract | problem_definition, contribution_list |
| Related Work | introduction | method, experimental_setup, discussion | baseline_refs, method_family |
| Method | related_work | experimental_setup, discussion, conclusion, abstract | core_mechanism, design_rationale, novelty_claim |
| Experimental Setup | method | main_results, ablation, discussion | dataset, protocol, implementation_details |
| Main Results | experimental_setup | discussion, conclusion, abstract | key_metrics, baseline_comparisons |
| Ablation | method, main_results | discussion | module_contribution |
| Discussion | method, main_results, ablation | conclusion | limitations, boundary_analysis |
| Conclusion | discussion, main_results | abstract | contribution_summary, future_work |
| Abstract | introduction, conclusion, main_results | 无 | core_result, problem_definition |
