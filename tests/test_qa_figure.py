import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QA_PATH = ROOT / "skills" / "academic-figure" / "scripts" / "qa_figure.py"


def load_qa_module():
    spec = importlib.util.spec_from_file_location("qa_figure", QA_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_svg(path: Path, body: str, width="5.5in", height="2.4in"):
    path.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 550 240">
{body}
</svg>
""",
        encoding="utf-8",
    )


def test_svg_with_editable_text_passes():
    qa = load_qa_module()
    svg_path = ROOT / "tests" / "tmp_editable.svg"
    try:
        write_svg(
            svg_path,
            """<rect x="30" y="80" width="120" height="50" fill="#e8f0f7" stroke="#2f5f8f" />
<text x="90" y="110" text-anchor="middle">Input features</text>
<rect x="250" y="80" width="140" height="50" fill="#f3eee4" stroke="#8a6f3d" />
<text x="320" y="110" text-anchor="middle">Fusion module</text>
""",
        )
        report = qa.run_qa(str(svg_path))
        assert report["verdict"] == "pass"
        check_names = {check["name"] for check in report["checks"]}
        assert "Editable Text" in check_names
    finally:
        svg_path.unlink(missing_ok=True)


def test_svg_with_banned_colormap_fails():
    qa = load_qa_module()
    svg_path = ROOT / "tests" / "tmp_colormap.svg"
    try:
        write_svg(
            svg_path,
            """<rect x="30" y="80" width="120" height="50" fill="url(#jet)" stroke="#2f5f8f" />
<text x="90" y="110" text-anchor="middle">Data</text>
""",
        )
        report = qa.run_qa(str(svg_path))
        check_names = {check["name"] for check in report["checks"]}
        assert "No Banned Colormaps" in check_names
    finally:
        svg_path.unlink(missing_ok=True)
