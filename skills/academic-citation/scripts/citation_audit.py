#!/usr/bin/env python3
"""Check Markdown numeric citation structure, NOT identity or claim support.

Exit 0: structure passes, identity/support still not checked.
Exit 1: malformed/missing/orphan/duplicate entries or unresolved REF_NEEDED.
Exit 2: explicit unverified entries or unsupported author-year format.
"""
import argparse
import re
from pathlib import Path

HEADING = re.compile(r'^##[ \t]+(?:References|参考文献)[ \t]*$', re.M | re.I)
ENTRY = re.compile(r'^\[(\d+)\][ \t]+(.+)$', re.M)
MARKER = re.compile(r'\[(\d+(?:\s*[-–—]\s*\d+)?(?:\s*[,，]\s*\d+(?:\s*[-–—]\s*\d+)?)*)\]')


def _without_code(text: str) -> str:
    text = re.sub(r'```[^\n]*\n.*?```|~~~[^\n]*\n.*?~~~', '', text, flags=re.S)
    return re.sub(r'`[^`\n]*`', '', text)


def _sections(text: str) -> tuple:
    text = _without_code(text)
    heading = HEADING.search(text)
    if not heading:
        return text, ''
    tail = text[heading.end():]
    end = re.search(r'^#{1,2}[ \t]+', tail, flags=re.M)
    return text[:heading.start()], tail[:end.start()] if end else tail


def parse_references(text: str) -> dict:
    """Absence of UNVERIFIED is UNKNOWN, never proof of verification."""
    refs = {}
    for match in ENTRY.finditer(_sections(text)[1]):
        ref_id = str(int(match.group(1)))
        content = match.group(2).strip()
        status = 'UNVERIFIED' if re.search(r'\bUNVERIFIED\b', content, re.I) else 'UNKNOWN'
        refs[ref_id] = {'content': content, 'status': status}
    return refs


def parse_inline_citations(text: str) -> list:
    citations = []
    for match in MARKER.finditer(_sections(text)[0]):
        for part in re.split(r'[,，]', match.group(1)):
            limits = re.split(r'[-–—]', part)
            start = int(limits[0])
            stop = int(limits[-1])
            # Invalid or implausibly large ranges are reported by audit().
            if 0 < start <= stop and stop - start <= 1000:
                citations.extend(str(n) for n in range(start, stop + 1))
    return citations


def parse_ref_needed(text: str) -> list:
    return [topic or 'unspecified' for topic in re.findall(
        r'\[REF_NEEDED(?::\s*([^\]]*))?\]', _without_code(text)
    )]


def audit(text: str, citation_style: str = 'numeric') -> dict:
    refs = parse_references(text)
    body, ref_text = _sections(text)
    inline = set(parse_inline_citations(text))
    ids = set(refs)
    seen = set()
    duplicates = set()
    for match in ENTRY.finditer(ref_text):
        ref_id = str(int(match.group(1)))
        if ref_id in seen:
            duplicates.add(ref_id)
        seen.add(ref_id)
    invalid = [match.group(0) for match in re.finditer(r'\[[\d\s,，\-–—]+\]', body)
               if not MARKER.fullmatch(match.group(0))]
    for match in MARKER.finditer(body):
        for part in re.split(r'[,，]', match.group(1)):
            limits = re.split(r'[-–—]', part)
            start, stop = int(limits[0]), int(limits[-1])
            if start <= 0 or stop < start or stop - start > 1000:
                invalid.append(match.group(0))
    if '0' in ids:
        invalid.append('reference [0]')
    needed = parse_ref_needed(text)
    unverified = {k: v for k, v in refs.items() if v['status'] == 'UNVERIFIED'}
    errors = bool(inline - ids or ids - inline or duplicates or invalid or needed)
    section_count = len(HEADING.findall(_without_code(text)))
    if section_count != 1:
        errors = True
    structural = 'not_checked' if citation_style == 'author-year' else ('fail' if errors else 'pass')
    return {
        'total_refs': len(refs), 'total_inline': len(inline),
        'orphan_refs': sorted(ids - inline, key=int),
        'missing_refs': sorted(inline - ids, key=int),
        'duplicate_refs': sorted(duplicates, key=int), 'invalid_markers': invalid,
        'unverified_refs': unverified, 'ref_needed_count': len(needed),
        'ref_needed_topics': needed, 'references_section_count': section_count,
        'structural_verdict': structural,
        'identity_verdict': 'not_checked', 'support_verdict': 'not_checked',
    }


def print_report(report: dict) -> str:
    print('Citation STRUCTURE Audit — not identity or claim-support verification')
    for key, value in report.items():
        print(f'{key}: {value}')
    if report['structural_verdict'] == 'not_checked':
        verdict = 'needs_verification'
    elif report['structural_verdict'] == 'fail':
        verdict = 'fail'
    elif report['unverified_refs']:
        verdict = 'needs_verification'
    else:
        verdict = 'structure_pass'
    print(f'Verdict: {verdict}; identity/support: NOT CHECKED')
    return verdict


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--citation-style', choices=('numeric', 'author-year'), default='numeric')
    args = parser.parse_args()
    try:
        text = Path(args.input).read_text(encoding='utf-8-sig')
    except OSError as exc:
        parser.error(str(exc))
    verdict = print_report(audit(text, args.citation_style))
    return {'structure_pass': 0, 'fail': 1, 'needs_verification': 2}[verdict]


if __name__ == '__main__':
    raise SystemExit(main())
