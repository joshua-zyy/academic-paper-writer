#!/usr/bin/env python3
"""
Evidence Scanner — scan a project directory for experimental artifacts.

Usage:
    python evidence_scanner.py --root /path/to/project

Scans for:
1. Checkpoint files (.pth, .pt, .h5, .ckpt)
2. Log files (.log, .csv, .tsv)
3. Config files (config.*, settings.*, *.yaml, *.yml, *.json)
4. Result tables (.csv, .tsv in results/ or outputs/ directories)
5. Training scripts (train.*, main.*, run.*)
"""

import argparse
import sys
from pathlib import Path

CHECKPOINT_EXTS = {".pth", ".pt", ".h5", ".ckpt", ".pkl", ".bin"}
LOG_EXTS = {".log", ".csv", ".tsv"}
CONFIG_NAMES = {"config", "settings", "hyperparams", "args"}
CONFIG_EXTS = {".py", ".yaml", ".yml", ".json", ".toml", ".ini"}
SCRIPT_NAMES = {"train", "main", "run", "eval", "evaluate", "test", "predict"}
SCRIPT_EXTS = {".py", ".sh"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".idea", "venv", ".venv", "env"}


def scan_directory(root: Path, max_depth: int = 3) -> dict:
    checkpoints = []
    logs = []
    configs = []
    scripts = []
    result_dirs = []

    def _scan(dir_path: Path, depth: int):
        if depth > max_depth:
            return
        try:
            entries = sorted(dir_path.iterdir())
        except PermissionError:
            return

        for entry in entries:
            if entry.is_dir():
                if entry.name in SKIP_DIRS or entry.name.startswith("."):
                    continue
                name_lower = entry.name.lower()
                if name_lower in {"results", "outputs", "logs", "checkpoints", "runs", "experiments"}:
                    result_dirs.append(str(entry))
                _scan(entry, depth + 1)
            elif entry.is_file():
                suffix = entry.suffix.lower()
                stem = entry.stem.lower()

                if suffix in CHECKPOINT_EXTS:
                    size_mb = entry.stat().st_size / (1024 * 1024)
                    checkpoints.append({"path": str(entry), "size_mb": round(size_mb, 1)})
                elif suffix in LOG_EXTS and depth <= max_depth:
                    logs.append(str(entry))
                elif stem in CONFIG_NAMES and suffix in CONFIG_EXTS:
                    configs.append(str(entry))
                elif stem in SCRIPT_NAMES and suffix in SCRIPT_EXTS:
                    scripts.append(str(entry))

    _scan(root, 0)
    return {
        "project_root": str(root),
        "checkpoints": checkpoints,
        "log_files": logs[:50],
        "config_files": configs,
        "training_scripts": scripts,
        "result_directories": result_dirs,
    }


def print_report(report: dict):
    print("Evidence Inventory Scan")
    print("=" * 50)
    print(f"Project root: {report['project_root']}")
    print()

    print(f"Checkpoints ({len(report['checkpoints'])}):")
    for ckpt in report["checkpoints"][:20]:
        print(f"  {ckpt['path']} ({ckpt['size_mb']} MB)")
    if len(report["checkpoints"]) > 20:
        print(f"  ... and {len(report['checkpoints']) - 20} more")

    print(f"\nConfig files ({len(report['config_files'])}):")
    for cfg in report["config_files"]:
        print(f"  {cfg}")

    print(f"\nTraining/eval scripts ({len(report['training_scripts'])}):")
    for s in report["training_scripts"]:
        print(f"  {s}")

    print(f"\nResult directories ({len(report['result_directories'])}):")
    for d in report["result_directories"]:
        print(f"  {d}")

    print(f"\nLog/data files (first 20 of {len(report['log_files'])}):")
    for l in report["log_files"][:20]:
        print(f"  {l}")

    total = (len(report["checkpoints"]) + len(report["config_files"]) +
             len(report["training_scripts"]) + len(report["result_directories"]))
    print(f"\nSummary: {total} key artifacts found")


def main():
    parser = argparse.ArgumentParser(description="Scan project for experimental artifacts.")
    parser.add_argument("--root", required=True, help="Project root directory")
    parser.add_argument("--max-depth", type=int, default=3, help="Max scan depth")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"Error: Not a directory: {root}", file=sys.stderr)
        sys.exit(1)

    report = scan_directory(root, args.max_depth)
    print_report(report)


if __name__ == "__main__":
    main()
