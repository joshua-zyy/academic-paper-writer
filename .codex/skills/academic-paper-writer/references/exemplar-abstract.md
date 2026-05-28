# Exemplar: Abstract

本文件展示经典论文 Abstract 的写作方式。核心原则：简洁有力、背景-方法-结果-意义闭环。

---

## 示例 1: Transformer (Vaswani et al., NeurIPS 2017)

**来源**: "Attention Is All You Need", NeurIPS 2017

### 原文

> The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show that these models are superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs. 

### 写作要点

1. **一句话背景**: "The dominant sequence transduction models are based on..."
2. **一句话问题**: 隐含在背景中（recurrent/convolutional 的局限性）
3. **一句话方法**: "We propose... the Transformer, based solely on attention mechanisms"
4. **一句话优势**: "superior in quality while being more parallelizable"
5. **量化结果**: 28.4 BLEU, 41.8 BLEU, 3.5 days on 8 GPUs

### 可迁移模式

```
[背景 + 隐含问题] → [一句话方法定位] → [核心优势] → [量化结果 × 2-3]
```

---

## 示例 2: GPT-3 (Brown et al., NeurIPS 2020)

**来源**: "Language Models are Few-Shot Learners", NeurIPS 2020

### 原文

> Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training on a large corpus of text followed by fine-tuning on a specific task. While typically task-agnostic in architecture, this method still requires task-specific fine-tuning datasets of thousands or more examples. By contrast, humans can generally perform a new language task from only a few examples or from simple instructions – something which current NLP systems still largely struggle to do. Here we show that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes even reaching competitiveness with prior state-of-the-art fine-tuning approaches. Specifically, we train GPT-3, an autoregressive language model with 175 billion parameters, and test its performance in the few-shot setting. GPT-3 achieves strong performance on many NLP datasets, including translation, question-answering, and cloze tasks. On some of these datasets, GPT-3 achieves results close to or better than state-of-the-art without any fine-tuning.

### 写作要点

1. **背景**: pre-training + fine-tuning 范式的成功
2. **问题**: 需要 task-specific fine-tuning，且需要大量样本
3. **对比（人 vs 机器）**: humans can... from only a few examples
4. **核心主张**: scaling up → few-shot performance
5. **具体方法**: GPT-3, 175B parameters
6. **结果**: strong performance on many NLP datasets, close to SOTA without fine-tuning

### 可迁移模式

```
[范式背景] → [范式局限] → [人的能力对比] → [本文主张] → [具体方法] → [关键结果]
```

---

## 示例 3: ResNet (He et al., CVPR 2016)

**来源**: "Deep Residual Learning for Image Recognition", CVPR 2016

### 原文

> Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the learning of layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers—8× deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers.

### 写作要点

1. **开门见山**: "Deeper neural networks are more difficult to train"
2. **方法核心**: residual learning framework
3. **方法解释**: reformulate as learning residual functions
4. **核心优势**: easier to optimize, gain accuracy from depth
5. **量化结果**: 152 layers, 3.57% error, 1st place ILSVRC 2015
6. **额外验证**: CIFAR-10 with 100 and 1000 layers

---

## 示例 4: BERT (Devlin et al., NAACL 2019)

**来源**: "BERT: Pre-training of Deep Bidirectional Transformers"

### 原文

> We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications.

### 写作要点

1. **名称解释**: BERT = Bidirectional Encoder Representations from Transformers
2. **核心差异**: Unlike... BERT is designed to pre-train deep bidirectional representations
3. **简洁性**: just one additional output layer
4. **广泛性**: wide range of tasks, without substantial architecture modifications

---

## 通用 Abstract 结构模板

### 模式 1: 问题-方法-结果型

```
[背景/问题] → [本文方法] → [核心优势] → [量化结果] → [意义/影响]
```

### 模式 2: 范式突破型

```
[现有范式] → [范式局限] → [本文如何打破局限] → [结果证明] → [意义]
```

### 模式 3: 能力对比型

```
[人的能力] → [机器的局限] → [本文如何缩小差距] → [结果]
```

---

## Abstract 四要素

| 要素 | 必要性 | 典型位置 |
|------|--------|----------|
| 背景问题 | 必须 | 开头 1-2 句 |
| 方法定位 | 必须 | 中段，一句话 |
| 核心优势 | 必须 | 方法后，1-2 句 |
| 量化结果 | 必须 | 后段，具体数字 |

---

## 常见错误

| 错误类型 | 表现 | 改进 |
|---------|------|------|
| 背景过长 | 前 3 句都在讲领域 | 1-2 句快速切入问题 |
| 方法模糊 | "提出了一个新方法" | 说明新在哪里、核心思想 |
| 无量化结果 | "取得了显著提升" | 给出具体数字 |
| 过度声明 | "解决了所有X问题" | 用 "demonstrates strong performance" 等克制表述 |
| 缺乏对比 | 不说与已有工作的差异 | 用 "Unlike..." 或 "In contrast to..." |

---

## 写作建议

1. **首句抓住问题**: 让读者立刻知道这篇论文解决什么问题
2. **方法描述具体**: 一句话说清核心思想，不要泛泛而谈
3. **结果量化**: 给出具体数字（BLEU、准确率、错误率等）
4. **长度控制**: 通常 150-250 词，不超过一页
5. **独立可读**: Abstract 应该独立于正文被理解
6. **避免引用**: Abstract 中通常不出现文献引用
