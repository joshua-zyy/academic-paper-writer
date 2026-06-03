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
    required_modes = ["arch-prompt", "chart-from-data", "architecture-svg"]

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


def _repo_root_from_skills(skills_root: Path) -> Path:
    return skills_root.resolve().parent


def _extract_frontmatter(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return {}
    end = content.find("\n---", 4)
    if end == -1:
        return {}
    fields = {}
    for line in content[4:end].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def _manifest_paths_from_text(text: str) -> list:
    paths = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("-"):
            value = stripped[1:].strip()
            if value.endswith(".md") or value.endswith(".py") or value.endswith(".yaml"):
                paths.append(value)
            continue
        if ":" in stripped:
            _, value = stripped.split(":", 1)
            value = value.strip().strip('"').strip("'")
            if value.endswith(".md") or value.endswith(".py") or value.endswith(".yaml"):
                paths.append(value)
    return paths


def check_manifest_links(skills_root: Path) -> list:
    issues = []
    manifests = sorted(skills_root.glob("*/manifest.yaml"))
    if not manifests:
        return [("WARN", "No skill manifests found")]

    for manifest in manifests:
        base = manifest.parent
        for rel in _manifest_paths_from_text(manifest.read_text(encoding="utf-8")):
            target = base / rel
            if not target.exists():
                issues.append(("FAIL", f"{manifest.relative_to(skills_root)} references missing file: {rel}"))
    if not issues:
        issues.append(("PASS", f"All {len(manifests)} skill manifest file references exist"))
    return issues


def check_skill_frontmatter(skills_root: Path) -> list:
    issues = []
    for skill_md in sorted(skills_root.glob("*/SKILL.md")):
        fields = _extract_frontmatter(skill_md)
        keys = set(fields)
        if keys != {"name", "description"}:
            issues.append(("FAIL", f"{skill_md.relative_to(skills_root)} frontmatter keys must be exactly name+description, got {sorted(keys)}"))
    if not issues:
        issues.append(("PASS", "All SKILL.md frontmatter blocks contain only name and description"))
    return issues


def check_package_noise(skills_root: Path) -> list:
    repo_root = _repo_root_from_skills(skills_root)
    roots = [skills_root, repo_root / ".codex" / "skills"]
    noisy = []
    for root in roots:
        if not root.exists():
            continue
        noisy.extend(p.resolve() for p in root.rglob("*.pyc"))
        noisy.extend(p.resolve() for p in root.rglob("__pycache__") if p.is_dir())
    if noisy:
        return [("FAIL", "Package noise found: " + ", ".join(str(p.relative_to(repo_root)) for p in noisy))]
    return [("PASS", "No .pyc or __pycache__ files under skills/ or .codex/skills/")]


def check_python_only_figure_policy(skills_root: Path) -> list:
    figure_root = skills_root / "academic-figure"
    if not figure_root.exists():
        return [("WARN", "academic-figure skill not found")]
    forbidden = ["ggplot2", "patchwork", "ComplexHeatmap", "Rscript", "Python or R"]
    hits = []
    for path in figure_root.rglob("*.md"):
        content = path.read_text(encoding="utf-8", errors="ignore")
        for token in forbidden:
            if token in content:
                hits.append(f"{path.relative_to(skills_root)}:{token}")
    for path in figure_root.rglob("*.yaml"):
        content = path.read_text(encoding="utf-8", errors="ignore")
        for token in forbidden:
            if token in content:
                hits.append(f"{path.relative_to(skills_root)}:{token}")
    if hits:
        return [("FAIL", "academic-figure contains non-Python backend language: " + ", ".join(hits))]
    return [("PASS", "academic-figure contains no non-Python backend language")]


def check_codex_mirror_drift(skills_root: Path) -> list:
    repo_root = _repo_root_from_skills(skills_root)
    codex_root = repo_root / ".codex" / "skills"
    if not codex_root.exists():
        return [("WARN", ".codex/skills directory not found")]
    drift = []
    missing = []
    extra = []
    for source in sorted(skills_root.rglob("*")):
        if not source.is_file():
            continue
        rel = source.relative_to(skills_root)
        mirror = codex_root / rel
        if not mirror.exists():
            missing.append(str(rel))
        elif source.read_text(encoding="utf-8").replace("\r\n", "\n") != mirror.read_text(encoding="utf-8").replace("\r\n", "\n"):
            drift.append(str(rel))
    for mirror in sorted(codex_root.rglob("*")):
        if not mirror.is_file():
            continue
        rel = mirror.relative_to(codex_root)
        source = skills_root / rel
        if not source.exists():
            extra.append(str(rel))
    issues = []
    if missing:
        issues.append(("FAIL", ".codex/skills missing files: " + ", ".join(missing)))
    if extra:
        issues.append(("FAIL", ".codex/skills has extra files not in skills/: " + ", ".join(extra)))
    if drift:
        issues.append(("FAIL", ".codex/skills content drift: " + ", ".join(drift)))
    if not issues:
        issues.append(("PASS", ".codex/skills mirrors matching files under skills/"))
    return issues


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

    unused = defined_types - referenced_types
    undefined = referenced_types - defined_types
    if undefined:
        issues.append(("FAIL", f"Probe types referenced in workflow but not defined in probe-agent.md: {undefined}"))
    elif unused:
        issues.append(("PASS", f"All {len(referenced_types)} referenced probe types defined; {len(unused)} defined types unused: {sorted(unused)}"))
    else:
        issues.append(("PASS", f"All {len(defined_types)} probe types defined and referenced"))

    return issues


def check_figure_agent_mode_names(skills_root: Path) -> list:
    paths = [
        skills_root / "academic-figure" / "agents" / "figure_agent.md",
        skills_root / "academic-figure" / "references" / "workflow-chart-from-data.md",
        skills_root / "academic-figure" / "references" / "workflow-arch-prompt.md",
        skills_root / "academic-figure" / "references" / "workflow-architecture-svg.md",
    ]
    stale_patterns = [
        r'A\s*路径', r'B\s*路径', r'C\s*路径',
        r'path_A', r'path_B', r'path_C',
        r'"A"\s*\|\s*"B"\s*\|\s*"C"',
        r'路径 A', r'路径 B', r'路径 C',
    ]
    hits = []
    for path in paths:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        for pattern in stale_patterns:
            for m in re.finditer(pattern, content):
                line = content[:m.start()].count('\n') + 1
                hits.append(f"{path.relative_to(skills_root)}:{line}: {m.group(0)}")
    if hits:
        return [("FAIL", "Stale A/B/C path labels in figure agent/workflows: " + ", ".join(hits))]
    return [("PASS", "Figure agent and workflow references use mode names, not legacy path labels")]


def check_debt_schema_completeness(skills_root: Path) -> list:
    shared = skills_root / "shared" / "schemas" / "verification-report.md"
    reviser_vs = skills_root / "academic-reviser" / "references" / "verification-status.md"
    if not shared.exists() or not reviser_vs.exists():
        return [("WARN", "Cannot check debt completeness — missing shared schema or reviser verification-status")]

    schema_content = shared.read_text(encoding="utf-8")
    versus_content = reviser_vs.read_text(encoding="utf-8")

    schema_debts = set(re.findall(r'(\w+_debt)', schema_content))
    versus_debts = set(re.findall(r'\| (\w+_debt)', versus_content))

    missing_in_schema = versus_debts - schema_debts
    missing_in_versus = schema_debts - versus_debts

    issues = []
    if missing_in_schema:
        issues.append(("FAIL", f"Debt types in reviser verification-status but missing from shared schema: {missing_in_schema}"))
    if missing_in_versus:
        issues.append(("WARN", f"Debt types in shared schema but missing from reviser verification-status table: {missing_in_versus}"))
    if not issues:
        issues.append(("PASS", f"All {len(schema_debts)} shared schema debt types are present in reviser verification-status table"))
    return issues


def check_agent_input_schema_debts(skills_root: Path) -> list:
    shared = skills_root / "shared" / "schemas" / "verification-report.md"
    agent = skills_root / "academic-reviser" / "agents" / "reviser_agent.md"
    if not shared.exists() or not agent.exists():
        return [("WARN", "Cannot check agent schema — missing files")]

    schema_debts = set(re.findall(r'(\w+_debt)', shared.read_text(encoding="utf-8")))
    agent_debts = set(re.findall(r'(\w+_debt)', agent.read_text(encoding="utf-8")))

    missing = schema_debts - agent_debts
    if missing:
        return [("FAIL", f"Reviser agent input schema missing debt fields from shared schema: {missing}")]
    return [("PASS", f"Reviser agent input schema covers all {len(schema_debts)} debt fields")]


def check_verification_output_template(skills_root: Path) -> list:
    shared = skills_root / "shared" / "schemas" / "verification-report.md"
    vs = skills_root / "academic-reviser" / "references" / "verification-status.md"
    if not shared.exists() or not vs.exists():
        return [("WARN", "Cannot check output template — missing files")]

    schema_debts = set(re.findall(r'(\w+_debt)', shared.read_text(encoding="utf-8")))
    vs_content = vs.read_text(encoding="utf-8")

    block_start = vs_content.find("## Verification Status")
    block_end = vs_content.find("```", vs_content.find("```", block_start) + 3) if block_start >= 0 else -1
    template_text = vs_content[block_start:block_end] if block_start >= 0 and block_end > block_start else vs_content

    template_debts = set(re.findall(r'-\s+(\w+_debt):', template_text))
    missing = schema_debts - template_debts
    if missing:
        return [("FAIL", f"Verification Status output template missing debt fields: {missing}")]
    return [("PASS", f"Verification Status output template covers all {len(schema_debts)} debt fields")]


def check_citation_hardcoded_threshold(skills_root: Path) -> list:
    path = skills_root / "academic-citation" / "SKILL.md"
    if not path.exists():
        return [("WARN", "academic-citation SKILL.md not found")]
    content = path.read_text(encoding="utf-8")
    patterns = ["至少 35 篇", "应达到 35 篇", "< 35 篇", "未达到 35 篇"]
    found = [p for p in patterns if p in content]
    if found:
        return [("FAIL", f"academic-citation SKILL.md has hardcoded citation threshold: {found}")]
    return [("PASS", "academic-citation SKILL.md uses configurable min_citations")]


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

    print("\n10. Figure agent mode names (no legacy path labels):")
    issues = check_figure_agent_mode_names(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n11. Debt schema completeness (shared vs reviser):")
    issues = check_debt_schema_completeness(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n12. Agent input schema debt coverage:")
    issues = check_agent_input_schema_debts(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n13. Verification output template debt coverage:")
    issues = check_verification_output_template(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n14. Citation threshold (configurable vs hardcoded):")
    issues = check_citation_hardcoded_threshold(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n15. Manifest file references:")
    issues = check_manifest_links(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n16. SKILL.md frontmatter:")
    issues = check_skill_frontmatter(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n17. Package hygiene:")
    issues = check_package_noise(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n18. Python-only figure policy:")
    issues = check_python_only_figure_policy(root)
    all_issues.extend(issues)
    for level, msg in issues:
        print(f"  [{level}] {msg}")

    print("\n19. .codex mirror drift:")
    issues = check_codex_mirror_drift(root)
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
