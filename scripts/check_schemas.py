#!/usr/bin/env python3
"""
Schema Consistency Checker — validate cross-skill schema alignment.

Usage:
    python check_schemas.py --skills-root /path/to/skills

Checks:
1. Each sub-skill's references/schemas/ has a corresponding shared/schemas/ copy
2. SKILL.md debt fields match verification-report schema debt fields
3. Probe types referenced in orchestration workflow exist in probe-agent.md
4. Reference files mentioned in SKILL.md "何时读取" tables exist
5. Figure dispatch templates use academic-figure mode names, not stale path labels
"""

import argparse
import re
import sys
from pathlib import Path


def check_schema_sync(skills_root: Path) -> list:
    issues = []
    shared_schemas = skills_root / "shared" / "schemas"
    if not shared_schemas.exists():
        issues.append(("FAIL", "shared/schemas/ directory not found"))
        return issues

    shared_files = {f.name for f in shared_schemas.glob("*.md")}

    sub_skills = [d.name for d in skills_root.iterdir()
                  if d.is_dir() and d.name != "shared"
                  and (d / "references" / "schemas").exists()]
    for skill in sub_skills:
        schema_dir = skills_root / skill / "references" / "schemas"
        for sf in schema_dir.glob("*.md"):
            if sf.name not in shared_files:
                issues.append(("FAIL", f"{skill}/references/schemas/{sf.name} has no shared/ copy"))
            else:
                content = sf.read_text(encoding="utf-8")
                expected_ref = f"skills/shared/schemas/{sf.name}"
                if expected_ref in content:
                    issues.append(("PASS", f"{skill}/references/schemas/{sf.name} correctly points to shared/"))
                else:
                    issues.append(("FAIL", f"{skill}/references/schemas/{sf.name} is not a pointer to {expected_ref}"))

    return issues


def check_debt_fields(skills_root: Path) -> list:
    issues = []
    reviser_skill = skills_root / "academic-reviser" / "SKILL.md"
    shared_schema = skills_root / "shared" / "schemas" / "verification-report.md"

    if not reviser_skill.exists() or not shared_schema.exists():
        issues.append(("FAIL", "Missing reviser SKILL.md or shared verification-report schema"))
        return issues

    schema_content = shared_schema.read_text(encoding="utf-8")
    schema_debts = set(re.findall(r'(\w+_debt)', schema_content))

    skill_content = reviser_skill.read_text(encoding="utf-8")
    skill_debts = set(re.findall(r'(\w+_debt)', skill_content))

    missing_in_skill = schema_debts - skill_debts
    missing_in_schema = skill_debts - schema_debts

    if missing_in_skill:
        issues.append(("FAIL", f"Debt fields in schema but missing from reviser SKILL.md: {missing_in_skill}"))
    if missing_in_schema:
        issues.append(("WARN", f"Debt fields in reviser SKILL.md but missing from schema: {missing_in_schema}"))
    if not missing_in_skill and not missing_in_schema:
        issues.append(("PASS", f"Debt fields aligned: {schema_debts}"))

    return issues


def check_reference_files_exist(skills_root: Path) -> list:
    issues = []
    for skill_dir in skills_root.iterdir():
        if not skill_dir.is_dir() or skill_dir.name == "shared":
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding="utf-8")
        # Only match relative references/ paths, not cross-skill paths
        refs = re.findall(r'(?<![a-z-]/)references/([^\s\|`]+\.md)', content)
        for ref in refs:
            ref_path = skill_dir / "references" / ref
            if not ref_path.exists():
                issues.append(("FAIL", f"{skill_dir.name}/references/{ref} referenced but not found"))

    return issues


def check_figure_dispatch_modes(skills_root: Path) -> list:
    issues = []
    stale_paths = []
    required_modes = ["arch-prompt", "chart-from-data", "architecture-image"]

    orchestrator_refs = skills_root / "academic-paper-writer" / "references"
    if orchestrator_refs.exists():
        content = "\n".join(p.read_text(encoding="utf-8") for p in orchestrator_refs.rglob("*.md"))
        stale_paths.extend(re.findall(r'\bpath:\s*[ABC]\b|路径\s*[ABC]|[ABC]\s*路径', content))

    if stale_paths:
        issues.append(("FAIL", f"Stale academic-figure path labels found: {sorted(set(stale_paths))}"))

    all_content = ""
    for skill_name in ["academic-paper-writer", "academic-figure"]:
        references_dir = skills_root / skill_name / "references"
        if references_dir.exists():
            all_content += "\n".join(p.read_text(encoding="utf-8") for p in references_dir.rglob("*.md"))

    missing_modes = [mode for mode in required_modes if mode not in all_content]
    if missing_modes:
        issues.append(("FAIL", f"Missing academic-figure mode names in dispatch templates: {missing_modes}"))

    if not stale_paths and not missing_modes:
        issues.append(("PASS", "Figure dispatch templates use correct mode names"))
    return issues


def _read_if_exists(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def check_min_citations_usage(skills_root: Path) -> list:
    workflow = skills_root / "academic-paper-writer" / "references" / "workflow-step-6.6-9.md"
    content = _read_if_exists(workflow)
    hardcoded_patterns = ["< 35 篇", "未达到 35 篇", ">= 35", "至少 35"]
    found = [pattern for pattern in hardcoded_patterns if pattern in content]
    if found:
        return [("FAIL", f"hardcoded citation threshold found in workflow-step-6.6-9.md: {found}")]
    return [("PASS", "Citation threshold uses min_citations instead of hardcoded 35")]


def check_figure_debt_flow(skills_root: Path) -> list:
    paths = [
        skills_root / "shared" / "schemas" / "verification-report.md",
        skills_root / "academic-reviser" / "SKILL.md",
        skills_root / "academic-paper-writer" / "references" / "workflow-step-6.6-9.md",
    ]
    content = "\n".join(_read_if_exists(path) for path in paths)
    deadlock_patterns = [
        "figure_debt = open 时 verdict 不得为 `passed`",
        "figure_debt = open 时 verdict 不得为 passed",
        "figure_debt 未闭合时判为 passed",
    ]
    found = [pattern for pattern in deadlock_patterns if pattern in content]
    if found:
        return [("FAIL", f"figure_debt deadlock language found: {found}")]
    return [("PASS", "figure_debt is treated as soft section debt and final delivery gate")]


def check_subagent_file_write_ownership(skills_root: Path) -> list:
    workflow = skills_root / "academic-paper-writer" / "references" / "workflow-step-0-4.md"
    content = _read_if_exists(workflow)
    conflict = "你已加载 academic-venue-research" in content and "生成 venue-brief.md 文件" in content
    if conflict:
        return [("FAIL", "subagent write ownership conflict: venue research dispatch asks subagent to generate venue-brief.md directly")]
    return [("PASS", "Subagent dispatch templates return structured content for orchestrator-owned writes")]


def check_prose_gate_evidence_debt(skills_root: Path) -> list:
    workflow = skills_root / "academic-paper-writer" / "references" / "workflow-step-6.6-9.md"
    content = _read_if_exists(workflow)
    blocking_phrases = [
        "Confirm Step 6.5 `evidence_debt = closed` before executing",
        "确认 Step 6.5 `evidence_debt = closed` before executing",
    ]
    found = [phrase for phrase in blocking_phrases if phrase in content]
    if found:
        return [("FAIL", f"Step 6.6 blocks all prose repair on closed evidence debt: {found}")]
    return [("PASS", "Step 6.6 allows safe prose repair when evidence_debt is open")]


def check_probe_types(skills_root: Path) -> list:
    issues = []
    probe_agent = skills_root / "academic-paper-writer" / "agents" / "probe-agent.md"
    workflow_dir = skills_root / "academic-paper-writer" / "references"

    if not probe_agent.exists() or not workflow_dir.exists():
        issues.append(("FAIL", "Missing probe-agent.md or workflow references"))
        return issues

    probe_content = probe_agent.read_text(encoding="utf-8")
    defined_types = set(re.findall(r'####\s+(\w+)\s+—', probe_content))

    workflow_content = "\n".join(p.read_text(encoding="utf-8") for p in workflow_dir.rglob("*.md"))
    referenced_types = set(re.findall(r'probe_type:\s*(\w+)', workflow_content))

    undefined = referenced_types - defined_types
    if undefined:
        issues.append(("FAIL", f"Probe types referenced in workflow but not defined in probe-agent.md: {undefined}"))
    else:
        issues.append(("PASS", f"All {len(referenced_types)} probe types defined"))

    return issues


def main():
    parser = argparse.ArgumentParser(description="Check cross-skill schema consistency.")
    parser.add_argument("--skills-root", required=True, help="Path to skills/ directory")
    args = parser.parse_args()

    root = Path(args.skills_root)
    if not root.is_dir():
        print(f"Error: Not a directory: {root}", file=sys.stderr)
        sys.exit(1)

    all_issues = []
    print("Schema Consistency Check")
    print("=" * 50)

    print("\n1. Schema sync (shared/ vs sub-skill/):")
    issues = check_schema_sync(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n2. Debt field alignment (schema vs SKILL.md):")
    issues = check_debt_fields(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n3. Reference file existence:")
    issues = check_reference_files_exist(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n4. Figure dispatch mode consistency:")
    issues = check_figure_dispatch_modes(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n5. Citation threshold consistency:")
    issues = check_min_citations_usage(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n6. Figure debt flow consistency:")
    issues = check_figure_debt_flow(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n7. Subagent file ownership:")
    issues = check_subagent_file_write_ownership(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n8. Prose gate evidence-debt behavior:")
    issues = check_prose_gate_evidence_debt(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n9. Probe type consistency:")
    issues = check_probe_types(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    fail_count = sum(1 for level, _ in all_issues if level == "FAIL")
    warn_count = sum(1 for level, _ in all_issues if level == "WARN")
    pass_count = sum(1 for level, _ in all_issues if level == "PASS")
    print(f"\n{'=' * 50}")
    print(f"Results: {pass_count} PASS | {fail_count} FAIL | {warn_count} WARN")
    sys.exit(1 if fail_count > 0 else 0)


if __name__ == "__main__":
    main()
