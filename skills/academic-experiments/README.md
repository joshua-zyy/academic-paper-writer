# Academic Experiments

独立可用的实验证据审计与复核技能。适用于 CS/AI/ML 论文中的实验验证。

## 触发方式

- "帮我复核这个仓库的实验结果"
- "验证 checkpoint 里的指标"
- "盘点实验产物"
- "run experiment evidence pass"

## 核心能力

| 能力 | 说明 |
|------|------|
| 证据盘点 | 遍历 config/checkpoint/log/CSV，建立证据清单 |
| 三级证据分类 | newly_run / preexisting_artifact / user_claim |
| 最小可复核执行 | 优先评估已有 checkpoint，而非长时间重训 |
| 协议风险审计 | 主动记录数据泄漏、验证集调参、基线缺失等风险 |
| 结果约束 | 确保结果表述不超越证据支撑 |

## 与其他 Skill 的关系

- 被 `academic-paper-writer` 在 Step 4（实验事实复核）中委托调用
- 可独立使用于任何需要实验验证的场景
