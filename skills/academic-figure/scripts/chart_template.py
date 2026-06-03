#!/usr/bin/env python3
"""
Academic Chart Template — reusable plotting boilerplate for CS/AI/ML papers.

Usage:
    python chart_template.py --input data.csv --output figure.svg --type line

This script is intended to be copied and adapted per figure. It enforces:
- Academic color palette (grayscale-safe)
- Editable SVG text (svg.fonttype='none')
- Figure size matching journal single/double-column standards
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
    "blue_secondary": "#3775BA",
    "neutral_light": "#CFCECE",
    "neutral_mid": "#767676",
    "neutral_dark": "#4D4D4D",
    "green_3": "#8BCF8B",
    "red_strong": "#B64342",
    "teal": "#42949E",
    "violet": "#9A4D8E",
    "orange": "#E08B2D",
    "gray_neutral": "#A0A0A0",
}

PALETTE_CS_AI_PASTEL = {
    "baseline_dark": "#484878",
    "baseline_mid": "#7884B4",
    "baseline_soft": "#B4C0E4",
    "ours_tiny": "#E4E4F0",
    "ours_base": "#E4CCD8",
    "ours_large": "#F0C0CC",
    "neutral_light": "#D8D8D8",
    "neutral_mid": "#A8A8A8",
    "neutral_dark": "#606060",
    "delta_up": "#2E9E44",
    "delta_down": "#E53935",
}

DEFAULT_COLORS = [
    PALETTE["blue_main"],
    PALETTE["green_3"],
    PALETTE["red_strong"],
    PALETTE["teal"],
    PALETTE["violet"],
    PALETTE["neutral_light"],
]

PALETTE_NMI_PASTEL = PALETTE_CS_AI_PASTEL  # Backward-compatible alias.

DEFAULT_COLORS_CS_AI_PASTEL = [
    PALETTE_CS_AI_PASTEL["baseline_dark"],
    PALETTE_CS_AI_PASTEL["baseline_mid"],
    PALETTE_CS_AI_PASTEL["baseline_soft"],
    PALETTE_CS_AI_PASTEL["ours_tiny"],
    PALETTE_CS_AI_PASTEL["ours_base"],
    PALETTE_CS_AI_PASTEL["ours_large"],
]

DEFAULT_COLORS_NMI_PASTEL = DEFAULT_COLORS_CS_AI_PASTEL  # Backward-compatible alias.

PALETTE_LIST = DEFAULT_COLORS_CS_AI_PASTEL

# Approximate NeurIPS/ICML double-column width in inches
DOUBLE_COL_WIDTH = 5.5  # inches
SINGLE_COL_WIDTH = 3.375  # inches
DEFAULT_HEIGHT = 3.5  # inches


def apply_pub_style(font_size=7, axes_linewidth=0.8):
    """Apply publication-ready matplotlib style."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
        "font.size": font_size,
        "axes.titlesize": font_size,
        "axes.labelsize": font_size,
        "legend.fontsize": 7,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "figure.dpi": 300,
        "savefig.dpi": 600,
        "svg.fonttype": "none",  # editable text in SVG
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.linewidth": axes_linewidth,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "lines.linewidth": 1.2,
        "lines.markersize": 4,
        "legend.frameon": False,
        "legend.borderpad": 0.2,
        "legend.handletextpad": 0.3,
    })


def add_panel_label(ax, label, x=-0.08, y=1.04, fontsize=9, color="black"):
    """Place a compact journal-style panel label near the top-left edge."""
    ax.text(
        x, y, label,
        transform=ax.transAxes,
        fontsize=fontsize,
        fontweight="bold",
        color=color,
        ha="left",
        va="bottom",
    )


def is_dark(hex_color, threshold=128):
    """Return True if a hex color is dark enough to need white text."""
    c = hex_color.lstrip("#")
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return (0.299 * r + 0.587 * g + 0.114 * b) < threshold


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
    """Save figure to SVG (vector format with editable text)."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    svg_path = out.with_suffix(".svg")
    fig.savefig(svg_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {svg_path}")


def save_pub_py(fig, filename, dpi=600):
    """Publication-style convenience wrapper for export bundles."""
    save_figure(fig, filename)


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
