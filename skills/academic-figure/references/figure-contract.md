# Figure Contract: 出图前合约模板

`chart-from-data` 模式的 Step 3 中使用。Agent 在生成代码或 SVG 前，必须与用户确认对应合约。

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

## Manual Figure Note（非自动绘制）

模型框架图、架构图、overview 图和复杂机制图不使用本 skill 自动绘制。若论文确实需要此类图，`figure-blueprint` 只记录：

```markdown
## Manual Figure Needed

### Purpose
[该图需要帮助读者理解的机制、流程或系统结构]

### Evidence Source
- Source: [用户描述 / 论文草稿 / 代码文件 / README / 已确认图示]
- Confidence: [confirmed / partial / needs verification]

### Required Content
- [必须出现在人工绘制图中的模块、数据流、阶段或对比]

### Caption Draft
[图注草案，说明图的核心阅读路径和证据边界]

### Boundary
This is a manual figure requirement note, not an automatically generated figure, SVG, or image prompt.
```
