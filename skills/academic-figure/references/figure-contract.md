# Figure Contract: 出图前合约模板

`chart-from-data` 模式的 Step 3 与 `architecture-svg` 模式的 Step 1 中使用。Agent 在生成代码或 SVG 前，必须与用户确认对应合约。

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
- Type: [training-curve | grouped-bar | heatmap | scatter | boxplot | radar | forest | ablation]
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
- Format required: [SVG / PDF / TIFF]

### Aesthetic Preferences
- Palette: [default / custom]
- Font: [Arial / Helvetica / Times New Roman]
- Legend position: [inside / outside right / outside bottom]

### Risk Assessment
- Potential reviewer challenge: [描述]
- Mitigation: [方案]
```

## Architecture SVG Contract

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

### Layout Plan
- Layout: [left-to-right pipeline / encoder-decoder / dual-branch fusion / retrieval-augmented pipeline / graph-neural stack / training-inference split]
- Main reading path: [从哪里开始，读者按什么方向理解]
- Arrow semantics: [solid=data flow, dashed=supervision/optional/feedback 等]
- Color semantics: [数据、模块、损失、输出、外部资源]

### Unconfirmed Items
- [VERIFY_ARCH: 需要用户或代码证据确认的模块、连接或路径]

### Target Output
- File: [figures/architecture_fig<N>.svg]
- Width: [single-column / double-column / full-width]
- Caption: [yes / no]
```

若 `Unconfirmed Items` 不为空，允许生成带待确认标记的草图，但不得交付为最终投稿图。
