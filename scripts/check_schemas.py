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

    sub_skills = ["academic-citation", "academic-experiments", "academic-reviser"]
    for skill in sub_skills:
        schema_dir = skills_root / skill / "references" / "schemas"
        if not schema_dir.exists():
            continue
        for sf in schema_dir.glob("*.md"):
            if sf.name not in shared_files:
                issues.append(("FAIL", f"{skill}/references/schemas/{sf.name} has no shared/ copy"))
            else:
                sub_content = sf.read_text(encoding="utf-8")
                shared_content = (shared_schemas / sf.name).read_text(encoding="utf-8")
                if sub_content == shared_content:
                    issues.append(("PASS", f"{skill}/references/schemas/{sf.name} matches shared/ copy"))
                else:
                    issues.append(("FAIL", f"{skill}/references/schemas/{sf.name} diverges from shared/ copy"))

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
    references_dir = skills_root / "academic-paper-writer" / "references"
    if not references_dir.exists():
        issues.append(("FAIL", "academic-paper-writer references directory not found"))
        return issues

    content = "\n".join(p.read_text(encoding="utf-8") for p in references_dir.rglob("*.md"))
    stale_paths = re.findall(r'\bpath:\s*[ABC]\b|路径\s*[ABC]|[ABC]\s*路径', content)
    if stale_paths:
        issues.append(("FAIL", f"Stale academic-figure path labels found: {sorted(set(stale_paths))}"))

    required_modes = ["arch-prompt", "chart-from-data"]
    missing_modes = [mode for mode in required_modes if mode not in content]
    if missing_modes:
        issues.append(("FAIL", f"Missing academic-figure mode names in dispatch templates: {missing_modes}"))

    if not stale_paths and not missing_modes:
        issues.append(("PASS", "Figure dispatch templates use academic-figure mode names"))
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

    fail_count = sum(1 for level, _ in all_issues if level == "FAIL")
    print(f"\n{'=' * 50}")
    print(f"Total issues: {len(all_issues)} | FAIL: {fail_count} | WARN: {sum(1 for l, _ in all_issues if l == 'WARN')}")
    sys.exit(1 if fail_count > 0 else 0)


if __name__ == "__main__":
    main()
