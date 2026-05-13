# Orchestration Workflow — Step-by-Step Reference

This file contains the detailed step-by-step workflow for the core orchestrator.
Load this when executing the section drafting loop.

---

## Step 0: Mode, Scope, and Current Section

- Determine whether the task is full-paper planning, single-section drafting, revision, citation pass, or experiment pass.
- If the user names a section, set it as the current section unit.
- If the user asks to "write a paper," form an Outline / Section Queue and enter the serial section loop.
- For `full-paper-planning`, maintain two lists: Section Queue (pending) and Revision Queue (drafted but needs revision).

## Step 1: Confirm Key Information (Blocking Gate)

Blocking confirmations — must stop and ask if missing:

1. **Target venue**: Required for `full-paper-planning`, formal drafting, or substantial revision. Only fall back to generic CS/AI structure if user explicitly says "undecided."
2. **Draft language**: Required for formal drafting. Default to English if not specified.
3. **Current section**: Determined by Step 0 if user did not specify.

If venue is known and relevant, read `references/writing-guidelines.md` and form a brief Venue / Language Brief.

## Step 2: Evidence Audit

Create a todo list for evidence items. Dispatch probe agents per section type (parallel when multiple probes are needed):

| Section | Probe tasks |
|---------|-------------|
| Introduction | `existing_draft` |
| Related Work | `existing_draft` |
| Method | `code_structure` + `preprocessing` |
| Experimental Setup | `data_statistics` + `experiment_config` |
| Main Results | `experiment_data` + `baseline_results` |
| Ablation | `ablation_results` |
| Discussion | `interpretability` |

Single probe: dispatch one general subagent with `agents/probe-agent.md`.
Multiple probes: dispatch multiple subagents simultaneously, each with a different probe type.

After probes return, aggregate into an Evidence Map. Light-weight, section-targeted inventory only.

Determine paper type: empirical / theory / survey / reproducibility / position.

List four categories:
- Known facts
- Missing but blocking facts
- Missing but placeholder-acceptable facts
- Claims needing external validation

For Introduction / Related Work, also audit exemplar paper candidates.
For Method, also audit model data flow, module boundaries, tensor shapes, recoverable formulas.

## Step 3: Literature Search and Verification

- Create a todo list for keywords and expected reference counts.
- Determine search keywords and scope.
- Delegate to `academic-citation`.
- Mark todo completed after return.

Input: current section, research keywords, target venue.
Output: Verified References, Exemplar Set (for Intro/RW), Citation-to-Claim Map per `../shared/schemas/verified-references.md`.

Constraint: only VERIFIED references enter the draft body. UNVERIFIED entries stay in candidate lists.

## Step 4: Experiment Evidence Verification

- Create a todo list for experiment evidence items.
- Delegate to `academic-experiments` (only when empirical paper and current section needs experiment facts).

Input: repo path, current section.
Output: Experiment Evidence, Protocol Risks, Remaining Blockers per `../shared/schemas/evidence-inventory.md`.

Introduction / Related Work do not block on this step.

## Step 5: Generate Section Plan

- Create a todo list for plan core modules.
- Read `references/paper-structure.md` and select structure by paper type and venue.
- Generate Evidence Map: section goal, key claims, evidence sources, gaps.

**Introduction / Related Work must generate a Section Blueprint**:
- Exemplar Set observed structures
- Functional units or work clusters to retain
- Narrative duty per paragraph or subsection
- Dense citation spots vs. synthesis spots
- Differentiation from exemplars

**Method sections must generate a Method Blueprint**:
- Recommended subsection order
- Architecture figure placement and intent
- Core vs. standard modules
- Module Card per core module: position, bottleneck, design choice, rationale, expected benefit, cost/limit/boundary, evidence source

## Step 6: Draft v1

- Create a todo list for subtopics to cover.
- Check Evidence Map and Verified References.
- Generate Draft v1 Markdown body.
- Mark todos completed.

Body constraints:
- Paper Body = draft text only; critique/audit notes go to sidecar.
- Only use verified references and confirmed experiment facts for definitive claims.
- Placeholders:
  - `[REF_NEEDED: claim/topic]`
  - `[FIGURE_NEEDED: purpose | placement | why]`
  - `[TABLE_NEEDED: purpose | columns | why]`
  - `[RESULT_NEEDED: experiment/metric/source]`
  - `[RESULT_UNVERIFIED: claim | why]`
  - `[METHOD_DETAIL_NEEDED: description]`
  - `[RATIONALE_NEEDED: module | missing]`
  - `[DATASET_DETAIL_NEEDED: description]`

**Method section minimum requirements**:
- Overall framework first, with architecture figure placeholder at proper position.
- Separate subsection per core module.
- Per module: purpose, input/output or tensor dims, core operation, at least one key formula or pseudo-formula.
- Narrative order per core module: (1) pipeline duty (2) why needed (3) why this design (4) core mechanism & formula (5) expected benefit (6) boundary & cost.
- Standard/supporting components: role + input/output + core operation only.
- If design motive is only weakly inferable, downgrade tone explicitly (e.g., "该设计意在...", "从实现结构看...").

Reference list must only contain entries cited in body or declared via `[REF_NEEDED: ...]`.

## Step 7: Placeholder Audit, Architecture Figure Pre-generation, and Debt List

After Draft v1, automatically execute:

1. **Scan placeholders** — count and classify all placeholders by type and location.
2. **Fill missing architecture figure placeholders** — for Method section, scan module headings; if missing `[FIGURE_NEEDED]`, insert:
   ```
   [FIGURE_NEEDED: Figure X <module> module diagram | corresponding subsection | show internal structure, input/output, data flow]
   ```
3. **Auto-trigger architecture figure generation** — per `[FIGURE_NEEDED]`, classify:
   - Architecture/pipeline/structure diagrams → dispatch `academic-figure` in `arch-prompt` mode, replace placeholder with prompt.
   - Data/curve/comparison charts → keep placeholder, add to debt list (trigger later when data is ready).
4. **Append debt list** — after Draft v1 (after references), append:
   ```markdown
   ---
   ## Appendix: Pending Items
   *Not part of the formal body; internal draft status record only.*

   ### Pending
   1. [FIGURE_NEEDED] <data chart placeholders>
   2. [TABLE_NEEDED] <table placeholders>
   3. [RESULT_NEEDED] <result placeholders>
   4. [REF_NEEDED] <reference placeholders>
   5. [METHOD_DETAIL_NEEDED] / [DATASET_DETAIL_NEEDED] / [RATIONALE_NEEDED] <if any>
   6. (Other known gaps)
   ```
   Mark items as "none" if the category has no placeholders.
5. **Report audit result** — include placeholder statistics (`placeholder_debt`) in Section Critique for Step 11 Verification.

## Step 8: Evidence Compliance Review (Phase 1 of Two-Phase Review)

- Create a todo list for evidence compliance checks.
- Delegate to `academic-reviser` in `targeted-evidence-mode`.
- Check `evidence_debt` status.

This is Phase 1. Only proceed to Phase 2 (prose polishing) after `evidence_debt = closed`.

Input: Draft v1 text, Evidence Map, Verified References, placeholder_debt from Step 7.
Output: `evidence_debt` (open|closed), `evidence_issues` list.

If `evidence_debt = open`, record issues and return to Step 6. Do not proceed to Step 9 while open.

## Step 9: Prose Quality Gate (Phase 2 of Two-Phase Review)

- Create a todo list for prose checks.
- Confirm Step 8 `evidence_debt = closed` before executing.
- Delegate to `academic-polishing`.

Input: Draft v1 text, current section type.
Output: `prose_debt` (open|closed), `failed_items`, rewritten text. For Method, also `method_prose_debt`.

Prose rewrite loop: max 2 rounds. If still open after 2 rounds, carry `prose_debt: open` forward; final Verification cannot be `passed`.

## Step 10: Expansion Pass (Content Density Check)

- Create a todo list for thin-draft checks.

Thin-draft conditions:
- Introduction <= 2 paragraphs, or only background + contribution list
- Related Work is just paper name listing, no work clusters or synthesis
- Method is only overview, no module breakdown or formulas
- Experimental Setup is only parameter listing, no protocol or risk notes
- Discussion / Conclusion is only generic statements, no boundary analysis

Expansion principle: use only existing evidence and compliant placeholders. Prioritize filling "reader understanding chain" gaps.

## Step 11: Self-Review & Verification

- Create a todo list for review items.
- Delegate to `academic-reviser`.
- Check verdict and decide whether to advance or revise.

Input: Expanded Draft, Evidence Map, prior step states (`prose_debt`, `thin_draft`, `frozen_claims`, etc.).
Output: Self-Review, Revised Draft vN (must absorb fixes), Section Critique, Verification Status (`passed`/`failed`/`blocked`) per `../shared/schemas/verification-report.md`.

If `blocked`, must include `safe_to_continue` and `frozen_claims`. Only advance if `safe_to_continue = yes`.

## Step 12: Integration & Section Loop (Dependency-Aware)

For `full-paper-planning`, do not end after one section revision.

### 12a. Status Update

- If `failed` and not externally blocked → keep current section active, continue next Step 11 round.
- If `blocked` and `safe_to_continue = yes` → write blockers to Revision Queue, freeze claims, advance.
- If `blocked` and `safe_to_continue = no` → keep active, wait for external evidence.
- Merge into Cumulative Draft; update Section Queue and Revision Queue.

### 12b. Dependency Check

After current section passes Verification, read `references/section-dependency-matrix.md`:

1. Read current section's `depended_by` list.
2. Check which sections in that list are already completed (exist in Cumulative Draft).
3. Check if `shared_claims` changed (compare original Evidence Map vs current draft).
4. If changed → mark corresponding section's `revision_queue` status as `pending`.
5. Before advancing, ask user: "This section changed X (claim), which section Y depends on. Revise Y first?"
   - User confirms → move Y to head of Section Queue.
   - User skips → Y keeps `pending`, auto-rechecked when Y is completed later.

### 12c. Select Next Section

Choose from sections whose `depends_on` are all satisfied and `revision_queue` has no `pending`:

Priority:
1. All `depends_on` completed
2. No `pending` recheck markers among them
3. User-specified section

Continue until:
- Core sections have substantial drafts
- Blocking evidence gaps would significantly increase hallucination risk
- User explicitly requests pause

---

## Cross-Skill Data Contracts

| Contract | Producer → Consumer | Purpose |
|----------|---------------------|---------|
| `../shared/schemas/evidence-inventory.md` | `academic-experiments`, Step 2 → Step 6 | Experiment evidence |
| `../shared/schemas/verified-references.md` | `academic-citation` → Step 6 | Verified references |
| `../shared/schemas/verification-report.md` | `academic-reviser` → Step 11 | Verification status |

Shared references in `../shared/references/`:
- `evidence-classification.md` — evidence type definitions
- `placeholder-guide.md` — placeholder system spec
- `paper-types.md` — paper type definitions
- `mode-spectrum.md` — mode spectrum (fidelity vs originality)
- `data-access-levels.md` — cross-skill data access boundaries

## When to Read Which Reference

| Reference file | Load condition |
|----------------|---------------|
| `references/paper-structure.md` | Determining section structure and goals |
| `references/writing-guidelines.md` | Venue style adaptation |
| `references/iteration-control.md` | Entering Draft → Revision → Verification loop |
| `references/content-density.md` | Expansion Pass (Step 10) |
| `references/exemplar-sections/` | Before writing Intro / RW / Method / Experiments / Abstract |
| `references/test-scenarios.md` | Regression testing after skill changes |
| `references/section-dependency-matrix.md` | Step 12 dependency checks |
| `references/orchestration-workflow.md` | Executing detailed step workflow (this file) |
| `../shared/schemas/...` | Receiving/consuming cross-skill data |
| `../shared/references/...` | Understanding shared concepts |
