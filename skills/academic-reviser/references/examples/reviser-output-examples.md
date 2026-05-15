# Reviser 输出示例

## Passed 场景

```md
## Section Critique

- Issues fixed:
  - 补充了 3 处缺失的 inline citation（此前为 [REF_NEEDED: ...]）
  - 降级了 2 处过度表述：将 "outperforms" 改为内部验证表述
  - 在讨论节明确了当前评估受限于单数据集

- Claims weakened or clarified:
  - "Our method achieves SOTA" → "achieves competitive results on the evaluated benchmarks"
  - "demonstrates strong generalization" → "shows promising results on internal validation"

- Evidence still missing:
  - 外部测试集评估结果（[RESULT_NEEDED: external test set evaluation]）
  - 与 [StrongBaseline2024] 的比较（实验排队中）

- Risks to carry into next section:
  - 当前 split 为 file-level，subject-level 泄漏风险需在 Limitations 中讨论

- Missing figure/table/formula placements: none

- Missing or inconsistent inline citations: 已全部闭合

## Verification Status

- Verdict: passed
- prose_debt: closed
- citation_debt: closed
- evidence_debt: closed
- figure_debt: closed
- thin_draft: no
- Checks performed:
  - [x] 事实与证据检查（13项）
  - [x] 论证强度与审稿风险检查（11项）
  - [x] 结构与风格检查（8项）
  - [x] 代码与方法一致性检查
  - [x] 引用闭合检查
- Remaining issues:
  - 外部测试集结果待补充（不阻塞继续，已标记 [RESULT_NEEDED]）
- Can move to next section: yes
```

## Blocked 场景

```md
## Section Critique

- Issues fixed:
  - 降级了 3 处强结论，改为中等强度表述

- Claims weakened or clarified:
  - "significantly improves" → "appears to improve"
  - "robust to domain shift" → 改为 [RESULT_NEEDED: domain shift evaluation]

- Evidence still missing:
  - 核心模块 X 的设计动机无法从代码恢复
  - 缺少 baseline Y 的比较结果

- Risks to carry into next section:
  - 当前 results section 依赖未闭合的 [RATIONALE_NEEDED]

## Verification Status

- Verdict: blocked
- prose_debt: closed
- citation_debt: closed
- evidence_debt: open
- figure_debt: closed
- thin_draft: no
- Checks performed:
  - [x] 事实与证据检查（13项）
  - [x] 论证强度与审稿风险检查（11项）
  - [x] 结构与风格检查（8项）
- Remaining issues:
  - [RATIONALE_NEEDED: 模块X设计动机] — 外部阻塞
  - [RESULT_NEEDED: baseline Y comparison] — 外部阻塞
- safe_to_continue: no
- frozen_claims:
  - Claim: "模块X通过机制M缓解了问题P"
    Reason frozen: 设计动机无法从代码恢复，需要作者提供设计文档
    Alternative text: "[RATIONALE_NEEDED: 模块X采用机制M的设计动机 | 预期缓解问题P | 需要作者提供]
    Unfreeze condition: 作者提供模块X的设计文档或会议记录
  - Claim: "方法在 baseline Y 上取得优势"
    Reason frozen: 缺少 baseline Y 的完整比较数据
    Alternative text: "[RESULT_NEEDED: baseline Y comparison | main results table]"
    Unfreeze condition: 完成 baseline Y 实验并获得可复核指标
```
