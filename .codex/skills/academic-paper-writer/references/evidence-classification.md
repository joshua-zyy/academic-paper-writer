# 证据分类体系

## 三类证据

| 类型 | 标识 | 含义 | 能否直接引用 |
|------|------|------|------------|
| 本轮执行 | `newly_run` | 在当前 session 中新运行/执行产生的证据 | ✅ 是 |
| 已有产物 | `preexisting_artifact` | 仓库中已有的 checkpoint、日志、结果文件 | ✅ 是（标注来源与限制） |
| 用户口述 | `user_claim` | 用户口头/文字描述但未提供可复核产物 | ❌ 否，只能转化为占位符 |

## 使用规则

1. `newly_run` 优先于 `preexisting_artifact` — 只有无法重跑时才退而求其次
2. `preexisting_artifact` 必须标注：来源路径、产生时间（或版本）、已知限制
3. `user_claim` 在正文中应用占位符形式引用，不得写成确定结论
4. 任何证据被写进正文前必须经过 `verification_status: verified` 阶段
