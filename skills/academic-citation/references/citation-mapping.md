# 引用映射指南

## Citation-to-Claim 映射

对每条正文使用的文献，至少记录：

| 字段 | 说明 |
|------|------|
| `title` | 论文标题 |
| `authors` | 作者列表 |
| `venue` | 发表会议/期刊 |
| `year` | 发表年份 |
| `source link` | 一级来源链接 |
| `status` | VERIFIED / UNVERIFIED |
| `why it matters` | 为什么这篇文献与本文相关 |
| `used in` | 在哪个 section 使用（Introduction / Related Work / Baseline comparison / Discussion） |
| `inline citation marker` | 正文中的引用标记（如 [1]） |

## 推荐输出格式

```md
## Verified References

1. Title: ...
   Authors: ...
   Venue: ...
   Year: ...
   Source Link: ...
   Status: VERIFIED
   Why It Matters: ...
   Used In: Introduction / Related Work / Baseline comparison / Discussion
   Inline Citation Marker: [1]
```

若只是候选而非正文已用文献，放在 `Candidate References` 中，不与 Verified References 混写。

## Exemplar Set 维护

用于章节组织学习而非直接正文引用的论文，可额外维护：

```md
## Exemplar Set

1. Title: ...
   Why exemplar: ...
   Observed structure: ...
   Reusable moves: ...
   Not reusable: ...
```

Exemplar Set 的用途是帮助写出更像该领域论文的 Introduction 或 Related Work，不是提供可复制原文。

## 正文映射规则

- 若一条文献已进入 `Verified References` 且被正文使用，则正文中**必须**出现对应的 inline citation marker
- 若正文中存在需要文献支撑的背景事实、方法比较或数据来源说明，却没有可用文献，则在该处直接保留 `[REF_NEEDED: ...]`
- 不要先生成 bibliography 再假设读者会自己猜哪些句子对应哪些参考文献
- 若目标 venue 未知，优先使用简单一致的 numeric style，例如 `[1]`, `[2]`

## 引用闭合检查

完成当前 section 后，检查：
- 需要文献支撑的段落是否有 inline citation 或 `[REF_NEEDED: ...]`
- 参考文献列表中的条目是否真的在正文中被引用
- 引用格式是否前后一致
- 是否存在"有参考文献列表但正文没有任何 inline citation"的伪完成状态
