# Section Moves

Use this file for phrase-level and move-level support when executing Prose Quality Gate. This file provides per-section move orders and phrase families, not the paper's overall writing strategy.

Derived from Academic Phrasebank and adapted for CS/AI/ML academic papers.

## Introduction

Questions this section must answer:

1. Why does the topic matter?
2. What is already known?
3. What is still missing or contested?
4. What does the present study ask or do?

Preferred move order:

1. establish importance
2. summarize what is known
3. identify a gap, limitation, or controversy
4. state the study aim
5. indicate value or approach

Useful phrase families:

- `Recent years have seen increasing interest in ...`
- `X is a central issue in ...`
- `Previous studies have shown that ...`
- `However, the mechanisms underlying ... remain poorly understood.`
- `Few studies have examined ...`
- `Here, we investigate whether ...`
- `This work provides ...`

Avoid:

- long historical throat-clearing
- detailed results
- inflated novelty claims before the gap is defined

## Related Work / Literature Review

Questions this section must answer:

1. What lines of work define the field?
2. What has been established?
3. Where do findings diverge or remain incomplete?
4. Which gap matters for the present paper?

Preferred move order:

1. describe the scope of existing work
2. identify dominant approaches
3. state what has been established
4. note disagreements or contradictions
5. isolate the missing piece

Useful phrase families:

- `A substantial body of work has focused on ...`
- `Most studies have relied on ...`
- `Previous work has established that ...`
- `Findings have been mixed regarding ...`
- `By contrast, little attention has been paid to ...`
- `No study has yet examined ...`

Avoid:

- citation-by-citation summary without grouping or synthesis
- treating all prior work as uniformly weak

## Method / Approach

Question this section must answer:

- Could another group reproduce the work from this description, or from this description plus a clearly cited protocol?

Preferred move order:

1. problem definition or notation
2. overall architecture or framework
3. core module descriptions (per module: purpose → input/output → mechanism → formula → rationale → boundary)
4. training objective or optimization
5. inference or prediction aggregation (if applicable)

Per-module narrative order:

1. pipeline duty (what problem does this module solve?)
2. why needed (bottleneck or gap it addresses)
3. why this design (rationale for the specific approach)
4. core mechanism and formula
5. expected benefit
6. boundary and cost / limitation

Useful phrase families:

- `To address the limitation of ..., we introduce ...`
- `Given that ..., we adopt ...`
- `Compared with ..., this design ...`
- `To enable ..., we further ...`
- `The module takes ... as input and produces ...`

Avoid:

- `under standard conditions`
- `using routine methods`
- formula listing without narrative context
- code walkthrough tone

## Experimental Setup

Question this section must answer:

- What data, protocol, implementation details, and evaluation metrics were used?

Preferred move order:

1. dataset description and preprocessing
2. evaluation protocol (splits, metrics, baselines)
3. implementation details (hyperparameters, hardware, software)
4. risk notes (data leakage, single-run, domain shift, etc.)

Useful phrase families:

- `We evaluate our method on ...`
- `The dataset consists of ...`
- `Following [ref], we adopt ...`
- `All experiments are conducted on ...`
- `We use ... as the evaluation metric`

Avoid:

- bare parameter listing without protocol context
- omitting risk notes or evaluation limitations

## Results

Question this section must answer:

- What was observed, under which condition, and with what evidence?

Preferred move order:

1. orient the reader to the figure, table, or experiment
2. state the main observation
3. add quantitative detail
4. note expected or unexpected patterns
5. compare with prior work only if it clarifies the result

Useful phrase families:

- `Table X shows ...`
- `As shown in Figure X, ...`
- `The most notable finding was that ...`
- `Contrary to expectations, ...`
- `No significant difference was observed in ...`
- `These results are consistent with ...`
- `In contrast to earlier reports, ...`

Avoid:

- discussion-length mechanism explanations
- repeating every visual detail from the figure
- claiming SOTA without complete baseline comparison

## Discussion / Limitations

Questions this section must answer:

1. What do the main findings mean?
2. How do they relate to earlier work?
3. Which explanations are plausible?
4. What limitations constrain interpretation?
5. What follows from the findings, and what does not?

Preferred move order:

1. restate the main finding
2. explain plausible reasons
3. compare with earlier work
4. note limitations
5. state implications
6. point to future work if needed

Useful phrase families:

- `Taken together, these findings suggest that ...`
- `A possible explanation is that ...`
- `This discrepancy may reflect ...`
- `These results should be interpreted with caution because ...`
- `An implication of this is that ...`
- `Further work is needed to determine whether ...`

Avoid:

- repeating the Results section in new words
- claiming mechanism when only association was shown
- vague "future work" without concrete next steps

## Conclusion

Questions this section must answer:

1. What was the central contribution?
2. Which finding matters most?
3. What implication follows, with what boundary?

Preferred move order:

1. return to the aim
2. summarize the decisive finding
3. state contribution or significance
4. give a boundary or forward look

Useful phrase families:

- `This study set out to ...`
- `The present findings indicate that ...`
- `These results extend our understanding of ...`
- `Notwithstanding these limitations, ...`
- `Further studies are required to ...`

Avoid:

- introducing new experiments
- ending on vague praise of the work
- overclaiming beyond what evidence supports

## Abstract

Questions this section must answer:

1. What problem or gap is being addressed?
2. What was done?
3. What was found?
4. Why should the reader care?

Preferred move order:

1. broad context
2. concrete gap
3. approach
4. key result with numbers if available
5. implication

Useful phrase families:

- `X remains challenging because ...`
- `Here, we ...`
- `Using ... , we found that ...`
- `We show that ...`
- `These findings suggest ...`

Keep the abstract selective. If a detail does not affect editorial triage, it probably does not belong.

## Title

Question this section must answer:

- Which few words make the paper searchable, accurate, and interesting without overclaiming?

Target properties:

- searchable
- specific
- restrained
- defensible

Useful patterns:

- `[Core entity] in/through/by [mechanism or context]`
- `[Process] shapes [outcome] in [system]`
- `[Signature/pattern/framework] of [phenomenon]`

Avoid:

- `A study of ...`
- vague hooks
- unverified `first`
- stacked jargon
