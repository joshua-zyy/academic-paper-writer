# arch-prompt 工作流

本路径不是默认论文绘图路径。只有用户明确要求“生成提示词”“外部生图工具 prompt”，且本轮不要求直接出图时才使用。一般论文架构图应使用 `architecture-image` 调用生图模型完成主体视觉。

## 入口

用户明确请求外部生图提示词 → `arch-prompt` 模式

禁止自动触发：academic-paper-writer 的 Step 6.4 对架构图类占位符默认调用 `architecture-image`。只有用户明确要求外部 prompt 且不要求本轮生成图片时，才调用本模式。

## Step 1：确认模型结构

用户提供或 agent 从论文上下文中提取：
- 核心组件列表（Embedding、Encoder × N、Decoder、Classifier 等）
- 数据流方向
- 关键连接方式（残差、跨层、注意力连接）
- 输出形式

## Step 2：选择提示词模板

按架构类型（详见 `references/architecture-prompting.md`）：
- CNN / Encoder-Decoder / Transformer / GNN / 多模态 / MoE

## Step 3：生成结构化提示词

- 风格控制：`scientific diagram, white background, flat 2D, vector illustration`
- 结构描述：自左向右或自顶向下布局、模块分组
- 标注要求：关键模块标注技术名称
- 配色方案：不同功能组用不同色系
- 连接方式：实线箭头=数据流，虚线=残差/跳跃连接

## Step 4：输出提示词 + 使用说明

- 提示词正文（通用描述式，不限定生图工具）
- 建议的后续步骤（用户自行出图后，可回传让 agent 协助排版/标注）

## Step 5（可选）：用户回传图后的协助

- 调整 panel 布局
- 添加标注文字 / 箭头
- 与实验图整合为 multi-panel 总图
