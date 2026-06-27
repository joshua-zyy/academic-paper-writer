#!/usr/bin/env python3
"""Convert local PDFs to Markdown with the MinerU precise parsing API.

Usage:
  python convert_pdfs_to_md_mineru_api.py refs refs_md --type ref
  python convert_pdfs_to_md_mineru_api.py refs/paper.pdf refs_md --type ref
  python convert_pdfs_to_md_mineru_api.py refs refs_md --type ref --limit 1
  python convert_pdfs_to_md_mineru_api.py refs refs_md --type ref --force

Environment:
  MINERU_API_TOKEN must contain the token created in the MinerU API console.
  MINERU_API_BASE can override the MinerU API base URL when needed.

Behavior:
  1. Accepts one local PDF file or recursively scans input_path for *.pdf.
  2. Applies for MinerU batch upload URLs, up to 50 files per batch.
  3. Uploads local PDFs via PUT, then polls batch results.
  4. Downloads each result zip and writes full.md as output_dir/<relative>.md.
  5. Copies linked images into output_dir/imgs/img_<hash>/ and rewrites links.
  6. Writes _index_ref.json or _index_style.json for the academic-citation skill.
  7. Writes mineru_api_report/_mineru_api_report.json for API task auditing and failure recovery.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import http.client
import json
import mimetypes
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


DEFAULT_API_BASE = "https://mineru.net"
MAX_BATCH_SIZE = 50
TERMINAL_STATES = {"done", "failed"}
RUNNING_STATES = {"waiting-file", "pending", "running", "converting"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".jp2", ".webp", ".gif", ".bmp"}


@dataclass(frozen=True)
class PdfJob:
    pdf_path: Path
    rel_path: Path
    md_path: Path
    images_dir: Path
    data_id: str


def safe_image_dir_name(pdf_rel_path: Path | str) -> str:
    """Return a stable image directory name for a PDF relative path."""
    normalized = Path(pdf_rel_path).with_suffix("").as_posix()
    digest = hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:12]
    return f"img_{digest}"


def stable_data_id(rel_path: Path) -> str:
    rel = rel_path.as_posix()
    digest = hashlib.sha1(rel.encode("utf-8")).hexdigest()[:24]
    return f"pdf_{digest}"


def chunked(items: list[PdfJob], size: int) -> Iterable[list[PdfJob]]:
    for start in range(0, len(items), size):
        yield items[start:start + size]


def http_json(method: str, url: str, token: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers = {"Accept": "*/*"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"请求失败 {url}: {exc.reason}") from exc

    try:
        result = json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"接口返回不是 JSON: {body[:500]}") from exc

    if result.get("code") != 0:
        raise RuntimeError(f"MinerU API 错误 code={result.get('code')} msg={result.get('msg')}")
    return result


def put_file_without_content_type(upload_url: str, file_path: Path) -> None:
    """Upload a file without a Content-Type header, as required by MinerU docs."""
    parsed = urllib.parse.urlsplit(upload_url)
    if parsed.scheme not in {"http", "https"}:
        raise RuntimeError(f"不支持的上传 URL: {upload_url}")

    connection_cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    port = parsed.port
    host = parsed.hostname
    if not host:
        raise RuntimeError(f"上传 URL 缺少 host: {upload_url}")

    path = parsed.path or "/"
    if parsed.query:
        path += f"?{parsed.query}"

    conn = connection_cls(host, port=port, timeout=180)
    try:
        size = file_path.stat().st_size
        conn.putrequest("PUT", path, skip_host=True, skip_accept_encoding=True)
        conn.putheader("Host", parsed.netloc)
        conn.putheader("Content-Length", str(size))
        conn.endheaders()
        with file_path.open("rb") as fh:
            while True:
                chunk = fh.read(1024 * 1024)
                if not chunk:
                    break
                conn.send(chunk)
        response = conn.getresponse()
        body = response.read().decode("utf-8", errors="replace")
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(f"上传失败 HTTP {response.status}: {body[:500]}")
    finally:
        conn.close()


def download_file(url: str, target: Path, attempts: int = 5) -> None:
    request = urllib.request.Request(url, headers={"Accept": "*/*"})
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=180) as response, target.open("wb") as fh:
                shutil.copyfileobj(response, fh)
            return
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"下载失败 HTTP {exc.code}: {detail[:500]}")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = RuntimeError(f"下载失败: {exc}")

        if attempt < attempts:
            time.sleep(min(2 ** attempt, 30))

    curl_exe = shutil.which("curl.exe") or shutil.which("curl")
    if curl_exe:
        result = subprocess.run(
            [curl_exe, "-L", "--retry", "5", "--retry-delay", "2", "--output", str(target), url],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and target.exists() and target.stat().st_size > 0:
            return
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"{last_error}; curl fallback failed: {detail[:500]}")

    raise RuntimeError(str(last_error))


def safe_extract_zip(zip_path: Path, extract_dir: Path) -> None:
    extract_dir.mkdir(parents=True, exist_ok=True)
    root = extract_dir.resolve()
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            normalized = PurePosixPath(info.filename)
            if normalized.is_absolute() or ".." in normalized.parts:
                raise RuntimeError(f"结果 zip 包含不安全路径: {info.filename}")
            target = (root / Path(*normalized.parts)).resolve()
            if not str(target).startswith(str(root)):
                raise RuntimeError(f"结果 zip 包含越界路径: {info.filename}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as source, target.open("wb") as dest:
                shutil.copyfileobj(source, dest)


def find_markdown_file(extract_dir: Path) -> Path:
    candidates = list(extract_dir.rglob("full.md"))
    if candidates:
        return candidates[0]
    candidates = sorted(extract_dir.rglob("*.md"))
    if candidates:
        return candidates[0]
    raise RuntimeError("结果 zip 中未找到 Markdown 文件")


def copy_linked_asset(link: str, source_md: Path, images_dir: Path, counter: int) -> tuple[str, int]:
    parsed = urllib.parse.urlsplit(link)
    if parsed.scheme in {"http", "https", "data"}:
        return link, counter

    raw_path = urllib.parse.unquote(parsed.path)
    if not raw_path:
        return link, counter

    source_path = (source_md.parent / raw_path).resolve()
    if not source_path.exists() or not source_path.is_file():
        return link, counter

    suffix = source_path.suffix.lower()
    if suffix not in IMAGE_SUFFIXES:
        guessed, _ = mimetypes.guess_type(str(source_path))
        if not guessed or not guessed.startswith("image/"):
            return link, counter

    images_dir.mkdir(parents=True, exist_ok=True)
    target_name = f"img_{counter:03d}{suffix or '.png'}"
    counter += 1
    target = images_dir / target_name
    shutil.copy2(source_path, target)
    return f"{images_dir.name}/{target_name}", counter


def rewrite_markdown_images(md_content: str, source_md: Path, md_path: Path, images_dir: Path) -> str:
    output_images_ref = os.path.relpath(images_dir, md_path.parent).replace("\\", "/")
    temp_images_dir = images_dir.parent / f"__tmp_{images_dir.name}"
    if temp_images_dir.exists():
        shutil.rmtree(temp_images_dir)
    temp_images_dir.mkdir(parents=True, exist_ok=True)

    counter = 1

    def replace_markdown(match: re.Match[str]) -> str:
        nonlocal counter
        alt, link = match.group(1), match.group(2).strip()
        new_link, counter = copy_linked_asset(link, source_md, temp_images_dir, counter)
        if new_link == link:
            return match.group(0)
        return f"![{alt}]({output_images_ref}/{new_link.split('/', 1)[1]})"

    md_content = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_markdown, md_content)

    def replace_html_img(match: re.Match[str]) -> str:
        nonlocal counter
        quote, link = match.group(1), html.unescape(match.group(2).strip())
        new_link, counter = copy_linked_asset(link, source_md, temp_images_dir, counter)
        if new_link == link:
            return match.group(0)
        rewritten = f"{output_images_ref}/{new_link.split('/', 1)[1]}"
        return match.group(0).replace(f"src={quote}{match.group(2)}{quote}", f"src={quote}{rewritten}{quote}")

    md_content = re.sub(r"src=([\'\"])([^\'\"]+)\1", replace_html_img, md_content)

    if images_dir.exists():
        shutil.rmtree(images_dir)
    if any(temp_images_dir.iterdir()):
        temp_images_dir.rename(images_dir)
    else:
        shutil.rmtree(temp_images_dir)

    return md_content


def extract_metadata(text: str, pdf_stem: str) -> dict[str, str]:
    lines = text.strip().splitlines()
    title = pdf_stem.replace("-", " ").replace("_", " ").strip()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            break
    first_500 = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", " ".join(lines[:20]))[:500]
    return {"title": title, "first_500_chars": first_500}


def is_up_to_date(pdf_path: Path, md_path: Path, images_dir: Path) -> bool:
    if not md_path.exists():
        return False
    pdf_mtime = pdf_path.stat().st_mtime
    if md_path.stat().st_mtime < pdf_mtime:
        return False
    if not images_dir.exists():
        md_content = md_path.read_text(encoding="utf-8")
        return not re.search(r"!\[[^\]]*\]\([^)]+\)|<img\b", md_content, flags=re.IGNORECASE)
    for image in images_dir.rglob("*"):
        if image.is_file() and image.stat().st_mtime < pdf_mtime:
            return False
    return True


def write_result_from_zip(job: PdfJob, zip_url: str, temp_root: Path) -> str:
    zip_path = temp_root / f"{job.data_id}.zip"
    extract_dir = temp_root / job.data_id
    download_file(zip_url, zip_path)
    safe_extract_zip(zip_path, extract_dir)

    source_md = find_markdown_file(extract_dir)
    md_content = source_md.read_text(encoding="utf-8")
    md_content = rewrite_markdown_images(md_content, source_md, job.md_path, job.images_dir)

    if not md_content.strip():
        raise RuntimeError("结果 Markdown 为空")

    job.md_path.parent.mkdir(parents=True, exist_ok=True)
    job.md_path.write_text(md_content, encoding="utf-8")
    return md_content


def submit_batch(jobs: list[PdfJob], token: str, args: argparse.Namespace) -> tuple[str, list[str]]:
    files = []
    for job in jobs:
        file_entry: dict[str, Any] = {
            "name": job.pdf_path.name,
            "data_id": job.data_id,
            "is_ocr": args.ocr,
        }
        if args.page_ranges:
            file_entry["page_ranges"] = args.page_ranges
        files.append(file_entry)

    payload: dict[str, Any] = {
        "files": files,
        "model_version": args.model_version,
        "language": args.language,
        "enable_formula": not args.disable_formula,
        "enable_table": not args.disable_table,
    }
    if args.extra_format:
        payload["extra_formats"] = args.extra_format

    api_base = args.api_base.rstrip("/")
    result = http_json("POST", f"{api_base}/api/v4/file-urls/batch", token=token, payload=payload)
    data = result["data"]
    batch_id = data["batch_id"]
    upload_urls = data["file_urls"]
    if len(upload_urls) != len(jobs):
        raise RuntimeError(f"上传链接数量不匹配: {len(upload_urls)} != {len(jobs)}")
    return batch_id, upload_urls


def poll_batch(batch_id: str, token: str, args: argparse.Namespace) -> list[dict[str, Any]]:
    deadline = time.time() + args.timeout
    last_state_summary = ""
    api_base = args.api_base.rstrip("/")

    while True:
        result = http_json("GET", f"{api_base}/api/v4/extract-results/batch/{batch_id}", token=token)
        data = result["data"]
        results = data.get("extract_result", [])
        states: dict[str, int] = {}
        for item in results:
            state = item.get("state", "unknown")
            states[state] = states.get(state, 0) + 1

        state_summary = ", ".join(f"{key}:{value}" for key, value in sorted(states.items()))
        if state_summary != last_state_summary:
            print(f"  batch {batch_id}: {state_summary}")
            last_state_summary = state_summary

        if results and all(item.get("state") in TERMINAL_STATES for item in results):
            return results

        if any(item.get("state") not in TERMINAL_STATES | RUNNING_STATES for item in results):
            return results

        if time.time() >= deadline:
            raise TimeoutError(f"轮询超时: batch_id={batch_id}")

        time.sleep(args.poll_interval)


def find_pdf_files(input_path: Path, limit: int | None) -> tuple[Path, list[Path]]:
    if input_path.is_file():
        if input_path.suffix.lower() != ".pdf":
            raise ValueError(f"输入文件不是 PDF: {input_path}")
        return input_path.parent, [input_path]
    if not input_path.is_dir():
        raise ValueError(f"输入路径不存在: {input_path}")

    pdf_files = sorted(input_path.rglob("*.pdf"))
    if limit:
        pdf_files = pdf_files[:limit]
    return input_path, pdf_files


def build_jobs(input_root: Path, pdf_files: list[Path], output_path: Path, args: argparse.Namespace) -> tuple[list[PdfJob], list[dict[str, str]]]:
    jobs: list[PdfJob] = []
    index: list[dict[str, str]] = []
    for pdf_path in pdf_files:
        rel_path = pdf_path.relative_to(input_root)
        md_rel = rel_path.with_suffix(".md")
        md_path = output_path / md_rel
        images_dir = output_path / "imgs" / safe_image_dir_name(rel_path)

        if not args.force and is_up_to_date(pdf_path, md_path, images_dir):
            existing_text = md_path.read_text(encoding="utf-8")
            meta = extract_metadata(existing_text, pdf_path.stem)
            meta["filename"] = md_rel.as_posix()
            meta["images_dir"] = f"imgs/{images_dir.name}/" if images_dir.exists() else ""
            index.append(meta)
            print(f"  skip {rel_path}")
            continue

        jobs.append(PdfJob(pdf_path, rel_path, md_path, images_dir, stable_data_id(rel_path)))

    return jobs, index


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PDF -> Markdown via MinerU precise parsing API")
    parser.add_argument("input_path", help="本地 PDF 文件或文献库目录（目录会递归扫描）")
    parser.add_argument("output_dir", help="输出目录（MD 文件保持相对路径写入）")
    parser.add_argument("--type", choices=["ref", "style"], default="ref",
                        help="索引类型：ref 写 _index_ref.json，style 写 _index_style.json")
    parser.add_argument("--token-env", default="MINERU_API_TOKEN", help="保存 MinerU API Token 的环境变量名")
    parser.add_argument("--api-base", default=os.environ.get("MINERU_API_BASE", DEFAULT_API_BASE),
                        help="MinerU API base URL，默认读取 MINERU_API_BASE 或 https://mineru.net")
    parser.add_argument("--model-version", choices=["pipeline", "vlm", "MinerU-HTML"], default="vlm",
                        help="MinerU 模型版本；PDF 推荐 vlm")
    parser.add_argument("--language", default="en", help="文档语言，英文论文建议 en；可按 MinerU 文档改为 ch 等")
    parser.add_argument("--ocr", action="store_true", help="启用 OCR，默认关闭")
    parser.add_argument("--disable-formula", action="store_true", help="关闭公式识别，默认开启")
    parser.add_argument("--disable-table", action="store_true", help="关闭表格识别，默认开启")
    parser.add_argument("--extra-format", action="append", choices=["docx", "html", "latex"],
                        help="额外导出格式，可重复传入；Markdown/JSON 默认导出")
    parser.add_argument("--page-ranges", help="页码范围，例如 1-10 或 2,4-6")
    parser.add_argument("--batch-size", type=int, default=10, help="每批上传数量，最大 50")
    parser.add_argument("--poll-interval", type=int, default=15, help="轮询间隔秒数")
    parser.add_argument("--timeout", type=int, default=3600, help="每个 batch 最大等待秒数")
    parser.add_argument("--limit", type=int, help="只处理前 N 个 PDF，便于试跑")
    parser.add_argument("--force", action="store_true", help="强制重新转换，忽略增量跳过判断")
    parser.add_argument("--debug-save-urls", action="store_true",
                        help="调试失败任务时保存 MinerU 返回的结果下载 URL；默认不保存签名 URL")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.batch_size < 1 or args.batch_size > MAX_BATCH_SIZE:
        print(f"错误: --batch-size 必须在 1 到 {MAX_BATCH_SIZE} 之间。")
        return 2

    if args.limit is not None and args.limit < 1:
        print("错误: --limit 必须是正整数。")
        return 2

    token = os.environ.get(args.token_env)
    if not token:
        print(f"错误: 未设置环境变量 {args.token_env}。请先设置 MinerU API Token。")
        return 2

    input_path = Path(args.input_path).resolve()
    output_path = Path(args.output_dir).resolve()
    try:
        input_root, pdf_files = find_pdf_files(input_path, args.limit)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 2

    output_path.mkdir(parents=True, exist_ok=True)
    jobs, index = build_jobs(input_root, pdf_files, output_path, args)
    if not jobs and not index:
        print(f"未找到 PDF 文件: {input_path}")
        return 0

    stats = {"total": len(jobs) + len(index), "converted": 0, "skipped": len(index), "failed": 0}
    report: list[dict[str, Any]] = []
    jobs_by_data_id = {job.data_id: job for job in jobs}

    print(f"待提交 {len(jobs)} 个 PDF，已跳过 {len(index)} 个。\n")

    with tempfile.TemporaryDirectory(prefix="mineru_api_") as temp_dir_str:
        temp_root = Path(temp_dir_str)
        for batch_jobs in chunked(jobs, args.batch_size):
            print(f"提交 batch: {len(batch_jobs)} 个文件")
            batch_id, upload_urls = submit_batch(batch_jobs, token, args)

            for job, upload_url in zip(batch_jobs, upload_urls):
                print(f"  upload {job.rel_path}")
                put_file_without_content_type(upload_url, job.pdf_path)

            results = poll_batch(batch_id, token, args)
            for item in results:
                data_id = item.get("data_id")
                if not isinstance(data_id, str):
                    report.append({"batch_id": batch_id, "state": "missing-data-id", "raw": item})
                    stats["failed"] += 1
                    continue
                job = jobs_by_data_id.get(data_id)
                if not job:
                    report.append({"batch_id": batch_id, "state": "unknown-job", "raw": item})
                    stats["failed"] += 1
                    continue

                state = item.get("state")
                if state != "done":
                    stats["failed"] += 1
                    err_msg = item.get("err_msg", "")
                    report.append({
                        "batch_id": batch_id,
                        "filename": job.rel_path.as_posix(),
                        "data_id": data_id,
                        "state": state,
                        "err_msg": err_msg,
                    })
                    print(f"  fail {job.rel_path}: {state} {err_msg}")
                    continue

                try:
                    md_text = write_result_from_zip(job, item["full_zip_url"], temp_root)
                    meta = extract_metadata(md_text, job.pdf_path.stem)
                    meta["filename"] = job.rel_path.with_suffix(".md").as_posix()
                    meta["images_dir"] = f"imgs/{job.images_dir.name}/" if job.images_dir.exists() else ""
                    index.append(meta)
                    stats["converted"] += 1
                    report.append({
                        "batch_id": batch_id,
                        "filename": job.rel_path.as_posix(),
                        "data_id": data_id,
                        "state": "done",
                        "md": meta["filename"],
                        "images_dir": meta["images_dir"],
                    })
                    print(f"  done {job.rel_path}")
                except Exception as exc:
                    stats["failed"] += 1
                    failure_record = {
                        "batch_id": batch_id,
                        "filename": job.rel_path.as_posix(),
                        "data_id": data_id,
                        "state": "postprocess-failed",
                        "err_msg": str(exc),
                    }
                    if args.debug_save_urls:
                        failure_record["full_zip_url"] = item.get("full_zip_url", "")
                    else:
                        failure_record["has_full_zip_url"] = bool(item.get("full_zip_url"))
                    report.append(failure_record)
                    print(f"  fail {job.rel_path}: {exc}")

    index_name = "_index_ref.json" if args.type == "ref" else "_index_style.json"
    index_path = output_path / index_name
    report_dir = output_path / "mineru_api_report"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "_mineru_api_report.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n结果: {stats['total']} 总 -> {stats['converted']} 新增 + {stats['skipped']} 跳过 + {stats['failed']} 失败")
    print(f"索引文件: {index_path}")
    print(f"报告文件: {report_path}")
    return 1 if stats["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
