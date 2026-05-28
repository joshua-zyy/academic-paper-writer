#!/usr/bin/env python3
"""
Citation Audit — scan a Markdown draft for citation integrity issues.

Usage:
    python citation_audit.py --input paper_draft.md

Checks:
1. Every [REF_NEEDED: ...] placeholder is tracked
2. Inline citations [N] have matching reference list entries
3. Reference list entries have corresponding inline citations
4. UNVERIFIED references are flagged
"""

import argparse
import re
import sys
from pathlib import Path


def parse_references(text: str) -> dict:
    """Extract reference list entries: [N] Title/Authors/..."""
    refs = {}
    pattern = re.compile(r'^\[(\d+)\]\s+(.+)', re.MULTILINE)
    for m in pattern.finditer(text):
        ref_id = m.group(1)
        content = m.group(2).strip()
        status = "UNVERIFIED" if "UNVERIFIED" in content.upper() else "VERIFIED"
        refs[ref_id] = {"content": content[:80], "status": status}
    return refs


def parse_inline_citations(text: str) -> list:
    """Find all inline citation markers [N] in body text (before References section)."""
    parts = text.split("## References")
    if len(parts) < 2:
        parts = text.split("## 参考文献")
    body = parts[0] if parts else text
    return re.findall(r'\[(\d+)\]', body)


def parse_ref_needed(text: str) -> list:
    """Find all [REF_NEEDED: ...] placeholders."""
    return re.findall(r'\[REF_NEEDED:\s*([^\]]+)\]', text)


def audit(text: str) -> dict:
    refs = parse_references(text)
    inline = parse_inline_citations(text)
    ref_needed = parse_ref_needed(text)

    inline_set = set(inline)
    ref_ids = set(refs.keys())

    orphan_refs = ref_ids - inline_set
    missing_refs = inline_set - ref_ids
    unverified = {k: v for k, v in refs.items() if v["status"] == "UNVERIFIED"}

    return {
        "total_refs": len(refs),
        "total_inline": len(inline_set),
        "orphan_refs": sorted(orphan_refs),
        "missing_refs": sorted(missing_refs),
        "unverified_refs": unverified,
        "ref_needed_count": len(ref_needed),
        "ref_needed_topics": ref_needed,
    }


def print_report(report: dict):
    print("Citation Audit Report")
    print("=" * 40)
    print(f"References in list: {report['total_refs']}")
    print(f"Unique inline citations: {report['total_inline']}")
    print(f"[REF_NEEDED] placeholders: {report['ref_needed_count']}")
    print()

    if report["orphan_refs"]:
        print(f"[WARN] Orphan references (in list but not cited inline): {report['orphan_refs']}")
    if report["missing_refs"]:
        print(f"[FAIL] Missing references (cited inline but not in list): {report['missing_refs']}")
    if report["unverified_refs"]:
        print(f"[WARN] UNVERIFIED references: {list(report['unverified_refs'].keys())}")
    if report["ref_needed_topics"]:
        print(f"[INFO] Open [REF_NEEDED] topics:")
        for t in report["ref_needed_topics"]:
            print(f"  - {t}")

    verdict = "pass" if not report["missing_refs"] else "fail"
    print(f"\nVerdict: {verdict.upper()}")
    return verdict


def main():
    parser = argparse.ArgumentParser(description="Audit citation integrity in a paper draft.")
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
