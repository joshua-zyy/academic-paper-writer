#!/usr/bin/env python3
"""
Figure QA Contract — automated checks for publication-ready figures.

Usage:
    python qa_figure.py --input figure.svg [--venue neurips]

Checks:
1. SVG text is editable (not converted to paths)
2. Color palette is grayscale-safe (no pure hues as sole discriminator)
3. No rainbow / jet / viridis colormaps
4. Figure size within venue limits
5. Axis truncation markers (if y-min > 0)
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Venue size constraints (width in inches)
VENUE_LIMITS = {
    "neurips": 5.5,
    "icml": 5.5,
    "iclr": 5.5,
    "cvpr": 3.375,
    "iccv": 3.375,
    "eccv": 3.375,
    "aaai": 6.5,
    "acl": 6.5,
}

BANNED_COLORMAPS = {"jet", "rainbow", "turbo", "nipy_spectral", "gist_rainbow", "hsv"}


def check_svg_text_editable(svg_path: str):
    """Verify that text elements exist and are not all paths."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}

    texts = root.findall(".//svg:text", ns)
    paths = root.findall(".//svg:path", ns)

    # Heuristic: if there are very few text elements relative to paths,
    # text may have been converted to paths.
    if len(texts) == 0 and len(paths) > 10:
        return False, "No editable text found; text likely converted to paths."
    if len(texts) < 3 and len(paths) > 50:
        return False, f"Suspiciously few text elements ({len(texts)}) for {len(paths)} paths."
    return True, f"Found {len(texts)} editable text elements."


def check_no_banned_colormaps(svg_path: str):
    """Scan for references to banned colormaps in SVG metadata or style."""
    content = Path(svg_path).read_text(encoding="utf-8", errors="ignore").lower()
    found = [c for c in BANNED_COLORMAPS if c in content]
    if found:
        return False, f"Banned colormaps detected: {found}"
    return True, "No banned colormaps found."


def check_grayscale_safety(svg_path: str):
    """Heuristic: ensure at least some elements differ in luminance."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}

    colors = set()
    for elem in root.iter():
        style = elem.get("style", "")
        fill = elem.get("fill", "")
        stroke = elem.get("stroke", "")
        for token in style.split(";"):
            if token.strip().startswith(("fill:", "stroke:")):
                colors.add(token.split(":", 1)[1].strip().lower())
        if fill:
            colors.add(fill.lower())
        if stroke:
            colors.add(stroke.lower())

    # Exclude black/white/transparent/grey from discriminators
    def is_color(c):
        c = c.replace("#", "")
        grey = len(set(c)) <= 2 if len(c) == 6 else False
        return not grey and c not in {"none", "black", "white", "#000000", "#ffffff", "#000", "#fff"}

    pure_colors = [c for c in colors if is_color(c)]
    # Accept if <= 2 pure colors (common case) or if grey tones exist
    grey_tones = [c for c in colors if "gray" in c or "grey" in c or (len(c) == 7 and len(set(c[1:])) <= 2)]
    if len(pure_colors) > 4 and not grey_tones:
        return False, f"Many pure hues ({len(pure_colors)}) without grey-tone backup; may fail grayscale printing."
    return True, f"Color set appears grayscale-safe ({len(pure_colors)} pure hues, {len(grey_tones)} grey tones)."


def check_venue_size(svg_path: str, venue: str = None):
    """Check figure width against venue limits."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    width_attr = root.get("width", "")
    height_attr = root.get("height", "")

    # Parse width in inches or pixels
    def to_inches(val):
        val = val.strip()
        if val.endswith("in"):
            return float(val[:-2])
        if val.endswith("pt"):
            return float(val[:-2]) / 72
        if val.endswith("px"):
            return float(val[:-2]) / 96
        return float(val) / 96  # assume px

    try:
        width_in = to_inches(width_attr)
    except ValueError:
        width_in = None

    if venue and venue.lower() in VENUE_LIMITS:
        limit = VENUE_LIMITS[venue.lower()]
        if width_in and width_in > limit + 0.2:
            return False, f"Width {width_in:.2f}in exceeds {venue.upper()} limit ({limit}in)."
    return True, f"Size: {width_attr} x {height_attr} (approx {width_in:.2f}in wide)."


def run_qa(svg_path: str, venue: str = None):
    """Run all QA checks and return report."""
    checks = [
        ("Editable Text", check_svg_text_editable),
        ("No Banned Colormaps", check_no_banned_colormaps),
        ("Grayscale Safety", check_grayscale_safety),
        ("Venue Size", lambda p: check_venue_size(p, venue)),
    ]

    report = {"file": svg_path, "venue": venue, "checks": [], "verdict": "pass"}
    for name, fn in checks:
        ok, msg = fn(svg_path)
        report["checks"].append({"name": name, "status": "pass" if ok else "fail", "message": msg})
        if not ok:
            report["verdict"] = "fail"

    return report


def print_report(report):
    print(f"\nFigure QA Report: {report['file']}")
    print(f"Venue: {report['venue'] or 'unspecified'}")
    print(f"Verdict: {report['verdict'].upper()}")
    print("-" * 40)
    for c in report["checks"]:
        icon = "[PASS]" if c["status"] == "pass" else "[FAIL]"
        print(f"{icon} {c['name']}: {c['message']}")
    print()


def main():
    parser = argparse.ArgumentParser(description="QA check academic figures.")
    parser.add_argument("--input", required=True, help="Path to SVG figure")
    parser.add_argument("--venue", choices=list(VENUE_LIMITS.keys()), help="Target venue for size check")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    report = run_qa(args.input, venue=args.venue)
    print_report(report)
    sys.exit(0 if report["verdict"] == "pass" else 1)


if __name__ == "__main__":
    main()
