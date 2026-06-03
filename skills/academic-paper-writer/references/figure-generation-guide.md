# 图表生成规范

## Figure Contract（前置步骤）

在生成任何图表提示词或绘图代码之前，必须先完成以下 Figure Contract：

1. **Core conclusion**：用一句话陈述该图必须捍卫的论点
2. **Evidence chain**：将每个计划面板映射到该论点，删除不承载独立证据的面板
3. **Archetype**：将图分类为 `quantitative grid`、`schematic-led composite`、`image plate + quant` 或 `asymmetric mixed-modality figure`
4. **Export contract**：设定最终尺寸、数据图可编辑文本、架构图生图/标注层需求、源数据、统计信息、图像完整性说明和导出格式

## 双路径处理

| 图类型 | 遇到占位符时 | 输出 |
|--------|:---:|------|
| 架构图/框架图/流程图/机制图 | 默认调用 `academic-figure` 的 `architecture-image`，用生图模型生成主体图片 | 图片写入 `./docs/paper-drafts/figures/fig{N}_arch.png`；必要时标注层写入 `./docs/paper-drafts/figures/fig{N}_arch_labels.svg`；正文占位符替换为图编号引用 |
| 数据结果图 | 自动生成 Python 绘图代码 | 代码写入 `./docs/paper-drafts/figures/codes/plot_{figure_id}.py`，正文保留占位符，**不自动执行** |

> 注：数据图代码在 Step 6.4 阶段不自动执行，留待 Step 9 全文完成后统一批量执行。

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

## 图片批量生成（Step 9）

全文所有核心章节 Verification 通过后，在 Step 9 统一执行图片批量生成。

### 数据图批量执行

1. 扫描 `./docs/paper-drafts/figures/codes/` 下所有 `plot_fig*.py`
2. 对每个脚本：检查 Python 环境 → 执行脚本 → 验证 SVG 输出 → 快速 QA
3. 执行失败不阻塞整体流程，记录为「待手动修复」

### 架构图生图状态复核

1. 扫描待补充清单中 `architecture-image` 项和 `./docs/paper-drafts/figures/fig*_arch.*`
2. 对已生成图片：核对 Architecture Contract、模块/连接、伪文字、分辨率和可选标注层
3. 对仍为 blocker 的图片：若当前环境可调用生图模型则重新执行 `architecture-image`；否则记录 blocker，不伪造图片路径

### 生成后验证清单

| 检查项 | 数据图 | 架构图 |
|--------|:---:|:---:|
| 文件存在且可打开 | ✅ | ✅ |
| 配色为学术色板（非 rainbow/jet） | ✅ | ✅ |
| 坐标轴标签可读、无乱码 | ✅ | — |
| 模块/连接与代码/论文描述一致 | — | ✅ |
| 输出格式合规 | SVG | 高分辨率图片 + 可选标注层 |
| 灰度打印可辨识 | ✅ | ✅ |
