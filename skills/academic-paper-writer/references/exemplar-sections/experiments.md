# Exemplar: Experiments

本文件展示经典论文 Experiments 章节的组织方式。核心原则：设置可复现、对比全面、消融详尽、风险坦诚。

---

## 示例 1: ResNet (He et al., CVPR 2016)

**来源**: "Deep Residual Learning for Image Recognition", CVPR 2016

### 原文片段

> ## 4. Experiments
>
> ### 4.1. ImageNet Classification
>
> The network is trained on the ILSVRC 2012 classification dataset that consists of 1000 classes. The models are trained on the 1.28 million training images, and evaluated on the 50k validation images. We also obtain a final result on the 100k test images...
>
> **Training.** Our implementation for ImageNet follows the practice in [21, 41]. The image is resized with its shorter side randomly sampled in [256, 480] for scale augmentation [41]. A 224×224 crop is randomly sampled from an image or its horizontal flip...

### 写作要点

1. **数据集明确**: 训练/验证/测试集大小、类别数
2. **设置可复现**: 尺寸、数据增强、训练超参数都给出
3. **对比全面**: 与 VGG、GoogLeNet、PReLU-net 等对比

### 消融实验的典范

> ### 4.2. Analysis of Residual Networks
>
> To understand the behavior of residual networks, we conduct extensive ablation studies...

**消融内容包括：**
- 残差连接 vs 无残差
- 不同深度（18/34/50/101/152层）
- 不同残差函数（identity vs projection shortcut）

### 可迁移模式

```
[数据集描述] → [训练设置（可复现）] → [主结果表] → [与baseline对比] → [消融实验] → [分析/讨论]
```

---

## 示例 2: Transformer (Vaswani et al., NeurIPS 2017)

**来源**: "Attention Is All You Need", NeurIPS 2017

### 原文片段

> ## 5 Training
>
> This section describes the training regime for our models.
>
> ### 5.1 Training Data and Batching
>
> We trained on the standard WMT 2014 English-German dataset consisting of about 4.5 million sentence pairs...
>
> ### 5.2 Hardware and Schedule
>
> We trained our models on one machine with 8 NVIDIA P100 GPUs...
>
> ### 5.3 Optimizer
>
> We used the Adam optimizer with β1 = 0.9, β2 = 0.98 and ε = 10^-9...

### 写作要点

1. **按主题分节**: Data → Hardware → Optimizer → Regularization
2. **超参数完整**: 所有关键超参数都给出
3. **训练时间**: 具体到 GPU 数量和训练时长
4. **结果对比**: 与当时 SOTA 对比（BLEU 分数）

### 结果呈现

| Model | BLEU | Training Time |
|-------|------|---------------|
| GNMT + RL | 24.6 | - |
| Transformer (base) | 27.3 | 12 hours |
| Transformer (big) | 28.4 | 3.5 days |

**表格特点：** 包含 baseline、自己的多个变体、关键指标、训练效率

---

## 示例 3: Vision Transformer (Dosovitskiy et al., ICLR 2021)

**来源**: "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"

### 原文片段

> ## 4 Experiments
>
> We evaluate the representation learning capabilities of ResNet, Hybrid, and ViT.
>
> ### 4.1 Setup
>
> **Datasets.** To explore the scaling properties of the models, we use ILSVRC-2012 ImageNet dataset with 1k classes and 1.3M images...
>
> **Model Variants.** We compare ViT with ResNet and hybrid variants...

### 写作要点

1. **多种对比维度**: 不同架构（ViT vs ResNet vs Hybrid）、不同规模（base/large/huge）
2. **数据效率分析**: 预训练数据量 vs 下游性能的关系
3. **Scale 研究深入**: 探索模型大小、数据量、计算量的影响

---

## 通用 Experiments 结构模板

### 标准结构

```markdown
## Experiments

### Experimental Setup
- 数据集描述（大小、划分、预处理）
- 评价指标
- 实现细节（框架、硬件、超参数）
- Baseline 方法

### Main Results
- 主结果表格
- 与 SOTA 对比
- 分析（为什么有效）

### Ablation Studies
- 核心组件的贡献
- 超参数敏感性
- 设计选择的验证

### Analysis / Discussion
- 成功案例分析
- 失败案例分析
- 局限性讨论
```

---

## 各子节的写作要点

### Experimental Setup

| 内容 | 必要性 | 说明 |
|------|--------|------|
| 数据集大小 | 必须 | 训练/验证/测试样本数 |
| 数据划分 | 必须 | train/val/test split 方式 |
| 预处理 | 必须 | 归一化、数据增强方法 |
| 评价指标 | 必须 | 使用什么 metric，为什么选择它 |
| 实现框架 | 推荐 | PyTorch/TensorFlow 等 |
| 硬件配置 | 推荐 | GPU 型号、数量 |
| 超参数 | 必须 | learning rate、batch size、epochs |
| Baseline | 必须 | 与什么方法对比，为什么选择它们 |

### Main Results

**表格必备要素：**
- 方法名称
- 关键指标（加粗最好结果）
- Baseline 对比
- 训练/推理效率（可选）

**文本分析要点：**
- 指出关键观察
- 解释为什么某些设置更有效
- 与 baseline 对比时说明差异原因

### Ablation Studies

**消融实验类型：**
1. **组件消融**: 去掉某个模块，看性能下降多少
2. **超参数敏感性**: 关键超参数取不同值的影响
3. **设计选择验证**: 选择 A 而非 B 的理由

**写作模板：**
```
To understand the contribution of each component, we conduct ablation studies on [dataset]. As shown in Table X, removing [component A] leads to a [X]% drop in [metric], demonstrating its importance for [purpose].
```

---

## 常见错误

| 错误类型 | 表现 | 改进 |
|---------|------|------|
| 设置不完整 | 缺少关键超参数 | 提供完整的训练配置表 |
| Baseline 不公平 | 只选弱的 baseline | 包含 SOTA，说明公平对比条件 |
| 消融缺失 | 只有主结果，无消融 | 至少有一个核心组件的消融 |
| 过度声明 | 内部验证说成泛化 | 区分 "on validation set" 和 "generalization" |
| 失败案例缺失 | 只展示成功 | 添加 failure analysis |

---

## 写作建议

1. **设置部分要具体到可复现**: 别人读完后应该能重现你的实验
2. **表格要有分析**: 不要只放表格，要点出关键观察
3. **消融要回答"为什么有效"**: 不仅是"有效"，还要解释"为什么"
4. **诚实讨论局限性**: 主动说明方法的适用边界
5. **区分验证和泛化**: 明确说明结果是在哪个集合上获得的
