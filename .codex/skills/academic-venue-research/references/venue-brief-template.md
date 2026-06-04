# Venue Brief Template

本文件包含 venue-brief.md 的模板格式。

---

```markdown
# Venue Brief

- Venue: {venue 名称}
- Official Source: {官方页面 URL}
- Language: {语言} [User Config]
- Min Citations: {预期引用数} [User Config]
- Fetch Timestamp: {YYYY-MM-DD HH:MM 或 Unknown}
- Source Confidence: high / medium / low

## 投稿要求

- Page Limit: {页数限制，含说明}
- Required Structure: {必需章节列表}
- Template: {模板要求}
- Anonymous Review: {是否双盲}
- Citation Format: {引用格式}
- Figure/Table Constraints: {图表数量、格式、分辨率、补充材料约束}
- Reproducibility / Artifact Expectations: {代码、数据、模型、补充材料要求}
- Appendix Policy: {附录政策}
- File Format: {文件格式要求}
- Other Requirements: {其他特殊要求}

## 写作风格备注

### 调研来源
- 调研论文数量：{数量}
- 调研论文列表：{论文标题列表}
- 调研方法：{本地文献库 / 开放获取论文 / 摘要分析}

### 论文结构偏好
- Introduction 长度：{平均段落数 / 页数}
- Introduction 组织方式：{常见结构}
- Related Work 位置：{独立章节 / Method 内 / Introduction 内}
- Related Work 组织方式：{按技术路线 / 按任务 / 按限制类型}
- Method 详细程度：{高 / 中 / 低}
- Experimental Setup 详细程度：{高 / 中 / 低}

### 写作风格偏好
- 语气：{正式 / 半正式 / 非正式}
- 用词偏好：{技术术语多 / 少 / 适中}
- 句式结构：{长句多 / 短句多 / 混合}
- 段落长度：{长段落 / 短段落 / 混合}

### 引用密度
- 平均引用数量：{数量}
- 引用格式：{数字 / 作者-年份}

### 图表使用偏好
- 平均图表数量：{数量}
- 图表类型偏好：{架构图 / 数据图 / 混合}
- 能力边界：若 venue 偏好架构图，后续只记录为 `manual_figure_needed`；`academic-figure` 不自动绘制架构图。
- 图表说明详细程度：{高 / 中 / 低}

### 各个部分的写法
- Abstract：{长度 / 结构 / 信息密度}
- Introduction：{背景介绍方式 / 问题陈述方式 / 贡献总结方式}
- Method：{详细程度 / 公式使用 / 算法描述}
- Experiments：{结果展示方式 / 分析深度}

### 逐节风格深度分析（基于 3-5 篇与项目主题最接近的同期论文）

> 以下信息提取自目标期刊中与项目研究内容最相似的 3-5 篇论文，分析其各模块内容的共性规律。

#### 相似论文清单
| # | 论文标题 | 年份 | 相似原因 |
|---|---------|------|---------|
| 1 | {title} | {year} | {共享任务/方法/数据集} |
| ... | ... | ... | ... |

#### Introduction 逻辑展开模式
- **段落级论证链**：{逐段概括论证功能（每段 1 句话）}
- **通用叙事结构**：{入选论文共同的 Intro 框架}
- **Gap 搭建方式**：{如何从已有工作过渡到 gap}
- **贡献陈述典型句式**：{收集到的典型表达}
- **高频关键短语**：{反复出现的关键词汇}

#### Related Work 组织风格
- **分组维度**：{按技术路线/任务/时间演进/其他}
- **每簇论述结构**：{共享 idea → 代表工作 → 能力 → 限制}
- **聚类粒度**：{平均工作簇数}，{每簇平均引用数}
- **区别表达方式**：{与最接近工作的区别陈述方式}
- **典型句式**：{工作簇引入/代表引用/区别陈述的句式}

#### Method 撰写深度与风格
- **公式密度**：{公式数/页数的平均值}，类型：{推导型/定义型/混合}
- **架构叙事顺序**：{从整体到局部的展开方式}
- **设计理由表述**：{入选论文解释"为什么"的方式}
- **模块边界描述**：{输入/输出/边界的界定方式}
- **典型句式**：{模块引入/设计理由/边界说明的句式}
- **常见记号风格**：{粗体/斜体/维度符号习惯}

#### Experiment 叙事结构
- **实验组织顺序**：{Setup → Results → Ablation → Analysis}
- **数据集描述粒度**：{样本量/类别分布/维度/预处理}
- **结果报告方式**：{best in bold / 单独标注 / 标准差}
- **结果解释语言**：{从数字到分析的过渡句式}
- **图表说明风格**：{标题详细程度 / 图注独立性}

#### Dataset 描述模式（若适用）
- **统计信息格式**：{文字 vs 表格呈现}
- **数据来源引用**：{公共数据集引用方式}
- **预处理深度**：{参数级别 vs 概要级别}

## 信息完整性

| 信息项 | 状态 | 来源 |
|--------|------|------|
| Page Limit | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Required Structure | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Template | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Anonymous Review | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Citation Format | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Appendix Policy | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Figure/Table Constraints | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Reproducibility / Artifact Expectations | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
```

---

## 字段说明

### 投稿要求部分

- **Page Limit**：正文页数限制，含说明（如 "8 页正文 + 不限页参考文献"）
- **Required Structure**：venue 要求的必需章节列表（如 "Abstract, Introduction, Method, Experiments, Conclusion"）
- **Template**：LaTeX/Word 模板要求（如 "使用 NeurIPS LaTeX 模板"）
- **Anonymous Review**：是否双盲（如 "是，需匿名提交"）
- **Citation Format**：引用格式（如 "数字格式 [1]" 或 "作者-年份格式 (Vaswani et al., 2017)"）
- **Appendix Policy**：附录政策（如 "允许附录，不计入页数限制"）
- **File Format**：PDF/A、文件大小限制等（如 "PDF 格式，不超过 10MB"）
- **Other Requirements**：其他特殊要求（如 "需要 Data Availability Statement"）
- **Source Confidence**：基于来源层级给出 high / medium / low。官方 guidelines/CFP/模板为 high，已录用论文观察为 medium，agent_knowledge 为 low 且必须标 unverified。
- **Figure/Table Constraints**：图表尺寸、格式、分辨率、补充材料、caption 或 source data 要求。
- **Reproducibility / Artifact Expectations**：代码、数据、模型、附录、rebuttal checklist 或 artifact 相关要求。

### 写作风格备注部分

- **调研来源**：说明调研的论文来源和数量
- **论文结构偏好**：各章节的长度、组织方式等
- **写作风格偏好**：语气、用词、句式、段落长度等
- **引用密度**：平均引用数量和引用格式
- **图表使用偏好**：图表数量、类型、说明详细程度等
- **各个部分的写法**：Abstract、Introduction、Method、Experiments 等的写法特点
- **逐节风格深度分析**：从 3-5 篇最相似论文中提取的逐节共性规律，包括：
  - 相似论文筛选标准与清单
  - Introduction 逻辑展开模式（段落论证链、gap 搭建方式、贡献句式）
  - Related Work 组织风格（分组维度、每簇结构、区别表达）
  - Method 撰写深度（公式密度、架构叙事、设计理由表述）
  - Experiment 叙事结构（实验顺序、结果报告、解释语言）
  - Dataset 描述模式（统计格式、来源引用、预处理深度）

### 信息完整性部分

- **状态**：VERIFIED（已验证）/ Unknown（未知）/ partial（部分验证）
- **来源**：信息来源（如 URL、agent_knowledge (unverified)）
