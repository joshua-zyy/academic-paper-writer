# Figure Anti-Patterns

| Pattern | Problem | Correct |
|---|---|---|
| Aesthetics first | Using rainbow/jet palettes to make charts "look good" | Grayscale-safe restrained academic palette |
| No QA delivery | Code runs → delivery without review | QA Contract required: readability, data consistency, format compliance |
| Invented architecture | Prompts include non-existent module connections | Architecture from code/paper evidence only; unconfirmed items marked |
| Hardcoded paths | File paths hardcoded to developer local paths | Use relative paths or parameterized configuration |
| Delivering unchecked generated images | Image looks professional but modules/arrows may be wrong | Contract first, verify module-by-module after generation |
