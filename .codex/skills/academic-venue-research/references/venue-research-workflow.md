# Venue Research Workflow

本文件包含期刊调研的详细执行流程。

---

## Step 1: 确认调研目标与范围

1. 确认目标 venue 名称
2. 确认调研类型：
   - `full`：完整调研投稿要求和写作风格
   - `requirements`：仅调研投稿要求
   - `style`：仅调研写作风格
3. 确认是否有本地风格参考文献库 MD 输出目录（`local_style_md_dir`）

## Step 2: 调研投稿要求

### 2.1 判断 venue 类型

- 知名 venue（如 NeurIPS、CVPR、ICLR、AAAI、IEEE T-PAMI、Nature、Science 等）→ 可直接使用已知要求，但仍需用 webfetch 标注信息来源
- 其他 venue → 必须用 webfetch 访问官方页面

### 2.2 使用 webfetch 获取官方信息

1. 构造搜索目标时**必须包含投稿年份**：`{venue_name} {year} author guidelines` 或 `{venue_name} {year} call for papers`
2. 若用户未指定投稿年份，使用当前年份
3. 使用 webfetch 访问最可能的官方页面
4. 若首次访问未找到，尝试 `submission guidelines` / `paper format` / `camera ready instructions` 等变体

**降级策略**（webfetch 失败时）：
- webfetch 返回空内容或无法访问 → 尝试其他可能的官方 URL
- 所有 URL 均失败 → 使用 agent 已知的 venue 知识（如有），并在信息完整性表中标注 `source: agent_knowledge (unverified)`
- agent 无相关知识 → 标注 Unknown，警告用户"未能获取官方信息，建议手动确认"

### 2.3 提取以下信息（按优先级）

| 信息项 | 必需/可选 | 说明 |
|--------|----------|------|
| Page Limit | 必需 | 正文页数限制（含/不含参考文献、附录） |
| Required Structure | 必需 | venue 要求的必需章节（如 Abstract 必须、Keywords 必须等） |
| Template | 必需 | LaTeX/Word 模板要求 |
| Anonymous Review | 必需 | 是否双盲 |
| Citation Format | 必需 | 引用格式（数字/作者-年份） |
| Appendix Policy | 可选 | 附录政策 |
| File Format | 可选 | PDF/A、文件大小限制等 |
| Other Requirements | 可选 | 其他特殊要求（如 data availability statement 等） |

## Step 3: 调研写作风格

### 3a. 筛选与研究主题最接近的同期论文（强制前置步骤）

**输入**: `project_keywords`（5-8 个关键词）、`project_description`（一句话摘要）、`local_style_md_dir`（可选）

1. **从本地风格文献库搜索**（若 `local_style_md_dir` 存在）：
   - 读取 `<local_style_md_dir>/_index_style.json`
   - 在每个条目的 `title` 和 `first_500_chars` 字段中匹配 `project_keywords`
   - 至少匹配 2 个关键词的条目视为候选
   - 匹配多个关键词的条目优先排序
2. **从 webfetch 获取**（若无本地风格文献库）：
   - webfetch 目标期刊最新（近 2 年）论文列表
   - 通过标题和摘要与 `project_keywords` 进行关键词匹配筛选
3. 从候选中选择 **3-5 篇最相似的论文**：
   - 优先：任务相同 + 方法家族相同
   - 次选：任务相同 + 方法家族不同
   - 补充：任务不同 + 方法家族相同
4. 对每篇入选论文标注相似度原因（共享任务/方法/数据集中的哪几项）
5. 若无法从同期刊找到足够相似论文 → 扩展至同领域顶会/顶刊，标注 `source_venue: different`

### 3b. 执行逐节深度风格分析

对 Step 3a 筛选出的 3-5 篇论文，按 `references/style-analysis-guide.md` 第 6 节执行逐节深度分析：

1. Introduction 深度分析：段落级逻辑链、逻辑展开模式、gap 搭建方式、贡献陈述句式、段落过渡规律、高频短语
2. Related Work 深度分析：工作簇分组逻辑、每簇论述结构、聚类粒度、区别点表达方式
3. Method 深度分析：公式密度、架构叙事顺序、设计理由表述、模块边界描述、常见记号风格
4. Experiments 深度分析：实验叙事结构、数据集描述模式、基线选择、结果报告方式、消融设计、解释语言、图表说明风格
5. Dataset 描述模式（若适用）

### 3c. 生成写作风格备注

按照 `references/venue-brief-template.md` 格式生成写作风格备注部分，包括"逐节风格深度分析" section。

## Step 4: 生成 Venue Brief

1. 整合投稿要求和写作风格调研结果
2. 按照 `references/venue-brief-template.md` 格式生成 venue-brief.md 文件
3. 输出调研摘要

## 失败处理

- webfetch 无法访问官方页面 → 依次尝试：(1) 其他官方 URL (2) agent 已知知识（标注 `agent_knowledge (unverified)`）(3) 标注 Unknown 并警告用户
- 本地风格参考文献库不存在 → 跳过写作风格调研，仅调研投稿要求
- 无法获取论文原文 → 基于摘要和已知信息进行风格分析，标注分析方法
