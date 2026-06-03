# 编排器输出契约（Orchestrator Output Contract）

完整论文生成期间，`academic-paper-writer` 编排器负责写入 `./docs/paper-drafts/` 下的最终产物。

## 默认文件

- `paper_draft.md`: 论文正文、唯一正式 `## References`、以及末尾统一「待补充清单」。正文只能使用 inline citation marker；各节不得单独列出引用说明或章节级参考文献。
- `section_blueprint.md`: 当前 Section Blueprint 与 Section Contract
- `venue-brief.md`: 目标 venue 要求与风格说明
- `figures/`: 图表输出；实验数据图默认交付 SVG，架构图默认交付生图模型生成的高分辨率图片
- `figures/codes/`: 生成的 Python 数据绘图脚本，或简单矢量兼容路径脚本

## 写入边界

子 skill 返回结构化内容和建议路径。完整论文 workflow 运行时，由编排器执行最终写入。

## 默认交付物

- **full-paper-planning**: paper_draft.md (complete), section_blueprint.md, venue-brief.md, figures/, Verified References + Citation-to-Claim Map
- **section-drafting**: Updated paper_draft.md (single section)
- **section-revision**: Revised section text or revised section blueprint

## 完成标准

- All Hard Gates (A-E) passed
- Thin draft resolved (content density check)
- Final verification passed (all hard debts closed)
- Citations >= min_citations (Gate D)
- `paper_draft.md` contains exactly one formal `## References` section.
- `paper_draft.md` ends with a synchronized `## 待补充清单`.
- No section-level citation explanation blocks remain after individual sections.
