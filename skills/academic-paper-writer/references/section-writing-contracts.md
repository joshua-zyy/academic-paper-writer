# Section Writing Contracts

Use this reference before drafting or revising any CS/AI/ML paper section. A section contract defines the argumentative job of the section: what the reader must understand, what evidence must be present, what order best supports the claim, and what failure modes make the section weak even if the prose is fluent.

## How To Use

For the current section, create a brief contract before writing prose:

1. **Reader state before**: what the reader knows entering the section.
2. **Reader state after**: what the reader must believe or understand after the section.
3. **Required moves**: the minimum rhetorical moves below for this section type.
4. **Evidence hooks**: verified citations, artifact facts, results, figures, or placeholders needed for each move.
5. **Failure checks**: section-specific anti-patterns to avoid.

If a required move lacks evidence, keep an explicit placeholder such as `[REF_NEEDED: ...]`, `[RESULT_NEEDED: ...]`, `[TABLE_NEEDED: ...]`, or `[METHOD_DETAIL_NEEDED: ...]`. Do not hide missing evidence through smoother prose.

**Citation format**: Default to numeric style; follow explicit author or verified venue requirements for author-year. Maintain one shared References list.

Use these moves at the requested scale, not as quotas. Local edits need only relevant checks. Missing material permits a clear framework and specific completion advice, not a global writing block.

## Abstract

**Job**: Give a self-contained, evidence-calibrated version of the paper after the main claims are stable.

Required moves:

1. State the concrete problem setting, not a generic field slogan.
2. Identify the specific gap or limitation that motivates the work.
3. Name the proposed method and its central mechanism in one compact sentence.
4. Report the strongest verified result or main empirical finding with its scope.
5. State the takeaway without adding claims absent from the body.

Failure checks:

- Written before Method and Results are stable.
- Contains broad motivation that could fit any paper in the field.
- Uses "significant", "robust", "SOTA", or "generalizes" without matching evidence.
- Introduces a contribution, dataset, or result not present in the body.

## Introduction

**Job**: Convert a broad research area into a precise unresolved problem and show why the proposed paper is a necessary response.

Required moves:

1. Establish the important phenomenon or task with field-specific context.
2. Narrow from broad context to the concrete modeling or evaluation problem.
3. Synthesize prior work by approach clusters rather than by paper list. For each cluster, state representative works, what the cluster enables, what residual limitation remains, and how that limitation maps to the paper's concrete gap.
4. Identify the remaining gap and explain the cost of leaving it unsolved.
5. Present the proposed bridge: what is modeled, how it differs, and why it addresses the gap.
6. Summarize verified contributions and, when available, key results within their true scope.

Mini-template for the prior-work move:

`Work cluster -> capability boundary -> residual limitation -> mapped gap/problem in this paper`

Failure checks:

- Opens with generic "deep learning has achieved success" background.
- States a gap but not why the gap matters.
- Lists modalities, modules, or techniques before establishing the research problem.
- Uses "method A did X, method B did Y" paper parade without cluster-level capability and limitation synthesis.
- Adds only a vague final sentence such as "however, limitations remain" after listing papers, instead of mapping each cluster's limitation to the next gap paragraph.
- Claims novelty through adjectives rather than contrast with verified prior work.
- Uses contribution bullets to compensate for a missing narrative chain.

## Related Work

**Job**: Position the paper against prior work by organizing the literature into meaningful clusters and making the closest distinctions explicit.

Required moves:

1. Define 2-4 work clusters that matter for this paper’s claim.
2. For each cluster: summarize the shared idea, representative works, achieved capability, and shared limitation.
3. Identify the closest competing or enabling works and state the exact difference.
4. Close each cluster or the whole section with how the present work is positioned.

Failure checks:

- Chronological paper parade with one sentence per citation.
- Citation bomb without synthesis.
- Omits the closest baseline or uses weak comparisons to make the method look novel.
- Says "unlike previous work" without naming the relevant previous work.

## Method

**Job**: Make the proposed system reproducible and rational: what it computes, why each core design is needed, and what boundaries the design has.

Required moves:

1. Define notation, inputs, outputs, and task formulation.
2. Give an architecture overview before module details, with a figure placeholder when helpful.
3. Explain core design, mechanism and author-provided rationale; use formulas where needed. Do not require a boundary/cost sentence or formula for every module.
4. For standard modules: state role, input/output, and operation without overclaiming novelty.
5. Describe training objective, optimization, inference procedure, and any aggregation or thresholding.

Failure checks:

- Code walkthrough instead of method description.
- Layer dump without rationale.
- All modules receive equal narrative weight despite unequal novelty.
- Formula-heavy text with no explanation of why the operation exists.
- Missing tensor shapes, input/output contracts, or loss/inference details.

## Experimental Setup

**Job**: Make the empirical protocol auditable and fair before results are interpreted.

Required moves:

1. Describe datasets, inclusion/exclusion criteria where relevant, preprocessing, sample counts, and splits.
2. Define evaluation metrics and why they fit the task.
3. List baselines and explain implementation source or tuning protocol.
4. Report training details, hyperparameters, compute, seeds, and selection criteria.
5. Identify missing actual protocol details for author completion; discuss necessary limitations in Discussion rather than appending defensive disclaimers here.

Failure checks:

- Treats community defaults as if they were verified project facts.
- Reports metrics without split strategy or class balance.
- Compares against baselines without fairness details.
- Omits the actual protocol or replaces unknown details with community defaults.

## Main Results

**Job**: Answer the primary empirical question with tables or figures and conservative interpretation.

Required moves:

1. Name the question answered by the result table or figure.
2. Present the main quantitative comparison with metric definitions and scope.
3. Interpret patterns across metrics, not just the best number.
4. Compare against baselines only within the verified protocol.
5. State the finding in its actual scope directly; concentrate necessary limitations in Discussion.

Failure checks:

- Cherry-picks one favorable metric while ignoring others.
- Converts internal validation into external generalization.
- Uses "outperform" or "SOTA" without complete, fair comparison.
- Gives numbers without traceability in the evidence record; internal paths/types do not belong in paper prose.

## Ablation And Analysis

**Job**: Test whether the proposed explanation for performance is credible.

Required moves:

1. State the hypothesis tested by each ablation or analysis.
2. Define the intervention: removed module, replaced component, changed parameter, or alternative protocol.
3. Report the effect size and direction, including uncertainty when available.
4. Interpret whether the result supports, weakly supports, or fails to support the design rationale.
5. Connect analysis back to Method claims without inventing causality.

Failure checks:

- Ablation only removes easy-to-remove components, not the claimed novelty.
- No hypothesis before showing a table.
- Treats correlation, attention weight, or visualization as causal proof.
- Ignores negative or ambiguous ablation outcomes.

## Discussion And Limitations

**Job**: Explain what the findings mean beyond the tables, while making boundaries explicit.

Required moves:

1. Synthesize the main findings rather than repeat results.
2. Explain plausible mechanisms or implications with citations or cautious language.
3. State limitations tied to data, protocol, model assumptions, compute, or deployment context.
4. Describe failure modes or conditions under which claims may not hold.
5. Give concrete future work that follows from the limitations.

Failure checks:

- Repeats Results paragraph by paragraph.
- Uses limitations as a generic disclaimer with no connection to the paper.
- Converts observations into clinical, causal, or deployment claims.
- Future work is a broad wish list rather than a direct response to limits.

## Conclusion

**Job**: Leave the reader with the paper’s defensible contribution and scope.

Required moves:

1. Restate the problem and proposed method in one concise sentence.
2. Summarize the main verified result or finding within scope.
3. State the takeaway for the research community.
4. Optionally name one concrete next step.

Failure checks:

- Copies the Abstract or contribution list.
- Introduces new evidence, citations, or claims.
- Ends with inflated claims that were not earned by the experiments.

## Scope and sufficiency check

Check the argumentative function against available material. Repair missing transitions when facts exist; otherwise retain a clearly identified outline/placeholder and describe the material needed. No mandatory paragraph/cluster count, citation minimum, optional ablation, or global evidence-closure gate.

Key factual prose links to author materials or located evidence. External claims use identity-checked references with a separate content-support mapping. Do not hide gaps with fluent prose or convert author hypotheses into findings. Acceptance follows the shared verification-report contract, not a second debt system.
