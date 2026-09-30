---
name: academic-experiments
description: "为 CS/AI/ML 写作盘点方法、实验配置、已有结果和来源，核对协议描述与材料一致性。默认只读，不要求重跑研究；授权后可重算或执行指定最小命令。用于实验证据、结果来源、协议说明、核对数字、evidence inventory、复核实验或明确授权的实验执行。"
---

# Academic Experiments

读 manifest 与 always_load，按请求范围执行。没有仓库也可读取作者表格、笔记和草稿；不是一律要求 repo_path。

| mode | 行为 |
|---|---|
| evidence-inventory-only | 默认：盘点已给材料，返回事实、来源、冲突、缺口，不执行研究代码 |
| experiment-evidence-pass | 定向核对协议与结果来源；仍只读，除非有明确执行授权 |
| minimal-reproducible-run | 仅执行明确批准的命令与范围，记录真实产物 |

先复用已有证据再补查，不默认评估 checkpoint。重算指标/统计需预先限定授权；新实验、重训、变更协议单独批准。无明确命令/输入/输出边界时先澄清，不由“复核”一词推定执行许可。

输出 `../shared/schemas/evidence-inventory.md`，数字记录单位、样本/受试者粒度、汇总方式、数据划分与来源；未知标明缺项。不返回 Results/Setup 正文，不评价方法学是否优秀，不把未运行写成复现通过。

编排使用 agents/experiment_agent.md；作者独立核对一个指标只交付相应事实与建议，不强制全仓扫描。执行策略按需读 references/run-strategy.md，协议描述读 references/protocol-risks.md。
