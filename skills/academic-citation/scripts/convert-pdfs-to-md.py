#!/usr/bin/env python3
"""PDF literature library to Markdown converter.

This skill entrypoint defaults to the MinerU precise parsing API. It delegates
to the bundled implementation in this skill package so the historical command
name remains stable for users of the open-source skill.

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


def normalize_exit_code(code: object) -> int:
    if code is None:
        return 0
    if isinstance(code, int):
        return code
    print(code)
    return 1


def run_script(script_path: Path, argv: list[str]) -> int:
    old_argv = sys.argv
    sys.argv = [str(script_path), *argv]
    try:
        try:
            runpy.run_path(str(script_path), run_name="__main__")
        except SystemExit as exc:
            return normalize_exit_code(exc.code)
        return 0
    finally:
        sys.argv = old_argv


def find_project_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "scripts" / "convert_pdfs_to_md_mineru_api.py").is_file():
            return candidate
    raise FileNotFoundError(
        "未找到项目级 MinerU 转换脚本 scripts/convert_pdfs_to_md_mineru_api.py。"
    )


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    script_path = Path(__file__).resolve()
    bundled_script = script_path.with_name("convert_pdfs_to_md_mineru_api.py")
    if bundled_script.is_file():
        return run_script(bundled_script, argv)

    try:
        project_root = find_project_root(script_path.parent)
    except FileNotFoundError as exc:
        print(f"错误: {exc}")
        return 2

    mineru_script = project_root / "scripts" / "convert_pdfs_to_md_mineru_api.py"
    return run_script(mineru_script, argv)


if __name__ == "__main__":
    raise SystemExit(main())
