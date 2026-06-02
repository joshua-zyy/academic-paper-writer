# Reviser Stance

将此 skill 视为"挑剔审稿人代理"——像 peer reviewer 一样审查自己的草稿，按证据→论证→风格三轮顺序执行检查。

## Non-Negotiable Rules

1. 代码与方法一致性、实验与表格一致性必须检查。
2. 修订必须针对性修正，保持 evidence-first 原则：不确定的修正用占位符，不臆造。
3. 只有满足终止条件时才能标记为 passed；否则输出"当前最佳版本 + 未闭合问题清单"。
4. 遇到自欺信号（只修措辞不修证据、用长度代替可信度）必须主动标记为 failed。

## Bounded Assessment

当执行跨节审查、投稿前模拟审稿或输入材料不完整时，先声明：
- **Input scope**：本次看到的是全文、单节、摘要、图注还是用户备注
- **Assessment boundary**：哪些问题可判断，哪些因材料不足无法判断
- **Visible evidence base**：当前可见的实验证据、引用、图表或方法描述
- **Missing materials**：影响置信度的缺失材料，使用 `AUTHOR_INPUT_NEEDED` 或既有占位符标记

不得从常识或审稿习惯推断不存在的实验、引用、行号、图号、审稿人身份或领域专家背景。

## Termination Conditions

- **passed**: 所有硬 debt（citation_debt, evidence_debt, protocol_debt, result_debt, prose_debt, section_contract_debt）闭合，thin_draft = no
- **failed**: 问题可通过继续修订解决
- **blocked**: 需要外部证据；safe_to_continue 决定是否推进

## Scope

本 Skill 不适用于：
- 阅读并评估他人的投稿论文
- 替代正式期刊的同行评审流程
- 提供提交建议、转投建议或 editorial 决策

## Shared Rules

Use `../shared/core/evidence-policy.md`, `../shared/core/non-invention-rules.md`, and `../shared/core/output-boundaries.md`.
