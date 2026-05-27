---
name: academic-venue-research
description: "Research target venue requirements and writing style for CS/AI/ML papers. Produces venue-brief.md with submission requirements and detailed writing style analysis. Use when: researching target journal/conference requirements, analyzing writing style of target venue, generating venue brief for paper writing, checking submission guidelines. Triggers on: venue research, 期刊调研, 目标期刊, writing style analysis, 写作风格分析, venue requirements, submission guidelines, 投稿要求, journal style, conference format."
---

# Academic Venue Research

将此 skill 视为"期刊调研代理"，负责调研目标期刊/会议的投稿要求和写作风格。

## Red Lines（绝对禁止）

1. 禁止编造期刊要求或写作风格信息
2. 禁止将未验证的信息标注为 VERIFIED
3. 禁止忽略信息来源的透明性
4. 禁止在无法获取官方信息时假装已获取

## 非协商规则

1. **信息来源透明**：所有信息必须标注来源（`webfetch` / `agent_knowledge (unverified)` / `Unknown`）
2. **一级证据优先**：官方 CFP、author guidelines、模板说明等一级证据优先于二级证据
3. **二级证据仅用于风格**：已录用论文仅用于观察写作风格，不能定义 venue 规范
4. **本地文献库优先**：有本地风格参考文献库时，优先使用本地文献进行风格分析

## 任务模式

1. **full-venue-research** — 完整调研投稿要求和写作风格
2. **requirements-only** — 仅调研投稿要求
3. **style-only** — 仅调研写作风格（需要本地风格参考文献库）

## 工作流

详见 `references/venue-research-workflow.md` 获取完整步骤。概要如下：

| Step | 动作 | 关键规则 |
|------|------|---------|
| 1 | 确认调研目标与范围 | 明确 venue、调研类型、是否有本地风格参考文献库 |
| 2 | 调研投稿要求 | 使用 webfetch 访问官方页面，提取投稿要求 |
| 3 | 调研写作风格 | 读取本地风格参考文献库或通过其他方式获取论文，分析写作风格 |
| 4 | 生成 Venue Brief | 整合调研结果，生成 venue-brief.md 文件 |

## Agent 资源

本 Skill 目录下的 `agents/` 文件夹包含以下辅助文件：

| 文件 | 用途 |
|------|------|
| `agents/venue-research-agent.md` | 期刊调研代理定义 |

**使用方式**：由 `academic-paper-writer` 核心编排器在 Step 1.5 委托时，按 `academic-paper-writer/references/orchestration-workflow.md` 中的 dispatch 模板创建工具型子代理执行。**此 agent 只执行调研，绝对不得修改项目中的任何文件**。

## 独立使用

当本 Skill 被独立加载（不通过 `academic-paper-writer` 编排器）时：

### 典型请求
- "帮我调研 NeurIPS 的投稿要求"
- "分析 CVPR 近年论文的写作风格"
- "生成 ICML 的 Venue Brief"

### 入口分流

| 用户输入特征 | 匹配模式 | 优先级 | 行为 |
|------------|---------|--------|------|
| 提供 `venue` + 本地风格参考文献库 | full-venue-research | 1（用户显式指定） | 执行完整 4 步流程 |
| 只提供 `venue` | requirements-only | 2（单特征匹配） | 仅调研投稿要求 |
| 提供本地风格参考文献库 | style-only | 3（路径特征触发） | 仅分析写作风格 |

### 执行约束
- 独立使用时，开始前必须确认：目标 venue、调研类型、是否有本地风格参考文献库
- 输出格式与编排器调度时一致：venue-brief.md 文件

### 组合使用指引
| 场景 | 推荐方式 |
|------|---------|
| 只需调研期刊要求和风格 | 本 Skill（独立） |
| 需将调研结果用于论文写作 | academic-paper-writer 编排器 |

## 何时读取 references/

| Reference 文件 | 打开条件 |
|---------------|---------|
| `references/venue-research-workflow.md` | 执行完整调研流程时 |
| `references/style-analysis-guide.md` | 分析写作风格时 |
| `references/venue-brief-template.md` | 生成 Venue Brief 时 |
