import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_schemas.py"


def load_checker_module():
    spec = importlib.util.spec_from_file_location("check_schemas", CHECKER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_detects_hardcoded_citation_threshold(tmp_path):
    checker = load_checker_module()
    root = tmp_path / "skills"
    write(
        root / "academic-paper-writer" / "references" / "workflow-step-6.6-9.md",
        "若总数 < 35 篇，在对话中提示用户。",
    )

    issues = checker.check_min_citations_usage(root)

    assert any(level == "FAIL" and "hardcoded citation threshold" in msg for level, msg in issues)


def test_allows_configured_min_citations(tmp_path):
    checker = load_checker_module()
    root = tmp_path / "skills"
    write(
        root / "academic-paper-writer" / "references" / "workflow-step-6.6-9.md",
        "若总数 < min_citations，在对话中提示用户。",
    )

    issues = checker.check_min_citations_usage(root)

    assert issues == [("PASS", "Citation threshold uses min_citations instead of hardcoded 35")]


def test_detects_figure_debt_deadlock_language(tmp_path):
    checker = load_checker_module()
    root = tmp_path / "skills"
    write(
        root / "shared" / "schemas" / "verification-report.md",
        "figure_debt 为软约束：figure_debt = open 时 verdict 不得为 passed",
    )

    issues = checker.check_figure_debt_flow(root)

    assert any(level == "FAIL" and "figure_debt deadlock" in msg for level, msg in issues)


def test_detects_subagent_direct_file_write_conflict(tmp_path):
    checker = load_checker_module()
    root = tmp_path / "skills"
    write(
        root / "academic-paper-writer" / "references" / "workflow-step-0-4.md",
        "你已加载 academic-venue-research 子 Skill\n生成 venue-brief.md 文件\n约束: 不得修改项目中的任何文件",
    )

    issues = checker.check_subagent_file_write_ownership(root)

    assert any(level == "FAIL" and "subagent write ownership" in msg for level, msg in issues)


def test_detects_closed_evidence_gate_before_prose(tmp_path):
    checker = load_checker_module()
    root = tmp_path / "skills"
    write(
        root / "academic-paper-writer" / "references" / "workflow-step-6.6-9.md",
        "Confirm Step 6.5 `evidence_debt = closed` before executing.",
    )

    issues = checker.check_prose_gate_evidence_debt(root)

    assert any(level == "FAIL" and "Step 6.6" in msg for level, msg in issues)
