# Academic Citation

独立可用的文献检索、核验与引用映射技能。适用于 CS/AI/ML 学术论文写作中的引用管理。

## 触发方式

直接描述需求即可触发：

- "帮我找几篇关于 graph transformer 的引用"
- "核验这篇论文的参考文献"
- "为 Introduction 建立 exemplar set"
- "citation pass for related work"

## 核心能力

| 能力 | 说明 |
|------|------|
| 多轮文献检索 | 四类查询策略（问题导向/方法导向/基线导向/时间导向） |
| 元数据核验 | VERIFIED/UNVERIFIED 分级，一级来源优先 |
| Exemplar Set 构建 | 学习同领域论文的章节组织与论证模式 |
| Citation-to-Claim 映射 | 每条引用与正文主张的精确对应 |
| 引用格式一致性 | 确保 inline citation 与 bibliography 闭合 |

## 与其他 Skill 的关系

- 被 `academic-paper-writer` 在 Step 3（文献检索与核验）中委托调用
- 可独立使用于任何需要文献检索核验的场景
