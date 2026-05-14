# 图表生成规范

## Figure Contract（前置步骤）

在生成任何图表提示词或绘图代码之前，必须先完成以下 Figure Contract：

1. **Core conclusion**：用一句话陈述该图必须捍卫的论点
2. **Evidence chain**：将每个计划面板映射到该论点，删除不承载独立证据的面板
3. **Archetype**：将图分类为 `quantitative grid`、`schematic-led composite`、`image plate + quant` 或 `asymmetric mixed-modality figure`
4. **Export contract**：设定最终尺寸、可编辑文本、源数据、统计信息、图像完整性说明和导出格式

## 双路径处理

| 图类型 | 遇到占位符时 | 输出 |
|--------|:---:|------|
| 架构图/框架图 | 自动生成提示词 | 写入 `figures/figure_prompts.md`，正文占位符替换为图编号引用 |
| 数据结果图 | 自动生成 Python 绘图代码 | 代码写入 `figures/plot_{figure_id}.py`，正文保留占位符，**不自动执行** |

## 绘图代码规范

生成的 Python 绘图代码必须遵循以下规范：

1. **强制初始化**（必须在脚本最前面）：
   ```python
   plt.rcParams['font.family'] = 'sans-serif'
   plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
   plt.rcParams['svg.fonttype'] = 'none'
   ```
2. **配色板**：使用学术色板（blue_main=#0F4D92, green_3=#8BCF8B, red_strong=#B64342, teal=#42949E, violet=#9A4D8E），同一方法在不同面板中保持颜色一致
3. **导出格式**：SVG（主要）+ PNG 300dpi（次要预览），文本保持可编辑
4. **多面板架构**：遵循 overview → deviation → relationship 三层递进，反冗余检查（无两个面板回答同一科学问题）
5. **简洁风格**：仅保留左+下 spine，frameless legend，tight_layout
