# Academic Paper Writer

面向 CS / AI / ML 领域的**模块化、证据驱动**论文写作 Agent Skill 集合。将论文写作拆分为 6 个独立子 Skill：编排核心、文体润色、文献引用、审修验证、实验复核、论文绘图。每个子 Skill 可独立触发使用，也可由编排核心串联为完整写作流程。

---

## Skills 索引

| Skill | 用途 | 触发词示例 |
|-------|------|-----------|
| `academic-paper-writer` | 全文编排：确认 venue → 审计证据 → 起草 → 质量闸门 → 审修 → 集成 | "写论文"、"paper draft"、"初稿" |
| `academic-polishing` | 文体润色：去 AI 化改写、Claim 强度控制、Method 叙事强化 | "润色"、"去AI"、"降 claim 强度" |
| `academic-citation` | 文献引用：检索、核验、Citation-to-Claim 映射、Exemplar Set 构建 | "找引用"、"文献检索"、"citation pass" |
| `academic-reviser` | 审修验证：三轮自审（证据→论证→风格）、Verification 判定 | "审修"、"self review"、"verification" |
| `academic-experiments` | 实验复核：证据盘点、最小可复核执行、协议风险审计 | "复核实验"、"verify results" |
| `academic-figure` | 论文绘图：实验数据图（Python 自动出图） + 模型架构图（生图提示词） | "绘图"、"画图"、"架构图"、"训练曲线" |

---

## 核心设计

**证据优先，逐节闭环** — 每节经历 `Draft → Quality Gate → Expansion → Self-Review → Revision → Verification`。

**模块独立，可编排** — 六个 Skill 各有独立触发词和完整 references/，由 core 在关键步骤委托调度：

| Core Step | 委托 Skill |
|-----------|-----------|
| 文献检索与核验 | `academic-citation` |
| 实验事实复核 | `academic-experiments` |
| 实验图表生成（可选） | `academic-figure` |
| Prose 质量闸门 | `academic-polishing` |
| 自我审查与 Verification | `academic-reviser` |

**Red Lines + Traffic Light** — 每个 Skill 定义显式禁止项（Red Lines）和 AI 介入边界（Traffic Light），确保输出不越过证据边界。

**数据契约 + 硬门控** — 跨技能交换遵循规范化 Schema（Evidence Inventory / Verified References / Verification Report），核心编排器设有 3 道不可跳过的完整性门控。详见 `skills/shared/`。

---

## 项目结构

```
academic-paper-writer/
├── README.md
├── LICENSE
├── skills/
│   ├── shared/                       # 跨技能共享层
│   │   ├── schemas/
│   │   │   ├── evidence-inventory.md
│   │   │   ├── verified-references.md
│   │   │   └── verification-report.md
│   │   ├── references/
│   │   │   ├── evidence-classification.md
│   │   │   ├── placeholder-guide.md
│   │   │   ├── paper-types.md
│   │   │   ├── mode-spectrum.md
│   │   │   └── data-access-levels.md
│   │   └── templates/
│   │       └── section-critique.md
│   ├── academic-paper-writer/         # 核心编排器
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── agents/openai.yaml
│   │   └── references/
    │       ├── paper-structure.md
    │       ├── writing-guidelines.md
    │       ├── iteration-control.md
    │       ├── content-density.md
    │       ├── test-scenarios.md
    │       └── exemplar-sections/
    ├── academic-polishing/           # 文体润色
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── agents/polishing_agent.md
    │   └── references/
    │       ├── de-ai-patterns.md
    │       ├── claim-strength.md
    │       └── method-narrative.md
    ├── academic-citation/            # 文献引用
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── agents/citation_agent.md
    │   └── references/
    │       ├── search-strategy.md
    │       ├── verification-protocol.md
    │       └── citation-mapping.md
    ├── academic-reviser/             # 审修验证
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── agents/reviser_agent.md
    │   └── references/
    │       ├── revision-checklist.md
    │       ├── verification-status.md
    │       └── common-pitfalls.md
    ├── academic-experiments/         # 实验复核
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── agents/experiment_agent.md
    │   └── references/
    │       ├── evidence-inventory.md
    │       ├── run-strategy.md
    │       └── protocol-risks.md
    └── academic-figure/              # 论文绘图
        ├── SKILL.md
        ├── README.md
        ├── agents/figure_agent.md
        └── references/
            ├── api.md
            ├── chart-types.md
            ├── design-theory.md
            ├── architecture-prompting.md
            ├── figure-contract.md
            ├── qa-contract.md
            └── tutorials.md
```

---

## 快速开始

### 安装

本 Skill 集合无需额外依赖，可直接集成到支持 Skill 机制的 LLM Agent 平台。

```bash
git clone https://github.com/joshua-zyy/academic-paper-writer.git
```

根据你使用的平台，在 Agent 配置中引用对应 `skills/<name>/SKILL.md`。

### 使用方式

**完整论文起草**（触发 `academic-paper-writer`，自动协调子 Skill）：

> "我有一个关于图神经网络的代码仓库，想写一篇投 NeurIPS 的论文，先帮我规划大纲，然后逐节推进。"

**独立使用子 Skill**：

> "帮我把这段 Method 润色成论文口吻" → `academic-polishing`
> "帮我找几篇关于 ViT 医学图像的引用" → `academic-citation`
> "帮我 self review 这节 Introduction" → `academic-reviser`
> "帮我盘点这个仓库的实验产物" → `academic-experiments`
> "根据这个 CSV 画训练曲线对比图" → `academic-figure`

---

## 核心工作流（编排器）

```
Step 0  判定任务模式
Step 1  确认 venue / 语言（Blocking Gate：缺失则停等）
Step 2  审计当前节证据
Step 3  文献检索与核验 → 委托 academic-citation
Step 4  实验事实复核 → 委托 academic-experiments
Step 4.5 实验图表生成（可选） → 委托 academic-figure
Step 5  生成 Section Blueprint / Method Blueprint
Step 6  起草 Draft v1（含占位符系统）
Step 7  Prose Quality Gate → 委托 academic-polishing
Step 8  Expansion Pass（内容密度检查）
Step 9  Self-Review & Verification → 委托 academic-reviser
Step 10 整合 & 继续 Section Loop
```

---

## 参考

1. [nature-skills](https://github.com/Yuan1z0825/nature-skills)（袁一哲，上海交通大学）
2. [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) 

## 许可

[MIT License](LICENSE)

> **免责声明**：本 Skill 旨在辅助学术写作的结构化与质量控制，最终论文的学术诚信、实验真实性与引用准确性由使用者本人负责。
