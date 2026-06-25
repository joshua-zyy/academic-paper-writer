#!/usr/bin/env python3
"""PDF literature library to Markdown converter.

This skill entrypoint defaults to the MinerU precise parsing API. It delegates
to the project-level implementation at scripts/convert_pdfs_to_md_mineru_api.py
so the academic-citation skill keeps the historical command name while using
one maintained converter.

Usage:
  python .agents/skills/academic-paper-writer/skills/academic-citation/scripts/convert-pdfs-to-md.py researchPaper/refs researchPaper/refs_md --type ref
  python .agents/skills/academic-paper-writer/skills/academic-citation/scripts/convert-pdfs-to-md.py researchPaper/refs/paper.pdf researchPaper/refs_md --type ref

Environment:
  MINERU_API_TOKEN must be set. Do not hard-code the token in this file.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def find_project_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "scripts" / "convert_pdfs_to_md_mineru_api.py").is_file():
            return candidate
    raise FileNotFoundError(
        "未找到项目级 MinerU 转换脚本 scripts/convert_pdfs_to_md_mineru_api.py。"
    )


def main() -> int:
    script_path = Path(__file__).resolve()
    try:
        project_root = find_project_root(script_path.parent)
    except FileNotFoundError as exc:
        print(f"错误: {exc}")
        return 2

    mineru_script = project_root / "scripts" / "convert_pdfs_to_md_mineru_api.py"
    sys.argv = [str(mineru_script), *sys.argv[1:]]
    runpy.run_path(str(mineru_script), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
