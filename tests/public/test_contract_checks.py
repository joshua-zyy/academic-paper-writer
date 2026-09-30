"""Offline static-contract regressions; no agent/scientific-quality claims."""
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('contract_checks', ROOT / 'scripts/check_schemas.py')
assert spec is not None and spec.loader is not None
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


class ContractCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.skills = Path(self.tmp.name) / 'skills'
        shutil.copytree(ROOT / 'skills', self.skills)

    def failures(self):
        return [message for level, message in checks.run_checks(self.skills) if level == 'FAIL']

    def change(self, path, old, new):
        target = self.skills / path
        text = target.read_text(encoding='utf-8')
        self.assertEqual(text.count(old), 1, old)
        target.write_text(text.replace(old, new), encoding='utf-8')

    def test_current_contracts(self):
        self.assertEqual(self.failures(), [])

    def test_empty_tree_is_not_a_pass(self):
        shutil.rmtree(self.skills)
        self.skills.mkdir()
        self.assertTrue(self.failures())

    def test_missing_manifest_link(self):
        (self.skills / 'academic-paper-writer/static/core/stance.md').unlink()
        self.assertTrue(any('stance.md' in m for m in self.failures()))

    def test_unknown_verdict_rejected(self):
        self.change('shared/schemas/verification-report.md',
                    'verdict: passed | needs_revision | needs_author_input',
                    'verdict: passed | needs_revision | escalated')
        self.assertTrue(any('verdict' in m for m in self.failures()))

    def test_delivery_level_not_verdict(self):
        self.change('shared/schemas/verification-report.md',
                    'delivery_level: usable_draft | partial_draft | structured_outline',
                    'delivery_level: passed | partial_draft | structured_outline')
        self.assertTrue(any('delivery_level' in m for m in self.failures()))

    def test_section_id_drift(self):
        self.change('academic-paper-writer/manifest.yaml',
                    '      results: references/section-writing-contracts.md',
                    '      main_results: references/section-writing-contracts.md')
        self.assertTrue(any('section IDs' in m for m in self.failures()))

    def test_missing_skill_is_not_silently_skipped(self):
        shutil.rmtree(self.skills / 'academic-experiments')
        self.assertTrue(any('academic-experiments' in m for m in self.failures()))

    def test_frontmatter_name_must_match_directory(self):
        self.change('academic-citation/SKILL.md', 'name: academic-citation', 'name: wrong-skill')
        self.assertTrue(any('frontmatter' in m for m in self.failures()))


if __name__ == '__main__':
    unittest.main()
