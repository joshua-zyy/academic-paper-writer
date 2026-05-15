# 路径 B: arch-prompt 工作流

## 入口

用户请求 → 判断为模型架构图 → arch-prompt 模式

自动触发：academic-paper-writer 的 Step 7 在 Draft v1 完成后，会自动扫描正文中的 `[FIGURE_NEEDED]` 占位符，对架构图类占位符以 arch-prompt 模式调用本 Skill。

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
