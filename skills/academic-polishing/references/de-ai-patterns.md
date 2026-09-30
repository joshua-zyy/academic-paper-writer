# 去假大空与过度防御

目的不是规避 AI 检测器，而是使正文具体、准确、有论证功能。

## 检查

- 空泛背景或评价：句子适用于任何论文？用已有研究对象、问题与证据替代，否则删，不造数字来显具体。
- 模板衔接：however/moreover 本身不是问题；检查两句实际是递进、对比还是因果，不能仅换另一个模板。
- 代码/流程说明：去掉“下面我们介绍”“从当前实现看”等内部口吻，真实实现写成方法，缺动机列待补。
- 重复：结果、图注、Discussion 是否重复同一完整数字和论点？各自承担呈现、解释与综合功能。
- 防御：删除空泛免责、重复“未来进一步验证”和假想审稿回应。Results 准确描述数据集与比较即可；必要局限在 Discussion 适度集中。

## 合成示例

原文：“Our powerful framework effectively captures robust features.”
若材料只支持加权聚合，改为：“The framework aggregates feature maps using the learned weights.” 不制造鲁棒或性能结论。

原文：“Our method significantly improves accuracy.”
已给数字为 82.1% 与 87.3%，改为具体结果；无统计依据不加 significantly，也不强制 appears。

原文：“需要指出，研究尚存在诸多不足，未来仍需进一步研究。”
无具体信息则删；确实影响解释的局限在 Discussion 根据作者材料具体说明，不套免责声明。

局部任务返回改写正文，缺材料留明确标记/建议；不要求所有结构或证据闭合才改语法与衔接。
