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
| 架构图/框架图 | 自动生成提示词 | 写入 `./docs/paper-drafts/figures/figure_prompts.md`，正文占位符替换为图编号引用 |
| 数据结果图 | 自动生成 Python 绘图代码 | 代码写入 `./docs/paper-drafts/figures/codes/plot_{figure_id}.py`，正文保留占位符，**不自动执行** |

> 注：数据图代码在 Step 6.4 阶段不自动执行，留待 Step 9 全文完成后统一批量执行。

## 绘图代码规范

生成的 Python 绘图代码必须遵循以下规范：

1. **强制初始化**（必须在脚本最前面）：
   ```python
   plt.rcParams['font.family'] = 'sans-serif'
   plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
   plt.rcParams['svg.fonttype'] = 'none'
   ```
2. **配色板**：使用学术色板（blue_main=#0F4D92, green_3=#8BCF8B, red_strong=#B64342, teal=#42949E, violet=#9A4D8E），同一方法在不同面板中保持颜色一致
3. **导出格式**：SVG（矢量），文字保持可编辑
4. **多面板架构**：遵循 overview → deviation → relationship 三层递进，反冗余检查（无两个面板回答同一科学问题）
5. **简洁风格**：仅保留左+下 spine，frameless legend，tight_layout

## 图片批量生成（Step 9）

全文所有核心章节 Verification 通过后，在 Step 9 统一执行图片批量生成。

### 数据图批量执行

1. 扫描 `./docs/paper-drafts/figures/codes/` 下所有 `plot_fig*.py`
2. 对每个脚本：检查 Python 环境 → 执行脚本 → 验证 SVG 输出 → 快速 QA
3. 执行失败不阻塞整体流程，记录为「待手动修复」

### 架构图批量生成

1. 读取 `./docs/paper-drafts/figures/figure_prompts.md` 中所有未生成图片的提示词
2. 若环境支持 image generation：按 architecture-image 模式逐张生成 → 保存为 `./docs/paper-drafts/figures/fig{N}_arch.png`
3. 若环境不支持：在对话中列出所有待手动生成的提示词

### 生成后验证清单

| 检查项 | 数据图 | 架构图 |
|--------|:---:|:---:|
| 文件存在且可打开 | ✅ | ✅ |
| 配色为学术色板（非 rainbow/jet） | ✅ | ✅ |
| 坐标轴标签可读、无乱码 | ✅ | — |
| 模块/连接与代码/论文描述一致 | — | ✅ |
| 输出矢量格式（SVG） | ✅ | — |
| 灰度打印可辨识 | ✅ | ✅ |
