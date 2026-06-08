#!/usr/bin/env python3
"""批量将 PDF 文献转为 Markdown 格式（增量转换，含图片提取）。

用法:
  参考文献库：python scripts/convert-pdfs-to-md.py <input_dir> <output_dir> --type ref
  风格文献库：python scripts/convert-pdfs-to-md.py <input_dir> <output_dir> --type style

依赖:
  pip install pymupdf4llm

行为:
  1. 递归扫描 input_dir 下所有 *.pdf
  2. 保持相对目录结构写入 output_dir（.pdf → .md）
  3. 每个 PDF 的图片提取到 <stem>_images/ 子目录（与 .md 同级）
  4. MD 中图片引用为相对路径 ![](<stem>_images/xxx.png)
  5. 若 .md 及对应图片目录均存在且不比 .pdf 旧 → 跳过（增量）
  6. 在 output_dir 生成索引文件（--type ref → _index_ref.json，--type style → _index_style.json）
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Optional


MIN_PYTHON = (3, 10)


def ensure_supported_python() -> None:
    if sys.version_info < MIN_PYTHON:
        current = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        required = ".".join(str(part) for part in MIN_PYTHON)
        print(f"错误: pymupdf4llm 需要 Python {required}+，当前环境为 Python {current}。")
        print("请切换到 Python 3.10+ 环境后再执行 PDF 转 Markdown。")
        sys.exit(1)


ensure_supported_python()

try:
    import pymupdf4llm
except ImportError:
    print("错误: 需要 pymupdf4llm 库。请在当前 Python 环境中运行:")
    print("  python -m pip install pymupdf4llm")
    sys.exit(1)


def convert_pdf_to_md(pdf_path: Path, md_path: Path, images_dir: Path) -> Optional[str]:
    md_path.parent.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    md_content = pymupdf4llm.to_markdown(
        str(pdf_path),
        write_images=True,
        image_path=str(images_dir),
        image_format="png",
        dpi=300,
    )

    md_content = re.sub(
        r'!\[([^\]]*)\]\([^)]*' + re.escape(images_dir.name) + r'[\\/]([^)]+)\)',
        r'![\1](' + images_dir.name + r'/\2)',
        md_content,
    )

    if not md_content or not md_content.strip():
        return None

    md_path.write_text(md_content, encoding="utf-8")
    return md_content


def is_up_to_date(pdf_path: Path, md_path: Path, images_dir: Path) -> bool:
    if not md_path.exists():
        return False
    pdf_mtime = pdf_path.stat().st_mtime
    if md_path.stat().st_mtime < pdf_mtime:
        return False
    if images_dir.exists():
        for img in images_dir.rglob('*'):
            if img.is_file() and img.stat().st_mtime < pdf_mtime:
                return False
    return True


def extract_metadata(text: str, pdf_stem: str) -> dict:
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
            first_500 = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', " ".join(lines[:20]))[:500]
            break
    return {"title": title, "first_500_chars": first_500}


def main():
    parser = argparse.ArgumentParser(description="PDF → Markdown 批量转换（增量，含图片提取）")
    parser.add_argument("input_dir", help="本地 PDF 文献库目录（递归扫描）")
    parser.add_argument("output_dir", help="输出目录（MD 文件将保持相对路径写入）")
    parser.add_argument("--type", choices=["ref", "style"], default="ref",
                        help="文献库类型：ref=参考文献库（_index_ref.json），style=风格文献库（_index_style.json）")
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

    index = []
    stats = {"total": len(pdf_files), "converted": 0, "skipped": 0, "failed": 0}

    print(f"扫描到 {len(pdf_files)} 个 PDF\n")

    for pdf_path in pdf_files:
        rel_path = pdf_path.relative_to(input_path)
        md_path = output_path / rel_path.with_suffix(".md")
        images_dir = md_path.parent / f"{pdf_path.stem}_images"

        if is_up_to_date(pdf_path, md_path, images_dir):
            stats["skipped"] += 1
            try:
                existing_text = md_path.read_text(encoding="utf-8")
                meta = extract_metadata(existing_text, pdf_path.stem)
                meta["filename"] = str(rel_path.with_suffix(".md"))
                meta["images_dir"] = f"{pdf_path.stem}_images/" if images_dir.exists() else ""
                index.append(meta)
            except Exception:
                pass
            print(f"  ⏭ {rel_path}")
            continue

        if images_dir.exists():
            shutil.rmtree(images_dir)

        try:
            text = convert_pdf_to_md(pdf_path, md_path, images_dir)
            if text is None:
                stats["failed"] += 1
                print(f"  ✗ {rel_path} (转换结果为空)")
                continue
            meta = extract_metadata(text, pdf_path.stem)
            meta["filename"] = str(rel_path.with_suffix(".md"))
            meta["images_dir"] = f"{pdf_path.stem}_images/" if images_dir.exists() else ""
            index.append(meta)
            stats["converted"] += 1
            print(f"  ✓ {rel_path}")
        except Exception as e:
            stats["failed"] += 1
            print(f"  ✗ {rel_path} ({e})")

    index_path = output_path / ("_index_ref.json" if args.type == "ref" else "_index_style.json")
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n结果: {stats['total']} 总 → {stats['converted']} 新增 + {stats['skipped']} 跳过 + {stats['failed']} 失败")
    print(f"索引文件: {index_path}")


if __name__ == "__main__":
    main()