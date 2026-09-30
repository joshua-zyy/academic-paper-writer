# 验收输出

遵循 `../shared/schemas/verification-report.md`：scope、target、draft_version、verdict、checks_run、issues、checked_sources、unchecked_items、next_action。

每个 issue 具有稳定 ID、类别、fix/author_input/suggestion、位置、具体问题、依据、修复完成条件及影响章节。

输出不包含修订正文或自评分。独立单段检查可以用简短表格呈现同样的信息，不强制全文报告；若作者要求改写，将写作任务转交主 agent 的 polishing/writer，而不是本验收 subagent 写。

验收状态只有 passed / needs_revision / needs_author_input。验收覆盖范围明确，不意味着投稿就绪。细则以共享契约为唯一判定来源，不重复另定义 debt 门控。
