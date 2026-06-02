# Experiment Output Contract

## experiment-evidence-pass

```
## Experiment Evidence
（逐条记录：Status, Evidence Type, Command, Workdir, Environment, Inputs, Key Config, Output Artifacts, Metrics Used In Draft, Protocol Risks, Claim Readiness）

## Protocol Risks
（数据泄漏 / 验证集调参 / baseline 缺失 / 无独立测试集 / 单次运行 / 指标定义模糊 / 图表溯源不明）

## Results / Setup Draft
（可用实验事实写成的草稿段落，缺证据处用占位符）

## Remaining Blockers
（无法运行的实验、缺失的数据/环境/依赖）
```

## evidence-inventory-only

- 实验产物清单（不执行任何命令）

## minimal-reproducible-run

- 运行记录 + Evidence Inventory 条目

## Claim Readiness

每个结果标注：`paper_ready` / `weaken_claim` / `blocked` / `author_input_needed`

Schema: `skills/shared/schemas/evidence-inventory.md`
