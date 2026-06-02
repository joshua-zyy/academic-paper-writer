# Mode: architecture-image

Use this mode when the user provides model structure, module descriptions, code evidence, or draft Method text and wants a model framework, overview, or module-detail image.

## Workflow

1. Build an Architecture Contract from user-provided or inspected evidence.
2. Mark uncertain modules or connections with `[VERIFY_ARCH: ...]`.
3. Create an Image Prompt Spec with short labels, visual hierarchy, and caption strategy.
4. Generate the image only after the contract is explicit.
5. Verify every module, arrow, label, and caption claim against the contract.

If evidence is insufficient, return an Architecture Contract plus prompt fallback (downgrade to arch-prompt mode) instead of a factual final figure. Keep complex text as short labels or numbers in the image; move detailed explanation to captions or legends. Deliverables: Architecture Contract, prompt spec, image path or prompt fallback, caption draft, and human-verifiable checklist.
