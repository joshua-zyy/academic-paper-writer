# 去AI化学术文体规范

目标：让论文正文读起来像经验丰富的人类学者撰写，而不是模板驱动的机器输出。

## 空洞形容词黑名单

| 避免使用 | 条件使用 |
|---|---|
| 非常重要的、显著的 | 仅在附有数据或 VERIFIED 引用时使用；否则删除或换成具体描述 |
| 大量的、许多 | 给出具体数量或范围 |
| 各种各样的 | 列出具体类别或用 "diverse" / "heterogeneous" 等更精确的词 |
| 显而易见的、不言而喻的 | 删除或改为具体论证 |
| 至关重要的 (crucial) | 删除或改为具体机制说明 |
| 深刻的 (profound) | 删除或改为具体效应量 |
| 前所未有的 (unprecedented) | 必须有严格比较支撑，否则删除 |
| 全面的 (comprehensive) | 删除或改为具体覆盖范围 |

## AI 典型连接词替换表

| 避免使用 | 推荐替换 |
|---|---|
| 此外 (Moreover / Furthermore) | 与此相关的是、这一发现与…一致、在…方面 |
| 然而 (However) | 尽管如此、这一矛盾暗示了、与之形成对比的是 |
| 因此 (Therefore) | 这一结果表明、由此可以推断、这一现象提示了 |
| 总而言之 (In summary) | 综合以上观察、上述证据表明 |
| 值得注意的是 (It is worth noting that) | 直接陈述事实，删除套话前缀 |
| 有趣的是 (Interestingly) | 删除，直接陈述观察 |
| 重要的是 (Importantly) | 删除，用因果连接替代 |
|  delve into | 分析、探讨、检验 |
|  notably | 删除或改为具体数据支撑 |
|  significantly | 仅在附 p 值或效应量时使用 |
|  effectively | 删除或改为具体性能指标 |
|  robustly | 删除或改为具体方差/稳定性指标 |

替换原则：不要机械地把一个模板词换成另一个模板词；应根据上下文逻辑选择最自然的表述。

## Before / After 改写示例

### 示例 1：Introduction 开头
- ❌ "In recent years, deep learning has garnered significant attention across various domains."
- ✅ "Deep learning methods have achieved measurable improvements in image classification accuracy, reducing top-5 error from 15.3% to 3.6% on ImageNet between 2012 and 2015."

### 示例 2：Method 描述
- ❌ "We delve into the architecture design to effectively capture robust features."
- ✅ "To reduce sensitivity to input scale variations, we replace global pooling with adaptive spatial attention, which reweights feature maps by estimated saliency scores."

### 示例 3：Results 陈述
- ❌ "Our method significantly outperforms the baseline, demonstrating strong generalization."
- ✅ "On the held-out test set, our method achieved 87.3% accuracy (±1.2%) compared to the ResNet-50 baseline of 82.1% (±1.5%)."

### 示例 4：Discussion 段落
- ❌ "However, it is worth noting that our approach has several limitations."
- ✅ "The current evaluation relies on a single-site dataset with 312 subjects; whether the observed performance transfers to multi-site protocols remains unverified."

## 强化句子级逻辑衔接

- 不要只是罗列事实，要在句子之间建立起因果、转折或递进的深层逻辑联系。
- 常见模式：
  - 因果：前句观察 → 后句推论或解释
  - 递进：前句局限 → 后句改进或补偿
  - 转折：前句主流方法 → 后句其未解决的问题
  - 并列补足：前句方法A局限 → 后句方法B在…方面补充
- 每一段的首句应承担该段的论证职责（topic sentence），而不是空泛的背景铺垫。
- 段落末尾应自然引出下一段的论证方向，而不是突兀跳转。

## 禁用的写作口吻

正文中不得出现以下口吻：

1. **元评论口吻**："这一节的关键是……""本文的方法学重点不在于……而在于……""下面依次解释非显然选择"
2. **审稿人对话口吻**："该设计的合理性在于……""从当前实现看……""一个合理解释是……"
3. **代码讲解口吻**："首先定义输入维度""然后调用 forward 函数""最后返回输出张量"
4. **checklist 痕迹**：段落读起来像是对"要写哪些要点"的逐条回答

## Prose Quality Gate 检查清单

### 通用检查

- [ ] 正文是否以完整 prose 段落为主（非提纲句、说明句）
- [ ] 是否无元评论口吻
- [ ] 是否无审稿人对话口吻
- [ ] 是否无代码讲解口吻
- [ ] 是否无空洞形容词
- [ ] AI 连接词是否已替换
- [ ] 句子间是否有深层逻辑衔接

### 章节专项

- [ ] Introduction / Related Work：有论证链和综合比较（非罗列）
- [ ] Method：有"问题→设计→机制→收益/边界"叙事（非公式罗列）
- [ ] Experimental Setup / Data：有协议、约束与风险说明
- [ ] Discussion / Limitations：有边界分析、失败模式

全部通过 → `prose_debt: closed`；任一项失败 → `prose_debt: open`

改写最多执行 2 轮；2 轮后仍未通过，保留 `prose_debt: open` 但允许继续后续步骤（最终 Verification 不得判为 passed）。
