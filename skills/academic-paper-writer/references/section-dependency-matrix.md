# 跨节影响关系

本表用于已写内容的增量复查，不是起草前置 DAG。按材料可先写有依据的部分，abstract 通常后置。

| 来源章节 ID | 变化内容 | 回查已有部分 |
|---|---|---|
| introduction | 问题、贡献、主线 | related_work, discussion, conclusion, abstract |
| related_work | 方法定位、引文支持 | introduction, method, discussion |
| method | 操作、模块、作者设计意图 | introduction, experimental_setup, results, discussion, conclusion, abstract |
| experimental_setup | 数据、协议、指标口径 | results, discussion, conclusion, abstract |
| results | 核心数字、比较、可选消融 | introduction, discussion, conclusion, abstract |
| discussion | 解释、贡献边界 | introduction, conclusion, abstract |
| conclusion | 总结主张 | abstract |
| abstract | 主体未出现的新内容 | 不直接传播；回查相应主体来源并修摘要 |

消融属于 results 子单元，不强制存在。Related Work 可合并入 Introduction；不存在的章节不创建依赖。主笔记录发生变化的具体 claim/evidence ID，标记关联已写部分 recheck_pending。只改语法无需重新探查。
