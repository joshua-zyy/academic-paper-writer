# 共享概念与边界规则

本目录包含跨技能共享的概念定义、边界规则和术语参考。

## 证据分类

详见 `schemas/evidence-inventory.md` 中的三类证据定义：
- `newly_run`：本轮 session 中实际运行产生的证据
- `preexisting_artifact`：仓库中已有但非本轮运行的证据
- `user_claim`：用户口述但未提供可复核产物

## 占位符系统

| 占位符 | 用途 |
|--------|------|
| `[REF_NEEDED: claim/topic]` | 缺少文献支撑 |
| `[FIGURE_NEEDED: purpose \| placement \| why]` | 缺少图表 |
| `[TABLE_NEEDED: purpose \| columns \| why]` | 缺少表格 |
| `[RESULT_NEEDED: experiment/metric/source]` | 缺少实验结果 |
| `[RESULT_UNVERIFIED: claim \| why]` | 结果未核验 |
| `[METHOD_DETAIL_NEEDED: description]` | 缺少方法细节 |
| `[RATIONALE_NEEDED: module \| missing]` | 缺少设计理由 |
| `[DATASET_DETAIL_NEEDED: description]` | 缺少数据集细节 |
| `[ABSTRACT_NEEDED: reason]` | Abstract 后置占位 |

## Claim 强度等级

| 强度 | 条件 | 典型表达 |
|------|------|---------|
| Strong | 本地可复核 + 无协议缺陷 | show, demonstrate, outperform |
| Medium | 内部验证 / baseline 不全 | suggest, indicate, appears to improve |
| Weak | 仅 user_claim / 无法复核 | may, could, requires further validation |

## Verification 判定

| Verdict | 含义 | 退出条件 |
|---------|------|---------|
| passed | 所有硬 debt 闭合，thin_draft = no | 可推进下一节 |
| failed | 问题可通过继续修订解决 | 继续修订 |
| blocked | 需要外部证据 | safe_to_continue 决定是否推进 |
