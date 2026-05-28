# Venue Brief Template

本文件包含 venue-brief.md 的模板格式。

---

```markdown
# Venue Brief

- Venue: {venue 名称}
- Official Source: {官方页面 URL}
- Language: {语言} [User Config]
- Min Citations: {预期引用数} [User Config]

## 投稿要求

- Page Limit: {页数限制，含说明}
- Required Structure: {必需章节列表}
- Template: {模板要求}
- Anonymous Review: {是否双盲}
- Citation Format: {引用格式}
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
- 图表说明详细程度：{高 / 中 / 低}

### 各个部分的写法
- Abstract：{长度 / 结构 / 信息密度}
- Introduction：{背景介绍方式 / 问题陈述方式 / 贡献总结方式}
- Method：{详细程度 / 公式使用 / 算法描述}
- Experiments：{结果展示方式 / 分析深度}

## 信息完整性

| 信息项 | 状态 | 来源 |
|--------|------|------|
| Page Limit | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Required Structure | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Template | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Anonymous Review | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Citation Format | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
| Appendix Policy | VERIFIED / Unknown | {URL 或 agent_knowledge (unverified)} |
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

### 写作风格备注部分

- **调研来源**：说明调研的论文来源和数量
- **论文结构偏好**：各章节的长度、组织方式等
- **写作风格偏好**：语气、用词、句式、段落长度等
- **引用密度**：平均引用数量和引用格式
- **图表使用偏好**：图表数量、类型、说明详细程度等
- **各个部分的写法**：Abstract、Introduction、Method、Experiments 等的写法特点

### 信息完整性部分

- **状态**：VERIFIED（已验证）/ Unknown（未知）/ partial（部分验证）
- **来源**：信息来源（如 URL、agent_knowledge (unverified)）
