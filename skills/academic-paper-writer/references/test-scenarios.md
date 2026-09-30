# 验证层级与场景索引

## 可自动执行的合成回归

运行 `python -B scripts/check_schemas.py --skills-root skills` 和 `python -B -m unittest discover -s tests/public -v`。

公开测试仅使用合成 Markdown 与临时技能目录，覆盖引用误放行、组合/范围/重复/未知条目、CLI 退出码及契约缺文件/枚举漂移等。它们验证脚本行为与静态契约，不证明 agent 遵循流程、论文质量或科学结论。

## 真实 agent 场景（不能由静态 PASS 代替）

场景与记录要求见仓库 `tests/public/README.md`。未运行时标未验证；不要声称所有场景通过，也无需建设新旧版本/竞品排名评测。

重点覆盖：仅想法材料下框架交付、有现成结果的直接叙述、可用本地文献无索引、敏感 PDF 上传边界、两轮无进展停止、局部段落修改不重启 intake，以及修改文件后的恢复验收。
