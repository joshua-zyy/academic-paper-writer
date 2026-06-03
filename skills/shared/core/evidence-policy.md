# 证据策略（Evidence Policy）

本文件定义 academic skill suite 的跨 skill 证据语义。

## 证据类型

| Type | 含义 | 是否可支撑论文 claim |
|---|---|---|
| `newly_run` | 当前工作会话中实际运行命令产生的证据 | yes |
| `preexisting_artifact` | 已存在的本地产物，例如 logs、CSV files、checkpoints、tables 或此前已验证输出 | yes，但必须记录来源和限制 |
| `user_claim` | 用户提供但 agent 未独立检查的陈述 | no |

## 规则

1. 只有记录了 source path、command 或 provenance 的 `newly_run` 与 `preexisting_artifact` 才能作为可用证据。
2. `user_claim` 只能作为调查上下文，不是已验证证据。
3. 对缺少支撑的 claim，应弱化、冻结或标记为 unsupported，不得让它听起来更确定。
4. 缺少证据时保留 placeholder；只有真实证据替代后才能删除 placeholder。

## 占位符系统（Placeholder System）

缺少证据时使用显式 placeholder，不得编造内容或删除缺口：

| Placeholder | 用途 |
|---|---|
| `[REF_NEEDED: claim/topic]` | 缺少文献支撑 |
| `[FIGURE_NEEDED: purpose \| placement \| why]` | 缺少图表 |
| `[TABLE_NEEDED: purpose \| columns \| why]` | 缺少表格 |
| `[RESULT_NEEDED: experiment/metric/source]` | 缺少实验结果 |
| `[RESULT_UNVERIFIED: claim \| why]` | 结果尚未验证 |
| `[METHOD_DETAIL_NEEDED: description]` | 缺少方法细节 |
| `[RATIONALE_NEEDED: module \| missing]` | 缺少设计动机 |
| `[DATASET_DETAIL_NEEDED: description]` | 缺少数据集细节 |
| `[ABSTRACT_NEEDED: reason]` | Abstract 延后撰写 |
