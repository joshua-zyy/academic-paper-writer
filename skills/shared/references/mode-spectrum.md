# 模式光谱：忠实度 vs 原创性

## 设计原理

不同任务模式对模板结构的需求不同。改编自 Lu et al. (2026) 的 template-based vs template-free 比较：忠实度（模板重、低方差）与原创性（模板轻、高方差）之间的选择决定了代码生成策略。

## 光谱表

| Skill | 模式 | 光谱位置 | 模板依赖 | 理由 |
|-------|------|---------|---------|------|
| academic-paper-writer | `full-paper-planning` | 平衡 | 中 | 有固定 section queue，但内容起草是创造性的 |
| academic-paper-writer | `section-drafting` | 平衡 | 中 | section 结构固定，但写作可适应论证 |
| academic-paper-writer | `section-revision` | 忠实度 | 重 | 修订有固定模板（Critique + Revised Draft） |
| academic-paper-writer | `related-work-or-citation-pass` | 忠实度 | 重 | Citation-to-Claim 映射格式固定 |
| academic-paper-writer | `experiment-evidence-pass` | 忠实度 | 重 | Evidence Inventory 输出格式固定 |
| academic-citation | `full-citation-pass` | 忠实度 | 重 | 检索→核验→映射流程固定 |
| academic-citation | `targeted-citation-search` | 平衡 | 中 | 范围更灵活 |
| academic-citation | `exemplar-set-only` | 平衡 | 中 | 仅构建 Exemplar Set 供学习 |
| academic-citation | `citation-verification` | 忠实度 | 重 | 核验流程完全固定 |
| academic-experiments | `experiment-evidence-pass` | 忠实度 | 重 | 盘点→运行→记录流程固定 |
| academic-experiments | `evidence-inventory-only` | 平衡 | 中 | 仅盘点，无运行约束 |
| academic-experiments | `minimal-reproducible-run` | 忠实度 | 重 | 最小可复核流程固定 |
| academic-figure | `figure-generation` (A 路径) | 平衡 | 中 | 代码生成有模板但适应数据 |
| academic-figure | `figure-generation` (B 路径) | 原创性 | 轻 | 架构图提示词依赖对模型结构的创造性理解 |
| academic-figure | `figure-revision` | 忠实度 | 重 | 按 QA Contract 逐项检查 |
| academic-figure | `figure-audit` | 忠实度 | 重 | 审查清单固定 |
| academic-polishing | `prose-quality-gate` | 忠实度 | 重 | 质量检查清单固定 |
| academic-polishing | `claim-strength-audit` | 忠实度 | 重 | 强度映射规则固定 |
| academic-polishing | `method-prose-rewrite` | 平衡 | 中 | Method 叙事可灵活调整 |
| academic-reviser | `full-section-review` | 忠实度 | 重 | 三轮检查流程固定 |
| academic-reviser | `cross-section-review` | 平衡 | 中 | 跨节检查需要判断力 |
| academic-reviser | `verification-only` | 忠实度 | 重 | 判定规则固定 |
| academic-reviser | `targeted-review` | 平衡 | 中 | 范围灵活 |

## 使用建议

- **忠实度模式**：模板、检查清单、输出格式应严格预定义，减少决策代价
- **平衡模式**：提供默认模板但允许适应，核心约束保留
- **原创性模式**：只提供原则性指导，减少结构约束

选择依据：用户输入越模糊、任务越开放 → 倾向原创性；用户要求越明确、输出越需要一致 → 倾向忠实度。
