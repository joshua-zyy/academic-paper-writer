# 运行策略与记录格式

## 运行优先级

默认按以下顺序执行，而非"一上来就 full training"：

1. **验证环境** — 检查 Python/CUDA 版本、依赖是否安装
2. **最小可复核命令** — 评估已有 checkpoint 或解释脚本
3. **评估或解释** — 运行 eval.py 或解释/可视化脚本
4. **重训** — 只有在确有必要时才进行完整训练

## 优先动作

- 评估现有 `best_model.pth`
- 运行解释脚本验证图表来源
- 复核单个 split 的指标计算流程
- 检查 subject-level 与 file-level 划分差异

## 运行记录格式

对每个进入论文正文的实验结果，至少记录：

```md
## Experiment Evidence

- Status: newly_run / preexisting_artifact / blocked
- Command: (实际执行的命令)
- Workdir: (工作目录)
- Environment: (Python 版本、CUDA 版本、关键依赖)
- Inputs: (输入数据、checkpoint 路径)
- Key Config: (关键超参数)
- Output Artifacts: (输出文件路径)
- Metrics Used In Draft: (正文中引用的指标值)
- Protocol Risks: (见 protocol-risks.md)
```

## 常见错误

以下行为会破坏证据链：

- 没区分重跑结果和仓库自带结果
- 没核对指标定义就把数字抄进论文
- 把 file-level split 写成 subject-level split
- 把验证集调阈值后的结果写成最终测试性能
- 只看到图，却不知道图对应哪个脚本和哪个 checkpoint
