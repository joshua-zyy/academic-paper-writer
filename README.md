# 📝 Academic Paper Writer

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/domain-CS%2FAI%2FML-brightgreen" alt="Domain">
  <img src="https://img.shields.io/badge/status-active-success" alt="Status">
</p>

面向 `CS / AI / ML` 论文写作场景的**模块化、证据驱动** Agent Skill 集合。

它不是“直接生成整篇论文”的通用 prompt，而是一套把论文写作拆成多个可验证环节的 skill system：先确认 `venue / language`，再审计证据、检索文献、复核实验、起草正文、执行 prose gate、最后做 verification。

---

## 🎯 项目定位

很多“论文写作 prompt”有三个常见问题：

1. 一次性生成整篇，容易把未核验内容写成定论
2. 文献、实验、语言润色混在一起，缺少明确职责边界
3. 缺少失败处理与降级路径，遇到证据缺口时只能硬写

这个项目把这些问题拆开处理：

- 🎯 **证据优先**：先找证据，再写主张
- 🔄 **逐节闭环**：按 section 推进，而不是一次性整篇输出
- 🤝 **模块协作**：文献、实验、审修、绘图分别由专门 skill 处理
- 🚧 **硬门控**：关键步骤不能跳过，证据不足时必须阻塞或降级
- ✅ **可验证**：用显式 schema、placeholder、verification status 管理缺口

---

## 📋 Skills 索引

| Skill | 用途 | 典型触发词 |
|-------|------|-----------|
| 🧠 `academic-paper-writer` | 核心编排器。负责完整论文起草、section loop、Hard Gates、子 skill 调度 | `写论文`、`paper draft`、`初稿` |
| ✨ `academic-polishing` | 文体润色、去 AI 化、claim 强度控制、Method 叙事强化 | `润色`、`去AI`、`claim strength` |
| 🔍 `academic-citation` | 文献检索、核验、Citation-to-Claim 映射、Exemplar Set 构建 | `找引用`、`文献检索`、`citation pass` |
| ✅ `academic-reviser` | 证据审查、三轮自审、Verification 判定 | `审修`、`self review`、`verification` |
| 🔬 `academic-experiments` | 实验证据盘点、最小可复核执行、协议风险审计 | `复核实验`、`verify results` |
| 📊 `academic-figure` | 论文图表生成：实验数据图 + 模型架构图提示词 | `绘图`、`训练曲线`、`架构图` |

---

## 🎭 适用场景

✅ **适合：**

- 📁 有代码仓库、实验日志、结果表、草稿、研究笔记中的一种或多种材料
- 📑 需要逐节推进 `Introduction / Related Work / Method / Experiments / Discussion / Conclusion`
- 🧩 需要把"能写的"和"暂时不能下结论的"内容明确区分开
- 🎛️ 希望对文献、实验、claim 强度、占位符、verification 做显式控制

❌ **不适合：**

- 🚫 非 `CS / AI / ML` 领域论文
- ⚡ 只想要一个"一次性成稿"的通用 prompt
- 🎨 纯排版/LaTeX 调整任务
- ⚠️ 明确要求无视证据边界、强行写成已验证结论的场景

---

## 🏗️ 核心设计

### 1. 🔍 证据优先，逐节闭环

每一节都不是“写完就算完”，而是经历固定闭环：

`Draft -> Evidence Review -> Prose Gate -> Expansion -> Self-Review -> Verification`

- 初稿可以带占位符
- 但占位符必须被记录、审计和追踪
- `Verification` 未通过时不能假装通过

### 2. 🧩 Core + Subskills 架构

核心编排器负责：

- 判断任务模式
- 确认 `venue / language`
- 组织 section queue
- 维护 cumulative draft
- 吸收子 skill 的专项结果

子 skills 负责专项任务：

| Core 环节 | 委托 Skill |
|-----------|-----------|
| 🔍 文献检索与核验 | `academic-citation` |
| 🔬 实验证据复核 | `academic-experiments` |
| 📊 图表 / 架构图 | `academic-figure` |
| ✨ Prose Quality Gate | `academic-polishing` |
| ✅ 证据审查与 Verification | `academic-reviser` |

### 3. 🚧 Hard Gates + 数据契约

跨 skill 交换不是自由文本，而是通过显式数据契约进行：

- 📦 `Evidence Inventory`
- ✅ `Verified References`
- 📋 `Verification Report`

核心编排器还维护 3 道不可跳过的门控：

- 🅰️ **Gate A**：当前节是否有足够证据可写
- 🅱️ **Gate B**：当前节是否有足够可用引用
- 🚪 **Gate C**：当前节是否通过 verification，能否推进到下一节

---

## 📚 文档分层

这个仓库采用了两层核心文档：

- `skills/academic-paper-writer/SKILL.md`
  作用：高层规则、触发条件、Hard Gates 摘要、数据契约、reference 导航

- `skills/academic-paper-writer/references/orchestration-workflow.md`
  作用：唯一的详细执行手册，包含 dispatch 模板、step-by-step 流程、fallback 路径、verification 细则

- 改“规则摘要、使用边界、导航”优先看 `SKILL.md`
- 改“具体执行步骤、模板、失败路径”优先看 `orchestration-workflow.md`

---

## 📁 项目结构

README 只保留高层目录，避免和文件级细节长期漂移：

```text
academic-paper-writer/
├── README.md
├── LICENSE
└── skills/
    ├── shared/
    │   ├── schemas/        # 跨技能数据契约
    │   ├── references/     # 共享概念与边界规则
    │   └── templates/      # 通用输出模板
    ├── academic-paper-writer/
    │   ├── SKILL.md
    │   ├── agents/
    │   └── references/
    ├── academic-polishing/
    ├── academic-citation/
    ├── academic-reviser/
    ├── academic-experiments/
    └── academic-figure/
```

建议按这个顺序读：

1. 👉 `README.md`
2. 👉 `skills/academic-paper-writer/SKILL.md`
3. 👉 `skills/academic-paper-writer/references/orchestration-workflow.md`
4. 👉 `skills/shared/schemas/*`
5. 👉 你关心的子 skill `SKILL.md`

---

## 🚀 快速开始

### 1. 📦 获取仓库

```bash
git clone https://github.com/joshua-zyy/academic-paper-writer.git
```

### 2. 🔌 在支持 Skill 机制的 Agent 平台中加载

本项目本身不依赖额外 Python 包或 Node 运行时；它的主要内容是 skill 文档、reference、schema 和少量辅助脚本。

常见使用方式：

- **完整论文工作流**：加载 `skills/academic-paper-writer/SKILL.md`
- **单一专项任务**：直接加载对应子 skill 的 `SKILL.md`

### 3. 📝 准备输入材料

越完整的输入，skill 的表现越稳定。常见输入包括：

- 📂 代码仓库路径
- 🏛️ 目标会议 / 期刊
- 🌐 写作语言
- 📊 现有实验日志、CSV、结果表、checkpoint
- 📄 现有草稿或 outline
- 📝 研究摘要 / 贡献点草稿

---

## 💡 使用示例

### 📄 完整论文起草

```text
我有一个图神经网络项目仓库，想写一篇投 NeurIPS 的论文。
请先确认 venue 和语言，然后按 section 逐节推进，不要一次性生成整篇。
```

### ✨ 单独润色 Method

```text
帮我把这段 Method 改成论文正文口吻，但不要把不确定的设计动机写成已确认事实。
```

### 🔗 单独做引用核验

```text
帮我为 Introduction 找 5-8 篇 VERIFIED 引用，并生成 Citation-to-Claim Map。
```

### 🔬 单独做实验复核

```text
先盘点这个仓库里的 checkpoint、日志和结果表，尽量用最小可复核方式确认 Main Results。
```

---

## 🔄 编排器核心工作流

```text
Step  0 🎯 判定任务模式
Step  1 🔒 确认 venue / 语言（Blocking Gate）
Step  2 🔍 审计当前节证据
Step  3 📚 文献检索与核验
Step  4 🔬 实验事实复核
Step  5 🧩 生成 Section Blueprint / Method Blueprint
Step  6 ✏️ 起草 Draft v1（含占位符系统）
Step  7 📌 占位符审计 + 架构图预生成
Step  8 ⚖️ 证据合规审查
Step  9 ✨ Prose Quality Gate
Step 10 📏 Expansion Pass（内容密度检查）
Step 11 ✅ Self-Review & Verification
Step 12 🔄 整合 & 依赖感知 Section Loop
```

说明：

- 🔒 `Step 1` 是硬阻塞，缺少 `venue / language` 时不能继续
- 📐 `section-drafting` 也要走完整闭环，只是缩小证据范围
- 🚧 `Introduction / Related Work` 在零 `VERIFIED` 引用时必须阻塞，不能只靠 `[REF_NEEDED]` 直接起草

---

## 🛡️ 安全边界

这个项目最重要的不是“写得快”，而是“不越界”。

核心边界包括：

- 🚫 不编造文献、实验结果、图表、命令或日志
- ⚠️ 不把 `UNVERIFIED` 文献写成 `VERIFIED`
- 🧪 不把 `user_claim` 写成可直接引用的证据
- 📛 不把内部验证包装成 `SOTA`、`generalization`、`strong evidence`
- 📌 缺失信息必须显式保留 placeholder，而不是静默略过

它允许输出“当前最佳草稿”，但不允许输出“伪装成已验证完成稿的草稿”。

---

## 🔧 维护与验证

### 1. 🔗 结构一致性检查

重点确认：

- 🔢 `README.md`、`SKILL.md`、`orchestration-workflow.md` 的步骤编号一致
- ⚡ Core 与子 skill 的 dispatch 架构没有冲突
- 🔗 shared schema 的生产者 / 消费者关系仍闭合

### 2. 💪 压力场景验证

至少跑下面几类场景：

- 📄 `Introduction` 文献不足
- 🧠 `Method` 设计动机无法稳定恢复
- 📊 `Results` 只能使用 `preexisting_artifact`

建议检查：

- ✅ 是否正确阻塞或降级
- 📌 是否保留必要 placeholder
- ⚠️ 是否错误放行强结论
- 📋 `Verification Status` 是否与规则一致

参考：`skills/academic-paper-writer/references/test-scenarios.md`

---

## 📖 参考项目

1. ⚡ [superpowers](https://github.com/obra/superpowers)
2. 🌿 [nature-skills](https://github.com/Yuan1z0825/nature-skills)
3. 🎓 [academic-research-skills](https://github.com/Imbad0202/academic-research-skills)

## 📄 许可

[MIT License](LICENSE)

> **免责声明**：本项目旨在辅助学术写作的结构化与质量控制，最终论文的学术诚信、实验真实性、引用准确性与投稿合规性由使用者本人负责。
