#!/usr/bin/env python3
"""
Academic Chart Template — reusable plotting boilerplate for CS/AI/ML papers.

Usage:
    python chart_template.py --input data.csv --output figure.svg --type line

This script is intended to be copied and adapted per figure. It enforces:
- Academic color palette (grayscale-safe)
- Editable SVG text (svg.fonttype='none')
- Figure size matching double-column venue standards
"""

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Academic style constants
# ---------------------------------------------------------------------------
PALETTE = {
    "blue_main": "#0F4D92",
    "green_3": "#8BCF8B",
    "red_strong": "#B64342",
    "teal": "#42949E",
    "violet": "#9A4D8E",
    "orange": "#E08B2D",
    "gray_neutral": "#A0A0A0",
}

PALETTE_LIST = list(PALETTE.values())

# Approximate NeurIPS/ICML double-column width in inches
DOUBLE_COL_WIDTH = 5.5  # inches
SINGLE_COL_WIDTH = 3.375  # inches
DEFAULT_HEIGHT = 3.5  # inches


def apply_pub_style():
    """Apply publication-ready matplotlib style."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "font.size": 8,
        "axes.titlesize": 9,
        "axes.labelsize": 8,
        "legend.fontsize": 7,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "svg.fonttype": "none",  # editable text in SVG
        "pdf.fonttype": 42,       # editable text in PDF
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "lines.linewidth": 1.2,
        "lines.markersize": 4,
        "legend.frameon": False,
        "legend.borderpad": 0.2,
        "legend.handletextpad": 0.3,
    })


def check_dependencies():
    """Check that required packages are available."""
    required = ["matplotlib", "numpy"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"Missing dependencies: {missing}", file=sys.stderr)
        print(f"Install with: pip install {' '.join(missing)}", file=sys.stderr)
        sys.exit(1)


def load_data(path: str):
    """Load numeric data from CSV or TSV."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    delimiter = "\t" if p.suffix in (".tsv", ".tab") else ","
    # Simple numpy load; extend to pandas if multi-column
    try:
        data = np.genfromtxt(p, delimiter=delimiter, skip_header=1)
    except Exception as e:
        raise RuntimeError(f"Failed to load {path}: {e}")
    return data


def plot_line(data, labels=None, title="", xlabel="", ylabel="", width=DOUBLE_COL_WIDTH, height=DEFAULT_HEIGHT):
    """Line plot with std band support.

    Expected data shape: (N, 2*M) where columns alternate [mean, std] per series.
    """
    fig, ax = plt.subplots(figsize=(width, height))
    num_series = data.shape[1] // 2
    x = np.arange(data.shape[0])

    for i in range(num_series):
        mean = data[:, 2 * i]
        std = data[:, 2 * i + 1] if 2 * i + 1 < data.shape[1] else np.zeros_like(mean)
        label = labels[i] if labels and i < len(labels) else f"Series {i+1}"
        color = PALETTE_LIST[i % len(PALETTE_LIST)]
        ax.plot(x, mean, label=label, color=color)
        ax.fill_between(x, mean - std, mean + std, color=color, alpha=0.15)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc="best")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


def plot_bar(data, labels=None, groups=None, title="", xlabel="", ylabel="", width=DOUBLE_COL_WIDTH, height=DEFAULT_HEIGHT):
    """Grouped bar chart with error bar support.

    Expected data shape: (num_groups, num_series) or (num_groups, 2*num_series) [mean, err].
    """
    fig, ax = plt.subplots(figsize=(width, height))
    has_err = data.shape[1] % 2 == 0 and data.shape[1] > 1
    num_series = data.shape[1] // 2 if has_err else data.shape[1]
    x = np.arange(data.shape[0])
    bar_width = 0.7 / num_series

    for i in range(num_series):
        mean = data[:, i] if not has_err else data[:, 2 * i]
        err = data[:, 2 * i + 1] if has_err else None
        label = labels[i] if labels and i < len(labels) else f"Series {i+1}"
        color = PALETTE_LIST[i % len(PALETTE_LIST)]
        offset = (i - num_series / 2 + 0.5) * bar_width
        ax.bar(x + offset, mean, bar_width, yerr=err, label=label, color=color, capsize=2)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if groups:
        ax.set_xticks(x)
        ax.set_xticklabels(groups, rotation=30, ha="right")
    ax.legend(loc="best")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return fig


def save_figure(fig, output_path: str):
    """Save figure to SVG (primary), PDF (secondary), and PNG (preview)."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    svg_path = out.with_suffix(".svg")
    pdf_path = out.with_suffix(".pdf")
    png_path = out.with_suffix(".png")

    fig.savefig(svg_path, format="svg", bbox_inches="tight")
    fig.savefig(pdf_path, format="pdf", bbox_inches="tight")
    fig.savefig(png_path, format="png", bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {svg_path}, {pdf_path}, {png_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate academic figures from data files.")
    parser.add_argument("--input", required=True, help="Path to input CSV/TSV")
    parser.add_argument("--output", required=True, help="Output base path (no extension)")
    parser.add_argument("--type", choices=["line", "bar"], default="line", help="Chart type")
    parser.add_argument("--title", default="", help="Figure title")
    parser.add_argument("--xlabel", default="", help="X-axis label")
    parser.add_argument("--ylabel", default="", help="Y-axis label")
    parser.add_argument("--labels", nargs="+", help="Series labels")
    parser.add_argument("--groups", nargs="+", help="Group labels (bar chart x-ticks)")
    parser.add_argument("--width", type=float, default=DOUBLE_COL_WIDTH, help="Figure width in inches")
    parser.add_argument("--height", type=float, default=DEFAULT_HEIGHT, help="Figure height in inches")
    args = parser.parse_args()

    check_dependencies()
    apply_pub_style()
    data = load_data(args.input)

    if args.type == "line":
        fig = plot_line(data, labels=args.labels, title=args.title, xlabel=args.xlabel, ylabel=args.ylabel,
                        width=args.width, height=args.height)
    elif args.type == "bar":
        fig = plot_bar(data, labels=args.labels, groups=args.groups, title=args.title, xlabel=args.xlabel, ylabel=args.ylabel,
                       width=args.width, height=args.height)
    else:
        raise ValueError(f"Unsupported chart type: {args.type}")

    save_figure(fig, args.output)


if __name__ == "__main__":
    main()
