# 数据访问级别

本文件定义的是跨技能协作时的**运行时数据边界约定**，不是当前仓库中已实现的 frontmatter 字段。

## 级别定义

| 级别 | 含义 | 适用范围 |
|------|------|---------|
| `raw` | 可接触原始未处理数据（代码、实验日志、配置文件） | 实验数据生产/核验类技能 |
| `redacted` | 可接触草稿文本和元数据，但不读取原始实验结果 | 文本处理类技能（润色、格式转换） |
| `verified_only` | 只接触已经过核验的数据和结论 | 证据依赖型技能（编排器、审修、引用） |

## 使用规则

- 编排器在向子 Skill 传递上下文时，应保证子 Skill 的实际输入不超出其约定级别
- `raw` → `redacted` → `verified_only` 为递减方向
- 高级别技能委托低级别子 Skill 时，必须先经过 Gate B（引用合规门控）过滤后再传递数据

## 当前项目中的解释方式

- `academic-experiments` 和代码/数据探查类任务可视为 `raw`
- `academic-polishing` 更接近 `redacted`
- `academic-paper-writer`、`academic-citation`、`academic-reviser` 默认按 `verified_only` 处理最终可写入正文的结论

若未来需要把该约束升级为可机器读取的元数据，应先确认所使用的 Skill 规范允许扩展 frontmatter 字段，再统一落地。
