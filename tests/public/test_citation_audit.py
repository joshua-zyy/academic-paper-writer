"""Offline integrity checks do not establish citation identity or support."""
import contextlib
import io
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = runpy.run_path(str(ROOT / 'skills/academic-citation/scripts/citation_audit.py'))


class CitationAuditTests(unittest.TestCase):
    def test_unknown_reference_is_not_verified(self):
        refs = API['parse_references']('Claim [1].\n## References\n[1] Invented paper, 2099.')
        self.assertEqual(refs['1']['status'], 'UNKNOWN')

    def test_grouped_and_range_citations_are_checked(self):
        report = API['audit']('Claim [1, 2] and [3–5].\n## References\n[1] Paper.')
        self.assertEqual(report['missing_refs'], ['2', '3', '4', '5'])

    def test_explicit_unverified_does_not_pass_readiness(self):
        report = API['audit']('Claim [1].\n## References\n[1] UNVERIFIED Paper.')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(API['print_report'](report), 'needs_verification')

    def test_duplicate_and_orphan_references_fail_structure(self):
        report = API['audit']('Claim [1].\n## References\n[1] A\n[1] B\n[2] C')
        self.assertEqual(report['duplicate_refs'], ['1'])
        self.assertEqual(report['orphan_refs'], ['2'])
        self.assertEqual(report['structural_verdict'], 'fail')

    def test_body_numbered_lines_are_not_references(self):
        self.assertEqual(API['parse_references']('[1] This is a body list.'), {})

    def test_claim_of_verified_in_text_is_not_evidence(self):
        report = API['audit']('Claim [1].\n## References\n[1] VERIFIED Paper.')
        self.assertEqual(report['identity_verdict'], 'not_checked')
        self.assertEqual(report['support_verdict'], 'not_checked')

    def test_appendix_numbers_and_code_are_not_references(self):
        text = 'Code `x[9]`. Claim [1].\n## References\n[1] Paper\n## 待补充清单\n[2] TODO'
        report = API['audit'](text)
        self.assertEqual(report['total_refs'], 1)
        self.assertEqual(report['missing_refs'], [])

    def test_author_year_is_explicitly_not_checked(self):
        report = API['audit']('Claim (Smith, 2025).\n## References\nSmith (2025). Paper.', citation_style='author-year')
        self.assertEqual(report['structural_verdict'], 'not_checked')

    def test_bare_ref_needed_is_unresolved(self):
        report = API['audit']('Claim [REF_NEEDED].\n## References\n')
        self.assertEqual(report['ref_needed_count'], 1)
        self.assertEqual(report['structural_verdict'], 'fail')

    def test_duplicate_reference_sections_fail_in_report(self):
        report = API['audit']('Claim [1].\n## References\n[1] A\n## References\n[1] A')
        self.assertEqual(report['structural_verdict'], 'fail')

    def test_malformed_numeric_marker_is_not_silently_ignored(self):
        report = API['audit']('Claim [1] and [1, ].\n## References\n[1] A.')
        self.assertEqual(report['structural_verdict'], 'fail')

    def test_invalid_ranges_fail(self):
        for marker in ('[0]', '[5–3]', '[1–10000]'):
            with self.subTest(marker=marker):
                report = API['audit'](f'Claim {marker}.\n## References\n')
                self.assertEqual(report['structural_verdict'], 'fail')

    def test_cli_exit_codes_and_scope(self):
        cases = (
            ('Claim [1].\n## References\n[1] Invented.', 'numeric', 0),
            ('Claim [1, 2].\n## References\n[1] A.', 'numeric', 1),
            ('Claim [1].\n## References\n[1] UNVERIFIED A.', 'numeric', 2),
            ('Claim (Smith, 2025).', 'author-year', 2),
        )
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'draft.md'
            for text, style, expected in cases:
                with self.subTest(style=style, expected=expected):
                    source.write_text(text, encoding='utf-8')
                    result = subprocess.run([
                        sys.executable, '-B', str(ROOT / 'skills/academic-citation/scripts/citation_audit.py'),
                        '--input', str(source), '--citation-style', style,
                    ], capture_output=True, text=True)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                    self.assertIn('identity/support: NOT CHECKED', result.stdout)


if __name__ == '__main__':
    unittest.main()
