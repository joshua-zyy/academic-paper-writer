# 占位符系统规范

## 占位符类型

| 占位符 | 用途 | 使用场景 |
|--------|------|---------|
| `[REF_NEEDED: claim/topic]` | 缺少文献支撑 | 需要引用但未找到合适文献 |
| `[FIGURE_NEEDED: purpose \| placement \| why]` | 缺少图表 | 应放置图表的位置 |
| `[TABLE_NEEDED: purpose \| columns \| why]` | 缺少表格 | 应放置表格的位置 |
| `[RESULT_NEEDED: experiment/metric/source]` | 缺少实验结果 | 需要实验数据但尚未生成 |
| `[RESULT_UNVERIFIED: claim \| why]` | 结果未核验 | 有结果但未经过 verification |
| `[METHOD_DETAIL_NEEDED: description]` | 缺少方法细节 | 方法描述中缺少关键操作或参数 |
| `[RATIONALE_NEEDED: module \| missing]` | 缺少设计理由 | 核心模块缺少设计动机说明 |
| `[DATASET_DETAIL_NEEDED: description]` | 缺少数据集细节 | 数据集信息不完整 |

## 原则

1. **禁止静默跳过** — 任何缺失信息必须用占位符标记
2. **禁止删除占位符但不补内容** — 占位符只能被真实内容替换
3. **占位符信息要丰富** — 包含足够上下文让后续能定位补什么
4. **Verification 时检查** — 剩余占位符数量是判定 passed 的条件之一
