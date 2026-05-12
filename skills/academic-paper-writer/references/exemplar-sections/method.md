# Exemplar: Method

本文件展示经典论文 Method 章节的组织方式。核心原则：先整体后模块、公式与动机结合、输入输出清晰。

---

## 示例 1: Transformer (Vaswani et al., NeurIPS 2017)

**来源**: "Attention Is All You Need", NeurIPS 2017

### 原文片段

> ## 3 Model Architecture
>
> The Transformer follows this overall architecture using stacked self-attention and point-wise, fully connected layers for both the encoder and decoder, shown in Figures 1 and 2 respectively.
>
> ### 3.1 Encoder and Decoder Stacks
>
> **Encoder:** The encoder is composed of a stack of N = 6 identical layers. Each layer has two sub-layers. The first is a multi-head self-attention mechanism, and the second is a simple, position-wise fully connected feed-forward network. We employ a residual connection around each of the two sub-layers, followed by layer normalization...
>
> **Decoder:** The decoder is also composed of a stack of N = 6 identical layers. In addition to the two sub-layers in each encoder layer, the decoder inserts a third sub-layer, which performs multi-head attention over the output of the encoder stack...
>
> ### 3.2 Attention
>
> An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors. We call our particular attention "Scaled Dot-Product Attention"...
>
> $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

### 写作要点

1. **整体框架先行**: 开篇一句话概括整体架构，并引用架构图
2. **模块分层介绍**: Encoder → Decoder → Attention → FFN → Positional Encoding
3. **公式紧随动机**: 先解释 attention 的直觉，再给公式，再解释 scaling 的原因
4. **输入输出清晰**: 每个 module 说明输入输出维度

### 关键公式与动机

> We suspect that for large values of d_k, the dot products grow large in magnitude, pushing the softmax function into regions where it has extremely small gradients. To counteract this effect, we scale the dot products by 1/√d_k.

**写作模式**: 问题（梯度消失）→ 解决（缩放）→ 公式

### 可迁移模式

```
[整体架构概述 + 图引用] → [模块1: 作用 + 结构 + 输入输出] → [模块2: 作用 + 结构 + 输入输出] → [关键公式 + 动机解释]
```

---

## 示例 2: ResNet (He et al., CVPR 2016)

**来源**: "Deep Residual Learning for Image Recognition", CVPR 2016

### 原文片段

> ## 3. Deep Residual Learning
>
> ### 3.1. Residual Learning
>
> Let us consider H(x) as an underlying mapping to be fit by a few stacked layers, with x denoting the inputs to the first of these layers. If one hypothesizes that multiple nonlinear layers can asymptotically approximate complicated functions, then it is equivalent to hypothesize that they can asymptotically approximate the residual function, i.e., F(x) := H(x) − x...
>
> ### 3.2. Identity Mapping by Shortcuts
>
> We adopt residual learning to every few stacked layers. A building block is shown in Fig. 2. Formally, a building block is defined as:
>
> $$y = \mathcal{F}(x, \{W_i\}) + x$$
>
> where x and y are the input and output vectors of the layers considered. The function F(x, {Wi}) represents the residual mapping to be learned.

### 写作要点

1. **问题驱动**: 从"为什么需要残差"开始，而非直接扔公式
2. **数学形式简洁**: 公式简单，但解释清楚 x、y、F 各自的含义
3. **实现细节后置**: 先讲原理，再讲具体实现（3.3节）
4. **图示配合**: "A building block is shown in Fig. 2"

### 残差动机的经典表述

> If one hypothesizes that multiple nonlinear layers can asymptotically approximate complicated functions, then it is equivalent to hypothesize that they can asymptotically approximate the residual function...

**写作模式**: 如果网络能学复杂函数 → 那它也能学残差函数 → 而残差更容易学

---

## 示例 3: BERT (Devlin et al., NAACL 2019)

**来源**: "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"

### 原文片段

> ## 3 BERT
>
> In this section, we introduce BERT and its detailed implementation. There are two steps in our framework: pre-training and fine-tuning.
>
> ### 3.1 Model Architecture
>
> BERT's model architecture is a multi-layer bidirectional Transformer encoder...
>
> ### 3.2 Input/Output Representations
>
> To make BERT handle a variety of down-stream tasks, our input representation is able to unambiguously represent both a single sentence and a pair of sentences...
>
> We use WordPiece embeddings with a 30,000 token vocabulary...

### 写作要点

1. **框架先行**: 开篇说明两个阶段（pre-training + fine-tuning）
2. **输入输出独立成节**: Input/Output Representations 单独一节，说明 token、segment、position embeddings
3. **实现细节具体**: 词汇表大小、层数、隐藏维度都给出

---

## 通用 Method 结构模板

### 模式 1: 整体 → 模块 → 细节

```
[整体架构概述] → [图引用] → [模块1: 动机 + 结构 + 公式 + 输入输出] → [模块2: ...] → [训练目标/损失函数] → [推理细节]
```

### 模式 2: 问题 → 解决 → 细节

```
[本文解决的核心问题] → [核心设计思路] → [具体模块实现] → [公式 + 解释] → [实现细节]
```

### 模式 3: 框架 → 组件 → 流程

```
[整体框架图 + 描述] → [组件1] → [组件2] → [组件N] → [训练流程] → [推理流程]
```

---

## Method 写作的四大要素

| 要素 | 必要性 | 说明 |
|------|--------|------|
| 整体框架 | 必须 | 一句话概括 + 架构图引用 |
| 模块拆解 | 必须 | 每个核心模块独立小节 |
| 公式 + 动机 | 必须 | 公式后紧跟解释，说明为什么这样设计 |
| 输入输出 | 必须 | 每个模块说明输入输出张量形状 |

---

## 核心模块的写作模板

对每个核心/非显然模块，按以下顺序展开：

```markdown
### X.X [模块名称]

[一句话说明该模块解决什么问题 / 在整体中的位置]

**结构:** [描述模块的核心结构]

**输入:** [张量形状或符号表示]

**输出:** [张量形状或符号表示]

**公式:** 
$$\text{公式}$$

**动机/设计原因:** [为什么采用这种设计，预期收益是什么]
```

---

## 常见错误

| 错误类型 | 表现 | 改进 |
|---------|------|------|
| 公式堆砌 | 只有公式，没有动机解释 | 每个公式后加"为什么这样" |
| 结构缺失 | 没有整体框架图 | 至少保留图占位 |
| 输入输出模糊 | 只说"特征"，不说维度 | 明确张量形状 |
| 平均用力 | 所有模块篇幅相同 | 核心模块详写，支撑模块简写 |
| 代码讲解口吻 | "我们首先做X，然后做Y" | 改为学术叙事："X用于...，随后Y负责..." |

---

## 写作建议

1. **开篇必有图引用**: "[Figure 1] shows the overall architecture"
2. **公式前有铺垫**: 先解释直觉，再给公式
3. **公式后有解释**: 说明各符号含义、设计动机
4. **区分核心与支撑**: 核心模块详写设计动机，支撑模块简写
5. **保持学术口吻**: 避免"我们代码里写了..."，改为"本文采用..."
