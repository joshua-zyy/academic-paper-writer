# 📝 Academic Paper Writer

**简体中文** | [English](README.en.md)

证据驱动 · 自动推进 · 主笔统一 · 并行取证 · 内容稿交付

[项目首页](https://joshua-zyy.github.io/academic-paper-writer) · [GitHub Issues](https://github.com/joshua-zyy/academic-paper-writer/issues) · [MIT License](LICENSE)

面向 CS / AI / ML 的八个 Agent Skills。一次启动，依据作者现有材料与想法，组织取证、写作、章节验收和全文验收，默认自动交付可用的论文**内容初稿**。后续可独立修改章节或段落，不必重新启动整篇流程。

材料决定交付深度：有依据的内容写成正文，缺材料处保留具体框架与补充建议。不编造结果、动机、方法或文献，不将框架稿包装成近投稿完整稿，也不承诺实验或稿件可被录用。

## 目录

- [Skills 一览](#skills-一览)
- [快速开始](#快速开始)
- [推荐配置](#推荐配置)
- [核心设计](#核心设计)
- [编排器核心工作流](#编排器核心工作流)
- [使用示例](#使用示例)
- [文档分层](#文档分层)
- [安全边界](#安全边界)
- [维护与验证](#维护与验证)
- [参考项目](#参考项目)

## Skills 一览

| Skill | 职责 | 独立用途 |
|-------|------|---------|
| **academic-paper-writer** | 主笔与整体编排，取证复用、章节及全文整合 | 整篇初稿、章节起草/修订 |
| **academic-citation** | 本地优先检索，文献身份与原文支持分别核对 | 定向找引用、核验、论点映射 |
| **academic-experiments** | 默认只读盘点协议、数据、结果和事实冲突 | 查结果来源、协议交代、授权范围内重算 |
| **academic-reviser** | 单一产物验收角色，报告问题及修复条件 | 章节/全文/局部验收；不替作者改正文 |
| **academic-polishing** | 表达、论证与主张范围；全文编排由主笔内化 | 章节、段落、句子改写 |
| **academic-figure** | 有源数据的图、图注与正文一致性 | 生成、审查或修改数据图；架构图由作者提供 |
| **academic-venue-research** | 当前官方要求与样例风格分开 | 定向查询投稿要求或写法 |
| **academic-latex-layout** | 独立排版、浮动体与模板适配 | 作者明确请求时调用，不进入默认内容稿路径 |

## 快速开始

### 方式一：Claude Code 插件安装（推荐）

```text
/plugin marketplace add joshua-zyy/academic-paper-writer
/plugin install academic-paper-writer@academic-paper-writer
```

需要 stable 分支时使用 `/plugin marketplace add joshua-zyy/academic-paper-writer@stable`。更新可执行 `/plugin update academic-paper-writer@academic-paper-writer`；是否自动更新以平台设置为准。

安装后使用 `/academic-paper-writer`；专项请求可用 `/academic-citation`、`/academic-experiments`、`/academic-reviser`、`/academic-polishing`、`/academic-figure`、`/academic-venue-research` 或 `/academic-latex-layout`。

### 方式二：Codex CLI 安装

```bash
# 用户级目录
 git clone https://github.com/joshua-zyy/academic-paper-writer.git ~/.agents/skills/academic-paper-writer
# 如需 stable：git clone -b stable <repository-url> <directory>
# 如需锁定版本：git clone -b <existing-tag> <repository-url> <directory>
```

进入安装目录后 `git pull`；切换版本前检查本地变更，再 `git checkout stable` 或目标标签。技能发现方式以当前平台版本为准。

### 方式三：手动加载

```bash
git clone https://github.com/joshua-zyy/academic-paper-writer.git
```

在支持 Skills 的平台中加载 `skills/academic-paper-writer/SKILL.md`；专项请求直接加载对应子技能。宿主支持 subagent 时可并行取证；不支持时主 agent 承担同样职责并说明降级，不伪造派发。

### 准备材料与本地文献库

代码、笔记、作者想法、现有草稿、日志、CSV、图表均可作为输入；不要求先有完整仓库或所有实验。说明材料位置和语言即可开始必要盘点；venue 可暂未确定。

**启动前推荐 MinerU PDF→Markdown 建库**，分别保存待引用文献与 venue 风格样例，供多轮任务复用。已有库直接使用，新增文献按需增量补充。不强制全部转换；缺 `_index_ref.json` 不阻塞写作，所需原文不可读只影响依赖它的判断。

```powershell
# <citation_skill_dir> 是当前安装的 academic-citation 绝对路径
$env:MINERU_API_TOKEN = "<token>"
python "<citation_skill_dir>/scripts/convert-pdfs-to-md.py" "<pdf_dir>" "<md_dir>" --type ref
# 风格库改用 --type style
```

MinerU API 会上传 PDF；敏感或未公开材料须确认上传授权，token 不进入论文或状态文件。转换成功与索引存在不证明文献身份或内容支持。

项目主体是技能文档与辅助脚本，无额外统一运行时。PDF 转换需 Python 3.10+ 和 MinerU API Token；数据图按需使用 matplotlib 等绘图依赖，不自动安装。公开测试和契约检查仅使用 Python 标准库。

## 推荐配置

### 推荐模型

| 模型 | 说明 |
|------|------|
| **claude-opus-5.5** | anyRouter 提供的 API，可参考 https://anyrouter.top/register?aff=hZXa |
| **gpt-6-astra** | agentRouter 提供的 API，可参考 https://agentrouter.org/register?aff=Wpuc |
| **DeepSeek V4.1 Flash** | 可用于测试技能|

模型名称、可用性与费用以服务商当前说明为准。敏感材料是否允许发送给模型/中继由作者决定。

### Agent 平台

| 平台 | 加载方式 |
|------|----------|
| OpenCode | 按平台设置加载 Skills，使用 subagent 调度 |
| Claude Code | 插件安装 |
| Codex CLI | 本地 Skills 目录 |
| 其他平台 | 加载 SKILL.md，依宿主能力执行 |

## 核心设计

### 一个主笔，取证与验收协作

主 agent 是正文唯一作者，负责起草、润色、修订与合并。探查 subagent 返回**事实、来源定位、冲突和缺口**；验收 subagent 返回**问题、依据和修复完成条件**，不输出章节初稿或修订正文。

首轮按方法、协议/结果、文献并行探查，跨节复用已有证据；后续只针对具体缺口补查，不每节重新全仓/全库读取。明确任务范围、读写路径、授权和结束条件；图表代理仅在分配目录生成获准的图与脚本，不改研究源文件或正文。

### 直接表达事实，不机械降调

区分作者提供的结果/事实、设计意图和未验证猜想，不将作者材料一概拒绝，也不一概视为已核验。正文直接写有依据的观察和比较，解释、因果、泛化、SOTA 分别检查自己的支持范围；局限在 Discussion 适度集中说明。

文献身份核对与原文是否支持具体论点分开。摘要支持的范围不冒充全文阅读。`min_citations` 无论作者指定还是系统建议，都**只是建议**，不凑数量、不作为完成门槛。

### 验收不是模拟审稿

验收关注表达、空泛段落、逻辑断链、数据/叙事矛盾、协议交代、解释与文献一致性、引用及图文错误。协议闭合是交代清楚、可追溯，不评价方法学是否最优，不模拟审稿人、不判断创新性或录用概率。

| 状态 | 含义 |
|------|------|
| `passed` | 声明范围内无待修问题，可保留建议 |
| `needs_revision` | 有主笔可修的具体问题 |
| `needs_author_input` | 缺作者材料、确认或授权；无关部分继续 |

问题必须有位置、依据与修复条件；修复后定向复核，不循环重审整稿。同一问题连续两轮无实质进展时交作者决定，保留真实状态。

交付等级另行标记：`usable_draft`（实质内容稿）、`partial_draft`（已有正文加局部框架）、`structured_outline`（框架与补充建议为主）。接收缺口交付不意味着验收通过或投稿就绪。

## 编排器核心工作流

1. **盘点与集中确认**：复用作者已给信息，默认自动推进，可选逐节确认、中途切换；主动推荐文献建库。
2. **首轮取证与主线确认**：并行探查、合并来源；写作前让作者确认核心主张与论证主线。
3. **主笔起草与章节验收**：有材料写正文，缺材料给具体框架与补充建议；按问题修复和定向补查，独立部分继续。
4. **全文整合与验收**：检查跨节主张/数字/术语、引用支持及图文一致性；Abstract 与 Conclusion 依据现有主体后置写作。
5. **交付或继续补证**：交付前集中说明重大缺口与等级，作者选择继续或接收现有稿；高成本补证、新实验等另行决策。

默认输出根目录为 `./academic-paper-writer/paper-drafts/`，作者可选择其他目录。主要文件：`paper_draft.md`、`section_blueprint.md`、`evidence_inventory.yaml`；持续多节任务用 `task_state.yaml` 记录主线、章节状态、问题与下一步。恢复时核对实际文件版本，不能只信状态文件的 PASS。

默认只交付**内容稿**，无需 LaTeX/Word、PDF 编译或投稿文件包。架构图由作者提供；必要数据图按授权生成。

## 使用示例

### 一次启动整篇初稿

```text
材料在 ./research：方法笔记、已有 CSV 结果和本地文献。
想法是用动态关系建模解决跨会话变化，语言英文，venue 暂未定。
请确认主线后自动推进，交付可用内容稿；缺材料处给具体框架和补充建议。
不要运行新实验或默认排版。
```

### 可选逐节推进

```text
这次每节写完让我确认；之后我可能切换回自动推进。
```

### 独立局部任务

```text
/academic-polishing 改写这段 Method，保留给定事实，不添加动机或结果。
/academic-citation 核对这一条文献的身份，以及它是否支持当前比较句。
/academic-experiments 只读核对 CSV、日志和结果段的指标口径，不运行代码。
/academic-reviser 验收这一节，给出具体问题和修复条件，不改正文。
```

只有笔记或想法也可先得到框架和已能写的内容；不能凭空填充完整 Results。只需排版时直接调用 academic-latex-layout。

## 文档分层

| 层级 | 文件 | 用途 |
|------|------|------|
| 技能入口 | 各 `SKILL.md` 与 `manifest.yaml` | 职责、路由、按需加载 |
| 共享规则 | `skills/shared/core/` | 证据、非编造、读写所有权 |
| 共享契约 | `skills/shared/schemas/` | 证据、文献身份/支持、阅读与验收 |
| 工作流 | writer `references/orchestration-workflow.md` 与三个 `workflow-step-*.md` | 准备、起草、验收/交付/恢复 |
| 专业细则 | 各技能 `references/` | 论证、图表、检索、协议等按需规则 |

项目辅助脚本在 `scripts/` 与对应技能 `scripts/`，公开合成回归测试在 `tests/public/`。不公开私人论文、结果或研究材料。

## 安全边界

- **不编造或混淆**：结果、文献、源码定位和核验状态都要有依据；作者事实、意图和猜想分别处理。
- **有限执行**：默认只读取证与检索；重算/统计须限定授权，新实验、重训、改变协议单独审批。
- **不扩大验收**：不将论文可用性检查变成方法学或创新性评审，不用模糊风格偏好阻塞。
- **缺口透明**：缺什么、影响哪部分、需作者给什么材料要具体；框架稿不称完整近投稿稿。
- **不擅自外传**：敏感 PDF 上传和材料处理须符合作者授权；token 不写入产物。

## 维护与验证

```bash
python -B scripts/check_schemas.py --skills-root skills
python -B -m unittest discover -s tests/public -v
```

契约检查只验证路径、声明与枚举等静态一致性，不能证明文献真实、科学结论正确或 agent 行为可靠。公开测试覆盖引用结构反例、CLI 状态与检查器反例；不建立新旧/竞品速度或质量排名。

`citation_audit.py` 仅检查 numeric 引用结构：组合/范围标记、缺失、孤立、重复与未核验标记；退出 0 也明确身份/原文支持 **NOT CHECKED**。author-year 返回未检查，需要单独对照。人工/真实 agent 场景见 `skills/academic-paper-writer/references/test-scenarios.md`，未执行不得声称行为通过。

`main` 为开发分支；需要固定版本时使用已有标签或维护的 stable 分支。当前功能是否经过真实任务验收，应以对应测试证据为准。

## 参考项目

- [PaperSpine](https://github.com/WUBING2023/PaperSpine)（MIT）：证据记录与同任务恢复思路。
- [nature-skills](https://github.com/Yuan1z0825/nature-skills)（Apache-2.0）：正文纪律与按需加载思路。
- [superpowers](https://github.com/obra/superpowers)
- [academic-research-skills](https://github.com/Imbad0202/academic-research-skills)

本轮借鉴工作流思想，不复制外部代码；若后续直接复用内容，应保留来源归属与相应许可。

[Agent Skills 规范](https://agentskills.io) · [Claude Code 文档](https://docs.anthropic.com/en/docs/claude-code/plugins) · [Codex CLI](https://github.com/openai/codex)

## 许可

[MIT License](LICENSE)。最终论文的学术诚信、研究真实性、引用准确性与投稿合规性由作者负责。
