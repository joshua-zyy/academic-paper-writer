# 图表生成规范

## Figure Contract（前置步骤）

在生成任何数据绘图代码之前，必须先完成以下 Figure Contract：

1. **Core conclusion**：用一句话陈述该图必须捍卫的论点
2. **Evidence chain**：将每个计划面板映射到该论点，删除不承载独立证据的面板
3. **Archetype**：将图分类为 `quantitative grid`、`schematic-led composite`、`image plate + quant` 或 `asymmetric mixed-modality figure`
4. **Export contract**：设定最终尺寸、数据图可编辑文本、源数据、统计信息、图像完整性说明和导出格式

## 图表处理路径

| 图类型 | 遇到占位符时 | 输出 |
|--------|:---:|------|
| 架构图/框架图/流程图/机制图 | 不自动绘制；记录为 `manual_figure_needed` | 在待补充清单中写明人工绘制需求、证据来源、caption 草案和边界说明；不生成图片、SVG 或生图 prompt |
| 数据结果图 | 自动生成 Python 绘图代码 | 代码写入 `./academic-paper-writer/paper-drafts/figures/codes/plot_{figure_id}.py`，正文保留占位符，**不自动执行** |

> 注：数据图代码在 Step 9.4 阶段不自动执行，留待 Step 12 全文完成后统一批量执行。

## 数据绘图代码规范

生成的 Python 绘图代码必须遵循以下规范：

1. **强制初始化**（必须在脚本最前面）：
   ```python
   plt.rcParams['font.family'] = 'sans-serif'
   plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
   plt.rcParams['svg.fonttype'] = 'none'
   ```
2. **配色板**：使用学术色板（blue_main=#0F4D92, green_3=#8BCF8B, red_strong=#B64342, teal=#42949E, violet=#9A4D8E），同一方法在不同面板中保持颜色一致
3. **导出格式**：SVG（矢量），文字保持可编辑
4. **CS/AI/ML 设计 gate**：先确认实验论证角色、claim-primary panel/shared legend/direct labels/hatch/palette，再写代码
5. **简洁风格**：仅保留左+下 spine，frameless legend，tight_layout

## 数据图批量生成（Step 12）

全文所有核心章节 Verification 通过后，在 Step 12 统一执行数据图批量生成。

### 数据图批量执行

1. 扫描 `./academic-paper-writer/paper-drafts/figures/codes/` 下所有 `plot_fig*.py`
2. 对每个脚本：检查 Python 环境 → 执行脚本 → 验证 SVG 输出 → 快速 QA
3. 执行失败不阻塞整体流程，记录为「待手动修复」

### 手工图表需求复核

1. 扫描待补充清单中的 `manual_figure_needed` 项。
2. 确认每项包含用途、证据来源、必须展示内容和 caption 草案。
3. 不调用 `academic-figure` 自动绘制模型框架图、架构图、overview 图或复杂机制图。

### 生成后验证清单

| 检查项 | 数据图 | 手工图表需求 |
|--------|:---:|:---:|
| 文件存在且可打开 | ✅ | 不适用 |
| 配色为学术色板（非 rainbow/jet） | ✅ | ✅ |
| 坐标轴标签可读、无乱码 | ✅ | — |
| 必须展示内容有证据来源 | — | ✅ |
| 输出格式合规 | SVG | 手工绘制需求记录完整 |
| 灰度打印可辨识 | ✅ | 交由人工绘图阶段检查 |
