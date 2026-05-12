# Claim 强度控制

## 强结论 (Strong)

**条件**（必须同时满足）：
- 有本地可复核结果
- 评估协议没有明显方法学缺陷
- 或多篇 VERIFIED 文献支持同一背景事实或比较结论

**典型表达**：show, demonstrate, outperform, consistently improves

## 中等结论 (Medium)

**触发降级的场景**：
- 结果来自内部验证而非独立测试
- 对比基线不全
- 只有单一来源支撑
- 本地代码与论文叙述尚未完全对齐

**典型表达**：suggest, indicate, is associated with, appears to improve

## 弱结论或假设 (Weak)

**触发降级的场景**：
- 只有用户口述，没有本地或外部证据
- 指标无法复核
- 引文尚未核验
- 评估协议存在明显泄漏或偏乐观设计

**典型表达**：may, could, is hypothesized to, requires further validation

---

## empirical paper 的常见过度表述

以下说法需要特别警惕，出现时必须主动弱化措辞：

| 过度表述 | 应改为 |
|---------|--------|
| 把内部验证写成"泛化良好" | 明确标注 internal validation 边界 |
| 把验证集调阈值后的结果写成最终性能 | 区分 validation 和 test 结果 |
| 把存在受试者泄漏的结果写成 clinical-level 证据 | 标注数据泄漏风险 |
| 把尚未补全 baseline 的结果写成 SOTA | 降级为"与当前比较范围相比……" |
| 把解释性热图直接写成生物标志物结论 | 区分"模型观察"和"领域解释" |

---

## Claim Strength Audit 输出格式

```md
## Claim Strength Changes

| 原文 | 问题 | 修改后 | 原因 |
|------|------|--------|------|
| "Our method outperforms all baselines" | 基线不全 | "Our method appears to improve over the compared baselines" | 缺少关键对比方法 |
| "This demonstrates strong generalization" | 仅内部验证 | "On our internal validation set, ..." | 无外部测试集 |
```
