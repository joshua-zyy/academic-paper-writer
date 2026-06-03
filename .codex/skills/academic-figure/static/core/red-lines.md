# Red Lines（绝对禁止）

1. 不得虚构 data、experiment results、model modules、architecture connections、losses、datasets 或 training flows。
2. 不得使用高饱和 rainbow-style 色板，或用视觉效果暗示没有统计支持的确定性。
3. 实验数据图不得缺少可编辑矢量输出；主格式为 SVG，文字保持可编辑。
4. 架构图、overview figure 和复杂机制图不得默认强行使用 Python/SVG；默认应走生图模型工作流，除非用户明确要求简单可编辑矢量图。
5. 不得把未经核对的架构图当作事实性最终图；必须有 Architecture Contract 和人工可核对清单。
6. 不得覆盖源数据或项目代码。只能为图表交付创建新脚本或输出文件。
7. 不得在 prompt 兼容路径中加入不可渲染或不受证据支持的细节。
8. 不得跳过 QA Contract。所有图表输出必须在交付前完成 QA。
9. 用户要求出图时不得只交付 prompt；若生图模型不可用，必须标注 blocker 和待执行提示词状态。
