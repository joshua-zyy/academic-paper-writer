# Template Constraints

Build a template profile before layout edits.

## Checklist

- Main `\documentclass` and options.
- Official `.cls` or `.sty` files and whether they are venue-owned.
- Single-column, two-column, or mixed layout.
- Loaded packages affecting floats, captions, subfigures, tables, geometry, fonts, and bibliography.
- Page limit and whether references/appendix count.
- Required bibliography style and compile engine.
- Existing build command: `Makefile`, `latexmkrc`, CI config, README, or editor settings.
- Known venue restrictions on packages, margins, font sizes, caption formatting, and author anonymity.

## Common Template Signals

| Signal | Layout implication |
|---|---|
| `neurips_*.sty` | Check anonymity, package interactions, page limit, and existing caption/section formatting before adding packages |
| `acmart` | Preserve class-managed metadata, caption style, and ACM spacing rules; avoid geometry changes |
| `IEEEtran` | Be cautious with two-column floats, `figure*`, and double-column spacing; package changes often affect float behavior |

## Compatibility Rules

- Preserve official template files.
- Do not add `float`, `placeins`, `subcaption`, `caption`, `stfloats`, `dblfloatfix`, or geometry-changing packages without checking existing template compatibility.
- If the template already defines caption or float behavior, prefer local edits over package changes.
- If venue rules are unknown, state the uncertainty and avoid global layout changes.

Test package compatibility by compiling after the smallest package-related change. If the package affects float behavior globally, ask before applying it.
