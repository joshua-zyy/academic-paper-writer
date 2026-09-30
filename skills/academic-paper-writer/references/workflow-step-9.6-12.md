# 验收、整合、交付与恢复

## 1. 验收调用

只使用一个 academic-reviser 角色，不模拟同行评审，不起草正文。

```yaml
scope: section             # 全文 manuscript；定向 targeted；修复后 recheck
target: results
draft_version: "当前正文内容标识"
draft_path: "实际 paper_draft.md 路径"
context: "相关已写章节与已确认主线"
evidence_ids: [E001]
source_paths: ["实际证据/图表/引用定位"]
prior_issue_ids: []
checks: "本 scope 的事实、逻辑、表达、协议描述、引用、图文一致性"
output: "shared/schemas/verification-report.md；不返回 Revised Draft"
```

验收读取真实当前产物，按需回查原文。资料缺失说明 not_checked/author_input，不把先前 PASS 或子代理自检当当前版本验收。

## 2. 主笔修订与停止

`fix` 项主 agent 修复；`author_input` 项核对或集中问作者，无法补齐保留框架与补充建议；`suggestion` 不阻塞。高成本补证交作者选择，不自动扩展实验。

修订后 recheck 仅问题与受影响范围。相同 issue_id 连续两輪没有实质进展，报告已尝试内容和分歧，让作者决定，不继续相同循环、不把接受缺口改成 passed。参考 iteration-control.md。

## 3. 整合

每节处理后更新正文与章节状态。共享主张/数字/术语变化时按 section-dependency-matrix.md 标记相关已写部分待复查；有具体修改才能触发，不为措辞无意义地重跑所有章节。

Abstract 与 Conclusion 根据已有主体内容后置写作；缺关键结果时给相应框架，不虚构完整摘要，不要求其余所有章节先 passed 才能处理。

自动模式继续下一独立部分；逐节模式集中展示本节产物与问题后等确认。

## 4. 引用、图表与全文验收

建立正文 marker → ref_id → 身份与支持记录的对应关系，去重并生成唯一正式 References。未确认候选不冒充确定引用；缺口进待补清单。min_citations 只报告建议与实际数量，不凑文献、不阻塞交付。

numeric 格式运行 citation_audit.py；输出只证明结构，不证明真实性或支持。author-year 格式脚本明确 not_checked，需人工/agent 对照清单。脚本失败应修格式；显式缺文献项可保留为降级交付，不能称已通过。

核对真实图、图注与正文；模型架构图由作者提供，缺失保留需求。生成脚本未运行不能算生成了图。

全文调用 manuscript 验收，检查跨节数据、主张、术语、协议、解释与文献、References 和图表一致性。修改影响范围再复核，不无条件重审全文。

## 5. 交付

主 agent 报告 usable_draft / partial_draft / structured_outline；正文实质程度决定等级，状态文件或文字长度不决定。列重大未解决项，允许作者选择继续补或接收现有稿。即使接收，保留真实问题状态。

交付 paper_draft.md、必要图与代码、简短待补建议。建议包含位置、缺什么、可提供的材料和写作用途。主线与证据记录供后续局部修改复用；无需默认提供 Word、LaTeX、PDF 或投稿包。

## 6. 轻量恢复状态

全文/持续多节任务主 agent 在 task_state.yaml 保存以下必要信息，无需新运行时或数据库：

```yaml
schema_version: 1
paper_root: "作者明确选择的输出根目录"
confirmed_choices:
  language: zh
  venue: null
  continuation_mode: auto
  min_citations: null              # 仅建议
  storyline: "已确认主张与主线或 blueprint 定位"
  execution_authorization: []
sections:
  - id: method
    content_status: prose         # prose | partial | outline | pending
    draft_version: "可对照实际内容的版本/标识"
    acceptance_verdict: null      # 或 passed/needs_revision/needs_author_input
    evidence_ids: [E001]
    recheck_pending: false
issues:
  - issue_id: I001
    report_locator: "当前问题报告的定位"
    unchanged_rounds: 0
next_action: "具体下一步"
delivery_level: null
```

证据、引用身份与支持映射保存在 evidence_inventory.yaml 对应命名区块，必要验收报告附在 task_state 的 acceptance_reports 中；不强制为空任务建立全套文件。

恢复先确认同一 paper_root，实际稿件、已确认主线及来源定位仍可用。文件变化或确认版本不可匹配时，把受影响部分设 recheck_pending，不重新问无变化的决定、不重做有效探查。文件路径/时间戳仅是线索，不证明内容已读或事实已验。
