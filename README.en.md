# 📝 Academic Paper Writer

[简体中文](README.md) | **English**

Evidence-driven · Automatic progression · One lead writer · Parallel evidence gathering · Content-draft delivery

[Project Website](https://joshua-zyy.github.io/academic-paper-writer) · [GitHub Issues](https://github.com/joshua-zyy/academic-paper-writer/issues) · [MIT License](LICENSE)

Eight Agent Skills for CS / AI / ML papers. Start a single workflow to organize evidence gathering, writing, section acceptance checks, and manuscript-wide acceptance checks around the author's existing materials and ideas. By default, the workflow progresses automatically toward a usable **paper content draft**. Later, sections or paragraphs can be edited independently without restarting the full-paper workflow.

Available materials determine the depth of delivery: supported content becomes prose, while missing material is handled with concrete outlines and suggestions for what to provide. The workflow does not invent results, motivations, methods, or references; present an outline as a nearly submission-ready manuscript; or promise publication acceptance.

## Contents

- [Skills Overview](#skills-overview)
- [Quick Start](#quick-start)
- [Recommended Configuration](#recommended-configuration)
- [Core Design](#core-design)
- [Orchestrator Workflow](#orchestrator-workflow)
- [Usage Examples](#usage-examples)
- [Documentation Layers](#documentation-layers)
- [Safety Boundaries](#safety-boundaries)
- [Maintenance and Verification](#maintenance-and-verification)
- [Reference Projects](#reference-projects)

## Skills Overview

| Skill | Responsibility | Standalone Uses |
|-------|----------------|-----------------|
| **academic-paper-writer** | Lead writing and orchestration, evidence reuse, section and manuscript integration | Full-paper drafts, section drafting and revision |
| **academic-citation** | Local-first search, with separate checks for reference identity and source support | Targeted citation search, verification, and claim mapping |
| **academic-experiments** | Read-only inventory of protocols, data, results, and factual conflicts by default | Trace results, clarify protocol descriptions, and recalculate within an authorized scope |
| **academic-reviser** | A single artifact-acceptance role reporting issues and conditions for resolving them | Section, manuscript, or targeted checks; does not rewrite the body text |
| **academic-polishing** | Prose, argumentation, and claim scope; applied internally by the lead writer during full-paper orchestration | Section, paragraph, and sentence rewrites |
| **academic-figure** | Source-backed data figures and consistency between figures, captions, and prose | Generate, check, or revise data figures; architecture diagrams are supplied by the author |
| **academic-venue-research** | Separate current official requirements from style observations in example papers | Targeted research on submission requirements or writing style |
| **academic-latex-layout** | Standalone typesetting, float placement, and template adaptation | Explicitly requested layout work; not part of the default content-draft workflow |

## Quick Start

### Option 1: Claude Code Plugin Installation (Recommended)

```text
/plugin marketplace add joshua-zyy/academic-paper-writer
/plugin install academic-paper-writer@academic-paper-writer
```

For the stable branch, use `/plugin marketplace add joshua-zyy/academic-paper-writer@stable`. To update, run `/plugin update academic-paper-writer@academic-paper-writer`; automatic updates depend on your platform settings.

After installation, use `/academic-paper-writer`. For specialized requests, use `/academic-citation`, `/academic-experiments`, `/academic-reviser`, `/academic-polishing`, `/academic-figure`, `/academic-venue-research`, or `/academic-latex-layout`.

### Option 2: Codex CLI Installation

```bash
# User-level directory
 git clone https://github.com/joshua-zyy/academic-paper-writer.git ~/.agents/skills/academic-paper-writer
# For stable: git clone -b stable <repository-url> <directory>
# To pin a version: git clone -b <existing-tag> <repository-url> <directory>
```

Run `git pull` inside the installation directory. Before switching versions, check for local changes, then use `git checkout stable` or the desired tag. Skill discovery depends on the current platform version.

### Option 3: Manual Loading

```bash
git clone https://github.com/joshua-zyy/academic-paper-writer.git
```

Load `skills/academic-paper-writer/SKILL.md` in a platform that supports Skills. For a specialized request, load the corresponding subskill directly. If the host supports subagents, evidence gathering can run in parallel. Otherwise, the main agent takes on the same responsibilities and discloses the fallback; it must not fabricate dispatch records.

### Prepare Materials and a Local Literature Library

Code, notes, research ideas, existing drafts, logs, CSV files, and figures are all valid inputs. A complete repository or a full set of experiments is not required. Provide the material locations and writing language to begin the necessary inventory; the target venue may remain undecided.

**Before starting, we recommend building a reusable Markdown library from local PDFs with MinerU.** Keep references intended for citation separate from venue-style examples. Reuse existing libraries and add new papers incrementally as needed. Converting every PDF is not mandatory. A missing `_index_ref.json` does not block writing, and unreadable source content only affects judgments that depend on it.

```powershell
# <citation_skill_dir> is the absolute path to the installed academic-citation skill
$env:MINERU_API_TOKEN = "<token>"
python "<citation_skill_dir>/scripts/convert-pdfs-to-md.py" "<pdf_dir>" "<md_dir>" --type ref
# Use --type style for a style library
```

The MinerU API uploads PDFs. Uploading sensitive or unpublished material requires explicit authorization; tokens must not appear in manuscripts or state files. Successful conversion and an available index do not establish reference identity or support for a claim.

The project consists primarily of skill documents and helper scripts, with no additional shared runtime. PDF conversion requires Python 3.10+ and a MinerU API token. Data plotting uses dependencies such as matplotlib as needed; they are not installed automatically. Public tests and contract checks use only the Python standard library.

## Recommended Configuration

### Recommended Models

| Model | Notes |
|-------|-------|
| **claude-opus-5.5** | API offered by anyRouter; see https://anyrouter.top/register?aff=hZXa |
| **gpt-6-astra** | API offered by agentRouter; see https://agentrouter.org/register?aff=Wpuc |
| **DeepSeek V4.1 Flash** | Can be used to test the skills |

Model names, availability, and pricing depend on the provider's current documentation. The author decides whether sensitive material may be sent to a model or relay service.

### Agent Platforms

| Platform | Loading Method |
|----------|----------------|
| OpenCode | Load Skills according to platform settings and use subagent dispatch |
| Claude Code | Plugin installation |
| Codex CLI | Local Skills directory |
| Other platforms | Load SKILL.md and operate within the host's capabilities |

## Core Design

### One Lead Writer, Supported by Evidence Gathering and Acceptance Checks

The main agent is the sole author of the manuscript body, responsible for drafting, polishing, revising, and merging. Evidence-gathering subagents return **facts, source locations, conflicts, and gaps**. The acceptance-check subagent returns **issues, supporting grounds, and conditions for resolving them**, not draft sections or revised prose.

The first round gathers evidence on methods, protocols/results, and literature in parallel, then reuses it across sections. Subsequent investigation targets specific gaps rather than rereading the entire repository or library for each section. Tasks specify their scope, read/write paths, authorization, and stopping conditions. Figure agents create only authorized figures and scripts in assigned directories; they do not modify research source files or manuscript prose.

### State Supported Facts Directly, Without Mechanical Hedging

Distinguish author-provided results and facts from design intent and unverified hypotheses. Do not reject all author material, or treat it all as verified. State supported observations and comparisons directly. Check interpretations, causal claims, generalization, and SOTA claims against their respective supporting evidence. Discuss limitations proportionately and primarily in the Discussion.

Checking a reference's identity is separate from checking whether its source content supports a specific claim. Abstract-level support must not be presented as full-text reading. Whether supplied by the author or suggested by the system, `min_citations` is **advisory only**: it is not a completion gate, and references are not padded to reach a quota.

### Acceptance Checks Are Not Simulated Peer Review

Acceptance checks cover prose quality, empty or generic paragraphs, broken reasoning, data–narrative contradictions, protocol descriptions, consistency between interpretations and literature, citation errors, and figure–text discrepancies. Protocol closure means clear, traceable reporting—not judging whether the methodology is optimal. The checker does not simulate reviewers or assess novelty or publication probability.

| Status | Meaning |
|--------|---------|
| `passed` | No unresolved repair issues within the declared scope; suggestions may remain |
| `needs_revision` | Specific issues the lead writer can repair |
| `needs_author_input` | Author materials, confirmation, or authorization are needed; unrelated work continues |

Every issue must include a location, supporting grounds, and a resolution condition. After a repair, recheck the affected scope rather than repeatedly reviewing the entire manuscript. If the same issue makes no substantive progress for two consecutive rounds, retain its actual status and ask the author to decide.

Delivery level is recorded separately: `usable_draft` (substantive content draft), `partial_draft` (existing prose plus local outlines), or `structured_outline` (primarily an outline and material requests). Accepting delivery with gaps does not mean the manuscript has passed acceptance checks or is ready for submission.

## Orchestrator Workflow

1. **Inventory and consolidated confirmation:** Reuse information already provided. Progress automatically by default, with optional section-by-section confirmation and mid-task switching. Proactively recommend a literature library.
2. **Initial evidence gathering and storyline confirmation:** Investigate in parallel and merge sources. Ask the author to confirm the central claims and argument before drafting.
3. **Lead-writer drafting and section checks:** Write supported prose and use concrete outlines and material requests where evidence is missing. Repair identified issues and investigate specific gaps while independent work continues.
4. **Manuscript integration and acceptance checks:** Check cross-section claims, numbers, terminology, citation support, and figure–text consistency. Write the Abstract and Conclusion after the body, based on its actual content.
5. **Deliver or gather more evidence:** Before delivery, consolidate major gaps and the delivery level. The author chooses whether to continue or accept the current draft; costly evidence gathering and new experiments require separate decisions.

The default output root is `./academic-paper-writer/paper-drafts/`; the author may choose another directory. Main files are `paper_draft.md`, `section_blueprint.md`, and `evidence_inventory.yaml`. Continuing multi-section tasks use `task_state.yaml` to record the storyline, section states, issues, and next action. On resumption, check actual file versions rather than trusting a stored PASS.

The default deliverable is a **content draft**, not LaTeX/Word formatting, a compiled PDF, or a submission package. The author supplies architecture diagrams; necessary data figures are generated within the authorized scope.

## Usage Examples

### Start a Full-Paper Draft Once

```text
Materials are in ./research: method notes, existing CSV results, and local literature.
The idea is to model dynamic relationships to address cross-session variation.
Write in English; the target venue is undecided.
Confirm the storyline, then proceed automatically and deliver a usable content draft.
For missing material, provide concrete outlines and suggestions for what to supply.
Do not run new experiments or typeset the paper by default.
```

### Optional Section-by-Section Progression

```text
Let me confirm each section after it is written this time.
I may switch back to automatic progression later.
```

### Standalone Local Tasks

```text
/academic-polishing Rewrite this Method paragraph, preserving the given facts without adding motivations or results.
/academic-citation Verify this reference's identity and whether it supports the current comparison sentence.
/academic-experiments Read-only: check metric definitions and reporting conventions across the CSV, logs, and results paragraph. Do not run code.
/academic-reviser Check this section and report concrete issues and resolution conditions. Do not rewrite the prose.
```

Notes or ideas alone can support an outline and whatever prose is justified; they cannot justify invented, complete Results. For typesetting only, call academic-latex-layout directly.

## Documentation Layers

| Layer | Files | Purpose |
|-------|-------|---------|
| Skill entry points | Each `SKILL.md` and `manifest.yaml` | Responsibilities, routing, and on-demand loading |
| Shared rules | `skills/shared/core/` | Evidence policy, non-invention, and read/write ownership |
| Shared contracts | `skills/shared/schemas/` | Evidence, reference identity/support, reading, and acceptance |
| Workflow | Writer's `references/orchestration-workflow.md` and three `workflow-step-*.md` files | Preparation, drafting, acceptance, delivery, and resumption |
| Specialized guidance | Each skill's `references/` | On-demand rules for argumentation, figures, retrieval, protocols, and more |

Project helper scripts live in `scripts/` and each relevant skill's `scripts/` directory. Public synthetic regression tests are in `tests/public/`. Private manuscripts, results, and research material are not published.

## Safety Boundaries

- **No fabrication or conflation:** Results, references, source-code locations, and verification states require grounds. Treat author facts, intent, and hypotheses separately.
- **Scoped execution:** Evidence gathering and retrieval are read-only by default. Recalculation and statistics require bounded authorization; new experiments, retraining, and protocol changes require separate approval.
- **Bounded acceptance checks:** Do not turn manuscript usability checks into methodology or novelty review, or block progress over vague stylistic preferences.
- **Transparent gaps:** Specify what is missing, which content it affects, and what the author should provide. Do not label an outline as a complete, nearly submission-ready manuscript.
- **No unauthorized disclosure:** Sensitive PDF uploads and material handling must follow the author's authorization. Never write tokens into deliverables.

## Maintenance and Verification

```bash
python -B scripts/check_schemas.py --skills-root skills
python -B -m unittest discover -s tests/public -v
```

Contract checks validate only static consistency of paths, declarations, and enums. They do not establish reference authenticity, scientific correctness, or reliable agent behavior. Public tests cover citation-structure counterexamples, CLI states, and checker counterexamples. The project does not build speed or quality rankings against previous versions or competing systems.

`citation_audit.py` checks only numeric citation structure: grouped/range markers, missing, orphaned, and duplicate entries, and explicit unverified markers. Even exit code 0 explicitly reports reference identity and source support as **NOT CHECKED**. Author–year citations are reported as not checked and require separate comparison. Manual/real-agent scenarios are documented in `skills/academic-paper-writer/references/test-scenarios.md`; unexecuted scenarios must not be reported as passed.

`main` is the development branch. To pin a version, use an existing tag or the maintained stable branch. Claims that a feature has passed real-task acceptance checks must be backed by the corresponding test evidence.

## Reference Projects

- [PaperSpine](https://github.com/WUBING2023/PaperSpine) (MIT): evidence records and same-task resumption ideas.
- [nature-skills](https://github.com/Yuan1z0825/nature-skills) (Apache-2.0): manuscript discipline and on-demand loading ideas.
- [superpowers](https://github.com/obra/superpowers)
- [academic-research-skills](https://github.com/Imbad0202/academic-research-skills)

This iteration draws on workflow ideas without copying external code. Future direct reuse must retain attribution and the applicable license.

[Agent Skills Specification](https://agentskills.io) · [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code/plugins) · [Codex CLI](https://github.com/openai/codex)

## License

[MIT License](LICENSE). The author remains responsible for the final paper's academic integrity, research authenticity, citation accuracy, and submission compliance.
