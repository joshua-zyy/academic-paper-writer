# 写作风格适配与证据优先级指南（精简版）

## 目录

- 使用定位
- 工具与信息来源
- 证据分层
- Venue / Language Brief 的最小内容
- 没有目标 venue 时的默认写法
- 风格适配的失败处理
- 与草稿生成的边界

## 使用定位

本文件用于两件事：
- 当用户提供目标会议/期刊时，生成简短、可审计的 Venue / Language Brief
- 在写作与修订阶段辅助 venue 风格适配

注意：
- 风格适配是增强项，不是主流程中心。
- 若用户没有提供目标会议/期刊，且当前任务已进入论文起草或正式章节写作，应先追问。
- 若风格信息与官方规则冲突，以官方规则为准。

---

## 1. 工具与信息来源

当需要做目标会议/期刊适配时，使用 web 检索确认少量高价值事实：
- 论文章节结构与必需组成部分
- 投稿规则
- 模板要求
- 页数限制
- 匿名要求
- 官方语言与格式偏好

---

## 2. 证据分层

### 一级证据：强约束来源（定义 venue 规则）
- 官方 CFP 页面
- 官方 author guidelines
- 官方 LaTeX / Word 模板说明
- 官方 submission instructions

这些信息可决定：页数限制、附录政策、匿名要求、模板要求、提交格式。

### 二级证据：风格样本来源（观察写作风格，不能覆盖一级规则）
- 官方 proceedings
- 已录用论文
- 最佳论文或代表性论文

辅助判断：Abstract 常见写法、Introduction 组织方式、Related Work 常见位置、Experiments 展开密度、图表使用习惯。

### 三级证据：弱参考来源（仅作辅助线索）
- 博客总结、经验帖、非官方模板解读

三级证据不能定义 venue 规范，不能覆盖一级或二级信息。若与官方页面冲突，直接丢弃。

---

## 3. Venue / Language Brief 的最小内容

```md
## Venue / Language Brief

- Venue:
- Official Source:
- Required Structure:
- Page Limit:
- Appendix Policy:
- Anonymous Review:
- Template:
- Language:
- Preferred Structure Notes:
- Writing Tone Notes:
```

说明：
- Official Source 必须指向官方页面或官方模板说明。
- Required Structure 要写成可执行的章节顺序。
- Preferred Structure Notes 只写高价值差异。
- 如果某项未确认，写 Unknown，不要猜。

---

## 4. 没有目标 venue 时的默认写法

若未提供目标会议/期刊：
- 对论文起草或正式章节写作，先追问用户的目标 venue
- 对论文起草或正式章节写作，若本轮语言未知，也先追问语言
- 若用户仍不给出或明确让代理决定，再默认使用通用 CS/AI 论文结构
- 默认英文写作；若用户明确要求中文，则使用中文
- 不生成 venue-specific 约束
- 不假设页数、匿名、模板要求

---

## 5. 风格适配的失败处理

若官方页面无法确认关键信息：
- 明确写出 Unknown
- 使用通用 CS/AI 结构继续生成大纲和草稿
- 不得因为需要完成 Style Brief 而引用二手页面强行补齐规则

---

## 6. 与草稿生成的边界

风格适配只能影响：大纲组织、语气与表达方式、是否保留某些常见章节。

风格适配不能越权影响：实验结果真实性、引用真实性、图表是否已存在、结论强度是否与证据匹配。

换言之，Style Brief 可以改变"怎么写"，不能改变"有没有事实依据"。

---

## 7. Two-Stage Writing

### 何时使用 bullet points

Bullet points **仅用于** Step 5 Blueprint 阶段，作为规划工具组织论点结构和论证顺序。

### 如何转换 bullet → prose

1. 将每个 bullet point 转换为一个完整句子（主语 + 谓语 + 宾语）
2. 在句子之间添加过渡词，建立因果、递进、转折或并列关系
3. 将 citation 标注自然融入句子中，而非作为列表项
4. 扩展 bullet 中省略的上下文和解释

### 常见错误

- **把提纲当正文**：Draft v1 中残留 bullet points 或提纲式短句
- **bullet 残留**：使用破折号或星号开头的短句段落
- **缺少过渡**：句子之间只靠连接词维持表面连贯，缺少深层逻辑
- **citation 列表化**：将引用作为独立列表项而非融入 prose
