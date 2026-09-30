# 验收状态与复核

唯一状态规则在 `../../shared/schemas/verification-report.md`。本文件只说明复核操作。

首次检查给稳定 issue_id。主笔修复后对照原 acceptance_condition，记录已解决/未解决的具体依据；稿件变更检查影响范围。条件满足才移出未解决清单，不因作者接受、换措辞或旧 PASS 自动关闭。

fix 可修但未修 → needs_revision。需作者事实或缺材料 → needs_author_input。无上述问题 → passed，仅针对已声明 scope。

连续两轮同问题无实质进展由主笔交作者决定；状态仍如实保留，不新增 escalated/unresolvable 枚举。引用数量与纯风格偏好不阻塞，缺材料不使整个框架交付失败。
