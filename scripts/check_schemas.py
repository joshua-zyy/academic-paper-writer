#!/usr/bin/env python3
"""Check static skill contracts and links, NOT facts or agent behavior.

Usage: python -B scripts/check_schemas.py --skills-root skills
No network access, source writes, or third-party dependencies.
"""
import argparse
import re
from pathlib import Path

SKILLS = (
    'academic-paper-writer', 'academic-citation', 'academic-experiments',
    'academic-reviser', 'academic-polishing', 'academic-figure',
    'academic-venue-research', 'academic-latex-layout',
)
SCHEMAS = (
    'evidence-inventory', 'verified-references', 'citation-to-claim-map',
    'literature-reading-report', 'verification-report',
)
SECTION_IDS = {
    'introduction', 'related_work', 'method', 'experimental_setup',
    'results', 'discussion', 'conclusion', 'abstract',
}


def _read(path: Path) -> str:
    return path.read_text(encoding='utf-8') if path.is_file() else ''


def check_links(root: Path) -> list:
    issues = []
    for name in SKILLS:
        base = root / name
        skill = base / 'SKILL.md'
        manifest = base / 'manifest.yaml'
        for path in (skill, manifest):
            if not path.is_file():
                issues.append(('FAIL', f'Missing {name}/{path.name}'))
        # Only simple top-level AgentSkills frontmatter is supported here.
        text = _read(skill)
        match = re.match(r'---\n(.*?)\n---(?:\n|$)', text, re.S)
        fields = dict(re.findall(r'^(\w+):\s*(.+)$', match[1], re.M)) if match else {}
        if (set(fields) != {'name', 'description'}
                or fields.get('name', '').strip('\"\'') != name
                or not fields.get('description', '').strip('\"\'')):
            issues.append(('FAIL', f'{name}/SKILL.md frontmatter name/description invalid'))
        # Manifest scalar file values; this is a link check, not a YAML parser.
        paths = []
        for line in _read(manifest).splitlines():
            line = line.split(' #', 1)[0].strip()
            value = line[1:].strip() if line.startswith('- ') else line.partition(':')[2].strip()
            value = value.strip('\"\'')
            if re.fullmatch(r'[^\s:]+\.(?:md|py|yaml)', value):
                paths.append(value)
        paths += re.findall(
            r'(?<![\w/-])((?:references|static|agents|scripts)/[^\s|`\"<>]+\.(?:md|py|yaml))',
            text,
        )
        for rel in sorted(set(paths)):
            target = (base / rel).resolve()
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                issues.append(('FAIL', f'{name} references missing/out-of-scope file: {rel}'))
    for name in SCHEMAS:
        path = root / 'shared/schemas' / f'{name}.md'
        if not path.is_file():
            issues.append(('FAIL', f'Missing shared/schemas/{name}.md'))
    # If a skill has a schema alias, require a pointer rather than a divergent copy.
    for path in root.glob('*/references/schemas/*.md'):
        canonical = root / 'shared/schemas' / path.name
        if not canonical.is_file() or f'skills/shared/schemas/{path.name}' not in _read(path):
            issues.append(('FAIL', f'{path.relative_to(root)} must point to shared schema'))
    return issues or [('PASS', 'All eight entries, manifests and declared links exist')]


def check_contract_enums(root: Path) -> list:
    issues = []
    declarations = (
        ('verification-report', 'verdict', {'passed', 'needs_revision', 'needs_author_input'}),
        ('verification-report', 'disposition', {'fix', 'author_input', 'suggestion'}),
        ('verification-report', 'delivery_level', {'usable_draft', 'partial_draft', 'structured_outline'}),
        ('evidence-inventory', 'type', {'newly_run', 'preexisting_artifact', 'author_provided', 'user_claim'}),
        ('evidence-inventory', 'verification_status', {'verified', 'unverified', 'conflicting', 'unavailable'}),
        ('verified-references', 'identity_status', {'VERIFIED', 'UNVERIFIED', 'CONFLICTING'}),
        ('citation-to-claim-map', 'support_status', {'supported', 'partial', 'contradicted', 'not_checked'}),
    )
    for schema, key, expected in declarations:
        text = _read(root / 'shared/schemas' / f'{schema}.md')
        match = re.search(rf'\b{key}:\s*([a-zA-Z_]+(?:\s*\|\s*[a-zA-Z_]+)+)', text)
        actual = set(re.split(r'\s*\|\s*', match[1])) if match else set()
        if actual != expected:
            issues.append(('FAIL', f'{schema} {key} enum mismatch: {sorted(actual)}'))
    manifest = _read(root / 'academic-paper-writer/manifest.yaml')
    section = re.search(r'^  section:\n(.*?)(?=^  \w+:|^references:)', manifest, re.M | re.S)
    actual = set(re.findall(r'^      (\w+):', section[1], re.M)) if section else set()
    if actual != SECTION_IDS:
        issues.append(('FAIL', f'Writer section IDs mismatch: {sorted(actual)}'))
    matrix = _read(root / 'academic-paper-writer/references/section-dependency-matrix.md')
    matrix_ids = set(re.findall(r'^\| ([a-z_]+) \|', matrix, re.M))
    if matrix_ids != SECTION_IDS:
        issues.append(('FAIL', f'Dependency matrix section IDs mismatch: {sorted(matrix_ids)}'))
    figure = _read(root / 'academic-figure/manifest.yaml')
    modes = {'chart-from-data', 'figure-blueprint', 'figure-audit', 'figure-revision'}
    if not all(re.search(rf'^      {mode}:', figure, re.M) for mode in modes):
        issues.append(('FAIL', 'Missing figure mode declarations'))
    return issues or [('PASS', 'Evidence, reference, acceptance and section enums align')]


def run_checks(root: Path) -> list:
    if not root.is_dir():
        return [('FAIL', f'Not a directory: {root}')]
    issues = check_links(root) + check_contract_enums(root)
    noise = list(root.rglob('*.pyc')) + list(root.rglob('__pycache__'))
    issues += ([('FAIL', f'Package noise: {p.relative_to(root)}') for p in noise]
               if noise else [('PASS', 'No Python cache artifacts in skills')])
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-root', required=True)
    args = parser.parse_args()
    issues = run_checks(Path(args.skills_root))
    print('Static skill contract check — NOT behavior or fact validation')
    for level, message in issues:
        print(f'[{level}] {message}')
    counts = {level: sum(item[0] == level for item in issues) for level in ('PASS', 'FAIL')}
    print(f'Results: {counts["PASS"]} PASS | {counts["FAIL"]} FAIL')
    return 1 if counts['FAIL'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
