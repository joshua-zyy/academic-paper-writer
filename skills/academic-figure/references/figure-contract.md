# Figure Contract: 出图前合约模板

`chart-from-data` 模式的 Step 3 中使用。Agent 在生成代码前，必须与用户确认此合约。

## 合约模板

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
