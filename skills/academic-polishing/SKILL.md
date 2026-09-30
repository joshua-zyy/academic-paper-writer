---
name: academic-polishing
description: "改写、润色或压缩 CS/AI/ML 论文段落与章节，去除假大空、模板语言、逻辑断链和过度防御，保持事实、数字、引用和作者意图。支持 Method 叙事、局部重组及按主张类型检查过度表述。用于润色、逐段修改、去AI、rewrite method、polish、prose quality 或 claim audit。"
---

# Academic Polishing

读 manifest 与 always_load，选择最小请求范围。独立段落/章节直接改写，不要求 venue、整篇证据包或全部材料闭合；不凭空补事实。

| mode | 用途 |
|---|---|
| prose-quality-gate | 表达、衔接、局部结构、重复与压缩 |
| method-prose-rewrite | 方法操作、数据流与作者设计意图组织 |
| de-ai-pass | 删除假大空和机械模板，不按连接词黑名单替换 |
| claim-strength-audit | 按具体主张及范围检查，不一律降调 |

编排时由主 agent 内化执行，不 dispatch 写作者。独立调用当前 agent 可返回改写文本；事实缺失标明并列补充建议，仍可改善已支持的句段。需要改变核心主张先请作者确认。

默认交付改写文本与必要简短说明；作者要求仅正文就不附检查表。相同问题两轮无实质进展说明分歧，不循环到每句都“可能”。
