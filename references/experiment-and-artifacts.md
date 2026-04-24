# 本地实验复核与证据产物指南

## 目录

- 使用定位
- 证据优先级
- 先做证据盘点
- 运行策略
- 运行记录格式
- 写结果时的约束
- 常见错误
- 失败处理

## 使用定位

当用户提供代码仓库、checkpoint、日志、图表、CSV 指标文件或实验脚本时，读取本文件。

目标不是“尽量多跑实验”，而是建立最短且可信的证据链。

---

## 1. 证据优先级

按可靠性从高到低区分三类：

1. `newly_run`
   - 当前会话中执行并记录了命令与输出
2. `preexisting_artifact`
   - 仓库中已存在的 checkpoint、日志、CSV、图表、表格，经检查后确认来源和含义
3. `user_claim`
   - 仅来自用户口述或旧草稿叙述，尚未本地复核

规则：

- 正文中的定量结果优先来自 `newly_run`。
- 若无法重跑，可使用 `preexisting_artifact`，但必须标注其来源与限制。
- `user_claim` 只能写成待核验信息，不能当作最终结果。

---

## 2. 先做证据盘点

在跑命令前，先盘点：

- `config.*`
- `main.*` / `train.*` / `eval.*`
- `run_*.sh` / `run_*.ps1`
- `requirements.txt` / `environment.yml` / conda 路径线索
- `checkpoints/`
- `logs/` / `outputs/` / `results/`
- 图表、CSV 指标文件、先前论文草稿

目标是回答四个问题：

1. 能否只评估已有 checkpoint，而无需重训？
2. 已有结果是窗口级、样本级还是受试者级？
3. 当前 split 协议是否可靠？
4. 哪些结果可以在合理时间内复核？

---

## 3. 运行策略

默认顺序：

1. 先验证环境是否可用
2. 再定位最小可复核命令
3. 先跑评估或解释脚本
4. 只有在确有必要时才重训

这比“一上来就 full training”更理性，也更符合论文取证需求。

优先动作示例：

- 评估现有 `best_model.pth`
- 运行解释脚本验证图表来源
- 复核单个 split 的指标计算流程
- 检查 subject-level 与 file-level 划分差异

---

## 4. 运行记录格式

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

其中 `Protocol Risks` 不能省略，尤其要主动记录：

- 数据泄漏风险
- 验证集调参
- baseline 缺失
- 没有独立测试集
- 只有单次运行、没有方差

---

## 5. 写结果时的约束

写 Results / Experiments 时，遵守以下规则：

- 先写协议，再写指标。
- 先交代 split 和 aggregation level，再给数字。
- 如果结果来自旧 artifact，要写清“来自现有 checkpoint / 现有输出文件”。
- 如果结果只支持内部验证，就写成 internal validation，不要升级成 generalization claim。
- 如果发现协议有缺陷，应主动把这件事写入 `Discussion / Limitations`。

---

## 6. 常见错误

以下行为会破坏证据链：

- 没区分重跑结果和仓库自带结果
- 没核对指标定义就把数字抄进论文
- 把 file-level split 写成 subject-level split
- 把验证集调阈值后的结果写成最终测试性能
- 只看到图，却不知道图对应哪个脚本和哪个 checkpoint

---

## 7. 失败处理

若代码无法运行：

- 报告具体阻塞点
- 记录已尝试命令
- 标出缺失环境、缺失数据、缺失依赖或超长运行成本
- 将结果节降级为“已知证据 + 待复核项”

不要因为运行受阻，就把旧草稿中的数字重新包装成已验证结果。
