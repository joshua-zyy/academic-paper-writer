<p align="center">
  <h1 align="center">📝 Academic Paper Writer</h1>
  <p align="center">证据驱动 · 分节闭环 · 模块协作 · 硬门控 · 可验证</p>
  <p align="center">
    <a href="https://github.com/joshua-zyy/academic-paper-writer/blob/main/LICENSE">
      <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
    </a>
    <img src="https://img.shields.io/badge/domain-CS%2FAI%2FML-brightgreen" alt="Domain">
    <img src="https://img.shields.io/badge/status-active-success" alt="Status">
    <img src="https://img.shields.io/badge/skill%20system-7%20skills-9A4D8E" alt="Skills">
    <img src="https://img.shields.io/badge/architecture-Core%20%2B%20Subskills-orange" alt="Architecture">
  </p>
    <p align="center">
      <a href="https://joshua-zyy.github.io/academic-paper-writer">
        <img src="https://img.shields.io/badge/🌐_访问项目页面-blue?style=for-the-badge" alt="官网">
      </a>
    </p>
</p>

---

Academic Paper Writer 是面向 `CS / AI / ML` 论文写作场景的 **模块化、证据驱动** 的 Agent Skill 集合。

<table>
<tr>
<td><strong>你是否也遇到过这些论文写作焦虑？</strong>
<br>
<blockquote>
<table>
<tr>
<td width="4px" bgcolor="#0F4D92">🤷</td>
<td><strong>无从下笔</strong> — 模型代码全部跑通，对着空白文档却不知第一句话写什么</td>
</tr>
<tr>
<td width="4px" bgcolor="#42949E">📐 </td>
<td><strong>表述不准</strong> — 算法和公式在脑中模糊，只有大概的思路</td>
</tr>
<tr>
<td width="4px" bgcolor="#B64342">🎨</td>
<td><strong> 图表头秃</strong> — 实验数据堆了一桌子，论文级的可视化不知道从何画起</td>
</tr>
<tr>
<td width="4px" bgcolor="#9A4D8E">🔍</td>
<td><strong> 缺少支点</strong> — 直觉上知道自己的工作有意义，但找不到让 reviewer 信服的论证锚点</td>
</tr>
</table>
</blockquote>
你不是一个人，学术写作的最大障碍往往不是做得不够，而是不知道怎么写出来。</td>
</tr>
</table>

**这不是一个简单的一次性生成整篇论文的 prompt，而是一套工程化写作系统： 先把论文拆成多个可独立验证的环节，按证据审计 → 文献检索 → 实验复核 → 起草 → 质量门 → 验证的闭环逐节推进。每个环节都设硬门控，证据不足就阻塞或降级，绝不硬写。**

**核心思想在于将各位researcher从枯燥的论文写作中解放出来，将更多的时间与经历投入到对于论文/模型创新点的思考与设计当中。**

---

## 💬 反馈与改进

<p align="center">
  <em>独自迭代与维护这个项目，必然会陷入思维逻辑的困境</em><br>
  <strong>非常重视与欢迎各位 researcher 提出在实际使用中遇到的问题以及对项目的改进想法</strong>
</p>

<table align="center">
<tr>
<td align="center"><strong>🐛 遇到问题</strong></td>
<td align="center"><strong>💡 有改进建议</strong></td>
<td align="center"><strong>🤔 有疑问</strong></td>
</tr>
<tr>
<td>工作流卡住、gate 误判、文档不清晰</td>
<td>觉得某个步骤可以优化、需要新的 skill 或 probe</td>
<td>不确定某个设计为什么这样、或者想了解最佳实践</td>
</tr>
</table>

<p align="center">
  <a href="https://github.com/joshua-zyy/academic-paper-writer/issues">
    <img src="https://img.shields.io/badge/📝_提交反馈-GitHub_Issues-blue?style=for-the-badge" alt="提交反馈">
  </a>
</p>

<p align="center">
  <em>每条 issue 描述清楚复现步骤或期望行为即可，我会定期查看并纳入迭代计划</em>
</p>

---

### 🚧 开发进度

<p align="center">
  <img src="https://img.shields.io/badge/📊_数据图绘制-积极完善中-purple" alt="数据图绘制">
  <img src="https://img.shields.io/badge/✨_文字润色-积极完善中-purple" alt="文字润色">
  <img src="https://img.shields.io/badge/🔍_文献检索-积极完善中-purple" alt="文献检索">
  <img src="https://img.shields.io/badge/📚_引用管理-积极完善中-purple" alt="引用管理">
</p>

<p align="center">
  <strong>项目正在积极优化中，欢迎各位 researcher star 和 fork 项目，一起推动项目发展</strong>
</p>

---

<h2 id="目录">📑 目录</h2>

- [Skills 一览](#skills-一览)
- [快速开始](#快速开始)
  - [Claude Code 插件安装](#方式一claude-code-插件安装推荐)
  - [Codex CLI 安装](#方式二codex-cli-安装)
  - [手动加载](#方式三手动加载)
- [推荐配置](#推荐配置)
- [核心设计](#核心设计)
- [编排器核心工作流](#编排器核心工作流)
- [使用示例](#使用示例)
- [适用场景](#适用场景)
- [文档分层](#文档分层)
- [项目结构](#项目结构)
- [安全边界](#安全边界)
- [维护与验证](#维护与验证)
- [参考项目](#参考项目)

---

<h2 id="skills-一览">📋 Skills 一览</h2>

| Skill | 角色 | 用途 | 典型触发词 |
|-------|------|------|-----------|
| 🧠 **academic-paper-writer** | **核心编排器** | 完整论文起草、section loop、Hard Gates、子 skill 调度 | `写论文`、`paper draft` |
| 🔍 **academic-citation** | 文献取证 | 文献检索、核验、Citation-to-Claim 映射、本地文献库优先搜索、subagent 全文阅读、Exemplar Set | `找引用`、`citation pass` |
| 🔬 **academic-experiments** | 实验取证 | 实验证据盘点、最小可复核执行、协议风险审计 | `复核实验`、`verify results` |
| ✅ **academic-reviser** | 审稿人 | 证据审查、三轮自审、Verification 判定 | `审修`、`self review` |
| ✨ **academic-polishing** | 文体打磨 | Prose Quality Gate、Claim Strength Audit、去 AI 化 | `润色`、`claim strength` |
| 📊 **academic-figure** | 数据图生成 | 实验数据图（Python 代码）、图表审查与修改；架构图只记录手工绘制需求 | `绘图`、`训练曲线`、`消融实验` |
| 🏛️ **academic-venue-research** | 期刊调研 | 调研目标 venue 投稿要求与写作风格，产出标准化 Venue Brief | `期刊调研`、`venue research`、`投稿要求` |

---

<h2 id="快速开始">🚀 快速开始</h2>

<h3 id="方式一claude-code-插件安装推荐">方式一：Claude Code 插件安装（推荐）</h3>

#### 选项 A：开发版（自动更新）

使用 `main` 分支，每次启动 Claude Code 自动获取最新版本。

```bash
# 1. 添加 marketplace（main 分支）
/plugin marketplace add joshua-zyy/academic-paper-writer

# 2. 安装插件
/plugin install academic-paper-writer@academic-paper-writer
```

> 💡 **自动更新**：main 分支版本无需手动更新，每次启动 Claude Code 会自动检测并同步最新代码。

#### 选项 B：稳定版（手动更新）

使用 `stable` 分支，只获取经过测试的稳定版本。

```bash
# 1. 添加 marketplace（stable 分支）
/plugin marketplace add joshua-zyy/academic-paper-writer@stable

# 2. 安装插件
/plugin install academic-paper-writer@academic-paper-writer
```

> ⚠️ **手动更新**：稳定版需要手动执行更新命令：
> ```bash
> /plugin update academic-paper-writer@academic-paper-writer
> ```

#### 版本对比

| 版本 | 分支 | 更新方式 | 适用场景 |
|------|------|----------|----------|
| **开发版** | `main` | 自动更新 | 开发者、早期用户、想要最新功能 |
| **稳定版** | `stable` | 手动更新 | 生产环境、稳定性要求高的用户 |

#### 安装后可用命令

- `/academic-paper-writer` - 完整论文工作流
- `/academic-citation` - 文献检索与核验
- `/academic-experiments` - 实验复核
- `/academic-reviser` - 审稿验证
- `/academic-polishing` - 文体打磨
- `/academic-figure` - 图表生成
- `/academic-venue-research` - 期刊调研

<h3 id="方式二codex-cli-安装">方式二：Codex CLI 安装</h3>

#### 选项 A：开发版（main 分支）

```bash
# 克隆到用户级目录（推荐）
git clone https://github.com/joshua-zyy/academic-paper-writer.git ~/.agents/skills/academic-paper-writer

# 或克隆到项目级目录
git clone https://github.com/joshua-zyy/academic-paper-writer.git .codex/skills/academic-paper-writer
```

#### 选项 B：稳定版（stable 分支）

```bash
# 克隆 stable 分支到用户级目录
git clone -b stable https://github.com/joshua-zyy/academic-paper-writer.git ~/.agents/skills/academic-paper-writer

# 或克隆到项目级目录
git clone -b stable https://github.com/joshua-zyy/academic-paper-writer.git .codex/skills/academic-paper-writer
```

#### 选项 C：指定版本（tag）

```bash
# 克隆特定版本
git clone -b v1.0.0 https://github.com/joshua-zyy/academic-paper-writer.git ~/.agents/skills/academic-paper-writer
```

#### 更新插件

```bash
# 进入 skill 目录
cd ~/.agents/skills/academic-paper-writer

# 拉取最新代码（main 分支）
git pull

# 或切换到 stable 分支
git checkout stable
git pull

# 或切换到特定版本
git checkout v1.0.0
```

#### 版本对比

| 版本 | 分支/标签 | 更新方式 | 适用场景 |
|------|-----------|----------|----------|
| **开发版** | `main` | `git pull` | 开发者、早期用户 |
| **稳定版** | `stable` | `git pull` | 生产环境 |
| **指定版本** | `v1.0.0` 等 | 手动切换 | 需要锁定版本 |

<h3 id="方式三手动加载">方式三：手动加载</h3>

```bash
git clone https://github.com/joshua-zyy/academic-paper-writer.git
```

在支持 Skill 机制的 Agent 平台中加载对应 SKILL.md：

| 场景 | 加载方式 |
|------|---------|
| 📄 **完整论文工作流** | 加载 `skills/academic-paper-writer/SKILL.md` |
| 🎯 **单一专项任务** | 直接加载对应子 skill 的 `SKILL.md` |

本项目本身不依赖额外 Python 包或 Node 运行时，主要内容是 skill 文档、reference、schema 和辅助脚本。

### 可选依赖

以下 Python 脚本为可选工具，按需安装：

| 脚本 | 用途 | 依赖                        |
|------|------|---------------------------|
| `skills/academic-citation/scripts/convert-pdfs-to-md.py` | 将本地 PDF 文献转换为 Markdown（本地文献库功能，含图片提取） | Python 3.10+, `pymupdf4llm` |
| `scripts/check_schemas.py` | 验证跨技能 schema 一致性 | Python 3.12+|

### 3. 准备输入材料

越完整的输入，skill 的表现越稳定：

<pre>
📂 代码仓库路径    🏛️ 目标会议 / 期刊    🌐 写作语言
📊 实验日志 / CSV  📄 已有草稿 / outline  📝 研究摘要 / 贡献点
</pre>

---

<h2 id="推荐配置">⚙️ 推荐配置</h2>

### 推荐模型

| 模型                       | 说明                                                                                       |
|--------------------------|------------------------------------------------------------------------------------------|
| 🚀 **gpt-5.5**           | anyRouter中提供免费的api，需要使用vpn+教育邮箱/linux do账号注册，地址: https://anyrouter.top/register?aff=hZXa |
| 🚀 **claude-4.8**        | anyRouter中提供免费的api，需要使用vpn+教育邮箱/linux do账号注册，地址: https://anyrouter.top/register?aff=hZXa                           |
| 🚀 **DeepSeek V4 Flash** | 没其他原因，主要是token价格低，且是推理模型支持1m上下文，可以用于测试skill效果                                            |

### 推荐 Agent 平台

| 平台 | 安装方式 | 更新方式 | 说明                                         |
|------|----------|----------|--------------------------------------------|
| ⚡ **OpenCode** | `git clone` 到 `~/.agents/skills/` | 手动 `git pull` | 强烈推荐，对于本skill多智能体派发编排最适配，开源 Agent 平台，灵活可扩展 |
| 🤖 **Claude Code** | `/plugin marketplace add` + `/plugin install` | 自动更新（main分支）或手动 `/plugin update` | Anthropic 官方 CLI 工具，原生支持 Skill 机制，推荐使用     |
| 🔧 **Codex CLI** | `git clone` 到 `~/.agents/skills/` | 手动 `git pull` | OpenAI 代码助手，支持多种编程任务                       |


> 💡 **提示**：使用支持 Skill 机制的 Agent 平台可获得最佳体验，其他平台也可通过加载 SKILL.md 文件使用本项目。

---

<h2 id="核心设计">🏗️ 核心设计</h2>

### 🔍 证据优先，逐节闭环

每一节经历固定闭环，不允许跳过任何环节：

```text
┌─────────────────────────────────────────────────────────────┐
│                 逐节闭环（每节必须经历）                      │
│                                                             │
│   ✏️ Draft v1 → 📌 占位符审计 → ⚖️ 证据合规审查              │
│       → ✨ Prose Gate → 📏 Expansion → ✅ Self-Review       │
│       → Verification                                        │
│              │                                               │
│              ├── passed  ▶️ 推进下一节                         │
│              └── failed  🔁 回到 ⚖️ 证据合规审查 重来          │
└─────────────────────────────────────────────────────────────┘
```

- 初稿可以带占位符，但占位符必须被记录、审计和追踪
- `Verification` 未通过时不能假装通过

### 🧩 Core + Subskills 架构

核心编排器负责：判断任务模式 → 确认 venue/language → 组织 section queue → 维护 cumulative draft → 吸收子 skill 的专项结果。

| Core 环节 | 委托 Skill | 处理方式 |
|-----------|-----------|---------|
| 🏛️ 目标 Venue 调研 | `academic-venue-research` | dispatch 子 Agent |
| 🔍 文献检索与核验（含本地文献库优先 + subagent 全文阅读） | `academic-citation` + `literature-reader-agent` | dispatch 子 Agent |
| 🔬 实验证据复核 | `academic-experiments` | dispatch 子 Agent |
| 📊 数据图 / 实验结果图 | `academic-figure` | dispatch 子 Agent |
| ✨ Prose Quality Gate | `academic-polishing` | **内化调用**（主 Agent 自行执行） |
| ✅ 证据审查与 Verification | `academic-reviser` | dispatch 子 Agent |

> **设计原则**：主 Agent 直接撰写论文正文，确保叙事风格一致。子 Agent 仅提供工具型专项输出，不得直接修改 Cumulative Draft。

### 🚧 Hard Gates + 数据契约

五个不可跳过的基础关卡：

| Gate                  | 触发位置 | 核心条件 | 失败处理 |
|-----------------------|---------|---------|---------|
| 🏛️ **A：Venue 调研**    | Step 1 → Step 2 | venue 确认后必须完成 Step 1.5，生成 venue-brief.md | 阻塞，不得进入 Step 2 |
| 🔬 **B：证据完备**         | Step 2 → Step 6 | 至少一条可引用证据 | 降级路径或阻塞 |
| 📖 **C：引用就绪**         | Step 3 → Step 6 | 至少一条 VERIFIED 引用 | Intro/RW 阻塞；Method 可占位 |
| 🚪 **D：Verification** | Step 6.8 → Step 7 | 所有 debt 闭合 + 内容达标 | passed/blocked/failed |
| 📚 **E：引用数量**         | Step 8 → 输出 | 全文去重引用 >= `min_citations` 篇（默认 35） | 未达标时提醒，可补充后重检 |

跨 skill 之间通过显式 **数据契约** 交换信息：

```yaml
📦 Evidence Inventory      # 实验证据盘点   → academic-experiments → orchestrator
✅ Verified References      # 核验文献清单   → academic-citation    → orchestrator
📖 LiteratureReadingReport # 文献阅读报告   → literature-reader-agent → orchestrator
📋 Verification Report     # 验证状态报告   → academic-reviser     → orchestrator
🗺️ Citation-to-Claim Map   # 引用-主张映射   → academic-citation    → orchestrator
```

---

<h2 id="编排器核心工作流">🔄 编排器核心工作流</h2>

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                         编排器核心工作流                                  │
│                                                                          │
│   🎯 Step 0  判定任务模式                                                 │
│    ↓                                                                    │
│   🔒 Step 1  确认 venue / 语言 + 本地文献库（🔴硬阻塞）                   │
│    ↓                                                                    │
│   🏛️ Step 1.5  Venue 调研（🔴硬阻塞，生成 venue-brief.md）                │
│    ↓                                                                    │
│   ⏭  Step 1b  可选 PDF→MD 转换（生成脚本提示用户，不阻塞主流程）           │
│    ↓                                                                    │
│   🔍 Step 2  并行证据审计（⚡涉及多 probe 时必须并行 dispatch）            │
│    ↓                                                                    │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │              调研阶段                                              │   │
│   │  📚 Step 3  文献检索与核验（四步流程）                              │   │
│   │     ├─ 3a  本地文献库优先搜索（MD/PDF 直读）                        │   │
│   │     ├─ 3b  联网检索 + 全文获取 + subagent 阅读                     │   │
│   │     └─ 3c  聚合 + Citation-to-Claim Map + 3d 引用清单文件          │   │
│   │  🔬 Step 4  实验事实复核                                           │   │
│   └──────────────────────────────────────────────────────────────────┘   │
│    ↓                                                                    │
│   🧩 Step 5  Section Blueprint / Method Blueprint                        │
│    ↓                                                                    │
│   ✏️ Step 6  Draft v1（前置深度探查检查 + 占位符系统 + 待补充清单）       │
│    ↓                                                                    │
│   📌 Step 6.4  占位符审计 + 数据图代码 / 手工图表需求                      │
│    ↓                                                                    │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │              质量门（双阶段审查）                                    │   │
│   │  ⚖️ Step 6.5  证据合规审查（Review Phase 1）                                 │   │
│   │  ✨ Step 6.6  Prose Quality Gate（Review Phase 2，内化调用）                  │   │
│   │  📏 Step 6.7 Expansion Pass（内容密度检查）                           │   │
│   └──────────────────────────────────────────────────────────────────┘   │
│    ↓                                                                    │
│   ✅ Step 6.8  Self-Review & Verification                                 │
│    │                                                                    │
│   ├── passed  →  🔄 Step 7  依赖感知 Section Loop（推进下一节）          │
│   └── failed  →  ⬆️ 回到 Step 6.5 证据合规审查 重来                        │
│                                                                          │
│   📌 Abstract 后置 — 所有核心章节全部 passed 后才允许生成                  │
│   📋 Step 8  引用清单生成（**强制**，核验 >= `min_citations` 篇引用，默认 35）                │
│    ↓                                                                    │
│   🖼️ Step 9  数据图批量生成（**强制**，执行数据图代码 + 复核手工图表需求）              │
└──────────────────────────────────────────────────────────────────────────┘
```

> - 🔒 Step 1 是硬阻塞，缺少 venue/language + 本地文献库确认时不能继续
> - Step 8→Step 9→输出最终稿，两者均为强制步骤，不可跳过
> - 📐 `section-drafting` 也要走完整闭环，只是缩小证据范围
> - 🚧 Introduction / Related Work 在零 VERIFIED 引用时必须阻塞
> - ⚡ Step 2 涉及多个 probe 时**必须并行** dispatch，不得串行
> - 📋 论文完成时 Step 8 **强制**生成引用清单，核验 >= `min_citations` 篇引用（默认 35）

---

<h2 id="使用示例">💡 使用示例</h2>

### 📄 完整论文起草

```text
我有一个图神经网络项目仓库，想写一篇投 NeurIPS 的论文。
请先确认 venue 和语言，然后按 section 逐节推进，
不要一次性生成整篇。
```

### ✨ 单独润色 Method

```text
帮我把这段 Method 改成论文正文口吻，
但不要把不确定的设计动机写成已确认事实。
```

### 🔗 单独做引用核验

```text
帮我为 Introduction 找 5-8 篇 VERIFIED 引用，
并生成 Citation-to-Claim Map。
```

### 🔬 单独做实验复核

```text
先盘点这个仓库里的 checkpoint、日志和结果表，
尽量用最小可复核方式确认 Main Results。
```

---

<h2 id="适用场景">🎭 适用场景</h2>

<table>
<tr>
<td width="50%" align="center">

### ✅ 适合

</td>
<td width="50%" align="center">

### ❌ 不适合

</td>
</tr>
<tr>
<td>

- 📁 有代码仓库、实验日志、结果表、草稿、研究笔记
- 📑 需要逐节推进完整论文
- 🧩 需要区分"能写的"和"暂时不能下结论的"
- 🎛️ 希望对文献、实验、claim 强度做显式控制

</td>
<td>

- 🚫 非 CS/AI/ML 领域论文
- ⚡ 只想要一次性成稿的通用 prompt
- 🎨 纯排版 / LaTeX 调整任务
- ⚠️ 要求无视证据边界强行写成已验证结论

</td>
</tr>
</table>

---

<h2 id="文档分层">📚 文档分层</h2>

| 层级 | 文件 | 作用 |
|------|------|------|
| **战略层** | `SKILL.md` | 高层规则、触发条件、Hard Gates 摘要、数据契约、reference 导航 |
| **战术导航** | `orchestration-workflow.md` | 导航索引，指引到按阶段拆分的执行文件 |
| **战术执行** | `workflow-step-0-4.md`<br/>`workflow-step-5-6.5.md`<br/>`workflow-step-6.6-9.md` | 拆分为 3 个文件的详细执行手册，每个包含独立 dispatch 模板、step-by-step 流程、fallback 路径。**按阶段加载以节省上下文窗口** |

> 💡 **阅读建议**：改规则摘要、使用边界、导航 → 看 `SKILL.md`。改具体执行步骤、模板、失败路径 → 按 Step 阶段加载对应的 `workflow-step-*.md`。

---

<h2 id="项目结构">📁 项目结构</h2>

```text
academic-paper-writer/
├── README.md
├── LICENSE
├── .claude-plugin/                     # Claude Code 插件配置
│   ├── plugin.json                     # 插件清单
│   └── marketplace.json                # 市场定义
├── .codex/                             # Codex CLI 插件配置
│   └── skills/                         # Codex skills 目录
├── scripts/                            # 项目级工具脚本
│   └── check_schemas.py                # 跨技能 schema 一致性检查
└── skills/
    ├── shared/
    │   ├── schemas/                    # 跨技能数据契约（5 个 schema）
    │   └── references/                 # 共享概念与边界规则
    ├── academic-paper-writer/          # 📌 核心编排器
    │   ├── SKILL.md
    │   ├── agents/                     # probe agent 定义
    │   └── references/                 # 工作流（导航索引 + 3 阶段文件 + exemplars）
    ├── academic-polishing/             # ✨ 文体打磨
    ├── academic-citation/              # 🔍 文献取证
    │   ├── agents/                     # citation_agent + literature-reader-agent
    │   ├── scripts/                    # citation_audit.py + convert-pdfs-to-md.py
    │   └── references/                 # 检索策略、核验协议、引用映射、reading report schema
    ├── academic-reviser/               # ✅ 审修验证
    │   ├── agents/                     # reviser_agent
    │   ├── scripts/                    # placeholder_audit.py
    │   └── references/                 # 检查清单、Verification 判定、常见陷阱
    ├── academic-experiments/           # 🔬 实验取证
    │   ├── agents/                     # experiment_agent
    │   ├── scripts/                    # evidence_scanner.py
    │   └── references/                 # 证据盘点、运行策略、协议风险
    └── academic-figure/                # 📊 数据图生成
        ├── agents/                     # figure_agent
        ├── scripts/                    # chart_template.py + qa_figure.py
        └── references/                 # 设计理论、图表类型、QA、教程
```

### 建议阅读顺序

```
1️⃣ README.md
2️⃣ skills/academic-paper-writer/SKILL.md
3️⃣ references/orchestration-workflow.md（导航索引）
4️⃣ references/workflow-step-*.md（按 Step 阶段加载）
5️⃣ skills/shared/schemas/*
6️⃣ 你关心的子 skill SKILL.md
```

---

<h2 id="安全边界">🛡️ 安全边界</h2>

> 这个项目最重要的不是"写得快"，而是**不越界**。

| 边界 | 说明 |
|------|------|
| 🚫 不编造 | 禁止编造文献、作者、年份、venue、DOI、arXiv 编号、实验结果、图表、命令或日志 |
| ⚠️ 不混淆 | 不把 `UNVERIFIED` 文献写成 `VERIFIED`，不把 `user_claim` 写成可引用证据 |
| 📛 不夸大 | 不把内部验证包装成 `SOTA`、`generalization`、`strong evidence` |
| 📌 不静默 | 缺失信息必须显式保留 `[REF_NEEDED]`、`[RESULT_NEEDED]` 等占位符，不得静默略过 |

> 它允许输出"当前最佳草稿"，但不允许输出"伪装成已验证完成稿的草稿"。

---

<h2 id="维护与验证">🔧 维护与验证</h2>

### 版本管理

本项目使用 Git 分支和标签进行版本管理：

| 分支/标签 | 说明 | 适用场景 |
|-----------|------|----------|
| `main` | 开发分支，最新功能 | 开发者、早期用户 |
| `stable` | 稳定分支，手动合并 | 生产环境、稳定性要求高的用户 |
| `v1.0.0` 等标签 | 版本标记 | 需要锁定特定版本的用户 |

**Claude Code 用户**：
- 使用 `main` 分支：自动获取最新版本
- 使用 `stable` 分支：需要手动执行 `/plugin update` 命令

**Codex CLI 用户**：
```bash
# 切换到 stable 分支
cd ~/.agents/skills/academic-paper-writer
git checkout stable
git pull

# 切换到特定版本
git checkout v1.0.0
```

### 结构一致性检查

```bash
# 使用自动化脚本检查跨技能 schema 对齐
python scripts/check_schemas.py --skills-root ./skills
```

检查项：
- ✅ 各子 skill schema 是否指向 `shared/schemas/` 的权威版本
- ✅ 所有 debt 字段在 schema 和 SKILL.md 之间是否对齐
- ✅ SKILL.md 中引用的 reference 文件是否存在
- ✅ 步骤编号是否一致

<h2 id="参考项目">📖 参考项目</h2>

- ⚡ [superpowers](https://github.com/obra/superpowers) 
- 🌿 [nature-skills](https://github.com/Yuan1z0825/nature-skills)  
- 🎓 [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) 

### 相关文档

- 📘 [Claude Code 插件文档](https://docs.anthropic.com/en/docs/claude-code/plugins)
- 📗 [Codex CLI 文档](https://github.com/openai/codex)
- 📙 [Agent Skills 规范](https://agentskills.io)

---

## 📄 许可

[MIT License](LICENSE)

> ⚠️ **免责声明**：本项目旨在辅助学术写作的结构化与质量控制，最终论文的学术诚信、实验真实性、引用准确性与投稿合规性由使用者本人负责。
