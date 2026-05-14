# Section-Specific Verification Checklists

本文件为 Gate C（Verification）提供按 section 类型分类的验证检查清单。在 Step 11 Self-Review & Verification 中，根据当前 section 类型加载对应清单逐项检查。

## Introduction

| 编号 | 检查项 | 失败处理 |
|------|--------|---------|
| I-1 | 所有贡献点在后文中有对应内容支撑 | 冻结无对应内容的贡献 claim |
| I-2 | 每篇引用在正文中有对应的 inline citation | 标记 citation_debt |
| I-3 | 问题陈述 → 空白识别 → 本文贡献 逻辑链完整 | 标记 thin_draft |
| I-4 | 背景引用的时效性与权威性匹配 venue 标准 | 记录但不阻塞 |
| I-5 | 无过度宽泛的背景铺垫（如从 AD 流行病学完整讲起） | 标记 prose_debt |

## Related Work

| 编号 | 检查项 | 失败处理 |
|------|--------|---------|
| RW-1 | 方法被划分为有意义的 work clusters 而非简单罗列 | 标记 thin_draft |
| RW-2 | 每个 work cluster 末尾有综合比较或 gap 识别 | 标记 thin_draft |
| RW-3 | 与本文方法最相关的工作单独讨论了方法差异 | 标记 thin_draft |
| RW-4 | 无漏引关键 baseline 或高度相关工作 | 记录但不阻塞 |
| RW-5 | 引用分布平衡，未过度引用单篇或单一团队 | 记录但不阻塞 |

## Method

| 编号 | 检查项 | 失败处理 |
|------|--------|---------|
| M-1 | 每个核心模块有明确的输入/输出描述（含张量维度） | 标记 thin_draft |
| M-2 | 每个非显然设计选择有设计动机交代 | 标记 thin_draft |
| M-3 | 模块之间的数据流有明确说明 | 标记 thin_draft |
| M-4 | 总体架构图已放置或 [FIGURE_NEEDED] 占位已存在 | 标记 figure_debt |
| M-5 | 核心公式正确且与代码/伪代码一致 | 标记 evidence_debt |
| M-6 | 所有符号在第一次使用时被定义 | 标记 prose_debt |
| M-7 | 标准/支撑性组件至少说明了作用与核心操作 | 标记 thin_draft |

## Experiments

| 编号 | 检查项 | 失败处理 |
|------|--------|---------|
| E-1 | 数据集划分细节完整（种子、比例、排除标准） | 标记 evidence_debt |
| E-2 | 所有实验数值可追溯到代码运行结果或 checkpoint | 标记 evidence_debt |
| E-3 | 超参数、训练协议、模型选择标准已报告 | 标记 evidence_debt |
| E-4 | 评价指标定义清楚（如 AUC 是 macro/micro/weighted） | 标记 prose_debt |
| E-5 | 基线方法的实现来源或引用已注明 | 标记 evidence_debt |
| E-6 | 消融实验的设置与控制变量方法已说明 | 标记 evidence_debt |

## Discussion / Limitations

| 编号 | 检查项 | 失败处理 |
|------|--------|---------|
| D-1 | 结果解读与实验数据对齐，无超出数据支持的解释 | 标记 evidence_debt |
| D-2 | 局限性被具体标注而非泛泛而谈 | 标记 thin_draft |
| D-3 | 未来工作方向与具体局限之间有直接映射关系 | 标记 prose_debt |
| D-4 | 神经科学/领域解读附有文献支撑或 [REF_NEEDED] | 标记 citation_debt |

## Conclusion

| 编号 | 检查项 | 失败处理 |
|------|--------|---------|
| C-1 | 结论未引入正文未出现的新主张、新数据 | 标记 evidence_debt |
| C-2 | 主要数值结果与实验节表一致 | 标记 evidence_debt |
| C-3 | 贡献点总结与 Introduction 中的贡献列表对齐 | 标记 prose_debt |
| C-4 | 未来工作与 Discussion 中的局限对齐 | 标记 prose_debt |

## Abstract

| 编号 | 检查项 | 失败处理 |
|------|--------|---------|
| A-1 | 数值结果与正文实验表一致 | 标记 evidence_debt |
| A-2 | 覆盖背景、问题、方法、结果、结论五个要素 | 标记 thin_draft |
| A-3 | 无正文未出现的方法术语或缩写 | 标记 prose_debt |

## 使用方式

在 Step 11 Verification 中，根据 `section` 字段选择对应清单：

```
section_type = "Introduction"     → 加载 Introduction 清单
section_type = "Related Work"     → 加载 Related Work 清单
section_type = "Method"           → 加载 Method 清单
...
```

逐项检查，记录每项 status（pass/fail/na）。fail 项按"失败处理"列执行。所有 fail 项必须在 `remaining_issues` 中列出。
