# Literature Reading Report Schema — 跨技能数据契约

**用途**: 文献阅读子代理（LiteratureReaderAgent）到论文编排器之间的论文阅读数据交换格式。
**生产者**: `literature-reader-agent` (由 `academic-paper-writer` Step 3 委托)
**消费者**: `academic-paper-writer` (Step 3 主 agent, 决定是否引用)

## 结构

```yaml
literature_reading_report:
  ref_id: string                  # 对应的引用编号，如 R001
  title: string                   # 论文标题

  # ——— 源信息 ———
  paper_available: boolean        # 是否能获取到论文全文
  source_of_content: enum         # full_text / abstract_only / metadata_only

  # ——— 核心主张（原文提取） ———
  core_claims:
    - claim: string               # 论文核心主张
      source_tag: "[原文]"        # 固定值，表示提取自原文

  # ——— 方法概述 ———
  method_summary: string          # 方法概述，1-3 句

  # ——— 关键结果 ———
  key_results:
    - result: string              # 主要结果/发现
      is_numerical: boolean       # 是否为数值型结果

  # ——— 可引用的 claim 列表 ———
  citable_claims:
    - claim: string               # 可被引用的 claim
      source: enum                # 原文 / 推断
     原文佐证: string | null      # 原文的具体语句（source=原文时必填，推断时为 null）
      confidence: enum            # high / medium / low
      suitable_purpose:           # background / method_comparison / baseline / dataset_source
        - string

  # ——— 关联度评估 ———
  relevance_to_current_work: enum # high / medium / low
  relevance_rationale: string     # 关联度判断依据

  # ——— 引用建议 ———
  recommendation: enum            # strongly_cite / cite / consider / skip
  recommendation_rationale: string

  # ——— 潜在风险 ———
  potential_risks:
    - risk: string                # 引用该文献的潜在风险
```

## 示例

```yaml
literature_reading_report:
  ref_id: R001
  title: "Attention Is All You Need"
  paper_available: true
  source_of_content: full_text

  core_claims:
    - claim: "Transformer 完全基于注意力机制，无需循环或卷积"
      source_tag: "[原文]"

  method_summary: "提出 Transformer 架构，使用自注意力机制（Scaled Dot-Product Attention + Multi-Head Attention）和位置编码替代循环结构。"

  key_results:
    - result: "WMT 2014 英德翻译 BLEU 28.4"
      is_numerical: true
    - result: "训练速度显著优于基于 RNN 的模型"
      is_numerical: false

  citable_claims:
    - claim: "Transformer 在 WMT 2014 英德翻译任务上达到 BLEU 28.4"
      source: 原文
      原文佐证: "Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task"
      confidence: high
      suitable_purpose:
        - baseline
        - method_comparison

    - claim: "自注意力机制能捕获长距离依赖"
      source: 推断
      原文佐证: null
      confidence: medium
      suitable_purpose:
        - background

  relevance_to_current_work: high
  relevance_rationale: "本文也使用注意力机制处理序列数据，Transformer 是核心基线"

  recommendation: cite
  recommendation_rationale: "Transformer 是该任务领域的标准基线，被广泛引用"

  potential_risks:
    - risk: "时间较早（2017），可能已被后续工作超越"
```
