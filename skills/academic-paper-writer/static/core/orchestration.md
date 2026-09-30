# 协作控制

## 派发

首次盘点按材料划分独立任务：方法实现与设计材料、实验设置与结果、参考文献；已知 venue 按需附加调研。同一来源指定负责人，避免 citation 与 probe 重复读完整库。

每个任务说明 question、已有 evidence_ids、允许读取范围、输出契约、禁止操作、需要返回的具体定位。任务失败只影响依赖它的事实，不重新 intake 或创建替代论文任务。支持并行时并行独立工作，不支持时串行降级且如实告知，不虚构 subagent。

## 角色

主 agent 主张/主线确认、正文、修订、合并。探查者取证。academic-reviser 单一验收角色，不改正文。academic-polishing 主笔内化。academic-figure 在分配路径生成数据图。

## 推进

默认 auto，step-by-step 每节处理完暂停。缺材料时记录框架与补充建议，继续独立章节；事实冲突不能猜，向作者集中确认。重大主张变化或高成本补证交作者选择。

论文起草前确认主线；交付前报告等级与重大未解决项。明确验收缺陷须修复或如实保留，不把接受交付写成验收通过。

章节 ID 统一：introduction、related_work、method、experimental_setup、results、discussion、conclusion、abstract。消融是 results 子单元，按材料可选，不是 Discussion 的硬前置。

## 持久化

主 agent 保存证据记录与必要 task_state；恢复先验证同一根目录、已确认选择、当前正文和受影响来源。只重做缺失或失效部分；状态标记不替代实际文件核对。
