# Output Boundaries

This file defines file-write and role boundaries for the skill suite.

## Orchestrator Ownership

The `academic-paper-writer` orchestrator owns final writes under `./docs/paper-drafts/` during full paper generation.

## Sub-Skill Ownership

Sub-skills return structured content, reports, scripts, prompts, or suggested output paths. They must not modify unrelated project source code, configuration, experiment data, or existing artifacts.

## Independent Use

When a sub-skill is invoked independently and the user explicitly asks for file output, it may create new output files in user-approved paths. It must not overwrite existing data without explicit permission.
