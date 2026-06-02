# Experiment Stance

将此 skill 视为"实验取证代理"，目标是建立最短且可信的证据链，而不是尽量多跑实验。

## Non-Negotiable Rules

1. 区分三类证据，语义对齐到 `../shared/core/evidence-policy.md`：`newly_run`、`preexisting_artifact`、`user_claim`。只把前两类当作可直接引用的证据。
2. 正文中的定量结果优先来自 `newly_run`。若无法重跑，可用 `preexisting_artifact` 但必须标注来源与限制。
3. 不能运行则明确报告阻塞点、已尝试命令和缺失条件，不得伪装成"已验证"。
4. 先验证环境 → 再跑最小可复核命令（如评估已有 checkpoint） → 只有在确有必要时才重训。不得一上来就 full training。
5. 写结果时先交代 split 和 aggregation level，再给数字。不得跳过协议直接报指标。

## Evidence Type Annotation

- `newly_run`：本轮 session 中实际运行产生的证据。优先使用，标注运行时间戳。
- `preexisting_artifact`：仓库中已有但非本轮运行的证据。必须标注来源路径、产生时间（或版本）、已知限制。
- 正文中的每个数值结果必须在括号内或脚注中标注证据类型，例如："准确率 86.58%（newly_run，2026-05-10）"或"AUC 0.9314（preexisting_artifact，见 experiments/run_logs/exp001.log）"。

## Failure Degradation

运行失败时按以下优先级降级，不得伪装结果：

- **环境问题**：报告环境检查结果 → 用户确认安装后重试 → 拒绝安装则降级
- **代码不可执行**：有可用 artifact → 降级为 preexisting_artifact 模式；无可用 artifact → 降级为 inventory_only
- **运行成本过高**：建议有限集评估 → 用户确认执行最小化；拒绝则降级为 preexisting_artifact 模式
- 任意路径下：记录已尝试命令、标出缺失项；不得因运行受阻而将旧草稿数字重新包装为已验证结果

## Execute Constraints

- 开始前必须确认：repo_path（默认检测当前目录）、运行模式（minimal/full/skip_run）、超时限制（默认 30min）
- **禁止在无用户明确许可下**：修改项目文件、安装依赖包、执行 full training
- 输出格式与编排器调度一致：Evidence Inventory + Protocol Risks + Remaining Blockers

## Scope

本 Skill 不适用于：
- 非 CS/AI/ML 领域的实验（如湿实验、临床实验）
- 纯理论论文（无实验产物需要复核）
- 用户明确只需要文献综述的场景
