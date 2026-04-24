# Exemplar: Related Work

本文件展示经典论文 Related Work 的组织方式。核心原则：按主题分组、有综合比较、有与本文的关系说明。

---

## 示例 1: Vision Transformer (Dosovitskiy et al., ICLR 2021)

**来源**: "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale", ICLR 2021

### 原文片段

> **Self-attention in NLP.** The Transformer architecture was proposed by Vaswani et al. (2017) for machine translation, and has since become the de-facto standard in many NLP tasks. Large Transformer models are often pre-trained on large corpora and then fine-tuned for the task at hand...
>
> **Self-attention in computer vision.** Self-attention has been applied to computer vision in a number of ways. Wang et al. (2018) apply a non-local self-attention operation to videos to aggregate information from the whole video. Another line of work replaces the convolutional backbone entirely with self-attention (e.g., Ramachandran et al., 2020). We compare to these in the experiments.
>
> Another line of work combines convolutional neural networks with self-attention, e.g., by augmenting convolutional features with self-attention (Hu et al., 2019) or by using self-attention to improve feature aggregation (Bello et al., 2019). In contrast to these works, we aim to explore the limits of a pure Transformer applied directly to sequences of image patches.

### 写作要点

1. **按主题分组**: 分为 NLP self-attention 和 Vision self-attention 两大主题
2. **主题内部有序**: Vision 部分进一步分为 "replace CNN entirely" 和 "combine CNN with attention" 两类
3. **对比定位**: "In contrast to these works, we aim to..."——明确本文落位
4. **引用回调**: "We compare to these in the experiments"——告诉读者实验部分会有具体对比

### 可迁移模式

```
[主题A] → [主题A的代表工作 + 共同特点] → [主题B] → [主题B的代表工作 + 共同特点] → [本文与各主题的关系]
```

---

## 示例 2: GAT (Veličković et al., ICLR 2018)

**来源**: "Graph Attention Networks", ICLR 2018

### 原文片段

> **Neural networks on graphs.** Graph neural networks (GNNs) have been introduced by Gori et al. (2005) and Scarselli et al. (2009) as a generalization of recurrent neural networks to arbitrary graphs. ...
>
> **Graph convolutional networks.** Recent interest in GNNs has been reinvigorated following the introduction of graph convolutional networks (GCNs) by Kipf & Welling (2017). GCNs extend convolutional neural networks to graph-structured data by using spectral graph convolutions...
>
> **Attention mechanisms.** Attention mechanisms have become a standard component in many sequence-based tasks... To the best of our knowledge, graph attention networks as introduced in this work are the first to apply attention mechanisms to graph neural networks.

### 写作要点

1. **方法谱系**: GNN → GCN → 本工作（attention-based GNN），展示清晰的演进脉络
2. **每个主题的闭环**: 背景 → 代表工作 → 核心机制 → 局限/缺口
3. **新颖性声明**: "To the best of our knowledge... are the first to..."——明确的创新定位
4. **与 Introduction 的分工**: Related Work 详述已有方法，Introduction 专注本文定位

### 可迁移模式

```
[方法谱系起点] → [中间发展] → [本文在谱系中的位置] → [与最近工作的具体差异]
```

---

## 示例 3: ResNet (He et al., CVPR 2016) - Related Work 节选

**来源**: "Deep Residual Learning for Image Recognition", CVPR 2016

### 原文片段

> **Residual Representations.** In image recognition, VLAD is a representation that encodes by the residual vectors with respect to a dictionary, and Fisher Vector can be formulated as a probabilistic version of VLAD...
>
> **Shortcuts.** The practice of shortcuts has a long history... Inception layers are composed of shortcut branches and a few deeper branches...
>
> Our formulation differs from these in that we show that shortcuts are the most direct way to address the degradation problem, and we provide extensive empirical evidence to support this claim.

### 写作要点

1. **主题命名**: 每个主题用粗体小标题明确标识
2. **跨领域借鉴**: 残差表示从 VLAD、Fisher Vector 借鉴，展示知识广度
3. **差异化定位**: "Our formulation differs from these in that..."——具体说明本文的不同
4. **证据支撑**: "provide extensive empirical evidence"——暗示实验部分会证明

---

## 通用 Related Work 结构模板

### 模式 1: 方法谱系型

适用于：你的工作是已有方法的自然延伸或改进

```
[方法家族A] → [代表工作 + 核心机制] → [共同局限] → [方法家族B] → [代表工作 + 核心机制] → [共同局限] → [本文如何综合/超越]
```

### 模式 2: 主题分组型

适用于：你的工作涉及多个子领域，需要分别交代

```
[主题A: 背景与代表工作] → [主题A与本文的关系] → [主题B: 背景与代表工作] → [主题B与本文的关系] → [综合定位]
```

### 模式 3: 对比表型

适用于：相关工作较多，需要系统比较

```
[按方法类别分组] → [每类给一个代表性工作] → [在文本中简要说明各类的优缺] → [可附加表格对比]
```

---

## 常见错误

| 错误类型 | 表现 | 改进 |
|---------|------|------|
| 罗列式 | "A做了X。B做了Y。C做了Z。" | 分组、比较、说明关系 |
| 无定位 | 只介绍他人工作，不说本文与它们的关系 | 每组结尾加一句与本文的关系 |
| 选择性忽略 | 只引用自己方法能赢的 baseline | 补充强基线，诚实讨论 |
| 过长 | Related Work 超过正文一半 | 精简背景，聚焦直接相关 |

---

## 写作建议

1. **每组必有一句"与本文的关系"**: 不能只有文献介绍
2. **使用对比句式**: "Unlike X, our method...", "In contrast to Y, we..."
3. **引用密度**: 每段应有足够 inline citation，但不要堆砌
4. **长度控制**: 一般 2-4 个主题组，每组 1-2 段
5. **与 Introduction 的分工**: Related Work 可以更深，Introduction 保持简洁
