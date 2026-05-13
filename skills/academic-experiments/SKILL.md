---
name: academic-experiments
description: "Use when user needs to audit, run, or verify experimental evidence for academic papers. Triggers on: 复核实验, run experiments, 实验结果, experiment evidence, verify results, 实验验证."
---

# Academic Experiments

将此 skill 视为"实验取证代理"，目标是建立最短且可信的证据链，而不是尽量多跑实验。

## Red Lines（绝对禁止）

1. 禁止编造实验结果、图表、命令或运行日志
2. 禁止把 user_claim（用户口述）当作最终结果写入正文
3. 禁止把"领域里常见的预处理/协议默认值"写成当前项目已确认事实
4. 禁止把内部验证包装成外部泛化或 SOTA 结论
5. 禁止因运行受阻就把旧草稿中的数字重新包装成已验证结果
6. 禁止在不知道图表数据来源的情况下将图表结论写进论文

## 非协商规则

1. 区分三类证据：`newly_run`（本轮执行）、`preexisting_artifact`（已有产物）、`user_claim`（用户口述）。只把前两类当作可直接引用的证据。
2. 正文中的定量结果优先来自 `newly_run`。若无法重跑，可用 `preexisting_artifact` 但必须标注来源与限制。
3. 不能运行则明确报告阻塞点、已尝试命令和缺失条件，不得伪装成"已验证"。
4. 先验证环境 → 再跑最小可复核命令（如评估已有 checkpoint） → 只有在确有必要时才重训。不得一上来就 full training。
5. 写结果时先交代 split 和 aggregation level，再给数字。不得跳过协议直接报指标。

## 任务模式

1. **experiment-evidence-pass** — 完整实验审计：盘点 + 运行 + 记录 + 风险分析
2. **evidence-inventory-only** — 仅盘点已有实验产物，不执行运行
3. **minimal-reproducible-run** — 执行最小可复核命令（如评估已有 checkpoint）

## 工作流

### Step 1: 证据盘点

在跑命令前，先盘点（详见 `references/evidence-inventory.md`）：

- 配置文件（config.*）
- 入口脚本（main.* / train.* / eval.*）
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

按优先级顺序执行（详见 `references/run-strategy.md`）：

1. 验证环境是否可用（Python/CUDA 版本、依赖）
2. 定位最小可复核命令（评估已有 checkpoint）
3. 运行评估或解释脚本
4. 只有在确有必要时才重训

### Step 3: 记录运行结果

详见 `references/run-strategy.md`。对每个进入论文正文的实验结果，至少记录：

```md
## Experiment Evidence
- Status: newly_run / preexisting_artifact / blocked
- Command: （实际执行的命令）
- Workdir: （工作目录）
- Environment: （Python/CUDA版本、关键依赖）
- Inputs: （输入数据、checkpoint路径）
- Key Config: （关键超参数）
- Output Artifacts: （输出文件路径）
- Metrics Used In Draft: （正文中引用的指标值）
- Protocol Risks: （见 Step 4）
```

### Step 4: 协议风险评估

主动记录以下风险（详见 `references/protocol-risks.md`）：

| 风险类型 | 检查点 |
|---------|--------|
| 数据泄漏 | 训练/测试划分是否规范 |
| 验证集调参 | 是否用验证集选阈值后报告测试性能 |
| baseline 缺失 | 是否缺少关键对比方法 |
| 无独立测试集 | 是否只有交叉验证或内部划分 |
| 单次运行 | 是否有方差估计 |
| 指标定义模糊 | 指标计算方式是否与标准定义一致 |
| 图表溯源不明 | 图表是否可追溯到对应脚本和 checkpoint |

### Step 5: 输出

输出按 `../shared/schemas/evidence-inventory.md` 中的 Evidence Inventory Schema 组织数据。以下是 Schema 数据的人可读呈现形式：

```md
## Experiment Evidence
- Status: newly_run / preexisting_artifact / blocked
- Command: （实际执行的命令）
- Workdir: （工作目录）
- Environment: （Python/CUDA版本、关键依赖）
- Inputs: （输入数据、checkpoint路径）
- Key Config: （关键超参数）
- Output Artifacts: （输出文件路径）
- Metrics Used In Draft: （正文中引用的指标值）
- Protocol Risks: （见 Step 4）
```

完整输出包含：

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

## 何时读取 references/

| Reference 文件 | 打开条件 |
|---------------|---------|
| `references/evidence-inventory.md` | 执行证据盘点时（Step 1） |
| `references/run-strategy.md` | 规划运行策略和记录结果时（Step 2-3） |
| `references/protocol-risks.md` | 评估协议风险时（Step 4） |

## 输出数据格式

实验结果应按 `../shared/schemas/evidence-inventory.md` 中定义的 Evidence Inventory Schema 组织输出。

## 不适用场景

本 Skill 不适用于：
- 非 CS/AI/ML 领域的实验（如湿实验、临床实验）
- 纯理论论文（无实验产物需要复核）
- 用户明确只需要文献综述的场景

## 失败处理

### 运行失败降级路径

```
运行失败
├─ 环境问题（CUDA/Python/依赖版本）
│  ├─ 报告具体环境检查结果
│  ├─ 提供安装命令建议
│  └─ 用户确认安装 → 重试；拒绝安装 → 降级
├─ 代码不可执行（语法错误/缺失文件）
│  ├─ 检查是否有可用 checkpoint / 日志 / 结果文件
│  ├─ 有可用 artifact → 降级为 preexisting_artifact 评估模式
│  │  └─ 仅执行 Step 1（证据盘点）+ Step 4（协议风险）
│  └─ 无可用 artifact → 降级为 inventory_only
│     └─ 输出 known_facts + missing_blocking，全部结果用 [RESULT_NEEDED]
├─ 运行成本过高（预计 > 30min 或超过用户预期）
│  ├─ 建议执行"有限集评估"（仅评估已有 checkpoint 的最小子集）
│  ├─ 用户确认 → 执行最小化版本
│  └─ 用户拒绝 → 降级为 preexisting_artifact 模式
└─ 任意路径下：
   - 记录已尝试命令
   - 标出缺失环境、缺失数据、缺失依赖
   - 不得因运行受阻而将旧草稿数字重新包装为已验证结果
```

## Anti-Patterns

| 模式 | 问题 | 正确做法 |
|------|------|---------|
| 先跑再想 | 一上来就 full training，不先盘点已有产物 | 先验证环境 → 跑最小可复核命令 → 确有必要才重训 |
| 协议后置 | 跑完才想用什么评估协议 | 写结果前先交代 split 和 aggregation level |
| 证据混淆 | 把 user_claim 和 newly_run 混在一起 | 严格区分三类证据，只有前两类可引用 |
| 伪装运行 | 运行受阻就把旧数字重包为已验证 | 如实报告阻塞点，不得伪造运行结果 |
