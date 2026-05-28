# 迭代控制指南

## 节级迭代闭环

当前 section 的最小闭环：

```
Draft v1 → Placeholder Audit → Evidence Compliance Review → Prose Quality Gate → Expansion Pass → Self-Review → Revised Draft v2 → Verification
```

## 退出条件

只有在以下情况之一成立时，才允许退出当前 section：

- **Verification 判定为 `passed`**：所有 debt（citation/protocol/result/rationale/prose）均已闭合，thin_draft 为 no
- **Verification 判定为 `blocked` 且 `safe_to_continue = yes`**：阻塞问题来自外部证据缺失，已冻结相关 claims，继续其他 section 不会放大幻觉风险
- **用户明确要求暂停**

## 不退出条件

以下情况保持当前 section 为活跃项，继续下一轮修订：

- **Verification 判定为 `failed` 且失败原因不是外部阻塞**：问题可通过继续改写解决，必须继续下一轮 Self-Review → Revision → Verification
- **Verification 判定为 `blocked` 且 `safe_to_continue = no`**：后续 section 会依赖未闭合 claim，必须等待外部证据

## 修订轮次

- 简单草稿：至少 1 轮审查
- 完整论文草稿：优先做 2 轮以上，其中至少含 1 轮扩写和 1 轮批判性修订
- 证据链复杂、实验风险高或目标 venue 较严：直到主要问题被显式处理后再停

## 轮次上限

- 单节内部 Draft→Verification 闭环最多执行 **3 轮**
- 3 轮后仍未通过 Verification → 冻结所有未闭合 claims，标记 `verdict: escalated`，报告用户决策
- 用户可选择：继续修订 / 接受当前版本（含已知缺口） / 跳过本节
- Prose Quality Gate 子循环上限为 **2 轮**，详见 Step 6.6 规则

## 跨章节整合（依赖感知）

参见 `references/section-dependency-matrix.md` 中的矩阵定义。

每完成一个 section 后，按矩阵执行依赖检查（编排器 Step 7b）：
- 当前 section 的 `depended_by` 列表中有哪些已完成 section
- 这些 section 是否因 `shared_claims` 变更而需要回修
- 若需回修，将对应 section 标记 `pending` 并询问使用者

此外，每完成 2-3 个 section，做一次轻量 integration pass：
- 术语是否一致
- 符号是否统一
- 贡献点口径是否前后一致
- 结论口气是否与当前累积证据匹配
