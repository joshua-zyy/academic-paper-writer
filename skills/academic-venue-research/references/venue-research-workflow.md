# Venue Research Workflow

本文件包含期刊调研的详细执行流程。

---

## Step 1: 确认调研目标与范围

1. 确认目标 venue 名称
2. 确认调研类型：
   - `full`：完整调研投稿要求和写作风格
   - `requirements`：仅调研投稿要求
   - `style`：仅调研写作风格
3. 确认是否有本地风格参考文献库（`local_style_ref_dir`）

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

### 3.1 获取论文

**优先级**：
1. 本地风格参考文献库（`local_style_ref_dir`）
2. 开放获取论文（通过 webfetch 访问 arXiv、OpenReview 等）
3. 基于摘要和已知信息进行风格分析

### 3.2 分析内容

详见 `references/style-analysis-guide.md`。

### 3.3 生成写作风格备注

按照 `references/venue-brief-template.md` 格式生成写作风格备注部分。

## Step 4: 生成 Venue Brief

1. 整合投稿要求和写作风格调研结果
2. 按照 `references/venue-brief-template.md` 格式生成 venue-brief.md 文件
3. 输出调研摘要

## 失败处理

- webfetch 无法访问官方页面 → 依次尝试：(1) 其他官方 URL (2) agent 已知知识（标注 `agent_knowledge (unverified)`）(3) 标注 Unknown 并警告用户
- 本地风格参考文献库不存在 → 跳过写作风格调研，仅调研投稿要求
- 无法获取论文原文 → 基于摘要和已知信息进行风格分析，标注分析方法
