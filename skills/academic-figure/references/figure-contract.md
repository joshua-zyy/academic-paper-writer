# Figure Contract: 出图前合约模板

`chart-from-data` 模式的 Step 3 与 `architecture-image` 模式的 Step 1 中使用。Agent 在生成代码或图片前，必须与用户确认对应合约。

## Chart Contract

```markdown
## Figure Contract

### Core Conclusion
[一句话说明此图要支持论文中的哪个 claim]

### Evidence Hierarchy
- Primary: [核心数据来源]
- Supporting: [辅助数据来源]
- Context: [baseline / reference 数据]

### Chart Archetype
- Type: [quantitative grid | hero metric + supports | ablation ladder | trend with uncertainty | distribution comparison]
- Chart type: [training-curve | grouped-bar | heatmap | scatter | boxplot | radar | forest | ablation]
- Panel count: [1 / 2 / 3+]

### Panel Mapping
| Panel | Data | Claim Supported |
|-------|------|-----------------|
| (a) | [数据描述] | [支持的 claim] |
| (b) | [数据描述] | [支持的 claim] |

### Target Venue
- Venue: [期刊/会议名]
- Column: [single / double / full page]
- Max width: [英寸]
- Format required: [SVG]

### Aesthetic Preferences
- Palette: [default / custom]
- Font: [Arial / Helvetica / Times New Roman]
- Legend position: [inside / outside right / outside bottom]

### Risk Assessment
- Potential reviewer challenge: [描述]
- Mitigation: [方案]

### Export Bundle
- Script: [plot_<figure>.py]
- Source data: [CSV/TSV path]
- Vector: [SVG]
```

## Architecture Image Contract

```markdown
## Architecture Contract

### Core Figure Claim
[一句话说明该架构图帮助读者理解什么机制、流程或系统结构]

### Evidence Source
- Source: [用户描述 / 论文草稿 / 代码文件 / README / 已确认图示]
- Confidence: [confirmed / partial / needs verification]

### Components
| ID | Label | Role | Evidence |
|----|-------|------|----------|
| C1 | [模块名] | [输入/编码器/融合/预测头/损失/检索器等] | [来源] |

### Data Flow
| From | To | Meaning | Evidence |
|------|----|---------|----------|
| C1 | C2 | [特征、token、embedding、graph message、logits 等] | [来源] |

### Image Prompt Plan
- Visual goal: [overview figure / framework figure / module detail figure / graphical abstract]
- Composition: [central framework / layered pipeline / multi-panel overview / module zoom-in]
- Label strategy: [short labels only / numbered modules / legend outside figure / no long text]
- Visual hierarchy: [核心模块、辅助模块、输入输出、监督路径如何区分]
### Style Boundary
- Style: [high-impact journal / clean scientific illustration / NMI-style low saturation]
- Avoid: [photorealistic lab scene, decorative 3D, excessive glow, unreadable text]

### Unconfirmed Items
- [VERIFY_ARCH: 需要用户或代码证据确认的模块、连接或路径]

### Target Output
- File: [./docs/paper-drafts/figures/architecture_fig<N>.png 或 .tiff]
- Size: [single-column / double-column / full-width / graphical abstract]
- Caption: [yes / no]
```

若 `Unconfirmed Items` 不为空，允许生成视觉草图，但不得交付为最终投稿图。最终交付前必须人工核对图片中的模块、连接、标签与图注。
