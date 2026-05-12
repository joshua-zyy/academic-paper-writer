---
name: "academic-experiments"
description: "Use when auditing, running, or verifying experimental evidence for academic papers — experiment inventory, result verification, protocol risk assessment. Triggers on: 复核实验, run experiments, 实验结果, experiment evidence, verify results, 实验验证."
---

# Academic Experiments

将此 skill 视为"实验取证代理"，目标是建立最短且可信的证据链，而不是尽量多跑实验。

## 非协商规则

- 不编造实验结果、图表、命令或运行日志。
- 区分三类证据：`newly_run`（本轮执行）、`preexisting_artifact`（已有产物）、`user_claim`（用户口述）。只把前两类当作可直接引用的证据。
- `user_claim` 只能写成待核验信息，不能当作最终结果。
- 正文中的定量结果优先来自 `newly_run`。若无法重跑，可用 `preexisting_artifact` 但必须标注来源与限制。
- 不要把"领域里常见的预处理/协议默认值"直接写进正文冒充当前项目事实。
- 不能运行则明确报告阻塞点、已尝试命令和缺失条件，不得伪装成"已验证"。
- 若结果仅为内部验证，明确写成 `internal validation`，不得包装成最终泛化结论或 SOTA 结论。

## 任务模式

1. **experiment-evidence-pass** — 完整实验审计：盘点 + 运行 + 记录 + 风险分析
2. **evidence-inventory-only** — 仅盘点已有实验产物，不执行运行
3. **minimal-reproducible-run** — 执行最小可复核命令（如评估已有 checkpoint）

## 工作流

### Step 1: 证据盘点

在跑命令前，先盘点（详见 `references/evidence-inventory.md`）：

- 配置文件（config.*）
- 入口脚本（main.* / train.* / eval.*）
- 运行脚本（run_*.sh / run_*.ps1）
- 环境文件（requirements.txt / environment.yml）
- Checkpoint 文件
- 日志与输出（logs/ / outputs/ / results/）
- 图表与 CSV 指标文件

回答四个问题：
1. 能否只评估已有 checkpoint，而无需重训？
2. 已有结果是窗口级、样本级还是受试者级？
3. 当前 split 协议是否可靠？
4. 哪些结果可以在合理时间内复核？

### Step 2: 运行策略

默认顺序（详见 `references/run-strategy.md`）：

1. 先验证环境是否可用
2. 再定位最小可复核命令
3. 先跑评估或解释脚本
4. 只有在确有必要时才重训

优先动作示例：
- 评估现有 `best_model.pth`
- 运行解释脚本验证图表来源
- 复核单个 split 的指标计算流程
- 检查 subject-level 与 file-level 划分差异

### Step 3: 记录运行结果

对每个进入论文正文的实验结果，至少记录：

```md
## Experiment Evidence

- Status: newly_run / preexisting_artifact / blocked
- Command: ...
- Workdir: ...
- Environment: ...
- Inputs: ...
- Key Config: ...
- Output Artifacts: ...
- Metrics Used In Draft: ...
- Protocol Risks: ...
```

### Step 4: 协议风险评估

主动记录（详见 `references/protocol-risks.md`）：

- 数据泄漏风险
- 验证集调参
- baseline 缺失
- 没有独立测试集
- 只有单次运行、没有方差
- 把 file-level split 写成 subject-level split
- 把验证集调阈值后的结果写成最终测试性能

### Step 5: 输出

```md
## Experiment Evidence
（按 Step 3 格式逐条记录）

## Protocol Risks
（按 Step 4 逐项列出）

## Results / Setup Draft
（可用实验事实写成的草稿段落，缺证据处用占位符）

## Remaining Blockers
（无法运行的实验、缺失的数据/环境/依赖）
```

## 写结果时的约束

- 先写协议，再写指标
- 先交代 split 和 aggregation level，再给数字
- 如果结果来自旧 artifact，写清"来自现有 checkpoint / 现有输出文件"
- 如果结果只支持内部验证，写成 internal validation，不升级成 generalization claim
- 如果发现协议有缺陷，主动写入 `Discussion / Limitations`
- 对实验协议与预处理细节，区分 `repo/artifact-verified protocol` 与 `domain-typical assumption`

## 失败处理

若代码无法运行：
- 报告具体阻塞点
- 记录已尝试命令
- 标出缺失环境、缺失数据、缺失依赖或超长运行成本
- 将结果节降级为"已知证据 + 待复核项"
- 不要因为运行受阻，就把旧草稿中的数字重新包装成已验证结果
