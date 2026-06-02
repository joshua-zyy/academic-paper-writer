# Mode: figure-revision

Use this mode when the user provides an existing figure or plotting script and asks for color, layout, label, caption, or style changes.

## Workflow

1. Confirm revision target and requested changes.
2. Judge execution path:
   - Source Python script available → edit script, rerun, and re-export.
   - Only an image file available → provide bounded revision plan or prompt revision; do not claim unavailable editability.
   - Architecture figure → revise the prompt specification and regenerate or provide updated prompt.
3. Run QA after revision and report remaining risks.

Do not overwrite source data or existing scripts unless the user explicitly asks. Create revised artifacts with new names. After revision, the figure must still be traceable to its evidence source.
