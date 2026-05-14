# Phrasebank Playbook

Use this file after the main argument and section role are already clear. It provides phrase-level and collocation support for evidence hedging, transitions, and rhetorical moves. Not a substitute for deciding what the paragraph is trying to do.

Derived from Academic Phrasebank, adapted for CS/AI/ML academic papers.

## Evidence strength verbs

Choose verbs that match the evidence level defined in `claim-strength.md`.

### Strong（仅当 Strong 条件全部满足时使用）

- `show`
- `demonstrate`
- `establish`
- `reveal`
- `identify`
- `outperform`
- `consistently improves`

### Moderate（内部验证 / baseline 不全时使用）

- `suggest`
- `indicate`
- `support the view that`
- `are consistent with`
- `point to`
- `appears to improve`
- `tends to`

### Speculative（仅 user_claim / 无法复核时使用）

- `may reflect`
- `could arise from`
- `appears to`
- `seems likely`
- `might be explained by`
- `is hypothesized to`
- `requires further validation`

## Evidence collocations

Adjectives for evidence:

- weak: `limited`, `scant`, `insufficient`
- developing: `growing`, `emerging`, `accumulating`
- strong: `robust`, `reliable`, `convincing`, `considerable`

Useful patterns:

- `The evidence presented here suggests that ...`
- `The available evidence supports the view that ...`
- `Current evidence raises important questions about ...`
- `The data point to a need for ...`

## Transition families

### Contrast

- `however`
- `by contrast`
- `nevertheless`
- `despite this`
- `whereas`
- `on the other hand`

### Addition

- `furthermore`
- `in addition`
- `moreover`
- `also`
- `additionally`

### Consequence

- `therefore`
- `thus`
- `consequently`
- `as a result`
- `thereby`

### Qualification

- `notably`
- `importantly`
- `approximately`
- `in part`
- `at least in this setting`

Prefer the smallest connective that does the job. Do not decorate every sentence with a transition word.

## Paragraph linking without repetition

Prefer these patterns over repeated `This suggests`:

- restate the noun: `Such heterogeneity ...`
- definite noun phrase: `The resulting gradient ...`
- participial summary: `Taken together, ...`
- zero-connective progression when the logic is already obvious

Limit demonstrative-led openings. One per paragraph is usually enough.

## Gap language

Use gap statements that are precise rather than dramatic:

- `remains poorly understood`
- `has not been examined in ...`
- `has received limited attention`
- `few studies have addressed ...`
- `evidence remains sparse for ...`
- `the extent to which ... remains an open question`

Avoid:

- `no one has ever studied`
- `completely unknown`
- `ignored by all previous work`

## Comparison with prior work

To align with earlier work:

- `These results are consistent with ...`
- `This finding accords with ...`
- `Our observations broadly support ...`

To mark divergence fairly:

- `In contrast to earlier reports, ...`
- `This finding differs from ...`
- `One possible reason for this discrepancy is ...`

## Limitation language

Useful patterns:

- `These findings should be interpreted with caution because ...`
- `A limitation of this study is that ...`
- `The generalisability of these results is limited by ...`
- `We cannot exclude the possibility that ...`
- `Another source of uncertainty is ...`
- `Our evaluation is constrained to ...`

Pair limitation language with the actual source of uncertainty, not with vague modesty.

## Implication language

Useful patterns:

- `An implication of this is that ...`
- `These findings may help to explain ...`
- `These data support further investigation of ...`
- `This work has implications for ...`

Implications should stay within the evidence boundary.

## Future-work language

Useful patterns:

- `Further work is needed to determine whether ...`
- `Future studies should examine ...`
- `A useful next step would be to ...`
- `Larger studies are required to validate ...`
- `Extending this approach to ... warrants investigation`

Future work should emerge from an actual limitation, uncertainty, or opportunity.
