# Architecture Prompting: 模型架构图生图提示词

`arch-prompt` 模式中生成结构化生图提示词的参考。提示词为工具无关的描述式模板，用户可适配到任意生图工具。

## 提示词编写原则

### 风格控制
所有提示词应包含以下风格约束：
```
scientific diagram, white background, flat 2D vector illustration style, 
clean and minimal, no shadows, no 3D effects, publication-quality
```

### 顶会风格参考
生成的提示词应参考 NeurIPS / CVPR / AAAI / ICLR / ICML 等顶会论文的插图风格：
- **简洁扁平化**：避免 3D 效果、渐变、阴影和过度装饰
- **学术色板**：使用色盲友好、灰度打印安全的配色（蓝 #0F4D92、绿 #27AE60、橙 #E67E22、红 #B64342、紫 #8E44AD、灰 #A0A0A0）
- **字体**：统一 Arial / Helvetica，无衬线
- **对齐**：模块间距均匀，水平和垂直居中精确
- **标注**：字体大小确保在最终出版尺寸（单栏 85mm / 双栏 175mm）下可读
- **连接**：实线箭头表示数据流，虚线表示残差/跳跃连接，线宽 1.5-2px

### 布局控制
| 架构类型 | 推荐布局 |
|---------|---------|
| CNN / 前馈网络 | 自左向右 |
| Encoder-Decoder | 左（Encoder）→ 中（Bottleneck）→ 右（Decoder） |
| Transformer | 自左向右，纵向展开每层内部 |
| GNN | 从上到下或从左到右 |
| 多模态 | 两条或多条平行管道汇合 |
| MoE | 自左向右，底部展开 Expert 层 |

### 标注控制
- 关键模块必须标注技术名称
- Tensor 维度在连接点标出
- 数据流方向用箭头指示
- 使用无衬线字体

## 按架构类型的提示词模板

### 1. CNN / 卷积网络

```
Scientific diagram of a [任务名] CNN architecture, white background, flat 2D vector illustration.

Layout: left to right flow.

Components (left to right):
1. [蓝色] Input: [输入尺寸描述]
2. → 灰色箭头
3. [绿色] Conv Block × [N]: [kernel_size, channel info]
4. → [可选: 池化层标注]
5. [绿色] Conv Block × [K]: [kernel_size, channel info]
6. → [可选: Global Average Pooling]
7. [橙色] FC Layer × [M]: [hidden_dim]
8. → [红色] Output: [输出描述]

Colors:
- Blue: input layer
- Green: convolutional layers (darker green for deeper layers)
- Orange: fully connected / classifier layers
- Red: output layer
- Gray: arrows and skip connections

Arrows: solid arrows for forward pass.
Labels: each block labeled with layer name and kernel/output size in Arial 10pt.
```

### 2. Encoder-Decoder

```
Scientific diagram of a [任务名] encoder-decoder architecture, white background, flat 2D vector illustration.

Layout: left (Encoder) to center (Bottleneck) to right (Decoder).

Encoder (left, top-down or left-right):
- [蓝色] Input → [绿色] Conv block × [N] → Downsampling

Bottleneck (center):
- [紫色] Bridge module: [描述]

Decoder (right):
- [橙色] Up-conv block × [N] → [蓝色] Output
- Skip connections: dashed gray arrows from each encoder layer to corresponding decoder layer

Labels:
- Each block: module name + feature map dimensions
- Arrows labeled with operation type (conv 3x3, max pool 2x2, up-conv 2x2)
- Skip connection arrows annotated with "skip connection"

Color scheme: encoder in blues, bottleneck in purple, decoder in oranges.
```

### 3. Transformer

```
Scientific diagram of a Transformer model architecture, white background, flat 2D vector illustration.

Layout: left to right with vertical expansion for internal blocks.

Components (left to right):
1. [蓝色] Input Embedding: [vocab_size → d_model, positional encoding]
2. → gray arrow labeled "d_model"
3. Large vertical block "Transformer Encoder × [N]":
   - [浅绿] Multi-Head Self-Attention: [num_heads, head_dim]
     - ← dashed arrow showing residual connection around attention
   - [浅绿] Add & Layer Norm
   - [浅绿] Feed-Forward Network: [d_ff dimension]
     - ← dashed arrow showing residual connection around FFN
   - [浅绿] Add & Layer Norm
4. → gray arrow
5. [绿色] Transformer Decoder × [N] (if applicable):
   - [浅橙] Masked Multi-Head Self-Attention
   - [浅橙] Cross-Attention (keys/values from encoder)
     - ← arrow from encoder output labeled "K, V"
   - [浅橙] Feed-Forward Network
6. → [橙色] Output: [linear + softmax, output_dim]

Annotations:
- Show d_model dimensions at key points
- Label attention heads
- Mark positional encoding injection point

Color scheme:
- Blue: embedding layer
- Green family: encoder (lighter=pre-norm, darker=post-norm)
- Orange family: decoder
- Gray dashed: residual/skip connections
```

### 4. GNN / 图神经网络

```
Scientific diagram of a [任务名] Graph Neural Network architecture, white background, flat 2D vector illustration.

Layout: left to right.

1. [蓝色] Input Graph: [N nodes, features per node]
   - Show a small example graph with circles (nodes) and lines (edges)
2. → gray arrow
3. [绿色] GNN Layer × [K]:
   - Node: message passing from neighbors + aggregation + update
   - Visual: show one node receiving messages from its neighbors
   - Label: "Message Passing: aggregate neighbor features → update node embedding"
4. → gray arrow
5. [绿色] GNN Layer (if k>1): repeat with wider embeddings
6. → [可选: [紫色] Graph Readout / Pooling: sum, mean, or attention pooling]
7. [橙色] MLP Classifier / Predictor: [hidden_dim × N → output_dim]
8. [红色] Output: [预测任务描述]

Colors:
- Blue: input graph
- Green: GNN layers (darker for deeper layers)
- Purple: readout/pooling
- Orange: classifier
- Red: output

Annotations:
- Node dimensions at each stage
- Message passing direction with arrows between node groups
```


### 5. 多模态融合

```
Scientific diagram of a [任务名] multimodal fusion architecture, white background, flat 2D vector illustration.

Layout: two parallel pipelines that converge at fusion point.

Top pipeline — [模态1名称]:
1. [蓝色] Modality A Input: [描述]
2. → [绿色] Encoder A: [模型/结构]
3. → [蓝色] Modality A Features

Bottom pipeline — [模态2名称]:
1. [红色] Modality B Input: [描述]
2. → [橙色] Encoder B: [模型/结构]
3. → [红色] Modality B Features

Fusion point — center:
4. [紫色] Fusion Module:
   - Arrow from Modality A Features entering top
   - Arrow from Modality B Features entering bottom
   - Label: [concat/attention/cross-attention/addition mechanism]
   - [紫色] Fused Representation

5. → gray arrow
6. [橙色] Output Head: [classifier/decoder/predictor]
7. [红色] Final Output: [任务描述]

Annotations:
- Feature dimensions at each stage
- Fusion method highlighted with a distinct shape (rounded rectangle)
- Attention weights visualization if applicable
```


### 6. Mixture-of-Experts (MoE)

```
Scientific diagram of a Mixture-of-Experts architecture, white background, flat 2D vector illustration.

Layout: left to right with expert layer expanded at bottom.

1. [蓝色] Input: [dimension]
2. → gray arrow
3. [绿色] Shared layers / embedding
4. Gate / Router:
   - [橙色] Router/Gate: softmax routing weights
   - Show routing decision: "top-k selection"
5. Experts layer (expanded vertically below main flow):
   - [浅蓝] Expert 1: [FFN/architecture]
   - [浅蓝] Expert 2: [FFN/architecture]
   - [浅蓝] Expert N: [FFN/architecture]
   - Dashed arrows from router to selected experts
6. → [紫色] Weighted sum of expert outputs
7. → [橙色] Output: [task description]

Colors:
- Blue: input and shared components
- Orange: routing/gating mechanism
- Light blue: individual experts
- Purple: combined output
- Gray: arrows

Annotations:
- Routing weights shown on arrow labels
- Expert capacity / load balancing noted
```
