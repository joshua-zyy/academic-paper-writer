# CS/AI/ML 论文报告规范 Checklist

本 checklist 定义 CS/AI/ML 实证论文必须报告的项目。在 Step 6.5（证据合规审查）和 Step 6.8（Verification）中按类别逐项检查。

## 计算资源 (Computational Resources)

- [ ] GPU/TPU 型号和数量
- [ ] 训练总时长（GPU-hours 或 wall-clock time）
- [ ] 内存/显存峰值使用
- [ ] 推理延迟（如适用，含 batch size 和硬件配置）

## 可复现性 (Reproducibility)

- [ ] 随机种子数量及设置方式（单种子/多种子/种子范围）
- [ ] 代码开源链接（或匿名链接用于双盲评审）
- [ ] 环境配置（Python/CUDA/框架版本，或 Docker/conda 环境文件）
- [ ] 数据集获取方式（公开数据集名称+链接，或私有数据描述）

## 实验设计 (Experimental Design)

- [ ] 交叉验证方式（k-fold / hold-out / leave-one-subject-out / 固定划分）
- [ ] 超参数搜索范围和方法（grid / random / Bayesian / 手动）
- [ ] 早停策略（patience、monitor metric、验证集比例）
- [ ] 数据增强方法（如使用，需列出具体增强操作和概率）

## 基线比较 (Baseline Comparison)

- [ ] 每个基线的实现来源（官方代码 / 自行复现 / 文献报告值）
- [ ] 是否在相同数据和协议下比较（相同 train/val/test split、相同预处理）
- [ ] 基线超参数是否经过调优（而非使用默认参数）
- [ ] 是否包含近期强基线（近 2-3 年同任务 SOTA 或 strong baseline）

## 统计显著性 (Statistical Significance)

- [ ] 是否报告方差或置信区间（多种子运行 / 交叉验证标准差）
- [ ] 统计检验方法（paired t-test / Wilcoxon signed-rank / bootstrap）
- [ ] 显著性水平（p 值阈值，如 p < 0.05）

## 伦理声明 (Ethical Considerations)

- [ ] 数据集使用许可（许可证类型、是否允许商业用途）
- [ ] 隐私保护措施（如涉及人类数据：脱敏、IRB 审批、知情同意）
- [ ] 偏见分析（如适用：不同人口统计子群的性能差异）

## 使用方式

在 `academic-paper-writer` 的 Step 6.5（证据合规审查）中，主 Agent 按此 checklist 逐项检查当前 section 是否覆盖了相关报告项。未覆盖项记录为 `protocol_debt`，在 Verification 中作为评审依据。

在 `academic-reviser` 的 Step 2（证据与事实检查）中，reviser Agent 参照此 checklist 检查实验相关 section 是否遗漏关键报告项。
