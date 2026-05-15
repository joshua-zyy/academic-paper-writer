#!/usr/bin/env python3
"""批量将 PDF 文献转为 Markdown 格式（增量转换）。

用法:
  python scripts/convert-pdfs-to-md.py <input_dir> <output_dir>

依赖:
  pip install markitdown

行为:
  1. 递归扫描 input_dir 下所有 *.pdf
  2. 保持相对目录结构写入 output_dir（.pdf → .md）
  3. 若 .md 已存在且不比对应 .pdf 旧 → 跳过（增量）
  4. 在 output_dir 生成 _index.json 供 agent 快速搜索
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    print("错误: 需要 markitdown 库。请在当前 Python 环境中运行:")
    print("  pip install markitdown")
    print("  (如果使用 conda 环境: conda activate <环境名> && pip install markitdown)")
    print("  注意: markitdown 只能通过 pip 安装，conda install 不支持")
    sys.exit(1)


def convert_pdf_to_md(md_converter: MarkItDown, pdf_path: Path, md_path: Path) -> str | None:
    md_path.parent.mkdir(parents=True, exist_ok=True)
    result = md_converter.convert(str(pdf_path))
    text = result.text_content
    if not text or not text.strip():
        return None
    md_path.write_text(text, encoding="utf-8")
    return text


def extract_metadata(text: str, pdf_stem: str) -> dict:
    """从 MD 文本中提取基础元数据（首段/标题行）。"""
    lines = text.strip().splitlines()
    title = pdf_stem.replace("-", " ").replace("_", " ").strip()
    first_500 = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("# ") or line.startswith("#"):
            title = line.lstrip("#").strip()
            break
    for line in lines:
        if line.strip():
            first_500 = " ".join(lines[:20])[:500]
            break
    return {"title": title, "first_500_chars": first_500}


def main():
    parser = argparse.ArgumentParser(description="PDF → Markdown 批量转换（增量）")
    parser.add_argument("input_dir", help="本地 PDF 文献库目录（递归扫描）")
    parser.add_argument("output_dir", help="输出目录（MD 文件将保持相对路径写入）")
    args = parser.parse_args()

    input_path = Path(args.input_dir).resolve()
    output_path = Path(args.output_dir).resolve()

    if not input_path.is_dir():
        print(f"错误: 输入目录不存在: {input_path}")
        sys.exit(1)

    output_path.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(input_path.rglob("*.pdf"))
    if not pdf_files:
        print(f"未找到 PDF 文件: {input_path}")
        return

    md_converter = MarkItDown()
    index = []
    stats = {"total": len(pdf_files), "converted": 0, "skipped": 0, "failed": 0}

    print(f"扫描到 {len(pdf_files)} 个 PDF\n")

    for pdf_path in pdf_files:
        rel_path = pdf_path.relative_to(input_path)
        md_path = output_path / rel_path.with_suffix(".md")

        pdf_mtime = pdf_path.stat().st_mtime
        md_exists = md_path.exists()
        md_mtime = md_path.stat().st_mtime if md_exists else 0

        if md_exists and md_mtime >= pdf_mtime:
            stats["skipped"] += 1
            try:
                existing_text = md_path.read_text(encoding="utf-8")
                meta = extract_metadata(existing_text, pdf_path.stem)
                meta["filename"] = str(rel_path.with_suffix(".md"))
                index.append(meta)
            except Exception:
                pass
            print(f"  ⏭ {rel_path}")
            continue

        try:
            text = convert_pdf_to_md(md_converter, pdf_path, md_path)
            if text is None:
                stats["failed"] += 1
                print(f"  ✗ {rel_path} (转换结果为空)")
                continue
            meta = extract_metadata(text, pdf_path.stem)
            meta["filename"] = str(rel_path.with_suffix(".md"))
            index.append(meta)
            stats["converted"] += 1
            print(f"  ✓ {rel_path}")
        except Exception as e:
            stats["failed"] += 1
            print(f"  ✗ {rel_path} ({e})")

    index_path = output_path / "_index.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n结果: {stats['total']} 总 → {stats['converted']} 新增 + {stats['skipped']} 跳过 + {stats['failed']} 失败")
    print(f"索引文件: {index_path}")


if __name__ == "__main__":
    main()
