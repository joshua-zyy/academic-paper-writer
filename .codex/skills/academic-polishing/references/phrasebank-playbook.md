# Phrasebank Playbook (CS/AI/ML)

在确定段落的论证目标和章节定位之后使用本文档。提供 phrase 级别和搭配级别的写作支持，包括证据强度措辞、过渡与修辞动作。不能替代对段落本身功能的判断。

源自 Academic Phrasebank，针对 CS/AI/ML 论文写作惯例进行了补充适配。

## 证据强度动词

根据 `claim-strength.md` 定义的证据等级选择匹配的动词。

### Strong（仅当 Strong 条件全部满足时使用）

- `show`
- `demonstrate`
- `establish`
- `reveal`
- `identify`
- `outperform`
- `consistently improves`
- `achieves state-of-the-art on`
- `surpasses`

### Moderate（内部验证 / baseline 不全时使用）

- `suggest`
- `indicate`
- `support the view that`
- `are consistent with`
- `point to`
- `appears to improve`
- `tends to`
- `compares favorably against`
- `yields competitive results`

### Speculative（仅 user_claim / 无法复核时使用）

- `may reflect`
- `could arise from`
- `appears to`
- `seems likely`
- `might be explained by`
- `is hypothesized to`
- `requires further validation`
- `remains an open question whether`

### CS 论文特有高频动词用法场景

| 场景 | 强度 | 推荐动词 |
|------|------|---------|
| 报告主表结果（full baseline 对比） | Strong | `outperform`, `consistently improves`, `surpasses` |
| Ablation study 验证模块有效性 | Moderate→Strong | `confirm`, `validate`, `demonstrate the contribution of` |
| 报告参数敏感性分析 | Moderate | `suggest`, `indicate`, `reveal a trade-off between` |
| 报告定性/可视化结果 | Speculative→Moderate | `suggest`, `appear to`, `are qualitatively consistent with` |
| 声称 generalization | Strong（需多数据集验证） | `generalize to`, `transfer effectively to` |
| 报告负结果/failure case | Speculative | `may stem from`, `could be attributed to` |

## 证据强度搭配

证据强度形容词：

- weak：`limited`, `scant`, `insufficient`, `preliminary`
- developing：`growing`, `emerging`, `accumulating`
- strong：`robust`, `reliable`, `convincing`, `considerable`, `compelling`

有用模式：

- `The evidence presented here suggests that ...`
- `The available evidence supports the view that ...`
- `Current evidence raises important questions about ...`
- `The data point to a need for ...`

## 过渡词族

### 转折

- `however`
- `by contrast`
- `nevertheless`
- `despite this`
- `whereas`
- `on the other hand`
- `in contrast to these approaches`

### 递进

- `furthermore`
- `in addition`
- `moreover`
- `also`
- `additionally`
- `beyond this`

### 因果

- `therefore`
- `thus`
- `consequently`
- `as a result`
- `thereby`
- `as a consequence`

### 限定

- `notably`
- `importantly`
- `approximately`
- `in part`
- `at least in this setting`
- `under the studied conditions`

选择最小的连接词来完成功能。不要给每个句子都装饰一个过渡词。

## 段落衔接（避免重复）

优先使用以下模式而非反复的 `This suggests`：

- 重述名词：`Such heterogeneity ...`
- 定名短语：`The resulting gradient ...`
- 分词总结：`Taken together, ...`
- 零连接词推进（当逻辑已经足够明显时）

限制以指示代词开头的句子。每段通常一个就够了。

## CS 论文特有过渡与衔接场景

| 场景 | 推荐模式 |
|------|---------|
| 从 architecture overview 过渡到 component 细节 | `We now describe each component in detail.` |
| 从 method 过渡到 experiments | `To evaluate the effectiveness of ..., we conduct experiments on ...` |
| 从 main result 过渡到 ablation | `We further perform ablation studies to isolate the contribution of ...` |
| 从 quantitative 过渡到 qualitative | `Beyond quantitative results, we provide qualitative analysis in ...` |
| 从 one experiment 过渡到下一个 | `We next investigate the effect of ...` |

## Gap 语言

使用精确而非夸张的 gap 表述：

通用 gap：
- `remains poorly understood`
- `has not been examined in ...`
- `has received limited attention`
- `few studies have addressed ...`
- `evidence remains sparse for ...`
- `the extent to which ... remains an open question`

CS/AI/ML 特有 gap（更偏技术限制）：
- `Existing methods are limited by ...`
- `Current approaches struggle with ... , particularly in ...`
- `Despite its success, [prior method] fails to capture ...`
- `A key bottleneck is that ...`
- `Most prior work assumes ... , which may not hold in ...`
- `The performance of existing methods degrades significantly when ...`
- `There is no existing method that jointly addresses ...`
- `Existing benchmarks do not adequately test ...`

避免：

- `no one has ever studied`（几乎从来不是真的）
- `completely unknown`
- `ignored by all previous work`

## 与已有工作的比较

对齐时：

- `These results are consistent with ...`
- `This finding accords with ...`
- `Our observations broadly support ...`
- `Our results align with the findings of ...`

标记差异（保持公平）：

- `In contrast to earlier reports, ...`
- `This finding differs from ...`
- `One possible reason for this discrepancy is ...`
- `This divergence may be attributed to differences in ...`
- `Unlike [prior method], our approach ...`

CS/AI/ML 特有比较场景：

| 场景 | 推荐表述 |
|------|---------|
| 报告比 baseline 更好的结果 | `Our method outperforms [baseline] by ... across all metrics.` |
| baseline 在某些设置更好 | `We note that [baseline] performs better under ... , suggesting ...` |
| 讨论与 prior work 的差异原因 | `The discrepancy between our results and [prior work] may stem from differences in ...` |
| 定位自己的贡献 | `A key distinction of our work is that it addresses ... which prior methods do not handle.` |

## Limitation 语言

有用模式：

- `These findings should be interpreted with caution because ...`
- `A limitation of this study is that ...`
- `The generalisability of these results is limited by ...`
- `We cannot exclude the possibility that ...`
- `Another source of uncertainty is ...`
- `Our evaluation is constrained to ...`

CS/AI/ML 特有 limitation 表达：

- `Our method assumes access to ... , which may not be available in ...`
- `The computational cost of ... limits its applicability to ...`
- `We only evaluate on ... ; the performance on other datasets remains unknown.`
- `The design of ... introduces a trade-off between ... and ...`
- `Our analysis is limited to ... ; we leave extensions to ... for future work.`
- `The current implementation requires ... , which may hinder deployment in ... limitation 应与不确定性的实际来源配对，而非模糊的谦虚。`

## Implication 语言

有用模式：

- `An implication of this is that ...`
- `These findings may help to explain ...`
- `These data support further investigation of ...`
- `This work has implications for ...`
- `Our findings suggest that ... could be a promising direction for ...`

Implication 应保持在证据边界之内。

CS/AI/ML 特有 implication 表达：

- `Our results suggest that [design choice] is a critical factor for ...`
- `This finding provides a practical guideline for designing ...`
- `The observed trade-off implies that ... should be chosen based on ...`
- `Our analysis reveals that ... , which has implications for ...`

## Future-work 语言

有用模式：

- `Further work is needed to determine whether ...`
- `Future studies should examine ...`
- `A useful next step would be to ...`
- `Larger studies are required to validate ...`
- `Extending this approach to ... warrants investigation`

CS/AI/ML 特有 future-work 表达：

- `An immediate direction is to extend our method to ...`
- `It would be valuable to apply this approach to ...`
- `Future work could explore alternative ... designs, such as ...`
- `Reducing the computational cost of ... is an important direction for practical deployment.`
- `Integrating ... with our framework could further improve ...`
- `We leave the investigation of ... to future work.`

Future-work 应从实际的 limitation、不确定性或机会中自然生长出来。

## CS/AI/ML 论文专用短语补充

### 描述 contribution

- `We make the following contributions: (i) ... (ii) ... (iii) ...`
- `To the best of our knowledge, this is the first work to ...`
- `This paper introduces a novel framework for ... that jointly addresses ...`
- `Our work advances the state of the art by ...`

### 描述方法设计

- `To address this limitation, we propose ...`
- `The key idea is to ...`
- `We design ... to capture ...`
- `The core of our method is a ... module that ...`
- `Our architecture consists of three key components: ... , each serving a distinct purpose.`
- `We adopt [standard technique] as the backbone, and extend it with ...`

### 描述实验设置

- `We evaluate our method on ... benchmark, following the standard protocol in [ref].`
- `For fair comparison, we re-implement all baselines using their official code and tune them on the validation set.`
- `All models are trained on ... GPUs with ... as the framework.`
- `We report the mean and standard deviation over ... random seeds.`

### 描述 ablation 结果

- `To verify the contribution of ... , we conduct an ablation study by removing it from the full model.`
- `Replacing ... with ... leads to a performance drop of ... , confirming its effectiveness.`
- `Each component contributes positively; the most significant drop occurs when ...`
- `We further analyze the sensitivity of ... by varying ...`

### 描述 SOTA 比较

- `Our method achieves ... on ... , outperforming all baselines by a significant margin.`
- `Our approach ranks first on ... among all compared methods.`
- `We note that our method also achieves competitive performance on ...`
- `While [baseline] excels at ... , our method consistently performs better on ...`

### 描述计算代价

- `Our method requires ... FLOPs / parameters, which is comparable to [baseline].`
- `Despite its improved performance, our method introduces only ... additional computational overhead.`
- `The inference speed of our method is ... , making it suitable for real-time applications.`