---
name: academic-paper-writer
description: "Core orchestrator for writing CS/AI/ML papers from scratch. Coordinates evidence audit, citation search, experiment verification, prose polishing, peer review, and figure generation across 6 sub-skills. Uses section-by-section drafting with Draft→Quality Gate→Expansion→Self-Review→Revision→Verification closed loop. Use when: writing a full paper draft from research notes or code repo, drafting paper sections one-by-one, coordinating multi-skill paper writing workflow, managing evidence-to-citation closed loop. Triggers on: 写论文, paper draft, 初稿, write introduction, draft method, 论文起草, full paper outline, section-by-section drafting, 证据闭环, 分节起草, academic paper writing, research paper drafting, write CS paper, draft AI paper, 从零写论文, 逐节写作."
---

# Academic Paper Writer (Core Orchestrator)

证据闭环型、分节推进的论文编排代理。协调六个子技能：Step 0→1→1.5→2→3→4→5→6→7→8→9。

## Router Protocol

1. Read `manifest.yaml`. It declares `always_load` files, `axes`, and `references.on_demand`.
2. Read every file listed under `always_load`. These are the skill's binding rules — not reference material.
3. Apply the loaded material as constraints:
   - `stance.md` defines core rules, sub-skill boundary, and scope.
   - `red-lines.md` defines absolute prohibitions. Do not negotiate these.
   - `output-contract.md` defines file outputs, deliverables, and completion criteria.
   - `anti-patterns.md` defines known failure modes and their correct alternatives.
   - `workflow.md` defines the Step 0-9 sequence summary.
   - `../shared/core/` policies define evidence, non-invention, and output boundaries.
4. Detect `mode`, `paper_type`, `section`, and `language` using manifest axes.
5. Echo the detected mode to the user before executing.
6. Reach for `references/` only when the manifest's `references.on_demand` condition is satisfied.

## Modes

| Mode | Purpose |
|---|---|
| `full-paper-planning` | From-scratch full paper (balanced spectrum) |
| `section-drafting` | Single section, narrowed evidence scope (balanced) |
| `section-revision` | Local evidence audit + rewrite (fidelity spectrum) |
| `related-work-or-citation-pass` | Delegate to academic-citation (fidelity spectrum) |
| `experiment-evidence-pass` | Delegate to academic-experiments (fidelity spectrum) |

## Sub-Skill Dispatch

| Task | Sub-Skill | Step |
|---|---|---|
| Venue research | academic-venue-research | Step 1.5 |
| Evidence audit | Probe agent | Step 2 |
| Citation search | academic-citation | Step 3 |
| Experiment audit | academic-experiments | Step 4 |
| Figure generation | academic-figure | Step 6.4 |
| Prose polishing | academic-polishing | Step 6.6 (internal) |
| Draft review | academic-reviser | Step 6.5 / 6.8 |

## Push Modes

| Mode | Behavior |
|---|---|
| `auto` (default) | Auto-advance after Verification; brief progress summary only |
| `step-by-step` | Pause after each section for user confirmation |

Switch anytime via user request.

## Hard Gates (A-E)

| Gate | Trigger | Condition | Failure |
|---|---|---|---|
| E: Venue | Step 1→2 | venue-brief.md exists | Blocked |
| A: Evidence | Step 2→6 | >= 1 usable evidence | Degradation or blocked |
| B: Citation | Step 3→6 | >= 1 VERIFIED or explicit no-literature | Section-dependent: Intro/RW blocked, Method may use placeholder |
| C: Verification | Step 6.8→7 | All hard debts closed + thin_draft=no | passed/failed/blocked |
| D: Citation Count | Step 8→output | Total >= min_citations | Warn, allow retry |

## 6.1 Pre-Draft Probe Rules

| Section | Probes to Dispatch | Strategy |
|---|---|---|
| Introduction | `existing_material` + local lit deep search + external lit search | **Must parallel** (3 Tasks) |
| Related Work | `existing_material` + local lit deep search + external lit search | **Must parallel** (3 Tasks) |
| Method | `code_structure` (Module Cards + tensor shapes + forward) + `preprocessing` | **Must parallel** |
| Experimental Setup | `experiment_setup` (hyperparams, dataset split, demographics) | Single probe |
| Results / Ablation | `experiment_results` (main results, baselines, ablation) | Single probe |
| Discussion | `interpretability` (interpretability results, network analysis) | Single probe |

## Default Section Queue

Abstract is post-posed, not in initial queue. Default: Introduction → Related Work → Method → Experimental Setup → Results → Discussion → Conclusion → Abstract.
