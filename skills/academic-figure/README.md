# Academic Figure

CS/AI/ML 学术论文图表生成 Skill。支持两类图表：

## 路径 A：实验数据图（自动出图）

给定实验数据，agent 生成 Python (matplotlib/seaborn) 代码并执行，输出符合发表标准的矢量图。

**支持的图表类型：**
- 训练/验证曲线（含置信带）
- 消融实验（分组柱状图 + hatching）
- 性能对比图（多数据集 × 多方法）
- 混淆矩阵（热力图）
- t-SNE/UMAP 散点图
- 箱线图 / 小提琴图
- 雷达图（多维度对比）
- 森林图（多任务效果汇总）

**输出格式：** SVG（主）、PDF、TIFF

**前置要求：** Python 3.8+，安装 `matplotlib seaborn numpy pandas scipy`

## 路径 B：模型架构图（生图提示词）

描述模型结构，agent 生成结构化生图提示词，你使用任意生图工具（Midjourney / DALL-E / Stable Diffusion 等）出图。

**支持的架构类型：**
- CNN / Encoder-Decoder / Transformer / GNN / 多模态 / Mixture-of-Experts

**返回内容：** 架构分析 + 生图提示词 + 使用说明

（可选）出图后可让 agent 协助排版、标注、与实验图整合。

## 使用示例

### 实验数据图
```
"根据这个 CSV 画出训练曲线，对比我们的方法和三个 baseline"
"帮我生成消融实验的柱状图，数据在这里"
"画一个混淆矩阵，显示分类结果"
```

### 模型架构图
```
"帮我生成一个 Transformer 架构图的提示词"
"画一个 GNN 编码器-解码器结构的描述图"
"我需要一个多模态融合架构的示意图提示词"
```

### 其他
```
"检查我的论文目前需要哪些图"
"审查一下这张图是否符合发表标准"
"帮我把这两张图合并成一个双面板图"
```
