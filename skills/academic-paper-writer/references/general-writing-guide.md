# 通用学术写作指南

本文件整合自圣心大学（Sacred Heart University）学术论文写作指南，针对CS/AI/ML领域进行适配。用于辅助论文写作时参考通用学术写作原则。

**来源**: [Organizing Academic Research Papers](https://library.sacredheart.edu/c.php?g=29803) - Sacred Heart University Library

---

## 文件协作图与决策树

### 相关文件定位

| 文件 | 核心职责 | 使用场景 |
|------|---------|---------|
| **general-writing-guide.md**（本文件） | 通用学术写作原则、结构指导、风格规范 | 写作前了解原则、写作中参考结构、完成后检查规范 |
| **exemplar-*.md** | CS/AI/ML领域的具体示例和可迁移模式 | 写作前参考领域范例、模仿优秀论文结构 |
| **writing-guidelines.md** | Venue适配、证据分层、风格调研 | 确认目标venue后、进行风格适配时 |
| **section-writing-contracts.md** | 章节论证契约、必需修辞动作、失败检查 | Step 8生成Section Contract、Step 9.0/9.8检查论证功能 |

### 决策树：何时参考哪个文件？

```
开始写作
  │
  ├─ 是否已确认目标venue？
  │   ├─ 否 → 先确认venue，再参考 writing-guidelines.md
  │   └─ 是 → 继续
  │
  ├─ 是否需要了解CS/AI/ML领域具体写法？
  │   ├─ 是 → 参考 exemplar-*.md（优先）
  │   └─ 否 → 继续
  │
  ├─ 是否需要了解通用学术写作原则？
  │   ├─ 是 → 参考 本文件（general-writing-guide.md）
  │   └─ 否 → 继续
  │
  └─ 是否需要检查章节论证功能？
      ├─ 是 → 参考 section-writing-contracts.md
      └─ 否 → 开始写作
```

### 协作关系说明

**本文件与exemplar文件的关系**：
- **exemplar文件优先**：当需要了解CS/AI/ML领域具体写法时，优先参考exemplar文件
- **本文件补充**：当需要了解通用学术写作原则或检查基本规范时，参考本文件
- **两者互补**：exemplar提供"怎么写"，本文件提供"为什么这样写"

**本文件与section-writing-contracts.md的关系**：
- **本文件**：提供通用写作原则和结构指导（宏观层面）
- **section-writing-contracts.md**：提供具体章节的论证契约和修辞动作（微观层面）
- **分工明确**：本文件不涉及具体章节的论证检查，由section-writing-contracts.md负责

---

## 使用定位

**何时参考本文件：**
- 写作时需要确认学术写作风格规范
- 撰写各部分内容时需要参考通用结构
- 检查论文是否符合学术写作基本要求
- 需要了解不同部分的写作策略时
- 需要了解学术写作的"为什么"时（而非仅"怎么做"）

**何时不参考本文件：**
- 需要CS/AI/ML领域具体示例时 → 参考 exemplar-*.md
- 需要检查章节论证功能时 → 参考 section-writing-contracts.md
- 需要进行venue风格适配时 → 参考 writing-guidelines.md

---

## 1. 学术写作风格原则

### 1.1 正式语调

学术写作使用正式的表达方式，特点包括：

| 要求 | 说明 | 示例 |
|------|------|------|
| 第三人称视角 | 通常避免使用"I"、"we"等第一人称 | ~~"We propose"~~ → "This paper proposes" |
| 客观陈述 | 呈现事实和证据，而非个人观点 | ~~"I think"~~ → "The results indicate" |
| 正式词汇 | 使用学科专业术语，避免口语化 | ~~"a lot of"~~ → "numerous" / "substantial" |

**CS/AI/ML领域例外**：
- 在描述方法时，使用"We"或"The authors"是可接受的
- 在Introduction中介绍贡献时，使用"We"是常见的
- 但应保持整体语调正式

### 1.2 清晰表达

**句子结构：**
- 使用简洁、直接的句子
- 避免过长的复合句
- 每个句子表达一个核心意思

**段落组织：**
- 每个段落有明确的主题句（通常在段首）
- 段落内容围绕主题句展开
- 段落之间有逻辑连接

**过渡词使用：**
- 因果关系：therefore, consequently, as a result
- 递进关系：furthermore, moreover, additionally
- 转折关系：however, nevertheless, in contrast
- 举例关系：for example, specifically, in particular

### 1.3 常见写作错误

| 错误类型 | 说明 | 正确做法 |
|---------|------|---------|
| 过度使用专业术语 | 使用"大词"显得专业，但影响可读性 | 使用准确且必要的术语 |
| 模糊表达 | 使用"they"、"we"、"people"等泛指 | 明确指代对象 |
| 冗余表述 | 重复表达相同意思 | 简洁直接 |
| 非正式语言 | 使用缩写、俚语、习语 | 使用正式表达 |
| 缺少过渡 | 段落之间缺乏逻辑连接 | 使用过渡词和过渡句 |

---

## 2. 各部分写作指南

### 2.1 Abstract

**定义**：摘要通常为一段300字以内的文字，概括论文的主要内容。

**四种类型**：

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| **批判性摘要** | 描述发现并评价研究的有效性、可靠性 | 较少使用 |
| **描述性摘要** | 说明论文包含的信息类型，不提供结果或结论 | 作为论文大纲 |
| **信息性摘要** | 作为论文的替代品，包含主要论点、结果和证据 | **CS/AI/ML最常用** |
| **高亮性摘要** | 吸引读者注意，不要求完整或平衡 | 宣传用途 |

**CS/AI/ML论文摘要结构**：
```
[背景问题] → [现有方法不足] → [本文方法] → [核心结果] → [意义]
```

**写作要点**：
1. 使用主动语态（尽可能）
2. 使用过去时态（报告已完成的研究）
3. 包含量化结果（如果可用）
4. 避免引用其他文献
5. 避免使用缩写或术语（除非必要）

**摘要不应包含**：
- 冗长的背景信息
- 对其他文献的引用
- 省略号或不完整句子
- 图表或图像

**CS/AI/ML示例（Transformer）**：
> The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show that these models are superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU.

**示例分析**：
- 背景问题：序列转换模型基于复杂的RNN/CNN
- 现有方法不足：encoder-decoder结构，需要attention连接
- 本文方法：Transformer，仅基于attention机制
- 核心结果：28.4 BLEU，提升2+ BLEU
- 意义：更易并行化，训练时间更短

**详细示例**：参考 `exemplar-abstract.md`

### 2.2 Introduction

**定义**：引言将读者从一般领域引导到具体研究问题。

**核心问题**（引言应回答）：
1. 研究什么？
2. 为什么这个主题重要？
3. 之前对该主题了解多少？
4. 本研究如何推进知识？

**倒三角结构**：

```
┌─────────────────────────────────────────┐
│            广泛的背景信息               │
│  ┌─────────────────────────────────┐   │
│  │      具体的研究背景             │   │
│  │  ┌─────────────────────────┐   │   │
│  │  │    研究缺口/问题        │   │   │
│  │  │  ┌─────────────────┐   │   │   │
│  │  │  │  本文研究目的   │   │   │   │
│  │  │  └─────────────────┘   │   │   │
│  │  └─────────────────────────┘   │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**引言的三个阶段**：
1. **建立研究领域**：
   - 强调主题的重要性
   - 概述当前研究状况
2. **识别研究缺口**：
   - 提出已有假设
   - 揭示现有研究的不足
   - 提出研究问题
3. **填补研究缺口**：
   - 说明研究目的
   - 概述关键特征
   - 描述潜在结果

**吸引读者的策略**：
1. 引人入胜的故事
2. 有力的引言或生动的轶事
3. 发人深省的问题
4. 令人困惑的场景
5. 说明研究重要性的案例

**CS/AI/ML领域建议**：
- 从领域现状切入，承认已有方法的成功
- 指出核心瓶颈（具体、技术性）
- 一句话讲清核心想法
- 给出量化贡献

**CS/AI/ML示例（ResNet）**：
> Deep convolutional neural networks have led to a series of breakthroughs for image classification. Deep networks naturally integrate low/mid/high-level features and classifiers in an end-to-end multi-layer fashion, and the "levels" of features can be enriched by the number of stacked layers (depth). Recent evidence reveals that network depth is of crucial importance, and the leading results on the challenging ImageNet dataset all exploit "very deep" models.
>
> In this paper, we address the degradation problem by introducing a deep residual learning framework. Instead of hoping each few stacked layers directly fit a desired underlying mapping, we explicitly let these layers fit a residual mapping.

**示例分析**：
- 领域现状：深度CNN在图像分类中取得突破
- 核心瓶颈：网络深度增加导致退化问题
- 核心想法：残差学习框架，让层拟合残差映射
- 量化贡献：解决退化问题，实现更深的网络

**详细示例**：参考 `exemplar-introduction.md`

### 2.3 Related Work / Literature Review

**定义**：文献综述调查与特定问题、研究领域或理论相关的学术文章、书籍和其他来源。

**文献综述的目的**：
- 将每项工作置于其对理解研究问题的贡献背景下
- 描述每项工作与其他工作的关系
- 识别解释和先前研究中的空白
- 解决先前研究中的矛盾
- 防止重复努力
- 指出进一步研究的方向
- 将自己的研究置于现有文献的背景下

**六种文献综述类型**：

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| **论点式** | 选择性地审查文献以支持或反驳论点 | 有明确立场时 |
| **整合式** | 综合代表性文献，生成新框架和视角 | 概念性综合 |
| **历史式** | 按时间顺序追踪问题/概念的演变 | 研究历史悠久的领域 |
| **方法论式** | 关注研究方法而非内容 | 方法比较 |
| **系统式** | 使用预先规定的方法审查现有证据 | 因果关系问题 |
| **理论式** | 审查累积的理论体系 | 理论框架建立 |

**组织方式**：

| 方式 | 说明 | CS/AI/ML常用度 |
|------|------|---------------|
| **按时间顺序** | 按发表时间组织 | ⭐⭐ |
| **按主题** | 按概念类别组织 | ⭐⭐⭐⭐⭐ |
| **按方法论** | 按研究方法组织 | ⭐⭐⭐⭐ |
| **按理论框架** | 按理论视角组织 | ⭐⭐⭐ |

**CS/AI/ML领域Related Work结构**：
```
[直接相关工作] → [支撑性背景工作] → [与本文的关系]
```

**写作要点**：
1. 总结并综合来源，而非仅仅列举
2. 保持自己的声音，而非被他人观点主导
3. 谨慎释义，准确表达原作者观点
4. 使用证据支持论述
5. 选择性引用，只选择最重要的观点

**CS/AI/ML示例（Vision Transformer）**：
> **Self-attention in NLP.** The Transformer architecture was proposed by Vaswani et al. (2017) for machine translation, and has since become the de-facto standard in many NLP tasks.
>
> **Self-attention in computer vision.** Self-attention has been applied to computer vision in a number of ways. Wang et al. (2018) apply a non-local self-attention operation to videos to aggregate information from the whole video.
>
> In contrast to these works, we aim to explore the limits of a pure Transformer applied directly to sequences of image patches.

**示例分析**：
- 按主题分组：NLP self-attention 和 Vision self-attention
- 主题内部有序：Vision部分进一步分类
- 对比定位：明确本文落位
- 引用回调：告诉读者实验部分会有具体对比

**详细示例**：参考 `exemplar-related-work.md`

### 2.4 Methodology

**定义**：方法部分提供判断研究有效性的信息，回答两个主要问题：
1. 数据是如何收集或生成的？
2. 数据是如何分析的？

**写作要求**：
- 使用过去时态
- 直接、精确
- 提供足够信息以允许复制研究

**CS/AI/ML领域方法结构**：
```
[问题定义/符号] → [整体架构] → [核心模块] → [训练目标/优化] → [推理/预测]
```

**方法部分应包含**：
1. 介绍整体方法论方法
2. 说明方法如何适应研究设计
3. 描述具体的数据收集方法
4. 解释如何分析结果
5. 为不熟悉的方法提供背景和理由
6. 说明样本选择和抽样程序的理由
7. 讨论潜在局限性

**CS/AI/ML领域特别注意**：
- 与代码实现保持一致
- 说明架构图的放置点
- 每个核心模块说明：作用、输入/输出、关键操作、公式
- 如果使用特殊技术（如attention、graph neural network），说明其在整体中的位置

**常见错误**：
| 错误 | 说明 |
|------|------|
| 无关细节 | 提供与理解方法无关的背景信息 |
| 过度解释基本程序 | 假设读者有基础知识 |
| 问题盲点 | 忽略研究中遇到的问题 |

**CS/AI/ML示例（Transformer方法结构）**：
```
1. 问题定义：序列转换任务（机器翻译）
2. 整体架构：Encoder-Decoder结构
3. 核心模块：
   - Multi-Head Attention
   - Position-wise Feed-Forward Networks
   - Positional Encoding
4. 训练目标：交叉熵损失 + Label Smoothing
5. 推理：自回归解码
```

**示例分析**：
- 问题定义清晰：序列转换任务
- 整体架构明确：Encoder-Decoder
- 核心模块详细：每个模块的作用、输入/输出、关键操作
- 训练目标具体：损失函数和优化策略
- 推理过程说明：自回归解码

**详细示例**：参考 `exemplar-method.md`

### 2.5 Results

**定义**：结果部分报告研究发现，不进行解释。

**CS/AI/ML领域结果结构**：
```
[主结果表格/图表] → [关键发现陈述] → [与baseline的比较]
```

**写作要点**：
1. 按逻辑顺序呈现结果
2. 使用图表辅助说明
3. 文字和图表互补，不重复
4. 报告统计显著性（如适用）
5. 只报告与研究问题相关的结果

**非文本元素使用**：
- 表格：呈现精确数值和比较
- 图表：展示趋势和关系
- 图像：展示示例或可视化

### 2.6 Discussion

**定义**：讨论部分解释和描述发现在已知研究问题背景下的意义。

**讨论的重要性**：
- 这是论文中最能展示批判性思维能力的部分
- 探索研究的潜在含义
- 填补现有空白

**讨论的组织结构**：

```
[重述研究问题] → [解释主要发现] → [与相关研究比较] → [承认局限性] → [提出未来工作]
```

**讨论的内容**：
1. **结果解释**：评论结果是否符合预期，解释意外发现
2. **与先前研究的比较**：将结果与其他研究的发现进行比较
3. **推论**：说明结果如何更广泛地应用
4. **假设**：从结果中得出的更一般的结论

**讨论的顺序要点**：
1. 从一般到具体（倒金字塔）
2. 使用与引言相同的关键词和时态
3. 先陈述答案，再陈述相关结果，然后引用他人工作
4. 分析意外发现
5. 识别潜在局限性和弱点
6. 以主要含义的简明总结结束

**CS/AI/ML领域建议**：
- 解释模型为何有效
- 说明为何可能失效
- 承认评估协议、数据质量、可解释性或泛化边界的限制
- 对reviewer最可能质疑的问题提前做方法学回应

**常见错误**：
| 错误 | 说明 |
|------|------|
| 结果重复 | 浪费整句话重述结果 |
| 引入新结果 | 讨论中不应引入新的结果 |
| 过度解释 | 读出数据不支持的结论 |

**CS/AI/ML示例（讨论结构）**：
```
1. 重述研究问题：本文提出了一种新的注意力机制
2. 解释主要发现：实验结果表明，该机制在多个任务上优于现有方法
3. 与相关研究比较：与Transformer相比，我们的方法在长序列上更高效
4. 承认局限性：在小数据集上，性能提升不明显
5. 提出未来工作：探索在更多任务上的应用，优化计算效率
```

**示例分析**：
- 重述研究问题：简洁回顾核心问题
- 解释主要发现：基于实验结果的客观陈述
- 与相关研究比较：与baseline的具体对比
- 承认局限性：诚实说明研究的边界
- 提出未来工作：具体、可执行的后续方向

**详细示例**：参考 `exemplar-experiments.md`

### 2.7 Conclusion

**定义**：结论部分总结研究并重申其重要性。

**结论应包含**：
1. 总结工作与主要发现
2. 重申局限性边界
3. 给出未来工作方向

**写作要点**：
- 简洁明了
- 不引入新信息
- 回扣研究问题
- 强调研究贡献

**CS/AI/ML领域建议**：
- 如果是早期草稿，可写成"当前证据支持的有限结论"
- 回扣方法贡献、当前结果边界和下一步最关键补强项

---

## 3. 写作检查清单

**注意**：本清单专注于通用写作规范检查。具体章节的论证检查（如必需修辞动作、失败检查等）请参考 `section-writing-contracts.md`。

### 3.1 语言规范检查

| 检查项 | 说明 |
|-------|------|
| [ ] 正式语调 | 避免非正式表达、口语化语言 |
| [ ] 准确术语 | 使用学科专业术语，避免模糊表达 |
| [ ] 简洁句子 | 句子结构清晰，避免过长复合句 |
| [ ] 段落主题 | 每个段落有明确的主题句 |
| [ ] 逻辑过渡 | 使用适当的过渡词和过渡句 |
| [ ] 时态一致 | 保持时态一致性（通常使用过去时） |

### 3.2 结构规范检查

| 检查项 | 说明 |
|-------|------|
| [ ] 研究问题清晰 | 论文围绕一个清晰的研究问题组织 |
| [ ] 逻辑连贯 | 各部分之间有清晰的逻辑连接 |
| [ ] 证据支撑 | 论点有充分的证据支持 |
| [ ] 引用规范 | 引用格式正确，避免抄袭 |

### 3.3 CS/AI/ML领域特别检查

| 检查项 | 说明 |
|-------|------|
| [ ] 方法可复现 | 提供足够细节，允许他人复现 |
| [ ] 代码一致性 | 方法描述与代码实现一致 |
| [ ] 结果可验证 | 实验结果有充分的验证 |
| [ ] 局限性说明 | 明确说明研究的局限性 |

**详细章节检查**：请参考 `section-writing-contracts.md` 中的"Required moves"和"Failure checks"。

---

## 参考资源

- [Organizing Academic Research Papers](https://library.sacredheart.edu/c.php?g=29803) - Sacred Heart University Library
- [Purdue OWL](https://owl.purdue.edu/) - Purdue University Online Writing Lab
- [The Elements of Style](https://www.strunkandwhite.com/) - Strunk & White
