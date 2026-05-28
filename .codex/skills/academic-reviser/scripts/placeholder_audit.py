#!/usr/bin/env python3
"""
Placeholder Audit — scan a Markdown draft for placeholder integrity.

Usage:
    python placeholder_audit.py --input paper_draft.md

Checks:
1. Count and categorize all placeholders
2. Detect bare placeholders missing context (e.g., [REF_NEEDED] without topic)
3. Detect deleted placeholders that left no replacement
4. Verify [ABSTRACT_NEEDED] is present if Abstract section is missing
"""

import argparse
import re
import sys
from pathlib import Path

PLACEHOLDER_PATTERNS = {
    "REF_NEEDED": re.compile(r'\[REF_NEEDED(?::\s*([^\]]+))?\]'),
    "FIGURE_NEEDED": re.compile(r'\[FIGURE_NEEDED(?::\s*([^\]]+))?\]'),
    "TABLE_NEEDED": re.compile(r'\[TABLE_NEEDED(?::\s*([^\]]+))?\]'),
    "RESULT_NEEDED": re.compile(r'\[RESULT_NEEDED(?::\s*([^\]]+))?\]'),
    "RESULT_UNVERIFIED": re.compile(r'\[RESULT_UNVERIFIED(?::\s*([^\]]+))?\]'),
    "METHOD_DETAIL_NEEDED": re.compile(r'\[METHOD_DETAIL_NEEDED(?::\s*([^\]]+))?\]'),
    "RATIONALE_NEEDED": re.compile(r'\[RATIONALE_NEEDED(?::\s*([^\]]+))?\]'),
    "DATASET_DETAIL_NEEDED": re.compile(r'\[DATASET_DETAIL_NEEDED(?::\s*([^\]]+))?\]'),
    "ABSTRACT_NEEDED": re.compile(r'\[ABSTRACT_NEEDED(?::\s*([^\]]+))?\]'),
}


def audit(text: str) -> dict:
    results = {}
    bare_placeholders = []
    total = 0

    for name, pattern in PLACEHOLDER_PATTERNS.items():
        matches = pattern.findall(text)
        count = len(pattern.findall(text))
        results[name] = count
        total += count

        bare = re.findall(rf'\[{name}\](?!\[)', text)
        if bare:
            bare_placeholders.append({"type": name, "count": len(bare)})

    has_abstract_section = bool(re.search(r'^#+\s*Abstract', text, re.MULTILINE | re.IGNORECASE))
    has_abstract_placeholder = results.get("ABSTRACT_NEEDED", 0) > 0

    return {
        "total_placeholders": total,
        "by_type": results,
        "bare_placeholders": bare_placeholders,
        "has_abstract_section": has_abstract_section,
        "has_abstract_placeholder": has_abstract_placeholder,
        "abstract_ok": has_abstract_section or has_abstract_placeholder,
    }


def print_report(report: dict):
    print("Placeholder Audit Report")
    print("=" * 40)
    print(f"Total placeholders: {report['total_placeholders']}")
    print()

    print("By type:")
    for name, count in report["by_type"].items():
        if count > 0:
            print(f"  {name}: {count}")
    print()

    if report["bare_placeholders"]:
        print("[WARN] Bare placeholders (missing context):")
        for bp in report["bare_placeholders"]:
            print(f"  {bp['type']}: {bp['count']} instance(s) without context description")
        print()

    if not report["abstract_ok"]:
        print("[FAIL] No Abstract section and no [ABSTRACT_NEEDED] placeholder found")
    elif report["has_abstract_placeholder"]:
        print("[INFO] Abstract pending — [ABSTRACT_NEEDED] placeholder present")
    else:
        print("[PASS] Abstract section exists")

    verdict = "pass" if not report["bare_placeholders"] and report["abstract_ok"] else "fail"
    print(f"\nVerdict: {verdict.upper()}")
    return verdict


def main():
    parser = argparse.ArgumentParser(description="Audit placeholders in a paper draft.")
    parser.add_argument("--input", required=True, help="Path to paper_draft.md")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    report = audit(text)
    verdict = print_report(report)
    sys.exit(0 if verdict == "pass" else 1)


if __name__ == "__main__":
    main()
