# Section Moves (CS/AI/ML)

用于执行 Prose Quality Gate 时提供 phrase 级别和 move 级别的写作参考。本文提供各章节的推荐 move order 和 phrase families，不涉及论文的整体写作策略。

源自 Academic Phrasebank，针对 CS/AI/ML 的会议和期刊写作惯例进行了适配。注意 CS 会议（NeurIPS, ICML, CVPR, ICLR, ACL 等）和 CS 期刊（TPAMI, IJCV, JMLR 等）在结构、节奏和审稿人预期上与 Nature 风格论文存在系统性差异。

## Introduction

本段必须回答的问题：

1. 研究问题域是什么，为什么重要？
2. 具体的技术挑战或瓶颈是什么？
3. 已有方法尝试了什么、哪里有不足？
4. 你的方法大致是什么、关键结果如何？
5. 具体贡献有哪些？

**CS 会议注记：** 多数顶会要求 Introduction 包含 mini-results（关键数值），让审稿人立即评估工作价值。与 Nature 不同，CS 会议的 Introduction 通常更长（1-2 页），且常有显式的 contribution bullet-point 列表。

推荐的 move order（CS 会议风格）：

1. 建立领域重要性
2. 指出具体未解决的技术挑战
3. 简要总结已有方法及其局限
4. 勾勒你的方法和关键结果
5. 显式列出 contributions（通常 3-4 条）
6. 可选：论文 roadmap 句

Useful phrase families:

- `Despite significant progress, ... remains a challenging problem due to ...`
- `Existing methods suffer from ... , limiting their applicability to ...`
- `In this paper, we propose ... , a novel framework that ...`
- `Our method achieves ... on ..., outperforming ... by ...`
- `We make the following contributions: (i) ... (ii) ... (iii) ...`
- `Extensive experiments on ... demonstrate that ...`
- `To the best of our knowledge, this is the first work to ...`

避免：

- 把贡献埋在最后一段（审稿人常在前面就停止阅读）
- 把微小的 engineering 改动列为贡献
- 无具体数值支撑就宣布结果
- 空洞的问题动机，缺少对已有方法的具体失败分析

## Related Work

本段必须回答的问题：

1. 该领域有哪些类别的已有工作？
2. 每类工作的核心贡献和关键局限是什么？
3. 你的方法相对于每类工作的定位在哪里？

CS 的 Related Work 通常比 Nature 风格更长、更技术化。它承担双重职责：(a) 把你的工作与具体 baselines 进行对比定位，(b) 展示你的技术深度。

推荐的 move order：

1. 将已有工作组织为 3-4 个主题组或方法类别
2. 对每组：陈述核心思路 → 代表性方法 → 主要成就 → 共有的局限
3. 显式说明你的方法在每个类别上的差异和改进
4. 以 positioning 句收尾，使 gap 具体化

Useful phrase families:

- `Existing approaches to ... can be broadly categorized into ...`
- `A line of work ... focuses on ...`
- `For example, [author] proposed ... which ...`
- `However, these methods share a common limitation: ...`
- `In contrast to these approaches, our method ...`
- `Most related to our work is ... , which ... differs from our approach in that ...`
- `A key distinction between our method and prior work is ...`

避免：

- 按时间顺序而非按主题组织论文
- citation bomb（"[1,2,3,4,5,6,7,8,9,10]"）且无综合归纳
- 声称方法"完全不同"但实际上只是已有技术的变体
- 遗漏最接近的 baselines（审稿人会注意到）

## Method

本段必须回答的问题：

1. 问题的数学形式化是什么？
2. 整体的 architecture / pipeline 是什么？
3. 每个 component 如何工作、为什么这样设计？
4. 模型如何训练、目标函数是什么？
5. 测试阶段的 inference 如何执行？

CS/AI/ML 的 Method 以 architecture 为中心。与湿实验描述实验协议不同，你是在描述一个人工设计的系统。每个设计选择都必须有 rationale。

推荐的 move order：

1. problem formulation：定义 notation、input/output 空间、关键变量
2. architecture overview：高层 diagram 引用 + 整体 pipeline 叙述
3. component-level description：按 **解决什么 gap → 设计 rationale → mechanism → formula → training behavior → boundary** 的顺序叙述每个模块
4. training objective：loss function(s)、regularization、优化细节
5. inference procedure：forward pass、post-processing、prediction aggregation
6. 可选：theoretical analysis（复杂度、收敛性、generalization bound）

每个 component 的叙事模式：

1. "为缓解 [具体问题/瓶颈]，我们设计了 [组件名称]。"
2. "关键点在于 ..."（为什么能 work）
3. "形式上，..."（数学描述）
4. "该设计的一个优势是 ..."（预期收益）
5. "一个局限是 ..."（边界/代价）

Useful phrase families:

- `Formally, let ... denote ...`
- `We formulate the problem as ...`
- `The overall architecture consists of three main components: ...`
- `To capture ..., we introduce a ... module that ...`
- `The objective function is defined as ...`
- `We optimize ... using ... with learning rate ...`
- `During inference, ...`
- `The computational complexity is ... , which is comparable to ...`

避免：

- 在正文中罗列 architecture（应放图中）
- 像 log 一样罗列层（"conv3x3 → ReLU → BN → conv3x3 → ReLU"）
- 遗漏 loss function 或训练细节
- code walkthrough 语气（"我们定义了一个继承自...的类"）
- 给标准构建块套上新的命名并声称"新颖性"

## Experimental Setup

本段必须回答的问题：

1. 用了什么 dataset、关键统计量是什么（规模、划分、领域）？
2. 用什么 metrics 评估、为什么？
3. 比较了哪些 baselines、是否进行了公平调参？
4. 实现细节是什么（硬件、框架、超参数）？

推荐的 move order：

1. dataset specifications：benchmark 来源、preprocessing、train/val/test 划分、data augmentation
2. evaluation metrics：主 metric、副 metrics、显著性报告方式
3. baselines：哪些方法、官方实现或复现、调参协议
4. 实现细节：framework、硬件（GPU 型号、内存）、训练预算、超参数搜索
5. 可选：评估协议细节（cross-validation、多 random seeds、多次运行）

Useful phrase families:

- `We evaluate our method on ... benchmark, which consists of ...`
- `Following standard practice, we use ... as the evaluation metric.`
- `We compare against the following baselines: ...`
- `For fair comparison, all baselines are tuned using the same protocol.`
- `All models are implemented in ... and trained on ... GPUs.`
- `We report the mean and standard deviation over ... random seeds.`

避免：

- 遗漏 dataset 统计信息（样本数、类别分布、图像分辨率）
- 用私有数据评估且未充分说明理由
- 对比调参不充分的 baselines
- 选择对自己有利但偏离社区标准的 metrics

## Results

本段必须回答的问题：

1. 与 baselines 相比，主要的定量结果是什么？
2. 方法的每个 component 是否如预期那样贡献了效果（ablation）？
3. 在不同条件下方法表现如何（参数敏感性）？
4. 定性示例展示了什么？
5. 计算代价如何？

在 CS/AI/ML 中，Results 通常由一系列实验组成，每个实验回答一个特定问题，常组织为子节。

推荐的 move order：

1. **main comparison：** 表格展示你的方法和所有 baselines 在所有 metrics 上的结果 → 标出最佳 → 评述模式
2. **ablation studies：** 移除/替换每个 component → 展示性能下降 → 验证设计选择
3. **parameter analysis：** 改变关键超参数 → 展示敏感性曲线或表格
4. **qualitative results：** 示例输出 + 评述方法做对了什么、做错了什么
5. **computational analysis：** 训练时间、inference 速度、模型规模 vs 性能的 trade-off

Useful phrase families:

- `Table X reports the main comparison results. Our method achieves ... , outperforming ...`
- `To verify the effectiveness of ..., we conduct an ablation study by ...`
- `Removing ... leads to a drop of ... , confirming its importance.`
- `We analyze the sensitivity of ... by varying ... from ... to ...`
- `Figure X shows qualitative examples. Our method produces ... while baselines ...`
- `In terms of computational cost, our method requires ... , which is ...`
- `Interestingly, we observe that ... , which suggests ...`

避免：

- 在某个 metric 上宣称最优但忽略了在其他 metrics 上的劣势
- 只在一个 dataset 或一个 seed 上做 ablation
- 挑出对己有利的定性示例（cherry-picking）
- 未做统计显著性检验就得出结论
- 比较 runtime 时未控制硬件和实现质量

## Discussion / Limitations

本段必须回答的问题：

1. 结果在数字之外意味着什么？
2. 方法在什么情况下会失败、为什么？
3. 有什么实际约束（数据、算力、领域范围）？
4. broader impacts 是什么（正面的和负面的）？

CS 论文越来越多地要求包含 limitation 段落或小节，可以是 Discussion 的子节，也可以是独立小节。

推荐的 move order：

1. 总结关键发现及其意义
2. 讨论 failure cases：什么输入导致退化、为什么
3. 列举 limitations：数据假设、计算代价、适用范围
4. 必要时讨论 broader impact（特别是 NeurIPS, ICML, FAccT）
5. 指向具体的未来方向（具体的技术扩展，而非泛泛之谈）

Useful phrase families:

- `Despite the promising results, our method has several limitations.`
- `A key limitation is that ... , which may affect performance when ...`
- `Our approach assumes that ... ; this may not hold in ...`
- `We observe that our method struggles with ... , likely because ...`
- `An interesting direction for future work is to extend ... by ...`
- `Potential negative societal impacts include ...`

避免：

- 复述 Results 部分的内容
- 对所有没做的东西都写"留给未来工作"
- 无具体分析就宣称 broader impact

## Conclusion

本段必须回答的问题：

1. 解决了什么问题、用了什么方法？
2. 主要结果是什么？
3. 社区的 takeaway 是什么？

CS 会议的 Conclusion 通常很短（1 段），有时与 Future Work 合并。不要浪费篇幅重复 Abstract 或 contribution list。

推荐的 move order：

1. 一句话重述问题和你的方法
2. 一句话总结关键结果（附核心数值）
3. 一句话说明意义或启示
4. 可选：一个具体的未来方向（不是列表）

Useful phrase families:

- `We presented ... , a ... method for ...`
- `On ... , our approach achieves ... , outperforming ...`
- `We hope that ... will inspire future work on ...`
- `An important next step is to extend our method to ...`

避免：

- 直接复制粘贴 Introduction 的 contribution list
- 泛泛写"还需要进一步研究"而不说具体做什么
- 引入新的结果或 ablation 实验
- overclaim（"我们的方法解决了...问题"）

## Abstract

本段必须回答的问题：

1. 具体的问题或 gap 是什么（有技术细节）？
2. 你的方法用一句话怎么说？
3. 关键结果是什么（最好有数字）？
4. 为什么这重要？

**CS 会议注记：** 会议审稿人经常只读 Abstract 和 Conclusion。Abstract 必须自包含且包含足够的具体信息。与 Nature 风格强调 broad motivation 不同，CS 的 Abstract 应强调技术具体性和定量结果。

推荐的 move order（会议风格）：

1. 有技术细节的问题陈述
2. 已有方法的局限（一句话）
3. 你的方法（一句话）
4. 关键结果附数字（如 "achieves 89.5% accuracy on ..., outperforming ... by 3.2%"）
5. 意义或启示

推荐的 move order（期刊风格）：

1. 更 broad 的背景
2. 具体的 gap
3. 方法
4. 关键结果
5. 启示

Useful phrase families:

- `We address the problem of ... in the setting of ...`
- `Existing methods are limited by ...`
- `We propose ... , a ... framework / algorithm / model that ...`
- `On ..., our method achieves ... , surpassing ...`
- `Our work provides ...`

避免：

- 写 CS 读者已经知道的背景（"深度学习取得了巨大成功..."）
- 模糊的数字（"显著提升"）
- 未核实就声称"首次"
- 写入本该出现在正文的方法细节

## Title

本段必须回答的问题：

- 哪几个词能让论文可搜索、具体、有趣且不过度宣称？

目标性质：

- searchable（包含领域关键词）
- specific（不要太泛）
- restrained（无夸张形容词："novel", "powerful", "superior"）
- defensible（准确描述论文内容）

CS/AI/ML 推荐标题模式：

- `[Method Name]: [Task Description]`（如 "CLIP: Learning Transferable Visual Models from Natural Language Supervision"）
- `[Task] with/by/for [Key Technique]`（如 "Image Super-Resolution via Sparse Representation"）
- `[Technique] for [Task]`（如 "Attention Is All You Need"）
- `A [Adjective] Approach to [Task]`（谨慎使用；只有 "simple" 和 "efficient" 是审稿人勉强接受的形容词）

避免：

- 满是缩写、不读全文就看不懂的标题
- `A novel ...`（基本应该删掉）
- `[Method] + [Method]: A hybrid approach to [Task]`（太多 "and" 和 "+"）
- 承诺比论文实际交付的更多
- 过时的双关语或幽默尝试

## CS/AI/ML 论文写作补充指导

### Conference 与 Journal 的区别

| 方面 | CS 会议（NeurIPS/CVPR/ICML） | CS 期刊（TPAMI/IJCV/JMLR） |
|------|-----------------------------|---------------------------|
| 页数限制 | 8-10 页正文 | 15-30 页，无严格限制 |
| Related Work | 通常较简洁或移至 supplementary | 全面、详尽 |
| Method | 紧凑，聚焦核心新颖性 | 展开，含全部细节 |
| Results | 聚焦主对比 + 关键 ablations | 完整实验，含 negative results |
| 审稿流程 | 单次决策（accept/reject） | 多轮修改 |
| Supplementary | 用于放证明、额外结果、视频 | 较少使用（论文自包含） |

### CS 论文常见陷阱

- **Overclaiming from insufficient baselines：** 声称 SOTA 必须在同一 benchmark 上对比近 2-3 年 *所有* 有竞争力的方法。
- **Missing negative results：** 审稿人会注意到你只报告了有效的结果。简要的 failure analysis 能建立可信度。
- **Weak related work positioning：** 没有把你方法与最接近的 competitors 区分开来，是"lack of novelty"拒稿的第一原因。
- **Architecture dump without rationale：** 描述了构建了什么，却没有解释 *为什么* 做每个设计选择。
- **Metric gaming：** 选择对自己有利但偏离社区标准的评估协议或 metrics。