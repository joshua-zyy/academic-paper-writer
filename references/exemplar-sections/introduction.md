# Exemplar: Introduction

本文件展示经典论文 Introduction 的组织方式。目标是学习叙述结构与论证模式，而非复制措辞。

---

## 示例 1: Transformer (Vaswani et al., NeurIPS 2017)

**来源**: "Attention Is All You Need", NeurIPS 2017

### 原文片段

> Recurrent neural networks, long short-term memory and gated recurrent neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems such as language modeling and machine translation. Numerous efforts have since continued to push the boundaries of recurrent language models and encoder-decoder architectures.
>
> ...
>
> In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output. The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs.

### 写作要点

1. **开场策略**: 从领域现状切入，承认已有方法（RNN/LSTM/GRU）的成功地位
2. **问题陈述**: 指出核心瓶颈——序列计算限制并行化（而非泛泛批评RNN不好）
3. **方法定位**: 一句话讲清核心想法——"eschewing recurrence and instead relying entirely on an attention mechanism"
4. **贡献量化**: 给出具体训练时间（12 hours on 8 P100 GPUs），而非空泛的"显著提升"

### 可迁移模式

```
[领域现状与主流方法] → [主流方法的核心瓶颈（具体、技术性）] → [本文核心想法（一句话定位）] → [量化贡献]
```

---

## 示例 2: ResNet (He et al., CVPR 2016)

**来源**: "Deep Residual Learning for Image Recognition", CVPR 2016

### 原文片段

> Deep convolutional neural networks have led to a series of breakthroughs for image classification. Deep networks naturally integrate low/mid/high-level features and classifiers in an end-to-end multi-layer fashion, and the "levels" of features can be enriched by the number of stacked layers (depth). Recent evidence reveals that network depth is of crucial importance, and the leading results on the challenging ImageNet dataset all exploit "very deep" models.
>
> ...
>
> In this paper, we address the degradation problem by introducing a deep residual learning framework. Instead of hoping each few stacked layers directly fit a desired underlying mapping, we explicitly let these layers fit a residual mapping.
>
> ...
>
> Our extremely deep residual nets are easy to optimize, but the counterpart "plain" nets (simply stacking layers) exhibit higher training error when the depth increases. We provide comprehensive experiments on ImageNet and CIFAR-10, showing that residual learning is easy to optimize and can gain accuracy from considerably increased depth.

### 写作要点

1. **开场策略**: 从领域突破切入，建立"深度网络很重要"的前提
2. **问题陈述**: 引入 counterintuitive 的现象——deeper networks have higher training error (not overfitting!)
3. **方法定位**: 用对比句式——"Instead of hoping... we explicitly let..."
4. **贡献要点**: 覆盖可优化性、准确率增益、实验验证

### 可迁移模式

```
[领域趋势/共识] → [反直觉现象/意想不到的问题] → [本文如何重新定义问题] → [关键优势 + 实验支撑]
```

---

## 示例 3: BERT (Devlin et al., NAACL 2019)

**来源**: "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", NAACL 2019

### 原文片段

> Language model pre-training has been shown to be effective for improving many natural language processing tasks. These include sentence-level tasks such as natural language inference and paraphrasing, which aim to predict the relationships among sentences, and token-level tasks such as named entity recognition and question answering, where models are required to produce fine-grained output at the token level.
>
> There are two existing strategies for applying pre-trained language representations to downstream tasks: feature-based and fine-tuning. ...
>
> We propose a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks.

### 写作要点

1. **开场策略**: 从成功范式切入（pre-training 有效）
2. **分类框架**: 将已有工作分为两类（feature-based vs fine-tuning），展示你对领域的系统理解
3. **问题陈述**: 指出已有方法的共同局限——unidirectional，限制了表示能力
4. **方法定位**: 对比句式——"Unlike..., BERT is designed to..."
5. **贡献要点**: 强调 simplicity（just one additional output layer）和 generality（wide range of tasks）

### 可迁移模式

```
[成功范式/趋势] → [已有工作的分类框架] → [所有类别的共同局限] → [本文如何打破局限] → [simplicity + generality]
```

---

## 通用 Introduction 结构模板

综合以上示例，一个有效的 Introduction 通常包含以下功能单元：

| 功能单元 | 典型位置 | 目的 |
|---------|---------|------|
| 领域背景 | 开场 1-2 段 | 建立问题重要性，让读者相信这件事值得做 |
| 主流方法 | 背景后 | 展示你对领域的理解，承认已有工作的贡献 |
| 核心瓶颈 | 中段 | 指出具体、技术性的问题（而非泛泛批评） |
| 本文想法 | 中后段 | 一句话讲清核心贡献（对比句式常用） |
| 贡献列表 | 结尾 | 3-5 条具体贡献，可包含量化结果 |

### 常见错误

1. **开场过长**: 背景铺垫超过 3 段，迟迟不进入问题
2. **问题模糊**: "现有方法效果不好"——没有说清哪里不好、为什么不好
3. **贡献空泛**: "提出了一个新方法"——没有说清新在哪里、解决了什么问题
4. **缺乏对比**: 没有建立与已有工作的明确差异

### 写作建议

- 第一段末尾应有明确的"然而/但是"转折，引出问题
- 核心方法描述应有对比句式（Unlike... / Instead of... / In contrast to...）
- 贡献点应具体：解决了什么问题、提升了多少、覆盖哪些任务
